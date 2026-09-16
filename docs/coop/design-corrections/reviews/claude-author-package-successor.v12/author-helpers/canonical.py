"""Product canonical JSON C from identity-and-evidence §3.

C never sorts, deduplicates, or infers array semantics. Keys are UTF-8
byte-ordered. No Unicode normalization. Shortest ordinary decimal integers.
"""
from __future__ import annotations

from typing import Any

I64_MIN = -(2**63)
U64_MAX = 2**64 - 1
MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32  # root container counts as 1


class CanonicalError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _escape_string(s: str) -> str:
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
        elif 0 <= o <= 0x1F:
            out.append(f"\\u{o:04x}")
        else:
            # U+007F and U+2028 remain unescaped; slash unescaped.
            out.append(ch)
    out.append('"')
    return "".join(out)


def _encode(value: Any, depth: int) -> str:
    t = type(value)
    if value is None:
        return "null"
    if t is bool:
        return "true" if value else "false"
    if t is int:
        if value < I64_MIN or value > U64_MAX:
            raise CanonicalError("C_INT_RANGE", "integer outside [-2^63, 2^64-1]")
        if value == 0:
            return "0"
        return str(value)
    if t is float:
        raise CanonicalError("C_FLOAT", "floating-point forbidden in C")
    if t is str:
        return _escape_string(value)
    if t is list:
        if depth > MAX_DEPTH:
            raise CanonicalError("C_DEPTH", "nesting depth exceeds 32")
        parts = [_encode(item, depth + 1) for item in value]
        return "[" + ",".join(parts) + "]"
    if t is dict:
        if depth > MAX_DEPTH:
            raise CanonicalError("C_DEPTH", "nesting depth exceeds 32")
        items = []
        for k in value.keys():
            if type(k) is not str:
                raise CanonicalError("C_KEY", "object keys must be strings")
            items.append((k.encode("utf-8"), k))
        items.sort(key=lambda x: x[0])
        # duplicate keys cannot exist in a Python dict; lexical admission
        # handles raw duplicate keys before parse.
        parts = []
        for _kb, k in items:
            parts.append(_escape_string(k) + ":" + _encode(value[k], depth + 1))
        return "{" + ",".join(parts) + "}"
    raise CanonicalError("C_TYPE", f"unsupported type {t}")


def encode(value: Any) -> bytes:
    """Return C(X) as UTF-8 bytes: no whitespace, no trailing newline."""
    t = type(value)
    depth = 1 if t in (list, dict) else 0
    s = _encode(value, depth)
    b = s.encode("utf-8")
    if len(b) > MAX_DESCRIPTOR_BYTES:
        raise CanonicalError("C_SIZE", "descriptor exceeds 4 MiB")
    return b


def sha256_c(value: Any) -> str:
    import hashlib

    return hashlib.sha256(encode(value)).hexdigest()
