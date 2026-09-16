# RESUMED INDEPENDENT DELTA REVIEW: interruption correction04 (m1-interruption-envelope-subject-04)

This continues review01/review02; it is not a fresh session. Reviewer: actual Claude (claude-opus-5). No subagents, commits, pushes, background jobs or private-session inspection.

## Verdict
**Changes required before selection. The optional-Run owner decision is conditionally accepted.**

- **F-A is resolved** legitimately and narrowly.
- **F-B's listed prerequisites** are now executed checks.
- **F-D is resolved** as a host custody design.
- Correction04 **introduces a blocking defect (V1)**: the join refuses every owner-valid ledger containing a verify step.
- **The error policy is still not one rule (V2).**
- Parent envelope5 remains the unchanged, unaccepted report05 bytes. No promotion, product, report-readiness or milestone claim.

## Custody
- Manifest `0cfda57a…875a` verified. Closure is **48/48 exact** on the original and my copy, before and after.
- **37/37 pins** match both external sources and copied bytes, before and after. The pin set is identical to subject02.
- Pinned `envelope5.json` (`45de2b0a…`) equals report-projection-**subject-05**'s envelope5. The pin's source path still names subject-04; the bytes are identical.
- Delta from subject02:
  - v6 schema: byte-identical.
  - Changed: `check.py`, `contract.md`, `join_probes.py`, `ledger_join.py`, `passage-overrides.json`, `root-result.json`, `successor.json`.
  - Added: `model-successor.json`, `owner_model_probes.py`.
- Execution:
  - Runs only from the copy: reference env `python -I -B`, jsonschema 4.25.1.
  - `PYTHONPYCACHEPREFIX` pointed at an empty private directory; own TMPDIR.
  - No pyc or `__pycache__` in the original or the copy afterwards.
- Writes: only this directory.
- Consulted read-only for consistency, **not as authority**: author06 / report subject-06 `contract.md` RPR5-3 and `report_model.recorded_failure_details` / `failure_envelope`.

**Root checker:** exit 0, and its output equals `root-result.json`: 42 shape, 52 ledger/preplanning/payload, 72 owner-model scenarios (6 changed), 43 metadata cases, 2 prose spans.

## Independent evidence (`work/probes.py`, 49 rows, all as designed)
I extracted the model myself (AST, from pinned bytes) and applied `model-successor.json` myself, checking sha, line and uniqueness. Owner-valid values come from pinned fixtures.

- **Optional Runs.**
  - A1: parent vs successor differ only in the termination `runId`. Step results are equal, exits are 130/130, and the record is valid.
  - A8: 79 successor ledgers over 7 workflows (including optional-first, later-optional and optional+query), all record-valid. All 130 canonical carriers are admitted.
  - A3/A4: optional-Run erasure is refused, both envelope-only and in record+envelope.
  - A5: substituting the earlier Run for a later optional one is refused.
  - A7: an ephemeral optional analysis does not commit.
- **Verify (V1).**
  - B1b: `kind=verify` + `verification` is a valid authoritative AnalysisResult.
  - B2: owner-valid `[verify, render]` ledgers, before-settle, after-settle and with no signal, are **all refused** (`J-INTERRUPTION-RESULT-KIND`).
  - B3: a verify step carrying `kind=analysis` without `verification` is **admitted**.
- **Errors (V2).**
  - C1/C2: a recorded optional-step CONFIG.INVALID admits **both** `[]` and the exact detail.
  - C3–C8: changed remedy, unrelated code, duplicate, reorder and omission are refused.
  - C9: a real rejection without a persisted detail silently gives the empty form, and the composed detail is refused.
  - C10: a committed `kind=run` admits errors both with and without the detail.
  - C11: `kind=invocation` with errors is valid and admitted.
- **Payload (V3).** C12: a no-commit `kind=failure` with real errors plus Run `findings` is valid and admitted.
- **Phase, signal and correlation.**
  - D1/D2: a cancelled step with a result, or a signal mismatch, is refused.
  - D4/D5: dropped project or correlation fields are refused.
  - D6: exit 4 is refused.
  - D3: a rejected step carrying a result is admitted, which is left to StepResult admission.
- **Preplanning.**
  - E1–E9: the context is closed and typed, covering signal, stage, requestId, correlation, non-empty errors and invocation carrier.
  - E10: a context reused after invocation admission is indistinguishable, so this is pure custody.
  - E11: no empty-steps record exists.
- **After-settle.**
  - F1–F3: the settled class is kept, reclassification is refused, and an optional step cancelled after required settlement stays after-settle success.
  - F4: exit on the settled branch is left to envelope admission.

## Previous findings
| | Disposition |
|---|---|
| **F-A** | **Resolved** by an explicit successor, conditionally accepted. Owner prose :226 never restricted "a Run committed by an earlier step" to required steps. Optionality governs gating, not commit identity. The change is scoped to the cancellation branch and correctly labelled a successor. See V4. |
| **F-B** | Signal, prefix, query-with-AnalysisResult and typed-input checks are **resolved**. The result-kind check is **wrong for verify**, so V1 was introduced. |
| **F-C** | **Mostly resolved.** Invented, changed and duplicate details, cancelled query carriers and wrong invocations are refused. V3 remains. |
| **F-D** | **Resolved as design.** A private preplanning observation; no dummy record. Exclusion after admission is a custody duty. |
| F3 (review01) | Stays withdrawn. Query builtins commit nothing. |
| F5 | Maintained. subject03 is historical and was never accepted. |

## Findings
- **V1 (high, blocking).** `ledger_join.py:53` maps verify steps to `kind == "analysis"`, but the owner AnalysisResult uses `kind=verify`: schema enum `[analysis, verify]`, and `workflows_model.v1.py:1913`.
  - Every repair-apply and repair-verify ledger fails the mandatory join, including settled ones, and the wrong kind is admitted (B3).
  - Root's 72 scenarios contain no verify step.
  - Fix: bind `result.kind` to `spec.kind` for analysis and verify, and add verify ledgers (before-settle, after-settle, committed verify Run carrier) to the checker.
- **V2 (medium, blocking): one coherent error rule.** For one ledger, root admits both `[]` and the exact recorded details, on failure, run and invocation carriers. Author06 is deterministic: errors always equal `recorded_failure_details`. Checked against the owners:
  - Owner :1340–1344 frames errors as *exactly* the recorded detail, "so the two surfaces never disagree".
  - Renderer and golden parity needs a single value.
  - Neither proposal is an exhaustive ledger projection: both include optional-step failures and exclude detail-less skipped terminations.

  **Recommended rule:** for before-settle interruption, `errors := recorded_failure_details(stepResults)`, in step order. The envelope6 empty form is exactly the empty-list case. On run/invocation carriers, `errors` is either absent or that same list; pick one. The host persists every composed route detail into `StepTermination.domainDetail` **at step recording**, as a named ledger-admission duty, because the join cannot observe its absence (C9). State whether optional-step details are included. Align `ledger_join`, the prose override and author06 together.
- **V3 (low-medium).** With no committed Run, refuse `findings` (and `advisoryReport` defensively). `result_fields` currently omits them. Keep `availability` only if the owner confirms it is invocation-scoped.
- **V4 (low).** The successor makes an interrupted aggregate name an optional Run that the settled required-only aggregate never names (A6). State this in the cancellation override and add a golden.

## Source obligations vs admitted-input duties
**Actual source obligations:**
- V1–V3.
- Apply the model successor at line 380 with both prose overrides and the envelope/report selection. A2 shows records produced under the parent law are refused.
- Persist route details at step recording.
- RequestContext custody that forbids a preplanning observation after admission.

**Legitimately owned by earlier admission (root precondition accepted):**
- invocation:3 / StepResult shape (D3), DAG, attempts/retry.
- Run admission and receipt, record custody.
- Settled D9 aggregation and exit/carrier pairing (F4).

**Genuinely missing precondition:** none beyond V1. The result-kind binding exists but is wrong.

## Remaining integration obligations
- Fix V1 and V2 (and V3), then re-review the delta.
- Select an accepted envelope parent, then apply envelope6, both prose overrides and the model successor together.
- Rebase the report aggregate and goldens onto optional-Run preservation, and reconcile author06's `J-ENV-INTERRUPTION-DETAIL` with the single V2 rule.
- Bind metadata/CLI/generated sources, inventory/source-map/registry/closure and all renderer branches to the selected major.
- Implement the host side: RequestContext custody, signal observation before and after planning, finalized ledger admission, cancellation recording, and D9 delivery across renderers (DR-G17/DR-G20).
- The 11 report feature blockers, AUDIT-G10 and the milestones remain open.

## Not claimed
- Selection, promotion or product adoption.
- Acceptance of envelope5, report05 or author06.
- Live signal handling, host delivery, browser, codec, runtime or source integration.
- Custody or confinement.
- Milestone qualification.
