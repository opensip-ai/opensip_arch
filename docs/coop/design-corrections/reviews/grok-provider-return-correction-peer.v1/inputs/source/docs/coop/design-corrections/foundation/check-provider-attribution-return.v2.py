"""Provider-return channel controls. Schema/atom boundary. Not full Run replay."""
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
FM = M.FM

U1 = "11" * 32
C_PROV = "closure2:" + "aa" * 32
C_PROV2 = "closure2:" + "ee" * 32
C_EVAL = "closure2:" + "bb" * 32
PLAN = "plan2:" + "cc" * 32
SNAP = "snapshot2:" + "aa" * 32


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


def plan_one(kinds=None):
    kinds = kinds or ["symbol", "file"]
    return {
        "schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": H("0"), "membershipDigest": H("0"),
        "cells": [{
            "capabilityId": "imports", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
            "required": True, "kinds": kinds,
            "programBindings": [{
                "ordinal": 0, "provenance": "default-unit",
                "enumerator": {"status": "selected", "closureId": C_PROV},
                "nativeContextDigest": H("0"), "universe": U1, "programEntry": None,
                "extents": [{"kind": k, "paths": ["src/a.ts"]} for k in kinds],
            }],
        }],
    }


def imports_fact(fid, resolved="file:src/a.ts"):
    return {
        "factId": fid, "relation": "imports", "resolution": "resolved-target",
        "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
        "confidenceMillionths": 1000000,
        "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a", "resolvedTarget": resolved},
        "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
    }


def sidecar(fid, native, kind="file", occupancy="first-party", exported=None, logical=None,
            manifest=None, evaluation=None, producer=C_PROV):
    if occupancy == "first-party" and evaluation is None:
        evaluation = native if kind == "symbol" else None
    if occupancy != "first-party":
        evaluation = None
    return {
        "schemaVersion": 2, "planId": PLAN, "sourceFactId": fid, "producerClosure": producer,
        "targetUniverse": U1, "targetNativeId": native, "kind": kind, "occupancy": occupancy,
        "exported": exported, "logicalPath": logical, "packageManifestPath": manifest,
        "evaluationNativeId": evaluation,
    }


def envelope(records, stage=0, producer=C_PROV):
    ordered = sorted(records, key=lambda r: r["sourceFactId"].encode("utf-8"))
    return {
        "schemaVersion": 2, "planId": PLAN, "producerClosure": producer,
        "stageOrdinal": stage, "records": ordered,
    }


KW = None


def kw():
    global KW
    if KW is None:
        KW = dict(
            plan_id=PLAN, producer_closure=C_PROV, stage_ordinal=0,
            inventories=[inv_file(), inv_file("src/b.ts"), inv_symbol()],
            enumeration_plan=plan_one(),
            closures={C_PROV: {"kind": "provider"}, C_PROV2: {"kind": "provider"}, C_EVAL: {"kind": "evaluator"}},
        )
    return dict(KW)


def expect_key(fn, key, label):
    try:
        fn()
    except M.ProviderReturnAdmissionError as exc:
        if exc.key != key:
            fail(f"{label}: key {exc.key!r} != {key!r}")
        return exc
    except AM.AtomAdmissionError as exc:
        if exc.key != key:
            fail(f"{label}: atom key {exc.key!r} != {key!r}")
        return exc
    fail(f"{label}: expected {key}")


def test_positive_file_first_party_capture():
    fid = fact2("1")
    rec = sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party", evaluation="src/a.ts")
    out = M.admit_provider_attribution_return(
        envelope([rec]), facts={fid: imports_fact(fid)}, **kw()
    )
    if out["status"] != "admitted":
        fail("positive status")
    if len(out["records"]) != 1 or out["records"][0]["evaluationNativeId"] != "src/a.ts":
        fail("positive record")
    if len(out["hostDerivedRefs"]) != 1 or out["hostDerivedRefs"][0]["domain"] != "target-attribution":
        fail("positive capture domain")
    digest = out["hostDerivedRefs"][0]["digest"]
    if digest not in out["blobs"]:
        fail("positive blob missing")
    if hashlib.sha256(out["blobs"][digest]).hexdigest() != digest:
        fail("positive blob digest")
    parsed = json.loads(out["blobs"][digest].decode("utf-8"))
    if parsed["evaluationNativeId"] != "src/a.ts":
        fail("positive captured identity")
    if any(r.get("domain") != "target-attribution" for r in out["hostDerivedRefs"]):
        fail("envelope must not become a digest domain")


def test_missing_envelope_is_lawful_omission():
    fid = fact2("1")
    out = M.admit_provider_attribution_return(
        None, facts={fid: imports_fact(fid)}, **kw()
    )
    if out["status"] != "omitted" or out["hostDerivedRefs"] or out["blobs"] or out["records"]:
        fail("missing envelope must capture nothing")


def test_present_empty_records_is_incomplete_not_omission():
    fid = fact2("1")
    out = M.admit_provider_attribution_return(
        envelope([]), facts={fid: imports_fact(fid)}, **kw()
    )
    if out["status"] != "admitted" or out["records"] or out["hostDerivedRefs"]:
        fail("empty records is present incomplete return")


def test_malformed_envelope_schema():
    fid = fact2("1")
    bad = envelope([sidecar(fid, "file:src/a.ts", evaluation="src/a.ts")])
    bad["schemaVersion"] = 1

    def go():
        M.admit_provider_attribution_return(bad, facts={fid: imports_fact(fid)}, **kw())
    expect_key(go, "PROVIDER_RETURN_SCHEMA", "malformed-envelope-version")


def test_malformed_record_null_eval_id():
    fid = fact2("1")
    rec = sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party", evaluation=None)

    def go():
        M.admit_provider_attribution_return(envelope([rec]), facts={fid: imports_fact(fid)}, **kw())
    expect_key(go, "TARGET_ATTRIBUTION_SCHEMA", "malformed-null-eval-id")


def test_unknown_fact_refuses():
    fid, extra = fact2("1"), fact2("9")
    rec = sidecar(extra, "file:src/a.ts", evaluation="src/a.ts")

    def go():
        M.admit_provider_attribution_return(envelope([rec]), facts={fid: imports_fact(fid)}, **kw())
    expect_key(go, "PROVIDER_RETURN_UNKNOWN_FACT", "extra-unknown-fact")


def test_record_order_refuses():
    fid1, fid2 = fact2("2"), fact2("1")
    recs = [
        sidecar(fid1, "file:src/a.ts", evaluation="src/a.ts"),
        sidecar(fid2, "file:src/a.ts", evaluation="src/a.ts"),
    ]
    env = {
        "schemaVersion": 2, "planId": PLAN, "producerClosure": C_PROV,
        "stageOrdinal": 0, "records": recs,
    }

    def go():
        M.admit_provider_attribution_return(
            env, facts={fid1: imports_fact(fid1), fid2: imports_fact(fid2)}, **kw()
        )
    expect_key(go, "PROVIDER_RETURN_SCHEMA", "record-order")


def test_c15_ephemeral_identity_conflict():
    fid = fact2("1")
    rec = sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party", evaluation="src/b.ts")
    args = kw()
    args["inventories"] = [inv_file("file:src/a.ts"), inv_file("src/b.ts"), inv_symbol()]

    def go():
        M.admit_provider_attribution_return(
            envelope([rec]), facts={fid: imports_fact(fid, "file:src/a.ts")}, **args
        )
    expect_key(go, "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT", "c15-conflict")


def test_c15_agreement_same_colon_path_identity():
    fid = fact2("1")
    rec = sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party", evaluation="file:src/a.ts")
    args = kw()
    args["inventories"] = [inv_file("file:src/a.ts"), inv_file("src/b.ts"), inv_symbol()]
    out = M.admit_provider_attribution_return(
        envelope([rec]), facts={fid: imports_fact(fid, "file:src/a.ts")}, **args
    )
    if out["status"] != "admitted":
        fail("c15 agreement")
    if out["records"][0]["evaluationNativeId"] != "file:src/a.ts":
        fail("c15 agreement identity")


def test_partial_omit_is_lawful():
    fid1, fid2 = fact2("1"), fact2("2")
    rec = sidecar(fid1, "file:src/a.ts", evaluation="src/a.ts")
    out = M.admit_provider_attribution_return(
        envelope([rec]),
        facts={fid1: imports_fact(fid1), fid2: imports_fact(fid2, "file:src/b.ts")},
        **kw(),
    )
    if out["status"] != "admitted" or len(out["records"]) != 1:
        fail("partial omit")
    if out["records"][0]["sourceFactId"] != fid1:
        fail("partial omit kept fact")


def test_refused_envelope_captures_nothing():
    fid = fact2("1")
    rec = sidecar(fid, "file:src/a.ts", evaluation="src/b.ts")
    args = kw()
    args["inventories"] = [inv_file("file:src/a.ts"), inv_file("src/b.ts"), inv_symbol()]
    try:
        M.admit_provider_attribution_return(
            envelope([rec]), facts={fid: imports_fact(fid)}, **args
        )
    except M.ProviderReturnAdmissionError:
        return
    fail("refused envelope must not return capture")


def test_public_route_schema_provider():
    raw = b"TARGET_ATTRIBUTION_SCHEMA owner-diagnostic"
    routed = M.route_internal_key("TARGET_ATTRIBUTION_SCHEMA", "provider-return", raw, "retained:fixture")
    term = routed["termination"]
    if term["class"] != "operational-failed" or term["errorCode"] != "PROVIDER.PROTOCOL_VIOLATION":
        fail("schema provider termination")
    if term.get("faultCause") != "provider-protocol":
        fail("schema provider faultCause")
    if term["domainDetail"]["code"] != "EVALUATION.INPUT_REFUSED":
        fail("schema provider detail")


def test_public_route_conflict_provider():
    raw = b"TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT owner-diagnostic"
    routed = M.route_internal_key(
        "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT", "provider-return", raw, "retained:fixture"
    )
    if routed["termination"]["domainDetail"]["code"] != "EVALUATION.INPUT_REFUSED":
        fail("conflict provider detail")
    if routed["observation"]["condition"] != "input-join-invalid":
        fail("conflict condition")
    if routed["observation"]["origin"] != "provider-return":
        fail("conflict origin")


def test_public_route_host_invented():
    raw = b"TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT host-constructed"
    routed = M.route_internal_key(
        "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT", "host-internal", raw, "retained:fixture"
    )
    term = routed["termination"]
    if term["errorCode"] != "SYSTEM.OUTCOME.ILLEGAL_STATE" or term.get("faultCause") != "host-invariant":
        fail("host invented termination")
    if term["domainDetail"]["code"] != "HOST.INVARIANT_VIOLATED":
        fail("host invented detail")


def test_internal_keys_are_not_domain_detail_codes():
    common = json.loads(
        (HERE.parent / "workflows" / "schemas" / "evaluator3" / "common.schema.json").read_text()
    )
    codes = set(common["$defs"]["DomainDetailCode"]["enum"])
    for key in list(M.SCHEMA_KEYS) + list(M.JOIN_KEYS):
        if key in codes:
            fail("internal key leaked as DomainDetailCode: " + key)
        if key.startswith("D9") or key.startswith("EVALUATION.TARGET"):
            fail("invented public alias")


def test_live_d9_not_discharged():
    if M.ROUTE_LAW["liveD9"] != "not discharged":
        fail("live D9 standing")
    if "d9_successor_codes" in dir(M) and getattr(M, "d9_successor_codes")():
        fail("no D9 successor codes")


def test_stage_mismatch():
    fid = fact2("1")
    rec = sidecar(fid, "file:src/a.ts", evaluation="src/a.ts")

    def go():
        args = kw()
        args["stage_ordinal"] = 1
        M.admit_provider_attribution_return(envelope([rec], stage=0), facts={fid: imports_fact(fid)}, **args)
    expect_key(go, "PROVIDER_RETURN_STAGE_ORDINAL", "stage")


def test_atom_boundary_c15_overwrite_refuses():
    fid = fact2("1")
    inputs = {
        "planId": PLAN,
        "facts": {fid: imports_fact(fid, "file:src/a.ts")},
        "inventories": [inv_file("file:src/a.ts"), inv_file("src/b.ts"), inv_symbol()],
        "enumerationPlan": plan_one(),
        "closures": {C_PROV: {"kind": "provider"}},
        "targetAttributions": {
            fid: sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party", evaluation="src/b.ts"),
        },
        "scopes": {}, "coverages": {}, "imports": {}, "importPayloads": {},
        "importObservations": {}, "planSelectedImportIds": [], "evaluationInputRefs": [],
        "incomingSearchAttestations": [], "universeDomains": {U1: "native.semantic-universe.typescript.v2"},
        "importScopeAdapter": "normalized-import-scope-descriptor",
    }

    def go():
        AM.evaluate_atom(
            {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
             "endpoint": "target", "filters": []},
            {"universe": U1, "kind": "file", "nativeSubjectId": "src/b.ts"},
            inputs,
        )
    try:
        go()
    except AM.AtomAdmissionError as exc:
        if exc.key != "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT":
            fail("atom c15 key " + exc.key)
        return
    fail("atom c15 expected refusal; silent overwrite would match src/b.ts")


CASES = [
    test_positive_file_first_party_capture,
    test_missing_envelope_is_lawful_omission,
    test_present_empty_records_is_incomplete_not_omission,
    test_malformed_envelope_schema,
    test_malformed_record_null_eval_id,
    test_unknown_fact_refuses,
    test_record_order_refuses,
    test_c15_ephemeral_identity_conflict,
    test_c15_agreement_same_colon_path_identity,
    test_partial_omit_is_lawful,
    test_refused_envelope_captures_nothing,
    test_public_route_schema_provider,
    test_public_route_conflict_provider,
    test_public_route_host_invented,
    test_internal_keys_are_not_domain_detail_codes,
    test_live_d9_not_discharged,
    test_stage_mismatch,
    test_atom_boundary_c15_overwrite_refuses,
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
        "standing": "provider-return schema/atom/capture controls; not full Run replay; LIVE D9 not discharged",
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
