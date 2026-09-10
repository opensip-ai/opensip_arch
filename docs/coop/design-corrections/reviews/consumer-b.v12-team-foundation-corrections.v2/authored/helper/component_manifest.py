"""Synthetic trusted observation of a component-manifest body.

identity-and-evidence §3: closure.manifestDigest is raw SHA-256 of the
admitted component-manifest body bytes encoded with the security metadata
profile, excluding the signature envelope. Real crypto/OS/signature
enforcement is not demanded. component-manifest-schemas.v11 is
DESIGN-CONTRACT-CANDIDATE / CANDIDATE-NOT-APPLIED / binds NOTHING — this
module does not claim stock inhabitance of that candidate.

DetectorManifestV1 ({schemaFamily, schemaMajor, compatibleClosures}) must
not occupy closure.manifestDigest.
"""
from __future__ import annotations

import hashlib
from typing import Any

from helper.canonical import C
from helper.errors import AdmissionError

MANIFEST_DOMAIN = "opensip.metadata.manifest.1"
V11_STANDING = {
    "documentClass": "DESIGN-CONTRACT-CANDIDATE",
    "status": "CANDIDATE-NOT-APPLIED",
    "binds": "NOTHING",
    "authorityClaim": "NONE",
    "stockInhabitanceClaimed": False,
}

# D-002 four platforms; identity closure.platform spelling → (os, arch).
PLATFORM_SPLIT = {
    "macos-aarch64": ("macos", "arm64"),
    "macos-x86_64": ("macos", "x86_64"),
    "linux-aarch64-gnu": ("linux", "arm64"),
    "linux-x86_64-gnu": ("linux", "x86_64"),
}


def metadata_preimage_sha256(canonical_bytes: bytes, *, domain: str = MANIFEST_DOMAIN) -> str:
    """SHA-256(UTF-8(domainTag) || 0x00 || canonicalBytes). Not the admission digest."""
    return hashlib.sha256(domain.encode("utf-8") + b"\x00" + canonical_bytes).hexdigest()


def component_manifest_body(
    *,
    closure_kind: str,
    semantic_version: str,
    platform: str,
    tree: list[dict],
    entrypoint: str | None = None,
) -> dict[str, Any]:
    """Joinable synthetic body. Not DetectorManifestV1. Not a sealed v11 instance."""
    if platform not in PLATFORM_SPLIT:
        raise AdmissionError("COMPONENT_MANIFEST_PLATFORM", platform)
    os_name, arch = PLATFORM_SPLIT[platform]
    ep = entrypoint or f"bin/{closure_kind}"
    entries = []
    for row in tree:
        entries.append(
            {
                "path": row["path"],
                "type": "file",
                "mode": "0755",
                "length": row["bytes"],
                "sha256": row["sha256"],
            }
        )
    entries = sorted(entries, key=lambda e: e["path"].encode("utf-8"))
    return {
        "kind": "component",
        "manifestSchemaVersion": 1,
        "name": f"opensip-{closure_kind}",
        "version": semantic_version,
        "role": "analyzer",
        "selectedClosureKind": closure_kind,
        "platforms": [
            {
                "os": os_name,
                "arch": arch,
                "entrypoint": ep,
                "tree": {"entries": entries},
            }
        ],
    }


def encode_manifest_body(body: dict) -> bytes:
    """Exact stored bytes. C is compatible with opensip-metadata-canonical.1 for
    ASCII NFC strings and i64-range integers used here. Admission identity is
    SHA-256 of these stored bytes (v11 encodingRule: no extra canonicalization
    of the admission digest). Signing preimage is domain-separated and is not
    closure.manifestDigest."""
    return C(body)


def stored_sha256(body_bytes: bytes) -> str:
    return hashlib.sha256(body_bytes).hexdigest()


def project_tree_from_manifest(body: dict, *, platform: str) -> list[dict]:
    os_name, arch = PLATFORM_SPLIT[platform]
    chosen = None
    for p in body.get("platforms") or []:
        if p.get("os") == os_name and p.get("arch") == arch:
            chosen = p
            break
    if chosen is None:
        raise AdmissionError("COMPONENT_MANIFEST_PLATFORM_ROW", platform)
    out = []
    for e in (chosen.get("tree") or {}).get("entries") or []:
        if e.get("type") != "file":
            continue
        out.append({"path": e["path"], "sha256": e["sha256"], "bytes": e["length"]})
    return sorted(out, key=lambda r: r["path"].encode("utf-8"))


def admit_component_manifest(store, closure: dict) -> dict:
    """Join retained body bytes to closure.manifestDigest / tree / platform / version.

    Does not claim v11 stock inhabitance. Does not verify signatures.
    """
    digest = closure["manifestDigest"]
    raw = store.get(digest)
    got = hashlib.sha256(raw).hexdigest()
    if got != digest:
        raise AdmissionError("COMPONENT_MANIFEST_REHASH", f"{digest} rehashes to {got}")
    from helper.lexical import admit_raw

    body = admit_raw(raw)
    if C(body) != raw:
        raise AdmissionError("COMPONENT_MANIFEST_NOT_C", digest)
    # DetectorManifestV1 is only {schemaFamily, schemaMajor, compatibleClosures}.
    if set(body.keys()) <= {"schemaFamily", "schemaMajor", "compatibleClosures"}:
        raise AdmissionError("COMPONENT_MANIFEST_IS_DETECTOR_LISTING", digest)
    if body.get("kind") != "component":
        raise AdmissionError("COMPONENT_MANIFEST_KIND", str(body.get("kind")))
    if body.get("version") != closure["semanticVersion"]:
        raise AdmissionError(
            "COMPONENT_MANIFEST_VERSION",
            f"{body.get('version')} != {closure['semanticVersion']}",
        )
    projected = project_tree_from_manifest(body, platform=closure["platform"])
    closure_tree = sorted(list(closure["tree"]), key=lambda r: r["path"].encode("utf-8"))
    if projected != closure_tree:
        raise AdmissionError("COMPONENT_MANIFEST_TREE", "projected file rows != closure.tree")
    expected_name = f"opensip-{closure['kind']}"
    if body.get("name") != expected_name:
        raise AdmissionError("COMPONENT_MANIFEST_NAME", f"{body.get('name')} != {expected_name}")
    if body.get("selectedClosureKind") != closure["kind"]:
        raise AdmissionError("COMPONENT_MANIFEST_SELECTED_KIND", str(body.get("selectedClosureKind")))
    return {
        "digest": digest,
        "bytes": len(raw),
        "body": body,
        "storedSha256": digest,
        "preimageSha256": metadata_preimage_sha256(raw),
        "v11Standing": V11_STANDING,
        "signatureEnvelopeVerified": False,
        "stockInhabitanceClaimed": False,
    }
