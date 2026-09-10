# Provider-return end-to-end v2

**Standing.** Actual Grok DESIGN COAUTHOR. COMPLETE58 retained, not accepted. Cancelled33 incomplete, not acceptance. Provider58 `/tmp/opensip-design-corrections/target-provider-return-successor.v1` read-only and unedited. Wrong-directory cancelled33 tree preserved at `grok-target-provider-return-e2e-author.v1/output`. This turn writes only `/tmp/opensip-design-corrections/grok-provider-return-end-to-end-author.v2/output`. No pin seal, freeze, product implementation, commit, or full-suite claim.

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`.

---

## Peer five findings (source58-peer.md)

| # | Peer | Disposition |
|---|---|---|
| 1 | Helper 18/18 is not owning admission; checker not in suite | **Agree.** Owning entry is `bind_worker_occupancy`. Proposed `run-evaluator3-checks.py` adds 16th job `provider-attribution-return`. Still not `close_run`. |
| 2 | Post-mint wrapper table cannot cross one-shot FactBatch isolation | **Agree; wire correction.** Worker emits `OccupancyCompanionV1` on negotiated `FactBatchV3` before fact2 exists. COMPLETE58 envelope is not delivery. |
| 3 | Stage/producer joins are caller-echo; require enumerator | **Partial.** Bind now joins retained execution-plan `planId`, `stageSpecDigest`, stage-spec `planId`/`producerClosure`, receipts, selected views with required `planId`. **Reject** blanket identity of fact-producing provider with EnumerationPlan enumerator. XI: enumerator is cell/program binding; Analyze stage-spec producer is the fact producer of that stage. Test `test_enumerator_need_not_equal_fact_producer` admits when they differ. Closed stage row has no `producerClosure`; fallback removed. |
| 4 | Envelope records open header; host-internal captures | **Agree.** Records items are closed full V2 required set (`additionalProperties: false`). Companions use full OccupancyCompanionV1 (runtime items = companion schema including allOf). `origin=host-internal` and unbound envelope refuse without capture. |
| 5 | C15 guard holds | **Agree; retained.** |

---

## Required corrections

### 1. CBOR bytes

`FactCandidateV1.canonicalRelationPayload` is deterministic-CBOR. JSON-vector `canonicalRelationPayloadHex` transcribes **those same bytes**. `decodedRelationPayload` is a verified TCB observation. Admission requires `hex == fact-plane._deterministic_cbor(decoded).hex()`. Canonical JSON UTF-8 hex is refused (`test_cbor_hex_is_not_canonical_json_utf8`). Encoder is the owner `artifacts/check-fact-plane.py` `_deterministic_cbor`, loaded from overlay `coop/artifacts` (missing file fails; no provider58 path fallback).

### 2. stageId / Analyze correlation / array order

FactBatchV3 **preserves** `stageId` (historical V2 name). Worker echoes `AnalyzeV2.stages[k].stageOrdinal`, which the host set equal to `execution-plan.stages[k].ordinal`. Bind requires `batch.stageId == execution-plan.stages[k].ordinal` and `batch.analysisOrdinal == Analyze.analysisOrdinal`. No replacement ordinal field. Integers remain uint64 (`0..18446744073709551615`), not 1e6/65535.

Registered array order: `canonical.py` adds vocabulary `candidateOrdinal` (integer unique nondecreasing). `check-array-orders.py` includes the new native schemas and exercises that token. Arrays are not silently sorted.

### 3. Owner admission

Trusted observations: Hello tokens; Plan locator; execution-plan (`planId` + stages with `stageSpecDigest`); stage-spec map whose C-digest equals that digest; `hostCapture.stageReceipts`; Analyze `analysisOrdinal`; closures; selected views (`planId` required); mint map as TCB observation of already-admitted mint (this helper does **not** prove FACT-ID-V1); inventories; enumeration plan; `prior_records`.

Enforced: execution_plan.planId; stage-spec.planId; actual retained digest; receipt ordinal/digest/producerClosure; view planId + producer + fact membership; mint correspondence of relation/resolution/source+target universe/entire payload/confidence/anchor count. Fictional `stages[].producerClosure` is not read as authority.

### 4. No IMMUTABLE_FOUNDATION

Proposed model loads only `HERE` siblings and `HERE.parents[1]/artifacts/check-fact-plane.py`. Overlay copies owners then proposed files.

### 5. Closed records, priorRecords, capture order, 16th checker

Return `records.items` closed full V2 fields. Batch companions validated as full OccupancyCompanionV1. `prior_records` restored for same-Plan occupancy conflict across batches. Capture refs are canonical-set; projected records ordered by `sourceFactId` utf-8. Launcher job wired.

---

## Controls (not full Run, not LIVE D9, not compiler qualification)

Disposable overlay: `output/overlay` (copied owners + proposed).

| Check | Result | First failure |
|---|---|---|
| `check-provider-attribution-return.v2.py` | **27/27** | development: artifacts path `parents[2]` vs `parents[1]`; final none |
| `check-array-orders.py` | **116/116** failed `[]` | none |
| native `negotiate` + CapabilityToken enum | accepted with token; no-spawn if Plan requires token and row lacks it | none |
| query / close_run / full launcher / native-cases corpus | **not** claimed | n/a |

---

## Proposed hashes

See `proposed-hashes.json`. New:

- `docs/coop/design-corrections/native/occupancy-companion.schema.v1.json` 5627 `ecd86617210c0655b5f5fb3be32ec79e6a835cb8ea1a4d6aed2079e122ecb88b`
- `docs/coop/design-corrections/native/fact-batch.schema.v3.json` 7648 `f18d83beca9c74231beaf7c229dec03946e0c1822dcc421e41bba4bfda5d79e1`

Patch: `provider58-to-e2e.patch` against unchanged provider58.

---

## Remaining

LIVE D9; OS/compiler qualification; pin seal; whole-suite receipts; native-cases live CBOR FactBatch frames through `protocol3_run` (payload remains prose-owned beside 34 rows, with scoped bind checks); P7 closure-kind; frozen24; query python three-way merge by root.
