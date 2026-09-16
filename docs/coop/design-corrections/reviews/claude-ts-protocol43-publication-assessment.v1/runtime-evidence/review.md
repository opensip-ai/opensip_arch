# Author assessment: typescript-semantic major 2 handshake and FactBatch payloads (frozen43)

**Standing.** This is the author's own assessment (Claude author-assessment
origin `f5617310-c7c7-4d85-acdd-31370f220944`). It is not an independent review,
not a blind-consumer result and not acceptance of the source or its application.
It is read-only. Nothing in frozen43, LIVE or earlier runtimes was changed. No
product code was implemented and nothing was committed or pushed. Any proposed
correction below is only a proposal and has not been applied. Reference-model
probes are design evidence. They do not qualify a compiler or worker.

## 1. Source custody

- Source tree: `/tmp/opensip-design-corrections/candidate-subject.v43`.
- Manifest: `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v43.json`.
- Manifest SHA-256: `db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d`.
- Full member verification is in `receipts/frozen43-verify.json`. All 12913 members were checked and 737769489 bytes were read. The result was: 0 missing, 0 mismatched, 0 size mismatches, 0 extra, `shaOk=true`, `ok=true`.
- Source42, source43 and all historical inputs were preserved. Nothing was written outside this runtime.

These are the pinned inherited owners. Their SHA-256 values match `native/source-pins.v2.json:47-80`:

| Path | SHA-256 |
|---|---|
| `docs/coop/artifacts/delivery.v2.json` | `47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3` |
| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b` |

Other bytes I cite, with their SHA-256:

| Path | SHA-256 |
|---|---|
| `docs/v2/contracts/product-v1/README.md` | `c53633c2…703e6` |
| `docs/v2/contracts/product-v1/native-evidence.md` | `66c6b82b…24cd` |
| `native/native-evidence.schemas.v2.json` | `2d37b810…6043` |
| `native/fact-batch.schema.v3.json` | `a963abd3…0de2` |
| `native/occupancy-companion.schema.v1.json` | `983864b1…861b` |
| `native/protocol3-transitions.v1.json` | `62d18f0e…1bd3` |
| `native/native_evidence_model.v2.py` | `6ffc6659…faf3` |
| `foundation/provider_attribution_return_model.v2.py` | `efb5f883…098e` |
| `foundation/check-provider-attribution-return.v2.py` | `0538fb14…080c` |
| `foundation/provider-target-attribution-return.schema.v2.json` | `2d5719b5…523f` |
| `foundation/execution_inputs_model.v1.py` | `66a15add…9ea1` |
| `native/native-cases.v2.json` | `c16fc62b…4d60` |

Full digests are in `review.json`.

## 2. Read paths and ranges

**Precedence law**
- `docs/v2/contracts/product-v1/README.md:29-58`. The selector tables decide which recipes apply. An explicit successor wins over a named inherited selector only within its declared scope. Any unresolved overlap is a design defect.

**`docs/v2/contracts/product-v1/native-evidence.md`**
- `:1-104`: standing.
- `:108-131`: §0 exact superseded-selector table.
- `:2770-3009`: §9.1-§9.6 and the producer mapping.
- `:3234`: HelloAck mismatch fault row.
- `:3788-3806`: §12 reference-evidence scope.

**`docs/v2/contracts/product-v1/identity-and-evidence.md`**
- `:237-263`: capability-manifest successor scope. It names no protocol payload.
- `:1496`: FactBatchV3 occupancy reference.

**`delivery.v2.json`, TS provider protocol** (`$.typescriptSemanticSubstrate.providerProtocol`)
- `major`
- `wireSchema.limits`
- `wireSchema.frameEnvelope`
- `wireSchema.payloadSchemas.{HelloV1 (:846), HelloAckV1 (:847), FactBatchV1 (:855), AnalyzeV1, UnavailableV1, CompleteV1}`
- `wireSchema.frameSchemas (:864-879)`
- `wireSchema.definitions.{FactCandidateV1, StageResultV1}`
- `wireSchema.commitments`
- `ordering`
- `closedWorkerToHostFrames`
- `wireSchemaCommitment`
- The TS descriptor `handshakeRequired` field (`:623`).

**`rust-provider-protocol.v2.json`**
- `protocolIdentity`, `limits`, `limitsHandshake`
- `wireSchema.envelope`
- `wireSchema.payloadSchemas.{HelloV2, HelloAckV2, FactBatchV2}`
- `wireSchema.definitions.FactCandidateV1`

**Native design-correction files**
- `native/native-evidence.schemas.v2.json`:
  - `:862-879`: `CapabilityToken`.
  - `:3985-4124`: `ProtocolLimitsV3`, `HelloV3`, `HelloAckV3`.
- `native/fact-batch.schema.v3.json:1-124`, the whole file.
- `native/occupancy-companion.schema.v1.json:318-331`: `x-opensip-wire`.
- `native/protocol3-transitions.v1.json`: grep only.
  - Hits: `:91` (guardLaw), `:94` and `:140` (HelloAck rows).
  - It never mentions `typescript` or `delivery.v2`.
- `native/native_evidence_model.v2.py:545-576`: the `TS2_TOKENS` constant and `negotiate()`.
- `native/native-cases.v2.json`: fixtures `ts2` and `ts2Attribution`, plus negotiation cases 0-3.
- `native/source-pins.v2.json:47-80`.

**Foundation files**
- `foundation/provider_attribution_return_model.v2.py:1-80` and `:317-397`.
- `foundation/check-provider-attribution-return.v2.py:30-49` and `:300-330`.
- `foundation/provider-target-attribution-return.schema.v2.json:125-149`.
- `foundation/execution_inputs_model.v1.py:96-113`.

**Context only**
- `docs/coop/artifacts/delivery.v4.json`. This is capability-manifest lineage, not a TS protocol owner.

I read no other reviewers' runtimes, consumer inputs or answers, or root outcome material.

## 3. What the precedence table actually does to the TS protocol

§0 (`native-evidence.md:112-127`) names exactly one typescript-semantic wire selector:
`$.typescriptSemanticSubstrate.wireSchema.definitions.CoverageResultV1.completenessRule`.
It is superseded by `CoverageResultV3`.

§0 names none of these:

- `providerProtocol.major` (value `1`)
- `wireSchema.frameEnvelope.fields.protocolMajor` ("uint64; exactly 1")
- `payloadSchemas.HelloV1`
- `payloadSchemas.HelloAckV1`
  - `protocolMajor` is "uint64 exactly 1".
  - `capabilities` is "exact sorted array [multi-stage-analyze-v1,sealed-vfs-v1,typescript-semantic-facts-v1]".
- `payloadSchemas.FactBatchV1`
- `frameSchemas.FactBatch.payloadType` (`FactBatchV1`)
- `commitments.domains.factBatch`

The Rust row (`:118`) supersedes only these Rust selectors: `RepositoryResolutionV2`, `CoverageResultV2`, `UnavailableV2.fields.reason`, `$.limits` and `phaseValues`.

So under the README law, every TS change has to come from the prose in §9.1, §9.4 and §9.6, or from a published successor artifact that declares its scope. The next sections check whether that prose is an exact substitution.

## 4. Per-question derivation

### 4.1 Token set and identity versions: determined (no defect)

§9.1 (`:2775-2780`) gives the TS token set.
- The four identity tokens: `source-identity-snapshot2`, `plan-identity-plan2`, `fact-identity-fact2`, `coverage-v3`.
- Also: `sealed-vfs-v1`, `multi-stage-analyze-v1`, `typescript-semantic-facts-v1`, `resolution-completeness-v2`, `unresolved-edge-v1`, `native-context-v2`.
- `dependency-source-v1` and `prepared-output-v3` are marked "(Rust)". §9.4 confirms that TS has no dependency-source or prepared frames.
- `target-attribution-v2` is optional and is not an identity token (`:2785-2787`).

The rest is also stated:
- identityVersions values: `{snapshot:2, plan:2, fact:2, coverage:3}` (`:2781`).
- Equality law: exact recursive equality (`:2804`).
- On mismatch: `FAULT`, `PROVIDER.PROTOCOL_VIOLATION`, and no source byte is sent (`:2805-2806`, `:3234`).

The reference agrees:
- `native_evidence_model.v2.py:551-555` has `TS2_TOKENS` and `TS2_TOKENS_ATTRIBUTION`.
- `native-cases.v2.json` has fixtures `ts2` and `ts2Attribution`.
- `check-provider-attribution-return.v2.py:42-46` has `TS_TOKENS`.

**Classification: no defect.** What is not determined is where these values travel in the TS payloads. That is §4.2.

### 4.2 TS major-2 Hello / HelloAck payloads: not reconstructible (MUST)

**What the owners say**
- §9.1 names `HelloV3` / `HelloAckV3` as the frames that carry the token array and `identityVersions` (`:2781-2782`).
- §9.4 says TS major 2 "Adds identity negotiation". It does not name a TS Hello or HelloAck payload, its fields, or its limits.
- §9.3 (`ProtocolLimitsV3`, "exact equality in Hello") lists 8 members and "All 24 v2 limits". Those 24 are the Rust `rust-provider-protocol.v2` limits. TS delivery.v2 has 10 numeric limits and a `limitRule`, with different members.

**The published schemas cannot carry TS as written**
- `HelloV3` (`schemas.v2.json:4025-4076`) is closed and has `protocolMajor: {const: 3}`. It requires `expectedCapabilities`, `identityVersions` and `limits: ProtocolLimitsV3`.
- `HelloAckV3` (`:4077-4124`) is closed and has `protocolMajor: {const: 3}`. It requires `capabilities` and `identityVersions`.
- `ProtocolLimitsV3` (`:3985-4024`) is closed with only the 8 Rust dependency-source, prepared, cfg and unresolved-edge constants.

**No owner tells a reader how to build the TS handshake from them.** A reader would have to choose between:

- **Reading A (project the V3 schemas onto TS):** use HelloV3/HelloAckV3 with `protocolMajor` 2. No owner gives that instruction. The schemas refuse major 2, and ProtocolLimitsV3 refuses the TS limits (probe below).
- **Reading B (apply §9.4 as a delta to delivery.v2):** keep HelloV1/HelloAckV1, set major 2, replace the fixed three-token `capabilities` with the negotiated array, and add `expectedCapabilities` and `identityVersions`. No owner gives this field list either.

**Concrete discriminators (TS worker, token absent)**

*Hello-A:*

```json
{"protocolMajor":2,
 "expectedCapabilities":["source-identity-snapshot2","plan-identity-plan2","fact-identity-fact2","coverage-v3","sealed-vfs-v1","multi-stage-analyze-v1","typescript-semantic-facts-v1","resolution-completeness-v2","unresolved-edge-v1","native-context-v2"],
 "identityVersions":{"snapshot":2,"plan":2,"fact":2,"coverage":3},
 "limits":{"maxDependencySourcePackages":4096,"maxDependencySourceEntries":1000000,"maxDependencySourceTotalBytes":8589934592,"maxDependencySourceChunkBytes":1048576,"maxUnresolvedEdgesPerStage":1000000,"maxCfgSets":4,"maxExpansionRows":1000000,"maxGeneratedFileRows":1000000}}
```

*Hello-B:*

```json
{"hostBuildId":"…",
 "expectedProviderDescriptorSha256":"…",
 "expectedRuntimeDescriptorSha256":"…",
 "limits":{"maxFramePayloadBytes":67108864,"maxSnapshotChunkBytes":1048576,"maxSnapshotEntries":200000,"maxAnalyzeStages":1024,"maxRelationsPerStage":64,"maxRequestedCoverageKeysPerStage":128,"maxFactBatchFacts":4096,"maxFactCandidatePayloadBytes":1048576,"maxCoverageEntriesPerFrame":4096,"maxStderrBytes":262144},
 "expectedCapabilities":[…same ten…],
 "identityVersions":{…}}
```

In Hello-B, major 2 appears only in the envelope, as in HelloV1.

- A closed decoder that follows B refuses Hello-A. Three HelloV1 fields are missing, and the limits map is not the delivery.v2 numeric map.
- A decoder that follows A refuses Hello-B, because of `additionalProperties:false`.

*HelloAck:*
- Ack-A is `{protocolMajor:2, capabilities:[…], identityVersions:{…}}`.
- Ack-B is the 14 HelloAckV1 fields, with `protocolMajor` 2, the token array in `capabilities`, plus `identityVersions`.
- Each refuses the other.

**Choices that stay unpinned in either reading**
- **Array order:**
  - HelloAckV1 uses an "exact sorted array".
  - HelloV3 and HelloAckV3 use `x-opensip-order: "sequence"`.
- **ProtocolLimitsV3 members for TS:** whether any of them (for example `maxUnresolvedEdgesPerStage`, relevant because TS negotiates `unresolved-edge-v1`) join the TS limits map.
- **Where `protocolMajor` lives:** only in the envelope (HelloV1 style) or also in the payload (V3 style).

**Why this is not only a missing convenience schema.** A TS JSON Schema is not needed if an exact substitution already defines the payload. Here none does:
- §9.4 is a list of capabilities, not a field-level delta.
- The only field-level successor (HelloV3/HelloAckV3) is fixed to major 3 by its own bytes.
- Pure inheritance (HelloAckV1 unchanged) cannot express identity tokens at all, because its `capabilities` is fixed at three legacy tokens. So §9.4 cannot be applied as a no-op either.

**Practical consequence**
- A host and a TS worker can each be built "conformant" from frozen43 and still meet `FAULT` / `PROVIDER.PROTOCOL_VIOLATION` at Hello or HelloAck. That happens before OpenUniverse and before any source byte. It affects every `ts-tsconfig`, `js-allowjs` and `js-synthesized` semantic cell (`:3001`).
- Under reading A, the handshake silently loses the provider and runtime descriptor checks (`providerBuildId`, `nodeVersion`, `typescriptCompilerSha256`, `typescriptStdlibMerkleRoot`, `defaultWorkBudgetProfileSha256`, `platformId`, …).
- The retained TS `FactCandidateV1.producerVersion` is defined as "exact providerBuildId from the verified handshake". It would then have no source.

**Classification: MUST, missing wire law.** It is also an unresolved overlap under `README.md:53-54`.

**Exact selectors**
- `native-evidence.md:2774-2794` (§9.1)
- `native-evidence.md:2879-2888` (§9.4)
- `native-evidence.md:2872-2877` (§9.3)
- `native-evidence.md:112-127` (§0)
- `native-evidence.schemas.v2.json#/$defs/HelloV3`, `#/$defs/HelloAckV3`, `#/$defs/ProtocolLimitsV3`
- `delivery.v2.json#/typescriptSemanticSubstrate/providerProtocol/wireSchema/payloadSchemas/HelloV1`, `…/HelloAckV1`, `…/wireSchema/limits`, `…/wireSchema/frameEnvelope/fields/protocolMajor`, `…/providerProtocol/major`

### 4.3 Protocol major value 2: value determined, selector table incomplete (SHOULD)

§9.1 (`:2774`, `:2792`), §9.4's title, `occupancy-companion.schema.v1.json:329` and `provider-target-attribution-return.schema.v2.json:138` all state typescript-semantic major 2. No reading of current law keeps the value 1. The override is definite in value.

The retained delivery.v2 selectors, however, still say "exactly 1" and have no §0 row:
- `providerProtocol.major`
- `frameEnvelope.fields.protocolMajor`
- `HelloAckV1.fields.protocolMajor`

**Classification: SHOULD, incomplete exact-selector table.** There is no competing wire value. Which fields carry the value is part of §4.2. The correction in §6 P2 covers this.

### 4.4 Unnegotiated TS FactBatch (token absent): incompatible readings (MUST)

**What the owners say**

For **Reading U-V1**, the retained delivery.v2 `FactBatchV1` `{analysisOrdinal, stageId, batchIndex, facts, batchCommitment}` (`delivery.v2.json:855`) stays:
- §0 supersedes no TS FactBatch selector.
- §9.4's delta list does not touch FactBatch.
- §9.6 says "Native §9.4 retains TS `delivery.v2` `AnalyzeV1.stageRequests`" (`:2912`).
- `provider-target-attribution-return.schema.v2.json:138` says "typescript-semantic protocol major 2. Unchanged frames."
- `fact-batch.schema.v3.json:31` names "Historical FactBatchV1/V2.stageId".
- The retained `commitments.domains.factBatch` (`opensip.ts-provider.fact-batch.v1`) only has a carrier in V1.

For **Reading U-V2**, the payload is "historical FactBatchV2", whose only definition in the pinned owners is `rust-provider-protocol.v2.json` `FactBatchV2` `{analysisOrdinal, stageId, batchIndex, candidates}`:
- §9.1 says: "When absent, historical FactBatchV2 remains … a FactBatchV2 payload with the token, is `PROVIDER.PROTOCOL_VIOLATION`" (`:2788-2791`).
- §9.6 says: "Historical FactBatchV2 remains the payload when the token is absent" (`:2952`).
- §9.6 calls `stageId` the "historical V2 name" in a paragraph that covers TS (`:2917`).
- `fact-batch.schema.v3.json:5` and `x-opensip-negotiation.whenAbsent` (`:119`) say: "MUST admit as historical FactBatchV2 (no schemaVersion, no occupancyCompanions)". V3 minus those two members is exactly Rust V2, not TS V1.
- `occupancy-companion.schema.v1.json:327` is `historicalFactBatchV2`.
- `execution_inputs_model.v1.py:109` says: "FactCandidateV1/FactBatchV2 stay closed when token … absent".

None of these statements is language-qualified. None names the TS `FactBatchV1` selector. TypeScript has never had a FactBatchV2. So the successor text does not declare a scope that covers the TS selector, and the retained TS selector conflicts with it. That is an unresolved overlap.

**Concrete discriminator** (TS worker, token not negotiated, one-stage Analyze):
- **Batch-1** `{"analysisOrdinal":0,"stageId":"s","batchIndex":0,"facts":[c0],"batchCommitment":"sha256:<H(opensip.ts-provider.fact-batch.v1, facts)>"}`
  - Admitted under U-V1, with the commitment verified.
  - Under U-V2 it is a closed-payload mismatch with unknown `facts`/`batchCommitment` and missing `candidates`, so it becomes `PROVIDER.PROTOCOL_VIOLATION`.
- **Batch-2** `{"analysisOrdinal":0,"stageId":"s","batchIndex":0,"candidates":[c0]}`
  - The mirror result: admitted under U-V2, a protocol violation under U-V1.

**Practical consequence**
- Token-absent is the default path, because `target-attribution-v2` is optional (`:2785-2787`). So every TS FactBatch in a non-attribution run is either admitted or a provider-protocol fault, depending on which owner the implementer follows.
- Whether the per-batch `factBatch` commitment is verified also depends on the reading.

**Reference cannot discriminate** (reference-only probe, `probes/probe-output.json`):
- Token absent: `provider_attribution_return_model.v2.py:317-328` `_token_gate` returns `{status: omitted, delivery: "unnegotiated-fact-batch-v2"}` for Batch-1, for Batch-2 and for `{"not":"a batch"}` alike. It never validates the historical shape.
  - That is within the model's occupancy scope. It is not evidence for either reading.
- Token present: `validate_schema(fact-batch v3)` refuses both Batch-1 and Batch-2.

**Classification: MUST, unresolved overlap.**

**Exact selectors**
- `native-evidence.md:2787-2791`, `:2917`, `:2948-2953`
- `fact-batch.schema.v3.json#/description` and `#/x-opensip-negotiation/whenAbsent`
- `occupancy-companion.schema.v1.json#/x-opensip-wire/historicalFactBatchV2`
- `delivery.v2.json#/typescriptSemanticSubstrate/providerProtocol/wireSchema/payloadSchemas/FactBatchV1`, `…/frameSchemas/FactBatch/payloadType`, `…/wireSchema/commitments/domains/factBatch`
- `native-evidence.md:112-127` (§0 has no row)

### 4.5 Negotiated TS FactBatchV3: field set determined (no defect), with two SHOULD/advisory notes

`fact-batch.schema.v3.json` is an explicit successor. Its declared scope is "FactBatch payload iff Hello/HelloAck negotiated target-attribution-v2". Its own text covers TS: "StageRequestV1.stageId (TS delivery.v2)" (`:31`, `:112`), and §9.6 does the same (`:2950`, `:2954`). Within that scope it wins over TS `FactBatchV1` under the precedence law.

The exact negotiated TS payload is a closed map:

| Member | Value |
|---|---|
| `schemaVersion` | `3` |
| `analysisOrdinal` | uint64, an echo of `AnalyzeV1.analysisOrdinal`. That value is "exactly 0" for TS, so the echo is `0`. |
| `stageId` | text, 1..255 bytes, echo of `StageRequestV1.stageId` |
| `batchIndex` | uint64, contiguous from 0 per requested stage |
| `candidates` | 1..4096 closed `FactCandidateV1`, ordered by `candidateOrdinal` (see below) |
| `occupancyCompanions` | 0..4096 `OccupancyCompanionV1`, at most `len(candidates)`, ordered by `candidateOrdinal` |

- There is no `facts` member and no `batchCommitment`.
- Each `FactCandidateV1` has the 14 delivery.v2 fields: `candidateOrdinal`, `relation`, `resolution`, `layer`, `producer`, `producerVersion`, `schemaVersion`, `language`, `sourceUniverseId`, `targetUniverseId`, `confidenceMillionths`, `relationSchemaId`, `canonicalRelationPayload`, `anchors`.
- `canonicalRelationPayload` is a deterministic-CBOR byte string of at most `maxFactCandidatePayloadBytes`.
- The schema's length caps on the candidate strings also apply.
- Frame name: `FactBatch`.
- The envelope major value is 2 (§4.3).

This field set is fixed by bytes, not by projection.

Two conditions:
- The payload is only reachable once a TS HelloAck can carry the token (§4.2).
- On the wire, `canonicalRelationPayload` is a byte string. `canonicalRelationPayloadHex` and `decodedRelationPayload` are the JSON-vector and TCB-observation forms. The schema says so itself: "JSON-vector transcription of FactCandidateV1.canonicalRelationPayload" and "Not a wire field" (`:80`, `:84`), and so does §9.6 (`:2903-2906`).

**S2 (SHOULD): the batch-commitment disposition is not stated.**
- On negotiated TS batches the closed V3 schema drops `batchCommitment`. So `delivery.v2` `commitments.domains.factBatch` has no carrier.
- `StageResultV1.factCommitment` and `CompleteV1.factStreamCommitment` are still defined over the ordered `FactCandidateV1` stream, so they still work.
- The override is definite and there is no alternative wire reading. But the loss of per-batch integrity is never stated. A reader may reasonably wonder whether it was intended.

**A1 (advisory): limit name.**
- §9.1 (`:2793`) and `fact-batch.schema.v3.json#/x-opensip-negotiation/helloLimits` bound companions by "existing `maxFactBatchCandidates` (4096)".
- That member exists only in Rust v2 limits. The TS member is `maxFactBatchFacts` (4096).
- The value is the same, and the schema hard-codes `maxItems: 4096`, so no payload is admitted differently. This is naming only.

**A2 (advisory): wire projection note.**
- The V3 schema is the JSON-vector admission form. The wire projection (hex → byte string, no `decodedRelationPayload`) is stated in field descriptions, not in one place.
- It is determined, but a one-line statement would remove any doubt.

### 4.6 Summary answer

> Does prose substitution fully determine the TS shape, or are incompatible admissible wire readings possible?

| Item | Determined? | Classification |
|---|---|---|
| Token set, `identityVersions` values, equality and fault law | yes | no defect |
| `protocolMajor` value 2 | value yes; §0 row missing | SHOULD (S1) |
| TS Hello fields and limits member set | **no** (A/B readings) | **MUST (M1)** |
| TS HelloAck fields, capabilities array order, placement of `protocolMajor` | **no** | **MUST (M1)** |
| Unnegotiated TS FactBatch | **no** (U-V1/U-V2) | **MUST (M2)** |
| Negotiated TS FactBatchV3 field set, caps and `schemaVersion` | yes (explicit successor), once M1 is fixed | no defect |
| V3 `batchCommitment` loss | definite; consequence unstated | SHOULD (S2) |
| `maxFactBatchCandidates` vs `maxFactBatchFacts` | same 4096 | advisory (A1) |
| V3 JSON-vector vs wire projection | determined by descriptions | advisory (A2) |
| Duplicate TS JSON Schema | optional convenience only | not a defect in itself |

## 5. Reference-model scope (reference-only)

- `negotiate()` (`native_evidence_model.v2.py:558-575`) compares only token sets. It has no payload field, major or limits input.
- `protocol3-transitions.v1.json` covers Rust major 3 only.
- §12 (`:3805-3806`) states that nothing executes a compiler or provider.

Probe: `probes/ts_protocol_probe.py`, run with `/tmp/opensip-architecture-review-env/bin/python -I -B`. It imports the frozen models read-only and writes only `probes/probe-output.json`. Results:
- `HelloV3` and `HelloAckV3` with `protocolMajor` 2 are refused ("exact const type/value mismatch"). With 3 they are valid.
- `ProtocolLimitsV3` with the TS delivery.v2 numeric limits is refused: 10 additional properties.
- `negotiate(ts2, ts2, ts2)` returns `accepted`, `identityNegotiated=true`, and no payload shape.
- Token absent: `_token_gate` omits Batch-1 (TS V1 shape), Batch-2 (Rust V2 shape) and junk identically. A V3 batch is refused with `PROVIDER_RETURN_UNNEGOTIATED_V3`.
- The V3 schema refuses both historical shapes and accepts V3.

None of this qualifies a TS worker or host. The probe shows only that the reference does not settle M1 or M2.

## 6. Smallest proposed correction (not implemented)

**P2 fixes M1 and S1.** It adds an exact TS major-2 handshake statement to §9.4, plus §0 rows.

*§0 row.* Source `delivery.v2.json`, selectors:
- `$.typescriptSemanticSubstrate.providerProtocol.major`
- `…wireSchema.frameEnvelope.fields.protocolMajor`
- `…wireSchema.payloadSchemas.HelloV1`
- `…wireSchema.payloadSchemas.HelloAckV1`

Disposition: **Superseded** by the typescript-semantic major-2 Hello and HelloAck of §9.4.

*§9.4 text.* This is the author's recommendation: the smallest delta that keeps the inherited descriptor checks the retained TS `FactCandidateV1.producerVersion` depends on.
- Envelope `protocolMajor` exactly 2.
- **Hello (TS major 2)** is closed:
  - Keep HelloV1's required members `hostBuildId`, `expectedProviderDescriptorSha256`, `expectedRuntimeDescriptorSha256` and `limits`.
  - `limits` stays the closed map equal to the delivery.v2 `wireSchema.limits` numeric fields, unchanged. `ProtocolLimitsV3` does not apply to typescript-semantic.
  - Add `expectedCapabilities`: the §9.1 TypeScript token set from the signed row, with optional `target-attribution-v2`.
  - Add `identityVersions` `{snapshot:2, plan:2, fact:2, coverage:3}`.
- **HelloAck (TS major 2)** is closed:
  - Keep HelloAckV1's 14 required members.
  - `protocolMajor` becomes exactly 2.
  - `capabilities` becomes the exact echo of Hello `expectedCapabilities`, replacing the fixed three-token array.
  - Add `identityVersions`, an exact echo.
- State one array-order rule. I recommend keeping HelloAckV1's sorted-ascending unique rule.
- If the owner wants a TS `maxUnresolvedEdgesPerStage`, that is a separate requirement decision. P2 does not add it.
- A `$defs/TypeScriptHelloV2` / `TypeScriptHelloAckV2` pair in `native-evidence.schemas.v2.json` is optional convenience once the prose is exact.
- Alternative, not recommended: adopt HelloV3/HelloAckV3 for TS with major relaxed to 2 and a TS limits definition. This is larger, drops the descriptor checks, and would need a new `producerVersion` source.

**P1 fixes M2.** It language-qualifies the absent-token payload at every current statement.

Replacement text: "When absent, the historical per-language payload remains: typescript-semantic major 2 → `delivery.v2` `FactBatchV1` `{analysisOrdinal, stageId, batchIndex, facts, batchCommitment}` unchanged, including `commitments.domains.factBatch`; rust-semantic major 3 → `rust-provider-protocol.v2` `FactBatchV2`. A FactBatchV3 payload without the token, or that language's historical payload with the token, is `PROVIDER.PROTOCOL_VIOLATION`."

Apply it at:
- `native-evidence.md:2788-2791`
- `:2952`
- the `:2828` row (Rust-only table, where it is already correct for Rust; add a pointer)
- `fact-batch.schema.v3.json#/description`
- `fact-batch.schema.v3.json#/x-opensip-negotiation/whenAbsent`
- `occupancy-companion.schema.v1.json#/x-opensip-wire/historicalFactBatchV2`

Also:
- At `:2917`, change "historical V2 name" to "historical FactBatchV1/V2 name".
- Add a §0 row. Source `delivery.v2.json`, selectors `…payloadSchemas.FactBatchV1` and `…frameSchemas.FactBatch.payloadType`. Disposition: **Retained** when `target-attribution-v2` is not negotiated; replaced by `FactBatchV3` (§9.6) when negotiated.
- The `execution_inputs_model.v1.py:109` note would need the same language qualification. It is reference text.
- Alternative, not recommended: supersede TS V1 by the Rust V2 shape. That is larger, because it removes the TS per-batch commitment domain from the non-attribution path.

**P3 fixes S2.** Add one sentence in §9.6: "Negotiated FactBatchV3 carries no `batchCommitment`; typescript-semantic `commitments.domains.factBatch` applies only to FactBatchV1; `StageResultV1.factCommitment` and `CompleteV1.factStreamCommitment` remain over the ordered `FactCandidateV1` stream." If the owner instead intends a per-batch commitment on V3, that is a schema change and outside this minimal proposal.

**P4 fixes A1 and A2.**
- At `:2793` and in `helloLimits`, write "`maxFactBatchCandidates` (Rust) / `maxFactBatchFacts` (TypeScript), both 4096".
- Add one line stating that on the wire `canonicalRelationPayloadHex` is carried as the `canonicalRelationPayload` byte string and `decodedRelationPayload` is absent.

**Reference.** No model change is required. Optionally, a check case could record the per-language historical payload and a TS major-2 HelloAck shape once P1/P2 exist. `_token_gate` shape validation lies outside the occupancy model's scope.

## 7. Out-of-question observation (not classified here)

- The Rust `HelloV3` schema omits HelloV2's `hostBuildId`, `expectedProtocolContractSha256` and `expectedIdentity`.
- `HelloAckV3` omits HelloAckV2's identity members.
- `ProtocolLimitsV3` is closed at 8 members while §9.3 says "All 24 v2 limits are retained … exact equality in Hello".
- The §0 Rust row names neither `HelloV2`/`HelloAckV2` nor `FactBatchV2`/envelope.

This is the Rust counterpart of M1. It weakens reading A for TS further. It needs its own bounded question and is not assessed or classified here.

## 8. Limitations

- **Scope:** the TS handshake and FactBatch only. TS `CoverageV3`, `NativeContextVerified` ordering within the delivery.v2 `ordering.normalPhases`, and `Unavailable` reasons were not assessed beyond noting that §9.4 names them.
- **Probes** are reference-only and not qualification.
- **Standing:** this is an author assessment, not independent assent.
