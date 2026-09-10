# Workflow query peer review (S-origin successor v5)

**Verdict: `WORKFLOW_QUERY_INCOMPLETE`**

V-origin peer recheck of S-origin `workflow-corrections.v5` query adapter. This reviewer authored an earlier workflow predecessor; this is successor review, not a new fresh origin, not unaided independent reconstruction, and not acceptance of this reviewer's own pilot.

Author claim `WORKFLOWS_READY_FOR_FINAL_RUN_BINDING` is **not admitted**. Named-fix self-report does not prove remaining conformance.

Charter `57df2ed6…` MATCH. Snapshot-manifest `03271dd791c7e14b2213d28e3a0ba3820cde8943735ba6f4feedda26f2070bb3` 317/317 MATCH. Input snapshot unmodified. Execution used an isolated path-redirected copy only.

R-GRAPH and R-CHAIN remain **INCOMPLETE** (author respected; no sixth Run; frozen stores not admitted). Scoped controls that independently pass **must not** be promoted to full-Run acceptance.

## Prior findings independently rechecked

| Prior id | This pass |
|---|---|
| extra-view2-must-not-become-admitted-fact-view | **PASS** (`Unit.ghost` excluded; extra view2 not in `evidence.viewIds`) |
| unselected-inventory-must-not-admit-endpoint | **PASS** (`Unit.delta` → `QUERY.ENDPOINT_UNKNOWN`) |
| coverage-entry-resolutionCompleteness-disclosed | **PASS** (`entry.resolutionCompleteness.state=incomplete` disclosed) |
| IncomingSearch incomplete (unimplemented path) | **PASS** when selected via `evaluationInputRefs` |
| close_run boolean without records | **PASS** → `QUERY.VIEW_UNKNOWN` |

Call graph now: `close_retained_run` → `admit_selected_closure` over `semantic-evidence.viewIds` and `proof.evaluationInputRefs` (plus execution-inputs `selectedRefs`). Extra `view2` occupancy is not admission.

## First failure (remaining existing-law)

`isolated-inventory-universe-from-execution-inputs-enumerationPlanDigest` — query-projection-contract.v3.md §2.

Lawful shape: `evaluationInputRefs = selectedRefs + {execution-inputs}`. `InputRefV1.domain` has no `enumeration-plan`. Universe of inventory vertices is the EnumerationPlan program binding, located by `ExecutionInputsV1.enumerationPlanDigest` (already parsed for `selectedRefs`).

Independent graph with that lawful shape and isolated selected inventory vertex `Unit.omega` (no incident projected facts) returned **`QUERY.ENDPOINT_UNKNOWN`** instead of lawful empty neighbors.

Call graph: `admit_selected_closure` never reads `enumerationPlanDigest`; it only looks for `domain=enumeration-plan` on refs. Author adapter-control `evaluationInputRefs` **illegally includes** `domain=enumeration-plan`, which hid this join on their 45 cases.

`absentOrContradictoryNorms`: none.

## Required correction vs final-binding dependency

**Required existing-law wrapper correction before binding:** load EnumerationPlan from the already-parsed `ExecutionInputsV1.enumerationPlanDigest` and bind inventory universe from `(cellOrdinal, programOrdinal)`. Do not require `domain=enumeration-plan` on selected/evaluation refs.

**Final-binding dependency (distinct):** identity-and-evidence §3 `close_run` of a later admitted complete Run. Frozen `syntax-code` `2e74a6b2…` is not an accepted flag. Do not fabricate `calls` facts.

## What independently held (scoped control only)

file@enumerated refused; package-without-PMP ambiguous; cache/standing/TA/deficiency host fields ignored; without `close_run` → `VIEW_UNKNOWN`; empty neighbors ≠ native-unavailable; QueryResult compact joins; six-field parity; path hopCount=1; includeStart default false; truncated-page vs truncated-bound; five frozen stores byte-identical.

Author `query_charter_test` exit 0 against snapshot vectors is not remaining-conformance. Live `query_charter_vectors` aborted at schema inhabitance (`jsonschema` import missing under this helper `-I` path) and was not used as an oracle.

## 134 map standing (46 unrelated tests not re-run)

46 executed + 2 INCOMPLETE + 24 frozen-run + 24 standing + 22 historical notReached + 12 frozen replay + 3 futureQualification + 1 measured-outside-48 = 134. Incomplete IDs kept: `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`, `R-CHAIN-ZERO-CONFIG-TO-RECEIPT`.

`R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` (parent `R-RUN-RUST`) and `R-REPLAY-THREE-VALUED` (`evaluatorReplay`) remain standalone-only; global parent dependencies are not discharged.

## Owner clause map

| Clause | Status |
|---|---|
| §1 selection | PASS-scoped |
| §2 vertex domain / inventory universe | FAIL |
| §3 projection table/order | PASS-scoped |
| §4 params/BFS/includeStart | PASS-scoped |
| §5 cursor/page/bounds/cache | PASS-scoped |
| §6 disclosure | PASS-scoped |
| §7 faults | PASS-scoped |
| §8 wrapper vs traverse | PARTIAL (records consumed; enum-plan locator not taken from ExecutionInputsV1) |
| workflows §8 parity + QueryResult | PASS-scoped |
| original query charter paragraph | INCOMPLETE (admitted Run not executed) |

Independent measurements: `output/independent/review_query_adapter.py` exit **1**. Reports: `workflow-query-review.md` / `.json`. No whole-consumer ACCEPT.
