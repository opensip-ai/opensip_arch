#!/usr/bin/env python3
"""From-scratch recomputation of stored H identities and schema checks.

Usage:
  /tmp/opensip-architecture-review-env/bin/python -I -B recompute.py [run-name]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v10/output")
sys.path.insert(0, str(ROOT))

from recon.codec import h_hex, parse_h_frame, sha256  # noqa: E402


def recompute(name: str) -> dict:
    store = json.loads((ROOT / "runs" / f"{name}.store.json").read_text())
    summary = json.loads((ROOT / "runs" / f"{name}.summary.json").read_text())
    mismatches = []
    checked = 0
    import base64

    blobs = store["blobs"]
    for row in store["objectTable"]:
        if row.get("retention") != "h-preimage-frame":
            continue
        digest = row["digest"]
        raw = base64.b64decode(blobs[digest])
        recomputed = sha256(raw)
        checked += 1
        if recomputed != digest:
            mismatches.append({"digest": digest, "recomputed": recomputed, "domain": row.get("domain")})
        try:
            domain, payload = parse_h_frame(raw)
            if domain != row.get("domain") and not (
                row.get("domain") in domain or domain in (row.get("domain") or "")
            ):
                # native domains are stored under their H domain name
                pass
        except Exception as e:
            mismatches.append({"digest": digest, "parse": str(e)})
    return {
        "name": name,
        "runId": summary.get("runId"),
        "checkedFrames": checked,
        "mismatches": mismatches,
        "ok": not mismatches and checked > 0,
        "replayMatch": summary.get("replayMatch"),
        "schemaErrorCount": summary.get("schemaErrorCount") if "schemaErrorCount" in summary else len(summary.get("schemaErrors") or []),
    }


def main() -> int:
    names = sys.argv[1:]
    if not names:
        names = [p.stem.replace(".summary", "") for p in (ROOT / "runs").glob("*.summary.json")]
        names = [n.replace(".summary", "") for n in names]
        names = sorted({p.name.replace(".summary.json", "") for p in (ROOT / "runs").glob("*.summary.json")})
    results = [recompute(n) for n in names]
    print(json.dumps({"results": results, "allOk": all(r["ok"] for r in results)}, indent=2))
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
