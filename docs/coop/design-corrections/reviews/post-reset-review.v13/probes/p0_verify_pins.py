#!/usr/bin/env python
"""Independent transitive-pin verification, run BEFORE the reference commands.

The prior v11 cycle failed with two stale pins. A checker that verifies its own
pins is only as good as the ledger; I verify every pin in every ledger myself,
against the copy I am about to run, and I also report pins whose target is
absent from the subject manifest entirely.
"""
import hashlib
import json
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else (
    "/tmp/opensip-design-corrections/post-reset-review.v13/work/subject-copy")
LEDGERS = [
    "docs/coop/design-corrections/foundation/source-pins.v1.json",
    "docs/coop/design-corrections/native/source-pins.v2.json",
    "docs/coop/design-corrections/workflows/source-pins.v1.json",
    "docs/coop/design-corrections/security/source-pins.v1.json",
]


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rows(doc):
    for key in ("files", "pins"):
        if isinstance(doc.get(key), list):
            for row in doc[key]:
                if isinstance(row, dict) and "path" in row and "sha256" in row:
                    yield row


def main():
    out = {"root": ROOT, "ledgers": {}, "totalPins": 0, "mismatch": [],
           "missing": [], "distinctTargets": set()}
    for led in LEDGERS:
        full = os.path.join(ROOT, led)
        doc = json.load(open(full))
        n = 0
        for row in rows(doc):
            n += 1
            out["totalPins"] += 1
            out["distinctTargets"].add(row["path"])
            target = os.path.join(ROOT, row["path"])
            if not os.path.isfile(target):
                out["missing"].append({"ledger": led, "path": row["path"]})
                continue
            actual = digest(target)
            if actual != row["sha256"]:
                out["mismatch"].append({
                    "ledger": led, "path": row["path"],
                    "pinned": row["sha256"], "actual": actual})
        out["ledgers"][led] = {"pinCount": n, "ledgerSha256": digest(full)}
    out["distinctTargets"] = len(out["distinctTargets"])
    out["clean"] = not out["mismatch"] and not out["missing"]
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["clean"] else 1


if __name__ == "__main__":
    sys.exit(main())
