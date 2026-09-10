"""Kit loader + schema validation harness (pinned local closure, no network)."""
import hashlib
import json
import os

import jsonschema
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

KIT = "/tmp/opensip-design-corrections/consumer-b.v4/subject"

DOCS = {
    "identity": "docs/coop/design-corrections/foundation/identity-schemas.v2.json",
    "relation": "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
    "native": "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "matrix": "docs/coop/design-corrections/native/native-capability-matrix.v2.json",
    "capdomains": "docs/coop/design-corrections/native/capability-manifest-domains.v2.json",
    "common": "docs/coop/design-corrections/workflows/schemas/common.schema.json",
    "policy": "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
    "imported": "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
    "testexec": "docs/coop/design-corrections/workflows/schemas/test-execution.schema.json",
    "comparison": "docs/coop/design-corrections/workflows/schemas/comparison-result.schema.json",
    "invocation": "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json",
    "repair": "docs/coop/design-corrections/workflows/schemas/repair.schema.json",
    "envelope": "docs/coop/design-corrections/workflows/schemas/command-envelope.schema.json",
    "review": "docs/coop/design-corrections/workflows/schemas/review.schema.json",
    "policytest": "docs/coop/design-corrections/workflows/schemas/policy-test.schema.json",
    "baseline": "docs/coop/design-corrections/workflows/schemas/baseline-artifact.schema.json",
    "graphquery": "docs/coop/design-corrections/workflows/schemas/graph-query.schema.json",
    "cmdinv-schema": "docs/coop/design-corrections/workflows/schemas/command-inventory.schema.json",
    "cmdinv": "docs/coop/design-corrections/workflows/command-inventory.v1.json",
    "details": "docs/coop/design-corrections/public-detail-registry.v1.json",
    "importctx": "docs/coop/design-corrections/foundation/import-source-context.schema.json",
    "seclife": "docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json",
    "prodconfig": "docs/coop/design-corrections/foundation/product-configuration.schema.v2.json",
    "permtables": "docs/coop/artifacts/permission-truth-tables.v9.json",
    "delivery4": "docs/coop/artifacts/delivery.v4.json",
    "resolvedinputs": "docs/coop/artifacts/resolved-inputs.v2.json",
    "factidentity": "docs/coop/artifacts/fact-identity-policy.v2.json",
    "factplane": "docs/coop/artifacts/fact-plane.v1.json",
    "d9": "docs/coop/artifacts/d9-exit-contract.v1.14.json",
    "c2plan": "docs/coop/artifacts/c2-plan-stage-schema.v4.json",
}

_raw = {}
_doc = {}
for k, rel in DOCS.items():
    with open(os.path.join(KIT, rel), "rb") as fh:
        b = fh.read()
    _raw[k] = b
    _doc[k] = json.loads(b.decode("utf-8"))


def raw(name):
    return _raw[name]


def doc(name):
    return _doc[name]


def doc_digest(name):
    """raw-artifact: raw SHA-256 of the EXACT FULL document bytes."""
    return hashlib.sha256(_raw[name]).hexdigest()


def path_of(name):
    return DOCS[name]


_resources = {}
for k, d in _doc.items():
    if isinstance(d, dict) and "$id" in d and d["$id"]:
        _resources[d["$id"]] = Resource.from_contents(d, default_specification=DRAFT202012)
REGISTRY = Registry().with_resources(list(_resources.items()))


def validate(name, selector, instance):
    """Validate `instance` against document `name` at JSON-pointer `selector`.

    Selector is '#' or '#/$defs/X'. Refs resolve through the pinned local closure.
    """
    d = _doc[name]
    if selector in ("#", ""):
        schema = dict(d)
    else:
        ptr = selector.lstrip("#").lstrip("/")
        node = d
        for part in ptr.split("/"):
            node = node[part.replace("~1", "/").replace("~0", "~")]
        schema = dict(node)
        schema["$id"] = d.get("$id", "urn:local:" + name)
        # keep sibling $defs reachable for local "#/$defs/..." refs
        if "$defs" in d and "$defs" not in schema:
            schema["$defs"] = d["$defs"]
    v = jsonschema.Draft202012Validator(schema, registry=REGISTRY)
    errs = sorted(v.iter_errors(instance), key=lambda e: list(e.absolute_path))
    if errs:
        e = errs[0]
        raise ValueError("schema refusal %s%s at %s: %s" % (
            name, selector, list(e.absolute_path), e.message))
    return True
