# S-M report plan r2: definitions S-M's report fixes, and the units left before it

**Lead plan record, 2026-10-13. Revision r2. Not law, not code, and no S-M figure.** It fixes the definitions that M3-L r6 item 9 leaves to S-M's report ("Unless S-M's report fixes it otherwise", PROPOSAL-r6:548), and orders the measurement units still owed before that report can be assembled. Each definition is a lead decision under the owner's standing direction (decide on the lead's recommendation; block only where none exists). Each has its reason and the alternatives rejected.

Nothing here fills a `⟨SM-n⟩` placeholder, computes F or T, or records an outcome (A)-(C). Those are recorded by S-M's report and the S-M delta round on L (L-G1; PROPOSAL-r6:186). O7, D3 and D13 are closed. Only L-G1 is open among L's gates (owner records 2026-10-09 meet L-G4, L-G5 and L-G9; L-G10 and L-G11 are met).

**Inputs.** The accepted S-M spikes under `docs/implementation/m3/spikes/s-m-*` (each with a final ACCEPT under `reviews/`), and the lead's read-only gap inventory of 2026-10-13. That inventory is preserved as `gap-inventory-2026-10-13.md` beside this record. It is a research aid; every number this plan relies on is cited to an accepted record.

**Changes from r1** (Codex `codex-s-m-report-plan-r1`, REQUIRED-FINDINGS; r1 is retained unchanged beside this file):

| # | Change | Finding |
|---|---|---|
| 1 | D-9 records SM-5's measured snapshot2-equivalent population per workload (rows, descriptor bytes, total bytes, bound standing) as the admitted-rows term. Any average-based ceiling is informational and estimated, outside the term. | SM-REPORT-PLAN-R1-RF-01 |
| 2 | §3a adds a coverage matrix for the large workloads smithy-rs, rspack, deno and sui (the last if S-P permits), and unit U-7 owes their pre-effect inputs before U-6. | SM-REPORT-PLAN-R1-RF-02 |
| 3 | D-1 calls its sizes workload source-count scenarios, carries the actual SM-2/SM-4 coverage beside them, and keeps any F, T or outcome conditional on the D-1 convention. | SM-REPORT-PLAN-R1-NBO-01 |

## 1. Where S-M stands

| Figure | Standing for the 14 item-9 rows | What closes it |
|---|---|---|
| SM-1, SM-3 | accepted figures (`grok-sm1-ready-r1`, `grok-sm3-ready-r2`, `…Complete:true`) | nothing |
| SM-6 | accepted, repository-only, labelled (`grok-sm6-readset-r1`) | nothing |
| SM-2 | 3+7 values for all 6 TS rows (`s-m-ts-cohort-2026-10-09`; express via `s-m-ts-synthesized-2026-10-10`) | D-4 |
| SM-4 | 3+7 values for all 8 Rust rows; first-party coverage thin | D-5, U-1 |
| SM-5 | TS accepted; Rust repository-only | D-2, U-2 |
| SM-7 | TS accepted; Rust only with the graph-expanded population, not the contracts' dependency-source set | D-2, D-3, U-2 |
| SM-8 | raw data only | D-6, U-4 (desk) |
| SM-9 | replay series at all 14 row sizes accepted as synthetic scaling scenarios (`s-m-replay-sized-2026-10-13`, Codex r2) | D-1 |
| SM-10 | raw data in every record | U-4 (desk) |
| SM-11..14, S_eff (S-M part) | S exact; SM-12 host values; SM-13 sites for 7 of 11 relation@rungs | D-8, D-9, U-3, U-4 |
| §9.2 reset labels | none recorded | D-7, U-5 |

## 2. Definitions S-M's report fixes (lead decisions)

### D-1. SM-9: boundary and graph size

- **Decision.**
  - **Boundary:** the native release `replay_run`. The image is the closed `opensip-sm-replay-bench` (`e82a4e2f…`, product `37581132`); for packets above the product canonical 4 MiB per-document cap, the pinned rows-transport variant (`7635c002…`) carries the same packets, with input loading the only change.
  - **Graph:** the closed generator's synthetic graph with one fact, one finding and one finding fingerprint per **counted source**: a workload source-count scenario. For a TS row, the count is SM-2's distinct configured files (express: the synthesized program's 141 roots). For a Rust row, it is the workload's RUST3-LIM input subjects S. These are input counts, not analysed coverage: Rust SM-4 analyses only part of S (census `subjectCoverage`, `s-m-rust-site-census-2026-10-13/REPORT.md:35-43`). The S-M report carries each row's actual SM-2/SM-4 coverage beside its SM-9.
  - **Values:** the accepted series in `spikes/s-m-replay-sized-2026-10-13` (series 2), each labelled "synthetic SM-9 under D-1".
- **Why this reading is lawful.** Item 9 defines SM-9 as complete replay "over a fact and finding graph of the size SM-2 and SM-4 imply. **Synthetic and labelled.**" (PROPOSAL-r6:563). The law asks for a synthetic graph, so real retained graphs are not required, and none exist before G3's emission binds after day 0. What the law leaves open is the graph's size. D-1 fixes it as an explicit benchmark convention: one fact and one finding per counted source, as in the accepted 193-source precedent (`s-m-full-replay-partial-2026-10-09`). It chooses no G3 emission factor or other owned parameter (PROPOSAL-r6:627).
- **What the label must carry.** The figure is a definition-bound synthetic figure. It is **not** a bound on any real workload's replay: real rules can emit zero findings for a source, and real graph shape, predicate work and retained bytes are not ordered by this family (Codex `SM-REPLAY-SIZED-R1-RF-01`, accepted). Any F, T or outcome the S-M report or delta round records from it is conditional on the D-1 convention and says so.
- **Correction recorded.** The control-state correction to `LD-SM9-BOUNDARY-AND-LOWER-BOUND-SIZING` said real SM-9 "needs real retained graphs". That overstated the law. The correction stands for the lower-bound claim and is narrowed here: SM-9 is synthetic by definition, and D-1 is its size rule.
- **Release boundary.** Release is the shipped profile. The Python reference and debug boundaries are oracles, not product replay (about 8x and 13x slower on the 193 graph).
- **Product state.** The image's product is `37581132`. Later product commits changed registries and schema bytes, not the replay algorithm (`s-m-replay-sized-2026-10-13/REPORT.md`, Disclosures). The S-M report states this; a re-measure is owed only if `replay_run` itself changes before the report.
- **Rejected.**
  - **Several facts or findings per source.** That chooses an emission factor, which is G3's (PROPOSAL-r6:627).
  - **Waiting for real graphs.** That contradicts "Synthetic and labelled" and recreates r5's gate cycle: real graphs need G3, after day 0.
  - **The 204 Program files for express.** Those include files outside the 141 repository roots.
  - **The Python reference or native debug boundary.** Neither is the shipped replay.

### D-2. The Rust dependency-source set for SM-5 and SM-7

- **Decision.** The Rust dependency-source set in SM-5 and SM-7 is the normative `DependencySourceSetV1` population: every non-path package in `Cargo.lock` that unified feature resolution activates for the target, admitted (`docs/v2/contracts/product-v1/native-evidence.md`, NE:612 L-RS1 and NE:1693-1694 DS-6), with DS4-P1's population rule (`snapshot-plan-c/ds4-p1-r1/CONTRACT.md:5`: "exactly the final activated admitted non-path population"; path packages stay in the snapshot, NE:1687). It is computed with the accepted DS4-P1 recipe (`spikes/s-m-dependency-fragment-2026-10-09`, `prepare_actual_dependency_source_set.py`) from the pinned public T2 lock and acquired archives. Nothing from a T2 repository runs.
- **SM-5 for a Rust row** is reported in two labelled parts per run, from one timed span: the repository read set's `snapshot2`/`plan2`-equivalent sealing (as accepted), and the dependency-source set's member hashing and `fileManifestSha256`/set identity (the host's content-addressed admission, NE:1706-1707). Rows, bytes and descriptor bytes are reported for each part against its own bounds.
- **SM-7 for a Rust row** streams the sealed repository set and then the dependency-source set's files, once per child, in ≤ 1 MiB framed chunks, as NE's custody order puts snapshot custody before dependency-source custody (NE:2863-2864).
- **Why.** Item 9 names "the Rust dependency-source set" (PROPOSAL-r6:561), and the contracts define exactly one: the activated admitted non-path set the Plan imports by `dependencySourceSetId`. The accepted map-transfer series (`s-m-actual-map-transfer-series-2026-10-10`) streamed a different population, the Cargo-expanded registry sources of each resolved build graph, and says itself that it "does not complete SM7". For axum the normative set is 187 registry packages and 7,338 files (`s-m-dependency-fragment-2026-10-09/REPORT.md:2`), more files than that whole axum map holds with the repository included (6,403 mapped files, `s-m-actual-map-transfer-series-2026-10-10/REPORT.md:11`).
- **Owed.** U-2 builds the set for the other Rust rows (R1, R2, R4-R8; R8 per entry under D-3) and runs the SM-5 and SM-7 series. The accepted map-transfer and dependency-fragment series stay as information, not as SM-7.
- **Rejected.**
  - **The graph-expanded map population.** It is not the set the contracts define or the Plan imports.
  - **The whole lock.** Lock-wide acquisition precedes activation (`snapshot-plan-c/PROPOSAL-r7.md:600`); the imported set is the activated one.
  - **The dependency fragment's CBOR-validating worker transfer as SM-7.** It times a different worker and framing, for one workload only.

### D-3. The overlay row R8 (`mr-rs-medium-serde-json`)

- **Decision.** R8 is run as its two Cargo workspace entries, as every accepted Rust series runs it: ordinal 7 (`rs-medium-serde`) and ordinal 8 (`rs-medium-serde-json`). Each R8 per-child figure (SM-4, SM-5's Rust part, SM-7) is the **sum** of the two entries' values, labelled "two entry children". SM-3 enters F once per child, so F(R8) carries SM-3 twice.
- **Why.** Item 9 adds the workspace as a row (PROPOSAL-r6:549) but no accepted rule merges two Cargo entries into one child. Each entry's map already carries the whole overlay plus its own registry sources. Summing two measured children uses only measured values and over-states, never under-states, the one-shot cost.
- **Rejected.** **A new single-child union map** would need a provider rule (one child for two Cargo roots) that no law states.

### D-4. SM-2: the TS analysis span

- **Decision.** SM-2 is the accepted cohort's whole-process span per run (`s-m-ts-cohort-2026-10-09`), median and maximum of 7 measured runs; for express, the synthesized program's whole-process span (`s-m-ts-synthesized-2026-10-10`). Labels: every `tsconfig*.json` in the repository, overlapping; repository-only types (T2 pins no `node_modules` tree); the span includes Node and TypeScript start and map preparation.
- **Consequence for T.** T = F + SM-2 then counts TS start twice (SM-1 inside SM-2, and again in F). The S-M report states this over-count beside each TS T.
- **Why.** It is the measured, reviewed 3+7 statistic. A start-free figure, such as summed per-config analysis intervals from the retained raw evidence, would be a new derivation, not a measured statistic, and it would still re-check files that several configs share. The whole-process span over-states one repository pass; over-statement errs toward (C), which the owner then decides (O4), and never hides a budget miss.
- **Rejected.** **Root tsconfig only.** Smithy-ts and umami have root-only values (`s-m-foundation-2026-10-09`), but a root config does not cover the repository.

### D-5. SM-4: the Rust analysis span and coverage

- **Decision.** SM-4 is the whole-graph span of the accepted package-context series (`s-m-remaining-context-series-2026-10-10`). That span includes per-unit compiler-child start, hashing, decoding and bookkeeping (its REPORT:7), and its coverage is labelled: the units analysed, first-party and dependency, and the units unavailable with their reasons. The summed per-unit analysis intervals (`s-m-actual-analysis-timing-series-2026-10-10`) are reported beside it as information.
- **Coverage owed before the report.** Item 9 says no build script or proc-macro **runs**, and the expansion that depends on them is **disclosed as unavailable** (PROPOSAL-r6:558). The closed executor instead marks build-script-only library units unavailable before launch, so axum, serde and serde_json's main libraries are not analysed at all. U-1 analyses them with the build-script expansion disclosed unavailable. The S-M report then uses U-1's whole-graph spans for the rows it changes.
- **Why.** The whole graph is what one Rust3 run over the workload costs, child starts included. The summed intervals omit per-unit start and map decode.
- **Rejected.**
  - **Summed intervals as SM-4.** They omit measured work.
  - **Proc-macro-consuming libraries.** Analysing a library that needs proc-macro output would need the macro executed, which item 9 forbids. Those units stay unavailable and disclosed.

### D-6. SM-8: the longest synchronous compiler call

- **Decision.** SM-8 is, per measured run, the longest single public TypeScript compiler API call the SM-2 driver makes (`maxPublicCompilerCall`), with its call name. The value is the median and maximum over SM-2's 7 measured runs, taken from SM-2's retained raw evidence. It is labelled with the driver's call granularity: `createProgram` per config, and `getSemanticDiagnostics` per file.
- **Why.** Item 9 names "the longest single synchronous compiler call inside SM-2 (the event-loop block)" (PROPOSAL-r6:562). The public call is the unit the driver can time exactly; the cohort records it already.
- **Label for the D law.** A provider that calls `getSemanticDiagnostics` program-wide would block for longer. The D law takes SM-8 for its liveness floor (PROPOSAL-r6:615), so the label travels with the figure.
- **Rejected.** **Event-loop-delay sampling.** It needs a new driver variant and measures the driver's scheduling, not the compiler call item 9 names.

### D-7. Q0 §9.2 reset labels

- **Warm.** The accepted 3+7 component series are fresh processes after 3 warmups on the same inputs, with no OpenSIP state and no reused provider. One-shot analysis declares no caches. They meet §9.2's warm fixture: one or more priming invocations on the same inputs, then each run a new process with no reused provider (`harness/DESIGN.md:805`). The S-M report labels them "warm, priming by warmups, no declared caches".
- **Cold.** §9.2's cold label needs the OS page-cache state recorded before **every** run (`harness/DESIGN.md:798-801`). No accepted run records it. U-5 re-runs the F and T components with that record. Until then, T under the cold reset is "not applied".
- **Why.** Outcome (C) compares T under each reset S-M can apply (PROPOSAL-r6:609-613). Leaving cold unmeasured would leave (C) under the 30 s cold budget undetermined.

### D-8. SM-12's labels

- **Peak memory** is whole-process `wait4` RSS, labelled "process peak, not incremental algorithm heap accounting", as the accepted record states (`s-m-rust-scope-2026-10-09/REPORT.md:7`).
- **"The accepted manifest"** (PROPOSAL-r6:588) is the accepted T2 corpus manifest (`corpus/t2-corpus-manifest.draft.json`, `c8cc48e1…`) over the verified T2 store. That is what RUST3-LIM's subject recipe and the accepted host derivations use. A product SnapshotManifest exists only after admission, which item 9 does not require for S-M.

### D-9. S_eff's first term

- **Decision.** "snapshot2's admitted rows, from SM-5" (PROPOSAL-r6:591) is recorded per workload as SM-5 measured it: the exact snapshot2-equivalent inventory population (its rows), its canonical descriptor bytes and total bytes, and its standing against each bound (100,000 rows, 4 MiB descriptor, 8 GiB; PROPOSAL-r6:559). For the medium rows this is `s-m-sealing-typed-2026-10-09/REPORT.md:7-23`; for the large workloads, `s-m-sealing-typed-remaining-2026-10-11/REPORT.md:9-29`. Under D-2 a Rust row's dependency-source part is reported beside it, not added to snapshot2's rows.
- **Not the term.** No ceiling is extrapolated from average bytes per row: row encoding varies with paths and content, and descriptor overhead is not a per-row constant. If the S-M report shows such a number, it is labelled "estimated, informational" and kept outside S_eff. S_eff itself is not filled; its other terms stay formulas (PROPOSAL-r6:591).

## 3. Units owed before S-M's report

| Unit | What | Depends on | Review |
|---|---|---|---|
| U-1 | **SM-4 coverage variant.** A new graph-executor variant (not a modification) that launches first-party library units whose only blocking edges are build scripts, with no build-script outputs, disclosing that expansion as unavailable; 3+7 whole-graph spans for R1, R3, R5, R6, R8. Records whether `after_analysis` is reached. | D-5 | Codex |
| U-2 | **Rust dependency-source sets, sealing and transfer under D-2.** DS4-P1 sets for R1, R2, R4-R8 (R8 per entry); SM-5 two-part sealing and SM-7 transfer series, 3+7, for all 8 Rust rows. | D-2, D-3 | Codex |
| U-3 | **SM-13 census completion.** Site-walk variant adding `literal@syntactic` and `control-flow@syntactic` sites, re-run over the 9 entries (no timing); desk records of the site-kind-to-query table, fixed bytes per candidate, frame and census row from the registered schemas and RPP `candidateSpoolAccounting`, the closed formulas (a)-(e) and SM-14 with owned parameters unset. `reachability@from-resolved-calls` and `clones` mode `near` are stated as derived from call and body sites. | — | Codex |
| U-4 | **Desk records.** SM-8 under D-6; SM-10 per F/T component; SM-11's labelled SM-4/SM-10 by covered units for the medium rows; S_eff's first term under D-9 for all 12 Rust workloads. | D-6, D-9 | Codex |
| U-5 | **Cold-reset series.** New pinned runner variants that record OS page-cache state before every run, over the F and T components. | D-7 | Codex |
| U-7 | **Large-workload pre-effect inputs** under §3a: site census over the accepted Smithy and Deno prepared entries; SM-11's labelled SM-4/SM-10 by covered units where analysis exists; exact substantiated unavailability for every entry with no analysis (rspack, sui, Smithy `rust-runtime`, the Deno root). | U-3 | Codex |
| U-6 | **S-M report assembly.** Every figure under D-1..D-9, labels, per-row F and T as item 9 defines them (conditional on D-1), and every outcome that holds, ready for the S-M delta round on L. | U-1..U-5, U-7 | Codex |

### 3a. Large workloads (SM-11 to SM-14, S-M part)

Item 9 adds smithy-rs, rspack and deno, and sui if S-P permits, for SM-11 to SM-14 (PROPOSAL-r6:571), and the S-M round's part applies to each (:586-591). No outcome depends on them (:577), but that does not make them optional.

| Workload | Exact S | SM-12 host derivations | SM-4 / SM-10 coverage | SM-13 sites | S_eff first term (SM-5) | Owed |
|---|---|---|---|---|---|---|
| smithy-rs | 1,084 (`s-m-rust-scope-2026-10-09`) | accepted, 3+7 | partial: 10 of 25 declared entries analysed (`s-m-actual-smithy-fuzz-framed-series-2026-10-10`, `s-m-actual-smithy-http-fuzz-framed-series-2026-10-10`, `s-m-actual-smithy-r11-hierarchy-r9-framed-series-2026-10-11`, the last informational because review work ran concurrently); `rust-runtime` unavailable before launch (descriptor 5,115,131 bytes over the closed driver's 4,194,304-byte bound, `s-m-actual-large-workspace-data-r8-2026-10-10/REPORT.md:7`); `aws-smithy-fuzz` refuses under `--locked` (`…-r7-2026-10-10/REPORT.md:7`) | none | 3,632 rows; 647,602 descriptor bytes; within bounds | U-7: census over the analysed entries; labelled coverage; each other entry's unavailability exact |
| rspack | 1,384 | accepted, 3+7 | none: no graph in any accepted series (`…-r1-2026-10-10`; r2 observed only Smithy, Deno and Sui, `…-r2-2026-10-10/REPORT.md:7`) | none | 23,980 rows; 4,085,164 descriptor bytes; within bounds | U-7: the exact per-entry reason from the retained r1 outcomes, desk only |
| deno | 1,052 | accepted, 3+7 | partial: the binary subworkspace and the SQLite entry analysed (`s-m-actual-deno-framed-bin-series-2026-10-10`, `s-m-actual-deno-sqlite-short-paths-framed-series-2026-10-10`); the root unavailable before launch (descriptor 22,825,382 bytes, r8 REPORT:7) | none | 14,920 rows; 2,227,549 descriptor bytes; within bounds | U-7: census over the two analysed entries; labelled coverage |
| sui (if S-P permits) | 3,318 (`s-m-sui-scope-series-2026-10-10`) | accepted, 3+7 | none: Move resolves, but its bin source is a symlink the no-follow copy excludes (r7 REPORT:7) | none | 19,063 rows; 3,509,292 descriptor bytes; within bounds | U-7: unavailability recorded exactly; no analysis claimed |

Quotients by S are recorded only where coverage is exact (:587), which holds for none of these. Unavailable or partial coverage is preserved as it is. U-7 executes no repository code, admits nothing natively and measures no worker figure.

## 4. What this plan does not do

It fills no placeholder, computes no F or T and records no outcome. It does not change L, the closed drivers, executors, observers or generators, or any accepted record. It chooses no G3 or C4a parameter. Full S-M, L-G1, effective L, native admission and worker, K1 and qualification remain open.
