"""Load an exported store. objectTable metadata is a CLAIM; blobs are the bytes."""
from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

from canonical import AdmissionError, sha256_hex


class Store:
    def __init__(self, path: Path, claimed_run_id: str):
        self.path = path
        self.claimed_run_id = claimed_run_id
        raw = path.read_bytes()
        self.file_sha256 = sha256_hex(raw)
        self.file_bytes = len(raw)
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise AdmissionError(
                "STORE_NOT_JSON",
                "export store is not UTF-8 JSON",
                "export-manifest.json",
                {"path": str(path), "error": str(e)},
            )
        if not isinstance(data, dict):
            raise AdmissionError("STORE_SHAPE", "store root is not an object", "export-manifest.json", {})
        self.data = data
        self.object_table: dict[str, Any] = data.get("objectTable") or {}
        self.blobs_b64: dict[str, str] = data.get("blobs") or {}
        self.claimed_blob_count = data.get("blobCount")
        self.blobs: dict[str, bytes] = {}
        self.blob_rehash_errors: list[dict] = []

    def rehash_all_blobs(self) -> list[dict]:
        errors = []
        if not isinstance(self.blobs_b64, dict):
            raise AdmissionError("STORE_BLOBS_SHAPE", "blobs is not an object", "identity-and-evidence.md§3 retention", {})
        if self.claimed_blob_count is not None and self.claimed_blob_count != len(self.blobs_b64):
            errors.append(
                {
                    "code": "BLOBCOUNT_MISMATCH",
                    "citation": "export store blobCount claim",
                    "operands": {"claimed": self.claimed_blob_count, "actual": len(self.blobs_b64)},
                }
            )
        for key, b64 in self.blobs_b64.items():
            if not isinstance(b64, str):
                errors.append({"code": "BLOB_NOT_B64", "citation": "identity-and-evidence.md§3", "operands": {"key": key}})
                continue
            try:
                raw = base64.b64decode(b64, validate=True)
            except Exception as e:
                errors.append({"code": "BLOB_B64_DECODE", "citation": "identity-and-evidence.md§3", "operands": {"key": key, "error": str(e)}})
                continue
            actual = sha256_hex(raw)
            if actual != key:
                errors.append(
                    {
                        "code": "BLOB_REHASH_MISMATCH",
                        "citation": "identity-and-evidence.md§3 (raw SHA256 of exact retained bytes)",
                        "operands": {"claimedKey": key, "actualSha256": actual, "byteLength": len(raw)},
                    }
                )
                continue
            self.blobs[key] = raw
        self.blob_rehash_errors = errors
        return errors

    def get_blob(self, digest: str) -> bytes | None:
        if digest in self.blobs:
            return self.blobs[digest]
        return None

    def require_blob(self, digest: str, citation: str, field: str) -> bytes:
        raw = self.get_blob(digest)
        if raw is None:
            raise AdmissionError(
                "PREIMAGE_MISSING",
                "retention mode preimage: bytes not retained under this digest",
                citation,
                {"digest": digest, "field": field},
            )
        if sha256_hex(raw) != digest:
            raise AdmissionError(
                "PREIMAGE_REHASH",
                "retained bytes do not rehash to the digest that named them",
                citation,
                {"digest": digest, "actual": sha256_hex(raw), "field": field},
            )
        return raw

    def claimed_run_digest(self) -> str:
        rid = self.claimed_run_id
        if ":" in rid:
            prefix, hexpart = rid.split(":", 1)
            if prefix != "run3":
                raise AdmissionError(
                    "CLAIMED_RUN_PREFIX",
                    "claimed RunId is not run3",
                    "identity-schemas.v3.json#/x-opensip-evaluator-profile",
                    {"claimedRunId": rid},
                )
            return hexpart
        return rid
