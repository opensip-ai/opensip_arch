# Audit area 3 — ExecutionInputs: clause → code map, and what the retained helper omits

Generation: `consumer-b.v18`. Inputs: the 101-file kit at `subject/` only.
Instrument: `output/lib/indep_execution_inputs.py` (NEW, written from the clauses before the old
helper was re-read), compared afterwards with `output/lib/opensip_closure.py`
(`check_execution_inputs_derivation`, `check_seal_and_proof`, `check_views`).

**Execution standing of this note.** The clause reading, the new instrument and the comparison
below were produced in generation 18. The instrument has **not been executed**: the reference
interpreter could not be invoked in this session (tool permission denied for running
`/tmp/opensip-architecture-review-env/bin/python`). Every row marked PREDICTED is therefore a
reading of code and clauses, not a measured result. Nothing in `output/` was re-exported,
re-closed or re-replayed after the Area 1 / Area 2 work, and no report numbers were changed.

---

## 1. Clause coverage

| # | Clause | Retained closure today | New instrument |
|---|---|---|---|
| X1 | schema `NativeCoverageAccountV1.applicability` closed enum; `allOf` pins `coverageIds maxItems 0` for the four non-supported kinds; §5 "none" / "do not fabricate Coverage at null U" | covered per branch (`EXECUTION_INPUTS_COVERAGE_DERIVE:*_NO_COVERAGE`, `DO_NOT_FABRICATE_COVERAGE_AT_NULL_UNIVERSE`) | same, plus the literal-membership check and the binding join for each `unavailable-*` kind (`unavailable-unselected` must actually sit on an unselected enumerator; `unavailable-null-universe` on a null U) |
| X2 | `CellProgramOutcomeV1.allOf` cross-field law | partial: `COMPLETE_CARRIES_NO_PAIR` only | full: complete ⇒ null pair **and** integer `stageOrdinal` **and** null `stageOrdinalNullReason`; null `stageOrdinal` ⇒ typed reason inside the enum |
| X3 | §3 selected-producer joins: non-null `stageOrdinal` matching a receipt, enumerator closure is a **Plan-selected provider**, stage-spec `producerClosure`, view `planId`, **each named scope `sourceUniverse` vs binding U**, receipt `outputDomains` vs the stage; "Selected U cannot become complete by omitting the stage and views" | **absent as a binding join.** `check_seal_and_proof` checks stage↔stage-spec output domains and a Plan-selected stage producer; `check_views` checks view `planId`, producer kind and scope enumerator — but nothing joins a **cell outcome** to its receipt, and no check compares a named scope's `sourceUniverse` to **that binding's** U | implemented: receipt/stage resolution by ordinal, receipt producer == cell enumerator, receipt `outputDomains` == the stage, attributed view `planId`/producer, every named scope `sourceUniverse` == binding U, and complete-selected ⇒ non-empty `viewDigests` |
| X4 | §4 outcome table, primary pair, membership, "complete + partial inventory", "empty kinds" | covered, **but with one branch the table does not contain** — see finding A below | the four table rows literally, with interpretation I-1 declared for row 2, plus the table row that the helper adds is **not** reproduced |
| X5 | §5 per-applicability envelopes; `coverageIds` equality; payload **and** subject-scope `sourceUniverse` == U; mixed complete+unknown; unsupported-typed pair from matrix+registry; `inapplicable-vcs` basis; **expected-subject membership**; explicit silence on `targetUniverse` | partial: equality, the **payload** universe check, mixed handling, matrix+registry pair, VCS basis. The **subject-scope** half of the universe clause and the whole **expected-subject membership** clause are absent | all of §5, including the scope half and the expected-subject join (interpretation I-2), and an explicit NOT-APPLICABLE row recording that §5 deliberately does not constrain `targetUniverse` |
| X6 | §4/§6 cardinality, kinds set-equality, `candidateResultRefs` equality, §6 candidate custody | cardinality / kinds / refs equality covered; **§6 custody (ids, paths vs this binding's Plan census, universe, snapshot `contentSha256`/`byteLength`, complete `examinedPaths`, complete-empty shape) is not implemented at all** | implemented, and where no envelope exists it is recorded as an **exercise gap**, not as a pass |
| X7 | `viewDigests` DESC: view2 H suffixes, equal to the **captured receipt** views attributed to this cell/program/U/producer | absent: `_cell_view_digests` reads the declared list and never compares it with any receipt | implemented (`OUTCOME_VIEWS_COME_FROM_THE_CAPTURED_RECEIPT`, plus H-suffix resolution) |
| X8 | §1 receipt totality over `execution-plan.stages`, `outputDomains` equal the stage, `outputRefs ⊆` domains, typed unavailable receipts; `selectedRefs` exact totality incl. coverage cover, blob-domain == `hostDerivedRefs`, imports == Plan `importIds`, forbidden domains | partial: `outputRefs ⊆ outputDomains`, stage-produced == complete-receipt union, blob-domain == `hostDerivedRefs`, import joins. **Receipt↔stage totality, receipt `outputDomains` == the stage, receipt `stageSpecDigest` == the stage's, the typed-unavailable receipt shape, `EXECUTION_INPUTS_SELECTED_COVER` and the forbidden-domain guard (on `selectedRefs` itself) are absent** | all implemented |
| X9 | §7 `evaluationInputRefs = selectedRefs + XI`; `execution-inputs` is not a `selectedRefs` member; `proof.executionInputsDigest` required | equality and the single XI member covered | same, plus the explicit non-circularity check and a recomputation of `rec_digest(ExecutionInputsV1)` against the XI digest |
| X10 | `UnselectedEnumeratorRef` (const `optional-unselected`, lawful only when `required=false`) vs `SelectedEnumeratorRef` ("Executable unavailability with this selected closure is `UnavailableProgramBindingV1`"), joined to `stageOrdinalNullReason` | absent: the typed null reason is accepted as asserted | derived: `optional-unselected` iff the binding carries an unselected enumerator on an optional cell, otherwise `unavailable-binding`; or the row may name an `unavailable` receipt whose reason is `provider-unavailable` |

Existing self-check counts were not treated as evidence: the three rows above marked **absent**
are clauses the old helper does not represent at all, and they were found by reading the clause
first and the helper second.

---

## 2. Findings this comparison produces

### A. `V18-D6` (defect in my own helper, not in the kit) — a derived-state branch the table does not contain

`opensip_closure.py:2737` adds:

```
elif unsupported and not any(v[0] == 'complete' for v in my_accounts.values()):
    derived_state = 'unavailable'
```

§4's fourth row is "all inventories complete, **every account complete/inapplicable/unsupported**,
candidate complete if owed → `complete`". A cell whose accounts are all `unsupported-typed` with
all inventories complete is therefore **complete** by the published table, and §5 routes the
unsupported work to `requiredCellDeficiencies` / the proof bridge instead — which is the same
distinction the helper itself records elsewhere
(`EXECUTION_INPUTS:COMPLETE_EXECUTION_IS_NOT_CAPABILITY_SUPPORT`: "account complete is EXTRACTION
completeness"). The added branch would refuse a lawful graph. It is dormant on the five positives
(no cell has an all-unsupported account set), so this is an over-strict law rather than a missed
refusal, and it must be removed rather than kept as a safety margin. The new instrument does not
reproduce it.

### B. `V18-D7` (PREDICTED defect in my own sealed fixtures) — `clones-fact` cells claim a complete outcome while expected file subjects are in no returned partition

* `evaluator-projection-registry.v1.json` → `relations.clones.sourceSubjectKind = "file"`.
* The `clones-fact` cells bind the **whole** file extent (`run_ts_full.py:210`,
  `run_syntax_code.py` `inv_specs`), which is correct and was itself a prior correction
  (V17-D4, "the capability does not narrow the kind's extent"), and retain a **complete** file
  inventory over it.
* The returned clones partition covers only the code files with clone bodies
  (`run_syntax_code.py:321` — `['src/a.js', 'src/b.js']`).
* §5: "every expected source subject from this cell's inventory/extent of the relation's
  subject-kind must be a member of some returned partition … Missing expected subjects →
  incomplete **even if the remaining Coverage is complete**", and §4 row 3: "any
  supported-available account not complete → `partial`".

Under interpretation **I-2** (declared in the instrument's docstring) the `clones-fact` outcome in
every Run that has one cannot be `complete`; the honest row is `partial`, with the required-cell
consequence handled by the proof bridge (§4: a `null` row deficiency bridges to
`required-cell-unsatisfied`). The alternative reading — that §5's closing sentence ("Global missing
expected subjects still needs a reconstruct join; this unit does not invent that census") suspends
the table row entirely — is recorded and **not** assumed.

Note the interaction that makes widening the scope the *wrong* repair: `scopeCapabilityLaw`
(identity-schemas.v3, enforced at `opensip_closure.py:3464`) says a scope carrying paths the
selected grammar cannot read is an **unsupported scope** whose Coverage must carry the prescribed
`unknown` + typed pair. So the lawful shapes are either (i) the narrow partition plus a `partial`
cell outcome, or (ii) an additional partition for the unreadable remainder carrying the prescribed
unsupported pair — which is "mixed complete+unknown → not complete", i.e. `partial` again. Both
reach the same conclusion: the `complete` row is the defect.

This finding is **PREDICTED, not measured**: it needs the instrument to run over the five exported
stores, and the repair needs the Runs re-derived, re-sealed and re-replayed. Both are blocked on
interpreter execution, so it stays an **open MUST** and the verdict stays `CHANGES_REQUIRED`.

---

## 3. Exercise gaps recorded (not passes)

| Gap | Why it matters | Status |
|---|---|---|
| §6 candidate-only custody: no Run declares a `clones-near` / `clones-cross-tsjs` cell, so no `CandidateProducerResultV1` exists. `candidateResultRefs` is `[]` in all five | the whole of §6 (group digests, `sourceBodies` id/path/universe/snapshot joins, `examinedPaths` == this binding's Plan census, complete-empty envelope) is unexercised; the equality law passes vacuously | open; needs a new positive Run plus its own discriminating controls |
| selected + unavailable binding (`SelectedEnumeratorRef` with `universe=null`, `stageOrdinalNullReason = unavailable-binding`, or a receipt with `state=unavailable`, `unavailableReason=provider-unavailable`) | the only unavailable binding in the positives is the **optional-unselected** shape, so half of §3's second sentence and the whole `StageReceiptV1.allOf[state=unavailable]` branch are unexercised | open |
| multi-stage execution plans | every Run declares exactly one stage, so receipt↔stage totality and "one receipt per stage" cannot fail in the positives | open |
| Area-3 discriminating controls (account relabelled, `coverageIds` narrowed to a complete subset, Coverage fabricated at null U, `complete` row over a partial inventory, unzipped carrier pair, view attributed without a receipt, `stageOrdinalNullReason` swapped) | required by the instruction ("unsupported/data-only and partial cases need their own discriminating controls") | not yet written — see the session report |
