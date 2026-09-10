"""Independent kit-only C, lexical, H, CVE1. Recipes from identity-and-evidence §3
and resolved-inputs.v2#planIdContract.canonicalValueEncoding. Not consumer helper."""
from __future__ import annotations

import hashlib
import unicodedata
from typing import Any

I64_MIN = -9223372036854775808
I64_MAX = 9223372036854775807
U64_MAX = 18446744073709551615
MAX_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32
PRODUCT_PREFIX = b"opensip.product.v1"

DOMAIN_PREFIX = {
    "snapshot": "snapshot2",
    "closure": "closure2",
    "import": "import2",
    "plan": "plan2",
    "subject-scope": "scope2",
    "fact": "fact2",
    "coverage": "coverage2",
    "view": "view2",
    "execution-plan": "exec-plan2",
    "finding-fingerprint": "finding-key2",
    "evaluation-subject": "subject3",
    "finding": "finding3",
    "proof-bundle": "proof3",
    "semantic-evidence": "evidence3",
    "evaluation-seal": "seal3",
    "run": "run3",
    "cache-key": "cache2",
    "regeneration-key": "regen2",
    "policy-derivation": "policy-derivation3",
}

NATIVE_DOMAINS = {
    "native.context.typescript.v2",
    "native.context.rust.v2",
    "native.context.syntax.v2",
    "native.semantic-universe.typescript.v2",
    "native.semantic-universe.rust.v2",
    "native.semantic-universe.syntax.v2",
    "native.dependency-source-set.v1",
    "native.unified-features.rust.v1",
    "native.prepared-output-set.v3",
    "native.cargo-config-projection.v2",
    "native.dependency-file-manifest.v1",
    "native.source-unit-ownership.v1",
}


class AdmissionError(Exception):
    def __init__(self, code: str, message: str, *, path: str = "", extra=None):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.path = path
        self.extra = extra or {}

    def as_dict(self):
        d = {"code": self.code, "message": self.message, "path": self.path}
        if self.extra:
            d["extra"] = self.extra
        return d


def _enc_str(s: str) -> str:
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\t":
            out.append("\\t")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\f":
            out.append("\\f")
        elif ch == "\r":
            out.append("\\r")
        elif o < 0x20:
            out.append(f"\\u{o:04x}")
        elif 0xD800 <= o <= 0xDFFF:
            raise AdmissionError("NON_SCALAR_UNICODE", f"surrogate U+{o:04X}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _encode(value: Any, depth: int) -> str:
    if depth > MAX_DEPTH:
        raise AdmissionError("NESTING_TOO_DEEP", str(depth))
    if value is None:
        return "null"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        if value < I64_MIN or value > U64_MAX:
            raise AdmissionError("INTEGER_OUT_OF_RANGE", str(value))
        return str(value)
    if type(value) is str:
        return _enc_str(value)
    if type(value) is list:
        return "[" + ",".join(_encode(v, depth + 1) for v in value) + "]"
    if type(value) is dict:
        keys = list(value.keys())
        for k in keys:
            if type(k) is not str:
                raise AdmissionError("OBJECT_KEY_NOT_STRING", repr(k))
        keys.sort(key=lambda k: k.encode("utf-8"))
        return "{" + ",".join(_enc_str(k) + ":" + _encode(value[k], depth + 1) for k in keys) + "}"
    if type(value) is float:
        raise AdmissionError("FLOAT_FORBIDDEN", "float")
    raise AdmissionError("UNSUPPORTED_TYPE", type(value).__name__)


def C(value: Any) -> bytes:
    raw = _encode(value, 1).encode("utf-8")
    if len(raw) > MAX_BYTES:
        raise AdmissionError("DESCRIPTOR_TOO_LARGE", str(len(raw)))
    return raw


class RawAdmit:
    def __init__(self, raw: bytes):
        if not isinstance(raw, (bytes, bytearray)):
            raise AdmissionError("LEXICAL_NOT_BYTES", "not bytes")
        if len(raw) > MAX_BYTES:
            raise AdmissionError("DESCRIPTOR_TOO_LARGE", str(len(raw)))
        try:
            self.text = raw.decode("utf-8")
        except UnicodeDecodeError as e:
            raise AdmissionError("MALFORMED_UTF8", str(e)) from e
        if self.text.startswith("\ufeff"):
            raise AdmissionError("BOM_FORBIDDEN", "BOM")
        self.s = self.text
        self.n = len(self.s)
        self.i = 0

    def peek(self) -> str:
        return self.s[self.i] if self.i < self.n else ""

    def skip_ws(self) -> None:
        while self.i < self.n and self.s[self.i] in " \t\n\r":
            self.i += 1

    def parse(self) -> Any:
        v = self._value(1)
        self.skip_ws()
        if self.i != self.n:
            raise AdmissionError("TRAILING_JUNK", str(self.i))
        return v

    def _value(self, depth: int) -> Any:
        if depth > MAX_DEPTH:
            raise AdmissionError("NESTING_TOO_DEEP", str(depth))
        self.skip_ws()
        if self.i >= self.n:
            raise AdmissionError("UNEXPECTED_EOF", "eof")
        c = self.s[self.i]
        if c == "{":
            return self._object(depth)
        if c == "[":
            return self._array(depth)
        if c == '"':
            return self._string()
        if c == "t":
            return self._lit("true", True)
        if c == "f":
            return self._lit("false", False)
        if c == "n":
            return self._lit("null", None)
        if c == "-" or c.isdigit():
            return self._number()
        raise AdmissionError("UNEXPECTED_TOKEN", repr(c))

    def _lit(self, lit, val):
        if self.s.startswith(lit, self.i):
            self.i += len(lit)
            return val
        raise AdmissionError("UNEXPECTED_TOKEN", lit)

    def _object(self, depth):
        self.i += 1
        self.skip_ws()
        out = {}
        seen = set()
        if self.peek() == "}":
            self.i += 1
            return out
        while True:
            self.skip_ws()
            if self.peek() != '"':
                raise AdmissionError("OBJECT_KEY_NOT_STRING", str(self.i))
            key = self._string()
            if key in seen:
                raise AdmissionError("DUPLICATE_KEY", key)
            seen.add(key)
            self.skip_ws()
            if self.peek() != ":":
                raise AdmissionError("EXPECTED_COLON", str(self.i))
            self.i += 1
            out[key] = self._value(depth + 1)
            self.skip_ws()
            c = self.peek()
            if c == ",":
                self.i += 1
                continue
            if c == "}":
                self.i += 1
                return out
            raise AdmissionError("EXPECTED_COMMA_OR_END", str(self.i))

    def _array(self, depth):
        self.i += 1
        self.skip_ws()
        out = []
        if self.peek() == "]":
            self.i += 1
            return out
        while True:
            out.append(self._value(depth + 1))
            self.skip_ws()
            c = self.peek()
            if c == ",":
                self.i += 1
                continue
            if c == "]":
                self.i += 1
                return out
            raise AdmissionError("EXPECTED_COMMA_OR_END", str(self.i))

    def _string(self):
        if self.peek() != '"':
            raise AdmissionError("EXPECTED_STRING", str(self.i))
        self.i += 1
        chars = []
        while self.i < self.n:
            c = self.s[self.i]
            if c == '"':
                self.i += 1
                return "".join(chars)
            if c == "\\":
                self.i += 1
                chars.append(self._escape())
                continue
            o = ord(c)
            if o < 0x20:
                raise AdmissionError("UNESCAPED_CONTROL", hex(o))
            if 0xD800 <= o <= 0xDFFF:
                raise AdmissionError("NON_SCALAR_UNICODE", hex(o))
            chars.append(c)
            self.i += 1
        raise AdmissionError("UNTERMINATED_STRING", "")

    def _escape(self):
        if self.i >= self.n:
            raise AdmissionError("UNTERMINATED_STRING", "escape")
        c = self.s[self.i]
        self.i += 1
        table = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"}
        if c in table:
            return table[c]
        if c == "u":
            return self._u()
        raise AdmissionError("BAD_ESCAPE", c)

    def _hex4(self):
        if self.i + 4 > self.n:
            raise AdmissionError("BAD_UNICODE_ESCAPE", "trunc")
        h = self.s[self.i : self.i + 4]
        self.i += 4
        return int(h, 16)

    def _u(self):
        cp = self._hex4()
        if 0xD800 <= cp <= 0xDBFF:
            if self.i + 6 <= self.n and self.s[self.i : self.i + 2] == "\\u":
                self.i += 2
                low = self._hex4()
                if 0xDC00 <= low <= 0xDFFF:
                    return chr(0x10000 + ((cp - 0xD800) << 10) + (low - 0xDC00))
                raise AdmissionError("NON_SCALAR_UNICODE", "high not followed by low")
            raise AdmissionError("NON_SCALAR_UNICODE", "unpaired high")
        if 0xDC00 <= cp <= 0xDFFF:
            raise AdmissionError("NON_SCALAR_UNICODE", "unpaired low")
        return chr(cp)

    def _number(self):
        start = self.i
        if self.peek() == "-":
            self.i += 1
            if self.i >= self.n or not self.s[self.i].isdigit():
                raise AdmissionError("BAD_NUMBER", "lone minus")
        if self.s[self.i] == "0":
            self.i += 1
            if self.i < self.n and self.s[self.i].isdigit():
                raise AdmissionError("LEADING_ZERO", "")
        else:
            while self.i < self.n and self.s[self.i].isdigit():
                self.i += 1
        if self.i < self.n and self.s[self.i] == ".":
            raise AdmissionError("FLOAT_FORBIDDEN", "")
        if self.i < self.n and self.s[self.i] in "eE":
            raise AdmissionError("EXPONENT_FORBIDDEN", "")
        token = self.s[start : self.i]
        if token == "-0":
            raise AdmissionError("NEG_ZERO_FORBIDDEN", "")
        value = int(token, 10)
        if value < I64_MIN or value > U64_MAX:
            raise AdmissionError("INTEGER_OUT_OF_RANGE", str(value))
        return value


def admit_raw(raw: bytes) -> Any:
    return RawAdmit(raw).parse()


def h_preimage(domain: str, canonical_bytes: bytes) -> bytes:
    if "\x00" in domain:
        raise AdmissionError("DOMAIN_NUL", domain)
    return (
        PRODUCT_PREFIX
        + b"\x00"
        + domain.encode("ascii")
        + b"\x00"
        + len(canonical_bytes).to_bytes(8, "big")
        + canonical_bytes
    )


def H(domain: str, value: Any) -> str:
    cx = C(value)
    return hashlib.sha256(h_preimage(domain, cx)).hexdigest()


def h_frame(domain: str, value: Any) -> bytes:
    return h_preimage(domain, C(value))


def typed_id(domain: str, value: Any) -> str:
    prefix = DOMAIN_PREFIX.get(domain)
    if prefix is None:
        raise AdmissionError("UNKNOWN_DOMAIN", domain)
    return f"{prefix}:{H(domain, value)}"


def parse_h_frame(frame: bytes, *, allowed_domains: set[str] | None = None) -> dict:
    prefix = PRODUCT_PREFIX + b"\x00"
    if not frame.startswith(prefix):
        raise AdmissionError("H_FRAME_PREFIX", "")
    rest = frame[len(prefix) :]
    nul = rest.find(b"\x00")
    if nul < 0:
        raise AdmissionError("H_FRAME_DOMAIN", "")
    domain = rest[:nul].decode("ascii")
    if allowed_domains is not None and domain not in allowed_domains:
        raise AdmissionError("H_FRAME_DOMAIN_SET", domain)
    after = rest[nul + 1 :]
    if len(after) < 8:
        raise AdmissionError("H_FRAME_LENGTH", "")
    declared = int.from_bytes(after[:8], "big")
    payload = after[8:]
    if declared != len(payload):
        raise AdmissionError("H_FRAME_LENGTH_MISMATCH", f"{declared} vs {len(payload)}")
    parsed = admit_raw(payload)
    rec = C(parsed)
    if rec != payload:
        raise AdmissionError("H_FRAME_NOT_CANONICAL", domain)
    digest = hashlib.sha256(frame).hexdigest()
    return {"domain": domain, "value": parsed, "digest": digest, "canonicalBytes": payload}


# CVE1
TAG = {
    "null": 0x00,
    "false": 0x01,
    "true": 0x02,
    "unsigned-64": 0x03,
    "NFC-UTF8-string": 0x04,
    "array": 0x05,
    "string-keyed-map": 0x06,
    "negative-signed-64": 0x07,
}
CVE1_TYPES = (
    "null",
    "false",
    "true",
    "unsigned-64",
    "negative-signed-64",
    "NFC-UTF8-string",
    "array",
    "string-keyed-map",
)
MAX_NESTING = 64
MAX_COLLECTION = 1048576


def cve1_classify(value: Any) -> str:
    if value is None:
        return "null"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        if value >= 0:
            if value > U64_MAX:
                raise AdmissionError("CVE1_U64", str(value))
            return "unsigned-64"
        if value < I64_MIN:
            raise AdmissionError("CVE1_I64", str(value))
        return "negative-signed-64"
    if type(value) is str:
        return "NFC-UTF8-string"
    if type(value) is list:
        return "array"
    if type(value) is dict:
        return "string-keyed-map"
    if type(value) is float:
        raise AdmissionError("FLOAT_FORBIDDEN", "cve1")
    if type(value) is bytes:
        raise AdmissionError("BYTES_FORBIDDEN", "cve1")
    raise AdmissionError("CVE1_UNSUPPORTED", type(value).__name__)


def cve1_encode(value: Any, *, depth: int = 0) -> bytes:
    if depth > MAX_NESTING:
        raise AdmissionError("CVE1_NESTING", str(depth))
    kind = cve1_classify(value)
    if kind == "null":
        return b"\x00"
    if kind == "false":
        return b"\x01"
    if kind == "true":
        return b"\x02"
    if kind == "unsigned-64":
        return b"\x03" + value.to_bytes(8, "big", signed=False)
    if kind == "negative-signed-64":
        return b"\x07" + value.to_bytes(8, "big", signed=True)
    if kind == "NFC-UTF8-string":
        if unicodedata.normalize("NFC", value) != value:
            raise AdmissionError("NON_NFC_STRING", "")
        if "\x00" in value:
            raise AdmissionError("NUL_IN_STRING", "")
        raw = value.encode("utf-8")
        return b"\x04" + len(raw).to_bytes(4, "big") + raw
    if kind == "array":
        if len(value) > MAX_COLLECTION:
            raise AdmissionError("CVE1_COLLECTION", "array")
        return b"\x05" + len(value).to_bytes(4, "big") + b"".join(cve1_encode(el, depth=depth + 1) for el in value)
    if kind == "string-keyed-map":
        if len(value) > MAX_COLLECTION:
            raise AdmissionError("CVE1_COLLECTION", "map")
        keys = list(value.keys())
        for k in keys:
            if type(k) is not str:
                raise AdmissionError("CVE1_MAP_KEY", "")
            if unicodedata.normalize("NFC", k) != k:
                raise AdmissionError("NON_NFC_STRING", "key")
        encoded = sorted((k.encode("utf-8"), k) for k in keys)
        parts = [b"\x06", len(encoded).to_bytes(4, "big")]
        seen = set()
        for kb, k in encoded:
            if kb in seen:
                raise AdmissionError("DUPLICATE_KEY", k)
            seen.add(kb)
            parts.append(cve1_encode(k, depth=depth + 1))
            parts.append(cve1_encode(value[k], depth=depth + 1))
        return b"".join(parts)
    raise AdmissionError("CVE1_UNSUPPORTED", kind)


def cve1_decode(data: bytes) -> Any:
    class D:
        def __init__(self, data):
            self.data = data
            self.i = 0

        def need(self, n):
            if self.i + n > len(self.data):
                raise AdmissionError("CVE1_TRUNCATED", str(n))
            b = self.data[self.i : self.i + n]
            self.i += n
            return b

        def u32(self):
            return int.from_bytes(self.need(4), "big")

        def decode(self, depth=0):
            if depth > MAX_NESTING:
                raise AdmissionError("CVE1_NESTING", str(depth))
            tag = self.need(1)[0]
            if tag == 0x00:
                return None
            if tag == 0x01:
                return False
            if tag == 0x02:
                return True
            if tag == 0x03:
                return int.from_bytes(self.need(8), "big", signed=False)
            if tag == 0x07:
                return int.from_bytes(self.need(8), "big", signed=True)
            if tag == 0x04:
                n = self.u32()
                raw = self.need(n)
                s = raw.decode("utf-8")
                if unicodedata.normalize("NFC", s) != s:
                    raise AdmissionError("NON_NFC_STRING", "decoded")
                if "\x00" in s:
                    raise AdmissionError("NUL_IN_STRING", "")
                return s
            if tag == 0x05:
                count = self.u32()
                return [self.decode(depth + 1) for _ in range(count)]
            if tag == 0x06:
                count = self.u32()
                items = []
                prev = None
                seen = set()
                for _ in range(count):
                    k = self.decode(depth + 1)
                    if type(k) is not str:
                        raise AdmissionError("CVE1_MAP_KEY", "")
                    kb = k.encode("utf-8")
                    if kb in seen:
                        raise AdmissionError("DUPLICATE_KEY", k)
                    seen.add(kb)
                    if prev is not None and kb < prev:
                        raise AdmissionError("CVE1_MAP_UNSORTED", "")
                    prev = kb
                    v = self.decode(depth + 1)
                    items.append((k, v))
                return {k: v for k, v in items}
            raise AdmissionError("CVE1_UNKNOWN_TAG", hex(tag))

    d = D(bytes(data))
    v = d.decode()
    if d.i != len(d.data):
        raise AdmissionError("CVE1_TRAILING", str(len(d.data) - d.i))
    return v


def capability_manifest_id_from_bytes(committed: bytes) -> str:
    return hashlib.sha256(b"opensip.capability-manifest.v1\x00" + committed).hexdigest()


def hex_of(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    if value.startswith("sha256:"):
        rest = value[7:]
        if len(rest) == 64 and all(c in "0123456789abcdef" for c in rest):
            return rest
        return None
    if ":" in value:
        _, rest = value.split(":", 1)
        if len(rest) == 64 and all(c in "0123456789abcdef" for c in rest):
            return rest
        return None
    if len(value) == 64 and all(c in "0123456789abcdef" for c in value):
        return value
    return None


def sort_c(xs: list) -> list:
    return sorted(xs, key=lambda x: C(x))
