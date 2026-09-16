"""Reverify frozen subject bytes after review work. Read-only on the freeze."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

FROZEN = Path("/tmp/opensip-implementation/m1-history-selection-subject-02")
OUTER = Path("/tmp/opensip-implementation/m1-history-selection-subject-02.manifest.json")
DECLARED = "39ddac40846fe240eea8352299d5059b7645cab9b0b0e7719f05a20d00d3d15e"
RESULTS = Path("/tmp/opensip-implementation/m1-grok-history-selection-review-02/review/results")
ADJACENT = Path("/tmp/opensip-implementation/m1-grok-history-selection-review-02/subject-manifest.json")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    outer_raw = OUTER.read_bytes()
    outer_hash = sha(outer_raw)
    manifest = json.loads(outer_raw)
    listed = [row["path"] for row in manifest["files"]]
    found = sorted(p.relative_to(FROZEN).as_posix() for p in FROZEN.rglob("*") if p.is_file())
    extra = sorted(set(found) - set(listed))
    missing = sorted(set(listed) - set(found))
    mismatches = []
    for row in manifest["files"]:
        p = FROZEN / row["path"]
        raw = p.read_bytes()
        if len(raw) != row["bytes"] or sha(raw) != row["sha256"]:
            mismatches.append(row["path"])
        if "mode" in row or "symlink" in row:
            mismatches.append("unexpected-mode-or-symlink:" + row["path"])
    pins = json.loads((FROZEN / "input-pins.json").read_bytes())["files"]
    pin_fail = []
    for pin in pins:
        raw = Path(pin["path"]).read_bytes()
        if len(raw) != pin["bytes"] or sha(raw) != pin["sha256"]:
            pin_fail.append(pin["path"])
    adjacent_hash = sha(ADJACENT.read_bytes()) if ADJACENT.is_file() else None
    out = {
        "outerSha256": outer_hash,
        "declaredSha256": DECLARED,
        "outerMatchesDeclared": outer_hash == DECLARED,
        "adjacentMatchesOuter": adjacent_hash == outer_hash,
        "listed": len(listed),
        "found": len(found),
        "extra": extra,
        "missing": missing,
        "mismatchCount": len(mismatches),
        "mismatches": mismatches,
        "pins": len(pins),
        "pinFailCount": len(pin_fail),
        "pinFail": pin_fail,
        "exactFileSet": extra == [] and missing == [],
        "frozenUnchanged": outer_hash == DECLARED and not mismatches and extra == [] and missing == [],
        "ok": outer_hash == DECLARED
        and not mismatches
        and extra == []
        and missing == []
        and not pin_fail
        and len(listed) == 70
        and len(pins) == 71,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "custody-after.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in ("ok", "outerSha256", "listed", "pins", "mismatchCount", "pinFailCount")}))
    raise SystemExit(0 if out["ok"] else 1)


if __name__ == "__main__":
    main()
