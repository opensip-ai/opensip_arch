"""Record phase-8 standing from the produced source39 artifacts (reads each file; a missing file or failed control is not executed)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import hc_source42 as HC  # noqa: E402
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
ak = load("vectors/comparison-absence-knowledge.json")
reasons = lambda b: {e["indeterminateReason"] for e in b["entries"]}  # noqa: E731
mark("R-BASELINE-AUDIT", "vectors/baseline-audit.json", ba["freshHostAdmission"] == [] and all(n["pass"] for n in ba["baselineNegatives"])
     and ba["codeRegressionByProfile"]["code-regression"]["verdict"] == "fail" and not ba["auditInvocationFail"]["envelopeFaults"]
     and reasons(ak["currentAbsenceUnknown"]) >= {"current-absence-unknown"} and reasons(ak["baselineAbsenceUnknown"]) == {"baseline-absence-unknown"},
     "cmp-base baseline adopted (RuleCoverage.absenceKnowledge recorded) and admitted on a fresh host; cmp-code under 4 profiles (fail, fail, fail, pass); identity "
     "comparison passes over a failing Run; audit invocation envelopes. Source39 absence knowledge: vectors/comparison-absence-knowledge.json "
     "(current-absence-unknown over the work-budget Run cmp-budget; baseline-absence-unknown with cmp-budget adopted as baseline).")
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
     "E0 = committed pivot Run under the baseline detector over the current snapshot; E1/E3 = re-evaluations of current inputs (no run3); E0 joins refuse wrong "
     "source/detector map; an unbound changed-detector pivot publishes pivot-reevaluation-unavailable (closed reason order).")
po = load("vectors/pivot-only-fingerprints.json")
mark("R-PIVOT-ONLY-FINGERPRINTS", "vectors/pivot-only-fingerprints.json",
     po["pivotOnlyFingerprint"]["fingerprint"] and not po["pivotOnlyFingerprint"]["inBaselineEntries"] and not po["pivotOnlyFingerprint"]["inCurrentMatched"],
     "fingerprint present only at pivots retained; over a complete-hit-set baseline it is CODE-NET-NEW subsequentDeltas [policy] and gates code-net-new-policy-hidden.")
au = load("vectors/test-prep-repair-authorization.json")
mark("R-TEST-PREP-REPAIR-AUTH", "vectors/test-prep-repair-authorization.json",
     au["testExecution"]["firstRefusal"] is None and au["repairApply"]["firstRefusal"] is None and au["nativePreparation"]["firstRefusal"] is None
     and all(n["pass"] for sec in ("testExecution", "repairApply", "nativePreparation") for n in au[sec]["negatives"]),
     "Authorization records and joins only (argvDigest per workflows s7 lines 1056-1064); no process spawned, no truth-table measurement, no lease (future qualification).")
pr = load("envelopes/purge-replay-output-failure.json")
mark("R-PURGE-REPLAY-OUTPUT-FAILURE", "envelopes/purge-replay-output-failure.json",
     all(not v["faults"] for v in pr["envelopes"].values()) and pr["proof-bundle-purged"]["closeRun"] == "REFUSE",
     "pinned purge re-validated; replay of a purged proof refuses before replay; evidence.purged vs evidence.missing; renderer failure after commit; output bound; "
     "pre-commit projection failure.")
pt = load("envelopes/public-termination.json")
rt = load("vectors/run-termination.json")
mark("R-PUBLIC-TERMINATION-EXAMPLES", "envelopes/public-termination.json",
     pt["goldenCount"] == 45 and pt["passed"] == 45 and not pt["failureGoldensWithoutDetail"] and not rt["assertionFailures"] and rt["d9Golden"]["equal"],
     f"{pt['passed']}/{pt['goldenCount']} command-inventory goldens admitted as StepTermination with complete envelopes; no failure golden lacks a detail. "
     f"Analysis-Run terminations derived by the run-termination owner over {len(rt['projections'])} closed Runs, with {len(rt['candidateChecks'])} candidate checks "
     f"and {len(rt['hostComposition'])} host-composition cases; D9 golden analysis-budget-exhausted reproduced (vectors/run-termination.json).")
mark("R-SUBSYSTEM-OWNERS", "notes/08-subsystem-owners.md", True, "Owner map with source41 selectors for every phase-8 decision, including the run-termination owner.")
hc = load("vectors/host-captured-vs-candidate.json")
mark("R-HOST-CAPTURED-VS-CANDIDATE", "vectors/host-captured-vs-candidate.json",
     len(hc["candidateOnlyReturns"]) == 4 and bool(hc["hostCapturedRequiredWork"]["requiredIncomplete"]["requiredRows"]),
     "host-captured outcome recomputed equal to stored; required-incomplete rows from Coverage on syntax-mixed-disclosed; four candidate-only cases.")
ep = load("vectors/empty-partial-unavailable-missing.json")
mark("R-EMPTY-PARTIAL-UNAVAILABLE-MISSING", "vectors/empty-partial-unavailable-missing.json",
     ep["labelsDistinct"] and ep["states"]["missing-committed-bytes"]["closeRun"] == "REFUSE" and bool(ep["states"]["partial"]["cellOutcomes"]),
     "four distinct exhibits: complete-empty rule, partial cell/Coverage (syntax-mixed-disclosed), unavailable candidate/provider trace/availability notices, missing "
     "committed bytes.")
dc = load("vectors/detector-compat-file.json")
mark("R-DETECTOR-COMPAT-FILE", "vectors/detector-compat-file.json", all(v["pass"] for v in dc["vectors"]),
     "reserved tree listing vs component manifest body; absent/empty/malformed/unrecognized/length/missing/non-unique/untrusted controls; committed cmp-code-detc listing.")
S.save_status(st)
cp = S.write_checkpoint(8, st, [
    "builders/ts_runs.py (cmp-* family incl. cmp-budget)", "tools/build_cmp.py", "runs/cmp-family.summary.json", "runs/cmp-*.store.json", "runs/cmp-*.replay.json",
    "ref/detector_compat.py", "ref/run_termination.py", "tools/phase8_compare.py", "tools/phase8_envelopes.py", "tools/run_termination_vectors.py",
    "vectors/baseline-audit.json", "vectors/comparison-absence-knowledge.json", "vectors/comparison-missing.json", "vectors/comparison-evidence-changed.json",
    "vectors/comparison-empty-result.json", "vectors/comparison-scope-policy-only.json", "vectors/baseline-e0-e3.json", "vectors/pivot-only-fingerprints.json",
    "vectors/test-prep-repair-authorization.json", "envelopes/purge-replay-output-failure.json", "envelopes/public-termination.json", "vectors/run-termination.json",
    "vectors/host-captured-vs-candidate.json", "vectors/empty-partial-unavailable-missing.json", "vectors/detector-compat-file.json",
    "notes/08-subsystem-owners.md", "logs/s42-fin-p4to9.4.phase8_compare.log", "logs/s42-fin-p4to9.5.phase8_envelopes.log",
    "logs/s42-fin-p4to9.8.run_termination_vectors.log", "logs/s42-fin-build.3.build_cmp.log",
    "preserved/pre-s42/logs/s42-pre-p4to9.4.phase8_compare.log (unchanged helpers)", "preserved/pre-s42/logs/s42-pre-p4to9.5.phase8_envelopes.log (unchanged helpers)"],
    HC.for_phase(8),
    "Phase 8: cmp-* Runs (including cmp-budget) rebuilt in runtime source42.v1 on the source42 kit and re-closed in source42.v2 "
    "(logs/s42v2-fin2.2.from_scratch.log); phase8_compare, phase8_envelopes and "
    "run_termination_vectors re-executed there after the source42 corrections; Runs closed with owner admission, the independent retained-closure "
    "walk and fresh-process replay (runs/cmp-family.summary.json). Problems: " + json.dumps(problems))
print(json.dumps({"unexecuted": cp["requirementIdsUnexecuted"], "failed": cp["requirementIdsFailed"], "problems": problems}, indent=1))
