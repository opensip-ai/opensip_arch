"""Hash index of this runtime's author outputs and of every changed work-copy file.

usage: hash_index.py <runtime-root>
Excludes launcher/process/event files and the scratch trees.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

rt = Path(sys.argv[1])
rows = []
for top in ("tools", "receipts", "delta", "review.md", "review.json"):
    base = rt / top
    if not base.exists():
        continue
    paths = [base] if base.is_file() else sorted(Path(d) / f for d, _, fs in os.walk(base) for f in fs)
    for p in paths:
        b = p.read_bytes()
        rows.append({"path": str(p.relative_to(rt)), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
changed = json.loads((rt / "delta" / "cumulative-vs-frozen43" / "files.json").read_text(encoding="utf-8"))["changed"]
for c in changed:
    if c["status"] == "removed":
        continue
    p = rt / "work" / "candidate" / c["path"]
    b = p.read_bytes()
    rows.append({"path": str(p.relative_to(rt)), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
                 "matchesCumulativeDelta": hashlib.sha256(b).hexdigest() == c["currentSha256"]})
(rt / "hash-index.json").write_text(json.dumps({"runtime": str(rt), "files": rows}, indent=1) + "\n", encoding="utf-8")
print(len(rows), all(r.get("matchesCumulativeDelta", True) for r in rows))
