#!/usr/bin/env python3
"""Snapshot BEFORE/AFTER images and SHA256 for v2.

BEFORE for v2 is the FINAL v1 handoff state of the isolated source copy, which is also compared to
frozen33 so both baselines stay visible in one record. v1 evidence is read, never written.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source")
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v33")
V1_AFTER = Path("/tmp/opensip-design-corrections/claude-atom-cause-author.v1/after-hashes.json")

TARGETS = [
    "docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md",
    "docs/coop/design-corrections/foundation/atom_model.v1.py",
    "docs/coop/design-corrections/foundation/check-atoms.v1.py",
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(phase):
    v1 = {r["path"]: r["sha256"] for r in json.loads(V1_AFTER.read_text())}
    out = HERE / phase
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for rel in TARGETS:
        p = SRC / rel
        flat = rel.replace("/", "__")
        shutil.copy2(p, out / flat)
        rows.append({"path": rel, "bytes": p.stat().st_size, "sha256": sha(p),
                     "v1FinalSha256": v1.get(rel),
                     "equalsV1Final": sha(p) == v1.get(rel),
                     "frozen33Sha256": sha(FROZEN / rel),
                     "equalsFrozen33": sha(p) == sha(FROZEN / rel),
                     "image": str(out / flat)})
    (HERE / f"{phase}-hashes.json").write_text(json.dumps(rows, indent=2) + "\n")
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
