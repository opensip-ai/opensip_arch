"""Capture a regular-file copy of the mutable successor source and record its custody.

1. Walks INPUT (excluding __pycache__) and hashes every file (pass 1).
2. Copies each file byte-for-byte into DEST (regular files; symlinks refused), hashing the bytes actually written.
3. Re-hashes INPUT (pass 2). If any input file changed between passes, or any copied file differs from pass 1,
   the capture refuses (exit 1) and DEST is left for inspection but marked failed.
4. Compares the captured tree with the pinned source38 manifest: unchanged / modified / added / missing, with hashes.
Writes OUT_JSON (custody) and prints a summary.
Usage: capture_source.py INPUT DEST OUT_JSON
"""
import hashlib
import json
import os
import sys
from pathlib import Path

SOURCE38 = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json")
SOURCE38_SHA = "2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5"
src, dest, out_json = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
if dest.exists():
    raise SystemExit("destination exists: %s" % dest)


def walk(root):
    rows = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x != "__pycache__")
        for name in sorted(files):
            p = Path(d) / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                raise SystemExit("symlink refused: %s" % rel)
            data = p.read_bytes()
            rows[rel] = (hashlib.sha256(data).hexdigest(), len(data))
    return rows


first = walk(src)
copy_faults = []
for rel, (digest, size) in first.items():
    target = dest / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    data = (src / rel).read_bytes()
    target.write_bytes(data)
    written = target.read_bytes()
    if hashlib.sha256(written).hexdigest() != digest or len(written) != size:
        copy_faults.append(rel)
second = walk(src)
drift = sorted(set(first) ^ set(second)) + sorted(r for r in set(first) & set(second) if first[r] != second[r])
raw38 = SOURCE38.read_bytes()
if hashlib.sha256(raw38).hexdigest() != SOURCE38_SHA:
    raise SystemExit("source38 manifest digest mismatch")
m38 = {f["path"]: f for f in json.loads(raw38)["files"]}
modified, added, missing = [], [], []
for rel, (digest, size) in sorted(first.items()):
    if rel not in m38:
        added.append({"path": rel, "sha256": digest, "bytes": size})
    elif m38[rel]["sha256"] != digest or m38[rel]["bytes"] != size:
        modified.append({"path": rel, "source38Sha256": m38[rel]["sha256"], "source38Bytes": m38[rel]["bytes"],
                         "sha256": digest, "bytes": size})
for rel in sorted(set(m38) - set(first)):
    missing.append({"path": rel, "source38Sha256": m38[rel]["sha256"]})
files = [{"path": rel, "sha256": d, "bytes": s} for rel, (d, s) in sorted(first.items(), key=lambda kv: kv[0].encode())]
manifest_bytes = json.dumps({"files": files}, sort_keys=True, separators=(",", ":")).encode()
report = {
    "artifact": "author-package-migration.captured-source", "version": 1,
    "standing": "Provisional capture of a MUTABLE integration tree for author-constructor evidence; not a frozen candidate.",
    "input": str(src), "capture": str(dest), "fileCount": len(first), "totalBytes": sum(s for _, s in first.values()),
    "copyFaults": copy_faults, "inputDriftDuringCapture": drift,
    "capturedFileListSha256": hashlib.sha256(manifest_bytes).hexdigest(),
    "source38": {"manifest": str(SOURCE38), "sha256": SOURCE38_SHA, "fileCount": len(m38),
                 "unchanged": len(first) - len(modified) - len(added), "modified": modified, "added": added,
                 "missing": missing},
    "files": files,
}
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps({k: report[k] for k in ("fileCount", "totalBytes", "copyFaults", "inputDriftDuringCapture",
                                         "capturedFileListSha256")}
                 | {"source38Modified": len(modified), "source38Added": len(added), "source38Missing": len(missing),
                    "modifiedPaths": [r["path"] for r in modified], "addedPaths": [r["path"] for r in added]},
                 indent=1))
raise SystemExit(1 if copy_faults or drift else 0)
