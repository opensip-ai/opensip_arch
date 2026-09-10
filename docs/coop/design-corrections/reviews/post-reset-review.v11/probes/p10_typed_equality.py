#!/usr/bin/env python3
"""p10: characterise the typed-equality inconsistency found in p09.

record() dedups annotations with C.equal_typed. walk() filters the $ref-chain contribution with
Python `not in` (i.e. ==), and builds `inherited` with `not in` too. 1 == True in Python but they
are not typed-equal, so a typed-DISTINCT annotation can be dropped before record() ever sees it.

Questions asked here:
  1. Is the resulting admission ORDER-DEPENDENT -- i.e. does swapping which of the two annotations
     sits on the property vs the alias change the verdict? That would put it in the same class as
     the primary defect under repair.
  2. Is it reachable, or do the registered documents / the law constrain annotation values to
     strings so that no typed-distinct-but-==-equal pair can be written?
  3. Does canonicalisation preserve the int/bool distinction (i.e. would the two documents be
     genuinely different registered bytes)?
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

V11 = Path("/tmp/opensip-design-corrections/candidate-subject.v11/docs/coop/design-corrections/foundation")
spec = importlib.util.spec_from_file_location("m", V11 / "identity-model.py")
M = importlib.util.module_from_spec(spec)
sys.modules["m"] = M
spec.loader.exec_module(M)
C = M.C

BARE = {"$ref": "#/$defs/DigestHex"}
A_INT = {"representation": "raw-artifact", "retention": "not-joined",
         "authority": "probe", "reason": "typed equality", "ordinal": 1}
A_BOOL = dict(A_INT, ordinal=True)
A_DIFF = dict(A_INT, authority="other-authority")

out = {}


def verdict(document, name="file"):
    try:
        M.relation_annotation_closure(name, document)
        return "ADMIT"
    except Exception as exc:
        return str(exc).split(":")[0]


def ref_chain(on_property, on_alias):
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    d["$defs"]["RevAliasV1"] = dict(BARE, **{"x-opensip-digest": on_alias})
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {
        "$ref": "#/$defs/RevAliasV1", "x-opensip-digest": on_property}
    return d


# 1. order dependence of the typed-distinct pair
out["orderDependence"] = {
    "intOnProperty_boolOnAlias": verdict(ref_chain(A_INT, A_BOOL)),
    "boolOnProperty_intOnAlias": verdict(ref_chain(A_BOOL, A_INT)),
    "controlDisagreeingPair": verdict(ref_chain(A_INT, A_DIFF)),
    "controlIdenticalPair": verdict(ref_chain(A_INT, dict(A_INT))),
}
out["orderDependence"]["verdictsDifferByOrder"] = (
    out["orderDependence"]["intOnProperty_boolOnAlias"]
    != out["orderDependence"]["boolOnProperty_intOnAlias"])

# which annotation actually survived into the sighting?
for label, d in (("intOnProperty", ref_chain(A_INT, A_BOOL)),
                 ("boolOnProperty", ref_chain(A_BOOL, A_INT))):
    cov = M.relation_digest_annotation_coverage(d)
    s = [x for x in cov["sightings"] if x["path"] == "file.rev"]
    out.setdefault("survivingAnnotations", {})[label] = {
        "count": len(s[0]["annotations"]) if s else None,
        "annotations": [{k: (str(v) + "/" + type(v).__name__) for k, v in a.items()
                         if k == "ordinal"} for a in s[0]["annotations"]] if s else None,
    }

# 2. canonicalisation: are the two documents genuinely distinct bytes?
out["canonicalDistinct"] = (
    C.canonical(ref_chain(A_INT, A_BOOL)) != C.canonical(ref_chain(A_BOOL, A_INT)))
out["annotationCanonicalDistinct"] = C.canonical(A_INT) != C.canonical(A_BOOL)
out["pythonEqual"] = A_INT == A_BOOL
out["equalTyped"] = C.equal_typed(A_INT, A_BOOL)

# 3. reachability: is the annotation shape constrained anywhere?
#    Search the registered document and the law for any schema of x-opensip-digest itself.
doc = M.RELATION_DOCUMENT
found = []


def hunt(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            if "digest" in k.lower() and k not in ("x-opensip-digest",):
                pass
            if k == "x-opensip-digest" and isinstance(v, dict):
                found.append({"at": path, "keys": sorted(v),
                              "valueTypes": {kk: type(vv).__name__ for kk, vv in v.items()}})
            hunt(v, path + "/" + str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            hunt(v, path + "/" + str(i))


hunt(doc)
out["registeredAnnotationShapes"] = found
out["registeredAnnotationKeySets"] = sorted({",".join(f["keys"]) for f in found})
out["registeredAnnotationValueTypes"] = sorted(
    {t for f in found for t in f["valueTypes"].values()})
out["lawConstrainsAnnotationShape"] = [
    k for k in doc["x-opensip-digest-law"]
    if "propert" in k.lower() or "schema" in k.lower() or "requir" in k.lower()]

print(json.dumps(out, indent=2, default=str))
