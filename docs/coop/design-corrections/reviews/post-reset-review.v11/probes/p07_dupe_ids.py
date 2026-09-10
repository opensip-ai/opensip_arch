#!/usr/bin/env python3
"""p07: duplicate check ids, and failure attribution recomputed from the LIST not a dict.

p06 keyed checks by id; unique ids (663) were fewer than the reported pass count (673), so
duplicate ids exist. If a duplicated id ever had one passing and one failing instance, a
dict-keyed reading could hide the failure. Recompute honestly from the ordered list.
"""
import collections
import json
import os
import subprocess

PY = "/tmp/opensip-architecture-review-env/bin/python"
WORK = "/tmp/opensip-design-corrections/post-reset-review.v11/copies/discriminate"
DC = "docs/coop/design-corrections"

out = {}
for tag in ("A_v11check_v11model", "B_v11check_v10model", "C_v10check_v10model"):
    dst = os.path.join(WORK, tag)
    rep = os.path.join(dst, "out.json")
    if not os.path.isfile(rep):
        subprocess.run([PY, "-I", "-B", os.path.join(dst, DC, "foundation/check-identity.py"),
                        "--report", rep], cwd=dst, capture_output=True, text=True)
    checks = json.load(open(rep))["checks"]
    counter = collections.Counter(c["id"] for c in checks)
    dupes = {k: v for k, v in counter.items() if v > 1}
    # any id where instances disagree -> a dict-keyed reading could hide a failure
    by_id = collections.defaultdict(set)
    for c in checks:
        by_id[c["id"]].add(bool(c["passed"]))
    inconsistent = sorted(k for k, v in by_id.items() if len(v) > 1)
    out[tag] = {
        "instances": len(checks),
        "uniqueIds": len(counter),
        "duplicateIdCount": len(dupes),
        "duplicateExtraInstances": sum(v - 1 for v in dupes.values()),
        "duplicateIds": dict(sorted(dupes.items(), key=lambda kv: -kv[1])),
        "idsWithDisagreeingInstances": inconsistent,
        "failedInstances": sorted(c["id"] for c in checks if not c["passed"]),
        "passedTotal": sum(1 for c in checks if c["passed"]),
    }
print(json.dumps(out, indent=2))
