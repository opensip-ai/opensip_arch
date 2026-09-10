"""Product canonical JSON C from identity-and-evidence §3.

UTF-8 byte-ordered keys, no whitespace or trailing newline, no Unicode
normalization, shortest ordinary decimal integers, unescaped Unicode
scalars. Escape quote and backslash; use \\b\\t\\n\\f\\r; lowercase
\\u00xx for other U+0000–001F; do not escape slash. Arrays keep admitted
order. C never sorts, deduplicates or infers semantics from a field name.
"""
from __future__ import annotations

from typing import Any

from helper.errors import AdmissionError
from helper.lexical import I64_MIN, U64_MAX

MAX_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32


def _encode_string(s: str) -> str:
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
            raise AdmissionError("NON_SCALAR_UNICODE", f"surrogate U+{o:04X} in C string")
        else:
            # U+007F and U+2028 remain unescaped; slash unescaped.
            out.append(ch)
    out.append('"')
    return "".join(out)


def _encode(value: Any, depth: int) -> str:
    if depth > MAX_DEPTH:
        raise AdmissionError("NESTING_TOO_DEEP", f"nesting depth {depth} exceeds {MAX_DEPTH}")
    if value is None:
        return "null"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        if value < I64_MIN or value > U64_MAX:
            raise AdmissionError("INTEGER_OUT_OF_RANGE", f"{value} outside C integer range")
        return str(value)
    if type(value) is str:
        return _encode_string(value)
    if type(value) is list:
        parts = [_encode(v, depth + 1) for v in value]
        return "[" + ",".join(parts) + "]"
    if type(value) is dict:
        # UTF-8 byte-ordered keys. Duplicate keys cannot exist in a Python dict.
        keys = list(value.keys())
        for k in keys:
            if type(k) is not str:
                raise AdmissionError("OBJECT_KEY_NOT_STRING", f"non-string key {k!r}")
        keys.sort(key=lambda k: k.encode("utf-8"))
        parts = []
        for k in keys:
            parts.append(_encode_string(k) + ":" + _encode(value[k], depth + 1))
        return "{" + ",".join(parts) + "}"
    if type(value) is float:
        raise AdmissionError("FLOAT_FORBIDDEN", "floating-point values forbidden in C")
    if type(value) is bytes:
        raise AdmissionError("BYTES_FORBIDDEN", "byte strings forbidden in C; use canonical string form")
    raise AdmissionError("UNSUPPORTED_TYPE", f"cannot encode {type(value).__name__}")


def C(value: Any) -> bytes:
    """Canonical JSON bytes. No trailing newline, no BOM, no whitespace."""
    text = _encode(value, depth=1)
    raw = text.encode("utf-8")
    if len(raw) > MAX_BYTES:
        raise AdmissionError("DESCRIPTOR_TOO_LARGE", f"C(X) {len(raw)} exceeds 4 MiB")
    return raw


def C_hex(value: Any) -> str:
    return C(value).hex()
