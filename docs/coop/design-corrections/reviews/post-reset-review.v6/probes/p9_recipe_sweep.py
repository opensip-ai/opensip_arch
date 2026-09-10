#!/usr/bin/env python
"""P9 - generalize the M-1 defect class.

M-1 was: a REQUIRED digest-bearing field with no producing recipe anywhere. This
sweeps every *Digest / *Id / *Root / *Commitment field in the identity, native
and workflow schema bundles and asks whether the five product contracts state a
producing rule for it. Anything unmentioned is a candidate M-1 twin that would
force implementer invention.
"""
import json, re, os
from pathlib import Path

S = Path("/tmp/opensip-design-corrections/candidate-subject.v6/docs")
DC = S / "coop/design-corrections"
CONTRACTS = S / "v2/contracts/product-v1"

prose = ""
for f in sorted(CONTRACTS.glob("*.md")):
    prose += f.read_text()
# the normative by-reference dependency is part of the design closure
prose += (S / "coop/artifacts/resolved-inputs.v2.json").read_text()
prose += (S / "coop/artifacts/delivery.v4.json").read_text()

BUNDLES = {
    "identity": DC / "foundation/identity-schemas.v2.json",
    "native": DC / "native/native-evidence.schemas.v2.json",
}
for p in sorted((DC / "workflows/schemas").glob("*.json")):
    BUNDLES["wf/" + p.stem] = p

PAT = re.compile(r"(Digest|MerkleRoot|Commitment|Id|Ids|Sha256|Hex)$")
INTERESTING = re.compile(r"(digest|merkleroot|commitment)", re.I)

found = {}


def walk(node, bundle, path, required):
    if isinstance(node, dict):
        req = set(node.get("required", []))
        for k, v in node.get("properties", {}).items():
            if INTERESTING.search(k):
                found.setdefault(k, {"bundles": set(), "required": False,
                                     "paths": []})
                found[k]["bundles"].add(bundle)
                found[k]["required"] |= (k in req)
                if len(found[k]["paths"]) < 3:
                    found[k]["paths"].append(path + "/" + k)
        for k, v in node.items():
            walk(v, bundle, path + "/" + str(k), required)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, bundle, path + "/" + str(i), required)


for name, p in BUNDLES.items():
    walk(json.loads(p.read_text()), name, "$", set())

rows = []
for field, info in sorted(found.items()):
    mentioned = field in prose
    # a recipe-ish mention: the field name appears near a producing verb
    recipe = False
    if mentioned:
        for m in re.finditer(re.escape(field), prose):
            ctx = prose[max(0, m.start() - 400):m.start() + 400].lower()
            if any(w in ctx for w in ("h(", "sha-256", "sha256", "raw sha",
                                      "digest of", "is the", "computed",
                                      "equals", "recipe", "canonical")):
                recipe = True
                break
    rows.append({"field": field, "required": info["required"],
                 "bundles": sorted(info["bundles"]),
                 "namedInContracts": mentioned,
                 "hasProducingContext": recipe,
                 "examplePath": info["paths"][0]})

out = {"probe": "P9-digest-field-recipe-sweep",
       "fieldCount": len(rows),
       "unmentioned": [r for r in rows if not r["namedInContracts"]],
       "mentionedWithoutProducingContext":
           [r for r in rows if r["namedInContracts"] and not r["hasProducingContext"]],
       "requiredAndUnmentioned":
           [r for r in rows if r["required"] and not r["namedInContracts"]],
       "all": rows}
print(json.dumps(out, indent=1))
