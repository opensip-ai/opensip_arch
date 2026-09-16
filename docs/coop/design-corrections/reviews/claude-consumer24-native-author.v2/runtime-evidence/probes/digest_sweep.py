"""Probe: bare 64-hex digest positions of the foundation record documents and whether each carries an
x-opensip-digest annotation on its path (leaf, branch or enclosing property). Read-only; stdout only.
Usage: digest_sweep.py ROOT
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "docs/coop/design-corrections/foundation"
DOCS = ["enumeration-plan.schema.v1.json", "subject-inventory.schema.v1.json", "evaluator-emission-plan.schema.v1.json",
        "target-attribution.schema.v1.json", "target-attribution.schema.v2.json", "incoming-search.schema.v1.json",
        "execution-inputs.schema.v1.json", "import-source-context.schema.json"]
HEX = "^[0-9a-f]{64}(?![\\s\\S])"


def sweep(doc):
    defs = doc.get("$defs", {})
    hex_defs = {n for n, d in defs.items() if isinstance(d, dict) and d.get("pattern") == HEX}
    seen = {}

    def walk(node, path, annotated, chain=()):
        if isinstance(node, list):
            for i, x in enumerate(node):
                walk(x, path + "[%d]" % i, annotated, chain)
            return
        if not isinstance(node, dict):
            return
        annotated = annotated or "x-opensip-digest" in node
        ref = node.get("$ref")
        if node.get("pattern") == HEX or (isinstance(ref, str) and ref.split("/")[-1] in hex_defs and ref.startswith("#/$defs/")):
            seen[path] = seen.get(path, True) and annotated
            return
        if isinstance(ref, str) and ref.startswith("#/$defs/") and ref.split("/")[-1] in defs and ref not in chain:
            walk(defs[ref.split("/")[-1]], path, annotated, chain + (ref,))
        for k, v in node.items():
            if k == "properties" and isinstance(v, dict):
                for name, sub in v.items():
                    walk(sub, path + "/" + name, annotated)
            elif k in ("items", "additionalProperties"):
                walk(v, path + "[]", annotated)
            elif k in ("oneOf", "anyOf", "allOf") and isinstance(v, list):
                for i, sub in enumerate(v):
                    walk(sub, path + "|" + k + str(i), annotated)

    walk({k: v for k, v in doc.items() if k != "$defs"}, "#", False)
    for name, d in defs.items():
        if name not in hex_defs:
            walk(d, "#/$defs/" + name, False)
    return {"total": len(seen), "unannotated": sorted(p for p, ok in seen.items() if not ok)}


out = {}
for name in DOCS:
    p = root / name
    if p.is_file():
        out[name] = sweep(json.loads(p.read_text()))
print(json.dumps(out, indent=1))
