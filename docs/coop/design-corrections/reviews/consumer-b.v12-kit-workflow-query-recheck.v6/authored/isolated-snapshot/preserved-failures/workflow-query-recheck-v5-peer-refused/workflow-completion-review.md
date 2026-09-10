# Workflow completion (query adapter corrections)

**Verdict: `WORKFLOWS_READY_FOR_FINAL_RUN_BINDING`**

Same S-origin kit-only team session. Role change to **author** of remaining query-adapter corrections identified in own workflow-recheck.v4. That review cannot independently accept this new work. Not product implementation, not whole-consumer ACCEPT, not root admission.

R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR and R-CHAIN-ZERO-CONFIG-TO-RECEIPT remain **INCOMPLETE** until actual admitted-Run query/traces/envelopes execute together. No sixth Run was invented. All five frozen Run stores are byte-identical.

## Custody

| Object | SHA-256 |
|---|---|
| original-consumer-charter.txt | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` |
| prior snapshot-manifest | `93926c8f2dbf1b45ab06e3479ad4e06ebf40405de0eef4a6a5ef6a040d773999` |
| own workflow-review.md | `c320ef2c7d046249a775c1a4e4a4c201e7cdaa2638be72720b5b5063b700a45e` |
| own workflow-review.json | `43d472cabd85d5f19705b4d1d490a1864548e7fd79a9c60ba6d425d3220e2f30` |

Failed prior adapter preserved under `preserved-failures/workflow-recheck-v4-query-adapter/`. Path redirects: `path-correction-record.v6.json`.

## Adapter corrections (existing law, not new semantics)

Public `execute_graph_query(request, run, objects, blobs, host)`:

1. Admits closed request/schema/params and `host.requestId` precondition.
2. Requires `close_run` of retained bytes (not a synthetic success flag). `close_retained_run` rehashes blobs and parses run3 H identity; it is **not** identity-and-evidence §3 complete-graph close.
3. Joins `{runId}|{snapshotId}|{latest:true}` to that Run.
4. Projects vertices/edges from admitted views, retained payloads, and TargetAttributionV1. Ignores `host.cache`, `host.standing`, `host.targetAttributions`, `host.evaluationDeficiencies`. Does not take caller edge/limitation arrays.
5. Package identity without `packageManifestPath` → `QUERY.ENDPOINT_AMBIGUOUS`.
6. `native-evidence-unavailable` only when no **selected** view matches `relation@minResolution`. Empty neighbors with a matching view are not that disclosure.
7. Emits GraphQueryResponseV1, CommandEnvelope `kind=query` with compact `QueryResult` (`items`=page count, `truncated`=context flag, `completenessMet` iff `countBasis=exact`, `nextCursor` iff identical context token), and exact six-field human/json/agent parity.
8. `traverse_projected_graph` remains labeled `algorithmic`.

Independently chosen adapter-control endpoints: `Unit.alpha` / `Unit.beta` / `Unit.gamma`. 40/40 discriminating cases exit 0. Frozen-store probe: all five `QUERY.VIEW_UNKNOWN` without `close_run`; no `calls@resolved-callee` fabricated.

## From-scratch commands (all exit 0)

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v4/output/scripts/query_charter_vectors.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v4/output/scripts/query_charter_test.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v4/output/scripts/workflow_correct_test.py
```

## 134 original IDs

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

In-scope 48: 46 executed, 2 INCOMPLETE (`R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`, `R-CHAIN-ZERO-CONFIG-TO-RECEIPT`).

`R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` (completeRunProperty) and `R-REPLAY-THREE-VALUED` (evaluatorReplay) remain executed only as standalone vectors; admitted global Run binding is still required and is not discharged by relabeling.

## Remaining final integration

1. Supply a later-corrected admitted Run (may supersede frozen hashes). Do not treat `2e74a6b2…` as an accepted flag.
2. Pass identity-and-evidence §3 `close_run` of that export into `execute_graph_query`.
3. If the admitted graph lacks a projectable binary rung, refuse or disclose — do not fabricate `calls` facts.
4. Join traces/envelopes to that admitted Run for `R-CHAIN-ZERO-CONFIG-TO-RECEIPT`.

## Limitations

- Frozen Run close_run / other-Run replay out of scope; stores not rewritten.
- R-GRAPH not claimed executed.
- Adapter-control retained H-graph is not a B12 complete Run and not frozen-store admission.
- close_retained_run is query-scoped identity/rehash, not identity-and-evidence §3 complete-graph close.
- No whole-consumer ACCEPT. No root admission. No product/host/compiler/crypto qualification.

