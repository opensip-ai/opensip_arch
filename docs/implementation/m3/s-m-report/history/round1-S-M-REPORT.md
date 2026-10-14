# S-M report: one-shot M3 provider figures (item 9)

**Lead report record, 2026-10-14 (U-6 of the S-M report plan r3). Preliminary: the lead's macOS host, not the D12 runner. Unreviewed until Codex accepts it.** This is the report M3-L r6 item 9 asks S-M for (`provider-protocol-l/PROPOSAL-r6.md`, item 9). It applies the plan's definitions D-1 to D-9 (`s-m-report-plan/PLAN-r3.md`) to accepted records, gives every figure SM-1 to SM-14 at its standing, computes F and T per workload under each reset S-M applied, and records **every** outcome that holds.

It is the S-M round's input, not its decision. The S-M delta round on L (L-G1) records these outcomes in L and raises the owner questions they name. Nothing here fills a `⟨SM-n⟩` placeholder in L, changes L, or takes effect. O7, D3 and D13 are closed, and only L-G1 is open.

`sm-report-data.json` carries every number below with its source record and SHA-256 pin. `assemble_sm_report.py` recomputes each component statistic from the raw run records: the median and maximum of 7 measured runs after 3 warmups.

## 1. Definitions applied

- **Workloads** (item 9, r2).
  - **TS rows (6):** express, napi-rs (TS), powertools-lambda, smithy-typescript, umami and vite.
  - **Rust rows (8):** napi-rs (Rust), aws-lambda-rust-runtime, axum, hyper, serde, serde-json, tokio, and the overlay `mr-rs-medium-serde-json` (R8).
- **Statistic.** 3 warmups and then 7 runs; median, with the maximum also reported.
- **D-1, SM-9.** SM-9 is the native release `replay_run` over a synthetic graph with one fact, one finding and one fingerprint per counted source. The source count is the TS row's distinct configured files (express: the 141 synthesized roots) or the Rust row's RUST3-LIM S. It is a **workload source-count scenario, not a bound on any real workload**, so every F, T and outcome below is **conditional on D-1**.
- **D-2, the Rust dependency set.** The Rust dependency-source set is `DependencySourceSetV1` (DS4-P1). SM-5 for Rust is the two-part one-span series. SM-7 for Rust streams the repository set and then the dependency set with every NE §9.2 field (U-2c).
- **D-3, R8.** R8 runs as its two Cargo entries. SM-4, SM-5 and SM-7 are the sums of the two entry children. SM-3 enters F once per child, so twice.
- **D-4, SM-2.** SM-2 is the cohort's whole-process span; for express it is the synthesized program. T = F + SM-2 counts the TS start twice, once in SM-1 and again inside SM-2. The over-count is stated beside each TS T.
- **D-5, SM-4.** SM-4 is the static-profile whole graph. It uses U-1's series (build-script outputs absent) for the rows U-1 changes, and the accepted static-profile series for hyper.
- **D-6 to D-9.** D-6 defines SM-8, D-7 the reset labels, D-8 SM-12's labels, and D-9 S_eff's first term (§4).
- **Resets (D-7).**
  - **Warm:** the accepted 3+7 series, "warm, priming by warmups, no declared caches".
  - **Cold:** U-5a (TS) and U-5b (Rust): "cold OpenSIP state, page cache recorded (never claimed flushed)".

## 2. Component figures (ms; median, warm / cold)

Maxima are in `sm-report-data.json`. SM-1 and SM-3 are each one start figure shared by every row of their language.

**TS rows**

| Row | SM-1 | SM-2 | SM-5 | SM-7 | SM-9 |
|---|---:|---:|---:|---:|---:|
| `js-medium-express` | 81.8 / 82.9 | 257.1 / 261.7 | 6.9 / 8.3 | 4.9 / 6.8 | 1,177.0 / 1,241.4 |
| `poly-medium-napi-rs` | 81.8 / 82.9 | 1,027.0 / 1,032.5 | 23.2 / 26.0 | 15.2 / 20.1 | 1,844.6 / 1,866.2 |
| `ts-medium-powertools-lambda` | 81.8 / 82.9 | 3,465.6 / 3,617.4 | 45.7 / 51.7 | 24.4 / 35.2 | 28,515.2 / 28,590.5 |
| `ts-medium-smithy-typescript` | 81.8 / 82.9 | 16,295.8 / 16,308.1 | 80.1 / 90.6 | 41.6 / 59.7 | 44,501.9 / 43,491.2 |
| `ts-medium-umami` | 81.8 / 82.9 | 2,302.6 / 2,236.4 | 66.1 / 74.8 | 34.2 / 50.2 | 62,508.6 / 59,405.1 |
| `ts-medium-vite` | 81.8 / 82.9 | 8,059.2 / 7,939.9 | 102.5 / 116.6 | 54.6 / 74.5 | 16,514.9 / 15,657.7 |

**Rust rows** (R8 shows the D-3 entry sums; SM-3 is per child)

| Row | SM-3 | SM-4 | SM-5 | SM-7 | SM-9 |
|---|---:|---:|---:|---:|---:|
| `poly-medium-napi-rs` | 8.7 / 8.4 | 15,802.4 / 15,603.8 | 647.1 / 682.3 | 180.1 / 217.2 | 2,608.7 / 2,493.1 |
| `rs-medium-aws-lambda-rust-runtime` | 8.7 / 8.4 | 7,716.0 / 7,741.9 | 1,775.7 / 1,848.3 | 307.3 / 359.6 | 1,835.6 / 1,763.3 |
| `rs-medium-axum` | 8.7 / 8.4 | 7,065.9 / 7,154.4 | 671.7 / 701.2 | 185.7 / 222.0 | 3,870.1 / 3,669.3 |
| `rs-medium-hyper` | 8.7 / 8.4 | 738.5 / 765.4 | 281.9 / 298.5 | 71.9 / 89.5 | 688.1 / 665.2 |
| `rs-medium-serde` | 8.7 / 8.4 | 1,440.2 / 1,467.6 | 85.8 / 93.5 | 29.2 / 37.5 | 2,094.6 / 2,000.1 |
| `rs-medium-serde-json` | 8.7 / 8.4 | 635.0 / 644.7 | 134.4 / 145.8 | 38.2 / 47.7 | 451.9 / 445.4 |
| `rs-medium-tokio` | 8.7 / 8.4 | 2,679.6 / 2,733.5 | 551.5 / 592.1 | 160.2 / 195.5 | 22,117.5 / 22,099.5 |
| `mr-rs-medium-serde-json` | 8.7 / 8.4 | 2,170.0 / 2,216.1 | 229.7 / 250.8 | 73.2 / 95.6 | 3,401.3 / 3,289.3 |

**Labels.**
- **TS SM-5 and SM-7.** These are the repository-only read set, because T2 pins no `node_modules` tree (SM-6).
- **Rust SM-5.** It is the repository part and the dependency part in one span.
- **Rust SM-7.** The dependency phase carries NE's fields with JSON headers; no protocol conformance is claimed.
- **SM-4.** It covers part of each workload (§4, SM-11).
- **SM-9.** It is synthetic under D-1.

## 3. F, T and outcomes

**Definitions.**
- **F and T** (item 9): F = start (SM-1 or SM-3) + SM-5 + SM-7 + SM-9, and T = F + analysis (SM-2 or SM-4). Each is computed here as the **sum of component medians**; the sums of maxima are in the JSON.
- **Targets.** These are the owner-approved targets (`analysis-quality/PLAN.md` §5.2 and §5.3), held on the D12 runner, so this comparison is preliminary:
  - edit target: ≤ 2 s median, **warm**;
  - medium budgets: cold ≤ 30 s and warm ≤ 8 s.
- **Outcome rules** (item 9):
  - **(B)** holds when warm F > 2 s;
  - **(C)** holds when cold T > 30 s or warm T > 8 s;
  - **(A)** holds only when neither does.

Cold F is shown for information; the edit target is warm.

Seconds:

**TS rows**

| Row | F warm | F cold | T warm | T cold | F warm without SM-9 | Outcomes |
|---|---:|---:|---:|---:|---:|---|
| `js-medium-express` | 1.271 | 1.339 | 1.528 | 1.601 | 0.094 | (A) |
| `poly-medium-napi-rs` | 1.965 | 1.995 | 2.992 | 3.028 | 0.120 | (A) |
| `ts-medium-powertools-lambda` | 28.667 | 28.760 | 32.133 | 32.378 | 0.152 | (B), (C) |
| `ts-medium-smithy-typescript` | 44.705 | 43.725 | 61.001 | 60.033 | 0.204 | (B), (C) |
| `ts-medium-umami` | 62.691 | 59.613 | 64.993 | 61.849 | 0.182 | (B), (C) |
| `ts-medium-vite` | 16.754 | 15.932 | 24.813 | 23.872 | 0.239 | (B), (C) |

**Rust rows**

| Row | F warm | F cold | T warm | T cold | F warm without SM-9 | Outcomes |
|---|---:|---:|---:|---:|---:|---|
| `poly-medium-napi-rs` | 3.445 | 3.401 | 19.247 | 19.005 | 0.836 | (B), (C) |
| `rs-medium-aws-lambda-rust-runtime` | 3.927 | 3.980 | 11.643 | 11.722 | 2.092 | (B), (C) |
| `rs-medium-axum` | 4.736 | 4.601 | 11.802 | 11.755 | 0.866 | (B), (C) |
| `rs-medium-hyper` | 1.051 | 1.062 | 1.789 | 1.827 | 0.363 | (A) |
| `rs-medium-serde` | 2.218 | 2.140 | 3.659 | 3.607 | 0.124 | (B) |
| `rs-medium-serde-json` | 0.633 | 0.647 | 1.268 | 1.292 | 0.181 | (A) |
| `rs-medium-tokio` | 22.838 | 22.896 | 25.517 | 25.629 | 0.720 | (B), (C) |
| `mr-rs-medium-serde-json` | 3.722 | 3.653 | 5.892 | 5.869 | 0.320 | (B) |

**Outcomes that hold** (every one, preliminary, conditional on D-1):
- **(A)** only: js-medium-express (tsjs), poly-medium-napi-rs (tsjs), rs-medium-hyper (rust), rs-medium-serde-json (rust).
- **(B)**, F > 2 s: ts-medium-powertools-lambda (tsjs), ts-medium-smithy-typescript (tsjs), ts-medium-umami (tsjs), ts-medium-vite (tsjs), poly-medium-napi-rs (rust), rs-medium-aws-lambda-rust-runtime (rust), rs-medium-axum (rust), rs-medium-serde (rust), rs-medium-tokio (rust), mr-rs-medium-serde-json (rust).
- **(C)**, T over a medium budget: ts-medium-powertools-lambda (tsjs), ts-medium-smithy-typescript (tsjs), ts-medium-umami (tsjs), ts-medium-vite (tsjs), poly-medium-napi-rs (rust), rs-medium-aws-lambda-rust-runtime (rust), rs-medium-axum (rust), rs-medium-tokio (rust).

**Sensitivities.** These are reported beside the outcomes; nothing is substituted for them.
- `poly-medium-napi-rs` (tsjs): the outcome differs under sums of maxima (warm F 2.042 s).
- `ts-medium-powertools-lambda` (tsjs): (B) depends on the synthetic SM-9: without it, warm F is 0.152 s; warm (C) depends on the synthetic SM-9; cold (C) depends on the synthetic SM-9; warm (C) holds without the double-counted TS start (D-4); cold (C) holds without the double-counted TS start (D-4).
- `ts-medium-smithy-typescript` (tsjs): (B) depends on the synthetic SM-9: without it, warm F is 0.204 s; warm (C) holds without SM-9; cold (C) depends on the synthetic SM-9; warm (C) holds without the double-counted TS start (D-4); cold (C) holds without the double-counted TS start (D-4).
- `ts-medium-umami` (tsjs): (B) depends on the synthetic SM-9: without it, warm F is 0.182 s; warm (C) depends on the synthetic SM-9; cold (C) depends on the synthetic SM-9; warm (C) holds without the double-counted TS start (D-4); cold (C) holds without the double-counted TS start (D-4).
- `ts-medium-vite` (tsjs): (B) depends on the synthetic SM-9: without it, warm F is 0.239 s; warm (C) holds without SM-9; warm (C) holds without the double-counted TS start (D-4).
- `poly-medium-napi-rs` (rust): (B) depends on the synthetic SM-9: without it, warm F is 0.836 s; warm (C) holds without SM-9.
- `rs-medium-aws-lambda-rust-runtime` (rust): (B) holds without SM-9; warm (C) holds without SM-9.
- `rs-medium-axum` (rust): (B) depends on the synthetic SM-9: without it, warm F is 0.866 s; warm (C) depends on the synthetic SM-9.
- `rs-medium-serde` (rust): (B) depends on the synthetic SM-9: without it, warm F is 0.124 s.
- `rs-medium-tokio` (rust): (B) depends on the synthetic SM-9: without it, warm F is 0.720 s; warm (C) depends on the synthetic SM-9.
- `mr-rs-medium-serde-json` (rust): (B) depends on the synthetic SM-9: without it, warm F is 0.320 s.

**Reading.**
- **(B) comes from the synthetic SM-9.** (B) holds without SM-9 only for rs-medium-aws-lambda-rust-runtime (rust). Every other (B) depends on D-1's one-fact-and-one-finding-per-source replay scenario.
- **SM-9 grows faster than linearly.** Across the D-1 scenarios, the replay span grows faster than the source count: 71 sources take 0.452 s and 1381 sources take 62.509 s, which is ×19.5 sources against ×138.3 time. This is descriptive; no complexity claim is made.
- **(C) without SM-9.** (C) holds without SM-9, under at least one reset, for ts-medium-smithy-typescript (tsjs), ts-medium-vite (tsjs), poly-medium-napi-rs (rust), rs-medium-aws-lambda-rust-runtime (rust). For ts-medium-powertools-lambda (tsjs), ts-medium-umami (tsjs), rs-medium-axum (rust), rs-medium-tokio (rust), (C) depends on SM-9. Rust SM-4's whole-graph span includes dependency crates, and TS SM-2 includes the TS start (D-4).
- **Edge case.** poly-medium-napi-rs (tsjs): (A) on sums of medians, but warm F exceeds 2 s on sums of maxima. The outcome stands as computed, with this stated.
- **For the delta round.** Under item 9, (B) raises owner question O3 and (C) raises O4. Both are recorded together, and neither masks the other. These are the S-M delta round's to record and raise, with the D-1 dependence stated.

## 4. Other figures

**SM-6** (accepted, `s-m-sm6-readset-2026-10-09`): the TS read-set size. It is repository-only, labelled, because T2 pins no dependency tree. Entries, content bytes and snapshot-equivalent descriptor bytes:

| Row | Entries | Content bytes | Descriptor bytes |
|---|---:|---:|---:|
| `js-medium-express` | 214 | 717115 | 27305 |
| `poly-medium-napi-rs` | 644 | 11675794 | 88420 |
| `ts-medium-powertools-lambda` | 1389 | 7818881 | 206175 |
| `ts-medium-smithy-typescript` | 2315 | 11541863 | 381452 |
| `ts-medium-umami` | 2026 | 9083336 | 283572 |
| `ts-medium-vite` | 2836 | 17644692 | 419807 |

Every set is within TS2's 200,000 entries and snapshot2's 100,000 rows, 4 MiB descriptor and 8 GiB.

**SM-8** (D-6; U-4a, `s-m-desk-u4a-2026-10-13`): the longest single public compiler call, in ms.

| Row | Source | Median | Max | Call |
|---|---|---:|---:|---|
| `js-medium-express` | s-m-ts-synthesized-2026-10-10 | 106.6 | 109.9 | createProgram |
| `poly-medium-napi-rs` | s-m-ts-cohort-2026-10-09 | 105.7 | 114.7 | createProgram |
| `ts-medium-powertools-lambda` | s-m-ts-cohort-2026-10-09 | 125.4 | 130.3 | createProgram |
| `ts-medium-smithy-typescript` | s-m-ts-cohort-2026-10-09 | 209.6 | 216.3 | getSemanticDiagnostics |
| `ts-medium-umami` | s-m-ts-cohort-2026-10-09 | 250.2 | 258.2 | createProgram |
| `ts-medium-vite` | s-m-ts-cohort-2026-10-09 | 198.9 | 206.1 | getSemanticDiagnostics |

Label: the driver's call granularity is `createProgram` per configuration and `getSemanticDiagnostics` per file. A program-wide call would block for longer.

**SM-10** (U-4b, `s-m-desk-u4b-2026-10-14`): the `wait4` peak RSS per process, for every row, component and reset (152 entries). It is information only, in native bytes with checked conversion. For SM-4 it is the largest compiler child; R8 is given per entry and as the larger of the two.

**SM-11** (U-4b, and U-7 for the large workloads): SM-4's time and SM-10's peak, labelled by covered units. **No quotient is recorded for any workload.** Every medium row's covered units include dependency crates, and all but hyper also miss first-party units. Large-workload coverage is partial (smithy-rs 13 of 1,084 subjects with sites, deno 1 of 1,052) or absent (rspack, sui).

**SM-12** (accepted, `s-m-rust-scope-2026-10-09`, plus `s-m-sui-scope-series-2026-10-10`): rebuilding the Rust subject scope. Two independent host derivations and a worker-prototype process agree on every array and commitment. Median ms:

| Workload | S | host-a | host-b | worker-prototype | Arrays and commitments equal |
|---|---:|---:|---:|---:|---|
| `poly-medium-napi-rs` | 239 | 3.0 | 5.9 | 5.9 | True |
| `rs-medium-aws-lambda-rust-runtime` | 192 | 2.4 | 4.9 | 4.9 | True |
| `rs-medium-axum` | 301 | 3.7 | 7.1 | 7.1 | True |
| `rs-medium-hyper` | 98 | 1.2 | 2.9 | 2.9 | True |
| `rs-medium-serde` | 208 | 2.6 | 5.2 | 5.2 | True |
| `rs-medium-serde-json` | 71 | 0.9 | 1.4 | 1.4 | True |
| `rs-medium-tokio` | 808 | 9.9 | 17.5 | 17.4 | True |
| `rs-large-smithy-rs` | 1084 | 13.4 | 22.9 | 22.9 | True |
| `poly-large-rspack` | 1384 | 17.7 | 30.4 | 30.4 | True |
| `poly-very-large-deno` | 1052 | 13.2 | 22.8 | 22.9 | True |
| `mr-rs-medium-serde-json` | 279 | 3.5 | 6.7 | 6.6 | True |

D-8's labels apply. Peak memory is whole-process `wait4` RSS, "process peak, not incremental algorithm heap accounting". "The accepted manifest" is the T2 corpus manifest (`c8cc48e1…`). For sui (item 9: "if S-P permits"), the accepted sui scope series gives 3,318 subjects: host-a 40.0 ms and host-b 67.6 ms. `domainCommitment` with bound keys and the worker's derivation wait for the completion round.

**SM-13** (a decomposition, not a value): census v2, `s-m-rust-site-census-v2-2026-10-13`, for the medium rows, and U-7 for the large rows. It gives:
- the site counts per relation@rung, labelled **sites, not candidates**;
- the exact fixed bytes from the registered schemas and RPP `candidateSpoolAccounting`: spool entry 35, FactBatch envelope 78, V2 47 or V3 82, occupancy companion 140, transport prefix 40 per frame, census row 61 and container 35;
- closed formulas (a) to (e) with G3's emission factor, census kinds and batching unset, and C4a's stages and keys unset.

**SM-14:** the formula Σ over stages of S_stage × K_stage, with S exact per workload and K_stage unset (C4a).

**S_eff** (D-9; U-4a): the first term is snapshot2's admitted rows, from SM-5, for all 12 Rust workloads. Every one is within snapshot2's bounds; for example, rspack has 23,980 rows and a 4,085,164-byte descriptor. Under D-2, each Rust row's dependency-source part (U-2c: 27 to 234 packages, 999 to 11,330 entries, up to 166,417,590 bytes) is reported beside it, not added to it. The other terms of S_eff remain formulas, and S_eff is not filled.

## 5. Large workloads (§3a; no outcome depends on them)

| Workload | S | SM-12 | SM-4/SM-10 coverage | SM-13 sites | S_eff first term |
|---|---:|---|---|---|---|
| smithy-rs | 1,084 | accepted 3+7 | partial: 10 of 25 entries analysed; 15 unavailable with exact reasons (U-7) | census over the 10 entries (U-7): 13 subjects with sites | 3,632 rows; 647,602 descriptor bytes |
| rspack | 1,384 | accepted 3+7 | none: both entries refused by the pinned stable compiler (nightly-only `-Z` flags) | none | 23,980 rows; 4,085,164 descriptor bytes |
| deno | 1,052 | accepted 3+7 | partial: 2 entries analysed; the root descriptor (22,825,382 bytes) is over the closed driver's bound | census over the 2 entries: 1 subject with sites | 14,920 rows; 2,227,549 descriptor bytes |
| sui (if S-P permits) | 3,318 | accepted 3+7 | none: two Git dependencies cannot be checked out offline, and the bin source is an excluded symlink | none | 19,063 rows; 3,509,292 descriptor bytes |

## 6. Standing and what this report does not do

- **Preliminary.** These are the lead's macOS host figures, not D12's. The targets are held on the D12 runner.
- **Conditional.** F, T and every outcome depend on D-1's synthetic SM-9.
- **Not filled.** No `⟨SM-n⟩` placeholder is filled in L. SM-11's quotients, SM-13's values, SM-14's values, S_eff, the worker's scratch and `domainCommitment` wait for the completion round (item 9, r6).
- **Not changed.** L, the closed drivers, executors, observers and generators, and every accepted record are unchanged. No G3 or C4a parameter is chosen.
- **Still open.** Full S-M closes at the S-M delta round. L-G1, effective L, native admission and worker, K1 and qualification remain open.
