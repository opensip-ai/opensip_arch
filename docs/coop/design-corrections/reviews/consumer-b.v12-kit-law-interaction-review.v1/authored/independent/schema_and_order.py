"""Stock JSON Schema + x-opensip-order against THIS origin's kit registry."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from independent.kit_core import AdmissionError, C

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/subject")
DOCS = KIT / "docs/coop/design-corrections"

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


def load_json(rel: str) -> dict:
    p = DOCS / rel if not rel.startswith("docs/") else KIT / rel
    if not p.exists() and rel.startswith("docs/"):
        p = KIT / rel
    if not p.exists():
        p = DOCS / rel
    return json.loads(p.read_text())


def kit_rel(rel: str) -> Path:
    if rel.startswith("docs/"):
        return KIT / rel
    return DOCS / rel


def all_schema_docs() -> list[tuple[str, dict]]:
    out = []
    for p in KIT.rglob("*.json"):
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        if isinstance(d, dict) and d.get("$id"):
            out.append((str(p.relative_to(KIT)), d))
    return out


_REG = None
_DOCS_BY_ID = None
_DOCS_BY_REL = None


def registry():
    global _REG, _DOCS_BY_ID, _DOCS_BY_REL
    if _REG is None:
        resources = []
        _DOCS_BY_ID = {}
        _DOCS_BY_REL = {}
        for rel, doc in all_schema_docs():
            sid = doc["$id"]
            resources.append((sid, Resource.from_contents(doc)))
            _DOCS_BY_ID[sid] = (rel, doc)
            _DOCS_BY_REL[rel] = doc
            # also index short design-corrections relative
            if "docs/coop/design-corrections/" in rel:
                short = rel.split("docs/coop/design-corrections/", 1)[1]
                _DOCS_BY_REL[short] = doc
        _REG = Registry().with_resources(resources)
    return _REG


def resolve_schema_rel(rel: str) -> tuple[str, dict]:
    registry()
    if rel in _DOCS_BY_REL:
        doc = _DOCS_BY_REL[rel]
        return rel, doc
    p = kit_rel(rel)
    doc = json.loads(p.read_text())
    return rel, doc


def check_order(arr: list, annotation, *, path: str) -> None:
    if not isinstance(arr, list):
        raise AdmissionError("ORDER_NOT_ARRAY", path, path=path)
    if annotation is None or annotation == "sequence":
        return
    if annotation == "canonical-set":
        keys = [C(x) for x in arr]
        if len(keys) != len(set(keys)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} canonical-set unique", path=path)
        if keys != sorted(keys):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} canonical-set sorted", path=path)
        return
    if annotation == "canonical-order":
        keys = [C(x) for x in arr]
        if keys != sorted(keys):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} canonical-order", path=path)
        return
    if annotation == "utf8":
        if any(type(x) is not str for x in arr):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} utf8 strings", path=path)
        keys = [x.encode("utf-8") for x in arr]
        if len(keys) != len(set(keys)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} utf8 unique", path=path)
        if keys != sorted(keys):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} utf8 sorted", path=path)
        return
    if annotation == "path":
        paths = []
        for x in arr:
            if type(x) is dict and "path" in x:
                paths.append(x["path"])
            elif type(x) is str:
                paths.append(x)
            else:
                raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} path field", path=path)
        if len(paths) != len(set(paths)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} duplicate paths", path=path)
        b = [p.encode("utf-8") for p in paths]
        if b != sorted(b):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} path sorted", path=path)
        return
    if annotation == "numeric":
        if any(type(x) is not int or type(x) is bool for x in arr):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} numeric", path=path)
        if len(arr) != len(set(arr)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} numeric unique", path=path)
        if arr != sorted(arr):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} numeric sorted", path=path)
        return
    if annotation == "ordinal":
        for i, x in enumerate(arr):
            if not isinstance(x, dict) or x.get("ordinal") != i:
                raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} ordinal {i}", path=path)
        return
    if annotation == "predicate":
        keys = []
        for x in arr:
            t = (x["ruleId"], x["subjectId"], x["predicateId"])
            keys.append("\0".join(t).encode("utf-8"))
        if len(keys) != len(set(keys)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} predicate unique", path=path)
        if keys != sorted(keys):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} predicate sorted", path=path)
        return
    if annotation in ("ruleId", "waiverId"):
        vals = [x[annotation] for x in arr]
        if len(vals) != len(set(vals)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} {annotation} unique", path=path)
        b = [v.encode("utf-8") for v in vals]
        if b != sorted(b):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} {annotation} sorted", path=path)
        return
    if isinstance(annotation, dict) and "by" in annotation:
        by = annotation["by"]
        keys = []
        for x in arr:
            tup = tuple(str(x[k]) for k in by)
            keys.append("\0".join(tup).encode("utf-8"))
        if len(keys) != len(set(keys)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} by unique", path=path)
        if keys != sorted(keys):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path} by sorted", path=path)
        return
    raise AdmissionError("ORDER_VOCABULARY", f"{path}: {annotation!r} outside closed vocabulary", path=path)


def _resolve_ref(schema: dict, doc: dict) -> dict:
    if not isinstance(schema, dict) or "$ref" not in schema:
        return schema
    ref = schema["$ref"]
    extra = {k: v for k, v in schema.items() if k != "$ref"}
    if ref.startswith("#/$defs/"):
        name = ref.split("/")[-1]
        merged = dict(doc.get("$defs", {}).get(name) or {})
        merged.update(extra)
        return merged
    if ref.startswith("#/"):
        cur = doc
        for part in ref[2:].split("/"):
            cur = cur[part]
        merged = dict(cur) if isinstance(cur, dict) else {"const": cur}
        merged.update(extra)
        return merged
    if ref == "#":
        merged = dict(doc)
        merged.update(extra)
        return merged
    # cross-document
    if "#" in ref:
        sid, frag = ref.split("#", 1)
        registry()
        if sid in _DOCS_BY_ID:
            _, other = _DOCS_BY_ID[sid]
            if frag.startswith("/$defs/"):
                name = frag.split("/")[-1]
                merged = dict(other.get("$defs", {}).get(name) or {})
                merged.update(extra)
                return merged
    return schema


def walk_order(instance: Any, schema: dict, doc: dict, *, path: str) -> list[dict]:
    hits = []
    schema = _resolve_ref(schema, doc)
    if not isinstance(schema, dict):
        return hits
    if "allOf" in schema:
        for sub in schema["allOf"]:
            hits.extend(walk_order(instance, sub, doc, path=path))
    if "anyOf" in schema:
        for sub in schema["anyOf"]:
            hits.extend(walk_order(instance, sub, doc, path=path))
    if "oneOf" in schema:
        for sub in schema["oneOf"]:
            hits.extend(walk_order(instance, sub, doc, path=path))
    t = schema.get("type")
    if t == "array" and isinstance(instance, list):
        ann = schema.get("x-opensip-order")
        if ann is not None:
            check_order(instance, ann, path=path)
            hits.append({"path": path, "order": ann, "n": len(instance)})
        items = schema.get("items") or {}
        for i, el in enumerate(instance):
            hits.extend(walk_order(el, items, doc, path=f"{path}[{i}]"))
    if t == "object" and isinstance(instance, dict):
        props = schema.get("properties") or {}
        addl = schema.get("additionalProperties")
        for k, v in instance.items():
            if k in props:
                hits.extend(walk_order(v, props[k], doc, path=f"{path}.{k}"))
            elif isinstance(addl, dict):
                hits.extend(walk_order(v, addl, doc, path=f"{path}.{k}"))
    return hits


def validate_against(instance: Any, schema_rel: str, *, selector: str | None = None, label: str = "") -> dict:
    rel, doc = resolve_schema_rel(schema_rel)
    if selector and selector.startswith("#/$defs/"):
        name = selector.split("/")[-1]
        schema = doc["$defs"][name]
        val_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": (doc.get("$id") or "urn:local") + "/inline-" + name,
            "$defs": doc.get("$defs", {}),
            **schema,
        }
    elif selector in (None, "#"):
        schema = doc
        val_schema = doc
    else:
        raise AdmissionError("SCHEMA_SELECTOR", selector)
    errors = []
    try:
        v = Draft202012Validator(val_schema, registry=registry())
        for e in v.iter_errors(instance):
            errors.append({"path": list(e.absolute_path), "message": e.message, "validator": e.validator})
    except Exception as ex:
        errors.append({"path": [], "message": str(ex), "validator": "setup"})
    order_err = None
    try:
        walk_order(instance, schema if selector and selector.startswith("#/$defs/") else doc, doc, path=label or "$")
    except AdmissionError as e:
        order_err = e.as_dict()
        errors.append(order_err)
    return {
        "label": label,
        "schema": rel,
        "selector": selector,
        "stockOk": not errors,
        "errors": errors[:12],
        "orderError": order_err,
    }


def file_sha256(rel: str) -> str:
    import hashlib

    p = kit_rel(rel)
    return hashlib.sha256(p.read_bytes()).hexdigest()
