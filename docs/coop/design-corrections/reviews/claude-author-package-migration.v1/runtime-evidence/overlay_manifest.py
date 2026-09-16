"""Write overlay/overlay-manifest.json and per-file unified diffs of the overlay against package15.

Every overlay file is listed with its package15 base digest (null for a new file) and its overlay digest, so an
orchestration can refuse to apply the overlay onto any other base. Diffs go to OUTDIR.
Usage: overlay_manifest.py OVERLAY PACKAGE15 OUTDIR
"""
import difflib
import hashlib
import json
import os
import sys
from pathlib import Path

overlay, base, outdir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
outdir.mkdir(parents=True, exist_ok=True)
rows, parts = [], []
for d, dirs, files in os.walk(overlay):
    dirs[:] = [x for x in dirs if x != "__pycache__"]
    for name in files:
        rel = (Path(d) / name).relative_to(overlay).as_posix()
        if rel == "overlay-manifest.json":
            continue
        data = (overlay / rel).read_bytes()
        prior = base / rel
        before = prior.read_bytes() if prior.is_file() else None
        rows.append({"path": rel, "status": "added" if before is None else ("modified" if before != data else "unchanged"),
                     "package15Sha256": hashlib.sha256(before).hexdigest() if before is not None else None,
                     "package15Bytes": len(before) if before is not None else None,
                     "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
        parts.extend(difflib.unified_diff((before or b"").decode().splitlines(keepends=True), data.decode().splitlines(keepends=True),
                                          fromfile=("package15/" + rel) if before is not None else "/dev/null",
                                          tofile="overlay/" + rel, n=3))
rows.sort(key=lambda r: r["path"].encode())
unchanged = [r["path"] for r in rows if r["status"] == "unchanged"]
if unchanged:
    raise SystemExit("overlay carries unchanged files (remove them): %s" % unchanged)
text = "".join(parts)
(outdir / "overlay-vs-package15.diff").write_text(text)
manifest = {"artifact": "author-package-migration.overlay", "version": 1,
            "base": "claude-author-package-successor.v15 (artifact-manifest 6a8d4feca9db7ea48e91debf3a080415f769ac7271b8bf67df145263148b701e)",
            "files": rows, "diffSha256": hashlib.sha256(text.encode()).hexdigest()}
(overlay / "overlay-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
print(json.dumps({"files": [(r["status"], r["path"]) for r in rows], "diffSha256": manifest["diffSha256"]}, indent=1))
