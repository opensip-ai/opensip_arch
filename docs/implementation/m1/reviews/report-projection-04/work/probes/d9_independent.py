"""Reviewer-independent D9/cancellation reimplementation from workflows-and-surfaces.md section 1 (review-04), checked against the frozen
aggregateCases and deliveryGoldens; plus RP-OBL-C01 envelope probes on envelope4 (accepted metadata-v2) and envelope5."""
import copy, hashlib, json, sys
from pathlib import Path
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
SUBJ = Path("/tmp/opensip-implementation/m1-report-projection-subject-04")
fx = json.loads((SUBJ / "fixtures.json").read_bytes())
ORDER = ["operational-failed", "request-rejected", "policy-failed", "indeterminate", "success"]
EXIT = {"success": 0, "policy-failed": 1, "request-rejected": 2, "indeterminate": 3, "operational-failed": 4, "interrupted": 130}

class Invalid(Exception):
    pass

def d9(terms):
    rank = min(ORDER.index(t["class"]) for t in terms)
    tied = [t for t in terms if ORDER.index(t["class"]) == rank]
    return next((t for t in tied if "domainDetail" in t), tied[0])

def aggregate(steps, cancellation):
    req = [s for s in steps if s["requirement"] == "required"]
    rec = [s for s in req if s["recorded"]]
    cancelled = [s for s in rec if s["outcome"] == "cancelled" or s["termination"]["class"] == "interrupted"]
    phase = (cancellation or {}).get("phase", "none")
    if cancellation and cancellation["requested"] != (phase != "none"):
        raise Invalid("requested/phase")
    for s in rec:
        if (s["outcome"] == "cancelled") != (s["termination"]["class"] == "interrupted"):
            raise Invalid("cancelled outcome <-> interrupted termination")
    if phase == "before-settle":
        if all(s["recorded"] and s["outcome"] != "cancelled" for s in req):
            raise Invalid("before-settle but every required step settled")
        if any(s["termination"].get("signal") != cancellation["signal"] for s in cancelled):
            raise Invalid("signal mismatch")
        committed = [s["analysisRunId"] for s in rec if s.get("analysisRunId") and s["outcome"] == "completed"]
        agg = {"class": "interrupted", "signal": cancellation["signal"]}
        if committed:
            agg["runId"] = committed[-1]
        return agg, {"committedRuns": len(committed)}
    if cancelled:
        raise Invalid("interrupted/cancelled step without before-settle")
    if phase == "after-settle" and len(rec) != len(req):
        raise Invalid("after-settle with unsettled required step")
    return d9([s["termination"] for s in rec]), {}

out = {"aggregateCases": [], "deliveryGoldens": []}
for case in fx["aggregateCases"]:
    try:
        got, info = aggregate(case["steps"], case["cancellation"])
        res = "match" if "expect" in case and got == case["expect"] else ("MISMATCH", got, case.get("expect", case.get("refusal")))
    except Invalid as exc:
        res = "match-refusal" if "refusal" in case else ("MISMATCH-refused", str(exc))
    out["aggregateCases"].append((case["id"], res))

for row in fx["deliveryGoldens"]:
    prior = row["priorSteps"]
    steps = [dict(s) for s in prior]
    if row["renderAttempts"]:
        rs = row["renderStep"]
        steps.append({"kind": "render", "requirement": rs["requirement"], "recorded": rs.get("outcome") is not None, "outcome": rs.get("outcome"), "termination": rs.get("termination")})
    if row["cancellation"] and row["cancellation"]["phase"] == "before-settle":
        pass
    try:
        got, _ = aggregate([s for s in steps if s["recorded"] or s["requirement"] == "required"], row["cancellation"])
    except Invalid as exc:
        got = "refused: " + str(exc)
    checks = {
        "aggregateMatchesIndependent": got == row["aggregate"],
        "priorTerminationsRetained": row["priorStepTerminations"] == [s["termination"] for s in prior],
        "exitFromClass": row["exitCode"] == EXIT[row["aggregate"]["class"]],
        "envelopeTerminationIsAggregate": row["envelope"] is None or row["envelope"]["termination"] == row["aggregate"],
        "envelopeExit": row["envelope"] is None or row["envelope"]["exitCode"] == row["exitCode"],
    }
    out["deliveryGoldens"].append({"id": row["id"], "envelopeKind": (row["envelope"] or {}).get("kind"), "delivered": row["delivered"], **checks,
                                   **({"independent": got, "golden": row["aggregate"]} if not checks["aggregateMatchesIndependent"] else {})})
by = {}
for row in fx["deliveryGoldens"]:
    key = json.dumps([row["aggregate"], row["exitCode"], row["priorStepTerminations"], bool(row["delivered"]), row["renderAttempts"]], sort_keys=True)
    by.setdefault(row["scenario"], set()).add(key)
out["crossFormatIdentical"] = {k: len(v) == 1 for k, v in by.items()}

# audit two-analysis ambiguity for before-settle runId choice
audit_steps = [{"kind": "analysis", "requirement": "required", "recorded": True, "outcome": "completed", "termination": {"class": "success"}, "analysisRunId": "run3:" + "1" * 64},
               {"kind": "analysis", "requirement": "required", "recorded": True, "outcome": "completed", "termination": {"class": "success"}, "analysisRunId": "run3:" + "2" * 64},
               {"kind": "comparison", "requirement": "required", "recorded": True, "outcome": "cancelled", "termination": {"class": "interrupted", "signal": "SIGINT"}}]
sys.path.insert(0, str(SUBJ))
import importlib.util
spec = importlib.util.spec_from_file_location("rm_probe", SUBJ / "report_model.py")
rm = importlib.util.module_from_spec(spec); spec.loader.exec_module(rm)
try:
    model = rm.invocation_aggregate([dict(s, stepId=i) for i, s in enumerate(audit_steps)], {"requested": True, "signal": "SIGINT", "phase": "before-settle"})
except Exception as exc:
    model = type(exc).__name__ + ": " + str(exc)[:120]
out["auditTwoCommittedRunsBeforeSettle"] = {"subjectModel": model, "independentLastCommitted": aggregate(audit_steps, {"requested": True, "signal": "SIGINT", "phase": "before-settle"})[0],
                                           "ownerText": "workflows-and-surfaces.md:226-227 'a Run committed by an earlier step is named in the termination's runId' (does not select among several)"}

# RP-OBL-C01 envelope probes
def load_source(name, path):
    module = type(sys)(name); module.__file__ = str(path)
    exec(compile(Path(path).read_bytes(), str(path), "exec"), module.__dict__)
    return module
cm = load_source("cm", ARCH / "docs/implementation/m1/metadata-v2/check_metadata.py")
reference, registry, documents = cm.load(ARCH)
from referencing import Resource
from referencing.jsonschema import DRAFT202012
e5 = reference.parse((SUBJ / "owner/command-envelope.v5.schema.json").read_bytes())
registry = registry.with_resource(e5["$id"], Resource(contents={k: v for k, v in e5.items() if k != "$schema"}, specification=DRAFT202012))
e4 = documents["urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"]
template = copy.deepcopy(fx["bases"]["fit-after-commit-query-failure"]["envelope"])
def variant(major, errors, termination, kind="failure"):
    env = copy.deepcopy(template)
    env["schemaMajor"] = major
    env["kind"] = kind
    env["termination"] = termination
    env["exitCode"] = EXIT[termination["class"]]
    env["errors"] = errors
    return env
def valid(schema, env):
    return reference.ExactValidator(schema, registry=registry).is_valid(env)
forms = {
    "interrupted-no-run-errors-empty": ([], {"class": "interrupted", "signal": "SIGINT"}),
    "interrupted-no-run-errors-invented-detail": ([{"code": "evidence.purged", "remedy": "re-run"}], {"class": "interrupted", "signal": "SIGINT"}),
    "interrupted-no-run-errors-omitted": (None, {"class": "interrupted", "signal": "SIGINT"}),
    "control-request-rejected-with-detail": ([{"code": "QUERY.VIEW_UNKNOWN", "remedy": "x"}], {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"}),
}
c01 = {}
for name, (errors, term) in forms.items():
    row = {}
    for major, schema in ((4, e4), (5, e5)):
        env = variant(major, errors if errors is not None else [], term)
        if errors is None:
            env.pop("errors")
        env.pop("advisoryReport", None)
        row["envelope%d" % major] = valid(schema, env)
    c01[name] = row
codes = [c for c in json.loads((ARCH / "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json").read_bytes())["$defs"]["DomainDetailCode"]["enum"]]
c01["domainDetailCodesMentioningInterruptCancelSignal"] = [c for c in codes if any(t in c.lower() for t in ("interrupt", "cancel", "signal"))]
out["RP-OBL-C01"] = c01
Path(__file__).with_name("d9_independent.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1)[:7000])
