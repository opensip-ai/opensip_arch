I’ll close the remaining false passes in the same four files: simpler derived accounts, exact receipt totality, real clone member locators, and owner-graph mutants that must fail.I'll resume the four execution-inputs files against the owner graphs: first read the live sources and native clone law, then close M1–M6 with derived checks and real mutants.I'll read the four live files and the owner clone/coverage law next so the derived checks match real graphs, not caller claims.Next I’ll read the native clone-group law, execution-plan output domains, and owner-graph fixture so the derived checks match actual producers.I have the owner-graph and clone-member law. Next I’ll rewrite the four files around derived accounts, exact receipt totality, and real mutants.The model is next: derived accounts from every owner entry, exact receipt totality, and blob-compared clone groups.Same four files only. Root still owns fixture/replay/ProofInputRef. 31/31, mismatches `[]`. Owner-graph file positive **ADMIT** and **not complete**.

## Exact files

| path | bytes | sha256 |
|---|---|---|
| `execution-inputs.schema.v1.json` | 22879 | `2d63376d55a76d0c30176e127002dd1c05c5cfc080d692c760a7521b0e568716` |
| `execution-inputs-contract.v1.md` | 9504 | `b7846aed8f05bb79b025c23527f1dd88d294b82aab40feacabd98b3d4aabae97` |
| `execution_inputs_model.v1.py` | 51482 | `5917d891e37b15bb9ff6b5e9878e2a777f7f7f47066dc1e466aa6f06b61fe15e` |
| `check-execution-inputs.v1.py` | 41065 | `1f302448954ed440dafffb1976a5095d22b16dbb3182a9bf4f0ff2c7886d9de7` |

Receipt: `/tmp/opensip-design-corrections/grok-execution-inputs.v2/check-receipt.json` (v1 pin and v7–v11 refused). Enumeration / input / fixture / replay / fault-observation / public registry untouched (`enumeration_model.v1.py` `043140fd…`, `evaluator_input_model.v3.py` `616c01d2…`).

Not a Run. Host capture remains a TCB observation: equality to this inventory does not prove a non-malicious host.

## Derived law (not more caller claims)

**Accounts** are references + `applicability` only. `accountState` / coverage answer / resolution / exhaustiveness / **all** native causes derive from **every** owner `CoverageResultV3` of **this** cell/program/returned view/enumerator/U/pair. No first-entry summary. A required pair must name every matching returned partition; a complete subset is `EXECUTION_INPUTS_COVERAGE_DERIVE`.

**Outcomes** join that aggregate plus inventories and candidate result. Partial inventory is legitimate known rows (`partial`). Host `complete` over incomplete package work is `EXECUTION_INPUTS_OUTCOME_DERIVE`.

**Receipts** are unique and total over execution-plan stages. `selectedRefs` is exact totality: complete-receipt outputs ∪ coverages of those views ∪ outcome inventories/candidates ∪ Plan `importIds`. Imports are Plan INPUT, not view-stage products. Optional unavailable stages need typed receipt state.

**Groups** always read retained bytes/hash/schema and compare any supplied map. `candidateResultRefs` equals non-null outcome refs, each bound once. Members are native body/symbol IDs (`clone_groups` `bodies[].id`); `/` is not membership.

## Mutants that were false passes

| clause | mutant | now |
|---|---|---|
| M1 | view left in receipt, removed from `viewDigests` **and** `selectedRefs` | `VIEW_TOTALITY` + `SELECTED_COVER` |
| M2 | omit one returned file partition (complete subset) | `COVERAGE_DERIVE` |
| M2 | complete + unknown partitions both named | ADMIT, derived **incomplete** (not first-entry complete) |
| M3 | host `complete` while package account incomplete | `OUTCOME_DERIVE` |
| M3 | selected U, omit stage and views | `OUTCOME_DERIVE` + `STAGE_ORDINAL` + `VIEW_TOTALITY` |
| M3 | fixture `symbol_state=partial` | ADMIT, rows `partial` |
| M4 | extra `candidateResultRefs` | `CANDIDATE_REQUIRED` |
| M4 | groups map ≠ blob | `REF_MISMATCH` |
| M4 | opaque member, no locator | `CANDIDATE_GROUP` |
| M4 | complete `examinedPaths=[]` vs snapshot extent | `CANDIDATE_BIND` |
| M5 | extra views map merge | `REF_MISMATCH` |
| M5 | evaluator missing from closures | `EVALUATOR_CLOSURE` |
| M5 | coverage envelope, payload blob gone | `EVIDENCE_UNAVAILABLE` (not `AttributeError`) |
| M6 | checker-only package complete-empty Coverage | ADMIT, file+package complete, vcs inapplicable |

Owner fixture file Coverage only: ADMIT, derived row `partial`, `native-work-incomplete` on `package`. Oracle asserts **not** complete.

Catch is `(canonical.AdmissionError, identity-model.v3.C.AdmissionError, ValidationError)`. Unsupported-typed cause is the matrix deficiency plus the cause-registry cause for **that** deficiency. All native causes stay on `derivedAccounts[].nativeCauses`; `requiredCellDeficiencies` remains one row per `(cell, program, cause, relation)` for root aggregation.

## Exact root handoff (do not invent stage outputs)

Owner identity `Domain` already has `subject-inventory`, `target-attribution`, `incoming-search` as canonical-record. It does **not** have `candidate-producer-result`. Current fixture stages declare `outputDomains: ["view"]` only. This unit treats inventories / candidate envelopes / target / incoming as **host-derived typed inputs** named by cell outcomes.

Needed root edits when you register ProofInputRef and reconstruct:

1. `identity-schemas.v3.json` `#/$defs/Domain` and `#/$defs/Ref/properties/domain`: add `candidate-producer-result`.
2. `x-opensip-digest-domains.byDomain.candidate-producer-result`: canonical-record → `foundation/execution-inputs.schema.v1.json#/$defs/CandidateProducerResultV1`.
3. Execution-plan / stage-spec `outputDomains`: add `subject-inventory` / `candidate-producer-result` **only on stages that produce them**. Do not add them to `derive-inventory-view`.
4. ProofInputRef / `evaluationInputRefs`: register `candidate-producer-result`. Reconstruct uses this record for view totality and required `kinds=[]`.
5. Clone member custody when `bodies[].id` is not an inventory `nativeSubjectId` or snapshot path: retain a native source-candidate body inventory `{id, path, language, universe}` **or** pass `member_locators`. Snapshot extent is already `objects[enumerationPlan.snapshotId].sourceInventory`. A separate `sourceMap` is needed only when body IDs are neither snapshot paths nor locators.

Architecture here is settled. Remaining work is that registration and reconstruct wiring.
