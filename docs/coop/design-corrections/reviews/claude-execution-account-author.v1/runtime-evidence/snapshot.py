#!/usr/bin/env python3
"""Snapshot BEFORE/AFTER images and SHA256 of the bounded owned files.

`python snapshot.py before` copies each target into ./before/ and records hashes.
`python snapshot.py after`  copies each target into ./after/ and records hashes.
Nothing outside this runtime is written.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source")

TARGETS = [
    "docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md",
    "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
    "docs/coop/design-corrections/foundation/execution_inputs_model.v1.py",
    "docs/coop/design-corrections/foundation/check-execution-inputs.v1.py",
    "docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py",
    "docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py",
    "docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py",
    "docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md",
    "docs/coop/design-corrections/foundation/check-composition.v3.py",
    "docs/coop/design-corrections/foundation/enumeration-contract.v1.md",
    "docs/v2/contracts/product-v1/native-evidence.md",
]


def main(phase: str) -> int:
    out = HERE / phase
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for rel in TARGETS:
        src = SRC / rel
        raw = src.read_bytes()
        flat = rel.replace("/", "__")
        (out / flat).write_bytes(raw)
        rows.append({
            "path": rel,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "image": str(out / flat),
        })
    (HERE / f"{phase}-hashes.json").write_text(json.dumps(rows, indent=2) + "\n")
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
