"""JSON Schema Draft 2020-12 plus x-opensip-order. Stock jsonschema does not enforce kit keywords."""
from __future__ import annotations

import copy
import re
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from jsonschema.validators import extend
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from canonical import AdmissionError, encode_c
from kit import Kit

HEX64 = re.compile(r"^[0-9a-f]{64}$")
TYPED_ID = re.compile(r"^([a-z0-9-]+):([0-9a-f]{64})$")
SHA256_TEXT = re.compile(r"^sha256:([0-9a-f]{64})$")


def _item_sort_key_bytes(order: Any, item: Any) -> bytes:
    if order == "sequence":
        return b""
    if order == "canonical-set" or order == "canonical-order":
        return encode_c(item, profile="product")
    if order == "utf8":
        if not isinstance(item, str):
            raise AdmissionError("ORDER_UTF8", "utf8 order requires string items", "identity-and-evidence.md§3 x-opensip-order", {"type": type(item).__name__})
        return item.encode("utf-8")
    if order == "path":
        if isinstance(item, str):
            return item.encode("utf-8")
        if isinstance(item, dict) and "path" in item:
            return str(item["path"]).encode("utf-8")
        raise AdmissionError("ORDER_PATH", "path order requires string or object.path", "identity-and-evidence.md§3 x-opensip-order", {})
    if order == "numeric":
        if not isinstance(item, int) or isinstance(item, bool):
            raise AdmissionError("ORDER_NUMERIC", "numeric order requires integers", "identity-and-evidence.md§3 x-opensip-order", {})
        return encode_c(item, profile="product")
    if order == "ordinal":
        if not isinstance(item, dict) or "ordinal" not in item:
            raise AdmissionError("ORDER_ORDINAL", "ordinal order requires object.ordinal", "identity-and-evidence.md§3 x-opensip-order", {})
        return b""
    if order == "predicate":
        if not isinstance(item, dict):
            raise AdmissionError("ORDER_PREDICATE", "predicate order requires objects", "identity-and-evidence.md§3 x-opensip-order", {})
        tup = f"{item.get('ruleId','')},{item.get('subjectId','')},{item.get('predicateId','')}"
        return tup.encode("utf-8")
    if order in ("ruleId", "waiverId"):
        if not isinstance(item, dict) or order not in item:
            raise AdmissionError("ORDER_KEY", f"{order} order requires that key", "identity-and-evidence.md§3 x-opensip-order", {"order": order})
        return str(item[order]).encode("utf-8")
    if isinstance(order, dict) and "by" in order:
        keys = order["by"]
        if not isinstance(item, dict):
            raise AdmissionError("ORDER_BY", "by-key order requires objects", "identity-and-evidence.md§3 x-opensip-order", {})
        parts = [str(item.get(k, "")) for k in keys]
        return ("\x1f".join(parts)).encode("utf-8")
    raise AdmissionError(
        "ORDER_VOCABULARY",
        "x-opensip-order annotation outside the closed vocabulary refuses",
        "identity-and-evidence.md§3 (closed x-opensip-order vocabulary)",
        {"order": order},
    )


def check_order(order: Any, instance: Any, path: str) -> None:
    if not isinstance(instance, list):
        return
    citation = "identity-and-evidence.md§3 x-opensip-order"
    unique_required = order not in ("sequence", "canonical-order")
    if order == "ordinal":
        ordinals = []
        for i, item in enumerate(instance):
            if not isinstance(item, dict) or "ordinal" not in item:
                raise AdmissionError("ORDER_ORDINAL", "missing ordinal", citation, {"path": path, "index": i})
            if not isinstance(item["ordinal"], int) or isinstance(item["ordinal"], bool):
                raise AdmissionError("ORDER_ORDINAL", "ordinal is not an integer", citation, {"path": path})
            ordinals.append(item["ordinal"])
        if ordinals != list(range(len(ordinals))):
            raise AdmissionError(
                "ORDER_ORDINAL_CONTIGUOUS",
                "ordinal order requires contiguous zero-based ordinals",
                citation,
                {"path": path, "ordinals": ordinals},
            )
        return
    if order == "sequence":
        return
    keys = [_item_sort_key_bytes(order, item) for item in instance]
    if unique_required:
        if len(keys) != len(set(keys)):
            raise AdmissionError(
                "ORDER_OR_DUPLICATE",
                "order annotation requires unique sort keys",
                citation,
                {"path": path, "order": order},
            )
        if keys != sorted(keys):
            raise AdmissionError(
                "ORDER_NOT_STRICT_ASCENDING",
                "array is not strict ascending under its x-opensip-order",
                citation,
                {"path": path, "order": order},
            )
    else:
        # canonical-order: nondecreasing, repeats allowed
        if keys != sorted(keys):
            raise AdmissionError(
                "ORDER_NOT_NONDECREASING",
                "canonical-order requires nondecreasing canonical item bytes",
                citation,
                {"path": path},
            )


def _order_keyword(validator, order, instance, schema):
    try:
        check_order(order, instance, "/")
    except AdmissionError as e:
        yield ValidationError(e.message, validator=validator, path=(), schema_path=("x-opensip-order",))


OpenSIPValidator = extend(Draft202012Validator, {"x-opensip-order": _order_keyword})


class SchemaBundle:
    def __init__(self, kit: Kit):
        self.kit = kit
        resources = []
        for rel, raw in kit.file_bytes.items():
            if not rel.endswith(".json"):
                continue
            try:
                doc = json_loads_maybe(raw)
            except Exception:
                continue
            if not isinstance(doc, dict):
                continue
            rid = doc.get("$id") or ("urn:opensip:kit:" + rel)
            resources.append((rid, Resource.from_contents(doc, default_specification=DRAFT202012)))
            resources.append(("kit://" + rel, Resource.from_contents(doc, default_specification=DRAFT202012)))
        registry = Registry()
        for rid, res in resources:
            registry = registry.with_resource(rid, res)
        self.registry = registry
        self._docs_by_rel = {rel: json_loads_maybe(raw) for rel, raw in kit.file_bytes.items() if rel.endswith(".json")}

    def document(self, rel_suffix: str) -> dict:
        for rel, doc in self._docs_by_rel.items():
            if rel.endswith(rel_suffix) or rel.endswith("/" + rel_suffix) or rel == rel_suffix:
                if isinstance(doc, dict):
                    return doc
        raise AdmissionError("SCHEMA_DOC_MISSING", f"schema document {rel_suffix} not in kit", "S-MISSING-DEP-IS-CUSTODY", {"path": rel_suffix})

    def validate(self, instance: Any, document: dict, selector: str, *, path: str = "") -> None:
        # Keep the document root so local #/$defs $ref resolve. Inlining a $defs
        # subschema as the validator root makes PointerToNowhere on sibling defs.
        if selector in ("#", "", None):
            schema = document
        else:
            resolved = resolve_pointer(document, selector)
            if not isinstance(resolved, dict):
                raise AdmissionError(
                    "SELECTOR",
                    f"selector {selector} is not an object schema",
                    "identity-and-evidence.md§3",
                    {"path": path, "selector": selector},
                )
            schema = dict(resolved)
            if "$defs" in document and "$defs" not in schema:
                schema["$defs"] = document["$defs"]
            if "$id" in document:
                schema.setdefault("$id", str(document["$id"]) + (selector or ""))
            if "$schema" in document:
                schema.setdefault("$schema", document["$schema"])
        rid = schema.get("$id") or document.get("$id") or "urn:opensip:anon"
        try:
            resource = Resource.from_contents(document if "$defs" in document else schema, default_specification=DRAFT202012)
            registry = self.registry.with_resource(rid, resource)
            if document.get("$id") and document["$id"] != rid:
                registry = registry.with_resource(document["$id"], resource)
            validator = OpenSIPValidator(schema, registry=registry)
            errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        except AdmissionError:
            raise
        except Exception as e:
            raise AdmissionError(
                "SCHEMA_VALIDATOR_FAULT",
                f"schema validator could not run: {e}",
                "identity-and-evidence.md§3 (owning schema including published keywords)",
                {"path": path, "selector": selector, "error": str(e)},
            )
        if errors:
            err = errors[0]
            loc = "/".join(str(p) for p in err.absolute_path)
            raise AdmissionError(
                "SCHEMA_INVALID",
                err.message,
                "identity-and-evidence.md§3 + owning schema " + selector,
                {"path": path, "instancePath": loc, "schemaPath": list(err.absolute_schema_path), "validator": err.validator},
            )


def json_loads_maybe(raw: bytes) -> Any:
    import json
    return json.loads(raw.decode("utf-8"))


def resolve_pointer(document: dict, selector: str) -> Any:
    if selector in ("#", "", None):
        return document
    if not selector.startswith("#"):
        raise AdmissionError("SELECTOR", f"non-local selector {selector}", "identity-and-evidence.md§3", {"selector": selector})
    if selector == "#":
        return document
    if not selector.startswith("#/"):
        raise AdmissionError("SELECTOR", f"unsupported selector {selector}", "identity-and-evidence.md§3", {"selector": selector})
    cur: Any = document
    for part in selector[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            raise AdmissionError("SELECTOR", f"{selector} not found at {part}", "identity-and-evidence.md§3", {})
    return cur


def merge_ref(schema: dict, document: dict, seen: set | None = None) -> dict:
    """Resolve a local $ref while preserving sibling keywords (Draft 2020-12)."""
    if seen is None:
        seen = set()
    if not isinstance(schema, dict):
        return schema
    if "$ref" not in schema:
        return schema
    ref = schema["$ref"]
    if not isinstance(ref, str) or not ref.startswith("#"):
        return schema
    if ref in seen:
        return {k: v for k, v in schema.items() if k != "$ref"}
    seen = set(seen)
    seen.add(ref)
    target = resolve_pointer(document, ref)
    if not isinstance(target, dict):
        return schema
    target = merge_ref(target, document, seen)
    merged = dict(target)
    for k, v in schema.items():
        if k == "$ref":
            continue
        merged[k] = v
    return merged
