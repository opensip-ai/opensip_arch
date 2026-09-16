# TS2 wire translation inventory: `typescript-semantic` protocol major 2

**Standing.** This is a proposed implementation artifact for root review. It is not an approval, a wire change, a schema document or product code. It supplies the TS2 projection input that audit `m1-generation-owner-audit-01` marks as missing (T1; precision gaps G1–G3 and G7).

**Scope.** Every member of the inherited `docs/coop/artifacts/delivery.v2.json` `$.typescriptSemanticSubstrate.providerProtocol.wireSchema` sections `frameEnvelope`, `frameSchemas`, `definitions` and `payloadSchemas`. Each member is translated to major 2 under the dispositions of `docs/v2/contracts/product-v1/native-evidence.md` §0 (superseded selectors), §9.1, §9.4, §9.5 and §9.7. The exact native handshake and startup schema documents (`native/provider-handshake.schemas.v1.json`, `native/provider-startup.schemas.v1.json`) govern every replacement they specify. The following were **not** used: delivery v3–v5 and rust-provider-protocol v1/v3/v4. No original byte was rewritten. The candidate source45 and application46 design is taken as complete and is not re-reviewed.

**Machine form.** `fields.json` holds every row, including the exact original text, source path, SHA and selector. `coverage.json` holds the counts. `tools/build.py` regenerates both files and this document from `tools/rows_*.py`. It opens sources read-only and fails on any uncovered or extra member, unresolvable ref, wire-type mismatch against a resolvable ref, or unexpected successor member delta.

```
OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch python3 tools/build.py
```

## 1. Coverage

- original members tabulated: **182** (rows 182; frameSchemas 16, frameEnvelope 4, definitions 78, payloadSchemas 84)
- new schema-native member rows: **18**
- dispositions (rows+new): {"value-substituted": 15, "retained": 106, "replaced": 61, "new": 18}
- rows with schema-native ref: 92; with handwritten checks: 114; citing gaps: 40
- wire-type cross-checks against resolved refs: 83 checked, 0 mismatches
- required-list comparisons: 28; successor member-list comparisons: 12
- script failures: 0


## 2. Conventions

- **Wire type** uses the spellings of delivery.v2 `canonicalCbor.closedDataModel`: `null`, `bool` (false|true), `uint64`, `negative-int64`, `UTF-8-NFC-text`, `byte-string`, `definite-array`, `definite-text-keyed-map`. `X|null` means nullable. `UNSTATED` means no bounded source states the CBOR type; the row cites a gap and makes no guess. No TS2 member uses `negative-int64`.
- **Disposition:**
  - `retained`: shape and value domain unchanged.
  - `replaced`: a schema-native successor owns the member. `successorMemberChange` is one of `unchanged`, `value-changed`, `moved` or `removed`.
  - `value-substituted`: name and shape are kept, but a stated supersession replaces the value domain. Examples are snapshot2/plan2 echoes and native universe identity.
  - `new`: the member is absent from delivery.v2 and is published schema-natively.
- **Schema-native ref** is an `$id#pointer` in a registered owner document. When a ref points into `fact-batch.3` candidate items or `TypeScriptFactBatchV1Vector`, it names a **JSON-vector** mirror. That mirror's `canonicalRelationPayloadHex`/`decodedRelationPayload` pair is a transcription and an observation, not a wire representation.
- **Handwritten checks** are listed apart from shape. They cover joins, echoes, provenance, NFC, canonical CBOR, ordering, commitments and limits. Owner keys map to reference executable law (see `fields.json conventions.handwrittenOwners`). Those functions are models within their stated scope, not the implementation's admission code.
- **Byte strings.** `SnapshotFileChunkV1.bytes` and `FactCandidateV1.canonicalRelationPayload` are recorded only as `byte-string`. A JSON Schema mirror, a generator `tsType` or a Rust `Vec<u8>`/`bytes` mapping each needs explicit root selection (TS2-G1). Plain JSON Schema also cannot validate NFC, UTF-8 byte lengths, deterministic-CBOR encoding or map order (TS2-G2).

## 3. Envelope

The major-2 envelope keeps the four inherited members `{protocolMajor, frameType, sequence, payload}`, all required, with no optional members. The only value change is `protocolMajor`, from exactly 1 to **exactly 2** (native-evidence.md:119). `frameType` gains one worker→host vocabulary member, `NativeContextVerified` (native-evidence.md:121). The proposed implementation record name is **`TypeScriptFrameV2`**. That is a name for generated/handwritten code only; it is not a wire field or wire name, and the wire carries none. Framing bytes (uint64 big-endian length, 32 raw SHA-256 bytes, then the CBOR payload) come from `providerProtocol.frameIntegrity` and are not CBOR members. The payload type is selected by `frameType` except in two cases, where host state selects it instead (TS2-G6):
- `FactBatch` is selected by negotiation.
- `Unavailable` is selected by phase.

## 4. Stage identity: logical C-2 text vs Analyze ordinals vs Plan ordinals

| carrier | member | wire | meaning |
|---|---|---|---|
| `StageRequestV1` | `stageId` | text | exact logical C-2 `stageId` **text**, copied from the verified Plan; unique within Analyze |
| `StageRequestV1` | `stageOrdinal` | uint64 | contiguous 0..n-1 in **this Analyze** request order (= `DispatchBindingV1.analyzeRequestOrdinal`) |
| `StageRequestV1` | `dependsOn` | array of text | C-2 `stageId` texts, sorted unique, `[]` when absent |
| `FactBatchV1` / `FactBatchV3` | `stageId` | text (StageIdText 1..255) | echo of current `StageRequestV1.stageId`; **not** `stageOrdinal`, **not** `execution-plan.stages[].ordinal` |
| `TypeScriptCoverageV2` | `stageId` | text | attributes every `CoverageResultV3` entry (entries carry no stageId/entryOrdinal) |
| `TypeScriptUnavailableV2` | `affectedStageIds` | array of text | all requested stageIds, request order |
| `TypeScriptBudgetExhaustedV2` | `triggerStageId` | text | one requested stageId |
| `StageResultV1` | `stageId`, `stageOrdinal` | text, uint64 | exact requested values |
| `PreAnalyzeUnavailableV1` | — | — | no stage member; host derives affected stages from `multiStageAnalyze.selection` |

`AnalyzeV1.stageRequests` may be a **subset** of the Plan stages. The Plan ordinal (`retainedStageOrdinal`) exists only in host `DispatchBindingV1` and is never on the TS2 wire. `analyzeRequestOrdinal` must not be equated with it (native-evidence.md:3024-3043). The inherited text states no length bound for request/result `stageId` (TS2-G3).

## 5. FactBatch: historical V1 vs negotiated V3

| aspect | historical `FactBatchV1` (token `target-attribution-v2` absent) | negotiated `FactBatchV3` (token in Hello **and** HelloAck) |
|---|---|---|
| owner | delivery.v2 `payloadSchemas.FactBatchV1` (retained, native-evidence.md:120); JSON vector `provider-handshake.1#/$defs/TypeScriptFactBatchV1Vector` | `opensip.product.fact-batch.3` |
| members | `analysisOrdinal, stageId, batchIndex, facts, batchCommitment` | `schemaVersion(3), analysisOrdinal, stageId, batchIndex, candidates, occupancyCompanions` |
| candidate array name | `facts` | `candidates` |
| per-batch commitment | `batchCommitment`, domain `opensip.ts-provider.fact-batch.v1` over deterministic-CBOR(facts) | none |
| companions | none; occupancy unknown except exact-id ephemeral | `occupancyCompanions[]` of `OccupancyCompanionV1`, associated by `candidateOrdinal`, length ≤ len(candidates) |
| cap | `maxFactBatchFacts` 4096 | same cap; no new limit member |
| wrong payload for negotiation state | `PROVIDER.PROTOCOL_VIOLATION` | `PROVIDER.PROTOCOL_VIOLATION` |
| stage/stream commitments | `StageResultV1.factCommitment` (stageFacts) and `CompleteV1.factStreamCommitment` (factStream) apply over the ordered `FactCandidateV1` stream, whichever payload carried it | same |

`FactCandidateV1` is unchanged under both payloads and has no occupancy member. Its universe-id members are value-substituted (§7 rows).

## 5a. G7 trace: same-named records are distinct

- **FactCandidateV1.** delivery.v2 TS `FactCandidateV1` restates `fact-plane.v1 candidateSchema` with an identical 14-member required list (asserted). `rust-provider-protocol.v2` `FactCandidateV1` is only an external ref to that candidateSchema, adjusted to a byte string. Supersession of universe-id values is stated separately per language: TS at native-evidence.md:125, Rust at :128. Producer, language and producerVersion sources differ by provider. The two records must not be merged by bare name.
- **CoverageKey.** Three distinct records share the name:
  - The TS `CoverageKeyV1` stays the **request key** in `RequestedCoverageDomainV1.keys`. It has 8 members and its universe ids are Sha256Text in the native universe identity.
  - The native-evidence `CoverageKeyV2` is the **entry key** inside `CoverageResultV3`. It has 5 members, bare-hex `sourceUniverse`/`targetUniverse`, and no producer, producerVersion or schemaVersion.
  - `rust-provider-protocol.v2` `CoverageKeyV2` is an 8-member external ref to c2 v3 `coverageKey.key`. It is not a TS2 carrier.
- **Subject-scope commitment.** The inherited per-stage recipe conflicts with the §4.1a per-key `scope2` recipe (TS2-G4). This is recorded as open and was not decided here.


## 6. Frame table (TS2)

| frame | TS2 payload / terminal | disposition | schema-native ref | notes |
|---|---|---|---|---|
| Hello | host-to-worker; payloadType TypeScriptHelloV2; terminal false | replaced | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloV2 | frame name retained; payloadType replaced  |
| OpenUniverse | host-to-worker; payloadType TypeScriptOpenUniverseV2; terminal false | replaced | opensip.product.provider-startup.1#/$defs/TypeScriptOpenUniverseV2 | frame name retained; payloadType replaced  |
| SnapshotManifest | host-to-worker; payloadType SnapshotManifestV1; terminal false | retained |  |   |
| SnapshotFileChunk | host-to-worker; payloadType SnapshotFileChunkV1; terminal false | retained |  |   |
| SnapshotSeal | host-to-worker; payloadType SnapshotSealV1; terminal false | retained |  |   |
| Analyze | host-to-worker; payloadType AnalyzeV1; terminal false | retained |  | retained; NativeContextVerified now precedes it (native-evidence.md:2992-2996)  |
| Cancel | host-to-worker; payloadType CancelV1; terminal true | retained |  |   |
| HelloAck | worker-to-host; payloadType TypeScriptHelloAckV2; terminal false | replaced | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2 | frame name retained; payloadType replaced  |
| UniverseAccepted | worker-to-host; payloadType TypeScriptUniverseAcceptedV2; terminal false | replaced | opensip.product.provider-startup.1#/$defs/TypeScriptUniverseAcceptedV2 | frame name retained; payloadType replaced  |
| SnapshotAccepted | worker-to-host; payloadType SnapshotAcceptedV1; terminal false | retained |  |   |
| FactBatch | worker-to-host; payloadType FactBatchV1 when target-attribution-v2 NOT negotiated, FactBatchV3 when negotiated; terminal false | retained | opensip.product.fact-batch.3# | Historical payloadType retained; negotiated alternative is schema-native opensip.product.fact-batch.3 TS2-G6 |
| Coverage | worker-to-host; payloadType TypeScriptCoverageV2; terminal false | replaced | opensip.product.provider-startup.1#/$defs/TypeScriptCoverageV2 | frame name Coverage retained (not CoverageV3)  |
| Unavailable | worker-to-host; payloadType PreAnalyzeUnavailableV1 in WAIT_NATIVE_CONTEXT_VERIFIED, TypeScriptUnavailableV2 immediately after Analyze; terminal true | replaced | opensip.product.provider-startup.1#/$defs/TypeScriptUnavailableV2 | second alternative opensip.product.provider-startup.1#/$defs/PreAnalyzeUnavailableV1 TS2-G6 |
| BudgetExhausted | worker-to-host; payloadType TypeScriptBudgetExhaustedV2; terminal true | replaced | opensip.product.provider-startup.1#/$defs/TypeScriptBudgetExhaustedV2 |   |
| Complete | worker-to-host; payloadType CompleteV1; terminal true | retained |  |   |
| Cancelled | worker-to-host; payloadType CancelledV1; terminal true | retained |  |   |
| NativeContextVerified | worker-to-host; payloadType NativeContextVerifiedV1; terminal false | new | opensip.product.provider-startup.1#/$defs/NativeContextVerifiedV1 | native-evidence.md:121, 2881 |

## 7. Field rows (every inherited member)

Columns: member · presence · wire type · bounds / closed vocabulary · disposition (member change) · schema-native ref · derivation · handwritten checks · gaps. Source for every row: `docs/coop/artifacts/delivery.v2.json` sha256 `47b6cfd1…e3cabf3`, selector `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.<member>`; exact original text is in fields.json `rows[].source.originalText`.

### frameEnvelope

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| protocolMajor | required | uint64 | exactly 2 (inherited 'exactly 1') | value-substituted |  | provider-handshake.schemas.v1.json#/x-opensip-wire-law/frameAndMajor/typescript-semantic; Envelope record proposed implementation name TypeScriptFrameV2 (not a wire field or wire name). | wire.admit_hello / wire.admit_hello_ack: envelope_protocol_major == 2 before payload admission |  |
| frameType | required | UTF-8-NFC-text | closed per direction. host->worker (7): Hello, OpenUniverse, SnapshotManifest, SnapshotFileChunk, SnapshotSeal, Analyze, Cancel. worker->host (10): HelloAck, UniverseAccepted, SnapshotAccepted, NativeContextVerified, FactBatch, Coverage, Unavailable, BudgetExhausted, Complete, Cancelled | retained |  | vocabulary = closedHostToWorkerFrames / closedWorkerToHostFrames + NativeContextVerified (worker->host); typescript-protocol2-order.v1.json rule frames agree; Member retained; vocabulary extended by one worker->host member. Rust-only CoverageV3 frame name does not apply (native-evidence.md:3000-3001). | d2.ordering + start.typescript_protocol2_run: frame lawful in phase; unknown frame -> PROVIDER.PROTOCOL_VIOLATION; TS2-G2 |  |
| sequence | required | uint64 | per direction, starts 0, +1; overflow refused | retained |  |  | d2.ordering.sequenceRule |  |
| payload | required | definite-text-keyed-map | closed map selected by frameSchemas[frameType].payloadType (TS2 table below) | retained |  |  | d2.canonicalCbor: decodeRule, decode once under selected closed schema; d2.limitRule: <= maxFramePayloadBytes 67108864 | TS2-G6 |

### definitions (string definitions)

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| DigestHex | n/a (string definition) | UTF-8-NFC-text | ^[0-9a-f]{64}$ | retained | opensip.product.provider-handshake.1#/$defs/DigestHex | schema-native pattern uses (?![\s\S]) end anchor; same language (no trailing newline) |  |  |
| Sha256Text | n/a (string definition) | UTF-8-NFC-text | ^sha256:[0-9a-f]{64}$ | retained | opensip.product.provider-handshake.1#/$defs/Sha256Text |  |  |  |
| ExecutionId | n/a (string definition) | UTF-8-NFC-text | non-empty; no length bound stated | retained | opensip.product.provider-startup.1#/$defs/ExecutionIdText |  | start.admit_open_universe: exact AttemptRecord value; TS2-G2 | TS2-G11 |
| SnapshotId | n/a (string definition) | UTF-8-NFC-text | ^snapshot2:[0-9a-f]{64}$ (inherited: canonical sealed SnapshotId text) | replaced | opensip.product.provider-startup.1#/$defs/SnapshotId2 |  | start.admit_open_universe: equals verified Plan snapshot2 |  |
| PlanId | n/a (string definition) | UTF-8-NFC-text | ^plan2:[0-9a-f]{64}$ (inherited: ^plan1:sha256:[0-9a-f]{64}$) | replaced | opensip.product.provider-startup.1#/$defs/PlanId2 |  | start.admit_open_universe: equals verified plan2 |  |
| PlanIntentCommitment | n/a (string definition) | UTF-8-NFC-text | ^sha256:[0-9a-f]{64}$ | retained | opensip.product.provider-startup.1#/$defs/Sha256Text | TypeScriptOpenUniverseV2.planIntentCommitment $ref Sha256Text | exact AttemptRecord/ExecutionPlan value |  |
| TypeScriptSemanticUniverseV1 | n/a (string definition) | definite-text-keyed-map | closed 19-member map (typescript-v1 map, protocolMajor 2, resolvedInputs TypeScriptUniverseV2ResolvedInputs) | replaced | opensip.product.provider-startup.1#/$defs/TypeScriptSemanticUniverseV2 |  | start.admit_open_universe: 11-member handshakeJoin with TypeScriptHelloAckV2; nativeContextId suffix in plan.nativeContextDigests |  |
| TypeScriptSemanticUniverseKey | n/a (string definition) | UTF-8-NFC-text | Sha256Text; native semantic-universe identity sha256:hex(H(native.semantic-universe.<language>.v2, universe.resolvedInputs)) (inherited recipe opensip.typescript-universe.v1 superseded) | replaced | opensip.product.provider-startup.1#/$defs/Sha256Text | TypeScriptOpenUniverseV2.universeKey $ref Sha256Text; recipe in startup law universeIdentity; type name has no schema-native def; every member typed by it is value-substituted | host and worker recompute (start.admit_universe_accepted) |  |

### definitions.SnapshotEntryV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| path | required | UTF-8-NFC-text | non-empty normalized project-relative; entries strictly sorted by UTF-8 bytes, unique; no length bound | retained |  |  | d2.snapshotTransport: normalization, ordering, uniqueness; TS2-G2 | TS2-G11 |
| kind | required | UTF-8-NFC-text | enum file\|symlink | retained |  |  |  |  |
| byteLength | required | uint64 | file byte length; 0 for symlink | retained |  |  | conditional on kind |  |
| contentSha256 | required | UTF-8-NFC-text\|null | DigestHex for file; null for symlink | retained |  |  | conditional on kind (plain schema needs if/then; see audit TF-2) |  |
| linkTarget | required | UTF-8-NFC-text\|null | normalized sealed link-target text for symlink; null for file; no length bound | retained |  |  | conditional on kind | TS2-G11 |

### definitions.ProviderWorkBudgetV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| sourceFilesVisited | required | uint64 | uint64 maximum; zero permits zero ops; no unlimited sentinel. Projected value: work-units L in 1..9223372036854775807 for all six, else profile default | retained |  |  | d2.stageRequestProjection.budgetProjection (sole budget authority) |  |
| astNodesVisited | required | uint64 | uint64 maximum; zero permits zero ops; no unlimited sentinel. Projected value: work-units L in 1..9223372036854775807 for all six, else profile default | retained |  |  | d2.stageRequestProjection.budgetProjection (sole budget authority) |  |
| moduleResolutionQueries | required | uint64 | uint64 maximum; zero permits zero ops; no unlimited sentinel. Projected value: work-units L in 1..9223372036854775807 for all six, else profile default | retained |  |  | d2.stageRequestProjection.budgetProjection (sole budget authority) |  |
| typeQueries | required | uint64 | uint64 maximum; zero permits zero ops; no unlimited sentinel. Projected value: work-units L in 1..9223372036854775807 for all six, else profile default | retained |  |  | d2.stageRequestProjection.budgetProjection (sole budget authority) |  |
| factsEmitted | required | uint64 | uint64 maximum; zero permits zero ops; no unlimited sentinel. Projected value: work-units L in 1..9223372036854775807 for all six, else profile default | retained |  |  | d2.stageRequestProjection.budgetProjection (sole budget authority) |  |
| factBytesEmitted | required | uint64 | uint64 maximum; zero permits zero ops; no unlimited sentinel. Projected value: work-units L in 1..9223372036854775807 for all six, else profile default | retained |  |  | d2.stageRequestProjection.budgetProjection (sole budget authority) |  |

### definitions.StageRequestV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| stageId | required | UTF-8-NFC-text | logical C-2 stageId TEXT copied exactly; unique within Analyze; bound unstated | retained |  | StageIdText 1..255 exists schema-natively for echoes only (see TS2-G3) | d2.stageRequestProjection: copy stage.stageId; dispatch: text is not stageOrdinal and not execution-plan.stages[].ordinal (native-evidence.md:3024-3043); TS2-G2 | TS2-G3 |
| stageOrdinal | required | uint64 | contiguous 0..n-1 in THIS Analyze order (n <= maxAnalyzeStages 1024) | retained |  |  | dispatch: equals DispatchBindingV1.analyzeRequestOrdinal; MUST NOT equal-by-assumption retainedStageOrdinal (Analyze may be a Plan subset) |  |
| operator | required | UTF-8-NFC-text | const semantic-provider | retained |  |  |  |  |
| providerId | required | UTF-8-NFC-text | const typescript-semantic | retained |  |  |  |  |
| dependsOn | required | definite-array | items C-2 stageId text; sorted unique; [] when C-2 absent; earlier stageRequest or completed external stage | retained |  |  | d2.multiStageAnalyze.batchability; d2.stageRequestProjection.dependsOn | TS2-G3 TS2-G11 |
| relations | required | definite-array | items text; non-empty sorted unique; <= maxRelationsPerStage 64; vocabulary = typescript relation map {declares, imports, references, calls, types, reachability} within live registry (native Relation enum adds unresolved-edge) | retained |  |  | fp.registry; d2.coverageDomain.relationSource; d2.limitRule |  |
| budget | required | definite-text-keyed-map | ProviderWorkBudgetV1 | retained |  |  |  |  |
| requestedCoverageDomain | required | definite-text-keyed-map | RequestedCoverageDomainV1 | retained |  | field text names CoverageResultV1; answering entries are now CoverageResultV3 (value meaning only) |  |  |

### definitions.SnapshotFileSubjectV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| path | required | UTF-8-NFC-text | exact kind=file manifest entry path; strict ascending UTF-8, unique | retained |  | exact echo of SnapshotEntryV1.path | reconstructed by both sides from accepted manifest |  |
| contentSha256 | required | UTF-8-NFC-text | DigestHex (non-null: file entries only) | retained |  | exact echo of SnapshotEntryV1.contentSha256 file branch |  |  |
| byteLength | required | uint64 | exact entry byteLength | retained |  | exact echo of SnapshotEntryV1.byteLength |  |  |

### definitions.SubjectScopeV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| scopeKind | required | UTF-8-NFC-text | const all-snapshot-files | retained |  |  |  |  |
| snapshotId | required | UTF-8-NFC-text | ^snapshot2:[0-9a-f]{64}$ via exact OpenUniverse echo | value-substituted | opensip.product.provider-startup.1#/$defs/SnapshotId2 | exact OpenUniverse SnapshotId; startup law lists SubjectScopeV1 snapshotId |  |  |
| subjectCount | required | uint64 | exact count of kind=file manifest entries (<= maxSnapshotEntries 200000) | retained |  |  |  |  |
| subjectScopeCommitment | required | UTF-8-NFC-text | Sha256Text; inherited recipe opensip.coverage.subject-scope.v1 over sorted SnapshotFileSubjectV1 | retained |  | shape retained; value recipe conflict recorded | recompute (both sides) | TS2-G4 |

### definitions.RequestedCoverageDomainV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| subjectScope | required | definite-text-keyed-map | SubjectScopeV1 | retained |  |  | d2.definitions: RequestedCoverageDomainV1.workerRule, every key.subjectScopeCommitment equals subjectScope's | TS2-G4 |
| keys | required | definite-array | items CoverageKeyV1 map; non-empty; sorted by deterministic-CBOR bytes, unique; <= maxRequestedCoverageKeysPerStage 128 | retained |  | item universe members value-substituted (see CoverageKeyV1) | d2.coverageDomain.keyConstruction/cardinality/overflowFate |  |
| domainCommitment | required | UTF-8-NFC-text | Sha256Text; domain opensip.ts-provider.requested-coverage-domain.v1 over {subjectScope, keys} | retained |  | recipe unchanged; committed value changes with substituted key universe ids | d2.commitments; worker recomputes before analysis |  |

### definitions.AnchorRefV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| kind | required | UTF-8-NFC-text | enum source-span\|fact-ref | retained |  | variants keys of AnchorRefV1 / fp anchorSchema | fp.anchor; anchors sorted by deterministic-CBOR bytes, unique |  |
| snapshotId | required | UNSTATED\|null | non-null for source-span, null for fact-ref; CBOR type and snapshot2 domain unstated | retained |  |  | fp.anchor | TS2-G5 |
| path | required | UTF-8-NFC-text\|null | source-span: normalized project-relative NFC path of a sealed file; fact-ref: null | retained |  | fact-plane sourceSpanSchema.rule | fp.anchor; TS2-G2 | TS2-G5 |
| contentSha256 | required | UNSTATED\|null | source-span: sealed file content digest (form unstated); fact-ref: null | retained |  |  | fp.anchor | TS2-G5 |
| startByte | required | UNSTATED\|null | source-span: [startByte,endByte) non-empty, in sealed bytes; integer type unstated; fact-ref: null | retained |  |  | fp.anchor | TS2-G5 |
| endByte | required | UNSTATED\|null | as startByte | retained |  |  | fp.anchor | TS2-G5 |
| factId | required | UNSTATED\|null | fact-ref: already-admitted fact identity (FACT-ID-V1 vs fact2 unstated); source-span: null | retained |  |  | fp.anchor: earlier admitted fact only | TS2-G5 |

### definitions.FactCandidateV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| candidateOrdinal | required | uint64 | contiguous within stage across FactBatch frames | retained | opensip.product.fact-batch.3#/properties/candidates/items/properties/candidateOrdinal |  | dispatch: first ordinal == expectedFirstCandidateOrdinal; never enters fact identity |  |
| relation | required | UTF-8-NFC-text | live relationRegistry key requested by stage; vector maxLength 64 | retained | opensip.product.fact-batch.3#/properties/candidates/items/properties/relation |  | fp.registry; TS2-G2 |  |
| resolution | required | UTF-8-NFC-text | rung of relation's live ladder; vector maxLength 64 | retained | opensip.product.fact-batch.3#/properties/candidates/items/properties/resolution |  | fp.registry |  |
| layer | required | UTF-8-NFC-text | relation's exact live layer; registry layers {derived, inventory, semantic, syntax}; vector maxLength 64 | retained | opensip.product.fact-batch.3#/properties/candidates/items/properties/layer |  | fp.registry |  |
| producer | required | UTF-8-NFC-text | const typescript-semantic; vector maxLength 128 | retained | opensip.product.fact-batch.3#/properties/candidates/items/properties/producer |  |  |  |
| producerVersion | required | UTF-8-NFC-text | exact verified providerBuildId; vector maxLength 256 | retained | opensip.product.fact-batch.3#/properties/candidates/items/properties/producerVersion | source now TypeScriptHelloAckV2.providerBuildId (native-evidence.md:2983-2984) | wire.admit_hello_ack; TS2-G2 |  |
| schemaVersion | required | uint64 | relation payload schema version (host registry) | retained | opensip.product.fact-batch.3#/properties/candidates/items/properties/schemaVersion |  | fp.candidate |  |
| language | required | UTF-8-NFC-text | const typescript; vector maxLength 64 | retained | opensip.product.fact-batch.3#/properties/candidates/items/properties/language |  |  |  |
| sourceUniverseId | required | UTF-8-NFC-text | Sha256Text; native semantic-universe identity sha256:hex(H(native.semantic-universe.<language>.v2, universe.resolvedInputs)) (inherited recipe opensip.typescript-universe.v1 superseded); vector maxLength 4096 | value-substituted | opensip.product.fact-batch.3#/properties/candidates/items/properties/sourceUniverseId |  | equals OpenUniverse.universeKey |  |
| targetUniverseId | required | UTF-8-NFC-text | native semantic-universe identity (Sha256Text) of the target universe (typescript or rust v2); required every fact; vector maxLength 4096 | value-substituted | opensip.product.fact-batch.3#/properties/candidates/items/properties/targetUniverseId |  | member of host-admitted target domain (d2.coverageDomain.targetPartition) |  |
| confidenceMillionths | required | uint64 | 0..1000000 | retained | opensip.product.fact-batch.3#/properties/candidates/items/properties/confidenceMillionths |  |  |  |
| relationSchemaId | required | UTF-8-NFC-text | exact host registry schemaId for relation@schemaVersion; vector maxLength 256 | retained | opensip.product.fact-batch.3#/properties/candidates/items/properties/relationSchemaId |  | fp.candidate |  |
| canonicalRelationPayload | required | byte-string | deterministic-CBOR bytes of host registry schema; <= maxFactCandidatePayloadBytes 1048576 | retained |  | no schema-native wire ref: fact-batch.3 canonicalRelationPayloadHex/decodedRelationPayload are JSON-vector transcription and observation, not wire members | fp.candidate: decode once, re-encode byte-equal; d2.limitRule | TS2-G1 |
| anchors | required | definite-array | items AnchorRefV1 map; non-empty; sorted by deterministic-CBOR bytes; unique; count bound unstated (vector maxItems 4096) | retained | opensip.product.fact-batch.3#/properties/candidates/items/properties/anchors |  | fp.anchor | TS2-G5 TS2-G11 |

### definitions.CoverageKeyV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| relation | required | UTF-8-NFC-text | one stage.relations member | retained |  |  | d2.coverageDomain.keyConstruction | TS2-G7 |
| resolution | required | UTF-8-NFC-text | relationResolutionById[relation]: declares->syntactic, imports->resolved-target, references->resolved-binding, calls->resolved-callee, types->checked, reachability->from-resolved-calls | retained |  |  |  | TS2-G7 |
| sourceUniverseId | required | UTF-8-NFC-text | Sha256Text; native semantic-universe identity sha256:hex(H(native.semantic-universe.<language>.v2, universe.resolvedInputs)) (inherited recipe opensip.typescript-universe.v1 superseded) | value-substituted |  | CoverageResultV3.key.sourceUniverse carries its 64-hex suffix | equals OpenUniverse.universeKey | TS2-G7 |
| targetUniverseId | required | UTF-8-NFC-text | native semantic-universe identity (Sha256Text) per targetPartition (<= 2 activated universes) | value-substituted |  |  |  | TS2-G7 |
| subjectScopeCommitment | required | UTF-8-NFC-text | Sha256Text | retained |  |  |  | TS2-G4 TS2-G7 |
| producer | required | UTF-8-NFC-text | const typescript-semantic | retained |  | request coordinate; not restated in native CoverageKeyV2 (startup law coverageFrames.entries) |  |  |
| producerVersion | required | UTF-8-NFC-text | exact verified providerBuildId (TypeScriptHelloAckV2) | retained |  | request coordinate only |  |  |
| schemaVersion | required | uint64 | exactly 1 | retained |  | request coordinate only |  |  |

### definitions.CoverageResultV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| stageId | required | UTF-8-NFC-text | attribution moves to TypeScriptCoverageV2.stageId (wrapper) | replaced (moved) | opensip.product.provider-startup.1#/$defs/TypeScriptCoverageV2/properties/stageId |  |  |  |
| entryOrdinal | required | uint64 | removed; array index i of entries answers keys[i] | replaced (removed) | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3 |  | start.admit_coverage_frame: count and positional bijection |  |
| coverageState | required | UTF-8-NFC-text | -> entry.coverage enum complete\|unknown | replaced (moved) | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/ViewEntryV3/properties/coverage |  | ne.admit_coverage_result_v3: RC-6 complete => examinedExhaustive |  |
| key | required | definite-text-keyed-map | -> key CoverageKeyV2 {relation, resolution, sourceUniverse, targetUniverse (bare 64 hex), subjectScopeCommitment} | replaced (value-changed) | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageKeyV2 |  | start.admit_coverage_frame: equals keys[i] (suffix projection); ne.admit_coverage_result_v3 §4.1a steps 1-4 | TS2-G4 TS2-G7 |
| deficiency | required | UTF-8-NFC-text\|null | -> entry.deficiency DeficiencyV2 (9 values) \| null | replaced (moved) | urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/ViewEntryV3/properties/deficiency |  |  |  |

### definitions.StageResultV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| stageId | required | UTF-8-NFC-text | exact requested stageId | retained |  |  |  | TS2-G3 |
| stageOrdinal | required | uint64 | exact requested stageOrdinal | retained |  |  |  |  |
| factBatchCount | required | uint64 | exact observed FactBatch frame count (V1 or V3 payload) | retained |  |  |  |  |
| factCount | required | uint64 | exact observed candidate count | retained |  |  |  |  |
| coverageEntryCount | required | uint64 | exact observed CoverageResultV3 entry count | retained |  |  |  |  |
| factCommitment | required | UTF-8-NFC-text | Sha256Text; domain stageFacts over ordered FactCandidateV1 stream whichever payload carried it | retained |  | provider-handshake x-opensip-wire-law/commitments/typescript-semantic | d2.commitments |  |
| coverageCommitment | required | UTF-8-NFC-text | Sha256Text over ordered CoverageResultV3 values; recipe/domain unchanged | value-substituted |  |  | d2.commitments | TS2-G12 |

### payloadSchemas.HelloV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| hostBuildId | required | UTF-8-NFC-text | non-empty NFC text | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloV2/properties/hostBuildId |  | TS2-G2 |  |
| expectedProviderDescriptorSha256 | required | UTF-8-NFC-text | DigestHex = raw SHA-256 of RFC 8785 typescript-provider/identity.json | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloV2/properties/expectedProviderDescriptorSha256 |  | d2.identity |  |
| expectedRuntimeDescriptorSha256 | required | UTF-8-NFC-text | DigestHex = raw SHA-256 of RFC 8785 typescript-runtime/identity.json | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloV2/properties/expectedRuntimeDescriptorSha256 |  | d2.identity |  |
| limits | required | definite-text-keyed-map | TypeScriptProtocolLimitsV1: exactly ten uint64 consts (see limits link) | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloV2/properties/limits |  | wire.admit_hello: missing/extra/renamed/retyped/changed member refuses before HelloAck |  |

### payloadSchemas.HelloAckV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| protocolMajor | required | uint64 | exactly 2 (inherited exactly 1); equals provider descriptor protocolMajor | replaced (value-changed) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/protocolMajor |  | wire.admit_hello_ack |  |
| providerBuildId | required | UTF-8-NFC-text | non-empty NFC; verified provider descriptor text | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/providerBuildId |  | wire.admit_hello_ack: equals provider descriptor; TS2-G2 |  |
| providerDescriptorSha256 | required | UTF-8-NFC-text | DigestHex | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/providerDescriptorSha256 |  | wire.admit_hello_ack: equals Hello expectedProviderDescriptorSha256; TS2-G2 |  |
| runtimeDescriptorSha256 | required | UTF-8-NFC-text | DigestHex | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/runtimeDescriptorSha256 |  | wire.admit_hello_ack: equals Hello expectedRuntimeDescriptorSha256; TS2-G2 |  |
| nodeVersion | required | UTF-8-NFC-text | non-empty NFC; verified runtime descriptor text | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/nodeVersion |  | wire.admit_hello_ack: equals runtime descriptor; TS2-G2 |  |
| v8Version | required | UTF-8-NFC-text | non-empty NFC; verified runtime descriptor text | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/v8Version |  | wire.admit_hello_ack: equals runtime descriptor; TS2-G2 |  |
| modulesAbi | required | UTF-8-NFC-text | non-empty NFC; verified runtime descriptor text | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/modulesAbi |  | wire.admit_hello_ack: equals runtime descriptor; TS2-G2 |  |
| typescriptVersion | required | UTF-8-NFC-text | non-empty NFC; verified provider descriptor text | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/typescriptVersion |  | wire.admit_hello_ack: equals provider descriptor; TS2-G2 |  |
| typescriptCompilerSha256 | required | UTF-8-NFC-text | DigestHex | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/typescriptCompilerSha256 |  | wire.admit_hello_ack: equals provider descriptor; TS2-G2 |  |
| typescriptStdlibMerkleRoot | required | UTF-8-NFC-text | DigestHex | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/typescriptStdlibMerkleRoot |  | wire.admit_hello_ack: equals provider descriptor; TS2-G2 |  |
| defaultWorkBudgetProfileId | required | UTF-8-NFC-text | const typescript-provider-default-work-budget-v1 | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/defaultWorkBudgetProfileId |  | wire.admit_hello_ack: equals provider descriptor; TS2-G2 |  |
| defaultWorkBudgetProfileSha256 | required | UTF-8-NFC-text | const bf7305a12d26a1938b615c861f995d66eac494915e6140c4942a2ea6f0846da6 | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/defaultWorkBudgetProfileSha256 |  | wire.admit_hello_ack: equals provider descriptor; TS2-G2 |  |
| platformId | required | UTF-8-NFC-text | non-empty NFC; selected release platformId | replaced (unchanged) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/platformId |  | wire.admit_hello_ack: equals runtime descriptor; TS2-G2 |  |
| capabilities | required | definite-array | TypeScriptCapabilitiesV2: 4..11 unique TypeScriptCapabilityToken, strictly ascending UTF-8, four identity tokens present (inherited fixed 3-token array) | replaced (value-changed) | opensip.product.provider-handshake.1#/$defs/TypeScriptHelloAckV2/properties/capabilities |  | wire.admit_hello_ack: exact echo of Hello expectedCapabilities (order is not JSON-Schema checkable) |  |

### payloadSchemas.OpenUniverseV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| executionId | required | UTF-8-NFC-text | ExecutionIdText | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptOpenUniverseV2/properties/executionId |  |  | TS2-G11 |
| snapshotId | required | UTF-8-NFC-text | SnapshotId2 | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptOpenUniverseV2/properties/snapshotId |  |  |  |
| planId | required | UTF-8-NFC-text | PlanId2 | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptOpenUniverseV2/properties/planId |  |  |  |
| planIntentCommitment | required | UTF-8-NFC-text | Sha256Text | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptOpenUniverseV2/properties/planIntentCommitment |  |  |  |
| providerId | required | UTF-8-NFC-text | const typescript-semantic | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptOpenUniverseV2/properties/providerId |  |  |  |
| universe | required | definite-text-keyed-map | TypeScriptSemanticUniverseV2 | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptOpenUniverseV2/properties/universe |  | start.admit_open_universe: handshakeJoin (11 members); admitted only when identityNegotiated |  |
| universeKey | required | UTF-8-NFC-text | Sha256Text; native semantic-universe identity (typescript v2) | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptOpenUniverseV2/properties/universeKey |  | host recomputes |  |

### payloadSchemas.UniverseAcceptedV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| executionId | required | UTF-8-NFC-text | exact OpenUniverse echo | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptUniverseAcceptedV2/properties/executionId |  | start.admit_universe_accepted |  |
| snapshotId | required | UTF-8-NFC-text | SnapshotId2 echo | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptUniverseAcceptedV2/properties/snapshotId |  | start.admit_universe_accepted |  |
| planId | required | UTF-8-NFC-text | PlanId2 echo | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptUniverseAcceptedV2/properties/planId |  | start.admit_universe_accepted |  |
| universeKey | required | UTF-8-NFC-text | Sha256Text; native semantic-universe identity (typescript v2); worker recomputation equal to OpenUniverse | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptUniverseAcceptedV2/properties/universeKey |  | start.admit_universe_accepted |  |

### payloadSchemas.SnapshotManifestV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| snapshotId | required | UTF-8-NFC-text | ^snapshot2:[0-9a-f]{64}$ via exact echo of OpenUniverse | value-substituted | opensip.product.provider-startup.1#/$defs/SnapshotId2 | startup identityMembers lists SnapshotManifest snapshotId |  |  |
| manifestSha256 | required | UTF-8-NFC-text | DigestHex over deterministic-CBOR entries (form disputed) | retained |  |  | worker recomputes | TS2-G10 |
| entries | required | definite-array | items SnapshotEntryV1 map; sorted unique by path UTF-8; <= maxSnapshotEntries 200000 | retained |  |  | d2.limitRule; d2.snapshotTransport |  |

### payloadSchemas.SnapshotFileChunkV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| snapshotId | required | UTF-8-NFC-text | ^snapshot2:[0-9a-f]{64}$ via exact echo of manifest | value-substituted | opensip.product.provider-startup.1#/$defs/SnapshotId2 | 'exact manifest SnapshotId' -> manifest echoes OpenUniverse; transitive (startup identityMembers does not enumerate chunk explicitly) |  |  |
| path | required | UTF-8-NFC-text | one kind=file manifest path | retained |  | exact echo of SnapshotEntryV1.path |  | TS2-G11 |
| chunkIndex | required | uint64 | contiguous from 0 per path | retained |  |  | d2.snapshotTransport |  |
| byteOffset | required | uint64 | exact cumulative prior chunk bytes | retained |  |  | checked uint64 add |  |
| bytes | required | byte-string | non-empty; length <= maxSnapshotChunkBytes 1048576 | retained |  |  | d2.limitRule; digest vs manifest contentSha256 | TS2-G1 |

### payloadSchemas.SnapshotSealV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| snapshotId | required | UTF-8-NFC-text | ^snapshot2:[0-9a-f]{64}$ via exact echo of manifest | value-substituted | opensip.product.provider-startup.1#/$defs/SnapshotId2 | startup identityMembers lists SnapshotSeal snapshotId |  |  |
| manifestSha256 | required | UTF-8-NFC-text | exact manifestSha256 echo | retained |  |  |  | TS2-G10 |
| entryCount | required | uint64 | exact entries length (<= 200000) | retained |  |  |  |  |
| totalFileBytes | required | uint64 | exact sum of file byteLength | retained |  |  | checked uint64 add |  |
| totalChunkCount | required | uint64 | exact emitted chunk count | retained |  |  |  |  |

### payloadSchemas.SnapshotAcceptedV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| snapshotId | required | UTF-8-NFC-text | ^snapshot2:[0-9a-f]{64}$ via exact echo of SnapshotSeal | value-substituted | opensip.product.provider-startup.1#/$defs/SnapshotId2 | startup identityMembers lists SnapshotAccepted snapshotId |  |  |
| manifestSha256 | required | UTF-8-NFC-text | worker-recomputed exact value | retained |  |  |  | TS2-G10 |
| entryCount | required | uint64 | worker-observed exact | retained |  |  |  |  |
| totalFileBytes | required | uint64 | worker-observed exact | retained |  |  |  |  |
| totalChunkCount | required | uint64 | worker-observed exact | retained |  |  |  |  |

### payloadSchemas.AnalyzeV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | exactly 0 (one Analyze per worker) | retained |  |  |  |  |
| executionId | required | UTF-8-NFC-text | exact OpenUniverse echo | retained |  |  |  |  |
| snapshotId | required | UTF-8-NFC-text | ^snapshot2:[0-9a-f]{64}$ via exact echo of OpenUniverse | value-substituted | opensip.product.provider-startup.1#/$defs/SnapshotId2 |  |  |  |
| planId | required | UTF-8-NFC-text | ^plan2:[0-9a-f]{64}$ via exact echo of OpenUniverse | value-substituted | opensip.product.provider-startup.1#/$defs/PlanId2 |  |  |  |
| universeKey | required | UTF-8-NFC-text | Sha256Text; native semantic-universe identity (typescript v2) echo | value-substituted | opensip.product.provider-startup.1#/$defs/Sha256Text |  |  |  |
| stageRequests | required | definite-array | items StageRequestV1 map; non-empty; <= maxAnalyzeStages 1024; all and only selected stages in verified logical order (may be a Plan subset) | retained |  |  | d2.multiStageAnalyze.selection/batchability/ordering; dispatch |  |

### payloadSchemas.FactBatchV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | exactly 0 | retained | opensip.product.provider-handshake.1#/$defs/TypeScriptFactBatchV1Vector/properties/analysisOrdinal |  | dispatch: == expectedAnalysisOrdinal |  |
| stageId | required | UTF-8-NFC-text | C-2 stageId TEXT echo of current StageRequestV1.stageId; StageIdText 1..255 | retained | opensip.product.provider-handshake.1#/$defs/TypeScriptFactBatchV1Vector/properties/stageId |  | dispatch: == expectedStageId; not stageOrdinal; not execution-plan ordinal |  |
| batchIndex | required | uint64 | contiguous from 0 per stage | retained | opensip.product.provider-handshake.1#/$defs/TypeScriptFactBatchV1Vector/properties/batchIndex |  | dispatch: == expectedBatchIndex |  |
| facts | required | definite-array | items FactCandidateV1 map; non-empty; ordered; <= maxFactBatchFacts 4096 | retained | opensip.product.provider-handshake.1#/$defs/TypeScriptFactBatchV1Vector/properties/facts | vector items ref fact-batch.3 JSON-vector candidate (hex transcription; see TS2-G1) | wire.admit_fact_batch |  |
| batchCommitment | required | UTF-8-NFC-text | Sha256Text; domain opensip.ts-provider.fact-batch.v1 over deterministic-CBOR(facts) | retained | opensip.product.provider-handshake.1#/$defs/TypeScriptFactBatchV1Vector/properties/batchCommitment |  | wire.admit_fact_batch: recompute; d2.commitments.domains.factBatch (FactBatchV1 only) |  |

### payloadSchemas.CoverageV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | exactly 0 | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptCoverageV2/properties/analysisOrdinal |  |  |  |
| stageId | required | UTF-8-NFC-text | StageIdText; current requested stage; attributes every entry | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptCoverageV2/properties/stageId |  |  |  |
| entries | required | definite-array | items CoverageResultV3; 1..4096; entries[i] answers requestedCoverageDomain.keys[i]; count == key count | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptCoverageV2/properties/entries |  | start.admit_coverage_frame; ne.admit_coverage_result_v3 |  |
| coverageCommitment | required | UTF-8-NFC-text | Sha256Text over ordered CoverageResultV3 entries; recipe unchanged | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptCoverageV2/properties/coverageCommitment |  |  | TS2-G12 |

### payloadSchemas.UnavailableV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | exactly 0 | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptUnavailableV2/properties/analysisOrdinal |  |  |  |
| affectedStageIds | required | definite-array | items StageIdText; all requested stageIds in request order; schema minItems 1, no maxItems (derived <= 1024) | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptUnavailableV2/properties/affectedStageIds |  |  | TS2-G8 |
| reason | required | UTF-8-NFC-text | enum capability-missing\|identity-version-mismatch\|node-modules-outside-read-set\|semantic-universe-incomplete\|snapshot-resolution-input-missing\|unsupported-compiler-mode (never native-context-mismatch) | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptUnavailableV2/properties/reason |  |  |  |
| coverage | required | definite-array | items CoverageResultV3 in stage-major/key order, unknown/provider-unavailable; schema minItems 0 no max (derived >= 1, <= 131072) | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptUnavailableV2/properties/coverage |  | cumulative key-range attribution | TS2-G8 |
| coverageCommitment | required | UTF-8-NFC-text | Sha256Text over CoverageResultV3 coverage | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptUnavailableV2/properties/coverageCommitment |  |  | TS2-G12 |

### payloadSchemas.BudgetExhaustedV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | exactly 0 | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptBudgetExhaustedV2/properties/analysisOrdinal |  |  |  |
| triggerStageId | required | UTF-8-NFC-text | StageIdText; one requested stageId | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptBudgetExhaustedV2/properties/triggerStageId |  |  |  |
| dimension | required | UTF-8-NFC-text | enum sourceFilesVisited\|astNodesVisited\|moduleResolutionQueries\|typeQueries\|factsEmitted\|factBytesEmitted | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptBudgetExhaustedV2/properties/dimension |  |  |  |
| limit | required | uint64 | exact requested budget | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptBudgetExhaustedV2/properties/limit |  |  |  |
| observed | required | uint64 | exactly limit+1 | replaced (unchanged) | opensip.product.provider-startup.1#/$defs/TypeScriptBudgetExhaustedV2/properties/observed |  | observed == limit+1 (checked) |  |
| coverage | required | definite-array | items CoverageResultV3, unknown/budget-exhausted, stage-major/key order; schema no maxItems | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptBudgetExhaustedV2/properties/coverage |  |  | TS2-G8 |
| coverageCommitment | required | UTF-8-NFC-text | Sha256Text over CoverageResultV3 coverage | replaced (value-changed) | opensip.product.provider-startup.1#/$defs/TypeScriptBudgetExhaustedV2/properties/coverageCommitment |  |  | TS2-G12 |

### payloadSchemas.CompleteV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| analysisOrdinal | required | uint64 | exactly 0 | retained |  |  |  |  |
| stageResults | required | definite-array | items StageResultV1 map; exactly one per requested stage in request order (<= 1024) | retained |  |  | d2.multiStageAnalyze.completeness |  |
| factStreamCommitment | required | UTF-8-NFC-text | Sha256Text; domain factStream over all ordered FactCandidateV1 (V1 or V3 carried) | retained |  | provider-handshake x-opensip-wire-law/commitments/typescript-semantic | d2.commitments |  |
| coverageStreamCommitment | required | UTF-8-NFC-text | Sha256Text over all ordered CoverageResultV3 values | value-substituted |  |  | d2.commitments | TS2-G12 |

### payloadSchemas.CancelV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| executionId | required | UTF-8-NFC-text\|null | OpenUniverse ExecutionId if opened, else null | retained |  | startup identityMembers: Cancel executionId exact echo (ExecutionId itself retained) |  |  |
| analysisOrdinal | required | uint64\|null | 0 after Analyze, else null | retained |  |  |  |  |
| reason | required | UTF-8-NFC-text | enum user-interrupt\|host-shutdown | retained |  |  | d2.ordering.cancelTransition |  |

### payloadSchemas.CancelledV1

| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |
|---|---|---|---|---|---|---|---|---|
| executionId | required | UTF-8-NFC-text\|null | exact Cancel value | retained |  |  |  |  |
| analysisOrdinal | required | uint64\|null | exact Cancel value | retained |  |  |  |  |
| observedPhase | required | UTF-8-NFC-text | enum handshake\|universe\|snapshot\|analysis (unchanged); snapshot for Cancel in WAIT_NATIVE_CONTEXT_VERIFIED/READY_ANALYZE | retained |  |  | start.typescript_protocol2_run cancellationObservedPhase |  |

## 8. New members (schema-native owners)

| record.member | wire | bounds / vocabulary | source selector | handwritten | gaps |
|---|---|---|---|---|---|
| TypeScriptHelloV2.expectedCapabilities | definite-array | TypeScriptCapabilitiesV2: 4..11 unique tokens, strictly ascending UTF-8, contains 4 identity tokens; optional target-attribution-v2 | `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json` #/$defs/TypeScriptHelloV2/properties/expectedCapabilities | wire.admit_hello: equals signed capability row |  |
| TypeScriptHelloV2.identityVersions | definite-text-keyed-map | IdentityVersionsV1 {snapshot:2, plan:2, fact:2, coverage:3} | `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json` #/$defs/TypeScriptHelloV2/properties/identityVersions |  |  |
| TypeScriptHelloAckV2.identityVersions | definite-text-keyed-map | IdentityVersionsV1; exact echo of Hello | `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json` #/$defs/TypeScriptHelloAckV2/properties/identityVersions | wire.admit_hello_ack: exact echo |  |
| NativeContextVerifiedV1.nativeContextId | UTF-8-NFC-text | Sha256Text; == OpenUniverse.universe.resolvedInputs.nativeContextId | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` #/$defs/NativeContextVerifiedV1/properties/nativeContextId | start.admit_native_context_verified |  |
| NativeContextVerifiedV1.recomputedNativeContextId | UTF-8-NFC-text | Sha256Text; worker recomputation, equal | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` #/$defs/NativeContextVerifiedV1/properties/recomputedNativeContextId | start.admit_native_context_verified |  |
| NativeContextVerifiedV1.equal | bool | const true | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` #/$defs/NativeContextVerifiedV1/properties/equal |  |  |
| PreAnalyzeUnavailableV1.executionId | UTF-8-NFC-text | ExecutionIdText == OpenUniverse | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` #/$defs/PreAnalyzeUnavailableV1/properties/executionId | start.admit_unavailable |  |
| PreAnalyzeUnavailableV1.snapshotId | UTF-8-NFC-text | SnapshotId2 == OpenUniverse | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` #/$defs/PreAnalyzeUnavailableV1/properties/snapshotId | start.admit_unavailable |  |
| PreAnalyzeUnavailableV1.planId | UTF-8-NFC-text | PlanId2 == OpenUniverse | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` #/$defs/PreAnalyzeUnavailableV1/properties/planId | start.admit_unavailable |  |
| PreAnalyzeUnavailableV1.reason | UTF-8-NFC-text | const native-context-mismatch | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` #/$defs/PreAnalyzeUnavailableV1/properties/reason |  |  |
| PreAnalyzeUnavailableV1.nativeContextId | UTF-8-NFC-text | Sha256Text == universe.resolvedInputs.nativeContextId | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` #/$defs/PreAnalyzeUnavailableV1/properties/nativeContextId | start.admit_unavailable |  |
| PreAnalyzeUnavailableV1.recomputedNativeContextId | UTF-8-NFC-text | Sha256Text; differs from nativeContextId | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` #/$defs/PreAnalyzeUnavailableV1/properties/recomputedNativeContextId | start.admit_unavailable; ne.pre_analyze_unavailable_conversion: host mints coverage after DONE |  |
| FactBatchV3.schemaVersion | uint64 | const 3 (payload discriminator; not FactCandidateV1.schemaVersion) | `docs/coop/design-corrections/native/fact-batch.schema.v3.json` #/properties/schemaVersion |  |  |
| FactBatchV3.analysisOrdinal | uint64 | uint64 echo of AnalyzeV1.analysisOrdinal (TS: 0) | `docs/coop/design-corrections/native/fact-batch.schema.v3.json` #/properties/analysisOrdinal | dispatch: == expectedAnalysisOrdinal |  |
| FactBatchV3.stageId | UTF-8-NFC-text | C-2 stageId TEXT 1..255 echo of StageRequestV1.stageId | `docs/coop/design-corrections/native/fact-batch.schema.v3.json` #/properties/stageId | dispatch: == expectedStageId |  |
| FactBatchV3.batchIndex | uint64 | contiguous from 0 per stage | `docs/coop/design-corrections/native/fact-batch.schema.v3.json` #/properties/batchIndex | dispatch: == expectedBatchIndex |  |
| FactBatchV3.candidates | definite-array | items FactCandidateV1 (wire bstr payload); 1..4096 (maxFactBatchFacts); member name candidates, not facts | `docs/coop/design-corrections/native/fact-batch.schema.v3.json` #/properties/candidates | wire.admit_fact_batch | TS2-G1 |
| FactBatchV3.occupancyCompanions | definite-array | items OccupancyCompanionV1 (10 required members, allOf branches); 0..len(candidates); strictly increasing candidateOrdinal naming this batch | `docs/coop/design-corrections/native/fact-batch.schema.v3.json` #/properties/occupancyCompanions | candidateOrdinal association (PROVIDER_RETURN_UNKNOWN_CANDIDATE); targetUniverseId byte-equal to candidate |  |

## 9. Successor member-list comparisons (exhaustive)

| original | successor | kept | removed/moved | added | same order |
|---|---|---|---|---|---|
| payloadSchemas.HelloV1 | `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json#/$defs/TypeScriptHelloV2` | 4/4 | [] | ["expectedCapabilities", "identityVersions"] | True |
| payloadSchemas.HelloAckV1 | `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json#/$defs/TypeScriptHelloAckV2` | 14/14 | [] | ["identityVersions"] | True |
| payloadSchemas.OpenUniverseV1 | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json#/$defs/TypeScriptOpenUniverseV2` | 7/7 | [] | [] | True |
| payloadSchemas.UniverseAcceptedV1 | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json#/$defs/TypeScriptUniverseAcceptedV2` | 4/4 | [] | [] | True |
| payloadSchemas.CoverageV1 | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json#/$defs/TypeScriptCoverageV2` | 4/4 | [] | [] | True |
| payloadSchemas.UnavailableV1 | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json#/$defs/TypeScriptUnavailableV2` | 5/5 | [] | [] | True |
| payloadSchemas.BudgetExhaustedV1 | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json#/$defs/TypeScriptBudgetExhaustedV2` | 7/7 | [] | [] | True |
| payloadSchemas.FactBatchV1 | `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json#/$defs/TypeScriptFactBatchV1Vector` | 5/5 | [] | [] | True |
| definitions.CoverageResultV1 | `docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/CoverageResultV3` | 1/5 | ["stageId", "entryOrdinal", "coverageState", "deficiency"] | ["entry", "schemaVersion"] | True |
| definitions.FactCandidateV1 | `docs/coop/design-corrections/native/fact-batch.schema.v3.json#/properties/candidates/items` | 13/14 | ["canonicalRelationPayload"] | ["canonicalRelationPayloadHex", "decodedRelationPayload"] | True |
| (FactBatchV1 vs negotiated) payloadSchemas.FactBatchV1 | `docs/coop/design-corrections/native/fact-batch.schema.v3.json#` | 3/5 | ["facts", "batchCommitment"] | ["schemaVersion", "candidates", "occupancyCompanions"] | True |
| (PreAnalyze alternative) payloadSchemas.UnavailableV1 | `docs/coop/design-corrections/native/provider-startup.schemas.v1.json#/$defs/PreAnalyzeUnavailableV1` | 1/5 | ["analysisOrdinal", "affectedStageIds", "coverage", "coverageCommitment"] | ["executionId", "snapshotId", "planId", "nativeContextId", "recomputedNativeContextId"] | True |

Required list vs field map, every closed record: frameEnvelope 4/4; definitions.SnapshotEntryV1 5/5; definitions.ProviderWorkBudgetV1 6/6; definitions.StageRequestV1 8/8; definitions.SnapshotFileSubjectV1 3/3; definitions.SubjectScopeV1 4/4; definitions.RequestedCoverageDomainV1 3/3; definitions.AnchorRefV1 7/no-field-map; definitions.FactCandidateV1 14/14; definitions.CoverageKeyV1 8/8; definitions.CoverageResultV1 5/5; definitions.StageResultV1 7/7; payloadSchemas.HelloV1 4/4; payloadSchemas.HelloAckV1 14/14; payloadSchemas.OpenUniverseV1 7/7; payloadSchemas.UniverseAcceptedV1 4/4; payloadSchemas.SnapshotManifestV1 3/3; payloadSchemas.SnapshotFileChunkV1 5/5; payloadSchemas.SnapshotSealV1 5/5; payloadSchemas.SnapshotAcceptedV1 5/5; payloadSchemas.AnalyzeV1 6/6; payloadSchemas.FactBatchV1 5/5; payloadSchemas.CoverageV1 4/4; payloadSchemas.UnavailableV1 5/5; payloadSchemas.BudgetExhaustedV1 7/7; payloadSchemas.CompleteV1 4/4; payloadSchemas.CancelV1 3/3; payloadSchemas.CancelledV1 3/3.

## 10. Gap register

### TS2-G1 — CBOR byte-string has no selected JSON/generator representation

Both are CBOR byte strings on the wire. fact-batch.schema.v3 canonicalRelationPayloadHex is a JSON-vector transcription (not a wire member, not a selected mirror); no schema-native record exists for SnapshotFileChunk bytes. Any JSON Schema mirror representation, generator tsType (e.g. Uint8Array) or Rust Vec<u8>/bytes mapping requires explicit root selection. Not chosen here.

- action: root selection
- rows citing: FactBatchV3.candidates, definitions.FactCandidateV1.fields.canonicalRelationPayload, payloadSchemas.SnapshotFileChunkV1.fields.bytes

### TS2-G2 — NFC, UTF-8 byte bounds and canonical CBOR are not plain-JSON-Schema checkable

Plain JSON Schema cannot validate NFC, deterministic-CBOR shortest encoding, map key order, duplicate keys or UTF-8 byte lengths (maxLength counts code points). Schema-native NfcText defs state 'NFC is checked by admission'. These remain handwritten (d2.canonicalCbor).

- action: handwritten admission; no wire change
- rows citing: (record-level)

### TS2-G3 — stageId text bound for StageRequestV1/StageResultV1/dependsOn not stated by a TS2 owner

delivery.v2 says 'exact C-2 stageId text' with no bound; c2-plan-stage-schema.v3 (bounded read) states none. StageIdText (1..255) is published in provider-handshake.1 and provider-startup.1 and used by FactBatchV1 vector, TypeScriptCoverageV2, TypeScriptUnavailableV2 and TypeScriptBudgetExhaustedV2, which echo these values, but no owner applies it to StageRequestV1/StageResultV1 and its 255 source is uncited. Echo equality makes it the effective bound on responses only.

- action: root selection whether StageIdText applies to request/result stageId members
- rows citing: definitions.StageRequestV1.fields.dependsOn, definitions.StageRequestV1.fields.stageId, definitions.StageResultV1.fields.stageId

### TS2-G4 — subjectScopeCommitment value domain: delivery.v2 SubjectScopeV1 recipe vs §4.1a per-key scope2

delivery.v2: one per-stage commitment under opensip.coverage.subject-scope.v1 over sorted SnapshotFileSubjectV1, and RequestedCoverageDomainV1.workerRule requires every key.subjectScopeCommitment to equal it. native-evidence §4.1a: subjectScopeCommitment is 'sha256:'+hex of scope2 = H('subject-scope', {snapshotId, sourceUniverse, targetUniverse, relation, resolution, enumeratorClosure, subjects}), i.e. per key, checked by admit_coverage_result_v3 against CoverageResultV3.key; §9.7 requires entries[i].key.subjectScopeCommitment == keys[i].subjectScopeCommitment. §0 names no delivery.v2 SubjectScopeV1/coverageSubjectScope selector as superseded and retains wireSchema.commitments. With cross-universe keys the two rules cannot both hold. Shape (Sha256Text) is identical either way; the value recipe is unresolved here.

- action: root/owner decision; do not generate a recipe
- rows citing: definitions.CoverageKeyV1.fields.subjectScopeCommitment, definitions.CoverageResultV1.fields.key, definitions.RequestedCoverageDomainV1.fields.subjectScope, definitions.SubjectScopeV1.fields.subjectScopeCommitment

### TS2-G5 — AnchorRefV1 member wire types and snapshot2/fact2 value domains unstated

delivery.v2 AnchorRefV1 has required+variants but no fields map; fact-plane anchorSchema/sourceSpanSchema give nullability and path rule but no CBOR types for snapshotId, contentSha256, startByte, endByte, factId. fact-batch.3 vector anchors items are {type: object}. startup identityMembers does not list anchor snapshotId; no bounded source states whether fact-ref factId is FACT-ID-V1 or fact2 text under fact-identity-fact2.

- action: owner statement required; recorded UNSTATED, not guessed
- rows citing: definitions.AnchorRefV1.required.contentSha256, definitions.AnchorRefV1.required.endByte, definitions.AnchorRefV1.required.factId, definitions.AnchorRefV1.required.path, definitions.AnchorRefV1.required.snapshotId, definitions.AnchorRefV1.required.startByte, definitions.FactCandidateV1.fields.anchors

### TS2-G6 — Frame rows whose payload is selected by negotiation or phase, not by a wire discriminator

FactBatch payload is FactBatchV1 or FactBatchV3 by HelloAck token target-attribution-v2; Unavailable payload is PreAnalyzeUnavailableV1 in WAIT_NATIVE_CONTEXT_VERIFIED or TypeScriptUnavailableV2 after Analyze. The envelope carries only frameType; selection is host state. A generated projection must expose both closed alternatives without inventing a tag or an untagged 'try each' decode.

- action: root selection of projection form (e.g. per-context decode entry points); no wire change
- rows citing: frameEnvelope.fields.payload, frameSchemas.FactBatch, frameSchemas.Unavailable

### TS2-G7 — Same-named records across owners are distinct (trace, not identity)

See translation.md 'G7 trace'. TS CoverageKeyV1 (8 members, Sha256Text universes) stays the request key; native CoverageKeyV2 (5 members, bare-hex universes) is the CoverageResultV3 entry key; rust-provider-protocol.v2 CoverageKeyV2 is an 8-member external ref to c2 v3 coverageKey.key and is not a TS2 carrier. TS FactCandidateV1 restates fact-plane candidateSchema (14 members, identical list); Rust FactCandidateV1 is an external ref to the same candidateSchema with 'wireAdjustment: byte string'; value-domain supersession for universe ids is stated for TS by §0:125 and for Rust separately by §0:128.

- action: namespace by owner/language; never merge by bare name
- rows citing: definitions.CoverageKeyV1.fields.relation, definitions.CoverageKeyV1.fields.resolution, definitions.CoverageKeyV1.fields.sourceUniverseId, definitions.CoverageKeyV1.fields.subjectScopeCommitment, definitions.CoverageKeyV1.fields.targetUniverseId, definitions.CoverageResultV1.fields.key

### TS2-G8 — Successor array bounds weaker than inherited derivable bounds

TypeScriptUnavailableV2.affectedStageIds has minItems 1 and no maxItems; coverage arrays have minItems 0 and no maxItems. Inherited text derives affectedStageIds <= maxAnalyzeStages (1024), coverage = sum of requested keys (>= 1 since every domain is non-empty; <= 1024*128 = 131072) and the whole payload <= maxFramePayloadBytes. The derived bounds are handwritten checks; the schema-native shape is not edited.

- action: handwritten admission; record only
- rows citing: payloadSchemas.BudgetExhaustedV1.fields.coverage, payloadSchemas.UnavailableV1.fields.affectedStageIds, payloadSchemas.UnavailableV1.fields.coverage

### TS2-G9 — providerProtocol.major and wireSchemaCommitment for major 2

§0:119 sets providerProtocol.major to 2. wireSchemaCommitment (domain opensip.delivery.ts-wire-schema.v1, sha 96ffbe7b...) commits the unchanged historical wireSchema object; no bounded source says whether a major-2 projection has or needs a commitment. Neither is a wire field.

- action: record; any projection-document commitment requires root selection
- rows citing: (record-level)

### TS2-G10 — manifestSha256 form: DigestHex vs commitments.domains.snapshotManifest

Field text is 'DigestHex over deterministic-CBOR entries' (bare 64 hex, no domain) while commitments.domains.snapshotManifest names opensip.ts-provider.snapshot-manifest.v1 and domainRule renders 'sha256:<hex>'. The inherited artifact does not reconcile them; text wire type is certain, pattern and preimage are not.

- action: owner decision; do not choose a pattern
- rows citing: payloadSchemas.SnapshotAcceptedV1.fields.manifestSha256, payloadSchemas.SnapshotManifestV1.fields.manifestSha256, payloadSchemas.SnapshotSealV1.fields.manifestSha256

### TS2-G11 — Unbounded text/array members with no schema-native successor bound

No length/count bound is stated beyond maxFramePayloadBytes (and maxAnalyzeStages for dependsOn by uniqueness over stageIds). fact-batch.3 vector bounds (anchors <= 4096, universe ids <= 4096) are JSON-vector bounds without cited wire derivation.

- action: record; frame-size limit is the only derivable wire bound
- rows citing: definitions.ExecutionId, definitions.FactCandidateV1.fields.anchors, definitions.SnapshotEntryV1.fields.linkTarget, definitions.SnapshotEntryV1.fields.path, definitions.StageRequestV1.fields.dependsOn, payloadSchemas.OpenUniverseV1.fields.executionId, payloadSchemas.SnapshotFileChunkV1.fields.path

### TS2-G12 — Commitment domain per coverage/manifest field is name-derived, not stated

provider-handshake law states factCommitment->stageFacts and factStreamCommitment->factStream explicitly. For coverage, delivery.v2 lists domains stageCoverage and coverageStream but the field texts say only 'Sha256Text over deterministic-CBOR entries/coverage'; Coverage frame, Unavailable and BudgetExhausted coverageCommitment have no named domain. §9.7 says recipes and domains are unchanged over CoverageResultV3 values.

- action: owner confirmation of field->domain map before implementing the recipe (link only here)
- rows citing: definitions.StageResultV1.fields.coverageCommitment, payloadSchemas.BudgetExhaustedV1.fields.coverageCommitment, payloadSchemas.CompleteV1.fields.coverageStreamCommitment, payloadSchemas.CoverageV1.fields.coverageCommitment, payloadSchemas.UnavailableV1.fields.coverageCommitment

## 11. Inherited links (not new wire fields)

| link | source | disposition | authority | ref |
|---|---|---|---|---|
| limits | `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.limits` | retained (ten numeric members); limitRule is policy text | native-evidence.md:119; §9.4 | opensip.product.provider-handshake.1#/$defs/TypeScriptProtocolLimitsV1 |
| commitments | `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.commitments` | retained (domainRule, eight domains, empty rule); factBatch applies to FactBatchV1.batchCommitment only; coverage domains now commit CoverageResultV3 values | native-evidence.md:119, 120, 126; §9.6; §9.7 |  |
| canonicalCbor | `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.canonicalCbor` | retained (handwritten codec law) | not named by native-evidence.md §0; inherited delivery.v2 member carried unchanged into major 2 (§9.4 lists every major-2 change) |  |
| multiStageAnalyze | `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.multiStageAnalyze` | retained; selection feeds pre-Analyze host conversion (§9.7) | not named by native-evidence.md §0; inherited delivery.v2 member carried unchanged into major 2 (§9.4 lists every major-2 change) |  |
| stageRequestProjection | `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.stageRequestProjection` | retained | not named by native-evidence.md §0; inherited delivery.v2 member carried unchanged into major 2 (§9.4 lists every major-2 change) |  |
| coverageDomain | `$.typescriptSemanticSubstrate.providerProtocol.wireSchema.coverageDomain` | retained; keyConstruction universe ids take native universe identity (§0:125); producerVersion source is TypeScriptHelloAckV2.providerBuildId | provider-startup.schemas.v1.json#/x-opensip-startup-law/universeIdentity; native-evidence.md:125, 3161-3164; §11 |  |
| frameIntegrity | `$.typescriptSemanticSubstrate.providerProtocol.frameIntegrity` | retained; uint64 BE length + 32 raw SHA-256 bytes + CBOR payload are framing, not CBOR fields | not named by native-evidence.md §0; inherited delivery.v2 member carried unchanged into major 2 (§9.4 lists every major-2 change) |  |
| major | `$.typescriptSemanticSubstrate.providerProtocol.major` | value-substituted 1 -> 2 (not a CBOR field) | native-evidence.md:119 (§0 row: HelloV1/HelloAckV1/protocolMajor superseded); §9.4 |  |
| wireSchemaCommitment | `$.typescriptSemanticSubstrate.providerProtocol.wireSchemaCommitment` | historical; see TS2-G9 | none |  |
| typescriptProtocol2Order | `docs/coop/design-corrections/native/typescript-protocol2-order.v1.json` | published abstract order table (23 rules); not a carrier | native-evidence.md:2998-2999 |  |

Limit values (== TypeScriptProtocolLimitsV1 consts, asserted): {"maxFramePayloadBytes": 67108864, "maxSnapshotChunkBytes": 1048576, "maxSnapshotEntries": 200000, "maxAnalyzeStages": 1024, "maxRelationsPerStage": 64, "maxRequestedCoverageKeysPerStage": 128, "maxFactBatchFacts": 4096, "maxFactCandidatePayloadBytes": 1048576, "maxCoverageEntriesPerFrame": 4096, "maxStderrBytes": 262144}

Commitment domains (retained): {"snapshotManifest": "opensip.ts-provider.snapshot-manifest.v1", "coverageSubjectScope": "opensip.coverage.subject-scope.v1", "requestedCoverageDomain": "opensip.ts-provider.requested-coverage-domain.v1", "factBatch": "opensip.ts-provider.fact-batch.v1", "stageFacts": "opensip.ts-provider.stage-facts.v1", "stageCoverage": "opensip.ts-provider.stage-coverage.v1", "factStream": "opensip.ts-provider.fact-stream.v1", "coverageStream": "opensip.ts-provider.coverage-stream.v1"}

## 12. Source pins

| path | sha256 |
|---|---|
| `docs/coop/artifacts/delivery.v2.json` | `47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3` |
| `docs/v2/contracts/product-v1/native-evidence.md` | `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0` |
| `docs/implementation/m1/reviews/generation-owner-audit-01/audit.json` | `86c84796a9ea294d6d571cc6f3b67caa4c3eec605f8db8adadd8166c02e42257` |
| `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json` | `9090e2ad51b767a176f51da09f201803d1cc82c047ade68102adcae1ee3a5f84` |
| `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` | `1e35a77bae8d9c20171a934e9c16e4de4d7ce98bb024016d7e17cf9b0b38729c` |
| `docs/coop/design-corrections/native/fact-batch.schema.v3.json` | `b0ebc133df8763f6cd5f3716542321eba21c69714fca368fbe31ba57677a24e0` |
| `docs/coop/design-corrections/native/occupancy-companion.schema.v1.json` | `d2bbbcc49adbb130d0bb010fee0b4cf25af7727f730fc329725fa62cd46ae14f` |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043` |
| `docs/coop/design-corrections/native/typescript-protocol2-order.v1.json` | `007ef7affce224c7bac6af3bb7897e86691085e2dd788f4a613e45c1fa5b8bbb` |
| `docs/coop/design-corrections/native/dispatch-binding.schema.v1.json` | `868c3cf241af9ecc205ba7d078354e38a7db5132974120c046ac23a2dd1df938` |
| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b` |
| `docs/coop/artifacts/fact-plane.v1.json` | `9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d` |
| `docs/coop/artifacts/c2-plan-stage-schema.v3.json` | `3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285` |
