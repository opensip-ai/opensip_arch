#!/usr/bin/env python3
"""Total retained checker for the Phase-1A evaluation-proof v5 contract.

The public helpers in this module are intentionally small and pure so another
contract can consume the same byte grammar and proof-dependency derivation:

  frame_component(tag, value)             -> typed/length-framed UTF-8 bytes
  encode_member(evaluation_id, predicate_id)
  encode_outcome(evaluation_id, predicate_id, outcome)
  commit(domain, items)                    -> full SHA-256 Merkle commitment
  encode_activation_manifest(manifest)     -> closed ActivationManifestV1 bytes
  derive_activation_manifest_ref(manifest) -> content-addressed manifest ref
  encode_semantic_object_binding(binding)   -> canonical derived-witness bytes
  resolve_semantic_object_bindings(authority)
                                           -> exact semantic-to-raw record map
  derive_semantic_requirements(authority)   -> typed semantic roots
  derive_raw_proof_requirements(bundle, authority)
                                           -> typed physical raw-CAS closure
  derive_authority_members(authority)       -> exact activated member IDs
  validate_bundle(bundle, authority)        -> fixed-authority bundle validation
  derive_verdict(bundle)                   -> policy-ir-2 core verdict
  derive_seed_requirements(bundle)         -> direct {ref: minimum capability}
  derive_transitive_requirements(seeds, dependency_edges)
  derive_proof_requirements(bundle, dependency_edges=None)
                                           -> complete {ref: minimum capability}
  derive_verdict_commitment(bundle)        -> policy-input commitment

Every validation entry point is total over successfully parsed JSON values.
Malformed roots and hostile nested values produce findings, never tracebacks.

Usage: python3 artifacts/check-evaluation-proof.py [contract] [--selftest]
Exit: 0 clean; 1 findings; 2 I/O or JSON syntax error.
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
from typing import Any, Callable

BINDING = "evaluation-proof.v5.json"
HERE = pathlib.Path(__file__).resolve().parent
NS = b"opensip.evaluation-proof.v2"
EXPECTED_VERSION = 5
EXPECTED_GRAMMAR_SHA256 = "343889cf713931b0e228d84de82cb67d8cb22cc13ae2b3cc71302476f89ef9e0"
VERSIONING = "versioning-policy.v4.json"
VERSIONING_SHA256 = "8e6933b287a8082ea27647860938bd9cdae93b37132bba21221c2c24b40069e6"
C2 = "c2-plan-stage-schema.v3.json"
C2_CHECKER = "check-c2.py"

REF_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PROJECT_RE = re.compile(r"^prj1-[0-9a-f]{64}$")
RUN_RE = re.compile(r"^run1:[0-9a-f]{64}$")
PLAN_RE = re.compile(r"^plan1:sha256:[0-9a-f]{64}$")
EVALUATION_RE = re.compile(r"^eval1:[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$")
PREDICATE_RE = re.compile(r"^predicate1:[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$")
ACTIVATION_RE = re.compile(r"^act1:[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$")
WAIVER_RE = re.compile(r"^waiver1:[a-z0-9][a-z0-9._:-]{0,127}$")
GENERIC_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._:#/-][a-z0-9]+)*$")

OUTCOMES = {"match", "no-match", "indeterminate", "error"}
SHAPES = {
    "local-match", "relationship-match", "aggregate-match", "no-match",
    "indeterminate", "error",
}
VERDICTS = {"pass", "fail", "advisory", "indeterminate"}
PAIRING = {
    "local-match": "match",
    "relationship-match": "match",
    "aggregate-match": "match",
    "no-match": "no-match",
    "indeterminate": "indeterminate",
    "error": "error",
}
CAPABILITY_RANK = {"recorded": 0, "verifiable": 1, "replayable": 2}
DEPENDENCY_ROLE_ORDER = [
    "coverage-fact-partition", "coverage-predicate-semantics", "partition-fact",
    "predicate-verifier", "policy-verifier", "verifier-signature", "fact-anchor",
    "replay-input", "historical-semantics", "historical-manifest",
    "historical-executable", "historical-signature", "historical-trust-root",
    "historical-public-key", "evaluation-authority-seal-record",
    "activation-manifest-record",
]
DEPENDENCY_ROLES = {
    "coverage-fact-partition", "coverage-predicate-semantics", "partition-fact",
    "predicate-verifier", "policy-verifier", "verifier-signature", "fact-anchor",
    "replay-input", "historical-semantics", "historical-manifest",
    "historical-executable", "historical-signature", "historical-trust-root",
    "historical-public-key", "evaluation-authority-seal-record",
    "activation-manifest-record",
}
HISTORICAL_DEPENDENCIES = {
    "historical-semantics": "sha256:d6a8d086d9ee0f2693f599ce39ecf90c0be65fd9a9127ddfd95572a2c95c3e04",
    "historical-manifest": "sha256:11e923bffcc99c94372d7b575d733b79787da09d5d06286732c691b1158828fa",
    "historical-executable": "sha256:e3be6c3634ac045fd02d4753ac61ed6d9b82ea161e106c143de69a2f196467a5",
    "historical-signature": "sha256:249a77c07b91bd865b4873c586ea4e41681be89d8d227590bfc44a3b33402ac5",
    "historical-trust-root": "sha256:b4834d2eb7324dbde0aa0c9c461bedaae1ba6317b02fd441612b96dd4b4778bf",
    "historical-public-key": "sha256:21fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9",
}
POLICY_EVALUATION_ORDER = [
    "indeterminate-or-error-dominates",
    "validate-exact-waivers",
    "suppress-waived-current-matches",
    "classify-effective-new-match-as-fail",
    "classify-effective-baseline-match-as-advisory",
    "classify-no-effective-match-as-pass",
]

TOP_KEYS = {
    "artifact", "version", "status", "author", "date", "claimId", "role",
    "supersedesProofObligationsOf", "repairs", "canonicalCommitmentGrammar",
    "normativePreimageGrammarSha256", "normativePreimageGrammar", "preimageGoldens",
    "wireGrammars", "persistedSchemaRegistry", "policySemanticsV2",
    "activationAuthority", "authoritySeam", "versioningV4RoleJoin", "c2AuthorityJoin",
    "proofObligationsByClaimShape", "invariants", "positiveVectors",
    "adversarialNegatives", "crossLanguageGoldens", "collisionControls",
    "decisionDependencies", "assurance", "knownLimitations", "sealRecommendation",
    "referenceTypeRegistry", "semanticObjectBindingContract",
}
BUNDLE_REQUIRED = {
    "schemaVersion", "projectId", "evaluationAuthoritySealRef", "objectStore", "partitionContents",
    "requiredUniverse", "evaluations", "replayClosureRefs", "verdictProof",
}
EVALUATION_REQUIRED = {
    "evaluationId", "predicateId", "outcome", "claimShape",
    "predicateSemanticsRef", "coverageRef", "proof",
}
SCHEMA_FIELDS: dict[str, tuple[set[str], set[str]]] = {
    "EvaluationProofBundleV5": (BUNDLE_REQUIRED, set()),
    "ActivationManifestV1": ({"schemaVersion", "projectId", "planId", "planIntentCommitment", "executionPlanCommitment", "resolvedActivationGraphRef", "members"}, set()),
    "ActivationMemberV1": ({"evaluationId", "predicateId", "claimShape", "coverageRef", "ruleActivationId", "predicateActivationId", "policyActivationId"}, set()),
    "VerifiedEvaluationAuthorityInputV2": ({"schemaVersion", "interfaceId", "suppliedBy", "planIdAdmission", "authoritySealAdmission", "evaluationAuthoritySeal", "activationManifest", "semanticObjectBindings", "semanticObjectRecords"}, set()),
    "PlanIdAdmissionV1": ({"verificationOwner", "planIdRecipe", "admittedResolvedInputsRef", "verifiedPlanId", "verificationReceiptRef"}, set()),
    "AuthoritySealAdmissionV1": ({"verificationOwner", "projectId", "resolvedEvaluationAuthoritySealRef", "sealedActivationManifestRef", "verificationReceiptRef"}, set()),
    "EvaluationAuthoritySealV1": ({"schemaVersion", "projectId", "planId", "planIntentCommitment", "executionPlanCommitment", "activationManifestRef"}, set()),
    "RawObjectRecordV3": ({"ref", "projectId", "kind", "dependencies"}, set()),
    "RawObjectDependencyV2": ({"ref", "projectId", "role"}, set()),
    "RawDependencyEdgeV2": ({"fromRef", "toRef", "projectId", "role"}, set()),
    "SemanticObjectBindingV1": ({"projectId", "semanticDomain", "semanticRef", "recordCasRef", "recordKind"}, set()),
    "SemanticObjectRecordV1": ({"projectId", "recordCasRef", "recordKind", "recordBytesHex"}, set()),
    "PartitionRecordV2": ({"partitionRef", "projectId", "members"}, set()),
    "RequiredUniverseV2": ({"declaredCount", "memberIds", "universeCommitment"}, set()),
    "MemberIdV2": ({"evaluationId", "predicateId"}, set()),
    "EvaluationV2": (EVALUATION_REQUIRED, set()),
    "LocalMatchProofV2": ({"kind", "subjectId", "factRefs"}, {"spanAnchor"}),
    "RelationshipMatchProofV2": ({"kind", "relationSemanticsRef", "witnessEdges", "factRefs"}, set()),
    "WitnessEdgeV1": ({"fromSubjectId", "toSubjectId", "relationKind", "factRef"}, set()),
    "AggregateMatchProofV2": ({"kind", "memberSetCommitment", "memberCount", "factPartitionRef", "foldSpec", "factRefs"}, set()),
    "NoMatchProofV2": ({"kind", "subjectSetCommitment", "subjectCount", "factPartitionRef"}, set()),
    "ReasonProofV2": ({"kind", "reasonRef"}, {"partialSubjectCount", "factRefs"}),
    "ReplayClosureRefV1": ({"ref", "projectId"}, set()),
    "VerdictProofV2": ({"verdict", "outcomeSetCommitment", "coverage", "baseline", "waivers", "waiverSetCommitment", "policy", "derivationCommitment"}, set()),
    "CoverageInputV1": ({"status", "coverageRef", "projectId"}, set()),
    "BaselineNoneV1": ({"kind"}, set()),
    "BaselineComparisonV1": ({"kind", "baselineRef", "projectId", "matchedMembers"}, set()),
    "WaiverV1": ({"waiverId", "waiverRef", "projectId", "target", "disposition"}, set()),
    "PolicyInputV2": ({"policyRef", "projectId", "semanticsVersion", "evaluationOrder", "matchDisposition", "baselineDisposition", "waivedDisposition", "noMatchDisposition", "incompleteDisposition"}, set()),
    "SpanAnchorV1": ({"line", "column"}, set()),
}

EXPECTED_REFERENCE_TYPE_REGISTRY = {
    "sha256LexicalPattern": r"^sha256:[0-9a-f]{64}$",
    "newtypes": {
        "SemanticCommitmentRef": "domain-separated semantic equality only; never a physical path, inventory, availability, lease, or purge key",
        "RawCasRef": "SHA-256 of exact stored bytes; only this type may enter ObjectRecord, physical custody, availability, lease, inventory, path, or purge APIs",
        "CommitmentDigest": "domain-separated proof/set digest with no implied retrievable record",
    },
    "semanticCommitmentFields": [
        "EvaluationProofBundleV5.evaluationAuthoritySealRef",
        "AuthoritySealAdmissionV1.resolvedEvaluationAuthoritySealRef",
        "AuthoritySealAdmissionV1.sealedActivationManifestRef",
        "EvaluationAuthoritySealV1.activationManifestRef",
        "SemanticObjectBindingV1.semanticRef",
    ],
    "rawCasFields": [
        "RawObjectRecordV3.ref", "RawObjectDependencyV2.ref",
        "RawDependencyEdgeV2.fromRef", "RawDependencyEdgeV2.toRef",
        "SemanticObjectBindingV1.recordCasRef", "SemanticObjectRecordV1.recordCasRef",
        "PlanIdAdmissionV1.admittedResolvedInputsRef", "PlanIdAdmissionV1.verificationReceiptRef",
        "AuthoritySealAdmissionV1.verificationReceiptRef",
        "ActivationManifestV1.resolvedActivationGraphRef", "ActivationMemberV1.coverageRef",
        "EvaluationV2.predicateSemanticsRef", "EvaluationV2.coverageRef",
        "LocalMatchProofV2.factRefs[]", "RelationshipMatchProofV2.relationSemanticsRef",
        "RelationshipMatchProofV2.factRefs[]", "WitnessEdgeV1.factRef",
        "AggregateMatchProofV2.factPartitionRef", "AggregateMatchProofV2.factRefs[]",
        "NoMatchProofV2.factPartitionRef", "ReasonProofV2.reasonRef", "ReasonProofV2.factRefs[]",
        "ReplayClosureRefV1.ref", "PartitionRecordV2.partitionRef",
        "CoverageInputV1.coverageRef", "BaselineComparisonV1.baselineRef",
        "WaiverV1.waiverRef", "PolicyInputV2.policyRef",
    ],
    "nonRetrievableCommitmentSuffixes": ["Commitment", "SetCommitment"],
    "rule": "Lexical sha256 form never determines type; the closed schema field/newtype does. SemanticCommitmentRef and RawCasRef are non-interchangeable Rust newtypes.",
}

EXPECTED_SEMANTIC_BINDING_CONTRACT = {
    "type": "SemanticObjectBindingV1",
    "key": ["projectId", "semanticDomain", "semanticRef"],
    "fields": ["projectId", "semanticDomain", "semanticRef", "recordCasRef", "recordKind"],
    "initialMappings": [
        {"semanticDomain": "activation-manifest-v1", "recordKind": "ActivationManifestV1"},
        {"semanticDomain": "evaluation-authority-seal-v1", "recordKind": "EvaluationAuthoritySealV1"},
    ],
    "resolver": [
        "resolve exactly one binding by (ProjectId,semanticDomain,semanticRef)",
        "fetch exactly one typed SemanticObjectRecordV1 by (ProjectId,recordCasRef,recordKind)",
        "verify RawCasRef equals SHA-256 of exact recordBytesHex bytes",
        "closed-decode bytes as recordKind under the EP5 grammar",
        "canonical byte-identical re-encode the decoded value",
        "recompute semanticDomain commitment over the complete canonical record bytes and require semanticRef equality",
    ],
    "physicalKey": ["projectId", "recordCasRef", "recordKind"],
    "bindingAuthority": "DERIVED-WITNESS-ONLY; a binding without its raw target confers no capability",
    "rawGraphRule": "RawObjectRecordV3 and every RawObjectDependencyV2/RawDependencyEdgeV2 endpoint are RawCasRef; SemanticCommitmentRef is forbidden.",
    "forbiddenBindingFields": [
        "bindingId", "requestId", "executionId", "runId", "runSealRef", "evidenceDigest",
        "verdict", "outcome", "sealedCapability", "effectiveCapability", "objectState",
        "lease", "fence", "ledger", "clocks", "physicalLocators",
    ],
}


class DuplicateKeyError(ValueError):
    pass


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(f"duplicate JSON object key {key!r}")
        out[key] = value
    return out


def _load_module(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_c2_module():
    return _load_module(HERE / C2_CHECKER, "check_c2_for_evaluation_proof_v3")


def _sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


_ACTIVE_GRAMMAR: Any = None


def _set_active_grammar(value: Any) -> None:
    global _ACTIVE_GRAMMAR
    _ACTIVE_GRAMMAR = value


def _grammar() -> dict[str, Any]:
    """Return the binding grammar; no checker-local tag table is authoritative."""
    global _ACTIVE_GRAMMAR
    if _ACTIVE_GRAMMAR is None:
        _ACTIVE_GRAMMAR = json.loads((HERE / BINDING).read_text())["normativePreimageGrammar"]
    if not isinstance(_ACTIVE_GRAMMAR, dict):
        raise ValueError("normativePreimageGrammar must be an object")
    return _ACTIVE_GRAMMAR


def _hex_tag(value: Any, path: str) -> int:
    if not isinstance(value, str) or not re.fullmatch(r"0x[0-9a-f]{2}", value):
        raise ValueError(f"{path} must be a lowercase 0xNN byte tag")
    return int(value, 16)


def _record_schema(name: str) -> dict[str, Any]:
    records = _grammar().get("records")
    if not isinstance(records, list):
        raise ValueError("grammar.records must be an array")
    matches = [row for row in records if isinstance(row, dict) and row.get("name") == name]
    if len(matches) != 1:
        raise ValueError(f"grammar must declare exactly one {name}")
    return matches[0]


def _record_tag(name: str) -> int:
    return _hex_tag(_record_schema(name).get("recordTag"), f"{name}.recordTag")


def _field_tag(record_name: str, field_name: str) -> int:
    fields = _record_schema(record_name).get("fields")
    if not isinstance(fields, list):
        raise ValueError(f"{record_name}.fields must be an array")
    matches = [row for row in fields if isinstance(row, dict) and row.get("name") == field_name]
    if len(matches) != 1:
        raise ValueError(f"grammar must declare exactly one {record_name}.{field_name}")
    return _hex_tag(matches[0].get("tag"), f"{record_name}.{field_name}.tag")


def _declared_order(record_name: str) -> list[str]:
    order = _record_schema(record_name).get("order")
    if not isinstance(order, list) or any(not isinstance(x, str) for x in order):
        raise ValueError(f"{record_name}.order must be a string array")
    field_names = [row.get("name") for row in _record_schema(record_name).get("fields", [])
                   if isinstance(row, dict)]
    if order != field_names:
        raise ValueError(f"{record_name}.order must exactly enumerate declared fields")
    return order


def _encode_text_record(record_name: str, values: dict[str, str]) -> bytes:
    order = _declared_order(record_name)
    if set(values) != set(order):
        raise ValueError(f"{record_name} text encoder values differ from declared fields")
    return (bytes([_record_tag(record_name)])
            + b"".join(frame_component(_field_tag(record_name, name), values[name])
                       for name in order))


def _require_declared_order(record_name: str, expected: list[str]) -> None:
    if _declared_order(record_name) != expected:
        raise ValueError(f"{record_name} nesting/order differs from executable encoder")


def _commitment_tag(section: str, key: str = "tag") -> int:
    commitment = _grammar().get("commitment")
    if not isinstance(commitment, dict) or not isinstance(commitment.get(section), dict):
        raise ValueError(f"grammar.commitment.{section} must be an object")
    return _hex_tag(commitment[section].get(key), f"commitment.{section}.{key}")


def frame_component(tag: int, value: str) -> bytes:
    """Encode one logical UTF-8 component injectively.

    The one-byte type tag distinguishes component roles and the uint32be length
    distinguishes boundaries. This function deliberately does not validate the
    value grammar so collision controls can show that even hostile U+001F input
    remains byte-distinct; persisted identifiers are validated before commit.
    """
    if not isinstance(tag, int) or isinstance(tag, bool) or not 0 <= tag <= 255:
        raise ValueError("component tag must be an unsigned byte")
    if not isinstance(value, str):
        raise TypeError("component value must be a string")
    raw = value.encode("utf-8")
    if len(raw) > 0xFFFFFFFF:
        raise ValueError("component exceeds uint32 length")
    return bytes([tag]) + len(raw).to_bytes(4, "big") + raw


def _frame_blob(tag: int, value: bytes) -> bytes:
    if not isinstance(value, bytes):
        raise TypeError("blob value must be bytes")
    return bytes([tag]) + len(value).to_bytes(4, "big") + value


def encode_member(evaluation_id: str, predicate_id: str) -> bytes:
    return _encode_text_record("MemberV1", {"evaluationId": evaluation_id, "predicateId": predicate_id})


def encode_outcome(evaluation_id: str, predicate_id: str, outcome: str) -> bytes:
    return _encode_text_record("OutcomeV1", {
        "evaluationId": evaluation_id, "predicateId": predicate_id, "outcome": outcome,
    })


def encode_subject(value: str) -> bytes:
    return _encode_text_record("SubjectV1", {"value": value})


def encode_waiver(value: dict[str, Any]) -> bytes:
    target = value["target"]
    return _encode_text_record("WaiverV1", {
        "waiverId": value["waiverId"], "waiverRef": value["waiverRef"],
        "target.evaluationId": target["evaluationId"],
        "target.predicateId": target["predicateId"], "disposition": value["disposition"],
    })


def encode_activation_member(member: dict[str, Any]) -> bytes:
    """Canonical ActivationMemberV1 record; every authority-bearing role is framed."""
    return _encode_text_record("ActivationMemberV1", {
        key: member[key] for key in ("evaluationId", "predicateId", "claimShape", "coverageRef",
                                    "ruleActivationId", "predicateActivationId", "policyActivationId")
    })


def encode_activation_manifest(manifest: dict[str, Any]) -> bytes:
    """Canonical bytes resolved from a closed ActivationManifestV1 value."""
    members = sorted(encode_activation_member(member) for member in manifest["members"])
    _require_declared_order("ActivationManifestV1", [
        "schemaVersion", "projectId", "planId", "planIntentCommitment",
        "executionPlanCommitment", "resolvedActivationGraphRef", "members", "members[]",
    ])
    return (bytes([_record_tag("ActivationManifestV1")])
            + frame_component(_field_tag("ActivationManifestV1", "schemaVersion"), str(manifest["schemaVersion"]))
            + b"".join(frame_component(_field_tag("ActivationManifestV1", key), manifest[key])
                       for key in ("projectId", "planId", "planIntentCommitment",
                                   "executionPlanCommitment", "resolvedActivationGraphRef"))
            + _frame_blob(_field_tag("ActivationManifestV1", "members"),
                          b"".join(_frame_blob(_field_tag("ActivationManifestV1", "members[]"), member)
                                   for member in members)))


def derive_activation_manifest_ref(manifest: dict[str, Any]) -> str:
    return commit("activation-manifest-v1", [encode_activation_manifest(manifest)])


def encode_evaluation_authority_seal(seal: dict[str, Any]) -> bytes:
    """Canonical pre-evaluation authority bytes, derived only from EP5 grammar."""
    return _encode_text_record("EvaluationAuthoritySealV1", {
        "schemaVersion": str(seal["schemaVersion"]),
        "projectId": seal["projectId"],
        "planId": seal["planId"],
        "planIntentCommitment": seal["planIntentCommitment"],
        "executionPlanCommitment": seal["executionPlanCommitment"],
        "activationManifestRef": seal["activationManifestRef"],
    })


def derive_evaluation_authority_seal_ref(seal: dict[str, Any]) -> str:
    return commit("evaluation-authority-seal-v1", [encode_evaluation_authority_seal(seal)])


def encode_semantic_object_binding(binding: dict[str, Any]) -> bytes:
    """Canonical ordering bytes for the derived SemanticObjectBindingV1 witness."""
    return _encode_text_record("SemanticObjectBindingV1", {
        key: binding[key] for key in (
            "projectId", "semanticDomain", "semanticRef", "recordCasRef", "recordKind")
    })


def _read_blob_frame(data: bytes, offset: int, expected_tag: int) -> tuple[bytes, int]:
    if offset + 5 > len(data) or data[offset] != expected_tag:
        raise ValueError(f"expected frame tag 0x{expected_tag:02x} at byte {offset}")
    length = int.from_bytes(data[offset + 1:offset + 5], "big")
    end = offset + 5 + length
    if end > len(data):
        raise ValueError("truncated frame payload")
    return data[offset + 5:end], end


def _decoded_text(raw: bytes) -> str:
    value = raw.decode("utf-8")
    if not value or unicodedata.normalize("NFC", value) != value:
        raise ValueError("record text is empty or non-NFC")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value):
        raise ValueError("record text contains a forbidden control character")
    return value


def _read_text_frame(data: bytes, offset: int, record_name: str,
                     field_name: str) -> tuple[str, int]:
    raw, end = _read_blob_frame(data, offset, _field_tag(record_name, field_name))
    return _decoded_text(raw), end


def decode_activation_member(data: bytes) -> dict[str, Any]:
    if not data or data[0] != _record_tag("ActivationMemberV1"):
        raise ValueError("ActivationMemberV1 record tag mismatch")
    offset = 1
    result: dict[str, Any] = {}
    for field in ("evaluationId", "predicateId", "claimShape", "coverageRef",
                  "ruleActivationId", "predicateActivationId", "policyActivationId"):
        result[field], offset = _read_text_frame(data, offset, "ActivationMemberV1", field)
    if offset != len(data):
        raise ValueError("ActivationMemberV1 has trailing or undeclared bytes")
    return result


def decode_activation_manifest(data: bytes) -> dict[str, Any]:
    if not data or data[0] != _record_tag("ActivationManifestV1"):
        raise ValueError("ActivationManifestV1 record tag mismatch")
    offset = 1
    version, offset = _read_text_frame(data, offset, "ActivationManifestV1", "schemaVersion")
    if not re.fullmatch(r"0|[1-9][0-9]*", version):
        raise ValueError("ActivationManifestV1 schemaVersion is not canonical unsigned decimal")
    result: dict[str, Any] = {"schemaVersion": int(version)}
    for field in ("projectId", "planId", "planIntentCommitment",
                  "executionPlanCommitment", "resolvedActivationGraphRef"):
        result[field], offset = _read_text_frame(data, offset, "ActivationManifestV1", field)
    members_blob, offset = _read_blob_frame(
        data, offset, _field_tag("ActivationManifestV1", "members"))
    if offset != len(data):
        raise ValueError("ActivationManifestV1 has trailing or undeclared bytes")
    members: list[dict[str, Any]] = []
    item_offset = 0
    while item_offset < len(members_blob):
        member_bytes, item_offset = _read_blob_frame(
            members_blob, item_offset, _field_tag("ActivationManifestV1", "members[]"))
        members.append(decode_activation_member(member_bytes))
    if not members:
        raise ValueError("ActivationManifestV1 members cannot be empty")
    result["members"] = members
    return result


def decode_evaluation_authority_seal(data: bytes) -> dict[str, Any]:
    if not data or data[0] != _record_tag("EvaluationAuthoritySealV1"):
        raise ValueError("EvaluationAuthoritySealV1 record tag mismatch")
    offset = 1
    version, offset = _read_text_frame(data, offset, "EvaluationAuthoritySealV1", "schemaVersion")
    if not re.fullmatch(r"0|[1-9][0-9]*", version):
        raise ValueError("EvaluationAuthoritySealV1 schemaVersion is not canonical unsigned decimal")
    result: dict[str, Any] = {"schemaVersion": int(version)}
    for field in ("projectId", "planId", "planIntentCommitment",
                  "executionPlanCommitment", "activationManifestRef"):
        result[field], offset = _read_text_frame(data, offset, "EvaluationAuthoritySealV1", field)
    if offset != len(data):
        raise ValueError("EvaluationAuthoritySealV1 has trailing or undeclared bytes")
    return result


SEMANTIC_RECORD_KINDS = {
    "activation-manifest-v1": "ActivationManifestV1",
    "evaluation-authority-seal-v1": "EvaluationAuthoritySealV1",
}


def resolve_semantic_object_bindings(authority: Any) -> dict[str, dict[str, Any]]:
    """Resolve exactly two typed semantic roots to exact canonical raw record bytes.

    Bindings are derived witnesses, never authority: each row must resolve one
    ProjectId-scoped raw record, whose exact bytes hash, closed decode, canonical
    byte-identical re-encode, and semantic domain commitment all recompute.
    """
    if not isinstance(authority, dict):
        raise TypeError("authority input must be an object")
    bindings = authority.get("semanticObjectBindings")
    records = authority.get("semanticObjectRecords")
    if not isinstance(bindings, list) or not isinstance(records, list):
        raise TypeError("authority input must carry binding and raw-record arrays")
    binding_fields = SCHEMA_FIELDS["SemanticObjectBindingV1"][0]
    record_fields = SCHEMA_FIELDS["SemanticObjectRecordV1"][0]
    if any(not isinstance(row, dict) or set(row) != binding_fields for row in bindings):
        raise ValueError("SemanticObjectBindingV1 rows must be recursively closed")
    if any(not isinstance(row, dict) or set(row) != record_fields for row in records):
        raise ValueError("SemanticObjectRecordV1 rows must be recursively closed")
    if bindings != sorted(bindings, key=encode_semantic_object_binding):
        raise ValueError("semantic bindings must be strict canonical byte order")
    keys = [(row["projectId"], row["semanticDomain"], row["semanticRef"]) for row in bindings]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate semantic binding key")
    physical_keys = [(row["projectId"], row["recordCasRef"], row["recordKind"])
                     for row in records]
    if records != sorted(records, key=lambda row: (
            row["projectId"], row["recordCasRef"], row["recordKind"])):
        raise ValueError("semantic raw records must be strict physical-key order")
    if len(physical_keys) != len(set(physical_keys)):
        raise ValueError("duplicate semantic raw-record physical key")
    record_map = {key: row for key, row in zip(physical_keys, records)}
    if len(bindings) != 2 or len(records) != 2:
        raise ValueError("exactly two initial semantic bindings and raw records are required")

    resolved: dict[str, dict[str, Any]] = {}
    seen_domains: set[str] = set()
    for binding in bindings:
        domain = binding["semanticDomain"]
        if domain not in SEMANTIC_RECORD_KINDS or binding["recordKind"] != SEMANTIC_RECORD_KINDS[domain]:
            raise ValueError("semantic binding domain/recordKind mapping is unknown or mismatched")
        if domain in seen_domains:
            raise ValueError("semantic binding domain is ambiguous")
        seen_domains.add(domain)
        for key in ("semanticRef", "recordCasRef"):
            if not isinstance(binding[key], str) or not REF_RE.fullmatch(binding[key]):
                raise ValueError(f"semantic binding {key} is malformed")
        if not isinstance(binding["projectId"], str) or not PROJECT_RE.fullmatch(binding["projectId"]):
            raise ValueError("semantic binding ProjectId is malformed")
        physical = (binding["projectId"], binding["recordCasRef"], binding["recordKind"])
        record = record_map.get(physical)
        if record is None:
            raise ValueError("semantic binding has no exact typed raw target")
        raw_hex = record["recordBytesHex"]
        if not isinstance(raw_hex, str) or not re.fullmatch(r"(?:[0-9a-f]{2})+", raw_hex):
            raise ValueError("semantic raw record bytes must be non-empty lowercase hexadecimal")
        raw = bytes.fromhex(raw_hex)
        raw_ref = "sha256:" + hashlib.sha256(raw).hexdigest()
        if raw_ref != binding["recordCasRef"] or raw_ref != record["recordCasRef"]:
            raise ValueError("raw record CAS digest does not match exact stored bytes")
        if domain == "activation-manifest-v1":
            decoded = decode_activation_manifest(raw)
            canonical = encode_activation_manifest(decoded)
            semantic_ref = derive_activation_manifest_ref(decoded)
        else:
            decoded = decode_evaluation_authority_seal(raw)
            canonical = encode_evaluation_authority_seal(decoded)
            semantic_ref = derive_evaluation_authority_seal_ref(decoded)
        if canonical != raw:
            raise ValueError("decoded record does not byte-identically re-encode canonically")
        if decoded.get("projectId") != binding["projectId"]:
            raise ValueError("decoded semantic record crosses ProjectId")
        if semantic_ref != binding["semanticRef"]:
            raise ValueError("semantic commitment does not recompute from exact full record bytes")
        if binding["semanticRef"] == binding["recordCasRef"]:
            raise ValueError("semantic commitment is aliased as raw CAS identity")
        resolved[domain] = {"binding": binding, "record": decoded, "bytes": raw}
    if set(resolved) != set(SEMANTIC_RECORD_KINDS):
        raise ValueError("semantic binding set is incomplete")
    seal = resolved["evaluation-authority-seal-v1"]["record"]
    manifest_ref = resolved["activation-manifest-v1"]["binding"]["semanticRef"]
    if seal.get("activationManifestRef") != manifest_ref:
        raise ValueError("authority seal does not semantically link the resolved activation manifest")
    return resolved


def derive_semantic_requirements(authority: Any) -> list[dict[str, str]]:
    resolved = resolve_semantic_object_bindings(authority)
    return sorted([{
        "identityKind": "semantic-commitment",
        "projectId": item["binding"]["projectId"],
        "semanticDomain": domain,
        "semanticRef": item["binding"]["semanticRef"],
        "recordKind": item["binding"]["recordKind"],
        "requiredForCapability": "verifiable",
    } for domain, item in resolved.items()], key=lambda row: (
        row["projectId"], row["semanticDomain"], row["semanticRef"], row["recordKind"]))


def derive_authority_members(authority: dict[str, Any]) -> list[dict[str, str]]:
    """Derive member IDs only from the admitted envelope (or its inner value)."""
    manifest = resolve_semantic_object_bindings(authority)["activation-manifest-v1"]["record"]
    members = manifest["members"]
    ordered = sorted(members, key=encode_activation_member)
    return [{"evaluationId": row["evaluationId"], "predicateId": row["predicateId"]}
            for row in ordered]


def _leaf(value: bytes) -> bytes:
    return hashlib.sha256(bytes([_commitment_tag("leaf")]) + len(value).to_bytes(8, "big") + value).digest()


def _node(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(bytes([_commitment_tag("internal")]) + left + right).digest()


def _merkle(items: list[bytes]) -> bytes:
    ordered = sorted(set(items))
    if not ordered:
        empty = _grammar()["commitment"]["empty"]
        return hashlib.sha256(bytes([_hex_tag(empty.get("tag"), "commitment.empty.tag")])
                              + _frame_blob(_hex_tag(empty.get("namespaceBlobTag"), "commitment.empty.namespaceBlobTag"),
                                            _grammar()["namespaceUtf8"].encode("utf-8"))).digest()
    level = [_leaf(item) for item in ordered]
    while len(level) > 1:
        level = [
            _node(level[i], level[i + 1]) if i + 1 < len(level) else level[i]
            for i in range(0, len(level), 2)
        ]
    return level[0]


def commitment_preimage(domain: str, items: list[bytes]) -> bytes:
    if not isinstance(domain, str) or not GENERIC_ID_RE.fullmatch(domain):
        raise ValueError("commitment domain must be a canonical identifier")
    if not isinstance(items, list) or any(not isinstance(item, bytes) for item in items):
        raise TypeError("commitment items must be a list of bytes")
    domains = _grammar().get("domains")
    if not isinstance(domains, list) or domain not in domains:
        raise ValueError("commitment domain is not declared by normativePreimageGrammar")
    outer = _grammar()["commitment"]["outer"]
    return (bytes([_hex_tag(outer.get("recordTag"), "commitment.outer.recordTag")])
            + _frame_blob(_hex_tag(outer.get("namespaceTag"), "commitment.outer.namespaceTag"),
                          _grammar()["namespaceUtf8"].encode("utf-8"))
            + _frame_blob(_hex_tag(outer.get("domainTag"), "commitment.outer.domainTag"), domain.encode("ascii"))
            + _frame_blob(_hex_tag(outer.get("merkleRootTag"), "commitment.outer.merkleRootTag"), _merkle(items)))


def commit(domain: str, items: list[bytes]) -> str:
    return "sha256:" + hashlib.sha256(commitment_preimage(domain, items)).hexdigest()


def _member_record_bytes(member: dict[str, Any]) -> bytes:
    return encode_member(member["evaluationId"], member["predicateId"])


def _baseline_bytes(baseline: dict[str, Any]) -> bytes:
    _require_declared_order("BaselineV1", ["kind", "baselineRef", "matchedMembers[]"])
    data = bytes([_record_tag("BaselineV1")]) + frame_component(_field_tag("BaselineV1", "kind"), baseline["kind"])
    if baseline["kind"] == "comparison":
        data += frame_component(_field_tag("BaselineV1", "baselineRef"), baseline["baselineRef"])
        for member in sorted(baseline["matchedMembers"], key=_member_record_bytes):
            data += _frame_blob(_field_tag("BaselineV1", "matchedMembers[]"), _member_record_bytes(member))
    return data


def _policy_bytes(policy: dict[str, Any]) -> bytes:
    _require_declared_order("PolicyV2", [
        "policyRef", "semanticsVersion", "matchDisposition", "baselineDisposition",
        "waivedDisposition", "noMatchDisposition", "incompleteDisposition",
        "evaluationOrder", "evaluationOrder[]", "evaluationOrder[].step",
    ])
    fields = ("policyRef", "semanticsVersion", "matchDisposition", "baselineDisposition",
              "waivedDisposition", "noMatchDisposition", "incompleteDisposition")
    ordered_steps = b"".join(
        _frame_blob(_field_tag("PolicyV2", "evaluationOrder[]"),
                    frame_component(_field_tag("PolicyV2", "evaluationOrder[].step"), step))
        for step in policy["evaluationOrder"]
    )
    return (bytes([_record_tag("PolicyV2")])
            + b"".join(frame_component(_field_tag("PolicyV2", key), policy[key]) for key in fields)
            + _frame_blob(_field_tag("PolicyV2", "evaluationOrder"), ordered_steps))


def derive_verdict(bundle: dict[str, Any]) -> str:
    """Replay policy-ir-2: waiver suppression precedes baseline classification.

    Policy evaluation remains owned by the pure core. The host seals the returned
    outcome; this independent function verifies that the persisted outcome is the
    result of the versioned pure semantics, rather than trusting its label.
    """
    evaluations = bundle["evaluations"]
    vp = bundle["verdictProof"]
    if vp["coverage"]["status"] == "incomplete" or any(
            e["outcome"] in {"indeterminate", "error"} for e in evaluations):
        return "indeterminate"

    matches = {(e["evaluationId"], e["predicateId"])
               for e in evaluations if e["outcome"] == "match"}
    baseline = vp["baseline"]
    baselined = ({(m["evaluationId"], m["predicateId"])
                  for m in baseline["matchedMembers"]}
                 if baseline["kind"] == "comparison" else set())
    waived = {(w["target"]["evaluationId"], w["target"]["predicateId"])
              for w in vp["waivers"]}
    effective_matches = matches - waived
    if effective_matches - baselined:
        return "fail"
    if effective_matches & baselined:
        return "advisory"
    return "pass"


def _verdict_input_bytes(bundle: dict[str, Any]) -> bytes:
    vp = bundle["verdictProof"]
    _require_declared_order("VerdictInputV2", [
        "outcomeSetCommitment", "coverage.status", "coverage.coverageRef", "baseline",
        "waivers", "waivers[]", "waiverSetCommitment", "policy",
    ])
    waiver_bytes = sorted(encode_waiver(w) for w in vp["waivers"])
    return (bytes([_record_tag("VerdictInputV2")])
            + frame_component(_field_tag("VerdictInputV2", "outcomeSetCommitment"), vp["outcomeSetCommitment"])
            + frame_component(_field_tag("VerdictInputV2", "coverage.status"), vp["coverage"]["status"])
            + frame_component(_field_tag("VerdictInputV2", "coverage.coverageRef"), vp["coverage"]["coverageRef"])
            + _frame_blob(_field_tag("VerdictInputV2", "baseline"), _baseline_bytes(vp["baseline"]))
            + _frame_blob(_field_tag("VerdictInputV2", "waivers"),
                          b"".join(_frame_blob(_field_tag("VerdictInputV2", "waivers[]"), w)
                                   for w in waiver_bytes))
            + frame_component(_field_tag("VerdictInputV2", "waiverSetCommitment"), vp["waiverSetCommitment"])
            + _frame_blob(_field_tag("VerdictInputV2", "policy"), _policy_bytes(vp["policy"])))


def derive_verdict_commitment(bundle: dict[str, Any]) -> str:
    """Commit the complete outcome/coverage/baseline/waiver/policy input."""
    return commit("verdict-input", [_verdict_input_bytes(bundle)])


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _exact_object(value: Any, required: set[str], optional: set[str], path: str,
                  out: list[tuple[str, str]], invariant: str = "EP-11") -> dict[str, Any] | None:
    if not isinstance(value, dict):
        out.append((invariant, f"{path}: expected object, got {type(value).__name__}"))
        return None
    keys = set(value)
    for key in sorted(required - keys):
        out.append((invariant, f"{path}: missing required field {key!r}"))
    for key in sorted(keys - required - optional):
        out.append((invariant, f"{path}: unknown field {key!r}"))
    return value


def _list(value: Any, path: str, out: list[tuple[str, str]],
          invariant: str = "EP-11") -> list[Any] | None:
    if not isinstance(value, list):
        out.append((invariant, f"{path}: expected array, got {type(value).__name__}"))
        return None
    return value


def _string(value: Any, path: str, out: list[tuple[str, str]], pattern: re.Pattern[str] | None = None,
            invariant: str = "EP-11", max_bytes: int = 4096) -> bool:
    if not isinstance(value, str):
        out.append((invariant, f"{path}: expected string, got {type(value).__name__}"))
        return False
    if unicodedata.normalize("NFC", value) != value or not value or len(value.encode("utf-8")) > max_bytes:
        out.append((invariant, f"{path}: string is empty, non-NFC, or over {max_bytes} UTF-8 bytes"))
        return False
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value):
        out.append(("EP-8", f"{path}: control characters are forbidden by the identifier/value grammar"))
        return False
    if pattern is not None and not pattern.fullmatch(value):
        out.append(("EP-8", f"{path}: value {value!r} violates its exact wire grammar"))
        return False
    return True


def _ref(value: Any, path: str, out: list[tuple[str, str]]) -> bool:
    if not isinstance(value, str) or not REF_RE.fullmatch(value):
        out.append(("EP-8", f"{path}: expected full sha256:<64 lowercase hex> reference"))
        return False
    return True


def _member(value: Any, path: str, out: list[tuple[str, str]]) -> tuple[str, str] | None:
    obj = _exact_object(value, {"evaluationId", "predicateId"}, set(), path, out)
    if obj is None:
        return None
    ok1 = _string(obj.get("evaluationId"), path + ".evaluationId", out, EVALUATION_RE)
    ok2 = _string(obj.get("predicateId"), path + ".predicateId", out, PREDICATE_RE)
    return (obj["evaluationId"], obj["predicateId"]) if ok1 and ok2 else None


def _validate_ref_record(value: Any, path: str, project_id: Any,
                         out: list[tuple[str, str]]) -> tuple[str, str] | None:
    obj = _exact_object(value, {"ref", "projectId"}, set(), path, out)
    if obj is None:
        return None
    ok = _ref(obj.get("ref"), path + ".ref", out)
    ok = _string(obj.get("projectId"), path + ".projectId", out, PROJECT_RE) and ok
    if ok and obj["projectId"] != project_id:
        out.append(("EP-9", f"{path}: reference crosses ProjectId custody"))
    return (obj["ref"], "replayable") if ok else None


def _proof_refs(evaluation: dict[str, Any]) -> list[str]:
    proof = evaluation["proof"]
    kind = proof["kind"]
    refs: list[str] = []
    if kind == "local-match-proof":
        refs.extend(proof["factRefs"])
    elif kind == "relationship-match-proof":
        refs.append(proof["relationSemanticsRef"])
        refs.extend(proof["factRefs"])
        refs.extend(edge["factRef"] for edge in proof["witnessEdges"])
    elif kind == "aggregate-match-proof":
        refs.append(proof["factPartitionRef"])
        refs.extend(proof["factRefs"])
    elif kind == "no-match-proof":
        refs.append(proof["factPartitionRef"])
    elif kind in {"indeterminate-proof", "error-proof"}:
        refs.append(proof["reasonRef"])
        refs.extend(proof.get("factRefs", []))
    return refs


def derive_authority_requirements(authority_input: Any) -> dict[str, str]:
    if not isinstance(authority_input, dict) or not isinstance(authority_input.get("evaluationAuthoritySeal"), dict):
        raise TypeError("authority input must be a VerifiedEvaluationAuthorityInputV2 object")
    resolved = resolve_semantic_object_bindings(authority_input)
    manifest = resolved["activation-manifest-v1"]["record"]
    plan = authority_input["planIdAdmission"]
    store = authority_input["authoritySealAdmission"]
    # Semantic roots are deliberately absent. The store receipt is the raw graph
    # root whose typed edges derive the EAS and activation-manifest raw records.
    return dict(sorted({
        manifest["resolvedActivationGraphRef"]: "replayable",
        plan["admittedResolvedInputsRef"]: "replayable",
        plan["verificationReceiptRef"]: "verifiable",
        store["verificationReceiptRef"]: "verifiable",
    }.items()))


def derive_seed_requirements(bundle: Any, authority: Any | None = None) -> dict[str, str]:
    """Derive direct roots from evaluation, verdict, and replay fields."""
    if not isinstance(bundle, dict):
        raise TypeError("bundle must be an object")
    requirements: dict[str, str] = {}

    def add(ref: str, capability: str) -> None:
        current = requirements.get(ref)
        if current is None or CAPABILITY_RANK[capability] < CAPABILITY_RANK[current]:
            requirements[ref] = capability

    for evaluation in bundle["evaluations"]:
        add(evaluation["predicateSemanticsRef"], "verifiable")
        add(evaluation["coverageRef"], "verifiable")
        for ref in _proof_refs(evaluation):
            add(ref, "verifiable")
    vp = bundle["verdictProof"]
    add(vp["coverage"]["coverageRef"], "verifiable")
    if vp["baseline"]["kind"] == "comparison":
        add(vp["baseline"]["baselineRef"], "verifiable")
    for waiver in vp["waivers"]:
        add(waiver["waiverRef"], "verifiable")
    add(vp["policy"]["policyRef"], "verifiable")
    for replay in bundle["replayClosureRefs"]:
        add(replay["ref"], "replayable")
    if authority is not None:
        for ref, capability in derive_authority_requirements(authority).items():
            add(ref, capability)
    return dict(sorted(requirements.items()))


def derive_transitive_requirements(seed_requirements: dict[str, str],
                                   dependency_edges: list[dict[str, Any]]) -> dict[str, str]:
    """Propagate exact minima over typed, same-capability dependency edges.

    Edge shape is closed RawDependencyEdgeV2: {fromRef,toRef,projectId,role};
    both endpoints are RawCasRef by the binding reference-type registry.
    Each reviewed role propagates the source minimum. An authored weaker/stronger
    number is never present or trusted. Cycles, duplicate/conflicting edges, and
    unreachable injected edges reject rather than silently becoming authority.
    """
    if not isinstance(seed_requirements, dict):
        raise TypeError("seed_requirements must be an object")
    if not isinstance(dependency_edges, list):
        raise TypeError("dependency_edges must be an array")
    result: dict[str, str] = {}
    for ref, capability in seed_requirements.items():
        if not isinstance(ref, str) or not REF_RE.fullmatch(ref):
            raise ValueError(f"invalid seed reference {ref!r}")
        if capability not in CAPABILITY_RANK:
            raise ValueError(f"invalid seed capability {capability!r}")
        current = result.get(ref)
        if current is None or CAPABILITY_RANK[capability] < CAPABILITY_RANK[current]:
            result[ref] = capability
    parsed: list[tuple[str, str]] = []
    seen_pairs: set[tuple[str, str]] = set()
    for edge in dependency_edges:
        if not isinstance(edge, dict) or set(edge) != {"fromRef", "toRef", "projectId", "role"}:
            raise ValueError("dependency edge must have exact v1 fields")
        if edge["role"] not in DEPENDENCY_ROLES:
            raise ValueError(f"unknown dependency role {edge['role']!r}")
        if not isinstance(edge["fromRef"], str) or not REF_RE.fullmatch(edge["fromRef"]):
            raise ValueError("invalid dependency fromRef")
        if not isinstance(edge["toRef"], str) or not REF_RE.fullmatch(edge["toRef"]):
            raise ValueError("invalid dependency toRef")
        if not isinstance(edge["projectId"], str) or not PROJECT_RE.fullmatch(edge["projectId"]):
            raise ValueError("invalid dependency ProjectId")
        pair = (edge["fromRef"], edge["toRef"])
        if pair in seen_pairs:
            raise ValueError(f"duplicate/conflicting dependency edge {pair!r}")
        seen_pairs.add(pair)
        parsed.append(pair)

    graph: dict[str, list[str]] = {}
    for source, target in parsed:
        graph.setdefault(source, []).append(target)
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting:
            raise ValueError(f"dependency cycle reaches {node}")
        if node in visited:
            return
        visiting.add(node)
        for child in graph.get(node, []):
            visit(child)
        visiting.remove(node)
        visited.add(node)
    for node in sorted(graph):
        visit(node)
    changed = True
    while changed:
        changed = False
        for source, target in parsed:
            if source not in result:
                continue
            capability = result[source]
            current = result.get(target)
            if current is None or CAPABILITY_RANK[capability] < CAPABILITY_RANK[current]:
                result[target] = capability
                changed = True
    unreachable = sorted({source for source, _ in parsed if source not in result})
    if unreachable:
        raise ValueError(f"unreachable injected dependency edges from {unreachable}")
    return dict(sorted(result.items()))


def derive_proof_requirements(bundle: Any,
                              dependency_edges: list[dict[str, Any]] | None = None,
                              authority: Any | None = None) -> dict[str, str]:
    """Derive the complete transitive proof/verdict dependency graph.

    If edges are omitted, they are read from each validated objectStore record's
    dependencies array. External consumers that resolve CAS bytes separately may
    pass the same closed edge records explicitly; ranks and propagation remain
    canonical here rather than being copied by the consumer.
    """
    seeds = derive_seed_requirements(bundle, authority)
    if dependency_edges is None:
        dependency_edges = []
        for record in bundle["objectStore"]:
            for dependency in record["dependencies"]:
                dependency_edges.append({
                    "fromRef": record["ref"],
                    "toRef": dependency["ref"],
                    "projectId": dependency["projectId"],
                    "role": dependency["role"],
                })
    return derive_transitive_requirements(seeds, dependency_edges)


def derive_raw_proof_requirements(bundle: Any, authority: Any,
                                  dependency_edges: list[dict[str, Any]] | None = None
                                  ) -> list[dict[str, str]]:
    """Return the complete physical closure as discriminated RawCasRef identities."""
    requirements = derive_proof_requirements(bundle, dependency_edges, authority)
    if not isinstance(bundle, dict) or not isinstance(bundle.get("objectStore"), list):
        raise TypeError("bundle objectStore must be an array")
    kind_by_ref: dict[str, str] = {}
    for record in bundle["objectStore"]:
        if not isinstance(record, dict) or not isinstance(record.get("ref"), str) or not isinstance(record.get("kind"), str):
            raise ValueError("raw object record identity is malformed")
        current = kind_by_ref.get(record["ref"])
        if current is not None and current != record["kind"]:
            raise ValueError("one RawCasRef is ambiguously assigned multiple record kinds")
        kind_by_ref[record["ref"]] = record["kind"]
    resolved = resolve_semantic_object_bindings(authority)
    manifest = resolved["activation-manifest-v1"]["record"]
    plan = authority["planIdAdmission"]
    external = {
        manifest["resolvedActivationGraphRef"]: "resolved-activation-graph",
        plan["admittedResolvedInputsRef"]: "resolved-inputs",
        plan["verificationReceiptRef"]: "plan-id-verification-receipt",
    }
    for ref, kind in external.items():
        current = kind_by_ref.get(ref)
        if current is not None and current != kind:
            raise ValueError("external raw authority root conflicts with objectStore kind")
        kind_by_ref.setdefault(ref, kind)
    missing = sorted(set(requirements) - set(kind_by_ref))
    if missing:
        raise ValueError(f"raw proof requirements lack recordKind for {missing}")
    project_id = bundle.get("projectId")
    return sorted([{
        "identityKind": "raw-cas",
        "projectId": project_id,
        "recordCasRef": ref,
        "recordKind": kind_by_ref[ref],
        "requiredForCapability": capability,
    } for ref, capability in requirements.items()], key=lambda row: (
        row["recordCasRef"], row["recordKind"], row["projectId"]))


def validate_activation_authority(value: Any, bundle: Any | None = None) -> list[tuple[str, str]]:
    """Validate EP5's typed acyclic pre-evaluation authority-seal envelope.

    This verifies closed shape, identity joins, and all declared bytes/digests.
    It does not prove external plan/store execution, RUN-ID-V1, or terminal Run
    publication; RR13-01 remains pending coordinated Evidence/OP/store work.
    """
    out: list[tuple[str, str]] = []
    try:
        envelope = _exact_object(value, SCHEMA_FIELDS["VerifiedEvaluationAuthorityInputV2"][0], set(), "$verifiedAuthorityInput", out, "EP-12")
        if envelope is None:
            return out
        if envelope.get("schemaVersion") != 2:
            out.append(("EP-12", "$verifiedAuthorityInput.schemaVersion: expected 2"))
        if envelope.get("interfaceId") != "opensip-evidence.verified-evaluation-authority-seal.v2":
            out.append(("EP-12", "$verifiedAuthorityInput.interfaceId: raw, aliased, or unknown authority interface"))
        if envelope.get("suppliedBy") != "opensip-evidence":
            out.append(("EP-12", "$verifiedAuthorityInput.suppliedBy: only opensip-evidence may supply admitted authority"))

        try:
            resolved_records = resolve_semantic_object_bindings(envelope)
        except (KeyError, TypeError, UnicodeError, ValueError) as exc:
            resolved_records = None
            out.append(("EP-12", f"$verifiedAuthorityInput.semanticObjectBindings: raw/semantic resolution failed ({exc})"))
        if resolved_records is not None:
            if envelope.get("activationManifest") != resolved_records["activation-manifest-v1"]["record"]:
                out.append(("EP-12", "$verifiedAuthorityInput.activationManifest: differs from closed decoded raw record bytes"))
            if envelope.get("evaluationAuthoritySeal") != resolved_records["evaluation-authority-seal-v1"]["record"]:
                out.append(("EP-12", "$verifiedAuthorityInput.evaluationAuthoritySeal: differs from closed decoded raw record bytes"))

        plan = _exact_object(envelope.get("planIdAdmission"), SCHEMA_FIELDS["PlanIdAdmissionV1"][0], set(), "$verifiedAuthorityInput.planIdAdmission", out, "EP-12")
        if plan is not None:
            if plan.get("verificationOwner") != "opensip-plan" or plan.get("planIdRecipe") != "PLAN-ID-V1":
                out.append(("EP-12", "$verifiedAuthorityInput.planIdAdmission: wrong owner or PlanId recipe"))
            _ref(plan.get("admittedResolvedInputsRef"), "$verifiedAuthorityInput.planIdAdmission.admittedResolvedInputsRef", out)
            _string(plan.get("verifiedPlanId"), "$verifiedAuthorityInput.planIdAdmission.verifiedPlanId", out, PLAN_RE, "EP-12")
            _ref(plan.get("verificationReceiptRef"), "$verifiedAuthorityInput.planIdAdmission.verificationReceiptRef", out)

        admission = _exact_object(envelope.get("authoritySealAdmission"), SCHEMA_FIELDS["AuthoritySealAdmissionV1"][0], set(), "$verifiedAuthorityInput.authoritySealAdmission", out, "EP-12")
        if admission is not None:
            if admission.get("verificationOwner") != "opensip-store":
                out.append(("EP-12", "$verifiedAuthorityInput.authoritySealAdmission: wrong verification owner"))
            _string(admission.get("projectId"), "$verifiedAuthorityInput.authoritySealAdmission.projectId", out, PROJECT_RE, "EP-12")
            for key in ("resolvedEvaluationAuthoritySealRef", "sealedActivationManifestRef", "verificationReceiptRef"):
                _ref(admission.get(key), f"$verifiedAuthorityInput.authoritySealAdmission.{key}", out)

        seal = _exact_object(envelope.get("evaluationAuthoritySeal"), SCHEMA_FIELDS["EvaluationAuthoritySealV1"][0], set(), "$verifiedAuthorityInput.evaluationAuthoritySeal", out, "EP-12")
        if seal is None:
            return out
        if seal.get("schemaVersion") != 1:
            out.append(("EP-12", "$verifiedAuthorityInput.evaluationAuthoritySeal.schemaVersion: expected 1"))
        _string(seal.get("projectId"), "$verifiedAuthorityInput.evaluationAuthoritySeal.projectId", out, PROJECT_RE, "EP-12")
        _string(seal.get("planId"), "$verifiedAuthorityInput.evaluationAuthoritySeal.planId", out, PLAN_RE, "EP-12")
        for key in ("planIntentCommitment", "executionPlanCommitment", "activationManifestRef"):
            _ref(seal.get(key), f"$verifiedAuthorityInput.evaluationAuthoritySeal.{key}", out)
        if plan is not None and plan.get("verifiedPlanId") != seal.get("planId"):
            out.append(("EP-12", "$verifiedAuthorityInput.planIdAdmission.verifiedPlanId: differs from authority seal"))

        manifest = _exact_object(envelope.get("activationManifest"), SCHEMA_FIELDS["ActivationManifestV1"][0], set(), "$verifiedAuthorityInput.activationManifest", out, "EP-12")
        parsed_members: list[dict[str, Any]] = []
        if manifest is not None:
            if manifest.get("schemaVersion") != 1:
                out.append(("EP-12", "$verifiedAuthorityInput.activationManifest.schemaVersion: expected 1"))
            _string(manifest.get("projectId"), "$verifiedAuthorityInput.activationManifest.projectId", out, PROJECT_RE, "EP-12")
            _string(manifest.get("planId"), "$verifiedAuthorityInput.activationManifest.planId", out, PLAN_RE, "EP-12")
            for key in ("planIntentCommitment", "executionPlanCommitment", "resolvedActivationGraphRef"):
                _ref(manifest.get(key), f"$verifiedAuthorityInput.activationManifest.{key}", out)
            for key in ("projectId", "planId", "planIntentCommitment", "executionPlanCommitment"):
                if manifest.get(key) != seal.get(key):
                    out.append(("EP-12", f"$verifiedAuthorityInput.activationManifest.{key}: differs from authority seal"))
            members = _list(manifest.get("members"), "$verifiedAuthorityInput.activationManifest.members", out, "EP-12")
            if members is not None:
                if not members:
                    out.append(("EP-12", "$verifiedAuthorityInput.activationManifest.members: activation universe cannot be empty"))
                pairs: set[tuple[str, str]] = set()
                for i, raw in enumerate(members):
                    path = f"$verifiedAuthorityInput.activationManifest.members[{i}]"
                    member = _exact_object(raw, SCHEMA_FIELDS["ActivationMemberV1"][0], set(), path, out, "EP-12")
                    if member is None:
                        continue
                    eid_ok = _string(member.get("evaluationId"), path + ".evaluationId", out, EVALUATION_RE, "EP-12")
                    pid_ok = _string(member.get("predicateId"), path + ".predicateId", out, PREDICATE_RE, "EP-12")
                    if member.get("claimShape") not in SHAPES:
                        out.append(("EP-12", f"{path}.claimShape: outside exact closed claim-shape enum"))
                    _ref(member.get("coverageRef"), path + ".coverageRef", out)
                    for key in ("ruleActivationId", "predicateActivationId", "policyActivationId"):
                        _string(member.get(key), path + "." + key, out, ACTIVATION_RE, "EP-12")
                    if eid_ok and pid_ok:
                        pair = (member["evaluationId"], member["predicateId"])
                        if pair in pairs:
                            out.append(("EP-12", f"{path}: duplicate activation member"))
                        pairs.add(pair)
                    parsed_members.append(member)
                try:
                    if parsed_members != sorted(parsed_members, key=encode_activation_member):
                        out.append(("EP-12", "$verifiedAuthorityInput.activationManifest.members: must be strict canonical byte order"))
                except (KeyError, TypeError, ValueError) as exc:
                    out.append(("EP-12", f"$verifiedAuthorityInput.activationManifest.members: cannot encode ({exc})"))
            try:
                if seal.get("activationManifestRef") != derive_activation_manifest_ref(manifest):
                    out.append(("EP-12", "$verifiedAuthorityInput.evaluationAuthoritySeal.activationManifestRef: manifest digest does not recompute"))
            except (KeyError, TypeError, ValueError) as exc:
                out.append(("EP-12", f"$verifiedAuthorityInput.activationManifest: cannot recompute ({exc})"))

        try:
            seal_ref = derive_evaluation_authority_seal_ref(seal)
            if admission is not None:
                if admission.get("resolvedEvaluationAuthoritySealRef") != seal_ref:
                    out.append(("EP-12", "$verifiedAuthorityInput.authoritySealAdmission.resolvedEvaluationAuthoritySealRef: seal bytes/digest do not recompute"))
                if admission.get("projectId") != seal.get("projectId") or admission.get("sealedActivationManifestRef") != seal.get("activationManifestRef"):
                    out.append(("EP-12", "$verifiedAuthorityInput.authoritySealAdmission: ProjectId/manifest join differs from seal"))
        except (KeyError, TypeError, ValueError) as exc:
            seal_ref = None
            out.append(("EP-12", f"$verifiedAuthorityInput.evaluationAuthoritySeal: cannot recompute ({exc})"))

        if isinstance(bundle, dict):
            if seal.get("projectId") != bundle.get("projectId"):
                out.append(("EP-12", "$verifiedAuthorityInput: ProjectId differs from semantic bundle"))
            if seal_ref is not None and bundle.get("evaluationAuthoritySealRef") != seal_ref:
                out.append(("EP-12", "$bundle.evaluationAuthoritySealRef: differs from admitted authority seal bytes"))
            evaluations = bundle.get("evaluations")
            if isinstance(evaluations, list):
                actual = [{key: evaluation.get(key) for key in ("evaluationId", "predicateId", "claimShape", "coverageRef")}
                          for evaluation in evaluations if isinstance(evaluation, dict)]
                expected = [{key: member.get(key) for key in ("evaluationId", "predicateId", "claimShape", "coverageRef")}
                            for member in parsed_members]
                try:
                    actual = sorted(actual, key=lambda row: encode_member(row["evaluationId"], row["predicateId"]))
                    expected = sorted(expected, key=lambda row: encode_member(row["evaluationId"], row["predicateId"]))
                except (KeyError, TypeError, ValueError):
                    pass
                if actual != expected:
                    out.append(("EP-12", "$bundle.evaluations: does not equal the fixed pre-evaluation activation universe"))
            ru = bundle.get("requiredUniverse")
            if isinstance(ru, dict) and manifest is not None:
                try:
                    member_ids = derive_authority_members(envelope)
                    if ru.get("memberIds") != member_ids or ru.get("declaredCount") != len(member_ids):
                        out.append(("EP-12", "$bundle.requiredUniverse: differs from admitted activation manifest"))
                    want = commit("universe", [encode_member(row["evaluationId"], row["predicateId"]) for row in member_ids])
                    if ru.get("universeCommitment") != want:
                        out.append(("EP-12", "$bundle.requiredUniverse.universeCommitment: differs from manifest derivation"))
                except (KeyError, TypeError, ValueError) as exc:
                    out.append(("EP-12", f"$bundle.requiredUniverse: authority derivation failed ({exc})"))
        return out
    except Exception as exc:
        return out + [("EP-TOTALITY", f"$verifiedAuthorityInput: controlled validation failure {type(exc).__name__}: {exc}")]


def _validate_proof(evaluation: dict[str, Any], path: str,
                    out: list[tuple[str, str]]) -> None:
    shape = evaluation.get("claimShape")
    proof = evaluation.get("proof")
    if shape == "local-match":
        obj = _exact_object(proof, {"kind", "subjectId", "factRefs"}, {"spanAnchor"}, path, out)
        if obj is None:
            return
        if obj.get("kind") != "local-match-proof":
            out.append(("EP-2", f"{path}.kind: wrong proof union tag"))
        _string(obj.get("subjectId"), path + ".subjectId", out)
        refs = _list(obj.get("factRefs"), path + ".factRefs", out, "EP-1")
        if refs is not None:
            if not refs:
                out.append(("EP-1", f"{path}.factRefs: local match requires at least one fact"))
            for i, ref in enumerate(refs):
                _ref(ref, f"{path}.factRefs[{i}]", out)
        if "spanAnchor" in obj:
            span = _exact_object(obj["spanAnchor"], {"line", "column"}, set(), path + ".spanAnchor", out)
            if span is not None:
                for key in ("line", "column"):
                    if not _is_int(span.get(key)) or span[key] < 1:
                        out.append(("EP-11", f"{path}.spanAnchor.{key}: expected positive integer"))
    elif shape == "relationship-match":
        obj = _exact_object(proof, {"kind", "relationSemanticsRef", "witnessEdges", "factRefs"}, set(), path, out)
        if obj is None:
            return
        if obj.get("kind") != "relationship-match-proof":
            out.append(("EP-2", f"{path}.kind: wrong proof union tag"))
        _ref(obj.get("relationSemanticsRef"), path + ".relationSemanticsRef", out)
        refs = _list(obj.get("factRefs"), path + ".factRefs", out, "EP-2")
        if refs is not None:
            if not refs:
                out.append(("EP-2", f"{path}.factRefs: relationship match requires facts"))
            for i, ref in enumerate(refs):
                _ref(ref, f"{path}.factRefs[{i}]", out)
        edges = _list(obj.get("witnessEdges"), path + ".witnessEdges", out, "EP-2")
        if edges is not None:
            if not edges:
                out.append(("EP-2", f"{path}.witnessEdges: relationship match requires an edge"))
            for i, edge in enumerate(edges):
                edge_obj = _exact_object(edge, {"fromSubjectId", "toSubjectId", "relationKind", "factRef"}, set(), f"{path}.witnessEdges[{i}]", out)
                if edge_obj is None:
                    continue
                for key in ("fromSubjectId", "toSubjectId", "relationKind"):
                    _string(edge_obj.get(key), f"{path}.witnessEdges[{i}].{key}", out)
                _ref(edge_obj.get("factRef"), f"{path}.witnessEdges[{i}].factRef", out)
    elif shape == "aggregate-match":
        obj = _exact_object(proof, {"kind", "memberSetCommitment", "memberCount", "factPartitionRef", "foldSpec", "factRefs"}, set(), path, out)
        if obj is None:
            return
        if obj.get("kind") != "aggregate-match-proof":
            out.append(("EP-2", f"{path}.kind: wrong proof union tag"))
        _ref(obj.get("memberSetCommitment"), path + ".memberSetCommitment", out)
        _ref(obj.get("factPartitionRef"), path + ".factPartitionRef", out)
        if obj.get("foldSpec") != "typed-merkle-set-v2":
            out.append(("EP-4", f"{path}.foldSpec: expected typed-merkle-set-v2"))
        if not _is_int(obj.get("memberCount")) or obj["memberCount"] < 0:
            out.append(("EP-4", f"{path}.memberCount: expected non-negative integer"))
        refs = _list(obj.get("factRefs"), path + ".factRefs", out, "EP-2")
        if refs is not None:
            if not refs:
                out.append(("EP-2", f"{path}.factRefs: aggregate match requires facts"))
            for i, ref in enumerate(refs):
                _ref(ref, f"{path}.factRefs[{i}]", out)
    elif shape == "no-match":
        obj = _exact_object(proof, {"kind", "subjectSetCommitment", "subjectCount", "factPartitionRef"}, set(), path, out)
        if obj is None:
            return
        if obj.get("kind") != "no-match-proof":
            out.append(("EP-2", f"{path}.kind: wrong proof union tag"))
        _ref(obj.get("subjectSetCommitment"), path + ".subjectSetCommitment", out)
        _ref(obj.get("factPartitionRef"), path + ".factPartitionRef", out)
        if not _is_int(obj.get("subjectCount")) or obj["subjectCount"] < 0:
            out.append(("EP-4", f"{path}.subjectCount: expected non-negative integer"))
    elif shape in {"indeterminate", "error"}:
        expected_kind = shape + "-proof"
        obj = _exact_object(proof, {"kind", "reasonRef"}, {"partialSubjectCount", "factRefs"}, path, out)
        if obj is None:
            return
        if obj.get("kind") != expected_kind:
            out.append(("EP-2", f"{path}.kind: wrong proof union tag"))
        _ref(obj.get("reasonRef"), path + ".reasonRef", out)
        if "partialSubjectCount" in obj and (not _is_int(obj["partialSubjectCount"]) or obj["partialSubjectCount"] < 0):
            out.append(("EP-11", f"{path}.partialSubjectCount: expected non-negative integer"))
        if "factRefs" in obj:
            refs = _list(obj["factRefs"], path + ".factRefs", out)
            if refs is not None:
                for i, ref in enumerate(refs):
                    _ref(ref, f"{path}.factRefs[{i}]", out)
    else:
        _exact_object(proof, set(), set(), path, out, "EP-2")
        out.append(("EP-2", f"{path}: no proof variant exists for claimShape {shape!r}"))


def validate_bundle(value: Any, authority: Any) -> list[tuple[str, str]]:
    """Total validation of one bundle against separately supplied fixed authority."""
    out: list[tuple[str, str]] = []
    try:
        bundle = _exact_object(value, BUNDLE_REQUIRED, set(), "$bundle", out)
        if bundle is None:
            return out
        if bundle.get("schemaVersion") != 5:
            out.append(("EP-11", "$bundle.schemaVersion: expected integer constant 5"))
        project_ok = _string(bundle.get("projectId"), "$bundle.projectId", out, PROJECT_RE)
        _ref(bundle.get("evaluationAuthoritySealRef"), "$bundle.evaluationAuthoritySealRef", out)
        project_id = bundle.get("projectId")

        store_records = _list(bundle.get("objectStore"), "$bundle.objectStore", out)
        store: dict[str, dict[str, Any]] = {}
        dependency_edges: list[dict[str, Any]] = []
        if store_records is not None:
            for i, record in enumerate(store_records):
                path = f"$bundle.objectStore[{i}]"
                obj = _exact_object(record, {"ref", "projectId", "kind", "dependencies"}, set(), path, out)
                if obj is None:
                    continue
                ref_ok = _ref(obj.get("ref"), path + ".ref", out)
                pid_ok = _string(obj.get("projectId"), path + ".projectId", out, PROJECT_RE)
                kind_ok = isinstance(obj.get("kind"), str) and obj["kind"] in {
                    "predicate-semantics", "coverage", "fact", "fact-partition",
                    "relation-semantics", "reason", "baseline", "waiver", "policy",
                    "replay-closure", "historical-semantics", "historical-manifest",
                    "historical-executable", "historical-signature",
                    "historical-trust-root", "historical-public-key",
                    "authority-seal-verification-receipt",
                    "evaluation-authority-seal-record", "activation-manifest-record",
                }
                if not kind_ok:
                    out.append(("EP-11", f"{path}.kind: unknown object kind {obj.get('kind')!r}"))
                if pid_ok and project_ok and obj["projectId"] != project_id:
                    out.append(("EP-9", f"{path}: object belongs to another ProjectId"))
                if ref_ok:
                    if obj["ref"] in store:
                        out.append(("EP-11", f"{path}.ref: duplicate object reference"))
                    else:
                        store[obj["ref"]] = obj
                dependencies = _list(obj.get("dependencies"), path + ".dependencies", out)
                if dependencies is not None:
                    seen_dependencies: set[str] = set()
                    for j, dependency in enumerate(dependencies):
                        dpath = f"{path}.dependencies[{j}]"
                        dep = _exact_object(dependency, {"ref", "projectId", "role"}, set(), dpath, out)
                        if dep is None:
                            continue
                        dep_ref_ok = _ref(dep.get("ref"), dpath + ".ref", out)
                        dep_pid_ok = _string(dep.get("projectId"), dpath + ".projectId", out, PROJECT_RE)
                        if dep_pid_ok and project_ok and dep["projectId"] != project_id:
                            out.append(("EP-9", f"{dpath}: dependency crosses ProjectId custody"))
                        if dep.get("role") not in DEPENDENCY_ROLES:
                            out.append(("EP-11", f"{dpath}.role: unknown dependency role {dep.get('role')!r}"))
                        if dep_ref_ok and ref_ok:
                            if dep["ref"] in seen_dependencies:
                                out.append(("EP-11", f"{dpath}.ref: duplicate dependency edge"))
                            seen_dependencies.add(dep["ref"])
                            dependency_edges.append({
                                "fromRef": obj["ref"], "toRef": dep["ref"],
                                "projectId": dep.get("projectId"),
                                "role": dep.get("role"),
                            })

        for i, edge in enumerate(dependency_edges):
            if edge["toRef"] not in store:
                out.append(("EP-9", f"$bundle.objectStore dependency[{i}]: target {edge['toRef']!r} is absent"))
            if edge["fromRef"] == edge["toRef"]:
                out.append(("EP-9", f"$bundle.objectStore dependency[{i}]: self-cycle is forbidden"))

        partitions_raw = _list(bundle.get("partitionContents"), "$bundle.partitionContents", out)
        partitions: dict[str, list[str]] = {}
        if partitions_raw is not None:
            for i, record in enumerate(partitions_raw):
                path = f"$bundle.partitionContents[{i}]"
                obj = _exact_object(record, {"partitionRef", "projectId", "members"}, set(), path, out)
                if obj is None:
                    continue
                ref_ok = _ref(obj.get("partitionRef"), path + ".partitionRef", out)
                pid_ok = _string(obj.get("projectId"), path + ".projectId", out, PROJECT_RE)
                if pid_ok and project_ok and obj["projectId"] != project_id:
                    out.append(("EP-9", f"{path}: partition crosses ProjectId custody"))
                members = _list(obj.get("members"), path + ".members", out)
                clean_members: list[str] = []
                if members is not None:
                    for j, member in enumerate(members):
                        if _string(member, f"{path}.members[{j}]", out):
                            clean_members.append(member)
                    if len(clean_members) != len(set(clean_members)):
                        out.append(("EP-4", f"{path}.members: duplicate logical members are forbidden"))
                if ref_ok:
                    if obj["partitionRef"] in partitions:
                        out.append(("EP-11", f"{path}.partitionRef: duplicate partition record"))
                    else:
                        partitions[obj["partitionRef"]] = clean_members
                    stored = store.get(obj["partitionRef"])
                    if stored is None or stored.get("kind") != "fact-partition":
                        out.append(("EP-9", f"{path}.partitionRef: no retained fact-partition object"))

        evals_raw = _list(bundle.get("evaluations"), "$bundle.evaluations", out)
        evaluations: list[dict[str, Any]] = []
        member_tuples: list[tuple[str, str]] = []
        referenced: set[str] = set()
        if evals_raw is not None:
            if not evals_raw:
                out.append(("EP-10", "$bundle.evaluations: required universe must be non-empty"))
            for i, evaluation in enumerate(evals_raw):
                path = f"$bundle.evaluations[{i}]"
                obj = _exact_object(evaluation, EVALUATION_REQUIRED, set(), path, out)
                if obj is None:
                    continue
                eid_ok = _string(obj.get("evaluationId"), path + ".evaluationId", out, EVALUATION_RE)
                pid_ok = _string(obj.get("predicateId"), path + ".predicateId", out, PREDICATE_RE)
                outcome = obj.get("outcome")
                shape = obj.get("claimShape")
                if isinstance(outcome, str):
                    _string(outcome, path + ".outcome", out, max_bytes=32)
                if not isinstance(outcome, str) or outcome not in OUTCOMES:
                    out.append(("EP-11", f"{path}.outcome: unknown closed enum value {outcome!r}"))
                if not isinstance(shape, str) or shape not in SHAPES:
                    out.append(("EP-11", f"{path}.claimShape: unknown closed enum value {shape!r}"))
                elif outcome in OUTCOMES and PAIRING[shape] != outcome:
                    out.append(("EP-2", f"{path}: claimShape {shape!r} cannot carry outcome {outcome!r}"))
                if _ref(obj.get("predicateSemanticsRef"), path + ".predicateSemanticsRef", out):
                    referenced.add(obj["predicateSemanticsRef"])
                    retained_predicate = store.get(obj["predicateSemanticsRef"])
                    if retained_predicate is None or retained_predicate.get("kind") != "predicate-semantics":
                        out.append(("EP-3", f"{path}.predicateSemanticsRef: historical predicate semantics is not retained with the correct type"))
                if _ref(obj.get("coverageRef"), path + ".coverageRef", out):
                    referenced.add(obj["coverageRef"])
                _validate_proof(obj, path + ".proof", out)
                proof_obj = obj.get("proof")
                if isinstance(proof_obj, dict) and shape in {"aggregate-match", "no-match"}:
                    partition_ref = proof_obj.get("factPartitionRef")
                    if isinstance(partition_ref, str) and partition_ref in partitions:
                        contents = partitions[partition_ref]
                        expected_set = commit("subject-set", [encode_subject(member) for member in contents])
                        commitment_key = "memberSetCommitment" if shape == "aggregate-match" else "subjectSetCommitment"
                        count_key = "memberCount" if shape == "aggregate-match" else "subjectCount"
                        if proof_obj.get(commitment_key) != expected_set:
                            out.append(("EP-4", f"{path}.proof.{commitment_key}: does not recompute from retained partition"))
                        if proof_obj.get(count_key) != len(set(contents)):
                            out.append(("EP-4", f"{path}.proof.{count_key}: disagrees with retained partition set"))
                if eid_ok and pid_ok:
                    member_tuples.append((obj["evaluationId"], obj["predicateId"]))
                evaluations.append(obj)
            if len(member_tuples) != len(set(member_tuples)):
                out.append(("EP-10", "$bundle.evaluations: duplicate logical evaluation member"))

        for evaluation in evaluations:
            try:
                referenced.update(_proof_refs(evaluation))
            except (KeyError, TypeError):
                pass

        ru = _exact_object(bundle.get("requiredUniverse"), {"declaredCount", "memberIds", "universeCommitment"}, set(), "$bundle.requiredUniverse", out, "EP-10")
        if ru is not None:
            if not _is_int(ru.get("declaredCount")) or ru["declaredCount"] < 1:
                out.append(("EP-10", "$bundle.requiredUniverse.declaredCount: expected positive integer"))
            ids_raw = _list(ru.get("memberIds"), "$bundle.requiredUniverse.memberIds", out, "EP-10")
            declared_members: list[tuple[str, str]] = []
            if ids_raw is not None:
                for i, member in enumerate(ids_raw):
                    parsed = _member(member, f"$bundle.requiredUniverse.memberIds[{i}]", out)
                    if parsed is not None:
                        declared_members.append(parsed)
                expected_order = sorted(member_tuples, key=lambda m: encode_member(*m))
                if declared_members != expected_order:
                    out.append(("EP-10", "$bundle.requiredUniverse.memberIds: must exactly equal the sorted activated member set"))
            if ru.get("declaredCount") != len(member_tuples):
                out.append(("EP-10", "$bundle.requiredUniverse.declaredCount: disagrees with activated members"))
            if all(isinstance(x, str) for tup in member_tuples for x in tup):
                want_u = commit("universe", [encode_member(*member) for member in member_tuples])
                if ru.get("universeCommitment") != want_u:
                    out.append(("EP-10", "$bundle.requiredUniverse.universeCommitment: does not recompute"))

        replay_raw = _list(bundle.get("replayClosureRefs"), "$bundle.replayClosureRefs", out)
        if replay_raw is not None:
            seen_replay: set[str] = set()
            for i, record in enumerate(replay_raw):
                parsed = _validate_ref_record(record, f"$bundle.replayClosureRefs[{i}]", project_id, out)
                if parsed is not None:
                    ref, _ = parsed
                    if ref in seen_replay:
                        out.append(("EP-11", f"$bundle.replayClosureRefs[{i}]: duplicate replay reference"))
                    seen_replay.add(ref)
                    referenced.add(ref)

        vp = _exact_object(bundle.get("verdictProof"), {
            "verdict", "outcomeSetCommitment", "coverage", "baseline", "waivers",
            "waiverSetCommitment", "policy", "derivationCommitment",
        }, set(), "$bundle.verdictProof", out, "EP-6")
        if vp is not None:
            verdict = vp.get("verdict")
            if not isinstance(verdict, str) or verdict not in VERDICTS:
                out.append(("EP-11", f"$bundle.verdictProof.verdict: unknown closed enum value {verdict!r}"))
            if all(isinstance(e.get("evaluationId"), str) and isinstance(e.get("predicateId"), str)
                   and isinstance(e.get("outcome"), str) for e in evaluations):
                want_o = commit("outcome-set", [encode_outcome(e["evaluationId"], e["predicateId"], e["outcome"]) for e in evaluations])
                if vp.get("outcomeSetCommitment") != want_o:
                    out.append(("EP-5", "$bundle.verdictProof.outcomeSetCommitment: does not cover every activated outcome"))

            coverage = _exact_object(vp.get("coverage"), {"status", "coverageRef", "projectId"}, set(), "$bundle.verdictProof.coverage", out, "EP-6")
            if coverage is not None:
                if coverage.get("status") not in {"complete", "incomplete"}:
                    out.append(("EP-11", "$bundle.verdictProof.coverage.status: unknown closed enum"))
                if _ref(coverage.get("coverageRef"), "$bundle.verdictProof.coverage.coverageRef", out):
                    referenced.add(coverage["coverageRef"])
                if not _string(coverage.get("projectId"), "$bundle.verdictProof.coverage.projectId", out, PROJECT_RE) or coverage.get("projectId") != project_id:
                    out.append(("EP-9", "$bundle.verdictProof.coverage: ProjectId mismatch"))

            baseline = vp.get("baseline")
            if not isinstance(baseline, dict):
                out.append(("EP-6", f"$bundle.verdictProof.baseline: expected tagged object, got {type(baseline).__name__}"))
            else:
                kind = baseline.get("kind")
                if kind == "none":
                    _exact_object(baseline, {"kind"}, set(), "$bundle.verdictProof.baseline", out, "EP-6")
                elif kind == "comparison":
                    base_obj = _exact_object(baseline, {"kind", "baselineRef", "projectId", "matchedMembers"}, set(), "$bundle.verdictProof.baseline", out, "EP-6")
                    if base_obj is not None:
                        if _ref(base_obj.get("baselineRef"), "$bundle.verdictProof.baseline.baselineRef", out):
                            referenced.add(base_obj["baselineRef"])
                        if not _string(base_obj.get("projectId"), "$bundle.verdictProof.baseline.projectId", out, PROJECT_RE) or base_obj.get("projectId") != project_id:
                            out.append(("EP-9", "$bundle.verdictProof.baseline: ProjectId mismatch"))
                        matched_raw = _list(base_obj.get("matchedMembers"), "$bundle.verdictProof.baseline.matchedMembers", out, "EP-6")
                        matched: list[tuple[str, str]] = []
                        if matched_raw is not None:
                            for i, member in enumerate(matched_raw):
                                parsed = _member(member, f"$bundle.verdictProof.baseline.matchedMembers[{i}]", out)
                                if parsed is not None:
                                    matched.append(parsed)
                            if len(matched) != len(set(matched)):
                                out.append(("EP-6", "$bundle.verdictProof.baseline.matchedMembers: duplicates forbidden"))
                            actual_matches = {(e.get("evaluationId"), e.get("predicateId")) for e in evaluations if e.get("outcome") == "match"}
                            if not set(matched) <= actual_matches:
                                out.append(("EP-7", "$bundle.verdictProof.baseline: names a member that is not a current match"))
                else:
                    out.append(("EP-11", f"$bundle.verdictProof.baseline.kind: unknown tag {kind!r}"))

            waivers_raw = _list(vp.get("waivers"), "$bundle.verdictProof.waivers", out, "EP-6")
            waivers: list[dict[str, Any]] = []
            if waivers_raw is not None:
                seen_ids: set[str] = set()
                seen_targets: set[tuple[str, str]] = set()
                actual_matches = {(e.get("evaluationId"), e.get("predicateId")) for e in evaluations if e.get("outcome") == "match"}
                for i, waiver in enumerate(waivers_raw):
                    path = f"$bundle.verdictProof.waivers[{i}]"
                    obj = _exact_object(waiver, {"waiverId", "waiverRef", "projectId", "target", "disposition"}, set(), path, out, "EP-6")
                    if obj is None:
                        continue
                    _string(obj.get("waiverId"), path + ".waiverId", out, WAIVER_RE)
                    if _ref(obj.get("waiverRef"), path + ".waiverRef", out):
                        referenced.add(obj["waiverRef"])
                    if not _string(obj.get("projectId"), path + ".projectId", out, PROJECT_RE) or obj.get("projectId") != project_id:
                        out.append(("EP-9", f"{path}: ProjectId mismatch"))
                    target = _member(obj.get("target"), path + ".target", out)
                    if obj.get("disposition") != "suppress-match":
                        out.append(("EP-7", f"{path}.disposition: policy-ir-2 supports only suppress-match"))
                    if obj.get("waiverId") in seen_ids:
                        out.append(("EP-6", f"{path}.waiverId: duplicate"))
                    elif isinstance(obj.get("waiverId"), str):
                        seen_ids.add(obj["waiverId"])
                    if target is not None:
                        if target in seen_targets:
                            out.append(("EP-6", f"{path}.target: multiple waivers for one member"))
                        seen_targets.add(target)
                        if target not in actual_matches:
                            out.append(("EP-7", f"{path}.target: waiver target is not a current match"))
                    waivers.append(obj)
                if len(waivers) == len(waivers_raw):
                    want_w = commit("waiver-set", [encode_waiver(w) for w in waivers])
                    if vp.get("waiverSetCommitment") != want_w:
                        out.append(("EP-6", "$bundle.verdictProof.waiverSetCommitment: does not recompute"))

            policy = _exact_object(vp.get("policy"), {
                "policyRef", "projectId", "semanticsVersion", "matchDisposition",
                "baselineDisposition", "waivedDisposition", "noMatchDisposition",
                "incompleteDisposition", "evaluationOrder",
            }, set(), "$bundle.verdictProof.policy", out, "EP-6")
            expected_policy = {
                "semanticsVersion": "policy-ir-2",
                "evaluationOrder": POLICY_EVALUATION_ORDER,
                "matchDisposition": "effective-new-match-fail",
                "baselineDisposition": "effective-baseline-match-advisory",
                "waivedDisposition": "suppress-before-baseline",
                "noMatchDisposition": "pass",
                "incompleteDisposition": "indeterminate",
            }
            if policy is not None:
                if _ref(policy.get("policyRef"), "$bundle.verdictProof.policy.policyRef", out):
                    referenced.add(policy["policyRef"])
                if not _string(policy.get("projectId"), "$bundle.verdictProof.policy.projectId", out, PROJECT_RE) or policy.get("projectId") != project_id:
                    out.append(("EP-9", "$bundle.verdictProof.policy: ProjectId mismatch"))
                for key, expected in expected_policy.items():
                    if policy.get(key) != expected:
                        invariant = "EP-13" if key == "evaluationOrder" else "EP-7"
                        out.append((invariant, f"$bundle.verdictProof.policy.{key}: expected {expected!r}"))

            structurally_ready = (isinstance(coverage, dict) and isinstance(baseline, dict)
                                  and isinstance(waivers_raw, list) and isinstance(policy, dict)
                                  and all(k in vp for k in {"outcomeSetCommitment", "waiverSetCommitment"}))
            if structurally_ready:
                try:
                    derived = derive_verdict(bundle)
                    if verdict != derived:
                        out.append(("EP-7", f"$bundle.verdictProof.verdict: asserted {verdict!r}, policy-ir-2 derives {derived!r}"))
                    want_d = derive_verdict_commitment(bundle)
                    if vp.get("derivationCommitment") != want_d:
                        out.append(("EP-7", "$bundle.verdictProof.derivationCommitment: policy inputs do not recompute"))
                except (KeyError, TypeError, ValueError) as exc:
                    out.append(("EP-7", f"$bundle.verdictProof: cannot derive policy outcome ({exc})"))

        for ref in sorted(referenced):
            if ref not in store:
                out.append(("EP-9", f"$bundle.objectStore: referenced object {ref!r} is absent"))

        try:
            complete_requirements = derive_proof_requirements(bundle, dependency_edges, authority)
        except (KeyError, TypeError, ValueError) as exc:
            out.append(("EP-9", f"$bundle.objectStore: dependency graph is invalid ({exc})"))
            complete_requirements = {ref: "verifiable" for ref in referenced}
        external_raw_roots: set[str] = set()
        try:
            resolved_authority = resolve_semantic_object_bindings(authority)
            authority_manifest = resolved_authority["activation-manifest-v1"]["record"]
            authority_plan = authority["planIdAdmission"]
            external_raw_roots = {
                authority_manifest["resolvedActivationGraphRef"],
                authority_plan["admittedResolvedInputsRef"],
                authority_plan["verificationReceiptRef"],
            }
        except (KeyError, TypeError, UnicodeError, ValueError):
            resolved_authority = None
        for ref in sorted(complete_requirements):
            if ref not in store and ref not in external_raw_roots:
                out.append(("EP-9", f"$bundle.objectStore: transitive dependency {ref!r} is absent"))

        used_store_refs = set(complete_requirements) | set(partitions)
        for ref in sorted(set(store) - used_store_refs):
            out.append(("EP-9", f"$bundle.objectStore: unreferenced object {ref!r} hides outside the proof graph"))

        if resolved_authority is not None:
            manifest_binding = resolved_authority["activation-manifest-v1"]["binding"]
            seal_binding = resolved_authority["evaluation-authority-seal-v1"]["binding"]
            semantic_refs = {manifest_binding["semanticRef"], seal_binding["semanticRef"]}
            if semantic_refs & set(store):
                out.append(("EP-9", "$bundle.objectStore: semantic commitment appears as a raw CAS object identity"))
            store_admission = authority.get("authoritySealAdmission", {}) if isinstance(authority, dict) else {}
            receipt_ref = store_admission.get("verificationReceiptRef")
            expected_chain = {
                receipt_ref: ("authority-seal-verification-receipt", [{
                    "ref": seal_binding["recordCasRef"], "projectId": project_id,
                    "role": "evaluation-authority-seal-record",
                }]),
                seal_binding["recordCasRef"]: ("evaluation-authority-seal-record", [{
                    "ref": manifest_binding["recordCasRef"], "projectId": project_id,
                    "role": "activation-manifest-record",
                }]),
                manifest_binding["recordCasRef"]: ("activation-manifest-record", []),
            }
            for ref, (kind, dependencies) in expected_chain.items():
                record = store.get(ref)
                if (not isinstance(record, dict) or record.get("kind") != kind
                        or record.get("projectId") != project_id
                        or record.get("dependencies") != dependencies):
                    out.append(("EP-12", f"$bundle.objectStore: exact raw authority chain record {ref!r} is absent or drifted"))

        # Kind compatibility is checked after every safely discoverable reference.
        expected_kinds: dict[str, set[str]] = {}
        def expect_kind(ref: Any, *kinds: str) -> None:
            if isinstance(ref, str) and REF_RE.fullmatch(ref):
                expected_kinds.setdefault(ref, set()).update(kinds)
        for evaluation in evaluations:
            expect_kind(evaluation.get("predicateSemanticsRef"), "predicate-semantics")
            expect_kind(evaluation.get("coverageRef"), "coverage")
            proof = evaluation.get("proof")
            if not isinstance(proof, dict):
                continue
            expect_kind(proof.get("relationSemanticsRef"), "relation-semantics")
            expect_kind(proof.get("reasonRef"), "reason")
            expect_kind(proof.get("factPartitionRef"), "fact-partition")
            for ref in proof.get("factRefs", []) if isinstance(proof.get("factRefs", []), list) else []:
                expect_kind(ref, "fact")
            for edge in proof.get("witnessEdges", []) if isinstance(proof.get("witnessEdges", []), list) else []:
                if isinstance(edge, dict):
                    expect_kind(edge.get("factRef"), "fact")
        if isinstance(vp, dict):
            cov = vp.get("coverage")
            if isinstance(cov, dict): expect_kind(cov.get("coverageRef"), "coverage")
            base = vp.get("baseline")
            if isinstance(base, dict): expect_kind(base.get("baselineRef"), "baseline")
            for waiver in vp.get("waivers", []) if isinstance(vp.get("waivers", []), list) else []:
                if isinstance(waiver, dict): expect_kind(waiver.get("waiverRef"), "waiver")
            pol = vp.get("policy")
            if isinstance(pol, dict): expect_kind(pol.get("policyRef"), "policy")
        for replay in replay_raw if isinstance(replay_raw, list) else []:
            if isinstance(replay, dict): expect_kind(replay.get("ref"), "replay-closure")
        for ref, kinds in expected_kinds.items():
            if ref in store and store[ref].get("kind") not in kinds:
                out.append(("EP-9", f"$bundle.objectStore: {ref} has kind {store[ref].get('kind')!r}, expected {sorted(kinds)}"))

        out.extend(validate_activation_authority(authority, bundle))
        return out
    except Exception as exc:  # totality boundary: caller-controlled JSON never escapes
        out.append(("EP-TOTALITY", f"$bundle: controlled validation failure {type(exc).__name__}: {exc}"))
        return out


NEGATIVE_MUTATION_KINDS = {
    "local-fact-refs-empty", "relationship-proof-tag-substitution",
    "predicate-semantics-object-removed", "subject-set-commitment-substitution",
    "outcome-set-commitment-substitution", "baseline-field-omitted",
    "match-relabeled-pass", "truncated-reference", "referenced-object-removed",
    "required-member-ids-omitted", "unknown-proof-field", "unknown-outcome-shape",
    "arbitrary-policy-and-verdict", "member-delimiter-injection",
    "outcome-delimiter-injection",
    "whole-universe-substitution", "inverse-baseline-waiver-order",
    "semantic-ref-as-cas", "semantic-binding-missing", "semantic-binding-duplicate",
    "semantic-binding-cross-project", "semantic-binding-semantic-substitution",
    "semantic-binding-domain-substitution", "semantic-binding-kind-substitution",
    "semantic-binding-cas-substitution", "valid-raw-wrong-semantic",
    "noncanonical-record-encoding", "outer-commitment-preimage-stored",
    "hidden-unreachable-binding", "versioning-raw-retyped-semantic",
    "downstream-field-in-binding", "authority-record-role-downgrade",
}


def _recompute_declared_commitments(bundle: dict[str, Any]) -> None:
    """Fixture-only helper: keep unrelated commitments coherent after a mutation."""
    evaluations = bundle["evaluations"]
    bundle["requiredUniverse"]["memberIds"] = [
        {"evaluationId": e["evaluationId"], "predicateId": e["predicateId"]}
        for e in sorted(evaluations, key=lambda item: encode_member(item["evaluationId"], item["predicateId"]))
    ]
    bundle["requiredUniverse"]["declaredCount"] = len(evaluations)
    bundle["requiredUniverse"]["universeCommitment"] = commit(
        "universe", [encode_member(e["evaluationId"], e["predicateId"]) for e in evaluations])
    bundle["verdictProof"]["outcomeSetCommitment"] = commit(
        "outcome-set", [encode_outcome(e["evaluationId"], e["predicateId"], e["outcome"])
                        for e in evaluations])
    bundle["verdictProof"]["waiverSetCommitment"] = commit(
        "waiver-set", [encode_waiver(w) for w in bundle["verdictProof"]["waivers"]])
    bundle["verdictProof"]["derivationCommitment"] = derive_verdict_commitment(bundle)


def _materialize_negative(positives: dict[str, dict[str, Any]], vector: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    base_id = vector["baseVectorId"]
    if base_id not in positives:
        raise ValueError(f"unknown baseVectorId {base_id!r}")
    positive = positives[base_id]
    bundle = copy.deepcopy(positive["bundle"])
    authority = copy.deepcopy(positive["verifiedAuthorityInput"])
    mutation = vector["mutation"]
    if not isinstance(mutation, dict) or set(mutation) != {"kind"}:
        raise ValueError("negative mutation must be closed {kind}")
    kind = mutation["kind"]
    if kind not in NEGATIVE_MUTATION_KINDS:
        raise ValueError(f"unknown negative mutation kind {kind!r}")
    evaluation = bundle["evaluations"][0]
    proof = evaluation["proof"]
    def binding(domain: str) -> dict[str, Any]:
        return next(row for row in authority["semanticObjectBindings"]
                    if row["semanticDomain"] == domain)
    def raw_record(kind: str) -> dict[str, Any]:
        return next(row for row in authority["semanticObjectRecords"]
                    if row["recordKind"] == kind)
    def replace_raw_graph_ref(old: str, new: str) -> None:
        for record in bundle["objectStore"]:
            if record["ref"] == old:
                record["ref"] = new
            for dependency in record["dependencies"]:
                if dependency["ref"] == old:
                    dependency["ref"] = new
    def replace_record_bytes(domain: str, raw: bytes) -> None:
        row = binding(domain)
        record = raw_record(row["recordKind"])
        old = row["recordCasRef"]
        new = "sha256:" + hashlib.sha256(raw).hexdigest()
        row["recordCasRef"] = new
        record["recordCasRef"] = new
        record["recordBytesHex"] = raw.hex()
        replace_raw_graph_ref(old, new)
    if kind == "local-fact-refs-empty":
        proof["factRefs"] = []
    elif kind == "relationship-proof-tag-substitution":
        evaluation["proof"] = {"kind": "local-match-proof", "subjectId": "src/a.ts", "factRefs": proof.get("factRefs", [])}
    elif kind == "predicate-semantics-object-removed":
        ref = evaluation["predicateSemanticsRef"]
        bundle["objectStore"] = [obj for obj in bundle["objectStore"] if obj["ref"] != ref]
    elif kind == "subject-set-commitment-substitution":
        proof["subjectSetCommitment"] = "sha256:" + "d" * 64
    elif kind == "outcome-set-commitment-substitution":
        bundle["verdictProof"]["outcomeSetCommitment"] = "sha256:" + "d" * 64
    elif kind == "baseline-field-omitted":
        del bundle["verdictProof"]["baseline"]
    elif kind == "match-relabeled-pass":
        bundle["verdictProof"]["verdict"] = "pass"
    elif kind == "truncated-reference":
        if "factPartitionRef" in proof:
            proof["factPartitionRef"] = "sha256:abcd"
        else:
            proof["factRefs"][0] = "sha256:abcd"
    elif kind == "referenced-object-removed":
        target = next(iter(_proof_refs(evaluation)))
        bundle["objectStore"] = [obj for obj in bundle["objectStore"] if obj["ref"] != target]
    elif kind == "required-member-ids-omitted":
        del bundle["requiredUniverse"]["memberIds"]
    elif kind == "unknown-proof-field":
        proof["trusted"] = True
    elif kind == "unknown-outcome-shape":
        evaluation["outcome"] = "partial-but-clean"
        evaluation["claimShape"] = "future-shape"
        evaluation["proof"] = {}
        _recompute_declared_commitments(bundle)
    elif kind == "arbitrary-policy-and-verdict":
        bundle["verdictProof"]["policy"]["matchDisposition"] = "always-pass"
        bundle["verdictProof"]["verdict"] = "pass"
    elif kind == "member-delimiter-injection":
        evaluation["evaluationId"] = "a"
        evaluation["predicateId"] = "b\x1fc"
        _recompute_declared_commitments(bundle)
    elif kind == "outcome-delimiter-injection":
        evaluation["outcome"] = "c\x1fd"
        _recompute_declared_commitments(bundle)
    elif kind == "whole-universe-substitution":
        replacements: dict[tuple[str, str], tuple[str, str]] = {}
        for index, row in enumerate(bundle["evaluations"], 1):
            old = (row["evaluationId"], row["predicateId"])
            replacements[old] = (f"eval1:substitute.{index}", f"predicate1:substitute.{index}")
            row["evaluationId"], row["predicateId"] = replacements[old]
        baseline = bundle["verdictProof"]["baseline"]
        for row in baseline.get("matchedMembers", []):
            row["evaluationId"], row["predicateId"] = replacements[(row["evaluationId"], row["predicateId"])]
        for waiver in bundle["verdictProof"]["waivers"]:
            target = waiver["target"]
            target["evaluationId"], target["predicateId"] = replacements[(target["evaluationId"], target["predicateId"])]
        _recompute_declared_commitments(bundle)
    elif kind == "inverse-baseline-waiver-order":
        bundle["verdictProof"]["policy"]["evaluationOrder"] = [
            "indeterminate-or-error-dominates", "validate-exact-waivers",
            "classify-baseline-match-as-advisory", "suppress-waived-current-matches",
            "classify-effective-new-match-as-fail", "classify-no-effective-match-as-pass",
        ]
        bundle["verdictProof"]["verdict"] = "advisory"
        bundle["verdictProof"]["derivationCommitment"] = derive_verdict_commitment(bundle)
    elif kind == "semantic-ref-as-cas":
        row = binding("activation-manifest-v1")
        row["recordCasRef"] = row["semanticRef"]
    elif kind == "semantic-binding-missing":
        authority["semanticObjectBindings"].pop()
    elif kind == "semantic-binding-duplicate":
        authority["semanticObjectBindings"].append(copy.deepcopy(authority["semanticObjectBindings"][0]))
        authority["semanticObjectBindings"].sort(key=encode_semantic_object_binding)
    elif kind == "semantic-binding-cross-project":
        binding("activation-manifest-v1")["projectId"] = "prj1-" + "b" * 64
    elif kind == "semantic-binding-semantic-substitution":
        binding("activation-manifest-v1")["semanticRef"] = "sha256:" + "0" * 64
    elif kind == "semantic-binding-domain-substitution":
        binding("activation-manifest-v1")["semanticDomain"] = "subject-set"
        authority["semanticObjectBindings"].sort(key=encode_semantic_object_binding)
    elif kind == "semantic-binding-kind-substitution":
        binding("activation-manifest-v1")["recordKind"] = "EvaluationAuthoritySealV1"
    elif kind == "semantic-binding-cas-substitution":
        binding("activation-manifest-v1")["recordCasRef"] = "sha256:" + "0" * 64
    elif kind == "valid-raw-wrong-semantic":
        binding("activation-manifest-v1")["semanticRef"] = binding("evaluation-authority-seal-v1")["semanticRef"]
    elif kind == "noncanonical-record-encoding":
        raw = bytes.fromhex(raw_record("ActivationManifestV1")["recordBytesHex"])
        noncanonical = raw[:2] + (2).to_bytes(4, "big") + b"01" + raw[7:]
        replace_record_bytes("activation-manifest-v1", noncanonical)
    elif kind == "outer-commitment-preimage-stored":
        raw = bytes.fromhex(raw_record("ActivationManifestV1")["recordBytesHex"])
        replace_record_bytes("activation-manifest-v1", commitment_preimage("activation-manifest-v1", [raw]))
    elif kind == "hidden-unreachable-binding":
        authority["semanticObjectBindings"].append({
            "projectId": bundle["projectId"], "semanticDomain": "activation-manifest-v1",
            "semanticRef": "sha256:" + "7" * 64, "recordCasRef": "sha256:" + "8" * 64,
            "recordKind": "ActivationManifestV1",
        })
        authority["semanticObjectBindings"].sort(key=encode_semantic_object_binding)
    elif kind == "versioning-raw-retyped-semantic":
        target = next(row for row in bundle["objectStore"] if row["kind"] == "historical-manifest")
        old = target["ref"]
        new = binding("activation-manifest-v1")["semanticRef"]
        replace_raw_graph_ref(old, new)
    elif kind == "downstream-field-in-binding":
        binding("activation-manifest-v1")["runId"] = "run1:" + "0" * 64
    elif kind == "authority-record-role-downgrade":
        receipt = authority["authoritySealAdmission"]["verificationReceiptRef"]
        record = next(row for row in bundle["objectStore"] if row["ref"] == receipt)
        record["dependencies"][0]["role"] = "policy-verifier"
    return bundle, authority


def _canonical_json_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _encode_golden_record(record_type: str, value: Any) -> bytes:
    if record_type == "MemberV1":
        return encode_member(value["evaluationId"], value["predicateId"])
    if record_type == "OutcomeV1":
        return encode_outcome(value["evaluationId"], value["predicateId"], value["outcome"])
    if record_type == "SubjectV1":
        return encode_subject(value["value"])
    if record_type == "WaiverV1":
        return encode_waiver(value)
    if record_type in {"BaselineV1:none", "BaselineV1:comparison"}:
        return _baseline_bytes(value)
    if record_type == "PolicyV2":
        return _policy_bytes(value)
    if record_type == "VerdictInputV2":
        return _verdict_input_bytes({"verdictProof": value})
    if record_type == "ActivationMemberV1":
        return encode_activation_member(value)
    if record_type == "ActivationManifestV1":
        return encode_activation_manifest(value)
    if record_type == "EvaluationAuthoritySealV1":
        return encode_evaluation_authority_seal(value)
    if record_type == "SemanticObjectBindingV1":
        return encode_semantic_object_binding(value)
    raise ValueError(f"unknown golden record type {record_type!r}")


def _check_normative_preimage_contract(contract: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    grammar = contract.get("normativePreimageGrammar")
    try:
        actual_sha = _canonical_json_sha256(grammar)
        if contract.get("normativePreimageGrammarSha256") != actual_sha:
            findings.append("EP-8: normativePreimageGrammarSha256 does not recompute")
        if actual_sha != EXPECTED_GRAMMAR_SHA256:
            findings.append("EP-8: normativePreimageGrammar differs from the independently pinned v5 grammar")
        if grammar.get("namespaceUtf8") != NS.decode("utf-8"):
            findings.append("EP-8: normative grammar namespace drift")
        expected_records = {
            "MemberV1", "OutcomeV1", "WaiverV1", "SubjectV1", "BaselineV1",
            "PolicyV2", "VerdictInputV2", "ActivationManifestV1", "ActivationMemberV1",
            "EvaluationAuthoritySealV1", "SemanticObjectBindingV1",
        }
        rows = grammar.get("records")
        if not isinstance(rows, list) or {row.get("name") for row in rows if isinstance(row, dict)} != expected_records:
            findings.append("EP-8: normative grammar must declare every and only the eleven committed record families")
        else:
            for row in rows:
                name = row["name"]
                _record_tag(name)
                order = _declared_order(name)
                for field in row["fields"]:
                    tag = _field_tag(name, field["name"])
                    if name == "EvaluationAuthoritySealV1":
                        lower, upper = 0x58, 0x5D
                    elif name == "SemanticObjectBindingV1":
                        lower, upper = 0x5E, 0x62
                    else:
                        lower, upper = 0x01, 0x57
                    if not lower <= tag <= upper:
                        findings.append(f"EP-8: {name}.{field['name']} tag is outside its declared legacy/seal range")
                    if set(field) != {"name", "tag", "encoding", "presence"}:
                        findings.append(f"EP-8: {name}.{field.get('name')} field grammar is not closed")
                if len(order) != len(set(order)):
                    findings.append(f"EP-8: {name} field order contains a duplicate")
        commitment = grammar.get("commitment")
        if not isinstance(commitment, dict) or set(commitment) != {
            "algorithm", "leaf", "internal", "oddNode", "empty", "outer",
            "itemSetRule", "digestText",
        }:
            findings.append("EP-8: commitment grammar is incomplete or open")
        else:
            _commitment_tag("leaf")
            _commitment_tag("internal")
            _commitment_tag("empty")
            _commitment_tag("empty", "namespaceBlobTag")
            for key in ("recordTag", "namespaceTag", "domainTag", "merkleRootTag"):
                _commitment_tag("outer", key)
        seal_schema = _record_schema("EvaluationAuthoritySealV1")
        forbidden = ["requestId", "executionId", "runId", "evidenceDigest", "verdict", "outcome", "sealedCapability", "effectiveCapability", "runSealRef", "clocks", "physicalLocators"]
        if seal_schema.get("forbiddenFields") != forbidden:
            findings.append("EP-12: EvaluationAuthoritySealV1 forbiddenFields list is incomplete or reordered")
        binding_forbidden = ["bindingId", "requestId", "executionId", "runId", "runSealRef", "evidenceDigest", "verdict", "outcome", "sealedCapability", "effectiveCapability", "objectState", "lease", "fence", "ledger", "clocks", "physicalLocators"]
        if _record_schema("SemanticObjectBindingV1").get("forbiddenFields") != binding_forbidden:
            findings.append("EP-12: SemanticObjectBindingV1 forbiddenFields list is incomplete or reordered")
        if grammar.get("domains") != ["universe", "subject-set", "outcome-set", "waiver-set", "verdict-input", "activation-manifest-v1", "evaluation-authority-seal-v1", "capability-closure", "semantic-capability-closure-v3"]:
            findings.append("EP-8: normative commitment domains/order drift")
    except Exception as exc:
        findings.append(f"EP-8: normative grammar cannot drive encoders ({type(exc).__name__}: {exc})")

    goldens = contract.get("preimageGoldens")
    if not isinstance(goldens, dict) or set(goldens) != {"purpose", "records", "commitments"}:
        return findings + ["EP-8: preimageGoldens must be a closed records/commitments object"]
    expected_types = {
        "MemberV1", "OutcomeV1", "SubjectV1", "WaiverV1", "BaselineV1:none",
        "BaselineV1:comparison", "PolicyV2", "VerdictInputV2", "ActivationMemberV1",
        "ActivationManifestV1",
        "EvaluationAuthoritySealV1", "SemanticObjectBindingV1",
    }
    record_rows = goldens.get("records")
    if not isinstance(record_rows, list) or {x.get("recordType") for x in record_rows if isinstance(x, dict)} != expected_types:
        findings.append("EP-8: record goldens do not cover every nested record/variant exactly once")
    else:
        for i, row in enumerate(record_rows):
            if set(row) != {"id", "recordType", "value", "encodedHex", "recordSha256"}:
                findings.append(f"EP-8: record golden[{i}] is not closed")
                continue
            try:
                encoded = _encode_golden_record(row["recordType"], row["value"])
                if row.get("encodedHex") != encoded.hex():
                    findings.append(f"EP-8: {row.get('id')} encodedHex disagrees with declared grammar")
                if row.get("recordSha256") != "sha256:" + hashlib.sha256(encoded).hexdigest():
                    findings.append(f"EP-8: {row.get('id')} recordSha256 disagrees")
            except Exception as exc:
                findings.append(f"EP-8: record golden[{i}] cannot encode ({type(exc).__name__}: {exc})")

    commitment_rows = goldens.get("commitments")
    expected_domains = set(_grammar().get("domains", [])) if isinstance(grammar, dict) else set()
    if not isinstance(commitment_rows, list) or {x.get("domain") for x in commitment_rows if isinstance(x, dict)} != expected_domains:
        findings.append("EP-8: commitment goldens do not cover every domain exactly once")
    else:
        for i, row in enumerate(commitment_rows):
            if set(row) != {"id", "domain", "itemEncodedHex", "sortedUniqueItemHex", "leafHashHex", "merkleRootHex", "outerPreimageHex", "commitment"}:
                findings.append(f"EP-8: commitment golden[{i}] is not closed")
                continue
            try:
                items = [bytes.fromhex(x) for x in row["itemEncodedHex"]]
                ordered = sorted(set(items))
                leaves = [_leaf(x) for x in ordered]
                root = _merkle(items)
                preimage = commitment_preimage(row["domain"], items)
                if row.get("sortedUniqueItemHex") != [x.hex() for x in ordered]:
                    findings.append(f"EP-8: {row.get('id')} sorted/deduplicated item golden disagrees")
                if row.get("leafHashHex") != [x.hex() for x in leaves]:
                    findings.append(f"EP-8: {row.get('id')} leaf hash golden disagrees")
                if row.get("merkleRootHex") != root.hex():
                    findings.append(f"EP-8: {row.get('id')} Merkle root golden disagrees")
                if row.get("outerPreimageHex") != preimage.hex():
                    findings.append(f"EP-8: {row.get('id')} outer preimage golden disagrees")
                if row.get("commitment") != "sha256:" + hashlib.sha256(preimage).hexdigest():
                    findings.append(f"EP-8: {row.get('id')} commitment golden disagrees")
            except Exception as exc:
                findings.append(f"EP-8: commitment golden[{i}] cannot recompute ({type(exc).__name__}: {exc})")
    return findings


def _historical_graph_findings(bundle: Any, authority_input: Any) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    try:
        if not isinstance(bundle, dict):
            return [("EP-9", "VERSIONING join bundle is not an object")]
        project = bundle["projectId"]
        policy_ref = bundle["verdictProof"]["policy"]["policyRef"]
        semantics_ref = HISTORICAL_DEPENDENCIES["historical-semantics"]
        expected_edges = {(policy_ref, semantics_ref, project, "historical-semantics")}
        expected_edges |= {
            (semantics_ref, ref, project, role)
            for role, ref in HISTORICAL_DEPENDENCIES.items() if role != "historical-semantics"
        }
        records = bundle.get("objectStore")
        if not isinstance(records, list):
            return [("EP-9", "VERSIONING join objectStore is not an array")]
        observed_edges: set[tuple[str, str, str, str]] = set()
        by_ref: dict[str, list[dict[str, Any]]] = {}
        for record in records:
            if not isinstance(record, dict):
                continue
            if isinstance(record.get("ref"), str):
                by_ref.setdefault(record["ref"], []).append(record)
            for dep in record.get("dependencies", []) if isinstance(record.get("dependencies"), list) else []:
                if not isinstance(dep, dict):
                    continue
                if dep.get("role") in set(HISTORICAL_DEPENDENCIES) or dep.get("ref") in set(HISTORICAL_DEPENDENCIES.values()):
                    observed_edges.add((record.get("ref"), dep.get("ref"), dep.get("projectId"), dep.get("role")))
        if observed_edges != expected_edges:
            out.append(("EP-9", "VERSIONING-v4 historical dependency edges are omitted, aliased, mislabeled, or injected"))
        for role, ref in HISTORICAL_DEPENDENCIES.items():
            rows = by_ref.get(ref, [])
            if len(rows) != 1 or rows[0].get("kind") != role or rows[0].get("projectId") != project:
                out.append(("EP-9", f"VERSIONING-v4 {role} object is absent, duplicated, mislabeled, or cross-project"))
        try:
            derived = derive_proof_requirements(bundle, authority=authority_input)
            for role, ref in HISTORICAL_DEPENDENCIES.items():
                if derived.get(ref) != "verifiable":
                    out.append(("EP-9", f"VERSIONING-v4 {role} does not carry exact verifiable minimum"))
        except Exception as exc:
            out.append(("EP-9", f"VERSIONING-v4 closure derivation failed ({type(exc).__name__}: {exc})"))
    except Exception as exc:
        out.append(("EP-9", f"VERSIONING-v4 graph check failed closed ({type(exc).__name__}: {exc})"))
    return out


def _check_versioning_role_join(contract: dict[str, Any], positives: dict[str, dict[str, Any]]) -> list[str]:
    findings: list[str] = []
    join = contract.get("versioningV4RoleJoin")
    required = {
        "sourceArtifact", "sourceSha256", "sourceFixtureId", "vocabularyOwner",
        "closedDependencyRoles", "propagationRule", "positiveVectorId",
        "historicalDependencies", "negativeControls",
    }
    if not isinstance(join, dict) or set(join) != required:
        return ["EP-9: versioningV4RoleJoin must be a closed exact role/custody contract"]
    try:
        live = _load(HERE / VERSIONING)
        if join.get("sourceArtifact") != VERSIONING or join.get("sourceSha256") != VERSIONING_SHA256 or _sha256_file(HERE / VERSIONING) != VERSIONING_SHA256:
            findings.append("EP-9: VERSIONING-v4 role join does not bind the exact live artifact")
        live_roles = live["historicalSemanticsPolicy"]["dependencyRoles"]
        if live_roles != list(HISTORICAL_DEPENDENCIES):
            findings.append("EP-9: live VERSIONING-v4 six-role vocabulary differs")
        fixture = next(x for x in live["historicalSemanticsPolicy"]["crossMajorFixtures"]
                       if x.get("id") == join.get("sourceFixtureId"))
        fixture_refs = {x["ref"] for x in fixture["expect"]["requiredDependencies"]
                        if x.get("requiredForCapability") == "verifiable"}
        if fixture_refs != set(HISTORICAL_DEPENDENCIES.values()):
            findings.append("EP-9: VERSIONING-v4 positive fixture dependency refs differ")
    except Exception as exc:
        findings.append(f"EP-9: live VERSIONING-v4 role join unavailable ({type(exc).__name__}: {exc})")
    expected_dependencies = [
        {"role": role, "ref": ref, "requiredForCapability": "verifiable"}
        for role, ref in HISTORICAL_DEPENDENCIES.items()
    ]
    if join.get("closedDependencyRoles") != DEPENDENCY_ROLE_ORDER or join.get("historicalDependencies") != expected_dependencies:
        findings.append("EP-9: joined role vocabulary/refs/minima are not exact")
    vector = positives.get(join.get("positiveVectorId"))
    if not isinstance(vector, dict):
        return findings + ["EP-9: VERSIONING-v4 positive join vector is absent"]
    hits = _historical_graph_findings(vector.get("bundle"), vector.get("verifiedAuthorityInput"))
    findings.extend(f"{inv}: {msg}" for inv, msg in hits)

    expected_controls = ([{"kind": "historical-ref-omitted", "role": role, "expectedInvariant": "EP-9"}
                          for role in HISTORICAL_DEPENDENCIES]
                         + [{"kind": "historical-role-mislabeled", "role": role, "expectedInvariant": "EP-9"}
                            for role in HISTORICAL_DEPENDENCIES]
                         + [{"kind": "unknown-historical-role", "role": "historical-semantics", "expectedInvariant": "EP-11"},
                            {"kind": "injected-unreachable-historical-edge", "role": "historical-public-key", "expectedInvariant": "EP-9"}])
    if join.get("negativeControls") != expected_controls:
        findings.append("EP-9: VERSIONING-v4 controls must cover every omission/mislabel plus unknown/injected roles")
        return findings
    for control in expected_controls:
        mutated = copy.deepcopy(vector)
        bundle = mutated["bundle"]
        role = control["role"]
        target = HISTORICAL_DEPENDENCIES[role]
        edges = [(record, dep) for record in bundle["objectStore"] for dep in record["dependencies"] if dep.get("ref") == target]
        if control["kind"] == "historical-ref-omitted":
            edges[0][0]["dependencies"].remove(edges[0][1])
        elif control["kind"] == "historical-role-mislabeled":
            edges[0][1]["role"] = "policy-verifier"
        elif control["kind"] == "unknown-historical-role":
            edges[0][1]["role"] = "historical-future"
        else:
            anchor = next(record for record in bundle["objectStore"] if record["ref"] == "sha256:" + "93" * 32)
            anchor["dependencies"].append({"ref": target, "projectId": bundle["projectId"], "role": role})
        graph_hit_ids = {inv for inv, _ in _historical_graph_findings(bundle, mutated["verifiedAuthorityInput"])}
        if control["kind"] == "unknown-historical-role":
            graph_hit_ids |= {inv for inv, _ in validate_bundle(bundle, mutated["verifiedAuthorityInput"])}
        if control["expectedInvariant"] not in graph_hit_ids:
            findings.append(f"{control['expectedInvariant']}: VERSIONING control {control['kind']}:{role} escaped")
    return findings


def _check_impl(value: Any) -> list[str]:
    findings: list[str] = []
    root_out: list[tuple[str, str]] = []
    contract = _exact_object(value, TOP_KEYS, set(), "$contract", root_out)
    findings.extend(f"{inv}: {msg}" for inv, msg in root_out)
    if contract is None:
        return [f"EP-11: $contract expected object, got {type(value).__name__}"]

    if contract.get("artifact") != "opensip.evaluation-proof":
        findings.append("EP-11: artifact must be opensip.evaluation-proof")
    if contract.get("version") != EXPECTED_VERSION:
        findings.append(f"EP-8: version must be integer {EXPECTED_VERSION}")
    if contract.get("status") != "CANDIDATE-AWAITING-INDEPENDENT-COMBINED-REREVIEW":
        findings.append("assurance: v5 must remain CANDIDATE-AWAITING-INDEPENDENT-COMBINED-REREVIEW")

    _set_active_grammar(contract.get("normativePreimageGrammar"))
    findings.extend(_check_normative_preimage_contract(contract))

    grammar = contract.get("canonicalCommitmentGrammar")
    grammar_out: list[tuple[str, str]] = []
    grammar_obj = _exact_object(grammar, {
        "version", "namespace", "component", "records", "leaf", "internal", "oddNode",
        "emptySet", "outer", "ordering", "truncation", "domains",
    }, set(), "$contract.canonicalCommitmentGrammar", grammar_out, "EP-8")
    findings.extend(f"{inv}: {msg}" for inv, msg in grammar_out)
    if grammar_obj is not None:
        expected = {
            "version": "typed-component-merkle-v5-declared",
            "namespace": NS.decode(),
            "component": "uint8(typeTag) || uint32be(len(utf8)) || utf8",
            "records": "Normative detail is closed by normativePreimageGrammar; this summary is non-substitutive.",
            "leaf": "sha256(0x00 || uint64be(len(record)) || record)",
            "internal": "sha256(0x01 || left || right)",
            "oddNode": "promote unchanged",
            "emptySet": "sha256(0x02 || frameBlob(0x30, namespace))",
            "outer": "sha256(0x30 || frameBlob(0x31,namespace) || frameBlob(0x32,domain) || frameBlob(0x33,merkleRoot))",
            "ordering": "deduplicate exact record bytes then sort unsigned bytewise ascending",
            "truncation": "FORBIDDEN",
        }
        for key, expected_value in expected.items():
            if grammar_obj.get(key) != expected_value:
                findings.append(f"EP-8: canonicalCommitmentGrammar.{key} drifted from the executable v2 grammar")
        if grammar_obj.get("domains") != ["universe", "subject-set", "outcome-set", "waiver-set", "verdict-input", "activation-manifest-v1", "evaluation-authority-seal-v1", "capability-closure", "semantic-capability-closure-v3"]:
            findings.append("EP-8: commitment domains are not the exact v5 semantic-custody ordered list")

    expected_wire_grammars = {
        "evaluationId": {"jsonType": "string", "pattern": r"^eval1:[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$", "controlCharacters": "FORBIDDEN"},
        "predicateId": {"jsonType": "string", "pattern": r"^predicate1:[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$", "controlCharacters": "FORBIDDEN"},
        "projectId": {"jsonType": "string", "pattern": r"^prj1-[0-9a-f]{64}$", "source": "resolved-inputs.v2.json#projectIdContract/PROJECT-ID-V1"},
        "planId": {"jsonType": "string", "pattern": r"^plan1:sha256:[0-9a-f]{64}$", "source": "resolved-inputs.v2.json#planIdContract"},
        "activationId": {"jsonType": "string", "pattern": r"^act1:[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$", "controlCharacters": "FORBIDDEN"},
        "contentRef": {"jsonType": "string", "pattern": r"^sha256:[0-9a-f]{64}$"},
        "outcome": {"closedEnum": ["match", "no-match", "indeterminate", "error"]},
        "claimShape": {"closedEnum": ["local-match", "relationship-match", "aggregate-match", "no-match", "indeterminate", "error"]},
        "verdict": {"closedEnum": ["pass", "fail", "advisory", "indeterminate"]},
        "dependencyRole": {"closedEnum": DEPENDENCY_ROLE_ORDER},
    }
    if contract.get("wireGrammars") != expected_wire_grammars:
        findings.append("EP-8: wireGrammars must exactly bind the executable identifier/value grammars and closed enums")

    if contract.get("referenceTypeRegistry") != EXPECTED_REFERENCE_TYPE_REGISTRY:
        findings.append("EP-12: referenceTypeRegistry must exactly discriminate semantic commitments, raw CAS identities, and non-retrievable digests")
    if contract.get("semanticObjectBindingContract") != EXPECTED_SEMANTIC_BINDING_CONTRACT:
        findings.append("EP-12: semanticObjectBindingContract must exactly bind the two typed domains to canonical raw record custody")

    expected_policy_semantics = {
        "id": "policy-ir-2", "owner": "pure evaluation core",
        "inputs": ["complete outcome set", "coverage status", "baseline match set", "waiver target set", "policy semantics identity"],
        "precedence": POLICY_EVALUATION_ORDER,
        "hostRule": "The host seals the core-returned policyOutcome and MUST NOT rederive a different verdict. Independent readers replay these same pure semantics to verify it.",
        "baselineRule": "Classify only effective matches remaining after exact waiver suppression; an effective baseline match is advisory.",
        "waiverRule": "Validate exact content-addressed waivers, then suppress each targeted current match before any baseline classification.",
    }
    if contract.get("policySemanticsV2") != expected_policy_semantics:
        findings.append("EP-13: policySemanticsV2 must exactly match waiver-before-baseline policy-ir-2")

    expected_authority_contract = {
        "inputType": "VerifiedEvaluationAuthorityInputV2",
        "evaluationAuthorityType": "EvaluationAuthoritySealV1",
        "trustedInputRule": "Only the exact closed v2 opensip-evidence envelope with two typed semantic bindings and two exact raw records is accepted; raw/semantic aliasing, binding-only availability, and producer/caller assertions are rejected.",
        "timing": "EvaluationAuthoritySealV1 is content-addressed and admitted before evaluation; terminal RunId/runSealRef are derived only after semantic EvidenceDigest validation.",
        "forbiddenInAuthoritySeal": ["requestId", "executionId", "runId", "evidenceDigest", "verdict", "outcome", "sealedCapability", "effectiveCapability", "runSealRef", "clocks", "physicalLocators"],
        "forbiddenInSemanticProof": ["runId", "runSealRef", "terminalRunRef"],
        "producerAuthority": "NONE",
    }
    if contract.get("activationAuthority") != expected_authority_contract:
        findings.append("EP-12: activationAuthority must exactly specify the lifecycle-neutral Evidence admission boundary")

    seam = contract.get("authoritySeam")
    if not isinstance(seam, dict) or set(seam) != {
        "status", "consumerBoundary", "requiredPlanProof", "requiredStoreProof",
        "evidenceOwner", "epVerificationLimit", "failureRule", "acceptedInputFields",
        "negativeControls", "notClaimed",
    }:
        findings.append("EP-12: authoritySeam must be the exact closed RR13-01 pending contract")
    elif (seam.get("status") != "RR13-01-PENDING-COORDINATED-EVIDENCE-OP-STORE-SUCCESSOR"
          or seam.get("acceptedInputFields") != ["schemaVersion", "interfaceId", "suppliedBy", "planIdAdmission", "authoritySealAdmission", "evaluationAuthoritySeal", "activationManifest", "semanticObjectBindings", "semanticObjectRecords"]
          or seam.get("negativeControls") != ["raw-authority-seal", "bundle-local-authority", "boolean-verified", "wrong-plan-owner", "wrong-store-owner", "cross-project-store-admission", "authority-seal-manifest-mismatch", "plan-id-admission-mismatch", "terminal-field-in-authority-seal", "terminal-field-in-semantic-bundle", "semantic-ref-as-cas", "semantic-binding-missing", "semantic-binding-duplicate", "semantic-binding-cross-project", "semantic-binding-semantic-substitution", "semantic-binding-domain-substitution", "semantic-binding-kind-substitution", "semantic-binding-cas-substitution", "valid-raw-wrong-semantic", "noncanonical-record-encoding", "outer-commitment-preimage-stored", "hidden-unreachable-binding", "versioning-raw-retyped-semantic", "downstream-field-in-binding", "authority-record-role-downgrade"]
          or "RR13-01 is closed" not in seam.get("notClaimed", [])):
        findings.append("EP-12: authoritySeam drifted, overclaimed closure, or admitted a raw/boolean authority path")

    c2_join_out: list[tuple[str, str]] = []
    c2_join = _exact_object(contract.get("c2AuthorityJoin"), {
        "sourceArtifact", "sourceSha256", "planIntentFixtureId", "intentBindingFixtureId",
        "planId", "expectedPlanIntentCommitment", "executionPlanCommitment",
        "authorityVectorIds",
    }, set(), "$contract.c2AuthorityJoin", c2_join_out, "EP-12")
    findings.extend(f"{inv}: {msg}" for inv, msg in c2_join_out)
    if c2_join is not None:
        try:
            c2_contract = _load(HERE / C2)
            c2mod = _load_c2_module()
            if c2_join.get("sourceArtifact") != C2 or c2_join.get("sourceSha256") != _sha256_file(HERE / C2):
                findings.append("EP-12: C2 activation join does not hash-bind the exact live artifact")
            fixture_id = c2_join.get("planIntentFixtureId")
            fixture = next(row for row in c2_contract["planIntentFixtures"] if row.get("id") == fixture_id and isinstance(row.get("intent"), dict))
            commitment = c2mod.plan_intent_commitment(fixture["intent"], c2_contract)
            if c2_join.get("expectedPlanIntentCommitment") != commitment or c2_join.get("executionPlanCommitment") != commitment:
                findings.append("EP-12: C2 PlanIntent/ExecutionPlan commitment equality does not recompute")
            binding = next(row for row in c2_contract["intentBindingFixtures"] if row.get("id") == c2_join.get("intentBindingFixtureId"))
            if binding.get("baseFixtureId") != fixture_id:
                findings.append("EP-12: C2 intent-binding fixture does not consume the named admitted PlanIntent")
            if not _string(c2_join.get("planId"), "$contract.c2AuthorityJoin.planId", c2_join_out, PLAN_RE, "EP-12"):
                findings.append("EP-12: C2 authority join PlanId is malformed")
        except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError, ImportError, KeyError, StopIteration, TypeError, ValueError) as exc:
            findings.append(f"EP-12: live C2 activation join unavailable or malformed ({type(exc).__name__}: {exc})")

    schemas = contract.get("persistedSchemaRegistry")
    schema_out: list[tuple[str, str]] = []
    schema_list = _list(schemas, "$contract.persistedSchemaRegistry", schema_out)
    findings.extend(f"{inv}: {msg}" for inv, msg in schema_out)
    required_schemas = set(SCHEMA_FIELDS)
    seen_schema: set[str] = set()
    if schema_list is not None:
        for i, schema in enumerate(schema_list):
            local: list[tuple[str, str]] = []
            obj = _exact_object(schema, {"name", "closed", "required", "optional"}, set(), f"$contract.persistedSchemaRegistry[{i}]", local)
            findings.extend(f"{inv}: {msg}" for inv, msg in local)
            if obj is None:
                continue
            if not isinstance(obj.get("name"), str) or obj["name"] in seen_schema:
                findings.append(f"EP-11: persistedSchemaRegistry[{i}] has missing/duplicate name")
            else:
                seen_schema.add(obj["name"])
            if obj.get("closed") is not True:
                findings.append(f"EP-11: schema {obj.get('name')!r} is not recursively closed")
            if not isinstance(obj.get("required"), list) or any(not isinstance(x, str) for x in obj.get("required", [])):
                findings.append(f"EP-11: schema {obj.get('name')!r}.required is not a string array")
            if not isinstance(obj.get("optional"), list) or any(not isinstance(x, str) for x in obj.get("optional", [])):
                findings.append(f"EP-11: schema {obj.get('name')!r}.optional is not a string array")
            if obj.get("name") in SCHEMA_FIELDS and isinstance(obj.get("required"), list) and isinstance(obj.get("optional"), list):
                expected_required, expected_optional = SCHEMA_FIELDS[obj["name"]]
                if len(obj["required"]) != len(set(obj["required"])) or set(obj["required"]) != expected_required:
                    findings.append(f"EP-11: schema {obj['name']}.required does not bind the executable fields")
                if len(obj["optional"]) != len(set(obj["optional"])) or set(obj["optional"]) != expected_optional:
                    findings.append(f"EP-11: schema {obj['name']}.optional does not bind the executable fields")
        if seen_schema != required_schemas:
            findings.append(f"EP-11: persisted schema registry names differ: missing={sorted(required_schemas-seen_schema)}, extra={sorted(seen_schema-required_schemas)}")

    invariants = contract.get("invariants")
    inv_out: list[tuple[str, str]] = []
    inv_list = _list(invariants, "$contract.invariants", inv_out)
    findings.extend(f"{inv}: {msg}" for inv, msg in inv_out)
    declared: set[str] = set()
    if inv_list is not None:
        for i, invariant in enumerate(inv_list):
            local: list[tuple[str, str]] = []
            obj = _exact_object(invariant, {"id", "assert"}, set(), f"$contract.invariants[{i}]", local)
            findings.extend(f"{inv}: {msg}" for inv, msg in local)
            if obj is not None and isinstance(obj.get("id"), str):
                declared.add(obj["id"])
    expected_invariants = {f"EP-{i}" for i in range(1, 14)}
    if declared != expected_invariants:
        findings.append(f"EP-11: invariant registry must be exactly EP-1..EP-13, got {sorted(declared)}")

    positives = contract.get("positiveVectors")
    pos_out: list[tuple[str, str]] = []
    pos_list = _list(positives, "$contract.positiveVectors", pos_out)
    findings.extend(f"{inv}: {msg}" for inv, msg in pos_out)
    positive_vectors: dict[str, dict[str, Any]] = {}
    ordered_positive_ids: list[str] = []
    if pos_list is not None:
        seen_ids: set[str] = set()
        for i, vector in enumerate(pos_list):
            local: list[tuple[str, str]] = []
            obj = _exact_object(vector, {"id", "why", "verifiedAuthorityInput", "bundle"}, set(), f"$contract.positiveVectors[{i}]", local)
            findings.extend(f"{inv}: {msg}" for inv, msg in local)
            if obj is None:
                continue
            vid = obj.get("id", f"positive[{i}]")
            if not isinstance(vid, str) or vid in seen_ids:
                findings.append(f"EP-11: positive vector id {vid!r} is missing/duplicate")
            elif isinstance(vid, str):
                seen_ids.add(vid)
                ordered_positive_ids.append(vid)
                if isinstance(obj.get("bundle"), dict) and isinstance(obj.get("verifiedAuthorityInput"), dict):
                    positive_vectors[vid] = {"bundle": obj["bundle"], "verifiedAuthorityInput": obj["verifiedAuthorityInput"]}
            hits = validate_bundle(obj.get("bundle"), obj.get("verifiedAuthorityInput"))
            if hits:
                findings.append(f"{vid}: positive vector violates {sorted({x for x, _ in hits})}: {hits[0][1]}")
            if isinstance(c2_join, dict) and isinstance(obj.get("verifiedAuthorityInput"), dict):
                authority = obj["verifiedAuthorityInput"].get("evaluationAuthoritySeal", {})
                for authority_key, join_key in (("planId", "planId"), ("planIntentCommitment", "expectedPlanIntentCommitment"), ("executionPlanCommitment", "executionPlanCommitment")):
                    if authority.get(authority_key) != c2_join.get(join_key):
                        findings.append(f"EP-12: {vid} authority {authority_key} differs from live C2 join")
    if isinstance(c2_join, dict) and c2_join.get("authorityVectorIds") != ordered_positive_ids:
        findings.append("EP-12: c2AuthorityJoin.authorityVectorIds must exactly enumerate every positive authority")

    findings.extend(_check_versioning_role_join(contract, positive_vectors))

    negatives = contract.get("adversarialNegatives")
    neg_out: list[tuple[str, str]] = []
    neg_list = _list(negatives, "$contract.adversarialNegatives", neg_out)
    findings.extend(f"{inv}: {msg}" for inv, msg in neg_out)
    exercised: set[str] = set()
    if neg_list is not None:
        seen_ids: set[str] = set()
        for i, vector in enumerate(neg_list):
            local: list[tuple[str, str]] = []
            obj = _exact_object(vector, {"id", "why", "violates", "baseVectorId", "mutation"}, set(), f"$contract.adversarialNegatives[{i}]", local)
            findings.extend(f"{inv}: {msg}" for inv, msg in local)
            if obj is None:
                continue
            vid, named = obj.get("id", f"negative[{i}]"), obj.get("violates")
            if not isinstance(vid, str) or vid in seen_ids:
                findings.append(f"EP-11: adversarial vector id {vid!r} is missing/duplicate")
            elif isinstance(vid, str):
                seen_ids.add(vid)
            if named not in declared:
                findings.append(f"{vid}: names undeclared invariant {named!r}")
                continue
            exercised.add(named)
            try:
                negative_bundle, fixed_authority = _materialize_negative(positive_vectors, obj)
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                findings.append(f"{vid}: cannot materialize retained mutation ({exc})")
                continue
            hits = validate_bundle(negative_bundle, fixed_authority)
            hit_ids = {x for x, _ in hits}
            if named not in hit_ids:
                findings.append(f"{vid}: NOT rejected by named invariant {named}; fired {sorted(hit_ids) or 'nothing'}")
    for missing in sorted(expected_invariants - exercised):
        findings.append(f"{missing}: no retained adversarial negative exercises the invariant")

    goldens = contract.get("crossLanguageGoldens")
    golden_out: list[tuple[str, str]] = []
    golden_list = _list(goldens, "$contract.crossLanguageGoldens", golden_out)
    findings.extend(f"{inv}: {msg}" for inv, msg in golden_out)
    if golden_list is not None:
        for i, golden in enumerate(golden_list):
            local: list[tuple[str, str]] = []
            obj = _exact_object(golden, {"id", "kind", "components", "encodedHex", "domain", "commitment"}, set(), f"$contract.crossLanguageGoldens[{i}]", local, "EP-8")
            findings.extend(f"{inv}: {msg}" for inv, msg in local)
            if obj is None or not isinstance(obj.get("components"), list):
                continue
            try:
                if obj.get("kind") == "member" and len(obj["components"]) == 2:
                    encoded = encode_member(*obj["components"])
                elif obj.get("kind") == "outcome" and len(obj["components"]) == 3:
                    encoded = encode_outcome(*obj["components"])
                elif obj.get("kind") == "subject" and len(obj["components"]) == 1:
                    encoded = encode_subject(obj["components"][0])
                else:
                    findings.append(f"EP-8: cross-language golden {obj.get('id')!r} has unknown kind/arity")
                    continue
                if obj.get("encodedHex") != encoded.hex():
                    findings.append(f"EP-8: cross-language golden {obj.get('id')!r} encoded bytes disagree")
                if obj.get("commitment") != commit(obj.get("domain"), [encoded]):
                    findings.append(f"EP-8: cross-language golden {obj.get('id')!r} digest disagrees")
            except (TypeError, ValueError) as exc:
                findings.append(f"EP-8: cross-language golden {obj.get('id')!r} cannot encode: {exc}")

    controls = contract.get("collisionControls")
    control_out: list[tuple[str, str]] = []
    control_list = _list(controls, "$contract.collisionControls", control_out)
    findings.extend(f"{inv}: {msg}" for inv, msg in control_out)
    if control_list is not None:
        kinds_seen: set[str] = set()
        for i, control in enumerate(control_list):
            local: list[tuple[str, str]] = []
            obj = _exact_object(control, {"id", "kind", "logicalA", "logicalB", "encodedHexA", "encodedHexB", "commitmentA", "commitmentB", "persistedGrammarAccepts"}, set(), f"$contract.collisionControls[{i}]", local, "EP-8")
            findings.extend(f"{inv}: {msg}" for inv, msg in local)
            if obj is None:
                continue
            try:
                kind = obj.get("kind")
                kinds_seen.add(kind)
                if kind == "member":
                    a, b = encode_member(*obj["logicalA"]), encode_member(*obj["logicalB"])
                    domain = "universe"
                elif kind == "outcome":
                    a, b = encode_outcome(*obj["logicalA"]), encode_outcome(*obj["logicalB"])
                    domain = "outcome-set"
                else:
                    findings.append(f"EP-8: collision control {obj.get('id')!r} has unknown kind")
                    continue
                if a == b or commit(domain, [a]) == commit(domain, [b]):
                    findings.append(f"EP-8: collision control {obj.get('id')!r} still aliases")
                if (obj.get("encodedHexA"), obj.get("encodedHexB")) != (a.hex(), b.hex()):
                    findings.append(f"EP-8: collision control {obj.get('id')!r} byte golden drift")
                if (obj.get("commitmentA"), obj.get("commitmentB")) != (commit(domain, [a]), commit(domain, [b])):
                    findings.append(f"EP-8: collision control {obj.get('id')!r} commitment golden drift")
                if obj.get("persistedGrammarAccepts") is not False:
                    findings.append(f"EP-8: collision control {obj.get('id')!r} must also be rejected by persisted identifier grammar")
            except (KeyError, TypeError, ValueError) as exc:
                findings.append(f"EP-8: collision control {obj.get('id')!r} malformed: {exc}")
        if kinds_seen != {"member", "outcome"}:
            findings.append("EP-8: both member and outcome collision controls are required")

    assurance = contract.get("assurance")
    assurance_out: list[tuple[str, str]] = []
    assurance_obj = _exact_object(assurance, {"state", "evidenceGrade", "independentRereview", "runtimeDemonstrated", "why"}, set(), "$contract.assurance", assurance_out)
    findings.extend(f"{inv}: {msg}" for inv, msg in assurance_out)
    if assurance_obj is not None:
        if assurance_obj.get("state") != "SPECIFIED" or assurance_obj.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED":
            findings.append("assurance: must remain SPECIFIED / IMPLEMENTABLE_UNEXECUTED")
        if assurance_obj.get("independentRereview") != "REQUIRED":
            findings.append("assurance: independent rereview must remain REQUIRED")
        if assurance_obj.get("runtimeDemonstrated") is not False:
            findings.append("assurance: this checker cannot claim runtime demonstration")

    return findings


def check(value: Any) -> list[str]:
    """Total contract checker: every parsed JSON value returns finite findings."""
    try:
        return _check_impl(value)
    except Exception as exc:
        return [f"EP-TOTALITY: controlled contract validation failure {type(exc).__name__}: {exc}"]


def _find_positive(contract: dict[str, Any], vector_id: str) -> dict[str, Any]:
    return next(v for v in contract["positiveVectors"] if v["id"] == vector_id)["bundle"]


def _find_positive_vector(contract: dict[str, Any], vector_id: str) -> dict[str, Any]:
    return next(v for v in contract["positiveVectors"] if v["id"] == vector_id)


def _mutate_match_to_pass(contract: dict[str, Any]) -> bool:
    _find_positive(contract, "EP5-POS-RELATIONSHIP-FAIL")["verdictProof"]["verdict"] = "pass"
    return True


def _mutate_unknown_union(contract: dict[str, Any]) -> bool:
    evaluation = _find_positive(contract, "EP5-POS-NOMATCH-PASS")["evaluations"][0]
    evaluation.update({"outcome": "partial-but-clean", "claimShape": "future-shape", "proof": {}})
    return True


def _mutate_omit_member_ids(contract: dict[str, Any]) -> bool:
    del _find_positive(contract, "EP5-POS-NOMATCH-PASS")["requiredUniverse"]["memberIds"]
    return True


def _mutate_policy_and_verdict(contract: dict[str, Any]) -> bool:
    bundle = _find_positive(contract, "EP5-POS-RELATIONSHIP-FAIL")
    bundle["verdictProof"]["policy"]["matchDisposition"] = "always-pass"
    bundle["verdictProof"]["verdict"] = "pass"
    return True


def _mutate_extra_proof_field(contract: dict[str, Any]) -> bool:
    _find_positive(contract, "EP5-POS-NOMATCH-PASS")["evaluations"][0]["proof"]["trusted"] = True
    return True


def _mutate_unknown_verdict(contract: dict[str, Any]) -> bool:
    _find_positive(contract, "EP5-POS-NOMATCH-PASS")["verdictProof"]["verdict"] = "green"
    return True


def _mutate_bad_reference(contract: dict[str, Any]) -> bool:
    _find_positive(contract, "EP5-POS-NOMATCH-PASS")["evaluations"][0]["predicateSemanticsRef"] = "sha256:" + "f" * 64
    return True


def _mutate_assurance(contract: dict[str, Any]) -> bool:
    contract["assurance"]["state"] = "DEMONSTRATED"
    return True


def _mutate_dependency_cycle(contract: dict[str, Any]) -> bool:
    bundle = _find_positive(contract, "EP5-POS-NOMATCH-PASS")
    fact = next(obj for obj in bundle["objectStore"] if obj["ref"] == "sha256:" + "f0" * 32)
    anchor = next(obj for obj in bundle["objectStore"] if obj["ref"] == "sha256:" + "93" * 32)
    anchor["dependencies"].append({"ref": fact["ref"], "projectId": bundle["projectId"], "role": "fact-anchor"})
    return True


def _mutate_dependency_role(contract: dict[str, Any]) -> bool:
    bundle = _find_positive(contract, "EP5-POS-NOMATCH-PASS")
    next(obj for obj in bundle["objectStore"] if obj["dependencies"])["dependencies"][0]["role"] = "future-role"
    return True


def _mutate_wire_grammar(contract: dict[str, Any]) -> bool:
    contract["wireGrammars"]["evaluationId"]["controlCharacters"] = "ALLOWED"
    return True


def _mutate_whole_universe(contract: dict[str, Any]) -> bool:
    vector = _find_positive_vector(contract, "EP5-POS-NOMATCH-PASS")
    materialized, _ = _materialize_negative(
        {vector["id"]: {"bundle": vector["bundle"], "verifiedAuthorityInput": vector["verifiedAuthorityInput"]}},
        {"baseVectorId": vector["id"], "mutation": {"kind": "whole-universe-substitution"}},
    )
    vector["bundle"] = materialized
    return True


def _mutate_inverse_precedence(contract: dict[str, Any]) -> bool:
    vector = _find_positive_vector(contract, "EP5-POS-BASELINE-WAIVER-PASS")
    materialized, _ = _materialize_negative(
        {vector["id"]: {"bundle": vector["bundle"], "verifiedAuthorityInput": vector["verifiedAuthorityInput"]}},
        {"baseVectorId": vector["id"], "mutation": {"kind": "inverse-baseline-waiver-order"}},
    )
    vector["bundle"] = materialized
    return True


def _mutate_manifest_ref(contract: dict[str, Any]) -> bool:
    _find_positive_vector(contract, "EP5-POS-NOMATCH-PASS")["verifiedAuthorityInput"]["evaluationAuthoritySeal"]["activationManifestRef"] = "sha256:" + "0" * 64
    return True


def _mutate_c2_commitment(contract: dict[str, Any]) -> bool:
    contract["c2AuthorityJoin"]["expectedPlanIntentCommitment"] = "sha256:" + "0" * 64
    return True


def _authority_vector(contract: dict[str, Any]) -> dict[str, Any]:
    return _find_positive_vector(contract, "EP5-POS-NOMATCH-PASS")


def _mutate_raw_authority(contract: dict[str, Any]) -> bool:
    vector = _authority_vector(contract)
    vector["verifiedAuthorityInput"] = vector["verifiedAuthorityInput"]["evaluationAuthoritySeal"]
    return True


def _mutate_bundle_local_authority(contract: dict[str, Any]) -> bool:
    vector = _authority_vector(contract)
    vector["bundle"]["authority"] = vector.pop("verifiedAuthorityInput")
    return True


def _mutate_boolean_authority(contract: dict[str, Any]) -> bool:
    _authority_vector(contract)["verifiedAuthorityInput"] = {"verified": True}
    return True


def _mutate_plan_owner(contract: dict[str, Any]) -> bool:
    _authority_vector(contract)["verifiedAuthorityInput"]["planIdAdmission"]["verificationOwner"] = "caller"
    return True


def _mutate_store_owner(contract: dict[str, Any]) -> bool:
    _authority_vector(contract)["verifiedAuthorityInput"]["authoritySealAdmission"]["verificationOwner"] = "producer"
    return True


def _mutate_store_project(contract: dict[str, Any]) -> bool:
    _authority_vector(contract)["verifiedAuthorityInput"]["authoritySealAdmission"]["projectId"] = "prj1-" + "b" * 64
    return True


def _mutate_store_manifest_join(contract: dict[str, Any]) -> bool:
    _authority_vector(contract)["verifiedAuthorityInput"]["authoritySealAdmission"]["sealedActivationManifestRef"] = "sha256:" + "0" * 64
    return True


def _mutate_plan_id_join(contract: dict[str, Any]) -> bool:
    _authority_vector(contract)["verifiedAuthorityInput"]["planIdAdmission"]["verifiedPlanId"] = "plan1:sha256:" + "0" * 64
    return True


def _mutate_terminal_bundle_field(contract: dict[str, Any]) -> bool:
    _authority_vector(contract)["bundle"]["runId"] = "run1:" + "0" * 64
    return True


SEMANTIC_MUTATIONS: list[tuple[str, Callable[[dict[str, Any]], bool]]] = [
    ("R8-P1A-P02 match relabeled pass", _mutate_match_to_pass),
    ("R8-P1A-P03 unknown outcome/shape/proof", _mutate_unknown_union),
    ("R8-P1A-P04 requiredUniverse.memberIds omitted", _mutate_omit_member_ids),
    ("arbitrary policy and verdict coordinated", _mutate_policy_and_verdict),
    ("proof tagged union gains unknown field", _mutate_extra_proof_field),
    ("unknown verdict enum", _mutate_unknown_verdict),
    ("unresolvable predicate identity", _mutate_bad_reference),
    ("transitive dependency cycle", _mutate_dependency_cycle),
    ("unknown transitive dependency role", _mutate_dependency_role),
    ("declared identifier grammar drifts from executable grammar", _mutate_wire_grammar),
    ("R8-P1A-RR-01 coordinated whole-universe substitution under fixed authority", _mutate_whole_universe),
    ("R8-P1A-RR-01 manifest digest substitution", _mutate_manifest_ref),
    ("R8-P1A-RR-01 C2 PlanIntent/ExecutionPlan commitment substitution", _mutate_c2_commitment),
    ("RR13-01 raw EvaluationAuthoritySealV1 is not admitted", _mutate_raw_authority),
    ("RR13-01 bundle-local authority is not admitted", _mutate_bundle_local_authority),
    ("RR13-01 boolean verified assertion is not admitted", _mutate_boolean_authority),
    ("RR13-01 wrong opensip-plan owner", _mutate_plan_owner),
    ("RR13-01 wrong opensip-store owner", _mutate_store_owner),
    ("RR13-01 cross-ProjectId store admission", _mutate_store_project),
    ("RR13-01 sealed manifest admission mismatch", _mutate_store_manifest_join),
    ("RR13-01 PlanId admission mismatch", _mutate_plan_id_join),
    ("A-prime terminal RunId in semantic bundle", _mutate_terminal_bundle_field),
    ("R8-P1A-RR-02 inverse baseline-before-waiver precedence", _mutate_inverse_precedence),
    ("design checker claims DEMONSTRATED", _mutate_assurance),
]


HOSTILE_VALUES: list[Any] = [None, True, 7, "scalar", [None], {}]


def _declarative_mutation_cases(contract: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Mutate every declared tag/order/field and every published golden component."""
    cases: list[tuple[str, dict[str, Any]]] = []

    def add(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        value = copy.deepcopy(contract)
        mutate(value)
        cases.append((name, value))

    records = contract["normativePreimageGrammar"]["records"]
    for ri, record in enumerate(records):
        rname = record["name"]
        add(f"grammar record tag {rname}", lambda c, ri=ri: c["normativePreimageGrammar"]["records"][ri].__setitem__("recordTag", "0x7f"))
        add(f"grammar record order {rname}", lambda c, ri=ri: c["normativePreimageGrammar"]["records"][ri].__setitem__("order", list(reversed(c["normativePreimageGrammar"]["records"][ri]["order"])) if len(c["normativePreimageGrammar"]["records"][ri]["order"]) > 1 else []))
        for fi, field in enumerate(record["fields"]):
            fname = field["name"]
            add(f"grammar field tag {rname}.{fname}", lambda c, ri=ri, fi=fi: c["normativePreimageGrammar"]["records"][ri]["fields"][fi].__setitem__("tag", "0x7f"))
            add(f"grammar field omission {rname}.{fname}", lambda c, ri=ri, fi=fi: c["normativePreimageGrammar"]["records"][ri]["fields"].pop(fi))
    scalar_keys = list(contract["normativePreimageGrammar"]["scalarEncoding"])
    for key in scalar_keys:
        add(f"grammar scalar encoding {key}", lambda c, key=key: c["normativePreimageGrammar"]["scalarEncoding"].__setitem__(key, "DRIFT"))
    rule_keys = list(contract["normativePreimageGrammar"]["recordRules"])
    for key in rule_keys:
        add(f"grammar ordering/duplicate rule {key}", lambda c, key=key: c["normativePreimageGrammar"]["recordRules"].__setitem__(key, "DRIFT"))
    for section, key in [("leaf", "tag"), ("internal", "tag"), ("empty", "tag"), ("empty", "namespaceBlobTag")]:
        add(f"grammar commitment tag {section}.{key}", lambda c, section=section, key=key: c["normativePreimageGrammar"]["commitment"][section].__setitem__(key, "0x7f"))
    for key in ("recordTag", "namespaceTag", "domainTag", "merkleRootTag"):
        add(f"grammar commitment tag outer.{key}", lambda c, key=key: c["normativePreimageGrammar"]["commitment"]["outer"].__setitem__(key, "0x7f"))
    add("grammar commitment sorting/dedup rule", lambda c: c["normativePreimageGrammar"]["commitment"].__setitem__("itemSetRule", "PRESERVE INPUT ORDER"))
    for i, domain in enumerate(contract["normativePreimageGrammar"]["domains"]):
        add(f"grammar domain omission {domain}", lambda c, i=i: c["normativePreimageGrammar"]["domains"].pop(i))
    add("grammar pinned sha assertion", lambda c: c.__setitem__("normativePreimageGrammarSha256", "0" * 64))

    forbidden = contract["activationAuthority"]["forbiddenInAuthoritySeal"]
    for field in forbidden:
        add(f"authority seal forbidden field {field}", lambda c, field=field: c["positiveVectors"][0]["verifiedAuthorityInput"]["evaluationAuthoritySeal"].__setitem__(field, True))
    for field in contract["activationAuthority"]["forbiddenInSemanticProof"]:
        add(f"semantic bundle forbidden terminal field {field}", lambda c, field=field: c["positiveVectors"][0]["bundle"].__setitem__(field, True))

    for i, row in enumerate(contract["preimageGoldens"]["records"]):
        for key in ("encodedHex", "recordSha256"):
            add(f"record golden {row['id']}.{key}", lambda c, i=i, key=key: c["preimageGoldens"]["records"][i].__setitem__(key, "00"))
        add(f"record golden omission {row['id']}", lambda c, i=i: c["preimageGoldens"]["records"].pop(i))
    for i, row in enumerate(contract["preimageGoldens"]["commitments"]):
        for key in ("itemEncodedHex", "sortedUniqueItemHex", "leafHashHex", "merkleRootHex", "outerPreimageHex", "commitment"):
            def mutate(c: dict[str, Any], i: int = i, key: str = key) -> None:
                target = c["preimageGoldens"]["commitments"][i]
                target[key] = ["00"] if isinstance(target[key], list) else "00"
            add(f"commitment golden {row['id']}.{key}", mutate)
        add(f"commitment golden omission {row['id']}", lambda c, i=i: c["preimageGoldens"]["commitments"].pop(i))
    return cases


def _hostile_cases(contract: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    cases: list[tuple[str, dict[str, Any]]] = []
    setters: list[tuple[str, Callable[[dict[str, Any], Any], None]]] = [
        ("root", lambda c, v: None),
        ("grammar", lambda c, v: c.__setitem__("canonicalCommitmentGrammar", v)),
        ("schemas", lambda c, v: c.__setitem__("persistedSchemaRegistry", v)),
        ("positive-vector", lambda c, v: c["positiveVectors"].__setitem__(0, v)),
        ("verified-authority-input", lambda c, v: c["positiveVectors"][0].__setitem__("verifiedAuthorityInput", v)),
        ("plan-admission", lambda c, v: c["positiveVectors"][0]["verifiedAuthorityInput"].__setitem__("planIdAdmission", v)),
        ("authority-seal-admission", lambda c, v: c["positiveVectors"][0]["verifiedAuthorityInput"].__setitem__("authoritySealAdmission", v)),
        ("evaluation-authority-seal", lambda c, v: c["positiveVectors"][0]["verifiedAuthorityInput"].__setitem__("evaluationAuthoritySeal", v)),
        ("activation-manifest", lambda c, v: c["positiveVectors"][0]["verifiedAuthorityInput"].__setitem__("activationManifest", v)),
        ("activation-member", lambda c, v: c["positiveVectors"][0]["verifiedAuthorityInput"]["activationManifest"]["members"].__setitem__(0, v)),
        ("bundle", lambda c, v: c["positiveVectors"][0].__setitem__("bundle", v)),
        ("object-store", lambda c, v: c["positiveVectors"][0]["bundle"].__setitem__("objectStore", v)),
        ("object-record", lambda c, v: c["positiveVectors"][0]["bundle"]["objectStore"].__setitem__(0, v)),
        ("partition-record", lambda c, v: c["positiveVectors"][0]["bundle"]["partitionContents"].__setitem__(0, v)),
        ("required-universe", lambda c, v: c["positiveVectors"][0]["bundle"].__setitem__("requiredUniverse", v)),
        ("member-record", lambda c, v: c["positiveVectors"][0]["bundle"]["requiredUniverse"]["memberIds"].__setitem__(0, v)),
        ("evaluation", lambda c, v: c["positiveVectors"][0]["bundle"]["evaluations"].__setitem__(0, v)),
        ("proof", lambda c, v: c["positiveVectors"][0]["bundle"]["evaluations"][0].__setitem__("proof", v)),
        ("verdict-proof", lambda c, v: c["positiveVectors"][0]["bundle"].__setitem__("verdictProof", v)),
        ("coverage", lambda c, v: c["positiveVectors"][0]["bundle"]["verdictProof"].__setitem__("coverage", v)),
        ("baseline", lambda c, v: c["positiveVectors"][0]["bundle"]["verdictProof"].__setitem__("baseline", v)),
        ("waivers", lambda c, v: c["positiveVectors"][0]["bundle"]["verdictProof"].__setitem__("waivers", v)),
        ("policy", lambda c, v: c["positiveVectors"][0]["bundle"]["verdictProof"].__setitem__("policy", v)),
        ("assurance", lambda c, v: c.__setitem__("assurance", v)),
        ("c2-authority-join", lambda c, v: c.__setitem__("c2AuthorityJoin", v)),
    ]
    for name, setter in setters:
        for value in HOSTILE_VALUES:
            if name == "root":
                cases.append((f"{name}={type(value).__name__}", value))
                continue
            mutated = copy.deepcopy(contract)
            try:
                setter(mutated, copy.deepcopy(value))
            except (KeyError, IndexError, TypeError):
                # A base-shape failure is itself caught by the clean-base guard.
                continue
            cases.append((f"{name}={type(value).__name__}", mutated))
    return cases


def selftest(contract: Any) -> int:
    base = check(contract)
    if base:
        print(f"REFUSING to self-test: base contract has {len(base)} finding(s); mutations would be masked.")
        for finding in base[:12]:
            print("  -", finding)
        return 1
    assert isinstance(contract, dict)
    failures: list[str] = []
    total = 0
    for name, mutate in SEMANTIC_MUTATIONS:
        total += 1
        mutated = copy.deepcopy(contract)
        before = copy.deepcopy(mutated)
        applied = False
        try:
            applied = mutate(mutated)
        except Exception as exc:
            failures.append(f"{name}: mutation raised {type(exc).__name__}: {exc}")
            continue
        if not applied or mutated == before:
            failures.append(f"{name}: mutation did not apply (escape)")
            continue
        if not check(mutated):
            failures.append(f"{name}: mutation survived")

    for name, mutated in _declarative_mutation_cases(contract):
        total += 1
        if mutated == contract:
            failures.append(f"{name}: mutation did not apply (escape)")
            continue
        try:
            result = check(mutated)
        except Exception as exc:
            failures.append(f"{name}: traceback escape {type(exc).__name__}: {exc}")
            continue
        if not result:
            failures.append(f"{name}: declarative mutation survived")

    hostile = _hostile_cases(contract)
    for name, value in hostile:
        total += 1
        try:
            result = check(value)
        except Exception as exc:  # this is precisely what totality forbids
            failures.append(f"{name}: traceback escape {type(exc).__name__}: {exc}")
            continue
        if not result:
            failures.append(f"{name}: hostile value was accepted")

    if failures:
        print(f"{len(failures)}/{total} evaluation-proof self-test cases escaped")
        for failure in failures:
            print("  -", failure)
        return 1
    print(f"PASS: {total} evaluation-proof mutations/hostile parsed-value cases rejected; base-dirty and non-applying-mutation guards active")
    return 0


def _load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(), object_pairs_hook=_pairs_no_duplicates)


def main() -> int:
    args = [arg for arg in sys.argv[1:] if arg != "--selftest"]
    path = pathlib.Path(args[0]) if args else HERE / BINDING
    try:
        contract = _load(path)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"cannot load {path}: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if "--selftest" in sys.argv:
        return selftest(contract)
    findings = check(contract)
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1
    assert isinstance(contract, dict)
    print(f"PASS: {path.name}; {len(contract['positiveVectors'])} fixed-authority positives; {len(contract['adversarialNegatives'])} named negatives; {len(contract['preimageGoldens']['records'])} record + {len(contract['preimageGoldens']['commitments'])} commitment preimage goldens; {len(contract['crossLanguageGoldens'])} retained cross-language goldens; EP-1..EP-13 clean")
    print("  pre-evaluation EvaluationAuthoritySealV1 validated; no RunId/runSealRef is admitted into semantic evaluation bytes")
    print("  assurance SPECIFIED / IMPLEMENTABLE_UNEXECUTED; independent combined-packet rereview REQUIRED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
