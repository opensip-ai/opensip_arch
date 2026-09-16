"""Outer-manifest custody for TS06: files, modes, symlink targets. Read-only on freeze."""
from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

FROZEN = Path("/tmp/opensip-implementation/m1-typescript-boundary-subject-06")
OUTER = Path("/tmp/opensip-implementation/m1-typescript-boundary-subject-06.manifest.json")
DECLARED = "0b399a5ed1f1ddd9c179870778da02de8bfa8049ba4134e04638cbdc239e6ae4"
RESULTS = Path("/tmp/opensip-implementation/m1-grok-typescript-boundary-review-06/review/results")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def mode_of(path: Path) -> str:
    return oct(path.lstat().st_mode & 0o7777)[2:]


def walk_files(root: Path) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        # include symlink dirs? os.walk doesn't follow by default; symlink dirs appear in dirnames
        # We need every file and symlink. os.walk lists symlink-to-dir as dir if followlinks False... actually
        # symlink dirs are in dirnames and will be walked into if they point to dirs within?
        # Safer: use freeze list vs rglob without follow.
        pass
    for p in root.rglob("*"):
        if p.is_symlink() or p.is_file():
            out.append(p.relative_to(root).as_posix())
    return sorted(out)


def main() -> None:
    raw = OUTER.read_bytes()
    outer_hash = sha(raw)
    man = json.loads(raw)
    listed = man["files"]
    listed_paths = [r["path"] for r in listed]
    found = walk_files(FROZEN)
    extra = sorted(set(found) - set(listed_paths))
    missing = sorted(set(listed_paths) - set(found))
    mismatches = []
    symlink_ok = 0
    file_ok = 0
    for row in listed:
        p = FROZEN / row["path"]
        try:
            st = p.lstat()
        except FileNotFoundError:
            mismatches.append({"path": row["path"], "error": "missing"})
            continue
        if mode_of(p) != str(row.get("mode", mode_of(p))):
            mismatches.append({"path": row["path"], "error": "mode", "want": row.get("mode"), "got": mode_of(p)})
        if row["type"] == "symlink":
            if not p.is_symlink():
                mismatches.append({"path": row["path"], "error": "not-symlink"})
                continue
            got = os.readlink(p)
            if got != row["target"]:
                mismatches.append({"path": row["path"], "error": "target", "want": row["target"], "got": got})
            else:
                symlink_ok += 1
        elif row["type"] == "file":
            if p.is_symlink() or not p.is_file():
                mismatches.append({"path": row["path"], "error": "not-file"})
                continue
            b = p.read_bytes()
            if len(b) != row["bytes"] or sha(b) != row["sha256"]:
                mismatches.append({"path": row["path"], "error": "hash"})
            else:
                file_ok += 1
        else:
            mismatches.append({"path": row["path"], "error": "unknown-type"})
    types = {}
    for r in listed:
        types[r["type"]] = types.get(r["type"], 0) + 1
    out = {
        "outerSha256": outer_hash,
        "declaredSha256": DECLARED,
        "outerMatchesDeclared": outer_hash == DECLARED,
        "listed": len(listed),
        "found": len(found),
        "extra": extra[:20],
        "extraCount": len(extra),
        "missing": missing[:20],
        "missingCount": len(missing),
        "mismatchCount": len(mismatches),
        "mismatches": mismatches[:30],
        "types": types,
        "filesOk": file_ok,
        "symlinksOk": symlink_ok,
        "exactFileSet": extra == [] and missing == [],
        "ok": outer_hash == DECLARED
        and extra == []
        and missing == []
        and not mismatches
        and len(listed) == 1700
        and types.get("symlink") == 18,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "custody-before.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in ("ok", "outerSha256", "listed", "found", "types", "mismatchCount", "extraCount", "missingCount")}))
    raise SystemExit(0 if out["ok"] else 1)


if __name__ == "__main__":
    main()
