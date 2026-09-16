// Native integration reference; exact source pins in assembly receipt. Inert types only.
export type Json = null | boolean | bigint | string | Json[] | {[key:string]:Json};
export type Control3Root = (({
    "body": ({
        "admittedManifestDigest": (string);
        "controlMajor": (bigint);
        "expectedStableId": (string);
        "maxControlFrameBytesOffer": (bigint);
        "platform": ({
            "arch": ("arm64" | "x86_64");
            "os": ("macos" | "linux");
        });
        "subprotocolOffers": ((({
            "role": (string);
            "roleSubprotocol": (string);
            "subprotocolVersion": (bigint);
        }))[]);
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("hello");
}) | ({
    "body": ({
        "admittedManifestDigest": (string);
        "controlMajor": (bigint);
        "maxControlFrameBytes": (bigint);
        "stableId": (string);
        "subprotocolConfirms": ((({
            "role": (string);
            "roleSubprotocol": (string);
            "subprotocolVersion": (bigint);
        }))[]);
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("helloAck");
}) | ({
    "body": ({
        "role": (string);
        "roleSubprotocol": (string);
        "subprotocolVersion": (bigint);
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("select");
}) | ({
    "body": ({
        "role": (string);
        "roleSubprotocol": (string);
        "subprotocolVersion": (bigint);
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("selectAck");
}) | ({
    "body": ({
        "decisionClass"?: ("PR-1" | "PR-2" | "PR-3" | "PR-4" | "PR-5" | "PR-6" | "PR-7" | "PR-8" | "PR-9");
        "detail"?: (string);
        "family": ("RF-1" | "RF-2" | "RF-3" | "RF-4" | "RF-5" | "RF-6" | "RF-7" | "RF-8");
        "supportedControlMajors"?: (((bigint))[]);
    }) & (Json & Json);
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("refusal");
}) | ({
    "body": ({
        "nonce": (string);
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("ping");
}) | ({
    "body": ({
        "nonce": (string);
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("pong");
}) | ({
    "body": ({
        "reason": ("user" | "deadline" | "supervisor-fault");
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("cancel");
}) | ({
    "body": ({
        "nonce": (string);
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("health");
}) | ({
    "body": ({
        "nonce": (string);
        "status": ("ready" | "busy" | "stopping");
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("healthReport");
}) | ({
    "body": ({
        "cpuNanoseconds": (bigint);
        "openHandles": (bigint);
        "residentBytes": (bigint);
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("resourceReport");
}) | ({
    "body": ({
        "detail": (string);
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("fault");
}) | ({
    "body": ({
        "authorizationRef": (string);
        "effectClass": ("HE-1" | "HE-2");
        "operationRef": (string);
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("effectRequest");
}) | ({
    "body": ({
        "commitClass": ("REVERSIBLE" | "IRREVERSIBLE");
        "decisionSeq": (bigint);
        "effectOutcome": ("COMPLETED" | "FAILED" | "INDETERMINATE");
        "outcomeSeq": (bigint);
        "requestSeq": (bigint);
        "resultRef"?: (string);
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("effectResult");
}) | ({
    "body": ({
        "reason": ("normal" | "cancelled" | "refused" | "fault");
    });
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("shutdown");
}) | ({
    "body": ({});
    "controlMajor": (bigint);
    "seq": (bigint);
    "type": ("shutdownAck");
}));
export type FactBatch3PropertiesCandidatesItems = ({
    "anchors": ((({
        [key: string]: Json;
    }))[]);
    "candidateOrdinal": (bigint);
    "canonicalRelationPayloadHex": (string);
    "confidenceMillionths": (bigint);
    "decodedRelationPayload": ({
        [key: string]: Json;
    });
    "language": (string);
    "layer": (string);
    "producer": (string);
    "producerVersion": (string);
    "relation": (string);
    "relationSchemaId": (string);
    "resolution": (string);
    "schemaVersion": (bigint);
    "sourceUniverseId": (string);
    "targetUniverseId": (string);
});
export type FactBatch3Root = ({
    "analysisOrdinal": (bigint);
    "batchIndex": (bigint);
    "candidates": ((({
        "anchors": ((({
            [key: string]: Json;
        }))[]);
        "candidateOrdinal": (bigint);
        "canonicalRelationPayloadHex": (string);
        "confidenceMillionths": (bigint);
        "decodedRelationPayload": ({
            [key: string]: Json;
        });
        "language": (string);
        "layer": (string);
        "producer": (string);
        "producerVersion": (string);
        "relation": (string);
        "relationSchemaId": (string);
        "resolution": (string);
        "schemaVersion": (bigint);
        "sourceUniverseId": (string);
        "targetUniverseId": (string);
    }))[]);
    "occupancyCompanions": ((Occupancy1Root)[]);
    "schemaVersion": (3n);
    "stageId": (string);
});
export type Handshake1DigestHex = (string);
export type Handshake1IdentityVersionsV1 = ({
    "coverage": (3n);
    "fact": (2n);
    "plan": (2n);
    "snapshot": (2n);
});
export type Handshake1NfcText = (string);
export type Handshake1Sha256Text = (string);
export type Handshake1StageIdText = (string);
export type Handshake1TypeScriptCapabilitiesV2 = ((Handshake1TypeScriptCapabilityToken)[]) & (Json & Json & Json & Json);
export type Handshake1TypeScriptCapabilityToken = ("coverage-v3" | "fact-identity-fact2" | "multi-stage-analyze-v1" | "native-context-v2" | "plan-identity-plan2" | "resolution-completeness-v2" | "sealed-vfs-v1" | "source-identity-snapshot2" | "target-attribution-v2" | "typescript-semantic-facts-v1" | "unresolved-edge-v1");
export type Handshake1TypeScriptFactBatchV1Vector = ({
    "analysisOrdinal": (0n);
    "batchCommitment": Handshake1Sha256Text;
    "batchIndex": Handshake1Uint64;
    "facts": ((FactBatch3PropertiesCandidatesItems)[]);
    "stageId": Handshake1StageIdText;
});
export type Handshake1TypeScriptHelloAckV2 = ({
    "capabilities": Handshake1TypeScriptCapabilitiesV2;
    "defaultWorkBudgetProfileId": ("typescript-provider-default-work-budget-v1");
    "defaultWorkBudgetProfileSha256": ("bf7305a12d26a1938b615c861f995d66eac494915e6140c4942a2ea6f0846da6");
    "identityVersions": Handshake1IdentityVersionsV1;
    "modulesAbi": Handshake1NfcText;
    "nodeVersion": Handshake1NfcText;
    "platformId": Handshake1NfcText;
    "protocolMajor": (2n);
    "providerBuildId": Handshake1NfcText;
    "providerDescriptorSha256": Handshake1DigestHex;
    "runtimeDescriptorSha256": Handshake1DigestHex;
    "typescriptCompilerSha256": Handshake1DigestHex;
    "typescriptStdlibMerkleRoot": Handshake1DigestHex;
    "typescriptVersion": Handshake1NfcText;
    "v8Version": Handshake1NfcText;
});
export type Handshake1TypeScriptHelloV2 = ({
    "expectedCapabilities": Handshake1TypeScriptCapabilitiesV2;
    "expectedProviderDescriptorSha256": Handshake1DigestHex;
    "expectedRuntimeDescriptorSha256": Handshake1DigestHex;
    "hostBuildId": Handshake1NfcText;
    "identityVersions": Handshake1IdentityVersionsV1;
    "limits": Handshake1TypeScriptProtocolLimitsV1;
});
export type Handshake1TypeScriptProtocolLimitsV1 = ({
    "maxAnalyzeStages": (1024n);
    "maxCoverageEntriesPerFrame": (4096n);
    "maxFactBatchFacts": (4096n);
    "maxFactCandidatePayloadBytes": (1048576n);
    "maxFramePayloadBytes": (67108864n);
    "maxRelationsPerStage": (64n);
    "maxRequestedCoverageKeysPerStage": (128n);
    "maxSnapshotChunkBytes": (1048576n);
    "maxSnapshotEntries": (200000n);
    "maxStderrBytes": (262144n);
});
export type Handshake1Uint64 = (bigint);
export type Native2ClosedWorldV2 = ({
    "deadCodeRepairEligible": (boolean);
    "dynamicDispatch": ("resolved" | "present" | "not-applicable");
    "entryPointsRecognized": ("all" | "partial" | "none");
    "exportsClosed": ("closed" | "open" | "unknown");
    "externalConsumers": ("none-declared" | "possible" | "unknown");
    "nonliteralLoading": ("none" | "present");
    "reasons": (((string))[]);
});
export type Native2CoverageKeyV2 = ({
    "relation": Native2Relation;
    "resolution": Native2Rung;
    "sourceUniverse": (string);
    "subjectScopeCommitment": (string);
    "targetUniverse": (string);
});
export type Native2CoverageResultV3 = ({
    "entry": Native2ViewEntryV3;
    "key": Native2CoverageKeyV2;
    "schemaVersion": (3n);
});
export type Native2DeficiencyV2 = ("language-tier-unsupported" | "provider-unavailable" | "input-closure-incomplete" | "budget-exhausted" | "confidence-floor-unmet" | "derivation-policy-unmet" | "resolution-incomplete" | "external-consumers-unknown" | "required-relation-missing");
export type Native2ExaminedUniverseV1 = ({
    "subjectCount": (bigint);
    "subjectScopeCommitment": (string);
});
export type Native2NativeCause = ("body-language-owner-ambiguous" | "body-language-owner-unenumerated" | "body-language-ownership-missing" | "capability-missing" | "config-flag-stripped" | "generated-file-missing" | "generated-file-out-of-bounds" | "generated-output-unavailable" | "linker-unavailable" | "lockfile-missing" | "missing-dependency-source" | "no-program-unit" | "node-modules-outside-read-set" | "source-replacement-outside-snapshot");
export type Native2Relation = ("file" | "package" | "vcs-change" | "declares" | "literal" | "control-flow" | "imports" | "references" | "calls" | "types" | "reachability" | "clones" | "unresolved-edge");
export type Native2ResolutionCompletenessState = ("complete" | "incomplete" | "partial" | "not-attempted" | "not-applicable");
export type Native2ResolutionCompletenessV2 = ({
    "attempted": (boolean);
    "examinedExhaustive": (boolean);
    "stageTerminal": (Native2StageTerminal | (null));
    "state": Native2ResolutionCompletenessState;
    "unresolvedEdgeClasses": ((Native2UnresolvedEdgeKindV1)[]);
    "unresolvedEdgeCount": (bigint);
});
export type Native2Rung = ("enumerated" | "manifest-declared" | "vcs-reported" | "syntactic" | "syntactic-specifier" | "resolved-target" | "syntactic-name-match" | "resolved-binding" | "syntactic-callee-name" | "resolved-callee" | "annotated" | "checked" | "from-resolved-calls" | "normalized-body-hash" | "observed");
export type Native2StageTerminal = ("complete" | "unavailable" | "budget-exhausted" | "provider-fault" | "cancelled" | "crash");
export type Native2SynthesizedCompilerOptionsV1 = ({
    "allowJs": (true);
    "checkJs": (false);
    "jsx"?: ("preserve");
    "module": ("node16");
    "moduleResolution": ("node16");
    "noEmit": (true);
    "skipLibCheck": (true);
    "strict": (false);
    "target": ("es2022");
    "types": ((Json)[]);
});
export type Native2TypeScriptUniverseV2ResolvedInputs = ({
    "allowJs": (boolean);
    "checkJs": (boolean);
    "configOrigin": ("tsconfig" | "jsconfig" | "synthesized");
    "executionCapableResolution": (false);
    "jsAdmittedToProgram": (boolean);
    "jsDiagnosticsEnabled": (boolean);
    "jsRootFiles": (((string))[]);
    "languageMode": ("ts-tsconfig" | "js-allowjs" | "js-synthesized");
    "lockfileKind": ("package-lock" | "pnpm-lock" | "yarn-lock" | "bun-lock" | "none");
    "nativeContextId": (string);
    "nodeModulesInReadSet": (boolean);
    "packageModuleType": ("module" | "commonjs" | "absent");
    "programRootFiles": (((string))[]);
    "resolutionCompletenessImplied": (false);
    "schemaVersion": (2n);
    "synthesizedOptions": (Native2SynthesizedCompilerOptionsV1 | (null));
    "synthesizerVersion": ((1n) | (null));
    "tsconfigGraphHash": (string);
});
export type Native2UnresolvedEdgeKindV1 = ("computed-member-access" | "dynamic-import-nonliteral" | "require-nonliteral" | "indirect-eval" | "reflective-access" | "untyped-any-call" | "unresolved-module-specifier" | "external-module-boundary" | "structural-dispatch" | "trait-object-dynamic-dispatch" | "generic-bound-dispatch" | "macro-expansion-unavailable" | "build-script-generated-unavailable" | "cfg-excluded-region" | "ffi-extern" | "entry-point-unrecognized");
export type Native2ViewEntryV3 = ({
    "closedWorld": Native2ClosedWorldV2;
    "confidenceMillionths": (bigint);
    "coverage": ("complete" | "unknown");
    "deficiency": (Native2DeficiencyV2 | (null));
    "derivationKinds": ((("annotated" | "jsdoc-declared" | "compiler-inferred"))[]);
    "examinedUniverse": Native2ExaminedUniverseV1;
    "nativeCause": (Native2NativeCause | (null));
    "relation": Native2Relation;
    "resolution": Native2Rung;
    "resolutionCompleteness": Native2ResolutionCompletenessV2;
});
export type Occupancy1LogicalPath = (string);
export type Occupancy1Root = ({
    "candidateOrdinal": (bigint);
    "evaluationNativeId": ((string) | (null));
    "exported": (("exported" | "not-exported" | "unknown") | (null));
    "kind": ("file" | "symbol" | "package" | "unknown");
    "logicalPath": (Occupancy1LogicalPath | (null));
    "occupancy": ("first-party" | "external" | "unknown");
    "packageManifestPath": (Occupancy1LogicalPath | (null));
    "schemaVersion": (1n);
    "targetNativeId": (string);
    "targetUniverseId": (string);
}) & (Json & Json & Json & Json & Json & Json & Json & Json);
export type Startup1DigestHex = (string);
export type Startup1ExecutionIdText = (string);
export type Startup1NativeContextVerifiedV1 = ({
    "equal": (true);
    "nativeContextId": Startup1Sha256Text;
    "recomputedNativeContextId": Startup1Sha256Text;
});
export type Startup1NfcText = (string);
export type Startup1PlanId2 = (string);
export type Startup1PreAnalyzeUnavailableV1 = ({
    "executionId": Startup1ExecutionIdText;
    "nativeContextId": Startup1Sha256Text;
    "planId": Startup1PlanId2;
    "reason": ("native-context-mismatch");
    "recomputedNativeContextId": Startup1Sha256Text;
    "snapshotId": Startup1SnapshotId2;
});
export type Startup1Sha256Text = (string);
export type Startup1SnapshotId2 = (string);
export type Startup1StageIdText = (string);
export type Startup1TypeScriptBudgetExhaustedV2 = ({
    "analysisOrdinal": (0n);
    "coverage": ((Native2CoverageResultV3)[]);
    "coverageCommitment": Startup1Sha256Text;
    "dimension": ("sourceFilesVisited" | "astNodesVisited" | "moduleResolutionQueries" | "typeQueries" | "factsEmitted" | "factBytesEmitted");
    "limit": Startup1Uint64;
    "observed": Startup1Uint64;
    "triggerStageId": Startup1StageIdText;
});
export type Startup1TypeScriptCoverageV2 = ({
    "analysisOrdinal": (0n);
    "coverageCommitment": Startup1Sha256Text;
    "entries": ((Native2CoverageResultV3)[]);
    "stageId": Startup1StageIdText;
});
export type Startup1TypeScriptOpenUniverseV2 = ({
    "executionId": Startup1ExecutionIdText;
    "planId": Startup1PlanId2;
    "planIntentCommitment": Startup1Sha256Text;
    "providerId": ("typescript-semantic");
    "snapshotId": Startup1SnapshotId2;
    "universe": Startup1TypeScriptSemanticUniverseV2;
    "universeKey": Startup1Sha256Text;
});
export type Startup1TypeScriptSemanticUniverseV2 = ({
    "capabilityManifestId": Startup1DigestHex;
    "manifestId": Startup1DigestHex;
    "modulesAbi": Startup1NfcText;
    "nodeVersion": Startup1NfcText;
    "platformId": Startup1NfcText;
    "protocolMajor": (2n);
    "providerArtifactId": ("typescript-provider");
    "providerArtifactSha256": Startup1DigestHex;
    "providerBuildId": Startup1NfcText;
    "providerDescriptorSha256": Startup1DigestHex;
    "resolvedInputs": Native2TypeScriptUniverseV2ResolvedInputs;
    "runtimeArtifactId": ("typescript-runtime");
    "runtimeArtifactSha256": Startup1DigestHex;
    "runtimeDescriptorSha256": Startup1DigestHex;
    "schemaVersion": (1n);
    "typescriptCompilerSha256": Startup1DigestHex;
    "typescriptStdlibMerkleRoot": Startup1DigestHex;
    "typescriptVersion": Startup1NfcText;
    "v8Version": Startup1NfcText;
});
export type Startup1TypeScriptUnavailableV2 = ({
    "affectedStageIds": ((Startup1StageIdText)[]);
    "analysisOrdinal": (0n);
    "coverage": ((Native2CoverageResultV3)[]);
    "coverageCommitment": Startup1Sha256Text;
    "reason": ("capability-missing" | "identity-version-mismatch" | "node-modules-outside-read-set" | "semantic-universe-incomplete" | "snapshot-resolution-input-missing" | "unsupported-compiler-mode");
});
export type Startup1TypeScriptUniverseAcceptedV2 = ({
    "executionId": Startup1ExecutionIdText;
    "planId": Startup1PlanId2;
    "snapshotId": Startup1SnapshotId2;
    "universeKey": Startup1Sha256Text;
});
export type Startup1Uint64 = (bigint);
export type Ts2DigestHex = string;
export type Ts2Sha256Text = string;
export type Ts2NfcText = string;
export type Ts2StageIdText = string;
export type Ts2SnapshotId2 = string;
export type Ts2PlanId2 = string;
export type Ts2ExecutionIdText = string;
export type Ts2ProjectPath = string;
export type Ts2SnapshotEntryV1 = {
    readonly "kind": "file";
    readonly "path": Ts2ProjectPath;
    readonly "byteLength": bigint;
    readonly "contentSha256": Ts2DigestHex;
    readonly "linkTarget": null;
} | {
    readonly "kind": "symlink";
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
export type Ts2AnchorRefV1 = {
    readonly "kind": "source-span";
    readonly "snapshotId": Ts2SnapshotId2;
    readonly "path": Ts2ProjectPath;
    readonly "contentSha256": Ts2DigestHex;
    readonly "startByte": bigint;
    readonly "endByte": bigint;
    readonly "factId": null;
} | {
    readonly "kind": "fact-ref";
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
export type Ts2FrameV2Payload = Handshake1TypeScriptHelloV2 | Startup1TypeScriptOpenUniverseV2 | Ts2SnapshotManifestV1 | Ts2SnapshotFileChunkV1 | Ts2SnapshotSealV1 | Ts2AnalyzeV1 | Ts2CancelV1 | Handshake1TypeScriptHelloAckV2 | Startup1TypeScriptUniverseAcceptedV2 | Ts2SnapshotAcceptedV1 | Startup1NativeContextVerifiedV1 | Ts2FactBatchV1 | Ts2FactBatchV3 | Startup1TypeScriptCoverageV2 | Startup1PreAnalyzeUnavailableV1 | Startup1TypeScriptUnavailableV2 | Startup1TypeScriptBudgetExhaustedV2 | Ts2CompleteV1 | Ts2CancelledV1;
export type Ts2FrameV2 = {
    readonly "protocolMajor": 2n;
    readonly "frameType": "Hello";
    readonly "sequence": bigint;
    readonly "payload": Handshake1TypeScriptHelloV2;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "OpenUniverse";
    readonly "sequence": bigint;
    readonly "payload": Startup1TypeScriptOpenUniverseV2;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "SnapshotManifest";
    readonly "sequence": bigint;
    readonly "payload": Ts2SnapshotManifestV1;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "SnapshotFileChunk";
    readonly "sequence": bigint;
    readonly "payload": Ts2SnapshotFileChunkV1;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "SnapshotSeal";
    readonly "sequence": bigint;
    readonly "payload": Ts2SnapshotSealV1;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "Analyze";
    readonly "sequence": bigint;
    readonly "payload": Ts2AnalyzeV1;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "Cancel";
    readonly "sequence": bigint;
    readonly "payload": Ts2CancelV1;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "HelloAck";
    readonly "sequence": bigint;
    readonly "payload": Handshake1TypeScriptHelloAckV2;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "UniverseAccepted";
    readonly "sequence": bigint;
    readonly "payload": Startup1TypeScriptUniverseAcceptedV2;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "SnapshotAccepted";
    readonly "sequence": bigint;
    readonly "payload": Ts2SnapshotAcceptedV1;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "NativeContextVerified";
    readonly "sequence": bigint;
    readonly "payload": Startup1NativeContextVerifiedV1;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "FactBatch";
    readonly "sequence": bigint;
    readonly "payload": Ts2FactBatchV1;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "FactBatch";
    readonly "sequence": bigint;
    readonly "payload": Ts2FactBatchV3;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "Coverage";
    readonly "sequence": bigint;
    readonly "payload": Startup1TypeScriptCoverageV2;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "Unavailable";
    readonly "sequence": bigint;
    readonly "payload": Startup1PreAnalyzeUnavailableV1;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "Unavailable";
    readonly "sequence": bigint;
    readonly "payload": Startup1TypeScriptUnavailableV2;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "BudgetExhausted";
    readonly "sequence": bigint;
    readonly "payload": Startup1TypeScriptBudgetExhaustedV2;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "Complete";
    readonly "sequence": bigint;
    readonly "payload": Ts2CompleteV1;
} | {
    readonly "protocolMajor": 2n;
    readonly "frameType": "Cancelled";
    readonly "sequence": bigint;
    readonly "payload": Ts2CancelledV1;
};
