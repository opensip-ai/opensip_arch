"""Verify frozen checker09 files/modes/links and copy listed entries only."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import sys
from pathlib import Path

FROZEN = Path("/tmp/opensip-implementation/m1-typescript-boundary-package-subject-09")
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/typescript-boundary-package-09/subject.json")
ARCHIVE = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/typescript-boundary-package-09/subject.tar.gz")
EXPECTED_MANIFEST = "a0ba3490eda46e4013030b7c0ac427a27bbc94ce630e074a8ca950190b025278"
EXPECTED_ARCHIVE = "7112392223bbf39cd376ff1aaca3d3e1a7ce6cd55036145af19ecce349d0c9bf"
EXPECTED_ARCHIVE_BYTES = 9013398
REVIEW = Path("/tmp/opensip-implementation/m1-grok-typescript-boundary-package-review-09/review")
PARENT08 = Path("/tmp/opensip-implementation/m1-typescript-boundary-package-subject-08")


def pin_bytes(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def verify(label: str) -> dict:
    raw = MANIFEST.read_bytes()
    outer = hashlib.sha256(raw).hexdigest()
    manifest = json.loads(raw)
    listed = manifest["entries"]
    files = dirs = links = 0
    mismatches = []
    for row in listed:
        p = FROZEN / row["path"]
        try:
            st = p.lstat()
        except FileNotFoundError:
            mismatches.append({"path": row["path"], "error": "missing"})
            continue
        mode = stat.S_IMODE(st.st_mode)
        if row["type"] == "file":
            files += 1
            if not stat.S_ISREG(st.st_mode):
                mismatches.append({"path": row["path"], "error": "not-file"})
                continue
            actual = pin_bytes(p.read_bytes())
            if mode != row["mode"] or actual["bytes"] != row["bytes"] or actual["sha256"] != row["sha256"]:
                mismatches.append({"path": row["path"], "mode": mode, "actual": actual, "row": row})
        elif row["type"] == "directory":
            dirs += 1
            if not stat.S_ISDIR(st.st_mode) or mode != row["mode"]:
                mismatches.append({"path": row["path"], "error": "dir-mismatch", "mode": mode})
        elif row["type"] == "symlink":
            links += 1
            if not stat.S_ISLNK(st.st_mode):
                mismatches.append({"path": row["path"], "error": "not-symlink"})
                continue
            target = os.readlink(p)
            if target != row.get("target") or mode != row["mode"]:
                mismatches.append({"path": row["path"], "target": target, "mode": mode, "row": row})
        else:
            mismatches.append({"path": row["path"], "error": "unknown-type"})
    archive = pin_bytes(ARCHIVE.read_bytes())
    return {
        "label": label,
        "outerSha256": outer,
        "declaredSha256": EXPECTED_MANIFEST,
        "outerMatchesDeclared": outer == EXPECTED_MANIFEST,
        "listedEntries": len(listed),
        "files": files,
        "directories": dirs,
        "symlinks": links,
        "mismatchCount": len(mismatches),
        "mismatches": mismatches[:20],
        "archiveSha256": archive["sha256"],
        "archiveBytes": archive["bytes"],
        "archiveMatches": archive == {"bytes": EXPECTED_ARCHIVE_BYTES, "sha256": EXPECTED_ARCHIVE},
        "ok": outer == EXPECTED_MANIFEST
        and not mismatches
        and len(listed) == 253
        and files == 209
        and archive["sha256"] == EXPECTED_ARCHIVE
        and archive["bytes"] == EXPECTED_ARCHIVE_BYTES,
    }


def copy_listed() -> dict:
    dest = REVIEW / "copy"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    manifest = json.loads(MANIFEST.read_text())
    copied = 0
    for row in manifest["entries"]:
        src = FROZEN / row["path"]
        dst = dest / row["path"]
        if row["type"] == "directory":
            dst.mkdir(parents=True, exist_ok=True)
            os.chmod(dst, row["mode"])
        elif row["type"] == "file":
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())
            os.chmod(dst, row["mode"])
        elif row["type"] == "symlink":
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists() or dst.is_symlink():
                dst.unlink()
            os.symlink(row["target"], dst)
        copied += 1
    return {"copied": copied, "dest": str(dest)}


def delta_vs_08() -> dict:
    skip = {"node_modules"}
    changed = []
    only09 = []
    only08 = []

    def walk(root: Path):
        rows = {}
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in skip]
            rel_dir = Path(dirpath).relative_to(root)
            for name in filenames:
                p = Path(dirpath) / name
                if p.is_symlink():
                    continue
                rel = (rel_dir / name).as_posix() if str(rel_dir) != "." else name
                if "node_modules" in rel.split("/"):
                    continue
                raw = p.read_bytes()
                rows[rel] = hashlib.sha256(raw).hexdigest()
        return rows

    a = walk(PARENT08)
    b = walk(FROZEN)
    for rel in sorted(set(a) | set(b)):
        if rel not in a:
            only09.append(rel)
        elif rel not in b:
            only08.append(rel)
        elif a[rel] != b[rel]:
            changed.append(rel)
    return {"changed": changed, "only09": only09, "only08": only08}


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    (REVIEW / "results").mkdir(parents=True, exist_ok=True)
    before = verify("before")
    (REVIEW / "results" / "custody-before.json").write_text(json.dumps(before, indent=2) + "\n")
    copied = copy_listed()
    delta = delta_vs_08()
    (REVIEW / "results" / "delta-vs-08.json").write_text(json.dumps(delta, indent=2) + "\n")
    print(json.dumps({"custodyOk": before["ok"], "copied": copied["copied"], "delta": delta}, indent=2))


if __name__ == "__main__":
    main()
