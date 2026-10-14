# S-M U-1: SM-4 coverage with build-script outputs absent

**Round 2.** Codex round 1 (`codex-sm-u1-r1`) found that PLAN-r3 claimed the static-profile and context series agree "within about 1%"; they differ by -0.507% to +7.774% (relative to context). PLAN-r3 now states the nine differences descriptively and rests D-5 on the command-data boundary alone. Nothing else changed; the round-1 PLAN-r3 and its script are under `s-m-report-plan/history/`.

This is an outside-product experiment, unit U-1 of the S-M report plan. It runs with the PLAN-r3 delta to D-5 (`docs/implementation/m3/s-m-report-plan/PLAN-r3.md`), which is submitted with this unit. Item 9 says no build script or proc-macro runs, and the expansion that depends on them is disclosed as unavailable (PROPOSAL-r6:558). U-1 analyses what can be analysed under that rule, preserves what cannot, and fills no SM-4 value.

## What blocked the build-script-only libraries

The block was not in an executor. The accepted static command-data producer spreads unavailability through every dependency edge. For axum, serde and serde_json, every blocker is a build-script unit, and Cargo's static `prepare_rustc` never reads build-script outputs; only `OUT_DIR` is set statically.

## The variants

None of these modifies an accepted piece.

### Producer variant (`producer-variant/`)

- **Clone.** A copy-on-write clone of the accepted producer, with exactly two files changed (the audit checks every other file).
- **`compiler/experimental_command_data.rs`.**
  - Unavailability does not spread through build-script units (custom-build targets and run-custom-build units); every other block is unchanged.
  - A unit constructed only because of this keeps Cargo's own `prepare_rustc` command, with `OUT_DIR` and `*_OUT_DIR` removed and recorded in `removedEnvironmentKeys`.
  - Its standing is `actual-static-cargo-command-data-build-script-outputs-absent`.
- **`util/context/experimental_command_data.rs`.** It only adds the control `command_data_build_script_only_consumer_constructed_with_outputs_absent`.
- **Controls.** All four `command_data_` controls pass (`run_bsabsent_controls_r1.py`, the accepted check recipe).
- **Image.** The variant test image is pinned in `variant-image.json`. It is 78 MB and is not staged; it is retained at its path, and the accepted image is unchanged.

### Collection and maps

- **Packets.** Fresh packets come from the accepted packet recipe, with only the destination changed.
- **Collection.** Collection over the nine entries succeeded. Each graph equals the accepted graph once the packet root is normalised.
- **Unchanged commands.** Every command the accepted producer constructed is unchanged, once packet roots and producer image paths are normalised.
- **New commands.** The new commands are exactly the units blocked only through build scripts (`collection/`, `u1-checks-r1.json`).
- **Maps.** Source maps were rebuilt with the accepted recipe for the new roots. File counts and bytes equal the accepted maps.

### Executor variants

- **Static-profile variant.** `cargo_lint_spelling_graph_execution_bsabsent.py` is the accepted static-profile executor, with build-script edges excluded from launch, blocking, externs and `-L`, and a per-unit `buildScriptOutputsAbsent` flag. Build-script units stay unavailable and never run.
- **Framed variant.** `framed_profile_graph_execution_bsabsent.py` applies the same change to the framed executor.

## Series (lead macOS, preliminary, not D12)

**Static-profile path (the SM-4 series under PLAN-r3 D-5).** `run_bsabsent_static_profile_series_r1.py` runs the closed static-profile driver (`c8cde6df…`) through the variant: 3 warmups and 7 measured runs per entry, lane held, priority 10. The audit checks:
- populations, read sets and metadata repeat across the ten runs;
- every unit the accepted series analysed is still analysed.

| Ord | Workload | New commands | Analysed units | Incomplete units | New first-party analysed | Whole-graph median ms | max ms | Accepted static-profile median ms |
|---|---|---:|---:|---:|---|---:|---:|---:|
| 0 | poly-medium-napi-rs | 36 | 97 | 5 | napi_derive_backend, napi_derive_backend, napi_sys | 15802.4 | 15872.9 | 8069.7 |
| 1 | rs-medium-aws-lambda-rust-runtime | 19 | 63 | 4 | — | 7716.0 | 7740.4 | 5349.7 |
| 2 | rs-medium-axum | 18 | 44 | 6 | — | 7065.9 | 7083.4 | 4061.6 |
| 3 | rs-medium-hyper | 0 | 7 | 0 | — | 744.8 | 753.8 | 738.5 |
| 4 | rs-medium-serde | 9 | 8 | 3 | — | 1440.2 | 1448.8 | 69.9 |
| 5 | rs-medium-serde-json | 3 | 3 | 2 | — | 635.0 | 639.7 | 140.1 |
| 6 | rs-medium-tokio | 11 | 27 | 0 | — | 2679.6 | 2682.7 | 1226.2 |
| 7 | mr-rs-medium-serde-json | 9 | 8 | 3 | — | 1445.0 | 1460.5 | 72.3 |
| 8 | mr-rs-medium-serde-json | 3 | 3 | 2 | — | 725.0 | 732.2 | 142.0 |

**Why first-party coverage barely moves.** Most newly launched first-party libraries end incomplete, as item 9 requires them to be preserved:
- **`serde_core`** stops at `include!(concat!(env!("OUT_DIR"), "/private.rs"))`. The file its build script generates is unavailable, so every dependant stays incomplete, including `axum`, `axum_extra`, `serde` and `serde_json`.
- **`serde_derive_internals`** reads `src/mod.rs` outside the prepared map. That source path is not in the pinned regular-file tree.

The new first-party analyses are napi's `napi_sys` and `napi_derive_backend`. Many dependency crates also become analysable (libc, mio, httparse and others), which raises whole-graph time.

**Metadata.** Metadata embeds each packet's registry root path (54 times in hyper's; the variant root is 9 bytes longer, matching the size difference). So byte equality with the accepted series is impossible by construction, and the control is population and repetition.

## Retained history

- **Framed-path run.** `run_bsabsent_framed_series_r1.py` and its records (in `large-records.tar.xz`) ran the framed executor variant first. Its whole graph is dominated by per-child map streaming (accepted napi 43,195.6 ms), which is why PLAN-r3 rejects it for SM-4.
- **Overlap during that run.** The lead's r79 status integration overlapped two of its napi **warmups**. Measured samples were unaffected, and none of it is used for SM-4.
- **First static-profile attempt.** It ran entry 0's ten graphs, then stopped because the plain driver reports no instrumented interval. Its runner copy and log are retained; the rerun treats that interval as absent.

## Standing

- **Execution.** No build script or proc-macro ran, and nothing was trimmed or rebounded.
- **Values.** No SM-4 value, F, T or outcome is recorded; the S-M report (U-6) takes these spans under D-5.
- **Gates.** L-G1 is open, and L is not in effect.
