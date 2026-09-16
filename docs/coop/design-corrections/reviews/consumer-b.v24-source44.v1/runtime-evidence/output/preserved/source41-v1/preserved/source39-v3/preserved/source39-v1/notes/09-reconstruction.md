# Phase 9 — schema, closure, export, replay and graph-query reconstruction (source39)

## From-scratch recompute command (R-FROM-SCRATCH-COMMAND)

Run these from `/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v1/output`. Each command reads only the exported stores and the kit.

```text
# every claimed complete positive, one fresh reference-interpreter process per Run: identities, graph admission, complete semantic replay
/tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py        # runs/<run>.replay.fromscratch.json + runs/from-scratch.summary.json

# one Run
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_run.py runs/<run>.store.json runs/<run>.replay.json

# every store (positives, designed negative, input mutations), fresh process each, without rebuilding
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_all.py --no-build  # runs/replay-all.summary.json

# admission first, then export replayed inputs, derived enumeration/ids/witnesses and the complete recomputed proof with comparison
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py       # runs/<run>.replay-export.json + runs/replay-export.summary.json

# per-record owning-schema and digest-law log, export sufficiency, provider context, four boundaries, three-valued vector
/tmp/opensip-architecture-review-env/bin/python -I -B tools/phase9_admission_log.py

# graph query over admitted Runs; analysis-Run terminations over closed Runs
/tmp/opensip-architecture-review-env/bin/python -I -B tools/phase9_graph_query.py
/tmp/opensip-architecture-review-env/bin/python -I -B tools/run_termination_vectors.py
```

`python3 tools/seq.py <label> <script> ...` runs the same invocation through the allowed `python3` prefix and retains each execution log under `logs/`.

Measured on the final bytes (`runs/from-scratch.summary.json`):
- **27 claimed complete positives ADMIT** with complete fresh-process replay:
  - 14 `cmp-*`, including the source39 work-budget comparison Run `cmp-budget`;
  - 6 Rust;
  - 4 syntax (`syntax-code`, `syntax-data`, `syntax-mixed-disclosed`, `syntax-mixed-omitted`);
  - 3 TypeScript.
- **Designed negative.** `syntax-mixed-falsecomplete` refuses `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`.
- **Input mutations.** Every mutation store refuses at its owning boundary (`runs/replay-all.summary.json`), except two controls that are lawful by design: `syntax-code~budget-exhausted` and `syntax-code~explicit-endpoint-source`. The latter now admits because the source39 `program-predicate.nodeDigest` names the v2 Predicate.
- **Original failure.** Before the source39 helper corrections, every one of the 26 ported Runs refused at owning-schema admission (`logs/s39-original-closure.0.from_scratch.log`). The original bytes are preserved in `preserved/s39-original/`.

## Four boundaries per claimed positive (R-DISTINGUISH-FOUR-BOUNDARIES)

`runs/<run>.records.json#/boundaries` separates these four:
1. **Schema.** Every record `ref/closure.py` admitted is re-validated against its owning kit schema:
   - typed scalars;
   - stock JSON Schema;
   - the `x-opensip-order` walk;
   - the `x-opensip-digest` law, including source39 annotations (stage-output `registeredBy`, the normalization map record, execution-inputs and incoming-search digests).
2. **Helper predicates.** The native context/universe, fact, Coverage, enumeration, execution-inputs, import and source39 law predicates (`ref/source39.py`). Their faults are empty on every positive.
3. **Closure and replay.** Graph admission across all joins and the digest-law preimage walk, then the independent semantic replay.
4. **Host enforcement.** Not claimed. Real OS/compiler/crypto/SQLite, host authentication and synthetic TCB observations are future qualification.

## Source39 joins executed at retained closure

| Law | Refusal keys | Executed where |
|---|---|---|
| stage output schema registered by the producer closure | `STAGE_OUTPUT_SCHEMA_*` | every positive; `syntax-code~stage-output-schema-relation-doc` |
| normalization specification map in the interpreting closure | `BODY_NORMALIZATION_*` | every clone fact; `syntax-code~clone-level-spec-not-in-grammar`; `vectors/clones-negatives.json` |
| body eligibility (census and scope capability) | `COVERAGE_SOURCE_VARIANT_*`, `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE` | every clones account; `syntax-mixed-falsecomplete` |
| retained UnitMembershipV1 order and row derivation | `ENUMERATION_MEMBERSHIP_ORDER`, `_ROW_DERIVATION` | every positive; `syntax-code~membership-reordered`; `vectors/discovery-membership.json` |
| snapshot rows inside pruned trees are committed reads | `SNAPSHOT_PRUNED_TREE_NOT_A_READ` | `ts-pass` (read row); `ts-pass~pruned-read-*` |
| one parameter per registered row; stage parameters are spec rows | `ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS`, `STAGE_SPEC_HIDDEN_PARAMETER` | every positive; `ts-pass~scope-document-duplicate` |
| account `targetUniverse` null | `EXECUTION_INPUTS_SCHEMA` | every positive |

## Replay (R-REPLAY-*)

- **After admission.** `close_run` replays only when graph admission has no faults, and `tools/replay_export.py` exports nothing unless `close_run` is ADMIT.
- **Complete proof comparison.** `runs/<run>.replay-export.json#/derived` exports the enumeration, predicate proofs with witnesses, findings, waivers, execution deficiencies and verdict. Its `#/comparison` shows, for every positive:
  - C(recomputed proof) is byte-equal to the retained proof;
  - evidence, seal and Run identities are equal.
- **Tamper controls.** `runs/{syntax-code,ts-pass,rust-mixed}.tamper-outputs.json`:
  - Semantic mutations keep record identities and citations valid and are refused by replay (`SEMANTIC_REPLAY_PROOF_MISMATCH` / `IDENTITY_MISMATCH`).
  - Identity mutations are refused at graph admission.
  - The imported-address control exists only where imports exist (ts-pass).
- **Three-valued law.** `vectors/replay-three-valued.json`.

## Export for root admission (R-OBJECT-TABLE-FRAMES, R-RETAINED-ARTIFACTS-IN-CLOSURE, R-ROOT-ADMISSION-EXPORT)

- Each `runs/<run>.store.json` carries the complete object table and every retained blob keyed by digest.
- The retained blobs include closure tree members such as the stage-output schema documents and normalization maps.
- The exact bytes are exposed for external root admission. This review reports only its own independent admission and replay; the root outcome is unobserved.

## Graph query (R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR)

`vectors/graph-query.json` holds 53 executed vectors over admitted Runs, with 0 assertion failures; every execution closes the retained Run with complete replay.
- **Carrier.** The source39 public success carrier is CommandEnvelope major 3 `kind=query` with `querySurface=graph-query-response` and the complete `GraphQueryResponseV1` in `queryResponse`. The JSON rendering is that envelope; the agent rendering adds `agentHints`. Parity is read at `command-inventory.v3.json` `queryDispatch.parityPaths`.
- **Refusals.** A project mismatch refuses `QUERY.PARAMS_MALFORMED`, per the published s7 row.

## Analysis-Run termination (source39 owner)

`vectors/run-termination.json` covers 28 closed Runs (27 positives plus the admitted work-budget mutation):
- the §3 population and §4 cause bridge/order;
- §5 `coverageId`;
- the D9 golden `analysis-budget-exhausted`;
- §6 candidate refusals;
- §7 host composition controls: receipt, attempt and derivation joins, authority, executionId, the detail allowlist and the ephemeral branch.
