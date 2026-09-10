"""Schema-guided instance traversal. Binds conditions to nested owner/child instances.

Applicator markers are not instance fields: if/then/else is evaluated against the
actual child object; only the taken branch's rules bind; the other is inapplicable.
"""
from __future__ import annotations

from typing import Any, Iterator

from . import kit_schemas, order


def resolve_ref(schema: dict, sid: str, root: dict) -> tuple[dict, str, str]:
    """Return (merged schema, schemaId, fragment pointer). Sibling keywords survive."""
    if not isinstance(schema, dict) or "$ref" not in schema:
        return schema, sid, ""
    ref = schema["$ref"]
    target, tsid, frag = {}, sid, ""
    if ref.startswith("#/"):
        frag = ref[1:] if ref.startswith("#/") else "/" + ref.split("#", 1)[-1]
        cur = root
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            cur = cur.get(part) if isinstance(cur, dict) else None
            if cur is None:
                break
        target = cur if isinstance(cur, dict) else {}
        tsid = sid
    else:
        try:
            looked = kit_schemas.REGISTRY.resolver(base_uri=sid or "").lookup(ref)
            target = looked.contents if isinstance(looked.contents, dict) else {}
            tsid = (target.get("$id") or sid or "").split("#", 1)[0]
            if "#" in ref:
                frag = "/" + ref.split("#", 1)[1].lstrip("/")
        except Exception:
            target = {}
            tsid = sid
    merged = dict(target)
    for k, v in schema.items():
        if k != "$ref":
            merged[k] = v
    return merged, tsid, frag


def kit_path_for_sid(sid: str) -> str:
    p = kit_schemas.SCHEMA_PATHS.get(sid)
    if not p:
        return sid or ""
    s = p.as_posix()
    return s.split("/subject/", 1)[-1] if "/subject/" in s else s


def _if_applies(iff: dict, instance: Any) -> bool:
    if not isinstance(iff, dict) or not isinstance(instance, dict):
        return False
    props = iff.get("properties") or {}
    for name, psch in props.items():
        if not isinstance(psch, dict):
            continue
        if "const" in psch:
            if instance.get(name) != psch["const"]:
                return False
        if psch.get("type") == "null" and instance.get(name) is not None:
            return False
        if psch.get("type") == "integer" and not isinstance(instance.get(name), int):
            return False
        if psch.get("type") == "string" and not isinstance(instance.get(name), str):
            return False
    return True


def walk_instance(
    instance: Any,
    schema: dict,
    *,
    sid: str,
    root: dict,
    owner_id: str,
    path: str,
    ptr: str,
    out: list,
) -> None:
    if not isinstance(schema, dict):
        return
    schema, sid, frag = resolve_ref(schema, sid, root)
    if frag:
        ptr = frag
    doc = kit_path_for_sid(sid)
    rec = {
        "schemaId": sid,
        "document": doc,
        "pointer": ptr or "/",
        "ownerId": owner_id,
        "instancePath": path or "/",
        "valueType": type(instance).__name__,
        "description": schema.get("description") if isinstance(schema.get("description"), str) else None,
        "note": schema.get("note") if isinstance(schema.get("note"), str) else None,
        "xOrder": schema.get("x-opensip-order"),
        "xDigest": schema.get("x-opensip-digest"),
        "required": list(schema.get("required") or []),
        "applicator": None,
        "applicable": True,
    }
    out.append(rec)

    # if/then/else: evaluate predicate; bind only taken branch
    if "if" in schema:
        applies = _if_applies(schema.get("if") or {}, instance)
        rec_if = dict(rec)
        rec_if["applicator"] = "if"
        rec_if["applicable"] = applies
        rec_if["pointer"] = (ptr or "/") + "/if"
        rec_if["description"] = None
        out.append(rec_if)
        branch = "then" if applies else "else"
        other = "else" if applies else "then"
        if schema.get(branch):
            walk_instance(
                instance, schema[branch], sid=sid, root=root, owner_id=owner_id,
                path=path, ptr=(ptr or "/") + "/" + branch, out=out,
            )
        if schema.get(other):
            out.append(
                {
                    **rec,
                    "applicator": other,
                    "applicable": False,
                    "pointer": (ptr or "/") + "/" + other,
                    "description": None,
                    "inapplicableReason": f"if-predicate {applies}; {other} branch not taken",
                }
            )

    for app in ("allOf", "oneOf", "anyOf"):
        for i, sub in enumerate(schema.get(app) or []):
            if isinstance(sub, dict):
                walk_instance(
                    instance, sub, sid=sid, root=root, owner_id=owner_id,
                    path=path, ptr=f"{ptr or '/'}/{app}/{i}", out=out,
                )

    if isinstance(instance, dict):
        props = schema.get("properties") or {}
        for name, psch in props.items():
            if name in instance:
                walk_instance(
                    instance[name], psch if isinstance(psch, dict) else {},
                    sid=sid, root=root, owner_id=owner_id,
                    path=f"{path}.{name}" if path else name,
                    ptr=f"{ptr or ''}/properties/{name}".replace("//", "/"),
                    out=out,
                )
    if isinstance(instance, list):
        items = schema.get("items")
        if isinstance(items, dict):
            for i, ent in enumerate(instance):
                walk_instance(
                    ent, items, sid=sid, root=root, owner_id=owner_id,
                    path=f"{path}[{i}]",
                    ptr=f"{ptr or ''}/items".replace("//", "/"),
                    out=out,
                )


def is_canonical_set(seq: list) -> bool:
    return seq == order.cset(list(seq))


def is_ordinal_order(seq: list) -> bool:
    if not seq:
        return True
    if all(isinstance(x, dict) and "ordinal" in x for x in seq):
        got = [x["ordinal"] for x in seq]
        return got == list(range(len(seq)))
    return False
