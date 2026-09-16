"""Custody of frozen schema-inventory04. Read-only on the freeze."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

FROZEN = Path("/tmp/opensip-implementation/m1-schema-inventory-subject-04")
OUTER = Path("/tmp/opensip-implementation/m1-schema-inventory-subject-04.manifest.json")
DECLARED = "6e9145ef1549a467fb9547b50c7b5bfb6a5b33838d2e127b6d67ad12cf0a9c1c"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
RESULTS = Path("/tmp/opensip-implementation/m1-grok-schema-inventory-review-04/review/results")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def snapshot(label: str) -> dict:
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
        if "mode" in row or "symlink" in row:
            mismatches.append("unexpected-mode-or-symlink:" + row["path"])
    pins = json.loads((FROZEN / "input-pins.json").read_bytes())["files"]
    pin_fail = []
    for pin in pins:
        raw = (ARCH / pin["path"]).read_bytes()
        copy_raw = (FROZEN / pin["copy"]).read_bytes()
        if len(raw) != pin["bytes"] or sha(raw) != pin["sha256"]:
            pin_fail.append("arch:" + pin["path"])
        if copy_raw != raw:
            pin_fail.append("copy-arch-mismatch:" + pin["copy"])
        if len(copy_raw) != pin["bytes"] or sha(copy_raw) != pin["sha256"]:
            pin_fail.append("copy:" + pin["copy"])
    out = {
        "label": label,
        "outerSha256": outer_hash,
        "declaredSha256": DECLARED,
        "outerMatchesDeclared": outer_hash == DECLARED,
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
        and len(listed) == 10
        and len(pins) == 5,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"custody-{label}.json").write_bytes(
        (json.dumps(out, indent=2) + "\n").encode()
    )
    return out


if __name__ == "__main__":
    import sys

    label = sys.argv[1] if len(sys.argv) > 1 else "before"
    out = snapshot(label)
    print(json.dumps({k: out[k] for k in ("ok", "label", "outerSha256", "listed", "pins", "mismatchCount", "pinFailCount")}))
    raise SystemExit(0 if out["ok"] else 1)
