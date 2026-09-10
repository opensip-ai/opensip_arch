"""CVE1 encoder/decoder from resolved-inputs.v2#planIdContract.canonicalValueEncoding.

Eight closed types. Exact class (never isinstance). Strings already NFC.
Maps unique keys, sorted by unsigned lexicographic NFC UTF-8 key bytes.
Floats and byte strings forbidden. Arrays preserve order (set semantics
are a field-specific pre-encoding step, not this encoder).
"""
from __future__ import annotations

import unicodedata
from typing import Any

from helper.errors import AdmissionError

I64_MIN = -9223372036854775808
I64_MAX = 9223372036854775807
U64_MAX = 18446744073709551615
MAX_NESTING = 64
MAX_COLLECTION_ITEMS = 1048576

CLOSED_TYPES = (
    "null",
    "false",
    "true",
    "unsigned-64",
    "negative-signed-64",
    "NFC-UTF8-string",
    "array",
    "string-keyed-map",
)

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


def _u32be(n: int) -> bytes:
    if n < 0 or n > 0xFFFFFFFF:
        raise AdmissionError("CVE1_LENGTH", f"u32 overflow {n}")
    return n.to_bytes(4, "big", signed=False)


def _u64be(n: int) -> bytes:
    if n < 0 or n > U64_MAX:
        raise AdmissionError("CVE1_U64", f"u64 overflow {n}")
    return n.to_bytes(8, "big", signed=False)


def _i64be(n: int) -> bytes:
    if n < I64_MIN or n > I64_MAX:
        raise AdmissionError("CVE1_I64", f"i64 overflow {n}")
    return n.to_bytes(8, "big", signed=True)


def classify(value: Any) -> str:
    if value is None:
        return "null"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        if value >= 0:
            if value > U64_MAX:
                raise AdmissionError("CVE1_U64", f"{value} exceeds unsigned-64")
            return "unsigned-64"
        if value < I64_MIN:
            raise AdmissionError("CVE1_I64", f"{value} below negative-signed-64")
        return "negative-signed-64"
    if type(value) is str:
        return "NFC-UTF8-string"
    if type(value) is list:
        return "array"
    if type(value) is dict:
        return "string-keyed-map"
    if type(value) is float:
        raise AdmissionError("FLOAT_FORBIDDEN", "Floating-point values and byte strings are forbidden")
    if type(value) is bytes:
        raise AdmissionError("BYTES_FORBIDDEN", "Floating-point values and byte strings are forbidden")
    raise AdmissionError("CVE1_UNSUPPORTED", f"not a closed CVE1 type: {type(value).__name__}")


def encode(value: Any, *, depth: int = 0) -> bytes:
    if depth > MAX_NESTING:
        raise AdmissionError("CVE1_NESTING", f"nesting {depth} exceeds {MAX_NESTING}")
    kind = classify(value)
    if kind == "null":
        return b"\x00"
    if kind == "false":
        return b"\x01"
    if kind == "true":
        return b"\x02"
    if kind == "unsigned-64":
        return b"\x03" + _u64be(value)
    if kind == "negative-signed-64":
        return b"\x07" + _i64be(value)
    if kind == "NFC-UTF8-string":
        if unicodedata.normalize("NFC", value) != value:
            raise AdmissionError("NON_NFC_STRING", "Strings MUST already be Unicode NFC; a non-NFC string is rejected rather than silently normalised.")
        if "\x00" in value:
            raise AdmissionError("NUL_IN_STRING", "U+0000 forbidden in CVE1 text")
        raw = value.encode("utf-8")
        return b"\x04" + _u32be(len(raw)) + raw
    if kind == "array":
        if len(value) > MAX_COLLECTION_ITEMS:
            raise AdmissionError("CVE1_COLLECTION", "array too large")
        parts = [b"\x05", _u32be(len(value))]
        for el in value:
            parts.append(encode(el, depth=depth + 1))
        return b"".join(parts)
    if kind == "string-keyed-map":
        if len(value) > MAX_COLLECTION_ITEMS:
            raise AdmissionError("CVE1_COLLECTION", "map too large")
        keys = list(value.keys())
        for k in keys:
            if type(k) is not str:
                raise AdmissionError("CVE1_MAP_KEY", "Map keys are unique strings")
            if unicodedata.normalize("NFC", k) != k:
                raise AdmissionError("NON_NFC_STRING", "map key is not NFC")
        # duplicate keys cannot exist in a Python dict; still reject if encoded keys collide
        encoded_keys = [(k.encode("utf-8"), k) for k in keys]
        encoded_keys.sort(key=lambda t: t[0])  # unsigned lexicographic UTF-8 bytes
        # uniqueness of UTF-8 bytes
        seen = set()
        parts = [b"\x06", _u32be(len(encoded_keys))]
        for kb, k in encoded_keys:
            if kb in seen:
                raise AdmissionError("DUPLICATE_KEY", "duplicate map keys rejected before encoding")
            seen.add(kb)
            parts.append(encode(k, depth=depth + 1))
            parts.append(encode(value[k], depth=depth + 1))
        return b"".join(parts)
    raise AdmissionError("CVE1_UNSUPPORTED", kind)


class _Dec:
    def __init__(self, data: bytes):
        self.data = data
        self.i = 0

    def need(self, n: int) -> bytes:
        if self.i + n > len(self.data):
            raise AdmissionError("CVE1_TRUNCATED", f"need {n} bytes at {self.i}")
        b = self.data[self.i : self.i + n]
        self.i += n
        return b

    def u32(self) -> int:
        return int.from_bytes(self.need(4), "big", signed=False)

    def decode(self, depth: int = 0) -> Any:
        if depth > MAX_NESTING:
            raise AdmissionError("CVE1_NESTING", f"nesting {depth} exceeds {MAX_NESTING}")
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
            try:
                s = raw.decode("utf-8")
            except UnicodeDecodeError as e:
                raise AdmissionError("MALFORMED_UTF8", str(e)) from e
            if unicodedata.normalize("NFC", s) != s:
                raise AdmissionError("NON_NFC_STRING", "decoded string is not NFC")
            if "\x00" in s:
                raise AdmissionError("NUL_IN_STRING", "U+0000 forbidden")
            return s
        if tag == 0x05:
            count = self.u32()
            if count > MAX_COLLECTION_ITEMS:
                raise AdmissionError("CVE1_COLLECTION", "array too large")
            return [self.decode(depth + 1) for _ in range(count)]
        if tag == 0x06:
            count = self.u32()
            if count > MAX_COLLECTION_ITEMS:
                raise AdmissionError("CVE1_COLLECTION", "map too large")
            items = []
            prev_key_bytes = None
            seen = set()
            for _ in range(count):
                k = self.decode(depth + 1)
                if type(k) is not str:
                    raise AdmissionError("CVE1_MAP_KEY", "map key not string")
                kb = k.encode("utf-8")
                if kb in seen:
                    raise AdmissionError("DUPLICATE_KEY", "duplicate map keys")
                seen.add(kb)
                if prev_key_bytes is not None and kb < prev_key_bytes:
                    raise AdmissionError("CVE1_MAP_UNSORTED", "map keys not sorted")
                if prev_key_bytes is not None and kb == prev_key_bytes:
                    raise AdmissionError("DUPLICATE_KEY", "duplicate map keys")
                prev_key_bytes = kb
                v = self.decode(depth + 1)
                items.append((k, v))
            return {k: v for k, v in items}
        raise AdmissionError("CVE1_UNKNOWN_TAG", f"unknown tag 0x{tag:02x}")


def decode(data: bytes) -> Any:
    if not isinstance(data, (bytes, bytearray)):
        raise AdmissionError("CVE1_NOT_BYTES", "decode requires bytes")
    d = _Dec(bytes(data))
    value = d.decode()
    if d.i != len(d.data):
        raise AdmissionError("CVE1_TRAILING", f"trailing {len(d.data) - d.i} bytes")
    return value


def round_trip(value: Any) -> dict:
    raw = encode(value)
    back = decode(raw)
    re = encode(back)
    return {
        "type": classify(value),
        "committedBytesHex": raw.hex(),
        "byteLength": len(raw),
        "decodedEquals": back == value and type(back) is type(value) or _deep_eq(back, value),
        "reencodeEquals": re == raw,
        "decoded": back if not isinstance(back, (bytes, bytearray)) else back.hex(),
    }


def _deep_eq(a: Any, b: Any) -> bool:
    if type(a) is not type(b) and not (type(a) is int and type(b) is int):
        # bool is not int here because we used type()
        if type(a) is bool or type(b) is bool:
            return a is b
    if type(a) is dict:
        if type(b) is not dict or a.keys() != b.keys():
            return False
        return all(_deep_eq(a[k], b[k]) for k in a)
    if type(a) is list:
        if type(b) is not list or len(a) != len(b):
            return False
        return all(_deep_eq(x, y) for x, y in zip(a, b))
    return a == b
