"""Reverify frozen history-native-delta bytes after review work."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

FROZEN = Path("/tmp/opensip-implementation/m1-history-native-delta-subject-01")
OUTER = Path("/tmp/opensip-implementation/m1-history-native-delta-subject-01.manifest.json")
DECLARED = "c87231a09082032f9b7c61ece2d13a7b31ab596478027f45e9940db95bbcb224"
RESULTS = Path("/tmp/opensip-implementation/m1-grok-history-native-delta-review-01/review/results")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    raw = OUTER.read_bytes()
    outer_hash = sha(raw)
    man = json.loads(raw)
    listed = [r["path"] for r in man["files"]]
    found = sorted(p.relative_to(FROZEN).as_posix() for p in FROZEN.rglob("*") if p.is_file())
    extra = sorted(set(found) - set(listed))
    missing = sorted(set(listed) - set(found))
    mismatches = []
    for row in man["files"]:
        b = (FROZEN / row["path"]).read_bytes()
        if len(b) != row["bytes"] or sha(b) != row["sha256"]:
            mismatches.append(row["path"])
    out = {
        "outerSha256": outer_hash,
        "declaredSha256": DECLARED,
        "listed": len(listed),
        "found": len(found),
        "extraCount": len(extra),
        "missingCount": len(missing),
        "mismatchCount": len(mismatches),
        "frozenUnchanged": outer_hash == DECLARED and not extra and not missing and not mismatches,
        "ok": outer_hash == DECLARED and not extra and not missing and not mismatches and len(listed) == 403,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "custody-after.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out))
    raise SystemExit(0 if out["ok"] else 1)


if __name__ == "__main__":
    main()
