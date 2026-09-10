"""Blind-consumer reference helper for OpenSIP DR-011-R10.

Written independently from contract prose only:
  - identity-and-evidence.md section 3 (canonical encoding C, H, frames, digest law)
  - admission-and-qualification.md section 1 (exact numeric/lexical admission)
  - fact-identity-policy.v2.json #/canonicalisationSchema (body identity frame)
  - resolved-inputs.v2.json #planIdContract.canonicalValueEncoding (CVE1)
  - delivery.v4.json derivedFrom.operations[17].value.recipe (capabilityManifestId)

No author model, checker, fixture or golden was read. Disposable design-reference
code; not product code.
"""

import hashlib
import json
import math
import re
import unicodedata

# --------------------------------------------------------------------------
# Exact typed admission (admission-and-qualification section 1, identity section 3)
# --------------------------------------------------------------------------

MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32
INT_MIN = -(2 ** 63)
INT_MAX = 2 ** 64 - 1


class AdmissionError(Exception):
    pass


_INT_TOKEN = re.compile(r"^-?(0|[1-9][0-9]*)$")


class _Lexer:
    """Strict JSON reader that keeps lexical information the contract needs.

    Refuses, before any deserialization can lose the evidence:
      duplicate object keys, floating/exponent tokens, -0, nonfinite tokens,
      malformed UTF-8, non-scalar Unicode (lone surrogates), depth > 32.
    """

    def __init__(self, raw: bytes):
        if not isinstance(raw, (bytes, bytearray)):
            raise AdmissionError("input must be bytes")
        if len(raw) > MAX_DESCRIPTOR_BYTES:
            raise AdmissionError("descriptor exceeds 4 MiB; never truncated")
        try:
            self.s = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise AdmissionError("malformed UTF-8: %s" % exc)
        self.i = 0
        self.n = len(self.s)

    def error(self, msg):
        raise AdmissionError("%s at offset %d" % (msg, self.i))

    def ws(self):
        while self.i < self.n and self.s[self.i] in " \t\n\r":
            self.i += 1

    def parse(self):
        self.ws()
        v = self.value(1)
        self.ws()
        if self.i != self.n:
            self.error("trailing content")
        return v

    def value(self, depth):
        if depth > MAX_DEPTH:
            self.error("nesting depth exceeds 32")
        if self.i >= self.n:
            self.error("unexpected end")
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
        return self.number()

    def lit(self, text, val):
        if self.s[self.i:self.i + len(text)] != text:
            self.error("bad literal")
        self.i += len(text)
        return val

    def obj(self, depth):
        self.i += 1
        out = {}
        self.ws()
        if self.i < self.n and self.s[self.i] == "}":
            self.i += 1
            return out
        while True:
            self.ws()
            if self.i >= self.n or self.s[self.i] != '"':
                self.error("object key must be a string")
            k = self.string()
            if k in out:
                raise AdmissionError("duplicate object key %r" % k)
            self.ws()
            if self.i >= self.n or self.s[self.i] != ":":
                self.error("expected ':'")
            self.i += 1
            self.ws()
            # a key adds no container depth; the value is one level deeper
            out[k] = self.value(depth + 1)
            self.ws()
            if self.i < self.n and self.s[self.i] == ",":
                self.i += 1
                continue
            if self.i < self.n and self.s[self.i] == "}":
                self.i += 1
                return out
            self.error("expected ',' or '}'")

    def arr(self, depth):
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
            self.error("expected ',' or ']'")

    def string(self):
        self.i += 1
        buf = []
        while True:
            if self.i >= self.n:
                self.error("unterminated string")
            c = self.s[self.i]
            if c == '"':
                self.i += 1
                text = "".join(buf)
                for ch in text:
                    if 0xD800 <= ord(ch) <= 0xDFFF:
                        raise AdmissionError("non-scalar Unicode (surrogate)")
                return text
            if c == "\\":
                self.i += 1
                if self.i >= self.n:
                    self.error("bad escape")
                e = self.s[self.i]
                simple = {'"': '"', "\\": "\\", "/": "/", "b": "\b",
                          "f": "\f", "n": "\n", "r": "\r", "t": "\t"}
                if e in simple:
                    buf.append(simple[e])
                    self.i += 1
                elif e == "u":
                    hexs = self.s[self.i + 1:self.i + 5]
                    if len(hexs) != 4 or not re.match(r"^[0-9a-fA-F]{4}$", hexs):
                        self.error("bad \\u escape")
                    cp = int(hexs, 16)
                    self.i += 5
                    if 0xD800 <= cp <= 0xDBFF:
                        if self.s[self.i:self.i + 2] != "\\u":
                            raise AdmissionError("lone high surrogate")
                        lo = self.s[self.i + 2:self.i + 6]
                        if len(lo) != 4 or not re.match(r"^[0-9a-fA-F]{4}$", lo):
                            raise AdmissionError("lone high surrogate")
                        lov = int(lo, 16)
                        if not (0xDC00 <= lov <= 0xDFFF):
                            raise AdmissionError("lone high surrogate")
                        self.i += 6
                        buf.append(chr(0x10000 + ((cp - 0xD800) << 10) + (lov - 0xDC00)))
                    elif 0xDC00 <= cp <= 0xDFFF:
                        raise AdmissionError("lone low surrogate")
                    else:
                        buf.append(chr(cp))
                else:
                    self.error("unknown escape")
                continue
            if ord(c) < 0x20:
                self.error("raw control character in string")
            buf.append(c)
            self.i += 1

    def number(self):
        start = self.i
        while self.i < self.n and self.s[self.i] not in ",]} \t\n\r":
            self.i += 1
        tok = self.s[start:self.i]
        if tok in ("NaN", "Infinity", "-Infinity"):
            raise AdmissionError("nonfinite numeric token %r" % tok)
        if tok == "-0":
            raise AdmissionError("-0 is not an admissible integer token")
        if not _INT_TOKEN.match(tok):
            raise AdmissionError(
                "non-integer numeric token %r: floats/exponents never satisfy an "
                "integer field even when mathematically equal" % tok)
        v = int(tok)
        if not (INT_MIN <= v <= INT_MAX):
            raise AdmissionError("integer out of [-2^63, 2^64-1]: %r" % tok)
        return v


def admit_bytes(raw):
    """Lexical admission of external descriptor bytes -> python value."""
    return _Lexer(raw).parse()


def admit_value(value, depth=1, _root=True):
    """Admission of an already-constructed in-memory value.

    An already-decoded 1.0 or True cannot satisfy an integer field, so floats are
    refused here as they are lexically.
    """
    if depth > MAX_DEPTH:
        raise AdmissionError("nesting depth exceeds 32")
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, float):
        raise AdmissionError("float value %r is inadmissible (no float type)" % value)
    if isinstance(value, int):
        if not (INT_MIN <= value <= INT_MAX):
            raise AdmissionError("integer out of range: %r" % value)
        return value
    if isinstance(value, str):
        for ch in value:
            if 0xD800 <= ord(ch) <= 0xDFFF:
                raise AdmissionError("non-scalar Unicode (surrogate)")
        return value
    if isinstance(value, list):
        for v in value:
            admit_value(v, depth + 1, False)
        return value
    if isinstance(value, dict):
        seen = set()
        for k in value:
            if not isinstance(k, str):
                raise AdmissionError("object key must be a string")
            if k in seen:
                raise AdmissionError("duplicate key %r" % k)
            seen.add(k)
            admit_value(value[k], depth + 1, False)
        return value
    raise AdmissionError("unsupported type %s" % type(value).__name__)


# --------------------------------------------------------------------------
# C: canonical JSON (identity-and-evidence section 3)
# --------------------------------------------------------------------------

_ESCAPES = {
    0x08: "\\b", 0x09: "\\t", 0x0A: "\\n", 0x0C: "\\f", 0x0D: "\\r",
}


def _c_string(s):
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif o in _ESCAPES:
            out.append(_ESCAPES[o])
        elif o < 0x20:
            out.append("\\u%04x" % o)          # lowercase \u00xx
        else:
            out.append(ch)                      # no escaping of /, U+007F, U+2028
    out.append('"')
    return "".join(out)


def c_encode(value):
    """C(X): canonical JSON bytes. Never sorts or dedupes an array."""
    admit_value(value)
    return _c(value).encode("utf-8")


def _c(v):
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return str(v)                            # shortest ordinary decimal
    if isinstance(v, str):
        return _c_string(v)
    if isinstance(v, list):
        return "[" + ",".join(_c(x) for x in v) + "]"
    if isinstance(v, dict):
        # UTF-8 byte-ordered keys
        items = sorted(v.items(), key=lambda kv: kv[0].encode("utf-8"))
        return "{" + ",".join(_c_string(k) + ":" + _c(x) for k, x in items) + "}"
    raise AdmissionError("uncanonicalizable %r" % (v,))


# --------------------------------------------------------------------------
# H and frames
# --------------------------------------------------------------------------

PRODUCT_PREFIX = b"opensip.product.v1"


def h_frame(domain, descriptor):
    body = c_encode(descriptor)
    return (PRODUCT_PREFIX + b"\x00" + domain.encode("ascii") + b"\x00"
            + len(body).to_bytes(8, "big") + body)


def H(domain, descriptor):
    return hashlib.sha256(h_frame(domain, descriptor)).hexdigest()


def ident(prefix, domain, descriptor):
    return "%s:%s" % (prefix, H(domain, descriptor))


def parse_frame(raw, allowed_domains):
    """Exact frame admission: prefix, member domain, declared length, byte-identity."""
    if not raw.startswith(PRODUCT_PREFIX + b"\x00"):
        raise AdmissionError("frame prefix mismatch (a raw payload is not a frame)")
    rest = raw[len(PRODUCT_PREFIX) + 1:]
    z = rest.find(b"\x00")
    if z < 0:
        raise AdmissionError("frame domain not terminated")
    domain = rest[:z].decode("ascii")
    if domain not in allowed_domains:
        raise AdmissionError("domain %r is not a member of the annotation's domain set" % domain)
    rest = rest[z + 1:]
    if len(rest) < 8:
        raise AdmissionError("frame truncated")
    declared = int.from_bytes(rest[:8], "big")
    body = rest[8:]
    if declared != len(body):
        raise AdmissionError("declared length %d != remaining %d" % (declared, len(body)))
    parsed = admit_bytes(body)
    if c_encode(parsed) != body:
        raise AdmissionError("frame body is not C of its own parse")
    return domain, parsed


def raw_sha256(b):
    return hashlib.sha256(b).hexdigest()


def canonical_record_digest(record):
    """canonical-record representation: raw SHA-256 of C(record)."""
    return raw_sha256(c_encode(record))


# --------------------------------------------------------------------------
# x-opensip-order enforcement (identity section 3 closed vocabulary)
# --------------------------------------------------------------------------

def _key_for(order, item):
    if order == "canonical-set" or order == "canonical-order":
        return c_encode(item)
    if order == "utf8":
        return item.encode("utf-8")
    if order == "path":
        return item["path"].encode("utf-8")
    if order == "numeric":
        return item
    if order == "ordinal":
        return item["ordinal"]
    if order == "predicate":
        return (item["ruleId"], item["subjectId"], item["predicateId"])
    if order in ("ruleId", "waiverId"):
        return item[order].encode("utf-8")
    if isinstance(order, dict) and "by" in order:
        return tuple(item[k] for k in order["by"])
    raise AdmissionError("annotation %r is outside the closed order vocabulary" % (order,))


def check_order(array, order):
    """Refuse a deviating order BEFORE hashing. `sequence` admits anything."""
    if order == "sequence":
        return True
    if order == "ordinal":
        for i, it in enumerate(array):
            if it["ordinal"] != i:
                raise AdmissionError("ordinal must be contiguous zero-based")
        return True
    keys = [_key_for(order, it) for it in array]
    unique_required = order not in ("sequence", "canonical-order")
    for a, b in zip(keys, keys[1:]):
        if order == "canonical-order":
            if a > b:
                raise AdmissionError("canonical-order requires nondecreasing item bytes")
        else:
            if a >= b:
                raise AdmissionError("order %r requires strictly ascending unique keys" % (order,))
    if unique_required and len(set(map(repr, keys))) != len(keys):
        raise AdmissionError("duplicate sort key under %r" % (order,))
    return True


# --------------------------------------------------------------------------
# CVE1 (resolved-inputs.v2 planIdContract.canonicalValueEncoding)
# --------------------------------------------------------------------------

CVE1_TYPES = ["null", "false", "true", "unsigned-64", "negative-signed-64",
              "NFC-UTF8-string", "array", "string-keyed-map"]


def cve1(value):
    if value is None:
        return b"\x00"
    if value is False:
        return b"\x01"
    if value is True:
        return b"\x02"
    if isinstance(value, float):
        raise AdmissionError("CVE1 forbids floating-point values")
    if isinstance(value, int):
        if value >= 0:
            if value > 2 ** 64 - 1:
                raise AdmissionError("unsigned-64 overflow")
            return b"\x03" + value.to_bytes(8, "big")
        if value < -(2 ** 63):
            raise AdmissionError("negative-signed-64 underflow")
        return b"\x07" + value.to_bytes(8, "big", signed=True)
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise AdmissionError("CVE1 rejects a non-NFC string rather than normalising")
        b = value.encode("utf-8")
        return b"\x04" + len(b).to_bytes(4, "big") + b
    if isinstance(value, list):
        return b"\x05" + len(value).to_bytes(4, "big") + b"".join(cve1(x) for x in value)
    if isinstance(value, dict):
        keys = list(value.keys())
        if len(set(keys)) != len(keys):
            raise AdmissionError("duplicate map key")
        for k in keys:
            if not isinstance(k, str):
                raise AdmissionError("CVE1 map keys must be strings")
        enc = sorted(((k.encode("utf-8"), k) for k in keys), key=lambda t: t[0])
        out = b"\x06" + len(keys).to_bytes(4, "big")
        for _, k in enc:
            out += cve1(k) + cve1(value[k])
        return out
    if isinstance(value, (bytes, bytearray)):
        raise AdmissionError("CVE1 forbids byte strings")
    raise AdmissionError("CVE1: unsupported type %s" % type(value).__name__)


CAPABILITY_MANIFEST_TAG = b"opensip.capability-manifest.v1"


def capability_manifest_id(manifest):
    committed = cve1(manifest)
    cid = hashlib.sha256(CAPABILITY_MANIFEST_TAG + b"\x00" + committed).hexdigest()
    return cid, committed


# --------------------------------------------------------------------------
# FACT-IDENTITY body frame (fact-identity-policy.v2 #/canonicalisationSchema)
# --------------------------------------------------------------------------

BODY_DOMAIN_TAG = b"opensip.fact-identity.v1"


def _u8len(b):
    if len(b) > 255:
        raise AdmissionError(
            "component of %d bytes is not representable under the inherited u8 length"
            % len(b))
    return bytes([len(b)]) + b


def framed_token_stream(tokens):
    """u32be token_count || (u16be kind_len || kind || u32be val_len || val)*"""
    out = len(tokens).to_bytes(4, "big")
    for kind, val in tokens:
        kb = kind.encode("utf-8")
        vb = val.encode("utf-8") if isinstance(val, str) else val
        if not kb:
            raise AdmissionError("token kind_id must be a non-empty canonical identifier")
        out += len(kb).to_bytes(2, "big") + kb + len(vb).to_bytes(4, "big") + vb
    return out


def body_payload_L0(body_bytes):
    return len(body_bytes).to_bytes(4, "big") + body_bytes


def body_identity_frame(level_id, level_version_32, language_id, language_version_32,
                        payload):
    if len(level_version_32) != 32:
        raise AdmissionError("levelVersion must be the raw 32 digest bytes, not hex text")
    if len(language_version_32) != 32:
        raise AdmissionError("languageVersion must be the raw 32 digest bytes")
    return (_u8len(BODY_DOMAIN_TAG)
            + _u8len(level_id.encode("ascii"))
            + _u8len(level_version_32)
            + _u8len(language_id.encode("ascii"))
            + _u8len(language_version_32)
            + len(payload).to_bytes(4, "big") + payload)


def body_identity(level_id, level_version_32, language_id, language_version_32, payload):
    frame = body_identity_frame(level_id, level_version_32, language_id,
                                language_version_32, payload)
    return "sha256:" + hashlib.sha256(frame).hexdigest(), frame


def body_language_version_bytes(record):
    """languageVersion component = raw 32 bytes of SHA-256(C(body-language-version))."""
    return hashlib.sha256(c_encode(record)).digest()
