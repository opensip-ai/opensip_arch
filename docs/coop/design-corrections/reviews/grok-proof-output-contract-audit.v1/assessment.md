I'll start by reading the design-review constraints, the frozen candidate-subject.v24 kit, and the inputs beside this prompt so the audit stays coauthor-bounded and evidence-based.The design-skill loop is out of scope here; I’ll stay in this session and read the prompt inputs plus the frozen v24 kit.Inputs are in place. Next I’ll read the P7/pilot diagnostics and locate the evaluator3 contracts and schemas in frozen v24.The diagnostics name specific contracts. I’ll locate the published kit and those evaluator3 files in frozen v24.I’ll locate the published kit, source pins, and foundation contracts next so the field-by-field audit has a defined corpus.The discrepancy is between root and P7 derivations. I’ll pin the published kit, then read the owning contracts, schemas, and reference models.I’ll identify the published kit file set, then extract proof-field ownership from contracts, schemas, and reference models.I’ll load the owning contracts and the Proof schema next, then map each field to the reference-model functions that emit it.Contracts are in hand. Next I’ll extract schema annotations and the reference-model functions that actually mint proof fields.I’ll inspect how the reference models fill `inputRefs` and `requiredCellDeficiencies`, then compare that to the schema and prose.I have the field-mapping evidence. Next I’ll write the audit so Codex can reconcile it with the successor: kit uniqueness, competing constructions, and the exact gaps.I’ll write the audit as a field-by-field account, then the JSON companion and the small derivation-table patch.The published normative-only kit does **not** uniquely determine a complete evaluator3 proof from admitted inputs. Several fields that change `C(proof)` are reconstructable in more than one way that all satisfy schema shape. Root reference is not law. P7 complete-`C` is not sufficient when expected fields come from P7’s own convention.

Written only under this session’s output directory:

- `proof-output-contract-audit.md`
- `proof-output-contract-audit.json`
- `proposed-proof-field-derivation.patch.md`

## What is unique in the kit

Proof shape, `evaluationInputRefs` = ExecutionInputs `selectedRefs` plus the ExecutionInputsV1 ref, `executionInputsDigest`, Kleene truth, postorder retention of every node, witness kind/emptiness (and **no** witness `inputRefs`), finding/waiver/verdict aggregation, disabled-rule empty enumeration, required-cell independence from disabled rules, and complete-`C` as the replay comparison rule.

## What is not unique

**1. `predicateProofs[].inputRefs`.** Schema is a unique set with no completeness join. Composition says witnesses bind the complete admitted selection, but the witness schema has no `inputRefs` field. Competing constructions: Run-wide copy of `evaluationInputRefs` (root’s 8 refs; the replay scanner), consulted-set including empty owed inputs, and hits-only (claimed 2 refs). The same reference stamps Run-wide `inputRefs` while copying atom-consulted `scopeIds` / witness `coverageIds`. Boolean union is well-defined only after the atomic set is defined.

**2. `proof.executionDeficiencies` source/cause/inputRefs.** Execution-inputs §4 (inventory digest for required partial inventory) and §5 (Coverage `inputRef`s for native accounts, canonical uniqueness) are class-specific. The hashed ExecutionInputsV1 record has **no** `requiredCellDeficiencies` field. Mapping into the proof lives in excluded reference code, which always uses `source=execution`, prepends the ExecutionInputsV1 ref, and emits `native-work-incomplete` / `unsupported-typed` — spellings **not** in the closed execution cause enum. Claimed `source=native` plus inventory `314855…` vs root `source=execution` plus Coverage + ExecutionInputs is exactly this gap. Forcing `source=execution` while “retaining original typed causes” contradicts the schema whenever the original cause is native-only.

**3. Exact supporting refs on ruleResult/witness deficiencies.** Required `evidence-kind-unavailable` with empty refs is covered. Atom/coverage/correspondence `inputRefs` are reference conventions (often the whole Run selection).

Honest schema-only reconstruction is never unique (`canonical-set` orders whatever you put in). Admitted whole-Run scope is stronger but still leaves the three families above open.

## P7 and earlier grades

Preserved: `FOUR_RUNS_REFUSED`; rust FULL_ADMIT withdrawn; original selected-field `proofCompare` withdrawn; TS `IMPORT_PRODUCER_KIND` first refusal and producing `notReached`; rust-partial first refusal now earlier membership/extent, with the ruleResults mismatch kept as diagnostic.

Not accepted: syntax-data successor FULL_ADMIT “on complete C.” That C matched claimed bytes after P7 derived expected `executionDeficiencies.inputRefs` from clones-fact `inventoryDigests` under §4. Root independently derived different source/refs. Full C of a self-derived expected proof is circular if those fields are not kit-unique.

Pilot symbol census remains an **existing-law** omission (execution-inputs §5 already includes `symbol`). It is not missing design.

## Proposed kit edits (output only)

Small derivation tables/paragraphs in `proposed-proof-field-derivation.patch.md`: consulted-set `predicateProof.inputRefs` (not hits-only, not automatic Run copy); failure-class table for `executionDeficiencies` that keeps original Coverage/inventory/candidate refs and does not prepend ExecutionInputsV1; fix of the semantic-evidence annotation that wrongly calls `evaluationInputRefs` an evaluated subset. No alternate evaluator, no duplicated native extraction, no live source edit.

No acceptance, freeze, or readiness. Codex can reconcile this with the target-identity successor before freezing.
