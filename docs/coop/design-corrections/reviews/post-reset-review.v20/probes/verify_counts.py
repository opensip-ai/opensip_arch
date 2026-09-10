"""Independently recount the reference results claimed in technical-review.v20.md.

The claim table is prose; this recomputes from the actual report JSON in the frozen
subject. Counts are finite calls/cases, not coverage qualification.
"""
import json
import os
import sys

ROOT = sys.argv[1]
DC = os.path.join(ROOT, "docs/coop/design-corrections")


def load(p):
    return json.load(open(os.path.join(DC, p)))


out = {}

# foundation: wrapper report embeds per-script stdout
f = load("foundation/validation-report.json")
comp = {}
for c in f.get("checks", []):
    try:
        s = json.loads(c["stdout"].strip().splitlines()[-1])
    except Exception:
        s = {}
    comp[c["script"]] = {
        "exitCode": c["exitCode"],
        "passed": s.get("passed"),
        "failed": s.get("failed"),
    }
out["foundation"] = {
    "sourcePinsValid": f.get("sourcePinsValid"),
    "sourceFileCount": f.get("sourceFileCount"),
    "passed": f.get("passed"),
    "components": comp,
    "componentPassSum": sum(
        v["passed"] for v in comp.values() if isinstance(v["passed"], int)
    ),
    "anyFailed": any(v.get("failed") for v in comp.values()),
}

sec = load("security/security-lifecycle-report.v1.json")
out["security"] = {
    k: sec.get(k)
    for k in ("casesPassed", "passed", "failed", "invariantSweepsPassed",
              "productQualification")
    if k in sec
}
out["securityKeys"] = list(sec.keys())

nat = load("native/native-evidence-report.v2.json")
out["native"] = {
    k: nat.get(k)
    for k in ("casesPassed", "passed", "failed", "matrixCells",
              "qualifiedCells", "productQualification")
    if k in nat
}
out["nativeKeys"] = list(nat.keys())

wf = load("workflows/workflows-validation-report.json")
out["workflowsKeys"] = list(wf.keys())
out["workflows"] = {
    k: wf.get(k)
    for k in ("checksPassed", "passed", "failed", "commands", "goldens",
              "productQualification")
    if k in wf
}

integ = load("integration-report.v1.json")
out["integrationKeys"] = list(integ.keys())
out["integration"] = {
    k: integ.get(k)
    for k in ("checksPassed", "passed", "failed", "productQualification")
    if k in integ
}

print(json.dumps(out, indent=2, default=str))
