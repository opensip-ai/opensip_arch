# Blind review — consumer-b.v24, runtime consumer-b.v24-source44.v1 (source44 kit)

## Verdict: CHANGES_REQUIRED

One MUST issue remains open in the provider startup law.

**M-s44-1.** A clean pre-Analyze `Unavailable(native-context-mismatch)` must be converted by the host into one `CoverageResultV3` per requested key (native-evidence §9.7; `provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion`).
- **Fixed by the kit:** every member of those committed records except `closedWorld`.
- **`closedWorld`:** given only as `closed_world_v2(no manifest, entry points none, no edges, externalConsumers unknown)`, a function no kit owner publishes.
- **What I measured:** four `closedWorld` values are each lawful under every published constraint I can find. Each admits, and each mints a different `coverage2` identity for the same requested key, in both languages.

Two conforming hosts can therefore commit different evidence for the same terminal. Everything else I reconstructed on the source44 kit holds, as measured below.

This is my own independent reconstruction. It makes no product qualification claim and grants no implementation authorization. It is not root acceptance; root admission of my exports is a separate gate whose outcome I have not observed.

## Requirement standing

Measured by `tools/finalize_review.py` (`logs/s44-fin10.3`); every ID is listed in `blind-review.json#/requirementStatus` and `requirement-status.json`, with checkpoints `checkpoints/phase-0..11.json`.

- **Executed:** all 123 requirements and all 8 standing rules; 0 unexecuted, 0 failed.
- **Future qualification:** the 3 items are recorded as unperformed.
- **Claimed complete positives:** 27, each admitted, replayed from scratch and exported.

Every accept-blocking ID is executed, so the verdict is not caused by missing work. It follows from M-s44-1 alone: all other basis items hold (`blind-review.json#/verdictBasis`).

## Inputs and custody

- **Kit.** `subject/consumer-input-manifest.json` SHA-256 `a3a5fba87d944fdec8e28165f42ad13b0268b03d0493eddf77bc32b0833e348f`. Parent frozen subject `e873c8db7b50f8d4bc4c6b1754239fb200b11f4e5d0f23b1ceaa6ea17297a32b`.
  - All 107 members pass SHA-256 and length checks, with no unlisted file, at phase 0 and again at the end (`vectors/phase0-custody.json`, `runs/final-custody.json`).
- **Charter and requirements.** `charter.md` `b3fdeac4…` and `requirements.json` `c314d161…` are the source43 text with source44 paths and hashes: 123 requirements, 8 standing rules, 3 future-qualification items.
- **Delta against my own source43 custody rows** (`s44-kit-delta.json`):
  - added: `native/provider-handshake.schemas.v1.json`, `native/provider-startup.schemas.v1.json`, `native/typescript-protocol2-order.v1.json`;
  - changed: `native/fact-batch.schema.v3.json`, `native/occupancy-companion.schema.v1.json`, `native/protocol3-transitions.v1.json`, `foundation/provider-target-attribution-return.schema.v2.json`, `foundation/execution-inputs-contract.v1.md`, `native-evidence.md`.
- **Continuation.** Same origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514, from the exact source43.v1 output copy; independence is not claimed anew.
  - Code was rebound (`rebind-s44-manifest.json`: 104 files, 123 occurrences).
  - The source43 final bytes of every file I changed are at `preserved/s43-final/`, with a hash manifest of all 473 copied result files.
- **What I read.** Only this runtime's kit, charter and requirements, my own current and prior work, and the installed Python/jsonschema. No LIVE, other runtimes, author models, fixtures, reports or root results.

## What the new bytes affect

- **AST read-census** (`selfcheck/s44-provenance.json`):
  - The changed and added members are read only by the phase-3 provider reconstruction (`ref/factbatch.py`, `ref/protocol3.py`, and the new `ref/protocol_ts2.py` and `ref/provider_wire.py`).
  - Generic readers: the validation registry, the custody tools and the kit census.
  - No unchanged kit document references a changed `$id`.
- **Charter line 248 (unchanged).** Apply the negotiated payload selection, exact payload bytes and request/batch correlation to the existing provider traces. The new owners change which historical payload, which event machine and which startup payloads those traces carry.

## The unchanged source43 helpers on the source44 kit (preserved, `preserved/s44-original/`)

- **Payload vectors** (`logs/s44-original.0`):
  - All 71 still met their source43 expectations: they admitted a TypeScript FactBatchV2 and refused the lawful TypeScript FactBatchV1 member set.
  - The run exited 1 only on the HC-51 token census, which now finds two more sites.
- **Traces** (`logs/s44-original.1`): exit 0 with no failure. The traces ran TypeScript on the Rust table, carried Rust modes as frame booleans, and carried startup/coverage/terminal/cancel frames as names only.

My source43 R-TRACE-* standing is therefore superseded under the source44 owners. My source43 advisory A-s42v3-1 is withdrawn: the kit now publishes the TypeScript historical payload and the TypeScript Hello schemas.

## Corrections from the kit (tools/hc_source44.py)

- **HC-56 — runtime adaptation.** Rebind, preservation, and source44 custody expectations.
- **HC-57 — historical FactBatch per language.**
  - `typescript-semantic`: delivery.v2 FactBatchV1 (`TypeScriptFactBatchV1Vector`). `batchCommitment` is recomputed as `SHA-256(UTF8(opensip.ts-provider.fact-batch.v1) ‖ 0x00 ‖ deterministic-CBOR(wire facts))` over the wire FactCandidateV1 projection (`ref/wirecbor.py`).
  - `rust-semantic`: FactBatchV2 (`RustFactBatchV2Vector`).
- **HC-58 — machines and payloads.**
  - TypeScript exchanges run on `typescript-protocol2-order.v1.json`; Rust exchanges run on protocol3 with `dependencyMode`/`preparedMode` derived from the admitted OpenUniverseV3.
  - Before the table, `ref/provider_exchange.py` admits every Hello, HelloAck, OpenUniverse, UniverseAccepted, NativeContextVerified, Unavailable, Coverage/CoverageV3, BudgetExhausted, Cancelled and FactBatch payload.
  - Worker refusals route `PROVIDER.PROTOCOL_VIOLATION`; host-authored refusals route a host invariant.
  - After DONE, a clean pre-Analyze Unavailable is converted by the host.
  - Fixture payloads join my retained ts-pass/rust-mixed Run values (resolvedInputs, native context ids, snapshot2, CoverageResultV3). The native semantic-universe identity I recompute equals the retained Run frame key in both languages.
- **Own errors, preserved.**
  - `logs/s44-smoke.0`: a fixture label-uniqueness assertion.
  - `logs/s44-p3.1`: a control that presumed `native/source-pins.v2.json` is a subject member.
  - `logs/s44-cp.7`: the provenance census parsed `.md` members as JSON.
  - `logs/s44-diff.0`: the result-diff classifier reported edited helper sources as unexpected.

## Independent vectors and results (all executed, 0 assertion failures)

- **`traces/payload-vectors.json`** (`logs/s44-p3.0`): 78 vectors.
  - Groups: selection 20, bytes 9, correlation 23, companions 26; plus 29 decoder, 10 encoder, 8 exchange controls and 2 kit vector cross-checks.
  - TypeScript FactBatchV1 admits, and Rust FactBatchV2 admits. These refuse:
    - TypeScript FactBatchV2 (`cb24.FACT_BATCH_V1_SCHEMA`) and Rust FactBatchV1 (`cb24.FACT_BATCH_V2_SCHEMA`);
    - a placeholder commitment, a commitment over JSON vectors, and a commitment without its domain (`cb24.FACT_BATCH_V1_BATCH_COMMITMENT`).
  - JSON member order does not change the commitment.
  - The source42.v3 exact-byte, correlation and companion vectors all still pass.
- **`traces/startup-vectors.json`** (`logs/s44-p3b.0`, re-run `logs/s44-cp.0`): 116 vectors.
  - Groups: handshake 34, open-universe 20, universe-accepted 7, native-context-verified 6, unavailable 20, coverage 11, budget-exhausted 8, cancelled 10.
  - **Handshake:**
    - limits equal delivery.v2 (10) and rust v2 + §9.3 (32), with CBOR byte equality;
    - the pinned contract digest equals the raw SHA-256 of `rust-provider-protocol.v2.json`;
    - RFC 8785 descriptor digests; signed-row tokens in UTF-8 order; exact echoes.
  - **Startup:**
    - native universe identity and handshake joins;
    - RepositoryResolutionV3, with derived modes (true,false) and, for an imported-descriptor preparation, (true,true);
    - pre-/post-Analyze Unavailable partition and phase law;
    - Coverage key correspondence; terminal coverage;
    - the TypeScript Cancelled `snapshot` interval.
  - **Wire-CBOR controls:** bytewise and length-first map orders coincide for text keys.
- **Traces** (`logs/s44-p3.2`): 43 wire traces (24 TypeScript, 19 Rust), plus 5 labelled abstract table tests (`traces/abstract.json`).
  - All 23 TypeScript rows and all 34 Rust rows are exercised, and rows are pairwise disjoint. Only P3-09 and P3-10 are table-only, because they are unreachable from an admitted OpenUniverseV3.
  - 33 FactBatch payloads: 31 validated; admitted 21 V3, 2 V1, 1 V2; refused 7.
  - Conclusions that changed from source43:
    - a TypeScript Unavailable after stage output faults T2-23;
    - a TypeScript ProviderFault faults (no row);
    - a Rust exchange that skips dependency custody faults P3-34.
  - identityNegotiated precedes every source byte.
- **Fresh closure, replay and export on the source44 kit** (`logs/s44-fin.0-.5`):
  - all 27 claimed complete positives admit through owner admission, the independent retained-closure walk and complete proof replay with reachable-set equality;
  - the designed negative refuses; every positive exports and replays equal;
  - admission log: 0 failures; graph query: 66 vectors, 0 failures;
  - reference census re-walked; retention negatives: 32, all pass.
- **Result bytes against the source43 copy** (`selfcheck/s44-result-diffs.json`; second execution `logs/s44-det.*`):
  - 251 of 473 retained result files are byte-identical.
  - 89 differ only as process-id-bearing replay outputs, which also differ between two source44 executions.
  - 10 are the expected phase-3, census and custody changes; 4 are helper sources edited here.
  - All 27 run ids equal source43.

## Issues

### MUST

- **M-s44-1** — see the verdict.
  - **Selectors:**
    - `native-evidence.md` §9.7 lines 3234–3249 (line 3241);
    - `provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion`;
    - `native-evidence.md` §4.5 lines 2208–2242 and FR-3 lines 2768–2777;
    - `native-evidence.schemas.v2.json#/$defs/ClosedWorldV2`.
  - **Determined:** `entryPointsRecognized none`, `nonliteralLoading none`, `externalConsumers unknown`, `deadCodeRepairEligible false`. FR-3 supports `exportsClosed unknown`.
  - **Undetermined:** `dynamicDispatch` (resolved or not-applicable) and `reasons` (free strings).
  - **Measured** (`traces/startup-vectors.json#/conversion`): candidates A/B/C/D each admit in both languages, and every key has four distinct `coverage2` identities; the `exportsClosed closed` and `deadCodeRepairEligible true` controls refuse. The traces use reading A and label it.
  - **Required change:** publish the conversion's `closedWorld` value, or closed_world_v2's result for that input.

### SHOULD

None.

### Advisories

- **A-s44-1 (new).** The return law's `standing` (line 65), `boundary.compilerWorkerTransport` (line 67) and `missingAndIncomplete.missingToken` (line 117) say "historical FactBatchV2" for any token-absent worker.
  - Its own per-mode rows (lines 138, 149), native §9.1/§9.2/§9.6, fact-batch v3, occupancy companion and the handshake wire law are per language.
  - Advisory: the capture result the return law owns is language-independent.
- **A-s44-2 (new).** `native/source-pins.v2.json` is cited (wire law line 64; native lines 112, 4069) but is not a subject member. The Hello digest stays determined by the wire law.
- **Carried**, with their owners unchanged or their native line selectors re-located in the source44 bytes: A-c1, A-c2, A-c3, A-n1, A-n6, A-v2-1, A-v2-2, A-v2-3, A-s41-1, A-s41-2, A-s42-1, A-s42-2, A-s42-3, A-s43-1. Their exact selectors and measurements are in `blind-review.json#/advisories`.
- **Withdrawn:** A-s42v3-1.

## What required invention

- **Records and refusals.** Nothing required inventing a record or refusal outcome, except the conversion `closedWorld`. That value is not invented: it is reported as M-s44-1 with every lawful candidate measured.
- **Named readings:**
  - `cb24.*` internal keys (A-c1) and my own check order;
  - Rust `CancelledV2.observedPhase` not validated (no published worker phase vocabulary);
  - synthetic trusted descriptors, rust-v1 row and prepared-output set, a fixture Plan and placeholder coverage commitments, all within the kit's own §9.7 reference scope;
  - the carried readings listed in `notes/10-gaps.md`.

## Limitations

- **Provider law on constructed payloads only.** It is executed on constructed payloads, not on built Runs (which retain no provider frames) and not in a worker process.
- **Not executed:**
  - snapshot, dependency-source and prepared custody payloads (abstract events);
  - commitment recomputation;
  - descriptor signatures;
  - post-terminal `bind_worker_occupancy`.
- **Future qualification, unperformed:** real OS/compiler/crypto/SQLite measurement, provider execution as enforcement, host authentication and synthetic TCB enforcement.
- **Reused exact prior measurements, with custody:** phases 1–2 and 4–8 vectors, builds and stores, mutation replay, tamper, and the source42 pre/post matrix. No helper outside phase 3 reads a changed member, helper bytes are rebound-only, and stores are byte-identical (`selfcheck/s44-provenance.json`).

## From-scratch recompute

```text
cd /private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output
for s in tools/from_scratch.py tools/replay_export.py tools/phase9_admission_log.py \
         vectors/phase3_payload_vectors.py vectors/phase3_startup_vectors.py vectors/phase3_traces.py; do
  /tmp/opensip-architecture-review-env/bin/python -I -B $s || exit 1
done
```

- **Scripts.** Every execution goes through `tools/seq.py`, which retains its log under `logs/`. Custody is `vectors/phase0_custody.py` and `tools/final_custody.py`; checkpoints are `tools/checkpoint_p123.py`, `p456`, `p7`, `p8`, `p9`; provenance is `tools/provenance_s44.py`; finalization is `tools/finalize_review.py [--phase11]`.
- **Machine-readable outputs:** `traces/`, `vectors/`, `runs/`, `selfcheck/`, `checkpoints/phase-0..11.json`, `requirement-status.json`, `blind-review.json`.
- **Notes:** `notes/13-source44-provider-wire.md` (this delta), `notes/10-gaps.md` and `notes/00-session-standing.md`.
