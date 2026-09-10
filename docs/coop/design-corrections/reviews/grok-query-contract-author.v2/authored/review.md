# Query successor correction v2 — Grok coauthor (not ACCEPT)

**Standing.** Isolated evaluator3 query successor under `/tmp/opensip-design-corrections/query-successor.v1`. This turn addresses root’s six QROOT findings from `query-successor-root-review.v1`. Coauthor feedback, not a blind review. Frozen23, live repo, product code, commits, and agents were not edited. Independent successor review, a new blind consumer, and application review remain required. Passing these checks is not acceptance.

**Python.** `/tmp/opensip-architecture-review-env/bin/python -I -B`.

---

## 1. Verdict

**QROOT-1..6 corrected on the same owned files.** Focused checker **81/81 PASS** after three original paging/cursor-bind failures in `traverse_projected_graph`. No ACCEPT claimed.

Root numbering in `confirmed-findings.v1.md` differs from the correction brief. Dispositions below use the **brief’s 1–6** and name the root probe ids.

---

## 2. QROOT dispositions

| Brief | Root probe / note | Disposition |
|---|---|---|
| **1** Strong `execute_graph_query` always `close_run`; synthetic goldens on a separate internal entry; `host.standing` must not bypass | `strong-wrapper-with-no-retained-run` | **Fixed.** Public entry requires retained `run`/`objects`/`blobs` and `close_run`. `host.standing=synthetic-admitted-fact-graph` with an invented graph is `IDENTITY.UNKNOWN` / `QUERY.VIEW_UNKNOWN`. Algorithm goldens use `traverse_projected_graph` only. |
| **2** Cache is not authoritative; poison/add/change/delete on admitted Runs; cache must not change result | `same-run-poisoned-derived-cache` | **Fixed.** Strong path does not read `host.cache`. On the actual M3-admitted Run, omitted/empty, added, changed-provenance, and deleted cache all return the same one outgoing reference. |
| **3** Vertex domain; unknown identity is not a zero-hop; fault precedence; new details if needed | `unknown-endpoint-zero-hop` | **Fixed.** Vertices = inventory rows from proof `evaluationInputRefs` (universe from EnumerationPlan bindings) ∪ projected fact endpoints. Unknown universe/`missing` → `QUERY.ENDPOINT_UNKNOWN`, not a zero-hop path. Known isolated `bar` with empty outgoing incidence is complete empty. Precedence: malformed `QUERY.PARAMS_MALFORMED` → package-without-path / multi-vertex `QUERY.ENDPOINT_AMBIGUOUS` → zero-match `QUERY.ENDPOINT_UNKNOWN`. |
| **4** Derive attribution and deficiencies from retained closure; `unresolvedEdgeCount`; partial/not-attempted; unresolved must not vanish | `actual-incomplete-incoming` | **Fixed.** TargetAttributionV1 and IncomingSearchV1 come from proof inputRefs. `host.targetAttributions` / `host.evaluationDeficiencies` are ignored. Deficiency citations keep exact `source`/`cause`/`inputRefs` (no coerce-to-execution). Coverage limitations copy `resolutionCompleteness.state` including `not-attempted`/`partial`, `unresolvedEdgeCount`, and incoming-search incompleteness even when default view selection is `references@resolved-binding`. Zero incoming rows are not “no callers.” |
| **5** One visited-endpoint law; check before extra work; `maxVisitedNodes=1` must not report 2 | `actual-path-visited-cap-one` | **Fixed.** `visitedNodes` is distinct canonical endpoints **entered**. Fact scans are not visits. Cap is checked **before** entering an unvisited vertex. One-edge path with `maxVisitedNodes=1` reports `visitedNodes=1`, `truncated-bound`, no path. Exactly-at-cap with empty frontier remains complete. Page vs operation truncation unchanged. |
| **6** Join explicit snapshot selector to `run.snapshotId`; index is not authority; latest is a trusted observation | `wrong-snapshot-index-result` | **Fixed.** Request `{snapshotId}` must equal the admitted Run’s `snapshotId`. A stale `runsForSnapshot` mapping a fake snapshot onto that Run is `QUERY.VIEW_UNKNOWN`. Matching snapshot on the admitted Run succeeds. `{latest:true}` requires `host.latestRunId` equal to `close_run` identity and is never derived from static Run bytes. |

**Other joins from the root review**

- Unsupported `relation@rung` is operation-refused (`QUERY.RELATION_UNSUPPORTED`); individual unprojectable facts are omitted with disclosure.
- Endpoint order is the utf-8 tuple `(universe, kind, nativeSubjectId, packageManifestPath or "")` then `fact2`.
- Cursor binds project+Run+fact-views+operation+effective params/position; it grants no authority. Continuation requires `{runId}`.
- Full failure carrier is CommandEnvelope major 3 `kind=failure` with nonempty `errors` and no `run`. `QueryRefusal.termination()` remains StepTermination; `envelope()` is the public carrier. Unknown-view and unsupported-major now have registered DomainDetails. No Run is invented before selection.

---

## 3. New DomainDetail inventory (root count-guard handoff)

Prior six remain. **Three new** this correction:

1. `QUERY.ENDPOINT_UNKNOWN`
2. `QUERY.SCHEMA_MAJOR_UNSUPPORTED`
3. `QUERY.VIEW_UNKNOWN`

Registered in `public-detail-registry.v1.json` and both `common` DomainDetailCode enums. No new D9 family. Error codes still `REQUEST.PRECONDITION_FAILED`, `REQUEST.SCHEMA_MAJOR_UNSUPPORTED`, `IDENTITY.UNKNOWN`, `HOST.IO_FAILURE`.

Closed shared count guards are root-owned (289 historical + 13 evaluator + previous six). Root adds these three after handoff.

---

## 4. Owned file hashes

| Path under `docs/coop/design-corrections/` | SHA-256 |
|---|---|
| `workflows/schemas/evaluator3/graph-query.schema.json` | `f23f1e22456ed98893221db43ff8824c3261958dd53f3c2adb9c31f038321bc8` |
| `workflows/query-projection-contract.v3.md` | `0b9d5439ae6e5b3e5e48c0641aef0410b3b18bdc7bf8bdf856ac838f77116f89` |
| `workflows/query_projection_model.v3.py` | `42cef0d49fae12e9aadee746029127f0032838a1f7fcedad32d2fad0ae69cd36` |
| `workflows/check-query-projection.v3.py` | `1f27e01b40c12b43bdcffd9308e2a1208fd7c2e2c937c1a661b26cce25d3fe96` |
| `workflows/workflow-projection-contract.v3.md` | `adf3896d3859d14838374db95ff81c2deb0942ecf6096b6ca5ef4959438c450b` |
| `workflows/workflow_projection_model.v3.py` | `50fef99cee4cd6a196d725b35b046ceb5cce6692f9fdb24ebd7d3bcaeb9903a1` |
| `workflows/command-inventory.v3.json` | `2a1f057a7aa6a9584705675f7aa7f5295f177cd2e574d6694581126f951b0e53` |
| `public-detail-registry.v1.json` | `39ec20cd9d1ead85ddbf9a21650765a4e3f45ae421efdd10a759f24fe012b580` |
| `workflows/schemas/common.schema.json` | `a57115f85e91405b0451b3be4a71075f1b3ff902d8094461847ba03959513502` |
| `workflows/schemas/evaluator3/common.schema.json` | `53ec6e19c917cf997491253258711a0d051c6c314a4dcf08d40af273cee03f29` |

Frozen evaluator3 `graph-query:2` unchanged (`9e49c84d…`). Historical `workflows/schemas/graph-query.schema.json` byte-identical to frozen23.

Contract prose is intended-design law; “Root will integrate” handoff comments are not behavioral law.

---

## 5. Controls

| Report | SHA-256 | result |
|---|---|---|
| `original-failures.json` | `4debf56952e0c891094708b00b252b369570f7ff7b66968bf4464212852a7bd4` | 81 checks, **3 FAIL** (`page-complete-last`, `cursor-params-changed`, `produced-cap-last-truncated-bound-no-cursor`) |
| `final-results.json` | `e2f44d0ea7bccc46ad6bd360cf5af96aa5241ec788e1cd0754263abe481421e6` | 81 checks, **0 FAIL** |

Original three failures: `traverse_projected_graph` did not pass decoded cursors into `finish_operation`, so paging restarted at position 0. Fixed; owner QROOT probes were already passing.

Measured owner probes matching root’s retained-probes.v2: unknown endpoint refused; no-closure standing bypass refused; poisoned cache ignored; snapshot index mismatch refused; path `maxVisitedNodes=1` reports `visitedNodes=1`; incomplete incoming disclosed without claiming absence.

---

## 6. Limits (candid)

- `imports@resolved-target` multi-kind TargetAttributionV1 join is table law; the TS semantic fixture still does not mint imports facts, so that join is not an owner-admitted positive.
- Dual-provenance two-row case remains algorithm-only (`traverse_projected_graph`); the owner fixture has one `references` fact.
- Inventory CLI parityFields still say `coverage`; synopsis `run3` only was already done.
- Source pins remain unsealed. Fifteenth launcher child is root’s after this CLI (`--report`/`--out` required, exit 2 if omitted).
- First crash this turn (canonical-set on deficiency `inputRefs`) happened before a JSON report; the preserved original-failures file is the first complete 81-check run.
- Independent review / new blind / application review still required.
