#!/usr/bin/env python3
"""Recompute the exact v14 -> v15 delta from the two frozen manifests directly.

Deliberately does NOT read any author-supplied delta account.
"""
import json

R = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/"


def load(p):
    m = json.load(open(R + p))
    return m, {e["path"]: (e["sha256"], e["bytes"]) for e in m["files"]}


m14, f14 = load("candidate-subject.v14.json")
m15, f15 = load("candidate-subject.v15.json")

assert m15["predecessorManifestSha256"] is not None
added = sorted(set(f15) - set(f14))
removed = sorted(set(f14) - set(f15))
modified = sorted(p for p in set(f14) & set(f15) if f14[p][0] != f15[p][0])

out = {
    "v14FileCount": m14["fileCount"], "v14TotalBytes": m14["totalBytes"],
    "v15FileCount": m15["fileCount"], "v15TotalBytes": m15["totalBytes"],
    "v15DeclaredPredecessorSha": m15["predecessorManifestSha256"],
    "added": len(added), "removed": len(removed), "modified": len(modified),
    "modifiedPaths": [
        {"path": p, "v14sha": f14[p][0], "v15sha": f15[p][0],
         "v14bytes": f14[p][1], "v15bytes": f15[p][1]}
        for p in modified
    ],
    "removedPaths": removed,
    # Added files that are NOT under a custody/records directory are the ones
    # that could carry new normative surface.
    "addedOutsideKnownRecordDirs": [
        p for p in added
        if "/reviews/" not in p and "/coop/completion/" not in p
    ][:120],
}
print(json.dumps(out, indent=2))
