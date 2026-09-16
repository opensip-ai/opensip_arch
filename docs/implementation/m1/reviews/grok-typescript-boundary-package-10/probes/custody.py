"""Verify frozen checker10 files/modes/links and copy listed entries only."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import sys
from pathlib import Path

FROZEN = Path("/tmp/opensip-implementation/m1-typescript-boundary-package-subject-10")
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/typescript-boundary-package-10/subject.json")
ARCHIVE = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/typescript-boundary-package-10/subject.tar.gz")
EXPECTED_MANIFEST = "7634b25d30c4d93301c66c4d09081c3aa452f8d9f383b7622eae69f2269acaec"
EXPECTED_ARCHIVE = "f2aae7c0833bbab9399543f1fd112356c20baf4744b46885c164984dbeacc4b8"
EXPECTED_ARCHIVE_BYTES = 9019804
REVIEW = Path("/tmp/opensip-implementation/m1-grok-typescript-boundary-package-review-10/review")
PARENT09 = Path("/tmp/opensip-implementation/m1-typescript-boundary-package-subject-09")
ARCH09 = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/typescript-boundary-package-09/subject.json")
ARCH09_SHA = "a0ba3490eda46e4013030b7c0ac427a27bbc94ce630e074a8ca950190b025278"


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
                mismatches.append({"path": row["path"], "mode": mode, "actual": actual, "row": {k: row.get(k) for k in ("bytes", "sha256", "mode")}})
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
                mismatches.append({"path": row["path"], "target": target, "mode": mode})
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
        and len(listed) == 263
        and files == 217
        and archive["sha256"] == EXPECTED_ARCHIVE
        and archive["bytes"] == EXPECTED_ARCHIVE_BYTES,
        "parent09ManifestUnchanged": hashlib.sha256(ARCH09.read_bytes()).hexdigest() == ARCH09_SHA,
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


def delta_vs_09() -> dict:
    skip = {"node_modules"}
    changed, only10, only09 = [], [], []

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
                rows[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
        return rows

    a, b = walk(PARENT09), walk(FROZEN)
    for rel in sorted(set(a) | set(b)):
        if rel not in a:
            only10.append(rel)
        elif rel not in b:
            only09.append(rel)
        elif a[rel] != b[rel]:
            changed.append(rel)
    return {"changed": changed, "only10": only10, "only09": only09}


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    (REVIEW / "results").mkdir(parents=True, exist_ok=True)
    before = verify("before")
    (REVIEW / "results" / "custody-before.json").write_text(json.dumps(before, indent=2) + "\n")
    copied = copy_listed()
    delta = delta_vs_09()
    (REVIEW / "results" / "delta-vs-09.json").write_text(json.dumps(delta, indent=2) + "\n")
    print(json.dumps({"custodyOk": before["ok"], "copied": copied["copied"], "parent09Unchanged": before["parent09ManifestUnchanged"], "delta": delta}, indent=2))


if __name__ == "__main__":
    main()
