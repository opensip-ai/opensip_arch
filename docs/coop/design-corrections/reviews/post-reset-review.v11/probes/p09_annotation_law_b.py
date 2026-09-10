#!/usr/bin/env python3
"""p09: corrections and extensions to p08.

p08 HARNESS ERROR, corrected here: the "nullable oneOf single-branch" probe used a
`{"type":"null"}` sibling. A null branch is not a governed form, so it is never a sighting and
ADMIT was the CORRECT verdict -- the probe tested nothing. Branch isolation is retested with BOTH
branches governed, in both branch orders.

Adds: branch-order isolation, the typed-equality consistency question between the two dedup sites,
whole-document key-order permutation invariance, all-13-relation closure, and the registered
injection inventory.
"""
import copy
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path

V11 = Path("/tmp/opensip-design-corrections/candidate-subject.v11/docs/coop/design-corrections/foundation")
V10 = Path("/tmp/opensip-design-corrections/candidate-subject.v10/docs/coop/design-corrections/foundation")


def load(tag, home):
    spec = importlib.util.spec_from_file_location(tag, home / "identity-model.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[tag] = mod
    spec.loader.exec_module(mod)
    return mod


M11, M10 = load("m11b", V11), load("m10b", V10)

ANN = {"representation": "raw-artifact", "retention": "not-joined",
       "authority": "probe", "reason": "independent reviewer probe control"}
BARE = {"$ref": "#/$defs/DigestHex"}
out = {}


def verdict(M, name, document):
    try:
        M.relation_annotation_closure(name, document)
        return "ADMIT"
    except Exception as exc:
        return str(exc).split(":")[0]


def doc(M):
    return copy.deepcopy(M.RELATION_DOCUMENT)


# ---------------------------------------------------------------- 1. branch isolation, corrected
def two_governed_branches(M, annotated_index):
    """BOTH branches governed; only one annotated. Branches are alternatives and get distinct
    paths, so the unannotated one must remain uncovered whichever position it occupies."""
    d = doc(M)
    branches = [dict(BARE), dict(BARE)]
    branches[annotated_index] = dict(BARE, **{"x-opensip-digest": ANN})
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {"oneOf": branches}
    return d


out["branchIsolation"] = [
    {"annotatedIndex": i,
     "expected": "RELATION_DIGEST_UNANNOTATED",
     "v11": verdict(M11, "file", two_governed_branches(M11, i)),
     "v10": verdict(M10, "file", two_governed_branches(M10, i))}
    for i in (0, 1)
]
out["branchIsolationCorrect"] = all(
    r["v11"] == r["expected"] for r in out["branchIsolation"])

# both branches annotated and agreeing -> positive control
d = doc(M11)
d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {
    "oneOf": [dict(BARE, **{"x-opensip-digest": ANN}), dict(BARE, **{"x-opensip-digest": ANN})]}
out["branchIsolationPositiveControl"] = verdict(M11, "file", d)


# ------------------------------------------------- 2. typed-equality consistency between sites
# record() dedups with C.equal_typed; walk()'s `inherited` list dedups with Python `not in` (==).
# 1 == True in Python but they are NOT typed-equal. If a parent and a descendant carry annotations
# that are == but not typed-equal, the descendant's is dropped from `inherited` and the conflict
# becomes invisible. This asks whether the two sites actually disagree.
A_INT = {"representation": "raw-artifact", "retention": "not-joined",
         "authority": "probe", "reason": "typed equality", "ordinal": 1}
A_BOOL = dict(A_INT, ordinal=True)
out["typedEquality"] = {
    "pythonEqual": A_INT == A_BOOL,
    "equalTyped": M11.C.equal_typed(A_INT, A_BOOL),
}

d = doc(M11)
d["$defs"]["RevAliasV1"] = dict(BARE, **{"x-opensip-digest": A_BOOL})
d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {
    "$ref": "#/$defs/RevAliasV1", "x-opensip-digest": A_INT}
out["typedEquality"]["viaRefChainVerdict"] = verdict(M11, "file", d)

# same pair, but placed so BOTH reach `inherited` (parent property + enclosing branch parent)
d = doc(M11)
d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {
    "x-opensip-digest": A_INT,
    "oneOf": [{"x-opensip-digest": A_BOOL, "oneOf": [dict(BARE)]}]}
out["typedEquality"]["viaInheritedListVerdict"] = verdict(M11, "file", d)

# control: two clearly-disagreeing annotations at the same inherited positions must conflict
d = doc(M11)
d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {
    "x-opensip-digest": A_INT,
    "oneOf": [{"x-opensip-digest": dict(A_INT, authority="other"), "oneOf": [dict(BARE)]}]}
out["typedEquality"]["disagreeingControlVerdict"] = verdict(M11, "file", d)


# ------------------------------------------------- 3. whole-document key-order permutation
def shuffled(node, rng):
    """Rebuild every dict with randomly permuted key insertion order. Canonically identical."""
    if isinstance(node, dict):
        items = list(node.items())
        rng.shuffle(items)
        return {k: shuffled(v, rng) for k, v in items}
    if isinstance(node, list):
        return [shuffled(v, rng) for v in node]
    return node


relations = list(M11.RELATION_DOCUMENT["x-opensip-relation-registry"]["relations"])
base = {r: verdict(M11, r, doc(M11)) for r in relations}
perm_stable = True
perm_detail = []
for seed in range(12):
    rng = random.Random(seed)
    permuted = shuffled(M11.RELATION_DOCUMENT, rng)
    got = {r: verdict(M11, r, permuted) for r in relations}
    same = got == base
    perm_stable &= same
    if not same:
        perm_detail.append({"seed": seed, "differs": {
            r: [base[r], got[r]] for r in relations if base[r] != got[r]}})
out["keyOrderPermutation"] = {
    "seeds": 12,
    "baseVerdicts": base,
    "allRelationsAdmitAtBase": all(v == "ADMIT" for v in base.values()),
    "stableUnderPermutation": perm_stable,
    "differences": perm_detail,
}

# the same permutation sweep against the PRE-FIX model, as discrimination evidence
base10 = {r: verdict(M10, r, copy.deepcopy(M10.RELATION_DOCUMENT)) for r in relations}
perm10_stable = True
for seed in range(12):
    permuted = shuffled(M10.RELATION_DOCUMENT, random.Random(seed))
    perm10_stable &= ({r: verdict(M10, r, permuted) for r in relations} == base10)
out["keyOrderPermutation"]["v10StableOnRegisteredDocument"] = perm10_stable


# ------------------------------------------------- 4. registered injection inventory
cov = M11.relation_digest_annotation_coverage()
by_rel = cov["byRelation"]
out["registeredInventory"] = {
    "relationCount": len(relations),
    "relationsWithSightings": len(by_rel),
    "governedTotal": cov["total"],
    "governedAnnotated": cov["annotated"],
    "governedUnannotated": cov["unannotated"],
    "sightingCount": len(cov["sightings"]),
    "annotatedSightingsAllRelations": sum(
        1 for s in cov["sightings"] if s["annotations"]),
    "perRelationAnnotated": {r: by_rel[r]["annotated"] for r in sorted(by_rel)},
    "everySightingHasMissingKey": all("missing" in s for s in cov["sightings"]),
    "anyMissingTrueOnRegistered": [s["path"] for s in cov["sightings"] if s.get("missing")],
}

# count distinct x-opensip-digest injections literally present in the registered document
def count_injections(node):
    n = 0
    if isinstance(node, dict):
        if "x-opensip-digest" in node:
            n += 1
        for v in node.values():
            n += count_injections(v)
    elif isinstance(node, list):
        for v in node:
            n += count_injections(v)
    return n


out["registeredInventory"]["literalInjectionsInDocument"] = count_injections(
    M11.RELATION_DOCUMENT)
out["registeredInventory"]["literalInjectionsInV10Document"] = count_injections(
    M10.RELATION_DOCUMENT)
out["registeredInventory"]["documentsByteIdentical"] = (
    M11.C.canonical(M11.RELATION_DOCUMENT) == M10.C.canonical(M10.RELATION_DOCUMENT))

print(json.dumps(out, indent=2, default=str))
