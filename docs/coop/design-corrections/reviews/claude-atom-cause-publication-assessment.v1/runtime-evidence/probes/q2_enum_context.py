"""Are those enum memberships accompanied by ANY per-member condition/description?

If every occurrence is a bare list item with no adjacent discriminating prose, the emission
condition is unpublished. READ-ONLY.
"""
import json
from pathlib import Path

S = Path("/tmp/opensip-design-corrections/candidate-subject.v33")
SPOTS = [
    ("foundation/identity-schemas.v3.json", 3320),
    ("foundation/identity-schemas.v3.json", 3487),
    ("foundation/identity-schemas.v3.json", 4888),
    ("foundation/evaluator-projection-registry.v1.json", 1184),
    ("workflows/schemas/policy-document.v2.schema.json", 894),
]
out = {"standing": "READ-ONLY context around each enum membership of the disputed causes."}
rows = []
for rel, line in SPOTS:
    p = S / "docs/coop/design-corrections" / rel
    L = p.read_text().splitlines()
    lo, hi = max(0, line - 22), min(len(L), line + 10)
    rows.append({"file": rel, "line": line,
                 "context": [f"{i+1}| {L[i]}" for i in range(lo, hi)]})
out["spots"] = rows

# Do the owning registries carry ANY per-cause description object?
ident = json.loads((S / "docs/coop/design-corrections/foundation/identity-schemas.v3.json").read_text())
reg = ident.get("x-opensip-evaluator-deficiency-registry")
out["evaluatorDeficiencyRegistry"] = {
    "topKeys": sorted(reg) if isinstance(reg, dict) else None,
    "sourcesIsFlatStringLists": (
        isinstance(reg.get("sources"), dict)
        and all(isinstance(v, list) and all(isinstance(x, str) for x in v)
                for v in reg["sources"].values())) if isinstance(reg, dict) else None,
    "causeLaw": reg.get("causeLaw") if isinstance(reg, dict) else None,
    "nativeCauseOwner": reg.get("nativeCauseOwner") if isinstance(reg, dict) else None,
    "anyPerCauseConditionObject": (
        any(isinstance(v, dict) for v in reg.get("sources", {}).values())
        if isinstance(reg, dict) else None),
}

proj = json.loads(
    (S / "docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json").read_text())


def find_enum_holder(node, target, path=""):
    found = []
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, list) and target in v:
                found.append({"path": path + "/" + k,
                              "siblingKeys": sorted(x for x in node if x != k),
                              "descriptionIfAny": node.get("description")})
            found.extend(find_enum_holder(v, target, path + "/" + k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            found.extend(find_enum_holder(v, target, path + "/" + str(i)))
    return found


for tok in ("missing-relation-coverage", "selector-unbound", "coverage-unknown",
            "uncovered-expected-source-subject"):
    out.setdefault("enumHolders", {})[tok] = {
        "projectionRegistry": find_enum_holder(proj, tok),
        "identitySchemas": find_enum_holder(ident, tok),
    }

# Is AtomCauseCodeV1 defined with per-member prose anywhere in the registries?
def deep_find_key(node, key, path=""):
    hits = []
    if isinstance(node, dict):
        for k, v in node.items():
            if k == key:
                hits.append({"path": path + "/" + k, "value": v})
            hits.extend(deep_find_key(v, key, path + "/" + k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            hits.extend(deep_find_key(v, key, path + "/" + str(i)))
    return hits


out["atomCauseCodeV1Definitions"] = {
    "projectionRegistry": deep_find_key(proj, "AtomCauseCodeV1"),
    "identitySchemas": deep_find_key(ident, "AtomCauseCodeV1"),
}
print(json.dumps(out, indent=2, default=str))
