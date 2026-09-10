#!/usr/bin/env python3
"""P1: structural mirror differential between foundation descriptors and their
declared workflow "exact mirror" counterparts.

Resolves every $ref (local pointer and urn: document ref) to a fully inlined
logical shape, then reports differences in: required set, property set,
type/const/enum, cardinality (minItems/maxItems/uniqueItems), string bounds and
pattern, and the normative x-opensip-order annotation.

This is a MEASUREMENT probe: it makes no claim about which side is correct.
"""
import json
import os
import sys

WORK = os.environ.get(
    "OPENSIP_WORK",
    "/tmp/opensip-design-corrections/bv3-corrections-author.v1/work",
)
FOUND = os.path.join(WORK, "docs/coop/design-corrections/foundation")
WFS = os.path.join(WORK, "docs/coop/design-corrections/workflows/schemas")

DOCS = {}


def load_docs():
    for name in sorted(os.listdir(WFS)):
        if name.endswith(".json"):
            doc = json.load(open(os.path.join(WFS, name)))
            DOCS[doc["$id"]] = doc
    for name in ("identity-schemas.v2.json", "relation-payload-schemas.v2.json"):
        doc = json.load(open(os.path.join(FOUND, name)))
        DOCS[doc["$id"]] = doc


def pointer(doc, frag):
    node = doc
    for part in frag.lstrip("#").split("/"):
        if not part:
            continue
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[part]
    return node


def resolve(node, doc_id, seen=()):
    """Inline every $ref. Cycles are marked, not expanded."""
    if isinstance(node, list):
        return [resolve(x, doc_id, seen) for x in node]
    if not isinstance(node, dict):
        return node
    if "$ref" in node:
        ref = node["$ref"]
        if ref.startswith("#"):
            target_doc, frag = doc_id, ref
        else:
            target_doc, _, frag = ref.partition("#")
            frag = frag or "#"
        key = (target_doc, frag)
        if key in seen:
            return {"$cycle": f"{target_doc}{frag}"}
        target = pointer(DOCS[target_doc], frag)
        inlined = resolve(target, target_doc, seen + (key,))
        rest = {k: v for k, v in node.items() if k != "$ref"}
        if rest:
            merged = dict(inlined)
            merged.update(resolve(rest, doc_id, seen))
            return merged
        return inlined
    return {k: resolve(v, doc_id, seen) for k, v in node.items()}


# Keywords whose divergence changes what instances are admitted or how they are
# canonically ordered. "description"/"x-opensip-digest" are descriptive only.
SEMANTIC = (
    "type", "const", "enum", "required", "additionalProperties",
    "minItems", "maxItems", "uniqueItems", "x-opensip-order",
    "minLength", "maxLength", "pattern", "minimum", "maximum",
    "not", "oneOf", "anyOf", "allOf", "$cycle",
)


def flatten(node, path="", out=None):
    if out is None:
        out = {}
    if isinstance(node, dict):
        for kw in SEMANTIC:
            if kw in node:
                out[f"{path}.{kw}"] = node[kw]
        for key, child in node.get("properties", {}).items():
            flatten(child, f"{path}/{key}", out)
        if "items" in node:
            flatten(node["items"], f"{path}[]", out)
    return out


def diff(a, b):
    rows = []
    for key in sorted(set(a) | set(b)):
        av, bv = a.get(key, "<absent>"), b.get(key, "<absent>")
        if isinstance(av, list) and isinstance(bv, list) and key.endswith(".required"):
            if sorted(av) == sorted(bv):
                continue
        if av != bv:
            rows.append({"field": key, "foundation": av, "workflow": bv})
    return rows


PAIRS = [
    ("import", "opensip.product.identity.2", "#/$defs/import",
     "urn:opensip:product-v1:workflows:imported-evidence", "#/$defs/ImportWrapperV2"),
    ("scope-descriptor", "opensip.product.identity.2", "#/$defs/scope-descriptor",
     "urn:opensip:product-v1:workflows:imported-evidence", "#/$defs/ImportScopeDescriptor"),
]


def main():
    load_docs()
    report = {}
    for name, fdoc, ffrag, wdoc, wfrag in PAIRS:
        f = flatten(resolve(pointer(DOCS[fdoc], ffrag), fdoc))
        w = flatten(resolve(pointer(DOCS[wdoc], wfrag), wdoc))
        rows = diff(f, w)
        report[name] = {"differences": len(rows), "rows": rows}
    print(json.dumps(report, indent=2))
    return 1 if any(v["differences"] for v in report.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
