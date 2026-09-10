"""Blind consumer-B independent reconstruction of the OpenSIP product canonical
encoder C, the identity frame H(D,X), the CVE1 capability-manifest encoder and the
FACT-IDENTITY body frame.

Written from prose only:
  - identity-and-evidence.md sections 2 and 3 (canonical JSON, H, prefixes, orders)
  - admission-and-qualification.md section 1 (lexical/numeric admission)
  - resolved-inputs.v2.json#planIdContract.canonicalValueEncoding (CVE1)
  - delivery.v4.json derivedFrom.operations[17] (CAP-MANIFEST-ID-V1 recipe/gates)
  - fact-identity-policy.v2.json#canonicalisationSchema (framed body preimage)

No author reference implementation was read. Nothing here is product code.
"""

import hashlib
import json
import re
import struct
import unicodedata

# --------------------------------------------------------------------------
# 1. Exact lexical/numeric admission (admission-and-qualification section 1,
#    identity-and-evidence section 3 "Before deserialization loses lexical
#    information").
# --------------------------------------------------------------------------

MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32
INT_MIN = -(2 ** 63)
INT_MAX = 2 ** 64 - 1

_INT_TOKEN = re.compile(r"^-?(?:0|[1-9][0-9]*)$")


class Refusal(Exception):
    """Typed admission refusal. Carries a short machine cause."""

    def __init__(self, cause, detail=""):
        super().__init__(f"{cause}{(': ' + detail) if detail else ''}")
        self.cause = cause
        self.detail = detail


def _reject_duplicate_keys(pairs):
    seen = set()
    out = {}
    for k, v in pairs:
        if k in seen:
            raise Refusal("DUPLICATE_KEY", k)
        seen.add(k)
        out[k] = v
    return out


class _Int(int):
    """An integer that was admitted from an ordinary integer token."""


def _number_hook(tok):
    # json calls parse_int for integer-looking tokens and parse_float for the rest.
    raise Refusal("NON_INTEGER_NUMBER", tok)


def _int_hook(tok):
    if not _INT_TOKEN.match(tok):
        raise Refusal("MALFORMED_INTEGER_TOKEN", tok)
    if tok == "-0":
        raise Refusal("NEGATIVE_ZERO", tok)
    v = int(tok)
    if v < INT_MIN or v > INT_MAX:
        raise Refusal("INTEGER_OUT_OF_RANGE", tok)
    return _Int(v)


def _constant_hook(tok):
    # Infinity / -Infinity / NaN
    raise Refusal("NONFINITE_NUMBER", tok)


def _check_scalars_and_depth(v, depth=1):
    """Container depth: the root container counts as 1; scalar leaves and object
    keys add no container depth (identity section 3)."""
    if isinstance(v, (dict, list)) and depth > MAX_DEPTH:
        raise Refusal("DEPTH_EXCEEDED", str(depth))
    if isinstance(v, dict):
        for k, sub in v.items():
            _check_text(k)
            _check_scalars_and_depth(sub, depth + 1)
    elif isinstance(v, list):
        for sub in v:
            _check_scalars_and_depth(sub, depth + 1)
    elif isinstance(v, str):
        _check_text(v)
    elif isinstance(v, bool):
        pass
    elif isinstance(v, int):
        if v < INT_MIN or v > INT_MAX:
            raise Refusal("INTEGER_OUT_OF_RANGE", str(v))
    elif v is None:
        pass
    else:
        raise Refusal("UNADMITTED_SCALAR_TYPE", type(v).__name__)


def _check_text(s):
    for ch in s:
        cp = ord(ch)
        if 0xD800 <= cp <= 0xDFFF:
            raise Refusal("NON_SCALAR_UNICODE", hex(cp))
    try:
        s.encode("utf-8")
    except UnicodeEncodeError as exc:  # lone surrogate
        raise Refusal("MALFORMED_UTF8", str(exc))


def admit(text_bytes):
    """Admit descriptor bytes -> python value, with exact lexical admission.

    Refuses duplicate keys, floating/exponent tokens, -0, nonfinite tokens,
    malformed UTF-8, non-scalar Unicode, oversize and overdeep descriptors,
    before any identity is computed.
    """
    if not isinstance(text_bytes, (bytes, bytearray)):
        raise Refusal("NOT_BYTES")
    if len(text_bytes) > MAX_DESCRIPTOR_BYTES:
        raise Refusal("DESCRIPTOR_TOO_LARGE", str(len(text_bytes)))
    try:
        s = text_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refusal("MALFORMED_UTF8", str(exc))
    value = json.loads(
        s,
        object_pairs_hook=_reject_duplicate_keys,
        parse_float=_number_hook,
        parse_int=_int_hook,
        parse_constant=_constant_hook,
    )
    _check_scalars_and_depth(value, 1)
    return value


# --------------------------------------------------------------------------
# 2. C - the canonical JSON encoder (identity-and-evidence section 3).
#    UTF-8 byte-ordered keys, no whitespace, no trailing newline, no Unicode
#    normalization, shortest ordinary decimal integers, unescaped Unicode
#    scalars. Escape " and \\; use \\b\\t\\n\\f\\r; lowercase \\u00xx for the
#    other U+0000-001F controls; do not escape slash. Arrays encode IN THEIR
#    ADMITTED ORDER: C never sorts or deduplicates.
# --------------------------------------------------------------------------

_C0_ESCAPES = {
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
}


def _c_string(s):
    _check_text(s)
    out = ['"']
    for ch in s:
        cp = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif cp in _C0_ESCAPES:
            out.append(_C0_ESCAPES[cp])
        elif cp <= 0x1F:
            out.append("\\u%04x" % cp)  # lowercase hex
        else:
            out.append(ch)  # U+007F and U+2028 stay unescaped
    out.append('"')
    return "".join(out)


def _c(value):
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):  # booleans handled above and are distinct
        if value < INT_MIN or value > INT_MAX:
            raise Refusal("INTEGER_OUT_OF_RANGE", str(value))
        return str(value)  # shortest ordinary decimal integer
    if isinstance(value, float):
        raise Refusal("FLOAT_FORBIDDEN", repr(value))
    if isinstance(value, str):
        return _c_string(value)
    if isinstance(value, list):
        return "[" + ",".join(_c(v) for v in value) + "]"  # admitted order
    if isinstance(value, dict):
        items = sorted(value.items(), key=lambda kv: kv[0].encode("utf-8"))
        return "{" + ",".join(_c_string(k) + ":" + _c(v) for k, v in items) + "}"
    raise Refusal("UNADMITTED_SCALAR_TYPE", type(value).__name__)


def C(value):
    """Canonical bytes of an admitted value."""
    return _c(value).encode("utf-8")


# --------------------------------------------------------------------------
# 3. x-opensip-order - the closed array-order vocabulary (identity section 3).
#    C itself never sorts; admission refuses a deviation BEFORE hashing.
# --------------------------------------------------------------------------

ORDER_VOCAB = {
    "sequence", "canonical-set", "canonical-order", "utf8", "path",
    "numeric", "ordinal", "predicate", "ruleId", "waiverId",
}


def _order_key(annotation, item):
    if annotation in ("canonical-set", "canonical-order"):
        return C(item)
    if annotation == "utf8":
        if not isinstance(item, str):
            raise Refusal("ORDER_KEY_NOT_STRING")
        return item.encode("utf-8")
    if annotation == "path":
        return item["path"].encode("utf-8")
    if annotation == "numeric":
        if isinstance(item, bool) or not isinstance(item, int):
            raise Refusal("ORDER_KEY_NOT_INTEGER")
        return item
    if annotation == "ordinal":
        return item["ordinal"]
    if annotation == "predicate":
        return (item["ruleId"], item["subjectId"], item["predicateId"])
    if annotation in ("ruleId", "waiverId"):
        return item[annotation].encode("utf-8")
    if isinstance(annotation, dict) and "by" in annotation:
        return tuple(item[k].encode("utf-8") if isinstance(item[k], str) else item[k]
                     for k in annotation["by"])
    raise Refusal("ORDER_ANNOTATION_UNKNOWN", repr(annotation))


def check_order(array, annotation):
    """Admission check for a declared array order. Returns None or raises."""
    if annotation == "sequence":
        return
    if isinstance(annotation, str) and annotation not in ORDER_VOCAB:
        raise Refusal("ORDER_ANNOTATION_UNKNOWN", annotation)
    if isinstance(annotation, dict) and set(annotation) != {"by"}:
        raise Refusal("ORDER_ANNOTATION_UNKNOWN", repr(annotation))
    if annotation == "ordinal":
        for i, item in enumerate(array):
            if item.get("ordinal") != i:
                raise Refusal("ORDER_NOT_CONTIGUOUS_ORDINAL", str(i))
        return
    keys = [_order_key(annotation, it) for it in array]
    strict = annotation != "canonical-order"
    for a, b in zip(keys, keys[1:]):
        if strict and not (a < b):
            raise Refusal("ORDER_NOT_STRICTLY_ASCENDING", repr(b))
        if not strict and a > b:
            raise Refusal("ORDER_NOT_NONDECREASING", repr(b))
    if strict and len(set(map(repr, keys))) != len(keys):
        raise Refusal("ORDER_KEYS_NOT_UNIQUE")


def ordered(items, annotation):
    """Construct an array in its declared order (producer side)."""
    if annotation == "sequence":
        return list(items)
    if annotation == "ordinal":
        return sorted(items, key=lambda i: i["ordinal"])
    out = sorted(items, key=lambda i: _order_key(annotation, i))
    check_order(out, annotation)
    return out


# --------------------------------------------------------------------------
# 4. H(D, X) and the identifier prefixes (identity section 3).
#    H(D,X) = SHA256( "opensip.product.v1" || 00 || D || 00
#                     || uint64BE(len(C(X))) || C(X) )
# --------------------------------------------------------------------------

FRAME_PREFIX = b"opensip.product.v1"


def frame(domain, descriptor):
    body = C(descriptor)
    return (FRAME_PREFIX + b"\x00" + domain.encode("ascii") + b"\x00"
            + struct.pack(">Q", len(body)) + body)


def H(domain, descriptor):
    return hashlib.sha256(frame(domain, descriptor)).hexdigest()


PREFIX = {
    "snapshot": "snapshot2", "closure": "closure2", "import": "import2",
    "plan": "plan2", "subject-scope": "scope2", "fact": "fact2",
    "coverage": "coverage2", "view": "view2", "execution-plan": "exec-plan2",
    "finding-fingerprint": "finding-key2", "finding": "finding2",
    "proof-bundle": "proof2", "semantic-evidence": "evidence2",
    "evaluation-seal": "seal2", "run": "run2", "cache-key": "cache2",
    "regeneration-key": "regen2", "policy-derivation": "policy-derivation2",
}


def identifier(domain, descriptor):
    h = H(domain, descriptor)
    return f"{PREFIX[domain]}:{h}", h


def parse_frame(blob):
    """Exact frame admission (identity section 3 'the closing digest law')."""
    if not blob.startswith(FRAME_PREFIX + b"\x00"):
        raise Refusal("FRAME_PREFIX_MISMATCH")
    rest = blob[len(FRAME_PREFIX) + 1:]
    nul = rest.index(b"\x00")
    domain = rest[:nul].decode("ascii")
    rest = rest[nul + 1:]
    declared = struct.unpack(">Q", rest[:8])[0]
    payload = rest[8:]
    if declared != len(payload):
        raise Refusal("FRAME_LENGTH_MISMATCH", f"{declared}!={len(payload)}")
    parsed = admit(payload)
    if C(parsed) != payload:
        raise Refusal("FRAME_PAYLOAD_NOT_CANONICAL")
    return domain, parsed


def raw_sha256(value):
    """canonical-record representation: raw SHA256 of C(record)."""
    return hashlib.sha256(C(value)).hexdigest()


def raw_bytes_sha256(blob):
    """raw-artifact representation: raw SHA256 of exact artifact bytes."""
    return hashlib.sha256(blob).hexdigest()


# --------------------------------------------------------------------------
# 5. CVE1 (resolved-inputs.v2#planIdContract.canonicalValueEncoding) and
#    CAP-MANIFEST-ID-V1 (delivery.v4 op 17).
# --------------------------------------------------------------------------

CAP_MANIFEST_DOMAIN = "opensip.capability-manifest.v1"


def cve1(value):
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
        raise Refusal("CVE1_INTEGER_OUT_OF_RANGE", str(value))
    if isinstance(value, float):
        raise Refusal("CVE1_FLOAT_FORBIDDEN")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise Refusal("CVE1_STRING_NOT_NFC", value)
        b = value.encode("utf-8")
        return b"\x04" + struct.pack(">I", len(b)) + b
    if isinstance(value, list):
        return b"\x05" + struct.pack(">I", len(value)) + b"".join(cve1(v) for v in value)
    if isinstance(value, dict):
        keys = list(value)
        if len(set(keys)) != len(keys):
            raise Refusal("CVE1_DUPLICATE_MAP_KEY")
        for k in keys:
            if not isinstance(k, str):
                raise Refusal("CVE1_MAP_KEY_NOT_STRING")
            if unicodedata.normalize("NFC", k) != k:
                raise Refusal("CVE1_STRING_NOT_NFC", k)
        items = sorted(value.items(), key=lambda kv: kv[0].encode("utf-8"))
        return (b"\x06" + struct.pack(">I", len(items))
                + b"".join(cve1(k) + cve1(v) for k, v in items))
    raise Refusal("CVE1_UNADMITTED_TYPE", type(value).__name__)


# CapabilityManifestV1 admission gates ADM-TYPE / ADM-CLOSED / ADM-DOMAIN /
# ADM-ORDER (delivery.v4 op 17 admission), reconstructed from prose.
CM_RECORD_KEYS = {
    "CapabilityManifestV1": {"schemaVersion", "profile", "providers", "coverageForAbsent"},
    "ProviderCapability": {"providerId", "language", "providerVersionSource",
                           "toolchainIdentitySource", "relations", "platformIds"},
    "AbsentCapability": {"providerId", "language", "relationIds", "coverageState",
                         "deficiency"},
}
PLATFORM_ID_DOMAIN_V1 = {
    "all-supported", "linux-x86_64-gnu", "linux-aarch64-gnu", "macos-aarch64",
    "macos-x86_64", "windows-x86_64-msvc", "windows-aarch64-msvc", "linux-x86_64-musl",
}
RELATION_REGISTRY_12 = {
    "calls", "clones", "control-flow", "declares", "file", "imports", "literal",
    "package", "reachability", "references", "types", "vcs-change",
}
RELATION_LADDERS_INHERITED = {  # fact-plane.v1#relationRegistry.relations[].ladder
    "file": ["enumerated"], "package": ["manifest-declared"],
    "vcs-change": ["vcs-reported"], "declares": ["syntactic"],
    "literal": ["syntactic"], "control-flow": ["syntactic"],
    "imports": ["syntactic-specifier", "resolved-target"],
    "references": ["syntactic-name-match", "resolved-binding"],
    "calls": ["syntactic-callee-name", "resolved-callee"],
    "types": ["annotated", "checked"],
    "reachability": ["from-resolved-calls"], "clones": ["normalized-body-hash"],
    "unresolved-edge": ["observed"],  # native section 4.4
}
DEFICIENCY_VOCAB_5 = {
    "required-relation-missing", "provider-unavailable", "language-tier-unsupported",
    "budget-exhausted", "confidence-floor-unmet",
}


def _adm_type_string(x, where):
    if type(x) is not str:
        raise Refusal("ADM-TYPE", f"{where} is {type(x).__name__}, not string")


def _adm_type_int(x, where):
    if type(x) is not int and type(x) is not _Int:
        raise Refusal("ADM-TYPE", f"{where} is {type(x).__name__}, not integer")
    if isinstance(x, bool):
        raise Refusal("ADM-TYPE", f"{where} is boolean, not integer")


def _adm_closed(obj, record, where):
    if type(obj) is not dict:
        raise Refusal("ADM-CLOSED", f"{where} is not an object")
    if set(obj) != CM_RECORD_KEYS[record]:
        raise Refusal("ADM-CLOSED", f"{where} key set {sorted(obj)}")


def _ascending_unique(values, where):
    b = [v.encode("utf-8") for v in values]
    for x, y in zip(b, b[1:]):
        if not x < y:
            raise Refusal("ADM-ORDER", f"{where} not strictly ascending at {y!r}")


def admit_capability_manifest(m):
    """Four gates, all before encoding (delivery.v4 op 17 admission)."""
    _adm_closed(m, "CapabilityManifestV1", "CapabilityManifestV1")
    _adm_type_int(m["schemaVersion"], "schemaVersion")
    _adm_type_string(m["profile"], "profile")
    if type(m["providers"]) is not list or type(m["coverageForAbsent"]) is not list:
        raise Refusal("ADM-TYPE", "providers/coverageForAbsent not arrays")
    for i, p in enumerate(m["providers"]):
        _adm_closed(p, "ProviderCapability", f"providers[{i}]")
        for f in ("providerId", "language", "providerVersionSource",
                  "toolchainIdentitySource"):
            _adm_type_string(p[f], f"providers[{i}].{f}")
        if type(p["relations"]) is not dict:
            raise Refusal("ADM-TYPE", f"providers[{i}].relations not a map")
        for rk, rv in p["relations"].items():
            _adm_type_string(rv, f"providers[{i}].relations[{rk}]")
            if rk not in RELATION_REGISTRY_12:
                raise Refusal("ADM-DOMAIN", f"relation key {rk}")
            if rv not in RELATION_LADDERS_INHERITED[rk]:
                raise Refusal("ADM-DOMAIN", f"{rk} rung {rv}")
        if type(p["platformIds"]) is not list:
            raise Refusal("ADM-TYPE", f"providers[{i}].platformIds")
        for v in p["platformIds"]:
            _adm_type_string(v, "platformId")
            if v not in PLATFORM_ID_DOMAIN_V1:
                raise Refusal("ADM-DOMAIN", f"platformId {v}")
        _ascending_unique(p["platformIds"], f"providers[{i}].platformIds")
    for i, a in enumerate(m["coverageForAbsent"]):
        _adm_closed(a, "AbsentCapability", f"coverageForAbsent[{i}]")
        for f in ("providerId", "language", "coverageState", "deficiency"):
            _adm_type_string(a[f], f"coverageForAbsent[{i}].{f}")
        if a["coverageState"] != "unavailable":
            raise Refusal("ADM-DOMAIN", f"coverageState {a['coverageState']}")
        if a["deficiency"] not in DEFICIENCY_VOCAB_5:
            raise Refusal("ADM-DOMAIN", f"deficiency {a['deficiency']}")
        for v in a["relationIds"]:
            _adm_type_string(v, "relationId")
            if v not in RELATION_REGISTRY_12:
                raise Refusal("ADM-DOMAIN", f"relationId {v}")
        _ascending_unique(a["relationIds"], f"coverageForAbsent[{i}].relationIds")
    _ascending_unique([p["providerId"] for p in m["providers"]], "providers")
    _ascending_unique([a["providerId"] for a in m["coverageForAbsent"]],
                      "coverageForAbsent")
    return m


def capability_manifest_id(manifest):
    admit_capability_manifest(manifest)
    committed = cve1(manifest)
    digest = hashlib.sha256(
        CAP_MANIFEST_DOMAIN.encode("utf-8") + b"\x00" + committed).hexdigest()
    return digest, committed


# --------------------------------------------------------------------------
# 6. FACT-IDENTITY body frame (fact-identity-policy.v2#canonicalisationSchema,
#    reused verbatim by identity-and-evidence "clones" section).
#      u8 len||"opensip.fact-identity.v1"
#      u8 len||levelId
#      u8 len||levelVersion   (RAW 32 digest bytes, never hex text)
#      u8 len||languageId
#      u8 len||languageVersion(RAW 32 bytes of SHA256(C(body-language-version)))
#      u32be len||payload
# --------------------------------------------------------------------------

BODY_DOMAIN_TAG = b"opensip.fact-identity.v1"


def _u8f(b):
    if len(b) > 255:
        raise Refusal("BODY_FRAME_COMPONENT_TOO_LONG", str(len(b)))
    return bytes([len(b)]) + b


def body_language_version_bytes(record):
    """languageVersion component = raw 32 bytes of SHA256(C(body-language-version))."""
    return hashlib.sha256(C(record)).digest()


def framed_token_stream(tokens):
    """u32be token_count || (u16be kind_len||kind || u32be val_len||val)*"""
    out = struct.pack(">I", len(tokens))
    for kind, val in tokens:
        kb = kind.encode("utf-8")
        vb = val if isinstance(val, bytes) else val.encode("utf-8")
        out += struct.pack(">H", len(kb)) + kb + struct.pack(">I", len(vb)) + vb
    return out


def body_identity(level_id, level_version_raw32, language_id,
                  language_version_raw32, payload_bytes):
    pre = (_u8f(BODY_DOMAIN_TAG)
           + _u8f(level_id.encode("ascii"))
           + _u8f(level_version_raw32)
           + _u8f(language_id.encode("ascii"))
           + _u8f(language_version_raw32)
           + struct.pack(">I", len(payload_bytes)) + payload_bytes)
    return "sha256:" + hashlib.sha256(pre).hexdigest(), pre


def l0_payload(span_bytes):
    """L0-verbatim: u32be raw_byte_len || exact body-span bytes."""
    return struct.pack(">I", len(span_bytes)) + span_bytes


# TypeScript closed longest-suffix source-variant table (identity clones section,
# mirrored machine-readably in the typescript universe languageVersionBinding).
TS_VARIANT_TABLE = {
    ".d.ts": "ts-declaration", ".ts": "ts", ".tsx": "tsx", ".mts": "mts",
    ".cts": "cts", ".js": "js", ".jsx": "jsx", ".mjs": "mjs", ".cjs": "cjs",
}
TS_VARIANT_LANGUAGE = {
    "ts": "typescript", "tsx": "typescript", "ts-declaration": "typescript",
    "mts": "typescript", "cts": "typescript",
    "js": "javascript", "jsx": "javascript", "mjs": "javascript",
    "cjs": "javascript",
}


def ts_source_variant(path):
    best = None
    for suffix in TS_VARIANT_TABLE:
        if path.endswith(suffix) and (best is None or len(suffix) > len(best)):
            best = suffix
    if best is None:
        raise Refusal("BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN", path)
    return TS_VARIANT_TABLE[best]


def rust_effective_edition(ownership, edition_map, anchor_path):
    """The selected-compilation-target edition law, in the fixed order of decision
    (identity clones section / native section 11 selectionLaw)."""
    if ownership is None:
        raise Refusal("BODY_LANGUAGE_OWNERSHIP_REQUIRED", anchor_path)
    if ownership["enumeration"] == "partial":
        raise Refusal("BODY_LANGUAGE_OWNER_UNENUMERATED", anchor_path)
    rows = [r for r in ownership["ownership"] if r["path"] == anchor_path]
    if not rows:
        raise Refusal("BODY_LANGUAGE_OWNER_NOT_COMPILED", anchor_path)
    selected = set(ownership["selectedUnitIds"])
    rows = [r for r in rows if r["unitId"] in selected]
    if not rows:
        raise Refusal("BODY_LANGUAGE_OWNER_NOT_SELECTED", anchor_path)
    units = {u["unitId"]: u for u in ownership["units"]}
    editions = set()
    for r in rows:
        u = units.get(r["unitId"])
        if u is None:
            raise Refusal("OWNERSHIP_UNIT_UNDECLARED", r["unitId"])
        editions.add(u["targetEdition"] if u["targetEdition"] is not None
                     else edition_map[u["crateName"]])
    if len(editions) != 1:
        raise Refusal("BODY_LANGUAGE_OWNER_AMBIGUOUS",
                      f"{anchor_path}:{sorted(editions)}")
    return editions.pop()


def unit_id(marker_path, target_kind, target_name):
    """unitId = H(native.compilation-unit.v1, UnitIdentityV1{...}), sha256: form."""
    rec = {"schemaVersion": 1, "markerPath": marker_path,
           "targetKind": target_kind, "targetName": target_name}
    return "sha256:" + H("native.compilation-unit.v1", rec), rec
