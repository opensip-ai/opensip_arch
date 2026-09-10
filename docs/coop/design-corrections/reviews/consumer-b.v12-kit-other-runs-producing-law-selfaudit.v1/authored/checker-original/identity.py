"""H identities, frames, typed prefixes, CVE1, clone L0 body identity.

Owners:
- identity-and-evidence.md §3 (H formula, prefixes, digest representations)
- identity-schemas.v3.json x-opensip-digest-domains
- resolved-inputs.v2.json#planIdContract.canonicalValueEncoding (CVE1)
- fact-identity-policy.v2.json canonicalisationSchema.byteGrammar (L0)
- relation-payload-schemas.v2.json clones.bodyIdentityJoin
"""
from __future__ import annotations

import hashlib
import struct
import unicodedata
from typing import Any

from .canonical import encode_c, LexicalRefusal

PRODUCT = b"opensip.product.v1"
FRAME_NUL = b"\x00"

# Domain / prefix table from identity-and-evidence §3.
TYPED_PREFIX = {
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
PREFIX_TO_DOMAIN = {v: k for k, v in TYPED_PREFIX.items()}

CAP_MANIFEST_DOMAIN = b"opensip.capability-manifest.v1"
CLONE_DOMAIN_TAG = b"opensip.fact-identity.v1"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def h_frame(domain: str, canonical_payload: bytes) -> bytes:
    if any(ord(c) > 127 for c in domain):
        raise LexicalRefusal("H_DOMAIN_NON_ASCII", domain)
    return (
        PRODUCT
        + FRAME_NUL
        + domain.encode("ascii")
        + FRAME_NUL
        + struct.pack(">Q", len(canonical_payload))
        + canonical_payload
    )


def H(domain: str, descriptor: Any) -> str:
    return sha256(h_frame(domain, encode_c(descriptor)))


def typed_id(domain: str, descriptor: Any) -> str:
    prefix = TYPED_PREFIX[domain]
    return f"{prefix}:{H(domain, descriptor)}"


def parse_h_frame(raw: bytes) -> dict[str, Any]:
    if not raw.startswith(PRODUCT + FRAME_NUL):
        raise LexicalRefusal("H_FRAME_PREFIX", "missing opensip.product.v1 NUL prefix")
    rest = raw[len(PRODUCT) + 1 :]
    z = rest.find(FRAME_NUL)
    if z < 0:
        raise LexicalRefusal("H_FRAME_DOMAIN", "missing domain NUL")
    try:
        domain = rest[:z].decode("ascii")
    except UnicodeDecodeError as e:
        raise LexicalRefusal("H_FRAME_DOMAIN", str(e)) from e
    rest = rest[z + 1 :]
    if len(rest) < 8:
        raise LexicalRefusal("H_FRAME_LENGTH", "short length field")
    (n,) = struct.unpack(">Q", rest[:8])
    payload = rest[8:]
    if len(payload) != n:
        raise LexicalRefusal("H_FRAME_LENGTH", f"declared {n} remaining {len(payload)}")
    return {"domain": domain, "payload": payload, "frame": raw}


def parse_typed_id(value: str) -> tuple[str, str]:
    if ":" not in value:
        raise LexicalRefusal("TYPED_ID", f"unprefixed {value!r}")
    prefix, hexd = value.split(":", 1)
    if prefix not in PREFIX_TO_DOMAIN:
        raise LexicalRefusal("TYPED_ID_PREFIX", prefix)
    if len(hexd) != 64 or any(c not in "0123456789abcdef" for c in hexd):
        raise LexicalRefusal("TYPED_ID_HEX", hexd)
    return PREFIX_TO_DOMAIN[prefix], hexd


def sha256_text_to_hex(value: str) -> str:
    if not value.startswith("sha256:") or len(value) != 7 + 64:
        raise LexicalRefusal("SHA256_TEXT", value)
    hexd = value[7:]
    if any(c not in "0123456789abcdef" for c in hexd):
        raise LexicalRefusal("SHA256_TEXT", value)
    return hexd


def capability_manifest_id(committed_bytes: bytes) -> str:
    return sha256(CAP_MANIFEST_DOMAIN + FRAME_NUL + committed_bytes)


# --- CVE1 (resolved-inputs.v2.json planIdContract.canonicalValueEncoding) ---

CVE1_NULL = b"\x00"
CVE1_FALSE = b"\x01"
CVE1_TRUE = b"\x02"
CVE1_U64 = b"\x03"
CVE1_NFC_STRING = b"\x04"
CVE1_ARRAY = b"\x05"
CVE1_MAP = b"\x06"
CVE1_I64 = b"\x07"


def cve1_encode(value: Any) -> bytes:
    if value is None:
        return CVE1_NULL
    if value is False:
        return CVE1_FALSE
    if value is True:
        return CVE1_TRUE
    if isinstance(value, bool):
        return CVE1_TRUE if value else CVE1_FALSE
    if isinstance(value, int) and not isinstance(value, bool):
        if 0 <= value <= (2**64 - 1):
            return CVE1_U64 + struct.pack(">Q", value)
        if -(2**63) <= value < 0:
            return CVE1_I64 + struct.pack(">q", value)
        raise LexicalRefusal("CVE1_INTEGER", str(value))
    if isinstance(value, str):
        nfc = unicodedata.normalize("NFC", value)
        if nfc != value:
            raise LexicalRefusal("CVE1_NON_NFC", value)
        raw = value.encode("utf-8")
        return CVE1_NFC_STRING + struct.pack(">I", len(raw)) + raw
    if isinstance(value, list):
        parts = [cve1_encode(v) for v in value]
        return CVE1_ARRAY + struct.pack(">I", len(value)) + b"".join(parts)
    if isinstance(value, dict):
        items = []
        for k, v in value.items():
            if not isinstance(k, str):
                raise LexicalRefusal("CVE1_MAP_KEY", type(k).__name__)
            nfc = unicodedata.normalize("NFC", k)
            if nfc != k:
                raise LexicalRefusal("CVE1_NON_NFC_KEY", k)
            items.append((k.encode("utf-8"), cve1_encode(k), cve1_encode(v)))
        items.sort(key=lambda t: t[0])
        keys = [t[0] for t in items]
        if len(set(keys)) != len(keys):
            raise LexicalRefusal("CVE1_DUP_KEY", "duplicate map key")
        body = b"".join(t[1] + t[2] for t in items)
        return CVE1_MAP + struct.pack(">I", len(items)) + body
    raise LexicalRefusal("CVE1_TYPE", type(value).__name__)


def u8_len_prefixed(data: bytes) -> bytes:
    if len(data) > 255:
        raise LexicalRefusal("U8_LEN", f"component length {len(data)} exceeds u8")
    return bytes([len(data)]) + data


def clone_l0_body_identity(
    *,
    body_span: bytes,
    level_id: str,
    level_version_raw32: bytes,
    language_id: str,
    language_version_raw32: bytes,
) -> str:
    """fact-identity-policy.v2 byteGrammar L0-verbatim.

    Preimage: u8 tag_len||tag || u8 levelId_len||levelId || u8 levelVersion_len||levelVersion
              || u8 languageId_len||languageId || u8 languageVersion_len||languageVersion
              || u32be payload_len || payload
    L0 payload: u32be raw_byte_len || exact snapshot body-span bytes
    Output: sha256:<64 hex>
    """
    if level_id != "L0-verbatim":
        raise LexicalRefusal("CLONE_LEVEL", level_id)
    if len(level_version_raw32) != 32 or len(language_version_raw32) != 32:
        raise LexicalRefusal("CLONE_VERSION_WIDTH", "levelVersion/languageVersion must be raw 32 bytes")
    payload = struct.pack(">I", len(body_span)) + body_span
    preimage = (
        u8_len_prefixed(CLONE_DOMAIN_TAG)
        + u8_len_prefixed(level_id.encode("ascii"))
        + u8_len_prefixed(level_version_raw32)
        + u8_len_prefixed(language_id.encode("ascii"))
        + u8_len_prefixed(language_version_raw32)
        + struct.pack(">I", len(payload))
        + payload
    )
    return "sha256:" + sha256(preimage)
