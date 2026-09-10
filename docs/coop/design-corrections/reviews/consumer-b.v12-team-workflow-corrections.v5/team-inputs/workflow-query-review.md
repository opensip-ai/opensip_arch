# Workflow query peer review (S-origin successor adapter)

**Verdict: `WORKFLOW_QUERY_INCOMPLETE`**

V-origin peer review of S-origin `workflow-corrections.v4` query adapter. This reviewer authored an earlier workflow predecessor; this is successor review, not a new fresh origin, not unaided independent reconstruction, and not acceptance of this reviewer's own pilot. Author claim `WORKFLOWS_READY_FOR_FINAL_RUN_BINDING` is **not admitted**.

Charter `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` MATCH. Snapshot-manifest `409860cdee1bc695dc849c4e2924773864aa10c69fa6d3f0bd541a64c2cdce8f` 302/302 MATCH. Input snapshot unmodified. Execution used an isolated path-redirected copy only.

R-GRAPH and R-CHAIN remain **INCOMPLETE** (author respected; no sixth Run; frozen stores not admitted). Algorithmic/scoped controls were checked independently and **must not** be promoted to full-Run acceptance.

## First failure

`extra-view2-must-not-become-admitted-fact-view` — query-projection-contract.v3.md §1 / §8.

Call graph: `execute_graph_query` calls `close_run` as a gate, discards its return, then `load_closure_records` iterates **every** `view2:` key in the object table. Independently adding an extra `view2` with calls fact `Unit.alpha → Unit.ghost` (not on any Run `evidence.viewIds`; `Run.evidenceId` is not even retained) changed auto-selected neighbors to `['Unit.beta', 'Unit.gamma', 'Unit.ghost']`.

Reading blobs is not admission authority. A callback/boolean `close_run` is not complete retained Run replay.

## Exact failures (existing-law reconstruction, not missing norms)

| id | Owner | Actual |
|---|---|---|
| extra-view2-must-not-become-admitted-fact-view | §1 admitted views of this Run | every `view2` blob is selected |
| unselected-inventory-must-not-admit-endpoint | §2 evaluationInputRefs inventories + EnumerationPlan universe | extra `SubjectInventoryV1` admitted `Unit.delta` |
| coverage-entry-resolutionCompleteness-disclosed | §6 + CoverageResultV3 `entry.resolutionCompleteness` | wrapper reads payload top-level; independent incomplete entry → `resolutionLimitations=[]` |

`absentOrContradictoryNorms`: none. IncomingSearchV1 citation (§6) is an unimplemented existing-law path, not a demonstrated hole in the kit.

## What independently held (scoped control only)

Author 40/40 re-executed from isolated copy (exit 0) is self-consistency, not an oracle. Independent reviewer graph also held: two-edge neighbors; `file@enumerated` / package-without-PMP; cache ignored; without `close_run` → `QUERY.VIEW_UNKNOWN`; empty neighbors ≠ `native-evidence-unavailable`; QueryResult compact joins; six-field human/json/agent parity; five frozen stores byte-identical and `QUERY.VIEW_UNKNOWN` without `close_run`. `close_retained_run.completeGraphClose is False` as labeled. `traverse_projected_graph` remains `algorithmic`.

## Required correction vs final-binding dependency

**Required existing-law wrapper correction before binding:**

1. Select views from the admitted Run (`semantic-evidence.viewIds` / `proof.evaluationInputRefs` domain=view), not every `view2` blob.
2. Select inventories from `evaluationInputRefs` domain=subject-inventory; universe from EnumerationPlan program binding.
3. Bind TargetAttributionV1 from this Run's selected inputs.
4. Copy CoverageResultV3 **entry** resolutionCompleteness / coverage / deficiency.
5. Cite IncomingSearchV1 when search is not complete.
6. Consume `close_run`'s admitted closure as projection input, not a success flag plus a second store walk.

**Final-binding dependency (distinct):** identity-and-evidence §3 `close_run` of a later-supplied admitted complete Run, then `execute_graph_query` over that closure. Do not treat frozen `syntax-code` `2e74a6b2…` as an accepted flag. Do not fabricate `calls` facts. If the admitted graph lacks a projectable binary rung, refuse or disclose.

## 134 map standing (46 unrelated tests not re-run)

Author counts 46 executed + 2 INCOMPLETE + 24 frozen-run + 24 standing + 22 historical notReached + 12 frozen replay + 3 futureQualification + 1 measured-outside-48 = 134. Incomplete IDs kept: `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`, `R-CHAIN-ZERO-CONFIG-TO-RECEIPT`.

`R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` (`completeRunProperty`, parent `R-RUN-RUST`) and `R-REPLAY-THREE-VALUED` (`evaluatorReplay`) remain standalone-only; global parent/complete-Run dependencies are not discharged.

## Owner clause map

| Clause | Status |
|---|---|
| §1 selection | FAIL |
| §2 vertex domain | PARTIAL (PMP/malformed/unknown pass; inventory selection fails) |
| §3 projection table/order | PASS-scoped |
| §4 params/BFS/includeStart | PASS-scoped |
| §5 cursor/page/bounds/cache | PASS-scoped |
| §6 disclosure | FAIL |
| §7 faults/host.requestId | PASS-scoped |
| §8 wrapper vs traverse | PARTIAL |
| workflows §8 parity + QueryResult | PASS-scoped |
| original query charter paragraph | INCOMPLETE (admitted Run not executed) |

## From-scratch commands

```
/tmp/opensip-architecture-review-env/bin/python -I -B …/output/isolated-snapshot/scripts/query_charter_vectors.py
/tmp/opensip-architecture-review-env/bin/python -I -B …/output/isolated-snapshot/scripts/query_charter_test.py
/tmp/opensip-architecture-review-env/bin/python -I -B …/output/independent/review_query_adapter.py
```

Measured exits: author vectors 0, author assert 0, independent **1**.

No whole-consumer ACCEPT. No root admission. No product/host/compiler qualification.
