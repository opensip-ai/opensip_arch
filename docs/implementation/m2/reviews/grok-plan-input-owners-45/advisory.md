# Advisory: Plan-scoped first-evaluation owner wrappers (45)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded review of four copied evaluator sources. **Not source acceptance. Not 43 freeze. Not runtime-19. Not full X / capture selection / enumeration / replay / M2.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-plan-input-owners-45/review`. Copied sources and trial/frozen trees were not edited.

Follows advisory 44. Root disposition **precision** (no selected X law change): helper 43 is `inspect_evaluator_parameters`; `EVALUATOR_EXECUTION_INPUT_SELECTION` has no extra `INPUTS` segment; X REFUSE has empty derived accounts/outcomes/deficiencies; owner checks are prerequisites to X, not deferred until after ADMIT. This unit is those Plan-scoped prerequisites only.

Inherits frozen 43 (currently under wH source review). **Must rebase accepted 43 before any future freeze.** Not approval of 43.

## Verdict

**PLAN-WRAPPERS-SOUND-FOR-BOUNDED-UNIT; REBASE-43-BEFORE-FREEZE.**

Shared Run tails keep frozen-43 guards, charge order, and local budgets. New wrappers do not mint a synthetic Run, do not accept caller ADMIT maps, and do not implement execution-input `SELECTED_COVER`. The initial missing-`evidence` compile failure is fixed: coverage membership is an explicit `ViewContext` field (Run: `evidence.coverageIds`; Plan: coverage-domain `ProofInputRef`s).

**requiredFindings:** none.

## Pins (copied = trial45 product; 4/4)

| File | Bytes | sha256 |
| --- | ---: | --- |
| `view_joins.rs` | 18822 | `9ab7fae993dbf1b0c0d9c3a01f41f505421489556fb83fe1034fd4f560d236fa` |
| `import_joins.rs` | 12068 | `6f74728c22365c2f95a2822d154bb66e4e576e5dbc799723da0d22916abca040` |
| `stage_output.rs` | 18268 | `6d6340e98e0b1da8cdde2afcaa4854e78546f8be052cf753d520b2fea7cb4a81` |
| `lib.rs` | 3291 | `e4668383b1cfec34dc0d334cdfc02e72b75aaca43f2c446cf3b14570a920b55c` |

Frozen-43 parents (byte-equal to SOURCE41 for the three owners; lib.rs already had 43 `inspect_evaluator_parameters`):

| File | Frozen-43 bytes / sha256 |
| --- | --- |
| `view_joins.rs` | 15794 / `ec5fa2487e330e419dacfe1aae778cf0ab456ffaa61d03394fe177f2c8c07bda` |
| `import_joins.rs` | 11077 / `01f8a3cf21bc3e2220e22a6240e645c43297e8937ed7b0684ed71c0175f7e2d6` |
| `stage_output.rs` | 17083 / `c7f34fdb81e6d054467bd818b521f7d9d64eb983db79ffe2097c18db029229a3` |
| `lib.rs` | 3148 / `1d927a65ec5ff6e5fd1ba07ad5f8b49b37f7f0c2570f48c0fcf994d0e5173704` |

`full_walk.rs`, `enumeration_join.rs`, `policy.rs` are **byte-equal** frozen43 ↔ trial45. Replay still calls the old Run wrappers.

## Extraction (lost-guard review)

**View.** `inspect_view_joins` still: limit on `steps==0 \|\| depth==0` → Run → Plan → snapshot from **Run.snapshotId** → semantic-evidence → `evidence.viewIds` contains `view_id` → tail. Tail is frozen-43 from the view record onward: `VIEW_PLAN_JOIN`, `UNSELECTED_PRODUCER`, enumerator kind, partition overlap, fact/anchor/UTF-8, `VIEW_COVERAGE_JOIN`, coverage producer, prerequisites, totality. `VIEW_PLAN_JOIN` now compares `text(view.planId)` to the context plan id string; for string locators this matches prior JsonValue equality against `run.planId`.

`inspect_plan_view_joins`: same entry limits → shape every `evaluation_refs` member as `ProofInputRef` (digest `^[0-9a-f]{64}$`) → `view2:{digest}` membership for this `view_id` (`ViewNotSelected` if absent) → Plan → snapshot from **Plan.snapshotId** → same tail. Coverage membership is `coverage2:{digest}` for `domain==coverage` refs, not evidence. Prefixes match `IdentityDomain::{View,Coverage}.prefix()`. Complete capture totality remains X.

**Import.** `inspect_import_joins` still loads snapshot from **Run.snapshotId**, then shared `inspect_import_context`. Plan form loads snapshot from **Plan.snapshotId**. Tail still: source-context decode-before-schema order, `IMPORT_SOURCE_JOIN` / mapping / VCS, then existing narrow `parameter_selection`. That last call is frozen-43 behavior, not a new grab of `inspect_evaluator_parameters`.

**Stage.** `inspect_stage_specs` still: `depth==0` → Run → Plan → **evaluation-seal** → execution-plan from seal → tail. Plan form: Plan + execution-plan, `execution.planId == plan_id` (`EXECUTION_PLAN_JOIN`), no seal. Tail still: `STAGE_SPEC_PLAN_JOIN`, unselected producer, outputDomain join, hidden parameters, `output_schema`. Stage-only helper does not require snapshot (separate prerequisite); mutation case 11 documents that.

No synthetic Run. No caller ADMIT maps. `lib.rs` exports the three Plan functions and **keeps** 43 `inspect_evaluator_parameters`.

## Independent checks

Pinned rustc/cargo **1.95.0** `--locked --offline`; CPython **3.12.13** `-I -B -X int_max_str_digits=0` for replay scripts. `CARGO_TARGET_DIR` under this review tree only.

| Check | Result |
| --- | --- |
| Copied pins vs trial45 product | 4/4 byte-equal |
| Evaluator `--lib` | 18 passed (includes preserved `stage_output` resource tests) |
| Mutation corpus 27 (missing/invalid/limit + ViewNotSelected + VIEW_COVERAGE_JOIN + VIEW_PLAN_JOIN + EXECUTION_PLAN_JOIN + STAGE_SPEC_PLAN_JOIN + IMPORT_SOURCE_JOIN) | **27/27** via rebuilt harness |
| Reference packets 42 (no output-domain objects) | **42/42** |
| Run-form host `view_joins` / `imports_join` / `stage_outputs_join` | 3 passed |
| Trial45 workspace vs frozen43 | both **132** passed; clippy `-D warnings` exit 0 |

Discriminating Plan-form refusals are typed `Err`, not ADMIT documents. Reference packets are admitted native/view/coverage/import objects, not complete X.

## requiredFindings

None.

## Residuals (not required findings)

- Plan view/coverage id formatting uses literal `view2:` / `coverage2:` rather than `IdentityDomain::prefix()`; currently equal to identity prefixes.
- Plan view only requires the named view’s coverages ⊆ coverage-domain refs; extra refs ignored. `SELECTED_COVER` is X.
- Plan import does not take `evaluation_refs`; import-vs-input-ref totality is I/X.
- Concurrent harness tests are not in the four pinned files; freeze must carry meaningful no-Run/refusal cases.
- Rebase onto **accepted** 43 before freeze.

## Limits

Not 43 source acceptance. Not runtime-19. Not full execution-inputs owner. Not capture selection, native Plan bind, enumeration join, or replay. Combined later acceptance must not waive 44’s Phase A/B split or reference42 locator totality.
