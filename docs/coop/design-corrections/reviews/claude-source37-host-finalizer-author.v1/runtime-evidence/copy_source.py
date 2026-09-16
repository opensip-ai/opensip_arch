"""Verify the frozen source37 manifest, copy the snapshot into this runtime, and verify the copy file by file.

Usage: python -I -B copy_source.py copy|verify DEST
`copy` refuses an existing DEST. `verify` compares DEST against the manifest and reports every
changed, missing or extra path (the author's edits are expected to show up here after editing).
Reads the frozen snapshot and manifest only; writes only DEST and stdout.
"""
import hashlib
import json
import os
import shutil
import sys

MANIFEST = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json"
EXPECTED = "245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680"
mode, dest = sys.argv[1], sys.argv[2]
raw = open(MANIFEST, "rb").read()
manifest_sha = hashlib.sha256(raw).hexdigest()
if manifest_sha != EXPECTED:
    raise SystemExit(f"manifest sha {manifest_sha} != {EXPECTED}")
m = json.loads(raw)
src = m["snapshotRoot"]


def verify(root):
    bad, listed, total = [], set(), 0
    for f in m["files"]:
        listed.add(f["path"])
        p = os.path.join(root, f["path"])
        if not os.path.isfile(p):
            bad.append({"path": f["path"], "state": "missing"})
            continue
        b = open(p, "rb").read()
        total += len(b)
        if hashlib.sha256(b).hexdigest() != f["sha256"] or len(b) != f["bytes"]:
            bad.append({"path": f["path"], "state": "changed", "sha256": hashlib.sha256(b).hexdigest(), "manifestSha256": f["sha256"]})
    extra = []
    for d, _, fs in os.walk(root):
        for fn in fs:
            rel = os.path.relpath(os.path.join(d, fn), root)
            if rel not in listed and "__pycache__" not in rel:
                extra.append(rel)
    return {"root": root, "files": len(m["files"]), "fileCountDeclared": m["fileCount"], "bytesMeasured": total,
            "totalBytesDeclared": m["totalBytes"], "changedOrMissing": bad, "extraFiles": sorted(extra),
            "exact": not bad and not extra and total == m["totalBytes"]}


if mode == "copy":
    frozen = verify(src)
    if not frozen["exact"]:
        print(json.dumps({"frozen": frozen}, indent=1))
        raise SystemExit("frozen snapshot does not match manifest; refusing to copy")
    if os.path.exists(dest):
        raise SystemExit(f"{dest} exists; refusing to overwrite")
    shutil.copytree(src, dest, symlinks=True)
    result = {"manifestSha256": manifest_sha, "frozenVerified": frozen["exact"], "copy": verify(dest)}
elif mode == "verify":
    result = {"manifestSha256": manifest_sha, "copy": verify(dest)}
else:
    raise SystemExit("mode must be copy or verify")
print(json.dumps(result, indent=1))
raise SystemExit(0 if mode == "verify" or result["copy"]["exact"] else 1)
