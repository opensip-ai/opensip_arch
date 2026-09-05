#!/usr/bin/env python3
"""Retained checker for the adjudicated DELIVERY contract.

  DL-PROV      local provenance and promotion precedence
  DL-ELIG      blocking requires VERIFIED plus retained evidence
  DL-SUPPLY    canonical exact manifest, offline trust, atomic set and rollback
  DL-PROF      typed profile capabilities resolve in the live fact plane
  DL-AIRGAP    finite compatibility window and signed offline bridge semantics
  DL-PLATFORM  P-4a and the initial supported set are closed decisions
  DL-TS        TypeScript has one exact bundled process/identity/VFS/authority topology
  DL-SCOPE     the v1 external-scanner overlay rejects before attempt admission
  DL-EXPL      evaluator-class explain support is honest
  DL-TM        exact threat references resolve
  DL-ASSURE    IMPLEMENTABLE is never treated as demonstrated product evidence
  DL-D9        DELIVERY domain conditions map into D9's closed termination vocabulary

Usage: python3 artifacts/check-delivery.py [contract] [--selftest]
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import re
import sys

BINDING = "delivery.v2.json"
TM = "threat-model.v3.json"
FP = "fact-plane.v1.json"
OP = "operability.v2.json"
D9 = "d9-exit-contract.v1.6.json"
C2 = "c2-plan-stage-schema.v3.json"
RI = "resolved-inputs.v2.json"
HERE = pathlib.Path(__file__).resolve().parent

SUPPORTED = {"linux-x86_64-gnu", "linux-aarch64-gnu", "macos-aarch64",
             "macos-x86_64", "windows-x86_64-msvc"}
PROFILE_PROVIDERS = {
    "core": set(),
    "typescript-deep": {"typescript"},
    "rust-deep": {"rust"},
    "full": {"typescript", "rust"},
}
RELEASE_REQUIRED = {"schemaVersion", "manifestId", "releaseVersion", "releaseSequence",
                    "createdAt", "expiresAt", "artifacts", "dependencyEdges", "profiles",
                    "platforms", "formatCompatibility", "trust", "verificationPolicy",
                    "signatures"}
ARTIFACT_REQUIRED = {"artifactId", "version", "sha256", "sizeBytes", "mediaType",
                     "platformIds", "executable", "licenseIds", "dependencyIds"}
KEY_REQUIRED = {"keyId", "algorithm", "publicKey"}
SIGNATURE_REQUIRED = {"keyId", "algorithm", "signature"}
ROLE_REQUIRED = {"roleId", "keyIds", "threshold"}
ROOT_REQUIRED = {"schemaVersion", "rootVersion", "createdAt", "expiresAt", "keys",
                 "roles", "signatures"}
REVOCATION_REQUIRED = {"schemaVersion", "snapshotVersion", "createdAt", "expiresAt",
                       "revokedKeyIds", "revokedArtifactDigests", "signatures"}
POLICY_REQUIRED = {"rootVersion", "releaseRoleId", "revocationSnapshotVersion",
                   "offlineBundleRequired"}
BUNDLE_REQUIRED = {"schemaVersion", "trustedRootChain", "revocationSnapshot", "manifest",
                   "artifactPayloads", "bundleCreatedAt"}
TS_RUNTIME_IDENTITY_REQUIRED = {
    "schemaVersion", "nodeVersion", "v8Version", "modulesAbi", "platformId",
    "executableRelativePath", "executableSha256", "runtimePayloadSha256",
    "licenseNoticeSha256",
}
TS_PROVIDER_IDENTITY_REQUIRED = {
    "schemaVersion", "providerBuildId", "protocolMajor", "entrypointRelativePath",
    "entrypointSha256", "typescriptVersion", "typescriptCompilerSha256",
    "typescriptStdlibMerkleRoot", "defaultWorkBudgetProfileId",
    "defaultWorkBudgetProfileSha256", "licenseNoticeSha256",
}
TS_HANDSHAKE_REQUIRED = {
    "protocolMajor", "providerBuildId", "providerDescriptorSha256",
    "runtimeDescriptorSha256", "nodeVersion", "v8Version", "modulesAbi",
    "typescriptVersion", "typescriptCompilerSha256", "typescriptStdlibMerkleRoot",
    "defaultWorkBudgetProfileId", "defaultWorkBudgetProfileSha256", "platformId",
    "capabilities",
}
TS_HOST_FRAMES = {
    "Hello", "OpenUniverse", "SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal",
    "Analyze", "Cancel",
}
TS_WORKER_FRAMES = {
    "HelloAck", "UniverseAccepted", "SnapshotAccepted", "FactBatch", "Coverage",
    "Unavailable", "BudgetExhausted", "Complete", "Cancelled",
}
TS_FRAME_PAYLOADS = {
    "Hello": ("host-to-worker", "HelloV1", False),
    "OpenUniverse": ("host-to-worker", "OpenUniverseV1", False),
    "SnapshotManifest": ("host-to-worker", "SnapshotManifestV1", False),
    "SnapshotFileChunk": ("host-to-worker", "SnapshotFileChunkV1", False),
    "SnapshotSeal": ("host-to-worker", "SnapshotSealV1", False),
    "Analyze": ("host-to-worker", "AnalyzeV1", False),
    "Cancel": ("host-to-worker", "CancelV1", True),
    "HelloAck": ("worker-to-host", "HelloAckV1", False),
    "UniverseAccepted": ("worker-to-host", "UniverseAcceptedV1", False),
    "SnapshotAccepted": ("worker-to-host", "SnapshotAcceptedV1", False),
    "FactBatch": ("worker-to-host", "FactBatchV1", False),
    "Coverage": ("worker-to-host", "CoverageV1", False),
    "Unavailable": ("worker-to-host", "UnavailableV1", True),
    "BudgetExhausted": ("worker-to-host", "BudgetExhaustedV1", True),
    "Complete": ("worker-to-host", "CompleteV1", True),
    "Cancelled": ("worker-to-host", "CancelledV1", True),
}
TS_PAYLOAD_REQUIRED = {
    "HelloV1": {"hostBuildId", "expectedProviderDescriptorSha256",
                "expectedRuntimeDescriptorSha256", "limits"},
    "HelloAckV1": TS_HANDSHAKE_REQUIRED,
    "OpenUniverseV1": {"executionId", "snapshotId", "planId",
                       "planIntentCommitment", "providerId", "universe", "universeKey"},
    "UniverseAcceptedV1": {"executionId", "snapshotId", "planId", "universeKey"},
    "SnapshotManifestV1": {"snapshotId", "manifestSha256", "entries"},
    "SnapshotFileChunkV1": {"snapshotId", "path", "chunkIndex", "byteOffset", "bytes"},
    "SnapshotSealV1": {"snapshotId", "manifestSha256", "entryCount",
                       "totalFileBytes", "totalChunkCount"},
    "SnapshotAcceptedV1": {"snapshotId", "manifestSha256", "entryCount",
                           "totalFileBytes", "totalChunkCount"},
    "AnalyzeV1": {"analysisOrdinal", "executionId", "snapshotId", "planId",
                  "universeKey", "stageRequests"},
    "FactBatchV1": {"analysisOrdinal", "stageId", "batchIndex", "facts",
                    "batchCommitment"},
    "CoverageV1": {"analysisOrdinal", "stageId", "entries", "coverageCommitment"},
    "UnavailableV1": {"analysisOrdinal", "affectedStageIds", "reason", "coverage",
                      "coverageCommitment"},
    "BudgetExhaustedV1": {"analysisOrdinal", "triggerStageId", "dimension", "limit",
                          "observed", "coverage", "coverageCommitment"},
    "CompleteV1": {"analysisOrdinal", "stageResults", "factStreamCommitment",
                   "coverageStreamCommitment"},
    "CancelV1": {"executionId", "analysisOrdinal", "reason"},
    "CancelledV1": {"executionId", "analysisOrdinal", "observedPhase"},
}
TS_DEFINITION_REQUIRED = {
    "SnapshotEntryV1": {"path", "kind", "byteLength", "contentSha256", "linkTarget"},
    "ProviderWorkBudgetV1": {"sourceFilesVisited", "astNodesVisited",
                             "moduleResolutionQueries", "typeQueries", "factsEmitted",
                             "factBytesEmitted"},
    "StageRequestV1": {"stageId", "stageOrdinal", "operator", "providerId",
                       "dependsOn", "relations", "budget", "requestedCoverageDomain"},
    "SnapshotFileSubjectV1": {"path", "contentSha256", "byteLength"},
    "SubjectScopeV1": {"scopeKind", "snapshotId", "subjectCount",
                       "subjectScopeCommitment"},
    "RequestedCoverageDomainV1": {"subjectScope", "keys", "domainCommitment"},
    "AnchorRefV1": {"kind", "snapshotId", "path", "contentSha256", "startByte",
                    "endByte", "factId"},
    "FactCandidateV1": {"candidateOrdinal", "relation", "resolution", "layer",
                        "producer", "producerVersion", "schemaVersion", "language",
                        "sourceUniverseId", "targetUniverseId", "confidenceMillionths",
                        "relationSchemaId", "canonicalRelationPayload", "anchors"},
    "CoverageKeyV1": {"relation", "resolution", "sourceUniverseId", "targetUniverseId",
                      "subjectScopeCommitment", "producer", "producerVersion",
                      "schemaVersion"},
    "CoverageResultV1": {"stageId", "entryOrdinal", "coverageState", "key",
                         "deficiency"},
    "StageResultV1": {"stageId", "stageOrdinal", "factBatchCount", "factCount",
                      "coverageEntryCount", "factCommitment", "coverageCommitment"},
}
TS_OFFLINE_ASSETS = {
    ("node-executable", "typescript-runtime"),
    ("node-shared-runtime-payload", "typescript-runtime"),
    ("node-runtime-identity-descriptor", "typescript-runtime"),
    ("node-unicode-icu-data", "typescript-runtime"),
    ("typescript-worker-entrypoint", "typescript-provider"),
    ("typescript-provider-identity-descriptor", "typescript-provider"),
    ("typescript-default-work-budget-profile", "typescript-provider"),
    ("typescript-compiler-javascript", "typescript-provider"),
    ("typescript-standard-library-declarations", "typescript-provider"),
    ("node-v8-typescript-dependency-licenses-notices",
     "typescript-runtime+typescript-provider"),
}
TS_BUDGET_DIMENSIONS = ["sourceFilesVisited", "astNodesVisited",
                        "moduleResolutionQueries", "typeQueries", "factsEmitted",
                        "factBytesEmitted"]
TS_DEFAULT_BUDGET_PROFILE = {
    "schemaVersion": 1,
    "profileId": "typescript-provider-default-work-budget-v1",
    "budget": {
        "sourceFilesVisited": 200000,
        "astNodesVisited": 50000000,
        "moduleResolutionQueries": 1000000,
        "typeQueries": 5000000,
        "factsEmitted": 1000000,
        "factBytesEmitted": 1073741824,
    },
}
TS_DEFAULT_BUDGET_SHA256 = "bf7305a12d26a1938b615c861f995d66eac494915e6140c4942a2ea6f0846da6"
TS_RELATION_RESOLUTIONS = {
    "declares": "syntactic",
    "imports": "resolved-target",
    "references": "resolved-binding",
    "calls": "resolved-callee",
    "types": "checked",
    "reachability": "from-resolved-calls",
}
TS_CROSS_UNIVERSE_RELATIONS = ["imports", "calls", "references"]
REQUEST_ID_RE = re.compile(r"^req1_[0-9a-f]{32}$")
TS_WIRE_SCHEMA_SHA256 = "96ffbe7b63972c99409125d9f7c18def5a2ca20f1e00bfbc7770f1d8321ce726"
V1_OVERLAY_SCHEMA_SHA256 = "fd8a51301dfd7df66f387b406d3308983288f2a9083cc45de32bce3ca1c316a4"
V1_SCOPE_REASONS = {
    "FEATURE.REQUIRES_CAPABILITY_RUNTIME",
    "FEATURE.EXTERNAL_SCANNER_NOT_IN_V1",
    "FEATURE.RESIDENT_TOPOLOGY_NOT_IN_V1",
    "FEATURE.WORKFLOW_NOT_IN_V1",
    "FEATURE.REMOTE_COMPUTATION_NOT_IN_V1",
    "FEATURE.REPOSITORY_HOOK_NOT_IN_V1",
    "FEATURE.REPOSITORY_EXECUTION_GRANT_REQUIRED",
    "FEATURE.SEMANTIC_PROVIDER_NOT_IN_V1",
    "FEATURE.UNBUNDLED_HOST_BUILTIN_NOT_IN_V1",
    "FEATURE.CAPABILITY_GRANT_NOT_IN_V1",
    "FEATURE.TYPESCRIPT_STAGE_BUDGET_UNIT_NOT_IN_V1",
}
V1_SCOPE_AXIS_SPECS = {
    "intentKind": (
        "PlanIntent.intentKind", "planIntent.schema.intentKind",
        {"analysis": ("ALLOW", None), "stored-view": ("ALLOW", None)},
    ),
    "executionTopology": (
        "PlanIntent.analysis.executionTopology",
        "planIntent.analysisIntentV1.executionTopology",
        {"one-shot": ("ALLOW", None),
         "resident-single-project": ("DENY", "FEATURE.RESIDENT_TOPOLOGY_NOT_IN_V1"),
         "resident-multi-project": ("DENY", "FEATURE.RESIDENT_TOPOLOGY_NOT_IN_V1")},
    ),
    "workflowIntent": (
        "PlanIntent.analysis.workflowIntent", "planIntent.analysisIntentV1.workflowIntent",
        {"analysis": ("ALLOW", None),
         "repair": ("DENY", "FEATURE.WORKFLOW_NOT_IN_V1"),
         "mutation": ("DENY", "FEATURE.WORKFLOW_NOT_IN_V1")},
    ),
    "networkIntent": (
        "PlanIntent.analysis.networkIntent", "planIntent.analysisIntentV1.networkIntent",
        {"denied": ("ALLOW", None),
         "granted": ("DENY", "FEATURE.REQUIRES_CAPABILITY_RUNTIME")},
    ),
    "remoteComputation": (
        "PlanIntent.analysis.remoteComputation",
        "planIntent.analysisIntentV1.remoteComputation",
        {"local-only": ("ALLOW", None),
         "cloud-service": ("DENY", "FEATURE.REMOTE_COMPUTATION_NOT_IN_V1"),
         "model-service": ("DENY", "FEATURE.REMOTE_COMPUTATION_NOT_IN_V1")},
    ),
    "repositoryBuildScripts": (
        "PlanIntent.analysis.repositoryExecution.buildScripts",
        "planIntent.analysisIntentV1.repositoryExecution.values",
        {"disabled": ("ALLOW", None), "granted": ("ALLOW_IF", "rust-repository-execution")},
    ),
    "repositoryProceduralMacros": (
        "PlanIntent.analysis.repositoryExecution.proceduralMacros",
        "planIntent.analysisIntentV1.repositoryExecution.values",
        {"disabled": ("ALLOW", None), "granted": ("ALLOW_IF", "rust-repository-execution")},
    ),
    "repositoryCompilerPlugins": (
        "PlanIntent.analysis.repositoryExecution.compilerPlugins",
        "planIntent.analysisIntentV1.repositoryExecution.values",
        {"disabled": ("ALLOW", None),
         "granted": ("DENY", "FEATURE.REPOSITORY_HOOK_NOT_IN_V1")},
    ),
    "repositoryProjectHooks": (
        "PlanIntent.analysis.repositoryExecution.projectHooks",
        "planIntent.analysisIntentV1.repositoryExecution.values",
        {"disabled": ("ALLOW", None),
         "granted": ("DENY", "FEATURE.REPOSITORY_HOOK_NOT_IN_V1")},
    ),
    "contributionOrigin": (
        "PlanIntent.analysis.admissionDescriptor.contributions[*].origin",
        "planIntent.admissionDescriptorV1.contribution.origin",
        {"bundled": ("ALLOW", None), "tracked-project": ("ALLOW", None),
         "external": ("ALLOW", None)},
    ),
    "contributionAuthority": (
        "PlanIntent.analysis.admissionDescriptor.contributions[*].authority",
        "planIntent.admissionDescriptorV1.contribution.authority",
        {"declarative-rule": ("ALLOW", None),
         "host-builtin": ("ALLOW_IF", "bundled-host-builtin"),
         "semantic-provider": ("ALLOW_IF", "bundled-semantic-provider"),
         "external-scanner": ("DENY", "FEATURE.EXTERNAL_SCANNER_NOT_IN_V1"),
         "imperative-rule": ("DENY", "FEATURE.REQUIRES_CAPABILITY_RUNTIME"),
         "native": ("DENY", "FEATURE.REQUIRES_CAPABILITY_RUNTIME"),
         "wasm": ("DENY", "FEATURE.REQUIRES_CAPABILITY_RUNTIME")},
    ),
    "capability": (
        "PlanIntent.analysis.admissionDescriptor.capabilityGrants[*].capability",
        "planIntent.admissionDescriptorV1.capabilityGrant.capability",
        {"read-snapshot": ("ALLOW_IF", "allowed-fact-stage-grant"),
         "write-private-scratch": ("ALLOW_IF", "bundled-provider-process-grant"),
         "spawn-process": ("ALLOW_IF", "bundled-provider-process-grant"),
         "repository-execution": ("ALLOW_IF", "rust-repository-execution"),
         "network": ("DENY", "FEATURE.REQUIRES_CAPABILITY_RUNTIME")},
    ),
    "stageKind": (
        "PlanIntent.analysis.admissionDescriptor.workflow.stages[*].kind",
        "executionPlan.stageKinds",
        {"fact-derivation": ("ALLOW", None), "rule-evaluation": ("ALLOW", None),
         "policy-evaluation": ("ALLOW", None),
         "probe": ("DENY", "FEATURE.REQUIRES_CAPABILITY_RUNTIME")},
    ),
    "factDerivationOperator": (
        "PlanIntent.analysis.admissionDescriptor.workflow.stages[*][kind=fact-derivation].operator",
        "stageSchemas.kinds.fact-derivation.operatorAuthority",
        {"builtin-extractor": ("ALLOW", None),
         "semantic-provider": ("ALLOW_IF", "bundled-semantic-provider-stage"),
         "external-scanner": ("DENY", "FEATURE.EXTERNAL_SCANNER_NOT_IN_V1")},
    ),
    "typescriptStageBudgetUnit": (
        "PlanIntent.analysis.admissionDescriptor.workflow.stages[*][kind=fact-derivation,operator=semantic-provider,providerId=typescript-semantic].budget.unit-or-absent",
        "{absent} union planIntent.wireTypes.stageBudgetV1.unit",
        {"absent": ("ALLOW", None), "work-units": ("ALLOW", None),
         "milliseconds": ("DENY", "FEATURE.TYPESCRIPT_STAGE_BUDGET_UNIT_NOT_IN_V1"),
         "bytes": ("DENY", "FEATURE.TYPESCRIPT_STAGE_BUDGET_UNIT_NOT_IN_V1"),
         "items": ("DENY", "FEATURE.TYPESCRIPT_STAGE_BUDGET_UNIT_NOT_IN_V1")},
    ),
}
_C2_CHECKER = None


def load(name: str):
    path = HERE / name
    return json.loads(path.read_text()) if path.exists() else None


def _cbor_head(major: int, value: int) -> bytes:
    if value < 24:
        return bytes([(major << 5) | value])
    if value < 256:
        return bytes([(major << 5) | 24, value])
    if value < 65536:
        return bytes([(major << 5) | 25]) + value.to_bytes(2, "big")
    if value < 4294967296:
        return bytes([(major << 5) | 26]) + value.to_bytes(4, "big")
    if value < 18446744073709551616:
        return bytes([(major << 5) | 27]) + value.to_bytes(8, "big")
    raise OverflowError("value outside uint64")


def deterministic_cbor(value: object) -> bytes:
    """Small RFC-8949 deterministic encoder for retained commitment vectors."""
    if value is None:
        return b"\xf6"
    if value is False:
        return b"\xf4"
    if value is True:
        return b"\xf5"
    if isinstance(value, int):
        return _cbor_head(0, value) if value >= 0 else _cbor_head(1, -1 - value)
    if isinstance(value, str):
        encoded = value.encode("utf-8")
        return _cbor_head(3, len(encoded)) + encoded
    if isinstance(value, list):
        return _cbor_head(4, len(value)) + b"".join(
            deterministic_cbor(item) for item in value)
    if isinstance(value, dict):
        encoded_items = [(deterministic_cbor(key), deterministic_cbor(item))
                         for key, item in value.items()]
        encoded_items.sort(key=lambda pair: pair[0])
        return _cbor_head(5, len(encoded_items)) + b"".join(
            key + item for key, item in encoded_items)
    raise TypeError("unsupported deterministic-CBOR vector type")


def cbor_commitment(domain: str, value: object) -> str:
    digest = hashlib.sha256(domain.encode("utf-8") + b"\0" +
                            deterministic_cbor(value)).hexdigest()
    return f"sha256:{digest}"


def tm_ids(tm: dict) -> set[str]:
    return {p["id"] for p in tm.get("requiredProperties", [])}


def admission_errors(fx: dict, contract: dict) -> list[tuple[str, str]]:
    errs: list[tuple[str, str]] = []
    if "grant" not in fx:
        return errs
    schema = contract["admissionSchema"]["ContributionAdmission"]
    if fx.get("grant") not in schema["closedGrants"]:
        errs.append(("DL-PROV", "unknown grant"))
        return errs
    if fx.get("role") not in schema["closedRoles"]:
        errs.append(("DL-ELIG", "unknown role"))
    if fx.get("schemaState") != "VALID":
        errs.append(("DL-PROV", "schema validation was skipped or failed"))
    if fx.get("capabilityState") != "VALID":
        errs.append(("DL-PROV", "capability validation was skipped or failed"))
    role = fx.get("role")
    blocking = role in {"required", "blocking"}
    if fx.get("grant") == "local-development" and blocking:
        errs.append(("DL-PROV", "local-development provenance cannot satisfy policy authority"))
    if fx.get("grant") == "published" and fx.get("signatureState") != "VALID":
        errs.append(("DL-PROV", "published provenance lacks a valid signature"))
    state = fx.get("verificationState", "<missing>")
    if state not in schema["closedVerificationStates"]:
        errs.append(("DL-ELIG", "verification state is missing, null or unknown"))
    if blocking:
        if state != "VERIFIED":
            errs.append(("DL-ELIG", "blocking authority requires VERIFIED exactly"))
        if not fx.get("verificationEvidenceId"):
            errs.append(("DL-ELIG", "blocking authority lacks verificationEvidenceId"))
        if fx.get("overrideId"):
            errs.append(("DL-PROV", "override cannot promote local/unverified provenance"))
    return errs


def rollback_errors(fx: dict) -> list[tuple[str, str]]:
    errs: list[tuple[str, str]] = []
    if "manifestCounter" not in fx:
        return errs
    if fx["manifestCounter"] < fx["installedCounter"]:
        if not fx.get("forced"):
            errs.append(("DL-SUPPLY", "rollback was not refused"))
        elif not fx.get("recorded"):
            errs.append(("DL-SUPPLY", "forced downgrade was not audited"))
    return errs


def release_errors(fx: dict, contract: dict) -> list[tuple[str, str]]:
    errs: list[tuple[str, str]] = []
    supported = {x["platformId"] for x in contract["platformMatrix"]["supported"]}
    if fx.get("platformId") not in supported:
        errs.append(("DL-PLATFORM", "platform is not in the supported set"))
    if not fx.get("allArtifacts"):
        errs.append(("DL-SUPPLY", "exact profile artifact closure is incomplete"))
    threshold = contract["releaseManifestSchema"]["Trust"]["releaseRole"]["threshold"]
    if fx.get("signatures", threshold) < threshold:
        errs.append(("DL-SUPPLY", "signature threshold not met"))
    if fx.get("revoked"):
        errs.append(("DL-SUPPLY", "revoked release accepted"))
    if fx.get("expired"):
        errs.append(("DL-SUPPLY", "expired release accepted"))
    if fx.get("networkUsed"):
        errs.append(("DL-SUPPLY", "offline verification used the network"))
    return errs


def migration_outcome(fx: dict) -> str:
    major = fx["artifactMajor"]
    available = set(fx["bundleMajors"])
    if major in available:
        return "read" if major == fx["currentMajor"] else "migrate"
    bridge = set(fx.get("bridgeMajors", []))
    if major in bridge and fx.get("bridgeSignatureValid") is True and not fx.get("networkUsed"):
        return "migrate"
    return "migration-unavailable"


def c2_intent_fixture_errors(intent: dict, c2: dict, fp: dict | None) -> list[str]:
    """Validate DELIVERY fixtures with C-2's retained, exact PlanIntent validator."""
    global _C2_CHECKER
    if _C2_CHECKER is None:
        checker_path = HERE / "check-c2.py"
        spec = importlib.util.spec_from_file_location("opensip_check_c2", checker_path)
        if spec is None or spec.loader is None:
            return ["could not load the live C-2 retained validator"]
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _C2_CHECKER = module
    validator = getattr(_C2_CHECKER, "validate_plan_intent", None)
    if not callable(validator):
        return ["live C-2 checker does not expose validate_plan_intent"]
    relations = set((fp or {}).get("relationRegistry", {}).get("relations", {}))
    return [f"{code}: {message}" for code, message in validator(intent, c2, relations)]


def _pointer_mutate(value: dict, operations: list[dict]) -> dict:
    out = copy.deepcopy(value)
    for operation in operations:
        path = operation.get("path", "")
        if not path.startswith("/") or operation.get("op") not in {"set", "remove"}:
            raise ValueError("overlay fixture uses an unknown mutation operation")
        parts = [part.replace("~1", "/").replace("~0", "~")
                 for part in path.split("/")[1:]]
        if not parts:
            raise ValueError("overlay fixture may not replace the document root")
        parent = out
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        leaf = parts[-1]
        if operation["op"] == "set":
            if isinstance(parent, list):
                parent[int(leaf)] = copy.deepcopy(operation.get("value"))
            else:
                parent[leaf] = copy.deepcopy(operation.get("value"))
        elif isinstance(parent, list):
            del parent[int(leaf)]
        else:
            if leaf not in parent:
                raise ValueError("overlay remove targets an absent field")
            del parent[leaf]
    return out


def _c2_scope_enum_sets(c2: dict) -> dict[str, set[str]]:
    intent = c2.get("planIntent") or {}
    analysis = intent.get("analysisIntentV1") or {}
    admission = intent.get("admissionDescriptorV1") or {}
    repo_values = set((analysis.get("repositoryExecution") or {}).get("values", []))
    return {
        "intentKind": set((intent.get("schema") or {}).get("intentKind", [])),
        "executionTopology": set(analysis.get("executionTopology", [])),
        "workflowIntent": set(analysis.get("workflowIntent", [])),
        "networkIntent": set(analysis.get("networkIntent", [])),
        "remoteComputation": set(analysis.get("remoteComputation", [])),
        "repositoryBuildScripts": repo_values,
        "repositoryProceduralMacros": repo_values,
        "repositoryCompilerPlugins": repo_values,
        "repositoryProjectHooks": repo_values,
        "contributionOrigin": set((admission.get("contribution") or {}).get("origin", [])),
        "contributionAuthority": set((admission.get("contribution") or {}).get("authority", [])),
        "capability": set((admission.get("capabilityGrant") or {}).get("capability", [])),
        "stageKind": set((c2.get("executionPlan") or {}).get("stageKinds", [])),
        "factDerivationOperator": set((((c2.get("stageSchemas") or {}).get("kinds") or {})
                                        .get("fact-derivation") or {}).get(
                                            "operatorAuthority", [])),
        "typescriptStageBudgetUnit": {"absent"} | set(
            ((intent.get("wireTypes") or {}).get("stageBudgetV1") or {}).get("unit", [])),
    }


def _rust_repository_execution_ok(analysis: dict) -> bool:
    descriptor = analysis.get("admissionDescriptor") or {}
    repo = analysis.get("repositoryExecution") or {}
    if analysis.get("networkIntent") != "denied" or \
            repo.get("compilerPlugins") != "disabled" or repo.get("projectHooks") != "disabled":
        return False
    project_id = (descriptor.get("scope") or {}).get("projectId")
    grants = [g for g in descriptor.get("capabilityGrants", [])
              if g.get("capability") == "repository-execution"]
    if len(grants) != 1:
        return False
    grant = grants[0]
    expected_parameters = {
        "build-scripts": repo.get("buildScripts") == "granted",
        "network": False,
        "procedural-macros": repo.get("proceduralMacros") == "granted",
    }
    if grant.get("projectId") != project_id or grant.get("parameters") != expected_parameters:
        return False
    rust_contributions = [x for x in descriptor.get("contributions", [])
                          if x.get("origin") == "bundled" and
                          x.get("authority") == "semantic-provider" and
                          x.get("contributionId") == "rust-semantic"]
    if len(rust_contributions) != 1:
        return False
    grant_id = grant.get("grantId")
    rust_stages = [x for x in (descriptor.get("workflow") or {}).get("stages", [])
                   if x.get("kind") == "fact-derivation" and
                   x.get("operator") == "semantic-provider" and
                   x.get("providerId") == "rust-semantic" and
                   grant_id in x.get("capabilityGrants", [])]
    return len(rust_stages) >= 1


def v1_overlay_outcome(intent: dict) -> tuple[str, str | None]:
    """Reference decision for the closed v1 matrix; input is already C-2-valid."""
    if intent.get("intentKind") == "stored-view":
        return "ALLOW", None
    analysis = intent.get("analysis") or {}
    descriptor = analysis.get("admissionDescriptor") or {}
    direct = [
        (analysis.get("executionTopology"), {"resident-single-project", "resident-multi-project"},
         "FEATURE.RESIDENT_TOPOLOGY_NOT_IN_V1"),
        (analysis.get("workflowIntent"), {"repair", "mutation"},
         "FEATURE.WORKFLOW_NOT_IN_V1"),
        (analysis.get("networkIntent"), {"granted"},
         "FEATURE.REQUIRES_CAPABILITY_RUNTIME"),
        (analysis.get("remoteComputation"), {"cloud-service", "model-service"},
         "FEATURE.REMOTE_COMPUTATION_NOT_IN_V1"),
    ]
    for value, denied, reason in direct:
        if value in denied:
            return "DENY", reason
    repo = analysis.get("repositoryExecution") or {}
    if (repo.get("buildScripts") == "granted" or
            repo.get("proceduralMacros") == "granted") and \
            not _rust_repository_execution_ok(analysis):
        return "DENY", "FEATURE.REPOSITORY_EXECUTION_GRANT_REQUIRED"
    if repo.get("compilerPlugins") == "granted" or repo.get("projectHooks") == "granted":
        return "DENY", "FEATURE.REPOSITORY_HOOK_NOT_IN_V1"

    allowed_provider_ids = {"rust-semantic", "typescript-semantic"}
    semantic_provider_relations = set(TS_RELATION_RESOLUTIONS)
    contributions = descriptor.get("contributions", [])
    contribution_by_provider = {}
    for contribution in contributions:
        authority = contribution.get("authority")
        if authority in {"imperative-rule", "native", "wasm"}:
            return "DENY", "FEATURE.REQUIRES_CAPABILITY_RUNTIME"
        if authority == "external-scanner":
            return "DENY", "FEATURE.EXTERNAL_SCANNER_NOT_IN_V1"
        if authority == "host-builtin" and contribution.get("origin") != "bundled":
            return "DENY", "FEATURE.UNBUNDLED_HOST_BUILTIN_NOT_IN_V1"
        if authority == "semantic-provider":
            provider_id = contribution.get("contributionId")
            if contribution.get("origin") != "bundled" or provider_id not in allowed_provider_ids:
                return "DENY", "FEATURE.SEMANTIC_PROVIDER_NOT_IN_V1"
            contribution_by_provider[provider_id] = contribution

    stages = (descriptor.get("workflow") or {}).get("stages", [])
    for stage in stages:
        if stage.get("kind") == "probe":
            return "DENY", "FEATURE.REQUIRES_CAPABILITY_RUNTIME"
    for stage in stages:
        if stage.get("kind") == "fact-derivation":
            if stage.get("operator") == "external-scanner":
                return "DENY", "FEATURE.EXTERNAL_SCANNER_NOT_IN_V1"
            if stage.get("operator") == "semantic-provider" and \
                    (stage.get("providerId") not in contribution_by_provider or
                     stage.get("providerId") not in allowed_provider_ids or
                     not set(stage.get("relations", [])) <= semantic_provider_relations):
                return "DENY", "FEATURE.SEMANTIC_PROVIDER_NOT_IN_V1"
    for stage in stages:
        if stage.get("kind") == "fact-derivation" and \
                stage.get("operator") == "semantic-provider" and \
                stage.get("providerId") == "typescript-semantic":
            budget = stage.get("budget")
            unit = "absent" if budget is None else budget.get("unit")
            if unit not in {"absent", "work-units"}:
                return "DENY", "FEATURE.TYPESCRIPT_STAGE_BUDGET_UNIT_NOT_IN_V1"

    references: dict[str, list[dict]] = {}
    for stage in stages:
        for grant_id in stage.get("capabilityGrants", []):
            references.setdefault(grant_id, []).append(stage)
    for grant in descriptor.get("capabilityGrants", []):
        capability = grant.get("capability")
        if capability == "network":
            return "DENY", "FEATURE.REQUIRES_CAPABILITY_RUNTIME"
        if capability == "repository-execution":
            if not _rust_repository_execution_ok(analysis):
                return "DENY", "FEATURE.REPOSITORY_EXECUTION_GRANT_REQUIRED"
            continue
        refs = references.get(grant.get("grantId"), [])
        if not refs:
            return "DENY", "FEATURE.CAPABILITY_GRANT_NOT_IN_V1"
        if capability == "read-snapshot":
            if any(stage.get("kind") != "fact-derivation" for stage in refs):
                return "DENY", "FEATURE.CAPABILITY_GRANT_NOT_IN_V1"
        elif capability in {"write-private-scratch", "spawn-process"}:
            if any(stage.get("kind") != "fact-derivation" or
                   stage.get("operator") != "semantic-provider" or
                   stage.get("providerId") not in allowed_provider_ids for stage in refs):
                return "DENY", "FEATURE.CAPABILITY_GRANT_NOT_IN_V1"
    return "ALLOW", None


def _check_impl(c: dict, tm: dict | None, fp: dict | None, op: dict | None,
                d9: dict | None) -> list[str]:
    findings: list[str] = []

    # DL-PROV / DL-ELIG fixtures and structural precedence.
    pp = c.get("provenancePolicy", {})
    grants = {g.get("grant"): g for g in pp.get("grants", [])}
    if set(grants) != {"published", "local-development"}:
        findings.append("DL-PROV: provenance grant set is not closed")
    local = grants.get("local-development", {})
    if local.get("waives") != ["publisher signature ONLY"]:
        findings.append("DL-PROV: local grant waives more than the publisher signature")
    if not local.get("planIdVisible") or not local.get("boundTo"):
        findings.append("DL-PROV: local provenance is not identity-bound and Plan-visible")
    if "No override" not in pp.get("precedence", ""):
        findings.append("DL-PROV: override precedence can promote local provenance")
    if "separate" not in pp.get("promotion", "") or "audited" not in pp.get("promotion", ""):
        findings.append("DL-PROV: contribution promotion is not a distinct audited transition")
    for fx in c.get("deliveryFixtures", []):
        errs = admission_errors(fx, c) + rollback_errors(fx)
        codes = {code for code, _ in errs}
        if fx["valid"] and errs:
            findings.append(f"{errs[0][0]} {fx['id']}: expected valid — {errs[0][1]}")
        elif not fx["valid"]:
            if not errs:
                findings.append(f"{fx.get('violates')} {fx['id']}: expected rejection")
            elif fx.get("violates") not in codes:
                findings.append(f"{fx['id']}: rejected by {sorted(codes)}, not {fx.get('violates')}")
    required_delivery_fixtures = {
        "published-blocking-ok", "reject-unverified-blocking", "reject-missing-verification",
        "reject-null-verification", "reject-unknown-verification",
        "reject-verified-without-evidence", "reject-local-dev-override",
    }
    have = {x["id"] for x in c.get("deliveryFixtures", [])}
    if required_delivery_fixtures - have:
        findings.append("DL-ELIG: missing verification/provenance negative controls")

    # DL-PLATFORM / P-4a.
    platform = c.get("platformMatrix", {})
    supported = {x.get("platformId") for x in platform.get("supported", [])}
    if supported != SUPPORTED:
        findings.append(f"DL-PLATFORM: supported set differs from the closed initial set {sorted(SUPPORTED)}")
    for row in platform.get("supported", []):
        if row.get("defaultProfile") != "full" or not row.get("minimum"):
            findings.append(f"DL-PLATFORM {row.get('platformId')}: lacks full default or minimum OS/ABI")
    if "unlisted platform is unsupported" not in platform.get("supportRule", ""):
        findings.append("DL-PLATFORM: unlisted-platform default is not closed")
    rust = c.get("rustSemanticSubstrate", {})
    if rust.get("decision") != "bundled-pinned-rustc-driver-sidecar":
        findings.append("DL-PLATFORM: P-4a Rust substrate is undecided")
    if "not a security sandbox" not in rust.get("processModel", ""):
        findings.append("DL-PLATFORM: Rust sidecar overclaims a process capability boundary")
    for key in ("providerProtocol", "toolchainIdentity", "offlineAssets",
                "repositoryExecution", "upgradeRule"):
        if not rust.get(key):
            findings.append(f"DL-PLATFORM: Rust substrate omits {key}")
    if "provider-unavailable" not in rust.get("repositoryExecution", {}).get("withoutGrant", ""):
        findings.append("DL-PLATFORM: incomplete generated cfg can silently look resolved")
    excluded = set(c.get("initialProductScope", {}).get("excludedUntilMechanismExists", []))
    for phrase in ("imperative rule contributions", "Probe stages", "scenario-effectful execution"):
        if phrase not in excluded:
            findings.append(f"DL-PLATFORM: missing-mechanism feature not excluded: {phrase}")

    # DL-TS — exact process, signed identity, closed wire API and host authority.
    ts = c.get("typescriptSemanticSubstrate") or {}
    if ts.get("decision") != "bundled-node-worker-with-pinned-typescript-compiler":
        findings.append("DL-TS: TypeScript execution boundary is not the selected bundled Node worker")
    boundary = ts.get("executionBoundary", "")
    if not all(term in boundary for term in
               ("Rust orchestration host directly spawns", "private one-shot worker process",
                "never embedded", "system Node.js", "resident daemon")):
        findings.append("DL-TS: execution boundary leaves embedding/runtime/residency open")

    process = ts.get("processModel") or {}
    expected_cardinality = {
        "closed": True,
        "keyFields": ["ExecutionId", "SnapshotId", "TypeScriptSemanticUniverseKey"],
        "workersPerDistinctKey": 1,
        "shareAcrossMatchingTypeScriptStages": True,
        "multiplexDifferentUniverseKeys": False,
        "reuseAcrossExecutionIds": False,
        "retainAfterTerminal": False,
        "residentWorker": False,
    }
    if process.get("workerCardinality") != expected_cardinality:
        findings.append("DL-TS: typed process cardinality/reuse rule drifted")
    expected_ownership = {
        "closed": True,
        "host": ["spawn", "stdin-write", "stdout-read", "stderr-capture", "cancellation",
                 "process-fate", "protocol-validation", "fact-validation", "fact-admission",
                 "Coverage-admission", "durable-write", "Run-seal", "termination",
                 "scratch-cleanup"],
        "worker": ["one-universe TypeScript CompilerHost VFS",
                   "one-universe compiler Program state", "candidate-fact construction",
                   "candidate-Coverage construction"],
        "workerMayMintHostIdentities": False,
        "workerMayWriteDurableState": False,
        "workerMayDerivePolicyOrTermination": False,
    }
    if process.get("ownership") != expected_ownership:
        findings.append("DL-TS: host/worker process ownership is not exact")
    if not all(x in process.get("start", "") for x in
               ("SnapshotId", "PlanId", "TypeScriptSemanticUniverseKey")) or \
            not all(x in process.get("end", "") for x in
                    ("destroy its scratch directory", "never retained")):
        findings.append("DL-TS: worker start/end lifecycle is incomplete")

    packaging = ts.get("packaging") or {}
    if packaging.get("runtimeArtifactId") != "typescript-runtime" or \
            packaging.get("providerArtifactId") != "typescript-provider":
        findings.append("DL-TS: runtime/provider artifact ownership is not exact")
    launch = packaging.get("launch", "")
    if not all(x in launch for x in ("absolute bundled runtime path", "--no-addons",
                                     "does not invoke a shell", "PATH/NODE_PATH/NODE_OPTIONS",
                                     "npm", "bun", "deno")):
        findings.append("DL-TS: absolute offline launch contract is incomplete")
    edges = " ".join(packaging.get("releaseManifestEdges", []))
    if not all(x in edges for x in ("typescript-provider depends on typescript-runtime",
                                    "typescript-deep and full", "no semver range")):
        findings.append("DL-TS: signed profile dependency closure is incomplete")
    offline = ts.get("offlineAssets") or {}
    offline_pairs = {(x.get("assetId"), x.get("suppliedBy"))
                     for x in offline.get("required", []) if isinstance(x, dict)}
    if offline.get("closed") is not True or offline.get("systemFallback") is not False or \
            offline.get("networkFetch") is not False or offline_pairs != TS_OFFLINE_ASSETS or \
            len(offline.get("required", [])) != len(TS_OFFLINE_ASSETS) or \
            not all(x in offline.get("activationRule", "") for x in
                    ("signed exact artifact closure", "digest-verified before spawn",
                     "network-fetched assets are forbidden")):
        findings.append("DL-TS: exact offline Node/provider/compiler/stdlib/data/notices closure drifted")

    identity = ts.get("identity") or {}
    if not all(x in identity.get("versionSelectionRule", "") for x in
               ("exactly one Node.js", "exactly one TypeScript", "Ranges",
                "system-runtime substitution")):
        findings.append("DL-TS: compiler/runtime release pin is not exact")
    runtime_desc = identity.get("runtimeDescriptor") or {}
    provider_desc = identity.get("providerDescriptor") or {}
    if set(runtime_desc.get("closedRequired", [])) != TS_RUNTIME_IDENTITY_REQUIRED or \
            runtime_desc.get("canonicalization") != "RFC 8785 JCS" or \
            "signed typescript-runtime artifact" not in runtime_desc.get("binding", ""):
        findings.append("DL-TS: runtime identity descriptor is not closed and release-bound")
    if set(provider_desc.get("closedRequired", [])) != TS_PROVIDER_IDENTITY_REQUIRED or \
            provider_desc.get("canonicalization") != "RFC 8785 JCS" or \
            "signed typescript-provider artifact" not in provider_desc.get("binding", ""):
        findings.append("DL-TS: provider/compiler identity descriptor is not closed and release-bound")
    default_budget_profile = identity.get("defaultWorkBudgetProfile") or {}
    default_budget_bytes = json.dumps(
        default_budget_profile.get("profile"), sort_keys=True, separators=(",", ":"),
        ensure_ascii=False).encode("utf-8")
    default_budget_digest = hashlib.sha256(
        b"opensip.ts-provider.default-work-budget-profile.v1\0" +
        default_budget_bytes).hexdigest()
    if default_budget_profile.get("path") != \
            "typescript-provider/default-work-budget-profile.v1.json" or \
            default_budget_profile.get("canonicalization") != "RFC 8785 JCS" or \
            default_budget_profile.get("domain") != \
            "opensip.ts-provider.default-work-budget-profile.v1\u0000" or \
            set(default_budget_profile.get("closedRequired", [])) != {
                "schemaVersion", "profileId", "budget"} or \
            default_budget_profile.get("profile") != TS_DEFAULT_BUDGET_PROFILE or \
            default_budget_profile.get("sha256") != TS_DEFAULT_BUDGET_SHA256 or \
            default_budget_digest != TS_DEFAULT_BUDGET_SHA256 or \
            not all(term in default_budget_profile.get("binding", "") for term in
                    ("provider descriptor", "HelloAckV1", "PlanId-bound")):
        findings.append("DL-TS: signed default TypeScript work-budget profile drifted")
    if set(identity.get("handshakeRequired", [])) != TS_HANDSHAKE_REQUIRED:
        findings.append("DL-TS: handshake cannot prove exact runtime/compiler/provider identity")
    if not all(x in identity.get("hostValidation", "") for x in
               ("Before sending source bytes", "compares every handshake identity",
                "provider-protocol")):
        findings.append("DL-TS: host does not validate identity before source disclosure")
    plan_rule = identity.get("planIdRule", "")
    if not all(x in plan_rule for x in
               ("PlanId commits manifestId", "capabilityManifestId", "artifact IDs and sha256",
                "protocolMajor", "Node/V8/modules ABI", "TypeScript version/compiler digest",
                "stdlib Merkle root", "defaultWorkBudgetProfileId",
                "defaultWorkBudgetProfileSha256",
                "resolved-inputs TypeScript semantic-universe")):
        findings.append("DL-TS: PlanId identity closure is incomplete")

    ts_protocol = ts.get("providerProtocol") or {}
    if ts_protocol.get("transport") != \
            "bidirectional inherited pipes: length-delimited canonical CBOR on stdin/stdout" or \
            ts_protocol.get("major") != 1:
        findings.append("DL-TS: private transport/protocol major is not exact")
    if set(ts_protocol.get("closedHostToWorkerFrames", [])) != TS_HOST_FRAMES or \
            set(ts_protocol.get("closedWorkerToHostFrames", [])) != TS_WORKER_FRAMES:
        findings.append("DL-TS: protocol frame vocabulary is not closed")
    frame_rule = ts_protocol.get("frameIntegrity", "")
    if not all(x in frame_rule for x in ("uint64 big-endian", "32 raw SHA-256",
                                         "canonical-CBOR", "non-frame stdout byte",
                                         "PROVIDER.PROTOCOL_VIOLATION")):
        findings.append("DL-TS: framing/integrity/stdout fault fate is incomplete")

    wire = ts_protocol.get("wireSchema") or {}
    wire_bytes = json.dumps(wire, sort_keys=True, separators=(",", ":"),
                            ensure_ascii=False).encode("utf-8")
    wire_digest = hashlib.sha256(b"opensip.delivery.ts-wire-schema.v1\0" + wire_bytes).hexdigest()
    expected_wire_commitment = {
        "algorithm": "SHA-256",
        "canonicalization": "UTF-8 JSON with object keys sorted, no insignificant whitespace, Unicode emitted directly; the wireSchema object only",
        "domain": "opensip.delivery.ts-wire-schema.v1\u0000",
        "sha256": TS_WIRE_SCHEMA_SHA256,
    }
    if ts_protocol.get("wireSchemaCommitment") != expected_wire_commitment or \
            wire_digest != TS_WIRE_SCHEMA_SHA256:
        findings.append("DL-TS-WIRE: closed protocol-major-1 wire schema commitment drifted")
    cbor = wire.get("canonicalCbor") or {}
    if cbor.get("standard") != "RFC 8949 core deterministic encoding" or \
            set(cbor.get("closedDataModel", [])) != {
                "null", "false", "true", "uint64", "negative-int64", "UTF-8-NFC-text",
                "byte-string", "definite-array", "definite-text-keyed-map"} or \
            set(cbor.get("forbidden", [])) != {
                "floating-point", "tags", "indefinite-length items", "non-shortest integers",
                "duplicate map keys", "non-NFC text", "unknown map fields"} or \
            "no ignore-unknown" not in cbor.get("decodeRule", ""):
        findings.append("DL-TS-WIRE: deterministic CBOR data model/unknown-field rule drifted")
    limits = wire.get("limits") or {}
    expected_limits = {
        "maxFramePayloadBytes": 67108864, "maxSnapshotChunkBytes": 1048576,
        "maxSnapshotEntries": 200000, "maxAnalyzeStages": 1024,
        "maxRelationsPerStage": 64, "maxRequestedCoverageKeysPerStage": 128,
        "maxFactBatchFacts": 4096,
        "maxFactCandidatePayloadBytes": 1048576,
        "maxCoverageEntriesPerFrame": 4096, "maxStderrBytes": 262144,
    }
    if any(limits.get(k) != v for k, v in expected_limits.items()) or \
            "rejected before allocation" not in limits.get("limitRule", "") or \
            "uint64 overflow" not in limits.get("limitRule", ""):
        findings.append("DL-TS-WIRE: protocol byte/count limits are incomplete or not exact")
    envelope = wire.get("frameEnvelope") or {}
    if envelope.get("closed") is not True or \
            set(envelope.get("required", [])) != {"protocolMajor", "frameType", "sequence", "payload"} or \
            envelope.get("optional") != [] or \
            set((envelope.get("fields") or {})) != {"protocolMajor", "frameType", "sequence", "payload"}:
        findings.append("DL-TS-WIRE: frame envelope is not the exact closed shape")

    frame_schemas = wire.get("frameSchemas") or {}
    if set(frame_schemas) != set(TS_FRAME_PAYLOADS):
        findings.append("DL-TS-WIRE: frameSchemas does not cover the exact frame vocabulary")
    for frame_name, (direction, payload_type, terminal) in TS_FRAME_PAYLOADS.items():
        if frame_schemas.get(frame_name) != {
                "direction": direction, "payloadType": payload_type, "terminal": terminal}:
            findings.append(f"DL-TS-WIRE: {frame_name} frame binding drifted")
    payloads = wire.get("payloadSchemas") or {}
    if set(payloads) != set(TS_PAYLOAD_REQUIRED):
        findings.append("DL-TS-WIRE: payload schema set is not total over protocol-major 1")
    for payload_name, required_fields in TS_PAYLOAD_REQUIRED.items():
        schema = payloads.get(payload_name) or {}
        if schema.get("closed") is not True or schema.get("optional") != [] or \
                set(schema.get("required", [])) != required_fields or \
                set((schema.get("fields") or {})) != required_fields:
            findings.append(f"DL-TS-WIRE: {payload_name} is not an exact closed payload")
    definitions = wire.get("definitions") or {}
    for definition_name, required_fields in TS_DEFINITION_REQUIRED.items():
        definition = definitions.get(definition_name) or {}
        if definition.get("closed") is not True or \
                set(definition.get("required", [])) != required_fields or \
                (definition_name != "AnchorRefV1" and
                 set((definition.get("fields") or {})) != required_fields):
            findings.append(f"DL-TS-WIRE: {definition_name} is not an exact closed nested type")
    budget_def = definitions.get("ProviderWorkBudgetV1") or {}
    if list(budget_def.get("required", [])) != TS_BUDGET_DIMENSIONS or \
            set((budget_def.get("fields") or {})) != set(TS_BUDGET_DIMENSIONS) or \
            "no unlimited sentinel" not in budget_def.get("zeroRule", "") or \
            not all(term in budget_def.get("authoritativeSource", "") for term in
                    ("stageRequestProjection.budgetProjection", "all six maxima",
                     "signed TypeScript provider budget profile", "sole")):
        findings.append("DL-TS-WIRE: deterministic provider budget shape/units drifted")
    subject_scope_def = definitions.get("SubjectScopeV1") or {}
    requested_domain_def = definitions.get("RequestedCoverageDomainV1") or {}
    if not all(term in subject_scope_def.get("membershipRule", "") for term in
               ("exactly every kind=file", "Both sides reconstruct", "membership",
                "non-membership")) or \
            not all(term in (requested_domain_def.get("fields") or {}).get(
                "domainCommitment", "") for term in
                    ("opensip.ts-provider.requested-coverage-domain.v1",
                     "{subjectScope,keys}", "excluded from the preimage")) or \
            not all(term in requested_domain_def.get("workerRule", "") for term in
                    ("recomputes subjectScope", "missing", "duplicate", "unordered",
                     "unrequested", "provider-protocol")):
        findings.append("DL-TS-WIRE: requested Coverage subject/domain type is incomplete")
    fact_candidate = definitions.get("FactCandidateV1") or {}
    fact_record_contract = (fp or {}).get("factRecordContractV1") or {}
    fact_component_ids = fact_record_contract.get("componentIds") or {}
    live_candidate_schema = fact_record_contract.get("candidateSchema") or {}
    live_payload_registry = fact_record_contract.get(
        "relationPayloadSchemaRegistryV1") or {}
    live_payload_schemas = live_payload_registry.get("schemas") or {}
    live_admission_mapping = fact_record_contract.get("candidateToAdmittedMapping") or {}
    live_fact_id = fact_record_contract.get("factIdContract") or {}
    expected_fact_join = {
        "source": "artifacts/fact-plane.v1.json#factRecordContractV1",
        "contractId": "opensip.fact-record.v1",
        "candidateSchemaId": "opensip.fact-candidate.v1",
        "relationPayloadRegistryId": "opensip.relation-payload-registry.v1",
        "candidateAdmissionMappingId": "opensip.fact-candidate-admission.v1",
        "factIdContractId": "opensip.fact-id.v1",
        "sourceSpanSchemaId": "opensip.source-span.v1",
        "anchorSchemaId": "opensip.anchor-ref.v1",
        "providerProfile": {"providerId": "typescript-semantic", "language": "typescript"},
        "conformanceVectorId": "fact-id-v1-typescript-declares",
        "requestIdInvarianceVectorId": "fact-id-v1-request-id-invariance",
    }
    expected_component_ids = {
        "factCandidate": "opensip.fact-candidate.v1",
        "relationPayloadRegistry": "opensip.relation-payload-registry.v1",
        "candidateAdmission": "opensip.fact-candidate-admission.v1",
        "factId": "opensip.fact-id.v1",
        "sourceSpan": "opensip.source-span.v1",
        "anchorRef": "opensip.anchor-ref.v1",
    }
    live_ts_profile = next((profile for profile in fact_record_contract.get(
        "providerProfiles", []) if isinstance(profile, dict) and
        profile.get("providerId") == "typescript-semantic"), {})
    live_ts_vector = next((vector for vector in fact_record_contract.get("vectors", [])
                           if isinstance(vector, dict) and
                           vector.get("id") == "fact-id-v1-typescript-declares"), {})
    if fact_candidate.get("factRecordJoin") != expected_fact_join or \
            fact_record_contract.get("contractId") != "opensip.fact-record.v1" or \
            fact_component_ids != expected_component_ids or \
            live_candidate_schema.get("id") != "opensip.fact-candidate.v1" or \
            live_candidate_schema.get("closed") is not True or \
            live_candidate_schema.get("additionalProperties") is not False or \
            live_candidate_schema.get("optional") != [] or \
            set(live_candidate_schema.get("required", [])) != \
            TS_DEFINITION_REQUIRED["FactCandidateV1"] or \
            set((live_candidate_schema.get("fields") or {})) != \
            TS_DEFINITION_REQUIRED["FactCandidateV1"] or \
            live_ts_profile != {"providerId": "typescript-semantic",
                                "language": "typescript"} or \
            live_payload_registry.get("id") != "opensip.relation-payload-registry.v1" or \
            live_admission_mapping.get("id") != "opensip.fact-candidate-admission.v1" or \
            live_fact_id.get("id") != "opensip.fact-id.v1" or \
            len(live_fact_id.get("preimageFields", [])) != 14 or \
            (live_ts_vector.get("candidate") or {}).get("producer") != \
            "typescript-semantic" or \
            (fact_record_contract.get("requestIdInvarianceVector") or {}).get("id") != \
            "fact-id-v1-request-id-invariance" or \
            not all(x in fact_candidate.get("hostJoin", "") for x in
                    ("opensip.fact-candidate.v1", "never an admitted fact",
                     "opensip.fact-candidate-admission.v1",
                     "opensip.relation-payload-registry.v1", "opensip.anchor-ref.v1",
                     "opensip.fact-record.v1", "opensip.fact-id.v1",
                     "candidateOrdinal", "RequestId")):
        findings.append("DL-TS-FACT: FactCandidateV1 exact FACT-PLANE admission/FACT-ID join drifted")
    field_destinations = live_admission_mapping.get("fieldDestinations") or {}
    if set(field_destinations) != TS_DEFINITION_REQUIRED["FactCandidateV1"] or \
            field_destinations.get("candidateOrdinal", "<missing>") is not None or \
            set((live_admission_mapping.get("hostInjected") or {})) != {
                "snapshotId", "factId"}:
        findings.append("DL-TS-FACT: candidate-to-admitted field mapping is not total")
    for relation, resolution in TS_RELATION_RESOLUTIONS.items():
        payload_schema = live_payload_schemas.get(relation) or {}
        live_relation = ((fp or {}).get("relationRegistry", {}).get(
            "relations", {}) or {}).get(relation) or {}
        if payload_schema.get("schemaId") != f"opensip.relation.{relation}.v1" or \
                payload_schema.get("schemaVersion") != 1 or \
                payload_schema.get("closed") is not True or \
                payload_schema.get("universeRule") not in {"same-only", "admitted-target"} or \
                resolution not in live_relation.get("ladder", []):
            findings.append(f"DL-TS-FACT: host relation payload join drifted for {relation}")
    anchor_ref = definitions.get("AnchorRefV1") or {}
    live_anchor = fact_record_contract.get("anchorSchema") or {}
    if "factRecordContractV1.anchorSchema" not in anchor_ref.get("join", "") or \
            live_anchor.get("id") != "opensip.anchor-ref.v1" or \
            set(live_anchor.get("required", [])) != \
            TS_DEFINITION_REQUIRED["AnchorRefV1"]:
        findings.append("DL-TS-FACT: AnchorRefV1 drifted from opensip.anchor-ref.v1")
    coverage_key = definitions.get("CoverageKeyV1") or {}
    c2_live = load(C2)
    live_coverage_fields = {item.get("field") for item in
                            (c2_live or {}).get("coverageKey", {}).get("key", [])}
    if set(coverage_key.get("required", [])) != live_coverage_fields or \
            "Field-for-field exact" not in coverage_key.get("join", ""):
        findings.append("DL-TS-WIRE: CoverageKeyV1 drifted from live C-2")
    coverage_result = definitions.get("CoverageResultV1") or {}
    if not all(x in coverage_result.get("completenessRule", "") for x in
               ("every full CoverageKeyV1", "exactly one entry",
                "Missing, duplicate or unrequested", "provider-protocol")):
        findings.append("DL-TS-WIRE: Coverage attribution/completeness is not exact")
    universe_type = definitions.get("TypeScriptSemanticUniverseV1", "")
    universe_key = definitions.get("TypeScriptSemanticUniverseKey", "")
    if "resolved-inputs.v2.json#planIdContract.semanticUniverseSchemas.typescript-v1" \
            not in universe_type or not all(x in universe_key for x in
                                            ("opensip.typescript-universe.v1", "CVE1", "SHA-256")):
        findings.append("DL-TS-WIRE: OpenUniverse lacks an exact RI universe/key join")
    ri_live = load(RI)
    ri_ts_schema = (((ri_live or {}).get("planIdContract") or {}).get(
        "semanticUniverseSchemas") or {}).get("typescript-v1") or {}
    expected_ri_ts_fields = {
        "schemaVersion", "manifestId", "capabilityManifestId", "runtimeArtifactId",
        "runtimeArtifactSha256", "providerArtifactId", "providerArtifactSha256",
        "runtimeDescriptorSha256", "providerDescriptorSha256", "protocolMajor",
        "providerBuildId", "nodeVersion", "v8Version", "modulesAbi", "typescriptVersion",
        "typescriptCompilerSha256", "typescriptStdlibMerkleRoot", "platformId",
        "resolvedInputs",
    }
    if ri_ts_schema.get("closed") is not True or \
            set(ri_ts_schema.get("required", [])) != expected_ri_ts_fields or \
            ri_ts_schema.get("constants") != {"schemaVersion": 1,
                                               "runtimeArtifactId": "typescript-runtime",
                                               "providerArtifactId": "typescript-provider"}:
        findings.append("DL-TS-WIRE: live RI TypeScriptSemanticUniverseV1 shape drifted")

    canonical_provider_join = ts_protocol.get("canonicalProviderIdJoin") or {}
    c2_full = next((fixture for fixture in (c2_live or {}).get("planIntentFixtures", [])
                    if fixture.get("id") == "valid-full-profile-semantic-providers"), {})
    c2_full_intent = c2_full.get("intent") or {}
    c2_full_stages = (((c2_full_intent.get("analysis") or {}).get(
        "admissionDescriptor") or {}).get("workflow") or {}).get("stages", [])
    c2_semantic_stages = [stage for stage in c2_full_stages
                          if isinstance(stage, dict) and
                          stage.get("operator") == "semantic-provider"]
    c2_provider_ids = {stage.get("providerId") for stage in c2_semantic_stages}
    c2_ts_stage = next((stage for stage in c2_semantic_stages
                        if stage.get("providerId") == "typescript-semantic"), {})
    ri_full = next((fixture for fixture in (((ri_live or {}).get("planIdContract") or {})
                   .get("goldenVectors") or {}).get("positive", [])
                   if fixture.get("id") == "planid-v1-ci-full-providers"), {})
    ri_full_input = ri_full.get("planInputConstruction") or {}
    ri_provider_ids = {universe.get("providerId") for universe in
                       ri_full_input.get("semanticUniverses", [])
                       if isinstance(universe, dict)}
    full_profile = next((profile for profile in c.get("installProfiles", {}).get(
        "profiles", []) if profile.get("profile") == "full"), {})
    full_manifest_providers = {
        provider.get("providerId"): provider for provider in
        (full_profile.get("capabilityManifest") or {}).get("providers", [])
        if isinstance(provider, dict)
    }
    expected_provider_join = {
        "closed": True,
        "canonicalProviderIds": ["rust-semantic", "typescript-semantic"],
        "aliasesAccepted": False,
        "c2Fixture": "c2-plan-stage-schema.v3.json#planIntentFixtures[id=valid-full-profile-semantic-providers]",
        "c2ExpectedPlanIntentCommitment":
            "sha256:bd03b1c6935a5941596d81d1a0bb88cfff353f605e087555f22932b2afdff7d1",
        "deliveryOverlayOutcome": "ALLOW",
        "typescriptStageSelection": {
            "stageId": "s3", "providerId": "typescript-semantic",
            "relations": ["declares", "references"],
            "selectedBy": "wireSchema.multiStageAnalyze"},
        "rustStageSelection": {
            "stageId": "s2", "providerId": "rust-semantic",
            "relations": ["declares", "references"],
            "selectedBy": "rustSemanticSubstrate.providerProtocol"},
        "riVector": "resolved-inputs.v2.json#planIdContract.goldenVectors.positive[id=planid-v1-ci-full-providers]",
        "riExpectedPlanIntentCommitment":
            "sha256:bd03b1c6935a5941596d81d1a0bb88cfff353f605e087555f22932b2afdff7d1",
        "riExpectedPlanId":
            "plan1:sha256:86ccc0baa679dec956c0ca310889798e6b45ebbc7e11157f71e636dbf2f68401",
        "joinRule": "The exact C-2 full-profile fixture must validate and ALLOW under the DELIVERY overlay; its two canonical provider IDs must equal the two RI semanticUniverses provider IDs and the selected DELIVERY capability-manifest provider IDs. The TypeScript selector must select s3 without aliasing or renaming.",
    }
    if canonical_provider_join != expected_provider_join or \
            c2_full.get("expectedCommitment") != \
            expected_provider_join["c2ExpectedPlanIntentCommitment"] or \
            c2_provider_ids != {"rust-semantic", "typescript-semantic"} or \
            c2_ts_stage != {"kind": "fact-derivation", "stageId": "s3",
                            "relations": ["declares", "references"],
                            "operator": "semantic-provider",
                            "providerId": "typescript-semantic",
                            "capabilityGrants": ["grant-read", "grant-spawn"],
                            "dependsOn": ["s1"]} or \
            v1_overlay_outcome(c2_full_intent) != ("ALLOW", None) or \
            ri_full.get("expectedPlanIntentCommitment") != \
            expected_provider_join["riExpectedPlanIntentCommitment"] or \
            ri_full_input.get("planIntentCommitment") != \
            expected_provider_join["riExpectedPlanIntentCommitment"] or \
            ri_full.get("expectedPlanId") != expected_provider_join["riExpectedPlanId"] or \
            ri_provider_ids != {"rust-semantic", "typescript-semantic"} or \
            (full_manifest_providers.get("typescript-semantic") or {}).get(
                "relations") != TS_RELATION_RESOLUTIONS or \
            (full_manifest_providers.get("rust-semantic") or {}).get(
                "relations") != TS_RELATION_RESOLUTIONS:
        findings.append("DL-TS-JOIN: canonical C-2/RI/DELIVERY full-profile provider seam drifted")
    for error in c2_intent_fixture_errors(c2_full_intent, c2_live or {}, fp):
        findings.append(f"DL-TS-JOIN: canonical full-profile fixture is not C-2 valid — {error}")

    ordering = ts_protocol.get("ordering") or {}
    if ordering.get("closed") is not True or ordering.get("oneAnalyzePerWorker") is not True or \
            ordering.get("normalPhases") != [
                "Hello/HelloAck", "OpenUniverse/UniverseAccepted",
                "SnapshotManifest/SnapshotFileChunk*/SnapshotSeal/SnapshotAccepted", "Analyze",
                "per-stage FactBatch*/Coverage", "Complete", "zero-exit/EOF"] or \
            not all(x in ordering.get("stageOrder", "") for x in
                    ("stageRequests order", "batchIndex 0..n-1", "exactly one Coverage")) or \
            not all(x in ordering.get("sequenceRule", "") for x in
                    ("independent uint64 sequence", "beginning at zero", "exactly one",
                     "provider-protocol")) or \
            "Unavailable is permitted only immediately after Analyze" not in \
            ordering.get("unavailableTerminal", "") or \
            "no later protocol frame" not in ordering.get("budgetTerminal", ""):
        findings.append("DL-TS-WIRE: protocol ordering/state machine is missing or permissive")

    multi = wire.get("multiStageAnalyze") or {}
    expected_multi_typed = {
        "closed": True,
        "analyzeFramesPerWorker": 1,
        "selectedStageKind": "fact-derivation",
        "selectedOperator": "semantic-provider",
        "selectedProviderId": "typescript-semantic",
        "stageSet": "ALL_AND_ONLY_MATCHING_BATCHABLE_STAGES",
        "stageOrder": "VERIFIED_EXECUTION_PLAN_LOGICAL_ORDER",
        "externalDependencies": "COMPLETE_BEFORE_ANALYZE",
        "intraGroupDependencies": "EARLIER_STAGE_REQUEST_ONLY",
        "dependencyPathLeavingAndReentering": "REJECT_PLAN_BEFORE_PROVIDER_SPAWN",
        "stageOutputOrder": "FACT_BATCH_ZERO_OR_MORE_THEN_EXACTLY_ONE_COVERAGE",
        "resultAttribution": "EXACT_STAGE_ID",
        "terminalStageResultCardinality": "BIJECTION_WITH_STAGE_REQUESTS",
        "admissionAtomicity": "WHOLE_ANALYZE_AFTER_COMPLETE_COMMITMENTS_ZERO_EXIT_EOF",
    }
    if any(multi.get(k) != v for k, v in expected_multi_typed.items()) or \
            not all(x in multi.get("selection", "") for x in
                    ("all and only C-2", "operator=semantic-provider",
                     "providerId=typescript-semantic", "OpenUniverse.universeKey")) or \
            not all(x in multi.get("batchability", "") for x in
                    ("dependency outside", "intra-set dependencies", "leaves the set",
                     "rejects the ExecutionPlan before provider spawn")) or \
            not all(x in multi.get("completeness", "") for x in
                    ("bijection with stageRequests", "counts/commitments",
                     "CoverageResultV1 independently")):
        findings.append("DL-TS-WIRE: one-Analyze multi-stage selection/attribution/terminal semantics drifted")

    stage_projection = wire.get("stageRequestProjection") or {}
    budget_projection = stage_projection.get("budgetProjection") or {}
    absent_budget = budget_projection.get("absent") or {}
    work_unit_budget = budget_projection.get("work-units") or {}
    expected_absent_budget = TS_DEFAULT_BUDGET_PROFILE["budget"]
    expected_field_projection = {
        "stageId", "stageOrdinal", "operator", "providerId", "dependsOn", "relations",
        "budget", "requestedCoverageDomain",
    }
    if stage_projection.get("closed") is not True or \
            "resolved-inputs.v2.json#planIdContract.planDescriptorSchema.workflow" not in \
            stage_projection.get("sourceContract", "") or \
            stage_projection.get("outputType") != "StageRequestV1" or \
            set((stage_projection.get("fieldProjection") or {})) != expected_field_projection or \
            "absent emit []" not in (stage_projection.get("fieldProjection") or {}).get(
                "dependsOn", "") or \
            "no global budget" not in (stage_projection.get("fieldProjection") or {}).get(
                "budget", ""):
        findings.append("DL-TS-PROJECTION: C-2 stage to StageRequestV1 projection is not total")
    if budget_projection.get("closed") is not True or \
            budget_projection.get("wireDimensionsInOrder") != TS_BUDGET_DIMENSIONS or \
            budget_projection.get("admittedC2InputDomain") != ["absent", "work-units"] or \
            budget_projection.get("preAdmissionDeniedC2Units") != \
            ["milliseconds", "bytes", "items"] or \
            absent_budget.get("profileId") != TS_DEFAULT_BUDGET_PROFILE["profileId"] or \
            absent_budget.get("profileSha256") != TS_DEFAULT_BUDGET_SHA256 or \
            absent_budget.get("output") != expected_absent_budget or \
            work_unit_budget.get("minimum") != 1 or \
            work_unit_budget.get("maximum") != 9223372036854775807 or \
            not all(term in work_unit_budget.get("rule", "") for term in
                    ("unit:work-units", "exact uint64 value L", "six")) or \
            not all(term in budget_projection.get("unsupportedUnitFate", "") for term in
                    ("milliseconds", "bytes", "items", "request-validation",
                     "FEATURE.TYPESCRIPT_STAGE_BUDGET_UNIT_NOT_IN_V1",
                     "never reach PlanId")):
        findings.append("DL-TS-PROJECTION: exact budget defaults/unit projection drifted")
    projection_vectors = {vector.get("id"): vector for vector in
                          stage_projection.get("vectors", []) if isinstance(vector, dict)}
    absent_vector = projection_vectors.get("stage-request-absent-depends-and-budget") or {}
    present_vector = projection_vectors.get(
        "stage-request-present-depends-and-work-units") or {}
    if (absent_vector.get("expected") or {}).get("dependsOn") != [] or \
            (absent_vector.get("expected") or {}).get("budget") != expected_absent_budget or \
            (present_vector.get("input") or {}).get("budget") != {
                "unit": "work-units", "limit": 7} or \
            (present_vector.get("expected") or {}).get("dependsOn") != ["s0"] or \
            (present_vector.get("expected") or {}).get("budget") != {
                dimension: 7 for dimension in TS_BUDGET_DIMENSIONS}:
        findings.append("DL-TS-PROJECTION: absent/present budget projection vectors drifted")
    for unit in ("milliseconds", "bytes", "items"):
        vector = projection_vectors.get(f"reject-stage-budget-{unit}") or {}
        if vector.get("input") != {"unit": unit, "limit": 1} or \
                vector.get("expected") != {
                    "phase": "request-validation", "decision": "DENY",
                    "domainReasonCode": "FEATURE.TYPESCRIPT_STAGE_BUDGET_UNIT_NOT_IN_V1",
                    "providerSpawned": False}:
            findings.append(f"DL-TS-PROJECTION: {unit} budget rejection vector drifted")

    coverage_domain = wire.get("coverageDomain") or {}
    target_partition = coverage_domain.get("targetPartition") or {}
    cardinality = coverage_domain.get("cardinality") or {}
    overflow_fate = coverage_domain.get("overflowFate") or {}
    if coverage_domain.get("closed") is not True or \
            coverage_domain.get("relationResolutionById") != TS_RELATION_RESOLUTIONS or \
            coverage_domain.get("crossUniverseRelations") != TS_CROSS_UNIVERSE_RELATIONS or \
            target_partition.get("maxActivatedSemanticUniversesV1") != 2 or \
            not all(term in target_partition.get("crossUniverse", "") for term in
                    ("imports", "calls", "references", "every activated",
                     "including the TypeScript source universe")) or \
            "exactly one CoverageResultV1" not in cardinality.get("perFullKey", "") or \
            not all(term in cardinality.get("bounds", "") for term in
                    ("maxRelationsPerStage=64", "maxActivatedSemanticUniversesV1=2",
                     "128", "maxCoverageEntriesPerFrame=4096")):
        findings.append("DL-TS-COVERAGE: requested full-key Coverage domain/partition drifted")
    d9_error_codes = set((d9 or {}).get("codeVocabulary", {}).get("errorCodes", []))
    if overflow_fate.get("d9Class") != "operational-failed" or \
            overflow_fate.get("d9ErrorCode") != "SYSTEM.OUTCOME.ILLEGAL_STATE" or \
            overflow_fate.get("d9ErrorCode") not in d9_error_codes or \
            overflow_fate.get("providerSpawned") is not False or \
            overflow_fate.get("coverageFabricated") is not False or \
            not all(term in overflow_fate.get("arithmetic", "") for term in
                    ("checked uint64", "never wrap", "truncate", "spawn")) or \
            "greater than maxRequestedCoverageKeysPerStage" not in \
            overflow_fate.get("trigger", ""):
        findings.append("DL-TS-COVERAGE: requested-domain overflow fate is not deterministic")

    coverage_constants = coverage_domain.get("vectorConstants") or {}
    subjects = coverage_constants.get("manifestFileSubjects") or []
    subject_scope = coverage_constants.get("subjectScope") or {}
    expected_subject_commitment = cbor_commitment(
        "opensip.coverage.subject-scope.v1", subjects)
    if [subject.get("path") for subject in subjects if isinstance(subject, dict)] != \
            ["src/index.ts", "src/lib.rs"] or \
            subject_scope.get("subjectCount") != len(subjects) or \
            subject_scope.get("snapshotId") != coverage_constants.get("snapshotId") or \
            subject_scope.get("subjectScopeCommitment") != expected_subject_commitment:
        findings.append("DL-TS-COVERAGE: subject-scope commitment vector does not reproduce")
    coverage_vectors = {vector.get("id"): vector for vector in
                        coverage_domain.get("vectors", []) if isinstance(vector, dict)}
    required_coverage_vectors = {
        "intra-universe-success-domain",
        "cross-universe-unavailable-two-targets",
        "cross-universe-budget-exhausted-two-targets",
        "reject-missing-requested-key", "reject-duplicate-requested-key",
        "reject-unrequested-target-key", "reject-unordered-requested-domain",
        "reject-derived-key-count-overflow",
    }
    if set(coverage_vectors) != required_coverage_vectors:
        findings.append("DL-TS-COVERAGE: requested-domain vector set is not exact")
    source_universe = coverage_constants.get("sourceTypeScriptUniverseId")
    rust_universe = coverage_constants.get("targetRustUniverseId")
    for vector_id, relation, resolution, target_ids, deficiency in (
            ("intra-universe-success-domain", "types", "checked",
             [source_universe], None),
            ("cross-universe-unavailable-two-targets", "imports", "resolved-target",
             [source_universe, rust_universe], "provider-unavailable"),
            ("cross-universe-budget-exhausted-two-targets", "references",
             "resolved-binding", [source_universe, rust_universe], "budget-exhausted")):
        vector = coverage_vectors.get(vector_id) or {}
        domain = vector.get("requestedCoverageDomain") or {}
        keys = domain.get("keys") or []
        recomputed_domain = cbor_commitment(
            "opensip.ts-provider.requested-coverage-domain.v1",
            {"subjectScope": subject_scope, "keys": keys})
        if domain.get("expectedKeyCount") != len(target_ids) or len(keys) != len(target_ids) or \
                domain.get("domainCommitment") != recomputed_domain or \
                keys != sorted(keys, key=deterministic_cbor) or \
                [key.get("targetUniverseId") for key in keys if isinstance(key, dict)] != \
                target_ids or \
                any(key.get("relation") != relation or key.get("resolution") != resolution or
                    key.get("sourceUniverseId") != source_universe or
                    key.get("subjectScopeCommitment") != expected_subject_commitment or
                    key.get("producer") != "typescript-semantic" or
                    key.get("producerVersion") != coverage_constants.get("providerBuildId") or
                    key.get("schemaVersion") != 1 for key in keys if isinstance(key, dict)):
            findings.append(f"DL-TS-COVERAGE: {vector_id} key/domain commitment drifted")
        if deficiency is not None:
            results = vector.get("expectedCoverage") or []
            if len(results) != len(keys) or any(
                    result.get("entryOrdinal") != ordinal or
                    result.get("keyIndex") != ordinal or
                    result.get("coverageState") != "unknown" or
                    result.get("deficiency") != deficiency
                    for ordinal, result in enumerate(results) if isinstance(result, dict)):
                findings.append(f"DL-TS-COVERAGE: {vector_id} per-key terminal result drifted")
    for vector_id in ("reject-missing-requested-key", "reject-duplicate-requested-key",
                      "reject-unrequested-target-key"):
        if coverage_vectors.get(vector_id, {}).get("expected") != \
                "provider-protocol / PROVIDER.PROTOCOL_VIOLATION":
            findings.append(f"DL-TS-COVERAGE: {vector_id} no longer fails closed")
    for vector_id in ("reject-unordered-requested-domain",
                      "reject-derived-key-count-overflow"):
        if "SYSTEM.OUTCOME.ILLEGAL_STATE before provider spawn" not in \
                coverage_vectors.get(vector_id, {}).get("expected", ""):
            findings.append(f"DL-TS-COVERAGE: {vector_id} no longer has exact host fate")

    commitments = wire.get("commitments") or {}
    if set((commitments.get("domains") or {})) != {
            "snapshotManifest", "coverageSubjectScope", "requestedCoverageDomain",
            "factBatch", "stageFacts", "stageCoverage", "factStream",
            "coverageStream"} or \
            not all(x in commitments.get("domainRule", "") for x in
                    ("SHA-256", "UTF8(domain)", "deterministic-CBOR")) or \
            "Coverage is never empty" not in commitments.get("empty", ""):
        findings.append("DL-TS-WIRE: stream commitment domains/empty semantics drifted")

    snapshot = ts_protocol.get("snapshotTransport") or {}
    if not all(x in snapshot.get("rule", "") for x in
               ("sealed Snapshot", "VFS", "never passes a live worktree root")) or \
            not all(x in snapshot.get("manifest", "") for x in
                    ("SnapshotId", "sorted by canonical path", "content SHA-256")) or \
            not all(x in snapshot.get("content", "") for x in
                    ("monotonically increasing chunk index", "validates complete byte counts",
                     "TypeScript CompilerHost over that VFS")) or \
            not all(x in snapshot.get("packageResolution", "") for x in
                    ("snapshot/VFS entries", "outside that closure is forbidden",
                     "provider-unavailable")):
        findings.append("DL-TS: sealed Snapshot VFS/package-resolution closure is incomplete")
    if "protocol-only" not in ts_protocol.get("stdout", "") or \
            "protocol violations" not in ts_protocol.get("stdout", ""):
        findings.append("DL-TS: stdout is not reserved exclusively for protocol")
    stderr = ts_protocol.get("stderr", "")
    if not all(x in stderr for x in ("non-authoritative", "256 KiB", "never carries facts",
                                     "never changes a result")) or \
            limits.get("maxStderrBytes") != 262144:
        findings.append("DL-TS: stderr may become unbounded or authoritative")

    supervision = ts.get("supervision") or {}
    atomicity = supervision.get("factBatchAtomicity") or {}
    if atomicity.get("authorityBeforeTerminal") != "CANDIDATE_ONLY" or \
            atomicity.get("admitOn") != \
            "valid Complete + matching stream commitments + exit status zero + EOF" or \
            atomicity.get("scope") != "entire Analyze across every requested stage" or \
            any(atomicity.get(k) != "DISCARD_ALL_CANDIDATES" for k in
                ("onUnavailable", "onBudgetExhausted", "onCancelled",
                 "onProtocolOrProcessFault")) or \
            set(atomicity.get("hostValidation", [])) != {
                "frame schema", "stage attribution", "batch order", "relation/rung",
                "typed anchors",
                "FACT-PLANE factRecordContractV1 admission + FACT-ID-V1 host minting",
                "Coverage key",
                "stream counts", "stream commitments"}:
        findings.append("DL-TS: candidate fact transaction/host validation authority drifted")
    unavailable = supervision.get("cleanUnavailable") or {}
    if unavailable != {
            "terminalFrame": "Unavailable", "allowedImmediatelyAfter": "Analyze",
            "factBatchCount": 0, "coverageFrameCount": 0,
            "candidateDisposition": "DISCARD_ALL_CANDIDATES",
            "coveragePayload": "Unavailable.coverage contains exactly one unavailable CoverageResultV1 for every full key in every requested stage's requestedCoverageDomain.keys, in stage-major/key order",
            "deficiency": "provider-unavailable",
            "d9ReasonCode": "COVERAGE.PROVIDER_UNAVAILABLE",
            "hostOutcome": "coherent Coverage-bearing Run; requiredness determines verdict, never operational-failed solely for clean Unavailable"}:
        findings.append("DL-TS: clean Unavailable ordering/Coverage/D9 fate drifted")
    deterministic_budget = supervision.get("deterministicBudget") or {}
    if deterministic_budget.get("terminalFrame") != "BudgetExhausted" or \
            deterministic_budget.get("source") != "Analyze.stageRequests[*].budget" or \
            deterministic_budget.get("dimensions") != TS_BUDGET_DIMENSIONS or \
            "provider wall clock is never read" not in deterministic_budget.get("counterRule", "") or \
            "provider-protocol" not in deterministic_budget.get("wallClock", "") or \
            deterministic_budget.get("candidateDisposition") != "DISCARD_ALL_CANDIDATES" or \
            deterministic_budget.get("deficiency") != "budget-exhausted" or \
            deterministic_budget.get("d9ReasonCode") != "COVERAGE.BUDGET_EXHAUSTED" or \
            "every full key in every requested stage's requestedCoverageDomain.keys" not in \
            deterministic_budget.get("coveragePayload", ""):
        findings.append("DL-TS: deterministic work-unit BudgetExhausted semantics drifted")
    if not all(x in supervision.get("userCancellation", "") for x in
               ("send Cancel once", "bounded cleanup grace", "interrupted/130",
                "does not overwrite")) or \
            not all(x in supervision.get("protocolOrCrash", "") for x in
                    ("non-zero exit", "EOF before", "hang", "provider-protocol",
                     "PROVIDER.PROTOCOL_VIOLATION")) or \
            not all(x in supervision.get("deliveryFailure", "") for x in
                    ("digest-mismatched", "delivery-required", "DELIVERY.REQUIRED_FAILED")) or \
            not all(x in supervision.get("success", "") for x in
                    ("valid Complete", "exit status zero", "Extra output", "provider-protocol")):
        findings.append("DL-TS: cancellation/crash/delivery/success process fate is ambiguous")

    authority = ts.get("authority") or {}
    if not all(x in authority.get("durable", "") for x in
               ("cannot allocate PlanId", "ledger/CAS", "commit facts", "seal a Run",
                "derive policy", "Only the Rust host")) or \
            "never given a live repository root" not in authority.get("source", ""):
        findings.append("DL-TS: worker can acquire host source/durable/policy authority")
    environment = authority.get("environment") or {}
    if environment.get("inheritParent") is not False or \
            environment.get("setExactly") != {"LC_ALL": "C", "LANG": "C", "TZ": "UTC"} or \
            not {"HOME", "USERPROFILE", "PATH", "NODE_PATH", "NODE_OPTIONS",
                 "NPM_CONFIG_USERCONFIG", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                 "NO_PROXY", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "GITHUB_TOKEN"} \
            <= set(environment.get("unsetAtMinimum", [])) or \
            environment.get("secretInheritance") is not False or \
            "FORBIDDEN" not in environment.get("extraVariables", ""):
        findings.append("DL-TS: child environment allowlist/secret stripping drifted")
    network = authority.get("network") or {}
    if network.get("v1Grant") != "DENIED" or network.get("fetchPackages") is not False or \
            network.get("dnsOrSocketInputMayAffectFacts") is not False or \
            network.get("missingResolutionInput") != "provider-unavailable Coverage" or \
            not all(x in network.get("enforcementClaim", "") for x in
                    ("provider logic", "TCB", "not a sandbox claim")):
        findings.append("DL-TS: v1 provider network denial/offline honesty drifted")
    if not all(x in authority.get("repositoryExecution", "") for x in
               ("disabled", "no tsserver plugins", "custom transformers", "native addons")):
        findings.append("DL-TS: repository JavaScript/native execution is not disabled")
    posture = ts.get("tcbPosture", "")
    if not all(x in posture for x in ("release-pinned TCB", "not a security sandbox",
                                      "do not authorize a sandbox claim")):
        findings.append("DL-TS: process boundary overclaims sandbox confinement")

    # DL-SCOPE — C-2 is general; DELIVERY owns a total v1 allow/deny overlay.
    product_scope = c.get("initialProductScope") or {}
    overlay = product_scope.get("externalScannerOverlay") or {}
    total_overlay = product_scope.get("v1PlanIntentOverlay") or {}
    domain_vocab = product_scope.get("domainReasonVocabulary") or {}
    if domain_vocab.get("closed") is not True or \
            set(domain_vocab.get("values", [])) != V1_SCOPE_REASONS or \
            "not D9 HostTermination codes" not in domain_vocab.get("owner", ""):
        findings.append("DL-SCOPE: DELIVERY typed domain-reason vocabulary is not closed or is confused with D9")
    c2 = load(C2)
    if not c2:
        findings.append(f"DL-SCOPE: could not load {C2}")
    else:
        intent_contract = c2.get("planIntent") or {}
        intent_schema = intent_contract.get("schema") or {}
        admission_schema = intent_contract.get("admissionDescriptorV1") or {}
        contribution_authorities = set((admission_schema.get("contribution") or {}).get(
            "authority", []))
        fact_operators = set((((c2.get("stageSchemas") or {}).get("kinds") or {}).get(
            "fact-derivation") or {}).get("operatorAuthority", []))
        if "external-scanner" not in contribution_authorities or \
                "external-scanner" not in fact_operators:
            findings.append("DL-SCOPE: live C-2 does not recognize external-scanner on both intent surfaces")
        tagged = intent_schema.get("taggedUnion") or {}
        if intent_schema.get("closed") is not True or \
                set(intent_schema.get("intentKind", [])) != {"analysis", "stored-view"} or \
                (tagged.get("analysis") or {}).get("payload") != "AnalysisIntentV1" or \
                (tagged.get("stored-view") or {}).get("payload") != "StoredViewIntentV1":
            findings.append("DL-SCOPE: live C-2 PlanIntent is not the expected closed tagged union")
        commitment = intent_contract.get("canonicalCommitment") or {}
        if commitment.get("field") != "planIntentCommitment" or \
                commitment.get("domainTagUtf8") != "opensip.plan-intent.v1" or \
                commitment.get("digest") != "SHA-256" or \
                "opensip-canonical-json-v1" not in commitment.get("preimage", ""):
            findings.append("DL-SCOPE: live C-2 PlanIntent commitment differs from DELIVERY overlay input")
        lifecycle = intent_contract.get("lifecycle") or {}
        if "request-validation" not in lifecycle.get("createdAt", "") or \
                not all(x in lifecycle.get("onInvalidOrExcluded", "") for x in
                        ("No ExecutionId", "AttemptRecord", "PlanId", "Run")):
            findings.append("DL-SCOPE: live C-2 rejection boundary can allocate attempt/Run identity")

        live_axes = _c2_scope_enum_sets(c2)
        axes = total_overlay.get("axes") or {}
        expected_axis_order = [
            "intentKind", "executionTopology", "workflowIntent", "networkIntent",
            "remoteComputation", "repositoryBuildScripts",
            "repositoryProceduralMacros", "repositoryCompilerPlugins",
            "repositoryProjectHooks", "contributionOrigin", "contributionAuthority",
            "stageKind", "factDerivationOperator", "typescriptStageBudgetUnit",
            "capability",
        ]
        if total_overlay.get("schemaVersion") != 1 or \
                total_overlay.get("closed") is not True or \
                total_overlay.get("axisOrder") != expected_axis_order or \
                total_overlay.get("decisionVocabulary") != ["ALLOW", "ALLOW_IF", "DENY"] or \
                set(axes) != set(V1_SCOPE_AXIS_SPECS):
            findings.append("DL-SCOPE-TOTAL: v1 overlay axes/order/decision vocabulary is not closed")
        repo_required = set(((intent_contract.get("analysisIntentV1") or {}).get(
            "repositoryExecution") or {}).get("required", []))
        if repo_required != {"buildScripts", "proceduralMacros", "compilerPlugins",
                             "projectHooks"}:
            findings.append("DL-SCOPE-TOTAL: future C-2 repository-execution field is unclassified")
        for axis_name, (path, source, expected_values) in V1_SCOPE_AXIS_SPECS.items():
            axis = axes.get(axis_name) or {}
            dispositions = axis.get("dispositions") or {}
            if axis.get("path") != path or axis.get("c2Source") != source:
                findings.append(f"DL-SCOPE-TOTAL: {axis_name} path/source binding drifted")
            if set(dispositions) != live_axes.get(axis_name, set()):
                findings.append(f"DL-SCOPE-TOTAL: {axis_name} leaves a live C-2 value unclassified")
            for value, (decision, detail) in expected_values.items():
                expected = {"decision": decision}
                if decision == "DENY":
                    expected["domainReasonCode"] = detail
                elif decision == "ALLOW_IF":
                    expected["conditionId"] = detail
                if dispositions.get(value) != expected:
                    findings.append(f"DL-SCOPE-TOTAL: {axis_name}={value} disposition drifted")
        expected_condition_reasons = {
            "allowed-fact-stage-grant": "FEATURE.CAPABILITY_GRANT_NOT_IN_V1",
            "bundled-host-builtin": "FEATURE.UNBUNDLED_HOST_BUILTIN_NOT_IN_V1",
            "bundled-provider-process-grant": "FEATURE.CAPABILITY_GRANT_NOT_IN_V1",
            "bundled-semantic-provider": "FEATURE.SEMANTIC_PROVIDER_NOT_IN_V1",
            "bundled-semantic-provider-stage": "FEATURE.SEMANTIC_PROVIDER_NOT_IN_V1",
            "rust-repository-execution": "FEATURE.REPOSITORY_EXECUTION_GRANT_REQUIRED",
        }
        conditions = total_overlay.get("conditions") or {}
        if set(conditions) != set(expected_condition_reasons):
            findings.append("DL-SCOPE-TOTAL: ALLOW_IF condition set is not closed")
        for condition_id, reason in expected_condition_reasons.items():
            condition = conditions.get(condition_id) or {}
            if condition.get("closed") is not True or \
                    condition.get("onFalse") != {"decision": "DENY",
                                                  "domainReasonCode": reason}:
                findings.append(f"DL-SCOPE-TOTAL: {condition_id} has no exact fail-closed fate")
        if (conditions.get("bundled-semantic-provider") or {}).get(
                "allowedContributionIds") != ["rust-semantic", "typescript-semantic"] or \
                (conditions.get("bundled-semantic-provider-stage") or {}).get(
                    "allowedProviderIds") != ["rust-semantic", "typescript-semantic"] or \
                (conditions.get("rust-repository-execution") or {}).get(
                    "parameterFields") != ["build-scripts", "network", "procedural-macros"]:
            findings.append("DL-SCOPE-TOTAL: provider/repository conditional allowlist drifted")

    overlay_bytes = json.dumps(total_overlay, sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False).encode("utf-8")
    overlay_digest = hashlib.sha256(
        b"opensip.delivery.v1-plan-intent-overlay.v1\0" + overlay_bytes).hexdigest()
    expected_overlay_commitment = {
        "algorithm": "SHA-256",
        "canonicalization": "UTF-8 JSON with object keys sorted, no insignificant whitespace, Unicode emitted directly; the v1PlanIntentOverlay object only",
        "domain": "opensip.delivery.v1-plan-intent-overlay.v1\u0000",
        "sha256": V1_OVERLAY_SCHEMA_SHA256,
    }
    if product_scope.get("v1PlanIntentOverlayCommitment") != expected_overlay_commitment or \
            overlay_digest != V1_OVERLAY_SCHEMA_SHA256:
        findings.append("DL-SCOPE-TOTAL: committed v1 overlay/fixtures drifted")
    excluded_product = set(product_scope.get("excludedByV1ProductOverlay", []))
    if "external-scanner fact-derivation operators, including otherwise C-2-schema-valid trusted scanners" \
            not in excluded_product:
        findings.append("DL-SCOPE: external scanner is not explicitly excluded by the v1 overlay")
    selector = overlay.get("selector") or {}
    expected_selector = {
        "stageIntentPath": "PlanIntent.analysis.admissionDescriptor.workflow.stages[*]",
        "stageKindField": "kind",
        "stageKindValue": "fact-derivation",
        "operatorField": "operator",
        "operatorValue": "external-scanner",
        "providerIdRule": "providerId is required on the matching stage intent",
        "contributionPath": "PlanIntent.analysis.admissionDescriptor.contributions[*]",
        "contributionAuthorityField": "authority",
        "contributionAuthorityValue": "external-scanner",
        "consistencyRule": "A stage intent and its referenced contribution must agree; either external-scanner surface is sufficient to reject and disagreement is invalid PlanIntent.",
    }
    if selector != expected_selector:
        findings.append("DL-SCOPE: PlanIntent stage/contribution external-scanner selector is not exact")
    input_rep = overlay.get("inputRepresentation", "")
    if not all(x in input_rep for x in ("frozen pre-admission PlanIntent",
                                        "planIntentCommitment", "SHA-256",
                                        "canonical JSON v1", "opensip.plan-intent.v1",
                                        "never a later ExecutionPlan")):
        findings.append("DL-SCOPE: rejection is not bound to the frozen PlanIntent commitment")
    if overlay.get("decision") != "reject" or \
            "request-validation" not in overlay.get("decisionPoint", "") or \
            "before attempt-admission" not in overlay.get("decisionPoint", ""):
        findings.append("DL-SCOPE: external scanner is not rejected before attempt admission")
    if overlay.get("domainReasonCode") != "FEATURE.EXTERNAL_SCANNER_NOT_IN_V1":
        findings.append("DL-SCOPE: external-scanner domain reason is not exact")
    identity_outcome = overlay.get("identityOutcome") or {}
    expected_request_outcome = {
        "contract": "REQUEST-ID-V1",
        "state": "PRESENT",
        "allocation": "ALLOCATED_AND_RESERVED_AT_FIRST_TRUSTED_INGRESS_BEFORE_PARSING",
        "owner": "orchestration host request-ingress adapter",
        "representation": "^req1_[0-9a-f]{32}$",
        "semanticParticipation": "NONE",
    }
    if identity_outcome.get("requestId") != expected_request_outcome:
        findings.append("DL-SCOPE: rejected scanner does not have mandatory ingress REQUEST-ID-V1")
    for key in ("executionId", "attemptRecord", "snapshotId", "planId", "runId", "run"):
        if identity_outcome.get(key) != "ABSENT":
            findings.append(f"DL-SCOPE: rejected scanner allocated {key}")
    if set(identity_outcome) != {"requestId", "executionId", "attemptRecord", "snapshotId",
                                "planId", "runId", "run"}:
        findings.append("DL-SCOPE: scanner rejection identity outcome is not closed")
    request_contract = (op or {}).get("requestIdContract") or {}
    request_authority = request_contract.get("authority") or {}
    request_allocation = request_contract.get("allocation") or {}
    request_representation = request_contract.get("representation") or {}
    if request_contract.get("id") != "REQUEST-ID-V1" or \
            request_contract.get("status") != "IMPLEMENTABLE" or \
            request_authority.get("allocationOwner") != expected_request_outcome["owner"] or \
            request_representation.get("regex") != expected_request_outcome["representation"] or \
            not all(x in request_allocation.get("point", "") for x in
                    ("first trusted host ingress", "before request parsing",
                     "request validation", "ExecutionId allocation")) or \
            not all(x in request_allocation.get("analysisAttemptRule", "") for x in
                    ("Rejected requests have RequestId", "no ExecutionId", "AttemptRecord",
                     "RunId", "Run")):
        findings.append("DL-SCOPE: scanner identity fate disagrees with live OPERABILITY REQUEST-ID-V1")

    admission_rule = product_scope.get("admissionRule") or {}
    expected_admission_rule = {
        "closed": True,
        "requestId": {"contract": "REQUEST-ID-V1", "stateBeforeParsing": "PRESENT_AND_RESERVED",
                      "owner": "orchestration host request-ingress adapter"},
        "evaluationPoint": "request-validation after C-2 schema validation/profile expansion/PlanIntent freeze and before attempt-admission",
        "excludedAuthorityForm": {"decision": "reject",
                                  "domainReasonCode": "FEATURE.REQUIRES_CAPABILITY_RUNTIME",
                                  "d9RejectionCause": "extension-admission-rejected",
                                  "d9ErrorCode": "EXTENSION.ADMISSION_REJECTED"},
        "externalScanner": {"decision": "reject", "selector": "externalScannerOverlay.selector",
                            "domainReasonCode": "FEATURE.EXTERNAL_SCANNER_NOT_IN_V1",
                            "d9RejectionCause": "extension-admission-rejected",
                            "d9ErrorCode": "EXTENSION.ADMISSION_REJECTED"},
        "totalV1Overlay": {"decision": "evaluate-all-axes",
                           "selector": "v1PlanIntentOverlay",
                           "onDeny": "v1PlanIntentOverlay.rejectionProjection"},
        "rejectedIdentityOutcome": {"requestId": "PRESENT", "executionId": "ABSENT",
                                    "attemptRecord": "ABSENT", "snapshotId": "ABSENT",
                                    "planId": "ABSENT", "runId": "ABSENT", "run": "ABSENT"},
        "externalScannerAdmissionAfterCheck": False,
        "stubOrDeferredAdmission": False,
    }
    if admission_rule != expected_admission_rule:
        findings.append("DL-SCOPE: aggregate admission rule contradicts or weakens the scanner overlay")
    if not all(x in overlay.get("nonEquivalence", "") for x in
               ("v1 product-scope overlay", "not an ARCH.PROBE-CONTRACT", "C-2 continues")):
        findings.append("DL-SCOPE: product exclusion is conflated with capability-runtime ontology")
    projection = total_overlay.get("rejectionProjection") or {}
    expected_projection = {
        "decision": "reject", "lifecycle": "pre-run request-validation",
        "d9RejectionCause": "extension-admission-rejected",
        "d9ErrorCode": "EXTENSION.ADMISSION_REJECTED",
        "reasonRule": "Every DENY or failed ALLOW_IF returns its exact domainReasonCode as typed detail; it never becomes a D9 code.",
        "identityOutcome": {"requestId": "PRESENT", "executionId": "ABSENT",
                            "attemptRecord": "ABSENT", "snapshotId": "ABSENT",
                            "planId": "ABSENT", "runId": "ABSENT", "run": "ABSENT"},
    }
    if projection != expected_projection:
        findings.append("DL-SCOPE-TOTAL: rejection projection/zero-attempt identity fate drifted")
    fixture_model = total_overlay.get("fixtureModel") or {}
    base_intent = fixture_model.get("baseAllowedAnalysisIntent") or {}
    live_base = next((x for x in (c2 or {}).get("planIntentFixtures", [])
                      if x.get("id") == "valid-minimal-analysis-intent"), {})
    if fixture_model.get("baseC2FixtureId") != "valid-minimal-analysis-intent" or \
            fixture_model.get("baseC2Commitment") != \
            "sha256:dca3a310674308c9bb951c5716ee871d19df42f4df07b406533a199d99a8c36d" or \
            live_base.get("intent") != base_intent or \
            live_base.get("expectedCommitment") != fixture_model.get("baseC2Commitment"):
        findings.append("DL-SCOPE-TOTAL: allowed base fixture drifted from live C-2 vector")
    if c2:
        for error in c2_intent_fixture_errors(base_intent, c2, fp):
            findings.append(f"DL-SCOPE-TOTAL: base fixture is not C-2 valid — {error}")
    common_reject = fixture_model.get("commonRejectOutcome") or {}
    expected_common_reject = {
        "admission": "rejected", "lifecycle": "pre-run",
        "requestIdAllocatedBefore": "parse",
        "d9RejectionCause": "extension-admission-rejected",
        "d9ErrorCode": "EXTENSION.ADMISSION_REJECTED",
        "executionIdAllocated": False, "attemptRecordCreated": False,
        "snapshotIdAllocated": False, "planIdAllocated": False,
        "runIdAllocated": False, "runCreated": False,
    }
    if common_reject != expected_common_reject:
        findings.append("DL-SCOPE-TOTAL: fixture rejection outcome is not exact zero-attempt D9")
    cases = fixture_model.get("cases", [])
    cases_by_id = {case.get("id"): case for case in cases if isinstance(case, dict)}
    required_reject_ids = {
        "reject-resident-single-project", "reject-resident-multi-project",
        "reject-repair-workflow", "reject-mutation-workflow", "reject-network-granted",
        "reject-cloud-service", "reject-model-service",
        "reject-build-script-without-rust-grant",
        "reject-procedural-macro-without-rust-grant", "reject-compiler-plugin",
        "reject-project-hook", "reject-probe-stage", "reject-imperative-rule",
        "reject-native-contribution", "reject-wasm-contribution",
        "reject-external-scanner", "reject-third-party-semantic-provider",
        "reject-unbundled-host-builtin", "reject-unattached-process-grant",
        "reject-typescript-milliseconds-stage-budget",
        "reject-typescript-bytes-stage-budget",
        "reject-typescript-items-stage-budget",
    }
    required_allow_ids = {"allow-bundled-typescript-provider",
                          "allow-typescript-work-unit-stage-budget",
                          "allow-rust-repository-execution"}
    if len(cases_by_id) != len(cases) or set(cases_by_id) != \
            required_reject_ids | required_allow_ids:
        findings.append("DL-SCOPE-TOTAL: zero-attempt/positive fixture set is not closed")
    for case_id, case in cases_by_id.items():
        try:
            fixture_intent = _pointer_mutate(base_intent, case.get("mutations", []))
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            findings.append(f"DL-SCOPE-TOTAL {case_id}: fixture mutation failed — {exc}")
            continue
        if c2:
            for error in c2_intent_fixture_errors(fixture_intent, c2, fp):
                findings.append(f"DL-SCOPE-TOTAL {case_id}: mutated intent is not C-2 valid — {error}")
        actual_decision, actual_reason = v1_overlay_outcome(fixture_intent)
        expect = case.get("expect") or {}
        if case_id in required_reject_ids:
            if expect != {"decision": "DENY", "domainReasonCode": actual_reason,
                          "outcome": "commonRejectOutcome"} and not (
                    case_id == "reject-external-scanner" and
                    expect == {"decision": "DENY", "domainReasonCode": actual_reason,
                               "outcome": "commonRejectOutcome",
                               "requestId": "req1_00000000000000000000000000000021"}):
                findings.append(f"DL-SCOPE-TOTAL {case_id}: rejection expectation is not exact")
            if actual_decision != "DENY" or actual_reason not in V1_SCOPE_REASONS:
                findings.append(f"DL-SCOPE-TOTAL {case_id}: excluded class was not denied")
        elif expect != {"decision": "ALLOW"} or actual_decision != "ALLOW" or \
                actual_reason is not None:
            findings.append(f"DL-SCOPE-TOTAL {case_id}: positive control was over-rejected")
    fixture_ids = overlay.get("fixtureIds") or {}
    if fixture_ids != {"reject": "reject-external-scanner",
                       "allowBundledProvider": "allow-bundled-typescript-provider"} or \
            not REQUEST_ID_RE.fullmatch((cases_by_id.get("reject-external-scanner", {})
                                         .get("expect") or {}).get("requestId", "")):
        findings.append("DL-SCOPE: external-scanner fixture references/RequestId drifted")

    # DL-D9 — DELIVERY may name domain reasons but D9 owns host termination.
    if not d9:
        findings.append(f"DL-D9: could not load {D9}")
    else:
        integration = c.get("terminationIntegration") or {}
        error_codes = set((d9.get("codeVocabulary") or {}).get("errorCodes", []))
        reason_codes = set((d9.get("codeVocabulary") or {}).get("reasonCodes", []))
        maps = d9.get("codeMaps") or {}
        deficiency_map = maps.get("deficiencyToReasonCode") or {}
        fault_map = maps.get("faultCauseToErrorCode") or {}
        rejection_map = maps.get("rejectionCauseToErrorCode") or {}

        scope_projection = ((c.get("initialProductScope") or {}).get(
            "v1PlanIntentOverlay") or {}).get("rejectionProjection") or {}
        scope_cause = scope_projection.get("d9RejectionCause")
        scope_code = scope_projection.get("d9ErrorCode")
        matrix_reasons = set()
        scope_overlay = ((c.get("initialProductScope") or {}).get(
            "v1PlanIntentOverlay") or {})
        for axis in (scope_overlay.get("axes") or {}).values():
            for disposition in (axis.get("dispositions") or {}).values():
                if disposition.get("decision") == "DENY":
                    matrix_reasons.add(disposition.get("domainReasonCode"))
        for condition in (scope_overlay.get("conditions") or {}).values():
            matrix_reasons.add((condition.get("onFalse") or {}).get("domainReasonCode"))
        if matrix_reasons != V1_SCOPE_REASONS or scope_code not in error_codes or \
                rejection_map.get(scope_cause) != scope_code:
            findings.append("DL-D9: total v1 overlay reasons do not share the live pre-run rejection projection")

        provider = integration.get("providerProtocolFault") or {}
        provider_cause = provider.get("d9FaultCause")
        provider_code = provider.get("d9ErrorCode")
        if provider_code not in error_codes or fault_map.get(provider_cause) != provider_code:
            findings.append("DL-D9: provider protocol condition does not map through live D9")
        frame_rule = (rust.get("providerProtocol") or {}).get("frameIntegrity", "")
        if provider_code not in frame_rule or "PROVIDER.PROTOCOL_FAULT" in frame_rule:
            findings.append("DL-D9: provider frame rule uses a non-canonical termination code")

        excluded_map = integration.get("excludedCapabilityForm") or {}
        domain_reason = excluded_map.get("domainReasonCode")
        rejection_cause = excluded_map.get("d9RejectionCause")
        rejection_code = excluded_map.get("d9ErrorCode")
        if domain_reason != "FEATURE.REQUIRES_CAPABILITY_RUNTIME":
            findings.append("DL-D9: excluded capability form lacks the required domain reason")
        if rejection_code not in error_codes or rejection_map.get(rejection_cause) != rejection_code:
            findings.append("DL-D9: excluded capability form does not map through live D9")
        admission_rule = c.get("initialProductScope", {}).get("admissionRule") or {}
        authority_rule = admission_rule.get("excludedAuthorityForm") or {}
        if authority_rule != {"decision": "reject", "domainReasonCode": domain_reason,
                              "d9RejectionCause": rejection_cause,
                              "d9ErrorCode": rejection_code}:
            findings.append("DL-D9: initial-product admission rule omits its domain-to-D9 join")
        projection = excluded_map.get("projectionRule", "")
        if "typed explanatory detail" not in projection or "sole public" not in projection:
            findings.append("DL-D9: domain reason and public termination code ownership are ambiguous")

        scanner_map = integration.get("excludedExternalScanner") or {}
        scanner_reason = scanner_map.get("domainReasonCode")
        scanner_cause = scanner_map.get("d9RejectionCause")
        scanner_code = scanner_map.get("d9ErrorCode")
        if scanner_reason != "FEATURE.EXTERNAL_SCANNER_NOT_IN_V1":
            findings.append("DL-D9: external-scanner scope overlay lacks its exact domain reason")
        if scanner_code not in error_codes or rejection_map.get(scanner_cause) != scanner_code:
            findings.append("DL-D9: external-scanner exclusion does not reuse live D9 rejection mapping")
        scanner_rule = admission_rule.get("externalScanner") or {}
        if scanner_rule.get("decision") != "reject" or \
                scanner_rule.get("domainReasonCode") != scanner_reason or \
                scanner_rule.get("d9RejectionCause") != scanner_cause or \
                scanner_rule.get("d9ErrorCode") != scanner_code:
            findings.append("DL-D9: aggregate scanner admission rule contradicts its live D9 join")
        if not all(x in scanner_map.get("projectionRule", "") for x in
                   ("not a new D9 code", "sole public")):
            findings.append("DL-D9: scanner domain detail could become a second public vocabulary")

        availability = integration.get("providerAvailability") or {}
        availability_deficiency = availability.get("d9Deficiency")
        availability_code = availability.get("d9ReasonCode")
        if availability_code not in reason_codes or \
                deficiency_map.get(availability_deficiency) != availability_code:
            findings.append("DL-D9: provider availability does not map through live Coverage reason code")
        budget = integration.get("providerBudget") or {}
        budget_deficiency = budget.get("d9Deficiency")
        budget_code = budget.get("d9ReasonCode")
        if budget_code not in reason_codes or deficiency_map.get(budget_deficiency) != budget_code:
            findings.append("DL-D9: provider budget does not map through live Coverage reason code")
        delivery_fault = integration.get("providerDeliveryFailure") or {}
        delivery_cause = delivery_fault.get("d9FaultCause")
        delivery_code = delivery_fault.get("d9ErrorCode")
        if delivery_code not in error_codes or fault_map.get(delivery_cause) != delivery_code:
            findings.append("DL-D9: missing/corrupt bundled provider does not map through live D9")
        interruption = integration.get("providerInterruption") or {}
        if interruption.get("d9Class") != "interrupted" or \
                interruption.get("d9ExitCode") != d9.get("classToExitCode", {}).get("interrupted") or \
                "not relabelled" not in interruption.get("projectionRule", ""):
            findings.append("DL-D9: provider cancellation conflicts with D9 interruption precedence")

    # DL-PROF — actual typed objects, exact provider membership and live relations.
    profiles = c.get("installProfiles", {})
    by_name = {p.get("profile"): p for p in profiles.get("profiles", [])}
    if set(by_name) != set(PROFILE_PROVIDERS):
        findings.append("DL-PROF: profile set is not closed")
    if profiles.get("defaultProfile") != "full":
        findings.append("DL-PROF: supported-platform default is not the P-4 full profile")
    relation_ladders = fp.get("relationRegistry", {}).get("relations", {}) if fp else {}
    deficiency_values = set(fp.get("deficiencyVocabulary", {}).get("values", [])) if fp else set()
    if not fp:
        findings.append(f"DL-PROF: could not load {FP}")
    for name, expected_providers in PROFILE_PROVIDERS.items():
        profile = by_name.get(name, {})
        if set(profile.get("semanticProviders", [])) != expected_providers:
            findings.append(f"DL-PROF {name}: semantic provider set is not exact")
        manifest = profile.get("capabilityManifest")
        if not isinstance(manifest, dict):
            findings.append(f"DL-PROF {name}: capability manifest is prose, not a typed object")
            continue
        if manifest.get("profile") != name or manifest.get("schemaVersion") != 1:
            findings.append(f"DL-PROF {name}: manifest identity/schema mismatch")
        provider_ids = {p.get("providerId") for p in manifest.get("providers", [])}
        for language in expected_providers:
            if f"{language}-semantic" not in provider_ids:
                findings.append(f"DL-PROF {name}: missing {language} semantic capability")
        absent_languages = {a.get("language") for a in manifest.get("coverageForAbsent", [])}
        if absent_languages != ({"typescript", "rust"} - expected_providers):
            findings.append(f"DL-PROF {name}: absent-provider Coverage set is not exact")
        for provider in manifest.get("providers", []):
            if not provider.get("providerVersionSource") or not provider.get("toolchainIdentitySource"):
                findings.append(f"DL-PROF {name}: provider identity source omitted")
            if provider.get("platformIds") != ["all-supported"]:
                findings.append(f"DL-PROF {name}: provider platform availability is ambiguous")
            for relation, rung in provider.get("relations", {}).items():
                ladder = relation_ladders.get(relation, {}).get("ladder", [])
                if rung not in ladder:
                    findings.append(f"DL-PROF {name}: {relation}={rung} is outside fact-plane")
        for absent in manifest.get("coverageForAbsent", []):
            if absent.get("coverageState") != "unavailable" or \
                    absent.get("deficiency") not in deficiency_values:
                findings.append(f"DL-PROF {name}: absent capability has invalid Coverage")
            for relation in absent.get("relationIds", []):
                if relation not in relation_ladders:
                    findings.append(f"DL-PROF {name}: absent relation {relation} is unknown")

    # DL-SUPPLY — the schema itself is load-bearing.
    rms = c.get("releaseManifestSchema", {})
    release = rms.get("ReleaseManifestV1", {})
    if set(release.get("required", [])) != RELEASE_REQUIRED or not release.get("closed"):
        findings.append("DL-SUPPLY: ReleaseManifestV1 required/closed shape is not exact")
    artifact = rms.get("ArtifactEntry", {})
    if set(artifact.get("required", [])) != ARTIFACT_REQUIRED:
        findings.append("DL-SUPPLY: ArtifactEntry cannot identify exact bytes/platform/dependencies")
    canon = rms.get("canonicalization", {})
    if "RFC 8785" not in canon.get("algorithm", "") or \
            "manifestId and signatures omitted" not in canon.get("signedBytes", "") or \
            "sha256" not in canon.get("manifestId", ""):
        findings.append("DL-SUPPLY: canonical signed bytes or manifest identity are ambiguous")
    schema_required = {
        "KeyDescriptor": KEY_REQUIRED,
        "Signature": SIGNATURE_REQUIRED,
        "Role": ROLE_REQUIRED,
        "RootMetadataV1": ROOT_REQUIRED,
        "RevocationSnapshotV1": REVOCATION_REQUIRED,
        "VerificationPolicy": POLICY_REQUIRED,
        "OfflineReleaseBundleV1": BUNDLE_REQUIRED,
    }
    for schema_name, required in schema_required.items():
        schema = rms.get(schema_name, {})
        if set(schema.get("required", [])) != required or not schema.get("closed"):
            findings.append(f"DL-SUPPLY: {schema_name} required/closed shape is not exact")
    if rms.get("KeyDescriptor", {}).get("algorithm") != "Ed25519" or \
            "keyId" not in rms.get("Signature", {}).get("required", []):
        findings.append("DL-SUPPLY: key/signature algorithm or key identity is ambiguous")
    root_roles = rms.get("RootMetadataV1", {}).get("requiredRoles", {})
    if root_roles != {
            "root": {"keyCount": 3, "threshold": 2},
            "release": {"keyCount": 3, "threshold": 2},
            "delegated-artifact": {"keyCount": 2, "threshold": 1}}:
        findings.append("DL-SUPPLY: root/release/delegated role membership is not exact")
    if "present empty arrays" not in rms.get("RevocationSnapshotV1", {}).get("emptyState", ""):
        findings.append("DL-SUPPLY: canonical empty revocation state is unspecified")
    if "exactly true" not in rms.get("VerificationPolicy", {}).get("rule", ""):
        findings.append("DL-SUPPLY: offline bundle is not conditionally required by policy")
    trust = rms.get("Trust", {})
    if trust.get("signatureAlgorithm") != "Ed25519 (RFC 8032)" or \
            trust.get("artifactDigest") != "SHA-256":
        findings.append("DL-SUPPLY: signature/digest algorithms are not exact")
    if trust.get("rootRole") != {"roleId": "root", "keyCount": 3, "threshold": 2} or \
            trust.get("releaseRole") != {"roleId": "release", "keyCount": 3, "threshold": 2} or \
            trust.get("delegatedArtifactRole") != {
                "roleId": "delegated-artifact", "keyCount": 2, "threshold": 1}:
        findings.append("DL-SUPPLY: root/release threshold semantics are not exact")
    if "both" not in trust.get("rootRotation", "") or not trust.get("revocation"):
        findings.append("DL-SUPPLY: root rotation/revocation is incomplete")
    if "pins the initial root" not in trust.get("bootstrap", "") or \
            "No trust-on-first-use" not in trust.get("bootstrap", ""):
        findings.append("DL-SUPPLY: initial root trust bootstrap is ambiguous or TOFU")
    vb_required = set(rms.get("OfflineReleaseBundleV1", {}).get("required", []))
    if vb_required != BUNDLE_REQUIRED:
        findings.append("DL-SUPPLY: mandatory offline verification closure is incomplete")
    admission_order = c.get("supplyChain", {}).get("admissionOrder", [])
    if len(admission_order) < 8 or "atomically activate set" not in admission_order:
        findings.append("DL-SUPPLY: exact set is not atomically verified and activated")
    if "no network" not in c.get("supplyChain", {}).get("offline", ""):
        findings.append("DL-SUPPLY: offline verification can fetch trust data")
    for fx in c.get("releaseFixtures", []):
        errs = release_errors(fx, c)
        codes = {code for code, _ in errs}
        if fx["valid"] and errs:
            findings.append(f"{errs[0][0]} {fx['id']}: expected valid — {errs[0][1]}")
        elif not fx["valid"]:
            if not errs:
                findings.append(f"{fx.get('violates')} {fx['id']}: expected rejection")
            elif fx.get("violates") not in codes:
                findings.append(f"{fx['id']}: rejected by {sorted(codes)}, not {fx.get('violates')}")

    # DL-AIRGAP.
    ag = c.get("airGapMigration", {}).get("contract", {})
    for key in ("window", "legacyInspector", "outsideWindow", "bridgeImport", "reinterpretation"):
        if not ag.get(key):
            findings.append(f"DL-AIRGAP: contract omits {key}")
    if "No indefinite" not in ag.get("legacyInspector", "") or \
            "migration-unavailable" not in ag.get("outsideWindow", ""):
        findings.append("DL-AIRGAP: compatibility is unbounded or falsely useful")
    for fx in c.get("migrationFixtures", []):
        got = migration_outcome(fx)
        errs = []
        if fx.get("networkUsed"):
            errs.append("migration used network")
        if got != fx.get("expect"):
            errs.append(f"derived {got}, expected {fx.get('expect')}")
        if fx["valid"] and errs:
            findings.append(f"DL-AIRGAP {fx['id']}: expected valid — {errs[0]}")
        elif not fx["valid"] and not errs:
            findings.append(f"DL-AIRGAP {fx['id']}: expected rejection")

    # DL-EXPL / DL-ASSURE.
    explain = c.get("explainTrace", {})
    if not explain.get("commonStates") or not any(
            x.get("support") == "UNSUPPORTED" for x in explain.get("byClass", [])):
        findings.append("DL-EXPL: opaque evaluator does not report UNSUPPORTED")
    assurance = c.get("assuranceStatus", {})
    states = set(op.get("assuranceStateMachine", {}).get("states", [])) if op else set()
    if not op:
        findings.append(f"DL-ASSURE: could not load {OP}")
    for prop in assurance.get("properties", []):
        if prop.get("state") not in states:
            findings.append(f"DL-ASSURE {prop.get('id')}: unknown assurance state")
        if prop.get("state") in {"QUALIFIED", "DEMONSTRATED"}:
            findings.append(f"DL-ASSURE {prop.get('id')}: paper contract claims product evidence")
    if assurance.get("releaseState") != "NOT-DEMONSTRATED":
        findings.append("DL-ASSURE: release is presented as demonstrated without evidence")
    tests = {t.get("id"): t for t in c.get("conformanceTests", [])}
    if tests.get("DL-11", {}).get("state") != "IMPLEMENTABLE":
        findings.append("DL-PLATFORM: platform gate remains falsely unimplementable after decisions")
    if tests.get("DL-12", {}).get("state") != "IMPLEMENTABLE":
        findings.append("DL-D9: cross-contract termination mapping has no implementable conformance test")
    if tests.get("DL-13", {}).get("state") != "IMPLEMENTABLE":
        findings.append("DL-TS: TypeScript provider topology has no implementable conformance test")
    if tests.get("DL-14", {}).get("state") != "IMPLEMENTABLE":
        findings.append("DL-SCOPE: external-scanner overlay has no implementable conformance test")
    properties = {p.get("id"): p for p in assurance.get("properties", [])}
    if properties.get("DL.P8", {}).get("testIds") != ["DL-12"]:
        findings.append("DL-D9: assurance registry does not bind the termination join to DL-12")
    if properties.get("DL.P9", {}).get("testIds") != ["DL-13"]:
        findings.append("DL-TS: assurance registry does not bind TypeScript topology to DL-13")
    if properties.get("DL.P10", {}).get("testIds") != ["DL-14"]:
        findings.append("DL-SCOPE: assurance registry does not bind scanner overlay to DL-14")

    # DL-TM.
    if not tm:
        findings.append(f"DL-TM: could not load {TM}")
    else:
        live = tm_ids(tm)
        for dep in c.get("decisionDependencies", []):
            for ref in dep.get("refs", []):
                if ref not in live:
                    findings.append(f"DL-TM: dependency cites unknown property {ref}")
    return findings


def check(c: object, tm: dict | None, fp: dict | None, op: dict | None,
          d9: dict | None) -> list[str]:
    """Total parsed-JSON checker: malformed schema types are findings, never crashes."""
    if not isinstance(c, dict):
        return ["DL-TYPE: DELIVERY root must be a JSON object"]
    try:
        return _check_impl(c, tm, fp, op, d9)
    except (AttributeError, TypeError, KeyError, IndexError, ValueError, OverflowError):
        # Do not reflect attacker-controlled values or implementation-specific exception text.
        return ["DL-TYPE: DELIVERY contains a malformed JSON container or field type"]


def _missing_verification(c):
    for fx in c["deliveryFixtures"]:
        if fx["id"] == "published-blocking-ok":
            fx.pop("verificationState", None)
            fx.pop("verificationEvidenceId", None)


def _paper_discharge(c):
    c["assuranceStatus"]["properties"][0]["state"] = "DEMONSTRATED"


def _delete_rust_decision(c):
    c["rustSemanticSubstrate"]["decision"] = "TBD"


def _empty_platforms(c):
    c["platformMatrix"]["supported"] = []


def _delete_manifest_schema(c):
    del c["releaseManifestSchema"]["ReleaseManifestV1"]


def _prose_profile(c):
    c["installProfiles"]["profiles"][0]["capabilityManifest"] = "typescript rust syntax"


def _default_core(c):
    c["installProfiles"]["defaultProfile"] = "core"


def _unbounded_compat(c):
    c["airGapMigration"]["contract"]["outsideWindow"] = "Name a bridge and promise usefulness."


def _local_override(c):
    c["provenancePolicy"]["precedence"] = "A tracked override may promote local code."


def _network_trust(c):
    c["supplyChain"]["offline"] = "Fetch current revocation metadata before install."


def _self_referential_manifest_id(c):
    c["releaseManifestSchema"]["canonicalization"]["signedBytes"] = \
        "UTF8(domain) || JCS(manifest with signatures omitted)"


def _drop_key_identity(c):
    c["releaseManifestSchema"]["KeyDescriptor"]["required"].remove("keyId")


def _unsigned_bridge(c):
    for fx in c["migrationFixtures"]:
        if fx["id"] == "signed-bridge-import":
            fx["bridgeSignatureValid"] = False


def _trust_on_first_use(c):
    c["releaseManifestSchema"]["Trust"]["bootstrap"] = \
        "Trust the first root supplied by the release bundle."


def _provider_protocol_private_spelling(c):
    c["rustSemanticSubstrate"]["providerProtocol"]["frameIntegrity"] = \
        "An incomplete frame is PROVIDER.PROTOCOL_FAULT."


def _drop_excluded_feature_d9_join(c):
    del c["terminationIntegration"]["excludedCapabilityForm"]


def _embed_typescript_in_host(c):
    c["typescriptSemanticSubstrate"]["decision"] = "embedded-javascript-runtime"


def _reuse_typescript_worker(c):
    c["typescriptSemanticSubstrate"]["processModel"]["workerCardinality"] = \
        "Reuse one resident worker across all universes and ExecutionIds."


def _use_system_node(c):
    c["typescriptSemanticSubstrate"]["packaging"]["launch"] = \
        "Run node from PATH and load TypeScript from the project."


def _drop_typescript_compiler_identity(c):
    c["typescriptSemanticSubstrate"]["identity"]["providerDescriptor"][
        "closedRequired"].remove("typescriptCompilerSha256")


def _drop_typescript_runtime_identity(c):
    c["typescriptSemanticSubstrate"]["identity"]["handshakeRequired"].remove(
        "runtimeDescriptorSha256")


def _pass_live_worktree_to_typescript(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["snapshotTransport"]["rule"] = \
        "Pass the live worktree root and let the worker read files on demand."


def _make_stderr_authoritative(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["stderr"] = \
        "Parse facts and terminal status from stderr without a byte cap."


def _let_typescript_commit(c):
    c["typescriptSemanticSubstrate"]["authority"]["durable"] = \
        "The worker writes facts directly to CAS and seals its Run."


def _claim_typescript_sandbox(c):
    c["typescriptSemanticSubstrate"]["tcbPosture"] = \
        "The process boundary is a proven security sandbox."


def _drop_typescript_process_ownership(c):
    del c["typescriptSemanticSubstrate"]["processModel"]["ownership"]


def _drop_typescript_protocol_ordering(c):
    del c["typescriptSemanticSubstrate"]["providerProtocol"]["ordering"]


def _drop_typescript_clean_unavailable(c):
    del c["typescriptSemanticSubstrate"]["supervision"]["cleanUnavailable"]


def _drop_typescript_deterministic_budget(c):
    del c["typescriptSemanticSubstrate"]["supervision"]["deterministicBudget"]


def _drop_typescript_network_authority(c):
    del c["typescriptSemanticSubstrate"]["authority"]["network"]


def _drop_typescript_offline_assets(c):
    del c["typescriptSemanticSubstrate"]["offlineAssets"]


def _multiplex_typescript_universes(c):
    cardinality = c["typescriptSemanticSubstrate"]["processModel"]["workerCardinality"]
    cardinality["multiplexDifferentUniverseKeys"] = True


def _reuse_typescript_execution_worker(c):
    cardinality = c["typescriptSemanticSubstrate"]["processModel"]["workerCardinality"]
    cardinality["reuseAcrossExecutionIds"] = True


def _permit_interleaved_typescript_stage_output(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["ordering"]["stageOrder"] = \
        "FactBatch and Coverage frames from requested stages may interleave."


def _drop_typescript_payload_schema(c):
    del c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "payloadSchemas"]["CoverageV1"]


def _open_typescript_payload_schema(c):
    payload = c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "payloadSchemas"]["AnalyzeV1"]
    payload["closed"] = False
    payload["optional"] = ["extensionData"]


def _drop_typescript_payload_required_field(c):
    payload = c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "payloadSchemas"]["OpenUniverseV1"]
    payload["required"].remove("planIntentCommitment")


def _misbind_typescript_frame(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "frameSchemas"]["FactBatch"]["direction"] = "host-to-worker"


def _allow_second_typescript_analyze(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "multiStageAnalyze"]["analyzeFramesPerWorker"] = 2


def _drop_typescript_result_attribution(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "multiStageAnalyze"]["resultAttribution"] = "POSITIONAL"


def _let_typescript_worker_mint_fact_id(c):
    candidate = c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "definitions"]["FactCandidateV1"]
    candidate["fields"]["factId"] = "worker-minted fact identity"
    candidate["hostJoin"] = "The worker's factId is authoritative."


def _drop_typescript_coverage_key_field(c):
    key = c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "definitions"]["CoverageKeyV1"]
    key["required"].remove("subjectScopeCommitment")


def _inherit_typescript_parent_environment(c):
    c["typescriptSemanticSubstrate"]["authority"]["environment"]["inheritParent"] = True


def _make_typescript_budget_wallclock_semantic(c):
    c["typescriptSemanticSubstrate"]["supervision"]["deterministicBudget"][
        "wallClock"] = "Worker wall-clock expiry emits a semantic BudgetExhausted."


def _allow_unavailable_after_facts(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["ordering"][
        "unavailableTerminal"] = "Unavailable may follow any number of FactBatch frames."


def _drop_typescript_wire_commitment(c):
    del c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchemaCommitment"]


def _root_json_string(_c):
    return "delivery"


def _root_json_null(_c):
    return None


def _root_json_array(_c):
    return []


def _typescript_ordering_exact_permissive_string(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["ordering"] = \
        "Any frame in any order."


def _typescript_wire_schema_string(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"] = "wire"


def _typescript_wire_schema_null(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"] = None


def _typescript_wire_schema_array(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"] = []


def _typescript_frame_schemas_scalar(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "frameSchemas"] = 7


def _typescript_payload_schemas_scalar(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "payloadSchemas"] = False


def _typescript_payload_schema_string(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "payloadSchemas"]["CoverageV1"] = "payload"


def _typescript_payload_schema_null(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "payloadSchemas"]["CoverageV1"] = None


def _typescript_payload_schema_array(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "payloadSchemas"]["CoverageV1"] = []


def _typescript_definitions_scalar(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "definitions"] = "definitions"


def _typescript_nested_definition_string(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "definitions"]["StageRequestV1"] = "stage"


def _typescript_nested_definition_null(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "definitions"]["StageRequestV1"] = None


def _typescript_nested_definition_array(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "definitions"]["StageRequestV1"] = []


def _typescript_multi_stage_scalar(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "multiStageAnalyze"] = "multi"


def _typescript_stage_projection_scalar(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "stageRequestProjection"] = None


def _typescript_coverage_domain_scalar(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "coverageDomain"] = []


def _drop_typescript_depends_normalization(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "stageRequestProjection"]["fieldProjection"]["dependsOn"] = \
        "copy only when present"


def _drift_typescript_default_budget(c):
    c["typescriptSemanticSubstrate"]["identity"]["defaultWorkBudgetProfile"][
        "profile"]["budget"]["typeQueries"] += 1


def _map_work_units_to_one_counter(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "stageRequestProjection"]["budgetProjection"]["work-units"]["rule"] = \
        "Map L only to typeQueries."


def _admit_typescript_milliseconds_budget(c):
    c["initialProductScope"]["v1PlanIntentOverlay"]["axes"][
        "typescriptStageBudgetUnit"]["dispositions"]["milliseconds"] = {
            "decision": "ALLOW"}


def _drop_requested_coverage_domain_field(c):
    stage = c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "definitions"]["StageRequestV1"]
    stage["required"].remove("requestedCoverageDomain")


def _drop_cross_universe_target_partition(c):
    domain = c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "coverageDomain"]
    domain["targetPartition"]["crossUniverse"] = \
        "Emit only the source universe key."


def _drift_subject_scope_commitment_vector(c):
    scope = c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "coverageDomain"]["vectorConstants"]["subjectScope"]
    scope["subjectScopeCommitment"] = "sha256:" + "0" * 64


def _drop_cross_universe_unavailable_result(c):
    vectors = c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "coverageDomain"]["vectors"]
    vector = next(v for v in vectors if v["id"] ==
                  "cross-universe-unavailable-two-targets")
    vector["expectedCoverage"].pop()


def _drop_cross_universe_budget_target(c):
    vectors = c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "coverageDomain"]["vectors"]
    vector = next(v for v in vectors if v["id"] ==
                  "cross-universe-budget-exhausted-two-targets")
    vector["requestedCoverageDomain"]["keys"].pop()
    vector["requestedCoverageDomain"]["expectedKeyCount"] = 1
    vector["expectedCoverage"].pop()


def _truncate_coverage_domain_overflow(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "coverageDomain"]["overflowFate"]["arithmetic"] = \
        "Truncate to the first 128 keys and spawn."


def _alias_canonical_provider_id(c):
    c["typescriptSemanticSubstrate"]["providerProtocol"][
        "canonicalProviderIdJoin"]["canonicalProviderIds"][1] = \
        "provider.typescript-semantic"


def _drop_fact_record_contract_join(c):
    del c["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"][
        "definitions"]["FactCandidateV1"]["factRecordJoin"]


def _admit_external_scanner(c):
    c["initialProductScope"]["externalScannerOverlay"]["decision"] = "admit"


def _allocate_scanner_execution_id(c):
    c["initialProductScope"]["externalScannerOverlay"]["identityOutcome"][
        "executionId"] = "ALLOCATED"


def _inspect_scanner_after_plan(c):
    c["initialProductScope"]["externalScannerOverlay"]["inputRepresentation"] = \
        "Inspect a reconstructed ExecutionPlan after attempt admission."


def _grow_d9_for_scanner(c):
    c["terminationIntegration"]["excludedExternalScanner"]["d9ErrorCode"] = \
        "FEATURE.EXTERNAL_SCANNER_NOT_IN_V1"


def _make_scanner_fixture_not_c2_valid(c):
    base = c["initialProductScope"]["v1PlanIntentOverlay"]["fixtureModel"][
        "baseAllowedAnalysisIntent"]
    base["analysis"]["admissionDescriptor"]["contributions"][0].pop("activationId")


def _untype_scanner_domain_reason(c):
    c["initialProductScope"]["domainReasonVocabulary"]["values"].remove(
        "FEATURE.EXTERNAL_SCANNER_NOT_IN_V1")


def _drop_scanner_request_id(c):
    del c["initialProductScope"]["externalScannerOverlay"]["identityOutcome"][
        "requestId"]


def _make_scanner_request_id_optional(c):
    request_id = c["initialProductScope"]["externalScannerOverlay"][
        "identityOutcome"]["requestId"]
    request_id["state"] = "OPTIONAL"


def _allocate_scanner_request_id_late(c):
    request_id = c["initialProductScope"]["externalScannerOverlay"][
        "identityOutcome"]["requestId"]
    request_id["allocation"] = "ALLOCATED_AFTER_PLANINTENT_VALIDATION"


def _admit_scanner_after_overlay_check(c):
    c["initialProductScope"]["admissionRule"][
        "externalScannerAdmissionAfterCheck"] = True


def _drop_resident_overlay_disposition(c):
    del c["initialProductScope"]["v1PlanIntentOverlay"]["axes"][
        "executionTopology"]["dispositions"]["resident-single-project"]


def _admit_repair_workflow(c):
    c["initialProductScope"]["v1PlanIntentOverlay"]["axes"][
        "workflowIntent"]["dispositions"]["repair"] = {"decision": "ALLOW"}


def _drop_v1_excluded_class_fixture(c):
    cases = c["initialProductScope"]["v1PlanIntentOverlay"]["fixtureModel"]["cases"]
    cases[:] = [case for case in cases if case.get("id") != "reject-project-hook"]


def _allocate_attempt_in_scope_rejection(c):
    c["initialProductScope"]["v1PlanIntentOverlay"]["fixtureModel"][
        "commonRejectOutcome"]["attemptRecordCreated"] = True


def _weaken_rust_repository_condition(c):
    c["initialProductScope"]["v1PlanIntentOverlay"]["conditions"][
        "rust-repository-execution"]["parameterFields"] = ["network"]


def _drop_v1_overlay_commitment(c):
    del c["initialProductScope"]["v1PlanIntentOverlayCommitment"]


MUTATIONS = [
    ("allow missing verification to block (R2-DL-01)", _missing_verification),
    ("call an unexecuted property DEMONSTRATED (R2-DL-02)", _paper_discharge),
    ("reopen the Rust substrate (R2-DL-03)", _delete_rust_decision),
    ("erase the supported-platform domain (R2-DL-03)", _empty_platforms),
    ("delete the release manifest schema (R2-DL-05)", _delete_manifest_schema),
    ("replace a typed capability manifest with prose (R2-DL-06)", _prose_profile),
    ("make syntax-only core the supported default (R2-DL-07)", _default_core),
    ("promise compatibility beyond the bundled window (R2-DL-04)", _unbounded_compat),
    ("let an override promote local provenance (R2-DL-08)", _local_override),
    ("fetch trust data during offline verification (R2-DL-05)", _network_trust),
    ("make manifestId hash recursively include itself (R2-DL-05)",
     _self_referential_manifest_id),
    ("drop key identity from trust metadata (R2-DL-05)", _drop_key_identity),
    ("accept an unsigned offline bridge (R2-DL-04/05)", _unsigned_bridge),
    ("replace pinned root bootstrap with TOFU (R2-DL-05)", _trust_on_first_use),
    ("reintroduce provider-private protocol fault spelling (IMP-DL-D9-01)",
     _provider_protocol_private_spelling),
    ("drop excluded-feature domain-to-D9 join (IMP-DL-D9-02)",
     _drop_excluded_feature_d9_join),
    ("embed TypeScript in the Rust host (IP-R4-03)", _embed_typescript_in_host),
    ("reuse TypeScript worker state across universes (IP-R4-03)",
     _reuse_typescript_worker),
    ("resolve Node/TypeScript from the ambient system (IP-R4-03)", _use_system_node),
    ("drop pinned TypeScript compiler identity (IP-R4-03)",
     _drop_typescript_compiler_identity),
    ("drop pinned JavaScript runtime handshake identity (IP-R4-03)",
     _drop_typescript_runtime_identity),
    ("let TypeScript reopen the live worktree (IP-R4-03)",
     _pass_live_worktree_to_typescript),
    ("turn stderr into an authoritative unbounded channel (IP-R4-03)",
     _make_stderr_authoritative),
    ("let TypeScript worker commit durable state (IP-R4-03)", _let_typescript_commit),
    ("claim a bare TypeScript process is a sandbox (IP-R4-03)",
     _claim_typescript_sandbox),
    ("drop host/worker ownership split (R5-PROBE-01)",
     _drop_typescript_process_ownership),
    ("drop protocol ordering state machine (R5-PROBE-02)",
     _drop_typescript_protocol_ordering),
    ("drop clean Unavailable fate (R5-PROBE-03)",
     _drop_typescript_clean_unavailable),
    ("drop deterministic BudgetExhausted fate (R5-PROBE-04)",
     _drop_typescript_deterministic_budget),
    ("drop TypeScript network authority rule (R5-PROBE-05)",
     _drop_typescript_network_authority),
    ("drop exact offline asset closure (R5-PROBE-06)",
     _drop_typescript_offline_assets),
    ("multiplex distinct TypeScript universe keys (R5-PROBE-07)",
     _multiplex_typescript_universes),
    ("reuse TypeScript child across ExecutionIds (R5-PROBE-07)",
     _reuse_typescript_execution_worker),
    ("permit interleaved logical-stage results (R5-PROBE-08)",
     _permit_interleaved_typescript_stage_output),
    ("delete one protocol-major-1 payload schema (R5-DLTS-01)",
     _drop_typescript_payload_schema),
    ("open a protocol payload to unknown optional fields (R5-DLTS-01)",
     _open_typescript_payload_schema),
    ("remove a required wire field (R5-DLTS-01)",
     _drop_typescript_payload_required_field),
    ("bind a frame to the wrong direction (R5-DLTS-01)",
     _misbind_typescript_frame),
    ("permit two Analyze frames per TypeScript child (R5-DLTS-01)",
     _allow_second_typescript_analyze),
    ("erase exact per-stage result attribution (R5-DLTS-01)",
     _drop_typescript_result_attribution),
    ("let the TypeScript worker mint FactId (R5-DLTS-01)",
     _let_typescript_worker_mint_fact_id),
    ("drift TypeScript CoverageKey from live C-2 (R5-DLTS-01)",
     _drop_typescript_coverage_key_field),
    ("inherit the parent environment in the TypeScript child (R5-DLTS-03)",
     _inherit_typescript_parent_environment),
    ("turn wall clock into a semantic provider budget (R5-DLTS-03)",
     _make_typescript_budget_wallclock_semantic),
    ("allow clean Unavailable after candidate facts (R5-DLTS-03)",
     _allow_unavailable_after_facts),
    ("remove the committed protocol-major-1 wire schema (R5-DLTS-01)",
     _drop_typescript_wire_commitment),
    ("replace DELIVERY root with a JSON string (R5R-DLTS-04)",
     _root_json_string),
    ("replace DELIVERY root with JSON null (R5R-DLTS-04)",
     _root_json_null),
    ("replace DELIVERY root with a JSON array (R5R-DLTS-04)",
     _root_json_array),
    ("retain exact permissive ordering scalar probe (R5R-DLTS-04)",
     _typescript_ordering_exact_permissive_string),
    ("replace wireSchema with a string (R5R-DLTS-04)",
     _typescript_wire_schema_string),
    ("replace wireSchema with null (R5R-DLTS-04)",
     _typescript_wire_schema_null),
    ("replace wireSchema with an array (R5R-DLTS-04)",
     _typescript_wire_schema_array),
    ("replace frameSchemas with a scalar (R5R-DLTS-04)",
     _typescript_frame_schemas_scalar),
    ("replace payloadSchemas with a scalar (R5R-DLTS-04)",
     _typescript_payload_schemas_scalar),
    ("replace one payload schema with a string (R5R-DLTS-04)",
     _typescript_payload_schema_string),
    ("replace one payload schema with null (R5R-DLTS-04)",
     _typescript_payload_schema_null),
    ("replace one payload schema with an array (R5R-DLTS-04)",
     _typescript_payload_schema_array),
    ("replace definitions with a scalar (R5R-DLTS-04)",
     _typescript_definitions_scalar),
    ("replace one nested definition with a string (R5R-DLTS-04)",
     _typescript_nested_definition_string),
    ("replace one nested definition with null (R5R-DLTS-04)",
     _typescript_nested_definition_null),
    ("replace one nested definition with an array (R5R-DLTS-04)",
     _typescript_nested_definition_array),
    ("replace multiStageAnalyze with a scalar (R5R-DLTS-04)",
     _typescript_multi_stage_scalar),
    ("replace StageRequest projection with null (R5R-DLTS-01/04)",
     _typescript_stage_projection_scalar),
    ("replace Coverage domain with an array (R5R-DLTS-03/04)",
     _typescript_coverage_domain_scalar),
    ("remove absent dependsOn normalization (R5R-DLTS-01)",
     _drop_typescript_depends_normalization),
    ("drift signed default TypeScript work budget (R5R-DLTS-01)",
     _drift_typescript_default_budget),
    ("map C-2 work units to only one counter (R5R-DLTS-01)",
     _map_work_units_to_one_counter),
    ("admit semantic milliseconds into the TypeScript provider (R5R-DLTS-01)",
     _admit_typescript_milliseconds_budget),
    ("remove requested Coverage domain from StageRequest (R5R-DLTS-03)",
     _drop_requested_coverage_domain_field),
    ("collapse cross-universe target partitions (R5R-DLTS-03)",
     _drop_cross_universe_target_partition),
    ("drift the subject-scope commitment oracle (R5R-DLTS-03)",
     _drift_subject_scope_commitment_vector),
    ("omit one cross-universe Unavailable result (R5R-DLTS-03)",
     _drop_cross_universe_unavailable_result),
    ("omit one cross-universe BudgetExhausted target (R5R-DLTS-03)",
     _drop_cross_universe_budget_target),
    ("truncate requested Coverage on overflow (R5R-DLTS-03)",
     _truncate_coverage_domain_overflow),
    ("restore a prefixed provider alias (R5R-DLTS-05)",
     _alias_canonical_provider_id),
    ("drop the exact FACT-PLANE record join (R5R-DLTS-02)",
     _drop_fact_record_contract_join),
    ("admit the v1-excluded external scanner (IP-R4-05)", _admit_external_scanner),
    ("allocate ExecutionId for rejected scanner (IP-R4-05)",
     _allocate_scanner_execution_id),
    ("defer scanner inspection until after Plan/attempt (IP-R4-05)",
     _inspect_scanner_after_plan),
    ("grow D9 vocabulary for scanner scope detail (IP-R4-05)", _grow_d9_for_scanner),
    ("call a malformed scanner intent C-2-valid (IP-R4-05)",
     _make_scanner_fixture_not_c2_valid),
    ("remove scanner detail from the typed domain union (IP-R4-05)",
     _untype_scanner_domain_reason),
    ("drop mandatory RequestId from scanner rejection (R5-DLSCOPE-01)",
     _drop_scanner_request_id),
    ("make rejected scanner RequestId optional (R5-DLSCOPE-01)",
     _make_scanner_request_id_optional),
    ("allocate scanner RequestId after validation (R5-DLSCOPE-02)",
     _allocate_scanner_request_id_late),
    ("admit scanner after the product-scope check (R5-DLSCOPE-02)",
     _admit_scanner_after_overlay_check),
    ("leave a live resident topology unclassified (R7-C2-03)",
     _drop_resident_overlay_disposition),
    ("admit a v1-excluded repair workflow (R7-C2-03)",
     _admit_repair_workflow),
    ("drop one excluded-class zero-attempt fixture (R7-C2-03)",
     _drop_v1_excluded_class_fixture),
    ("allocate an AttemptRecord for a scope rejection (R7-C2-03)",
     _allocate_attempt_in_scope_rejection),
    ("weaken the Rust repository-execution conditional grant (R7-C2-03)",
     _weaken_rust_repository_condition),
    ("remove the committed total v1 overlay (R7-C2-03)",
     _drop_v1_overlay_commitment),
]


def selftest(base: dict, tm: dict | None, fp: dict | None, op: dict | None,
             d9: dict | None) -> int:
    pre = check(base, tm, fp, op, d9)
    if pre:
        print(f"REFUSING to self-test: base contract has {len(pre)} finding(s)")
        for item in pre[:8]:
            print("  -", item)
        return 1
    print("mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, mutation in MUTATIONS:
        candidate = copy.deepcopy(base)
        replacement = mutation(candidate)
        if replacement is not None or mutation is _root_json_null:
            candidate = replacement
        found = check(candidate, tm, fp, op, d9)
        if not found:
            escaped += 1
        print(f"  {'reject' if found else 'ESCAPE':>6}  {name}")
        print(f"          {found[0] if found else 'NO FINDING — mutation survived'}")
    print()
    if escaped:
        print(f"{escaped}/{len(MUTATIONS)} mutations ESCAPED")
        return 1
    print(f"all {len(MUTATIONS)} mutations rejected — adjudicated defects are load-bearing")
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    path = pathlib.Path(args[0]) if args else HERE / BINDING
    if not path.exists():
        print(f"missing contract: {path}", file=sys.stderr)
        return 2
    contract = json.loads(path.read_text())
    tm, fp, op, d9 = load(TM), load(FP), load(OP), load(D9)
    if "--selftest" in sys.argv:
        return selftest(contract, tm, fp, op, d9)
    found = check(contract, tm, fp, op, d9)
    if found:
        print(f"{len(found)} finding(s) in {path.name}:")
        for item in found:
            print("  -", item)
        return 1
    print(f"delivery OK — {path.name}, {len(contract['deliveryFixtures'])} admission/rollback fixtures, "
          f"{len(contract['migrationFixtures'])} migration fixtures, "
          f"{len(contract['releaseFixtures'])} release fixtures, "
          "DL-PROV / DL-ELIG / DL-SUPPLY / DL-PROF / DL-AIRGAP / DL-PLATFORM / "
          "DL-TS / DL-SCOPE / DL-EXPL / DL-TM / DL-ASSURE / DL-D9 clean")
    print(f"  P-4a: {contract['rustSemanticSubstrate']['decision']}; "
          f"supported platforms: {len(contract['platformMatrix']['supported'])}; "
          f"default profile: {contract['installProfiles']['defaultProfile']}")
    print("  product release state: NOT-DEMONSTRATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
