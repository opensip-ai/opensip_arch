I’ll implement the six root-requested corrections in the owned workflow files, starting from the composer’s blocking law, comparison execution state, admitted baseline adoption, and real SARIF/pivot boundaries.I’ll apply the schema and model corrections first (blocking law, comparison execution state, admitted adoption, SARIF, no false adoption errors), then extend the checker into v6.v5’s 174 controls held. I’ll add the remaining replay-case verdict projections so the loop covers the root suite, not only the first slice.v6 corrections are in the owned workflow files only. Bounded checker: **224/224 passed**, including preserved **v5 174**. That is not full profile acceptance. Report: stdout or `grok-workflow-projection.v6/` only (v5/history not overwritten).

## What changed

**1. Verdict unknown = composer `blocks()`**  
`cross-family-edge-not-owed` is a non-blocking disclosure. Import deficiencies block only when `evidenceKind` is required. Correspondence causes are not “unknown”; they are unmatched/live. Waived live findings plus incomplete enumeration stay indeterminate. Replay-case projections keep the proof verdict (file/runtime/history/symbol/scope/budget/nongating, including optional unknown).

**2. Comparison carries execution independently**  
ComparisonDescriptor schemaMajor 2 now requires `currentEvaluationState` and `currentExecutionDeficiencies` (exact source/cause, not collapsed into `ruleDeficiencies`). Budget-exhausted / native work failure makes comparison indeterminate even if all rules are disabled. Matched fail still dominates.

**3. Public adoption is `adopt_admitted_baseline_v3`**  
Uses `close_run` + Plan policy/waiver/ScopeDocument/snapshot join and trusted custody. `adopt_baseline_v3` is internal. `retentionPins` must be the unique sorted `{run3} ∪ pivotClosure.closureId` set. Root `scope_document` fixture: 1 finding, adoption succeeds. Ordinary analysis without ScopeDocument still refuses adoption. Reminted wrong entries/pins/scope refuse.

**4. Compare maps are not required before whole refusal**  
Unmapped/schema/recipe whole-outs do not demand E0–E3 maps. Unchanged policy/scope/waiver/detector axes copy E4. `compare_admitted_v3` derives current from an admitted Run. Same-context baseline/current performs comparison; policy-changed current without an E1 re-eval is typed pivot-unavailable. Unit `pivotPresence` maps are not full comparison evidence.

**5. SARIF adapter**  
Waived findings emit SARIF `suppressions` (`kind=external`, `status=accepted`). `message.id` is defined on rule `messageStrings`. URIs are percent-encoded. Validated against the isolated adapter schema, **not** claimed as OASIS full SARIF qualification. `serialization_overflow_termination` validates as evaluator3 `StepTermination`. Candidate and graph-query request schemas validated.

**6. Ordinary `project_admitted_run_v3`**  
Returns `scopeDocumentParameter: absent|selected`. No adoption-error advisory on ordinary analysis.

## Tests

- v5 control coverage preserved (174)
- Non-blocking cause, waived+incomplete, execution comparison, disabled+budget
- `adopt_admitted_baseline_v3` on `scope_document={include:['src/**']}` plus remint refusals
- `compare_admitted_v3` same-context and policy-change pivot-unavailable
- Replay-case verdict alignment (file, two-universe, runtime, history, symbol, scope, budget, nongating)

## Actual blockers (not this unit)

- `PivotClosure.kind` does not admit Plan `provider` enumerator closures; those are omitted from pins.
- Fixture detector vs evaluator platforms differ (`any` vs `macos-aarch64`); detector-change E0 can still be pivot-incompatible.
- Not every check-replay import/test row is in the projection loop (test-result / some symbol collision rows remain).
- No OASIS SARIF document in-tree; adapter subset is not full-schema qualification.
- Execution-input-manifest completion remains a separate root blocker. Mock `pivotPresence` on `compare_v3` is still a unit path, not retained-run evidence.
