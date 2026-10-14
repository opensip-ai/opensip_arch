# S-M Rust site census r1

This is an outside-product experiment. It supplies the S-M round's inputs to M3-L r6 item 9 ("When SM-11 to SM-14 are filled"). It produces no SM-11, SM-13 or SM-14 value.

## What ran

- **The driver.** It is a variant of the closed framed driver (`s-m-actual-framed-analysis-series-2026-10-10/closed-driver-source.rs`, `43315ea6…`). `producer/driver.rs` differs from the closed source in exactly three places:
  - an `extern crate rustc_hir;` and `mod site_walk;` pair;
  - `after_analysis` names its `TyCtxt`;
  - one `site_walk::emit(tcx);` call, placed after the closed `after_analysis` timing event, so the closed interval excludes the walk.
- **The walk.** The new module `producer/site_walk.rs` counts compiler **sites** per source file of the local crate:
  - local definitions by `DefKind`;
  - `use` items, with their resolution categories, and `extern crate` items, as a count only;
  - expressions, and expressions with a type in typeck results;
  - call and method-call sites, with their resolution, and method receivers that are trait objects or type parameters;
  - path expressions and paths, with resolution;
  - field expressions, closures and bodies.

  Macro-expanded sites count at their call site, in their base kind. They are **also** counted in a `<kind>.expanded` key, which is a subset of the base kind and never added to it.
- **The build.** It uses the closed recipe: bare rustc from the pinned 1.95 rustc-dev sysroot, at nice 10 under the lane lock. The image is `d04be840…`, 677768 bytes, at `compiled-image/site-driver`.
- **The runs.** The unchanged closed graph executor and root observer ran over the nine accepted prepared entries of the framed analysis series. Each entry ran twice, for 354 compiler children in all. Every unit's standing repeated the accepted pilot population: `allPopulationsRepeated` True. Site counts were identical across both runs: `allSiteCountsDeterministic` True. No timing statistic is claimed.

## What the audit derives

`audit_sm_rust_site_census_r1.py` is read-only. Its output is `site-census-checks-r1.json`.

- **Subject counts.** It computes the subject count S by RUST3-LIM's recipe: non-empty regular `.rs` blobs of the verified T2 store tree, with overlays taken by mount. For every repository with a row, S equals RUST3-LIM's recorded count. The overlay `mr-rs-medium-serde-json`, which has no row, gets S = 279 (208 + 71).
- **Subject mapping.** Every first-party site file is mapped to a subject, and its bytes must equal the store file. No first-party site falls outside a subject.
- **Dependency crates.** Sites in dependency crates are reported separately. They are not workload subjects.
- **Relation grouping.** Site kinds are grouped by the relation@rung they are **offered for** (NE:590-601, M3L-R6-NBO-01). The grouping is a label, not an emission recipe. Base totals exclude every `.expanded` key. The macro-expanded subset is reported separately per relation (`...ExpandedSubsetByRelation`).
- **Round 2 (Codex SM-SITE-R1-RF-01).** Round 1's audit summed the `.expanded` subset into the declaration totals, because the `def.` prefix matched both keys. Round 2 corrects only that derived aggregation. The driver, runs and raw observations are unchanged. Round 1's audit output is kept as `history/site-census-checks-r1-round1.json`.

| Ord | Workload | S | RUST3-LIM S | Subjects with sites | First-party units analysed / unavailable | Dependency units analysed |
|---|---|---|---|---|---|---|
| 0 | poly-medium-napi-rs | 239 | 239 | 4 | 1 / 41 | 65 |
| 1 | rs-medium-aws-lambda-rust-runtime | 192 | 192 | 0 | 0 / 8 | 48 |
| 2 | rs-medium-axum | 301 | 301 | 19 | 1 / 3 | 31 |
| 3 | rs-medium-hyper | 98 | 98 | 18 | 1 / 0 | 6 |
| 4 | rs-medium-serde | 208 | 208 | 0 | 0 / 12 | 2 |
| 5 | rs-medium-serde-json | 71 | 71 | 0 | 0 / 3 | 2 |
| 6 | rs-medium-tokio | 808 | 808 | 1 | 1 / 8 | 15 |
| 7 | mr-rs-medium-serde-json | 279 | no row | 0 | 0 / 12 | 2 |
| 8 | mr-rs-medium-serde-json | 279 | no row | 0 | 0 / 6 | 2 |

## What this does not supply

- **Coverage.** No workload has exact coverage. Most first-party code sits in units that the closed executor marks unavailable before launch: build scripts, proc macros, non-library targets, and their dependants. So, under item 9's rule, no SM-11 per-subject quotient is derived.
- **Owned parameters.** No stage, requested key, emission factor, census symbol kind or batching is chosen. These parameters remain with their owners: G3 for emission, census kinds and batching, and C4a for stages and keys.
- **Fixed byte overheads.** This unit does not supply the fixed overheads for SM-13 (b) to (e), and it states no SM-13 or SM-14 value.
- **Scratch.** No scratch is measured.
- **Scope.** There is no native admission or product change. Full S-M is not complete, L-G1 is not met, L is not in effect, and nothing is qualified.
