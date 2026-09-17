# Advisory: draft41 retained enumeration reader

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded review of private `read_inputs` only. **Not source/runtime approval. Not full E-join, reconstruct, parser-38, or M2.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-enumeration-reader-41/review`. Copied inputs preserved. No live/frozen/history writes.

Copied pins (`inputs.json` **504** / `6c53f2483253b35c53ff5f4c4d65c1f4610310fe590734fb924efc6e663aee30`): `enumeration_join.rs` **9201** / `0b068f1027b79e9c97a43b67d54573891eac0ea3064cf8f65f8b0313f8241f0a`; `native_universe.rs` **30186** / `080ae8b744e62af108ab4aaae5ddbf4f38a9d4d50ce6ac8122299935635bf2f6`; `enumeration-registry.json` **9215** / `4b46425b17c9ea85187babb0e177cd0cb8296f0389aaf53c9cb26bb293ba25ad`. Selected E39 **50447** / `d32883fd…26992`. Reconstruct `evaluator_input_model.v3.py` **17578** / `021cc9ac…4ba8b`. Module is `pub(crate)`-error / private `JoinInputs` / `#![allow(dead_code)]` / `lib.rs` `mod enumeration_join` without `pub use`.

## Verdict

**The reader is the right next slice: maps from retained bytes, no host tables, no ADMIT/`bindResult`/`membership_derivation`.** Binding-derived universe census is **sufficient for this join** and must **not** be expanded to future Run-walk completeness. Before the join, close **inventory-ref taint** and keep parameter law aligned with `import-registry` without requiring emission here.

Do not implement discovery or M3 in this module.

## What already matches E39 + reconstruct

| Map | Draft | Selected law |
| --- | --- | --- |
| Plan / snapshot | `object` Plan then Snapshot | reconstruct `owner['plan']` / `owner['snapshot']` |
| Analysis spec | `identity_record_shape(…, "analysis-spec")` | Plan.`analysisSpecDigest` identity record |
| Parameters | `import-registry.json` (same include as `import_joins`) match `schemaDigest`↔row `sha256`; `registered_record_shape`; duplicate key `EVALUATOR_PARAMETER_DUPLICATE`; unknown `EVALUATOR_PARAMETER_UNREGISTERED`; require enumeration-plan key | reconstruct `parameter_row_of` + those refusals; emission required only for **full reconstruct**, correctly omitted here |
| Scope | blob `plan.scopeDigest` canonical record | `C.parse(blobs[plan.scopeDigest])` |
| Membership | `current_record_shape` `UnitMembershipV1` | reconstruct parse of `enumeration.membershipDigest`; schema is stronger, still not U-4b (deferred) |
| Snapshot | every `sourceInventory` row: unique path, blob load, `require_length` | reconstruct loads **all** source bytes; E only rehashes **used** manifests — reconstruct-shaped, keep |
| Contexts | Plan.`nativeContextDigests` then `inspect_native_retention` (runs `inspect_native_context`) | E map of descriptors; no ADMIT payload stored |
| Universes | first-seen binding `universe` ≠ null, then `inspect_plan_native`, then retention + `bindResult` refuse | E `ENUMERATION_ADMISSION_PRECONDITION` if `bindResult` present |
| Nested | TS `nested_record(…,"configGraph")`; Rust `nested_frame(…,"sourceUnitOwnership", "native.source-unit-ownership.v1")`; syntax none; other domain `Law` | E `retained_inputs[uni]` those keys only |
| Closures | Plan.`semanticClosures` | enough for E enumerator ∈ plan closures |
| Keys | `digest_hex` bare suffix | reconstruct `nativeUniverses` keys |

API is `read_inputs(inputs, plan_id, inventory_refs, budget)` producing private `JoinInputs`. Local `remaining` steps plus copied `descriptor_work` / owner budgets. Not a public inspect path.

## Binding-derived universe census vs Run walk

**Sufficient for `admit_enumeration`.** E only looks up universes named on `programBindings`. Passing that census into `inspect_plan_native` still enforces context set = Plan.`nativeContextDigests`, language requested, `UNIVERSE_CONTEXT_NOT_SELECTED`, and `inspect_*_universe` with empty refusals.

**Not sufficient for future `inspect_retained_walk`.** Walk must still census universes reached from views/coverage/facts and apply `UNIVERSE_FRAME_UNRETAINED`. Do **not** widen this reader’s census to that set; that would mix walk completeness into the join.

Redundant but acceptable: `inspect_plan_native` already retains+binds those universes; the following `inspect_native_retention(bind=true)` binds again. Not a join blocker. Context retention **before** plan-native uses `bind=true` on **Context** frames, which admits contexts (`inspect_native_context`) and does not bind universes — selection-before-bind holds.

## Parameter selection / schema admission

Using source-bound `import-registry.json` is the right **product** owner (same bytes `import_joins` includes). `registered_record_shape` rehashes payload **and** schema document (existing product pattern; reconstruct Python loads schema from disk). Keep it.

Do **not** require `evaluator-emission-plan` in this join (draft comment is correct). Reconstruct still must require it later.

At-most-one per registry key is implemented. `requiredForEvaluator3` on emission is not enforced here — correct.

Watch drift: identity `PAYLOADS.classes.parameter.rows` has four keys; evaluator `import-registry.json` adds `framework-recognition-plan`. Reconstruct `required_parameters` uses `parameter_row_of` (computed file digest → identity rows) and **refuses unregistered**. A spec citing only the extra import-registry row would pass this reader and fail reconstruct. Do not treat that payload as enumeration input (draft already drops everything except enumeration-plan). Before reconstruct, confirm the two registries’ **required** rows stay aligned; do not expand this reader into identity’s payload class.

## Inventory-ref semantics (must close in the join)

`inventory_refs: &[[u8;32]]` is still a **caller list**. The reader only `canonical_record()`s each digest. Reconstruct instead takes `input_refs` and keeps `domain=='subject-inventory'`. E then `C.validate(INV_SCHEMA)` and joins `(cellOrdinal, programOrdinal, kind)`.

Before full join, do **not** treat `JoinInputs.inventories` as proven subject inventories. The join must:

1. Prove each digest is a retained **subject-inventory** (domain / identity), not an arbitrary canonical blob.
2. Prefer deriving the list from admitted evaluation `input_refs` (reconstruct) rather than leaving a permanent public `inventory_refs` argument.
3. Admit `opensip.product.subject-inventory.1` and bind `parameterDigest` / `planId` as E does.
4. Empty list is allowed in the reader; E law is `ENUMERATION_INVENTORY_MISSING_RECORD` per expected key — keep that in the join, no silent empty ADMIT.

This is the main taint hole. Not discovery/M3.

## Other join deferrals (not reader defects)

- `inspect_enumeration_membership` / U-4b / unit roots not run yet.
- Missing TS `configGraph` is `Ok(None)` then omitted from `retained`; join must still `ENUMERATION_ADMISSION_PRECONDITION` for TS modes (E **825–827**).
- `enumeration-registry.json` kind map unused; belongs in the join, not the reader.
- `membership_derivation` absent — keep it that way.
- Policy/emission binding explicitly out of scope.

## Limits

Not a public API. Not installed. Not full E-join or reconstruct. Not parser-38. Root implements the join next. Copied inputs are the reviewed bytes if the trial file moves.
