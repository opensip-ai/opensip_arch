"""Draft 2020-12 schema validation against kit documents."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v10/subject")


def _collect_schemas() -> list[tuple[str, dict, Path]]:
    out = []
    for p in sorted((KIT / "docs").rglob("*.json")):
        try:
            obj = json.loads(p.read_text())
        except Exception:
            continue
        if isinstance(obj, dict) and obj.get("$schema") and (obj.get("$id") or "$defs" in obj):
            sid = obj.get("$id") or str(p)
            out.append((sid, obj, p))
    return out


_SCHEMAS = _collect_schemas()
_BY_ID = {sid: obj for sid, obj, _ in _SCHEMAS}
_BY_SUFFIX: dict[str, dict] = {}
for sid, obj, p in _SCHEMAS:
    _BY_SUFFIX[p.name] = obj
    rel = str(p.relative_to(KIT / "docs"))
    _BY_SUFFIX[rel] = obj


def _registry() -> Registry:
    reg = Registry()
    for sid, obj, _ in _SCHEMAS:
        reg = reg.with_resource(sid, Resource.from_contents(obj, default_specification=DRAFT202012))
    return reg


REGISTRY = _registry()


def schema_by_id(sid: str) -> dict:
    if sid not in _BY_ID:
        raise KeyError(sid)
    return _BY_ID[sid]


def validate_against(instance: Any, schema: dict, *, selector: str | None = None) -> list[str]:
    target = schema
    if selector:
        if not selector.startswith("#/"):
            raise ValueError(selector)
        cur: Any = schema
        for part in selector[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            cur = cur[part]
        target = cur
        if "$id" not in target:
            # keep parent $id for $ref resolution
            wrapped = {
                "$schema": schema.get("$schema", "https://json-schema.org/draft/2020-12/schema"),
                "$id": schema.get("$id", "urn:opensip:local"),
                "$defs": schema.get("$defs", {}),
                "type": target.get("type", "object"),
            }
            wrapped.update({k: v for k, v in target.items() if k != "$defs"})
            target = wrapped
    try:
        validator = Draft202012Validator(target, registry=REGISTRY)
    except Exception:
        validator = Draft202012Validator(target)
    errs = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '$'}: {e.message}" for e in errs]


def validate_def(instance: Any, document_rel: str, def_name: str) -> list[str]:
    p = KIT / "docs" / document_rel if not document_rel.startswith("/") else Path(document_rel)
    if not p.exists():
        p = KIT / document_rel
    schema = json.loads(p.read_text())
    return validate_against(instance, schema, selector=f"#/$defs/{def_name}")


def validate_root(instance: Any, document_rel: str) -> list[str]:
    p = KIT / "docs" / document_rel
    if not p.exists():
        p = KIT / document_rel
    schema = json.loads(p.read_text())
    return validate_against(instance, schema)
