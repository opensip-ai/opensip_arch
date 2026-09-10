"""Independent C (canonical JSON) and H identity from identity-and-evidence §3.

Not copied from author code. Built from product-v1/identity-and-evidence.md
and admission-and-qualification.md lexical rules.
"""
from __future__ import annotations

import hashlib
import unicodedata
from typing import Any

PRODUCT_PREFIX = b"opensip.product.v1"
MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32
INT_MIN = -(2**63)
INT_MAX = (2**64) - 1

H_PREFIX = {
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


class AdmissionError(Exception):
    def __init__(self, code: str, message: str, *, path: str = "$") -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.path = path


def _utf8_scalar_string(s: str) -> None:
    for ch in s:
        cp = ord(ch)
        if 0xD800 <= cp <= 0xDFFF:
            raise AdmissionError("NON_SCALAR_UNICODE", "surrogate scalar forbidden")


def encode_c_string(s: str) -> bytes:
    _utf8_scalar_string(s)
    out = bytearray()
    out.append(0x22)
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.extend(b'\\"')
        elif ch == "\\":
            out.extend(b"\\\\")
        elif o == 0x08:
            out.extend(b"\\b")
        elif o == 0x09:
            out.extend(b"\\t")
        elif o == 0x0A:
            out.extend(b"\\n")
        elif o == 0x0C:
            out.extend(b"\\f")
        elif o == 0x0D:
            out.extend(b"\\r")
        elif o < 0x20:
            out.extend(f"\\u{o:04x}".encode("ascii"))
        else:
            out.extend(ch.encode("utf-8"))
    out.append(0x22)
    return bytes(out)


def encode_c_int(n: int) -> bytes:
    if type(n) is not int:
        raise AdmissionError("INTEGER_TYPE", "integer required; bool is not an integer")
    if n < INT_MIN or n > INT_MAX:
        raise AdmissionError("INTEGER_OUT_OF_RANGE", f"integer {n} outside [-2^63, 2^64-1]")
    return str(n).encode("ascii")


def canonical_json(value: Any, *, depth: int = 0) -> bytes:
    """C(X): UTF-8, sorted object keys, no whitespace, no trailing newline, no NFC."""
    t = type(value)
    if value is None:
        return b"null"
    if t is bool:
        return b"true" if value else b"false"
    if t is int:
        return encode_c_int(value)
    if t is float:
        raise AdmissionError("FLOAT_FORBIDDEN", "floating-point values are forbidden")
    if t is str:
        return encode_c_string(value)
    if t is list:
        if depth + 1 > MAX_DEPTH:
            raise AdmissionError("NESTING_DEPTH", "nesting depth exceeds 32")
        parts = [b"["]
        for i, item in enumerate(value):
            if i:
                parts.append(b",")
            parts.append(canonical_json(item, depth=depth + 1))
        parts.append(b"]")
        return b"".join(parts)
    if t is dict:
        if depth + 1 > MAX_DEPTH:
            raise AdmissionError("NESTING_DEPTH", "nesting depth exceeds 32")
        for k in value:
            if type(k) is not str:
                raise AdmissionError("NON_STRING_KEY", "object keys must be strings")
        keys = sorted(value.keys(), key=lambda k: k.encode("utf-8"))
        parts = [b"{"]
        for i, k in enumerate(keys):
            if i:
                parts.append(b",")
            parts.append(encode_c_string(k))
            parts.append(b":")
            parts.append(canonical_json(value[k], depth=depth + 1))
        parts.append(b"}")
        return b"".join(parts)
    raise AdmissionError("UNSUPPORTED_TYPE", f"cannot encode {t.__name__}")


def C(value: Any) -> bytes:
    encoded = canonical_json(value)
    if len(encoded) > MAX_DESCRIPTOR_BYTES:
        raise AdmissionError("DESCRIPTOR_TOO_LARGE", f"{len(encoded)} bytes exceeds 4 MiB")
    return encoded


def H_frame(domain: str, descriptor: Any) -> bytes:
    if "\x00" in domain:
        raise AdmissionError("DOMAIN_NUL", "domain must not contain NUL")
    cx = C(descriptor)
    return (
        PRODUCT_PREFIX
        + b"\x00"
        + domain.encode("ascii")
        + b"\x00"
        + len(cx).to_bytes(8, "big")
        + cx
    )


def H_digest(domain: str, descriptor: Any) -> str:
    return hashlib.sha256(H_frame(domain, descriptor)).hexdigest()


def H_id(domain: str, descriptor: Any) -> str:
    prefix = H_PREFIX.get(domain)
    if prefix is None:
        raise AdmissionError("UNKNOWN_H_DOMAIN", f"no product prefix for domain {domain}")
    return f"{prefix}:{H_digest(domain, descriptor)}"


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_h_frame(frame: bytes) -> tuple[str, bytes]:
    """Parse an H preimage frame. Returns (domain, C(X) bytes)."""
    if not frame.startswith(PRODUCT_PREFIX + b"\x00"):
        raise AdmissionError("H_FRAME_PREFIX", "frame does not start with opensip.product.v1 NUL")
    rest = frame[len(PRODUCT_PREFIX) + 1 :]
    nul = rest.find(b"\x00")
    if nul < 0:
        raise AdmissionError("H_FRAME_DOMAIN", "missing domain NUL")
    domain = rest[:nul].decode("ascii")
    rest = rest[nul + 1 :]
    if len(rest) < 8:
        raise AdmissionError("H_FRAME_LENGTH", "missing length")
    declared = int.from_bytes(rest[:8], "big")
    payload = rest[8:]
    if declared != len(payload):
        raise AdmissionError(
            "H_FRAME_LENGTH_MISMATCH",
            f"declared {declared} remaining {len(payload)}",
        )
    return domain, payload


# ---------------------------------------------------------------------------
# Lexical admission of raw JSON text (before object encode)
# ---------------------------------------------------------------------------

class RawJsonError(AdmissionError):
    pass


def _decode_utf8_strict(raw: bytes) -> str:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise RawJsonError("MALFORMED_UTF8", str(e)) from e
    _utf8_scalar_string(text)
    return text


class _Scanner:
    def __init__(self, text: str) -> None:
        self.s = text
        self.i = 0
        self.n = len(text)

    def peek(self) -> str:
        return self.s[self.i] if self.i < self.n else ""

    def get(self) -> str:
        ch = self.peek()
        self.i += 1
        return ch

    def skip_ws(self) -> None:
        while self.i < self.n and self.s[self.i] in " \t\r\n":
            self.i += 1


def admit_raw_json(raw: bytes, *, max_bytes: int = MAX_DESCRIPTOR_BYTES) -> Any:
    """Admit a JSON document from raw bytes with exact-integer / duplicate / string laws.

    This is distinct from encoding an already-parsed Python object.
    """
    if len(raw) > max_bytes:
        raise RawJsonError("DESCRIPTOR_TOO_LARGE", f"{len(raw)} bytes exceeds bound")
    text = _decode_utf8_strict(raw)
    sc = _Scanner(text)
    value = _parse_value(sc, depth=0)
    sc.skip_ws()
    if sc.i != sc.n:
        raise RawJsonError("TRAILING_BYTES", "trailing content after top-level value")
    return value


def _parse_value(sc: _Scanner, depth: int) -> Any:
    sc.skip_ws()
    ch = sc.peek()
    if ch == "":
        raise RawJsonError("UNEXPECTED_EOF", "unexpected end of input")
    if ch == "n":
        return _expect(sc, "null", None)
    if ch == "t":
        return _expect(sc, "true", True)
    if ch == "f":
        return _expect(sc, "false", False)
    if ch == '"':
        return _parse_string(sc)
    if ch == "[":
        return _parse_array(sc, depth)
    if ch == "{":
        return _parse_object(sc, depth)
    if ch == "-" or ch.isdigit():
        return _parse_integer(sc)
    raise RawJsonError("UNEXPECTED_TOKEN", f"unexpected {ch!r}")


def _expect(sc: _Scanner, lit: str, value: Any) -> Any:
    if sc.s[sc.i : sc.i + len(lit)] != lit:
        raise RawJsonError("UNEXPECTED_TOKEN", f"expected {lit}")
    sc.i += len(lit)
    return value


def _parse_integer(sc: _Scanner) -> int:
    start = sc.i
    if sc.peek() == "-":
        sc.get()
    if sc.peek() == "0":
        sc.get()
        # -0 or 0 followed by more digits / fraction / exponent is refused
        nxt = sc.peek()
        if nxt == "0" or nxt.isdigit():
            raise RawJsonError("LEADING_ZERO", "leading zeros forbidden")
        if nxt in ".eE":
            raise RawJsonError("NON_INTEGER_TOKEN", "floating/exponent token forbidden")
        token = sc.s[start : sc.i]
        if token == "-0":
            raise RawJsonError("NEGATIVE_ZERO", "-0 is refused")
        return 0
    if not sc.peek().isdigit():
        raise RawJsonError("INVALID_NUMBER", "expected digit")
    while sc.peek().isdigit():
        sc.get()
    nxt = sc.peek()
    if nxt in ".eE":
        raise RawJsonError("NON_INTEGER_TOKEN", "floating/exponent token forbidden")
    token = sc.s[start : sc.i]
    n = int(token)
    if n < INT_MIN or n > INT_MAX:
        raise RawJsonError("INTEGER_OUT_OF_RANGE", f"{token} outside range")
    return n


def _parse_string(sc: _Scanner) -> str:
    if sc.get() != '"':
        raise RawJsonError("EXPECTED_STRING", "expected quote")
    out: list[str] = []
    while True:
        ch = sc.get()
        if ch == "":
            raise RawJsonError("UNTERMINATED_STRING", "unterminated string")
        if ch == '"':
            return "".join(out)
        if ch == "\\":
            esc = sc.get()
            mapping = {
                '"': '"',
                "\\": "\\",
                "/": "/",
                "b": "\b",
                "t": "\t",
                "n": "\n",
                "f": "\f",
                "r": "\r",
            }
            if esc in mapping:
                out.append(mapping[esc])
                continue
            if esc == "u":
                hex4 = sc.s[sc.i : sc.i + 4]
                if len(hex4) < 4 or any(c not in "0123456789abcdefABCDEF" for c in hex4):
                    raise RawJsonError("INVALID_UNICODE_ESCAPE", "need 4 hex digits")
                sc.i += 4
                cp = int(hex4, 16)
                if 0xD800 <= cp <= 0xDFFF:
                    raise RawJsonError("NON_SCALAR_UNICODE", "surrogate escape forbidden")
                out.append(chr(cp))
                continue
            raise RawJsonError("INVALID_ESCAPE", f"invalid escape \\{esc}")
        if ord(ch) < 0x20:
            raise RawJsonError("UNESCAPED_CONTROL", "unescaped control in string")
        out.append(ch)


def _parse_array(sc: _Scanner, depth: int) -> list[Any]:
    if depth + 1 > MAX_DEPTH:
        raise RawJsonError("NESTING_DEPTH", "nesting depth exceeds 32")
    if sc.get() != "[":
        raise RawJsonError("EXPECTED_ARRAY", "expected [")
    sc.skip_ws()
    items: list[Any] = []
    if sc.peek() == "]":
        sc.get()
        return items
    while True:
        items.append(_parse_value(sc, depth + 1))
        sc.skip_ws()
        ch = sc.get()
        if ch == "]":
            return items
        if ch != ",":
            raise RawJsonError("EXPECTED_COMMA", "expected comma or ]")
        sc.skip_ws()


def _parse_object(sc: _Scanner, depth: int) -> dict[str, Any]:
    if depth + 1 > MAX_DEPTH:
        raise RawJsonError("NESTING_DEPTH", "nesting depth exceeds 32")
    if sc.get() != "{":
        raise RawJsonError("EXPECTED_OBJECT", "expected {")
    sc.skip_ws()
    obj: dict[str, Any] = {}
    if sc.peek() == "}":
        sc.get()
        return obj
    while True:
        sc.skip_ws()
        if sc.peek() != '"':
            raise RawJsonError("EXPECTED_KEY", "expected string key")
        key = _parse_string(sc)
        if key in obj:
            raise RawJsonError("DUPLICATE_KEY", f"duplicate key {key!r}")
        sc.skip_ws()
        if sc.get() != ":":
            raise RawJsonError("EXPECTED_COLON", "expected colon")
        obj[key] = _parse_value(sc, depth + 1)
        sc.skip_ws()
        ch = sc.get()
        if ch == "}":
            return obj
        if ch != ",":
            raise RawJsonError("EXPECTED_COMMA", "expected comma or }")
        sc.skip_ws()


def is_nfc(s: str) -> bool:
    return unicodedata.is_normalized("NFC", s)
