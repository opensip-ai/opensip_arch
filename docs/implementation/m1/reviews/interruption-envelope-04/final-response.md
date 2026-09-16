# RESUMED INDEPENDENT DELTA REVIEW: interruption correction04

**Verdict: changes are required before selection. The owner decision to preserve optional Runs is conditionally accepted.** Correction04 fixes F-A properly and narrowly, and closes most of F-B and F-D. But it introduces a blocking defect that rejects every verify step (V1). It also still accepts two different error outputs for the same ledger (V2). Parent envelope5 is still the unchanged, unaccepted report05 bytes. Nothing here is a promotion, product claim or report-readiness claim. The review is in `review.json` and `review.md` in the review-04 directory.

## Custody
- **Subject:** the manifest SHA matches. The 48 files match exactly on the original and on my copy, before and after.
- **Pins:** all 37 match both their external sources and the copied bytes, before and after. They are the same pins as subject02.
- **Parent:** the pinned `envelope5.json` has the same bytes as report-projection subject-05's envelope5. The pin's source path still names subject-04.
- **Execution:** everything ran from my copy with `python -I -B`, an empty private pycache prefix and my own TMPDIR. There are no pyc files or `__pycache__` in either subject tree. I wrote only inside the review directory.
- **Root checker:** exits 0 and its output equals `root-result.json` (42 shape, 52 ledger, 72 model with 6 changed, 43 metadata, 2 prose spans).

## My own tests
`work/probes.py` has 49 rows and all behave as designed. I extracted the workflow model myself and applied `model-successor.json` myself, checking the hash, the line and that the replaced text is unique.

- **Optional Runs:**
  - The parent and patched models differ only in the interrupted termination's `runId`.
  - All 79 ledgers the patched model generates are valid, and the join admits all 130 of their correct outputs.
  - Erasing an optional Run is refused, both in the envelope alone and in record plus envelope.
  - Naming the earlier required Run instead of the later optional one is refused.
  - An ephemeral optional analysis correctly commits nothing.
- **Verify steps:** real `[verify, render]` ledgers are refused before settle, after settle and with no signal at all. The reverse mistake, a verify step carrying `kind=analysis`, is accepted.
- **Errors:**
  - A changed remedy, unrelated code, duplicate, reordering or omission is refused.
  - For the same ledger, both `[]` and the exact recorded detail are accepted.
  - If a real rejection's detail was never saved, the empty form is chosen silently.
  - A `kind=run` or `kind=invocation` output is accepted with or without the errors.
- **Payloads:** a failure with no committed Run is still accepted when it carries `findings`.
- **Phase, signal and correlation:** all mismatches are refused.
- **Pre-planning:** the pre-planning check is closed and typed. Reusing its context after an invocation exists can't be detected, which makes that a host custody duty.
- **After settle:** the settled class is kept and reclassification is refused.

## Previous findings
| | Status |
|---|---|
| **F-A** | **Resolved.** The owner text never limited "a Run committed by an earlier step" to required steps. Being optional controls gating, not whether a Run was committed. The change is confined to the cancellation branch and correctly presented as a successor. |
| **F-B** | Signal, cancelled-suffix, query-result and typed-input checks are **resolved**. The result-kind check is **wrong for verify** (V1). |
| **F-C** | **Mostly resolved**; V3 remains. |
| **F-D** | **Resolved as a design.** Keeping pre-planning out after an invocation exists is a custody duty. |
| F3 | Stays withdrawn. Query commands commit nothing. |
| F5 | Maintained. |

## Findings
- **V1 (high, blocking).** `ledger_join.py:53` requires verify steps to carry `kind=analysis`. The owner uses `kind=verify` (schema enum `[analysis, verify]`, and `workflows_model.v1.py:1913`). So repair-apply and repair-verify can never pass the mandatory check, and root's 72 scenarios include no verify step. Fix: require the result kind to match the step kind, and add verify ledgers to the checker.
- **V2 (medium, blocking): the error rule has to be single-valued.**
  - The owner text at :1340–1344 says errors equal the recorded detail exactly.
  - Report goldens need the same output across all renderers.
  - author06 (unreviewed, checked only for consistency) always sets errors equal to the recorded details.

  Neither proposal projects the whole ledger: both include optional-step failures and skip steps with no saved detail. **My recommendation:** for an interruption before settle, errors are exactly the recorded details in step order. The empty form is simply the case where there are none. On run and invocation outputs, errors are either always absent or always that same list; pick one. The host must save every composed detail when it records the step, because the join can't see a missing one. The rule must say whether optional-step details count. Apply it to the join, the prose and author06 together.
- **V3 (low-medium).** When no Run was committed, refuse `findings` (and `advisoryReport` as a precaution).
- **V4 (low).** An interrupted result now names an optional Run that the normal settled result never names. The prose should say so, with a golden.

**Real source obligations versus inherited checks:**
- **Must be implemented:** V1–V3.
- **Applied together:** the model successor and both prose overrides. Records produced under the old rule are refused by the new join.
- **Named host duties:**
  - Save error details when each step is recorded.
  - Custody that keeps pre-planning from being used after an invocation exists.
- **Root may rely on earlier checks for:** invocation, step and DAG admission, Run admission, record custody, and settled exit/output pairing. The only missing precondition I found is V1.

## Remaining integration work
- Fix V1–V3, then get the delta re-reviewed.
- Pick an accepted envelope parent. Apply envelope6, both prose overrides and the model successor together.
- Rebase the report aggregate and goldens, and align author06 with the single V2 rule.
- Bind metadata/CLI, generated sources, inventory/registry/closure and every renderer to the selected major.
- Implement the real host behaviour: RequestContext custody, signal observation, final ledger admission, cancellation recording and D9 delivery.
- The 11 report feature blockers, AUDIT-G10 and the milestones remain open.

I'm not claiming anything about live signals, host delivery, browser, source integration or milestone qualification.
