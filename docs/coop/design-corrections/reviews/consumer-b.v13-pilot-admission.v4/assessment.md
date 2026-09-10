I'll start from the full checkpoint prompt, copy the completed v3 output into v4, then fix exact condition matching before prose derivation.I'll copy the completed v3 output into v4 and rebase helper paths so this checkpoint starts from that exact graph.I'll add document identity to traces, switch matching to an exact four-tuple, and keep reading the remaining contracts.Exact matching exposed real gaps: v2 tables were bound onto v3 records, and some required fields were generic `payload` buckets. I’ll correct applicability and emit the actual compared fields.**PILOT-CHECKPOINT-COMPLETED.** `reconstructionAccepted` is false. `rootAdmission` is unobserved. Whole-task acceptance remains prohibited.

## A. Exact matching

The v3 matcher used `(condition, instance, field)` then fell back to `(condition, instance)`, ignored document identity, and exited 0 even when missing was nonempty. That zero is not required-occurrences minus executed-occurrences.

Preserved:

- Weak v3 result: `inventory/v3-weak-matching-coverage-difference.json` (claimed missing 0)
- First exact run: `inventory/v4-exact-matching-first.json` (**124 OPEN**)

After reconciling real field/document differences (v2 tables not aliased onto v3 records; required `field` is the compared field, not a generic `payload` bucket):

**1245 required, 2530 traces, 0 missing.** The process now exits 1 if any 4-tuple is missing.

Negatives (`inventory/exact-match-negatives.json`): omitting one field comparison leaves OPEN; a same-named pointer traced under identity-schemas.v3 does not discharge identity-schemas.v2.

## B. Prose derivation / complete replay

Composition §9, atom, enumeration, and execution-inputs contracts were read in contiguous chunks. Field account: `prose-law-account.json`.

Replay now requires exactly one run/plan/proof, binds universe to a Plan-selected context, selects subjects per enabled rule from retained inventories, and compares **complete C** of proof, findings, witnesses, evidence, seal, and Run.

Helper correction: claimed `evidence.coverageIds` omitted `coverage2:cc962fa0…` that §9.7 includes (views ∪ EI coverage). Pre-correction store: `inventory/v4-before-evidence-coverage-remint.store.json`.

After remint, proof C `4c63cd037bd9f8f406d30eecfa726f8d480da23ed04b7fddded804dd6a9f5a44` equals derived C; output mismatches empty. Fresh-process replay of raw export bytes passes.

This graph’s selected program uses `exists` over file subjects. Unused atom ops were not treated as executed.

## Semantic negative

Mutate finding.severity, remint finding/proof/evidence/seal/run. Schema admit **passes** (156 records). Independent complete replay **refuses**. `inventory/semantic-negative.json`.

## Export

Store SHA-256 `71cfaccf7f97291fe8d1df1ce3a65541fd4820a9255d6a0cb002cffd9deab41d`  
`run3:1050928bec362407438bad61d96896bd00c137d8af32e6a731ed6b6789b620f5`

Original TS attached properties retained. Original 123/8/3 remains required later (`next-work.md`).
