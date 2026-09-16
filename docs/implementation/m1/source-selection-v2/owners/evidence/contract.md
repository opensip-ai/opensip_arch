# Report evidence design candidate (author-02): RP-DO-03, RP-DO-05, RP-DO-09, RP-DO-10

## 0. Standing

This is an **author-02 correction candidate** answering the fresh independent review `m1-report-evidence-design-review-01` of frozen `m1-report-evidence-design-subject-01` (outer `0af84231…fa11`, decision changes-required). It is not approval; a separate review and root acceptance are still required.

| Scope | State |
|---|---|
| Review01 findings | F1–F4 (high) and F5–F7 (medium) corrected with executable laws and permanent regression cases; F8 and F9 (low) corrected (§2) |
| Report parent | Rebased onto the frozen, unaccepted `m1-report-projection-subject-07` (outer `cee1eb24…c43e6c8`). Its bytes are never edited. |
| Owner successors S1–S4 | Proposals, not accepted. S2 is executed against the pinned identity model; see §3. |
| Remaining blockers for these four features | None found. Owner acceptance of S1–S4 is a dependency. |
| Separate work, not selected or duplicated | root timing, catalog, configuration and history proposals |
| Not claimed | runtime, browser, generator, performance, Run replay or product qualification; whole-report completion |

`check.py` verifies these prior inputs, which stay immutable:
- the subject-01 outer manifest;
- the parent07 outer manifest and every parent07 file it reads;
- the review01 finding list.

## 1. Subject, closure and how to run

**Subject.** `subject-files.json` lists every file except itself:
- **Code:** `reference_model.py`, `identity_bridge.py`, `build_owner.py`, `build_fixtures.py`, `check.py`, `seal.py`.
- **Owner records (`owner/`):**
  - `framework-recognition-plan.schema.v1.json`
  - `identity-parameter-registry-patch.v2.json`
  - `native-recognition-successor.v1.json`
  - `report-projection-successor-patch.v2.json`
  - `evidence-design-successor.v2.json` (register and finding dispositions)
- **Data and documents:** `fixtures.json`, `source-pins.json`, `contract.md`.

**Run** from any cwd, on an exact copy of the listed files:

```
TMPDIR=<existing absolute dir> /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B <copy>/check.py \
  --architecture /Users/sb/code/opensip-ai/opensip_arch --subject-strict --out <absolute result path>
```

**Closure.** Parent07's stronger hook is adopted.

| Mechanism | What it enforces |
|---|---|
| Pins | 89 files and 2 listings, verified before import and re-hashed at every governed open |
| Unattributable events | Every open or listing event without an absolute path is refused `UNATTRIBUTABLE-PATH-EVENT` |
| Alias probe | Exact, case-variant and `..` spellings of the unpinned README are refused `UNPINNED-LOAD`; the relative spelling is refused `UNATTRIBUTABLE-PATH-EVENT`. The probe runs in strict mode only, so a trace never pins its target. |
| Fresh-source loader | Bytecode is never read. Overlay modules compile only when their bytes equal the digest this run wrote from pinned bytes plus the published transforms (`verifiedOverlayCompiles`). |
| Cleanup | Scratch is removed by an absolute scandir/lstat/unlink walk |
| Processes and writes | No child processes; only the declared `--out` may be written, and it cannot be read |

`seal.py` is an authoring tool and `check.py` never runs it. It regenerates the owner records and fixtures, and it writes pins from an in-memory trace.

## 2. Finding dispositions (review01)

### F1 (high): historical Run admission

**Mechanism.**
- **Optional registry row.** S2 adds the `FrameworkRecognitionPlanV1` parameter row with **no** `requiredForEvaluatorMajors`.
- **Identity-model successor (T1).** An exact once-only source transform appends the document to `identity-model.v3.py`'s closed registered-record list. Without it, `validate_registered_record` refuses a new-Plan payload with `UNREGISTERED_DOCUMENT` (found by execution).
- **New-Plan duty.** `admit_new_plan_recognition_parameter` runs at the pre-Plan boundary of a **new** Plan, after `admit_parameter_selection`. When any requested languageMode maps to typescript or rust in the identity `languageModes` map, exactly one parameter must resolve to the row; otherwise `NEW_PLAN_RECOGNITION_PARAMETER_REQUIRED`. Retained closure never applies the duty.

**Executed (`identityBridge`).** A scratch overlay holds exact copies of the 60 traced owner files, plus the successor registry, T1 and the new document. The pinned evaluator3 reference fixture builds real retained Runs (`build_file_inputs` → `seal_fixture` → `open_run_closure` → `derive` → reseal → `close_run`):

| Case | Result |
|---|---|
| Predecessor Run (no parameter) | Admitted by the pinned model **and** by the successor model with the same `run3`; custody is read from its own two parameters as `not-plan-bound` |
| New-Plan Run (fixture-only transforms F1/F2 select the parameter) | Admitted by the successor model; `plan-bound`; a different PlanId |
| Pinned predecessor model closing the new-Plan Run | Refused `PAYLOAD_PARAMETER_UNREGISTERED`, so nothing is silently upgraded |
| Parameter bytes lost | `close_run` refuses `EVIDENCE_UNAVAILABLE`; custody under purged or partial-missing availability is `unavailable` |
| Duty | Syntax-only spec without the parameter: admitted. Compiler-mode spec without it: refused. With one: admitted. With two: `ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS`. |

The synthetic `planBound` flag is gone. World custody comes from `analysisSpecParameters`, `parameterAvailability` and `retainedParameterPayloads` (`custody_from_parameters`).

**Observation for the owners, not changed here.** Native `admit_analysis_spec` calls the historical `identity-model.py`, which uses the v2 registry.

### F2 (high): cross-universe test callers

`derive_test_reachability` walks the owner `graph.reach` to the end. It derives origin sets for the subject universe **and every universe among the reach rows**, and matches hits per universe. The embedded `testOrigins` carry every set used (`testOriginsProjection`, cap 256).

**Rows:**
- `reachedUniverses` is embedded on `not-found-incomplete` and `unknown/no-test-origin-identity` rows.
- A reached universe with no identity adds `reached-universe-without-test-origin-identity`.
- A set not embedded adds `origin-sets-not-embedded`.

**Regressions:**
- The review C1 world (`cross-universe-test`): helper is `static-path-from-test-origin` with its origin in the tests universe.
- Variant `mixed-reached-universe-without-identity`: a legacy-universe caller (no test identity) of `rs:core::shared_fmt` gives `not-found-incomplete` with blockers exactly `reached-universe-without-test-origin-identity` and `test-origin-set-partial`, and `reachedUniverses` naming both universes.
- Mutant M4 (hits restricted to the subject universe) is killed; M14 (the identity blocker dropped) is killed.

### F3 (high): default globs are not a test population

**No origin set can be complete.**
- TS/JS sets are const `partial` and always carry `recognizer-globs-not-test-population`.
- Rust sets remain `partial` with `in-target-unit-tests-not-identified`.
- The `no-static-path-within-bound` state is **removed** from the schema. A search without a hit is `not-found-incomplete`, always with `test-origin-set-partial` and interpretation `…not-untested`.

**FR-8.** A `package.json` jest object with any of `testMatch`, `testRegex`, `roots`, `projects` or `testPathIgnorePatterns` is read as data; vitest-jest then reports `test-selection-configured`. The pinned native recognizer returns no unresolved choice for the same input; both results are recorded in `nativeModel`.

**Imported execution evidence.** `TestPayloadV1` is never an origin source. Every set has interpretation `native-static-origin-identity-not-imported-execution`, and an `imported-test-id` origin is refused `SCHEMA`.

**Regressions:**
- The review C2 world (`jest-configured`): helper is `not-found-incomplete` and the set lists `test-selection-configured`.
- Document cases reintroducing the absence state or `completeness: complete` → `SCHEMA`; dropping the default-glob limitation → `J-TR-ORIGIN-SET`.
- Mutants M9 and M13 are killed.

### F4 (high): Cargo workspace member binaries

**FR-7 successor (`cargo_target_entries`).** For each Rust universe, the entries are every **selected** `bin` or `lib` target from retained `SourceUnitOwnershipV1`, each paired with the unique `RustUniverseV2ResolvedInputs.crateRootPaths` member that target owns.

**Missing coverage** is exact: `target-crate-root-unresolved`, `target-crate-root-ambiguous`, `ownership-enumeration-partial`. State is `all` only with every root resolved from complete ownership.

These entries (provenance `cargo-target`, unitId recomputable) are the effective entry points together with the recognized effects. `scope_state` drives the `entry-recognition-not-all` blocker for the target universe and for any origin universe outside the entry set.

**Executed against the pinned native model.**
- `discover_units` folds the mixed workspace into one `cargo-workspace` unit with members `crates/app` and `crates/core`.
- `recognize_frameworks` at the unit root reports `all` with only `src/main.rs`.
- The successor entries are `crates/app/src/main.rs`, `crates/core/src/lib.rs` and `src/main.rs`.

**Regressions:**
- The review C3 trace for `rs:core::shared_fmt` is now `path-found` from `crates/app/src/main.rs`.
- The variant with that crate root unresolved gives `partial` with `target-crate-root-unresolved`, and the trace is `no-entry-origin` with `entry-recognition-not-all`.
- Mutant M10 (member targets ignored) is killed.

### F5 (medium): patch composition

S4 uses semantic operations whose preconditions are checked on the current document at application time:
- `remove-members`, with `key` and `selectorGuard` on the per-command const;
- `insert-members-after`;
- `add`.

The parent-pinned identity is recorded separately (`patchedReportCanonicalSha256`).

**Executed:** this patch and a real second obligation's operations (RP-DO-11 stand-in: remove `step-duration` from `FeatureId` and all 8 per-command consts, 9 ops) run sequentially through the same applier in both orders and give identical documents.

**Refused with precondition errors:** re-applying this patch; another obligation claiming one of these members; a missing insert anchor; a wrong command selector guard.

### F6 (medium): coupling bounds and report budget

`fit_coupling` builds the largest deterministic prefixes under a byte budget, in this order:
1. cells, priority facts descending then keys;
2. target buckets, facts descending then keys;
3. drilldown rows of listed cells (cap 1000).

**Carrier:**
- Each list has an `ItemProjectionV1` with a measured `rejectedByteDelta`.
- Owners are exactly the closure referenced by listed cells and buckets (`ownerClosure`).
- Totals stay exact over the whole projection (`cellCount`, `cellFactSum`, `targetBucketCount`, `ownerCount`).
- Omitted cells or buckets add the blockers `cells-omitted` / `target-buckets-omitted`, and `blankCellMeans` becomes `not-determined-cells-omitted`.
- A skeleton that does not fit gives no panel (`omitted/exploration-budget-exceeded`).

**Report-wide placement.** `projectionPriority` becomes comparison, catalog, evidence, graph, history, symbolEvidence, coupling. `place_successor_panels` gives each successor panel exactly the canonical bytes the whole panels object leaves. An omitted `symbolEvidence` forces `coupling` omitted (`J-BUDGET-ORDER`). `symbolEvidence` metrics are byte-bounded the same way.

**Executed (`denseCoupling`, `integration`).**
- **Dense 120-package workspace** (14,280 cells):
  - at 4,194,304 B: 4,193,904 B with 3,911 cells omitted;
  - at 200,000 B: 13,896 omitted;
  - at 1,000 B: no panel.
- **Refusals:** a no-dependency blank-cell claim with omitted cells → `J-COUPLING-ABSENCE`; a panel over its budget → `J-COUPLING-BUDGET`.
- **Inside parent07 `audit-full`:** under the effective exploration budget, the dense panel is placed with 4,292 cells omitted and the whole panels object stays within the cap. A tight cap omits both panels, and a present `coupling` after an omitted `symbolEvidence` is refused `J-BUDGET-ORDER`.

Mutants M12 and M17 are killed.

### F7 (medium): mutants and featureMap

**Permanent fixtures that kill review01's surviving mutants:**

| Mutant | Fixture that kills it |
|---|---|
| M4 | the cross-universe world |
| M7 | `mixed-whole-view-test-bound`: host test bound 10 gives `lower-bound`, `unexamined-work-bound`, `projection-lower-bound` |
| M8 | `mixed-zero-under-limitation`: an exact 0 under a calls limitation has `zeroSupportsAbsence: false` |

**featureMap.** Refs are fully resolved against the patched schema (11 refs); a bogus member is refused.

**Mutation evidence.** The author mutation run is authoring evidence, not part of the claimed closure. It is recorded beside the candidate in `mutation-results.json` (harness `mutants.py`).
- **Method.** Each mutant is one exact once-only source replacement in a fresh copy, run in trace mode.
- **Result.** All 13 are killed, and each kill point was checked to be its law-specific assertion or refusal:
  - review01's surviving M4, M7 and M8;
  - F2: M14;
  - F3: M9, M13;
  - F4: M10;
  - F6: M12 (`J-COUPLING-ABSENCE`) and M17 (`J-COUPLING-BUDGET-INTERNAL`);
  - F8: M15;
  - F9: M11;
  - F1: M16 (published row required again: refused by owner-byte regeneration) and M16b (only the overlay row required: the predecessor Run is refused `EVALUATOR_REQUIRED_PARAMETER_MISSING` by the real identity model).
- **Surfaced gap.** M14 survived the first run; the variant above now kills it.

### F8 (low): duplicate provenance

Cells expose three counts, disclosed by the const `countUnits`:
- `facts`: distinct fact2 observations;
- `programEdges`: distinct endpoint pairs per universe;
- `sourceDependencies`: distinct importer anchor paths × universe-independent target identity.

**Regressions:**
- The review C6 duplicate (`mixed-cross-program-duplicate`): shared→web is 2 facts, 2 program edges and **1** source dependency.
- The mixed `legacy→web` cell shows the same pattern.
- Mutant M15 is killed.

### F9 (low): anchor path versus symbol path

Importer owners key on the imports fact **anchor paths**. This is native §2.1's law: rows whose path equals the enclosing fact's anchor path; imports anchors are source-text spans read.
- Every anchor must give the same owner set; otherwise the fact goes to bucket `importer-anchor-owners-disagree`. A fact without anchors goes to `importer-anchor-missing`.
- The importer symbol inventory path is never used for ownership. When it lies outside the anchors it is counted (`importerSymbolPathOutsideAnchors`).
- Origin and test-origin subjects still use symbol inventory attribution, because they are subject identities, not fact occurrences.

**S3** exposes the retained anchor paths.

**Regressions:**
- Mixed facts `i18` (anchored in a legacy file, symbol in web) and `i19` (anchors in two packages).
- Host case `coupling-symbol-path-instead-of-anchor` → `J-COUPLING-OWNER`.
- Mutant M11 is killed.

## 3. Owner successors

| Id | Owner | Record | Effect |
|---|---|---|---|
| S1 | native §8 | `owner/native-recognition-successor.v1.json` | FR-6 repository-relative paths; FR-7 per-unit recognition plus Cargo target entries; FR-8 configured jest selection. No native schema change. |
| S2 | foundation/identity | `owner/identity-parameter-registry-patch.v2.json` | Optional registry row, T1 source transform and the new-Plan duty. Historical Runs are unchanged; new Plans that select the parameter get a new PlanId. |
| S3 | query §8a | register | Whole-view internal projection with anchor paths and the §5 produced-item law. No public operation. |
| S4 | report | `owner/report-projection-successor-patch.v2.json` | 33 semantic operations: FeatureId and seven featureStates consts, projectionPriority, two PanelsV1 members, 22 `$defs` |

S5–S7 (imported evidence, enumeration and inventory, native `SourceUnitOwnershipV1`) are unchanged.

## 4. Laws in brief

**Coupling (R08).** Every blank-cell or absence claim requires complete cells and no blockers, over the admitted imports view only.
- Joins: `J-COUPLING-RUN`, `-BUDGET`, `-OWNER-KEY`, `-ORDER`, `-CELL`, `-COUNT`, `-BUCKET`, `-OWNER-CLOSURE`, `-TOTALS`, `-PROJECTION`, `-ABSENCE`, `-DRILL`.

**Metrics (R07).** A closed catalog of five graph operations. Each reading is `exact`, `lower-bound` or `unknown`, interpreted as a static projected count. A zero supports absence only when exact and unlimited.

**Entry points (R12).** Custody is `not-plan-bound`, `unavailable` or `plan-bound`. Traces start only at an embedded reachability origin whose native-attested path is an effective entry (explicit, cargo-target or recognized). `no-entry-origin` is never dead-code proof.
- Joins: `J-ENTRY-*` (including `J-ENTRY-CARGO`) and `J-TRACE-*`.

**Test reachability (R07).**
- States: `is-test-origin`, `static-path-from-test-origin` (a static path, not executed coverage), `not-found-incomplete`, `unknown`.
- Joins: `J-TR-*`.

## 5. Evidence and limits

**Strict run.** Exit 0, `CHECK OK`, about 68 s. Every item below asserts an exact expected result.

1. Parent immutability, regeneration, owner admission and patch composition (§2 F5).
2. Identity bridge (§2 F1).
3. Glob law: 22 contract examples plus 3 more, agreeing with the pinned `workflows_model.v1.glob_match`.
4. Native model evidence.
5. Worlds validated against the owner schemas, including `RustUniverseV2ResolvedInputs`.
6. Positive derivations: mixed Rust + TS/JS (19 facts, 8 cells, 35 metrics, trace and test states), integration, cross-universe and jest-configured worlds.
7. Variants:
   - partial package inventory;
   - recognition not-plan-bound, purged, partial-missing and partial-present;
   - no reachability view;
   - 101 origins;
   - Cargo member root unresolved;
   - whole-view test bound;
   - zero under a limitation;
   - cross-program duplicate;
   - 100,001 call facts;
   - metric byte budget;
   - purged Run evidence.
8. Dense coupling.
9. Adversarial cases:
   - **42 document cases:** 34 refused by named joins, 8 by `SCHEMA`.
   - **14 recognition parameter cases.**
   - **7 host-derivation cases.** Prefix guess, symbol-spelling parse, symbol path instead of anchor, target-ownership-as-package and the browser entry-name heuristic all pass in-document admission and are refused only by the host derivation.
10. Report integration under parent07 `audit-full`.
11. Register, featureMap and requirement-text sentences.

**Limits:**
- **Synthetic inputs.** Worlds, the mock graph owner and the evaluator3 Runs are reference constructions: synthetic fixtures of the pinned owners, not product Runs, providers, stores or a browser.
- **Occupancy** reconciliation is given on facts.
- **Owner models.** The native, identity and evaluator models are executed. `query_projection_model.v3` is not, so S3 is specified by law and reference function only.
- **Overlay documents.** Documents read by owner code inside the overlay are this run's own byte copies. Only compiled overlay sources are re-verified at compile.
- **Proposals.** S1–S4 are unaccepted.
- **Not provided:** no runtime, browser, generator, performance or Run replay qualification, and no whole-report completion.
