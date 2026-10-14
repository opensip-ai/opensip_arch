# S-M cold-reset series for the Rust-row components (U-5b)

This is an outside-product measurement, unit U-5b of the accepted S-M report plan r3 (`docs/implementation/m3/s-m-report-plan/PLAN-r3.md`, D-7 and U-5). It applies Q0 §9.2's **cold** reset (`harness/DESIGN.md:798-801`) to every F and T component of the eight Rust rows (item 9: F = SM-3 + SM-5 + SM-7 + SM-9; T = F + SM-4):
- **SM-3:** Rust start.
- **SM-5:** two parts in one span (the U-2c r2 runner).
- **SM-7:** with every NE §9.2 dependency field (the U-2c r3 runner).
- **SM-9:** at the eight Rust row sizes under D-1 (71, 98, 192, 208, 239, 279, 301, 808). These are synthetic source-count scenarios with no real-workload bound.
- **SM-4:** the U-1 static-profile whole graph with build-script outputs absent, the series D-5 assigns to the rows U-1 changes.

U-5a (`s-m-cold-ts-2026-10-13`) covered the TS rows. This unit fills no placeholder, computes no F or T and records no outcome.

## The cold reset

`cold_reset.py` is U-5a's accepted file, byte for byte. Before **every** run, warmups included, as the first statement of the measured loop and before any timestamp, it does three things:
1. **OpenSIP state.** It checks that the project's OpenSIP state is absent; none is ever created.
2. **Disposable caches.** It replaces them with a fresh, empty, private 0700 per-run TMPDIR under the set's TMPDIR, deleting the previous run's first.
3. **Page cache.** It records the OS page-cache state with `vm_stat`. The page cache is never claimed flushed.

The label is **"cold OpenSIP state, page cache recorded"**. Each component directory's `cold-reset-records.json` holds one record per child, in order.

**SM-4 note.** The compiler children run with their constructed command environment and inherit no TMPDIR, so the per-run TMPDIR is the parent runner's only. Every run already writes a fresh output root. For SM-4, the reset therefore contributes the state-absent check and the page-cache record.

## The runners

`build_cold_rust_runners.py` copies each accepted runner byte for byte into its own directory, with U-5a's insertions only:
- the `cold_reset` import;
- one reset as the first statement of the single measured loop;
- `_cr.write(...)` before the lane is released.

There are two runner-specific redirections, each asserted:
- **SM-4.** The runner (U-1's `run_bsabsent_static_profile_series_r1.py`) has no `env`/`T` in its loop. The reset takes a placeholder dict and the series root, and the result goes to this directory.
- **Replay.** It is restricted to the eight Rust sizes, and its outputs go to this directory.

The SM-5 and SM-7 sources are the **published** U-2c runners (`codex-sm-u2c-r2` ACCEPT). `ACCEPTED-RUNNER-SOURCE` names each source and its hash. The audit checks every diff (`allDiffsConfined` True).

Recipes are otherwise unchanged: 3 warmups and 7 measured runs, the lane held, priority 10, and the accepted inputs and pins. A read-only preflight confirmed, before any run, that every pinned input under `/tmp` was intact after the 2026-10-14 temp cleanup (`LD-WORKDIR-TMP-EROSION`).

## Results (lead macOS, preliminary, not D12; ms)

The warm medians (accepted SM-3, replay r2, U-1, and U-2c SM-5 r2 and SM-7 r3) are shown for information only. No ratio or claim is drawn.

| Figure | Workload | Cold median | Cold max | Warm median |
|---|---|---:|---:|---:|
| SM-3 | `SM-3` | 8.400 | 9.112 | 8.688 |
| SM-5 | `rs-medium-axum` | 701.155 | 705.849 | 671.664 |
| SM-5 | `poly-medium-napi-rs` | 682.264 | 688.909 | 647.140 |
| SM-5 | `rs-medium-aws-lambda-rust-runtime` | 1848.345 | 1956.754 | 1775.701 |
| SM-5 | `rs-medium-hyper` | 298.473 | 307.052 | 281.947 |
| SM-5 | `rs-medium-serde` | 93.496 | 93.659 | 85.826 |
| SM-5 | `rs-medium-serde-json` | 145.848 | 146.364 | 134.405 |
| SM-5 | `rs-medium-tokio` | 592.069 | 613.023 | 551.460 |
| SM-5 | `mr-rs-medium-serde-json/rs-medium-serde` | 97.652 | 99.114 | 89.731 |
| SM-5 | `mr-rs-medium-serde-json/rs-medium-serde-json` | 153.181 | 154.104 | 140.003 |
| SM-7 | `rs-medium-axum` | 221.972 | 223.080 | 185.669 |
| SM-7 | `poly-medium-napi-rs` | 217.162 | 217.903 | 180.126 |
| SM-7 | `rs-medium-aws-lambda-rust-runtime` | 359.615 | 361.143 | 307.326 |
| SM-7 | `rs-medium-hyper` | 89.524 | 90.024 | 71.925 |
| SM-7 | `rs-medium-serde` | 37.521 | 37.769 | 29.186 |
| SM-7 | `rs-medium-serde-json` | 47.664 | 49.041 | 38.182 |
| SM-7 | `rs-medium-tokio` | 195.522 | 196.303 | 160.183 |
| SM-7 | `mr-rs-medium-serde-json/rs-medium-serde` | 40.763 | 40.974 | 30.967 |
| SM-7 | `mr-rs-medium-serde-json/rs-medium-serde-json` | 54.858 | 55.924 | 42.269 |
| SM-9 (D-1) | `replay-71` | 445.429 | 460.685 | 451.903 |
| SM-9 (D-1) | `replay-98` | 665.230 | 683.649 | 688.052 |
| SM-9 (D-1) | `replay-192` | 1763.345 | 1814.142 | 1835.616 |
| SM-9 (D-1) | `replay-208` | 2000.114 | 2090.880 | 2094.577 |
| SM-9 (D-1) | `replay-239` | 2493.072 | 2582.435 | 2608.736 |
| SM-9 (D-1) | `replay-279` | 3289.309 | 3317.966 | 3401.329 |
| SM-9 (D-1) | `replay-301` | 3669.324 | 3889.883 | 3870.144 |
| SM-9 (D-1) | `replay-808` | 22099.523 | 22335.544 | 22117.471 |
| SM-4 | `0:poly-medium-napi-rs` | 15603.841 | 15664.550 | 15802.355 |
| SM-4 | `1:rs-medium-aws-lambda-rust-runtime` | 7741.934 | 7792.372 | 7715.988 |
| SM-4 | `2:rs-medium-axum` | 7154.443 | 7178.720 | 7065.915 |
| SM-4 | `3:rs-medium-hyper` | 765.404 | 781.839 | 744.849 |
| SM-4 | `4:rs-medium-serde` | 1467.555 | 1480.289 | 1440.237 |
| SM-4 | `5:rs-medium-serde-json` | 644.702 | 649.319 | 634.981 |
| SM-4 | `6:rs-medium-tokio` | 2733.472 | 2743.411 | 2679.623 |
| SM-4 | `7:mr-rs-medium-serde-json` | 1475.395 | 1483.982 | 1445.043 |
| SM-4 | `8:mr-rs-medium-serde-json` | 740.729 | 743.617 | 724.972 |

**Controls carried by the runners.**
- **SM-4.** Every entry's population, read sets and metadata repeat across its ten runs, and its analysed and incomplete units and new analyses equal U-1's.
- **SM-5.** Every child's repository part reproduces the accepted typed shape, and every shape equals U-2c's.
- **SM-7.** Snapshot manifests, dependency manifests and seals equal U-2c's. The positive control passes and all 20 refusal controls refuse.
- **Replay.** Every replay passes, with one finding per source.

**R8 (`mr-rs-medium-serde-json`), two entry children (D-3).** Medians summed and maxima summed:
- SM-4: 2216.124 / 2227.599;
- SM-5: 250.833 / 253.218;
- SM-7: 95.621 / 96.897.

## Current interpretation

Each copied runner writes its accepted runner's `standing` text verbatim into its result, including the replay runner's withdrawn lower-bound wording. U-5a's round-1 finding covered exactly this. `cold-rust-interpretation.json` is the current interpretation for all five components:
- **Label.** Each is labelled "cold OpenSIP state, page cache recorded".
- **Inherited text.** The inherited `standing` is marked obsolete.
- **Replay.** It carries `SM9LowerBoundOnly=false` and the D-1 synthetic label.

The audit (`audit_cold_rust.py`, read-only, output `cold-rust-checks.json`) requires that record.

## Evidence

All raw child records are in `raw-evidence.tar.xz`, with its index pinned. They are the SM-3 child stdout/stderr, the replay, SM-5 and SM-7 evidence directories, and the 37 MB SM-4 result. The run logs are `run_all-1.log` and `run_all-2.log`, with each component's `run.log`.

## Standing

- **What this is.** Cold-reset inputs for the S-M report (U-6).
- **What it is not.** No F, T or outcome is computed, and no placeholder is filled.
- **Gates.** L-G1 is open, and L is not in effect.
