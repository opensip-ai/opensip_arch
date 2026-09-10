# Mixed-root absence — peer coauthor review

**Standing.** Actual Grok, read-only. Isolated `evaluator-successor.v1`. W not edited. Not independent acceptance.

**Verdict.** `AGREE_MINIMAL_HITSET_ABSENCE`. Root’s counterexample is real. The precise split is the minimal fix. Do not restore `executionDeficiencies` as an absence predicate.

## Counterexample (as run)

`probe-mixed-root-absence.v1.py` / `mixed-root-absence.v1.json`. Same snapshot, detector, ScopeDocument `**`. Baseline glob `README.md`; current glob `src/**`. E1 = fully admitted prior-policy Run. Three file subjects; every emitWhen root `p` is determinate (`true`|`false`) on both views. One True / two False each side.

README vanish is `POLICY-DELTA` because E4 membership is “emitted now” and E2/E3 copy along unchanged axes (`_presence_from_equalities`). The new `src` fingerprint is `INDETERMINATE` / `pivot-reevaluation-unavailable` with `pivotsAvailable.E1=available` because `_compare_matched` treats **this fingerprint’s** `E1 is None` as unbound (`workflow_projection_model.v3.py` ~996–1002). `E1` is None because `axis_presence_knowledge` only stores False when `rule_can_prove_absence` is true, and that helper returns False unless **every** selected root is `"false"` (~1794–1823). A known hit on README cannot prevent knowing the src non-hit is absent. `baselineCanProveAbsentNonhit: false` is that helper, not missing work.

## Callers / composition

- Presence True = matched occurrence (incl. waived). False on E0–E3 = `prove_absence[rule]` then extent check. Else omit (None).
- Composition (`evaluator_composition_model.v3.py`): per-subject strong Kleene at root `p`; findings only from `"true"`; global verdict `fail` if any gating fail, else `indeterminate` if `executionDeficiencies` **or** any gating rule indeterminate, else `pass`. Required execution cells are independent of rule findings (`evaluator-composition-contract.v3.md` §5; `current_run_verdict`).
- Complete file-false + omitted required package: file roots can be fully known; sealed Run / comparison verdict still indeterminate. That is global completeness, not per-rule fingerprint authority.

## `executionDeficiencies`

W11 already dropped them from `rule_can_prove_absence`. Keep that. They belong on `_apply_execution_to_comparison` / sealed Run verdict only. Do not make them an unconditional absence block. Budget-exhausted still cannot prove absence (subjects not evaluated). `ruleResults.outcome` is not root knowledge (W11); the mixed-root defect is the all-false test, not outcome.

## Minimal fix

Keep `rule_can_prove_absence` = complete enum + every selected root `"false"` (**zero findings for the whole rule**; existing `boolean-or-true-does-not-prove-absence` stays).

Add closed hit-set knowledge: complete enum + every selected root determinate (`true` **or** `false`). Then a fingerprint **not** in that view’s exact emitted matched-hit set is absent (`False`). Unknown any selected root → cannot prove a non-hit absent. Known hits always usable. Waivers stay `waivedB`/`waivedC`. Extent (`path_absence_claim_allowed`) unchanged.

`axis_presence_knowledge` must key per-fingerprint False on **determinate roots**, not on all-false.

## Normative wording (workflows-and-surfaces.md §3 Evidence for presence)

Replace the sentence that requires a determinate **false** root for every selected subject with:

A known matched finding establishes presence even when waived; waiver status is a separate axis. For one rule at one admitted view, a fingerprint that is not in that view’s exact emitted matched-hit set is absent when that rule’s subject enumeration is complete and every selected subject has a determinate `emitWhen` proof root `p` (`true` or `false`). A true root on a different subject does not block that negative. Unknown roots, incomplete enumeration, disabled evaluation, and exhausted budgets do not prove a non-hit absent. All selected roots `false` asserts the rule emitted no findings; it is not required to prove one fingerprint absent. An advisory `pass` alone does not establish absence. A false root may retain unknown child witnesses under the published three-valued composition law; those witnesses do not turn a determinate false root into unknown. Known hits remain usable when other roots are unknown. `executionDeficiencies` and the sealed Run verdict speak to global analysis completeness; they do not retract per-rule fingerprint presence or absence already fixed by those roots.

Same split in `workflow-projection-contract.v3.md` §12 (today: “every root `false`”).

## Minimum control (this probe, `code-regression`)

| check | expect |
|---|---|
| three roots each side | all `true` or `false` |
| `rule_can_prove_absence(baseline)` / `(current)` | `false` (a true root exists) |
| determinate-roots / closed hit-set on both | `true` |
| README entry | `POLICY-DELTA` vanished; E1 `true`; E4 `false` |
| src entry | `POLICY-DELTA` appeared; E1 **`false` not null**; E4 `true`; not `INDETERMINATE` |
| `counts.INDETERMINATE` | `0` |
| `counts.POLICY-DELTA` | `2` |
| `verdict` | `pass` (profile does not gate policy-axis newly-live) |
| `currentExecutionDeficiencies` | `[]` |

Do not treat catalog/W12 listing work as part of this fix. Root applies W after W12 hands back.
