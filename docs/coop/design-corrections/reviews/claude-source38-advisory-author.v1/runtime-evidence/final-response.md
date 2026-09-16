I corrected all three advisories in my own copy of source38 and reviewed root's A5 patch, which needs corrections. Both focused owner checks pass on the final bytes, all 7 controls that break a law on purpose caught the break, and the source38 bytes are unchanged. None of this is design acceptance, and all 54 recovery cases (F00–F53) are still not executed.

## ADV38-01: details and attribution on an analysis termination
The pure projection check is unchanged. I added a new §7 to `run-termination-contract.v1.md`: the rules the host finalizer applies when it builds the whole termination.
- **Faults, rejections and interruptions** are returned to their owners without reading a Run, so they never go through verdict derivation.
- **`executionId`** must belong to the step's last, completed attempt. That attempt's commit receipt must name the same Run, and the attempt must be bound to the Run's plan.
- **`authority`** is left out on a committed Run. An ephemeral attempt must carry `authority=ephemeral`, never a `runId`, and no detail.
- **Allowed details, first match wins; nothing else is allowed:**
  1. `EVALUATION.WORK_BUDGET_EXHAUSTED`, only when a work-budget record is retained and it is the primary reason.
  2. `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`, only when the first reason is provider-unavailable and the host observed the closure missing.
  3. The deficiency of the Coverage record named by `coverageId`, when it is one of the five registered native codes.
  - Query, doctor, host-invariant and every other code are refused.
- **Controls:** 37 cases over real closed Runs. Unrelated but schema-valid details and wrong-attempt or wrong-Run attribution are refused, while the pure projection check still reports `owner-validation-required` for the same inputs.

Three choices are new host behaviour, so please weigh them:
- the matching detail is required, not just permitted;
- `authority` is omitted on committed Runs;
- the work-budget detail applies only when the budget is the primary reason.

I made the detail required because it becomes the failure envelope's `errors` and decides the aggregate tie-break.

## ADV38-02: association naming an unmigrated carrier
The read-only map now sends format 1 and format 2 carriers explicitly to F46 `unknown-carrier-incompatible` (exit 4, `HOST.IO_FAILURE`). The order is now stated:
1. a binding mismatch;
2. then, if any format 3 object exists, the existing corruption and quarantine checks, then the below-`first_generation` check;
3. then F46 for a carrier with no format 3 objects.

Nothing is migrated or written. SQLite checks cover:
- both formats, at several generations;
- a binding mismatch taking precedence;
- a foreign witness not displacing F46;
- one format 3 object counting as corruption, not F46;
- the existing migrated below-`first_generation` case.

## ADV38-03
`commit-recovery-readonly.v3.md` now:
- records F00–F37 as the plan when the document was written, with F00–F53 current and all 54 cases not executed;
- scopes `MIGRATION.CORRUPT` to writer and maintenance opens, never read-only paths.

## A5 review: corrections required
The effective `allowJs` default and both flag formulas are right, and they agree with the model, the context agreement check and the context schemas. The patch has three problems:
- **A5-C1:** "apply inheritance before these defaults" is wrong. TypeScript 5.6.3 applies the jsconfig default per file, then merges `extends`. So a `jsconfig.json` extending a base with `allowJs:false` is effectively `true`, and so is a `tsconfig.json` extending a base named `jsconfig.json`. Over 52 compiler observations (root's 32 plus 20 new `extends` cases run offline with the verified compiler), root's wording is wrong on 8 and my amended wording on 0.
- **A5-C2:** the retained native case `ts-tsconfig-without-allowjs-excludes-js` still expects the old default, and root's corrected model now fails it.
- **A5-C3 (editorial):** the `ts-tsconfig` mode row leaves out jsconfig entries that set `allowJs:false`.

The proposed fix is `a5-review/proposed-amendment.r2.diff`; the amended cases agree with root's model. Root's patch was not copied into my tree.

## Controls and custody
| Check | Baseline | Edited |
|---|---|---|
| Semantic replay | 30/30 | 31/31 |
| Carrier validator | 362/0 | 384/0 |

Each deliberate break failed exactly the checks it should:
- restoring the old model;
- disabling the detail check, the receipt check, or the `executionId` check;
- sending fault terminations through derivation;
- restoring the old dispatch JSON or the old prose.

At the start, all 12904 manifest files matched and the working copies had no hardlinks. At the end, the touched and dependency files are unchanged in source38, and the review and A5 inputs are unchanged. I ran only the two focused validators; I did not run the planning checker or the six global groups.

## For root to merge and rebind
- **Shared sentence:** the last paragraph of `workflows-and-surfaces.md` §9 changed.
- **Pins to rebind:**
  - five source-pin ledgers pin all 10 touched files;
  - the implementation coverage, normative-inputs and planning-sources files pin 6 of them;
  - planning sections `security-and-lifecycle:12` and `workflows-and-surfaces:10` changed text, and `workflows-and-surfaces:11`–`13` shifted by 4 lines.

## Limits
- Host inputs to §7 are trusted, not authenticated.
- Ephemeral reasons are not derived by this contract.
- The second read-only stability snapshot is covered by the route law check, not simulated.
- A carrier with no journal table at all plus an association still has no read-only standing; that is outside ADV38-02.
- I found no owner that routes compiler diagnostic 5052 into admission.

## Failed attempt
The first A5 amendment run exited 1 because re-serializing the native cases JSON would have rewritten unrelated bytes. Its output is kept; the second run replaces only the stale case and keeps every other byte.

Everything is in `/tmp/opensip-design-corrections/claude-source38-advisory-author.v1`; the full before/after hashes are in `review.json`, and all background processes have finished.
- `review.md`
- `review.json`
- `proposed-edits.diff`
- `a5-review/assessment.md`
- `a5-review/proposed-amendment.r2.diff`
