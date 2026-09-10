"""CVE1 encoder/decoder from resolved-inputs.v2#planIdContract.canonicalValueEncoding.

Eight closed types. Independent of C (canonical JSON). Strings must already be NFC.
"""
from __future__ import annotations

import unicodedata
from typing import Any

from helpers.canonical import AdmissionError, INT_MIN

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

U64_MAX = (2**64) - 1
MAX_NESTING = 64
MAX_COLLECTION_ITEMS = 1048576


class Cve1Error(AdmissionError):
    pass


def encode(value: Any, *, depth: int = 0) -> bytes:
    if depth > MAX_NESTING:
        raise Cve1Error("CVE1_NESTING", "nesting exceeds 64")
    t = type(value)
    if value is None:
        return b"\x00"
    if t is bool:
        return b"\x02" if value else b"\x01"
    if t is int:
        if value < 0:
            if value < INT_MIN:
                raise Cve1Error("CVE1_INT_RANGE", "negative below i64")
            return b"\x07" + value.to_bytes(8, "big", signed=True)
        if value > U64_MAX:
            raise Cve1Error("CVE1_INT_RANGE", "unsigned above u64")
        return b"\x03" + value.to_bytes(8, "big", signed=False)
    if t is float:
        raise Cve1Error("CVE1_FLOAT", "float forbidden")
    if t is str:
        if not unicodedata.is_normalized("NFC", value):
            raise Cve1Error("CVE1_NON_NFC", "string is not Unicode NFC")
        if "\x00" in value:
            raise Cve1Error("CVE1_NUL_TEXT", "NUL in text forbidden")
        raw = value.encode("utf-8")
        return b"\x04" + len(raw).to_bytes(4, "big") + raw
    if t is list:
        if len(value) > MAX_COLLECTION_ITEMS:
            raise Cve1Error("CVE1_COLLECTION", "array too large")
        parts = [b"\x05", len(value).to_bytes(4, "big")]
        for item in value:
            parts.append(encode(item, depth=depth + 1))
        return b"".join(parts)
    if t is dict:
        if len(value) > MAX_COLLECTION_ITEMS:
            raise Cve1Error("CVE1_COLLECTION", "map too large")
        keys = []
        for k in value:
            if type(k) is not str:
                raise Cve1Error("CVE1_MAP_KEY", "map keys must be strings")
            if not unicodedata.is_normalized("NFC", k):
                raise Cve1Error("CVE1_NON_NFC", "map key is not NFC")
            keys.append(k)
        # duplicate keys cannot exist in a Python dict; still reject empty? uniqueness is structural
        keys_sorted = sorted(keys, key=lambda k: k.encode("utf-8"))
        # uniqueness of NFC UTF-8 bytes
        seen: set[bytes] = set()
        for k in keys_sorted:
            kb = k.encode("utf-8")
            if kb in seen:
                raise Cve1Error("CVE1_DUPLICATE_KEY", "duplicate map key")
            seen.add(kb)
        parts = [b"\x06", len(keys_sorted).to_bytes(4, "big")]
        for k in keys_sorted:
            parts.append(encode(k, depth=depth + 1))
            parts.append(encode(value[k], depth=depth + 1))
        return b"".join(parts)
    raise Cve1Error("CVE1_TYPE", f"unsupported type {t.__name__}")


def decode(data: bytes, *, depth: int = 0) -> Any:
    value, rest = _decode_one(data, depth)
    if rest:
        raise Cve1Error("CVE1_TRAILING", "trailing bytes after value")
    return value


def _decode_one(data: bytes, depth: int) -> tuple[Any, bytes]:
    if depth > MAX_NESTING:
        raise Cve1Error("CVE1_NESTING", "nesting exceeds 64")
    if not data:
        raise Cve1Error("CVE1_EOF", "unexpected end")
    tag = data[0]
    rest = data[1:]
    if tag == 0x00:
        return None, rest
    if tag == 0x01:
        return False, rest
    if tag == 0x02:
        return True, rest
    if tag == 0x03:
        if len(rest) < 8:
            raise Cve1Error("CVE1_EOF", "truncated unsigned-64")
        n = int.from_bytes(rest[:8], "big", signed=False)
        return n, rest[8:]
    if tag == 0x07:
        if len(rest) < 8:
            raise Cve1Error("CVE1_EOF", "truncated negative-signed-64")
        n = int.from_bytes(rest[:8], "big", signed=True)
        if n >= 0:
            raise Cve1Error("CVE1_NEGATIVE_TAG", "tag 07 requires negative i64")
        return n, rest[8:]
    if tag == 0x04:
        if len(rest) < 4:
            raise Cve1Error("CVE1_EOF", "truncated string length")
        n = int.from_bytes(rest[:4], "big")
        rest = rest[4:]
        if len(rest) < n:
            raise Cve1Error("CVE1_EOF", "truncated string")
        raw = rest[:n]
        rest = rest[n:]
        try:
            s = raw.decode("utf-8")
        except UnicodeDecodeError as e:
            raise Cve1Error("CVE1_UTF8", str(e)) from e
        if not unicodedata.is_normalized("NFC", s):
            raise Cve1Error("CVE1_NON_NFC", "decoded string is not NFC")
        return s, rest
    if tag == 0x05:
        if len(rest) < 4:
            raise Cve1Error("CVE1_EOF", "truncated array count")
        count = int.from_bytes(rest[:4], "big")
        rest = rest[4:]
        if count > MAX_COLLECTION_ITEMS:
            raise Cve1Error("CVE1_COLLECTION", "array too large")
        items = []
        for _ in range(count):
            item, rest = _decode_one(rest, depth + 1)
            items.append(item)
        return items, rest
    if tag == 0x06:
        if len(rest) < 4:
            raise Cve1Error("CVE1_EOF", "truncated map count")
        count = int.from_bytes(rest[:4], "big")
        rest = rest[4:]
        if count > MAX_COLLECTION_ITEMS:
            raise Cve1Error("CVE1_COLLECTION", "map too large")
        obj: dict[str, Any] = {}
        prev_key_bytes: bytes | None = None
        for _ in range(count):
            key, rest = _decode_one(rest, depth + 1)
            val, rest = _decode_one(rest, depth + 1)
            if type(key) is not str:
                raise Cve1Error("CVE1_MAP_KEY", "map key is not a string")
            kb = key.encode("utf-8")
            if prev_key_bytes is not None and kb <= prev_key_bytes:
                if kb == prev_key_bytes:
                    raise Cve1Error("CVE1_DUPLICATE_KEY", "duplicate map key")
                raise Cve1Error("CVE1_UNSORTED_MAP", "map keys not strictly ascending")
            prev_key_bytes = kb
            obj[key] = val
        return obj, rest
    raise Cve1Error("CVE1_UNKNOWN_TAG", f"unknown tag 0x{tag:02x}")


def round_trip(value: Any) -> dict[str, Any]:
    encoded = encode(value)
    decoded = decode(encoded)
    reencoded = encode(decoded)
    return {
        "encodedHex": encoded.hex(),
        "decoded": decoded,
        "reencodedHex": reencoded.hex(),
        "roundTripBytesEqual": encoded == reencoded,
        "valueEqual": decoded == value,
    }
