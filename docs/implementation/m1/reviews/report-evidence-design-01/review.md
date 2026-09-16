# Independent review: report evidence design subject-01 (RP-DO-03/05/09/10)

**Decision: changes-required.** Four High findings were reproduced independently. Three Medium and two Low findings follow.

This is a design/reference review. It does not claim production, runtime, provider, browser, generator, performance or Run replay qualification. Catalogue, timing and configuration proposals are separate and unaccepted, and this review does not assess them.

## Custody and reproduction

| Check | Before | After |
|---|---|---|
| Outer manifest sha256 | `0af84231…a11` ✔ | `0af84231…a11` ✔ |
| Exact subject file set | 13 ✔ | 13 ✔ |
| Inner manifest vs outer | agree ✔ | agree ✔ |
| External pins | 47/47 ✔ (0 listings) | 47/47 ✔ |
| `__pycache__` in subject | none | none |

- **Copied run.** I ran `check.py --subject-strict` on my own copy (`copy/subject`). It exited 0 with `CHECK OK`, and the result file is **byte-identical** to the root validation `result.json` (sha256 `5c7ea5c6…`).
- **Python flags.** Every run used `metadata-reference-env/bin/python -I -B`.
- **Loader.** The reviewer harness compiles verified source bytes, refuses sourceless modules, and raises on any `.pyc` open or any write outside this directory.
- **Bytecode scan.** No new `.pyc` was found under the subject, the architecture docs or this directory.

## Findings

### F1 — High: the S2 required parameter row breaks the claimed historical Run behaviour

**Claim.** Historical Runs "stay admitted under their own profile" and show `not-plan-bound`, and no vocabulary is widened (`owner/identity-parameter-registry-patch.v1.json#/identityEffects`).

**Owner law.** `foundation/identity-model.v3.py:147-187` `admit_parameter_selection` is "pure over the parameters array". The retained Run closure calls it. It refuses `EVALUATOR_REQUIRED_PARAMETER_MISSING` for every row with `requiredForEvaluatorMajors ∋ 3` and has no profile dispatch.

**Reproduced** (`evidence/probe-owner.json` P1, pinned identity-model.v3 executed in memory):
- The current required selection is admitted.
- With the S2 row added, the same selection is refused with `EVALUATOR_REQUIRED_PARAMETER_MISSING:foundation/framework-recognition-plan.schema.v1.json`.

**Consequence.** `not-plan-bound` only exists through the synthetic `recognition.planBound` flag (`build_fixtures.py:137`). RP-EV-INT-IDENTITY's "successor profile" names a mechanism that does not exist.

**Fix.** Pick one owner mechanism and execute it against `admit_parameter_selection` and `close_run` with a retained predecessor Run:
- a profile-qualified requirement field (an identity successor, which means the vocabulary *does* change);
- an optional row, with absence mapped to `not-plan-bound`;
- or a new evaluator major.

### F2 — High: cross-universe test callers are ignored, giving an unsound `no-static-path-within-bound`

**Candidate code.**
- `reference_model.py:1053` keeps only reach hits in the subject's universe.
- `test_blockers` (`:1017-1025`) and origin-set derivation (`:1037-1039`) only consider that universe.

**Owner law.** `calls` has universe rule `admitted-target` (query contract §3), and R07 requires binding to the exact universe/identity (`prototype-report-inventory.md:67`).

**Reproduced** (`probe-candidate.json` C1):
- **Setup.** The integration world with the test file in its own tsjs unit/universe, all records schema-valid.
- **Reach.** The walk returns `ts:tests/helper.test.ts#t` at depth 1. That universe's origin set is `declared` and contains it.
- **Result.** The helper row is `no-static-path-within-bound` with no blockers. The patched schema and host admission both accept it.
- **Baseline.** The unmodified world gives `static-path-from-test-origin`.
- **Mutation.** Mutant M4 (filter removed) survives the check.

**Fix.** Derive and match origin sets per universe for every universe among the reach items. Add a blocker when a reached universe has no declared set. Add C1 as a fixture.

### F3 — High: `declared` TS/JS origin sets rest on default globs that ignore the jest configuration

**Owner model.** `native_evidence_model.v2.py:3544-3548`: when `package.json` has a `jest` key, the recognizer always emits the default globs with `assurance: declared` and no `unresolvedChoices`. It never reads `testMatch`, `testRegex`, `roots` or `projects`.

**Reproduced.**
- `probe-owner.json` P2: a `package.json` with `testMatch: ["**/tests/**/*.it.ts"]` yields the default globs, and none of them matches `tests/parse.it.ts`.
- `probe-candidate.json` C2: with the jest-configured test `src/helper.it.ts` calling `helper`, the origin set is `declared` with 0 origins. Both subjects come out `no-static-path-within-bound` with no blockers, and schema and host accept.

**Fix.** Either:
- treat recognizer globs as `partial` (e.g. limitation `recognizer-default-globs-not-configuration`); or
- extend S1 so native reads the jest/vitest test selection as data and reports unresolved choices.

Add C2 as a fixture.

### F4 — High: Cargo workspace member entry points are dropped while the unit reports `all`

**Owner model.**
- `discover_units` folds member packages into one `cargo-workspace` unit. The probe shows one unit with `memberPackageRoots [crates/app, crates/core]`.
- `recognize_frameworks` reads only the root `Cargo.toml` and `src/main.rs|lib.rs` (`:3560-3563`).
- The proposed FR-7 (S1) fixes recognition at that workspace granularity.

**Reproduced.**
- **Native model** (P2): a workspace root with a package and a member binary gives `{all, recognized}` with only `src/main.rs`.
- **Candidate's own expectation** (`check.py:523`) and C3: `rs:core::shared_fmt`'s only reachability origin is `rs:app::main` in `crates/app/src/main.rs`. That path is owned by the **selected** `bin` target `app`. The trace is still `no-entry-origin` with `blockers: []`.
- **R12 conflict.** R12 (`prototype-report-inventory.md:97`) requires the stated scope to be honest, and this trace does not meet that.

**Fix.** Recognize per member package or per selected Cargo target root, and commit that in FR-7 and the parameter. Otherwise mark workspace units with members as `partial` (or add a blocker). Update the `check.py:523` expectation.

### F5 — Medium: S4 remove-rows ops do not compose with another obligation's exact ops

**Claim.** The patch says the ops commute with other successors, but `check.py:378-388` only proves set semantics through a helper that ignores `before`/`after`.

**Reproduced** (C4): I built an RP-DO-11 `step-duration` patch with the same exact before/after discipline over the 8 shared selectors. Applying both through check.py's own `apply_patch`:
- this patch then RP-DO-11 → `patch before mismatch /$defs/FeatureId/enum`;
- RP-DO-11 then this patch → the same refusal.

**Fix.** Make remove-rows match-based with explicit preconditions, or publish a rebase law. Then test both orders with real ops.

### F6 — Medium: the coupling panel has no byte projection for owners, cells or targetBuckets

**Gap.** RP-EV-INT-BUDGET projects only metrics and drilldown. The schema admits up to 1,000,000 cells, and `check.py:752-757` measured only the 39,085 B integration panels.

**Failed first probe, kept as evidence.** C7 hit foundation `canonical.canonical` → `BYTE_LIMIT` (`canonical.py:7,72-73`, 4 MiB) while canonicalising a dense 120-package panel.

**Corrected check** (`probe-c7-sizes.json`, element-wise canonical bytes):

| Dense packages | Panel bytes | Over the 4,194,304 B cap? |
|---|---|---|
| 40 | 1,224,223 | no |
| 80 | 3,000,064 | no |
| 120 | 5,959,928 | **yes** |

`admit_coupling` accepts all three, and `drilldownProjection` is the panel's only projection member.

**Fix.** Add cells/owners byte-budget projections (or a whole-panel omitted state) and put the new panels into the projection priority. Test at the schema maxima.

### F7 — Medium: gaps in check.py coverage

**Mutants.**
- **Survived:** M4 (cross-universe filter), M7 (whole-view `countBasis` forced exact; `reference_model.py:382`), M8 (metric `zeroSupportsAbsence` ignores limitations; `:611`).
- **Killed:** M1, M2, M3, M5, M6.

**Vacuous featureMap check.** `check.py:770` passes a nonexistent final member (C5 bogus ref). The 10 real refs do resolve.

**Fix.** Add fixtures for >100,000 imports (or a lowered test bound), an exact zero under limitations, and a cross-universe caller. Resolve refs fully.

### F8 — Low: duplicate provenance across universes inflates coupling counts

C6: the same `packages/shared/src/format.ts` import observed by two programs moves the shared→web cell from 1/1/1 to 2/2/2 (facts/edges/importerSymbols), and it is accepted. **Fix:** add a universe-independent distinct count, or a const count-unit disclosure.

### F9 — Low (not reproduced; design question): importer path source

The candidate attributes importers through symbol inventory rows (`reference_model.py:453`). The native ownership selection law keys on the **fact anchor path** (`native-evidence.md:4041-4044`), and `imports` carries source-text anchors. No provider data was available to show a divergence. **Fix:** justify this against the imports producer, or expose anchors in S3 and attribute by anchor.

## Verified without finding

- **Identity recipes.** Candidate `native_h` equals the pinned `native_identity` for `FrameworkRecognitionV1` and equals `source_unit_id` for `UnitIdentityV1`.
- **Rust ownership order.** `path_owner_keys` follows `native-evidence.md:4038-4050`: partial → equal path → selection → no fallback. M2 is killed.
- **Unit-root-relative glob slicing** is enforced (M6 killed).
- **Rust origin set** is const `partial`.
- **Metrics cap.** `metrics maxItems 320` = `maxPlannedSubjects 64 × 5`.
- **Unknown on continuation.** A continuation cursor gives `unknown`.
- **Imported testId** is refused as an origin.

## Observations

- **O1.** Explicit `discovery.entryPoints` turn every unit into `{all, explicit}` (C9), which removes `entry-recognition-not-all` everywhere. FR-2 and §4.5 item 2 arguably support this, so it is disclosure-only.
- **O2.** S3 looks implementable from `query_projection_model.v3` internals (`select_views`, `collect_projected_edges`, `relevant_resolution_limitations`). Neither the candidate nor this review executed it, and its produced-item law without a cursor is unstated.

## Limitations

- **Synthetic inputs.** Worlds, graph owner and parameters are synthetic. Source data and synthetic admitted dictionaries are not runtime custody.
- **Not run:** no engine, provider, store, generator, browser or measurement.
- **Unpinned sources.** Owner-model sources read outside the 47 pins are hash-recorded in `evidence/probe-*.json` (`compiledSources`, `openedGovernedFiles`).

## Evidence index

| Evidence | Files |
|---|---|
| Custody | `evidence/custody-{before,after}.json` |
| Copied check run | `evidence/copy-check-*` |
| Owner-model probes | `evidence/probe-owner.json` |
| Candidate counterexamples | `evidence/probe-candidate.json` (includes the failed C7) |
| Corrected size probe | `evidence/probe-c7-sizes.json` |
| Mutants | `evidence/mutants.json`, `evidence/mutants/*` |

The scripts are in `scratch/`, and their sha256 digests are listed in `review.json`.
