#!/usr/bin/env python3
"""p04: systematic audit of EVERY source pin in the frozen v11 subject.

Independent of the candidate's own pin-checking scripts: reads each pin ledger, recomputes the
digest of each pinned path from the FROZEN bytes, and reports every stale/missing pin. Also
reports the v10 digest for each stale pin, to show whether the pin is simply a not-refreshed
predecessor value.
"""
import hashlib
import json
import os

V11 = "/tmp/opensip-design-corrections/candidate-subject.v11"
V10 = "/tmp/opensip-design-corrections/candidate-subject.v10"
LEDGERS = [
    "docs/coop/design-corrections/foundation/source-pins.v1.json",
    "docs/coop/design-corrections/security/source-pins.v1.json",
    "docs/coop/design-corrections/native/source-pins.v2.json",
    "docs/coop/design-corrections/workflows/source-pins.v1.json",
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


def collect(obj, out):
    """Find every {path, sha256} record anywhere in the ledger structure."""
    if isinstance(obj, dict):
        if isinstance(obj.get("path"), str) and isinstance(obj.get("sha256"), str):
            out.append((obj["path"], obj["sha256"]))
        for v in obj.values():
            collect(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect(v, out)


report = {"ledgers": [], "totalPins": 0, "totalStale": 0, "totalMissing": 0}
for ledger in LEDGERS:
    pins = []
    collect(json.load(open(os.path.join(V11, ledger))), pins)
    stale, missing = [], []
    for path, pinned in pins:
        actual = sha(os.path.join(V11, path))
        if actual is None:
            missing.append(path)
        elif actual != pinned:
            stale.append({
                "path": path,
                "pinned": pinned,
                "actualV11": actual,
                "v10Digest": sha(os.path.join(V10, path)),
                "pinEqualsV10": pinned == sha(os.path.join(V10, path)),
            })
    report["ledgers"].append({
        "ledger": ledger,
        "ledgerSha256": sha(os.path.join(V11, ledger)),
        "pinCount": len(pins),
        "staleCount": len(stale),
        "missingCount": len(missing),
        "stale": stale,
        "missing": missing,
    })
    report["totalPins"] += len(pins)
    report["totalStale"] += len(stale)
    report["totalMissing"] += len(missing)

report["ALL_PINS_CURRENT"] = report["totalStale"] == 0 and report["totalMissing"] == 0
print(json.dumps(report, indent=2))
