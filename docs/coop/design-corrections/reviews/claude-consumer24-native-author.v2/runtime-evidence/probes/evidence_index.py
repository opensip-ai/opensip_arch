"""Index every receipt of this runtime (all attempts, failed ones included) for the review. Stdout only.

For each receipts/<label>/: argv, cwd, exit, seconds, stdout/stderr SHA-256. A label with a numeric suffix is a
later attempt of the same label; nothing is dropped.
Usage: evidence_index.py
"""
import json
from pathlib import Path

here = Path(__file__).resolve().parent.parent / "receipts"
rows = []
for d in sorted(p for p in here.iterdir() if p.is_dir()):
    command = json.loads((d / "command.json").read_text()) if (d / "command.json").exists() else {}
    digests = json.loads((d / "digests.json").read_text()) if (d / "digests.json").exists() else {}
    rows.append({"label": d.name, "argv": command.get("argv"), "cwd": command.get("cwd"),
                 "exit": int((d / "exit.txt").read_text()) if (d / "exit.txt").exists() else None,
                 "seconds": digests.get("seconds"), "stdoutSha256": digests.get("stdoutSha256"),
                 "stderrSha256": digests.get("stderrSha256")})
print(json.dumps({"receipts": len(rows), "nonZeroExit": [r["label"] for r in rows if r["exit"] not in (0,)],
                  "rows": rows}, indent=1))
