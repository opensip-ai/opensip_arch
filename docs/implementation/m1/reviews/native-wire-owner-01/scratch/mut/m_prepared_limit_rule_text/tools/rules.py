"""Profiles, private representation, handwritten admission catalog, commitment map, state machines and
scoped supersessions for the native wire-carrier author candidate."""

from common import ORDERS

PROFILES = {
    "ts2-cbor": {
        "protocol": "typescript-semantic", "major": "2",
        "source": {"pin": "delivery2", "selector": "$.typescriptSemanticSubstrate.providerProtocol.wireSchema.canonicalCbor"},
        "dataModel": ["null", "false", "true", "uint64", "negative-int64", "UTF-8-NFC-text", "byte-string", "definite-array", "definite-text-keyed-map"],
        "negativeIntegers": "DECODABLE: major type 1 in -2^63..-1 is inside the closed data model; no TS2 carrier member has a negative-integer type, so every negative integer in a TS2 payload refuses as a type mismatch (PROVIDER.PROTOCOL_VIOLATION).",
        "forbidden": ["floating-point", "tags", "indefinite-length items", "non-shortest integer or length arguments", "duplicate map keys", "non-text map keys", "invalid UTF-8", "non-NFC text", "unknown map fields", "simple values other than false/true/null"],
        "mapOrder": "ascending bytewise order of each key's deterministic-CBOR encoding",
        "frameIntegrity": "uint64 big-endian payload length, 32 raw SHA-256 payload bytes, then one canonical-CBOR payload",
        "decodeRule": "decode once under the host-state-selected closed carrier; re-encode and require byte equality",
    },
    "rust3-cbor": {
        "protocol": "rust-semantic", "major": "3",
        "source": {"pin": "rust2", "selector": "$.canonicalCbor"},
        "dataModel": ["null", "false", "true", "uint64", "UTF-8-NFC-text", "byte-string", "definite-array", "definite-text-keyed-map"],
        "negativeIntegers": "FORBIDDEN at decode: any CBOR major type 1 item refuses before carrier typing (rust2 canonicalCbor.forbidden[0]).",
        "forbidden": ["negative integers", "floating point", "tags", "undefined and unassigned simple values", "indefinite-length items", "non-shortest integer or length arguments", "duplicate map keys", "non-text map keys", "invalid UTF-8", "non-NFC text", "unknown map fields"],
        "mapOrder": "length of encoded key first, then bytewise",
        "frameIntegrity": "8-byte big-endian payload length, 32 raw SHA-256 payload bytes, canonical-CBOR payload (40-byte prefix)",
        "decodeRule": "retain payload bytes; decode once under the host-state-selected closed carrier; re-encode and require byte equality",
    },
    "mapOrderEquivalence": "For text keys the two map-order rules select the same order: a deterministic-CBOR text key starts with its length header (0x60+n below 24, 0x78 n up to 255, 0x79 nn beyond), so bytewise order of encoded keys is length-first then bytewise. The checker proves it over every carrier member name and random keys.",
    "notProvedByJsonSchema": ["NFC", "UTF-8 byte bounds (maxLength counts scalars)", "shortest encodings", "map order", "duplicate keys", "byte strings", "negative-integer profile", "domain joins, echoes and commitments"],
}

PRIVATE_REPRESENTATION = {
    "standing": "Private carrier choices for one generator recipe; none is a wire change or a wire name.",
    "uint64": {"rust": "u64", "typescript": "bigint", "json-vector": "JSON integer (vectors only)"},
    "text": {"rust": "String (NFC and byte bounds checked by admission)", "typescript": "string"},
    "bytes": {"rust": "protocol::wire::ByteString(Vec<u8>) newtype; codec accepts only CBOR major type 2; length prefix checked against maxBytes before allocation",
              "typescript": "Uint8Array (owned copy, never a view into the frame buffer)",
              "json-vector": "lowercase hex in a member named <member>Hex, JSON vectors only; never a JSON array, base64 or hex on the wire and never a generated JSON carrier"},
    "bool": {"rust": "bool", "typescript": "boolean"},
    "null": {"rust": "unit (only inside nullable or variant-record branches)", "typescript": "null"},
    "nullable": {"rust": "Option<T> serialized as present CBOR null; never skipped", "typescript": "T | null, property required"},
    "optional": {"rust": "Option<T> with skip-when-absent; absent is not null", "typescript": "prop?: T under exactOptionalPropertyTypes; undefined never serialized"},
    "array": {"rust": "Vec<T>", "typescript": "readonly T[]"},
    "enum": {"rust": "enum with exact string renames", "typescript": "string-literal union"},
    "const": {"rust": "validated scalar (const checked at decode)", "typescript": "literal type"},
    "record": {"rust": "struct with deny-unknown-fields", "typescript": "interface; decoder rejects extra keys"},
    "variant-record": {"rust": "enum with one struct per discriminator value; codec writes every memberOrder member including nulls",
                       "typescript": "discriminated union on the discriminator member; every member present"},
    "alias": {"rust": "pub type Alias = Target;", "typescript": "export type Alias = Target;"},
    "extern": {"rust": "generated type from the registered schema (options.json namespace); JSON-vector integers map to u64/bigint because every extern integer has minimum 0",
               "typescript": "same generated type name"},
    "frame-payload": {"rust": "per-protocol enum; decode entry point takes (frameType, HostSelector) and never tries alternatives",
                      "typescript": "per-protocol discriminated union with the same selector-parameterized decoder"},
    "selectors": {
        "negotiated-target-attribution-v2": "true iff target-attribution-v2 is in both the admitted Hello and HelloAck token arrays (handshake law factBatch.negotiated)",
        "host-phase": "the host phase in which the Unavailable frame arrives; any other phase has no transition row and faults before payload typing",
    },
    "namespaces": {
        "Ts2": "delivery.v2 typescript-semantic wireSchema successors (this document)",
        "Rust3": "rust-provider-protocol.v2 wireSchema successors and native-evidence §9.2 records (this document)",
        "extern": "Handshake1, Startup1, Native2, Occupancy1 exactly as generator candidate03 options.json names them",
        "forbidden": "bare CoverageKeyV2, FactCandidateV1, AnchorRefV1, StageResult* or FactBatchV3 type names",
    },
    "orders": ORDERS,
}


def rule(id_, applies, text, owner, kind):
    return {"id": id_, "appliesTo": applies, "kind": kind, "rule": text, "owner": owner}


ADMISSION = [
    rule("FRAME-LIMIT", "both", "Declared payload length <= maxFramePayloadBytes 67108864 before allocation; every array/text/byte length checked before allocation. A member with no maxItems/maxBytes is bounded only by this limit.", "delivery2 limits.limitRule; rust2 framing.allocationRule", "bound"),
    rule("TS2-ENV-MAJOR", "typescript-semantic", "Envelope protocolMajor == 2 before payload typing.", "handshake x-opensip-wire-law.frameAndMajor", "state"),
    rule("TS2-ENV-DIRECTION-BY-FRAME", "typescript-semantic", "frameType must belong to the direction being read (closedHostToWorkerFrames + closedWorkerToHostFrames + NativeContextVerified).", "delivery2 providerProtocol.closed*Frames; nativeMd §0 line 121", "state"),
    rule("TS2-ENV-SEQUENCE", "typescript-semantic", "Per-direction sequence starts at 0 and increases by exactly 1; overflow refuses.", "delivery2 ordering.sequenceRule", "order"),
    rule("RUST3-FRAME-PRECHECK", "rust-semantic", "Before P3 matching: frameType known, direction equals the frame row direction, sequence equals that direction's counter, counter < 2^64-1, payload decodes under the selected carrier with every join below. Failure is FAULT / PROVIDER.PROTOCOL_VIOLATION (same outcome as P3-34).", "rust2 orderingAndStateMachine.transitionAstV2.framePrecheck (retained)", "state"),
    rule("ECHO-SNAPSHOT2", "both", "Every snapshotId echo (manifest, chunk, seal, accepted, SubjectScopeV1, AnchorRefV1 source-span, SubjectV2.subjectId preimage) is the exact OpenUniverse snapshot2 text.", "startup x-opensip-startup-law.identityMembers + SUCC-ECHO-ENUMERATION", "echo"),
    rule("ECHO-PLAN2", "rust-semantic", "Every PreparedOutput{Manifest,Chunk,Seal,Accepted}.planId is the exact OpenUniverse plan2 text.", "startup identityMembers + SUCC-ECHO-ENUMERATION", "echo"),
    rule("ECHO-OPEN-UNIVERSE", "both", "Analyze executionId/snapshotId/planId (and TS universeKey) equal OpenUniverse.", "delivery2 AnalyzeV1.fields; startup identityMembers", "echo"),
    rule("TS2-MANIFEST-DIGEST", "typescript-semantic", "manifestSha256 = lowercase hex SHA-256(deterministic-CBOR(entries)); no domain, no prefix; Seal and Accepted echo it.", "SUCC-TS2-MANIFEST-DIGEST", "commitment"),
    rule("RAW-MANIFEST-DIGEST", "rust-semantic", "SnapshotManifest, DependencySourceManifest and PreparedOutputManifest manifestSha256 = lowercase hex SHA-256(deterministic-CBOR(entries)); Seal and Accepted echo it.", "rust2 commitments.snapshotManifest/preparedOutputManifest; SUCC-DEPSRC-DIGEST", "commitment"),
    rule("TS2-SNAPSHOT-ORDER", "typescript-semantic", "entries strictly ascending unique by path UTF-8 bytes; kind decides the variant.", "delivery2 SnapshotManifestV1.fields.entries", "order"),
    rule("RUST3-SNAPSHOT-ENTRY-TYPES", "rust-semantic", "file: byteLength uint64, contentSha256 DigestHex, executable bool, targetBytes null; symlink: targetBytes non-empty byte string, other variant members null.", "SUCC-RUST3-SNAPSHOT-ENTRY", "shape"),
    rule("CHUNK-CUSTODY", "both", "Chunks follow entry order; chunkIndex contiguous from 0 per entry; byteOffset = checked sum of prior chunk bytes; a zero-length entry has no chunk; SHA-256 of the concatenated bytes equals the entry digest; total length equals the entry length.", "delivery2 snapshotTransport; rust2 SnapshotFileChunkV2.fields.bytes; nativeMd §3.2", "order"),
    rule("SEAL-AGGREGATES", "both", "entryCount = len(entries); total bytes = checked sum of entry lengths (Rust: <= stated limit); totalChunkCount = chunks sent.", "delivery2 SnapshotSealV1.fields; rust2 SnapshotSealV2.fields.all; ProtocolLimitsV3", "join"),
    rule("ACCEPTED-EQUALS-SEAL", "both", "Accepted members are exactly the Seal values, after byte/digest/VFS validation.", "delivery2 SnapshotAcceptedV1; rust2 SnapshotAcceptedV2; nativeMd §9.2 line 2879", "echo"),
    rule("DEPSRC-CUSTODY", "rust-semantic", "DependencySourceManifestV3.entries ordered package-then-path; each packageKey names one DependencySourceSetV1.packages row by 'name SP version SP sourceId'; the rows of one package are exactly its DependencyFileManifestV1 (H(native.dependency-file-manifest.v1) equals fileManifestSha256; count = fileCount; byte sum = totalBytes); every package of the set appears; entries <= maxDependencySourceEntries; distinct packages <= maxDependencySourcePackages; totalBytes <= maxDependencySourceTotalBytes; chunk bytes <= maxDependencySourceChunkBytes; dependencySourceSetId equals OpenUniverse.repositoryResolution.dependencySourceSetId on every frame. Empty set: entries [], manifestSha256 = hex(SHA-256(0x80)), seal counts 0, no chunk.", "SUCC-DEPSRC-DIGEST; nativeMd §3.1, §3.2, §9.3, §9.7", "join"),
    rule("PREPARED-V3-ENTRY", "rust-semantic", "entries[i] answers PreparedOutputSetV3.rows[i]: outputOrdinal = i; kind = planRow.kind; planRow = the exact row; logicalPath = '.opensip/prepared/v3/' + i + '-' + planRow.blob.sha256 + '.blob'; blobByteLength/blobSha256 = planRow.blob.byteLength/sha256; contentByteLength/contentSha256 equal the blob values (no V2 wrapper); a generated-file row requires planRow.generated.blob == planRow.blob.", "SUCC-PREPARED-V3", "join"),
    rule("PREPARED-V3-SET-JOIN", "rust-semantic", "Worker: every planRow.inputBinding.dependencySourceSetId equals repositoryResolution.dependencySourceSetId and cfgSetId names a universe.resolvedInputs.cfgSets entry; row kinds inert only. Host (before spawn): H(native.prepared-output-set.v3, {schemaVersion 3, preparation, rows: [entries[*].planRow]}) == repositoryResolution.preparedOutputSetId; macro-expansion rows <= maxExpansionRows, generated-file rows <= maxGeneratedFileRows, build-script-directives rows <= maxPreparedOutputEntries, totalBlobBytes <= maxPreparedOutputTotalBlobBytes, encoded manifest <= maxFramePayloadBytes; otherwise no spawn (host invariant, operational-failed / SYSTEM.OUTCOME.ILLEGAL_STATE as delivery2 coverageDomain.overflowFate).", "SUCC-PREPARED-V3", "join"),
    rule("TS2-BUDGET-PROJECTION", "typescript-semantic", "budget is exactly delivery2 stageRequestProjection.budgetProjection output.", "delivery2 stageRequestProjection.budgetProjection", "join"),
    rule("TS2-STAGE-PROJECTION", "typescript-semantic", "stageRequests are all and only selected stages in verified logical order; stageOrdinal contiguous 0..n-1; dependsOn [] when absent.", "delivery2 multiStageAnalyze; stageRequestProjection", "join"),
    rule("DISPATCH-STAGE-CORRELATION", "both", "stageId is C-2 text (StageIdText) and equals DispatchBindingV1.expectedStageId; stageOrdinal = analyzeRequestOrdinal, never retainedStageOrdinal; FactBatch analysisOrdinal/batchIndex/first candidateOrdinal equal the dispatch expectations; batch count 1..cap (rust2 T016 guard retained as pre-match admission).", "dispatch x-opensip-wire.correlation; nativeMd §9.6 lines 3024-3043; rust2 T016", "join"),
    rule("TS2-SUBJECT-SCOPE-RETAINED", "typescript-semantic", "SubjectScopeV1 fully retained: commitment C(opensip.coverage.subject-scope.v1, sorted SnapshotFileSubjectV1[]); subjectCount = kind=file entries; recomputed by host and worker.", "delivery2 definitions.SubjectScopeV1 (retained)", "commitment"),
    rule("PER-KEY-SCOPE2", "both", "Each request key's subjectScopeCommitment = 'sha256:' + hex of scope2 = H('subject-scope', D_key), D_key = {schemaVersion 2, snapshotId, sourceUniverse, targetUniverse (64-hex suffixes of the key), relation, resolution (the key's), enumeratorClosure (Plan-selected provider closure2 of the stage), subjects (host enumeration)}. Host mints before spawn; the same descriptor drives admit_coverage_result_v3 and pre-Analyze conversion. Worker checks Sha256Text shape only and echoes: entries[i].key.subjectScopeCommitment and entries[i].entry.examinedUniverse.subjectScopeCommitment equal keys[i]. No equality with TS SubjectScopeV1.subjectScopeCommitment or rust2 commitments.subjectScope is required.", "SUCC-PER-KEY-SCOPE2; nativeMd §4.1a; identityMd §3 lines 287-294", "commitment"),
    rule("TS2-DOMAIN-COMMITMENT", "typescript-semantic", "domainCommitment = C(opensip.ts-provider.requested-coverage-domain.v1, {subjectScope, keys}); keys carry per-key scope2 values; worker recomputes.", "delivery2 RequestedCoverageDomainV1.fields.domainCommitment", "commitment"),
    rule("RUST3-DOMAIN-COMMITMENT", "rust-semantic", "domainCommitment = C(opensip.rust-provider.analysis-domain.v2, {subjects, requestedCoverageDomain}); analysisDomain equals a fresh host reconstruction (wireRule) with per-key scope2 values.", "rust2 commitments.analysisDomain; planAndDomainProjection.wireRule", "commitment"),
    rule("RUST3-SUBJECTS", "rust-semantic", "subjectsAlgorithm retained; the snapshotId in the subjectId preimage is the snapshot2 text.", "rust2 planAndDomainProjection.subjectsAlgorithm; SUCC-ECHO-ENUMERATION", "commitment"),
    rule("RUST3-PLAN-STAGE-BYTES", "rust-semantic", "deterministic-CBOR(planStage) equals the selected ExecutionPlan stage bytes; optional members absent exactly when absent.", "rust2 planAndDomainProjection.planStageByteRule", "join"),
    rule("UNIVERSE-NATIVE-IDENTITY", "both", "Universe ids are sha256:hex(H(native.semantic-universe.<language>.v2, universe.resolvedInputs)); CoverageKeyV2 entries carry the 64-hex suffix.", "startup universeIdentity; nativeMd §0 lines 125, 128", "join"),
    rule("FP-CANDIDATE", "both", "fact-plane candidate law: registry relation/rung/layer/schemaId, producer/language constants, producerVersion = verified providerBuildId, target universe in host-admitted target domain.", "factPlane candidateSchema.fields; delivery2 FactCandidateV1.fields", "join"),
    rule("RELATION-PAYLOAD-CBOR", "both", "canonicalRelationPayload decodes once to the registry payload schema and re-encodes byte-equal; <= 1048576 bytes.", "factPlane candidateSchema.transportRepresentation; handshake candidateCborProjection", "shape"),
    rule("ANCHOR-WIRE-SPAN", "both", "Wire anchor rule (retained fact-plane sourceSpanSchema.rule): source-span requires snapshotId = OpenUniverse snapshot2, path = a kind=file manifest path, contentSha256 = that entry digest, startByte < endByte <= entry byteLength (NON-EMPTY). Array order: TS2 cbor-bytes-strict (delivery2 AnchorRefV1.ordering), Rust3 cve1-bytes-strict (factPlane anchorSchema.ordering); count 1..100000. The shared fact2 rule (identity-model.v3.py line 1892 ANCHOR_RANGE: 0 <= a <= b <= len, plus ANCHOR_UTF8) is NOT narrowed: the non-empty requirement is a provider-wire admission rule only, and zero-length fact2 anchors from other producers stay admissible.", "SUCC-ANCHOR-RULES", "join"),
    rule("ANCHOR-FACT-REF-REFUSED", "both", "kind=fact-ref is PROVIDER.PROTOCOL_VIOLATION at candidate admission before any fact2 mint, because fact-identity-fact2 is a mandatory identity token in both token sets and identity-schemas.v3 fact.anchors has no fact reference.", "SUCC-FACT-REF-REFUSED", "state"),
    rule("OCCUPANCY-JOIN", "both", "occupancyCompanions length <= len(candidates); each candidateOrdinal names a candidate of this batch; targetUniverseId byte-equal to that candidate.", "occupancy x-opensip-order-vocabulary.candidateOrdinal; nativeMd §9.6", "join"),
    rule("RUST3-SPOOL", "rust-semantic", "Candidate spool accounting over deterministic-CBOR({analysisOrdinal, stageId, candidate}) retained; bytes budget increments use candidate encoded length.", "rust2 limitPolicy.candidateSpoolAccounting; deterministicBudget", "bound"),
    rule("COMMIT-MAP", "both", "Every stage/stream/terminal commitment uses exactly the commitmentMap row for its field.", "SUCC-COMMIT-MAP", "commitment"),
    rule("COMMIT-TS2-FACT-BATCH", "typescript-semantic", "batchCommitment = C(opensip.ts-provider.fact-batch.v1, facts) over wire candidates; FactBatchV3 carries none.", "handshake x-opensip-wire-law.commitments.typescript-semantic", "commitment"),
    rule("CANCEL-NULLABILITY", "both", "Cancel.executionId is null iff OpenUniverse has not been sent, otherwise its exact value; analysisOrdinal is null iff Analyze has not been sent, otherwise Analyze.analysisOrdinal (TS2: 0).", "delivery2 CancelV1.fields; SUCC-RUST3-FAULT-CANCEL", "echo"),
    rule("CANCELLED-ECHO", "both", "Cancelled executionId and analysisOrdinal equal the Cancel values.", "delivery2 CancelledV1.fields; rust2 CancelledV2.fields.all", "echo"),
    rule("TS2-OBSERVED-PHASE", "typescript-semantic", "observedPhase is the inherited enum; snapshot for a Cancel in WAIT_NATIVE_CONTEXT_VERIFIED or READY_ANALYZE.", "startup x-opensip-startup-law.cancellation", "state"),
    rule("RUST3-FAULT-CANCEL-TYPES", "rust-semantic", "ProviderFault.executionId/analysisOrdinal: null iff the worker has not received OpenUniverse/Analyze, otherwise the received values; ProviderFault.phase and Cancelled.observedPhase are the host phase in which the Cancel was sent or the fault received (one of the 16 *PRE_COMPLETE phases); detailCode IdentityText, diagnostic only, normalizes to provider-protocol.", "SUCC-RUST3-FAULT-CANCEL", "state"),
    rule("RUST3-BUDGET-EXHAUSTED", "rust-semantic", "triggerStageId = current stage; unit/limit = planStage.budget (a stage without budget or with milliseconds cannot BudgetExhausted); observed = limit + 1 (checked).", "rust2 T020 guard (retained pre-match); SUCC-RUST3-OBSERVED", "join"),
]

DOMAIN_RULE = "C(d, v) = 'sha256:' + lowercase hex SHA-256(UTF8(d) || 0x00 || deterministic-CBOR(v))"
COMMITMENT_MAP = {
    "function": DOMAIN_RULE,
    "rows": [
        {"protocol": "typescript-semantic", "field": "Startup1TypeScriptCoverageV2.coverageCommitment", "domain": "opensip.ts-provider.stage-coverage.v1", "value": "this frame's entries (CoverageResultV3[])"},
        {"protocol": "typescript-semantic", "field": "Ts2StageResultV1.coverageCommitment", "domain": "opensip.ts-provider.stage-coverage.v1", "value": "that stage's entries; equals its Coverage frame value"},
        {"protocol": "typescript-semantic", "field": "Ts2CompleteV1.coverageStreamCommitment", "domain": "opensip.ts-provider.coverage-stream.v1", "value": "all entries, stage-major/key order"},
        {"protocol": "typescript-semantic", "field": "Startup1TypeScriptUnavailableV2.coverageCommitment", "domain": "opensip.ts-provider.coverage-stream.v1", "value": "coverage (stage-major/key order)"},
        {"protocol": "typescript-semantic", "field": "Startup1TypeScriptBudgetExhaustedV2.coverageCommitment", "domain": "opensip.ts-provider.coverage-stream.v1", "value": "coverage (stage-major/key order)"},
        {"protocol": "typescript-semantic", "field": "Ts2StageResultV1.factCommitment", "domain": "opensip.ts-provider.stage-facts.v1", "value": "that stage's wire FactCandidateV1 values in order, whichever FactBatch payload carried them; empty stage commits 0x80"},
        {"protocol": "typescript-semantic", "field": "Ts2CompleteV1.factStreamCommitment", "domain": "opensip.ts-provider.fact-stream.v1", "value": "all wire candidates stage-major"},
        {"protocol": "typescript-semantic", "field": "Ts2FactBatchV1.batchCommitment", "domain": "opensip.ts-provider.fact-batch.v1", "value": "facts"},
        {"protocol": "typescript-semantic", "field": "Ts2RequestedCoverageDomainV1.domainCommitment", "domain": "opensip.ts-provider.requested-coverage-domain.v1", "value": "{subjectScope, keys}"},
        {"protocol": "typescript-semantic", "field": "Ts2SubjectScopeV1.subjectScopeCommitment", "domain": "opensip.coverage.subject-scope.v1", "value": "sorted SnapshotFileSubjectV1[]"},
        {"protocol": "both", "field": "Ts2CoverageKeyV1.subjectScopeCommitment / Rust3CoverageKeyV2.subjectScopeCommitment / Native2CoverageKeyV2.subjectScopeCommitment / Native2ExaminedUniverseV1.subjectScopeCommitment", "domain": "foundation identity H('subject-scope') (no delivery/rust domain)", "value": "D_key; spelled sha256:<scope2 hex>", "recipe": "identity canonical H frame, not DOMAIN_RULE"},
        {"protocol": "typescript-semantic", "field": "Ts2SnapshotManifestV1.manifestSha256 (+ Seal/Accepted echo)", "domain": None, "value": "entries", "recipe": "lowercase hex SHA-256(deterministic-CBOR(entries)); delivery2 commitments.domains.snapshotManifest not applied"},
        {"protocol": "rust-semantic", "field": "Startup1CoverageV3.coverageCommitment", "domain": "opensip.rust-provider.stage-coverage.v2", "value": "this frame's entries"},
        {"protocol": "rust-semantic", "field": "Rust3StageResultV2.coverageCommitment", "domain": "opensip.rust-provider.stage-coverage.v2", "value": "that stage's entries"},
        {"protocol": "rust-semantic", "field": "Rust3CompleteV2.coverageStreamCommitment", "domain": "opensip.rust-provider.coverage-stream.v2", "value": "all entries stage-major"},
        {"protocol": "rust-semantic", "field": "Startup1UnavailableV3.coverageCommitment", "domain": "opensip.rust-provider.coverage-stream.v2", "value": "coverage"},
        {"protocol": "rust-semantic", "field": "Startup1BudgetExhaustedV3.coverageCommitment", "domain": "opensip.rust-provider.coverage-stream.v2", "value": "coverage"},
        {"protocol": "rust-semantic", "field": "Rust3StageResultV2.factCommitment", "domain": "opensip.rust-provider.stage-facts.v2", "value": "that stage's wire candidates"},
        {"protocol": "rust-semantic", "field": "Rust3CompleteV2.factStreamCommitment", "domain": "opensip.rust-provider.fact-stream.v2", "value": "all wire candidates stage-major"},
        {"protocol": "rust-semantic", "field": "Rust3StageAnalysisDomainV2.domainCommitment", "domain": "opensip.rust-provider.analysis-domain.v2", "value": "{subjects, requestedCoverageDomain}"},
        {"protocol": "rust-semantic", "field": "Rust3SubjectV2.subjectId", "domain": "opensip.rust-provider.subject.v2", "value": "{snapshotId (snapshot2 text), path, contentSha256, byteLength}", "recipe": "'rust-file:sha256:' + hex(...) as rust2 subjectsAlgorithm"},
        {"protocol": "rust-semantic", "field": "Rust3SnapshotManifestV2 / Native2DependencySourceManifestV3 / Rust3PreparedOutputManifestV3 .manifestSha256", "domain": None, "value": "entries", "recipe": "lowercase hex SHA-256(deterministic-CBOR(entries))"},
    ],
    "basis": "Preimage shape decides the domain: per-stage ordered entries match stageCoverage ('stageCoverageEntries'); stage-major arrays across all requested stages match coverageStream ('stage-major ... values'). Terminal Unavailable/BudgetExhausted coverage is stage-major across all stages, so it is coverageStream. The v1 checker (non-owner, *.v1 domains) used the same structure; the v2 checker executes none of these recipes.",
}

TRANSITIONS = {
    "typescript-semantic": {
        "base": {"pin": "ts2order", "rules": "23"},
        "overlay": "none: T2-14 already guards post-Analyze Unavailable with outputSeen=false; T2-18 keeps Cancel from START (delivery2 cancelTransition).",
    },
    "rust-semantic": {
        "base": {"pin": "p3", "rules": "34"},
        "precedence": "protocol3-transitions.v1.json is the only matching table for major 3; rust2 transitionAstV2 rules are not interpreted. rust2 framePrecheck and the T016/T020 payload guards are retained as pre-match admission (RUST3-FRAME-PRECHECK, DISPATCH-STAGE-CORRELATION, RUST3-BUDGET-EXHAUSTED).",
        "stateAdditions": {"outputSeen": False},
        "stateUpdateAdditions": [{"onFrame": "Analyze", "sets": "outputSeen = false"},
                                 {"onFrames": ["FactBatch", "CoverageV3"], "sets": "outputSeen = true"}],
        "guardAdditions": {"P3-25": {"outputSeen": False}},
        "cancelInStart": "No row (P3-29 *PRE_COMPLETE excludes START). The host never emits Cancel before Hello; an interruption in START terminates the child without a Cancel frame and interrupted/130 precedence is unchanged.",
        "terminalGuards": "Unchanged P3 preMatchLaw: FAULT absorbing; any frame after a terminal in WAIT_ZERO_EXIT/WAIT_EOF/DONE faults; process faults from any phase; unmatched frame P3-34.",
        "custodyOrder": "SnapshotAccepted -> DependencySource custody (always) -> PreparedOutput custody iff preparedOutputSetId != null -> NativeContextVerified or pre-Analyze Unavailable -> Analyze (nativeMd §9.1 step 4 lines 2863-2866; P3-08..P3-22).",
    },
}
