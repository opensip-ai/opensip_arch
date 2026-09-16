# Provider-trace payload law: reconciliation and executed reconstruction (runtime source42.v3)

## The obligation and my earlier statement

- **Charter**, "Current incorporated correction owners" (line 248): *"When reconstructing the existing provider traces, apply the current negotiated payload selection, exact payload-byte representation and request/batch correlation law."* This belongs to the existing R-TRACE-* requirements. It is not new scope.
- **My source42.v2 result** (bytes preserved at `preserved/s42-v2-final/`):
  - Every trace's Hello/HelloAck negotiated `target-attribution-v2`, yet every `FactBatch` event was a frame name with no payload.
  - `HOST_ASSUMPTIONS` listed "payload schema validation" as a future-host item.
  - The review said "No Run negotiates target-attribution-v2 or FactBatchV3 occupancy companions; no claim is made about them", filed under "not constructed by any original requirement; read but not exercised".
  - R-TRACE-* were nevertheless marked executed.
  - **Assessment.** Those traces are exact transition evidence and remain valid as such, but they executed no payload law. The statement is withdrawn (HC-53; `blind-review.json#/priorIssueDisposition`).
- **Existing actual artifacts.** No complete Run retains FactBatch frames. The Runs build fact2 stores and captures directly, so no existing Run, trace or vector executed this law. Nothing prior is cited as payload evidence.

## Owners read

- `native-evidence.md`:
  - s9.1 lines 2774-2794 (majors; optional token; V3 iff echoed; V3 without token or V2 with token is `PROVIDER.PROTOCOL_VIOLATION`);
  - s9.2 line 2828;
  - s9.4 lines 2879-2888;
  - s9.6 lines 2896-3018.
- `native/fact-batch.schema.v3.json` (whole document), `native/dispatch-binding.schema.v1.json`, `native/occupancy-companion.schema.v1.json`.
- `foundation/provider-target-attribution-return.schema.v2.json` (return law, internal keys); `foundation/evaluator-fault-observation.schema.v3.json#/x-opensip-routes`.
- `foundation/evaluator-projection-registry.v1.json` (`targetNativeIdField`, `endpointTargetRungs`).
- `artifacts/fact-plane.v1.json`: `candidateSchema` (`transportRepresentation`), `relationPayloadSchemaRegistryV1` (`canonicalPayloadEncoding`, `sharedTypes`, `schemas`), `relationRegistry`, vectors, negativeFixtures.
- `artifacts/rust-provider-protocol.v2.json`: `AnalyzeV2`, `FactBatchV2`, `StageRequestV2`, `FactCandidateV1.wireAdjustment`, limits.
- `artifacts/delivery.v2.json`: `AnalyzeV1`, `StageRequestV1`, `FactCandidateV1`, `FactBatchV1`.
- `native/native-evidence.schemas.v2.json` HelloV3/HelloAckV3.

## Reconstruction (`ref/factbatch.py`, no author code)

- **Entry.** `buffer_fact_batch_occupancy(payload, hello_caps, ack_caps, dispatch, retained, request, host)` is the ANALYZING entry. Receipts and views are not parameters (s9.6 Timing).
- **Selection.** FactBatchV3 iff `target-attribution-v2` is on both Hello and HelloAck; otherwise historical FactBatchV2.
  - Token absent with a V3-shaped payload: `PROVIDER_RETURN_UNNEGOTIATED_V3`.
  - Token present: the payload must admit as FactBatchV3, so a V2 payload refuses `PROVIDER_RETURN_SCHEMA`.
  - V2 admission uses the rust-provider-protocol closed members, with closed FactCandidateV1 items in the kit's JSON-vector transcription.
- **Exact bytes.** A restricted deterministic-CBOR encoder and decoder built from `canonicalPayloadEncoding`:
  - accepted types: null, false, true, uint64, NFC text, definite array, definite text-keyed map;
  - map keys ascend by encoded key bytes;
  - refused: shortest-form violations, negative integers, floats, byte strings, tags, indefinite lengths, duplicate keys, non-NFC text, trailing bytes.
  - Admission of each candidate:
    1. the hex transcribes bytes;
    2. the bytes decode once;
    3. the decoded value equals `decodedRelationPayload`;
    4. `deterministic_cbor(decodedRelationPayload) == bytes` (`PROVIDER_RETURN_PAYLOAD_CBOR`);
    5. the closed relation payload schema holds, including resolution rules (`FACT_RELATION_PAYLOAD_INVALID`).
- **Request/batch correlation.**
  - `DispatchBindingV1` is derived from the current Analyze stage request (TS `StageRequestV1.stageId`; Rust `StageRequestV2.planStage.stageId`) and a retained Plan fragment, looked up by stage id. The fragment holds execution-plan rows, stage specs and closure kinds, and is not an admitted ExecutionPlan.
  - Schema: `dispatch-binding.schema.v1.json`.
  - Plan joins: planId, stage spec at `retainedStageOrdinal`, producer, and provider kind.
  - Consistency with the request.
  - Batch correlation: `stageId`, `analysisOrdinal`, `batchIndex`, and the contiguous candidate stream from `expectedFirstCandidateOrdinal` across batches (host stream counters).
- **Companions.**
  - Each ordinal must name a candidate in this batch.
  - The target universe must be byte-equal to the candidate's.
  - The relation needs a `targetNativeIdField` at a target rung.
  - `targetNativeId` must equal the decoded field.
- **Refusal handling.** Refusal is atomic. The public route comes from `x-opensip-routes`: provider-return goes to `PROVIDER.PROTOCOL_VIOLATION` and host-internal to `SYSTEM.OUTCOME.ILLEGAL_STATE`.
- **Check order and key binding.**
  - The check order is my own; no kit order exists. Every check runs, so later violations stay visible.
  - Keys are labelled by binding:
    - `kit-text`: a sentence names the key;
    - `key-name`: the published key whose name denotes the check;
    - `cb24`: no key is published (A-c1).
- **HC-51.** The companion schema publishes the order token `candidateOrdinal`. `ref/schemas.py` does not know it and refuses every lawful FactBatchV3 with `ORDER_ANNOTATION_UNKNOWN`. `PayloadKit` adds exactly that token and leaves `ref/schemas.py` byte-unchanged. A census shows only `fact-batch.schema.v3.json` uses it.
- **Exchanges.** `PayloadExchange` runs the published protocol3 table and applies the entry at each FactBatch that reaches ANALYZING. A refused payload faults the exchange, recorded as `payload:fact-batch-refused(KEY)`, the same kind of payload rule as the s9.1 echo. The refusal route is checked equal to the s10 fault projection.

## Executed (`logs/s42v3-p3b.*`, 0 assertion failures)

### `traces/payload-vectors.json`

71 vectors (13 selection, 9 bytes, 23 correlation, 26 companions), plus 29 decoder vectors, 10 encoder vectors, 4 exchange controls, 3 explanatory controls and 2 kit vector cross-checks.

- **Negotiated vs unnegotiated** (TS and Rust each):
  - admitted: V3 with the token; V2 without it (occupancy omitted, nothing buffered); V3 with empty companions;
  - V3 without the token refuses `UNNEGOTIATED_V3`, as does V2 plus `schemaVersion`;
  - V2 with the token refuses `SCHEMA`;
  - a FactBatchV1-shaped TS payload refuses `cb24.FACT_BATCH_V2_SCHEMA` (A-s42v3-1);
  - exchange controls: Hello-only or HelloAck-only token faults at HelloAck; both or neither passes with `identityNegotiated` true.
- **Exact bytes:**
  - both fact-plane vectors re-encode byte-equal and decode equal, and the kit candidates admit as V3 candidate items;
  - hand-assembled bytes equal the encoder;
  - these refuse `PAYLOAD_CBOR`: canonical JSON UTF-8 hex, alphabetical key order, non-shortest header, indefinite map, trailing byte, and hex of another lawful payload;
  - uppercase hex of the exact bytes refuses `SCHEMA` only;
  - byte-exact CBOR carrying an unknown field refuses `FACT_RELATION_PAYLOAD_INVALID`;
  - a missing rung-required field refuses `FACT_RELATION_PAYLOAD_INVALID` and masks `TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH`;
  - every forbidden profile item has a vector.
- **Correlation:**
  - TS Analyze selects Plan stages 1 and 3 as request ordinals 0 and 1;
  - dispatch coordinates are (retained 3, request 1); stage batches 0 and 1 give (1,0,0,0) and (1,0,1,3);
  - `stageId` refuses `STAGE_ID` when it is `"1"`, `"3"`, another requested stage, or Rust `"0"`; an integer refuses `SCHEMA` first;
  - `analysisOrdinal` mismatch refuses; `batchIndex` gap or replay refuses;
  - the stream refuses on restart or skip; an internal gap passes schema but refuses the stream check; duplicate or reverse order refuses `SCHEMA`;
  - dispatch refusals (host-internal): dispatch omitted (`DISPATCH`), `retainedStageOrdinal` equated with the request ordinal (`STAGE_SPEC`), extra dispatch member (`cb24` schema), plan mismatch, a non-stage producer, and a dispatch derived for another request;
  - 4097 candidates refuse `SCHEMA`;
  - explanatory: integer `stageId` lookup raises `ValueError`, and lookup by request ordinal selects the wrong stage.
- **Companions:**
  - admitted: a partial set with a gap; symbol, file-external-hint and package-first-party; package-unknown all null;
  - refused: unknown ordinal (atomic: nothing buffered), prior-batch ordinal, universe not byte-equal, `targetNativeId` differing from the payload or spelled as the inventory path, syntactic imports/calls rungs;
  - refused `SCHEMA` (16 cases): `planId`/`sourceFactId`/`producerClosure` members, every tested allOf branch, dot-dot LogicalPath, reversed or duplicate order.
- **HC-51:** the corrected token admits 40 V3 batches; the unchanged Kit refuses all 40.

### Traces

25 traces (6 complete, 3 unavailable, 2 cancel, 10 fault, 4 terminal). All 34 rows are exercised and rows are pairwise disjoint.

- 21 FactBatch payloads:
  - 19 validated: 13 V3 admitted, 1 V2 admitted, 5 refused;
  - 2 never validated, because a pre-match law faults first (WAIT_CANCELLED; post-terminal).
- Added traces:
  - negotiated multi-batch Analyze subset;
  - unnegotiated FactBatchV2;
  - HelloAck omitting the token;
  - V3 without the token;
  - V2 with the token;
  - `stageId` echoing the request ordinal;
  - candidate stream restarting at 0;
  - canonical JSON hex.
- TypeScript exchanges now use TypeScript caps and protocol major 2. HelloV3 fixes major 3, so their Hello payloads are admitted on the shared members with `protocolMajor` substituted and recorded.

## Standing

- **Executed.** These are executed schema, byte and join checks on constructed payloads. They are not future-host items merely because no worker process is spawned.
- **Not claimed:**
  - actual worker-process enforcement, or that a real provider emits these bytes;
  - OS, provider or compiler qualification.
- **Not constructed here:**
  - post-terminal `bind_worker_occupancy` (fact2 mint, views, stageReceipts, TargetAttributionV2 projection and capture, C15);
  - payload bodies of other frames;
  - anchor admission of the constructed candidates.
- **Own construction errors** (preserved):
  - `logs/s42v3-p3.0` (IndexError in a companion-list edit);
  - `logs/s42v3-p3.1` (TS protocolMajor 2 sent to HelloV3).
