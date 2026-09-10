#!/usr/bin/env python
"""Cross-check every count in validation-summary.v1.json against the report it
summarises, and against the artifact the count is about.

validation-summary.v1.json is itself one of the 36 files modified in v13, and it
is cited as reference evidence for this review, so its counts are in scope. No
reference command validates it -- nothing joins the summary to the artifacts it
describes -- so a stale value survives a full six-command PASS.
"""
import json
import sys
from pathlib import Path

HERE = Path(
    "/tmp/opensip-design-corrections/post-reset-review.v13/work/subject-copy"
    "/docs/coop/design-corrections")
V12 = Path("/tmp/opensip-design-corrections/candidate-subject.v12"
           "/docs/coop/design-corrections")


def load(p):
    return json.loads(p.read_text())


def main():
    s = load(HERE / "validation-summary.v1.json")
    matrix = load(HERE / "native/native-capability-matrix.v2.json")
    ident = load(HERE / "foundation/identity-report.json")
    wf = load(HERE / "workflows/workflows-report.v1.json")
    nat = load(HERE / "native/native-evidence-report.v2.json")
    integ = load(HERE / "integration-report.v1.json")
    sec = load(HERE / "security/security-lifecycle-report.v1.json")

    rows = [
        ("native.matrixCells", s["native"]["matrixCells"], len(matrix["cells"]),
         "native-capability-matrix.v2.json#/cells"),
        ("native.casesPassed", s["native"]["casesPassed"], nat["cases"]["total"],
         "native-evidence-report.v2.json#/total"),
        ("native.qualifiedCells", s["native"]["qualifiedCells"],
         nat["matrix"]["qualifiedCells"],
         "native-evidence-report.v2.json#/matrix/qualifiedCells"),
        ("native.matrixCells vs the report's own count",
         s["native"]["matrixCells"], nat["matrix"]["cells"],
         "native-evidence-report.v2.json#/matrix/cells"),
        ("foundation.identity", s["foundation"]["components"]["identity"],
         len(ident["checks"]), "identity-report.json#/checks"),
        ("workflows.checksPassed", s["workflows"]["checksPassed"], wf["passed"],
         "workflows-report.v1.json#/passed"),
        ("integration.checksPassed", s["integration"]["checksPassed"],
         integ["passed"], "integration-report.v1.json#/passed"),
        ("security.casesPassed", s["security"]["casesPassed"],
         sec["counts"]["pass"], "security-lifecycle-report.v1.json"),
        ("security.sweeps", s["security"]["invariantSweepsPassed"],
         len(sec["sweeps"]), "security-lifecycle-report.v1.json#/sweeps"),
    ]
    results = [{"field": f, "claimed": c, "actual": a, "source": src,
                "agrees": c == a} for f, c, a, src in rows]

    # Was the value correct in the predecessor? That distinguishes a value that
    # was never right from one that went stale when the artifact grew.
    prior = {}
    try:
        s12 = load(V12 / "validation-summary.v1.json")
        m12 = load(V12 / "native/native-capability-matrix.v2.json")
        prior = {"v12ClaimedMatrixCells": s12["native"]["matrixCells"],
                 "v12ActualMatrixCells": len(m12["cells"]),
                 "v12Agreed": s12["native"]["matrixCells"] == len(m12["cells"])}
    except Exception as exc:
        prior = {"error": str(exc)[:120]}

    stale = [r for r in results if not r["agrees"]]
    out = {
        "summaryStanding": s.get("standing"),
        "results": results,
        "staleCount": len(stale),
        "stale": stale,
        "predecessor": prior,
        "note": ("v12 recorded 60 against an actual 60. v13 grew the matrix to "
                 "66 (the syntax-only mode added by CB3-MUST-3) and the summary "
                 "was modified in v13 but this count was not updated. Nothing "
                 "joins the summary to the matrix, so all six reference "
                 "commands still PASS."),
    }
    print(json.dumps(out, indent=2))
    return 0 if not stale else 1


if __name__ == "__main__":
    sys.exit(main())
