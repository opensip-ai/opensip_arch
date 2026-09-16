"""Hash index of this runtime's author outputs (tools, receipts, delta, review) and changed work-copy files.

usage: hash_index.py <runtime-root>
Excludes launcher/process/event files, the two scratch trees and the unchanged bulk of the work copy.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

rt = Path(sys.argv[1])
rows = []
for top in ("tools", "receipts", "delta-final", "delta", "review.md", "review.json"):
    base = rt / top
    paths = [base] if base.is_file() else sorted(Path(d) / f for d, _, fs in os.walk(base) for f in fs) if base.exists() else []
    for p in paths:
        b = p.read_bytes()
        rows.append({"path": str(p.relative_to(rt)), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
changed = json.loads((rt / "delta-final" / "files.json").read_text(encoding="utf-8"))["changed"]
for c in changed:
    p = rt / "work" / "candidate" / c["path"]
    b = p.read_bytes()
    rows.append({"path": str(p.relative_to(rt)), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
                 "matchesDeltaAfter": hashlib.sha256(b).hexdigest() == c["afterSha256"]})
(rt / "hash-index.json").write_text(json.dumps({"runtime": str(rt), "files": rows}, indent=1) + "\n", encoding="utf-8")
print(len(rows), all(r.get("matchesDeltaAfter", True) for r in rows))
