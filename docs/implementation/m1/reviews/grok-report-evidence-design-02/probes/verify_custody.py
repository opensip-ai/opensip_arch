#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m1-grok-report-evidence-design-review-02/review")
SUBJECT = Path("/tmp/opensip-implementation/m1-report-evidence-design-subject-02")
OUTER = Path("/tmp/opensip-implementation/m1-report-evidence-design-subject-02.json")
ADJACENT = Path("/tmp/opensip-implementation/m1-grok-report-evidence-design-review-02/subject-manifest.json")
DECLARED = "d811b4132058668e7404c23d6159e43f929284f5a79de55539c32c1380d5a18e"
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
            if p.is_symlink():
                found[rel] = {"kind": "symlink", "target": os.readlink(p)}
                continue
            if p.is_file():
                found[rel] = {"bytes": p.stat().st_size, "sha256": sha256_file(p)}
    return found


def listing_digest(path: str) -> str:
    return hashlib.sha256("\n".join(sorted(os.listdir(path))).encode()).hexdigest()


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    raw = OUTER.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    adj = hashlib.sha256(ADJACENT.read_bytes()).hexdigest()
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
        if now.get("kind") == "symlink":
            mismatches.append({"path": path, "field": "symlink"})
            continue
        if now.get("bytes") != row.get("bytes") or now.get("sha256") != row.get("sha256"):
            mismatches.append({"path": path, "expected": {k: row.get(k) for k in ("bytes", "sha256")}, "actual": now})
    pins = json.loads((SUBJECT / "source-pins.json").read_text())
    pin_fail = []
    for pin in pins["files"]:
        p = Path(pin["path"])
        if not p.is_file() or p.is_symlink():
            pin_fail.append({"path": pin["path"], "reason": "missing-or-symlink"})
            continue
        if p.stat().st_size != pin["bytes"] or sha256_file(p) != pin["sha256"]:
            pin_fail.append({"path": pin["path"], "reason": "bytes-or-hash"})
    listing_fail = []
    for listing in pins["directoryListings"]:
        if listing_digest(listing["path"]) != listing["entriesSha256"]:
            listing_fail.append(listing["path"])
    inner = json.loads((SUBJECT / "subject-files.json").read_bytes())
    inner_listed = {r["path"] for r in inner["files"]}
    out = {
        "outerSha256": digest,
        "declaredSha256": DECLARED,
        "outerMatchesDeclared": digest == DECLARED,
        "adjacentMatchesOuter": adj == digest,
        "listed": len(listed),
        "found": len(found),
        "extra": extra,
        "missing": missing,
        "mismatchCount": len(mismatches),
        "mismatches": mismatches[:10],
        "innerSubjectFiles": len(inner_listed),
        "innerEqualsOuterMinusSelf": inner_listed == (set(listed) - {"subject-files.json"}),
        "pins": {"files": len(pins["files"]), "failed": pin_fail[:10], "failCount": len(pin_fail), "listings": len(pins["directoryListings"]), "listingFail": listing_fail},
        "parent07Manifest": Path("/tmp/opensip-implementation/m1-report-projection-subject-07.json").is_file(),
        "subject01Manifest": Path("/tmp/opensip-implementation/m1-report-evidence-design-subject-01.json").is_file(),
        "review01": Path("/tmp/opensip-implementation/m1-report-evidence-design-review-01/review.json").is_file(),
        "exactFileSet": not extra and not missing and not mismatches,
        "ok": digest == DECLARED and adj == digest and not extra and not missing and not mismatches and not pin_fail and not listing_fail,
    }
    (RESULTS / "custody-before.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in ("outerSha256", "outerMatchesDeclared", "adjacentMatchesOuter", "listed", "found", "exactFileSet", "ok")}, indent=2))
    print("pins", out["pins"]["files"], "fail", out["pins"]["failCount"], "listings", out["pins"]["listings"], "listingFail", listing_fail)
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
