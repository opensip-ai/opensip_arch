#!/usr/bin/env python3
"""Snapshot BEFORE/AFTER images and SHA256 for the v2 follow-up.

BEFORE here means "the v1 handoff bytes", i.e. the state of the source at the start of this
follow-up. The v1 runtime's own before/after images are never touched.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source")
V1 = Path("/tmp/opensip-design-corrections/claude-execution-account-author.v1")

TARGETS = [
    "docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md",
    "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
    "docs/coop/design-corrections/foundation/execution_inputs_model.v1.py",
    "docs/coop/design-corrections/foundation/check-execution-inputs.v1.py",
    "docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py",
    "docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py",
    "docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md",
    "docs/coop/design-corrections/foundation/enumeration-contract.v1.md",
    "docs/v2/contracts/product-v1/native-evidence.md",
]


def main(phase: str) -> int:
    out = HERE / phase
    out.mkdir(parents=True, exist_ok=True)
    frozen32 = {}
    rows = []
    for rel in TARGETS:
        raw = (SRC / rel).read_bytes()
        flat = rel.replace("/", "__")
        (out / flat).write_bytes(raw)
        row = {
            "path": rel,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "image": str(out / flat),
        }
        rows.append(row)
    # Cross-check against the v1 handoff hashes so the v2 BEFORE is provably the v1 AFTER.
    v1_after = {r["path"]: r for r in json.loads((V1 / "after-hashes.json").read_text())}
    for row in rows:
        v1 = v1_after.get(row["path"])
        row["v1AfterSha256"] = v1["sha256"] if v1 else None
        row["equalsV1After"] = bool(v1) and v1["sha256"] == row["sha256"]
    _ = frozen32
    (HERE / f"{phase}-hashes.json").write_text(json.dumps(rows, indent=2) + "\n")
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
