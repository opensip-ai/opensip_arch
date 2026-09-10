I'll start from the root pivot-input-join review and confirm any E1–E3 join defect with an actual counterexample before changing the owned workflow code.The root review is clear: E1–E3 must re-evaluate the same current facts. I’ll inspect Plan/input identity and reproduce a same-snapshot pivot that currently binds with different native coverage.Counterexample confirmed: E1 binds with different `importIds`. Next I’ll join non-substituted semantic inputs for E1–E3 and add the typed detector-manifest binding.v10 is on the same owned workflow3 files. Reports are only under `grok-workflow-projection.v10/`. v9 remains 322. Counts are not acceptance.

**Receipt:** 342/342 at `/tmp/opensip-design-corrections/grok-workflow-projection.v10/workflow-projection-check.json`. Root remints still PASS `open_run_closure` and REFUSE complete semantic close. Foundation was not rewritten for `executionInputsDigest` activation.

### Defect, confirmed then fixed

Root review said E1–E3 were specified as re-evaluation of the **same retained current facts**, but `_bind_pivot_runs` only joined snapshot/policy/ScopeDocument/waivers/detector.

**Counterexample (reproduced before the fix):** same snapshot, same policyDigest (vs baseline), same foundation scope, same nativeContext/config, **different `importIds`**. `compare_admitted` bound E1 as `available` and would have attributed import/coverage change as a policy-axis result.

After the fix that graph is `EVALUATION.FINDING_JOIN_REFUSED`. A legitimate policy remint (`gate` True vs False, same imports/facts) still binds E1.

E1–E3 now join non-substituted semantic inputs: snapshot, resolvedConfig, nativeContext, Plan-selected imports, foundation `plan.scopeDigest`, capability bytes, closures, fact/coverage evidence, inventory rows. View/inventory/execution-input **Plan locators** (`planId`, `executionPlanId`, view2 ids) are stripped. policy/waiver/emission/analysis-spec/rule-program may remint. E0 excludes detector closures so a prior detector is allowed.

### Wider scope

Baseline ScopeDocument `**` vs current `src/**` on the same snapshot: E2 is available. Paths selected only under the wider document stay present at E2 and false at E4 (SCOPE-DELTA), not fabricated empty selection. Absence False is not claimed for a path outside pivot examined extent, current extracted inventory, or the pivot ScopeDocument.

### declared-compatible (concrete, not a vague optional)

Identity hashes `closure.manifestDigest` as **unsigned body bytes** under the security metadata profile, signature envelope excluded. New owned schema: `schemas/evaluator3/detector-manifest.schema.json` (`DetectorManifestV1`) with `compatibleClosures: [{closureId, semanticsMajor}]`.

`compare_admitted` fills `compatibleWith` **only** from that body when `host.closures[id].trust==admitted` (TCB receipt from retained generation / installed signed release / signed closureBundle). Caller maps stay refused. This helper does **not** verify signatures.

**Security-owned remainder:** signature envelope, release catalog, and closureBundle verification. Exact bounded ask: keep admitting the body bytes identity already names; do not add a second workflows-owned signature checker.

### Inventory

`command-inventory.v3.json` is validated against evaluator3 schema 3 (JSON renderer 3 / envelope 3). `command-inventory.v1.json` stays historical major 1.

### Remaining joins

- v1 inventory instance remains schemaMajor 1; it is not inventory:3
- v1/v3 share command names; v3 renderer/envelope majors are the selected profile
- parityFields token `findings` vs FindingSurface / sarif-adapter:2
- `proof.executionInputsDigest`: join compares captured records **minus Plan locators** when both sides have the ref; missing capture is omitted (root still activating); foundation was not patched
- Physical store pointer inventories are not part of semantic execution-inputs identity (main Grok v6); this projector does not join `retainedObjectKeys` / `retainedBlobDigests`

Unknown/known-hit law and pivot-only fingerprints are preserved.

### Owned source hashes (v10)

| Path | SHA-256 |
|---|---|
| `workflow_projection_model.v3.py` | `cd79b3d87b2176eca88b6da00dede5f4480901bd65c9517a4d1b1d0222af69e7` |
| `check-workflow-projection.v3.py` | `0d1f650a3bcf4624c6bb55780d0b056ea09a096cd9131ed22115b548ffe1230c` |
| `workflow-projection-contract.v3.md` | `5c29b47f654271bf593f9fc93d86e719481727a6646acbd7f3f8bdf505aeedf1` |
| `command-inventory.v3.json` | `f3ef932a8c7f878813fbdaa11003166f3994160490c53b65a45f7cc5ec8a4b5d` |
| `command-inventory.v1.json` | `a2ca604bc7176132bbc8f6396a66bfa46cf12d7d3f369bf46aefe82f23149067` |
| `schemas/evaluator3/detector-manifest.schema.json` | `ce54903a8806ae5e3d3dcbb3b1a787719af252a802128826b54597ae1f00bd58` |

Full set: `source-hashes.v10.md`. Companion notes: `declared-compatible-standing.v10.md`, `command-inventory-joins.v10.md`.
