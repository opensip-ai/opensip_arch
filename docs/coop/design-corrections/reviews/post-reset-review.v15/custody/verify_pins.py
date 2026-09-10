#!/usr/bin/env python3
"""Independently verify every transitive pin in the four live pin manifests.

Reads the pin manifests from the subject (or a copy) and recomputes each pinned
file's SHA256 from the actual bytes at the pinned path. Does NOT re-pin.
"""
import hashlib
import json
import os
import sys

ROOT = sys.argv[1].rstrip("/")
BASE = os.path.join(ROOT, "docs/coop/design-corrections")

PIN_FILES = [
    "foundation/source-pins.v1.json",
    "workflows/source-pins.v1.json",
    "native/source-pins.v2.json",
    "security/source-pins.v1.json",
]


def entries(doc):
    """Yield (path, sha256) pairs regardless of which of the two shapes is used."""
    if "files" in doc:
        raw = doc["files"]
    else:
        raw = doc["pins"]
    if isinstance(raw, dict):
        for k, v in raw.items():
            yield k, (v if isinstance(v, str) else (v.get("sha256") or v.get("hash")))
    else:
        for e in raw:
            yield (e.get("path") or e.get("file")), (e.get("sha256") or e.get("hash"))


def main():
    out = {"root": ROOT, "byFile": {}, "totalPinsChecked": 0,
           "stale": 0, "missing": 0, "staleDetail": [], "missingDetail": []}
    for pf in PIN_FILES:
        doc = json.load(open(os.path.join(BASE, pf)))
        n = st = ms = 0
        for rel, exp in entries(doc):
            n += 1
            # Pin paths are repo-root relative in these manifests.
            cand = os.path.join(ROOT, rel)
            if not os.path.isfile(cand):
                # try relative to the pin file's own directory
                cand2 = os.path.join(BASE, os.path.dirname(pf), rel)
                cand = cand2 if os.path.isfile(cand2) else cand
            if not os.path.isfile(cand):
                ms += 1
                out["missingDetail"].append({"pinFile": pf, "path": rel})
                continue
            got = hashlib.sha256(open(cand, "rb").read()).hexdigest()
            if got != exp:
                st += 1
                out["staleDetail"].append(
                    {"pinFile": pf, "path": rel, "pinned": exp, "actual": got})
        out["byFile"][pf] = n
        out["totalPinsChecked"] += n
        out["stale"] += st
        out["missing"] += ms
    out["rePinnedByMe"] = False
    out["CLEAN"] = out["stale"] == 0 and out["missing"] == 0
    print(json.dumps(out, indent=2))
    return 0 if out["CLEAN"] else 1


if __name__ == "__main__":
    sys.exit(main())
