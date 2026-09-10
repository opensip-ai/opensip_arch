"""Independent blind-consumer reference helpers for OpenSIP DR-011-R10.

Written from the normative prose/registries in
/tmp/opensip-design-corrections/consumer-b.v8/subject only.  No author
implementation was read.  Everything here is disposable design-reference code.

Normative sources for each helper are named in its docstring by exact selector.
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
import unicodedata

KIT = "/tmp/opensip-design-corrections/consumer-b.v8/subject/"

# --------------------------------------------------------------------------
# C: canonical JSON  (identity-and-evidence.md section 3, "Canonical JSON ...")
# --------------------------------------------------------------------------

_ESCAPES = {
    0x22: '\\"',
    0x5C: "\\\\",
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
}


class CanonError(Exception):
    pass


def _c_string(s: str) -> str:
    out = ['"']
    for ch in s:
        cp = ord(ch)
        if 0xD800 <= cp <= 0xDFFF:
            raise CanonError("non-scalar Unicode (lone surrogate) in string")
        if cp in _ESCAPES:
            out.append(_ESCAPES[cp])
        elif cp <= 0x1F:
            # lowercase \u00xx for other U+0000-001F controls
            out.append("\\u%04x" % cp)
        else:
            # everything else unescaped, including / , U+007F and U+2028
            out.append(ch)
    out.append('"')
    return "".join(out)


def _c(value) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        # shortest ordinary decimal integer; no -0 (Python has none), no exponent
        if not (-(2 ** 63) <= value <= 2 ** 64 - 1):
            raise CanonError("integer out of canonical range [-2^63, 2^64-1]")
        return str(value)
    if isinstance(value, float):
        raise CanonError("floating point value is inadmissible in C")
    if isinstance(value, str):
        return _c_string(value)
    if isinstance(value, list):
        # arrays are encoded IN THEIR ADMITTED ORDER; C never sorts.
        return "[" + ",".join(_c(v) for v in value) + "]"
    if isinstance(value, dict):
        keys = list(value.keys())
        for k in keys:
            if not isinstance(k, str):
                raise CanonError("non-string object key")
        if len(set(keys)) != len(keys):
            raise CanonError("duplicate key")
        keys.sort(key=lambda k: k.encode("utf-8"))  # UTF-8 byte-ordered keys
        return "{" + ",".join(_c_string(k) + ":" + _c(value[k]) for k in keys) + "}"
    raise CanonError("unencodable type %r" % type(value))


def C(value) -> bytes:
    """Canonical JSON bytes.  No whitespace, no trailing newline."""
    return _c(value).encode("utf-8")


# --------------------------------------------------------------------------
# Exact typed / lexical admission BEFORE deserialization
# identity-and-evidence.md section 3 paragraph 1;
# admission-and-qualification.md section 1
# --------------------------------------------------------------------------

MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32

_NUM_RE = re.compile(rb"-?(0|[1-9][0-9]*)")


class AdmissionError(Exception):
    def __init__(self, code, detail=""):
        super().__init__(code + (": " + detail if detail else ""))
        self.code = code
        self.detail = detail


def admit_raw(raw: bytes, max_bytes: int = MAX_DESCRIPTOR_BYTES,
              max_depth: int = MAX_DEPTH):
    """Admit RAW descriptor bytes, then parse.

    Refuses, before any JSON value exists, in this order:
      LEX_SIZE          descriptor over the 4 MiB bound
      LEX_UTF8          malformed UTF-8
      LEX_SURROGATE     non-scalar Unicode (lone surrogate, incl. \\ud800 escape)
      LEX_NUMBER        float/exponent token, -0, nonfinite token
      LEX_DUPLICATE_KEY duplicate object key
      LEX_DEPTH         nesting depth over 32 (root container counts as 1;
                        scalar leaves and object keys add no container depth)
      LEX_INT_RANGE     integer outside [-2^63, 2^64-1]
    The first refusal observed is the one reported.
    """
    if len(raw) > max_bytes:
        raise AdmissionError("LEX_SIZE", "%d > %d" % (len(raw), max_bytes))
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as e:
        raise AdmissionError("LEX_UTF8", str(e))

    # nonfinite tokens and float spellings are caught lexically below; the
    # JSON grammar itself is walked by a small scanner so that duplicate keys
    # and depth are observed on the token stream rather than after parsing.
    depth_seen = [0]

    def _scan(i, depth):
        i = _ws(i)
        if i >= len(text):
            raise AdmissionError("LEX_SYNTAX", "unexpected end")
        ch = text[i]
        if ch == "{":
            depth += 1
            depth_seen[0] = max(depth_seen[0], depth)
            if depth > max_depth:
                raise AdmissionError("LEX_DEPTH", "depth %d > %d" % (depth, max_depth))
            i = _ws(i + 1)
            keys = set()
            if i < len(text) and text[i] == "}":
                return i + 1
            while True:
                i = _ws(i)
                if i >= len(text) or text[i] != '"':
                    raise AdmissionError("LEX_SYNTAX", "object key expected")
                k, i = _string(i)
                if k in keys:
                    raise AdmissionError("LEX_DUPLICATE_KEY", k)
                keys.add(k)
                i = _ws(i)
                if i >= len(text) or text[i] != ":":
                    raise AdmissionError("LEX_SYNTAX", "colon expected")
                i = _scan(i + 1, depth)
                i = _ws(i)
                if i < len(text) and text[i] == ",":
                    i += 1
                    continue
                if i < len(text) and text[i] == "}":
                    return i + 1
                raise AdmissionError("LEX_SYNTAX", "object continuation")
        if ch == "[":
            depth += 1
            depth_seen[0] = max(depth_seen[0], depth)
            if depth > max_depth:
                raise AdmissionError("LEX_DEPTH", "depth %d > %d" % (depth, max_depth))
            i = _ws(i + 1)
            if i < len(text) and text[i] == "]":
                return i + 1
            while True:
                i = _scan(i, depth)
                i = _ws(i)
                if i < len(text) and text[i] == ",":
                    i += 1
                    continue
                if i < len(text) and text[i] == "]":
                    return i + 1
                raise AdmissionError("LEX_SYNTAX", "array continuation")
        if ch == '"':
            _, i = _string(i)
            return i
        for lit in ("true", "false", "null"):
            if text.startswith(lit, i):
                return i + len(lit)
        for bad in ("NaN", "Infinity", "-Infinity"):
            if text.startswith(bad, i):
                raise AdmissionError("LEX_NUMBER", "nonfinite token %s" % bad)
        m = re.compile(r"-?[0-9][0-9]*(\.[0-9]+)?([eE][-+]?[0-9]+)?").match(text, i)
        if not m:
            raise AdmissionError("LEX_SYNTAX", "value expected at %d" % i)
        tok = m.group(0)
        if "." in tok or "e" in tok or "E" in tok:
            raise AdmissionError("LEX_NUMBER", "float/exponent token %s" % tok)
        if tok == "-0":
            raise AdmissionError("LEX_NUMBER", "-0")
        if re.match(r"-?0[0-9]", tok):
            raise AdmissionError("LEX_NUMBER", "leading zero %s" % tok)
        n = int(tok)
        if not (-(2 ** 63) <= n <= 2 ** 64 - 1):
            raise AdmissionError("LEX_INT_RANGE", tok)
        return m.end()

    def _ws(i):
        while i < len(text) and text[i] in " \t\n\r":
            i += 1
        return i

    def _string(i):
        assert text[i] == '"'
        i += 1
        out = []
        while True:
            if i >= len(text):
                raise AdmissionError("LEX_SYNTAX", "unterminated string")
            ch = text[i]
            if ch == '"':
                return "".join(out), i + 1
            if ch == "\\":
                nxt = text[i + 1]
                if nxt == "u":
                    hexs = text[i + 2:i + 6]
                    cp = int(hexs, 16)
                    if 0xD800 <= cp <= 0xDFFF:
                        # a surrogate escape must be a well-formed pair
                        if not (0xD800 <= cp <= 0xDBFF and text[i + 6:i + 8] == "\\u"):
                            raise AdmissionError("LEX_SURROGATE", hexs)
                        lo = int(text[i + 8:i + 12], 16)
                        if not (0xDC00 <= lo <= 0xDFFF):
                            raise AdmissionError("LEX_SURROGATE", hexs)
                        out.append(chr(0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00)))
                        i += 12
                        continue
                    out.append(chr(cp))
                    i += 6
                    continue
                out.append({"n": "\n", "t": "\t", "r": "\r", "b": "\b",
                            "f": "\f", '"': '"', "\\": "\\", "/": "/"}[nxt])
                i += 2
                continue
            if 0xD800 <= ord(ch) <= 0xDFFF:
                raise AdmissionError("LEX_SURROGATE", hex(ord(ch)))
            out.append(ch)
            i += 1

    end = _scan(0, 0)
    if _ws(end) != len(text):
        raise AdmissionError("LEX_SYNTAX", "trailing bytes")
    return json.loads(text), depth_seen[0]


# --------------------------------------------------------------------------
# H and the retained preimage frame
# identity-and-evidence.md section 3, "For domain D and descriptor X"
# --------------------------------------------------------------------------

FRAME_PREFIX = b"opensip.product.v1"

PREFIXES = {
    "snapshot": "snapshot2", "closure": "closure2", "import": "import2",
    "plan": "plan2", "subject-scope": "scope2", "fact": "fact2",
    "coverage": "coverage2", "view": "view2", "execution-plan": "exec-plan2",
    "finding-fingerprint": "finding-key2", "finding": "finding2",
    "proof-bundle": "proof2", "semantic-evidence": "evidence2",
    "evaluation-seal": "seal2", "run": "run2", "cache-key": "cache2",
    "regeneration-key": "regen2", "policy-derivation": "policy-derivation2",
}


def frame(domain: str, descriptor) -> bytes:
    body = C(descriptor)
    return (FRAME_PREFIX + b"\x00" + domain.encode("ascii") + b"\x00"
            + struct.pack(">Q", len(body)) + body)


def H(domain: str, descriptor) -> str:
    """lowercase hex of H(D, X)."""
    return hashlib.sha256(frame(domain, descriptor)).hexdigest()


def ident(domain: str, descriptor) -> str:
    """typed foundation identity <prefix>:<64 hex>."""
    return PREFIXES[domain] + ":" + H(domain, descriptor)


def parse_frame(blob: bytes):
    """Exact frame admission (identity-and-evidence section 3, closing digest law)."""
    if not blob.startswith(FRAME_PREFIX + b"\x00"):
        raise AdmissionError("FRAME_PREFIX")
    rest = blob[len(FRAME_PREFIX) + 1:]
    nul = rest.find(b"\x00")
    if nul < 0:
        raise AdmissionError("FRAME_DOMAIN")
    domain = rest[:nul].decode("ascii")
    rest = rest[nul + 1:]
    if len(rest) < 8:
        raise AdmissionError("FRAME_LENGTH")
    (declared,) = struct.unpack(">Q", rest[:8])
    payload = rest[8:]
    if declared != len(payload):
        raise AdmissionError("FRAME_LENGTH", "%d != %d" % (declared, len(payload)))
    value, _ = admit_raw(payload)
    if C(value) != payload:
        raise AdmissionError("FRAME_NOT_CANONICAL")
    return domain, value


def raw_sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def record_digest(record) -> str:
    """`canonical-record` representation: raw SHA-256 of C(record)."""
    return hashlib.sha256(C(record)).hexdigest()


# --------------------------------------------------------------------------
# x-opensip-order  (identity-and-evidence.md section 3)
# --------------------------------------------------------------------------

def check_order(items, annotation, where=""):
    """Return list of order violations for one array under its annotation."""
    bad = []
    if annotation == "sequence":
        return bad
    if annotation in ("canonical-set", "canonical-order"):
        keys = [C(i) for i in items]
        strict = annotation == "canonical-set"
    elif annotation == "utf8":
        keys = [i.encode("utf-8") for i in items]
        strict = True
    elif annotation == "path":
        keys = [i["path"].encode("utf-8") for i in items]
        strict = True
    elif annotation == "numeric":
        keys = list(items)
        strict = True
    elif annotation == "ordinal":
        if [i["ordinal"] for i in items] != list(range(len(items))):
            bad.append((where, "ordinal not contiguous zero-based"))
        return bad
    elif annotation == "predicate":
        keys = [(i["ruleId"], i["subjectId"], i["predicateId"]) for i in items]
        keys = [("\x00".join(k)).encode("utf-8") for k in keys]
        strict = True
    elif annotation in ("ruleId", "waiverId"):
        keys = [i[annotation].encode("utf-8") for i in items]
        strict = True
    elif isinstance(annotation, dict) and "by" in annotation:
        keys = [tuple(i[k] for k in annotation["by"]) for i in items]
        keys = [("\x00".join(str(x) for x in k)).encode("utf-8") for k in keys]
        strict = True
    else:
        bad.append((where, "annotation outside the closed vocabulary: %r" % (annotation,)))
        return bad
    for a, b in zip(keys, keys[1:]):
        if strict and not a < b:
            bad.append((where, "not strictly ascending under %r" % (annotation,)))
            break
        if not strict and a > b:
            bad.append((where, "decreasing under %r" % (annotation,)))
            break
    return bad


# --------------------------------------------------------------------------
# CVE1  (resolved-inputs.v2.json#planIdContract.canonicalValueEncoding)
# --------------------------------------------------------------------------

class CVE1Error(Exception):
    pass


def cve1(value) -> bytes:
    """The eight closed CVE1 types with their exact tags and lengths."""
    if value is None:
        return b"\x00"
    if value is False:
        return b"\x01"
    if value is True:
        return b"\x02"
    if isinstance(value, int):
        if 0 <= value <= 2 ** 64 - 1:
            return b"\x03" + struct.pack(">Q", value)
        if -(2 ** 63) <= value < 0:
            return b"\x07" + struct.pack(">q", value)
        raise CVE1Error("integer outside the two closed integer types")
    if isinstance(value, float):
        raise CVE1Error("floating-point values are forbidden")
    if isinstance(value, bytes):
        raise CVE1Error("byte strings are forbidden")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise CVE1Error("non-NFC string is rejected rather than normalised")
        b = value.encode("utf-8")
        return b"\x04" + struct.pack(">I", len(b)) + b
    if isinstance(value, list):
        return b"\x05" + struct.pack(">I", len(value)) + b"".join(cve1(v) for v in value)
    if isinstance(value, dict):
        keys = list(value.keys())
        if len(set(keys)) != len(keys):
            raise CVE1Error("duplicate map key")
        for k in keys:
            if not isinstance(k, str):
                raise CVE1Error("map key is not a string")
            if unicodedata.normalize("NFC", k) != k:
                raise CVE1Error("non-NFC map key")
        keys.sort(key=lambda k: k.encode("utf-8"))
        out = [b"\x06", struct.pack(">I", len(keys))]
        for k in keys:
            out.append(cve1(k))
            out.append(cve1(value[k]))
        return b"".join(out)
    raise CVE1Error("unencodable type %r" % type(value))


CAP_DOMAIN = b"opensip.capability-manifest.v1"


def capability_manifest_id(committed: bytes) -> str:
    """SHA256(UTF8("opensip.capability-manifest.v1") || 00 || committedBytes)."""
    return hashlib.sha256(CAP_DOMAIN + b"\x00" + committed).hexdigest()


# --------------------------------------------------------------------------
# FACT-IDENTITY body frame
# relation-payload-schemas.v2 clones bodyIdentityJoin;
# identity-and-evidence.md "clones: the inherited body recipe"
# --------------------------------------------------------------------------

FACT_IDENTITY_DOMAIN = "opensip.fact-identity.v1"


def _u8len(b: bytes) -> bytes:
    if len(b) > 255:
        raise CanonError("component exceeds the inherited u8 length")
    return bytes([len(b)]) + b


def body_frame(level_id: str, level_version_raw: bytes, language_id: str,
               language_version_raw: bytes, payload: bytes) -> bytes:
    assert len(level_version_raw) == 32 and len(language_version_raw) == 32
    return (_u8len(FACT_IDENTITY_DOMAIN.encode("ascii"))
            + _u8len(level_id.encode("utf-8"))
            + _u8len(level_version_raw)
            + _u8len(language_id.encode("utf-8"))
            + _u8len(language_version_raw)
            + struct.pack(">I", len(payload)) + payload)


def l0_payload(span_bytes: bytes) -> bytes:
    """L0-verbatim payload: u32be raw_byte_len || exact body-span bytes."""
    return struct.pack(">I", len(span_bytes)) + span_bytes


def token_stream_payload(tokens) -> bytes:
    """L1-L3: u32be token_count || token*, token = u16be kind_len||kind||u32be val_len||val."""
    out = [struct.pack(">I", len(tokens))]
    for kind, val in tokens:
        kb = kind.encode("utf-8")
        vb = val.encode("utf-8")
        out.append(struct.pack(">H", len(kb)) + kb + struct.pack(">I", len(vb)) + vb)
    return b"".join(out)


def body_identity(level_id, level_version_hex, language_id, blv_record, payload):
    """Returns (sha256text, frame_bytes).  languageVersion is the RAW 32 bytes of
    SHA-256(C(body-language-version))."""
    lv = bytes.fromhex(level_version_hex)
    langv = hashlib.sha256(C(blv_record)).digest()
    fr = body_frame(level_id, lv, language_id, langv, payload)
    return "sha256:" + hashlib.sha256(fr).hexdigest(), fr


# --------------------------------------------------------------------------
# document digests
# --------------------------------------------------------------------------

def doc_bytes(rel: str) -> bytes:
    with open(KIT + rel, "rb") as f:
        return f.read()


def doc_digest(rel: str) -> str:
    return raw_sha256(doc_bytes(rel))
