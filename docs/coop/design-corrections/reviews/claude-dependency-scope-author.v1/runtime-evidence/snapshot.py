#!/usr/bin/env python3
"""BEFORE/AFTER images and SHA256 of the three owned files, against frozen35 and its manifest."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/dependency-scope-successor.v1/source")
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v35")
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v35.json")
MANIFEST_SHA = "eb45c22b88a428887672d729be6645abf7d4d175474313d0909c8307d7966c85"
TARGETS = [
    "docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md",
    "docs/coop/design-corrections/foundation/atom_model.v1.py",
    "docs/coop/design-corrections/foundation/check-atoms.v1.py",
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(phase):
    raw = MANIFEST.read_bytes()
    man = {f["path"]: f["sha256"] for f in json.loads(raw)["files"]}
    out = HERE / phase
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for rel in TARGETS:
        p = SRC / rel
        flat = rel.replace("/", "__")
        shutil.copy2(p, out / flat)
        rows.append({"path": rel, "bytes": p.stat().st_size, "sha256": sha(p),
                     "frozen35Sha256": sha(FROZEN / rel), "manifestSha256": man.get(rel),
                     "equalsFrozen35": sha(p) == sha(FROZEN / rel), "image": str(out / flat)})
    doc = {"manifestSha256": hashlib.sha256(raw).hexdigest(),
           "manifestShaMatchesDeclared": hashlib.sha256(raw).hexdigest() == MANIFEST_SHA, "files": rows}
    (HERE / f"{phase}-hashes.json").write_text(json.dumps(doc, indent=2) + "\n")
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
