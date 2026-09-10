#!/usr/bin/env python
"""Point 7: independent assessment of the repair-case harness comparison

    except M.Refusal as r:
        check(cid, case['expect'].get('refusal') == r.detail, r.detail)
        ...
        continue

`Refusal.detail` defaults to None, and `case['expect'].get('refusal')` is None
for a case that expects SUCCESS. So None == None passes, and `continue` then
skips every later assertion for that case.

Questions I answer with measurement, not agreement:
  Q1 Is a detail-free Refusal actually REACHABLE from repair_preview on these
     frozen bytes? (If not, the weakness is latent-only.)
  Q2 How many repair cases expect success (no `refusal` key) and would therefore
     be masked?
  Q3 Does the truth table actually mis-pass? (bounded discriminating control)
  Q4 Does the same pattern appear in the OTHER case harnesses?
  Q5 Is anything currently mis-reported - i.e. does the suite pass today because
     of this, or in spite of it?
"""
import ast
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

SUBJ = "/tmp/opensip-design-corrections/candidate-subject.v17"
DC = Path(SUBJ) / "docs/coop/design-corrections"
OUT = sys.argv[1]
sys.path.insert(0, str(DC / "foundation"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M = load("workflows_model", DC / "workflows/workflows_model.v1.py")
CASES = json.loads((DC / "workflows/workflow-cases.v1.json").read_bytes())
CHECKER_SRC = (DC / "workflows/check_workflows.v1.py").read_text()
MODEL_SRC = (DC / "workflows/workflows_model.v1.py").read_text()

rep = {"probe": "c07-harness-nullable-refusal"}

# ---------- Q1: detail-free Refusal raise sites, and reachability ----------
tree = ast.parse(MODEL_SRC)
raises = []
for node in ast.walk(tree):
    if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call):
        fn = node.exc.func
        name = getattr(fn, "id", None) or getattr(fn, "attr", None)
        if name != "Refusal":
            continue
        args = node.exc.args
        detail_is_none = False
        if len(args) < 2:
            detail_is_none = True          # detail defaults to None
        elif isinstance(args[1], ast.Constant) and args[1].value is None:
            detail_is_none = True
        kw = {k.arg: k.value for k in node.exc.keywords}
        if "detail" in kw and isinstance(kw["detail"], ast.Constant) \
                and kw["detail"].value is None:
            detail_is_none = True
        raises.append({
            "line": node.lineno,
            "errorCodeArg": (args[0].value if args and isinstance(args[0], ast.Constant)
                             else ast.dump(args[0])[:80] if args else None),
            "detailIsNone": detail_is_none,
            "source": MODEL_SRC.splitlines()[node.lineno - 1].strip()[:150],
        })
rep["totalRefusalRaiseSitesInModel"] = len(raises)
rep["detailFreeRaiseSites"] = [r for r in raises if r["detailIsNone"]]
rep["detailFreeRaiseSiteCount"] = len(rep["detailFreeRaiseSites"])

# which functions contain them, and is repair_preview among the callers?
func_of = {}
for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        for sub in ast.walk(node):
            if isinstance(sub, ast.Raise):
                func_of[sub.lineno] = node.name
for r in rep["detailFreeRaiseSites"]:
    r["inFunction"] = func_of.get(r["line"])
rep["functionsWithDetailFreeRefusals"] = sorted(
    {r["inFunction"] for r in rep["detailFreeRaiseSites"] if r["inFunction"]})

# repair_preview's direct callees, to judge reachability honestly
rp = next((n for n in ast.walk(tree)
           if isinstance(n, ast.FunctionDef) and n.name == "repair_preview"), None)
callees = set()
if rp:
    for sub in ast.walk(rp):
        if isinstance(sub, ast.Call):
            f = sub.func
            nm = getattr(f, "id", None) or getattr(f, "attr", None)
            if nm:
                callees.add(nm)
rep["repairPreviewDirectCallees"] = sorted(callees)
rep["detailFreeFunctionsDirectlyCalledByRepairPreview"] = sorted(
    set(rep["functionsWithDetailFreeRefusals"]) & callees)
# does repair_preview itself contain a detail-free raise?
rep["repairPreviewItselfHasDetailFreeRaise"] = "repair_preview" in \
    rep["functionsWithDetailFreeRefusals"]

# ---------- Q2: repair cases that expect success ----------
rcases = CASES["repairScenario"]["cases"]
expect_success = [c for c in rcases if "refusal" not in c.get("expect", {})]
expect_refusal = [c for c in rcases if "refusal" in c.get("expect", {})]
rep["repairCaseCount"] = len(rcases)
rep["repairCasesExpectingSuccess"] = len(expect_success)
rep["repairCasesExpectingRefusal"] = len(expect_refusal)
rep["repairCasesExpectingSuccessIds"] = [c["id"] for c in expect_success]
# of the refusal-expecting ones, how many name a NULL refusal deliberately?
rep["repairCasesWithExplicitNullRefusal"] = [
    c["id"] for c in expect_refusal if c["expect"]["refusal"] is None]
rep["repairCasesWithExpectRemedyContains"] = [
    c["id"] for c in rcases if "expectRemedyContains" in c]

# ---------- Q3: the truth table, exactly as the harness evaluates it ----------
def harness_predicate(expect, detail):
    return expect.get("refusal") == detail


truth = [
    {"case": "expects SUCCESS (no `refusal` key); refusal fires with detail=None",
     "expect": {}, "detail": None,
     "harnessSaysPass": harness_predicate({}, None),
     "shouldPass": False,
     "isMisPass": harness_predicate({}, None) is True},
    {"case": "expects SUCCESS; refusal fires WITH a detail",
     "expect": {}, "detail": "some.decision-key",
     "harnessSaysPass": harness_predicate({}, "some.decision-key"),
     "shouldPass": False,
     "isMisPass": harness_predicate({}, "some.decision-key") is True},
    {"case": "expects an explicit NULL refusal; refusal fires with detail=None",
     "expect": {"refusal": None}, "detail": None,
     "harnessSaysPass": harness_predicate({"refusal": None}, None),
     "shouldPass": True, "isMisPass": False},
    {"case": "expects a named refusal; that refusal fires",
     "expect": {"refusal": "k"}, "detail": "k",
     "harnessSaysPass": harness_predicate({"refusal": "k"}, "k"),
     "shouldPass": True, "isMisPass": False},
    {"case": "expects a named refusal; a DIFFERENT refusal fires",
     "expect": {"refusal": "k"}, "detail": "other",
     "harnessSaysPass": harness_predicate({"refusal": "k"}, "other"),
     "shouldPass": False, "isMisPass": False},
]
rep["truthTable"] = truth
rep["misPassingRows"] = [t for t in truth if t["isMisPass"]]
rep["theDefectIsReal"] = bool(rep["misPassingRows"])
rep["theDefectIsExactlyOneRow"] = len(rep["misPassingRows"]) == 1

# The second row shows the ordinary case is NOT masked: an expected-success case
# that refuses WITH a detail is correctly reported as a failure.
rep["expectedSuccessWithDetailIsCorrectlyCaught"] = (
    truth[1]["harnessSaysPass"] is False)

# ---------- Q3b: does `continue` skip later assertions? ----------
seg = CHECKER_SRC.split("for case in RS['cases']:")[1][:2000]
rep["harnessContinuesAfterTheComparison"] = bool(
    re.search(r"except M\.Refusal as r:.*?continue", seg, re.S))
rep["assertionsSkippedByContinue"] = [
    m for m in ("plan-schema", "applicable", "edits", "journal",
                "unmet-remedy-carries-the-native-cause")
    if m in CHECKER_SRC]
rep["expectRemedyContainsIsConditional"] = bool(
    re.search(r"if 'expectRemedyContains' in case:", CHECKER_SRC))

# ---------- Q4: the same pattern in the other harnesses ----------
pattern = re.compile(r"case\['expect'\]\.get\('refusal'\) == (?:r|x|exc)\.detail")
hits = []
for m in pattern.finditer(CHECKER_SRC):
    line = CHECKER_SRC[:m.start()].count("\n") + 1
    ctx = CHECKER_SRC.splitlines()[line - 1].strip()
    # is an errorCode/other conjunct present on the same line?
    guarded = "errorCode" in ctx or "error_code" in ctx
    hits.append({"line": line, "text": ctx[:170], "hasAdditionalConjunct": guarded})
rep["sameComparisonSites"] = hits
rep["sameComparisonSiteCount"] = len(hits)
rep["unguardedSites"] = [h for h in hits if not h["hasAdditionalConjunct"]]

# ---------- Q5: is anything mis-reported TODAY? ----------
# For every expect-success repair case, run repair_preview exactly as the harness
# does and record whether it refuses at all.
RS = CASES["repairScenario"]
C = CASES.get("constants", {})
observed = []
for c in expect_success:
    observed.append({"id": c["id"],
                     "note": "executed below via the checker's own report"})
# The authoritative answer is the executed report: if any positive case had
# silently refused, its later assertions would be absent from the report.
rep["executedReportEvidence"] = {
    "method": "The frozen workflows-report.v1.json lists every check id the "
              "harness emitted. If a positive repair case had been masked, its "
              "downstream ids (.plan-schema, .applicable, ...) would be ABSENT.",
}
try:
    rpt = json.loads((DC / "workflows/workflows-report.v1.json").read_bytes())
    ids = set()
    for k in ("checks", "passed", "results"):
        v = rpt.get(k)
        if isinstance(v, list):
            for x in v:
                if isinstance(x, dict) and "id" in x:
                    ids.add(x["id"])
    rep["executedReportEvidence"]["reportExposesPerCheckIds"] = bool(ids)
    rep["executedReportEvidence"]["reportKeys"] = sorted(rpt.keys())
    rep["executedReportEvidence"]["checkCount"] = rpt.get("checkCount")
    rep["executedReportEvidence"]["failed"] = rpt.get("failed")
    if ids:
        missing = []
        for c in expect_success:
            base = "repair." + c["id"]
            downstream = [i for i in ids if i.startswith(base + ".")]
            missing.append({"case": c["id"], "downstreamCheckIds": len(downstream)})
        rep["executedReportEvidence"]["perPositiveCase"] = missing
        rep["executedReportEvidence"]["positivesWithZeroDownstreamChecks"] = [
            m for m in missing if m["downstreamCheckIds"] == 0]
except Exception as e:
    rep["executedReportEvidence"]["error"] = type(e).__name__ + ": " + str(e)

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

print("Refusal raise sites in model      :", rep["totalRefusalRaiseSitesInModel"])
print("  of which detail-free            :", rep["detailFreeRaiseSiteCount"])
print("  functions containing them       :", rep["functionsWithDetailFreeRefusals"])
print("  repair_preview itself has one   :", rep["repairPreviewItselfHasDetailFreeRaise"])
print("  detail-free fns called directly :",
      rep["detailFreeFunctionsDirectlyCalledByRepairPreview"])
print()
print("repair cases                      :", rep["repairCaseCount"])
print("  expecting SUCCESS               :", rep["repairCasesExpectingSuccess"])
print("  expecting a refusal             :", rep["repairCasesExpectingRefusal"])
print("  with an explicit NULL refusal   :", rep["repairCasesWithExplicitNullRefusal"])
print()
print("TRUTH TABLE (harness predicate):")
for t in truth:
    flag = "  <-- MIS-PASS" if t["isMisPass"] else ""
    print("  pass=%-5s should=%-5s  %s%s" % (t["harnessSaysPass"], t["shouldPass"],
                                             t["case"], flag))
print()
print("defect is real                    :", rep["theDefectIsReal"])
print("exactly one mis-passing row       :", rep["theDefectIsExactlyOneRow"])
print("expected-success WITH detail is caught:",
      rep["expectedSuccessWithDetailIsCorrectlyCaught"])
print("continue skips later assertions   :", rep["harnessContinuesAfterTheComparison"])
print("expectRemedyContains is conditional:", rep["expectRemedyContainsIsConditional"])
print()
print("same comparison sites             :", rep["sameComparisonSiteCount"])
for h in hits:
    print("   line %-5d guarded=%-5s %s" % (h["line"], h["hasAdditionalConjunct"],
                                            h["text"][:110]))
print()
print("executed report evidence:", json.dumps(
    {k: v for k, v in rep["executedReportEvidence"].items()
     if k != "perPositiveCase"}, indent=1)[:800])
