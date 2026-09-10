# Workflow completion (peer-refused query adapter corrections)

**Verdict: `WORKFLOWS_READY_FOR_FINAL_RUN_BINDING`** (scoped: wrapper selected-closure reconstruction only)

Same S-origin kit-only author. V-origin peer refused prior READY (`WORKFLOW_QUERY_INCOMPLETE`, first failure `extra-view2-must-not-become-admitted-fact-view`). This pass corrects those existing-law gaps. Not a new fresh origin. Not independent acceptance. Not whole-consumer ACCEPT.

R-GRAPH and R-CHAIN remain **INCOMPLETE**. No sixth Run. Five frozen stores byte-identical.

## Peer dispositions applied

| Peer id | Owner | Correction |
|---|---|---|
| extra-view2-must-not-become-admitted-fact-view | §1/§8 | views from evidence.viewIds + evaluationInputRefs domain=view; extra Unit.ghost not selected |
| unselected-inventory-must-not-admit-endpoint | §2 | inventories from evaluationInputRefs domain=subject-inventory; Unit.delta ENDPOINT_UNKNOWN |
| coverage-entry-resolutionCompleteness-disclosed | §6 | copy CoverageResultV3 **entry**.resolutionCompleteness |
| IncomingSearchV1 (unimplemented path) | §6 | cite incoming-search-incomplete when completeSearch is false |
| close_run as gate then store walk | §8 | projection uses close_run.records; boolean flag without records is VIEW_UNKNOWN |

## Measurement

Preserved prior 40 controls plus 5 new discriminating cases (45/45 exit 0). Frozen probe: all five `QUERY.VIEW_UNKNOWN` without close_run.

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v5/output/scripts/query_charter_vectors.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v5/output/scripts/query_charter_test.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v5/output/scripts/workflow_correct_test.py
```

## 134 map

| reviewedScope | Count |
|---|---:|
| in-scope-executed | 46 |
| out-of-scope-frozen-run | 24 |
| standing-of-consumer-continuation-not-re-executed-here | 24 |
| notReached-historical-vector | 22 |
| out-of-scope-frozen-run-replay | 12 |
| futureQualification | 3 |
| in-scope-INCOMPLETE | 2 |
| measured-standalone-outside-established-48 | 1 |
| **total** | **134** |

46 executed + 2 INCOMPLETE. `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` and `R-REPLAY-THREE-VALUED` remain standalone-only; parents are not discharged.

## Remaining final integration

1. Later-supplied admitted Run (may supersede frozen hashes).
2. §3 `close_run` MUST return `records` with selected views/inventories/TA/Coverage/IncomingSearch — same interface `execute_graph_query` now consumes.
3. Do not fabricate `calls` facts.
4. Join traces/envelopes for R-CHAIN.

Failed prior adapter: `preserved-failures/workflow-query-recheck-v5-peer-refused/`. Path: `path-correction-record.v7.json`.

