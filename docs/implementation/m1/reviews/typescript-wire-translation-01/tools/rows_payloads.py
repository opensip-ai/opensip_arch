"""Rows for delivery.v2 wireSchema payloadSchemas, plus new/negotiated members from schema-native owners."""
from rows_common import *  # noqa: F401,F403

G2 = "TS2-G2"
ECHO_S = "^snapshot2:[0-9a-f]{64}$ via exact echo"
ECHO_P = "^plan2:[0-9a-f]{64}$ via exact echo"
TSKEY = "Sha256Text; native semantic-universe identity (typescript v2)"


def hs(rec, m):
    return HS + f"{rec}/properties/{m}"


def st(rec, m):
    return ST + f"{rec}/properties/{m}"


PAYLOADS = {
    # HelloV1 -> TypeScriptHelloV2
    "payloadSchemas.HelloV1.fields.hostBuildId": R(T, "non-empty NFC text", "replaced", A_HELLO, r=hs("TypeScriptHelloV2", "hostBuildId"), m="unchanged", h=[G2]),
    "payloadSchemas.HelloV1.fields.expectedProviderDescriptorSha256": R(T, "DigestHex = raw SHA-256 of RFC 8785 typescript-provider/identity.json", "replaced", A_HELLO, r=hs("TypeScriptHelloV2", "expectedProviderDescriptorSha256"), m="unchanged", h=["d2.identity"]),
    "payloadSchemas.HelloV1.fields.expectedRuntimeDescriptorSha256": R(T, "DigestHex = raw SHA-256 of RFC 8785 typescript-runtime/identity.json", "replaced", A_HELLO, r=hs("TypeScriptHelloV2", "expectedRuntimeDescriptorSha256"), m="unchanged", h=["d2.identity"]),
    "payloadSchemas.HelloV1.fields.limits": R(M, "TypeScriptProtocolLimitsV1: exactly ten uint64 consts (see limits link)", "replaced", A_HELLO, r=hs("TypeScriptHelloV2", "limits"), m="unchanged",
                                              h=["wire.admit_hello: missing/extra/renamed/retyped/changed member refuses before HelloAck"]),
    # HelloAckV1 -> TypeScriptHelloAckV2
    "payloadSchemas.HelloAckV1.fields.protocolMajor": R(U, "exactly 2 (inherited exactly 1); equals provider descriptor protocolMajor", "replaced", A_HELLO, r=hs("TypeScriptHelloAckV2", "protocolMajor"), m="value-changed", h=["wire.admit_hello_ack"]),
    **{f"payloadSchemas.HelloAckV1.fields.{k}": R(T, v, "replaced", A_HELLO, r=hs("TypeScriptHelloAckV2", k), m="unchanged", h=["wire.admit_hello_ack: " + src, G2])
       for k, v, src in [
           ("providerBuildId", "non-empty NFC; verified provider descriptor text", "equals provider descriptor"),
           ("providerDescriptorSha256", "DigestHex", "equals Hello expectedProviderDescriptorSha256"),
           ("runtimeDescriptorSha256", "DigestHex", "equals Hello expectedRuntimeDescriptorSha256"),
           ("nodeVersion", "non-empty NFC; verified runtime descriptor text", "equals runtime descriptor"),
           ("v8Version", "non-empty NFC; verified runtime descriptor text", "equals runtime descriptor"),
           ("modulesAbi", "non-empty NFC; verified runtime descriptor text", "equals runtime descriptor"),
           ("typescriptVersion", "non-empty NFC; verified provider descriptor text", "equals provider descriptor"),
           ("typescriptCompilerSha256", "DigestHex", "equals provider descriptor"),
           ("typescriptStdlibMerkleRoot", "DigestHex", "equals provider descriptor"),
           ("defaultWorkBudgetProfileId", "const typescript-provider-default-work-budget-v1", "equals provider descriptor"),
           ("defaultWorkBudgetProfileSha256", "const bf7305a12d26a1938b615c861f995d66eac494915e6140c4942a2ea6f0846da6", "equals provider descriptor"),
           ("platformId", "non-empty NFC; selected release platformId", "equals runtime descriptor"),
       ]},
    "payloadSchemas.HelloAckV1.fields.capabilities": R(A, "TypeScriptCapabilitiesV2: 4..11 unique TypeScriptCapabilityToken, strictly ascending UTF-8, four identity tokens present (inherited fixed 3-token array)", "replaced", A_HELLO,
                                                       r=hs("TypeScriptHelloAckV2", "capabilities"), m="value-changed", h=["wire.admit_hello_ack: exact echo of Hello expectedCapabilities (order is not JSON-Schema checkable)"]),
    # OpenUniverseV1 -> TypeScriptOpenUniverseV2
    "payloadSchemas.OpenUniverseV1.fields.executionId": R(T, "ExecutionIdText", "replaced", A_START + "; " + A_RET_ID, r=st("TypeScriptOpenUniverseV2", "executionId"), m="unchanged", g=["TS2-G11"]),
    "payloadSchemas.OpenUniverseV1.fields.snapshotId": R(T, "SnapshotId2", "replaced", A_START, r=st("TypeScriptOpenUniverseV2", "snapshotId"), m="value-changed"),
    "payloadSchemas.OpenUniverseV1.fields.planId": R(T, "PlanId2", "replaced", A_START, r=st("TypeScriptOpenUniverseV2", "planId"), m="value-changed"),
    "payloadSchemas.OpenUniverseV1.fields.planIntentCommitment": R(T, "Sha256Text", "replaced", A_START + "; " + A_RET_ID, r=st("TypeScriptOpenUniverseV2", "planIntentCommitment"), m="unchanged"),
    "payloadSchemas.OpenUniverseV1.fields.providerId": R(T, "const typescript-semantic", "replaced", A_START, r=st("TypeScriptOpenUniverseV2", "providerId"), m="unchanged"),
    "payloadSchemas.OpenUniverseV1.fields.universe": R(M, "TypeScriptSemanticUniverseV2", "replaced", A_START, r=st("TypeScriptOpenUniverseV2", "universe"), m="value-changed", h=["start.admit_open_universe: handshakeJoin (11 members); admitted only when identityNegotiated"]),
    "payloadSchemas.OpenUniverseV1.fields.universeKey": R(T, TSKEY, "replaced", A_START + "; " + A_UNIV, r=st("TypeScriptOpenUniverseV2", "universeKey"), m="value-changed", h=["host recomputes"]),
    # UniverseAcceptedV1 -> TypeScriptUniverseAcceptedV2
    "payloadSchemas.UniverseAcceptedV1.fields.executionId": R(T, "exact OpenUniverse echo", "replaced", A_START, r=st("TypeScriptUniverseAcceptedV2", "executionId"), m="unchanged", h=["start.admit_universe_accepted"]),
    "payloadSchemas.UniverseAcceptedV1.fields.snapshotId": R(T, "SnapshotId2 echo", "replaced", A_START, r=st("TypeScriptUniverseAcceptedV2", "snapshotId"), m="value-changed", h=["start.admit_universe_accepted"]),
    "payloadSchemas.UniverseAcceptedV1.fields.planId": R(T, "PlanId2 echo", "replaced", A_START, r=st("TypeScriptUniverseAcceptedV2", "planId"), m="value-changed", h=["start.admit_universe_accepted"]),
    "payloadSchemas.UniverseAcceptedV1.fields.universeKey": R(T, TSKEY + "; worker recomputation equal to OpenUniverse", "replaced", A_START, r=st("TypeScriptUniverseAcceptedV2", "universeKey"), m="value-changed", h=["start.admit_universe_accepted"]),
    # SnapshotManifestV1
    "payloadSchemas.SnapshotManifestV1.fields.snapshotId": R(T, ECHO_S + " of OpenUniverse", "value-substituted", A_ECHO, r=ST + "SnapshotId2", x="startup identityMembers lists SnapshotManifest snapshotId"),
    "payloadSchemas.SnapshotManifestV1.fields.manifestSha256": R(T, "DigestHex over deterministic-CBOR entries (form disputed)", "retained", A_INHERIT, h=["worker recomputes"], g=["TS2-G10"]),
    "payloadSchemas.SnapshotManifestV1.fields.entries": R(A, "items SnapshotEntryV1 map; sorted unique by path UTF-8; <= maxSnapshotEntries 200000", "retained", A_INHERIT, h=["d2.limitRule", "d2.snapshotTransport"]),
    # SnapshotFileChunkV1
    "payloadSchemas.SnapshotFileChunkV1.fields.snapshotId": R(T, ECHO_S + " of manifest", "value-substituted", A_ECHO, r=ST + "SnapshotId2",
                                                              x="'exact manifest SnapshotId' -> manifest echoes OpenUniverse; transitive (startup identityMembers does not enumerate chunk explicitly)"),
    "payloadSchemas.SnapshotFileChunkV1.fields.path": R(T, "one kind=file manifest path", "retained", A_INHERIT, x="exact echo of SnapshotEntryV1.path", g=["TS2-G11"]),
    "payloadSchemas.SnapshotFileChunkV1.fields.chunkIndex": R(U, "contiguous from 0 per path", "retained", A_INHERIT, h=["d2.snapshotTransport"]),
    "payloadSchemas.SnapshotFileChunkV1.fields.byteOffset": R(U, "exact cumulative prior chunk bytes", "retained", A_INHERIT, h=["checked uint64 add"]),
    "payloadSchemas.SnapshotFileChunkV1.fields.bytes": R(B, "non-empty; length <= maxSnapshotChunkBytes 1048576", "retained", A_INHERIT, h=["d2.limitRule", "digest vs manifest contentSha256"], g=["TS2-G1"]),
    # SnapshotSealV1
    "payloadSchemas.SnapshotSealV1.fields.snapshotId": R(T, ECHO_S + " of manifest", "value-substituted", A_ECHO, r=ST + "SnapshotId2", x="startup identityMembers lists SnapshotSeal snapshotId"),
    "payloadSchemas.SnapshotSealV1.fields.manifestSha256": R(T, "exact manifestSha256 echo", "retained", A_INHERIT, g=["TS2-G10"]),
    "payloadSchemas.SnapshotSealV1.fields.entryCount": R(U, "exact entries length (<= 200000)", "retained", A_INHERIT),
    "payloadSchemas.SnapshotSealV1.fields.totalFileBytes": R(U, "exact sum of file byteLength", "retained", A_INHERIT, h=["checked uint64 add"]),
    "payloadSchemas.SnapshotSealV1.fields.totalChunkCount": R(U, "exact emitted chunk count", "retained", A_INHERIT),
    # SnapshotAcceptedV1
    "payloadSchemas.SnapshotAcceptedV1.fields.snapshotId": R(T, ECHO_S + " of SnapshotSeal", "value-substituted", A_ECHO, r=ST + "SnapshotId2", x="startup identityMembers lists SnapshotAccepted snapshotId"),
    "payloadSchemas.SnapshotAcceptedV1.fields.manifestSha256": R(T, "worker-recomputed exact value", "retained", A_INHERIT, g=["TS2-G10"]),
    "payloadSchemas.SnapshotAcceptedV1.fields.entryCount": R(U, "worker-observed exact", "retained", A_INHERIT),
    "payloadSchemas.SnapshotAcceptedV1.fields.totalFileBytes": R(U, "worker-observed exact", "retained", A_INHERIT),
    "payloadSchemas.SnapshotAcceptedV1.fields.totalChunkCount": R(U, "worker-observed exact", "retained", A_INHERIT),
    # AnalyzeV1
    "payloadSchemas.AnalyzeV1.fields.analysisOrdinal": R(U, "exactly 0 (one Analyze per worker)", "retained", A_INHERIT),
    "payloadSchemas.AnalyzeV1.fields.executionId": R(T, "exact OpenUniverse echo", "retained", A_RET_ID),
    "payloadSchemas.AnalyzeV1.fields.snapshotId": R(T, ECHO_S + " of OpenUniverse", "value-substituted", A_ECHO, r=ST + "SnapshotId2"),
    "payloadSchemas.AnalyzeV1.fields.planId": R(T, ECHO_P + " of OpenUniverse", "value-substituted", A_ECHO, r=ST + "PlanId2"),
    "payloadSchemas.AnalyzeV1.fields.universeKey": R(T, TSKEY + " echo", "value-substituted", A_START + "; " + A_UNIV, r=ST + "Sha256Text"),
    "payloadSchemas.AnalyzeV1.fields.stageRequests": R(A, "items StageRequestV1 map; non-empty; <= maxAnalyzeStages 1024; all and only selected stages in verified logical order (may be a Plan subset)", "retained", A_INHERIT,
                                                       h=["d2.multiStageAnalyze.selection/batchability/ordering", "dispatch"]),
    # FactBatchV1 (historical; token absent)
    "payloadSchemas.FactBatchV1.fields.analysisOrdinal": R(U, "exactly 0", "retained", A_FB, r=hs("TypeScriptFactBatchV1Vector", "analysisOrdinal"), h=["dispatch: == expectedAnalysisOrdinal"]),
    "payloadSchemas.FactBatchV1.fields.stageId": R(T, "C-2 stageId TEXT echo of current StageRequestV1.stageId; StageIdText 1..255", "retained", A_FB, r=hs("TypeScriptFactBatchV1Vector", "stageId"),
                                                   h=["dispatch: == expectedStageId; not stageOrdinal; not execution-plan ordinal"]),
    "payloadSchemas.FactBatchV1.fields.batchIndex": R(U, "contiguous from 0 per stage", "retained", A_FB, r=hs("TypeScriptFactBatchV1Vector", "batchIndex"), h=["dispatch: == expectedBatchIndex"]),
    "payloadSchemas.FactBatchV1.fields.facts": R(A, "items FactCandidateV1 map; non-empty; ordered; <= maxFactBatchFacts 4096", "retained", A_FB, r=hs("TypeScriptFactBatchV1Vector", "facts"),
                                                 x="vector items ref fact-batch.3 JSON-vector candidate (hex transcription; see TS2-G1)", h=["wire.admit_fact_batch"]),
    "payloadSchemas.FactBatchV1.fields.batchCommitment": R(T, "Sha256Text; domain opensip.ts-provider.fact-batch.v1 over deterministic-CBOR(facts)", "retained", A_FB, r=hs("TypeScriptFactBatchV1Vector", "batchCommitment"),
                                                           h=["wire.admit_fact_batch: recompute", "d2.commitments.domains.factBatch (FactBatchV1 only)"]),
    # CoverageV1 -> TypeScriptCoverageV2
    "payloadSchemas.CoverageV1.fields.analysisOrdinal": R(U, "exactly 0", "replaced", A_COV, r=st("TypeScriptCoverageV2", "analysisOrdinal"), m="unchanged"),
    "payloadSchemas.CoverageV1.fields.stageId": R(T, "StageIdText; current requested stage; attributes every entry", "replaced", A_COV, r=st("TypeScriptCoverageV2", "stageId"), m="unchanged"),
    "payloadSchemas.CoverageV1.fields.entries": R(A, "items CoverageResultV3; 1..4096; entries[i] answers requestedCoverageDomain.keys[i]; count == key count", "replaced", A_COV, r=st("TypeScriptCoverageV2", "entries"), m="value-changed",
                                                  h=["start.admit_coverage_frame", "ne.admit_coverage_result_v3"]),
    "payloadSchemas.CoverageV1.fields.coverageCommitment": R(T, "Sha256Text over ordered CoverageResultV3 entries; recipe unchanged", "replaced", A_COV, r=st("TypeScriptCoverageV2", "coverageCommitment"), m="value-changed", g=["TS2-G12"]),
    # UnavailableV1 -> TypeScriptUnavailableV2 (post-Analyze); PreAnalyzeUnavailableV1 is a separate new record
    "payloadSchemas.UnavailableV1.fields.analysisOrdinal": R(U, "exactly 0", "replaced", A_COV, r=st("TypeScriptUnavailableV2", "analysisOrdinal"), m="unchanged"),
    "payloadSchemas.UnavailableV1.fields.affectedStageIds": R(A, "items StageIdText; all requested stageIds in request order; schema minItems 1, no maxItems (derived <= 1024)", "replaced", A_COV, r=st("TypeScriptUnavailableV2", "affectedStageIds"), m="unchanged", g=["TS2-G8"]),
    "payloadSchemas.UnavailableV1.fields.reason": R(T, "enum capability-missing|identity-version-mismatch|node-modules-outside-read-set|semantic-universe-incomplete|snapshot-resolution-input-missing|unsupported-compiler-mode (never native-context-mismatch)", "replaced", A_COV + "; §9.4", r=st("TypeScriptUnavailableV2", "reason"), m="value-changed"),
    "payloadSchemas.UnavailableV1.fields.coverage": R(A, "items CoverageResultV3 in stage-major/key order, unknown/provider-unavailable; schema minItems 0 no max (derived >= 1, <= 131072)", "replaced", A_COV, r=st("TypeScriptUnavailableV2", "coverage"), m="value-changed", h=["cumulative key-range attribution"], g=["TS2-G8"]),
    "payloadSchemas.UnavailableV1.fields.coverageCommitment": R(T, "Sha256Text over CoverageResultV3 coverage", "replaced", A_COV, r=st("TypeScriptUnavailableV2", "coverageCommitment"), m="value-changed", g=["TS2-G12"]),
    # BudgetExhaustedV1 -> TypeScriptBudgetExhaustedV2
    "payloadSchemas.BudgetExhaustedV1.fields.analysisOrdinal": R(U, "exactly 0", "replaced", A_COV, r=st("TypeScriptBudgetExhaustedV2", "analysisOrdinal"), m="unchanged"),
    "payloadSchemas.BudgetExhaustedV1.fields.triggerStageId": R(T, "StageIdText; one requested stageId", "replaced", A_COV, r=st("TypeScriptBudgetExhaustedV2", "triggerStageId"), m="unchanged"),
    "payloadSchemas.BudgetExhaustedV1.fields.dimension": R(T, "enum sourceFilesVisited|astNodesVisited|moduleResolutionQueries|typeQueries|factsEmitted|factBytesEmitted", "replaced", A_COV, r=st("TypeScriptBudgetExhaustedV2", "dimension"), m="unchanged"),
    "payloadSchemas.BudgetExhaustedV1.fields.limit": R(U, "exact requested budget", "replaced", A_COV, r=st("TypeScriptBudgetExhaustedV2", "limit"), m="unchanged"),
    "payloadSchemas.BudgetExhaustedV1.fields.observed": R(U, "exactly limit+1", "replaced", A_COV, r=st("TypeScriptBudgetExhaustedV2", "observed"), m="unchanged", h=["observed == limit+1 (checked)"]),
    "payloadSchemas.BudgetExhaustedV1.fields.coverage": R(A, "items CoverageResultV3, unknown/budget-exhausted, stage-major/key order; schema no maxItems", "replaced", A_COV, r=st("TypeScriptBudgetExhaustedV2", "coverage"), m="value-changed", g=["TS2-G8"]),
    "payloadSchemas.BudgetExhaustedV1.fields.coverageCommitment": R(T, "Sha256Text over CoverageResultV3 coverage", "replaced", A_COV, r=st("TypeScriptBudgetExhaustedV2", "coverageCommitment"), m="value-changed", g=["TS2-G12"]),
    # CompleteV1
    "payloadSchemas.CompleteV1.fields.analysisOrdinal": R(U, "exactly 0", "retained", A_INHERIT),
    "payloadSchemas.CompleteV1.fields.stageResults": R(A, "items StageResultV1 map; exactly one per requested stage in request order (<= 1024)", "retained", A_INHERIT, h=["d2.multiStageAnalyze.completeness"]),
    "payloadSchemas.CompleteV1.fields.factStreamCommitment": R(T, "Sha256Text; domain factStream over all ordered FactCandidateV1 (V1 or V3 carried)", "retained", A_FB, x="provider-handshake x-opensip-wire-law/commitments/typescript-semantic", h=["d2.commitments"]),
    "payloadSchemas.CompleteV1.fields.coverageStreamCommitment": R(T, "Sha256Text over all ordered CoverageResultV3 values", "value-substituted", A_COV, h=["d2.commitments"], g=["TS2-G12"]),
    # CancelV1 / CancelledV1
    "payloadSchemas.CancelV1.fields.executionId": R(T + "|" + N, "OpenUniverse ExecutionId if opened, else null", "retained", A_RET_ID, x="startup identityMembers: Cancel executionId exact echo (ExecutionId itself retained)"),
    "payloadSchemas.CancelV1.fields.analysisOrdinal": R(U + "|" + N, "0 after Analyze, else null", "retained", A_INHERIT),
    "payloadSchemas.CancelV1.fields.reason": R(T, "enum user-interrupt|host-shutdown", "retained", A_INHERIT, h=["d2.ordering.cancelTransition"]),
    "payloadSchemas.CancelledV1.fields.executionId": R(T + "|" + N, "exact Cancel value", "retained", A_RET_ID),
    "payloadSchemas.CancelledV1.fields.analysisOrdinal": R(U + "|" + N, "exact Cancel value", "retained", A_INHERIT),
    "payloadSchemas.CancelledV1.fields.observedPhase": R(T, "enum handshake|universe|snapshot|analysis (unchanged); snapshot for Cancel in WAIT_NATIVE_CONTEXT_VERIFIED/READY_ANALYZE", "retained", A_ORDER,
                                                         h=["start.typescript_protocol2_run cancellationObservedPhase"]),
}

# New members (schema-native owners). Key: (record, member). Source selector = the ref.
NEW = {
    ("TypeScriptHelloV2", "expectedCapabilities"): R(A, "TypeScriptCapabilitiesV2: 4..11 unique tokens, strictly ascending UTF-8, contains 4 identity tokens; optional target-attribution-v2", "new", A_HELLO + "; §9.1", r=hs("TypeScriptHelloV2", "expectedCapabilities"), h=["wire.admit_hello: equals signed capability row"]),
    ("TypeScriptHelloV2", "identityVersions"): R(M, "IdentityVersionsV1 {snapshot:2, plan:2, fact:2, coverage:3}", "new", A_HELLO + "; §9.1", r=hs("TypeScriptHelloV2", "identityVersions")),
    ("TypeScriptHelloAckV2", "identityVersions"): R(M, "IdentityVersionsV1; exact echo of Hello", "new", A_HELLO + "; §9.1", r=hs("TypeScriptHelloAckV2", "identityVersions"), h=["wire.admit_hello_ack: exact echo"]),
    ("NativeContextVerifiedV1", "nativeContextId"): R(T, "Sha256Text; == OpenUniverse.universe.resolvedInputs.nativeContextId", "new", A_FRAMES + "; §9.2", r=st("NativeContextVerifiedV1", "nativeContextId"), h=["start.admit_native_context_verified"]),
    ("NativeContextVerifiedV1", "recomputedNativeContextId"): R(T, "Sha256Text; worker recomputation, equal", "new", A_FRAMES + "; §9.5", r=st("NativeContextVerifiedV1", "recomputedNativeContextId"), h=["start.admit_native_context_verified"]),
    ("NativeContextVerifiedV1", "equal"): R(BOOL, "const true", "new", A_FRAMES, r=st("NativeContextVerifiedV1", "equal")),
    ("PreAnalyzeUnavailableV1", "executionId"): R(T, "ExecutionIdText == OpenUniverse", "new", A_ORDER, r=st("PreAnalyzeUnavailableV1", "executionId"), h=["start.admit_unavailable"]),
    ("PreAnalyzeUnavailableV1", "snapshotId"): R(T, "SnapshotId2 == OpenUniverse", "new", A_ORDER, r=st("PreAnalyzeUnavailableV1", "snapshotId"), h=["start.admit_unavailable"]),
    ("PreAnalyzeUnavailableV1", "planId"): R(T, "PlanId2 == OpenUniverse", "new", A_ORDER, r=st("PreAnalyzeUnavailableV1", "planId"), h=["start.admit_unavailable"]),
    ("PreAnalyzeUnavailableV1", "reason"): R(T, "const native-context-mismatch", "new", A_ORDER, r=st("PreAnalyzeUnavailableV1", "reason")),
    ("PreAnalyzeUnavailableV1", "nativeContextId"): R(T, "Sha256Text == universe.resolvedInputs.nativeContextId", "new", A_ORDER, r=st("PreAnalyzeUnavailableV1", "nativeContextId"), h=["start.admit_unavailable"]),
    ("PreAnalyzeUnavailableV1", "recomputedNativeContextId"): R(T, "Sha256Text; differs from nativeContextId", "new", A_ORDER, r=st("PreAnalyzeUnavailableV1", "recomputedNativeContextId"),
                                                                 h=["start.admit_unavailable", "ne.pre_analyze_unavailable_conversion: host mints coverage after DONE"]),
    ("FactBatchV3", "schemaVersion"): R(U, "const 3 (payload discriminator; not FactCandidateV1.schemaVersion)", "new", A_FB, r=FB + "/properties/schemaVersion"),
    ("FactBatchV3", "analysisOrdinal"): R(U, "uint64 echo of AnalyzeV1.analysisOrdinal (TS: 0)", "new", A_FB, r=FB + "/properties/analysisOrdinal", x="schema allows any uint64; TS value 0 derived from AnalyzeV1", h=["dispatch: == expectedAnalysisOrdinal"]),
    ("FactBatchV3", "stageId"): R(T, "C-2 stageId TEXT 1..255 echo of StageRequestV1.stageId", "new", A_FB, r=FB + "/properties/stageId", h=["dispatch: == expectedStageId"]),
    ("FactBatchV3", "batchIndex"): R(U, "contiguous from 0 per stage", "new", A_FB, r=FB + "/properties/batchIndex", h=["dispatch: == expectedBatchIndex"]),
    ("FactBatchV3", "candidates"): R(A, "items FactCandidateV1 (wire bstr payload); 1..4096 (maxFactBatchFacts); member name candidates, not facts", "new", A_FB, r=FB + "/properties/candidates", g=["TS2-G1"], h=["wire.admit_fact_batch"]),
    ("FactBatchV3", "occupancyCompanions"): R(A, "items OccupancyCompanionV1 (10 required members, allOf branches); 0..len(candidates); strictly increasing candidateOrdinal naming this batch", "new", A_FB + "; §9.6", r=FB + "/properties/occupancyCompanions",
                                               h=["candidateOrdinal association (PROVIDER_RETURN_UNKNOWN_CANDIDATE)", "targetUniverseId byte-equal to candidate"]),
}
