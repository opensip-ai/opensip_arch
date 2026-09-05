#!/usr/bin/env python3
"""Evidence v8 foundation checker.

This candidate intentionally remains RED until accepted D9/retention and
TrustedRequestContext leaf joins plus remaining changed-root contract binding
are implemented.  The executable
foundation below proves closed final records, project-wide integrity
enumeration, a complete snapshot/CAS guard, the shared-R4/attempt-A2 recovery
state machine, and the pinned RT13 serialized-custody reducer join.
It is an architecture test double, not production durability evidence.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
import pathlib
import re
import sys
from typing import Any, Callable


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "evidence.v8.json"
PINS = {
    "evidence.v7.json": "157da8cf2b44fd72794ee2c7c3dedfa30745164798c45a8d21e08094a128c356",
    "check-evidence-v7.py": "9fd858b1c59f064dd9693ba3c6d2d935fc462f0833078cc2eb5bc26cc4009524",
    "evidence.v7.review-adversarial-prefreeze-rejected.json":
        "5a98de124ffd0ab1b47e148d13b5f8e9dbab549fb8e62e02b37a8066ba09ab2d",
    "evaluation-proof.v8.json": "4bb33f772c8c510c470643082f6bfb8a4df28a050b4720dda6cdd5187bd3e303",
    "check-evaluation-proof-v8.py": "c80ac50e21dcd350e5f5285958a6cfb94d52c5c3f7d64f2396d91b544fa82769",
    "retention-tiers.v13.json": "3f79668a6d26b5ecc7fd843be71aef90e779ac024a1ac54bb5cc2c8fc3e0a349",
    "check-retention-custody-v13.py": "0290b4ae22816843c2fbce1288ea36f21e78b396361fa6c0bf5291338be519f6",
    "check-retention-custody.py": "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    "versioning-policy.v8.json": "ea4b52b5a4d187ec35ad994d8ffcd888db287566c8fb53f3df17e5203d84ae2e",
    "check-versioning-v8.py": "82834720a8fd4ec8701dad2b43ad94d6ad9e52d21aeb077f4286fab5fb156844",
}

FINAL_TYPES = (
    "TerminalRunV1", "RunIndexV1", "AttemptRunLinkV1",
    "RunCustodyRootV1", "RunAuthorityIndexV1", "RunCommitNotificationV1",
)
SHARED_R4 = (
    "TerminalRunV1", "RunIndexV1", "RunCustodyRootV1",
    "RunAuthorityIndexV1",
)
ATTEMPT_A2 = ("AttemptRunLinkV1", "RunCommitNotificationV1")
FINAL_FIELDS = {
    "TerminalRunV1": (
        "schemaVersion", "projectId", "runId", "runSealRef",
        "recordBytesHex"),
    "RunIndexV1": ("schemaVersion", "projectId", "runId", "runSealRef"),
    "AttemptRunLinkV1": (
        "schemaVersion", "projectId", "executionId", "disposition",
        "runId", "runSealRef"),
    "RunCustodyRootV1": (
        "schemaVersion", "projectId", "runId", "runSealRef",
        "semanticEvidenceCasRef", "unitIds"),
    "RunAuthorityIndexV1": (
        "schemaVersion", "projectId", "runId", "runSealRef",
        "planAuthorityReceiptRef", "evaluationAuthorityAdmissionRef", "planId",
        "planIntentCommitment", "executionPlanCommitment",
        "activationManifestRef", "evaluationAuthoritySealRef"),
    "RunCommitNotificationV1": (
        "schemaVersion", "projectId", "notificationKind",
        "committerRequestId", "executionId", "runId", "runSealRef"),
}
CONTENT_FIELDS = {
    "schemaVersion", "projectId", "authorityFixture", "privateCas",
    "attempts", "journals", "rtState", "finalRecords", "terminalFacts",
}
AUTHORITY_FIXTURE_FIELDS = {
    "schemaVersion", "projectId", "evaluationAuthoritySealRef",
    "evaluationAuthorityIndexCasRef", "evaluationAuthorityAdmissionCasRef",
    "evaluationProofBundleCasRef", "semanticCapabilityClosureCasRef",
    "rawProofInventoryCasRef", "semanticEvidenceCasRef",
    "frozenRetentionTargetRef",
}
PRIVATE_CAS_FIELDS = {
    "schemaVersion", "projectId", "recordCasRef", "recordKind",
    "recordBytesHex",
}
ATTEMPT_FIELDS = {
    "schemaVersion", "projectId", "executionId", "revision",
    "frozenAttemptCasRef", "evaluationAuthoritySealRef",
    "evaluationAuthorityAdmissionCasRef", "frozenRetentionTargetRef",
    "semanticEvidenceCasRef",
}
JOURNAL_FIELDS = {
    "schemaVersion", "projectId", "executionId", "expectedAttemptRevision",
    "frozenAttemptCasRef", "evaluationAuthoritySealRef",
    "evaluationAuthorityAdmissionCasRef", "semanticEvidenceCasRef",
    "frozenRetentionTargetRef", "rawProofInventoryCasRef",
    "custodyPreparationRef", "custodyState", "leaseId", "ownerId",
    "ownerLivenessToken", "fencingToken", "pinnedRefs", "custodyRevision",
}
TERMINAL_FACT_TYPES = (
    "AttemptTerminalDispositionV1", "CustodyLossProofV1",
)
TERMINAL_FACT_FIELDS = {
    "AttemptTerminalDispositionV1": {
        "schemaVersion", "projectId", "executionId", "disposition",
        "custodyLossProofRef",
    },
    "CustodyLossProofV1": {
        "schemaVersion", "projectId", "executionId", "cause",
        "frozenAttemptCasRef", "custodyPreparationRef",
        "observedAtSequence", "requiredObjectStates",
    },
}
PROJECT_RE = re.compile(r"^prj1-[0-9a-f]{64}$")
RUN_RE = re.compile(r"^run1:[0-9a-f]{64}$")
PLAN_RE = re.compile(r"^plan1:sha256:[0-9a-f]{64}$")
REF_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
EXEC_RE = re.compile(r"^exec1-[a-z0-9-]+$")
REQUEST_RE = re.compile(r"^req1_[0-9a-f]{32}$")
UNIT_RE = re.compile(r"^unit3:sha256:[0-9a-f]{64}$")
LEASE_RE = re.compile(r"^lease1:[0-9a-f]{32}$")
OWNER_RE = re.compile(r"^owner1:[0-9a-f]{32}$")
LIVENESS_RE = re.compile(r"^live1:[0-9a-f]{32}$")
TOKEN_KEYS = {
    "storeInstanceToken", "transactionToken", "continuityToken",
    "preparedCustodyToken", "finalizedEvidenceToken", "candidateCache",
}
UNIT_IDS = [
    "unit3:sha256:5c6c613a74f68e39a5052a06274fa612888a63c327f0a1c8ae03c86ede1b9adc",
    "unit3:sha256:22311dbe7dd9fd958d1946e6795a2add39298a41fa6eb82f918ee61c312054ed",
]
PROTECTED = (
    "canonicalWireGrammar", "acceptedGolden", "runSubstitutionGoldens",
    "d9Mapping",
)
CHANGED_ROOT_KEYS = {
    "version", "role", "supersedes", "reviewFindingTransfers",
    "recursiveRequestIdExclusion", "dependencies", "importedAuthorityContract",
    "semanticJoins", "persistedVsProjection",
    "apiContract", "storeContract", "admissionAndSealOrdering",
    "sealedCapabilityContract",
    "runAuthorityIndexContract", "correlationDifferential",
    "availabilityDifferential", "storeCapabilityContinuityContract",
    "invariants", "durableRecoveryContract", "recoveryMatrixContract",
}
ADDED_ROOT_KEYS = {"successorDelta", "foundationImplementation"}
TODO_FINDINGS = (
    "E8-TODO-D9-RETENTION-SUCCESSOR: no independently accepted D9/retention successor is available for mechanical termination derivation",
    "E8-TODO-REQUEST-CONTEXT-LEAF: TrustedRequestContextV1 construction authority is not yet pinned to an independently accepted leaf contract",
    "E8-TODO-CONTRACT-BINDING: remaining changed-root semantics are not yet mutation-completely bound",
)
TODO_DECLARATIONS = [
    "E8-TODO-D9-RETENTION-SUCCESSOR: after independent acceptance, pin the D9/retention successors and derive termination without authored class/code/exit literals.",
    "E8-TODO-REQUEST-CONTEXT-LEAF: pin the independently accepted TrustedRequestContextV1 construction contract; E8 currently uses only an opaque test fixture capability.",
    "E8-TODO-CONTRACT-BINDING: bind the remaining changed-root semantics and prove mutation-complete successor enforcement before any seal.",
]
SUCCESSOR_PREDECESSOR = (
    "evidence.v7.json@157da8cf2b44fd72794ee2c7c3dedfa30745164798c45a8d21e08094a128c356")
SUCCESSOR_REJECTION = (
    "evidence.v7.review-adversarial-prefreeze-rejected.json@"
    "5a98de124ffd0ab1b47e148d13b5f8e9dbab549fb8e62e02b37a8066ba09ab2d")
SUCCESSOR_SCOPE = (
    "The checker compares every unlisted predecessor root value for exact equality "
    "and rejects additions outside addedRootKeys. Text-substring sampling is not a "
    "successor oracle.")
PROJECT_STATE_CONTRACT = {
    "schema": "DurableProjectContentV2",
    "guard": "ProjectSnapshotGuardV1 = (projectRevision, sha256(canonical full token-free content))",
    "begin": "Validate the complete current project, copy the complete content, and capture the guard in one serializable read.",
    "commit": "Compare both revision and canonical full-content digest, validate the complete candidate project, then atomically swap content and increment revision exactly once.",
    "staleResult": "LEDGER.BUSY_TIMEOUT; a retry audits changed state before any derivation or write",
}
INTEGRITY_CONTRACT = {
    "sharedR4": list(SHARED_R4),
    "attemptA2": list(ATTEMPT_A2),
    "rule": "Enumerate every row of all six project-wide containers before target lookup. Every Run group has exactly one closed shared R4 and at least one complete A2; every ExecutionId in either A2 container has exactly both peers; no journal coexists with its A2. Any orphan, duplicate, wrong-project, malformed, partial, or conflicting row is LEDGER.CORRUPT and state remains byte-for-byte unchanged.",
    "noSeventhFinalRecord": True,
}
TRANSITION_TABLE = [
    {"sharedR4": "EMPTY", "attemptA2": "EMPTY", "journal": "EXACT",
     "action": "NEW: insert R4+A2 and consume journal"},
    {"sharedR4": "COMPLETE_EXACT", "attemptA2": "EMPTY", "journal": "EXACT",
     "action": "CONVERGE: reuse R4, insert A2, consume journal"},
    {"sharedR4": "COMPLETE_EXACT", "attemptA2": "COMPLETE_EXACT",
     "journal": "ABSENT", "action": "IDEMPOTENT_SUCCESS"},
    {"sharedR4": "EMPTY_OR_COMPLETE_EXACT", "attemptA2": "EMPTY",
     "journal": "ABSENT", "action": "NO_PREPARED_RUN"},
    {"sharedR4": "EMPTY_OR_COMPLETE_EXACT", "attemptA2": "EMPTY",
     "journal": "ABSENT", "terminalFacts": "EXACT",
     "action": "CUSTODY_LOSS_FACTS"},
    {"sharedR4": "ANY_OTHER", "attemptA2": "ANY_OTHER",
     "journal": "ANY_OTHER", "action": "LEDGER.CORRUPT_UNCHANGED"},
]
FOCUSED_PROBES = [
    "closed-final-schema cross-project and unknown-field rejection",
    "all 64 final-record masks with journal absent and exact (128 classified states)",
    "unrelated no-journal orphan blocks NoPreparedRun",
    "same Run second Attempt adds only its A2 pair",
    "Attempt and journal post-snapshot TOCTOU causes stale-CAS refusal and preserves concurrent bytes",
    "mechanical RT13 serialized custody: 23-object acquire/retry/release, pending expiry, purge, crash-gap repin, contention, response loss, and wrong-binding negatives",
    "closed same-project RT inventory superset with exact 23-key pin subset and authority-neutral extras",
    "typed private CAS missing/duplicate/hash/kind/project/canonical/coherent-substitution rejection",
    "delayed reducer-derived reclaim, immutable-only repin patch, stale-CAS retry audit and FACTS-only custody loss",
    "RunCommitNotification concurrent winner, changed-RequestId replay and raw-context rejection",
]
SERIALIZED_CUSTODY_CONTRACT = {
    "authority": "Import pinned retention-tiers.v13.json, check-retention-custody-v13.py and check-retention-custody.py; cold-regenerate RT13 through EP8. Durable LeaseStateV2 objects are a closed, unique, same-project superset; the mechanically derived 23 RawObjectStateV1 keys remain the exact required pin subset and sole source of the two unit IDs, closure commitment and Run custody authority. Extra project objects cannot enter units, pins or Run authority.",
    "states": ["IDLE", "HELD_PREPARED", "HELD_PENDING_EXPIRY",
               "RECLAIMED_PENDING_REPIN", "COMMITTED_RELEASED",
               "ABORTED_RELEASED"],
    "acquisition": "One project snapshot transaction executes RT13 resolve-and-pin over all 23 AVAILABLE keys, writes the matching FrozenAttemptRecordV1 and sole RunFreePreparedCommitV3, and records exact lease/owner/liveness/fence/scope plus custodyRevision=1.",
    "horizon": "expiresAtSequence is exactly acquisition atSequence + 1. Same-owner exact retry returns unchanged state and never extends the horizon; +2, arbitrary sequence and wall-clock substitution are forbidden.",
    "serialization": "At most one custody journal exists project-wide. A different Attempt while HELD_PREPARED or RECLAIMED_PENDING_REPIN changes no byte and waits/retries or reaches LEDGER.BUSY_TIMEOUT; after release it may acquire and converge by adding only its A2.",
    "commit": "The same project transaction reconstructs authority from current RT13 state, requires exact project/lease/owner/liveness/fence/scope, 23 AVAILABLE objects and empty pendingExpiryRefs, establishes or verifies shared R4, adds this Attempt A2, establishes RunCustodyRootV1 lineage, executes RT13 release, and removes only this journal.",
    "pendingExpiry": "Any pendingExpiryRefs after admission forbids Run publication because RT13 release would expire required objects. Preserve the HELD journal and public state unchanged; its D9 lifecycle/code remains explicitly unresolved in E8.",
    "recovery": "An exact host-owned dead-owner observation executes crash-reclaim at the next ledger sequence once that sequence is greater than or equal to expiresAtSequence, including after real intervening unrelated-object or pending-expiry events. The reducer's exact output sets lease=null and journal state RECLAIMED_PENDING_REPIN with custodyRevision+1. That journal gates contenders. A distinct next transaction revalidates every immutable CAS authority byte, then resolve-and-pins the exact required 23-key subset at the next fence and patches only custody fields/revision.",
    "failure": "A failed final transaction changes no durable byte. Response loss after commit leaves complete R4+A2, RELEASED lease and no journal; retry verifies and returns the byte-identical committed result.",
    "mutableEvents": "Intersecting purge while HELD is rejected by the RT13 reducer; intersecting expiry becomes pending and blocks commit; after release purge/expiry may alter current availability without changing persisted Run identity.",
    "residuals": ["SERIALIZED-CUSTODY-THROUGHPUT", "SERIALIZED-CUSTODY-FAIRNESS",
                  "OWNER-LIVENESS-AUTHORITY", "LEASE-RECOVERY-LATENCY",
                  "PRODUCTION-ATOMICITY", "CD-RT-5", "G19"],
}

PRIVATE_CAS_CONTRACT = {
    "record": "PrivateCasObjectV1 is exact {schemaVersion,projectId,recordCasRef,recordKind,recordBytesHex}; raw SHA-256, kind and ProjectId are validated over exact bytes before any reference is followed.",
    "fixedAuthority": "Cold-seed and exact-match the EP8 immutable authority CAS/index, canonical EvaluationProofBundleV5, canonical RT13 SemanticCapabilityClosureV3, RawProofInventoryV1 wire bytes, SemanticEvidenceV1 wire bytes and canonical FrozenRetentionTargetV1.",
    "dynamicAuthority": "FrozenAttemptRecordV1, all 23 CustodyPreparedObjectV2 rows and CustodyPreparationMaterialV2 use canonical JSON bytes and closed schemas; referenced missing, duplicate, malformed, noncanonical or coherent-substitution records are LEDGER.CORRUPT.",
    "attemptJoin": "FrozenAttemptRecordV1 binds its exact revision/content CAS plus the EP8 admission, seal, frozen target and SemanticEvidence refs. RunFreePreparedCommitV3 repeats and exactly joins those immutable refs and its expected revision.",
    "custodyJoin": "CustodyPreparationMaterialV2 contains the exact cold-derived units and exactly 23 required row CAS refs. Each row binds one exact unit/minimum/raw object/frozen target; no extra row can enter authority.",
    "writeRule": "Every private CAS, FrozenAttempt and journal write is absent-or-byte-exact. A collision never overwrites durable bytes.",
}

RT_INVENTORY_CONTRACT = {
    "schema": "LeaseStateV2.objects is a closed array of unique RawObjectStateV1 rows, all with the state ProjectId.",
    "requiredSubset": "The cold-derived 23 physical keys must all be present; other valid project objects are allowed but are excluded from pinnedRefs, custody rows, units, RunCustodyRootV1 and all Run identity.",
    "reclaim": "Crash reclaim is reduced at current ledgerSequence+1 whenever that next sequence is >= expiresAtSequence. Real intervening expiry/purge events remain in reducer history; pending required expiry is applied by reclaim and prevents repin/Run publication.",
}

TERMINAL_FACT_CONTRACT = {
    "types": ["AttemptTerminalDispositionV1", "CustodyLossProofV1"],
    "rule": "When required custody is unavailable before Run publication, atomically remove the journal and persist one exact paired disposition/loss proof. The proof enumerates all 23 required object states and binds the frozen Attempt and custody preparation.",
    "exclusions": ["RunId", "runSealRef", "D9 class", "D9 code", "exit code", "RequestId"],
    "authorityBoundary": "These are source FACTS only. A future independently accepted RT/D9 successor derives public termination; E8 authors no class/code/exit literal.",
}

NOTIFICATION_CONTRACT = {
    "record": "RunCommitNotificationV1 is exact {schemaVersion,projectId,notificationKind,committerRequestId,executionId,runId,runSealRef}; notificationKind is run-committed.",
    "key": ["ProjectId", "ExecutionId", "run-committed"],
    "authority": "commit_run_v2/recover_run_v2 accept an opaque TrustedRequestContextV1 plus host-owned ExecutionId, never raw identities. Construction of the trusted request leaf remains an explicit external TODO.",
    "atomicity": "Exactly one notification for this Attempt is one of the six final transaction writes. Concurrent winner owns committerRequestId; a loser/recovery replay with a different current RequestId verifies and preserves the persisted winner row.",
    "delivery": "The durable row supports replayable delivery. E8 claims neither external exactly-once delivery nor EventEnvelopeV3; OP6 alone derives that envelope.",
    "forbidden": ["plane", "phase", "budget", "payload", "capability tokens", "EventEnvelopeV3"],
}

OP6_TRACE_CONTRACT = {
    "export": "check-evidence-v8.py#export_op6_recovery_custody_traces",
    "shape": "raw token-free required refs/units/frozen-target/custody-row materials and CAS bytes plus ordered project/RT13/journal/final/fact snapshots for commit, delayed-reclaim and custody-loss",
    "oracleBoundary": "No success/pinned/verified assertion boolean is exported; OP6 must independently recompute identities and state consequences from the raw records.",
}

API_CONTRACT = {
    "opaqueTypes": [
        "DurableProjectStateV2", "ProjectStoreAuthorityV1",
        "TrustedRequestContextV1", "AdmittedEvaluationAuthorityV1",
        "ValidatedEP8BundleV5", "ValidatedRunFreeClosureV3",
        "PreparedCustodyV1", "FinalizedSemanticEvidenceV1",
        "CommittedRunV1", "VerifiedStoredRunV1",
    ],
    "calls": [
        "opensip_store.open_project_store_authority_v1(HostProjectAdmissionV1, DurableProjectStateV2) -> ProjectStoreAuthorityV1",
        "ProjectStoreAuthorityV1.authorize_evaluation(EvaluationAuthorityCandidateV1) -> AdmittedEvaluationAuthorityV1",
        "ProjectStoreAuthorityV1.resolve_stored_evaluation(EvaluationAuthoritySealRef) -> AdmittedEvaluationAuthorityV1",
        "opensip_evidence.validate_semantic_bundle_v1(bundle, AdmittedEvaluationAuthorityV1) -> ValidatedEP8BundleV5",
        "opensip_retention.validate_run_free_closure_v3(ValidatedEP8BundleV5, AdmittedEvaluationAuthorityV1, RT13.SemanticCapabilityClosureV3) -> ValidatedRunFreeClosureV3",
        "opensip_store.prepare_custody_v1(ProjectStoreAuthorityV1, FrozenRetentionTarget, RawProofInventoryV1, ValidatedRunFreeClosureV3) -> PreparedCustodyV1",
        "opensip_evidence.finalize_semantic_evidence_v1(ValidatedEP8BundleV5, ValidatedRunFreeClosureV3, PreparedCustodyV1) -> FinalizedSemanticEvidenceV1",
        "opensip_store.prepare_run_commit_v3(ProjectStoreAuthorityV1, FrozenAttemptRecord, AdmittedEvaluationAuthorityV1, FinalizedSemanticEvidenceV1, RT13.LeaseStateV2) -> RunFreePreparedCommitV3",
        "opensip_store.commit_run_v2(ProjectStoreAuthorityV1, TrustedRequestContextV1, ExecutionId, AdmittedEvaluationAuthorityV1, FinalizedSemanticEvidenceV1, PreparedCustodyV1) -> CommittedRunV1",
        "opensip_store.recover_run_v2(ProjectStoreAuthorityV1, TrustedRequestContextV1, ExecutionId) -> CommittedRunV1 | NoPreparedRun | AttemptTerminalDispositionV1",
        "opensip_store.read_committed_run_v1(ProjectStoreAuthorityV1, RunId) -> VerifiedStoredRunV1",
        "opensip_evidence.project_read_v1(VerifiedStoredRunV1, RT13 mutableState, VERSIONING v8 availability) -> EvidenceReadProjectionV1",
    ],
    "constructionRule": "There is one production ProjectStoreAuthorityV1 nominal port. Commit/recovery accept that live port, an opaque host-owned TrustedRequestContextV1 and host-owned ExecutionId; they never accept raw RequestId/ExecutionId strings from callers. Fresh recovery reads the journal itself, cold-resolves EP8 authority, and remints finalized/custody capabilities under the new session. No overload accepts caller journal/candidate/inventory, an old handle/token, raw JSON, supplied PlanId/RunId/ref, owner string or verified/pinned boolean. The TrustedRequestContextV1 construction leaf remains externally pending and is not invented by E8.",
}

DURABLE_RECOVERY_CONTRACT = {
    "stateType": "DurableProjectStateV2",
    "sessionType": "ProjectStoreAuthorityV1",
    "stateOwns": [
        "EP8 immutable authority CAS/index",
        "closed typed private Evidence CAS with exact raw hash/kind/project/canonical-byte validation",
        "frozen Attempt revisions and exact content CAS refs",
        "RunFreePreparedCommitV3 journals with exact RT13 lease binding and custody revision",
        "RT13 LeaseStateV2 closed unique same-project object superset containing the exact 23-key required subset, singular lease, monotonic fence and pending expiry",
        "paired AttemptTerminalDispositionV1/CustodyLossProofV1 source facts for pre-Run custody loss",
        "six final record maps including RunCommitNotificationV1",
    ],
    "sessionRule": "Every open/reopen creates a new nonserializable instance token over the durable state. No module-global ledger map or ephemeral-token-keyed durable state exists.",
    "recoveryApi": "recover_run_v2(ProjectStoreAuthorityV1, TrustedRequestContextV1, ExecutionId)",
    "recoveryOrder": [
        "audit complete private CAS and read exact frozen Attempt content plus private Run-free journal",
        "EP8 cold-resolve EAS from exact immutable CAS/index under the fresh session",
        "reread exact canonical bundle/closure/inventory/SemanticEvidence/target/custody material and all 23 required row bytes",
        "rederive RT13 closure/raw inventory and unchanged SemanticEvidence identities",
        "reconstruct exact custody from RT13 state; if the owner is dead, reclaim at the next eligible sequence after all real intervening events, then revalidate immutable authority and patch only custody fields during fresh repin",
        "commit through that same session/context or verify the complete six-record committed set while preserving its persisted committerRequestId",
    ],
    "forbiddenAuthority": [
        "old AdmittedEvaluationAuthorityV1", "old ProjectStoreAuthority session token",
        "old FinalizedSemanticEvidenceV1", "old PreparedCustodyV1",
        "warm candidate/cache/inventory", "caller journal or boolean",
        "process-global ledger keyed by any token",
    ],
}


class DuplicateKeyError(ValueError):
    pass


class LedgerCorrupt(ValueError):
    pass


class BusyTimeout(RuntimeError):
    pass


class NoPreparedRun(ValueError):
    pass


class CustodyPendingExpiry(RuntimeError):
    """Post-admission custody loss; D9 classification intentionally unresolved."""


class CommitFailed(RuntimeError):
    pass


class ResponseLost(RuntimeError):
    pass


class CustodyUnavailable(RuntimeError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def load(name_or_path: str | pathlib.Path) -> Any:
    path = pathlib.Path(name_or_path)
    if not path.is_absolute() and path.parent == pathlib.Path("."):
        path = HERE / path
    return json.loads(path.read_text(), object_pairs_hook=_pairs)


def sha_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha_ref(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _module(filename: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


_RT_CONTEXT: dict[str, Any] | None = None


def _rt_context() -> dict[str, Any]:
    """Load and mechanically derive the sole RT13 custody authority."""
    global _RT_CONTEXT
    if _RT_CONTEXT is not None:
        return _RT_CONTEXT
    for filename in (
            "evaluation-proof.v8.json", "check-evaluation-proof-v8.py",
            "retention-tiers.v13.json", "check-retention-custody-v13.py",
            "check-retention-custody.py"):
        actual = sha_file(filename)
        if actual != PINS[filename]:
            raise ValueError(f"pinned RT13 input drift: {filename}")
    rt = load("retention-tiers.v13.json")
    ep = load("evaluation-proof.v8.json")
    rt13mod = _module(
        "check-retention-custody-v13.py", "rt13_authority_for_evidence_v8")
    ep8mod = _module(
        "check-evaluation-proof-v8.py", "ep8_authority_for_evidence_v8")
    rtcore = _module(
        "check-retention-custody.py", "rtcore_authority_for_evidence_v8")
    findings = rt13mod.check(rt)
    if findings:
        raise ValueError(f"pinned RT13 is red: {findings[0]}")
    derived = rt13mod.regenerate(rt, ep, ep8mod, rtcore)
    frozen = rt["capabilityClosure"]["semanticClosure"]
    if derived["proofRefs"] != frozen["proofRefs"] or \
            derived["units"] != frozen["units"] or \
            derived["closureCommitment"] != frozen["closureCommitment"]:
        raise ValueError("cold RT13 derivation differs from authoritative closure")
    pin_refs = sorted([{
        "projectId": row["projectId"],
        "recordCasRef": row["recordCasRef"],
        "recordKind": row["recordKind"],
    } for row in derived["proofRefs"]], key=canonical)
    if len(pin_refs) != 23 or len({canonical(row) for row in pin_refs}) != 23:
        raise ValueError("RT13 does not derive exactly 23 unique raw objects")
    _RT_CONTEXT = {
        "contract": rt,
        "checker": rt13mod,
        "core": rtcore,
        "derived": derived,
        "pinRefs": pin_refs,
        "unitIds": [row["unitId"] for row in derived["units"]],
    }
    return _RT_CONTEXT


def _validate_rt_state(value: Any, project: str) -> dict[str, Any]:
    ctx = _rt_context()
    findings: list[tuple[str, str]] = []
    ctx["core"]._validate_lease_state(value, "$rtState", findings)
    if findings:
        raise LedgerCorrupt(f"RT13 LeaseStateV2 invalid: {findings[0]}")
    if value.get("projectId") != project:
        raise LedgerCorrupt("RT13 state crosses ProjectId")
    expected = {canonical(row) for row in ctx["pinRefs"]}
    actual: set[bytes] = set()
    for row in value.get("objects", []):
        if not isinstance(row, dict) or set(row) != {
                "projectId", "recordCasRef", "recordKind", "state"}:
            raise LedgerCorrupt("RawObjectStateV1 is not exact/closed")
        key = canonical({key: row[key] for key in (
            "projectId", "recordCasRef", "recordKind")})
        if key in actual:
            raise LedgerCorrupt("RT13 project inventory contains a duplicate raw key")
        actual.add(key)
    if not expected <= actual:
        raise LedgerCorrupt("RT13 project inventory omits required raw authority")
    return copy.deepcopy(value)


def _initial_rt_state(project: str) -> dict[str, Any]:
    state = {
        "schemaVersion": 2,
        "projectId": project,
        "ledgerSequence": 0,
        "lastIssuedFencingToken": 0,
        "objects": [dict(row, state="AVAILABLE")
                    for row in _rt_context()["pinRefs"]],
        "lease": None,
    }
    return _validate_rt_state(state, project)


def _reduce_rt(state: dict[str, Any], event: dict[str, Any],
               project: str) -> dict[str, Any]:
    ctx = _rt_context()
    findings: list[tuple[str, str]] = []
    ctx["core"]._validate_lease_state(state, "$before", findings)
    ctx["core"]._validate_lease_event(event, "$event", project, findings)
    if findings:
        raise LedgerCorrupt(f"RT13 reducer input invalid: {findings[0]}")
    output = ctx["core"].reduce_lease(copy.deepcopy(state), copy.deepcopy(event))
    if not isinstance(output, dict) or set(output) != {"state", "result"}:
        raise LedgerCorrupt("RT13 reducer output is not exact")
    _validate_rt_state(output["state"], project)
    return output


def _rt_error(result: Any) -> Any:
    return (result.get("termination") or {}).get("errorCode") \
        if isinstance(result, dict) else None


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _exact(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise LedgerCorrupt(f"{label} is not an exact closed object")
    return value


def _has_token_key(value: Any) -> bool:
    if isinstance(value, dict):
        return bool(set(value) & TOKEN_KEYS) or any(
            _has_token_key(child) for child in value.values())
    if isinstance(value, list):
        return any(_has_token_key(child) for child in value)
    return False


def _walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_strings(child)


def _cas_entry(project: str, kind: str, raw: bytes) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "projectId": project,
        "recordCasRef": sha_ref(raw),
        "recordKind": kind,
        "recordBytesHex": raw.hex(),
    }


def _json_cas_entry(project: str, kind: str,
                    value: dict[str, Any]) -> dict[str, Any]:
    return _cas_entry(project, kind, canonical(value))


def _accepted_ep8_vector() -> dict[str, Any]:
    ep = load("evaluation-proof.v8.json")
    vector_id = ep.get("acceptedAuthorityVectorId")
    rows = [row for row in ep.get("positiveVectors", [])
            if isinstance(row, dict) and row.get("id") == vector_id]
    if len(rows) != 1:
        raise LedgerCorrupt("EP8 accepted authority vector is not unique")
    return rows[0]


def _authority_context(contract: dict[str, Any]) -> dict[str, Any]:
    """Cold-build every immutable byte needed by the Evidence test store."""
    vector = _accepted_ep8_vector()
    golden = contract["acceptedGolden"]
    values = golden["values"]
    project = values["projectId"]
    if vector.get("bundle", {}).get("projectId") != project:
        raise LedgerCorrupt("EP8 accepted vector crosses the Evidence project")
    authority = vector.get("authorityGoldens") or {}
    fixture = vector.get("trustedStoreFixture") or {}
    if fixture.get("projectId") != project:
        raise LedgerCorrupt("EP8 durable authority fixture crosses ProjectId")

    entries: list[dict[str, Any]] = []
    for row in fixture.get("immutableCasRecords", []):
        if not isinstance(row, dict) or set(row) != {
                "projectId", "recordCasRef", "recordKind", "recordBytesHex"}:
            raise LedgerCorrupt("EP8 immutable CAS row is not closed")
        try:
            raw = bytes.fromhex(row["recordBytesHex"])
        except (TypeError, ValueError) as exc:
            raise LedgerCorrupt("EP8 immutable CAS bytes are malformed") from exc
        entry = _cas_entry(project, row["recordKind"], raw)
        if row["projectId"] != project or entry["recordCasRef"] != row["recordCasRef"]:
            raise LedgerCorrupt("EP8 immutable CAS row fails hash/project validation")
        entries.append(entry)

    index_raw = authority.get("evaluationAuthorityStoreIndexRaw") or {}
    try:
        index_bytes = bytes.fromhex(index_raw["encodedHex"])
    except (KeyError, TypeError, ValueError) as exc:
        raise LedgerCorrupt("EP8 authority index bytes are absent/malformed") from exc
    index_entry = _cas_entry(project, "EvaluationAuthorityIndexV1", index_bytes)
    if index_entry["recordCasRef"] != index_raw.get("rawCasRef"):
        raise LedgerCorrupt("EP8 authority index raw hash differs")
    entries.append(index_entry)

    bundle_entry = _json_cas_entry(
        project, "EvaluationProofBundleV5", vector["bundle"])
    if bundle_entry["recordCasRef"] != values["evaluationProofBundleCasRef"]:
        raise LedgerCorrupt("EP8 bundle canonical bytes differ from Evidence")
    entries.append(bundle_entry)

    closure = _rt_context()["contract"]["capabilityClosure"]["semanticClosure"]
    closure_entry = _json_cas_entry(
        project, "SemanticCapabilityClosureV3", closure)
    if closure_entry["recordCasRef"] != values["semanticCapabilityClosureCasRef"]:
        raise LedgerCorrupt("RT13 closure canonical bytes differ from Evidence")
    entries.append(closure_entry)

    inventory_entry = _cas_entry(
        project, "RawProofInventoryV1",
        bytes.fromhex(golden["rawProofInventoryHex"]))
    semantic_entry = _cas_entry(
        project, "SemanticEvidenceV1",
        bytes.fromhex(golden["semanticEvidenceHex"]))
    if semantic_entry["recordCasRef"] != golden["semanticEvidenceCasRef"]:
        raise LedgerCorrupt("SemanticEvidence raw hash differs from protected identity")
    entries += [inventory_entry, semantic_entry]

    frozen_target = {
        "schemaVersion": 1,
        "projectId": project,
        "targetCapability": values["sealedCapability"],
        "evaluationAuthoritySealRef": values["evaluationAuthoritySealRef"],
        "semanticCapabilityClosureCommitment":
            values["semanticCapabilityClosureCommitment"],
        "unitIds": copy.deepcopy(_rt_context()["unitIds"]),
    }
    target_entry = _json_cas_entry(
        project, "FrozenRetentionTargetV1", frozen_target)
    entries.append(target_entry)

    refs = [row["recordCasRef"] for row in entries]
    if len(refs) != len(set(refs)):
        raise LedgerCorrupt("base private CAS contains duplicate raw hashes")
    admission_ref = authority.get("evaluationAuthorityAdmissionRef")
    if admission_ref not in refs or \
            values["evaluationAuthoritySealRef"] != \
            authority.get("evaluationAuthoritySealRef"):
        raise LedgerCorrupt("EP8 admission/seal authority join differs")
    fixture_row = {
        "schemaVersion": 1,
        "projectId": project,
        "evaluationAuthoritySealRef": values["evaluationAuthoritySealRef"],
        "evaluationAuthorityIndexCasRef": index_entry["recordCasRef"],
        "evaluationAuthorityAdmissionCasRef": admission_ref,
        "evaluationProofBundleCasRef": bundle_entry["recordCasRef"],
        "semanticCapabilityClosureCasRef": closure_entry["recordCasRef"],
        "rawProofInventoryCasRef": inventory_entry["recordCasRef"],
        "semanticEvidenceCasRef": semantic_entry["recordCasRef"],
        "frozenRetentionTargetRef": target_entry["recordCasRef"],
    }
    return {
        "entries": entries,
        "entriesByRef": {row["recordCasRef"]: row for row in entries},
        "fixture": fixture_row,
        "frozenTarget": frozen_target,
    }


def _attempt_material(row: dict[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(value) for key, value in row.items()
            if key != "frozenAttemptCasRef"}


def _custody_row_materials(contract: dict[str, Any]) -> list[dict[str, Any]]:
    project = contract["acceptedGolden"]["values"]["projectId"]
    target_ref = _authority_context(contract)["fixture"]["frozenRetentionTargetRef"]
    rows: list[dict[str, Any]] = []
    for unit in _rt_context()["derived"]["units"]:
        for obj in unit["objectRefs"]:
            rows.append({
                "schemaVersion": 2,
                "projectId": project,
                "frozenRetentionTargetRef": target_ref,
                "unitId": unit["unitId"],
                "requiredForCapability": unit["requiredForCapability"],
                "recordCasRef": obj["recordCasRef"],
                "recordKind": obj["recordKind"],
            })
    rows.sort(key=canonical)
    if len(rows) != 23 or len({canonical(row) for row in rows}) != 23:
        raise LedgerCorrupt("custody preparation does not derive 23 unique rows")
    return rows


def _custody_row_entries(contract: dict[str, Any]) -> list[dict[str, Any]]:
    project = contract["acceptedGolden"]["values"]["projectId"]
    return [_json_cas_entry(project, "CustodyPreparedObjectV2", row)
            for row in _custody_row_materials(contract)]


def _custody_material(contract: dict[str, Any], execution_id: str,
                      attempt: dict[str, Any]) -> dict[str, Any]:
    ctx = _authority_context(contract)
    values = contract["acceptedGolden"]["values"]
    return {
        "schemaVersion": 2,
        "projectId": values["projectId"],
        "executionId": execution_id,
        "frozenAttemptCasRef": attempt["frozenAttemptCasRef"],
        "evaluationAuthoritySealRef": values["evaluationAuthoritySealRef"],
        "evaluationAuthorityAdmissionCasRef":
            ctx["fixture"]["evaluationAuthorityAdmissionCasRef"],
        "semanticEvidenceCasRef": ctx["fixture"]["semanticEvidenceCasRef"],
        "evaluationProofBundleCasRef":
            ctx["fixture"]["evaluationProofBundleCasRef"],
        "semanticCapabilityClosureCasRef":
            ctx["fixture"]["semanticCapabilityClosureCasRef"],
        "semanticCapabilityClosureCommitment":
            values["semanticCapabilityClosureCommitment"],
        "rawProofInventoryCasRef": ctx["fixture"]["rawProofInventoryCasRef"],
        "frozenRetentionTargetRef": ctx["fixture"]["frozenRetentionTargetRef"],
        "units": copy.deepcopy(_rt_context()["derived"]["units"]),
        "requiredRowCasRefs": sorted(
            row["recordCasRef"] for row in _custody_row_entries(contract)),
    }


def _decode_canonical_json(entry: dict[str, Any], label: str) -> dict[str, Any]:
    try:
        raw = bytes.fromhex(entry["recordBytesHex"])
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs)
    except (TypeError, ValueError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError) as exc:
        raise LedgerCorrupt(f"{label} canonical JSON bytes are malformed") from exc
    if not isinstance(value, dict) or canonical(value) != raw:
        raise LedgerCorrupt(f"{label} bytes are not exact canonical JSON")
    return value


def _cas_put(rows: list[dict[str, Any]], entry: dict[str, Any]) -> None:
    matches = [row for row in rows
               if isinstance(row, dict) and
               row.get("recordCasRef") == entry["recordCasRef"]]
    if not matches:
        rows.append(copy.deepcopy(entry))
        return
    if len(matches) != 1 or matches[0] != entry:
        raise LedgerCorrupt("private CAS write is not absent-or-exact")


def _validate_private_cas(value: Any, project: str,
                          contract: dict[str, Any]) -> \
        tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    if not isinstance(value, list):
        raise LedgerCorrupt("private CAS container is not an array")
    base = _authority_context(contract)["entriesByRef"]
    allowed_dynamic = {
        "FrozenAttemptRecordV1", "CustodyPreparedObjectV2",
        "CustodyPreparationMaterialV2",
    }
    rows: dict[str, dict[str, Any]] = {}
    decoded: dict[str, dict[str, Any]] = {}
    for raw_entry in value:
        entry = _exact(raw_entry, PRIVATE_CAS_FIELDS, "PrivateCasObjectV1")
        if entry.get("schemaVersion") != 1 or entry.get("projectId") != project or \
                not REF_RE.fullmatch(entry.get("recordCasRef", "")) or \
                not isinstance(entry.get("recordKind"), str) or \
                not entry["recordKind"] or \
                not isinstance(entry.get("recordBytesHex"), str) or \
                not re.fullmatch(r"(?:[0-9a-f]{2})+", entry["recordBytesHex"]):
            raise LedgerCorrupt("PrivateCasObjectV1 scalar/project shape invalid")
        try:
            raw_bytes = bytes.fromhex(entry["recordBytesHex"])
        except ValueError as exc:
            raise LedgerCorrupt("private CAS bytes are malformed") from exc
        if sha_ref(raw_bytes) != entry["recordCasRef"]:
            raise LedgerCorrupt("private CAS hash does not bind exact bytes")
        ref = entry["recordCasRef"]
        if ref in rows:
            raise LedgerCorrupt("duplicate private CAS raw key")
        rows[ref] = copy.deepcopy(entry)
        if ref in base:
            if entry != base[ref]:
                raise LedgerCorrupt("fixed private CAS kind/project/bytes substituted")
        elif entry["recordKind"] in allowed_dynamic:
            decoded[ref] = _decode_canonical_json(entry, entry["recordKind"])
        else:
            raise LedgerCorrupt("unknown/unbound private CAS record kind")
    for ref, expected in base.items():
        if rows.get(ref) != expected:
            raise LedgerCorrupt("required private authority CAS record missing")
    return rows, decoded


def _terminal_values(contract: dict[str, Any]) -> list[str]:
    golden = contract["acceptedGolden"]
    values = golden["values"]
    return [
        "1", values["projectId"], golden["runId"], values["planId"],
        values["planIntentCommitment"], values["executionPlanCommitment"],
        values["activationManifestRef"], values["evaluationAuthoritySealRef"],
        golden["semanticEvidenceCasRef"], golden["evidenceDigest"],
        values["verdict"], values["sealedCapability"],
        values["semanticCapabilityClosureCasRef"],
        values["semanticCapabilityClosureCommitment"],
    ]


def _decode_terminal(raw: bytes) -> list[str]:
    if not raw or raw[0] != 0x84:
        raise LedgerCorrupt("TerminalRunV1 record tag invalid")
    offset = 1
    values: list[str] = []
    for tag in range(0xB0, 0xBE):
        if offset + 5 > len(raw) or raw[offset] != tag:
            raise LedgerCorrupt("TerminalRunV1 field tag/order invalid")
        size = int.from_bytes(raw[offset + 1:offset + 5], "big")
        start = offset + 5
        end = start + size
        if end > len(raw):
            raise LedgerCorrupt("TerminalRunV1 field length invalid")
        try:
            text = raw[start:end].decode("utf-8")
        except UnicodeDecodeError as exc:
            raise LedgerCorrupt("TerminalRunV1 field is not UTF-8") from exc
        if not text or any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
            raise LedgerCorrupt("TerminalRunV1 text scalar invalid")
        values.append(text)
        offset = end
    if offset != len(raw):
        raise LedgerCorrupt("TerminalRunV1 has trailing bytes")
    return values


def _fixture_request_id_value(execution_id: str,
                              generation: str = "live") -> str:
    return "req1_" + hashlib.sha256(
        f"{execution_id}\0{generation}".encode("utf-8")).hexdigest()[:32]


def _expected_records(contract: dict[str, Any], execution_id: str,
                      committer_request_id: str | None = None) -> \
        dict[str, dict[str, Any]]:
    if not isinstance(execution_id, str) or not EXEC_RE.fullmatch(execution_id):
        raise ValueError("ExecutionId invalid")
    if committer_request_id is None:
        committer_request_id = _fixture_request_id_value(execution_id)
    if not REQUEST_RE.fullmatch(committer_request_id):
        raise ValueError("committing RequestId invalid")
    golden = contract["acceptedGolden"]
    values = golden["values"]
    project = values["projectId"]
    run_id = golden["runId"]
    seal = golden["runSealRef"]
    return {
        "TerminalRunV1": {
            "schemaVersion": 1, "projectId": project, "runId": run_id,
            "runSealRef": seal, "recordBytesHex": golden["terminalRunEncodedHex"],
        },
        "RunIndexV1": {
            "schemaVersion": 1, "projectId": project, "runId": run_id,
            "runSealRef": seal,
        },
        "AttemptRunLinkV1": {
            "schemaVersion": 1, "projectId": project,
            "executionId": execution_id, "disposition": "run-committed",
            "runId": run_id, "runSealRef": seal,
        },
        "RunCustodyRootV1": {
            "schemaVersion": 1, "projectId": project, "runId": run_id,
            "runSealRef": seal,
            "semanticEvidenceCasRef": golden["semanticEvidenceCasRef"],
            "unitIds": list(UNIT_IDS),
        },
        "RunAuthorityIndexV1": copy.deepcopy(golden["runAuthorityIndex"]),
        "RunCommitNotificationV1": {
            "schemaVersion": 1, "projectId": project,
            "notificationKind": "run-committed",
            "committerRequestId": committer_request_id,
            "executionId": execution_id,
            "runId": run_id, "runSealRef": seal,
        },
    }


def _validate_final(name: str, value: Any, project: str,
                    contract: dict[str, Any]) -> dict[str, Any]:
    if name not in FINAL_FIELDS:
        raise LedgerCorrupt(f"unknown final container {name}")
    row = _exact(value, set(FINAL_FIELDS[name]), name)
    if row.get("schemaVersion") != 1 or row.get("projectId") != project or \
            not PROJECT_RE.fullmatch(project):
        raise LedgerCorrupt(f"{name} schema/project invalid")
    if not RUN_RE.fullmatch(row.get("runId", "")) or \
            not REF_RE.fullmatch(row.get("runSealRef", "")):
        raise LedgerCorrupt(f"{name} Run identity invalid")
    golden = contract["acceptedGolden"]
    if row["runId"] != golden["runId"] or row["runSealRef"] != golden["runSealRef"]:
        raise LedgerCorrupt(f"{name} differs from protected Run identity")
    if name == "TerminalRunV1":
        encoded = row["recordBytesHex"]
        if not isinstance(encoded, str) or not re.fullmatch(r"(?:[0-9a-f]{2})+", encoded):
            raise LedgerCorrupt("TerminalRunV1 recordBytesHex invalid")
        raw = bytes.fromhex(encoded)
        if sha_ref(raw) != row["runSealRef"] or \
                _decode_terminal(raw) != _terminal_values(contract):
            raise LedgerCorrupt("TerminalRunV1 bytes/hash/field join invalid")
    elif name == "AttemptRunLinkV1":
        if not EXEC_RE.fullmatch(row.get("executionId", "")) or \
                row.get("disposition") != "run-committed":
            raise LedgerCorrupt("AttemptRunLinkV1 invalid")
    elif name == "RunCustodyRootV1":
        if row.get("semanticEvidenceCasRef") != golden["semanticEvidenceCasRef"] or \
                row.get("unitIds") != UNIT_IDS or \
                any(not UNIT_RE.fullmatch(x) for x in row.get("unitIds", []) \
                    if isinstance(x, str)):
            raise LedgerCorrupt("RunCustodyRootV1 exact custody join invalid")
    elif name == "RunAuthorityIndexV1":
        if row != golden["runAuthorityIndex"]:
            raise LedgerCorrupt("RunAuthorityIndexV1 authority join invalid")
    elif name == "RunCommitNotificationV1":
        if not EXEC_RE.fullmatch(row.get("executionId", "")) or \
                row.get("notificationKind") != "run-committed" or \
                not REQUEST_RE.fullmatch(row.get("committerRequestId", "")):
            raise LedgerCorrupt("RunCommitNotificationV1 invalid")
    return copy.deepcopy(row)


def _validate_attempt(value: Any, project: str,
                      contract: dict[str, Any]) -> dict[str, Any]:
    row = _exact(value, ATTEMPT_FIELDS, "FrozenAttemptRecordV1")
    if row.get("schemaVersion") != 1 or row.get("projectId") != project or \
            not EXEC_RE.fullmatch(row.get("executionId", "")) or \
            not _is_int(row.get("revision")) or row["revision"] < 0:
        raise LedgerCorrupt("FrozenAttemptRecordV1 scalar invalid")
    for key in ("frozenAttemptCasRef", "evaluationAuthoritySealRef",
                "evaluationAuthorityAdmissionCasRef",
                "frozenRetentionTargetRef", "semanticEvidenceCasRef"):
        if not REF_RE.fullmatch(row.get(key, "")):
            raise LedgerCorrupt("FrozenAttemptRecordV1 ref invalid")
    authority = _authority_context(contract)["fixture"]
    for key in ("evaluationAuthoritySealRef",
                "evaluationAuthorityAdmissionCasRef",
                "frozenRetentionTargetRef", "semanticEvidenceCasRef"):
        if row[key] != authority[key]:
            raise LedgerCorrupt("FrozenAttemptRecordV1 authority ref substituted")
    return copy.deepcopy(row)


def _validate_journal(value: Any, project: str) -> dict[str, Any]:
    row = _exact(value, JOURNAL_FIELDS, "RunFreePreparedCommitV3")
    if row.get("schemaVersion") != 3 or row.get("projectId") != project or \
            not EXEC_RE.fullmatch(row.get("executionId", "")) or \
            not _is_int(row.get("expectedAttemptRevision")) or \
            row["expectedAttemptRevision"] < 0 or \
            not _is_int(row.get("custodyRevision")) or row["custodyRevision"] < 1:
        raise LedgerCorrupt("RunFreePreparedCommitV3 scalar invalid")
    for key in ("frozenAttemptCasRef", "evaluationAuthoritySealRef",
                "evaluationAuthorityAdmissionCasRef", "semanticEvidenceCasRef",
                "frozenRetentionTargetRef", "rawProofInventoryCasRef",
                "custodyPreparationRef"):
        if not REF_RE.fullmatch(row.get(key, "")):
            raise LedgerCorrupt("RunFreePreparedCommitV3 ref invalid")
    if row.get("custodyState") not in {
            "HELD_PREPARED", "RECLAIMED_PENDING_REPIN"} or \
            not LEASE_RE.fullmatch(row.get("leaseId", "")) or \
            not OWNER_RE.fullmatch(row.get("ownerId", "")) or \
            not LIVENESS_RE.fullmatch(row.get("ownerLivenessToken", "")) or \
            not _is_int(row.get("fencingToken")) or row["fencingToken"] < 1:
        raise LedgerCorrupt("RunFreePreparedCommitV3 custody binding invalid")
    if not isinstance(row.get("pinnedRefs"), list) or \
            sorted(row["pinnedRefs"], key=canonical) != _rt_context()["pinRefs"]:
        raise LedgerCorrupt("RunFreePreparedCommitV3 pin set is not exact RT13 authority")
    return copy.deepcopy(row)


def _validate_attempt_private_cas(row: dict[str, Any],
                                  cas: dict[str, dict[str, Any]],
                                  decoded: dict[str, dict[str, Any]]) -> None:
    ref = row["frozenAttemptCasRef"]
    entry = cas.get(ref)
    if entry is None or entry.get("recordKind") != "FrozenAttemptRecordV1" or \
            decoded.get(ref) != _attempt_material(row):
        raise LedgerCorrupt(
            "FrozenAttemptRecordV1 revision/content is not bound to audited CAS bytes")


def _validate_journal_private_cas(row: dict[str, Any],
                                  attempt: dict[str, Any],
                                  cas: dict[str, dict[str, Any]],
                                  decoded: dict[str, dict[str, Any]],
                                  contract: dict[str, Any]) -> None:
    authority = _authority_context(contract)["fixture"]
    exact_attempt = {
        "expectedAttemptRevision": attempt["revision"],
        "frozenAttemptCasRef": attempt["frozenAttemptCasRef"],
        "evaluationAuthoritySealRef": attempt["evaluationAuthoritySealRef"],
        "evaluationAuthorityAdmissionCasRef":
            attempt["evaluationAuthorityAdmissionCasRef"],
        "semanticEvidenceCasRef": attempt["semanticEvidenceCasRef"],
        "frozenRetentionTargetRef": attempt["frozenRetentionTargetRef"],
        "rawProofInventoryCasRef": authority["rawProofInventoryCasRef"],
    }
    for key, expected in exact_attempt.items():
        if row.get(key) != expected:
            raise LedgerCorrupt("journal immutable Attempt/authority snapshot substituted")
    material = _custody_material(contract, row["executionId"], attempt)
    expected_entry = _json_cas_entry(
        row["projectId"], "CustodyPreparationMaterialV2", material)
    if row["custodyPreparationRef"] != expected_entry["recordCasRef"] or \
            cas.get(expected_entry["recordCasRef"]) != expected_entry or \
            decoded.get(expected_entry["recordCasRef"]) != material:
        raise LedgerCorrupt("journal custody preparation is not exact audited CAS authority")
    for expected in _custody_row_entries(contract):
        if cas.get(expected["recordCasRef"]) != expected or \
                decoded.get(expected["recordCasRef"]) != \
                _decode_canonical_json(expected, "CustodyPreparedObjectV2"):
            raise LedgerCorrupt("required custody row missing/substituted in private CAS")


def _validate_terminal_fact(name: str, value: Any,
                            project: str) -> dict[str, Any]:
    row = _exact(value, TERMINAL_FACT_FIELDS[name], name)
    if row.get("schemaVersion") != 1 or row.get("projectId") != project or \
            not EXEC_RE.fullmatch(row.get("executionId", "")):
        raise LedgerCorrupt(f"{name} scalar/project invalid")
    forbidden = {"runId", "runSealRef", "class", "errorCode", "exitCode",
                 "RequestId", "requestId"}
    if set(_walk_strings(row)) & forbidden:
        raise LedgerCorrupt(f"{name} contains Run/D9/request authority")
    if name == "AttemptTerminalDispositionV1":
        if row.get("disposition") != "custody-lost-before-run" or \
                not REF_RE.fullmatch(row.get("custodyLossProofRef", "")):
            raise LedgerCorrupt("AttemptTerminalDispositionV1 value invalid")
    else:
        if row.get("cause") != "required-custody-unavailable" or \
                not REF_RE.fullmatch(row.get("frozenAttemptCasRef", "")) or \
                not REF_RE.fullmatch(row.get("custodyPreparationRef", "")) or \
                not _is_int(row.get("observedAtSequence")) or \
                row["observedAtSequence"] < 0 or \
                not isinstance(row.get("requiredObjectStates"), list):
            raise LedgerCorrupt("CustodyLossProofV1 value invalid")
        expected_keys = {canonical(ref) for ref in _rt_context()["pinRefs"]}
        actual_keys: set[bytes] = set()
        for state in row["requiredObjectStates"]:
            parsed = _exact(state, {
                "projectId", "recordCasRef", "recordKind", "state"},
                "CustodyLossProofV1.requiredObjectStates[]")
            key = canonical({field: parsed[field] for field in (
                "projectId", "recordCasRef", "recordKind")})
            if parsed["projectId"] != project or key in actual_keys or \
                    parsed.get("state") not in {"AVAILABLE", "PURGED", "EXPIRED"}:
                raise LedgerCorrupt("CustodyLossProofV1 object state invalid")
            actual_keys.add(key)
        if actual_keys != expected_keys:
            raise LedgerCorrupt("CustodyLossProofV1 must enumerate exact required subset")
    return copy.deepcopy(row)


def _audit(content: Any, contract: dict[str, Any]) -> None:
    root = _exact(content, CONTENT_FIELDS, "DurableProjectContentV2")
    project = root.get("projectId")
    if root.get("schemaVersion") != 2 or not isinstance(project, str) or \
            not PROJECT_RE.fullmatch(project) or _has_token_key(root):
        raise LedgerCorrupt("durable project envelope invalid")
    authority_fixture = _exact(
        root.get("authorityFixture"), AUTHORITY_FIXTURE_FIELDS,
        "PrivateAuthorityIndexV1")
    if authority_fixture != _authority_context(contract)["fixture"] or \
            not isinstance(root.get("privateCas"), list) or \
            not isinstance(root.get("rtState"), dict):
        raise LedgerCorrupt("durable project owned namespace shape invalid")
    cas, decoded_cas = _validate_private_cas(
        root["privateCas"], project, contract)
    attempts_raw = root.get("attempts")
    journals_raw = root.get("journals")
    if not isinstance(attempts_raw, list) or not isinstance(journals_raw, list):
        raise LedgerCorrupt("attempt/journal containers must be arrays")
    attempts: dict[str, dict[str, Any]] = {}
    for raw in attempts_raw:
        row = _validate_attempt(raw, project, contract)
        if row["executionId"] in attempts:
            raise LedgerCorrupt("duplicate Attempt execution key")
        _validate_attempt_private_cas(row, cas, decoded_cas)
        attempts[row["executionId"]] = row
    journals: dict[str, dict[str, Any]] = {}
    for raw in journals_raw:
        row = _validate_journal(raw, project)
        execution = row["executionId"]
        if execution in journals:
            raise LedgerCorrupt("duplicate journal execution key")
        attempt = attempts.get(execution)
        if attempt is None:
            raise LedgerCorrupt("journal/Attempt join invalid")
        _validate_journal_private_cas(
            row, attempt, cas, decoded_cas, contract)
        journals[execution] = row
    if len(journals) > 1:
        raise LedgerCorrupt("serialized custody permits at most one project journal")
    rt_state = _validate_rt_state(root["rtState"], project)
    lease = rt_state.get("lease")
    if journals:
        journal = next(iter(journals.values()))
        if journal["custodyState"] == "HELD_PREPARED":
            if not isinstance(lease, dict) or lease.get("state") != "HELD" or \
                    lease.get("leaseId") != journal["leaseId"] or \
                    lease.get("ownerId") != journal["ownerId"] or \
                    lease.get("ownerLivenessToken") != journal["ownerLivenessToken"] or \
                    lease.get("fencingToken") != journal["fencingToken"] or \
                    sorted(lease.get("pinnedRefs", []), key=canonical) != journal["pinnedRefs"]:
                raise LedgerCorrupt("HELD journal does not reconstruct from RT13 state")
        elif lease is not None or \
                rt_state["lastIssuedFencingToken"] != journal["fencingToken"]:
            raise LedgerCorrupt("RECLAIMED_PENDING_REPIN journal/RT13 state mismatch")
    elif isinstance(lease, dict) and lease.get("state") == "HELD":
        raise LedgerCorrupt("HELD RT13 lease exists without its sole custody journal")

    terminal = root.get("terminalFacts")
    if not isinstance(terminal, dict) or set(terminal) != set(TERMINAL_FACT_TYPES):
        raise LedgerCorrupt("terminal fact container set invalid")
    parsed_terminal: dict[str, list[dict[str, Any]]] = {}
    for name in TERMINAL_FACT_TYPES:
        if not isinstance(terminal[name], list):
            raise LedgerCorrupt(f"{name} container is not an array")
        parsed_terminal[name] = [
            _validate_terminal_fact(name, row, project) for row in terminal[name]]
    terminal_executions = {
        row["executionId"] for rows in parsed_terminal.values() for row in rows}
    for execution in terminal_executions:
        dispositions = [row for row in parsed_terminal[
            "AttemptTerminalDispositionV1"] if row["executionId"] == execution]
        proofs = [row for row in parsed_terminal["CustodyLossProofV1"]
                  if row["executionId"] == execution]
        if len(dispositions) != 1 or len(proofs) != 1 or \
                dispositions[0]["custodyLossProofRef"] != \
                sha_ref(canonical(proofs[0])) or \
                execution not in attempts or execution in journals:
            raise LedgerCorrupt("custody terminal facts are partial/duplicate/unjoined")

    finals = root.get("finalRecords")
    if not isinstance(finals, dict) or set(finals) != set(FINAL_TYPES):
        raise LedgerCorrupt("final record container set invalid")
    parsed: dict[str, list[dict[str, Any]]] = {}
    for name in FINAL_TYPES:
        rows = finals[name]
        if not isinstance(rows, list):
            raise LedgerCorrupt(f"{name} container is not an array")
        parsed[name] = [_validate_final(name, row, project, contract) for row in rows]

    run_ids = {row["runId"] for name in FINAL_TYPES for row in parsed[name]}
    for run_id in run_ids:
        for name in SHARED_R4:
            peers = [row for row in parsed[name] if row["runId"] == run_id]
            if len(peers) != 1:
                raise LedgerCorrupt(f"Run group lacks exactly one {name}")
        executions = {
            row["executionId"] for name in ATTEMPT_A2 for row in parsed[name]
            if row["runId"] == run_id
        }
        if not executions:
            raise LedgerCorrupt("shared R4 has no complete Attempt A2")
        for execution in executions:
            link = [row for row in parsed["AttemptRunLinkV1"]
                    if row["executionId"] == execution and row["runId"] == run_id]
            notifications = [row for row in parsed["RunCommitNotificationV1"]
                             if row["executionId"] == execution and
                             row["runId"] == run_id]
            if len(link) != 1 or len(notifications) != 1 or \
                    link[0]["runSealRef"] != notifications[0]["runSealRef"]:
                raise LedgerCorrupt("Attempt A2 is partial, duplicate, or conflicting")
            if execution in journals:
                raise LedgerCorrupt("journal coexists with committed Attempt A2")
    # Detect an A2 split across Run groups or same ExecutionId reused.
    all_execs = {row["executionId"] for name in ATTEMPT_A2 for row in parsed[name]}
    for execution in all_execs:
        links = [row for row in parsed["AttemptRunLinkV1"]
                 if row["executionId"] == execution]
        boxes = [row for row in parsed["RunCommitNotificationV1"]
                 if row["executionId"] == execution]
        if len(links) != 1 or len(boxes) != 1 or \
                (links[0]["runId"], links[0]["runSealRef"]) != \
                (boxes[0]["runId"], boxes[0]["runSealRef"]):
            raise LedgerCorrupt("ExecutionId does not own exactly one identical A2 pair")
        if execution in terminal_executions:
            raise LedgerCorrupt("custody-loss disposition coexists with committed A2")
    # Force canonical encodability as part of the project-wide audit.
    canonical(root)


_STATE_TOKEN = object()
_SNAPSHOT_TOKEN = object()


class _DurableProjectStateV2:
    __slots__ = ("_token", "project_revision", "content")

    def __init__(self, token: object, content: dict[str, Any]) -> None:
        if token is not _STATE_TOKEN:
            raise TypeError("guarded durable state required")
        self._token = token
        self.project_revision = 0
        self.content = copy.deepcopy(content)

    def __reduce__(self):
        raise TypeError("durable backend capability is not serializable")


class _ProjectSnapshotV1:
    __slots__ = ("_token", "project_revision", "content_digest", "content")

    def __init__(self, token: object, revision: int, digest: str,
                 content: dict[str, Any]) -> None:
        if token is not _SNAPSHOT_TOKEN:
            raise TypeError("guarded snapshot required")
        self._token = token
        self.project_revision = revision
        self.content_digest = digest
        self.content = content

    def __reduce__(self):
        raise TypeError("snapshot capability is not serializable")


def _guard(state: _DurableProjectStateV2) -> tuple[int, str]:
    return state.project_revision, sha_ref(canonical(state.content))


def _begin(state: _DurableProjectStateV2,
           contract: dict[str, Any]) -> _ProjectSnapshotV1:
    if not isinstance(state, _DurableProjectStateV2) or state._token is not _STATE_TOKEN:
        raise TypeError("guarded durable state required")
    _audit(state.content, contract)
    revision, digest = _guard(state)
    return _ProjectSnapshotV1(
        _SNAPSHOT_TOKEN, revision, digest, copy.deepcopy(state.content))


def _commit(state: _DurableProjectStateV2, snapshot: _ProjectSnapshotV1,
            contract: dict[str, Any]) -> None:
    if not isinstance(snapshot, _ProjectSnapshotV1) or \
            snapshot._token is not _SNAPSHOT_TOKEN:
        raise TypeError("guarded project snapshot required")
    if _guard(state) != (snapshot.project_revision, snapshot.content_digest):
        raise BusyTimeout("project snapshot guard changed")
    _audit(snapshot.content, contract)
    state.content = copy.deepcopy(snapshot.content)
    state.project_revision += 1


def _empty_state(contract: dict[str, Any]) -> _DurableProjectStateV2:
    project = contract["acceptedGolden"]["values"]["projectId"]
    authority = _authority_context(contract)
    content = {
        "schemaVersion": 2,
        "projectId": project,
        "authorityFixture": copy.deepcopy(authority["fixture"]),
        "privateCas": copy.deepcopy(authority["entries"]),
        "attempts": [],
        "journals": [],
        "rtState": _initial_rt_state(project),
        "finalRecords": {name: [] for name in FINAL_TYPES},
        "terminalFacts": {name: [] for name in TERMINAL_FACT_TYPES},
    }
    state = _DurableProjectStateV2(_STATE_TOKEN, content)
    _audit(state.content, contract)
    return state


def _attempt(contract: dict[str, Any], execution_id: str) -> dict[str, Any]:
    golden = contract["acceptedGolden"]
    authority = _authority_context(contract)["fixture"]
    material = {
        "schemaVersion": 1,
        "projectId": golden["values"]["projectId"],
        "executionId": execution_id,
        "revision": 1,
        "evaluationAuthoritySealRef": authority["evaluationAuthoritySealRef"],
        "evaluationAuthorityAdmissionCasRef":
            authority["evaluationAuthorityAdmissionCasRef"],
        "frozenRetentionTargetRef": authority["frozenRetentionTargetRef"],
        "semanticEvidenceCasRef": authority["semanticEvidenceCasRef"],
    }
    entry = _json_cas_entry(
        material["projectId"], "FrozenAttemptRecordV1", material)
    return dict(material, frozenAttemptCasRef=entry["recordCasRef"])


def _attempt_entry(attempt: dict[str, Any]) -> dict[str, Any]:
    return _json_cas_entry(
        attempt["projectId"], "FrozenAttemptRecordV1",
        _attempt_material(attempt))


def _operational_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\0".join(parts).encode("utf-8")).hexdigest()[:32]
    return f"{prefix}:{digest}"


def _owner_identity(execution_id: str, generation: str) -> tuple[str, str]:
    return (
        _operational_id("owner1", execution_id, generation, "owner"),
        _operational_id("live1", execution_id, generation, "liveness"),
    )


_TRUSTED_REQUEST_CONTEXT_TEST_TOKEN = object()
_HOST_EXECUTION_ID_TEST_TOKEN = object()


class _TrustedRequestContextFixtureV1:
    """Opaque test leaf only; the production construction oracle is a TODO."""
    __slots__ = ("_token", "request_id")

    def __init__(self, token: object, request_id: str) -> None:
        if token is not _TRUSTED_REQUEST_CONTEXT_TEST_TOKEN or \
                not REQUEST_RE.fullmatch(request_id):
            raise TypeError("host-owned TrustedRequestContextV1 required")
        self._token = token
        self.request_id = request_id

    def __reduce__(self):
        raise TypeError("TrustedRequestContextV1 is not serializable")


def _request_context_fixture(execution_id: str,
                             generation: str = "live") -> \
        _TrustedRequestContextFixtureV1:
    return _TrustedRequestContextFixtureV1(
        _TRUSTED_REQUEST_CONTEXT_TEST_TOKEN,
        _fixture_request_id_value(execution_id, generation))


def _request_id_from_context(value: Any) -> str:
    if not isinstance(value, _TrustedRequestContextFixtureV1) or \
            value._token is not _TRUSTED_REQUEST_CONTEXT_TEST_TOKEN:
        raise TypeError("opaque TrustedRequestContextV1 capability required")
    return value.request_id


class _HostExecutionIdFixtureV1:
    __slots__ = ("_token", "execution_id")

    def __init__(self, token: object, execution_id: str) -> None:
        if token is not _HOST_EXECUTION_ID_TEST_TOKEN or \
                not EXEC_RE.fullmatch(execution_id):
            raise TypeError("host-owned ExecutionId required")
        self._token = token
        self.execution_id = execution_id

    def __reduce__(self):
        raise TypeError("host-owned ExecutionId is not serializable")


def _execution_id_fixture(execution_id: str) -> _HostExecutionIdFixtureV1:
    return _HostExecutionIdFixtureV1(
        _HOST_EXECUTION_ID_TEST_TOKEN, execution_id)


def _execution_id_from_host(value: Any) -> str:
    if not isinstance(value, _HostExecutionIdFixtureV1) or \
            value._token is not _HOST_EXECUTION_ID_TEST_TOKEN:
        raise TypeError("host-owned ExecutionId capability required")
    return value.execution_id


def _journal(contract: dict[str, Any], execution_id: str,
             lease: dict[str, Any], attempt: dict[str, Any],
             *, custody_state: str = "HELD_PREPARED",
             custody_revision: int = 1) -> dict[str, Any]:
    authority = _authority_context(contract)["fixture"]
    material = _custody_material(contract, execution_id, attempt)
    preparation = _json_cas_entry(
        attempt["projectId"], "CustodyPreparationMaterialV2", material)
    return {
        "schemaVersion": 3,
        "projectId": attempt["projectId"],
        "executionId": execution_id,
        "expectedAttemptRevision": attempt["revision"],
        "frozenAttemptCasRef": attempt["frozenAttemptCasRef"],
        "evaluationAuthoritySealRef": attempt["evaluationAuthoritySealRef"],
        "evaluationAuthorityAdmissionCasRef":
            attempt["evaluationAuthorityAdmissionCasRef"],
        "semanticEvidenceCasRef": attempt["semanticEvidenceCasRef"],
        "frozenRetentionTargetRef": attempt["frozenRetentionTargetRef"],
        "rawProofInventoryCasRef": authority["rawProofInventoryCasRef"],
        "custodyPreparationRef": preparation["recordCasRef"],
        "custodyState": custody_state,
        "custodyRevision": custody_revision,
        "leaseId": lease["leaseId"],
        "ownerId": lease["ownerId"],
        "ownerLivenessToken": lease["ownerLivenessToken"],
        "fencingToken": lease["fencingToken"],
        "pinnedRefs": copy.deepcopy(_rt_context()["pinRefs"]),
    }


def _prepare(state: _DurableProjectStateV2, contract: dict[str, Any],
             execution_id: str, *, owner_generation: str = "live") -> None:
    snapshot = _begin(state, contract)
    expected_attempt = _attempt(contract, execution_id)
    attempts = [row for row in snapshot.content["attempts"]
                if row.get("executionId") == execution_id]
    journals = [row for row in snapshot.content["journals"]
                if row.get("executionId") == execution_id]
    all_journals = snapshot.content["journals"]
    owner_id, liveness = _owner_identity(execution_id, owner_generation)
    if journals:
        journal = _validate_journal(journals[0], snapshot.content["projectId"])
        lease = snapshot.content["rtState"].get("lease")
        if attempts == [expected_attempt] and len(journals) == 1 and \
                journal["custodyState"] == "HELD_PREPARED" and \
                journal["ownerId"] == owner_id and \
                journal["ownerLivenessToken"] == liveness and \
                isinstance(lease, dict) and \
                lease["expiresAtSequence"] == lease["acquiredAtSequence"] + 1 and \
                journal == _journal(
                    contract, execution_id, lease, expected_attempt):
            return
        raise LedgerCorrupt("same-execution preparation is not insert-or-exact")
    if all_journals:
        raise BusyTimeout("project custody journal serializes finalization")
    if attempts and attempts != [expected_attempt]:
        raise LedgerCorrupt("same-execution Attempt preparation collision")
    rt_state = snapshot.content["rtState"]
    at_sequence = rt_state["ledgerSequence"] + 1
    next_fence = rt_state["lastIssuedFencingToken"] + 1
    lease_id = _operational_id(
        "lease1", execution_id, owner_generation, str(next_fence))
    event = {
        "kind": "resolve-and-pin",
        "projectId": snapshot.content["projectId"],
        "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
        "atSequence": at_sequence,
        "leaseId": lease_id,
        "ownerId": owner_id,
        "ownerLivenessToken": liveness,
        "expectedPreviousFencingToken": rt_state["lastIssuedFencingToken"],
        "expiresAtSequence": at_sequence + 1,
        "pinRefs": copy.deepcopy(_rt_context()["pinRefs"]),
    }
    reduced = _reduce_rt(rt_state, event, snapshot.content["projectId"])
    if _rt_error(reduced["result"]) == "REQUEST.UNSATISFIABLE":
        raise CustodyUnavailable("RT13 authoritative object set is unavailable")
    if reduced["result"].get("kind") != "LEASE_GRANTED" or \
            reduced["result"].get("fencingToken") != next_fence:
        raise BusyTimeout("RT13 resolve-and-pin did not grant exact custody")
    snapshot.content["rtState"] = reduced["state"]
    lease = reduced["state"]["lease"]
    _cas_put(snapshot.content["privateCas"], _attempt_entry(expected_attempt))
    for entry in _custody_row_entries(contract):
        _cas_put(snapshot.content["privateCas"], entry)
    material = _custody_material(contract, execution_id, expected_attempt)
    _cas_put(snapshot.content["privateCas"], _json_cas_entry(
        snapshot.content["projectId"], "CustodyPreparationMaterialV2",
        material))
    if not attempts:
        snapshot.content["attempts"].append(expected_attempt)
    snapshot.content["journals"].append(_journal(
        contract, execution_id, lease, expected_attempt))
    _commit(state, snapshot, contract)


def _classify(content: dict[str, Any], contract: dict[str, Any],
              execution_id: str) -> str:
    _audit(content, contract)
    expected = _expected_records(contract, execution_id)
    finals = content["finalRecords"]
    shared = all(expected[name] in finals[name] for name in SHARED_R4)
    shared_any = any(expected[name] in finals[name] for name in SHARED_R4)
    link = expected["AttemptRunLinkV1"] in finals["AttemptRunLinkV1"]
    notifications = [row for row in finals["RunCommitNotificationV1"]
                     if row["executionId"] == execution_id and
                     row["runId"] == expected["RunIndexV1"]["runId"] and
                     row["runSealRef"] == expected["RunIndexV1"]["runSealRef"]]
    attempt = link and len(notifications) == 1
    attempt_any = link or bool(notifications)
    journals = [row for row in content["journals"]
                if row.get("executionId") == execution_id]
    if shared_any and not shared or attempt_any and not attempt or len(journals) > 1:
        raise LedgerCorrupt("target recovery state is partial or duplicate")
    journal = len(journals) == 1
    terminal_dispositions = [row for row in content["terminalFacts"]
                             ["AttemptTerminalDispositionV1"]
                             if row["executionId"] == execution_id]
    terminal_proofs = [row for row in content["terminalFacts"]
                       ["CustodyLossProofV1"]
                       if row["executionId"] == execution_id]
    terminal = len(terminal_dispositions) == 1 and len(terminal_proofs) == 1
    if not shared and not attempt and journal:
        return "NEW"
    if shared and not attempt and journal:
        return "CONVERGE"
    if shared and attempt and not journal:
        return "IDEMPOTENT_SUCCESS"
    if not attempt and not journal and terminal:
        return "CUSTODY_LOSS_FACTS"
    if not attempt and not journal and (not shared or shared):
        return "NO_PREPARED_RUN"
    raise LedgerCorrupt("target recovery state is outside the closed transition table")


def _custody_binding(content: dict[str, Any], execution_id: str) -> \
        tuple[dict[str, Any], dict[str, Any]]:
    journals = [row for row in content["journals"]
                if row["executionId"] == execution_id]
    if len(journals) != 1:
        raise LedgerCorrupt("exact target custody journal absent or duplicate")
    journal = journals[0]
    if journal["custodyState"] == "RECLAIMED_PENDING_REPIN":
        raise BusyTimeout("custody reclaim must repin before finalization")
    lease = content["rtState"].get("lease")
    if not isinstance(lease, dict) or lease.get("state") != "HELD" or \
            lease["leaseId"] != journal["leaseId"] or \
            lease["ownerId"] != journal["ownerId"] or \
            lease["ownerLivenessToken"] != journal["ownerLivenessToken"] or \
            lease["fencingToken"] != journal["fencingToken"] or \
            lease["expiresAtSequence"] != lease["acquiredAtSequence"] + 1 or \
            sorted(lease["pinnedRefs"], key=canonical) != _rt_context()["pinRefs"]:
        raise LedgerCorrupt("custody authority cannot be reconstructed from RT13 state")
    if lease["pendingExpiryRefs"]:
        raise CustodyPendingExpiry(
            "required pins became pending expiry after admission; D9 unresolved")
    object_states = {
        canonical({key: row[key] for key in (
            "projectId", "recordCasRef", "recordKind")}): row["state"]
        for row in content["rtState"]["objects"]
    }
    if any(object_states.get(canonical(ref)) != "AVAILABLE"
           for ref in _rt_context()["pinRefs"]):
        raise CustodyUnavailable("required RT13 object is no longer AVAILABLE")
    return journal, lease


def _finalize(state: _DurableProjectStateV2, contract: dict[str, Any],
              execution_id: str, request_context: Any,
              interleave: Callable[[_DurableProjectStateV2], None] | None = None,
              *, fail_transaction: bool = False,
              lose_response: bool = False) -> str:
    committer_request_id = _request_id_from_context(request_context)
    snapshot = _begin(state, contract)
    action = _classify(snapshot.content, contract, execution_id)
    if action == "IDEMPOTENT_SUCCESS":
        return action
    if action == "CUSTODY_LOSS_FACTS":
        raise CustodyUnavailable("typed custody-loss facts are available")
    if action == "NO_PREPARED_RUN":
        raise NoPreparedRun(execution_id)
    journal, lease = _custody_binding(snapshot.content, execution_id)
    writes = _expected_records(
        contract, execution_id, committer_request_id)
    if action == "NEW":
        for name in SHARED_R4:
            snapshot.content["finalRecords"][name].append(copy.deepcopy(writes[name]))
    for name in ATTEMPT_A2:
        snapshot.content["finalRecords"][name].append(copy.deepcopy(writes[name]))
    release = {
        "kind": "release",
        "projectId": snapshot.content["projectId"],
        "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
        "atSequence": snapshot.content["rtState"]["ledgerSequence"] + 1,
        "leaseId": journal["leaseId"],
        "ownerId": journal["ownerId"],
        "fencingToken": journal["fencingToken"],
    }
    reduced = _reduce_rt(
        snapshot.content["rtState"], release, snapshot.content["projectId"])
    if reduced["result"].get("kind") != "LEASE_RELEASED" or \
            reduced["result"].get("expiryAppliedRefs") != [] or \
            reduced["state"].get("lease", {}).get("state") != "RELEASED":
        raise LedgerCorrupt("RT13 release did not preserve exact committed custody")
    snapshot.content["rtState"] = reduced["state"]
    snapshot.content["journals"] = [
        row for row in snapshot.content["journals"]
        if row["executionId"] != execution_id
    ]
    if interleave is not None:
        interleave(state)
    if fail_transaction:
        raise CommitFailed("injected final transaction failure")
    _commit(state, snapshot, contract)
    if lose_response:
        raise ResponseLost("injected response loss after commit")
    return action


def _commit_run_v2(state: _DurableProjectStateV2,
                   contract: dict[str, Any], request_context: Any,
                   execution_id: Any, **kwargs: Any) -> str:
    execution = _execution_id_from_host(execution_id)
    return _finalize(
        state, contract, execution, request_context, **kwargs)


def _recover_run_v2(state: _DurableProjectStateV2,
                    contract: dict[str, Any], request_context: Any,
                    execution_id: Any) -> Any:
    _request_id_from_context(request_context)
    execution = _execution_id_from_host(execution_id)
    snapshot = _begin(state, contract)
    action = _classify(snapshot.content, contract, execution)
    if action == "CUSTODY_LOSS_FACTS":
        disposition = next(
            row for row in snapshot.content["terminalFacts"]
            ["AttemptTerminalDispositionV1"]
            if row["executionId"] == execution)
        proof = next(
            row for row in snapshot.content["terminalFacts"]["CustodyLossProofV1"]
            if row["executionId"] == execution)
        return {"disposition": copy.deepcopy(disposition),
                "lossProof": copy.deepcopy(proof)}
    return _finalize(state, contract, execution, request_context)


def _abort_custody(state: _DurableProjectStateV2,
                   contract: dict[str, Any], execution_id: str) -> None:
    """Release without publishing a Run; D9 classification stays external/TODO."""
    snapshot = _begin(state, contract)
    rows = [row for row in snapshot.content["journals"]
            if row["executionId"] == execution_id]
    if len(rows) != 1 or rows[0]["custodyState"] != "HELD_PREPARED":
        raise LedgerCorrupt("abort requires one exact HELD custody journal")
    journal = rows[0]
    event = {
        "kind": "release", "projectId": snapshot.content["projectId"],
        "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
        "atSequence": snapshot.content["rtState"]["ledgerSequence"] + 1,
        "leaseId": journal["leaseId"], "ownerId": journal["ownerId"],
        "fencingToken": journal["fencingToken"],
    }
    reduced = _reduce_rt(
        snapshot.content["rtState"], event, snapshot.content["projectId"])
    if reduced["result"].get("kind") != "LEASE_RELEASED":
        raise LedgerCorrupt("RT13 abort release failed")
    snapshot.content["rtState"] = reduced["state"]
    snapshot.content["journals"] = [
        row for row in snapshot.content["journals"]
        if row["executionId"] != execution_id]
    _commit(state, snapshot, contract)


def _record_custody_loss(state: _DurableProjectStateV2,
                         contract: dict[str, Any],
                         execution_id: str) -> dict[str, dict[str, Any]]:
    """Persist only recomputable pre-Run facts; D9 owns later termination."""
    snapshot = _begin(state, contract)
    rows = [row for row in snapshot.content["journals"]
            if row["executionId"] == execution_id]
    if len(rows) != 1:
        raise LedgerCorrupt("custody loss requires one exact journal")
    journal = rows[0]
    if journal["custodyState"] == "HELD_PREPARED":
        lease = snapshot.content["rtState"].get("lease")
        if not isinstance(lease, dict) or lease.get("state") != "HELD":
            raise LedgerCorrupt("HELD custody loss lacks reducer authority")
        release = {
            "kind": "release", "projectId": snapshot.content["projectId"],
            "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
            "atSequence": snapshot.content["rtState"]["ledgerSequence"] + 1,
            "leaseId": journal["leaseId"], "ownerId": journal["ownerId"],
            "fencingToken": journal["fencingToken"],
        }
        reduced = _reduce_rt(
            snapshot.content["rtState"], release, snapshot.content["projectId"])
        if reduced["result"].get("kind") != "LEASE_RELEASED":
            raise LedgerCorrupt("custody-loss release failed")
        snapshot.content["rtState"] = reduced["state"]
    elif journal["custodyState"] != "RECLAIMED_PENDING_REPIN" or \
            snapshot.content["rtState"].get("lease") is not None:
        raise LedgerCorrupt("custody loss state is not terminalizable")

    object_map = {
        canonical({key: row[key] for key in (
            "projectId", "recordCasRef", "recordKind")}): row
        for row in snapshot.content["rtState"]["objects"]
    }
    required_states = [copy.deepcopy(object_map[canonical(ref)])
                       for ref in _rt_context()["pinRefs"]]
    if all(row["state"] == "AVAILABLE" for row in required_states):
        raise LedgerCorrupt("custody loss facts require an unavailable required object")
    proof = {
        "schemaVersion": 1,
        "projectId": snapshot.content["projectId"],
        "executionId": execution_id,
        "cause": "required-custody-unavailable",
        "frozenAttemptCasRef": journal["frozenAttemptCasRef"],
        "custodyPreparationRef": journal["custodyPreparationRef"],
        "observedAtSequence": snapshot.content["rtState"]["ledgerSequence"],
        "requiredObjectStates": required_states,
    }
    disposition = {
        "schemaVersion": 1,
        "projectId": snapshot.content["projectId"],
        "executionId": execution_id,
        "disposition": "custody-lost-before-run",
        "custodyLossProofRef": sha_ref(canonical(proof)),
    }
    if any(row.get("executionId") == execution_id
           for name in FINAL_TYPES for row in snapshot.content["finalRecords"][name]):
        raise LedgerCorrupt("custody loss facts cannot coexist with Run records")
    snapshot.content["terminalFacts"]["CustodyLossProofV1"].append(proof)
    snapshot.content["terminalFacts"]["AttemptTerminalDispositionV1"].append(
        disposition)
    snapshot.content["journals"] = [
        row for row in snapshot.content["journals"]
        if row["executionId"] != execution_id]
    _commit(state, snapshot, contract)
    return {"disposition": disposition, "lossProof": proof}


_DEAD_OBSERVATION_TOKEN = object()


class _DeadOwnerObservationV1:
    __slots__ = (
        "_token", "project_id", "execution_id", "lease_id", "owner_id",
        "liveness", "fence")

    def __init__(self, token: object, journal: dict[str, Any]) -> None:
        if token is not _DEAD_OBSERVATION_TOKEN:
            raise TypeError("host-owned dead-owner observation required")
        self._token = token
        self.project_id = journal["projectId"]
        self.execution_id = journal["executionId"]
        self.lease_id = journal["leaseId"]
        self.owner_id = journal["ownerId"]
        self.liveness = journal["ownerLivenessToken"]
        self.fence = journal["fencingToken"]

    def __reduce__(self):
        raise TypeError("host liveness observation is not serializable")


def _observe_dead_owner_for_test(state: _DurableProjectStateV2,
                                 contract: dict[str, Any],
                                 execution_id: str) -> _DeadOwnerObservationV1:
    snapshot = _begin(state, contract)
    rows = [row for row in snapshot.content["journals"]
            if row["executionId"] == execution_id]
    if len(rows) != 1 or rows[0]["custodyState"] != "HELD_PREPARED":
        raise LedgerCorrupt("no exact HELD owner to observe")
    return _DeadOwnerObservationV1(_DEAD_OBSERVATION_TOKEN, rows[0])


def _reclaim_to_pending(state: _DurableProjectStateV2,
                        contract: dict[str, Any], execution_id: str,
                        observation: Any) -> None:
    if not isinstance(observation, _DeadOwnerObservationV1) or \
            observation._token is not _DEAD_OBSERVATION_TOKEN:
        raise TypeError("host-owned dead-owner observation required")
    snapshot = _begin(state, contract)
    rows = [row for row in snapshot.content["journals"]
            if row["executionId"] == execution_id]
    if len(rows) != 1:
        raise LedgerCorrupt("reclaim target journal absent or duplicate")
    journal = rows[0]
    expected_observation = (
        journal["projectId"], journal["executionId"], journal["leaseId"],
        journal["ownerId"], journal["ownerLivenessToken"],
        journal["fencingToken"])
    actual_observation = (
        observation.project_id, observation.execution_id,
        observation.lease_id, observation.owner_id, observation.liveness,
        observation.fence)
    if actual_observation != expected_observation:
        raise LedgerCorrupt("dead-owner observation does not bind exact journal")
    if journal["custodyState"] == "RECLAIMED_PENDING_REPIN":
        return
    lease = snapshot.content["rtState"].get("lease")
    next_sequence = snapshot.content["rtState"]["ledgerSequence"] + 1
    if not isinstance(lease, dict) or lease.get("state") != "HELD" or \
            next_sequence < lease["expiresAtSequence"]:
        raise LedgerCorrupt(
            "lease is not reclaimable at the reducer's next eligible sequence")
    event = {
        "kind": "crash-reclaim",
        "projectId": journal["projectId"],
        "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
        "atSequence": next_sequence,
        "leaseId": journal["leaseId"],
        "expectedOwnerId": journal["ownerId"],
        "expectedOwnerLivenessToken": journal["ownerLivenessToken"],
        "expectedFencingToken": journal["fencingToken"],
        "scopeRefs": copy.deepcopy(journal["pinnedRefs"]),
        "observedOwnerAlive": False,
    }
    reduced = _reduce_rt(
        snapshot.content["rtState"], event, snapshot.content["projectId"])
    if reduced["result"].get("kind") != "LEASE_RECLAIMED" or \
            reduced["state"].get("lease") is not None:
        raise LedgerCorrupt("RT13 did not produce exact reclaimed state")
    snapshot.content["rtState"] = reduced["state"]
    journal["custodyState"] = "RECLAIMED_PENDING_REPIN"
    journal["custodyRevision"] += 1
    _commit(state, snapshot, contract)


def _repin_after_reclaim(state: _DurableProjectStateV2,
                         contract: dict[str, Any], execution_id: str,
                         *, owner_generation: str = "recovery",
                         interleave: Callable[[_DurableProjectStateV2], None] | None = None) -> None:
    snapshot = _begin(state, contract)
    rows = [row for row in snapshot.content["journals"]
            if row["executionId"] == execution_id]
    if len(rows) != 1:
        raise LedgerCorrupt("repin target journal absent or duplicate")
    journal = rows[0]
    if journal["custodyState"] == "HELD_PREPARED":
        return
    rt_state = snapshot.content["rtState"]
    if rt_state.get("lease") is not None or \
            rt_state["lastIssuedFencingToken"] != journal["fencingToken"]:
        raise LedgerCorrupt("repin does not start from exact reclaimed fence")
    owner_id, liveness = _owner_identity(execution_id, owner_generation)
    at_sequence = rt_state["ledgerSequence"] + 1
    next_fence = rt_state["lastIssuedFencingToken"] + 1
    event = {
        "kind": "resolve-and-pin",
        "projectId": snapshot.content["projectId"],
        "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
        "atSequence": at_sequence,
        "leaseId": _operational_id(
            "lease1", execution_id, owner_generation, str(next_fence)),
        "ownerId": owner_id,
        "ownerLivenessToken": liveness,
        "expectedPreviousFencingToken": rt_state["lastIssuedFencingToken"],
        "expiresAtSequence": at_sequence + 1,
        "pinRefs": copy.deepcopy(_rt_context()["pinRefs"]),
    }
    reduced = _reduce_rt(rt_state, event, snapshot.content["projectId"])
    if reduced["result"].get("kind") != "LEASE_GRANTED" or \
            reduced["result"].get("fencingToken") != next_fence:
        raise CustodyUnavailable("fresh RT13 repin did not grant exact authority")
    old_revision = journal["custodyRevision"]
    snapshot.content["rtState"] = reduced["state"]
    replacement = copy.deepcopy(journal)
    new_lease = reduced["state"]["lease"]
    replacement.update({
        "custodyState": "HELD_PREPARED",
        "custodyRevision": old_revision + 1,
        "leaseId": new_lease["leaseId"],
        "ownerId": new_lease["ownerId"],
        "ownerLivenessToken": new_lease["ownerLivenessToken"],
        "fencingToken": new_lease["fencingToken"],
        "pinnedRefs": copy.deepcopy(_rt_context()["pinRefs"]),
    })
    snapshot.content["journals"] = [replacement]
    if interleave is not None:
        interleave(state)
    _commit(state, snapshot, contract)


def _apply_rt_event(state: _DurableProjectStateV2,
                    contract: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    snapshot = _begin(state, contract)
    reduced = _reduce_rt(
        snapshot.content["rtState"], event, snapshot.content["projectId"])
    # Rejections never consume a sequence or mutate the project revision.
    if reduced["result"].get("kind") == "D9":
        return reduced["result"]
    snapshot.content["rtState"] = reduced["state"]
    _commit(state, snapshot, contract)
    return reduced["result"]


def _atomic_concurrent_change(state: _DurableProjectStateV2,
                              contract: dict[str, Any],
                              mutate: Callable[[dict[str, Any]], None]) -> None:
    candidate = copy.deepcopy(state.content)
    mutate(candidate)
    _audit(candidate, contract)
    state.content = candidate
    state.project_revision += 1


def _public_snapshot(state: _DurableProjectStateV2) -> dict[str, Any]:
    return {
        "projectRevision": state.project_revision,
        "finalRecords": copy.deepcopy(state.content["finalRecords"]),
    }


def _raw_state_snapshot(state: _DurableProjectStateV2) -> dict[str, Any]:
    return {
        "projectRevision": state.project_revision,
        "contentDigest": sha_ref(canonical(state.content)),
        "content": copy.deepcopy(state.content),
    }


def _extra_rt_object(project: str, marker: str) -> dict[str, Any]:
    return {
        "projectId": project,
        "recordCasRef": "sha256:" + hashlib.sha256(
            marker.encode("utf-8")).hexdigest(),
        "recordKind": "unrelated-project-object",
        "state": "AVAILABLE",
    }


def _trace_snapshot(state: _DurableProjectStateV2) -> dict[str, Any]:
    return {
        "projectRevision": state.project_revision,
        "projectId": state.content["projectId"],
        "attempts": copy.deepcopy(state.content["attempts"]),
        "journals": copy.deepcopy(state.content["journals"]),
        "rtState": copy.deepcopy(state.content["rtState"]),
        "terminalFacts": copy.deepcopy(state.content["terminalFacts"]),
        "finalRecords": copy.deepcopy(state.content["finalRecords"]),
    }


def export_op6_recovery_custody_traces(
        contract: dict[str, Any]) -> dict[str, Any]:
    """Raw, token-free records for OP6 recomputation; no pass/fail oracle."""
    normal = _empty_state(contract)
    normal_steps = [{"operation": "initial", "state": _trace_snapshot(normal)}]
    _prepare(normal, contract, "exec1-trace-commit")
    normal_steps.append({
        "operation": "prepare_run_commit_v3",
        "state": _trace_snapshot(normal),
    })
    live_context = _request_context_fixture("exec1-trace-commit")
    _commit_run_v2(
        normal, contract, live_context,
        _execution_id_fixture("exec1-trace-commit"))
    normal_steps.append({
        "operation": "commit_run_v2",
        "trustedRequestContextLeaf": {
            "committerRequestId": live_context.request_id,
            "authority": "TEST-FIXTURE-ONLY; production leaf pending",
        },
        "state": _trace_snapshot(normal),
    })

    delayed = _empty_state(contract)
    delayed.content["rtState"]["objects"] += [
        _extra_rt_object(delayed.content["projectId"], "trace-extra-a"),
        _extra_rt_object(delayed.content["projectId"], "trace-extra-b"),
    ]
    delayed_steps = [{"operation": "initial", "state": _trace_snapshot(delayed)}]
    _prepare(delayed, contract, "exec1-trace-recovery")
    observation = _observe_dead_owner_for_test(
        delayed, contract, "exec1-trace-recovery")
    delayed_steps.append({"operation": "prepare", "state": _trace_snapshot(delayed)})
    for index, kind in enumerate(("expiry", "purge")):
        target = copy.deepcopy(delayed.content["rtState"]["objects"][23 + index])
        target.pop("state")
        event = {
            "kind": kind, "projectId": delayed.content["projectId"],
            "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
            "atSequence": delayed.content["rtState"]["ledgerSequence"] + 1,
            "targetRefs": [target],
        }
        result = _apply_rt_event(delayed, contract, event)
        delayed_steps.append({
            "operation": "rt13-event", "event": event,
            "reducerResult": result, "state": _trace_snapshot(delayed),
        })
    _reclaim_to_pending(
        delayed, contract, "exec1-trace-recovery", observation)
    delayed_steps.append({
        "operation": "crash-reclaim", "state": _trace_snapshot(delayed)})
    _repin_after_reclaim(
        delayed, contract, "exec1-trace-recovery",
        owner_generation="trace-recovery")
    delayed_steps.append({
        "operation": "repin", "state": _trace_snapshot(delayed)})

    loss = _empty_state(contract)
    _prepare(loss, contract, "exec1-trace-loss")
    loss_observation = _observe_dead_owner_for_test(
        loss, contract, "exec1-trace-loss")
    target = copy.deepcopy(_rt_context()["pinRefs"][0])
    expiry = {
        "kind": "expiry", "projectId": loss.content["projectId"],
        "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
        "atSequence": loss.content["rtState"]["ledgerSequence"] + 1,
        "targetRefs": [target],
    }
    expiry_result = _apply_rt_event(loss, contract, expiry)
    _reclaim_to_pending(loss, contract, "exec1-trace-loss", loss_observation)
    before_loss = _trace_snapshot(loss)
    facts = _record_custody_loss(loss, contract, "exec1-trace-loss")

    value = {
        "schemaVersion": 1,
        "assurance": "ARCHITECTURE-TEST-DOUBLE-RAW-TRACE",
        "authority": {
            "projectId": normal.content["projectId"],
            "requiredPinRefs": copy.deepcopy(_rt_context()["pinRefs"]),
            "unitIds": copy.deepcopy(_rt_context()["unitIds"]),
            "frozenRetentionTarget": copy.deepcopy(
                _authority_context(contract)["frozenTarget"]),
            "requiredCustodyRows": _custody_row_materials(contract),
            "requiredCustodyRowCas": sorted(
                _custody_row_entries(contract), key=lambda row: row["recordCasRef"]),
        },
        "scenarios": [
            {"id": "commit", "steps": normal_steps},
            {"id": "delayed-reclaim", "steps": delayed_steps},
            {"id": "custody-loss", "steps": [
                {"operation": "expiry", "event": expiry,
                 "reducerResult": expiry_result},
                {"operation": "reclaimed", "state": before_loss},
                {"operation": "terminal-facts", "facts": facts,
                 "state": _trace_snapshot(loss)},
            ]},
        ],
    }
    if _has_token_key(value) or any(
            text in {"pass", "passed", "verified", "pinned"}
            for text in _walk_strings(value)):
        raise LedgerCorrupt("OP6 trace export contains token/pass-booleans")
    return value


def run_authority_repair_probes(contract: dict[str, Any]) -> dict[str, Any]:
    project = contract["acceptedGolden"]["values"]["projectId"]

    base = _empty_state(contract)
    _prepare(base, contract, "exec1-extra-baseline")
    _finalize(base, contract, "exec1-extra-baseline",
              _request_context_fixture("exec1-extra-baseline"))
    baseline_final = copy.deepcopy(base.content["finalRecords"])

    extra = _empty_state(contract)
    extra.content["rtState"]["objects"].append(
        _extra_rt_object(project, "extra-authority-neutral"))
    _prepare(extra, contract, "exec1-extra-baseline")
    extra_lease = copy.deepcopy(extra.content["rtState"]["lease"])
    _finalize(extra, contract, "exec1-extra-baseline",
              _request_context_fixture("exec1-extra-baseline"))
    inventory_superset = {
        "objectCount": len(extra.content["rtState"]["objects"]),
        "leasePinCount": len(extra_lease["pinnedRefs"]),
        "leasePins": extra_lease["pinnedRefs"],
        "unitIds": extra.content["finalRecords"]["RunCustodyRootV1"][0]["unitIds"],
        "sameFinalRecordsAsNoExtra": extra.content["finalRecords"] == baseline_final,
    }
    inventory_rejected = 0
    for mutate in (
            lambda c: c["rtState"]["objects"].pop(0),
            lambda c: c["rtState"]["objects"].append(
                copy.deepcopy(c["rtState"]["objects"][0])),
            lambda c: c["rtState"]["objects"][0].__setitem__(
                "projectId", "prj1-" + "f" * 64)):
        candidate = copy.deepcopy(_empty_state(contract).content)
        mutate(candidate)
        try:
            _audit(candidate, contract)
        except LedgerCorrupt:
            inventory_rejected += 1

    prepared = _empty_state(contract)
    _prepare(prepared, contract, "exec1-cas-attacks")
    cas_rejected = 0
    cas_mutations: list[Callable[[dict[str, Any]], None]] = []
    semantic_ref = _authority_context(contract)["fixture"]["semanticEvidenceCasRef"]
    cas_mutations.append(lambda c: c["privateCas"].__setitem__(
        slice(None), [row for row in c["privateCas"]
                      if row["recordCasRef"] != semantic_ref]))
    cas_mutations.append(lambda c: c["privateCas"].append(
        copy.deepcopy(c["privateCas"][0])))
    cas_mutations.append(lambda c: c["privateCas"][0].__setitem__("unknown", 1))
    cas_mutations.append(lambda c: c["privateCas"][0].__setitem__(
        "recordBytesHex", c["privateCas"][0]["recordBytesHex"] + "00"))
    cas_mutations.append(lambda c: c["privateCas"][0].__setitem__(
        "recordKind", "SemanticEvidenceV1"))
    cas_mutations.append(lambda c: c["privateCas"][0].__setitem__(
        "projectId", "prj1-" + "f" * 64))

    def noncanonical_attempt(c: dict[str, Any]) -> None:
        attempt = c["attempts"][0]
        old_ref = attempt["frozenAttemptCasRef"]
        material = _attempt_material(attempt)
        raw = json.dumps(material, sort_keys=True, indent=1).encode("utf-8")
        entry = _cas_entry(project, "FrozenAttemptRecordV1", raw)
        c["privateCas"].append(entry)
        attempt["frozenAttemptCasRef"] = entry["recordCasRef"]
        journal = c["journals"][0]
        journal["frozenAttemptCasRef"] = entry["recordCasRef"]
        custody = _custody_material(contract, journal["executionId"], attempt)
        custody_entry = _json_cas_entry(
            project, "CustodyPreparationMaterialV2", custody)
        c["privateCas"].append(custody_entry)
        journal["custodyPreparationRef"] = custody_entry["recordCasRef"]
        assert old_ref != entry["recordCasRef"]
    cas_mutations.append(noncanonical_attempt)

    def coherent_semantic(c: dict[str, Any]) -> None:
        fixture = c["authorityFixture"]
        old = fixture["semanticEvidenceCasRef"]
        original = next(row for row in c["privateCas"]
                        if row["recordCasRef"] == old)
        replacement = _cas_entry(
            project, "SemanticEvidenceV1",
            bytes.fromhex(original["recordBytesHex"]) + b"x")
        c["privateCas"].append(replacement)
        fixture["semanticEvidenceCasRef"] = replacement["recordCasRef"]
        c["attempts"][0]["semanticEvidenceCasRef"] = replacement["recordCasRef"]
        c["journals"][0]["semanticEvidenceCasRef"] = replacement["recordCasRef"]
    cas_mutations.append(coherent_semantic)

    def coherent_custody_row(c: dict[str, Any]) -> None:
        journal = c["journals"][0]
        material_entry = next(row for row in c["privateCas"]
                              if row["recordCasRef"] == journal["custodyPreparationRef"])
        material = _decode_canonical_json(material_entry, "material")
        old_ref = material["requiredRowCasRefs"][0]
        row_entry = next(row for row in c["privateCas"]
                         if row["recordCasRef"] == old_ref)
        row = _decode_canonical_json(row_entry, "row")
        row["requiredForCapability"] = (
            "replayable" if row["requiredForCapability"] == "verifiable"
            else "verifiable")
        replacement = _json_cas_entry(project, "CustodyPreparedObjectV2", row)
        c["privateCas"].append(replacement)
        material["requiredRowCasRefs"][0] = replacement["recordCasRef"]
        material["requiredRowCasRefs"].sort()
        replacement_material = _json_cas_entry(
            project, "CustodyPreparationMaterialV2", material)
        c["privateCas"].append(replacement_material)
        journal["custodyPreparationRef"] = replacement_material["recordCasRef"]
    cas_mutations.append(coherent_custody_row)

    def coherent_material(c: dict[str, Any]) -> None:
        journal = c["journals"][0]
        entry = next(row for row in c["privateCas"]
                     if row["recordCasRef"] == journal["custodyPreparationRef"])
        material = _decode_canonical_json(entry, "material")
        material["units"] = list(reversed(material["units"]))
        replacement = _json_cas_entry(
            project, "CustodyPreparationMaterialV2", material)
        c["privateCas"].append(replacement)
        journal["custodyPreparationRef"] = replacement["recordCasRef"]
    cas_mutations.append(coherent_material)

    for mutate in cas_mutations:
        candidate = copy.deepcopy(prepared.content)
        mutate(candidate)
        try:
            _audit(candidate, contract)
        except (LedgerCorrupt, AssertionError):
            cas_rejected += 1

    delayed = _empty_state(contract)
    delayed.content["rtState"]["objects"] += [
        _extra_rt_object(project, "delayed-extra-a"),
        _extra_rt_object(project, "delayed-extra-b"),
    ]
    _prepare(delayed, contract, "exec1-delayed-reclaim")
    delayed_observation = _observe_dead_owner_for_test(
        delayed, contract, "exec1-delayed-reclaim")
    for index, kind in enumerate(("expiry", "purge")):
        ref = {key: delayed.content["rtState"]["objects"][23 + index][key]
               for key in ("projectId", "recordCasRef", "recordKind")}
        _apply_rt_event(delayed, contract, {
            "kind": kind, "projectId": project,
            "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
            "atSequence": delayed.content["rtState"]["ledgerSequence"] + 1,
            "targetRefs": [ref],
        })
    delayed_before = delayed.content["rtState"]["ledgerSequence"]
    _reclaim_to_pending(
        delayed, contract, "exec1-delayed-reclaim", delayed_observation)
    delayed_after = delayed.content["rtState"]["ledgerSequence"]

    loss = _empty_state(contract)
    _prepare(loss, contract, "exec1-required-expiry-loss")
    loss_observation = _observe_dead_owner_for_test(
        loss, contract, "exec1-required-expiry-loss")
    _apply_rt_event(loss, contract, {
        "kind": "expiry", "projectId": project,
        "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
        "atSequence": loss.content["rtState"]["ledgerSequence"] + 1,
        "targetRefs": [copy.deepcopy(_rt_context()["pinRefs"][0])],
    })
    _reclaim_to_pending(
        loss, contract, "exec1-required-expiry-loss", loss_observation)
    repin_unavailable = ""
    try:
        _repin_after_reclaim(
            loss, contract, "exec1-required-expiry-loss")
    except CustodyUnavailable as exc:
        repin_unavailable = type(exc).__name__
    facts = _record_custody_loss(
        loss, contract, "exec1-required-expiry-loss")
    loss_after_facts = _raw_state_snapshot(loss)
    recovered_facts = _recover_run_v2(
        loss, contract,
        _request_context_fixture("exec1-required-expiry-loss", "recovery"),
        _execution_id_fixture("exec1-required-expiry-loss"))
    facts_replay_unchanged = (
        recovered_facts == facts and _raw_state_snapshot(loss) == loss_after_facts)
    fact_strings = set(_walk_strings(facts))

    patch_only = _empty_state(contract)
    _prepare(patch_only, contract, "exec1-repin-patch")
    patch_observation = _observe_dead_owner_for_test(
        patch_only, contract, "exec1-repin-patch")
    _reclaim_to_pending(
        patch_only, contract, "exec1-repin-patch", patch_observation)
    before_journal = copy.deepcopy(patch_only.content["journals"][0])
    _repin_after_reclaim(patch_only, contract, "exec1-repin-patch")
    after_journal = copy.deepcopy(patch_only.content["journals"][0])
    mutable_fields = {
        "custodyState", "custodyRevision", "leaseId", "ownerId",
        "ownerLivenessToken", "fencingToken", "pinnedRefs",
    }
    immutable_preserved = all(
        before_journal[key] == after_journal[key]
        for key in set(before_journal) - mutable_fields)

    corrupt_retry = _empty_state(contract)
    _prepare(corrupt_retry, contract, "exec1-repin-cas")
    corrupt_observation = _observe_dead_owner_for_test(
        corrupt_retry, contract, "exec1-repin-cas")
    _reclaim_to_pending(
        corrupt_retry, contract, "exec1-repin-cas", corrupt_observation)
    stale_refusal = ""
    def inject_corrupt_authority(current: _DurableProjectStateV2) -> None:
        current.content["journals"][0]["semanticEvidenceCasRef"] = \
            "sha256:" + "fe" * 32
        current.project_revision += 1
    try:
        _repin_after_reclaim(
            corrupt_retry, contract, "exec1-repin-cas",
            interleave=inject_corrupt_authority)
    except BusyTimeout as exc:
        stale_refusal = type(exc).__name__
    retry_audit = ""
    try:
        _repin_after_reclaim(corrupt_retry, contract, "exec1-repin-cas")
    except LedgerCorrupt as exc:
        retry_audit = type(exc).__name__

    notification = _empty_state(contract)
    _prepare(notification, contract, "exec1-notification-race")
    loser_context = _request_context_fixture(
        "exec1-notification-race", "loser")
    winner_context = _request_context_fixture(
        "exec1-notification-race", "winner")
    loser_stale = ""
    try:
        _finalize(
            notification, contract, "exec1-notification-race", loser_context,
            interleave=lambda current: _finalize(
                current, contract, "exec1-notification-race", winner_context))
    except BusyTimeout as exc:
        loser_stale = type(exc).__name__
    replay = _finalize(
        notification, contract, "exec1-notification-race", loser_context)
    notification_rows = notification.content["finalRecords"][
        "RunCommitNotificationV1"]
    raw_context_rejected = ""
    raw_before = _raw_state_snapshot(notification)
    try:
        _commit_run_v2(
            notification, contract, loser_context.request_id,
            _execution_id_fixture("exec1-notification-race"))
    except TypeError as exc:
        if _raw_state_snapshot(notification) == raw_before:
            raw_context_rejected = type(exc).__name__
    raw_execution_rejected = ""
    try:
        _commit_run_v2(
            notification, contract, loser_context,
            "exec1-notification-race")
    except TypeError as exc:
        if _raw_state_snapshot(notification) == raw_before:
            raw_execution_rejected = type(exc).__name__

    traces = export_op6_recovery_custody_traces(contract)
    return {
        "inventorySuperset": inventory_superset,
        "inventoryNegativeCases": {
            "cases": 3, "rejected": inventory_rejected},
        "privateCasNegativeCases": {
            "cases": len(cas_mutations), "rejected": cas_rejected},
        "delayedReclaim": {
            "sequenceBeforeReclaim": delayed_before,
            "sequenceAfterReclaim": delayed_after,
            "journalState": delayed.content["journals"][0]["custodyState"],
        },
        "custodyLossFacts": {
            "repinOutcome": repin_unavailable,
            "disposition": facts["disposition"],
            "lossProof": facts["lossProof"],
            "recoveryReturnsExactFactsUnchanged": facts_replay_unchanged,
            "forbiddenD9OrRunFields": sorted(
                fact_strings & {"class", "errorCode", "exitCode",
                                "runId", "runSealRef"}),
            "finalRecordCount": sum(
                len(rows) for rows in loss.content["finalRecords"].values()),
        },
        "repinPatch": {
            "immutablePreserved": immutable_preserved,
            "changedFields": sorted(
                key for key in before_journal
                if before_journal[key] != after_journal[key]),
            "staleCasOutcome": stale_refusal,
            "retryAuditOutcome": retry_audit,
        },
        "notification": {
            "loserFirstOutcome": loser_stale,
            "loserReplayOutcome": replay,
            "rows": copy.deepcopy(notification_rows),
            "winnerRequestId": winner_context.request_id,
            "loserRequestId": loser_context.request_id,
            "rawContextOutcome": raw_context_rejected,
            "rawExecutionOutcome": raw_execution_rejected,
        },
        "op6Trace": {
            "scenarioIds": [row["id"] for row in traces["scenarios"]],
            "authority": traces["authority"],
        },
    }


def run_rt13_custody_probes(contract: dict[str, Any]) -> dict[str, Any]:
    ctx = _rt_context()
    authority_ok = (
        len(ctx["pinRefs"]) == 23 and ctx["unitIds"] == UNIT_IDS and
        ctx["derived"]["closureCommitment"] ==
        "sha256:156ac0017a65c026a2e939c728fc189aa81728ad827c2218e1b4ccce8924c626")

    acquire = _empty_state(contract)
    _prepare(acquire, contract, "exec1-rt-acquire")
    acquire_before_retry = _raw_state_snapshot(acquire)
    lease = acquire.content["rtState"]["lease"]
    _prepare(acquire, contract, "exec1-rt-acquire")
    acquire_retry_ok = (
        _raw_state_snapshot(acquire) == acquire_before_retry and
        lease["expiresAtSequence"] == lease["acquiredAtSequence"] + 1 and
        len(lease["pinnedRefs"]) == 23 and
        acquire.content["journals"][0]["fencingToken"] == lease["fencingToken"])
    horizon_rejections = 0
    for replacement in (
            lease["acquiredAtSequence"] + 2,
            lease["acquiredAtSequence"] + 1000,
            "2026-08-01T00:00:00Z"):
        candidate = _DurableProjectStateV2(
            _STATE_TOKEN, copy.deepcopy(acquire.content))
        candidate.content["rtState"]["lease"]["expiresAtSequence"] = replacement
        before = _raw_state_snapshot(candidate)
        try:
            _finalize(candidate, contract, "exec1-rt-acquire",
                      _request_context_fixture("exec1-rt-acquire"))
        except (LedgerCorrupt, TypeError, ValueError):
            if _raw_state_snapshot(candidate) == before:
                horizon_rejections += 1

    failed = _empty_state(contract)
    _prepare(failed, contract, "exec1-rt-txn-fail")
    failed_before = _raw_state_snapshot(failed)
    failure_unchanged = False
    try:
        _finalize(
            failed, contract, "exec1-rt-txn-fail",
            _request_context_fixture("exec1-rt-txn-fail"),
            fail_transaction=True)
    except CommitFailed:
        failure_unchanged = _raw_state_snapshot(failed) == failed_before

    lost = _empty_state(contract)
    _prepare(lost, contract, "exec1-rt-response-lost")
    response_lost = False
    try:
        _finalize(
            lost, contract, "exec1-rt-response-lost",
            _request_context_fixture("exec1-rt-response-lost"),
            lose_response=True)
    except ResponseLost:
        response_lost = True
    lost_after = _raw_state_snapshot(lost)
    retry_action = _finalize(
        lost, contract, "exec1-rt-response-lost",
        _request_context_fixture("exec1-rt-response-lost", "retry"))
    response_retry_ok = (
        response_lost and retry_action == "IDEMPOTENT_SUCCESS" and
        _raw_state_snapshot(lost) == lost_after and
        lost.content["rtState"]["lease"]["state"] == "RELEASED" and
        lost.content["journals"] == [] and
        all(len(lost.content["finalRecords"][name]) == 1
            for name in FINAL_TYPES) and
        lost.content["finalRecords"]["RunCommitNotificationV1"][0]
        ["committerRequestId"] ==
        _request_context_fixture("exec1-rt-response-lost").request_id and
        lost.content["finalRecords"]["RunCustodyRootV1"][0]["unitIds"] ==
        ctx["unitIds"])

    pending = _empty_state(contract)
    _prepare(pending, contract, "exec1-rt-pending-expiry")
    pending_target = copy.deepcopy(ctx["pinRefs"][0])
    pending_event = {
        "kind": "expiry", "projectId": pending.content["projectId"],
        "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
        "atSequence": pending.content["rtState"]["ledgerSequence"] + 1,
        "targetRefs": [pending_target],
    }
    pending_result = _apply_rt_event(pending, contract, pending_event)
    pending_before_final = _raw_state_snapshot(pending)
    pending_blocked = False
    try:
        _finalize(pending, contract, "exec1-rt-pending-expiry",
                  _request_context_fixture("exec1-rt-pending-expiry"))
    except CustodyPendingExpiry:
        pending_blocked = (
            _raw_state_snapshot(pending) == pending_before_final and
            pending_result.get("kind") == "READ_CONTINUES" and
            pending.content["rtState"]["lease"]["pendingExpiryRefs"] ==
            [pending_target])
    _abort_custody(pending, contract, "exec1-rt-pending-expiry")
    pending_abort_released = (
        pending.content["journals"] == [] and
        pending.content["rtState"]["lease"]["state"] == "RELEASED" and
        pending.content["rtState"]["objects"][0]["state"] == "EXPIRED" and
        all(not pending.content["finalRecords"][name] for name in FINAL_TYPES))

    purge_held = _empty_state(contract)
    _prepare(purge_held, contract, "exec1-rt-purge-held")
    purge_before = _raw_state_snapshot(purge_held)
    purge_event = {
        "kind": "purge", "projectId": purge_held.content["projectId"],
        "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
        "atSequence": purge_held.content["rtState"]["ledgerSequence"] + 1,
        "targetRefs": [copy.deepcopy(ctx["pinRefs"][0])],
    }
    purge_result = _apply_rt_event(purge_held, contract, purge_event)
    purge_held_blocked = (
        _rt_error(purge_result) == "LEDGER.BUSY_TIMEOUT" and
        _raw_state_snapshot(purge_held) == purge_before)

    restart = _empty_state(contract)
    _prepare(restart, contract, "exec1-rt-restart")
    old_fence = restart.content["rtState"]["lastIssuedFencingToken"]
    observation = _observe_dead_owner_for_test(
        restart, contract, "exec1-rt-restart")
    _reclaim_to_pending(restart, contract, "exec1-rt-restart", observation)
    pending_gap = _raw_state_snapshot(restart)
    _reclaim_to_pending(restart, contract, "exec1-rt-restart", observation)
    reclaim_idempotent = _raw_state_snapshot(restart) == pending_gap
    contender_before = _raw_state_snapshot(restart)
    contender_blocked = False
    try:
        _prepare(restart, contract, "exec1-rt-contender")
    except BusyTimeout:
        contender_blocked = _raw_state_snapshot(restart) == contender_before
    _repin_after_reclaim(
        restart, contract, "exec1-rt-restart", owner_generation="fresh")
    repinned = restart.content["rtState"]["lease"]
    repin_ok = (
        restart.content["journals"][0]["custodyState"] == "HELD_PREPARED" and
        restart.content["journals"][0]["custodyRevision"] == 3 and
        repinned["fencingToken"] == old_fence + 1 and
        repinned["expiresAtSequence"] == repinned["acquiredAtSequence"] + 1)
    restart_action = _finalize(
        restart, contract, "exec1-rt-restart",
        _request_context_fixture("exec1-rt-restart", "recovery"))
    restart_committed = (
        restart_action == "NEW" and restart.content["journals"] == [] and
        restart.content["rtState"]["lease"]["state"] == "RELEASED")

    convergence = _empty_state(contract)
    _prepare(convergence, contract, "exec1-rt-first")
    busy_before = _raw_state_snapshot(convergence)
    busy = False
    try:
        _prepare(convergence, contract, "exec1-rt-second")
    except BusyTimeout:
        busy = _raw_state_snapshot(convergence) == busy_before
    _finalize(convergence, contract, "exec1-rt-first",
              _request_context_fixture("exec1-rt-first"))
    _prepare(convergence, contract, "exec1-rt-second")
    converged = _finalize(
        convergence, contract, "exec1-rt-second",
        _request_context_fixture("exec1-rt-second"))
    convergence_ok = (
        busy and converged == "CONVERGE" and
        len(convergence.content["finalRecords"]["RunCustodyRootV1"]) == 1 and
        len(convergence.content["finalRecords"]["AttemptRunLinkV1"]) == 2)

    wrong = _empty_state(contract)
    _prepare(wrong, contract, "exec1-rt-wrong")
    wrong_journal = wrong.content["journals"][0]
    base_event = {
        "kind": "crash-reclaim", "projectId": wrong.content["projectId"],
        "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
        "atSequence": wrong.content["rtState"]["ledgerSequence"] + 1,
        "leaseId": wrong_journal["leaseId"],
        "expectedOwnerId": wrong_journal["ownerId"],
        "expectedOwnerLivenessToken": wrong_journal["ownerLivenessToken"],
        "expectedFencingToken": wrong_journal["fencingToken"],
        "scopeRefs": copy.deepcopy(wrong_journal["pinnedRefs"]),
        "observedOwnerAlive": False,
    }
    wrong_rejections = 0
    wrong_cases: list[Callable[[dict[str, Any]], None]] = [
        lambda event: event.__setitem__("expectedOwnerId", "owner1:" + "f" * 32),
        lambda event: event.__setitem__("expectedOwnerLivenessToken", "live1:" + "f" * 32),
        lambda event: event.__setitem__("expectedFencingToken", event["expectedFencingToken"] + 1),
        lambda event: event.__setitem__("projectId", "prj1-" + "f" * 64),
        lambda event: event["scopeRefs"].pop(),
        lambda event: event.__setitem__("observedOwnerAlive", True),
    ]
    for mutate in wrong_cases:
        event = copy.deepcopy(base_event)
        mutate(event)
        before = canonical(wrong.content["rtState"])
        try:
            reduced = _reduce_rt(
                wrong.content["rtState"], event, wrong.content["projectId"])
            rejected = reduced["result"].get("kind") == "D9"
        except (LedgerCorrupt, ValueError):
            rejected = True
        if rejected and canonical(wrong.content["rtState"]) == before:
            wrong_rejections += 1

    reconstruction_rejections = 0
    for mutate in (
            lambda content: content["journals"][0].__setitem__(
                "ownerId", "owner1:" + "e" * 32),
            lambda content: content["journals"][0].__setitem__(
                "ownerLivenessToken", "live1:" + "e" * 32),
            lambda content: content["journals"][0].__setitem__(
                "fencingToken", content["journals"][0]["fencingToken"] + 1),
            lambda content: content["journals"][0].__setitem__(
                "projectId", "prj1-" + "e" * 64),
            lambda content: content["journals"][0]["pinnedRefs"].pop()):
        candidate = copy.deepcopy(wrong.content)
        mutate(candidate)
        try:
            _audit(candidate, contract)
        except LedgerCorrupt:
            reconstruction_rejections += 1

    malformed_journals = 0
    cross_attempt = copy.deepcopy(wrong.content)
    cross_attempt["journals"][0]["executionId"] = "exec1-other-attempt"
    duplicate = copy.deepcopy(wrong.content)
    duplicate["journals"].append(copy.deepcopy(duplicate["journals"][0]))
    for candidate in (cross_attempt, duplicate):
        try:
            _audit(candidate, contract)
        except LedgerCorrupt:
            malformed_journals += 1

    unavailable_rejections = 0
    for state_name in ("PURGED", "EXPIRED"):
        unavailable = _empty_state(contract)
        unavailable.content["rtState"]["objects"][0]["state"] = state_name
        before = _raw_state_snapshot(unavailable)
        try:
            _prepare(unavailable, contract, f"exec1-rt-{state_name.lower()}")
        except CustodyUnavailable:
            if _raw_state_snapshot(unavailable) == before:
                unavailable_rejections += 1
    missing = _empty_state(contract)
    missing.content["rtState"]["objects"].pop()
    missing_before = _raw_state_snapshot(missing)
    try:
        _prepare(missing, contract, "exec1-rt-missing")
    except LedgerCorrupt:
        if _raw_state_snapshot(missing) == missing_before:
            unavailable_rejections += 1

    after_release = _empty_state(contract)
    _prepare(after_release, contract, "exec1-rt-after-release")
    _finalize(after_release, contract, "exec1-rt-after-release",
              _request_context_fixture("exec1-rt-after-release"))
    purge_after = {
        "kind": "purge", "projectId": after_release.content["projectId"],
        "transactionBoundary": "ONE_PROJECT_LEDGER_TRANSACTION",
        "atSequence": after_release.content["rtState"]["ledgerSequence"] + 1,
        "targetRefs": [copy.deepcopy(ctx["pinRefs"][0])],
    }
    purge_after_result = _apply_rt_event(after_release, contract, purge_after)
    purge_after_release = (
        purge_after_result.get("kind") == "PURGE_COMMITTED" and
        after_release.content["rtState"]["objects"][0]["state"] == "PURGED")

    return {
        "authority23": authority_ok,
        "acquireAndSameOwnerRetry": acquire_retry_ok,
        "horizonCases": {"cases": 3, "rejected": horizon_rejections},
        "transactionFailureUnchanged": failure_unchanged,
        "responseLossIdempotent": response_retry_ok,
        "pendingExpiryBlocksCommitUnchanged": pending_blocked,
        "pendingExpiryAbortReleased": pending_abort_released,
        "intersectingPurgeWhileHeldBlocked": purge_held_blocked,
        "reclaimPendingIdempotent": reclaim_idempotent,
        "contenderBlockedInReclaimGap": contender_blocked,
        "freshRepinNextFence": repin_ok,
        "restartCommittedReleased": restart_committed,
        "contenderThenConverges": convergence_ok,
        "wrongBindingCases": {"cases": 6, "rejected": wrong_rejections},
        "reconstructionCases": {"cases": 5, "rejected": reconstruction_rejections},
        "journalMismatchCases": {"cases": 2, "rejected": malformed_journals},
        "unavailableCases": {"cases": 3, "rejected": unavailable_rejections},
        "purgeAfterRelease": purge_after_release,
    }


def _rt13_probe_errors(result: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(result, dict):
        return ["RT13 custody probe root invalid"]
    booleans = [
        "authority23", "acquireAndSameOwnerRetry",
        "transactionFailureUnchanged", "responseLossIdempotent",
        "pendingExpiryBlocksCommitUnchanged",
        "pendingExpiryAbortReleased",
        "intersectingPurgeWhileHeldBlocked", "reclaimPendingIdempotent",
        "contenderBlockedInReclaimGap", "freshRepinNextFence",
        "restartCommittedReleased", "contenderThenConverges",
        "purgeAfterRelease",
    ]
    for key in booleans:
        if result.get(key) is not True:
            errors.append(f"RT13 custody probe failed: {key}")
    for key, count in (
            ("wrongBindingCases", 6), ("reconstructionCases", 5),
            ("journalMismatchCases", 2), ("unavailableCases", 3)):
        if result.get(key) != {"cases": count, "rejected": count}:
            errors.append(f"RT13 custody adversarial set failed: {key}")
    if result.get("horizonCases") != {"cases": 3, "rejected": 3}:
        errors.append("RT13 minimum sequence horizon substitutions escaped")
    return errors


def _authority_repair_probe_errors(result: Any) -> list[str]:
    if not isinstance(result, dict):
        return ["durable-authority repair probe root invalid"]
    errors: list[str] = []
    inventory = result.get("inventorySuperset") or {}
    if inventory.get("objectCount") != 24 or \
            inventory.get("leasePinCount") != 23 or \
            inventory.get("leasePins") != _rt_context()["pinRefs"] or \
            inventory.get("unitIds") != UNIT_IDS or \
            inventory.get("sameFinalRecordsAsNoExtra") is not True:
        errors.append("project RT inventory superset influenced Run authority")
    if result.get("inventoryNegativeCases") != {"cases": 3, "rejected": 3}:
        errors.append("project RT inventory closure negatives escaped")
    if result.get("privateCasNegativeCases") != {"cases": 10, "rejected": 10}:
        errors.append("typed private CAS authority negatives escaped")
    delayed = result.get("delayedReclaim") or {}
    if delayed != {
            "sequenceBeforeReclaim": 3, "sequenceAfterReclaim": 4,
            "journalState": "RECLAIMED_PENDING_REPIN"}:
        errors.append("delayed crash reclaim did not follow RT13 next-sequence truth")
    loss = result.get("custodyLossFacts") or {}
    if loss.get("repinOutcome") != "CustodyUnavailable" or \
            loss.get("forbiddenD9OrRunFields") != [] or \
            loss.get("finalRecordCount") != 0 or \
            loss.get("recoveryReturnsExactFactsUnchanged") is not True or \
            (loss.get("disposition") or {}).get("disposition") != \
            "custody-lost-before-run" or \
            (loss.get("lossProof") or {}).get("cause") != \
            "required-custody-unavailable":
        errors.append("custody-loss output is not FACTS-only/no-Run")
    repin = result.get("repinPatch") or {}
    if repin.get("immutablePreserved") is not True or \
            repin.get("changedFields") != [
                "custodyRevision", "custodyState", "fencingToken", "leaseId",
                "ownerId", "ownerLivenessToken"] or \
            repin.get("staleCasOutcome") != "BusyTimeout" or \
            repin.get("retryAuditOutcome") != "LedgerCorrupt":
        errors.append("repin overwrote immutable authority or skipped retry audit")
    notice = result.get("notification") or {}
    rows = notice.get("rows") or []
    if notice.get("loserFirstOutcome") != "BusyTimeout" or \
            notice.get("loserReplayOutcome") != "IDEMPOTENT_SUCCESS" or \
            notice.get("rawContextOutcome") != "TypeError" or len(rows) != 1 or \
            notice.get("rawExecutionOutcome") != "TypeError" or \
            rows[0].get("committerRequestId") != notice.get("winnerRequestId") or \
            rows[0].get("committerRequestId") == notice.get("loserRequestId"):
        errors.append("RunCommitNotification winner/replay/request authority failed")
    trace = result.get("op6Trace") or {}
    if trace.get("scenarioIds") != [
            "commit", "delayed-reclaim", "custody-loss"] or \
            (trace.get("authority") or {}).get("requiredPinRefs") != \
            _rt_context()["pinRefs"] or \
            len((trace.get("authority") or {}).get(
                "requiredCustodyRows", [])) != 23 or \
            len((trace.get("authority") or {}).get(
                "requiredCustodyRowCas", [])) != 23:
        errors.append("OP6 raw recovery/custody trace export incomplete")
    return errors


def run_foundation_probes(contract: dict[str, Any]) -> dict[str, Any]:
    project = contract["acceptedGolden"]["values"]["projectId"]
    other_project = "prj1-" + "b" * 64
    schema_rejections = 0
    base = _expected_records(contract, "exec1-schema")
    for name in FINAL_TYPES:
        for kind in ("unknown-field", "cross-project"):
            candidate = copy.deepcopy(base[name])
            if kind == "unknown-field":
                candidate["unknown"] = True
            else:
                candidate["projectId"] = other_project
            try:
                _validate_final(name, candidate, project, contract)
            except LedgerCorrupt:
                schema_rejections += 1

    state_cases = 0
    state_cases_passed = 0
    state_outcomes = {
        "NEW": 0, "NO_PREPARED_RUN": 0, "IDEMPOTENT_SUCCESS": 0,
        "LEDGER_CORRUPT_UNCHANGED": 0,
    }
    for journal_present in (False, True):
        for mask in range(0, 1 << len(FINAL_TYPES)):
            state = _empty_state(contract)
            execution = f"exec1-state-{int(journal_present)}-{mask}"
            writes = _expected_records(contract, execution)
            if journal_present:
                _prepare(state, contract, execution)
            for index, name in enumerate(FINAL_TYPES):
                if mask & (1 << index):
                    state.content["finalRecords"][name].append(writes[name])
            before = _raw_state_snapshot(state)
            state_cases += 1
            actual = ""
            try:
                actual = _finalize(
                    state, contract, execution,
                    _request_context_fixture(execution))
            except LedgerCorrupt:
                if _raw_state_snapshot(state) == before:
                    actual = "LEDGER_CORRUPT_UNCHANGED"
            except NoPreparedRun:
                if _raw_state_snapshot(state) == before:
                    actual = "NO_PREPARED_RUN"
            full_mask = (1 << len(FINAL_TYPES)) - 1
            if mask == 0 and journal_present:
                expected = "NEW"
            elif mask == 0 and not journal_present:
                expected = "NO_PREPARED_RUN"
            elif mask == full_mask and not journal_present:
                expected = "IDEMPOTENT_SUCCESS"
            else:
                expected = "LEDGER_CORRUPT_UNCHANGED"
            if actual == expected:
                state_cases_passed += 1
                state_outcomes[expected] += 1

    orphan = _empty_state(contract)
    orphan_execution = "exec1-unrelated-orphan"
    orphan.content["finalRecords"]["RunIndexV1"].append(
        _expected_records(contract, orphan_execution)["RunIndexV1"])
    orphan_before = _raw_state_snapshot(orphan)
    orphan_blocked = False
    try:
        _finalize(
            orphan, contract, "exec1-no-prepared-target",
            _request_context_fixture("exec1-no-prepared-target"))
    except LedgerCorrupt:
        orphan_blocked = _raw_state_snapshot(orphan) == orphan_before

    convergence = _empty_state(contract)
    _prepare(convergence, contract, "exec1-attempt-a")
    first_action = _finalize(
        convergence, contract, "exec1-attempt-a",
        _request_context_fixture("exec1-attempt-a"))
    before_second_public = _public_snapshot(convergence)
    _prepare(convergence, contract, "exec1-attempt-b")
    second_action = _finalize(
        convergence, contract, "exec1-attempt-b",
        _request_context_fixture("exec1-attempt-b"))
    after_second_public = _public_snapshot(convergence)
    counts = {name: len(convergence.content["finalRecords"][name])
              for name in FINAL_TYPES}

    retry = _empty_state(contract)
    _prepare(retry, contract, "exec1-prepare-retry")
    retry_exact_before = _raw_state_snapshot(retry)
    _prepare(retry, contract, "exec1-prepare-retry")
    retry_exact_unchanged = _raw_state_snapshot(retry) == retry_exact_before
    retry.content["journals"][0]["semanticEvidenceCasRef"] = "sha256:" + "ee" * 32
    retry_conflict_before = _raw_state_snapshot(retry)
    retry_conflict_rejected = False
    try:
        _prepare(retry, contract, "exec1-prepare-retry")
    except LedgerCorrupt:
        retry_conflict_rejected = _raw_state_snapshot(retry) == retry_conflict_before

    attempt_toctou = _empty_state(contract)
    _prepare(attempt_toctou, contract, "exec1-toctou-attempt")
    attempt_before_public = _public_snapshot(attempt_toctou)
    attempt_busy = False
    def mutate_target_revision(content: dict[str, Any]) -> None:
        attempt = next(row for row in content["attempts"]
                       if row["executionId"] == "exec1-toctou-attempt")
        journal = next(row for row in content["journals"]
                       if row["executionId"] == "exec1-toctou-attempt")
        attempt["revision"] = 2
        attempt_entry = _json_cas_entry(
            attempt["projectId"], "FrozenAttemptRecordV1",
            _attempt_material(attempt))
        attempt["frozenAttemptCasRef"] = attempt_entry["recordCasRef"]
        _cas_put(content["privateCas"], _attempt_entry(attempt))
        journal["expectedAttemptRevision"] = 2
        journal["frozenAttemptCasRef"] = attempt["frozenAttemptCasRef"]
        material = _custody_material(
            contract, "exec1-toctou-attempt", attempt)
        material_entry = _json_cas_entry(
            attempt["projectId"], "CustodyPreparationMaterialV2", material)
        _cas_put(content["privateCas"], material_entry)
        journal["custodyPreparationRef"] = material_entry["recordCasRef"]
    try:
        _finalize(
            attempt_toctou, contract, "exec1-toctou-attempt",
            _request_context_fixture("exec1-toctou-attempt"),
            interleave=lambda state: _atomic_concurrent_change(
                state, contract, mutate_target_revision))
    except BusyTimeout:
        attempt_busy = True
    attempt_after_public = _public_snapshot(attempt_toctou)
    attempt_row = next(row for row in attempt_toctou.content["attempts"]
                       if row["executionId"] == "exec1-toctou-attempt")
    attempt_journal = next(row for row in attempt_toctou.content["journals"]
                           if row["executionId"] == "exec1-toctou-attempt")
    attempt_bytes_preserved = (
        attempt_row["revision"] == 2 and
        attempt_journal["expectedAttemptRevision"] == 2)

    journal_toctou = _empty_state(contract)
    _prepare(journal_toctou, contract, "exec1-toctou-journal")
    journal_before_public = _public_snapshot(journal_toctou)
    journal_busy = False
    def mutate_target_journal(content: dict[str, Any]) -> None:
        journal = next(row for row in content["journals"]
                       if row["executionId"] == "exec1-toctou-journal")
        journal["custodyRevision"] += 1
    try:
        _finalize(
            journal_toctou, contract, "exec1-toctou-journal",
            _request_context_fixture("exec1-toctou-journal"),
            interleave=lambda state: _atomic_concurrent_change(
                state, contract, mutate_target_journal))
    except BusyTimeout:
        journal_busy = True
    journal_after_public = _public_snapshot(journal_toctou)
    journal_bytes_preserved = next(
        row for row in journal_toctou.content["journals"]
        if row["executionId"] == "exec1-toctou-journal"
    )["custodyRevision"] == 2

    return {
        "schemaVersion": 1,
        "assurance": "EXECUTABLE-FOUNDATION-TEST-DOUBLE-NOT-RUNTIME-DEMONSTRATION",
        "closedSchema": {"cases": 12, "rejected": schema_rejections},
        "stateMatrix": {
            "cases": state_cases, "passed": state_cases_passed,
            "outcomes": state_outcomes,
        },
        "noJournalOrphan": {
            "blockedAsCorrupt": orphan_blocked,
            "beforePublic": orphan_before["content"]["finalRecords"],
            "afterPublic": _public_snapshot(orphan)["finalRecords"],
        },
        "sameRunSecondAttempt": {
            "firstAction": first_action, "secondAction": second_action,
            "counts": counts, "beforePublic": before_second_public,
            "afterPublic": after_second_public,
        },
        "prepareRetry": {
            "exactRetryUnchanged": retry_exact_unchanged,
            "conflictingSameExecutionRejectedUnchanged": retry_conflict_rejected,
        },
        "attemptToctou": {
            "staleCasRejected": attempt_busy,
            "concurrentBytesPreserved": attempt_bytes_preserved,
            "beforePublic": attempt_before_public,
            "afterPublic": attempt_after_public,
        },
        "journalToctou": {
            "staleCasRejected": journal_busy,
            "concurrentBytesPreserved": journal_bytes_preserved,
            "beforePublic": journal_before_public,
            "afterPublic": journal_after_public,
        },
        "rt13Custody": run_rt13_custody_probes(contract),
        "authorityRepairs": run_authority_repair_probes(contract),
    }


def _probe_errors(result: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(result, dict) or result.get("schemaVersion") != 1:
        return ["foundation probe root invalid"]
    if result.get("closedSchema") != {"cases": 12, "rejected": 12}:
        errors.append("closed final-schema probes failed")
    if result.get("stateMatrix") != {
            "cases": 128, "passed": 128,
            "outcomes": {
                "NEW": 1, "NO_PREPARED_RUN": 1,
                "IDEMPOTENT_SUCCESS": 1,
                "LEDGER_CORRUPT_UNCHANGED": 125}}:
        errors.append("exhaustive 128-state final/journal matrix failed")
    if (result.get("noJournalOrphan") or {}).get("blockedAsCorrupt") is not True:
        errors.append("unrelated no-journal orphan did not block target lookup")
    convergence = result.get("sameRunSecondAttempt") or {}
    if convergence.get("firstAction") != "NEW" or \
            convergence.get("secondAction") != "CONVERGE" or \
            convergence.get("counts") != {
                "TerminalRunV1": 1, "RunIndexV1": 1,
                "AttemptRunLinkV1": 2, "RunCustodyRootV1": 1,
                "RunAuthorityIndexV1": 1, "RunCommitNotificationV1": 2}:
        errors.append("same-Run second-Attempt convergence failed")
    retry = result.get("prepareRetry") or {}
    if retry != {
            "exactRetryUnchanged": True,
            "conflictingSameExecutionRejectedUnchanged": True}:
        errors.append("same-execution prepare insert-or-exact probe failed")
    for key in ("attemptToctou", "journalToctou"):
        row = result.get(key) or {}
        if row.get("staleCasRejected") is not True or \
                row.get("concurrentBytesPreserved") is not True or \
                row.get("beforePublic", {}).get("finalRecords") != \
                row.get("afterPublic", {}).get("finalRecords"):
            errors.append(f"{key} snapshot/CAS probe failed")
    errors.extend(_rt13_probe_errors(result.get("rt13Custody")))
    errors.extend(_authority_repair_probe_errors(result.get("authorityRepairs")))
    return errors


def _foundation_contract_errors(value: Any, *, run_probes: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["root is not an object"]
    for filename, expected in PINS.items():
        actual = sha_file(filename)
        if actual != expected:
            errors.append(f"pinned input drift: {filename} {actual} != {expected}")
    try:
        predecessor = load("evidence.v7.json")
    except Exception as exc:
        return errors + [f"cannot load immutable E7 predecessor: {exc}"]
    if (value.get("artifact"), value.get("version")) != ("opensip.evidence", 8):
        errors.append("artifact/version mismatch")
    if value.get("status") != "CANDIDATE-NOT-APPLIED" or \
            value.get("sealRecommendation") != "DO-NOT-SEAL":
        errors.append("candidate/no-seal status drift")
    if value.get("supersedes") != {
            "artifact": "evidence.v7.json", "sha256": PINS["evidence.v7.json"],
            "checker": "check-evidence-v7.py",
            "checkerSha256": PINS["check-evidence-v7.py"],
            "review": "evidence.v7.review-adversarial-prefreeze-rejected.json",
            "reviewSha256": PINS["evidence.v7.review-adversarial-prefreeze-rejected.json"]}:
        errors.append("E7 rejected predecessor/review pins drift")
    dependency_rows = {
        "evaluationProof": ("evaluation-proof.v8.json",
                            "check-evaluation-proof-v8.py"),
        "retentionCustody": ("retention-tiers.v13.json",
                             "check-retention-custody-v13.py"),
        "versioning": ("versioning-policy.v8.json", "check-versioning-v8.py"),
    }
    for key, (artifact_name, checker_name) in dependency_rows.items():
        row = (value.get("dependencies") or {}).get(key) or {}
        if row.get("artifact") != artifact_name or \
                row.get("sha256") != PINS[artifact_name] or \
                row.get("checker") != checker_name or \
                row.get("checkerSha256") != PINS[checker_name]:
            errors.append(f"pinned dependency declaration drift: {key}")
    delta = value.get("successorDelta") or {}
    if set(delta.get("changedRootKeys") or []) != CHANGED_ROOT_KEYS or \
            set(delta.get("addedRootKeys") or []) != ADDED_ROOT_KEYS or \
            tuple(delta.get("protectedIdentityKeys") or []) != PROTECTED or \
            delta.get("predecessor") != SUCCESSOR_PREDECESSOR or \
            delta.get("rejection") != SUCCESSOR_REJECTION or \
            delta.get("scope") != SUCCESSOR_SCOPE:
        errors.append("closed successor delta declaration drift")
    if set(value) != set(predecessor) | ADDED_ROOT_KEYS:
        errors.append("E8 root additions differ from exact successor delta")
    for key in set(predecessor) - CHANGED_ROOT_KEYS:
        if value.get(key) != predecessor.get(key):
            errors.append(f"unlisted predecessor surface changed: {key}")
    for key in PROTECTED:
        if value.get(key) != predecessor.get(key):
            errors.append(f"protected identity surface changed: {key}")
    if value.get("apiContract") != API_CONTRACT:
        errors.append("closed commit/recovery API contract drift")
    if value.get("durableRecoveryContract") != DURABLE_RECOVERY_CONTRACT:
        errors.append("closed durable recovery authority contract drift")
    expected_imported_authority = copy.deepcopy(
        predecessor.get("importedAuthorityContract"))
    try:
        expected_imported_authority["finalizeApi"] = (
            "commit_run_v2(ProjectStoreAuthorityV1, TrustedRequestContextV1, "
            "ExecutionId, AdmittedEvaluationAuthorityV1, "
            "FinalizedSemanticEvidenceV1, PreparedCustodyV1)")
        expected_imported_authority["onePortRule"] = (
            "EP8 authority operations and Evidence v8 journal/run operations "
            "are traits of one production opensip_store "
            "ProjectStoreAuthorityV1 nominal port; the checker composite is "
            "one session, not a second public store type.")
    except TypeError:
        errors.append("immutable E7 imported-authority contract is not an object")
    else:
        if value.get("importedAuthorityContract") != \
                expected_imported_authority:
            errors.append(
                "imported authority differs from exact E8 API derivation")
    expected_run_authority = copy.deepcopy(
        predecessor.get("runAuthorityIndexContract"))
    try:
        expected_run_authority["atomicPeers"] = [
            "TerminalRunV1", "RunIndexV1", "AttemptRunLinkV1",
            "RunCustodyRootV1", "RunCommitNotificationV1"]
    except TypeError:
        errors.append("immutable E7 Run authority contract is not an object")
    else:
        if value.get("runAuthorityIndexContract") != expected_run_authority:
            errors.append(
                "Run authority index differs from exact E8 atomic-peer derivation")
    expected_correlation = copy.deepcopy(
        predecessor.get("correlationDifferential"))
    try:
        expected_correlation["semanticInputs"] = (
            "byte-identical EP8 bundle, RT13 closure, admitted authority and "
            "canonical Evidence records")
        expected_correlation["expectedDistinct"] = [
            "RequestId", "ExecutionId", "AttemptRunLinkV1",
            "RunCommitNotificationV1.committerRequestId"]
    except TypeError:
        errors.append("immutable E7 correlation differential is not an object")
    else:
        if value.get("correlationDifferential") != expected_correlation:
            errors.append(
                "correlation differential differs from exact E8 derivation")
    expected_recovery_matrix = copy.deepcopy(
        predecessor.get("recoveryMatrixContract"))
    try:
        expected_recovery_matrix["failureVisibility"] = (
            "Every failed or merely prepared scenario has zero newly public "
            "RunId/runSealRef/Terminal/RunAuthorityIndex/"
            "RunCommitNotificationV1; custody-loss source facts contain no "
            "Run or D9 conclusion.")
    except TypeError:
        errors.append("immutable E7 recovery matrix contract is not an object")
    else:
        if value.get("recoveryMatrixContract") != expected_recovery_matrix:
            errors.append(
                "recovery matrix differs from exact E8 visibility derivation")
    expected_store = copy.deepcopy(predecessor.get("storeContract"))
    try:
        journal_contract = expected_store["records"].pop(
            "RunFreePreparedCommitV2")
        journal_contract["required"] = [
            "schemaVersion", "projectId", "executionId",
            "expectedAttemptRevision", "frozenAttemptCasRef",
            "evaluationAuthoritySealRef", "evaluationAuthorityAdmissionCasRef",
            "semanticEvidenceCasRef", "frozenRetentionTargetRef",
            "rawProofInventoryCasRef", "custodyPreparationRef",
            "custodyState", "custodyRevision", "leaseId", "ownerId",
            "ownerLivenessToken", "fencingToken", "pinnedRefs"]
        expected_store["records"]["RunFreePreparedCommitV3"] = journal_contract
        expected_store["records"].pop("CustodyPreparationMaterialV1")
        expected_store["records"].pop("CustodyPreparedObjectV1")
        expected_store["records"].update({
            "PrivateCasObjectV1": {
                "closed": True,
                "required": ["schemaVersion", "projectId", "recordCasRef",
                             "recordKind", "recordBytesHex"],
                "authorityRule": "Validate raw SHA-256, exact bytes, closed kind and ProjectId before following any ref; fixed EP8/RT13/Evidence inputs are byte-exact and dynamic JSON records must be canonical",
            },
            "FrozenAttemptRecordV1": {
                "closed": True, "contentAddressed": True,
                "required": ["schemaVersion", "projectId", "executionId",
                             "revision", "evaluationAuthoritySealRef",
                             "evaluationAuthorityAdmissionCasRef",
                             "frozenRetentionTargetRef", "semanticEvidenceCasRef"],
                "authorityRule": "the Attempt row carries frozenAttemptCasRef to these exact canonical bytes; journal expected revision and every immutable ref must equal them",
            },
            "CustodyPreparationMaterialV2": {
                "closed": True, "contentAddressed": True,
                "required": ["schemaVersion", "projectId", "executionId",
                             "frozenAttemptCasRef", "evaluationAuthoritySealRef",
                             "evaluationAuthorityAdmissionCasRef",
                             "semanticEvidenceCasRef", "evaluationProofBundleCasRef",
                             "semanticCapabilityClosureCasRef",
                             "semanticCapabilityClosureCommitment",
                             "rawProofInventoryCasRef", "frozenRetentionTargetRef",
                             "units", "requiredRowCasRefs"],
                "authorityRule": "canonical durable authority material; recovery freshly derives every value plus exactly 23 row CAS refs and requires exact equality",
            },
            "CustodyPreparedObjectV2": {
                "closed": True, "contentAddressed": True,
                "required": ["schemaVersion", "projectId",
                             "frozenRetentionTargetRef", "unitId",
                             "requiredForCapability", "recordCasRef", "recordKind"],
                "authorityRule": "each canonical row equals one exact cold-derived unit/minimum/raw-key association; current custody authority still comes exclusively from the RT13 reducer over the exact 23-key required subset, never row presence, a boolean, or an opaque token",
            },
            "AttemptTerminalDispositionV1": {
                "closed": True,
                "required": ["schemaVersion", "projectId", "executionId",
                             "disposition", "custodyLossProofRef"],
                "constants": {"disposition": "custody-lost-before-run"},
                "authorityRule": "paired source fact only; contains no RunId, RequestId or authored D9 class/code/exit",
            },
            "CustodyLossProofV1": {
                "closed": True,
                "required": ["schemaVersion", "projectId", "executionId",
                             "cause", "frozenAttemptCasRef",
                             "custodyPreparationRef", "observedAtSequence",
                             "requiredObjectStates"],
                "constants": {"cause": "required-custody-unavailable"},
                "authorityRule": "enumerates the exact 23 required object states after reducer truth; source fact only, with no Run or D9 conclusion",
            },
            "RunCommitNotificationV1": {
                "key": ["projectId", "executionId", "run-committed"],
                "required": ["schemaVersion", "projectId", "notificationKind",
                             "committerRequestId", "executionId", "runId",
                             "runSealRef"],
                "constants": {"notificationKind": "run-committed"},
                "uniqueness": "exactly one durable row per Attempt; concurrent winner owns committerRequestId and later replay preserves it",
            },
        })
        expected_store["records"]["RunCustodyRootV1"]["boundary"] = (
            "operational reachability/lineage outside EvidenceDigest; unitIds "
            "are the exact two RT13 cold-derived UNIT-ID-V3 values")
        expected_store["transaction"][0] = (
            "Through one fresh ProjectStoreAuthorityV1 session over DurableProjectStateV2, audit the complete closed private CAS, cold-resolve EP8 authority and reread/rehash bundle, RT13 closure, raw inventory, SemanticEvidence, explicit target, exact 23 custody rows, custody preparation and frozen Attempt revision/content.")
        expected_store["transaction"][2] = (
            "In one serializable transaction publish-or-verify the exact six "
            "final records including RunCommitNotificationV1 from the opaque "
            "TrustedRequestContextV1, mechanically apply RT13 release, and remove "
            "RunFreePreparedCommitV3; journal removal and custody transfer do "
            "not add a seventh published record.")
        expected_store["recovery"][1] = (
            "Journal exists but no index/link: open a fresh session over the same durable state; audit every referenced CAS byte; EP8 cold-resolves EAS; reread and rederive SemanticEvidence plus RT13 closure/raw inventory/exact custody rows; remint finalized evidence and custody under that session; retry with the same session and a fresh opaque recovery TrustedRequestContextV1.")
        expected_store["recovery"][2] = (
            "Commit succeeded but response was lost: exact Attempt link, Run index and persisted RunCommitNotificationV1 return the committed result idempotently; a different current recovery RequestId does not rewrite or corrupt the winner row.")
        expected_store["recovery"][4] = (
            "Concurrent semantically identical Attempts converge on one RunIndex/RunCustodyRoot and retain distinct AttemptRunLinkV1/RunCommitNotificationV1 pairs.")
        expected_store["finalTransaction"]["writes"][3] = "RunCustodyRootV1"
        expected_store["finalTransaction"]["writes"][5] = \
            "RunCommitNotificationV1"
        expected_store["finalTransaction"]["precondition"] = (
            "the current-session ProjectStoreAuthorityV1, opaque TrustedRequestContextV1 and freshly minted EP8 handle/finalized/custody capabilities pass an in-transaction complete private-CAS/Attempt/journal/RT inventory audit; Terminal and RunAuthorityIndex fully rederive without any old token authority")
        expected_store["finalTransaction"]["visibility"] = (
            "RunId, Terminal, RunAuthorityIndex and RunCommitNotificationV1 become public together or none do")
    except (KeyError, IndexError, TypeError):
        errors.append("immutable E7 storeContract cannot derive E8 alias correction")
    else:
        if value.get("storeContract") != expected_store:
            errors.append("storeContract differs from exact durable-authority/notification successor derivation")
    expected_continuity = copy.deepcopy(
        predecessor.get("storeCapabilityContinuityContract"))
    try:
        expected_continuity["api"] = (
            "commit_run_v2(ProjectStoreAuthorityV1, TrustedRequestContextV1, ExecutionId, AdmittedEvaluationAuthorityV1, FinalizedSemanticEvidenceV1, PreparedCustodyV1) -> CommittedRunV1")
        expected_continuity["preconditions"][0] = (
            "live commit arguments are current-session opaque capabilities including TrustedRequestContextV1; cold recovery accepts only a fresh store session, fresh trusted request context and host-owned ExecutionId and remints all live values")
        expected_continuity["atomicWrites"][3] = "RunCustodyRootV1"
        expected_continuity["atomicWrites"][5] = "RunCommitNotificationV1"
    except (KeyError, IndexError, TypeError):
        errors.append("immutable E7 continuity contract cannot derive E8 alias correction")
    else:
        if value.get("storeCapabilityContinuityContract") != expected_continuity:
            errors.append("store capability continuity contract differs from exact E8 repair")
    golden = value.get("acceptedGolden") or {}
    if golden.get("semanticEvidenceCasRef") != \
            "sha256:858ccc7c508c49c44ae85df6f880b4e26cecb0b2ec182abbf890a6c1ea8a0d82" or \
            golden.get("evidenceDigest") != \
            "sha256:6edbf46f919565e5a10426e4ff9f1dcf56588d18d1b75ad1c32cd848b19f47b9" or \
            golden.get("runId") != \
            "run1:3f319950f6a00565611029f3accc38a2afd38b3f4ab6539b2d6c8304ef0a9208" or \
            golden.get("runSealRef") != \
            "sha256:d34fc5e0d80f2af919c3ab572f03793b7893dddb2f816587b76bce40af497734":
        errors.append("protected Evidence/Run identity constant drift")
    strings = list(_walk_strings(value))
    alias_pattern = re.compile(r"(?<![A-Za-z0-9])CustodyRootV1(?![A-Za-z0-9])")
    if any(alias_pattern.search(text) for text in strings):
        errors.append("forbidden CustodyRootV1 alias appears on an E8 surface")
    stale_pattern = re.compile(
        r"(?<![A-Za-z0-9])(?:EP7|RT12|VERSIONING v6|VERSIONING v7|Evidence v7)(?![A-Za-z0-9])")
    stale = [text for text in strings if stale_pattern.search(text)]
    if stale:
        errors.append(f"stale current-generation nomenclature: {stale[0]}")
    foundation = value.get("foundationImplementation") or {}
    if foundation.get("status") != "PARTIAL-CANDIDATE-RED" or \
            foundation.get("assurance") != "IMPLEMENTABLE_UNEXECUTED" or \
            foundation.get("blockingTodos") != TODO_DECLARATIONS:
        errors.append("partial/RED assurance boundary or TODO list drift")
    schemas = foundation.get("finalRecordSchemas") or {}
    if schemas != {name: list(fields) for name, fields in FINAL_FIELDS.items()}:
        errors.append("closed final-record schema declaration drift")
    if foundation.get("projectState") != PROJECT_STATE_CONTRACT:
        errors.append("snapshot/revision/full-content CAS contract drift")
    if foundation.get("integrityEnumeration") != INTEGRITY_CONTRACT:
        errors.append("project-wide R4/A2 integrity declaration drift")
    if foundation.get("transitionTable") != TRANSITION_TABLE:
        errors.append("closed R4/A2/journal transition table drift")
    if foundation.get("focusedExecutableProbes") != FOCUSED_PROBES:
        errors.append("focused executable probe declaration drift")
    if foundation.get("serializedCustodyContract") != SERIALIZED_CUSTODY_CONTRACT:
        errors.append("RT13 serialized-custody contract drift")
    if foundation.get("privateCasContract") != PRIVATE_CAS_CONTRACT:
        errors.append("typed private CAS authority contract drift")
    if foundation.get("rtObjectInventoryContract") != RT_INVENTORY_CONTRACT:
        errors.append("RT project-object inventory contract drift")
    if foundation.get("terminalFactContract") != TERMINAL_FACT_CONTRACT:
        errors.append("custody-loss terminal FACTS contract drift")
    if foundation.get("runCommitNotificationContract") != NOTIFICATION_CONTRACT:
        errors.append("RunCommitNotificationV1 contract drift")
    if foundation.get("op6TraceExportContract") != OP6_TRACE_CONTRACT:
        errors.append("OP6 raw trace export contract drift")
    if run_probes:
        try:
            errors.extend(_probe_errors(run_foundation_probes(value)))
        except Exception as exc:
            errors.append(f"foundation probes raised {type(exc).__name__}: {exc}")
    return errors


def check(value: Any) -> list[str]:
    """Full E8 check: intentionally RED on exactly three explicit TODOs."""
    return _foundation_contract_errors(value) + list(TODO_FINDINGS)


def foundation_selftest(value: Any) -> list[str]:
    failures = _foundation_contract_errors(value, run_probes=True)
    if failures:
        return failures
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("version", lambda x: x.__setitem__("version", 7)),
        ("status", lambda x: x.__setitem__("status", "APPLIED")),
        ("rt13-dependency", lambda x: x["dependencies"]["retentionCustody"]
            .__setitem__("checkerSha256", "0" * 64)),
        ("successor-predecessor", lambda x: x["successorDelta"].__setitem__(
            "predecessor", "anything")),
        ("successor-rejection", lambda x: x["successorDelta"].__setitem__(
            "rejection", "anything")),
        ("successor-scope", lambda x: x["successorDelta"].__setitem__(
            "scope", "anything")),
        ("project-schema", lambda x: x["foundationImplementation"]["projectState"]
            .__setitem__("schema", "TrustMeV1")),
        ("project-guard", lambda x: x["foundationImplementation"]["projectState"]
            .__setitem__("guard", "revision only")),
        ("project-begin", lambda x: x["foundationImplementation"]["projectState"]
            .__setitem__("begin", "trust caller")),
        ("project-commit", lambda x: x["foundationImplementation"]["projectState"]
            .__setitem__("commit", "blind overwrite")),
        ("project-stale", lambda x: x["foundationImplementation"]["projectState"]
            .__setitem__("staleResult", "success")),
        ("alias", lambda x: x["foundationImplementation"]["integrityEnumeration"]
            ["sharedR4"].__setitem__(2, "CustodyRootV1")),
        ("integrity-attempt-a2", lambda x: x["foundationImplementation"]
            ["integrityEnumeration"]["attemptA2"].pop()),
        ("integrity-rule", lambda x: x["foundationImplementation"]
            ["integrityEnumeration"].__setitem__("rule", "trust caller boolean")),
        ("integrity-seventh", lambda x: x["foundationImplementation"]
            ["integrityEnumeration"].__setitem__("noSeventhFinalRecord", False)),
        ("transition-table", lambda x: x["foundationImplementation"].__setitem__(
            "transitionTable", [])),
        ("focused-probes", lambda x: x["foundationImplementation"].__setitem__(
            "focusedExecutableProbes", [])),
        ("custody-authority", lambda x: x["foundationImplementation"]
            ["serializedCustodyContract"].__setitem__("authority", "trust row")),
        ("custody-states", lambda x: x["foundationImplementation"]
            ["serializedCustodyContract"]["states"].pop()),
        ("custody-acquisition", lambda x: x["foundationImplementation"]
            ["serializedCustodyContract"].__setitem__("acquisition", "split writes")),
        ("custody-horizon", lambda x: x["foundationImplementation"]
            ["serializedCustodyContract"].__setitem__("horizon", "wall clock")),
        ("custody-serialization", lambda x: x["foundationImplementation"]
            ["serializedCustodyContract"].__setitem__("serialization", "many journals")),
        ("custody-commit", lambda x: x["foundationImplementation"]
            ["serializedCustodyContract"].__setitem__("commit", "boolean pinned")),
        ("custody-pending-expiry", lambda x: x["foundationImplementation"]
            ["serializedCustodyContract"].__setitem__("pendingExpiry", "commit anyway")),
        ("custody-recovery", lambda x: x["foundationImplementation"]
            ["serializedCustodyContract"].__setitem__("recovery", "reuse fence")),
        ("custody-failure", lambda x: x["foundationImplementation"]
            ["serializedCustodyContract"].__setitem__("failure", "partial writes")),
        ("custody-events", lambda x: x["foundationImplementation"]
            ["serializedCustodyContract"].__setitem__("mutableEvents", "ignore reducer")),
        ("custody-residuals", lambda x: x["foundationImplementation"]
            ["serializedCustodyContract"]["residuals"].pop()),
        ("private-cas-hash", lambda x: x["foundationImplementation"]
            ["privateCasContract"].__setitem__("record", "trust ref")),
        ("rt-inventory-subset", lambda x: x["foundationImplementation"]
            ["rtObjectInventoryContract"].__setitem__(
                "requiredSubset", "extras become authority")),
        ("terminal-fact-d9", lambda x: x["foundationImplementation"]
            ["terminalFactContract"]["exclusions"].remove("D9 code")),
        ("notification-context", lambda x: x["foundationImplementation"]
            ["runCommitNotificationContract"].__setitem__(
                "authority", "accept raw requestId")),
        ("op6-trace-oracle", lambda x: x["foundationImplementation"]
            ["op6TraceExportContract"].__setitem__(
                "oracleBoundary", "export pass=true")),
        ("api-commit-v1", lambda x: x["apiContract"]["calls"].__setitem__(
            8, "opensip_store.commit_run_v1(ProjectStoreAuthorityV1, "
            "RequestId, ExecutionId) -> CommittedRunV1")),
        ("api-raw-identities", lambda x: x["apiContract"].__setitem__(
            "constructionRule", "Commit accepts raw RequestId/ExecutionId.")),
        ("durable-state-type", lambda x: x["durableRecoveryContract"]
            .__setitem__("stateType", "DurableProjectStateV1")),
        ("durable-state-owns", lambda x: x["durableRecoveryContract"]
            ["stateOwns"].__setitem__(4, "only the 23 required objects")),
        ("durable-recovery-v1", lambda x: x["durableRecoveryContract"]
            .__setitem__("recoveryApi", "recover_run_v1(raw ExecutionId)")),
        ("imported-authority-finalize", lambda x: x["importedAuthorityContract"]
            .__setitem__("finalizeApi", "commit_run_v1(raw ids)")),
        ("run-authority-notification", lambda x: x["runAuthorityIndexContract"]
            ["atomicPeers"].__setitem__(4, "outbox")),
        ("correlation-notification", lambda x: x["correlationDifferential"]
            ["expectedDistinct"].pop()),
        ("recovery-failure-visibility", lambda x: x["recoveryMatrixContract"]
            .__setitem__("failureVisibility", "prepared RunId may leak")),
        ("schema-open", lambda x: x["foundationImplementation"]["finalRecordSchemas"]
            ["RunIndexV1"].append("unknown")),
        ("journal-lease-field", lambda x: x["storeContract"]["records"]
            ["RunFreePreparedCommitV3"]["required"].remove("fencingToken")),
        ("store-transaction", lambda x: x["storeContract"].__setitem__(
            "transaction", [])),
        ("store-recovery", lambda x: x["storeContract"].__setitem__(
            "recovery", [])),
        ("store-final-transaction", lambda x: x["storeContract"].__setitem__(
            "finalTransaction", {})),
        ("continuity-preconditions", lambda x: x["storeCapabilityContinuityContract"]
            .__setitem__("preconditions", [])),
        ("continuity-atomic", lambda x: x["storeCapabilityContinuityContract"]
            ["atomicWrites"].pop()),
        ("continuity-collision", lambda x: x["storeCapabilityContinuityContract"]
            .__setitem__("collisionRule", "overwrite")),
        ("continuity-toctou", lambda x: x["storeCapabilityContinuityContract"]
            .__setitem__("toctouRule", "none")),
        ("word-alias", lambda x: x["reviewFindingTransfers"][0].__setitem__(
            "closure", "accept CustodyRootV1 alias")),
        ("stale-generation", lambda x: x["recursiveRequestIdExclusion"]
            ["surfaces"].__setitem__(0, "EP7 EvaluationAuthoritySealV1")),
        ("identity", lambda x: x["acceptedGolden"].__setitem__(
            "runId", "run1:" + "f" * 64)),
        ("todo-promotion", lambda x: x["foundationImplementation"].__setitem__(
            "blockingTodos", [])),
    ]
    for label, mutate in mutations:
        candidate = copy.deepcopy(value)
        mutate(candidate)
        if not _foundation_contract_errors(candidate, run_probes=False):
            failures.append(f"{label} mutation escaped")
    return failures


def main(argv: list[str]) -> int:
    positional = [arg for arg in argv[1:]
                  if arg not in {"--selftest", "--foundation-selftest"}]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        value = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if "--foundation-selftest" in argv[1:]:
        failures = foundation_selftest(value)
        if failures:
            for failure in failures:
                print(f"FOUNDATION-FAIL: {failure}")
            return 1
        probes = run_foundation_probes(value)
        print("PASS: E8 foundation; 12 closed-schema negatives; "
              f"{probes['stateMatrix']['cases']} final/journal states; "
              "same-Run convergence; exact retry collision; target "
              "Attempt/journal snapshot-CAS TOCTOU")
        print("NOTE: durable-authority/notification foundation is checker-green; "
              "full E8 remains RED on accepted D9/retention, trusted request "
              "context leaf, and remaining contract binding")
        return 0
    errors = check(value)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    if "--selftest" in argv[1:]:
        failures = foundation_selftest(value)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
    print("PASS: evidence.v8.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
