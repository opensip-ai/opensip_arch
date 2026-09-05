#!/usr/bin/env python3
"""Executable design-integrity checker for Evaluation Proof v6.

EP6 keeps the reviewed EP5 pure proof core but replaces self-attested authority
with exact raw receipts, live C2/RI recomputation, a unique project-scoped store
lookup, and a guarded non-serializable admission capability.

Public successor APIs consumed by RT11/Evidence v5:

  admit_evaluation_authority(input) -> _AdmittedEvaluationAuthorityV1
  validate_bundle(bundle, admitted_handle)
  resolve_semantic_object_bindings(admitted_handle)
  derive_semantic_requirements(admitted_handle)
  derive_dependency_edges(bundle, admitted_handle)
  derive_raw_proof_requirements(bundle, admitted_handle)
  derive_transitive_requirements(seed_requirements, dependency_edges)
  encode_semantic_object_binding(binding)

Usage: python3 -B check-evaluation-proof-v6.py [artifact] [--selftest]
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import re
import sys
import unicodedata
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "evaluation-proof.v6.json"
EXPECTED_VERSION = 6
PROJECT_RE = re.compile(r"^prj1-[0-9a-f]{64}$")
REF_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PLAN_RE = re.compile(r"^plan1:sha256:[0-9a-f]{64}$")
SNAPSHOT_RE = re.compile(r"^snap1:sha256:[0-9a-f]{64}$")

PINNED = {
    "evaluation-proof.v5.json": "e05f6d8d9dd5f1f98dc1972a178c7fe58981c71b06a69feb00a717e03475988b",
    "check-evaluation-proof.py": "1ccc12c347f0c7598604227179a2ba0cc461466657908b5c5f9645db4f7b99e2",
    "c2-plan-stage-schema.v3.json": "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285",
    "check-c2.py": "4f31d57cd1cd252d47eeb520aa31b5fe8c4fd3b0f0f067a6840b008b1fe176f3",
    "resolved-inputs.v2.json": "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    "check-resolved-inputs.py": "7ffed1c0e66e345a72c5e0e7feaf332508d0842c1ecdba8572f872997917ffa0",
    "fact-plane.v1.json": "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
}

AUTHORITY_INPUT_FIELDS = {
    "schemaVersion", "interfaceId", "admittedResolvedInputs",
    "planAuthorityReceipt", "evaluationAuthorityAdmission",
    "authorityObjectRecords", "authorityDependencyEdges",
    "evaluationAuthorityStoreIndex", "evaluationAuthoritySeal",
    "activationManifest", "semanticObjectBindings", "semanticObjectRecords",
}
RESOLVED_FIELDS = {
    "schemaVersion", "projectId", "frozenPlanIntent", "snapshotDescriptor",
    "snapshotContentManifest", "planDescriptor",
}
PLAN_RECEIPT_FIELDS = {
    "schemaVersion", "projectId", "admittedResolvedInputsRef",
    "planIntentRecipe", "planIntentCommitment", "snapshotRecipe",
    "snapshotId", "planRecipe", "planId",
}
ADMISSION_FIELDS = {
    "schemaVersion", "projectId", "planAuthorityReceiptRef", "planId",
    "activationManifestRef", "activationManifestRecordRef",
    "evaluationAuthoritySealRef", "evaluationAuthoritySealRecordRef",
}
RAW_RECORD_FIELDS = {"projectId", "recordCasRef", "recordKind", "recordBytesHex"}
EDGE_FIELDS = {"fromRef", "toRef", "projectId", "role"}
INDEX_FIELDS = {
    "schemaVersion", "projectId", "evaluationAuthoritySealRef",
    "evaluationAuthorityAdmissionRef",
}
CONTENT_FIELDS = {"path", "kind", "byteLength", "recordCasRef"}
ROLE_CAPABILITY = {
    "plan-authority-receipt": None,
    "admitted-resolved-inputs": None,
    "snapshot-content": "replayable",
    "evaluation-authority-seal-record": None,
    "activation-manifest-record": None,
}
CAPABILITY_RANK = {"recorded": 0, "verifiable": 1, "replayable": 2}
RAW_KIND_BY_TYPE = {
    "AdmittedResolvedInputsV1": "resolved-inputs",
    "PlanAuthorityReceiptV1": "plan-id-verification-receipt",
    "EvaluationAuthorityAdmissionV1": "authority-seal-verification-receipt",
}
DOMAIN_BY_TYPE = {
    "AdmittedResolvedInputsV1": "opensip.admitted-resolved-inputs.v1",
    "PlanAuthorityReceiptV1": "opensip.plan-authority-receipt.v1",
    "EvaluationAuthorityAdmissionV1": "opensip.evaluation-authority-admission.v1",
    "EvaluationAuthorityIndexV1": "opensip.evaluation-authority-index.v1",
}
FIELDS_BY_TYPE = {
    "AdmittedResolvedInputsV1": RESOLVED_FIELDS,
    "PlanAuthorityReceiptV1": PLAN_RECEIPT_FIELDS,
    "EvaluationAuthorityAdmissionV1": ADMISSION_FIELDS,
    "EvaluationAuthorityIndexV1": INDEX_FIELDS,
}
FORBIDDEN_AUTHORITY_KEYS = {
    "verificationOwner", "suppliedBy", "verified", "pinned", "requestId",
    "executionId", "runId", "runSealRef", "terminal", "TerminalRunV1",
    "evidenceDigest", "RunAuthorityIndexV1",
}


class DuplicateKeyError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(), object_pairs_hook=_pairs)


def sha_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_module(filename: str, name: str):
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


_EP5: Any = None
_C2: Any = None
_RI: Any = None


def _modules() -> tuple[Any, Any, Any]:
    global _EP5, _C2, _RI
    for filename, expected in PINNED.items():
        actual = sha_file(HERE / filename)
        if actual != expected:
            raise ValueError(f"pinned input drift: {filename} {actual} != {expected}")
    if _EP5 is None:
        _EP5 = _load_module("check-evaluation-proof.py", "ep5_pinned_for_ep6")
    if _C2 is None:
        _C2 = _load_module("check-c2.py", "c2_pinned_for_ep6")
    if _RI is None:
        _RI = _load_module("check-resolved-inputs.py", "ri_pinned_for_ep6")
    return _EP5, _C2, _RI


def _validate_json_model(value: Any) -> None:
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int) and not isinstance(value, bool):
        if not -(1 << 63) <= value < (1 << 63):
            raise ValueError("integer outside signed-64")
        return
    if isinstance(value, float):
        raise ValueError("floats are forbidden")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise ValueError("non-NFC string")
        return
    if isinstance(value, list):
        for item in value:
            _validate_json_model(item)
        return
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        for key, item in value.items():
            _validate_json_model(key)
            _validate_json_model(item)
        return
    raise ValueError(f"unsupported JSON value {type(value).__name__}")


def canonical_json(value: Any) -> bytes:
    _validate_json_model(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def raw_record_bytes(record_type: str, value: dict[str, Any]) -> bytes:
    if record_type not in DOMAIN_BY_TYPE:
        raise ValueError(f"unknown raw record type {record_type}")
    if not isinstance(value, dict) or set(value) != FIELDS_BY_TYPE[record_type]:
        raise ValueError(f"{record_type} is not the exact closed record")
    return DOMAIN_BY_TYPE[record_type].encode("ascii") + b"\0" + canonical_json(value)


def raw_record_ref(record_type: str, value: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(raw_record_bytes(record_type, value)).hexdigest()


def _walk_forbidden(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        bad = set(value) & FORBIDDEN_AUTHORITY_KEYS
        if bad:
            raise ValueError(f"{path} contains forbidden authority keys {sorted(bad)}")
        for key, child in value.items():
            _walk_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_forbidden(child, f"{path}[{index}]")


def _decode_authority_record(row: Any, record_type: str,
                             expected_value: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    if not isinstance(row, dict) or set(row) != RAW_RECORD_FIELDS:
        raise ValueError(f"{record_type} physical row is not closed")
    if row.get("recordKind") != RAW_KIND_BY_TYPE[record_type]:
        raise ValueError(f"{record_type} has wrong recordKind")
    raw_hex = row.get("recordBytesHex")
    if not isinstance(raw_hex, str) or not re.fullmatch(r"(?:[0-9a-f]{2})+", raw_hex):
        raise ValueError(f"{record_type} bytes are not lowercase nonempty hex")
    raw = bytes.fromhex(raw_hex)
    ref = "sha256:" + hashlib.sha256(raw).hexdigest()
    if row.get("recordCasRef") != ref:
        raise ValueError(f"{record_type} raw CAS mismatch")
    domain = DOMAIN_BY_TYPE[record_type].encode("ascii") + b"\0"
    if not raw.startswith(domain):
        raise ValueError(f"{record_type} domain mismatch")
    parsed = json.loads(raw[len(domain):].decode("utf-8"), object_pairs_hook=_pairs)
    if not isinstance(parsed, dict) or set(parsed) != FIELDS_BY_TYPE[record_type]:
        raise ValueError(f"{record_type} decoded fields are not exact")
    if domain + canonical_json(parsed) != raw:
        raise ValueError(f"{record_type} does not byte-identically canonical re-encode")
    if parsed != expected_value:
        raise ValueError(f"{record_type} bytes differ from supplied closed value")
    _walk_forbidden(parsed)
    return parsed, raw


def encode_semantic_object_binding(binding: dict[str, Any]) -> bytes:
    return _modules()[0].encode_semantic_object_binding(binding)


_CAPABILITY_TOKEN = object()


class _AdmittedEvaluationAuthorityV1:
    """Opaque in-process capability; parsed JSON can never be an instance."""
    __slots__ = ("_input", "_legacy", "_raw_refs", "_token")

    def __init__(self, token: object, value: dict[str, Any], legacy: dict[str, Any],
                 raw_refs: dict[str, str]) -> None:
        if token is not _CAPABILITY_TOKEN:
            raise TypeError("AdmittedEvaluationAuthorityV1 has no public constructor")
        self._input = value
        self._legacy = legacy
        self._raw_refs = raw_refs
        self._token = token

    def __reduce__(self):
        raise TypeError("AdmittedEvaluationAuthorityV1 is non-serializable")

    def __repr__(self) -> str:
        return "<opaque AdmittedEvaluationAuthorityV1>"


def _exact_project(value: Any, label: str) -> str:
    if not isinstance(value, str) or not PROJECT_RE.fullmatch(value):
        raise ValueError(f"{label} is not PROJECT-ID-V1")
    return value


def _exact_ref(value: Any, label: str) -> str:
    if not isinstance(value, str) or not REF_RE.fullmatch(value):
        raise ValueError(f"{label} is not Raw/Semantic sha256 ref")
    return value


def _content_manifest(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for entry in snapshot["entries"]:
        if entry["kind"] == "file":
            result.append({
                "path": entry["path"], "kind": "file-bytes",
                "byteLength": entry["byteLength"],
                "recordCasRef": "sha256:" + entry["contentSha256"],
            })
        else:
            target = bytes.fromhex(entry["targetBytesHex"])
            result.append({
                "path": entry["path"], "kind": "symlink-target-bytes",
                "byteLength": len(target),
                "recordCasRef": "sha256:" + hashlib.sha256(target).hexdigest(),
            })
    return sorted(result, key=canonical_json)


def _legacy_authority(value: dict[str, Any], refs: dict[str, str]) -> dict[str, Any]:
    receipt = value["planAuthorityReceipt"]
    admission = value["evaluationAuthorityAdmission"]
    return {
        "schemaVersion": 2,
        "interfaceId": "opensip-evidence.verified-evaluation-authority-seal.v2",
        "suppliedBy": "opensip-evidence",
        "planIdAdmission": {
            "verificationOwner": "opensip-plan",
            "planIdRecipe": "PLAN-ID-V1",
            "admittedResolvedInputsRef": receipt["admittedResolvedInputsRef"],
            "verifiedPlanId": receipt["planId"],
            "verificationReceiptRef": admission["planAuthorityReceiptRef"],
        },
        "authoritySealAdmission": {
            "verificationOwner": "opensip-store",
            "projectId": admission["projectId"],
            "resolvedEvaluationAuthoritySealRef": admission["evaluationAuthoritySealRef"],
            "sealedActivationManifestRef": admission["activationManifestRef"],
            "verificationReceiptRef": refs["EvaluationAuthorityAdmissionV1"],
        },
        "evaluationAuthoritySeal": value["evaluationAuthoritySeal"],
        "activationManifest": value["activationManifest"],
        "semanticObjectBindings": value["semanticObjectBindings"],
        "semanticObjectRecords": value["semanticObjectRecords"],
    }


def admit_evaluation_authority(value: Any) -> _AdmittedEvaluationAuthorityV1:
    """Validate the complete pre-core chain and mint the sole opaque handle."""
    ep5, c2mod, rimod = _modules()
    if not isinstance(value, dict) or set(value) != AUTHORITY_INPUT_FIELDS:
        raise ValueError("EvaluationAuthorityAdmissionInputV1 is not exact/closed")
    if value.get("schemaVersion") != 1 or value.get("interfaceId") != \
            "opensip-evidence.evaluation-authority-admission.v1":
        raise ValueError("authority admission interface/version mismatch")
    _walk_forbidden(value)
    resolved = value["admittedResolvedInputs"]
    receipt = value["planAuthorityReceipt"]
    admission = value["evaluationAuthorityAdmission"]
    if not isinstance(resolved, dict) or set(resolved) != RESOLVED_FIELDS or resolved.get("schemaVersion") != 1:
        raise ValueError("AdmittedResolvedInputsV1 is not exact")
    if not isinstance(receipt, dict) or set(receipt) != PLAN_RECEIPT_FIELDS or receipt.get("schemaVersion") != 1:
        raise ValueError("PlanAuthorityReceiptV1 is not exact")
    if not isinstance(admission, dict) or set(admission) != ADMISSION_FIELDS or admission.get("schemaVersion") != 1:
        raise ValueError("EvaluationAuthorityAdmissionV1 is not exact")

    project = _exact_project(resolved.get("projectId"), "resolved project")
    if receipt.get("projectId") != project or admission.get("projectId") != project:
        raise ValueError("authority receipts cross ProjectId")
    intent = resolved["frozenPlanIntent"]
    snapshot = resolved["snapshotDescriptor"]
    plan = resolved["planDescriptor"]
    c2_contract = load_json(HERE / "c2-plan-stage-schema.v3.json")
    fact_plane = load_json(HERE / "fact-plane.v1.json")
    relations = set(fact_plane["relationRegistry"]["relations"])
    intent_errors = c2mod.validate_plan_intent(intent, c2_contract, relations)
    if intent_errors:
        raise ValueError(f"pinned C2 rejected PlanIntent: {intent_errors[0]}")
    intent_commitment = c2mod.plan_intent_commitment(intent, c2_contract)
    # Exercise the exact imported canonical byte API too; this is not a syntax check.
    if not c2mod.canonical_plan_intent(intent, c2_contract):
        raise ValueError("pinned C2 canonical PlanIntent unexpectedly empty")
    intent_project = intent.get("analysis", {}).get("admissionDescriptor", {}).get("scope", {}).get("projectId")
    if intent_project != project:
        raise ValueError("PlanIntent ProjectId differs from admitted inputs")

    snapshot_errors = rimod._snapshot_record_errors(snapshot)
    if snapshot_errors:
        raise ValueError(f"pinned RI rejected SnapshotDescriptor: {snapshot_errors[0]}")
    _, snapshot_id = rimod._snapshot_id(snapshot)
    if snapshot.get("projectId") != project:
        raise ValueError("SnapshotDescriptor ProjectId differs")
    if not isinstance(resolved.get("snapshotContentManifest"), list) or \
            any(not isinstance(row, dict) or set(row) != CONTENT_FIELDS
                for row in resolved["snapshotContentManifest"]):
        raise ValueError("snapshot content manifest is not exact/closed")
    if resolved["snapshotContentManifest"] != _content_manifest(snapshot):
        raise ValueError("snapshot content manifest is not derived from the descriptor")

    plan_errors = rimod._plan_record_errors(plan, c2_contract)
    if plan_errors:
        raise ValueError(f"pinned RI rejected PlanDescriptor: {plan_errors[0]}")
    _, plan_id = rimod._plan_id(plan, c2_contract)
    if plan.get("scope", {}).get("projectId") != project:
        raise ValueError("PlanDescriptor ProjectId differs")
    descriptor = intent["analysis"]["admissionDescriptor"]
    for field in ("release", "invocationProfile", "resolvedConfiguration", "scope",
                  "changeSpec", "contributions", "capabilityGrants", "workflow", "budgets"):
        if plan.get(field) != descriptor.get(field):
            raise ValueError(f"PlanDescriptor.{field} differs from admitted PlanIntent")
    if plan.get("snapshotId") != snapshot_id or plan.get("planIntentCommitment") != intent_commitment:
        raise ValueError("PlanDescriptor identity inputs differ from recomputation")

    if receipt != {
        "schemaVersion": 1, "projectId": project,
        "admittedResolvedInputsRef": raw_record_ref("AdmittedResolvedInputsV1", resolved),
        "planIntentRecipe": "opensip.plan-intent.v1",
        "planIntentCommitment": intent_commitment,
        "snapshotRecipe": "SNAPSHOT-ID-V1", "snapshotId": snapshot_id,
        "planRecipe": "PLAN-ID-V1", "planId": plan_id,
    }:
        raise ValueError("PlanAuthorityReceiptV1 differs from exact C2/RI recomputation")

    records = value["authorityObjectRecords"]
    if not isinstance(records, list) or len(records) != 3 or records != sorted(
            records, key=lambda row: (row.get("projectId"), row.get("recordCasRef"), row.get("recordKind"))):
        raise ValueError("authority object records are not exact sorted three-record custody")
    by_kind = {row.get("recordKind"): row for row in records if isinstance(row, dict)}
    if set(by_kind) != set(RAW_KIND_BY_TYPE.values()):
        raise ValueError("authority object record kinds are incomplete/ambiguous")
    refs: dict[str, str] = {}
    for record_type, kind in RAW_KIND_BY_TYPE.items():
        supplied = {"AdmittedResolvedInputsV1": resolved,
                    "PlanAuthorityReceiptV1": receipt,
                    "EvaluationAuthorityAdmissionV1": admission}[record_type]
        decoded, _ = _decode_authority_record(by_kind[kind], record_type, supplied)
        if decoded.get("projectId") != project or by_kind[kind].get("projectId") != project:
            raise ValueError(f"{record_type} physical/project join differs")
        refs[record_type] = by_kind[kind]["recordCasRef"]

    if receipt["admittedResolvedInputsRef"] != refs["AdmittedResolvedInputsV1"] or \
            admission["planAuthorityReceiptRef"] != refs["PlanAuthorityReceiptV1"] or \
            admission.get("planId") != plan_id:
        raise ValueError("receipt-to-resolved-input raw lineage differs")

    semantic_input = {
        "semanticObjectBindings": value["semanticObjectBindings"],
        "semanticObjectRecords": value["semanticObjectRecords"],
    }
    resolved_semantic = ep5.resolve_semantic_object_bindings(semantic_input)
    manifest = resolved_semantic["activation-manifest-v1"]
    seal = resolved_semantic["evaluation-authority-seal-v1"]
    if value["activationManifest"] != manifest["record"] or \
            value["evaluationAuthoritySeal"] != seal["record"]:
        raise ValueError("semantic record values differ from exact raw bytes")
    manifest_binding = manifest["binding"]
    seal_binding = seal["binding"]
    if admission != {
        "schemaVersion": 1, "projectId": project,
        "planAuthorityReceiptRef": refs["PlanAuthorityReceiptV1"],
        "planId": plan_id,
        "activationManifestRef": manifest_binding["semanticRef"],
        "activationManifestRecordRef": manifest_binding["recordCasRef"],
        "evaluationAuthoritySealRef": seal_binding["semanticRef"],
        "evaluationAuthoritySealRecordRef": seal_binding["recordCasRef"],
    }:
        raise ValueError("EvaluationAuthorityAdmissionV1 differs from resolved plan/manifest/seal")
    for field in ("projectId", "planId", "planIntentCommitment"):
        want = {"projectId": project, "planId": plan_id,
                "planIntentCommitment": intent_commitment}[field]
        if value["activationManifest"].get(field) != want or value["evaluationAuthoritySeal"].get(field) != want:
            raise ValueError(f"manifest/seal {field} join differs")
    if value["activationManifest"].get("executionPlanCommitment") != intent_commitment or \
            value["evaluationAuthoritySeal"].get("executionPlanCommitment") != intent_commitment:
        raise ValueError("execution plan commitment differs from admitted PlanIntent")
    if refs["EvaluationAuthorityAdmissionV1"] != raw_record_ref(
            "EvaluationAuthorityAdmissionV1", admission):
        raise ValueError("authority admission raw ref mismatch")

    rows = value["evaluationAuthorityStoreIndex"]
    if not isinstance(rows, list):
        raise ValueError("evaluation authority store index is not an array")
    for row in rows:
        if not isinstance(row, dict) or set(row) != INDEX_FIELDS or row.get("schemaVersion") != 1:
            raise ValueError("EvaluationAuthorityIndexV1 row is not exact")
        _exact_project(row.get("projectId"), "store-index project")
        _exact_ref(row.get("evaluationAuthoritySealRef"), "store-index seal")
        _exact_ref(row.get("evaluationAuthorityAdmissionRef"), "store-index admission")
    matches = [row for row in rows if (row["projectId"], row["evaluationAuthoritySealRef"]) ==
               (project, admission["evaluationAuthoritySealRef"])]
    if len(matches) != 1 or matches[0]["evaluationAuthorityAdmissionRef"] != refs["EvaluationAuthorityAdmissionV1"]:
        raise ValueError("ProjectId/seal store-index lookup is missing, ambiguous, or mismatched")

    expected_edges = [
        {"fromRef": refs["EvaluationAuthorityAdmissionV1"], "toRef": refs["PlanAuthorityReceiptV1"], "projectId": project, "role": "plan-authority-receipt"},
        {"fromRef": refs["EvaluationAuthorityAdmissionV1"], "toRef": seal_binding["recordCasRef"], "projectId": project, "role": "evaluation-authority-seal-record"},
        {"fromRef": refs["EvaluationAuthorityAdmissionV1"], "toRef": manifest_binding["recordCasRef"], "projectId": project, "role": "activation-manifest-record"},
        {"fromRef": refs["PlanAuthorityReceiptV1"], "toRef": refs["AdmittedResolvedInputsV1"], "projectId": project, "role": "admitted-resolved-inputs"},
    ] + [
        {"fromRef": refs["AdmittedResolvedInputsV1"], "toRef": item["recordCasRef"], "projectId": project, "role": "snapshot-content"}
        for item in resolved["snapshotContentManifest"]
    ]
    expected_edges.sort(key=canonical_json)
    edges = value["authorityDependencyEdges"]
    if not isinstance(edges, list) or any(not isinstance(edge, dict) or set(edge) != EDGE_FIELDS
                                          for edge in edges):
        raise ValueError("raw authority dependency edges are not closed")
    if edges != expected_edges:
        raise ValueError("raw authority dependency graph differs from actual receipt graph")
    if any(edge["projectId"] != project or edge["role"] not in ROLE_CAPABILITY
           or edge["fromRef"] == edge["toRef"] for edge in edges):
        raise ValueError("raw authority dependency graph is invalid/cross-project/cyclic")
    return _AdmittedEvaluationAuthorityV1(
        _CAPABILITY_TOKEN, copy.deepcopy(value), _legacy_authority(value, refs), refs)


def _require_handle(value: Any) -> _AdmittedEvaluationAuthorityV1:
    if not isinstance(value, _AdmittedEvaluationAuthorityV1) or value._token is not _CAPABILITY_TOKEN:
        raise TypeError("only module-admitted AdmittedEvaluationAuthorityV1 is accepted")
    return value


def resolve_semantic_object_bindings(authority: Any) -> dict[str, dict[str, Any]]:
    handle = _require_handle(authority)
    return _modules()[0].resolve_semantic_object_bindings(handle._legacy)


def derive_semantic_requirements(authority: Any) -> list[dict[str, str]]:
    handle = _require_handle(authority)
    return _modules()[0].derive_semantic_requirements(handle._legacy)


def derive_dependency_edges(bundle: Any, authority: Any) -> list[dict[str, Any]]:
    handle = _require_handle(authority)
    if not isinstance(bundle, dict) or not isinstance(bundle.get("objectStore"), list):
        raise TypeError("bundle objectStore must be an array")
    edges: list[dict[str, Any]] = []
    for record in bundle["objectStore"]:
        if not isinstance(record, dict) or not isinstance(record.get("dependencies"), list):
            raise ValueError("bundle objectStore record/dependencies malformed")
        for child in record["dependencies"]:
            edges.append({"fromRef": record["ref"], "toRef": child["ref"],
                          "projectId": child["projectId"], "role": child["role"]})
    # The bundle's retained EP5 core projection repeats the admitted
    # admission->seal edge. Both authored surfaces are independently checked;
    # the physical closure canonicalizes their byte-identical witness to one
    # graph edge. A differing role/project is retained and then rejected as a
    # conflicting endpoint pair by derive_transitive_requirements.
    edges.extend(copy.deepcopy(handle._input["authorityDependencyEdges"]))
    unique = {canonical_json(edge): edge for edge in edges}
    return sorted(unique.values(), key=canonical_json)


def derive_transitive_requirements(seed_requirements: dict[str, str],
                                   dependency_edges: list[dict[str, Any]]) -> dict[str, str]:
    if not isinstance(seed_requirements, dict) or not isinstance(dependency_edges, list):
        raise TypeError("requirements/edges have wrong type")
    result: dict[str, str] = {}
    for ref, capability in seed_requirements.items():
        _exact_ref(ref, "seed ref")
        if capability not in CAPABILITY_RANK:
            raise ValueError("unknown seed capability")
        result[ref] = capability
    graph: dict[str, list[str]] = {}
    seen: set[tuple[str, str]] = set()
    parsed = []
    for edge in dependency_edges:
        if not isinstance(edge, dict) or set(edge) != EDGE_FIELDS:
            raise ValueError("dependency edge is not exact/closed")
        if edge["role"] not in set(ROLE_CAPABILITY) | _modules()[0].DEPENDENCY_ROLES:
            raise ValueError("dependency role is unknown")
        _exact_project(edge["projectId"], "edge project")
        _exact_ref(edge["fromRef"], "edge fromRef")
        _exact_ref(edge["toRef"], "edge toRef")
        pair = (edge["fromRef"], edge["toRef"])
        if pair in seen or pair[0] == pair[1]:
            raise ValueError("duplicate/self dependency edge")
        seen.add(pair)
        graph.setdefault(pair[0], []).append(pair[1])
        parsed.append(edge)
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting:
            raise ValueError("dependency graph cycle")
        if node in visited:
            return
        visiting.add(node)
        for child in graph.get(node, []):
            visit(child)
        visiting.remove(node)
        visited.add(node)
    for node in graph:
        visit(node)
    changed = True
    while changed:
        changed = False
        for edge in parsed:
            source = edge["fromRef"]
            if source not in result:
                continue
            capability = ROLE_CAPABILITY.get(edge["role"]) or result[source]
            current = result.get(edge["toRef"])
            if current is None or CAPABILITY_RANK[capability] > CAPABILITY_RANK[current]:
                result[edge["toRef"]] = capability
                changed = True
    unreachable = sorted(source for source in graph if source not in result)
    if unreachable:
        raise ValueError(f"unreachable injected dependency edges: {unreachable}")
    return dict(sorted(result.items()))


def derive_raw_proof_requirements(bundle: Any, authority: Any) -> list[dict[str, str]]:
    handle = _require_handle(authority)
    ep5 = _modules()[0]
    seeds = ep5.derive_seed_requirements(bundle, None)
    admission_ref = handle._raw_refs["EvaluationAuthorityAdmissionV1"]
    graph_ref = handle._input["activationManifest"]["resolvedActivationGraphRef"]
    seeds[admission_ref] = "verifiable"
    seeds[graph_ref] = "replayable"
    requirements = derive_transitive_requirements(seeds, derive_dependency_edges(bundle, handle))
    kinds: dict[str, str] = {}
    for row in bundle["objectStore"]:
        kinds[row["ref"]] = row["kind"]
    for row in handle._input["authorityObjectRecords"]:
        kinds[row["recordCasRef"]] = row["recordKind"]
    kinds[graph_ref] = "resolved-activation-graph"
    for item in handle._input["admittedResolvedInputs"]["snapshotContentManifest"]:
        kinds[item["recordCasRef"]] = item["kind"]
    missing = sorted(set(requirements) - set(kinds))
    if missing:
        raise ValueError(f"raw requirements lack typed record kind: {missing}")
    project = bundle.get("projectId")
    return sorted([{
        "identityKind": "raw-cas", "projectId": project,
        "recordCasRef": ref, "recordKind": kinds[ref],
        "requiredForCapability": capability,
    } for ref, capability in requirements.items()], key=lambda row: (
        row["recordCasRef"], row["recordKind"], row["projectId"]))


def validate_bundle(bundle: Any, authority: Any) -> list[tuple[str, str]]:
    try:
        handle = _require_handle(authority)
    except (TypeError, ValueError) as exc:
        return [("EP6-AUTHORITY", str(exc))]
    if not isinstance(bundle, dict) or bundle.get("projectId") != \
            handle._input["evaluationAuthorityAdmission"]["projectId"]:
        return [("EP6-PROJECT", "bundle ProjectId differs from admitted authority")]
    findings = _modules()[0].validate_bundle(bundle, handle._legacy)
    return findings


def _golden_errors(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for row in contract.get("rawAuthorityGoldens", []):
        if not isinstance(row, dict) or set(row) != {
                "id", "recordType", "domainUtf8", "value", "encodedHex",
                "byteLength", "rawCasRef"}:
            errors.append("raw authority golden is not exact/closed")
            continue
        try:
            encoded = raw_record_bytes(row["recordType"], row["value"])
            if row["domainUtf8"] != DOMAIN_BY_TYPE[row["recordType"]] or \
                    row["encodedHex"] != encoded.hex() or row["byteLength"] != len(encoded) or \
                    row["rawCasRef"] != "sha256:" + hashlib.sha256(encoded).hexdigest():
                errors.append(f"raw authority golden {row.get('id')} does not recompute")
        except Exception as exc:
            errors.append(f"raw authority golden {row.get('id')} invalid: {exc}")
    if len(contract.get("rawAuthorityGoldens", [])) != 3:
        errors.append("exactly three canonical raw authority goldens are required")
    return errors


def check(contract: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(contract, dict):
        return ["root is not an object"]
    try:
        ep5, c2mod, rimod = _modules()
    except Exception as exc:
        return [f"pinned checker import failed: {type(exc).__name__}: {exc}"]
    if (contract.get("artifact"), contract.get("version")) != \
            ("opensip.evaluation-proof", EXPECTED_VERSION):
        errors.append("artifact/version mismatch")
    if contract.get("status") != "CANDIDATE-NOT-APPLIED" or \
            contract.get("sealRecommendation") != "DO-NOT-SEAL":
        errors.append("candidate/no-seal status drift")
    assurance = contract.get("assurance") or {}
    if assurance.get("state") != "SPECIFIED" or \
            assurance.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            assurance.get("candidateState") != "NOT-APPLIED":
        errors.append("assurance exceeds implementable-unexecuted candidate")
    if contract.get("knownLimitations") is None or not all(
            word in json.dumps(contract.get("knownLimitations"))
            for word in ("V10", "CD-RT-5", "G19", "not applied")):
        errors.append("required unresolved/not-applied residuals absent")
    c2 = contract.get("c2AuthorityJoin") or {}
    ri = contract.get("resolvedInputsAuthorityJoin") or {}
    if c2.get("sourceSha256") != PINNED["c2-plan-stage-schema.v3.json"] or \
            c2.get("checkerSha256") != PINNED["check-c2.py"] or \
            set(c2.get("importedCheckerApis") or []) != {
                "validate_plan_intent", "canonical_plan_intent", "plan_intent_commitment"}:
        errors.append("C2 artifact/checker/API pins drift")
    if ri.get("sourceSha256") != PINNED["resolved-inputs.v2.json"] or \
            ri.get("checkerSha256") != PINNED["check-resolved-inputs.py"] or \
            set(ri.get("importedCheckerApis") or []) != {
                "_snapshot_record_errors", "_snapshot_id", "_plan_record_errors",
                "_plan_id", "_materialize_plan_vector"}:
        errors.append("RI artifact/checker/API pins drift")
    capability = contract.get("authorityAdmissionContract") or {}
    if capability.get("capabilityType") != "AdmittedEvaluationAuthorityV1" or \
            capability.get("nonSerializable") is not True or \
            capability.get("nonDisplay") is not True or \
            capability.get("noPublicConstructor") is not True:
        errors.append("opaque capability contract drift")
    if set((contract.get("authorityDependencyGraph") or {}).get("closedRoles") or {}) != set(ROLE_CAPABILITY):
        errors.append("authority dependency role registry drift")
    errors.extend(_golden_errors(contract))

    vectors = contract.get("positiveVectors")
    if not isinstance(vectors, list) or len(vectors) != 7:
        errors.append("expected seven positive vectors")
        return errors
    ids = set()
    for index, vector in enumerate(vectors):
        if not isinstance(vector, dict):
            errors.append(f"vector[{index}] is not an object")
            continue
        ident = vector.get("id")
        if not isinstance(ident, str) or not ident.startswith("EP6-POS-") or ident in ids:
            errors.append(f"vector[{index}] id invalid/duplicate")
        ids.add(ident)
        try:
            handle = admit_evaluation_authority(vector.get("authorityAdmissionInput"))
            findings = validate_bundle(vector.get("bundle"), handle)
            if findings:
                errors.append(f"{ident}: pure core rejected corrected authority: {findings[0]}")
            requirements = derive_raw_proof_requirements(vector["bundle"], handle)
            if not requirements or any(row["identityKind"] != "raw-cas" for row in requirements):
                errors.append(f"{ident}: raw proof closure is empty/non-raw")
            goldens = vector.get("authorityGoldens") or {}
            admission = vector["authorityAdmissionInput"]["evaluationAuthorityAdmission"]
            if goldens.get("evaluationAuthorityAdmissionRef") != raw_record_ref(
                    "EvaluationAuthorityAdmissionV1", admission):
                errors.append(f"{ident}: authority admission golden drift")
            store_golden = goldens.get("evaluationAuthorityStoreIndexRaw") or {}
            store_value = vector["authorityAdmissionInput"]["evaluationAuthorityStoreIndex"][0]
            store_bytes = DOMAIN_BY_TYPE["EvaluationAuthorityIndexV1"].encode() + b"\0" + canonical_json(store_value)
            if store_golden.get("encodedHex") != store_bytes.hex() or \
                    store_golden.get("rawCasRef") != "sha256:" + hashlib.sha256(store_bytes).hexdigest():
                errors.append(f"{ident}: store-index raw golden drift")
        except Exception as exc:
            errors.append(f"{ident}: authority admission failed: {type(exc).__name__}: {exc}")
    if contract.get("acceptedAuthorityVectorId") != "EP6-POS-NOMATCH-PASS":
        errors.append("accepted authority vector id drift")
    required_negatives = {
        "EP6-NEG-PROJECT-SUBSTITUTION", "EP6-NEG-CROSS-PROJECT-VALID-RECEIPTS",
        "EP6-NEG-OPAQUE-RECEIPT-CAS", "EP6-NEG-ARBITRARY-VALID-RECEIPT-CAS",
        "EP6-NEG-OWNER-STRING-OR-BOOLEAN-AUTHORITY", "EP6-NEG-MISSING-STORE-INDEX",
        "EP6-NEG-AMBIGUOUS-STORE-INDEX", "EP6-NEG-RECEIPT-RESOLVED-INPUT-EDGE-REMOVED",
        "EP6-NEG-CALLER-CONSTRUCTED-HANDLE", "EP6-NEG-SERIALIZED-HANDLE",
        "EP6-NEG-TERMINAL-OR-RUN-CYCLE",
    }
    negatives = contract.get("adversarialControlsV6") or []
    if {row.get("id") for row in negatives if isinstance(row, dict)} != required_negatives:
        errors.append("adversarial authority control matrix incomplete")
    return errors


def _must_reject(label: str, value: dict[str, Any], failures: list[str]) -> None:
    try:
        admit_evaluation_authority(value)
        failures.append(f"{label}: escaped authority admission")
    except (KeyError, TypeError, UnicodeError, ValueError, DuplicateKeyError):
        pass


def selftest(contract: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    base_vector = next(row for row in contract["positiveVectors"]
                       if row["id"] == "EP6-POS-NOMATCH-PASS")
    base = base_vector["authorityAdmissionInput"]
    good = admit_evaluation_authority(base)
    if validate_bundle(base_vector["bundle"], good):
        failures.append("positive handle/core control failed")

    mutated = copy.deepcopy(base)
    mutated["admittedResolvedInputs"]["projectId"] = "prj1-" + "b" * 64
    _must_reject("project substitution", mutated, failures)
    mutated = copy.deepcopy(base)
    mutated["evaluationAuthorityStoreIndex"][0]["projectId"] = "prj1-" + "b" * 64
    _must_reject("cross-project store receipt", mutated, failures)
    mutated = copy.deepcopy(base)
    mutated["authorityObjectRecords"][0]["recordBytesHex"] = "00"
    _must_reject("opaque receipt", mutated, failures)
    mutated = copy.deepcopy(base)
    mutated["authorityObjectRecords"][0]["recordCasRef"] = "sha256:" + "c" * 64
    _must_reject("arbitrary valid-looking receipt CAS", mutated, failures)
    mutated = copy.deepcopy(base)
    mutated["verificationOwner"] = "opensip-plan"
    _must_reject("owner string authority", mutated, failures)
    mutated = copy.deepcopy(base)
    mutated["verified"] = True
    _must_reject("boolean authority", mutated, failures)
    mutated = copy.deepcopy(base)
    mutated["evaluationAuthorityStoreIndex"] = []
    _must_reject("missing store index", mutated, failures)
    mutated = copy.deepcopy(base)
    mutated["evaluationAuthorityStoreIndex"].append(
        copy.deepcopy(mutated["evaluationAuthorityStoreIndex"][0]))
    _must_reject("ambiguous store index", mutated, failures)
    mutated = copy.deepcopy(base)
    mutated["authorityDependencyEdges"] = [edge for edge in mutated["authorityDependencyEdges"]
                                            if edge["role"] != "admitted-resolved-inputs"]
    _must_reject("receipt to resolved-input edge removal", mutated, failures)
    mutated = copy.deepcopy(base)
    mutated["evaluationAuthorityAdmission"]["terminal"] = {}
    _must_reject("terminal field/content cycle", mutated, failures)
    mutated = copy.deepcopy(base)
    mutated["admittedResolvedInputs"]["snapshotContentManifest"] = []
    _must_reject("snapshot content edge removal", mutated, failures)
    if not validate_bundle(base_vector["bundle"], copy.deepcopy(base)):
        failures.append("parsed dictionary was accepted as opaque handle")
    try:
        _AdmittedEvaluationAuthorityV1(object(), base, {}, {})
        failures.append("caller constructed opaque handle")
    except TypeError:
        pass
    try:
        json.dumps(good)
        failures.append("opaque handle serialized")
    except TypeError:
        pass
    bundle = copy.deepcopy(base_vector["bundle"])
    bundle["projectId"] = "prj1-" + "b" * 64
    if not validate_bundle(bundle, good):
        failures.append("bundle project substitution escaped")

    # Every named successor negative must be backed by at least one executable
    # mutation above, and artifact-level tampering must be detected too.
    changed = copy.deepcopy(contract)
    changed["c2AuthorityJoin"]["checkerSha256"] = "0" * 64
    if not check(changed, verify_files=False):
        failures.append("C2 checker pin mutation escaped")
    changed = copy.deepcopy(contract)
    changed["rawAuthorityGoldens"][0]["encodedHex"] = "00"
    if not check(changed, verify_files=False):
        failures.append("raw golden mutation escaped")
    return failures


def main(argv: list[str]) -> int:
    path = HERE / BINDING
    selftest_mode = "--selftest" in argv[1:]
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    if positional:
        path = pathlib.Path(positional[0])
    try:
        contract = load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    findings = check(contract)
    if findings:
        for finding in findings:
            print(f"FAIL: {finding}")
        return 1
    if selftest_mode:
        failures = selftest(contract)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print("PASS: evaluation-proof.v6.json; 7 same-project authority vectors; 15 executable adversarial controls")
    else:
        accepted = next(row for row in contract["positiveVectors"]
                        if row["id"] == "EP6-POS-NOMATCH-PASS")
        handle = admit_evaluation_authority(accepted["authorityAdmissionInput"])
        rows = derive_raw_proof_requirements(accepted["bundle"], handle)
        counts = {cap: sum(row["requiredForCapability"] == cap for row in rows)
                  for cap in ("verifiable", "replayable")}
        print(f"PASS: evaluation-proof.v6.json; {len(rows)} derived raw refs "
              f"({counts['verifiable']} verifiable/{counts['replayable']} replayable); "
              "RR13-01 specified/implementable-unexecuted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
