# Phase 9 — schema, closure, export, replay and graph query (runtime source41.v1)

This note replaces my source39.v3 phase-9 note (`preserved/source39-v3/notes/09-reconstruction.md`) for the source41 kit. Every result below was executed in this runtime after the last helper change: logs `s41-fin-*` and `s41-fin2-p45.*`. The corrections are HC-39..HC-45 (`tools/hc_source41.py`).

## From-scratch recompute commands (R-FROM-SCRATCH-COMMAND)

Run from `/private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1/output`. Each command reads only the exported stores and the kit, and every Run is closed in its own fresh reference-interpreter process.

```text
# owner graph admission -> independent retained-closure walk -> semantic replay -> reachable output-set equality, per claimed positive
/tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py      # runs/<run>.replay.fromscratch.json, runs/from-scratch.summary.json

# one Run
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_run.py runs/<run>.store.json runs/<run>.replay.json

# the independent retained-closure walk alone (no owner admission, no replay)
/tmp/opensip-architecture-review-env/bin/python -I -B tools/walk_run.py runs/<run>.store.json <dst.json>

# every store (positives, designed negative, input mutations), without rebuilding
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_all.py --no-build

# admission first (close_run must ADMIT), then export replayed inputs, derived enumeration/ids/witnesses and the complete recomputed proof
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py     # runs/<run>.replay-export.json, runs/replay-export.summary.json

# per-record owning-schema and digest-law log, export sufficiency, four boundaries
/tmp/opensip-architecture-review-env/bin/python -I -B tools/phase9_admission_log.py

# retention/reference-class negatives (corrected code in-process; unchanged ported helpers preserved/pre-s41 in fresh processes)
/tmp/opensip-architecture-review-env/bin/python -I -B tools/retention_negatives.py

# graph query and analysis-Run terminations over closed Runs
/tmp/opensip-architecture-review-env/bin/python -I -B tools/phase9_graph_query.py
/tmp/opensip-architecture-review-env/bin/python -I -B tools/run_termination_vectors.py
```

`python3 tools/seq.py <label> <script> ...` runs the same invocations through the allowed `python3` prefix and keeps every log under `logs/`.

## Stage order of `ref/closure.py close_run`

1. **Owner graph admission** (`admit_graph`). It admits:
   - native context and universe;
   - facts, Coverage and views;
   - enumeration, including the U-0 root decision taken first (HC-39) and U-4b.5 membership enforcement with the tsjs `unitKind` projection;
   - execution inputs, including the s3 view attribution totality (HC-42);
   - imports and the source39 laws;
   - the `x-opensip-digest` law over every admitted record.
2. **Independent retained closure** (`ref/retained_graph.py`). It derives the complete required graph from the owning schemas and registries only. It imports no builder, evaluator, closure, digestlaw or native helper, and never reads the export `objectTable`. Faults are reported by obligation.
3. **Semantic replay.** It runs only when stages 1 and 2 both admit.
4. **Reachable output-set equality.** The walked reachable run3, seal3, evidence3, proof3, finding3, finding-key2 and subject3 set must equal the recomputed set in both directions.

## Measured on the final bytes

- **27 claimed complete positives.**
  - 14 `cmp-*`, 6 Rust, 4 syntax, 3 TypeScript.
  - Each ADMITs through all four stages in a fresh process: 27/27 owner admission, 27/27 retained closure, 27/27 reachable-set equality (`runs/from-scratch.summary.json`, `logs/s41-fin-build.4.from_scratch.log`).
  - Required preimages per positive range from 109 (`syntax-data`) to 210 (`cmp-code-detc`).
  - Reachable semantic outputs per positive range from 4 (`cmp-empty`) to 28 (`rust-mixed`, `rust-mixed-clones-required`, `rust-extra-unit`).
  - The only unreachable retained semantic frame is `policy-derivation3` (advisory A-v2-2).
- **Export replay.** `tools/replay_export.py` (`logs/s41-fin-p4to9.9.replay_export.log`): for all 27, `close_run` ADMIT; C(recomputed proof) byte-equal to the retained proof frame; evidence, seal and Run identities equal; every witness byte-equal (`runs/replay-export.summary.json` `allExportedAndEqual: true`).
- **Designed negative.** `syntax-mixed-falsecomplete` refuses `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE` at owner graph admission.
- **Input mutations** (`runs/replay-all.summary.json`, `logs/s41-fin-mut.0.replay_all.log`).
  - 66 stores closed: 29 admit, 37 refuse.
  - The 29 admitting stores are the 27 positives plus the lawful controls `syntax-code~budget-exhausted` and `~explicit-endpoint-source`.
  - The source41 controls refuse at owner graph admission:
    - `syntax-code~unit-kind-other-family` → `ENUMERATION_MEMBERSHIP_ORDER:unitKind-family:0`;
    - `ts-pass~unit-kind-not-mode-projection` → `ENUMERATION_MEMBERSHIP_ORDER:unitKind:0`;
    - `syntax-code~unit-root-external-sentinel` → `ENUMERATION_MEMBERSHIP_UNIT_ROOT:0:rootPath`;
    - `syntax-code~row-view-omitted` → `EXECUTION_INPUTS_VIEW_TOTALITY:0:0`.
- **Unchanged-helper comparison.** `selfcheck/s41-prepost-matrix.json` (`logs/s41-fin-neg.1.prepost_s41.log`) crosses pre/post code with original/current bytes. Every cell is a fresh-process closure.
  - **Positives.**
    - Pre code admits all 27 original-byte stores and all 27 current-byte stores.
    - Post code admits all 27 current-byte stores. Of the original-byte stores it admits 23 and refuses 4: `syntax-code`, `syntax-data`, `syntax-mixed-disclosed` and `syntax-mixed-omitted` refuse `EXECUTION_INPUTS_VIEW_TOTALITY:1:0`. The unchanged builder had put the one syntax view on the `imports` row, which carries no imports scope (HC-42).
    - Run/proof/evidence/seal identities are unchanged for the other 23 positives. The syntax Runs changed identity because their `ExecutionInputsV1` row views changed.
  - **Designed negative.** Refused under all four combinations.
  - **The four source41 controls.** The corrected code refuses all four. The unchanged code:
    - admitted `syntax-code~unit-kind-other-family` and `ts-pass~unit-kind-not-mode-projection`;
    - refused `~unit-root-external-sentinel` only by generic schema admission (`SCHEMA_REFUSED:unit-membership`), not by the U-0 decision;
    - refused `~row-view-omitted` as `EXECUTION_INPUTS_OUTCOME_DERIVE`, not by attribution totality.
- **Retention/reference-class negatives** (`vectors/retention-negatives.json`, `logs/s41-fin-neg.0.retention_negatives.log`).
  - 32 constructed; `allPass: true`.
  - Each negative is closed by the corrected code in-process and by the unchanged helpers in a fresh process.
  - Census pairs no constructed positive contains, which therefore have no negative: `canonical-record/owner-retained`, `raw-artifact/owner-retained`, `snapshot-path/not-joined`.

## Four boundaries per claimed positive (R-DISTINGUISH-FOUR-BOUNDARIES)

`runs/<run>.records.json#/boundaries` (`logs/s41-fin-p4to9.7.phase9_admission_log.log`: 27 positives, 0 failures) separates:
1. **Schema.** Typed scalars, stock JSON Schema, the `x-opensip-order` walk and the `x-opensip-digest` law.
2. **Helper predicates.** Native, fact, Coverage, enumeration, execution-input, import and source39 predicates.
3. **Closure and replay.** Owner graph admission; the retained-closure stage; then replay with reachable-set equality.
4. **Host enforcement.** Not claimed (future qualification).

## Replay controls

- **Tamper** (`runs/{syntax-code,ts-pass,rust-mixed}.tamper-outputs.json`, `logs/s41-fin-tamper.*`).
  - Semantic controls, reminted end to end: parameter value, citation, severity, waiver membership, enumeration, finding removed, witness, verdict, predicate value, and imported address (ts-pass only; the other two Runs have no imported atom).
  - Each is admitted by owner admission and by the retained closure, then refused by replay.
  - Identity controls refuse before replay: stale hash, missing input preimage and missing output preimage.
- **Retention/reference-class negatives:** `vectors/retention-negatives.json` (`logs/s41-fin-neg.0.retention_negatives.log`).
- **Three-valued law:** `vectors/replay-three-valued.json`.

## Export for root admission (R-OBJECT-TABLE-FRAMES, R-RETAINED-ARTIFACTS-IN-CLOSURE, R-ROOT-ADMISSION-EXPORT)

- Each `runs/<run>.store.json` carries the complete object table and every retained blob keyed by raw SHA-256.
- That includes the `evaluation-subject` descriptors, closure tree members, stage-output schema documents and normalization maps.
- The walker lists unreachable frames as non-authoritative.
- The exact bytes are exposed for external root admission, whose outcome is unobserved here.

## Graph query (R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR)

`vectors/graph-query.json` (`logs/s41-fin-p4to9.6.phase9_graph_query.log`): 53 executed vectors over Runs admitted by the complete `close_run`, 0 assertion failures.
- Carrier: CommandEnvelope major 3, `querySurface=graph-query-response`, with `queryResponse`.
- Parity is read at `command-inventory.v3.json` `queryDispatch.parityPaths`.

## Analysis-Run termination

`vectors/run-termination.json` (`logs/s41-fin-p4to9.8.run_termination_vectors.log`): 28 closed Runs, 9 candidate checks, 30 host-composition cases, 0 failures. That includes the source41 non-object key (HC-41) and the four s7.3 derivation-binding refusals.
