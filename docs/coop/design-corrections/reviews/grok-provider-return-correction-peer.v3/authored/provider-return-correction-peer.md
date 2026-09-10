# Provider-return e2e correction — coauthor peer (v3)

**Standing.** Same independent Grok coauthor peer as v2 COMPLETE23. Reviewing corrected NEW bytes in `grok-provider-return-correction-peer.v3/inputs/source`. Not fresh blind. Not final-whole acceptance. Not pin seal. Not product compiler. Not LIVE D9 discharge. Query/proof/closure are root-accepted elsewhere and not in this copy.

**Verdict: `CORRECTIONS_REQUIRED`.**

Worker `OccupancyCompanionV1` on negotiated `FactBatchV3` is the right *kind* of delivery (table no longer has to cross a closed FactBatch after mint). These bytes do not yet give a NEW blind a complete published law for stage correlation, schema completeness, or prior-batch occupancy. **27/27 is not delivery.**

Source-manifest SHA256 `1054a15375c0d8de272c277fd937d2eb99d5b4582ef266bd15daf72289138af2` matches. All 1322 listed files match. All 21 proposed hashes match. Provider58 was not edited here. Pins are stale; the full launcher was **not** run and was **not** pin-bypassed. Checks used a disposable overlay under this output directory.

---

## 1. Prior five findings (v2) vs these bytes

| # | v2 MUST | Disposition |
|---|---|---|
| 1 | 18 helper controls ≠ owning admission | **Partial.** Owning entry is now `bind_worker_occupancy`. Launcher lists a 16th job. Still `fullRun: false`. Independently re-run **27/27** with that standing. Not `close_run`. |
| 2 | Wrapper table cannot cross one-shot FactBatch | **Kind addressed; law incomplete.** Companion is a worker product on `FactBatchV3` associated by `candidateOrdinal` before fact2 exists. Isolation *shape* is right. StageId type/correlation is not (§2). |
| 3 | Stage/producer caller-echo; enumerator=producer | **Partial.** Bind joins execution-plan `stageSpecDigest` → stage-spec `producerClosure`, not `enumerator.closureId`. Probe `P-ENUMERATOR-DISTINCT` admits when they differ. Receipts / Analyze `analysisOrdinal` are skip-if-None. Analyze-subset stage correlation fails (§2). |
| 4 | Open records; host-internal captures | **Partial.** `origin=host-internal` refuses `PROVIDER_RETURN_HOST_AUTHORED` with no capture. Published envelope/batch schemas are still incomplete without Python mutation (§4). |
| 5 | C15 holds | **Retained.** `P-HOST-INTERNAL-AND-C15`. |

Required join for occupancy (exact, not blanket enumerator equality): **execution-plan stage row `stageSpecDigest` → retained stage-spec `producerClosure`** (fact-producing Analyze provider) **= minted fact `producerClosure` = selected view `producerClosure`**, and if receipts are supplied, **receipt `producerClosure`**. XI cell/program `enumerator.closureId` is a different owner and is not this join.

---

## 2. MUST — stageId / Analyze / retained execution ordinal

**Owners (not this helper’s single-stage fixture).**

- TypeScript `AnalyzeV1.StageRequestV1`: `stageId` = exact **C-2 text**; `stageOrdinal` = uint64 **contiguous 0..n-1 in Analyze order**. `FactBatchV1.stageId` = “current requested stage” (that text).
- TypeScript Analyze is a **provider subset** of Plan stages (`delivery.v2.json`: stageRequests = C-2 fact-derivation stages for `typescript-semantic` only).
- Rust `AnalyzeV2.StageRequestV2.stageOrdinal` = **contiguous Analyze order**; `planStage` = nested C-2 bytes. `FactBatchV2` still named `stageId`.
- Retained `StageReceiptV1.ordinal` / execution-plan `stages[].ordinal` are Plan-wide integers (receipt ordinal max 1023).
- Current §9.4 does **not** republish an Analyze payload; TS still inherits AnalyzeV1.stageRequests.

**What these bytes claim.** Native §9.6: “Stage correlation **(unchanged Analyze)**.” `AnalyzeV2.stages[k].stageOrdinal == execution-plan.stages[k].ordinal`, echoed as `FactBatch.stageId`. “No second ordinal field.” FactBatchV3 types `stageId` as uint64 and calls that a preserved historical name.

**What actually happens.**

1. Integer `stageId` is a **type change** from TS text C-2 `stageId`. §9.6 must not call that unchanged.
2. `stages[k]` **index** equality is not a law when Analyze is a subset of Plan stages.
3. Contiguous Analyze ordinal 0 is not Plan ordinal 0.

**Probe `P-ANALYZE-SUBSET-STAGEID` (not a 27 case).** Plan stages ordinal 0 = other provider, ordinal 2 = this producer. Worker echo of Analyze-contiguous `stageId=0` **refuses** `TARGET_ATTRIBUTION_PRODUCER_MISMATCH` (bind looked up Plan stage 0). `stageId=2` (Plan ordinal) admits. So a worker that obeys owning StageRequestV1/V2 contiguous order cannot bind this producer’s occupancy.

§9.6 also writes `producerClosure` from `batch.stageOrdinal` while the field remains `stageId`.

**Published invocation vs claimed complete entry.** Schema `x-opensip-return-law.invocation.inputs` does **not** list `stage_receipts` or `analyze_analysis_ordinal`. Function docstring lists them as trusted observations. Code: `if stage_receipts is not None` / `if analyze_analysis_ordinal is not None`. Probe `P-OPTIONAL-RECEIPT-ANALYSIS`: omit receipts → **admitted**; omit analysisOrdinal with batch `analysisOrdinal=9` → **admitted**; supply analysisOrdinal=0 vs batch 9 → `PROVIDER_RETURN_ANALYSIS_ORDINAL`. Skip-if-None is not complete-entry enforcement.

When receipts *are* passed, `_require_receipt` checks only `ordinal`, `stageSpecDigest`, `producerClosure`. Closed `StageReceiptV1` also requires `outputDomains`, `outputRefs`, `state`, `unavailableReason`.

**Remedy (minimal).** Publish one correlation law and implement it:

- Keep FactBatch `stageId` as the **owning wire identity** of the current requested stage (TS: C-2 text). Do not silently retarget the same name to Plan ordinal.
- Join Plan/receipt via nested `planStage` / `stageSpecDigest`, not `Analyze.stages[k]` vs `execution-plan.stages[k]`.
- If occupancy bind needs Plan ordinal, add a **named** field with an explicit copy rule from the retained execution-plan row for the requested C-2 stage — not “unchanged Analyze.”
- Either require `stage_receipts` and `analyze_analysis_ordinal` in the published input list and refuse omission, or stop calling this a complete owning entry for stage correlation.

---

## 3. MUST — prior_records vs current-batch facts map

`bind_worker_occupancy` projects companions from **this** batch, then `_admit_target_attributions` over `combined = prior_records + records` using `facts` built **only** from `minted_by_ordinal` (this batch).

**Probe `P-PRIOR-DISTINCT-ADMITTABLE`.** Prior V2 for `fact2:22…` (different first-party file, no occupancy conflict) with current mint only `{0: fact2:11…}` refuses `TARGET_ATTRIBUTION_FACT_NOT_IN_PLAN`. Author `test_prior_records_occupancy_conflict` only tests a **contradictory** prior while **smuggling** the prior fact into the current mint map (ordinal 1 is not even a candidate in that batch).

**Remedy.** Atom `facts` must include admitted descriptors for every `prior_records.sourceFactId` (Plan-retained facts), while `minted_by_ordinal` stays this-batch only for companion projection. Distinct prior-batch occupancy must remain admittable.

Candidate order: `x-opensip-order: candidateOrdinal` is unique nondecreasing integers in `canonical.py` (NEW blind can implement the token). Contiguous-within-stage across batches is **not** that token and is **not** enforced in bind (`P-CANDIDATEORDINAL-VOCAB`).

---

## 4. MUST — schemas complete outside Python mutation

At import, the model does:

```
RETURN_SCHEMA["properties"]["records"]["items"] = TARGET_SCHEMA
BATCH_SCHEMA["properties"]["occupancyCompanions"]["items"] = COMPANION_SCHEMA
```

Published `fact-batch.schema.v3.json` `$defs.OccupancyCompanionV1` has **no `allOf`**. Probe: first-party + `evaluationNativeId: null` **admits** under the published batch schema and **refuses** under `occupancy-companion.schema.v1.json`.

Published return `records.items` lists V2 field names with `additionalProperties: false` but **no `$ref`** to selected V2, no occupancy `allOf`, `logicalPath` is plain string. Leftover COMPLETE58 prose remains: producerSupply “After fact2 mint, emit one V2 record”; joins still mention `envelope.stageOrdinal`.

**Remedy.** `$ref` `occupancy-companion.schema.v1.json` (full allOf) as FactBatchV3 companion items. `$ref` `target-attribution.schema.v2.json` as return records items. Delete runtime mutation. Delete superseded COMPLETE58 producerSupply/joins or mark them historical-not-delivery so a NEW blind does not implement post-mint envelopes.

---

## 5. SHOULD — mint correspondence / receipt totality

`_mint_correspondence` compares relation, resolution, universes, **entire payload**, confidence, **anchor count**. Probe `P-MINT-ANCHORS-COUNT-ONLY`: same count, different path → **admitted**. If mint map is a TCB observation of already-admitted mint, compare anchors as values (or C-canonical), not length.

Receipts, when required, should join `outputDomains` to the stage row.

---

## 6. What holds (not 27-as-delivery)

- Companion-on-FactBatch isolation **shape**: worker writes occupancy before emit; host fills `planId` / `sourceFactId` / `producerClosure` after mint. No `/tmp` provider58 fallback (`P-NO-TMP-FALLBACK`). CBOR hex is owner `_deterministic_cbor`, not JSON UTF-8 (helper `test_cbor_hex_is_not_canonical_json_utf8`; 27 includes it).
- Token `target-attribution-v2` is in `CapabilityToken`. Owner `negotiate`: optional to spawn; Plan-required missing token → no spawn (`P-NATIVE-NEGOTIATE`). Not a live FactBatch through `protocol3_run` (author remaining; this peer agrees).
- host-internal / unbound envelope refuse without capture.
- C15 retained.
- Enumerator ≠ stage-spec producer is allowed; join is producer.
- Array-order **116/116** including `candidateOrdinal` token (helper). First failure: none on that suite.
- Provider-return helper **27/27**, `fullRun: false`. First failure: none on that suite. Development first failure (artifacts `parents[2]` vs `parents[1]`) is not present on this overlay (`parents[1]/artifacts`).

---

## 7. Helper vs owning (do not relabel)

| Check | Result | First failure | Class |
|---|---|---|---|
| `check-provider-attribution-return.v2.py` | 27/27 ok | none | Helper maps + bind. Not close_run. Single-stage Plan ordinal 0. |
| `check-array-orders.py` | 116/116 | none | Helper. |
| `native_evidence_model.negotiate` | accepted with/without token; no-spawn if Plan requires token and row lacks it | none | Owner native function. Not live CBOR FactBatch. |
| Independent probes | 13 ran; 7 author-claims fail | first real-boundary fail: published batch schema admits first-party null eval (`P-SCHEMA-PUBLISHED-INCOMPLETE`) | This peer’s owning-law tests. |
| Full `run-evaluator3-checks.py` | **not run** | pins stale | No pin bypass. |
| `protocol3_run` live FactBatchV3 | **not run** | author remaining | Payload still prose-owned beside 34 rows. |

---

## 8. MUST / SHOULD / advisory

### MUST

1. **Stage correlation law.** Selectors: native-evidence §9.6; `fact-batch.schema.v3.json` `stageId`; delivery TS `StageRequestV1`/`FactBatchV1.stageId`; rust `StageRequestV2.stageOrdinal`; `StageReceiptV1.ordinal`. Consequence: a subset Analyze cannot bind. Remedy: §2.
2. **Required vs optional trusted inputs.** Selectors: return schema `invocation.inputs`; `bind_worker_occupancy` defaults. Consequence: omit receipts / analysisOrdinal skips checks. Remedy: publish and enforce the same set.
3. **Prior-batch facts.** Selector: `bind_worker_occupancy` `facts` vs `prior_records`. Consequence: `TARGET_ATTRIBUTION_FACT_NOT_IN_PLAN` for a lawful distinct prior. Remedy: §3.
4. **Published schemas without mutation.** Selectors: `fact-batch.schema.v3.json` `$defs.OccupancyCompanionV1`; return `records.items`; model lines assigning `items`. Consequence: NEW blind implements a weaker companion than the Python helper. Remedy: §4.

### SHOULD

1. Compare mint anchors as values, not counts.
2. When receipts are required, join `outputDomains`/`state` to the stage row.

### Advisory

1. `candidateOrdinal` order token is documented; cross-batch contiguity is not this token.
2. 27/27 and 116/116 are helper preconditions.
3. LIVE D9 remains future. No new D9 codes observed on the public route helpers.

---

## 9. Limitations

- Did not read other active author copies, consumer outputs, private logs, web, or subagents. Previous own peer v2 history was used.
- Did not run the source-pinned full launcher (pins stale; no bypass).
- Did not run `protocol3_run` with a live FactBatchV3 CBOR frame.
- Did not re-run query/proof/closure (out of scope).
- Independent occupancy probes are design-reference maps except `negotiate`, which is the owner native function.
- Overlay is disposable check copy only.

No source mutation. No pin seal. No global passing claim.
