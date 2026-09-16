"""Run one tree's check-execution-inputs.v1.py (the owning checker only) with stdout captured to a file.

usage: run_checker.py <tree-root> <label>
Writes receipts/checker-<label>.json (the checker's own --receipt), receipts/checker-<label>.stdout.txt
and receipts/checker-<label>.summary.json (exit code, mismatches, case results, owned hashes).
"""
import contextlib
import hashlib
import json
import runpy
import sys
import time
from pathlib import Path

RT = Path("/private/tmp/opensip-design-corrections/claude-view-attribution-assessment.v1")
tree, label = Path(sys.argv[1]), sys.argv[2]
checker = tree / "docs/coop/design-corrections/foundation/check-execution-inputs.v1.py"
if not str(tree.resolve()).startswith(str(RT.resolve())):
    raise SystemExit("refusing to run a checker outside this runtime: " + str(tree))
receipt = RT / "receipts" / ("checker-" + label + ".json")
stdout_path = RT / "receipts" / ("checker-" + label + ".stdout.txt")
if receipt.exists() or stdout_path.exists():
    raise SystemExit("refusing to overwrite an existing receipt for label " + label)
receipt.parent.mkdir(parents=True, exist_ok=True)
t0 = time.time()
code = None
with open(stdout_path, "w") as out, contextlib.redirect_stdout(out):
    sys.argv = [str(checker), "--receipt", str(receipt), "--hashes", str(RT / "receipts" / ("checker-" + label + ".hashes.json"))]
    try:
        runpy.run_path(str(checker), run_name="__main__")
    except SystemExit as exc:
        code = exc.code
elapsed = time.time() - t0
report = json.loads(receipt.read_text())
summary = {
    "tree": str(tree), "label": label, "exitCode": code, "seconds": round(elapsed, 1),
    "receiptSha256": hashlib.sha256(receipt.read_bytes()).hexdigest(),
    "mismatches": report["mismatches"],
    "caseResults": {c["case"]: [c["result"], c.get("refusals")] for c in report["cases"]},
    "caseCount": len(report["cases"]), "oracleFailures": report["oracles"],
    "ownedHashes": report["ownedHashes"],
}
(RT / "receipts" / ("checker-" + label + ".summary.json")).write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({k: summary[k] for k in ("label", "exitCode", "seconds", "caseCount", "mismatches", "receiptSha256")}, indent=2))
