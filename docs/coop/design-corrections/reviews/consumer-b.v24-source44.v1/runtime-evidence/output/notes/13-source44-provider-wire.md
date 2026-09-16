# Source44: provider wire, startup and trace law (runtime source44.v1)

## Kit delta and what it affects

Against my own source43 custody rows (`s44-kit-delta.json`; manifest `a3a5fba8…`, parent `e873c8db…`, 107 members, 98 unchanged):

- **Added:**
  - `native/provider-handshake.schemas.v1.json`
  - `native/provider-startup.schemas.v1.json`
  - `native/typescript-protocol2-order.v1.json`
- **Changed:**
  - `native/fact-batch.schema.v3.json` (whenAbsent is now per language)
  - `native/occupancy-companion.schema.v1.json` (`historicalFactBatchV1`/`V2`)
  - `native/protocol3-transitions.v1.json` (derivedObservations, rowPayloads, host-derived modes)
  - `foundation/provider-target-attribution-return.schema.v2.json` (per-mode worker rows)
  - `foundation/execution-inputs-contract.v1.md` (per-language wording)
  - `native-evidence.md` (§0 rows 119–129; §9.1–9.4 expanded; new §9.7)

**Readers.** An AST read-census of my helpers (`selfcheck/s44-provenance.json#/memberReaders`) finds that only the phase-3 provider reconstruction reads these members.
- The validation registry and `tools/reference_census.py` load every kit document.
- No unchanged kit document references a changed `$id`.

**Charter scope.** Charter line 248 still applies the negotiated payload selection, exact payload bytes and request/batch correlation to the existing provider traces. The new owners change which payload, which machine and which startup payloads those traces carry.

## The unchanged source43 helpers on the source44 kit

`tools/run_preserved_s43.py` ran the preserved source43 scripts with their own helpers. Outputs are in `preserved/s44-original/`.

- **`logs/s44-original.0`** (payload vectors):
  - All 71 vectors matched their source43 expectations.
  - They still admitted a TypeScript FactBatchV2 and refused the lawful FactBatchV1 member set.
  - The script exited 1 only because the HC-51 `candidateOrdinal` census finds the two new historical vector sites.
- **`logs/s44-original.1`** (traces): exit 0, no failure. It detected none of the source44 changes (HC-58).

## Corrections (HC-57, HC-58)

- **Historical FactBatch (HC-57).**
  - When the token is absent, `typescript-semantic` admits delivery.v2 FactBatchV1 as `TypeScriptFactBatchV1Vector`.
    - `batchCommitment` is recomputed as `sha256(UTF8(opensip.ts-provider.fact-batch.v1) ‖ 0x00 ‖ deterministic-CBOR(wire facts))`.
    - The wire candidate is the vector with `decodedRelationPayload` removed and `canonicalRelationPayload` as a byte string (`ref/wirecbor.py`).
  - `rust-semantic` admits FactBatchV2 as `RustFactBatchV2Vector`.
- **Machines (HC-58).**
  - `typescript-semantic` exchanges run on the TypeScript protocol-2 table (`ref/protocol_ts2.py`; 23 rows).
  - `rust-semantic` exchanges run on protocol3 (34 rows).
    - `dependencyMode` and `preparedMode` come from the admitted OpenUniverseV3, so every admitted Rust exchange takes the dependency-source frames.
    - P3-09 and P3-10 are exercised only by labelled abstract table tests (`traces/abstract.json`).
- **Payload admission before the table** (`ref/provider_exchange.py`, `ref/provider_wire.py`):
  - **Hello/HelloAck:**
    - the published schemas; limits equal to delivery.v2 (TypeScript) or the 24+8 ProtocolLimitsV3 members with CBOR byte equality (Rust);
    - RFC 8785 descriptor digests and descriptor fields; the raw-byte contract digest; the rust-v1 identity row;
    - signed-row tokens and exact token/identityVersions echoes.
  - **OpenUniverse:** identity members and the native semantic-universe identity (equal to my retained Run frame keys); handshake joins; plan native-context membership; RepositoryResolutionV3 joins.
  - **UniverseAccepted:** exact echo. **NativeContextVerified:** join.
  - **Unavailable:** pre- versus post-Analyze classification, phase law, correlation, reason partition, affected stages and terminal coverage.
  - **Coverage wrappers:** requested-key correspondence.
  - **BudgetExhausted.**
  - **Cancelled:** the inserted TypeScript `snapshot` interval and the Cancel echo.
  - **Refusal routes:** worker refusals route `PROVIDER.PROTOCOL_VIOLATION`; host-authored refusals route a host invariant.
- **Host conversion.** After a clean pre-Analyze Unavailable reaches DONE, the host mints one CoverageResultV3 per requested key and admits it (schema, RC-1/RC-2/RC-6, cause registry, §4.5 ingredients). `stage_authority("unavailable")` admits as StageAuthorityV1.
- **Fixtures** (`vectors/payload_fixtures.py`):
  - resolvedInputs, native context ids, snapshot2 ids and CoverageResultV3 records come from my retained ts-pass and rust-mixed stores;
  - descriptors, the rust-v1 row, the prepared-output set and coverage commitments are synthetic host inputs (§9.7 reference scope).

## Measured (0 assertion failures)

- **`traces/payload-vectors.json`** (`logs/s44-p3.0`): 78 vectors.
  - Groups: selection 20, bytes 9, correlation 23, companions 26. Also 29 decoder and 10 encoder vectors.
  - TypeScript FactBatchV1 admits. These refuse:
    - TypeScript FactBatchV2 (`cb24.FACT_BATCH_V1_SCHEMA`);
    - Rust FactBatchV1 (`cb24.FACT_BATCH_V2_SCHEMA`);
    - a placeholder commitment, a commitment over JSON vectors, or one without the domain (`cb24.FACT_BATCH_V1_BATCH_COMMITMENT`).
  - JSON member order does not change the commitment.
- **`traces/startup-vectors.json`** (`logs/s44-p3b.0` and the `s44-cp.0` rerun): 116 vectors.
  - Groups: handshake 34, open-universe 20, universe-accepted 7, native-context-verified 6, unavailable 20, coverage 11, budget-exhausted 8, cancelled 10.
  - Wire-CBOR controls: the two inherited map orders coincide for text keys.
  - The conversion measurement is below.
- **Traces** (`logs/s44-p3.2`): 43 wire traces, 24 TypeScript and 19 Rust (complete 6, unavailable/budget 7, cancel 5, fault 21, terminal 4), plus 5 abstract tests.
  - Every row of both tables is exercised and rows are pairwise disjoint.
  - FactBatch payloads: 33 total, 31 validated. Admitted: 21 V3, 2 V1, 1 V2. Refused: 7.
  - Conclusions that changed from source43:
    - a TypeScript Unavailable after stage output is T2-23 FAULT (source43 reached DONE via P3-25);
    - a TypeScript ProviderFault is T2-23 FAULT (no row);
    - a Rust exchange that skips dependency custody faults P3-34.

## M-s44-1: the host-minted closedWorld is not determined

- **Law.** §9.7 (lines 3234–3249) and `provider-startup#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion` give closedWorld only as `closed_world_v2(no manifest, entry points none, no edges, externalConsumers unknown)`. A kit-wide search finds `closed_world_v2` only at those two places.
- **What §4.5 decides.** When `exportsClosed=closed` (every ingredient) and when `deadCodeRepairEligible` is true.
- **Determined by the text:** `entryPointsRecognized none`, `nonliteralLoading none`, `externalConsumers unknown`, `deadCodeRepairEligible false`.
- **exportsClosed.** FR-3 (line 2771, "closed-world is `unknown`") and §4.5 line 2226 support `unknown`, but no admission rule refuses `open`.
- **Not published anywhere for this input:** `dynamicDispatch` (`resolved` or `not-applicable`) and `reasons`, which are free strings; the backticked names in §4.5 are not a published vocabulary.
- **Measured.** Four candidates (A: unknown/not-applicable/[]; B: unknown/resolved/[]; C: open/not-applicable/[]; D: unknown/not-applicable/[provider-unavailable]):
  - each admits for both languages;
  - each mints a distinct `coverage2` identity for every requested key;
  - the `exportsClosed closed` and `deadCodeRepairEligible true` controls refuse.
- **Not decisive:**
  - the workflows five-field display sentinel (a display reduction; it also says `nonliteralLoading present`);
  - atom-evaluation's whole-record ranking.
- **What the traces do.** They use reading A and label it.
- **Required change.** Publish closed_world_v2's result for that input, or the minted closedWorld value itself.

## Advisories

- **A-s44-1.** The return law's `standing`, `boundary.compilerWorkerTransport` and `missingAndIncomplete.missingToken` (lines 65, 67, 117) still say "historical FactBatchV2" for any token-absent worker. Everything else is per language: its own per-mode worker rows (lines 138, 149), native §9.1/§9.2/§9.6, fact-batch v3 whenAbsent, and the handshake wire law.
  - **Why advisory.** The capture result the return law owns is language-independent, and payload selection has explicit per-language owners.
- **A-s44-2.** `native/source-pins.v2.json` is cited (wire law `expectedProtocolContractSha256.rule`; native line 112; line 4069) but is not a subject member.
  - **Why advisory.** The wire law states the digest, and it equals the raw SHA-256 of `rust-provider-protocol.v2.json`.
- **Withdrawn: A-s42v3-1.** The current owners publish the TypeScript historical payload and the TypeScript Hello schemas.

## Readings and limitations specific to source44

- **Not validated here:** Rust `CancelledV2.observedPhase`; no owner I can read publishes the worker phase vocabulary, and source44 leaves it unchanged.
- **Placeholders:** coverage/stream commitments are not recomputed (the kit's own §9.7 reference scope).
- **Fixture Plan:** `PLAN_ID` with the language's retained snapshot2 and native context digests. The prepared-mode trace reuses the retained non-prepared universe coordinates for Analyze, FactBatch and Coverage.
- **Own errors, preserved:**
  - `logs/s44-smoke.0`: a label-uniqueness assertion over every store label;
  - `logs/s44-p3.1`: a control that presumed the pin document is a subject member.

## Fresh versus reused

- **Executed fresh in source44:**
  - phase 3, and the unchanged source43 phase-3 scripts on the source44 kit;
  - from-scratch closure and complete replay of all 27 positives, export replay and admission log (`logs/s44-fin.0-.2`);
  - graph query, 66 vectors (`s44-fin.3`);
  - reference census (`s44-fin.4`) and retention negatives, 32, all pass (`s44-fin.5`);
  - custody, checkpoints, provenance, final custody, phases 10–11.
- **Reused as exact prior measurements, with custody:** phases 1–2 and 4–8 vectors, builds and stores, mutation replay, tamper, and the source42 pre/post matrix.

## Byte differences of re-executed results

- **Comparison.** Every file in `preserved/s43-final/results-manifest.json` (473) against its source43 hash (`selfcheck/s44-result-diffs.json`). 103 differ:
  - **89 carry a `"pid"` member** (the replay subprocess id). A second source44 execution of from-scratch, export replay and retention negatives (`logs/s44-det.0-.4`) changes the same 89 files again (`selfcheck/s44-determinism-after.json`).
  - **10 are expected content changes:** the 7 phase-3 trace files, the kit census, and the two custody reports.
  - **4 are helper sources** I edited in source44 that the manifest had hashed along with the results.
  - **251** files are byte-identical to source43, including `vectors/graph-query.json` and `vectors/retention-negatives.json`.
- **Result equality, independent of bytes.** All 27 claimed-positive run ids equal the preserved source43 review, and from-scratch agrees with every Run's retained replay result.
- **Own tool error, preserved.** `logs/s44-diff.0`: the classifier reported the 4 edited helper sources as unexpected.
