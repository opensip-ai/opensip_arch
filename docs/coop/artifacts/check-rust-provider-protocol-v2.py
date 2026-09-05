#!/usr/bin/env python3
"""Retained checker for the Rust semantic-provider protocol v2 candidate.

Supported invocations:
  python3 -I -B docs/coop/artifacts/check-rust-provider-protocol-v2.py
  python3 -I -B docs/coop/artifacts/check-rust-provider-protocol-v2.py --selftest

This checker imports no producer checker and treats no producer fixture as an
oracle. It hashes immutable inputs before semantic use, uses fixed independent
fixtures, and refuses mutation testing unless the exact clean candidate passes.
"""
from __future__ import annotations

import sys

if sys.flags.isolated != 1 or not sys.dont_write_bytecode:
    print("RPPV2-UNSUPPORTED-INVOCATION: require python3 -I -B", file=sys.stderr)
    raise SystemExit(2)

import ast
import copy
import hashlib
import itertools
import json
import pathlib
import re
import subprocess
import unicodedata
from decimal import Decimal
from typing import Any, Callable


HERE = pathlib.Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
PROTOCOL = "rust-provider-protocol.v2.json"
DELIVERY_JOIN = "delivery-rust-provider-join.v2.json"
RI_JOIN = "resolved-inputs-rust-provider-join.v2.json"
RESPONSE = "rust-provider-protocol.v2.adjudication-v1-rejection-response.json"
CHECKER = "check-rust-provider-protocol-v2.py"
NEW_FILES = {
    f"docs/coop/artifacts/{PROTOCOL}",
    f"docs/coop/artifacts/{DELIVERY_JOIN}",
    f"docs/coop/artifacts/{RI_JOIN}",
    f"docs/coop/artifacts/{RESPONSE}",
    f"docs/coop/artifacts/{CHECKER}",
}
CONCURRENT_NONCANDIDATE_FILES = {
    "docs/coop/artifacts/check-r1-v1.5.py",
    "docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.5.adjudication-rust-realization.json",
    "docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.5.json",
}

DEPENDENCY_HASHES = {
    "delivery.v2.json": "47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3",
    "resolved-inputs.v2.json": "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    "c2-plan-stage-schema.v3.json": "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285",
    "fact-plane.v1.json": "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
    "d9-exit-contract.v1.13.json": "fc2c546a4cdbe2038f3a5db333ab9903d21ae9d6223777b139b58551fb2f2fae",
    "d9-exit-contract.v1.13.review-independent-prefreeze.json":
        "88ab60efb21f603213ebff722f62f310b422f03981895e3f6779f2febe734c5b",
}
FROZEN_V1_HASHES = {
    "rust-provider-protocol.v1.json": "8c749eb7942a80cee3da2e304328addce4dac42e20a084b4ce26bcf31da51796",
    "check-rust-provider-protocol.py": "c190ee7f62552ec342f5da1f66ba2b840cdffd5cd5cddb25e5987c315ee1502e",
    "rust-provider-protocol.v1.adjudication-gap-response.json":
        "6da46e9160287cecd57e4ea6e9b5ea6fb7c3fb8b65708732f40c45ada2214891",
    "delivery-rust-provider-join.v1.json": "42eb9788132aee6d436123881bbd2e82db0da4f223bd13de16c26410fb3e5558",
    "resolved-inputs-rust-provider-join.v1.json":
        "b85017567f2f31589b17d9cd130aeb55b58700844f431cb7baa650a4f255d707",
    "rust-provider-protocol.v1.review-independent-prefreeze.json":
        "566dc23e6b774a5c8141a45ab4563579d3a2e5a1d0427cb29d7cdaca16ca6a69",
}

# Replaced after the three mutually joined JSON artifacts reach stable bytes.
LOCAL_RAW_HASHES = {
    PROTOCOL: "6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b",
    DELIVERY_JOIN: "12dd96eddaf99ba9b6efafa05fe11791685065b225fd602b4b5a9692345dfa1e",
    RI_JOIN: "435ec9cdd45a85255df0c099238bd0a3e1c10e88960716cd84649030d6482d47",
}

EXPECTED_LIMITS = {
    "maxFramePayloadBytes": 67108864,
    "maxSnapshotChunkBytes": 1048576,
    "maxSnapshotEntries": 200000,
    "maxSnapshotTotalFileBytes": 8589934592,
    "maxPreparedOutputChunkBytes": 1048576,
    "maxPreparedOutputEntries": 256,
    "maxPreparedOutputTotalBlobBytes": 1073741824,
    "maxAnalyzeStages": 256,
    "maxRelationsPerStage": 64,
    "maxSubjectsPerStage": 256,
    "maxRequestedCoverageKeysPerStage": 256,
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
EXPECTED_FRAMES = {
    "Hello": ("host-to-worker", "HelloV2", False),
    "HelloAck": ("worker-to-host", "HelloAckV2", False),
    "OpenUniverse": ("host-to-worker", "OpenUniverseV2", False),
    "UniverseAccepted": ("worker-to-host", "UniverseAcceptedV2", False),
    "SnapshotManifest": ("host-to-worker", "SnapshotManifestV2", False),
    "SnapshotFileChunk": ("host-to-worker", "SnapshotFileChunkV2", False),
    "SnapshotSeal": ("host-to-worker", "SnapshotSealV2", False),
    "SnapshotAccepted": ("worker-to-host", "SnapshotAcceptedV2", False),
    "PreparedOutputManifest": ("host-to-worker", "PreparedOutputManifestV2", False),
    "PreparedOutputChunk": ("host-to-worker", "PreparedOutputChunkV2", False),
    "PreparedOutputSeal": ("host-to-worker", "PreparedOutputSealV2", False),
    "PreparedOutputAccepted": ("worker-to-host", "PreparedOutputAcceptedV2", False),
    "Analyze": ("host-to-worker", "AnalyzeV2", False),
    "FactBatch": ("worker-to-host", "FactBatchV2", False),
    "Coverage": ("worker-to-host", "CoverageV2", False),
    "Unavailable": ("worker-to-host", "UnavailableV2", True),
    "BudgetExhausted": ("worker-to-host", "BudgetExhaustedV2", True),
    "Complete": ("worker-to-host", "CompleteV2", True),
    "ProviderFault": ("worker-to-host", "ProviderFaultV2", True),
    "Cancel": ("host-to-worker", "CancelV2", False),
    "Cancelled": ("worker-to-host", "CancelledV2", True),
}
PHASES = [
    "START", "WAIT_HELLO_ACK", "READY_OPEN_UNIVERSE", "WAIT_UNIVERSE_ACCEPTED",
    "READY_SNAPSHOT_MANIFEST", "RECEIVING_SNAPSHOT", "WAIT_SNAPSHOT_ACCEPTED",
    "READY_PREPARED_MANIFEST", "RECEIVING_PREPARED", "WAIT_PREPARED_ACCEPTED",
    "READY_ANALYZE", "ANALYZING", "READY_COMPLETE", "WAIT_CANCELLED",
    "WAIT_ZERO_EXIT", "WAIT_EOF", "DONE", "FAULT",
]
PROVIDER_FAULT_PHASES = PHASES[1:13]
CANCEL_PHASES = PHASES[:13]
BOOL_OBSERVATIONS = [
    "userInterruptBeforeFinalization", "deliveryFailure", "postTerminalBytes",
    "malformedFrame", "schemaOrCommitmentFault", "handshakeMismatch",
    "deadlineHang", "nonzeroExit", "earlyEof", "coverageObserved", "hostCancelSent",
]
TERMINAL_KINDS = ["none", "complete", "unavailable", "budget-exhausted", "provider-fault", "cancelled"]
REDUCER_ROWS = [
    (1, "userInterruptBeforeFinalization=true", "USER_INTERRUPTED"),
    (2, "deliveryFailure=true", "DELIVERY_REQUIRED_FAILURE"),
    (3, "postTerminalBytes=true", "POST_TERMINAL_OUTPUT"),
    (4, "malformedFrame=true", "MALFORMED_FRAME"),
    (5, "schemaOrCommitmentFault=true", "SCHEMA_OR_COMMITMENT_FAULT"),
    (6, "handshakeMismatch=true", "HANDSHAKE_MISMATCH"),
    (7, "deadlineHang=true", "DEADLINE_HANG"),
    (8, "nonzeroExit=true", "NONZERO_EXIT"),
    (9, "earlyEof=true", "EARLY_EOF"),
    (10, "terminalKind=cancelled and hostCancelSent=false", "UNSOLICITED_CANCELLED"),
    (11, "terminalKind=provider-fault", "PROVIDER_DECLARED_FAULT"),
    (12, "terminalKind=complete", "VERIFIED_COMPLETE"),
    (13, "terminalKind=unavailable", "VERIFIED_UNAVAILABLE"),
    (14, "terminalKind=budget-exhausted", "VERIFIED_BUDGET_EXHAUSTED"),
    (15, "terminalKind=cancelled and hostCancelSent=true", "VERIFIED_CANCELLED"),
    (16, "true", "INCOMPLETE_PROTOCOL"),
]
TOOL_FIELDS = {"artifact_id", "bundle_relative_path", "file_sha256", "role"}
PARAM_FIELDS = {"schema_version", "build_scripts", "procedural_macros", "network", "tool_paths"}
COVERAGE_FIELDS = {
    "relation", "resolution", "sourceUniverseId", "targetUniverseId",
    "subjectScopeCommitment", "producer", "producerVersion", "schemaVersion",
}
SUBJECT_FIELDS = {"subjectOrdinal", "subjectId", "path", "startByte", "endByte"}
IDENT_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

EXPECTED_PREEXISTING_COUNT = 371
EXPECTED_PREEXISTING_AGGREGATE = "a4fbc23f61e395ee124cf4421810d6099252e29e9eed1347ee17887cc4ea809a"
EXPECTED_PREEXISTING_SOURCE_COUNT = 339
EXPECTED_PREEXISTING_SOURCE_AGGREGATE = "62059d537b03941befd615c4e651809ae0b640226b43473499af22d0518aafcf"
EXPECTED_RECORDED_POSITIVE = 263
EXPECTED_RECORDED_ADVERSARIAL = 68
EXPECTED_RECORDED_MUTATIONS = 42
EXPECTED_RECORDED_STATE_TRACES = 78

# No local source is imported. If that changes, the file must be listed here,
# read as bytes, hash-checked, compiled with dont_inherit, and only then exec'd.
LOCAL_EXEC_SOURCES: dict[str, str] = {}


class StrictJsonError(ValueError):
    pass


class CheckReport:
    def __init__(self) -> None:
        self.positive = 0
        self.adversarial = 0
        self.failures: list[str] = []

    def expect(self, condition: bool, label: str) -> None:
        self.positive += 1
        if not condition:
            self.failures.append(label)

    def reject(self, thunk: Callable[[], Any], label: str) -> None:
        self.adversarial += 1
        try:
            result = thunk()
        except Exception:
            return
        if result is not False:
            self.failures.append(label)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise StrictJsonError("duplicate key")
        out[key] = value
    return out


def _constant(value: str) -> None:
    raise StrictJsonError(f"nonfinite {value}")


def _float(value: str) -> None:
    raise StrictJsonError(f"float {value}")


def strict_candidate_loads(text: str) -> Any:
    return json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant, parse_float=_float)


def strict_dependency_loads(text: str) -> Any:
    return json.loads(
        text, object_pairs_hook=_pairs, parse_constant=_constant,
        parse_float=lambda value: Decimal(value),
    )


def assert_candidate_value(value: Any, depth: int = 0) -> None:
    if depth > 128:
        raise StrictJsonError("candidate nesting")
    if value is None or type(value) in {bool, int, str}:
        return
    if type(value) is list:
        for item in value:
            assert_candidate_value(item, depth + 1)
        return
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise StrictJsonError("non-string key")
            assert_candidate_value(item, depth + 1)
        return
    raise StrictJsonError(f"forbidden candidate type {type(value).__name__}")


def read_hashed_json(name: str, expected: str, dependency: bool) -> tuple[Any, bytes]:
    raw = (HERE / name).read_bytes()
    actual = sha256(raw)
    if actual != expected:
        raise StrictJsonError(f"hash {name}: expected {expected}, got {actual}")
    loader = strict_dependency_loads if dependency else strict_candidate_loads
    value = loader(raw.decode("utf-8"))
    if not dependency:
        assert_candidate_value(value)
    return value, raw


def read_candidate_unpinned(name: str) -> tuple[Any, bytes]:
    raw = (HERE / name).read_bytes()
    value = strict_candidate_loads(raw.decode("utf-8"))
    assert_candidate_value(value)
    return value, raw


def load_pinned_local_source(name: str) -> dict[str, Any]:
    expected = LOCAL_EXEC_SOURCES.get(name)
    if expected is None:
        raise StrictJsonError("unlisted local source")
    raw = (HERE / name).read_bytes()
    if sha256(raw) != expected:
        raise StrictJsonError("local source hash")
    namespace: dict[str, Any] = {}
    exec(compile(raw, str(HERE / name), "exec", dont_inherit=True), namespace)
    return namespace


def import_custody_errors() -> list[str]:
    errors: list[str] = []
    raw = (HERE / CHECKER).read_bytes()
    tree = ast.parse(raw, filename=CHECKER)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                errors.append("relative import")
                continue
            names = [(node.module or "").split(".")[0]]
        else:
            continue
        for name in names:
            if name != "__future__" and name not in sys.stdlib_module_names:
                errors.append(f"non-stdlib import {name}")
    if LOCAL_EXEC_SOURCES:
        errors.append("unexpected local exec source")
    return errors


def _u64(value: Any) -> bool:
    return type(value) is int and 0 <= value <= 0xFFFFFFFFFFFFFFFF


def _i64(value: Any) -> bool:
    return type(value) is int and -(1 << 63) <= value <= (1 << 63) - 1


def _nfc(value: Any, max_bytes: int = 4096, nonempty: bool = True) -> bool:
    return (
        type(value) is str and (bool(value) or not nonempty)
        and unicodedata.normalize("NFC", value) == value
        and len(value.encode("utf-8")) <= max_bytes
    )


def _path(value: Any) -> bool:
    if not _nfc(value) or value.startswith("/") or "\\" in value or "\x00" in value:
        return False
    if re.match(r"^[A-Za-z]:", value):
        return False
    return all(part not in {"", ".", ".."} for part in value.split("/"))


def _closed(value: Any, fields: set[str]) -> bool:
    return type(value) is dict and set(value) == fields


def _head(major: int, value: int) -> bytes:
    if not _u64(value):
        raise ValueError("CBOR uint")
    if value < 24:
        return bytes([(major << 5) | value])
    if value <= 0xFF:
        return bytes([(major << 5) | 24, value])
    if value <= 0xFFFF:
        return bytes([(major << 5) | 25]) + value.to_bytes(2, "big")
    if value <= 0xFFFFFFFF:
        return bytes([(major << 5) | 26]) + value.to_bytes(4, "big")
    return bytes([(major << 5) | 27]) + value.to_bytes(8, "big")


def cbor_encode(value: Any, depth: int = 0) -> bytes:
    if depth > 64:
        raise ValueError("CBOR depth/cycle")
    if value is None:
        return b"\xf6"
    if value is False:
        return b"\xf4"
    if value is True:
        return b"\xf5"
    if type(value) is int:
        return _head(0, value)
    if type(value) is bytes:
        return _head(2, len(value)) + value
    if type(value) is str:
        if unicodedata.normalize("NFC", value) != value:
            raise ValueError("CBOR NFC")
        raw = value.encode("utf-8")
        return _head(3, len(raw)) + raw
    if type(value) is list:
        return _head(4, len(value)) + b"".join(cbor_encode(v, depth + 1) for v in value)
    if type(value) is dict:
        encoded: list[tuple[bytes, bytes]] = []
        for key, item in value.items():
            if type(key) is not str:
                raise ValueError("CBOR map key")
            ek = cbor_encode(key, depth + 1)
            encoded.append((ek, cbor_encode(item, depth + 1)))
        encoded.sort(key=lambda pair: (len(pair[0]), pair[0]))
        return _head(5, len(encoded)) + b"".join(k + v for k, v in encoded)
    raise ValueError("CBOR type")


def cbor_decode(data: bytes) -> Any:
    def argument(ai: int, pos: int) -> tuple[int, int]:
        if ai < 24:
            return ai, pos
        sizes = {24: 1, 25: 2, 26: 4, 27: 8}
        if ai not in sizes or pos + sizes[ai] > len(data):
            raise ValueError("CBOR argument")
        size = sizes[ai]
        value = int.from_bytes(data[pos:pos + size], "big")
        if (size == 1 and value < 24) or (size == 2 and value <= 0xFF) or (size == 4 and value <= 0xFFFF) or (size == 8 and value <= 0xFFFFFFFF):
            raise ValueError("CBOR non-shortest")
        return value, pos + size

    def parse(pos: int, depth: int) -> tuple[Any, int]:
        if depth > 64 or pos >= len(data):
            raise ValueError("CBOR truncation")
        initial = data[pos]
        pos += 1
        major, ai = initial >> 5, initial & 31
        if major == 7:
            if ai == 20:
                return False, pos
            if ai == 21:
                return True, pos
            if ai == 22:
                return None, pos
            raise ValueError("CBOR simple/float")
        value, pos = argument(ai, pos)
        if major == 0:
            return value, pos
        if major == 2:
            end = pos + value
            if end > len(data):
                raise ValueError("CBOR bytes")
            return data[pos:end], end
        if major == 3:
            end = pos + value
            if end > len(data):
                raise ValueError("CBOR text")
            text = data[pos:end].decode("utf-8")
            if unicodedata.normalize("NFC", text) != text:
                raise ValueError("CBOR NFC")
            return text, end
        if major == 4:
            out: list[Any] = []
            for _ in range(value):
                item, pos = parse(pos, depth + 1)
                out.append(item)
            return out, pos
        if major == 5:
            out_map: dict[str, Any] = {}
            previous: tuple[int, bytes] | None = None
            for _ in range(value):
                key_start = pos
                key, pos = parse(pos, depth + 1)
                key_raw = data[key_start:pos]
                order = (len(key_raw), key_raw)
                if type(key) is not str or key in out_map or (previous is not None and order <= previous):
                    raise ValueError("CBOR map")
                previous = order
                item, pos = parse(pos, depth + 1)
                out_map[key] = item
            return out_map, pos
        raise ValueError("CBOR major")

    value, end = parse(0, 0)
    if end != len(data) or cbor_encode(value) != data:
        raise ValueError("CBOR trailing/noncanonical")
    return value


def frame_encode(envelope: dict[str, Any]) -> bytes:
    payload = cbor_encode(envelope)
    return len(payload).to_bytes(8, "big") + hashlib.sha256(payload).digest() + payload


def frame_decode(raw: bytes, bound: int) -> dict[str, Any]:
    if len(raw) < 8:
        raise ValueError("frame prefix")
    length = int.from_bytes(raw[:8], "big")
    if length > bound:
        raise ValueError("frame oversize before allocation")
    if len(raw) != 40 + length:
        raise ValueError("frame length")
    payload = raw[40:]
    if hashlib.sha256(payload).digest() != raw[8:40]:
        raise ValueError("frame digest")
    value = cbor_decode(payload)
    if type(value) is not dict:
        raise ValueError("frame envelope")
    return value


def bounded_parameter_errors(value: Any) -> list[str]:
    errors: list[str] = []

    def walk(item: Any, depth: int) -> None:
        if depth > 8:
            errors.append("depth")
            return
        if item is None or type(item) is bool:
            return
        if type(item) is int:
            if not _i64(item):
                errors.append("integer")
            return
        if type(item) is str:
            if not _nfc(item, 4096, False):
                errors.append("string")
            return
        if type(item) is list:
            if len(item) > 256:
                errors.append("array")
            for child in item:
                walk(child, depth + 1)
            return
        if type(item) is dict:
            if len(item) > 64:
                errors.append("map")
            keys = list(item)
            if keys != sorted(keys, key=lambda key: key.encode("utf-8") if type(key) is str else b""):
                errors.append("map order")
            for key, child in item.items():
                if type(key) is not str or len(key.encode("utf-8")) > 128 or IDENT_RE.fullmatch(key) is None:
                    errors.append("key")
                walk(child, depth + 1)
            return
        errors.append("type")

    walk(value, 0)
    try:
        canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
        if len(canonical) > 65536:
            errors.append("total")
    except (TypeError, ValueError):
        errors.append("canonical")
    return errors


def repository_parameter_errors(value: Any) -> list[str]:
    errors = bounded_parameter_errors(value)
    if not _closed(value, PARAM_FIELDS):
        return errors + ["parameter fields"]
    if value["schema_version"] != 2 or type(value["build_scripts"]) is not bool or type(value["procedural_macros"]) is not bool or value["network"] is not False:
        errors.append("parameter scalar")
    tools = value["tool_paths"]
    if type(tools) is not list:
        return errors + ["tools type"]
    expected_order: list[tuple[bytes, bytes]] = []
    for tool in tools:
        if not _closed(tool, TOOL_FIELDS):
            errors.append("tool fields")
            continue
        if tool["artifact_id"] != "rust-toolchain-bundle" or not _path(tool["bundle_relative_path"]):
            errors.append("tool path")
        if type(tool["file_sha256"]) is not str or DIGEST_RE.fullmatch(tool["file_sha256"]) is None:
            errors.append("tool digest")
        if tool["role"] not in {"cargo", "rustc", "linker", "proc-macro-host", "dynamic-loader"}:
            errors.append("tool role")
        expected_order.append((tool["role"].encode(), tool["bundle_relative_path"].encode()))
    if expected_order != sorted(expected_order) or len(expected_order) != len(set(expected_order)):
        errors.append("tool order")
    enabled = value["build_scripts"] or value["procedural_macros"]
    if bool(tools) != enabled:
        errors.append("tool enabledness")
    return errors


def _document_errors(docs: dict[str, Any]) -> list[str]:
    p, d, r, a = docs[PROTOCOL], docs[DELIVERY_JOIN], docs[RI_JOIN], docs[RESPONSE]
    errors: list[str] = []

    def need(condition: bool, label: str) -> None:
        if not condition:
            errors.append(label)

    for value, artifact, version in [
        (p, "opensip.rust-provider-protocol", 2),
        (d, "opensip.delivery-rust-provider-join", 2),
        (r, "opensip.resolved-inputs-rust-provider-join", 2),
        (a, "opensip.rust-provider-protocol.adjudication-v1-rejection-response", 2),
    ]:
        need(type(value) is dict and value.get("artifact") == artifact and value.get("version") == version, f"identity {artifact}")
        need(value.get("status") == "CANDIDATE-NOT-APPLIED" and value.get("reviewStatus") == "AWAITING-INDEPENDENT-REVIEW", f"status {artifact}")
        authority = value.get("authority", {})
        need(authority.get("selfReview") is False and authority.get("independentReviewPerformed") is False, f"review authority {artifact}")
        for key in ["integrationAuthority", "productAuthority", "freezeAuthority", "demonstrationAuthority", "releaseAuthority"]:
            need(authority.get(key) == "NONE", f"authority {artifact} {key}")

    need(p.get("limits") == EXPECTED_LIMITS, "limits exact")
    limit_def = p.get("wireSchema", {}).get("definitions", {}).get("ProtocolLimitsV2", {})
    need(limit_def.get("closed") is True and set(limit_def.get("required", [])) == set(EXPECTED_LIMITS) and limit_def.get("optional") == [], "limit schema")
    need("24 required uint64" in p.get("limitsHandshake", {}).get("numericProjection", ""), "limit count prose")
    need(set(p.get("limitPolicy", {}).get("required", [])) == {"policyId", "comparison", "arithmetic", "allocation", "candidateSpoolAccounting", "aggregateAccounting", "semanticBudgetSeparation"}, "limit policy closed")
    need(set(p["limits"]).isdisjoint({"limitRule", "policyId", "candidateSpoolAccounting"}), "numeric policy separation")
    spool = p.get("limitPolicy", {}).get("candidateSpoolAccounting", {})
    need("analysisOrdinal,stageId,candidate" in spool.get("entryShape", "") and len(spool.get("excludedBytes", [])) == 6, "spool exact accounting")

    actual_frames = {
        key: (row.get("direction"), row.get("payloadType"), row.get("workerTerminal"))
        for key, row in p.get("wireSchema", {}).get("frameSchemas", {}).items()
    }
    need(actual_frames == EXPECTED_FRAMES, "frame vocabulary")
    need(p.get("protocolIdentity", {}).get("protocolMajor") == 2 and p["protocolIdentity"].get("typescriptWireInheritance") is False, "protocol identity")
    need(p["protocolIdentity"].get("retransmission") is False and p["protocolIdentity"].get("deduplication") is False, "no retry")
    payloads = p.get("wireSchema", {}).get("payloadSchemas", {})
    need(set(payloads) == {v[1] for v in EXPECTED_FRAMES.values()}, "payload vocabulary")
    for name, schema in payloads.items():
        need(schema.get("closed") is True and schema.get("optional") == [] and type(schema.get("required")) is list and bool(schema["required"]), f"closed payload {name}")
    defs = p.get("wireSchema", {}).get("definitions", {})
    need(defs.get("ToolPathV2", {}).get("required") == ["artifact_id", "bundle_relative_path", "file_sha256", "role"], "wire tool fields")
    need(defs.get("PreparedOutputBlobV2", {}).get("required") == ["kind", "ownerId", "configuration", "content"], "blob fields")
    need(defs.get("PreparedOutputEntryV2", {}).get("required") == ["outputOrdinal", "kind", "planRow", "logicalPath", "blobByteLength", "blobSha256", "contentByteLength", "contentSha256"], "manifest entry fields")
    need(defs.get("StageRequestV2", {}).get("required") == ["stageOrdinal", "planStage", "analysisDomain"], "stage wrapper")
    need(defs.get("C2PlanStageV3", {}).get("recursiveValidationRequired") is True, "C2 recursive stage")

    machine = p.get("orderingAndStateMachine", {})
    need(machine.get("model") == "closed parametric deterministic transition system", "machine model")
    need(machine.get("stateRecord", {}).get("phaseValues") == PHASES, "machine phases")
    need(machine.get("providerFaultPermittedPhases") == PROVIDER_FAULT_PHASES, "fault phases")
    need(machine.get("cancelPermittedPhases") == CANCEL_PHASES, "cancel phases")
    need(machine.get("initialState") == initial_state(), "initial state")
    need(not any("ANY" in phase or "*" in phase or "ALIAS" in phase for phase in machine.get("stateRecord", {}).get("phaseValues", [])), "no pseudo phases")
    event_record = machine.get("eventRecord", {})
    need(event_record.get("kindValues") == ["frame", "zero-exit", "nonzero-exit", "signal-death", "eof", "deadline", "stdout-byte"], "event kinds")
    need(event_record.get("frameTypeValues") == list(EXPECTED_FRAMES) + ["UNKNOWN_FRAME"], "event frame types")
    transition_ast = machine.get("transitionAstV2", {})
    rules = transition_ast.get("rules", [])
    need([row.get("priority") for row in rules] == list(range(1, 29)), "AST priorities")
    need([row.get("id") for row in rules] == [f"T{i:03d}-" + row.get("id", "").split("-", 1)[1] for i, row in enumerate(rules, 1)], "AST ids")
    need(all(type(row.get("guard")) is dict and type(row.get("actions")) is list and type(row.get("phaseIn")) is list and type(row.get("event")) is dict for row in rules), "AST structured rules")
    need(transition_ast.get("guardGrammar", {}).get("operators") == ["true", "all", "eq", "neq", "lt", "between", "in", "phaseIn", "eventKindIn", "checkedAddCompare", "directionMatchesFrameSchema", "sequenceEqualsDirectionCounter", "directionCounterLessThan"], "guard grammar")
    need(transition_ast.get("actionGrammar", {}).get("operators") == ["set", "copy", "checkedAdd", "checkedIncrementDirectionCounter"], "action grammar")
    analyze_rule = next((row for row in rules if row.get("id") == "T015-ANALYZE"), {})
    need(analyze_rule.get("guard") == {"op": "between", "value": "event.stageCount", "minimum": 1, "maximumRef": "limits.maxAnalyzeStages"}, "Analyze nonempty guard")
    need({"op": "copy", "field": "stageCount", "from": "event.stageCount"} in analyze_rule.get("actions", []), "Analyze exact stageCount assignment")
    unavailable_rule = next((row for row in rules if row.get("id") == "T019-UNAVAILABLE"), {})
    need(unavailable_rule.get("guard", {}).get("op") == "all" and {"op": "eq", "left": "state.outputSeen", "right": {"const": False}} in unavailable_rule.get("guard", {}).get("items", []), "Unavailable AST predicate")
    fallback = rules[-1] if rules else {}
    need(fallback.get("id") == "T028-TOTAL-FALLBACK" and fallback.get("phaseIn") == PHASES[:-1] and fallback.get("event", {}).get("kindIn") == event_record.get("kindValues"), "total AST fallback")
    model_domain = machine.get("modelCheckDomain", {})
    need(model_domain.get("preparedModeValues") == [False, True] and model_domain.get("stageCountValues") == [1, 2, 3] and model_domain.get("factBatchCountPerStageValues") == [0, 1, 2], "model domain")
    need(model_domain.get("requireIndependentAstInterpreter") is True and model_domain.get("requireIndependentReferenceModel") is True, "dual model requirement")

    domain = p.get("planAndDomainProjection", {})
    need("byte-for-byte" in domain.get("planStageByteRule", ""), "plan stage bytes")
    need(len(domain.get("subjectsAlgorithm", [])) == 5 and len(domain.get("coverageDomainAlgorithm", [])) == 5, "domain algorithms")
    need("independently structured" in domain.get("independentDerivationRequirement", ""), "two domain derivations")
    custody = p.get("preparedOutputCustody", {})
    need("every exact blob byte" in custody.get("transfer", "") and "read-only" in custody.get("readAuthority", ""), "prepared byte custody")
    need("unique reconstruction" in custody.get("planCommitmentProof", ""), "manifest plan proof")

    c2pin = r.get("c2BoundedParameterValuePin", {})
    need(c2pin.get("limits") == {"maxDepth": 8, "maxMapEntries": 64, "maxArrayItems": 256, "maxStringUtf8Bytes": 4096, "maxTotalCanonicalBytes": 65536}, "C2 bounds")
    need(c2pin.get("canonicalIdentifierPattern") == IDENT_RE.pattern and c2pin.get("noCamelCaseException") is True, "C2 identifier")
    need("opensip-canonical-json-v1" in c2pin.get("canonicalByteMetric", ""), "C2 canonical byte metric")
    params = r.get("repositoryExecutionGrantParametersV2", {})
    need(params.get("required") == ["schema_version", "build_scripts", "procedural_macros", "network", "tool_paths"] and params.get("optional") == [], "parameter schema")
    tool = r.get("toolPathV2", {})
    need(tool.get("required") == ["artifact_id", "bundle_relative_path", "file_sha256", "role"] and all(tool.get("c2KeyProof", {}).get(k) is True for k in TOOL_FIELDS), "RI tool schema")
    bijection = r.get("planTag10ToWireBijection", {})
    field_map = bijection.get("fieldMap", [])
    need(type(field_map) is list and len(field_map) == 5 and "forward" not in bijection.get("reverseRule", "").lower(), "tag10 mapping")
    final_mapping_rule = field_map[-1].get("rule", "") if type(field_map) is list and field_map and type(field_map[-1]) is dict else ""
    need("exact recursive equality and deterministic-CBOR byte equality" in final_mapping_rule, "tag10 wire equality")
    blob = r.get("preparedOutputBlobV2", {})
    need(blob.get("required") == ["kind", "ownerId", "configuration", "content"] and "no outputDigest" in blob.get("digestRule", ""), "RI non-self blob")
    need("tag 9" in r.get("preparedOutputManifestBinding", {}).get("planIdProof", "").lower(), "tag9 proof")
    need("derivation A" in r.get("analysisDomainBinding", {}).get("byteEquality", ""), "RI domain equality")

    observation = d.get("compositeObservationV2", {})
    need(set(observation.get("required", [])) == set(BOOL_OBSERVATIONS + ["terminalKind"]), "observation fields")
    need(observation.get("finiteDomainSize") == 12288 and "2^11" in observation.get("domainCalculation", ""), "reducer domain")
    rows = d.get("orderedNormalizationReducerV2", {}).get("rows", [])
    actual_rows = [(row.get("priority"), row.get("predicate"), row.get("normalizedFate")) for row in rows]
    need(actual_rows == REDUCER_ROWS, "ordered reducer")
    need(len(d.get("orderedNormalizationReducerV2", {}).get("compositeGoldens", [])) == 4, "composite goldens")
    need("Equal D9 code" in d.get("orderedNormalizationReducerV2", {}).get("equalPublicCodeRule", ""), "equal code rule")
    context = d.get("hostFinalizerContextV2", {})
    need(set(context.get("required", [])) == {"interruptionTiming", "admittedProviderRequiredness", "c1PredicateSufficiencyWithoutProvider", "otherRequiredCoverage", "verdict", "durability", "requiredPostconditions"}, "finalizer context")
    need("predicate" in d.get("hostFinalizerProjection", {}).get("c1PredicateRelativeRule", "").lower(), "C1 predicate sufficiency")
    final_rows = {row.get("id"): row for row in d.get("hostFinalizerProjection", {}).get("rows", [])}
    need(set(final_rows) == {"user-interruption-before-finalization", "delivery-required-failure", "provider-protocol-failure", "complete", "optional-unavailable-sufficient", "required-unavailable", "optional-budget-sufficient", "required-budget-exhausted", "cancelled"}, "finalizer rows")
    need("durability=committed" in final_rows.get("required-unavailable", {}).get("requiredConditionsForExactGolden", "") and "durability=committed" in final_rows.get("required-budget-exhausted", {}).get("requiredConditionsForExactGolden", ""), "D9 golden applicability")
    need(d.get("d9Reference", {}).get("joinState") == "CONDITIONAL-NOT-APPLIED", "D9 conditional")

    findings = [row.get("id") for row in a.get("findingDispositions", [])]
    need(findings == [
        "RPP-PF-01-LIMITS-HANDSHAKE-UNSATISFIABLE", "RPP-PF-02-TOOLPATH-C2-CARRIER-INVALID",
        "RPP-PF-03-STATE-MACHINE-NOT-CLOSED", "RPP-PF-04-PREPARED-OUTPUT-CONTENT-NOT-TRANSPORTED",
        "RPP-PF-05-D9-UNAVAILABLE-REQUIREDNESS-LOST", "RPP-PF-06-SUBJECT-AND-COVERAGE-DOMAIN-PRIVATE",
        "RPP-PF-07-SUPERVISOR-FATES-OVERLAP",
    ], "seven finding response")
    need(all(row.get("v2Disposition") == "REPAIRED-IN-CANDIDATE-AWAITING-INDEPENDENT-REVIEW" for row in a.get("findingDispositions", [])), "finding dispositions")
    need([row.get("id") for row in a.get("acceptedV1DecisionPreservation", [])] == [f"RPP-GAP-{i:02d}" for i in range(1, 21)], "twenty preservation rows")
    need(a.get("sourceReview", {}).get("decision") == "REJECT" and a.get("sourceReview", {}).get("findingCount") == 7, "review response")
    need(a.get("candidateSet") == [PROTOCOL, CHECKER, RESPONSE, DELIVERY_JOIN, RI_JOIN], "candidate set")
    need(a.get("exactFilesCreated") == [f"docs/coop/artifacts/{name}" for name in [PROTOCOL, CHECKER, RESPONSE, DELIVERY_JOIN, RI_JOIN]], "exact created files")

    for doc_name, value in [(PROTOCOL, p), (DELIVERY_JOIN, d), (RI_JOIN, r)]:
        for pin in value.get("dependencyPins", []):
            path = pin.get("path")
            need(path in DEPENDENCY_HASHES and pin.get("sha256") == DEPENDENCY_HASHES[path], f"dependency pin {doc_name}:{path}")
    need(p.get("rejectionBasis", {}).get("sha256") == FROZEN_V1_HASHES["rust-provider-protocol.v1.review-independent-prefreeze.json"], "protocol review pin")
    need(d.get("rejectionBasis", {}).get("sha256") == FROZEN_V1_HASHES["rust-provider-protocol.v1.review-independent-prefreeze.json"], "delivery review pin")
    need(r.get("rejectionBasis", {}).get("sha256") == FROZEN_V1_HASHES["rust-provider-protocol.v1.review-independent-prefreeze.json"], "RI review pin")
    return errors


def document_errors(docs: Any) -> list[str]:
    """Total parsed-JSON validator: hostile roots become findings, never raises."""
    try:
        if type(docs) is not dict or set(docs) != {PROTOCOL, DELIVERY_JOIN, RI_JOIN, RESPONSE}:
            return ["candidate document set"]
        return _document_errors(docs)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        return [f"hostile candidate shape: {type(exc).__name__}"]


def prepared_blob(kind: str, owner: str, configuration: list[str], content: bytes) -> dict[str, Any]:
    return {"kind": kind, "ownerId": owner, "configuration": configuration, "content": content}


def prepared_fixture() -> tuple[list[dict[str, Any]], list[bytes], str]:
    blobs = [
        prepared_blob("build-script", "pkg-a", ["cfg(a)"], b"cfg=feature-a\n"),
        prepared_blob("proc-macro", "macro-a", [], bytes(range(1, 33))),
    ]
    raw_blobs = [cbor_encode(blob) for blob in blobs]
    digests = [sha256(raw) for raw in raw_blobs]
    rows = [
        {"packageId": "pkg-a", "cfg": ["cfg(a)"], "outputDigest": digests[0]},
        {"crateId": "macro-a", "outputDigest": digests[1]},
    ]
    entries: list[dict[str, Any]] = []
    for i, (kind, row, blob, raw) in enumerate(zip(["build-script", "proc-macro"], rows, blobs, raw_blobs)):
        entries.append({
            "outputOrdinal": i,
            "kind": kind,
            "planRow": row,
            "logicalPath": f".opensip/prepared/v2/{i}-{row['outputDigest']}.blob",
            "blobByteLength": len(raw),
            "blobSha256": row["outputDigest"],
            "contentByteLength": len(blob["content"]),
            "contentSha256": sha256(blob["content"]),
        })
    return entries, raw_blobs, sha256(cbor_encode(entries))


def validate_prepared(entries: Any, raw_blobs: Any, commitment: Any) -> bool:
    if type(entries) is not list or type(raw_blobs) is not list or len(entries) != len(raw_blobs) or len(entries) > 256:
        return False
    derived: list[dict[str, Any]] = []
    for i, (entry, raw) in enumerate(zip(entries, raw_blobs)):
        if not _closed(entry, {"outputOrdinal", "kind", "planRow", "logicalPath", "blobByteLength", "blobSha256", "contentByteLength", "contentSha256"}) or type(raw) is not bytes:
            return False
        if entry["outputOrdinal"] != i or not raw:
            return False
        try:
            blob = cbor_decode(raw)
        except Exception:
            return False
        if not _closed(blob, {"kind", "ownerId", "configuration", "content"}) or type(blob["content"]) is not bytes:
            return False
        row = entry["planRow"]
        if entry["kind"] == "build-script":
            if not _closed(row, {"packageId", "cfg", "outputDigest"}) or blob["kind"] != "build-script" or blob["ownerId"] != row["packageId"] or blob["configuration"] != row["cfg"]:
                return False
        elif entry["kind"] == "proc-macro":
            if not _closed(row, {"crateId", "outputDigest"}) or blob["kind"] != "proc-macro" or blob["ownerId"] != row["crateId"] or blob["configuration"] != []:
                return False
        else:
            return False
        digest = sha256(raw)
        logical = f".opensip/prepared/v2/{i}-{digest}.blob"
        expected = {
            "outputOrdinal": i, "kind": entry["kind"], "planRow": row, "logicalPath": logical,
            "blobByteLength": len(raw), "blobSha256": digest,
            "contentByteLength": len(blob["content"]), "contentSha256": sha256(blob["content"]),
        }
        if row["outputDigest"] != digest or entry != expected:
            return False
        derived.append(expected)
    return type(commitment) is str and commitment == sha256(cbor_encode(derived))


def domain_hash(prefix: str, value: Any) -> str:
    return "sha256:" + sha256(prefix.encode() + b"\x00" + cbor_encode(value))


def derive_subjects(snapshot_id: str, entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = [e for e in entries if e["kind"] == "file" and e["path"].endswith(".rs") and e["byteLength"] > 0]
    selected.sort(key=lambda e: e["path"].encode())
    if not selected or len(selected) > 256 or len({e["path"] for e in selected}) != len(selected):
        raise ValueError("subject domain")
    out = []
    for ordinal, entry in enumerate(selected):
        identity_input = {"snapshotId": snapshot_id, "path": entry["path"], "contentSha256": entry["contentSha256"], "byteLength": entry["byteLength"]}
        out.append({
            "subjectOrdinal": ordinal,
            "subjectId": "rust-file:" + domain_hash("opensip.rust-provider.subject.v2", identity_input),
            "path": entry["path"], "startByte": 0, "endByte": entry["byteLength"],
        })
    return out


def semantic_ids(rows: list[dict[str, Any]], rust_universe: dict[str, Any]) -> tuple[str, list[str]]:
    rust_id = domain_hash("opensip.rust-provider.universe.v2", rust_universe)
    values: list[str] = []
    for row in rows:
        if row["providerId"] == "rust-semantic" and row["universe"] == rust_universe:
            values.append(rust_id)
        else:
            values.append(domain_hash("opensip.semantic-universe.v2", row))
    values = sorted(set(values), key=lambda value: value.encode())
    return rust_id, values


def subject_commitment(subjects: list[dict[str, Any]]) -> str:
    return domain_hash("opensip.rust-provider.subject-scope.v2", subjects)


def derive_coverage_a(stage: dict[str, Any], subjects: list[dict[str, Any]], rust_id: str, targets: list[str], provider_build: str, fact: dict[str, Any]) -> list[dict[str, Any]]:
    relation_registry = fact["relationRegistry"]["relations"]
    schemas = fact["factRecordContractV1"]["relationPayloadSchemaRegistryV1"]["schemas"]
    commitment = subject_commitment(subjects)
    out: list[dict[str, Any]] = []
    for relation in stage["relations"]:
        for rung in relation_registry[relation]["ladder"]:
            selected_targets = [rust_id] if schemas[relation]["universeRule"] == "same-only" else targets
            for target in selected_targets:
                out.append({
                    "relation": relation, "resolution": rung, "sourceUniverseId": rust_id,
                    "targetUniverseId": target, "subjectScopeCommitment": commitment,
                    "producer": "rust-semantic", "producerVersion": provider_build,
                    "schemaVersion": schemas[relation]["schemaVersion"],
                })
    if not out or len(out) > 256 or len({cbor_encode(row) for row in out}) != len(out):
        raise ValueError("coverage domain")
    return out


def derive_coverage_b(stage: dict[str, Any], subjects: list[dict[str, Any]], rust_id: str, targets: list[str], provider_build: str, fact: dict[str, Any]) -> list[dict[str, Any]]:
    relations = fact["relationRegistry"]["relations"]
    schemas = fact["factRecordContractV1"]["relationPayloadSchemaRegistryV1"]["schemas"]
    commitment = subject_commitment(subjects)
    triples = list(itertools.chain.from_iterable(
        itertools.product(
            [relation], relations[relation]["ladder"],
            [rust_id] if schemas[relation]["universeRule"] == "same-only" else list(targets),
        )
        for relation in stage["relations"]
    ))
    return [{
        "relation": relation, "resolution": rung, "sourceUniverseId": rust_id,
        "targetUniverseId": target, "subjectScopeCommitment": commitment,
        "producer": "rust-semantic", "producerVersion": provider_build,
        "schemaVersion": schemas[relation]["schemaVersion"],
    } for relation, rung, target in triples]


def validate_domain(domain: Any, stage: dict[str, Any], expected_subjects: list[dict[str, Any]], expected_keys: list[dict[str, Any]]) -> bool:
    if not _closed(domain, {"subjects", "requestedCoverageDomain", "domainCommitment"}):
        return False
    if domain["subjects"] != expected_subjects or domain["requestedCoverageDomain"] != expected_keys:
        return False
    if any(not _closed(row, SUBJECT_FIELDS) for row in domain["subjects"]):
        return False
    if any(not _closed(row, COVERAGE_FIELDS) for row in domain["requestedCoverageDomain"]):
        return False
    expected = domain_hash("opensip.rust-provider.analysis-domain.v2", {"subjects": expected_subjects, "requestedCoverageDomain": expected_keys})
    return domain["domainCommitment"] == expected and cbor_encode(stage) == cbor_encode(copy.deepcopy(stage))


def initial_state() -> dict[str, Any]:
    return {
        "phase": "START", "stageIndex": 0, "stageCount": 0, "nextBatchIndex": 0,
        "nextCandidateOrdinal": 0, "outputSeen": False, "nextHostSequence": 0,
        "nextWorkerSequence": 0, "preparedMode": False, "requestClosed": False,
        "terminalKind": None,
    }


def fault(state: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(state)
    out["phase"] = "FAULT"
    return out


def step_frame(state: dict[str, Any], direction: str, sequence: int, frame_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    if state["phase"] in {"DONE", "FAULT", "WAIT_ZERO_EXIT", "WAIT_EOF"} or frame_type not in EXPECTED_FRAMES:
        return fault(state)
    expected_direction = EXPECTED_FRAMES[frame_type][0]
    seq_key = "nextHostSequence" if direction == "host-to-worker" else "nextWorkerSequence"
    if direction != expected_direction or sequence != state[seq_key] or sequence == 0xFFFFFFFFFFFFFFFF:
        return fault(state)
    out = copy.deepcopy(state)
    out[seq_key] += 1
    phase = state["phase"]
    direct = {
        ("START", "Hello"): "WAIT_HELLO_ACK",
        ("WAIT_HELLO_ACK", "HelloAck"): "READY_OPEN_UNIVERSE",
        ("READY_OPEN_UNIVERSE", "OpenUniverse"): "WAIT_UNIVERSE_ACCEPTED",
        ("WAIT_UNIVERSE_ACCEPTED", "UniverseAccepted"): "READY_SNAPSHOT_MANIFEST",
        ("READY_SNAPSHOT_MANIFEST", "SnapshotManifest"): "RECEIVING_SNAPSHOT",
        ("RECEIVING_SNAPSHOT", "SnapshotFileChunk"): "RECEIVING_SNAPSHOT",
        ("RECEIVING_SNAPSHOT", "SnapshotSeal"): "WAIT_SNAPSHOT_ACCEPTED",
        ("READY_PREPARED_MANIFEST", "PreparedOutputManifest"): "RECEIVING_PREPARED",
        ("RECEIVING_PREPARED", "PreparedOutputChunk"): "RECEIVING_PREPARED",
        ("RECEIVING_PREPARED", "PreparedOutputSeal"): "WAIT_PREPARED_ACCEPTED",
        ("WAIT_PREPARED_ACCEPTED", "PreparedOutputAccepted"): "READY_ANALYZE",
    }
    if (phase, frame_type) in direct:
        out["phase"] = direct[(phase, frame_type)]
        if frame_type == "OpenUniverse":
            out["preparedMode"] = payload.get("preparedMode") is True
        return out
    if phase == "WAIT_SNAPSHOT_ACCEPTED" and frame_type == "SnapshotAccepted":
        out["phase"] = "READY_PREPARED_MANIFEST" if state["preparedMode"] else "READY_ANALYZE"
        return out
    if phase == "READY_ANALYZE" and frame_type == "Analyze":
        count = payload.get("stageCount")
        if type(count) is not int or count < 1 or count > 256:
            return fault(out)
        out.update({"phase": "ANALYZING", "stageIndex": 0, "stageCount": count, "nextBatchIndex": 0, "nextCandidateOrdinal": 0, "outputSeen": False})
        return out
    if phase == "ANALYZING" and frame_type == "FactBatch":
        if (
            payload.get("batchIndex") != state["nextBatchIndex"]
            or payload.get("firstCandidateOrdinal") != state["nextCandidateOrdinal"]
            or type(payload.get("candidateCount")) is not int
            or not 1 <= payload["candidateCount"] <= EXPECTED_LIMITS["maxFactBatchCandidates"]
        ):
            return fault(out)
        out["nextBatchIndex"] += 1
        out["nextCandidateOrdinal"] += payload["candidateCount"]
        out["outputSeen"] = True
        return out
    if phase == "ANALYZING" and frame_type == "Coverage":
        out["outputSeen"] = True
        out["stageIndex"] += 1
        out["nextBatchIndex"] = 0
        out["nextCandidateOrdinal"] = 0
        out["phase"] = "READY_COMPLETE" if out["stageIndex"] == out["stageCount"] else "ANALYZING"
        return out
    if phase == "ANALYZING" and frame_type == "Unavailable" and state["stageIndex"] == 0 and not state["outputSeen"]:
        out["phase"], out["terminalKind"] = "WAIT_ZERO_EXIT", "unavailable"
        return out
    if (
        phase == "ANALYZING" and frame_type == "BudgetExhausted"
        and payload.get("budgetMatchesCurrentStage") is True
        and payload.get("budgetUnit") in {"work-units", "bytes", "items"}
    ):
        out["phase"], out["terminalKind"] = "WAIT_ZERO_EXIT", "budget-exhausted"
        return out
    if phase == "READY_COMPLETE" and frame_type == "Complete":
        out["phase"], out["terminalKind"] = "WAIT_ZERO_EXIT", "complete"
        return out
    if phase in PROVIDER_FAULT_PHASES and frame_type == "ProviderFault":
        out["phase"], out["terminalKind"] = "WAIT_ZERO_EXIT", "provider-fault"
        return out
    if phase in CANCEL_PHASES and frame_type == "Cancel":
        if state["requestClosed"]:
            return fault(out)
        out["requestClosed"] = True
        out["phase"] = "WAIT_CANCELLED"
        return out
    if phase == "WAIT_CANCELLED" and frame_type == "Cancelled" and state["requestClosed"]:
        out["phase"], out["terminalKind"] = "WAIT_ZERO_EXIT", "cancelled"
        return out
    return fault(out)


def step_process(state: dict[str, Any], event: str) -> dict[str, Any]:
    if state["phase"] == "FAULT":
        return copy.deepcopy(state)
    out = copy.deepcopy(state)
    if event == "zero-exit" and state["phase"] == "WAIT_ZERO_EXIT":
        out["phase"] = "WAIT_EOF"
        return out
    if event == "eof" and state["phase"] == "WAIT_EOF":
        out["phase"] = "DONE"
        return out
    out["phase"] = "FAULT"
    return out


def _resolve_ast(reference: Any, state: dict[str, Any], event: dict[str, Any]) -> Any:
    if type(reference) is dict and set(reference) == {"const"}:
        return reference["const"]
    if type(reference) is not str:
        return reference
    if reference.startswith("state."):
        return state[reference[6:]]
    if reference.startswith("event."):
        return event[reference[6:]]
    if reference.startswith("limits."):
        return EXPECTED_LIMITS[reference[7:]]
    raise ValueError(f"unknown AST reference {reference}")


def _guard_ast(guard: dict[str, Any], state: dict[str, Any], event: dict[str, Any]) -> bool:
    op = guard.get("op")
    if op == "true":
        return True
    if op == "all":
        return all(_guard_ast(item, state, event) for item in guard["items"])
    if op == "eq":
        return _resolve_ast(guard["left"], state, event) == _resolve_ast(guard["right"], state, event)
    if op == "neq":
        return _resolve_ast(guard["left"], state, event) != _resolve_ast(guard["right"], state, event)
    if op == "lt":
        return _resolve_ast(guard["left"], state, event) < _resolve_ast(guard["right"], state, event)
    if op == "between":
        value = _resolve_ast(guard["value"], state, event)
        maximum = _resolve_ast(guard["maximumRef"], state, event)
        return type(value) is int and guard["minimum"] <= value <= maximum
    if op == "in":
        return _resolve_ast(guard["value"], state, event) in guard["values"]
    if op == "phaseIn":
        return state["phase"] in guard["values"]
    if op == "eventKindIn":
        return event["kind"] in guard["values"]
    if op == "checkedAddCompare":
        left = _resolve_ast(guard["left"], state, event)
        right = _resolve_ast(guard["right"], state, event)
        add = guard["add"]
        if not _u64(left) or not _u64(add) or left > 0xFFFFFFFFFFFFFFFF - add:
            return False
        value = left + add
        return value < right if guard["comparison"] == "lt" else value == right
    raise ValueError(f"unknown AST guard {op}")


def _actions_ast(actions: list[dict[str, Any]], state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    original = copy.deepcopy(state)
    out = copy.deepcopy(state)
    try:
        for action in actions:
            op, field = action["op"], action.get("field")
            if op == "set":
                out[field] = _resolve_ast(action["value"], out, event)
            elif op == "copy":
                out[field] = _resolve_ast(action["from"], out, event)
            elif op == "checkedAdd":
                addition = _resolve_ast(action["from"], out, event) if "from" in action else _resolve_ast(action["value"], out, event)
                if not _u64(out[field]) or not _u64(addition) or out[field] > 0xFFFFFFFFFFFFFFFF - addition:
                    raise OverflowError
                out[field] += addition
            else:
                raise ValueError(f"unknown AST action {op}")
    except (KeyError, TypeError, OverflowError, ValueError):
        original["phase"] = "FAULT"
        return original
    return out


def _event_matches(pattern: dict[str, Any], event: dict[str, Any]) -> bool:
    if "kind" in pattern and event["kind"] != pattern["kind"]:
        return False
    if "kindIn" in pattern and event["kind"] not in pattern["kindIn"]:
        return False
    if "frameType" in pattern and event.get("frameType") != pattern["frameType"]:
        return False
    return True


def _invariants_ast(machine: dict[str, Any], state: dict[str, Any], event: dict[str, Any]) -> bool:
    if state["phase"] == "FAULT":
        return True
    for row in machine["stateRecord"]["invariants"]:
        if _guard_ast(row["when"], state, event) and not _guard_ast(row["assert"], state, event):
            return False
    return True


def ast_step(protocol: dict[str, Any], state: dict[str, Any], event: dict[str, Any], rule_hits: set[str] | None = None) -> dict[str, Any]:
    machine = protocol["orderingAndStateMachine"]
    transition = machine["transitionAstV2"]
    if state["phase"] == "FAULT":
        return copy.deepcopy(state)
    if state["phase"] in {"WAIT_ZERO_EXIT", "WAIT_EOF", "DONE"} and event["kind"] in {"frame", "stdout-byte"}:
        return fault(state)
    working = copy.deepcopy(state)
    if event["kind"] == "frame":
        frame_type = event.get("frameType")
        direction = event.get("direction")
        if (
            frame_type not in EXPECTED_FRAMES
            or event.get("payloadValid") is not True
            or direction != EXPECTED_FRAMES[frame_type][0]
        ):
            return fault(state)
        counter = "nextHostSequence" if direction == "host-to-worker" else "nextWorkerSequence"
        if event.get("sequence") != working[counter] or working[counter] == 0xFFFFFFFFFFFFFFFF:
            return fault(state)
        working[counter] += 1
    matched = False
    for rule in transition["rules"]:
        if working["phase"] not in rule["phaseIn"] or not _event_matches(rule["event"], event):
            continue
        if not _guard_ast(rule["guard"], working, event):
            continue
        if rule_hits is not None:
            rule_hits.add(rule["id"])
        working = _actions_ast(rule["actions"], working, event)
        matched = True
        break
    if not matched:
        return fault(working)
    if not _invariants_ast(machine, working, event):
        return fault(working)
    return working


def frame_event(state: dict[str, Any], frame_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    direction = EXPECTED_FRAMES.get(frame_type, ("host-to-worker", "", False))[0]
    sequence = state["nextHostSequence"] if direction == "host-to-worker" else state["nextWorkerSequence"]
    repository_mode = None
    if frame_type == "OpenUniverse":
        repository_mode = "prepared" if payload.get("preparedMode") is True else "disabled"
    return {
        "kind": "frame", "direction": direction, "sequence": sequence,
        "frameType": frame_type, "payloadValid": payload.get("payloadValid", True),
        "repositoryMode": repository_mode,
        "stageCount": payload.get("stageCount"),
        "batchIndex": payload.get("batchIndex"),
        "firstCandidateOrdinal": payload.get("firstCandidateOrdinal"),
        "candidateCount": payload.get("candidateCount"),
        "budgetMatchesCurrentStage": payload.get("budgetMatchesCurrentStage"),
        "budgetUnit": payload.get("budgetUnit"),
    }


def reference_event_step(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    if event["kind"] != "frame":
        return step_process(state, event["kind"])
    if event.get("payloadValid") is not True or event.get("frameType") not in EXPECTED_FRAMES:
        return fault(state)
    payload = {
        "preparedMode": event.get("repositoryMode") == "prepared",
        "stageCount": event.get("stageCount"),
        "batchIndex": event.get("batchIndex"),
        "firstCandidateOrdinal": event.get("firstCandidateOrdinal"),
        "candidateCount": event.get("candidateCount"),
        "budgetMatchesCurrentStage": event.get("budgetMatchesCurrentStage"),
        "budgetUnit": event.get("budgetUnit"),
    }
    return step_frame(state, event["direction"], event["sequence"], event["frameType"], payload)


def paired_step(protocol: dict[str, Any], reference: dict[str, Any], interpreted: dict[str, Any], event: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    next_reference = reference_event_step(reference, event)
    next_interpreted = ast_step(protocol, interpreted, event)
    if next_reference != next_interpreted:
        raise AssertionError(f"AST/reference divergence for {event}: {next_reference} != {next_interpreted}")
    return next_reference, next_interpreted


def emit(state: dict[str, Any], frame_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    direction = EXPECTED_FRAMES[frame_type][0]
    sequence = state["nextHostSequence"] if direction == "host-to-worker" else state["nextWorkerSequence"]
    return step_frame(state, direction, sequence, frame_type, payload)


def reach_analyze(prepared: bool) -> dict[str, Any]:
    state = initial_state()
    for frame_type, payload in [
        ("Hello", None), ("HelloAck", None), ("OpenUniverse", {"preparedMode": prepared}),
        ("UniverseAccepted", None), ("SnapshotManifest", None), ("SnapshotSeal", None),
        ("SnapshotAccepted", None),
    ]:
        state = emit(state, frame_type, payload)
    if prepared:
        for frame_type in ["PreparedOutputManifest", "PreparedOutputSeal", "PreparedOutputAccepted"]:
            state = emit(state, frame_type)
    return state


def normal_trace(prepared: bool, batch_counts: list[int]) -> dict[str, Any]:
    state = emit(reach_analyze(prepared), "Analyze", {"stageCount": len(batch_counts)})
    for batches in batch_counts:
        for _ in range(batches):
            state = emit(state, "FactBatch", {"batchIndex": state["nextBatchIndex"], "firstCandidateOrdinal": state["nextCandidateOrdinal"], "candidateCount": 1})
        state = emit(state, "Coverage")
    state = emit(state, "Complete")
    state = step_process(state, "zero-exit")
    return step_process(state, "eof")


def normal_trace_dual(protocol: dict[str, Any], prepared: bool, batch_counts: list[int]) -> dict[str, Any]:
    reference = initial_state()
    interpreted = initial_state()

    def frame(frame_type: str, payload: dict[str, Any] | None = None) -> None:
        nonlocal reference, interpreted
        event = frame_event(reference, frame_type, payload)
        reference, interpreted = paired_step(protocol, reference, interpreted, event)

    for frame_type, payload in [
        ("Hello", None), ("HelloAck", None), ("OpenUniverse", {"preparedMode": prepared}),
        ("UniverseAccepted", None), ("SnapshotManifest", None), ("SnapshotSeal", None),
        ("SnapshotAccepted", None),
    ]:
        frame(frame_type, payload)
    if prepared:
        for frame_type in ["PreparedOutputManifest", "PreparedOutputSeal", "PreparedOutputAccepted"]:
            frame(frame_type)
    frame("Analyze", {"stageCount": len(batch_counts)})
    for batches in batch_counts:
        for _ in range(batches):
            frame("FactBatch", {"batchIndex": reference["nextBatchIndex"], "firstCandidateOrdinal": reference["nextCandidateOrdinal"], "candidateCount": 1})
        frame("Coverage")
    frame("Complete")
    for kind in ["zero-exit", "eof"]:
        reference, interpreted = paired_step(protocol, reference, interpreted, {"kind": kind})
    return reference


def dual_analyzing_prefix(protocol: dict[str, Any], prepared: bool, stage_count: int) -> tuple[dict[str, Any], dict[str, Any]]:
    reference = initial_state()
    interpreted = initial_state()
    for frame_type, payload in [
        ("Hello", None), ("HelloAck", None), ("OpenUniverse", {"preparedMode": prepared}),
        ("UniverseAccepted", None), ("SnapshotManifest", None), ("SnapshotSeal", None),
        ("SnapshotAccepted", None),
    ]:
        event = frame_event(reference, frame_type, payload)
        reference, interpreted = paired_step(protocol, reference, interpreted, event)
    if prepared:
        for frame_type in ["PreparedOutputManifest", "PreparedOutputSeal", "PreparedOutputAccepted"]:
            event = frame_event(reference, frame_type)
            reference, interpreted = paired_step(protocol, reference, interpreted, event)
    event = frame_event(reference, "Analyze", {"stageCount": stage_count})
    return paired_step(protocol, reference, interpreted, event)


def exercise_all_ast_rules(protocol: dict[str, Any]) -> set[str]:
    hits: set[str] = set()
    rules = protocol["orderingAndStateMachine"]["transitionAstV2"]["rules"]
    for rule in rules:
        state = initial_state()
        state["phase"] = rule["phaseIn"][0]
        if state["phase"] == "ANALYZING":
            state["stageCount"] = 2 if rule["id"] == "T017-COVERAGE-NEXT" else 1
        elif state["phase"] == "READY_COMPLETE":
            state["stageCount"] = 1
            state["stageIndex"] = 1
            state["outputSeen"] = True
        elif state["phase"] == "WAIT_CANCELLED":
            state["requestClosed"] = True
        elif state["phase"] in {"WAIT_ZERO_EXIT", "WAIT_EOF", "DONE"}:
            state["terminalKind"] = "complete"
        pattern = rule["event"]
        kind = pattern.get("kind") or pattern.get("kindIn", ["eof"])[0]
        if rule["id"] == "T027-PROCESS-FAULT":
            kind = "nonzero-exit"
        if rule["id"] == "T028-TOTAL-FALLBACK":
            kind = "eof"
        if kind == "frame":
            frame_type = pattern["frameType"]
            payload: dict[str, Any] = {}
            if rule["id"] == "T003-OPEN-DISABLED":
                payload["preparedMode"] = False
            elif rule["id"] == "T004-OPEN-PREPARED":
                payload["preparedMode"] = True
            elif rule["id"] == "T009-SNAPSHOT-ACCEPTED-DISABLED":
                state["preparedMode"] = False
            elif rule["id"] == "T010-SNAPSHOT-ACCEPTED-PREPARED":
                state["preparedMode"] = True
            elif rule["id"] == "T015-ANALYZE":
                payload["stageCount"] = 1
            elif rule["id"] == "T016-FACT-BATCH":
                payload.update({"batchIndex": 0, "firstCandidateOrdinal": 0, "candidateCount": 1})
            elif rule["id"] == "T020-BUDGET":
                payload.update({"budgetMatchesCurrentStage": True, "budgetUnit": "items"})
            event = frame_event(state, frame_type, payload)
        else:
            event = {"kind": kind}
        ast_step(protocol, state, event, hits)
    return hits


def reduce_observation(obs: dict[str, Any]) -> str:
    if obs["userInterruptBeforeFinalization"]:
        return "USER_INTERRUPTED"
    if obs["deliveryFailure"]:
        return "DELIVERY_REQUIRED_FAILURE"
    if obs["postTerminalBytes"]:
        return "POST_TERMINAL_OUTPUT"
    if obs["malformedFrame"]:
        return "MALFORMED_FRAME"
    if obs["schemaOrCommitmentFault"]:
        return "SCHEMA_OR_COMMITMENT_FAULT"
    if obs["handshakeMismatch"]:
        return "HANDSHAKE_MISMATCH"
    if obs["deadlineHang"]:
        return "DEADLINE_HANG"
    if obs["nonzeroExit"]:
        return "NONZERO_EXIT"
    if obs["earlyEof"]:
        return "EARLY_EOF"
    if obs["terminalKind"] == "cancelled" and not obs["hostCancelSent"]:
        return "UNSOLICITED_CANCELLED"
    if obs["terminalKind"] == "provider-fault":
        return "PROVIDER_DECLARED_FAULT"
    if obs["terminalKind"] == "complete":
        return "VERIFIED_COMPLETE"
    if obs["terminalKind"] == "unavailable":
        return "VERIFIED_UNAVAILABLE"
    if obs["terminalKind"] == "budget-exhausted":
        return "VERIFIED_BUDGET_EXHAUSTED"
    if obs["terminalKind"] == "cancelled" and obs["hostCancelSent"]:
        return "VERIFIED_CANCELLED"
    return "INCOMPLETE_PROTOCOL"


def base_observation() -> dict[str, Any]:
    return {**{key: False for key in BOOL_OBSERVATIONS}, "terminalKind": "none"}


def effective_required(requiredness: str, sufficiency: str) -> bool:
    return requiredness == "required" or sufficiency == "insufficient"


PROVIDER_PROTOCOL_FATES = {
    "POST_TERMINAL_OUTPUT", "MALFORMED_FRAME", "SCHEMA_OR_COMMITMENT_FAULT",
    "HANDSHAKE_MISMATCH", "DEADLINE_HANG", "NONZERO_EXIT", "EARLY_EOF",
    "UNSOLICITED_CANCELLED", "PROVIDER_DECLARED_FAULT", "INCOMPLETE_PROTOCOL",
}


def finalizer_projection(fate: str, context: dict[str, str]) -> str:
    timing = context["interruptionTiming"]
    if fate == "USER_INTERRUPTED" or timing == "signal-before-finalization":
        return "D9-INTERRUPTED-130"
    if timing == "signal-after-finalization":
        return "PRESERVE-SETTLED-FINALIZATION"
    if fate == "DELIVERY_REQUIRED_FAILURE":
        return "D9-DELIVERY-OPERATIONAL-4"
    if fate in PROVIDER_PROTOCOL_FATES:
        return "D9-PROVIDER-PROTOCOL-OPERATIONAL-4"
    if fate == "VERIFIED_COMPLETE":
        return "DEFER-EXACT-HOST-D9-NO-PROVIDER-DEFICIENCY"
    if fate == "VERIFIED_CANCELLED":
        return "D9-INTERRUPTED-130"
    required = effective_required(
        context["admittedProviderRequiredness"],
        context["c1PredicateSufficiencyWithoutProvider"],
    )
    host_ready = context["durability"] == "committed" and context["requiredPostconditions"] == "met"
    if fate == "VERIFIED_UNAVAILABLE":
        if required and host_ready:
            return "D9-REQUIRED-PROVIDER-UNAVAILABLE-3"
        if required:
            return "DEFER-HIGHER-PRIORITY-HOST-D9"
        if (
            context["otherRequiredCoverage"] == "satisfied"
            and context["verdict"] == "pass" and host_ready
        ):
            return "D9-OPTIONAL-PROVIDER-UNAVAILABLE-SUCCESS-0"
        return "DEFER-EXACT-HOST-D9-NO-PROVIDER-DEFICIENCY"
    if fate == "VERIFIED_BUDGET_EXHAUSTED":
        if required and host_ready:
            return "D9-REQUIRED-BUDGET-EXHAUSTED-3"
        if required:
            return "DEFER-HIGHER-PRIORITY-HOST-D9"
        return "DEFER-EXACT-HOST-D9-NO-PROVIDER-DEFICIENCY"
    raise ValueError("unknown normalized fate")


def checked_add(current: int, addition: int, bound: int) -> int:
    if not _u64(current) or not _u64(addition) or current > 0xFFFFFFFFFFFFFFFF - addition:
        raise OverflowError("u64")
    result = current + addition
    if result > bound:
        raise OverflowError("bound")
    return result


def spool_bytes(analysis_ordinal: int, stage_id: str, candidate: dict[str, Any]) -> bytes:
    return cbor_encode({"analysisOrdinal": analysis_ordinal, "stageId": stage_id, "candidate": candidate})


def aggregate_manifest(ignore_pyc: bool) -> tuple[int, str]:
    proc = subprocess.run(["rg", "--files", "docs/coop/artifacts"], cwd=REPO_ROOT, check=True, capture_output=True, text=True)
    paths = []
    for path in proc.stdout.splitlines():
        if path in NEW_FILES or path in CONCURRENT_NONCANDIDATE_FILES:
            continue
        if ignore_pyc and (path.endswith(".pyc") or "/__pycache__/" in path):
            continue
        paths.append(path)
    paths.sort()
    manifest = b""
    for path in paths:
        digest = sha256((REPO_ROOT / path).read_bytes())
        manifest += f"{digest}  {path}\n".encode()
    return len(paths), sha256(manifest)


def pointer_parent(root: Any, path: tuple[Any, ...]) -> tuple[Any, Any]:
    if not path or any(part == "*" for part in path):
        raise ValueError("ambiguous path")
    node = root
    for part in path[:-1]:
        if type(part) is int:
            if type(node) is not list or part < 0 or part >= len(node):
                raise ValueError("missing path")
        elif type(node) is not dict or part not in node:
            raise ValueError("missing path")
        node = node[part]
    return node, path[-1]


def apply_mutation(docs: dict[str, Any], spec: tuple[str, str, tuple[Any, ...], Any]) -> dict[str, Any]:
    mutation_id, doc_name, path, value = spec
    if not mutation_id:
        raise ValueError("mutation id")
    out = copy.deepcopy(docs)
    parent, key = pointer_parent(out[doc_name], path)
    before = copy.deepcopy(out[doc_name])
    if value is DELETE:
        if type(parent) is dict and key in parent:
            del parent[key]
        elif type(parent) is list and type(key) is int and 0 <= key < len(parent):
            del parent[key]
        else:
            raise ValueError("missing delete")
    else:
        if type(parent) is dict:
            if key not in parent:
                raise ValueError("missing set")
            parent[key] = value
        elif type(parent) is list and type(key) is int and 0 <= key < len(parent):
            parent[key] = value
        else:
            raise ValueError("missing set")
    if out[doc_name] == before:
        raise ValueError("no-op mutation")
    return out


DELETE = object()


def mutation_specs() -> list[tuple[str, str, tuple[Any, ...], Any]]:
    return [
        ("M01-limit-extra", PROTOCOL, ("limits",), {**EXPECTED_LIMITS, "limitRule": 1}),
        ("M02-limit-missing", PROTOCOL, ("limits",), {k: v for k, v in EXPECTED_LIMITS.items() if k != "maxFramePayloadBytes"}),
        ("M03-limit-bool", PROTOCOL, ("limits", "maxFramePayloadBytes"), True),
        ("M04-limit-schema", PROTOCOL, ("wireSchema", "definitions", "ProtocolLimitsV2", "closed"), False),
        ("M05-policy-member", PROTOCOL, ("limitPolicy", "required"), ["policyId"]),
        ("M06-frame-delete", PROTOCOL, ("wireSchema", "frameSchemas", "PreparedOutputChunk"), DELETE),
        ("M07-frame-direction", PROTOCOL, ("wireSchema", "frameSchemas", "Coverage", "direction"), "host-to-worker"),
        ("M08-payload-open", PROTOCOL, ("wireSchema", "payloadSchemas", "AnalyzeV2", "closed"), False),
        ("M09-tool-camel", PROTOCOL, ("wireSchema", "definitions", "ToolPathV2", "required"), ["artifactId", "bundle_relative_path", "file_sha256", "role"]),
        ("M10-blob-self", PROTOCOL, ("wireSchema", "definitions", "PreparedOutputBlobV2", "required"), ["kind", "ownerId", "configuration", "content", "outputDigest"]),
        ("M11-stage-private", PROTOCOL, ("wireSchema", "definitions", "StageRequestV2", "required"), ["stageOrdinal", "planStage", "analysisDomain", "subjects"]),
        ("M12-phase-alias", PROTOCOL, ("orderingAndStateMachine", "stateRecord", "phaseValues", 11), "ANALYZING_ANY_STAGE"),
        ("M13-fault-phase-drop", PROTOCOL, ("orderingAndStateMachine", "providerFaultPermittedPhases"), PROVIDER_FAULT_PHASES[:-1]),
        ("M14-cancel-phase-drop", PROTOCOL, ("orderingAndStateMachine", "cancelPermittedPhases"), CANCEL_PHASES[:-1]),
        ("M15-initial", PROTOCOL, ("orderingAndStateMachine", "initialState", "stageCount"), 1),
        ("M16-transition-table", PROTOCOL, ("orderingAndStateMachine", "transitionAstV2", "rules"), []),
        ("M17-domain-owner", PROTOCOL, ("planAndDomainProjection", "planStageByteRule"), "copy approximately"),
        ("M18-domain-algorithm", PROTOCOL, ("planAndDomainProjection", "subjectsAlgorithm"), []),
        ("M19-two-derivations", PROTOCOL, ("planAndDomainProjection", "independentDerivationRequirement"), "one derivation"),
        ("M20-prepared-bytes", PROTOCOL, ("preparedOutputCustody", "transfer"), "digest rows only"),
        ("M21-tag-c2-limit", RI_JOIN, ("c2BoundedParameterValuePin", "limits", "maxDepth"), 9),
        ("M22-camel-exception", RI_JOIN, ("c2BoundedParameterValuePin", "noCamelCaseException"), False),
        ("M23-param-key", RI_JOIN, ("repositoryExecutionGrantParametersV2", "required", 0), "schemaVersion"),
        ("M24-tool-key", RI_JOIN, ("toolPathV2", "required", 0), "artifactId"),
        ("M25-tool-key-proof", RI_JOIN, ("toolPathV2", "c2KeyProof", "artifact_id"), False),
        ("M26-tag10-drop", RI_JOIN, ("planTag10ToWireBijection", "fieldMap"), []),
        ("M27-tag10-byte", RI_JOIN, ("planTag10ToWireBijection", "fieldMap", 4, "rule"), "same count"),
        ("M28-blob-digest", RI_JOIN, ("preparedOutputBlobV2", "digestRule"), "opaque digest"),
        ("M29-tag9", RI_JOIN, ("preparedOutputManifestBinding", "planIdProof"), "not committed"),
        ("M30-domain-equality", RI_JOIN, ("analysisDomainBinding", "byteEquality"), "copy request"),
        ("M31-domain-size", DELIVERY_JOIN, ("compositeObservationV2", "finiteDomainSize"), 12287),
        ("M32-reducer-order", DELIVERY_JOIN, ("orderedNormalizationReducerV2", "rows", 2, "priority"), 99),
        ("M33-reducer-fate", DELIVERY_JOIN, ("orderedNormalizationReducerV2", "rows", 3, "normalizedFate"), "NONZERO_EXIT"),
        ("M34-reducer-fallback", DELIVERY_JOIN, ("orderedNormalizationReducerV2", "rows", 15), DELETE),
        ("M35-reducer-goldens", DELIVERY_JOIN, ("orderedNormalizationReducerV2", "compositeGoldens"), []),
        ("M36-finalizer-context", DELIVERY_JOIN, ("hostFinalizerContextV2", "required"), []),
        ("M37-finalizer-rows", DELIVERY_JOIN, ("hostFinalizerProjection", "rows"), []),
        ("M38-d9-apply", DELIVERY_JOIN, ("d9Reference", "joinState"), "APPLIED"),
        ("M39-response-findings", RESPONSE, ("findingDispositions",), []),
        ("M40-response-preservation", RESPONSE, ("acceptedV1DecisionPreservation",), []),
        ("M41-response-authority", RESPONSE, ("authority", "selfReview"), True),
        ("M42-response-status", RESPONSE, ("status",), "APPLIED"),
    ]


def run_semantic_checks(report: CheckReport, docs: dict[str, Any], deps: dict[str, Any], raw: dict[str, bytes]) -> tuple[int, int]:
    p, d, r, a = docs[PROTOCOL], docs[DELIVERY_JOIN], docs[RI_JOIN], docs[RESPONSE]
    structural = document_errors(docs)
    report.expect(not structural, "document structure: " + "; ".join(structural[:4]))
    report.expect(not import_custody_errors(), "import custody")

    # Strict JSON behavior is independent of the candidate documents.
    report.reject(lambda: strict_candidate_loads('{"a":1,"a":2}'), "duplicate JSON accepted")
    report.reject(lambda: strict_candidate_loads('{"a":NaN}'), "nonfinite JSON accepted")
    report.reject(lambda: strict_candidate_loads('{"a":1.25}'), "float JSON accepted")
    report.expect(type(strict_dependency_loads('{"a":1.25}')["a"]) is Decimal, "dependency finite decimal")
    for hostile_root in [None, True, 7, "x", [], [1], {"unexpected": {}}]:
        report.reject(lambda hostile_root=hostile_root: not document_errors(hostile_root), "hostile document set accepted")
    for hostile_value in [None, True, 7, "x", [], [1], {}]:
        hostile_docs = copy.deepcopy(docs)
        hostile_docs[PROTOCOL] = hostile_value
        report.reject(lambda hostile_docs=hostile_docs: not document_errors(hostile_docs), "hostile protocol root accepted")

    hello_limits = copy.deepcopy(EXPECTED_LIMITS)
    report.expect(hello_limits == p["limits"] and cbor_encode(hello_limits) == cbor_encode(p["limits"]), "Hello limit equality")
    for bad in [
        {**hello_limits, "limitRule": "x"},
        {k: v for k, v in hello_limits.items() if k != "maxScratchBytes"},
        {**hello_limits, "maxScratchBytes": True},
        {**hello_limits, "maxScratchBytes": -1},
    ]:
        report.reject(lambda bad=bad: bad == EXPECTED_LIMITS, "invalid limits accepted")
    report.reject(lambda: checked_add(0xFFFFFFFFFFFFFFFF, 1, 0xFFFFFFFFFFFFFFFF), "u64 overflow accepted")
    report.expect(checked_add(4, 5, 9) == 9, "checked bound inclusive")
    report.reject(lambda: checked_add(4, 6, 9), "bound overflow accepted")

    tool = {"artifact_id": "rust-toolchain-bundle", "bundle_relative_path": "bin/rustc", "file_sha256": "a" * 64, "role": "rustc"}
    params = {"build_scripts": True, "network": False, "procedural_macros": False, "schema_version": 2, "tool_paths": [tool]}
    report.expect(repository_parameter_errors(params) == [], "valid C2 parameters")
    report.expect(cbor_encode(params["tool_paths"]) == cbor_encode(copy.deepcopy(params["tool_paths"])), "tag10/wire bytes")
    invalid_params: list[Any] = []
    bad = copy.deepcopy(params); bad["tool_paths"][0]["artifactId"] = bad["tool_paths"][0].pop("artifact_id"); invalid_params.append(bad)
    bad = copy.deepcopy(params); bad["tool_paths"][0]["future_key"] = True; invalid_params.append(bad)
    bad = copy.deepcopy(params); bad["schema_version"] = 2.0; invalid_params.append(bad)
    bad = copy.deepcopy(params); bad["schema_version"] = 1 << 63; invalid_params.append(bad)
    bad = copy.deepcopy(params); bad["tool_paths"][0]["role"] = b"rustc"; invalid_params.append(bad)
    bad = copy.deepcopy(params); bad["tool_paths"][0]["bundle_relative_path"] = "e\u0301"; invalid_params.append(bad)
    bad = copy.deepcopy(params); bad["tool_paths"] = [tool] * 257; invalid_params.append(bad)
    bad = copy.deepcopy(params); bad["future"] = None; invalid_params.append(bad)
    bad = {"schema_version": 2, "build_scripts": True, "network": False, "procedural_macros": False, "tool_paths": [tool]}; invalid_params.append(bad)
    nested: Any = None
    for _ in range(10): nested = {"a": nested}
    bad = copy.deepcopy(params); bad["tool_paths"] = nested; invalid_params.append(bad)
    for bad in invalid_params:
        report.reject(lambda bad=bad: not repository_parameter_errors(bad), "invalid C2 parameter accepted")
    report.reject(lambda: not bounded_parameter_errors({f"k{i}": i for i in range(65)}), "C2 map bound accepted")
    report.reject(lambda: not bounded_parameter_errors({"a": "x" * 4097}), "C2 string bound accepted")
    report.reject(lambda: not bounded_parameter_errors({"a": ["x" * 4096] * 20}), "C2 total bound accepted")
    for hostile in ["/tmp/rustc", "../bin/rustc", "C:/bin/rustc", "bin\\rustc", "bin//rustc", "bin/./rustc", "bin/\x00rustc"]:
        report.reject(lambda hostile=hostile: _path(hostile), f"hostile root accepted {hostile!r}")
    report.expect(_path("bin/rustc"), "canonical tool path")

    # Canonical CBOR and framing fixed fixtures.
    values = [None, False, True, 0, 23, 24, 256, "é", b"\x00\xff", [1, "x"], {"aa": 1, "b": 2}]
    for value in values:
        encoded = cbor_encode(value)
        report.expect(cbor_decode(encoded) == value, f"CBOR roundtrip {value!r}")
    report.reject(lambda: cbor_decode(b"\x18\x01"), "nonshortest CBOR accepted")
    report.reject(lambda: cbor_decode(b"\xfb" + b"\x00" * 8), "float CBOR accepted")
    report.reject(lambda: cbor_decode(bytes.fromhex("a2616101616102")), "duplicate CBOR map accepted")
    envelope = {"protocolMajor": 2, "direction": "host-to-worker", "sequence": 0, "frameType": "Hello", "payload": {"limits": EXPECTED_LIMITS}}
    framed = frame_encode(envelope)
    report.expect(frame_decode(framed, EXPECTED_LIMITS["maxFramePayloadBytes"]) == envelope, "frame roundtrip")
    report.reject(lambda: frame_decode(framed[:8] + bytes([framed[8] ^ 1]) + framed[9:], EXPECTED_LIMITS["maxFramePayloadBytes"]), "frame digest accepted")
    report.reject(lambda: frame_decode((EXPECTED_LIMITS["maxFramePayloadBytes"] + 1).to_bytes(8, "big"), EXPECTED_LIMITS["maxFramePayloadBytes"]), "oversize frame accepted")

    # Exact candidate spool accounting includes the closed wrapper, not only candidate bytes.
    candidate = {"candidateOrdinal": 0, "relation": "declares", "canonicalRelationPayload": b"\xa0"}
    entry_raw = spool_bytes(0, "rust-declares", candidate)
    report.expect(len(entry_raw) > len(cbor_encode(candidate)) and cbor_decode(entry_raw)["candidate"] == candidate, "spool wrapper bytes")
    report.expect(checked_add(0, len(entry_raw), len(entry_raw)) == len(entry_raw), "spool exact boundary")
    report.reject(lambda: checked_add(0, len(entry_raw), len(entry_raw) - 1), "spool over-bound accepted")

    # Byte-bearing prepared corpus round trips and hostile mutations.
    entries, blobs, manifest = prepared_fixture()
    report.expect(validate_prepared(entries, blobs, manifest), "prepared corpus valid")
    empty_blob = prepared_blob("build-script", "pkg-empty", [], b"")
    empty_raw = cbor_encode(empty_blob)
    empty_digest = sha256(empty_raw)
    empty_row = {"packageId": "pkg-empty", "cfg": [], "outputDigest": empty_digest}
    empty_entry = {"outputOrdinal": 0, "kind": "build-script", "planRow": empty_row, "logicalPath": f".opensip/prepared/v2/0-{empty_digest}.blob", "blobByteLength": len(empty_raw), "blobSha256": empty_digest, "contentByteLength": 0, "contentSha256": sha256(b"")}
    report.expect(validate_prepared([empty_entry], [empty_raw], sha256(cbor_encode([empty_entry]))), "empty prepared content")
    chunks = [[blob[i:i + 7] for i in range(0, len(blob), 7)] for blob in blobs]
    report.expect([b"".join(parts) for parts in chunks] == blobs, "prepared chunk roundtrip")
    bad_entries = copy.deepcopy(entries); bad_entries[0]["blobByteLength"] += 1
    report.reject(lambda: validate_prepared(bad_entries, blobs, manifest), "prepared size accepted")
    bad_entries = copy.deepcopy(entries); bad_entries[0]["blobSha256"] = "0" * 64
    report.reject(lambda: validate_prepared(bad_entries, blobs, manifest), "prepared digest accepted")
    bad_entries = copy.deepcopy(entries); bad_entries[0]["contentSha256"] = "0" * 64
    report.reject(lambda: validate_prepared(bad_entries, blobs, manifest), "prepared content digest accepted")
    bad_entries = copy.deepcopy(entries); bad_entries.reverse()
    report.reject(lambda: validate_prepared(bad_entries, blobs, manifest), "prepared order accepted")
    report.reject(lambda: validate_prepared(entries, blobs[:-1], manifest), "missing blob accepted")
    changed = list(blobs); changed[0] = bytes([changed[0][0] ^ 1]) + changed[0][1:]
    report.reject(lambda: validate_prepared(entries, changed, manifest), "changed blob accepted")
    bad_entries = copy.deepcopy(entries); bad_entries[0]["logicalPath"] = "tmp/output"
    report.reject(lambda: validate_prepared(bad_entries, blobs, manifest), "prepared path accepted")
    bad_blob = cbor_decode(blobs[0]); bad_blob["cas_ref"] = "sha256:" + "a" * 64
    changed = list(blobs); changed[0] = cbor_encode(bad_blob)
    report.reject(lambda: validate_prepared(entries, changed, manifest), "hidden CAS accepted")
    cycle: list[Any] = []; cycle.append(cycle)
    report.reject(lambda: cbor_encode(cycle), "prepared cycle accepted")

    # Deterministic subjects and Coverage: two independently shaped derivations.
    snapshot_id = "snap1:sha256:" + "1" * 64
    snapshot_entries = [
        {"path": "README.md", "kind": "file", "byteLength": 3, "contentSha256": "1" * 64},
        {"path": "src/b.rs", "kind": "file", "byteLength": 20, "contentSha256": "b" * 64},
        {"path": "src/a.rs", "kind": "file", "byteLength": 10, "contentSha256": "a" * 64},
        {"path": "src/empty.rs", "kind": "file", "byteLength": 0, "contentSha256": "e" * 64},
    ]
    rust_universe = {"providerBuildId": "rust-provider:fixture", "resolvedInputs": {"edition": "2024"}}
    semantic_rows = [
        {"providerId": "rust-semantic", "providerVersion": "rust-provider:fixture", "universe": rust_universe},
        {"providerId": "typescript-semantic", "providerVersion": "ts:fixture", "universe": {"module": "node"}},
    ]
    stage = {"kind": "fact-derivation", "stageId": "rust-main", "relations": ["calls", "declares"], "operator": "semantic-provider", "providerId": "rust-semantic"}
    subjects = derive_subjects(snapshot_id, snapshot_entries)
    rust_id, targets = semantic_ids(semantic_rows, rust_universe)
    keys_a = derive_coverage_a(stage, subjects, rust_id, targets, "rust-provider:fixture", deps["fact-plane.v1.json"])
    keys_b = derive_coverage_b(stage, subjects, rust_id, targets, "rust-provider:fixture", deps["fact-plane.v1.json"])
    report.expect(cbor_encode(keys_a) == cbor_encode(keys_b), "two Coverage derivations")
    report.expect([s["path"] for s in subjects] == ["src/a.rs", "src/b.rs"] and all(s["startByte"] == 0 for s in subjects), "subject range/order")
    domain = {"subjects": subjects, "requestedCoverageDomain": keys_a, "domainCommitment": domain_hash("opensip.rust-provider.analysis-domain.v2", {"subjects": subjects, "requestedCoverageDomain": keys_a})}
    report.expect(validate_domain(domain, stage, subjects, keys_a), "domain wire equality")
    relation_registry = deps["fact-plane.v1.json"]["relationRegistry"]["relations"]
    expected_call_count = len(relation_registry["calls"]["ladder"]) * len(targets)
    report.expect(sum(1 for key in keys_a if key["relation"] == "calls") == expected_call_count, "all call rungs/targets")
    report.expect(sum(1 for key in keys_a if key["relation"] == "declares") == 1, "same-only declares")
    mutations: list[Any] = []
    bad = copy.deepcopy(domain); bad["subjects"][0]["endByte"] += 1; mutations.append(bad)
    bad = copy.deepcopy(domain); bad["subjects"].reverse(); mutations.append(bad)
    bad = copy.deepcopy(domain); bad["requestedCoverageDomain"] = bad["requestedCoverageDomain"][1:]; mutations.append(bad)
    bad = copy.deepcopy(domain); bad["requestedCoverageDomain"][0]["targetUniverseId"] = "sha256:" + "9" * 64; mutations.append(bad)
    bad = copy.deepcopy(domain); bad["requestedCoverageDomain"][0]["producer"] = "other"; mutations.append(bad)
    bad = copy.deepcopy(domain); bad["requestedCoverageDomain"][0]["producerVersion"] = "other"; mutations.append(bad)
    bad = copy.deepcopy(domain); bad["requestedCoverageDomain"][0]["schemaVersion"] = 2; mutations.append(bad)
    bad = copy.deepcopy(domain); bad["domainCommitment"] = "sha256:" + "0" * 64; mutations.append(bad)
    for bad in mutations:
        report.reject(lambda bad=bad: validate_domain(bad, stage, subjects, keys_a), "domain mutation accepted")
    report.expect(cbor_encode(stage) == cbor_encode(copy.deepcopy(stage)), "Plan stage byte equality")

    # Concrete independent state model.
    trace_count = 0
    for prepared in [False, True]:
        for stage_count in range(1, 4):
            for batch_counts in itertools.product(range(3), repeat=stage_count):
                trace_count += 1
                try:
                    terminal_state = normal_trace_dual(p, prepared, list(batch_counts))
                except AssertionError as exc:
                    report.failures.append(str(exc))
                    terminal_state = {"phase": "FAULT"}
                report.expect(terminal_state["phase"] == "DONE", "normal state trace")
    report.expect(exercise_all_ast_rules(p) == {f"T{i:03d}-" + row["id"].split("-", 1)[1] for i, row in enumerate(p["orderingAndStateMachine"]["transitionAstV2"]["rules"], 1)}, "all transition AST rules exercised")
    for prepared in [False, True]:
        state = emit(reach_analyze(prepared), "Analyze", {"stageCount": 1})
        terminal = emit(state, "Unavailable")
        report.expect(step_process(step_process(terminal, "zero-exit"), "eof")["phase"] == "DONE", "Unavailable trace")
        state_after_fact = emit(state, "FactBatch", {"batchIndex": 0, "firstCandidateOrdinal": 0, "candidateCount": 1})
        report.expect(emit(state_after_fact, "Unavailable")["phase"] == "FAULT", "late Unavailable fault")
        budget = emit(state_after_fact, "BudgetExhausted", {"budgetMatchesCurrentStage": True, "budgetUnit": "items"})
        report.expect(budget["phase"] == "WAIT_ZERO_EXIT", "budget trace")
        try:
            ref, interp = dual_analyzing_prefix(p, prepared, 1)
            ref, interp = paired_step(p, ref, interp, frame_event(ref, "Unavailable"))
            ref, interp = paired_step(p, ref, interp, {"kind": "zero-exit"})
            ref, interp = paired_step(p, ref, interp, {"kind": "eof"})
            report.expect(ref["phase"] == "DONE", "dual Unavailable trace")
        except AssertionError:
            report.expect(False, "dual Unavailable trace")
        try:
            ref, interp = dual_analyzing_prefix(p, prepared, 1)
            fact_event = frame_event(ref, "FactBatch", {"batchIndex": 0, "firstCandidateOrdinal": 0, "candidateCount": 1})
            ref, interp = paired_step(p, ref, interp, fact_event)
            budget_event = frame_event(ref, "BudgetExhausted", {"budgetMatchesCurrentStage": True, "budgetUnit": "items"})
            ref, interp = paired_step(p, ref, interp, budget_event)
            report.expect(ref["terminalKind"] == "budget-exhausted", "dual Budget trace")
        except AssertionError:
            report.expect(False, "dual Budget trace")
        try:
            ref, interp = dual_analyzing_prefix(p, prepared, 1)
            fact_event = frame_event(ref, "FactBatch", {"batchIndex": 0, "firstCandidateOrdinal": 0, "candidateCount": 1})
            ref, interp = paired_step(p, ref, interp, fact_event)
            ref, interp = paired_step(p, ref, interp, frame_event(ref, "Unavailable"))
            report.expect(ref["phase"] == "FAULT", "dual late Unavailable")
        except AssertionError:
            report.expect(False, "dual late Unavailable")
    for phase in CANCEL_PHASES:
        state = initial_state(); state["phase"] = phase
        cancelled = emit(emit(state, "Cancel"), "Cancelled")
        report.expect(cancelled["phase"] == "WAIT_ZERO_EXIT" and cancelled["terminalKind"] == "cancelled", f"cancel {phase}")
    for phase in PROVIDER_FAULT_PHASES:
        state = initial_state(); state["phase"] = phase
        report.expect(emit(state, "ProviderFault")["terminalKind"] == "provider-fault", f"provider fault {phase}")
    state = initial_state()
    report.reject(lambda: step_frame(state, "host-to-worker", 1, "Hello")["phase"] != "FAULT", "skipped sequence accepted")
    state["nextHostSequence"] = 0xFFFFFFFFFFFFFFFF
    report.reject(lambda: step_frame(state, "host-to-worker", 0xFFFFFFFFFFFFFFFF, "Hello")["phase"] != "FAULT", "sequence overflow accepted")
    terminal = emit(normal_trace(False, [0]), "Hello")
    report.expect(terminal["phase"] == "FAULT", "post-DONE frame fault")
    report.expect(step_process(reach_analyze(False), "eof")["phase"] == "FAULT", "early EOF fault")
    state = emit(emit(reach_analyze(False), "Analyze", {"stageCount": 1}), "Unavailable")
    report.expect(step_process(state, "nonzero-exit")["phase"] == "FAULT", "nonzero exit fault")
    report.expect(step_frame(state, "worker-to-host", state["nextWorkerSequence"], "ProviderFault")["phase"] == "FAULT", "post-terminal frame fault")

    for invalid_payload in [
        {"batchIndex": 1, "firstCandidateOrdinal": 0, "candidateCount": 1},
        {"batchIndex": 0, "firstCandidateOrdinal": 1, "candidateCount": 1},
        {"batchIndex": 0, "firstCandidateOrdinal": 0, "candidateCount": 0},
    ]:
        ref, interp = dual_analyzing_prefix(p, False, 1)
        try:
            ref, interp = paired_step(p, ref, interp, frame_event(ref, "FactBatch", invalid_payload))
            report.expect(ref["phase"] == "FAULT", "dual invalid FactBatch")
        except AssertionError:
            report.expect(False, "dual invalid FactBatch")
    for invalid_budget in [
        {"budgetMatchesCurrentStage": False, "budgetUnit": "items"},
        {"budgetMatchesCurrentStage": True, "budgetUnit": "milliseconds"},
    ]:
        ref, interp = dual_analyzing_prefix(p, False, 1)
        try:
            ref, interp = paired_step(p, ref, interp, frame_event(ref, "BudgetExhausted", invalid_budget))
            report.expect(ref["phase"] == "FAULT", "dual invalid Budget")
        except AssertionError:
            report.expect(False, "dual invalid Budget")
    ref, interp = dual_analyzing_prefix(p, False, 1)
    try:
        ref, interp = paired_step(p, ref, interp, frame_event(ref, "Complete"))
        report.expect(ref["phase"] == "FAULT", "dual early Complete")
    except AssertionError:
        report.expect(False, "dual early Complete")

    # Frame precheck mutations are compared as well as independently rejected.
    ref = initial_state(); interp = initial_state()
    valid_hello = frame_event(ref, "Hello")
    for change in [
        {"sequence": 1}, {"direction": "worker-to-host"},
        {"payloadValid": False}, {"frameType": "UNKNOWN_FRAME"},
    ]:
        event = {**valid_hello, **change}
        try:
            next_ref, next_interp = paired_step(p, ref, interp, event)
            report.expect(next_ref["phase"] == "FAULT", "dual frame precheck")
        except AssertionError:
            report.expect(False, "dual frame precheck")

    # Directly exercise interpreter/reference agreement on every accepted
    # ProviderFault/Cancel phase and hostile precheck/process route.
    for phase in PROVIDER_FAULT_PHASES:
        ref = initial_state(); ref["phase"] = phase
        interp = copy.deepcopy(ref)
        event = frame_event(ref, "ProviderFault")
        try:
            paired_step(p, ref, interp, event)
            report.expect(True, f"dual provider fault {phase}")
        except AssertionError:
            report.expect(False, f"dual provider fault {phase}")
    for phase in CANCEL_PHASES:
        ref = initial_state(); ref["phase"] = phase
        interp = copy.deepcopy(ref)
        event = frame_event(ref, "Cancel")
        try:
            paired_step(p, ref, interp, event)
            report.expect(True, f"dual cancel {phase}")
        except AssertionError:
            report.expect(False, f"dual cancel {phase}")
    for hostile_event in [
        {"kind": "eof"}, {"kind": "nonzero-exit"}, {"kind": "signal-death"},
        {"kind": "deadline"}, {"kind": "stdout-byte"},
    ]:
        ref = reach_analyze(False)
        try:
            paired_step(p, ref, copy.deepcopy(ref), hostile_event)
            report.expect(True, f"dual hostile {hostile_event['kind']}")
        except AssertionError:
            report.expect(False, f"dual hostile {hostile_event['kind']}")

    # Exhaustive ordered reducer, including exact overlap cases.
    reducer_count = 0
    fates = {row[2] for row in REDUCER_ROWS}
    for mask in range(1 << len(BOOL_OBSERVATIONS)):
        booleans = {key: bool(mask & (1 << i)) for i, key in enumerate(BOOL_OBSERVATIONS)}
        for terminal in TERMINAL_KINDS:
            reducer_count += 1
            fate = reduce_observation({**booleans, "terminalKind": terminal})
            if fate not in fates:
                report.failures.append("reducer escaped finite fate")
                break
    report.expect(reducer_count == 12288, "reducer exhaustive count")
    composites = [
        ({"malformedFrame": True, "nonzeroExit": True}, "none", "MALFORMED_FRAME"),
        ({"postTerminalBytes": True, "nonzeroExit": True}, "complete", "POST_TERMINAL_OUTPUT"),
        ({"coverageObserved": True, "deadlineHang": True}, "none", "DEADLINE_HANG"),
    ]
    for fields, terminal, expected in composites:
        obs = base_observation(); obs.update(fields); obs["terminalKind"] = terminal
        report.expect(reduce_observation(obs) == expected, f"composite {expected}")
    obs = {**{key: True for key in BOOL_OBSERVATIONS}, "terminalKind": "provider-fault"}
    report.expect(reduce_observation(obs) == "USER_INTERRUPTED", "interruption precedence")

    # D9 values are read from exact pinned bytes, not copied from producer prose.
    d9 = deps["d9-exit-contract.v1.13.json"]
    goldens = {row["id"]: row for row in d9["goldenCases"]}
    final_rows = {row["id"]: row for row in d["hostFinalizerProjection"]["rows"]}
    cross = [
        ("optional-unavailable-sufficient", "analysis-optional-provider-unavailable"),
        ("required-unavailable", "analysis-required-provider-unavailable"),
        ("required-budget-exhausted", "analysis-budget-exhausted"),
        ("user-interruption-before-finalization", "user-interrupt-finite"),
    ]
    for row_id, golden_id in cross:
        row, golden = final_rows[row_id], goldens[golden_id]
        for key, value in row.get("d9Axes", {}).items():
            report.expect(golden["scenarioAxes"][key] == value, f"D9 axes {row_id}:{key}")
        termination = row["termination"]
        expected_term = golden["expectedTermination"]
        report.expect(termination["class"] == expected_term["class"], f"D9 class {row_id}")
        report.expect(termination["reasonCodes"] == expected_term.get("reasonCodes", []), f"D9 reasons {row_id}")
        report.expect(termination["exitCode"] == d9["classToExitCode"][termination["class"]], f"D9 exit {row_id}")
    report.expect(not effective_required("optional", "sufficient"), "optional sufficient")
    report.expect(effective_required("optional", "insufficient"), "predicate makes required")
    report.expect(effective_required("required", "sufficient"), "admission makes required")
    report.expect(d["d9Reference"]["candidateSha256"] == DEPENDENCY_HASHES["d9-exit-contract.v1.13.json"], "D9 exact pin")

    finalizer_results = {
        "D9-INTERRUPTED-130", "PRESERVE-SETTLED-FINALIZATION",
        "D9-DELIVERY-OPERATIONAL-4", "D9-PROVIDER-PROTOCOL-OPERATIONAL-4",
        "DEFER-EXACT-HOST-D9-NO-PROVIDER-DEFICIENCY",
        "D9-REQUIRED-PROVIDER-UNAVAILABLE-3",
        "D9-OPTIONAL-PROVIDER-UNAVAILABLE-SUCCESS-0",
        "D9-REQUIRED-BUDGET-EXHAUSTED-3", "DEFER-HIGHER-PRIORITY-HOST-D9",
    }
    finalizer_count = 0
    for values in itertools.product(
        ["none", "signal-before-finalization", "signal-after-finalization"],
        ["optional", "required"], ["sufficient", "insufficient"],
        ["satisfied", "unsatisfied", "unknown"],
        ["pass", "advisory", "fail", "indeterminate", "unavailable"],
        ["committed", "failed", "not-required", "not-applicable"],
        ["met", "failed", "not-applicable"],
    ):
        context = dict(zip([
            "interruptionTiming", "admittedProviderRequiredness",
            "c1PredicateSufficiencyWithoutProvider", "otherRequiredCoverage",
            "verdict", "durability", "requiredPostconditions",
        ], values))
        for fate in {row[2] for row in REDUCER_ROWS}:
            finalizer_count += 1
            if finalizer_projection(fate, context) not in finalizer_results:
                report.failures.append("finalizer escaped closed result")
    report.expect(finalizer_count == 34560, "finalizer exhaustive count")
    optional_context = {"interruptionTiming": "none", "admittedProviderRequiredness": "optional", "c1PredicateSufficiencyWithoutProvider": "sufficient", "otherRequiredCoverage": "satisfied", "verdict": "pass", "durability": "committed", "requiredPostconditions": "met"}
    required_context = {**optional_context, "admittedProviderRequiredness": "required"}
    predicate_context = {**optional_context, "c1PredicateSufficiencyWithoutProvider": "insufficient"}
    report.expect(finalizer_projection("VERIFIED_UNAVAILABLE", optional_context) == "D9-OPTIONAL-PROVIDER-UNAVAILABLE-SUCCESS-0", "optional Unavailable finalizer")
    report.expect(finalizer_projection("VERIFIED_UNAVAILABLE", required_context) == "D9-REQUIRED-PROVIDER-UNAVAILABLE-3", "required Unavailable finalizer")
    report.expect(finalizer_projection("VERIFIED_UNAVAILABLE", predicate_context) == "D9-REQUIRED-PROVIDER-UNAVAILABLE-3", "predicate-relative Unavailable finalizer")
    report.expect(finalizer_projection("VERIFIED_BUDGET_EXHAUSTED", required_context) == "D9-REQUIRED-BUDGET-EXHAUSTED-3", "required Budget finalizer")

    # Immutable bytes and preservation. .pyc is ignored by source aggregation.
    for name, expected in FROZEN_V1_HASHES.items():
        report.expect(sha256((HERE / name).read_bytes()) == expected, f"frozen v1 {name}")
    full_count, full_hash = aggregate_manifest(False)
    source_count, source_hash = aggregate_manifest(True)
    report.expect((full_count, full_hash) == (EXPECTED_PREEXISTING_COUNT, EXPECTED_PREEXISTING_AGGREGATE), "pre-existing full bytes")
    report.expect((source_count, source_hash) == (EXPECTED_PREEXISTING_SOURCE_COUNT, EXPECTED_PREEXISTING_SOURCE_AGGREGATE), "pre-existing source bytes ignoring pyc")
    report.expect(all((REPO_ROOT / path).exists() for path in NEW_FILES), "exact new files exist")

    # Response execution/hash record is checked only after stable values are installed.
    execution = a.get("checkerExecutionRecord", {})
    report.expect(execution.get("reducerTupleCount") == 12288, "recorded reducer count")
    if EXPECTED_RECORDED_POSITIVE >= 0:
        report.expect(execution.get("runtimePositiveCount") == EXPECTED_RECORDED_POSITIVE, "recorded positive")
        report.expect(execution.get("runtimeAdversarialCount") == EXPECTED_RECORDED_ADVERSARIAL, "recorded adversarial")
        report.expect(execution.get("mutationProbeCount") == EXPECTED_RECORDED_MUTATIONS, "recorded mutations")
        report.expect(execution.get("stateModelTraceCount") == EXPECTED_RECORDED_STATE_TRACES, "recorded traces")
        report.expect(execution.get("normalExit") == 0 and execution.get("selftestExit") == 0 and execution.get("state") == "STABLE-PASS", "recorded exits")
        hashes = a.get("hashRecord", {})
        report.expect(hashes.get("protocolSha256") == LOCAL_RAW_HASHES[PROTOCOL], "recorded protocol hash")
        report.expect(hashes.get("deliveryJoinSha256") == LOCAL_RAW_HASHES[DELIVERY_JOIN], "recorded delivery hash")
        report.expect(hashes.get("resolvedInputsJoinSha256") == LOCAL_RAW_HASHES[RI_JOIN], "recorded RI hash")
        report.expect(hashes.get("checkerSha256") == sha256(raw[CHECKER]), "recorded checker hash")
        report.expect(hashes.get("state") == "TWO-STABLE-POST-RUN-REHASHES-MATCH", "recorded stable hashes")
        preservation = a["preExistingByteIdentity"]["afterExcludingFiveNewFiles"]
        report.expect(preservation == {"artifactFileCount": 371, "aggregateManifestSha256": EXPECTED_PREEXISTING_AGGREGATE, "matchesBefore": True}, "recorded preservation")
    return reducer_count, trace_count


def run_selftest(report: CheckReport, docs: dict[str, Any]) -> int:
    # Dirty-base refusal is actual: callers reach here only after exact raw-hash
    # loading and a completely clean normal check.
    if document_errors(docs):
        report.failures.append("RPPV2-DIRTY-BASE: mutation selftest refused")
        return 0
    specs = mutation_specs()
    ids = [spec[0] for spec in specs]
    if len(ids) != len(set(ids)):
        report.failures.append("duplicate mutation id")
        return 0
    applied = 0
    for spec in specs:
        try:
            mutated = apply_mutation(docs, spec)
        except Exception as exc:
            report.failures.append(f"mutation apply escape {spec[0]}: {exc}")
            continue
        applied += 1
        if not document_errors(mutated):
            report.failures.append(f"mutation survived {spec[0]}")
    if applied != len(specs):
        report.failures.append("mutation skip escape")

    # Harness adversaries: each must be refused before it could count as a pass.
    report.reject(lambda: apply_mutation(docs, ("E-NOOP", PROTOCOL, ("version",), 2)), "no-op mutation accepted")
    report.reject(lambda: apply_mutation(docs, ("E-MISSING", PROTOCOL, ("missing",), 1)), "failed mutation accepted")
    report.reject(lambda: apply_mutation(docs, ("E-AMBIG", PROTOCOL, ("*",), 1)), "ambiguous mutation accepted")
    report.reject(lambda: (_ for _ in ()).throw(ValueError("duplicate ids")) if len({"x", "x"}) != 2 else True, "duplicate mutation accepted")
    report.reject(lambda: (_ for _ in ()).throw(ValueError("skip")) if applied - 1 != len(specs) else True, "skip mutation accepted")
    dirty = copy.deepcopy(docs); dirty[PROTOCOL]["version"] = 99
    report.reject(lambda: not document_errors(dirty), "dirty base accepted")
    return applied


def main() -> int:
    if sys.argv[1:] not in ([], ["--selftest"]):
        print("RPPV2-UNSUPPORTED-INVOCATION: require no arguments or --selftest", file=sys.stderr)
        return 2
    selftest = sys.argv[1:] == ["--selftest"]
    report = CheckReport()
    try:
        docs: dict[str, Any] = {}
        raw: dict[str, bytes] = {}
        for name in [PROTOCOL, DELIVERY_JOIN, RI_JOIN]:
            docs[name], raw[name] = read_hashed_json(name, LOCAL_RAW_HASHES[name], False)
        docs[RESPONSE], raw[RESPONSE] = read_candidate_unpinned(RESPONSE)
        raw[CHECKER] = (HERE / CHECKER).read_bytes()
        deps: dict[str, Any] = {}
        for name, expected in DEPENDENCY_HASHES.items():
            deps[name], _ = read_hashed_json(name, expected, True)
    except Exception as exc:
        print(f"RPPV2-FAIL load: {exc}", file=sys.stderr)
        return 1

    reducer_count, trace_count = run_semantic_checks(report, docs, deps, raw)
    mutations = 0
    if selftest:
        if report.failures:
            print("RPPV2-DIRTY-BASE: mutation selftest refused", file=sys.stderr)
            for failure in report.failures[:20]:
                print(f"  {failure}", file=sys.stderr)
            return 1
        mutations = run_selftest(report, docs)
    if report.failures:
        print(f"RPPV2-FAIL positive={report.positive} adversarial={report.adversarial} reducer={reducer_count} state_traces={trace_count} mutations={mutations}", file=sys.stderr)
        for failure in report.failures[:40]:
            print(f"  {failure}", file=sys.stderr)
        return 1
    mode = "selftest" if selftest else "normal"
    print(f"RPPV2-PASS mode={mode} positive={report.positive} adversarial={report.adversarial} reducer={reducer_count} state_traces={trace_count} mutations={mutations}")
    print("RPPV2-RESIDUAL independent-review-required applied=false product=false integration=false freeze=false release=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
