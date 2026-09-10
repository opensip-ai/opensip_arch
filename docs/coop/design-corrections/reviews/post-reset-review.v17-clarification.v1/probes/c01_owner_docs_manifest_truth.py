#!/usr/bin/env python
"""Point 1: verify EVERY document I claimed byte-identical against its own actual
manifest entries, and characterise exactly what changed in the crosswalk.

My original arDispositions basis said the crosswalk was byte-identical to v16.
That is factually wrong - my own delta section listed it as changed. This probe
establishes the truth for every owner document I cited, and separates
ORIGINAL OBLIGATION/CONTRACT/SELECTOR preservation from CHANGED ROUTING.
"""
import hashlib
import json
import os
import subprocess
import sys

REV = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews"
SUBJ = "/tmp/opensip-design-corrections/candidate-subject.v17"
V16X = "/tmp/opensip-design-corrections/post-reset-review.v17-clarification.v1/v16x"
OUT = sys.argv[1]

DOCS = [
    "docs/coop/design-corrections/correction-crosswalk.proposed.md",
    "docs/coop/design-corrections/correction-crosswalk.proposed.json",
    "docs/coop/design-corrections/current-source-map.proposed.md",
    "docs/coop/design-corrections/inherited-residuals.proposed.md",
    "docs/coop/design-corrections/inherited-row-sources.proposed.json",
    "docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json",
    "docs/coop/design-corrections/qualification-gates.proposed.json",
    "docs/coop/architecture-depth-review/REVIEW.md",
    "docs/v2/architecture/08-decision-and-readiness-register.md",
]


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


m16 = json.load(open(os.path.join(REV, "candidate-subject.v16.json")))
m17 = json.load(open(os.path.join(REV, "candidate-subject.v17.json")))
a = {f["path"]: f for f in m16["files"]}
b = {f["path"]: f for f in m17["files"]}

rep = {"probe": "c01-owner-docs-manifest-truth", "documents": []}
for rel in DOCS:
    ea, eb = a.get(rel), b.get(rel)
    row = {
        "path": rel,
        "inV16Manifest": ea is not None,
        "inV17Manifest": eb is not None,
        "v16Sha256": ea["sha256"] if ea else None,
        "v17Sha256": eb["sha256"] if eb else None,
        "byteIdenticalPerManifest": bool(ea and eb and ea["sha256"] == eb["sha256"]),
    }
    full = os.path.join(SUBJ, rel)
    if os.path.isfile(full):
        row["frozenSha256"] = sha_file(full)
        row["frozenMatchesV17Manifest"] = row["frozenSha256"] == row["v17Sha256"]
    rep["documents"].append(row)

rep["documentsChanged"] = [d for d in rep["documents"]
                           if d["inV16Manifest"] and not d["byteIdenticalPerManifest"]]
rep["documentsByteIdentical"] = [d for d in rep["documents"]
                                 if d["byteIdenticalPerManifest"]]
rep["documentsAbsentFromManifest"] = [d for d in rep["documents"]
                                      if not d["inV17Manifest"]]

# ---- exact field-level crosswalk comparison ----
os.makedirs(V16X, exist_ok=True)
subprocess.run(
    ["tar", "xzf", os.path.join(REV, "candidate-source.v16.tar.gz"),
     "docs/coop/design-corrections/correction-crosswalk.proposed.json"],
    cwd=V16X, capture_output=True)
old_p = os.path.join(V16X, "docs/coop/design-corrections/correction-crosswalk.proposed.json")
new_p = os.path.join(SUBJ, "docs/coop/design-corrections/correction-crosswalk.proposed.json")
cw = {}
if os.path.isfile(old_p):
    cw["v16ExtractedSha256"] = sha_file(old_p)
    cw["v16ExtractedMatchesManifest"] = (
        cw["v16ExtractedSha256"] == a["docs/coop/design-corrections/"
                                      "correction-crosswalk.proposed.json"]["sha256"])
    old = json.load(open(old_p))
    new = json.load(open(new_p))
    cw["v16TopKeys"] = sorted(old.keys())
    cw["v17TopKeys"] = sorted(new.keys())
    cw["topKeysEqual"] = sorted(old.keys()) == sorted(new.keys())
    oi = {i["id"]: i for i in old["items"]}
    ni = {i["id"]: i for i in new["items"]}
    cw["v16ItemCount"] = len(oi)
    cw["v17ItemCount"] = len(ni)
    cw["itemIdsEqual"] = sorted(oi) == sorted(ni)
    changed_fields = {}
    per_row = {}
    for k in sorted(set(oi) & set(ni)):
        diffs = []
        for f in sorted(set(oi[k]) | set(ni[k])):
            if oi[k].get(f) != ni[k].get(f):
                diffs.append(f)
                changed_fields[f] = changed_fields.get(f, 0) + 1
        per_row[k] = diffs
    cw["perRowChangedFields"] = per_row
    cw["changedFieldHistogram"] = changed_fields
    cw["rowsWithAnyChange"] = [k for k, v in per_row.items() if v]
    cw["rowsWithNoChange"] = [k for k, v in per_row.items() if not v]
    cw["everyRowChangedOnlyRoutingFields"] = all(
        set(v) <= {"latestCompletedReview", "historicalReviews"}
        for v in per_row.values())
    # obligation / contract / selector fields must be untouched
    SUBSTANCE = ["obligation", "selector", "owner", "unit", "contract",
                 "evidence", "ownerRows", "status", "severity", "id",
                 "requirement", "disposition"]
    cw["substantiveFieldsPresent"] = sorted(
        {f for k in ni for f in ni[k] if f in SUBSTANCE})
    cw["substantiveFieldsChanged"] = sorted(
        {f for f in changed_fields if f in SUBSTANCE})
    cw["allSubstantiveFieldsUnchanged"] = not cw["substantiveFieldsChanged"]
rep["crosswalkComparison"] = cw

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

print("=== owner documents vs their OWN manifest entries ===")
for d in rep["documents"]:
    tag = "IDENTICAL" if d["byteIdenticalPerManifest"] else (
        "CHANGED" if d["inV16Manifest"] else "NOT-IN-V16")
    if not d["inV17Manifest"]:
        tag = "NOT IN MANIFEST"
    print("  %-11s %s" % (tag, d["path"]))
    if tag == "CHANGED":
        print("              v16 %s" % d["v16Sha256"])
        print("              v17 %s" % d["v17Sha256"])
print()
print("=== crosswalk exact field comparison ===")
for k in ("v16ExtractedMatchesManifest", "v16ItemCount", "v17ItemCount",
          "itemIdsEqual", "changedFieldHistogram", "rowsWithNoChange",
          "everyRowChangedOnlyRoutingFields", "substantiveFieldsChanged",
          "allSubstantiveFieldsUnchanged"):
    print("  %-36s %s" % (k, json.dumps(cw.get(k))[:200]))
