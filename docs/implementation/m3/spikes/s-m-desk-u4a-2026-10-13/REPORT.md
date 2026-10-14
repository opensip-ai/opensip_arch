# S-M desk record U-4a: SM-8 and S_eff's first term

This is a desk record under the accepted S-M report plan (`docs/implementation/m3/s-m-report-plan/PLAN-r2.md`, Codex r2 ACCEPT). It applies D-6 and D-9 to accepted, committed evidence. Nothing was run. It fills no placeholder, computes no F or T and records no outcome; S_eff is not filled.

The plan's U-4 is split. **U-4a** (this record) covers SM-8 and S_eff's first term. **U-4b** covers SM-10 per F/T component and SM-11's labelled SM-4/SM-10 by covered units; it follows U-1, which changes SM-4's coverage.

## SM-8 under D-6

**Definition (D-6).** For each measured SM-2 run, SM-8 is the longest single public TypeScript compiler API call the SM-2 driver made, with its call name. The record gives the median and maximum over the 7 measured runs.

- **Source.** `derive_u4a.py` reads each measured run's committed stdout evidence (ordinals 3-9 of `results.json`).
- **The maximum.** It takes the maximum over every configuration's retained `calls[]`, incomplete configurations included.
- **Cross-check.** Where a completed configuration records `maxPublicCompilerCall`, that value must equal the maximum of its calls.
- **Express.** Express uses the synthesized program, under D-4.

| Row | Source | Median ms | Max ms | Longest call |
|---|---|---:|---:|---|
| poly-medium-napi-rs | s-m-ts-cohort-2026-10-09 | 105.719 | 114.749 | createProgram |
| ts-medium-powertools-lambda | s-m-ts-cohort-2026-10-09 | 125.411 | 130.272 | createProgram |
| ts-medium-smithy-typescript | s-m-ts-cohort-2026-10-09 | 209.570 | 216.292 | getSemanticDiagnostics |
| ts-medium-umami | s-m-ts-cohort-2026-10-09 | 250.174 | 258.166 | createProgram |
| ts-medium-vite | s-m-ts-cohort-2026-10-09 | 198.878 | 206.101 | getSemanticDiagnostics |
| js-medium-express | s-m-ts-synthesized-2026-10-10 | 106.561 | 109.894 | createProgram |

**Label (D-6).** The driver's call granularity is `createProgram` per configuration and `getSemanticDiagnostics` per file. A provider that calls `getSemanticDiagnostics` program-wide would block for longer. The D law takes SM-8 for its liveness floor, so this label travels with the figure.

## S_eff's first term under D-9

**Definition (D-9).** For each Rust workload, the term is SM-5's measured snapshot2-equivalent population, copied from the accepted sealing checks:

- the rows;
- the total bytes;
- the canonical descriptor bytes;
- the standing against each bound: 100,000 rows, a 4 MiB descriptor and 8 GiB in total.

No ceiling is extrapolated from average bytes per row. Under D-2, a Rust row's dependency-source part is owed by U-2. It will be reported beside this term, not added to snapshot2's rows.

| Workload | Rows | Total bytes | Descriptor bytes | Within every bound | Source |
|---|---:|---:|---:|---|---|
| poly-medium-napi-rs | 644 | 11,675,794 | 88,420 | yes | `s-m-sealing-typed-2026-10-09` |
| rs-medium-aws-lambda-rust-runtime | 567 | 2,446,357 | 86,122 | yes | `s-m-sealing-typed-2026-10-09` |
| rs-medium-axum | 498 | 1,968,335 | 71,338 | yes | `s-m-sealing-typed-2026-10-09` |
| rs-medium-hyper | 138 | 1,447,837 | 17,039 | yes | `s-m-sealing-typed-2026-10-09` |
| rs-medium-serde | 347 | 1,331,295 | 50,946 | yes | `s-m-sealing-typed-2026-10-09` |
| rs-medium-serde-json | 92 | 737,131 | 11,578 | yes | `s-m-sealing-typed-2026-10-09` |
| rs-medium-tokio | 883 | 6,256,646 | 116,528 | yes | `s-m-sealing-typed-2026-10-09` |
| mr-rs-medium-serde-json | 439 | 2,068,426 | 69,635 | yes | `s-m-sealing-typed-2026-10-09` |
| poly-large-rspack | 23,980 | 69,293,473 | 4,085,164 | yes | `s-m-sealing-typed-remaining-2026-10-11` |
| poly-very-large-deno | 14,920 | 93,725,209 | 2,227,549 | yes | `s-m-sealing-typed-remaining-2026-10-11` |
| rs-large-smithy-rs | 3,632 | 51,487,333 | 647,602 | yes | `s-m-sealing-typed-remaining-2026-10-11` |
| rs-very-large-sui | 19,063 | 203,261,240 | 3,509,292 | yes | `s-m-sealing-typed-remaining-2026-10-11` |

## Standing

- **Records.** Desk records only, on the lead's macOS host, labelled preliminary.
- **Not filled.** No `⟨SM-n⟩` placeholder, no S_eff, no F, T or outcome.
- **Gates.** O7, D3 and D13 are closed. L-G1 is open, and L is not in effect.
