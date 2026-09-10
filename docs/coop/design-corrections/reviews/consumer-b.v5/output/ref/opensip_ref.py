"""Blind-consumer reference helper for OpenSIP DR-011-R10.

Written from the contract PROSE + the machine-readable registries in the kit only.
No author model, checker, fixture or golden was read.  Every rule implemented here
cites the selector it came from in a comment.

Sources (all inside the verified consumer kit):
  C / H                       identity-and-evidence.md section 3
  digest law + annotations    foundation/identity-schemas.v2.json #/x-opensip-digest-domains
  payload registry            foundation/identity-schemas.v2.json #/x-opensip-payload-registry
  relation registry           foundation/relation-payload-schemas.v2.json #/x-opensip-relation-registry
  body identity frame         docs/coop/artifacts/fact-identity-policy.v2.json #/canonicalisationSchema
  CVE1                        docs/coop/artifacts/resolved-inputs.v2.json #/planIdContract/canonicalValueEncoding
  capability manifest id      docs/coop/artifacts/delivery.v4.json CAP-MANIFEST-ID-V1
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import struct
import unicodedata

KIT = "/tmp/opensip-design-corrections/consumer-b.v5/subject"

# ---------------------------------------------------------------------------
# 1. Exact typed admission  (identity-and-evidence section 3, admission section 1)
# ---------------------------------------------------------------------------


class Refuse(Exception):
    def __init__(self, code, detail=""):
        super().__init__(f"{code}:{detail}" if detail else code)
        self.code = code
        self.detail = detail


MIN_I = -(2**63)
MAX_U = 2**64 - 1

_INT_TOKEN = re.compile(r"^-?(0|[1-9][0-9]*)$")


class _Int(int):
    """Marker for an integer that arrived as an ordinary integer token."""


def _object_pairs(pairs):
    seen = set()
    out = {}
    for k, v in pairs:
        if k in seen:
            raise Refuse("ADMIT_DUPLICATE_KEY", k)
        seen.add(k)
        out[k] = v
    return out


def _no_float(x):
    raise Refuse("ADMIT_NONINTEGER_NUMBER", str(x))


def parse(text_bytes):
    """Lexical admission before deserialisation loses information.

    Refuses duplicate keys, floating/exponent tokens, -0, nonfinite tokens,
    malformed UTF-8, non-scalar Unicode (lone surrogates), out-of-range integers.
    """
    if isinstance(text_bytes, str):
        raw = text_bytes.encode("utf-8", "surrogatepass")
    else:
        raw = text_bytes
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refuse("ADMIT_MALFORMED_UTF8", str(exc))
    for ch in text:
        if 0xD800 <= ord(ch) <= 0xDFFF:
            raise Refuse("ADMIT_NON_SCALAR_UNICODE", hex(ord(ch)))
    # -0 / 1.0 / 1e0 / Infinity / NaN are all rejected by parse_int/parse_float hooks
    def _pi(s):
        if not _INT_TOKEN.match(s):
            raise Refuse("ADMIT_INTEGER_TOKEN", s)
        if s == "-0":
            raise Refuse("ADMIT_NEGATIVE_ZERO", s)
        v = int(s)
        if v < MIN_I or v > MAX_U:
            raise Refuse("ADMIT_INTEGER_RANGE", s)
        return v

    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_pairs,
            parse_int=_pi,
            parse_float=_no_float,
            parse_constant=lambda c: (_ for _ in ()).throw(Refuse("ADMIT_NONFINITE", c)),
        )
    except Refuse:
        raise
    except json.JSONDecodeError as exc:
        raise Refuse("ADMIT_JSON_SYNTAX", str(exc))
    check_bounds(value)
    return value


MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32


def check_bounds(value, _depth=0):
    """Root container counts as 1; scalar leaves and object keys add no depth."""
    if isinstance(value, (dict, list)):
        d = _depth + 1
        if d > MAX_DEPTH:
            raise Refuse("ADMIT_DEPTH", str(d))
        items = value.values() if isinstance(value, dict) else value
        for v in items:
            check_bounds(v, d)
    elif isinstance(value, bool):
        return
    elif isinstance(value, int):
        if value < MIN_I or value > MAX_U:
            raise Refuse("ADMIT_INTEGER_RANGE", str(value))
    elif isinstance(value, float):
        raise Refuse("ADMIT_NONINTEGER_NUMBER", repr(value))


# ---------------------------------------------------------------------------
# 2. C  -- the canonical encoder (identity-and-evidence section 3)
# ---------------------------------------------------------------------------

_ESC = {
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
}


def _c_string(s):
    out = ['"']
    for ch in s:
        o = ord(ch)
        if 0xD800 <= o <= 0xDFFF:
            raise Refuse("ADMIT_NON_SCALAR_UNICODE", hex(o))
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif o in _ESC:
            out.append(_ESC[o])
        elif o < 0x20:
            out.append("\\u%04x" % o)  # lowercase \u00xx, controls only
        else:
            out.append(ch)  # U+007F and U+2028 stay unescaped; slash not escaped
    out.append('"')
    return "".join(out)


def C(value):
    """Canonical JSON bytes.  Keys UTF-8 byte-ordered; arrays in ADMITTED order."""
    return _c(value).encode("utf-8")


def _c(value):
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        if value < MIN_I or value > MAX_U:
            raise Refuse("ADMIT_INTEGER_RANGE", str(value))
        return str(value)  # shortest ordinary decimal integer
    if isinstance(value, float):
        raise Refuse("ADMIT_NONINTEGER_NUMBER", repr(value))
    if isinstance(value, str):
        return _c_string(value)
    if isinstance(value, list):
        return "[" + ",".join(_c(v) for v in value) + "]"  # C never sorts
    if isinstance(value, dict):
        keys = sorted(value.keys(), key=lambda k: k.encode("utf-8"))
        return "{" + ",".join(_c_string(k) + ":" + _c(value[k]) for k in keys) + "}"
    raise Refuse("ADMIT_UNSUPPORTED_TYPE", type(value).__name__)


# ---------------------------------------------------------------------------
# 3. H and the retained preimage frame (identity-and-evidence section 3)
# ---------------------------------------------------------------------------

_PREFIX_LITERAL = b"opensip.product.v1"

# "Domain / prefix" column of the identity section 3 table.
DOMAIN_PREFIX = {
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


def frame(domain, descriptor):
    body = C(descriptor)
    return (
        _PREFIX_LITERAL
        + b"\x00"
        + domain.encode("ascii")
        + b"\x00"
        + struct.pack(">Q", len(body))
        + body
    )


def H(domain, descriptor):
    return hashlib.sha256(frame(domain, descriptor)).hexdigest()


def ident(domain, descriptor):
    return DOMAIN_PREFIX[domain] + ":" + H(domain, descriptor)


def sha256_text(domain, descriptor):
    """Native Sha256Text spelling of the SAME H digest."""
    return "sha256:" + H(domain, descriptor)


def raw(record):
    """canonical-record representation: raw SHA-256 of C(record)."""
    return hashlib.sha256(C(record)).hexdigest()


def raw_bytes(b):
    return hashlib.sha256(b).hexdigest()


class CAS:
    """One content-addressed store keyed by raw SHA-256, as section 3 states.

    It retains raw artifacts, canonical records AND H preimage frames, because
    H(D,X) is SHA256 of the framed preimage.
    """

    def __init__(self):
        self.objects = {}

    def put_bytes(self, b):
        d = raw_bytes(b)
        self.objects[d] = b
        return d

    def put_record(self, record):
        return self.put_bytes(C(record))

    def put_frame(self, domain, descriptor):
        return self.put_bytes(frame(domain, descriptor))

    def get(self, digest):
        if digest not in self.objects:
            raise Refuse("EVIDENCE_MISSING", digest)
        return self.objects[digest]

    def parse_frame(self, digest, expected_domains, registry_validate=None):
        """Exact frame admission.  Never a blob escape (section 3, closing digest law)."""
        b = self.get(digest)
        if not b.startswith(_PREFIX_LITERAL + b"\x00"):
            raise Refuse("FRAME_PREFIX", digest)
        rest = b[len(_PREFIX_LITERAL) + 1 :]
        nul = rest.index(b"\x00")
        domain = rest[:nul].decode("ascii")
        if domain not in expected_domains:
            raise Refuse("FRAME_DOMAIN_NOT_IN_SET", domain)
        rest = rest[nul + 1 :]
        declared = struct.unpack(">Q", rest[:8])[0]
        payload = rest[8:]
        if declared != len(payload):
            raise Refuse("FRAME_LENGTH", str(declared))
        parsed = parse(payload)
        if C(parsed) != payload:
            raise Refuse("FRAME_NOT_CANONICAL", digest)
        if registry_validate is not None:
            registry_validate(domain, parsed)
        if hashlib.sha256(b).hexdigest() != digest:
            raise Refuse("FRAME_DIGEST", digest)
        return domain, parsed


# ---------------------------------------------------------------------------
# 4. CVE1 and capabilityManifestId  (resolved-inputs.v2 + delivery.v4)
# ---------------------------------------------------------------------------


def cve1(value):
    if value is None:
        return b"\x00"
    if value is True:
        return b"\x02"
    if value is False:
        return b"\x01"
    if isinstance(value, int):
        if 0 <= value <= 2**64 - 1:
            return b"\x03" + struct.pack(">Q", value)
        if -(2**63) <= value < 0:
            return b"\x07" + struct.pack(">q", value)
        raise Refuse("CVE1_INTEGER_RANGE", str(value))
    if isinstance(value, float):
        raise Refuse("CVE1_FLOAT_FORBIDDEN", repr(value))
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise Refuse("CVE1_NOT_NFC", value)
        b = value.encode("utf-8")
        return b"\x04" + struct.pack(">I", len(b)) + b
    if isinstance(value, list):
        return b"\x05" + struct.pack(">I", len(value)) + b"".join(cve1(v) for v in value)
    if isinstance(value, dict):
        keys = list(value.keys())
        if len(set(keys)) != len(keys):
            raise Refuse("CVE1_DUPLICATE_KEY", "")
        for k in keys:
            if not isinstance(k, str):
                raise Refuse("CVE1_NON_STRING_KEY", repr(k))
            if unicodedata.normalize("NFC", k) != k:
                raise Refuse("CVE1_NOT_NFC", k)
        keys.sort(key=lambda k: k.encode("utf-8"))
        out = b"\x06" + struct.pack(">I", len(keys))
        for k in keys:
            out += cve1(k) + cve1(value[k])
        return out
    raise Refuse("CVE1_UNSUPPORTED_TYPE", type(value).__name__)


CAP_MANIFEST_DOMAIN = b"opensip.capability-manifest.v1"


def capability_manifest_id(manifest):
    committed = cve1(manifest)
    return committed, hashlib.sha256(CAP_MANIFEST_DOMAIN + b"\x00" + committed).hexdigest()


# ---------------------------------------------------------------------------
# 5. Body identity frame  (fact-identity-policy.v2 canonicalisationSchema)
# ---------------------------------------------------------------------------

BODY_DOMAIN_TAG = b"opensip.fact-identity.v1"


def _u8p(b):
    if len(b) > 255:
        raise Refuse("BODY_COMPONENT_TOO_LONG", str(len(b)))
    return bytes([len(b)]) + b


def body_payload_L0(body_bytes):
    # payloadEncodingByLevel L0-verbatim: u32be raw_byte_len || exact body-span bytes
    return struct.pack(">I", len(body_bytes)) + body_bytes


def body_payload_tokens(tokens):
    # streamFraming: u32be token_count || token*
    # token = u16be kind_id_len || kind_id || u32be value_len || value
    out = struct.pack(">I", len(tokens))
    for kind, value in tokens:
        kb = kind.encode("utf-8")
        vb = value.encode("utf-8")
        out += struct.pack(">H", len(kb)) + kb + struct.pack(">I", len(vb)) + vb
    return out


def body_identity(level_id, level_version_raw32, language_id, language_version_raw32, payload):
    if len(level_version_raw32) != 32 or len(language_version_raw32) != 32:
        raise Refuse("BODY_FIXED_WIDTH", "levelVersion/languageVersion must be raw 32 bytes")
    pre = (
        _u8p(BODY_DOMAIN_TAG)
        + _u8p(level_id.encode("ascii"))
        + _u8p(level_version_raw32)
        + _u8p(language_id.encode("ascii"))
        + _u8p(language_version_raw32)
        + struct.pack(">I", len(payload))
        + payload
    )
    return pre, "sha256:" + hashlib.sha256(pre).hexdigest()


def language_version_raw32(body_language_version_record):
    """identity section 3: raw 32 bytes of SHA-256(C(body-language-version))."""
    return hashlib.sha256(C(body_language_version_record)).digest()


# ---------------------------------------------------------------------------
# 6. Schema access + validation
# ---------------------------------------------------------------------------

import jsonschema  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402
from referencing import Registry, Resource  # noqa: E402

_DOCS = {}


def doc(relpath):
    if relpath not in _DOCS:
        with open(os.path.join(KIT, relpath), "rb") as fh:
            b = fh.read()
        _DOCS[relpath] = (json.loads(b.decode("utf-8")), b)
    return _DOCS[relpath]


def doc_json(relpath):
    return doc(relpath)[0]


def doc_digest(relpath):
    """raw-artifact: raw SHA-256 of the EXACT FULL document bytes."""
    return raw_bytes(doc(relpath)[1])


_PATHS = {
    "identity": "docs/coop/design-corrections/foundation/identity-schemas.v2.json",
    "relation": "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
    "native": "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "matrix": "docs/coop/design-corrections/native/native-capability-matrix.v2.json",
    "common": "docs/coop/design-corrections/workflows/schemas/common.schema.json",
    "policy-document": "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
    "imported-evidence": "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
    "test-execution": "docs/coop/design-corrections/workflows/schemas/test-execution.schema.json",
    "invocation-record": "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json",
    "command-envelope": "docs/coop/design-corrections/workflows/schemas/command-envelope.schema.json",
    "comparison-result": "docs/coop/design-corrections/workflows/schemas/comparison-result.schema.json",
    "repair": "docs/coop/design-corrections/workflows/schemas/repair.schema.json",
    "review": "docs/coop/design-corrections/workflows/schemas/review.schema.json",
    "graph-query": "docs/coop/design-corrections/workflows/schemas/graph-query.schema.json",
    "policy-test": "docs/coop/design-corrections/workflows/schemas/policy-test.schema.json",
    "baseline-artifact": "docs/coop/design-corrections/workflows/schemas/baseline-artifact.schema.json",
    "command-inventory-schema": "docs/coop/design-corrections/workflows/schemas/command-inventory.schema.json",
    "import-source-context": "docs/coop/design-corrections/foundation/import-source-context.schema.json",
    "product-configuration": "docs/coop/design-corrections/foundation/product-configuration.schema.v2.json",
}


def _registry():
    reg = Registry()
    for key, rel in _PATHS.items():
        d = doc_json(rel)
        if "$id" in d:
            reg = reg.with_resource(d["$id"], Resource.from_contents(d))
    return reg


_REG = _registry()


def validate(bundle, selector, instance):
    """Validate `instance` against `bundle#selector` through the pinned local closure."""
    d = doc_json(_PATHS[bundle])
    doc_id = d["$id"]
    wrapper = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$ref": doc_id + ("" if selector == "#" else selector),
    }
    v = Draft202012Validator(wrapper, registry=_REG)
    errs = sorted(v.iter_errors(instance), key=lambda e: list(e.absolute_path))
    if errs:
        e = errs[0]
        raise Refuse(
            "SCHEMA_INVALID",
            f"{bundle}{selector} @ /{'/'.join(str(p) for p in e.absolute_path)}: {e.message}",
        )
    return True


def schema_ok(bundle, selector, instance):
    try:
        validate(bundle, selector, instance)
        return True, None
    except Refuse as exc:
        return False, exc.detail


# ---------------------------------------------------------------------------
# 7. Registries loaded from the kit
# ---------------------------------------------------------------------------

IDENTITY = doc_json(_PATHS["identity"])
RELATION_DOC = doc_json(_PATHS["relation"])
NATIVE = doc_json(_PATHS["native"])
MATRIX = doc_json(_PATHS["matrix"])
COMMON = doc_json(_PATHS["common"])

RELATION_REGISTRY = RELATION_DOC["x-opensip-relation-registry"]["relations"]
ANCHOR_LAW = RELATION_DOC["x-opensip-relation-registry"]["anchorLaw"]
DIGEST_DOMAINS = IDENTITY["x-opensip-digest-domains"]
DOMAIN_SETS = DIGEST_DOMAINS["domainSets"]
PAYLOAD_REGISTRY = IDENTITY["x-opensip-payload-registry"]
GRAMMAR_REGISTRY = NATIVE["x-opensip-grammar-capability-registry"]
CAUSE_REGISTRY = NATIVE["x-opensip-deficiency-cause-registry"]["deficiencies"]
ROUTE_REGISTRY = NATIVE["x-opensip-public-route-registry"]
CAPABILITY_IDS = MATRIX["capabilityIdLaw"]["members"]
LANGUAGE_MODES = MATRIX["languageModes"]
CELLS = {(c["capability"], c["mode"]): c for c in MATRIX["cells"]}

RELATION_DOC_DIGEST = doc_digest(_PATHS["relation"])
NATIVE_DOC_DIGEST = doc_digest(_PATHS["native"])
POLICY_DOC_DIGEST = doc_digest(_PATHS["policy-document"])
IMPORTED_EVIDENCE_DIGEST = doc_digest(_PATHS["imported-evidence"])
TEST_EXECUTION_DIGEST = doc_digest(_PATHS["test-execution"])
COMMON_DOC_DIGEST = doc_digest(_PATHS["common"])
IMPORT_SOURCE_CONTEXT_DIGEST = doc_digest(_PATHS["import-source-context"])


def relation_selector(rel):
    return RELATION_REGISTRY[rel]["selector"]


def ladder(rel):
    row = RELATION_REGISTRY.get(rel)
    if not row or not row.get("ladder"):
        # "no empty-ladder fallback: a relation with no ladder is a registry defect"
        raise Refuse("RELATION_LADDER_MISSING", rel)
    return row["ladder"]


def rung_index(rel, rung):
    lad = ladder(rel)
    if rung not in lad:
        raise Refuse("RUNG_NOT_IN_RELATION_LADDER", f"{rel}@{rung}")
    return lad.index(rung)


def anchor_cardinality(rel):
    law = RELATION_REGISTRY[rel]["anchorLaw"]
    if "cardinality" in law:
        return ("exact", law["cardinality"])
    return ("min", law["minimum"])
