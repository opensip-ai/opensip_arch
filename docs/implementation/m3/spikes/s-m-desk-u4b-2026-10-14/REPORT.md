# S-M desk record U-4b: SM-10 per F/T component, and SM-11's labelled coverage

**Round 2.** Codex round 1 (`codex-sm-desk-u4b-r1`) found SM-U4B-R1-RF-01: the JSON held two current SM-2 records per reset for Express, one from the cohort and one from the synthesized program. D-4 selects the synthesized program only. Round 2 makes three changes:
- Express is excluded from the cohort loop.
- The cohort's Express figures move to `SM10Informational`, labelled "NOT D-4 SM-2".
- The derivation asserts that every current entry is unique by language, row, component, reset and entry child, and that the count is exactly 152.

No measurement changed. Every other entry equals round 1's, and SM-11 is unchanged. The round-1 derivation, records, report and subject are under `history/`.

This is a desk record under the accepted S-M report plan r3 (`docs/implementation/m3/s-m-report-plan/PLAN-r3.md`, U-4; D-3, D-5, D-7). It completes U-4: U-4a (`s-m-desk-u4a-2026-10-13`) covered SM-8 and S_eff's first term. `derive_u4b.py` reads committed result records, or records pinned by a committed index. Nothing was run. It fills no placeholder, computes no F or T and records no outcome.

## SM-10 per F/T component

**Definition (item 9).** SM-10 is per-process `wait4` `ru_maxrss`, information only. It is given in the native unit as recorded (`bytes` on this macOS host), with the checked conversion to bytes (identity, asserted 0 ≤ v < 2^64). For each row, component and reset, the record gives the median and maximum over the 7 measured runs of that run's process peak. `u4b-desk-records.json` has 152 current entries, each with its source and unique by language, row, component, reset and entry child. It also has two informational entries (the cohort's Express run), which are not SM-2 under D-4.

**Sources.**
- **Warm** (D-7, "warm, priming by warmups, no declared caches"): the accepted component series. These are SM-1 and SM-3 ready, the TS cohort and synthesized program (D-4), typed sealing and transfer (TS rows), replay sized r2, U-1 static-profile for SM-4 (D-5), and U-2c's SM-5 r2 and SM-7 r3 (Rust rows).
- **Cold:** U-5a (TS rows) and U-5b (Rust rows).

**Labels.**
- **SM-4.** A run launches many compiler children, so the per-run value is the **largest single compiler child's peak**, with the child counts recorded. The executor parent is not a recorded process (lead decision LD-U4B-SM4-RSS).
  - **hyper.** Its warm SM-4 is the accepted static-profile series, because U-1 changes no hyper unit (D-5). Its cold SM-4 is the U-1 runner over the same population.
- **SM-7.** The figure is the receiver child's peak; the sender is the measuring parent.
- **SM-1 and SM-3.** Each is one shared start figure for its language.
- **Express SM-2.** The synthesized program (D-4), only.
- **SM-9.** These are synthetic replay scenarios at each row's D-1 size.
- **R8 (D-3).** RSS is reported per entry child, and the table shows the larger of the two (lead decision LD-U4B-R8-RSS). D-3's sums apply to per-child time; peaks of sequential children are not added.

Medians in MiB (1 MiB = 1,048,576 bytes), **warm / cold**. Maxima are in the JSON.

**TS rows**

| Row | SM-1 | SM-2 | SM-5 | SM-7 | SM-9 |
|---|---:|---:|---:|---:|---:|
| `js-medium-express` | 117.1 / 117.2 | 256.7 / 256.9 | 36.1 / 36.0 | 18.5 / 18.4 | 33.2 / 33.3 |
| `poly-medium-napi-rs` | 117.1 / 117.2 | 411.5 / 458.6 | 38.0 / 38.1 | 24.5 / 24.6 | 37.9 / 37.9 |
| `ts-medium-powertools-lambda` | 117.1 / 117.2 | 787.3 / 714.9 | 37.2 / 37.3 | 20.4 / 20.4 | 109.2 / 108.8 |
| `ts-medium-smithy-typescript` | 117.1 / 117.2 | 888.1 / 937.4 | 38.7 / 38.7 | 25.4 / 25.3 | 131.6 / 132.1 |
| `ts-medium-umami` | 117.1 / 117.2 | 782.9 / 776.5 | 37.4 / 37.5 | 21.7 / 21.7 | 151.4 / 151.4 |
| `ts-medium-vite` | 117.1 / 117.2 | 1328.5 / 1315.9 | 42.7 / 42.7 | 26.8 / 26.7 | 84.9 / 84.9 |

**Rust rows**

| Row | SM-3 | SM-4 | SM-5 | SM-7 | SM-9 |
|---|---:|---:|---:|---:|---:|
| `poly-medium-napi-rs` | 24.6 / 24.6 | 494.7 / 493.7 | 55.8 / 55.8 | 31.5 / 31.5 | 42.4 / 42.7 |
| `rs-medium-aws-lambda-rust-runtime` | 24.6 / 24.6 | 386.4 / 386.1 | 58.6 / 58.5 | 40.0 / 40.0 | 37.9 / 38.6 |
| `rs-medium-axum` | 24.6 / 24.6 | 414.2 / 414.3 | 56.0 / 56.1 | 31.2 / 30.9 | 48.8 / 48.8 |
| `rs-medium-hyper` | 24.6 / 24.6 | 200.4 / 200.9 | 53.7 / 53.7 | 23.6 / 23.4 | 29.1 / 29.1 |
| `rs-medium-serde` | 24.6 / 24.6 | 263.7 / 262.4 | 53.0 / 53.0 | 20.3 / 20.3 | 39.7 / 39.9 |
| `rs-medium-serde-json` | 24.6 / 24.6 | 249.5 / 249.5 | 53.1 / 53.1 | 21.1 / 21.0 | 26.7 / 26.8 |
| `rs-medium-tokio` | 24.6 / 24.6 | 326.4 / 327.8 | 55.6 / 55.5 | 26.6 / 26.6 | 97.2 / 97.2 |
| `mr-rs-medium-serde-json` | 24.6 / 24.6 | 264.7 / 265.0 | 53.2 / 53.2 | 21.1 / 21.1 | 46.2 / 46.6 |

## SM-11: SM-4 and SM-10 by covered units (medium Rust rows)

**Rule (item 9, S-M round part).** For each workload the record carries:
- the exact subject count S by RUST3-LIM's recipe;
- SM-4's time and SM-10's peak RSS, each labelled with the compilation units it covers.

A quotient by S is recorded **only** where those units are exactly the workload's first-party crates holding its S subjects. A figure that includes dependency crates, or misses a first-party unit, is recorded with its coverage and no quotient. The worker's scratch is not measured here.

**Coverage.** The coverage comes from U-1's populations, the SM-4 series under D-5, read from the first measured run's unit standings. A unit is first-party when its Cargo `pkg_id` is a `path+` package; every other unit is a dependency. S is RUST3-LIM's count, as the census records it.

| Ord | Row | S | SM-4 warm ms (median / max) | SM-4 cold ms | SM-10 MiB warm / cold | First-party analysed | First-party not analysed | Dependency units analysed | Quotient |
|---|---|---:|---:|---:|---:|---|---:|---:|---|
| 0 | `poly-medium-napi-rs` | 239 | 15802.4 / 15872.9 | 15603.8 / 15664.5 | 494.7 / 493.7 | 4 (napi_build (lib), napi_derive_backend (lib), napi_derive_backend (lib), napi_sys (lib)) | 38 | 93 | none: includes dependency crates and misses first-party units |
| 1 | `rs-medium-aws-lambda-rust-runtime` | 192 | 7716.0 / 7740.4 | 7741.9 / 7792.4 | 386.4 / 386.1 | 0 (—) | 8 | 63 | none: includes dependency crates and misses first-party units |
| 2 | `rs-medium-axum` | 301 | 7065.9 / 7083.4 | 7154.4 / 7178.7 | 414.2 / 414.3 | 1 (axum_core (lib)) | 3 | 43 | none: includes dependency crates and misses first-party units |
| 3 | `rs-medium-hyper` | 98 | 738.5 / 749.2 | 765.4 / 781.8 | 200.4 / 200.9 | 1 (hyper (lib)) | 0 | 6 | none: includes dependency crates |
| 4 | `rs-medium-serde` | 208 | 1440.2 / 1448.8 | 1467.6 / 1480.3 | 263.7 / 262.4 | 0 (—) | 12 | 8 | none: includes dependency crates and misses first-party units |
| 5 | `rs-medium-serde-json` | 71 | 635.0 / 639.7 | 644.7 / 649.3 | 249.5 / 249.5 | 0 (—) | 3 | 3 | none: includes dependency crates and misses first-party units |
| 6 | `rs-medium-tokio` | 808 | 2679.6 / 2682.7 | 2733.5 / 2743.4 | 326.4 / 327.8 | 1 (tests_build (lib)) | 8 | 26 | none: includes dependency crates and misses first-party units |
| 7 | `mr-rs-medium-serde-json` / rs-medium-serde | 279 | 1445.0 / 1460.5 | 1475.4 / 1484.0 | 264.7 / 265.0 | 0 (—) | 12 | 8 | none: includes dependency crates and misses first-party units |
| 8 | `mr-rs-medium-serde-json` / rs-medium-serde-json | 279 | 725.0 / 732.2 | 740.7 / 743.6 | 261.3 / 259.8 | 0 (—) | 6 | 3 | none: includes dependency crates and misses first-party units |

**Result.** Every row's covered units include dependency crates. Every row except hyper also misses first-party units, which are unavailable for the reasons in the JSON (build scripts, proc macros, non-library targets and their dependants, and `serde_core`'s `OUT_DIR` include). Under item 9's rule, **no SM-11 quotient is recorded**. This agrees with the accepted census.

**R8 two entry children (D-3).** The SM-4 medians sum to 2170.0 ms warm and 2216.1 ms cold.

## Standing

- **Records.** Desk records only, on the lead's macOS host, labelled preliminary, not D12.
- **Not filled.** No `⟨SM-n⟩` placeholder, F, T or outcome; SM-12 to SM-14 are untouched.
- **Gates.** O7, D3 and D13 are closed. L-G1 is open, and L is not in effect.
