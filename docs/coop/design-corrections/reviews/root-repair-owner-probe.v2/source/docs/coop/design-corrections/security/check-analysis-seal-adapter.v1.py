"""Bounded analysis-SEAL adapter check. Independent of the pin-gated official security suite.

Public reference boundary: admit_analysis_seal requires identity-model.v3.close_run on a
supplied retained graph and compares RunId. Prefix dispatch is a different helper.
Linearize is an abstract brokered-effect schedule, not this check.

Not a product host. Not official pin qualification. Synthetic fixtures only.
Does not regenerate source-pins. Does not invoke check-security-lifecycle.v1.py.

  python -I -B check-analysis-seal-adapter.v1.py
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOUNDATION = HERE.parent / "foundation"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


S = load("seal_adapter_security", HERE / "security_lifecycle_model_v1.py")
F = load("seal_adapter_fixture", FOUNDATION / "evaluator_graph_fixture.v3.py")
X = load("seal_adapter_exec_in", FOUNDATION / "execution_inputs_fixture.v3.py")
R = load("seal_adapter_replay", FOUNDATION / "evaluator_replay_model.v3.py")
M = R.M
E = R.E
C = M.C


def seal_derived(graph, result, objects, blobs):
    objects = copy.deepcopy(objects)
    blobs = copy.deepcopy(blobs)
    objects.update(result["objects"])
    blobs.update(result["blobs"])
    i = graph["inputs"]

    def add(domain, fields):
        value = {"schemaVersion": 3, **fields}
        key = M.identifier(domain, value)
        objects[key] = (domain, value)
        return key

    evidence = add("semantic-evidence", {
        "planId": i["planId"], "viewIds": graph["viewIds"], "coverageIds": graph["coverageIds"],
        "importIds": i["plan"]["importIds"], "findingIds": result["proof"]["findingIds"],
        "proofBundleId": result["proofBundleId"],
    })
    sid = add("evaluation-seal", {
        "planId": i["planId"], "executionPlanId": i["executionPlanId"], "evidenceId": evidence,
        "evaluatorClosure": i["evaluatorClosure"], "policyDigest": i["plan"]["policyDigest"],
        "proofBundleId": result["proofBundleId"], "verdict": result["proof"]["verdict"],
    })
    run = {
        "schemaVersion": 3, "projectId": graph["snapshot"]["projectId"],
        "snapshotId": i["plan"]["snapshotId"], "planId": i["planId"], "evidenceId": evidence,
        "evaluationSealId": sid, "capabilityManifestId": i["plan"]["capabilityManifestId"],
    }
    return run, objects, blobs


def remint_first_finding(run, objects, blobs):
    run = copy.deepcopy(run)
    objects = copy.deepcopy(objects)
    blobs = copy.deepcopy(blobs)
    evidence = objects[run["evidenceId"]][1]
    seal = objects[run["evaluationSealId"]][1]
    proof = copy.deepcopy(objects[seal["proofBundleId"]][1])
    fid = proof["findingIds"][0]
    finding = copy.deepcopy(objects[fid][1])
    finding["severity"] = "warning" if finding.get("severity") != "warning" else "error"
    newfid = M.identifier("finding", finding)
    objects[newfid] = ("finding", finding)

    def replace(value):
        if type(value) is str:
            return newfid if value == fid else value
        if type(value) is list:
            return [replace(x) for x in value]
        if type(value) is dict:
            return {k: replace(v) for k, v in value.items()}
        return value

    proof = replace(proof)
    # findingIds arrays are x-opensip-order: canonical-set. Substituting one element does not
    # preserve that order, so re-normalise every canonical-set finding array after replacement
    # rather than relying on the replacement digest sorting into the replaced position.
    proof["findingIds"] = R.E.cset(proof["findingIds"])
    proof["waivedFindingIds"] = R.E.cset(proof["waivedFindingIds"])
    for _rr in proof["ruleResults"]:
        _rr["findingIds"] = R.E.cset(_rr["findingIds"])
    pid = M.identifier("proof-bundle", proof)
    objects[pid] = ("proof-bundle", proof)
    evidence = replace(copy.deepcopy(evidence))
    evidence["findingIds"] = R.E.cset(evidence["findingIds"])
    evidence["proofBundleId"] = pid
    eid = M.identifier("semantic-evidence", evidence)
    objects[eid] = ("semantic-evidence", evidence)
    seal = copy.deepcopy(seal)
    seal["proofBundleId"] = pid
    seal["evidenceId"] = eid
    sid = M.identifier("evaluation-seal", seal)
    objects[sid] = ("evaluation-seal", seal)
    run["evidenceId"] = eid
    run["evaluationSealId"] = sid
    return run, objects, blobs


def journal_seal(run_id, seq=1):
    return {
        "recordType": "SEAL",
        "recordSchema": 3,
        "grantGeneration": 1,
        "seq": seq,
        "operationRef": "op-adapter-0000000000000000000000000000",
        "runId": run_id,
    }


def full_admitted_graph():
    """Public fixture API: build_file_inputs, attach_host_capture BEFORE seed seal, derive, close_run.

    attach_host_capture is required because reconstruct now demands exactly one
    evaluationInputRefs member domain=execution-inputs and proof.executionInputsDigest.
    """
    g = F.build_file_inputs()
    attached = X.attach_host_capture(g)
    if attached["admission"]["result"] != "ADMIT":
        raise RuntimeError("EXECUTION_INPUTS_ATTACH:" + ",".join(attached["admission"].get("refusals") or []))
    seed, objects, blobs, _ = F.seal_fixture(g)
    _rid, owner = M.open_run_closure(seed, objects, blobs)
    i = g["inputs"]
    result = R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"], i["evaluationInputRefs"], objects, blobs, owner)
    run, objects, blobs = seal_derived(g, result, objects, blobs)
    run_id = M.close_run(run, objects, blobs)
    return run, objects, blobs, run_id, attached["digest"]


def expect_reject(fn, key):
    try:
        fn()
    except S.Reject as e:
        if str(e) == key or str(e).startswith(key):
            return str(e)
        raise AssertionError("reject %r want prefix %r" % (str(e), key))
    raise AssertionError("expected Reject %s" % key)


def main() -> int:
    rows = []
    # Prefix helper is not close_run.
    prefix = S.admit_seal_run_id_prefix("run3:" + "a" * 64)
    rows.append({"case": "prefix-nonfixture-admits-without-close-run", "result": prefix,
                 "ok": prefix["authority"] == "run3-pattern"})
    expect_reject(lambda: S.admit_seal_run_id_prefix(S.FIXTURE_SEAL_RUN_ID), "SEAL_RUN_ID_FIXTURE_NOT_AUTHORITY")
    rows.append({"case": "prefix-fixture-refused", "result": "SEAL_RUN_ID_FIXTURE_NOT_AUTHORITY", "ok": True})

    expect_reject(lambda: S.admit_seal_run_id_prefix("run3:" + "a" * 64 + "\n"), "SEAL_RUN_ID_INVALID")
    rows.append({"case": "prefix-trailing-newline-refused", "result": "SEAL_RUN_ID_INVALID", "ok": True})

    missing = {"recordSchema": 3, "grantGeneration": 1, "seq": 1, "operationRef": "op-x",
               "runId": "run3:" + "b" * 64}
    expect_reject(lambda: S.admit_journal_record(missing), "JOURNAL_RECORD_SCHEMA_INVALID")
    rows.append({"case": "journal-missing-recordType-invalid", "result": "JOURNAL_RECORD_SCHEMA_INVALID", "ok": True})
    hist = {"recordType": "SEAL", "recordSchema": 2, "grantGeneration": 1, "seq": 1,
            "operationRef": "op-x", "runId": "run2:" + "c" * 64}
    expect_reject(lambda: S.admit_journal_record(hist), "JOURNAL_RECORD_SCHEMA_HISTORICAL")
    rows.append({"case": "journal-historical-2-unchanged", "result": "JOURNAL_RECORD_SCHEMA_HISTORICAL", "ok": True})

    run, objects, blobs, run_id, digest = full_admitted_graph()
    if not str(run_id).startswith("run3:") or run_id == S.FIXTURE_SEAL_RUN_ID:
        raise AssertionError("close_run did not return a live run3")
    rec = journal_seal(run_id)
    admitted = S.admit_analysis_seal(rec, run, objects, blobs)
    rows.append({"case": "analysis-seal-full-admitted", "result": admitted, "runId": run_id,
                 "executionInputsDigest": digest, "ok": admitted["authority"] == "identity-model.v3.close_run"})

    wrong = journal_seal("run3:" + "d" * 64)
    expect_reject(lambda: S.admit_analysis_seal(wrong, run, objects, blobs), "SEAL_RUN_ID_MISMATCH")
    rows.append({"case": "analysis-seal-wrong-id", "result": "SEAL_RUN_ID_MISMATCH", "ok": True})

    expect_reject(lambda: S.admit_analysis_seal(journal_seal(S.FIXTURE_SEAL_RUN_ID), run, objects, blobs),
                  "SEAL_RUN_ID_FIXTURE_NOT_AUTHORITY")
    rows.append({"case": "analysis-seal-fixture-id-not-authority", "result": "SEAL_RUN_ID_FIXTURE_NOT_AUTHORITY", "ok": True})

    owner_run, owner_objects, owner_blobs = remint_first_finding(run, objects, blobs)
    owner_id, _ = M.open_run_closure(owner_run, owner_objects, owner_blobs)
    if not str(owner_id).startswith("run3:"):
        raise AssertionError("owner-only remint failed open_run_closure")
    expect_reject(lambda: S.admit_analysis_seal(journal_seal(owner_id), owner_run, owner_objects, owner_blobs),
                  "SEAL_CLOSE_RUN_REFUSED:")
    rows.append({"case": "analysis-seal-owner-only-semantically-false", "ownerRunId": owner_id,
                 "result": "SEAL_CLOSE_RUN_REFUSED", "ok": True})

    # The adapter consumes its own identity module's normalized outcome types.
    # Same-named foreign exceptions and owner-looking text are not owner refusals.
    identity = S._identity_model_v3()
    original_close = identity.close_run
    def raising(exc):
        def fail(*args, **kwargs):
            raise exc
        return fail
    try:
        for label, exc in (
            ("admission", identity.C.AdmissionError("REFERENCE_IDENTITY")),
            ("missing", identity.EvidenceUnavailable("retained:test")),
            ("replay-mismatch", identity.CompleteReplayMismatch("EVALUATOR_COMPLETE_PROOF_REPLAY")),
        ):
            identity.close_run = raising(exc)
            try:
                S.admit_analysis_seal(rec, run, objects, blobs)
            except S.Reject as refused:
                assert str(refused).startswith("SEAL_CLOSE_RUN_REFUSED:") and refused.__cause__ is exc
            else:
                raise AssertionError("typed owner refusal admitted: " + label)
            rows.append({"case": "analysis-seal-typed-" + label, "ok": True,
                         "standing": "in-process adapter boundary control, not product fault injection"})
        for label, exc in (
            ("foreign-admission-name", type("AdmissionError", (Exception,), {})("REFERENCE_IDENTITY")),
            ("foreign-mismatch-name", type("CompleteReplayMismatch", (Exception,), {})("EVALUATOR_COMPLETE_PROOF_REPLAY")),
            ("owner-looking-text", RuntimeError("EVIDENCE_UNAVAILABLE:retained:test")),
        ):
            identity.close_run = raising(exc)
            try:
                S.admit_analysis_seal(rec, run, objects, blobs)
            except Exception as raised:
                assert raised is exc, "host defect misclassified: " + label
            else:
                raise AssertionError("host defect admitted: " + label)
            rows.append({"case": "analysis-seal-host-defect-" + label, "ok": True,
                         "standing": "unexpected exception propagates; outer host fault projection not implemented here"})
    finally:
        identity.close_run = original_close
    restored = S.admit_analysis_seal(rec, run, objects, blobs)
    rows.append({"case": "analysis-seal-lawful-after-boundary-controls", "ok": restored == admitted})

    failed = [r for r in rows if not r.get("ok")]
    report = {
        "artifact": "opensip.security.analysis-seal-adapter-check",
        "version": 1,
        "standing": "design reference; not product qualification; independent of pin-gated official suite",
        "passed": not failed,
        "productQualification": False,
        "counts": {"total": len(rows), "pass": len(rows) - len(failed), "fail": len(failed)},
        "cases": rows,
        "joins": {
            "close_run": "identity-model.v3.close_run",
            "executionInputsDigest": "proof-bundle required field; reconstruct requires evaluationInputRefs domain=execution-inputs; attach_host_capture before seed seal",
            "linearize": "abstract brokered-effect TCB; fixture runId; not this adapter",
        },
    }
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
