"""Blind-consumer reference implementation of the OpenSIP product-v1 canonical
encoder C, identity function H, the x-opensip-order vocabulary, the
x-opensip-digest walker and the CVE1 capability-manifest encoder.

Written by the blind consumer directly from the normative prose of
  docs/v2/contracts/product-v1/identity-and-evidence.md  (sections 2, 3, 4, 5)
  docs/v2/contracts/product-v1/admission-and-qualification.md (section 1)
  docs/coop/artifacts/resolved-inputs.v2.json #planIdContract.canonicalValueEncoding
  docs/coop/artifacts/delivery.v4.json #derivedFrom.operations[17] CAP-MANIFEST-ID-V1
and the machine-readable annotations of
  docs/coop/design-corrections/foundation/identity-schemas.v2.json
No author reference model, fixture, golden or checker was read or copied; none
is present in the consumer kit.
"""

import hashlib
import json
import re
import unicodedata

# ---------------------------------------------------------------- admission --

MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024      # identity 3: "Maximum descriptor is 4 MiB"
MAX_DEPTH = 32                              # "nesting depth 32: the root container counts as 1"
INT_MIN = -(2 ** 63)                        # "Integer range is [-2^63, 2^64-1]"
INT_MAX = 2 ** 64 - 1


class Refuse(Exception):
    """An admission refusal.  Never a truncation, never a repair."""

    def __init__(self, code, detail=""):
        super().__init__("%s%s" % (code, (": " + detail) if detail else ""))
        self.code = code
        self.detail = detail


_INT_TOKEN = re.compile(r"^-?(0|[1-9][0-9]*)$")


def _no_dup_keys(pairs):
    seen = set()
    out = {}
    for k, v in pairs:
        if k in seen:
            raise Refuse("ADMIT.DUPLICATE_KEY", k)
        seen.add(k)
        out[k] = v
    return out


def _admit_number(token):
    # identity 3: "reject ... floating/exponent tokens, `-0`, nonfinite tokens"
    # admission 1: "`1.0`, `1e0`, `1E0` ... do not satisfy an integer field"
    if not _INT_TOKEN.match(token):
        raise Refuse("ADMIT.NON_INTEGER_TOKEN", token)
    if token == "-0":
        raise Refuse("ADMIT.NEGATIVE_ZERO", token)
    value = int(token)
    if not (INT_MIN <= value <= INT_MAX):
        raise Refuse("ADMIT.INTEGER_RANGE", token)
    return value


def parse(text_or_bytes):
    """Lexical admission before deserialization loses lexical information."""
    if isinstance(text_or_bytes, bytes):
        if len(text_or_bytes) > MAX_DESCRIPTOR_BYTES:
            raise Refuse("ADMIT.DESCRIPTOR_TOO_LARGE", str(len(text_or_bytes)))
        try:
            text = text_or_bytes.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise Refuse("ADMIT.MALFORMED_UTF8", str(exc))
    else:
        text = text_or_bytes
        if len(text.encode("utf-8")) > MAX_DESCRIPTOR_BYTES:
            raise Refuse("ADMIT.DESCRIPTOR_TOO_LARGE")
    for ch in text:
        if 0xD800 <= ord(ch) <= 0xDFFF:      # "non-scalar Unicode"
            raise Refuse("ADMIT.NON_SCALAR_UNICODE", hex(ord(ch)))
    try:
        value = json.loads(text, object_pairs_hook=_no_dup_keys, parse_float=_reject_float,
                           parse_int=_admit_number, parse_constant=_reject_constant)
    except Refuse:
        raise
    except ValueError as exc:
        raise Refuse("ADMIT.MALFORMED_JSON", str(exc)[:120])
    check_depth(value)
    _check_scalar_unicode(value)     # also catches a \udXXX escape sequence
    return value


def _check_scalar_unicode(value):
    if isinstance(value, str):
        for ch in value:
            if 0xD800 <= ord(ch) <= 0xDFFF:
                raise Refuse("ADMIT.NON_SCALAR_UNICODE", hex(ord(ch)))
    elif isinstance(value, dict):
        for k, v in value.items():
            _check_scalar_unicode(k)
            _check_scalar_unicode(v)
    elif isinstance(value, list):
        for v in value:
            _check_scalar_unicode(v)


def _reject_float(token):
    raise Refuse("ADMIT.FLOAT_TOKEN", token)


def _reject_constant(token):
    raise Refuse("ADMIT.NONFINITE_TOKEN", token)


def check_depth(value, depth=0):
    """The root container counts as 1; scalar leaves and object keys add none."""
    if isinstance(value, (dict, list)):
        depth += 1
        if depth > MAX_DEPTH:
            raise Refuse("ADMIT.DEPTH_EXCEEDED", str(depth))
        items = value.values() if isinstance(value, dict) else value
        for item in items:
            check_depth(item, depth)
    return depth


# --------------------------------------------------------------- encoder C --

_SHORT_ESCAPES = {0x08: "\\b", 0x09: "\\t", 0x0A: "\\n", 0x0C: "\\f", 0x0D: "\\r"}


def _encode_string(s):
    out = ['"']
    for ch in s:
        o = ord(ch)
        if 0xD800 <= o <= 0xDFFF:
            raise Refuse("ADMIT.NON_SCALAR_UNICODE", hex(o))
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif o in _SHORT_ESCAPES:
            out.append(_SHORT_ESCAPES[o])
        elif o < 0x20:
            out.append("\\u%04x" % o)        # lowercase \u00xx for other C0
        else:
            out.append(ch)                   # U+007F and U+2028 stay unescaped;
        # slash is never escaped; no Unicode normalization is applied.
    out.append('"')
    return "".join(out)


def C(value):
    """Canonical JSON bytes.  Arrays are encoded in their ADMITTED order."""
    return _c(value).encode("utf-8")


def _c(value):
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):               # bool is checked above first
        if not (INT_MIN <= value <= INT_MAX):
            raise Refuse("ADMIT.INTEGER_RANGE", str(value))
        return str(value)                    # shortest ordinary decimal
    if isinstance(value, float):
        raise Refuse("ADMIT.FLOAT_VALUE", repr(value))
    if isinstance(value, str):
        return _encode_string(value)
    if isinstance(value, list):
        return "[" + ",".join(_c(v) for v in value) + "]"
    if isinstance(value, dict):
        keys = list(value.keys())
        for k in keys:
            if not isinstance(k, str):
                raise Refuse("ADMIT.NON_STRING_KEY", repr(k))
        if len(set(keys)) != len(keys):
            raise Refuse("ADMIT.DUPLICATE_KEY")
        # UTF-8 byte-ordered keys
        keys.sort(key=lambda k: k.encode("utf-8"))
        return "{" + ",".join(_encode_string(k) + ":" + _c(value[k]) for k in keys) + "}"
    raise Refuse("ADMIT.UNENCODABLE", type(value).__name__)


# ---------------------------------------------------------------- identity --

FRAME_PREFIX = b"opensip.product.v1"


def frame(domain, descriptor):
    body = C(descriptor)
    if len(body) > MAX_DESCRIPTOR_BYTES:
        raise Refuse("ADMIT.DESCRIPTOR_TOO_LARGE", str(len(body)))
    return (FRAME_PREFIX + b"\x00" + domain.encode("utf-8") + b"\x00"
            + len(body).to_bytes(8, "big") + body)


def H(domain, descriptor):
    """H(D,X)=SHA256(ASCII("opensip.product.v1")||00||ASCII(D)||00||u64be(len(C(X)))||C(X))"""
    return hashlib.sha256(frame(domain, descriptor)).hexdigest()


def parse_frame(blob, expected_domains, records=None):
    """Frame admission is exact and is not a blob escape (identity 3)."""
    if not blob.startswith(FRAME_PREFIX + b"\x00"):
        raise Refuse("CLOSURE.FRAME_PREFIX")
    rest = blob[len(FRAME_PREFIX) + 1:]
    nul = rest.find(b"\x00")
    if nul < 0:
        raise Refuse("CLOSURE.FRAME_PREFIX")
    domain = rest[:nul].decode("utf-8")
    if domain not in expected_domains:
        raise Refuse("CLOSURE.FRAME_DOMAIN_NOT_IN_SET", domain)
    rest = rest[nul + 1:]
    if len(rest) < 8:
        raise Refuse("CLOSURE.FRAME_LENGTH")
    declared = int.from_bytes(rest[:8], "big")
    body = rest[8:]
    if declared != len(body):
        raise Refuse("CLOSURE.FRAME_LENGTH_MISMATCH", "%d != %d" % (declared, len(body)))
    payload = parse(body)
    if C(payload) != body:
        raise Refuse("CLOSURE.FRAME_NOT_CANONICAL", domain)
    return domain, payload


RAW = lambda b: hashlib.sha256(b).hexdigest()          # raw-artifact digest
REC = lambda o: hashlib.sha256(C(o)).hexdigest()       # canonical-record digest


def prefixed(prefix, domain, descriptor):
    return "%s:%s" % (prefix, H(domain, descriptor))


# ------------------------------------------------------------ order keyword --

ORDER_VOCABULARY = {"sequence", "canonical-set", "canonical-order", "utf8", "path",
                    "numeric", "ordinal", "predicate", "ruleId", "waiverId"}
_UNIQUE_REQUIRED = ORDER_VOCABULARY - {"sequence", "canonical-order"}


def _order_key(annotation, item):
    if annotation in ("canonical-set", "canonical-order"):
        return C(item)
    if annotation == "utf8":
        if not isinstance(item, str):
            raise Refuse("ORDER.UTF8_NEEDS_SCALAR_STRING")
        return item.encode("utf-8")
    if annotation == "path":
        return item["path"].encode("utf-8")
    if annotation == "numeric":
        if isinstance(item, bool) or not isinstance(item, int):
            raise Refuse("ORDER.NUMERIC_NEEDS_INTEGER")
        return item
    if annotation == "ordinal":
        return item["ordinal"]
    if annotation == "predicate":
        return tuple(item[k].encode("utf-8") for k in ("ruleId", "subjectId", "predicateId"))
    if annotation in ("ruleId", "waiverId"):
        return item[annotation].encode("utf-8")
    if isinstance(annotation, dict) and "by" in annotation:
        return tuple(item[k].encode("utf-8") for k in annotation["by"])
    raise Refuse("ORDER.ANNOTATION_OUTSIDE_VOCABULARY", repr(annotation))


def check_order(annotation, array, where=""):
    """An annotation outside this vocabulary refuses rather than passing silently."""
    if isinstance(annotation, str):
        if annotation not in ORDER_VOCABULARY:
            raise Refuse("ORDER.ANNOTATION_OUTSIDE_VOCABULARY", "%s %s" % (where, annotation))
    elif isinstance(annotation, dict):
        if set(annotation) != {"by"} or not annotation["by"]:
            raise Refuse("ORDER.ANNOTATION_OUTSIDE_VOCABULARY", where)
    else:
        raise Refuse("ORDER.ANNOTATION_OUTSIDE_VOCABULARY", where)
    if annotation == "sequence":
        return True
    if annotation == "ordinal":
        got = [item["ordinal"] for item in array]
        if got != list(range(len(array))):
            raise Refuse("ORDER.ORDINAL_NOT_CONTIGUOUS_ZERO_BASED", where)
        return True
    keys = [_order_key(annotation, item) for item in array]
    strict = annotation != "canonical-order"
    for a, b in zip(keys, keys[1:]):
        if strict and not (a < b):
            raise Refuse("ORDER.NOT_STRICTLY_ASCENDING", "%s %r" % (where, b))
        if not strict and a > b:
            raise Refuse("ORDER.NOT_NONDECREASING", where)
    if isinstance(annotation, dict) or annotation in _UNIQUE_REQUIRED:
        if len(set(keys)) != len(keys):
            raise Refuse("ORDER.DUPLICATE_SORT_KEY", where)
    return True


# ---------------------------------------------------------------- CVE1 -------
# resolved-inputs.v2 #planIdContract.canonicalValueEncoding: eight closed types.

def cve1(value):
    if value is None:
        return b"\x00"
    if value is True:
        return b"\x02"
    if value is False:
        return b"\x01"
    if isinstance(value, int):
        if 0 <= value <= 2 ** 64 - 1:
            return b"\x03" + value.to_bytes(8, "big")
        if -(2 ** 63) <= value < 0:
            return b"\x07" + value.to_bytes(8, "big", signed=True)
        raise Refuse("CVE1.INTEGER_RANGE", str(value))
    if isinstance(value, float):
        raise Refuse("CVE1.FLOAT_FORBIDDEN")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise Refuse("CVE1.STRING_NOT_NFC", value)
        b = value.encode("utf-8")
        return b"\x04" + len(b).to_bytes(4, "big") + b
    if isinstance(value, list):
        return b"\x05" + len(value).to_bytes(4, "big") + b"".join(cve1(v) for v in value)
    if isinstance(value, dict):
        keys = list(value.keys())
        if len(set(keys)) != len(keys):
            raise Refuse("CVE1.DUPLICATE_MAP_KEY")
        for k in keys:
            if not isinstance(k, str):
                raise Refuse("CVE1.NON_STRING_MAP_KEY")
            if unicodedata.normalize("NFC", k) != k:
                raise Refuse("CVE1.STRING_NOT_NFC", k)
        keys.sort(key=lambda k: k.encode("utf-8"))   # unsigned lexicographic NFC UTF-8
        return (b"\x06" + len(keys).to_bytes(4, "big")
                + b"".join(cve1(k) + cve1(value[k]) for k in keys))
    raise Refuse("CVE1.UNENCODABLE", type(value).__name__)


CAP_MANIFEST_PREFIX = b"opensip.capability-manifest.v1"


def capability_manifest_id(committed_bytes):
    """CAP-MANIFEST-ID-V1 (delivery.v4 op 17 step3), also identity 3."""
    return hashlib.sha256(CAP_MANIFEST_PREFIX + b"\x00" + committed_bytes).hexdigest()
