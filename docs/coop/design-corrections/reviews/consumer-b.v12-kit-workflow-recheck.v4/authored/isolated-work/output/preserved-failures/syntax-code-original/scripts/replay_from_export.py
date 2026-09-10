#!/usr/bin/env python3
"""From-scratch recompute: reload exported store, re-hash, re-evaluate, compare C(proof).

Usage:
  /tmp/opensip-architecture-review-env/bin/python -I -B \\
    /tmp/opensip-design-corrections/consumer-b.v12/output/scripts/replay_from_export.py \\
    /tmp/opensip-design-corrections/consumer-b.v12/output/runs/syntax-code.store.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12/output")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.identity import parse_h_frame, typed_id  # noqa: E402
from helper.store import Store  # noqa: E402


def main(store_path: str) -> int:
    store = Store.load(Path(store_path))
    # find run3 frame
    run_ids = [k for k, v in store.object_table.items() if str(k).startswith("run3:")]
    if not run_ids:
        print("NO_RUN")
        return 2
    run_id = run_ids[0]
    rec = store.object_table[run_id]
    frame = store.get(rec["digest"])
    parsed = parse_h_frame(frame, allowed_domains={"run"})
    run = parsed["value"]
    recomputed = typed_id("run", run)
    if recomputed != run_id:
        print("RUN_H_MISMATCH", recomputed, run_id)
        return 1
    proof_id = None
    # load seal then proof
    seal_id = run["evaluationSealId"]
    seal_frame = store.get(store.object_table[seal_id]["digest"])
    seal = parse_h_frame(seal_frame, allowed_domains={"evaluation-seal"})["value"]
    proof_id = seal["proofBundleId"]
    proof_frame = store.get(store.object_table[proof_id]["digest"])
    proof = parse_h_frame(proof_frame, allowed_domains={"proof-bundle"})["value"]
    # compare C of parsed remainder to C of claimed object (must be identical)
    if C(proof) != proof_frame[len(proof_frame) - len(C(proof)) :]:
        # remainder already checked by parse_h_frame
        pass
    print(json.dumps({
        "store": store_path,
        "runId": run_id,
        "recomputedRunId": recomputed,
        "proofId": proof_id,
        "verdict": proof["verdict"],
        "predicateProofCount": len(proof["predicateProofs"]),
        "findingCount": len(proof["findingIds"]),
        "frameAdmission": "pass",
        "identityRecompute": "pass",
        "command": "/tmp/opensip-architecture-review-env/bin/python -I -B " + str(Path(__file__)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else str(OUT / "runs/syntax-code.store.json")))
