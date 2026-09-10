"""Independent C, CVE1, H, and body-identity codecs reconstructed from kit prose.

Owners:
- C: docs/v2/contracts/product-v1/identity-and-evidence.md §3
- CVE1: docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding
- H: identity-and-evidence.md §3
- capabilityManifestId: delivery.v4 CAP-MANIFEST-ID-V1 + identity-and-evidence §3
- bodyIdentity: fact-identity-policy.v2 canonicalisationSchema + identity-and-evidence clones successor
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from typing import Any, Mapping

PRODUCT_PREFIX = b"opensip.product.v1"
CAP_MANIFEST_DOMAIN = "opensip.capability-manifest.v1"
BODY_DOMAIN_TAG = "opensip.fact-identity.v1"

H_PREFIX = {
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
}

CVE1_NULL = 0x00
CVE1_FALSE = 0x01
CVE1_TRUE = 0x02
CVE1_U64 = 0x03
CVE1_STR = 0x04
CVE1_ARR = 0x05
CVE1_MAP = 0x06
CVE1_I64 = 0x07

MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32
INT_MIN = -(2**63)
INT_MAX = 2**64 - 1


class AdmissionError(Exception):
    def __init__(self, code: str, message: str, *, gate: str | None = None, path: str = "$"):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.gate = gate
        self.path = path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def u8(n: int) -> bytes:
    if not 0 <= n <= 255:
        raise AdmissionError("BOUND", f"u8 out of range: {n}")
    return bytes([n])


def u16be(n: int) -> bytes:
    if not 0 <= n <= 0xFFFF:
        raise AdmissionError("BOUND", f"u16 out of range: {n}")
    return n.to_bytes(2, "big")


def u32be(n: int) -> bytes:
    if not 0 <= n <= 0xFFFFFFFF:
        raise AdmissionError("BOUND", f"u32 out of range: {n}")
    return n.to_bytes(4, "big")


def u64be(n: int) -> bytes:
    if not 0 <= n <= 0xFFFFFFFFFFFFFFFF:
        raise AdmissionError("BOUND", f"u64 out of range: {n}")
    return n.to_bytes(8, "big")


def i64be(n: int) -> bytes:
    if not -(2**63) <= n <= 2**63 - 1:
        raise AdmissionError("BOUND", f"i64 out of range: {n}")
    return n.to_bytes(8, "big", signed=True)


_CONTROL_ESCAPE = {
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
}


def encode_c_string(s: str) -> str:
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif o in _CONTROL_ESCAPE:
            out.append(_CONTROL_ESCAPE[o])
        elif o < 0x20:
            out.append(f"\\u{o:04x}")
        else:
            # Unescaped Unicode scalar characters, including U+007F and U+2028.
            # Slash is not escaped.
            out.append(ch)
    out.append('"')
    return "".join(out)


def encode_c_int(n: int) -> str:
    if n < INT_MIN or n > INT_MAX:
        raise AdmissionError("INTEGER_RANGE", f"integer {n} outside [{INT_MIN}, {INT_MAX}]")
    if n == 0:
        return "0"
    return str(n)


def _container_depth(value: Any, depth: int = 1) -> int:
    """Root container counts as 1; scalar leaves and object keys add no container depth."""
    if isinstance(value, dict):
        if not value:
            return depth
        return max(_container_depth(v, depth + 1) for v in value.values())
    if isinstance(value, list):
        if not value:
            return depth
        return max(_container_depth(v, depth + 1) for v in value)
    return depth


def encode_c(value: Any, *, _root: bool = True) -> bytes:
    """Canonical JSON C(X) from identity-and-evidence §3.

    Already-parsed objects only. Lexical JSON admission is admit_json_text.
    """
    if _root:
        d = _container_depth(value)
        if d > MAX_DEPTH:
            raise AdmissionError("DEPTH", f"nesting depth {d} exceeds {MAX_DEPTH}")

    if value is None:
        text = "null"
    elif value is True:
        text = "true"
    elif value is False:
        text = "false"
    elif isinstance(value, bool):
        raise AdmissionError("TYPE", "non-canonical bool subclass")
    elif isinstance(value, int) and not isinstance(value, bool):
        text = encode_c_int(value)
    elif isinstance(value, float):
        raise AdmissionError("FLOAT_FORBIDDEN", "C forbids floating-point values")
    elif isinstance(value, str):
        text = encode_c_string(value)
    elif isinstance(value, list):
        parts = [encode_c(v, _root=False).decode("utf-8") for v in value]
        text = "[" + ",".join(parts) + "]"
    elif isinstance(value, dict):
        items = []
        for k in value:
            if not isinstance(k, str):
                raise AdmissionError("MAP_KEY", "object keys must be strings")
        # UTF-8 byte-ordered keys. C never sorts arrays.
        for k in sorted(value.keys(), key=lambda s: s.encode("utf-8")):
            items.append(encode_c_string(k) + ":" + encode_c(value[k], _root=False).decode("utf-8"))
        text = "{" + ",".join(items) + "}"
    else:
        raise AdmissionError("TYPE", f"C cannot encode {type(value).__name__}")

    raw = text.encode("utf-8")
    if _root and len(raw) > MAX_DESCRIPTOR_BYTES:
        raise AdmissionError("SIZE", f"descriptor {len(raw)} exceeds {MAX_DESCRIPTOR_BYTES}")
    return raw


def canonical_digest(record: Any) -> str:
    return sha256(encode_c(record))


# --- lexical JSON admission (before decoding can round numbers) ---

_INT_TOKEN = re.compile(r"^-?(0|[1-9][0-9]*)$")
_NUM_TOKEN = re.compile(r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$")


def admit_json_text(text: str | bytes, *, expect_integer_paths: set[str] | None = None) -> Any:
    """Lexical admission: duplicate keys, float/exponent tokens, -0, nonfinite, UTF-8, surrogates.

    expect_integer_paths: JSON Pointer-like paths whose tokens must be ordinary integers.
    """
    if isinstance(text, bytes):
        try:
            text = text.decode("utf-8")
        except UnicodeDecodeError as e:
            raise AdmissionError("UTF8", f"malformed UTF-8: {e}") from e
    if "\ud800" in text or any(0xD800 <= ord(c) <= 0xDFFF for c in text):
        raise AdmissionError("SURROGATE", "lone surrogate in JSON text")

    decoder = json.JSONDecoder(object_pairs_hook=_reject_duplicate_pairs)
    try:
        obj, idx = decoder.raw_decode(text)
    except json.JSONDecodeError as e:
        raise AdmissionError("JSON", str(e)) from e
    rest = text[idx:]
    if rest.strip():
        raise AdmissionError("TRAILING", "trailing JSON content")

    _scan_tokens(text, expect_integer_paths or set())
    return obj


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict:
    seen: set[str] = set()
    out = {}
    for k, v in pairs:
        if k in seen:
            raise AdmissionError("DUPLICATE_KEY", f"duplicate key {k!r}")
        seen.add(k)
        out[k] = v
    return out


def _scan_tokens(text: str, integer_paths: set[str]) -> None:
    """Reject float/exponent/-0 tokens. Path tracking is best-effort for claimed integer fields."""
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in " \t\r\n{}[],:":
            i += 1
            continue
        if ch == '"':
            i += 1
            while i < n:
                if text[i] == "\\":
                    i += 2
                    continue
                if text[i] == '"':
                    i += 1
                    break
                i += 1
            continue
        if ch in "-0123456789":
            j = i
            if text[j] == "-":
                j += 1
            while j < n and text[j].isdigit():
                j += 1
            if j < n and text[j] in ".eE":
                k = j
                while k < n and text[k] not in " \t\r\n{}[],:":
                    k += 1
                tok = text[i:k]
                raise AdmissionError("NON_INTEGER_TOKEN", f"numeric token {tok!r} is not an ordinary integer")
            tok = text[i:j]
            if tok in ("-0", "+0") or tok.startswith("-0") and tok != "-0" and not tok.startswith("-0") is False:
                if tok == "-0" or (tok.startswith("-0") and len(tok) > 2 and tok[2].isdigit()):
                    raise AdmissionError("NEG_ZERO", f"rejected numeric token {tok!r}")
            if tok.startswith("0") and len(tok) > 1:
                raise AdmissionError("LEADING_ZERO", f"rejected numeric token {tok!r}")
            if tok.startswith("-0") and len(tok) > 2:
                raise AdmissionError("LEADING_ZERO", f"rejected numeric token {tok!r}")
            if not _INT_TOKEN.match(tok):
                raise AdmissionError("NON_INTEGER_TOKEN", f"numeric token {tok!r} is not an ordinary integer")
            i = j
            continue
        if text.startswith("true", i):
            i += 4
            continue
        if text.startswith("false", i):
            i += 5
            continue
        if text.startswith("null", i):
            i += 4
            continue
        raise AdmissionError("JSON", f"unexpected character {ch!r} at {i}")


# --- CVE1 ---

def _require_nfc(s: str, path: str) -> bytes:
    if unicodedata.normalize("NFC", s) != s:
        raise AdmissionError("NON_NFC", f"string at {path} is not NFC", gate="CVE1")
    raw = s.encode("utf-8")
    return raw


def encode_cve1(value: Any, *, path: str = "$", depth: int = 0) -> bytes:
    """CVE1 from resolved-inputs.v2 planIdContract.canonicalValueEncoding.

    Eight closed types. Admission of type happens before encoding for capability
    manifests (ADM-TYPE); this encoder still refuses floats and non-NFC.
    """
    if depth > 64:
        raise AdmissionError("CVE1_DEPTH", f"nesting exceeds 64 at {path}")
    if value is None:
        return bytes([CVE1_NULL])
    if value is False:
        return bytes([CVE1_FALSE])
    if value is True:
        return bytes([CVE1_TRUE])
    if isinstance(value, bool):
        raise AdmissionError("CVE1_TYPE", f"bool subclass at {path}")
    if isinstance(value, int):
        if value < INT_MIN or value > INT_MAX:
            raise AdmissionError("CVE1_RANGE", f"integer out of range at {path}")
        if value < 0:
            return bytes([CVE1_I64]) + i64be(value)
        return bytes([CVE1_U64]) + u64be(value)
    if isinstance(value, float):
        raise AdmissionError("CVE1_FLOAT", f"float forbidden at {path}")
    if isinstance(value, str):
        raw = _require_nfc(value, path)
        return bytes([CVE1_STR]) + u32be(len(raw)) + raw
    if isinstance(value, list):
        if len(value) > 1_048_576:
            raise AdmissionError("CVE1_BOUND", f"array too large at {path}")
        parts = [encode_cve1(v, path=f"{path}[{i}]", depth=depth + 1) for i, v in enumerate(value)]
        return bytes([CVE1_ARR]) + u32be(len(value)) + b"".join(parts)
    if isinstance(value, dict):
        if len(value) > 1_048_576:
            raise AdmissionError("CVE1_BOUND", f"map too large at {path}")
        keys = []
        seen = set()
        for k in value:
            if not isinstance(k, str):
                raise AdmissionError("CVE1_KEY", f"non-string map key at {path}")
            kb = _require_nfc(k, f"{path}.{k}")
            if kb in seen:
                raise AdmissionError("CVE1_DUP_KEY", f"duplicate map key at {path}")
            seen.add(kb)
            keys.append((kb, k))
        keys.sort(key=lambda t: t[0])  # unsigned lexicographic NFC UTF-8 key bytes
        parts = []
        for kb, k in keys:
            parts.append(encode_cve1(k, path=f"{path}@{k}", depth=depth + 1))
            parts.append(encode_cve1(value[k], path=f"{path}.{k}", depth=depth + 1))
        return bytes([CVE1_MAP]) + u32be(len(keys)) + b"".join(parts)
    raise AdmissionError("CVE1_TYPE", f"unsupported type {type(value).__name__} at {path}")


def decode_cve1(data: bytes, *, depth: int = 0) -> Any:
    value, rest = _decode_cve1_one(data, depth=depth)
    if rest:
        raise AdmissionError("CVE1_TRAILING", f"{len(rest)} trailing bytes")
    return value


def _decode_cve1_one(data: bytes, *, depth: int = 0) -> tuple[Any, bytes]:
    if depth > 64:
        raise AdmissionError("CVE1_DEPTH", "nesting exceeds 64")
    if not data:
        raise AdmissionError("CVE1_EOF", "empty CVE1 buffer")
    tag = data[0]
    rest = data[1:]
    if tag == CVE1_NULL:
        return None, rest
    if tag == CVE1_FALSE:
        return False, rest
    if tag == CVE1_TRUE:
        return True, rest
    if tag == CVE1_U64:
        if len(rest) < 8:
            raise AdmissionError("CVE1_EOF", "truncated u64")
        return int.from_bytes(rest[:8], "big"), rest[8:]
    if tag == CVE1_I64:
        if len(rest) < 8:
            raise AdmissionError("CVE1_EOF", "truncated i64")
        return int.from_bytes(rest[:8], "big", signed=True), rest[8:]
    if tag == CVE1_STR:
        if len(rest) < 4:
            raise AdmissionError("CVE1_EOF", "truncated string length")
        n = int.from_bytes(rest[:4], "big")
        rest = rest[4:]
        if len(rest) < n:
            raise AdmissionError("CVE1_EOF", "truncated string")
        raw = rest[:n]
        s = raw.decode("utf-8")
        if unicodedata.normalize("NFC", s) != s:
            raise AdmissionError("NON_NFC", "decoded string is not NFC")
        return s, rest[n:]
    if tag == CVE1_ARR:
        if len(rest) < 4:
            raise AdmissionError("CVE1_EOF", "truncated array count")
        n = int.from_bytes(rest[:4], "big")
        rest = rest[4:]
        items = []
        for _ in range(n):
            v, rest = _decode_cve1_one(rest, depth=depth + 1)
            items.append(v)
        return items, rest
    if tag == CVE1_MAP:
        if len(rest) < 4:
            raise AdmissionError("CVE1_EOF", "truncated map count")
        n = int.from_bytes(rest[:4], "big")
        rest = rest[4:]
        items = []
        prev_key_bytes: bytes | None = None
        for _ in range(n):
            k, rest = _decode_cve1_one(rest, depth=depth + 1)
            v, rest = _decode_cve1_one(rest, depth=depth + 1)
            if not isinstance(k, str):
                raise AdmissionError("CVE1_KEY", "map key is not a string")
            kb = k.encode("utf-8")
            if prev_key_bytes is not None and kb <= prev_key_bytes:
                raise AdmissionError("CVE1_MAP_ORDER", "map keys are not strictly sorted unique")
            prev_key_bytes = kb
            items.append((k, v))
        return dict(items), rest
    raise AdmissionError("CVE1_TAG", f"unknown tag {tag:#x}")


# --- H identity ---

def h_preimage(domain: str, descriptor: Any) -> bytes:
    if not domain or "\x00" in domain:
        raise AdmissionError("DOMAIN", f"invalid domain {domain!r}")
    cx = encode_c(descriptor)
    return PRODUCT_PREFIX + b"\x00" + domain.encode("ascii") + b"\x00" + u64be(len(cx)) + cx


def h_hex(domain: str, descriptor: Any) -> str:
    return sha256(h_preimage(domain, descriptor))


def h_id(domain: str, descriptor: Any) -> str:
    prefix = H_PREFIX.get(domain)
    hx = h_hex(domain, descriptor)
    if prefix:
        return f"{prefix}:{hx}"
    return hx


def h_sha256_text(domain: str, descriptor: Any) -> str:
    return "sha256:" + h_hex(domain, descriptor)


def parse_h_frame(frame: bytes) -> tuple[str, bytes]:
    """Parse retained H preimage frame. Returns (domain, C(X) bytes)."""
    prefix = PRODUCT_PREFIX + b"\x00"
    if not frame.startswith(prefix):
        raise AdmissionError("H_FRAME", "frame does not begin with opensip.product.v1 NUL")
    rest = frame[len(prefix):]
    z = rest.find(b"\x00")
    if z < 0:
        raise AdmissionError("H_FRAME", "missing domain terminator")
    domain = rest[:z].decode("ascii")
    rest = rest[z + 1:]
    if len(rest) < 8:
        raise AdmissionError("H_FRAME", "missing length")
    n = int.from_bytes(rest[:8], "big")
    payload = rest[8:]
    if len(payload) != n:
        raise AdmissionError("H_FRAME", f"declared length {n} != remaining {len(payload)}")
    return domain, payload


def capability_manifest_id(committed_bytes: bytes) -> str:
    pre = CAP_MANIFEST_DOMAIN.encode("utf-8") + b"\x00" + committed_bytes
    return sha256(pre)


# --- body identity ---

LEVEL_IDS = (
    "L0-verbatim",
    "L1-lexical",
    "L2-comment-insensitive",
    "L3-identifier-insensitive",
)


def l0_payload(span: bytes) -> bytes:
    """L0 payload is itself length-prefixed: u32be raw_byte_len || exact bytes."""
    return u32be(len(span)) + span


def framed_token_stream(tokens: list[tuple[str, bytes]]) -> bytes:
    """L1-L3 payload: u32be token_count || (u16be kind_len || kind || u32be value_len || value)*"""
    parts = [u32be(len(tokens))]
    for kind, value in tokens:
        kb = kind.encode("utf-8")
        if not kb:
            raise AdmissionError("TOKEN_KIND", "empty token kind_id")
        parts.append(u16be(len(kb)))
        parts.append(kb)
        parts.append(u32be(len(value)))
        parts.append(value)
    return b"".join(parts)


def body_language_version_record(
    *,
    language_id: str,
    compiler_name: str,
    compiler_version: str,
    compiler_build: str,
    dialect: Mapping[str, Any],
) -> dict:
    return {
        "schemaVersion": 1,
        "languageId": language_id,
        "compilerName": compiler_name,
        "compilerVersion": compiler_version,
        "compilerBuild": compiler_build,
        "dialect": dict(dialect),
    }


def language_version_bytes(blv: Mapping[str, Any]) -> bytes:
    """Raw 32 bytes of SHA-256(C(body-language-version))."""
    return hashlib.sha256(encode_c(dict(blv))).digest()


def body_identity_frame(
    *,
    level_id: str,
    level_version: bytes,
    language_id: str,
    language_version: bytes,
    payload: bytes,
) -> bytes:
    """Fully framed domain-separated preimage.

    identity-and-evidence clones successor: u8 len||component for the five
    identity components, then u32be payload_len || payload.
    level_version and language_version are raw 32-byte digests, never hex text.
    """
    if level_id not in LEVEL_IDS:
        raise AdmissionError("LEVEL", f"unknown levelId {level_id}")
    if len(level_version) != 32:
        raise AdmissionError("LEVEL_VERSION", "levelVersion must be raw 32 bytes")
    if len(language_version) != 32:
        raise AdmissionError("LANGUAGE_VERSION", "languageVersion must be raw 32 bytes")
    tag = BODY_DOMAIN_TAG.encode("ascii")
    lid = level_id.encode("ascii")
    lang = language_id.encode("ascii")
    parts = [
        u8(len(tag)) + tag,
        u8(len(lid)) + lid,
        u8(len(level_version)) + level_version,
        u8(len(lang)) + lang,
        u8(len(language_version)) + language_version,
        u32be(len(payload)) + payload,
    ]
    return b"".join(parts)


def body_identity(frame: bytes) -> str:
    return "sha256:" + sha256(frame)


def ts_source_variant(path: str) -> str:
    """Longest-suffix table. .d.ts is never read as .ts."""
    p = path.lower()
    table = [
        (".d.ts", "ts-declaration"),
        (".tsx", "tsx"),
        (".mts", "mts"),
        (".cts", "cts"),
        (".ts", "ts"),
        (".jsx", "jsx"),
        (".mjs", "mjs"),
        (".cjs", "cjs"),
        (".js", "js"),
    ]
    for suf, var in table:
        if p.endswith(suf):
            return var
    raise AdmissionError("BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN", f"unlisted suffix for {path}")


def body_language_id_for_variant(variant: str) -> str:
    if variant in ("ts", "tsx", "ts-declaration", "mts", "cts"):
        return "typescript"
    if variant in ("js", "jsx", "mjs", "cjs"):
        return "javascript"
    raise AdmissionError("VARIANT", f"unknown sourceVariant {variant}")


def sort_canonical_set(items: list[Any]) -> list[Any]:
    encoded = [(encode_c(it), it) for it in items]
    encoded.sort(key=lambda t: t[0])
    out = []
    prev = None
    for b, it in encoded:
        if prev is not None and b == prev:
            raise AdmissionError("SET_DUP", "canonical-set duplicate")
        prev = b
        out.append(it)
    return out


def sort_by_keys(items: list[dict], keys: list[str]) -> list[dict]:
    def keyfn(it: dict) -> bytes:
        return b"\x00".join(str(it[k]).encode("utf-8") for k in keys)
    items = list(items)
    items.sort(key=keyfn)
    prev = None
    for it in items:
        k = keyfn(it)
        if prev is not None and k == prev:
            raise AdmissionError("SET_DUP", f"duplicate sort key {keys}")
        prev = k
    return items


def sort_utf8(items: list[str]) -> list[str]:
    items = list(items)
    items.sort(key=lambda s: s.encode("utf-8"))
    prev = None
    for s in items:
        b = s.encode("utf-8")
        if prev is not None and b == prev:
            raise AdmissionError("SET_DUP", "utf8-set duplicate")
        prev = b
    return items
