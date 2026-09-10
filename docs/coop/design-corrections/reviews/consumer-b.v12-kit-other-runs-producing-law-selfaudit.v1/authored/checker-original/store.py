"""Raw store parser. Does not treat claimed proof/witness as truth."""
from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from .canonical import encode_c, lexical_scan_raw, LexicalRefusal
from .identity import parse_h_frame, sha256, PREFIX_TO_DOMAIN, TYPED_PREFIX


@dataclass
class ObjectMeta:
    key: str
    kind: str
    label: str | None
    digest: str
    declared_bytes: int | None
    domain: str | None = None
    typed_id: str | None = None


@dataclass
class Store:
    name: str
    path: str
    sha256: str
    bytes_len: int
    object_table: dict[str, dict[str, Any]]
    blobs: dict[str, bytes]
    meta: dict[str, ObjectMeta]
    raw_faults: list[dict[str, Any]] = field(default_factory=list)

    def blob(self, digest: str) -> bytes | None:
        return self.blobs.get(digest)

    def by_label(self, label: str) -> list[tuple[ObjectMeta, bytes]]:
        out = []
        for key, m in self.meta.items():
            if m.label == label:
                raw = self.blobs.get(m.digest)
                if raw is not None:
                    out.append((m, raw))
        return out

    def typed(self, prefix: str) -> list[tuple[ObjectMeta, bytes]]:
        out = []
        for key, m in self.meta.items():
            if key.startswith(prefix + ":"):
                raw = self.blobs.get(m.digest)
                if raw is not None:
                    out.append((m, raw))
        return out


def load_store(path: str, name: str, declared_sha: str, declared_bytes: int) -> Store:
    raw_file = open(path, "rb").read()
    actual_sha = hashlib.sha256(raw_file).hexdigest()
    faults: list[dict[str, Any]] = []
    if actual_sha != declared_sha:
        faults.append({"code": "EXPORT_SHA_MISMATCH", "actual": actual_sha, "declared": declared_sha})
    if len(raw_file) != declared_bytes:
        faults.append({"code": "EXPORT_BYTES_MISMATCH", "actual": len(raw_file), "declared": declared_bytes})
    data = json.loads(raw_file.decode("utf-8"))
    if set(data.keys()) != {"objectTable", "blobs", "blobCount"} and not set(["objectTable", "blobs"]).issubset(data.keys()):
        faults.append({"code": "STORE_SHAPE", "keys": list(data.keys())})
    ot = data.get("objectTable") or {}
    blobs_b64 = data.get("blobs") or {}
    blobs: dict[str, bytes] = {}
    for k, v in blobs_b64.items():
        try:
            b = base64.b64decode(v, validate=True)
        except Exception as e:
            faults.append({"code": "BLOB_B64", "digest": k, "error": str(e)})
            continue
        h = hashlib.sha256(b).hexdigest()
        if h != k:
            faults.append({"code": "BLOB_SHA", "key": k, "actual": h, "len": len(b)})
        blobs[k] = b
    if data.get("blobCount") is not None and data["blobCount"] != len(blobs):
        faults.append({"code": "BLOBCOUNT", "declared": data["blobCount"], "actual": len(blobs)})

    meta: dict[str, ObjectMeta] = {}
    for key, rec in ot.items():
        kind = rec.get("kind")
        digest = rec.get("digest")
        if not digest:
            digest = key.split(":", 1)[1] if ":" in key else key
        nbytes = rec.get("bytes")
        m = ObjectMeta(
            key=key,
            kind=kind,
            label=rec.get("label"),
            digest=digest,
            declared_bytes=nbytes,
            domain=rec.get("domain"),
            typed_id=rec.get("typedId") or (key if ":" in key else None),
        )
        meta[key] = m
        raw = blobs.get(digest)
        if raw is None:
            faults.append({"code": "OBJECT_BLOB_MISSING", "key": key, "digest": digest, "kind": kind, "label": rec.get("label")})
            continue
        if nbytes is not None and len(raw) != nbytes:
            faults.append({"code": "OBJECT_BYTES", "key": key, "declared": nbytes, "actual": len(raw)})
    return Store(
        name=name,
        path=path,
        sha256=actual_sha,
        bytes_len=len(raw_file),
        object_table=ot,
        blobs=blobs,
        meta=meta,
        raw_faults=faults,
    )


def decode_record(raw: bytes) -> dict[str, Any]:
    """Decode a retained blob as H-frame or canonical JSON record."""
    try:
        fr = parse_h_frame(raw)
        payload = fr["payload"]
        # payload must be C of a JSON value
        try:
            obj = json.loads(payload.decode("utf-8"))
        except Exception as e:
            return {"form": "h-identity", "domain": fr["domain"], "payload_bytes": payload, "json_error": str(e)}
        recomputed = encode_c(obj)
        return {
            "form": "h-identity",
            "domain": fr["domain"],
            "payload": obj,
            "payload_bytes": payload,
            "c_matches": recomputed == payload,
            "c_actual": recomputed,
        }
    except LexicalRefusal:
        pass
    try:
        obj = json.loads(raw.decode("utf-8"))
    except Exception as e:
        return {"form": "raw-artifact", "bytes": raw, "json_error": str(e)}
    recomputed = encode_c(obj)
    return {
        "form": "canonical-record-or-json",
        "payload": obj,
        "c_matches": recomputed == raw,
        "c_actual": recomputed,
        "raw": raw,
    }
