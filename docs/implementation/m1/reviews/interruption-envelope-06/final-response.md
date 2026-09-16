# RESUMED INDEPENDENT DELTA REVIEW: interruption correction06

**Verdict: changes required, but narrow.** The ownership decision is right: availability belongs to the invocation, not to a committed Run. The schema6 change and the new combined delivery check are sound in substance. One blocking prose defect (F1) and one small fix (N1) remain; N2–N4 are advisory. Parent envelope5 is still unaccepted. Report07 is unreviewed and still references correction05. Nothing here claims integration, product, M2/M3 or report-feature completion. The review is in `review.json` and `review.md` in the review-06 directory.

## Custody
- **Subject:** the manifest SHA matches. The 51 files match exactly on the original and on my copy, before and after.
- **Pins:** all 38 match their sources and the copies, before and after. The only new pin is the native evidence model.
- **Execution:** everything ran from my copy with `-I -B`, a private pycache and my own TMPDIR, compiling verified bytes. There are no pyc files in either subject tree. I wrote only inside the review directory.
- **Root checker:** exits 0 and its output equals `root-result.json`. That is 42 shape, 59 narrow join, 43 metadata, 102 owner-model scenarios (9 changed Run choices, 12 wrong verify-kind cases) and 34 availability cases that run the pinned native functions.
- **Failed-probe evidence:** the preserved `composite-check.stderr` shows the missing-`skipReason` failure, as you described.

## My own tests
`work/probes06.py` has 34 rows and all behave as designed. I extracted the native projector and the workflow model myself.

- **Schema:** the only change is that `availability` left the forbidden list (15 → 14 members). `findings` and `advisoryReport` are still refused. The schema can't check the counts; only the new join does.
- **Owner-model ledgers:** 20 ledgers (default, fit, repair-apply with verify, and a profile with optional analysis) at every cancel point, with every started step's selection kept. All are accepted, and leaving out the availability account is always refused. A command with no parity field and no selection correctly carries no account; an invented empty account is refused.
- **Before planning:** all 45 inventory commands behave deterministically in both directions, and an unknown command is refused.
- **Other checks:**
  - Errors and availability coexist on a no-Run failure.
  - A real skip from the model passes, and a skip carrying a detail is refused.
  - Wrong counts, order, notice code, bounds (1025 notices / 65 steps), tuple types, extra keys and request/workflow mismatches are refused.
  - A 4097-character path passes the join but is refused by the envelope shape check, which is required separately.

## Findings
- **F1 (medium, blocking):** `passage-overrides.json` is byte-identical to subject05. Its failure paragraph still says that without a committed Run "no findings, advisoryReport or Run-availability payload is carried". That contradicts schema6 and the new join, which requires availability for parity commands and kept selections. None of the new rules are in any prose override. They exist only in `contract.md` and the successor duties: the combined entry points, the presence rule, the empty account before planning, the profile rule and the exact skip termination.
  - **Fix:** forbid only `findings`/`advisoryReport` without a Run; state the invocation-scoped availability rule and those new duties; then re-freeze with the checker verifying the new text.
- **N1 (low-medium, small fix):** a non-empty selection is accepted on a step that never started. That covers a cancelled step with no attempts, which is how the model records "signal arrived before the step began", and a rejected step with no attempts. The contract itself says kept selections come from an attempt that was later cancelled or rejected.
  - **Fix:** require at least one attempt on the selecting step, and add both cases as refusals.
- **N2 (low, advisory):** a completed analysis left out of the selection context is accepted with an empty account. Either the native owner confirms every completed analysis made a selection and the join refuses the omission, or this is declared a host custody duty only.
- **N3 (low, advisory):** requiring an empty account for any profile with an analysis or verify step is root's own rule. The owner text ties the parity field only to analysis-class inventory commands, so the rule belongs in the owner prose (as part of F1).
- **N4 (low, advisory):** `check.py:101` still records `new-form-no-availability` using a `{}` placeholder. It passes only because `{}` is not a valid account, so it now gives a false signal. Rename it or make it a positive case.

**Earlier findings:**
- R1 is resolved in the schema and join, but not yet in the prose (F1).
- R2 (skipped steps) is resolved.
- R3, which output kind each command uses, is still an integration duty.
- V1–V4, the optional-Run decision and the F3 withdrawal are all preserved.

**Limits:** the selection contexts are synthetic dictionaries, not real host custody. The undeclared rows were not produced by running native selection. Repair and verify results are synthetic. I didn't assess codec size limits for large availability accounts.

**Remaining duties:**
- Fix F1 and N1, re-freeze, and get this narrow delta re-reviewed. Get owner answers on N2 and N3.
- Apply schema6, the revised prose, model line 380, and the error, payload and availability joins together.
- Rebase report07 onto correction06.
- The host must keep every selection and always call the combined entry points.
- Rebase metadata, CLI and generated sources onto the selected major.
