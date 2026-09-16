#!/usr/bin/env python3
"""BEFORE/AFTER images and SHA256 of the three owned files, against frozen35 and the dependency-scope successor."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/dependency-totality-successor.v1/source")
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v35")
SCOPE = Path("/tmp/opensip-design-corrections/dependency-scope-successor.v1/source")
TARGETS = [
    "docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md",
    "docs/coop/design-corrections/foundation/atom_model.v1.py",
    "docs/coop/design-corrections/foundation/check-atoms.v1.py",
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(phase):
    out = HERE / phase
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for rel in TARGETS:
        p = SRC / rel
        flat = rel.replace("/", "__")
        shutil.copy2(p, out / flat)
        rows.append({"path": rel, "bytes": p.stat().st_size, "sha256": sha(p),
                     "frozen35Sha256": sha(FROZEN / rel), "dependencyScopeSuccessorSha256": sha(SCOPE / rel),
                     "equalsDependencyScopeSuccessor": sha(p) == sha(SCOPE / rel), "image": str(out / flat)})
    (HERE / f"{phase}-hashes.json").write_text(json.dumps({"files": rows}, indent=2) + "\n")
    print(json.dumps({"files": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
