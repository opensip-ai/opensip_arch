# Frozen trial review: evaluation-budget-25

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of private `estimate_evaluation_work`. **Not runtime selection. Not v11 re-acceptance. Not full input-driver census, compose, atom scan, Run, or replay.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-evaluation-budget-review-25/review`. Live, frozen, and history not edited. No commits.

Predicate-witness-23 source acceptance remains separate. Runtime-11 was formally reviewed; live last contract is now v11. That install is **not** this source. Live still has **no** `budgets.rs`. Source-25 bytes are unchanged by that activation.

Private inherited `product/design-lock.json` is `515f092c…b523` / 36241 with **9 inventory / 15 contract** successors — **not** 18/22. The old 23 README/reviewer label is preserved in the separate 23 correction; this trial does not relabel those frozen files.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/evaluation-budget-25/subject.json` | 47986 | `d28722ba9e90a3e23af1cf413f62d6dea7b9eb4fb522ee860ab35c6d52f2cd25` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 2296102 | `d6b4e322666240965d1c1492f131b297268d08390f9f37b0a0879e098e13f0a7` |
| adjacent `budget-result.json` | 290 | `dd9f64f4cac93cdb92813cbe00fc12f0f947dbed78328438b1cba99d4972e688` |
| export | `/tmp/opensip-implementation/m2-evaluation-budget-subject-25` | **266/266** members; tar 266; 0 extra; 0 missing |

266 `files[].path` values are unique and string-sorted.

Dependency pins hash-match: predicate-witness-23 `62771186…cd25`; runtime-v10 unit `2160836f…9346`; selected composition `evaluator_composition_model.v3.py` `cceeb42b…cbda` / 16980.

Live lock independently **18 inventory / 25 contract** (`f10fe384…2668` / 55300). Last inventory candidate remains v20; last contract is runtime **v11**. Live `proofs.rs` exists; live `lib.rs` has no `estimate_evaluation_work`.

## Source delta vs frozen 23

**242** prior product files byte-identical, including identity, identity-policy, `Cargo.lock`, host fixture, `proofs.rs`, and prior runtime bodies. External TCB unchanged.

Changed: `lib.rs` export. **New:** planned `crates/evaluator/src/budgets.rs` (**8363** / `2d958b434a2437dbf2f1f0daf32e44640f57428c3cc079631aff51309a29a761`), already named in inventory v20.

## Law vs selected compose cost (lines 106–115)

`estimate_evaluation_work` takes inert `EvaluationCensus` and `RuleWork` slices plus a u64 limit. It does not take a Run id, retained graph, or claimed outputs. The full input driver must derive the counts; this helper cannot mint Run, proof, or replay.

Selected formula: inventory rows + locators + sum over **enabled** rules of `selected * (nodes + atoms * (facts + observations + coverages))`. Disabled rules contribute zero work and zero output bounds. Intermediates use u128 saturating ops capped at **limit+1** so comparison stays exact; U64MAX+1 cannot wrap into a small `WithinBudget` cost. Zero factors stay zero even when the other factor is capped.

Failure order matches compose: if cost > min(limit, 2^64−1) → `BudgetExceeded` **with no exact cost field** (not truncate permission). Only if work fits are predicate/finding bounds checked against 100000 → `OutputBoundExceeded`. `WithinBudget` reports exact u64 work and bounds.

Synthetic arithmetic may exceed schema-admitted policy-tree sizes; schema/program owners remain prerequisites. AST cost projection uses sized dummy populations, not full compose/enumeration/atom scan.

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- Frozen actual vs expected: **2513/2513**, **0 mismatch** (570 within / 1878 budget-exceeded / 65 output-bound-exceeded). **72** `actual-AST-*` rows; **2441** unlimited-integer formula/extreme/random.
- Independent unlimited-integer formula vs frozen expected: **0 mismatch**. Independent extract of compose cost AST 106–115 vs that formula on all 72 AST grids: **0 mismatch**.
- Independent probes: exact 138/137 boundary; zero population / zero atoms; disabled inventory exhaust; U64 overflow of scan and inventory; exhaustion **before** 100000 bound; bound refusal when cost fits; U64MAX inclusive; BudgetExceeded has no `work`.
- `cargo test --locked --offline -p opensip-evaluator budgets --lib`: **6** new unit regressions ok. Identity policy independently passed: `sourceFilesVerified: 110`. Frozen workspace sums to **113**. Independent `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` Finished.

Did not re-exec Unicode-15 or 07–12 corpora. Did not treat live v11 as this source.

## requiredFindings

None.

## Limits (not required findings)

- Supplied census/rule counts are not independently derived here and are not admission tokens.
- This helper does not run compose, atom scan, enumeration, or emit exhausted deficiencies/state; `BudgetExceeded` only refuses a successful truncated Run.
- Synthetic counts may exceed admitted policy-tree bounds.
- Live 18/25 runtime v11 does not install these `budgets.rs` bytes.
- Inherited private lock remains 9/15; it is not a selected 18/24 or 18/25 runtime base.

## Verdict

No required findings. Private `estimate_evaluation_work` matches selected compose cost arithmetic, preserves exhaustion-before-output-bound and non-wrapping U64 comparison, and does not mint a Run. Not a live/runtime selection.
