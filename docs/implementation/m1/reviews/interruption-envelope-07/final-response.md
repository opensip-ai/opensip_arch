# RESUMED INDEPENDENT DELTA REVIEW: interruption correction07

**Verdict: accept, for this narrow delta only.** Review06's F1 and N1 are fixed, and the N2, N3 and N4 dispositions are accepted. There are no new findings, just three low observations. Acceptance covers only the change from correction06 to correction07, as design/reference standing:
- the revised failure paragraph (1340–1349) and the new availability section (1302–1338);
- the attempt requirement in the join;
- the corrected rejected-attempt fixture and the two new refusals;
- the checker's prose assertions;
- the N4 rename.

It does not cover selection or promotion, envelope5, report07 or report features, generator or product work, M1 qualification, live signals or D9 delivery, host custody, or envelope capacity (L02). The review is in `review.json` and `review.md` in the review-07 directory.

## Custody
- **Subject:** the manifest SHA matches. The 51 files match exactly on the original and on my copy, before and after.
- **Pins:** all 38 match their sources and the copies, before and after, and are unchanged from subject06.
- **Delta:** 7 files changed, none added or removed. Schema6 is byte-identical to correction06.
- **Execution:** everything ran from my copy with `-I -B`, a private pycache and my own TMPDIR, compiling verified bytes. There are no pyc files in either subject tree. I wrote only inside the review directory.
- **Root checker:** exits 0 and its output equals `root-result.json` (42 / 59 / 43 / 102 with 9 changed and 12 wrong-kind / 36 availability / 3 prose spans).
- **Preserved evidence:** the line-wrap stderr and the capacity audit both match what you described.

## My own tests
**`work/probes07.py`, 22 rows, all as designed:**
- **Prose (F1):**
  - All three before-spans match the pinned owner lines exactly, and the spans don't overlap.
  - After applying all three overrides to the pinned source, no availability ban remains anywhere.
  - Eleven required duties are present in the resulting text, including both entry points, the attempt requirement, the exact skip termination, custody-only completeness, the profile addition and the preplanning empty account.
- **Attempt binding (N1):**
  - Refused: an unstarted cancelled step, a rejected step with no attempts, and a skipped step.
  - Accepted: a step cancelled mid-attempt, and rejected, operationally failed and completed attempts.
  - An unstarted step still allows the empty parity account, and "selected but empty" stays distinct from "no selection".
- **N2:** leaving a completed analysis out of the context is still admitted, which matches the published custody-only duty.
- **N4:** the renamed case is present, and a valid empty account is accepted on the empty-errors form.
- **Capacity sanity check (L02):** a single step with 995 notices and 4096-character roots passes the join and the shape check, but the pinned canonical codec refuses it (BYTE_LIMIT). So capacity really is outside this join, as you said.

**Regression:** I reran a byte-identical copy of my review06 probes. Of the 34 rows, exactly B1 and B3 flip to refused, as the N1 fix requires. The other 32 are unchanged, including the 20 owner ledgers, the presence rule, all 45 preplanning commands, bounds, correlation, errors and skips.

## Observations (low, non-blocking)
- **O1:** the kept text says leaving out a required account is a "required-delivery operational fault". It doesn't say whether an interrupted invocation in that situation is delivered as 130 or becomes 4. This predates the delta; settle it together with L02.
- **O2:** the subject mentions L02 only as a generic codec sentence (`contract.md:43`), and the successor duties don't name it. At selection, record it explicitly, including:
  - no silent truncation;
  - precedence between the existing `OUTPUT.SERIALIZATION_FAILED` overflow rule and interrupted/130.

  It was correctly kept out of this delta.
- **O3:** the checker only checks that phrases appear in the after-text. Pinning the after-text hashes at re-freeze would catch silent prose drift.

**Limits:** selection contexts, undeclared rows and repair/verify results are synthetic. The mid-attempt-cancelled shape is one the owner model never produces. Capacity and full native, parameter and Run admission are not proven.

**Remaining duties:**
- Apply schema6, all three prose overrides, model line 380 and all the joins together under an accepted parent.
- Qualify L02 and get the owner's precedence decision.
- Rebase report07 onto correction07, and bind each command's output kind.
- The host must keep every selection immutably and always call the combined entry points.
- Rebase metadata, CLI and source onto the selected major.
