"""Reviewer probe (review-04): does the subject D9 aggregate count a recorded required *skipped* step's termination, which the pinned owner
reference model workflows_model.v1.py excludes (outcome != 'skipped')?"""
import importlib.util, json, sys
from pathlib import Path
SUBJ = Path("/tmp/opensip-implementation/m1-report-projection-subject-04")
spec = importlib.util.spec_from_file_location("rm", SUBJ / "report_model.py"); rm = importlib.util.module_from_spec(spec); spec.loader.exec_module(rm)
run = "run3:" + "a" * 64
cases = {
 "skipped-step-carrying-request-rejected": [
   {"stepId": 0, "kind": "analysis", "requirement": "required", "recorded": True, "outcome": "completed", "termination": {"class": "success"}, "analysisRunId": run},
   {"stepId": 1, "kind": "query", "requirement": "required", "recorded": True, "outcome": "skipped", "skipReason": "dependency-not-completed",
    "termination": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"}}],
 "skipped-step-carrying-indeterminate": [
   {"stepId": 0, "kind": "analysis", "requirement": "required", "recorded": True, "outcome": "completed", "termination": {"class": "success"}, "analysisRunId": run},
   {"stepId": 1, "kind": "query", "requirement": "required", "recorded": True, "outcome": "skipped", "skipReason": "dependency-not-completed",
    "termination": {"class": "indeterminate", "reasonCodes": ["QUERY.COMPLETENESS_UNMET"]}}],
}
out = {}
for name, steps in cases.items():
    try:
        subject = rm.invocation_aggregate(steps, {"requested": False, "signal": "SIGINT", "phase": "none"})
    except Exception as exc:
        subject = type(exc).__name__ + ": " + str(exc)
    required = [s for s in steps if s["requirement"] == "required" and s["outcome"] != "skipped"]
    order = ["operational-failed", "request-rejected", "policy-failed", "indeterminate", "success"]
    classes = [s["termination"]["class"] for s in required]
    pick = next((c for c in order if c in classes), "success")
    matching = [s["termination"] for s in required if s["termination"]["class"] == pick]
    owner_like = next((t for t in matching if t.get("domainDetail")), matching[0] if matching else {"class": "success"})
    out[name] = {"subjectAggregate": subject, "ownerReferenceModelRuleAggregate": owner_like, "diverges": subject != owner_like}
print(json.dumps(out, indent=1))
