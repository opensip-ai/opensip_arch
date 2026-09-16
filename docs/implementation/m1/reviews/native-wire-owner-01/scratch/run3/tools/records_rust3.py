"""rust-semantic protocol major 3 wire carriers (namespace Rust3)."""
from common import (U, T, B, BOOL, NULL, A, REF, EXT, NULLABLE, M, REC, VREC, ALIAS, SRC, HS, ST, NE, OC, I63_MAX)

R2 = "$.wireSchema."
FRAME_BYTES = 67108864
PRE_COMPLETE = ["WAIT_HELLO_ACK", "READY_OPEN_UNIVERSE", "WAIT_UNIVERSE_ACCEPTED", "READY_SNAPSHOT_MANIFEST",
                "RECEIVING_SNAPSHOT", "WAIT_SNAPSHOT_ACCEPTED", "READY_DEPENDENCY_MANIFEST", "RECEIVING_DEPENDENCY",
                "WAIT_DEPENDENCY_ACCEPTED", "READY_PREPARED_MANIFEST", "RECEIVING_PREPARED", "WAIT_PREPARED_ACCEPTED",
                "WAIT_NATIVE_CONTEXT_VERIFIED", "READY_ANALYZE", "ANALYZING", "READY_COMPLETE"]

SCALARS = {
    "Rust3IdentityText": {"type": T(min_scalars=1, max_scalars=4096, max_utf8=4096, pattern="^[^\\u0000-\\u001f\\u0080-\\u009f]+(?![\\s\\S])", controls=True), "sameShapeAs": HS + "#/$defs/IdentityText",
                          "source": SRC("rust2", R2 + "definitions.IdentityText")},
    "Rust3DigestHex": {"type": T(pattern="^[0-9a-f]{64}(?![\\s\\S])"), "sameShapeAs": HS + "#/$defs/DigestHex",
                       "source": SRC("rust2", R2 + "definitions.DigestHex")},
    "Rust3Sha256Text": {"type": T(pattern="^sha256:[0-9a-f]{64}(?![\\s\\S])"), "sameShapeAs": HS + "#/$defs/Sha256Text",
                        "source": SRC("rust2", R2 + "definitions.Sha256Text")},
    "Rust3CanonicalPath": {"type": T(min_scalars=1, max_utf8=4096, pattern="^(?!/)(?![A-Za-z]:)(?!.*(^|/)\\.\\.?(/|$))(?!.*//)[^\\u0000\\\\]+(?<!/)(?![\\s\\S])"),
                           "source": SRC("rust2", R2 + "definitions.CanonicalPath"),
                           "note": "rust2 rule (no leading slash, backslash, NUL, drive prefix, empty/dot/dot-dot segment). 4096 bytes is c2 v3 canonicalRelativePath, the bound of every host-constructed path; Native2CanonicalPath is weaker and is not used for this carrier."},
    "Rust3StageIdText": {"type": T(min_scalars=1, max_scalars=255), "sameShapeAs": ST + "#/$defs/StageIdText",
                         "source": SRC("dispatch", "#/properties/expectedStageId")},
    "Rust3SnapshotId2": {"type": T(pattern="^snapshot2:[0-9a-f]{64}(?![\\s\\S])"), "sameShapeAs": ST + "#/$defs/SnapshotId2",
                         "source": SRC("startup", "#/$defs/SnapshotId2")},
    "Rust3PlanId2": {"type": T(pattern="^plan2:[0-9a-f]{64}(?![\\s\\S])"), "sameShapeAs": ST + "#/$defs/PlanId2",
                     "source": SRC("startup", "#/$defs/PlanId2")},
    "Rust3CanonicalIdentifier": {"type": T(min_scalars=1, max_utf8=128, pattern="^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*(?![\\s\\S])"),
                                 "source": SRC("c2v3", "$.planIntent.wireTypes.canonicalIdentifier")},
    "Rust3PackageKey": {"type": T(min_scalars=5, max_scalars=4096, pattern="^[^ ]+ [^ ]+ [^ ]*(?![\\s\\S])"),
                        "source": SRC("nativeModel", "dependency_source_set_admit key f'{name} {version} {sourceId}'"),
                        "note": "Grammar settled by this candidate: name SP version SP sourceId of exactly one DependencySourceSetV1.packages row (same spelling as UnifiedFeaturesV1.activated[].packageKey)."},
}

SNAP, PLAN, DIG, SHA = REF("Rust3SnapshotId2"), REF("Rust3PlanId2"), REF("Rust3DigestHex"), REF("Rust3Sha256Text")
STAGE, IDT, PATH = REF("Rust3StageIdText"), REF("Rust3IdentityText"), REF("Rust3CanonicalPath")
ANCHOR_MEMBERS = ["kind", "snapshotId", "path", "contentSha256", "startByte", "endByte", "factId"]
FRAME_NAMES = ["Hello", "HelloAck", "OpenUniverse", "UniverseAccepted", "SnapshotManifest", "SnapshotFileChunk",
               "SnapshotSeal", "SnapshotAccepted", "DependencySourceManifest", "DependencySourceChunk",
               "DependencySourceSeal", "DependencySourceAccepted", "PreparedOutputManifest", "PreparedOutputChunk",
               "PreparedOutputSeal", "PreparedOutputAccepted", "NativeContextVerified", "Analyze", "FactBatch",
               "CoverageV3", "Unavailable", "BudgetExhausted", "Complete", "ProviderFault", "Cancel", "Cancelled"]

AGG = lambda total_name, total_max: [M("entryCount", U()), M(total_name, U(max=total_max)), M("totalChunkCount", U())]

RECORDS = {
    "Rust3ProviderFrameV3": REC([
        M("protocolMajor", U(const=3)), M("direction", T(enum=["host-to-worker", "worker-to-host"])),
        M("sequence", U()), M("frameType", T(enum=FRAME_NAMES)),
        M("payload", {"t": "frame-payload", "protocol": "rust-semantic"}),
    ], SRC("rust2", R2 + "envelope"), ["RUST3-FRAME-PRECHECK", "FRAME-LIMIT"],
        "Private name; RustProviderEnvelopeV2 is not reused and no published name is invented on the wire."),
    "Rust3SnapshotEntryV2": VREC("kind", ["path", "kind", "byteLength", "contentSha256", "executable", "targetBytes"], {
        "file": {"path": PATH, "byteLength": U(), "contentSha256": DIG, "executable": BOOL(), "targetBytes": NULL},
        "symlink": {"path": PATH, "byteLength": NULL, "contentSha256": NULL, "executable": NULL,
                    "targetBytes": B(1, FRAME_BYTES)},
    }, SRC("rust2", R2 + "definitions.SnapshotEntryV2"), ["RUST3-SNAPSHOT-ENTRY-TYPES"]),
    "Rust3SnapshotManifestV2": REC([
        M("snapshotId", SNAP), M("manifestSha256", DIG),
        M("entries", A(REF("Rust3SnapshotEntryV2"), 1, 200000, "path-utf8-strict")),
    ], SRC("rust2", R2 + "payloadSchemas.SnapshotManifestV2"), ["ECHO-SNAPSHOT2", "RAW-MANIFEST-DIGEST"]),
    "Rust3SnapshotFileChunkV2": REC([
        M("snapshotId", SNAP), M("path", PATH), M("chunkIndex", U()), M("byteOffset", U()), M("bytes", B(1, 1048576)),
    ], SRC("rust2", R2 + "payloadSchemas.SnapshotFileChunkV2"), ["ECHO-SNAPSHOT2", "CHUNK-CUSTODY"]),
    "Rust3SnapshotSealV2": REC([M("snapshotId", SNAP), M("manifestSha256", DIG)] + AGG("totalFileBytes", 8589934592),
                               SRC("rust2", R2 + "payloadSchemas.SnapshotSealV2"), ["ECHO-SNAPSHOT2", "SEAL-AGGREGATES"]),
    "Rust3SnapshotAcceptedV2": REC([M("snapshotId", SNAP), M("manifestSha256", DIG)] + AGG("totalFileBytes", 8589934592),
                                   SRC("rust2", R2 + "payloadSchemas.SnapshotAcceptedV2"), ["ACCEPTED-EQUALS-SEAL"]),
    "Rust3DependencySourceChunkV3": REC([
        M("dependencySourceSetId", SHA), M("packageKey", REF("Rust3PackageKey")),
        M("path", EXT(NE, "#/$defs/CanonicalPath")), M("chunkIndex", U()), M("byteOffset", U()),
        M("bytes", B(1, 1048576)),
    ], SRC("nativeMd", "§9.2 line 2877 DependencySourceChunk member list"), ["DEPSRC-CUSTODY"],
        "New private record name for an existing frame; member list exactly as §9.2 states. path uses the manifest entry path shape it echoes."),
    "Rust3DependencySourceAcceptedV3": ALIAS(EXT(NE, "#/$defs/DependencySourceSealV3"),
                                             SRC("nativeMd", "§9.2 line 2879 'exact seal echo'"),
                                             "Private alias: identical member set and types to Native2DependencySourceSealV3; ACCEPTED-EQUALS-SEAL."),
    "Rust3PreparedOutputEntryV3": REC([
        M("outputOrdinal", U(max=2000255)),
        M("kind", T(enum=["build-script-directives", "macro-expansion", "generated-file"])),
        M("planRow", EXT(NE, "#/$defs/PreparedOutputRowV3")),
        M("logicalPath", T(pattern="^\\.opensip/prepared/v3/(0|[1-9][0-9]*)-[0-9a-f]{64}\\.blob(?![\\s\\S])")),
        M("blobByteLength", U(max=1073741824)), M("blobSha256", DIG),
        M("contentByteLength", U(max=1073741824)), M("contentSha256", DIG),
    ], SRC("rust2", R2 + "definitions.PreparedOutputEntryV2"), ["PREPARED-V3-ENTRY"],
        "Member names of PreparedOutputEntryV2 unchanged; value domains substituted to the Plan-bound PreparedOutputSetV3 row (scoped successor SUCC-PREPARED-V3)."),
    "Rust3PreparedOutputManifestV3": REC([
        M("planId", PLAN), M("manifestSha256", DIG),
        M("entries", A(REF("Rust3PreparedOutputEntryV3"), 0, 2000256, "outputOrdinal-contiguous")),
    ], SRC("rust2", R2 + "payloadSchemas.PreparedOutputManifestV2"), ["ECHO-PLAN2", "RAW-MANIFEST-DIGEST", "PREPARED-V3-SET-JOIN"]),
    "Rust3PreparedOutputChunkV3": REC([
        M("planId", PLAN), M("outputOrdinal", U(max=2000255)), M("chunkIndex", U()), M("byteOffset", U()),
        M("bytes", B(1, 1048576)),
    ], SRC("rust2", R2 + "payloadSchemas.PreparedOutputChunkV2"), ["ECHO-PLAN2", "CHUNK-CUSTODY"]),
    "Rust3PreparedOutputSealV3": REC([M("planId", PLAN), M("manifestSha256", DIG)] + AGG("totalBlobBytes", 1073741824),
                                     SRC("rust2", R2 + "payloadSchemas.PreparedOutputSealV2"), ["ECHO-PLAN2", "SEAL-AGGREGATES"]),
    "Rust3PreparedOutputAcceptedV3": REC([M("planId", PLAN), M("manifestSha256", DIG)] + AGG("totalBlobBytes", 1073741824),
                                         SRC("rust2", R2 + "payloadSchemas.PreparedOutputAcceptedV2"), ["ACCEPTED-EQUALS-SEAL"]),
    "Rust3SubjectV2": REC([
        M("subjectOrdinal", U(max=255)), M("subjectId", T(pattern="^rust-file:sha256:[0-9a-f]{64}(?![\\s\\S])")),
        M("path", PATH), M("startByte", U(const=0)), M("endByte", U(min=1)),
    ], SRC("rust2", R2 + "definitions.SubjectV2"), ["RUST3-SUBJECTS", "ECHO-SNAPSHOT2"]),
    "Rust3CoverageKeyV2": REC([
        M("relation", EXT(NE, "#/$defs/Relation")), M("resolution", EXT(NE, "#/$defs/Rung")),
        M("sourceUniverseId", SHA), M("targetUniverseId", SHA), M("subjectScopeCommitment", SHA),
        M("producer", T(const="rust-semantic")), M("producerVersion", IDT), M("schemaVersion", U()),
    ], SRC("rust2", R2 + "definitions.CoverageKeyV2"), ["UNIVERSE-NATIVE-IDENTITY", "PER-KEY-SCOPE2"],
        "rust2 8-member request key (c2 v3 coverageKey.key). Never merged with Native2CoverageKeyV2 (5-member entry key) or Ts2CoverageKeyV1."),
    "Rust3StageAnalysisDomainV2": REC([
        M("subjects", A(REF("Rust3SubjectV2"), 1, 256, "path-utf8-strict")),
        M("requestedCoverageDomain", A(REF("Rust3CoverageKeyV2"), 1, 256, "nested-loop-relation-rung-target")),
        M("domainCommitment", SHA),
    ], SRC("rust2", R2 + "definitions.StageAnalysisDomainV2"), ["RUST3-DOMAIN-COMMITMENT", "PER-KEY-SCOPE2"]),
    "Rust3C2StageBudgetV1": REC([
        M("unit", T(enum=["work-units", "milliseconds", "bytes", "items"])), M("limit", U(min=1, max=I63_MAX)),
    ], SRC("c2v3", "$.planIntent.wireTypes.stageBudgetV1")),
    "Rust3C2PlanStageV3": REC([
        M("kind", T(const="fact-derivation")), M("stageId", STAGE),
        M("dependsOn", A(STAGE, 0, None, "sequence"), "optional"),
        M("budget", REF("Rust3C2StageBudgetV1"), "optional"),
        M("relations", A(EXT(NE, "#/$defs/Relation"), 1, 64, "sequence")),
        M("operator", T(const="semantic-provider")),
        M("capabilityGrants", A(REF("Rust3CanonicalIdentifier"), 0, None, "sequence"), "optional"),
        M("providerId", T(const="rust-semantic"), "optional"),
    ], SRC("c2v3", "$.stageSchemas.common + $.stageSchemas.kinds.fact-derivation"), ["RUST3-PLAN-STAGE-BYTES"],
        "Optional members are ABSENT (never null) when absent in the ExecutionPlan; deterministic-CBOR(planStage) must equal the selected Plan stage bytes."),
    "Rust3StageRequestV2": REC([
        M("stageOrdinal", U(max=255)), M("planStage", REF("Rust3C2PlanStageV3")),
        M("analysisDomain", REF("Rust3StageAnalysisDomainV2")),
    ], SRC("rust2", R2 + "definitions.StageRequestV2"), ["DISPATCH-STAGE-CORRELATION"]),
    "Rust3AnalyzeV2": REC([
        M("analysisOrdinal", U()), M("executionId", IDT), M("snapshotId", SNAP), M("planId", PLAN),
        M("stages", A(REF("Rust3StageRequestV2"), 1, 256, "sequence")),
    ], SRC("rust2", R2 + "payloadSchemas.AnalyzeV2"), ["ECHO-OPEN-UNIVERSE"]),
    "Rust3AnchorRefV1": VREC("kind", ANCHOR_MEMBERS, {
        "source-span": {"snapshotId": SNAP, "path": PATH, "contentSha256": DIG, "startByte": U(), "endByte": U(),
                        "factId": NULL},
        "fact-ref": {"snapshotId": NULL, "path": NULL, "contentSha256": NULL, "startByte": NULL, "endByte": NULL,
                     "factId": T(min_scalars=1, max_utf8=4096)},
    }, SRC("factPlane", "$.factRecordContractV1.anchorSchema"), ["ANCHOR-WIRE-SPAN", "ANCHOR-FACT-REF-REFUSED", "ECHO-SNAPSHOT2"]),
    "Rust3FactCandidateV1": REC([
        M("candidateOrdinal", U()), M("relation", EXT(NE, "#/$defs/Relation")), M("resolution", EXT(NE, "#/$defs/Rung")),
        M("layer", T(enum=["derived", "inventory", "semantic", "syntax"])),
        M("producer", T(const="rust-semantic")), M("producerVersion", IDT), M("schemaVersion", U()),
        M("language", T(const="rust")), M("sourceUniverseId", SHA), M("targetUniverseId", SHA),
        M("confidenceMillionths", U(max=1000000)), M("relationSchemaId", T(min_scalars=1, max_utf8=4096)),
        M("canonicalRelationPayload", B(1, 1048576)),
        M("anchors", A(REF("Rust3AnchorRefV1"), 1, 100000, "cve1-bytes-strict")),
    ], SRC("factPlane", "$.factRecordContractV1.candidateSchema"), ["FP-CANDIDATE", "UNIVERSE-NATIVE-IDENTITY", "RELATION-PAYLOAD-CBOR"]),
    "Rust3FactBatchV2": REC([
        M("analysisOrdinal", U()), M("stageId", STAGE), M("batchIndex", U()),
        M("candidates", A(REF("Rust3FactCandidateV1"), 1, 4096, "candidateOrdinal-contiguous")),
    ], SRC("rust2", R2 + "payloadSchemas.FactBatchV2"), ["DISPATCH-STAGE-CORRELATION", "RUST3-SPOOL"]),
    "Rust3FactBatchV3": REC([
        M("schemaVersion", U(const=3)), M("analysisOrdinal", U()), M("stageId", STAGE), M("batchIndex", U()),
        M("candidates", A(REF("Rust3FactCandidateV1"), 1, 4096, "candidateOrdinal-contiguous")),
        M("occupancyCompanions", A(EXT(OC, "#"), 0, 4096, "candidateOrdinal-increasing")),
    ], SRC("factBatch3", "#"), ["DISPATCH-STAGE-CORRELATION", "OCCUPANCY-JOIN", "RUST3-SPOOL"]),
    "Rust3StageResultV2": REC([
        M("stageId", STAGE), M("factCount", U()), M("coverageEntryCount", U()), M("factCommitment", SHA),
        M("coverageCommitment", SHA),
    ], SRC("rust2", R2 + "definitions.StageResultV2"), ["COMMIT-MAP"],
        "Retained members; values commit CoverageResultV3 (native-evidence §9.7 names StageResultV2.coverageCommitment explicitly)."),
    "Rust3CompleteV2": REC([
        M("analysisOrdinal", U()), M("stageResults", A(REF("Rust3StageResultV2"), 1, 256, "request-order")),
        M("factStreamCommitment", SHA), M("coverageStreamCommitment", SHA),
    ], SRC("rust2", R2 + "payloadSchemas.CompleteV2"), ["COMMIT-MAP"]),
    "Rust3ProviderFaultV2": REC([
        M("executionId", NULLABLE(IDT)), M("analysisOrdinal", NULLABLE(U())), M("phase", T(enum=PRE_COMPLETE)),
        M("faultKind", T(enum=["compiler-crash", "internal-invariant", "input-rejected"])), M("detailCode", IDT),
    ], SRC("rust2", R2 + "payloadSchemas.ProviderFaultV2"), ["RUST3-FAULT-CANCEL-TYPES"]),
    "Rust3CancelV2": REC([
        M("executionId", NULLABLE(IDT)), M("analysisOrdinal", NULLABLE(U())), M("reason", T(const="user-interrupt")),
    ], SRC("rust2", R2 + "payloadSchemas.CancelV2"), ["RUST3-FAULT-CANCEL-TYPES", "CANCEL-NULLABILITY"]),
    "Rust3CancelledV2": REC([
        M("executionId", NULLABLE(IDT)), M("analysisOrdinal", NULLABLE(U())), M("observedPhase", T(enum=PRE_COMPLETE)),
    ], SRC("rust2", R2 + "payloadSchemas.CancelledV2"), ["RUST3-FAULT-CANCEL-TYPES", "CANCELLED-ECHO"]),
}
PREIMAGE_ONLY = set()

FRAMES = [
    ("Hello", "host-to-worker", False, EXT(HS, "#/$defs/HelloV3")),
    ("HelloAck", "worker-to-host", False, EXT(HS, "#/$defs/HelloAckV3")),
    ("OpenUniverse", "host-to-worker", False, EXT(ST, "#/$defs/OpenUniverseV3")),
    ("UniverseAccepted", "worker-to-host", False, EXT(ST, "#/$defs/UniverseAcceptedV3")),
    ("SnapshotManifest", "host-to-worker", False, REF("Rust3SnapshotManifestV2")),
    ("SnapshotFileChunk", "host-to-worker", False, REF("Rust3SnapshotFileChunkV2")),
    ("SnapshotSeal", "host-to-worker", False, REF("Rust3SnapshotSealV2")),
    ("SnapshotAccepted", "worker-to-host", False, REF("Rust3SnapshotAcceptedV2")),
    ("DependencySourceManifest", "host-to-worker", False, EXT(NE, "#/$defs/DependencySourceManifestV3")),
    ("DependencySourceChunk", "host-to-worker", False, REF("Rust3DependencySourceChunkV3")),
    ("DependencySourceSeal", "host-to-worker", False, EXT(NE, "#/$defs/DependencySourceSealV3")),
    ("DependencySourceAccepted", "worker-to-host", False, REF("Rust3DependencySourceAcceptedV3")),
    ("PreparedOutputManifest", "host-to-worker", False, REF("Rust3PreparedOutputManifestV3")),
    ("PreparedOutputChunk", "host-to-worker", False, REF("Rust3PreparedOutputChunkV3")),
    ("PreparedOutputSeal", "host-to-worker", False, REF("Rust3PreparedOutputSealV3")),
    ("PreparedOutputAccepted", "worker-to-host", False, REF("Rust3PreparedOutputAcceptedV3")),
    ("NativeContextVerified", "worker-to-host", False, EXT(ST, "#/$defs/NativeContextVerifiedV1")),
    ("Analyze", "host-to-worker", False, REF("Rust3AnalyzeV2")),
    ("FactBatch", "worker-to-host", False, {"select": "negotiated-target-attribution-v2",
                                            "alternatives": {"false": REF("Rust3FactBatchV2"), "true": REF("Rust3FactBatchV3")}}),
    ("CoverageV3", "worker-to-host", False, EXT(ST, "#/$defs/CoverageV3")),
    ("Unavailable", "worker-to-host", True, {"select": "host-phase",
                                            "alternatives": {"WAIT_NATIVE_CONTEXT_VERIFIED": EXT(ST, "#/$defs/PreAnalyzeUnavailableV1"),
                                                             "ANALYZING": EXT(ST, "#/$defs/UnavailableV3")}}),
    ("BudgetExhausted", "worker-to-host", True, EXT(ST, "#/$defs/BudgetExhaustedV3")),
    ("Complete", "worker-to-host", True, REF("Rust3CompleteV2")),
    ("ProviderFault", "worker-to-host", True, REF("Rust3ProviderFaultV2")),
    ("Cancel", "host-to-worker", False, REF("Rust3CancelV2")),
    ("Cancelled", "worker-to-host", True, REF("Rust3CancelledV2")),
]
