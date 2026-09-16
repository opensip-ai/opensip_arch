I've finished ADJ-2 to ADJ-5 in a new work copy, along with the planning-reference and README fixes. The corrected native checker passes 477/477 (the wire43 baseline passed 428/428), and the 40 handshake cases still pass. Nothing was frozen, repinned in a global ledger or committed. I verified all inputs before starting; at the end frozen43, the wire43 handoff and the prior assessment runtime were all byte-identical.

## What changed

- **ADJ-2 (pre-Analyze `Unavailable`):**
  - **Payload:** a new closed `PreAnalyzeUnavailableV1` with execution, snapshot and plan correlation plus the expected and recomputed native context IDs. It carries no stage IDs or coverage.
  - **Where it is lawful:** only in the NativeContextVerified interval (TS row T2-10, Rust P3-21), and only with reason `native-context-mismatch`. That reason is refused after Analyze.
  - **After it:** a clean exit still requires zero-exit then EOF. Any later frame or process fault is a fault, with no facts, coverage or Run.
  - **Host conversion:** it stays a clean `COVERAGE.PROVIDER_UNAVAILABLE` terminal. The host mints unknown coverage for its own planned stages through the existing coverage owners (`admit_coverage_result_v3`, `run_termination`). No join had to be fixed.
  - **TypeScript order:** the TS ordering and supervision overrides are published, including a new 23-row TypeScript major-2 order table.
- **ADJ-3 (OpenUniverse / UniverseAccepted):**
  - **Member names and IDs:** inherited names are kept; `snapshotId` and `planId` now carry `snapshot2` and `plan2` text.
  - **TypeScript:** `universeKey` is the native universe identity, the universe must match the admitted HelloAck, and there is no `repositoryResolution`.
  - **Rust:** `repositoryResolution` is `RepositoryResolutionV3`, joined to the universe and the selected preparation; UniverseAccepted is a full recursive echo.
  - **Mode flags:** `dependencyMode` and `preparedMode` are host-derived from the admitted payload, not wire booleans. `dependencyMode` is always true, because an empty dependency set still goes through manifest, seal and accepted; I checked this against the existing empty-set custody laws and found no contradiction. As a result, P3-09 and P3-10 can no longer be reached from a real OpenUniverse; they remain only as abstract table rows.
- **ADJ-4 (Coverage frame versus entry):** Rust's frame is `CoverageV3`, with a new §0 supersession row. TypeScript keeps the frame name `Coverage`. In both, the inherited wrapper carries `CoverageResultV3` entries matched to the requested keys by position. Commitment recipes are unchanged, and terminal coverage arrays are in stage-then-key order.
- **ADJ-5 (cancellation):** `observedPhase` is `snapshot` for a Cancel received in the new interval. There is no new enum value or terminal route.
- **Planning and README:** the shared-HelloV3 wording now names the per-language handshakes.
  - Chapter 14 was regenerated with `python docs/operations/check_repository_file_inventory.py --write`, not hand-edited.
  - The build-plan prose now names the per-language handshakes too.
  - The v9/v10/v11 input layers and the historical architecture docs are unchanged.
  - The stale README and contract §12 counts are now count-free.
- **rustCommitHash:** no owner requires the 64-hex release/handshake value to equal the 40-hex native-context compiler commit. They have distinct meanings, so nothing changed. If an owner ever joins them, it will have to state a representation mapping.

## Controls

| Control | Result |
|---|---|
| Native checker, corrected (also re-run after mutation restores) | 477/477 |
| Native checker, wire43 baseline | 428/428 |
| Foundation identity checker, before and after | 1596 passed, 0 failed, both |
| Attribution checker | 47/47 |
| Execution-inputs checker | no mismatches |
| Inventory generator `--check` | passes |
| Startup mutation controls | 9 of 9 applied and detected |
| Refusal audit | all 49 new cases (11 positive, 38 negative) refused or faulted for their stated reason |
| Three-state discriminator | frozen43 and wire43 refuse or leave undetermined each selected behaviour; the final state admits or refuses it as designed |

Kept as receipts rather than erased:
- The first authored Rust reason set wrongly included the TypeScript-only `node-modules-outside-read-set`; corrected in receipt 11.
- The first case pre-check failed 30 cases because the exchange didn't catch refusals from the separately loaded wire and startup modules; fixed, then 96/96.
- Two planning-check runs omitted the required `--source` argument.

## Still open

- **R-1:** `ClosedWorldV2` has no "not examined" value, so host-minted entries use non-authorizing derived values. This is advisory.
- **R-2:** other `UnavailableReasonV3` reasons remain post-Analyze only, as you scoped it.
- **R-3:** the implementation-planning check stops at `Planning source changed: native-evidence`, identically for wire43 and the final copy. It needs your new planning layer, and I couldn't check anything past that point.
- **R-4:** D9 reduction for user cancellation after a malformed `Cancelled` is not modelled.
- **R-5 and R-6:** coverage commitments are not recomputed, and Rust `CancelledV2` was not exercised.

## For your integration

Repin these current ledgers:
- the native, security, workflows, foundation and evaluator3 source pins (native also needs the new consumed-source entries in receipt 22);
- `implementation-coverage.v1.json` and `implementation-planning-sources.v1.json`.

Do not repin v9/v10/v11 or anything under `reviews/**`. Regenerate the native report after repinning.

Everything is in `/private/tmp/opensip-design-corrections/claude-provider-startup43-correction.v1/`:
- `review.md`
- `review.json`
- `delta/cumulative-vs-frozen43/` (20 files, including the repin index)
- `delta/incremental-vs-wire43/` (12 files, with wire43 parent and current hashes)
- `hash-index.json`
- `receipts/`
