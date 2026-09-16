"""Schema×instance annotation sites. Independent of handler cases.

Walks published x-opensip-* field annotations through $ref/allOf/if/then/oneOf
without a whitelist of nested container names. Document-level registries are
excluded here and bound by table iteration elsewhere.
"""
from __future__ import annotations

from typing import Any, Iterator

from jsonschema import Draft202012Validator

from . import kit_schemas


def _lookup(ref: str, base_id: str | None = None):
    resolver = kit_schemas.REGISTRY.resolver(base_uri=base_id or "")
    try:
        return resolver.lookup(ref)
    except Exception:
        return kit_schemas.REGISTRY.resolver().lookup(ref)


def _schema_id_of(schema: dict, fallback: str | None) -> str | None:
    sid = schema.get("$id") or fallback
    if sid and "#" in sid:
        return sid.split("#", 1)[0]
    return sid


def _iter_sub(schema: dict, base_id: str | None):
    sid = _schema_id_of(schema, base_id)
    if "$ref" in schema and set(schema.keys()) <= {"$ref", "$id", "$schema", "description"}:
        resolved = _lookup(schema["$ref"], sid).contents
        yield resolved, _schema_id_of(resolved, sid) if _schema_id_of(resolved, None) else sid
        return
    if "$ref" in schema:
        resolved = _lookup(schema["$ref"], sid).contents
        merged = dict(resolved)
        for k, v in schema.items():
            if k != "$ref":
                merged[k] = v
        yield merged, _schema_id_of(resolved, sid)
        return
    yield schema, sid

DOCUMENT_LEVEL = {
    "x-opensip-digest-domains",
    "x-opensip-digest-law",
    "x-opensip-relation-registry",
    "x-opensip-payload-registry",
    "x-opensip-deficiency-cause-registry",
    "x-opensip-kind-derivation",
    "x-opensip-file-membership-extent-law",
    "x-opensip-subject-language-table",
    "x-opensip-join-law",
    "x-opensip-evaluator-profile",
    "x-opensip-evidence-relation-registry",
    "x-opensip-config-node-kind-law",
    "x-opensip-capability-id-law",
    "x-opensip-new-internal-faults",
    "x-opensip-identity",
    "x-opensip-parameter-registry-extension",
    "x-opensip-mirror",
    "x-opensip-ownership-attribute",
}


def fragment_ptr(schema: dict, current: str) -> str:
    if not isinstance(schema, dict):
        return current
    ref = schema.get("$ref")
    extra = set(schema.keys()) - {"$ref", "$id", "$schema", "description"}
    if isinstance(ref, str) and "#" in ref and not extra:
        frag = ref.split("#", 1)[1]
        return frag if frag.startswith("/") else "/" + frag
    return current or ""


def join_prop(fp: str, k: str) -> str:
    return f"{fp}/{k}" if fp else k


def join_idx(fp: str, i: int) -> str:
    return f"{fp}[{i}]" if fp else f"[{i}]"


def iter_x_sites(
    instance: Any,
    schema: dict,
    base_id: str | None,
    root_ident: str,
    field_path: str = "",
    schema_ptr: str = "",
    parent: Any = None,
    seen: set | None = None,
) -> Iterator[dict]:
    seen = seen if seen is not None else set()
    ptr0 = fragment_ptr(schema, schema_ptr)
    marker = (id(schema), field_path, ptr0)
    if marker in seen:
        return
    seen.add(marker)
    try:
        subs = list(_iter_sub(schema, base_id))
    except Exception:
        return
    for sch, sid in subs:
        if not isinstance(sch, dict):
            continue
        ptr = ptr0
        for kw, annot in sch.items():
            if not str(kw).startswith("x-opensip-"):
                continue
            if kw in DOCUMENT_LEVEL:
                continue
            yield {
                "keyword": kw,
                "annot": annot,
                "value": instance,
                "parent": parent,
                "root": root_ident,
                "field": field_path or "/",
                "schema_ptr": f"{ptr}/{kw}" if ptr else f"/{kw}",
                "schema_id": sid,
                "kitPath": _kit_path(sid),
            }
        if isinstance(instance, dict) and (
            sch.get("type") == "object" or "properties" in sch or "additionalProperties" in sch
        ):
            props = sch.get("properties") or {}
            addl = sch.get("additionalProperties")
            for k, v in instance.items():
                if k in props:
                    yield from iter_x_sites(
                        v,
                        props[k],
                        sid,
                        root_ident,
                        join_prop(field_path, k),
                        ptr + "/properties/" + k,
                        parent=instance,
                        seen=seen,
                    )
                elif isinstance(addl, dict):
                    yield from iter_x_sites(
                        v,
                        addl,
                        sid,
                        root_ident,
                        join_prop(field_path, k),
                        ptr + "/additionalProperties",
                        parent=instance,
                        seen=seen,
                    )
        if isinstance(instance, list) and (sch.get("type") == "array" or "items" in sch or "x-opensip-order" in sch):
            item_schema = sch.get("items") or {}
            for i, item in enumerate(instance):
                yield from iter_x_sites(
                    item,
                    item_schema,
                    sid,
                    root_ident,
                    join_idx(field_path, i),
                    ptr + "/items",
                    parent=instance,
                    seen=seen,
                )
        for i, alt in enumerate(sch.get("allOf") or []):
            yield from iter_x_sites(
                instance, alt, sid, root_ident, field_path, ptr + f"/allOf/{i}", parent=parent, seen=seen
            )
        ife = sch.get("if")
        if ife is not None:
            try:
                Draft202012Validator(ife, registry=kit_schemas.REGISTRY).validate(instance)
                then = sch.get("then")
                if then is not None:
                    yield from iter_x_sites(
                        instance, then, sid, root_ident, field_path, ptr + "/then", parent=parent, seen=seen
                    )
            except Exception:
                els = sch.get("else")
                if els is not None:
                    yield from iter_x_sites(
                        instance, els, sid, root_ident, field_path, ptr + "/else", parent=parent, seen=seen
                    )
        for key in ("oneOf", "anyOf"):
            alts = sch.get(key)
            if not isinstance(alts, list):
                continue
            for i, alt in enumerate(alts):
                try:
                    Draft202012Validator(alt, registry=kit_schemas.REGISTRY).validate(instance)
                except Exception:
                    continue
                yield from iter_x_sites(
                    instance, alt, sid, root_ident, field_path, ptr + f"/{key}/{i}", parent=parent, seen=seen
                )
                break


def _kit_path(sid: str | None) -> str | None:
    if not sid:
        return None
    p = kit_schemas.SCHEMA_PATHS.get(sid)
    if not p:
        return None
    posix = p.as_posix()
    if "/subject/" in posix:
        return posix.split("/subject/", 1)[-1]
    return posix
