"""File-level comparison of a rebuilt package with package15, plus text diffs of every non-export file that changed.

Classifies each path: unchanged, modified, added, removed, and `movedToHistorical` (a package15 path whose exact bytes
now live under historical-source38-before-native-v2/). Export stores (*.store.json) are compared by digest only; their
unified diffs are not emitted. Writes OUTDIR/package-vs-package15.json and OUTDIR/package-vs-package15.diff.
Usage: package_diff.py PACKAGE15 NEWPACKAGE OUTDIR
"""
import difflib
import hashlib
import json
import os
import sys
from pathlib import Path

old, new, outdir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
outdir.mkdir(parents=True, exist_ok=True)
HIST = "historical-source38-before-native-v2/"


def walk(root):
    rows = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        for name in files:
            p = Path(d) / name
            rows[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return rows


a, b = walk(old), walk(new)
rows, parts = [], []
for rel in sorted(set(a) | set(b), key=lambda s: s.encode()):
    if rel in a and rel in b:
        status = "unchanged" if a[rel] == b[rel] else "modified"
    elif rel in a:
        status = "movedToHistorical" if b.get(HIST + rel) == a[rel] else "removed"
    else:
        status = "added"
        if rel.startswith(HIST) and a.get(rel[len(HIST):]) == b[rel]:
            status = "historicalCopyOfPackage15"
    if status == "unchanged":
        continue
    rows.append({"path": rel, "status": status, "package15Sha256": a.get(rel), "sha256": b.get(rel)})
    if status in ("modified", "added") and not rel.endswith(".store.json") and not rel.startswith(HIST):
        try:
            before = (old / rel).read_text() if rel in a else ""
            after = (new / rel).read_text()
        except UnicodeDecodeError:
            continue
        parts.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                          fromfile=("package15/" + rel) if rel in a else "/dev/null", tofile="package/" + rel, n=3))
text = "".join(parts)
(outdir / "package-vs-package15.diff").write_text(text)
summary = {}
for r in rows:
    summary[r["status"]] = summary.get(r["status"], 0) + 1
report = {"package15": str(old), "package": str(new), "counts": summary, "unchangedCount": len(set(a) & set(b)) - summary.get("modified", 0),
          "files": rows, "diffSha256": hashlib.sha256(text.encode()).hexdigest()}
(outdir / "package-vs-package15.json").write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps({"counts": summary, "unchanged": report["unchangedCount"], "diffSha256": report["diffSha256"],
                  "modifiedOrAdded": [r["path"] for r in rows if r["status"] in ("modified", "added")]}, indent=1))
