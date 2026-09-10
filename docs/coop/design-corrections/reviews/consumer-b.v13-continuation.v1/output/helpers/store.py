"""Retained object table + blob/frame bytes keyed by digest.

A digest declaration does not retain bytes. Every retained preimage is stored
as exact bytes (base64 JSON is sufficient for export).
"""
from __future__ import annotations

import base64
import hashlib
import json
from typing import Any

from . import canonical, h


class Store:
    def __init__(self):
        self.objects: dict[str, Any] = {}  # typed id or domain:digest -> object
        self.blobs: dict[str, bytes] = {}  # sha256 hex -> exact bytes
        self.frames: dict[str, dict] = {}  # digest -> {domain, canonicalBytes, object}
        self.meta: dict[str, Any] = {}

    def put_blob(self, data: bytes, path: str | None = None) -> str:
        digest = hashlib.sha256(data).hexdigest()
        self.blobs[digest] = data
        return digest

    def put_canonical_record(self, domain: str, obj: Any, typed: bool = True) -> str:
        cx = canonical.encode(obj)
        digest = h.h_digest(domain, obj) if domain in h.PREFIX or domain in h.NATIVE_H_DOMAINS else h.raw_sha256(cx)
        if domain in h.PREFIX:
            ident = h.h_id(domain, obj)
        elif domain in h.NATIVE_H_DOMAINS:
            ident = h.native_sha256_text(domain, obj)
        else:
            ident = digest
        self.objects[ident] = obj
        self.frames[digest] = {
            "domain": domain,
            "identity": ident,
            "canonicalBytesHex": cx.hex(),
            "canonicalSha256": h.raw_sha256(cx),
        }
        self.blobs[h.raw_sha256(cx)] = cx
        # also retain C bytes under H digest when they differ
        return ident

    def put_raw_digest_record(self, obj: Any) -> str:
        """canonical-record representation: digest is SHA-256(C(obj))."""
        cx = canonical.encode(obj)
        digest = h.raw_sha256(cx)
        self.objects[digest] = obj
        self.blobs[digest] = cx
        self.frames[digest] = {
            "domain": "canonical-record",
            "identity": digest,
            "canonicalBytesHex": cx.hex(),
            "canonicalSha256": digest,
        }
        return digest

    def require_blob(self, digest: str) -> bytes:
        if digest not in self.blobs:
            raise KeyError(f"blob {digest} not retained")
        return self.blobs[digest]

    def export(self) -> dict:
        blobs_b64 = {d: base64.b64encode(b).decode("ascii") for d, b in sorted(self.blobs.items())}
        return {
            "objectTable": self.objects,
            "blobs": blobs_b64,
            "frames": self.frames,
            "meta": self.meta,
        }

    def export_json(self) -> str:
        return json.dumps(self.export(), indent=2, sort_keys=True) + "\n"


def load_export(doc: dict) -> Store:
    s = Store()
    s.objects = dict(doc.get("objectTable") or {})
    s.frames = dict(doc.get("frames") or {})
    s.meta = dict(doc.get("meta") or {})
    for d, b64 in (doc.get("blobs") or {}).items():
        s.blobs[d] = base64.b64decode(b64)
    return s
