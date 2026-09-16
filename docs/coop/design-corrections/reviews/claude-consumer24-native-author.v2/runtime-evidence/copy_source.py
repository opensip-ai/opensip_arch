"""Regular-file working copy of frozen source38, verified against its pinned manifest.

Usage: copy_source.py copy DEST | verify-parent | diff DEST
  copy          verifies the frozen snapshot against the manifest, then copies it with shutil.copy2 (regular
                files, never hardlinks) to DEST and verifies the copy.
  verify-parent re-verifies the frozen snapshot (read-only) against the manifest.
  diff          lists every path of DEST that differs from, is missing from, or is extra to the manifest, with
                parent and current SHA-256 and byte counts.
Writes only DEST (copy) and stdout.
"""
import hashlib
import json
import os
import shutil
import sys

MANIFEST = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json"
EXPECTED = "2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5"
raw = open(MANIFEST, "rb").read()
if hashlib.sha256(raw).hexdigest() != EXPECTED:
    raise SystemExit("manifest hash mismatch")
M = json.loads(raw)
ROOT = M["snapshotRoot"]
ROWS = {f["path"]: f for f in M["files"]}


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def compare(root):
    changed, missing, extra, total = [], [], [], 0
    for rel, f in ROWS.items():
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            missing.append(rel)
            continue
        size = os.path.getsize(p)
        total += size
        digest = sha(p)
        if digest != f["sha256"] or size != f["bytes"]:
            changed.append({"path": rel, "parentSha256": f["sha256"], "parentBytes": f["bytes"], "sha256": digest, "bytes": size})
    for d, _, fs in os.walk(root):
        for fn in fs:
            full = os.path.join(d, fn)
            rel = os.path.relpath(full, root)
            if "__pycache__" in rel.split(os.sep):
                continue
            if rel not in ROWS:
                extra.append({"path": rel, "sha256": sha(full), "bytes": os.path.getsize(full)})
            elif os.path.islink(full) or os.stat(full).st_nlink > 1:
                changed.append({"path": rel, "linkOrHardlink": True})
    return {"root": root, "manifestSha256": EXPECTED, "files": len(ROWS), "bytesListed": total, "totalBytes": M["totalBytes"],
            "changed": changed, "missing": sorted(missing), "extra": sorted(extra, key=lambda r: r["path"]),
            "exact": not changed and not missing and not extra}


mode = sys.argv[1]
if mode == "copy":
    dest = sys.argv[2]
    parent = compare(ROOT)
    if not parent["exact"]:
        print(json.dumps({"parent": parent}, indent=1))
        raise SystemExit("frozen parent does not match manifest")
    if os.path.exists(dest):
        raise SystemExit("destination exists")
    shutil.copytree(ROOT, dest, symlinks=False, copy_function=shutil.copy2)
    out = {"parentExact": True, "copy": compare(dest)}
elif mode == "verify-parent":
    out = {"parent": compare(ROOT)}
elif mode == "diff":
    out = {"copy": compare(sys.argv[2])}
else:
    raise SystemExit("mode must be copy, verify-parent or diff")
print(json.dumps(out, indent=1))
