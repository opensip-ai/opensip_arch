# SOURCE27: retained import correspondence and global parameter selection

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Frozen private source review of `inspect_import_joins` / `inspect_parameter_selection`. **Not runtime selection. Not layout-22. Not two-key import-payload walk. Not replay. Not caller ADMIT.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-import-joins-review-27/review`. Export `/tmp/opensip-implementation/m2-import-joins-subject-27`. No live/frozen/history edits.

**subjectManifestSha256:** `279a2f935a10a428b7374c6fd7805c9e8aa52ce7077c415d6e6bc7c56328754e` (`docs/implementation/m2/trials/import-joins-27/subject.json`, **49982**). **277/277** files pin-match, string-path sorted, no duplicates. Archive `subject.tar.gz` **2638423** / `00bfb659…ef98`, 277 members.

Archived advisory + order-precision are read, not rewritten. Exact-profile outcomes take precedence over the original test-table shorthand for mapping order/duplicate.

## Verdict

**NO-REQUIRED-FINDINGS.** Pure retained correspondence and global parameter selection match selected `open_run_closure` 1951–1986 and `admit_parameter_selection` 147–187, including the order-precision fault split. Two-key `payloadClass==import` walk and a public 9-row staleness API are **not** claimed.

## API authority

`crates/evaluator/src/import_joins.rs` **11077** / `01f8a3cf…e2d6` (new). `no_std`, `forbid(unsafe_code)`, identity-only Cargo. Two public functions:

- `inspect_parameter_selection(inputs, analysis_digest, budget) -> Result<(), ImportJoinError>` — rehashes `analysis-spec` shape; does not walk parameter payload refs.
- `inspect_import_joins(inputs, run_id, budget) -> Result<ImportJoinChecks, ImportJoinError>` — `ImportJoinChecks` is an import **count** only.

No ADMIT token, no caller-supplied registry, no `classify_staleness` export, no payload-class import owner. `RetainedInputs::object` already checks import `producerClosure=provider` and `adapterClosure=adapter`; the wrapper maps `ClosureRole` to `CLOSURE_FIELD_KIND:import.{field}:{expected}` (initial 99-case run had 6 diagnostic mismatches from duplicating that check; preserved under `initial-role-diagnostic/`, then mapped typed).

Host `imports.rs` is still absent. This is not I/O/receipts.

## Phase order (selected)

1. If `plan.importIds` nonempty: count import-source-context parameters → `IMPORT_SOURCE_CONTEXT_MULTIPLE` if >1; zero legal.
2. One context: decode canonical **payload** blob before `registered_record_shape` (schema artifact). Preserves compound store-fault order.
3. Per Plan import: `object(import)` roles, then `current_record_shape` SourceCorrespondence.
4. `exact-snapshot`: identity compare → `IMPORT_SOURCE_JOIN`. No staleness call.
5. `vcs-revision`: null mapping pointer → **named** `IMPORT_SOURCE_MAPPING_REQUIRED`. Else foreign SourceMappingV1 (**schema/order/uniqueItems/LogicalPath** fail as `Record` / harness `invalid` = `REGISTERED_RECORD:#/$defs/SourceMappingV1`, **before** SHAPE). Extra snapshotId / inventory digest (and a defensive generatedPath UTF-8 increase) collapse to `IMPORT_CORRESPONDENCE_SHAPE`. Consumability projection → `IMPORT_VCS_JOIN` if not consumable.
6. **Always** `parameter_selection` last, including Plans with **no** imports.

MOST SPECIFIC FIRST: imports + two context rows → `IMPORT_SOURCE_CONTEXT_MULTIPLE`; no imports + two context rows → `ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS:foundation/import-source-context.schema.json`.

## Metadata

`import-registry.json` **1534** / `8e54e247…36c2`, `include_bytes!`, not caller-selected. Five rows, 311c insertion order, `atMostOnePerSpec: true`. Each `sha256` equals the bound source-alias document in this tree (and 311c `requiredForEvaluatorMajors` containing 3 ↔ `requiredForEvaluator3`). Aliases exist in unchanged `schema_registry.rs`. Unregistered/ambiguous digest matches are skipped here (payload admission’s duty). First missing required row follows source registry order (enumeration-plan before emission-plan).

## Staleness consumability (projection, not the 9-row table)

After a mapping is shape-admitted, selected `classify_staleness` is consumable only for `commit-equal-clean-mapped`. The owner inlines that caller condition:

`vcs.kind != none` ∧ commit equal ∧ (`buildIdentity` null ∨ ∈ `declaredBuildIds`) ∧ both dirty flags false.

Wrong-build is still decided before dirty in the selected table; both still refuse `IMPORT_VCS_JOIN`. Mapping digest ∈ `admittedSourceMappings` is implied by loading the correspondence digest through `foreign`. Exact-snapshot table rows and `corrupt=True` are unused here, as selected. This is **not** a public 9-row API.

## Comparisons and tests

- 408 selected-I/W oracle rows, 41 checked, **0** expected/actual mismatch. Includes **243** parameter-cardinality combinations (`3^5`) and **48** staleness-matrix cases. Oracle: selected identity import AST + 7 helpers + parameter selection, selected W mapping/staleness, explicit local payload-walk shim. Not full import-payload walk.
- Host fixture **111** cases, **1980785** / `894015b4…d5ea`, under unchanged `MAX_BYTES` 4MiB. Keys = first 117 oracle labels minus `zero-*`. Prior native fixture **3736129** / `9d18cfd1…227f` **byte-identical** stage-output-26.
- Reproduced frozen export: `cargo test --locked --offline` `native_owner_tests::imports_join_retained_source_revision_build_and_parameter_selection` **ok** (rustc **1.95.0**). Subject `workspace.stdout` sums **119** passed; Clippy deny-warnings clean; identity-policy **110** source files, TCB `sha2-const-stable=0.1.0` / `unicode-normalization=0.1.24` (+ tinyvec transitive).

## Delta versus frozen 26

Two changed inputs: `crates/evaluator/src/lib.rs` (export only), `crates/host/src/native_owner_tests.rs` (one new test). Three new files: `import_joins.rs`, `import-registry.json`, `import-joins-fixtures.json`. Identity/policy/Cargo/TCB/native fixture/stage_output body unchanged. Live tree still has **no** `import_joins.rs`.

Private inherited `product/design-lock.json` **36241** / `515f092c…b523` is **9 inventory / 15 contract**, **not** live. Independently, live lock is **19 / 28** (`59148` / `f1d12e90…ae74`, last contract `native-runtime-selection-v13`). Layout-22 is separately proposed and not reviewed. Future integration must recompose the current live base.

## Limits (not claimed)

Two-key import payload / workflow-registry drift / full walk; catching `Unsupported` as success; 9-row staleness public API; host I/O `imports.rs`; `IMPORT_JOIN` / `IMPORT_OPERATION_JOIN` (already `run_links.rs`); `close_run` / ReplayedRun; caller ADMIT; live install; layout-22; runtime selection; M2–M6 complete; Claude agreement; product qualification.

Original advisory.md/json and followup-order-precision.md/json remain the boundary record. Combined later acceptance does not waive this unit.
