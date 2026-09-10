# Provider-return end-to-end v3

**Standing.** Actual Grok DESIGN COAUTHOR continuing COMPLETE29. COMPLETE58 retained, not accepted. Provider58 `/tmp/opensip-design-corrections/target-provider-return-successor.v1` read-only and unedited. COMPLETE29 proposed21 is a separate read-only copy under peer3 review; this turn does not mutate 29/source58/peer source. Writes only `/tmp/opensip-design-corrections/grok-provider-return-end-to-end-author.v3/output`. No pin seal, freeze, product implementation, commit, or full-suite claim. No self-acceptance.

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`.

Source: own prior v2 `.../author.v2/output/proposed` + unchanged provider58. Root query/proof/closure copies offlimits.

---

## Root corrections applied

### 1. stageId / Analyze correlation / timing

Native §9.4 retains TS `delivery.v2` `AnalyzeV1.stageRequests`. `StageRequestV1.stageId` is C-2 **text**; `stageOrdinal` is contiguous in **this Analyze**. Rust `AnalyzeV2` `StageRequestV2` has `stageOrdinal` + nested `planStage` (C-2 bytes with original `stageId`). Provider Analyze may be a **subset** of Plan stages.

FactBatchV3 **preserves** historical `stageId` as **string C-2 text**. Intentional field-type correction from author v2 integer typing. Corresponding request: worker echoes `StageRequestV1.stageId` / `StageRequestV2.planStage.stageId`. No new worker field; no implicit new channel. schemaVersion remains 3.

Host `DispatchBindingV1` (`native/dispatch-binding.schema.v1.json`) is a required TCB observation derived at Analyze dispatch: `planId`, `retainedStageOrdinal`, `analyzeRequestOrdinal`, `expectedStageId`, `expectedAnalysisOrdinal`, `expectedBatchIndex`, `expectedFirstCandidateOrdinal`, `producerClosure`, `stageSpecDigest`. Correlation: `batch.stageId == expectedStageId`; `batch.analysisOrdinal == expectedAnalysisOrdinal`; `batch.batchIndex == expectedBatchIndex`; execution-plan lookup uses `retainedStageOrdinal`. Request ordinal is not retained ordinal. Omitting dispatch refuses `PROVIDER_RETURN_DISPATCH`.

Timing: `buffer_fact_batch_occupancy` during ANALYZING (dispatch required; receipts/views MUST NOT be required). After Coverage/Complete → native view → stageReceipt → `capture_occupancy` / `bind_worker_occupancy` (dispatch AND receipts/views required; selected view digest must appear on receipt `outputRefs`).

Lingering `batch.stageOrdinal` prose removed. Native §9.1: four identity tokens remain; `target-attribution-v2` is an additional optional capability, not an identity token.

### 2. Root helper probes (author29 overlay, modelSha256 `780c1d2c…`, not full Run)

| Probe | author29 | v3 |
|---|---|---|
| valid-helper | ADMIT `1c5df32c…` | ADMIT same digest on the **handmade helper** path (TCB-assumed `fact2:111…`). Owner-admitted positive is a separate case. |
| missing-required-receipt-and-analysis-context | ADMIT same digest | **REFUSE** `PROVIDER_RETURN_DISPATCH` (required observation; analysisOrdinal=77 cannot bypass) |
| different-anchor-same-length | ADMIT | **REFUSE** `PROVIDER_RETURN_MINT_MISJOIN: anchors` (entire `(path, blobDigest/contentSha256, startByte, endByte)`, not count) |
| second-compatible-batch-only-current-mint-map | REFUSE `TARGET_ATTRIBUTION_FACT_NOT_IN_PLAN` for prior `fact2:111…` | **ADMIT** current batch; prior facts are not required in this-batch mint map. Combined occupancy-conflict uses sidecars (`AM._admit_provider_occupancy_conflicts` does not use facts). |

Positive two-batch/two-stage and negative provider-conflict at the current-mint-map boundary are checker cases, not only a negative with an augmented map. Diagnostics remain helper probes, not fullRun.

### 3. Owner-admitted positive

`test_owner_admitted_semantic_fixture_positive` uses `evaluator_semantic_fixture.build_ts_semantic_graph(imports, subject_kind=file)` + `attach_host_capture` + M3 `open_run_closure` / `derive` / `replay` / `close_run`. Candidate CBOR is transcribed from the owning fact payload/anchors (`path`, `blobDigest`, `startByte`, `endByte`); fact2 payload schema is unchanged. Binder is driven from those records. Captured sidecar digest is compared to the fixture sidecar digest. Malformed receipt `outputRefs` through the same path refuses `PROVIDER_RETURN_VIEW_NOT_ON_RECEIPT`.

**Preadmitted observations:** fixture-minted fact2, view, inventories, enumeration plan, execution-plan/stage-spec, hostCapture receipts, DispatchBindingV1 derived from that stage, mint map as a host TCB observation of already-admitted mint.

**Runtime verification:** M3 close APIs on the same graph. The occupancy helper does **not** prove FACT-ID-V1 or compiler TCB authenticity.

Handmade helper facts remain labeled TCB assumptions for narrow join comparison.

### 4. Array-order vocabulary / schema completeness

`candidateOrdinal` is published in `occupancy-companion.schema.v1.json` `x-opensip-order-vocabulary` (blindkit JSON) with closed meaning: integer unique strictly increasing; gaps lawful at the annotation. Contiguous 0..n-1 across batches of one requested stage is a separate candidate-stream law joined to `DispatchBindingV1.expectedFirstCandidateOrdinal`. `canonical.py` implements that token; it is not Python-only vocabulary. Order-law metadata is retained.

New schemas are independently complete: `FactBatchV3.occupancyCompanions.items` `$ref` `opensip.product.occupancy-companion.1` (including allOf); return `records.items` `$ref` `opensip.product.target-attribution.2`. Validators use `referencing.Registry`. **No import-time mutation** of schema dictionaries. External/package/unknown companion branches are checker cases.

### 5. shared-profile-decisions

Stale “enumeration/atom joins / full independent replay still pending” from an older phase is replaced. Current reference evidence (`check-enumeration`, `check-atoms`, `check-semantic-replay`, `check-provider-attribution-return`) is described as reference, not product qualification. No premature final assent. LIVE D9 / OS / compiler remain future.

---

## Controls (not full Run, not LIVE D9, not compiler qualification)

Disposable overlay: `output/overlay` (provider58 design-corrections except reviews/completion + provider58 artifacts + proposed). Owner-positive requires artifacts such as `delivery.v4.json`; v2 overlay that copied only `check-fact-plane.py` is insufficient for that case.

| Check | Result | First-run failures |
|---|---|---|
| `check-provider-attribution-return.v2.py` | **42/42** | (1) `FileNotFoundError` `overlay/docs/coop/artifacts/delivery.v4.json` until provider58 artifacts were copied; (2) `PROVIDER_RETURN_UNIVERSE_MISMATCH` on owner-positive because helper `companion()` hardcoded universe `11…` instead of the fixture universe. Final none. |
| `check-array-orders.py` | **121/121** failed `[]` | none |
| native `negotiate` + CapabilityToken enum | accepted with token; no-spawn if Plan requires token and row lacks it; token is not one of the four identity tokens | none |
| root-style helper probes | dispatch omission REFUSE; same-length different-path REFUSE; compatible second batch with current mint map ADMIT; handmade valid-helper still `1c5df32c…` | n/a |
| query / close_run of the occupancy helper itself / full launcher / native-cases corpus / LIVE D9 | **not** claimed | n/a |

---

## Proposed hashes

See `proposed-hashes.json`. 22 files (v2 21 + `dispatch-binding.schema.v1.json`). New vs provider58:

- `docs/coop/design-corrections/native/dispatch-binding.schema.v1.json` 4568 `868c3cf241af9ecc205ba7d078354e38a7db5132974120c046ac23a2dd1df938`
- `docs/coop/design-corrections/native/occupancy-companion.schema.v1.json` 6784 `f2cb0b725355ad1a800f8ed108d79e4e462e0cb35ca2d8116d95fe5c4ce96427`
- `docs/coop/design-corrections/native/fact-batch.schema.v3.json` 8547 `a963abd38fb2cf8a7b3b78a36469a7d166a4e315cd5f9c63cdbbff55c04c0de2`

Model sha256 `78eac275f4c638c515695dd511126fb7f742a2fcb372e56f1c1f06ba62ce41c8`.

Patch: `provider58-to-e2e.patch` against unchanged provider58 (proposed-file subset only).

29 model remains `780c1d2cbbff266ac9aeeff83fc4cf16766568a7f4a386f5981834c36d6fdffb`. Provider58 model remains `fb851602d1bdb73140d283e2b40f023f708db9c6cfb351ac2ec56646ae881ff2`.

---

## Remaining

LIVE D9; OS/compiler qualification; pin seal; whole-suite receipts; native-cases live CBOR FactBatch frames through `protocol3_run`; P7 closure-kind; frozen24; query python three-way merge by root. Peer3 independently reviews 29; later findings remain separate. This authoring is not acceptance.
