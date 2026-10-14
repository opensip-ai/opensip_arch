# S-M report: one-shot M3 provider figures (item 9)

**Lead report record, 2026-10-14 (U-6 of the S-M report plan r3). Preliminary: the lead's macOS host, not the D12 runner. Unreviewed until Codex accepts it.** This is the report M3-L r6 item 9 asks S-M for (`provider-protocol-l/PROPOSAL-r6.md`, item 9). It applies the plan's definitions D-1 to D-9 (`s-m-report-plan/PLAN-r3.md`) to accepted records, gives every figure SM-1 to SM-14 at its standing, computes F and T per workload under each reset S-M applied, and records **every** outcome that holds.

It is the S-M round's input, not its decision. The S-M delta round on L (L-G1) records these outcomes in L and raises the owner questions they name. Nothing here fills a `⟨SM-n⟩` placeholder in L, changes L, or takes effect. O7, D3 and D13 are closed, and only L-G1 is open.

**Round 2** (Codex SM-U6-R1-RF-01 and RF-02): every figure in §4 and §5 is now materialized in `sm-report-data.json` → `otherFigures` from pinned accepted records, and the renderer reads only that file. §4 adds the SM-5 populations against their bounds, and SM-12's maxima and peak RSS for every actor, Sui included. The timing components, F, T and outcomes are unchanged from round 1. `sm-report-data.json` carries every number in this report, with its source records pinned by SHA-256. `assemble_sm_report.py` recomputes each component statistic from the raw run records: the median and maximum of 7 measured runs after 3 warmups.

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

Every value in this section is materialized in `sm-report-data.json` → `otherFigures`, with the source records pinned in `pins`.

**SM-5 populations** (item 9 SM-5; D-9; D-2). The rows are the snapshot2-equivalent inventory population. The repository part's bounds are 100,000 rows, a 4 MiB descriptor and 8 GiB. The dependency part's bounds are 4,096 packages, 1,000,000 entries and 8 GiB (NE:2931-2932; the schema's packages maxItems). No contract bound was found on dependency descriptor bytes, so they are reported only. R8 is given per entry; each entry's repository part is the overlay union (D-3). The dependency part is reported beside snapshot2's rows, never added to them.

| Row | Repo rows | Repo bytes | Snapshot descriptor bytes | Within repo bounds | Dep packages | Dep entries | Dep bytes | Dep descriptor bytes | Within dep bounds |
|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| `js-medium-express` (TS) | 214 | 717115 | 27305 | yes | — | — | — | — | — |
| `poly-medium-napi-rs` (TS) | 644 | 11675794 | 88420 | yes | — | — | — | — | — |
| `ts-medium-powertools-lambda` (TS) | 1389 | 7818881 | 206175 | yes | — | — | — | — | — |
| `ts-medium-smithy-typescript` (TS) | 2315 | 11541863 | 381452 | yes | — | — | — | — | — |
| `ts-medium-umami` (TS) | 2026 | 9083336 | 283572 | yes | — | — | — | — | — |
| `ts-medium-vite` (TS) | 2836 | 17644692 | 419807 | yes | — | — | — | — | — |
| `rs-medium-axum` (Rust) | 498 | 1968335 | 71338 | yes | 187 | 7338 | 75258910 | 95069 | yes |
| `poly-medium-napi-rs` (Rust) | 644 | 11675794 | 88420 | yes | 153 | 6852 | 76407827 | 77833 | yes |
| `rs-medium-aws-lambda-rust-runtime` (Rust) | 567 | 2446357 | 86122 | yes | 234 | 11330 | 166417590 | 118987 | yes |
| `rs-medium-hyper` (Rust) | 138 | 1447837 | 17039 | yes | 55 | 2880 | 37658554 | 28143 | yes |
| `rs-medium-serde` (Rust) | 347 | 1331295 | 50946 | yes | 27 | 999 | 11156070 | 13943 | yes |
| `rs-medium-serde-json` (Rust) | 92 | 737131 | 11578 | yes | 37 | 1586 | 17011309 | 19001 | yes |
| `rs-medium-tokio` (Rust) | 883 | 6256646 | 116528 | yes | 146 | 6031 | 59869578 | 74270 | yes |
| `mr-rs-medium-serde-json` (Rust) / rs-medium-serde | 439 | 2068426 | 69635 | yes | 27 | 999 | 11156070 | 13943 | yes |
| `mr-rs-medium-serde-json` (Rust) / rs-medium-serde-json | 439 | 2068426 | 69635 | yes | 34 | 1490 | 15723557 | 17477 | yes |

**SM-6** (accepted, `s-m-sm6-readset-2026-10-09`): the TS read-set size. It is repository-only, labelled, because T2 pins no dependency tree.

| Row | Entries | Content bytes | Descriptor bytes | Within TS2 and snapshot2 bounds |
|---|---:|---:|---:|---|
| `js-medium-express` | 214 | 717115 | 27305 | yes |
| `poly-medium-napi-rs` | 644 | 11675794 | 88420 | yes |
| `ts-medium-powertools-lambda` | 1389 | 7818881 | 206175 | yes |
| `ts-medium-smithy-typescript` | 2315 | 11541863 | 381452 | yes |
| `ts-medium-umami` | 2026 | 9083336 | 283572 | yes |
| `ts-medium-vite` | 2836 | 17644692 | 419807 | yes |

**SM-8** (D-6; U-4a): the longest single public compiler call, in ms.

| Row | Source | Median | Max | Call |
|---|---|---:|---:|---|
| `poly-medium-napi-rs` | s-m-ts-cohort-2026-10-09 | 105.7 | 114.7 | createProgram |
| `ts-medium-powertools-lambda` | s-m-ts-cohort-2026-10-09 | 125.4 | 130.3 | createProgram |
| `ts-medium-smithy-typescript` | s-m-ts-cohort-2026-10-09 | 209.6 | 216.3 | getSemanticDiagnostics |
| `ts-medium-umami` | s-m-ts-cohort-2026-10-09 | 250.2 | 258.2 | createProgram |
| `ts-medium-vite` | s-m-ts-cohort-2026-10-09 | 198.9 | 206.1 | getSemanticDiagnostics |
| `js-medium-express` | s-m-ts-synthesized-2026-10-10 | 106.6 | 109.9 | createProgram |

Label: driver call granularity: createProgram per configuration, getSemanticDiagnostics per file; a provider calling program-wide would block longer (label for the D law liveness floor).

**SM-10** (U-4b): the `wait4` peak RSS per process, for every row, component and reset. There are 152 current entries, unique by language,row,component,reset,entryChild, plus 2 informational entries. All are in `otherFigures.SM10`. The values are information only, in native bytes with checked conversion. For SM-4 the value is the largest compiler child per run, and R8 is given per entry and as the larger of the two.

**SM-11** (U-4b; U-7): SM-4's time and SM-10's peak, labelled by covered units. **No quotient is recorded for any workload** (0). Every medium row's covered units include dependency crates, and all but hyper also miss first-party units (`otherFigures.SM11.medium`). Large-workload coverage: rs-large-smithy-rs 13 of 1084 subjects with sites; poly-very-large-deno 1 of 1052 subjects with sites. poly-large-rspack and rs-very-large-sui have no analysed entry.

**SM-12** (accepted, `s-m-rust-scope-2026-10-09`, plus `s-m-sui-scope-series-2026-10-10`): rebuilding the Rust subject scope.
- **Measurement.** Time is the reconstruction/commitment/array-CBOR span after input parsing. Memory is whole-process wait4 RSS, native bytes (macOS) with identity conversion; process peak, not incremental algorithm heap accounting (D-8).
- **Worker prototype.** The worker-prototype is a separate process repeating the second implementation; not the operational native worker.
- **Still owed.** domainCommitment with bound keys and the worker derivation wait for the completion round.

Times in ms, median and max of 7; peak RSS in bytes.

| Workload | S | Actor | Median | Max | Peak RSS bytes | Arrays and commitments equal |
|---|---:|---|---:|---:|---:|---|
| `poly-medium-napi-rs` | 239 | host-a | 3.0 | 3.0 | 25935872 | yes |
| `poly-medium-napi-rs` | 239 | host-b | 5.9 | 5.9 | 26312704 | yes |
| `poly-medium-napi-rs` | 239 | worker-prototype | 5.9 | 5.9 | 26312704 | yes |
| `rs-medium-aws-lambda-rust-runtime` | 192 | host-a | 2.4 | 2.4 | 25870336 | yes |
| `rs-medium-aws-lambda-rust-runtime` | 192 | host-b | 4.9 | 4.9 | 26279936 | yes |
| `rs-medium-aws-lambda-rust-runtime` | 192 | worker-prototype | 4.9 | 4.9 | 26279936 | yes |
| `rs-medium-axum` | 301 | host-a | 3.7 | 3.8 | 25968640 | yes |
| `rs-medium-axum` | 301 | host-b | 7.1 | 7.1 | 26312704 | yes |
| `rs-medium-axum` | 301 | worker-prototype | 7.1 | 7.2 | 26312704 | yes |
| `rs-medium-hyper` | 98 | host-a | 1.2 | 1.2 | 25591808 | yes |
| `rs-medium-hyper` | 98 | host-b | 2.9 | 2.9 | 25935872 | yes |
| `rs-medium-hyper` | 98 | worker-prototype | 2.9 | 3.0 | 25952256 | yes |
| `rs-medium-serde` | 208 | host-a | 2.6 | 2.6 | 25772032 | yes |
| `rs-medium-serde` | 208 | host-b | 5.2 | 5.2 | 26165248 | yes |
| `rs-medium-serde` | 208 | worker-prototype | 5.2 | 5.2 | 26198016 | yes |
| `rs-medium-serde-json` | 71 | host-a | 0.9 | 0.9 | 25559040 | yes |
| `rs-medium-serde-json` | 71 | host-b | 1.4 | 1.4 | 25886720 | yes |
| `rs-medium-serde-json` | 71 | worker-prototype | 1.4 | 1.5 | 25886720 | yes |
| `rs-medium-tokio` | 808 | host-a | 9.9 | 10.0 | 26607616 | yes |
| `rs-medium-tokio` | 808 | host-b | 17.5 | 19.0 | 27000832 | yes |
| `rs-medium-tokio` | 808 | worker-prototype | 17.4 | 17.5 | 26968064 | yes |
| `rs-large-smithy-rs` | 1084 | host-a | 13.4 | 13.5 | 29310976 | yes |
| `rs-large-smithy-rs` | 1084 | host-b | 22.9 | 23.1 | 29720576 | yes |
| `rs-large-smithy-rs` | 1084 | worker-prototype | 22.9 | 23.1 | 29622272 | yes |
| `poly-large-rspack` | 1384 | host-a | 17.7 | 17.9 | 50380800 | yes |
| `poly-large-rspack` | 1384 | host-b | 30.4 | 30.7 | 50806784 | yes |
| `poly-large-rspack` | 1384 | worker-prototype | 30.4 | 30.7 | 50823168 | yes |
| `poly-very-large-deno` | 1052 | host-a | 13.2 | 13.3 | 40009728 | yes |
| `poly-very-large-deno` | 1052 | host-b | 22.8 | 22.9 | 40452096 | yes |
| `poly-very-large-deno` | 1052 | worker-prototype | 22.9 | 23.1 | 40435712 | yes |
| `mr-rs-medium-serde-json` | 279 | host-a | 3.5 | 3.5 | 25853952 | yes |
| `mr-rs-medium-serde-json` | 279 | host-b | 6.7 | 6.7 | 26312704 | yes |
| `mr-rs-medium-serde-json` | 279 | worker-prototype | 6.6 | 6.7 | 26329088 | yes |
| `rs-very-large-sui` | 3318 | host-a | 40.0 | 40.5 | 48922624 | yes |
| `rs-very-large-sui` | 3318 | host-b | 67.6 | 68.8 | 50511872 | yes |
| `rs-very-large-sui` | 3318 | worker-prototype | 67.9 | 68.7 | 50511872 | yes |
| `rs-very-large-sui` | 3318 | closed-rust-helper | 16.5 | 17.0 | 38207488 | yes |

D-8: "the accepted manifest" is the T2 corpus manifest (`c8cc48e1…`).

**SM-13** (a decomposition, not a value: sites, not candidates; owned parameters unset): census v2 (`s-m-rust-site-census-v2-2026-10-13`) and U-7 (`s-m-large-site-census-2026-10-13`).

Fixed bytes per candidate, by relation@rung:

| Relation@rung | Candidate fixed bytes |
|---|---:|
| declares@syntactic | 347 |
| literal@syntactic | 345 |
| control-flow@syntactic | 355 |
| imports@resolved-target | 353 |
| references@resolved-binding | 360 |
| calls@resolved-callee | 349 |
| types@checked | 341 |
| reachability@from-resolved-calls | 366 |
| clones@normalized-body-hash | 355 |
| clones@near (candidate only) | 334 |
| unresolved-edge@observed | 362 |

The other fixed parts:
- (b) spool entry: 35 bytes;
- (c) envelope 78, FactBatch V2 47 or V3 82, occupancy companion 140;
- (d) 40 bytes of transport prefix per frame;
- (e) census row 61, complete container 35.

The formulas (a) to (e) are in `otherFigures.SM13.fixedBytes`, with these parameters unset: G3: emission factor per site kind, census symbol kinds, batching, confidence, targetUniverseId, relation payload, anchors per candidate; C4a: stage grouping, stageId, requested keys K_stage; release: producerVersion. Site totals (first-party / dependency crates) are labelled sites, not candidates:
- `poly-medium-napi-rs` (ord 0): 3073 / 764215
- `rs-medium-aws-lambda-rust-runtime` (ord 1): 0 / 531149
- `rs-medium-axum` (ord 2): 45763 / 292259
- `rs-medium-hyper` (ord 3): 3707 / 104105
- `rs-medium-serde` (ord 4): 0 / 41274
- `rs-medium-serde-json` (ord 5): 0 / 23662
- `rs-medium-tokio` (ord 6): 11 / 93154
- `mr-rs-medium-serde-json` (ord 7): 0 / 41274
- `mr-rs-medium-serde-json` (ord 8): 0 / 23662
- `rs-large-smithy-rs`: 7103 / 9087367
- `poly-very-large-deno`: 152 / 57360

**SM-14:** the formula `SM-14 = Σ_stages S_stage × K_stage; S per workload exact (census r1/v2, RUST3-LIM); K_stage unset (C4a)`. S is exact per workload (`otherFigures.SM14.S`), and K_stage is unset (C4a).

**S_eff** (D-9; U-4a): the first term is snapshot2's admitted rows, from SM-5, for all 12 Rust workloads. It is not filled.

| Workload | Rows | Total bytes | Descriptor bytes | Within all bounds |
|---|---:|---:|---:|---|
| `poly-medium-napi-rs` | 644 | 11675794 | 88420 | yes |
| `rs-medium-aws-lambda-rust-runtime` | 567 | 2446357 | 86122 | yes |
| `rs-medium-axum` | 498 | 1968335 | 71338 | yes |
| `rs-medium-hyper` | 138 | 1447837 | 17039 | yes |
| `rs-medium-serde` | 347 | 1331295 | 50946 | yes |
| `rs-medium-serde-json` | 92 | 737131 | 11578 | yes |
| `rs-medium-tokio` | 883 | 6256646 | 116528 | yes |
| `mr-rs-medium-serde-json` | 439 | 2068426 | 69635 | yes |
| `poly-large-rspack` | 23980 | 69293473 | 4085164 | yes |
| `poly-very-large-deno` | 14920 | 93725209 | 2227549 | yes |
| `rs-large-smithy-rs` | 3632 | 51487333 | 647602 | yes |
| `rs-very-large-sui` | 19063 | 203261240 | 3509292 | yes |

Under D-2, the dependency-source part (the SM-5 table above) is reported beside this term, not added to it. The other terms of S_eff remain formulas.

## 5. Large workloads (§3a; no outcome depends on them)

Per-entry outcomes with exact reasons are in `docs/implementation/m3/spikes/s-m-large-site-census-2026-10-13/large-workload-entry-coverage.md`.

| Workload | S | Analysed entries | Subjects with sites | S_eff first term (rows; descriptor bytes) |
|---|---:|---:|---:|---|
| `rs-large-smithy-rs` | 1084 | [{'ordinal': 9, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-large-owned-corpus-8d62e4ic/rs-large-smithy-rs/rust-runtime/aws-smithy-eventstream/fuzz', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}, {'ordinal': 16, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-large-owned-corpus-8d62e4ic/rs-large-smithy-rs/rust-runtime/aws-smithy-types/fuzz', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}, {'ordinal': 12, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-large-owned-corpus-8d62e4ic/rs-large-smithy-rs/rust-runtime/aws-smithy-http/fuzz', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}, {'ordinal': 0, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-large-owned-corpus-8d62e4ic/rs-large-smithy-rs/aws/rust-runtime', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}, {'ordinal': 18, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-large-owned-corpus-8d62e4ic/rs-large-smithy-rs/tools/ci-build/changelogger', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}, {'ordinal': 19, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-large-owned-corpus-8d62e4ic/rs-large-smithy-rs/tools/ci-build/crate-hasher', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}, {'ordinal': 20, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-large-owned-corpus-8d62e4ic/rs-large-smithy-rs/tools/ci-build/publisher', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}, {'ordinal': 21, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-large-owned-corpus-8d62e4ic/rs-large-smithy-rs/tools/ci-build/runtime-versioner', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}, {'ordinal': 22, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-large-owned-corpus-8d62e4ic/rs-large-smithy-rs/tools/ci-build/sdk-versioner', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}, {'ordinal': 23, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-large-owned-corpus-8d62e4ic/rs-large-smithy-rs/tools/ci-build/smithy-rs-tool-common', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}] | 13 | 3632; 647602 |
| `poly-very-large-deno` | 1052 | [{'ordinal': 26, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-large-owned-corpus-8d62e4ic/poly-very-large-deno/tests/specs/node/child_process_extra_pipes/test-pipe', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}, {'ordinal': 27, 'cwd': '/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-ds-tlzerj_a/p/tests/sqlite_extension', 'acceptedPilotPopulationRepeated': True, 'siteCountsDeterministic': True}] | 1 | 14920; 2227549 |
| `poly-large-rspack` | 1384 | 0 | — | 23980; 4085164 |
| `rs-very-large-sui` (if S-P permits) | 3318 | 0 | — | 19063; 3509292 |

The causes are in the coverage record:
- rspack: both entries are refused by the pinned stable compiler (nightly-only `-Z` flags).
- sui: two Git dependencies cannot be checked out offline, and its bin source is an excluded symlink.
- deno: the root descriptor (22,825,382 bytes) is over the closed driver's bound.
- smithy-rs: 15 of its 25 entries are unavailable.

## 6. Standing and what this report does not do

- **Preliminary.** These are the lead's macOS host figures, not D12's. The targets are held on the D12 runner.
- **Conditional.** F, T and every outcome depend on D-1's synthetic SM-9.
- **Not filled.** No `⟨SM-n⟩` placeholder is filled in L. SM-11's quotients, SM-13's values, SM-14's values, S_eff, the worker's scratch and `domainCommitment` wait for the completion round (item 9, r6).
- **Not changed.** L, the closed drivers, executors, observers and generators, and every accepted record are unchanged. No G3 or C4a parameter is chosen.
- **Still open.** Full S-M closes at the S-M delta round. L-G1, effective L, native admission and worker, K1 and qualification remain open.
