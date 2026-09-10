"""Law 4: do BOTH stage outputDomains sets carry the same admission constraints?

Requirement 4 calls them 'both stage outputDomains sets'. This locates every
outputDomains subschema in the identity schemas and compares their constraint sets
(items ref, uniqueItems, maxItems, vocabulary annotation), then tests actual
admission of a duplicate and of an unregistered domain token at each site.
"""
import json
import sys

ROOT = sys.argv[1]
P = ROOT + "/docs/coop/design-corrections/foundation/identity-schemas.v2.json"
doc = json.load(open(P))


def find(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "outputDomains" and isinstance(v, dict):
                yield (path + "/" + k, v)
            yield from find(v, path + "/" + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from find(v, f"{path}/{i}")


sites = list(find(doc))
rows = []
for path, sch in sites:
    items = sch.get("items", {})
    rows.append({
        "path": path,
        "itemsRef": items.get("$ref"),
        "uniqueItems": sch.get("uniqueItems"),
        "maxItems": sch.get("maxItems"),
        "hasVocabularyAnnotation": "x-opensip-vocabulary" in items,
        "vocabularyAuthority": (items.get("x-opensip-vocabulary") or {}).get(
            "authority"),
        "order": sch.get("x-opensip-order"),
    })

domain_enum = doc["$defs"]["Domain"]["enum"]
out = {
    "siteCount": len(sites),
    "sites": rows,
    "allFlatDomainRef": all(r["itemsRef"] == "#/$defs/Domain" for r in rows),
    "uniqueItemsValues": sorted({str(r["uniqueItems"]) for r in rows}),
    "uniqueItemsSymmetric": len({r["uniqueItems"] for r in rows}) == 1,
    "maxItemsSymmetric": len({r["maxItems"] for r in rows}) == 1,
    "annotationSymmetric": len({r["vocabularyAuthority"] for r in rows}) == 1,
    "domainEnumSize": len(domain_enum),
    "domainEnumUnique": len(set(domain_enum)) == len(domain_enum),
}

# Does the byDomain registry agree with the Domain enum?
by = doc.get("x-opensip-digest-domains", {}).get("byDomain")
if isinstance(by, dict):
    out["byDomainKeys"] = len(by)
    out["domainMinusByDomain"] = sorted(set(domain_enum) - set(by))
    out["byDomainMinusDomain"] = sorted(set(by) - set(domain_enum))
    out["vocabularyAgrees"] = set(domain_enum) == set(by)

print(json.dumps(out, indent=2))
