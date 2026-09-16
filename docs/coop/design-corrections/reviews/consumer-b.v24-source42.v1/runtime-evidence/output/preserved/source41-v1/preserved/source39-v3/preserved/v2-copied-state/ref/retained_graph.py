"""Independent retained-closure walker (source39.v2 self-audit; helper correction HC-33).

Derives the COMPLETE retained graph a Run requires from the owning schemas and registries alone, starting at run3, and admits
it before any replay. Normative basis:
  - evaluator-composition-contract.v3 s7: "Closing these outputs traverses their reference fields under the owning schemas. A
    field declared as a typed-prefix identity resolves and admits the retained descriptor in its prefix-selected identity
    domain; checking only bare fields carrying x-opensip-digest does not close typed-prefix references ... A replay
    implementation cannot establish complete retention by comparing only an output subset selected by its own emitter."
  - identity-and-evidence s3: domain/prefix table; closing digest law (representations, retention modes, frame admission);
    "Every visited fact/scope and view/proof/execution/evidence/seal joins the current source or Plan, including objects
    reached through typed Ref fields".
  - identity-schemas.v3 #/x-opensip-digest-domains (byDomain, domainSets with closureJoins / nestedIdentities / nestedRecords /
    blobJoins / snapshotJoins / contextAgreementFields, closureMembership, closureKinds) and #/x-opensip-payload-registry.
  - native-evidence.schemas.v2 and relation-payload-schemas.v2 #/x-opensip-digest-law retention vocabularies.

Independence: reads only the exported content-addressed blobs and the kit. It does not import builders, evaluator, closure,
digestlaw, native_ctx, native_facts, imports or membership, never reads the export objectTable, and never consults recomputed
outputs to decide what is required. canonical.py is used only for the section-3 C codec; schemas.py only for kit-document
Draft 2020-12 plus x-opensip-order admission.

Obligations are reported separately (never merged into one pass/fail):
  LEXICAL   retained bytes are not a valid frame / not exact C of their own parse
  SCHEMA    a resolved record fails its owning selector, or a law position is unannotated / unregistered
  IDENTITY  typed prefix outside the current identity table, frame domain outside the prefix/annotation domain set
  RETENTION promised bytes absent, declared length differs
  JOIN      closure membership/kind, derived recipe, fragment location, closure-tree membership, snapshot inventory,
            Plan/snapshot join, context agreement, selected import
Owner-semantic admissions (native context admission, universe binding, relation body-identity parse joins, enumeration,
execution-input derivation) are NOT re-implemented here; they stay with the owner graph admission, which runs as its own stage.
"""
import base64
import hashlib
import json
import re
from collections import Counter, deque

import canonical as K
import schemas

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
NE = "native/native-evidence.schemas.v2.json"
REL = "foundation/relation-payload-schemas.v2.json"
IDOC = KIT.doc(ID)
DD = IDOC["x-opensip-digest-domains"]
BYDOMAIN = DD["byDomain"]
SETS = DD["domainSets"]
PAYREG = IDOC["x-opensip-payload-registry"]["classes"]
RELREG = KIT.doc(REL)["x-opensip-relation-registry"]["relations"]
MEMBERSHIP = DD["closureMembership"]
KINDS = DD["closureKinds"]["byField"]
TAG = b"opensip.product.v1"
HEX64 = schemas.HEX64
HEXRE = re.compile(r"^[0-9a-f]{64}$")
TYPED_PATTERN = re.compile(r"^\^([a-z][a-z0-9-]*[0-9]):\[0-9a-f\]\{64\}\(\?!\[\\s\\S\]\)$")

# identity-and-evidence s3 domain/prefix table (current rows) and evaluator-composition-contract.v3 s9.7 output table
PREFIX_DOMAIN = {
    "snapshot2": "snapshot", "closure2": "closure", "import2": "import", "plan2": "plan", "scope2": "subject-scope",
    "fact2": "fact", "coverage2": "coverage", "view2": "view", "exec-plan2": "execution-plan",
    "finding-key2": "finding-fingerprint", "subject3": "evaluation-subject", "finding3": "finding", "proof3": "proof-bundle",
    "evidence3": "semantic-evidence", "seal3": "evaluation-seal", "run3": "run", "cache2": "cache-key",
    "regen2": "regeneration-key", "policy-derivation3": "policy-derivation",
}
DOMAIN_PREFIX = {d: p for p, d in PREFIX_DOMAIN.items()}
SEMANTIC_OUTPUT_DOMAINS = ("run", "evaluation-seal", "semantic-evidence", "proof-bundle", "finding", "finding-fingerprint",
                           "evaluation-subject")
PLAN_JOINED_DOMAINS = {"fact", "subject-scope", "view", "proof-bundle", "execution-plan", "semantic-evidence", "evaluation-seal",
                       "run", "stage-spec", "cache-key", "regeneration-key"}
# identity s3: the closing law governs identity-schemas.v3 and the relation bundle; native carries its own sweep; the listed
# foundation record documents are swept before they are walked (FOUNDATION_DIGEST_UNANNOTATED).
LAW_DOCS = {schemas.norm_rel(d) for d in (ID, NE, REL, "foundation/enumeration-plan.schema.v1.json",
                                          "foundation/subject-inventory.schema.v1.json",
                                          "foundation/evaluator-emission-plan.schema.v1.json",
                                          "foundation/target-attribution.schema.v1.json", "foundation/target-attribution.schema.v2.json",
                                          "foundation/incoming-search.schema.v1.json", "foundation/execution-inputs.schema.v1.json",
                                          "foundation/import-source-context.schema.json")}
RETENTION_VOCAB = {
    schemas.norm_rel(ID): set(DD["retention"]),
    schemas.norm_rel(NE): set(KIT.doc(NE)["x-opensip-digest-law"]["retention"]),
    schemas.norm_rel(REL): set(KIT.doc(REL)["x-opensip-digest-law"]["retention"]),
}
CAP_MANIFEST_TAG = b"opensip.capability-manifest.v1\x00"


def _registered_schema_documents():
    docs = {REL}
    for cls in ("coverage", "import", "parameter"):
        for row in PAYREG[cls]["rows"].values():
            docs.add(row["document"])
    return {KIT.digest(d): d for d in docs}


REGISTERED_DOCS = _registered_schema_documents()
SET_ROWS = {dom: (set_name, row) for set_name, rows in SETS.items() for dom, row in rows.items()}


class ExportError(Exception):
    pass


def load_cas(exported):
    """The content-addressed store of an export: raw SHA-256 -> bytes, every key re-hashed (identity s3: one CAS)."""
    blobs = {}
    for h, b64 in exported["blobs"].items():
        b = base64.b64decode(b64, validate=True)
        if hashlib.sha256(b).hexdigest() != h:
            raise ExportError(f"EXPORT_BLOB_DIGEST_MISMATCH:{h}")
        blobs[h] = b
    return blobs


def parse_frame(b):
    """identity s3 frame admission grammar. Returns (domain, value, error)."""
    head = TAG + b"\x00"
    if not b.startswith(head):
        return None, None, "FRAME_PREFIX"
    rest = b[len(head):]
    nul = rest.find(b"\x00")
    if nul <= 0:
        return None, None, "FRAME_DOMAIN_TERMINATOR"
    try:
        dom = rest[:nul].decode("ascii")
    except UnicodeDecodeError:
        return None, None, "FRAME_DOMAIN_ASCII"
    rest = rest[nul + 1:]
    if len(rest) < 8:
        return None, None, "FRAME_LENGTH_FIELD"
    body = rest[8:]
    if int.from_bytes(rest[:8], "big") != len(body):
        return None, None, "FRAME_LENGTH_MISMATCH"
    try:
        v = K.parse_raw(body)
        if K.C(v) != body:
            return None, None, "FRAME_NOT_CANONICAL"
    except K.AdmissionError as exc:
        return None, None, f"FRAME_BODY_REFUSED:{exc.boundary}"
    return dom, v, None


def at_path(value, path):
    nodes = [value]
    for seg in path:
        nxt = []
        for n in nodes:
            if seg == "[]":
                if isinstance(n, list):
                    nxt.extend(n)
            elif isinstance(n, dict) and seg in n:
                nxt.append(n[seg])
        nodes = nxt
    return nodes


def _hex_of(value, form=None):
    if not isinstance(value, str):
        return None
    if ":" in value:
        value = value.split(":", 1)[1]
    return value if HEXRE.match(value) else None


class Walker:
    def __init__(self, cas):
        self.cas = cas
        self.faults = []
        self.classes = Counter()
        self.frames = {}          # hex -> (domain, value)
        self.records = {}         # (hex, doc, sel) -> value
        self.required = {}        # hex -> {"class", "path"}
        self.typed = {}           # typed id -> domain (reachable descriptors)
        self.admitted = set()     # (hex, doc, sel) admitted
        self.refused = set()      # hex whose descent is masked
        self.masked = []
        self.pending = []
        self.exemptions = []
        self.delegated = []
        self.queue = deque()

    # ------------------------------------------------------------------ bookkeeping
    def fault(self, obligation, code, path, detail=""):
        self.faults.append({"obligation": obligation, "code": code, "path": path, "detail": detail})

    def need(self, hx, cls, path):
        self.required.setdefault(hx, {"class": cls, "path": path})

    def fetch(self, hx, path, cls):
        """identity s3 retention 'preimage': fetch the bytes under this digest and re-hash them."""
        b = self.cas.get(hx)
        if b is None:
            self.fault("RETENTION", "PREIMAGE_MISSING", path, cls)
            return None
        if hashlib.sha256(b).hexdigest() != hx:
            self.fault("IDENTITY", "PREIMAGE_DIGEST_MISMATCH", path, cls)
            return None
        return b

    # ------------------------------------------------------------------ resolution primitives
    def resolve_frame(self, hx, allowed, path, cls, expect_domain_note=""):
        self.classes[cls] += 1
        if hx is None:
            self.fault("LEXICAL", "IDENTITY_SUFFIX_NOT_HEX", path, cls)
            return None, None
        self.need(hx, cls, path)
        if hx in self.frames:
            dom, v = self.frames[hx]
            if dom not in allowed:
                self.fault("IDENTITY", "FRAME_DOMAIN_NOT_ALLOWED", path, f"{dom} not in {sorted(allowed)}")
                return None, None
            return dom, v
        if hx in self.refused:
            return None, None
        b = self.fetch(hx, path, cls)
        if b is None:
            self.refused.add(hx)
            return None, None
        dom, v, err = parse_frame(b)
        if err:
            self.fault("LEXICAL", err, path, cls)
            self.refused.add(hx)
            return None, None
        if dom not in allowed:
            self.fault("IDENTITY", "FRAME_DOMAIN_NOT_ALLOWED", path, f"{dom} not in {sorted(allowed)}")
            self.refused.add(hx)
            return None, None
        if dom in DOMAIN_PREFIX:
            doc, sel = ID, f"#/$defs/{dom}"
        elif dom in SET_ROWS and "selector" in SET_ROWS[dom][1]:
            doc, sel = SET_ROWS[dom][1].get("document", NE), SET_ROWS[dom][1]["selector"]
        else:
            self.fault("SCHEMA", "FRAME_DOMAIN_SELECTOR_UNREGISTERED", path, dom)
            self.refused.add(hx)
            return None, None
        r = KIT.admit(v, doc, sel)
        if not r["ok"]:
            self.fault("SCHEMA", "FRAME_RECORD_REFUSED", path, f"{dom}:{r['typed']}{r['stock'][:1]}{r['order'][:1]}")
            self.refused.add(hx)
            self.masked.append(path)
            return None, None
        self.frames[hx] = (dom, v)
        if dom in DOMAIN_PREFIX:
            self.typed[f"{DOMAIN_PREFIX[dom]}:{hx}"] = dom
        self.queue.append((v, doc, sel, path, {"frameDomain": dom, "hex": hx}))
        return dom, v

    def load_record(self, hx, path, cls):
        """Fetch + exact-C parse of a canonical-record preimage (selector chosen by the caller after parsing when keyed)."""
        self.classes[cls] += 1
        if hx is None:
            self.fault("LEXICAL", "RECORD_DIGEST_NOT_HEX", path, cls)
            return None
        self.need(hx, cls, path)
        if hx in self.refused:
            return None
        b = self.fetch(hx, path, cls)
        if b is None:
            self.refused.add(hx)
            return None
        try:
            v = K.parse_raw(b)
            if K.C(v) != b:
                raise K.AdmissionError("RECORD_NOT_CANONICAL")
        except K.AdmissionError as exc:
            self.fault("LEXICAL", "RECORD_NOT_CANONICAL", path, f"{cls}:{exc.boundary}")
            self.refused.add(hx)
            return None
        return v

    def admit_record(self, hx, v, doc, sel, path, ctx):
        key = (hx, schemas.norm_rel(doc), sel)
        if key in self.admitted:
            return True
        r = KIT.admit(v, doc, sel)
        if not r["ok"]:
            self.fault("SCHEMA", "RECORD_REFUSED", path, f"{doc}{sel}:{r['typed']}{r['stock'][:1]}{r['order'][:1]}")
            self.masked.append(path)
            return False
        self.admitted.add(key)
        self.records[key] = v
        self.queue.append((v, doc, sel, path, dict(ctx, hex=hx)))
        return True

    def raw(self, hx, path, cls, length=None):
        self.classes[cls] += 1
        if hx is None:
            self.fault("LEXICAL", "RAW_DIGEST_NOT_HEX", path, cls)
            return None
        self.need(hx, cls, path)
        b = self.fetch(hx, path, cls)
        if b is None:
            return None
        if length is not None and len(b) != length:
            self.fault("RETENTION", "ARTIFACT_LENGTH_MISMATCH", path, f"{len(b)}!={length}")
        return b

    # ------------------------------------------------------------------ schema/instance collection
    def collect(self, value, doc, sel):
        resolver = KIT.registry.resolver(base_uri=KIT.base_uri(doc))
        start = KIT.resolve_pointer(doc, sel)
        leaves = {}
        self._walk(start, value, resolver, "", None, None, leaves, 0)
        return leaves

    def _walk(self, schema, inst, resolver, path, parent, key, leaves, depth):
        if depth > 256 or not isinstance(schema, dict):
            return
        if isinstance(inst, (str, int)) and not isinstance(inst, bool):
            leaf = leaves.setdefault(path, {"value": inst, "ann": None, "typed": None, "hex": False, "parent": parent, "key": key})
            if "x-opensip-digest" in schema and leaf["ann"] is None:
                leaf["ann"] = schema["x-opensip-digest"]
            pat = schema.get("pattern")
            if isinstance(pat, str):
                m = TYPED_PATTERN.match(pat)
                if m:
                    leaf["typed"] = m.group(1)
                if pat == HEX64:
                    leaf["hex"] = True
        if "$ref" in schema:
            r = resolver.lookup(schema["$ref"])
            self._walk(r.contents, inst, r.resolver, path, parent, key, leaves, depth + 1)
        for sub in schema.get("allOf", []):
            self._walk(sub, inst, resolver, path, parent, key, leaves, depth + 1)
        for k in ("anyOf", "oneOf"):
            for sub in schema.get(k, []):
                if KIT._is_valid(sub, inst, resolver):
                    self._walk(sub, inst, resolver, path, parent, key, leaves, depth + 1)
        if "if" in schema:
            branch = "then" if KIT._is_valid(schema["if"], inst, resolver) else "else"
            if branch in schema:
                self._walk(schema[branch], inst, resolver, path, parent, key, leaves, depth + 1)
        if isinstance(inst, list):
            if isinstance(schema.get("items"), dict):
                for i, item in enumerate(inst):
                    self._walk(schema["items"], item, resolver, f"{path}[{i}]", parent, key, leaves, depth + 1)
            for i, sub in enumerate(schema.get("prefixItems", [])):
                if i < len(inst):
                    self._walk(sub, inst[i], resolver, f"{path}[{i}]", parent, key, leaves, depth + 1)
        if isinstance(inst, dict):
            props = schema.get("properties", {})
            for k, v in inst.items():
                if k in props:
                    self._walk(props[k], v, resolver, f"{path}.{k}", inst, k, leaves, depth + 1)
                elif isinstance(schema.get("additionalProperties"), dict):
                    self._walk(schema["additionalProperties"], v, resolver, f"{path}.{k}", inst, k, leaves, depth + 1)

    # ------------------------------------------------------------------ one retained record
    def descend(self, value, doc, sel, rpath, ctx):
        ndoc = schemas.norm_rel(doc)
        def_name = sel.rsplit("/", 1)[-1] if sel.startswith("#/$defs/") else ndoc
        leaves = self.collect(value, doc, sel)
        for p in sorted(leaves):
            leaf = leaves[p]
            path = f"{rpath}{p}"
            if leaf["ann"] is not None:
                if isinstance(leaf["value"], str):
                    self.annotated(leaf, path, ndoc, def_name, value, ctx)
            elif leaf["typed"] is not None and isinstance(leaf["value"], str):
                if ndoc.startswith("coop/design-corrections/workflows/"):
                    # HC-36: composition s7 closes typed-prefix references of evaluator OUTPUTS; a workflow-owned Plan input document
                    # (WaiverSetV1 target.fingerprint, PolicyDocumentV2 import pins) is admitted by its owning unit's schema admission
                    # (identity s3 lines 597-600, 627-631) and its typed values are equality keys (composition s5), not retention references.
                    self.classes["typed-prefix/workflow-owner-scoped-key"] += 1
                    self.exemptions.append({"path": path, "class": "typed-prefix/workflow-owner-scoped-key", "document": ndoc, "prefix": leaf["typed"]})
                else:
                    self.typed_ref(leaf, path, def_name, value, ctx)
            elif leaf["hex"] and ndoc in LAW_DOCS:
                code = "DIGEST_FIELD_UNANNOTATED" if ndoc in RETENTION_VOCAB else "FOUNDATION_DIGEST_UNANNOTATED"
                self.fault("SCHEMA", code, path, f"{ndoc}{sel}")
        dom = ctx.get("frameDomain")
        if dom in SET_ROWS:
            self.registry_joins(dom, value, rpath, ctx)
        if def_name in PLAN_JOINED_DOMAINS or dom in PLAN_JOINED_DOMAINS:
            for fld in ("planId", "snapshotId"):
                if isinstance(value, dict) and isinstance(value.get(fld), str):
                    self.pending.append(("plan-join", fld, value[fld], f"{rpath}.{fld}"))
        if dom == "view":
            self.pending.append(("view-fact-producer", value, rpath))
        if dom == "evaluation-seal":
            self.pending.append(("seal-proof-evaluator", value, rpath))

    def typed_ref(self, leaf, path, def_name, record, ctx):
        prefix, v = leaf["typed"], leaf["value"]
        if prefix == "sha256":
            self.fault("SCHEMA", "NATIVE_SHA256_TEXT_UNANNOTATED", path)
            return
        dom = PREFIX_DOMAIN.get(prefix)
        if dom is None:
            self.fault("IDENTITY", "IDENTITY_PREFIX_NOT_CURRENT", path, prefix)
            return
        if not v.startswith(prefix + ":"):
            self.fault("LEXICAL", "TYPED_IDENTITY_SPELLING", path, v[:24])
            return
        got, val = self.resolve_frame(_hex_of(v), {dom}, path, f"typed-prefix:{dom}")
        field = f"{def_name}.{leaf['key']}"
        if got == "closure":
            kind = KINDS.get(field)
            if kind is not None and leaf["parent"] is record:
                self.classes["closureKinds"] += 1
                if val["kind"] != kind:
                    self.fault("JOIN", "CLOSURE_KIND_MISMATCH", path, f"{field}:{val['kind']}!={kind}")
            if field in MEMBERSHIP["direct"] and leaf["parent"] is record:
                self.classes["closureMembership:direct"] += 1
                self.pending.append(("closure-direct", v, path, field))
        if got == "import":
            self.pending.append(("import-selected", v, path))

    def annotated(self, leaf, path, ndoc, def_name, record, ctx):
        ann, v, parent = leaf["ann"], leaf["value"], leaf["parent"] or {}
        rep = ann.get("representation")
        ret = ann.get("retention", "preimage")
        vocab = RETENTION_VOCAB.get(ndoc)
        if vocab is not None and ret not in vocab and ret != "preimage":
            self.fault("SCHEMA", "RETENTION_UNREGISTERED", path, f"{ndoc}:{ret}")
            return
        if rep == "by-domain":
            dname = parent.get("domain")
            row = BYDOMAIN.get(dname)
            if row is None:
                self.fault("SCHEMA", "BY_DOMAIN_UNREGISTERED", path, str(dname))
                return
            self.classes[f"by-domain:{dname}"] += 1
            self.annotated(dict(leaf, ann=row), path, schemas.norm_rel(ID), def_name, record, ctx)
            return
        cls = f"{rep}/{ret}"
        if rep == "h-identity":
            if ret == "derived":
                self.classes[cls] += 1
                self.delegated.append({"path": path, "class": cls, "owner": "owner binding recomputes (identity x-opensip-digest-domains.retention.derived)"})
                return
            if "domainSet" in ann:
                allowed = set(SETS[ann["domainSet"]])
            elif "<language>" in ann.get("domain", ""):
                allowed = set(SETS["native-semantic-universe"])
            else:
                allowed = {ann.get("domain")}
            got, val = self.resolve_frame(_hex_of(v), allowed, path, cls)
            if got == "closure" and ann.get("kind") and val is not None:
                self.classes["closureKinds"] += 1
                if val["kind"] != ann["kind"]:
                    self.fault("JOIN", "CLOSURE_KIND_MISMATCH", path, f"{val['kind']}!={ann['kind']}")
            return
        if rep == "canonical-record":
            record_ann = ann.get("record", {})
            if ret == "owner-retained":
                self.classes[cls] += 1
                self.exemptions.append({"path": path, "class": cls})
                return
            if ret == "fragment":
                self.fragment(ann, v, parent, path, cls)
                return
            hx = _hex_of(v)
            rec = self.load_record(hx, path, cls)
            if rec is None:
                return
            row = self.record_row(record_ann, parent, rec, path)
            if row is None:
                self.refused.add(hx)
                return
            child_ctx = {"ownerFact": ctx.get("hex")} if record_ann.get("payloadClass") == "relation" else {}
            if record_ann.get("payloadClass") == "relation":
                child_ctx["ownerFactSnapshot"] = record.get("snapshotId")
            self.admit_record(hx, rec, row[0], row[1], path, child_ctx)
            return
        if rep == "raw-artifact":
            if ret == "owner-retained":
                self.classes[cls] += 1
                self.exemptions.append({"path": path, "class": cls})
                return
            if ret == "closure-tree-member":
                self.classes[cls] += 1
                self.pending.append(("tree-member", _hex_of(v), path, ctx.get("joinedClosures", [])))
                return
            length = None
            for lf in ("bytes", "byteLength"):
                if isinstance(parent.get(lf), int) and not isinstance(parent.get(lf), bool) and leaf["key"] in ("sha256", "contentSha256"):
                    length = parent[lf]
            b = self.raw(_hex_of(v), path, cls, length)
            if b is not None and ann.get("artifactClass") == "registered-schema-document" and _hex_of(v) not in REGISTERED_DOCS:
                self.fault("JOIN", "SCHEMA_DOCUMENT_UNREGISTERED", path)
            if ann.get("registeredBy"):
                self.classes["raw-artifact/registeredBy-closure-tree"] += 1
                self.pending.append(("tree-member", _hex_of(v), path, [_hex_of(parent.get(ann["registeredBy"]["closureField"]))]))
            return
        if rep == "capability-manifest-id":
            self.classes[cls] += 1
            self.pending.append(("capability-manifest-id", v, path))
            return
        if rep == "snapshot-path":
            self.classes[cls] += 1
            if ret == "not-joined":
                self.exemptions.append({"path": path, "class": cls})
            else:
                self.pending.append(("snapshot-path", v, path, ctx.get("ownerFactSnapshot")))
            return
        if rep == "framed-body-identity":
            self.raw(_hex_of(v), path, cls)
            self.delegated.append({"path": path, "class": cls, "owner": "relation bodyIdentityJoin parse joins (owner graph admission)"})
            return
        self.fault("SCHEMA", "DIGEST_REPRESENTATION_UNREGISTERED", path, str(rep))

    def record_row(self, record_ann, parent, rec, path):
        if "bundle" in record_ann:
            return ID, record_ann["selector"]
        if "document" in record_ann:
            return record_ann["document"], record_ann["selector"]
        cls = record_ann.get("payloadClass")
        if cls is None or "resolvedThrough" in record_ann:
            self.fault("SCHEMA", "DIGEST_BARE_PAYLOAD_ROOT", path, str(cls))
            return None
        sdf = record_ann.get("schemaDigestField")
        if cls == "relation":
            row = RELREG.get(parent.get("relation"))
            doc, sel = REL, (row or {}).get("selector")
        elif cls == "coverage":
            row = PAYREG["coverage"]["rows"].get(str(rec.get("schemaVersion")) if isinstance(rec, dict) else None)
            doc, sel = (row or {}).get("document"), (row or {}).get("selector")
        elif cls == "import":
            row = PAYREG["import"]["rows"].get(f"{parent.get('kind')}|{rec.get('payloadDomain') if isinstance(rec, dict) else None}")
            doc, sel = (row or {}).get("document"), (row or {}).get("selector")
        elif cls == "parameter":
            rows = [r for r in PAYREG["parameter"]["rows"].values() if KIT.digest(r["document"]) == parent.get(sdf)]
            if len(rows) > 1:
                self.fault("SCHEMA", "PAYLOAD_PARAMETER_AMBIGUOUS_ROW", path)
                return None
            row = rows[0] if rows else None
            doc, sel = (row or {}).get("document"), (row or {}).get("selector")
        else:
            row = None
        if row is None or sel is None:
            self.fault("SCHEMA", "PAYLOAD_ROW_UNREGISTERED", path, cls)
            return None
        if parent.get(sdf) != KIT.digest(doc):
            self.fault("JOIN", "PAYLOAD_SCHEMA_DIGEST_JOIN", path, cls)
            return None
        return doc, sel

    def fragment(self, ann, v, parent, path, cls):
        self.classes[cls] += 1
        loc = ann["locatedBy"]
        prog_hex = parent.get(loc["record"])
        b = self.cas.get(prog_hex) if isinstance(prog_hex, str) else None
        if b is None:
            self.fault("RETENTION", "FRAGMENT_OWNER_MISSING", path, loc["record"])
            return
        try:
            prog = K.parse_raw(b)
        except K.AdmissionError:
            self.fault("LEXICAL", "FRAGMENT_OWNER_NOT_CANONICAL", path)
            return
        rule = next((r for r in prog.get("rules", []) if isinstance(r, dict) and r.get("ruleId") == parent.get("ruleId")), None)
        node = rule.get("emitWhen") if rule else None
        addr = parent.get(loc["addressedBy"])
        parts = addr.split(".") if isinstance(addr, str) else []
        if not parts or parts[0] != "p":
            node = None
        for seg in parts[1:]:
            if node is None or not seg.isdigit():
                node = None
                break
            i = int(seg)
            if node.get("op") in ("and", "or") and i < len(node.get("operands", [])):
                node = node["operands"][i]
            elif node.get("op") == "not" and i == 0:
                node = node.get("operand")
            else:
                node = None
        if node is None:
            self.fault("JOIN", "FRAGMENT_UNLOCATED", path, str(addr))
            return
        r = KIT.admit(node, ann["record"]["document"], ann["record"]["selector"])
        if not r["ok"]:
            self.fault("SCHEMA", "FRAGMENT_RECORD_REFUSED", path)
            return
        if hashlib.sha256(K.C(node)).hexdigest() != v:
            self.fault("JOIN", "FRAGMENT_MISMATCH", path)
            return
        if parent.get("operation") is not None and node.get("op") != parent.get("operation"):
            self.fault("JOIN", "FRAGMENT_OPERATION_MISMATCH", path)

    # ------------------------------------------------------------------ domain-set registry joins
    def registry_joins(self, dom, value, rpath, ctx):
        set_name, row = SET_ROWS[dom]
        joined = []
        for j in row.get("closureJoins", []):
            for node in at_path(value, j["path"]):
                p = f"{rpath}.{'.'.join(j['path'])}"
                self.classes[f"registry:closureJoins:{j['form']}"] += 1
                got, val = self.resolve_frame(_hex_of(node), {"closure"}, p, f"registry:closureJoins:{j['form']}")
                if val is not None:
                    joined.append(_hex_of(node))
                    if val["kind"] != j["kind"]:
                        self.fault("JOIN", "CLOSURE_KIND_MISMATCH", p, f"{val['kind']}!={j['kind']}")
        if joined:
            # closure-tree-member annotations inside this record resolve against the closures its row joins
            for i, pend in enumerate(self.pending):
                if pend[0] == "tree-member" and pend[2].startswith(rpath + ".") and not pend[3]:
                    self.pending[i] = (pend[0], pend[1], pend[2], joined)
        for j in row.get("nestedIdentities", []):
            for node in at_path(value, j["path"]):
                if node is None:
                    continue
                p = f"{rpath}.{'.'.join(j['path'])}"
                self.resolve_frame(_hex_of(node), set(SETS[j["domainSet"]]), p, f"registry:nestedIdentities:{j['form']}")
        for j in row.get("nestedRecords", []):
            for node in at_path(value, j["path"]):
                if node is None:
                    continue
                p = f"{rpath}.{'.'.join(j['path'])}"
                rec = self.load_record(_hex_of(node), p, "registry:nestedRecords")
                if rec is not None and self.admit_record(_hex_of(node), rec, j["document"], j["selector"], p, {}):
                    for bj in j.get("blobJoins", []):
                        self.blob_joins(rec, bj, p, "registry:nestedRecords.blobJoins")
        for bj in row.get("blobJoins", []):
            self.blob_joins(value, bj, rpath, "registry:blobJoins")
        for sj in row.get("snapshotJoins", []):
            self.classes[f"registry:snapshotJoins:{sj['form']}"] += 1
            self.pending.append(("snapshot-join", sj, at_path(value, sj["path"]), f"{rpath}.{'.'.join(sj['path'])}"))
        if row.get("contextAgreementFields") or row.get("contextDomain"):
            self.pending.append(("context-agreement", row, value, rpath))

    def blob_joins(self, value, bj, rpath, cls):
        for node in at_path(value, bj["path"]):
            if not isinstance(node, dict):
                continue
            p = f"{rpath}.{'.'.join(bj['path'])}.{bj['digestField']}"
            ln = node.get(bj["lengthField"]) if bj.get("lengthField") else None
            self.raw(_hex_of(node.get(bj["digestField"])), p, cls, ln)

    # ------------------------------------------------------------------ driver
    def walk(self, run_id):
        if not isinstance(run_id, str) or not run_id.startswith("run3:"):
            self.fault("IDENTITY", "IDENTITY_PREFIX_NOT_CURRENT", "$run", str(run_id)[:16])
            return self.report(run_id)
        self.resolve_frame(_hex_of(run_id), {"run"}, "$run", "typed-prefix:run")
        while self.queue:
            v, doc, sel, path, ctx = self.queue.popleft()
            self.descend(v, doc, sel, path, ctx)
        self.post_pass(run_id)
        return self.report(run_id)

    def obj(self, ident):
        hx = _hex_of(ident)
        return self.frames.get(hx, (None, None))[1] if hx else None

    def post_pass(self, run_id):
        run = self.obj(run_id)
        plan = self.obj(run["planId"]) if run else None
        snapshot = self.obj(plan["snapshotId"]) if plan else None
        inventory = {r["path"]: r for r in snapshot["sourceInventory"]} if snapshot else None
        for pend in self.pending:
            kind = pend[0]
            if kind == "plan-join":
                _, fld, val, path = pend
                want = (run or {}).get("planId") if fld == "planId" else (plan or {}).get("snapshotId")
                self.classes[f"join:{fld}"] += 1
                if want is not None and val != want:
                    self.fault("JOIN", "PLAN_JOIN" if fld == "planId" else "SNAPSHOT_JOIN", path, val[:24])
            elif kind == "closure-direct":
                _, val, path, field = pend
                if plan is not None and val not in plan["semanticClosures"]:
                    self.fault("JOIN", "CLOSURE_MEMBERSHIP_DIRECT", path, field)
            elif kind == "import-selected":
                _, val, path = pend
                self.classes["closureMembership:selectedThroughOtherInput"] += 1
                if plan is not None and val not in plan["importIds"]:
                    self.fault("JOIN", "UNSELECTED_EVALUATION_IMPORT", path)
            elif kind == "view-fact-producer":
                _, view, path = pend
                for i, fid in enumerate(view["facts"]):
                    f = self.obj(fid)
                    self.classes["closureMembership:equalToDirect"] += 1
                    if f is not None and f["producerClosure"] != view["producerClosure"]:
                        self.fault("JOIN", "FACT_PRODUCER_VIEW_JOIN", f"{path}.facts[{i}]")
            elif kind == "seal-proof-evaluator":
                _, seal, path = pend
                proof = self.obj(seal["proofBundleId"])
                self.classes["closureMembership:equalToDirect"] += 1
                if proof is not None and proof["evaluatorClosure"] != seal["evaluatorClosure"]:
                    self.fault("JOIN", "PROOF_SEAL_EVALUATOR_JOIN", path)
            elif kind == "tree-member":
                _, hx, path, closures = pend
                trees = [self.frames.get(c, (None, None))[1] for c in closures if c]
                trees = [t for t in trees if t is not None]
                if not trees:
                    self.fault("JOIN", "TREE_MEMBER_CLOSURE_UNRESOLVED", path)
                    continue
                rows = [r for t in trees for r in t["tree"] if r["sha256"] == hx]
                if not rows:
                    self.fault("JOIN", "CLOSURE_TREE_MEMBER_ABSENT", path)
                else:
                    self.raw(hx, path, "raw-artifact/closure-tree-member", rows[0]["bytes"])
            elif kind == "capability-manifest-id":
                _, val, path = pend
                b = self.cas.get(plan["capabilityManifestBytesDigest"]) if plan else None
                if b is None:
                    self.fault("RETENTION", "DERIVED_SOURCE_MISSING", path)
                elif hashlib.sha256(CAP_MANIFEST_TAG + b).hexdigest() != val:
                    self.fault("JOIN", "DERIVED_MISMATCH", path, "capability-manifest-id")
            elif kind == "snapshot-path":
                _, val, path, fact_snapshot = pend
                snap = self.obj(fact_snapshot) if fact_snapshot else snapshot
                inv = {r["path"] for r in snap["sourceInventory"]} if snap else None
                if inv is None:
                    self.fault("JOIN", "SNAPSHOT_PATH_OWNER_UNRESOLVED", path)
                elif val not in inv:
                    self.fault("JOIN", "SNAPSHOT_PATH_NOT_INVENTORIED", path, val)
            elif kind == "snapshot-join":
                _, sj, nodes, path = pend
                if inventory is None:
                    continue
                for node in nodes:
                    if node is None:
                        continue
                    if sj["form"] == "inventoried-paths":
                        items = node if isinstance(node, list) else [node]
                        for it in items:
                            pth = it.get(sj.get("pathField", "path")) if isinstance(it, dict) else it
                            if pth not in inventory:
                                self.fault("JOIN", "SNAPSHOT_JOIN_PATH_NOT_INVENTORIED", path, str(pth))
                    elif sj["form"] == "inventoried-path-and-digest":
                        pth, dg = node.get(sj["pathField"]), node.get(sj["digestField"])
                        if pth not in inventory:
                            self.fault("JOIN", "SNAPSHOT_JOIN_PATH_NOT_INVENTORIED", path, str(pth))
                        elif inventory[pth]["sha256"] != dg:
                            self.fault("JOIN", "SNAPSHOT_JOIN_DIGEST_MISMATCH", path, str(pth))
            elif kind == "context-agreement":
                _, row, universe, path = pend
                ctx_val = universe.get(row["contextField"][0]) if row.get("contextField") else None
                hx = _hex_of(ctx_val)
                dom, ctx_rec = self.frames.get(hx, (None, None)) if hx else (None, None)
                self.classes["registry:contextAgreementFields"] += 1
                if ctx_rec is None:
                    self.fault("JOIN", "UNIVERSE_CONTEXT_UNRESOLVED", path)
                    continue
                if row.get("contextDomain") and dom != row["contextDomain"]:
                    self.fault("JOIN", "UNIVERSE_CONTEXT_LANGUAGE", path, f"{dom}!={row['contextDomain']}")
                for f in row.get("contextAgreementFields", []):
                    if universe.get(f) != ctx_rec.get(f):
                        self.fault("JOIN", "UNIVERSE_CONTEXT_AGREEMENT", path, f)

    def report(self, run_id):
        retained = set(self.cas)
        required = set(self.required)
        unreachable = sorted(retained - required)
        unreachable_frames = Counter()
        unreachable_semantic = []
        for hx in unreachable:
            dom, _, err = parse_frame(self.cas[hx])
            if not err:
                unreachable_frames[dom] += 1
                if dom in SEMANTIC_OUTPUT_DOMAINS or dom == "policy-derivation":
                    unreachable_semantic.append(f"{DOMAIN_PREFIX[dom]}:{hx}")
        reachable = {d: sorted(i for i, dd in self.typed.items() if dd == d) for d in sorted(set(self.typed.values()))}
        first = self.faults[0] if self.faults else None
        by_obligation = {}
        for f in self.faults:
            by_obligation.setdefault(f["obligation"], f)
        return {"runId": run_id, "result": "REFUSE" if self.faults else "ADMIT",
                "firstRefusal": first, "firstRefusalByObligation": by_obligation, "faults": self.faults,
                "maskedDescents": self.masked,
                "referenceClassesWalked": dict(sorted(self.classes.items())),
                "reachableDescriptors": reachable,
                "reachableSemanticOutputs": {d: reachable.get(d, []) for d in SEMANTIC_OUTPUT_DOMAINS},
                "requiredPreimages": len(required), "retainedPreimages": len(retained),
                "requiredButAbsent": sorted(required - retained),
                "unreachableRetained": {"count": len(unreachable), "framesByDomain": dict(sorted(unreachable_frames.items())),
                                        "semanticOutputs": unreachable_semantic,
                                        "standing": "not evaluation inputs and not authoritative outputs (identity closureMembership standing; composition 'Additional retained unreachable objects do not become authoritative findings')"},
                "exemptions": self.exemptions, "delegatedToOwner": self.delegated}


def close_retained_graph(exported):
    try:
        cas = load_cas(exported)
    except (ExportError, ValueError) as exc:
        return {"runId": exported.get("runId"), "result": "REFUSE",
                "firstRefusal": {"obligation": "IDENTITY", "code": str(exc).split(":")[0], "path": "$export", "detail": str(exc)},
                "faults": [], "referenceClassesWalked": {}}
    return Walker(cas).walk(exported.get("runId"))
