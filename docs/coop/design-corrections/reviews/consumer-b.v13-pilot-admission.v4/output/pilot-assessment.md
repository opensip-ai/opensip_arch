# consumer-b.v13-pilot-admission.v4

**Verdict:** `PILOT-CHECKPOINT-COMPLETED`  
**reconstructionAccepted:** false  
**rootAdmission:** unobserved  
Whole-task `ACCEPT-RECONSTRUCTABLE` remains prohibited.

This turn fixed exact condition matching and executed independent complete-proof replay against the selected composition/atom/enumeration/execution-inputs laws.

## A. Exact matching

v3 `run_condition_trace.py` matched `(condition, instance, field)` then fell back to `(condition, instance)`, ignored document identity, and exited 0 even if missing was nonempty. That zero is not required-occurrences minus executed-occurrences.

Preserved:

- Weak v3 result: `inventory/v3-weak-matching-coverage-difference.json` (claimed missing 0)
- First exact mismatch: `inventory/v4-exact-matching-first.json` (**124 OPEN**)

Reconciled without dropping owed conditions:

- Historical `identity-schemas.v2.json` tables are not aliased onto v3-admitted records
- Required `field` is the actual compared field, not a generic `payload` bucket
- Process now exits 1 if any required 4-tuple is missing

Current exact result: **1245 required, 2530 traces, 0 missing**.

Negatives (`inventory/exact-match-negatives.json`):

- Omitting one required field comparison leaves OPEN and would fail the checkpoint
- A same-named pointer traced under identity-schemas.v3 does **not** discharge the same pointer under identity-schemas.v2

Document aliases are only schema `$id` → that document's kit path.

## B. Prose derivation / complete replay

Contracts read in contiguous chunks: composition v3, atom v1, enumeration v1, execution-inputs v1, and identity-and-evidence selected joins (fact2 C encoding, ladder vs rungs).

Field account: `prose-law-account.json`.

Replay now:

- Requires exactly one `run3` / `plan2` / `proof3` and joins them
- Binds universe to a Plan-selected native context (not the first `tsconfigGraphHash` object)
- Selects subjects per enabled rule kind from retained inventories
- Takes detectorClosure from the emission binding for that rule
- Compares **complete C** of proof, findings, witnesses, evidence, seal, and Run

Helper correction: claimed `evidence.coverageIds` omitted `coverage2:cc962fa0…` that composition §9.7 includes (views ∪ EI coverage). Pre-correction bytes: `inventory/v4-before-evidence-coverage-remint.store.json`. Builder reminted evidence/seal/run.

After remint: proof C `4c63cd037bd9f8f406d30eecfa726f8d480da23ed04b7fddded804dd6a9f5a44` equals derived C; output mismatches empty (`pilot/ts-complete-replay-compare.json`). Fresh-process replay of raw export bytes passes.

This graph's selected program uses `exists` over file subjects. `count-at-most` / `all-covered` / `none` are unused on this selected tree (not missing-handler inapplicable for owed nodes).

## Semantic negative

`inventory/semantic-negative.json`: mutate finding.severity, remint finding/proof/evidence/seal/run. Schema admit **passes** (156 records). Independent complete replay **refuses** (findingIds / ruleResults / evidence.findingIds). Not a missing-record prerequisite.

## Export

- Store SHA-256 `71cfaccf7f97291fe8d1df1ce3a65541fd4820a9255d6a0cb002cffd9deab41d`
- `run3:1050928bec362407438bad61d96896bd00c137d8af32e6a731ed6b6789b620f5`
- Original TS attached properties retained

## Commands

```
/tmp/opensip-architecture-review-env/bin/python -I -B derive_conditions.py
/tmp/opensip-architecture-review-env/bin/python -I -B run_condition_trace.py
/tmp/opensip-architecture-review-env/bin/python -I -B run_exact_match_negatives.py
/tmp/opensip-architecture-review-env/bin/python -I -B pilot_ts_rebuild.py
/tmp/opensip-architecture-review-env/bin/python -I -B pilot_ts_fresh_replay.py
/tmp/opensip-architecture-review-env/bin/python -I -B run_semantic_negative.py
```
