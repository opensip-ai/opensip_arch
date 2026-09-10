"""Content-addressed store + typed object table (identity S3).

"one content-addressed store keyed by raw SHA256 retains all three of raw
artifacts, canonical records and H identities: the object retained under a
bare-hex h-identity digest is the exact H preimage frame."
"""
from __future__ import annotations

import hashlib
import json

import canon as K
import kit


class Refusal(Exception):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


class Store:
    def __init__(self):
        self.blobs: dict[str, bytes] = {}       # raw sha256 -> bytes
        self.objects: dict[str, dict] = {}      # typed id "domain2:hex" -> descriptor
        self.object_domain: dict[str, str] = {}  # typed id -> domain

    # -- raw blobs ----------------------------------------------------------
    def put_blob(self, data: bytes) -> str:
        d = hashlib.sha256(data).hexdigest()
        self.blobs[d] = data
        return d

    def get_blob(self, digest: str) -> bytes:
        if digest not in self.blobs:
            raise Refusal("EVIDENCE_UNAVAILABLE", f"blob {digest} not retained")
        return self.blobs[digest]

    def has_blob(self, digest: str) -> bool:
        return digest in self.blobs

    # -- canonical records (retention: preimage under raw SHA256 of C(rec)) --
    def put_record(self, record) -> str:
        return self.put_blob(K.C(record))

    def get_record(self, digest: str, doc_key=None, selector=None, where=""):
        raw = self.get_blob(digest)
        obj = K.admit_raw(raw)
        if K.C(obj) != raw:
            raise Refusal("RECORD_NOT_CANONICAL", f"{where} {digest}")
        if doc_key:
            kit.validate(doc_key, selector, obj, where or digest)
        return obj

    # -- H identities (retention: preimage FRAME under the bare hex) --------
    def put_identity(self, domain: str, descriptor) -> str:
        """Retain the exact H preimage frame; return the prefixed typed id."""
        blob = K.frame(domain, descriptor)
        hexd = self.put_blob(blob)
        prefix = kit.DOMAIN_PREFIX.get(domain)
        tid = f"{prefix}:{hexd}" if prefix else hexd
        self.objects[tid] = descriptor
        self.object_domain[tid] = domain
        return tid

    def put_native_identity(self, domain: str, descriptor) -> str:
        """Native H identity: retained as a frame, spelled `sha256:<hex>`."""
        blob = K.frame(domain, descriptor)
        hexd = self.put_blob(blob)
        tid = "sha256:" + hexd
        self.objects[tid] = descriptor
        self.object_domain[tid] = domain
        return tid

    def load_frame(self, hexd: str, allowed_domains, where=""):
        """Fetch, re-hash, parse and validate an H preimage frame."""
        blob = self.get_blob(hexd)
        if hashlib.sha256(blob).hexdigest() != hexd:
            raise Refusal("FRAME_DIGEST_MISMATCH", f"{where} {hexd}")
        try:
            domain, payload = K.parse_frame(blob, allowed_domains)
        except K.AdmissionError as exc:
            raise Refusal(exc.code, f"{where}: {exc.detail}") from exc
        return domain, payload

    # -- export -------------------------------------------------------------
    def export(self):
        import base64
        return {
            "blobs": {d: base64.b64encode(b).decode("ascii")
                      for d, b in sorted(self.blobs.items())},
            "objects": [
                {"id": tid, "domain": self.object_domain[tid],
                 "descriptor": self.objects[tid]}
                for tid in sorted(self.objects)],
        }


def split_id(tid: str, expect_prefix: str) -> str:
    if not tid.startswith(expect_prefix + ":"):
        raise Refusal("ID_PREFIX", f"{tid} is not {expect_prefix}:")
    return tid.split(":", 1)[1]
