// Generated candidate: explicit named type renderer; inert carriers, not admission.
export type Json = null | boolean | bigint | string | Json[] | {[key:string]:Json};
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
export type Handshake1TypeScriptCapabilityToken = ("coverage-v3" | "fact-identity-fact2" | "multi-stage-analyze-v1" | "native-context-v2" | "plan-identity-plan2" | "resolution-completeness-v2" | "sealed-vfs-v1" | "source-identity-snapshot2" | "target-attribution-v2" | "typescript-semantic-facts-v1" | "unresolved-edge-v1") & (string);
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
    "dynamicDispatch": ("resolved" | "present" | "not-applicable") & (string);
    "entryPointsRecognized": ("all" | "partial" | "none") & (string);
    "exportsClosed": ("closed" | "open" | "unknown") & (string);
    "externalConsumers": ("none-declared" | "possible" | "unknown") & (string);
    "nonliteralLoading": ("none" | "present") & (string);
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
export type Native2DeficiencyV2 = ("language-tier-unsupported" | "provider-unavailable" | "input-closure-incomplete" | "budget-exhausted" | "confidence-floor-unmet" | "derivation-policy-unmet" | "resolution-incomplete" | "external-consumers-unknown" | "required-relation-missing") & (string);
export type Native2ExaminedUniverseV1 = ({
    "subjectCount": (bigint);
    "subjectScopeCommitment": (string);
});
export type Native2NativeCause = ("body-language-owner-ambiguous" | "body-language-owner-unenumerated" | "body-language-ownership-missing" | "capability-missing" | "config-flag-stripped" | "generated-file-missing" | "generated-file-out-of-bounds" | "generated-output-unavailable" | "linker-unavailable" | "lockfile-missing" | "missing-dependency-source" | "no-program-unit" | "node-modules-outside-read-set" | "source-replacement-outside-snapshot") & (string);
export type Native2Relation = ("file" | "package" | "vcs-change" | "declares" | "literal" | "control-flow" | "imports" | "references" | "calls" | "types" | "reachability" | "clones" | "unresolved-edge") & (string);
export type Native2ResolutionCompletenessState = ("complete" | "incomplete" | "partial" | "not-attempted" | "not-applicable") & (string);
export type Native2ResolutionCompletenessV2 = ({
    "attempted": (boolean);
    "examinedExhaustive": (boolean);
    "stageTerminal": (Native2StageTerminal | (null));
    "state": Native2ResolutionCompletenessState;
    "unresolvedEdgeClasses": ((Native2UnresolvedEdgeKindV1)[]);
    "unresolvedEdgeCount": (bigint);
});
export type Native2Rung = ("enumerated" | "manifest-declared" | "vcs-reported" | "syntactic" | "syntactic-specifier" | "resolved-target" | "syntactic-name-match" | "resolved-binding" | "syntactic-callee-name" | "resolved-callee" | "annotated" | "checked" | "from-resolved-calls" | "normalized-body-hash" | "observed") & (string);
export type Native2StageTerminal = ("complete" | "unavailable" | "budget-exhausted" | "provider-fault" | "cancelled" | "crash") & (string);
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
    "configOrigin": ("tsconfig" | "jsconfig" | "synthesized") & (string);
    "executionCapableResolution": (false);
    "jsAdmittedToProgram": (boolean);
    "jsDiagnosticsEnabled": (boolean);
    "jsRootFiles": (((string))[]);
    "languageMode": ("ts-tsconfig" | "js-allowjs" | "js-synthesized") & (string);
    "lockfileKind": ("package-lock" | "pnpm-lock" | "yarn-lock" | "bun-lock" | "none") & (string);
    "nativeContextId": (string);
    "nodeModulesInReadSet": (boolean);
    "packageModuleType": ("module" | "commonjs" | "absent") & (string);
    "programRootFiles": (((string))[]);
    "resolutionCompletenessImplied": (false);
    "schemaVersion": (2n);
    "synthesizedOptions": (Native2SynthesizedCompilerOptionsV1 | (null));
    "synthesizerVersion": ((1n) | (null));
    "tsconfigGraphHash": (string);
});
export type Native2UnresolvedEdgeKindV1 = ("computed-member-access" | "dynamic-import-nonliteral" | "require-nonliteral" | "indirect-eval" | "reflective-access" | "untyped-any-call" | "unresolved-module-specifier" | "external-module-boundary" | "structural-dispatch" | "trait-object-dynamic-dispatch" | "generic-bound-dispatch" | "macro-expansion-unavailable" | "build-script-generated-unavailable" | "cfg-excluded-region" | "ffi-extern" | "entry-point-unrecognized") & (string);
export type Native2ViewEntryV3 = ({
    "closedWorld": Native2ClosedWorldV2;
    "confidenceMillionths": (bigint);
    "coverage": ("complete" | "unknown") & (string);
    "deficiency": (Native2DeficiencyV2 | (null));
    "derivationKinds": ((("annotated" | "jsdoc-declared" | "compiler-inferred") & (string))[]);
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
    "exported": (("exported" | "not-exported" | "unknown") & (string) | (null));
    "kind": ("file" | "symbol" | "package" | "unknown") & (string);
    "logicalPath": (Occupancy1LogicalPath | (null));
    "occupancy": ("first-party" | "external" | "unknown") & (string);
    "packageManifestPath": (Occupancy1LogicalPath | (null));
    "schemaVersion": (1n);
    "targetNativeId": (string);
    "targetUniverseId": (string);
}) & (Json & Json & Json & Json & Json & Json & Json & Json);
export type Startup1DigestHex = (string);
export type Startup1ExecutionIdText = (string);
export type Startup1NfcText = (string);
export type Startup1PlanId2 = (string);
export type Startup1Sha256Text = (string);
export type Startup1SnapshotId2 = (string);
export type Startup1StageIdText = (string);
export type Startup1TypeScriptBudgetExhaustedV2 = ({
    "analysisOrdinal": (0n);
    "coverage": ((Native2CoverageResultV3)[]);
    "coverageCommitment": Startup1Sha256Text;
    "dimension": ("sourceFilesVisited" | "astNodesVisited" | "moduleResolutionQueries" | "typeQueries" | "factsEmitted" | "factBytesEmitted") & (string);
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
    "reason": ("capability-missing" | "identity-version-mismatch" | "node-modules-outside-read-set" | "semantic-universe-incomplete" | "snapshot-resolution-input-missing" | "unsupported-compiler-mode") & (string);
});
export type Startup1TypeScriptUniverseAcceptedV2 = ({
    "executionId": Startup1ExecutionIdText;
    "planId": Startup1PlanId2;
    "snapshotId": Startup1SnapshotId2;
    "universeKey": Startup1Sha256Text;
});
export type Startup1Uint64 = (bigint);
