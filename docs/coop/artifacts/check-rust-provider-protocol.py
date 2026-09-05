#!/usr/bin/env python3
"""Retained checker for the Rust semantic-provider protocol candidate.

Run only as:
  python3 -I -B docs/coop/artifacts/check-rust-provider-protocol.py
  python3 -I -B docs/coop/artifacts/check-rust-provider-protocol.py --selftest

The checker imports no producer checker. It hashes every dependency before use,
strictly rejects duplicate/nonfinite JSON, rejects floats in every protocol
value, validates exact cross-surface joins, supplies an independent
deterministic-CBOR/frame oracle, exercises the protocol state/fate model, and
refuses mutation testing on a dirty base.
"""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import sys
import unicodedata
from typing import Any, Callable


HERE = pathlib.Path(__file__).resolve().parent
PROTOCOL = "rust-provider-protocol.v1.json"
DELIVERY_JOIN = "delivery-rust-provider-join.v1.json"
RI_JOIN = "resolved-inputs-rust-provider-join.v1.json"
GAP_RESPONSE = "rust-provider-protocol.v1.adjudication-gap-response.json"

DEPENDENCY_HASHES = {
    "delivery.v2.json": "47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3",
    "resolved-inputs.v2.json": "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    "c2-plan-stage-schema.v3.json": "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285",
    "fact-plane.v1.json": "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
    "d9-exit-contract.v1.13.json": "fc2c546a4cdbe2038f3a5db333ab9903d21ae9d6223777b139b58551fb2f2fae",
    "d9-exit-contract.v1.13.review-independent-prefreeze.json":
        "88ab60efb21f603213ebff722f62f310b422f03981895e3f6779f2febe734c5b",
}

# Patched only after all three candidate JSON files reach final exact bytes.
LOCAL_RAW_HASHES = {
    PROTOCOL: "8c749eb7942a80cee3da2e304328addce4dac42e20a084b4ce26bcf31da51796",
    DELIVERY_JOIN: "42eb9788132aee6d436123881bbd2e82db0da4f223bd13de16c26410fb3e5558",
    RI_JOIN: "b85017567f2f31589b17d9cd130aeb55b58700844f431cb7baa650a4f255d707",
}
LOCAL_SEMANTIC_HASHES = {
    PROTOCOL: "dedd2cabe41df14da6719f7704798741e4d54092fb4cd0c5ec55338d4c8d2d7c",
    DELIVERY_JOIN: "5a2a427af272fe766470256df50bc32d926af5fff33ccf3fad6ee9d324840854",
    RI_JOIN: "a81856854e836b6b3c192897cb8fdf4b40fec9385dd627f36404b1e86c5b441b",
}

EXPECTED_FRAMES = {
    "Hello": ("host-to-worker", "HelloV1", False),
    "HelloAck": ("worker-to-host", "HelloAckV1", False),
    "OpenUniverse": ("host-to-worker", "OpenUniverseV1", False),
    "UniverseAccepted": ("worker-to-host", "UniverseAcceptedV1", False),
    "SnapshotManifest": ("host-to-worker", "SnapshotManifestV1", False),
    "SnapshotFileChunk": ("host-to-worker", "SnapshotFileChunkV1", False),
    "SnapshotSeal": ("host-to-worker", "SnapshotSealV1", False),
    "SnapshotAccepted": ("worker-to-host", "SnapshotAcceptedV1", False),
    "Analyze": ("host-to-worker", "AnalyzeV1", False),
    "FactBatch": ("worker-to-host", "FactBatchV1", False),
    "Coverage": ("worker-to-host", "CoverageV1", False),
    "Unavailable": ("worker-to-host", "UnavailableV1", True),
    "BudgetExhausted": ("worker-to-host", "BudgetExhaustedV1", True),
    "Complete": ("worker-to-host", "CompleteV1", True),
    "ProviderFault": ("worker-to-host", "ProviderFaultV1", True),
    "Cancel": ("host-to-worker", "CancelV1", True),
    "Cancelled": ("worker-to-host", "CancelledV1", True),
}

EXPECTED_LIMITS = {
    "maxFramePayloadBytes": 67108864,
    "maxSnapshotChunkBytes": 1048576,
    "maxSnapshotEntries": 200000,
    "maxSnapshotTotalFileBytes": 8589934592,
    "maxAnalyzeStages": 1024,
    "maxRelationsPerStage": 64,
    "maxSubjectsPerStage": 1000000,
    "maxRequestedCoverageKeysPerStage": 128,
    "maxFactBatchCandidates": 4096,
    "maxFactCandidatesTotal": 1000000,
    "maxCanonicalRelationPayloadBytes": 1048576,
    "maxCoverageEntriesPerFrame": 4096,
    "maxCandidateSpoolBytes": 1073741824,
    "maxRequestPayloadBytesTotal": 9663676416,
    "maxResponsePayloadBytesTotal": 1073741824,
    "maxRequestFrames": 1000000,
    "maxResponseFrames": 1000000,
    "maxStderrBytes": 262144,
    "maxScratchBytes": 2147483648,
    "cancellationGraceMilliseconds": 5000,
    "normalExitGraceMilliseconds": 5000,
}

SUPERVISOR_EVENT_SEMANTIC_HASH = "f80ed3f4214d3c2221a74fd7bf2e3d5ea9722964db764ac0b5e40d2f6b506c5d"

RUST_UNIVERSE_FIELDS = {
    "schemaVersion", "manifestId", "capabilityManifestId",
    "providerArtifactId", "providerArtifactSha256", "toolchainArtifactId",
    "toolchainArtifactSha256", "protocolMajor", "providerBuildId",
    "rustCommitHash", "rustcVersion", "cargoVersion", "hostTriple",
    "targetTriple", "sysrootDigest", "rustcDevLlvmDigest",
    "standardLibraryComponentDigests", "providerBinarySha256",
    "licenseNoticeBundleSha256", "platformId", "resolvedInputs",
}
RUST_RESOLVED_FIELDS = {
    "edition", "cfg", "packageLockIdentity", "resolvedPackages", "rustflags",
    "crateRootPaths", "executionCapableResolution", "buildScriptOutputs",
    "procMacroOutputs",
}
COVERAGE_KEY_FIELDS = {
    "relation", "resolution", "sourceUniverseId", "targetUniverseId",
    "subjectScopeCommitment", "producer", "producerVersion", "schemaVersion",
}
FACT_CANDIDATE_FIELDS = {
    "candidateOrdinal", "relation", "resolution", "layer", "producer",
    "producerVersion", "schemaVersion", "language", "sourceUniverseId",
    "targetUniverseId", "confidenceMillionths", "relationSchemaId",
    "canonicalRelationPayload", "anchors",
}
ANCHOR_FIELDS = {
    "kind", "snapshotId", "path", "contentSha256", "startByte", "endByte",
    "factId",
}
CAPABILITY_FIELDS = {
    "providerId", "language", "providerVersionSource",
    "toolchainIdentitySource", "relations", "platformIds",
}
REPOSITORY_RESOLUTION_FIELDS = {
    "mode", "grantId", "projectId", "network", "buildScriptOutputs",
    "procMacroOutputs", "toolPaths",
}
TOOL_PATH_FIELDS = {"artifactId", "bundleRelativePath", "fileSha256", "role"}

DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SNAP_RE = re.compile(r"^snap1:sha256:[0-9a-f]{64}$")
PLAN_RE = re.compile(r"^plan1:sha256:[0-9a-f]{64}$")
FACT_ID_RE = re.compile(r"^fact:sha256:[0-9a-f]{64}$")
IDENT_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$")


class StrictJsonError(ValueError):
    pass


def _reject_constant(value: str) -> None:
    raise StrictJsonError(f"forbidden JSON constant {value}")


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise StrictJsonError("duplicate JSON object key")
        out[key] = value
    return out


def strict_json_loads(data: str) -> Any:
    return json.loads(
        data,
        object_pairs_hook=_pairs,
        parse_constant=_reject_constant,
    )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def semantic_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def semantic_hash(value: Any) -> str:
    return sha256_bytes(semantic_bytes(value))


def _read_hashed(path: pathlib.Path, expected: str) -> tuple[Any | None, str | None]:
    try:
        raw = path.read_bytes()
    except OSError:
        return None, f"RPP-IO: cannot read required {path.name}"
    actual = sha256_bytes(raw)
    if actual != expected:
        return None, f"RPP-HASH: {path.name} expected {expected}, observed {actual}"
    try:
        text = raw.decode("utf-8")
        return strict_json_loads(text), None
    except (UnicodeError, ValueError, json.JSONDecodeError):
        return None, f"RPP-JSON: {path.name} is not strict duplicate-free finite JSON"


def _read_candidate(path: pathlib.Path) -> tuple[Any | None, str | None, str | None]:
    try:
        raw = path.read_bytes()
    except OSError:
        return None, None, f"RPP-IO: cannot read candidate {path.name}"
    actual = sha256_bytes(raw)
    try:
        value = strict_json_loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError, json.JSONDecodeError):
        return None, actual, f"RPP-JSON: {path.name} is not strict duplicate-free finite JSON"
    return value, actual, None


def _u64(value: Any) -> bool:
    return type(value) is int and 0 <= value <= 0xFFFFFFFFFFFFFFFF


def _nfc(value: Any, *, nonempty: bool = True, max_bytes: int = 4096) -> bool:
    return (
        type(value) is str
        and (bool(value) or not nonempty)
        and unicodedata.normalize("NFC", value) == value
        and len(value.encode("utf-8")) <= max_bytes
    )


def _identity(value: Any) -> bool:
    return _nfc(value) and not any(ord(ch) < 0x20 or 0x7F <= ord(ch) <= 0x9F for ch in value)


def _digest(value: Any) -> bool:
    return type(value) is str and DIGEST_RE.fullmatch(value) is not None


def _sha(value: Any) -> bool:
    return type(value) is str and SHA_RE.fullmatch(value) is not None


def _canonical_path(value: Any) -> bool:
    if not _nfc(value) or value.startswith("/") or "\\" in value or "\x00" in value:
        return False
    if re.match(r"^[A-Za-z]:", value):
        return False
    parts = value.split("/")
    return all(part not in {"", ".", ".."} for part in parts)


def _closed(value: Any, fields: set[str]) -> bool:
    return type(value) is dict and set(value) == fields


def _sorted_unique_text(values: Any, *, path: bool = False, allow_empty: bool = True) -> bool:
    if type(values) is not list or (not allow_empty and not values):
        return False
    validator = _canonical_path if path else _nfc
    if not all(validator(v) for v in values):
        return False
    return values == sorted(values, key=lambda s: s.encode("utf-8")) and len(values) == len(set(values))


# Independent RFC 8949 deterministic-CBOR restricted-profile oracle.
def _cbor_head(major: int, value: int) -> bytes:
    if not _u64(value):
        raise ValueError("CBOR argument outside uint64")
    if value < 24:
        return bytes([(major << 5) | value])
    if value <= 0xFF:
        return bytes([(major << 5) | 24, value])
    if value <= 0xFFFF:
        return bytes([(major << 5) | 25]) + value.to_bytes(2, "big")
    if value <= 0xFFFFFFFF:
        return bytes([(major << 5) | 26]) + value.to_bytes(4, "big")
    return bytes([(major << 5) | 27]) + value.to_bytes(8, "big")


def cbor_encode(value: Any, *, depth: int = 0) -> bytes:
    if depth > 64:
        raise ValueError("CBOR nesting too deep")
    if value is None:
        return b"\xf6"
    if type(value) is bool:
        return b"\xf5" if value else b"\xf4"
    if type(value) is int:
        if not _u64(value):
            raise ValueError("only uint64 is admitted")
        return _cbor_head(0, value)
    if type(value) is bytes:
        return _cbor_head(2, len(value)) + value
    if type(value) is str:
        if unicodedata.normalize("NFC", value) != value:
            raise ValueError("non-NFC text")
        raw = value.encode("utf-8")
        return _cbor_head(3, len(raw)) + raw
    if type(value) is list:
        return _cbor_head(4, len(value)) + b"".join(
            cbor_encode(item, depth=depth + 1) for item in value
        )
    if type(value) is dict:
        encoded: list[tuple[bytes, bytes]] = []
        for key, item in value.items():
            if type(key) is not str:
                raise ValueError("map key is not text")
            key_bytes = cbor_encode(key, depth=depth + 1)
            encoded.append((key_bytes, cbor_encode(item, depth=depth + 1)))
        encoded.sort(key=lambda pair: (len(pair[0]), pair[0]))
        return _cbor_head(5, len(encoded)) + b"".join(k + v for k, v in encoded)
    raise ValueError("value outside closed CBOR data model")


class _CborReader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def take(self, count: int) -> bytes:
        if count < 0 or self.pos + count > len(self.data):
            raise ValueError("truncated CBOR")
        out = self.data[self.pos:self.pos + count]
        self.pos += count
        return out

    def arg(self, additional: int) -> int:
        if additional < 24:
            return additional
        widths = {24: 1, 25: 2, 26: 4, 27: 8}
        if additional not in widths:
            raise ValueError("indefinite or reserved CBOR argument")
        width = widths[additional]
        value = int.from_bytes(self.take(width), "big")
        lower = {1: 24, 2: 256, 4: 65536, 8: 4294967296}[width]
        if value < lower:
            raise ValueError("non-shortest CBOR argument")
        return value

    def item(self, depth: int = 0) -> Any:
        if depth > 64:
            raise ValueError("CBOR nesting too deep")
        initial = self.take(1)[0]
        major, additional = initial >> 5, initial & 31
        if major == 0:
            return self.arg(additional)
        if major == 1:
            raise ValueError("negative integer forbidden")
        if major == 2:
            return self.take(self.arg(additional))
        if major == 3:
            try:
                value = self.take(self.arg(additional)).decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError("invalid UTF-8") from exc
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError("non-NFC text")
            return value
        if major == 4:
            return [self.item(depth + 1) for _ in range(self.arg(additional))]
        if major == 5:
            count = self.arg(additional)
            out: dict[str, Any] = {}
            previous: tuple[int, bytes] | None = None
            for _ in range(count):
                key_start = self.pos
                key = self.item(depth + 1)
                key_bytes = self.data[key_start:self.pos]
                if type(key) is not str:
                    raise ValueError("non-text map key")
                order_key = (len(key_bytes), key_bytes)
                if previous is not None and order_key <= previous:
                    raise ValueError("duplicate or noncanonical map-key order")
                if key in out:
                    raise ValueError("duplicate map key")
                previous = order_key
                out[key] = self.item(depth + 1)
            return out
        if major == 6:
            raise ValueError("tag forbidden")
        if major == 7 and additional in {20, 21, 22}:
            return {20: False, 21: True, 22: None}[additional]
        raise ValueError("float/simple value forbidden")


def cbor_decode_canonical(data: bytes) -> Any:
    reader = _CborReader(data)
    value = reader.item()
    if reader.pos != len(data):
        raise ValueError("trailing CBOR bytes")
    if cbor_encode(value) != data:
        raise ValueError("CBOR does not round-trip canonically")
    return value


def frame_encode(envelope: dict[str, Any]) -> bytes:
    payload = cbor_encode(envelope)
    if len(payload) > EXPECTED_LIMITS["maxFramePayloadBytes"]:
        raise ValueError("frame payload exceeds bound")
    return len(payload).to_bytes(8, "big") + hashlib.sha256(payload).digest() + payload


def frame_decode(frame: bytes) -> dict[str, Any]:
    if len(frame) < 40:
        raise ValueError("truncated frame prefix")
    length = int.from_bytes(frame[:8], "big")
    if length > EXPECTED_LIMITS["maxFramePayloadBytes"]:
        raise ValueError("declared frame payload exceeds bound")
    if len(frame) != 40 + length:
        raise ValueError("frame length mismatch or extra bytes")
    payload = frame[40:]
    if hashlib.sha256(payload).digest() != frame[8:40]:
        raise ValueError("frame digest mismatch")
    value = cbor_decode_canonical(payload)
    if type(value) is not dict:
        raise ValueError("envelope is not a map")
    return value


def _rust_universe_errors(value: Any) -> list[str]:
    errors: list[str] = []
    if not _closed(value, RUST_UNIVERSE_FIELDS):
        return ["RustUniverseV1 is not the exact closed rust-v1 record"]
    constants = {
        "schemaVersion": 1,
        "providerArtifactId": "rust-provider",
        "toolchainArtifactId": "rust-toolchain-bundle",
    }
    if any(value.get(k) != v for k, v in constants.items()):
        errors.append("RustUniverseV1 constants drifted")
    for key in {
        "manifestId", "capabilityManifestId", "providerArtifactSha256",
        "toolchainArtifactSha256", "rustCommitHash", "sysrootDigest",
        "rustcDevLlvmDigest", "providerBinarySha256", "licenseNoticeBundleSha256",
    }:
        if not _digest(value.get(key)):
            errors.append(f"RustUniverseV1 {key} is not DigestHex")
    if value.get("protocolMajor") != 1:
        errors.append("RustUniverseV1 protocolMajor is not 1")
    for key in {
        "providerBuildId", "rustcVersion", "cargoVersion", "hostTriple",
        "targetTriple", "platformId",
    }:
        if not _identity(value.get(key)):
            errors.append(f"RustUniverseV1 {key} is not canonical text")
    stdlib = value.get("standardLibraryComponentDigests")
    if type(stdlib) is not dict or not stdlib or any(
        not _identity(k) or not _digest(v) for k, v in stdlib.items()
    ):
        errors.append("RustUniverseV1 stdlib digest map is invalid")
    resolved = value.get("resolvedInputs")
    if not _closed(resolved, RUST_RESOLVED_FIELDS):
        return errors + ["RustUniverseV1 resolvedInputs is not closed"]
    if resolved.get("edition") not in {"2015", "2018", "2021", "2024"}:
        errors.append("Rust resolved edition is invalid")
    if not _sorted_unique_text(resolved.get("cfg")):
        errors.append("Rust cfg is not sorted unique text")
    if not _digest(resolved.get("packageLockIdentity")):
        errors.append("Rust package lock identity is invalid")
    packages = resolved.get("resolvedPackages")
    if type(packages) is not list:
        errors.append("Rust packages is not an array")
    else:
        ids: list[str] = []
        for package in packages:
            if not _closed(package, {"packageId", "version", "sourceDigest", "features"}):
                errors.append("Rust resolved package is not closed")
                continue
            if not _identity(package.get("packageId")) or not _identity(package.get("version")):
                errors.append("Rust resolved package identity/version invalid")
            else:
                ids.append(package["packageId"])
            if not _digest(package.get("sourceDigest")) or not _sorted_unique_text(package.get("features")):
                errors.append("Rust resolved package digest/features invalid")
        if ids != sorted(ids, key=lambda s: s.encode("utf-8")) or len(ids) != len(set(ids)):
            errors.append("Rust resolved packages are not sorted unique")
    if type(resolved.get("rustflags")) is not list or not all(
        _nfc(item, nonempty=False) for item in resolved.get("rustflags", [])
    ):
        errors.append("Rust rustflags is not an ordered text array")
    if not _sorted_unique_text(resolved.get("crateRootPaths"), path=True, allow_empty=False):
        errors.append("Rust crate roots invalid")
    if type(resolved.get("executionCapableResolution")) is not bool:
        errors.append("Rust executionCapableResolution is not boolean")
    build = resolved.get("buildScriptOutputs")
    if type(build) is not list:
        errors.append("buildScriptOutputs is not an array")
    else:
        keys: list[tuple[str, str]] = []
        for row in build:
            if not _closed(row, {"packageId", "cfg", "outputDigest"}):
                errors.append("buildScriptOutput is not closed")
                continue
            if not _identity(row.get("packageId")) or not _nfc(row.get("cfg")) or not _digest(row.get("outputDigest")):
                errors.append("buildScriptOutput values invalid")
            else:
                keys.append((row["packageId"], row["cfg"]))
        if keys != sorted(keys) or len(keys) != len(set(keys)):
            errors.append("buildScriptOutputs not sorted unique")
    proc = resolved.get("procMacroOutputs")
    if type(proc) is not list:
        errors.append("procMacroOutputs is not an array")
    else:
        ids = []
        for row in proc:
            if not _closed(row, {"crateId", "outputDigest"}) or not _identity(row.get("crateId")) or not _digest(row.get("outputDigest")):
                errors.append("procMacroOutput invalid")
                continue
            ids.append(row["crateId"])
        if ids != sorted(ids) or len(ids) != len(set(ids)):
            errors.append("procMacroOutputs not sorted unique")
    if resolved.get("executionCapableResolution") is False and (build or proc):
        errors.append("execution-disabled universe has repository outputs")
    return errors


def _selected_rust_capability(delivery: dict[str, Any]) -> dict[str, Any] | None:
    try:
        profiles = delivery["installProfiles"]["profiles"]
        full = next(row for row in profiles if row.get("profile") == "full")
        providers = full["capabilityManifest"]["providers"]
        return copy.deepcopy(next(row for row in providers if row.get("providerId") == "rust-semantic"))
    except (KeyError, TypeError, StopIteration):
        return None


def _capability_errors(value: Any, expected: Any) -> list[str]:
    if not _closed(value, CAPABILITY_FIELDS):
        return ["RustProviderCapabilityV1 is not closed"]
    if type(expected) is not dict or value != expected:
        return ["RustProviderCapabilityV1 is not exact signed capability row"]
    if value.get("providerId") != "rust-semantic" or value.get("language") != "rust":
        return ["RustProviderCapabilityV1 canonical identity drifted"]
    if type(value.get("relations")) is not dict or not value["relations"]:
        return ["RustProviderCapabilityV1 relations invalid"]
    if value.get("platformIds") != ["all-supported"]:
        return ["RustProviderCapabilityV1 platformIds drifted"]
    return []


def _tool_path_errors(value: Any) -> list[str]:
    if not _closed(value, TOOL_PATH_FIELDS):
        return ["ToolPathV1 is not closed"]
    if value.get("artifactId") != "rust-toolchain-bundle":
        return ["ToolPathV1 artifactId drifted"]
    if not _canonical_path(value.get("bundleRelativePath")) or not _digest(value.get("fileSha256")):
        return ["ToolPathV1 path/digest invalid"]
    if value.get("role") not in {"cargo", "rustc", "linker", "proc-macro-host", "dynamic-loader"}:
        return ["ToolPathV1 role invalid"]
    return []


def _repository_errors(value: Any, universe: Any) -> list[str]:
    if not _closed(value, REPOSITORY_RESOLUTION_FIELDS):
        return ["RepositoryResolutionV1 is not closed"]
    errors: list[str] = []
    if value.get("mode") not in {"disabled", "prepared"} or type(value.get("network")) is not bool or value.get("network") is not False:
        errors.append("RepositoryResolutionV1 mode/network invalid")
    if not _identity(value.get("projectId")):
        errors.append("RepositoryResolutionV1 projectId invalid")
    tool_paths = value.get("toolPaths")
    if type(tool_paths) is not list:
        errors.append("RepositoryResolutionV1 toolPaths not array")
        tool_paths = []
    else:
        for row in tool_paths:
            errors.extend(_tool_path_errors(row))
        keys = [
            (row.get("role"), row.get("bundleRelativePath"))
            for row in tool_paths if type(row) is dict
        ]
        if keys != sorted(keys) or len(keys) != len(set(keys)):
            errors.append("RepositoryResolutionV1 toolPaths not sorted unique")
    resolved = universe.get("resolvedInputs", {}) if type(universe) is dict else {}
    if value.get("buildScriptOutputs") != resolved.get("buildScriptOutputs") or value.get("procMacroOutputs") != resolved.get("procMacroOutputs"):
        errors.append("RepositoryResolutionV1 outputs differ from rust-v1")
    execution = resolved.get("executionCapableResolution")
    if value.get("mode") == "disabled":
        if value.get("grantId") is not None or tool_paths or value.get("buildScriptOutputs") != [] or value.get("procMacroOutputs") != [] or execution is not False:
            errors.append("disabled RepositoryResolutionV1 contradicts rust-v1")
    else:
        if not _identity(value.get("grantId")) or not tool_paths or execution is not True:
            errors.append("prepared RepositoryResolutionV1 lacks grant/tool paths/execution-capable rust-v1")
    return errors


def _coverage_key_errors(value: Any, relations: dict[str, Any]) -> list[str]:
    if not _closed(value, COVERAGE_KEY_FIELDS):
        return ["CoverageKeyV1 is not closed"]
    errors: list[str] = []
    relation = value.get("relation")
    entry = relations.get(relation) if type(relations) is dict and type(relation) is str else None
    if type(entry) is not dict or value.get("resolution") not in entry.get("ladder", []):
        errors.append("CoverageKeyV1 relation/resolution invalid")
    for key in ("sourceUniverseId", "subjectScopeCommitment"):
        if not _sha(value.get(key)):
            errors.append(f"CoverageKeyV1 {key} invalid")
    if not _identity(value.get("targetUniverseId")):
        errors.append("CoverageKeyV1 targetUniverseId invalid")
    if value.get("producer") != "rust-semantic" or not _identity(value.get("producerVersion")) or value.get("schemaVersion") != 1:
        errors.append("CoverageKeyV1 provider/version/schema invalid")
    return errors


def _anchor_errors(value: Any, snapshot_id: str) -> list[str]:
    if not _closed(value, ANCHOR_FIELDS):
        return ["AnchorRefV1 is not closed"]
    if value.get("kind") == "source-span":
        if value.get("snapshotId") != snapshot_id or not _canonical_path(value.get("path")) or not _digest(value.get("contentSha256")):
            return ["source-span anchor identity invalid"]
        if not _u64(value.get("startByte")) or not _u64(value.get("endByte")) or value["endByte"] <= value["startByte"] or value.get("factId") is not None:
            return ["source-span anchor range/null fields invalid"]
        return []
    if value.get("kind") == "fact-ref":
        if type(value.get("factId")) is not str or FACT_ID_RE.fullmatch(value["factId"]) is None:
            return ["fact-ref anchor FactId invalid"]
        if any(value.get(k) is not None for k in ("snapshotId", "path", "contentSha256", "startByte", "endByte")):
            return ["fact-ref anchor non-FactId fields are not null"]
        return []
    return ["AnchorRefV1 kind invalid"]


def _subject_id(value: Any) -> bool:
    return (
        _identity(value)
        and type(value) is str
        and re.fullmatch(r"[a-z][a-z0-9._-]*:.+", value) is not None
    )


def _relation_payload_errors(value: Any, schema: Any, resolution: Any) -> list[str]:
    """Validate a decoded relation payload against the pinned host registry."""
    if type(schema) is not dict or schema.get("closed") is not True:
        return ["relation payload host schema missing/open"]
    required = schema.get("required")
    optional = schema.get("optional")
    fields = schema.get("fields")
    if type(required) is not list or type(optional) is not list or type(fields) is not dict:
        return ["relation payload host schema malformed"]
    required_set = set(required)
    optional_set = set(optional)
    if len(required_set) != len(required) or len(optional_set) != len(optional) or required_set & optional_set or set(fields) != required_set | optional_set:
        return ["relation payload host schema field declaration malformed"]
    if type(value) is not dict or not required_set <= set(value) or not set(value) <= required_set | optional_set:
        return ["relation payload does not satisfy exact closed field set"]

    errors: list[str] = []
    rules = schema.get("resolutionRules", {})
    if type(rules) is not dict:
        errors.append("relation payload resolution rule table malformed")
    elif rules:
        rule = rules.get(resolution)
        if type(rule) is not dict or set(rule) != {"required", "forbidden"} or type(rule.get("required")) is not list or type(rule.get("forbidden")) is not list:
            errors.append("relation payload resolution has no exact host rule")
        else:
            if not set(rule["required"]) <= set(value) or set(rule["forbidden"]) & set(value):
                errors.append("relation payload violates resolution field rule")
    if schema.get("schemaId") == "opensip.relation.vcs-change.v1":
        renamed = value.get("changeKind") == "renamed"
        if ("previousPath" in value) != renamed:
            errors.append("vcs-change previousPath union invalid")

    enums = schema.get("enums", {})
    if type(enums) is not dict:
        errors.append("relation payload enum table malformed")
        enums = {}
    validators: dict[str, Callable[[Any], bool]] = {
        "CanonicalPath": _canonical_path,
        "CanonicalText": _identity,
        "SubjectIdV1": _subject_id,
        "DigestHex": _digest,
        "Sha256Text": _sha,
        "UInt64": _u64,
    }
    for name, value_type in fields.items():
        if name not in value:
            continue
        validator = validators.get(value_type)
        if validator is not None:
            if not validator(value[name]):
                errors.append(f"relation payload field {name} has invalid {value_type}")
        elif value_type in enums:
            if type(enums[value_type]) is not list or value[name] not in enums[value_type]:
                errors.append(f"relation payload field {name} has invalid {value_type}")
        else:
            errors.append(f"relation payload field {name} has unknown host type {value_type}")
    return errors


def _candidate_errors(value: Any, *, stage: dict[str, Any], snapshot_id: str,
                      relations: dict[str, Any], expected_ordinal: int,
                      payload_schemas: dict[str, Any] | None = None) -> list[str]:
    if not _closed(value, FACT_CANDIDATE_FIELDS):
        return ["FactCandidateV1 is not closed"]
    errors: list[str] = []
    relation = value.get("relation")
    registry = relations.get(relation) if type(relations) is dict and type(relation) is str else None
    if value.get("candidateOrdinal") != expected_ordinal:
        errors.append("FactCandidateV1 ordinal is not contiguous")
    if relation not in stage.get("relations", []) or type(registry) is not dict:
        errors.append("FactCandidateV1 relation was not requested")
    else:
        if value.get("resolution") not in registry.get("ladder", []) or value.get("layer") != registry.get("layer"):
            errors.append("FactCandidateV1 rung/layer invalid")
    if value.get("producer") != "rust-semantic" or value.get("producerVersion") != stage.get("providerVersion") or value.get("language") != "rust":
        errors.append("FactCandidateV1 provider context mismatch")
    if value.get("schemaVersion") != 1 or not _sha(value.get("sourceUniverseId")) or not _identity(value.get("targetUniverseId")):
        errors.append("FactCandidateV1 schema/universe invalid")
    if not _u64(value.get("confidenceMillionths")) or value["confidenceMillionths"] > 1000000:
        errors.append("FactCandidateV1 confidence invalid")
    if not _identity(value.get("relationSchemaId")):
        errors.append("FactCandidateV1 relation schema invalid")
    payload = value.get("canonicalRelationPayload")
    if type(payload) is not bytes or len(payload) > EXPECTED_LIMITS["maxCanonicalRelationPayloadBytes"]:
        errors.append("FactCandidateV1 payload is not bounded bytes")
    else:
        try:
            decoded = cbor_decode_canonical(payload)
            if type(decoded) is not dict:
                errors.append("FactCandidateV1 relation payload is not a closed map")
            elif type(payload_schemas) is not dict or type(relation) is not str or type(payload_schemas.get(relation)) is not dict:
                errors.append("FactCandidateV1 relation payload host schema unavailable")
            else:
                selected_schema = payload_schemas[relation]
                if value.get("relationSchemaId") != selected_schema.get("schemaId") or value.get("schemaVersion") != selected_schema.get("schemaVersion"):
                    errors.append("FactCandidateV1 relation schema id/version mismatch")
                errors.extend(_relation_payload_errors(decoded, selected_schema, value.get("resolution")))
                if selected_schema.get("universeRule") == "same-only" and value.get("sourceUniverseId") != value.get("targetUniverseId"):
                    errors.append("FactCandidateV1 same-only universe rule violated")
        except ValueError:
            errors.append("FactCandidateV1 relation payload is not canonical CBOR")
    anchors = value.get("anchors")
    if type(anchors) is not list or not anchors:
        errors.append("FactCandidateV1 anchors empty/non-array")
    else:
        for anchor in anchors:
            errors.extend(_anchor_errors(anchor, snapshot_id))
        try:
            encoded = [cbor_encode(anchor) for anchor in anchors]
            if encoded != sorted(encoded) or len(encoded) != len(set(encoded)):
                errors.append("FactCandidateV1 anchors not canonical sorted unique")
        except ValueError:
            errors.append("FactCandidateV1 anchor encoding invalid")
    return errors


def _commit(domain: str, value: Any) -> str:
    return "sha256:" + sha256_bytes(domain.encode("utf-8") + b"\0" + cbor_encode(value))


def _snapshot_entry_errors(value: Any) -> list[str]:
    fields = {"path", "kind", "byteLength", "contentSha256", "executable", "targetBytes"}
    if not _closed(value, fields) or not _canonical_path(value.get("path")):
        return ["SnapshotEntryV1 is not closed/canonical"]
    if value.get("kind") == "file":
        if not _u64(value.get("byteLength")) or not _digest(value.get("contentSha256")) or type(value.get("executable")) is not bool or value.get("targetBytes") is not None:
            return ["SnapshotEntryV1 file variant invalid"]
        return []
    if value.get("kind") == "symlink":
        if any(value.get(key) is not None for key in ("byteLength", "contentSha256", "executable")) or type(value.get("targetBytes")) is not bytes or not value["targetBytes"]:
            return ["SnapshotEntryV1 symlink variant invalid"]
        return []
    return ["SnapshotEntryV1 kind invalid"]


def _stage_errors(value: Any, *, relations: dict[str, Any], provider_version: str) -> list[str]:
    fields = {
        "kind", "stageId", "dependsOn", "operator", "providerId", "relations",
        "capabilityGrants", "budget", "subjects", "requestedCoverageDomain",
    }
    if not _closed(value, fields):
        return ["StageRequestV1 is not closed"]
    errors: list[str] = []
    if value.get("kind") != "fact-derivation" or value.get("operator") != "semantic-provider" or value.get("providerId") != "rust-semantic" or not _identity(value.get("stageId")):
        errors.append("StageRequestV1 constants/identity invalid")
    if not _sorted_unique_text(value.get("dependsOn")) or not _sorted_unique_text(value.get("capabilityGrants")):
        errors.append("StageRequestV1 dependency/grant arrays not sorted unique")
    requested_relations = value.get("relations")
    relations_valid = _sorted_unique_text(requested_relations, allow_empty=False)
    if not relations_valid or len(requested_relations) > EXPECTED_LIMITS["maxRelationsPerStage"] or any(rel not in relations for rel in requested_relations):
        errors.append("StageRequestV1 relations invalid")
    budget = value.get("budget")
    if budget is not None:
        if not _closed(budget, {"unit", "limit"}) or budget.get("unit") not in {"work-units", "milliseconds", "bytes", "items"} or type(budget.get("limit")) is not int or not 1 <= budget["limit"] <= 0x7FFFFFFFFFFFFFFF:
            errors.append("StageRequestV1 budget invalid")
    subjects = value.get("subjects")
    if type(subjects) is not list or not subjects or len(subjects) > EXPECTED_LIMITS["maxSubjectsPerStage"]:
        errors.append("StageRequestV1 subjects invalid")
        subjects = []
    else:
        for index, subject in enumerate(subjects):
            if not _closed(subject, {"subjectOrdinal", "subjectId", "path", "startByte", "endByte"}) or subject.get("subjectOrdinal") != index or not _identity(subject.get("subjectId")) or not _canonical_path(subject.get("path")) or not _u64(subject.get("startByte")) or not _u64(subject.get("endByte")) or subject["endByte"] <= subject["startByte"]:
                errors.append("SubjectV1 invalid/noncontiguous")
    expected_scope = _commit("opensip.rust-provider.subject-scope.v1", subjects) if subjects else None
    domain = value.get("requestedCoverageDomain")
    if type(domain) is not list or not domain or len(domain) > EXPECTED_LIMITS["maxRequestedCoverageKeysPerStage"]:
        errors.append("StageRequestV1 Coverage domain invalid")
    else:
        encoded: list[bytes] = []
        for key in domain:
            errors.extend(_coverage_key_errors(key, relations))
            if type(key) is dict:
                if key.get("subjectScopeCommitment") != expected_scope or key.get("relation") not in requested_relations or key.get("producerVersion") != provider_version:
                    errors.append("StageRequestV1 Coverage key/context mismatch")
                try:
                    encoded.append(cbor_encode(key))
                except ValueError:
                    errors.append("StageRequestV1 Coverage key not encodable")
        if encoded != sorted(encoded) or len(encoded) != len(set(encoded)):
            errors.append("StageRequestV1 Coverage domain not canonical sorted unique")
    return errors


def _coverage_result_errors(value: Any, *, stage_id: str, expected_key: Any,
                            ordinal: int, state: str, deficiency: Any) -> list[str]:
    fields = {"stageId", "entryOrdinal", "coverageState", "key", "deficiency"}
    if not _closed(value, fields):
        return ["CoverageResultV1 is not closed"]
    if value.get("stageId") != stage_id or value.get("entryOrdinal") != ordinal or value.get("coverageState") != state or value.get("deficiency") != deficiency or value.get("key") != expected_key:
        return ["CoverageResultV1 does not exactly match requested key/state"]
    if (state == "complete") != (deficiency is None):
        return ["CoverageResultV1 complete/deficiency union invalid"]
    return []


def _payload_fixture_catalog(protocol: dict[str, Any], deps: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    fx = _fixture_values(deps)
    content = b"0123456789"
    entry = {
        "path": "src/lib.rs",
        "kind": "file",
        "byteLength": len(content),
        "contentSha256": sha256_bytes(content),
        "executable": False,
        "targetBytes": None,
    }
    entries = [entry]
    manifest_digest = sha256_bytes(cbor_encode(entries))
    wire_stage = {key: copy.deepcopy(value) for key, value in fx["stage"].items() if key != "providerVersion"}
    wire_stage["budget"] = {"unit": "items", "limit": 10}
    complete_result = {
        "stageId": wire_stage["stageId"],
        "entryOrdinal": 0,
        "coverageState": "complete",
        "key": copy.deepcopy(fx["coverageKey"]),
        "deficiency": None,
    }
    unavailable_result = copy.deepcopy(complete_result)
    unavailable_result["coverageState"] = "unknown"
    unavailable_result["deficiency"] = "provider-unavailable"
    budget_result = copy.deepcopy(complete_result)
    budget_result["coverageState"] = "unknown"
    budget_result["deficiency"] = "budget-exhausted"
    stage_candidates = [copy.deepcopy(fx["candidate"])]
    stage_coverage = [complete_result]
    stage_fact_commitment = _commit("opensip.rust-provider.stage-facts.v1", stage_candidates)
    stage_coverage_commitment = _commit("opensip.rust-provider.stage-coverage.v1", stage_coverage)
    fact_stream_commitment = _commit("opensip.rust-provider.fact-stream.v1", stage_candidates)
    coverage_stream_commitment = _commit("opensip.rust-provider.coverage-stream.v1", stage_coverage)
    expected_identity = {
        "protocolMajor": 1,
        "providerBuildId": fx["universe"]["providerBuildId"],
        "rustCommitHash": fx["universe"]["rustCommitHash"],
        "hostTriple": fx["universe"]["hostTriple"],
        "targetTriple": fx["universe"]["targetTriple"],
        "sysrootDigest": fx["universe"]["sysrootDigest"],
    }
    open_universe = {
        "executionId": "exec1_" + "27" * 16,
        "snapshotId": fx["snapshotId"],
        "planId": fx["planId"],
        "planIntentCommitment": fx["planIntentCommitment"],
        "providerId": "rust-semantic",
        "universe": copy.deepcopy(fx["universe"]),
        "repositoryResolution": copy.deepcopy(fx["repoDisabled"]),
    }
    seal = {
        "snapshotId": fx["snapshotId"],
        "manifestSha256": manifest_digest,
        "entryCount": 1,
        "totalFileBytes": len(content),
        "totalChunkCount": 1,
    }
    analyze = {
        "analysisOrdinal": 0,
        "executionId": open_universe["executionId"],
        "snapshotId": fx["snapshotId"],
        "planId": fx["planId"],
        "stages": [wire_stage],
    }
    payloads = {
        "Hello": {
            "hostBuildId": "opensip-host:1",
            "expectedProtocolContractSha256": LOCAL_RAW_HASHES[PROTOCOL],
            "expectedIdentity": expected_identity,
            "expectedCapabilities": copy.deepcopy(fx["capability"]),
            "limits": copy.deepcopy(EXPECTED_LIMITS),
        },
        "HelloAck": {
            **copy.deepcopy(expected_identity),
            "capabilities": copy.deepcopy(fx["capability"]),
        },
        "OpenUniverse": open_universe,
        "UniverseAccepted": {
            "executionId": open_universe["executionId"],
            "snapshotId": open_universe["snapshotId"],
            "planId": open_universe["planId"],
            "providerId": open_universe["providerId"],
            "universe": copy.deepcopy(open_universe["universe"]),
            "repositoryResolution": copy.deepcopy(open_universe["repositoryResolution"]),
        },
        "SnapshotManifest": {
            "snapshotId": fx["snapshotId"],
            "manifestSha256": manifest_digest,
            "entries": entries,
        },
        "SnapshotFileChunk": {
            "snapshotId": fx["snapshotId"],
            "path": "src/lib.rs",
            "chunkIndex": 0,
            "byteOffset": 0,
            "bytes": content,
        },
        "SnapshotSeal": seal,
        "SnapshotAccepted": copy.deepcopy(seal),
        "Analyze": analyze,
        "FactBatch": {
            "analysisOrdinal": 0,
            "stageId": wire_stage["stageId"],
            "batchIndex": 0,
            "candidates": stage_candidates,
        },
        "Coverage": {
            "analysisOrdinal": 0,
            "stageId": wire_stage["stageId"],
            "entries": stage_coverage,
            "coverageCommitment": stage_coverage_commitment,
        },
        "Unavailable": {
            "analysisOrdinal": 0,
            "affectedStageIds": [wire_stage["stageId"]],
            "reason": "generated-cfg-unavailable",
            "coverage": [unavailable_result],
            "coverageCommitment": _commit("opensip.rust-provider.coverage-stream.v1", [unavailable_result]),
        },
        "BudgetExhausted": {
            "analysisOrdinal": 0,
            "triggerStageId": wire_stage["stageId"],
            "unit": "items",
            "limit": 10,
            "observed": 11,
            "coverage": [budget_result],
            "coverageCommitment": _commit("opensip.rust-provider.coverage-stream.v1", [budget_result]),
        },
        "Complete": {
            "analysisOrdinal": 0,
            "stageResults": [{
                "stageId": wire_stage["stageId"],
                "factCount": 1,
                "coverageEntryCount": 1,
                "factCommitment": stage_fact_commitment,
                "coverageCommitment": stage_coverage_commitment,
            }],
            "factStreamCommitment": fact_stream_commitment,
            "coverageStreamCommitment": coverage_stream_commitment,
        },
        "ProviderFault": {
            "executionId": open_universe["executionId"],
            "analysisOrdinal": 0,
            "phase": "analysis",
            "faultKind": "internal-invariant",
            "detailCode": "rust-provider-invariant",
        },
        "Cancel": {
            "executionId": open_universe["executionId"],
            "analysisOrdinal": 0,
            "reason": "user-interrupt",
        },
        "Cancelled": {
            "executionId": open_universe["executionId"],
            "analysisOrdinal": 0,
            "observedPhase": "analysis",
        },
    }
    context = {
        **fx,
        "expectedIdentity": expected_identity,
        "openUniverse": open_universe,
        "manifestEntries": entries,
        "manifestDigest": manifest_digest,
        "snapshotContent": content,
        "seal": seal,
        "analyze": analyze,
        "wireStage": wire_stage,
        "stageCandidates": stage_candidates,
        "stageCoverage": stage_coverage,
        "unavailableCoverage": [unavailable_result],
        "budgetCoverage": [budget_result],
    }
    return payloads, context


def _payload_errors(protocol: dict[str, Any], frame_type: str, payload: Any,
                    context: dict[str, Any]) -> list[str]:
    frame = EXPECTED_FRAMES.get(frame_type)
    if frame is None or type(payload) is not dict:
        return ["payload frame/type invalid"]
    schema = protocol.get("wireSchema", {}).get("payloadSchemas", {}).get(frame[1], {})
    required = set(schema.get("required", [])) if type(schema) is dict else set()
    if set(payload) != required:
        return [f"{frame[1]} exact field set invalid"]
    errors: list[str] = []
    open_value = context["openUniverse"]
    analyze = context["analyze"]
    stage = context["wireStage"]
    if frame_type == "Hello":
        if not _identity(payload.get("hostBuildId")) or payload.get("expectedProtocolContractSha256") != LOCAL_RAW_HASHES[PROTOCOL] or payload.get("limits") != EXPECTED_LIMITS:
            errors.append("Hello identity/contract/limits invalid")
        ident = payload.get("expectedIdentity")
        if not _closed(ident, {"protocolMajor", "providerBuildId", "rustCommitHash", "hostTriple", "targetTriple", "sysrootDigest"}) or ident != context["expectedIdentity"]:
            errors.append("Hello expectedIdentity invalid")
        errors.extend(_capability_errors(payload.get("expectedCapabilities"), context["capability"]))
    elif frame_type == "HelloAck":
        expected = {**context["expectedIdentity"], "capabilities": context["capability"]}
        if payload != expected:
            errors.append("HelloAck does not exactly match expected identity/capability")
    elif frame_type == "OpenUniverse":
        if not _identity(payload.get("executionId")) or SNAP_RE.fullmatch(payload.get("snapshotId", "")) is None or PLAN_RE.fullmatch(payload.get("planId", "")) is None or not _sha(payload.get("planIntentCommitment")) or payload.get("providerId") != "rust-semantic":
            errors.append("OpenUniverse identity invalid")
        errors.extend(_rust_universe_errors(payload.get("universe")))
        errors.extend(_repository_errors(payload.get("repositoryResolution"), payload.get("universe")))
    elif frame_type == "UniverseAccepted":
        expected = {key: copy.deepcopy(open_value[key]) for key in ("executionId", "snapshotId", "planId", "providerId", "universe", "repositoryResolution")}
        if payload != expected:
            errors.append("UniverseAccepted is not exact OpenUniverse echo")
    elif frame_type == "SnapshotManifest":
        entries = payload.get("entries")
        if payload.get("snapshotId") != open_value["snapshotId"] or type(entries) is not list or not entries or len(entries) > EXPECTED_LIMITS["maxSnapshotEntries"]:
            errors.append("SnapshotManifest identity/count invalid")
        else:
            for row in entries:
                errors.extend(_snapshot_entry_errors(row))
            paths = [row.get("path") for row in entries if type(row) is dict]
            if len(paths) != len(entries) or not all(_canonical_path(path) for path in paths):
                errors.append("SnapshotManifest paths malformed")
            elif paths != sorted(paths, key=lambda x: x.encode("utf-8")) or len(paths) != len(set(paths)):
                errors.append("SnapshotManifest paths not sorted unique")
            try:
                encoded_entries = cbor_encode(entries)
            except ValueError:
                encoded_entries = b""
                errors.append("SnapshotManifest entries not canonical-CBOR encodable")
            if payload.get("manifestSha256") != sha256_bytes(encoded_entries):
                errors.append("SnapshotManifest digest mismatch")
    elif frame_type == "SnapshotFileChunk":
        if payload.get("snapshotId") != open_value["snapshotId"] or payload.get("path") != "src/lib.rs" or payload.get("chunkIndex") != 0 or payload.get("byteOffset") != 0 or type(payload.get("bytes")) is not bytes or not payload["bytes"] or len(payload["bytes"]) > EXPECTED_LIMITS["maxSnapshotChunkBytes"]:
            errors.append("SnapshotFileChunk identity/order/bound invalid")
    elif frame_type in {"SnapshotSeal", "SnapshotAccepted"}:
        if payload != context["seal"]:
            errors.append(f"{frame_type} does not match exact validated snapshot counts")
    elif frame_type == "Analyze":
        if payload.get("analysisOrdinal") != 0 or payload.get("executionId") != open_value["executionId"] or payload.get("snapshotId") != open_value["snapshotId"] or payload.get("planId") != open_value["planId"]:
            errors.append("Analyze identity invalid")
        stages = payload.get("stages")
        if type(stages) is not list or not stages or len(stages) > EXPECTED_LIMITS["maxAnalyzeStages"]:
            errors.append("Analyze stages invalid")
        else:
            ids: list[str] = []
            for row in stages:
                errors.extend(_stage_errors(row, relations=context["relations"], provider_version=context["universe"]["providerBuildId"]))
                if type(row) is dict:
                    ids.append(row.get("stageId"))
            if len(ids) != len(stages) or not all(_identity(stage_id) for stage_id in ids):
                errors.append("Analyze stage identifiers malformed")
            elif ids != sorted(ids, key=lambda x: x.encode("utf-8")) or len(ids) != len(set(ids)):
                errors.append("Analyze stages not in unique ExecutionPlan order")
    elif frame_type == "FactBatch":
        if payload.get("analysisOrdinal") != 0 or payload.get("stageId") != stage["stageId"] or payload.get("batchIndex") != 0:
            errors.append("FactBatch attribution/index invalid")
        candidates = payload.get("candidates")
        if type(candidates) is not list or not candidates or len(candidates) > EXPECTED_LIMITS["maxFactBatchCandidates"]:
            errors.append("FactBatch candidate array invalid")
        else:
            stage_context = {**stage, "providerVersion": context["universe"]["providerBuildId"]}
            for index, candidate in enumerate(candidates):
                errors.extend(_candidate_errors(
                    candidate, stage=stage_context,
                    snapshot_id=open_value["snapshotId"],
                    relations=context["relations"], expected_ordinal=index,
                    payload_schemas=context["payloadSchemas"],
                ))
    elif frame_type == "Coverage":
        entries = payload.get("entries")
        if payload.get("analysisOrdinal") != 0 or payload.get("stageId") != stage["stageId"] or type(entries) is not list or len(entries) != len(stage["requestedCoverageDomain"]):
            errors.append("Coverage attribution/cardinality invalid")
        else:
            for index, key in enumerate(stage["requestedCoverageDomain"]):
                errors.extend(_coverage_result_errors(entries[index], stage_id=stage["stageId"], expected_key=key, ordinal=index, state="complete", deficiency=None))
            if payload.get("coverageCommitment") != _commit("opensip.rust-provider.stage-coverage.v1", entries):
                errors.append("Coverage commitment mismatch")
    elif frame_type in {"Unavailable", "BudgetExhausted"}:
        coverage = payload.get("coverage")
        wanted_deficiency = "provider-unavailable" if frame_type == "Unavailable" else "budget-exhausted"
        if payload.get("analysisOrdinal") != 0 or type(coverage) is not list or len(coverage) != len(stage["requestedCoverageDomain"]):
            errors.append(f"{frame_type} coverage cardinality invalid")
        else:
            for index, key in enumerate(stage["requestedCoverageDomain"]):
                errors.extend(_coverage_result_errors(coverage[index], stage_id=stage["stageId"], expected_key=key, ordinal=index, state="unknown", deficiency=wanted_deficiency))
            if payload.get("coverageCommitment") != _commit("opensip.rust-provider.coverage-stream.v1", coverage):
                errors.append(f"{frame_type} coverage commitment mismatch")
        if frame_type == "Unavailable":
            if payload.get("affectedStageIds") != [stage["stageId"]] or payload.get("reason") not in {"semantic-universe-incomplete", "snapshot-resolution-input-missing", "unsupported-compiler-mode", "generated-cfg-unavailable"}:
                errors.append("Unavailable stage/reason invalid")
        else:
            budget = stage.get("budget")
            if payload.get("triggerStageId") != stage["stageId"] or type(budget) is not dict or payload.get("unit") != budget.get("unit") or payload.get("unit") == "milliseconds" or payload.get("limit") != budget.get("limit") or not _u64(payload.get("observed")) or payload["observed"] <= payload["limit"]:
                errors.append("BudgetExhausted trigger/unit/count invalid")
            if payload.get("unit") in {"work-units", "items"} and payload.get("observed") != payload.get("limit") + 1:
                errors.append("BudgetExhausted unit counter not first disallowed count")
    elif frame_type == "Complete":
        results = payload.get("stageResults")
        if payload.get("analysisOrdinal") != 0 or type(results) is not list or len(results) != 1:
            errors.append("Complete stageResults invalid")
        else:
            expected = {
                "stageId": stage["stageId"],
                "factCount": len(context["stageCandidates"]),
                "coverageEntryCount": len(context["stageCoverage"]),
                "factCommitment": _commit("opensip.rust-provider.stage-facts.v1", context["stageCandidates"]),
                "coverageCommitment": _commit("opensip.rust-provider.stage-coverage.v1", context["stageCoverage"]),
            }
            if results != [expected]:
                errors.append("Complete stage result/count/commitment mismatch")
        if payload.get("factStreamCommitment") != _commit("opensip.rust-provider.fact-stream.v1", context["stageCandidates"]) or payload.get("coverageStreamCommitment") != _commit("opensip.rust-provider.coverage-stream.v1", context["stageCoverage"]):
            errors.append("Complete stream commitment mismatch")
    elif frame_type == "ProviderFault":
        if payload.get("executionId") not in {None, open_value["executionId"]} or payload.get("analysisOrdinal") not in {None, 0} or payload.get("phase") not in {"handshake", "universe", "snapshot", "analysis"} or payload.get("faultKind") not in {"compiler-crash", "internal-invariant", "input-rejected"} or not _identity(payload.get("detailCode")):
            errors.append("ProviderFault union invalid")
    elif frame_type == "Cancel":
        if payload.get("executionId") not in {None, open_value["executionId"]} or payload.get("analysisOrdinal") not in {None, 0} or payload.get("reason") != "user-interrupt":
            errors.append("Cancel union invalid")
    elif frame_type == "Cancelled":
        if payload.get("executionId") not in {None, open_value["executionId"]} or payload.get("analysisOrdinal") not in {None, 0} or payload.get("observedPhase") not in {"handshake", "universe", "snapshot", "analysis"}:
            errors.append("Cancelled union invalid")
    return errors


def _admission_outcome(*, terminal: str | None, semantic_valid: bool,
                       exit_status: int | None, eof: bool, extra_stdout: bool,
                       user_signal: bool) -> tuple[str, str, str]:
    """Observed fate -> candidate, Coverage, D9-provider contribution."""
    if user_signal:
        return "DISCARD_ALL", "ADMIT_NONE", "interrupted/130"
    process_valid = semantic_valid and exit_status == 0 and eof and not extra_stdout
    if not process_valid or terminal not in {
        "Complete", "Unavailable", "BudgetExhausted", "ProviderFault", "Cancelled",
    }:
        return "DISCARD_ALL", "ADMIT_NONE", "provider-protocol/PROVIDER.PROTOCOL_VIOLATION"
    if terminal == "Complete":
        return "ADMIT_ALL_ATOMIC", "ADMIT_COMPLETE", "no-provider-deficiency-or-fault"
    if terminal == "Unavailable":
        return "DISCARD_ALL", "ADMIT_EXHAUSTIVE_UNKNOWN", "provider-unavailable/COVERAGE.PROVIDER_UNAVAILABLE"
    if terminal == "BudgetExhausted":
        return "DISCARD_ALL", "ADMIT_EXHAUSTIVE_UNKNOWN", "budget-exhausted/COVERAGE.BUDGET_EXHAUSTED"
    if terminal == "ProviderFault":
        return "DISCARD_ALL", "ADMIT_NONE", "provider-protocol/PROVIDER.PROTOCOL_VIOLATION"
    return "DISCARD_ALL", "ADMIT_NONE", "provider-protocol/PROVIDER.PROTOCOL_VIOLATION"


def _payload_shape_errors(protocol: Any) -> list[str]:
    errors: list[str] = []
    try:
        wire = protocol["wireSchema"]
        frames = wire["frameSchemas"]
        payloads = wire["payloadSchemas"]
    except (KeyError, TypeError):
        return ["RPP-SCHEMA: wireSchema/frameSchemas/payloadSchemas missing or malformed"]
    if type(frames) is not dict or set(frames) != set(EXPECTED_FRAMES):
        errors.append("RPP-SCHEMA: frame vocabulary is not exact")
    else:
        for name, expected in EXPECTED_FRAMES.items():
            row = frames.get(name)
            wanted = {"direction": expected[0], "payloadType": expected[1], "terminal": expected[2]}
            if row != wanted:
                errors.append(f"RPP-SCHEMA: {name} frame binding drifted")
    if type(payloads) is not dict or {v[1] for v in EXPECTED_FRAMES.values()} != set(payloads):
        errors.append("RPP-SCHEMA: payload vocabulary is not exact")
    else:
        for name, schema in payloads.items():
            if type(schema) is not dict or schema.get("closed") is not True or schema.get("optional") != []:
                errors.append(f"RPP-SCHEMA: {name} is not closed/no-optional")
                continue
            required = schema.get("required")
            fields = schema.get("fields")
            if type(required) is not list or type(fields) is not dict or set(required) != set(fields) or len(required) != len(set(required)):
                errors.append(f"RPP-SCHEMA: {name} required/field set mismatch")
    envelope = wire.get("envelope") if type(wire) is dict else None
    if type(envelope) is not dict or envelope.get("closed") is not True or envelope.get("optional") != [] or set(envelope.get("required", [])) != {"protocolMajor", "direction", "sequence", "frameType", "payload"}:
        errors.append("RPP-SCHEMA: envelope is not exact closed shape")
    return errors


def _envelope_errors(protocol: dict[str, Any], envelope: Any) -> list[str]:
    fields = {"protocolMajor", "direction", "sequence", "frameType", "payload"}
    if not _closed(envelope, fields):
        return ["envelope is not exact closed map"]
    errors: list[str] = []
    if envelope.get("protocolMajor") != 1 or not _u64(envelope.get("sequence")):
        errors.append("envelope protocolMajor/sequence invalid")
    frame = EXPECTED_FRAMES.get(envelope.get("frameType"))
    if frame is None or envelope.get("direction") != frame[0]:
        errors.append("envelope frameType/direction invalid")
    if type(envelope.get("payload")) is not dict:
        errors.append("envelope payload is not map")
    else:
        try:
            schema = protocol["wireSchema"]["payloadSchemas"][frame[1]] if frame else None
            required = set(schema["required"])
            if set(envelope["payload"]) != required:
                errors.append("envelope payload does not match exact selected schema")
        except (KeyError, TypeError):
            errors.append("envelope selected payload schema missing")
    return errors


def _session_type_errors(events: Any, *, stage_count: int, user_signal: bool = False,
                         exit_status: int | None = 0, eof: bool = True,
                         extra_stdout: bool = False) -> list[str]:
    if type(events) is not list:
        return ["session events not array"]
    errors: list[str] = []
    seq = {"host-to-worker": 0, "worker-to-host": 0}
    phase = "START"
    stage_index = 0
    batch_index = 0
    analysis_output = False
    terminal: str | None = None
    cancel_sent = False
    for event in events:
        if type(event) is not tuple or len(event) != 3:
            errors.append("session event malformed")
            continue
        direction, sequence, frame_type = event
        if direction not in seq or sequence != seq.get(direction):
            errors.append("session independent sequence violation")
            continue
        seq[direction] += 1
        expected = EXPECTED_FRAMES.get(frame_type)
        if expected is None or expected[0] != direction:
            errors.append("session frame direction/vocabulary violation")
            continue
        if terminal is not None:
            errors.append("session frame after terminal")
            continue
        if frame_type == "Cancel":
            if cancel_sent:
                errors.append("second Cancel")
            cancel_sent = True
            phase = "WAIT_CANCELLED"
            continue
        if phase == "WAIT_CANCELLED":
            if frame_type != "Cancelled":
                errors.append("only Cancelled may follow Cancel")
            else:
                terminal = frame_type
            continue
        if frame_type == "ProviderFault" and phase != "START":
            terminal = frame_type
            continue
        expected_by_phase = {
            "START": "Hello",
            "WAIT_HELLO_ACK": "HelloAck",
            "READY_OPEN": "OpenUniverse",
            "WAIT_UNIVERSE": "UniverseAccepted",
            "READY_MANIFEST": "SnapshotManifest",
            "WAIT_SNAPSHOT": None,
            "WAIT_SNAPSHOT_ACCEPTED": "SnapshotAccepted",
            "READY_ANALYZE": "Analyze",
        }
        if phase in expected_by_phase:
            wanted = expected_by_phase[phase]
            if phase == "WAIT_SNAPSHOT" and frame_type in {"SnapshotFileChunk", "SnapshotSeal"}:
                if frame_type == "SnapshotSeal":
                    phase = "WAIT_SNAPSHOT_ACCEPTED"
                continue
            if frame_type != wanted:
                errors.append(f"session state {phase} rejects {frame_type}")
                continue
            phase = {
                "START": "WAIT_HELLO_ACK",
                "WAIT_HELLO_ACK": "READY_OPEN",
                "READY_OPEN": "WAIT_UNIVERSE",
                "WAIT_UNIVERSE": "READY_MANIFEST",
                "READY_MANIFEST": "WAIT_SNAPSHOT",
                "WAIT_SNAPSHOT_ACCEPTED": "READY_ANALYZE",
                "READY_ANALYZE": "ANALYSIS",
            }[phase]
            continue
        if phase != "ANALYSIS":
            errors.append(f"session has unhandled phase/frame {phase}/{frame_type}")
            continue
        if frame_type == "Unavailable":
            if analysis_output or stage_index != 0:
                errors.append("Unavailable after analysis output")
            terminal = frame_type
        elif frame_type == "BudgetExhausted":
            terminal = frame_type
        elif frame_type == "FactBatch":
            analysis_output = True
            batch_index += 1
        elif frame_type == "Coverage":
            analysis_output = True
            stage_index += 1
            batch_index = 0
            if stage_index > stage_count:
                errors.append("too many Coverage frames")
        elif frame_type == "Complete":
            if stage_index != stage_count:
                errors.append("Complete before exhaustive Coverage")
            terminal = frame_type
        else:
            errors.append(f"frame {frame_type} illegal during analysis")
    if terminal is None:
        errors.append("session missing terminal")
    if user_signal:
        if not cancel_sent:
            errors.append("user-signal fixture lacks Cancel")
    else:
        if exit_status != 0 or not eof or extra_stdout:
            errors.append("terminal lacks zero-exit/EOF/no-extra fate")
    return errors


def _fixture_values(deps: dict[str, Any]) -> dict[str, Any]:
    ri = deps["resolved-inputs.v2.json"]
    vector = next(
        row for row in ri["planIdContract"]["goldenVectors"]["positive"]
        if row.get("id") == "planid-v1-ci-full-providers"
    )
    construction = vector["planInputConstruction"]
    rust_wrapper = next(
        row for row in construction["semanticUniverses"]
        if row.get("providerId") == "rust-semantic"
    )
    universe = copy.deepcopy(rust_wrapper["universe"])
    capability = _selected_rust_capability(deps["delivery.v2.json"])
    snapshot_id = construction["snapshotId"]
    plan_id = vector["expectedPlanId"]
    source_universe = "sha256:" + "24" * 32
    subject = {
        "subjectOrdinal": 0,
        "subjectId": "rust:item",
        "path": "src/lib.rs",
        "startByte": 0,
        "endByte": 10,
    }
    subject_commitment = "sha256:" + sha256_bytes(
        b"opensip.rust-provider.subject-scope.v1\0" + cbor_encode([subject])
    )
    relations = deps["fact-plane.v1.json"]["relationRegistry"]["relations"]
    payload_schemas = deps["fact-plane.v1.json"]["factRecordContractV1"]["relationPayloadSchemaRegistryV1"]["schemas"]
    coverage_key = {
        "relation": "declares",
        "resolution": "syntactic",
        "sourceUniverseId": source_universe,
        "targetUniverseId": source_universe,
        "subjectScopeCommitment": subject_commitment,
        "producer": "rust-semantic",
        "producerVersion": universe["providerBuildId"],
        "schemaVersion": 1,
    }
    stage = {
        "kind": "fact-derivation",
        "stageId": "s2",
        "dependsOn": ["s1"],
        "operator": "semantic-provider",
        "providerId": "rust-semantic",
        "relations": ["declares", "references"],
        "capabilityGrants": ["grant-read", "grant-spawn"],
        "budget": None,
        "subjects": [subject],
        "requestedCoverageDomain": [coverage_key],
        "providerVersion": universe["providerBuildId"],
    }
    relation_payload = {
        "container": "rust:crate",
        "declared": "rust:item",
        "declarationKind": "function",
    }
    candidate = {
        "candidateOrdinal": 0,
        "relation": "declares",
        "resolution": "syntactic",
        "layer": "syntax",
        "producer": "rust-semantic",
        "producerVersion": universe["providerBuildId"],
        "schemaVersion": 1,
        "language": "rust",
        "sourceUniverseId": source_universe,
        "targetUniverseId": source_universe,
        "confidenceMillionths": 1000000,
        "relationSchemaId": "opensip.relation.declares.v1",
        "canonicalRelationPayload": cbor_encode(relation_payload),
        "anchors": [{
            "kind": "source-span",
            "snapshotId": snapshot_id,
            "path": "src/lib.rs",
            "contentSha256": "25" * 32,
            "startByte": 0,
            "endByte": 10,
            "factId": None,
        }],
    }
    repo_disabled = {
        "mode": "disabled",
        "grantId": None,
        "projectId": "prj1-" + "22" * 32,
        "network": False,
        "buildScriptOutputs": [],
        "procMacroOutputs": [],
        "toolPaths": [],
    }
    return {
        "universe": universe,
        "capability": capability,
        "snapshotId": snapshot_id,
        "planId": plan_id,
        "planIntentCommitment": vector["expectedPlanIntentCommitment"],
        "sourceUniverse": source_universe,
        "subjectCommitment": subject_commitment,
        "coverageKey": coverage_key,
        "stage": stage,
        "candidate": candidate,
        "repoDisabled": repo_disabled,
        "relations": relations,
        "payloadSchemas": payload_schemas,
    }


def _runtime_oracle_findings(protocol: dict[str, Any], deps: dict[str, Any]) -> tuple[list[str], int, int]:
    findings: list[str] = []
    positive = 0
    adversarial = 0
    try:
        fx = _fixture_values(deps)
        payloads, payload_context = _payload_fixture_catalog(protocol, deps)
    except (KeyError, TypeError, StopIteration, ValueError):
        return ["RPP-RUNTIME: cannot construct exact dependency-backed fixture"], positive, adversarial

    def positive_probe(name: str, fn: Callable[[], bool]) -> None:
        nonlocal positive
        positive += 1
        try:
            if fn() is not True:
                findings.append(f"RPP-RUNTIME {name}: positive probe failed")
        except (AttributeError, IndexError, KeyError, TypeError, ValueError, OverflowError):
            findings.append(f"RPP-RUNTIME {name}: positive probe raised")

    def negative_probe(name: str, fn: Callable[[], Any]) -> None:
        nonlocal adversarial
        adversarial += 1
        try:
            fn()
        except (AttributeError, IndexError, KeyError, TypeError, ValueError, OverflowError, StrictJsonError, json.JSONDecodeError):
            return
        findings.append(f"RPP-RUNTIME {name}: adversarial probe escaped")

    def reject_probe(name: str, fn: Callable[[], Any]) -> None:
        """A semantic malformed-input probe must return findings, never raise."""
        nonlocal adversarial
        adversarial += 1
        try:
            result = fn()
        except (AttributeError, IndexError, KeyError, TypeError, ValueError, OverflowError):
            findings.append(f"RPP-RUNTIME {name}: total validator raised")
            return
        if type(result) is not list or not result:
            findings.append(f"RPP-RUNTIME {name}: adversarial probe escaped")

    hello_payload = copy.deepcopy(payloads["Hello"])
    hello = {
        "protocolMajor": 1,
        "direction": "host-to-worker",
        "sequence": 0,
        "frameType": "Hello",
        "payload": hello_payload,
    }
    positive_probe("RPP-POS-CBOR-ROUNDTRIP", lambda: cbor_decode_canonical(cbor_encode(hello)) == hello)
    positive_probe("RPP-POS-FRAME-ROUNDTRIP", lambda: frame_decode(frame_encode(hello)) == hello)
    positive_probe("RPP-POS-ENVELOPE", lambda: _envelope_errors(protocol, hello) == [])
    positive_probe("RPP-POS-RUST-UNIVERSE", lambda: _rust_universe_errors(fx["universe"]) == [])
    positive_probe("RPP-POS-CAPABILITY", lambda: _capability_errors(fx["capability"], fx["capability"]) == [])
    positive_probe("RPP-POS-REPOSITORY-DISABLED", lambda: _repository_errors(fx["repoDisabled"], fx["universe"]) == [])
    positive_probe("RPP-POS-COVERAGE-KEY", lambda: _coverage_key_errors(fx["coverageKey"], fx["relations"]) == [])
    positive_probe(
        "RPP-POS-FACT-CANDIDATE",
        lambda: _candidate_errors(
            fx["candidate"], stage=fx["stage"], snapshot_id=fx["snapshotId"],
            relations=fx["relations"], expected_ordinal=0,
            payload_schemas=fx["payloadSchemas"],
        ) == [],
    )

    # Every frame is recursively checked as an exact payload, exact envelope,
    # canonical CBOR value, and length+raw-digest wire frame.
    for frame_type, payload in payloads.items():
        direction = EXPECTED_FRAMES[frame_type][0]
        envelope = {
            "protocolMajor": 1,
            "direction": direction,
            "sequence": 0,
            "frameType": frame_type,
            "payload": copy.deepcopy(payload),
        }
        positive_probe(
            f"RPP-POS-FULL-PAYLOAD-{frame_type}",
            lambda frame_type=frame_type, payload=payload, envelope=envelope: (
                _payload_errors(protocol, frame_type, payload, payload_context) == []
                and _envelope_errors(protocol, envelope) == []
                and frame_decode(frame_encode(envelope)) == envelope
            ),
        )

    prepared_universe = copy.deepcopy(fx["universe"])
    prepared_universe["resolvedInputs"]["executionCapableResolution"] = True
    prepared_universe["resolvedInputs"]["buildScriptOutputs"] = [{
        "packageId": "crate-a", "cfg": "generated",
        "outputDigest": "28" * 32,
    }]
    prepared_universe["resolvedInputs"]["procMacroOutputs"] = [{
        "crateId": "crate-a", "outputDigest": "29" * 32,
    }]
    prepared_repo = {
        "mode": "prepared",
        "grantId": "grant-repository-execution",
        "projectId": fx["repoDisabled"]["projectId"],
        "network": False,
        "buildScriptOutputs": copy.deepcopy(prepared_universe["resolvedInputs"]["buildScriptOutputs"]),
        "procMacroOutputs": copy.deepcopy(prepared_universe["resolvedInputs"]["procMacroOutputs"]),
        "toolPaths": [{
            "artifactId": "rust-toolchain-bundle",
            "bundleRelativePath": "bin/cargo",
            "fileSha256": "30" * 32,
            "role": "cargo",
        }],
    }
    positive_probe(
        "RPP-POS-REPOSITORY-PREPARED",
        lambda: _rust_universe_errors(prepared_universe) == []
        and _repository_errors(prepared_repo, prepared_universe) == [],
    )
    positive_probe(
        "RPP-POS-ADMISSION-COMPLETE",
        lambda: _admission_outcome(
            terminal="Complete", semantic_valid=True, exit_status=0,
            eof=True, extra_stdout=False, user_signal=False,
        ) == ("ADMIT_ALL_ATOMIC", "ADMIT_COMPLETE", "no-provider-deficiency-or-fault"),
    )
    positive_probe(
        "RPP-POS-ADMISSION-UNAVAILABLE",
        lambda: _admission_outcome(
            terminal="Unavailable", semantic_valid=True, exit_status=0,
            eof=True, extra_stdout=False, user_signal=False,
        ) == ("DISCARD_ALL", "ADMIT_EXHAUSTIVE_UNKNOWN", "provider-unavailable/COVERAGE.PROVIDER_UNAVAILABLE"),
    )
    positive_probe(
        "RPP-POS-ADMISSION-BUDGET",
        lambda: _admission_outcome(
            terminal="BudgetExhausted", semantic_valid=True, exit_status=0,
            eof=True, extra_stdout=False, user_signal=False,
        ) == ("DISCARD_ALL", "ADMIT_EXHAUSTIVE_UNKNOWN", "budget-exhausted/COVERAGE.BUDGET_EXHAUSTED"),
    )
    positive_probe(
        "RPP-POS-ADMISSION-INVALID-FATE",
        lambda: _admission_outcome(
            terminal="Complete", semantic_valid=True, exit_status=1,
            eof=True, extra_stdout=False, user_signal=False,
        ) == ("DISCARD_ALL", "ADMIT_NONE", "provider-protocol/PROVIDER.PROTOCOL_VIOLATION"),
    )
    positive_probe(
        "RPP-POS-ADMISSION-USER-SIGNAL",
        lambda: _admission_outcome(
            terminal=None, semantic_valid=False, exit_status=None,
            eof=False, extra_stdout=False, user_signal=True,
        ) == ("DISCARD_ALL", "ADMIT_NONE", "interrupted/130"),
    )
    happy = [
        ("host-to-worker", 0, "Hello"),
        ("worker-to-host", 0, "HelloAck"),
        ("host-to-worker", 1, "OpenUniverse"),
        ("worker-to-host", 1, "UniverseAccepted"),
        ("host-to-worker", 2, "SnapshotManifest"),
        ("host-to-worker", 3, "SnapshotFileChunk"),
        ("host-to-worker", 4, "SnapshotSeal"),
        ("worker-to-host", 2, "SnapshotAccepted"),
        ("host-to-worker", 5, "Analyze"),
        ("worker-to-host", 3, "FactBatch"),
        ("worker-to-host", 4, "Coverage"),
        ("worker-to-host", 5, "Complete"),
    ]
    unavailable = happy[:9] + [("worker-to-host", 3, "Unavailable")]
    budget = happy[:10] + [("worker-to-host", 4, "BudgetExhausted")]
    cancel = happy[:9] + [
        ("host-to-worker", 6, "Cancel"),
        ("worker-to-host", 3, "Cancelled"),
    ]
    provider_fault = happy[:4] + [("worker-to-host", 2, "ProviderFault")]
    positive_probe("RPP-POS-SESSION-COMPLETE", lambda: _session_type_errors(happy, stage_count=1) == [])
    positive_probe("RPP-POS-SESSION-UNAVAILABLE", lambda: _session_type_errors(unavailable, stage_count=1) == [])
    positive_probe("RPP-POS-SESSION-BUDGET", lambda: _session_type_errors(budget, stage_count=1) == [])
    positive_probe("RPP-POS-SESSION-CANCEL", lambda: _session_type_errors(cancel, stage_count=1, user_signal=True, exit_status=None, eof=False) == [])
    positive_probe("RPP-POS-SESSION-PROVIDER-FAULT", lambda: _session_type_errors(provider_fault, stage_count=1) == [])

    negative_probe("RPP-NEG-JSON-DUPLICATE", lambda: strict_json_loads('{"a":1,"a":2}'))
    negative_probe("RPP-NEG-JSON-NAN", lambda: strict_json_loads('{"a":NaN}'))
    negative_probe("RPP-NEG-CBOR-NONSHORTEST", lambda: cbor_decode_canonical(b"\x18\x00"))
    negative_probe("RPP-NEG-CBOR-DUPLICATE-MAP", lambda: cbor_decode_canonical(bytes.fromhex("a2616100616101")))
    negative_probe("RPP-NEG-CBOR-FLOAT", lambda: cbor_decode_canonical(bytes.fromhex("f93c00")))
    bad_digest = bytearray(frame_encode(hello)); bad_digest[8] ^= 1
    negative_probe("RPP-NEG-FRAME-DIGEST", lambda: frame_decode(bytes(bad_digest)))
    oversize = (EXPECTED_LIMITS["maxFramePayloadBytes"] + 1).to_bytes(8, "big") + b"\x00" * 32
    negative_probe("RPP-NEG-FRAME-OVERSIZE", lambda: frame_decode(oversize))
    negative_probe("RPP-NEG-FRAME-TRUNCATED", lambda: frame_decode(frame_encode(hello)[:-1]))
    bad_seq = copy.deepcopy(happy); bad_seq[1] = ("worker-to-host", 1, "HelloAck")
    negative_probe(
        "RPP-NEG-SESSION-SEQUENCE",
        lambda: (_ for _ in ()).throw(ValueError()) if _session_type_errors(bad_seq, stage_count=1) else None,
    )
    missing_coverage = happy[:-2] + [happy[-1]]
    negative_probe(
        "RPP-NEG-SESSION-MISSING-COVERAGE",
        lambda: (_ for _ in ()).throw(ValueError()) if _session_type_errors(missing_coverage, stage_count=1) else None,
    )
    after_terminal = happy + [("worker-to-host", 6, "ProviderFault")]
    negative_probe(
        "RPP-NEG-SESSION-AFTER-TERMINAL",
        lambda: (_ for _ in ()).throw(ValueError()) if _session_type_errors(after_terminal, stage_count=1) else None,
    )
    unavailable_after_fact = happy[:10] + [("worker-to-host", 4, "Unavailable")]
    negative_probe(
        "RPP-NEG-UNAVAILABLE-AFTER-FACT",
        lambda: (_ for _ in ()).throw(ValueError()) if _session_type_errors(unavailable_after_fact, stage_count=1) else None,
    )
    bad_candidate = copy.deepcopy(fx["candidate"]); bad_candidate["producer"] = "typescript-semantic"
    negative_probe(
        "RPP-NEG-CANDIDATE-PRODUCER",
        lambda: (_ for _ in ()).throw(ValueError()) if _candidate_errors(
            bad_candidate, stage=fx["stage"], snapshot_id=fx["snapshotId"],
            relations=fx["relations"], expected_ordinal=0,
            payload_schemas=fx["payloadSchemas"],
        ) else None,
    )
    bad_coverage = copy.deepcopy(fx["coverageKey"]); bad_coverage["relation"] = "invented"
    negative_probe(
        "RPP-NEG-COVERAGE-RELATION",
        lambda: (_ for _ in ()).throw(ValueError()) if _coverage_key_errors(bad_coverage, fx["relations"]) else None,
    )

    type_mutations: dict[str, tuple[str, Any]] = {
        "Hello": ("hostBuildId", 1),
        "HelloAck": ("protocolMajor", "1"),
        "OpenUniverse": ("executionId", 1),
        "UniverseAccepted": ("universe", "not-a-record"),
        "SnapshotManifest": ("entries", "not-an-array"),
        "SnapshotFileChunk": ("bytes", "not-bytes"),
        "SnapshotSeal": ("entryCount", "1"),
        "SnapshotAccepted": ("entryCount", "1"),
        "Analyze": ("stages", {}),
        "FactBatch": ("candidates", {}),
        "Coverage": ("entries", {}),
        "Unavailable": ("coverage", {}),
        "BudgetExhausted": ("observed", "11"),
        "Complete": ("stageResults", {}),
        "ProviderFault": ("detailCode", 1),
        "Cancel": ("reason", 1),
        "Cancelled": ("observedPhase", 1),
    }
    for frame_type, payload in payloads.items():
        unknown = copy.deepcopy(payload)
        unknown["unknownField"] = None
        reject_probe(
            f"RPP-NEG-{frame_type}-UNKNOWN-FIELD",
            lambda frame_type=frame_type, unknown=unknown: _payload_errors(
                protocol, frame_type, unknown, payload_context,
            ),
        )
        missing = copy.deepcopy(payload)
        missing.pop(protocol["wireSchema"]["payloadSchemas"][EXPECTED_FRAMES[frame_type][1]]["required"][0])
        reject_probe(
            f"RPP-NEG-{frame_type}-MISSING-FIELD",
            lambda frame_type=frame_type, missing=missing: _payload_errors(
                protocol, frame_type, missing, payload_context,
            ),
        )
        bad_type = copy.deepcopy(payload)
        field, bad_value = type_mutations[frame_type]
        bad_type[field] = bad_value
        reject_probe(
            f"RPP-NEG-{frame_type}-TYPE",
            lambda frame_type=frame_type, bad_type=bad_type: _payload_errors(
                protocol, frame_type, bad_type, payload_context,
            ),
        )
        for hostile_name, hostile in (
            ("NULL", None), ("ARRAY", []), ("TEXT", "x"), ("INTEGER", 1),
        ):
            reject_probe(
                f"RPP-NEG-{frame_type}-ROOT-{hostile_name}",
                lambda frame_type=frame_type, hostile=hostile: _payload_errors(
                    protocol, frame_type, hostile, payload_context,
                ),
            )

    nested_mutations: list[tuple[str, str, str, Any]] = [
        ("HELLO-IDENTITY", "Hello", "expectedIdentity", {}),
        ("OPEN-UNIVERSE", "OpenUniverse", "universe", {}),
        ("SNAPSHOT-ENTRY", "SnapshotManifest", "entries", [{}]),
        ("ANALYZE-STAGE", "Analyze", "stages", [{}]),
        ("FACT-CANDIDATE", "FactBatch", "candidates", [{}]),
        ("COVERAGE-RESULT", "Coverage", "entries", [{}]),
        ("COMPLETE-RESULT", "Complete", "stageResults", [{}]),
    ]
    for label, frame_type, field, bad_value in nested_mutations:
        malformed = copy.deepcopy(payloads[frame_type])
        malformed[field] = bad_value
        reject_probe(
            f"RPP-NEG-NESTED-{label}",
            lambda frame_type=frame_type, malformed=malformed: _payload_errors(
                protocol, frame_type, malformed, payload_context,
            ),
        )

    for label, transform in (
        ("MISSING", lambda entries: []),
        ("DUPLICATE", lambda entries: entries + copy.deepcopy(entries)),
        ("UNREQUESTED", lambda entries: [{**copy.deepcopy(entries[0]), "key": {**copy.deepcopy(entries[0]["key"]), "relation": "references"}}]),
    ):
        bad = copy.deepcopy(payloads["Coverage"])
        bad["entries"] = transform(bad["entries"])
        reject_probe(
            f"RPP-NEG-COVERAGE-{label}",
            lambda bad=bad: _payload_errors(protocol, "Coverage", bad, payload_context),
        )
    bad_commitment = copy.deepcopy(payloads["Coverage"])
    bad_commitment["coverageCommitment"] = "sha256:" + "00" * 32
    reject_probe(
        "RPP-NEG-COVERAGE-COMMITMENT",
        lambda: _payload_errors(protocol, "Coverage", bad_commitment, payload_context),
    )

    capability_mismatch = copy.deepcopy(payloads["HelloAck"])
    capability_mismatch["capabilities"]["language"] = "typescript"
    reject_probe(
        "RPP-NEG-HANDSHAKE-CAPABILITY-MISMATCH",
        lambda: _payload_errors(protocol, "HelloAck", capability_mismatch, payload_context),
    )

    unknown_relation_payload = copy.deepcopy(fx["candidate"])
    decoded_relation = cbor_decode_canonical(unknown_relation_payload["canonicalRelationPayload"])
    decoded_relation["unknown"] = "forbidden"
    unknown_relation_payload["canonicalRelationPayload"] = cbor_encode(decoded_relation)
    reject_probe(
        "RPP-NEG-RELATION-PAYLOAD-UNKNOWN-FIELD",
        lambda: _candidate_errors(
            unknown_relation_payload, stage=fx["stage"], snapshot_id=fx["snapshotId"],
            relations=fx["relations"], expected_ordinal=0,
            payload_schemas=fx["payloadSchemas"],
        ),
    )

    mismatched_repo = copy.deepcopy(prepared_repo)
    mismatched_repo["buildScriptOutputs"][0]["outputDigest"] = "31" * 32
    reject_probe(
        "RPP-NEG-REPOSITORY-PREPARED-OUTPUT-MISMATCH",
        lambda: _repository_errors(mismatched_repo, prepared_universe),
    )
    return findings, positive, adversarial


def _pin_rows(rows: Any) -> dict[str, str] | None:
    if type(rows) is not list:
        return None
    out: dict[str, str] = {}
    for row in rows:
        if not _closed(row, {"path", "sha256", "selector"}) and not _closed(row, {"path", "sha256", "use"}):
            return None
        if type(row.get("path")) is not str or not _digest(row.get("sha256")) or row["path"] in out:
            return None
        out[row["path"]] = row["sha256"]
    return out


def check_documents(protocol: Any, delivery_join: Any, ri_join: Any,
                    gap_response: Any, deps: dict[str, Any],
                    observed_hashes: dict[str, str], *,
                    enforce_semantic_pins: bool = True,
                    run_runtime: bool = True) -> tuple[list[str], int, int]:
    """Total checker over already parsed values; never trusts producer booleans."""
    findings: list[str] = []
    positive_count = 0
    adversarial_count = 0
    roots = {
        PROTOCOL: protocol,
        DELIVERY_JOIN: delivery_join,
        RI_JOIN: ri_join,
    }
    for name, value in roots.items():
        if type(value) is not dict:
            findings.append(f"RPP-TYPE: {name} root must be an object")
    if findings:
        return findings, positive_count, adversarial_count

    try:
        for name, expected in LOCAL_RAW_HASHES.items():
            if observed_hashes.get(name) != expected:
                findings.append(f"RPP-HASH: {name} exact candidate bytes drifted")
        for name, expected in DEPENDENCY_HASHES.items():
            if observed_hashes.get(name) != expected:
                findings.append(f"RPP-HASH: dependency {name} drifted")
        if enforce_semantic_pins:
            for name, value in roots.items():
                if semantic_hash(value) != LOCAL_SEMANTIC_HASHES[name]:
                    findings.append(f"RPP-SEMANTIC: {name} semantic object drifted")

        if protocol.get("artifact") != "opensip.rust-provider-protocol" or protocol.get("version") != 1:
            findings.append("RPP-META: protocol identity/version drifted")
        if protocol.get("status") != "CANDIDATE-NOT-APPLIED" or protocol.get("reviewStatus") != "AWAITING-INDEPENDENT-REVIEW":
            findings.append("RPP-META: protocol status overclaims application/review")
        authority = protocol.get("authority")
        expected_authority = {
            "architectureContractOnly": True,
            "applied": False,
            "integrationAuthority": "NONE",
            "productAuthority": "NONE",
            "freezeAuthority": "NONE",
            "demonstrationAuthority": "NONE",
            "releaseAuthority": "NONE",
            "independentReviewRequired": True,
            "producerClaimsAreAuthority": False,
        }
        if authority != expected_authority:
            findings.append("RPP-META: protocol authority boundary drifted")
        protocol_pins = _pin_rows(protocol.get("dependencyPins"))
        if protocol_pins != DEPENDENCY_HASHES:
            findings.append("RPP-JOIN: protocol dependency pins are not exact")
        joins = protocol.get("narrowJoinReferences")
        expected_joins = [
            {"path": DELIVERY_JOIN, "artifact": "opensip.delivery-rust-provider-join", "version": 1},
            {"path": RI_JOIN, "artifact": "opensip.resolved-inputs-rust-provider-join", "version": 1},
        ]
        if joins != expected_joins:
            findings.append("RPP-JOIN: narrow join references drifted")

        identity = protocol.get("protocolIdentity")
        if type(identity) is not dict or identity.get("protocolMajor") != 1 or identity.get("providerId") != "rust-semantic" or identity.get("language") != "rust":
            findings.append("RPP-PROTOCOL: identity drifted")
        if type(identity) is not dict or any(identity.get(k) is not False for k in (
            "retransmission", "deduplication", "acknowledgementRetry",
            "residentSession", "typescriptWireInheritance",
        )) or identity.get("oneAnalyzePerChild") is not True:
            findings.append("RPP-PROTOCOL: v1 retry/residency/Analyze law drifted")
        cbor = protocol.get("canonicalCbor")
        if type(cbor) is not dict or cbor.get("standard") != "RFC 8949 core deterministic encoding" or "floating point" not in cbor.get("forbidden", []) or "duplicate map keys" not in cbor.get("forbidden", []) or "length" not in cbor.get("mapOrder", ""):
            findings.append("RPP-CBOR: deterministic profile drifted")
        framing = protocol.get("framing")
        if type(framing) is not dict or framing.get("prefixBytes") != 40 or framing.get("lengthFieldBytes") != 8 or framing.get("digestFieldBytes") != 32 or framing.get("digestRepresentation") != "raw bytes, never hexadecimal text" or framing.get("digestScope") != "SHA-256 of the exact canonical-CBOR payload bytes only" or "payloadLength" not in framing.get("frameBytes", ""):
            findings.append("RPP-FRAME: exact length+raw-digest+payload grammar drifted")
        limits = protocol.get("limits")
        if type(limits) is not dict or {key: limits.get(key) for key in EXPECTED_LIMITS} != EXPECTED_LIMITS or set(limits) != set(EXPECTED_LIMITS) | {"limitRule"} or "before allocation" not in limits.get("limitRule", ""):
            findings.append("RPP-BOUNDS: exact limit set drifted")
        findings.extend(_payload_shape_errors(protocol))
        ordering = protocol.get("orderingAndStateMachine")
        if type(ordering) is not dict or "no retransmission" not in ordering.get("sequenceRule", "") or "zero-exit/EOF" not in ordering.get("normalPhases", []) or len(ordering.get("transitions", [])) != 17 or "first worker analysis output" not in ordering.get("unavailableRule", "") or "Only Cancelled may follow" not in ordering.get("cancelRule", "") or "exit status zero" not in ordering.get("terminalRule", ""):
            findings.append("RPP-FSM: state/sequence/terminal contract drifted")
        atomic = protocol.get("candidateAtomicity")
        if type(atomic) is not dict or atomic.get("authorityBeforeAdmission") != "CANDIDATE_ONLY" or atomic.get("spoolOwner") != "host" or "Unavailable" not in atomic.get("discardAllOn", []) or "BudgetExhausted" not in atomic.get("discardAllOn", []) or "one valid Complete terminal" not in atomic.get("admitOn", []) or "child exits zero within grace" not in atomic.get("admitOn", []):
            findings.append("RPP-ATOMIC: all-or-none spool/admission drifted")
        response_projection = protocol.get("responseProjection")
        if type(response_projection) is not dict or "bijection" not in response_projection.get("coverage", "") or "never mints FACT-ID" not in response_projection.get("candidate", ""):
            findings.append("RPP-RESPONSE: candidate/Coverage projection drifted")
        request_projection = protocol.get("requestProjection")
        if type(request_projection) is not dict or "until HelloAck identity and capabilities are recursively equal" not in request_projection.get("sourceDisclosure", ""):
            findings.append("RPP-REQUEST: source disclosure gate drifted")
        budget_contract = protocol.get("deterministicBudget")
        if type(budget_contract) is not dict or "cannot authorize BudgetExhausted" not in budget_contract.get("milliseconds", ""):
            findings.append("RPP-BUDGET: milliseconds supervisor-only law drifted")
        repo = protocol.get("repositoryExecution")
        if type(repo) is not dict or "host resolved-inputs adapter" not in repo.get("preparedGrant", "") or "cannot execute project code" not in repo.get("semanticChild", ""):
            findings.append("RPP-REPO: repository execution owner/projection drifted")
        d9_join = protocol.get("d9Join")
        if type(d9_join) is not dict or d9_join.get("state") != "CONDITIONAL-NOT-APPLIED" or "fc2c546a" not in d9_join.get("candidate", "") or "88ab60ef" not in d9_join.get("independentReview", "") or "does not integrate" not in d9_join.get("rule", ""):
            findings.append("RPP-D9: conditional-not-applied D9 reference drifted")

        if delivery_join.get("artifact") != "opensip.delivery-rust-provider-join" or delivery_join.get("version") != 1 or delivery_join.get("status") != "CANDIDATE-NOT-APPLIED" or delivery_join.get("reviewStatus") != "AWAITING-INDEPENDENT-REVIEW":
            findings.append("RPP-DL: DELIVERY join metadata drifted")
        dl_pins = _pin_rows(delivery_join.get("dependencyPins"))
        wanted_dl = {
            "delivery.v2.json": DEPENDENCY_HASHES["delivery.v2.json"],
            "d9-exit-contract.v1.13.json": DEPENDENCY_HASHES["d9-exit-contract.v1.13.json"],
            "d9-exit-contract.v1.13.review-independent-prefreeze.json": DEPENDENCY_HASHES["d9-exit-contract.v1.13.review-independent-prefreeze.json"],
        }
        if dl_pins != wanted_dl:
            findings.append("RPP-DL: DELIVERY join dependency pins drifted")
        card = delivery_join.get("processModel", {}).get("workerCardinality")
        expected_key = ["ExecutionId", "SnapshotId", "complete closed resolved-inputs rust-v1 semantic-universe value"]
        if type(card) is not dict or card.get("keyFields") != expected_key or card.get("workersPerDistinctKey") != 1 or any(card.get(k) is not False for k in (
            "multiplexDifferentUniverseValues", "reuseAcrossExecutionIds",
            "reuseAcrossSnapshotIds", "reuseAcrossAttempts", "retainAfterTerminal",
            "residentWorker",
        )) or card.get("shareAcrossRustStagesInSameExactKey") is not True:
            findings.append("RPP-DL: worker cardinality/reuse law drifted")
        process = delivery_join.get("processModel", {})
        if "immediately before" not in process.get("start", "") or "reap every descendant" not in process.get("end", "") or "not a security sandbox" not in process.get("tcbPosture", ""):
            findings.append("RPP-DL: worker start/destruction/TCB law drifted")
        launch = delivery_join.get("launch")
        if type(launch) is not dict or launch.get("commandArray") != [
            "<verified-rust-provider-absolute-path>", "--protocol-stdio-v1",
            "--toolchain-root", "<verified-rust-toolchain-bundle-absolute-root>",
            "--scratch-root", "<host-private-child-scratch-absolute-path>",
        ] or launch.get("environment", {}).get("inheritParent") is not False or launch.get("environment", {}).get("setExactly") != {"LANG": "C", "LC_ALL": "C", "TZ": "UTC"}:
            findings.append("RPP-DL: exact launch/environment drifted")
        if type(launch) is not dict or "no live worktree" not in launch.get("roots", {}).get("snapshot", ""):
            findings.append("RPP-DL: sealed-VFS/no-live-root launch law drifted")
        ownership = delivery_join.get("ownership")
        if type(ownership) is not dict or ownership.get("semanticChildMayWriteDurableState") is not False:
            findings.append("RPP-DL: semantic-child durable-state boundary drifted")
        if delivery_join.get("diagnosticsAndScratchBounds") != {
            "maxStderrBytes": 262144,
            "stderrOverflow": "Capture the first maxStderrBytes, append a host-owned truncation marker outside provider bytes, and continue protocol validation; stderr alone never changes semantic or D9 fate.",
            "maxScratchBytes": 2147483648,
            "scratchOverflow": "Terminate and reap the child, discard candidates and map provider-protocol / PROVIDER.PROTOCOL_VIOLATION.",
            "cancellationGraceMilliseconds": 5000,
            "normalExitGraceMilliseconds": 5000,
        }:
            findings.append("RPP-DL: diagnostics/scratch/grace bounds drifted")
        d9_ref = delivery_join.get("d9Reference")
        if type(d9_ref) is not dict or d9_ref.get("candidateSha256") != DEPENDENCY_HASHES["d9-exit-contract.v1.13.json"] or d9_ref.get("independentReviewSha256") != DEPENDENCY_HASHES["d9-exit-contract.v1.13.review-independent-prefreeze.json"] or d9_ref.get("reviewDecision") != "PASS" or d9_ref.get("reviewCandidateState") != "CANDIDATE-NOT-APPLIED" or d9_ref.get("joinState") != "CONDITIONAL-NOT-APPLIED":
            findings.append("RPP-DL: D9 exact reference/application boundary drifted")
        event_map = delivery_join.get("supervisorEventMap")
        if type(event_map) is not list or len(event_map) != 15 or len({row.get("event") for row in event_map if type(row) is dict}) != 15 or semantic_hash(event_map) != SUPERVISOR_EVENT_SEMANTIC_HASH:
            findings.append("RPP-DL: supervisor event map not exhaustive/unique")
        else:
            combined = " ".join(row.get("d9Projection", "") for row in event_map)
            for token in (
                "provider-unavailable", "COVERAGE.PROVIDER_UNAVAILABLE",
                "budget-exhausted", "COVERAGE.BUDGET_EXHAUSTED",
                "delivery-required", "DELIVERY.REQUIRED_FAILED",
                "provider-protocol", "PROVIDER.PROTOCOL_VIOLATION",
                "interrupted", "exitCode=130",
            ):
                if token not in combined:
                    findings.append(f"RPP-DL: supervisor map omits {token}")

        if ri_join.get("artifact") != "opensip.resolved-inputs-rust-provider-join" or ri_join.get("version") != 1 or ri_join.get("status") != "CANDIDATE-NOT-APPLIED" or ri_join.get("reviewStatus") != "AWAITING-INDEPENDENT-REVIEW":
            findings.append("RPP-RI: RI join metadata drifted")
        ri_pins = _pin_rows(ri_join.get("dependencyPins"))
        wanted_ri = {
            "resolved-inputs.v2.json": DEPENDENCY_HASHES["resolved-inputs.v2.json"],
            "delivery.v2.json": DEPENDENCY_HASHES["delivery.v2.json"],
            "c2-plan-stage-schema.v3.json": DEPENDENCY_HASHES["c2-plan-stage-schema.v3.json"],
        }
        if ri_pins != wanted_ri:
            findings.append("RPP-RI: RI join dependency pins drifted")
        binding = ri_join.get("repositoryExecutionPlanBinding")
        if type(binding) is not dict or binding.get("owner") != "host resolved-inputs adapter" or binding.get("semanticSidecarExecutesRepositoryCode") is not False or binding.get("granted", {}).get("network") is not False or "future result" not in binding.get("why", ""):
            findings.append("RPP-RI: pre-Plan repository owner/cycle rule drifted")
        params = ri_join.get("repositoryExecutionGrantParametersV1")
        expected_param_fields = {"schema-version", "build-scripts", "procedural-macros", "network", "tool-paths"}
        if type(params) is not dict or params.get("closed") is not True or set(params.get("required", [])) != expected_param_fields or params.get("optional") != [] or set(params.get("fields", {})) != expected_param_fields or "field 10" not in params.get("c2Carrier", ""):
            findings.append("RPP-RI: PlanId-bound repository grant schema drifted")
        tool = ri_join.get("toolPathV1")
        if type(tool) is not dict or tool.get("closed") is not True or set(tool.get("required", [])) != TOOL_PATH_FIELDS or tool.get("optional") != [] or set(tool.get("fields", {})) != TOOL_PATH_FIELDS or "does not enter PlanId" not in tool.get("physicalMapping", ""):
            findings.append("RPP-RI: ToolPathV1/physical mapping drifted")
        cap_binding = ri_join.get("capabilityHandshakeBinding")
        if type(cap_binding) is not dict or cap_binding.get("closed") is not True or set(cap_binding.get("required", [])) != CAPABILITY_FIELDS or cap_binding.get("optional") != [] or "exact recursive equality" not in " ".join(cap_binding.get("hostValidationOrder", [])) or "producer boolean" not in cap_binding.get("mismatch", "") or "capabilityManifestId" not in cap_binding.get("planCommitment", "") or "PLAN-ID-V1" not in cap_binding.get("planCommitment", ""):
            findings.append("RPP-RI: capability handshake equality drifted")

        delivery = deps.get("delivery.v2.json")
        ri = deps.get("resolved-inputs.v2.json")
        c2 = deps.get("c2-plan-stage-schema.v3.json")
        fact = deps.get("fact-plane.v1.json")
        d9 = deps.get("d9-exit-contract.v1.13.json")
        review = deps.get("d9-exit-contract.v1.13.review-independent-prefreeze.json")
        if type(delivery) is not dict or delivery.get("rustSemanticSubstrate", {}).get("decision") != "bundled-pinned-rustc-driver-sidecar" or set(delivery.get("rustSemanticSubstrate", {}).get("providerProtocol", {}).get("handshakeRequired", [])) != {"protocolMajor", "providerBuildId", "rustCommitHash", "hostTriple", "targetTriple", "sysrootDigest", "capabilities"}:
            findings.append("RPP-XJOIN: live DELIVERY Rust substrate/handshake drifted")
        rust_schema = ri.get("planIdContract", {}).get("semanticUniverseSchemas", {}).get("rust-v1") if type(ri) is dict else None
        if type(rust_schema) is not dict or rust_schema.get("closed") is not True or set(rust_schema.get("required", [])) != RUST_UNIVERSE_FIELDS:
            findings.append("RPP-XJOIN: live RI rust-v1 schema drifted")
        c2_key_fields = [row.get("field") for row in c2.get("coverageKey", {}).get("key", [])] if type(c2) is dict else []
        if c2_key_fields != ["relation", "resolution", "sourceUniverseId", "targetUniverseId", "subjectScopeCommitment", "producer", "producerVersion", "schemaVersion"]:
            findings.append("RPP-XJOIN: live C-2 CoverageKey drifted")
        candidate_required = fact.get("factRecordContractV1", {}).get("candidateSchema", {}).get("required", []) if type(fact) is dict else []
        if set(candidate_required) != FACT_CANDIDATE_FIELDS:
            findings.append("RPP-XJOIN: live FACT-PLANE candidate schema drifted")
        selected_capability = _selected_rust_capability(delivery) if type(delivery) is dict else None
        if selected_capability is None or _capability_errors(selected_capability, selected_capability):
            findings.append("RPP-XJOIN: signed Rust ProviderCapability row unavailable")
        fault_map = d9.get("codeMaps", {}).get("faultCauseToErrorCode", {}) if type(d9) is dict else {}
        deficiency_map = d9.get("codeMaps", {}).get("deficiencyToReasonCode", {}) if type(d9) is dict else {}
        if fault_map.get("provider-protocol") != "PROVIDER.PROTOCOL_VIOLATION" or fault_map.get("delivery-required") != "DELIVERY.REQUIRED_FAILED" or deficiency_map.get("provider-unavailable") != "COVERAGE.PROVIDER_UNAVAILABLE" or deficiency_map.get("budget-exhausted") != "COVERAGE.BUDGET_EXHAUSTED" or d9.get("classToExitCode", {}).get("interrupted") != 130:
            findings.append("RPP-XJOIN: exact D9 v1.13 provider maps drifted")
        verdict = review.get("verdict", {}) if type(review) is dict else {}
        if verdict.get("decision") != "PASS" or verdict.get("candidateState") != "CANDIDATE-NOT-APPLIED" or verdict.get("blockingFindingCount") != 0 or verdict.get("inputHashDrift") is not False:
            findings.append("RPP-XJOIN: D9 v1.13 independent review boundary drifted")

        if type(gap_response) is not dict:
            findings.append("RPP-GAP: gap-response root missing/malformed")
        else:
            expected_gap_fields = {
                "artifact", "version", "status", "reviewStatus", "purpose",
                "sourceAudit", "authority", "candidateSet", "gapDispositions",
                "typescriptNonInheritance", "retransmission",
                "closureCriterionResponse", "checkerExecutionRecord",
                "hashRecord", "preExistingByteIdentity", "residuals",
                "exactFilesCreated",
            }
            if set(gap_response) != expected_gap_fields:
                findings.append("RPP-GAP: gap-response root is not exact closed shape")
            if gap_response.get("artifact") != "opensip.rust-provider-protocol.adjudication-gap-response" or gap_response.get("status") != "CANDIDATE-NOT-APPLIED" or gap_response.get("reviewStatus") != "AWAITING-INDEPENDENT-REVIEW":
                findings.append("RPP-GAP: gap-response metadata drifted")
            gap_authority = gap_response.get("authority")
            if gap_authority != {
                "producerResponseOnly": True,
                "selfReview": False,
                "independentReviewPerformed": False,
                "applied": False,
                "integrationAuthority": "NONE",
                "productAuthority": "NONE",
                "freezeAuthority": "NONE",
                "demonstrationAuthority": "NONE",
                "releaseAuthority": "NONE",
            }:
                findings.append("RPP-GAP: producer-only/no-review authority boundary drifted")
            dispositions = gap_response.get("gapDispositions")
            expected_gap_ids = {f"RPP-GAP-{i:02d}" for i in range(1, 21)}
            if type(dispositions) is not list or {row.get("id") for row in dispositions if type(row) is dict} != expected_gap_ids or len(dispositions) != 20:
                findings.append("RPP-GAP: not every audit section-5 fork is dispositioned exactly once")
            elif any(row.get("disposition") != "RESOLVED-IN-CANDIDATE-AWAITING-INDEPENDENT-REVIEW" or not row.get("resolvedBy") or not row.get("checkerCoverage") for row in dispositions):
                findings.append("RPP-GAP: one or more dispositions lack candidate owner/checker coverage")
            if gap_response.get("typescriptNonInheritance", {}).get("inherited") is not False or gap_response.get("retransmission", {}).get("v1Allowed") is not False:
                findings.append("RPP-GAP: TypeScript inheritance/retransmission correction drifted")
            expected_candidate_set = [
                PROTOCOL, pathlib.Path(__file__).name, GAP_RESPONSE,
                DELIVERY_JOIN, RI_JOIN,
            ]
            if gap_response.get("candidateSet") != expected_candidate_set:
                findings.append("RPP-GAP: exact five-file candidate set drifted")
            execution = gap_response.get("checkerExecutionRecord")
            if execution != {
                "requiredNormalCommand": "python3 -I -B docs/coop/artifacts/check-rust-provider-protocol.py",
                "requiredSelftestCommand": "python3 -I -B docs/coop/artifacts/check-rust-provider-protocol.py --selftest",
                "normalExit": 0,
                "selftestExit": 0,
                "runtimePositiveCount": 36,
                "runtimeAdversarialCount": 147,
                "mutationProbeCount": 76,
            }:
                findings.append("RPP-GAP: retained checker execution record drifted")
            try:
                checker_sha = sha256_bytes(pathlib.Path(__file__).read_bytes())
            except OSError:
                checker_sha = ""
            hash_record = gap_response.get("hashRecord")
            if hash_record != {
                "protocolSha256": LOCAL_RAW_HASHES[PROTOCOL],
                "deliveryJoinSha256": LOCAL_RAW_HASHES[DELIVERY_JOIN],
                "resolvedInputsJoinSha256": LOCAL_RAW_HASHES[RI_JOIN],
                "checkerSha256": checker_sha,
                "selfHash": "Not embedded; self-referential file hashing is not an authority mechanism.",
            }:
                findings.append("RPP-GAP: exact candidate hash record drifted")
            byte_identity = gap_response.get("preExistingByteIdentity")
            if type(byte_identity) is not dict or byte_identity.get("beforeArtifactFileCount") != 365 or byte_identity.get("beforeAggregateManifestSha256") != "6888c041efb7f2c75daf0bd0bd8b4d94b408369e2f752014160a307441c324b4" or byte_identity.get("afterExcludingFiveNewFiles") != {
                "artifactFileCount": 365,
                "aggregateManifestSha256": "6888c041efb7f2c75daf0bd0bd8b4d94b408369e2f752014160a307441c324b4",
                "matchesBefore": True,
            }:
                findings.append("RPP-GAP: pre-existing artifact byte-identity record drifted")
            expected_created = [f"docs/coop/artifacts/{name}" for name in expected_candidate_set]
            if gap_response.get("exactFilesCreated") != expected_created:
                findings.append("RPP-GAP: exact created-path list drifted")

        if run_runtime:
            runtime_findings, positive_count, adversarial_count = _runtime_oracle_findings(protocol, deps)
            findings.extend(runtime_findings)
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError, OverflowError):
        findings.append("RPP-TYPE: malformed nested candidate/dependency value")
    return findings, positive_count, adversarial_count


def load_all() -> tuple[dict[str, Any] | None, dict[str, str], list[str]]:
    docs: dict[str, Any] = {}
    hashes: dict[str, str] = {}
    findings: list[str] = []
    for name in (PROTOCOL, DELIVERY_JOIN, RI_JOIN):
        value, actual, error = _read_candidate(HERE / name)
        if error:
            findings.append(error)
        else:
            docs[name] = value
            hashes[name] = actual or ""
    gap_value, _, gap_error = _read_candidate(HERE / GAP_RESPONSE)
    if gap_error:
        findings.append(gap_error)
    else:
        docs[GAP_RESPONSE] = gap_value
    for name, expected in DEPENDENCY_HASHES.items():
        value, error = _read_hashed(HERE / name, expected)
        if error:
            findings.append(error)
        else:
            docs[name] = value
            hashes[name] = expected
    return docs if not findings else None, hashes, findings


def _set_path(root: dict[str, Any], path: tuple[Any, ...], value: Any) -> bool:
    try:
        cursor: Any = root
        for part in path[:-1]:
            cursor = cursor[part]
        before = semantic_hash(cursor[path[-1]])
        cursor[path[-1]] = value
        return semantic_hash(cursor[path[-1]]) != before
    except (KeyError, TypeError, IndexError):
        return False


Mutation = tuple[str, str, Callable[[dict[str, Any]], bool]]


def _mutations() -> list[Mutation]:
    p = PROTOCOL
    d = DELIVERY_JOIN
    r = RI_JOIN
    return [
        ("RPP-MUT-001-worker-key", d, lambda x: _set_path(x, ("processModel", "workerCardinality", "keyFields"), ["rust-v1"])),
        ("RPP-MUT-002-worker-count", d, lambda x: _set_path(x, ("processModel", "workerCardinality", "workersPerDistinctKey"), 2)),
        ("RPP-MUT-003-cross-execution-reuse", d, lambda x: _set_path(x, ("processModel", "workerCardinality", "reuseAcrossExecutionIds"), True)),
        ("RPP-MUT-004-cross-snapshot-reuse", d, lambda x: _set_path(x, ("processModel", "workerCardinality", "reuseAcrossSnapshotIds"), True)),
        ("RPP-MUT-005-cross-attempt-reuse", d, lambda x: _set_path(x, ("processModel", "workerCardinality", "reuseAcrossAttempts"), True)),
        ("RPP-MUT-006-resident", d, lambda x: _set_path(x, ("processModel", "workerCardinality", "residentWorker"), True)),
        ("RPP-MUT-007-start-early", d, lambda x: _set_path(x, ("processModel", "start"), "Start during PlanIntent.")),
        ("RPP-MUT-008-no-reap", d, lambda x: _set_path(x, ("processModel", "end"), "Retain child and scratch.")),
        ("RPP-MUT-009-sandbox-claim", d, lambda x: _set_path(x, ("processModel", "tcbPosture"), "Security sandbox.")),
        ("RPP-MUT-010-cbor-profile", p, lambda x: _set_path(x, ("canonicalCbor", "standard"), "implementation-defined")),
        ("RPP-MUT-011-cbor-float", p, lambda x: x["canonicalCbor"]["forbidden"].remove("floating point") is None),
        ("RPP-MUT-012-cbor-map-order", p, lambda x: _set_path(x, ("canonicalCbor", "mapOrder"), "sort source keys")),
        ("RPP-MUT-013-frame-order", p, lambda x: _set_path(x, ("framing", "frameBytes"), "length, payload, digest")),
        ("RPP-MUT-014-digest-text", p, lambda x: _set_path(x, ("framing", "digestRepresentation"), "hex text")),
        ("RPP-MUT-015-digest-scope", p, lambda x: _set_path(x, ("framing", "digestScope"), "whole frame")),
        ("RPP-MUT-016-frame-bound", p, lambda x: _set_path(x, ("limits", "maxFramePayloadBytes"), 0)),
        ("RPP-MUT-017-response-bound", p, lambda x: _set_path(x, ("limits", "maxResponsePayloadBytesTotal"), 0)),
        ("RPP-MUT-018-spool-bound", p, lambda x: _set_path(x, ("limits", "maxCandidateSpoolBytes"), 0)),
        ("RPP-MUT-019-stderr-bound", p, lambda x: _set_path(x, ("limits", "maxStderrBytes"), 0)),
        ("RPP-MUT-020-grace-bound", p, lambda x: _set_path(x, ("limits", "cancellationGraceMilliseconds"), 0)),
        ("RPP-MUT-021-delete-request-frame", p, lambda x: x["wireSchema"]["frameSchemas"].pop("OpenUniverse", None) is not None),
        ("RPP-MUT-022-delete-response-frame", p, lambda x: x["wireSchema"]["frameSchemas"].pop("Coverage", None) is not None),
        ("RPP-MUT-023-open-payload", p, lambda x: _set_path(x, ("wireSchema", "payloadSchemas", "AnalyzeV1", "closed"), False)),
        ("RPP-MUT-024-unknown-optional", p, lambda x: _set_path(x, ("wireSchema", "payloadSchemas", "AnalyzeV1", "optional"), ["extension"])),
        ("RPP-MUT-025-delete-required", p, lambda x: x["wireSchema"]["payloadSchemas"]["OpenUniverseV1"]["required"].remove("universe") is None),
        ("RPP-MUT-026-wrong-direction", p, lambda x: _set_path(x, ("wireSchema", "frameSchemas", "FactBatch", "direction"), "host-to-worker")),
        ("RPP-MUT-027-second-analyze", p, lambda x: _set_path(x, ("protocolIdentity", "oneAnalyzePerChild"), False)),
        ("RPP-MUT-028-sequence-retry", p, lambda x: _set_path(x, ("orderingAndStateMachine", "sequenceRule"), "duplicates are retries")),
        ("RPP-MUT-029-delete-transition", p, lambda x: bool(x["orderingAndStateMachine"]["transitions"].pop())),
        ("RPP-MUT-030-unavailable-after-facts", p, lambda x: _set_path(x, ("orderingAndStateMachine", "unavailableRule"), "Unavailable at any time")),
        ("RPP-MUT-031-terminal-eof", p, lambda x: _set_path(x, ("orderingAndStateMachine", "terminalRule"), "terminal alone succeeds")),
        ("RPP-MUT-032-cancel-any-frame", p, lambda x: _set_path(x, ("orderingAndStateMachine", "cancelRule"), "any response after cancel")),
        ("RPP-MUT-033-retransmission", p, lambda x: _set_path(x, ("protocolIdentity", "retransmission"), True)),
        ("RPP-MUT-034-dedup", p, lambda x: _set_path(x, ("protocolIdentity", "deduplication"), True)),
        ("RPP-MUT-035-typescript-inheritance", p, lambda x: _set_path(x, ("protocolIdentity", "typescriptWireInheritance"), True)),
        ("RPP-MUT-036-candidate-authority", p, lambda x: _set_path(x, ("candidateAtomicity", "authorityBeforeAdmission"), "ADMITTED")),
        ("RPP-MUT-037-provider-spool", p, lambda x: _set_path(x, ("candidateAtomicity", "spoolOwner"), "provider")),
        ("RPP-MUT-038-admit-before-exit", p, lambda x: x["candidateAtomicity"]["admitOn"].remove("child exits zero within grace") is None),
        ("RPP-MUT-039-keep-unavailable-facts", p, lambda x: x["candidateAtomicity"]["discardAllOn"].remove("Unavailable") is None),
        ("RPP-MUT-040-keep-budget-facts", p, lambda x: x["candidateAtomicity"]["discardAllOn"].remove("BudgetExhausted") is None),
        ("RPP-MUT-041-partial-coverage", p, lambda x: _set_path(x, ("responseProjection", "coverage"), "emit only keys with facts")),
        ("RPP-MUT-042-handshake-delete-capabilities", p, lambda x: x["wireSchema"]["payloadSchemas"]["HelloAckV1"]["required"].remove("capabilities") is None),
        ("RPP-MUT-043-capability-presence-only", r, lambda x: _set_path(x, ("capabilityHandshakeBinding", "mismatch"), "field presence is enough")),
        ("RPP-MUT-044-capability-plan-detach", r, lambda x: _set_path(x, ("capabilityHandshakeBinding", "planCommitment"), "not in PlanId")),
        ("RPP-MUT-045-tool-path-open", r, lambda x: _set_path(x, ("toolPathV1", "closed"), False)),
        ("RPP-MUT-046-tool-path-drop-digest", r, lambda x: x["toolPathV1"]["required"].remove("fileSha256") is None),
        ("RPP-MUT-047-tool-path-not-plan", r, lambda x: _set_path(x, ("repositoryExecutionGrantParametersV1", "c2Carrier"), "not PlanId")),
        ("RPP-MUT-048-absolute-path-in-plan", r, lambda x: _set_path(x, ("toolPathV1", "physicalMapping"), "absolute root enters PlanId")),
        ("RPP-MUT-049-sidecar-repo-owner", r, lambda x: _set_path(x, ("repositoryExecutionPlanBinding", "owner"), "semantic sidecar")),
        ("RPP-MUT-050-sidecar-executes-code", r, lambda x: _set_path(x, ("repositoryExecutionPlanBinding", "semanticSidecarExecutesRepositoryCode"), True)),
        ("RPP-MUT-051-network-grant", r, lambda x: _set_path(x, ("repositoryExecutionPlanBinding", "granted", "network"), True)),
        ("RPP-MUT-052-launch-shell", d, lambda x: _set_path(x, ("launch", "commandArray"), ["sh", "-c", "rust-provider"])),
        ("RPP-MUT-053-inherit-env", d, lambda x: _set_path(x, ("launch", "environment", "inheritParent"), True)),
        ("RPP-MUT-054-live-worktree", d, lambda x: _set_path(x, ("launch", "roots", "snapshot"), "live worktree")),
        ("RPP-MUT-055-sidecar-durable", d, lambda x: _set_path(x, ("ownership", "semanticChildMayWriteDurableState"), True)),
        ("RPP-MUT-056-timeout-budget", d, lambda x: _set_path(x, ("supervisorEventMap", 12, "d9Projection"), "deficiency=budget-exhausted")),
        ("RPP-MUT-057-delete-fate", d, lambda x: bool(x["supervisorEventMap"].pop())),
        ("RPP-MUT-058-private-d9-code", d, lambda x: _set_path(x, ("supervisorEventMap", 7, "d9Projection"), "PROVIDER.PRIVATE")),
        ("RPP-MUT-059-d9-silent-apply", d, lambda x: _set_path(x, ("d9Reference", "joinState"), "APPLIED")),
        ("RPP-MUT-060-d9-candidate-hash", d, lambda x: _set_path(x, ("d9Reference", "candidateSha256"), "00" * 32)),
        ("RPP-MUT-061-d9-review-hash", d, lambda x: _set_path(x, ("d9Reference", "independentReviewSha256"), "00" * 32)),
        ("RPP-MUT-062-protocol-status", p, lambda x: _set_path(x, ("status",), "APPLIED")),
        ("RPP-MUT-063-product-authority", p, lambda x: _set_path(x, ("authority", "productAuthority"), "GRANTED")),
        ("RPP-MUT-064-delivery-join-status", d, lambda x: _set_path(x, ("status",), "APPLIED")),
        ("RPP-MUT-065-ri-join-status", r, lambda x: _set_path(x, ("status",), "APPLIED")),
        ("RPP-MUT-066-dependency-pin", p, lambda x: _set_path(x, ("dependencyPins", 0, "sha256"), "00" * 32)),
        ("RPP-MUT-067-provider-id", p, lambda x: _set_path(x, ("protocolIdentity", "providerId"), "rust")),
        ("RPP-MUT-068-budget-milliseconds", p, lambda x: _set_path(x, ("deterministicBudget", "milliseconds"), "worker returns BudgetExhausted")),
        ("RPP-MUT-069-source-before-handshake", p, lambda x: _set_path(x, ("requestProjection", "sourceDisclosure"), "send source before HelloAck")),
        ("RPP-MUT-070-provider-fact-id", p, lambda x: _set_path(x, ("responseProjection", "candidate"), "provider mints FACT-ID")),
    ]


def selftest(base_docs: dict[str, Any], base_hashes: dict[str, str]) -> int:
    deps = {name: base_docs[name] for name in DEPENDENCY_HASHES}
    pre, positive, adversarial = check_documents(
        base_docs[PROTOCOL], base_docs[DELIVERY_JOIN], base_docs[RI_JOIN],
        base_docs[GAP_RESPONSE], deps, base_hashes,
    )
    if pre:
        print(f"REFUSING to self-test: dirty base has {len(pre)} finding(s)")
        for finding in pre[:12]:
            print("  -", finding)
        return 1

    print("Rust provider protocol mutation self-test — every applied mutation must be REJECTED\n")
    escaped = 0
    failure_to_apply = 0
    mutations = _mutations()
    for name, target, mutate in mutations:
        docs = copy.deepcopy(base_docs)
        before = semantic_hash(docs[target])
        applied = False
        try:
            applied = mutate(docs[target]) is True
        except (AttributeError, IndexError, KeyError, TypeError, ValueError):
            applied = False
        after = semantic_hash(docs[target])
        if not applied or before == after:
            failure_to_apply += 1
            escaped += 1
            print(f"  ESCAPE  {name}: mutation failed to apply")
            continue
        found, _, _ = check_documents(
            docs[PROTOCOL], docs[DELIVERY_JOIN], docs[RI_JOIN], docs[GAP_RESPONSE],
            {dep: docs[dep] for dep in DEPENDENCY_HASHES}, base_hashes,
            enforce_semantic_pins=False, run_runtime=False,
        )
        if found:
            print(f"  reject  {name}: {found[0]}")
        else:
            escaped += 1
            print(f"  ESCAPE  {name}: no finding")

    drift_hashes = copy.deepcopy(base_hashes)
    drift_hashes["fact-plane.v1.json"] = "00" * 32
    drift_found, _, _ = check_documents(
        base_docs[PROTOCOL], base_docs[DELIVERY_JOIN], base_docs[RI_JOIN],
        base_docs[GAP_RESPONSE], deps, drift_hashes, run_runtime=False,
    )
    if drift_found:
        print(f"  reject  RPP-MUT-071-dependency-drift: {drift_found[0]}")
    else:
        escaped += 1
        print("  ESCAPE  RPP-MUT-071-dependency-drift: no finding")

    dirty = copy.deepcopy(base_docs[PROTOCOL])
    dirty["status"] = "DIRTY"
    dirty_found, _, _ = check_documents(
        dirty, base_docs[DELIVERY_JOIN], base_docs[RI_JOIN], base_docs[GAP_RESPONSE],
        deps, base_hashes, enforce_semantic_pins=False, run_runtime=False,
    )
    if dirty_found:
        print(f"  reject  RPP-MUT-072-dirty-base-probe: {dirty_found[0]}")
    else:
        escaped += 1
        print("  ESCAPE  RPP-MUT-072-dirty-base-probe: no finding")

    for label, hostile in (("string", "x"), ("null", None), ("array", []), ("integer", 1)):
        found, _, _ = check_documents(
            hostile, base_docs[DELIVERY_JOIN], base_docs[RI_JOIN],
            base_docs[GAP_RESPONSE], deps, base_hashes, run_runtime=False,
        )
        if found:
            print(f"  reject  RPP-HOSTILE-ROOT-{label}: {found[0]}")
        else:
            escaped += 1
            print(f"  ESCAPE  RPP-HOSTILE-ROOT-{label}: no finding")

    # Harness probe: a no-op is deliberately classified as an escape. It is not
    # part of the candidate mutation count and must not be silently accepted.
    noop_doc = copy.deepcopy(base_docs[PROTOCOL])
    noop_before = semantic_hash(noop_doc)
    noop_applied = _set_path(noop_doc, ("status",), noop_doc["status"])
    if noop_applied or semantic_hash(noop_doc) != noop_before:
        escaped += 1
        print("  ESCAPE  RPP-HARNESS-NOOP: failure-to-apply detector is broken")
    else:
        print("  reject  RPP-HARNESS-NOOP: mutation failure-to-apply counted as escape")

    print()
    total = len(mutations) + 2 + 4
    if escaped:
        print(
            f"{escaped}/{total} semantic mutations/probes ESCAPED; "
            f"failure-to-apply={failure_to_apply}; runtime positive={positive}; "
            f"runtime adversarial={adversarial}"
        )
        return 1
    print(
        f"all {total} semantic mutations/probes rejected; "
        f"failure-to-apply={failure_to_apply}; runtime positive={positive}; "
        f"runtime adversarial={adversarial}"
    )
    return 0


def main() -> int:
    if not sys.flags.isolated or not sys.dont_write_bytecode:
        print("RPP-ISOLATION: invoke only with python3 -I -B", file=sys.stderr)
        return 2
    docs, hashes, load_findings = load_all()
    if load_findings or docs is None:
        for finding in load_findings:
            print(finding)
        return 2
    if "--selftest" in sys.argv[1:]:
        if sys.argv[1:] != ["--selftest"]:
            print("usage: check-rust-provider-protocol.py [--selftest]", file=sys.stderr)
            return 2
        return selftest(docs, hashes)
    if sys.argv[1:]:
        print("usage: check-rust-provider-protocol.py [--selftest]", file=sys.stderr)
        return 2
    deps = {name: docs[name] for name in DEPENDENCY_HASHES}
    findings, positive, adversarial = check_documents(
        docs[PROTOCOL], docs[DELIVERY_JOIN], docs[RI_JOIN], docs[GAP_RESPONSE],
        deps, hashes,
    )
    if findings:
        print(f"{len(findings)} Rust provider protocol finding(s):")
        for finding in findings:
            print("  -", finding)
        return 1
    print(
        "rust provider protocol candidate clean — exact protocol + DELIVERY join + "
        "RI join; CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW"
    )
    print(
        f"  runtime corpus: {positive} positive, {adversarial} adversarial; "
        f"frames={len(EXPECTED_FRAMES)}, supervisor fates=15"
    )
    print("  D9 v1.13 reference: independently pre-freeze reviewed, conditional/not applied")
    print("  authority: no product, integration, freeze, demonstrated or release authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
