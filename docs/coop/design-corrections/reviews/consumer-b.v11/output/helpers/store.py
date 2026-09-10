"""Content-addressed reconstruction store: blobs keyed by SHA-256, H frames, canonical records."""
from __future__ import annotations

import base64
import json
from typing import Any

from helpers.canonical import C, H_PREFIX, H_frame, sha256_hex


class Store:
    def __init__(self) -> None:
        self.blobs: dict[str, bytes] = {}
        self.objects: dict[str, dict[str, Any]] = {}
        self.notes: list[str] = []

    def put_blob(self, data: bytes) -> str:
        d = sha256_hex(data)
        self.blobs[d] = data
        return d

    def put_canonical(self, record: Any) -> str:
        return self.put_blob(C(record))

    def put_h(self, domain: str, descriptor: Any) -> str:
        frame = H_frame(domain, descriptor)
        digest = self.put_blob(frame)
        prefix = H_PREFIX.get(domain)
        if prefix is None:
            ident = f"sha256:{digest}"
        else:
            ident = f"{prefix}:{digest}"
        self.objects[ident] = {
            "domain": domain,
            "descriptor": descriptor,
            "digest": digest,
            "id": ident,
        }
        return ident

    def put_native(self, domain: str, descriptor: Any) -> str:
        """Native H identity: sha256:<hex> of the framed preimage. Returns bare hex."""
        ident = self.put_h(domain, descriptor)
        return ident.split(":", 1)[1]

    def export(self) -> dict[str, Any]:
        blobs_b64 = {k: base64.b64encode(v).decode("ascii") for k, v in sorted(self.blobs.items())}
        return {
            "objectTable": self.objects,
            "blobs": blobs_b64,
            "blobCount": len(self.blobs),
            "objectCount": len(self.objects),
        }

    def dump(self, path) -> None:
        path.write_text(json.dumps(self.export(), indent=2) + "\n")
