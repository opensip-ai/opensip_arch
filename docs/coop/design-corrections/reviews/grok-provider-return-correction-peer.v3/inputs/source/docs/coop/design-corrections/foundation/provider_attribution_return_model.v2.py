"""Worker occupancy companion → TargetAttributionV2 projection.

Owning host-adapter entry is bind_worker_occupancy. Design reference, not a
host runtime. Loads only siblings of this file (current selected source).
Missing dependencies fail. No fallback to provider58 paths.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NATIVE_HERE = HERE.parent / "native"
ARTIFACTS = HERE.parents[1] / "artifacts"
TOKEN = "target-attribution-v2"


def _load(name: str, path: Path):
    if not path.is_file():
        raise FileNotFoundError(str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = _load("occ_canonical", HERE / "canonical.py")
AM = _load("occ_atom", HERE / "atom_model.v1.py")
FM = _load("occ_fault", HERE / "evaluator_fault_model.v3.py")
FP = _load("occ_fact_plane", ARTIFACTS / "check-fact-plane.py")

BATCH_SCHEMA = json.loads((NATIVE_HERE / "fact-batch.schema.v3.json").read_text(encoding="utf-8"))
COMPANION_SCHEMA = json.loads((NATIVE_HERE / "occupancy-companion.schema.v1.json").read_text(encoding="utf-8"))
RETURN_SCHEMA = json.loads((HERE / "provider-target-attribution-return.schema.v2.json").read_text(encoding="utf-8"))
TARGET_SCHEMA = json.loads((HERE / "target-attribution.schema.v2.json").read_text(encoding="utf-8"))
RETURN_SCHEMA["properties"]["records"]["items"] = TARGET_SCHEMA
BATCH_SCHEMA["properties"]["occupancyCompanions"]["items"] = COMPANION_SCHEMA
FAULTS = RETURN_SCHEMA["x-opensip-new-internal-faults"]
SCHEMA_KEYS = frozenset(FAULTS["schemaKeys"])
JOIN_KEYS = frozenset(FAULTS["joinKeys"])
ROUTE_LAW = FAULTS["publicRoute"]
ALLOWED_ORIGINS = (ROUTE_LAW["providerOrigin"], ROUTE_LAW["hostInventedOrigin"])


class ProviderReturnAdmissionError(Exception):
    def __init__(self, key: str, detail: str = ""):
        self.key = key
        self.detail = detail
        super().__init__(key + (": " + detail if detail else ""))


def raw_digest(obj) -> str:
    return hashlib.sha256(C.canonical(obj)).hexdigest()


def deterministic_cbor(value) -> bytes:
    """Exact fact-plane relation-payload CBOR. JSON UTF-8 is not this encoding."""
    return FP._deterministic_cbor(value)


def condition_for_key(key: str) -> str:
    if key in SCHEMA_KEYS:
        return ROUTE_LAW["schemaCondition"]
    if key in JOIN_KEYS:
        return ROUTE_LAW["joinCondition"]
    raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", "unknown internal key")


def public_observation(internal_key: str, origin: str, diagnostic_bytes: bytes, reference: str | None = None) -> dict:
    if origin not in ALLOWED_ORIGINS:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", "origin")
    condition = condition_for_key(internal_key)
    if internal_key.encode("utf-8") not in diagnostic_bytes:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", "diagnostic must contain internal key")
    return {
        "schemaVersion": 3,
        "condition": condition,
        "origin": origin,
        "diagnosticDigest": hashlib.sha256(diagnostic_bytes).hexdigest(),
        "reference": reference,
        "limit": None,
    }


def route_internal_key(internal_key: str, origin: str, diagnostic_bytes: bytes, reference: str | None = None) -> dict:
    observation = public_observation(internal_key, origin, diagnostic_bytes, reference)
    routed = FM.route(observation, diagnostic_bytes)
    expected_detail = ROUTE_LAW["providerDetail"] if origin == ROUTE_LAW["providerOrigin"] else ROUTE_LAW["hostDetail"]
    actual = routed["termination"]["domainDetail"]["code"]
    if actual != expected_detail:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", "public detail " + actual)
    routed["internalKey"] = internal_key
    return routed


def _canon_refs(refs: list) -> list:
    return sorted({C.canonical(x): x for x in refs}.values(), key=C.canonical)


def verify_candidate_cbor(candidate: dict) -> dict:
    decoded = candidate.get("decodedRelationPayload")
    hex_text = candidate.get("canonicalRelationPayloadHex")
    if not isinstance(decoded, dict) or not isinstance(hex_text, str):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PAYLOAD_CBOR", "vector fields")
    try:
        cbor = deterministic_cbor(decoded)
    except Exception as exc:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PAYLOAD_CBOR", str(exc)) from exc
    if hex_text != cbor.hex():
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PAYLOAD_CBOR", "hex is not deterministic-CBOR of decodedRelationPayload")
    return decoded


def _bare_universe(universe_id: str) -> str:
    if isinstance(universe_id, str) and universe_id.startswith("sha256:") and len(universe_id) == 71:
        return universe_id[7:]
    return universe_id


def _stage_spec(execution_plan: dict, stage_specs: dict, stage_id: int, plan_id: str) -> tuple[dict, dict]:
    if execution_plan.get("planId") != plan_id:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PLAN_MISMATCH", "execution_plan.planId")
    stages = execution_plan.get("stages") or []
    row = next((s for s in stages if s.get("ordinal") == stage_id), None)
    if row is None:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_NOT_IN_PLAN", str(stage_id))
    digest = row.get("stageSpecDigest")
    spec = stage_specs.get(digest)
    if not isinstance(spec, dict):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_SPEC", str(digest))
    if spec.get("planId") != plan_id:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PLAN_MISMATCH", "stage-spec.planId")
    required = (
        "schemaVersion", "planId", "producerClosure", "operation", "parameters",
        "outputDomains", "outputSchemaDigest",
    )
    if any(k not in spec for k in required):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_SPEC", "fields")
    if raw_digest({k: spec[k] for k in required}) != digest:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_SPEC", "digest")
    pc = spec.get("producerClosure")
    if not pc:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_PRODUCER", str(stage_id))
    return row, spec


def _require_receipt(receipts: list, row: dict, spec: dict) -> None:
    rec = next((r for r in (receipts or []) if r.get("ordinal") == row.get("ordinal")), None)
    if rec is None:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_RECEIPT", str(row.get("ordinal")))
    if rec.get("stageSpecDigest") != row.get("stageSpecDigest"):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_RECEIPT", "stageSpecDigest")
    if rec.get("producerClosure") != spec.get("producerClosure"):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_RECEIPT", "producerClosure")


def _require_selected_provider(closures: dict, producer_closure: str) -> None:
    if (closures.get(producer_closure) or {}).get("kind") != "provider":
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PRODUCER_NOT_PROVIDER", producer_closure)


def _fact_in_producer_view(views: dict, fact_id: str, producer_closure: str, plan_id: str) -> bool:
    for view in (views or {}).values():
        if view.get("planId") != plan_id:
            continue
        if view.get("producerClosure") != producer_closure:
            continue
        if fact_id in (view.get("facts") or []):
            return True
    return False


def _mint_correspondence(fact: dict, cand: dict, decoded: dict) -> None:
    if fact.get("relation") != cand.get("relation") or fact.get("resolution") != cand.get("resolution"):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISJOIN", "relation")
    if fact.get("sourceUniverse") != _bare_universe(cand.get("sourceUniverseId")):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISJOIN", "sourceUniverse")
    if fact.get("targetUniverse") != _bare_universe(cand.get("targetUniverseId")):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISJOIN", "targetUniverse")
    if (fact.get("payload") or {}) != decoded:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISJOIN", "payload")
    if fact.get("confidenceMillionths") != cand.get("confidenceMillionths"):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISJOIN", "confidence")
    fact_anchors = fact.get("anchors") or []
    cand_anchors = cand.get("anchors") or []
    if len(fact_anchors) != len(cand_anchors):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISJOIN", "anchors")


def project_companion_to_v2(companion: dict, fact: dict, plan_id: str, producer_closure: str) -> dict:
    return {
        "schemaVersion": 2,
        "planId": plan_id,
        "sourceFactId": fact["factId"],
        "producerClosure": producer_closure,
        "targetUniverse": fact["targetUniverse"],
        "targetNativeId": companion["targetNativeId"],
        "kind": companion["kind"],
        "occupancy": companion["occupancy"],
        "exported": companion.get("exported"),
        "logicalPath": companion.get("logicalPath"),
        "packageManifestPath": companion.get("packageManifestPath"),
        "evaluationNativeId": companion.get("evaluationNativeId"),
    }


def bind_worker_occupancy(
    batch,
    *,
    negotiated_tokens: list,
    plan_id: str,
    execution_plan: dict,
    stage_specs: dict,
    closures: dict,
    views: dict,
    minted_by_ordinal: dict,
    inventories: list,
    enumeration_plan: dict,
    stage_receipts: list | None = None,
    analyze_analysis_ordinal: int | None = None,
    prior_records: list | None = None,
):
    """Owning host-adapter entry.

    Trusted host observations (do not prove FACT-ID-V1): negotiated Hello tokens;
    retained Plan locator; execution-plan (planId + stages with stageSpecDigest);
    retained stage-spec map keyed by that digest; hostCapture.stageReceipts;
    Analyze analysisOrdinal; closure kind map; selected views with required planId;
    mint map from THIS batch as a host TCB observation of already-admitted mint;
    inventories; enumeration plan; already-captured TargetAttributionV2 prior_records.

    Provider claims: FactCandidateV1 members and OccupancyCompanionV1 occupancy fields.

    Host-filled: planId, sourceFactId, producerClosure from stage-spec, targetUniverse
    from minted fact.

    EnumerationPlan enumerator is a separate XI cell/program binding. This entry
    does not require producerClosure == enumerator.closureId.
    """
    tokens = list(negotiated_tokens or [])
    if TOKEN not in tokens:
        if batch is not None and isinstance(batch, dict) and batch.get("schemaVersion") == 3:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_UNNEGOTIATED_V3", TOKEN)
        return {
            "status": "omitted",
            "records": [],
            "hostDerivedRefs": [],
            "blobs": {},
            "delivery": "unnegotiated-fact-batch-v2",
        }
    if batch is None:
        return {
            "status": "omitted",
            "records": [],
            "hostDerivedRefs": [],
            "blobs": {},
            "delivery": "negotiated-empty-worker-return",
        }
    try:
        C.validate(BATCH_SCHEMA, batch)
    except Exception as exc:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", str(exc)) from exc
    if analyze_analysis_ordinal is not None and batch.get("analysisOrdinal") != analyze_analysis_ordinal:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_ANALYSIS_ORDINAL", str(batch.get("analysisOrdinal")))
    row, spec = _stage_spec(execution_plan, stage_specs, batch["stageId"], plan_id)
    producer_closure = spec["producerClosure"]
    _require_selected_provider(closures, producer_closure)
    if stage_receipts is not None:
        _require_receipt(stage_receipts, row, spec)
    candidates = {c["candidateOrdinal"]: c for c in batch["candidates"]}
    if len(candidates) != len(batch["candidates"]):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_DUPLICATE_CANDIDATE", "candidateOrdinal")
    records = []
    for companion in batch["occupancyCompanions"]:
        try:
            C.validate(COMPANION_SCHEMA, companion)
        except Exception as exc:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", str(exc)) from exc
        ordinal = companion["candidateOrdinal"]
        cand = candidates.get(ordinal)
        if cand is None:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_UNKNOWN_CANDIDATE", str(ordinal))
        if companion.get("targetUniverseId") != cand.get("targetUniverseId"):
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_UNIVERSE_MISMATCH", str(ordinal))
        decoded = verify_candidate_cbor(cand)
        fact = minted_by_ordinal.get(ordinal)
        if fact is None:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISSING", str(ordinal))
        if fact.get("producerClosure") != producer_closure:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_PRODUCER_MISMATCH", fact.get("factId"))
        _mint_correspondence(fact, cand, decoded)
        spec_rel = AM.REGISTRY["relations"].get(fact.get("relation")) or {}
        field = spec_rel.get("targetNativeIdField")
        if not field or decoded.get(field) != companion.get("targetNativeId"):
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH", str(ordinal))
        if (fact.get("payload") or {}).get(field) != companion.get("targetNativeId"):
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH", "fact-payload")
        if not _fact_in_producer_view(views, fact["factId"], producer_closure, plan_id):
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_FACT_NOT_IN_VIEW", fact["factId"])
        records.append(project_companion_to_v2(companion, fact, plan_id, producer_closure))
    records = sorted(records, key=lambda r: r["sourceFactId"].encode("utf-8"))
    facts = {minted_by_ordinal[o]["factId"]: minted_by_ordinal[o] for o in minted_by_ordinal}
    combined = {}
    for rec in list(prior_records or []) + records:
        fid = rec.get("sourceFactId")
        if fid in combined:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_DUPLICATE_FACT", fid)
        combined[fid] = rec
        try:
            C.validate(TARGET_SCHEMA, rec)
        except Exception as exc:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_SCHEMA", str(exc)) from exc
    atom_inputs = {
        "planId": plan_id,
        "facts": facts,
        "inventories": inventories,
        "enumerationPlan": enumeration_plan,
        "closures": closures,
        "targetAttributions": combined,
    }
    try:
        AM._admit_target_attributions(atom_inputs)
    except AM.AtomAdmissionError as exc:
        raise ProviderReturnAdmissionError(exc.key, exc.detail) from exc
    blobs = {}
    refs = []
    for rec in records:
        digest = raw_digest(rec)
        blobs[digest] = C.canonical(rec)
        refs.append({"domain": "target-attribution", "digest": digest})
    return {
        "status": "admitted",
        "records": records,
        "hostDerivedRefs": _canon_refs(refs),
        "blobs": blobs,
        "delivery": "fact-batch-v3-companion",
        "producerClosure": producer_closure,
        "stageId": batch["stageId"],
    }


def admit_provider_attribution_return(envelope, **kwargs):
    """COMPLETE58 helper is not the owning delivery."""
    origin = kwargs.pop("origin", None)
    if origin == "host-internal":
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_HOST_AUTHORED", "origin=host-internal")
    if envelope is not None and kwargs.get("batch") is None:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_UNBOUND_ENVELOPE", "no worker FactBatchV3")
    if envelope is not None:
        try:
            C.validate(RETURN_SCHEMA, envelope)
        except Exception as exc:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", str(exc)) from exc
    if "negotiated_tokens" not in kwargs:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_OWNERS_REQUIRED", "negotiated_tokens")
    keys = (
        "negotiated_tokens", "plan_id", "execution_plan", "stage_specs",
        "closures", "views", "minted_by_ordinal", "inventories", "enumeration_plan",
        "stage_receipts", "analyze_analysis_ordinal", "prior_records",
    )
    return bind_worker_occupancy(kwargs.get("batch"), **{k: kwargs[k] for k in keys if k in kwargs})
