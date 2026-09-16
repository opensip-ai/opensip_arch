"""H identity from identity-and-evidence §3.

H(D,X) = SHA256(ASCII("opensip.product.v1") || 00 || ASCII(D) || 00 || uint64BE(length(C(X))) || C(X))
Identifier = prefix + ":" + lowercase hex of H.
"""
from __future__ import annotations

import hashlib
from typing import Any

from . import canonical

PRODUCT = b"opensip.product.v1"
CAP_DOMAIN = b"opensip.capability-manifest.v1"

# Domain D (H argument) -> public prefix. Identity-and-evidence §3 table
# plus composition §9.7 and native §11.
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

NATIVE_H_DOMAINS = {
    "native.context.typescript.v2",
    "native.context.rust.v2",
    "native.context.syntax.v2",
    "native.semantic-universe.typescript.v2",
    "native.semantic-universe.rust.v2",
    "native.semantic-universe.syntax.v2",
    "native.dependency-source-set.v1",
    "native.unified-features.rust.v1",
    "native.prepared-output-set.v3",
    "native.cargo-config-projection.v2",
    "native.dependency-file-manifest.v1",
    "native.source-unit-ownership.v1",
    "native.compilation-unit.v1",
}


def h_preimage_bytes(domain: str, descriptor: Any) -> bytes:
    """Exact H preimage frame. Identity §3: this is what an h-identity digest retains."""
    cx = canonical.encode(descriptor)
    return (
        PRODUCT
        + b"\x00"
        + domain.encode("ascii")
        + b"\x00"
        + len(cx).to_bytes(8, "big", signed=False)
        + cx
    )


def parse_h_frame(frame: bytes) -> tuple[str, bytes]:
    """Admit an h-identity retained object: prefix, domain, declared length, remainder = C(X)."""
    prefix = PRODUCT + b"\x00"
    if not frame.startswith(prefix):
        raise ValueError("H_FRAME_PREFIX")
    rest = frame[len(prefix) :]
    z = rest.find(b"\x00")
    if z < 0:
        raise ValueError("H_FRAME_DOMAIN")
    domain = rest[:z].decode("ascii")
    rest = rest[z + 1 :]
    if len(rest) < 8:
        raise ValueError("H_FRAME_LEN")
    n = int.from_bytes(rest[:8], "big", signed=False)
    cx = rest[8:]
    if len(cx) != n:
        raise ValueError(f"H_FRAME_LENGTH_MISMATCH:{n}!={len(cx)}")
    return domain, cx


def h_digest(domain: str, descriptor: Any) -> str:
    return hashlib.sha256(h_preimage_bytes(domain, descriptor)).hexdigest()


def h_id(domain: str, descriptor: Any) -> str:
    digest = h_digest(domain, descriptor)
    prefix = PREFIX.get(domain)
    if prefix is None:
        raise ValueError(f"no public prefix for domain {domain}")
    return f"{prefix}:{digest}"


def native_sha256_text(domain: str, descriptor: Any) -> str:
    if domain not in NATIVE_H_DOMAINS:
        raise ValueError(f"not a native H domain: {domain}")
    return "sha256:" + h_digest(domain, descriptor)


def native_bare_hex(domain: str, descriptor: Any) -> str:
    if domain not in NATIVE_H_DOMAINS:
        raise ValueError(f"not a native H domain: {domain}")
    return h_digest(domain, descriptor)


def capability_manifest_id(committed_bytes: bytes) -> str:
    """CAP-MANIFEST-ID-V1 over already-admitted CVE1 committed bytes."""
    pre = CAP_DOMAIN + b"\x00" + committed_bytes
    return hashlib.sha256(pre).hexdigest()


def raw_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def suffix(typed_id: str) -> str:
    if ":" in typed_id:
        return typed_id.split(":", 1)[1]
    return typed_id
