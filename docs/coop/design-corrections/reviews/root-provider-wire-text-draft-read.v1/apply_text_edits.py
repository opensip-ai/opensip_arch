"""Apply the exact text corrections to the work copy. Every `old` must occur exactly once.

usage: apply_text_edits.py <work-candidate-root>
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
NE = "docs/v2/contracts/product-v1/native-evidence.md"
FB = "docs/coop/design-corrections/native/fact-batch.schema.v3.json"
OC = "docs/coop/design-corrections/native/occupancy-companion.schema.v1.json"
PR = "docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json"
PM = "docs/coop/design-corrections/foundation/provider_attribution_return_model.v2.py"
EM = "docs/coop/design-corrections/foundation/execution_inputs_model.v1.py"
EC = "docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md"
RD = "docs/coop/design-corrections/native/README.md"
NM = "docs/coop/design-corrections/native/native_evidence_model.v2.py"
CK = "docs/coop/design-corrections/native/check_native_evidence.v2.py"

ROW_118 = "| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.wireSchema.definitions.RepositoryResolutionV2`, `$.wireSchema.definitions.CoverageResultV2`, `$.wireSchema.payloadSchemas.UnavailableV2.fields.reason`, `$.limits`, `$.orderingAndStateMachine.stateRecord.phaseValues` | **Superseded** by protocol major 3 frames, identity negotiation, limits and phases (§9). |"

EDITS = [
    # ------------------------------------------------------------------ native-evidence.md
    (NE, "intro-frame-names",
     "`SubjectIdV1`). Protocol3 frame names stay; FactBatch payload version is\ncapability-gated.",
     "`SubjectIdV1`). Provider frame names stay; FactBatch payload version is\ncapability-gated per language (§9.1)."),
    (NE, "s0-rows", ROW_118, ROW_118 + "\n" + "\n".join([
        "| `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.providerProtocol.major`, `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.frameEnvelope.fields.protocolMajor`, `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.payloadSchemas.HelloV1`, `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.payloadSchemas.HelloAckV1` | **Superseded** by typescript-semantic protocol major 2 (§9.4): `major` and the envelope `protocolMajor` are 2; `TypeScriptHelloV2` / `TypeScriptHelloAckV2` (`native/provider-handshake.schemas.v1.json`) keep every inherited member, including all provider/runtime descriptor verification, replace only the protocol major value and the fixed three-token `capabilities` array, and add the token array and `identityVersions`. `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.limits` (its ten numeric members), `$.typescriptSemanticSubstrate.identity` (descriptors, `handshakeRequired`, `hostValidation`) and `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.commitments` are **retained**; `limitRule` is policy text, never a Hello member. |",
        "| `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.payloadSchemas.FactBatchV1`, `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.frameSchemas.FactBatch.payloadType`, `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.commitments.domains.factBatch` | **Retained** when `target-attribution-v2` is not negotiated; **replaced** by `FactBatchV3` (§9.6) when it is. `factBatch` commits `FactBatchV1.batchCommitment` only; `stageFacts` and `factStream` are retained whichever payload carried the candidates (§9.6). |",
        "| `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.providerProtocol.ordering.normalPhases`, `$.typescriptSemanticSubstrate.providerProtocol.closedWorkerToHostFrames`, `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.frameSchemas` | **Extended** by §9.4: worker→host frame `NativeContextVerified` (payload of §9.2) between `SnapshotAccepted` and `Analyze`. |",
        "| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.protocolIdentity.protocolMajor`, `$.wireSchema.envelope.fields.protocolMajor`, `$.wireSchema.payloadSchemas.HelloV2`, `$.wireSchema.payloadSchemas.HelloAckV2`, `$.wireSchema.definitions.ExpectedRustIdentityV2` | **Superseded** by rust-semantic protocol major 3 (§9.1): `HelloV3` / `HelloAckV3` / `ExpectedRustIdentityV3` (`native/provider-handshake.schemas.v1.json`) keep `hostBuildId`, `expectedProtocolContractSha256`, `expectedIdentity` and every identity echo, replace the major value 2 with 3 and the `RustProviderCapabilityV2` record with the token array, and add `identityVersions`. `$.limitsHandshake`, `$.limitPolicy` and `$.requestProjection.identity` are **retained** and apply to `ProtocolLimitsV3` and `HelloV3`. |",
        "| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.wireSchema.payloadSchemas.FactBatchV2`, `$.wireSchema.frameSchemas.FactBatch.payloadType` | **Retained** when `target-attribution-v2` is not negotiated; **replaced** by `FactBatchV3` (§9.6) when it is. |",
        "| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` (registered bytes kept) | `#/$defs/HelloV3`, `#/$defs/HelloAckV3`, `#/$defs/ProtocolLimitsV3` | **Superseded** by the same-named definitions of `native/provider-handshake.schemas.v1.json`. The registered document is not edited: its raw SHA-256 is a registered `payloadSchemaDigest` (§10), so a byte change there would be a schema-document successor with its own re-registration. |",
    ])),
    (NE, "s9.1-hello-carriers",
     "`HelloV3` also carries `identityVersions: {snapshot:2, plan:2, fact:2, coverage:3}`\nand `HelloAckV3` must echo the token array and identity versions exactly.",
     "Hello also carries `identityVersions: {snapshot:2, plan:2, fact:2, coverage:3}`\nand HelloAck must echo the token array and identity versions exactly, in both\nlanguages: `HelloV3`/`HelloAckV3` for `rust-semantic` (below) and\n`TypeScriptHelloV2`/`TypeScriptHelloAckV2` for `typescript-semantic` (§9.4), each\npublished field by field in `native/provider-handshake.schemas.v1.json`."),
    (NE, "s9.1-factbatch-limits-rust-hello",
     "identity token set. When present on both Hello and HelloAck, FactBatch\npayload is FactBatchV3. When absent, historical FactBatchV2 remains and\noccupancy is unknown except exact-id ephemeral. A FactBatchV3 payload\nwithout the token, or a FactBatchV2 payload with the token, is\n`PROVIDER.PROTOCOL_VIOLATION`.\nProtocol major stays 3 / TypeScript major 2. No new ProtocolLimitsV3 member;\ncompanions are bounded by existing `maxFactBatchCandidates` (4096) and\n`len(candidates)`.",
     """identity token set. When present on both Hello and HelloAck, FactBatch
payload is FactBatchV3 in either language. When absent, the historical
per-language payload remains and occupancy is unknown except exact-id
ephemeral: `typescript-semantic` keeps `delivery.v2` `FactBatchV1`
`{analysisOrdinal, stageId, batchIndex, facts, batchCommitment}` unchanged,
including its `commitments.domains.factBatch` commitment, and `rust-semantic`
keeps `rust-provider-protocol.v2` `FactBatchV2`
`{analysisOrdinal, stageId, batchIndex, candidates}` unchanged. A FactBatchV3
payload without the token, or that language's historical payload with the
token, is `PROVIDER.PROTOCOL_VIOLATION`.
Protocol major stays 3 / TypeScript major 2. The token adds no limit member in
either language; companions are bounded by the existing per-language candidate
cap — `maxFactBatchCandidates` 4096 (`rust-semantic`), `maxFactBatchFacts` 4096
(`typescript-semantic`) — and `len(candidates)`.

**Rust major-3 Hello/HelloAck (field level).** `HelloV3` =
`{protocolMajor:3, hostBuildId, expectedProtocolContractSha256, expectedIdentity,
expectedCapabilities, identityVersions, limits}` keeps every `HelloV2` member.
`hostBuildId` is unchanged. `expectedProtocolContractSha256` stays the raw SHA-256
of the exact bytes of the selected inherited contract `HelloV2` names,
`docs/coop/artifacts/rust-provider-protocol.v2.json` (pinned
`6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b`); it
authenticates the retained inherited base only, and no digest of the successor
documents is a Hello member. `expectedIdentity` (`ExpectedRustIdentityV3`) =
`{protocolMajor:3, providerBuildId, rustCommitHash, hostTriple, targetTriple,
sysrootDigest}`, copied from the selected Plan semantic-universe row's retained
`resolved-inputs.v2` `rust-v1` members of those names, which that row's
`deliveryJoin` binds to the verified signed release. `expectedCapabilities`, the
token array, replaces `RustProviderCapabilityV2`; `limits` is `ProtocolLimitsV3`
(§9.3). `HelloAckV3` = `{protocolMajor:3, providerBuildId, rustCommitHash,
hostTriple, targetTriple, sysrootDigest, capabilities, identityVersions}`: the five
identity members equal `Hello.expectedIdentity` exactly, `protocolMajor` equals
`expectedIdentity.protocolMajor`, and `capabilities` and `identityVersions` echo
Hello exactly. The major-3 successor law is identified on the wire by
`protocolMajor` 3, the token set, `identityVersions` and the exact limits map.

**Token-array order (both languages).** Token arrays are strictly unique in
ascending UTF-8 byte order and contain only that language's tokens, the four
identity tokens included. Hello carries exactly the selected signed row's tokens;
HelloAck echoes the Hello array exactly. `typescript-semantic` inherits this from
`HelloAckV1` ("exact sorted array"); for `rust-semantic` it replaces the unordered
`sequence` annotation of the superseded definition, so exact recursive equality
and token-set equality coincide. Any handshake mismatch is `FAULT` /
`PROVIDER.PROTOCOL_VIOLATION` before a source byte (step 2 below)."""),
    (NE, "s9.2-factbatch-row",
     "| `FactBatch` | worker→host | Historical `FactBatchV2` when `target-attribution-v2` is absent;",
     "| `FactBatch` | worker→host | Historical `rust-provider-protocol.v2` `FactBatchV2` when `target-attribution-v2` is absent (the `typescript-semantic` historical payload is `delivery.v2` `FactBatchV1`, §9.1);"),
    (NE, "s9.3-limits",
     "`maxGeneratedFileRows 1000000`. All 24 v2 limits are retained with identical values.",
     """`maxGeneratedFileRows 1000000`. All 24 v2 limits are retained with identical values.

`ProtocolLimitsV3` (`native/provider-handshake.schemas.v1.json`) is therefore the
closed map of exactly 32 members — the 24 `rust-provider-protocol.v2` `limits`
members with identical values plus the eight above — and it is the `rust-semantic`
`HelloV3.limits` value. `limitsHandshake` semantic and deterministic-CBOR byte
equality and `limitPolicy` apply to it unchanged; a missing, extra, renamed,
retyped or changed member refuses Hello before HelloAck. `ProtocolLimitsV3` does not
apply to `typescript-semantic`, whose limits are stated in §9.4."""),
    (NE, "s9.4-handshake-factbatch-order",
     "differing byte. `Unavailable.reason` adds `capability-missing`,\n`identity-version-mismatch`, `node-modules-outside-read-set`.",
     """differing byte. `Unavailable.reason` adds `capability-missing`,
`identity-version-mismatch`, `node-modules-outside-read-set`.

**TypeScript major-2 Hello/HelloAck (field level).** Frame names `Hello` and
`HelloAck` are unchanged; `providerProtocol.major` and the envelope `protocolMajor`
are exactly 2. `TypeScriptHelloV2` keeps the `HelloV1` members unchanged —
`hostBuildId` (non-empty NFC text), `expectedProviderDescriptorSha256`,
`expectedRuntimeDescriptorSha256`, `limits` — and adds `expectedCapabilities` and
`identityVersions`; like `HelloV1` it carries no payload `protocolMajor`. `limits`
is `TypeScriptProtocolLimitsV1`, exactly the ten numeric members of `delivery.v2`
`wireSchema.limits` with identical values: `maxFramePayloadBytes 67108864`,
`maxSnapshotChunkBytes 1048576`, `maxSnapshotEntries 200000`,
`maxAnalyzeStages 1024`, `maxRelationsPerStage 64`,
`maxRequestedCoverageKeysPerStage 128`, `maxFactBatchFacts 4096`,
`maxFactCandidatePayloadBytes 1048576`, `maxCoverageEntriesPerFrame 4096`,
`maxStderrBytes 262144`. `limitRule` is policy text and never a member, and no
`ProtocolLimitsV3` member applies. `TypeScriptHelloAckV2` keeps all 14 `HelloAckV1`
members with `protocolMajor` exactly 2 and `capabilities` the exact echo of Hello
`expectedCapabilities` (replacing the fixed three-token array), and adds the
`identityVersions` echo.

The two expected descriptor digests are the raw SHA-256 of the RFC 8785 bytes of
the verified signed `typescript-provider/identity.json` and
`typescript-runtime/identity.json` (`delivery.v2` `identity`; `resolved-inputs.v2`
`typescript-v1.deliveryJoin`). HelloAck `providerDescriptorSha256` and
`runtimeDescriptorSha256` equal them; `providerBuildId`, `protocolMajor`,
`typescriptVersion`, `typescriptCompilerSha256`, `typescriptStdlibMerkleRoot`,
`defaultWorkBudgetProfileId` and `defaultWorkBudgetProfileSha256` equal the
provider descriptor, and `nodeVersion`, `v8Version`, `modulesAbi` and `platformId`
equal the runtime descriptor (`identity.hostValidation`). Any such mismatch, and any
token-array or `identityVersions` echo mismatch under the order rule of §9.1, is
`FAULT` / `PROVIDER.PROTOCOL_VIOLATION` before a source byte. The verified
`providerBuildId` remains the source of `FactCandidateV1.producerVersion`.

**FactBatch.** Negotiated: `FactBatchV3` (§9.6). Not negotiated: `delivery.v2`
`FactBatchV1` `{analysisOrdinal, stageId, batchIndex, facts, batchCommitment}`
unchanged, `facts` capped by `maxFactBatchFacts` and
`batchCommitment = sha256:hex(SHA-256(UTF8("opensip.ts-provider.fact-batch.v1") ||
0x00 || deterministic-CBOR(facts)))` over the wire `FactCandidateV1` array.

**Order to Analyze.** The major-2 normal order is Hello/HelloAck,
OpenUniverse/UniverseAccepted, SnapshotManifest/SnapshotFileChunk*/SnapshotSeal/
SnapshotAccepted, `NativeContextVerified`, Analyze, per-stage FactBatch*/Coverage,
Complete, zero-exit/EOF; `NativeContextVerified` is a worker→host frame with the
§9.2 payload (§0)."""),
    (NE, "s9.6-stageid-name",
     "`FactBatch.stageId` (historical V2 name, preserved on V3 as",
     "`FactBatch.stageId` (historical FactBatchV1/V2 name, preserved on V3 as"),
    (NE, "s9.6-absent-payload",
     "member). Protocol majors unchanged. Historical FactBatchV2 remains the payload\nwhen the token is absent. V3 `stageId` remains C-2 text (historical type);",
     "member). Protocol majors unchanged. When the token is absent the historical\nper-language payload remains: `delivery.v2` `FactBatchV1` for `typescript-semantic`,\n`rust-provider-protocol.v2` `FactBatchV2` for `rust-semantic` (§9.1). V3 `stageId`\nremains C-2 text (historical type);"),
    (NE, "s9.6-commitments-projection",
     "corresponding request: worker echoes `StageRequestV1.stageId` /\n`StageRequestV2.planStage.stageId`.\n",
     """corresponding request: worker echoes `StageRequestV1.stageId` /
`StageRequestV2.planStage.stageId`.

**Commitments and CBOR projection.** `FactBatchV3` carries no per-batch
commitment. `typescript-semantic` `commitments.domains.factBatch` applies only to
`FactBatchV1.batchCommitment`; `typescript-semantic` `StageResultV1.factCommitment` /
`CompleteV1.factStreamCommitment` and `rust-semantic` `commitments.stageFacts` /
`factStream` remain over the ordered `FactCandidateV1` stream whichever payload
carried it. In the JSON-vector form `canonicalRelationPayloadHex` is the lowercase
hex of the wire `canonicalRelationPayload` CBOR byte string and
`decodedRelationPayload` is a verified observation that is not on the wire: the
wire candidate drops `decodedRelationPayload` and carries
`canonicalRelationPayload = bytes(canonicalRelationPayloadHex)`, and admission
requires `canonicalRelationPayloadHex = hex(deterministic-CBOR(decodedRelationPayload))`.
`native/provider_wire_model.v1.py` `admit_fact_batch` executes these wire joins for
both historical payloads and `FactBatchV3`. The occupancy entries below decide
occupancy capture only; a token-absent omission there is not validation of the
historical payload.
"""),
    (NE, "s9.6-syntax-only-row",
     "| `syntax-only` | omit token | FactBatchV2. MUST NOT invent file/package occupancy from specifier text. |",
     "| `syntax-only` | omit token | Historical FactBatch payload of its protocol (§9.1), no companion. MUST NOT invent file/package occupancy from specifier text. |"),
    (NE, "s12-case-count",
     "`native/native-cases.v2.json` (375 cases) carries hand-authored expected outcomes; every",
     "`native/native-cases.v2.json` (428 cases) carries hand-authored expected outcomes; every"),
    (NE, "s12-wire-evidence",
     "against the closed bundle, 100 definitions; workflow payloads and wrapper records against\nthe pinned workflow documents through a registry closure, no network), runs the model,\nvalidates the matrix, and writes `native/native-evidence-report.v2.json`.",
     """against the closed bundle, 115 definitions; workflow payloads and wrapper records against
the pinned workflow documents through a registry closure, no network), runs the model,
validates the matrix, and writes `native/native-evidence-report.v2.json`.
Provider handshake and FactBatch wire records validate against
`native/provider-handshake.schemas.v1.json`, whose limit maps, inherited Hello/HelloAck
members, descriptor bindings, token vocabularies and contract digest the checker re-derives
from `delivery.v2`, `rust-provider-protocol.v2`, `resolved-inputs.v2` and §9.3/§9.4 of this
contract; `native/provider_wire_model.v1.py` executes the cross-record joins (descriptor
digests and echoes, Rust identity echoes, token and `identityVersions` echoes, limit CBOR
equality, candidate CBOR projection and the TypeScript batch commitment, checked against
`hashlib`/`cbor2`-authored vectors). It frames no bytes and runs no worker."""),
    # ------------------------------------------------------------------ fact-batch.schema.v3.json
    (FB, "description-field-names",
     "Preserves historical FactBatchV2 field names analysisOrdinal, stageId, batchIndex, candidates.",
     "Preserves the historical rust-semantic FactBatchV2 field names analysisOrdinal, stageId, batchIndex, candidates (the typescript-semantic historical FactBatchV1 names its array facts and carries batchCommitment)."),
    (FB, "description-absent",
     "When the token is absent, historical FactBatchV2 remains. A V3 payload without the token, or a V2 payload with the token, is PROVIDER.PROTOCOL_VIOLATION.",
     "When the token is absent the historical per-language payload remains: typescript-semantic delivery.v2 FactBatchV1 {analysisOrdinal, stageId, batchIndex, facts, batchCommitment}; rust-semantic rust-provider-protocol.v2 FactBatchV2 {analysisOrdinal, stageId, batchIndex, candidates}. A V3 payload without the token, or that language's historical payload with the token, is PROVIDER.PROTOCOL_VIOLATION."),
    (FB, "whenAbsent",
     "    \"whenAbsent\": \"FactBatch payload MUST admit as historical FactBatchV2 (no schemaVersion, no occupancyCompanions).\",",
     "    \"whenAbsent\": \"FactBatch payload MUST admit as the negotiating language's historical payload, neither of which carries schemaVersion or occupancyCompanions: typescript-semantic delivery.v2 FactBatchV1 {analysisOrdinal, stageId, batchIndex, facts, batchCommitment} (native/provider-handshake.schemas.v1.json#/$defs/TypeScriptFactBatchV1Vector); rust-semantic rust-provider-protocol.v2 FactBatchV2 {analysisOrdinal, stageId, batchIndex, candidates} (#/$defs/RustFactBatchV2Vector).\","),
    (FB, "helloLimits-commitments-projection",
     "    \"helloLimits\": \"No new ProtocolLimitsV3 member. occupancyCompanions bounded by existing maxFactBatchCandidates 4096 and len(candidates).\",",
     "    \"helloLimits\": \"No new limit member in either language. candidates and occupancyCompanions are bounded by the language's existing candidate cap (rust-semantic maxFactBatchCandidates 4096; typescript-semantic maxFactBatchFacts 4096) and occupancyCompanions by len(candidates).\",\n"
     "    \"commitments\": \"FactBatchV3 carries no per-batch commitment. typescript-semantic delivery.v2 commitments.domains.factBatch applies only to historical FactBatchV1.batchCommitment; the stageFacts and factStream commitments of both languages remain over the ordered FactCandidateV1 stream.\",\n"
     "    \"wireProjection\": \"On the wire each candidate is FactCandidateV1 with canonicalRelationPayload = the CBOR byte string whose lowercase hex is canonicalRelationPayloadHex; decodedRelationPayload is not a wire member. Admission requires canonicalRelationPayloadHex == hex(deterministic-CBOR(decodedRelationPayload)).\","),
    # ------------------------------------------------------------------ occupancy-companion.schema.v1.json
    (OC, "historical-payloads",
     "    \"historicalFactBatchV2\": \"unchanged closed payload when the token is not negotiated\",",
     "    \"historicalFactBatchV2\": \"rust-semantic: unchanged closed rust-provider-protocol.v2 FactBatchV2 when the token is not negotiated\",\n"
     "    \"historicalFactBatchV1\": \"typescript-semantic: unchanged closed delivery.v2 FactBatchV1 {analysisOrdinal, stageId, batchIndex, facts, batchCommitment} when the token is not negotiated\","),
    (OC, "protocol-major-note",
     "payload version of FactBatch is capability-gated, not a silent field add under FactBatchV2\",",
     "payload version of FactBatch is capability-gated, not a silent field add under either historical payload\","),
    # ------------------------------------------------------------------ provider-target-attribution-return.schema.v2.json
    (PR, "ts-worker-note",
     "\"worker\": \"typescript-semantic protocol major 2. Unchanged frames.\",",
     "\"worker\": \"typescript-semantic protocol major 2 (native-evidence 9.4: TypeScriptHelloV2/TypeScriptHelloAckV2). Frame names unchanged; FactBatch payload is FactBatchV3 when target-attribution-v2 is negotiated, otherwise historical delivery.v2 FactBatchV1.\","),
    (PR, "rust-worker-note",
     "\"worker\": \"rust-semantic protocol major 3. Unchanged frames including FactBatch and CoverageV3.\",",
     "\"worker\": \"rust-semantic protocol major 3 (native-evidence 9.1: HelloV3/HelloAckV3). Frame names unchanged including FactBatch and CoverageV3; FactBatch payload is FactBatchV3 when target-attribution-v2 is negotiated, otherwise historical rust-provider-protocol.v2 FactBatchV2.\","),
    # ------------------------------------------------------------------ provider_attribution_return_model.v2.py
    (PM, "token-gate-scope",
     "def _token_gate(batch, negotiated_tokens: list):\n    tokens = list(negotiated_tokens or [])",
     "def _token_gate(batch, negotiated_tokens: list):\n"
     "    \"\"\"Occupancy-capture gate only.\n\n"
     "    Token absent: nothing is captured, and a FactBatchV3-shaped batch refuses. This is NOT\n"
     "    admission of the historical payload (typescript-semantic delivery.v2 FactBatchV1 or\n"
     "    rust-semantic FactBatchV2); that wire law is native/provider_wire_model.v1.py\n"
     "    admit_fact_batch, and a batch this gate omits has not been validated by it.\n"
     "    \"\"\"\n"
     "    tokens = list(negotiated_tokens or [])"),
    (PM, "token-gate-label",
     "            \"delivery\": \"unnegotiated-fact-batch-v2\",",
     "            \"delivery\": \"unnegotiated-historical-fact-batch\","),
    # ------------------------------------------------------------------ execution inputs
    (EM, "needed-root-note",
     "    \"FactCandidateV1/FactBatchV2 stay closed when token target-attribution-v2 is absent\",",
     "    \"FactCandidateV1 and the historical per-language FactBatch (typescript-semantic delivery.v2 FactBatchV1, \"\n"
     "    \"rust-semantic FactBatchV2) stay closed when token target-attribution-v2 is absent\","),
    (EC, "contract-absent-note",
     "Historical FactBatchV2/FactCandidateV1 stay closed when the token is absent.",
     "The historical per-language FactBatch (typescript-semantic `delivery.v2` `FactBatchV1`, rust-semantic `FactBatchV2`) and `FactCandidateV1` stay closed when the token is absent."),
    (EC, "contract-silent-field-note",
     "occupancy is a negotiated payload version, not a silent FactBatchV2 field.",
     "occupancy is a negotiated payload version, not a silent field of either historical FactBatch payload."),
    # ------------------------------------------------------------------ native README
    (RD, "readme-files",
     "context, coverage, protocol, matrix, stage authority) |",
     "context, coverage, protocol, matrix, stage authority) |\n"
     "| `provider-handshake.schemas.v1.json` | closed field-level provider handshake records: `TypeScriptHelloV2`/`TypeScriptHelloAckV2`/`TypeScriptProtocolLimitsV1` (typescript-semantic major 2), `HelloV3`/`HelloAckV3`/`ExpectedRustIdentityV3`/`ProtocolLimitsV3` (rust-semantic major 3, superseding the same-named definitions of the registered bundle), historical `TypeScriptFactBatchV1Vector`/`RustFactBatchV2Vector`, and the `x-opensip-wire-law` binding rules |\n"
     "| `provider_wire_model.v1.py` | wire reference loaded by the model: executes the handshake and FactBatch joins a schema cannot express (descriptor digests and fields, identity/token/identityVersions echoes, contract digest, limit CBOR equality, candidate CBOR projection, TypeScript batch commitment); frames nothing and qualifies no worker |"),
    (RD, "readme-selectors",
     "| superseded (protocol major 3, identity negotiation) | §9 |",
     "| superseded (protocol major 3, identity negotiation) | §9 |\n"
     "| `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.providerProtocol.major`, `...wireSchema.frameEnvelope.fields.protocolMajor`, `...wireSchema.payloadSchemas.HelloV1`, `...HelloAckV1` | superseded (typescript-semantic major 2: `TypeScriptHelloV2`/`TypeScriptHelloAckV2`, every inherited member kept) | §9.4 |\n"
     "| `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.payloadSchemas.FactBatchV1`, `...frameSchemas.FactBatch.payloadType`, `...commitments.domains.factBatch` | retained without `target-attribution-v2`; `FactBatchV3` with it | §9.1, §9.6 |\n"
     "| `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.providerProtocol.ordering.normalPhases`, `...closedWorkerToHostFrames`, `...wireSchema.frameSchemas` | extended (`NativeContextVerified` before Analyze) | §9.4 |\n"
     "| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.protocolIdentity.protocolMajor`, `$.wireSchema.envelope.fields.protocolMajor`, `$.wireSchema.payloadSchemas.HelloV2`, `...HelloAckV2`, `$.wireSchema.definitions.ExpectedRustIdentityV2` | superseded (rust-semantic major 3: `HelloV3`/`HelloAckV3`, identity and contract digest kept) | §9.1 |\n"
     "| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.wireSchema.payloadSchemas.FactBatchV2`, `$.wireSchema.frameSchemas.FactBatch.payloadType` | retained without `target-attribution-v2`; `FactBatchV3` with it | §9.1, §9.6 |\n"
     "| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` (registered bytes kept) | `#/$defs/HelloV3`, `#/$defs/HelloAckV3`, `#/$defs/ProtocolLimitsV3` | superseded by `provider-handshake.schemas.v1.json` | §0, §9 |"),
    # ------------------------------------------------------------------ native model
    (NM, "wire-reexports",
     "            \"identityNegotiated\": all(t in hello_ack for t in IDENTITY_TOKENS), \"next\": \"OpenUniverse\"}\n\n\n# The Rust major-3 transition system, READ",
     "            \"identityNegotiated\": all(t in hello_ack for t in IDENTITY_TOKENS), \"next\": \"OpenUniverse\"}\n\n\n"
     "# Provider handshake and FactBatch WIRE records (native-evidence 9.1, 9.3, 9.4, 9.6). `negotiate` above decides\n"
     "# token sets only. The field-level Hello/HelloAck records, the per-language limit maps, the historical-versus-\n"
     "# negotiated FactBatch payloads and their cross-record joins are published in provider-handshake.schemas.v1.json\n"
     "# and executed by provider_wire_model.v1.py, which carries the bytes-bearing wire CBOR this file does not.\n"
     "WIRE = _load(\"provider_wire_model_v1\", HERE / \"provider_wire_model.v1.py\")\n"
     "admit_provider_hello = WIRE.admit_hello\n"
     "admit_provider_hello_ack = WIRE.admit_hello_ack\n"
     "admit_provider_fact_batch = WIRE.admit_fact_batch\n"
     "validate_provider_wire = WIRE.validate_wire\n"
     "provider_wire_limits = WIRE.published_limits\n\n\n"
     "# The Rust major-3 transition system, READ"),
    # ------------------------------------------------------------------ native checker
    (CK, "import-re", "import json\nimport sys\n", "import json\nimport re\nimport sys\n"),
    (CK, "consumed-sources",
     "    (\"docs/v2/contracts/product-v1/native-evidence.md\", \"owned: contract these checks evidence\"),\n]",
     "    (\"docs/v2/contracts/product-v1/native-evidence.md\", \"owned: contract these checks evidence\"),\n"
     "    (\"docs/coop/design-corrections/native/provider-handshake.schemas.v1.json\", \"owned: provider handshake, limit and historical FactBatch records (section 9)\"),\n"
     "    (\"docs/coop/design-corrections/native/provider_wire_model.v1.py\", \"owned: provider wire joins loaded by the model (section 9)\"),\n"
     "    (\"docs/coop/design-corrections/native/fact-batch.schema.v3.json\", \"negotiated FactBatchV3 and the candidate vector item used by the wire model\"),\n"
     "    (\"docs/coop/design-corrections/native/occupancy-companion.schema.v1.json\", \"FactBatchV3 companion items resolved by the wire model registry\"),\n]"),
    (CK, "domain-sha-step",
     "            elif fn == \"rawSha256Canonical\":\n                result = hashlib.sha256(model.C.canonical(args[\"value\"])).hexdigest()\n",
     "            elif fn == \"rawSha256Canonical\":\n                result = hashlib.sha256(model.C.canonical(args[\"value\"])).hexdigest()\n"
     "            elif fn == \"domainSha256Hex\":\n"
     "                # hashlib oracle over an independently authored deterministic-CBOR preimage under a\n"
     "                # delivery.v2 commitment domain: sha256:hex(SHA-256(UTF8(domain) || 0x00 || bytes)).\n"
     "                result = \"sha256:\" + hashlib.sha256(args[\"domain\"].encode(\"utf-8\") + b\"\\0\" + bytes.fromhex(args[\"hex\"])).hexdigest()\n"),
    (CK, "wire-drift-controls",
     "                          \"undeclaredRepresentationSites\": undeclared_representation}\n",
     r'''                          "undeclaredRepresentationSites": undeclared_representation}

    # ---- provider handshake publication (section 9). The successor records are held to the PUBLISHED
    # inherited inputs, not to themselves: TypeScript limits are re-derived from delivery.v2 AND from the
    # section 9.4 prose; ProtocolLimitsV3 from rust-provider-protocol.v2 plus the section 9.3 prose; every
    # inherited Hello/HelloAck member must survive in its successor; every TypeScript HelloAck member must be
    # bound to a descriptor or an echo; the Rust identity has a retained Plan-row source; the contract
    # digest names real bytes.
    wire_doc = json.loads((HERE / "provider-handshake.schemas.v1.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(wire_doc)
    wire_faults: list[str] = []
    wire_open: list[str] = []
    def walk_wire(x, p):
        if isinstance(x, dict):
            if x.get("type") == "object" and "additionalProperties" not in x:
                wire_open.append(p)
            for k, v in x.items():
                walk_wire(v, p + "/" + k)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk_wire(v, p + "/" + str(i))
    walk_wire(wire_doc, "")
    wdefs = wire_doc["$defs"]
    def const_map(name):
        d = wdefs[name]
        if d.get("additionalProperties") is not False or sorted(d["required"]) != sorted(d["properties"]):
            wire_faults.append(name + ": not a closed map whose required members are exactly its properties")
        return {k: v.get("const") for k, v in d["properties"].items()}
    delivery_doc = json.loads((REPO / "docs/coop/artifacts/delivery.v2.json").read_text(encoding="utf-8"))
    rust_v2 = json.loads((REPO / "docs/coop/artifacts/rust-provider-protocol.v2.json").read_text(encoding="utf-8"))
    ts_protocol = delivery_doc["typescriptSemanticSubstrate"]["providerProtocol"]
    ts_identity = delivery_doc["typescriptSemanticSubstrate"]["identity"]
    ts_inherited = {k: v for k, v in ts_protocol["wireSchema"]["limits"].items() if k != "limitRule"}
    contract_text = (REPO / "docs/v2/contracts/product-v1/native-evidence.md").read_text(encoding="utf-8")
    def section_limits(start, end):
        body = contract_text.split(start, 1)[1].split(end, 1)[0]
        return {m.group(1): int(m.group(2)) for m in re.finditer(r"`(max\w+) (\d+)`", body)}
    ts_prose = section_limits("### 9.4 TypeScript major 2", "### 9.5")
    rust_prose = section_limits("### 9.3 Limits", "### 9.4")
    ts_published = const_map("TypeScriptProtocolLimitsV1")
    if not (same(ts_published, ts_inherited) and same(ts_prose, ts_inherited)):
        wire_faults.append(f"TypeScriptProtocolLimitsV1 {ts_published} / section 9.4 {ts_prose} != delivery.v2 numeric limits {ts_inherited}")
    rust_expected = dict(rust_v2["limits"])
    rust_expected.update(rust_prose)
    rust_published = const_map("ProtocolLimitsV3")
    if (len(rust_prose) != 8 or set(rust_prose) & set(rust_v2["limits"]) or len(rust_published) != 32
            or not same(rust_published, rust_expected)):
        wire_faults.append(f"ProtocolLimitsV3 ({len(rust_published)}) != 24 rust-provider-protocol.v2 limits + 8 section 9.3 members {rust_prose}")
    ps_ts = ts_protocol["wireSchema"]["payloadSchemas"]
    ps_rust = rust_v2["wireSchema"]["payloadSchemas"]
    for name, inherited_required in [
            ("TypeScriptHelloV2", ps_ts["HelloV1"]["required"]),
            ("TypeScriptHelloAckV2", ps_ts["HelloAckV1"]["required"]),
            ("TypeScriptHelloAckV2", ts_identity["handshakeRequired"]),
            ("HelloV3", ps_rust["HelloV2"]["required"]),
            ("HelloAckV3", ps_rust["HelloAckV2"]["required"]),
            ("ExpectedRustIdentityV3", rust_v2["wireSchema"]["definitions"]["ExpectedRustIdentityV2"]["required"]),
            ("HelloV3", model.SCHEMAS["$defs"]["HelloV3"]["required"]),
            ("HelloAckV3", model.SCHEMAS["$defs"]["HelloAckV3"]["required"])]:
        lost = sorted(set(inherited_required) - set(wdefs[name]["required"]))
        if lost:
            wire_faults.append(f"{name} drops inherited members {lost}")
    wire_law = wire_doc["x-opensip-wire-law"]
    ts_binding = wire_law["typescriptDescriptorBinding"]
    unbound = sorted(set(wdefs["TypeScriptHelloAckV2"]["required"]) - set(ts_binding["providerDescriptorFields"])
                     - set(ts_binding["runtimeDescriptorFields"])
                     - {"providerDescriptorSha256", "runtimeDescriptorSha256", "capabilities", "identityVersions"})
    if unbound:
        wire_faults.append(f"TypeScriptHelloAckV2 members bound to no descriptor or echo {unbound}")
    for kind, fields in (("provider", ts_binding["providerDescriptorFields"]), ("runtime", ts_binding["runtimeDescriptorFields"])):
        for fld in fields:
            if fld not in ts_identity[kind + "Descriptor"]["closedRequired"]:
                wire_faults.append(f"{kind} descriptor has no member {fld}")
    rust_row = json.loads((REPO / "docs/coop/artifacts/resolved-inputs.v2.json").read_text(encoding="utf-8"))[
        "planIdContract"]["semanticUniverseSchemas"]["rust-v1"]["required"]
    unsourced = sorted(set(wire_law["rustIdentityBinding"]["identityFields"]) - set(rust_row))
    if unsourced:
        wire_faults.append(f"rust-v1 Plan row carries no source for expectedIdentity members {unsourced}")
    if sha256_file(REPO / wire_law["expectedProtocolContractSha256"]["artifact"]) != wire_law["expectedProtocolContractSha256"]["sha256"]:
        wire_faults.append("expectedProtocolContractSha256 artifact bytes differ from the published digest")
    if (set(wdefs["TypeScriptCapabilityToken"]["enum"]) != set(model.TS2_TOKENS_ATTRIBUTION)
            or set(wdefs["RustCapabilityToken"]["enum"]) != set(model.RUST3_TOKENS_ATTRIBUTION)
            or list(model.WIRE.IDENTITY_TOKENS) != list(model.IDENTITY_TOKENS)):
        wire_faults.append("per-language token vocabularies differ from the section 9.1 token sets")
    if not (set(wdefs["TypeScriptCapabilityToken"]["enum"]) | set(wdefs["RustCapabilityToken"]["enum"])) <= set(model.SCHEMAS["$defs"]["CapabilityToken"]["enum"]):
        wire_faults.append("a per-language token is outside CapabilityToken")
    registered_versions = {k: v["const"] for k, v in model.SCHEMAS["$defs"]["HelloV3"]["properties"]["identityVersions"]["properties"].items()}
    if not same(const_map("IdentityVersionsV1"), registered_versions):
        wire_faults.append("identityVersions differ from the registered section 9.1 values")
    report["providerWire"] = {"document": "native/provider-handshake.schemas.v1.json", "defs": len(wdefs),
                              "openObjects": wire_open, "typescriptLimits": len(ts_published),
                              "rustLimits": len(rust_published), "section93Members": len(rust_prose),
                              "section94Members": len(ts_prose), "faults": wire_faults}
'''),
    (CK, "ok-includes-wire",
     "          and not undeclared_retention and not undeclared_representation)",
     "          and not undeclared_retention and not undeclared_representation\n          and not wire_faults and not wire_open)"),
    (CK, "limitations-wire",
     "        \"No cell is QUALIFIED; the four platform families are asserted design-invariant only.\",\n    ]",
     "        \"No cell is QUALIFIED; the four platform families are asserted design-invariant only.\",\n"
     "        \"Provider handshake and FactBatch records are JSON vectors: frame length/digest/sequence bytes, process lifetime and compiler output are not exercised, and descriptor digests hash canonical.py bytes, which equal RFC 8785 only for the fixture value domain.\",\n    ]"),
    (CK, "print-wire-faults",
     "    for path in undeclared_retention + undeclared_representation:\n        print(\"FAIL digest-law vocabulary:\", path)\n",
     "    for path in undeclared_retention + undeclared_representation:\n        print(\"FAIL digest-law vocabulary:\", path)\n"
     "    for fault in wire_faults + [\"open object \" + p for p in wire_open]:\n        print(\"FAIL provider-wire:\", fault)\n"),
]

log = []
for rel, label, old, new in EDITS:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{rel} [{label}]: expected exactly one occurrence, found {count}")
    before = hashlib.sha256(text.encode("utf-8")).hexdigest()
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    log.append({"file": rel, "edit": label, "beforeSha256": before,
                "afterSha256": hashlib.sha256(text.encode("utf-8")).hexdigest()})
for rel in sorted({e[0] for e in EDITS}):
    if rel.endswith(".json"):
        json.loads((ROOT / rel).read_text(encoding="utf-8"))
print(json.dumps({"applied": len(log), "edits": log}, indent=1))
