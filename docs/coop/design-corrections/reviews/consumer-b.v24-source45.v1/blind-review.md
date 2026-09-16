# Blind review — consumer-b.v24, runtime consumer-b.v24-source45.v1 (source45 kit)

## Verdict: ACCEPT-RECONSTRUCTABLE

- **Source44 finding resolved.** My source44 review returned CHANGES_REQUIRED for one reason (M-s44-1): the host conversion after a clean pre-Analyze `Unavailable` committed a `closedWorld` value that no kit owner published. The source45 kit publishes that value exactly. It appears in native-evidence §9.7 and in `provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversionClosedWorld`, and the two owners agree.
- **Correction applied and measured.** My corrected helper applies the value. Admitted entries mint stable `coverage2` identities in both languages, and every value I previously considered lawful now refuses.
- **Advisory A-s44-1 resolved.** The return law now names the historical payload per language.
- **Charter conditions.** Every charter condition for acceptance holds on measured evidence:
  - all 123 requirements and 8 standing rules are executed, none failed;
  - all 27 claimed complete positives are exported, schema/registry/closure admitted, and replayed from scratch with complete proof comparison;
  - every helper failure is corrected from the kit with its original preserved;
  - no MUST or SHOULD issue remains.

**Scope of this recommendation.** It is my own internal recommendation from independent reconstruction. It makes no product qualification claim, grants no implementation authorization, and is not root acceptance: root admission of the exact exports is a separate gate whose result I have not observed.

## Requirement standing

Measured by `tools/finalize_review.py` (`logs/s45-fin10.3`); every ID is in `blind-review.json#/requirementStatus` and `requirement-status.json`, with checkpoints `checkpoints/phase-0..11.json`.
- **Executed:** 123 requirements and 8 standing rules; 0 unexecuted, 0 failed.
- **Future qualification:** 3 items, recorded as unperformed and not demanded.
- **Claimed complete positives:** 27.
- **Verdict basis** (`blind-review.json#/verdictBasis`): every item true.

## Inputs and custody

- **Kit.** `subject/consumer-input-manifest.json` SHA-256 `707715363ac6249e22a4eb30a628ac61f6e951d2d8de71cc8641cfdeb7a6ee69`. Parent frozen subject `8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155`.
  - All 107 members pass SHA-256 and length checks, with no unlisted file, at phase 0 and at the end (`vectors/phase0-custody.json`, `runs/final-custody.json`).
- **Charter and requirements.** `charter.md` `cf211b89…` and `requirements.json` `947054b7…`: the same 123/8/3 IDs and incorporated owners, with source45 paths and hashes.
- **Delta against my own source44 custody rows** (`s45-kit-delta.json`). Three members changed; none added or removed:
  - `native-evidence.md`: §9.7 host conversion `closedWorld`;
  - `native/provider-startup.schemas.v1.json`: `hostConversionClosedWorld`;
  - `foundation/provider-target-attribution-return.schema.v2.json`: per-language historical payload wording.
- **Continuation.** Same origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514, from the exact source44.v1 output copy; independence is not claimed anew.
  - The exact source44 final bytes (138 files, including its review) and hashes of all 546 result files were preserved at `preserved/s44-final/` before anything changed.
  - Code was then rebound (`rebind-s45-manifest.json`: 113 files, 132 occurrences).
- **What I read.** Only this runtime's kit, charter and requirements, my own current and prior work, and installed Python/jsonschema.

## Reassessment of my source44 issues

- **M-s44-1 — resolved by the source45 bytes.**
  - **Published value:** `{exportsClosed: unknown, entryPointsRecognized: none, nonliteralLoading: none, externalConsumers: unknown, dynamicDispatch: not-applicable, reasons: ["no-manifest"], deadCodeRepairEligible: false}`.
  - **Selectors:** native-evidence.md §9.7 lines 3241–3261; `provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion` (line 58) and `hostConversionClosedWorld` (lines 59–69).
  - **Relation to my candidates:** it keeps every member my source44 reading found determined and fixes the two that were open. It equals none of my four source44 candidates; reading A, which my source44 traces used, differed only in `reasons: []`.
  - **Measured** (`traces/startup-vectors.json#/conversion`):
    - the owners agree, and the value admits as ClosedWorldV2;
    - the conversion admits all entries (TypeScript 4, Rust 2) with StageAuthorityV1 unavailable;
    - two mintings give identical `coverage2` identities;
    - each source44 candidate refuses `cb24.CONVERSION_CLOSED_WORLD_NOT_PUBLISHED` on every entry.
- **A-s44-1 — resolved by the source45 bytes.** Return law lines 65, 67 and 117 now name delivery.v2 FactBatchV1 for `typescript-semantic` and rust-provider-protocol.v2 FactBatchV2 for `rust-semantic`.
  - **Residue:** line 117 has the editorial duplication "Historical the historical", reported as advisory A-s45-1.
  - **Measured:** the payload vectors re-execute on the new bytes (78, 0 failures).
- **A-s44-2 — carried.** `native/source-pins.v2.json` is still cited but still absent from the subject.

## Source44 result-comparison arithmetic (reconciled)

My source44 report said "251 of 473 retained result files are byte-identical", while `selfcheck/s44-result-diffs.json` reported 103 differing files (89 + 10 + 4). Derived from my retained source44 files (`selfcheck/s45-s44-arithmetic-reconciliation.json`, all checks true):
- **Full 473-file comparison:** 370 identical and 103 differing (89 process-id-bearing, 10 expected content, 4 helper sources edited in source44). Re-hashing the current copied bytes gives the same 370/103.
- **347-file determinism subset** (runs/, negatives/, vectors/ non-store files): 251 identical and 96 differing (89 differed between two source44 executions; 7 stable but different from source43). The remaining 7 differing files are the phase-3 traces outside that subset.
- **The error:** my source44 prose paired the subset's identical count with the full manifest size. The source44 report is preserved unchanged at `preserved/s44-final/blind-review.md`, and this is recorded as a disposition of my own reporting error.

## What the new bytes affect, and what was executed

- **Affected construction.** AST read-census (`selfcheck/s45-provenance.json`):
  - the changed members are read only by `ref/factbatch.py`, `ref/provider_wire.py` and `vectors/phase3_startup_vectors.py`, all phase 3;
  - no non-phase-3 helper reads them, and no unchanged kit document references a changed `$id`;
  - all 104 stores are byte-identical to source44.
- **Unchanged source44 helpers first** (`preserved/s45-original/`, `logs/s45-original.0-.2`). After an equality check against the preserved source44 bytes with the root mapped back, the phase-3 scripts passed all their own checks on the source45 kit. They still reported the determinacy gap and still minted reading A, so they did not detect the new law.
- **Correction HC-60** (`tools/hc_source45.py`): the published value from both owners, no caller-chosen `closedWorld`, and refusal of any other value. HC-59 is the runtime adaptation.
- **Phase 3, executed fresh** (`logs/s45-p3.0-.2`, 0 assertion failures):
  - **`traces/payload-vectors.json`:** 78 vectors (selection 20, bytes 9, correlation 23, companions 26); 29 decoder, 10 encoder and 8 exchange controls.
  - **`traces/startup-vectors.json`:** 116 vectors (handshake 34, open-universe 20, universe-accepted 7, native-context-verified 6, unavailable 20, coverage 11, budget-exhausted 8, cancelled 10), plus wire-CBOR controls and the conversion measurement above.
  - **Traces:** 43 wire traces (24 TypeScript on `typescript-protocol2-order.v1.json`, 19 Rust on protocol3) and 5 abstract table tests. All 23 TypeScript and 34 Rust rows are exercised, and rows are disjoint; only P3-09 and P3-10 are table-only. 33 FactBatch payloads: 21 V3, 2 V1 and 1 V2 admitted, 7 refused, 2 not validated before a pre-match fault. identityNegotiated precedes every source byte.
- **Closure, replay and export, executed fresh on the source45 kit** (`logs/s45-fin.0-.5`):
  - all 27 claimed complete positives admit through owner admission, the independent retained-closure walk and complete proof replay with reachable-set equality;
  - the designed negative refuses; all 27 export and replay equal;
  - admission log: 0 failures; graph query: 66 vectors, 0 failures; reference census re-walked; retention negatives: 32, all pass.
- **Result bytes against the exact source44 copy** (`selfcheck/s45-result-diffs.json`, 546 files): 446 identical and 100 differing:
  - 89 process-id-bearing replay outputs;
  - 4 expected content: `traces/startup-vectors.json`, `traces/unavailable.json`, `vectors/phase0-custody.json`, `runs/final-custody.json`;
  - 4 rebound-only helper sources;
  - 3 helper sources edited here.

  All 27 run ids equal source44, and from-scratch agrees with every retained replay result.
- **Reused as exact prior measurements, with custody:** phases 1–2 and 4–8 vectors, builds and stores, mutation replay, tamper, the source42 pre/post matrix, and the source44 two-execution determinism probe.

## Own errors, preserved

- `logs/s45-cp.7`: the result-diff classifier checked helper sources before the root mapping.
- All earlier own errors stay in their logs and `tools/hc_source4*.py`.

## Issues

### MUST

None. Every acceptBlocking item is executed. The only earlier MUST (M-s44-1) is resolved by published law and measured. Re-reading every selector my helpers and issues cite in the three changed members found no new missing, ambiguous or contradictory required law (`notes/10-gaps.md`).

### SHOULD

None.

### Advisories

- **A-s45-1 (new, editorial).** `provider-target-attribution-return.schema.v2.json#/x-opensip-return-law/missingAndIncomplete/missingToken` (line 117) begins "Historical the historical per-language payload". The rule it states is unchanged.
- **A-s44-2 (carried).** `native/source-pins.v2.json` is cited (wire law line 64; native lines 112 and 4088) but is not a subject member; the Hello digest stays determined by the wire law.
- **Carried**, with owners unchanged or native selectors re-located in the source45 bytes: A-c1, A-c2 (now native lines 3584–3619), A-c3, A-n1, A-n6, A-v2-1, A-v2-2, A-v2-3, A-s41-1, A-s41-2, A-s42-1, A-s42-2, A-s42-3, A-s43-1. Exact selectors and measurements are in `blind-review.json#/advisories`.
- **Resolved:** M-s44-1, A-s44-1. **Withdrawn earlier:** A-s42v3-1.

## What required invention

Nothing required inventing a record, identity or refusal outcome. Named readings remain:
- `cb24.*` internal keys (A-c1) and my own check order;
- Rust `CancelledV2.observedPhase` not validated (no published worker phase vocabulary);
- synthetic trusted descriptors, rust-v1 row and prepared-output set, a fixture Plan and placeholder coverage commitments, all within the kit's own §9.7 reference scope;
- the carried readings in `notes/10-gaps.md`.

## Limitations

- **Provider law on constructed payloads only.** It is executed on constructed payloads, not on built Runs (which retain no provider frames) and not in a worker process.
- **Not executed:**
  - snapshot, dependency-source and prepared custody payloads (abstract events);
  - commitment recomputation;
  - descriptor signatures;
  - post-terminal `bind_worker_occupancy`.
- **Kit-delta localization** is by content and section structure, because my custody keeps hashes rather than earlier kit bytes. A same-length wording change that no helper reads and no issue cites would not have been located.
- **Future qualification, unperformed:** real OS/compiler/crypto/SQLite measurement, provider execution as enforcement, host authentication and synthetic TCB enforcement.

## From-scratch recompute

```text
cd /private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output
for s in tools/from_scratch.py tools/replay_export.py tools/phase9_admission_log.py \
         vectors/phase3_payload_vectors.py vectors/phase3_startup_vectors.py vectors/phase3_traces.py; do
  /tmp/opensip-architecture-review-env/bin/python -I -B $s || exit 1
done
```

- **Scripts.** Every execution goes through `tools/seq.py`, which retains its log under `logs/`. Custody is `vectors/phase0_custody.py` and `tools/final_custody.py`; checkpoints are `tools/checkpoint_p123.py`, `p456`, `p7`, `p8`, `p9`; provenance and result diffs are `tools/provenance_s45.py` and `tools/result_diffs_s45.py`; finalization is `tools/finalize_review.py [--phase11]`.
- **Machine-readable outputs:** `traces/`, `vectors/`, `runs/`, `selfcheck/`, `checkpoints/`, `requirement-status.json`, `blind-review.json`.
- **Notes:** `notes/14-source45-closed-world.md`, `notes/10-gaps.md`, `notes/00-session-standing.md`.
