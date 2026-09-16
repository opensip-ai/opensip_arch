"""Policy-test route probe over a work/source copy (READ-ONLY; run with -I -B).

Records, for the given source: the historical workflow1 route (legacy workflows_model.v1.run_policy_test through the
projection owner's legacy module) on the retained PolicyTestSuiteV1, and the evaluator3 public route
(workflows_model.v3.run_admitted_policy_test) on that V1 suite and on the explicitly authored PolicyTestSuiteV2 fixture.
Used before the correction (fixture from --fixture) and after it, to pin the unchanged historical identity and to show
the route change. Usage: route_probe.py --source ROOT --fixture POLICY_TEST_CASES_V3_JSON --out OUT_JSON
"""
import argparse
import copy
import importlib.util
import json
import traceback
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--source", required=True, type=Path)
ap.add_argument("--fixture", required=True, type=Path)
ap.add_argument("--out", required=True, type=Path)
a = ap.parse_args()
W = a.source.resolve() / "docs/coop/design-corrections/workflows"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load("route_probe_projection3", W / "workflow_projection_model.v3.py")
WF3 = load("route_probe_workflows3", W / "workflows_model.v3.py")
canonical = WF3.canonical
RAW = canonical.parse((W / "workflow-cases.v1.json").read_bytes())
C = dict(RAW["constants"])  # the checker's _r2_sub constant derivations (check-workflow-projection.v3.py)
C["ARGV"] = WF3.raw_sha(canonical.canonical(["scripts/test.sh", "--ci"]))
C["ARGV2"] = WF3.raw_sha(canonical.canonical(["/usr/bin/bash", "-c", "rm -rf ."]))
C["TOOL0#bin/node"] = C["TOOL0"] + "#bin/node"
C["ARGV4"] = WF3.raw_sha(canonical.canonical(["node", "test.js"]))
C["ARGV3"] = WF3.raw_sha(canonical.canonical(["bin/node", "test.js"]))


def sub(o):
    if isinstance(o, str) and o.startswith("$"):
        if o[1:] in C:
            return C[o[1:]]
        if o[1:] in RAW["policyDocs"]:
            return sub(RAW["policyDocs"][o[1:]])
        raise KeyError(o)
    if isinstance(o, dict):
        return {sub(k) if isinstance(k, str) and k.startswith("$") else k: sub(v) for k, v in o.items()}
    if isinstance(o, list):
        return [sub(v) for v in o]
    return o


V1_SUITE = sub(RAW)["policySuite"]
V2_SUITE = canonical.parse(a.fixture.read_bytes())["currentSuite"]


def route(fn):
    try:
        res, refusal = fn()
        return {"outcome": "RETURNED", "resolverAccepted": res["resolverAccepted"], "policyTestResultId": res["policyTestResultId"],
                "suiteDigest": res["suiteDigest"], "candidatePolicyDigest": res["candidatePolicyDigest"], "summary": res["summary"],
                "resolverRefusal": None if refusal is None else [refusal.error_code, refusal.detail],
                "cases": {c["id"]: {k: c[k] for k in ("outcome", "observedVerdict", "findings", "indeterminateRules", "expectationOutcomes")} for c in res["results"]}}
    except Exception as exc:
        row = {"outcome": "REFUSED" if hasattr(exc, "error_code") else "EXCEPTION", "type": type(exc).__name__}
        if hasattr(exc, "error_code"):
            row.update(errorCode=exc.error_code, detail=exc.detail, remedy=exc.remedy, subject=exc.subject,
                       termination=exc.termination(), exitCode=WF3.exit_code(exc.termination()))
        else:
            row["trace"] = traceback.format_exc().splitlines()[-4:]
        return row


report = {
    "source": str(a.source.resolve()),
    "historicalWorkflow1Route_P.W.run_policy_test_V1": route(lambda: P.W.run_policy_test(copy.deepcopy(V1_SUITE))),
    "evaluator3Route_run_admitted_policy_test_V1": route(lambda: WF3.run_admitted_policy_test(copy.deepcopy(V1_SUITE))),
    "evaluator3Route_run_admitted_policy_test_V2": route(lambda: WF3.run_admitted_policy_test(copy.deepcopy(V2_SUITE))),
    "evaluator3_run_policy_test_isLegacyObject": WF3.run_policy_test is WF3._base.run_policy_test,
    "evaluator3_suiteRef": WF3.POLICY_TEST_SUITE_REF,
}
a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text(json.dumps(report, indent=1, default=str) + "\n")
print(json.dumps({k: (v if not isinstance(v, dict) else {x: v.get(x) for x in ("outcome", "policyTestResultId", "summary", "errorCode", "detail")}) for k, v in report.items()}, indent=1))
