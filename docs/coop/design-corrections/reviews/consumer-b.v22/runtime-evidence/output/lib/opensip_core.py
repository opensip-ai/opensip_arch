"""consumer-b.v22 INDEPENDENT reconstruction core.

Everything here is written from the normative kit prose/schemas only:

* `C`  -- identity-and-evidence section 3 "Canonical JSON": UTF-8 byte-ordered keys,
  no whitespace, no trailing newline, no Unicode normalisation, shortest ordinary
  decimal integers, unescaped Unicode scalars; escape only `"` and `\\`, the five
  short escapes `\\b \\t \\n \\f \\r`, and lowercase `\\u00xx` for the remaining
  U+0000-001F controls; `/` is NOT escaped; U+007F and U+2028 stay unescaped.
  Arrays are encoded in their ADMITTED order -- C never sorts or dedupes.
* `H(D, X)` -- SHA256(ASCII("opensip.product.v1") || 00 || ASCII(D) || 00 ||
  uint64BE(len(C(X))) || C(X)).
* `h_frame` -- the exact retained preimage bytes for an `h-identity` digest.
* CVE1 -- docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding
  (eight closed types, exact tags/lengths, NFC-only strings, key-sorted maps).
* lexical admission -- the pre-deserialisation rules of identity section 3, run on RAW
  INPUT BYTES, deliberately separate from encoding an already-parsed object.

No author reference model, fixture or golden was read. Embedded kit examples were
not used as expected values.
"""
import hashlib
import json
import re
import struct
import unicodedata

PRODUCT_PREFIX = b"opensip.product.v1"

# ---------------------------------------------------------------- C (canonical JSON)

_SHORT = {0x08: "\\b", 0x09: "\\t", 0x0A: "\\n", 0x0C: "\\f", 0x0D: "\\r"}

MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32
INT_MIN = -(2 ** 63)
INT_MAX = 2 ** 64 - 1


class CanonError(Exception):
    pass


def _cstr(s):
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif o in _SHORT:
            out.append(_SHORT[o])
        elif o < 0x20:
            out.append("\\u%04x" % o)
        else:
            # unescaped Unicode scalar character; / U+007F U+2028 are NOT escaped
            out.append(ch)
    out.append('"')
    return "".join(out)


def _enc(x, depth):
    if depth > MAX_DEPTH:
        raise CanonError("DEPTH_EXCEEDED")
    if x is True:
        return "true"
    if x is False:
        return "false"
    if x is None:
        return "null"
    if isinstance(x, int):
        if not (INT_MIN <= x <= INT_MAX):
            raise CanonError("INTEGER_RANGE")
        return "%d" % x          # shortest ordinary decimal integer
    if isinstance(x, float):
        raise CanonError("FLOAT_FORBIDDEN")
    if isinstance(x, str):
        for ch in x:
            if unicodedata.category(ch) == "Cs":
                raise CanonError("NON_SCALAR_UNICODE")
        return _cstr(x)
    if isinstance(x, list):
        # admitted order preserved: C never sorts, dedupes or infers set semantics
        return "[" + ",".join(_enc(v, depth + 1) for v in x) + "]"
    if isinstance(x, dict):
        keys = list(x.keys())
        for k in keys:
            if not isinstance(k, str):
                raise CanonError("NON_STRING_KEY")
        if len(set(keys)) != len(keys):
            raise CanonError("DUPLICATE_KEY")
        keys.sort(key=lambda k: k.encode("utf-8"))   # UTF-8 byte order
        return "{" + ",".join(_cstr(k) + ":" + _enc(x[k], depth + 1) for k in keys) + "}"
    raise CanonError("UNSUPPORTED_TYPE:%s" % type(x).__name__)


def C(x):
    """Canonical bytes of an already-parsed object."""
    b = _enc(x, 1).encode("utf-8")
    if len(b) > MAX_DESCRIPTOR_BYTES:
        raise CanonError("DESCRIPTOR_TOO_LARGE")
    return b


def raw_sha256(b):
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------- opensip-metadata-canonical.1 (S2, never mixed)

class MetadataProfileError(Exception):
    pass


I64_MIN = -(2 ** 63)
I64_MAX = 2 ** 63 - 1


def _menc(x, depth):
    """`opensip-metadata-canonical.1` = opensip-canonical-json-v1 with the five
    undetermined points decided (security-completion v1 2.1 / v8 2.1):
      UR-1 key order   ascending Unicode scalar value == unsigned UTF-8 byte order
      UR-2 integers    signed 64-bit two's complement only; out of range refuses
      UR-3 NFC         REJECT non-NFC strings and keys; the encoder NEVER normalizes
      UR-4 escaping    exactly CJ-R08 (same escape set as C)
      UR-5 surrogates  reject lone surrogates
    plus: duplicate keys reject, floats reject, array order preserved.
    This is a SEPARATE codec from C: "A decoder for one profile never admits the
    other's documents."
    """
    if depth > MAX_DEPTH:
        raise MetadataProfileError("DEPTH_EXCEEDED")
    if x is True:
        return "true"
    if x is False:
        return "false"
    if x is None:
        return "null"
    if isinstance(x, int):
        if not (I64_MIN <= x <= I64_MAX):
            raise MetadataProfileError("INTEGER_OUT_OF_RANGE")
        return "%d" % x
    if isinstance(x, float):
        raise MetadataProfileError("FLOAT_REJECTED")
    if isinstance(x, str):
        for ch in x:
            if unicodedata.category(ch) == "Cs":
                raise MetadataProfileError("LONE_SURROGATE")
        if unicodedata.normalize("NFC", x) != x:
            raise MetadataProfileError("NON_NFC_STRING")
        return _cstr(x)
    if isinstance(x, list):
        return "[" + ",".join(_menc(v, depth + 1) for v in x) + "]"
    if isinstance(x, dict):
        keys = list(x.keys())
        for k in keys:
            if not isinstance(k, str):
                raise MetadataProfileError("NON_STRING_KEY")
            if unicodedata.normalize("NFC", k) != k:
                raise MetadataProfileError("NON_NFC_STRING")
        if len({unicodedata.normalize("NFC", k) for k in keys}) != len(keys):
            raise MetadataProfileError("NFC_KEY_COLLISION")
        keys.sort(key=lambda k: k.encode("utf-8"))
        return "{" + ",".join(_cstr(k) + ":" + _menc(x[k], depth + 1) for k in keys) + "}"
    raise MetadataProfileError("NON_MODEL_LEAF")


def Cmeta(x):
    return _menc(x, 1).encode("utf-8")


def metadata_preimage_digest(domain_tag, x):
    """preimageSha256 = SHA-256(UTF-8(domainTag) || 0x00 || canonicalBytes)."""
    return raw_sha256(domain_tag.encode("utf-8") + b"\x00" + Cmeta(x))


def rec_digest(x):
    """raw SHA-256 of C(record) -- the `canonical-record` representation."""
    return raw_sha256(C(x))


# ---------------------------------------------------------------- H / frames

def h_frame(domain, x):
    cx = C(x)
    return (PRODUCT_PREFIX + b"\x00" + domain.encode("ascii") + b"\x00"
            + struct.pack(">Q", len(cx)) + cx)


def H(domain, x):
    return raw_sha256(h_frame(domain, x))


PREFIX = {
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
    # workflows-and-surfaces.md section 10 typed identity recipes. `workflow.mutation-intent`
    # is deliberately ABSENT: section 10 says it returns its BARE 64-hex H value, so it has no
    # typed prefix and must not be given one.
    "workflow.baseline": "baseline2",
    "workflow.comparison": "comparison2",
    "workflow.repair-plan": "repairplan2",
    "workflow.mutation-receipt": "receipt2",
    "workflow.verification-link": "receipt2",
    "workflow.policy-test-result": "policytest2",
    "workflow.candidate": "candidate2",
}


def ID(domain, x):
    return PREFIX[domain] + ":" + H(domain, x)


def parse_h_frame(frame_bytes, allowed_domains):
    """Exact frame admission (identity section 3 closing digest law).

    The literal prefix must match, the domain must be a member of the annotation's
    named domain set, the declared length must equal the remaining byte count, and
    the remainder must be byte-identical to C of its own parse.
    """
    p = PRODUCT_PREFIX + b"\x00"
    if not frame_bytes.startswith(p):
        raise CanonError("FRAME_PREFIX")
    rest = frame_bytes[len(p):]
    z = rest.find(b"\x00")
    if z < 0:
        raise CanonError("FRAME_DOMAIN_TERMINATOR")
    domain = rest[:z].decode("ascii")
    if domain not in allowed_domains:
        raise CanonError("FRAME_DOMAIN_UNREGISTERED:%s" % domain)
    rest = rest[z + 1:]
    if len(rest) < 8:
        raise CanonError("FRAME_LENGTH_FIELD")
    declared = struct.unpack(">Q", rest[:8])[0]
    payload = rest[8:]
    if declared != len(payload):
        raise CanonError("FRAME_LENGTH_MISMATCH")
    obj = json.loads(payload.decode("utf-8"))
    if C(obj) != payload:
        raise CanonError("FRAME_NOT_CANONICAL")
    return domain, obj


# ---------------------------------------------------------------- lexical admission (RAW bytes)

_NUM = re.compile(rb"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?")


class LexicalRefusal(Exception):
    def __init__(self, code, detail=None, offset=None):
        super().__init__(code)
        self.code = code
        self.detail = detail
        self.offset = offset


def admit_raw_descriptor(b, max_bytes=MAX_DESCRIPTOR_BYTES, max_depth=MAX_DEPTH):
    """Pre-deserialisation admission of RAW input bytes.

    identity-and-evidence section 3: "Before deserialization loses lexical
    information, reject duplicate keys, floating/exponent tokens, -0, nonfinite
    tokens, malformed UTF-8 and non-scalar Unicode. Integer range is
    [-2^63, 2^64-1] ... Maximum descriptor is 4 MiB and nesting depth 32: the root
    container counts as 1; scalar leaves and object keys add no container depth."

    Returns the parsed object. Raises LexicalRefusal with the FIRST refusal.
    """
    if not isinstance(b, (bytes, bytearray)):
        raise TypeError("raw bytes required")
    if len(b) > max_bytes:
        raise LexicalRefusal("DESCRIPTOR_TOO_LARGE", "%d bytes" % len(b))
    try:
        text = b.decode("utf-8", errors="strict")
    except UnicodeDecodeError as e:
        raise LexicalRefusal("MALFORMED_UTF8", str(e), e.start)
    for i, ch in enumerate(text):
        if unicodedata.category(ch) == "Cs":
            raise LexicalRefusal("NON_SCALAR_UNICODE", "U+%04X" % ord(ch), i)

    # token scan for numbers and nonfinite literals, before any decode
    i, n, depth, maxdepth = 0, len(text), 0, 0
    in_str, esc = False, False
    while i < n:
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str = True
            i += 1
            continue
        if ch in "{[":
            depth += 1
            maxdepth = max(maxdepth, depth)
            if depth > max_depth:
                raise LexicalRefusal("NESTING_DEPTH_EXCEEDED", "depth %d" % depth, i)
            i += 1
            continue
        if ch in "}]":
            depth -= 1
            i += 1
            continue
        for lit in ("NaN", "Infinity", "-Infinity"):
            if text.startswith(lit, i):
                raise LexicalRefusal("NONFINITE_TOKEN", lit, i)
        if ch == "-" or ch.isdigit():
            m = _NUM.match(b, len(text[:i].encode("utf-8")))
            tok = m.group(0).decode("ascii") if m else None
            if tok is None:
                raise LexicalRefusal("MALFORMED_NUMBER", text[i:i + 12], i)
            if "." in tok or "e" in tok or "E" in tok:
                raise LexicalRefusal("FLOAT_OR_EXPONENT_TOKEN", tok, i)
            if tok == "-0":
                raise LexicalRefusal("NEGATIVE_ZERO_TOKEN", tok, i)
            v = int(tok)
            if not (INT_MIN <= v <= INT_MAX):
                raise LexicalRefusal("INTEGER_RANGE", tok, i)
            i += len(tok)
            continue
        i += 1
    if in_str:
        raise LexicalRefusal("UNTERMINATED_STRING")

    def no_dup(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                raise LexicalRefusal("DUPLICATE_KEY", k)
            seen.add(k)
        return dict(pairs)

    try:
        obj = json.loads(text, object_pairs_hook=no_dup,
                         parse_constant=lambda c: (_ for _ in ()).throw(
                             LexicalRefusal("NONFINITE_TOKEN", c)))
    except LexicalRefusal:
        raise
    except json.JSONDecodeError as e:
        raise LexicalRefusal("MALFORMED_JSON", str(e), e.pos)
    return obj


# ---------------------------------------------------------------- CVE1

class Cve1Error(Exception):
    pass


CVE1_TYPES = ["null", "false", "true", "unsigned-64", "negative-signed-64",
              "NFC-UTF8-string", "array", "string-keyed-map"]
CVE1_MAX_NESTING = 64
CVE1_MAX_ITEMS = 1048576


def cve1_type(v):
    if v is None:
        return "null"
    if v is False:
        return "false"
    if v is True:
        return "true"
    if isinstance(v, int):
        if v < 0:
            if v < -(2 ** 63):
                raise Cve1Error("NEGATIVE_SIGNED_64_RANGE")
            return "negative-signed-64"
        if v > 2 ** 64 - 1:
            raise Cve1Error("UNSIGNED_64_RANGE")
        return "unsigned-64"
    if isinstance(v, float):
        raise Cve1Error("FLOAT_FORBIDDEN")
    if isinstance(v, bytes):
        raise Cve1Error("BYTE_STRING_FORBIDDEN")
    if isinstance(v, str):
        return "NFC-UTF8-string"
    if isinstance(v, list):
        return "array"
    if isinstance(v, dict):
        return "string-keyed-map"
    raise Cve1Error("UNSUPPORTED_TYPE:%s" % type(v).__name__)


def cve1(v, depth=1):
    if depth > CVE1_MAX_NESTING:
        raise Cve1Error("MAX_NESTING")
    t = cve1_type(v)
    if t == "null":
        return b"\x00"
    if t == "false":
        return b"\x01"
    if t == "true":
        return b"\x02"
    if t == "unsigned-64":
        return b"\x03" + struct.pack(">Q", v)
    if t == "negative-signed-64":
        return b"\x07" + struct.pack(">q", v)
    if t == "NFC-UTF8-string":
        if unicodedata.normalize("NFC", v) != v:
            raise Cve1Error("STRING_NOT_NFC")
        e = v.encode("utf-8")
        return b"\x04" + struct.pack(">I", len(e)) + e
    if t == "array":
        if len(v) > CVE1_MAX_ITEMS:
            raise Cve1Error("MAX_COLLECTION_ITEMS")
        out = b"\x05" + struct.pack(">I", len(v))
        for el in v:
            out += cve1(el, depth + 1)
        return out
    if t == "string-keyed-map":
        if len(v) > CVE1_MAX_ITEMS:
            raise Cve1Error("MAX_COLLECTION_ITEMS")
        keys = []
        for k in v:
            if not isinstance(k, str):
                raise Cve1Error("MAP_KEY_NOT_STRING")
            if unicodedata.normalize("NFC", k) != k:
                raise Cve1Error("MAP_KEY_NOT_NFC")
            keys.append(k)
        enc = [k.encode("utf-8") for k in keys]
        if len(set(enc)) != len(enc):
            raise Cve1Error("MAP_DUPLICATE_KEY")
        order = sorted(range(len(keys)), key=lambda i: enc[i])   # unsigned lexicographic
        out = b"\x06" + struct.pack(">I", len(keys))
        for i in order:
            out += cve1(keys[i], depth + 1) + cve1(v[keys[i]], depth + 1)
        return out
    raise Cve1Error("UNREACHABLE")


def cve1_decode(b, pos=0, depth=1):
    """Bounded, total-refusing CVE1 decoder (decoderBounds of
    capability-manifest-domains.v2)."""
    if depth > CVE1_MAX_NESTING:
        raise Cve1Error("MAX_NESTING")
    if pos >= len(b):
        raise Cve1Error("TRUNCATED")
    tag = b[pos]
    pos += 1
    if tag == 0x00:
        return None, pos
    if tag == 0x01:
        return False, pos
    if tag == 0x02:
        return True, pos
    if tag == 0x03:
        if pos + 8 > len(b):
            raise Cve1Error("TRUNCATED_U64")
        return struct.unpack(">Q", b[pos:pos + 8])[0], pos + 8
    if tag == 0x07:
        if pos + 8 > len(b):
            raise Cve1Error("TRUNCATED_I64")
        v = struct.unpack(">q", b[pos:pos + 8])[0]
        if v >= 0:
            raise Cve1Error("NEGATIVE_TAG_NONNEGATIVE_VALUE")
        return v, pos + 8
    if tag == 0x04:
        if pos + 4 > len(b):
            raise Cve1Error("TRUNCATED_STRLEN")
        ln = struct.unpack(">I", b[pos:pos + 4])[0]
        pos += 4
        if pos + ln > len(b):
            raise Cve1Error("TRUNCATED_STR")
        s = b[pos:pos + ln].decode("utf-8")
        if unicodedata.normalize("NFC", s) != s:
            raise Cve1Error("STRING_NOT_NFC")
        return s, pos + ln
    if tag == 0x05:
        if pos + 4 > len(b):
            raise Cve1Error("TRUNCATED_ARRLEN")
        n = struct.unpack(">I", b[pos:pos + 4])[0]
        pos += 4
        if n > CVE1_MAX_ITEMS:
            raise Cve1Error("MAX_COLLECTION_ITEMS")
        out = []
        for _ in range(n):
            v, pos = cve1_decode(b, pos, depth + 1)
            out.append(v)
        return out, pos
    if tag == 0x06:
        if pos + 4 > len(b):
            raise Cve1Error("TRUNCATED_MAPLEN")
        n = struct.unpack(">I", b[pos:pos + 4])[0]
        pos += 4
        if n > CVE1_MAX_ITEMS:
            raise Cve1Error("MAX_COLLECTION_ITEMS")
        out = {}
        prev = None
        for _ in range(n):
            k, pos = cve1_decode(b, pos, depth + 1)
            if not isinstance(k, str):
                raise Cve1Error("MAP_KEY_NOT_STRING")
            kb = k.encode("utf-8")
            if prev is not None and kb <= prev:
                raise Cve1Error("MAP_KEYS_NOT_STRICTLY_ASCENDING")
            prev = kb
            v, pos = cve1_decode(b, pos, depth + 1)
            out[k] = v
        return out, pos
    raise Cve1Error("UNKNOWN_TAG:0x%02x" % tag)


def cve1_decode_exact(b):
    v, pos = cve1_decode(b, 0, 1)
    if pos != len(b):
        raise Cve1Error("TRAILING_BYTES")
    return v


CAP_MANIFEST_DOMAIN = b"opensip.capability-manifest.v1"


def capability_manifest_id(committed_bytes):
    """SHA256(UTF8("opensip.capability-manifest.v1") || 0x00 || committedBytes)."""
    return raw_sha256(CAP_MANIFEST_DOMAIN + b"\x00" + committed_bytes)


# ---------------------------------------------------------------- x-opensip-order

class OrderRefusal(Exception):
    def __init__(self, code, path, detail=None):
        super().__init__("%s at %s (%s)" % (code, path, detail))
        self.code = code
        self.path = path
        self.detail = detail


ORDER_VOCAB = {"sequence", "canonical-set", "canonical-order", "utf8", "path",
               "numeric", "ordinal", "predicate", "ruleId", "waiverId"}


def _order_key(ann, item, path):
    if ann == "canonical-set" or ann == "canonical-order":
        return C(item)
    if ann == "utf8":
        if not isinstance(item, str):
            raise OrderRefusal("ORDER_ITEM_NOT_SCALAR_STRING", path, repr(item)[:40])
        return item.encode("utf-8")
    if ann == "path":
        if not (isinstance(item, dict) and isinstance(item.get("path"), str)):
            raise OrderRefusal("ORDER_PATH_KEY_MISSING", path, repr(item)[:60])
        return item["path"].encode("utf-8")
    if ann == "numeric":
        if not isinstance(item, int) or isinstance(item, bool):
            raise OrderRefusal("ORDER_ITEM_NOT_INTEGER", path, repr(item)[:40])
        return item
    if ann == "ordinal":
        if not (isinstance(item, dict) and isinstance(item.get("ordinal"), int)):
            raise OrderRefusal("ORDER_ORDINAL_KEY_MISSING", path, repr(item)[:60])
        return item["ordinal"]
    if ann == "predicate":
        for k in ("ruleId", "subjectId", "predicateId"):
            if not isinstance(item.get(k), str):
                raise OrderRefusal("ORDER_PREDICATE_TUPLE_MISSING", path, k)
        return (item["ruleId"] + "," + item["subjectId"] + "," + item["predicateId"]).encode("utf-8")
    if ann in ("ruleId", "waiverId"):
        if not (isinstance(item, dict) and isinstance(item.get(ann), str)):
            raise OrderRefusal("ORDER_KEY_MISSING", path, ann)
        return item[ann].encode("utf-8")
    raise OrderRefusal("ORDER_ANNOTATION_OUTSIDE_VOCABULARY", path, repr(ann))


def check_order(ann, arr, path):
    """Enforce one x-opensip-order annotation on one admitted array."""
    if isinstance(ann, dict):
        by = ann.get("by")
        if not (isinstance(by, list) and by and all(isinstance(k, str) for k in by)
                and set(ann.keys()) == {"by"}):
            raise OrderRefusal("ORDER_ANNOTATION_OUTSIDE_VOCABULARY", path, repr(ann))
        keys = []
        for it in arr:
            if not isinstance(it, dict):
                raise OrderRefusal("ORDER_BY_ITEM_NOT_OBJECT", path, repr(it)[:40])
            tup = []
            for k in by:
                if k not in it:
                    raise OrderRefusal("ORDER_BY_KEY_MISSING", path, k)
                v = it[k]
                if not isinstance(v, str):
                    raise OrderRefusal("ORDER_BY_KEY_NOT_STRING", path, k)
                tup.append(v)
            keys.append(tuple(x.encode("utf-8") for x in tup))
        for i in range(1, len(keys)):
            if not keys[i - 1] < keys[i]:
                raise OrderRefusal("ORDER_NOT_STRICTLY_ASCENDING", path + "[%d]" % i,
                                   "by=%s" % by)
        if len(set(keys)) != len(keys):
            raise OrderRefusal("ORDER_SORT_KEY_NOT_UNIQUE", path, "by=%s" % by)
        return
    if ann not in ORDER_VOCAB:
        raise OrderRefusal("ORDER_ANNOTATION_OUTSIDE_VOCABULARY", path, repr(ann))
    if ann == "sequence":
        return
    keys = [_order_key(ann, it, path) for it in arr]
    if ann == "canonical-order":
        for i in range(1, len(keys)):
            if keys[i - 1] > keys[i]:
                raise OrderRefusal("ORDER_NOT_NONDECREASING", path + "[%d]" % i, ann)
        return
    if ann == "ordinal":
        if keys != list(range(len(keys))):
            raise OrderRefusal("ORDER_ORDINAL_NOT_CONTIGUOUS_ZERO_BASED",
                               path, repr(keys)[:80])
        return
    for i in range(1, len(keys)):
        if not keys[i - 1] < keys[i]:
            raise OrderRefusal("ORDER_NOT_STRICTLY_ASCENDING", path + "[%d]" % i, ann)
    if len(set(keys)) != len(keys):
        raise OrderRefusal("ORDER_SORT_KEY_NOT_UNIQUE", path, ann)


def cset(items):
    """Cset(X): unique members keyed by C(member), ordered by those canonical bytes."""
    seen = {}
    for it in items:
        seen[C(it)] = it
    return [seen[k] for k in sorted(seen)]


def cset_strings(items):
    return sorted(set(items), key=lambda s: C(s))
