"""Content-addressed reconstruction store: raw artifacts, C records, H frames."""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
from typing import Any

from helper.canonical import C
from helper.identity import H, DOMAIN_PREFIX, h_frame, typed_id


class Store:
    def __init__(self):
        self.blobs: dict[str, bytes] = {}  # digest -> exact bytes
        self.object_table: dict[str, dict] = {}  # typed id or digest -> meta

    def put_raw(self, data: bytes, *, label: str = "") -> str:
        d = hashlib.sha256(data).hexdigest()
        self.blobs[d] = data
        self.object_table[d] = {"kind": "raw-artifact", "label": label, "bytes": len(data)}
        return d

    def put_canonical(self, obj: Any, *, label: str = "") -> str:
        raw = C(obj)
        d = hashlib.sha256(raw).hexdigest()
        self.blobs[d] = raw
        self.object_table[d] = {"kind": "canonical-record", "label": label, "bytes": len(raw)}
        return d

    def put_h(self, domain: str, obj: Any, *, label: str = "") -> dict:
        frame = h_frame(domain, obj)
        digest = hashlib.sha256(frame).hexdigest()
        self.blobs[digest] = frame
        prefix = DOMAIN_PREFIX.get(domain)
        typed = f"{prefix}:{digest}" if prefix else None
        rec = {
            "kind": "h-identity",
            "domain": domain,
            "digest": digest,
            "typedId": typed,
            "sha256Text": f"sha256:{digest}",
            "label": label,
            "bytes": len(frame),
        }
        self.object_table[digest] = rec
        if typed:
            self.object_table[typed] = rec
        return rec

    def get(self, digest: str) -> bytes:
        if digest not in self.blobs:
            raise KeyError(f"not retained: {digest}")
        return self.blobs[digest]

    def export(self, path: Path) -> None:
        blobs_b64 = {k: base64.b64encode(v).decode("ascii") for k, v in sorted(self.blobs.items())}
        path.write_text(
            json.dumps(
                {
                    "objectTable": self.object_table,
                    "blobs": blobs_b64,
                    "blobCount": len(self.blobs),
                },
                indent=2,
            )
            + "\n"
        )

    @classmethod
    def load(cls, path: Path) -> "Store":
        doc = json.loads(path.read_text())
        s = cls()
        for k, b64 in doc["blobs"].items():
            s.blobs[k] = base64.b64decode(b64)
        s.object_table = doc["objectTable"]
        return s
