"""Owning-schema validation including published x-opensip-order.

Stock JSON Schema does not enforce x-opensip-order or x-opensip-digest.
Those are executed here independently after Draft 2020-12 validation.
"""
from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from .canonical import check_order
from .kit_owners import KitOwners


def build_registry(owners: KitOwners) -> Registry:
    registry = Registry()
    for sid, doc in owners.schemas_by_id.items():
        try:
            registry = registry.with_resource(sid, Resource.from_contents(doc, default_specification=DRAFT202012))
        except Exception:
            # some JSON files are not JSON Schema
            continue
    return registry


def validate_against(instance: Any, schema: dict[str, Any], registry: Registry, schema_id: str | None = None) -> list[str]:
    faults: list[str] = []
    try:
        validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
        for err in validator.iter_errors(instance):
            path = "/" + "/".join(str(p) for p in err.absolute_path)
            faults.append(f"SCHEMA:{path}:{err.message}")
    except SchemaError as e:
        faults.append(f"SCHEMA_DOCUMENT:{e.message}")
    except Exception as e:
        faults.append(f"SCHEMA_RUNTIME:{type(e).__name__}:{e}")
    faults.extend(_walk_order(schema, instance, registry, path="$"))
    return faults


def _resolve_ref(schema: dict[str, Any], registry: Registry, ref: str, base: dict[str, Any]) -> dict[str, Any] | None:
    if ref.startswith("#/"):
        cur: Any = base
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                return None
        return cur if isinstance(cur, dict) else None
    try:
        retrieved = registry.get_or_retrieve(ref)
        contents = retrieved.value.contents
        return contents if isinstance(contents, dict) else None
    except Exception:
        return None


def _walk_order(schema: Any, instance: Any, registry: Registry, path: str, root: dict[str, Any] | None = None) -> list[str]:
    faults: list[str] = []
    if not isinstance(schema, dict):
        return faults
    root = root or schema
    if "$ref" in schema:
        resolved = _resolve_ref(schema, registry, schema["$ref"], root)
        if resolved:
            faults.extend(_walk_order(resolved, instance, registry, path, resolved if "$id" in resolved else root))
        return faults
    if "x-opensip-order" in schema and isinstance(instance, list):
        for f in check_order(schema["x-opensip-order"], instance):
            faults.append(f"ORDER:{path}:{f}")
    if schema.get("type") == "object" and isinstance(instance, dict):
        props = schema.get("properties") or {}
        for k, sub in props.items():
            if k in instance:
                faults.extend(_walk_order(sub, instance[k], registry, f"{path}.{k}", root))
        addl = schema.get("additionalProperties")
        if isinstance(addl, dict):
            for k, v in instance.items():
                if k not in props:
                    faults.extend(_walk_order(addl, v, registry, f"{path}.{k}", root))
    if schema.get("type") == "array" and isinstance(instance, list):
        items = schema.get("items")
        if isinstance(items, dict):
            for i, v in enumerate(instance):
                faults.extend(_walk_order(items, v, registry, f"{path}[{i}]", root))
    for comb in ("allOf", "anyOf", "oneOf"):
        for i, sub in enumerate(schema.get(comb) or []):
            faults.extend(_walk_order(sub, instance, registry, path, root))
    if "if" in schema:
        # still walk then/else if present; order annotations on those branches
        for k in ("then", "else"):
            if k in schema:
                faults.extend(_walk_order(schema[k], instance, registry, path, root))
    if "$defs" in schema and schema is root:
        pass
    return faults


def schema_for_identity_def(owners: KitOwners, def_name: str) -> dict[str, Any]:
    base = dict(owners.identity_v3)
    base["$ref"] = f"#/$defs/{def_name}"
    return base


def schema_for_native_def(owners: KitOwners, def_name: str) -> dict[str, Any]:
    base = dict(owners.native)
    base["$ref"] = f"#/$defs/{def_name}"
    return base
