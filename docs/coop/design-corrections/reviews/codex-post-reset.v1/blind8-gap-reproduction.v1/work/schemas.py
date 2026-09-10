"""Pinned local schema closure + exact typed validation.

The payload registry law (identity-schemas.v2#/x-opensip-payload-registry) says
validation resolves "through the pinned local registry closure with no network
retrieval".  This module builds that closure from the kit only.
"""
from __future__ import annotations

import json

import jsonschema
import referencing
from referencing.jsonschema import DRAFT202012

from osip import KIT, doc_bytes

DOCS = {
    "identity": "docs/coop/design-corrections/foundation/identity-schemas.v2.json",
    "relation": "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
    "native": "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "common": "docs/coop/design-corrections/workflows/schemas/common.schema.json",
    "policy-document": "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
    "imported-evidence": "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
    "test-execution": "docs/coop/design-corrections/workflows/schemas/test-execution.schema.json",
    "invocation-record": "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json",
    "command-envelope": "docs/coop/design-corrections/workflows/schemas/command-envelope.schema.json",
    "command-inventory": "docs/coop/design-corrections/workflows/schemas/command-inventory.schema.json",
    "comparison-result": "docs/coop/design-corrections/workflows/schemas/comparison-result.schema.json",
    "baseline-artifact": "docs/coop/design-corrections/workflows/schemas/baseline-artifact.schema.json",
    "repair": "docs/coop/design-corrections/workflows/schemas/repair.schema.json",
    "review": "docs/coop/design-corrections/workflows/schemas/review.schema.json",
    "policy-test": "docs/coop/design-corrections/workflows/schemas/policy-test.schema.json",
    "graph-query": "docs/coop/design-corrections/workflows/schemas/graph-query.schema.json",
    "import-source-context": "docs/coop/design-corrections/foundation/import-source-context.schema.json",
    "product-configuration": "docs/coop/design-corrections/foundation/product-configuration.schema.v2.json",
    "security": "docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json",
}

LOADED = {}
BY_ID = {}
for name, rel in DOCS.items():
    d = json.loads(doc_bytes(rel).decode("utf-8"))
    LOADED[name] = d
    if d.get("$id"):
        BY_ID[d["$id"]] = d

_resources = [(i, DRAFT202012.create_resource(d)) for i, d in BY_ID.items()]
REGISTRY = referencing.Registry().with_resources(_resources)


# ---- exact typed const/enum ------------------------------------------------
# admission-and-qualification section 1: "an already-decoded 1.0 or True cannot
# satisfy const:1".  Python's == makes True == 1, so const/enum are overridden.

def _same(a, b):
    if type(a) is bool or type(b) is bool:
        return a is b
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    if a is None or b is None:
        return a is None and b is None
    return False


def _const(validator, const, instance, schema):
    if not _same(instance, const):
        yield jsonschema.exceptions.ValidationError(
            "%r is not the exact const %r" % (instance, const))


def _enum(validator, enums, instance, schema):
    if not any(_same(instance, e) for e in enums):
        yield jsonschema.exceptions.ValidationError(
            "%r is not one of %r (exact typed)" % (instance, enums))


Base = jsonschema.validators.validator_for({"$schema": "https://json-schema.org/draft/2020-12/schema"})
ExactValidator = jsonschema.validators.extend(Base, {"const": _const, "enum": _enum})


def validate(instance, doc: str, selector: str):
    """Validate `instance` against DOCS[doc] at JSON-pointer `selector`
    ('#/$defs/X' or '#').  Returns a list of error strings."""
    d = LOADED[doc]
    if selector in ("#", ""):
        schema = d
    else:
        assert selector.startswith("#/")
        schema = {"$ref": d["$id"] + selector}
    v = ExactValidator(schema, registry=REGISTRY)
    return ["%s: %s" % ("/".join(str(p) for p in e.absolute_path) or "<root>", e.message)
            for e in sorted(v.iter_errors(instance), key=lambda e: list(e.absolute_path))]
