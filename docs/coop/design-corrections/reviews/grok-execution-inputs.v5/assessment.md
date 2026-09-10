I’ll close the remaining cause-pairing holes, add a reusable host-capture helper that both fixtures can use, and write reports only to a new v5 folder.I’ll thread binding carriers through outcome derivation, pair each Coverage’s deficiency with its cause, and add a reusable host-capture helper the checker can share.I'll continue the v5 correction from the leftover checker builder and current source, then finish the helper, mutants, and v5 reports without touching root replay or prior receipts.The helper and v4 receipts are already on disk. Next I’ll read the model, checker, helper, and contract so the remaining v5 edits match the retained source.The leftover inlined `manifest_from_owner` is still in the checker. I’ll read the model, helper remainder, and checker builder next so the replacement stays exact.The model already threads binding and paired coverage records. I’ll read admission, the rest of the checker, and the contract so the leftover builder and mutants can be finished cleanly.I’ll inspect fixture shapes, schema `sourceBodies`, and remaining checker helpers so the shared builder and mutants stay compatible with both graph sources.Identity already lists those domains, so I’ll inspect the registry and native cause rows and keep the helper compatible with that registration.Binding carriers already exist on `UnavailableProgramBindingV1`. I’ll finish the helper (no post-attach rebuild), wire the checker through it, and add the remaining mutants.Next I’ll replace the inlined checker builder with the shared helper and add the v5 mutants.The budget-swap case is passing because the host pair is matching a later unrelated `provider-unavailable` account. I’ll join the outcome scalar to the derived primary pair, not to any source pair.Two join failures are order bugs: helper inventory records weren’t in canonical digest order, and census-incomplete coverage was emitting a null pair as the primary source. I’ll fix both.v5 correction is in the isolated successor only. Enumeration sources were not retouched. v4 receipts are intact. This is not a Run.

## What changed

1. **Binding carrier.** `derive_outcome(..., binding=)` collects same-cell inventories first. Unselected / `universe=null` keep those inventory pairs and use `UnavailableProgramBindingV1.deficiency`/`nativeCause` (`budget-exhausted` or `input-closure-incomplete`), not a generic `provider-unavailable` wipe.
2. **Paired records.** `_summarize_coverage_records` keeps each Coverage `deficiency+nativeCause+inputRef` together. `requiredCellDeficiencies` is canonical-record unique. Outcome scalar equals the derived primary pair (so an inventory `budget-exhausted` cannot be rewritten as a later unrelated `provider-unavailable`).
3. **RC / unsupported.** Unsupported-typed stays the matrix pair. Complete extraction with RC-3 resolution-incomplete stays native; no manufactured carrier. Census-incomplete complete-looking partitions describe missing work at account level without unzipping null pairs.
4. **Helper.** New `execution_inputs_fixture.v3.py` is the shared builder. The checker calls it; the helper does not import the checker. It does not invent required native Coverage.

## Helper call sequence (before seed seal)

```python
from execution_inputs_fixture.v3 import attach_host_capture
attached = attach_host_capture(graph)  # mutates graph; pre-output store only
# attached["digest"] == inputs.executionInputsDigest == proof.executionInputsDigest
# evaluationInputRefs == manifest.selectedRefs + {domain:"execution-inputs", digest}
# do not call attach again after adding proof/seal/finding objects
```

`normalize_graph` accepts both `evaluator_graph_fixture.v3` and `evaluator_semantic_fixture.v3` field names. `selectedRefs` is view + coverage of captured views + inventories + Plan imports + target/incoming/bound candidate sidecars. Policy/schema roots are not added. Retained keys are the pre-output store and **exclude** the execution-inputs blob (no self-hash). Later outputs must not change that digest.

Missing required work is described on `requiredCellDeficiencies` (semantic attach: inventory `file`/`package` still `native-work-incomplete`; helper did not mint Coverage). Root should change fixtures where that work must actually exist.

## Compatibility

Admit/helper treat `execution-inputs` and `candidate-producer-result` as canonical-record blob preimages. They stay valid if those domains are already in the M3 registry. Hashed `selectedRefs` still must **not** include `execution-inputs` (circular). `sourceBodies.byteLength` is snapshot file length; whole-file join is only that opaque provider coordinate, not a body-span compiler.

## Checks

Python 3.12 (`/tmp/opensip-architecture-review-env/bin/python -I -B`). Checker default is stdout; `--receipt` into v1–v4 is refused. 47 cases, `mismatches []`, `oracles []`. Unit checks are not public full-replay qualification.

Reports: `/tmp/opensip-design-corrections/grok-execution-inputs.v5/check-receipt.json` and `hashes.json`.

| File | bytes | sha256 |
|---|---|---|
| `execution-inputs.schema.v1.json` | 25849 | `a7fde8cb6c5db2bf50def20d4227d36c4cb7aa0b67e15de17348a89cd6513fdf` |
| `execution-inputs-contract.v1.md` | 14451 | `9dcc9a21017548e508eaae52b38fef38798943b00da57ed1fb1c650e8c600a2b` |
| `execution_inputs_model.v1.py` | 63078 | `c767553f854de2defca55f9678e79006b5bf4c9a4b0eb149c2ccc7b3c3695860` |
| `check-execution-inputs.v1.py` | 56091 | `4f846890524a5ed76e47990962c6502d0c81300c915e2259603f05267c870df0` |
| `execution_inputs_fixture.v3.py` | 22062 | `1caecc3a6b4e3d7d4f92d9e5ecd504fc26b75bc4c86fe2c71d71c59a0f7206ea` |

Enumeration four-file hashes are unchanged from v4 (`62ff499e…` / `f977cad6…` / `e8a51329…` / `d5477076…`).

## Root remaining

- Require `proof.executionInputsDigest` and `evaluationInputRefs = selectedRefs + execution-inputs ref`.
- Reconstruct already has that join; wire it through public full replay.
- Add inventory/candidate `outputDomains` only on stages that produce them (current fixtures are view-only).
- Where complete required native work is owed, change owner fixtures; do not have the helper invent Coverage.
