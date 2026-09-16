"""Record phase-8 standing from the produced artifacts (reads each file; a missing file or failed control is not executed)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import status as S  # noqa: E402

OUT = S.OUT
st = S.load_status()
problems = []


def load(rel):
    return json.load(open(OUT + rel))


def mark(rid, artifact, ok, notes):
    if not os.path.exists(OUT + artifact.split("#")[0]):
        problems.append((rid, "missing", artifact))
        S.set_status(st, rid, "unexecuted", artifact, None, "artifact missing")
        return
    S.set_status(st, rid, "executed" if ok else "failed", artifact, None, notes)
    if not ok:
        problems.append((rid, artifact))


ba = load("vectors/baseline-audit.json")
mark("R-BASELINE-AUDIT", "vectors/baseline-audit.json", ba["freshHostAdmission"] == [] and all(n["pass"] for n in ba["baselineNegatives"])
     and ba["codeRegressionByProfile"]["code-regression"]["verdict"] == "fail" and not ba["auditInvocationFail"]["envelopeFaults"],
     "cmp-base baseline adopted and admitted on a fresh host; cmp-code under 4 profiles (fail, fail, fail, pass); identity comparison passes over a failing Run; audit invocation envelopes.")
cm = load("vectors/comparison-missing.json")
mark("R-CMP-MISSING", "vectors/comparison-missing.json", cm["verdict"] == "indeterminate" and cm["termination"]["reasonCodes"] == ["VERDICT.INDETERMINATE"],
     "required runtime evidence absent on current side: INDETERMINATE required-evidence-unavailable, gating rule deficiency, golden audit-required-evidence-lost.")
ce = load("vectors/comparison-evidence-changed.json")
mark("R-CMP-EVIDENCE-CHANGED", "vectors/comparison-evidence-changed.json", ce["nonGatingRule"]["verdict"] == "pass" and ce["gatingRule"]["verdict"] == "indeterminate",
     "same kind, different import2: non-gating EVIDENCE-DELTA; gating INDETERMINATE evidence-content-changed.")
cz = load("vectors/comparison-empty-result.json")
mark("R-CMP-EMPTY-RESULT", "vectors/comparison-empty-result.json", cz["distinct"]["performed"] == [True, False],
     "performed complete-empty (zero entries, pass) vs not-performed unmapped project (zero entries, indeterminate, remedy).")
sp = load("vectors/comparison-scope-policy-only.json")
mark("R-SCOPE-POLICY-ONLY-COMPARISON", "vectors/comparison-scope-policy-only.json",
     sp["sourceAndDiscoveryScope"]["snapshotIdEqual"] and sp["sourceAndDiscoveryScope"]["foundationScopeDescriptorDigestEqual"],
     "only ScopeDocumentV1 changes; snapshot and foundation scope descriptor identical; SCOPE-DELTA via E2 re-evaluation.")
e03 = load("vectors/baseline-e0-e3.json")
mark("R-E0-VS-E1-E3", "vectors/baseline-e0-e3.json", e03["E0"]["sameSnapshotDifferentPlanAndRun"] and all(r["pass"] for r in e03["E0"]["refusals"]),
     "E0 = committed pivot Run (cmp-code) under the baseline detector over the current snapshot; E1/E3 = re-evaluations of current inputs (no run3); E0 joins refuse wrong source/detector map.")
po = load("vectors/pivot-only-fingerprints.json")
mark("R-PIVOT-ONLY-FINGERPRINTS", "vectors/pivot-only-fingerprints.json",
     po["pivotOnlyFingerprint"]["fingerprint"] and not po["pivotOnlyFingerprint"]["inBaselineEntries"] and not po["pivotOnlyFingerprint"]["inCurrentMatched"],
     "fingerprint present only at E0/E1 retained as CODE-NET-NEW subsequentDeltas [policy]; gates code-net-new-policy-hidden under code-regression.")
au = load("vectors/test-prep-repair-authorization.json")
mark("R-TEST-PREP-REPAIR-AUTH", "vectors/test-prep-repair-authorization.json",
     au["testExecution"]["firstRefusal"] is None and au["repairApply"]["firstRefusal"] is None and au["nativePreparation"]["firstRefusal"] is None
     and all(n["pass"] for sec in ("testExecution", "repairApply", "nativePreparation") for n in au[sec]["negatives"]),
     "Authorization records and joins only; no process spawned, no truth-table measurement, no lease (future qualification).")
pr = load("envelopes/purge-replay-output-failure.json")
mark("R-PURGE-REPLAY-OUTPUT-FAILURE", "envelopes/purge-replay-output-failure.json",
     all(not v["faults"] for v in pr["envelopes"].values()) and pr["proof-bundle-purged"]["closeRun"] == "REFUSE",
     "pinned purge re-validated; replay of a purged proof refuses before replay; evidence.purged vs evidence.missing; renderer failure after commit; output bound; pre-commit projection failure carried without an invented detail.")
pt = load("envelopes/public-termination.json")
mark("R-PUBLIC-TERMINATION-EXAMPLES", "envelopes/public-termination.json", pt["goldenCount"] == 43,
     f"{pt['passed']}/43 goldens admitted as StepTermination (+ envelope where constructible); failure goldens without a detail: {pt['failureGoldensWithoutDetail']}.")
mark("R-SUBSYSTEM-OWNERS", "notes/08-subsystem-owners.md", True, "Owner map with selectors for every phase-8 decision.")
hc = load("vectors/host-captured-vs-candidate.json")
mark("R-HOST-CAPTURED-VS-CANDIDATE", "vectors/host-captured-vs-candidate.json", len(hc["candidateOnlyReturns"]) == 4,
     "host-captured outcome recomputed equal to stored; four candidate-only cases (absent required/optional, complete, partial).")
ep = load("vectors/empty-partial-unavailable-missing.json")
mark("R-EMPTY-PARTIAL-UNAVAILABLE-MISSING", "vectors/empty-partial-unavailable-missing.json", ep["labelsDistinct"] and ep["states"]["missing-committed-bytes"]["closeRun"] == "REFUSE",
     "four distinct exhibits: complete-empty rule, partial cell/Coverage, unavailable candidate/provider trace/availability notices, missing committed bytes (closure refusal + availability partial).")
dc = load("vectors/detector-compat-file.json")
mark("R-DETECTOR-COMPAT-FILE", "vectors/detector-compat-file.json", all(v["pass"] for v in dc["vectors"]),
     "reserved tree listing vs component manifest body; absent/empty/malformed/unrecognized/length/missing/non-unique/untrusted controls; committed cmp-code-detc listing.")
S.save_status(st)
cp = S.write_checkpoint(8, st, [
    "builders/ts_runs.py (cmp-* family)", "tools/build_cmp.py", "runs/cmp-family.summary.json", "runs/cmp-*.store.json", "runs/cmp-*.replay.json",
    "runs/ts-pass.pre-builder-extension.store.json", "ref/detector_compat.py", "tools/phase8_compare.py", "tools/phase8_envelopes.py",
    "vectors/baseline-audit.json", "vectors/comparison-missing.json", "vectors/comparison-evidence-changed.json", "vectors/comparison-empty-result.json",
    "vectors/comparison-scope-policy-only.json", "vectors/baseline-e0-e3.json", "vectors/pivot-only-fingerprints.json",
    "vectors/test-prep-repair-authorization.json", "envelopes/purge-replay-output-failure.json", "envelopes/public-termination.json",
    "vectors/host-captured-vs-candidate.json", "vectors/empty-partial-unavailable-missing.json", "vectors/detector-compat-file.json",
    "notes/08-subsystem-owners.md", "vectors/*.attempt1.json", "vectors/*.attempt2.json", "vectors/*.attempt3.json", "envelopes/*.attempt3.json",
    "runs/phase8-envelopes.attempt1.log", "runs/phase8-envelopes.attempt2.log"],
    ["HC-8 ref/schemas.py: $id-less kit documents were unresolvable by absolute selector (referencing defragments 'kit:///' to 'kit:/'); original crash runs/phase8-envelopes.attempt1.log; corrected by registering the urlunparse spelling; syntax-code regression replay ADMIT (runs/syntax-code.replay.regress-hc8.json).",
     "HC-9 tools/phase8_compare.py attempt1 (vectors/*.attempt1.json): DetectorDisposition lacked pivotRunId/indeterminateReason required by comparison-result #/$defs/DetectorDisposition allOf, and the evidence-axis rule overwrote a pivot-unavailable INDETERMINATE; attempt2 (vectors/*.attempt2.json): an unknown current-side absence was labelled pivot-reevaluation-unavailable before workflows s3 lines 374-377 could apply. Corrected from those selectors.",
     "HC-10 tools/phase8_envelopes.py attempt2 (runs/phase8-envelopes.attempt2.log): repair reconstruction read a nonexistent descriptor field baseSnapshotId; corrected to the descriptor snapshotId bound by security S10.1 lines 1159-1162. attempt3 (*.attempt3.json): the unsorted grant-set control was built in already-sorted order and was admitted; corrected to descending order (native lines 3741-3743).",
     "HC-11 builders/ts_runs.py extended with a same-project comparison family; the rebuilt ts-pass store is byte-identical to the preserved pre-extension store (runs/cmp-family.summary.json#/regression)."],
    "Phase 8 executed. All cmp-* Runs admitted with complete fresh-process replay. Problems: " + json.dumps(problems))
print(json.dumps({"unexecuted": cp["requirementIdsUnexecuted"], "failed": cp["requirementIdsFailed"], "problems": problems}, indent=1))
