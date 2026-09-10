I'll review the mixed-root absence counterexample against W callers, composition proof law, and the current workflow paragraph—read-only, no W edits.The counterexample is real: E1 is bound, but per-fingerprint `E1=null` because `rule_can_prove_absence` still requires every root false. I'll write the short review with the split wording and expected control.**Verdict: `AGREE_MINIMAL_HITSET_ABSENCE`.** The counterexample is real. Root’s split is the minimal fix. Do not put `executionDeficiencies` back on absence.

The `src` fingerprint is `INDETERMINATE` / `pivot-reevaluation-unavailable` even though `pivotsAvailable.E1` is `available`. `_compare_matched` treats **this fingerprint’s** `E1 is None` as unbound. `E1` is None because `axis_presence_knowledge` only writes False when `rule_can_prove_absence` is true, and that helper requires **every** selected root `"false"`. A README hit cannot stop you knowing the src non-hit is absent. README vanish still works because E4 is “emitted now” and E2/E3 copy along unchanged axes.

**Keep** `rule_can_prove_absence` as complete enumeration + all selected roots `"false"` (no findings for the whole rule; existing `boolean-or-true-does-not-prove-absence` stays).

**Add** closed hit-set knowledge: complete enumeration + every selected root determinate (`true` or `false`). A fingerprint **not** in that view’s exact emitted matched-hit set is absent. Unknown any selected root → cannot prove a non-hit absent. Known hits stay usable. Waivers stay separate. Extent checks unchanged. `axis_presence_knowledge` must key per-fingerprint False on the closed hit-set, not on all-false.

W11 was right to drop `executionDeficiencies` from `rule_can_prove_absence`. They belong only on sealed Run / comparison **verdict** (composition §5, `current_run_verdict`, `_apply_execution_to_comparison`). Complete file-false plus omitted required package can still make the **global** verdict indeterminate without retracting known per-rule file absence. Budget-exhausted still cannot prove absence.

**§3 wording to substitute:** a non-hit is absent when that rule’s enumeration is complete and every selected `emitWhen` root `p` is determinate (`true` or `false`); a true root on a different subject does not block that negative; all-false is the stronger “rule emitted no findings” claim; `executionDeficiencies` do not retract root-fixed fingerprint knowledge.

**This probe (`code-regression`):** README `POLICY-DELTA` vanished (E1 true, E4 false); src `POLICY-DELTA` appeared (E1 **false, not null**, E4 true); `INDETERMINATE` 0; `POLICY-DELTA` 2; verdict `pass`.

Reports: `review.md`, `review.json`. W not edited.
