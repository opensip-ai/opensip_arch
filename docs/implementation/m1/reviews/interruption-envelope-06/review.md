# RESUMED INDEPENDENT DELTA REVIEW: interruption correction06 (m1-interruption-envelope-subject-06)

This continues review01/02/04/05; it is not a fresh session. Reviewer: actual Claude (claude-opus-5). No subagents, network, background tasks, commits, pushes or private-session inspection.

## Verdict
**Changes required (narrow).** The ownership decision, the schema6 delta and the composite join are accepted in substance. One blocking prose defect (**F1**) and one small binding fix (**N1**) remain. N2–N4 are advisory.

Parent envelope5 is still unaccepted. Report07 is unreviewed and still references correction05. No integration, product, M2/M3 or report-feature claim.

## Custody
- Manifest `d7c1b799…3060` verified. Closure is **51/51 exact** on the original and my copy, before and after.
- **38/38 pins** match sources and copies, before and after. The only new pin is `inputs/native_evidence_model.v2.py`.
- Delta from subject05:
  - Changed: `check.py`, `command-envelope.v6.schema.json`, `contract.md`, `input-pins.json`, `ledger_join.py`, `root-result.json`, `successor.json`.
  - Added: `availability_probes.py`, the native model pin, and an empty `root-tests.txt`.
  - **`passage-overrides.json` is byte-identical to subject05** (see F1).
- Root validation directory: `composite-check.stderr` preserves the failed run where the synthetic skipped step lacked `skipReason`, consistent with the stated history.
- Execution:
  - Runs only from my copy: reference env `-I -B`.
  - Private pycache; own TMPDIR.
  - Verified bytes compiled directly. No pyc or `__pycache__` in either subject tree afterwards.
- Writes: only this directory.

**Root checker:** exit 0, and its output equals `root-result.json`:
- 42 shape;
- 59 narrow join/preplanning;
- 43 metadata;
- 102 owner-model scenarios (9 changed Run choices, 12 wrong verify-kind refusals);
- **34 composite availability** cases, running the pinned `invocation_availability` / `release_absence_notices`.

## What changed, and the assessment
- **Ownership decision: correct.** Availability is the *invocation's* account, composed per selecting analysis step (workflows-and-surfaces.md:1302–1329, native `invocation_availability`). It does not require a Run.
  - Selected-with-no-absences (an empty step entry) differs from no selection (no entry), as the owner states at :1320–1321.
  - A selection retained from an attempt later rejected is lawful.
- **Schema6.** The forbidden list goes from 15 to 14 members; the difference is **exactly `availability`**. `findings` and `advisoryReport` remain forbidden. Shape cannot bind counts; only the join does.
- **Composite join**, in `validate_interruption_delivery` / `validate_preplanning_delivery`:
  - Context `{requestId, workflow, perStep}`, correlated to the record.
  - Builtin parity comes from inventory `capability-availability`. A profile with any analysis/verify step is treated as required.
  - Selections: strictly increasing, in range, analysis/verify, not skipped, ≤64 steps, ≤1024 unique typed tuples per step.
  - Presence: required or any selection ⇒ availability equals `native_projector(pairs)`; otherwise it is absent.
  - Before planning: a resolved parity command requires the empty account; otherwise it is absent. Never a non-empty account.
- **Skipped steps:** the termination must be exactly `{request-rejected, REQUEST.PRECONDITION_FAILED}` with no detail.

## Independent probes (`work/probes06.py`, 34 rows, all as designed)
I extracted the native projector (two functions and the remedy table) and the workflow model with the successor line myself.

- **Schema.**
  - S1: the delta is `{availability}`.
  - S2: the empty-errors form with an empty account is valid.
  - S3: a shape-valid wrong count is refused only by the join.
  - S4: `findings` and `advisoryReport` are still shape-refused.
- **Owner ledgers.**
  - A1: 20 model ledgers (default, fit, repair-apply with verify, and an optional+required analysis profile) at every cut, with every started analysis/verify selection retained. All are valid and accepted, and omitting the account is refused wherever one is present.
  - A2: a builtin with no parity field and no selection gives an absent account, and an invented empty account is refused. A retained selection there must be present.
- **Binding counterexamples.**
  - **B1: a selection on a cancelled step with `attempts: []` (never started) is admitted.**
  - B2: a rejected step with an attempt keeps its selection, coexisting with the exact error list. This is lawful.
  - **B3: a rejected step with `attempts: []` plus a selection is admitted.**
  - **B4: a completed authoritative analysis missing from `perStep` gives an admitted empty account.**
  - B5/B6: refused cases are a step out of range, 65 steps, 1025 notices, an extra tuple key, a non-string mode, a negative step and a render step. 1024 notices are accepted.
  - B7: a 4097-character root passes the join but is refused by the required envelope shape.
  - B8/B9: an extra context key and a changed notice code are refused.
- **Presence.**
  - C1: a profile whose analysis steps were all cancelled still requires the empty account.
  - C2: a settled success is bound too.
  - C3: a query builtin has no account, and an invented one is refused.
  - C4/C5: request and workflow mismatches are refused.
- **Errors and skips.**
  - E1: a no-Run failure with exact errors plus availability is valid and accepted.
  - E3: a real model skip then cancel passes the exact skip check.
  - E4: a skip carrying a detail is refused.
- **Preplanning.**
  - P1: **all 45 inventory commands** are deterministic, and the opposite choice is refused each time.
  - P2: an unknown command is refused.
  - P3: the empty form plus the empty account is valid.

## Findings
- **F1 (medium, blocking): the prose override contradicts the schema and join.** `passage-overrides.json` is unchanged, and its 1340–1349 after-text still says:

  > With no committed Run … no findings, advisoryReport or **Run-availability payload** is carried.

  Schema6 now admits availability there, and the join *requires* it for parity commands and retained selections. None of the new rules (the composite entry points, the presence rule, the preplanning empty account, profile parity, the exact skipped termination) are in any override; they live only in `contract.md` and successor duties.

  **Fix:**
  1. Revise the after-text so that only `findings`/`advisoryReport` are forbidden without a Run.
  2. State that the invocation's retained availability account (1302–1329) is carried through the composite delivery join, including the parity empty account and no invented preplanning selections.
  3. Add the skipped-termination rule and the entry-point duty.
  4. Re-freeze with the checker verifying the new text.
- **N1 (low-medium, required small fix).** A selection is admitted on a step that never started (B1, B3). The contract grounds retention in "a selection made by an attempt later cancelled or rejected". **Fix:** require at least one attempt on the selecting step, and add B1/B3 as shape-valid refusals.
- **N2 (low, advisory).** A completed analysis/verify step omitted from `perStep` is admitted (B4). If the native owner confirms that every completed analysis/verify step resolved a selection, refuse the omission. Otherwise state explicitly that this is host custody only.
- **N3 (low, advisory).** The profile parity duty (C1) is root-derived; the owner text binds parity to analysis-class *inventory* commands. Put the profile rule into the owner prose as part of F1.
- **N4 (low, advisory).** `check.py:101` still records `new-form-no-availability` with a `{}` placeholder. It passes only because `{}` is an invalid account. Rename it or replace it with a positive valid-account case.

## Previous findings
| | Disposition |
|---|---|
| R1 | **Resolved in schema and join**; prose not updated (F1). |
| R2 | **Resolved.** Exact skipped termination. Alignment with report07 is intended, but report07 was not reviewed. |
| R3 | Unchanged integration duty: output kind per command. |
| V1–V4, optional-Run decision, F3 withdrawal | Preserved (regression counts 102/9/12 unchanged). |

## Limits
- Selection contexts are synthetic admitted-state dictionaries, not RequestContext custody. Nothing shows the host retained every selection.
- No native selection execution derived the undeclared rows; they are synthetic.
- Repair/verify domain results are synthetic.
- Overall codec byte limits for large accounts are not assessed.

## Remaining duties
- Fix F1 and N1, then re-freeze and re-review this narrow delta. Get owner answers for N2 and N3.
- Select an accepted parent. Apply together: schema6, the revised prose overrides, model line 380, and the error/payload/availability joins with the composite entry points.
- Rebase report07 onto correction06: availability on interrupted outputs, exact skipped termination, output kind per command.
- Host: retain every selection immutably, supply the RequestContext account, and always use the composite entry points.
- Bind metadata/CLI/generated sources, inventory/registry/closure and codec limits to the selected major.

## Not claimed
- Selection, promotion or product/source adoption.
- Acceptance of envelope5 or report07, or completion of report features.
- Live signals, D9 delivery, browser, purity, or M1/M2/M3 qualification.
- Real selection retention or custody.
