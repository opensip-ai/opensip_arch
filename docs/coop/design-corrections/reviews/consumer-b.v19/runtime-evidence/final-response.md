`REFERENCE_INTERPRETER_AVAILABLE` — the interpreter ran, so this turn is execution, not authorship. Final state: **46 stages, 0 failed**, verdict **ACCEPT-RECONSTRUCTABLE**.

## Confinement and custody (before any copied code ran)

`census_v19.py` (fresh) found every active module still pointing at generation 18 → `rebind_v19.py` copied `lib` to `lib.before-image.v18`, rewrote **path form only** (trailing separator required), quarantined 7 generation-pinned tools, and restored labels instead of rewriting them. Re-run after every stage: **0 foreign write/root rows**, and no earlier generation was modified this session (measured by mtime).

Two new self-reference findings: **V19-D1** — four historical `HELPER CORRECTION` sentences had been relabelled by every rebind since v15 (true generations v14/v15/v16/v15) and `deliver.py`'s ancestry had **lost generation 17**; repaired from the retained before-images by `label_history_v19.py`, which now reports `NO HISTORICAL LABEL DRIFT`. **V19-D2** — my own new rebind rewrote its own docstring; split and self-excluded.

Kit: 102/102 rows verified (path, sha256, byte length), manifest and declared parent PASS, re-verified unchanged after reconstruction. The delta was **measured**, not taken from the instruction: 93 unchanged, **8 changed + 1 added** — the added file is `foundation/glob-pattern-contract.v1.md`.

## The two pending SHOULDs, closed on published law

**S2** — the new glob contract decides the terminal `**` case against the reading I had written up: `src/**` matches `src`, `src/legacy.js` and `src/nested/legacy.js`. Predicate reconstructed from the published equivalence; **23 required examples + 22 derived properties + 5 composition cases, 0 failures**. I kept the v18 predicate alongside to measure the delta: every glob this origin actually uses spells its terminal wildcard `**/*`, the readings agree on all of them, so **no Run changed for the glob law**.

**S1** — workflows §6 plus `repair.schema.json closedWorld` publish the selection law. Reconstructed in `repair_selection_v19.py`: relevant universes (target occurrences ∪ the retained selected-program census, with a selected-but-unavailable binding contributing typed unresolved ownership), every retained `coverage2` of a relevant `sourceUniverse` ordered on all six members, a **non-vacuous** conjunction gate, and the five-field least-closed summary with absence folded in. Measured: typescript 1 universe/5 records, rust 2/5, rust-partial 3/8 — all ineligible, every dissent naming six members. 9 law-branch controls (including the branches no Run contains) PASS. The descriptor now **derives** that summary; my earlier one-favourable-record projection is gone, and a control refuses it.

## Area 3 (existing law) — executed, not planned

My v18 prediction is now a measurement: the first run refused exactly the predicted `clones-fact` rows (**V18-D8**). **V18-D7**'s invented branch is removed. New: **V19-D3** — 7 accounts called `unsupported-typed` for matrix cells that are `SUPPORTED-DESIGN` with a null deficiency, merging *capability support* with *work completion*; the host row is now derived by a shared §4/§5 derivation in `opensip_build.py`. Ten clauses ported into the retained closure (checks per Run rose 791→854, 970→1042, 1072→1137, 679→730, 700→780). Independent instrument: **0 refusals** (185/195/185/148/200). **11 discriminating controls all refuse**, 9 at the intended law; the 2 masked ones record where they were masked.

Honest consequence: all five Runs are now `indeterminate`, because required cells that are partial emit `required-cell-unsatisfied`. I manufactured no Coverage partition and lowered no `required` flag to keep a green verdict.

Also found by reading the changed native chapter for its own correction markers: **V19-D5** — zero-config selection *is* the `default` profile, whose requested set is fixed by the matrix; my vector hand-picked 4 capabilities and disclosed 2 absences, where the law yields 11/11/10 and **16** notices. **V19-D4** — `phase6_repair.schema_admit` never read `S.admit`'s result, so its owning-schema boundary measured nothing and hid four malformed control inputs.

Areas 1 and 2 remain green, and the three `programEntry` provenances (default, explicit, **synthesized**) are now measured: 8 cases, 0 failures.

## Reconciled deliverables

`output/blind-review.md` / `.json`: 102-file kit digest and declared parent, ancestry v14→v19, 46 declared stages (45 recorded when the final reconciliation stage ran, rule stated), 131 executed + 3 future-qualification, 0 MUST / 0 SHOULD / 1 advisory, **29 helper rows / 0 open**, 95 artifact digests, history `CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE`.

Disclosed rather than claimed: four law branches are implemented and measured but unexercised by a positive Run (§6 candidate custody, a selected-but-unavailable binding, multi-stage receipts, a js-synthesized cell); the generation-17 overwrite of two generation-16 files stays **OPEN** with no restoration verdict; every provider/compiler observation is a synthetic TCB input; no root admission, agreement or product qualification is claimed.
