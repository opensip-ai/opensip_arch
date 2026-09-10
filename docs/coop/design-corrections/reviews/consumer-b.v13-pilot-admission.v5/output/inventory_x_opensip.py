#!/usr/bin/env python3
"""Mechanical inventory of every x-opensip-* annotation on schemas selected by the TS pilot.

Does not filter by implemented handlers. Writes full annotation values.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v5/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")
sys.path.insert(0, str(OUT))

from helpers import kit_schemas, store  # noqa: E402


def pointer(parts: list) -> str:
    out = ""
    for p in parts:
        s = str(p).replace("~", "~0").replace("/", "~1")
        out += "/" + s
    return out or "/"


def walk_ann(obj, parts, hits):
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = parts + [k]
            if str(k).startswith("x-opensip-"):
                hits.append({"pointer": pointer(p), "keyword": k, "value": v})
            walk_ann(v, p, hits)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_ann(v, parts + [i], hits)


def flatten_table(keyword: str, value, parent_ptr: str) -> list[dict]:
    """Recursively nested law tables: emit a row per nested object that is itself a law entry."""
    rows = []
    if not isinstance(value, dict):
        return rows
    # common table containers
    for table_key in (
        "domainSets",
        "byDomain",
        "relations",
        "deficiencies",
        "keys",
        "rows",
        "ladders",
        "classes",
        "languages",
        "members",
        "map",
        "sources",
        "rungs",
        "closureJoins",
        "snapshotJoins",
        "nestedRecords",
        "nestedIdentities",
        "blobJoins",
        "languageVersionBinding",
        "coverageTotality",
        "anchorLaw",
        "bodyIdentityJoin",
        "selectionCardinality",
        "changedIdentifierMajors",
        "newIdentifierDomains",
        "policyUniverseMap",
        "basenames",
        "releaseDeclarationRegistry",
        "capabilityIdLaw",
    ):
        if table_key in value:
            nested = value[table_key]
            rows.append(
                {
                    "parentPointer": parent_ptr,
                    "keyword": keyword,
                    "nestedKey": table_key,
                    "nestedPointer": parent_ptr + "/" + table_key,
                    "shape": type(nested).__name__,
                    "n": len(nested) if isinstance(nested, (dict, list)) else None,
                    "keys": list(nested.keys())[:80] if isinstance(nested, dict) else None,
                }
            )
            if isinstance(nested, dict):
                for nk, nv in nested.items():
                    if isinstance(nv, dict):
                        rows.extend(
                            flatten_table(
                                keyword + "." + table_key + "." + str(nk),
                                nv,
                                parent_ptr + "/" + table_key + "/" + str(nk).replace("/", "~1"),
                            )
                        )
            if isinstance(nested, list):
                for i, nv in enumerate(nested):
                    if isinstance(nv, dict):
                        rows.extend(
                            flatten_table(
                                keyword + "." + table_key + f"[{i}]",
                                nv,
                                parent_ptr + "/" + table_key + f"/{i}",
                            )
                        )
    return rows


# schemas the TS pilot actually binds (from constructor + identity registry)
SELECTED = [
    ("docs/coop/design-corrections/foundation/identity-schemas.v3.json", "urn:opensip:product-v1:identity:v3"),
    ("docs/coop/design-corrections/native/native-evidence.schemas.v2.json", "urn:opensip:product-v1:native:evidence-schemas:v2"),
    ("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json", "opensip.product.relation-payload.2"),
    ("docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json", "opensip.product.enumeration-plan.1"),
    ("docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json", None),
    ("docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json", "opensip.product.execution-inputs.1"),
    ("docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json", "opensip.product.subject-inventory.1"),
    ("docs/coop/design-corrections/foundation/target-attribution.schema.v2.json", "opensip.product.target-attribution.2"),
    ("docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json", "urn:opensip:product-v1:policy-document:2"),
    ("docs/coop/design-corrections/workflows/schemas/policy-document.schema.json", "urn:opensip:product-v1:workflows:policy-document"),
    ("docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json", "urn:opensip:product-v1:workflows:imported-evidence"),
    ("docs/coop/design-corrections/foundation/product-configuration.schema.v2.json", "urn:opensip:product-configuration:2"),
    ("docs/coop/design-corrections/native/capability-manifest-domains.v2.json", "opensip.native.capability-manifest-domains.2"),
    ("docs/coop/design-corrections/native/native-capability-matrix.v2.json", None),
    ("docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json", "opensip.product.provider-target-attribution-return.2"),
    ("docs/coop/design-corrections/foundation/evaluator-fault-observation.schema.v3.json", None),
    ("docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json", None),
    ("docs/coop/design-corrections/native/occupancy-companion.schema.v1.json", None),
    ("docs/coop/design-corrections/native/fact-batch.schema.v3.json", None),
]


def main():
    documents = []
    all_hits = []
    nested = []
    for rel, sid in SELECTED:
        p = KIT / rel
        if not p.exists():
            documents.append({"path": rel, "missing": True})
            continue
        data = json.loads(p.read_text())
        hits = []
        walk_ann(data, [], hits)
        documents.append(
            {
                "path": rel,
                "schemaId": data.get("$id") or sid,
                "bytes": p.stat().st_size,
                "annotationCount": len(hits),
                "topLevelXOpensip": [k for k in data if str(k).startswith("x-opensip-")],
            }
        )
        for h in hits:
            rec = {
                "kitPath": rel,
                "schemaId": data.get("$id") or sid,
                "pointer": h["pointer"],
                "keyword": h["keyword"],
                "valueType": type(h["value"]).__name__,
                "value": h["value"],
            }
            all_hits.append(rec)
            if isinstance(h["value"], dict):
                nested.extend(
                    [
                        {**n, "kitPath": rel, "schemaId": rec["schemaId"], "rootKeyword": h["keyword"]}
                        for n in flatten_table(h["keyword"], h["value"], h["pointer"])
                    ]
                )

    # classify keywords
    by_kw = {}
    for h in all_hits:
        by_kw.setdefault(h["keyword"], 0)
        by_kw[h["keyword"]] += 1

    out = {
        "standing": "Unfiltered mechanical inventory of x-opensip-* on schemas selected by the TS pilot. Not coverage.",
        "documentCount": len(documents),
        "annotationCount": len(all_hits),
        "nestedTableRows": len(nested),
        "keywordHistogram": by_kw,
        "documents": documents,
        "annotations": all_hits,
        "nestedLawTables": nested,
    }
    dest = OUT / "inventory" / "x-opensip-inventory.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2, sort_keys=False) + "\n")
    print("wrote", dest, "annotations", len(all_hits), "nested", len(nested), "keywords", sorted(by_kw))


if __name__ == "__main__":
    main()
