"""Stock JSON Schema plus published x-opensip-order. Digest joins are separate closure."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from helper.errors import AdmissionError
from helper.order import walk_schema_order

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v5/subject")

try:
    import jsonschema
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError as e:  # pragma: no cover
    jsonschema = None
    Draft202012Validator = None
    Registry = None
    Resource = None
    _IMPORT_ERR = e
else:
    _IMPORT_ERR = None


def _load(rel: str) -> dict:
    return json.loads((KIT / rel).read_text())


def kit_registry() -> Any:
    if Registry is None:
        raise RuntimeError(f"jsonschema not available: {_IMPORT_ERR}")
    files = [
        "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
        "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
        "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
        "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
        "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json",
        "docs/coop/design-corrections/workflows/schemas/common.schema.json",
        "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
        "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json",
        "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
        "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json",
        "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/command-inventory.schema.json",
        "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json",
        "docs/coop/design-corrections/workflows/schemas/repair.schema.json",
        "docs/coop/design-corrections/foundation/target-attribution.schema.v1.json",
        "docs/coop/design-corrections/workflows/schemas/test-execution.schema.json",
    ]
    resources = []
    for f in files:
        doc = _load(f)
        sid = doc.get("$id")
        if sid:
            resources.append((sid, Resource.from_contents(doc)))
    reg = Registry().with_resources(resources)
    return reg


_REG = None


def registry():
    global _REG
    if _REG is None:
        _REG = kit_registry()
    return _REG


def validate_against(instance: Any, schema_rel: str, *, selector: str | None = None, label: str = "") -> dict:
    doc = _load(schema_rel)
    schema = doc
    if selector:
        if not selector.startswith("#/$defs/"):
            if selector == "#":
                schema = doc
            else:
                raise AdmissionError("SCHEMA_SELECTOR", selector)
        else:
            name = selector.split("/")[-1]
            schema = doc["$defs"][name]
    # $id of fragment validators: use document as root for $ref
    root = dict(doc)
    # Validate instance against a wrapper that $refs the def when needed
    if selector and selector.startswith("#/$defs/"):
        check_schema = {"$ref": selector}
        # Draft202012Validator needs the full document as schema with $id
        val_schema = {**doc, "$ref": selector}
        # Can't put $ref at root alongside $defs easily in some libs; use:
        val_schema = {
            "$schema": doc.get("$schema"),
            "$id": doc.get("$id", "") + "#validate-" + selector.split("/")[-1],
            "$ref": selector if False else doc.get("$id", "") + selector,
            # better: inline
        }
        val_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$defs": doc.get("$defs", {}),
            **{k: v for k, v in schema.items()},
        }
        # If schema is a def, just use it with parent $defs
        val_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": (doc.get("$id") or "urn:local") + "/inline",
            "$defs": doc.get("$defs", {}),
            **schema,
        }
    else:
        val_schema = doc
    errors = []
    if Draft202012Validator is None:
        raise RuntimeError("jsonschema missing")
    try:
        v = Draft202012Validator(val_schema, registry=registry())
        for e in v.iter_errors(instance):
            errors.append({"path": list(e.absolute_path), "message": e.message, "validator": e.validator})
    except Exception as ex:
        errors.append({"path": [], "message": str(ex), "validator": "setup"})
    order_err = None
    try:
        walk_schema_order(instance, schema if selector else doc, doc.get("$defs") or schema.get("$defs") or {}, path=label or "$")
    except AdmissionError as e:
        order_err = e.as_dict()
        errors.append(order_err)
    return {
        "label": label,
        "schema": schema_rel,
        "selector": selector,
        "stockOk": all(e.get("validator") not in ("setup",) and "code" not in e for e in errors) and order_err is None and not errors,
        "errors": errors,
        "orderError": order_err,
        "note": "Stock JSON Schema does not enforce x-opensip-digest joins; those are closure.",
    }
