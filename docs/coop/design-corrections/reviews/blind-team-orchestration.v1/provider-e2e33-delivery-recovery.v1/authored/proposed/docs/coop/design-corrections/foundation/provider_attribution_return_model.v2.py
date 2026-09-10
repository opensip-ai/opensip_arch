"""Worker occupancy companion → TargetAttributionV2 projection.

Owning host-adapter entry is bind_worker_occupancy. Design reference, not a
host runtime. Historical COMPLETE58 admit_provider_attribution_return that
accepted a caller-built V2 envelope plus origin= is not the delivery interface:
the compiler-native table cannot cross a closed FactBatch of already-encoded
opaque payloads, and origin is not a blessing on identical bytes.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NATIVE_HERE = HERE.parent / "native"
IMMUTABLE_FOUNDATION = Path(
    "/tmp/opensip-design-corrections/target-provider-return-successor.v1"
    "/docs/coop/design-corrections/foundation"
)
TOKEN = "target-attribution-v2"


def _pick(*paths: Path) -> Path:
    for path in paths:
        if path.is_file():
            return path
    raise FileNotFoundError(paths[0])


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = _load("occ_canonical", _pick(HERE / "canonical.py", IMMUTABLE_FOUNDATION / "canonical.py"))
AM = _load("occ_atom", _pick(HERE / "atom_model.v1.py", IMMUTABLE_FOUNDATION / "atom_model.v1.py"))
FM = _load("occ_fault", _pick(HERE / "evaluator_fault_model.v3.py", IMMUTABLE_FOUNDATION / "evaluator_fault_model.v3.py"))

BATCH_SCHEMA = json.loads(_pick(
    NATIVE_HERE / "fact-batch.schema.v3.json",
    HERE / "fact-batch.schema.v3.json",
).read_text(encoding="utf-8"))
COMPANION_SCHEMA = json.loads(_pick(
    NATIVE_HERE / "occupancy-companion.schema.v1.json",
    HERE / "occupancy-companion.schema.v1.json",
).read_text(encoding="utf-8"))
RETURN_SCHEMA = json.loads((HERE / "provider-target-attribution-return.schema.v2.json").read_text(encoding="utf-8"))
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


def decode_candidate_payload(candidate: dict) -> dict:
    raw = bytes.fromhex(candidate["canonicalRelationPayloadHex"])
    return json.loads(raw.decode("utf-8"))


def _stage_producer(execution_plan: dict, stage_specs: dict, stage_ordinal: int) -> str:
    stages = execution_plan.get("stages") or []
    row = next((s for s in stages if s.get("ordinal") == stage_ordinal), None)
    if row is None:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_NOT_IN_PLAN", str(stage_ordinal))
    spec = stage_specs.get(row.get("stageSpecDigest")) or {}
    pc = spec.get("producerClosure") or row.get("producerClosure")
    if not pc:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_PRODUCER", str(stage_ordinal))
    return pc


def _require_selected_provider(closures: dict, producer_closure: str) -> None:
    if (closures.get(producer_closure) or {}).get("kind") != "provider":
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PRODUCER_NOT_PROVIDER", producer_closure)


def _fact_in_producer_view(views: dict, fact_id: str, producer_closure: str, plan_id: str) -> bool:
    for view in (views or {}).values():
        if view.get("producerClosure") != producer_closure:
            continue
        if view.get("planId") not in (None, plan_id) and view.get("planId") != plan_id:
            continue
        if fact_id in (view.get("facts") or []):
            return True
    return False


def project_companion_to_v2(companion: dict, fact: dict, plan_id: str, producer_closure: str) -> dict:
    """Mechanical host projection. Host fills locators; occupancy fields copy from the worker companion."""
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
):
    """Owning host-adapter entry.

    Trusted host observations: negotiated Hello tokens, retained Plan locator,
    execution-plan + stage specs, closure kind map, selected views, mint map
    from THIS batch's candidates, inventories, enumeration plan.

    Provider claims: FactCandidateV1 members and OccupancyCompanionV1 occupancy
    fields. planId / sourceFactId / producerClosure are rederived, never taken
    from a caller envelope.
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
    producer_closure = _stage_producer(execution_plan, stage_specs, batch["stageOrdinal"])
    _require_selected_provider(closures, producer_closure)
    candidates = {c["candidateOrdinal"]: c for c in batch["candidates"]}
    if len(candidates) != len(batch["candidates"]):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_DUPLICATE_CANDIDATE", "candidateOrdinal")
    ords = [c["candidateOrdinal"] for c in batch["candidates"]]
    if ords != sorted(ords) or len(ords) != len(set(ords)):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_CANDIDATE_ORDINAL", "unique-order")
    if ords != list(range(ords[0], ords[0] + len(ords))):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_CANDIDATE_ORDINAL", "contiguous")
    comp_ords = [c["candidateOrdinal"] for c in batch["occupancyCompanions"]]
    if comp_ords != sorted(comp_ords) or len(comp_ords) != len(set(comp_ords)):
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_CANDIDATE_ORDINAL", "companion-order")
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
        fact = minted_by_ordinal.get(ordinal)
        if fact is None:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISSING", str(ordinal))
        if fact.get("producerClosure") != producer_closure:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_PRODUCER_MISMATCH", fact.get("factId"))
        if fact.get("relation") != cand.get("relation") or fact.get("resolution") != cand.get("resolution"):
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISJOIN", str(ordinal))
        spec = AM.REGISTRY["relations"].get(fact.get("relation")) or {}
        field = spec.get("targetNativeIdField")
        payload = decode_candidate_payload(cand)
        if not field or (fact.get("payload") or {}).get(field) != companion.get("targetNativeId"):
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH", str(ordinal))
        if payload.get(field) != companion.get("targetNativeId"):
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH", "payload")
        if (fact.get("payload") or {}).get(field) != payload.get(field):
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_MINT_MISJOIN", "payload")
        if not _fact_in_producer_view(views, fact["factId"], producer_closure, plan_id):
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_FACT_NOT_IN_VIEW", fact["factId"])
        records.append(project_companion_to_v2(companion, fact, plan_id, producer_closure))
    facts = {minted_by_ordinal[o]["factId"]: minted_by_ordinal[o] for o in minted_by_ordinal}
    atom_inputs = {
        "planId": plan_id,
        "facts": facts,
        "inventories": inventories,
        "enumerationPlan": enumeration_plan,
        "closures": closures,
        "targetAttributions": {r["sourceFactId"]: r for r in records},
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
        "stageOrdinal": batch["stageOrdinal"],
    }


def admit_provider_attribution_return(envelope, **kwargs):
    """COMPLETE58 helper is not the owning delivery.

    A caller-built TargetAttributionV2 envelope is not worker output. origin is
    not a parameter that blesses identical bytes. Host-authored mapping refuses
    and captures nothing. Unbound provider-return envelopes refuse.
    """
    origin = kwargs.pop("origin", None)
    if origin == "host-internal":
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_HOST_AUTHORED", "origin=host-internal")
    if envelope is not None and kwargs.get("batch") is None:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_UNBOUND_ENVELOPE", "no worker FactBatchV3")
    if "negotiated_tokens" not in kwargs:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_OWNERS_REQUIRED", "negotiated_tokens")
    return bind_worker_occupancy(kwargs.get("batch"), **{
        k: kwargs[k] for k in (
            "negotiated_tokens", "plan_id", "execution_plan", "stage_specs",
            "closures", "views", "minted_by_ordinal", "inventories", "enumeration_plan",
        )
    })
