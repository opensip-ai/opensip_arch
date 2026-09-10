I'll verify the v3 source-manifest hash and every listed file, then review the corrected bytes against the five prior findings and the native stage/protocol law.Hashes match. I'll copy a disposable overlay and read the new schemas, bind model, and native §9.1/§9.4/§9.6.I'll write focused probes for stageId correlation, optional receipts, prior-record facts-map scope, and schema completeness, then run the 27/array/native checks.**Verdict: `CORRECTIONS_REQUIRED`.** Companion-on-`FactBatchV3` is the right *kind* of worker delivery. These bytes still do not give a complete published stage-correlation law, complete schemas without Python mutation, or prior-batch occupancy. **27/27 is not delivery.**

Manifest SHA256 `1054a15375c0d8de272c277fd937d2eb99d5b4582ef266bd15daf72289138af2` matches; all 1322 files and all 21 proposed hashes match. Output is only under `grok-provider-return-correction-peer.v3/output`. Pins were stale; the full launcher was not run and was not bypassed.

### What the 27 suite does not test
Owning TS `FactBatch.stageId` is **C-2 text**. `StageRequestV1`/`StageRequestV2.stageOrdinal` is **contiguous Analyze 0..n-1**. Analyze is a **provider subset** of Plan stages. Receipts use **Plan-wide** ordinals. §9.6 still says “unchanged Analyze” and `stages[k]` index equality, and types `FactBatchV3.stageId` as uint64.

Probe: Plan ordinal 0 = other producer, ordinal 2 = this producer. Analyze-contiguous `stageId=0` looks up the wrong Plan stage (`TARGET_ATTRIBUTION_PRODUCER_MISMATCH`). `stageId=2` admits. A worker that follows owning Analyze order cannot bind.

`stage_receipts` and `analyze_analysis_ordinal` are skip-if-None. Omit receipts → admit. Omit analysisOrdinal with batch `analysisOrdinal=9` → admit. Published invocation.inputs does not even list those fields.

Distinct prior-batch V2 (no conflict) refuses `TARGET_ATTRIBUTION_FACT_NOT_IN_PLAN` because atom `facts` is only the current mint map. The 27 prior-records case smuggles the prior fact into that map.

Published `FactBatchV3` `$defs.OccupancyCompanionV1` has **no allOf**; first-party + null `evaluationNativeId` admits. The model then **assigns** the full companion/V2 schemas onto `items` at import. A NEW blind reading only the JSON does not get that law. Return schema still says “After fact2 mint, emit one V2 record.”

### What does hold
Isolation *shape*: companion is written in-worker before emit. No `/tmp` fallback. CBOR hex is owner deterministic-CBOR. `origin=host-internal` refuses without capture. C15 retained. Enumerator ≠ stage-spec producer is allowed; required join is **stage-spec `producerClosure`**, not XI `enumerator.closureId`. Token `target-attribution-v2` is optional to spawn; Plan-required missing token does not spawn (owner `negotiate`).

Helper re-runs: **27/27** (`fullRun: false`, first failure none) and **116/116** array-order (first failure none). Those remain helper preconditions.

Four MUSTs (stage correlation, trusted-input set, prior-batch facts, schemas without mutation) plus selectors/consequences/remedies are in `provider-return-correction-peer.md` and `.json`.
