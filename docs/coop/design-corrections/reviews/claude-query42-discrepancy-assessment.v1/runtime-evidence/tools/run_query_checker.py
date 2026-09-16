"""Run one runtime tree's workflows/check-query-projection.v3.py (the owning query checker only).

usage: run_query_checker.py <tree-root> <label>
Writes receipts/check-query-<label>.json (--report), .stdout.txt, .summary.json.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

RT = Path("/private/tmp/opensip-design-corrections/claude-query42-discrepancy-assessment.v1")
tree, label = Path(sys.argv[1]), sys.argv[2]
if not str(tree.resolve()).startswith(str(RT.resolve())):
    raise SystemExit("refusing a tree outside this runtime")
checker = tree / "docs/coop/design-corrections/workflows/check-query-projection.v3.py"
report = RT / "receipts" / ("check-query-" + label + ".json")
if report.exists():
    raise SystemExit("refusing to overwrite " + str(report))
proc = subprocess.run(["/tmp/opensip-architecture-review-env/bin/python", "-I", "-B", str(checker), "--report", str(report)],
                      capture_output=True, text=True, timeout=3000)
(RT / "receipts" / ("check-query-" + label + ".stdout.txt")).write_text(proc.stdout[-20000:] + "\n--- stderr ---\n" + proc.stderr[-20000:])
data = json.loads(report.read_text()) if report.exists() else {}
summary = {"label": label, "tree": str(tree), "exitCode": proc.returncode,
           "reportSha256": hashlib.sha256(report.read_bytes()).hexdigest() if report.exists() else None,
           "count": data.get("count"), "failedCount": data.get("failedCount"),
           "failed": [{"id": c["id"], "detail": c["detail"]} for c in data.get("failed", [])],
           "checks": {c["id"]: c["ok"] for c in data.get("checks", [])},
           "checkerSha256": hashlib.sha256(checker.read_bytes()).hexdigest(),
           "modelSha256": hashlib.sha256((checker.parent / "query_projection_model.v3.py").read_bytes()).hexdigest()}
(RT / "receipts" / ("check-query-" + label + ".summary.json")).write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({k: summary[k] for k in ("label", "exitCode", "count", "failedCount", "failed", "reportSha256")}, indent=2))
if proc.returncode not in (0, 1):
    print("stderr tail:", proc.stderr[-2000:])
