"""x-opensip-order admission from identity-and-evidence §3 closed vocabulary."""
from __future__ import annotations

from typing import Any

from helper.canonical import C
from helper.errors import AdmissionError


def _item_bytes(item: Any) -> bytes:
    return C(item)


def check_order(arr: list, annotation, *, path: str) -> None:
    if not isinstance(arr, list):
        raise AdmissionError("ORDER_NOT_ARRAY", f"{path} not array")
    if annotation is None or annotation == "sequence":
        return
    if annotation == "canonical-set":
        keys = [_item_bytes(x) for x in arr]
        if len(keys) != len(set(keys)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: canonical-set requires unique items", path=path)
        if keys != sorted(keys):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: canonical-set not strictly ascending C bytes", path=path)
        return
    if annotation == "canonical-order":
        keys = [_item_bytes(x) for x in arr]
        if keys != sorted(keys):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: canonical-order not nondecreasing", path=path)
        return
    if annotation == "utf8":
        if any(type(x) is not str for x in arr):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: utf8 requires string items")
        keys = [x.encode("utf-8") for x in arr]
        if len(keys) != len(set(keys)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: utf8 unique")
        if keys != sorted(keys):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: utf8 not ascending")
        return
    if annotation == "path":
        paths = []
        for x in arr:
            if type(x) is dict and "path" in x:
                paths.append(x["path"])
            elif type(x) is str:
                paths.append(x)
            else:
                raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: path order needs path field")
        if len(paths) != len(set(paths)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: duplicate paths refuse")
        b = [p.encode("utf-8") for p in paths]
        if b != sorted(b):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: path not ascending UTF-8")
        return
    if annotation == "numeric":
        if any(type(x) is not int or type(x) is bool for x in arr):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: numeric requires integers")
        if len(arr) != len(set(arr)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: numeric unique")
        if arr != sorted(arr):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: numeric not ascending")
        return
    if annotation == "ordinal":
        for i, x in enumerate(arr):
            if not isinstance(x, dict) or x.get("ordinal") != i:
                raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: ordinal must be contiguous 0-based", path=path)
        return
    if annotation == "predicate":
        keys = []
        for x in arr:
            t = (x["ruleId"], x["subjectId"], x["predicateId"])
            keys.append("\0".join(t).encode("utf-8"))
        if len(keys) != len(set(keys)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: predicate unique")
        if keys != sorted(keys):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: predicate not ascending")
        return
    if annotation in ("ruleId", "waiverId"):
        key = annotation
        vals = [x[key] for x in arr]
        if len(vals) != len(set(vals)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: {key} unique")
        b = [v.encode("utf-8") for v in vals]
        if b != sorted(b):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: {key} not ascending")
        return
    if isinstance(annotation, dict) and "by" in annotation:
        by = annotation["by"]
        keys = []
        for x in arr:
            tup = tuple(str(x[k]) for k in by)
            keys.append("\0".join(tup).encode("utf-8"))
        if len(keys) != len(set(keys)):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: unique by {by}")
        if keys != sorted(keys):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{path}: not ascending by {by}")
        return
    raise AdmissionError("ORDER_VOCABULARY", f"{path}: annotation {annotation!r} outside closed vocabulary")


def walk_schema_order(instance: Any, schema: dict, defs: dict, *, path: str = "$") -> None:
    """Walk a Draft-2020-12-like schema object and enforce x-opensip-order on arrays."""
    if schema is None:
        return
    if "$ref" in schema:
        ref = schema["$ref"]
        if ref.startswith("#/$defs/"):
            name = ref.split("/")[-1]
            walk_schema_order(instance, defs.get(name, {}), defs, path=path)
        return
    if "allOf" in schema:
        for sub in schema["allOf"]:
            walk_schema_order(instance, sub, defs, path=path)
    t = schema.get("type")
    if t == "array" and isinstance(instance, list):
        ann = schema.get("x-opensip-order")
        check_order(instance, ann, path=path)
        items = schema.get("items") or {}
        for i, el in enumerate(instance):
            walk_schema_order(el, items, defs, path=f"{path}[{i}]")
    if t == "object" and isinstance(instance, dict):
        props = schema.get("properties") or {}
        for k, v in instance.items():
            if k in props:
                walk_schema_order(v, props[k], defs, path=f"{path}.{k}")
