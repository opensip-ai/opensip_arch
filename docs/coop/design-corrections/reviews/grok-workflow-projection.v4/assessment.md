I’ll pick up the seven workflow corrections in the owned schema folder and three workflow files, then run the checker after the remaining patches.The gating schema text is already in place. Next I’ll scan remaining model defaults and the checker’s output path, then complete tests without writing a historical receipt.I’ll write the checker so it covers the seven laws, restore the original cases, and emit only an explicit `--output` path or stdout.Two check failures: declared-origin used the wrong `accept_origins` side, and the receipt guard was matching its own filename strings. I’ll fix both.The seven workflow-projection gaps are closed in the owned evaluator3 schemas and the three workflow files. Bounded checks ran after the fixes: **141/141 passed**. That is not complete admission and not a full Run replay.

## Bounded result

```
/tmp/opensip-architecture-review-env/bin/python -I -B \
  .../workflows/check-workflow-projection.v3.py \
  --output /tmp/opensip-workflow-projection-scratch.json
```

- passed: `true`
- count: `141`
- failed: `[]`
- standing: isolated evaluator3 schemas + pure projection over **admitted** finding/proof-shaped objects
- checker default is **stdout**; `--output` writes a path you name. It does **not** write `workflow-projection-report.v1/v2/v3.json`

This projector consumes admitted proof results. Root owns `close_run` → full replay and any input-execution-manifest work.

## The seven laws, as implemented

| Gap | Behavior now |
|---|---|
| 1 Gating | `ruleResults` have no gating field. Gating is policy `enabled ∧ gate ∧ severity floor`. Advisory live findings do not fail, including when `outcome=fail`. `executionDeficiencies` / `budget-exhausted` stay independent. Optional `proof_verdict` must match the derived verdict. |
| 2 Baseline unmatched | Comparison keeps both sides. `baseline-or-current` keeps gating unmatched obligations when current is empty or the rule is gone. `current-only` uses current policy coverage. Advisory unmatched does not always-block. Matched CODE-NET-NEW fail dominates. |
| 3 Candidates | Matched group-by-fingerprint **after** BaselineEntry agreement: one `candidateId`, all `findingIds`, per-occurrence params kept. Unmatched stay keyed by `findingId`. Suppression follows that logical id; fingerprint suppression does not hide unmatched. |
| 4 SARIF | `FindingSurface` is the intermediate row. `project_sarif` emits SARIF **2.1.0** (`sarif-adapter:2`): one result per `finding3`, citations + generic-7 message params, `partialFingerprints` only when matched. |
| 5 compare_v3 | Current `E4` / `waivedC` / `entryRules` come from admitted occurrences. Caller `presence`/`entryRules` refuse. Missing `occurrences`/`ruleResults` refuse; `ruleResults=[]` does not heal. Independently admitted `pivotPresence` is E0–E3 only, no invented False defaults. Adapter emits comparison **schemaMajor 2**; historical major 1 is refused, not run as v1 semantics. |
| 6 Baseline verify | Schema + H identity + context-document digest bindings + `side=baseline` unmatched + `run3\|closure2` pins. Scope join is mandatory (`analysis_spec=None` is not a bypass). `exportedAtUtc` is trusted custody input. Origin Run admission is a prerequisite; this path does not call replay. |
| 7 Whole shapes | Unmapped / declared-origin / recipe-unsupported outputs include required `contextDelta`. Unmapped: `comparisonPerformed=false`, empty unmatched/coverage, `REQUEST.PRECONDITION_FAILED`. `CONFIG.INVALID` is not used as a DomainDetail. |

Owned paths only: `workflows/schemas/evaluator3/`, `workflow_projection_model.v3.py`, `check-workflow-projection.v3.py`, `workflow-projection-contract.v3.md`. LIVE / frozen21 / history / root foundation were not edited.
