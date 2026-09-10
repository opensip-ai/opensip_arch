#!/usr/bin/env python
"""Corrected governance cross-reference scan.

Fixes two defects in my first pass (p09):
  1. custody/handoff records use RECORD-RELATIVE paths; resolve relative to the
     record's own directory as well as the repo root.
  2. a pin inside a key named `originalFinding` / `beforeSha256` / `v5Sha256`
     etc. is an AS-OF-THEN pin by construction and is classified as historical,
     not unresolved - but it must still resolve to SOME real prior state, so it
     is reported separately rather than silently dropped.
"""
import hashlib
import json
import os
import re
import sys

ROOT = "/tmp/opensip-design-corrections/candidate-subject.v17"
OUT = sys.argv[1]
HEX64 = re.compile(r"^[0-9a-f]{64}$")

RECORDS = [
    "docs/coop/design-corrections/post-reset-dispositions.v17.proposed.json",
    "docs/coop/design-corrections/reviews/codex-post-reset.v1/successor-source-assessment.v17.json",
    "docs/coop/design-corrections/reviews/codex-post-reset.v1/blind-assessment.v6.json",
    "docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v17/reference-checks.json",
    "docs/coop/design-corrections/reviews/codex-post-reset.v1/advisory-application-account.v17.proposed.json",
    "docs/coop/design-corrections/reviews/codex-post-reset.v1/identity-check-counts.v17.json",
    "docs/coop/design-corrections/historical-preservation-report.v17.json",
    "docs/coop/design-corrections/correction-crosswalk.proposed.json",
    "docs/coop/design-corrections/reviews/bv6-corrections-author.v6/handoff.json",
    "docs/coop/design-corrections/reviews/bv6-corrections-author.v6/custody.json",
]

HISTORICAL_KEYS = {"beforeSha256", "v5Sha256", "v16Sha256", "frozen16",
                   "predecessorManifestSha256", "priorSha256"}
HISTORICAL_PARENT_KEYS = {"originalFinding", "originalCoauthorDisposition",
                          "sourceEvidence", "subsequentCorrectionEvidence",
                          "coauthorDisposition"}


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


rep = {"records": []}
current_ok = historical = notfound = mismatch = 0
problems = []
hist_rows = []


def scan(obj, record, recdir, ptr="", parents=()):
    global current_ok, historical, notfound, mismatch
    if isinstance(obj, dict):
        pk = next((k for k in ("path", "file", "source")
                   if isinstance(obj.get(k), str)), None)
        sks = [k for k in obj
               if isinstance(obj.get(k), str) and HEX64.match(obj[k])
               and ("sha" in k.lower() or "digest" in k.lower())]
        if pk:
            for sk in sks:
                path, sha = obj[pk], obj[sk]
                cands = [os.path.join(ROOT, path),
                         os.path.join(recdir, path),
                         os.path.join(ROOT, "docs/coop/design-corrections", path)]
                full = next((c for c in cands if os.path.isfile(c)), None)
                is_hist = (sk in HISTORICAL_KEYS
                           or any(p in HISTORICAL_PARENT_KEYS for p in parents))
                if full is None:
                    notfound += 1
                    problems.append({"record": record, "pointer": ptr,
                                     "path": path, "key": sk,
                                     "problem": "path not found"})
                    continue
                actual = sha_file(full)
                if actual == sha:
                    current_ok += 1
                elif is_hist:
                    historical += 1
                    hist_rows.append({"record": record, "pointer": ptr,
                                      "path": path, "key": sk,
                                      "pinned": sha, "currentFrozen": actual,
                                      "classifiedAs":
                                          "as-of-then pin under key '%s'" % sk
                                          if sk in HISTORICAL_KEYS else
                                          "as-of-then pin inside a historical "
                                          "parent key"})
                else:
                    mismatch += 1
                    problems.append({"record": record, "pointer": ptr,
                                     "path": path, "key": sk,
                                     "declared": sha, "actual": actual,
                                     "problem": "digest does not resolve and is "
                                                "NOT marked historical"})
        for k, v in obj.items():
            scan(v, record, recdir, ptr + "/" + str(k), parents + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan(v, record, recdir, ptr + "/" + str(i), parents)


for rel in RECORDS:
    p = os.path.join(ROOT, rel)
    if not os.path.isfile(p):
        rep["records"].append({"record": rel, "present": False})
        continue
    rep["records"].append({"record": rel, "present": True,
                           "sha256": sha_file(p)})
    with open(p) as fh:
        doc = json.load(fh)
    scan(doc, rel, os.path.dirname(p))

rep.update({
    "currentPinsResolved": current_ok,
    "historicalAsOfPins": historical,
    "unresolvedNotMarkedHistorical": mismatch,
    "pathsNotFound": notfound,
    "problems": problems,
    "historicalRows": hist_rows,
    "allCurrentPinsResolve": mismatch == 0 and notfound == 0,
})

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True)

print("current pins resolved     :", current_ok)
print("historical as-of pins     :", historical)
print("UNRESOLVED (not historical):", mismatch)
print("paths not found           :", notfound)
print()
for p in problems[:25]:
    print("  PROBLEM:", json.dumps(p)[:280])
print()
for h in hist_rows[:15]:
    print("  HISTORICAL:", h["path"], "| key:", h["key"],
          "| pinned", h["pinned"][:12], "vs frozen", h["currentFrozen"][:12])
