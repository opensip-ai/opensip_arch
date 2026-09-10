"""Stock JSON Schema plus published kit keywords x-opensip-order and digest annotations.

Stock jsonschema does not enforce x-opensip-* keywords. This module walks the
owning schema (including $ref) and independently executes those laws.
"""
from __future__ import annotations

import json
from typing import Any
from urllib.parse import urldefrag

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from helpers.canonical import C, AdmissionError
from helpers.paths import KIT


class KeywordError(AdmissionError):
    pass


def load_json(rel: str) -> Any:
    return json.loads((KIT / rel).read_text())


def build_registry(documents: dict[str, Any]) -> Registry:
    """documents: {uri: schema_dict}"""
    registry = Registry()
    for uri, schema in documents.items():
        registry = registry.with_resource(uri, Resource.from_contents(schema, default_specification=DRAFT202012))
    return registry


def stock_validate(instance: Any, schema: dict[str, Any], registry: Registry | None = None) -> list[str]:
    if registry is None:
        validator = Draft202012Validator(schema)
    else:
        validator = Draft202012Validator(schema, registry=registry)
    errors = []
    for e in validator.iter_errors(instance):
        errors.append(f"{list(e.absolute_path)}: {e.message}")
    return errors


def check_x_opensip_order(instance: Any, schema: dict[str, Any], *, registry_docs: dict[str, Any] | None = None) -> list[str]:
    """Walk instance/schema and enforce x-opensip-order on arrays."""
    docs = registry_docs or {}
    cache: dict[str, Any] = {}
    faults: list[str] = []

    def resolve(sch: dict[str, Any], base: str) -> tuple[dict[str, Any], str]:
        if "$ref" not in sch:
            return sch, base
        ref = sch["$ref"]
        if ref.startswith("#"):
            uri = base
            frag = ref[1:]
        else:
            uri, frag = urldefrag(ref)
            if not uri:
                uri = base
            if frag and not frag.startswith("/"):
                frag = "/" + frag if frag.startswith("$") else frag
        doc = docs.get(uri)
        if doc is None and uri in docs:
            doc = docs[uri]
        if doc is None:
            # try base document
            doc = docs.get(base)
        if doc is None:
            return sch, base
        target = _pointer(doc, frag) if frag else doc
        if not isinstance(target, dict):
            return sch, uri
        return target, uri

    def walk(inst: Any, sch: dict[str, Any], base: str, path: str) -> None:
        sch, base = resolve(sch, base)
        if "allOf" in sch:
            for sub in sch["allOf"]:
                if isinstance(sub, dict):
                    walk(inst, sub, base, path)
        order = sch.get("x-opensip-order")
        if order is not None and isinstance(inst, list):
            try:
                _check_order(inst, order, path)
            except KeywordError as e:
                faults.append(f"{path}: {e.code}: {e.message}")
        if sch.get("type") == "object" or "properties" in sch:
            if isinstance(inst, dict):
                props = sch.get("properties") or {}
                for k, sub in props.items():
                    if k in inst and isinstance(sub, dict):
                        walk(inst[k], sub, base, f"{path}.{k}")
                addl = sch.get("additionalProperties")
                if isinstance(addl, dict):
                    for k, v in inst.items():
                        if k not in props:
                            walk(v, addl, base, f"{path}.{k}")
        items = sch.get("items")
        if isinstance(items, dict) and isinstance(inst, list):
            for i, v in enumerate(inst):
                walk(v, items, base, f"{path}[{i}]")
        one = sch.get("oneOf") or sch.get("anyOf")
        if isinstance(one, list) and inst is not None:
            # walk matching branch only when unique
            matching = []
            for sub in one:
                if isinstance(sub, dict):
                    matching.append(sub)
            for sub in matching:
                try:
                    walk(inst, sub, base, path)
                except Exception:
                    pass

    root_id = schema.get("$id", "")
    walk(instance, schema, root_id, "$")
    return faults


def _pointer(doc: Any, frag: str) -> Any:
    if not frag:
        return doc
    if frag.startswith("/"):
        parts = frag[1:].split("/")
    else:
        parts = frag.split("/")
    cur = doc
    for p in parts:
        p = p.replace("~1", "/").replace("~0", "~")
        if p == "":
            continue
        if isinstance(cur, dict):
            cur = cur[p]
        else:
            raise KeyError(p)
    return cur


def _item_c_bytes(item: Any) -> bytes:
    return C(item)


def _check_order(arr: list[Any], order: Any, path: str) -> None:
    n = len(arr)
    if order == "sequence":
        return
    if order == "canonical-set":
        keys = [_item_c_bytes(x) for x in arr]
        for i in range(1, n):
            if keys[i] <= keys[i - 1]:
                raise KeywordError("ORDER_CANONICAL_SET", f"{path} not strict ascending unique C bytes")
        if len(set(keys)) != n:
            raise KeywordError("ORDER_UNIQUE", f"{path} duplicate canonical items")
        return
    if order == "canonical-order":
        keys = [_item_c_bytes(x) for x in arr]
        for i in range(1, n):
            if keys[i] < keys[i - 1]:
                raise KeywordError("ORDER_CANONICAL_ORDER", f"{path} not nondecreasing C bytes")
        return
    if order == "utf8":
        if any(type(x) is not str for x in arr):
            raise KeywordError("ORDER_UTF8", f"{path} utf8 order requires string items")
        keys = [x.encode("utf-8") for x in arr]
        for i in range(1, n):
            if keys[i] <= keys[i - 1]:
                raise KeywordError("ORDER_UTF8", f"{path} not strict ascending unique UTF-8")
        return
    if order == "path":
        paths = []
        for x in arr:
            if type(x) is str:
                paths.append(x)
            elif type(x) is dict and "path" in x:
                paths.append(x["path"])
            else:
                raise KeywordError("ORDER_PATH", f"{path} path order requires path field")
        keys = [p.encode("utf-8") for p in paths]
        for i in range(1, n):
            if keys[i] <= keys[i - 1]:
                raise KeywordError("ORDER_PATH", f"{path} paths not unique strict ascending UTF-8")
        return
    if order == "numeric":
        if any(type(x) is not int for x in arr):
            raise KeywordError("ORDER_NUMERIC", f"{path} numeric order requires integers")
        for i in range(1, n):
            if arr[i] <= arr[i - 1]:
                raise KeywordError("ORDER_NUMERIC", f"{path} not strict ascending unique integers")
        return
    if order == "ordinal":
        ords = []
        for x in arr:
            if type(x) is not dict or "ordinal" not in x:
                raise KeywordError("ORDER_ORDINAL", f"{path} ordinal order requires ordinal field")
            ords.append(x["ordinal"])
        if ords != list(range(n)):
            raise KeywordError("ORDER_ORDINAL", f"{path} ordinals not contiguous 0..n-1")
        return
    if order == "predicate":
        keys = []
        for x in arr:
            if type(x) is not dict:
                raise KeywordError("ORDER_PREDICATE", f"{path} predicate order requires objects")
            tup = f"{x.get('ruleId','')},{x.get('subjectId','')},{x.get('predicateId','')}"
            keys.append(tup.encode("utf-8"))
        for i in range(1, n):
            if keys[i] <= keys[i - 1]:
                raise KeywordError("ORDER_PREDICATE", f"{path} not strict ascending unique predicate tuples")
        return
    if order in ("ruleId", "waiverId"):
        keys = []
        for x in arr:
            if type(x) is str:
                keys.append(x.encode("utf-8"))
            elif type(x) is dict and order in x:
                keys.append(str(x[order]).encode("utf-8"))
            else:
                raise KeywordError("ORDER_KEY", f"{path} missing {order}")
        for i in range(1, n):
            if keys[i] <= keys[i - 1]:
                raise KeywordError("ORDER_KEY", f"{path} not strict ascending unique {order}")
        return
    if isinstance(order, dict) and "by" in order:
        fields = order["by"]
        keys = []
        for x in arr:
            if type(x) is not dict:
                raise KeywordError("ORDER_BY", f"{path} by-order requires objects")
            tup = tuple(str(x.get(f, "")).encode("utf-8") for f in fields)
            keys.append(tup)
        for i in range(1, n):
            if keys[i] <= keys[i - 1]:
                raise KeywordError("ORDER_BY", f"{path} not strict ascending unique by {fields}")
        return
    raise KeywordError("ORDER_VOCABULARY", f"{path} x-opensip-order {order!r} outside closed vocabulary")


def collect_digest_annotations(schema: dict[str, Any], instance: Any) -> list[dict[str, Any]]:
    """Collect x-opensip-digest annotations actually present on the instance."""
    found: list[dict[str, Any]] = []

    def walk(inst: Any, sch: dict[str, Any], path: str) -> None:
        if not isinstance(sch, dict):
            return
        if "$ref" in sch and len(sch) == 1:
            return
        ann = sch.get("x-opensip-digest")
        if ann is not None and inst is not None:
            found.append({"path": path, "annotation": ann, "value": inst})
        if isinstance(inst, dict):
            props = sch.get("properties") or {}
            for k, sub in props.items():
                if k in inst:
                    walk(inst[k], sub, f"{path}.{k}")
        if isinstance(inst, list) and isinstance(sch.get("items"), dict):
            for i, v in enumerate(inst):
                walk(v, sch["items"], f"{path}[{i}]")

    walk(instance, schema, "$")
    return found
