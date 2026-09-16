"""Incremental changed-file manifest and unified diff: v1 work source (frozen, root-captured) -> this runtime's source.

Walks both trees (excluding __pycache__). Writes OUTDIR/v1-to-v2.changed-files.json and OUTDIR/v1-to-v2.diff.
Usage: diff_incremental.py OUTDIR
"""
import difflib
import hashlib
import json
import os
import sys
from pathlib import Path

V1 = Path("/private/tmp/opensip-design-corrections/claude-consumer24-native-author.v1/source")
V2 = Path(__file__).resolve().parent.parent / "source"
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)


def walk(root):
    found = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        for name in files:
            rel = os.path.relpath(os.path.join(d, name), root)
            found[rel] = hashlib.sha256((root / rel).read_bytes()).hexdigest()
    return found


a, b = walk(V1), walk(V2)
rows, parts = [], []
for rel in sorted(set(a) | set(b), key=lambda s: s.encode("utf-8")):
    if a.get(rel) == b.get(rel):
        continue
    status = "added" if rel not in a else ("removed" if rel not in b else "modified")
    rows.append({"path": rel, "status": status, "v1Sha256": a.get(rel), "v2Sha256": b.get(rel)})
    before = (V1 / rel).read_text() if rel in a else ""
    after = (V2 / rel).read_text() if rel in b else ""
    parts.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                      fromfile="v1/" + rel if rel in a else "/dev/null",
                                      tofile="v2/" + rel if rel in b else "/dev/null", n=3))
    if parts and not parts[-1].endswith("\n"):
        parts[-1] += "\n\\ No newline at end of file\n"
text = "".join(parts)
(out / "v1-to-v2.diff").write_text(text)
report = {"artifact": "consumer24-native-author.v1-to-v2", "version": 1, "v1Root": str(V1), "v2Root": str(V2),
          "v1Files": len(a), "v2Files": len(b), "changed": rows,
          "diffSha256": hashlib.sha256(text.encode()).hexdigest(), "diffBytes": len(text.encode())}
(out / "v1-to-v2.changed-files.json").write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps({"v1Files": len(a), "v2Files": len(b), "changedCount": len(rows),
                  "paths": [(r["status"], r["path"]) for r in rows], "diffSha256": report["diffSha256"]}, indent=1))
