# Phase 9 — schema, closure, export, replay and graph query (runtime source42.v1)

This note replaces my source41 phase-9 note (`preserved/source41-v1/notes/09-reconstruction.md`) for the source42 kit. Every result below was executed in this runtime after the source42 helper corrections (`tools/hc_source42.py`, HC-47..HC-50): logs `s42-fin-*` and `s42-fin2-*`.

## From-scratch recompute commands (R-FROM-SCRATCH-COMMAND)

Run from `/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v1/output`. Each command reads only the exported stores and the kit, and every Run is closed in its own fresh reference-interpreter process.

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

# retention/reference-class negatives (corrected code in-process; unchanged ported helpers preserved/pre-s42 in fresh processes)
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
   - enumeration: the U-0 root decision first; U-4b.5 membership enforcement; the source42 program-binding law (`programEntry` null on available default bindings, derived U-1 marker entry against the retained config-graph entry, explicit entry, default-unit cardinality);
   - execution inputs: s3 candidate views from complete receipts only, a `selectedRefs` view on no receipt refused, attribution totality;
   - imports and the registered laws;
   - the `x-opensip-digest` law over every admitted record.
2. **Independent retained closure** (`ref/retained_graph.py`). It derives the complete required graph from the owning schemas and registries only, and never reads the export `objectTable`.
3. **Semantic replay.** It runs only when stages 1 and 2 both admit.
4. **Reachable output-set equality.** The walked reachable run3, seal3, evidence3, proof3, finding3, finding-key2 and subject3 set must equal the recomputed set in both directions.

## Measured on the final bytes

- **27 claimed complete positives** (14 `cmp-*`, 6 Rust, 4 syntax, 3 TypeScript).
  - Each ADMITs through all four stages in a fresh process (`runs/from-scratch.summary.json`, `logs/s42-fin-build.4.from_scratch.log`).
  - Every TS, cmp and Rust positive now carries `programEntry: null` on its `default-unit` bindings; every syntax positive carries a `default-unit` U-9 binding.
- **Export replay.** `logs/s42-fin-p4to9.9.replay_export.log`: `close_run` ADMIT and byte-equal recomputed proofs for all 27 (`runs/replay-export.summary.json`).
- **Designed negative.** `syntax-mixed-falsecomplete` refuses `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE` at owner graph admission.
- **Input mutations** (`runs/replay-all.summary.json`). Final counts are in `blind-review.json`. The two lawful controls `syntax-code~budget-exhausted` and `~explicit-endpoint-source` admit; every other mutation refuses. The source42 controls refuse at owner graph admission:
  - `ts-pass~default-unit-program-entry` and `rust-mixed~default-unit-program-entry` → `ENUMERATION_BINDING_PROGRAM_ENTRY:0:0:default-unit-non-null`;
  - `ts-pass~explicit-entry-not-graph-entry` → `ENUMERATION_BINDING_PROGRAM_ENTRY:0:0:explicit-entry`;
  - `syntax-code~selected-view-not-on-receipt` → `EXECUTION_INPUTS_SELECTED_COVER:view-not-on-receipt:…`;
  - `syntax-code~second-default-unit-binding` → `cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY:0`. The first version (`logs/s42-fin-mut.0.replay_all.log`, v1) refused only `SCHEMA_REFUSED:execution-inputs` from my own capture error (HC-50). The rebuild and re-closure ran in runtime source42.v2 (`logs/s42v2-fin2.0.syntax_runs.log`, `logs/s42v2-fin2.1.replay_all.log`: 71 stores, 29 admit, all others refuse).
- **Graph query:** 53 vectors, 0 failures (`logs/s42-fin-p4to9.6.phase9_graph_query.log`).
- **Per-record admission log:** 27 positives, 0 failures (`logs/s42-fin-p4to9.7.phase9_admission_log.log`).
- **Analysis-Run termination:** 28 closed Runs, 9 candidate checks, 30 host compositions, 0 failures (`logs/s42-fin-p4to9.8.run_termination_vectors.log`).
- **Tamper** (`logs/s42-fin-tamper.*`): every semantic control is admitted by owner admission and the retained closure, then refused by replay; every identity control is refused before replay.
- **Retention/reference-class negatives** (`vectors/retention-negatives.json`, `logs/s42-fin-neg.0.retention_negatives.log`).
  - 32 constructed; `allPass: true`.
  - Each negative is closed by the corrected code in-process and by the unchanged helpers (`preserved/pre-s42`) in a fresh process.
  - Census pairs no constructed positive contains, which therefore have no negative: `canonical-record/owner-retained`, `raw-artifact/owner-retained`, `snapshot-path/not-joined`.
- **Unchanged-vs-corrected matrix** (`selfcheck/s42-prepost-matrix.json`, `logs/s42v2-fin2.5.prepost_s42.log`, runtime source42.v2). Every computed cell is a fresh-process closure over exact bytes.
  - **Positives, original bytes.** These were built by the unchanged helpers and have the same run ids as my source41 exports.
    - The unchanged code admits all 27.
    - The corrected code admits only the 4 syntax positives and refuses the 17 ts-/cmp-* and 6 rust-* positives with `ENUMERATION_BINDING_PROGRAM_ENTRY:…:default-unit-non-null`.
    - The syntax originals carry `explicit-plan-selection` with `programEntry: null`. The contract's §1 cardinality and null rules do not refuse that shape, so their correction is a construction change (default-unit per line 21) rather than a refusal.
  - **Positives, rebuilt bytes.** Both codes admit all 27. No positive keeps its identities, because every enumeration plan changed.
  - **Controls.**
    - The unchanged code admits `ts-pass~default-unit-program-entry`, `ts-pass~explicit-entry-not-graph-entry` and `rust-mixed~default-unit-program-entry`.
    - It refuses `syntax-code~second-default-unit-binding` only as `ENUMERATION_INVENTORY_MISSING_RECORD`, and `syntax-code~selected-view-not-on-receipt` only as `EXECUTION_INPUTS_REF_POINTER`.
    - The corrected code refuses all nine controls on their own laws.

## Four boundaries per claimed positive (R-DISTINGUISH-FOUR-BOUNDARIES)

`runs/<run>.records.json#/boundaries` separates:
1. **Schema.** Typed scalars, stock JSON Schema, the `x-opensip-order` walk and the `x-opensip-digest` law.
2. **Helper predicates.** Native, fact, Coverage, enumeration, execution-input, import and source39 predicates.
3. **Closure and replay.** Owner graph admission, then the retained-closure stage, then replay with reachable-set equality.
4. **Host enforcement.** Not claimed (future qualification).

## Export for root admission (R-OBJECT-TABLE-FRAMES, R-RETAINED-ARTIFACTS-IN-CLOSURE, R-ROOT-ADMISSION-EXPORT)

Each `runs/<run>.store.json` carries the complete object table and every retained blob keyed by raw SHA-256. The walker lists unreachable frames (`policy-derivation3`) as non-authoritative. The exact bytes are exposed for external root admission, whose outcome is unobserved here.
