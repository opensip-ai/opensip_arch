#!/usr/bin/env python3
"""p02: exact v10 -> v11 manifest diff, treated as the assertion set to test."""
import hashlib
import json

BASE = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews"


def load(v):
    raw = open(f"{BASE}/candidate-subject.{v}.json", "rb").read()
    return hashlib.sha256(raw).hexdigest(), json.loads(raw)


s10, m10 = load("v10")
s11, m11 = load("v11")

a = {e["path"]: (e["sha256"], e["bytes"]) for e in m10["files"]}
b = {e["path"]: (e["sha256"], e["bytes"]) for e in m11["files"]}

added = sorted(set(b) - set(a))
removed = sorted(set(a) - set(b))
changed = sorted(p for p in set(a) & set(b) if a[p][0] != b[p][0])
same = sorted(set(a) & set(b) - set(changed))

out = {
    "v10ManifestSha256": s10,
    "v11ManifestSha256": s11,
    "v11PredecessorDeclared": m11.get("predecessorManifestSha256"),
    "predecessorChainOk": m11.get("predecessorManifestSha256") == s10,
    "v10FileCount": len(a),
    "v11FileCount": len(b),
    "added": [{"path": p, "sha256": b[p][0], "bytes": b[p][1]} for p in added],
    "removed": [{"path": p, "sha256": a[p][0], "bytes": a[p][1]} for p in removed],
    "changed": [
        {
            "path": p,
            "oldSha256": a[p][0], "newSha256": b[p][0],
            "oldBytes": a[p][1], "newBytes": b[p][1],
            "byteDelta": b[p][1] - a[p][1],
        }
        for p in changed
    ],
    "unchangedCount": len(same),
    "totalTouched": len(added) + len(removed) + len(changed),
}
print(json.dumps(out, indent=2))
