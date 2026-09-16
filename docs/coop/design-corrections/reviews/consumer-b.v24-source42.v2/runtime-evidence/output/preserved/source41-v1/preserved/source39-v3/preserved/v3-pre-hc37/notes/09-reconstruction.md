# Phase 9 — schema, closure, export, replay and graph query (runtime source39.v3)

This note replaces `preserved/source39-v1/notes/09-reconstruction.md` for the current bytes. The source39.v2 self-audit (HC-33..HC-36)
changed the closure pipeline and the exported stores. v2 measurements reused here are listed with their evidence in
`notes/12-v3-completion.md`.

## From-scratch recompute commands (R-FROM-SCRATCH-COMMAND)

Run from `/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v3/output`. Each command reads only the exported stores and the kit, and every Run is closed in its own fresh reference-interpreter process.

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

# retention/reference-class negatives (post code in-process, pre code preserved/pre-hc33 in fresh processes)
/tmp/opensip-architecture-review-env/bin/python -I -B tools/retention_negatives.py

# graph query and analysis-Run terminations over closed Runs
/tmp/opensip-architecture-review-env/bin/python -I -B tools/phase9_graph_query.py
/tmp/opensip-architecture-review-env/bin/python -I -B tools/run_termination_vectors.py
```

`python3 tools/seq.py <label> <script> ...` runs the same invocations through the allowed `python3` prefix and keeps every log under
`logs/`.

## Stage order of `ref/closure.py close_run`

1. **Owner graph admission** (`admit_graph`). The owner records and joins are admitted:
   - native context and universe admission;
   - facts, Coverage and views;
   - enumeration, execution inputs and imports;
   - the source39 laws;
   - the `x-opensip-digest` law over every admitted record.
2. **Independent retained closure** (`ref/retained_graph.py`, HC-33).
   - It starts at `run3` and derives the complete required graph from the owning schemas and registries only. Its sources are:
     - typed-prefix identities per the identity s3 table;
     - every `x-opensip-digest` representation/retention pair of the identity, native and relation bundles;
     - `byDomain`;
     - `domainSets` (`closureJoins`, `nestedIdentities`, `nestedRecords.blobJoins`, `blobJoins`, `snapshotJoins`, `contextAgreementFields`);
     - `closureMembership` and `closureKinds`;
     - the payload registry.
   - It does not import builders, evaluator, closure, digestlaw or native helpers, and never reads the export `objectTable`.
   - Faults are reported by obligation: LEXICAL, SCHEMA, IDENTITY, RETENTION or JOIN.
   - Stages 1 and 2 always both run and are reported separately.
3. **Semantic replay.** It runs only when stages 1 and 2 both admit.
4. **Reachable output-set equality** (HC-34). The walked reachable set of run3, seal3, evidence3, proof3, finding3, finding-key2 and subject3 must equal the recomputed set in both directions.

## Measured on the final bytes

- **27 claimed complete positives.**
  - They are 14 `cmp-*`, 6 Rust, 4 syntax and 3 TypeScript.
  - Each ADMITs through all four stages in a fresh process (`runs/from-scratch.summary.json`, measured in source39.v2 after the last code change).
  - **Re-closed in source39.v3** by `tools/replay_export.py` (`logs/v3-final.0.replay_export.log`): all 27 are `close_run` ADMIT and retained-closure ADMIT with reachable-set equality.
  - For each positive, C(recomputed proof) is byte-equal to the retained proof frame, evidence/seal/Run identities are equal, and every witness is byte-equal (`runs/replay-export.summary.json` `allExportedAndEqual: true`).
  - Required preimages per positive range from 109 (`syntax-data`) to 210 (`cmp-code-detc`).
  - Reachable semantic outputs per positive range from 4 (`cmp-empty`) to 28 (Rust).
- **Designed negative.** `syntax-mixed-falsecomplete` refuses `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE` at owner graph admission.
- **Input mutations** (`runs/replay-all.summary.json`, v2).
  - 62 stores were closed. 29 admit: the 27 positives plus the lawful controls `syntax-code~budget-exhausted` and `~explicit-endpoint-source`.
  - The remaining 33 refuse at owner graph admission with their owner-named causes.
- **Pre/post correction** (`selfcheck/prepost-matrix.json`, v2).
  - Pre code admits all 27 v1 stores and all 27 v2 stores.
  - Post code refuses 26 v1 stores at the retained-closure stage. `cmp-empty` references no subject, so its bytes did not change.
  - Post code admits all 27 v2 stores.
  - Run, proof, evidence and seal identities are unchanged. The only byte delta is added `evaluation-subject` descriptors.

## Four boundaries per claimed positive (R-DISTINGUISH-FOUR-BOUNDARIES)

`runs/<run>.records.json#/boundaries` (v2 admission log, 27 positives, 0 failures) separates:
1. **Schema.** Typed scalars, stock JSON Schema, the `x-opensip-order` walk and the `x-opensip-digest` law.
2. **Helper predicates.** Native, fact, Coverage, enumeration, execution-input, import and source39 predicates.
3. **Closure and replay.** Owner graph admission; the retained-closure stage (`#/boundaries/retainedClosure`); then replay with reachable-set equality.
4. **Host enforcement.** Not claimed (future qualification).

## Replay controls

- **Tamper** (`runs/{syntax-code,ts-pass,rust-mixed}.tamper-outputs.json`, v2).
  - Semantic controls, reminted end to end: parameter value, citation, severity, waiver membership, enumeration, finding removed, witness, verdict, predicate value, and imported address (ts-pass only).
  - Each is admitted by owner admission and by the retained closure, then refused by replay.
  - Identity controls refuse before replay: stale hash, missing input preimage and missing output preimage.
- **Retention/reference-class negatives.** `vectors/retention-negatives.json` (v3); results in `notes/11-v2-self-audit.md`.
- **Three-valued law.** `vectors/replay-three-valued.json`.

## Export for root admission (R-OBJECT-TABLE-FRAMES, R-RETAINED-ARTIFACTS-IN-CLOSURE, R-ROOT-ADMISSION-EXPORT)

- Each `runs/<run>.store.json` carries the complete object table and every retained blob keyed by raw SHA-256.
- That includes the `evaluation-subject` descriptors composition s7 requires, closure tree members, stage-output schema documents and normalization maps.
- The export also holds some unreachable frames: `policy-derivation3`, and in some variants unselected closures or imports. The walker lists them as non-authoritative.
- The exact bytes are exposed for external root admission, whose outcome is unobserved here.

## Graph query (R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR)

`vectors/graph-query.json` (v2, `logs/v2-p89.1.phase9_graph_query.log`): 53 executed vectors over Runs admitted by the complete `close_run`, 0 assertion failures.
- Carrier: CommandEnvelope major 3, `querySurface=graph-query-response`, with `queryResponse`.
- Parity is read at `command-inventory.v3.json` `queryDispatch.parityPaths`.

## Analysis-Run termination

`vectors/run-termination.json`: 28 closed Runs, 9 candidate checks, 30 host-composition cases, 0 failures. It was measured in v2 (`logs/v2-rt.0`) and repeated in v3 (`logs/v3-final.1`).
