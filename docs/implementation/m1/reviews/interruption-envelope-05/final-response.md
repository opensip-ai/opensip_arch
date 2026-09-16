# RESUMED INDEPENDENT DELTA REVIEW: interruption05

**Verdict: accept-conditional for this delta only; not selection and not promotion.** V1–V4 are fixed and adequately tested, and I found no new defect in the join. One owner decision is still open before selection (R1, availability). The optional-Run owner decision is kept, and F3 stays withdrawn. Parent envelope5 is still unchanged and unaccepted; its bytes are also unchanged in report06. The review is in `review.json` and `review.md` in the review-05 directory.

## Custody
- **Subject:** the manifest SHA matches. The 48 files match exactly on the original and on my copy, before and after.
- **Pins:** all 37 match their external sources and the copies, before and after. They are the same pins as subject04.
- **Schema and parent:** schema6 is byte-identical to subjects 01–04, and envelope5 matches report-projection subject-06.
- **Delta from subject04:** 7 files changed (contract, the join, both probe modules, the prose overrides, root-result and successor), none added or removed.
- **Execution:** everything ran from my copy with `python -I -B`, a fresh private pycache and my own TMPDIR, compiling verified bytes. There are no pyc files in either subject tree. I wrote only inside the review directory.
- **Root checker:** exits 0 and its output equals `root-result.json`. That is 42 shape, 59 join, 43 metadata and 102 owner-model scenarios (9 changed), plus 12 wrong-verify-kind refusals.

## My own tests
`work/probes05.py` has 47 rows and all behave as designed. I built my own ledgers, ran them through my own extraction of the pinned model, and applied the one-line model patch myself.

- **V1 (result kinds):**
  - The one result type defined by reference, test-execution, has kind `test-execution`, so exact matching is safe for it.
  - Required and optional repair-preview → repair-apply → verify → render ledgers are all valid and accepted at every cut.
  - Refused with both shapes valid: verify carrying `analysis`, analysis carrying `verify`, and apply carrying a preview result.
- **Model:** my repair ledgers give exactly 3 changed cases (optional verify × 3 signals), with step results and exits identical. That fits root's 9. Settled optional-verify ends in success/0, while interrupting before render names the verify Run with exit 130.
- **V2 (errors):**
  - An exact non-empty list is accepted on failure, run and invocation outputs. Omitting it, sending `[]`, duplicating it or changing a remedy is refused.
  - With an empty list, failure needs `errors:[]`, while run and invocation must omit `errors`. Using `[]` there is refused by both the schema and the join.
  - Across four different ledgers, exactly one errors form is lawful for each output kind.
  - This matches the old owner's exactness rule and invents nothing.
- **V3 (payloads):**
  - On outputs with no committed Run, `findings` and `availability` are refused on failure, and `availability` is refused on invocation.
  - A run output carrying `availability` is accepted.
- **Checks that still hold:** preplanning works, after-settle keeps its class, and erasing an optional verify Run is refused.

## Findings
- **R1 (medium; owner decision before selection).** `availability` is refused on outputs with no committed Run, by both the join and the unchanged schema6 empty form. But the owner ties it to the invocation, not to a Run:
  - The envelope description says "collection of THIS invocation".
  - workflows-and-surfaces.md:1302–1309 says it "rides the invocation that selected it", one entry per analysis step that made a selection.
  - :1324–1329 makes it a declared parity field of every analysis command.

  In review01 I accepted the schema's exclusion without checking this text; I'm correcting that now. The owner has two options:
  - **(a)** keep the ban and amend the availability prose; or
  - **(b)** allow recorded selections, which needs a schema6 successor plus matching join and projection changes.

  Either way, it has to land together with the model successor, both prose overrides and the report rebase.
- **R2 (low).** The join excludes skipped steps by their outcome, but report06 filters only by class and detail. They agree on ledgers the owner model produces; make the exclusion explicit when rebasing report06.
- **R3 (low).** The errors form is now single-valued for each output kind, but which output kind a command uses is still per-command dispatch. Bind it in the report/inventory integration so goldens have one answer.

## Remaining duties
- Resolve R1.
- Select an accepted parent, then apply schema6, both prose overrides, model line 380 and the error/payload rule together.
- Rebase report06's aggregate, error law (R2) and goldens, and bind the output kind per command (R3).
- Host work: save composed details when each step is recorded, admit the final ledger, keep RequestContext custody, record cancellation, and deliver D9 across renderers.
- Bind metadata/CLI, generated sources and inventory/registry/closure to the selected major.

The repair and verify results in both root's tests and mine are synthetic, schema-valid inputs, not real apply/verify custody or Run replay. I'm not claiming live signals, D9 delivery, browser, purity or M1 qualification, and I'm not claiming any of the 11 report blockers are closed.
