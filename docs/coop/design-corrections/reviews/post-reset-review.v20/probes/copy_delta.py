"""Exact deltas the six canonical commands produced in the disposable copy.

Unchanged bytes reconstruct from the frozen subject, so only CHANGED/ADDED/REMOVED
paths are retained here, with before/after digests.
"""
import hashlib
import json
import os
import sys

SNAP, COPY = sys.argv[1], sys.argv[2]


def index(root):
    out = {}
    for dp, _d, fs in os.walk(root):
        for fn in fs:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, root)
            try:
                out[rel] = hashlib.sha256(open(p, "rb").read()).hexdigest()
            except OSError:
                pass
    return out


a, b = index(SNAP), index(COPY)
changed = [{"path": k, "frozen": a[k], "afterRun": b[k]}
           for k in a.keys() & b.keys() if a[k] != b[k]]
added = sorted(b.keys() - a.keys())
removed = sorted(a.keys() - b.keys())

print(json.dumps({
    "frozenFileCount": len(a),
    "copyFileCount": len(b),
    "changedCount": len(changed),
    "changed": sorted(changed, key=lambda x: x["path"]),
    "addedCount": len(added),
    "added": added[:50],
    "removedCount": len(removed),
    "removed": removed[:50],
    "note": "Unchanged bytes are reconstructable from the frozen subject and are "
            "not retained.",
}, indent=2))
