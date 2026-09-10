"""FACT-IDENTITY body frame from fact-identity-policy.v2 canonicalisationSchema
plus identity-and-evidence languageVersionBinding (raw SHA-256 of C(body-language-version)).

The framed preimage is retained under its 64-hex suffix. Recipe match is not
frame retention.
"""
from __future__ import annotations

import hashlib
from typing import Any

from helper.canonical import C
from helper.errors import AdmissionError


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


def body_identity_frame(*, level_id: str, level_spec_bytes: bytes, language_id: str, language_version: bytes, payload: bytes) -> bytes:
    """Exact FACT-IDENTITY preimage retained under SHA-256(frame) hex suffix."""
    if len(language_version) != 32:
        raise AdmissionError("LANGUAGE_VERSION_WIDTH", "languageVersion must be raw 32 digest bytes")
    level_version = hashlib.sha256(level_spec_bytes).digest()
    return (
        _u8pref(DOMAIN_TAG)
        + _u8pref(level_id.encode("ascii"))
        + _u8pref(level_version)
        + _u8pref(language_id.encode("ascii"))
        + _u8pref(language_version)
        + len(payload).to_bytes(4, "big")
        + payload
    )


def body_identity(*, level_id: str, level_spec_bytes: bytes, language_id: str, language_version: bytes, payload: bytes) -> str:
    pre = body_identity_frame(
        level_id=level_id,
        level_spec_bytes=level_spec_bytes,
        language_id=language_id,
        language_version=language_version,
        payload=payload,
    )
    return "sha256:" + hashlib.sha256(pre).hexdigest()


def parse_u8pref(buf: bytes, i: int) -> tuple[bytes, int]:
    if i >= len(buf):
        raise AdmissionError("FACT_IDENTITY_FRAME", "truncated u8 length")
    n = buf[i]
    i += 1
    if i + n > len(buf):
        raise AdmissionError("FACT_IDENTITY_FRAME", "truncated u8 payload")
    return buf[i : i + n], i + n


def parse_body_identity_frame(frame: bytes) -> dict[str, Any]:
    """Parse retained FACT-IDENTITY preimage. Does not treat SHA-256 text as authority."""
    tag, i = parse_u8pref(frame, 0)
    if tag != DOMAIN_TAG:
        raise AdmissionError("FACT_IDENTITY_TAG", f"unexpected domain tag {tag!r}")
    level_id_b, i = parse_u8pref(frame, i)
    level_version, i = parse_u8pref(frame, i)
    language_id_b, i = parse_u8pref(frame, i)
    language_version, i = parse_u8pref(frame, i)
    if i + 4 > len(frame):
        raise AdmissionError("FACT_IDENTITY_FRAME", "truncated payload_len")
    payload_len = int.from_bytes(frame[i : i + 4], "big")
    i += 4
    if i + payload_len != len(frame):
        raise AdmissionError(
            "FACT_IDENTITY_FRAME",
            f"payload_len {payload_len} remainder {len(frame) - i}",
        )
    payload = frame[i:]
    rec = {
        "tag": tag.decode("ascii"),
        "levelId": level_id_b.decode("ascii"),
        "levelVersion": level_version,
        "languageId": language_id_b.decode("ascii"),
        "languageVersion": language_version,
        "payload": payload,
        "payloadLen": payload_len,
    }
    if rec["levelId"] == "L0-verbatim":
        if payload_len < 4:
            raise AdmissionError("L0_PAYLOAD", "L0 payload missing inner length")
        raw_len = int.from_bytes(payload[:4], "big")
        span = payload[4:]
        if raw_len != len(span):
            raise AdmissionError("L0_PAYLOAD", f"inner len {raw_len} span {len(span)}")
        if payload_len != raw_len + 4:
            raise AdmissionError("L0_PAYLOAD", "payload_len must equal raw_byte_len + 4")
        rec["l0Span"] = span
        rec["l0RawLen"] = raw_len
    return rec
