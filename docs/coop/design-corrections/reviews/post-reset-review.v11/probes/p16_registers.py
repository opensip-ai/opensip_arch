#!/usr/bin/env python3
"""p16: independent verification of the register/routing basis for AR, FW, DR and gates.

Establishes, from the frozen v11 bytes:
  - the exact normative-byte scope of the v10->v11 delta (which contract/schema/registry files,
    if any, changed)
  - AR/FW row inventories and statuses in the crosswalk
  - DR-201..205 routing (owner rows of which AR row, and that row's status)
  - the inherited residual row inventory (DR-001..011 and DR-011-R01..R16)
  - all 32 qualification gates and their demonstrated flags over the four platform families
  - the 30 evaluation subresiduals
  - the protected historical files declared unchanged
"""
import hashlib
import json
import os
import re

V10 = "/tmp/opensip-design-corrections/candidate-subject.v10"
V11 = "/tmp/opensip-design-corrections/candidate-subject.v11"
DC = "docs/coop/design-corrections"
BASE = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


out = {}

# ---- normative byte scope of the delta
m10 = {e["path"]: e["sha256"] for e in json.load(
    open(f"{BASE}/candidate-subject.v10.json"))["files"]}
m11 = {e["path"]: e["sha256"] for e in json.load(
    open(f"{BASE}/candidate-subject.v11.json"))["files"]}
changed = sorted(p for p in set(m10) & set(m11) if m10[p] != m11[p])
added = sorted(set(m11) - set(m10))
removed = sorted(set(m10) - set(m11))


def classify(p):
    if p.startswith("docs/v2/contracts/"):
        return "normative-contract"
    if p.startswith("docs/v2/architecture/"):
        return "normative-architecture"
    if p.startswith("docs/catalog/"):
        return "catalog"
    if re.search(r"schemas?\.v\d+\.json$", p) or p.endswith(".schema.json"):
        return "registered-schema"
    if "registry" in os.path.basename(p):
        return "registry"
    return "other"


out["deltaScope"] = {
    "changed": len(changed), "added": len(added), "removed": len(removed),
    "changedByClass": {},
    "normativeChanged": [p for p in changed if classify(p) != "other"],
    "addedNormative": [p for p in added if classify(p) != "other"],
    "removedAny": removed,
}
for p in changed:
    c = classify(p)
    out["deltaScope"]["changedByClass"].setdefault(c, []).append(p)
out["onlyNormativeChangeIsAssessedContract"] = (
    out["deltaScope"]["normativeChanged"]
    == ["docs/v2/contracts/product-v1/identity-and-evidence.md"])
out["noRegisteredSchemaOrRegistryChanged"] = not [
    p for p in changed + added if classify(p) in ("registered-schema", "registry")]

# ---- crosswalk: AR/FW rows and DR-201..205 routing
cw = json.load(open(os.path.join(V11, DC, "correction-crosswalk.proposed.json")))
items = cw["items"]
ids = [i["id"] for i in items]
out["crosswalk"] = {
    "rowCount": len(items),
    "arRows": sorted(i for i in ids if i.startswith("AR-")),
    "fwRows": sorted(i for i in ids if i.startswith("FW-")),
    "statusesByRow": {i["id"]: i.get("status") for i in items},
}
owner_map = {}
for i in items:
    for row in i.get("ownerRows", []) or []:
        rid = row["id"] if isinstance(row, dict) else row
        owner_map.setdefault(rid, []).append(
            {"parent": i["id"], "parentStatus": i.get("status")})
out["scopedOwners"] = {k: owner_map.get(k) for k in
                       ("DR-201", "DR-202", "DR-203", "DR-204", "DR-205")}
out["allScopedOwnersRouted"] = all(out["scopedOwners"].values())

# every crosswalk row's latestCompletedReview now points at the v10 review
lcr = {i["id"]: i.get("latestCompletedReview", {}) for i in items}
out["latestCompletedReview"] = {
    "distinctShas": sorted({(v or {}).get("sha256") for v in lcr.values()}),
    "distinctVerdicts": sorted({(v or {}).get("overallVerdict") for v in lcr.values()}),
    "distinctUnresolved": sorted({
        ",".join((v or {}).get("unresolvedShouldIds", []) or []) for v in lcr.values()}),
    "historicalDepth": sorted({len(i.get("historicalReviews", []) or []) for i in items}),
}
out["latestReviewShaMatchesV10Review"] = out["latestCompletedReview"]["distinctShas"] == [
    "64e15aff50d77f0f84b53c145acc6a46d208afe0a1e090272d5deaf25ca3e8f9"]

# ---- inherited residual rows
txt = open(os.path.join(V11, DC, "inherited-residuals.proposed.md")).read()
found = sorted(set(re.findall(r"DR-0\d{2}(?:-R\d{2})?", txt)))
out["inheritedResidualRows"] = {
    "found": found, "count": len(found),
    "parents": [f for f in found if "-R" not in f],
    "r12Children": [f for f in found if f.startswith("DR-011-R")],
}

# ---- qualification gates
g = json.load(open(os.path.join(V11, DC, "qualification-gates.proposed.json")))
rows = g.get("gates") or g.get("items") or []
out["qualificationGates"] = {
    "count": len(rows),
    "demonstratedTrue": [r.get("id") for r in rows if r.get("demonstrated")],
    "allUndemonstrated": all(not r.get("demonstrated") for r in rows),
    "platformFamilies": sorted({p for r in rows
                                for p in (r.get("platforms") or r.get("platformFamilies") or [])}),
}

# ---- evaluation subresiduals
e = json.load(open(os.path.join(V11, DC, "evaluation-residual-dispositions.proposed.json")))
erows = e.get("items") or e.get("dispositions") or []
out["evaluationSubresiduals"] = {
    "count": len(erows),
    "idPrefixes": sorted({str(r.get("id", ""))[:3] for r in erows}),
    "unchangedFromV10": sha(os.path.join(V11, DC, "evaluation-residual-dispositions.proposed.json"))
                        == sha(os.path.join(V10, DC, "evaluation-residual-dispositions.proposed.json")),
}

# ---- protected historical files
h = json.load(open(os.path.join(V11, DC, "historical-preservation-report.v11.json")))
hrows = h.get("files") or h.get("protected") or []
mismatch = []
for r in hrows:
    p = r.get("path")
    if not p:
        continue
    a = sha(os.path.join(V11, p))
    if a and r.get("sha256") and a != r["sha256"]:
        mismatch.append(p)
out["historicalPreservation"] = {
    "declaredCount": len(hrows),
    "digestMismatch": mismatch,
    "allIntact": not mismatch,
    "standing": h.get("standing", "")[:200],
}
print(json.dumps(out, indent=2))
