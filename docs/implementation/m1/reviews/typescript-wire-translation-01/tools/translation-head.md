# TS2 wire translation inventory: `typescript-semantic` protocol major 2

**Standing.** This is a proposed implementation artifact for root review. It is not an approval, a wire change, a schema document or product code. It supplies the TS2 projection input that audit `m1-generation-owner-audit-01` marks as missing (T1; precision gaps G1–G3 and G7).

**Scope.** Every member of the inherited `docs/coop/artifacts/delivery.v2.json` `$.typescriptSemanticSubstrate.providerProtocol.wireSchema` sections `frameEnvelope`, `frameSchemas`, `definitions` and `payloadSchemas`. Each member is translated to major 2 under the dispositions of `docs/v2/contracts/product-v1/native-evidence.md` §0 (superseded selectors), §9.1, §9.4, §9.5 and §9.7. The exact native handshake and startup schema documents (`native/provider-handshake.schemas.v1.json`, `native/provider-startup.schemas.v1.json`) govern every replacement they specify. The following were **not** used: delivery v3–v5 and rust-provider-protocol v1/v3/v4. No original byte was rewritten. The candidate source45 and application46 design is taken as complete and is not re-reviewed.

**Machine form.** `fields.json` holds every row, including the exact original text, source path, SHA and selector. `coverage.json` holds the counts. `tools/build.py` regenerates both files and this document from `tools/rows_*.py`. It opens sources read-only and fails on any uncovered or extra member, unresolvable ref, wire-type mismatch against a resolvable ref, or unexpected successor member delta.

```
OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch python3 tools/build.py
```

## 1. Coverage

{{COUNTS}}

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

