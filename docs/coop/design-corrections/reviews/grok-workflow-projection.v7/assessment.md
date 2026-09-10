I’ll close the remaining correctness gaps in the owned workflow files: admitted-run verdict ownership, required-evidence coverage, full deficiency records, real pivot-run comparison, and the replay loop.I have the axis substitutions and fixture constraints. Next I’ll patch verdict ownership, full deficiency records, pivot-run binding, and the remaining comparison joins.v7 closes the remaining comparison/verdict/pivot gaps in the owned workflow files. Bounded checker: **252/252 passed**, including **v6 ≥ 224** controls. Report: stdout or `grok-workflow-projection.v7/` only (v6/history not overwritten). Not full profile acceptance.

## Fixes

| # | Change |
|---|---|
| 1 | Admitted-run verdict: **fail** from policy-gating live unwaived findings; **indeterminate** from admitted `ruleResult.outcome` plus execution/budget. Deficiencies on a determinate-false branch no longer force unknown. `and`/`or` `atom_override` is supported; mixed `and(none, exists)` stays consistent with proof. |
| 2 | `requiredCoverage` comes from outcome + required-evidence causes. Complete inventory + required imported unknown (`wrapper-partial`) → coverage `unknown` → comparison **indeterminate** with no matched fail. |
| 3 | Comparison copies the **full** evaluation-deficiency record (`inputRefs`, `predicateId`, `nativeCause`, …). |
| 4 | `compare_admitted_v3(..., pivot_runs=)` binds section-3 substitutions. Same-snapshot `gate=True` vs `gate=False` binds **E1=available**. Supplying the current Run as E1 (wrong policy) **refuses**. Incomplete pivot population is not treated as false absence. Equalities only follow valid substitutions (no E4 copy onto an earlier axis when a later one changed). |
| 5 | `current_detectors` must match admitted emission; `compatibleWith` without signed provenance is refused. Detectors group by `contributionId`; conflicting semantics refuse. PivotClosure successor includes **`provider`**; selected provider closures are pinned, not dropped. |
| 6 | Baseline/comparison **refuse** if ScopeDocumentV1 is not selected. `plan.scopeDigest` is not used as a substitute. |
| 7 | `evidenceAvailability.relations` is derived from admitted facts/views. |
| 8 | SARIF URIs use `quote(..., safe='/')` so `foo:bar` cannot become a scheme. Colon/space controls added. The 12 registered detail codes remain. |
| 9 | Replay projection loop covers all **29** check-replay positives (file/runtime/history/test/symbol). The 6 remints stay owner-refuse, not projected. |
| 10 | Host adapter treats closure platform `any` as portable (rewritten to the host platform). That is compatibility law, not a fixture defect. |

## Remaining gaps (real, not deferred pivots)

- No in-tree OASIS SARIF document; adapter subset is not full-schema qualification.
- `compatibleWith` still needs authenticated detector-manifest provenance; arbitrary maps stay refused.
- Execution-input-manifest completion remains a separate root blocker.
- Check-replay has no separate waiver **positive** (only reminted invented-waiver refuse).
- E2/E3 bound positives are not separately graphed; the genuine bound case is same-snapshot **E1** on a policy-gate change, with E2/E3 derived only when those substitutions are actually equal.

Changed-context pivots are implemented and tested (bound E1 available + wrong-context refuse), not left as “permanently unavailable.”
