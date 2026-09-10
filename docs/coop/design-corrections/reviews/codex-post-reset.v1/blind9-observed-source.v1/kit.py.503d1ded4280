"""Kit loader: pinned schema documents, registries, and the local $ref closure.

Every document is read from the verified consumer kit only.  Nothing is
retrieved from the network (identity S3: "transitive references are resolved
through the pinned registry closure without network retrieval").
"""
from __future__ import annotations

import hashlib
import json
import os

import jsonschema
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

KIT = os.environ.get(
    "OPENSIP_KIT",
    "/tmp/opensip-design-corrections/consumer-b.v9/subject")

DOCS = {
    "identity":            "docs/coop/design-corrections/foundation/identity-schemas.v2.json",
    "relation":            "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
    "native":              "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "capability-domains":  "docs/coop/design-corrections/native/capability-manifest-domains.v2.json",
    "capability-matrix":   "docs/coop/design-corrections/native/native-capability-matrix.v2.json",
    "policy-document":     "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
    "common":              "docs/coop/design-corrections/workflows/schemas/common.schema.json",
    "imported-evidence":   "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
    "test-execution":      "docs/coop/design-corrections/workflows/schemas/test-execution.schema.json",
    "command-envelope":    "docs/coop/design-corrections/workflows/schemas/command-envelope.schema.json",
    "command-inventory":   "docs/coop/design-corrections/workflows/schemas/command-inventory.schema.json",
    "comparison-result":   "docs/coop/design-corrections/workflows/schemas/comparison-result.schema.json",
    "invocation-record":   "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json",
    "repair":              "docs/coop/design-corrections/workflows/schemas/repair.schema.json",
    "baseline-artifact":   "docs/coop/design-corrections/workflows/schemas/baseline-artifact.schema.json",
    "policy-test":         "docs/coop/design-corrections/workflows/schemas/policy-test.schema.json",
    "graph-query":         "docs/coop/design-corrections/workflows/schemas/graph-query.schema.json",
    "review":              "docs/coop/design-corrections/workflows/schemas/review.schema.json",
    "import-source-context": "docs/coop/design-corrections/foundation/import-source-context.schema.json",
    "product-configuration": "docs/coop/design-corrections/foundation/product-configuration.schema.v2.json",
    "resolved-inputs":     "docs/coop/artifacts/resolved-inputs.v2.json",
    "fact-identity-policy": "docs/coop/artifacts/fact-identity-policy.v2.json",
    "protocol3":           "docs/coop/design-corrections/native/protocol3-transitions.v1.json",
    "public-detail-registry": "docs/coop/design-corrections/public-detail-registry.v1.json",
    "d9":                  "docs/coop/artifacts/d9-exit-contract.v1.14.json",
    "permission-truth":    "docs/coop/artifacts/permission-truth-tables.v9.json",
    "delivery":            "docs/coop/artifacts/delivery.v4.json",
    "fact-plane":          "docs/coop/artifacts/fact-plane.v1.json",
}

_bytes: dict[str, bytes] = {}
_json: dict[str, dict] = {}
for key, rel in DOCS.items():
    with open(os.path.join(KIT, rel), "rb") as fh:
        _bytes[key] = fh.read()
    _json[key] = json.loads(_bytes[key].decode("utf-8"))


def doc(key: str) -> dict:
    return _json[key]


def doc_bytes(key: str) -> bytes:
    return _bytes[key]


def doc_path(key: str) -> str:
    return DOCS[key]


def doc_digest(key: str) -> str:
    """raw SHA-256 of the EXACT FULL schema document bytes."""
    return hashlib.sha256(_bytes[key]).hexdigest()


# --- jsonschema registry over the pinned local closure -----------------------

_resources = []
for key, data in _json.items():
    if isinstance(data, dict) and "$schema" in data and "$id" in data:
        _resources.append((data["$id"], Resource.from_contents(data)))
REGISTRY = Registry().with_resources(_resources)


def validator_for(doc_key: str, selector: str) -> Draft202012Validator:
    """A validator for `document#selector`, resolved through the pinned closure."""
    base = _json[doc_key]
    if selector in ("#", ""):
        schema = dict(base)
    else:
        node = base
        for part in selector.lstrip("#/").split("/"):
            node = node[part]
        schema = dict(node)
        schema.setdefault("$schema", "https://json-schema.org/draft/2020-12/schema")
        if "$id" in base:
            schema["$id"] = base["$id"] + "#anon-selector"
            # keep the parent document reachable for local "#/$defs/..." refs
            schema = {"$schema": schema["$schema"],
                      "$id": base["$id"] + "#anon-selector",
                      "$ref": base["$id"] + selector}
    return Draft202012Validator(schema, registry=REGISTRY)


_validator_cache: dict[tuple[str, str], Draft202012Validator] = {}


def validate(doc_key: str, selector: str, instance, where: str = ""):
    ck = (doc_key, selector)
    v = _validator_cache.get(ck)
    if v is None:
        v = validator_for(doc_key, selector)
        _validator_cache[ck] = v
    errors = sorted(v.iter_errors(instance), key=lambda e: list(e.absolute_path))
    if errors:
        e = errors[0]
        loc = "/".join(str(p) for p in e.absolute_path)
        raise SchemaRefusal(
            f"SCHEMA_INVALID[{doc_key}{selector}] {where} at '{loc}': {e.message}")


class SchemaRefusal(Exception):
    pass


# --- normative registries ----------------------------------------------------

IDENTITY = _json["identity"]
DIGEST_DOMAINS = IDENTITY["x-opensip-digest-domains"]
BY_DOMAIN = DIGEST_DOMAINS["byDomain"]
DOMAIN_SETS = DIGEST_DOMAINS["domainSets"]
PAYLOAD_REGISTRY = IDENTITY["x-opensip-payload-registry"]

RELATION_REGISTRY = _json["relation"]["x-opensip-relation-registry"]
RELATIONS = RELATION_REGISTRY["relations"]

NATIVE = _json["native"]
GRAMMAR_CAPS = NATIVE["x-opensip-grammar-capability-registry"]
DEFICIENCY_CAUSE = NATIVE["x-opensip-deficiency-cause-registry"]
CONFIG_NODE_KIND_LAW = NATIVE["x-opensip-config-node-kind-law"]
PUBLIC_ROUTES = NATIVE["x-opensip-public-route-registry"]

SCOPE_CAPABILITY_LAW = DIGEST_DOMAINS["scopeCapabilityLaw"]
LANGUAGE_MODES = DIGEST_DOMAINS["languageModes"]["map"]
CLOSURE_KINDS = DIGEST_DOMAINS["closureKinds"]["byField"]
CLOSURE_MEMBERSHIP = DIGEST_DOMAINS["closureMembership"]

CVE1 = _json["resolved-inputs"]["planIdContract"]["canonicalValueEncoding"]

# The five resolved rungs (native S4.3 RC-1).
RESOLVED_RUNGS = {"resolved-target", "resolved-binding", "resolved-callee",
                  "checked", "from-resolved-calls"}

INVENTORY_CAPABILITIES = {"file@enumerated", "package@manifest-declared",
                          "vcs-change@vcs-reported"}

# Which document each identity domain's payload validates against.
IDENTITY_DOMAIN_SELECTOR = {
    "snapshot": ("identity", "#/$defs/snapshot"),
    "closure": ("identity", "#/$defs/closure"),
    "import": ("identity", "#/$defs/import"),
    "plan": ("identity", "#/$defs/plan"),
    "subject-scope": ("identity", "#/$defs/subject-scope"),
    "coverage": ("identity", "#/$defs/coverage"),
    "view": ("identity", "#/$defs/view"),
    "execution-plan": ("identity", "#/$defs/execution-plan"),
    "finding-fingerprint": ("identity", "#/$defs/finding-fingerprint"),
    "finding": ("identity", "#/$defs/finding"),
    "proof-bundle": ("identity", "#/$defs/proof-bundle"),
    "semantic-evidence": ("identity", "#/$defs/semantic-evidence"),
    "evaluation-seal": ("identity", "#/$defs/evaluation-seal"),
    "run": ("identity", "#/$defs/run"),
    "cache-key": ("identity", "#/$defs/cache-key"),
    "regeneration-key": ("identity", "#/$defs/regeneration-key"),
    "policy-derivation": ("identity", "#/$defs/policy-derivation"),
    "fact": ("identity", "#/$defs/fact"),
}

DOMAIN_PREFIX = {
    "snapshot": "snapshot2", "closure": "closure2", "import": "import2",
    "plan": "plan2", "subject-scope": "scope2", "coverage": "coverage2",
    "view": "view2", "execution-plan": "exec-plan2",
    "finding-fingerprint": "finding-key2", "finding": "finding2",
    "proof-bundle": "proof2", "semantic-evidence": "evidence2",
    "evaluation-seal": "seal2", "run": "run2", "fact": "fact2",
    "cache-key": "cache2", "regeneration-key": "regen2",
    "policy-derivation": "policy-derivation2",
}
