"""H identity from identity-and-evidence §3.

H(D,X) = SHA256(ASCII("opensip.product.v1") || 00 || ASCII(D) || 00 || uint64BE(length(C(X))) || C(X))
Identifier is prefix + ':' + lowercase H hex.
"""
from __future__ import annotations

import hashlib
from typing import Any

from helper.canonical import C
from helper.errors import AdmissionError

PRODUCT_PREFIX = b"opensip.product.v1"

# Domain used in H() vs public identifier prefix. From identity-and-evidence §3 table
# and identity-schemas.v3 patterns. Unchanged native/input keep major2; evaluator
# outputs use major3.
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

# Native H domains (identity-and-evidence §3): carried as sha256:<hex>, not typed prefixes.
NATIVE_DOMAINS = {
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
}


def h_preimage(domain: str, canonical_bytes: bytes) -> bytes:
    if "\x00" in domain:
        raise AdmissionError("DOMAIN_NUL", "domain must not contain NUL")
    d = domain.encode("ascii")
    return (
        PRODUCT_PREFIX
        + b"\x00"
        + d
        + b"\x00"
        + len(canonical_bytes).to_bytes(8, "big", signed=False)
        + canonical_bytes
    )


def H(domain: str, value: Any) -> str:
    """Lowercase hex of H(D,X)."""
    cx = C(value)
    pre = h_preimage(domain, cx)
    return hashlib.sha256(pre).hexdigest()


def h_frame(domain: str, value: Any) -> bytes:
    """Exact retained H preimage frame (the object stored under the digest)."""
    cx = C(value)
    return h_preimage(domain, cx)


def typed_id(domain: str, value: Any) -> str:
    prefix = DOMAIN_PREFIX.get(domain)
    if prefix is None:
        raise AdmissionError("UNKNOWN_DOMAIN", f"no typed prefix for domain {domain}")
    return f"{prefix}:{H(domain, value)}"


def sha256_text(domain: str, value: Any) -> str:
    """Native sha256:<H hex> spelling."""
    return "sha256:" + H(domain, value)


def parse_h_frame(frame: bytes, *, allowed_domains: set[str] | None = None) -> dict:
    """Admit an H frame: prefix, domain, length, remainder == C(parse)."""
    prefix = PRODUCT_PREFIX + b"\x00"
    if not frame.startswith(prefix):
        raise AdmissionError("H_FRAME_PREFIX", "frame does not begin with opensip.product.v1 NUL")
    rest = frame[len(prefix) :]
    nul = rest.find(b"\x00")
    if nul < 0:
        raise AdmissionError("H_FRAME_DOMAIN", "missing domain terminator")
    try:
        domain = rest[:nul].decode("ascii")
    except UnicodeDecodeError as e:
        raise AdmissionError("H_FRAME_DOMAIN", "domain not ASCII") from e
    if allowed_domains is not None and domain not in allowed_domains:
        raise AdmissionError("H_FRAME_DOMAIN_SET", f"domain {domain} not in allowed set")
    after = rest[nul + 1 :]
    if len(after) < 8:
        raise AdmissionError("H_FRAME_LENGTH", "missing length")
    declared = int.from_bytes(after[:8], "big", signed=False)
    payload = after[8:]
    if declared != len(payload):
        raise AdmissionError(
            "H_FRAME_LENGTH_MISMATCH",
            f"declared {declared} remaining {len(payload)}",
        )
    # remainder must be byte-identical to C of its own parse
    from helper.lexical import admit_raw
    from helper.canonical import C as Cenc

    parsed = admit_raw(payload)
    rec = Cenc(parsed)
    if rec != payload:
        raise AdmissionError("H_FRAME_NOT_CANONICAL", "remainder is not C of its parse")
    digest = hashlib.sha256(frame).hexdigest()
    return {"domain": domain, "value": parsed, "digest": digest, "canonicalBytes": payload}


def raw_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
