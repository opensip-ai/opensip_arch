# Advisory: private composition kernel (50)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded review of two pinned private files. **Not public API. Not atom truth. Not SOURCE48/runtime24 re-acceptance. Not replay, custody, or M2.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-composition-kernel-50-advisory/review`. Copied sources, trial product, frozen48, and live repositories were not edited. Tests used a disposable overlay copy.

## Verdict

**PRIVATE-KERNEL-MATCHES-SELECTED-COMPOSITION; NO-REQUIRED-FINDINGS.**

`compose` with a private `FnMut` scanner matches selected `evaluator_composition_model.v3.py` (**16980** / `cceeb42b…`) on truth, boolean witnesses, descendant flattening, fingerprint correspondence, citations, gating, waivers, budget-before-output-bound order, and proof preimages. `budgets.rs` is byte-equal the accepted SOURCE48 helper. After Plan-budget exhaustion, `CompositionOutput.work` is `BudgetExceeded` (no wrapped exact u64 cost). The eventual public boundary must not expose this scanner callback; a fixed admitted atom scanner remains TODO.

## Pins

| File | Bytes | sha256 |
| --- | ---: | --- |
| `composition.rs` | 35187 | `63c0cd13ea5f1e755bd27f0a5e4c18dad9a3284d9edbe8a28876bda174f5ed62` |
| `budgets.rs` | 8363 | `2d958b434a2437dbf2f1f0daf32e44640f57428c3cc079631aff51309a29a761` |

`budgets.rs` equals SOURCE48 `product/crates/evaluator/src/budgets.rs`. Trial product `composition.rs` equals the pin. Selected atom file `atom_model.v1.py` **97581** / `4477285c…` is not this kernel. `compose` is crate-private.

## Semantics vs selected composition model

- **Truth:** `true`/`false`/`indeterminate` only; `not` arity 1; Kleene `and`/`or`; unknown op `EVALUATOR_BOOLEAN_OPERATION`.
- **Boolean witness:** kind `boolean`, empty fact/import/coverage match lists; `scopeIds`/`inputRefs`/`deficiencies` flattened with `cset`; blocking deficiencies only from indeterminate children when the parent is indeterminate.
- **Addresses:** `{parent}.{i}` matches `predicate_child_addresses` (`p`, `p.0`, …).
- **Descendants:** current node result plus children's descendant lists; finding citations walk that flattening.
- **Correspondence:** file/package skip tokens; duplicate detector projection refuses; empty/missing tokens `projection-unavailable`; incomplete collision population `population-incomplete`; non-unique signature `signature-ambiguous`; otherwise schemaVersion-2 fingerprint with empty `relatedSubjectKeys`.
- **Waivers:** fingerprint locator equality, else exact `{ruleId, subjectPath}`.
- **Gating:** enabled ∧ gate ∧ severity ≥ `gateSeverityAtLeast`; fail iff gating and an unwaived true finding; else indeterminate iff gating and unknown (incomplete enum, required-evidence defs, or blocking indeterminate); else pass. Proof verdict fail ≻ indeterminate (including leftover execution deficiencies) ≻ pass.
- **Budget:** `estimate_evaluation_work` then skip `eval_node` when `BudgetExceeded`, append `work-budget-exhausted`. Output-bound `EVALUATION.OUTPUT_BOUND_EXCEEDED` only when work fits. Exhausted proof keeps `evaluationState: budget-exhausted` and does not claim an exact overflowing cost.
- **Proof:** program blob, evaluation-subject joins, sorted predicateProofs / ruleResults, `cset` findings/waivers/execution deficiencies, proof-bundle identity.

`blocks()` currently hard-codes the sole identity-v3 `nonBlockingDisclosures` member `cross-family-edge-not-owed`. That matches today's registry; a later registry add would need a shared read, not this kernel silently expanding.

## Independent overlay

Disposable copy under this review tree; probes read trial fixtures (including r2 compact rows expanded **after** parse). Did not reopen the original 638 MB expanded `composition-check` raw (exit **101**, 4 MiB parser). Parser/product limits unchanged.

| Check | Result |
| --- | --- |
| helpers (truth/correspondence/waiver) | **2732** |
| predicate builder | **144** |
| finding builder | **596** |
| whole kernel (r2) | **420** (320 values / 100 refused; 30 compact repeats) |
| `budgets.rs` unit tests | **6** |

## requiredFindings

None.

## Limits

Private kernel only. No public `FnMut` truth callback. Fixed atom scanner and admission are not this unit. Local `step`/`max_depth` `Limit` is a development bound, distinct from Plan `BudgetExceeded`. SOURCE48 and runtime24 are already accepted separately and were not re-reviewed. Not replay, custody, or M2. A later freeze needs new bytes after rebase onto accepted runtime24 plus additive layout.
