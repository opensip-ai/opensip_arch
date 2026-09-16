"""Reference-check CBOR codec and carrier interpreter for wire-carriers.v1.json.

Test scaffolding for the AUTHOR candidate: it checks that the declarative input is interpretable and that sample
payloads admit or refuse as stated. It is NOT a production wire decoder and does not implement joins beyond the
shape declared in the carrier input.
"""
import re
import unicodedata


class Refuse(Exception):
    def __init__(self, code, where=""):
        super().__init__(code + (":" + where if where else ""))
        self.code = code


def _head(major, n):
    if n < 24:
        return bytes([major << 5 | n])
    for ai, size in ((24, 1), (25, 2), (26, 4), (27, 8)):
        if n < 1 << (8 * size):
            return bytes([major << 5 | ai]) + n.to_bytes(size, "big")
    raise Refuse("INT_RANGE")


def encode(v):
    if v is None:
        return b"\xf6"
    if v is True:
        return b"\xf5"
    if v is False:
        return b"\xf4"
    if isinstance(v, int):
        return _head(0, v) if v >= 0 else _head(1, -1 - v)
    if isinstance(v, (bytes, bytearray)):
        return _head(2, len(v)) + bytes(v)
    if isinstance(v, str):
        b = v.encode("utf-8")
        return _head(3, len(b)) + b
    if isinstance(v, list):
        return _head(4, len(v)) + b"".join(encode(x) for x in v)
    if isinstance(v, dict):
        items = sorted(((encode(k), encode(x)) for k, x in v.items()), key=lambda kv: kv[0])
        return _head(5, len(items)) + b"".join(k + x for k, x in items)
    raise Refuse("UNENCODABLE", type(v).__name__)


def decode(data, profile):
    """Decode one item under a profile ('ts2-cbor' or 'rust3-cbor'), refusing every non-canonical form."""
    pos = 0

    def arg(ai):
        nonlocal pos
        if ai < 24:
            return ai
        if ai > 27:
            raise Refuse("INDEFINITE_OR_RESERVED")
        size = 1 << (ai - 24)
        if pos + size > len(data):
            raise Refuse("TRUNCATED")
        n = int.from_bytes(data[pos:pos + size], "big")
        pos += size
        if (ai == 24 and n < 24) or (ai > 24 and n < 1 << (8 * (size // 2))):
            raise Refuse("NON_SHORTEST")
        return n

    def item():
        nonlocal pos
        if pos >= len(data):
            raise Refuse("TRUNCATED")
        ib = data[pos]
        pos += 1
        major, ai = ib >> 5, ib & 31
        if major == 7:
            if ai == 20:
                return False
            if ai == 21:
                return True
            if ai == 22:
                return None
            raise Refuse("FLOAT_OR_SIMPLE")
        if major == 6:
            raise Refuse("TAG")
        n = arg(ai)
        if major == 0:
            return n
        if major == 1:
            if profile == "rust3-cbor":
                raise Refuse("NEGATIVE_INTEGER_FORBIDDEN")
            if n > (1 << 63) - 1:
                raise Refuse("INT_RANGE")
            return -1 - n
        if major in (2, 3):
            if pos + n > len(data):
                raise Refuse("TRUNCATED")
            raw = data[pos:pos + n]
            pos += n
            if major == 2:
                return bytes(raw)
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                raise Refuse("INVALID_UTF8")
            if unicodedata.normalize("NFC", text) != text:
                raise Refuse("NON_NFC")
            return text
        if major == 4:
            return [item() for _ in range(n)]
        out, prev = {}, None
        for _ in range(n):
            start = pos
            k = item()
            kraw = bytes(data[start:pos])
            if not isinstance(k, str):
                raise Refuse("NON_TEXT_KEY")
            if prev is not None and kraw <= prev:
                raise Refuse("DUPLICATE_KEY" if kraw == prev else "MAP_ORDER")
            prev = kraw
            out[k] = item()
        return out

    value = item()
    if pos != len(data):
        raise Refuse("TRAILING_BYTES")
    if encode(value) != bytes(data):
        raise Refuse("REENCODE_MISMATCH")
    return value


CVE1_TAGS = {"null": b"\x00", False: b"\x01", True: b"\x02"}


def cve1(v):
    if v is None:
        return b"\x00"
    if v is False:
        return b"\x01"
    if v is True:
        return b"\x02"
    if isinstance(v, int):
        return b"\x03" + v.to_bytes(8, "big") if v >= 0 else b"\x07" + v.to_bytes(8, "big", signed=True)
    if isinstance(v, str):
        b = v.encode("utf-8")
        return b"\x04" + len(b).to_bytes(4, "big") + b
    if isinstance(v, list):
        return b"\x05" + len(v).to_bytes(4, "big") + b"".join(cve1(x) for x in v)
    if isinstance(v, dict):
        keys = sorted(v, key=lambda k: k.encode("utf-8"))
        return b"\x06" + len(v).to_bytes(4, "big") + b"".join(cve1(k) + cve1(v[k]) for k in keys)
    raise Refuse("CVE1_UNENCODABLE")


class Carriers:
    """Interprets the declarative input. `extern_validate(generatedType, value)` is supplied by the caller."""

    def __init__(self, doc, extern_validate):
        self.doc = doc
        self.types = dict(doc["scalars"])
        self.records = doc["records"]
        self.extern_validate = extern_validate

    def check(self, t, v, where):
        k = t["t"]
        if k == "ref":
            name = t["ref"]
            if name in self.types:
                return self.check(self.types[name]["type"], v, where)
            return self.check_record(name, v, where)
        if k == "extern":
            return self.extern_validate(t["generatedType"], v, where)
        if k == "frame-payload":
            if not isinstance(v, dict):
                raise Refuse("TYPE_MAP", where)
            return
        if k == "nullable":
            return None if v is None else self.check(t["of"], v, where)
        if k == "null":
            if v is not None:
                raise Refuse("TYPE_NULL", where)
            return
        if k == "bool":
            if not isinstance(v, bool):
                raise Refuse("TYPE_BOOL", where)
            if "const" in t and v != t["const"]:
                raise Refuse("CONST", where)
            return
        if k == "uint64":
            if not isinstance(v, int) or isinstance(v, bool) or v < 0 or v > 18446744073709551615:
                raise Refuse("TYPE_UINT64", where)
            if "const" in t and v != int(t["const"]):
                raise Refuse("CONST", where)
            if "min" in t and v < int(t["min"]) or "max" in t and v > int(t["max"]):
                raise Refuse("UINT_BOUND", where)
            return
        if k == "text":
            if not isinstance(v, str):
                raise Refuse("TYPE_TEXT", where)
            if unicodedata.normalize("NFC", v) != v:
                raise Refuse("NON_NFC", where)
            n = len(v)
            if "minScalars" in t and n < int(t["minScalars"]) or "maxScalars" in t and n > int(t["maxScalars"]):
                raise Refuse("TEXT_SCALARS", where)
            if "maxUtf8Bytes" in t and len(v.encode("utf-8")) > int(t["maxUtf8Bytes"]):
                raise Refuse("TEXT_UTF8_BYTES", where)
            if t.get("forbidC0C1") and any(ord(c) < 0x20 or 0x80 <= ord(c) <= 0x9F for c in v):
                raise Refuse("TEXT_CONTROL", where)
            if "pattern" in t and not re.search(t["pattern"], v):
                raise Refuse("TEXT_PATTERN", where)
            if "enum" in t and v not in t["enum"]:
                raise Refuse("ENUM", where)
            if "const" in t and v != t["const"]:
                raise Refuse("CONST", where)
            return
        if k == "bytes":
            if not isinstance(v, bytes):
                raise Refuse("TYPE_BYTES", where)
            if len(v) < int(t["minBytes"]) or len(v) > int(t["maxBytes"]):
                raise Refuse("BYTES_BOUND", where)
            return
        if k == "array":
            if not isinstance(v, list):
                raise Refuse("TYPE_ARRAY", where)
            if len(v) < int(t["minItems"]) or "maxItems" in t and len(v) > int(t["maxItems"]):
                raise Refuse("ARRAY_BOUND", where)
            for i, x in enumerate(v):
                self.check(t["items"], x, f"{where}[{i}]")
            return
        raise Refuse("UNKNOWN_TYPE_KIND", k)

    def check_record(self, name, v, where=None):
        where = where or name
        r = self.records[name]
        if r["kind"] == "alias":
            return self.check(r["target"], v, where)
        if not isinstance(v, dict):
            raise Refuse("TYPE_MAP", where)
        if r["kind"] == "record":
            spec = {m["name"]: m for m in r["members"]}
            for key in v:
                if key not in spec:
                    raise Refuse("UNKNOWN_MEMBER", f"{where}.{key}")
            for m in r["members"]:
                if m["name"] not in v:
                    if m["presence"] == "required":
                        raise Refuse("MISSING_MEMBER", f"{where}.{m['name']}")
                    continue
                self.check(m["type"], v[m["name"]], f"{where}.{m['name']}")
            return
        disc = v.get(r["discriminator"])
        if disc not in r["variants"]:
            raise Refuse("VARIANT", where)
        if set(v) != set(r["memberOrder"]):
            raise Refuse("VARIANT_MEMBERS", where)
        for key, t in r["variants"][disc].items():
            self.check(t, v[key], f"{where}.{key}")

    def frame_payload(self, protocol, frame_type, value, selector=None):
        for f in self.doc["protocols"][protocol]["frames"]:
            if f["frameType"] == frame_type:
                p = f["payload"]
                if "select" in p:
                    if selector not in p["alternatives"]:
                        raise Refuse("SELECTOR_UNLAWFUL", frame_type)
                    p = p["alternatives"][selector]
                return self.check(p, value, frame_type)
        raise Refuse("UNKNOWN_FRAME", frame_type)
