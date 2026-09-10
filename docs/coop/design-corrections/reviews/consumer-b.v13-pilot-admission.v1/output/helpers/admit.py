"""Owning-schema admission: stock Draft 2020-12 + every selected $ref +
published x-opensip-order and x-opensip-digest retention.

A stock-schema pass alone is not admission.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from jsonschema import Draft202012Validator
from referencing.exceptions import Unresolvable

from . import canonical, h, kit_schemas, order, store


class AdmitError(Exception):
    def __init__(self, code: str, message: str, path: str = ""):
        super().__init__(f"{code}:{path}: {message}" if path else f"{code}: {message}")
        self.code = code
        self.message = message
        self.path = path
        self.firstRefusal = code


def _lookup(ref: str, base_id: str | None = None):
    resolver = kit_schemas.REGISTRY.resolver(base_uri=base_id or "")
    try:
        return resolver.lookup(ref)
    except Exception:
        # absolute retry
        return kit_schemas.REGISTRY.resolver().lookup(ref)


def resolve_schema(schema: dict, base_id: str | None = None) -> dict:
    """Follow a single $ref, returning the referenced schema object (may still contain nested $ref)."""
    ref = schema.get("$ref")
    if not ref:
        return schema
    try:
        resolved = _lookup(ref, base_id)
        return resolved.contents
    except Exception as e:
        raise AdmitError("SCHEMA_REF_UNRESOLVABLE", f"cannot resolve $ref {ref} (base={base_id}): {e}", "") from e


def schema_id_of(schema: dict, fallback: str | None) -> str | None:
    sid = schema.get("$id") or fallback
    if sid and "#" in sid:
        return sid.split("#", 1)[0]
    return sid


def iter_subschemas(schema: dict, base_id: str | None):
    """Yield (resolved_schema, effective_id) after one $ref hop if present."""
    sid = schema_id_of(schema, base_id)
    if "$ref" in schema and set(schema.keys()) <= {"$ref", "$id", "$schema", "description"}:
        resolved = resolve_schema(schema, sid)
        # keep the document id for nested relative $ref
        yield resolved, schema_id_of(resolved, sid) if schema_id_of(resolved, None) else sid
        return
    # $ref plus siblings: JSON Schema 2020-12 applies $ref as if inlined alongside
    if "$ref" in schema:
        resolved = resolve_schema(schema, sid)
        # merge sibling keywords onto a copy of resolved for walking
        merged = dict(resolved)
        for k, v in schema.items():
            if k != "$ref":
                merged[k] = v
        yield merged, schema_id_of(resolved, sid)
        return
    yield schema, sid


def stock_validate(instance: Any, schema: dict) -> None:
    try:
        Draft202012Validator(schema, registry=kit_schemas.REGISTRY).validate(instance)
    except Exception as e:
        raise AdmitError("STOCK_SCHEMA", str(e)) from e


def walk_order(instance: Any, schema: dict, base_id: str | None, path: str) -> list[str]:
    errors: list[str] = []
    for sch, sid in iter_subschemas(schema, base_id):
        if sch.get("type") == "array" and isinstance(instance, list):
            ann = sch.get("x-opensip-order", "sequence")
            try:
                order.check_order(instance, ann, unique_items=bool(sch.get("uniqueItems")))
            except order.OrderError as e:
                errors.append(f"{path or '/'}: {e}")
            item_schema = sch.get("items") or {}
            for i, item in enumerate(instance):
                errors.extend(walk_order(item, item_schema, sid, f"{path}[{i}]"))
        if sch.get("type") == "object" and isinstance(instance, dict):
            props = sch.get("properties") or {}
            for k, v in instance.items():
                if k in props:
                    errors.extend(walk_order(v, props[k], sid, f"{path}/{k}"))
            addl = sch.get("additionalProperties")
            if isinstance(addl, dict):
                for k, v in instance.items():
                    if k not in props:
                        errors.extend(walk_order(v, addl, sid, f"{path}/{k}"))
        # oneOf/anyOf: try each
        for key in ("oneOf", "anyOf"):
            alts = sch.get(key)
            if isinstance(alts, list) and instance is not None:
                # walk the first matching alternative for order (stock already admitted)
                matched = False
                for alt in alts:
                    try:
                        Draft202012Validator(alt, registry=kit_schemas.REGISTRY).validate(instance)
                    except Exception:
                        continue
                    errors.extend(walk_order(instance, alt, sid, path))
                    matched = True
                    break
                if not matched:
                    # still walk all for diagnostics? no — first-refusal already at stock
                    pass
        if "items" in sch and sch.get("type") != "array" and isinstance(instance, list):
            for i, item in enumerate(instance):
                errors.extend(walk_order(item, sch["items"], sid, f"{path}[{i}]"))
    return errors


def _get_path(obj: Any, parts: list) -> Any:
    cur = obj
    for p in parts:
        if p == "[]":
            return cur
        if isinstance(cur, dict):
            cur = cur.get(p)
        else:
            return None
    return cur


def check_digest_retention(
    instance: Any,
    schema: dict,
    st: store.Store,
    base_id: str | None,
    path: str,
    seen: set | None = None,
) -> list[str]:
    """For every x-opensip-digest field, require retained preimage and admit nested records."""
    errors = []
    seen = seen if seen is not None else set()
    for sch, sid in iter_subschemas(schema, base_id):
        dig = sch.get("x-opensip-digest")
        if dig and isinstance(instance, str):
            err = _require_digest(instance, dig, st, path)
            if err:
                errors.append(err)
            errors.extend(_admit_nested_canonical(instance, dig, st, path, seen))
        props = sch.get("properties") or {}
        if isinstance(instance, dict):
            for k, v in instance.items():
                psch = props.get(k)
                if psch is None:
                    addl = sch.get("additionalProperties")
                    if isinstance(addl, dict):
                        errors.extend(check_digest_retention(v, addl, st, sid, f"{path}/{k}", seen))
                    continue
                # resolve property schema
                for psch2, psid in iter_subschemas(psch, sid):
                    nested_dig = psch2.get("x-opensip-digest")
                    if nested_dig and isinstance(v, str):
                        err = _require_digest(v, nested_dig, st, f"{path}/{k}")
                        if err:
                            errors.append(err)
                        errors.extend(_admit_nested_canonical(v, nested_dig, st, f"{path}/{k}", seen))
                    errors.extend(check_digest_retention(v, psch, st, sid, f"{path}/{k}", seen))
        if sch.get("type") == "array" and isinstance(instance, list):
            item_schema = sch.get("items") or {}
            for i, item in enumerate(instance):
                errors.extend(check_digest_retention(item, item_schema, st, sid, f"{path}[{i}]", seen))
        for key in ("oneOf", "anyOf"):
            alts = sch.get(key)
            if isinstance(alts, list):
                for alt in alts:
                    try:
                        Draft202012Validator(alt, registry=kit_schemas.REGISTRY).validate(instance)
                    except Exception:
                        continue
                    errors.extend(check_digest_retention(instance, alt, st, sid, path, seen))
                    break
    return errors


BUNDLE_TO_SCHEMA_ID = {
    "identity": "urn:opensip:product-v1:identity:v3",
}


def _nested_schema(annot: dict) -> tuple[str, str | None] | None:
    """Return (schema_id, def_name_or_None_for_root) or None if retention-only."""
    rec = annot.get("record") or {}
    selector = rec.get("selector")
    document = rec.get("document")
    bundle = rec.get("bundle")
    if not selector and not document:
        return None
    sid = None
    if bundle in BUNDLE_TO_SCHEMA_ID:
        sid = BUNDLE_TO_SCHEMA_ID[bundle]
    elif document:
        sid = kit_schemas.schema_id_for_document(document)
    if sid is None:
        raise AdmitError(
            "NESTED_SCHEMA_UNRESOLVABLE",
            f"nested record document={document!r} bundle={bundle!r} selector={selector!r} not in kit",
        )
    defn: str | None
    if selector in (None, "", "#"):
        defn = None
    elif selector.startswith("#/$defs/"):
        defn = selector[len("#/$defs/") :] or None
    elif selector.startswith("#/"):
        # non-$defs JSON pointer: admit via a $ref to that fragment
        defn = "__fragment__:" + selector
    else:
        defn = selector
    return sid, defn


def _admit_nested_canonical(value: str, annot: dict, st: store.Store, path: str, seen: set) -> list[str]:
    """When a digest names a canonical nested record, admit that preimage against its owning schema."""
    if annot.get("representation") != "canonical-record":
        return []
    try:
        resolved = _nested_schema(annot)
    except AdmitError as e:
        return [f"{path}: {e.code}: {e.message}"]
    if resolved is None:
        return []
    sid, defn = resolved
    rec = annot.get("record") or {}
    selector = rec.get("selector") or ""
    bare = _bare(value)
    key = (bare, sid, selector)
    if key in seen:
        return []
    seen.add(key)
    raw = st.blobs.get(bare) or st.blobs.get(value)
    if raw is None:
        return [f"{path}: nested canonical-record {bare} preimage missing"]
    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception as e:
        return [f"{path}: nested canonical-record {bare} is not JSON: {e}"]
    if defn and defn.startswith("__fragment__:"):
        schema = {"$ref": sid + defn[len("__fragment__:") :]}
        label = defn
    else:
        schema = kit_schemas.wrap_def(sid, defn)
        label = defn or sid
    try:
        admit_instance(payload, schema, st, f"{path}[{label}]", seen)
    except AdmitError as e:
        return [f"{path}: nested {label} refused: {e.code}: {e.message}"]
    return []


def _bare(digest: str) -> str:
    if ":" in digest:
        return digest.split(":")[-1]
    return digest


def _require_digest(value: str, annot: dict, st: store.Store, path: str) -> str | None:
    rep = annot.get("representation")
    retention = annot.get("retention")
    if retention == "derived":
        return None  # recomputed elsewhere
    bare = _bare(value)
    if rep in ("raw-artifact", "canonical-record", "framed-body-identity"):
        if bare not in st.blobs and value not in st.blobs:
            return f"{path}: {rep} digest {bare} not retained in blobs"
        return None
    if rep == "h-identity":
        # Identity §3: the retained blob under the H digest IS the framed preimage.
        domain = annot.get("domain")
        domain_set = annot.get("domainSet")
        frame = st.blobs.get(bare) or st.blobs.get(value)
        typed = None
        for cand in (value, "sha256:" + bare if len(bare) == 64 else None):
            if cand and cand in st.objects:
                typed = st.objects[cand]
                break
        if typed is None:
            for ident, rec in st.objects.items():
                if ident.endswith(bare):
                    typed = rec
                    break
        if frame is None and typed is None and retention in (None, "preimage", "preimage-frame"):
            return f"{path}: h-identity {value} preimage not retained (representation={rep} domain={domain} domainSet={domain_set})"
        if frame is not None:
            try:
                parsed_domain, cx = h.parse_h_frame(frame)
            except Exception:
                # Some h-identity fields name a suffix whose blob is C(X) of a nested
                # canonical-record (native context uses framed H). A UTF-8 JSON blob
                # here is not an H frame.
                try:
                    json.loads(frame.decode("utf-8"))
                    # C(X) stored under the H digest is the historical helper bug.
                    return f"{path}: h-identity {value} retained C(X) under H digest; framed preimage required"
                except Exception:
                    return f"{path}: h-identity {value} retained bytes are not an H frame"
            if hashlib.sha256(frame).hexdigest() != bare:
                return f"{path}: h-identity {value} SHA256(frame)!=digest"
            if typed is not None:
                restated = canonical.encode(typed)
                if cx != restated:
                    return f"{path}: h-identity {value} H-frame C(X) != stored object"
            if domain and parsed_domain != domain and parsed_domain.split(".")[0] != str(domain):
                # domain on identity fields is the H argument (snapshot, plan, …);
                # native domainSet rows use native.context.* names. Equality is
                # required when the annotation names an H argument domain.
                if domain in h.PREFIX and parsed_domain != domain:
                    return f"{path}: h-identity {value} frame domain {parsed_domain}!={domain}"
        return None
    if rep == "capability-manifest-id":
        # retention derived: recomputed at close_run from retained committed bytes
        return None
    if rep == "by-domain":
        return None
    return None


def admit_instance(
    instance: Any,
    schema: dict,
    st: store.Store | None = None,
    path: str = "",
    seen: set | None = None,
) -> dict:
    stock_validate(instance, schema)
    base = schema.get("$id")
    if not base and schema.get("$ref"):
        base = schema["$ref"].split("#", 1)[0]
    order_errors = walk_order(instance, schema, base, path)
    digest_errors = []
    if st is not None:
        digest_errors = check_digest_retention(instance, schema, st, base, path, seen if seen is not None else set())
    ok = not order_errors and not digest_errors
    if not ok:
        raise AdmitError(
            "ORDER_OR_DIGEST" if order_errors else "DIGEST_RETENTION",
            "; ".join(order_errors + digest_errors),
            path,
        )
    return {
        "stockPass": True,
        "orderPass": True,
        "digestPass": True,
        "admitted": True,
        "path": path,
    }


def admit_identity_record(obj: Any, def_name: str, st: store.Store, path: str) -> dict:
    schema = kit_schemas.wrap_def("urn:opensip:product-v1:identity:v3", def_name)
    return admit_instance(obj, schema, st, path)


def admit_native_def(obj: Any, def_name: str, st: store.Store, path: str) -> dict:
    schema = kit_schemas.wrap_def("urn:opensip:product-v1:native:evidence-schemas:v2", def_name)
    return admit_instance(obj, schema, st, path)


def admit_relation_payload(payload: Any, relation: str, st: store.Store, path: str) -> dict:
    defn = kit_schemas.REL_TO_PAYLOAD_DEF.get(relation)
    if not defn:
        raise AdmitError("UNKNOWN_RELATION", relation, path)
    schema = kit_schemas.wrap_def("opensip.product.relation-payload.2", defn)
    return admit_instance(payload, schema, st, path)


def admit_document(obj: Any, schema_id: str, st: store.Store, path: str, def_name: str | None = None) -> dict:
    schema = kit_schemas.wrap_def(schema_id, def_name)
    return admit_instance(obj, schema, st, path)
