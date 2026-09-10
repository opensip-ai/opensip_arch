#!/usr/bin/env python
"""Final custody: copy deltas after all execution, and the final pin seal
(all 1308 transitive pins re-verified in the FROZEN subject and in every copy
AFTER all recording).
"""
import hashlib
import json
import os
import sys

REV = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews"
FROZEN = "/tmp/opensip-design-corrections/candidate-subject.v17"
COPIES = "/tmp/opensip-design-corrections/post-reset-review.v17/copies"
OUT = sys.argv[1]

PIN_FILES = [
    "docs/coop/design-corrections/foundation/source-pins.v1.json",
    "docs/coop/design-corrections/native/source-pins.v2.json",
    "docs/coop/design-corrections/security/source-pins.v1.json",
    "docs/coop/design-corrections/workflows/source-pins.v1.json",
]


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def pin_entries(root, rel):
    doc = json.load(open(os.path.join(root, rel)))
    if isinstance(doc, dict):
        if "pins" in doc:
            return doc["pins"]
        if "files" in doc:
            return doc["files"]
    return []


def seal(root, label):
    total = ok = miss = bad = 0
    problems = []
    per = {}
    for rel in PIN_FILES:
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            per[rel] = {"present": False}
            continue
        ents = pin_entries(root, rel)
        n = m = b_ = 0
        for e in ents:
            path, sha = e.get("path"), e.get("sha256")
            if not path or not sha:
                continue
            total += 1
            n += 1
            full = os.path.join(root, path)
            if not os.path.isfile(full):
                miss += 1
                m += 1
                problems.append({"copy": label, "pinFile": rel,
                                 "path": path, "problem": "missing"})
                continue
            if sha_file(full) != sha:
                bad += 1
                b_ += 1
                problems.append({"copy": label, "pinFile": rel, "path": path,
                                 "declared": sha,
                                 "actual": sha_file(full),
                                 "problem": "mismatch"})
            else:
                ok += 1
        per[rel] = {"present": True, "entries": n, "missing": m, "mismatch": b_}
    return {"scope": label, "root": root, "pinsChecked": total, "valid": ok,
            "missing": miss, "mismatch": bad, "perPinFile": per,
            "problems": problems, "sealHolds": miss == 0 and bad == 0}


m = json.load(open(os.path.join(REV, "candidate-subject.v17.json")))
declared = {e["path"]: e for e in m["files"]}

rep = {"finalPinSeal": [], "copyCustody": []}
rep["finalPinSeal"].append(seal(FROZEN, "frozen-subject (immutable, read-only)"))

for name in sorted(os.listdir(COPIES)):
    root = os.path.join(COPIES, name)
    if not os.path.isdir(root) or name == "v16-extract":
        continue
    modified, missing, added = [], [], []
    for p, e in declared.items():
        full = os.path.join(root, p)
        if not os.path.isfile(full):
            missing.append(p)
        elif sha_file(full) != e["sha256"]:
            modified.append(p)
    for dp, _, fns in os.walk(root):
        for fn in fns:
            r = os.path.relpath(os.path.join(dp, fn), root)
            if r not in declared:
                added.append(r)
    rep["copyCustody"].append({
        "copyName": name,
        "copyRoot": root,
        "declared": len(declared),
        "modifiedVsManifest": sorted(modified),
        "missingVsManifest": sorted(missing),
        "addedVsManifest": sorted(added),
        "byteExactVsManifestAfterAllExecution":
            not modified and not missing and not added,
    })
    rep["finalPinSeal"].append(seal(root, "copy:" + name))

# v16-extract is a partial reference extraction, recorded separately
ve = os.path.join(COPIES, "v16-extract")
if os.path.isdir(ve):
    files = []
    for dp, _, fns in os.walk(ve):
        for fn in fns:
            files.append(os.path.relpath(os.path.join(dp, fn), ve))
    rep["v16Extract"] = {
        "root": ve,
        "purpose": "PARTIAL extraction of named v16 files from the repository's "
                   "own candidate-source.v16.tar.gz, used only as the "
                   "before-image for structural diffs. Not a full copy and not "
                   "a subject.",
        "fileCount": len(files),
        "files": sorted(files),
    }

rep["allCopiesByteExactAfterExecution"] = all(
    c["byteExactVsManifestAfterAllExecution"] for c in rep["copyCustody"])
rep["finalSealHoldsEverywhere"] = all(s["sealHolds"] for s in rep["finalPinSeal"])
rep["totalPinsCheckedAcrossAllScopes"] = sum(
    s["pinsChecked"] for s in rep["finalPinSeal"])

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True)

for s in rep["finalPinSeal"]:
    print("%-42s pins=%4d valid=%4d missing=%d mismatch=%d seal=%s"
          % (s["scope"], s["pinsChecked"], s["valid"], s["missing"],
             s["mismatch"], s["sealHolds"]))
print()
for c in rep["copyCustody"]:
    print("%-26s byteExactAfterExecution=%s modified=%d added=%d missing=%d"
          % (c["copyName"], c["byteExactVsManifestAfterAllExecution"],
             len(c["modifiedVsManifest"]), len(c["addedVsManifest"]),
             len(c["missingVsManifest"])))
print()
print("all copies byte-exact after execution:", rep["allCopiesByteExactAfterExecution"])
print("final seal holds everywhere          :", rep["finalSealHoldsEverywhere"])
print("total pins checked across all scopes :", rep["totalPinsCheckedAcrossAllScopes"])
if "v16Extract" in rep:
    print("v16-extract partial reference files  :", rep["v16Extract"]["fileCount"])
