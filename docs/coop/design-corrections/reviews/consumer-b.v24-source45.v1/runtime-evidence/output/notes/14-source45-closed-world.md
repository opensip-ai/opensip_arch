# Source45: published host-conversion closedWorld, per-language return law, and source44 arithmetic (runtime source45.v1)

## Kit delta and what it affects

Against my own source44 custody rows (`s45-kit-delta.json`; manifest `70771536…`, parent `8b4efbb0…`, 107 members, 104 unchanged, none added or removed):

| Member | Bytes | Change I located |
|---|---|---|
| `docs/v2/contracts/product-v1/native-evidence.md` | 328234 → 329013 | §9.7 host conversion: the `closedWorld` bullet now gives one complete JSON value (lines 3241–3261) and names its machine-readable owner. Headings before §9.7 keep their lines; every later heading moved by +19. |
| `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` | 32941 → 33341 | `x-opensip-startup-law/preAnalyzeUnavailable/hostConversion` (line 58) now references `hostConversionClosedWorld` (new object, lines 59–69). `$defs` moved by +11 lines. |
| `docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json` | 19507 → 19872 | `x-opensip-return-law` `standing` (65), `boundary.compilerWorkerTransport` (67) and `missingAndIncomplete.missingToken` (117) now name the historical payload per language. |

**How the changes were located.** My custody holds member hashes, not the bytes of earlier kits. The changes were therefore located by content and section structure, and every selector my helpers and issues cite was re-read in the source45 bytes. A same-length wording change that no helper reads and no issue cites would not have been located.

**Readers** (AST census, `selfcheck/s45-provenance.json`):
- return schema: `ref/factbatch.py`;
- startup schema: `ref/provider_wire.py`, `vectors/phase3_startup_vectors.py`;
- native-evidence.md: `ref/provider_wire.py`.

No non-phase-3 helper reads a changed member, and no unchanged kit document references a changed `$id`.

## M-s44-1 reassessed: resolved

The published value, identical in both owners:

```json
{"exportsClosed": "unknown", "entryPointsRecognized": "none", "nonliteralLoading": "none", "externalConsumers": "unknown",
 "dynamicDispatch": "not-applicable", "reasons": ["no-manifest"], "deadCodeRepairEligible": false}
```

- **Consistency with my source44 reading.** It keeps every member my source44 reading found determined, and fixes the two members nothing published (`dynamicDispatch`, `reasons`). It also resolves `exportsClosed` to `unknown`, the reading FR-3 supported.
- **Source44 candidates.** It equals none of my four source44 candidates. Reading A, which my source44 traces used, differs only in `reasons` (`[]`).
- **Measured** (`traces/startup-vectors.json#/conversion`, `logs/s45-p3.1`):
  - the §9.7 JSON block equals `hostConversionClosedWorld`, and the value admits as ClosedWorldV2;
  - the published conversion admits every minted entry (CoverageResultV3 schema, RC-1/RC-2/RC-6, cause registry, §4.5 ingredient rules): 4 entries for TypeScript, 2 for Rust;
  - `stage_authority("unavailable")` admits StageAuthorityV1;
  - two mintings give identical `coverage2` identities;
  - each source44 candidate refuses `cb24.CONVERSION_CLOSED_WORLD_NOT_PUBLISHED` on every entry and nothing else;
  - the `exportsClosed closed` and `deadCodeRepairEligible true` controls also refuse on the §4.5 ingredient keys.
- **Traces.** Both unavailable-before-analyze traces now mint and check the published value (`logs/s45-p3.2`).

## A-s44-1 reassessed: resolved

The three return-law sentences now name delivery.v2 FactBatchV1 for `typescript-semantic` and rust-provider-protocol.v2 FactBatchV2 for `rust-semantic`. These agree with the per-mode rows, native §9.1/§9.2/§9.6, fact-batch v3 and the handshake wire law.
- **Residue.** Line 117 reads "Historical the historical per-language payload"; this is editorial and does not change the rule (A-s45-1).
- **Unaffected reads.** No key, route or join my helpers read changed. The key-binding selectors (`invocation/inputs/dispatch`, `invocation/inputs/batch`, `x-opensip-new-internal-faults`) are present. The payload vectors re-execute with 78 vectors and 0 failures (`logs/s45-p3.0`).

## The unchanged source44 phase-3 helpers on the source45 kit

`tools/run_unchanged_s44.py` first checked that every imported helper equals `preserved/s44-final` with the runtime root mapped back, then redirected writes to `preserved/s45-original/`:
- `logs/s45-original.0`: payload vectors 78 matched, exit 0.
- `logs/s45-original.1`: startup vectors 116 matched, exit 0; they still reported the M-s44-1 determinacy gap as measured.
- `logs/s45-original.2`: traces exit 0; they still minted the conversion with reading A.

None of these failed, so none detected the source45 law. Correction HC-60: `ref/provider_wire.py` reads both owners and refuses any other conversion `closedWorld`; `vectors/phase3_startup_vectors.py` and `vectors/phase3_traces.py` were updated.

## Fresh versus reused

- **Executed fresh in source45:**
  - phase 3 (`logs/s45-p3.0-.2`);
  - from-scratch closure and complete replay of all 27 claimed positives, all ADMIT, with the designed negative refusing (`logs/s45-fin.0`);
  - export replay, all equal (`.1`); admission log, 0 failures (`.2`); graph query, 66 vectors, 0 failures (`.3`);
  - reference census (`.4`); retention negatives, 32, all pass (`.5`);
  - custody, checkpoints 0–9, provenance, result diffs, final custody (`logs/s45-cp.*`, `logs/s45-fin10.*`), and phase 11.
- **Reused as exact prior measurements, with custody:**
  - phases 1–2 and 4–8 vectors, builds and stores (104 stores byte-identical), mutation replay, tamper, the source42 pre/post matrix;
  - the source44 two-execution determinism probe.
- **Result bytes against the exact source44 copy** (`selfcheck/s45-result-diffs.json`, all 546 hashed files): 446 identical and 100 differing:
  - **89** process-id-bearing replay outputs;
  - **4** expected content changes: `traces/startup-vectors.json`, `traces/unavailable.json`, `vectors/phase0-custody.json`, `runs/final-custody.json`;
  - **4** rebound-only helper sources (runtime path): `vectors/payload_fixtures.py`, `phase1_canonical.py`, `phase2_capmanifest.py`, `phase3_payload_vectors.py`;
  - **3** helper sources edited here: `vectors/phase0_custody.py`, `phase3_startup_vectors.py`, `phase3_traces.py`.

  Every other trace file, `vectors/reference-census.json`, `vectors/retention-negatives.json` and `vectors/graph-query.json` are byte-identical to source44. All 27 run ids equal the source44 review.
- **Own tool error, preserved.** `logs/s45-cp.7`: the classifier tested helper sources against the edited/new status before the root mapping.

## Source44 arithmetic reconciliation (internal reporting consistency)

Derived from my retained source44 files (`selfcheck/s45-s44-arithmetic-reconciliation.json`, every check true):
- **Full comparison** (`preserved/s43-final/results-manifest.json`): 473 files, 370 identical and 103 differing (89 process-id-bearing, 10 expected content, 4 helper sources edited in source44). The current copied bytes give the same 370/103.
- **Determinism-probe subset** (runs/, negatives/, vectors/ non-store): 347 files, 251 identical and 96 differing (89 differed between two source44 executions; 7 stable but different from source43). The other 7 differing files are the phase-3 traces outside that subset.
- **Source44 prose error.** `blind-review.md` said "251 of 473 retained result files are byte-identical", and `notes/13` said "251 files are byte-identical". Both paired the subset's identical count with the full manifest size. The source44 bytes are preserved unchanged at `preserved/s44-final/`; the current `notes/13` carries an appended correction.
