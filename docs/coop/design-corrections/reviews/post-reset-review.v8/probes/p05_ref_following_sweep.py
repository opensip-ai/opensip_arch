#!/usr/bin/env python3
"""P05: the digest law checked at the FIELD sites, following $ref.

`#/$defs/Hash` and `#/$defs/DigestHex` are reusable type definitions, not
fields. The closing digest law governs fields. So: resolve every property whose
type is (or $refs) a bare-64-hex type, and require the annotation AT THE FIELD.
An annotation on the shared type would be exactly the "inherit a plausible
rule" the law forbids, so its absence there is correct only if every referencing
field carries its own.

Also: does the native bundle's retention vocabulary have a declared owner?
"""
import json, re, sys
from pathlib import Path

SUBJ = Path("/tmp/opensip-design-corrections/candidate-subject.v8")
F = SUBJ / "docs/coop/design-corrections/foundation"
NAT = SUBJ / "docs/coop/design-corrections/native"

BARE = re.compile(r"^\^\[0-9a-f\]\{64\}\(\?!\[\\s\\S\]\)\$?$")
out = {}


def analyse(path, label):
    doc = json.loads(path.read_bytes())
    defs = doc.get("$defs", {})

    # which $defs are bare-64-hex scalar types?
    hexlike = set()
    for name, node in defs.items():
        if isinstance(node, dict) and isinstance(node.get("pattern"), str) \
                and BARE.match(node["pattern"]):
            hexlike.add("#/$defs/" + name)

    fields = []

    def annotation_of(node):
        """The annotation may sit on the property, on `items` for an array of
        digests, or on the non-null branch of a nullable `oneOf`. All three are
        the SAME field site: descend before concluding it is unannotated."""
        if not isinstance(node, dict):
            return None
        if "x-opensip-digest" in node:
            return node["x-opensip-digest"]
        if "items" in node:
            a = annotation_of(node["items"])
            if a is not None:
                return a
        for b in node.get("oneOf", []) + node.get("anyOf", []):
            if isinstance(b, dict) and b.get("type") == "null":
                continue
            a = annotation_of(b)
            if a is not None:
                return a
        return None

    def is_hex_site(node):
        """Does this schema node denote a bare 64-hex scalar?"""
        if not isinstance(node, dict):
            return False
        if isinstance(node.get("pattern"), str) and BARE.match(node["pattern"]):
            return True
        if node.get("$ref") in hexlike:
            return True
        # arrays of them
        if "items" in node and is_hex_site(node["items"]):
            return "items"
        # nullable one-of
        if "oneOf" in node:
            branches = [b for b in node["oneOf"] if is_hex_site(b)]
            if branches:
                return "oneOf"
        return False

    def walk(node, path_):
        if isinstance(node, dict):
            for pname, pnode in (node.get("properties") or {}).items():
                site = is_hex_site(pnode)
                if site:
                    ann = annotation_of(pnode)
                    fields.append({
                        "path": path_ + "/properties/" + pname,
                        "via": ("$ref" if pnode.get("$ref") in hexlike
                                else ("inline" if site is True else str(site))),
                        "annotated": ann is not None,
                        "representation": (ann or {}).get("representation")
                        if isinstance(ann, dict) else ann,
                        "retention": (ann or {}).get("retention", "preimage")
                        if isinstance(ann, dict) else None,
                        "annotationSite": ("property" if "x-opensip-digest" in pnode
                                           else ("items" if "items" in pnode else "oneOf")),
                    })
            for k, v in node.items():
                walk(v, path_ + "/" + str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path_ + "/" + str(i))

    walk(doc, "#")
    unann = [f["path"] for f in fields if not f["annotated"]]
    reps, rets = {}, {}
    for f in fields:
        if f["annotated"]:
            reps[f["representation"]] = reps.get(f["representation"], 0) + 1
            rets[f["retention"]] = rets.get(f["retention"], 0) + 1
    # is the shared type itself annotated? (it must NOT be, per the law's logic)
    shared_annotated = {n: ("x-opensip-digest" in defs[n.split("/")[-1]])
                        for n in sorted(hexlike)}
    return {
        "hexScalarTypeDefs": sorted(hexlike),
        "sharedTypeCarriesAnnotation": shared_annotated,
        "digestBearingFieldSites": len(fields),
        "annotatedFieldSites": len(fields) - len(unann),
        "unannotatedFieldSites": unann,
        "representationHistogram": reps,
        "retentionHistogram": rets,
        "EVERY_FIELD_SITE_ANNOTATED": not unann,
        "fields": fields,
    }


def main():
    out["identity"] = analyse(F / "identity-schemas.v2.json", "identity")
    out["native"] = analyse(NAT / "native-evidence.schemas.v2.json", "native")
    out["relation"] = analyse(F / "relation-payload-schemas.v2.json", "relation")

    # Does the native contract declare its own closed retention vocabulary?
    md = (SUBJ / "docs/v2/contracts/product-v1/native-evidence.md").read_text()
    vocab_terms = ["preimage-frame", "closure-tree-member", "owner-retained",
                   "raw-artifact", "canonical-record", "h-identity", "preimage"]
    out["nativeRetentionVocabularyDeclared"] = {
        t: (t in md) for t in vocab_terms}
    natdoc = json.loads((NAT / "native-evidence.schemas.v2.json").read_bytes())
    out["nativeBundleDeclaresItsOwnDigestVocabulary"] = {
        k: (json.dumps(v)[:600] if not isinstance(v, str) else v[:600])
        for k, v in natdoc.items() if k.startswith("x-opensip")}
    json.dump(out, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
