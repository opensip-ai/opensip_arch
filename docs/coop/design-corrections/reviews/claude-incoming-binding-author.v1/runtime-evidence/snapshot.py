#!/usr/bin/env python3
"""BEFORE/AFTER images and SHA256 of the three owned files, compared to frozen34 and its manifest."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/incoming-binding-successor.v1/source")
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v34")
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/"
                "candidate-subject.v34.json")
MANIFEST_SHA = "bd00c07d910e1fa7769b0aab5b180a96e984a255df849b5a96dc563ccbf8f3c6"
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
                     "frozen34Sha256": sha(FROZEN / rel), "manifestSha256": man.get(rel),
                     "equalsFrozen34": sha(p) == sha(FROZEN / rel),
                     "image": str(out / flat)})
    doc = {"manifestSha256": hashlib.sha256(raw).hexdigest(),
           "manifestShaMatchesDeclared": hashlib.sha256(raw).hexdigest() == MANIFEST_SHA,
           "files": rows}
    (HERE / f"{phase}-hashes.json").write_text(json.dumps(doc, indent=2) + "\n")
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
