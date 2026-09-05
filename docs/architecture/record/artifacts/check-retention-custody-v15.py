#!/usr/bin/env python3
"""Exact architecture conformance checker for retention-tiers.v15.json.

The sole admitted invocation is ``python3 -I -B``.  This checker is an
architecture test instrument: it grants no application, product, freeze,
seal, integration, release, or production authority.
"""

from __future__ import annotations

import sys

STARTUP_REFUSAL = (
    "RT15-CHECKER-UNSUPPORTED-INVOCATION: use python3 -I -B "
    "check-retention-custody-v15.py"
)
if sys.flags.isolated != 1 or not sys.flags.dont_write_bytecode:
    print(STARTUP_REFUSAL, file=sys.stderr)
    raise SystemExit(2)

import ast
import copy
import hashlib
import json
import pathlib
import re
import types
from typing import Any, Callable, Mapping


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "retention-tiers.v15.json"
RT15_STATUS = "CANDIDATE-NOT-APPLIED/AWAITING-INDEPENDENT-REVIEW"
PROJECT_A = "prj1-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
PROJECT_B = "prj1-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
TX_BOUNDARY = "ONE_PROJECT_LEDGER_TRANSACTION"
REF_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PROJECT_RE = re.compile(r"^prj1-[0-9a-f]{64}$")

EP8 = "evaluation-proof.v8.json"
EP8_CHECKER = "check-evaluation-proof-v8.py"
EP8_REVIEW = "ep8-rt13.review-independent-cold-reconstruction.json"
RT13 = "retention-tiers.v13.json"
RT13_CHECKER = "check-retention-custody-v13.py"
RT_CORE = "check-retention-custody.py"
RT14 = "retention-tiers.v14.json"
RT14_CHECKER = "check-retention-custody-v14.py"
RT14_REVIEW = "retention-tiers.v14.review-independent-prefreeze.json"
D9 = "d9-exit-contract.v1.13.json"
D9_CHECKER = "check-d9-v1.13.py"
D9_REVIEW = "d9-exit-contract.v1.13.review-independent-prefreeze.json"

PINS: dict[str, str] = {
    EP8: "4bb33f772c8c510c470643082f6bfb8a4df28a050b4720dda6cdd5187bd3e303",
    EP8_CHECKER: "c80ac50e21dcd350e5f5285958a6cfb94d52c5c3f7d64f2396d91b544fa82769",
    EP8_REVIEW: "f4599b32a9f1b93049111b9e86debd19419902c9c5f4fb886f8d0dc9c330567e",
    RT13: "3f79668a6d26b5ecc7fd843be71aef90e779ac024a1ac54bb5cc2c8fc3e0a349",
    RT13_CHECKER: "0290b4ae22816843c2fbce1288ea36f21e78b396361fa6c0bf5291338be519f6",
    RT_CORE: "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    RT14: "b66d0275d326cdd0cfdbec5e0810788e7768c10c9f1d7ab2c4df8c44b6975770",
    RT14_CHECKER: "6b190a89ba1700cf820746b473e8e3a521c9b2f6b4856f0c501d72a44b0a1d60",
    RT14_REVIEW: "dfb037bd121f7b73fbfeb77bbbaf0e1028a8c89318c5991bb3b3ec935046575c",
    D9: "fc2c546a4cdbe2038f3a5db333ab9903d21ae9d6223777b139b58551fb2f2fae",
    D9_CHECKER: "a905ab0e4b932c2ef4c565e847a12cb398abf9cd7a74abd92f95cbc85ffc8717",
    D9_REVIEW: "88ab60efb21f603213ebff722f62f310b422f03981895e3f6779f2febe734c5b",
}

ROOT_ORDER = [
    "artifact", "version", "status", "claimId",
    "supersedesAsArchitectureCandidate", "dependencies",
    "semanticBasisProjection", "operationalCustodyProjectionContract",
    "semanticLeaseProtocolV3", "storageAndLineage", "custodyPolicy",
    "authority", "integrationState", "semanticOwnershipBoundary",
    "invariants", "assurance", "retainedResiduals", "sealRecommendation",
    "rawPhysicalIdentityContract", "verifiedSemanticRtApiContract",
]
PROTECTED_ROOTS = [
    "artifact", "claimId", "storageAndLineage", "custodyPolicy",
    "integrationState", "assurance", "sealRecommendation",
    "rawPhysicalIdentityContract",
]
REMOVED_RT14_ROOTS = [
    "capabilityClosure", "leaseProtocol", "d9Derivation",
    "identityStabilityFromRT12", "contextualD9Rejoin",
]

OLD_PATTERNED_REFS = [
    "sha256:8484848484848484848484848484848484848484848484848484848484848484",
    "sha256:9191919191919191919191919191919191919191919191919191919191919191",
    "sha256:9292929292929292929292929292929292929292929292929292929292929292",
    "sha256:9393939393939393939393939393939393939393939393939393939393939393",
    "sha256:a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1",
    "sha256:b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0",
    "sha256:c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0",
    "sha256:e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5",
    "sha256:e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6e6",
    "sha256:f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0",
    "sha256:f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1",
]
DISCOVERED_OLD_PREIMAGES = [
    "sha256:11e923bffcc99c94372d7b575d733b79787da09d5d06286732c691b1158828fa",
    "sha256:16c2fca9e371936458d01576b4ca311c22d166a45539ccbc9104823d0b10db47",
    "sha256:21fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9",
    "sha256:249a77c07b91bd865b4873c586ea4e41681be89d8d227590bfc44a3b33402ac5",
    "sha256:b4834d2eb7324dbde0aa0c9c461bedaae1ba6317b02fd441612b96dd4b4778bf",
    "sha256:d6a8d086d9ee0f2693f599ce39ecf90c0be65fd9a9127ddfd95572a2c95c3e04",
    "sha256:e3be6c3634ac045fd02d4753ac61ed6d9b82ea161e106c143de69a2f196467a5",
]


class DuplicateKeyError(ValueError):
    pass


class FloatForbidden(ValueError):
    pass


class AuthorityError(RuntimeError):
    pass


class ResolutionError(ValueError):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def _reject_float(_value: str) -> Any:
    raise FloatForbidden("floating-point JSON values are forbidden")


def _reject_constant(value: str) -> Any:
    raise FloatForbidden(f"non-finite JSON value is forbidden: {value}")


def parse_json_bytes(source: bytes, label: str) -> Any:
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label}: invalid UTF-8") from exc
    return json.loads(
        text, object_pairs_hook=_pairs, parse_float=_reject_float,
        parse_constant=_reject_constant,
    )


def pretty(value: Any) -> bytes:
    return (json.dumps(
        value, indent=2, ensure_ascii=True, sort_keys=False, allow_nan=False,
    ) + "\n").encode("utf-8")


def compact(value: Any, *, sort_keys: bool = False) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=sort_keys,
        separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cas(data: bytes) -> str:
    return "sha256:" + sha256(data)


def domain_digest(domain: str, data: bytes) -> str:
    return cas(domain.encode("ascii") + b"\x00" + len(data).to_bytes(8, "big") + data)


def exact_recursive_equal(actual: Any, expected: Any, path: str = "$") -> str | None:
    if type(actual) is not type(expected):
        return f"{path}: type {type(actual).__name__} != {type(expected).__name__}"
    if isinstance(expected, dict):
        if list(actual) != list(expected):
            return f"{path}: key order/set {list(actual)!r} != {list(expected)!r}"
        for key in expected:
            found = exact_recursive_equal(actual[key], expected[key], f"{path}.{key}")
            if found:
                return found
        return None
    if isinstance(expected, list):
        if len(actual) != len(expected):
            return f"{path}: length {len(actual)} != {len(expected)}"
        for index, (left, right) in enumerate(zip(actual, expected)):
            found = exact_recursive_equal(left, right, f"{path}[{index}]")
            if found:
                return found
        return None
    return None if actual == expected else f"{path}: {actual!r} != {expected!r}"


class FrozenAuthority:
    def __init__(self) -> None:
        self.buffers: dict[str, bytes] = {}
        self.identities: dict[str, tuple[int, int, int, int]] = {}
        self.parsed: dict[str, Any] = {}
        self.modules: dict[str, types.ModuleType] = {}
        self.read_counts: dict[str, int] = {}

    @staticmethod
    def _identity(path: pathlib.Path) -> tuple[int, int, int, int]:
        stat = path.stat()
        return stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns

    def freeze(self) -> None:
        resolved_seen: set[pathlib.Path] = set()
        for name, expected in PINS.items():
            path = (HERE / name).resolve(strict=True)
            if path in resolved_seen:
                raise AuthorityError(f"dependency alias escaped read-once rule: {name}")
            resolved_seen.add(path)
            before = self._identity(path)
            source = path.read_bytes()
            self.read_counts[name] = self.read_counts.get(name, 0) + 1
            after = self._identity(path)
            if before != after:
                raise AuthorityError(f"dependency changed while read: {name}")
            if sha256(source) != expected:
                raise AuthorityError(f"dependency hash drift: {name}")
            self.identities[name] = before
            self.buffers[name] = source
        if any(count != 1 for count in self.read_counts.values()):
            raise AuthorityError("dependency content read count is not exactly one")

        for name in (EP8, EP8_REVIEW, RT13, RT14, RT14_REVIEW, D9, D9_REVIEW):
            self.parsed[name] = parse_json_bytes(self.buffers[name], name)
        self._validate_reviews()
        for name in (EP8_CHECKER, RT13_CHECKER, RT_CORE, RT14_CHECKER):
            self.modules[name] = self._execute_verified(name)

    def _validate_reviews(self) -> None:
        ep_review = self.parsed[EP8_REVIEW]
        rt14_review = self.parsed[RT14_REVIEW]
        d9_review = self.parsed[D9_REVIEW]
        if ep_review.get("verdict", {}).get("decision") != "PASS":
            raise AuthorityError("EP8/RT13 joint review is not PASS")
        verdict14 = rt14_review.get("verdict", {})
        blockers14 = rt14_review.get("blockingFindings")
        if verdict14.get("decision") != "REJECTED-BY-DEPENDENCY" or \
                not isinstance(blockers14, list) or len(blockers14) != 1 or \
                blockers14[0].get("id") != "RT14-PF-01-REJECTED-D9-AUTHORITY":
            raise AuthorityError("RT14 dependency rejection binding drift")
        verdict9 = d9_review.get("verdict", {})
        if verdict9.get("decision") != "PASS" or \
                verdict9.get("blockingFindingCount") != 0 or \
                d9_review.get("blockingFindings") != []:
            raise AuthorityError("D9 v1.13 PASS binding drift")
        subjects = d9_review.get("reviewBinding", {}).get("exactSubjects", [])
        observed = {row.get("path"): row.get("sha256") for row in subjects
                    if isinstance(row, dict)}
        if observed != {D9: PINS[D9], D9_CHECKER: PINS[D9_CHECKER]}:
            raise AuthorityError("D9 exact review subjects drift")

    def _execute_verified(self, name: str) -> types.ModuleType:
        source = self.buffers[name]
        module = types.ModuleType("verified_" + name.replace(".", "_").replace("-", "_"))
        module.__file__ = f"<verified:{name}>"
        code = compile(source, module.__file__, "exec", dont_inherit=True, optimize=0)
        exec(code, module.__dict__)
        return module

    def end_stat_check(self) -> None:
        for name, identity in self.identities.items():
            if self._identity((HERE / name).resolve(strict=True)) != identity:
                raise AuthorityError(f"dependency metadata changed after snapshot: {name}")
        if any(count != 1 for count in self.read_counts.values()):
            raise AuthorityError("dependency was reread")


def _component(tag: int, value: str) -> bytes:
    data = value.encode("utf-8")
    return bytes([tag]) + len(data).to_bytes(4, "big") + data


def _blob(tag: int, value: bytes) -> bytes:
    return bytes([tag]) + len(value).to_bytes(4, "big") + value


def encode_raw_key(item: Mapping[str, str]) -> bytes:
    return _blob(
        0x75,
        _component(0x76, item["recordCasRef"])
        + _component(0x77, item["projectId"])
        + _component(0x78, item["recordKind"]),
    )


def _object_refs_blob(object_refs: list[dict[str, str]]) -> bytes:
    rows = sorted(encode_raw_key(item) for item in object_refs)
    if len(rows) != len(set(rows)):
        raise ValueError("duplicate raw object key")
    return _blob(0x79, b"".join(rows))


def derive_unit_id(project_id: str, capability: str,
                   object_refs: list[dict[str, str]]) -> str:
    preimage = (
        b"opensip.semantic-custody-unit-id.v3\x00\x70"
        + _component(0x72, project_id)
        + _component(0x74, capability)
        + _object_refs_blob(object_refs)
    )
    return "unit3:sha256:" + sha256(preimage)


def encode_unit(unit: Mapping[str, Any]) -> bytes:
    return (
        b"\x70" + _component(0x71, unit["unitId"])
        + _component(0x72, unit["projectId"])
        + _component(0x74, unit["requiredForCapability"])
        + _object_refs_blob(unit["objectRefs"])
    )


def _merkle(items: list[bytes]) -> bytes:
    ordered = sorted(set(items))
    if not ordered:
        return hashlib.sha256(b"\x02" + _blob(0x30, b"opensip.evaluation-proof.v2")).digest()
    level = [hashlib.sha256(b"\x00" + len(item).to_bytes(8, "big") + item).digest()
             for item in ordered]
    while len(level) > 1:
        level = [
            hashlib.sha256(b"\x01" + level[index] + level[index + 1]).digest()
            if index + 1 < len(level) else level[index]
            for index in range(0, len(level), 2)
        ]
    return level[0]


def semantic_closure_commitment(units: list[dict[str, Any]]) -> str:
    root = _merkle([encode_unit(unit) for unit in units])
    preimage = (
        b"\x30" + _blob(0x31, b"opensip.evaluation-proof.v2")
        + _blob(0x32, b"semantic-capability-closure-v3")
        + _blob(0x33, root)
    )
    return cas(preimage)


def derive_operational_projection(
        closure: dict[str, Any], source_bundle_ref: str,
        source_closure_ref: str) -> tuple[dict[str, Any], bytes, str, str]:
    units: list[dict[str, Any]] = []
    for source in closure["units"]:
        refs = sorted(copy.deepcopy(source["objectRefs"]), key=encode_raw_key)
        units.append({
            "unitId": source["unitId"], "projectId": source["projectId"],
            "requiredForCapability": source["requiredForCapability"],
            "objectRefs": refs,
        })
    units.sort(key=encode_unit)
    unique: dict[tuple[str, str, str], dict[str, str]] = {}
    for unit in units:
        for row in unit["objectRefs"]:
            key = row["projectId"], row["recordCasRef"], row["recordKind"]
            if key in unique:
                raise ValueError("operational projection has duplicate unit owner")
            unique[key] = copy.deepcopy(row)
    required = sorted(unique.values(), key=encode_raw_key)
    projection = {
        "schemaVersion": 1,
        "projectId": closure["projectId"],
        "sourceEvaluationProofBundleCasRef": source_bundle_ref,
        "sourceSemanticCapabilityClosureCasRef": source_closure_ref,
        "sourceSemanticCapabilityClosureCommitment": closure["closureCommitment"],
        "normalizationAlgorithm": "OPEN-SIP-OPERATIONAL-CUSTODY-KEY-ORDER-V1",
        "operationalUnits": units,
        "requiredObjectRefs": required,
    }
    encoded = compact(projection)
    return projection, encoded, cas(encoded), domain_digest(
        "opensip.operational-custody-projection.v1", encoded,
    )


RECORD_TYPES: dict[str, dict[str, Any]] = {
    "source-bytes": {
        "expectedValueType": "FixtureSourceBytesRecordV1",
        "selector": "/sourcePath", "idField": "sourcePath",
        "selectedValueType": "FixtureSourcePathV1",
    },
    "predicate-semantics": {
        "expectedValueType": "FixturePredicateSemanticsRecordV1",
        "selector": "/predicateId", "idField": "predicateId",
        "selectedValueType": "FixturePredicateIdV1",
    },
    "policy": {
        "expectedValueType": "FixturePolicyRecordV1",
        "selector": "/policyId", "idField": "policyId",
        "selectedValueType": "FixturePolicyIdV1",
    },
    "fact": {
        "expectedValueType": "FixtureFactRecordV1",
        "selector": "/factId", "idField": "factId",
        "selectedValueType": "FixtureFactIdV1",
    },
    "coverage": {
        "expectedValueType": "FixtureCoverageRecordV1",
        "selector": "/coverageId", "idField": "coverageId",
        "selectedValueType": "FixtureCoverageIdV1",
    },
    "replay-plan": {
        "expectedValueType": "FixtureReplayPlanRecordV1",
        "selector": "/planId", "idField": "planId",
        "selectedValueType": "FixtureReplayPlanIdV1",
    },
    "resolved-activation-graph": {
        "expectedValueType": "FixtureResolvedActivationGraphRecordV1",
        "selector": "/graphId", "idField": "graphId",
        "selectedValueType": "FixtureGraphIdV1",
    },
}
RECORD_COMMON_PREFIX = ["schemaVersion", "projectId", "recordKind"]
RECORD_COMMON_SUFFIX = [
    "requiredCapability", "unitLabel", "dependencies", "payload",
]
DEPENDENCY_FIELDS = ["projectId", "recordCasRef", "recordKind", "role"]
REQUEST_FIELDS = [
    "projectId", "recordCasRef", "recordKind", "expectedValueType",
    "selector", "requiredCapability",
]
RESULT_FIELDS = [
    "schemaVersion", "kind", "projectId", "recordCasRef", "recordKind",
    "expectedValueType", "selector", "requiredCapability",
    "validatedByteLength", "validatedDigest", "validatedBytesHex",
    "selectedValueType", "selectedValue",
]


def _closed_object(value: Any, fields: list[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or list(value) != fields:
        raise ResolutionError("CLOSED_TYPE_MISMATCH", f"{label} ordered fields")
    return value


def validate_raw_object_resolution(raw_bytes: Any, request: Any) -> dict[str, Any]:
    """Pure RawObjectResolutionConformanceV1 validation in normative order."""
    if type(raw_bytes) is not bytes or len(raw_bytes) == 0:
        raise ResolutionError("BYTES_NOT_PRESENT", "nonempty immutable bytes required")

    # Length and digest are computed before any parse or selector use.  The
    # bounded UInt64 length and digest-to-CAS equality are the complete physical
    # integrity gate for this API; no identity or receipt substitutes for bytes.
    length = len(raw_bytes)
    if length > 2**64 - 1:
        raise ResolutionError("BYTE_LENGTH_INVALID", "length exceeds UInt64")
    digest = sha256(raw_bytes)
    if not isinstance(request, dict) or list(request) != REQUEST_FIELDS:
        raise ResolutionError("REQUEST_SHAPE_MISMATCH", "closed request fields")
    expected_ref = request.get("recordCasRef")
    if not isinstance(expected_ref, str) or not REF_RE.fullmatch(expected_ref) or \
            expected_ref != "sha256:" + digest:
        raise ResolutionError("CAS_MISMATCH", "SHA-256(raw bytes) differs from recordCasRef")

    try:
        record = parse_json_bytes(raw_bytes, "RawObjectResolutionConformanceV1 bytes")
    except (DuplicateKeyError, FloatForbidden, ValueError, json.JSONDecodeError) as exc:
        raise ResolutionError("CLOSED_TYPE_MISMATCH", type(exc).__name__) from exc
    kind = request.get("recordKind")
    declaration = RECORD_TYPES.get(kind) if isinstance(kind, str) else None
    if declaration is None:
        raise ResolutionError("CLOSED_TYPE_MISMATCH", "record kind is not registered")
    fields = RECORD_COMMON_PREFIX + [declaration["idField"]] + RECORD_COMMON_SUFFIX
    _closed_object(record, fields, "record")
    if record.get("schemaVersion") != 1 or type(record.get("schemaVersion")) is not int:
        raise ResolutionError("CLOSED_TYPE_MISMATCH", "schemaVersion")
    if not all(isinstance(record.get(key), str) for key in (
            "projectId", "recordKind", declaration["idField"],
            "requiredCapability", "unitLabel", "payload")):
        raise ResolutionError("CLOSED_TYPE_MISMATCH", "record scalar types")
    dependencies = record.get("dependencies")
    if not isinstance(dependencies, list):
        raise ResolutionError("CLOSED_TYPE_MISMATCH", "dependencies array")
    for index, dependency in enumerate(dependencies):
        _closed_object(dependency, DEPENDENCY_FIELDS, f"dependency[{index}]")
        if not all(isinstance(dependency.get(key), str) for key in DEPENDENCY_FIELDS):
            raise ResolutionError("CLOSED_TYPE_MISMATCH", "dependency scalar types")
        if not PROJECT_RE.fullmatch(dependency["projectId"]) or \
                not REF_RE.fullmatch(dependency["recordCasRef"]):
            raise ResolutionError("CLOSED_TYPE_MISMATCH", "dependency identity")

    if request.get("expectedValueType") != declaration["expectedValueType"]:
        raise ResolutionError("EXPECTED_TYPE_MISMATCH", "closed type name")
    if request.get("selector") != declaration["selector"]:
        raise ResolutionError("SELECTOR_MISMATCH", "record-specific selector")
    if request.get("projectId") != record["projectId"]:
        raise ResolutionError("PROJECT_MISMATCH", "projectId")
    if request.get("recordKind") != record["recordKind"]:
        raise ResolutionError("RECORD_KIND_MISMATCH", "recordKind")
    if request.get("requiredCapability") != record["requiredCapability"]:
        raise ResolutionError("CAPABILITY_MISMATCH", "requiredCapability")
    selected = record[declaration["idField"]]
    return {
        "schemaVersion": 1,
        "kind": "RAW_OBJECT_USABLE",
        "projectId": request["projectId"],
        "recordCasRef": request["recordCasRef"],
        "recordKind": request["recordKind"],
        "expectedValueType": request["expectedValueType"],
        "selector": request["selector"],
        "requiredCapability": request["requiredCapability"],
        "validatedByteLength": length,
        "validatedDigest": "sha256:" + digest,
        "validatedBytesHex": raw_bytes.hex(),
        "selectedValueType": declaration["selectedValueType"],
        "selectedValue": selected,
    }


def raw_key(project_id: str, record_ref: str, record_kind: str) -> dict[str, str]:
    return {
        "projectId": project_id,
        "recordCasRef": record_ref,
        "recordKind": record_kind,
    }


def _semantic_ref(domain: str, raw_bytes: bytes) -> str:
    return domain_digest("opensip.rt15.fixture-semantic-binding.v1/" + domain, raw_bytes)


def _raw_bytes_commitment(rows: list[dict[str, Any]]) -> str:
    framed = b"".join(
        len(bytes.fromhex(row["rawBytesHex"])).to_bytes(8, "big")
        + bytes.fromhex(row["rawBytesHex"])
        for row in sorted(rows, key=lambda item: item["request"]["recordCasRef"])
    )
    return domain_digest("opensip.rt15.raw-object-bytes-closure.v1", framed)


def build_fixture(fixture_id: str, project_id: str,
                  specs: list[dict[str, Any]]) -> dict[str, Any]:
    if not specs:
        raise ValueError("fixture requires records")
    built: dict[str, dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []
    for spec in specs:
        name = spec["name"]
        kind = spec["kind"]
        declaration = RECORD_TYPES[kind]
        dependencies: list[dict[str, str]] = []
        for dependency_name, role in spec.get("dependencies", []):
            if dependency_name not in built:
                raise ValueError("fixture specifications must be topological")
            target = built[dependency_name]
            dependencies.append({
                **raw_key(project_id, target["recordCasRef"], target["recordKind"]),
                "role": role,
            })
        record = {
            "schemaVersion": 1,
            "projectId": project_id,
            "recordKind": kind,
            declaration["idField"]: spec["selectedValue"],
            "requiredCapability": spec["capability"],
            "unitLabel": spec["unitLabel"],
            "dependencies": dependencies,
            "payload": spec["payload"],
        }
        raw_bytes = compact(record)
        record_ref = cas(raw_bytes)
        request = {
            "projectId": project_id,
            "recordCasRef": record_ref,
            "recordKind": kind,
            "expectedValueType": declaration["expectedValueType"],
            "selector": declaration["selector"],
            "requiredCapability": spec["capability"],
        }
        result = validate_raw_object_resolution(raw_bytes, request)
        row = {
            "request": request,
            "rawBytesHex": raw_bytes.hex(),
            "expectedResult": result,
            "dependencies": copy.deepcopy(dependencies),
        }
        rows.append(row)
        built[name] = {
            "name": name, "recordCasRef": record_ref, "recordKind": kind,
            "capability": spec["capability"], "unitLabel": spec["unitLabel"],
            "root": bool(spec.get("root")), "rawBytes": raw_bytes,
            "selectedValue": spec["selectedValue"],
        }

    graph: list[dict[str, str]] = []
    for row in rows:
        for dependency in row["dependencies"]:
            graph.append({
                "fromRef": row["request"]["recordCasRef"],
                "toRef": dependency["recordCasRef"],
                "projectId": project_id,
                "role": dependency["role"],
            })
    graph.sort(key=lambda edge: (
        edge["fromRef"], edge["toRef"], edge["projectId"], edge["role"],
    ))

    proof_refs = [{
        "identityKind": "raw-cas",
        "projectId": project_id,
        "recordCasRef": item["recordCasRef"],
        "recordKind": item["recordKind"],
        "requiredForCapability": item["capability"],
    } for item in built.values()]
    proof_refs.sort(key=lambda item: encode_raw_key(item))

    groups: dict[tuple[str, str], list[dict[str, str]]] = {}
    for item in built.values():
        groups.setdefault((item["capability"], item["unitLabel"]), []).append(
            raw_key(project_id, item["recordCasRef"], item["recordKind"]),
        )
    units: list[dict[str, Any]] = []
    for (capability, _label), refs in groups.items():
        ordered_refs = sorted(refs, key=encode_raw_key)
        units.append({
            "unitId": derive_unit_id(project_id, capability, ordered_refs),
            "projectId": project_id,
            "requiredForCapability": capability,
            "objectRefs": ordered_refs,
        })
    units.sort(key=encode_unit)

    bindings: list[dict[str, str]] = []
    roots: list[dict[str, str]] = []
    for item in built.values():
        if not item["root"]:
            continue
        domain = "rt15-fixture-" + item["recordKind"] + "-v1"
        semantic_ref = _semantic_ref(domain, item["rawBytes"])
        bindings.append({
            "projectId": project_id, "semanticDomain": domain,
            "semanticRef": semantic_ref, "recordCasRef": item["recordCasRef"],
            "recordKind": item["recordKind"],
        })
        roots.append({
            "identityKind": "semantic-commitment", "projectId": project_id,
            "semanticDomain": domain, "semanticRef": semantic_ref,
            "recordKind": item["recordKind"],
            "requiredForCapability": item["capability"],
        })
    bindings.sort(key=lambda item: compact(item, sort_keys=True))
    roots.sort(key=lambda item: compact(item, sort_keys=True))
    commitment = semantic_closure_commitment(units)
    closure = {
        "schemaVersion": 3,
        "projectId": project_id,
        "sealedCapability": "replayable",
        "semanticObjectBindings": bindings,
        "semanticRoots": roots,
        "proofRefs": proof_refs,
        "dependencyEdges": graph,
        "units": units,
        "closureCommitment": commitment,
    }
    closure_bytes = compact(closure, sort_keys=True)
    closure_ref = cas(closure_bytes)

    run_id = "run1:" + sha256(("opensip.rt15.fixture-run.v1\x00" + fixture_id).encode())
    availability = []
    for unit in units:
        availability.append({
            "schemaVersion": 2, "projectId": project_id, "runId": run_id,
            "unitId": unit["unitId"],
            "objectStates": [{**copy.deepcopy(key), "state": "AVAILABLE"}
                             for key in unit["objectRefs"]],
        })
    availability_fixtures = [{
        "id": fixture_id + "-ALL-AVAILABLE", "runId": run_id,
        "stateOverrides": [], "expectedEffectiveCapability": "replayable",
    }]
    availability_sha = sha256(compact({
        "unitAvailabilityRecords": availability,
        "availabilityFixtures": availability_fixtures,
    }, sort_keys=True))

    proof_bundle = {
        "schemaVersion": 1, "projectId": project_id,
        "proofRefs": proof_refs, "dependencyEdges": graph,
        "semanticRoots": roots,
    }
    proof_bundle_bytes = compact(proof_bundle, sort_keys=True)
    proof_bundle_ref = cas(proof_bundle_bytes)
    projection, projection_bytes, projection_ref, projection_digest = \
        derive_operational_projection(closure, proof_bundle_ref, closure_ref)

    snapshot_records = [{
        "recordCasRef": row["request"]["recordCasRef"],
        "rawBytesHex": row["rawBytesHex"],
    } for row in rows]
    snapshot_preimage = compact(snapshot_records, sort_keys=True)
    snapshot_id = "snapshot1:sha256:" + sha256(
        b"opensip.rt15.raw-object-snapshot.v1\x00"
        + len(snapshot_preimage).to_bytes(8, "big") + snapshot_preimage,
    )
    snapshot = {
        "schemaVersion": 1, "snapshotId": snapshot_id,
        "projectId": project_id, "records": snapshot_records,
    }
    commitment_input = {
        "proofBundleCasRef": proof_bundle_ref,
        "semanticClosureCasRef": closure_ref,
        "semanticClosureCommitment": commitment,
        "availabilityCanonicalSha256": availability_sha,
        "operationalProjectionRef": projection_ref,
        "operationalProjectionDigest": projection_digest,
        "rawObjectSnapshotId": snapshot_id,
    }
    commitments = {
        "rawBytesCommitment": _raw_bytes_commitment(rows),
        "fixtureCommitment": domain_digest(
            "opensip.rt15.raw-object-resolution-fixture.v1",
            compact(commitment_input, sort_keys=True),
        ),
    }
    return {
        "fixtureId": fixture_id,
        "status": "FIXTURE-ONLY/NEW-BYTE-DERIVED/NOT-RT13-NOMATCH",
        "projectId": project_id,
        "recordCount": len(rows),
        "unitCount": len(units),
        "resolutionRows": rows,
        "dependencyGraph": graph,
        "proofBundleCanonicalBytesHex": proof_bundle_bytes.hex(),
        "proofBundleCasRef": proof_bundle_ref,
        "semanticClosure": closure,
        "semanticClosureCanonicalBytesHex": closure_bytes.hex(),
        "semanticClosureCasRef": closure_ref,
        "unitAvailabilityRecords": availability,
        "availabilityFixtures": availability_fixtures,
        "availabilityCanonicalSha256": availability_sha,
        "operationalProjection": projection,
        "operationalProjectionCanonicalBytesHex": projection_bytes.hex(),
        "operationalProjectionRef": projection_ref,
        "operationalProjectionDigest": projection_digest,
        "rawObjectSnapshot": snapshot,
        "commitments": commitments,
    }


PRIMARY_SPECS = [
    {"name": "source", "kind": "source-bytes", "selectedValue": "src/rt15_fixture.rs",
     "capability": "replayable", "unitLabel": "replay", "dependencies": [],
     "payload": "pub fn rt15_fixture() -> bool { true }"},
    {"name": "predicate", "kind": "predicate-semantics", "selectedValue": "pred:rt15-byte-custody",
     "capability": "verifiable", "unitLabel": "verify", "dependencies": [],
     "payload": "all selected raw objects validate before semantic use"},
    {"name": "policy", "kind": "policy", "selectedValue": "policy:rt15-exact-bytes",
     "capability": "verifiable", "unitLabel": "verify",
     "dependencies": [("predicate", "predicate-semantics")],
     "payload": "identity-only retained objects are unusable"},
    {"name": "fact", "kind": "fact", "selectedValue": "fact:rt15-source-present",
     "capability": "verifiable", "unitLabel": "verify",
     "dependencies": [("source", "source-content")],
     "payload": "fixture source bytes are present"},
    {"name": "coverage", "kind": "coverage", "selectedValue": "coverage:rt15-byte-closure",
     "capability": "verifiable", "unitLabel": "verify",
     "dependencies": [("fact", "coverage-fact"), ("predicate", "coverage-predicate")],
     "payload": "predicate and source fact are covered", "root": True},
    {"name": "replay", "kind": "replay-plan", "selectedValue": "plan:rt15-replay",
     "capability": "replayable", "unitLabel": "replay",
     "dependencies": [("source", "replay-source"), ("policy", "replay-policy")],
     "payload": "replay from exact selected bytes"},
    {"name": "graph", "kind": "resolved-activation-graph", "selectedValue": "graph:rt15-primary",
     "capability": "replayable", "unitLabel": "replay",
     "dependencies": [("coverage", "activation-coverage"), ("replay", "activation-replay")],
     "payload": "complete primary fixture graph", "root": True},
]

ALTERNATE_SPECS = [
    {"name": "source", "kind": "source-bytes", "selectedValue": "src/rt15_alt.rs",
     "capability": "replayable", "unitLabel": "replay-a", "dependencies": [],
     "payload": "pub const ALT: u8 = 15;"},
    {"name": "predicate", "kind": "predicate-semantics", "selectedValue": "pred:rt15-alt",
     "capability": "verifiable", "unitLabel": "verify", "dependencies": [],
     "payload": "alternate fixture predicate"},
    {"name": "fact", "kind": "fact", "selectedValue": "fact:rt15-alt",
     "capability": "verifiable", "unitLabel": "verify",
     "dependencies": [("predicate", "fact-predicate")],
     "payload": "alternate fixture fact", "root": True},
    {"name": "replay", "kind": "replay-plan", "selectedValue": "plan:rt15-alt",
     "capability": "replayable", "unitLabel": "replay-a",
     "dependencies": [("source", "replay-source"), ("fact", "replay-fact")],
     "payload": "alternate replay plan"},
    {"name": "graph", "kind": "resolved-activation-graph", "selectedValue": "graph:rt15-alt",
     "capability": "replayable", "unitLabel": "replay-b",
     "dependencies": [("replay", "activation-replay"), ("predicate", "activation-predicate")],
     "payload": "alternate fixture graph", "root": True},
]


def synthetic_specs(record_count: int, unit_count: int) -> list[dict[str, Any]]:
    if record_count < unit_count or unit_count < 1:
        raise ValueError("invalid generated fixture cardinality")
    kinds = list(RECORD_TYPES)
    specs: list[dict[str, Any]] = []
    for index in range(record_count):
        kind = kinds[index % len(kinds)]
        declaration = RECORD_TYPES[kind]
        group_index = index % unit_count
        capability = "verifiable" if group_index % 2 == 0 else "replayable"
        dependencies = [] if index == 0 else [(f"r{index - 1}", "generated-parent")]
        specs.append({
            "name": f"r{index}", "kind": kind,
            "selectedValue": f"{declaration['idField']}:generated:{record_count}:{index}",
            "capability": capability, "unitLabel": f"unit-{group_index}",
            "dependencies": dependencies,
            "payload": f"generated payload {record_count}/{unit_count}/{index}",
            "root": index >= max(0, record_count - 2),
        })
    return specs


RAW_OBJECT_STATES = {
    "AVAILABLE", "OUTAGE", "PURGED", "EXPIRED", "CORRUPT",
    "MISSING-DEPENDENCY",
}
LEASE_STATES = {"HELD", "RELEASED", "RECLAIMED_STALE"}
STATE_FIELDS = [
    "schemaVersion", "projectId", "ledgerSequence",
    "lastIssuedFencingToken", "objects", "lease",
]
OBJECT_STATE_FIELDS = ["projectId", "state", "recordCasRef", "recordKind"]
LEASE_FIELDS = [
    "leaseId", "projectId", "ownerId", "ownerLivenessToken", "ownerAlive",
    "previousFencingToken", "fencingToken", "state", "acquiredAtSequence",
    "expiresAtSequence", "pinnedRefs", "pendingExpiryRefs",
]
EVENT_FIELDS: dict[str, list[str]] = {
    "expiry": ["kind", "projectId", "transactionBoundary", "atSequence", "targetRefs"],
    "release": ["kind", "projectId", "transactionBoundary", "atSequence",
                "leaseId", "ownerId", "fencingToken"],
    "crash-reclaim": [
        "kind", "projectId", "transactionBoundary", "atSequence", "leaseId",
        "expectedOwnerId", "expectedOwnerLivenessToken", "expectedFencingToken",
        "successorFencingToken", "scopeRefs", "observedOwnerAlive",
    ],
    "resolve-and-pin": [
        "kind", "projectId", "transactionBoundary", "atSequence", "leaseId",
        "ownerId", "ownerLivenessToken", "expectedPreviousFencingToken",
        "expiresAtSequence", "pinRefs",
    ],
}
RESULT_VARIANT_FIELDS: dict[str, list[str]] = {
    "LEASE_GRANTED": ["kind", "leaseId", "fencingToken", "idempotent"],
    "READ_CONTINUES": ["kind"],
    "EXPIRY_COMMITTED": ["kind", "expiredRefs"],
    "LEASE_RELEASED": ["kind", "leaseState", "expiryAppliedRefs"],
    "LEASE_RECLAIMED": ["kind", "leaseId", "leaseState", "expiryAppliedRefs"],
    "RETENTION_PRECONDITION_FAILED": ["kind"],
    "RETENTION_BUSY": ["kind"],
    "RETENTION_LOCAL_UNAVAILABLE": ["kind"],
}


def _validate_key(value: Any, project_id: str, label: str) -> dict[str, Any]:
    _closed_object(value, ["projectId", "recordCasRef", "recordKind"], label)
    if value["projectId"] != project_id or not REF_RE.fullmatch(value["recordCasRef"]) or \
            not isinstance(value["recordKind"], str) or not value["recordKind"]:
        raise ValueError(f"{label}: invalid raw object key")
    return value


def _validate_key_array(value: Any, project_id: str, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ValueError(f"{label}: expected array")
    seen: set[tuple[str, str, str]] = set()
    for index, row in enumerate(value):
        _validate_key(row, project_id, f"{label}[{index}]")
        key = row["projectId"], row["recordCasRef"], row["recordKind"]
        if key in seen:
            raise ValueError(f"{label}: duplicate key")
        seen.add(key)
    return value


def _validate_lease_state(state: Any) -> dict[str, Any]:
    _closed_object(state, STATE_FIELDS, "LeaseStateV3")
    if state["schemaVersion"] != 3 or type(state["schemaVersion"]) is not int:
        raise ValueError("LeaseStateV3 schemaVersion")
    project_id = state["projectId"]
    if not isinstance(project_id, str) or not PROJECT_RE.fullmatch(project_id):
        raise ValueError("LeaseStateV3 projectId")
    for field in ("ledgerSequence", "lastIssuedFencingToken"):
        if type(state[field]) is not int or state[field] < 0 or state[field] > 2**64 - 1:
            raise ValueError(f"LeaseStateV3 {field}")
    if not isinstance(state["objects"], list):
        raise ValueError("LeaseStateV3 objects")
    seen: set[tuple[str, str, str]] = set()
    for index, row in enumerate(state["objects"]):
        _closed_object(row, OBJECT_STATE_FIELDS, f"objects[{index}]")
        _validate_key({key: row[key] for key in ("projectId", "recordCasRef", "recordKind")},
                      project_id, f"objects[{index}]")
        if row["state"] not in RAW_OBJECT_STATES:
            raise ValueError("RawObjectStateV1 state")
        key = row["projectId"], row["recordCasRef"], row["recordKind"]
        if key in seen:
            raise ValueError("duplicate object state")
        seen.add(key)
    lease = state["lease"]
    if lease is not None:
        _closed_object(lease, LEASE_FIELDS, "LeaseRecordV2")
        if lease["projectId"] != project_id or lease["state"] not in LEASE_STATES or \
                type(lease["ownerAlive"]) is not bool:
            raise ValueError("LeaseRecordV2 project/state/ownerAlive")
        for field in ("previousFencingToken", "fencingToken", "acquiredAtSequence",
                      "expiresAtSequence"):
            if type(lease[field]) is not int or lease[field] < 0:
                raise ValueError(f"LeaseRecordV2 {field}")
        for field in ("leaseId", "ownerId", "ownerLivenessToken"):
            if not isinstance(lease[field], str) or not lease[field]:
                raise ValueError(f"LeaseRecordV2 {field}")
        _validate_key_array(lease["pinnedRefs"], project_id, "pinnedRefs")
        _validate_key_array(lease["pendingExpiryRefs"], project_id, "pendingExpiryRefs")
    return state


def _validate_event(event: Any, project_id: str, next_sequence: int) -> dict[str, Any]:
    if not isinstance(event, dict) or event.get("kind") not in EVENT_FIELDS:
        raise ValueError("unknown or malformed semantic lease event")
    kind = event["kind"]
    _closed_object(event, EVENT_FIELDS[kind], kind)
    if event["projectId"] != project_id or \
            event["transactionBoundary"] != TX_BOUNDARY or \
            type(event["atSequence"]) is not int or event["atSequence"] != next_sequence:
        raise ValueError("event project/transaction/sequence")
    array_field = {
        "expiry": "targetRefs", "release": None,
        "crash-reclaim": "scopeRefs", "resolve-and-pin": "pinRefs",
    }[kind]
    if array_field:
        _validate_key_array(event[array_field], project_id, array_field)
    integer_fields = {
        "expiry": [], "release": ["fencingToken"],
        "crash-reclaim": ["expectedFencingToken", "successorFencingToken"],
        "resolve-and-pin": ["expectedPreviousFencingToken", "expiresAtSequence"],
    }[kind]
    for field in integer_fields:
        if type(event[field]) is not int or event[field] < 0:
            raise ValueError(f"event {field}")
    if kind == "crash-reclaim" and type(event["observedOwnerAlive"]) is not bool:
        raise ValueError("event observedOwnerAlive")
    return event


def _key_tuple(row: Mapping[str, Any]) -> tuple[str, str, str]:
    return row["projectId"], row["recordCasRef"], row["recordKind"]


def _failure(prestate: dict[str, Any], kind: str) -> dict[str, Any]:
    return {"schemaVersion": 3, "state": copy.deepcopy(prestate), "result": {"kind": kind}}


def reduce_semantic_lease_v3(state: Any, event: Any) -> dict[str, Any]:
    _validate_lease_state(state)
    _validate_event(event, state["projectId"], state["ledgerSequence"] + 1)
    current = copy.deepcopy(state)
    objects = {_key_tuple(row): row for row in current["objects"]}
    lease = current["lease"]
    kind = event["kind"]

    if kind == "resolve-and-pin":
        requested = {_key_tuple(row) for row in event["pinRefs"]}
        if lease is not None and lease["state"] == "HELD":
            same = (
                lease["leaseId"] == event["leaseId"]
                and lease["ownerId"] == event["ownerId"]
                and lease["ownerLivenessToken"] == event["ownerLivenessToken"]
                and lease["previousFencingToken"] == event["expectedPreviousFencingToken"]
                and lease["expiresAtSequence"] == event["expiresAtSequence"]
                and {_key_tuple(row) for row in lease["pinnedRefs"]} == requested
            )
            if same:
                return {"schemaVersion": 3, "state": current, "result": {
                    "kind": "LEASE_GRANTED", "leaseId": lease["leaseId"],
                    "fencingToken": lease["fencingToken"], "idempotent": True,
                }}
            return _failure(state, "RETENTION_PRECONDITION_FAILED")
        if event["expectedPreviousFencingToken"] != current["lastIssuedFencingToken"] or \
                event["expiresAtSequence"] <= event["atSequence"]:
            return _failure(state, "RETENTION_PRECONDITION_FAILED")
        if any(key not in objects or objects[key]["state"] != "AVAILABLE"
               for key in requested):
            return _failure(state, "RETENTION_LOCAL_UNAVAILABLE")
        next_fence = current["lastIssuedFencingToken"] + 1
        if next_fence > 2**64 - 1:
            return _failure(state, "RETENTION_PRECONDITION_FAILED")
        current["ledgerSequence"] = event["atSequence"]
        current["lastIssuedFencingToken"] = next_fence
        current["lease"] = {
            "leaseId": event["leaseId"], "projectId": event["projectId"],
            "ownerId": event["ownerId"],
            "ownerLivenessToken": event["ownerLivenessToken"],
            "ownerAlive": True,
            "previousFencingToken": event["expectedPreviousFencingToken"],
            "fencingToken": next_fence, "state": "HELD",
            "acquiredAtSequence": event["atSequence"],
            "expiresAtSequence": event["expiresAtSequence"],
            "pinnedRefs": copy.deepcopy(event["pinRefs"]),
            "pendingExpiryRefs": [],
        }
        return {"schemaVersion": 3, "state": current, "result": {
            "kind": "LEASE_GRANTED", "leaseId": event["leaseId"],
            "fencingToken": next_fence, "idempotent": False,
        }}

    if kind == "expiry":
        targets = {_key_tuple(row) for row in event["targetRefs"]}
        current["ledgerSequence"] = event["atSequence"]
        if lease is not None and lease["state"] == "HELD" and \
                targets & {_key_tuple(row) for row in lease["pinnedRefs"]}:
            existing = {_key_tuple(row) for row in lease["pendingExpiryRefs"]}
            lease["pendingExpiryRefs"] += [
                copy.deepcopy(row) for row in event["targetRefs"]
                if _key_tuple(row) not in existing
            ]
            return {"schemaVersion": 3, "state": current,
                    "result": {"kind": "READ_CONTINUES"}}
        for target in targets:
            if target in objects:
                objects[target]["state"] = "EXPIRED"
        return {"schemaVersion": 3, "state": current, "result": {
            "kind": "EXPIRY_COMMITTED",
            "expiredRefs": copy.deepcopy(event["targetRefs"]),
        }}

    if kind == "release":
        if lease is None or lease["state"] != "HELD" or \
                lease["leaseId"] != event["leaseId"] or \
                lease["ownerId"] != event["ownerId"] or \
                lease["fencingToken"] != event["fencingToken"]:
            return _failure(state, "RETENTION_PRECONDITION_FAILED")
        applied = copy.deepcopy(lease["pendingExpiryRefs"])
        for row in applied:
            if _key_tuple(row) in objects:
                objects[_key_tuple(row)]["state"] = "EXPIRED"
        lease["state"] = "RELEASED"
        lease["pendingExpiryRefs"] = []
        current["ledgerSequence"] = event["atSequence"]
        return {"schemaVersion": 3, "state": current, "result": {
            "kind": "LEASE_RELEASED", "leaseState": "RELEASED",
            "expiryAppliedRefs": applied,
        }}

    if kind == "crash-reclaim":
        scope = {_key_tuple(row) for row in event["scopeRefs"]}
        if lease is None or lease["state"] != "HELD" or \
                event["leaseId"] != lease["leaseId"] or \
                event["expectedOwnerId"] != lease["ownerId"] or \
                event["expectedOwnerLivenessToken"] != lease["ownerLivenessToken"] or \
                event["expectedFencingToken"] != lease["fencingToken"] or \
                event["successorFencingToken"] != event["expectedFencingToken"] + 1 or \
                event["successorFencingToken"] > 2**64 - 1 or \
                scope != {_key_tuple(row) for row in lease["pinnedRefs"]} or \
                event["observedOwnerAlive"] is not False or \
                event["atSequence"] < lease["expiresAtSequence"]:
            return _failure(state, "RETENTION_PRECONDITION_FAILED")
        applied = copy.deepcopy(lease["pendingExpiryRefs"])
        for row in applied:
            if _key_tuple(row) in objects:
                objects[_key_tuple(row)]["state"] = "EXPIRED"
        reclaimed_id = lease["leaseId"]
        current["lastIssuedFencingToken"] = event["successorFencingToken"]
        current["lease"] = None
        current["ledgerSequence"] = event["atSequence"]
        return {"schemaVersion": 3, "state": current, "result": {
            "kind": "LEASE_RECLAIMED", "leaseId": reclaimed_id,
            "leaseState": "RECLAIMED_STALE", "expiryAppliedRefs": applied,
        }}
    raise ValueError("unreachable event kind")


def is_retention_local_unavailable_v1(output: Any) -> bool:
    if not isinstance(output, dict) or list(output) != ["schemaVersion", "state", "result"] or \
            output.get("schemaVersion") != 3 or not isinstance(output.get("result"), dict):
        raise ValueError("invalid SemanticLeaseOutputV3")
    result = output["result"]
    kind = result.get("kind")
    if kind not in RESULT_VARIANT_FIELDS or list(result) != RESULT_VARIANT_FIELDS[kind]:
        raise ValueError("invalid SemanticLeaseResultV3")
    return kind == "RETENTION_LOCAL_UNAVAILABLE"


def _object_state(key: dict[str, str], state: str = "AVAILABLE") -> dict[str, str]:
    return {
        "projectId": key["projectId"], "state": state,
        "recordCasRef": key["recordCasRef"], "recordKind": key["recordKind"],
    }


def _base_state(keys: list[dict[str, str]], *, sequence: int = 10,
                fence: int = 4, lease: Any = None) -> dict[str, Any]:
    return {
        "schemaVersion": 3, "projectId": keys[0]["projectId"],
        "ledgerSequence": sequence, "lastIssuedFencingToken": fence,
        "objects": [_object_state(key) for key in keys], "lease": lease,
    }


def _held_lease(project_id: str, pinned: list[dict[str, str]], *,
                fence: int = 5, previous: int = 4, expires: int = 12,
                pending: list[dict[str, str]] | None = None) -> dict[str, Any]:
    return {
        "leaseId": "lease1:11111111111111111111111111111111",
        "projectId": project_id,
        "ownerId": "owner1:22222222222222222222222222222222",
        "ownerLivenessToken": "live1:33333333333333333333333333333333",
        "ownerAlive": True, "previousFencingToken": previous,
        "fencingToken": fence, "state": "HELD", "acquiredAtSequence": 7,
        "expiresAtSequence": expires, "pinnedRefs": copy.deepcopy(pinned),
        "pendingExpiryRefs": copy.deepcopy(pending or []),
    }


def lease_goldens(primary: dict[str, Any]) -> list[dict[str, Any]]:
    keys = [copy.deepcopy(unit) for unit in
            primary["operationalProjection"]["requiredObjectRefs"][:3]]
    project = primary["projectId"]
    grant_state = _base_state(keys, sequence=10, fence=4)
    grant_event = {
        "kind": "resolve-and-pin", "projectId": project,
        "transactionBoundary": TX_BOUNDARY, "atSequence": 11,
        "leaseId": "lease1:11111111111111111111111111111111",
        "ownerId": "owner1:22222222222222222222222222222222",
        "ownerLivenessToken": "live1:33333333333333333333333333333333",
        "expectedPreviousFencingToken": 4, "expiresAtSequence": 20,
        "pinRefs": [copy.deepcopy(keys[0])],
    }
    held = _held_lease(project, [keys[0]], fence=5, previous=4, expires=20)
    held_state = _base_state(keys, sequence=11, fence=5, lease=held)
    retry_event = copy.deepcopy(grant_event)
    retry_event["atSequence"] = 12
    conflict_event = copy.deepcopy(retry_event)
    conflict_event["leaseId"] = "lease1:99999999999999999999999999999999"
    unavailable_state = _base_state(keys, sequence=10, fence=4)
    unavailable_state["objects"][0]["state"] = "EXPIRED"
    expiry_state = _base_state(
        keys, sequence=11, fence=5,
        lease=_held_lease(project, [keys[0]], fence=5, previous=4, expires=20),
    )
    expiry_event = {
        "kind": "expiry", "projectId": project,
        "transactionBoundary": TX_BOUNDARY, "atSequence": 12,
        "targetRefs": [copy.deepcopy(keys[0]), copy.deepcopy(keys[1])],
    }
    release_pending = [copy.deepcopy(keys[1]), copy.deepcopy(keys[2])]
    release_state = _base_state(
        keys, sequence=20, fence=5,
        lease=_held_lease(project, [keys[0]], fence=5, previous=4,
                          expires=20, pending=release_pending),
    )
    release_event = {
        "kind": "release", "projectId": project,
        "transactionBoundary": TX_BOUNDARY, "atSequence": 21,
        "leaseId": release_state["lease"]["leaseId"],
        "ownerId": release_state["lease"]["ownerId"], "fencingToken": 5,
    }
    reclaim_state = _base_state(
        keys, sequence=20, fence=5,
        lease=_held_lease(project, [keys[0]], fence=5, previous=4,
                          expires=21, pending=release_pending),
    )
    reclaim_event = {
        "kind": "crash-reclaim", "projectId": project,
        "transactionBoundary": TX_BOUNDARY, "atSequence": 21,
        "leaseId": reclaim_state["lease"]["leaseId"],
        "expectedOwnerId": reclaim_state["lease"]["ownerId"],
        "expectedOwnerLivenessToken": reclaim_state["lease"]["ownerLivenessToken"],
        "expectedFencingToken": 5, "successorFencingToken": 6,
        "scopeRefs": [copy.deepcopy(keys[0])], "observedOwnerAlive": False,
    }
    free_expiry_state = _base_state(keys, sequence=30, fence=6)
    free_expiry_event = {
        "kind": "expiry", "projectId": project,
        "transactionBoundary": TX_BOUNDARY, "atSequence": 31,
        "targetRefs": [copy.deepcopy(keys[2])],
    }
    bad_reclaim = copy.deepcopy(reclaim_event)
    bad_reclaim["successorFencingToken"] = 7
    cases = [
        ("SLV3-01-FRESH-GRANT", grant_state, grant_event),
        ("SLV3-02-IDEMPOTENT-GRANT", held_state, retry_event),
        ("SLV3-03-CONFLICT-PRECONDITION", held_state, conflict_event),
        ("SLV3-04-LOCAL-UNAVAILABLE", unavailable_state, grant_event),
        ("SLV3-05-EXPIRY-DEFERRED", expiry_state, expiry_event),
        ("SLV3-06-RELEASE-COMPLETE-PENDING", release_state, release_event),
        ("SLV3-07-CRASH-SUCCESSOR-FENCE", reclaim_state, reclaim_event),
        ("SLV3-08-EXPIRY-COMMITTED", free_expiry_state, free_expiry_event),
        ("SLV3-09-BAD-SUCCESSOR-REFUSES", reclaim_state, bad_reclaim),
    ]
    return [{
        "id": case_id, "preState": copy.deepcopy(prestate),
        "event": copy.deepcopy(event),
        "expectedOutput": reduce_semantic_lease_v3(prestate, event),
    } for case_id, prestate, event in cases]


def _raw_resolution_contract(primary: dict[str, Any],
                             alternate: dict[str, Any]) -> dict[str, Any]:
    registry: list[dict[str, Any]] = []
    for kind, declaration in RECORD_TYPES.items():
        registry.append({
            "recordKind": kind,
            "expectedValueType": declaration["expectedValueType"],
            "orderedFields": RECORD_COMMON_PREFIX + [declaration["idField"]]
            + RECORD_COMMON_SUFFIX,
            "selector": declaration["selector"],
            "selectedValueType": declaration["selectedValueType"],
            "dependencyOrderedFields": DEPENDENCY_FIELDS,
            "closed": True,
        })
    return {
        "type": "RawObjectResolutionConformanceV1",
        "closed": True,
        "ownership": {
            "byteReadOwner": "orchestration host or immutable content-addressed read boundary",
            "semanticValidatorOwner": "VerifiedSemanticRTSnapshotV1 pure validation API",
            "rule": "The caller supplies the exact bytes. This API cannot fetch, mutate, persist, invoke a callback, mint a receipt, or attest liveness.",
            "identitySubstitution": "A CAS identity, receipt, path, selector, snapshot id, or availability assertion without the exact bytes is never usable.",
        },
        "pureFunctionSignature": "validate_raw_object_resolution_v1(VerifiedSemanticRTSnapshotV1, RawBytes, RawObjectResolutionRequestV1) -> RawObjectResolutionResultV1",
        "requestOrderedFields": REQUEST_FIELDS,
        "requestType": {
            "projectId": "ProjectId",
            "recordCasRef": "RawCasRef",
            "recordKind": "ClosedRecordKindV1",
            "expectedValueType": "ClosedRawValueTypeV1",
            "selector": "ClosedRecordSelectorV1",
            "requiredCapability": "SemanticCapabilityV1",
        },
        "resultOrderedFields": RESULT_FIELDS,
        "validationOrder": [
            "1. require nonempty caller-supplied immutable bytes",
            "2. derive UInt64 byte length and SHA-256 digest, then require digest-derived CAS equals request.recordCasRef",
            "3. parse strict UTF-8 JSON and require the registered closed record type, ordered fields, nested dependency type, exact scalar types, and no duplicate/nonfinite/float value",
            "4. require expected value type, record-specific selector, projectId, recordKind, and requiredCapability equality",
            "5. return RAW_OBJECT_USABLE with the exact validated bytes and selected value",
        ],
        "failureRule": "Every failure is explicit and returns no usable result; no fallback, default, identity-only terminal, fetch, callback, mutation, persistence, or liveness conclusion is permitted.",
        "closedTypeRegistry": registry,
        "fixtureAlgorithm": {
            "input": "Any finite nonempty topologically ordered record specification with any positive unit cardinality not exceeding record cardinality.",
            "recordBytes": "Compact insertion-order UTF-8 JSON of the registered closed record; dependencies name only already-derived raw keys.",
            "recordCasRef": "sha256:lowercase_hex(SHA256(recordBytes))",
            "proofRefs": "One proof ref per byte-bearing record, sorted by the inherited RT13 encoded RawObjectKeyV1 bytes.",
            "units": "Group every proof ref exactly once by declared capability and fixture unit label; derive UNIT-ID-V3 from the exact grouped raw keys; no count table exists.",
            "semanticClosure": "Construct a complete SemanticCapabilityClosureV3 with byte-derived proof refs, graph, bindings, roots, units, and the inherited RT13 Merkle commitment grammar.",
            "operationalProjection": "Derive OperationalCustodyProjectionV1 from the new closure using the generic count-independent projection algorithm.",
            "snapshot": "Embed every exact raw byte vector keyed by its derived CAS; snapshot identity commits to the complete ordered byte map.",
            "forbidden": "No fixture ref may equal an old RT13 NOMATCH proof ref and no identity-only row may terminate the closure.",
        },
        "fixtureGoldens": [primary, alternate],
        "cardinalityEvidence": {
            "primary": {"recordCount": 7, "unitCount": 2},
            "differentEmbeddedShape": {"recordCount": 5, "unitCount": 3},
            "checkerGeneratedShape": {"recordCount": 9, "unitCount": 4},
            "fixedCountAssumption": "FORBIDDEN",
        },
        "oldRt13FeasibilityBoundary": {
            "rt13NomatchProofRefCount": 23,
            "identityOnlyExternalRefCount": 18,
            "forwardDiscoverablePreimageCount": 7,
            "unresolvedPatternedIdentityCount": 11,
            "forwardDiscoverableRefs": DISCOVERED_OLD_PREIMAGES,
            "unresolvedPatternedRefs": OLD_PATTERNED_REFS,
            "v6IndependentAuditSha256": "b3fa29fccb4457a29b9f1d5ea71c262270e39ddd32ac5de3a233d6320678d523",
            "v7FeasibilityReportSha256": "d31d088fc9bcde0f9b6c55e4b868b019abe8002655183708b205946a6d3a9fbe",
            "disposition": "The embedded fixtures use only new forward-derived identities. They neither recover nor replace any old RT13 NOMATCH object and make no preimage claim for the eleven patterned hashes.",
        },
        "futureConsumerBoundary": "A separately authored downstream successor may pin an exact reviewed fixture snapshot/result, but this candidate imports no downstream artifact and grants no downstream application authority.",
    }


def _operational_contract() -> dict[str, Any]:
    return {
        "type": "OperationalCustodyProjectionV1",
        "closed": True,
        "orderedFields": [
            "schemaVersion", "projectId", "sourceEvaluationProofBundleCasRef",
            "sourceSemanticCapabilityClosureCasRef",
            "sourceSemanticCapabilityClosureCommitment",
            "normalizationAlgorithm", "operationalUnits", "requiredObjectRefs",
        ],
        "sourceAuthority": {
            "bundle": "exact verified EP8 bundle bytes or an exact checker-generated fixture proof bundle",
            "semanticClosure": "exact selected SemanticCapabilityClosureV3 bytes; source arrays, unit ids, source object order, CAS, and commitment are never mutated",
            "joinRules": [
                "bundle.projectId equals closure.projectId equals projection.projectId",
                "bundle proof requirements equal closure proofRefs, dependency graph, and unit ownership",
                "source closure CAS hashes the exact semantic closure canonical bytes",
                "source closure commitment recomputes under SEMANTIC-CAPABILITY-CLOSURE-GRAMMAR-V3",
            ],
        },
        "sortingGrammar": {
            "source": "exact RT13 SEMANTIC-CAPABILITY-CLOSURE-GRAMMAR-V3 tags and framing",
            "component": "tag || u32be(len(UTF8(s))) || UTF8(s)",
            "blob": "tag || u32be(len(bytes)) || bytes",
            "encodedRawKey": "blob(0x75, component(0x76,recordCasRef) || component(0x77,projectId) || component(0x78,recordKind))",
            "encodedUnitKey": "0x70 || component(0x71,unitId) || component(0x72,projectId) || component(0x74,requiredForCapability) || blob(0x79,concat(sort_unsigned(encodedRawKey(objectRefs))))",
            "comparison": "lexicographic unsigned bytes",
        },
        "derivation": {
            "operationalUnits": "Copy every source unit and sort only copied objectRefs by encodedRawKey; then sort copied units by encodedUnitKey.",
            "requiredObjectRefs": "Exact unique union of all operational unit objectRefs, sorted by encodedRawKey.",
            "sourceMutation": "FORBIDDEN", "lookupTable": "FORBIDDEN",
            "fixedUnitCount": "FORBIDDEN", "fixedObjectCount": "FORBIDDEN",
        },
        "canonicalGrammar": {
            "name": "OPERATIONAL-CUSTODY-PROJECTION-CANONICAL-JSON-V1",
            "encoding": "UTF-8, compact, no BOM or surrounding bytes",
            "rootKeyOrder": [
                "schemaVersion", "projectId", "sourceEvaluationProofBundleCasRef",
                "sourceSemanticCapabilityClosureCasRef",
                "sourceSemanticCapabilityClosureCommitment",
                "normalizationAlgorithm", "operationalUnits", "requiredObjectRefs",
            ],
            "unitKeyOrder": ["unitId", "projectId", "requiredForCapability", "objectRefs"],
            "rawObjectKeyOrder": ["projectId", "recordCasRef", "recordKind"],
            "objects": "closed; missing, unknown, duplicate, or reordered keys reject",
            "arrays": "exact derived order", "floatsExponentNaNInfinity": "forbidden",
        },
        "identityTypes": {
            "refType": "OperationalCustodyProjectionRefV1",
            "refEquation": "sha256:lowercase_hex(SHA256(projectionCanonicalBytes))",
            "digestType": "OperationalCustodyProjectionDigestV1",
            "digestDomain": "opensip.operational-custody-projection.v1",
            "digestEquation": "sha256:lowercase_hex(SHA256(ASCII(domain) || 0x00 || u64be(length) || projectionCanonicalBytes))",
            "semanticAliasForbidden": True,
        },
        "cardinality": {
            "algorithm": "derived from input arrays; no accepted count table",
            "twentyThreeIsOnlyOneCompatibilityGolden": True,
            "twoUnitsIsOnlyOneCompatibilityGolden": True,
            "embeddedByteBearingCounts": [[7, 2], [5, 3]],
            "checkerGeneratedCount": [9, 4],
        },
        "rt13NomatchCompatibilityGolden": {
            "sourceEvaluationProofBundleCasRef": "sha256:cc27c2beef32f3343d167c5727aa255b51884993ca416c4a862388e3be96a829",
            "sourceSemanticCapabilityClosureCasRef": "sha256:70ce71b8fc31551809c7c800a165fa5d9a8a8e04a7e5523e7668324fce8a977c",
            "requiredObjectRefCount": 23, "unitCount": 2,
            "operationalUnitOrder": ["replayable", "verifiable"],
            "canonicalByteLength": 10606,
            "projectionRef": "sha256:49a09580190c2f12de3912581171b3ed77dbd9c85a81c8367978a16016d16b60",
            "projectionDigest": "sha256:58c16d46dca070edb155ff8373973638b20f08877006f9a871306ed8b1a6afd3",
            "byteCustodyStatus": "IDENTITY-ONLY-COMPATIBILITY-GOLDEN; NOT A RawObjectResolutionConformanceV1 FIXTURE",
        },
    }


def _semantic_lease_contract(primary: dict[str, Any]) -> dict[str, Any]:
    return {
        "state": {
            "type": "LeaseStateV3", "closed": True, "schemaVersion": 3,
            "orderedFields": STATE_FIELDS,
            "nestedTypes": {
                "RawObjectKeyV1": ["projectId", "recordCasRef", "recordKind"],
                "RawObjectStateV1": OBJECT_STATE_FIELDS,
                "LeaseRecordV2": LEASE_FIELDS,
            },
        },
        "events": [{
            "type": {"expiry": "ExpiryEventV1", "release": "ReleaseEventV1",
                     "crash-reclaim": "CrashReclaimEventV3",
                     "resolve-and-pin": "ResolveAndPinEventV2"}[kind],
            "kind": kind, "closed": True, "orderedFields": fields,
        } for kind, fields in EVENT_FIELDS.items()],
        "commonRules": {
            "transactionBoundary": TX_BOUNDARY,
            "sequence": "event.atSequence equals prestate.ledgerSequence + 1",
            "project": "event, state, every raw key, lease, and scope share one projectId",
            "failureState": "Every semantic refusal returns a byte-exact deep copy of prestate with no sequence, fence, lease, object, or pending-expiry movement.",
            "externalFacts": "Owner liveness and fencing validity are primitive prevalidated inputs; this pure reducer neither establishes nor persists their provenance.",
        },
        "output": {
            "type": "SemanticLeaseOutputV3", "closed": True,
            "orderedFields": ["schemaVersion", "state", "result"],
            "schemaVersion": 3,
            "resultVariantOrderedFields": RESULT_VARIANT_FIELDS,
            "forbiddenPayloads": [
                "host termination class", "host error code", "process exit code",
                "receipt", "liveness proof", "journal", "recovery record",
            ],
        },
        "reducers": {
            "reduce_expiry_v1": "Advance one accepted sequence; defer an intersecting held pin by appending only not-yet-pending targets in event order, otherwise expire present targets.",
            "reduce_release_v1": "Require exact held lease identity/owner/fence; apply the complete ordered pendingExpiryRefs array, mark RELEASED, clear pending expiry, and advance once.",
            "reduce_crash_reclaim_v3": "Require exact held scope/owner/liveness/fence, false observed-owner-alive, expiry reached, and successorFencingToken exactly expected+1; apply complete ordered pending expiry, advance lastIssuedFencingToken exactly once, clear lease, and advance sequence.",
            "reduce_resolve_and_pin_v2": "Preserve exact RT13 idempotent retry; otherwise require current previous fence, future expiry, and every requested raw key AVAILABLE, then allocate exactly lastIssuedFencingToken+1.",
            "is_retention_local_unavailable_v1": "True exactly for a validated RETENTION_LOCAL_UNAVAILABLE result kind.",
        },
        "pureFunctionSignatures": [
            "reduce_expiry_v1(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ExpiryEventV1) -> SemanticLeaseOutputV3",
            "reduce_release_v1(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ReleaseEventV1) -> SemanticLeaseOutputV3",
            "reduce_crash_reclaim_v3(VerifiedSemanticRTSnapshotV1, LeaseStateV3, CrashReclaimEventV3) -> SemanticLeaseOutputV3",
            "reduce_resolve_and_pin_v2(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ResolveAndPinEventV2) -> SemanticLeaseOutputV3",
        ],
        "goldenScenarios": lease_goldens(primary),
        "legacyCompatibilityRule": "The verifier independently projects applicable exact RT13 LeaseStateV2 transitions to this host-neutral vocabulary. Crash successor-fence movement is the sole state delta; legacy host classification never enters this root.",
        "mutationRequirements": [
            "wrong event key order or runtime type", "cross-project key",
            "non-next sequence", "wrong transaction boundary", "duplicate raw key",
            "partial pending-expiry application", "pending-expiry sort or filter",
            "crash successor fence unchanged", "crash successor fence skips a value",
            "failure sequence movement", "failure fence movement", "failure state mutation",
        ],
    }


def _verified_api_contract(primary: dict[str, Any],
                           alternate: dict[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "constructor": {
            "signature": "validate_semantic_rt_snapshot_v1(FrozenDependencySnapshotV1, VerifiedD9SnapshotV1) -> VerifiedSemanticRTSnapshotV1",
            "compatibilityCapabilityUse": "VerifiedD9SnapshotV1 is consumed only by the verifier while reproducing rejected RT14 call shapes and rows; it is never retained or made semantically reachable.",
        },
        "frozenDependencySnapshotContract": {
            "kind": "opaque immutable in-memory capability; never JSON or persisted",
            "requiredProperties": [
                "one snapshotId and one alias-collapsed immutable byte map",
                "every unique local input read exactly once and hashed before any local source executes",
                "strict UTF-8 JSON with duplicate, float, NaN, and Infinity rejection",
                "verified sources compiled from buffers under synthetic filenames with no pyc, path import, sys.path discovery, or nested content reread",
                "stat-only end identity check and unchanged repository-state observation",
            ],
        },
        "verifiedD9Compatibility": {
            "scope": "checker/verifier only",
            "exactSubjects": {
                "artifactSha256": PINS[D9], "checkerSha256": PINS[D9_CHECKER],
                "reviewSha256": PINS[D9_REVIEW],
            },
            "requiredReviewState": "PASS / zero blockers / CANDIDATE-NOT-APPLIED",
            "rt14CorpusState": "REJECTED-BY-DEPENDENCY; semantic delta conditionally acceptable but never applied",
            "exactCallShapeCount": 6, "rowDenominator": {"retained": 11, "local": 1, "contextual": 4, "total": 16},
            "persistence": "FORBIDDEN",
        },
        "returnedSnapshot": {
            "type": "VerifiedSemanticRTSnapshotV1",
            "retainsExactly": [
                "snapshotId", "verified RT15 candidate buffer/object",
                "verified RT13 semantic basis buffer/object",
                "verified EP8 pure validation/derivation adapter",
                "operational projection encoder/ref/digest callables",
                "four semantic lease reducer callables",
                "retention-local-unavailable predicate",
                "RawObjectResolutionConformanceV1 pure validation callable and exact fixture snapshots",
            ],
            "mustNotRetain": [
                "D9 compatibility capability/module/bytes/review",
                "rejected RT14 contextual overlay",
                "downstream transaction, persistence, journal, receipt, recovery, or mutation capability",
            ],
            "objectGraphRule": "The verifier proves every must-not-retain object unreachable before returning the snapshot.",
        },
        "pureCallSignatures": [
            "derive_operational_custody_projection_v1(VerifiedSemanticRTSnapshotV1, VerifiedEvaluationProofBundleV1, ExactSemanticCapabilityClosureV3) -> (OperationalCustodyProjectionV1, OperationalCustodyProjectionRefV1, OperationalCustodyProjectionDigestV1)",
            "validate_raw_object_resolution_v1(VerifiedSemanticRTSnapshotV1, RawBytes, RawObjectResolutionRequestV1) -> RawObjectResolutionResultV1",
            "reduce_expiry_v1(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ExpiryEventV1) -> SemanticLeaseOutputV3",
            "reduce_release_v1(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ReleaseEventV1) -> SemanticLeaseOutputV3",
            "reduce_crash_reclaim_v3(VerifiedSemanticRTSnapshotV1, LeaseStateV3, CrashReclaimEventV3) -> SemanticLeaseOutputV3",
            "reduce_resolve_and_pin_v2(VerifiedSemanticRTSnapshotV1, LeaseStateV3, ResolveAndPinEventV2) -> SemanticLeaseOutputV3",
            "is_retention_local_unavailable_v1(VerifiedSemanticRTSnapshotV1, SemanticLeaseOutputV3) -> bool",
        ],
        "rawObjectResolutionConformance": _raw_resolution_contract(primary, alternate),
        "verifierTcb": {
            "soleInvocationPrefix": ["python3", "-I", "-B"],
            "requiredFlags": {"isolated": 1, "ignoreEnvironment": 1,
                              "noUserSite": 1, "dontWriteBytecode": True},
            "nestedProcesses": "FORBIDDEN", "localPathImports": "FORBIDDEN",
            "nestedContentRereads": "FORBIDDEN", "pyc": "FORBIDDEN",
            "sourceExecutionOrder": "all local data/checker/review buffers hash and review-bind before any verified local source buffer executes",
        },
    }


def expected_candidate(authority: FrozenAuthority) -> dict[str, Any]:
    rt13 = authority.parsed[RT13]
    closure_root = rt13["capabilityClosure"]
    closure = closure_root["semanticClosure"]
    primary = build_fixture("RT15-RAW-BYTES-PRIMARY-V1", PROJECT_A, PRIMARY_SPECS)
    alternate = build_fixture("RT15-RAW-BYTES-ALTERNATE-V1", PROJECT_B, ALTERNATE_SPECS)
    availability_projection = {
        "unitAvailabilityRecords": closure_root["unitAvailabilityRecords"],
        "availabilityFixtures": closure_root["availabilityFixtures"],
    }
    dependencies = {
        "schemaVersion": 1,
        "semanticSources": [
            {"role": "evaluation-proof-basis", "artifact": EP8, "sha256": PINS[EP8]},
            {"role": "retention-semantic-basis", "artifact": RT13, "sha256": PINS[RT13]},
        ],
    }
    semantic_basis = {
        "schemaVersion": 1,
        "sourceEvaluationProofArtifact": EP8,
        "sourceEvaluationProofSha256": PINS[EP8],
        "sourceRetentionArtifact": RT13,
        "sourceRetentionSha256": PINS[RT13],
        "semanticClosureGrammarSha256": "abd8c541da028f2a273cc509bb8a2bc1c19eb78618ea56676ac301a83dd82ef8",
        "semanticClosureGrammar": copy.deepcopy(closure_root["closureGrammar"]),
        "semanticCapabilityClosure": copy.deepcopy(closure),
        "semanticCapabilityClosureCasRef": "sha256:" + sha256(compact(closure, sort_keys=True)),
        "semanticCapabilityClosureCommitment": closure["closureCommitment"],
        "unitAvailabilityRecords": copy.deepcopy(closure_root["unitAvailabilityRecords"]),
        "availabilityFixtures": copy.deepcopy(closure_root["availabilityFixtures"]),
        "availabilityCanonicalSha256": sha256(compact(availability_projection, sort_keys=True)),
        "authorizedSemanticDeltaIds": [
            "RT15-DELTA-D9-FREE-LEASE-RESULT-VOCABULARY",
            "RT15-DELTA-CRASH-SUCCESSOR-FENCE",
            "RT15-DELTA-RAW-OBJECT-RESOLUTION-CONFORMANCE",
        ],
    }
    ownership = {
        "semanticDependencies": [
            "evaluation-proof.v8.json exact accepted pure-bundle authority",
            "retention-tiers.v13.json exact closure, custody, lease-transition, purge/lineage, policy, identity, and product-boundary basis",
        ],
        "ownsExactly": [
            "OperationalCustodyProjectionV1 and its canonical/ref/digest algorithms",
            "LeaseStateV3, four closed event types, SemanticLeaseOutputV3, and four pure reducers",
            "RawObjectResolutionConformanceV1 pure validator and new fixture-only byte closure",
            "VerifiedSemanticRTSnapshotV1",
        ],
        "runtimeAuthorityBoundary": "Liveness, fencing service, persistence, transactions, durability, recovery, atomicity, and content-addressed reads remain external caller responsibilities; semantic reducers consume only closed primitive values.",
        "dependencyBackedgeRule": "The semantic dependency root contains only EP8 and RT13. D9 and rejected RT14 are verifier-only compatibility evidence; downstream, store, receipt, journal, proof, recovery, and transaction artifacts are neither dependencies nor returned capabilities.",
        "rootDelta": {
            "predecessor": RT14, "predecessorRootCount": 19,
            "protectedRootKeys": PROTECTED_ROOTS, "protectedRootCount": 8,
            "changedRootKeys": ["version", "status", "supersedesAsArchitectureCandidate",
                                "authority", "invariants", "retainedResiduals"],
            "changedRootCount": 6, "removedRootKeys": REMOVED_RT14_ROOTS,
            "removedRootCount": 5,
            "addedRootKeys": [
                "dependencies", "semanticBasisProjection",
                "operationalCustodyProjectionContract", "semanticLeaseProtocolV3",
                "semanticOwnershipBoundary", "verifiedSemanticRtApiContract",
            ],
            "addedRootCount": 6, "finalRootCount": 20,
            "equation": "8 protected + 6 changed + 6 added = 20; five predecessor roots removed",
        },
    }
    return {
        "artifact": rt13["artifact"],
        "version": 15,
        "status": RT15_STATUS,
        "claimId": rt13["claimId"],
        "supersedesAsArchitectureCandidate": RT14,
        "dependencies": dependencies,
        "semanticBasisProjection": semantic_basis,
        "operationalCustodyProjectionContract": _operational_contract(),
        "semanticLeaseProtocolV3": _semantic_lease_contract(primary),
        "storageAndLineage": copy.deepcopy(rt13["storageAndLineage"]),
        "custodyPolicy": copy.deepcopy(rt13["custodyPolicy"]),
        "authority": {
            "candidateState": "NOT-APPLIED",
            "authorityClaim": "NONE",
            "semanticSourceRule": "Only exact verified EP8 facts, exact selected RT13 semantic/custody/product basis, and new forward-derived fixture bytes may enter RT-owned derivation.",
            "verifiedSnapshotRequired": True,
            "externalExecutionPrecondition": "Runtime byte reads, liveness, fencing, persistence, transaction, durability, recovery, and atomicity authority remain outside this semantic contract.",
            "productionExecutionClaim": "NONE",
        },
        "integrationState": copy.deepcopy(rt13["integrationState"]),
        "semanticOwnershipBoundary": ownership,
        "invariants": [
            "RT15-1: exact RT13 semantic closure bytes, arrays, CAS, commitment, availability, custody, policy, product, and no-seal basis never change",
            "RT15-2: operational projection has its own closed grammar, ref, digest, and count-independent algorithm",
            "RT15-3: every semantic state, event, output, raw resolution request/result, record type, and nested dependency type is closed",
            "RT15-4: caller-supplied bytes are validated before type, selector, project, kind, capability, or semantic use",
            "RT15-5: identity, receipt, path, selector, snapshot id, or availability alone never substitutes for bytes",
            "RT15-6: every fixture proof ref, graph endpoint, unit key, closure identity, projection identity, and commitment derives forward from embedded bytes",
            "RT15-7: the new fixtures do not replace RT13 NOMATCH identities and make no preimage claim for eleven patterned hashes",
            "RT15-8: every accepted non-idempotent event is exactly one next-sequence project transaction",
            "RT15-9: semantic refusal is byte-exact state/fence/sequence preserving",
            "RT15-10: release and reclaim apply the complete ordered pending-expiry array",
            "RT15-11: crash reclaim advances successor fencing exactly once and clears the lease",
            "RT15-12: D9 is checker/verifier-only and is unreachable from the returned semantic snapshot",
            "RT15-13: no downstream or storage semantic dependency backedge exists",
            "RT15-14: candidate, product, integration, application, seal, freeze, release, and production authority remain absent",
        ],
        "assurance": copy.deepcopy(rt13["assurance"]),
        "retainedResiduals": [
            "RT14 remains REJECTED-BY-DEPENDENCY and NOT-APPLIED. D9 v1.13 independently repairs only the checker/verifier compatibility authority; a fresh independent RT15 review is still required.",
            "The E8 preparation v6 finding is repaired here only by a new fixture-only byte-bearing upstream closure. The frozen old RT13 patterned identities remain unresolved and are not claimed or replaced.",
            "Any downstream successor must pin exact independently reviewed RT15 artifact/checker bytes and an exact fixture snapshot/result, rebuild its enclosing values, and receive its own fresh independent review.",
            "No production byte store, liveness, fencing, persistence, transaction, durability, recovery, crash, concurrency, or atomicity implementation is demonstrated.",
            "CD-RT-5 remains BLOCKED, product state remains BLOCKED_ON_PHASE_1A, durable default remains UNSELECTED, and this architecture candidate author has no review/application/freeze authority.",
        ],
        "sealRecommendation": copy.deepcopy(rt13["sealRecommendation"]),
        "rawPhysicalIdentityContract": copy.deepcopy(rt13["rawPhysicalIdentityContract"]),
        "verifiedSemanticRtApiContract": _verified_api_contract(primary, alternate),
    }


def _validate_fixture(fixture: Any, expected: dict[str, Any],
                      label: str) -> list[str]:
    findings: list[str] = []
    difference = exact_recursive_equal(fixture, expected, label)
    if difference:
        findings.append(f"RT15-FIXTURE-EXACT: {difference}")
    if not isinstance(fixture, dict):
        return findings or [f"RT15-FIXTURE-TOTAL: {label} is not an object"]
    try:
        rows = fixture["resolutionRows"]
        row_by_ref: dict[str, dict[str, Any]] = {}
        for index, row in enumerate(rows):
            raw = bytes.fromhex(row["rawBytesHex"])
            result = validate_raw_object_resolution(raw, row["request"])
            if exact_recursive_equal(result, row["expectedResult"],
                                     f"{label}.resolutionRows[{index}].expectedResult"):
                findings.append(f"RT15-RAW-RESULT: {label} row {index} result drift")
            ref = row["request"]["recordCasRef"]
            if ref in row_by_ref:
                findings.append(f"RT15-RAW-DUPLICATE: {label} duplicate {ref}")
            row_by_ref[ref] = row
            parsed = parse_json_bytes(raw, f"{label} raw row {index}")
            if parsed["dependencies"] != row["dependencies"]:
                findings.append(f"RT15-RAW-DEPENDENCY: {label} row {index} envelope drift")
        if set(row_by_ref) & set(OLD_PATTERNED_REFS):
            findings.append(f"RT15-RAW-OLD-IDENTITY: {label} reuses patterned RT13 refs")
        old_refs = {
            row["recordCasRef"] for row in expected["semanticClosure"]["proofRefs"]
        }
        if set(row_by_ref) != old_refs or len(row_by_ref) != fixture["recordCount"]:
            findings.append(f"RT15-RAW-CLOSURE: {label} bytes/proofRefs are not bijective")
        for edge in fixture["dependencyGraph"]:
            if edge["fromRef"] not in row_by_ref or edge["toRef"] not in row_by_ref:
                findings.append(f"RT15-RAW-GRAPH: {label} endpoint has no bytes")
        adjacency: dict[str, list[str]] = {ref: [] for ref in row_by_ref}
        for edge in fixture["dependencyGraph"]:
            adjacency[edge["fromRef"]].append(edge["toRef"])
        colors: dict[str, int] = {}
        def visit(node: str) -> None:
            if colors.get(node) == 1:
                raise ValueError("cycle")
            if colors.get(node) == 2:
                return
            colors[node] = 1
            for child in adjacency[node]:
                visit(child)
            colors[node] = 2
        for ref in adjacency:
            visit(ref)

        closure = fixture["semanticClosure"]
        closure_bytes = compact(closure, sort_keys=True)
        if closure_bytes.hex() != fixture["semanticClosureCanonicalBytesHex"] or \
                cas(closure_bytes) != fixture["semanticClosureCasRef"]:
            findings.append(f"RT15-RAW-CLOSURE-CAS: {label} closure bytes/CAS drift")
        if semantic_closure_commitment(closure["units"]) != closure["closureCommitment"]:
            findings.append(f"RT15-RAW-COMMITMENT: {label} semantic commitment drift")
        owners = [key["recordCasRef"] for unit in closure["units"]
                  for key in unit["objectRefs"]]
        if len(owners) != len(set(owners)) or set(owners) != set(row_by_ref):
            findings.append(f"RT15-RAW-UNIT-OWNERS: {label} owner closure drift")
        for unit in closure["units"]:
            if unit["unitId"] != derive_unit_id(
                    unit["projectId"], unit["requiredForCapability"], unit["objectRefs"]):
                findings.append(f"RT15-RAW-UNIT-ID: {label} unit id drift")
        bundle_bytes = bytes.fromhex(fixture["proofBundleCanonicalBytesHex"])
        if cas(bundle_bytes) != fixture["proofBundleCasRef"]:
            findings.append(f"RT15-RAW-BUNDLE-CAS: {label} proof bundle CAS drift")
        if parse_json_bytes(bundle_bytes, label + " proof bundle")["proofRefs"] != closure["proofRefs"]:
            findings.append(f"RT15-RAW-BUNDLE-CLOSURE: {label} proof ref drift")
        projection, encoded, ref, digest = derive_operational_projection(
            closure, fixture["proofBundleCasRef"], fixture["semanticClosureCasRef"])
        if (projection, encoded.hex(), ref, digest) != (
                fixture["operationalProjection"],
                fixture["operationalProjectionCanonicalBytesHex"],
                fixture["operationalProjectionRef"],
                fixture["operationalProjectionDigest"]):
            findings.append(f"RT15-RAW-PROJECTION: {label} projection drift")
        snapshot = fixture["rawObjectSnapshot"]
        if {row["recordCasRef"]: row["rawBytesHex"] for row in snapshot["records"]} != \
                {ref: row["rawBytesHex"] for ref, row in row_by_ref.items()}:
            findings.append(f"RT15-RAW-SNAPSHOT: {label} snapshot is not byte-complete")
        if fixture["commitments"] != expected["commitments"]:
            findings.append(f"RT15-RAW-FIXTURE-COMMITMENT: {label} commitment drift")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError,
            DuplicateKeyError, FloatForbidden, ResolutionError) as exc:
        findings.append(f"RT15-FIXTURE-TOTAL: {label} controlled {type(exc).__name__}")
    return findings


def _project_old_state(state: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(state)
    projected["schemaVersion"] = 3
    return projected


def _project_old_result(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("kind") == "D9":
        code = result.get("termination", {}).get("errorCode")
        mapping = {
            "REQUEST.PRECONDITION_FAILED": "RETENTION_PRECONDITION_FAILED",
            "LEDGER.BUSY_TIMEOUT": "RETENTION_BUSY",
            "REQUEST.UNSATISFIABLE": "RETENTION_LOCAL_UNAVAILABLE",
        }
        return {"kind": mapping[code]}
    projected = copy.deepcopy(result)
    if projected.get("kind") == "READ_CONTINUES":
        projected = {"kind": "READ_CONTINUES"}
    return projected


def _legacy_lease_findings(authority: FrozenAuthority) -> tuple[list[str], int]:
    findings: list[str] = []
    count = 0
    rt13 = authority.parsed[RT13]
    old_reduce = authority.modules[RT_CORE].reduce_lease
    for scenario in rt13["leaseProtocol"]["scenarios"]:
        old_state = copy.deepcopy(scenario["initial"])
        for event in scenario["events"]:
            if event["kind"] not in EVENT_FIELDS:
                continue
            old_output = old_reduce(copy.deepcopy(old_state), copy.deepcopy(event))
            v3_state = _project_old_state(old_state)
            v3_event = copy.deepcopy(event)
            if event["kind"] == "crash-reclaim":
                v3_event = {
                    **{key: value for key, value in event.items()
                       if key not in ("scopeRefs", "observedOwnerAlive")},
                    "successorFencingToken": event["expectedFencingToken"] + 1,
                    "scopeRefs": copy.deepcopy(event["scopeRefs"]),
                    "observedOwnerAlive": event["observedOwnerAlive"],
                }
            expected_state = _project_old_state(old_output["state"])
            if event["kind"] == "crash-reclaim" and \
                    old_output["result"].get("kind") == "LEASE_RECLAIMED":
                expected_state["lastIssuedFencingToken"] = v3_event["successorFencingToken"]
            expected = {
                "schemaVersion": 3, "state": expected_state,
                "result": _project_old_result(old_output["result"]),
            }
            actual = reduce_semantic_lease_v3(v3_state, v3_event)
            difference = exact_recursive_equal(actual, expected)
            if difference:
                findings.append(f"RT15-LEASE-RT13-COMPAT: {scenario['id']} {difference}")
            count += 1
            old_state = old_output["state"]
    return findings, count


def _d9_class(axes: dict[str, Any]) -> str:
    def analysis() -> str:
        if axes["lifecycle"] == "cannot-seal-coherent-run" or \
                axes["durability"] == "failed" or \
                axes["requiredPostconditions"] == "failed":
            return "operational-failed"
        if axes["requiredCoverage"] in ("unsatisfied", "unknown") or \
                axes["verdict"] == "indeterminate":
            return "indeterminate"
        if axes["verdict"] == "fail":
            return "policy-failed"
        return "success" if axes["verdict"] in ("pass", "advisory") \
            else "operational-failed"
    if axes["commandKind"] == "serve":
        return "success" if axes["domainCondition"] in (
            "clean-shutdown", "graceful-signal-stop") else "operational-failed"
    if axes["admission"] == "rejected":
        return "operational-failed" if axes["domainCondition"] == "host-fault" \
            else "request-rejected"
    if axes["domainCondition"] == "host-fault":
        return "operational-failed"
    if axes["interruption"] == "signal-before-finalization":
        return "interrupted"
    acl = axes["commandKind"] == "run" and axes["admission"] == "admitted" and \
        axes["lifecycle"] == "cannot-seal-coherent-run" and \
        axes["domainCondition"] == "precondition-failed" and \
        axes["rejectionCause"] == "unsatisfiable"
    if acl:
        return "request-rejected"
    if axes["commandKind"] == "mutation":
        if axes["domainCondition"] == "precondition-failed":
            return "request-rejected"
        return analysis() if axes["domainCondition"] == "verification-propagated" else "success"
    if axes["commandKind"] == "query":
        if axes["domainCondition"] == "addressed-identity-unresolved":
            return "request-rejected"
        return "indeterminate" if axes["requiredCoverage"] == "unsatisfied" else "success"
    return analysis()


def _d9_codes(axes: dict[str, Any], maps: dict[str, Any]) -> dict[str, Any]:
    if axes["deficiency"] != "none":
        values = [maps["deficiencyToReasonCode"][axes["deficiency"]]]
        values += [maps["deficiencyToReasonCode"][item]
                   for item in axes.get("secondaryDeficiencies", [])]
        return {"reasonCodes": values}
    if axes["rejectionCause"] != "none":
        return {"errorCode": maps["rejectionCauseToErrorCode"][axes["rejectionCause"]]}
    if axes["faultCause"] != "none":
        return {"errorCode": maps["faultCauseToErrorCode"][axes["faultCause"]]}
    return {}


def _d9_compatibility_findings(authority: FrozenAuthority) -> tuple[list[str], int, int]:
    findings: list[str] = []
    rt13 = authority.parsed[RT13]
    rt14 = authority.parsed[RT14]
    d9 = authority.parsed[D9]
    projected = copy.deepcopy(rt14)
    projected.pop("contextualD9Rejoin", None)
    projected["version"] = 13
    projected["supersedesAsArchitectureCandidate"] = "retention-tiers.v12.json"
    difference = exact_recursive_equal(projected, rt13)
    if difference:
        findings.append(f"RT15-RT14-RT13-PROJECTION: {difference}")
    tree = ast.parse(authority.buffers[RT14_CHECKER].decode("utf-8"), RT14_CHECKER)
    calls = [(node.lineno, ast.unparse(node.func), len(node.args),
              [keyword.arg for keyword in node.keywords])
             for node in ast.walk(tree) if isinstance(node, ast.Call)
             and "d9mod" in ast.unparse(node.func)]
    expected_calls = [
        (357, "d9mod.derive_class", 1, []),
        (358, "d9mod.derive_codes", 2, []),
        (472, "d9mod.V17.V16.derive_class", 1, []),
        (473, "d9mod.derive_class", 1, []),
        (480, "d9mod.reduce_concurrent", 2, []),
        (534, "authorities['d9mod'].check", 3, []),
    ]
    if sorted(calls) != sorted(expected_calls):
        findings.append("RT15-D9-CALL-SHAPES: exact six frozen calls drifted")
    rows: list[tuple[str, dict[str, Any], dict[str, Any], int]] = []
    for row in rt13["d9Derivation"]["rows"]:
        rows.append((row["id"], row["axes"], row["expectedTermination"],
                     row["expectedExitCode"]))
    local = rt14["contextualD9Rejoin"]["contextSplit"]["retentionLocalUnavailable"]
    rows.append(("RT14-LOCAL-UNAVAILABLE", local["axes"],
                 local["expectedReducerResult"]["termination"], local["expectedExitCode"]))
    matrix = rt14["contextualD9Rejoin"]["contextSplit"][
        "admittedAuthorizedCustodyLoss"]["coreCompletionMatrix"]
    for row in matrix:
        expected_termination = {key: value for key, value in row["expectedTermination"].items()
                                if key != "executionId"}
        rows.append((row["id"], row["axes"], expected_termination,
                     row["expectedExitCode"]))
    for row_id, axes, expected_termination, expected_exit in rows:
        termination = {"class": _d9_class(axes), **_d9_codes(axes, d9["codeMaps"])}
        if termination != expected_termination or \
                d9["classToExitCode"][termination["class"]] != expected_exit:
            findings.append(f"RT15-D9-ROW: {row_id} drifted")
    control = rt14["contextualD9Rejoin"]["faultPrecedenceControl"]["conditions"]
    reduced = {
        "faultCause": control["faultCauses"][0], "rejectionCause": "none",
        "deficiency": "none", "secondaryDeficiencies": [],
    }
    if reduced != {"faultCause": "durability-commit", "rejectionCause": "none",
                    "deficiency": "none", "secondaryDeficiencies": []}:
        findings.append("RT15-D9-PRECEDENCE: fault control drifted")
    return findings, len(calls), len(rows)


def _semantic_findings(candidate: dict[str, Any], expected: dict[str, Any],
                       authority: FrozenAuthority) -> list[str]:
    findings: list[str] = []
    rt13 = authority.parsed[RT13]
    if list(candidate) != ROOT_ORDER:
        findings.append("RT15-ROOT-ORDER: exact 20-root order drifted")
    for key in PROTECTED_ROOTS:
        if exact_recursive_equal(candidate.get(key), rt13[key], f"$.{key}"):
            findings.append(f"RT15-PROTECTED: {key} drifted from exact RT13 basis")
    if candidate.get("status") != RT15_STATUS:
        findings.append("RT15-STATUS: candidate/review boundary drifted")
    dependencies = candidate.get("dependencies")
    if dependencies != expected["dependencies"]:
        findings.append("RT15-DEPENDENCIES: semantic dependencies are not exactly EP8+RT13")
    basis = candidate.get("semanticBasisProjection")
    if not isinstance(basis, dict) or \
            basis.get("semanticCapabilityClosure") != rt13["capabilityClosure"]["semanticClosure"]:
        findings.append("RT15-SEMANTIC-BASIS: exact RT13 closure drifted")
    api = candidate.get("verifiedSemanticRtApiContract")
    try:
        fixtures = api["rawObjectResolutionConformance"]["fixtureGoldens"]
        expected_fixtures = expected["verifiedSemanticRtApiContract"][
            "rawObjectResolutionConformance"]["fixtureGoldens"]
        if len(fixtures) != 2:
            findings.append("RT15-FIXTURE-COUNT: exactly two embedded shapes required")
        for index, wanted in enumerate(expected_fixtures):
            actual = fixtures[index] if index < len(fixtures) else None
            findings.extend(_validate_fixture(actual, wanted, f"fixture[{index}]"))
    except (AttributeError, IndexError, KeyError, TypeError) as exc:
        findings.append(f"RT15-FIXTURE-TOTAL: controlled {type(exc).__name__}")
    try:
        old_closure = rt13["capabilityClosure"]["semanticClosure"]
        projection, encoded, ref, digest = derive_operational_projection(
            old_closure,
            "sha256:cc27c2beef32f3343d167c5727aa255b51884993ca416c4a862388e3be96a829",
            "sha256:70ce71b8fc31551809c7c800a165fa5d9a8a8e04a7e5523e7668324fce8a977c",
        )
        if (len(projection["requiredObjectRefs"]), len(projection["operationalUnits"]),
                len(encoded), ref, digest) != (
                23, 2, 10606,
                "sha256:49a09580190c2f12de3912581171b3ed77dbd9c85a81c8367978a16016d16b60",
                "sha256:58c16d46dca070edb155ff8373973638b20f08877006f9a871306ed8b1a6afd3"):
            findings.append("RT15-OP-RT13-GOLDEN: 23-ref compatibility projection drifted")
    except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        findings.append(f"RT15-OP-TOTAL: controlled {type(exc).__name__}")
    try:
        goldens = candidate["semanticLeaseProtocolV3"]["goldenScenarios"]
        for row in goldens:
            output = reduce_semantic_lease_v3(row["preState"], row["event"])
            difference = exact_recursive_equal(output, row["expectedOutput"])
            if difference:
                findings.append(f"RT15-LEASE-GOLDEN: {row.get('id')} {difference}")
        local = next(row for row in goldens if row["id"] == "SLV3-04-LOCAL-UNAVAILABLE")
        if not is_retention_local_unavailable_v1(local["expectedOutput"]):
            findings.append("RT15-LEASE-PREDICATE: local unavailable predicate drift")
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError) as exc:
        findings.append(f"RT15-LEASE-TOTAL: controlled {type(exc).__name__}")
    legacy, _count = _legacy_lease_findings(authority)
    findings.extend(legacy)
    d9_findings, _calls, _rows = _d9_compatibility_findings(authority)
    findings.extend(d9_findings)
    try:
        external = {
            row["recordCasRef"] for row in rt13["capabilityClosure"]["semanticClosure"]["proofRefs"]
        } - {
            row["recordCasRef"] for row in authority.parsed[EP8]["positiveVectors"][3]
            ["trustedStoreFixture"]["immutableCasRecords"]
        }
        if len(external) != 18 or set(DISCOVERED_OLD_PREIMAGES) | set(OLD_PATTERNED_REFS) != external or \
                set(DISCOVERED_OLD_PREIMAGES) & set(OLD_PATTERNED_REFS):
            findings.append("RT15-E8-FEASIBILITY: exact 7/18 + 11/18 partition drifted")
    except (KeyError, TypeError, IndexError) as exc:
        findings.append(f"RT15-E8-FEASIBILITY-TOTAL: controlled {type(exc).__name__}")
    return findings


def check_contract(candidate: Any, authority: FrozenAuthority,
                   candidate_source: bytes | None = None) -> list[str]:
    if not isinstance(candidate, dict) or not candidate:
        return ["RT15-TOTALITY-ROOT: candidate must be a nonempty object"]
    findings: list[str] = []
    try:
        expected = expected_candidate(authority)
        difference = exact_recursive_equal(candidate, expected)
        if difference:
            findings.append(f"RT15-EXACT-CANDIDATE: {difference}")
        if candidate_source is not None and candidate_source != pretty(candidate):
            findings.append("RT15-CANONICAL-RAW: candidate is not exact canonical pretty JSON")
        findings.extend(_semantic_findings(candidate, expected, authority))
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError,
            ValueError, DuplicateKeyError, FloatForbidden, ResolutionError) as exc:
        findings.append(f"RT15-TOTALITY-EXCEPTION: controlled {type(exc).__name__}")
    return findings


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def _candidate_mutations() -> list[Mutation]:
    def fixture(root: dict[str, Any], index: int = 0) -> dict[str, Any]:
        return root["verifiedSemanticRtApiContract"][
            "rawObjectResolutionConformance"]["fixtureGoldens"][index]

    return [
        ("version", lambda root: root.__setitem__("version", 14)),
        ("status promotion", lambda root: root.__setitem__("status", "APPLIED")),
        ("supersedes", lambda root: root.__setitem__("supersedesAsArchitectureCandidate", RT13)),
        ("dependency hash", lambda root: root["dependencies"]["semanticSources"][0].__setitem__("sha256", "0" * 64)),
        ("dependency injection", lambda root: root["dependencies"]["semanticSources"].append({"role": "store", "artifact": "store.json", "sha256": "0" * 64})),
        ("basis source", lambda root: root["semanticBasisProjection"].__setitem__("sourceRetentionArtifact", RT14)),
        ("grammar id", lambda root: root["semanticBasisProjection"]["semanticClosureGrammar"].__setitem__("id", "drift")),
        ("closure cas", lambda root: root["semanticBasisProjection"].__setitem__("semanticCapabilityClosureCasRef", "sha256:" + "0" * 64)),
        ("basis proof ref", lambda root: root["semanticBasisProjection"]["semanticCapabilityClosure"]["proofRefs"][0].__setitem__("recordCasRef", "sha256:" + "0" * 64)),
        ("basis commitment", lambda root: root["semanticBasisProjection"].__setitem__("semanticCapabilityClosureCommitment", "sha256:" + "0" * 64)),
        ("availability", lambda root: root["semanticBasisProjection"]["unitAvailabilityRecords"].pop()),
        ("projection type", lambda root: root["operationalCustodyProjectionContract"].__setitem__("type", "OperationalCustodyProjectionV2")),
        ("projection tag", lambda root: root["operationalCustodyProjectionContract"]["sortingGrammar"].__setitem__("encodedRawKey", "wrong")),
        ("projection fixed count", lambda root: root["operationalCustodyProjectionContract"]["cardinality"].__setitem__("algorithm", "exactly 23")),
        ("lease state version", lambda root: root["semanticLeaseProtocolV3"]["state"].__setitem__("schemaVersion", 2)),
        ("lease event fields", lambda root: root["semanticLeaseProtocolV3"]["events"][2]["orderedFields"].pop()),
        ("lease result variant", lambda root: root["semanticLeaseProtocolV3"]["output"]["resultVariantOrderedFields"]["LEASE_RECLAIMED"].pop()),
        ("lease reducer", lambda root: root["semanticLeaseProtocolV3"]["reducers"].__setitem__("reduce_crash_reclaim_v3", "skip fence")),
        ("lease golden state", lambda root: root["semanticLeaseProtocolV3"]["goldenScenarios"][0]["preState"].__setitem__("ledgerSequence", 9)),
        ("lease golden successor", lambda root: root["semanticLeaseProtocolV3"]["goldenScenarios"][6]["event"].__setitem__("successorFencingToken", 7)),
        ("storage", lambda root: root["storageAndLineage"].__setitem__("purgeAuthority", "caller")),
        ("custody", lambda root: root["custodyPolicy"].__setitem__("durableDefault", "selected")),
        ("authority", lambda root: root["authority"].__setitem__("authorityClaim", "APPLIED")),
        ("integration", lambda root: root["integrationState"].__setitem__("CD-RT-5", "PASS")),
        ("ownership backedge", lambda root: root["semanticOwnershipBoundary"]["semanticDependencies"].append("downstream store")),
        ("invariant", lambda root: root["invariants"].pop()),
        ("assurance", lambda root: root["assurance"].__setitem__("evidenceGrade", "PRODUCTION")),
        ("residual", lambda root: root["retainedResiduals"].pop()),
        ("seal", lambda root: root.__setitem__("sealRecommendation", "SEAL")),
        ("physical identity", lambda root: root["rawPhysicalIdentityContract"].__setitem__("rawCasPattern", ".*")),
        ("api constructor", lambda root: root["verifiedSemanticRtApiContract"]["constructor"].__setitem__("signature", "wrong")),
        ("d9 checker hash", lambda root: root["verifiedSemanticRtApiContract"]["verifiedD9Compatibility"]["exactSubjects"].__setitem__("checkerSha256", "0" * 64)),
        ("request order", lambda root: root["verifiedSemanticRtApiContract"]["rawObjectResolutionConformance"]["requestOrderedFields"].reverse()),
        ("validation order", lambda root: root["verifiedSemanticRtApiContract"]["rawObjectResolutionConformance"]["validationOrder"].reverse()),
        ("type registry", lambda root: root["verifiedSemanticRtApiContract"]["rawObjectResolutionConformance"]["closedTypeRegistry"].pop()),
        ("primary raw bytes", lambda root: fixture(root)["resolutionRows"][0].__setitem__("rawBytesHex", fixture(root)["resolutionRows"][0]["rawBytesHex"][:-2] + "00")),
        ("primary usable result", lambda root: fixture(root)["resolutionRows"][0]["expectedResult"].__setitem__("kind", "IDENTITY_ONLY")),
        ("primary projection", lambda root: fixture(root).__setitem__("operationalProjectionRef", "sha256:" + "0" * 64)),
        ("alternate count", lambda root: fixture(root, 1).__setitem__("recordCount", 7)),
        ("snapshot byte omission", lambda root: fixture(root)["rawObjectSnapshot"]["records"].pop()),
    ]


def _raw_adversarial(fixtures: list[dict[str, Any]]) -> tuple[int, int, int]:
    passed = 0
    total = 0
    escapes = 0
    for fixture_index, fixture in enumerate(fixtures):
        for row_index, row in enumerate(fixture["resolutionRows"]):
            raw = bytes.fromhex(row["rawBytesHex"])
            request = row["request"]
            attacks: list[tuple[str, Any, dict[str, Any], str]] = []
            attacks.append(("missing", None, copy.deepcopy(request), "BYTES_NOT_PRESENT"))
            attacks.append(("empty", b"", copy.deepcopy(request), "BYTES_NOT_PRESENT"))
            attacks.append(("byte-flip", raw[:-1] + bytes([raw[-1] ^ 1]), copy.deepcopy(request), "CAS_MISMATCH"))
            changed = copy.deepcopy(request); changed["recordCasRef"] = "sha256:" + "0" * 64
            attacks.append(("wrong-cas", raw, changed, "CAS_MISMATCH"))
            changed = copy.deepcopy(request); changed["expectedValueType"] = "WrongTypeV1"
            attacks.append(("wrong-type", raw, changed, "EXPECTED_TYPE_MISMATCH"))
            changed = copy.deepcopy(request); changed["selector"] = "/wrong"
            attacks.append(("wrong-selector", raw, changed, "SELECTOR_MISMATCH"))
            changed = copy.deepcopy(request); changed["projectId"] = PROJECT_B if request["projectId"] != PROJECT_B else PROJECT_A
            attacks.append(("wrong-project", raw, changed, "PROJECT_MISMATCH"))
            other_kind = next(kind for kind in RECORD_TYPES if kind != request["recordKind"])
            changed = copy.deepcopy(request); changed["recordKind"] = other_kind
            attacks.append(("wrong-kind", raw, changed, "CLOSED_TYPE_MISMATCH"))
            changed = copy.deepcopy(request); changed["requiredCapability"] = \
                "replayable" if request["requiredCapability"] == "verifiable" else "verifiable"
            attacks.append(("wrong-capability", raw, changed, "CAPABILITY_MISMATCH"))
            float_raw = raw.replace(b'"schemaVersion":1', b'"schemaVersion":1.0', 1)
            changed = copy.deepcopy(request); changed["recordCasRef"] = cas(float_raw)
            attacks.append(("float", float_raw, changed, "CLOSED_TYPE_MISMATCH"))
            duplicate_raw = raw.replace(b'{"schemaVersion":1', b'{"schemaVersion":1,"schemaVersion":1', 1)
            changed = copy.deepcopy(request); changed["recordCasRef"] = cas(duplicate_raw)
            attacks.append(("duplicate-key", duplicate_raw, changed, "CLOSED_TYPE_MISMATCH"))
            for attack_name, attack_raw, attack_request, expected_code in attacks:
                total += 1
                try:
                    validate_raw_object_resolution(attack_raw, attack_request)
                    escapes += 1
                except ResolutionError as exc:
                    if exc.code == expected_code:
                        passed += 1
                    else:
                        escapes += 1
                except Exception:
                    escapes += 1
    return passed, total, escapes


def _lease_adversarial(goldens: list[dict[str, Any]]) -> tuple[int, int, int]:
    passed = 0
    total = 0
    escapes = 0
    for row in goldens:
        attacks: list[dict[str, Any]] = []
        changed = copy.deepcopy(row["event"]); changed["atSequence"] += 1; attacks.append(changed)
        changed = copy.deepcopy(row["event"]); changed["transactionBoundary"] = "WRONG"; attacks.append(changed)
        changed = copy.deepcopy(row["event"]); changed["projectId"] = PROJECT_B; attacks.append(changed)
        changed = copy.deepcopy(row["event"]); first = next(iter(changed)); value = changed.pop(first); changed[first] = value; attacks.append(changed)
        for event in attacks:
            total += 1
            try:
                reduce_semantic_lease_v3(row["preState"], event)
                escapes += 1
            except (TypeError, ValueError, ResolutionError):
                passed += 1
            except Exception:
                escapes += 1
    return passed, total, escapes


HOSTILE_ROOTS: list[tuple[str, Any]] = [
    ("null", None), ("false", False), ("zero", 0), ("float", 1.5),
    ("string", "hostile"), ("array", []), ("empty-object", {}),
    ("array-object", [{}]),
]


def selftest(candidate: dict[str, Any], candidate_source: bytes,
             authority: FrozenAuthority) -> int:
    expected = expected_candidate(authority)
    if candidate_source != pretty(expected) or candidate_source != pretty(candidate):
        print("REFUSING to self-test: base is not exact canonical RT15 candidate")
        return 1
    base = check_contract(candidate, authority, candidate_source)
    if base:
        print(f"REFUSING to self-test: base has {len(base)} finding(s)")
        for finding in base[:12]:
            print("  -", finding)
        return 1

    print("frozen authority and canonical base")
    print(f"  pass  {len(PINS)}/{len(PINS)} inputs read once and hash-bound before source execution")
    print("  pass  strict duplicate/nonfinite/float rejection and exact canonical candidate")

    generated = build_fixture(
        "RT15-RAW-BYTES-GENERATED-SELFTEST-V1", PROJECT_A,
        synthetic_specs(9, 4),
    )
    generated_findings = _validate_fixture(generated, generated, "generated[9/4]")
    generated_ok = generated["recordCount"] == 9 and generated["unitCount"] == 4 and \
        not generated_findings
    print("\ncount-independent fixture algorithm")
    print(f"  {'pass' if generated_ok else 'FAIL':>6}  generated 9 refs / 4 units; every ref byte-bearing")

    mutations = _candidate_mutations()
    mutation_failures = 0
    signatures: set[str] = set()
    noops = 0
    duplicates = 0
    print("\nexact candidate mutations - every row must be rejected")
    for name, mutate in mutations:
        changed = copy.deepcopy(candidate)
        before = pretty(changed)
        try:
            mutate(changed)
            after = pretty(changed)
            if after == before:
                noops += 1
                rejected = False
            else:
                signature = sha256(after)
                if signature in signatures:
                    duplicates += 1
                signatures.add(signature)
                rejected = bool(check_contract(changed, authority, after))
        except Exception:
            rejected = False
        mutation_failures += 0 if rejected else 1
        print(f"  {'reject' if rejected else 'ESCAPE':>6}  {name}")

    fixtures = candidate["verifiedSemanticRtApiContract"][
        "rawObjectResolutionConformance"]["fixtureGoldens"]
    raw_passed, raw_total, raw_escapes = _raw_adversarial(fixtures)
    print(f"\nraw resolution adversarial: {raw_passed}/{raw_total} rejected at exact validation stage; escapes={raw_escapes}")
    lease_gold = candidate["semanticLeaseProtocolV3"]["goldenScenarios"]
    lease_passed, lease_total, lease_escapes = _lease_adversarial(lease_gold)
    print(f"semantic lease shape adversarial: {lease_passed}/{lease_total} rejected; escapes={lease_escapes}")

    hostile: list[tuple[str, Any]] = list(HOSTILE_ROOTS)
    for key in ROOT_ORDER:
        for value in (None, "hostile"):
            changed = copy.deepcopy(candidate)
            changed[key] = value
            hostile.append((f"{key}={type(value).__name__}", changed))
    hostile_failures = 0
    for _name, value in hostile:
        try:
            source = pretty(value)
            rejected = bool(check_contract(value, authority, source))
        except Exception:
            rejected = False
        hostile_failures += 0 if rejected else 1
    print(f"hostile totality: {len(hostile) - hostile_failures}/{len(hostile)} rejected without escape")

    legacy_findings, legacy_count = _legacy_lease_findings(authority)
    d9_findings, call_count, row_count = _d9_compatibility_findings(authority)
    print("\nsupplemental predecessor compatibility (not authority promotion)")
    print(f"  {'pass' if not legacy_findings else 'FAIL':>6}  {legacy_count} applicable RT13 lease transitions")
    print(f"  {'pass' if not d9_findings else 'FAIL':>6}  RT14/D9 v1.13: {call_count} call shapes, {row_count} rows")

    dirty = candidate_source.replace(b"{\n", b"{ \n", 1)
    try:
        parsed_dirty = parse_json_bytes(dirty, "dirty")
        dirty_refused = dirty != candidate_source and dirty != pretty(parsed_dirty)
    except Exception:
        dirty_refused = False
    print(f"  {'pass' if dirty_refused else 'FAIL':>6}  dirty parsed-equal base refused before mutation accounting")

    authority.end_stat_check()
    failed = (
        not generated_ok or mutation_failures or noops or duplicates
        or raw_escapes or lease_escapes or hostile_failures
        or legacy_findings or d9_findings or not dirty_refused
    )
    print()
    if failed:
        print(
            "RT15 selftest failures: "
            f"generated={not generated_ok}, object={mutation_failures}/{len(mutations)}, "
            f"noops={noops}, duplicates={duplicates}, raw={raw_escapes}/{raw_total}, "
            f"lease={lease_escapes}/{lease_total}, hostile={hostile_failures}/{len(hostile)}, "
            f"legacy={len(legacy_findings)}, d9={len(d9_findings)}, dirty={not dirty_refused}"
        )
        return 1
    print(
        f"all {len(mutations)} exact candidate mutations, {raw_total} raw-resolution "
        f"adversarials, {lease_total} lease-shape adversarials, and {len(hostile)} hostile "
        "shapes rejected; zero no-op, duplicate, skipped, ambiguous, or escaped cases; "
        "generated 9/4 fixture, exact RT13 lease projection, and RT14/D9 6-call/16-row "
        "supplemental compatibility passed"
    )
    return 0


def main(argv: list[str]) -> int:
    try:
        authority = FrozenAuthority()
        authority.freeze()
    except (OSError, UnicodeError, SyntaxError, AuthorityError, ValueError,
            DuplicateKeyError, FloatForbidden, json.JSONDecodeError) as exc:
        print(f"cannot freeze RT15 authority: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if "--emit-candidate" in argv[1:]:
        sys.stdout.buffer.write(pretty(expected_candidate(authority)))
        authority.end_stat_check()
        return 0
    positional = [item for item in argv[1:]
                  if item not in ("--selftest", "--emit-candidate")]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        source = path.read_bytes()
        candidate = parse_json_bytes(source, str(path))
    except (OSError, UnicodeError, ValueError, DuplicateKeyError, FloatForbidden,
            json.JSONDecodeError) as exc:
        print(f"cannot load RT15 candidate: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if "--selftest" in argv[1:]:
        if not isinstance(candidate, dict):
            print("selftest requires an object root", file=sys.stderr)
            return 1
        return selftest(candidate, source, authority)
    findings = check_contract(candidate, authority, source)
    try:
        authority.end_stat_check()
    except AuthorityError as exc:
        findings.append(f"RT15-AUTHORITY-END: {exc}")
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    raw = candidate["verifiedSemanticRtApiContract"][
        "rawObjectResolutionConformance"]["fixtureGoldens"]
    print(
        f"RT15 contract OK - {path.name}; {len(PINS)} frozen inputs read once; "
        f"byte-bearing fixtures {raw[0]['recordCount']}/{raw[0]['unitCount']} and "
        f"{raw[1]['recordCount']}/{raw[1]['unitCount']}; exact RT13 semantic basis; "
        "D9-free returned snapshot; CANDIDATE-NOT-APPLIED"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
