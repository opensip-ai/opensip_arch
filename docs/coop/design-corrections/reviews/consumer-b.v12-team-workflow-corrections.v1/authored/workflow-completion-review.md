# Workflow completion (role-change authoring)

**Verdict: `WORKFLOWS_READY_FOR_INDEPENDENT_RECHECK`**

Explicit role change: the former workflow validator authored these bounded corrections. Prior reviewer outputs remain historical reviews of **old** bytes. They are **not** independent acceptance of these new bytes. A later peer/root still checks this work. Not whole-consumer ACCEPT. Not a root outcome. Not product/host implementation. Frozen Run stores were not rewritten.

## Custody

| Object | SHA-256 | Result |
|---|---|---|
| kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | 80/80 PASS |
| parent | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | unchanged |
| continuation-inputs.json | see `workflow-completion-review.json#/inputHashes` | recorded |

Five copied Run stores remain byte-identical (`frozen-run-hashes.json`: syntax-code `2e74a6b2…`, ts `885b8e45…`, rust `67dc12f8…`, syntax-data `1d07e4c8…`, rust-partial `b6c2b240…`).

Original failed workflow examples preserved under `preserved-failures/workflow-review-v2-refused-original/` before replacement. Historical foundation vectors were not overwritten with prose. Mechanical KIT/OUT rewrites: `path-correction-record.v3.json`.

## From-scratch isolated command

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v1/output/scripts/workflow_correct.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v1/output/scripts/workflow_correct_test.py
```

Tests exit **nonzero** on a failed assertion or schema/setup error. Last run: exit 0. Expected values are recomputed from kit laws (`helper/workflow_laws.py`), not from saved consumer helper results.

## What was corrected (all 15 refusals + identity-recipe mismatches)

Executed functions consume input records. Literal unconditional throws are not admission.

| ID | What changed |
|---|---|
| `R-REPAIR-APPLY-KEY` | Key is raw SHA-256 of `C({operation, projectId, repairPlanId, baseSnapshotId})`, not an arbitrary record. Unequal to `H("workflow.mutation-intent", MutationReplayScopeV1)`. |
| `R-REPAIR-DESCRIPTOR` | `repairPlanId = repairplan2:` + `H("workflow.repair-plan", descriptor)`. |
| `R-CMP-*` / `R-BASELINE-AUDIT` / `R-E0-VS-E1-E3` | `comparison2:`/`baseline2:` from selected H recipes. Counts match entries. Presence/classification/`liveInCurrent` consistent. |
| `R-SCOPE-POLICY-ONLY-COMPARISON` | Two retained ScopeDocumentV1 preimages; unequal `scopeDigest`; policy unchanged. |
| `R-PIVOT-ONLY-FINGERPRINTS` | Fingerprint in E0 only (`B=false`, `E4=false`); counts follow classification. |
| `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` | Two committed `SourceUnitOwnershipV1` maps derive edition 2018 independently; same L0. A 2021 map moves identity. Ownership never enters BLV. |
| `R-RUN-UNSUPPORTED-GRAMMAR` | `admit_syntax_suffix` against the bundled suffix table. `.unknownlang` refuses `unsupported-file`. |
| `R-HIDDEN-MISMATCH-PER-LANGUAGE` | TS path vs inventory; Rust edition-map crate vs admitted roots. |
| `R-CLONES-NEGATIVE-VECTORS` | `admit_clones_fact` on anchors, level-spec, languageId vs provider. |
| `R-REPAIR-AUTHORITY-PER-TARGET` | `repair_target_join` against matched fingerprints. |
| `R-MIN-RESOLUTION-THREE-LEVELS` | Three levels × qualifying/insufficient. Type qualifying present. Resolved/type complete-absence is `false`. |
| `R-MIN-RESOLUTION-REPAIR-EVIDENCE` | RepairPlanV1 `evidenceRequirements` bound to those cases, not prose. |
| `R-MULTI-UNIT-MISSING-CAPS` | Zero-config synthesized graphs over two workspace roots; advertised vs installed; candidate-only cells. |
| `R-CANDIDATE-ONLY-CLONES` | `kinds=[]`, `extents=[]`, `candidateSourcePaths` present. |
| `R-HOST-CAPTURED-VS-CANDIDATE` | Labeled synthetic hostCapture/selectedRefs vs candidateResultRefs. |
| `R-CHAIN-ZERO-CONFIG-TO-RECEIPT` | Measured hashes of executed artifacts, not a checklist sentence. Original checklist preserved. |
| `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` | Projectable `calls@resolved-callee`. Nontrivial path/reach. Continuation cursor `q3.<runId-64hex>.<selectionHash64>.<position>`. `coverageIds` from selected views. `file@enumerated` refuses `QUERY.RELATION_UNSUPPORTED` (not a success body). human/json/agent parity of the same fields. `underlyingRunAdmissionUnverified` retained. |

Envelopes, config graphs, JS body through TS, three-valued exists, invocation disclosure, D9 map, and cited standing documents were re-executed in this pass.

Genuinely absent/contradictory laws: **none**.

## 134 original IDs

Full rows: `workflow-completion-review.json#/originalRequirementIds`. Copied historical claims are **not** accepted by copy.

| reviewedScope | Count |
|---|---:|
| in-scope workflow correction (executed) | 48 |
| standing of consumer continuation (not re-executed) | 24 |
| historical vector notReached | 23 |
| out-of-scope frozen Run | 24 |
| out-of-scope frozen Run replay | 12 |
| futureQualification | 3 |
| **total** | **134** |

## Limitations (this bounded task)

- Frozen TS/Rust/syntax-data/partial Run admission and other-Run replay stay out of scope (Main B12 owns Run-graph corrections elsewhere).
- Query examples do not claim `close_run`.
- Synthetic TCB observations are labeled.
- This file is an authoring completion record, not independent acceptance.
