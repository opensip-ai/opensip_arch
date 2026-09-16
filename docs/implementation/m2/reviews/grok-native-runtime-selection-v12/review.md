# Native-runtime selection v12 — formal implementation-unit review

**Verdict: `NEEDS-CHANGES`**

Root remains lead. Not Claude agreement. Not live install. Frozen source-25 and live/history were not edited.

**subjectManifestSha256** `ab5d4ee8f816c20a1c0e182a6e4a92c05062b0aef88db4b9ca470d2d2da80bae`  
`docs/implementation/m2/native-runtime-selection-v12-subject.json` **9904** bytes, 45 members, 44 successor candidates + successor record, paths sorted unique, 0 member pin mismatches.

## requiredFindings

1. **`contract-parent-composition-not-in-accepted-set`** — `successor.json` lists `docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py` **16980** / `cceeb42bd2fb221235e503e5626784ad45cea009f4c8e4098325c83ad0aecbda` as a contract parent. Independently: that path/hash is **not** in live lock `inputs`, not an inventory **candidate**, and not a contract **record**. `tools/verify_design.py` `contract_successor` (223–226) will raise `contract parent is not an accepted base or selected inventory` at private activation. Same class as runtime-v2’s extra parent.

   The pin **is** the selected compose formula used by frozen budget-25 (dependency-pins + source-25 review). It does not belong on this contract parent list until it is actually in the lock accepted set.

   **Packaging-only fix:** drop that parent; keep v11 successor **record** `4c70c1e3…d62b` / 10922 and inventory v20 **candidate** `321f3da7…f5a7` / 141292. Do not patch frozen-25.

## What otherwise checked (not acceptance)

Two mapped inputs (`budgets.rs` **8363** / `2d958b43…a761`, `lib.rs` **2063** / `bb2286d5…f95a`) compose frozen budget-25 onto **current live 18/25**. Inventory v20 **candidate**: 383 files, 20 packages. **243** non-lock product files match frozen 25; only `design-lock.json` is live 18/25 (`f10fe384…2668` / 55300). Implementation **46924** / `255dcd50…5c3a`; archive **2307061** / `91c46663…c1c7`; export 258/258; materialization 2/2.

Versus live v11: fixture/identity/policy/Cargo/`proofs.rs` unchanged; only `lib.rs` changed + new `budgets.rs`. Live still lacks `budgets.rs`. Frozen-25 inherited lock remains **9/15** (`515f092c…b523`); this unit’s base is live 18/25, not a stale 18/22 label.

Host isolation: **125** sources, **18** archives, **113** tests, help/version 0. Six base preflights exit 0. Provider **not rebuilt**: 25 source+`Cargo.lock` pins revalidated against accepted v10 receipt `3aa90b48…9139` (14 archives, 3 unavailable) and this export/live, 0 mismatches.

Independent: identity-policy 110 passed; 6 budget unit tests ok. Did not re-pipe 2513 comparisons (archived source-25: 72 AST + 2441 formula, 0 mismatch). Stage-meta subject `91cd4c58…9269` is **not** a live contract.

`estimate_evaluation_work` still takes inert census/rule counts; driver must derive; no Run/replay; u128 limit+1; zero-products; disabled rules zero; exhaustion before 100000 output bound; `BudgetExceeded` has no exact cost.

## Limits / not claimed

Not M2 complete, full compose, atom scan, replay, or release. Source-25 is not runtime acceptance. This unit is **not** ACCEPT-DESIGN-UNIT until the parent set is an accepted-lock set. Root assent/private activation of the **current** record would refuse.
