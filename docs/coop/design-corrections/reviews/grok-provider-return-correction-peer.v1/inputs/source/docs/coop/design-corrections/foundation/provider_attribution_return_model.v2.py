"""Host-adapter TargetAttributionV2 return. Design reference, not a host runtime.

Admit ProviderTargetAttributionReturnV2 after fact2 mint and before
attach_host_capture / close_run. Capture admitted records as domain=target-attribution
blobs. The envelope is not a Run preimage and not a protocol3 frame.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = _load("provider_return_canonical", HERE / "canonical.py")
AM = _load("provider_return_atom", HERE / "atom_model.v1.py")
FM = _load("provider_return_fault", HERE / "evaluator_fault_model.v3.py")

SCHEMA = json.loads((HERE / "provider-target-attribution-return.schema.v2.json").read_text(encoding="utf-8"))
FAULTS = SCHEMA["x-opensip-new-internal-faults"]
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


def admit_provider_attribution_return(
    envelope,
    *,
    plan_id: str,
    producer_closure: str,
    stage_ordinal: int,
    facts: dict,
    inventories: list,
    enumeration_plan: dict,
    closures: dict,
    prior_records: list | None = None,
    origin: str = "provider-return",
):
    """Admit wrapper return or lawful omission. Capture V2 records only.

    origin is recorded by the host TCB: provider-return for wrapper output,
    host-internal if the host constructed the mapping itself.
    """
    if origin not in ALLOWED_ORIGINS:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", "origin")
    if envelope is None:
        return {
            "status": "omitted",
            "records": [],
            "hostDerivedRefs": [],
            "blobs": {},
            "origin": origin,
        }
    try:
        C.validate(SCHEMA, envelope)
    except Exception as exc:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_SCHEMA", str(exc)) from exc
    if envelope.get("planId") != plan_id:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PLAN_MISMATCH", "planId")
    if envelope.get("producerClosure") != producer_closure:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PRODUCER_MISMATCH", "producerClosure")
    if (closures.get(producer_closure) or {}).get("kind") != "provider":
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_PRODUCER_NOT_PROVIDER", producer_closure)
    if envelope.get("stageOrdinal") != stage_ordinal:
        raise ProviderReturnAdmissionError("PROVIDER_RETURN_STAGE_ORDINAL", str(envelope.get("stageOrdinal")))
    records = list(envelope.get("records") or [])
    seen = set()
    for rec in records:
        fid = rec.get("sourceFactId")
        if fid in seen:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_DUPLICATE_FACT", fid)
        seen.add(fid)
        if rec.get("planId") != plan_id:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_PLAN_MISMATCH", rec.get("planId"))
        if rec.get("producerClosure") != producer_closure:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_PRODUCER_MISMATCH", rec.get("producerClosure"))
        fact = facts.get(fid)
        if fact is None:
            raise ProviderReturnAdmissionError("PROVIDER_RETURN_UNKNOWN_FACT", fid)
        if fact.get("producerClosure") != producer_closure:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_PRODUCER_MISMATCH", fid)
    prior = list(prior_records or [])
    combined = {}
    for rec in prior + records:
        fid = rec.get("sourceFactId")
        if fid in combined:
            raise ProviderReturnAdmissionError("TARGET_ATTRIBUTION_DUPLICATE_FACT", fid)
        combined[fid] = rec
    atom_inputs = {
        "planId": plan_id,
        "facts": facts,
        "inventories": inventories,
        "enumerationPlan": enumeration_plan,
        "closures": closures,
        "targetAttributions": {rec["sourceFactId"]: rec for rec in records},
    }
    try:
        AM._admit_target_attributions(atom_inputs)
        AM._admit_provider_occupancy_conflicts(combined, facts)
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
        "origin": origin,
    }
