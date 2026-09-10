"""Blind consumer-B v7 independent reference helpers for OpenSIP DR-011-R10.

Written from the normative prose in the input kit only.  No author reference
implementation was read (foundation/canonical.py, identity-model.py,
native_evidence_model.v2.py, workflows_model.v1.py and the checkers are NOT in
the kit and were not consulted).

Sources for each construct, by exact selector:

  C (canonical JSON)   docs/v2/contracts/product-v1/identity-and-evidence.md S3
  exact typed parse    identity-and-evidence.md S3 + admission-and-qualification.md S1
  H(D,X)               identity-and-evidence.md S3
  H frame retention    identity-and-evidence.md S3 "the closing digest law"
  CVE1                 docs/coop/artifacts/resolved-inputs.v2.json
                         #planIdContract.canonicalValueEncoding
  CAP-MANIFEST-ID-V1   docs/coop/artifacts/delivery.v4.json
                         #derivedFrom.operations[17].value.recipe
                       + docs/coop/design-corrections/native/
                         capability-manifest-domains.v2.json  (effective ADM-DOMAIN
                         registry, selected by identity-and-evidence S3)
  body identity frame  docs/coop/artifacts/fact-identity-policy.v2.json
                         #canonicalisationSchema.byteGrammar
                       + identity-and-evidence.md S3 "clones: the inherited body
                         recipe" (which of the two grammatically available L0
                         readings is admitted)
"""

import hashlib
import json
import os
import re
import unicodedata

SUBJECT = os.environ.get(
    "OPENSIP_SUBJECT",
    "/tmp/opensip-design-corrections/consumer-b.v7/subject",
)

# ---------------------------------------------------------------------------
# 1. Exact typed admission of RAW INPUT BYTES (lexical, before json.loads)
# ---------------------------------------------------------------------------
# identity-and-evidence S3: "Before deserialization loses lexical information,
# reject duplicate keys, floating/exponent tokens, -0, nonfinite tokens,
# malformed UTF-8 and non-scalar Unicode. Integer range is [-2^63, 2^64-1] ...
# Maximum descriptor is 4 MiB and nesting depth 32: the root container counts
# as 1; scalar leaves and object keys add no container depth."
# admission-and-qualification S1: "1.0, 1e0, 1E0, ... booleans and numeric
# strings do not satisfy an integer field ... -0, nonfinite tokens ... rejected."

MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32


class Refused(Exception):
    def __init__(self, code, detail=""):
        super().__init__(code + ((": " + detail) if detail else ""))
        self.code = code
        self.detail = detail


_INT_RE = re.compile(r"-?(?:0|[1-9][0-9]*)$")

INT_MIN = -(2 ** 63)
INT_MAX = 2 ** 64 - 1


class _Scanner:
    """Minimal strict JSON scanner.  Only what the contract admits."""

    def __init__(self, text):
        self.s = text
        self.i = 0
        self.n = len(text)

    def err(self, code, d=""):
        raise Refused(code, d + " at offset %d" % self.i)

    def ws(self):
        while self.i < self.n and self.s[self.i] in " \t\n\r":
            self.i += 1

    def parse(self):
        self.ws()
        v = self.value(1)
        self.ws()
        if self.i != self.n:
            self.err("LEX_TRAILING_BYTES")
        return v

    def value(self, depth):
        if self.i >= self.n:
            self.err("LEX_EOF")
        c = self.s[self.i]
        if c == "{":
            return self.obj(depth)
        if c == "[":
            return self.arr(depth)
        if c == '"':
            return self.string()
        if c == "t":
            return self.lit("true", True)
        if c == "f":
            return self.lit("false", False)
        if c == "n":
            return self.lit("null", None)
        if c == "-" or c.isdigit():
            return self.number()
        # NaN / Infinity / -Infinity
        self.err("LEX_BAD_TOKEN", repr(self.s[self.i:self.i + 12]))

    def lit(self, word, val):
        if self.s[self.i:self.i + len(word)] != word:
            self.err("LEX_BAD_TOKEN")
        self.i += len(word)
        return val

    def number(self):
        j = self.i
        while self.i < self.n and self.s[self.i] not in ",]} \t\n\r":
            self.i += 1
        tok = self.s[j:self.i]
        if tok in ("NaN", "Infinity", "-Infinity"):
            raise Refused("LEX_NONFINITE", tok)
        if not _INT_RE.match(tok):
            # 1.0, 1e0, 1E0, 1.0000000000000001, 9007199254740991.1 ...
            raise Refused("LEX_NOT_AN_INTEGER_TOKEN", tok)
        if tok == "-0":
            raise Refused("LEX_NEGATIVE_ZERO", tok)
        v = int(tok)
        if v < INT_MIN or v > INT_MAX:
            raise Refused("LEX_INTEGER_RANGE", tok)
        return v

    def string(self):
        assert self.s[self.i] == '"'
        self.i += 1
        out = []
        while True:
            if self.i >= self.n:
                self.err("LEX_EOF_IN_STRING")
            c = self.s[self.i]
            if c == '"':
                self.i += 1
                return "".join(out)
            if c == "\\":
                self.i += 1
                if self.i >= self.n:
                    self.err("LEX_EOF_IN_ESCAPE")
                e = self.s[self.i]
                self.i += 1
                simple = {'"': '"', "\\": "\\", "/": "/", "b": "\b",
                          "f": "\f", "n": "\n", "r": "\r", "t": "\t"}
                if e in simple:
                    out.append(simple[e])
                elif e == "u":
                    hx = self.s[self.i:self.i + 4]
                    if len(hx) != 4 or any(ch not in "0123456789abcdefABCDEF" for ch in hx):
                        self.err("LEX_BAD_UNICODE_ESCAPE")
                    self.i += 4
                    cp = int(hx, 16)
                    if 0xD800 <= cp <= 0xDBFF:
                        if self.s[self.i:self.i + 2] != "\\u":
                            raise Refused("LEX_LONE_SURROGATE", hx)
                        hx2 = self.s[self.i + 2:self.i + 6]
                        if len(hx2) != 4:
                            self.err("LEX_BAD_UNICODE_ESCAPE")
                        lo = int(hx2, 16)
                        if not (0xDC00 <= lo <= 0xDFFF):
                            raise Refused("LEX_LONE_SURROGATE", hx)
                        self.i += 6
                        cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00)
                    elif 0xDC00 <= cp <= 0xDFFF:
                        raise Refused("LEX_LONE_SURROGATE", hx)
                    out.append(chr(cp))
                else:
                    self.err("LEX_BAD_ESCAPE", e)
            else:
                if ord(c) < 0x20:
                    raise Refused("LEX_RAW_CONTROL", hex(ord(c)))
                out.append(c)
                self.i += 1

    def obj(self, depth):
        if depth > MAX_DEPTH:
            raise Refused("LEX_DEPTH", str(depth))
        self.i += 1
        out = {}
        self.ws()
        if self.i < self.n and self.s[self.i] == "}":
            self.i += 1
            return out
        while True:
            self.ws()
            if self.i >= self.n or self.s[self.i] != '"':
                self.err("LEX_OBJECT_KEY")
            k = self.string()
            if k in out:
                raise Refused("LEX_DUPLICATE_KEY", k)
            self.ws()
            if self.i >= self.n or self.s[self.i] != ":":
                self.err("LEX_EXPECTED_COLON")
            self.i += 1
            self.ws()
            out[k] = self.value(depth + 1)
            self.ws()
            if self.i < self.n and self.s[self.i] == ",":
                self.i += 1
                continue
            if self.i < self.n and self.s[self.i] == "}":
                self.i += 1
                return out
            self.err("LEX_EXPECTED_COMMA_OR_BRACE")

    def arr(self, depth):
        if depth > MAX_DEPTH:
            raise Refused("LEX_DEPTH", str(depth))
        self.i += 1
        out = []
        self.ws()
        if self.i < self.n and self.s[self.i] == "]":
            self.i += 1
            return out
        while True:
            self.ws()
            out.append(self.value(depth + 1))
            self.ws()
            if self.i < self.n and self.s[self.i] == ",":
                self.i += 1
                continue
            if self.i < self.n and self.s[self.i] == "]":
                self.i += 1
                return out
            self.err("LEX_EXPECTED_COMMA_OR_BRACKET")


def parse_exact(raw):
    """Admit raw descriptor BYTES.  Returns the decoded value or raises Refused."""
    if not isinstance(raw, (bytes, bytearray)):
        raise TypeError("parse_exact takes bytes; use it for raw-input admission")
    if len(raw) > MAX_DESCRIPTOR_BYTES:
        raise Refused("LEX_SIZE", str(len(raw)))
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise Refused("LEX_MALFORMED_UTF8", str(e))
    return _Scanner(text).parse()


# ---------------------------------------------------------------------------
# 2. C -- the canonical encoder (identity-and-evidence S3)
# ---------------------------------------------------------------------------
# "Canonical JSON has UTF-8 byte-ordered keys, no whitespace or trailing
#  newline, no Unicode normalization, shortest ordinary decimal integers, and
#  unescaped Unicode scalar characters. Escape quote and backslash, use
#  \b\t\n\f\r, and lowercase \u00xx for other U+0000-001F controls; do not
#  escape slash. Arrays are encoded in their admitted order: C never sorts,
#  deduplicates or infers semantics."
# "U+007F and U+2028 remain unescaped."

_C_ESCAPES = {0x22: '\\"', 0x5C: "\\\\", 0x08: "\\b", 0x09: "\\t",
              0x0A: "\\n", 0x0C: "\\f", 0x0D: "\\r"}


def _c_string(s):
    out = ['"']
    for ch in s:
        o = ord(ch)
        if o in _C_ESCAPES:
            out.append(_C_ESCAPES[o])
        elif o < 0x20:
            out.append("\\u%04x" % o)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _c(v, depth=1):
    if depth > MAX_DEPTH:
        raise Refused("C_DEPTH", str(depth))
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if type(v) is int:
        if v < INT_MIN or v > INT_MAX:
            raise Refused("C_INTEGER_RANGE", str(v))
        return str(v)          # shortest ordinary decimal
    if type(v) is float:
        raise Refused("C_FLOAT_FORBIDDEN", repr(v))
    if type(v) is str:
        return _c_string(v)
    if type(v) is list:
        return "[" + ",".join(_c(x, depth + 1) for x in v) + "]"
    if type(v) is dict:
        items = []
        seen = set()
        for k in v:
            if type(k) is not str:
                raise Refused("C_NON_STRING_KEY", repr(k))
            kb = k.encode("utf-8")
            if kb in seen:
                raise Refused("C_DUPLICATE_KEY", k)
            seen.add(kb)
            items.append((kb, k))
        items.sort(key=lambda t: t[0])          # UTF-8 byte order
        return "{" + ",".join(
            _c_string(k) + ":" + _c(v[k], depth + 1) for _, k in items) + "}"
    raise Refused("C_UNSUPPORTED_TYPE", type(v).__name__)


def C(value):
    """Canonical bytes of a descriptor."""
    b = _c(value).encode("utf-8")
    if len(b) > MAX_DESCRIPTOR_BYTES:
        raise Refused("C_SIZE", str(len(b)))
    return b


def sha256hex(b):
    return hashlib.sha256(b).hexdigest()


def raw_digest(record):
    """canonical-record representation: raw SHA-256 of C(record)."""
    return sha256hex(C(record))


# ---------------------------------------------------------------------------
# 3. H(D, X) and the retained H preimage frame
# ---------------------------------------------------------------------------
# H(D,X) = SHA256(ASCII("opensip.product.v1") || 00 || ASCII(D) || 00
#                 || uint64BE(length(C(X))) || C(X))

H_PREFIX = b"opensip.product.v1"


def h_frame(domain, descriptor):
    cx = C(descriptor)
    return (H_PREFIX + b"\x00" + domain.encode("ascii") + b"\x00"
            + len(cx).to_bytes(8, "big") + cx)


def H(domain, descriptor):
    return sha256hex(h_frame(domain, descriptor))


def parse_h_frame(frame):
    """Exact frame admission (identity-and-evidence S3 closing digest law)."""
    if not frame.startswith(H_PREFIX + b"\x00"):
        raise Refused("FRAME_PREFIX")
    rest = frame[len(H_PREFIX) + 1:]
    nul = rest.find(b"\x00")
    if nul < 0:
        raise Refused("FRAME_DOMAIN_TERMINATOR")
    domain = rest[:nul].decode("ascii")
    body = rest[nul + 1:]
    if len(body) < 8:
        raise Refused("FRAME_LENGTH_FIELD")
    declared = int.from_bytes(body[:8], "big")
    payload = body[8:]
    if declared != len(payload):
        raise Refused("FRAME_LENGTH_MISMATCH", "%d!=%d" % (declared, len(payload)))
    value = parse_exact(payload)
    if C(value) != payload:
        raise Refused("FRAME_NOT_CANONICAL")
    return domain, value


IDENTITY_PREFIX = {
    "snapshot": "snapshot2", "closure": "closure2", "import": "import2",
    "plan": "plan2", "subject-scope": "scope2", "fact": "fact2",
    "coverage": "coverage2", "view": "view2", "execution-plan": "exec-plan2",
    "finding-fingerprint": "finding-key2", "finding": "finding2",
    "proof-bundle": "proof2", "semantic-evidence": "evidence2",
    "evaluation-seal": "seal2", "run": "run2", "cache-key": "cache2",
    "regeneration-key": "regen2", "policy-derivation": "policy-derivation2",
}


def identity(domain, descriptor):
    return IDENTITY_PREFIX[domain] + ":" + H(domain, descriptor)


# ---------------------------------------------------------------------------
# 4. CVE1 and CAP-MANIFEST-ID-V1
# ---------------------------------------------------------------------------
# resolved-inputs.v2#planIdContract.canonicalValueEncoding, eight closed types.

CVE1_MAX_NESTING = 64          # capability-manifest-domains.v2 decoderBounds
CVE1_MAX_ITEMS = 1048576


def _u32be(n):
    if n < 0 or n > 0xFFFFFFFF:
        raise Refused("CVE1_U32_RANGE", str(n))
    return n.to_bytes(4, "big")


def cve1(value, depth=1):
    if depth > CVE1_MAX_NESTING:
        raise Refused("CVE1_DEPTH", str(depth))
    if value is None:
        return b"\x00"
    if value is False:
        return b"\x01"
    if value is True:
        return b"\x02"
    if type(value) is int:
        if 0 <= value <= 2 ** 64 - 1:
            return b"\x03" + value.to_bytes(8, "big")
        if -(2 ** 63) <= value < 0:
            return b"\x07" + (value & (2 ** 64 - 1)).to_bytes(8, "big")
        raise Refused("CVE1_INTEGER_RANGE", str(value))
    if type(value) is float:
        raise Refused("CVE1_FLOAT_FORBIDDEN", repr(value))
    if type(value) is str:
        if unicodedata.normalize("NFC", value) != value:
            raise Refused("CVE1_NOT_NFC", value)
        b = value.encode("utf-8")
        return b"\x04" + _u32be(len(b)) + b
    if type(value) is list:
        if len(value) > CVE1_MAX_ITEMS:
            raise Refused("CVE1_TOO_MANY_ITEMS", str(len(value)))
        return b"\x05" + _u32be(len(value)) + b"".join(
            cve1(e, depth + 1) for e in value)
    if type(value) is dict:
        if len(value) > CVE1_MAX_ITEMS:
            raise Refused("CVE1_TOO_MANY_ITEMS", str(len(value)))
        keys = []
        seen = set()
        for k in value:
            if type(k) is not str:
                raise Refused("CVE1_NON_STRING_KEY", repr(k))
            if unicodedata.normalize("NFC", k) != k:
                raise Refused("CVE1_NOT_NFC", k)
            kb = k.encode("utf-8")
            if kb in seen:
                raise Refused("CVE1_DUPLICATE_KEY", k)
            seen.add(kb)
            keys.append((kb, k))
        keys.sort(key=lambda t: t[0])
        out = [b"\x06", _u32be(len(keys))]
        for kb, k in keys:
            out.append(cve1(k, depth + 1))
            out.append(cve1(value[k], depth + 1))
        return b"".join(out)
    raise Refused("CVE1_UNSUPPORTED_TYPE", type(value).__name__)


def cve1_decode(buf):
    """Independent decoder, used only for the decode(encode(x))==x property."""
    val, off = _cve1_dec(buf, 0, 1)
    if off != len(buf):
        raise Refused("CVE1_TRAILING_BYTES")
    return val


def _cve1_dec(b, i, depth):
    if depth > CVE1_MAX_NESTING:
        raise Refused("CVE1_DEPTH")
    if i >= len(b):
        raise Refused("CVE1_EOF")
    t = b[i]
    i += 1
    if t == 0x00:
        return None, i
    if t == 0x01:
        return False, i
    if t == 0x02:
        return True, i
    if t == 0x03:
        return int.from_bytes(b[i:i + 8], "big"), i + 8
    if t == 0x07:
        v = int.from_bytes(b[i:i + 8], "big")
        return v - 2 ** 64, i + 8
    if t == 0x04:
        n = int.from_bytes(b[i:i + 4], "big")
        i += 4
        s = b[i:i + n].decode("utf-8")
        if unicodedata.normalize("NFC", s) != s:
            raise Refused("CVE1_NOT_NFC", s)
        return s, i + n
    if t == 0x05:
        n = int.from_bytes(b[i:i + 4], "big")
        i += 4
        out = []
        for _ in range(n):
            v, i = _cve1_dec(b, i, depth + 1)
            out.append(v)
        return out, i
    if t == 0x06:
        n = int.from_bytes(b[i:i + 4], "big")
        i += 4
        out = {}
        prev = None
        for _ in range(n):
            k, i = _cve1_dec(b, i, depth + 1)
            if type(k) is not str:
                raise Refused("CVE1_NON_STRING_KEY")
            kb = k.encode("utf-8")
            if prev is not None and kb <= prev:
                raise Refused("CVE1_MAP_KEYS_UNSORTED", k)
            prev = kb
            v, i = _cve1_dec(b, i, depth + 1)
            out[k] = v
        return out, i
    raise Refused("CVE1_UNKNOWN_TAG", hex(t))


CAP_MANIFEST_DOMAIN = b"opensip.capability-manifest.v1"


def capability_manifest_id(committed_bytes):
    return sha256hex(CAP_MANIFEST_DOMAIN + b"\x00" + committed_bytes)


# --- the four inherited admission gates, in the inherited order --------------
# delivery.v4 #derivedFrom.operations[17].value.admission
# effective registry: native/capability-manifest-domains.v2.json

_CMD = None


def cm_domains():
    global _CMD
    if _CMD is None:
        with open(os.path.join(
                SUBJECT, "docs/coop/design-corrections/native/"
                         "capability-manifest-domains.v2.json"), "rb") as f:
            _CMD = parse_exact(f.read())
    return _CMD


RECORD_KEYS = {
    "CapabilityManifestV1": ["schemaVersion", "profile", "providers",
                             "coverageForAbsent"],
    "ProviderCapability": ["providerId", "language", "providerVersionSource",
                           "toolchainIdentitySource", "relations",
                           "platformIds"],
    "AbsentCapability": ["providerId", "language", "relationIds",
                         "coverageState", "deficiency"],
}

# The declared sort keys (delivery.v4 op 8, declaredSortKeys) and the declared
# ADM-ORDER traversal order (capability-manifest-domains.v2 traversalOrder).
SORT_KEYS = {
    "CapabilityManifestV1.providers": "providerId",
    "CapabilityManifestV1.coverageForAbsent": "providerId",
    "ProviderCapability.platformIds": None,      # the element string
    "AbsentCapability.relationIds": None,
}


def admit_capability_manifest(m):
    """Run ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER in the inherited order.

    Returns the complete violation list in the declared traversal order (empty
    list == admitted).  Nothing is normalised, sorted or coerced.
    """
    reg = cm_domains()["registries"]
    rel_dom = set(reg["RELATION-DOMAIN-V2"]["members"])
    ladders = reg["RELATION-LADDER-DOMAIN-V2"]["ladders"]
    plat = set(reg["PLATFORM-ID-DOMAIN-V1"]["members"])
    defic = set(reg["DEFICIENCY-DOMAIN-V1"]["members"])
    cov = set(reg["COVERAGE-STATE-DOMAIN-V1"]["members"])
    v = []

    def is_str(x):
        return type(x) is str

    # ---- ADM-TYPE (exact JSON type, before any content comparison) ----
    if type(m) is not dict:
        return ["ADM-TYPE:CapabilityManifestV1 is not an object"]
    if "schemaVersion" in m and type(m["schemaVersion"]) is not int:
        v.append("ADM-TYPE:CapabilityManifestV1.schemaVersion is not an integer")
    for name in ("profile",):
        if name in m and not is_str(m[name]):
            v.append("ADM-TYPE:CapabilityManifestV1.%s is not a string" % name)
    for arr in ("providers", "coverageForAbsent"):
        if arr in m and type(m[arr]) is not list:
            v.append("ADM-TYPE:CapabilityManifestV1.%s is not an array" % arr)
    for i, p in enumerate(m.get("providers", []) if type(m.get("providers")) is list else []):
        if type(p) is not dict:
            v.append("ADM-TYPE:providers[%d] is not an object" % i)
            continue
        for name in ("providerId", "language", "providerVersionSource",
                     "toolchainIdentitySource"):
            if name in p and not is_str(p[name]):
                v.append("ADM-TYPE:providers[%d].%s is not a string" % (i, name))
        if "relations" in p and type(p["relations"]) is not dict:
            v.append("ADM-TYPE:providers[%d].relations is not an object" % i)
        elif "relations" in p:
            for k, val in p["relations"].items():
                if not is_str(val):
                    v.append("ADM-TYPE:providers[%d].relations[%s] is not a string" % (i, k))
        if "platformIds" in p and type(p["platformIds"]) is not list:
            v.append("ADM-TYPE:providers[%d].platformIds is not an array" % i)
        elif "platformIds" in p:
            for j, x in enumerate(p["platformIds"]):
                if not is_str(x):
                    v.append("ADM-TYPE:providers[%d].platformIds[%d] is not a string" % (i, j))
    for i, a in enumerate(m.get("coverageForAbsent", []) if type(m.get("coverageForAbsent")) is list else []):
        if type(a) is not dict:
            v.append("ADM-TYPE:coverageForAbsent[%d] is not an object" % i)
            continue
        for name in ("providerId", "language", "coverageState", "deficiency"):
            if name in a and not is_str(a[name]):
                v.append("ADM-TYPE:coverageForAbsent[%d].%s is not a string" % (i, name))
        if "relationIds" in a and type(a["relationIds"]) is not list:
            v.append("ADM-TYPE:coverageForAbsent[%d].relationIds is not an array" % i)
        elif "relationIds" in a:
            for j, x in enumerate(a["relationIds"]):
                if not is_str(x):
                    v.append("ADM-TYPE:coverageForAbsent[%d].relationIds[%d] is not a string" % (i, j))
    if v:
        return v

    # ---- ADM-CLOSED (record key sets exact; a map is not a record) ----
    def closed(obj, rec, label):
        want = set(RECORD_KEYS[rec])
        have = set(obj.keys())
        for k in sorted(have - want):
            v.append("ADM-CLOSED:%s undeclared key %s" % (label, k))
        for k in sorted(want - have):
            v.append("ADM-CLOSED:%s missing key %s" % (label, k))

    closed(m, "CapabilityManifestV1", "CapabilityManifestV1")
    for i, p in enumerate(m["providers"]):
        closed(p, "ProviderCapability", "providers[%d]" % i)
    for i, a in enumerate(m["coverageForAbsent"]):
        closed(a, "AbsentCapability", "coverageForAbsent[%d]" % i)
    if v:
        return v

    # ---- ADM-DOMAIN (registry membership, exact NFC UTF-8 bytes) ----
    for i, p in enumerate(m["providers"]):
        for k in p["relations"]:
            if k not in rel_dom:
                v.append("ADM-DOMAIN:providers[%d].relations key %r not in "
                         "RELATION-DOMAIN-V2" % (i, k))
            elif p["relations"][k] not in ladders[k]:
                v.append("ADM-DOMAIN:providers[%d].relations[%s] value %r is not a "
                         "rung of that relation's ladder" % (i, k, p["relations"][k]))
        for x in p["platformIds"]:
            if x not in plat:
                v.append("ADM-DOMAIN:providers[%d].platformIds %r not in "
                         "PLATFORM-ID-DOMAIN-V1" % (i, x))
    for i, a in enumerate(m["coverageForAbsent"]):
        for x in a["relationIds"]:
            if x not in rel_dom:
                v.append("ADM-DOMAIN:coverageForAbsent[%d].relationIds %r not in "
                         "RELATION-DOMAIN-V2" % (i, x))
        if a["coverageState"] not in cov:
            v.append("ADM-DOMAIN:coverageForAbsent[%d].coverageState %r not in "
                     "COVERAGE-STATE-DOMAIN-V1" % (i, a["coverageState"]))
        if a["deficiency"] not in defic:
            v.append("ADM-DOMAIN:coverageForAbsent[%d].deficiency %r not in "
                     "DEFICIENCY-DOMAIN-V1" % (i, a["deficiency"]))
    if v:
        return v

    # ---- ADM-ORDER, in the DECLARED traversal order ----
    def ascending(seq, key, label):
        prev = None
        for x in seq:
            b = (x if key is None else x[key]).encode("utf-8")
            if prev is not None and b <= prev:
                v.append("ADM-ORDER:%s not strictly ascending at %r" %
                         (label, x if key is None else x[key]))
            prev = b

    for i, p in enumerate(m["providers"]):
        ascending(p["platformIds"], None, "providers[%d].platformIds" % i)
    for i, a in enumerate(m["coverageForAbsent"]):
        ascending(a["relationIds"], None, "coverageForAbsent[%d].relationIds" % i)
    ascending(m["providers"], "providerId", "providers")
    ascending(m["coverageForAbsent"], "providerId", "coverageForAbsent")
    return v


# ---------------------------------------------------------------------------
# 5. FACT-IDENTITY body frame (fact-identity-policy.v2 byteGrammar +
#    identity-and-evidence S3 "clones" paragraph)
# ---------------------------------------------------------------------------
FACT_IDENTITY_DOMAIN_TAG = b"opensip.fact-identity.v1"


def _u8len(b):
    if len(b) > 255:
        raise Refused("BODY_FRAME_COMPONENT_TOO_LONG", str(len(b)))
    return bytes([len(b)]) + b


def body_payload_L0(span_bytes):
    """L0-verbatim: u32be raw_byte_len || exact body-span bytes."""
    return len(span_bytes).to_bytes(4, "big") + span_bytes


def body_payload_tokens(tokens):
    """L1-L3 framedTokenStream: u32be count || (u16be klen||k||u32be vlen||v)*"""
    out = [len(tokens).to_bytes(4, "big")]
    for kind, value in tokens:
        kb = kind.encode("utf-8")
        vb = value if isinstance(value, bytes) else value.encode("utf-8")
        out.append(len(kb).to_bytes(2, "big") + kb
                   + len(vb).to_bytes(4, "big") + vb)
    return b"".join(out)


def body_identity_frame(level_id, level_version_raw32, language_id,
                        language_version_raw32, payload):
    """Fully framed, domain-separated preimage.

    identity-and-evidence S3 fixes the reading: the trailing component is
    `u32be len || payload`, and at L0 the payload is ITSELF length-prefixed, so
    payload_len == raw_byte_len + 4.
    """
    assert len(level_version_raw32) == 32
    assert len(language_version_raw32) == 32
    return (_u8len(FACT_IDENTITY_DOMAIN_TAG)
            + _u8len(level_id.encode("ascii"))
            + _u8len(level_version_raw32)
            + _u8len(language_id.encode("ascii"))
            + _u8len(language_version_raw32)
            + len(payload).to_bytes(4, "big") + payload)


def body_identity(level_id, level_version_raw32, language_id,
                  language_version_raw32, payload):
    fr = body_identity_frame(level_id, level_version_raw32, language_id,
                             language_version_raw32, payload)
    return "sha256:" + sha256hex(fr), fr


# ---------------------------------------------------------------------------
# 6. Schema access + validation through the pinned local closure
# ---------------------------------------------------------------------------
import jsonschema                                            # noqa: E402
from referencing import Registry, Resource                   # noqa: E402
from referencing.jsonschema import DRAFT202012               # noqa: E402

DOCS = {
    "identity": "docs/coop/design-corrections/foundation/identity-schemas.v2.json",
    "relation": "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
    "native": "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "matrix": "docs/coop/design-corrections/native/native-capability-matrix.v2.json",
    "capdomains": "docs/coop/design-corrections/native/capability-manifest-domains.v2.json",
    "product-config": "docs/coop/design-corrections/foundation/product-configuration.schema.v2.json",
    "import-source-context": "docs/coop/design-corrections/foundation/import-source-context.schema.json",
    "common": "docs/coop/design-corrections/workflows/schemas/common.schema.json",
    "policy-document": "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
    "imported-evidence": "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
    "invocation-record": "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json",
    "command-envelope": "docs/coop/design-corrections/workflows/schemas/command-envelope.schema.json",
    "command-inventory-schema": "docs/coop/design-corrections/workflows/schemas/command-inventory.schema.json",
    "command-inventory": "docs/coop/design-corrections/workflows/command-inventory.v1.json",
    "comparison-result": "docs/coop/design-corrections/workflows/schemas/comparison-result.schema.json",
    "repair": "docs/coop/design-corrections/workflows/schemas/repair.schema.json",
    "baseline-artifact": "docs/coop/design-corrections/workflows/schemas/baseline-artifact.schema.json",
    "test-execution": "docs/coop/design-corrections/workflows/schemas/test-execution.schema.json",
    "policy-test": "docs/coop/design-corrections/workflows/schemas/policy-test.schema.json",
    "graph-query": "docs/coop/design-corrections/workflows/schemas/graph-query.schema.json",
    "review": "docs/coop/design-corrections/workflows/schemas/review.schema.json",
    "public-detail-registry": "docs/coop/design-corrections/public-detail-registry.v1.json",
    "security": "docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json",
    "d9": "docs/coop/artifacts/d9-exit-contract.v1.14.json",
    "resolved-inputs": "docs/coop/artifacts/resolved-inputs.v2.json",
    "delivery": "docs/coop/artifacts/delivery.v4.json",
    "fact-identity": "docs/coop/artifacts/fact-identity-policy.v2.json",
    "fact-plane": "docs/coop/artifacts/fact-plane.v1.json",
    "permission-truth": "docs/coop/artifacts/permission-truth-tables.v9.json",
}

_raw_cache = {}
_doc_cache = {}


def doc_bytes(name):
    if name not in _raw_cache:
        with open(os.path.join(SUBJECT, DOCS[name]), "rb") as f:
            _raw_cache[name] = f.read()
    return _raw_cache[name]


def doc(name):
    if name not in _doc_cache:
        _doc_cache[name] = parse_exact(doc_bytes(name))
    return _doc_cache[name]


def doc_digest(name):
    """raw-artifact representation: raw SHA-256 of the exact full document bytes."""
    return sha256hex(doc_bytes(name))


_registry = None


def registry():
    global _registry
    if _registry is None:
        r = Registry()
        for name in DOCS:
            try:
                d = doc(name)
            except Exception:
                continue
            if not isinstance(d, dict):
                continue
            res = Resource.from_contents(d, default_specification=DRAFT202012)
            uri = d.get("$id")
            if uri:
                r = r.with_resource(uri, res)
            # also register by kit-relative path, the form the annotations use
            r = r.with_resource(DOCS[name].split("docs/coop/design-corrections/")[-1], res)
        _registry = r
    return _registry


def doc_uri(document):
    d = doc(document)
    uri = d.get("$id") if isinstance(d, dict) else None
    return uri or DOCS[document].split("docs/coop/design-corrections/")[-1]


def validator_for(document, selector="#"):
    """Validate a SELECTOR of a document IN THE DOCUMENT'S OWN CONTEXT, so that
    local $ref resolution behaves exactly as the payload registry law states:
    'admission validates the payload against the row's selector, resolved
    through the pinned local closure with no network retrieval'."""
    ref = doc_uri(document) + (selector if selector not in ("", None) else "#")
    return jsonschema.Draft202012Validator({"$ref": ref}, registry=registry())


def validate(document, selector, instance):
    """Returns [] on success, else a list of error strings."""
    v = validator_for(document, selector)
    errs = sorted(v.iter_errors(instance), key=lambda e: list(e.path))
    return ["%s: %s" % ("/".join(str(x) for x in e.path) or "<root>", e.message)
            for e in errs]


# ---------------------------------------------------------------------------
# 7. Content-addressed store (one store keyed by raw SHA-256)
# ---------------------------------------------------------------------------
class CAS(dict):
    """digest hex -> exact retained bytes."""

    def put(self, b):
        d = sha256hex(b)
        if d in self and self[d] != b:
            raise Refused("CAS_COLLISION", d)
        self[d] = b
        return d

    def put_record(self, record):
        return self.put(C(record))

    def put_frame(self, domain, descriptor):
        return self.put(h_frame(domain, descriptor))

    def get(self, d):
        if d not in self:
            raise Refused("EVIDENCE_UNAVAILABLE", d)
        return self[d]


# ---------------------------------------------------------------------------
# 8. `x-opensip-order` admission (identity-and-evidence S3)
# ---------------------------------------------------------------------------
# "x-opensip-order is the machine-readable schema annotation for these orders,
#  and the closed vocabulary is exactly [sequence, canonical-set,
#  canonical-order, utf8, path, numeric, ordinal, predicate, ruleId, waiverId,
#  {by:[...]}].  All except sequence and canonical-order also require unique
#  sort keys; uniqueItems alone neither selects nor overrides an order.  An
#  annotation outside this vocabulary refuses rather than passing silently."

ORDER_VOCABULARY = {"sequence", "canonical-set", "canonical-order", "utf8",
                    "path", "numeric", "ordinal", "predicate", "ruleId",
                    "waiverId"}


def _order_key(kind, item):
    if kind == "canonical-set" or kind == "canonical-order":
        return C(item)
    if kind == "utf8":
        if type(item) is not str:
            raise Refused("ORDER_UTF8_NEEDS_A_STRING_ITEM", repr(item))
        return item.encode("utf-8")
    if kind == "path":
        return item["path"].encode("utf-8")
    if kind == "numeric":
        return item
    if kind == "ordinal":
        return item["ordinal"]
    if kind == "predicate":
        return (item["ruleId"] + "," + item["subjectId"] + ","
                + item["predicateId"]).encode("utf-8")
    if kind in ("ruleId", "waiverId"):
        return item[kind].encode("utf-8")
    raise Refused("ORDER_ANNOTATION_UNKNOWN", str(kind))


def admit_order(schema_node, instance, path="#", resolver=None, faults=None):
    """Walk an instance against a schema node and enforce every declared order.

    Returns a list of order faults.  `sequence` (and any unannotated array)
    imposes nothing.  Anything outside the closed vocabulary REFUSES.
    """
    if faults is None:
        faults = []
    if not isinstance(schema_node, dict):
        return faults
    if "$ref" in schema_node and resolver is not None:
        schema_node = resolver(schema_node["$ref"]) or {}
    ann = schema_node.get("x-opensip-order")
    if ann is not None and isinstance(instance, list):
        if isinstance(ann, dict):
            keys = ann.get("by")
            if not isinstance(keys, list) or not keys:
                faults.append("ORDER_ANNOTATION_UNKNOWN:%s:%r" % (path, ann))
            else:
                prev = None
                seen = set()
                for it in instance:
                    k = tuple(it[x] for x in keys)
                    kb = "\x00".join(k).encode("utf-8")
                    if prev is not None and kb <= prev:
                        faults.append("ORDER_NOT_STRICTLY_ASCENDING:%s:%r"
                                      % (path, k))
                    if kb in seen:
                        faults.append("ORDER_DUPLICATE_SORT_KEY:%s:%r" % (path, k))
                    seen.add(kb)
                    prev = kb
        elif ann not in ORDER_VOCABULARY:
            faults.append("ORDER_ANNOTATION_UNKNOWN:%s:%s" % (path, ann))
        elif ann != "sequence":
            prev = None
            seen = set()
            for it in instance:
                try:
                    k = _order_key(ann, it)
                except Refused as r:
                    faults.append("%s:%s" % (r.code, path))
                    break
                kb = k if isinstance(k, bytes) else k
                if prev is not None:
                    lt = (kb < prev) if isinstance(kb, bytes) else (kb < prev)
                    eq = kb == prev
                    if lt or (eq and ann != "canonical-order"):
                        faults.append("ORDER_NOT_ASCENDING:%s:%r" % (path, it))
                if ann != "canonical-order":
                    key_repr = kb if isinstance(kb, bytes) else repr(kb)
                    if key_repr in seen:
                        faults.append("ORDER_DUPLICATE_SORT_KEY:%s" % path)
                    seen.add(key_repr)
                prev = kb
    # descend
    if isinstance(instance, dict):
        for k, v in instance.items():
            sub = (schema_node.get("properties", {}) or {}).get(k)
            if sub is None:
                sub = schema_node.get("additionalProperties")
            if isinstance(sub, dict):
                admit_order(sub, v, path + "/" + k, resolver, faults)
    elif isinstance(instance, list):
        items = schema_node.get("items")
        if isinstance(items, dict):
            for i, v in enumerate(instance):
                admit_order(items, v, path + "/%d" % i, resolver, faults)
    for comb in ("oneOf", "anyOf", "allOf"):
        for alt in schema_node.get(comb, []):
            admit_order(alt, instance, path, resolver, faults)
    return faults


def order_resolver(document):
    d = doc(document)

    def resolve(ref):
        if not ref.startswith("#/"):
            return None
        node = d
        for p in ref.lstrip("#/").split("/"):
            p = p.replace("~1", "/").replace("~0", "~")
            if p not in node:
                return None
            node = node[p]
        return node
    return resolve


def admit_ordered(document, selector, instance):
    d = doc(document)
    node = d
    if selector not in ("#", "", None):
        for p in selector.lstrip("#/").split("/"):
            node = node[p]
    return admit_order(node, instance, selector, order_resolver(document))
