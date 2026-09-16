"""Check that correction.patch applied by a standard tool to the frozen39 before-bytes reproduces the delta after-bytes.

Usage: patch_apply_check.py prepare DELTA_MANIFEST DIR   # write each delta file's frozen39 bytes under DIR (must not exist)
       patch_apply_check.py verify  DELTA_MANIFEST DIR OUT_JSON   # after `patch -p1 -d DIR -i PATCH`: compare to after
"""
import hashlib
import json
import sys
from pathlib import Path

mode, delta_path, d = sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
delta = json.loads(delta_path.read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
manifest = Path(delta["base"]["manifest"])
if sha(manifest.read_bytes()) != delta["base"]["manifestSha256"]:
    raise SystemExit("manifest sha mismatch")
root = Path(json.loads(manifest.read_bytes())["snapshotRoot"])
if mode == "prepare":
    if d.exists():
        raise SystemExit("exists: %s" % d)
    for f in delta["files"]:
        data = (root / f["path"]).read_bytes()
        if sha(data) != f["before"]["sha256"]:
            raise SystemExit("frozen39 drift: " + f["path"])
        (d / f["path"]).parent.mkdir(parents=True, exist_ok=True)
        with open(d / f["path"], "xb") as fh:
            fh.write(data)
    print(json.dumps({"prepared": [f["path"] for f in delta["files"]]}, indent=1))
else:
    patch = delta_path.parent / delta["patch"]["path"]
    rows = []
    for f in delta["files"]:
        data = (d / f["path"]).read_bytes()
        rows.append({"path": f["path"], "sha256": sha(data), "bytes": len(data),
                     "holds": sha(data) == f["after"]["sha256"] and len(data) == f["after"]["bytes"]})
    stray = sorted(p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file() and p.relative_to(d).as_posix() not in {f["path"] for f in delta["files"]})
    out = {"artifact": "nested-workspace-author.patch-apply-check", "version": 1, "patch": str(patch), "patchSha256": sha(patch.read_bytes()),
           "patchShaMatchesManifest": sha(patch.read_bytes()) == delta["patch"]["sha256"], "files": rows, "strayFiles": stray,
           "holds": all(r["holds"] for r in rows) and not stray and sha(patch.read_bytes()) == delta["patch"]["sha256"]}
    Path(sys.argv[4]).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))
    raise SystemExit(0 if out["holds"] else 1)
