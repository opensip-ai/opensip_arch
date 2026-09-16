"""Verify the old author package against its artifact manifest, then copy it as regular files.

Refuses unless artifact-manifest.json has the pinned SHA-256 and every listed file matches its digest and size.
Files present but unlisted (other than __pycache__) are reported. The copy is byte-for-byte and re-verified.
Usage: copy_package.py PACKAGE DEST MANIFEST_SHA256 OUT_JSON
"""
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

pkg, dest, want, out_json = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], Path(sys.argv[4])
if dest.exists():
    raise SystemExit("destination exists")
raw = (pkg / "artifact-manifest.json").read_bytes()
got = hashlib.sha256(raw).hexdigest()
if got != want:
    raise SystemExit("artifact manifest digest %s != %s" % (got, want))
manifest = json.loads(raw)
faults, listed = [], set()
for row in manifest["files"]:
    p = pkg / row["path"]
    listed.add(row["path"])
    if not p.is_file() or p.is_symlink():
        faults.append({"path": row["path"], "fault": "missing"})
        continue
    data = p.read_bytes()
    if hashlib.sha256(data).hexdigest() != row["sha256"] or len(data) != row["bytes"]:
        faults.append({"path": row["path"], "fault": "digest"})
present = set()
for d, dirs, files in os.walk(pkg):
    dirs[:] = [x for x in dirs if x != "__pycache__"]
    for name in files:
        present.add((Path(d) / name).relative_to(pkg).as_posix())
unlisted = sorted(present - listed - {"artifact-manifest.json"})
if faults:
    print(json.dumps({"verified": False, "faults": faults[:20]}, indent=1))
    raise SystemExit(1)
shutil.copytree(pkg, dest, symlinks=False, copy_function=shutil.copy2, ignore=shutil.ignore_patterns("__pycache__"))
copy_faults = [r["path"] for r in manifest["files"]
               if hashlib.sha256((dest / r["path"]).read_bytes()).hexdigest() != r["sha256"]]
report = {"package": str(pkg), "copy": str(dest), "artifactManifestSha256": got, "listedFiles": len(manifest["files"]),
          "verified": True, "unlistedFilesPresent": unlisted, "copyFaults": copy_faults,
          "sourceManifestSha256": manifest.get("sourceManifestSha256")}
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps(report, indent=1))
raise SystemExit(1 if copy_faults else 0)
