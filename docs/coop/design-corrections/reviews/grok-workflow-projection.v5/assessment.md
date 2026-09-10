I’ll add a `project_admitted_run_v3` adapter over root `close_run` (full replay) and drive the existing projections from actual admitted proof objects, without touching root-owned identity/native code.The two-universe graph and `close_run` are confirmed. I’ll add the admitted-run adapter and bounded checks next, writing reports only to a new v5 folder.`project_admitted_run_v3` is in the owned workflow model. It calls root `identity-model.v3.close_run` (full replay), builds occurrence maps from the admitted Plan/policy/emission/proof, and drives the existing baseline-entry, candidate, SARIF, and current-verdict projections.

Bounded checker: **174/174 passed** (v4 **141** controls preserved). That is not full Run integration and not profile acceptance.

## Typed outputs (synthetic owner-admitted graphs)

| Graph | Findings / subjects / fingerprints | Baseline entries | Logical candidates | SARIF 2.1 results | Current verdict | Artifact adoption |
|---|---|---|---|---|---|---|
| `multiple_universes=True` | 6 / 6 / 3 | 3 | 3 (all 6 `findingId`s kept, 2 configs each) | 6, citations + message params | **fail** (policy ∧ proof) | not performed |
| ordinary file positive | 3 / 3 / 3 | 3 | 3 | 3 | **fail** | not performed |
| `gate=False` | 3 live findings | 3 | 3 | 3 | **pass** (nongating) | not performed |

Same-path configs across two universes share a fingerprint; different (or identical) params do not drop occurrences.

Ordinary analysis with **no** ScopeDocumentV1 parameter is legal. Baseline **entry** projection does not need one. Baseline **artifact adoption** still does: `adopt_baseline_v3` on these graphs refuses `BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER`. Scope joining law is unchanged. To test successful adoption, root needs a fixture that **selects** the existing ScopeDocumentV1 parameter; this adapter will not invent that selection or `exportedAtUtc`.

## What the adapter does / does not do

- **Does:** `close_run` → read Plan policy blob, emission-plan parameter, proof findings, fingerprint preimages, parameter records → `project_baseline_entries` / `project_candidates` / `project_sarif` / `current_run_verdict`. Gating from admitted policy only. No producer `verified` flags or expected finding lists.
- **Does not:** call `open_run_closure` (owner-internal). Reconstruct `importScopes` / `importFlagsAdapter` / `coverageScopes` (root input driver). Claim execution-input-manifest completion. Qualify real extraction.

Report path: stdout, or `--output` under `grok-workflow-projection.v5/` only. Historical v1–v4 receipts were not overwritten.

## Remaining integration gaps (not this bounded unit)

1. **ScopeDocument-selected adoption** — no current replay fixture selects ScopeDocumentV1; positive artifact adoption is untested.
2. **Execution-input-manifest completion** — view totality / candidate-cell execution is still a separate root blocker.
3. **Comparison** — E0–E3 pivot maps and a retained baseline artifact are not produced from `close_run` here; this subtask stopped at entries, candidates, SARIF, current verdict.
4. **M3 cause table** — identity-schemas.v3 now registers additional native/import/execution causes (`scope-without-coverage`, `overload-ambiguous`, `zero-owed-wrappers`, `work-budget-exhausted`, …). Workflow projection consumes proof `ruleResults.deficiencies` after close_run; it does not re-derive those causes.
5. **Test counts are not acceptance.** 174 bounded checks ≠ complete admission, ≠ public-registry integration, ≠ full evaluator3 profile.
