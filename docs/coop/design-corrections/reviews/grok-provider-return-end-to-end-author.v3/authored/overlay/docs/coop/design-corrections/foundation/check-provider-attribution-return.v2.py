"""End-to-end occupancy companion controls. Schema/atom/wire-bind. Not full Run replay.

Helper-minted facts in most cases are TCB assumptions for join comparison.
test_owner_admitted_semantic_fixture_positive derives one Plan/stage/spec/receipt/view/fact
from evaluator_semantic_fixture + M3 close APIs. That helper still does not prove
compiler TCB authenticity or FACT-ID-V1.
"""
from __future__ import annotations

import copy
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
VIEW2 = "view2:" + "dd" * 32
TOKEN = "target-attribution-v2"
STAGE_ID = "s-imports"
STAGE_ID_B = "s-syntax"
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


def inv_package(name="dup", path="packages/left/package.json"):
    return {
        "schemaVersion": 1, "planId": PLAN, "parameterDigest": H("0"),
        "cellOrdinal": 0, "programOrdinal": 0, "kind": "package", "state": "complete",
        "deficiency": None, "nativeCause": None, "examinedPaths": [path],
        "rows": [{
            "nativeSubjectId": name, "kind": "package", "path": path, "qualifiedName": name,
            "subjectLanguage": "json", "signatureTokens": [], "projections": [],
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


def fact_anchor(path="src/a.ts"):
    return {"path": path, "blobDigest": H("a"), "startByte": 0, "endByte": 12}


def cand_anchor(path="src/a.ts"):
    return {
        "kind": "source-span", "path": path, "contentSha256": H("a"),
        "startByte": 0, "endByte": 12,
    }


def imports_fact(fid, resolved="file:src/a.ts", path="src/a.ts"):
    payload = imports_payload(resolved)
    return {
        "factId": fid, "relation": "imports", "resolution": "resolved-target",
        "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
        "confidenceMillionths": 1000000,
        "payload": payload,
        "anchors": [fact_anchor(path)],
    }


def candidate(ordinal, resolved="file:src/a.ts", path="src/a.ts"):
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
        "anchors": [cand_anchor(path)],
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


def batch(cands, comps, stage_id=STAGE_ID, analysis=0, batch_index=0):
    return {
        "schemaVersion": 3,
        "analysisOrdinal": analysis,
        "stageId": stage_id,
        "batchIndex": batch_index,
        "candidates": list(cands),
        "occupancyCompanions": list(comps),
    }


def stage_spec(producer=C_PROV):
    spec = {
        "schemaVersion": 2, "planId": PLAN, "producerClosure": producer,
        "operation": "analyze", "parameters": [], "outputDomains": ["view"],
        "outputSchemaDigest": H("1"),
    }
    digest = M.raw_digest({k: spec[k] for k in STAGE_FIELDS})
    return digest, spec


def dispatch_binding(digest, stage_id=STAGE_ID, retained=0, request_ordinal=0,
                     analysis=0, batch_index=0, first_cand=0, producer=C_PROV):
    return {
        "schemaVersion": 1,
        "planId": PLAN,
        "retainedStageOrdinal": retained,
        "analyzeRequestOrdinal": request_ordinal,
        "expectedStageId": stage_id,
        "expectedAnalysisOrdinal": analysis,
        "expectedBatchIndex": batch_index,
        "expectedFirstCandidateOrdinal": first_cand,
        "producerClosure": producer,
        "stageSpecDigest": digest,
    }


def owners(fid, resolved="file:src/a.ts", inventories=None, enumerator=C_ENUM,
           stage_id=STAGE_ID, retained=0, request_ordinal=0, view_id=VIEW):
    digest, spec = stage_spec()
    fact = imports_fact(fid, resolved)
    view_digest = view_id.split(":", 1)[1]
    return dict(
        negotiated_tokens=list(TS_TOKENS),
        plan_id=PLAN,
        execution_plan={
            "schemaVersion": 2, "planId": PLAN,
            "stages": [{"ordinal": retained, "stageSpecDigest": digest, "requires": [], "outputDomains": ["view"]}],
        },
        stage_specs={digest: spec},
        closures={
            C_PROV: {"kind": "provider"}, C_PROV2: {"kind": "provider"},
            C_EVAL: {"kind": "evaluator"}, C_ENUM: {"kind": "provider"},
        },
        views={view_id: {"planId": PLAN, "producerClosure": C_PROV, "facts": [fid]}},
        minted_by_ordinal={0: fact},
        inventories=inventories or [inv_file(), inv_file("src/b.ts"), inv_symbol()],
        enumeration_plan=plan_one(enumerator=enumerator),
        stage_receipts=[{
            "ordinal": retained, "stageSpecDigest": digest, "producerClosure": C_PROV,
            "outputDomains": ["view"],
            "outputRefs": [{"domain": "view", "digest": view_digest}],
            "state": "complete", "unavailableReason": None,
        }],
        dispatch=dispatch_binding(digest, stage_id=stage_id, retained=retained,
                                  request_ordinal=request_ordinal),
        prior_records=[],
    )


def expect_key(fn, key, label):
    try:
        fn()
    except M.ProviderReturnAdmissionError as exc:
        if exc.key != key:
            fail(f"{label}: key {exc.key!r} != {key!r} detail={exc.detail!r}")
        return exc
    fail(f"{label}: expected {key}")


def test_pipeline_positive_file_first_party():
    fid = fact2("1")
    out = M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **owners(fid))
    if out["status"] != "admitted" or out["delivery"] != "fact-batch-v3-companion":
        fail("pipeline status")
    if out["records"][0]["sourceFactId"] != fid or out["records"][0]["producerClosure"] != C_PROV:
        fail("host-filled locators")
    if out["stageId"] != STAGE_ID:
        fail("stageId echo")
    if out["retainedStageOrdinal"] != 0 or out["analyzeRequestOrdinal"] != 0:
        fail("dispatch ordinals")
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


def test_receipt_omits_view_refuses():
    fid = fact2("1")
    args = owners(fid)
    args["stage_receipts"][0]["outputRefs"] = []

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_VIEW_NOT_ON_RECEIPT", "receipt-outputRefs")


def test_stage_not_in_execution_plan_refuses():
    fid = fact2("1")
    args = owners(fid)
    args["dispatch"] = dispatch_binding(
        args["dispatch"]["stageSpecDigest"], retained=7, stage_id=STAGE_ID,
    )

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_STAGE_NOT_IN_PLAN", "stage-owner")


def test_analyze_subset_does_not_equate_request_and_retained_ordinal():
    fid = fact2("1")
    digest, spec = stage_spec()
    digest0, spec0 = stage_spec(C_PROV2)
    spec0["outputSchemaDigest"] = H("2")
    digest0 = M.raw_digest({k: spec0[k] for k in STAGE_FIELDS})
    args = owners(fid, retained=5, request_ordinal=0)
    args["stage_specs"] = {digest: spec, digest0: spec0}
    args["execution_plan"]["stages"] = [
        {"ordinal": 0, "stageSpecDigest": digest0, "requires": [], "outputDomains": ["view"]},
        {"ordinal": 5, "stageSpecDigest": digest, "requires": [], "outputDomains": ["view"]},
    ]
    args["stage_receipts"] = [
        {
            "ordinal": 0, "stageSpecDigest": digest0, "producerClosure": C_PROV2,
            "outputDomains": ["view"], "outputRefs": [],
            "state": "complete", "unavailableReason": None,
        },
        {
            "ordinal": 5, "stageSpecDigest": digest, "producerClosure": C_PROV,
            "outputDomains": ["view"], "outputRefs": [{"domain": "view", "digest": VIEW.split(":", 1)[1]}],
            "state": "complete", "unavailableReason": None,
        },
    ]
    args["dispatch"] = dispatch_binding(
        digest, stage_id=STAGE_ID, retained=5, request_ordinal=0,
    )
    out = M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    if out["retainedStageOrdinal"] != 5 or out["analyzeRequestOrdinal"] != 0:
        fail("subset ordinals")
    if out["stageId"] != STAGE_ID:
        fail("text stageId preserved")


def test_integer_stage_id_refuses_schema():
    fid = fact2("1")

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)], stage_id=0), **owners(fid))
    expect_key(go, "PROVIDER_RETURN_SCHEMA", "integer-stageId")


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
    args["dispatch"] = dispatch_binding(digest, producer=C_EVAL)

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


def test_two_batch_two_stage_positive():
    fid1, fid2 = fact2("1"), fact2("2")
    d_a, spec_a = stage_spec()
    spec_b = dict(spec_a)
    spec_b["outputSchemaDigest"] = H("3")
    d_b = M.raw_digest({k: spec_b[k] for k in STAGE_FIELDS})
    args = owners(fid2, resolved="file:src/b.ts")
    args["stage_specs"] = {d_a: spec_a, d_b: spec_b}
    args["execution_plan"]["stages"] = [
        {"ordinal": 0, "stageSpecDigest": d_a, "requires": [], "outputDomains": ["view"]},
        {"ordinal": 5, "stageSpecDigest": d_b, "requires": [], "outputDomains": ["view"]},
    ]
    args["views"] = {
        VIEW: {"planId": PLAN, "producerClosure": C_PROV, "facts": [fid1]},
        VIEW2: {"planId": PLAN, "producerClosure": C_PROV, "facts": [fid2]},
    }
    args["stage_receipts"] = [
        {
            "ordinal": 0, "stageSpecDigest": d_a, "producerClosure": C_PROV,
            "outputDomains": ["view"], "outputRefs": [{"domain": "view", "digest": VIEW.split(":", 1)[1]}],
            "state": "complete", "unavailableReason": None,
        },
        {
            "ordinal": 5, "stageSpecDigest": d_b, "producerClosure": C_PROV,
            "outputDomains": ["view"], "outputRefs": [{"domain": "view", "digest": VIEW2.split(":", 1)[1]}],
            "state": "complete", "unavailableReason": None,
        },
    ]
    first = dict(args)
    first["dispatch"] = dispatch_binding(d_a, stage_id=STAGE_ID_B, retained=0, request_ordinal=0)
    first["minted_by_ordinal"] = {0: imports_fact(fid1, "file:src/a.ts")}
    first["prior_records"] = []
    out1 = M.bind_worker_occupancy(
        batch([candidate(0, "file:src/a.ts")], [companion(0, "file:src/a.ts")], stage_id=STAGE_ID_B),
        **first,
    )
    if out1["status"] != "admitted" or len(out1["records"]) != 1:
        fail("first batch")
    second = dict(args)
    second["dispatch"] = dispatch_binding(d_b, stage_id=STAGE_ID, retained=5, request_ordinal=1)
    second["minted_by_ordinal"] = {0: imports_fact(fid2, "file:src/b.ts", path="src/b.ts")}
    second["prior_records"] = list(out1["records"])
    out2 = M.bind_worker_occupancy(
        batch([candidate(0, "file:src/b.ts", path="src/b.ts")],
              [companion(0, "file:src/b.ts", evaluation="src/b.ts")]),
        **second,
    )
    if out2["status"] != "admitted" or out2["records"][0]["sourceFactId"] != fid2:
        fail("second batch current-only mint map")
    if out2["retainedStageOrdinal"] != 5 or out2["analyzeRequestOrdinal"] != 1:
        fail("second-stage dispatch")


def test_provider_conflict_prior_records_current_mint_map():
    fid1, fid2 = fact2("1"), fact2("2")
    prior = {
        "schemaVersion": 2, "planId": PLAN, "sourceFactId": fid2, "producerClosure": C_PROV,
        "targetUniverse": U1, "targetNativeId": "file:src/a.ts", "kind": "file",
        "occupancy": "first-party", "exported": None, "logicalPath": None,
        "packageManifestPath": None, "evaluationNativeId": "src/b.ts",
    }
    args = owners(fid1, inventories=[inv_file(), inv_file("src/b.ts"), inv_symbol()])
    args["prior_records"] = [prior]
    args["views"][VIEW]["facts"] = [fid1]
    args["minted_by_ordinal"] = {0: imports_fact(fid1)}

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "TARGET_ATTRIBUTION_PROVIDER_OCCUPANCY_CONFLICT", "prior-current-map")


def test_malformed_companion_schema():
    fid = fact2("1")
    rec = companion(0)
    rec["evaluationNativeId"] = None

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [rec]), **owners(fid))
    expect_key(go, "PROVIDER_RETURN_SCHEMA", "malformed-companion")


def test_package_first_party_companion():
    fid = fact2("1")
    resolved = "dup"
    path = "packages/left/package.json"
    args = owners(fid, resolved=resolved, inventories=[inv_file(), inv_package(), inv_symbol()])
    args["minted_by_ordinal"] = {0: imports_fact(fid, resolved)}
    rec = companion(0, resolved=resolved, kind="package", occupancy="first-party",
                    evaluation="dup", manifest=path)
    out = M.bind_worker_occupancy(batch([candidate(0, resolved)], [rec]), **args)
    if out["records"][0]["kind"] != "package" or out["records"][0]["packageManifestPath"] != path:
        fail("package companion")


def test_external_file_companion():
    fid = fact2("1")
    resolved = "file:node_modules/x.ts"
    args = owners(fid, resolved=resolved, inventories=[inv_file(), inv_file("src/b.ts"), inv_symbol()])
    args["minted_by_ordinal"] = {0: imports_fact(fid, resolved)}
    rec = companion(0, resolved=resolved, kind="file", occupancy="external")
    out = M.bind_worker_occupancy(batch([candidate(0, resolved)], [rec]), **args)
    if out["records"][0]["occupancy"] != "external" or out["records"][0]["evaluationNativeId"] is not None:
        fail("external companion")


def test_unknown_package_companion_null_paths():
    fid = fact2("1")
    resolved = "file:mystery"
    args = owners(fid, resolved=resolved, inventories=[inv_file(), inv_symbol()])
    args["minted_by_ordinal"] = {0: imports_fact(fid, resolved)}
    rec = companion(0, resolved=resolved, kind="package", occupancy="unknown")
    out = M.bind_worker_occupancy(batch([candidate(0, resolved)], [rec]), **args)
    if out["records"][0]["packageManifestPath"] is not None or out["records"][0]["evaluationNativeId"] is not None:
        fail("unknown package")


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
    args["minted_by_ordinal"] = {0: imports_fact(fid1), 1: imports_fact(fid2, "file:src/b.ts", path="src/b.ts")}
    cands = [candidate(0), candidate(1, "file:src/b.ts", path="src/b.ts")]
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


def test_different_anchor_same_length_refuses():
    fid = fact2("1")
    args = owners(fid)
    cand = candidate(0)
    cand["anchors"] = [cand_anchor("src/b.ts")]

    def go():
        M.bind_worker_occupancy(batch([cand], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_MINT_MISJOIN", "same-length-different-path")


def test_same_path_different_span_refuses():
    fid = fact2("1")
    args = owners(fid)
    cand = candidate(0)
    cand["anchors"] = [{
        "kind": "source-span", "path": "src/a.ts", "contentSha256": H("a"),
        "startByte": 1, "endByte": 13,
    }]

    def go():
        M.bind_worker_occupancy(batch([cand], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_MINT_MISJOIN", "same-path-different-span")


def test_omitted_dispatch_refuses():
    fid = fact2("1")
    args = owners(fid)
    args.pop("dispatch")

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_DISPATCH", "omit-dispatch")


def test_analysis_ordinal_not_in_dispatch_refuses():
    fid = fact2("1")
    args = owners(fid)

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)], analysis=77), **args)
    expect_key(go, "PROVIDER_RETURN_ANALYSIS_ORDINAL", "analysis-77")


def test_bind_without_receipts_refuses():
    fid = fact2("1")
    args = owners(fid)
    args["stage_receipts"] = None

    def go():
        M.bind_worker_occupancy(batch([candidate(0)], [companion(0)]), **args)
    expect_key(go, "PROVIDER_RETURN_RECEIPT", "capture-needs-receipt")


def test_buffer_does_not_require_receipts_or_views():
    fid = fact2("1")
    args = owners(fid)
    out = M.buffer_fact_batch_occupancy(
        batch([candidate(0)], [companion(0)]),
        negotiated_tokens=args["negotiated_tokens"],
        dispatch=args["dispatch"],
    )
    if out["status"] != "buffered" or out["hostDerivedRefs"] or out["phase"] != "buffer":
        fail("buffer without receipts")
    if out["bufferedCompanionCount"] != 1:
        fail("buffered count")


def test_schemas_are_not_mutated_at_import():
    batch_items = M.BATCH_SCHEMA["properties"]["occupancyCompanions"]["items"]
    if "$ref" not in batch_items or batch_items["$ref"] != "opensip.product.occupancy-companion.1":
        fail("batch items must $ref occupancy-companion; got " + repr(batch_items))
    rec_items = M.RETURN_SCHEMA["properties"]["records"]["items"]
    if "$ref" not in rec_items or rec_items["$ref"] != "opensip.product.target-attribution.2":
        fail("return records must $ref target-attribution")
    if "allOf" not in M.COMPANION_SCHEMA:
        fail("companion allOf must remain on the owner schema")
    if M.BATCH_SCHEMA["properties"]["stageId"].get("type") != "string":
        fail("stageId must remain text")


def test_owner_admitted_semantic_fixture_positive():
    """Derive one owner-admitted Plan/stage/spec/receipt/view/fact, transcribe a candidate,
    drive the binder, compare captured sidecar to the fixture sidecar.

    Preadmitted observations: fixture-minted fact2 (payloadDigest + required anchors),
    view, inventories, enumeration plan, execution-plan/stage-spec, hostCapture receipts
    after attach_host_capture, DispatchBindingV1 derived from that stage.
    Runtime verification: M3 open_run_closure + derive + replay + close_run on the same
    graph. The occupancy helper does not prove FACT-ID-V1 or compiler TCB authenticity.
    """
    S = _load("semantic_fixture_owner", HERE / "evaluator_semantic_fixture.v3.py")
    X = _load("execution_capture_owner", HERE / "execution_inputs_fixture.v3.py")
    R = _load("semantic_replay_owner", HERE / "evaluator_replay_model.v3.py")
    MM = R.M
    atom = {
        "op": "exists", "relation": "imports", "minResolution": "resolved-target",
        "endpoint": "target", "filters": [],
    }
    graph = S.build_ts_semantic_graph(
        atom=atom, subject_kind="file", has_declares=False,
        has_references_fact=False, second_partition=False,
    )
    attached = X.attach_host_capture(graph)
    manifest = attached["manifest"]
    objects, blobs = graph["objects"], graph["blobs"]
    close_error = None
    try:
        seed, objects, blobs, _ = S.seed_seal(graph)
        _, owner = MM.open_run_closure(seed, objects, blobs)
        i = graph["inputs"]
        result = R.derive(
            i["planId"], i["executionPlanId"], i["evaluatorClosure"],
            i["evaluationInputRefs"], objects, blobs, owner,
        )
        run, objects, blobs = S.seal_derived(graph, result, objects, blobs)
        actual = R.replay(run, objects, blobs)
        run_id = MM.close_run(run, objects, blobs)
        if run_id != actual["runId"]:
            raise AssertionError("close_run runId != replay runId")
        graph["_owner_close"] = {"runId": run_id, "verdict": actual.get("verdict")}
    except Exception as exc:  # noqa: BLE001
        close_error = f"{type(exc).__name__}: {exc}"
        objects, blobs = graph["objects"], graph["blobs"]

    imports_facts = [
        (k, v) for k, (dom, v) in objects.items()
        if dom == "fact" and v.get("relation") == "imports"
    ]
    if len(imports_facts) != 1:
        fail("expected one imports fact, got " + str(len(imports_facts)))
    fid, fact_rec = imports_facts[0]
    payload = C.parse(blobs[fact_rec["payloadDigest"]])
    anchors = list(fact_rec["anchors"])
    if not anchors or any(a.get("blobDigest") is None or a.get("startByte") is None for a in anchors):
        fail("owner fact anchors must include blobDigest/startByte/endByte")
    cand_anchors = [{
        "kind": "source-span",
        "path": a["path"],
        "contentSha256": a["blobDigest"],
        "startByte": a["startByte"],
        "endByte": a["endByte"],
    } for a in anchors]
    cbor_hex = M.deterministic_cbor(payload).hex()
    cand = {
        "candidateOrdinal": 0,
        "relation": fact_rec["relation"],
        "resolution": fact_rec["resolution"],
        "layer": "semantic",
        "producer": "typescript-semantic",
        "producerVersion": "fixture",
        "schemaVersion": 1,
        "language": "typescript",
        "sourceUniverseId": "sha256:" + fact_rec["sourceUniverse"],
        "targetUniverseId": "sha256:" + fact_rec["targetUniverse"],
        "confidenceMillionths": fact_rec["confidenceMillionths"],
        "relationSchemaId": "opensip.imports-payload.v1",
        "canonicalRelationPayloadHex": cbor_hex,
        "decodedRelationPayload": payload,
        "anchors": cand_anchors,
    }
    sidecar_refs = [
        r for r in graph["inputs"]["evaluationInputRefs"]
        if r.get("domain") == "target-attribution"
    ]
    if not sidecar_refs:
        sidecar_refs = [
            r for r in manifest.get("selectedRefs") or []
            if r.get("domain") == "target-attribution"
        ]
    if len(sidecar_refs) != 1:
        fail("expected one fixture sidecar ref, got " + str(sidecar_refs))
    fixture_sidecar = C.parse(blobs[sidecar_refs[0]["digest"]])
    occ = companion(
        0,
        resolved=payload["resolvedTarget"],
        kind=fixture_sidecar["kind"],
        occupancy=fixture_sidecar["occupancy"],
        evaluation=fixture_sidecar["evaluationNativeId"],
        exported=fixture_sidecar.get("exported"),
        logical=fixture_sidecar.get("logicalPath"),
        manifest=fixture_sidecar.get("packageManifestPath"),
    )
    occ["targetUniverseId"] = cand["targetUniverseId"]
    plan_id = graph["planId"]
    exec_id = graph["inputs"]["executionPlanId"]
    exec_plan = objects[exec_id][1]
    stage = exec_plan["stages"][0]
    spec = C.parse(blobs[stage["stageSpecDigest"]])
    views = {}
    for vid in graph["viewIds"]:
        views[vid] = objects[vid][1]
    inventories = [inv for _d, inv in graph["inventoryResults"]]
    receipts = list(manifest["hostCapture"]["stageReceipts"])
    dispatch = {
        "schemaVersion": 1,
        "planId": plan_id,
        "retainedStageOrdinal": stage["ordinal"],
        "analyzeRequestOrdinal": 0,
        "expectedStageId": "s-imports",
        "expectedAnalysisOrdinal": 0,
        "expectedBatchIndex": 0,
        "expectedFirstCandidateOrdinal": 0,
        "producerClosure": spec["producerClosure"],
        "stageSpecDigest": stage["stageSpecDigest"],
    }
    mint_fact = {
        "factId": fid,
        "relation": fact_rec["relation"],
        "resolution": fact_rec["resolution"],
        "sourceUniverse": fact_rec["sourceUniverse"],
        "targetUniverse": fact_rec["targetUniverse"],
        "producerClosure": fact_rec["producerClosure"],
        "confidenceMillionths": fact_rec["confidenceMillionths"],
        "payload": payload,
        "anchors": anchors,
    }
    closures = {k: v for k, (dom, v) in objects.items() if dom == "closure"}
    out = M.bind_worker_occupancy(
        batch([cand], [occ], stage_id="s-imports"),
        negotiated_tokens=list(TS_TOKENS),
        plan_id=plan_id,
        execution_plan=exec_plan,
        stage_specs={stage["stageSpecDigest"]: spec},
        closures=closures,
        views=views,
        minted_by_ordinal={0: mint_fact},
        inventories=inventories,
        enumeration_plan=graph["enumerationPlan"],
        dispatch=dispatch,
        stage_receipts=receipts,
        prior_records=[],
    )
    if out["status"] != "admitted" or len(out["records"]) != 1:
        fail("owner-positive bind")
    captured = out["records"][0]
    if M.raw_digest(captured) != sidecar_refs[0]["digest"]:
        fail("captured sidecar digest != fixture sidecar digest")
    if captured["sourceFactId"] != fid:
        fail("sourceFactId")
    # Discriminating malformed join through the same owner path.
    bad_receipts = copy.deepcopy(receipts)
    for rec in bad_receipts:
        rec["outputRefs"] = []

    def go_join():
        M.bind_worker_occupancy(
            batch([cand], [occ], stage_id="s-imports"),
            negotiated_tokens=list(TS_TOKENS),
            plan_id=plan_id,
            execution_plan=exec_plan,
            stage_specs={stage["stageSpecDigest"]: spec},
            closures=closures,
            views=views,
            minted_by_ordinal={0: mint_fact},
            inventories=inventories,
            enumeration_plan=graph["enumerationPlan"],
            dispatch=dispatch,
            stage_receipts=bad_receipts,
            prior_records=[],
        )
    expect_key(go_join, "PROVIDER_RETURN_VIEW_NOT_ON_RECEIPT", "owner-malformed-receipt-join")
    if close_error:
        fail("M3 close APIs failed after successful bind: " + close_error)


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
    test_receipt_omits_view_refuses,
    test_stage_not_in_execution_plan_refuses,
    test_analyze_subset_does_not_equate_request_and_retained_ordinal,
    test_integer_stage_id_refuses_schema,
    test_row_producer_closure_is_not_authority,
    test_stage_spec_digest_mismatch_refuses,
    test_receipt_mismatch_refuses,
    test_evaluator_closure_refuses,
    test_c15_conflict_from_worker_companion,
    test_two_batch_two_stage_positive,
    test_provider_conflict_prior_records_current_mint_map,
    test_malformed_companion_schema,
    test_package_first_party_companion,
    test_external_file_companion,
    test_unknown_package_companion_null_paths,
    test_origin_host_internal_does_not_capture,
    test_origin_provider_return_unbound_envelope_refuses,
    test_origin_probe_digests_not_captured,
    test_public_route_host_authored,
    test_internal_keys_are_not_domain_detail_codes,
    test_live_d9_not_discharged,
    test_partial_companion_omit_other_candidate,
    test_refused_batch_captures_nothing,
    test_mint_payload_mismatch_refuses,
    test_different_anchor_same_length_refuses,
    test_same_path_different_span_refuses,
    test_omitted_dispatch_refuses,
    test_analysis_ordinal_not_in_dispatch_refuses,
    test_bind_without_receipts_refuses,
    test_buffer_does_not_require_receipts_or_views,
    test_schemas_are_not_mutated_at_import,
    test_owner_admitted_semantic_fixture_positive,
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
        "standing": (
            "FactBatchV3 CBOR companion → host projection against DispatchBindingV1 "
            "and execution-plan stage-spec; owner-positive uses semantic fixture + M3 close APIs; "
            "not compiler TCB authenticity; not full Run product qualification; LIVE D9 not discharged"
        ),
        "ok": ok,
        "passed": sum(1 for r in results if r["ok"]),
        "failed": sum(1 for r in results if not r["ok"]),
        "fullRun": False,
        "helperDoesNotProveTcbAuthenticity": True,
        "results": results,
    }
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
