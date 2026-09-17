# Reconsideration: `public-with-owner-deferred-ok`

**Separate from** preserved original `review.md`. Does not rewrite that critique.  
**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Subject finding:** original required finding 1, `pub(crate) fn inspect_structure_with_owner`.  
**Snapshot (unchanged):** identity `closure.rs` **55265** / `86902be8…b3d3` **604–616**; evaluator `full_walk.rs` **11371** / `ae27c088…2374` **112–114**, **175–177**.

## Decision

**Withdraw as required.** No authority or acceptance path from public `inspect_structure_with_owner` to Run / replay / publication was identified. The proposed `pub(crate)` action is crate-wrong and would not compile. Do not equate `StructuralChecks` diagnostic counts with `inspect_retained_walk` / full closure.

## Why the original action fails

`inspect_structure_with_owner` is a method on `RetainedInputs` in **`opensip-identity`**. `ClosedOwner` and `inspect_retained_walk` live in **`opensip-evaluator`**. Rust `pub(crate)` is crate-private, not workspace-private. Evaluator cannot call a `pub(crate)` identity method. The original action is not an implementable correction of this composition.

## Advisory31, as written

Advisory31 allowed an **optional public** diagnostic walk-with-owner that returns **only** `StructuralChecks`, “not an authority token.” It also said fragment / stage-schema `Ok` belongs **inside** the fixed composition. Those two sentences are satisfied by the snapshot as follows:

- Public `inspect_local_structure` / `inspect_identity_record` / `inspect_current_record` still construct `RejectOwner` (fail-closed, including Retention and StageSchema).
- Public `inspect_retained_walk` accepts **no** caller owner and always constructs private `ClosedOwner`, which is the only path that `Ok`s deferred Retention / StageSchema **and** then runs `inspect_stage_specs` / native / body / remaining owners.
- Public `inspect_structure_with_owner` returns `StructuralChecks` (object/blob/record/foreign **counts**). Comments: it does not establish that callbacks discharged semantic obligations or ran later phases; it must never substitute for the fixed composition.

A caller who implements `resolve -> Ok(())` can obtain counts without later owners. That is a **weaker diagnostic**, not a forged ADMIT. Nothing in this API returns a Run id, replay result, publication ledger, or `RetainedWalkChecks`. No consumer treats `StructuralChecks` as those tokens.

## Authority / acceptance path hunt

| Candidate path | Actual |
| --- | --- |
| `StructuralChecks` used as Run / ADMIT | Struct has no Run id; accessors are counts only (`object_count` / `blob_count` / `record_count`). |
| Host substitutes with-owner for `inspect_retained_walk` | Different return type; later owners never run; cannot mint `RetainedWalkChecks`. Misuse yields less checking, not a sealed graph. |
| No-op owner + later treating counts as closure | Documented as no semantic guarantee. Equating counts to full closure would be a **caller** defect, not an authority minted by this API. |
| `GraphError::OwnerJoin` as success | ClosedOwner maps owner errors to `OwnerJoin` then unwraps the real error. Custom owners returning `OwnerJoin` do not produce `StructuralChecks` success. |
| Default `inspect_*` catching `Unsupported` | Still `RejectOwner`; limits observation `default-remains-unsupported` is `Unsupported("capability derivation")`. |

No path from this public diagnostic to acceptance of a Run, replay, or publication was found. **Withdrawn as required.**

## Remaining limit (not a required snapshot change)

Hosts that want the composition must call `inspect_retained_walk`. `inspect_local_structure` must stay fail-closed. Do not later map `StructuralChecks` onto ADMIT. Visibility of `inspect_structure_with_owner` may stay `pub` as advisory31’s optional diagnostic.

## Not this reconsideration

Findings 2 and 3 (`bodyIdentityJoin` vs `"clones"`; nestedIdentities `join['domainSet']`) remain required **on the immutable snapshot**. Root’s trial adoption of registry-driven dispatch is not this snapshot and is not acceptance. Mutated registry rows used as distinguishing probes are **not** valid inputs to the source-pinned current registry; the existing body owner still only supports current `clones`. Future registry changes remain separately reviewed. Canonical walk-order is wH advisory33, not this note.
