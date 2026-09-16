"""FACT-IDENTITY framed body identity from fact-identity-policy.v2 canonicalisationSchema
and relation-payload-schemas.v2 bodyIdentityJoin."""
from __future__ import annotations

import hashlib
from typing import Any

from . import canonical

DOMAIN_TAG = b"opensip.fact-identity.v1"


def u8_len_prefixed(b: bytes) -> bytes:
    if len(b) > 255:
        raise ValueError("u8 length overflow")
    return bytes([len(b)]) + b


def framed_body_identity(
    *,
    level_id: str,
    level_version_raw32: bytes,
    language_id: str,
    language_version_raw32: bytes,
    payload: bytes,
) -> tuple[bytes, str]:
    """Return (frame_bytes, sha256:<hex>)."""
    if len(level_version_raw32) != 32 or len(language_version_raw32) != 32:
        raise ValueError("levelVersion and languageVersion are raw 32-byte digests")
    pre = (
        u8_len_prefixed(DOMAIN_TAG)
        + u8_len_prefixed(level_id.encode("ascii"))
        + u8_len_prefixed(level_version_raw32)
        + u8_len_prefixed(language_id.encode("ascii"))
        + u8_len_prefixed(language_version_raw32)
        + len(payload).to_bytes(4, "big")
        + payload
    )
    digest = hashlib.sha256(pre).hexdigest()
    return pre, "sha256:" + digest


def l0_payload(body_bytes: bytes) -> bytes:
    return len(body_bytes).to_bytes(4, "big") + body_bytes


def token_stream(tokens: list[tuple[str, bytes]]) -> bytes:
    parts = [len(tokens).to_bytes(4, "big")]
    for kind, value in tokens:
        kb = kind.encode("utf-8")
        parts.append(len(kb).to_bytes(2, "big"))
        parts.append(kb)
        parts.append(len(value).to_bytes(4, "big"))
        parts.append(value)
    return b"".join(parts)


def language_version_raw32(record: dict) -> bytes:
    return hashlib.sha256(canonical.encode(record)).digest()
