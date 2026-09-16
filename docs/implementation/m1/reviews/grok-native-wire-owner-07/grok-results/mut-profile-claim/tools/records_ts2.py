"""typescript-semantic protocol major 2 wire carriers (namespace Ts2)."""
from common import (U, T, B, BOOL, NULL, A, REF, EXT, NULLABLE, M, REC, VREC, ALIAS, SRC, HS, ST, NE, OC)

D2 = "$.typescriptSemanticSubstrate.providerProtocol.wireSchema."

SCALARS = {
    "Ts2DigestHex": {"type": T(pattern="^[0-9a-f]{64}(?![\\s\\S])"), "sameShapeAs": HS + "#/$defs/DigestHex",
                     "source": SRC("delivery2", D2 + "definitions.DigestHex")},
    "Ts2Sha256Text": {"type": T(pattern="^sha256:[0-9a-f]{64}(?![\\s\\S])"), "sameShapeAs": HS + "#/$defs/Sha256Text",
                      "source": SRC("delivery2", D2 + "definitions.Sha256Text")},
    "Ts2NfcText": {"type": T(min_scalars=1), "sameShapeAs": HS + "#/$defs/NfcText",
                   "source": SRC("handshake", "#/$defs/NfcText")},
    "Ts2StageIdText": {"type": T(min_scalars=1, max_scalars=255), "sameShapeAs": ST + "#/$defs/StageIdText",
                       "source": SRC("dispatch", "#/properties/expectedStageId")},
    "Ts2SnapshotId2": {"type": T(pattern="^snapshot2:[0-9a-f]{64}(?![\\s\\S])"), "sameShapeAs": ST + "#/$defs/SnapshotId2",
                       "source": SRC("startup", "#/$defs/SnapshotId2")},
    "Ts2PlanId2": {"type": T(pattern="^plan2:[0-9a-f]{64}(?![\\s\\S])"), "sameShapeAs": ST + "#/$defs/PlanId2",
                   "source": SRC("startup", "#/$defs/PlanId2")},
    "Ts2ExecutionIdText": {"type": T(pattern="^exec1_[0-9a-f]{32}(?![\\s\\S])"),
                           "source": SRC("identityMd", "lines 63-72 (exec1_ + 32 lowercase hex, end-anchored)"),
                           "note": "Startup1ExecutionIdText is minLength 1 only; the exact AttemptRecord value always has this grammar, so a narrower carrier refuses nothing the host constructs."},
    "Ts2ProjectPath": {"type": T(min_scalars=1, max_scalars=4096, lexical="logical-path-segments"),
                       "source": SRC("identitySchemas3", "#/$defs/LogicalPath (host constructs manifest paths from the snapshot2 source inventory)"),
                       "note": "Normative lexical admission logical-path-segments (identity-schemas.v3 LogicalPath declarative grammar: split on /, every segment 1..255 scalars, not . or .., no U+0000 or backslash). 4096 scalars is the identity LogicalPath bound; no pattern is carried."},
}

SNAP = REF("Ts2SnapshotId2")
DIG = REF("Ts2DigestHex")
SHA = REF("Ts2Sha256Text")
STAGE = REF("Ts2StageIdText")
EXEC = REF("Ts2ExecutionIdText")

ANCHOR_MEMBERS = ["kind", "snapshotId", "path", "contentSha256", "startByte", "endByte", "factId"]

RECORDS = {
    "Ts2FrameV2": REC([
        M("protocolMajor", U(const=2)),
        M("frameType", T(enum=["Hello", "OpenUniverse", "SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal", "Analyze",
                               "Cancel", "HelloAck", "UniverseAccepted", "SnapshotAccepted", "NativeContextVerified",
                               "FactBatch", "Coverage", "Unavailable", "BudgetExhausted", "Complete", "Cancelled"])),
        M("sequence", U()),
        M("payload", {"t": "frame-payload", "protocol": "typescript-semantic"}),
    ], SRC("delivery2", D2 + "frameEnvelope"), ["TS2-ENV-MAJOR", "TS2-ENV-DIRECTION-BY-FRAME", "TS2-ENV-SEQUENCE", "FRAME-LIMIT"],
        "Private name. The wire carries no record name; payload is a nested CBOR map selected by frameType and host state."),
    "Ts2SnapshotEntryV1": VREC("kind", ["path", "kind", "byteLength", "contentSha256", "linkTarget"], {
        "file": {"path": REF("Ts2ProjectPath"), "byteLength": U(), "contentSha256": DIG, "linkTarget": NULL},
        "symlink": {"path": REF("Ts2ProjectPath"), "byteLength": U(const=0), "contentSha256": NULL,
                    "linkTarget": T(min_scalars=1)},
    }, SRC("delivery2", D2 + "definitions.SnapshotEntryV1"), ["TS2-SNAPSHOT-ORDER", "TS2-LOGICAL-PATH-ADMISSION"]),
    "Ts2SnapshotManifestV1": REC([
        M("snapshotId", SNAP), M("manifestSha256", DIG),
        M("entries", A(REF("Ts2SnapshotEntryV1"), 0, 200000, "path-utf8-strict")),
    ], SRC("delivery2", D2 + "payloadSchemas.SnapshotManifestV1"), ["ECHO-SNAPSHOT2", "TS2-MANIFEST-DIGEST"]),
    "Ts2SnapshotFileChunkV1": REC([
        M("snapshotId", SNAP), M("path", REF("Ts2ProjectPath")), M("chunkIndex", U()), M("byteOffset", U()),
        M("bytes", B(1, 1048576)),
    ], SRC("delivery2", D2 + "payloadSchemas.SnapshotFileChunkV1"), ["ECHO-SNAPSHOT2", "CHUNK-CUSTODY", "TS2-LOGICAL-PATH-ADMISSION"]),
    "Ts2SnapshotSealV1": REC([
        M("snapshotId", SNAP), M("manifestSha256", DIG), M("entryCount", U(max=200000)), M("totalFileBytes", U()),
        M("totalChunkCount", U()),
    ], SRC("delivery2", D2 + "payloadSchemas.SnapshotSealV1"), ["ECHO-SNAPSHOT2", "SEAL-AGGREGATES"]),
    "Ts2SnapshotAcceptedV1": REC([
        M("snapshotId", SNAP), M("manifestSha256", DIG), M("entryCount", U(max=200000)), M("totalFileBytes", U()),
        M("totalChunkCount", U()),
    ], SRC("delivery2", D2 + "payloadSchemas.SnapshotAcceptedV1"), ["ACCEPTED-EQUALS-SEAL"]),
    "Ts2ProviderWorkBudgetV1": REC([M(n, U()) for n in
                                    ["sourceFilesVisited", "astNodesVisited", "moduleResolutionQueries", "typeQueries",
                                     "factsEmitted", "factBytesEmitted"]],
                                   SRC("delivery2", D2 + "definitions.ProviderWorkBudgetV1"), ["TS2-BUDGET-PROJECTION"],
                                   "Inherited shape is any uint64; the host projection emits 1..2^63-1 only (handwritten TS2-BUDGET-PROJECTION)."),
    "Ts2SubjectScopeV1": REC([
        M("scopeKind", T(const="all-snapshot-files")), M("snapshotId", SNAP), M("subjectCount", U(max=200000)),
        M("subjectScopeCommitment", SHA),
    ], SRC("delivery2", D2 + "definitions.SubjectScopeV1"), ["ECHO-SNAPSHOT2", "TS2-SUBJECT-SCOPE-RETAINED"]),
    "Ts2CoverageKeyV1": REC([
        M("relation", EXT(NE, "#/$defs/Relation")), M("resolution", EXT(NE, "#/$defs/Rung")),
        M("sourceUniverseId", SHA), M("targetUniverseId", SHA), M("subjectScopeCommitment", SHA),
        M("producer", T(const="typescript-semantic")), M("producerVersion", REF("Ts2NfcText")), M("schemaVersion", U(const=1)),
    ], SRC("delivery2", D2 + "definitions.CoverageKeyV1"), ["UNIVERSE-NATIVE-IDENTITY", "PER-KEY-SCOPE2"]),
    "Ts2RequestedCoverageDomainV1": REC([
        M("subjectScope", REF("Ts2SubjectScopeV1")),
        M("keys", A(REF("Ts2CoverageKeyV1"), 1, 128, "cbor-bytes-strict")),
        M("domainCommitment", SHA),
    ], SRC("delivery2", D2 + "definitions.RequestedCoverageDomainV1"), ["TS2-DOMAIN-COMMITMENT", "PER-KEY-SCOPE2"]),
    "Ts2StageRequestV1": REC([
        M("stageId", STAGE), M("stageOrdinal", U(max=1023)), M("operator", T(const="semantic-provider")),
        M("providerId", T(const="typescript-semantic")),
        M("dependsOn", A(STAGE, 0, None, "utf8-strict")),
        M("relations", A(EXT(NE, "#/$defs/Relation"), 1, 64, "sequence")),
        M("budget", REF("Ts2ProviderWorkBudgetV1")),
        M("requestedCoverageDomain", REF("Ts2RequestedCoverageDomainV1")),
    ], SRC("delivery2", D2 + "definitions.StageRequestV1"), ["DISPATCH-STAGE-CORRELATION", "TS2-STAGE-PROJECTION"],
        "relations keep the C-2 array exactly (already canonical); stageOrdinal is contiguous in this Analyze."),
    "Ts2AnchorRefV1": VREC("kind", ANCHOR_MEMBERS, {
        "source-span": {"snapshotId": SNAP, "path": REF("Ts2ProjectPath"), "contentSha256": DIG,
                        "startByte": U(), "endByte": U(), "factId": NULL},
        "fact-ref": {"snapshotId": NULL, "path": NULL, "contentSha256": NULL, "startByte": NULL, "endByte": NULL,
                     "factId": T(min_scalars=1, max_scalars=4096)},
    }, SRC("delivery2", D2 + "definitions.AnchorRefV1"), ["ANCHOR-WIRE-SPAN", "ANCHOR-FACT-REF-REFUSED", "ECHO-SNAPSHOT2", "TS2-LOGICAL-PATH-ADMISSION"],
        "fact-ref stays shape-decodable only so that admission can refuse it with one typed PROVIDER.PROTOCOL_VIOLATION; it never reaches fact2 minting."),
    "Ts2FactCandidateV1": REC([
        M("candidateOrdinal", U()), M("relation", EXT(NE, "#/$defs/Relation")), M("resolution", EXT(NE, "#/$defs/Rung")),
        M("layer", T(enum=["derived", "inventory", "semantic", "syntax"])),
        M("producer", T(const="typescript-semantic")), M("producerVersion", REF("Ts2NfcText")),
        M("schemaVersion", U()), M("language", T(const="typescript")),
        M("sourceUniverseId", SHA), M("targetUniverseId", SHA), M("confidenceMillionths", U(max=1000000)),
        M("relationSchemaId", T(min_scalars=1, max_scalars=4096)),
        M("canonicalRelationPayload", B(1, 1048576)),
        M("anchors", A(REF("Ts2AnchorRefV1"), 1, 100000, "cbor-bytes-strict")),
    ], SRC("delivery2", D2 + "definitions.FactCandidateV1"), ["FP-CANDIDATE", "UNIVERSE-NATIVE-IDENTITY", "RELATION-PAYLOAD-CBOR"]),
    "Ts2FactBatchV1": REC([
        M("analysisOrdinal", U(const=0)), M("stageId", STAGE), M("batchIndex", U()),
        M("facts", A(REF("Ts2FactCandidateV1"), 1, 4096, "candidateOrdinal-contiguous")),
        M("batchCommitment", SHA),
    ], SRC("delivery2", D2 + "payloadSchemas.FactBatchV1"), ["DISPATCH-STAGE-CORRELATION", "COMMIT-TS2-FACT-BATCH"]),
    "Ts2FactBatchV3": REC([
        M("schemaVersion", U(const=3)), M("analysisOrdinal", U(const=0)), M("stageId", STAGE), M("batchIndex", U()),
        M("candidates", A(REF("Ts2FactCandidateV1"), 1, 4096, "candidateOrdinal-contiguous")),
        M("occupancyCompanions", A(EXT(OC, "#"), 0, 4096, "candidateOrdinal-increasing")),
    ], SRC("factBatch3", "#"), ["DISPATCH-STAGE-CORRELATION", "OCCUPANCY-JOIN"],
        "Wire form of opensip.product.fact-batch.3 for typescript-semantic: candidates carry the CBOR byte string, never the vector hex/decoded pair."),
    "Ts2AnalyzeV1": REC([
        M("analysisOrdinal", U(const=0)), M("executionId", EXEC), M("snapshotId", SNAP), M("planId", REF("Ts2PlanId2")),
        M("universeKey", SHA), M("stageRequests", A(REF("Ts2StageRequestV1"), 1, 1024, "sequence")),
    ], SRC("delivery2", D2 + "payloadSchemas.AnalyzeV1"), ["ECHO-OPEN-UNIVERSE", "TS2-STAGE-PROJECTION"]),
    "Ts2StageResultV1": REC([
        M("stageId", STAGE), M("stageOrdinal", U(max=1023)), M("factBatchCount", U()), M("factCount", U()),
        M("coverageEntryCount", U()), M("factCommitment", SHA), M("coverageCommitment", SHA),
    ], SRC("delivery2", D2 + "definitions.StageResultV1"), ["COMMIT-MAP"]),
    "Ts2CompleteV1": REC([
        M("analysisOrdinal", U(const=0)), M("stageResults", A(REF("Ts2StageResultV1"), 1, 1024, "request-order")),
        M("factStreamCommitment", SHA), M("coverageStreamCommitment", SHA),
    ], SRC("delivery2", D2 + "payloadSchemas.CompleteV1"), ["COMMIT-MAP"]),
    "Ts2CancelV1": REC([
        M("executionId", NULLABLE(EXEC)), M("analysisOrdinal", NULLABLE(U(const=0))),
        M("reason", T(enum=["user-interrupt", "host-shutdown"])),
    ], SRC("delivery2", D2 + "payloadSchemas.CancelV1"), ["CANCEL-NULLABILITY"]),
    "Ts2CancelledV1": REC([
        M("executionId", NULLABLE(EXEC)), M("analysisOrdinal", NULLABLE(U(const=0))),
        M("observedPhase", T(enum=["handshake", "universe", "snapshot", "analysis"])),
    ], SRC("delivery2", D2 + "payloadSchemas.CancelledV1"), ["CANCELLED-ECHO", "TS2-OBSERVED-PHASE"]),
    "Ts2SnapshotFileSubjectV1": REC([
        M("path", REF("Ts2ProjectPath")), M("contentSha256", DIG), M("byteLength", U()),
    ], SRC("delivery2", D2 + "definitions.SnapshotFileSubjectV1"), ["TS2-SUBJECT-SCOPE-RETAINED", "TS2-LOGICAL-PATH-ADMISSION"],
        "Commitment preimage record only; never a frame payload member."),
}
PREIMAGE_ONLY = {"Ts2SnapshotFileSubjectV1"}

FRAMES = [
    # name, direction, workerTerminal, payload selection
    ("Hello", "host-to-worker", False, EXT(HS, "#/$defs/TypeScriptHelloV2")),
    ("OpenUniverse", "host-to-worker", False, EXT(ST, "#/$defs/TypeScriptOpenUniverseV2")),
    ("SnapshotManifest", "host-to-worker", False, REF("Ts2SnapshotManifestV1")),
    ("SnapshotFileChunk", "host-to-worker", False, REF("Ts2SnapshotFileChunkV1")),
    ("SnapshotSeal", "host-to-worker", False, REF("Ts2SnapshotSealV1")),
    ("Analyze", "host-to-worker", False, REF("Ts2AnalyzeV1")),
    ("Cancel", "host-to-worker", False, REF("Ts2CancelV1")),
    ("HelloAck", "worker-to-host", False, EXT(HS, "#/$defs/TypeScriptHelloAckV2")),
    ("UniverseAccepted", "worker-to-host", False, EXT(ST, "#/$defs/TypeScriptUniverseAcceptedV2")),
    ("SnapshotAccepted", "worker-to-host", False, REF("Ts2SnapshotAcceptedV1")),
    ("NativeContextVerified", "worker-to-host", False, EXT(ST, "#/$defs/NativeContextVerifiedV1")),
    ("FactBatch", "worker-to-host", False, {"select": "negotiated-target-attribution-v2",
                                            "alternatives": {"false": REF("Ts2FactBatchV1"), "true": REF("Ts2FactBatchV3")}}),
    ("Coverage", "worker-to-host", False, EXT(ST, "#/$defs/TypeScriptCoverageV2")),
    ("Unavailable", "worker-to-host", True, {"select": "host-phase",
                                            "alternatives": {"WAIT_NATIVE_CONTEXT_VERIFIED": EXT(ST, "#/$defs/PreAnalyzeUnavailableV1"),
                                                             "ANALYZING": EXT(ST, "#/$defs/TypeScriptUnavailableV2")}}),
    ("BudgetExhausted", "worker-to-host", True, EXT(ST, "#/$defs/TypeScriptBudgetExhaustedV2")),
    ("Complete", "worker-to-host", True, REF("Ts2CompleteV1")),
    ("Cancelled", "worker-to-host", True, REF("Ts2CancelledV1")),
]
