"""Schema validation of every constructed descriptor against the kit's own
closed schemas, through a pinned local registry closure with no network."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import jsonschema
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

SUBJECT = "/tmp/opensip-design-corrections/consumer-b.v3/subject"
PATHS = {
    "identity": "docs/coop/design-corrections/foundation/identity-schemas.v2.json",
    "relation": "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
    "native": "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "common": "docs/coop/design-corrections/workflows/schemas/common.schema.json",
    "policy": "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
    "imported": "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
    "invocation": "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json",
    "repair": "docs/coop/design-corrections/workflows/schemas/repair.schema.json",
    "test-execution": "docs/coop/design-corrections/workflows/schemas/test-execution.schema.json",
    "comparison": "docs/coop/design-corrections/workflows/schemas/comparison-result.schema.json",
    "envelope": "docs/coop/design-corrections/workflows/schemas/command-envelope.schema.json",
    "review": "docs/coop/design-corrections/workflows/schemas/review.schema.json",
    "policy-test": "docs/coop/design-corrections/workflows/schemas/policy-test.schema.json",
    "baseline": "docs/coop/design-corrections/workflows/schemas/baseline-artifact.schema.json",
    "graph-query": "docs/coop/design-corrections/workflows/schemas/graph-query.schema.json",
    "importsrc": "docs/coop/design-corrections/foundation/import-source-context.schema.json",
}
DOCS = {k: json.load(open(os.path.join(SUBJECT, v))) for k, v in PATHS.items()}

_resources = []
for key, doc in DOCS.items():
    if "$id" in doc:
        _resources.append((doc["$id"], Resource.from_contents(doc, DRAFT202012)))
REGISTRY = Registry().with_resources(_resources)


def validator(doc_key, selector):
    doc = DOCS[doc_key]
    schema = dict(doc)
    schema.pop("$id", None)
    if selector != "#":
        node = doc
        for part in selector.lstrip("#/").split("/"):
            node = node[part.replace("~1", "/").replace("~0", "~")]
        schema = dict(node)
        schema["$defs"] = doc.get("$defs", {})
        schema["$id"] = doc.get("$id", "urn:cb:anon") + "#cb-selected"
        # keep the original document reachable for local $ref resolution
        reg = REGISTRY.with_resource(
            schema["$id"], Resource.from_contents(schema, DRAFT202012))
        return jsonschema.Draft202012Validator(schema, registry=reg)
    return jsonschema.Draft202012Validator(schema, registry=REGISTRY)


_CACHE = {}


def check(doc_key, selector, instance, label):
    k = (doc_key, selector)
    if k not in _CACHE:
        _CACHE[k] = validator(doc_key, selector)
    errs = sorted(_CACHE[k].iter_errors(instance), key=lambda e: list(e.path))
    return {"label": label, "document": PATHS[doc_key], "selector": selector,
            "valid": not errs,
            "errors": [f"{list(e.path)}: {e.message}" for e in errs[:6]]}
