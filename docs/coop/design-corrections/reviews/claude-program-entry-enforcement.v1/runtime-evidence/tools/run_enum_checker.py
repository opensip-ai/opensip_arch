"""Run one runtime tree's check-enumeration.v1.py (the owning enumeration checker only).

usage: run_enum_checker.py <tree-root> <label>
Writes receipts/check-enumeration-<label>.json (--receipt), .hashes.json, .stdout.txt, .summary.json.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

RT = Path("/private/tmp/opensip-design-corrections/claude-program-entry-enforcement.v1")
tree, label = Path(sys.argv[1]), sys.argv[2]
if not str(tree.resolve()).startswith(str(RT.resolve())):
    raise SystemExit("refusing a tree outside this runtime")
checker = tree / "docs/coop/design-corrections/foundation/check-enumeration.v1.py"
receipt = RT / "receipts" / ("check-enumeration-" + label + ".json")
hashes = RT / "receipts" / ("check-enumeration-" + label + ".hashes.json")
if receipt.exists():
    raise SystemExit("refusing to overwrite " + str(receipt))
proc = subprocess.run(["/tmp/opensip-architecture-review-env/bin/python", "-I", "-B", str(checker),
                       "--receipt", str(receipt), "--hashes", str(hashes)], capture_output=True, text=True)
(RT / "receipts" / ("check-enumeration-" + label + ".stdout.txt")).write_text(proc.stdout + "\n--- stderr ---\n" + proc.stderr)
report = json.loads(receipt.read_text())
summary = {"label": label, "tree": str(tree), "exitCode": proc.returncode,
           "receiptSha256": hashlib.sha256(receipt.read_bytes()).hexdigest(),
           "caseCount": len(report["cases"]), "mismatches": report["mismatches"],
           "caseResults": {c["case"]: [c["result"], c["refusals"]] for c in report["cases"]},
           "ownedHashes": report["ownedHashes"]}
(RT / "receipts" / ("check-enumeration-" + label + ".summary.json")).write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({k: summary[k] for k in ("label", "exitCode", "caseCount", "mismatches", "receiptSha256")}, indent=2))
if proc.stderr.strip():
    print("stderr tail:", proc.stderr[-1500:])
