"""Verify all four source-pin ledgers against the frozen subject bytes.

Each ledger pins product-contract / schema source documents by sha256. A pin that
no longer matches means the unit's checks were validated against different bytes
than the ones under review.
"""
import hashlib
import json
import os
import sys

ROOT = sys.argv[1]
LEDGERS = [
    "docs/coop/design-corrections/foundation/source-pins.v1.json",
    "docs/coop/design-corrections/security/source-pins.v1.json",
    "docs/coop/design-corrections/native/source-pins.v2.json",
    "docs/coop/design-corrections/workflows/source-pins.v1.json",
]


def walk_pins(obj, path=""):
    """Yield (label, relpath, sha256) for any dict carrying a path+sha256 pair."""
    if isinstance(obj, dict):
        p = obj.get("path") or obj.get("file") or obj.get("source")
        h = obj.get("sha256") or obj.get("digest") or obj.get("sha256Digest")
        if isinstance(p, str) and isinstance(h, str) and len(h) == 64:
            yield (path, p, h)
        for k, v in obj.items():
            if isinstance(v, str) and len(v) == 64 and all(
                c in "0123456789abcdef" for c in v
            ) and k not in ("sha256", "digest", "sha256Digest"):
                # key-as-path form: {"docs/x.md": "<sha>"}
                if "/" in k or k.endswith(".json") or k.endswith(".md"):
                    yield (path, k, v)
            yield from walk_pins(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_pins(v, f"{path}[{i}]")


results = []
for led in LEDGERS:
    full = os.path.join(ROOT, led)
    doc = json.load(open(full))
    pins = list(walk_pins(doc))
    ok, bad, missing = 0, [], []
    seen = set()
    for label, rel, exp in pins:
        key = (rel, exp)
        if key in seen:
            continue
        seen.add(key)
        target = os.path.join(ROOT, rel)
        if not os.path.isfile(target):
            missing.append({"at": label, "path": rel, "declared": exp})
            continue
        actual = hashlib.sha256(open(target, "rb").read()).hexdigest()
        if actual == exp:
            ok += 1
        else:
            bad.append(
                {"at": label, "path": rel, "declared": exp, "actual": actual}
            )
    results.append(
        {
            "ledger": led,
            "ledgerSha256": hashlib.sha256(open(full, "rb").read()).hexdigest(),
            "distinctPins": len(seen),
            "verifiedOk": ok,
            "mismatchCount": len(bad),
            "mismatches": bad,
            "missingCount": len(missing),
            "missing": missing,
        }
    )

print(json.dumps({"root": ROOT, "ledgers": results}, indent=2))
