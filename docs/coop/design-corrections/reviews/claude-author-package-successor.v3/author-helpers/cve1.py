"""CVE1 encoder/decoder from resolved-inputs.v2.json#planIdContract.canonicalValueEncoding."""
from __future__ import annotations

import unicodedata
from typing import Any

TAG_NULL = 0x00
TAG_FALSE = 0x01
TAG_TRUE = 0x02
TAG_U64 = 0x03
TAG_STR = 0x04
TAG_ARR = 0x05
TAG_MAP = 0x06
TAG_I64 = 0x07

MAX_NESTING = 64
MAX_COLLECTION_ITEMS = 1048576
I64_MIN = -(2**63)
U64_MAX = 2**64 - 1


class Cve1Error(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _u8(n: int) -> bytes:
    return bytes([n])


def _u16be(n: int) -> bytes:
    return n.to_bytes(2, "big", signed=False)


def _u32be(n: int) -> bytes:
    return n.to_bytes(4, "big", signed=False)


def _u64be(n: int) -> bytes:
    return n.to_bytes(8, "big", signed=False)


def _i64be(n: int) -> bytes:
    return n.to_bytes(8, "big", signed=True)


def encode(value: Any, depth: int = 0) -> bytes:
    if depth > MAX_NESTING:
        raise Cve1Error("CVE1_NESTING", "nesting exceeds 64")
    t = type(value)
    if value is None:
        return _u8(TAG_NULL)
    if t is bool:
        return _u8(TAG_TRUE if value else TAG_FALSE)
    if t is int:
        if value < 0:
            if value < I64_MIN:
                raise Cve1Error("CVE1_INT_RANGE", "negative integer below i64")
            return _u8(TAG_I64) + _i64be(value)
        if value > U64_MAX:
            raise Cve1Error("CVE1_INT_RANGE", "unsigned integer above u64")
        return _u8(TAG_U64) + _u64be(value)
    if t is float:
        raise Cve1Error("CVE1_FLOAT", "Floating-point values and byte strings are forbidden")
    if t is str:
        nfc = unicodedata.normalize("NFC", value)
        if nfc != value:
            raise Cve1Error("CVE1_NFC", "Strings MUST already be Unicode NFC")
        raw = value.encode("utf-8")
        return _u8(TAG_STR) + _u32be(len(raw)) + raw
    if t is bytes:
        raise Cve1Error("CVE1_BYTES", "Floating-point values and byte strings are forbidden")
    if t is list:
        if len(value) > MAX_COLLECTION_ITEMS:
            raise Cve1Error("CVE1_COLLECTION", "array exceeds maxCollectionItems")
        out = [_u8(TAG_ARR), _u32be(len(value))]
        for item in value:
            out.append(encode(item, depth + 1))
        return b"".join(out)
    if t is dict:
        if len(value) > MAX_COLLECTION_ITEMS:
            raise Cve1Error("CVE1_COLLECTION", "map exceeds maxCollectionItems")
        keys = []
        seen = set()
        for k in value.keys():
            if type(k) is not str:
                raise Cve1Error("CVE1_MAP_KEY", "map keys must be strings")
            nfc = unicodedata.normalize("NFC", k)
            if nfc != k:
                raise Cve1Error("CVE1_NFC", "map keys MUST already be Unicode NFC")
            kb = k.encode("utf-8")
            if kb in seen:
                raise Cve1Error("CVE1_DUP_KEY", "duplicate map keys")
            seen.add(kb)
            keys.append((kb, k))
        keys.sort(key=lambda x: x[0])
        out = [_u8(TAG_MAP), _u32be(len(keys))]
        for kb, k in keys:
            out.append(encode(k, depth + 1))
            out.append(encode(value[k], depth + 1))
        return b"".join(out)
    raise Cve1Error("CVE1_TYPE", f"unsupported type {t}")


class _Cursor:
    def __init__(self, data: bytes):
        self.data = data
        self.i = 0

    def remaining(self) -> int:
        return len(self.data) - self.i

    def take(self, n: int) -> bytes:
        if self.remaining() < n:
            raise Cve1Error("CVE1_TRUNCATED", "truncated CVE1 value")
        b = self.data[self.i : self.i + n]
        self.i += n
        return b

    def u8(self) -> int:
        return self.take(1)[0]

    def u32(self) -> int:
        return int.from_bytes(self.take(4), "big", signed=False)


def _decode(cur: _Cursor, depth: int) -> Any:
    if depth > MAX_NESTING:
        raise Cve1Error("CVE1_NESTING", "nesting exceeds 64")
    tag = cur.u8()
    if tag == TAG_NULL:
        return None
    if tag == TAG_FALSE:
        return False
    if tag == TAG_TRUE:
        return True
    if tag == TAG_U64:
        n = int.from_bytes(cur.take(8), "big", signed=False)
        return n
    if tag == TAG_I64:
        n = int.from_bytes(cur.take(8), "big", signed=True)
        if n >= 0:
            raise Cve1Error("CVE1_I64_SIGN", "negative-signed-64 must be negative")
        return n
    if tag == TAG_STR:
        n = cur.u32()
        raw = cur.take(n)
        try:
            s = raw.decode("utf-8")
        except UnicodeDecodeError as e:
            raise Cve1Error("CVE1_UTF8", "malformed UTF-8") from e
        if unicodedata.normalize("NFC", s) != s:
            raise Cve1Error("CVE1_NFC", "decoded string is not NFC")
        return s
    if tag == TAG_ARR:
        n = cur.u32()
        if n > MAX_COLLECTION_ITEMS:
            raise Cve1Error("CVE1_COLLECTION", "array exceeds maxCollectionItems")
        return [_decode(cur, depth + 1) for _ in range(n)]
    if tag == TAG_MAP:
        n = cur.u32()
        if n > MAX_COLLECTION_ITEMS:
            raise Cve1Error("CVE1_COLLECTION", "map exceeds maxCollectionItems")
        out = {}
        prev_key_bytes = None
        for _ in range(n):
            k = _decode(cur, depth + 1)
            if type(k) is not str:
                raise Cve1Error("CVE1_MAP_KEY", "map key is not a string")
            kb = k.encode("utf-8")
            if prev_key_bytes is not None and kb <= prev_key_bytes:
                raise Cve1Error("CVE1_MAP_ORDER", "map keys not strictly ascending")
            prev_key_bytes = kb
            if kb in out:
                raise Cve1Error("CVE1_DUP_KEY", "duplicate map keys")
            v = _decode(cur, depth + 1)
            out[k] = v
        return out
    raise Cve1Error("CVE1_UNKNOWN_TAG", f"unknown tag {tag:#x}")


def decode(data: bytes) -> Any:
    cur = _Cursor(data)
    value = _decode(cur, 0)
    if cur.remaining() != 0:
        raise Cve1Error("CVE1_TRAILING", "trailing bytes after CVE1 value")
    return value


def type_name(value: Any) -> str:
    t = type(value)
    if value is None:
        return "null"
    if t is bool:
        return "true" if value else "false"
    if t is int:
        return "unsigned-64" if value >= 0 else "negative-signed-64"
    if t is str:
        return "NFC-UTF8-string"
    if t is list:
        return "array"
    if t is dict:
        return "string-keyed-map"
    return f"unsupported:{t}"


EIGHT_TYPES = (
    "null",
    "false",
    "true",
    "unsigned-64",
    "negative-signed-64",
    "NFC-UTF8-string",
    "array",
    "string-keyed-map",
)
