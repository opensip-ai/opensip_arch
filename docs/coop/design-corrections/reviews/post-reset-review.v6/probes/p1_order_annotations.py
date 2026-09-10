#!/usr/bin/env python
"""P1 - independent audit of x-opensip-order coverage and agreement.

Claim under test (identity-and-evidence.md L107): "Every array in
identity-schemas.v2 carries this annotation". Also audits the other closed
schema bundles for arrays lacking an order annotation, and checks that the
declared annotation vocabulary is exactly the one the contract names.
"""
import json, os, sys

SUBJ = "/tmp/opensip-design-corrections/candidate-subject.v6/docs"
DC = os.path.join(SUBJ, "coop/design-corrections")

VOCAB = {"sequence", "canonical-set", "path", "numeric", "ordinal",
         "predicate", "ruleId", "waiverId"}

BUNDLES = {
    "identity-schemas.v2": "foundation/identity-schemas.v2.json",
    "native-evidence.schemas.v2": "native/native-evidence.schemas.v2.json",
    "security-lifecycle.schemas.v1": "security/security-lifecycle.schemas.v1.json",
    "product-configuration.schema.v2": "foundation/product-configuration.schema.v2.json",
}
WF = os.path.join(DC, "workflows/schemas")
for fn in sorted(os.listdir(WF)):
    if fn.endswith(".json"):
        BUNDLES["workflows/" + fn[:-5]] = "workflows/schemas/" + fn


def walk(node, path, out, in_props=False):
    """Find every schema object declaring type array (or items)."""
    if isinstance(node, dict):
        is_arr = node.get("type") == "array" or (
            "items" in node and "properties" not in node)
        if is_arr:
            out.append((path, node))
        for k, v in node.items():
            walk(v, path + "/" + str(k), out, in_props)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path + "/" + str(i), out, in_props)


results = {}
for name, rel in BUNDLES.items():
    p = os.path.join(DC, rel)
    if not os.path.exists(p):
        results[name] = {"error": "missing"}
        continue
    doc = json.load(open(p))
    arrs = []
    walk(doc, "$", arrs)
    ann, unann, badvocab = [], [], []
    for path, node in arrs:
        a = node.get("x-opensip-order")
        if a is None:
            unann.append(path)
        else:
            ann.append((path, a))
            if a not in VOCAB:
                badvocab.append((path, a))
    results[name] = {
        "arrayCount": len(arrs),
        "annotated": len(ann),
        "unannotated": len(unann),
        "unannotatedPaths": unann[:25],
        "outOfVocabulary": badvocab,
        "annotationHistogram": {v: sum(1 for _, x in ann if x == v)
                                for v in sorted({x for _, x in ann})},
    }

print(json.dumps(results, indent=1, sort_keys=True))
