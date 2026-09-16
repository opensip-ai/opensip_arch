"""Reverify frozen report-projection08 bytes after review work."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

FROZEN = Path("/tmp/opensip-implementation/m1-report-projection-subject-08")
OUTER = Path("/tmp/opensip-implementation/m1-report-projection-subject-08.json")
DECLARED = "be85df13b84789295e4ed4b63153bfbb4589885fba22bfd883d661f97776f033"
RESULTS = Path("/tmp/opensip-implementation/m1-grok-report-projection-review-08/review/results")
ADJACENT = Path("/tmp/opensip-implementation/m1-grok-report-projection-review-08/subject-manifest.json")


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
        raw = (FROZEN / row["path"]).read_bytes()
        if len(raw) != row["bytes"] or sha(raw) != row["sha256"]:
            mismatches.append(row["path"])
    pins = json.loads((FROZEN / "source-pins.json").read_bytes())
    pin_fail = []
    for pin in pins["files"]:
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
        "pins": len(pins["files"]),
        "listings": len(pins["directoryListings"]),
        "pinFailCount": len(pin_fail),
        "pinFail": pin_fail,
        "exactFileSet": extra == [] and missing == [],
        "frozenUnchanged": outer_hash == DECLARED and not mismatches and extra == [] and missing == [],
        "ok": outer_hash == DECLARED
        and not mismatches
        and extra == []
        and missing == []
        and not pin_fail
        and len(listed) == 21
        and len(pins["files"]) == 96
        and len(pins["directoryListings"]) == 3,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "custody-after.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in ("ok", "outerSha256", "listed", "pins", "listings", "mismatchCount", "pinFailCount")}))
    raise SystemExit(0 if out["ok"] else 1)


if __name__ == "__main__":
    main()
