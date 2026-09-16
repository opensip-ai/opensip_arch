# RESUMED INDEPENDENT DELTA REVIEW: interruption05 (m1-interruption-envelope-subject-05)

This continues review01/02/04; it is not a fresh session. Reviewer: actual Claude (claude-opus-5). No subagents, background jobs, commits, pushes or private-session inspection.

## Verdict
**Accept-conditional (delta only; not selection, not promotion).**

- **V1–V4 are fixed and adequately tested.** The accepted optional-Run owner decision and the withdrawn F3 query premise are preserved.
- **No defect was introduced in the join mechanics.**
- **One owner decision remains before selection (R1):** `availability` on interrupted outputs with no committed Run.
- Parent envelope5 is still the unchanged, unaccepted bytes, also unchanged in report06.

## Custody
- Manifest `34556f3f…530f` verified. Closure is **48/48 exact** on the original and my copy, before and after.
- **37/37 pins** match external sources and copies, before and after; the set is identical to subject04.
- Envelope5 `45de2b0a…` equals report-projection **subject-06** envelope5. Schema6 is byte-identical to subjects 01–04.
- Delta from subject04 (7 files changed, none added or removed):
  - `ledger_join.py`: exact kind equality; the deterministic errors rule; the payload refusal on no-Run outputs.
  - Prose: both before-images unchanged; the error rule and the settled-vs-interrupted Run-identity asymmetry are now stated.
  - `owner_model_probes.py`: verify workflows added.
  - `contract.md`, `join_probes.py`, `root-result.json` and `successor.json`: updated to match.
- Execution:
  - Runs only from the copy: reference env `-I -B`.
  - A fresh private `PYTHONPYCACHEPREFIX`; own TMPDIR.
  - Verified bytes compiled directly. No pyc or `__pycache__` in either subject tree afterwards.
- Writes: only this directory.

**Root checker:** exit 0, and its output equals `root-result.json`:
- 42 shape;
- 59 join/preplanning/payload;
- 43 metadata;
- 102 owner-model scenarios, 9 of which change the Run choice;
- 12 shape-valid wrong-kind verify refusals.

## Independent probes (`work/probes05.py`, 47 rows, all as designed)
I used my own ledger builders (repair values from pinned fixtures), fed into my own extraction of the pinned owner model, before and after my own application of the one-line successor.

- **V1 (result kinds).**
  - `TestExecutionStepResult.kind` is const `test-execution`, so exact equality is safe for the one result type reached through a `$ref`.
  - Required and optional **repair-preview → repair-apply → verify → render** ledgers, at no signal, cut 2, cut 3 (verify committed) and cut 4 (after settle), are all valid and accepted on the failure, run and invocation outputs that apply.
  - Refused, with both shapes valid:
    - a verify step with `kind=analysis`;
    - an analysis step with `kind=verify`;
    - an apply step carrying a preview result.
- **Model.**
  - My repair ledgers give exactly 3 changed cases (optional verify, cut 3, × 3 signals). Step results and exits are identical, consistent with root's 9.
  - Optional verify: settled result is `success`, exit 0; interrupted before render it names the verify Run, exit 130.
- **V2 (errors).**
  - Exact non-empty lists are accepted on failure, invocation and run outputs. Omission, `[]`-instead-of-list, duplication and a changed remedy are refused.
  - Empty list:
    - failure with `errors:[]` is accepted; with errors absent it is shape-refused;
    - an invented detail is refused;
    - run and invocation outputs with errors absent are accepted; with `errors:[]` they are shape-refused and join-refused.
  - Across four shape-valid ledgers there is **exactly one lawful errors form for each output kind**.
  - A synthetic skipped step carrying a detail is excluded, and an optional indeterminate detail is not projected.
  - A required operational fault followed by a cancelled render gives an interrupted aggregate that masks exit 4. That is the existing cancellation law, unchanged.
- **V3 (payloads).**
  - Refused: a no-Run failure carrying `findings` or `availability`, and a no-Run invocation output carrying `availability`.
  - A run output carrying `availability` is accepted.
  - The schema6 empty form already refuses `availability`.
- **Regressions.**
  - Preplanning is accepted, and non-empty errors there are refused.
  - After settle, the class is kept and reclassification is refused.
  - Erasing an optional verify Run is refused.

## Previous findings
| | Disposition |
|---|---|
| V1 | **Fixed.** Exact `spec.kind`, including verify. |
| V2 | **Fixed.** One projection per output kind, matching envelope6 allOf/19. The detail-saving duty is now at step recording. No inventions: absence of a recorded detail is a named host duty the join cannot observe. Owner exactness at :1340–1344 is preserved and the settled branch is untouched. |
| V3 | **Fixed as specified.** The availability part raises R1. |
| V4 | **Fixed** in prose and tested. |
| Optional-Run decision / F3 | Preserved / still withdrawn. |

## Findings
- **R1 (medium; owner decision before selection).** `availability` is refused on interrupted outputs with no committed Run, by both the join and the unchanged schema6 empty form. But the owner scopes it to the **invocation** and the analysis step that made a selection, not to a committed Run:
  - the envelope description says "collection of THIS invocation … Present on the invocation that selected them";
  - workflows-and-surfaces.md:1302–1309 says it "rides the invocation that selected it", one entry per analysis step that made a selection;
  - :1324–1329 makes it a declared parity field of every analysis command.

  Review01 accepted the schema exclusion without examining this text; I'm correcting that here. The owner must choose:
  - **(a)** keep the ban and amend the availability prose; or
  - **(b)** admit recorded selections on no-Run outputs. That needs a schema6 successor, a join change and a projection rule.

  Either way, apply it together with the model successor, both prose overrides and the report06 rebase.
- **R2 (low).** The join excludes skipped steps by outcome, whereas report06's `recorded_failure_details` filters only by class and detail. They agree on owner-emitted ledgers. Make the exclusion explicit when rebasing report06.
- **R3 (low).** The errors form is single-valued per output kind, but choosing between failure and invocation (no Run), or run and invocation (Run), is still per-command dispatch. Bind it in report/inventory integration so goldens are single-valued.

## Test adequacy
**Strong:**
- Independent builders run against the same pinned owner model.
- Shape-valid negatives throughout.
- Presence/absence rules tested against the real schema.
- Verify covered as both required and optional.

**Limits:**
- Repair and verify results are synthetic admitted-shape inputs, not real apply/verify custody or Run replay.
- Availability is tested only for presence and refusal. The golden has zero steps, so there is no owner-valid selection ledger.
- Unrecorded details and RequestContext misuse remain host duties.

## Remaining duties
- Resolve R1.
- Select an accepted parent. Apply schema6, both prose overrides, model line 380 and the error/payload rule together.
- Rebase the report06 aggregate, the interrupted failure law (R2) and goldens. Bind the output kind per command (R3).
- Host implementation:
  - detail persistence at step recording;
  - finalized ledger admission;
  - RequestContext custody;
  - cancellation recording;
  - D9 delivery across renderers.
- Bind metadata/CLI/generated sources and inventory/registry/closure to the selected major.

## Not claimed
- Selection, promotion or product/source adoption.
- Acceptance of envelope5 or report06, or closure of the 11 report feature blockers.
- Live host signals, D9 delivery, browser, purity or M1 qualification.
- Real apply/verify custody or Run replay.
