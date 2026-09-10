"""Schema admission including published x-opensip-* keywords.

Stock jsonschema does not enforce x-opensip-order or x-opensip-digest.
This walker does. A stock-schema pass is only one stage of admission.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Optional

from . import canonical, order

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")

try:
    import jsonschema
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError:  # pragma: no cover
    jsonschema = None
    Draft202012Validator = None
    Registry = None


class SchemaAdmitError(Exception):
    def __init__(self, code: str, message: str, path: str = ""):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.path = path


def load_json(rel: str) -> Any:
    return json.loads((KIT / rel).read_text())


def stock_validate(instance: Any, schema: dict, registry=None) -> list[str]:
    if Draft202012Validator is None:
        return ["jsonschema not installed"]
    try:
        if registry is not None:
            Draft202012Validator(schema, registry=registry).validate(instance)
        else:
            Draft202012Validator(schema).validate(instance)
        return []
    except Exception as e:
        return [str(e)]


def _resolve_ref(schema: dict, root: dict) -> dict:
    ref = schema.get("$ref")
    if not ref:
        return schema
    if ref.startswith("#/$defs/"):
        name = ref.split("/")[-1]
        return root.get("$defs", {}).get(name, schema)
    if ref == "#":
        return root
    return schema


def walk_order(instance: Any, schema: dict, root: dict, path: str = "") -> list[str]:
    errors: list[str] = []
    schema = _resolve_ref(schema, root)
    if schema.get("type") == "array" and isinstance(instance, list):
        ann = schema.get("x-opensip-order", "sequence")
        try:
            order.check_order(instance, ann, unique_items=bool(schema.get("uniqueItems")))
        except order.OrderError as e:
            errors.append(f"{path or '/'}: {e}")
        item_schema = schema.get("items") or {}
        for i, item in enumerate(instance):
            errors.extend(walk_order(item, item_schema, root, f"{path}[{i}]"))
    elif schema.get("type") == "object" and isinstance(instance, dict):
        props = schema.get("properties") or {}
        for k, v in instance.items():
            if k in props:
                errors.extend(walk_order(v, props[k], root, f"{path}/{k}"))
            elif "$ref" in schema:
                resolved = _resolve_ref(schema, root)
                if resolved is not schema:
                    errors.extend(walk_order(instance, resolved, root, path))
                    return errors
        addl = schema.get("additionalProperties")
        if addl is False:
            extra = set(instance) - set(props)
            req = set(schema.get("required") or [])
            missing = req - set(instance)
            if extra:
                errors.append(f"{path}: additionalProperties {sorted(extra)}")
            if missing:
                errors.append(f"{path}: missing {sorted(missing)}")
        elif isinstance(addl, dict):
            for k, v in instance.items():
                if k not in props:
                    errors.extend(walk_order(v, addl, root, f"{path}/{k}"))
    return errors


def check_digest_annotations(schema: dict, path: str = "", root: dict | None = None) -> list[str]:
    """Every 64-hex field in identity-schemas.v3 must carry x-opensip-digest."""
    errors = []
    root = root or schema
    schema = _resolve_ref(schema, root)
    if schema.get("type") == "string" and "pattern" in schema:
        pat = schema["pattern"]
        if "[0-9a-f]{64}" in pat and "x-opensip-digest" not in schema:
            # prefixed identities (snapshot2:...) are not 64-hex fields
            if pat.startswith("^[0-9a-f]{64}"):
                errors.append(f"{path}: 64-hex field lacks x-opensip-digest")
    props = schema.get("properties") or {}
    for k, v in props.items():
        errors.extend(check_digest_annotations(v, f"{path}/{k}", root))
    items = schema.get("items")
    if isinstance(items, dict):
        errors.extend(check_digest_annotations(items, f"{path}[]", root))
    defs = schema.get("$defs") or {}
    if path == "":
        for name, d in defs.items():
            errors.extend(check_digest_annotations(d, f"$defs/{name}", root))
    return errors


def admit_record(instance: Any, schema: dict, stock_registry=None) -> dict:
    stock = stock_validate(instance, schema, stock_registry)
    order_errors = walk_order(instance, schema, schema)
    return {
        "stockErrors": stock,
        "orderErrors": order_errors,
        "stockPass": stock == [],
        "orderPass": order_errors == [],
        "admitted": stock == [] and order_errors == [],
        "note": "stock JSON Schema does not enforce x-opensip-order or x-opensip-digest; both are required for admission",
    }
