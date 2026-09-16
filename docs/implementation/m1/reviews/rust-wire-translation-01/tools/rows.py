"""Rust3 translation rows: every rust-provider-protocol.v2 $.wireSchema member, external expansions, and new
schema-native members. Proposed implementation artifact; not product code."""
from common import (A, A_ANCHOR, A_C2, A_DISPATCH, A_DS, A_ECHO, A_F92, A_FP, A_INH, A_LIM, A_NCV, A_P3, A_PRE,
                    A_PREP, A_R118, A_R122, A_R123, A_R128, A_R129, A_R130, A_RV1, A_UNIV, B, BOOL, DB, F, FB, FBC,
                    HS, M, NE, R, ST, T, U, X)

ARITH = "derived: rust2 $.limitPolicy.arithmetic (checked uint64 counts/offsets/aggregates); no per-field type text"
ECHO = "echo (no v2 field text): "
SNAP2 = "SnapshotId2 ^snapshot2:[0-9a-f]{64}"
PLAN2 = "PlanId2 ^plan2:[0-9a-f]{64}"
IDTEXT = "IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control"
STAGEID = "StageIdText 1..255 (code points): C-2 stageId text echo of StageRequestV2.planStage.stageId; not stageOrdinal, not retainedStageOrdinal"

ENVELOPE = {
    "protocolMajor": R(U, U, "exactly 3 (inherited field text 'uint64 exactly 2')", "value-substituted",
                       A_R122 + "; provider-handshake law frameAndMajor.rust-semantic",
                       h=["wire.admit_hello: envelope protocolMajor == 3 before payload admission", "wire.admit_hello_ack"]),
    "direction": R(T, T, "enum host-to-worker|worker-to-host; equals the frame row direction", "retained", A_INH,
                   h=["rp2.transitionAstV2 framePrecheck directionMatchesFrameSchema", "chk2.step_frame"],
                   x="Rust-only envelope member: the TS2 frameEnvelope has no direction member; never merge the envelopes"),
    "sequence": R(U, U, "exact next sequence for its direction; each direction starts at 0; a counter at 18446744073709551615 refuses",
                  "retained", A_INH, h=["rp2.transitionAstV2 framePrecheck sequenceEqualsDirectionCounter/directionCounterLessThan",
                                        "chk2.step_frame"], g=["R3-G17"]),
    "frameType": R(T, T, "closed 26-name vocabulary (inherited 21 minus Coverage; plus CoverageV3, DependencySourceManifest, DependencySourceChunk, DependencySourceSeal, DependencySourceAccepted, NativeContextVerified); lawful per concrete phase",
                   "value-substituted", A_R129 + "; " + A_F92 + "; " + A_P3,
                   h=["p3.transitions first match; no row -> P3-34 FAULT", "ne.protocol3_run"]),
    "payload": R(M, M, "exact closed payload map selected by frameType, except FactBatch (negotiated token) and Unavailable (phase); payload <= maxFramePayloadBytes 67108864",
                 "retained", A_INH, h=["rp2.canonicalCbor decodeRule", "rp2.framing allocationRule"], g=["R3-G6"]),
}

FRAMES = {
    "Hello": F("HelloV3", "host-to-worker", False, "replaced", A_R122, r=HS + "HelloV3", rules=["P3-01"]),
    "HelloAck": F("HelloAckV3", "worker-to-host", False, "replaced", A_R122, r=HS + "HelloAckV3", rules=["P3-02"],
                  x="identityNegotiated = every identity token present in capabilities"),
    "OpenUniverse": F("OpenUniverseV3", "host-to-worker", False, "replaced", A_R128, r=ST + "OpenUniverseV3", rules=["P3-03"],
                      x="guard identityNegotiated=true; otherwise FAULT with sourceBytesSent=false"),
    "UniverseAccepted": F("UniverseAcceptedV3", "worker-to-host", False, "replaced", A_R128, r=ST + "UniverseAcceptedV3", rules=["P3-04"]),
    "SnapshotManifest": F("SnapshotManifestV2", "host-to-worker", False, "retained", A_INH, rules=["P3-05"]),
    "SnapshotFileChunk": F("SnapshotFileChunkV2", "host-to-worker", False, "retained", A_INH, rules=["P3-06"]),
    "SnapshotSeal": F("SnapshotSealV2", "host-to-worker", False, "retained", A_INH, rules=["P3-07"]),
    "SnapshotAccepted": F("SnapshotAcceptedV2", "worker-to-host", False, "retained", A_INH, rules=["P3-08", "P3-09", "P3-10"],
                          x="dependencyMode is true for every admitted OpenUniverseV3, so P3-08 -> READY_DEPENDENCY_MANIFEST; P3-09/P3-10 unreachable"),
    "PreparedOutputManifest": F("UNRESOLVED (inherited PreparedOutputManifestV2)", "host-to-worker", False, "unresolved", A_PREP,
                                rules=["P3-16"], g=["R3-G9"], cls="owner-contradictory", x="frame name retained; only when preparedOutputSetId is non-null"),
    "PreparedOutputChunk": F("UNRESOLVED (inherited PreparedOutputChunkV2)", "host-to-worker", False, "unresolved", A_PREP,
                             rules=["P3-17"], g=["R3-G9"], cls="owner-contradictory"),
    "PreparedOutputSeal": F("UNRESOLVED (inherited PreparedOutputSealV2)", "host-to-worker", False, "unresolved", A_PREP,
                            rules=["P3-18"], g=["R3-G9"], cls="owner-contradictory"),
    "PreparedOutputAccepted": F("UNRESOLVED (inherited PreparedOutputAcceptedV2)", "worker-to-host", False, "unresolved", A_PREP,
                                rules=["P3-19"], g=["R3-G9"], cls="owner-contradictory"),
    "Analyze": F("AnalyzeV2", "host-to-worker", False, "retained", A_INH + "; native-evidence.md:3024-3029 (unchanged Analyze frames)", rules=["P3-22"]),
    "FactBatch": F("FactBatchV2 unless target-attribution-v2 is in both Hello and HelloAck arrays; then FactBatchV3", "worker-to-host", False,
                   "retained", A_R123, r=FB, rules=["P3-23"], g=["R3-G6"]),
    "Coverage": F("frame renamed CoverageV3 with payload CoverageV3", "worker-to-host", False, "replaced", A_R129, r=ST + "CoverageV3",
                  rules=["P3-24"], x="frame name Coverage does not exist for rust-semantic major 3 (typescript-semantic keeps Coverage)"),
    "Unavailable": F("PreAnalyzeUnavailableV1 in WAIT_NATIVE_CONTEXT_VERIFIED (P3-21); UnavailableV3 in ANALYZING (P3-25)", "worker-to-host", True,
                     "replaced", A_R129 + "; " + A_PRE, r=ST + "UnavailableV3", rules=["P3-21", "P3-25"], g=["R3-G6", "R3-G17"]),
    "BudgetExhausted": F("BudgetExhaustedV3", "worker-to-host", True, "replaced", A_R129, r=ST + "BudgetExhaustedV3", rules=["P3-26"]),
    "Complete": F("CompleteV2", "worker-to-host", True, "retained", A_INH, rules=["P3-27"], g=["R3-G13"]),
    "ProviderFault": F("ProviderFaultV2", "worker-to-host", True, "retained", A_INH, rules=["P3-28"], g=["R3-G14"]),
    "Cancel": F("CancelV2", "host-to-worker", False, "retained", A_INH, rules=["P3-29"], g=["R3-G14", "R3-G17"]),
    "Cancelled": F("CancelledV2", "worker-to-host", True, "retained", A_INH, rules=["P3-30"], g=["R3-G14"]),
}

NEW_FRAMES = {
    "CoverageV3": F("CoverageV3", "worker-to-host", False, "new", A_R129, r=ST + "CoverageV3", rules=["P3-24"],
                    x="rename of inherited Coverage; next is stage-dependent ANALYZING_OR_READY_COMPLETE"),
    "DependencySourceManifest": F("DependencySourceManifestV3", "host-to-worker", False, "new", A_DS, r=NE + "DependencySourceManifestV3",
                                  rules=["P3-11"], g=["R3-G11"]),
    "DependencySourceChunk": F("UNNAMED (prose member list only)", "host-to-worker", False, "new", A_DS, rules=["P3-12"],
                               g=["R3-G3", "R3-G10"], cls="owner-missing"),
    "DependencySourceSeal": F("DependencySourceSealV3", "host-to-worker", False, "new", A_DS, r=NE + "DependencySourceSealV3", rules=["P3-13"]),
    "DependencySourceAccepted": F("UNNAMED ('exact seal echo'; shape of DependencySourceSealV3 by echo)", "worker-to-host", False, "new", A_DS,
                                  r=NE + "DependencySourceSealV3", rules=["P3-14", "P3-15"], g=["R3-G3", "R3-G10"], cls="owner-missing"),
    "NativeContextVerified": F("NativeContextVerifiedV1", "worker-to-host", False, "new", A_NCV, r=ST + "NativeContextVerifiedV1", rules=["P3-20"]),
}


def _hs(rec, m):
    return HS + rec + "/properties/" + m


def _st(rec, m):
    return ST + rec + "/properties/" + m


PAYLOADS = {
    "HelloV2": {
        "hostBuildId": R(T, T, IDTEXT, "replaced", A_R122, r=_hs("HelloV3", "hostBuildId"), m="unchanged", ts="definition IdentityText",
                         h=["wire.admit_hello: equals trusted hostBuildId"], g=["R3-G2"]),
        "expectedProtocolContractSha256": R(T, T, "DigestHex = raw SHA-256 of rust-provider-protocol.v2.json bytes 6308a98c...793b; authenticates the inherited base only",
                                            "replaced", A_R122, r=_hs("HelloV3", "expectedProtocolContractSha256"), m="unchanged",
                                            h=["wire.admit_hello: CONTRACT_PIN and CONTRACT_DIGEST", "hs.law expectedProtocolContractSha256"]),
        "expectedIdentity": R(M, M, "ExpectedRustIdentityV3 (6 members; protocolMajor 3)", "replaced", A_R122, r=_hs("HelloV3", "expectedIdentity"),
                              m="value-changed", h=["wire.admit_hello: identityFields equal the selected Plan rust-v1 row"]),
        "expectedCapabilities": R(M, A, "RustCapabilitiesV3: 4..13 unique RustCapabilityToken, strictly ascending UTF-8, four identity tokens (inherited: closed 6-member RustProviderCapabilityV2 map)",
                                  "replaced", A_R122, r=_hs("HelloV3", "expectedCapabilities"), m="value-changed",
                                  h=["wire.admit_hello: equals the UTF-8-sorted signed capability row", "hs.law capabilityArrays (order not JSON-Schema checkable)"],
                                  x="wire type changes map -> array"),
        "limits": R(M, M, "ProtocolLimitsV3: exactly 32 uint64 constants (24 inherited identical + 8 of §9.3)", "replaced", A_R122 + "; " + A_LIM,
                    r=_hs("HelloV3", "limits"), m="value-changed",
                    h=["rp2.limitsHandshake semantic and deterministic-CBOR byte equality", "wire.admit_hello: LIMITS"]),
    },
    "HelloAckV2": {
        "protocolMajor": R(U, U, "exactly 3 (inherited exactly 2); equals Hello expectedIdentity.protocolMajor", "replaced", A_R122,
                           r=_hs("HelloAckV3", "protocolMajor"), m="value-changed", h=["wire.admit_hello_ack: IDENTITY_ECHO"]),
        "providerBuildId": R(T, T, IDTEXT + "; exact Hello expectedIdentity value", "replaced", A_R122, r=_hs("HelloAckV3", "providerBuildId"),
                             m="unchanged", ts="successor schema (inherited text: exact Hello expectedIdentity value)", h=["wire.admit_hello_ack: IDENTITY_ECHO"]),
        "rustCommitHash": R(T, T, "DigestHex; exact Hello expectedIdentity value", "replaced", A_R122, r=_hs("HelloAckV3", "rustCommitHash"),
                            m="unchanged", ts="successor schema; resolved-inputs.v2 rust-v1 digestFields", h=["wire.admit_hello_ack: IDENTITY_ECHO"]),
        "hostTriple": R(T, T, IDTEXT + "; exact Hello expectedIdentity value", "replaced", A_R122, r=_hs("HelloAckV3", "hostTriple"),
                        m="unchanged", ts="successor schema", h=["wire.admit_hello_ack: IDENTITY_ECHO"]),
        "targetTriple": R(T, T, IDTEXT + "; exact Hello expectedIdentity value", "replaced", A_R122, r=_hs("HelloAckV3", "targetTriple"),
                          m="unchanged", ts="successor schema", h=["wire.admit_hello_ack: IDENTITY_ECHO"]),
        "sysrootDigest": R(T, T, "DigestHex; exact Hello expectedIdentity value", "replaced", A_R122, r=_hs("HelloAckV3", "sysrootDigest"),
                           m="unchanged", ts="successor schema; rust-v1 digestFields", h=["wire.admit_hello_ack: IDENTITY_ECHO"]),
        "capabilities": R(M, A, "RustCapabilitiesV3; exact echo of Hello expectedCapabilities (same members, same order)", "replaced", A_R122,
                          r=_hs("HelloAckV3", "capabilities"), m="value-changed", ts="successor schema (inherited: exact recursive equality with Hello record)",
                          h=["wire.admit_hello_ack: CAPABILITY_ECHO"], x="wire type changes map -> array"),
    },
    "OpenUniverseV2": {
        "executionId": R(T, T, IDTEXT + " (startup ExecutionIdText minLength 1; IdentityText rules by admission); the host value is exec1_[0-9a-f]{32} (identity-and-evidence.md:63-72), a subset",
                         "replaced", A_R128 + "; " + A_ECHO, r=_st("OpenUniverseV3", "executionId"), m="unchanged", ts="field text 'IdentityText exact AttemptRecord value'",
                         h=["start.admit_open_universe: exact AttemptRecord value; NFC + IdentityText"], g=["R3-G2"]),
        "snapshotId": R(T, T, SNAP2 + " (inherited ^snap1:sha256:[0-9a-f]{64}$)", "replaced", A_R128, r=_st("OpenUniverseV3", "snapshotId"),
                        m="value-changed", ts="definition SnapshotId -> SnapshotId2", h=["start.admit_open_universe: equals the verified Plan snapshot2"]),
        "planId": R(T, T, PLAN2 + " (inherited ^plan1:sha256:[0-9a-f]{64}$)", "replaced", A_R128, r=_st("OpenUniverseV3", "planId"),
                    m="value-changed", ts="definition PlanId -> PlanId2", h=["start.admit_open_universe: equals the verified plan2"]),
        "planIntentCommitment": R(T, T, "Sha256Text; exact AttemptRecord/ExecutionPlan value", "replaced", A_R128, r=_st("OpenUniverseV3", "planIntentCommitment"),
                                  m="unchanged", h=["start.admit_open_universe: OPEN_UNIVERSE_CORRELATION"]),
        "providerId": R(T, T, "const rust-semantic", "replaced", A_R128, r=_st("OpenUniverseV3", "providerId"), m="unchanged"),
        "universe": R(M, M, "RustSemanticUniverseV2: 21-member rust-v1 map, protocolMajor 3, resolvedInputs RustUniverseV2ResolvedInputs",
                      "replaced", A_R128 + "; " + A_R130, r=_st("OpenUniverseV3", "universe"), m="value-changed",
                      h=["start.admit_open_universe: handshakeJoin (6 members) equals HelloV3.expectedIdentity; nativeContextId suffix in plan.nativeContextDigests"]),
        "repositoryResolution": R(M, M, "RepositoryResolutionV3 {dependencySourceSetId, preparedOutputSetId|null, authorizationId|null, workerExecutesRepositoryCode:false, effects|null}",
                                  "replaced", A_R118 + "; native-evidence.md:2886-2888, 3183-3187", r=_st("OpenUniverseV3", "repositoryResolution"),
                                  m="value-changed", h=["start.admit_open_universe: REPOSITORY_RESOLUTION_JOIN", "ne.protocol3_open_universe_event: derived dependencyMode/preparedMode"]),
    },
    "UniverseAcceptedV2": {
        "executionId": R(T, T, "exact recursive echo of OpenUniverse", "replaced", A_R128, r=_st("UniverseAcceptedV3", "executionId"), m="unchanged",
                         ts=ECHO + "OpenUniverse (inherited fields.all)", h=["start.admit_universe_accepted: UNIVERSE_ACCEPTED_ECHO"]),
        "snapshotId": R(T, T, SNAP2 + " echo", "replaced", A_R128, r=_st("UniverseAcceptedV3", "snapshotId"), m="value-changed",
                        ts=ECHO + "OpenUniverse", h=["start.admit_universe_accepted: UNIVERSE_ACCEPTED_ECHO"]),
        "planId": R(T, T, PLAN2 + " echo", "replaced", A_R128, r=_st("UniverseAcceptedV3", "planId"), m="value-changed",
                    ts=ECHO + "OpenUniverse", h=["start.admit_universe_accepted: UNIVERSE_ACCEPTED_ECHO"]),
        "providerId": R(T, T, "const rust-semantic echo", "replaced", A_R128, r=_st("UniverseAcceptedV3", "providerId"), m="unchanged",
                        ts=ECHO + "OpenUniverse"),
        "universe": R(M, M, "RustSemanticUniverseV2 echo (no digest-only echo)", "replaced", A_R128, r=_st("UniverseAcceptedV3", "universe"),
                      m="value-changed", ts=ECHO + "OpenUniverse", h=["start.admit_universe_accepted: UNIVERSE_ACCEPTED_ECHO"]),
        "repositoryResolution": R(M, M, "RepositoryResolutionV3 echo", "replaced", A_R128, r=_st("UniverseAcceptedV3", "repositoryResolution"),
                                  m="value-changed", ts=ECHO + "OpenUniverse", h=["start.admit_universe_accepted: UNIVERSE_ACCEPTED_ECHO"]),
    },
    "SnapshotManifestV2": {
        "snapshotId": R(T, T, SNAP2 + " via exact OpenUniverse echo", "value-substituted", A_ECHO + " (lists SnapshotManifest snapshotId)",
                        r=ST + "SnapshotId2", ts=ECHO + "OpenUniverse.snapshotId"),
        "manifestSha256": R(T, T, "DigestHex = lowercase hex SHA-256(deterministic-CBOR(entries)); no domain, no prefix", "retained", A_INH,
                            ts="rust2 $.commitments.snapshotManifest", h=["rp2.commitments snapshotManifest: worker recomputes"],
                            x="the Rust owner states this recipe; contrast TS2-G10 and proposal P-3"),
        "entries": R(A, A, "items SnapshotEntryV2; 1..maxSnapshotEntries 200000; strict ascending unique CanonicalPath (UTF-8 bytes)", "retained", A_INH,
                     h=["rp2.limitPolicy allocation", "rp2.requestProjection snapshot"]),
    },
    "SnapshotFileChunkV2": {
        "snapshotId": R(T, T, SNAP2 + " via exact manifest/OpenUniverse echo", "value-substituted", A_ECHO + " (transitive; SnapshotFileChunk not enumerated)",
                        r=ST + "SnapshotId2", ts=ECHO + "SnapshotManifest.snapshotId", g=["R3-G16"]),
        "path": R(T, T, "CanonicalPath of one kind=file manifest entry, in manifest order", "retained", A_INH,
                  ts=ECHO + "SnapshotEntryV2.path (field text 'path/index/offset exact contiguous manifest order')"),
        "chunkIndex": R(U, U, "contiguous from 0 per path", "retained", A_INH, ts=ARITH, g=["R3-G15"]),
        "byteOffset": R(U, U, "exact cumulative prior chunk bytes of that path (checked add)", "retained", A_INH, ts=ARITH,
                        h=["rp2.limitPolicy arithmetic"], g=["R3-G15"]),
        "bytes": R(B, B, "non-empty; 1..maxSnapshotChunkBytes 1048576", "retained", A_INH, h=["rp2.limitPolicy allocation: length before allocation"],
                   g=["R3-G1"]),
    },
    "SnapshotSealV2": {
        "snapshotId": R(T, T, SNAP2 + " echo", "value-substituted", A_ECHO + " (lists SnapshotSeal snapshotId)", r=ST + "SnapshotId2", ts=ECHO + "manifest"),
        "manifestSha256": R(T, T, "DigestHex echo of SnapshotManifest.manifestSha256", "retained", A_INH, ts=ECHO + "manifest (fields.all 'exact checked aggregates')"),
        "entryCount": R(U, U, "exact entries length (<= 200000)", "retained", A_INH, ts=ARITH, g=["R3-G15"]),
        "totalFileBytes": R(U, U, "exact checked sum of file byteLength; <= maxSnapshotTotalFileBytes 8589934592", "retained", A_INH, ts=ARITH,
                            h=["rp2.limitPolicy aggregateAccounting"], g=["R3-G15"]),
        "totalChunkCount": R(U, U, "exact emitted chunk count", "retained", A_INH, ts=ARITH, g=["R3-G15"]),
    },
    "SnapshotAcceptedV2": {
        "snapshotId": R(T, T, SNAP2 + " echo of SnapshotSeal", "value-substituted", A_ECHO + " (lists SnapshotAccepted snapshotId)", r=ST + "SnapshotId2", ts=ECHO + "seal"),
        "manifestSha256": R(T, T, "DigestHex; exact SnapshotSeal value after byte/digest/VFS validation", "retained", A_INH, ts=ECHO + "seal"),
        "entryCount": R(U, U, "exact SnapshotSeal value", "retained", A_INH, ts=ECHO + "seal; " + ARITH, g=["R3-G15"]),
        "totalFileBytes": R(U, U, "exact SnapshotSeal value", "retained", A_INH, ts=ECHO + "seal; " + ARITH, g=["R3-G15"]),
        "totalChunkCount": R(U, U, "exact SnapshotSeal value", "retained", A_INH, ts=ECHO + "seal; " + ARITH, g=["R3-G15"]),
    },
    "PreparedOutputManifestV2": {
        "planId": R(T, T, PLAN2 + " via exact OpenUniverse echo", "value-substituted", A_ECHO + " (lists PreparedOutputManifest planId)", r=ST + "PlanId2",
                    ts=ECHO + "OpenUniverse.planId", g=["R3-G9"]),
        "manifestSha256": R(T, T, "inherited: hex SHA-256(deterministic-CBOR(entries)) over PreparedOutputEntryV2 entries", "unresolved", A_PREP,
                            cls="owner-contradictory", ts="rust2 $.commitments.preparedOutputManifest", g=["R3-G9"]),
        "entries": R(A, A, "inherited: PreparedOutputEntryV2[] 0..maxPreparedOutputEntries 256, contiguous ordinal, rust-v1 row order", "unresolved", A_PREP,
                     cls="owner-contradictory", g=["R3-G9"], h=["chk2.validate_prepared (inherited v2 law)"]),
    },
    "PreparedOutputChunkV2": {
        "planId": R(T, T, "inherited echo; plan2 substitution not enumerated for this frame", "unresolved", A_PREP, cls="owner-missing",
                    ts=ECHO + "manifest", g=["R3-G9", "R3-G16"]),
        "outputOrdinal": R(U, U, "inherited: manifest outputOrdinal, in ordinal/chunk/offset order", "unresolved", A_PREP, cls="owner-contradictory", ts=ARITH, g=["R3-G9"]),
        "chunkIndex": R(U, U, "inherited: contiguous from 0 per ordinal", "unresolved", A_PREP, cls="owner-contradictory", ts=ARITH, g=["R3-G9"]),
        "byteOffset": R(U, U, "inherited: exact cumulative prior bytes", "unresolved", A_PREP, cls="owner-contradictory", ts=ARITH, g=["R3-G9"]),
        "bytes": R(B, B, "inherited: non-empty; 1..maxPreparedOutputChunkBytes 1048576", "unresolved", A_PREP, cls="owner-contradictory", g=["R3-G9", "R3-G1"]),
    },
    "PreparedOutputSealV2": {
        "planId": R(T, T, "inherited echo; plan2 substitution not enumerated for this frame", "unresolved", A_PREP, cls="owner-missing",
                    ts=ECHO + "manifest", g=["R3-G9", "R3-G16"]),
        "manifestSha256": R(T, T, "inherited: echo of manifest", "unresolved", A_PREP, cls="owner-contradictory", ts=ECHO + "manifest", g=["R3-G9"]),
        "entryCount": R(U, U, "inherited: exact checked aggregate", "unresolved", A_PREP, cls="owner-contradictory", ts=ARITH, g=["R3-G9"]),
        "totalBlobBytes": R(U, U, "inherited: exact checked sum; <= maxPreparedOutputTotalBlobBytes 1073741824", "unresolved", A_PREP,
                            cls="owner-contradictory", ts=ARITH, g=["R3-G9"]),
        "totalChunkCount": R(U, U, "inherited: exact checked aggregate", "unresolved", A_PREP, cls="owner-contradictory", ts=ARITH, g=["R3-G9"]),
    },
    "PreparedOutputAcceptedV2": {
        "planId": R(T, T, PLAN2 + " echo", "value-substituted", A_ECHO + " (lists PreparedOutputAccepted planId)", r=ST + "PlanId2",
                    ts=ECHO + "seal", g=["R3-G9"]),
        "manifestSha256": R(T, T, "inherited: exact PreparedOutputSeal value", "unresolved", A_PREP, cls="owner-contradictory", ts=ECHO + "seal", g=["R3-G9"]),
        "entryCount": R(U, U, "inherited: exact PreparedOutputSeal value", "unresolved", A_PREP, cls="owner-contradictory", ts=ECHO + "seal", g=["R3-G9"]),
        "totalBlobBytes": R(U, U, "inherited: exact PreparedOutputSeal value", "unresolved", A_PREP, cls="owner-contradictory", ts=ECHO + "seal", g=["R3-G9"]),
        "totalChunkCount": R(U, U, "inherited: exact PreparedOutputSeal value", "unresolved", A_PREP, cls="owner-contradictory", ts=ECHO + "seal", g=["R3-G9"]),
    },
    "AnalyzeV2": {
        "analysisOrdinal": R(U, U, "uint64; one Analyze per child (protocolIdentity.oneAnalyzePerChild); no exact value stated (TS2 is exactly 0)",
                             "retained", A_INH, ts="derived: RustFactBatchV2Vector/fact-batch.3/DispatchBindingV1 analysisOrdinal echoes are Uint64",
                             h=["dispatch: expectedAnalysisOrdinal"]),
        "executionId": R(T, T, IDTEXT + "; exact OpenUniverse echo", "retained", A_ECHO + " (lists Analyze)", ts=ECHO + "OpenUniverse.executionId"),
        "snapshotId": R(T, T, SNAP2 + " echo", "value-substituted", A_ECHO + " (lists Analyze)", r=ST + "SnapshotId2", ts=ECHO + "OpenUniverse.snapshotId"),
        "planId": R(T, T, PLAN2 + " echo", "value-substituted", A_ECHO + " (lists Analyze)", r=ST + "PlanId2", ts=ECHO + "OpenUniverse.planId"),
        "stages": R(A, A, "items StageRequestV2; 1..maxAnalyzeStages 256; every selected stage (kind fact-derivation, operator semantic-provider, providerId rust-semantic) in exact verified ExecutionPlan order",
                    "retained", A_INH + "; " + A_DISPATCH, h=["rp2.planAndDomainProjection selectedStageRule", "rp2.transitionAstV2 T015 stageCount"]),
    },
    "FactBatchV2": {
        "analysisOrdinal": R(U, U, "exact Analyze analysisOrdinal echo", "retained", A_R123, r=_hs("RustFactBatchV2Vector", "analysisOrdinal"),
                             ts="successor vector (no v2 field text)", h=["dispatch: == expectedAnalysisOrdinal", "wire.admit_fact_batch: CORRELATION"]),
        "stageId": R(T, T, STAGEID, "retained", A_R123 + "; " + A_DISPATCH, r=_hs("RustFactBatchV2Vector", "stageId"),
                     ts="successor vector + DispatchBindingV1.expectedStageId maxLength 255", h=["dispatch: == expectedStageId"], g=["R3-G2"]),
        "batchIndex": R(U, U, "contiguous from 0 per stage", "retained", A_R123, r=_hs("RustFactBatchV2Vector", "batchIndex"),
                        ts="successor vector", h=["rp2.transitionAstV2 T016 nextBatchIndex", "dispatch: == expectedBatchIndex"]),
        "candidates": R(A, A, "items FactCandidateV1; 1..maxFactBatchCandidates 4096; candidateOrdinal contiguous from 0 across the stage's batches",
                        "retained", A_R123, r=_hs("RustFactBatchV2Vector", "candidates"),
                        h=["rp2.transitionAstV2 T016 firstCandidateOrdinal/candidateCount", "dispatch: expectedFirstCandidateOrdinal",
                           "wire.admit_fact_batch: BATCH_CANDIDATE_CAP", "rp2.limitPolicy candidateSpoolAccounting"],
                        x="vector items are fact-batch.3 JSON-vector candidates (hex transcription), not wire candidates"),
    },
    "CoverageV2": {
        "analysisOrdinal": R(U, U, "Uint64 (not const)", "replaced", A_R129, r=_st("CoverageV3", "analysisOrdinal"), m="unchanged", ts="successor schema"),
        "stageId": R(T, T, "StageIdText; current requested stage; attributes every entry", "replaced", A_R129, r=_st("CoverageV3", "stageId"),
                     m="unchanged", ts="successor schema", h=["start.admit_coverage_frame: COVERAGE_STAGE"]),
        "entries": R(A, A, "items CoverageResultV3; schema 1..4096; count == len(requestedCoverageDomain) <= 256; entries[i] answers keys[i]",
                     "replaced", A_R129, r=_st("CoverageV3", "entries"), m="value-changed",
                     h=["start.admit_coverage_frame: COVERAGE_BIJECTION/COVERAGE_KEY_CORRESPONDENCE", "ne.admit_coverage_result_v3"], g=["R3-G8"]),
        "coverageCommitment": R(T, T, "Sha256Text over the ordered CoverageResultV3 entries; domain not named by field text", "replaced", A_R129,
                                r=_st("CoverageV3", "coverageCommitment"), m="value-changed", cls="owner-missing", g=["R3-G12"]),
    },
    "UnavailableV2": {
        "analysisOrdinal": R(U, U, "Uint64", "replaced", A_R129, r=_st("UnavailableV3", "analysisOrdinal"), m="unchanged", ts="successor schema"),
        "affectedStageIds": R(A, A, "items StageIdText; all requested stageIds in request order; schema minItems 1, no maxItems (derived <= 256)",
                              "replaced", A_R129, r=_st("UnavailableV3", "affectedStageIds"), m="unchanged",
                              ts="successor schema description '(inherited)'; no v2 field text", g=["R3-G8"]),
        "reason": R(T, T, "enum capability-missing|dependency-source-incomplete|generated-cfg-unavailable|identity-version-mismatch|prepared-output-not-inert|prepared-output-stale|semantic-universe-incomplete|snapshot-resolution-input-missing|unsupported-compiler-mode (inherited 4; never native-context-mismatch)",
                    "replaced", A_R118 + "; " + A_R129 + "; native-evidence.md:2889-2891", r=_st("UnavailableV3", "reason"), m="value-changed",
                    h=["start.admit_unavailable: pre-Analyze reason refused after Analyze"], g=["R3-G7"]),
        "coverage": R(A, A, "items CoverageResultV3 unknown/provider-unavailable, stage-major/key order; schema minItems 0, no maxItems (derived 1..65536)",
                      "replaced", A_R129, r=_st("UnavailableV3", "coverage"), m="value-changed", h=["ne.admit_coverage_result_v3"], g=["R3-G8"]),
        "coverageCommitment": R(T, T, "Sha256Text over coverage; domain not named by field text", "replaced", A_R129, r=_st("UnavailableV3", "coverageCommitment"),
                                m="value-changed", cls="owner-missing", g=["R3-G12"]),
    },
    "BudgetExhaustedV2": {
        "analysisOrdinal": R(U, U, "Uint64", "replaced", A_R129, r=_st("BudgetExhaustedV3", "analysisOrdinal"), m="unchanged", ts="successor schema"),
        "triggerStageId": R(T, T, "StageIdText; one requested stage whose budget was exhausted", "replaced", A_R129, r=_st("BudgetExhaustedV3", "triggerStageId"),
                            m="unchanged", ts="successor schema", h=["rp2.transitionAstV2 T020 budgetMatchesCurrentStage"]),
        "unit": R(T, T, "enum work-units|bytes|items; equals the stage budget unit (never milliseconds)", "replaced", A_R129, r=_st("BudgetExhaustedV3", "unit"),
                  m="unchanged", h=["rp2.deterministicBudget"]),
        "limit": R(U, U, "exact requested stage budget limit (C-2 stageBudgetV1 1..9223372036854775807)", "replaced", A_R129, r=_st("BudgetExhaustedV3", "limit"),
                   m="unchanged", ts="successor schema; c2 v3 $.planIntent.wireTypes.stageBudgetV1"),
        "observed": R(U, U, "uint64; relation to limit not stated by the v2 grammar", "replaced", A_R129, r=_st("BudgetExhaustedV3", "observed"),
                      m="unchanged", ts="successor schema", cls="owner-missing", h=["rp2.deterministicBudget checked increments"], g=["R3-G14"]),
        "coverage": R(A, A, "items CoverageResultV3 unknown/budget-exhausted, stage-major/key order; schema minItems 0, no maxItems", "replaced", A_R129,
                      r=_st("BudgetExhaustedV3", "coverage"), m="value-changed", h=["ne.admit_coverage_result_v3"], g=["R3-G8"]),
        "coverageCommitment": R(T, T, "Sha256Text over coverage; domain not named by field text", "replaced", A_R129,
                                r=_st("BudgetExhaustedV3", "coverageCommitment"), m="value-changed", cls="owner-missing", g=["R3-G12"]),
    },
    "CompleteV2": {
        "analysisOrdinal": R(U, U, "exact Analyze analysisOrdinal", "retained", A_INH, ts="derived (analysisOrdinal echoes are Uint64)"),
        "stageResults": R(A, A, "items StageResultV2; exactly one per Analyze stage in request order (<= 256)", "retained", A_INH,
                          h=["rp2.candidateAtomicity admitOn valid Complete"], g=["R3-G13"]),
        "factStreamCommitment": R(T, T, "Sha256Text; domain opensip.rust-provider.fact-stream.v2 over stage-major FactCandidateV1 values, whichever payload carried them",
                                  "retained", A_R123 + "; provider-handshake law commitments.rust-semantic", ts="rust2 $.commitments.factStream",
                                  h=["rp2.commitments factStream"]),
        "coverageStreamCommitment": R(T, T, "Sha256Text; domain opensip.rust-provider.coverage-stream.v2 over stage-major CoverageResultV3 values",
                                      "value-substituted", A_R129, ts="rust2 $.commitments.coverageStream (field name)", h=["rp2.commitments coverageStream"],
                                      g=["R3-G12"]),
    },
    "ProviderFaultV2": {
        "executionId": R(X, X, "type and nullability unstated (fault is lawful before OpenUniverse)", "retained", A_INH, cls="owner-missing", ts="UNSTATED", g=["R3-G14"]),
        "analysisOrdinal": R(X, X, "type and nullability unstated (fault is lawful before Analyze)", "retained", A_INH, cls="owner-missing", ts="UNSTATED", g=["R3-G14"]),
        "phase": R(X, X, "no field text; vocabulary unstated", "retained", A_INH + "; " + A_R118, cls="owner-missing", ts="UNSTATED", g=["R3-G14"]),
        "faultKind": R(T, T, "enum compiler-crash|internal-invariant|input-rejected", "retained", A_INH),
        "detailCode": R(X, X, "diagnostic only, never D9 authority; normalizes to provider-protocol", "retained", A_INH, cls="owner-missing", ts="UNSTATED",
                        h=["rp2.responseProjection typedFault"], g=["R3-G14"]),
    },
    "CancelV2": {
        "executionId": R(X, X, "type and nullability unstated (Cancel is lawful before OpenUniverse)", "retained", A_INH, cls="owner-missing", ts="UNSTATED", g=["R3-G14"]),
        "analysisOrdinal": R(X, X, "type and nullability unstated", "retained", A_INH, cls="owner-missing", ts="UNSTATED", g=["R3-G14"]),
        "reason": R(T, T, "const user-interrupt", "retained", A_INH),
    },
    "CancelledV2": {
        "executionId": R(X, X, "exact Cancel echo; type unstated", "retained", A_INH, cls="owner-missing", ts=ECHO + "Cancel", g=["R3-G14"]),
        "analysisOrdinal": R(X, X, "exact Cancel echo; type unstated", "retained", A_INH, cls="owner-missing", ts=ECHO + "Cancel", g=["R3-G14"]),
        "observedPhase": R(T, T, "exact concrete phase at Cancel receipt; phase vocabulary is the 22 major-3 phases (superseded 18); lawful subset unstated",
                           "value-substituted", A_R118 + "; native-evidence.md:3302", cls="owner-missing", ts="field text; protocol3-transitions.v1.json $.phases",
                           g=["R3-G14"]),
    },
}

STRING_DEFS = {
    "IdentityText": R(T, T, IDTEXT, "retained", A_INH, r=HS + "IdentityText", h=["rp2.schemaLanguage text byte bound"], g=["R3-G2"]),
    "DigestHex": R(T, T, "^[0-9a-f]{64}$ (schema-native end anchor (?![\\s\\S]))", "retained", A_INH, r=HS + "DigestHex"),
    "Sha256Text": R(T, T, "^sha256:[0-9a-f]{64}$", "retained", A_INH, r=HS + "Sha256Text"),
    "SnapshotId": R(T, T, SNAP2 + " (inherited ^snap1:sha256:[0-9a-f]{64}$)", "replaced", A_R128, r=ST + "SnapshotId2", m="value-changed"),
    "PlanId": R(T, T, PLAN2 + " (inherited ^plan1:sha256:[0-9a-f]{64}$)", "replaced", A_R128, r=ST + "PlanId2", m="value-changed"),
    "CanonicalPath": R(T, T, "NFC slash-relative path; no leading slash, backslash, NUL, drive prefix, empty, dot or dot-dot segment; no schema-native equivalent (native-evidence CanonicalPath pattern is weaker)",
                       "retained", A_INH, h=["rp2.schemaLanguage text rule"], g=["R3-G2"]),
}

V2_LIMITS = [("maxFramePayloadBytes", 67108864), ("maxSnapshotChunkBytes", 1048576), ("maxSnapshotEntries", 200000),
             ("maxSnapshotTotalFileBytes", 8589934592), ("maxPreparedOutputChunkBytes", 1048576), ("maxPreparedOutputEntries", 256),
             ("maxPreparedOutputTotalBlobBytes", 1073741824), ("maxAnalyzeStages", 256), ("maxRelationsPerStage", 64),
             ("maxSubjectsPerStage", 256), ("maxRequestedCoverageKeysPerStage", 256), ("maxFactBatchCandidates", 4096),
             ("maxFactCandidatesTotal", 1000000), ("maxCanonicalRelationPayloadBytes", 1048576), ("maxCoverageEntriesPerFrame", 4096),
             ("maxCandidateSpoolBytes", 1073741824), ("maxRequestPayloadBytesTotal", 9663676416), ("maxResponsePayloadBytesTotal", 1073741824),
             ("maxRequestFrames", 1000000), ("maxResponseFrames", 1000000), ("maxStderrBytes", 262144), ("maxScratchBytes", 2147483648),
             ("cancellationGraceMilliseconds", 5000), ("normalExitGraceMilliseconds", 5000)]
NEW_LIMITS = [("maxDependencySourcePackages", 4096), ("maxDependencySourceEntries", 1000000), ("maxDependencySourceTotalBytes", 8589934592),
              ("maxDependencySourceChunkBytes", 1048576), ("maxUnresolvedEdgesPerStage", 1000000), ("maxCfgSets", 4),
              ("maxExpansionRows", 1000000), ("maxGeneratedFileRows", 1000000)]

RECORD_DEFS = {
    "ProtocolLimitsV2": {name: R(U, U, "const %d; identical in ProtocolLimitsV3" % value, "replaced", A_R118 + "; " + A_LIM,
                                 r=HS + "ProtocolLimitsV3/properties/" + name, m="unchanged", ts="rule 'every member is uint64' + top-level $.limits",
                                 h=["rp2.limitsHandshake", "rp2.limitPolicy"]) for name, value in V2_LIMITS},
    "ExpectedRustIdentityV2": {
        "protocolMajor": R(U, U, "exactly 3 (inherited exactly 2)", "replaced", A_R122, r=_hs("ExpectedRustIdentityV3", "protocolMajor"), m="value-changed"),
        "providerBuildId": R(T, T, IDTEXT + "; selected Plan rust-v1 row value", "replaced", A_R122, r=_hs("ExpectedRustIdentityV3", "providerBuildId"),
                             m="unchanged", ts="successor schema (inherited fields.remaining 'exact verified release/rust-v1 identity')"),
        "rustCommitHash": R(T, T, "DigestHex", "replaced", A_R122, r=_hs("ExpectedRustIdentityV3", "rustCommitHash"), m="unchanged", ts="successor schema; rust-v1 digestFields"),
        "hostTriple": R(T, T, IDTEXT, "replaced", A_R122, r=_hs("ExpectedRustIdentityV3", "hostTriple"), m="unchanged", ts="successor schema"),
        "targetTriple": R(T, T, IDTEXT, "replaced", A_R122, r=_hs("ExpectedRustIdentityV3", "targetTriple"), m="unchanged", ts="successor schema"),
        "sysrootDigest": R(T, T, "DigestHex", "replaced", A_R122, r=_hs("ExpectedRustIdentityV3", "sysrootDigest"), m="unchanged", ts="successor schema; rust-v1 digestFields"),
    },
    "RustProviderCapabilityV2": {name: R(text_type, None, "member removed: the record is replaced by the RustCapabilitiesV3 token array", "replaced", A_R122,
                                         r=HS + "RustCapabilitiesV3", m="removed", ts="resolved-inputs-rust-provider-join.v2 $.capabilityHandshakeBinding.fields")
                                 for name, text_type in [("providerId", T), ("language", T), ("providerVersionSource", T), ("toolchainIdentitySource", T),
                                                         ("relations", M), ("platformIds", A)]},
    "ToolPathV2": {name: R(wt, None, "no Rust3 provider-wire carrier: RepositoryResolutionV3 is closed without toolPaths (the shape survives only as C-2 grant parameters, off this wire)",
                           "removed", A_R118 + "; native-evidence.md:2886-2888", m="removed", ts="field text")
                   for name, wt in [("artifact_id", T), ("bundle_relative_path", T), ("file_sha256", T), ("role", T)]},
    "RepositoryResolutionV2": {
        "mode": R(T, None, "enum disabled|prepared; removed (prepared mode is now preparedOutputSetId != null, host-derived)", "replaced", A_R118,
                  r=NE + "RepositoryResolutionV3", m="removed", ts="variants text"),
        "grantId": R("UTF-8-NFC-text|null", None, "removed (no stated successor; authorizationId is a new member, not declared a rename)", "replaced", A_R118,
                     r=NE + "RepositoryResolutionV3", m="removed", ts="variants text"),
        "projectId": R(T, None, "removed", "replaced", A_R118, r=NE + "RepositoryResolutionV3", m="removed", ts="resolved-inputs-rust-provider-join.v2 providerRequestProjection"),
        "network": R(BOOL, "definite-text-keyed-map|null", "false; replaced by disclosed effects copied from AuthorizedExecutionV2 (effects.network is an EffectV1)",
                     "replaced", A_R118 + "; native-evidence.md:2887-2888", r=NE + "RepositoryResolutionV3/properties/effects", m="moved", ts="variants text"),
        "buildScriptOutputs": R(A, None, "removed (rust-v1 rows superseded)", "replaced", A_R118 + "; " + A_R130, r=NE + "RepositoryResolutionV3", m="removed", ts="variants text"),
        "procMacroOutputs": R(A, None, "removed (rust-v1 rows superseded)", "replaced", A_R118 + "; " + A_R130, r=NE + "RepositoryResolutionV3", m="removed", ts="variants text"),
        "toolPaths": R(A, None, "removed", "replaced", A_R118, r=NE + "RepositoryResolutionV3", m="removed", ts="variants text"),
        "preparedOutputManifestCommitment": R("UTF-8-NFC-text|null", None, "removed", "replaced", A_R118, r=NE + "RepositoryResolutionV3", m="removed",
                                              ts="variants text; resolved-inputs-rust-provider-join.v2 preparedOutputManifestBinding.manifestCommitment"),
    },
    "SnapshotEntryV2": {
        "path": R(T, T, "CanonicalPath; entries strict ascending unique by UTF-8 bytes", "retained", A_INH, ts="SnapshotManifestV2.fields.entries"),
        "kind": R(T, T, "enum file|symlink", "retained", A_INH, ts="variants keys"),
        "byteLength": R("uint64|null", "uint64|null", "file: non-null content length; symlink: null", "retained", A_INH,
                        ts=ARITH + "; subjectsAlgorithm 'byteLength is greater than zero'", g=["R3-G15"]),
        "contentSha256": R("UNSTATED|null", "UNSTATED|null", "file: non-null digest (form unstated; enters SubjectV2.subjectId preimage); symlink: null",
                           "retained", A_INH, cls="owner-missing", ts="UNSTATED (variants give nullability only)", g=["R3-G15"]),
        "executable": R("UNSTATED|null", "UNSTATED|null", "file: non-null; symlink: null", "retained", A_INH, cls="owner-missing",
                        ts="UNSTATED (variants give nullability only)", g=["R3-G15"]),
        "targetBytes": R("UNSTATED|null", "UNSTATED|null", "symlink: non-empty target (requestProjection.snapshot 'symlink target bytes remain in the manifest'); file: null",
                         "retained", A_INH, cls="owner-missing", ts="UNSTATED (CBOR type not stated)", g=["R3-G15", "R3-G1"]),
    },
    "PreparedOutputBlobV2": {
        "kind": R(T, T, "inherited enum build-script|proc-macro (PreparedOutputRowV3 kinds differ)", "unresolved", A_PREP, cls="owner-contradictory", ts="variants keys", g=["R3-G9"]),
        "ownerId": R(T, T, "inherited: rust-v1 row packageId or crateId (rows superseded)", "unresolved", A_PREP, cls="owner-contradictory", ts="variants text", g=["R3-G9"]),
        "configuration": R(A, A, "inherited: exact rust-v1 cfg array or []", "unresolved", A_PREP, cls="owner-contradictory", ts="variants text", g=["R3-G9"]),
        "content": R(B, B, "inherited: exact byte string, possibly empty", "unresolved", A_PREP, cls="owner-contradictory", g=["R3-G9", "R3-G1"]),
    },
    "PreparedOutputEntryV2": {
        "outputOrdinal": R(U, U, "inherited: contiguous from 0; build-script rows then proc-macro rows", "unresolved", A_PREP, cls="owner-contradictory", g=["R3-G9"]),
        "kind": R(T, T, "inherited: build-script|proc-macro", "unresolved", A_PREP, cls="owner-contradictory", ts="PreparedOutputBlobV2 variants", g=["R3-G9"]),
        "planRow": R(M, M, "inherited: exact rust-v1 row (superseded by rust-v2)", "unresolved", A_PREP, cls="owner-contradictory", g=["R3-G9"]),
        "logicalPath": R(T, T, "inherited: .opensip/prepared/v2/<ordinal>-<planRow.outputDigest>.blob", "unresolved", A_PREP, cls="owner-contradictory", g=["R3-G9"]),
        "blobByteLength": R(U, U, "inherited: exact deterministic-CBOR blob length", "unresolved", A_PREP, cls="owner-contradictory", ts=ARITH, g=["R3-G9"]),
        "blobSha256": R(T, T, "inherited: DigestHex of exact blob bytes == planRow.outputDigest", "unresolved", A_PREP, cls="owner-contradictory", g=["R3-G9"]),
        "contentByteLength": R(U, U, "inherited: exact content length", "unresolved", A_PREP, cls="owner-contradictory", ts=ARITH, g=["R3-G9"]),
        "contentSha256": R(T, T, "inherited: SHA-256 of exact content bytes", "unresolved", A_PREP, cls="owner-contradictory", g=["R3-G9"]),
    },
    "SubjectV2": {
        "subjectOrdinal": R(U, U, "contiguous from 0 in path order", "retained", A_INH, ts="rust2 subjectsAlgorithm", h=["chk2.derive_subjects"]),
        "subjectId": R(T, T, "'rust-file:sha256:' + hex(SHA-256(UTF8(opensip.rust-provider.subject.v2) || 0x00 || deterministic-CBOR({snapshotId, path, contentSha256, byteLength}))); the snapshotId input becomes snapshot2 text",
                       "value-substituted", A_INH + "; " + A_R128 + " (SnapshotId superseded)", cls="owner-missing", ts="rust2 subjectsAlgorithm",
                       h=["chk2.derive_subjects"], g=["R3-G16"]),
        "path": R(T, T, "CanonicalPath of a non-empty .rs file entry", "retained", A_INH, ts="rust2 subjectsAlgorithm"),
        "startByte": R(U, U, "exactly 0", "retained", A_INH, ts="rust2 subjectsAlgorithm"),
        "endByte": R(U, U, "entry byteLength (> 0)", "retained", A_INH, ts="rust2 subjectsAlgorithm"),
    },
    "CoverageKeyV2": {
        "relation": R(T, T, "one planStage.relations member (C-2 order); fact-plane registry", "retained", A_INH, ts="c2 v3 coverageKey.key + rust2 coverageDomainAlgorithm",
                      h=["rp2.planAndDomainProjection coverageDomainAlgorithm", "fp.registry"], g=["R3-G7"]),
        "resolution": R(T, T, "every rung of the relation's fact-plane ladder, weakest first", "retained", A_INH, ts="rust2 coverageDomainAlgorithm", g=["R3-G7"]),
        "sourceUniverseId": R(T, T, "Sha256Text; native semantic-universe identity sha256:hex(H(native.semantic-universe.rust.v2, universe.resolvedInputs)) (inherited opensip.rust-provider.universe.v2 recipe superseded)",
                              "value-substituted", A_UNIV, ts="rust2 coverageDomainAlgorithm", h=["start.admit_coverage_frame: sourceUniverse suffix join"], g=["R3-G7"]),
        "targetUniverseId": R(T, T, "native semantic-universe identity of each target: [source] for same-only, else the admitted target set (inherited opensip.semantic-universe.v2 recipe superseded)",
                              "value-substituted", A_UNIV, ts="rust2 coverageDomainAlgorithm", h=["start.admit_coverage_frame: targetUniverse suffix join"], g=["R3-G7"]),
        "subjectScopeCommitment": R(T, T, "Sha256Text; value recipe contested (rust2 per-stage subjectScope vs §4.1a per-key scope2)", "retained",
                                    A_INH + "; native-evidence.md:1889-1947 (§4.1a); :136", cls="owner-contradictory", ts="rust2 $.commitments.subjectScope",
                                    h=["ne.admit_coverage_result_v3", "ne.subject_scope_commitment"], g=["R3-G4", "R3-G7"]),
        "producer": R(T, T, "const rust-semantic", "retained", A_INH, ts="rust2 coverageDomainAlgorithm"),
        "producerVersion": R(T, T, "verified providerBuildId (HelloV3.expectedIdentity.providerBuildId)", "retained", A_INH, ts="rust2 coverageDomainAlgorithm"),
        "schemaVersion": R(U, U, "the relation payload registry schemaVersion", "retained", A_INH, ts="rust2 coverageDomainAlgorithm"),
    },
    "StageAnalysisDomainV2": {
        "subjects": R(A, A, "items SubjectV2; 1..maxSubjectsPerStage 256; identical for every selected stage", "retained", A_INH,
                      ts="rust2 subjectsAlgorithm", h=["chk2.validate_domain", "rij.analysisDomainBinding"]),
        "requestedCoverageDomain": R(A, A, "items CoverageKeyV2 (rust2, 8 members); 1..maxRequestedCoverageKeysPerStage 256; canonical nested-loop order relation/rung/target (not sorted); duplicates refuse",
                                     "retained", A_INH, ts="rust2 coverageDomainAlgorithm", h=["chk2.validate_domain", "rp2.planAndDomainProjection wireRule"], g=["R3-G4"]),
        "domainCommitment": R(T, T, "Sha256Text; opensip.rust-provider.analysis-domain.v2 over {subjects, requestedCoverageDomain}; recipe retained, committed value changes with substituted keys",
                              "value-substituted", A_INH + "; " + A_UNIV, ts="rust2 $.commitments.analysisDomain", h=["chk2.validate_domain"], g=["R3-G4"]),
    },
    "StageRequestV2": {
        "stageOrdinal": R(U, U, "contiguous 0..n-1 in THIS Analyze order (== DispatchBindingV1.analyzeRequestOrdinal; never assumed == retainedStageOrdinal)",
                          "retained", A_INH + "; " + A_DISPATCH, ts="field text 'contiguous Analyze order'", h=["dispatch: analyzeRequestOrdinal"]),
        "planStage": R(M, M, "C2PlanStageV3: exact nested C-2 stage bytes; optional C-2 members present only when present in the ExecutionPlan", "retained",
                       A_INH + "; " + A_C2, h=["rp2.planAndDomainProjection planStageByteRule"]),
        "analysisDomain": R(M, M, "StageAnalysisDomainV2: exact host reconstruction", "retained", A_INH, h=["rp2.planAndDomainProjection wireRule", "chk2.validate_domain"]),
    },
    "CoverageResultV2": {
        "stageId": R(T, T, "moved to the CoverageV3 wrapper stageId", "replaced", A_R118 + "; " + A_R129, r=_st("CoverageV3", "stageId"), m="moved"),
        "entryOrdinal": R(U, None, "removed: array index i of entries answers requestedCoverageDomain.keys[i]", "replaced", A_R118 + "; " + A_R129,
                          r=NE + "CoverageResultV3", m="removed", ts="derived: rust2 deterministicBudget 'Coverage entryOrdinal'",
                          h=["start.admit_coverage_frame: positional bijection"]),
        "coverageState": R(T, T, "-> entry.coverage enum complete|unknown (RC-6: complete requires examinedExhaustive)", "replaced", A_R118,
                           r=NE + "ViewEntryV3/properties/coverage", m="moved", h=["ne.admit_coverage_result_v3"]),
        "key": R(M, M, "-> key CoverageKeyV2 (native-evidence, 5 members: relation, resolution, sourceUniverse, targetUniverse bare 64-hex, subjectScopeCommitment)",
                 "replaced", A_R118, r=NE + "CoverageKeyV2", m="value-changed", h=["start.admit_coverage_frame: equals keys[i] by suffix projection", "ne.admit_coverage_result_v3 §4.1a steps 1-4"],
                 g=["R3-G4", "R3-G7"]),
        "deficiency": R("UTF-8-NFC-text|null", "UTF-8-NFC-text|null", "-> entry.deficiency DeficiencyV2 (9 values) | null (inherited: null | provider-unavailable | budget-exhausted)",
                        "replaced", A_R118, r=NE + "ViewEntryV3/properties/deficiency", m="moved"),
    },
    "StageResultV2": {
        "stageId": R(T, T, "exact requested stage id (StageIdText by echo)", "retained", A_R129 + " (record superseded; no successor record)", cls="owner-missing",
                     ts=ECHO + "planStage.stageId (fields.all)", g=["R3-G13"]),
        "factCount": R(U, U, "exact recomputed candidate count", "retained", A_R129 + " (record superseded; no successor record)", cls="owner-missing", ts=ARITH, g=["R3-G13"]),
        "coverageEntryCount": R(U, U, "exact recomputed CoverageResultV3 entry count", "retained", A_R129 + " (record superseded; no successor record)",
                                cls="owner-missing", ts=ARITH, g=["R3-G13"]),
        "factCommitment": R(T, T, "Sha256Text; opensip.rust-provider.stage-facts.v2 over the stage's ordered FactCandidateV1 values, whichever payload carried them",
                            "retained", A_R123 + "; provider-handshake law commitments.rust-semantic", cls="owner-missing", ts="rust2 $.commitments.stageFacts (field name)",
                            h=["rp2.commitments stageFacts"], g=["R3-G13"]),
        "coverageCommitment": R(T, T, "Sha256Text; stageCoverage recipe/domain unchanged over CoverageResultV3 values (§9.7)", "value-substituted",
                                A_R129 + "; native-evidence.md:3283-3287", cls="owner-missing", ts="rust2 $.commitments.stageCoverage (field name)",
                                h=["rp2.commitments stageCoverage"], g=["R3-G12", "R3-G13"]),
    },
}

# Definitions with no member list in the v2 grammar: one record-level row each; members are expanded under EXTERNAL.
RECORD_ONLY_DEFS = {
    "RustUniverseV1": R(M, M, "complete external rust-v1 value -> RustSemanticUniverseV2", "replaced", A_R128, r=ST + "RustSemanticUniverseV2",
                        m="value-changed", ts="external resolved-inputs.v2 rust-v1", h=["start.admit_open_universe"]),
    "C2PlanStageV3": R(M, M, "exact closed C-2 fact-derivation stage (recursive validation against pinned c2 v3 bytes)", "retained", A_C2,
                       ts="external c2-plan-stage-schema.v3", h=["c2.stageSchemas", "rp2.planAndDomainProjection planStageByteRule"]),
    "FactCandidateV1": R(M, M, "closed 14-member fact-plane candidate; canonicalRelationPayload is a byte string", "retained", A_FP, r=FB + "/properties/candidates/items",
                         ts="external fact-plane candidateSchema", h=["fp.candidate", "wire.admit_fact_batch"],
                         x="the ref is the JSON-vector candidate (hex transcription + decoded observation), not a wire record"),
}

_C2 = "c2 v3 $.stageSchemas"
EXTERNAL = {
    "C2PlanStageV3": {
        "kind": R(T, T, "const fact-derivation", "retained", A_C2, ts=_C2 + ".common.required", h=["rp2.planAndDomainProjection selectedStageRule"]),
        "stageId": R(T, T, "C-2 stageId text; unique; 1..255 by DispatchBindingV1.expectedStageId (which names StageRequestV2.planStage.stageId); c2 v3 states no type/bound",
                     "retained", A_C2 + "; " + A_DISPATCH, ts=_C2 + ".common.required; dispatch-binding expectedStageId", h=["dispatch: expectedStageId"], g=["R3-G2"]),
        "dependsOn": R(A, A, "optional; stageId texts of earlier stages", "retained", A_C2, ts=_C2 + ".common.optional; workflow.stages text", pres="optional"),
        "budget": R(M, M, "optional; stageBudgetV1 {unit work-units|milliseconds|bytes|items, limit 1..9223372036854775807}", "retained", A_C2,
                    ts=_C2 + ".common.optional; c2 v3 planIntent.wireTypes.stageBudgetV1", h=["rp2.deterministicBudget"], pres="optional"),
        "relations": R(A, A, "fact-plane registry relation names; <= maxRelationsPerStage 64", "retained", A_C2, ts=_C2 + ".kinds.fact-derivation.required",
                       h=["fp.registry"]),
        "operator": R(T, T, "const semantic-provider for selected stages (C-2 enum builtin-extractor|semantic-provider|external-scanner)", "retained", A_C2,
                      ts=_C2 + ".kinds.fact-derivation.operatorAuthority"),
        "capabilityGrants": R(A, A, "optional; AdmissionDescriptorV1.capabilityGrants[*].grantId texts", "retained", A_C2, ts=_C2 + ".kinds.fact-derivation.optional",
                              pres="optional"),
        "providerId": R(T, T, "optional in C-2; const rust-semantic for every selected stage", "retained", A_C2, ts=_C2 + ".kinds.fact-derivation.optional; selectedStageRule",
                        pres="optional"),
    },
    "FactCandidateV1": {
        "candidateOrdinal": R(U, U, "contiguous within the attributed stage from 0 (resets each stage); transport-only", "retained", A_FP, r=FBC + "candidateOrdinal",
                              h=["rp2.transitionAstV2 T016/T017", "dispatch: expectedFirstCandidateOrdinal"]),
        "relation": R(T, T, "requested by the stage; registry key", "retained", A_FP, r=FBC + "relation", h=["fp.registry"]),
        "resolution": R(T, T, "rung of the relation's ladder", "retained", A_FP, r=FBC + "resolution", h=["fp.registry"]),
        "layer": R(T, T, "the relation's registry layer", "retained", A_FP, r=FBC + "layer", h=["fp.registry"]),
        "producer": R(T, T, "const rust-semantic", "retained", A_FP, r=FBC + "producer"),
        "producerVersion": R(T, T, "verified providerBuildId (HelloV3.expectedIdentity.providerBuildId)", "retained", A_FP, r=FBC + "producerVersion"),
        "schemaVersion": R(U, U, "exact host registry schemaVersion", "retained", A_FP, r=FBC + "schemaVersion", h=["fp.candidate"]),
        "language": R(T, T, "const rust", "retained", A_FP, r=FBC + "language"),
        "sourceUniverseId": R(T, T, "Sha256Text; native rust v2 semantic-universe identity (== OpenUniverse universe identity)", "value-substituted", A_UNIV,
                              r=FBC + "sourceUniverseId", g=["R3-G7"]),
        "targetUniverseId": R(T, T, "native semantic-universe identity of a host-admitted target; same-only relations require == source", "value-substituted",
                              A_UNIV, r=FBC + "targetUniverseId", g=["R3-G7"]),
        "confidenceMillionths": R(U, U, "0..1000000", "retained", A_FP, r=FBC + "confidenceMillionths"),
        "relationSchemaId": R(T, T, "exact host registry schemaId", "retained", A_FP, r=FBC + "relationSchemaId", h=["fp.candidate"]),
        "canonicalRelationPayload": R(B, B, "deterministic-CBOR bytes; <= maxCanonicalRelationPayloadBytes 1048576; decode once, re-encode equal", "retained", A_FP,
                                      ts="wireAdjustment 'canonicalRelationPayload is a byte string'", h=["fp.candidate", "wire.admit_fact_batch: CANDIDATE_PAYLOAD_BOUND"],
                                      x="no schema-native wire ref: fact-batch.3 canonicalRelationPayloadHex/decodedRelationPayload are JSON-vector members", g=["R3-G1"]),
        "anchors": R(A, A, "items AnchorRefV1; non-empty; sorted ascending by CVE1(anchor) bytes, unique (vector maxItems 4096)", "retained", A_FP,
                     r=FBC + "anchors", h=["fp.anchor"], g=["R3-G5"]),
    },
    "AnchorRefV1": {
        "kind": R(T, T, "enum source-span|fact-ref", "retained", A_ANCHOR, ts="anchorSchema.variants keys", h=["fp.anchor"]),
        "snapshotId": R("UNSTATED|null", "UNSTATED|null", "source-span: non-null; fact-ref: null; snapshot2 substitution not enumerated", "retained", A_ANCHOR,
                        cls="owner-missing", ts="UNSTATED", g=["R3-G5", "R3-G16"]),
        "path": R("UTF-8-NFC-text|null", "UTF-8-NFC-text|null", "source-span: normalized project-relative NFC path of a sealed file; fact-ref: null", "retained", A_ANCHOR,
                  ts="fact-plane sourceSpanSchema.rule", g=["R3-G5"]),
        "contentSha256": R("UNSTATED|null", "UNSTATED|null", "source-span: sealed file digest (form unstated); fact-ref: null", "retained", A_ANCHOR,
                           cls="owner-missing", ts="UNSTATED", g=["R3-G5"]),
        "startByte": R("UNSTATED|null", "UNSTATED|null", "source-span: [startByte,endByte) non-empty in bounds; fact-ref: null", "retained", A_ANCHOR,
                       cls="owner-missing", ts="UNSTATED", g=["R3-G5"]),
        "endByte": R("UNSTATED|null", "UNSTATED|null", "as startByte", "retained", A_ANCHOR, cls="owner-missing", ts="UNSTATED", g=["R3-G5"]),
        "factId": R("UNSTATED|null", "UNSTATED|null", "fact-ref: FACT-ID-V1 (conflicts with mandatory fact2); source-span: null", "retained", A_ANCHOR,
                    cls="owner-contradictory", ts="UNSTATED", g=["R3-G5"]),
    },
    "RustUniverseV1": {},
    "RustUniverseV1.resolvedInputs": {},
}

_RV1_DIGEST = {"manifestId", "capabilityManifestId", "providerArtifactSha256", "toolchainArtifactSha256", "rustCommitHash", "sysrootDigest",
               "rustcDevLlvmDigest", "providerBinarySha256", "licenseNoticeBundleSha256"}
for _name in ["schemaVersion", "manifestId", "capabilityManifestId", "providerArtifactId", "providerArtifactSha256", "toolchainArtifactId",
              "toolchainArtifactSha256", "protocolMajor", "providerBuildId", "rustCommitHash", "rustcVersion", "cargoVersion", "hostTriple",
              "targetTriple", "sysrootDigest", "rustcDevLlvmDigest", "standardLibraryComponentDigests", "providerBinarySha256",
              "licenseNoticeBundleSha256", "platformId", "resolvedInputs"]:
    _ref = _st("RustSemanticUniverseV2", _name)
    if _name in _RV1_DIGEST:
        _row = R(T, T, "DigestHex (64 lowercase hex)", "replaced", A_R128, r=_ref, m="unchanged", ts="rust-v1 digestFields/digestRepresentation")
    elif _name == "schemaVersion":
        _row = R(U, U, "const 1", "replaced", A_R128, r=_ref, m="unchanged", ts="rust-v1 constants")
    elif _name in ("providerArtifactId", "toolchainArtifactId"):
        _row = R(T, T, "const " + ("rust-provider" if _name == "providerArtifactId" else "rust-toolchain-bundle"), "replaced", A_R128, r=_ref, m="unchanged",
                 ts="rust-v1 constants")
    elif _name == "protocolMajor":
        _row = R(X, U, "const 3 (rust-v1 states no constant; deliveryJoin equals the handshake)", "replaced", A_R128, r=_ref, m="value-changed",
                 ts="successor schema", h=["start.admit_open_universe: handshakeJoin"])
    elif _name == "standardLibraryComponentDigests":
        _row = R(M, M, "open map: component name -> DigestHex", "replaced", A_R128, r=_ref, m="unchanged", ts="rust-v1 digestRepresentation",
                 x="open-keyed map: a Rust carrier must be an ordered map, not fixed fields")
    elif _name == "resolvedInputs":
        _row = R(M, M, "RustUniverseV2ResolvedInputs (14 members; wholesale supersession)", "replaced", A_R128 + "; " + A_R130, r=_ref, m="value-changed")
    else:
        _row = R(X, T, "NfcText (non-empty; NFC by admission); rust-v1 states no text type", "replaced", A_R128, r=_ref, m="unchanged",
                 ts="successor schema", h=(["start.admit_open_universe: handshakeJoin (IdentityText in HelloV3 vs NfcText here; equality closes the bound)"]
                                           if _name in ("providerBuildId", "hostTriple", "targetTriple") else []))
    EXTERNAL["RustUniverseV1"][_name] = _row

for _name, _change in [("edition", "value-changed"), ("cfg", "removed"), ("packageLockIdentity", "removed"), ("resolvedPackages", "removed"),
                       ("rustflags", "value-changed"), ("crateRootPaths", "value-changed"), ("executionCapableResolution", "value-changed"),
                       ("buildScriptOutputs", "removed"), ("procMacroOutputs", "removed")]:
    _inh = BOOL if _name == "executionCapableResolution" else (X if _name == "edition" else A)
    EXTERNAL["RustUniverseV1.resolvedInputs"][_name] = R(
        _inh, None, ("same-name member of RustUniverseV2ResolvedInputs; wholesale supersession, equality not asserted" if _change == "value-changed"
                     else "removed by wholesale supersession (no rename is stated)"),
        "replaced", A_R130, r=(NE + "RustUniverseV2ResolvedInputs/properties/" + _name if _change == "value-changed" else NE + "RustUniverseV2ResolvedInputs"),
        m=_change, ts="resolved-inputs.v2 rust-v1.resolvedInputs text")


def N_(w, b, src, *, r=None, h=(), g=(), cls="governed", x=None, ts="schema-native"):
    row = R(None, w, b, "new", src, cls=cls, r=r, ts=ts, x=x, h=h, g=g)
    return row


NEW = {
    "HelloV3.protocolMajor": N_(U, "const 3 (kept from the superseded native-evidence.schemas.v2 HelloV3)", A_R122, r=_hs("HelloV3", "protocolMajor"), h=["wire.admit_hello"]),
    "HelloV3.identityVersions": N_(M, "IdentityVersionsV1 {snapshot:2, plan:2, fact:2, coverage:3}", A_R122, r=_hs("HelloV3", "identityVersions")),
    "HelloAckV3.identityVersions": N_(M, "exact echo of Hello identityVersions", A_R122, r=_hs("HelloAckV3", "identityVersions"),
                                      h=["wire.admit_hello_ack: IDENTITY_VERSIONS_ECHO"]),
}
for _name, _value in NEW_LIMITS:
    NEW["ProtocolLimitsV3." + _name] = N_(U, "const %d" % _value, A_LIM, r=HS + "ProtocolLimitsV3/properties/" + _name, h=["rp2.limitsHandshake"])

_RIN = NE + "RustUniverseV2ResolvedInputs/properties/"
for _name, _w, _b in [
        ("schemaVersion", U, "const 2"), ("edition", M, "open map -> integer 2015|2018|2021|2024"),
        ("lockfileIdentity", M, "LockfileIdentityV1"), ("dependencySourceSetId", T, "Sha256Text (native.dependency-source-set.v1)"),
        ("unifiedFeaturesId", T, "Sha256Text (native.unified-features.rust.v1)"), ("nativeContextId", T, "Sha256Text (native.context.rust.v2); suffix in plan.nativeContextDigests"),
        ("cfgSets", A, "1..4 {cfgSetId, cfg}"), ("rustflags", M, "RustflagsProjectionV1"),
        ("crateRootPaths", A, "0..100000 CanonicalPath, utf8 order"), ("configProjectionSha256", T, "bare 64-hex suffix of H(native.cargo-config-projection.v2, ...)"),
        ("executionCapableResolution", BOOL, "prepared products consumed as inert data only"), ("preparedOutputSetId", "UTF-8-NFC-text|null", "Sha256Text (native.prepared-output-set.v3) | null"),
        ("preparedResolution", T, "enum none|host-prepared|imported-inert"), ("sourceUnitOwnershipId", "UTF-8-NFC-text|null", "Sha256Text | null")]:
    NEW["RustUniverseV2ResolvedInputs." + _name] = N_(_w, _b, A_R130, r=_RIN + _name, h=(["start.admit_open_universe"] if _name == "nativeContextId" else []))

_RR = NE + "RepositoryResolutionV3/properties/"
NEW.update({
    "RepositoryResolutionV3.dependencySourceSetId": N_(T, "Sha256Text; required non-null; == universe.resolvedInputs.dependencySourceSetId", A_R118, r=_RR + "dependencySourceSetId",
                                                      h=["start.admit_open_universe: REPOSITORY_RESOLUTION_JOIN"]),
    "RepositoryResolutionV3.preparedOutputSetId": N_("UTF-8-NFC-text|null", "Sha256Text | null; == universe.resolvedInputs.preparedOutputSetId", A_R118, r=_RR + "preparedOutputSetId",
                                                    h=["start.admit_open_universe: REPOSITORY_RESOLUTION_JOIN"]),
    "RepositoryResolutionV3.authorizationId": N_("UTF-8-NFC-text|null", "Sha256Text | null; null when preparedOutputSetId is null or the preparation is imported-descriptor", A_R118,
                                                r=_RR + "authorizationId", h=["start.admit_open_universe: REPOSITORY_RESOLUTION_JOIN"]),
    "RepositoryResolutionV3.workerExecutesRepositoryCode": N_(BOOL, "const false", A_R118, r=_RR + "workerExecutesRepositoryCode"),
    "RepositoryResolutionV3.effects": N_("definite-text-keyed-map|null", "{subprocess, filesystemWrite, network, environment} of EffectV1 | null; null exactly when authorizationId is null",
                                        A_R118, r=_RR + "effects", h=["start.admit_open_universe: authorizationId-effects pairing"], x="successor of inherited network (moved)"),
})

_DM = NE + "DependencySourceManifestV3/properties/"
_DS = NE + "DependencySourceSealV3/properties/"
NEW.update({
    "DependencySourceManifestV3.dependencySourceSetId": N_(T, "Sha256Text; == OpenUniverse repositoryResolution.dependencySourceSetId", A_DS, r=_DM + "dependencySourceSetId"),
    "DependencySourceManifestV3.manifestSha256": N_(T, "DigestHex; digest annotation 'exact transport manifest frame bytes as sent' (self-referential); no recipe", A_DS,
                                                   r=_DM + "manifestSha256", cls="owner-contradictory", g=["R3-G11"]),
    "DependencySourceManifestV3.entries": N_(A, "0..1000000 (maxDependencySourceEntries); uniqueItems; order law unstated (x-opensip-order sequence); [] for an empty set", A_DS,
                                            r=_DM + "entries", g=["R3-G11"]),
    "DependencySourceManifestV3.entries[].packageKey": N_(T, "text 1..4096; grammar and join to DependencyPackageSourceV1 unstated", A_DS,
                                                         r=_DM + "entries/items/properties/packageKey", cls="owner-missing", g=["R3-G11"]),
    "DependencySourceManifestV3.entries[].path": N_(T, "CanonicalPath pattern, 1..4096", A_DS, r=_DM + "entries/items/properties/path", g=["R3-G2"]),
    "DependencySourceManifestV3.entries[].byteLength": N_(U, "uint64", A_DS, r=_DM + "entries/items/properties/byteLength"),
    "DependencySourceManifestV3.entries[].contentSha256": N_(T, "DigestHex of the retained member bytes", A_DS, r=_DM + "entries/items/properties/contentSha256"),
    "DependencySourceSealV3.dependencySourceSetId": N_(T, "Sha256Text echo", A_DS, r=_DS + "dependencySourceSetId"),
    "DependencySourceSealV3.manifestSha256": N_(T, "DigestHex echo", A_DS, r=_DS + "manifestSha256", g=["R3-G11"]),
    "DependencySourceSealV3.entryCount": N_(U, "uint64; 0 for an empty set", A_DS, r=_DS + "entryCount"),
    "DependencySourceSealV3.totalBytes": N_(U, "uint64; maxDependencySourceTotalBytes 8589934592 exists, binding not restated", A_DS, r=_DS + "totalBytes"),
    "DependencySourceSealV3.totalChunkCount": N_(U, "uint64; 0 for an empty set (no chunk)", A_DS, r=_DS + "totalChunkCount"),
})
for _name in ["dependencySourceSetId", "packageKey", "path", "chunkIndex", "byteOffset", "bytes"]:
    NEW["DependencySourceChunk(unnamed)." + _name] = N_(X, ("member named by native-evidence.md:2877 only; maxDependencySourceChunkBytes 1048576 exists but is not bound by the row"
                                                           if _name == "bytes" else "member named by native-evidence.md:2877 only; no type, bound or order"),
                                                       A_DS, cls="owner-missing", ts="UNSTATED", g=["R3-G10", "R3-G3"] + (["R3-G1"] if _name == "bytes" else []))
for _name in ["dependencySourceSetId", "manifestSha256", "entryCount", "totalBytes", "totalChunkCount"]:
    NEW["DependencySourceAccepted(unnamed)." + _name] = N_(T if _name in ("dependencySourceSetId", "manifestSha256") else U, "exact DependencySourceSeal echo after digest/VFS validation",
                                                          A_DS, r=_DS + _name, cls="owner-missing", ts="echo of DependencySourceSealV3 (native-evidence.md:2879)",
                                                          g=["R3-G10", "R3-G3"])

_NCV = ST + "NativeContextVerifiedV1/properties/"
_PRE = ST + "PreAnalyzeUnavailableV1/properties/"
NEW.update({
    "NativeContextVerifiedV1.nativeContextId": N_(T, "Sha256Text == OpenUniverse.universe.resolvedInputs.nativeContextId", A_NCV, r=_NCV + "nativeContextId",
                                                 h=["start.admit_native_context_verified"]),
    "NativeContextVerifiedV1.recomputedNativeContextId": N_(T, "Sha256Text; worker recomputation; equal", A_NCV, r=_NCV + "recomputedNativeContextId",
                                                           h=["start.admit_native_context_verified"]),
    "NativeContextVerifiedV1.equal": N_(BOOL, "const true", A_NCV, r=_NCV + "equal"),
    "PreAnalyzeUnavailableV1.executionId": N_(T, "ExecutionIdText == OpenUniverse (rust-semantic IdentityText)", A_PRE, r=_PRE + "executionId", h=["start.admit_unavailable"]),
    "PreAnalyzeUnavailableV1.snapshotId": N_(T, "SnapshotId2 == OpenUniverse", A_PRE, r=_PRE + "snapshotId", h=["start.admit_unavailable"]),
    "PreAnalyzeUnavailableV1.planId": N_(T, "PlanId2 == OpenUniverse", A_PRE, r=_PRE + "planId", h=["start.admit_unavailable"]),
    "PreAnalyzeUnavailableV1.reason": N_(T, "const native-context-mismatch", A_PRE, r=_PRE + "reason"),
    "PreAnalyzeUnavailableV1.nativeContextId": N_(T, "Sha256Text == universe.resolvedInputs.nativeContextId", A_PRE, r=_PRE + "nativeContextId", h=["start.admit_unavailable"]),
    "PreAnalyzeUnavailableV1.recomputedNativeContextId": N_(T, "Sha256Text; differs from nativeContextId", A_PRE, r=_PRE + "recomputedNativeContextId",
                                                           h=["start.admit_unavailable", "ne.pre_analyze_unavailable_conversion: host mints coverage after DONE"]),
    "FactBatchV3.schemaVersion": N_(U, "const 3 (payload discriminator; not FactCandidateV1.schemaVersion)", A_R123, r=FB + "/properties/schemaVersion"),
    "FactBatchV3.analysisOrdinal": N_(U, "uint64 echo of AnalyzeV2.analysisOrdinal", A_R123, r=FB + "/properties/analysisOrdinal", h=["dispatch: expectedAnalysisOrdinal"]),
    "FactBatchV3.stageId": N_(T, STAGEID, A_R123, r=FB + "/properties/stageId", h=["dispatch: expectedStageId"]),
    "FactBatchV3.batchIndex": N_(U, "contiguous from 0 per stage", A_R123, r=FB + "/properties/batchIndex", h=["dispatch: expectedBatchIndex"]),
    "FactBatchV3.candidates": N_(A, "wire items FactCandidateV1 (bstr payload); 1..4096 (maxFactBatchCandidates); JSON-vector ref", A_R123, r=FB + "/properties/candidates",
                                 h=["wire.admit_fact_batch"], g=["R3-G1"]),
    "FactBatchV3.occupancyCompanions": N_(A, "OccupancyCompanionV1 (10 members, allOf branches); 0..len(candidates); strictly increasing candidateOrdinal naming this batch", A_R123,
                                          r=FB + "/properties/occupancyCompanions", h=["wire.admit_fact_batch: COMPANION_CANDIDATE"]),
    "CoverageResultV3.schemaVersion": N_(U, "const 3", A_R129, r=NE + "CoverageResultV3/properties/schemaVersion"),
    "CoverageResultV3.key": N_(M, "CoverageKeyV2 (native-evidence, 5 members)", A_R129, r=NE + "CoverageResultV3/properties/key", g=["R3-G7"]),
    "CoverageResultV3.entry": N_(M, "ViewEntryV3 (10 members; schema-native, not expanded here)", A_R129, r=NE + "CoverageResultV3/properties/entry",
                                h=["ne.admit_coverage_result_v3", "ne.coverage_bijection"]),
    "CoverageKeyV2@native-evidence.relation": N_(T, "Relation enum; == keys[i].relation", A_R129, r=NE + "CoverageKeyV2/properties/relation", h=["start.admit_coverage_frame"], g=["R3-G7"]),
    "CoverageKeyV2@native-evidence.resolution": N_(T, "Rung enum; == keys[i].resolution", A_R129, r=NE + "CoverageKeyV2/properties/resolution", h=["start.admit_coverage_frame"], g=["R3-G7"]),
    "CoverageKeyV2@native-evidence.sourceUniverse": N_(T, "bare 64-hex suffix of keys[i].sourceUniverseId", A_R129, r=NE + "CoverageKeyV2/properties/sourceUniverse",
                                                      h=["start.admit_coverage_frame"], g=["R3-G7"]),
    "CoverageKeyV2@native-evidence.targetUniverse": N_(T, "bare 64-hex suffix of keys[i].targetUniverseId", A_R129, r=NE + "CoverageKeyV2/properties/targetUniverse",
                                                      h=["start.admit_coverage_frame"], g=["R3-G7"]),
    "CoverageKeyV2@native-evidence.subjectScopeCommitment": N_(T, "Sha256Text; == keys[i].subjectScopeCommitment and the host-minted scope2 text form", A_R129,
                                                              r=NE + "CoverageKeyV2/properties/subjectScopeCommitment", cls="owner-contradictory",
                                                              h=["ne.admit_coverage_result_v3"], g=["R3-G4"]),
})

__all__ = ["ENVELOPE", "FRAMES", "NEW_FRAMES", "PAYLOADS", "STRING_DEFS", "RECORD_DEFS", "RECORD_ONLY_DEFS", "EXTERNAL", "NEW", "V2_LIMITS", "NEW_LIMITS", "DB"]
