"""FACT-IDENTITY bodyIdentity framing from identity-and-evidence §3 clones recipe."""
from __future__ import annotations

import hashlib

from helpers.canonical import C, sha256_hex


def framed_component_u8(data: bytes) -> bytes:
    if len(data) > 255:
        raise ValueError("u8 length overflow")
    return bytes([len(data)]) + data


def body_identity_frame(
    *,
    level_id: str,
    level_version_raw32: bytes,
    language_id: str,
    language_version_raw32: bytes,
    payload: bytes,
) -> bytes:
    if len(level_version_raw32) != 32 or len(language_version_raw32) != 32:
        raise ValueError("levelVersion and languageVersion must be raw 32 bytes")
    return (
        framed_component_u8(b"opensip.fact-identity.v1")
        + framed_component_u8(level_id.encode("utf-8"))
        + framed_component_u8(level_version_raw32)
        + framed_component_u8(language_id.encode("utf-8"))
        + framed_component_u8(language_version_raw32)
        + len(payload).to_bytes(4, "big")
        + payload
    )


def l0_payload(body_span: bytes) -> bytes:
    """L0 payload is itself length-prefixed: u32be raw_byte_len || span. Outer frame adds another u32be."""
    return len(body_span).to_bytes(4, "big") + body_span


def l_token_payload(tokens: list[tuple[str, bytes]]) -> bytes:
    """L1–L3: u32be token_count || (u32be kind_len||kind || u32be value_len||value)*"""
    parts = [len(tokens).to_bytes(4, "big")]
    for kind, value in tokens:
        kb = kind.encode("utf-8")
        parts.append(len(kb).to_bytes(4, "big") + kb)
        parts.append(len(value).to_bytes(4, "big") + value)
    return b"".join(parts)


def body_identity(
    *,
    level_id: str,
    level_spec_bytes: bytes,
    language_id: str,
    body_language_version_record: dict,
    payload: bytes,
) -> tuple[str, bytes]:
    level_version = hashlib.sha256(level_spec_bytes).digest()
    lang_version = hashlib.sha256(C(body_language_version_record)).digest()
    frame = body_identity_frame(
        level_id=level_id,
        level_version_raw32=level_version,
        language_id=language_id,
        language_version_raw32=lang_version,
        payload=payload,
    )
    return "sha256:" + sha256_hex(frame), frame


def suffix_variant(path: str) -> str:
    table = [
        (".d.ts", "ts-declaration"),
        (".ts", "ts"),
        (".tsx", "tsx"),
        (".mts", "mts"),
        (".cts", "cts"),
        (".js", "js"),
        (".jsx", "jsx"),
        (".mjs", "mjs"),
        (".cjs", "cjs"),
    ]
    # longest match
    table.sort(key=lambda x: len(x[0]), reverse=True)
    lower = path  # suffixes are case-sensitive as published
    for suf, var in table:
        if lower.endswith(suf):
            return var
    raise ValueError(f"unlisted suffix for {path}")
