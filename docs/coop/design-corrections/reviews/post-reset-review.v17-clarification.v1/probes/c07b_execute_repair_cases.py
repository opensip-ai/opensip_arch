#!/usr/bin/env python
"""Point 7, decisive question: is any positive repair case ACTUALLY masked today?

I replicate the checker's repair loop exactly, but instead of the checker's
comparison I record, per case, whether repair_preview raised at all and with
what detail. That tells us whether the 1787 figure is inflated by a silently
masked case, or whether the harness weakness is latent.

No source byte is modified. repair_preview is a pure function over in-memory
inputs; the interpreter runs with -B so no bytecode is written.
"""
import importlib.util
import json
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
C = CASES["constants"]
RS = CASES["repairScenario"]


def tree_bytes(t):
    return {k: v.encode() for k, v in t.items()}


rows = []
for case in RS["cases"]:
    cid = case["id"]
    tree = tree_bytes(RS["tree"])
    run = dict(RS["run"])
    if case.get("runAvailability"):
        run["availability"] = case["runAvailability"]
    trust = {C["PROD"]: "revoked" if case.get("revokeRecipe") else "admitted"}
    if case.get("trustAbsent"):
        trust = {}
    if case.get("runOverride"):
        run.update(case["runOverride"])
    for field in ["closedWorld", "evidenceOrigin"]:
        if field in case:
            run[field] = case[field]
    edits = [dict(e, postimage=e["postimage"].encode())
             if e.get("postimage") is not None else dict(e)
             for e in RS["edits"]] + ([case["extraEdit"]] if case.get("extraEdit") else [])
    scope = list(RS["permittedScope"])
    if case.get("mutateTreeBeforePreview"):
        tree.update(tree_bytes(case["mutateTreeBeforePreview"]))
    run["snapshotId"] = M.tree_snapshot_id(C["PRJ"], tree_bytes(RS["tree"]))
    requirements = case.get("evidenceRequirements", RS["evidenceRequirements"])

    expects_refusal = "refusal" in case.get("expect", {})
    expected_detail = case.get("expect", {}).get("refusal")
    raised = None
    detail = "<none-raised>"
    remedy = None
    try:
        M.repair_preview(C["PRJ"], tree, run, RS["recipe"], RS["targets"], edits,
                         requirements, scope, trust,
                         ephemeral=case.get("ephemeral", False))
        raised = False
    except M.Refusal as r:
        raised = True
        detail = r.detail
        remedy = r.remedy
    except Exception as e:
        raised = "OTHER:" + type(e).__name__

    harness_verdict = None
    masked = False
    if raised is True:
        harness_verdict = (expected_detail == detail)
        # MASKED == the harness passes and continues, but the case expected success
        masked = (harness_verdict is True) and (not expects_refusal)
    rows.append({
        "id": cid,
        "expectsRefusal": expects_refusal,
        "expectedDetail": expected_detail,
        "raised": raised,
        "actualDetail": detail,
        "remedyHead": (remedy or "")[:90] if remedy else None,
        "harnessWouldReportPass": harness_verdict,
        "silentlyMasked": masked,
    })

positives = [r for r in rows if not r["expectsRefusal"]]
negatives = [r for r in rows if r["expectsRefusal"]]
rep = {
    "probe": "c07b-execute-repair-cases",
    "caseCount": len(rows),
    "positiveCases": len(positives),
    "negativeCases": len(negatives),
    "rows": rows,
    "positivesThatRaised": [r for r in positives if r["raised"] is True],
    "positivesSilentlyMasked": [r for r in rows if r["silentlyMasked"]],
    "negativesRaisingDetailFree": [
        r for r in negatives if r["raised"] is True and r["actualDetail"] is None],
    "anyPositiveMaskedToday": any(r["silentlyMasked"] for r in rows),
    "allNegativesRaised": all(r["raised"] is True for r in negatives),
    "allPositivesCompletedWithoutRefusal":
        all(r["raised"] is False for r in positives),
}
with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

print("repair cases executed        :", rep["caseCount"])
print("  positive (expect success)  :", rep["positiveCases"])
print("  negative (expect refusal)  :", rep["negativeCases"])
print()
print("positives that raised at all :", len(rep["positivesThatRaised"]))
print("positives SILENTLY MASKED    :", len(rep["positivesSilentlyMasked"]))
print("all positives completed clean:", rep["allPositivesCompletedWithoutRefusal"])
print("all negatives raised         :", rep["allNegativesRaised"])
print()
print("negatives whose refusal is DETAIL-FREE (rely on the null comparison):")
for r in rep["negativesRaisingDetailFree"]:
    print("   %-64s expected=%s" % (r["id"][:64], r["expectedDetail"]))
print()
if rep["positivesThatRaised"]:
    print("!! POSITIVE CASES THAT RAISED:")
    for r in rep["positivesThatRaised"]:
        print("   ", json.dumps(r)[:300])
