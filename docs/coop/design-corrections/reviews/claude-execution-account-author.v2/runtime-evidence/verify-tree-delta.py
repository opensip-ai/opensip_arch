#!/usr/bin/env python3
"""Whole-tree delta: the v2 working copy vs the frozen32 subject it was copied from.

READ ONLY on both trees. Also separates the v1 changes from the v2 changes, so root can see that
this follow-up touched no new file beyond the nine v1 already named.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v32")
WORK = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source")
V1 = Path("/tmp/opensip-design-corrections/claude-execution-account-author.v1")


def index(root: Path) -> dict:
    out = {}
    for p in root.rglob("*"):
        if p.is_file() and not p.is_symlink():
            raw = p.read_bytes()
            out[str(p.relative_to(root))] = (len(raw), hashlib.sha256(raw).hexdigest())
    return out


def main() -> int:
    a, b = index(FROZEN), index(WORK)
    changed = sorted(k for k in a.keys() & b.keys() if a[k][1] != b[k][1])
    added = sorted(b.keys() - a.keys())
    removed = sorted(a.keys() - b.keys())
    v1_after = {r["path"]: r["sha256"] for r in json.loads((V1 / "after-hashes.json").read_text())}
    rows = []
    for k in changed:
        rows.append({
            "path": k, "frozenSha256": a[k][1], "workingSha256": b[k][1],
            "v1HandoffSha256": v1_after.get(k),
            "changedInV2": v1_after.get(k) is not None and v1_after[k] != b[k][1],
            "unchangedSinceV1": v1_after.get(k) == b[k][1],
        })
    out = {
        "standing": "READ-ONLY whole-tree comparison of the v2 working copy against the frozen32 "
                    "subject. Not a custody claim over frozen32, which remains the root retainer's.",
        "frozen": {"root": str(FROZEN), "files": len(a), "bytes": sum(v[0] for v in a.values())},
        "working": {"root": str(WORK), "files": len(b), "bytes": sum(v[0] for v in b.values())},
        "changedFiles": rows,
        "addedFiles": added, "removedFiles": removed,
        "changedCount": len(changed), "addedCount": len(added), "removedCount": len(removed),
        "changedInV2": [r["path"] for r in rows if r["changedInV2"]],
        "unchangedSinceV1": [r["path"] for r in rows if r["unchangedSinceV1"]],
        "newFilesTouchedInV2BeyondV1": [r["path"] for r in rows if r["v1HandoffSha256"] is None],
    }
    (HERE / "tree-delta.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "frozenFiles": out["frozen"]["files"], "frozenBytes": out["frozen"]["bytes"],
        "changedCount": out["changedCount"], "added": added, "removed": removed,
        "changedInV2": out["changedInV2"],
        "unchangedSinceV1": out["unchangedSinceV1"],
        "newFilesTouchedInV2BeyondV1": out["newFilesTouchedInV2BeyondV1"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
