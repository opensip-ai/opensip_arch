"""Executor for the published x-opensip-digest closing law over ADMITTED instances.

Sources: identity-and-evidence s3 'The closing digest law'; identity-schemas.v3.json #/x-opensip-digest-domains
(byDomain, domainSets, retention) and #/x-opensip-payload-registry; relation-payload-schemas.v2.json
#/x-opensip-digest-law. Stock JSON Schema ignores these keywords. This walks an instance together with its schema
(same branch discipline as the x-opensip-order walk) and resolves every annotated digest against the retained store:
raw-artifact bytes retained; canonical-record bytes retained, canonical, and admitted under the named record (payload
class rows resolved by their keyedBy); h-identity frame retained, domain in the named set, H recomputed;
capability-manifest-id recomputed from the committed bytes; by-domain dispatched through byDomain; fragment
recomputed where located. Bare 64-hex values reached without an annotation are reported; they are refusals inside the
documents the law names (identity, native, relation bundles) and a reported census elsewhere (notes/02 candidate 4).
"""
import hashlib

import canonical as K
import cve1
import schemas

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
REL_DOC = "foundation/relation-payload-schemas.v2.json"
DD = KIT.doc(ID)["x-opensip-digest-domains"]
BYDOMAIN = DD["byDomain"]
SETS = DD["domainSets"]
CLASSES = KIT.doc(ID)["x-opensip-payload-registry"]["classes"]
RELREG = KIT.doc(REL_DOC)["x-opensip-relation-registry"]
HEX64 = schemas.HEX64
LAW_DOCS = {schemas.norm_rel(ID), schemas.norm_rel("native/native-evidence.schemas.v2.json"), schemas.norm_rel(REL_DOC)}
REPRESENTATIONS = {"raw-artifact", "canonical-record", "h-identity", "capability-manifest-id", "by-domain", "snapshot-path",
                   "framed-body-identity"}


def registered_payload_documents():
    docs = {REL_DOC}
    for cls in ("coverage", "import", "parameter"):
        for row in CLASSES[cls]["rows"].values():
            docs.add(row["document"])
    return {KIT.digest(d): d for d in docs}


REGISTERED_DOCS = registered_payload_documents()


def collect(instance, rel, selector):
    resolver = KIT.registry.resolver(base_uri=KIT.base_uri(rel))
    start = KIT.resolve_pointer(rel, selector)
    annotated, hexes = {}, {}
    _walk(start, instance, resolver, "$", None, annotated, hexes, 0)
    return annotated, hexes


def _walk(schema, inst, resolver, path, parent, annotated, hexes, depth):
    if depth > 200 or not isinstance(schema, dict):
        return
    if isinstance(inst, str):
        if "x-opensip-digest" in schema:
            annotated.setdefault(path, (inst, schema["x-opensip-digest"], parent))
        if schema.get("pattern") == HEX64:
            hexes[path] = inst
    if "$ref" in schema:
        r = resolver.lookup(schema["$ref"])
        _walk(r.contents, inst, r.resolver, path, parent, annotated, hexes, depth + 1)
    for sub in schema.get("allOf", []):
        _walk(sub, inst, resolver, path, parent, annotated, hexes, depth + 1)
    for key in ("anyOf", "oneOf"):
        for sub in schema.get(key, []):
            if KIT._is_valid(sub, inst, resolver):
                _walk(sub, inst, resolver, path, parent, annotated, hexes, depth + 1)
    if "if" in schema:
        if KIT._is_valid(schema["if"], inst, resolver):
            if "then" in schema:
                _walk(schema["then"], inst, resolver, path, parent, annotated, hexes, depth + 1)
        elif "else" in schema:
            _walk(schema["else"], inst, resolver, path, parent, annotated, hexes, depth + 1)
    if isinstance(inst, list) and isinstance(schema.get("items"), dict):
        for i, item in enumerate(inst):
            _walk(schema["items"], item, resolver, f"{path}[{i}]", parent, annotated, hexes, depth + 1)
    if isinstance(inst, dict):
        props = schema.get("properties", {})
        for k, v in inst.items():
            if k in props:
                _walk(props[k], v, resolver, f"{path}.{k}", inst, annotated, hexes, depth + 1)
            elif isinstance(schema.get("additionalProperties"), dict):
                _walk(schema["additionalProperties"], v, resolver, f"{path}.{k}", inst, annotated, hexes, depth + 1)


def _hex(value):
    return value[7:] if value.startswith("sha256:") else value


def _record_row(record, parent, rec):
    """Returns (document, selector) for a canonical-record annotation, or raises KeyError-like AdmissionError."""
    if "bundle" in record:
        return ID, record["selector"]
    if "document" in record:
        return record["document"], record["selector"]
    cls = record["payloadClass"]
    if "resolvedThrough" in record:
        raise K.AdmissionError("DIGEST_BARE_PAYLOAD_ROOT", cls)
    if cls == "relation":
        row = RELREG["relations"].get(parent.get("relation"))
        if row is None:
            raise K.AdmissionError("DIGEST_PAYLOAD_ROW_UNREGISTERED", f"relation:{parent.get('relation')}")
        if parent.get(record["schemaDigestField"]) != KIT.digest(REL_DOC):
            raise K.AdmissionError("DIGEST_PAYLOAD_SCHEMA_DIGEST_JOIN", "relation")
        return REL_DOC, row["selector"]
    if cls == "coverage":
        row = CLASSES["coverage"]["rows"].get(str(rec.get("schemaVersion")))
    elif cls == "import":
        row = CLASSES["import"]["rows"].get(f"{parent.get('kind')}|{rec.get('payloadDomain')}")
    elif cls == "parameter":
        row = next((r for r in CLASSES["parameter"]["rows"].values() if KIT.digest(r["document"]) == parent.get(record["schemaDigestField"])), None)
    else:
        row = None
    if row is None:
        raise K.AdmissionError("DIGEST_PAYLOAD_ROW_UNREGISTERED", cls)
    if cls != "parameter" and parent.get(record["schemaDigestField"]) != KIT.digest(row["document"]):
        raise K.AdmissionError("DIGEST_PAYLOAD_SCHEMA_DIGEST_JOIN", cls)
    return row["document"], row["selector"]


def _node_at(pred, addr):
    parts = addr.split(".")
    if parts[0] != "p":
        return None
    cur = pred
    for p in parts[1:]:
        i = int(p)
        if cur["op"] in ("and", "or"):
            cur = cur["operands"][i]
        elif cur["op"] == "not" and i == 0:
            cur = cur["operand"]
        else:
            return None
    return cur


def check_value(store, path, value, ann, parent, ctx):
    rep = ann.get("representation")
    faults = []
    if rep not in REPRESENTATIONS:
        return [f"DIGEST_REPRESENTATION_UNREGISTERED:{path}:{rep}"]
    if rep == "snapshot-path":
        return []
    if rep == "framed-body-identity":
        # relation x-opensip-digest-law: frame retained under the 64-hex suffix (retention provider-output-retained);
        # the parse/level/language/L0-span join is the owner bodyIdentityJoin applied by native_facts.clones_join_faults.
        hx = _hex(value)
        if hx not in store.blobs:
            return [f"DIGEST_PREIMAGE_MISSING:{path}"]
        return [] if hashlib.sha256(store.blobs[hx]).hexdigest() == hx else [f"DIGEST_PREIMAGE_MISMATCH:{path}"]
    if rep == "by-domain":
        row = BYDOMAIN.get((parent or {}).get("domain"))
        if row is None:
            return [f"DIGEST_BY_DOMAIN_UNREGISTERED:{path}:{(parent or {}).get('domain')}"]
        return check_value(store, path, value, row, parent, ctx)
    if rep == "capability-manifest-id":
        plan = ctx.get("plan")
        b = store.blobs.get(plan["capabilityManifestBytesDigest"]) if plan else None
        if b is None:
            return [f"DIGEST_DERIVED_SOURCE_MISSING:{path}"]
        return [] if cve1.capability_manifest_id(b) == value else [f"DIGEST_DERIVED_MISMATCH:{path}"]
    if ann.get("retention") == "owner-retained":
        return []
    if rep == "h-identity" and ann.get("retention") == "derived":
        # identity x-opensip-digest-domains.retention.derived: recomputed from another retained record by the stated
        # recipe; no separate preimage exists (e.g. SourceUnitOwnershipV1 unitId, re-derived by bind_rust_universe).
        return []
    if rep == "raw-artifact":
        hx = _hex(value)
        if hx not in store.blobs:
            return [f"DIGEST_PREIMAGE_MISSING:{path}"]
        if hashlib.sha256(store.blobs[hx]).hexdigest() != hx:
            return [f"DIGEST_PREIMAGE_MISMATCH:{path}"]
        if ann.get("artifactClass") == "registered-schema-document" and hx not in REGISTERED_DOCS:
            faults.append(f"SCHEMA_DOCUMENT_UNREGISTERED:{path}")
        return faults
    if rep == "canonical-record":
        record = ann.get("record", {})
        if ann.get("retention") == "fragment":
            loc = ann["locatedBy"]
            prog_hex = parent.get(loc["record"])
            if prog_hex not in store.blobs:
                return [f"DIGEST_FRAGMENT_OWNER_MISSING:{path}"]
            prog = store.get_record(prog_hex)
            rule = next((r for r in prog.get("rules", []) if r.get("ruleId") == parent.get("ruleId")), None)
            node = _node_at(rule["emitWhen"], parent.get(loc["addressedBy"])) if rule else None
            if node is None:
                return [f"DIGEST_FRAGMENT_UNLOCATED:{path}"]
            if hashlib.sha256(K.C(node)).hexdigest() != value:
                return [f"DIGEST_FRAGMENT_MISMATCH:{path}"]
            r = KIT.admit(node, record["document"], record["selector"])
            return [] if r["ok"] else [f"DIGEST_FRAGMENT_RECORD_REFUSED:{path}:{record['document']}{record['selector']}"]
        hx = _hex(value)
        if hx not in store.blobs:
            return [f"DIGEST_PREIMAGE_MISSING:{path}"]
        try:
            rec = store.get_record(hx)
        except K.AdmissionError as exc:
            return [f"DIGEST_PREIMAGE_NOT_CANONICAL:{path}:{exc.boundary}"]
        try:
            doc, sel = _record_row(record, parent or {}, rec)
        except K.AdmissionError as exc:
            return [f"{exc.boundary}:{path}:{exc.detail}"]
        r = KIT.admit(rec, doc, sel)
        if not r["ok"]:
            return [f"DIGEST_RECORD_REFUSED:{path}:{doc}{sel}"]
        return _descend(store, hx, rec, doc, sel, ctx, path)
    if rep == "h-identity":
        if "domainSet" in ann:
            allowed = set(SETS[ann["domainSet"]].keys())
        elif "<language>" in ann.get("domain", ""):
            allowed = set(SETS["native-semantic-universe"].keys())
        else:
            allowed = {ann["domain"]}
        hx = _hex(value)
        if hx not in store.blobs:
            return [f"DIGEST_PREIMAGE_MISSING:{path}"]
        try:
            d, v = store.get_frame(hx, allowed)
        except K.AdmissionError as exc:
            return [f"DIGEST_FRAME_REFUSED:{path}:{exc.boundary}"]
        if K.H(d, v) != hx:
            return [f"DIGEST_FRAME_MISMATCH:{path}"]
        row = BYDOMAIN.get(d)
        if row is not None and row.get("representation") == "h-identity":
            doc, sel = ID, f"#/$defs/{d}"
        else:
            nrow = SETS.get("native-context", {}).get(d) or SETS.get("native-semantic-universe", {}).get(d) or SETS.get("native-nested", {}).get(d)
            if nrow is None or "selector" not in nrow:
                return faults
            doc, sel = nrow.get("document", "native/native-evidence.schemas.v2.json"), nrow["selector"]
        return _descend(store, hx, v, doc, sel, ctx, path)
    return faults


def _descend(store, hx, value, doc, sel, ctx, path):
    """Transitive closure: every retained record/frame reached through an annotation has its own annotations executed
    (the closing law applies to every retained digest field, not only those of the root record). Visited-set guarded."""
    seen = ctx.setdefault("_visited", set())
    key = (hx, schemas.norm_rel(doc), sel)
    if key in seen:
        return []
    seen.add(key)
    r = KIT.admit(value, doc, sel)
    if not r["ok"]:
        return [f"DIGEST_RECORD_REFUSED:{path}:{doc}{sel}"]
    res = check_instance(store, value, doc, sel, ctx)
    if res["unannotatedOutsideLaw"]:
        ctx.setdefault("_outsideLaw", {}).setdefault(f"{doc}{sel}", res["unannotatedOutsideLaw"])
    return [f"{f}<-{path}" for f in res["faults"]]


def check_instance(store, instance, rel, selector, ctx):
    annotated, hexes = collect(instance, rel, selector)
    faults = []
    for path, (value, ann, parent) in sorted(annotated.items()):
        faults += check_value(store, path, value, ann, parent, ctx)
    unannotated = sorted(p for p in hexes if p not in annotated)
    in_law = schemas.norm_rel(rel) in LAW_DOCS
    if in_law:
        faults += [f"DIGEST_FIELD_UNANNOTATED:{p}" for p in unannotated]
    return {"annotated": len(annotated), "faults": faults, "unannotatedOutsideLaw": [] if in_law else unannotated}
