"""Worker occupancy companion → TargetAttributionV2 projection.

Owning host-adapter entries:
  buffer_fact_batch_occupancy — ANALYZING; dispatch required; receipts/views MUST NOT be required
  capture_occupancy / bind_worker_occupancy — post-terminal; dispatch AND receipts/views required

Design reference, not a host runtime. Loads only siblings of this file and
HERE.parents[1]/artifacts/check-fact-plane.py. Missing dependencies fail.
No fallback to provider58 paths. Schemas are not mutated at import time.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

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
DISPATCH_SCHEMA = json.loads((NATIVE_HERE / "dispatch-binding.schema.v1.json").read_text(encoding="utf-8"))
RETURN_SCHEMA = json.loads((HERE / "provider-target-attribution-return.schema.v2.json").read_text(encoding="utf-8"))
TARGET_SCHEMA = json.loads((HERE / "target-attribution.schema.v2.json").read_text(encoding="utf-8"))


def _resource(schema: dict) -> Resource:
    return Resource(contents=schema, specification=DRAFT202012)


SCHEMA_REGISTRY = Registry().with_resources([
    (BATCH_SCHEMA["$id"], _resource(BATCH_SCHEMA)),
    (COMPANION_SCHEMA["$id"], _resource(COMPANION_SCHEMA)),
    (DISPATCH_SCHEMA["$id"], _resource(DISPATCH_SCHEMA)),
    (RETURN_SCHEMA["$id"], _resource(RETURN_SCHEMA)),
    (TARGET_SCHEMA["$id"], _resource(TARGET_SCHEMA)),
])

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


def validate_schema(schema, value):
    """ExactValidator with registered $id binding. Does not mutate schema dicts."""
    return C.validate(schema, value, registry=SCHEMA_REGISTRY)


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


def _require_dispatch(dispatch) -> dict:
    if not isinstance(dispatch, dict):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_DISPATCH", "required")
    try:
        validate_schema(DISPATCH_SCHEMA, dispatch)
    except Exception as exc:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_DISPATCH", str(exc)) from exc
    return dispatch


def _correlate_batch(batch: dict, dispatch: dict) -> None:
    if batch.get("stageId") != dispatch["expectedStageId"]:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_ID", str(batch.get("stageId")))
    if batch.get("analysisOrdinal") != dispatch["expectedAnalysisOrdinal"]:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_ANALYSIS_ORDINAL", str(batch.get("analysisOrdinal")))
    if batch.get("batchIndex") != dispatch["expectedBatchIndex"]:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_BATCH_INDEX", str(batch.get("batchIndex")))


def _stage_from_dispatch(execution_plan: dict, stage_specs: dict, dispatch: dict, plan_id: str) -> tuple[dict, dict]:
    if execution_plan.get("planId") != plan_id or dispatch.get("planId") != plan_id:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PLAN_MISMATCH", "planId")
    retained = dispatch["retainedStageOrdinal"]
    stages = execution_plan.get("stages") or []
    row = next((s for s in stages if s.get("ordinal") == retained), None)
    if row is None:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_NOT_IN_PLAN", str(retained))
    digest = row.get("stageSpecDigest")
    if digest != dispatch.get("stageSpecDigest"):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_SPEC", "dispatch.stageSpecDigest")
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
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_PRODUCER", str(retained))
    if pc != dispatch.get("producerClosure"):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_PRODUCER", "dispatch.producerClosure")
    return row, spec


def _require_receipt(receipts, row: dict, spec: dict) -> dict:
    if receipts is None:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_RECEIPT", "required")
    rec = next((r for r in receipts if r.get("ordinal") == row.get("ordinal")), None)
    if rec is None:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_RECEIPT", str(row.get("ordinal")))
    if rec.get("stageSpecDigest") != row.get("stageSpecDigest"):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_RECEIPT", "stageSpecDigest")
    if rec.get("producerClosure") != spec.get("producerClosure"):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_RECEIPT", "producerClosure")
    return rec


def _require_selected_provider(closures: dict, producer_closure: str) -> None:
    if (closures.get(producer_closure) or {}).get("kind") != "provider":
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PRODUCER_NOT_PROVIDER", producer_closure)


def _view_digest(view_id: str) -> str:
    if isinstance(view_id, str) and ":" in view_id:
        return view_id.split(":", 1)[1]
    return view_id


def _fact_in_producer_view(views: dict, fact_id: str, producer_closure: str, plan_id: str, receipt: dict | None) -> bool:
    if views is None:
        return False
    for view_id, view in views.items():
        if view.get("planId") != plan_id:
            continue
        if view.get("producerClosure") != producer_closure:
            continue
        if fact_id not in (view.get("facts") or []):
            continue
        if receipt is not None:
            digest = _view_digest(view_id)
            refs = receipt.get("outputRefs") or []
            if not any(r.get("domain") == "view" and r.get("digest") == digest for r in refs):
                raise ProviderReturnAdmissionError("PROVIDER_RETURN_VIEW_NOT_ON_RECEIPT", digest)
        return True
    return False


def _span_key_fact(anchor: dict) -> tuple:
    return (
        anchor.get("path"),
        anchor.get("blobDigest"),
        anchor.get("startByte"),
        anchor.get("endByte"),
    )


def _span_key_candidate(anchor: dict) -> tuple:
    digest = anchor.get("contentSha256")
    if digest is None:
        digest = anchor.get("blobDigest")
    return (
        anchor.get("path"),
        digest,
        anchor.get("startByte"),
        anchor.get("endByte"),
    )


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
    fact_anchors = [_span_key_fact(a) for a in (fact.get("anchors") or [])]
    cand_anchors = [_span_key_candidate(a) for a in (cand.get("anchors") or [])]
    if any(k[0] is None or k[1] is None or k[2] is None or k[3] is None for k in fact_anchors + cand_anchors):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISJOIN", "anchor-fields")
    if sorted(fact_anchors) != sorted(cand_anchors):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISJOIN", "anchors")


def _candidate_stream(batch: dict, dispatch: dict) -> dict:
    candidates = {}
    ords = []
    for cand in batch["candidates"]:
        ordinal = cand["candidateOrdinal"]
        if ordinal in candidates:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_DUPLICATE_CANDIDATE", str(ordinal))
        candidates[ordinal] = cand
        ords.append(ordinal)
    if ords != sorted(ords) or len(ords) != len(set(ords)):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_CANDIDATE_STREAM", "unique-increasing")
    if ords and ords[0] != dispatch["expectedFirstCandidateOrdinal"]:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_CANDIDATE_STREAM", "expectedFirstCandidateOrdinal")
    first = dispatch["expectedFirstCandidateOrdinal"]
    if ords != list(range(first, first + len(ords))):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_CANDIDATE_STREAM", "contiguous candidate stream")
    return candidates


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


def _token_gate(batch, negotiated_tokens: list):
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
    return None


def _buffer_body(batch, dispatch: dict) -> dict:
    try:
        validate_schema(BATCH_SCHEMA, batch)
    except Exception as exc:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", str(exc)) from exc
    _correlate_batch(batch, dispatch)
    candidates = _candidate_stream(batch, dispatch)
    companions = []
    for companion in batch["occupancyCompanions"]:
        try:
            validate_schema(COMPANION_SCHEMA, companion)
        except Exception as exc:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", str(exc)) from exc
        ordinal = companion["candidateOrdinal"]
        cand = candidates.get(ordinal)
        if cand is None:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_UNKNOWN_CANDIDATE", str(ordinal))
        if companion.get("targetUniverseId") != cand.get("targetUniverseId"):
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_UNIVERSE_MISMATCH", str(ordinal))
        decoded = verify_candidate_cbor(cand)
        spec_rel = AM.REGISTRY["relations"].get(cand.get("relation")) or {}
        field = spec_rel.get("targetNativeIdField")
        if not field or decoded.get(field) != companion.get("targetNativeId"):
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH", str(ordinal))
        companions.append((ordinal, companion, cand, decoded))
    return {"candidates": candidates, "companions": companions}


def buffer_fact_batch_occupancy(
    batch,
    *,
    negotiated_tokens: list,
    dispatch,
):
    """ANALYZING entry. Dispatch is required. Receipts and views MUST NOT be required.

    A receipt/view not yet constructed cannot be an admission precondition.
    Does not project TargetAttributionV2 and does not capture hostDerivedRefs.
    """
    omitted = _token_gate(batch, negotiated_tokens)
    if omitted is not None:
        omitted["phase"] = "buffer"
        return omitted
    dispatch = _require_dispatch(dispatch)
    body = _buffer_body(batch, dispatch)
    return {
        "status": "buffered",
        "records": [],
        "hostDerivedRefs": [],
        "blobs": {},
        "delivery": "fact-batch-v3-companion",
        "phase": "buffer",
        "producerClosure": dispatch["producerClosure"],
        "stageId": batch["stageId"],
        "retainedStageOrdinal": dispatch["retainedStageOrdinal"],
        "analyzeRequestOrdinal": dispatch["analyzeRequestOrdinal"],
        "bufferedCompanionCount": len(body["companions"]),
    }


def capture_occupancy(
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
    dispatch=None,
    stage_receipts=None,
    prior_records: list | None = None,
):
    """Post-terminal capture. Dispatch AND receipts/views are required.

    Timing: Coverage/Complete → native view → stageReceipt → this entry.
    Current-batch facts+records admit first. Combined occupancy-conflict then
    runs on prior_records + new records without requiring prior facts in the
    current mint map (AM._admit_provider_occupancy_conflicts does not use facts).
    """
    omitted = _token_gate(batch, negotiated_tokens)
    if omitted is not None:
        omitted["phase"] = "capture"
        return omitted
    dispatch = _require_dispatch(dispatch)
    if dispatch.get("planId") != plan_id:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PLAN_MISMATCH", "dispatch.planId")
    body = _buffer_body(batch, dispatch)
    row, spec = _stage_from_dispatch(execution_plan, stage_specs, dispatch, plan_id)
    producer_closure = spec["producerClosure"]
    _require_selected_provider(closures, producer_closure)
    receipt = _require_receipt(stage_receipts, row, spec)
    if views is None:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_FACT_NOT_IN_VIEW", "views-required")
    records = []
    for ordinal, companion, cand, decoded in body["companions"]:
        fact = minted_by_ordinal.get(ordinal)
        if fact is None:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISSING", str(ordinal))
        if fact.get("producerClosure") != producer_closure:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_PRODUCER_MISMATCH", fact.get("factId"))
        _mint_correspondence(fact, cand, decoded)
        spec_rel = AM.REGISTRY["relations"].get(fact.get("relation")) or {}
        field = spec_rel.get("targetNativeIdField")
        if (fact.get("payload") or {}).get(field) != companion.get("targetNativeId"):
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH", "fact-payload")
        if not _fact_in_producer_view(views, fact["factId"], producer_closure, plan_id, receipt):
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_FACT_NOT_IN_VIEW", fact["factId"])
        records.append(project_companion_to_v2(companion, fact, plan_id, producer_closure))
    records = sorted(records, key=lambda r: r["sourceFactId"].encode("utf-8"))
    current_facts = {minted_by_ordinal[o]["factId"]: minted_by_ordinal[o] for o in minted_by_ordinal}
    current_map = {}
    for rec in records:
        fid = rec.get("sourceFactId")
        if fid in current_map:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_DUPLICATE_FACT", fid)
        current_map[fid] = rec
        try:
            validate_schema(TARGET_SCHEMA, rec)
        except Exception as exc:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_SCHEMA", str(exc)) from exc
    atom_inputs = {
        "planId": plan_id,
        "facts": current_facts,
        "inventories": inventories,
        "enumerationPlan": enumeration_plan,
        "closures": closures,
        "targetAttributions": current_map,
    }
    try:
        AM._admit_target_attributions(atom_inputs)
    except AM.AtomAdmissionError as exc:
        raise ProviderReturnAdmissionError(exc.key, exc.detail) from exc
    combined = {}
    for rec in list(prior_records or []) + records:
        fid = rec.get("sourceFactId")
        if fid in combined:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_DUPLICATE_FACT", fid)
        combined[fid] = rec
        try:
            validate_schema(TARGET_SCHEMA, rec)
        except Exception as exc:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_SCHEMA", str(exc)) from exc
    try:
        AM._admit_provider_occupancy_conflicts(combined, {})
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
        "phase": "capture",
        "producerClosure": producer_closure,
        "stageId": batch["stageId"],
        "retainedStageOrdinal": dispatch["retainedStageOrdinal"],
        "analyzeRequestOrdinal": dispatch["analyzeRequestOrdinal"],
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
    dispatch=None,
    stage_receipts=None,
    prior_records: list | None = None,
    **_ignored,
):
    """Owning post-terminal host-adapter entry (combined bind).

    Trusted host observations (do not prove FACT-ID-V1): negotiated Hello tokens;
    DispatchBindingV1 derived at Analyze dispatch from the actual Plan stage;
    retained Plan locator; execution-plan (planId + stages with stageSpecDigest);
    retained stage-spec map keyed by that digest; hostCapture.stageReceipts
    (required here; not required at buffer); selected views with required planId
    whose digest appears on the matching receipt.outputRefs; mint map from THIS
    batch as a host TCB observation of already-admitted mint; inventories;
    enumeration plan; already-captured TargetAttributionV2 prior_records.

    Provider claims: FactCandidateV1 members and OccupancyCompanionV1 occupancy fields.

    Host-filled: planId, sourceFactId, producerClosure from stage-spec, targetUniverse
    from minted fact.

    EnumerationPlan enumerator is a separate XI cell/program binding. This entry
    does not require producerClosure == enumerator.closureId.

    Analyze request ordinal is not retained execution-plan ordinal. FactBatch.stageId
    is C-2 text, correlated to dispatch.expectedStageId.
    """
    return capture_occupancy(
        batch,
        negotiated_tokens=negotiated_tokens,
        plan_id=plan_id,
        execution_plan=execution_plan,
        stage_specs=stage_specs,
        closures=closures,
        views=views,
        minted_by_ordinal=minted_by_ordinal,
        inventories=inventories,
        enumeration_plan=enumeration_plan,
        dispatch=dispatch,
        stage_receipts=stage_receipts,
        prior_records=prior_records,
    )


def admit_provider_attribution_return(envelope, **kwargs):
    """COMPLETE58 helper is not the owning delivery."""
    origin = kwargs.pop("origin", None)
    if origin == "host-internal":
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_HOST_AUTHORED", "origin=host-internal")
    if envelope is not None and kwargs.get("batch") is None:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_UNBOUND_ENVELOPE", "no worker FactBatchV3")
    if envelope is not None:
        try:
            validate_schema(RETURN_SCHEMA, envelope)
        except Exception as exc:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", str(exc)) from exc
    if "negotiated_tokens" not in kwargs:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_OWNERS_REQUIRED", "negotiated_tokens")
    if "dispatch" not in kwargs:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_DISPATCH", "required")
    keys = (
        "negotiated_tokens", "plan_id", "execution_plan", "stage_specs",
        "closures", "views", "minted_by_ordinal", "inventories", "enumeration_plan",
        "stage_receipts", "dispatch", "prior_records",
    )
    return bind_worker_occupancy(kwargs.get("batch"), **{k: kwargs[k] for k in keys if k in kwargs})
