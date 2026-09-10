#!/usr/bin/env python3
"""p18: is the completed v10 review preserved verbatim inside frozen v11?

Executed during the review as a heredoc; retained here as the exact code that produced
logs/p18-prior-review-preservation.json. Compares every file of the embedded
reviews/post-reset-review.v10 tree against the original in the repository, and confirms the
enforcement-removal probe, harness instrumentation and failed attempts are retained with scope.
"""
import hashlib
import json
import os

V11 = "/tmp/opensip-design-corrections/candidate-subject.v11"
REPO = "/Users/sb/code/opensip-ai/opensip_arch"
REL = "docs/coop/design-corrections/reviews/post-reset-review.v10"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


rows, missing, mismatch = [], [], []
base = os.path.join(V11, REL)
for dirpath, _, files in os.walk(base):
    for n in files:
        f = os.path.join(dirpath, n)
        rel = os.path.relpath(f, base)
        r = os.path.join(REPO, REL, rel)
        if not os.path.isfile(r):
            missing.append(rel)
            continue
        a, b = sha(f), sha(r)
        if a != b:
            mismatch.append({"path": rel, "frozen": a, "repo": b})
        rows.append(rel)

out = {
    "frozenFileCount": len(rows),
    "missingFromRepo": missing,
    "digestMismatch": mismatch,
    "preservedVerbatim": not missing and not mismatch,
    "reviewJsonSha": sha(os.path.join(base, "review.json")),
    "reviewJsonMatchesDeclared": sha(os.path.join(base, "review.json"))
    == "64e15aff50d77f0f84b53c145acc6a46d208afe0a1e090272d5deaf25ca3e8f9",
    "custodyPresent": os.path.isfile(os.path.join(base, "custody.json")),
}
work = os.path.join(base, "work")
probes = os.path.join(base, "probes")
out["workArtifacts"] = sorted(os.listdir(work))[:40] if os.path.isdir(work) else None
out["probeArtifacts"] = sorted(os.listdir(probes))[:40] if os.path.isdir(probes) else None
print(json.dumps(out, indent=2))
