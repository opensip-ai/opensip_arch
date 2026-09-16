# Consumer24 workflow items M4, M5, S5, S6, S7, A6, A8, A9, A11, A12, A13 and A14: coauthor correction

**Standing.** This is an authorized architecture, design and reference correction by the same coauthor origin (f5617310…). It is not product implementation, independent acceptance or readiness.
- I made no pins, planning, grades, commit or push.
- Root integrates overlapping paragraphs with the native coauthor (M1/M2/M3/S1–S4/A1/A2/A4) and with root items A3/A5/A7/A10.
- No reference Python was made normative. Every law is published in prose and schemas.

## Custody and tree

**Initial custody.** The frozen source38 manifest `2ddfa0db…7e5c5` was verified. All 12,904 files matched and were copied as regular bytes into `work/source38-work`, with distinct inodes and `nlink` 1 (`receipts/parent-custody-and-copy.json`).

**Final custody** (`receipts/final-custody-and-diff.json`):
- The manifest bytes still match.
- The work tree has 21 changed files and no added or removed paths.
- Every changed file's parent copy still equals the manifest.
- All 27 dependency files are unchanged in both trees.

**Full diff:** `diffs/source38-to-corrected.diff` (2,048 lines, sha256 `b65201ad…d941ff`).

**Changed files** (source38 → corrected sha256):

| File | source38 | corrected |
|---|---|---|
| foundation/check-composition.v3.py | `99397b06…` | `aeb17e1d…` |
| foundation/check-replay.v3.py | `8405862f…` | `b1dd2052…` |
| foundation/evaluator-composition-contract.v3.md | `1640740f…` | `357e90fd…` |
| public-detail-registry.v1.json | `39ec20cd…` | `c4627126…` |
| workflows/check-query-projection.v3.py | `82eddd74…` | `26dac0f9…` |
| workflows/check-workflow-projection.v3.py | `4f356745…` | `f357ad17…` |
| workflows/command-inventory.v3.json | `c12ca4e8…` | `d456c8d9…` |
| workflows/query-projection-contract.v3.md | `6a504eb5…` | `34b744f1…` |
| workflows/query_surface_projection.v3.py | `e23c3d0b…` | `188d51c3…` |
| workflows/schemas/common.schema.json | `f73094dd…` | `7767a195…` |
| workflows/schemas/evaluator3/baseline-artifact.schema.json | `786e99af…` | `d5126989…` |
| workflows/schemas/evaluator3/command-envelope.schema.json | `57555caf…` | `c2205d67…` |
| workflows/schemas/evaluator3/command-inventory.schema.json | `729bf198…` | `42d065d3…` |
| workflows/schemas/evaluator3/common.schema.json | `36124787…` | `5e6e0490…` |
| workflows/schemas/evaluator3/comparison-result.schema.json | `205ab9d7…` | `0d5c8a96…` |
| workflows/schemas/test-execution.schema.json | `8c1f5bee…` | `a6f7c2d8…` |
| workflows/workflow-projection-contract.v3.md | `1f8128bb…` | `6fe7bf03…` |
| workflows/workflow_projection_model.v3.py | `50fef99c…` | `bca6e1e6…` |
| v2 native-evidence.md | `cfe69627…` | `a8cbb3b8…` |
| v2 security-and-lifecycle.md | `9ca85de1…` | `4fb55aaf…` |
| v2 workflows-and-surfaces.md | `857d6bbe…` | `71078934…` |

Full hashes are in `review.json#/finalCustodyAndDiff/changedFiles`.

## Focused checks (reference interpreter `-I -B`, foreground)

| Checker | Baseline (unmodified) | Final tree |
|---|---|---|
| workflows/check-workflow-projection.v3.py | 493 pass | **585 pass** |
| workflows/check-query-projection.v3.py | 193 pass | **202 pass** |
| foundation/check-current-profile.v3.py (runs `run_projection_controls`) | 22 pass (parent, read-only) | **36 pass** |
| foundation/check-composition.v3.py | 20 pass | **30 pass** |
| foundation/check-replay.v3.py | 68 pass (parent, read-only) | **73 pass** |
| workflows/check-comparison-knowledge.v3.py | pass | pass |
| foundation/check-semantic-replay.v3.py | 30 pass | 30 pass |
| foundation/check-evaluator-faults.v3.py | 41 pass | 41 pass |
| workflows/check_workflows.v1.py (retained profile) | exit 0 | exit 0 (stdout identical) |
| check-integration.py (registry/mirror parity) | 412 pass | 412 pass |
| security/check-security-lifecycle.v1.py, owner launcher | exit 0 | **not executed**: source-pin gate lists the 21 changed files |
| Same checker body via the labelled unpinned driver | 464 cases, 11 sweeps (parent) | 464 cases, 11 sweeps hold |

The unpinned result is not a pin-valid pass. Root must rerun the owner launcher under updated pins.

## Items

### M4: detector identity

**Law.** Published in workflows-and-surfaces §2 (**Detector identity**), workflow-projection-contract §2/§3/§11, and the baseline-artifact schema descriptions:
- `detectorClosure` has exactly one row per emission-plan `contributionId`, disabled rules included.
- `detectorId` equals `contributionId`, and closure and major equal that row's `detectorClosure` and `semanticsMajor`, which must equal the rule's `ruleProgramRef` major.
- A conflicting row refuses.
- Every entry's `detectorId` is its rule's contribution.

`verify_baseline_artifact_v3` enforces these joins *after* recomputing `baselineId`.

**Before and after** (same fixtures, `receipts/identity-effects.json#/M4`):

| Case | Before | After |
|---|---|---|
| Reminted rename (schema-valid) | verify OK | `CONFIG.INVALID / EVALUATION.FINDING_JOIN_REFUSED` |
| Entry detector outside the closure | admitted | refused |
| Conflicting contribution row | admitted | refused |
| Stale-hash rename | `IMPORT.ARTIFACT_CORRUPT` | `IMPORT.ARTIFACT_CORRUPT` |

**Checker fixture change.** The historical `art_extra` fixture reminted a baseline with a non-contributing detector row. It is now refused at admission; the control proves the boundary by refusal message. E0 exact-map refusals remain covered directly.

### M5: public query carrier

**Producer inventory.** `kind=query` is emitted by:
- the query command (all 20 graph-query:3 operations; the only command whose parity fields include `query-response`);
- eight other query-class commands: `recommend`, `baseline-show`, `policy-show`, `policy-test`, `candidates`, `inspect`, `review-brief` and `repair-preview`.

invocation:3 carries only the compact `QueryResult`. A globally required response would therefore make eight commands unrepresentable.

**Correction.**
- The envelope requires `querySurface` on `kind=query`.
- `graph-query-response` requires `queryResponse`, the complete `GraphQueryResponseV1`.
- `command-owned-summary` forbids `queryResponse`.
- Non-query kinds forbid both fields.
- The reference renderers emit JSON as that envelope, agent as the envelope plus `agentHints`, and human as labelled parity. Parity is recovered from each rendering.
- A missing carrier is `DELIVERY.REQUIRED_FAILED` / `DELIVERY.REQUIRED_PROJECTION_FAILED` with no `runId`.

**Selectors.** Envelope schema, workflows §8 (**Public query carrier**), inventory JSON `parityRule`, query contract §7, and `query_surface_projection.v3.py`.

**Controls.**
- Projection controls, executed by current-profile.
- A retained owner-admitted `graph.neighbors` response (through `close_run`), carried and rendered in check-query-projection.

**Effect.** Breaking within major 3: a compact-only query envelope was admitted before and is refused after. Root decides between a pre-release correction and a major bump.

### S5: argv digest

`argvDigest` is the lowercase hex raw SHA-256 of `C(exact ordered argv)`:
- Every member is preserved, including repeats and empty strings.
- No shell-joined surrogate is used.
- One recipe covers the grant and `TestPayloadV1`.
- It digests host test params, the host-selected preparation argv, and adapter-recorded argv.

**Selectors.** workflows §7, security S10 and the native preparation grant.

**Controls** (through `admit_test_execution`):
- the exact digest admits;
- a shell-joined surrogate, repeat or reorder is refused with `TEST.PRINCIPAL_NOT_ADMITTED`;
- the join collision is demonstrated;
- the payload uses the same recipe.

Schema descriptions are unchanged.

### S6 and A13: public details

**Registered** (registry and both common mirrors): `DOCTOR.REPORT_NOT_PRODUCIBLE`, `OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED` and `DELIVERY.REQUIRED_PROJECTION_FAILED`.

**Goldens.**
- `query-latest-empty` carries `QUERY.VIEW_UNKNOWN`, matching the query contract row.
- The other two goldens carry their new details.
- The Golden schema requires detail on request-rejected and operational-failed goldens unless `detailSuppliedBy` names the native route composition.
- No D9 class or code was added.

**StepTermination** (both mirrors):
- `RENDERER_FAILED_AFTER_COMMIT` requires `runId`.
- `REQUIRED_PROJECTION_FAILED` forbids `runId`.
- Both are `operational-failed` / `DELIVERY.REQUIRED_FAILED`.
- Other operational failures keep their optional `runId`, and exclusivity is retained.

**Controls.**
- Every v3 failure golden forms a lawful failure envelope.
- Each of the three is refused without errors and admitted with its detail.
- The pre-commit and post-commit discriminators hold in both mirrors.
- Integration parity holds (412).
- The closed-registry sweep holds.

### S7: presence knowledge

**Law.** workflows §3 (**One presence-knowledge law on every side**), projection contract §12/§13, the comparison schema, and the model.
- B, E0–E3 and E4 are each `true`, `false` or `null`.
- `false` is either:
  - **non-selection**: the side's policy does not enable the rule, or its ScopeDocument does not select the path. This attributes the change to the policy or scope axis. It is never CODE-FIXED, because B, E0 and E1 share the baseline selection.
  - **evaluated absence**: the complete-hit-set law holds, with the attested path extent.
- The baseline records `RuleCoverage.absenceKnowledge` at adoption.
- If an entry's first attributable change rests on `null`, the entry is INDETERMINATE with `current-absence-unknown` or `baseline-absence-unknown`.
- A known earlier change keeps its classification, and deficiencies stay independent.

**Counterexample built before correction** (full `compare_admitted_v3` over `close_run`-admitted Runs):

| Current Run (gating and non-gating) | Before | After |
|---|---|---|
| Partial inventory | CODE-FIXED ×2 (one subject still present, unmatched) | INDETERMINATE `current-absence-unknown`, E4 null |
| Budget exhausted | CODE-FIXED ×2 | INDETERMINATE `current-absence-unknown`, E4 null |
| Complete removal | CODE-FIXED | CODE-FIXED (control) |
| Unchanged | UNCHANGED | UNCHANGED |

**Additional controls.**
- A budget-exhausted baseline records unknown absence; a later hit is `baseline-absence-unknown`, not CODE-NET-NEW.
- A known CODE-NET-NEW still fails over unknown absence.
- A disabled current rule with a bound E1 is POLICY-DELTA vanished; without E1 it is `pivot-reevaluation-unavailable`.
- The current law equals the pivot law.

My first law treated non-selection as unknown. The existing control `wider-scope-does-not-false-absent-unselected-current-paths` refuted it (run after-edits-3), and that led to the non-selection clause.

**Identity effects.**
- Every baselineId changes (`f2ab44c6…→44951dfd…`, `4dcd1081…→191da4dd…`).
- Every measured comparisonResultId changes.
- Unknown-absence entries are reclassified.

### A6: correspondence precedence

**Law.** Composition contract §4/§9.5/§9.7:
- First applicable wins: `projection-unavailable` > `population-incomplete` > `signature-ambiguous`.
- A duplicate projection refuses first.
- An anonymous subject is kept unmatched by those three causes (identity-and-evidence §3); `anonymous-subject` stays closed and is never emitted.
- There is one deficiency per unmatched finding, and `reason` equals it.

**Controls.**
- Synthetic co-occurrence cases.
- Complete replayed Runs.

The reference behaviour is identical before and after, so there is no identity change.

### A8: routes

- Query contract §7 row: request `projectId` ≠ Run → `REQUEST.PRECONDITION_FAILED` / `QUERY.PARAMS_MALFORMED`.
- workflows §2 and projection contract §14: present listing refusal → `REQUEST.PRECONDITION_FAILED` / `EVALUATION.PROJECTION_INPUT_INCOMPLETE`.
- Messages remain diagnostic.

**Controls.** Owner retained-Run refusals plus a contract-row join.

### A9: required evidence independent of the root

**Law** (composition §5/§9.5). A required `evidence-kind-unavailable` deficiency makes an enabled gating rule indeterminate whatever its root value. A live unwaived finding still fails, and an advisory rule passes.

**Controls.**
- Composed cases.
- Complete replayed Runs: a false-root gating Run is indeterminate with roots `{false}`; a live failure still fails; an advisory Run passes.

Reference behaviour is unchanged.

### A11: enforcement vocabulary

Membership is necessary, not sufficient: the value must equal the selected truth-table profile row.
- v9 has 0 platform-primitive rows (measured), so `ENFORCED-PLATFORM` cannot be claimed in this profile.
- `EnforcementV1` retains that future vocabulary, which needs successor truth-table and schema versions.
- `ENFORCED-AT-HOST-BROKER` is still refused by the truth-table equality check.

The change is a description plus workflows §7. The schema SHA appears only in pins and in `workflows-report.v1.json`.

### A12: hidden gate reason

The existing `code-net-new-policy-hidden` covers any later detector, policy, scope or waiver axis; `subsequentDeltas` names it. Updated in workflows §3 and the `gateReason` description. No new enum.

### A14: preserved

The deliberately conservative evidence attribution, with its named successor path, is unchanged. The control confirms the text. It is the selected owner law, and changing it would add an unselected counterfactual evidence pivot.

## Failed attempts (preserved)

1. **carrier-v3** could not run: it needs SRC/ROOT/OUT arguments, and it is not used here.
2. **Probe A11 section** failed on a wrong path; the retry ran on the unmodified tree.
3. **after-edits-2 crash** at `art_extra`, now converted to an admission-boundary control. The first draft read `exc.args`; it was corrected before application.
4. **Owner security launcher** is pin-gated. The unpinned driver is labelled as such.
5. **after-edits-3 failures:**
   - the wider-scope discriminator, which produced the non-selection law;
   - the a12 whitespace mismatch.
6. **Partial application** of `apply_s7_nonselection.py` (anchor backticks), resumed by a separate script.
7. **Self-caught authoring defects:**
   - a tautological A6 control was replaced before application;
   - a convoluted argument was simplified;
   - an applied, non-discriminating S7 schema control was replaced with three discriminators.

## Remaining integration needs

- **Pins and planning** for all 21 files. The command inventory is also referenced by the `docs/v2/architecture` implementation JSONs.
- **Overlap integration** of shared paragraphs and files: workflows §2/§3/§7/§8/§9, both common schemas, the registry and the composition contract.
- **Major decisions:**
  - envelope:3 `querySurface` is required and breaking;
  - baseline:2 `absenceKnowledge` changes every baselineId;
  - comparison:2 nullable presence changes comparison ids.

  Historical subjects are not rewritten.
- **R1** (measured, not closed). A subject that becomes unmatched through a signature collision under *complete* enumeration still yields CODE-FIXED.
  - Gating verdict: indeterminate (correspondence-incomplete).
  - Non-gating verdict: `pass`.
  - A same-path guard would contradict the selected projection contract §12 example (empty baseline plus unmatched, then pivot-only CODE-NET-NEW), so this needs a root decision.
- **R2** (measured). Eight other query-class commands have parity fields with no envelope carrier. Also, `QueryParams.operation` is typed by the graph-query `Operation` enum, which has no operation for recommend or policy-test (observed only).
- **Baseline evaluated absence** is per rule; baseline:2 has no per-path extent.
- **Pre-existing:** `check-workflow-projection` reads two external historical `/tmp` files.
- **Profile-1 artifacts** are intentionally unchanged.
- **Not done:** no product renderer or host qualification, and consumer24 exports were not revalidated.

## Limits

- Fixtures are finite and synthetic, admitted through `close_run`; unit projections are labelled.
- The human rendering is a reference parity projection, not UI.
- The current-side path extent reuses the pivot predicate; no real extraction was exercised.
- No global suites were run.

Receipts: `receipts/**` (hashes in `review.json#/receiptSha256`). Tools: `tools/*.py`.
