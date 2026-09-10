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
from . import condtrace
from . import xsites


class AdmitError(Exception):
    def __init__(self, code: str, message: str, path: str = ""):
        super().__init__(f"{code}:{path}: {message}" if path else f"{code}: {message}")
        self.code = code
        self.message = message
        self.path = path
        self.firstRefusal = code


GRAPH_CTX: dict[str, Any] = {"inventory": None, "store": None}


def set_graph_context(st: store.Store | None) -> None:
    """Bind the enclosing snapshot inventory for snapshot-path joins."""
    inv: dict[str, dict] = {}
    if st is not None:
        for ident, obj in st.objects.items():
            if ident.startswith("snapshot2:") and isinstance(obj, dict):
                for row in obj.get("sourceInventory") or []:
                    if isinstance(row, dict) and isinstance(row.get("path"), str):
                        inv[row["path"]] = row
                break
    GRAPH_CTX["inventory"] = inv
    GRAPH_CTX["store"] = st


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
    for site in xsites.iter_x_sites(instance, schema, base_id, path):
        kw = site["keyword"]
        val = site["value"]
        sp = site["schema_ptr"]
        inst = site["root"]
        field = site["field"]
        if kw == "x-opensip-order" and isinstance(val, list):
            try:
                order.check_order(val, site["annot"], unique_items=False)
                condtrace.emit(
                    condition=sp, instance=inst, field=field, comparison="order",
                    left=site["annot"] if not isinstance(site["annot"], dict) else site["annot"],
                    right=len(val), result="pass",
                )
            except order.OrderError as e:
                condtrace.emit(
                    condition=sp, instance=inst, field=field, comparison="order",
                    left=site["annot"], right=str(e), result="refuse",
                )
                errors.append(f"{site['root']}/{field}: {e}")
        if kw == "x-opensip-uniqueness" and isinstance(site["annot"], dict):
            seq = val if isinstance(val, list) else (val.get("rules") if isinstance(val, dict) else None)
            keys = site["annot"].get("ownershipTuple") or site["annot"].get("rules")
            if keys and isinstance(seq, list):
                val = seq
        if kw == "x-opensip-uniqueness" and isinstance(val, list) and isinstance(site["annot"], dict):
            keys = site["annot"].get("ownershipTuple") or site["annot"].get("rules")
            if keys:
                seen_t = {}
                dup = None
                for i, item in enumerate(val):
                    if type(item) is dict:
                        tup = tuple(item.get(k) for k in keys)
                        if tup in seen_t:
                            dup = tup
                            errors.append(f"{inst}/{field}: uniqueness {keys} duplicate {tup}")
                            break
                        seen_t[tup] = i
                condtrace.emit(
                    condition=sp, instance=inst, field=field, comparison="uniqueness",
                    left=list(keys), right=dup, result="refuse" if dup else "pass",
                )
        if kw == "x-opensip-vocabulary":
            err = _check_vocabulary(val, site["annot"], inst, field, sp, parent=site.get("parent"))
            if err:
                errors.append(err)
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
    for site in xsites.iter_x_sites(instance, schema, base_id, path):
        if site["keyword"] != "x-opensip-digest":
            continue
        annot = site["annot"]
        val = site["value"]
        err = _require_digest(
            val,
            annot,
            st,
            f"{site['root']}/{site['field']}" if site["field"] != "/" else site["root"],
            parent=site["parent"],
            root=site["root"],
            field=site["field"],
            schema_ptr=site["schema_ptr"],
        )
        if err:
            errors.append(err)
        if isinstance(val, str):
            errors.extend(_admit_nested_canonical(val, annot, st, f"{site['root']}/{site['field']}", seen))
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


def _inventory() -> dict[str, dict]:
    inv = GRAPH_CTX.get("inventory")
    if inv:
        return inv
    st = GRAPH_CTX.get("store")
    if st is None:
        return {}
    for ident, obj in st.objects.items():
        if ident.startswith("snapshot2:") and isinstance(obj, dict):
            return {r["path"]: r for r in (obj.get("sourceInventory") or []) if isinstance(r, dict) and "path" in r}
    return {}


def _check_vocabulary(value: Any, annot: dict, inst: str, field: str, sp: str, parent: Any = None) -> str | None:
    auth = (annot or {}).get("authority") or ""
    members: list[str] | None = None
    if "languageModes/map" in auth:
        members = list(kit_schemas.identity_schema()["x-opensip-digest-domains"]["languageModes"]["map"])
    elif auth.endswith("/byDomain") or auth.endswith("byDomain"):
        members = list(kit_schemas.identity_schema()["x-opensip-digest-domains"]["byDomain"])
    elif "native-capability-matrix" in auth and "capabilities" in auth:
        matrix = json.loads(
            (kit_schemas.KIT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json").read_text()
        )
        members = [c["id"] for c in matrix.get("capabilities") or []]
    elif "x-opensip-config-node-kind-law" in auth:
        native = kit_schemas.SCHEMAS["urn:opensip:product-v1:native:evidence-schemas:v2"]
        law = native.get("x-opensip-config-node-kind-law") or {}
        path = parent.get("path") if isinstance(parent, dict) else None
        basename = str(path).rsplit("/", 1)[-1] if path else ""
        want = (law.get("basenames") or {}).get(basename, law.get("otherwise") or "other")
        ok = value == want
        condtrace.emit(
            condition=sp, instance=inst, field=field, comparison="basename-kind",
            left=value, right=want, result="pass" if ok else "refuse",
        )
        condtrace.emit(
            condition="/x-opensip-config-node-kind-law", instance=inst, field=field,
            comparison="basename-kind", left=basename, right=want, result="pass" if ok else "refuse",
        )
        if not ok:
            return f"{inst}/{field}: config-node-kind {value!r} != {want} for basename {basename!r}"
        return None
    if members is None:
        admission = str((annot or {}).get("admission") or "")
        if "shape only" in admission.lower() or not any(
            tok in auth for tok in (".json#", "/x-opensip-", "capabilities[]", "languageModes")
        ):
            condtrace.emit(
                condition=sp, instance=inst, field=field, comparison="vocabulary-shape-only",
                left=value, right=auth[:80], result="pass",
            )
            return None
        condtrace.emit(
            condition=sp, instance=inst, field=field, comparison="vocabulary-dispatch",
            left=auth, right=None, result="refuse-unhandled-authority",
        )
        return f"{inst}/{field}: unhandled x-opensip-vocabulary authority {auth!r}"
    ok = value in members
    condtrace.emit(
        condition=sp, instance=inst, field=field, comparison="in-vocabulary",
        left=value, right=ok, result="pass" if ok else "refuse",
    )
    if not ok:
        return f"{inst}/{field}: vocabulary {value!r} not in {auth}"
    return None


def _require_digest(
    value: Any,
    annot: dict,
    st: store.Store,
    path: str,
    parent: Any = None,
    root: str = "",
    field: str = "/",
    schema_ptr: str = "",
) -> str | None:
    root = root or path
    sp = schema_ptr or "/x-opensip-digest"
    rep = annot.get("representation")
    retention = annot.get("retention")
    if retention == "derived":
        condtrace.emit(
            condition=sp, instance=root, field=field, comparison="derived",
            left=value if isinstance(value, (str, int)) else type(value).__name__,
            right=annot.get("derivedFrom"), result="pass-derived",
        )
        return None

    if rep == "by-domain":
        dname = parent.get("domain") if isinstance(parent, dict) else None
        if not dname:
            dname = annot.get("domain") or annot.get("byDomainKey")
        idsch = kit_schemas.identity_schema()
        by = (idsch.get("x-opensip-digest-domains") or {}).get("byDomain") or {}
        if dname not in by:
            condtrace.emit(
                condition=sp, instance=root, field=field, comparison="by-domain-sibling",
                left=dname, right=None, result="refuse",
            )
            condtrace.emit(
                condition="/x-opensip-digest-domains/byDomain", instance=root, field=field,
                comparison="by-domain-lookup", left=dname, right=None, result="refuse",
            )
            return f"{path}: by-domain {dname} unregistered"
        row = by[dname]
        term = row.get("representation")
        if term == "by-domain":
            condtrace.emit(
                condition=f"/x-opensip-digest-domains/byDomain/{dname}", instance=root, field=field,
                comparison="terminal-forbidden", left=term, right=None, result="refuse",
            )
            return f"{path}: byDomain/{dname} names terminal by-domain (forbidden)"
        condtrace.emit(
            condition=sp, instance=root, field=field, comparison="by-domain-sibling",
            left=dname, right=term, result="pass",
        )
        condtrace.emit(
            condition=f"/x-opensip-digest-domains/byDomain/{dname}", instance=root, field=field,
            comparison="dispatch", left=dname, right=term, result="pass",
        )
        nested = dict(annot)
        nested.update({k: v for k, v in row.items() if k not in nested})
        nested["representation"] = term
        return _require_digest(value, nested, st, path, parent=parent, root=root, field=field, schema_ptr=sp)

    if rep == "snapshot-path":
        if not isinstance(value, str):
            condtrace.emit(
                condition=sp, instance=root, field=field, comparison="snapshot-path-type",
                left=type(value).__name__, right="str", result="refuse",
            )
            return f"{path}: snapshot-path requires string path, got {type(value).__name__}"
        if retention == "not-joined":
            condtrace.emit(
                condition=sp, instance=root, field=field, comparison="not-joined",
                left=value, right=annot.get("join"), result="inapplicable",
            )
            return None
        if isinstance(parent, dict) and parent.get("changeKind") == "deleted":
            condtrace.emit(
                condition=sp, instance=root, field=field, comparison="unless-deleted",
                left=value, right="deleted", result="inapplicable",
            )
            return None
        inv = _inventory()
        ok = value in inv
        condtrace.emit(
            condition=sp, instance=root, field=field, comparison="in-inventory",
            left=value, right=ok, result="pass" if ok else "refuse",
        )
        if not ok:
            return f"{path}: snapshot-path {value!r} not in snapshot inventory"
        return None

    if annot.get("codec") == "uint64":
        dg = None
        if isinstance(parent, dict):
            dg = parent.get("contentSha256") or parent.get("sha256")
        blob = None
        if dg:
            blob = st.blobs.get(_bare(str(dg))) or st.blobs.get(str(dg))
        want = len(blob) if blob is not None else None
        ok = isinstance(value, int) and not isinstance(value, bool) and want is not None and value == want
        condtrace.emit(
            condition=sp, instance=root, field=field, comparison="uint64-length",
            left=value, right=want, result="pass" if ok else "refuse",
        )
        if not ok:
            return f"{path}: uint64 length {value} != retained {want}"
        return None

    if not isinstance(value, str):
        condtrace.emit(
            condition=sp, instance=root, field=field, comparison="digest-type",
            left=type(value).__name__, right="str", result="refuse",
        )
        return f"{path}: digest representation {rep} requires string, got {type(value).__name__}"

    if retention == "derived":
        return None
    bare = _bare(value)
    if rep in ("raw-artifact", "canonical-record", "framed-body-identity"):
        ok = bare in st.blobs or value in st.blobs
        condtrace.emit(
            condition=sp, instance=root, field=field, comparison="blob-retained",
            left=bare, right=ok, result="pass" if ok else "refuse",
        )
        if not ok:
            return f"{path}: {rep} digest {bare} not retained in blobs"
        if rep == "raw-artifact" and isinstance(parent, dict) and "path" in parent:
            inv = _inventory()
            pth = parent.get("path")
            if pth in inv and parent.get("contentSha256") == value:
                row = inv[pth]
                eq = row.get("sha256") == _bare(value)
                condtrace.emit(
                    condition=sp, instance=root, field=field, comparison="inventory-sha256",
                    left=_bare(value), right=row.get("sha256"), result="pass" if eq else "refuse",
                )
                if not eq:
                    return f"{path}: contentSha256 != inventory sha256 for {pth}"
        return None
    if rep == "h-identity":
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
            condtrace.emit(
                condition=sp, instance=root, field=field, comparison="h-frame-retained",
                left=value, right=None, result="refuse",
            )
            return f"{path}: h-identity {value} preimage not retained (representation={rep} domain={domain} domainSet={domain_set})"
        if frame is not None:
            try:
                parsed_domain, cx = h.parse_h_frame(frame)
            except Exception:
                try:
                    json.loads(frame.decode("utf-8"))
                    condtrace.emit(
                        condition=sp, instance=root, field=field, comparison="h-frame-not-c",
                        left=value, right="C(X)", result="refuse",
                    )
                    return f"{path}: h-identity {value} retained C(X) under H digest; framed preimage required"
                except Exception:
                    condtrace.emit(
                        condition=sp, instance=root, field=field, comparison="h-frame-parse",
                        left=value, right=None, result="refuse",
                    )
                    return f"{path}: h-identity {value} retained bytes are not an H frame"
            if hashlib.sha256(frame).hexdigest() != bare:
                condtrace.emit(
                    condition=sp, instance=root, field=field, comparison="h-frame-hash",
                    left=hashlib.sha256(frame).hexdigest(), right=bare, result="refuse",
                )
                return f"{path}: h-identity {value} SHA256(frame)!=digest"
            if typed is not None:
                restated = canonical.encode(typed)
                if cx != restated:
                    condtrace.emit(
                        condition=sp, instance=root, field=field, comparison="h-frame-c",
                        left=True, right=False, result="refuse",
                    )
                    return f"{path}: h-identity {value} H-frame C(X) != stored object"
            if domain and parsed_domain != domain and parsed_domain.split(".")[0] != str(domain):
                if domain in h.PREFIX and parsed_domain != domain:
                    condtrace.emit(
                        condition=sp, instance=root, field=field, comparison="h-frame-domain",
                        left=parsed_domain, right=domain, result="refuse",
                    )
                    return f"{path}: h-identity {value} frame domain {parsed_domain}!={domain}"
        condtrace.emit(
            condition=sp, instance=root, field=field, comparison="h-identity",
            left=bare, right=domain or domain_set, result="pass",
        )
        return None
    if rep == "capability-manifest-id":
        condtrace.emit(
            condition=sp, instance=root, field=field, comparison="derived-delegate-close_run",
            left=value, right="plan.capabilityManifestBytesDigest", result="delegated",
        )
        return None
    condtrace.emit(
        condition=sp, instance=root, field=field, comparison="dispatch",
        left=rep, right=None, result="refuse-unhandled-representation",
    )
    return f"{path}: unhandled x-opensip-digest representation {rep}"


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
