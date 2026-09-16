# Phase 9 — schema, closure, export, replay and graph-query reconstruction

## From-scratch recompute command (R-FROM-SCRATCH-COMMAND)

Run from `/tmp/opensip-design-corrections/consumer-b.v24/output`. Each command reads only the exported stores and the kit.

```text
# every claimed complete positive, one fresh reference-interpreter process per Run: recompute identities, graph admission, semantic replay
/tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py        # writes runs/<run>.replay.fromscratch.json + runs/from-scratch.summary.json

# one Run
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_run.py runs/<run>.store.json runs/<run>.replay.json

# admission first, then export the replayed inputs, derived enumeration/ids/witnesses and the complete recomputed proof with comparison
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py       # writes runs/<run>.replay-export.json + runs/replay-export.summary.json

# per-record owning-schema + digest-law log, export sufficiency, provider context, four boundaries, three-valued vector
/tmp/opensip-architecture-review-env/bin/python -I -B tools/phase9_admission_log.py

# graph query reconstruction over admitted Runs
/tmp/opensip-architecture-review-env/bin/python -I -B tools/phase9_graph_query.py
```

(`python3 tools/runref.py <script>` is the same invocation through the allowed `python3` prefix.)

Measured on the final bytes (`runs/from-scratch.summary.json`):
- 26 claimed positives were ADMITTED with complete replay: 13 `cmp-*`, 6 Rust, 4 syntax and 3 TypeScript Runs.
- The one designed negative in that directory, `syntax-mixed-falsecomplete`, still refuses with `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`.
- Every result matches the original replay.
- The first summary labelled that negative as a failed positive (`runs/from-scratch.summary.attempt1.json`). The replay itself was correct; HC-12 corrected the tool's classification.

## Four boundaries per claimed positive (R-DISTINGUISH-FOUR-BOUNDARIES)

`runs/<run>.records.json#/boundaries` separates these four:

1. **Schema.** Every record `ref/closure.py` admitted is re-validated against its owning kit schema. This covers typed scalars, stock JSON Schema and the `x-opensip-order` walk, plus the `x-opensip-digest` law. All 26 Runs have 0 refused records; per-Run record counts are 51–122.
2. **Helper predicates.** The native context/universe, facts, Coverage, enumeration, execution-inputs and import re-derivations that run inside graph admission. Their faults are empty on every positive. These predicates are not closure by themselves.
3. **Closure and replay.** Graph admission across all joins and the digest-law preimage walk, then the independent semantic replay. Replay compares the recomputed proof bytes and proof/evidence/seal/run identities with the retained claim.
4. **Host enforcement.** Not claimed anywhere. Real OS, compiler, crypto and SQLite behaviour, host authentication and synthetic TCB observations are future qualification.

## Replay (R-REPLAY-*)

- **After admission.** `close_run` performs replay only when graph admission has no faults. `tools/replay_export.py` also exports nothing unless `close_run` is ADMIT.
- **Enumeration, ids, predicates, witnesses, verdict.** `runs/<run>.replay-export.json#/derived` holds:
  - per-rule `enumeration` (selected subject ids, state, unresolved ids);
  - every predicate proof with its witness: `matchingFactIds`, `coverageIds`, `childPredicateIds`, import rows, uncertain ids, deficiencies and value;
  - findings with fingerprints and evidenceRefs;
  - waived ids, execution deficiencies, evaluation state and verdict.
- **Complete proof comparison.** `#/proof` is the complete recomputed proof. `#/comparison` shows, for all 26 Runs, that `proofBytesEqual` holds, evidence, seal and run ids are equal, and every witness is byte-equal to the retained witness.
- **No caller truth.** The evaluator's inputs are the admitted graph only: plan, policy, emission, enumeration plan, inventories, selected views, scopes, Coverage, facts/payloads, imports and execution inputs. There is no expected-output input anywhere.
- **Tamper controls.** `runs/{syntax-code,ts-pass,rust-mixed}.tamper-outputs.json`:
  - Record identities and citation membership stay valid while the logical result changes. Every semantic control (parameter value, citation, severity, waiver membership, enumeration, finding removed, witness, verdict, predicate value) is refused by replay with `SEMANTIC_REPLAY_PROOF_MISMATCH` / `IDENTITY_MISMATCH`.
  - Identity controls are refused earlier, at graph admission.
  - The imported-address control only exists where imports exist (ts-pass).
- **Three-valued law.** `vectors/replay-three-valued.json` is an explanatory re-evaluation over ts-pass inputs:
  - an atom on `references@resolved-binding`, which has no retained Coverage and no match, is `indeterminate` for every subject (witness deficiency `native/missing-relation-coverage`), never vacuous `false`;
  - `and(calls, references)` yields `false` where calls is false and `indeterminate` otherwise;
  - `or(calls, references)` yields `true` where calls is true.

## Export for root admission (R-OBJECT-TABLE-FRAMES, R-RETAINED-ARTIFACTS-IN-CLOSURE, R-ROOT-ADMISSION-EXPORT)

- Each `runs/<run>.store.json` carries the complete object table (id, domain, frame SHA-256, frame bytes) and every retained blob keyed by digest.
- `records.json#/export` shows no missing frames and that every blob rehashes.
- Retained referenced artifacts are also covered by the digest law: every annotated preimage the retention law requires must be present in the export, and graph admission refuses otherwise.
- These exact bytes are exposed for external root admission. This review reports only its own independent admission and replay; the root outcome is unobserved.

## Graph query (R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR)

`vectors/graph-query.json` holds 53 executed vectors: 27 valid, 25 invalid, 1 explanatory. Every execution closes the retained Run with complete replay, and nothing is minted. The script exits nonzero on any failed expectation, and the final run had 0 failures. Coverage:

- **Selection.**
  - `runId`, a `snapshotId` with a unique trusted observation, and trusted `latest` resolve to `resolvedView {runId}`.
  - A missing, stale or unequal observation refuses `IDENTITY.UNKNOWN` / `QUERY.VIEW_UNKNOWN`.
  - Two Runs observed for one snapshot (cmp-base, cmp-scope) refuse `QUERY.VIEW_AMBIGUOUS`.
  - An explicit fact-view not on the Run refuses `QUERY.FACT_VIEW_UNAVAILABLE`.
- **Endpoints and units.**
  - Neighbor order follows the UTF-8 endpoint tuple, then fact2 id.
  - One row per fact2; a control-flow self-loop appears once.
  - An isolated inventory vertex and a package endpoint are admitted with zero rows.
  - An external calls target (`npm:left-pad@1.3.0#pad`) is a lawful vertex.
  - For `imports@resolved-target` (multi-kind), the target kind comes from exact-id occupancy (`ts:src/util.ts` is a symbol). The two npm targets have no occupancy and are omitted as `unprojectable-fact`.
  - Another universe, or an absent native id, refuses `QUERY.ENDPOINT_UNKNOWN`.
- **Path and reach.**
  - Path selects the shortest direct hop; zero-hop is admitted; no path is a complete empty result; `both` direction and the semantic maxDepth law are exercised.
  - Reach excludes the start by default; `includeStart` adds a depth-0 row with no via; incoming reach at depth 2 is exercised.
- **Bounds vs pages.**
  - Page size 1 gives `truncated-page` with an exact count.
  - A visited cap of 1 on a one-edge path gives `truncated-bound` / `lower-bound`. Under `completeness=required` that becomes indeterminate `QUERY.COMPLETENESS_UNMET` with the runId, exit 3.
  - Zero-hop exactly at the cap is complete.
  - The items cap and visited cap on reach yield canonical prefixes.
- **Continuation.**
  - Page 1 was taken under `latest` = cmp-base. Page 2, taken after the latest observation moved to cmp-code, still reads cmp-base when the view is `{runId}`; the two pages concatenate to the single-page result.
  - Presence or absence of a caller cache does not change the response.
  - A continuation under `latest`, on the newer Run, or with changed params refuses `QUERY.CURSOR_MISMATCH`.
- **Evidence vs stored edges.**
  - A relation with no selected view gives zero rows and complete traversal plus `native-evidence-unavailable`.
  - `ts-clones-required` gives complete traversal with its execution deficiencies cited exactly.
- **Failures.**
  - Schema major 2, an extra param, a LogicalPath subject, a package endpoint without a manifest path, and a manifest path on a symbol each produce a typed failure envelope.
  - A non-projectable rung and the clones relation refuse `QUERY.RELATION_UNSUPPORTED`.
  - Availability `purged`/`expired`/`corrupt`/`unavailable`, and missing or corrupt retained bytes, route to operational-failed / `HOST.IO_FAILURE` / host-io.
  - A malformed projectId is omitted from the envelope. A malformed host requestId is a reference-call precondition, not a public refusal.
- **Renderers and summary joins.**
  - Human, JSON and agent renderings preserve all six parity fields.
  - Compact `QueryResult` joins hold: page items, truncated, cursor, `completenessMet` equals `countBasis=exact`, and termination and project equality.
  - Negatives are refused: completeness claimed on a lower bound, items counting the total, a dropped cursor, and a renderer dropping termination-class.
- **Measured carrier gap.** CommandEnvelope major 3 (`additionalProperties: false`) has no field for the complete `GraphQueryResponseV1`. Adding one is refused. Yet the query command's parity field `query-response` (command-inventory v3, workflows lines 1055-1060) must be that complete response, and the JSON envelope is the parity reference. The JSON and agent renderings here therefore carry `{envelope, queryResponse}` as a cb24 carrier. Adjudicated in phase 10.
