"""Post-reset author v2 (Claude): security schema additions for P3 (AdmittedBoundaryInventoryV1), P9
(RepairRecoveryAuthorizationV1 / RecoveryAuthorizationAdmissionV1) and P10 (InstallationTransitionIntentV1,
InstallationTransitionJournalV1, TransitionIntentAdmissionV1, TransitionJournalAdmissionV1, TransitionRecoveryV1), plus the
LeaseTraceV1 `transition-journal` op. Round-trip verified: json.dumps(indent=2, ensure_ascii=False) + newline reproduces
the current bytes. Idempotent."""
import json
from pathlib import Path

P = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json')
raw = P.read_bytes()
doc = json.loads(raw)
assert (json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode() == raw, 'round-trip'
D, S = doc['$defs'], doc['schemas']

REL_DIR = {"type": "string", "minLength": 1, "maxLength": 4096, "pattern": "^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]+(?![\\s\\S])"}
REL_DIR_OR_ROOT = {"type": "string", "maxLength": 4096, "pattern": "^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]*(?![\\s\\S])"}
D['RequestId'] = {"type": "string", "pattern": "^req1_[0-9a-f]{32}(?![\\s\\S])"}
D['ExecutionId'] = {"type": "string", "pattern": "^exec1_[0-9a-f]{32}(?![\\s\\S])"}
D['JournalState'] = {"enum": ["PREPARING", "STAGED", "APPLYING", "APPLIED", "COMMITTED", "FAILED_CLEAN", "FAILED_ROLLED_BACK", "RECOVERY_BLOCKED", "INDETERMINATE"]}
D['RecoveryAction'] = {"enum": ["discard-temps", "roll-back-renamed", "verify-postimages-and-commit"]}
D['NamespaceList'] = {"type": "array", "maxItems": 65536, "uniqueItems": True, "items": {"type": "string", "minLength": 1, "maxLength": 4096}}
D['StateSchema'] = {"enum": [1, 2]}
D['TransitionOperation'] = {"enum": ["core-update", "core-repair", "core-rollback", "store-migrate", "store-rollback"]}
D['TransitionRefusal'] = {"type": "string", "pattern": "^TRANSITION\\.[A-Z_]+(:[^ ]+)?(?![\\s\\S])", "maxLength": 256}
D['LogicalPath'] = {"type": "string", "minLength": 1, "maxLength": 1024, "pattern": "^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]+(?![\\s\\S])"}

S['AdmittedBoundaryInventoryV1'] = {
    "title": "S3 export (post-reset v2 P3): the admitted authority boundaries of the selected root as relative scope paths; produced only by boundary_inventory over an ACCEPTed DiscoveryResultV1 and consumed unchanged by the native unit instrument",
    "type": "object", "additionalProperties": False,
    "required": ["schemaVersion", "source", "selectedRoot", "nestedRepositories", "nestedProjects", "custodyExcludedUnits", "prunedTrees"],
    "properties": {
        "schemaVersion": {"const": 1},
        "source": {"const": "security.discovery"},
        "selectedRoot": {"type": "string", "minLength": 1, "maxLength": 4096},
        "nestedRepositories": {"type": "array", "maxItems": 4096, "uniqueItems": True, "items": REL_DIR},
        "nestedProjects": {"type": "array", "maxItems": 4096, "uniqueItems": True, "items": REL_DIR},
        "custodyExcludedUnits": {"type": "array", "maxItems": 4096, "items": {
            "type": "object", "additionalProperties": False, "required": ["path", "reason"],
            "properties": {"path": REL_DIR_OR_ROOT,
                           "reason": {"type": "string", "minLength": 1, "maxLength": 256,
                                      "pattern": "^(DIRECTORY_CUSTODY:[A-Z_]+|MARKER_CUSTODY:(Cargo\\.toml|package\\.json|tsconfig\\.json|jsconfig\\.json):[A-Z_]+|DEPTH)(?![\\s\\S])"}}}},
        "prunedTrees": {"type": "array", "maxItems": 65536, "items": {
            "type": "object", "additionalProperties": False, "required": ["path", "reason", "markerCount"],
            "properties": {"path": REL_DIR, "reason": {"enum": ["dependency-tree", "vcs-tree", "cargo-build-output"]}, "markerCount": {"$ref": "#/$defs/I64NonNegative"}}}}}}

S['RepairRecoveryAuthorizationV1'] = {
    "title": "product data (S10.2); identity H('security.repair-recovery-authorization.v1', record) is the workflow RepairApplyJournalV1.recoveryAuthorizationRef; authorizes ONE finite recovery action within the original plan's authority under the EXCLUSIVE lease at the host-broker boundary; never repository execution, never a new edit",
    "type": "object", "additionalProperties": False,
    "required": ["authorizationSchema", "kind", "projectId", "repairPlanId", "baseSnapshotId", "recipeClosureId", "journalRef", "journalState",
                 "observedJournalStateDigest", "recoveryAction", "originalRequestId", "recoveryRequestId", "recoveryExecutionId", "consent",
                 "issuedAt", "expiresAt", "leaseMode", "mutationBoundary", "repositoryExecution", "newEdits"],
    "properties": {
        "authorizationSchema": {"const": 1},
        "kind": {"const": "repair-recover"},
        "projectId": {"$ref": "#/$defs/ProjectId"},
        "repairPlanId": {"$ref": "#/$defs/RepairPlanId"},
        "baseSnapshotId": {"$ref": "#/$defs/SnapshotId"},
        "recipeClosureId": {"$ref": "#/$defs/ClosureId"},
        "journalRef": {"type": "string", "pattern": "^security\\.repair-apply-journal-identity\\.v1:[0-9a-f]{64}(?![\\s\\S])",
                       "description": "H over the closed noncircular journal identity preimage {schemaFamily, schemaMajor, requestId, stepId, executionId, repairPlanId, baseSnapshotId, authorizationRef}: never state, paths, blobs or a recoveryAuthorizationRef"},
        "journalState": {"$ref": "#/$defs/JournalState"},
        "observedJournalStateDigest": {"$ref": "#/$defs/Hex64", "description": "raw SHA-256 of canonical {state, stagedPaths, appliedPaths, preimageBlobs} as read under the EXCLUSIVE lease before any recovery write; single use / crash-safe resume"},
        "recoveryAction": {"$ref": "#/$defs/RecoveryAction"},
        "originalRequestId": {"$ref": "#/$defs/RequestId"},
        "recoveryRequestId": {"$ref": "#/$defs/RequestId"},
        "recoveryExecutionId": {"$ref": "#/$defs/ExecutionId"},
        "consent": {"$ref": "#/$defs/Consent"},
        "issuedAt": {"$ref": "#/$defs/Timestamp"},
        "expiresAt": {"$ref": "#/$defs/Timestamp"},
        "leaseMode": {"const": "EXCLUSIVE"},
        "mutationBoundary": {"const": "host-broker"},
        "repositoryExecution": {"const": False},
        "newEdits": {"const": False}}}

S['RecoveryAuthorizationAdmissionV1'] = {
    "type": "object", "additionalProperties": False,
    "required": ["result", "refusals", "d9", "grantsRepositoryExecution", "grantsNewEdits", "planScope", "leaseMode", "mutationBoundary", "action",
                 "recipeTrustConsulted", "journalRef", "journalStateDigest", "identityDomain", "inspection", "preimagePostimageLaw", "replaySemantics",
                 "revocationPath", "trustedContextInputs"],
    "properties": {
        "result": {"enum": ["ADMIT", "REFUSE"]},
        "refusals": {"type": "array", "maxItems": 64, "items": {"type": "string", "pattern": "^AUTHZ\\.[A-Z_]+(:[^ ]+)?(?![\\s\\S])"}},
        "d9": {"$ref": "#/$defs/NullableD9"},
        "grantsRepositoryExecution": {"const": False},
        "grantsNewEdits": {"const": False},
        "planScope": {"const": "original-plan-only"},
        "leaseMode": {"enum": [None, "EXCLUSIVE"]},
        "mutationBoundary": {"enum": [None, "host-broker"]},
        "action": {"oneOf": [{"type": "null"}, {"$ref": "#/$defs/RecoveryAction"}]},
        "recipeTrustConsulted": {"type": ["boolean", "null"]},
        "journalRef": {"$ref": "#/$defs/NullableString"},
        "journalStateDigest": {"oneOf": [{"type": "null"}, {"$ref": "#/$defs/Hex64"}]},
        "identityDomain": {"const": "security.repair-recovery-authorization.v1"},
        "inspection": {"type": "string"},
        "preimagePostimageLaw": {"type": "string"},
        "replaySemantics": {"type": "string"},
        "revocationPath": {"type": "string"},
        "trustedContextInputs": {"$ref": "#/$defs/StringList"}}}

S['InstallationTransitionIntentV1'] = {
    "title": "S9.2 required operation/field contract of the host-projected installation transition intent (workflow CoreTransitionIntentV1 successor; the same eleven fields serve core update|repair|rollback and store migrate|rollback)",
    "type": "object", "additionalProperties": False,
    "required": ["schemaVersion", "operation", "fromCoreClosure", "toCoreClosure", "fromStateSchema", "toStateSchema", "fromStoreGeneration",
                 "toStoreGeneration", "platformProfileSetBodyDigest", "preconditionGeneration", "rollbackDeadline"],
    "properties": {
        "schemaVersion": {"const": 1},
        "operation": {"$ref": "#/$defs/TransitionOperation"},
        "fromCoreClosure": {"$ref": "#/$defs/ClosureId"},
        "toCoreClosure": {"$ref": "#/$defs/ClosureId"},
        "fromStateSchema": {"$ref": "#/$defs/StateSchema"},
        "toStateSchema": {"$ref": "#/$defs/StateSchema"},
        "fromStoreGeneration": {"$ref": "#/$defs/I64NonNegative"},
        "toStoreGeneration": {"$ref": "#/$defs/I64NonNegative"},
        "platformProfileSetBodyDigest": {"$ref": "#/$defs/Hex64"},
        "preconditionGeneration": {"$ref": "#/$defs/I64NonNegative"},
        "rollbackDeadline": {"$ref": "#/$defs/NullableTimestamp"}}}

S['InstallationTransitionJournalV1'] = {
    "title": "S9.2 closed installation transition journal, written under the held fence only after every lease of the affected set is held; identity H('security.installation-transition-journal.v1', record)",
    "type": "object", "additionalProperties": False,
    "required": ["journalSchema", "kind", "intentDigest", "operation", "fromCoreClosure", "toCoreClosure", "fromStateSchema", "toStateSchema",
                 "fromStoreGeneration", "toStoreGeneration", "platformProfileSetBodyDigest", "preconditionGeneration", "rollbackDeadline",
                 "registryDigest", "registry", "affects", "leaseSet", "state", "fenceHeld", "writtenAfterAllLeasesHeld"],
    "properties": {
        "journalSchema": {"const": 1},
        "kind": {"const": "installation-transition"},
        "intentDigest": {"$ref": "#/$defs/Hex64", "description": "raw SHA-256 of the canonical admitted intent (= the mutation step inputDescriptorDigest, S15)"},
        "operation": {"$ref": "#/$defs/TransitionOperation"},
        "fromCoreClosure": {"$ref": "#/$defs/ClosureId"},
        "toCoreClosure": {"$ref": "#/$defs/ClosureId"},
        "fromStateSchema": {"$ref": "#/$defs/StateSchema"},
        "toStateSchema": {"$ref": "#/$defs/StateSchema"},
        "fromStoreGeneration": {"$ref": "#/$defs/I64NonNegative"},
        "toStoreGeneration": {"$ref": "#/$defs/I64NonNegative"},
        "platformProfileSetBodyDigest": {"$ref": "#/$defs/Hex64"},
        "preconditionGeneration": {"$ref": "#/$defs/I64NonNegative"},
        "rollbackDeadline": {"$ref": "#/$defs/NullableTimestamp"},
        "registryDigest": {"$ref": "#/$defs/Hex64", "description": "raw SHA-256 of the canonical sorted namespace registry frozen under the fence"},
        "registry": {"$ref": "#/$defs/NamespaceList"},
        "affects": {"enum": ["all-registered", "none"]},
        "leaseSet": {"$ref": "#/$defs/NamespaceList", "description": "the exact EXCLUSIVE lease set held (locator byte order) = core_transition_affected_namespaces over the frozen registry"},
        "state": {"enum": ["LEASED", "PREPARING", "PREPARED", "COMMITTED", "DONE", "ABORTED"]},
        "fenceHeld": {"const": True},
        "writtenAfterAllLeasesHeld": {"const": True}}}

S['TransitionIntentAdmissionV1'] = {
    "type": "object", "additionalProperties": False,
    "required": ["result", "refusals", "d9", "requiredFields", "operations"],
    "properties": {"result": {"enum": ["ADMIT", "REFUSE"]},
                   "refusals": {"type": "array", "maxItems": 64, "items": {"$ref": "#/$defs/TransitionRefusal"}},
                   "d9": {"$ref": "#/$defs/NullableD9"},
                   "requiredFields": {"$ref": "#/$defs/StringList"},
                   "operations": {"type": "array", "minItems": 5, "maxItems": 5, "items": {"$ref": "#/$defs/TransitionOperation"}}}}

S['TransitionJournalAdmissionV1'] = {
    "type": "object", "additionalProperties": False,
    "required": ["result", "refusals", "d9", "journalRef", "affects", "leaseSet", "identityDomain", "fenceHeldThroughout", "recovery", "trustedContextInputs"],
    "properties": {"result": {"enum": ["ADMIT", "REFUSE"]},
                   "refusals": {"type": "array", "maxItems": 64, "items": {"$ref": "#/$defs/TransitionRefusal"}},
                   "d9": {"$ref": "#/$defs/NullableD9"},
                   "journalRef": {"oneOf": [{"type": "null"}, {"type": "string", "pattern": "^security\\.installation-transition-journal\\.v1:[0-9a-f]{64}(?![\\s\\S])"}]},
                   "affects": {"enum": [None, "all-registered", "none"]},
                   "leaseSet": {"oneOf": [{"type": "null"}, {"$ref": "#/$defs/NamespaceList"}]},
                   "identityDomain": {"const": "security.installation-transition-journal.v1"},
                   "fenceHeldThroughout": {"const": True},
                   "recovery": {"type": "string"},
                   "trustedContextInputs": {"$ref": "#/$defs/StringList"}}}

S['TransitionRecoveryV1'] = {
    "title": "S9.2 crash recovery decision for a journaled installation transition (first act under the next fence)",
    "type": "object", "additionalProperties": False,
    "required": ["action", "journalStateAfter", "refusal", "d9", "reacquire", "fromStep", "rationale", "trustedContextInputs"],
    "properties": {"action": {"enum": ["ABORT", "RESUME-COMMIT", "RELEASE-ONLY", "QUARANTINE", "BUSY", "REFUSE"]},
                   "journalStateAfter": {"enum": [None, "DONE", "ABORTED"]},
                   "refusal": {"enum": [None, "MIGRATION.CORRUPT", "PROJECT.BUSY", "TRANSITION.FENCE_NOT_HELD"]},
                   "d9": {"$ref": "#/$defs/NullableD9"},
                   "reacquire": {"oneOf": [{"type": "null"}, {"$ref": "#/$defs/NamespaceList"}]},
                   "fromStep": {"oneOf": [{"type": "null"}, {"$ref": "#/$defs/I64Positive"}]},
                   "rationale": {"$ref": "#/$defs/NullableString"},
                   "trustedContextInputs": {"$ref": "#/$defs/StringList"}}}

ops = S['LeaseTraceV1']['properties']['trace']['items']['properties']['op']['enum']
if 'transition-journal' not in ops:
    ops.append('transition-journal')

doc['standing'] = doc['standing'].rstrip('.') + ". Post-reset v2 additions: AdmittedBoundaryInventoryV1 (S3 export, P3), RepairRecoveryAuthorizationV1 / RecoveryAuthorizationAdmissionV1 (S10.2, P9), InstallationTransitionIntentV1 / InstallationTransitionJournalV1 / TransitionIntentAdmissionV1 / TransitionJournalAdmissionV1 / TransitionRecoveryV1 (S9.2, P10) and the LeaseTraceV1 transition-journal op."
P.write_bytes((json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode())
print('schemas now', len(S), 'defs', len(D))
