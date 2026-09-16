"""Shared vocabulary for the Rust3 retained-field wire translation.

Proposed implementation artifact for root review. Not an approval, not a wire change, not product code.
"""

# Wire types: rust-provider-protocol.v2 $.canonicalCbor.closedDataModel, with false|true folded to bool.
# Negative integers are FORBIDDEN on the Rust wire ($.canonicalCbor.forbidden[0]); there is no negative-int type here.
U = "uint64"
T = "UTF-8-NFC-text"
B = "byte-string"
A = "definite-array"
M = "definite-text-keyed-map"
N = "null"
BOOL = "bool"
X = "UNSTATED"
WIRE_BASE = {U, T, B, A, M, N, BOOL, X}


def wire_ok(w):
    return w is None or all(part in WIRE_BASE for part in w.split("|"))


# Schema-native owner $id prefixes (exact $id values of the pinned documents).
HS = "opensip.product.provider-handshake.1#/$defs/"
ST = "opensip.product.provider-startup.1#/$defs/"
NE = "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/"
FB = "opensip.product.fact-batch.3#"
FBC = FB + "/properties/candidates/items/properties/"
OC = "opensip.product.occupancy-companion.1#"
DB = "opensip.product.dispatch-binding.1#"

# Repository-relative source paths.
RP2 = "docs/coop/artifacts/rust-provider-protocol.v2.json"
NEMD = "docs/v2/contracts/product-v1/native-evidence.md"
IDMD = "docs/v2/contracts/product-v1/identity-and-evidence.md"
NATIVE = "docs/coop/design-corrections/native/"
HSP = NATIVE + "provider-handshake.schemas.v1.json"
STP = NATIVE + "provider-startup.schemas.v1.json"
NEP = NATIVE + "native-evidence.schemas.v2.json"
FBP = NATIVE + "fact-batch.schema.v3.json"
OCP = NATIVE + "occupancy-companion.schema.v1.json"
DBP = NATIVE + "dispatch-binding.schema.v1.json"
P3P = NATIVE + "protocol3-transitions.v1.json"
WIREM = NATIVE + "provider_wire_model.v1.py"
STARTM = NATIVE + "provider_startup_model.v1.py"
NEM = NATIVE + "native_evidence_model.v2.py"
PINS = NATIVE + "source-pins.v2.json"
FP = "docs/coop/artifacts/fact-plane.v1.json"
RI = "docs/coop/artifacts/resolved-inputs.v2.json"
RIJ = "docs/coop/artifacts/resolved-inputs-rust-provider-join.v2.json"
C2V3 = "docs/coop/artifacts/c2-plan-stage-schema.v3.json"
C2V4 = "docs/coop/artifacts/c2-plan-stage-schema.v4.json"
CHK2 = "docs/coop/artifacts/check-rust-provider-protocol-v2.py"
CHK1 = "docs/coop/artifacts/check-rust-provider-protocol.py"
CTL2 = "docs/coop/artifacts/control-protocol-contract.v2.json"
CTLS3 = "docs/coop/completion/control-completion.schema.v3.json"
IMPL = "docs/implementation/README.md"
AUDIT = "docs/implementation/m1/reviews/generation-owner-audit-01/audit.md"
TSDIR = "/tmp/opensip-implementation/m1-typescript-wire-translation-01/"
GAPDIR = "/tmp/opensip-implementation/m1-protocol-gap-resolution-01/"

# Exact bytes read on 2026-09-14 (sha256, byte length). The architecture working tree has uncommitted and untracked
# edits; these pins are of the bytes read, and build.py refuses to run if any differ.
SOURCES = {
    RP2: ("6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b", 61698),
    NEMD: ("83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0", 329013),
    IDMD: ("c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f", 135448),
    HSP: ("9090e2ad51b767a176f51da09f201803d1cc82c047ade68102adcae1ee3a5f84", 32009),
    STP: ("1e35a77bae8d9c20171a934e9c16e4de4d7ce98bb024016d7e17cf9b0b38729c", 33341),
    NEP: ("2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043", 277967),
    FBP: ("b0ebc133df8763f6cd5f3716542321eba21c69714fca368fbe31ba57677a24e0", 10028),
    OCP: ("d2bbbcc49adbb130d0bb010fee0b4cf25af7727f730fc329725fa62cd46ae14f", 8821),
    DBP: ("868c3cf241af9ecc205ba7d078354e38a7db5132974120c046ac23a2dd1df938", 4568),
    P3P: ("b0aca55d89482be14e9c34554c1febb66d9751754b7c3057a383a010515feb0b", 14845),
    WIREM: ("a2a8b9d116552856412e4257069f8c75debd6d8b2fe165407477fb7b28e46295", 19099),
    STARTM: ("3f75b859b45c4fc6d5e5c8ede642a981d8d83bdf55d8e19ef7c9ffe7d5e8d494", 16245),
    NEM: ("7d1c0acf2c7d74e52c6570bba66dcb846c03710f64cb61a2c83bd1c39abab8be", 319376),
    PINS: ("ef2da049061341ee75250e2b262544d53ff3dbd24da642679f40bc1a48cb17bf", 219232),
    FP: ("9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d", 59168),
    RI: ("0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43", 107615),
    RIJ: ("435ec9cdd45a85255df0c099238bd0a3e1c10e88960716cd84649030d6482d47", 16770),
    C2V3: ("3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285", 112128),
    C2V4: ("4876284790462968549f834b866c7ffc5f7be1c43b583169570c1947c5c4af39", 174430),
    CHK2: ("7b967b888fc172b27268fae2f59273e5cf10b58b97db7c1f19a15657826a48e4", 105962),
    CHK1: ("c190ee7f62552ec342f5da1f66ba2b840cdffd5cd5cddb25e5987c315ee1502e", 125802),
    CTL2: ("c50a79fef566ecccbd8913a3d309b0cf7332f7d77f892474a548ef3d7b4ebdca", 80533),
    CTLS3: ("2929de62e9eb3a3dc78959eaf3d50361b8d1f895d086940724c1c743ac46a98c", 22476),
    # Re-pinned: this untracked file changed on disk during authoring (first read: e1204151c30bff15e541c927afc03e3f671b43e0f760c11e49388022b14f8572,
    # 14955 bytes). The re-read text changes no Rust3 disposition; it records the control-owner chain as under root verification.
    IMPL: ("d4aad574086892e31addf5a0263084fee694e195650d07270dbfb8e275ed73c3", 7503),
    AUDIT: ("1423515e44f4a35b3a4433e65fdffa3914a4f4e0e0d12e47452914adb88c5903", 24669),
    TSDIR + "fields.json": ("4c211bb5fd28115b9fad3384d978b3911dd8f1f63cbd6fcf2e633430a27efe6a", 243789),
    TSDIR + "coverage.json": ("b288c30de9cbb98e9f8d09a4f9c34fa7780ac74c5a338046cce40e69e62d22f2", 675),
    TSDIR + "translation.md": ("c579ae5ca206c4ba22aef3874d9afd66e8a54f511052e546f347eafe093e6213", 78094),
    GAPDIR + "resolutions.md": ("c60af837f526b2de5982c7abdb94f4400687a61d04aae0c516c1fe692ea90781", 24484),
}

# Disposition authorities (native-evidence.md line numbers at sha 83b99783...; build.py verifies each anchor line).
A_R117 = "native-evidence.md:117 (§0: repositoryExecution.preparedOwner/forbidden relabeled)"
A_R118 = "native-evidence.md:118 (§0: RepositoryResolutionV2, CoverageResultV2, UnavailableV2.fields.reason, $.limits, orderingAndStateMachine.stateRecord.phaseValues superseded by major 3, §9)"
A_R122 = "native-evidence.md:122 (§0: protocolMajor, envelope protocolMajor, HelloV2, HelloAckV2, ExpectedRustIdentityV2 superseded); §9.1 native-evidence.md:2816-2844"
A_R123 = "native-evidence.md:123 (§0: FactBatchV2 retained unless target-attribution-v2 negotiated); §9.1 :2799-2814; §9.6 :3061-3086"
A_R124 = "native-evidence.md:124 (§0: native-evidence.schemas.v2 HelloV3/HelloAckV3/ProtocolLimitsV3 superseded by provider-handshake)"
A_R128 = "native-evidence.md:128 (§0: OpenUniverseV2, UniverseAcceptedV2, SnapshotId, PlanId, RustUniverseV1, universe-id algorithms superseded); §9.7 :3158-3203"
A_R129 = "native-evidence.md:129 (§0: frameSchemas.Coverage, CoverageV2, UnavailableV2, BudgetExhaustedV2, commitments.stageCoverage/coverageStream, StageResultV2 superseded); §9.2 :2884; §9.7 :3270-3294"
A_R130 = "native-evidence.md:130 (§0: resolved-inputs.v2 rust-v1.resolvedInputs superseded by rust-v2)"
A_F92 = "native-evidence.md:2872-2884 (§9.2 frame table)"
A_P3 = "protocol3-transitions.v1.json $.rules/$.rowPayloads (native-evidence.md:2906-2927)"
A_ECHO = "provider-startup.schemas.v1.json#/x-opensip-startup-law/identityMembers; native-evidence.md:3158-3161"
A_UNIV = "provider-startup.schemas.v1.json#/x-opensip-startup-law/universeIdentity; native-evidence.md:128, 3161-3164"
A_INH = "not named by native-evidence.md §0 (lines 112-138): retained rust-provider-protocol.v2 member"
A_DS = "native-evidence.md:2876-2879 (§9.2 DependencySource rows); §3.2 :1704-1712; protocol3-transitions P3-11..P3-15"
A_NCV = "native-evidence.md:2881; provider-startup.schemas.v1.json#/x-opensip-startup-law/nativeContextVerified; P3-20"
A_PRE = "native-evidence.md:2882, 3205-3268; provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable; P3-21"
A_LIM = "native-evidence.md:2929-2942 (§9.3); provider-handshake.schemas.v1.json#/x-opensip-wire-law/limits/rust-semantic"
A_PREP = "native-evidence.md:2880 (§9.2 'as above for inert rows only'); §3.6 :1803-1865; §0 :118, :130"
A_DISPATCH = "native-evidence.md:3024-3043 (§9.6 stage correlation); dispatch-binding.schema.v1.json"
A_C2 = "rust-provider-protocol.v2 definitions.C2PlanStageV3 -> c2-plan-stage-schema.v3.json $.stageSchemas.common + $.stageSchemas.kinds.fact-derivation; $.planAndDomainProjection.planStageByteRule"
A_FP = "rust-provider-protocol.v2 definitions.FactCandidateV1 -> fact-plane.v1.json $.factRecordContractV1.candidateSchema (wireAdjustment: canonicalRelationPayload is a byte string)"
A_ANCHOR = "fact-plane.v1.json $.factRecordContractV1.anchorSchema (reached through FactCandidateV1.anchors)"
A_RV1 = "rust-provider-protocol.v2 definitions.RustUniverseV1 -> resolved-inputs.v2.json $.planIdContract.semanticUniverseSchemas.rust-v1"

DISPOSITIONS = {"retained", "replaced", "value-substituted", "new", "removed", "unresolved"}
MEMBER_CHANGES = {None, "unchanged", "value-changed", "moved", "removed"}
# governed: an owner states the answer. owner-missing: no bounded owner states it. owner-contradictory: owners disagree.
# proposal-pending: only an unaccepted proposal answers it. implementation-choice: no wire question; root selects.
CLASSES = {"governed", "owner-missing", "owner-contradictory", "proposal-pending", "implementation-choice"}


def R(inh, w, b, d, a, *, cls="governed", r=None, ts="field-text", x=None, h=(), g=(), m=None, pres="required"):
    """One translation row. inh=inherited v2 wire type; w=major-3 wire type; b=bounds/closed vocabulary;
    d=disposition; a=authority; cls=resolution class; r=schema-native ref; ts=type source; x=derivation note;
    h=handwritten (semantic-owner) checks, each prefixed by an OWNERS key; g=gap ids; m=member change; pres=presence."""
    return {"presence": pres, "inheritedWireType": inh, "wireType": w, "boundsOrVocabulary": b, "disposition": d,
            "successorMemberChange": m, "dispositionAuthority": a, "resolutionClass": cls, "schemaNativeRef": r,
            "typeSource": ts, "derivation": x, "handwrittenChecks": list(h), "gaps": list(g)}


def F(payload, direction, terminal, d, a, *, r=None, rules=(), x=None, g=(), cls="governed"):
    """One frame row (frame name, direction, worker-terminal flag, major-3 payload)."""
    return {"payload": payload, "direction": direction, "workerTerminal": terminal, "disposition": d,
            "dispositionAuthority": a, "resolutionClass": cls, "schemaNativeRef": r, "transitionRules": list(rules),
            "derivation": x, "gaps": list(g)}


# Semantic owners (shape is the schema; these own non-shape law). (path, line|None, needle) is verified by build.py:
# for a line the needle must occur on that line; for None the needle is a JSON selector that must exist.
OWNERS = {
    "rp2.canonicalCbor": (RP2, None, "$.canonicalCbor"),
    "rp2.framing": (RP2, None, "$.framing"),
    "rp2.schemaLanguage": (RP2, None, "$.schemaLanguage"),
    "rp2.limitPolicy": (RP2, None, "$.limitPolicy"),
    "rp2.limitsHandshake": (RP2, None, "$.limitsHandshake"),
    "rp2.commitments": (RP2, None, "$.commitments"),
    "rp2.planAndDomainProjection": (RP2, None, "$.planAndDomainProjection"),
    "rp2.requestProjection": (RP2, None, "$.requestProjection"),
    "rp2.preparedOutputCustody": (RP2, None, "$.preparedOutputCustody"),
    "rp2.candidateAtomicity": (RP2, None, "$.candidateAtomicity"),
    "rp2.deterministicBudget": (RP2, None, "$.deterministicBudget"),
    "rp2.transitionAstV2": (RP2, None, "$.orderingAndStateMachine.transitionAstV2"),
    "rp2.responseProjection": (RP2, None, "$.responseProjection"),
    "p3.transitions": (P3P, None, "$.rules"),
    "hs.law": (HSP, None, "$.x-opensip-wire-law"),
    "st.law": (STP, None, "$.x-opensip-startup-law"),
    "wire.admit_hello": (WIREM, 193, "def admit_hello("),
    "wire.admit_hello_ack": (WIREM, 237, "def admit_hello_ack("),
    "wire.admit_fact_batch": (WIREM, 278, "def admit_fact_batch("),
    "start.admit_open_universe": (STARTM, 100, "def admit_open_universe("),
    "start.admit_universe_accepted": (STARTM, 143, "def admit_universe_accepted("),
    "start.admit_native_context_verified": (STARTM, 152, "def admit_native_context_verified("),
    "start.admit_unavailable": (STARTM, 161, "def admit_unavailable("),
    "start.admit_coverage_frame": (STARTM, 186, "def admit_coverage_frame("),
    "ne.protocol3_run": (NEM, 609, "def protocol3_run("),
    "ne.coverage_bijection": (NEM, 1380, "def coverage_bijection("),
    "ne.subject_scope_commitment": (NEM, 1530, "def subject_scope_commitment("),
    "ne.admit_coverage_result_v3": (NEM, 1545, "def admit_coverage_result_v3("),
    "ne.protocol3_open_universe_event": (NEM, 4579, "def protocol3_open_universe_event("),
    "ne.pre_analyze_unavailable_conversion": (NEM, 4586, "def pre_analyze_unavailable_conversion("),
    "chk2.validate_prepared": (CHK2, 739, "def validate_prepared("),
    "chk2.derive_subjects": (CHK2, 780, "def derive_subjects("),
    "chk2.validate_domain": (CHK2, 851, "def validate_domain("),
    "chk2.step_frame": (CHK2, 879, "def step_frame("),
    "dispatch": (DBP, None, "$.x-opensip-wire.correlation"),
    "fp.candidate": (FP, None, "$.factRecordContractV1.candidateSchema"),
    "fp.anchor": (FP, None, "$.factRecordContractV1.anchorSchema"),
    "fp.registry": (FP, None, "$.relationRegistry"),
    "c2.stageSchemas": (C2V3, None, "$.stageSchemas"),
    "rij.analysisDomainBinding": (RIJ, None, "$.analysisDomainBinding"),
    "rij.preparedOutputManifestBinding": (RIJ, None, "$.preparedOutputManifestBinding"),
}

GAPS = {
    "R3-G1": {
        "title": "CBOR byte strings have no JSON Schema wire mirror",
        "class": "implementation-choice",
        "finding": "SnapshotFileChunkV2.bytes, PreparedOutputChunkV2.bytes, PreparedOutputBlobV2.content, FactCandidateV1.canonicalRelationPayload and the prose-only DependencySourceChunk.bytes are CBOR byte strings (rust-provider-protocol.v2 schemaLanguage.bytes; SnapshotEntryV2.targetBytes is untyped, see R3-G15). No schema-native record carries them; fact-batch.3 canonicalRelationPayloadHex is a JSON-vector transcription only. TS2-G1's ByteString/Uint8Array carrier choice is an unaccepted proposal and is not assumed here.",
        "action": "root carrier selection; the wire stays CBOR major type 2, definite length",
    },
    "R3-G2": {
        "title": "NFC, UTF-8 byte bounds, uint64-only integers, canonical CBOR and CanonicalPath are not JSON-Schema admission",
        "class": "governed",
        "finding": "rust-provider-protocol.v2 canonicalCbor/schemaLanguage require NFC, byte-counted bounds, shortest integers, no negative integers, no floats/tags, length-first map order and decode-once/re-encode equality. The JSON Schema IdentityText maxLength counts code points (a 4096-code-point NFC string can exceed 4096 UTF-8 bytes; probe in coverage.json). native-evidence.schemas.v2 CanonicalPath's pattern admits an empty segment and a drive prefix that the v2 CanonicalPath rule refuses (probe). StageIdText maxLength 255 counts code points. Schema validity is never CBOR admission.",
        "action": "handwritten decode-once admission; no wire change",
    },
    "R3-G3": {
        "title": "Unnamed major-3 records: envelope, DependencySourceChunk and DependencySourceAccepted payloads",
        "class": "owner-missing",
        "finding": "Only the envelope protocolMajor value is superseded (native-evidence.md:122); no successor name for RustProviderEnvelopeV2 is published (audit G4). §9.2 gives DependencySourceChunk a member list and DependencySourceAccepted 'exact seal echo' with no record name (audit G5/G8). The wire carries no record names, so this is a naming/registry gap, not a wire gap.",
        "action": "root/owner naming; do not reuse RustProviderEnvelopeV2 or invent a published name",
    },
    "R3-G4": {
        "title": "subjectScopeCommitment: rust2 per-stage commitments.subjectScope vs §4.1a per-key scope2",
        "class": "owner-contradictory",
        "finding": "rust-provider-protocol.v2 coverageDomainAlgorithm puts one commitments.subjectScope value (domain opensip.rust-provider.subject-scope.v2 over the stage SubjectV2 array) in every key of a stage. native-evidence §4.1a (:1889-1947) makes key.subjectScopeCommitment the per-key scope2 over {snapshotId, sourceUniverse, targetUniverse, relation, resolution, enumeratorClosure, subjects}, and startup coverageFrames.entries requires entries[i].key.subjectScopeCommitment == keys[i]. Keys of one stage differ in relation/rung/target, so both cannot hold. §0 names neither rust2 commitments.subjectScope nor analysisDomain as superseded (§0:136 covers c2 v4 only; rust2 references c2 v3). StageAnalysisDomainV2.domainCommitment and examinedUniverse.subjectCount (len(D.subjects) vs SubjectV2) inherit the question. Proposal P-1 addresses typescript-semantic only.",
        "action": "owner decision; no recipe chosen here",
    },
    "R3-G5": {
        "title": "AnchorRefV1 member wire types unstated; fact-ref contradicts mandatory fact2",
        "class": "owner-contradictory",
        "finding": "fact-plane anchorSchema gives nullability and variants but no CBOR types for snapshotId/contentSha256/startByte/endByte/factId, and no Rust major-3 owner restates them (startup identityMembers does not list anchor snapshotId). fact-ref names FACT-ID-V1 while RustCapabilitiesV3 requires fact-identity-fact2 and identity-schemas.v3 fact anchors have no fact reference. Proposal P-2 (names rust-semantic major 3) would refuse fact-ref; it is unaccepted.",
        "action": "owner statement; recorded UNSTATED",
    },
    "R3-G6": {
        "title": "Payload selected by host state, not by a wire discriminator",
        "class": "governed",
        "finding": "FactBatch is FactBatchV2 or FactBatchV3 by target-attribution-v2 in both token arrays (handshake law factBatch; §0:123); Unavailable is PreAnalyzeUnavailableV1 in WAIT_NATIVE_CONTEXT_VERIFIED (P3-21) or UnavailableV3 in ANALYZING (P3-25) (startup law preAnalyzeUnavailable.phase). The selection is governed; the carrier form (state-parameterized decode, no tag, no try-each) is an implementation choice (TS2-G6 proposal form not assumed).",
        "action": "state-parameterized decode entry points; no wire change",
    },
    "R3-G7": {
        "title": "Same-named records inside the Rust3 wire and across languages",
        "class": "governed",
        "finding": "rust-provider-protocol.v2 CoverageKeyV2 (8 members; request key in StageAnalysisDomainV2) and native-evidence.schemas.v2 CoverageKeyV2 (5 members; CoverageResultV3 entry key, bare-hex universes) BOTH appear on the Rust major-3 wire. FactCandidateV1 is language-specific in values (producer/language/producerVersion source). StageResultV2 (5 members) is not TS StageResultV1 (7). native-evidence.schemas.v2 UnavailableReasonV3 (7 values) differs from the startup UnavailableV3.reason enum (9 values) that P3-25 actually admits; no Rust3 carrier references UnavailableReasonV3 (closure check).",
        "action": "namespace by owner $id; never merge by bare name",
    },
    "R3-G8": {
        "title": "Successor array bounds weaker than inherited derivable bounds",
        "class": "governed",
        "finding": "UnavailableV3.affectedStageIds has minItems 1 and no maxItems (derived <= maxAnalyzeStages 256); UnavailableV3/BudgetExhaustedV3.coverage have minItems 0 and no maxItems (derived 1..65536 = 256 stages x 256 keys, and <= maxFramePayloadBytes); CoverageV3.entries maxItems 4096 exceeds the derived per-stage key count <= maxRequestedCoverageKeysPerStage 256.",
        "action": "handwritten derived bounds; schema not edited",
    },
    "R3-G9": {
        "title": "PreparedOutput frames: no major-3 payload owner; inherited payload joins superseded rows",
        "class": "owner-contradictory",
        "finding": "§9.2 :2880 keeps the four PreparedOutput frames 'as above for inert rows only'. The inherited PreparedOutputManifestV2 entries (PreparedOutputEntryV2.planRow = exact rust-v1 buildScriptOutputs/procMacroOutputs row) and PreparedOutputBlobV2 variants (build-script/proc-macro owned by rust-v1 packageId/crateId) join rows that §0:130 supersedes (rust-v2 resolvedInputs carries preparedOutputSetId, PreparedOutputSetV3 rows of kinds build-script-directives|macro-expansion|generated-file). RepositoryResolutionV2.preparedOutputManifestCommitment/mode are superseded (§0:118). preparedOutputCustody.order still reads 'when repositoryResolution.mode=prepared'. startup identityMembers substitutes planId for PreparedOutputManifest/PreparedOutputAccepted but not Chunk/Seal. Whether entries stay PreparedOutputEntryV2 or become PreparedOutputRowV3-based is unstated (audit G6).",
        "action": "owner successor for PreparedOutput{Manifest,Chunk,Seal,Accepted} payloads; generate no carrier until then",
    },
    "R3-G10": {
        "title": "DependencySourceChunk and DependencySourceAccepted have no field-level schema",
        "class": "owner-missing",
        "finding": "native-evidence.md:2877 lists DependencySourceChunk {dependencySourceSetId, packageKey, path, chunkIndex, byteOffset, bytes} with no wire types, bounds or order law; maxDependencySourceChunkBytes exists (§9.3) but the frame row does not bind it. :2879 DependencySourceAccepted is 'exact seal echo after digest/VFS validation'; its shape follows DependencySourceSealV3 by echo only.",
        "action": "owner field-level publication; types recorded UNSTATED",
    },
    "R3-G11": {
        "title": "DependencySourceManifestV3.manifestSha256 recipe is self-referential; entry order and packageKey grammar unstated",
        "class": "owner-contradictory",
        "finding": "native-evidence.schemas.v2 DependencySourceManifestV3/DependencySourceSealV3 manifestSha256 carry x-opensip-digest raw-artifact 'the exact transport manifest frame bytes as sent', but manifestSha256 is itself a member of that manifest frame, so the stated preimage contains its own digest. No recipe analogous to rust2 commitments.snapshotManifest (hex SHA-256 of deterministic-CBOR(entries)) is stated. entries is x-opensip-order 'sequence' with uniqueItems and no sort key; packageKey is text 1..4096 with no grammar or join to DependencyPackageSourceV1.",
        "action": "owner recipe/order statement",
    },
    "R3-G12": {
        "title": "Coverage commitment field -> domain map unstated",
        "class": "owner-missing",
        "finding": "rust2 commitments define stageCoverage (opensip.rust-provider.stage-coverage.v2) and coverageStream (opensip.rust-provider.coverage-stream.v2), but the CoverageV2, UnavailableV2 and BudgetExhaustedV2 field texts do not name a domain for coverageCommitment; StageResultV2 says only 'v2 commitments'. §9.7 :3283-3287 lists the fields and says recipes/domains are unchanged over CoverageResultV3 values without mapping them. The v2 checker executes none of the stage/stream fact or coverage commitments; the v1 checker (not an owner) used *.v1 domains. Proposal P-4 is typescript-semantic only.",
        "action": "owner confirmation of each field's domain before implementing recipes",
    },
    "R3-G13": {
        "title": "StageResultV2 superseded with no successor record",
        "class": "owner-missing",
        "finding": "native-evidence.md:129 lists $.wireSchema.definitions.StageResultV2 as superseded for major 3, but no StageResultV3 is published; §9.7 :3286-3287 only states that StageResultV2.coverageCommitment's recipe is unchanged over CoverageResultV3 values. Members are carried here with that value substitution, pending an owner record.",
        "action": "owner record or explicit retention statement",
    },
    "R3-G14": {
        "title": "ProviderFaultV2/CancelV2/CancelledV2 member types, nullability and phase vocabulary unstated",
        "class": "owner-missing",
        "finding": "rust-provider-protocol.v2 gives field text only for ProviderFaultV2.faultKind/detailCode, CancelV2.reason and CancelledV2 'all'. executionId/analysisOrdinal types and nullability are unstated even though Cancel and ProviderFault are lawful before OpenUniverse/Analyze. ProviderFaultV2.phase has no text; CancelledV2.observedPhase is 'exact concrete phase' whose vocabulary (§0:118 phaseValues) is superseded by the 22 major-3 phases, with no statement of which subset is lawful. The v2 checker types none of these payloads; the v1 checker's types (nullable, handshake|universe|snapshot|analysis) are not an owner. BudgetExhaustedV2.observed's relation to limit is also unstated in v2.",
        "action": "owner field-level statement; recorded UNSTATED",
    },
    "R3-G15": {
        "title": "Retained v2 members whose wire types are only derivable",
        "class": "owner-missing",
        "finding": "SnapshotEntryV2.contentSha256, executable and targetBytes have no type text (variants give only nullability; targetBytes 'non-empty'). Chunk indexes/offsets and Seal/Accepted aggregates have no per-field type; this translation derives uint64 from limitPolicy.arithmetic ('count, offset ... additions use checked uint64') and records that derivation in typeSource.",
        "action": "owner confirmation; derivations are labeled, not asserted as owner text",
    },
    "R3-G16": {
        "title": "Identity echo substitution not enumerated for every carrier",
        "class": "owner-missing",
        "finding": "startup identityMembers enumerates SnapshotManifest/SnapshotSeal/SnapshotAccepted snapshotId, Analyze, PreparedOutputManifest/PreparedOutputAccepted planId, Cancel/Cancelled executionId and PreAnalyzeUnavailableV1. It does not name SnapshotFileChunkV2.snapshotId, PreparedOutputChunkV2/PreparedOutputSealV2.planId, AnchorRefV1.snapshotId, or the snapshotId inside the SubjectV2.subjectId preimage (subjectsAlgorithm), whose value necessarily changes with snapshot2 but is not restated.",
        "action": "owner enumeration; echo rows carry the transitive substitution with this gap",
    },
    "R3-G17": {
        "title": "protocol3-transitions vs retained v2 transitionAstV2: ordering divergences",
        "class": "owner-contradictory",
        "finding": "§0:118 supersedes only orderingAndStateMachine.stateRecord.phaseValues, and protocol3-transitions claims to state existing behaviour exactly. Yet (a) v2 T023 permits Cancel in START while P3-29 uses *PRE_COMPLETE, which excludes START (P3-34 FAULT); (b) v2 T019 admits Unavailable only at stageIndex 0 before any output, while P3-25 is unguarded; (c) v2 T016/T020 FactBatch and BudgetExhausted guards and the framePrecheck direction/sequence/overflow law have no P3 rows (P3 ownedByProse covers payload validation only); (d) preparedOutputCustody.order ('Disabled mode goes directly from SnapshotAccepted to Analyze') contradicts P3-08 dependency custody and P3-20. (c) is plausibly retained law; (a), (b) and (d) are divergent.",
        "action": "owner reconciliation of the major-3 machine; supervisors must not pick silently",
    },
    "R3-G18": {
        "title": "Common control protocol owner selection is a proposal",
        "class": "proposal-pending",
        "finding": "Rust provider frames own stdin/stdout (rust2 protocolIdentity.transport, framing.stdoutRule). The m1-protocol-gap-resolution-01 claim that control-protocol-contract.v2 plus control-completion.schema.v3 own common control (fd3/fd4, controlMajor independent of Rust major 3) is unaccepted and needs root registry-route confirmation; the contract's own in-file status/binds fields (coverage.json controlOwner) do not by themselves establish acceptance.",
        "action": "root confirmation; no control carrier in Rust3 provider translation",
    },
    "R3-G19": {
        "title": "Citation defect in the unaccepted gap-resolution proposal",
        "class": "proposal-pending",
        "finding": "m1-protocol-gap-resolution-01/resolutions.md cites docs/coop/artifacts/check-rust-provider-protocol.py (c190ee7f...) as 'checkRust2' (line 1048 manifest recipe; lines 852-1129 commitment structure). That checker targets rust-provider-protocol.v1.json (its line 27) and is listed in FROZEN_V1_HASHES by check-rust-provider-protocol-v2.py (line 64); its commitment domains are *.v1. The rust2 commitments text itself still states snapshotManifest = hex(SHA-256(deterministic-CBOR(entries))), so TS2-G10's Rust precedent survives, but TS2-G12's 'checkRust2 applies the same structure' support does not.",
        "action": "correct the proposal's citations before review",
    },
}
