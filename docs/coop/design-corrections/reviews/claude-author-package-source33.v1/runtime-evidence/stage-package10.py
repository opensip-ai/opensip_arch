#!/usr/bin/env python3
"""Stage package v10 as an exact copy of the immutable v9, and preserve v9 BEFORE-images.

v9 is never written. The BEFORE-images of every file this pass will edit are copied into
package10/historical-source33-before-remint/ under a name that cannot collide with the existing
historical-source25/26/27/28/30/31/32 preparation directories.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
V9 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v9")
V10 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v10")
BEFORE_DIRNAME = "historical-source33-before-remint"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    existing = sorted(p.name for p in V10.iterdir()) if V10.exists() else []
    if existing:
        raise SystemExit("package10 is not empty; refusing to overwrite: %s" % existing[:10])
    # Guard: the new before-image directory must not collide with any existing name in v9.
    v9_names = {p.name for p in V9.iterdir()}
    if BEFORE_DIRNAME in v9_names:
        raise SystemExit("before-image directory name collides with an existing v9 entry")

    shutil.copytree(V9, V10, dirs_exist_ok=True)

    v9_index, v10_index = {}, {}
    for p in sorted(V9.rglob("*")):
        if p.is_file() and not p.is_symlink():
            v9_index[str(p.relative_to(V9))] = (p.stat().st_size, sha(p))
    for p in sorted(V10.rglob("*")):
        if p.is_file() and not p.is_symlink():
            v10_index[str(p.relative_to(V10))] = (p.stat().st_size, sha(p))

    out = {
        "standing": "package10 staged as an EXACT copy of the immutable package9. v9 is not "
                    "written by this or any later step of this runtime.",
        "v9Root": str(V9), "v10Root": str(V10),
        "v9FileCount": len(v9_index), "v10FileCount": len(v10_index),
        "copyIsExact": v9_index == v10_index,
        "beforeImageDirectory": BEFORE_DIRNAME,
        "beforeImageNameCollidesWithExistingV9Entry": BEFORE_DIRNAME in v9_names,
        "existingHistoricalDirectories": sorted(n for n in v9_names if n.startswith("historical-")),
    }
    (HERE / "reports" / "stage-package10.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0 if out["copyIsExact"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
