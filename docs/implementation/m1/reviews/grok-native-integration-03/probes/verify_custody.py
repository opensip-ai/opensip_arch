#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m1-grok-native-integration-review-03/review")
SUBJECT = Path("/tmp/opensip-implementation/m1-grok-native-integration-review-03/subject")
MANIFEST = Path("/tmp/opensip-implementation/m1-grok-native-integration-review-03/subject-manifest.json")
DECLARED = "b323785fcf3bdee525fb4b84e47d10250a6bf93f57176f10ab92023c7e95069a"
RESULTS = REVIEW / "results"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def walk(root: Path) -> dict[str, dict]:
    found = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == ".":
            rel_dir = ""
        dirnames.sort()
        filenames.sort()
        for name in filenames:
            rel = name if not rel_dir else f"{rel_dir}/{name}"
            p = root / rel
            if p.is_symlink() or not p.is_file():
                found[rel] = {"path": rel, "kind": "nonfile"}
                continue
            st = p.stat()
            found[rel] = {"path": rel, "bytes": st.st_size, "sha256": sha256_file(p)}
    return found


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    raw = MANIFEST.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    man = json.loads(raw)
    listed = {r["path"]: r for r in man["files"]}
    found = walk(SUBJECT)
    extra = sorted(set(found) - set(listed))
    missing = sorted(set(listed) - set(found))
    mismatches = []
    for path, row in listed.items():
        now = found.get(path)
        if not now:
            continue
        if now.get("bytes") != row.get("bytes") or now.get("sha256") != row.get("sha256"):
            mismatches.append({"path": path, "expected": {k: row.get(k) for k in ("bytes", "sha256")}, "actual": {k: now.get(k) for k in ("bytes", "sha256")}})
    out = {
        "outerSha256": digest,
        "declaredSha256": DECLARED,
        "outerMatchesDeclared": digest == DECLARED,
        "listed": len(listed),
        "found": len(found),
        "extra": extra,
        "missing": missing,
        "mismatchCount": len(mismatches),
        "mismatches": mismatches[:20],
        "exactFileSet": not extra and not missing and not mismatches,
        "ok": digest == DECLARED and not extra and not missing and not mismatches,
    }
    (RESULTS / "custody-before.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in ("outerSha256", "outerMatchesDeclared", "listed", "found", "exactFileSet", "mismatchCount", "ok")}, indent=2))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
