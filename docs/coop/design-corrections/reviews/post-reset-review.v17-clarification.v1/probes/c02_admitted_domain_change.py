#!/usr/bin/env python
"""Point 2: the ACTUAL admitted-domain change at EvidenceRequirement.deficiency,
and an honest restatement of what my p02/p08 metrics do and do not prove.

My original report said 'zero structural pointers changed' and 'no admission was
widened'. Both need correction:
  - p02's figure is the INTERSECTION-LEAF metric only. Additions are structural
    changes, and there are many.
  - The deficiency field's admitted value domain DELIBERATELY changed. Four
    native outcomes that the v16 field REFUSED now admit. That is the point of
    the correction, and calling it 'no widening' misdescribes it.

This probe measures the exact admitted-set delta at the field, by validating
every candidate token against the v16 and v17 field schemas.
"""
import json
import os
import sys
import subprocess

REV = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews"
SUBJ = "/tmp/opensip-design-corrections/candidate-subject.v17"
V16X = "/tmp/opensip-design-corrections/post-reset-review.v17-clarification.v1/v16x"
OUT = sys.argv[1]
DCrel = "docs/coop/design-corrections"

for f in ("workflows/schemas/repair.schema.json",
          "workflows/schemas/common.schema.json",
          "workflows/schemas/imported-evidence.schema.json",
          "workflows/schemas/invocation-record.schema.json",
          "workflows/schemas/policy-document.schema.json",
          "native/native-evidence.schemas.v2.json",
          "foundation/identity-schemas.v2.json"):
    subprocess.run(["tar", "xzf", os.path.join(REV, "candidate-source.v16.tar.gz"),
                    os.path.join(DCrel, f)], cwd=V16X, capture_output=True)

sys.path.insert(0, os.path.join(SUBJ, DCrel, "foundation"))
from jsonschema import Draft202012Validator          # noqa: E402
from referencing import Registry, Resource            # noqa: E402
from referencing.jsonschema import DRAFT202012        # noqa: E402
import glob                                           # noqa: E402


def build(root):
    schemas = {}
    for p in sorted(glob.glob(os.path.join(root, DCrel, "workflows/schemas/*.schema.json"))):
        s = json.load(open(p))
        schemas[s["$id"]] = s
    fp = os.path.join(root, DCrel, "foundation/identity-schemas.v2.json")
    extra = []
    if os.path.isfile(fp):
        f = json.load(open(fp))
        extra = [(f["$id"], Resource(contents=f, specification=DRAFT202012))]
    reg = Registry().with_resources(
        [(k, Resource(contents=v, specification=DRAFT202012))
         for k, v in schemas.items()] + extra)
    return schemas, reg


s16, r16 = build(V16X)
s17, r17 = build(SUBJ)
U = "urn:opensip:product-v1:workflows:"

f16 = s16[U + "repair"]["$defs"]["EvidenceRequirement"]["properties"]["deficiency"]
f17 = s17[U + "repair"]["$defs"]["EvidenceRequirement"]["properties"]["deficiency"]
v16 = Draft202012Validator({k: v for k, v in f16.items()
                            if k not in ("description",)}, registry=r16)
v17 = Draft202012Validator({k: v for k, v in f17.items()
                            if k not in ("description", "x-opensip-vocabulary")},
                           registry=r17)

d9 = s16[U + "common"]["$defs"]["D9Deficiency"]["enum"]
nat = s17[U + "common"]["$defs"]["NativeSufficiencyDeficiency"]["enum"]
imp = s17[U + "common"]["$defs"]["ImportedRequirementDeficiency"]["enum"]
universe = sorted(set(d9) | set(nat) | set(imp))

rows = []
for tok in universe:
    a = v16.is_valid(tok)
    b = v17.is_valid(tok)
    rows.append({"token": tok, "admittedByV16Field": a, "admittedByV17Field": b,
                 "newlyAdmitted": (not a) and b,
                 "noLongerAdmitted": a and (not b),
                 "inD9": tok in d9, "inNative": tok in nat, "inImported": tok in imp})

rep = {
    "probe": "c02-admitted-domain-change",
    "v16FieldSchema": f16,
    "v17FieldSchemaShape": {"oneOf": [x["$ref"] for x in f17["oneOf"]]},
    "d9Members": d9, "nativeMembers": nat, "importedMembers": imp,
    "tokenUniverseSize": len(universe),
    "rows": rows,
    "newlyAdmitted": sorted(r["token"] for r in rows if r["newlyAdmitted"]),
    "noLongerAdmitted": sorted(r["token"] for r in rows if r["noLongerAdmitted"]),
    "admittedByV16Count": sum(1 for r in rows if r["admittedByV16Field"]),
    "admittedByV17Count": sum(1 for r in rows if r["admittedByV17Field"]),
}
rep["admittedSetChanged"] = bool(rep["newlyAdmitted"] or rep["noLongerAdmitted"])
rep["theFourBlindNamedOutcomes"] = [
    t for t in ("derivation-policy-unmet", "external-consumers-unknown",
                "input-closure-incomplete", "resolution-incomplete")]
rep["allFourWereRefusedByV16Field"] = all(
    not next(r for r in rows if r["token"] == t)["admittedByV16Field"]
    for t in rep["theFourBlindNamedOutcomes"])
rep["allFourAreAdmittedByV17Field"] = all(
    next(r for r in rows if r["token"] == t)["admittedByV17Field"]
    for t in rep["theFourBlindNamedOutcomes"])

# ---- honest restatement of the p02 metric ----
p02 = json.load(open("/tmp/opensip-design-corrections/post-reset-review.v17/"
                     "logs/p02-schema-structural-diff.json"))
tot_changed = sum(d.get("structuralPointersChanged", 0) for d in p02["documents"])
tot_only16 = sum(d.get("structuralPointersOnlyInV16", 0) for d in p02["documents"])
tot_only17 = sum(d.get("structuralPointersOnlyInV17", 0) for d in p02["documents"])
rep["p02MetricRestated"] = {
    "whatItMeasured": "leaf-level values at JSON pointers present in BOTH "
                      "versions, after stripping a chosen prose key set; empty "
                      "containers vanish under flattening",
    "intersectionLeafValuesChanged": tot_changed,
    "pointersOnlyInV16": tot_only16,
    "pointersOnlyInV17": tot_only17,
    "additionsAreStructuralChanges": True,
    "correctStatement": ("No leaf value at any pointer common to both versions "
                         "changed (%d), and one pointer was removed (%d); %d new "
                         "structural pointers were ADDED. Additions include a new "
                         "presence conditional, two new enum definitions, new "
                         "relation-registry laws and new annotation blocks - all "
                         "structural schema changes."
                         % (tot_changed, tot_only16, tot_only17)),
    "isNotAProofOfZeroStructuralChange": True,
}
p08 = json.load(open("/tmp/opensip-design-corrections/post-reset-review.v17/"
                     "logs/p08-executable-delta.json"))
rep["p08MetricRestated"] = {
    "whatItMeasured": "a token/line heuristic: comments and docstrings removed "
                      "by tokenizing, then a line-level SequenceMatcher diff",
    "isNotAnASTOrSemanticProof": True,
    "noRemovedRaiseLineIsNotAProofOfPreservedRefusalSet": True,
    "removedExecutableLinesByFile": {
        f["path"]: f.get("removedExecutableLines") for f in p08["files"]},
}

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

print("v16 field schema      :", json.dumps(
    {k: v for k, v in f16.items() if k != "description"}))
print("v17 field schema shape:", json.dumps(rep["v17FieldSchemaShape"]))
print()
print("token universe        :", rep["tokenUniverseSize"])
print("admitted by v16 field :", rep["admittedByV16Count"])
print("admitted by v17 field :", rep["admittedByV17Count"])
print()
print("NEWLY ADMITTED (%d):" % len(rep["newlyAdmitted"]))
for t in rep["newlyAdmitted"]:
    print("   +", t)
print("NO LONGER ADMITTED (%d):" % len(rep["noLongerAdmitted"]))
for t in rep["noLongerAdmitted"]:
    print("   -", t)
print()
print("the four blind-named outcomes were refused by the v16 field:",
      rep["allFourWereRefusedByV16Field"])
print("...and are admitted by the v17 field                       :",
      rep["allFourAreAdmittedByV17Field"])
print()
print("p02 restated:", rep["p02MetricRestated"]["correctStatement"])
