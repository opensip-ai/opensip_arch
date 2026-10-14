# S-M gap inventory against M3-L r6 item 9 (2026-10-13)

**Standing.** Read-only research note by the lead's research agent. It is not law, it fills no `⟨SM-n⟩` placeholder, and it derives no F, T or outcome. Every number below is either quoted from an accepted spike record (cited by path and line) or, where marked **DERIVED (not accepted)**, recomputed read-only from that record's retained raw data. A derived number is an inventory aid, never an S-M figure (PROPOSAL-r6:620, :623).

**Pins.** Architecture repo `opensip_arch` at `a208594fe` (2026-10-13). Paths below are relative to `docs/implementation/m3/` unless absolute.

- Law: `provider-protocol-l/PROPOSAL-r6.md` item 9, lines 540-629 (workloads :549, statistic :550, host :551, figure table :553-568, SM-11..14 workloads :571, two-part rule :579-603, derived F/T :605-607, outcomes :609-613, forbidden substitutes :622-629).
- T2 manifest: `corpus/t2-corpus-manifest.draft.json` (Rust medium `devIds` :426-434, TS/JS medium `devIds` :488-495, overlay workspace `mr-rs-medium-serde-json` :7753-7768).
- Q0 resets: `harness/DESIGN.md:796-807` (§9.2 cold/warm).
- Control register: `/Users/sb/code/.opensip-implementation-cache/control-2026-10-06/SM-DELIVERABLES.json`. **It is stale.** Its `authority` is PROPOSAL-r5, and its rows do not list the accepted 2026-10-10/11 actual series (analysis timing, framed analysis, static profile, map transfer, context series, large-workspace data, Smithy/Deno series). Its SM-7 row ("Add Rust dependency-source set and multiworkspace overlay") is partly overtaken by `spikes/s-m-actual-map-transfer-series-2026-10-10`.
- Review standing: every `spikes/s-m-*` directory has a final ACCEPT review under `reviews/` (Grok, or Codex r2 for the site census). Two earlier rounds were REQUIRED-FINDINGS and were superseded: `reviews/grok-sm-sealing-typed-remaining-r1` and `reviews/codex-sm-rust-site-census-r1`.

---

## 0. Headline findings

1. **F cannot be computed for any workload from accepted values.** SM-9 exists for one synthetic population only: 193 sources, sized from the napi-rs TypeScript cohort (`spikes/s-m-full-replay-partial-2026-10-09/native/REPORT.md:5-11`). No other workload has a sized replay. That one population also has three different timed boundaries (Python reference, native debug, native release), and no decision says which one is SM-9.
2. **The napi-rs TypeScript row is one decision away from a computable F and T.** The replay population is exactly napi's 193 distinct configured TS files (`spikes/s-m-ts-cohort-2026-10-09/REPORT.md:16`). It is computable only if the lead records that (i) this graph is "the size SM-2 implies" for napi-TS and (ii) the native release `replay_run` is the SM-9 boundary. See §3.
3. **Rust SM-4 barely covers first-party code.** The site census (`spikes/s-m-rust-site-census-2026-10-13/REPORT.md:33-43`) and a derived split of the analysis-timing series (§2, SM-4) show four workloads with zero first-party units analysed: lambda, serde, serde-json and the overlay. In the other four, the analysed first-party unit is small: napi `napi_build`, axum `axum_core`, hyper `hyper` (default features only) and tokio `tests_build`. Almost all accepted Rust analysis time is spent in dependency crates.
4. **The SM-13 census misses four relation@rungs.** NE's table has rust-cargo cells for `literal@syntactic`, `control-flow@syntactic`, `reachability@from-resolved-calls` and `clones` mode `near`. The census groups only 7 relation@rungs (`site-census-checks-r1.json` `offeredRelationGrouping`). The fixed-bytes and closed-formula parts of SM-13, and the SM-14 formula, are not in any accepted record.
5. **TS SM-2 already exceeds the 8 s warm target on two workloads.** The accepted cohort medians are smithy-typescript 16.30 s and vite 8.06 s. If the lead adopts these as SM-2, T_warm > 8 s follows for those rows whatever F is. The cohort over-counts (overlapping configs) and under-resolves (no dependencies), so adopting it is a lead decision, not a fact.
6. **No accepted run carries a Q0 §9.2 reset label.** No record captures page-cache state (cold) or a priming slot (warm). Every record says "no cold reset claimed" (for example `spikes/s-m-transfer-2026-10-09/REPORT.md:9`, `spikes/s-m-ts-cohort-2026-10-09/REPORT.md:12`).

---

## 1. Exact workload list

### 1.1 Item 9 workloads, used by SM-1..SM-10, F and T (PROPOSAL-r6:549)

| Language | # | Workload id | Source | Notes |
|---|---|---|---|---|
| Rust | R1 | `poly-medium-napi-rs` | T2M :427 | polyglot, counted in both languages |
| Rust | R2 | `rs-medium-aws-lambda-rust-runtime` | T2M :428 | |
| Rust | R3 | `rs-medium-axum` | T2M :429 | |
| Rust | R4 | `rs-medium-hyper` | T2M :430 | |
| Rust | R5 | `rs-medium-serde` | T2M :431 | |
| Rust | R6 | `rs-medium-serde-json` | T2M :432 | |
| Rust | R7 | `rs-medium-tokio` | T2M :433 | |
| Rust | R8 | `mr-rs-medium-serde-json` | T2M :7754 (members `rs-medium-serde`, `rs-medium-serde-json`) | workspace added by PROPOSAL-r6:549 |
| TS/JS | T1 | `js-medium-express` | T2M :489 | no tsconfig/jsconfig |
| TS/JS | T2 | `poly-medium-napi-rs` | T2M :490 | same tree as R1 |
| TS/JS | T3 | `ts-medium-powertools-lambda` | T2M :491 | |
| TS/JS | T4 | `ts-medium-smithy-typescript` | T2M :492 | |
| TS/JS | T5 | `ts-medium-umami` | T2M :493 | |
| TS/JS | T6 | `ts-medium-vite` | T2M :494 | |

Excluded held-out entries: `poly-medium-tauri` and `rs-medium-ripgrep` (Rust), `js-medium-axios` (TS).

**Row count.** Item 9 gives 8 Rust rows and 6 TS rows, 14 F/T rows in all. They cover 13 distinct read sets: 12 repositories plus the overlay.

**Overlay entry split.** Every accepted Rust graph series runs the overlay as **two Cargo workspace entries**:
- ordinal 7, cwd `…/mr-rs-medium-serde-json/rs-medium-serde`;
- ordinal 8, cwd `…/mr-rs-medium-serde-json/rs-medium-serde-json`.

This split is in `spikes/s-m-actual-static-profile-series-2026-10-10/initial-nine-command-pilots/actual-command-source-maps-r1.json`, `results[7..8].cwd`. Each entry's map holds the whole overlay (441 files) plus that entry's own registry sources. No accepted rule combines entries 7 and 8 into one overlay figure for SM-4 or SM-7.

### 1.2 Additional workloads for SM-11..SM-14 (PROPOSAL-r6:571)

| # | Workload id | RUST3-LIM S | Standing |
|---|---|---|---|
| L1 | `rs-large-smithy-rs` | 1,084 | dev, large |
| L2 | `poly-large-rspack` | 1,384 | dev, large |
| L3 | `poly-very-large-deno` | 1,052 | dev (selected through its large per-language bucket) |
| L4 | `rs-very-large-sui` | 3,318 | "if S-P permits" |

---

## 2. Per-figure inventory (SM-1..SM-14)

### 2.1 Summary table

Key: ✓ = an accepted value at 3 warmups + 7 runs, with median and max; ◐ = partial; ✗ = none. "Every row" means the figure is workload-independent: the start figures are one per language, measured once, and apply to every row of that language.

| SM | Item 9 requires (PROPOSAL-r6 line) | Accepted supplier(s) | Coverage (14 rows) | Precise gap |
|---|---|---|---|---|
| SM-1 | TS start, fresh Node from pinned closure, TS loaded, request-ready (:555) | `spikes/s-m-sm1-ready-closure-2026-10-09` (REPORT:3): median 81.849083 ms, max 83.380958 ms; review `grok-sm1-ready-r1` `SM1FigureComplete:true` | ✓ every TS row (T1-T6) | None for the S-M report. Placeholder not filled, which is lawful until the delta round. |
| SM-2 | TS fresh-process Program + full semantic pass over the repository (:556) | `s-m-ts-cohort-2026-10-09` (REPORT:15-20) for all 6; `s-m-ts-synthesized-2026-10-10` (REPORT:9) for express; `s-m-foundation-2026-10-09` (REPORT:9) root-only for smithy-ts and umami | ◐ all 6 have a 3+7 value | Boundary is exploratory "every tsconfig", overlapping, with incomplete configs. No dependency tree, so missing types. Span includes Node start and map preparation, so it double-counts SM-1 in T. Express is covered only by the supplementary synthesized program. |
| SM-3 | Rust sidecar callback-ready (:557) | `s-m-sm3-ready-2026-10-09` (REPORT:3): median 8.687583 ms, max 8.914583 ms; `grok-sm3-ready-r2` `SM3FigureComplete:true` | ✓ every Rust row (R1-R8) | None for the S-M report. |
| SM-4 | Rust analysis through typecheck; build-script/proc-macro expansion disclosed unavailable (:558) | `s-m-actual-analysis-timing-series-2026-10-10` (REPORT:9-17); `s-m-actual-framed-analysis-series-2026-10-10` (REPORT:9-17); `s-m-actual-static-profile-series-2026-10-10` (REPORT:17-25); `s-m-remaining-context-series-2026-10-10`; older `s-m-rust-typecheck-2026-10-09` (REPORT:17-24) | ◐ all 8 have a 3+7 value | First-party coverage: zero units for R2, R5, R6, R8; one small unit for R1, R3, R4, R7. Test, example and bench targets are not in any graph. No selected series or span (summed per-unit interval or whole graph). No rule combines the two overlay entries. |
| SM-5 | Seal read set: enumerate, SHA-256, snapshot2/plan2-equivalent digests; rows, bytes, descriptor bytes vs bounds (:559) | `s-m-sealing-typed-2026-10-09` (REPORT:7-21), all 13 read sets; `s-m-sealing-typed-remaining-2026-10-11` (REPORT:7-29), the large sets | ✓ TS (repository-only; T2 pins no dependency tree); ◐ Rust | Rust dependency-source sets are absent from the read set and the plan2-equivalent (`dependencySourceSetsIncluded:false`). Plan fields are public synthetic template values. Overlay configuration not captured. Record says `SM5FigureComplete:false`. |
| SM-6 | TS read-set size vs TS2 and snapshot2 bounds; repository-only labelled if T2 pins no deps (:560) | `s-m-sm6-readset-2026-10-09` (REPORT:11-20); `grok-sm6-readset-r1` `SM6FigureComplete:true` | ✓ T1-T6 | None. |
| SM-7 | Stream sealed set plus Rust dependency-source set, ≤1 MiB frames, once per child (:561) | TS and Rust repository-only: `s-m-transfer-2026-10-09` (REPORT:11-24). Rust repository plus graph-expanded dependencies: `s-m-actual-map-transfer-series-2026-10-10` (REPORT:7-17). Axum lock-wide dependency-only: `s-m-dependency-fragment-2026-10-09` (`fragment/metrics.json`) | ✓ TS; ◐ Rust R1-R7; ✗ R8 as one child | Rust maps carry graph-expanded registry sources, not the lock-wide dependency-source set (axum: 150 packages / 5,905 files in the map vs 187 / 7,338 in the accepted dependency-source descriptor). R8 transferred only as two separate per-entry maps. |
| SM-8 | Longest single synchronous compiler call inside SM-2 (:562) | Raw per-config `maxPublicCompilerCall` in `s-m-ts-cohort-2026-10-09/evidence/*.stdout.json` and `s-m-ts-synthesized-2026-10-10/evidence` | ◐ raw data for all 6; no accepted statistic | No accepted SM-8 statistic and no definition. Wrapped public-call maxima are declared "not all internal calls or whole event-loop blocks" (ts-cohort REPORT:12). §2.2 gives derived values. |
| SM-9 | Complete replay (IE:1580-1592) over a synthetic graph of the size SM-2/SM-4 imply (:563) | `s-m-full-replay-partial-2026-10-09/native/REPORT.md:9-11`: 193-source graph. Reference median 14,689.338 ms; native debug 23,295.959 ms; native release 1,838.605 ms (max 1,859.721 ms) | ◐ T2 (napi-TS) only, conditionally; ✗ the other 13 rows | No per-workload sized graphs. No sizing rule. No choice of replay boundary. Report says "does not close SM9" (:5). |
| SM-10 | Per-process `ru_maxrss`, native unit labelled, checked byte conversion (:564) | Every accepted run records `rssNative` / `rss_native`, macOS bytes with identity conversion | ◐ raw for all rows | No consolidated SM-10 table per F/T component. Rust analysis RSS is per-unit compiler child, not a provider process. |
| SM-11 (S-M part) | Exact S; SM-4 time and SM-10 RSS labelled with covered units; quotient only when coverage is exact (:587) | S: `s-m-rust-site-census-2026-10-13` (REPORT:33-43) for R1-R8; `s-m-rust-scope-2026-10-09` (REPORT:9-43) for L1-L3; `s-m-sui-scope-series-2026-10-10` for L4 (3,318). Unit-level times and RSS in the analysis-timing raw data | ◐ S ✓ for all 12 workloads; labelled SM-4/SM-10 ✗ | No accepted record labels SM-4/SM-10 with covered units. Coverage is exact nowhere, so no quotient, which is lawful. Large workloads: partial SM-4 only (Smithy 10 of 25 entries, Deno 2 of 3, Rspack none, Sui none). |
| SM-12 (S-M part) | Host's two independent derivations of subject array and `commitments.subjectScope`, time and peak memory (:588) | `s-m-rust-scope-2026-10-09` (REPORT:9-43): host-a and host-b, 3+7, 11 workloads; `s-m-sui-scope-series-2026-10-10` (REPORT:7-31) | ✓ R1-R8 and L1-L4 | Peak memory is whole-process wait4 RSS, not algorithm memory; acceptable only with that label (lead call). "Accepted manifests" is ambiguous: T2 manifest (as used) vs accepted SnapshotManifest (`s-m-manifest-scope-2026-10-09`, worker side only). `domainCommitment` uses an illustrative key, which is lawful: it is deferred. |
| SM-13 (S-M part) | Per rust-cargo relation@rung: (1) site counts with query named, labelled sites; (2) exact fixed bytes per candidate, frame and census row from schemas and RPP `candidateSpoolAccounting`; (3) closed formulas (a)-(e) with unset owners (:589) | `s-m-rust-site-census-2026-10-13` (Codex r2 ACCEPT): sites per relation for R1-R8, first-party covered subjects only | ◐ part (1) for R1-R8 over 7 of 11 relation rows; ✗ parts (2) and (3); ✗ L1-L4 | Missing relation@rungs: `literal@syntactic`, `control-flow@syntactic`, `reachability@from-resolved-calls`, `clones` mode `near` (NE:592, :597, :599). No site-kind-to-query table. No fixed bytes. No formulas. No large-workload census. Sites are zero for R2, R5, R6, R8 (no first-party unit analysed). |
| SM-14 (S-M part) | Formula Σ S_stage × K_stage, S exact, K unset (C4a) (:590) | S as for SM-11 | ◐ S ✓; formula ✗ | Desk record only: write the formula with per-workload S and K_stage unset (owner C4a). |
| S_eff first term | snapshot2 admitted rows, from SM-5 (:591) | Rows and descriptor bytes in the sealing records | ◐ data ✓, record ✗ | Not recorded anywhere. "Admitted rows" needs a reading: the workload's rows if within bounds, or the bound-implied ceiling (100,000 rows; about 27,000 under 4 MiB). |

### 2.2 Per-figure detail and per-workload coverage

#### SM-1: TS start
- **Accepted figure.** `spikes/s-m-sm1-ready-closure-2026-10-09/REPORT.md:3`: Node 24.16.0 with TS 6.0.3 from a 142-file pinned runtime, 3 warmups + 7 runs, median 81.849083 ms, max 83.380958 ms. Review `reviews/grok-sm1-ready-r1/review.json`: `SM1FigureComplete:true`.
- **Earlier observations, not the figure.**
  - Foundation, Node 24.21 prototype: 80.610959 ms (`s-m-foundation-2026-10-09/REPORT.md:7`).
  - Product-version pinned startup: 79.832250 ms (`s-m-transfer-2026-10-09/REPORT.md:32`).
- **Coverage.** One figure for every TS row. **Gap: none.**

#### SM-2: TS analysis
Source: `spikes/s-m-ts-cohort-2026-10-09/REPORT.md:15-20` (whole-process spans, 3 warmups + 7 runs).

| Row | Median ms | Max ms | Configs (incomplete) | Distinct configured files | Other accepted values |
|---|---:|---:|---|---:|---|
| T1 express | 92.757 (initialization only, no analysis) | 93.573 | 0 | 0 | Synthesized program (`s-m-ts-synthesized-2026-10-10/REPORT.md:5,9`): 257.128 / 259.057 ms; 141 roots, 204 Program files, 0 diagnostics (checkJs false) |
| T2 napi-rs | 1,026.995 | 1,038.700 | 8 (2) | 193 | |
| T3 powertools | 3,465.558 | 3,547.487 | 51 (2) | 936 | |
| T4 smithy-ts | 16,295.809 | 16,368.381 | 230 (4) | 1,159 | Root tsconfig only (foundation REPORT:9): 847.376 ms |
| T5 umami | 2,302.595 | 2,317.559 | 7 (1) | 1,381 | Root tsconfig only: 1,719.613 ms |
| T6 vite | 8,059.187 | 8,139.471 | 55 (18) | 678 | |

**Gaps.**
- (a) **No selected repository Program boundary.** The cohort is every `tsconfig*.json` basename, overlapping (REPORT:7). Shared files are re-checked per config, so the sum over-states one whole-repository pass. Incomplete configs under-state it.
- (b) **Missing dependency types.** T2 pins no `node_modules` tree (results `dependencyTreePinned:false`). That is lawful, but it must be labelled.
- (c) **Span definition.** The whole-process span includes Node/TS load (SM-1) and sealed-map preparation (REPORT:11), so T = F + SM-2 double-counts start. Per-config `elapsedNanos` are retained in `evidence/*.stdout.json`, so an analysis-only span is derivable without new runs.
- (d) **Express.** Only the supplementary synthesized-options recipe supplies an analysis (`s-m-ts-synthesized-2026-10-10/REPORT.md:3-5`). Its standing as "the" express SM-2 needs a lead decision.

#### SM-3: Rust start
- **Accepted figure.** `spikes/s-m-sm3-ready-2026-10-09/REPORT.md:3`: median 8.687583 ms, max 8.914583 ms. Review `reviews/grok-sm3-ready-r2`: `SM3FigureComplete:true`.
- **Coverage.** Every Rust row. **Gap: none.**
- **Caveat for T.** The accepted SM-4 series launch one fresh compiler child per unit. A one-shot Rust3 sidecar's per-unit start is not SM-3. The lead must state how per-unit child start enters T (see SM-4).

#### SM-4: Rust analysis
All values are 3 warmups + 7 runs, in ms.

| Row | Entry | Analyses/run | Summed instrumented analysis, median / max (analysis-timing REPORT:9-17) | Whole graph, static profile (static-profile REPORT:17-25) | Whole graph, package context (`remaining-context-series`) | First-party units analysed / unavailable (census REPORT:35-43) | **DERIVED** first-party-only summed analysis, median |
|---|---|---:|---|---:|---:|---|---|
| R1 napi | 0 | 66 | 2,488.600 / 2,493.965 | 8,069.737 | 8,036.631 | 1 / 41 | 23.779 (`napi_build`) |
| R2 lambda | 1 | 48 | 1,831.740 / 1,838.503 | 5,349.709 | 5,373.543 | 0 / 8 | 0 |
| R3 axum | 2 | 32 | 1,786.885 / 1,887.742 | 4,061.596 | 3,920.591 | 1 / 3 | 363.011 (`axum_core`) |
| R4 hyper | 3 | 7 | 507.936 / 515.384 | 738.522 | 731.949 | 1 / 0 | 40.594 (`hyper`) |
| R5 serde | 4 | 2 | 22.600 / 22.821 | 69.862 | 64.823 | 0 / 12 | 0 |
| R6 serde-json | 5 | 2 | 97.269 / 98.072 | 140.140 | 140.854 | 0 / 3 | 0 |
| R7 tokio | 6 | 16 | 390.312 / 392.214 | 1,226.191 | 1,202.608 | 1 / 8 | 4.411 (`tests_build`) |
| R8 overlay | 7 | 2 | 22.491 / 22.746 | 72.280 | 71.741 | 0 / 12 | 0 |
| R8 overlay | 8 | 2 | 97.110 / 104.882 | 141.990 | 141.020 | 0 / 6 | 0 |

The framed series (`s-m-actual-framed-analysis-series-2026-10-10/REPORT.md:9-17`) gives same-child framed values within about 3% of the summed column.

The derived first-party column is from `actual-analysis-timing-samples-r1.json`. Units are joined to `original-graph-data/<n>.json`, and `pkg_id` not `registry+…` counts as first-party.

**Why first-party units are unavailable (DERIVED).** This is a read-only classification of `original-graph-data/<n>.json` units. "BS-only" means a first-party **library** unit whose only blocking edges, direct or transitive, are build-script compile/run units. A first-party unit that is itself a build-script, proc-macro or bin/test target is counted separately.

| Row | BS-only library units | Other first-party units |
|---|---|---|
| R1 napi | 3: `napi_derive_backend` ×2, `napi_sys` | 11 libraries also blocked by proc-macros; 24 build-script units; 2 proc-macro crates; 1 binary; 1 available |
| R2 lambda | 0 | 5 libraries blocked by dependency proc-macros and build scripts; 3 bin targets |
| R3 axum | 2: **`axum`**, `axum_extra` | 1 proc-macro crate (`axum-macros`); 1 available (`axum_core`) |
| R4 hyper | 0 | 1 available (`hyper`) |
| R5 serde | 3: **`serde`**, `serde_core`, `serde_derive_internals` | 8 build-script units; 1 proc-macro crate (`serde_derive`) |
| R6 serde-json | 1: **`serde_json`** | 2 build-script units |
| R7 tokio | 0 | 5 libraries, including the `tokio` library, blocked through `tokio-macros`; 2 proc-macro crates; 1 binary; 1 available (`tests_build`) |
| R8 entry 7 | 3: `serde`, `serde_core`, `serde_derive_internals` | 8 build-script units; 1 proc-macro crate |
| R8 entry 8 | 2: `serde_core`, `serde_json` | 4 build-script units |

The main libraries of axum, serde and serde_json are blocked only by build-script edges.

**Gaps.**
- (a) **First-party coverage.** Coverage is far from "the repository". Build-script-only blocks could lawfully be analysed with the build-script expansion disclosed as unavailable, as PROPOSAL-r6:558 words it, but the closed executor marks them unavailable before launch.
- (b) **Targets not in the graphs.** Test, example and bench targets are in no graph. So even hyper, with 0 first-party units unavailable, covers only 18 of its 98 subjects (census `subjectCoverage` 0.1837).
- (c) **No selected series or span.** Summed instrumented intervals exclude per-child start and map decode. Whole-graph spans include hashing, dispatch and per-unit child start.
- (d) **No overlay combination rule** for entries 7 and 8.

The older direct-library cohort (`s-m-rust-typecheck-2026-10-09/REPORT.md:17-24`) is superseded in coverage and has only 7 of 48 roots successful.

#### SM-5: Sealing
Source: `s-m-sealing-typed-2026-10-09/REPORT.md:7-21` (3 warmups + 7 runs, ms).

| Row(s) | Rows | Source bytes | Descriptor bytes | Median ms | Max ms |
|---|---:|---:|---:|---:|---:|
| T1 express | 214 | 717,115 | 27,305 | 6.890541 | 7.077583 |
| R1/T2 napi | 644 | 11,675,794 | 88,420 | 23.218750 | 23.350958 |
| R2 lambda | 567 | 2,446,357 | 86,122 | 19.475667 | 19.733584 |
| R3 axum | 498 | 1,968,335 | 71,338 | 17.446042 | 17.713125 |
| R4 hyper | 138 | 1,447,837 | 17,039 | 4.719250 | 4.864958 |
| R5 serde | 347 | 1,331,295 | 50,946 | 11.043250 | 11.481250 |
| R6 serde-json | 92 | 737,131 | 11,578 | 2.948458 | 2.990458 |
| R7 tokio | 883 | 6,256,646 | 116,528 | 27.853375 | 28.274500 |
| R8 overlay | 439 | 2,068,426 | 69,635 | 13.844417 | 14.332042 |
| T3 powertools | 1,389 | 7,818,881 | 206,175 | 45.720167 | 46.150125 |
| T4 smithy-ts | 2,315 | 11,541,863 | 381,452 | 80.098750 | 80.843958 |
| T5 umami | 2,026 | 9,083,336 | 283,572 | 66.081375 | 66.752750 |
| T6 vite | 2,836 | 17,644,692 | 419,807 | 102.498958 | 102.926375 |

All 13 sets are within the 100,000-row, 4 MiB and 8 GiB bounds (REPORT:23).

For S_eff and SM-11..14 on the large workloads (`s-m-sealing-typed-remaining-2026-10-11/REPORT.md:9-29`):

| Workload | Rows | Descriptor bytes | Within bounds |
|---|---:|---:|---|
| smithy-rs | 3,632 | 647,602 | yes |
| rspack | 23,980 | 4,085,164 | yes, 109,140 bytes under the descriptor bound |
| deno | 14,920 | 2,227,549 | yes |
| sui | 19,063 | 3,509,292 | yes |

**Gaps.**
- (a) **Rust read sets omit dependency sources.** Rust read sets are repository-only (REPORT:25). The dependency-source set (and its import identity in a plan2-equivalent) is absent. Map-file inventories that include dependencies exist: R1 7,324 files, R2 6,646, R3 6,403, R4 1,525, R5 550, R6 213, R7 4,631, R8 643 + 533 (`actual-command-source-maps-r1.json`). None has been sealed in a timed run.
- (b) **Synthetic plan fields.** Snapshot and plan templates carry public synthetic non-inventory fields (REPORT:5). Only the axum read set has a complete plan2-equivalent preimage (`s-m-plan-equivalent-2026-10-09`), timed once, "diagnostic only".
- (c) **Overlay configuration** not captured (REPORT:25).
- (d) **Rspack headroom.** Rspack is 109,140 bytes under the descriptor bound on its repository-only set. Adding dependency sources can only grow it. That is a likely S-R finding, not a gap to "fix".

#### SM-6: TS read-set size
- **Accepted figure.** `s-m-sm6-readset-2026-10-09/REPORT.md:11-20`.

| Row | Entries | Bytes | Descriptor bytes | Tracked `node_modules` rows |
|---|---:|---:|---:|---:|
| express | 214 | 717,115 | 27,305 | 0 |
| napi | 644 | 11,675,794 | 88,420 | 0 |
| powertools | 1,389 | 7,818,881 | 206,175 | 0 |
| smithy-ts | 2,315 | 11,541,863 | 381,452 | 0 |
| umami | 2,026 | 9,083,336 | 283,572 | 0 |
| vite | 2,836 | 17,644,692 | 419,807 | 13 |

- All are repository-only, labelled, and within every bound. **Gap: none.**

#### SM-7: Transfer
TS rows use the repository-only sealed set; no Rust dependency set applies. Source: `s-m-transfer-2026-10-09/REPORT.md:11-24` (3 warmups + 7 runs, ms).

| Row | Median | Max |
|---|---:|---:|
| T1 express | 4.923 | 5.252 |
| T2 napi | 15.207 | 15.375 |
| T3 powertools | 24.416 | 25.309 |
| T4 smithy-ts | 41.624 | 42.572 |
| T5 umami | 34.211 | 35.000 |
| T6 vite | 54.558 | 55.770 |

**TS gap:** none, beyond the framing being a throwaway probe (REPORT:7).

Rust rows: sealed set plus dependency-source set. Source: `s-m-actual-map-transfer-series-2026-10-10/REPORT.md:7-17` (3 warmups + 7 runs; whole T2 repository plus Cargo-expanded registry sources of the resolved graph).

| Row | Mapped files | Median ms | Max ms | Registry packages in map (DERIVED) |
|---|---:|---:|---:|---:|
| R1 napi | 7,324 | 308.409 | 312.686 | 143 |
| R2 lambda | 6,646 | 264.138 | 275.369 | 149 |
| R3 axum | 6,403 | 253.194 | 258.022 | 150 |
| R4 hyper | 1,525 | 59.111 | 59.184 | 14 |
| R5 serde | 550 | 25.829 | 26.107 | 4 |
| R6 serde-json | 213 | 9.735 | 9.890 | 4 |
| R7 tokio | 4,631 | 184.599 | 185.109 | 80 |
| R8 entry 7 | 643 | 31.344 | 31.408 | 4 |
| R8 entry 8 | 533 | 24.501 | 24.668 | 3 |

Repository-only Rust transfer (`s-m-transfer-2026-10-09`) also exists for R1-R7 (for example axum 9.174 ms), but not for R8.

**Rust gaps.**
- (a) **Which dependency-source set.** The "Rust dependency-source set" in the maps is the host-filtered graph expansion. For axum it is 150 packages and 5,905 files, including `.cargo-ok` markers. The accepted DS4-P1 descriptor is 187 packages and 7,338 files (`s-m-dependency-fragment-2026-10-09/REPORT.md:2`). Its dependency-only transfer took a median of 1,591.848 ms host / 498.140 ms worker (`fragment/metrics.json`), through a different, CBOR-validating worker. A lead decision must pick one; DS4-P1 sets exist only for axum.
- (b) **R8 has no single-child transfer.** Entries 7 and 8 each stream the whole overlay plus their own registry sources.
- (c) **Not marked complete.** The map-transfer report itself says it "does not complete SM7" (REPORT:5).

#### SM-8: Longest synchronous compiler call
- **No accepted statistic.** DERIVED from accepted raw data (`s-m-ts-cohort-2026-10-09/evidence/<id>-<3..9>.stdout.json`): per measured run, the maximum over configs of `maxPublicCompilerCall.elapsedNanos`, then median and max over the 7 runs.

| Row | Median ms | Max ms | Call |
|---|---:|---:|---|
| T1 express | 106.561 | 109.894 | from the synthesized evidence; the cohort has no call |
| T2 napi | 105.719 | 114.749 | `createProgram` |
| T3 powertools | 125.411 | 130.272 | `createProgram` |
| T4 smithy-ts | 209.570 | 216.292 | `getSemanticDiagnostics` |
| T5 umami | 250.174 | 258.166 | `createProgram` |
| T6 vite | 198.878 | 206.101 | `getSemanticDiagnostics` |

- **Gaps.**
  - (a) **No definition.** SM-8 is undefined: is it the longest public API call, or the whole uninterrupted synchronous stretch? The cohort driver may not yield between calls.
  - (b) **Call granularity.** `getSemanticDiagnostics` is called per file in the cohort. A provider calling it program-wide would block for the whole pass.
  - (c) **Not accepted.** These values are not accepted figures. The D law's liveness floor takes SM-8 (PROPOSAL-r6:615).

#### SM-9: Complete replay
- **Accepted values.** One population: 193 synthetic sources, which are napi's TS configured files, with one illustrative fact and one finding per source (`s-m-full-replay-partial-2026-10-09/native/REPORT.md:5`).

| Path | Median ms | Max ms |
|---|---:|---:|
| Python reference `close_run`/replay | 14,689.338 | 14,768.295 |
| Native debug `replay_run` | 23,295.959 | 23,390.869 |
| Native release `replay_run` | 1,838.605 | 1,859.721 |

  Each path is 3 warmups + 7 runs (REPORT:9-11, :13).
- **Coverage.** T2 (napi-TS) only, and only conditionally. ✗ for the other 13 rows.
- **Gaps.**
  - (a) **No graph for any other row.** Item 9 needs a graph "of the size SM-2 and SM-4 imply", per workload. Natural sizes from accepted data are TS distinct configured files and Rust S. TS: express 204 Program files or 141 roots; powertools 936; smithy-ts 1,159; umami 1,381; vite 678. Rust: 239, 192, 301, 98, 208, 71, 808, 279. Even napi's Rust row (S = 239) differs from its TS row (193).
  - (b) **No sizing rule.** The sizing rule (sources or subjects, one fact and one finding each, or otherwise) is unrecorded. It needs a lead decision. It must not borrow a G3 emission factor, by analogy with PROPOSAL-r6:627.
  - (c) **No boundary choice.** Three boundaries differ by about 8x to 13x, and no decision picks one.
  - (d) **Open controls.** The register's "forged/missing control audits" remain open (`SM-DELIVERABLES.json` SM-9 row).

#### SM-10: RSS
- **Raw availability.** Every record retains native `wait4` RSS in macOS bytes with a checked identity conversion. Examples:
  - cohort `results.json` `runs[].rssBytes`;
  - per compiler child, `observationInformational.rss_native` in the analysis-timing samples;
  - rust-scope REPORT:9-43 "Process peak RSS bytes".
- **DERIVED medians (not accepted).**
  - TS cohort whole-process RSS: express 129,941,504; napi 431,489,024; powertools 825,507,840; smithy-ts 931,266,560; umami 820,953,088; vite 1,392,984,064 bytes.
  - Largest Rust analysis child per run: napi 430,899,200; lambda 393,347,072; axum 360,398,848; hyper 210,141,184; serde 93,880,320; serde-json 136,265,728; tokio 227,229,696 bytes.
- **Gaps.**
  - (a) No consolidated SM-10 record keyed to the F/T components.
  - (b) Rust per-unit children are not a single provider process. Their maximum is not a provider RSS.

#### SM-11: Rust cost per subject (S-M part)
- **S, exact.** From the census (REPORT:35-43), equal to RUST3-LIM where a row exists: R1 239, R2 192, R3 301, R4 98, R5 208, R6 71, R7 808, R8 279 (no RUST3-LIM row; 208 + 71). Large workloads from rust-scope (REPORT:32-40) and the Sui series: L1 1,084, L2 1,384, L3 1,052, L4 3,318.
- **Subject coverage (census `subjectCoverage`).** Coverage is exact for no workload:

| Row | Subjects covered | Fraction |
|---|---|---:|
| R1 | 4 of 239 | 0.0167 |
| R2 | 0 | 0 |
| R3 | 19 of 301 | 0.0631 |
| R4 | 18 of 98 | 0.1837 |
| R5 | 0 | 0 |
| R6 | 0 | 0 |
| R7 | 1 of 808 | 0.0012 |
| R8 | 0 | 0 |

- **Gaps.**
  - (a) **No labelled record.** No accepted record states SM-4 time and SM-10 RSS "each labelled with the compilation units it covers" (PROPOSAL-r6:587). The data exist per unit in the analysis-timing raw data, so this is a desk join, not a measurement.
  - (b) **Large workloads.**
    - **Smithy-rs:** partial SM-4 for 10 of 25 declared workspace entries. Sources: `s-m-actual-smithy-fuzz-framed-series-2026-10-10`, `…-http-fuzz-…`, `…-r11-hierarchy-r9-…` (REPORT:7-15, informational because review work ran concurrently). The original `rust-runtime` entry is unavailable before launch (descriptor 5,115,131 bytes > 4 MiB; `s-m-actual-large-workspace-data-r8-2026-10-10/REPORT.md:7`).
    - **Deno:** partial for 2 of 3 entries: binary subworkspace 11.503 ms; SQLite entry summed analysis 305.792 ms. The root entry is unavailable (descriptor 22,825,382 bytes, 76,424 rows; r8 REPORT:7).
    - **Rspack:** attempted only in large-workspace r1, with no graph.
    - **Sui:** Move resolves, but its bin source is a symlink excluded by the no-follow copy (r7 REPORT:7). No analysis.
  - (c) **Scratch** is not measured, which is lawful (PROPOSAL-r6:587).

#### SM-12: Scope rebuild (S-M part)
- **Accepted values.** `s-m-rust-scope-2026-10-09/REPORT.md:9-43` (3 warmups + 7 runs per actor).

| Row | host-a median ms | host-b median ms |
|---|---:|---:|
| R1 napi | 2.980 | 5.873 |
| R2 lambda | 2.421 | 4.884 |
| R3 axum | 3.741 | 7.086 |
| R4 hyper | 1.214 | 2.893 |
| R5 serde | 2.596 | 5.178 |
| R6 serde-json | 0.893 | 1.410 |
| R7 tokio | 9.893 | 17.452 |
| R8 overlay | 3.485 | 6.696 |
| L1 smithy-rs | 13.388 | 22.927 |
| L2 rspack | 17.735 | 30.430 |
| L3 deno | 13.229 | 22.772 |
| L4 sui (`s-m-sui-scope-series-2026-10-10/REPORT.md:7-19`) | 39.993 | 67.584 |

  Each also has process peak RSS (25.6-50.8 MB) and an exact Rust-helper equality check (REPORT:55-67).
- **Gaps (minor, label decisions).**
  - (a) Peak memory is whole-process wait4 RSS, explicitly "not incremental algorithm memory" (REPORT:7).
  - (b) Inputs are synthetic snapshot-equivalent descriptors over T2-pinned trees. If "accepted manifests" (PROPOSAL-r6:588) means accepted SnapshotManifests, only the worker-side reconstruction in `s-m-manifest-scope-2026-10-09` exists (R1-R8), with no host 3+7 timing.
  - (c) The worker derivation and `domainCommitment` are deferred to the completion round, which is lawful.

#### SM-13: Response volume (S-M decomposition)
**Part 1: site counts.** Census (Codex r2 ACCEPT, `reviews/codex-sm-rust-site-census-r2/review.json`): first-party sites per relation for R1-R8. Examples from `site-census-checks-r1.json`:

| Row | declares | references | calls | types |
|---|---:|---:|---:|---:|
| R1 napi | 69 | 753 | 360 | 1,539 |
| R3 axum | 3,268 | 15,668 | 4,393 | 18,939 |
| R4 hyper | 759 | 1,266 | 217 | 1,109 |
| R7 tokio | 3 | 0 | 0 | 0 |
| R2, R5, R6, R8 | 0 | 0 | 0 | 0 |

Dependency-crate sites are reported separately.

**Gaps.**
- (a) **Omitted relation@rungs.** NE's rust-cargo cells also include:
  - `literal@syntactic` and `control-flow@syntactic` (NE:592);
  - `reachability@from-resolved-calls` (NE:597);
  - `clones` mode `near` (NE:599; candidate-only).

  The census grouping covers declares, imports, references, calls, types, unresolved-edge and clones-body only. Codex M3L-R6-NBO-01 (`reviews/codex-provider-protocol-l-r6/REVIEW.md:68`) requires the full NE:590-601 range. Reachability and near-clones may be recorded as derived from call and body sites, but that has to be stated.
- (b) **No site-kind-to-query table.** "Each site kind named with the compiler query it counts" is only in prose (REPORT:11-17). `producer/site_walk.rs` uses `tcx.typeck`, `def_kind`, `hir_*`, `iter_local_def_id`.
- (c) **No fixed bytes.** Fixed bytes per candidate, per frame and per census row are absent. RPP `candidateSpoolAccounting` (`docs/coop/artifacts/rust-provider-protocol.v2.json`, the `limitPolicy.candidateSpoolAccounting` object) defines the entry as deterministic CBOR of `{analysisOrdinal, stageId, candidate}`. The frame is 8-byte length + 32-byte digest (a 40-byte transport prefix). This is desk derivation plus, optionally, a named reference encoder.
- (d) **No closed formulas** for (a)-(e) with unset G3/C4a parameters.
- (e) **No large-workload census.** L1-L4 have none; the accepted Smithy and Deno graphs could be censused.
- (f) **Zero sites for four rows.** R2, R5, R6 and R8 have zero sites because no first-party unit was analysed (see SM-4).

#### SM-14: Work units (S-M part)
- Only S exists. The formula record (Σ_stages S_stage × K_stage, with S per workload and K_stage unset, owner C4a) is missing. This is desk work.

---

## 3. F and T per workload: computable from accepted values today?

**Formulas.** F = start + SM-5 + SM-7 + SM-9 (PROPOSAL-r6:606). T = F + analysis (:607). Component medians are in ms, taken from §2.

**Column key.** ✓ = accepted 3+7 value; ◐ = accepted but partial or definitional; ✗ = missing.

| Row | start | SM-5 | SM-7 | SM-9 | F computable? | analysis | T computable? | Missing component(s) |
|---|---|---|---|---|---|---|---|---|
| T1 express | SM-1 ✓ 81.849 | ✓ 6.891 | ✓ 4.923 | ✗ | **No** | ◐ synthesized 257.128 | **No** | SM-9 (204- or 141-source graph); express SM-2 standing |
| T2 napi-TS | SM-1 ✓ | ✓ 23.219 | ✓ 15.207 | ◐ 193-source graph | **Conditionally** | ◐ 1,026.995 | **Conditionally** | Lead decisions: replay boundary and "193 = SM-2-implied size" |
| T3 powertools | SM-1 ✓ | ✓ 45.720 | ✓ 24.416 | ✗ | No | ◐ 3,465.558 | No | SM-9 (936) |
| T4 smithy-ts | SM-1 ✓ | ✓ 80.099 | ✓ 41.624 | ✗ | No | ◐ 16,295.809 | No (T_warm > 8 s if SM-2 is adopted) | SM-9 (1,159) |
| T5 umami | SM-1 ✓ | ✓ 66.081 | ✓ 34.211 | ✗ | No | ◐ 2,302.595 | No | SM-9 (1,381) |
| T6 vite | SM-1 ✓ | ✓ 102.499 | ✓ 54.558 | ✗ | No | ◐ 8,059.187 | No (T_warm > 8 s if SM-2 is adopted) | SM-9 (678) |
| R1 napi-Rust | SM-3 ✓ 8.688 | ◐ 23.219 (no deps) | ◐ 308.409 (graph deps) | ✗ | No | ◐ 2,488.600 summed; first-party 23.8 | No | SM-9 (239); SM-5 with deps; dependency-set decision |
| R2 lambda | SM-3 ✓ | ◐ 19.476 | ◐ 264.138 | ✗ | No | ◐ 1,831.740; first-party 0 | No | SM-9 (192); SM-5 deps; first-party analysis absent |
| R3 axum | SM-3 ✓ | ◐ 17.446 | ◐ 253.194 (or DS4-P1 1,591.848) | ✗ | No | ◐ 1,786.885 | No | SM-9 (301); SM-5 deps; dependency-set decision |
| R4 hyper | SM-3 ✓ | ◐ 4.719 | ◐ 59.111 | ✗ | No | ◐ 507.936 | No | SM-9 (98); SM-5 deps |
| R5 serde | SM-3 ✓ | ◐ 11.043 | ◐ 25.829 | ✗ | No | ◐ 22.600; first-party 0 | No | SM-9 (208); SM-5 deps; first-party analysis absent |
| R6 serde-json | SM-3 ✓ | ◐ 2.948 | ◐ 9.735 | ✗ | No | ◐ 97.269; first-party 0 | No | SM-9 (71); SM-5 deps; first-party analysis absent |
| R7 tokio | SM-3 ✓ | ◐ 27.853 | ◐ 184.599 | ✗ | No | ◐ 390.312; first-party 4.4 | No | SM-9 (808); SM-5 deps; tokio lib unavailable (proc-macro) |
| R8 overlay | SM-3 ✓ | ◐ 13.844 | ✗ as one child (31.344 + 24.501 per entry) | ✗ | No | ◐ 2 entries: 22.491 + 97.110; first-party 0 | No | SM-9 (279); one-child SM-7 or entry-combination rule; SM-5 deps |

**Reset labels.** For every row, T under Q0 §9.2 cold and warm resets (`harness/DESIGN.md:798-805`) is not available as labelled. No run recorded page-cache state (cold) or a priming slot (warm). Every accepted run is a fresh process with fresh private outputs and no reused provider, so the lead may label them. A missing page-cache record still blocks the exact cold label "cold OpenSIP state, page cache recorded".

**napi-TS conditional arithmetic.** ILLUSTRATIVE ONLY, not an S-M figure, and not to be cited as F or T. It uses SM-1 + SM-5 + SM-7 + native-release SM-9:
- F_median-sum = 81.849083 + 23.218750 + 15.206667 + 1,838.605042 = 1,958.879542 ms.
- F_max-sum = 1,981.828625 ms.
- T = F + 1,026.995125 ≈ 2,985.9 ms.

With the Python reference replay instead, F would be about 14.8 s. With native debug, about 23.4 s. So the replay-boundary decision alone decides whether napi-TS sits near (A) or squarely in (B).

---

## 4. Prioritized smallest measurement units for the S-M delta round

**Constraints honoured by every unit below.**
- Outside product, over public pinned T2 bytes only.
- No T2 repository code, build script or proc macro executes.
- Lead macOS host, labelled preliminary, 3 warmups + 7 runs, median and max.
- Never trim inputs or change bounds.
- Accepted closed drivers and executors are not modified; new variants are separate pinned files.
- Each unit is listed with the lead decision it needs first; a decision costs no measurement.

### P1. Per-workload sized SM-9 replay series
This unblocks F for all 14 rows; nothing else does.
- **Lead decisions first (record as lead decisions):**
  - SM-9 boundary = native release `replay_run`;
  - sizing rule = one synthetic fact and one finding per TS distinct configured file / per Rust subject S, mirroring the accepted 193-source recipe and labelled synthetic;
  - express size: 204 Program files or 141 roots.
- **Run.** Generate new packets with the closed generator recipe (a new variant file). Run the unchanged native release driver.
- **Populations (12 new):** TS 204 (or 141), 936, 1,159, 1,381, 678; Rust 239, 192, 301, 98, 208, 71, 808, 279. Napi-TS 193 reuses the accepted set.
- **Cost.** 10 children each. The 193-source run is about 1.8 s per child; time grows with size and must be measured, not extrapolated (PROPOSAL-r6:620).
- **Closes** SM-9 for every row. With P2/P3 or the dependency-set decision, F/T become computable for all TS rows at once.

### P2. One-child overlay transfer, plus the Rust dependency-set decision
- **Lead decision.** Is the Rust dependency-source set for SM-7 (and SM-5) the graph-expanded set already transferred, or the lock-wide DS4-P1 set (accepted only for axum)? If graph-expanded, R1-R7 SM-7 is already ✓ and only R8 needs a run.
- **Run.** One new map: the overlay's 439 regular files plus the union of the entry-7 and entry-8 registry sources (4 + 3 packages). Use it with the accepted order-preserving receiver (`s-m-actual-map-transfer-series-2026-10-10/closed-receiver`, unchanged). 10 children.
- **Alternative.** Lead decision that the overlay's Rust provider runs one child per Cargo entry, so SM-7(R8) is the sum of two children. That needs no run, but it must be stated.
- **If DS4-P1 is chosen instead.** A dependency-source-set intake and transfer is needed for 7 more workloads. That is materially larger: lock-wide sets, already acquired archives, and the closed fragment worker.

### P3. SM-5 Rust sealing with the dependency-source set
- **Run.** A new sealing variant whose read set is the pinned map file list (repository + registry sources) instead of the repository tree. Keep the closed probe's hashing and descriptor recipe. 8 Rust rows (9 entries; overlay as P2's union), 10 children each, millisecond to sub-second spans.
- **Report** rows, bytes and descriptor bytes against snapshot2 bounds (no trimming). Include the dependency-source set's identity in the plan2-equivalent if the lead wants plan2 to carry the import.
- **Closes** the Rust SM-5 gap and gives S_eff's first term on the real read sets.

### P4. SM-4 first-party coverage variant
- **Run.** A new graph-executor variant, not a modification. It launches first-party library units whose only unavailability is a **build-script** edge, with no build-script outputs (no OUT_DIR, no emitted cfgs). It discloses that expansion as unavailable, as PROPOSAL-r6:558 words it, and records whether `after_analysis` is reached.
- **Targets: BS-only library units (§2.2 SM-4):**
  - `axum`, `axum_extra`;
  - `serde`, `serde_core`, `serde_derive_internals`;
  - `serde_json`;
  - napi's `napi_sys` and `napi_derive_backend`;
  - the same libraries in R8 entries 7 and 8.

  Libraries that consume proc-macros stay unavailable: lambda's 5, the `tokio` library and napi's 11.
- **Optional extension.** Check-mode analysis of first-party proc-macro **crates themselves** (`axum-macros`, `tokio-macros`, `serde_derive`, napi's derive crates). Type-checking a proc-macro crate's source does not execute it. Their build-script-blocked dependencies (proc-macro2 and similar) fall under the same variant. This is a lawfulness reading the lead should record before use.
- **Statistic.** 3 warmups + 7 runs per entry, with the site-walk variant attached in the same children so SM-13 sites come from the same run.
- **Effect.** Raises SM-4, SM-11 and SM-13 first-party coverage. It cannot make coverage exact, because test, example and bench targets are not in the graphs.
- **Gating.** Outcomes (A)-(C) depend on SM-4 only through T. Schedule this after P1-P3.

### P5. SM-13 census completion (desk work, plus one small re-census run)
- **Desk records, no measurement:**
  - site-kind-to-compiler-query table;
  - fixed bytes per candidate, per frame and per census row from the registered schemas and RPP `candidateSpoolAccounting`, naming any reference encoder and its standing;
  - closed formulas (a)-(e) with unset parameters named (G3 emission, census kinds, batching; C4a stages);
  - SM-14 formula with exact S;
  - S_eff first term.
- **Run.** A site-walk variant adding `literal@syntactic` and `control-flow@syntactic` site kinds (HIR literal and `if`/`match`/`loop` expressions). Record `reachability@from-resolved-calls` and `clones` `near` as derived from call and body sites, or count them. Re-run over the 9 accepted entries: no timing, 2 runs, as the r2 census did.

### P6. SM-8 definition and record
- **Lead decision.** Define SM-8 as the longest single public synchronous compiler API call (per-file `getSemanticDiagnostics` granularity) or as the longest uninterrupted event-loop stretch.
- If the former, a desk derivation from the accepted cohort raw data (§2.2 SM-8) suffices.
- If the latter, a new Node cohort variant timing the program-wide semantic call, or `perf_hooks` event-loop delay, over the same 6 inputs.

### P7. Large-workload SM-11/SM-13 inputs
- **Run.** The site-walk variant over the accepted Smithy (10 graphs) and Deno (2 graphs) prepared entries.
- Record Rspack (no graph) and Sui (bin symlink excluded) as unavailable with reasons.
- Lowest priority: no outcome (A)-(C) depends on SM-11..14 (PROPOSAL-r6:577).

### P8. Reset labelling
- For P1-P3 and any re-run, record OS page-cache state before every run (cold label), and run one priming invocation per series (warm fixture).
- For the existing accepted components, a lead labelling decision is enough.

---

## 5. Decisions that close gaps with no measurement

| # | Decision | Closes or unblocks |
|---|---|---|
| D-1 | SM-9 boundary (native release `replay_run`) and sizing rule | SM-9 for T2 at once; defines P1 |
| D-2 | Rust dependency-source set for SM-5/SM-7 (graph-expanded or DS4-P1) | SM-7 R1-R7; scope of P2/P3 |
| D-3 | Overlay R8 composition (one child with union map, or two entry children) | SM-4/SM-7 R8 |
| D-4 | SM-2 span: whole process (double-counts SM-1) or summed per-config analysis (derivable); express via synthesized recipe | SM-2, T for TS |
| D-5 | SM-4 series and span: summed instrumented intervals, or whole graph including per-unit child start | T for Rust |
| D-6 | SM-8 definition | SM-8 (and the D law's liveness floor) |
| D-7 | §9.2 labels for already-accepted fresh-process runs | the T(cold)/T(warm) reporting rule |
| D-8 | SM-12 peak-memory label (process RSS) and the meaning of "accepted manifests" | SM-12 S-M part |
| D-9 | S_eff first-term reading | S_eff record |

---

## 6. Record hygiene noted in passing
- `SM-DELIVERABLES.json` cites PROPOSAL-r5 as authority. It does not reflect the accepted actual series or the r6 two-part rule beyond SM-11/13/14.
- The site census table lists `mr-rs-medium-serde-json` twice (ordinals 7 and 8). These are the two Cargo entries, not duplicate workloads.
- The Smithy r11/hierarchy series timings are "informational" because concurrent review work ran on the host (`s-m-actual-smithy-r11-hierarchy-r9-framed-series-2026-10-11/REPORT.md:15`). Any SM-4/SM-11 use must carry that label.
