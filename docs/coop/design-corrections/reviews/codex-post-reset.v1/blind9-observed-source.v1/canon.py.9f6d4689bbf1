"""Independent reference encoder / identity helper for OpenSIP DR-011-R10.

Written from the normative prose ONLY (identity-and-evidence.md sections 2-3,
admission-and-qualification.md section 1, resolved-inputs.v2#planIdContract.
canonicalValueEncoding).  No author implementation was read.

Everything here is disposable design-reference code.
"""
from __future__ import annotations

import hashlib
import re
import struct
import unicodedata

MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024      # identity S3 "Maximum descriptor is 4 MiB"
MAX_DEPTH = 32                              # "nesting depth 32: the root container counts as 1"
INT_MIN = -(2 ** 63)                        # "Integer range is [-2^63, 2^64-1]"
INT_MAX = 2 ** 64 - 1

PRODUCT_FRAME_PREFIX = b"opensip.product.v1"
CAPABILITY_MANIFEST_DOMAIN = b"opensip.capability-manifest.v1"


class AdmissionError(Exception):
    """Raised for any lexical / typed / structural admission refusal."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


# ---------------------------------------------------------------------------
# 1. Exact lexical admission of RAW input bytes.
#
# identity S3: "Before deserialization loses lexical information, reject
# duplicate keys, floating/exponent tokens, -0, nonfinite tokens, malformed
# UTF-8 and non-scalar Unicode."
# admission S1 adds: 1.0 / 1e0 / booleans / numeric strings never satisfy an
# integer field.
#
# This is a hand-written JSON reader: json.loads() would already have lost the
# lexical distinctions the contract requires us to refuse on.
# ---------------------------------------------------------------------------

_WS = b" \t\n\r"
_INT_TOKEN = re.compile(rb"-?(?:0|[1-9][0-9]*)")


class _Reader:
    def __init__(self, data: bytes):
        self.b = data
        self.i = 0
        self.n = len(data)

    def peek(self):
        return self.b[self.i:self.i + 1]

    def skip_ws(self):
        while self.i < self.n and self.b[self.i:self.i + 1] in (b" ", b"\t", b"\n", b"\r"):
            self.i += 1

    def expect(self, ch: bytes):
        if self.peek() != ch:
            raise AdmissionError("LEX_UNEXPECTED", f"want {ch!r} at byte {self.i}")
        self.i += 1


def admit_raw(data: bytes, *, max_bytes: int = MAX_DESCRIPTOR_BYTES,
              max_depth: int = MAX_DEPTH):
    """Parse raw JSON bytes under the exact typed admission profile.

    Returns the decoded Python object.  Ints stay int, bools stay bool
    (they are distinct: "booleans are distinct").
    """
    if len(data) > max_bytes:
        raise AdmissionError("DESCRIPTOR_TOO_LARGE", f"{len(data)} > {max_bytes}")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise AdmissionError("MALFORMED_UTF8", str(exc)) from exc
    for ch in text:
        # "non-scalar Unicode" -- surrogates are not Unicode scalar values.
        if 0xD800 <= ord(ch) <= 0xDFFF:
            raise AdmissionError("NON_SCALAR_UNICODE", hex(ord(ch)))

    r = _Reader(data)
    r.skip_ws()
    value = _read_value(r, depth=0, max_depth=max_depth)
    r.skip_ws()
    if r.i != r.n:
        raise AdmissionError("LEX_TRAILING", f"{r.n - r.i} trailing bytes")
    return value


def _read_value(r: _Reader, depth: int, max_depth: int):
    c = r.peek()
    if c == b"{":
        return _read_object(r, depth, max_depth)
    if c == b"[":
        return _read_array(r, depth, max_depth)
    if c == b'"':
        return _read_string(r)
    if c == b"t":
        _lit(r, b"true")
        return True
    if c == b"f":
        _lit(r, b"false")
        return False
    if c == b"n":
        _lit(r, b"null")
        return None
    return _read_number(r)


def _lit(r: _Reader, lit: bytes):
    if r.b[r.i:r.i + len(lit)] != lit:
        raise AdmissionError("LEX_TOKEN", f"at byte {r.i}")
    r.i += len(lit)


def _read_object(r: _Reader, depth: int, max_depth: int):
    # "the root container counts as 1; scalar leaves and object keys add no
    # container depth"
    if depth + 1 > max_depth:
        raise AdmissionError("DEPTH_EXCEEDED", f"depth {depth + 1} > {max_depth}")
    r.expect(b"{")
    out = {}
    r.skip_ws()
    if r.peek() == b"}":
        r.i += 1
        return out
    while True:
        r.skip_ws()
        if r.peek() != b'"':
            raise AdmissionError("LEX_KEY", f"at byte {r.i}")
        key = _read_string(r)
        if key in out:
            raise AdmissionError("DUPLICATE_KEY", key)
        r.skip_ws()
        r.expect(b":")
        r.skip_ws()
        out[key] = _read_value(r, depth + 1, max_depth)
        r.skip_ws()
        c = r.peek()
        if c == b",":
            r.i += 1
            continue
        if c == b"}":
            r.i += 1
            return out
        raise AdmissionError("LEX_OBJECT", f"at byte {r.i}")


def _read_array(r: _Reader, depth: int, max_depth: int):
    if depth + 1 > max_depth:
        raise AdmissionError("DEPTH_EXCEEDED", f"depth {depth + 1} > {max_depth}")
    r.expect(b"[")
    out = []
    r.skip_ws()
    if r.peek() == b"]":
        r.i += 1
        return out
    while True:
        r.skip_ws()
        out.append(_read_value(r, depth + 1, max_depth))
        r.skip_ws()
        c = r.peek()
        if c == b",":
            r.i += 1
            continue
        if c == b"]":
            r.i += 1
            return out
        raise AdmissionError("LEX_ARRAY", f"at byte {r.i}")


def _read_string(r: _Reader) -> str:
    r.expect(b'"')
    out = []
    while True:
        if r.i >= r.n:
            raise AdmissionError("LEX_STRING", "unterminated")
        c = r.b[r.i]
        if c == 0x22:       # closing quote
            r.i += 1
            return "".join(out)
        if c == 0x5C:       # backslash
            r.i += 1
            e = r.b[r.i:r.i + 1]
            r.i += 1
            simple = {b'"': '"', b"\\": "\\", b"/": "/", b"b": "\b",
                      b"f": "\f", b"n": "\n", b"r": "\r", b"t": "\t"}
            if e in simple:
                out.append(simple[e])
                continue
            if e == b"u":
                hx = r.b[r.i:r.i + 4].decode("ascii", errors="replace")
                if len(hx) != 4 or not re.fullmatch(r"[0-9a-fA-F]{4}", hx):
                    raise AdmissionError("LEX_ESCAPE", hx)
                r.i += 4
                cp = int(hx, 16)
                if 0xD800 <= cp <= 0xDBFF:
                    # a valid pair is the only lawful continuation
                    if r.b[r.i:r.i + 2] != b"\\u":
                        raise AdmissionError("NON_SCALAR_UNICODE", f"lone high {hx}")
                    hx2 = r.b[r.i + 2:r.i + 6].decode("ascii", errors="replace")
                    if not re.fullmatch(r"[0-9a-fA-F]{4}", hx2):
                        raise AdmissionError("LEX_ESCAPE", hx2)
                    lo = int(hx2, 16)
                    if not (0xDC00 <= lo <= 0xDFFF):
                        raise AdmissionError("NON_SCALAR_UNICODE", f"bad pair {hx}{hx2}")
                    r.i += 6
                    out.append(chr(0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00)))
                    continue
                if 0xDC00 <= cp <= 0xDFFF:
                    raise AdmissionError("NON_SCALAR_UNICODE", f"lone low {hx}")
                out.append(chr(cp))
                continue
            raise AdmissionError("LEX_ESCAPE", repr(e))
        if c < 0x20:
            raise AdmissionError("LEX_CONTROL", hex(c))
        # consume one whole UTF-8 sequence
        j = r.i + 1
        while j < r.n and (r.b[j] & 0xC0) == 0x80:
            j += 1
        out.append(r.b[r.i:j].decode("utf-8"))
        r.i = j


def _read_number(r: _Reader):
    m = _INT_TOKEN.match(r.b, r.i)
    if not m:
        # nonfinite tokens (NaN/Infinity) and everything else land here
        tail = r.b[r.i:r.i + 12]
        raise AdmissionError("NUMBER_NOT_INTEGER", tail.decode("ascii", "replace"))
    tok = m.group(0)
    end = m.end()
    nxt = r.b[end:end + 1]
    if nxt in (b".", b"e", b"E"):
        # "floating/exponent tokens" -- 1.0, 1e0, 1E0 are NOT integers
        raise AdmissionError("NUMBER_NOT_INTEGER", (tok + nxt).decode())
    if tok == b"-0":
        raise AdmissionError("NEGATIVE_ZERO", "-0")
    r.i = end
    v = int(tok)
    if not (INT_MIN <= v <= INT_MAX):
        raise AdmissionError("INTEGER_RANGE", str(v))
    return v


# ---------------------------------------------------------------------------
# 2. C -- the canonical encoder.
#
# identity S3: "Canonical JSON has UTF-8 byte-ordered keys, no whitespace or
# trailing newline, no Unicode normalization, shortest ordinary decimal
# integers, and unescaped Unicode scalar characters. Escape quote and
# backslash, use \b\t\n\f\r, and lowercase \u00xx for other U+0000-001F
# controls; do not escape slash.  Arrays are encoded in their admitted order."
# "U+007F and U+2028 remain unescaped."
# ---------------------------------------------------------------------------

_SIMPLE_ESCAPES = {
    0x08: "\\b", 0x09: "\\t", 0x0A: "\\n", 0x0C: "\\f", 0x0D: "\\r",
    0x22: '\\"', 0x5C: "\\\\",
}


def c_string(s: str) -> str:
    out = ['"']
    for ch in s:
        cp = ord(ch)
        if 0xD800 <= cp <= 0xDFFF:
            raise AdmissionError("NON_SCALAR_UNICODE", hex(cp))
        esc = _SIMPLE_ESCAPES.get(cp)
        if esc is not None:
            out.append(esc)
        elif cp < 0x20:
            out.append("\\u%04x" % cp)     # lowercase hex
        else:
            out.append(ch)                  # incl. U+007F and U+2028, unescaped
    out.append('"')
    return "".join(out)


def C(value) -> bytes:
    """Canonical bytes of an already-admitted value."""
    return _c(value).encode("utf-8")


def _c(v) -> str:
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        if not (INT_MIN <= v <= INT_MAX):
            raise AdmissionError("INTEGER_RANGE", str(v))
        return str(v)                       # shortest ordinary decimal
    if isinstance(v, float):
        raise AdmissionError("FLOAT_FORBIDDEN", repr(v))
    if isinstance(v, str):
        return c_string(v)
    if isinstance(v, (list, tuple)):
        return "[" + ",".join(_c(x) for x in v) + "]"
    if isinstance(v, dict):
        # UTF-8 byte-ordered keys
        items = sorted(v.items(), key=lambda kv: kv[0].encode("utf-8"))
        return "{" + ",".join(c_string(k) + ":" + _c(x) for k, x in items) + "}"
    raise AdmissionError("UNENCODABLE_TYPE", type(v).__name__)


# ---------------------------------------------------------------------------
# 3. H and the frame.
# H(D,X) = SHA256("opensip.product.v1" || 00 || D || 00 || u64be(len C(X)) || C(X))
# ---------------------------------------------------------------------------

def frame(domain: str, descriptor) -> bytes:
    body = C(descriptor)
    return (PRODUCT_FRAME_PREFIX + b"\x00" + domain.encode("ascii") + b"\x00"
            + struct.pack(">Q", len(body)) + body)


def H(domain: str, descriptor) -> str:
    return hashlib.sha256(frame(domain, descriptor)).hexdigest()


def parse_frame(blob: bytes, allowed_domains):
    """Exact frame admission (identity S3 'Frame admission is exact')."""
    if not blob.startswith(PRODUCT_FRAME_PREFIX + b"\x00"):
        raise AdmissionError("FRAME_PREFIX", "not an H frame")
    rest = blob[len(PRODUCT_FRAME_PREFIX) + 1:]
    nul = rest.find(b"\x00")
    if nul < 0:
        raise AdmissionError("FRAME_DOMAIN", "no domain terminator")
    domain = rest[:nul].decode("ascii")
    if domain not in allowed_domains:
        raise AdmissionError("FRAME_DOMAIN_UNREGISTERED", domain)
    rest = rest[nul + 1:]
    if len(rest) < 8:
        raise AdmissionError("FRAME_LENGTH", "truncated")
    (declared,) = struct.unpack(">Q", rest[:8])
    body = rest[8:]
    if declared != len(body):
        raise AdmissionError("FRAME_LENGTH", f"declared {declared} actual {len(body)}")
    payload = admit_raw(body)
    if C(payload) != body:
        raise AdmissionError("FRAME_NOT_CANONICAL", domain)
    return domain, payload


def raw_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_record_digest(record) -> str:
    """raw SHA256 of C(record) -- the `canonical-record` representation."""
    return hashlib.sha256(C(record)).hexdigest()


# ---------------------------------------------------------------------------
# 4. x-opensip-order -- the closed annotation vocabulary of identity S3.
# ---------------------------------------------------------------------------

_UNIQUE_REQUIRED = {"canonical-set", "utf8", "path", "numeric", "ordinal",
                    "predicate", "ruleId", "waiverId"}


def check_order(annotation, array, where: str = ""):
    """Validate an array against its declared x-opensip-order annotation."""
    if annotation is None:
        raise AdmissionError("ORDER_ANNOTATION_MISSING", where)
    if isinstance(annotation, dict):
        keys = annotation.get("by")
        if not isinstance(keys, list) or not keys:
            raise AdmissionError("ORDER_ANNOTATION_INVALID", where)
        sort_keys = [tuple(str(item[k]).encode("utf-8") for k in keys) for item in array]
        _strict_ascending(sort_keys, where, "by:" + ",".join(keys))
        return
    if annotation == "sequence":
        return
    if annotation == "canonical-order":
        keys = [C(x) for x in array]
        for a, b in zip(keys, keys[1:]):
            if a > b:
                raise AdmissionError("ORDER_OR_DUPLICATE", f"{where}: canonical-order")
        return
    if annotation == "canonical-set":
        _strict_ascending([C(x) for x in array], where, "canonical-set")
        return
    if annotation == "utf8":
        _strict_ascending([x.encode("utf-8") for x in array], where, "utf8")
        return
    if annotation == "path":
        _strict_ascending([x["path"].encode("utf-8") for x in array], where, "path")
        return
    if annotation == "numeric":
        _strict_ascending(list(array), where, "numeric")
        return
    if annotation == "ordinal":
        ords = [x["ordinal"] for x in array]
        if ords != list(range(len(ords))):
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{where}: ordinal not contiguous")
        return
    if annotation == "predicate":
        _strict_ascending(
            [(p["ruleId"].encode(), p["subjectId"].encode(), p["predicateId"].encode())
             for p in array], where, "predicate")
        return
    if annotation in ("ruleId", "waiverId"):
        _strict_ascending([x[annotation].encode("utf-8") for x in array],
                          where, annotation)
        return
    # "An annotation outside this vocabulary refuses rather than passing silently."
    raise AdmissionError("ORDER_ANNOTATION_UNREGISTERED", f"{where}: {annotation!r}")


def _strict_ascending(keys, where, label):
    for a, b in zip(keys, keys[1:]):
        if a >= b:
            raise AdmissionError("ORDER_OR_DUPLICATE", f"{where}: {label}")


def sorted_canonical_set(items):
    return sorted(items, key=C)


# ---------------------------------------------------------------------------
# 5. CVE1 -- the capability-manifest value encoder.
# resolved-inputs.v2.json#planIdContract.canonicalValueEncoding, all eight
# closed types.  NOTE: CVE1 is a SEPARATE codec from C and applies to the
# capability manifest only (identity S3).
# ---------------------------------------------------------------------------

def cve1(value) -> bytes:
    if value is None:
        return b"\x00"
    if value is False:
        return b"\x01"
    if value is True:
        return b"\x02"
    if isinstance(value, int):
        if 0 <= value <= 2 ** 64 - 1:
            return b"\x03" + struct.pack(">Q", value)
        if -(2 ** 63) <= value < 0:
            return b"\x07" + struct.pack(">q", value)
        raise AdmissionError("CVE1_INT_RANGE", str(value))
    if isinstance(value, float):
        raise AdmissionError("CVE1_FLOAT_FORBIDDEN", repr(value))
    if isinstance(value, bytes):
        raise AdmissionError("CVE1_BYTES_FORBIDDEN", "byte strings are forbidden")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise AdmissionError("CVE1_NOT_NFC", value)
        enc = value.encode("utf-8")
        return b"\x04" + struct.pack(">I", len(enc)) + enc
    if isinstance(value, (list, tuple)):
        out = b"\x05" + struct.pack(">I", len(value))
        for e in value:
            out += cve1(e)
        return out
    if isinstance(value, dict):
        keys = list(value.keys())
        for k in keys:
            if not isinstance(k, str):
                raise AdmissionError("CVE1_MAP_KEY", repr(k))
            if unicodedata.normalize("NFC", k) != k:
                raise AdmissionError("CVE1_NOT_NFC", k)
        if len(set(keys)) != len(keys):
            raise AdmissionError("CVE1_DUPLICATE_KEY", "map keys are unique")
        ordered = sorted(keys, key=lambda k: k.encode("utf-8"))
        out = b"\x06" + struct.pack(">I", len(ordered))
        for k in ordered:
            out += cve1(k) + cve1(value[k])
        return out
    raise AdmissionError("CVE1_UNENCODABLE", type(value).__name__)


def capability_manifest_id(committed_bytes: bytes) -> str:
    """SHA256(UTF8("opensip.capability-manifest.v1") || 00 || committedBytes)"""
    return hashlib.sha256(
        CAPABILITY_MANIFEST_DOMAIN + b"\x00" + committed_bytes).hexdigest()


# ---------------------------------------------------------------------------
# 6. FACT-IDENTITY body frame (fact-identity-policy.v2 #/canonicalisationSchema
#    byteGrammar.domainSeparatedPreimage, with identity S3's explicit reading
#    of the double length prefix at L0).
# ---------------------------------------------------------------------------

FACT_IDENTITY_DOMAIN_TAG = b"opensip.fact-identity.v1"


def _u8len(component: bytes) -> bytes:
    if len(component) > 255:
        raise AdmissionError("BODY_FRAME_COMPONENT_TOO_LONG", str(len(component)))
    return bytes([len(component)]) + component


def l0_payload(body_span: bytes) -> bytes:
    """u32be raw_byte_len || exact body-span bytes."""
    return struct.pack(">I", len(body_span)) + body_span


def framed_token_stream(tokens) -> bytes:
    """u32be token_count || (u16be kind_len||kind || u32be val_len||val)*"""
    out = struct.pack(">I", len(tokens))
    for kind, val in tokens:
        kb = kind.encode("utf-8")
        vb = val if isinstance(val, bytes) else val.encode("utf-8")
        if not kb:
            raise AdmissionError("TOKEN_KIND_EMPTY", "")
        out += struct.pack(">H", len(kb)) + kb + struct.pack(">I", len(vb)) + vb
    return out


def body_identity_frame(level_id: str, level_version_raw32: bytes,
                        language_id: str, language_version_raw32: bytes,
                        payload: bytes) -> bytes:
    if len(level_version_raw32) != 32:
        raise AdmissionError("LEVEL_VERSION_NOT_RAW32", str(len(level_version_raw32)))
    if len(language_version_raw32) != 32:
        raise AdmissionError("LANGUAGE_VERSION_NOT_RAW32", str(len(language_version_raw32)))
    return (_u8len(FACT_IDENTITY_DOMAIN_TAG)
            + _u8len(level_id.encode("ascii"))
            + _u8len(level_version_raw32)
            + _u8len(language_id.encode("ascii"))
            + _u8len(language_version_raw32)
            + struct.pack(">I", len(payload)) + payload)


def body_identity(level_id: str, level_version_raw32: bytes, language_id: str,
                  language_version_raw32: bytes, payload: bytes) -> str:
    f = body_identity_frame(level_id, level_version_raw32, language_id,
                            language_version_raw32, payload)
    return "sha256:" + hashlib.sha256(f).hexdigest()
