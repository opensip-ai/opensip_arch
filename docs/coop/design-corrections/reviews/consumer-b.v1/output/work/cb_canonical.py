"""Consumer-B independent reference: exact admission, canonical encoding, H identity.

Authored ONLY from the prose of:
  docs/v2/contracts/product-v1/identity-and-evidence.md  §3
  docs/v2/contracts/product-v1/admission-and-qualification.md  §1
  docs/v2/contracts/product-v1/workflows-and-surfaces.md  §10
  docs/coop/artifacts/delivery.v4.json  $.derivedFrom.operations[17].value.recipe (CAP-MANIFEST-ID-V1)

No author reference model was read. Disposable design-reference code.
"""

import hashlib
import json
import re

# ---------------------------------------------------------------------------
# Lexical admission (identity-and-evidence.md §3; admission-and-qualification §1)
# "Before deserialization loses lexical information, reject duplicate keys,
#  floating/exponent tokens, -0, nonfinite tokens, malformed UTF-8 and
#  non-scalar Unicode."
# "Integer range is [-2^63, 2^64-1]."
# ---------------------------------------------------------------------------

INT_MIN = -(2 ** 63)
INT_MAX = 2 ** 64 - 1
MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32


class Refused(Exception):
    def __init__(self, code, detail=""):
        super().__init__("%s %s" % (code, detail))
        self.code = code
        self.detail = detail


class Int(int):
    """Marker: an integer that came from an ordinary integer token."""


_FLOAT_TOKEN = re.compile(r"^-?(0|[1-9][0-9]*)([.][0-9]+)?([eE][-+]?[0-9]+)?$")
_ORDINARY_INT = re.compile(r"^(0|-?[1-9][0-9]*)$")


def _reject_number(tok):
    # "1.0, 1e0, 1E0 ... do not satisfy an integer field"; "-0 ... rejected"
    if tok == "-0":
        raise Refused("NUMBER.NEGATIVE_ZERO", tok)
    if not _ORDINARY_INT.match(tok):
        raise Refused("NUMBER.NOT_ORDINARY_INTEGER", tok)
    v = int(tok)
    if v < INT_MIN or v > INT_MAX:
        raise Refused("NUMBER.OUT_OF_CANONICAL_RANGE", tok)
    return Int(v)


def _object_pairs_hook(pairs):
    seen = set()
    out = {}
    for k, v in pairs:
        if k in seen:
            raise Refused("JSON.DUPLICATE_KEY", k)
        seen.add(k)
        out[k] = v
    return out


def parse(text_bytes):
    """Exact typed admission of descriptor bytes -> Python value.

    Refuses: oversized bytes, malformed UTF-8, non-scalar Unicode (lone
    surrogates), duplicate keys, float/exponent tokens, -0, nonfinite tokens,
    integers outside the canonical range, and nesting deeper than 32.
    """
    if not isinstance(text_bytes, (bytes, bytearray)):
        raise Refused("INPUT.NOT_BYTES")
    if len(text_bytes) > MAX_DESCRIPTOR_BYTES:
        raise Refused("DESCRIPTOR.TOO_LARGE", str(len(text_bytes)))
    try:
        s = text_bytes.decode("utf-8", "strict")
    except UnicodeDecodeError as e:
        raise Refused("UTF8.MALFORMED", str(e))
    for ch in s:
        if 0xD800 <= ord(ch) <= 0xDFFF:  # non-scalar Unicode
            raise Refused("UNICODE.NON_SCALAR", hex(ord(ch)))
    if re.search(r"\\u[dD][89abAB][0-9a-fA-F]{2}", s):
        # escaped lone/paired surrogate escapes: refuse the lexical form
        raise Refused("UNICODE.SURROGATE_ESCAPE")
    for bad in ("NaN", "Infinity", "-Infinity"):
        if re.search(r"(?<![\"\w])" + re.escape(bad) + r"(?![\"\w])", s):
            raise Refused("NUMBER.NONFINITE", bad)
    try:
        value = json.loads(
            s,
            object_pairs_hook=_object_pairs_hook,
            parse_float=_reject_number,
            parse_int=_reject_number,
            parse_constant=lambda c: (_ for _ in ()).throw(
                Refused("NUMBER.NONFINITE", c)),
        )
    except Refused:
        raise
    except json.JSONDecodeError as e:
        raise Refused("JSON.MALFORMED", str(e))
    _check_depth(value, 1)
    return value


def _check_depth(v, depth):
    # "the root container counts as 1; scalar leaves and object keys add no
    #  container depth"
    if isinstance(v, (dict, list)):
        if depth > MAX_DEPTH:
            raise Refused("DESCRIPTOR.DEPTH_EXCEEDED", str(depth))
        items = v.values() if isinstance(v, dict) else v
        for x in items:
            _check_depth(x, depth + 1)


def max_depth(v, depth=1):
    if not isinstance(v, (dict, list)):
        return depth - 1
    items = list(v.values()) if isinstance(v, dict) else list(v)
    if not items:
        return depth
    return max([depth] + [max_depth(x, depth + 1) for x in items])


# ---------------------------------------------------------------------------
# Canonical encoding (identity-and-evidence.md §3)
# ---------------------------------------------------------------------------

_ESCAPES = {
    0x22: '\\"',
    0x5C: "\\\\",
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
}


def _enc_string(s):
    if not isinstance(s, str):
        raise Refused("TYPE.NOT_STRING")
    out = ['"']
    for ch in s:
        cp = ord(ch)
        if 0xD800 <= cp <= 0xDFFF:
            raise Refused("UNICODE.NON_SCALAR", hex(cp))
        if cp in _ESCAPES:
            out.append(_ESCAPES[cp])
        elif cp <= 0x1F:
            out.append("\\u%04x" % cp)  # lowercase \u00xx
        else:
            # unescaped Unicode scalar characters; slash is NOT escaped;
            # U+007F and U+2028 remain unescaped.
            out.append(ch)
    out.append('"')
    return "".join(out).encode("utf-8")


def _enc_int(v):
    if isinstance(v, bool):
        raise Refused("TYPE.BOOL_IS_NOT_INT")
    if not isinstance(v, int):
        raise Refused("TYPE.NOT_INT")
    if v < INT_MIN or v > INT_MAX:
        raise Refused("NUMBER.OUT_OF_CANONICAL_RANGE", str(v))
    return str(v).encode("ascii")  # shortest ordinary decimal integer


# Array ordering disciplines (identity-and-evidence.md §3).
ORDER_SET = "set"                 # sorted+unique by canonical item bytes (default)
ORDER_INVENTORY = "inventory"     # sorted by UTF-8 logical path
ORDER_PREDICATE = "predicate"     # (ruleId, subjectId, predicateId)
ORDER_STAGES = "stages"           # contiguous ordinal
ORDER_ORDINAL_DEPS = "ordinals"   # numeric sort
ORDER_PRIORITY = "priority"       # declared order preserved

# Field-path -> ordering, keyed by the last path segment reached inside a
# descriptor. Read directly from §3's named exceptions.
ARRAY_ORDER = {
    "sourceInventory": ORDER_INVENTORY,
    "tree": ORDER_INVENTORY,
    "blobs": ORDER_INVENTORY,
    "predicateProofs": ORDER_PREDICATE,
    "stages": ORDER_STAGES,
    "requires": ORDER_ORDINAL_DEPS,
    "allowedScopes": ORDER_PRIORITY,
}


def _order_of(key):
    return ARRAY_ORDER.get(key, ORDER_SET)


def _enc_array(items, key):
    order = _order_of(key)
    encoded = [encode(x) for x in items]
    if order == ORDER_PRIORITY:
        seq = encoded
    elif order == ORDER_INVENTORY:
        keyed = []
        for x, e in zip(items, encoded):
            if not isinstance(x, dict) or "path" not in x:
                raise Refused("INVENTORY.NO_PATH")
            keyed.append((x["path"].encode("utf-8"), e))
        paths = [k for k, _ in keyed]
        if len(set(paths)) != len(paths):
            raise Refused("INVENTORY.DUPLICATE_PATH")
        seq = [e for _, e in sorted(keyed, key=lambda t: t[0])]
    elif order == ORDER_PREDICATE:
        keyed = []
        for x, e in zip(items, encoded):
            keyed.append(((x["ruleId"].encode("utf-8"),
                           x["subjectId"].encode("utf-8"),
                           x["predicateId"].encode("utf-8")), e))
        ks = [k for k, _ in keyed]
        if len(set(ks)) != len(ks):
            raise Refused("PREDICATE.DUPLICATE_KEY")
        seq = [e for _, e in sorted(keyed, key=lambda t: t[0])]
    elif order == ORDER_STAGES:
        ordinals = [x["ordinal"] for x in items]
        if sorted(ordinals) != list(range(len(ordinals))):
            raise Refused("STAGES.NOT_CONTIGUOUS_ORDINAL", str(ordinals))
        seq = [e for _, e in sorted(zip(ordinals, encoded), key=lambda t: t[0])]
    elif order == ORDER_ORDINAL_DEPS:
        for x in items:
            if isinstance(x, bool) or not isinstance(x, int):
                raise Refused("ORDINALS.NOT_INTEGER")
        if len(set(items)) != len(items):
            raise Refused("ORDINALS.DUPLICATE")
        seq = [encode(x) for x in sorted(items)]
    else:  # ORDER_SET
        if len(set(encoded)) != len(encoded):
            raise Refused("SET.DUPLICATE_ITEM")
        seq = sorted(encoded)
    return b"[" + b",".join(seq) + b"]"


def encode(v, key=None):
    """Canonical JSON bytes: UTF-8 byte-ordered keys, no whitespace, no
    trailing newline, no Unicode normalization, shortest ordinary decimal
    integers, unescaped Unicode scalars."""
    if v is None:
        return b"null"
    if isinstance(v, bool):
        return b"true" if v else b"false"
    if isinstance(v, int):
        return _enc_int(v)
    if isinstance(v, float):
        raise Refused("TYPE.FLOAT_FORBIDDEN", repr(v))
    if isinstance(v, str):
        return _enc_string(v)
    if isinstance(v, list):
        return _enc_array(v, key)
    if isinstance(v, dict):
        ks = list(v.keys())
        for k in ks:
            if not isinstance(k, str):
                raise Refused("KEY.NOT_STRING")
        kb = [k.encode("utf-8") for k in ks]
        if len(set(kb)) != len(kb):
            raise Refused("JSON.DUPLICATE_KEY")
        parts = []
        for k in sorted(ks, key=lambda x: x.encode("utf-8")):
            parts.append(_enc_string(k) + b":" + encode(v[k], k))
        return b"{" + b",".join(parts) + b"}"
    raise Refused("TYPE.UNSUPPORTED", type(v).__name__)


def canonical(v):
    b = encode(v)
    if len(b) > MAX_DESCRIPTOR_BYTES:
        raise Refused("DESCRIPTOR.TOO_LARGE", str(len(b)))
    if max_depth(v) > MAX_DEPTH:
        raise Refused("DESCRIPTOR.DEPTH_EXCEEDED")
    return b


# ---------------------------------------------------------------------------
# H identity (identity-and-evidence.md §3)
#   H(D,X) = SHA256(ASCII("opensip.product.v1") || 00 || ASCII(D) || 00
#                   || uint64BE(length(C(X))) || C(X))
# ---------------------------------------------------------------------------

NAMESPACE = b"opensip.product.v1"


def H_preimage(domain, descriptor):
    c = canonical(descriptor)
    return (NAMESPACE + b"\x00" + domain.encode("ascii") + b"\x00"
            + len(c).to_bytes(8, "big") + c), c


def H(domain, descriptor):
    pre, _ = H_preimage(domain, descriptor)
    return hashlib.sha256(pre).hexdigest()


# Domain -> identifier prefix, from identity-and-evidence.md §3's
# "Domain / prefix" table.
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
    "finding": "finding2",
    "proof-bundle": "proof2",
    "semantic-evidence": "evidence2",
    "evaluation-seal": "seal2",
    "run": "run2",
    "cache-key": "cache2",
    "regeneration-key": "regen2",
    "policy-derivation": "policy-derivation2",
}


def ident(domain, descriptor):
    return PREFIX[domain] + ":" + H(domain, descriptor)


def raw(descriptor):
    """Raw SHA-256 of canonical bytes (auxiliary digests)."""
    return hashlib.sha256(canonical(descriptor)).hexdigest()


def blob_sha256(b):
    return hashlib.sha256(b).hexdigest()


def capability_manifest_id(committed_bytes):
    """CAP-MANIFEST-ID-V1, retained (delivery.v4 op[17].value.recipe;
    restated in identity-and-evidence.md §3)."""
    return hashlib.sha256(
        b"opensip.capability-manifest.v1" + b"\x00" + committed_bytes).hexdigest()


# ---------------------------------------------------------------------------
# Exact const/enum/integer validation (admission-and-qualification.md §1)
# "an already-decoded 1.0 or True cannot satisfy const:1"
# ---------------------------------------------------------------------------

def exact_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def exact_const(v, c):
    if isinstance(c, bool):
        return isinstance(v, bool) and v is c
    if isinstance(c, int):
        return exact_int(v) and v == c
    if isinstance(c, str):
        return isinstance(v, str) and v == c
    return v == c and type(v) is type(c)


def exact_enum(v, members):
    return any(exact_const(v, m) for m in members)
