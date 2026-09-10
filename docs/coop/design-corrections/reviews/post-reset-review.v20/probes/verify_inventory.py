"""Verify every declared hash/length in the frozen subject manifest against the snapshot.

Independent re-verification: does not trust the manifest's own fileCount/totalBytes.
Reports extras present on disk but undeclared, and declared-but-missing.
"""
import hashlib
import json
import os
import sys

MANIFEST = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "run"

man = json.load(open(MANIFEST))
root = man["snapshotRoot"]
files = man["files"]

declared = {}
for f in files:
    declared[f["path"]] = f

mismatch_hash = []
mismatch_len = []
missing = []
ok = 0
total_bytes = 0

for path, rec in declared.items():
    full = os.path.join(root, path) if not path.startswith("/") else path
    if not os.path.isfile(full):
        missing.append(path)
        continue
    data = open(full, "rb").read()
    h = hashlib.sha256(data).hexdigest()
    n = len(data)
    total_bytes += n
    exp_h = rec.get("sha256")
    exp_n = rec.get("bytes", rec.get("length"))
    if exp_h is not None and h != exp_h:
        mismatch_hash.append({"path": path, "declared": exp_h, "actual": h})
    if exp_n is not None and n != exp_n:
        mismatch_len.append({"path": path, "declared": exp_n, "actual": n})
    if (exp_h is None or h == exp_h) and (exp_n is None or n == exp_n):
        ok += 1

# extras on disk not declared
on_disk = set()
for dirpath, _dirnames, filenames in os.walk(root):
    for fn in filenames:
        p = os.path.relpath(os.path.join(dirpath, fn), root)
        on_disk.add(p)
extras = sorted(on_disk - set(declared.keys()))

out = {
    "label": LABEL,
    "manifest": MANIFEST,
    "manifestSha256": hashlib.sha256(open(MANIFEST, "rb").read()).hexdigest(),
    "declaredFileCount": man.get("fileCount"),
    "declaredTotalBytes": man.get("totalBytes"),
    "declaredEntries": len(declared),
    "onDiskCount": len(on_disk),
    "verifiedOk": ok,
    "recomputedTotalBytes": total_bytes,
    "hashMismatches": mismatch_hash[:50],
    "hashMismatchCount": len(mismatch_hash),
    "lengthMismatches": mismatch_len[:50],
    "lengthMismatchCount": len(mismatch_len),
    "missingCount": len(missing),
    "missing": missing[:50],
    "undeclaredExtrasCount": len(extras),
    "undeclaredExtras": extras[:50],
}
print(json.dumps(out, indent=2))
