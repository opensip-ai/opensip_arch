"""Reference-check CBOR codec, carrier interpreter, document-driven lexical rules and ECMA-262 pattern translation for
wire-carriers.v1.json (candidate 03).

Test scaffolding for the AUTHOR candidate: it checks that the declarative input is interpretable and that sample
payloads admit or refuse as stated. It is NOT a production wire decoder and not production admission.
"""
import hashlib
import re
import unicodedata


class Refuse(Exception):
    def __init__(self, code, where=""):
        super().__init__(code + (":" + where if where else ""))
        self.code = code


class ByteLen:
    """A byte string represented only by its length, for exact accounting without materializing chunk bytes."""
    __slots__ = ("n",)

    def __init__(self, n):
        self.n = n


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
    if isinstance(v, ByteLen):
        raise Refuse("BYTELEN_NOT_ENCODABLE")
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


_DIGEST_INLINE = 1 << 16


def encoded_digest(v, exclude=()):
    """SHA-256 hex of the deterministic-CBOR encoding of v (top-level map members named in `exclude` removed), streamed
    into the hash; list/dict objects shared within one call are encoded once, so uniform manifests of hundreds of
    thousands of entries stay cheap. Byte-for-byte equal to hashlib.sha256(encode(v)).hexdigest()."""
    if exclude:
        v = {k: x for k, x in v.items() if k not in exclude}
    h, memo, lengths = hashlib.sha256(), {}, {}

    def feed(x):
        if isinstance(x, (list, dict)):
            hit = memo.get(id(x))
            if hit is not None and hit[0] is x:
                h.update(hit[1])
                return
            if encoded_length(x, lengths) <= _DIGEST_INLINE:
                b = encode(x)
                memo[id(x)] = (x, b)
                h.update(b)
                return
            if isinstance(x, list):
                h.update(_head(4, len(x)))
                for y in x:
                    feed(y)
            else:
                h.update(_head(5, len(x)))
                for kb, y in sorted(((encode(k), y) for k, y in x.items()), key=lambda kv: kv[0]):
                    h.update(kb)
                    feed(y)
        else:
            h.update(encode(x))
    feed(v)
    return h.hexdigest()


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


def _head_len(n):
    return 1 if n < 24 else 2 if n < 256 else 3 if n < 65536 else 5 if n < 1 << 32 else 9


def encoded_length(v, _memo=None):
    """Exact deterministic-CBOR length of v without materializing it. Shared list/dict objects are memoized by
    identity, so uniform accounting vectors of hundreds of thousands of entries stay cheap. The memo keeps a reference
    to every memoized object, so a transient object's id can never be reused by another object while the memo lives."""
    if _memo is None:
        _memo = {}
    if v is None or v is True or v is False:
        return 1
    if isinstance(v, ByteLen):
        return _head_len(v.n) + v.n
    if isinstance(v, int):
        return _head_len(v if v >= 0 else -1 - v)
    if isinstance(v, (bytes, bytearray)):
        return _head_len(len(v)) + len(v)
    if isinstance(v, str):
        n = len(v.encode("utf-8"))
        return _head_len(n) + n
    key = id(v)
    hit = _memo.get(key)
    if hit is not None and hit[0] is v:
        return hit[1]
    if isinstance(v, list):
        out = _head_len(len(v)) + sum(encoded_length(x, _memo) for x in v)
    elif isinstance(v, dict):
        out = _head_len(len(v)) + sum(encoded_length(k, _memo) + encoded_length(x, _memo) for k, x in v.items())
    else:
        raise Refuse("UNENCODABLE", type(v).__name__)
    _memo[key] = (v, out)
    return out


# ---------------------------------------------------------------- ECMA-262 pattern dialect (finite translation)
ECMA_WHITESPACE = "\t\n\u000b\u000c\r \u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000\ufeff"
ECMA_LINE_TERMINATORS = "\n\r\u2028\u2029"
_SUPPORTED_ESCAPES = set("\\/.^$|?*+()[]{}-") | {"u", "s", "S", "n", "r", "t"}


class UnsupportedPattern(Exception):
    pass


def _cls(chars):
    return "".join("\\u%04x" % ord(c) for c in chars)


def ecma_to_python(pattern, flags):
    """Translate an ECMA-262 pattern evaluated with RegExp(pattern, flags).test(s) into a Python `re.search` pattern
    with identical results, for the finite construct set this candidate's closure uses. Any construct outside that set
    raises UnsupportedPattern (never a silent pass). Differences handled: `.` (ECMA excludes all four line terminators
    unless `s`), `$` (ECMA end of input unless `m`; Python `$` also matches before a final newline), `\\s`/`\\S`
    (ECMA whitespace set), and `\\u{...}` refused. Flags other than `u` and `s` are refused."""
    if set(flags) - {"u", "s"} or "u" not in flags:
        raise UnsupportedPattern("flags " + flags)
    dot = "[\\s\\S]" if "s" in flags else "[^" + _cls(ECMA_LINE_TERMINATORS) + "]"
    ws = "[" + _cls(ECMA_WHITESPACE) + "]"
    nws = "[^" + _cls(ECMA_WHITESPACE) + "]"
    out, i, n = [], 0, len(pattern)
    while i < n:
        c = pattern[i]
        if c == "\\":
            if i + 1 >= n:
                raise UnsupportedPattern("trailing backslash")
            e = pattern[i + 1]
            if e == "u":
                if pattern[i + 2:i + 3] == "{":
                    raise UnsupportedPattern("\\u{...}")
                hexd = pattern[i + 2:i + 6]
                if not re.fullmatch(r"[0-9a-fA-F]{4}", hexd):
                    raise UnsupportedPattern("bad \\u escape")
                out.append("\\u" + hexd.lower()); i += 6; continue
            if e in ("d", "D", "w", "W"):
                out.append({"d": "[0-9]", "D": "[^0-9]", "w": "[A-Za-z0-9_]", "W": "[^A-Za-z0-9_]"}[e]); i += 2; continue
            if e == "s":
                out.append(ws); i += 2; continue
            if e == "S":
                out.append(nws); i += 2; continue
            if e not in _SUPPORTED_ESCAPES:
                raise UnsupportedPattern("escape \\" + e)
            out.append("\\" + e); i += 2; continue
        if c == "[":
            j = i + 1
            body = []
            if j < n and pattern[j] == "^":
                body.append("^"); j += 1
            while j < n and pattern[j] != "]":
                if pattern[j] == "\\":
                    e = pattern[j + 1]
                    if e == "u":
                        hexd = pattern[j + 2:j + 6]
                        if not re.fullmatch(r"[0-9a-fA-F]{4}", hexd):
                            raise UnsupportedPattern("bad class \\u escape")
                        body.append("\\u" + hexd.lower()); j += 6; continue
                    if e in ("d", "w"):
                        body.append({"d": "0-9", "w": "A-Za-z0-9_"}[e]); j += 2; continue
                    if e in ("s", "S"):
                        body.append(("\\s", "\\S")[e == "S"]); j += 2; continue
                    if e not in _SUPPORTED_ESCAPES:
                        raise UnsupportedPattern("class escape \\" + e)
                    body.append("\\" + e); j += 2; continue
                if pattern[j] == "[":
                    raise UnsupportedPattern("nested class")
                body.append(pattern[j]); j += 1
            if j >= n:
                raise UnsupportedPattern("unterminated class")
            text = "".join(body)
            if "\\s" in text or "\\S" in text:
                if text != "\\s\\S":
                    raise UnsupportedPattern("class with \\s/\\S other than [\\s\\S]")
                out.append("[\\s\\S]")
            else:
                out.append("[" + text + "]")
            i = j + 1; continue
        if c == ".":
            out.append(dot); i += 1; continue
        if c == "$":
            out.append("(?![\\s\\S])"); i += 1; continue
        if c == "(" and pattern.startswith("(?", i):
            if not any(pattern.startswith(t, i) for t in ("(?:", "(?=", "(?!")):
                raise UnsupportedPattern("group " + pattern[i:i + 4])
        out.append(c); i += 1
    return "".join(out)


_ECMA_CACHE = {}


def ecma_test(pattern, flags, value):
    key = (pattern, flags)
    rx = _ECMA_CACHE.get(key)
    if rx is None:
        rx = _ECMA_CACHE[key] = re.compile(ecma_to_python(pattern, flags))
    return rx.search(value) is not None


# ---------------------------------------------------------------- document-driven lexical rules
def split_package_key(rule, v, where=""):
    sep = rule["separator"]
    limit = int(rule["nameVersionForbidAtOrBelow"])
    first = v.find(sep)
    second = v.find(sep, first + 1) if first >= 0 else -1
    if first <= 0 or second <= first + 1:
        raise Refuse("PACKAGE_KEY_LEXICAL", where)
    name, version, source = v[:first], v[first + 1:second], v[second + 1:]
    if any(ord(c) <= limit for c in name + version):
        raise Refuse("PACKAGE_KEY_LEXICAL", where)
    return name, version, source


def lexical(rules, name, v, flags="u", where=""):
    """Apply the normative lexical rule `name` exactly as its structured definition in
    wire-carriers.v1.json privateRepresentation.lexicalRules states it (no hardcoded copy)."""
    rule = rules.get(name)
    if rule is None:
        raise Refuse("UNKNOWN_LEXICAL", name)
    if rule["kind"] == "package-key":
        split_package_key(rule, v, where)
        return
    if rule["kind"] != "segments":
        raise Refuse("UNKNOWN_LEXICAL", name)
    if "minScalars" in rule and len(v) < int(rule["minScalars"]):
        raise Refuse("PATH_LEXICAL", where)
    if rule.get("forbidLeadingSeparator") and v.startswith(rule["separator"]):
        raise Refuse("PATH_LEXICAL", where)
    if any(c in v for c in rule["forbiddenScalars"]):
        raise Refuse("PATH_LEXICAL", where)
    segments = v.split(rule["separator"])
    for g in segments:
        if g in rule["forbiddenSegments"]:
            raise Refuse("PATH_LEXICAL", where)
        if "maxSegmentScalars" in rule and len(g) > int(rule["maxSegmentScalars"]):
            raise Refuse("PATH_LEXICAL", where)
    prefix = rule.get("firstSegmentForbiddenPattern")
    if prefix is not None and ecma_test(prefix, flags, segments[0]):
        raise Refuse("PATH_LEXICAL", where)


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
    """Interprets the declarative input. `extern_validate(generatedType, value, where)` is supplied by the caller."""

    def __init__(self, doc, extern_validate):
        self.doc = doc
        self.types = dict(doc["scalars"])
        self.records = doc["records"]
        self.extern_validate = extern_validate
        self.lex = doc["privateRepresentation"]["lexicalRules"]
        self.flags = doc["privateRepresentation"]["patternDialect"]["flags"]

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
            if "lexical" in t:
                lexical(self.lex, t["lexical"], v, self.flags, where)
            if "pattern" in t and not ecma_test(t["pattern"], self.flags, v):
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
