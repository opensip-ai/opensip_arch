// INERT GENERATION TRIAL. Owner SHA256 3f8a45f22f72cc52a74762d39079f5cdeca185f39ccb8421cb2085726d3f6981
import type { Handshake1HelloAckV3, Handshake1HelloV3, Handshake1TypeScriptHelloAckV2, Handshake1TypeScriptHelloV2, Native2CanonicalPath, Native2DependencySourceManifestV3, Native2DependencySourceSealV3, Native2PreparedOutputRowV3, Native2Relation, Native2Rung, Occupancy1Root, Startup1BudgetExhaustedV3, Startup1CoverageV3, Startup1NativeContextVerifiedV1, Startup1OpenUniverseV3, Startup1PreAnalyzeUnavailableV1, Startup1TypeScriptBudgetExhaustedV2, Startup1TypeScriptCoverageV2, Startup1TypeScriptOpenUniverseV2, Startup1TypeScriptUnavailableV2, Startup1TypeScriptUniverseAcceptedV2, Startup1UnavailableV3, Startup1UniverseAcceptedV3 } from "./externs.js";
export type Ts2DigestHex = string;

export type Ts2Sha256Text = string;

export type Ts2NfcText = string;

export type Ts2StageIdText = string;

export type Ts2SnapshotId2 = string;

export type Ts2PlanId2 = string;

export type Ts2ExecutionIdText = string;

export type Ts2ProjectPath = string;

export type Rust3IdentityText = string;

export type Rust3DigestHex = string;

export type Rust3Sha256Text = string;

export type Rust3CanonicalPath = string;

export type Rust3StageIdText = string;

export type Rust3SnapshotId2 = string;

export type Rust3PlanId2 = string;

export type Rust3CanonicalIdentifier = string;

export type Rust3PackageKey = string;

export type Ts2SnapshotEntryV1 = { readonly "kind": "file";
readonly "path": Ts2ProjectPath;
readonly "byteLength": bigint;
readonly "contentSha256": Ts2DigestHex;
readonly "linkTarget": null;
} | { readonly "kind": "symlink";
readonly "path": Ts2ProjectPath;
readonly "byteLength": 0n;
readonly "contentSha256": null;
readonly "linkTarget": string;
};

export interface Ts2SnapshotManifestV1 {
readonly "snapshotId": Ts2SnapshotId2;
readonly "manifestSha256": Ts2DigestHex;
readonly "entries": ReadonlyArray<Ts2SnapshotEntryV1>;
}

export interface Ts2SnapshotFileChunkV1 {
readonly "snapshotId": Ts2SnapshotId2;
readonly "path": Ts2ProjectPath;
readonly "chunkIndex": bigint;
readonly "byteOffset": bigint;
readonly "bytes": Uint8Array;
}

export interface Ts2SnapshotSealV1 {
readonly "snapshotId": Ts2SnapshotId2;
readonly "manifestSha256": Ts2DigestHex;
readonly "entryCount": bigint;
readonly "totalFileBytes": bigint;
readonly "totalChunkCount": bigint;
}

export interface Ts2SnapshotAcceptedV1 {
readonly "snapshotId": Ts2SnapshotId2;
readonly "manifestSha256": Ts2DigestHex;
readonly "entryCount": bigint;
readonly "totalFileBytes": bigint;
readonly "totalChunkCount": bigint;
}

export interface Ts2ProviderWorkBudgetV1 {
readonly "sourceFilesVisited": bigint;
readonly "astNodesVisited": bigint;
readonly "moduleResolutionQueries": bigint;
readonly "typeQueries": bigint;
readonly "factsEmitted": bigint;
readonly "factBytesEmitted": bigint;
}

export interface Ts2SubjectScopeV1 {
readonly "scopeKind": "all-snapshot-files";
readonly "snapshotId": Ts2SnapshotId2;
readonly "subjectCount": bigint;
readonly "subjectScopeCommitment": Ts2Sha256Text;
}

export interface Ts2CoverageKeyV1 {
readonly "relation": Native2Relation;
readonly "resolution": Native2Rung;
readonly "sourceUniverseId": Ts2Sha256Text;
readonly "targetUniverseId": Ts2Sha256Text;
readonly "subjectScopeCommitment": Ts2Sha256Text;
readonly "producer": "typescript-semantic";
readonly "producerVersion": Ts2NfcText;
readonly "schemaVersion": 1n;
}

export interface Ts2RequestedCoverageDomainV1 {
readonly "subjectScope": Ts2SubjectScopeV1;
readonly "keys": ReadonlyArray<Ts2CoverageKeyV1>;
readonly "domainCommitment": Ts2Sha256Text;
}

export interface Ts2StageRequestV1 {
readonly "stageId": Ts2StageIdText;
readonly "stageOrdinal": bigint;
readonly "operator": "semantic-provider";
readonly "providerId": "typescript-semantic";
readonly "dependsOn": ReadonlyArray<Ts2StageIdText>;
readonly "relations": ReadonlyArray<Native2Relation>;
readonly "budget": Ts2ProviderWorkBudgetV1;
readonly "requestedCoverageDomain": Ts2RequestedCoverageDomainV1;
}

export type Ts2AnchorRefV1 = { readonly "kind": "source-span";
readonly "snapshotId": Ts2SnapshotId2;
readonly "path": Ts2ProjectPath;
readonly "contentSha256": Ts2DigestHex;
readonly "startByte": bigint;
readonly "endByte": bigint;
readonly "factId": null;
} | { readonly "kind": "fact-ref";
readonly "snapshotId": null;
readonly "path": null;
readonly "contentSha256": null;
readonly "startByte": null;
readonly "endByte": null;
readonly "factId": string;
};

export interface Ts2FactCandidateV1 {
readonly "candidateOrdinal": bigint;
readonly "relation": Native2Relation;
readonly "resolution": Native2Rung;
readonly "layer": "derived" | "inventory" | "semantic" | "syntax";
readonly "producer": "typescript-semantic";
readonly "producerVersion": Ts2NfcText;
readonly "schemaVersion": bigint;
readonly "language": "typescript";
readonly "sourceUniverseId": Ts2Sha256Text;
readonly "targetUniverseId": Ts2Sha256Text;
readonly "confidenceMillionths": bigint;
readonly "relationSchemaId": string;
readonly "canonicalRelationPayload": Uint8Array;
readonly "anchors": ReadonlyArray<Ts2AnchorRefV1>;
}

export interface Ts2FactBatchV1 {
readonly "analysisOrdinal": 0n;
readonly "stageId": Ts2StageIdText;
readonly "batchIndex": bigint;
readonly "facts": ReadonlyArray<Ts2FactCandidateV1>;
readonly "batchCommitment": Ts2Sha256Text;
}

export interface Ts2FactBatchV3 {
readonly "schemaVersion": 3n;
readonly "analysisOrdinal": 0n;
readonly "stageId": Ts2StageIdText;
readonly "batchIndex": bigint;
readonly "candidates": ReadonlyArray<Ts2FactCandidateV1>;
readonly "occupancyCompanions": ReadonlyArray<Occupancy1Root>;
}

export interface Ts2AnalyzeV1 {
readonly "analysisOrdinal": 0n;
readonly "executionId": Ts2ExecutionIdText;
readonly "snapshotId": Ts2SnapshotId2;
readonly "planId": Ts2PlanId2;
readonly "universeKey": Ts2Sha256Text;
readonly "stageRequests": ReadonlyArray<Ts2StageRequestV1>;
}

export interface Ts2StageResultV1 {
readonly "stageId": Ts2StageIdText;
readonly "stageOrdinal": bigint;
readonly "factBatchCount": bigint;
readonly "factCount": bigint;
readonly "coverageEntryCount": bigint;
readonly "factCommitment": Ts2Sha256Text;
readonly "coverageCommitment": Ts2Sha256Text;
}

export interface Ts2CompleteV1 {
readonly "analysisOrdinal": 0n;
readonly "stageResults": ReadonlyArray<Ts2StageResultV1>;
readonly "factStreamCommitment": Ts2Sha256Text;
readonly "coverageStreamCommitment": Ts2Sha256Text;
}

export interface Ts2CancelV1 {
readonly "executionId": (Ts2ExecutionIdText) | null;
readonly "analysisOrdinal": (0n) | null;
readonly "reason": "host-shutdown" | "user-interrupt";
}

export interface Ts2CancelledV1 {
readonly "executionId": (Ts2ExecutionIdText) | null;
readonly "analysisOrdinal": (0n) | null;
readonly "observedPhase": "analysis" | "handshake" | "snapshot" | "universe";
}

export interface Ts2SnapshotFileSubjectV1 {
readonly "path": Ts2ProjectPath;
readonly "contentSha256": Ts2DigestHex;
readonly "byteLength": bigint;
}

export type Rust3SnapshotEntryV2 = { readonly "kind": "file";
readonly "path": Rust3CanonicalPath;
readonly "byteLength": bigint;
readonly "contentSha256": Rust3DigestHex;
readonly "executable": boolean;
readonly "targetBytes": null;
} | { readonly "kind": "symlink";
readonly "path": Rust3CanonicalPath;
readonly "byteLength": null;
readonly "contentSha256": null;
readonly "executable": null;
readonly "targetBytes": Uint8Array;
};

export interface Rust3SnapshotManifestV2 {
readonly "snapshotId": Rust3SnapshotId2;
readonly "manifestSha256": Rust3DigestHex;
readonly "entries": ReadonlyArray<Rust3SnapshotEntryV2>;
}

export interface Rust3SnapshotFileChunkV2 {
readonly "snapshotId": Rust3SnapshotId2;
readonly "path": Rust3CanonicalPath;
readonly "chunkIndex": bigint;
readonly "byteOffset": bigint;
readonly "bytes": Uint8Array;
}

export interface Rust3SnapshotSealV2 {
readonly "snapshotId": Rust3SnapshotId2;
readonly "manifestSha256": Rust3DigestHex;
readonly "entryCount": bigint;
readonly "totalFileBytes": bigint;
readonly "totalChunkCount": bigint;
}

export interface Rust3SnapshotAcceptedV2 {
readonly "snapshotId": Rust3SnapshotId2;
readonly "manifestSha256": Rust3DigestHex;
readonly "entryCount": bigint;
readonly "totalFileBytes": bigint;
readonly "totalChunkCount": bigint;
}

export interface Rust3DependencySourceChunkV3 {
readonly "dependencySourceSetId": Rust3Sha256Text;
readonly "packageKey": Rust3PackageKey;
readonly "path": Native2CanonicalPath;
readonly "chunkIndex": bigint;
readonly "byteOffset": bigint;
readonly "bytes": Uint8Array;
}

export type Rust3DependencySourceAcceptedV3 = Native2DependencySourceSealV3;

export interface Rust3PreparedOutputEntryV3 {
readonly "outputOrdinal": bigint;
readonly "kind": "build-script-directives" | "generated-file" | "macro-expansion";
readonly "planRow": Native2PreparedOutputRowV3;
readonly "logicalPath": string;
readonly "blobByteLength": bigint;
readonly "blobSha256": Rust3DigestHex;
readonly "contentByteLength": bigint;
readonly "contentSha256": Rust3DigestHex;
}

export interface Rust3PreparedOutputManifestV3 {
readonly "planId": Rust3PlanId2;
readonly "manifestSha256": Rust3DigestHex;
readonly "entries": ReadonlyArray<Rust3PreparedOutputEntryV3>;
}

export interface Rust3PreparedOutputChunkV3 {
readonly "planId": Rust3PlanId2;
readonly "outputOrdinal": bigint;
readonly "chunkIndex": bigint;
readonly "byteOffset": bigint;
readonly "bytes": Uint8Array;
}

export interface Rust3PreparedOutputSealV3 {
readonly "planId": Rust3PlanId2;
readonly "manifestSha256": Rust3DigestHex;
readonly "entryCount": bigint;
readonly "totalBlobBytes": bigint;
readonly "totalChunkCount": bigint;
}

export interface Rust3PreparedOutputAcceptedV3 {
readonly "planId": Rust3PlanId2;
readonly "manifestSha256": Rust3DigestHex;
readonly "entryCount": bigint;
readonly "totalBlobBytes": bigint;
readonly "totalChunkCount": bigint;
}

export interface Rust3SubjectV2 {
readonly "subjectOrdinal": bigint;
readonly "subjectId": string;
readonly "path": Rust3CanonicalPath;
readonly "startByte": 0n;
readonly "endByte": bigint;
}

export interface Rust3CoverageKeyV2 {
readonly "relation": Native2Relation;
readonly "resolution": Native2Rung;
readonly "sourceUniverseId": Rust3Sha256Text;
readonly "targetUniverseId": Rust3Sha256Text;
readonly "subjectScopeCommitment": Rust3Sha256Text;
readonly "producer": "rust-semantic";
readonly "producerVersion": Rust3IdentityText;
readonly "schemaVersion": bigint;
}

export interface Rust3StageAnalysisDomainV2 {
readonly "subjects": ReadonlyArray<Rust3SubjectV2>;
readonly "requestedCoverageDomain": ReadonlyArray<Rust3CoverageKeyV2>;
readonly "domainCommitment": Rust3Sha256Text;
}

export interface Rust3C2StageBudgetV1 {
readonly "unit": "bytes" | "items" | "milliseconds" | "work-units";
readonly "limit": bigint;
}

export interface Rust3C2PlanStageV3 {
readonly "kind": "fact-derivation";
readonly "stageId": Rust3StageIdText;
readonly "dependsOn"?: ReadonlyArray<Rust3StageIdText>;
readonly "budget"?: Rust3C2StageBudgetV1;
readonly "relations": ReadonlyArray<Native2Relation>;
readonly "operator": "semantic-provider";
readonly "capabilityGrants"?: ReadonlyArray<Rust3CanonicalIdentifier>;
readonly "providerId"?: "rust-semantic";
}

export interface Rust3StageRequestV2 {
readonly "stageOrdinal": bigint;
readonly "planStage": Rust3C2PlanStageV3;
readonly "analysisDomain": Rust3StageAnalysisDomainV2;
}

export interface Rust3AnalyzeV2 {
readonly "analysisOrdinal": bigint;
readonly "executionId": Rust3IdentityText;
readonly "snapshotId": Rust3SnapshotId2;
readonly "planId": Rust3PlanId2;
readonly "stages": ReadonlyArray<Rust3StageRequestV2>;
}

export type Rust3AnchorRefV1 = { readonly "kind": "source-span";
readonly "snapshotId": Rust3SnapshotId2;
readonly "path": Rust3CanonicalPath;
readonly "contentSha256": Rust3DigestHex;
readonly "startByte": bigint;
readonly "endByte": bigint;
readonly "factId": null;
} | { readonly "kind": "fact-ref";
readonly "snapshotId": null;
readonly "path": null;
readonly "contentSha256": null;
readonly "startByte": null;
readonly "endByte": null;
readonly "factId": string;
};

export interface Rust3FactCandidateV1 {
readonly "candidateOrdinal": bigint;
readonly "relation": Native2Relation;
readonly "resolution": Native2Rung;
readonly "layer": "derived" | "inventory" | "semantic" | "syntax";
readonly "producer": "rust-semantic";
readonly "producerVersion": Rust3IdentityText;
readonly "schemaVersion": bigint;
readonly "language": "rust";
readonly "sourceUniverseId": Rust3Sha256Text;
readonly "targetUniverseId": Rust3Sha256Text;
readonly "confidenceMillionths": bigint;
readonly "relationSchemaId": string;
readonly "canonicalRelationPayload": Uint8Array;
readonly "anchors": ReadonlyArray<Rust3AnchorRefV1>;
}

export interface Rust3FactBatchV2 {
readonly "analysisOrdinal": bigint;
readonly "stageId": Rust3StageIdText;
readonly "batchIndex": bigint;
readonly "candidates": ReadonlyArray<Rust3FactCandidateV1>;
}

export interface Rust3FactBatchV3 {
readonly "schemaVersion": 3n;
readonly "analysisOrdinal": bigint;
readonly "stageId": Rust3StageIdText;
readonly "batchIndex": bigint;
readonly "candidates": ReadonlyArray<Rust3FactCandidateV1>;
readonly "occupancyCompanions": ReadonlyArray<Occupancy1Root>;
}

export interface Rust3StageResultV2 {
readonly "stageId": Rust3StageIdText;
readonly "factCount": bigint;
readonly "coverageEntryCount": bigint;
readonly "factCommitment": Rust3Sha256Text;
readonly "coverageCommitment": Rust3Sha256Text;
}

export interface Rust3CompleteV2 {
readonly "analysisOrdinal": bigint;
readonly "stageResults": ReadonlyArray<Rust3StageResultV2>;
readonly "factStreamCommitment": Rust3Sha256Text;
readonly "coverageStreamCommitment": Rust3Sha256Text;
}

export interface Rust3ProviderFaultV2 {
readonly "executionId": (Rust3IdentityText) | null;
readonly "analysisOrdinal": (bigint) | null;
readonly "phase": "ANALYZING" | "READY_ANALYZE" | "READY_COMPLETE" | "READY_DEPENDENCY_MANIFEST" | "READY_OPEN_UNIVERSE" | "READY_PREPARED_MANIFEST" | "READY_SNAPSHOT_MANIFEST" | "RECEIVING_DEPENDENCY" | "RECEIVING_PREPARED" | "RECEIVING_SNAPSHOT" | "WAIT_DEPENDENCY_ACCEPTED" | "WAIT_HELLO_ACK" | "WAIT_NATIVE_CONTEXT_VERIFIED" | "WAIT_PREPARED_ACCEPTED" | "WAIT_SNAPSHOT_ACCEPTED" | "WAIT_UNIVERSE_ACCEPTED";
readonly "faultKind": "compiler-crash" | "input-rejected" | "internal-invariant";
readonly "detailCode": Rust3IdentityText;
}

export interface Rust3CancelV2 {
readonly "executionId": (Rust3IdentityText) | null;
readonly "analysisOrdinal": (bigint) | null;
readonly "reason": "user-interrupt";
}

export interface Rust3CancelledV2 {
readonly "executionId": (Rust3IdentityText) | null;
readonly "analysisOrdinal": (bigint) | null;
readonly "observedPhase": "ANALYZING" | "READY_ANALYZE" | "READY_COMPLETE" | "READY_DEPENDENCY_MANIFEST" | "READY_OPEN_UNIVERSE" | "READY_PREPARED_MANIFEST" | "READY_SNAPSHOT_MANIFEST" | "RECEIVING_DEPENDENCY" | "RECEIVING_PREPARED" | "RECEIVING_SNAPSHOT" | "WAIT_DEPENDENCY_ACCEPTED" | "WAIT_HELLO_ACK" | "WAIT_NATIVE_CONTEXT_VERIFIED" | "WAIT_PREPARED_ACCEPTED" | "WAIT_SNAPSHOT_ACCEPTED" | "WAIT_UNIVERSE_ACCEPTED";
}

export type Ts2FrameV2Payload = Handshake1TypeScriptHelloV2 | Startup1TypeScriptOpenUniverseV2 | Ts2SnapshotManifestV1 | Ts2SnapshotFileChunkV1 | Ts2SnapshotSealV1 | Ts2AnalyzeV1 | Ts2CancelV1 | Handshake1TypeScriptHelloAckV2 | Startup1TypeScriptUniverseAcceptedV2 | Ts2SnapshotAcceptedV1 | Startup1NativeContextVerifiedV1 | Ts2FactBatchV1 | Ts2FactBatchV3 | Startup1TypeScriptCoverageV2 | Startup1PreAnalyzeUnavailableV1 | Startup1TypeScriptUnavailableV2 | Startup1TypeScriptBudgetExhaustedV2 | Ts2CompleteV1 | Ts2CancelledV1;

export type Ts2FrameV2 = { readonly "protocolMajor": 2n; readonly "frameType": "Hello"; readonly "sequence": bigint; readonly "payload": Handshake1TypeScriptHelloV2; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "OpenUniverse"; readonly "sequence": bigint; readonly "payload": Startup1TypeScriptOpenUniverseV2; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "SnapshotManifest"; readonly "sequence": bigint; readonly "payload": Ts2SnapshotManifestV1; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "SnapshotFileChunk"; readonly "sequence": bigint; readonly "payload": Ts2SnapshotFileChunkV1; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "SnapshotSeal"; readonly "sequence": bigint; readonly "payload": Ts2SnapshotSealV1; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "Analyze"; readonly "sequence": bigint; readonly "payload": Ts2AnalyzeV1; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "Cancel"; readonly "sequence": bigint; readonly "payload": Ts2CancelV1; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "HelloAck"; readonly "sequence": bigint; readonly "payload": Handshake1TypeScriptHelloAckV2; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "UniverseAccepted"; readonly "sequence": bigint; readonly "payload": Startup1TypeScriptUniverseAcceptedV2; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "SnapshotAccepted"; readonly "sequence": bigint; readonly "payload": Ts2SnapshotAcceptedV1; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "NativeContextVerified"; readonly "sequence": bigint; readonly "payload": Startup1NativeContextVerifiedV1; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "FactBatch"; readonly "sequence": bigint; readonly "payload": Ts2FactBatchV1; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "FactBatch"; readonly "sequence": bigint; readonly "payload": Ts2FactBatchV3; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "Coverage"; readonly "sequence": bigint; readonly "payload": Startup1TypeScriptCoverageV2; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "Unavailable"; readonly "sequence": bigint; readonly "payload": Startup1PreAnalyzeUnavailableV1; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "Unavailable"; readonly "sequence": bigint; readonly "payload": Startup1TypeScriptUnavailableV2; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "BudgetExhausted"; readonly "sequence": bigint; readonly "payload": Startup1TypeScriptBudgetExhaustedV2; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "Complete"; readonly "sequence": bigint; readonly "payload": Ts2CompleteV1; }
 | { readonly "protocolMajor": 2n; readonly "frameType": "Cancelled"; readonly "sequence": bigint; readonly "payload": Ts2CancelledV1; };

export type Rust3ProviderFrameV3Payload = Handshake1HelloV3 | Handshake1HelloAckV3 | Startup1OpenUniverseV3 | Startup1UniverseAcceptedV3 | Rust3SnapshotManifestV2 | Rust3SnapshotFileChunkV2 | Rust3SnapshotSealV2 | Rust3SnapshotAcceptedV2 | Native2DependencySourceManifestV3 | Rust3DependencySourceChunkV3 | Native2DependencySourceSealV3 | Rust3DependencySourceAcceptedV3 | Rust3PreparedOutputManifestV3 | Rust3PreparedOutputChunkV3 | Rust3PreparedOutputSealV3 | Rust3PreparedOutputAcceptedV3 | Startup1NativeContextVerifiedV1 | Rust3AnalyzeV2 | Rust3FactBatchV2 | Rust3FactBatchV3 | Startup1CoverageV3 | Startup1PreAnalyzeUnavailableV1 | Startup1UnavailableV3 | Startup1BudgetExhaustedV3 | Rust3CompleteV2 | Rust3ProviderFaultV2 | Rust3CancelV2 | Rust3CancelledV2;

export type Rust3ProviderFrameV3 = { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "Hello"; readonly "payload": Handshake1HelloV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "HelloAck"; readonly "payload": Handshake1HelloAckV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "OpenUniverse"; readonly "payload": Startup1OpenUniverseV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "UniverseAccepted"; readonly "payload": Startup1UniverseAcceptedV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "SnapshotManifest"; readonly "payload": Rust3SnapshotManifestV2; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "SnapshotFileChunk"; readonly "payload": Rust3SnapshotFileChunkV2; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "SnapshotSeal"; readonly "payload": Rust3SnapshotSealV2; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "SnapshotAccepted"; readonly "payload": Rust3SnapshotAcceptedV2; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "DependencySourceManifest"; readonly "payload": Native2DependencySourceManifestV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "DependencySourceChunk"; readonly "payload": Rust3DependencySourceChunkV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "DependencySourceSeal"; readonly "payload": Native2DependencySourceSealV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "DependencySourceAccepted"; readonly "payload": Rust3DependencySourceAcceptedV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "PreparedOutputManifest"; readonly "payload": Rust3PreparedOutputManifestV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "PreparedOutputChunk"; readonly "payload": Rust3PreparedOutputChunkV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "PreparedOutputSeal"; readonly "payload": Rust3PreparedOutputSealV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "PreparedOutputAccepted"; readonly "payload": Rust3PreparedOutputAcceptedV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "NativeContextVerified"; readonly "payload": Startup1NativeContextVerifiedV1; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "Analyze"; readonly "payload": Rust3AnalyzeV2; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "FactBatch"; readonly "payload": Rust3FactBatchV2; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "FactBatch"; readonly "payload": Rust3FactBatchV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "CoverageV3"; readonly "payload": Startup1CoverageV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "Unavailable"; readonly "payload": Startup1PreAnalyzeUnavailableV1; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "Unavailable"; readonly "payload": Startup1UnavailableV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "BudgetExhausted"; readonly "payload": Startup1BudgetExhaustedV3; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "Complete"; readonly "payload": Rust3CompleteV2; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "ProviderFault"; readonly "payload": Rust3ProviderFaultV2; }
 | { readonly "protocolMajor": 3n; readonly "direction": "host-to-worker"; readonly "sequence": bigint; readonly "frameType": "Cancel"; readonly "payload": Rust3CancelV2; }
 | { readonly "protocolMajor": 3n; readonly "direction": "worker-to-host"; readonly "sequence": bigint; readonly "frameType": "Cancelled"; readonly "payload": Rust3CancelledV2; };
