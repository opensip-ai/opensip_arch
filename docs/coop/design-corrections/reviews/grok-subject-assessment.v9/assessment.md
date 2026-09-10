Root’s v8 review is about ordinary valid cases the 13 checks missed. I’ll read the current model and owner fields, then fix those joins and add the two-symbols-same-file controls.I’ll rewrite the admission model around those ordinary-case bugs, then add two-symbols-same-file controls and a v9 receipt.v8 wrote its receipt into **v7** (`/tmp/opensip-design-corrections/grok-subject-assessment.v7/check-receipt.json`). This work uses **v9 only**. Frozen/live/product files were not touched.

## Owned files

| File | SHA-256 |
|---|---|
| `enumeration-plan.schema.v1.json` | `89669b0b075439b3cff56f798d035a2ac2aa479c50a0710a29724e5db2e23c1a` |
| `subject-inventory.schema.v1.json` | `f510a6bc629ba34a98e45600b30736ddca4f08ce3359fc1f0ad6a516a7615924` |
| `enumeration-contract.v1.md` | `5f44585be339ae33f3379f2ed8d44792f9c3d64ee8bd2e5b0a41c7a8df1ef7d8` |
| `enumeration_model.v1.py` | `fcd9ef8544b33258b18007f807129da1a62f38738cf936b03030f8167c7d49aa` |
| `check-enumeration.v1.py` | `9007bd8f48a0c737acf2cad42e468b79782e9df6338cd7059d6cb80f9f4d311c` |

Receipt: `/tmp/opensip-design-corrections/grok-subject-assessment.v9/check-receipt.json`  
`/tmp/opensip-architecture-review-env/bin/python -I -B check-enumeration.v1.py` → **20 cases, 0 mismatches**.

## Fixes (ordinary valid cases)

1. Path uniqueness is **file/package only**. Native IDs unique per inventory. Projection closure uniqueness **reset per row**. **ADMIT** two symbols on `src/a.ts` with the same detector; **REFUSE** duplicate native ID and duplicate projection-within-row (schema unique `closureId` order is the primary refusal).
2. `evaluation_subject_id` uses **`identity-model.v3.identifier`** (`PREFIX` already has `evaluation-subject`→`subject3`) and checks parity with `C.identity`. The earlier “root follow-up” claim was wrong.
3. File extent remains membership exemption (all first-party scoped paths, including `Cargo.toml` without a Rust cell). **Symbol** extent uses owner `programRootFiles` / syntax code suffixes / rust `sourceUnitOwnership` selected paths. Alternate programs with different `programRootFiles` **ADMIT**. `bindResult` flags refused if present.
4. `excludedPathPrefixes` containing `.` **excludes all** (`ENUMERATION_SCOPE_EXCLUDE_ALL`). `membership_derivation` has explicit required/allowed keys and `mode`; operational mode requires admitted `boundaries`.
5. Null-universe binding cannot mint complete rows. Available binding + unavailable inventory is legitimate. Carrier law applied to bindings and inventories. Context/universe joined via `nativeContextId` + `languageMode`, not fake ADMIT flags.
6. Named packages from **snapshot bytes** (`json` / `tomllib`). Nameless `package.json` / workspace-only Cargo.toml → no package subject, file inventory remains. Parse error → package inventory **unavailable** (`provider-unavailable`, `nativeCause` null). **No NativeCause member names parse failure**; that is a real owner-vocab gap, not an invented cause.
7. Complete file/symbol/package **examined == extent** (canonical-set / `C.canonical` string order).
8. Schema failures catch only `AdmissionError`/`ValidationError`. Locator schema-fail does **not** also emit `MISSING_RECORD`. REFUSE returns empty index/population.
9. Population dedups `(universe,kind,nativeSubjectId)`, keeps all inventory refs, records collisions without last-writer.

API: `admit_enumeration(..., snapshot_inventory=, source_blobs=, retained_inputs=)`. Not a Run; native universe H is not re-hashed here. Root still owns full graph replay.
