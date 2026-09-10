"""End-to-end occupancy companion controls. Schema/atom/wire-bind. Not full Run replay."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = _load("provider_return_model_v2", HERE / "provider_attribution_return_model.v2.py")
AM = M.AM
C = M.C

U1 = "11" * 32
C_PROV = "closure2:" + "aa" * 32
C_PROV2 = "closure2:" + "ee" * 32
C_EVAL = "closure2:" + "bb" * 32
C_ENUM = "closure2:" + "99" * 32
PLAN = "plan2:" + "cc" * 32
SNAP = "snapshot2:" + "aa" * 32
VIEW = "view2:" + "ee" * 32
TOKEN = "target-attribution-v2"
TS_TOKENS = [
    "source-identity-snapshot2", "plan-identity-plan2", "fact-identity-fact2", "coverage-v3",
    "sealed-vfs-v1", "multi-stage-analyze-v1", "typescript-semantic-facts-v1",
    "resolution-completeness-v2", "unresolved-edge-v1", "native-context-v2", TOKEN,
]
STAGE_FIELDS = (
    "schemaVersion", "planId", "producerClosure", "operation", "parameters",
    "outputDomains", "outputSchemaDigest",
)


def H(ch: str) -> str:
    return ch * 64


def fact2(ch: str) -> str:
    return "fact2:" + H(ch)


def fail(msg: str) -> None:
    raise AssertionError(msg)


def inv_file(path="src/a.ts"):
    return {
        "schemaVersion": 1, "planId": PLAN, "parameterDigest": H("0"),
        "cellOrdinal": 0, "programOrdinal": 0, "kind": "file", "state": "complete",
        "deficiency": None, "nativeCause": None, "examinedPaths": [path],
        "rows": [{
            "nativeSubjectId": path, "kind": "file", "path": path, "qualifiedName": path,
            "subjectLanguage": "typescript", "signatureTokens": [], "projections": [],
        }],
        "universe": U1,
    }


def inv_symbol(nid="ts-symbol:src/a.ts#f", path="src/a.ts"):
    return {
        "schemaVersion": 1, "planId": PLAN, "parameterDigest": H("0"),
        "cellOrdinal": 0, "programOrdinal": 0, "kind": "symbol", "state": "complete",
        "deficiency": None, "nativeCause": None, "examinedPaths": [path],
        "rows": [{
            "nativeSubjectId": nid, "kind": "symbol", "path": path, "qualifiedName": "f",
            "subjectLanguage": "typescript", "exported": "exported",
            "signatureTokens": ["f"], "projections": [],
        }],
        "universe": U1,
    }


def plan_one(enumerator=C_PROV, kinds=None):
    kinds = kinds or ["symbol", "file"]
    return {
        "schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": H("0"), "membershipDigest": H("0"),
        "cells": [{
            "capabilityId": "imports", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
            "required": True, "kinds": kinds,
            "programBindings": [{
                "ordinal": 0, "provenance": "default-unit",
                "enumerator": {"status": "selected", "closureId": enumerator},
                "nativeContextDigest": H("0"), "universe": U1, "programEntry": None,
                "extents": [{"kind": k, "paths": ["src/a.ts"]} for k in kinds],
            }],
        }],
    }


def imports_payload(resolved="file:src/a.ts"):
    return {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a", "resolvedTarget": resolved}


def imports_fact(fid, resolved="file:src/a.ts"):
    payload = imports_payload(resolved)
    return {
        "factId": fid, "relation": "imports", "resolution": "resolved-target",
        "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
        "confidenceMillionths": 1000000,
        "payload": payload,
        "anchors": [{"kind": "source-span", "path": "src/a.ts"}],
    }


def candidate(ordinal, resolved="file:src/a.ts"):
    payload = imports_payload(resolved)
    cbor_hex = M.deterministic_cbor(payload).hex()
    return {
        "candidateOrdinal": ordinal,
        "relation": "imports",
        "resolution": "resolved-target",
        "layer": "semantic",
        "producer": "typescript-semantic",
        "producerVersion": "test",
        "schemaVersion": 1,
        "language": "typescript",
        "sourceUniverseId": "sha256:" + U1,
        "targetUniverseId": "sha256:" + U1,
        "confidenceMillionths": 1000000,
        "relationSchemaId": "opensip.imports-payload.v1",
        "canonicalRelationPayloadHex": cbor_hex,
        "decodedRelationPayload": payload,
        "anchors": [{"kind": "source-span", "path": "src/a.ts"}],
    }


def companion(ordinal, resolved="file:src/a.ts", kind="file", occupancy="first-party",
              evaluation="src/a.ts", exported=None, logical=None, manifest=None):
    if occupancy != "first-party":
        evaluation = None
    return {
        "schemaVersion": 1,
        "candidateOrdinal": ordinal,
        "targetUniverseId": "sha256:" + U1,
        "targetNativeId": resolved,
        "kind": kind, "occupancy": occupancy, "exported": exported,
        "logicalPath": logical, "packageManifestPath": manifest,
        "evaluationNativeId": evaluation,
    }


def batch(cands, comps, stage_id=0):
    return {
        "schemaVersion": 3,
        "analysisOrdinal": 0,
        "stageId": stage_id,
        "batchIndex": 0,
        "candidates": list(cands),
        "occupancyCompanions": list(comps),
    }


def stage_spec():
    spec = {
        "schemaVersion": 2, "planId": PLAN, "producerClosure": C_PROV,
        "operation": "analyze", "parameters": [], "outputDomains": ["view"],
        "outputSchemaDigest": H("1"),
    }
    digest = M.raw_digest({k: spec[k] for k in STAGE_FIELDS})
    return digest, spec


def owners(fid, resolved="file:src/a.ts", inventories=None, enumerator=C_ENUM):
    digest, spec = stage_spec()
    fact = imports_fact(fid, resolved)
    return dict(
        negotiated_tokens=list(TS_TOKENS),
        plan_id=PLAN,
        execution_plan={
            "schemaVersion": 2, "planId": PLAN,
            "stages": [{"ordinal": 0, "stageSpecDigest": digest, "requires": [], "outputDomains": ["view"]}],
        },
        stage_specs={digest: spec},
        closures={
            C_PROV: {"kind": "provider"}, C_PROV2: {"kind": "provider"},
            C_EVAL: {"kind": "evaluator"}, C_ENUM: {"kind": "provider"},
        },
        views={VIEW: {"planId": PLAN, "producerClosure": C_PROV, "facts": [fid]}},
        minted_by_ordinal={0: fact},
        inventories=inventories or [inv_file(), inv_file("src/b.ts"), inv_symbol()],
        enumeration_plan=plan_one(enumerator=enumerator),
        stage_receipts=[{
            "ordinal": 0, "stageSpecDigest": digest, "producerClosure": C_PROV,
            "outputDomains": ["view"], "outputRefs": [], "state": "complete", "unavailableReason": None,
        }],
        analyze_analysis_ordinal=0,
        prior_records=[],
    )


def expect_key(fn, key, label):
    try:
        fn()
    except M.ProviderReturnAdmissionError as exc:
        if exc.key != key:
            fail(f"{label}: key {exc.key!r} != {key!r}")
        return exc
    fail(f"{label}: expected {key}")


def test_pipeline_positive_file_first_party():
    fid = fact2("1")
    out = M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **owners(fid))
    if out["status"] != "admitted" or out["delivery"] != "fact-batch-v3-companion":
        fail("pipeline status")
    if out["records"][0]["sourceFactId"] != fid or out["records"][0]["producerClosure"] != C_PROV:
        fail("host-filled locators")
    if out["stageId"] != 0:
        fail("stageId echo")
    digest = out["hostDerivedRefs"][0]["digest"]
    if hashlib.sha256(out["blobs"][digest]).hexdigest() != digest:
        fail("capture digest")


def test_cbor_hex_is_not_canonical_json_utf8():
    payload = imports_payload()
    json_hex = C.canonical(payload).hex()
    cbor_hex = M.deterministic_cbor(payload).hex()
    if json_hex == cbor_hex:
        fail("fixture must distinguish CBOR from JSON UTF-8")
    fid = fact2("1")
    cand = candidate(0)
    cand["canonicalRelationPayloadHex"] = json_hex

    def go():
        M.bind_worker_occupancy(batch([cand], [companion(0)]), **owners(fid))
    expect_key(go, "PROVIDER_RETURN_PAYLOAD_CBOR", "json-utf8-hex")


def test_enumerator_need_not_equal_fact_producer():
    fid = fact2("1")
    args = owners(fid, enumerator=C_ENUM)
    if args["enumeration_plan"]["cells"][0]["programBindings"][0]["enumerator"]["closureId"] == C_PROV:
        fail("enumerator fixture")
    out = M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    if out["producerClosure"] != C_PROV:
        fail("stage-spec producer")


def test_unnegotiated_omits():
    fid = fact2("1")
    args = owners(fid)
    args["negotiated_tokens"] = [t for t in TS_TOKENS if t != TOKEN]
    out = M.bind_worker_occupancy(None, **args)
    if out["status"] != "omitted" or out["hostDerivedRefs"]:
        fail("unnegotiated omit")


def test_unnegotiated_v3_refuses():
    fid = fact2("1")
    args = owners(fid)
    args["negotiated_tokens"] = [t for t in TS_TOKENS if t != TOKEN]

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_UNNEGOTIATED_V3", "v3-without-token")


def test_missing_companions_lawful_empty():
    fid = fact2("1")
    out = M.bind_worker_occupancy(batch([candidate(0)], []), **owners(fid))
    if out["status"] != "admitted" or out["records"] or out["hostDerivedRefs"]:
        fail("empty companions")


def test_unknown_candidate_ordinal_refuses():
    fid = fact2("1")

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(9)]), **owners(fid))
    expect_key(go, "PROVIDER_RETURN_UNKNOWN_CANDIDATE", "extra-ordinal")


def test_payload_native_id_mismatch_refuses():
    fid = fact2("1")
    bad = companion(0, resolved="file:src/other.ts", evaluation="src/a.ts")

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [bad]), **owners(fid))
    expect_key(go, "TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH", "payload-join")


def test_fact_not_in_view_refuses():
    fid = fact2("1")
    args = owners(fid)
    args["views"] = {VIEW: {"planId": PLAN, "producerClosure": C_PROV, "facts": []}}

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_FACT_NOT_IN_VIEW", "view-membership")


def test_view_plan_id_required():
    fid = fact2("1")
    args = owners(fid)
    args["views"] = {VIEW: {"producerClosure": C_PROV, "facts": [fid]}}

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_FACT_NOT_IN_VIEW", "missing-view-planId")


def test_stage_not_in_execution_plan_refuses():
    fid = fact2("1")

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)], stage_id=7), **owners(fid))
    expect_key(go, "PROVIDER_RETURN_STAGE_NOT_IN_PLAN", "stage-owner")


def test_row_producer_closure_is_not_authority():
    fid = fact2("1")
    args = owners(fid)
    args["execution_plan"]["stages"][0]["producerClosure"] = C_PROV2
    out = M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    if out["producerClosure"] != C_PROV:
        fail("stage-spec producer wins; row has no producerClosure field in the closed schema")


def test_stage_spec_digest_mismatch_refuses():
    fid = fact2("1")
    args = owners(fid)
    args["execution_plan"]["stages"][0]["stageSpecDigest"] = "ab" * 32

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_STAGE_SPEC", "digest")


def test_receipt_mismatch_refuses():
    fid = fact2("1")
    args = owners(fid)
    args["stage_receipts"][0]["producerClosure"] = C_PROV2

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_RECEIPT", "receipt")


def test_evaluator_closure_refuses():
    fid = fact2("1")
    args = owners(fid)
    spec = dict(next(iter(args["stage_specs"].values())))
    spec["producerClosure"] = C_EVAL
    digest = M.raw_digest({k: spec[k] for k in STAGE_FIELDS})
    args["stage_specs"] = {digest: spec}
    args["execution_plan"]["stages"][0]["stageSpecDigest"] = digest
    args["stage_receipts"][0]["stageSpecDigest"] = digest
    args["stage_receipts"][0]["producerClosure"] = C_EVAL

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_PRODUCER_NOT_PROVIDER", "kind")


def test_c15_conflict_from_worker_companion():
    fid = fact2("1")
    args = owners(fid, resolved="file:src/a.ts",
                  inventories=[inv_file("file:src/a.ts"), inv_file("src/b.ts"), inv_symbol()])
    args["minted_by_ordinal"] = {0: imports_fact(fid, "file:src/a.ts")}
    rec = companion(0, resolved="file:src/a.ts", evaluation="src/b.ts")

    def go():
        M.bind_worker_occupancy(batch([candidate(0, "file:src/a.ts")], [rec]), **args)
    expect_key(go, "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT", "c15")


def test_prior_records_occupancy_conflict():
    fid1, fid2 = fact2("1"), fact2("2")
    prior = {
        "schemaVersion": 2, "planId": PLAN, "sourceFactId": fid2, "producerClosure": C_PROV,
        "targetUniverse": U1, "targetNativeId": "file:src/a.ts", "kind": "file",
        "occupancy": "first-party", "exported": None, "logicalPath": None,
        "packageManifestPath": None, "evaluationNativeId": "src/b.ts",
    }
    args = owners(fid1, inventories=[inv_file(), inv_file("src/b.ts"), inv_symbol()])
    args["prior_records"] = [prior]
    args["views"][VIEW]["facts"] = [fid1, fid2]
    args["minted_by_ordinal"] = {
        0: imports_fact(fid1),
        1: imports_fact(fid2),
    }

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "TARGET_ATTRIBUTION_PROVIDER_OCCUPANCY_CONFLICT", "prior")


def test_malformed_companion_schema():
    fid = fact2("1")
    rec = companion(0)
    rec["evaluationNativeId"] = None

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [rec]), **owners(fid))
    expect_key(go, "PROVIDER_RETURN_SCHEMA", "malformed-companion")


def test_origin_host_internal_does_not_capture():
    fid = fact2("1")
    rec = {
        "schemaVersion": 2, "planId": PLAN, "sourceFactId": fid, "producerClosure": C_PROV,
        "targetUniverse": U1, "targetNativeId": "file:src/a.ts", "kind": "file",
        "occupancy": "first-party", "exported": None, "logicalPath": None,
        "packageManifestPath": None, "evaluationNativeId": "src/a.ts",
    }
    env = {"schemaVersion": 2, "planId": PLAN, "producerClosure": C_PROV, "stageOrdinal": 0, "records": [rec]}

    def go():
        M.admit_provider_attribution_return(env, origin="host-internal")
    expect_key(go, "PROVIDER_RETURN_HOST_AUTHORED", "host-internal")


def test_origin_provider_return_unbound_envelope_refuses():
    fid = fact2("1")
    rec = {
        "schemaVersion": 2, "planId": PLAN, "sourceFactId": fid, "producerClosure": C_PROV,
        "targetUniverse": U1, "targetNativeId": "file:src/a.ts", "kind": "file",
        "occupancy": "first-party", "exported": None, "logicalPath": None,
        "packageManifestPath": None, "evaluationNativeId": "src/a.ts",
    }
    env = {"schemaVersion": 2, "planId": PLAN, "producerClosure": C_PROV, "stageOrdinal": 0, "records": [rec]}

    def go():
        M.admit_provider_attribution_return(env, origin="provider-return")
    expect_key(go, "PROVIDER_RETURN_UNBOUND_ENVELOPE", "unbound")


def test_origin_probe_digests_not_captured():
    fid = fact2("1")
    rec = {
        "schemaVersion": 2, "planId": PLAN, "sourceFactId": fid, "producerClosure": C_PROV,
        "targetUniverse": U1, "targetNativeId": "file:src/a.ts", "kind": "file",
        "occupancy": "first-party", "exported": None, "logicalPath": None,
        "packageManifestPath": None, "evaluationNativeId": "src/a.ts",
    }
    env = {"schemaVersion": 2, "planId": PLAN, "producerClosure": C_PROV, "stageOrdinal": 0, "records": [rec]}
    captured = []
    for origin in ("provider-return", "host-internal"):
        try:
            out = M.admit_provider_attribution_return(env, origin=origin)
            captured.append(out.get("hostDerivedRefs"))
        except M.ProviderReturnAdmissionError:
            captured.append("REFUSE")
    if captured != ["REFUSE", "REFUSE"]:
        fail("origin probe must refuse both; got " + repr(captured))


def test_public_route_host_authored():
    raw = b"PROVIDER_RETURN_HOST_AUTHORED owner-diagnostic"
    routed = M.route_internal_key("PROVIDER_RETURN_HOST_AUTHORED", "host-internal", raw, "retained:fixture")
    if routed["termination"]["domainDetail"]["code"] != "HOST.INVARIANT_VIOLATED":
        fail("host authored detail")


def test_internal_keys_are_not_domain_detail_codes():
    common = json.loads(
        (HERE.parent / "workflows" / "schemas" / "evaluator3" / "common.schema.json").read_text()
    )
    codes = set(common["$defs"]["DomainDetailCode"]["enum"])
    for key in list(M.SCHEMA_KEYS) + list(M.JOIN_KEYS):
        if key in codes:
            fail("internal key leaked as DomainDetailCode: " + key)


def test_live_d9_not_discharged():
    if M.ROUTE_LAW["liveD9"] != "not discharged":
        fail("live D9 standing")


def test_partial_companion_omit_other_candidate():
    fid1, fid2 = fact2("1"), fact2("2")
    args = owners(fid1)
    args["views"][VIEW]["facts"] = [fid1, fid2]
    args["minted_by_ordinal"] = {0: imports_fact(fid1), 1: imports_fact(fid2, "file:src/b.ts")}
    cands = [candidate(0), candidate(1, "file:src/b.ts")]
    out = M.bind_worker_occupancy(batch(cands, [companion(0)]), **args)
    if len(out["records"]) != 1 or out["records"][0]["sourceFactId"] != fid1:
        fail("partial companion")


def test_refused_batch_captures_nothing():
    fid = fact2("1")
    try:
        M.bind_worker_occupancy(batch([candidate(0)], [companion(9)]), **owners(fid))
    except M.ProviderReturnAdmissionError:
        return
    fail("must refuse")


def test_mint_payload_mismatch_refuses():
    fid = fact2("1")
    args = owners(fid)
    args["minted_by_ordinal"][0] = imports_fact(fid, "file:src/b.ts")

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_MINT_MISJOIN", "payload")


CASES = [
    test_pipeline_positive_file_first_party,
    test_cbor_hex_is_not_canonical_json_utf8,
    test_enumerator_need_not_equal_fact_producer,
    test_unnegotiated_omits,
    test_unnegotiated_v3_refuses,
    test_missing_companions_lawful_empty,
    test_unknown_candidate_ordinal_refuses,
    test_payload_native_id_mismatch_refuses,
    test_fact_not_in_view_refuses,
    test_view_plan_id_required,
    test_stage_not_in_execution_plan_refuses,
    test_row_producer_closure_is_not_authority,
    test_stage_spec_digest_mismatch_refuses,
    test_receipt_mismatch_refuses,
    test_evaluator_closure_refuses,
    test_c15_conflict_from_worker_companion,
    test_prior_records_occupancy_conflict,
    test_malformed_companion_schema,
    test_origin_host_internal_does_not_capture,
    test_origin_provider_return_unbound_envelope_refuses,
    test_origin_probe_digests_not_captured,
    test_public_route_host_authored,
    test_internal_keys_are_not_domain_detail_codes,
    test_live_d9_not_discharged,
    test_partial_companion_omit_other_candidate,
    test_refused_batch_captures_nothing,
    test_mint_payload_mismatch_refuses,
]


def main() -> int:
    results = []
    for fn in CASES:
        try:
            fn()
            results.append({"case": fn.__name__, "ok": True})
        except Exception as exc:  # noqa: BLE001
            results.append({"case": fn.__name__, "ok": False, "error": f"{type(exc).__name__}: {exc}"})
    ok = all(r["ok"] for r in results)
    report = {
        "standing": "FactBatchV3 CBOR companion → host projection against execution-plan stage-spec; not full Run; LIVE D9 not discharged",
        "ok": ok,
        "passed": sum(1 for r in results if r["ok"]),
        "failed": sum(1 for r in results if not r["ok"]),
        "fullRun": False,
        "results": results,
    }
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
