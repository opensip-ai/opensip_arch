#!/usr/bin/env python3
"""Whole-tree delta: successor working copy vs the frozen32 subject it was copied from.

READ ONLY on both trees. Establishes exactly which files this authorship changed, added or
removed across all 12 898 files, rather than inferring it from the two pin ledgers.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v32")
WORK = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source")


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
    out = {
        "standing": "READ-ONLY whole-tree comparison of this author's working copy against the "
                    "frozen32 subject. Not a custody claim over frozen32 itself, which remains the "
                    "root retainer's.",
        "frozen": {"root": str(FROZEN), "files": len(a), "bytes": sum(v[0] for v in a.values())},
        "working": {"root": str(WORK), "files": len(b), "bytes": sum(v[0] for v in b.values())},
        "changedFiles": [
            {"path": k, "frozenSha256": a[k][1], "workingSha256": b[k][1],
             "frozenBytes": a[k][0], "workingBytes": b[k][0]}
            for k in changed
        ],
        "addedFiles": added,
        "removedFiles": removed,
        "changedCount": len(changed),
        "addedCount": len(added),
        "removedCount": len(removed),
    }
    (HERE / "tree-delta.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "frozenFiles": out["frozen"]["files"], "frozenBytes": out["frozen"]["bytes"],
        "workingFiles": out["working"]["files"], "workingBytes": out["working"]["bytes"],
        "changed": changed, "added": added, "removed": removed,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
