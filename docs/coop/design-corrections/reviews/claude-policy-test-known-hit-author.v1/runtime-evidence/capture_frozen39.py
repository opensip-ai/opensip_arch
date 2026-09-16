"""Verify the formal frozen39 manifest and ALL its members, then take a disposable regular-file capture of those bytes.

1. The manifest file must hash to the expected sha256.
2. Every listed member under the snapshot root must exist as a regular file (no symlink) with the listed sha256 and
   bytes; the snapshot must contain no unlisted file (excluding __pycache__ directories, reported separately).
3. Each verified member's bytes are written to DEST as a fresh regular file (open 'xb'; link count checked) and re-hashed.
4. The snapshot is re-verified after copying (drift check).
Writes OUT_JSON and exits non-zero on any fault. Usage: capture_frozen39.py DEST OUT_JSON
"""
import hashlib
import json
import os
import sys
from pathlib import Path

MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json")
EXPECTED = "f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009"
dest, out_json = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
if dest.exists():
    raise SystemExit("destination exists: %s" % dest)
raw = MANIFEST.read_bytes()
manifest_sha = hashlib.sha256(raw).hexdigest()
if manifest_sha != EXPECTED:
    raise SystemExit("manifest sha mismatch: " + manifest_sha)
manifest = json.loads(raw)
root = Path(manifest["snapshotRoot"])
members = manifest["files"]


def verify():
    faults = []
    for f in members:
        p = root / f["path"]
        if p.is_symlink() or not p.is_file():
            faults.append({"path": f["path"], "fault": "missing-or-not-regular"})
            continue
        data = p.read_bytes()
        if hashlib.sha256(data).hexdigest() != f["sha256"] or len(data) != f["bytes"]:
            faults.append({"path": f["path"], "fault": "digest-or-size"})
    listed = {f["path"] for f in members}
    unlisted, pycache = [], []
    for d, dirs, files in os.walk(root):
        for x in list(dirs):
            if x == "__pycache__":
                pycache.append(str((Path(d) / x).relative_to(root)))
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        for n in files:
            rel = (Path(d) / n).relative_to(root).as_posix()
            if rel not in listed:
                unlisted.append(rel)
    return faults, sorted(unlisted), sorted(pycache)


before_faults, before_unlisted, before_pycache = verify()
copy_faults = []
if not before_faults:
    for f in members:
        data = (root / f["path"]).read_bytes()
        target = dest / f["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "xb") as fh:
            fh.write(data)
        written = target.read_bytes()
        if hashlib.sha256(written).hexdigest() != f["sha256"] or os.stat(target).st_nlink != 1:
            copy_faults.append(f["path"])
after_faults, after_unlisted, after_pycache = verify()
report = {
    "artifact": "policy-test-known-hit-author.frozen39-capture", "version": 1,
    "standing": "Disposable regular-file capture of verified frozen39 bytes for a bounded author correction; not a freeze, repin or successor.",
    "manifest": str(MANIFEST), "manifestSha256": manifest_sha, "snapshotRoot": str(root), "capture": str(dest),
    "memberCount": len(members), "totalBytes": sum(f["bytes"] for f in members),
    "verifyBefore": {"faults": before_faults, "unlisted": before_unlisted, "pycacheDirs": before_pycache},
    "copyFaults": copy_faults,
    "verifyAfter": {"faults": after_faults, "unlisted": after_unlisted, "pycacheDirs": after_pycache},
}
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps({k: report[k] for k in ("manifestSha256", "memberCount", "totalBytes", "copyFaults")}
                 | {"faultsBefore": len(before_faults), "faultsAfter": len(after_faults), "unlistedBefore": before_unlisted[:20],
                    "pycacheBefore": before_pycache[:20]}, indent=1))
raise SystemExit(1 if before_faults or after_faults or copy_faults or before_unlisted or after_unlisted else 0)
