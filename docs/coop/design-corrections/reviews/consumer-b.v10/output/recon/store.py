"""Content-addressed object table and blob store for reconstructed graphs."""
from __future__ import annotations

import base64
import json
from typing import Any

from .codec import encode_c, h_hex, h_id, h_preimage, sha256


class Store:
    def __init__(self):
        self.objects: dict[str, dict] = {}  # digest -> {domain, id, descriptor, preimage_b64}
        self.blobs: dict[str, str] = {}  # digest -> b64 bytes
        self.by_id: dict[str, dict] = {}

    def put_blob(self, data: bytes, *, path: str | None = None) -> dict:
        hx = sha256(data)
        self.blobs[hx] = base64.b64encode(data).decode("ascii")
        rec = {"path": path, "sha256": hx, "bytes": len(data)}
        return rec

    def put_canonical(self, domain: str, descriptor: dict, *, typed: bool = True) -> dict:
        pre = h_preimage(domain, descriptor)
        hx = sha256(pre)
        ident = h_id(domain, descriptor)
        self.blobs[hx] = base64.b64encode(pre).decode("ascii")
        row = {
            "domain": domain,
            "digest": hx,
            "id": ident,
            "descriptor": descriptor,
            "retention": "h-preimage-frame",
        }
        self.objects[hx] = row
        self.by_id[ident] = row
        return row

    def put_canonical_record(self, name: str, record: dict) -> str:
        raw = encode_c(record)
        hx = sha256(raw)
        self.blobs[hx] = base64.b64encode(raw).decode("ascii")
        self.objects[hx] = {
            "domain": name,
            "digest": hx,
            "id": hx,
            "descriptor": record,
            "retention": "canonical-record",
        }
        return hx

    def put_raw(self, name: str, data: bytes) -> str:
        hx = sha256(data)
        self.blobs[hx] = base64.b64encode(data).decode("ascii")
        self.objects[hx] = {
            "domain": name,
            "digest": hx,
            "id": hx,
            "descriptor": None,
            "retention": "raw-artifact",
            "bytes": len(data),
        }
        return hx

    def export(self) -> dict:
        table = []
        for hx, row in sorted(self.objects.items()):
            table.append(
                {
                    "digest": hx,
                    "domain": row["domain"],
                    "id": row.get("id"),
                    "retention": row["retention"],
                }
            )
        return {
            "objectTable": table,
            "blobs": self.blobs,
            "objectCount": len(self.objects),
            "blobCount": len(self.blobs),
        }
