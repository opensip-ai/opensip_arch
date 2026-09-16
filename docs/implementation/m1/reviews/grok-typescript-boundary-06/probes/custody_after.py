"""Reverify frozen TS06 bytes after review work."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

FROZEN = Path("/tmp/opensip-implementation/m1-typescript-boundary-subject-06")
OUTER = Path("/tmp/opensip-implementation/m1-typescript-boundary-subject-06.manifest.json")
DECLARED = "0b399a5ed1f1ddd9c179870778da02de8bfa8049ba4134e04638cbdc239e6ae4"
RESULTS = Path("/tmp/opensip-implementation/m1-grok-typescript-boundary-review-06/review/results")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    raw = OUTER.read_bytes()
    outer_hash = sha(raw)
    man = json.loads(raw)
    listed = [r["path"] for r in man["files"]]
    found = sorted(
        p.relative_to(FROZEN).as_posix()
        for p in FROZEN.rglob("*")
        if p.is_symlink() or p.is_file()
    )
    extra = sorted(set(found) - set(listed))
    missing = sorted(set(listed) - set(found))
    mismatches = []
    for row in man["files"]:
        p = FROZEN / row["path"]
        if row["type"] == "symlink":
            if not p.is_symlink() or os.readlink(p) != row["target"]:
                mismatches.append(row["path"])
        else:
            b = p.read_bytes()
            if len(b) != row["bytes"] or sha(b) != row["sha256"]:
                mismatches.append(row["path"])
    out = {
        "outerSha256": outer_hash,
        "declaredSha256": DECLARED,
        "outerMatchesDeclared": outer_hash == DECLARED,
        "listed": len(listed),
        "found": len(found),
        "extraCount": len(extra),
        "missingCount": len(missing),
        "mismatchCount": len(mismatches),
        "frozenUnchanged": outer_hash == DECLARED and not extra and not missing and not mismatches,
        "ok": outer_hash == DECLARED and not extra and not missing and not mismatches and len(listed) == 1700,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "custody-after.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out))
    raise SystemExit(0 if out["ok"] else 1)


if __name__ == "__main__":
    main()
