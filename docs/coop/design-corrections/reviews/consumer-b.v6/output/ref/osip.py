"""Blind consumer-B v6 disposable reference helper.

Written ONLY from the prose/schemas of the subject kit:
  - identity-and-evidence.md sec.3 (canonical encoding C, identity preimage H,
    closing digest law, payload registry, clones body frame)
  - resolved-inputs.v2.json#planIdContract.canonicalValueEncoding  (CVE1)
  - capability-manifest-domains.v2.json (ADM-TYPE/CLOSED/DOMAIN/ORDER gates)
  - relation-payload-schemas.v2.json#x-opensip-relation-registry (ladders,
    anchorLaw, snapshotJoins, coverageTotality)

No author reference model, fixture, golden or vector was read or copied.
"""
import hashlib, json, re, unicodedata, struct

# ---------------------------------------------------------------- C (codec)

_ESC = {'"': '\\"', "\\": "\\\\", "\b": "\\b", "\t": "\\t",
        "\n": "\\n", "\f": "\\f", "\r": "\\r"}


class Refuse(Exception):
    def __init__(self, code, detail=""):
        super().__init__(f"{code}{(':' + detail) if detail else ''}")
        self.code, self.detail = code, detail


def _cstr(s):
    if not isinstance(s, str):
        raise Refuse("C_TYPE", "not a string")
    out = ['"']
    for ch in s:
        cp = ord(ch)
        if 0xD800 <= cp <= 0xDFFF:                      # non-scalar Unicode
            raise Refuse("C_SURROGATE", hex(cp))
        if ch in _ESC:
            out.append(_ESC[ch])
        elif cp < 0x20:
            out.append("\\u%04x" % cp)                  # lowercase \u00xx
        else:
            out.append(ch)                              # incl. U+007F, U+2028
    out.append('"')
    return "".join(out)


INT_MIN, INT_MAX = -(2 ** 63), 2 ** 64 - 1


def C(x, depth=1):
    """Canonical bytes. Root container counts as depth 1; max depth 32."""
    if depth > 32:
        raise Refuse("C_DEPTH")
    if x is None:
        return b"null"
    if x is True:
        return b"true"
    if x is False:
        return b"false"
    if isinstance(x, int):                              # bool handled above
        if not (INT_MIN <= x <= INT_MAX):
            raise Refuse("C_INT_RANGE", str(x))
        return str(x).encode()                          # shortest decimal, no -0
    if isinstance(x, float):
        raise Refuse("C_FLOAT")
    if isinstance(x, str):
        return _cstr(x).encode("utf-8")
    if isinstance(x, list):
        return b"[" + b",".join(C(v, depth + 1) for v in x) + b"]"
    if isinstance(x, dict):
        keys = list(x.keys())
        for k in keys:
            if not isinstance(k, str):
                raise Refuse("C_KEY_TYPE")
        if len(set(keys)) != len(keys):
            raise Refuse("C_DUP_KEY")
        ordered = sorted(keys, key=lambda k: k.encode("utf-8"))   # UTF-8 byte order
        return (b"{" + b",".join(_cstr(k).encode("utf-8") + b":" + C(x[k], depth + 1)
                                 for k in ordered) + b"}")
    raise Refuse("C_TYPE", type(x).__name__)


PRODUCT_PREFIX = b"opensip.product.v1"


def frame(domain, x):
    c = C(x)
    return (PRODUCT_PREFIX + b"\x00" + domain.encode("ascii") + b"\x00"
            + struct.pack(">Q", len(c)) + c)


def H(domain, x):
    return hashlib.sha256(frame(domain, x)).hexdigest()


def ident(prefix, domain, x):
    return f"{prefix}:{H(domain, x)}"


def raw(x):
    """canonical-record digest: raw SHA-256 of C(record)."""
    return hashlib.sha256(C(x)).hexdigest()


def rawbytes(b):
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------- ordering annotations

def check_order(items, ann, what="array"):
    """Enforce the x-opensip-order vocabulary of identity sec.3."""
    if ann == "sequence":
        return True
    if ann == "canonical-set":
        ks = [C(i) for i in items]
    elif ann == "canonical-order":
        ks = [C(i) for i in items]
        for a, b in zip(ks, ks[1:]):
            if a > b:
                raise Refuse("ORDER", what)
        return True
    elif ann == "utf8":
        ks = [i.encode("utf-8") for i in items]
    elif ann == "path":
        ks = [i["path"].encode("utf-8") for i in items]
    elif ann == "numeric":
        ks = items
    elif ann == "ordinal":
        for n, i in enumerate(items):
            if i["ordinal"] != n:
                raise Refuse("ORDER", what)
        return True
    elif ann == "predicate":
        ks = [(i["ruleId"], i["subjectId"], i["predicateId"]) for i in items]
    elif isinstance(ann, dict) and "by" in ann:
        ks = [tuple(i[k] for k in ann["by"]) for i in items]
    else:
        raise Refuse("ORDER_ANNOTATION_UNKNOWN", str(ann))
    for a, b in zip(ks, ks[1:]):
        if not (a < b):
            raise Refuse("ORDER", what)
    return True


# --------------------------------------------------------------- CVE1 encoder

CVE1_MAX_NESTING = 64
CVE1_MAX_ITEMS = 1048576


def cve1(v, depth=1):
    if depth > CVE1_MAX_NESTING:
        raise Refuse("CVE1_DEPTH")
    if v is None:
        return b"\x00"
    if v is False:
        return b"\x01"
    if v is True:
        return b"\x02"
    if isinstance(v, int):
        if 0 <= v <= 2 ** 64 - 1:
            return b"\x03" + struct.pack(">Q", v)
        if -(2 ** 63) <= v < 0:
            return b"\x07" + struct.pack(">q", v)
        raise Refuse("CVE1_INT_RANGE", str(v))
    if isinstance(v, float):
        raise Refuse("CVE1_FLOAT")
    if isinstance(v, str):
        if unicodedata.normalize("NFC", v) != v:
            raise Refuse("CVE1_NOT_NFC", v)
        b = v.encode("utf-8")
        return b"\x04" + struct.pack(">I", len(b)) + b
    if isinstance(v, list):
        if len(v) > CVE1_MAX_ITEMS:
            raise Refuse("CVE1_ITEMS")
        return (b"\x05" + struct.pack(">I", len(v))
                + b"".join(cve1(e, depth + 1) for e in v))
    if isinstance(v, dict):
        ks = list(v.keys())
        if len(set(ks)) != len(ks):
            raise Refuse("CVE1_DUP_KEY")
        for k in ks:
            if not isinstance(k, str):
                raise Refuse("CVE1_KEY_TYPE")
            if unicodedata.normalize("NFC", k) != k:
                raise Refuse("CVE1_NOT_NFC", k)
        if len(ks) > CVE1_MAX_ITEMS:
            raise Refuse("CVE1_ITEMS")
        ordered = sorted(ks, key=lambda k: k.encode("utf-8"))
        out = b"\x06" + struct.pack(">I", len(ordered))
        for k in ordered:
            out += cve1(k, depth + 1) + cve1(v[k], depth + 1)
        return out
    raise Refuse("CVE1_TYPE", type(v).__name__)


CAP_DOMAIN = b"opensip.capability-manifest.v1"


def capability_manifest_id(committed_bytes):
    return hashlib.sha256(CAP_DOMAIN + b"\x00" + committed_bytes).hexdigest()


# -------------------------------------- capability-manifest admission (ADM-*)

class CapRegistry:
    """Effective ADM-DOMAIN registry, loaded from the SELECTED successor
    capability-manifest-domains.v2.json (identity sec.3 / native sec.11)."""

    def __init__(self, doc):
        self.doc = doc
        self.rec = doc["recordShape"]
        self.reg = doc["registries"]
        self.open_positions = set(doc["declaredOPEN"].keys())
        self.by_position = {}
        for name, r in self.reg.items():
            for pos in r["boundPositions"]:
                self.by_position[pos] = name
        self.relations = set(self.reg["RELATION-DOMAIN-V2"]["members"])
        self.ladders = self.reg["RELATION-LADDER-DOMAIN-V2"]["ladders"]
        self.platforms = set(self.reg["PLATFORM-ID-DOMAIN-V1"]["members"])
        self.deficiencies = set(self.reg["DEFICIENCY-DOMAIN-V1"]["members"])
        self.coverage_states = set(self.reg["COVERAGE-STATE-DOMAIN-V1"]["members"])

    # -- ADM-TYPE ---------------------------------------------------------
    @staticmethod
    def _exact_int(v):
        return isinstance(v, int) and not isinstance(v, bool)

    @staticmethod
    def _exact_str(v):
        return isinstance(v, str)

    def admit(self, m):
        """Run the four inherited gates in their inherited order, returning the
        COMPLETE violation list in the document's declared traversal order."""
        v = []
        self._type(m, v)
        if v:
            return v
        self._closed(m, v)
        if v:
            return v
        self._domain(m, v)
        if v:
            return v
        self._order(m, v)
        return v

    def _type(self, m, v):
        if not isinstance(m, dict):
            v.append(("ADM-TYPE", "$", "manifest is not an object"))
            return
        if "schemaVersion" in m and not self._exact_int(m["schemaVersion"]):
            v.append(("ADM-TYPE", "schemaVersion", repr(m["schemaVersion"])))
        for key in ("profile",):
            if key in m and not self._exact_str(m[key]):
                v.append(("ADM-TYPE", key, repr(m[key])))
        for i, p in enumerate(m.get("providers", []) or []):
            if not isinstance(p, dict):
                v.append(("ADM-TYPE", f"providers[{i}]", "not an object")); continue
            for key in ("providerId", "language", "providerVersionSource",
                        "toolchainIdentitySource"):
                if key in p and not self._exact_str(p[key]):
                    v.append(("ADM-TYPE", f"providers[{i}].{key}", repr(p[key])))
            rel = p.get("relations")
            if rel is not None and not isinstance(rel, dict):
                v.append(("ADM-TYPE", f"providers[{i}].relations", "not a map"))
            elif isinstance(rel, dict):
                for k, val in rel.items():
                    if not self._exact_str(val):
                        v.append(("ADM-TYPE", f"providers[{i}].relations[{k}]", repr(val)))
            pi = p.get("platformIds")
            if pi is not None and not isinstance(pi, list):
                v.append(("ADM-TYPE", f"providers[{i}].platformIds", "not an array"))
            elif isinstance(pi, list):
                for j, e in enumerate(pi):
                    if not self._exact_str(e):
                        v.append(("ADM-TYPE", f"providers[{i}].platformIds[{j}]", repr(e)))
        for i, a in enumerate(m.get("coverageForAbsent", []) or []):
            if not isinstance(a, dict):
                v.append(("ADM-TYPE", f"coverageForAbsent[{i}]", "not an object")); continue
            for key in ("providerId", "language", "coverageState", "deficiency"):
                if key in a and not self._exact_str(a[key]):
                    v.append(("ADM-TYPE", f"coverageForAbsent[{i}].{key}", repr(a[key])))
            ri = a.get("relationIds")
            if ri is not None and not isinstance(ri, list):
                v.append(("ADM-TYPE", f"coverageForAbsent[{i}].relationIds", "not an array"))
            elif isinstance(ri, list):
                for j, e in enumerate(ri):
                    if not self._exact_str(e):
                        v.append(("ADM-TYPE", f"coverageForAbsent[{i}].relationIds[{j}]", repr(e)))

    def _closed(self, m, v):
        def rec(obj, shape, where):
            need = set(self.rec[shape]["requiredKeys"])
            got = set(obj.keys())
            for k in sorted(need - got):
                v.append(("ADM-CLOSED", where, f"missing key {k}"))
            for k in sorted(got - need):
                v.append(("ADM-CLOSED", where, f"undeclared key {k}"))
        rec(m, "CapabilityManifestV1", "$")
        for i, p in enumerate(m.get("providers", []) or []):
            if isinstance(p, dict):
                rec(p, "ProviderCapability", f"providers[{i}]")
        for i, a in enumerate(m.get("coverageForAbsent", []) or []):
            if isinstance(a, dict):
                rec(a, "AbsentCapability", f"coverageForAbsent[{i}]")

    def _domain(self, m, v):
        for i, p in enumerate(m.get("providers", []) or []):
            if not isinstance(p, dict):
                continue
            for k, val in (p.get("relations") or {}).items():
                if k not in self.relations:
                    v.append(("ADM-DOMAIN", f"providers[{i}].relations key", k))
                    continue
                if val not in self.ladders.get(k, []):
                    v.append(("ADM-DOMAIN", f"providers[{i}].relations[{k}]", val))
            for j, e in enumerate(p.get("platformIds") or []):
                if e not in self.platforms:
                    v.append(("ADM-DOMAIN", f"providers[{i}].platformIds[{j}]", str(e)))
        for i, a in enumerate(m.get("coverageForAbsent", []) or []):
            if not isinstance(a, dict):
                continue
            for j, e in enumerate(a.get("relationIds") or []):
                if e not in self.relations:
                    v.append(("ADM-DOMAIN", f"coverageForAbsent[{i}].relationIds[{j}]", str(e)))
            if a.get("coverageState") not in self.coverage_states:
                v.append(("ADM-DOMAIN", f"coverageForAbsent[{i}].coverageState",
                          str(a.get("coverageState"))))
            if a.get("deficiency") not in self.deficiencies:
                v.append(("ADM-DOMAIN", f"coverageForAbsent[{i}].deficiency",
                          str(a.get("deficiency"))))

    @staticmethod
    def _asc(seq, key):
        ks = [key(x).encode("utf-8") for x in seq]
        return all(a < b for a, b in zip(ks, ks[1:]))

    def _order(self, m, v):
        # declared traversal order of the successor registry
        for i, p in enumerate(m.get("providers", []) or []):
            if isinstance(p, dict) and isinstance(p.get("platformIds"), list):
                if not self._asc(p["platformIds"], lambda s: s):
                    v.append(("ADM-ORDER", f"providers[{i}].platformIds", "not strictly ascending unique"))
        for i, a in enumerate(m.get("coverageForAbsent", []) or []):
            if isinstance(a, dict) and isinstance(a.get("relationIds"), list):
                if not self._asc(a["relationIds"], lambda s: s):
                    v.append(("ADM-ORDER", f"coverageForAbsent[{i}].relationIds", "not strictly ascending unique"))
        if isinstance(m.get("providers"), list):
            if not self._asc(m["providers"], lambda p: p["providerId"]):
                v.append(("ADM-ORDER", "providers", "not strictly ascending unique by providerId"))
        if isinstance(m.get("coverageForAbsent"), list):
            if not self._asc(m["coverageForAbsent"], lambda p: p["providerId"]):
                v.append(("ADM-ORDER", "coverageForAbsent", "not strictly ascending unique by providerId"))


# ------------------------------------------- FACT-IDENTITY body identity frame

FACT_IDENTITY_TAG = b"opensip.fact-identity.v1"


def _u8c(b):
    if len(b) > 255:
        raise Refuse("BODY_FRAME_COMPONENT_TOO_LONG", str(len(b)))
    return bytes([len(b)]) + b


def body_frame(level_id, level_version_raw32, language_id, language_version_raw32,
               payload):
    """identity sec.3 'clones' frame. levelVersion/languageVersion are the RAW
    32 digest bytes, never hex text. Outer component is u32be len || payload."""
    assert len(level_version_raw32) == 32 and len(language_version_raw32) == 32
    return (_u8c(FACT_IDENTITY_TAG)
            + _u8c(level_id.encode("utf-8"))
            + _u8c(level_version_raw32)
            + _u8c(language_id.encode("utf-8"))
            + _u8c(language_version_raw32)
            + struct.pack(">I", len(payload)) + payload)


def l0_payload(span_bytes):
    """L0-verbatim payload is ITSELF length-prefixed: u32be raw_byte_len||bytes."""
    return struct.pack(">I", len(span_bytes)) + span_bytes


def token_stream_payload(tokens):
    """L1-L3: u32be token_count || (u16be kind_len||kind || u32be val_len||val)*"""
    out = struct.pack(">I", len(tokens))
    for kind, val in tokens:
        kb, vb = kind.encode("utf-8"), val.encode("utf-8")
        out += struct.pack(">H", len(kb)) + kb + struct.pack(">I", len(vb)) + vb
    return out


def body_identity(level_id, level_version_hex, language_id, blv_record, payload):
    lv = bytes.fromhex(level_version_hex)
    langv = hashlib.sha256(C(blv_record)).digest()
    fr = body_frame(level_id, lv, language_id, langv, payload)
    return "sha256:" + hashlib.sha256(fr).hexdigest(), fr


# ------------------------------------------------------- dialect / language id

def longest_suffix(table, path):
    best = None
    for suf in table:
        if path.endswith(suf) and (best is None or len(suf) > len(best)):
            best = suf
    return best
