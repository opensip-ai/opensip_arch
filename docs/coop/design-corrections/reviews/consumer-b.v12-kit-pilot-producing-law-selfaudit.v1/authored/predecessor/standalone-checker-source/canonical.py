"""Product canonical encoder C, lexical admission, H, CVE1, metadata profile.

Derived from identity-and-evidence §3, admission-and-qualification §1,
resolved-inputs.v2#planIdContract.canonicalValueEncoding, and
security-and-lifecycle S2 / security-completion.v1 §2.1.
"""
from __future__ import annotations

import hashlib
import struct
import unicodedata
from typing import Any


PRODUCT_H_PREFIX = b"opensip.product.v1"
I64_MIN = -(2**63)
I64_MAX = 2**63 - 1
U64_MAX = 2**64 - 1
MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32


class AdmissionError(Exception):
    def __init__(self, code: str, message: str, citation: str, operands: dict | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.citation = citation
        self.operands = operands or {}

    def as_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "citation": self.citation,
            "operands": self.operands,
        }


def _utf8_strict(raw: bytes, citation: str) -> str:
    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as e:
        raise AdmissionError(
            "MALFORMED_UTF8",
            f"malformed UTF-8 at byte {e.start}",
            citation,
            {"start": e.start, "reason": str(e)},
        )


class JsonLexer:
    def __init__(self, text: str, citation: str):
        self.s = text
        self.i = 0
        self.n = len(text)
        self.citation = citation

    def peek(self) -> str:
        return self.s[self.i] if self.i < self.n else ""

    def skip_ws(self) -> None:
        # C forbids whitespace in canonical form, but lexical admission of
        # raw input still sees JSON tokens. Exported C(X) has no whitespace.
        while self.i < self.n and self.s[self.i] in " \t\n\r":
            self.i += 1

    def expect(self, ch: str) -> None:
        if self.peek() != ch:
            raise AdmissionError(
                "JSON_SYNTAX",
                f"expected {ch!r} at {self.i}, got {self.peek()!r}",
                self.citation,
                {"index": self.i},
            )
        self.i += 1

    def parse_string(self) -> str:
        self.expect('"')
        out: list[str] = []
        s, i, n = self.s, self.i, self.n
        while i < n:
            c = s[i]
            if c == '"':
                self.i = i + 1
                value = "".join(out)
                for ch in value:
                    o = ord(ch)
                    if 0xD800 <= o <= 0xDFFF:
                        raise AdmissionError(
                            "NON_SCALAR_UNICODE",
                            "lone surrogate in string",
                            self.citation,
                            {"codepoint": hex(o)},
                        )
                return value
            if c == "\\":
                if i + 1 >= n:
                    raise AdmissionError("JSON_SYNTAX", "truncated escape", self.citation, {"index": i})
                e = s[i + 1]
                if e == "u":
                    if i + 6 > n:
                        raise AdmissionError("JSON_SYNTAX", "truncated \\u escape", self.citation, {"index": i})
                    hexpart = s[i + 2 : i + 6]
                    if any(ch not in "0123456789abcdefABCDEF" for ch in hexpart):
                        raise AdmissionError("JSON_SYNTAX", "invalid \\u hex", self.citation, {"hex": hexpart})
                    cp = int(hexpart, 16)
                    if 0xD800 <= cp <= 0xDFFF:
                        raise AdmissionError(
                            "NON_SCALAR_UNICODE",
                            "lone surrogate \\u escape",
                            self.citation,
                            {"codepoint": hex(cp)},
                        )
                    out.append(chr(cp))
                    i += 6
                    continue
                mapping = {
                    '"': '"',
                    "\\": "\\",
                    "/": "/",
                    "b": "\b",
                    "f": "\f",
                    "n": "\n",
                    "r": "\r",
                    "t": "\t",
                }
                if e not in mapping:
                    raise AdmissionError("JSON_SYNTAX", f"invalid escape \\{e}", self.citation, {"index": i})
                out.append(mapping[e])
                i += 2
                continue
            if ord(c) < 0x20:
                raise AdmissionError(
                    "JSON_SYNTAX",
                    "unescaped control in string",
                    self.citation,
                    {"index": i, "ord": ord(c)},
                )
            out.append(c)
            i += 1
        raise AdmissionError("JSON_SYNTAX", "unterminated string", self.citation, {"index": self.i})

    def parse_number(self, profile: str) -> int:
        start = self.i
        s, i, n = self.s, self.i, self.n
        if s[i] == "-":
            i += 1
        if i >= n or s[i] not in "0123456789":
            raise AdmissionError("JSON_SYNTAX", "invalid number", self.citation, {"index": start})
        if s[i] == "0":
            i += 1
            if i < n and s[i] in "0123456789":
                raise AdmissionError(
                    "LEADING_ZERO",
                    "leading zero is not a shortest ordinary integer",
                    self.citation,
                    {"index": start, "token": s[start:i + 1]},
                )
        else:
            while i < n and s[i] in "0123456789":
                i += 1
        if i < n and s[i] in ".eE":
            raise AdmissionError(
                "FLOATING_OR_EXPONENT_TOKEN",
                "floating/exponent token refused before decode",
                self.citation,
                {"index": start, "token": s[start : min(n, i + 8)]},
            )
        token = s[start:i]
        if token == "-0":
            raise AdmissionError("NEG_ZERO", "-0 is refused", self.citation, {"index": start})
        self.i = i
        try:
            value = int(token, 10)
        except ValueError as e:
            raise AdmissionError("JSON_SYNTAX", f"invalid integer token {token!r}", self.citation, {}) from e
        if profile == "metadata":
            if value < I64_MIN or value > I64_MAX:
                raise AdmissionError(
                    "INTEGER_OUT_OF_RANGE",
                    "metadata integers are i64",
                    self.citation,
                    {"value": str(value)},
                )
        else:
            if value < I64_MIN or value > U64_MAX:
                raise AdmissionError(
                    "INTEGER_OUT_OF_RANGE",
                    "product integers are [-2^63, 2^64-1]",
                    self.citation,
                    {"value": str(value)},
                )
        return value

    def parse_literal(self, word: str, value: Any) -> Any:
        if self.s.startswith(word, self.i):
            self.i += len(word)
            return value
        raise AdmissionError("JSON_SYNTAX", f"expected {word}", self.citation, {"index": self.i})

    def parse_value(self, depth: int, profile: str) -> Any:
        self.skip_ws()
        c = self.peek()
        if c == "{":
            return self.parse_object(depth, profile)
        if c == "[":
            return self.parse_array(depth, profile)
        if c == '"':
            return self.parse_string()
        if c == "-" or c in "0123456789":
            return self.parse_number(profile)
        if c == "t":
            return self.parse_literal("true", True)
        if c == "f":
            return self.parse_literal("false", False)
        if c == "n":
            return self.parse_literal("null", None)
        raise AdmissionError("JSON_SYNTAX", f"unexpected {c!r}", self.citation, {"index": self.i})

    def parse_object(self, depth: int, profile: str) -> dict:
        if depth > MAX_DEPTH:
            raise AdmissionError("NESTING_DEPTH", "descriptor nesting exceeds 32", self.citation, {"depth": depth})
        self.expect("{")
        self.skip_ws()
        if self.peek() == "}":
            self.i += 1
            return {}
        out: dict[str, Any] = {}
        seen: set[str] = set()
        while True:
            self.skip_ws()
            if self.peek() != '"':
                raise AdmissionError("JSON_SYNTAX", "object key must be string", self.citation, {"index": self.i})
            key = self.parse_string()
            if key in seen:
                raise AdmissionError(
                    "DUPLICATE_KEY",
                    "duplicate object key refused before decode",
                    self.citation,
                    {"key": key},
                )
            seen.add(key)
            if profile == "metadata":
                if not unicodedata.is_normalized("NFC", key):
                    raise AdmissionError("NON_NFC_STRING", "metadata key is not NFC", self.citation, {"key": key})
            self.skip_ws()
            self.expect(":")
            value = self.parse_value(depth + 1, profile)
            out[key] = value
            self.skip_ws()
            if self.peek() == ",":
                self.i += 1
                continue
            if self.peek() == "}":
                self.i += 1
                return out
            raise AdmissionError("JSON_SYNTAX", "expected , or }", self.citation, {"index": self.i})

    def parse_array(self, depth: int, profile: str) -> list:
        if depth > MAX_DEPTH:
            raise AdmissionError("NESTING_DEPTH", "descriptor nesting exceeds 32", self.citation, {"depth": depth})
        self.expect("[")
        self.skip_ws()
        if self.peek() == "]":
            self.i += 1
            return []
        out: list[Any] = []
        while True:
            out.append(self.parse_value(depth + 1, profile))
            self.skip_ws()
            if self.peek() == ",":
                self.i += 1
                continue
            if self.peek() == "]":
                self.i += 1
                return out
            raise AdmissionError("JSON_SYNTAX", "expected , or ]", self.citation, {"index": self.i})


def admit_json_bytes(raw: bytes, *, profile: str = "product", citation: str = "identity-and-evidence.md§3") -> Any:
    if len(raw) > MAX_DESCRIPTOR_BYTES:
        raise AdmissionError(
            "DESCRIPTOR_TOO_LARGE",
            "descriptor exceeds 4 MiB",
            citation,
            {"bytes": len(raw)},
        )
    text = _utf8_strict(raw, citation)
    if "\ufffe" in text or "\uffff" in text:
        # noncharacters are scalars; allowed. Lone surrogates cannot appear in str.
        pass
    lexer = JsonLexer(text, citation)
    value = lexer.parse_value(1, profile)
    lexer.skip_ws()
    if lexer.i != lexer.n:
        raise AdmissionError(
            "TRAILING_BYTES",
            "trailing bytes after one JSON value",
            citation,
            {"index": lexer.i, "remaining": lexer.n - lexer.i},
        )
    if profile == "metadata":
        _require_nfc(value, citation)
    return value


def _require_nfc(value: Any, citation: str) -> None:
    if isinstance(value, str):
        if not unicodedata.is_normalized("NFC", value):
            raise AdmissionError("NON_NFC_STRING", "metadata string is not NFC", citation, {"value": value[:80]})
    elif isinstance(value, dict):
        for k, v in value.items():
            _require_nfc(k, citation)
            _require_nfc(v, citation)
    elif isinstance(value, list):
        for item in value:
            _require_nfc(item, citation)


def encode_c(value: Any, *, profile: str = "product") -> bytes:
    """Canonical JSON C (identity-and-evidence §3) or metadata profile (S2)."""
    out = bytearray()
    _encode(value, out, profile)
    return bytes(out)


def _encode(value: Any, out: bytearray, profile: str) -> None:
    if value is None:
        out.extend(b"null")
        return
    if value is True:
        out.extend(b"true")
        return
    if value is False:
        out.extend(b"false")
        return
    if isinstance(value, bool):
        out.extend(b"true" if value else b"false")
        return
    if isinstance(value, int) and not isinstance(value, bool):
        if profile == "metadata":
            if value < I64_MIN or value > I64_MAX:
                raise AdmissionError("INTEGER_OUT_OF_RANGE", "metadata i64 overflow", "security-and-lifecycle.md#S2", {"value": str(value)})
        else:
            if value < I64_MIN or value > U64_MAX:
                raise AdmissionError("INTEGER_OUT_OF_RANGE", "product integer overflow", "identity-and-evidence.md§3", {"value": str(value)})
        out.extend(str(value).encode("ascii"))
        return
    if isinstance(value, str):
        if profile == "metadata" and not unicodedata.is_normalized("NFC", value):
            raise AdmissionError("NON_NFC_STRING", "metadata encoder never normalizes", "security-completion.v1.md§2.1", {})
        out.extend(_encode_string(value))
        return
    if isinstance(value, list):
        out.append(ord("["))
        for i, item in enumerate(value):
            if i:
                out.append(ord(","))
            _encode(item, out, profile)
        out.append(ord("]"))
        return
    if isinstance(value, dict):
        keys = list(value.keys())
        if any(not isinstance(k, str) for k in keys):
            raise AdmissionError("NON_STRING_KEY", "object keys must be strings", "identity-and-evidence.md§3", {})
        keys.sort(key=lambda k: k.encode("utf-8"))
        out.append(ord("{"))
        for i, k in enumerate(keys):
            if i:
                out.append(ord(","))
            out.extend(_encode_string(k))
            out.append(ord(":"))
            _encode(value[k], out, profile)
        out.append(ord("}"))
        return
    raise AdmissionError(
        "NON_MODEL_LEAF",
        f"canonical encoder refuses {type(value).__name__}",
        "identity-and-evidence.md§3",
        {"type": type(value).__name__},
    )


def _encode_string(s: str) -> bytes:
    buf = bytearray()
    buf.append(ord('"'))
    for ch in s:
        o = ord(ch)
        if ch == '"':
            buf.extend(b'\\"')
        elif ch == "\\":
            buf.extend(b"\\\\")
        elif ch == "\b":
            buf.extend(b"\\b")
        elif ch == "\t":
            buf.extend(b"\\t")
        elif ch == "\n":
            buf.extend(b"\\n")
        elif ch == "\f":
            buf.extend(b"\\f")
        elif ch == "\r":
            buf.extend(b"\\r")
        elif o < 0x20:
            buf.extend(f"\\u{o:04x}".encode("ascii"))
        else:
            buf.extend(ch.encode("utf-8"))
    buf.append(ord('"'))
    return bytes(buf)


def h_identity(domain: str, descriptor: Any) -> tuple[str, bytes]:
    """H(D,X) and the exact framed preimage bytes.

    H(D,X) = SHA256(ASCII("opensip.product.v1") || 00 || ASCII(D) || 00 || uint64BE(len(C(X))) || C(X))
    """
    cx = encode_c(descriptor, profile="product")
    frame = (
        PRODUCT_H_PREFIX
        + b"\x00"
        + domain.encode("ascii")
        + b"\x00"
        + struct.pack(">Q", len(cx))
        + cx
    )
    digest = hashlib.sha256(frame).hexdigest()
    return digest, frame


def parse_h_frame(raw: bytes, *, expected_domain: str | None = None, expected_domains: set[str] | None = None) -> tuple[str, Any, bytes]:
    """Parse an H preimage frame. Returns (domain, parsed descriptor, C bytes)."""
    citation = "identity-and-evidence.md§3 (closing digest law / H frame)"
    prefix = PRODUCT_H_PREFIX + b"\x00"
    if not raw.startswith(prefix):
        raise AdmissionError(
            "H_FRAME_PREFIX",
            "frame does not begin with opensip.product.v1 NUL",
            citation,
            {"prefix": raw[:32].hex()},
        )
    rest = raw[len(prefix) :]
    z = rest.find(b"\x00")
    if z < 1:
        raise AdmissionError("H_FRAME_DOMAIN", "missing domain in H frame", citation, {})
    try:
        domain = rest[:z].decode("ascii")
    except UnicodeDecodeError as e:
        raise AdmissionError("H_FRAME_DOMAIN", "non-ASCII H domain", citation, {}) from e
    if expected_domain is not None and domain != expected_domain:
        raise AdmissionError(
            "H_FRAME_DOMAIN_MISMATCH",
            "H frame domain is not the annotation's domain",
            citation,
            {"actual": domain, "expected": expected_domain},
        )
    if expected_domains is not None and domain not in expected_domains:
        raise AdmissionError(
            "H_FRAME_DOMAIN_SET",
            "H frame domain is not a member of the annotation domain set",
            citation,
            {"actual": domain, "allowed": sorted(expected_domains)},
        )
    rest = rest[z + 1 :]
    if len(rest) < 8:
        raise AdmissionError("H_FRAME_LENGTH", "truncated uint64 length", citation, {})
    declared = struct.unpack(">Q", rest[:8])[0]
    payload = rest[8:]
    if declared != len(payload):
        raise AdmissionError(
            "H_FRAME_LENGTH_MISMATCH",
            "declared C length does not equal remaining byte count",
            citation,
            {"declared": declared, "remaining": len(payload)},
        )
    parsed = admit_json_bytes(payload, profile="product", citation=citation)
    recomputed = encode_c(parsed, profile="product")
    if recomputed != payload:
        raise AdmissionError(
            "C_BYTE_IDENTITY",
            "C(parse(payload)) is not byte-identical to the framed remainder",
            citation,
            {
                "declaredSha256": hashlib.sha256(payload).hexdigest(),
                "recomputedSha256": hashlib.sha256(recomputed).hexdigest(),
            },
        )
    return domain, parsed, payload


def sha256_hex(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


# --- CVE1 (capability-manifest committed bytes) ---

CVE1_NULL = 0x00
CVE1_FALSE = 0x01
CVE1_TRUE = 0x02
CVE1_U64 = 0x03
CVE1_NFC_STRING = 0x04
CVE1_ARRAY = 0x05
CVE1_MAP = 0x06
CVE1_I64NEG = 0x07


def encode_cve1(value: Any) -> bytes:
    """resolved-inputs.v2#planIdContract.canonicalValueEncoding eight closed types."""
    return _cve1(value, 0)


def _cve1(value: Any, depth: int) -> bytes:
    if depth > 64:
        raise AdmissionError("CVE1_NESTING", "CVE1 nesting exceeds 64", "resolved-inputs.v2.json#planIdContract.canonicalValueEncoding", {})
    if value is None:
        return bytes([CVE1_NULL])
    if value is False:
        return bytes([CVE1_FALSE])
    if value is True:
        return bytes([CVE1_TRUE])
    if isinstance(value, bool):
        return bytes([CVE1_TRUE if value else CVE1_FALSE])
    if isinstance(value, int) and not isinstance(value, bool):
        if 0 <= value <= U64_MAX:
            return bytes([CVE1_U64]) + struct.pack(">Q", value)
        if I64_MIN <= value < 0:
            return bytes([CVE1_I64NEG]) + struct.pack(">q", value)
        raise AdmissionError("CVE1_INTEGER", "integer outside CVE1 u64/i64", "resolved-inputs.v2.json#planIdContract.canonicalValueEncoding", {"value": str(value)})
    if isinstance(value, str):
        if not unicodedata.is_normalized("NFC", value):
            raise AdmissionError(
                "CVE1_NON_NFC",
                "CVE1 rejects non-NFC strings rather than normalising",
                "resolved-inputs.v2.json#planIdContract.canonicalValueEncoding",
                {"value": value[:80]},
            )
        b = value.encode("utf-8")
        return bytes([CVE1_NFC_STRING]) + struct.pack(">I", len(b)) + b
    if isinstance(value, list):
        parts = [bytes([CVE1_ARRAY]) + struct.pack(">I", len(value))]
        for item in value:
            parts.append(_cve1(item, depth + 1))
        return b"".join(parts)
    if isinstance(value, dict):
        items = []
        seen: set[bytes] = set()
        for k, v in value.items():
            if not isinstance(k, str):
                raise AdmissionError("CVE1_MAP_KEY", "map keys must be strings", "resolved-inputs.v2.json#planIdContract.canonicalValueEncoding", {})
            kb = _cve1(k, depth + 1)
            if kb in seen:
                raise AdmissionError("CVE1_DUPLICATE_KEY", "duplicate CVE1 map key", "resolved-inputs.v2.json#planIdContract.canonicalValueEncoding", {"key": k})
            seen.add(kb)
            items.append((k.encode("utf-8"), kb, _cve1(v, depth + 1)))
        items.sort(key=lambda t: t[0])  # unsigned lexicographic NFC UTF-8 key bytes
        parts = [bytes([CVE1_MAP]) + struct.pack(">I", len(items))]
        for _, kb, vb in items:
            parts.append(kb)
            parts.append(vb)
        return b"".join(parts)
    raise AdmissionError(
        "CVE1_FORBIDDEN_TYPE",
        f"floating-point and byte strings are forbidden; got {type(value).__name__}",
        "resolved-inputs.v2.json#planIdContract.canonicalValueEncoding",
        {"type": type(value).__name__},
    )


def capability_manifest_id(committed_bytes: bytes) -> str:
    """SHA256(UTF8("opensip.capability-manifest.v1") || 00 || committedBytes)."""
    return hashlib.sha256(b"opensip.capability-manifest.v1\x00" + committed_bytes).hexdigest()


def metadata_preimage_sha256(domain_tag: str, canonical_bytes: bytes) -> str:
    """security-completion.v1 §2.1 domain-separated digest."""
    return hashlib.sha256(domain_tag.encode("utf-8") + b"\x00" + canonical_bytes).hexdigest()
