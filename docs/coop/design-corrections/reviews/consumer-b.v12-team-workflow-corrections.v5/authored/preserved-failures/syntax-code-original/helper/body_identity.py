"""FACT-IDENTITY body frame from fact-identity-policy.v2 canonicalisationSchema
plus identity-and-evidence languageVersionBinding (raw SHA-256 of C(body-language-version)).
"""
from __future__ import annotations

import hashlib
from typing import Any

from helper.canonical import C


DOMAIN_TAG = b"opensip.fact-identity.v1"


def _u8pref(b: bytes) -> bytes:
    if len(b) > 255:
        raise ValueError("component exceeds u8 length")
    return bytes([len(b)]) + b


def body_language_version(*, language_id: str, compiler_name: str, compiler_version: str, compiler_build: str, dialect: dict) -> dict:
    return {
        "schemaVersion": 1,
        "languageId": language_id,
        "compilerName": compiler_name,
        "compilerVersion": compiler_version,
        "compilerBuild": compiler_build,
        "dialect": dialect,
    }


def language_version_bytes(blv: dict) -> bytes:
    return hashlib.sha256(C(blv)).digest()  # raw 32


def l0_payload(span: bytes) -> bytes:
    return len(span).to_bytes(4, "big") + span


def framed_token_stream(tokens: list[tuple[str, bytes]]) -> bytes:
    parts = [len(tokens).to_bytes(4, "big")]
    for kind, value in tokens:
        kb = kind.encode("utf-8")
        parts.append(len(kb).to_bytes(2, "big") + kb + len(value).to_bytes(4, "big") + value)
    return b"".join(parts)


def body_identity(*, level_id: str, level_spec_bytes: bytes, language_id: str, language_version: bytes, payload: bytes) -> str:
    level_version = hashlib.sha256(level_spec_bytes).digest()
    pre = (
        _u8pref(DOMAIN_TAG)
        + _u8pref(level_id.encode("ascii"))
        + _u8pref(level_version)
        + _u8pref(language_id.encode("ascii"))
        + _u8pref(language_version)
        + len(payload).to_bytes(4, "big")
        + payload
    )
    return "sha256:" + hashlib.sha256(pre).hexdigest()
