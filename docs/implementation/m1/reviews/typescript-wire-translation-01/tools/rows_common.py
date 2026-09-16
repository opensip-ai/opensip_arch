"""Shared vocabulary for the TS2 wire translation rows (proposed implementation artifact; not product code)."""

# Wire types: exact spellings of delivery.v2 wireSchema.canonicalCbor.closedDataModel, with false|true folded to bool.
U = "uint64"
NI = "negative-int64"
T = "UTF-8-NFC-text"
B = "byte-string"
A = "definite-array"
M = "definite-text-keyed-map"
N = "null"
BOOL = "bool"
UNSTATED = "UNSTATED"

WIRE_TYPES = {U, NI, T, B, A, M, N, BOOL, UNSTATED}

# Schema-native owner $id prefixes.
HS = "opensip.product.provider-handshake.1#/$defs/"
ST = "opensip.product.provider-startup.1#/$defs/"
NE = "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/"
FB = "opensip.product.fact-batch.3#"
OC = "opensip.product.occupancy-companion.1#"

WS = "$.typescriptSemanticSubstrate.providerProtocol.wireSchema"
PP = "$.typescriptSemanticSubstrate.providerProtocol"

# Disposition authorities (native-evidence.md line numbers at sha 83b99783...).
A_HELLO = "native-evidence.md:119 (§0 row: HelloV1/HelloAckV1/protocolMajor superseded); §9.4"
A_FB = "native-evidence.md:120 (§0 row: FactBatchV1 retained unless target-attribution-v2); §9.1; §9.4; §9.6"
A_FRAMES = "native-evidence.md:121 (§0 row: frameSchemas extended with NativeContextVerified); §9.4"
A_START = "native-evidence.md:125 (§0 row: OpenUniverse/UniverseAccepted/SnapshotId/PlanId/universe/universe key superseded); §9.7"
A_RET_ID = "native-evidence.md:125 (§0 row: ExecutionId and PlanIntentCommitment retained)"
A_COV = "native-evidence.md:126 (§0 row: CoverageV1/CoverageResultV1/UnavailableV1/BudgetExhaustedV1/coverage commitments superseded); §9.7"
A_CRV1 = "native-evidence.md:116 (§0 row: CoverageResultV1.completenessRule superseded by CoverageResultV3); §4.3"
A_ORDER = "native-evidence.md:127 (§0 row: unavailableTerminal / observedPhase extended, no member added); §9.7"
A_INHERIT = "not named by native-evidence.md §0; inherited delivery.v2 member carried unchanged into major 2 (§9.4 lists every major-2 change)"
A_ECHO = "provider-startup.schemas.v1.json#/x-opensip-startup-law/identityMembers (exact-echo members carry snapshot2/plan2); native-evidence.md:3158-3161"
A_UNIV = "provider-startup.schemas.v1.json#/x-opensip-startup-law/universeIdentity; native-evidence.md:125, 3161-3164; §11"
A_SUBJ = "native-evidence.md:136 (§0 row: c2 coverageKey.key[subjectScopeCommitment] shape retained, recipe §4.1a); see TS2-G4"

# Handwritten (non-shape) check owners. Reference-model functions are executable law within their stated scope, not product code.
HANDWRITTEN_OWNERS = {
    "wire.admit_hello": "docs/coop/design-corrections/native/provider_wire_model.v1.py:193 admit_hello",
    "wire.admit_hello_ack": "docs/coop/design-corrections/native/provider_wire_model.v1.py:237 admit_hello_ack",
    "wire.admit_fact_batch": "docs/coop/design-corrections/native/provider_wire_model.v1.py:278 admit_fact_batch",
    "start.admit_open_universe": "docs/coop/design-corrections/native/provider_startup_model.v1.py:100 admit_open_universe",
    "start.admit_universe_accepted": "docs/coop/design-corrections/native/provider_startup_model.v1.py:143 admit_universe_accepted",
    "start.admit_native_context_verified": "docs/coop/design-corrections/native/provider_startup_model.v1.py:152 admit_native_context_verified",
    "start.admit_unavailable": "docs/coop/design-corrections/native/provider_startup_model.v1.py:161 admit_unavailable",
    "start.admit_coverage_frame": "docs/coop/design-corrections/native/provider_startup_model.v1.py:186 admit_coverage_frame",
    "start.typescript_protocol2_run": "docs/coop/design-corrections/native/provider_startup_model.v1.py:228 typescript_protocol2_run (+ typescript-protocol2-order.v1.json)",
    "ne.admit_coverage_result_v3": "docs/coop/design-corrections/native/native_evidence_model.v2.py:1545 admit_coverage_result_v3",
    "ne.pre_analyze_unavailable_conversion": "docs/coop/design-corrections/native/native_evidence_model.v2.py:4586 pre_analyze_unavailable_conversion",
    "d2.canonicalCbor": "delivery.v2 " + WS + ".canonicalCbor (closed maps, NFC, shortest ints, decodeRule)",
    "d2.limitRule": "delivery.v2 " + WS + ".limits.limitRule (reject before allocation; checked uint64 overflow)",
    "d2.ordering": "delivery.v2 " + PP + ".ordering (sequenceRule, stageOrder, terminals)",
    "d2.frameIntegrity": "delivery.v2 " + PP + ".frameIntegrity",
    "d2.snapshotTransport": "delivery.v2 " + PP + ".snapshotTransport",
    "d2.multiStageAnalyze": "delivery.v2 " + WS + ".multiStageAnalyze",
    "d2.stageRequestProjection": "delivery.v2 " + WS + ".stageRequestProjection",
    "d2.coverageDomain": "delivery.v2 " + WS + ".coverageDomain",
    "d2.commitments": "delivery.v2 " + WS + ".commitments",
    "d2.definitions": "delivery.v2 " + WS + ".definitions record-level rules (membershipRule, workerRule, ordering, join, completenessRule)",
    "d2.identity":"delivery.v2 $.typescriptSemanticSubstrate.identity (hostValidation)",
    "fp.candidate": "fact-plane.v1.json#factRecordContractV1 (candidateSchema, candidateToAdmittedMapping, relationPayloadSchemaRegistryV1)",
    "fp.anchor": "fact-plane.v1.json#factRecordContractV1.anchorSchema + sourceSpanSchema",
    "fp.registry": "fact-plane.v1.json#relationRegistry (+ native-evidence §4.4 unresolved-edge extension)",
    "dispatch": "docs/coop/design-corrections/native/dispatch-binding.schema.v1.json DispatchBindingV1 (native-evidence §9.6)",
}


def R(w, b, d, a, r=None, x=None, h=(), g=(), m=None, note=None):
    """One translation row. w=wire type (str, or 'X|null'); b=bounds/closed vocabulary; d=disposition;
    a=authority; r=schema-native replacement ref; x=derivation; h=handwritten checks; g=gap ids;
    m=successor member change for members of replaced records; note=free text."""
    return {
        "wireType": w,
        "boundsOrVocabulary": b,
        "disposition": d,
        "dispositionAuthority": a,
        "schemaNativeRef": r,
        "derivation": x,
        "handwrittenChecks": list(h),
        "gaps": list(g),
        "successorMemberChange": m,
        "note": note,
    }


DISPOSITIONS = {"retained", "replaced", "value-substituted", "new"}
MEMBER_CHANGES = {None, "unchanged", "value-changed", "moved", "removed"}

GAPS = {
    "TS2-G1": {
        "title": "CBOR byte-string has no selected JSON/generator representation",
        "members": ["payloadSchemas.SnapshotFileChunkV1.fields.bytes", "definitions.FactCandidateV1.fields.canonicalRelationPayload"],
        "finding": "Both are CBOR byte strings on the wire. fact-batch.schema.v3 canonicalRelationPayloadHex is a JSON-vector transcription (not a wire member, not a selected mirror); no schema-native record exists for SnapshotFileChunk bytes. Any JSON Schema mirror representation, generator tsType (e.g. Uint8Array) or Rust Vec<u8>/bytes mapping requires explicit root selection. Not chosen here.",
        "action": "root selection",
    },
    "TS2-G2": {
        "title": "NFC, UTF-8 byte bounds and canonical CBOR are not plain-JSON-Schema checkable",
        "members": ["every UTF-8-NFC-text row"],
        "finding": "Plain JSON Schema cannot validate NFC, deterministic-CBOR shortest encoding, map key order, duplicate keys or UTF-8 byte lengths (maxLength counts code points). Schema-native NfcText defs state 'NFC is checked by admission'. These remain handwritten (d2.canonicalCbor).",
        "action": "handwritten admission; no wire change",
    },
    "TS2-G3": {
        "title": "stageId text bound for StageRequestV1/StageResultV1/dependsOn not stated by a TS2 owner",
        "members": ["definitions.StageRequestV1.fields.stageId", "definitions.StageRequestV1.fields.dependsOn", "definitions.StageResultV1.fields.stageId"],
        "finding": "delivery.v2 says 'exact C-2 stageId text' with no bound; c2-plan-stage-schema.v3 (bounded read) states none. StageIdText (1..255) is published in provider-handshake.1 and provider-startup.1 and used by FactBatchV1 vector, TypeScriptCoverageV2, TypeScriptUnavailableV2 and TypeScriptBudgetExhaustedV2, which echo these values, but no owner applies it to StageRequestV1/StageResultV1 and its 255 source is uncited. Echo equality makes it the effective bound on responses only.",
        "action": "root selection whether StageIdText applies to request/result stageId members",
    },
    "TS2-G4": {
        "title": "subjectScopeCommitment value domain: delivery.v2 SubjectScopeV1 recipe vs §4.1a per-key scope2",
        "members": ["definitions.SubjectScopeV1.fields.subjectScopeCommitment", "definitions.CoverageKeyV1.fields.subjectScopeCommitment", "definitions.RequestedCoverageDomainV1.fields.subjectScope"],
        "finding": "delivery.v2: one per-stage commitment under opensip.coverage.subject-scope.v1 over sorted SnapshotFileSubjectV1, and RequestedCoverageDomainV1.workerRule requires every key.subjectScopeCommitment to equal it. native-evidence §4.1a: subjectScopeCommitment is 'sha256:'+hex of scope2 = H('subject-scope', {snapshotId, sourceUniverse, targetUniverse, relation, resolution, enumeratorClosure, subjects}), i.e. per key, checked by admit_coverage_result_v3 against CoverageResultV3.key; §9.7 requires entries[i].key.subjectScopeCommitment == keys[i].subjectScopeCommitment. §0 names no delivery.v2 SubjectScopeV1/coverageSubjectScope selector as superseded and retains wireSchema.commitments. With cross-universe keys the two rules cannot both hold. Shape (Sha256Text) is identical either way; the value recipe is unresolved here.",
        "action": "root/owner decision; do not generate a recipe",
    },
    "TS2-G5": {
        "title": "AnchorRefV1 member wire types and snapshot2/fact2 value domains unstated",
        "members": ["definitions.AnchorRefV1.required.*"],
        "finding": "delivery.v2 AnchorRefV1 has required+variants but no fields map; fact-plane anchorSchema/sourceSpanSchema give nullability and path rule but no CBOR types for snapshotId, contentSha256, startByte, endByte, factId. fact-batch.3 vector anchors items are {type: object}. startup identityMembers does not list anchor snapshotId; no bounded source states whether fact-ref factId is FACT-ID-V1 or fact2 text under fact-identity-fact2.",
        "action": "owner statement required; recorded UNSTATED, not guessed",
    },
    "TS2-G6": {
        "title": "Frame rows whose payload is selected by negotiation or phase, not by a wire discriminator",
        "members": ["frameSchemas.FactBatch", "frameSchemas.Unavailable", "frameEnvelope.fields.payload"],
        "finding": "FactBatch payload is FactBatchV1 or FactBatchV3 by HelloAck token target-attribution-v2; Unavailable payload is PreAnalyzeUnavailableV1 in WAIT_NATIVE_CONTEXT_VERIFIED or TypeScriptUnavailableV2 after Analyze. The envelope carries only frameType; selection is host state. A generated projection must expose both closed alternatives without inventing a tag or an untagged 'try each' decode.",
        "action": "root selection of projection form (e.g. per-context decode entry points); no wire change",
    },
    "TS2-G7": {
        "title": "Same-named records across owners are distinct (trace, not identity)",
        "members": ["definitions.CoverageKeyV1", "definitions.CoverageResultV1", "definitions.FactCandidateV1"],
        "finding": "See translation.md 'G7 trace'. TS CoverageKeyV1 (8 members, Sha256Text universes) stays the request key; native CoverageKeyV2 (5 members, bare-hex universes) is the CoverageResultV3 entry key; rust-provider-protocol.v2 CoverageKeyV2 is an 8-member external ref to c2 v3 coverageKey.key and is not a TS2 carrier. TS FactCandidateV1 restates fact-plane candidateSchema (14 members, identical list); Rust FactCandidateV1 is an external ref to the same candidateSchema with 'wireAdjustment: byte string'; value-domain supersession for universe ids is stated for TS by §0:125 and for Rust separately by §0:128.",
        "action": "namespace by owner/language; never merge by bare name",
    },
    "TS2-G8": {
        "title": "Successor array bounds weaker than inherited derivable bounds",
        "members": ["payloadSchemas.UnavailableV1.fields.affectedStageIds", "payloadSchemas.UnavailableV1.fields.coverage", "payloadSchemas.BudgetExhaustedV1.fields.coverage"],
        "finding": "TypeScriptUnavailableV2.affectedStageIds has minItems 1 and no maxItems; coverage arrays have minItems 0 and no maxItems. Inherited text derives affectedStageIds <= maxAnalyzeStages (1024), coverage = sum of requested keys (>= 1 since every domain is non-empty; <= 1024*128 = 131072) and the whole payload <= maxFramePayloadBytes. The derived bounds are handwritten checks; the schema-native shape is not edited.",
        "action": "handwritten admission; record only",
    },
    "TS2-G9": {
        "title": "providerProtocol.major and wireSchemaCommitment for major 2",
        "members": ["(link) $.typescriptSemanticSubstrate.providerProtocol.major", "(link) $.typescriptSemanticSubstrate.providerProtocol.wireSchemaCommitment"],
        "finding": "§0:119 sets providerProtocol.major to 2. wireSchemaCommitment (domain opensip.delivery.ts-wire-schema.v1, sha 96ffbe7b...) commits the unchanged historical wireSchema object; no bounded source says whether a major-2 projection has or needs a commitment. Neither is a wire field.",
        "action": "record; any projection-document commitment requires root selection",
    },
    "TS2-G10": {
        "title": "manifestSha256 form: DigestHex vs commitments.domains.snapshotManifest",
        "members": ["payloadSchemas.SnapshotManifestV1.fields.manifestSha256", "payloadSchemas.SnapshotSealV1.fields.manifestSha256", "payloadSchemas.SnapshotAcceptedV1.fields.manifestSha256"],
        "finding": "Field text is 'DigestHex over deterministic-CBOR entries' (bare 64 hex, no domain) while commitments.domains.snapshotManifest names opensip.ts-provider.snapshot-manifest.v1 and domainRule renders 'sha256:<hex>'. The inherited artifact does not reconcile them; text wire type is certain, pattern and preimage are not.",
        "action": "owner decision; do not choose a pattern",
    },
    "TS2-G11": {
        "title": "Unbounded text/array members with no schema-native successor bound",
        "members": ["definitions.ExecutionId", "definitions.SnapshotEntryV1.fields.path", "definitions.SnapshotEntryV1.fields.linkTarget", "payloadSchemas.SnapshotFileChunkV1.fields.path", "definitions.StageRequestV1.fields.dependsOn", "definitions.FactCandidateV1.fields.anchors"],
        "finding": "No length/count bound is stated beyond maxFramePayloadBytes (and maxAnalyzeStages for dependsOn by uniqueness over stageIds). fact-batch.3 vector bounds (anchors <= 4096, universe ids <= 4096) are JSON-vector bounds without cited wire derivation.",
        "action": "record; frame-size limit is the only derivable wire bound",
    },
    "TS2-G12": {
        "title": "Commitment domain per coverage/manifest field is name-derived, not stated",
        "members": ["payloadSchemas.CoverageV1.fields.coverageCommitment", "payloadSchemas.UnavailableV1.fields.coverageCommitment", "payloadSchemas.BudgetExhaustedV1.fields.coverageCommitment", "definitions.StageResultV1.fields.coverageCommitment", "payloadSchemas.CompleteV1.fields.coverageStreamCommitment"],
        "finding": "provider-handshake law states factCommitment->stageFacts and factStreamCommitment->factStream explicitly. For coverage, delivery.v2 lists domains stageCoverage and coverageStream but the field texts say only 'Sha256Text over deterministic-CBOR entries/coverage'; Coverage frame, Unavailable and BudgetExhausted coverageCommitment have no named domain. §9.7 says recipes and domains are unchanged over CoverageResultV3 values.",
        "action": "owner confirmation of field->domain map before implementing the recipe (link only here)",
    },
}

# Inherited links: not new wire fields.
LINKS = {
    "limits": {
        "source": WS + ".limits",
        "disposition": "retained (ten numeric members); limitRule is policy text",
        "authority": "native-evidence.md:119; §9.4",
        "schemaNativeRef": HS + "TypeScriptProtocolLimitsV1",
        "carriedOnWireAs": "TypeScriptHelloV2.limits",
    },
    "commitments": {
        "source": WS + ".commitments",
        "disposition": "retained (domainRule, eight domains, empty rule); factBatch applies to FactBatchV1.batchCommitment only; coverage domains now commit CoverageResultV3 values",
        "authority": "native-evidence.md:119, 120, 126; §9.6; §9.7",
        "schemaNativeRef": None,
    },
    "canonicalCbor": {"source": WS + ".canonicalCbor", "disposition": "retained (handwritten codec law)", "authority": A_INHERIT, "schemaNativeRef": None},
    "multiStageAnalyze": {"source": WS + ".multiStageAnalyze", "disposition": "retained; selection feeds pre-Analyze host conversion (§9.7)", "authority": A_INHERIT, "schemaNativeRef": None},
    "stageRequestProjection": {"source": WS + ".stageRequestProjection", "disposition": "retained", "authority": A_INHERIT, "schemaNativeRef": None},
    "coverageDomain": {"source": WS + ".coverageDomain", "disposition": "retained; keyConstruction universe ids take native universe identity (§0:125); producerVersion source is TypeScriptHelloAckV2.providerBuildId", "authority": A_UNIV, "schemaNativeRef": None},
    "frameIntegrity": {"source": PP + ".frameIntegrity", "disposition": "retained; uint64 BE length + 32 raw SHA-256 bytes + CBOR payload are framing, not CBOR fields", "authority": A_INHERIT, "schemaNativeRef": None},
    "major": {"source": PP + ".major", "disposition": "value-substituted 1 -> 2 (not a CBOR field)", "authority": A_HELLO, "schemaNativeRef": None},
    "wireSchemaCommitment": {"source": PP + ".wireSchemaCommitment", "disposition": "historical; see TS2-G9", "authority": "none", "schemaNativeRef": None},
    "typescriptProtocol2Order": {"source": "docs/coop/design-corrections/native/typescript-protocol2-order.v1.json", "disposition": "published abstract order table (23 rules); not a carrier", "authority": "native-evidence.md:2998-2999", "schemaNativeRef": None},
}
