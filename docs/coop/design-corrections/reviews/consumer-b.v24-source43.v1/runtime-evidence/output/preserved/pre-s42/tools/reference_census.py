"""Mechanical census of the normative reference vocabulary the retained-closure walker must execute (source39.v2 self-audit).

Walks every kit JSON schema document (no helper model, no store) and records:
  - every typed-prefix identity position: a string schema whose pattern is ^<prefix>:[0-9a-f]{64}(?![\\s\\S]);
  - every x-opensip-digest annotation: (representation, retention) with its schema position and record/domain/domainSet target;
  - every x-opensip-digest-domains registry join form (closureJoins, nestedIdentities, nestedRecords, blobJoins, snapshotJoins,
    contextAgreementFields, languageVersionBinding retention) and closureMembership class.
Writes output/vectors/reference-census.json. It is the vocabulary from which negatives are chosen; it asserts nothing about stores.
Usage: python3 output/tools/reference_census.py
"""
import collections
import json
import os
import re

KIT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/subject/docs/"
OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output/preserved/pre-s42/"
TYPED = re.compile(r"^\^([a-z][a-z0-9-]*[0-9]):\[0-9a-f\]\{64\}\(\?!\[\\s\\S\]\)$")


def walk(node, pointer, rel, typed, digests):
    if isinstance(node, dict):
        pat = node.get("pattern")
        if isinstance(pat, str):
            m = TYPED.match(pat)
            if m:
                typed.append({"document": rel, "position": pointer, "prefix": m.group(1)})
        ann = node.get("x-opensip-digest")
        if isinstance(ann, dict):
            target = ann.get("domain") or ann.get("domainSet") or ann.get("record") or ann.get("artifactClass") or ann.get("derivedFrom")
            digests.append({"document": rel, "position": pointer, "representation": ann.get("representation"),
                            "retention": ann.get("retention", "preimage"), "target": target,
                            "locatedBy": ann.get("locatedBy")})
        for k, v in node.items():
            walk(v, f"{pointer}/{k.replace('~', '~0').replace('/', '~1')}", rel, typed, digests)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{pointer}/{i}", rel, typed, digests)


def main():
    typed, digests = [], []
    for d, _, fs in sorted(os.walk(KIT)):
        for f in sorted(fs):
            if f.endswith(".json"):
                p = os.path.join(d, f)
                rel = os.path.relpath(p, KIT)
                try:
                    doc = json.load(open(p))
                except ValueError:
                    continue
                walk(doc, "#", rel, typed, digests)
    idoc = json.load(open(KIT + "coop/design-corrections/foundation/identity-schemas.v3.json"))
    dd = idoc["x-opensip-digest-domains"]
    joins = collections.Counter()
    for set_name, rows in dd["domainSets"].items():
        for dom, row in rows.items():
            for key in ("closureJoins", "nestedIdentities", "nestedRecords", "blobJoins", "snapshotJoins"):
                for j in row.get(key, []):
                    joins[(set_name, key, j.get("form", "-"))] += 1
                    for bj in j.get("blobJoins", []) if key == "nestedRecords" else []:
                        joins[(set_name, "nestedRecords.blobJoins", "-")] += 1
            if row.get("contextAgreementFields"):
                joins[(set_name, "contextAgreementFields", "-")] += 1
            if row.get("languageVersionBinding"):
                joins[(set_name, "languageVersionBinding", row["languageVersionBinding"].get("retention", "-"))] += 1
    pair_counts = collections.Counter((x["representation"], x["retention"]) for x in digests)
    out = {
        "standing": "vocabulary census of kit bytes only; every class listed here must be walked by the retained-closure walker or explicitly declared out of the Run-closure walk",
        "typedPrefixPositions": typed,
        "typedPrefixes": sorted({x["prefix"] for x in typed}),
        "digestAnnotations": digests,
        "representationRetentionPairs": [{"representation": r, "retention": t, "count": n} for (r, t), n in sorted(pair_counts.items(), key=str)],
        "byDomainRows": {k: {"representation": v.get("representation"), "retention": v.get("retention", "preimage")} for k, v in dd["byDomain"].items()},
        "registryJoinForms": [{"domainSet": s, "join": k, "form": f, "count": n} for (s, k, f), n in sorted(joins.items())],
        "closureMembershipClasses": {k: sorted(v) for k, v in dd["closureMembership"].items() if isinstance(v, dict)},
        "closureKindsByField": dd["closureKinds"]["byField"],
        "classification": "explanatory",
    }
    os.makedirs(OUT + "vectors", exist_ok=True)
    json.dump(out, open(OUT + "vectors/reference-census.json", "w"), indent=1)
    print(json.dumps({"typedPositions": len(typed), "prefixes": out["typedPrefixes"], "digestAnnotations": len(digests),
                      "pairs": out["representationRetentionPairs"]}, indent=None))


if __name__ == "__main__":
    main()
