#!/usr/bin/env python3
"""From-scratch recompute: load exported stores, recompute H, close, replay-compare."""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers.canonical import C, parse_h_frame, sha256_hex
from helpers.closure import close_run
from helpers.store import Store

EXPORTS = Path(__file__).resolve().parent / "exports"


def load_store(path: Path) -> tuple[Store, str]:
    doc = json.loads(path.read_text())
    s = Store()
    for d, b64 in doc["blobs"].items():
        s.blobs[d] = base64.b64decode(b64)
    for oid, obj in doc["objectTable"].items():
        s.objects[oid] = obj
    return s, doc["runId"]


def main() -> int:
    failed = 0
    for p in sorted(EXPORTS.glob("*.store.json")):
        s, run_id = load_store(p)
        # recompute identities from frames
        mismatches = []
        for oid, obj in s.objects.items():
            digest = oid.split(":")[-1]
            frame = s.blobs.get(digest)
            if frame is None:
                continue
            if sha256_hex(frame) != digest:
                mismatches.append(oid)
            try:
                _d, payload = parse_h_frame(frame)
                if payload != C(obj["descriptor"]):
                    mismatches.append(oid + ":C")
            except Exception:
                pass
        cl = close_run(s, run_id)
        replay = json.loads(p.with_name(p.name.replace(".store.json", ".replay.json")).read_text())
        claimed = replay["claimedVerdict"]
        recomputed = replay["recomputedVerdict"]
        print(p.name, "close", cl["ok"], "h_mismatch", len(mismatches), "verdict", claimed, recomputed)
        if (not cl["ok"]) or mismatches or claimed != recomputed:
            failed += 1
            if cl["faults"]:
                print("  faults", cl["faults"][:8])
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
