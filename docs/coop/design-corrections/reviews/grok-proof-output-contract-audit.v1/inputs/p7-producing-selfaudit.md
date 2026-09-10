# Producing-law self-audit of COMPLETE49 four-Run grades

This is a follow-through on the same kit-only origin (`grok-kit-only-other-runs-full-review.v1`), not a new fresh review. Original COMPLETE49 files are frozen under `history/`. The original checker is frozen under `checker-original/` with pathdiff in `history/checker-pathdiff.txt`. Consumer inputs were not reminted.

**Successor scoped verdict remains `FOUR_RUNS_REFUSED`.** Rust `FOUR_RUN_FULL_ADMIT` is **withdrawn**. Syntax-data is re-admitted only on successor complete C-equality, not on the original selected-field comparison. Original findings are not waived.

## What COMPLETE49 actually compared

Original `checker-original/replay.py:_proof_compare` compared a projection: verdict, evaluationState, predicate operation/value/witnessDigest/scopeIds, rule outcome and selectedSubjectIds, sorted `(cause, nativeCause)` pairs, findingIds. It copied claimed `evaluationInputRefs`, `executionPlanId`, `evaluatorClosure`, `ruleProgramDigest`, and `executionInputsDigest` into the computed proof.

Composition §7 requires **C of the complete recomputed proof** and reminted evidence/seal/Run identities. Counts, selected fields, verdict, or a witnessDigest are not complete-bundle comparison. Original rust and syntax-data `proofCompare: []` therefore **exceeded actual coverage**.

Original enumeration compared inventory file rows to **claimed** `binding.extents`. That lets a hashed KindExtentV1 certify itself. Enumeration §5 / `x-opensip-file-membership-extent-law.fileKind` requires independently deriving remaining first-party snapshot paths. Original never joined `membershipDigest = C(UnitMembershipV1)` and never required membership rows to cover snapshot paths (§8).

## Successor execution (not paragraph counts)

Read entire: `enumeration-contract.v1.md`, `execution-inputs-contract.v1.md`, `atom-evaluation-contract.v1.md`, `evaluator-composition-contract.v3.md`, plus incorporated schemas/annotations. Row-level execution is `inventory/producing-law-execution-rows.json` and `inventory/producing-law-paragraph-inventory.json`.

Independently executed before semantic comparison:

- `C(UnitMembershipV1)` vs `enumerationPlan.membershipDigest`
- membership row paths vs snapshot Blob paths
- file extent from snapshot minus excludeAlways, vs claimed inventory cell extents
- package subjects by parsing retained `Cargo.toml` / `package.json` (workspace-only root is not a named package)
- stage receipt ordinals; `hostDerivedRefs` C-set vs selected blob-domain refs
- `selectedRefs` reconstructed from complete receipts ∪ view coverage ∪ cell inventories ∪ Plan imports
- outcome `state` derived from inventories and supported-available Coverage completeness
- native account `coverageIds` re-scanned from view Coverage payloads
- complete `encode_c(proof)` and remint of proof3/evidence3/seal3/run3

Policy-specific bound: admitted RulePrograms are `file-present` / `none` / `file` / `enumerated`. Atom incoming/import/sufficiency_v2 resolved-rung branches are inapplicable because those atoms are not in the admitted programs. That is not an invented generic-analyzer hole.

## Grades after producing-law execution

| Export | Original | Successor first refusal | producing | fullsemantic | proof C |
|---|---|---|---|---|---|
| TypeScript | REFUSED `IMPORT_PRODUCER_KIND` | **preserved** same | notReached | DIAGNOSTIC | true (diagnostic) |
| Rust complete | **FULL_ADMIT withdrawn** | `ENUMERATION_MEMBERSHIP_SNAPSHOT_COVER` missing `#/Cargo.toml`, `#/a/Cargo.toml`, `Cargo.lock` | REFUSED | DIAGNOSTIC | **true** (diagnostic only) |
| Syntax data | FULL_ADMIT basis withdrawn | none on successor C-path | PASS | PASS | **true**, reminted `run3:ab1d6fc4…` equals retained |
| Rust partial | REFUSED rule outcome | **earlier** membership/extent cover (same missing paths) | REFUSED | DIAGNOSTIC | false (`ruleResults` C) |

Rust diagnostic proof C-equality with reminted run ID matching the retained `run3:9032d3b0…` does **not** restore FULL_ADMIT. Composition §7: input admission precedes replay; hashes of claimed inventories/extents do not establish owner admission. The claimed inventory file extent is only `#/a/src/lib.rs` while independently remaining snapshot paths are four files.

Syntax-data original `proofCompare: []` would have accepted empty `executionDeficiencies.inputRefs`. Claimed record cites inventory `3148550880c15c379d0d41ab02b7c6b76da46068e2713ede1f248fa81fe7c850`. Successor derives those refs from the required clones-fact cell `inventoryDigests` (execution-inputs §4), then complete C(proof) and enclosing IDs match. The original *method* is withdrawn; the graph is re-admitted on the successor method.

Rust-partial original `MUST-PARTIAL-RULE-ENUMERATION` is preserved as diagnostic: claimed `ruleResults.enumeration` lists only the complete inventory-cell file inventory and outcome `pass`; independent file-kind population still includes the clones-fact partial inventory. First refusal is now the earlier membership/extent producing join.

## Not claimed

No whole-134-consumer ACCEPT. No product qualification or implementation authorization. No query execution. `R-RUN-SYNTAX-CODE` is still not in these four exports.
