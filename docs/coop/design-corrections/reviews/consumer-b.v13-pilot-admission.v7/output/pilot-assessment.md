# consumer-b.v13-pilot-admission.v6

**Verdict:** `PILOT-CHECKPOINT-INCOMPLETE`  
**reconstructionAccepted:** false  
**rootAdmission:** unobserved  
Whole-task `ACCEPT-RECONSTRUCTABLE` remains prohibited.

This checkpoint corrected the **inventory methodology** (descriptions, unrecognized predicates, document identity, field walk, derived identities). It does **not** close every selected owner law. Remaining OPEN work is listed below. Incomplete is reported rather than an unsupported COMPLETE.

## Method corrections (own code)

1. `derive_conditions.py` no longer treats `description` as SCHEMA_NOISE. Textual clauses are inventoried. `keep_pointer` no longer drops unrecognized families (`return True`). Dedup is `(document, pointer, instance, field)`.
2. `specification_inventory.py` walks selected schemas including `$ref` sibling keywords, applicators, and all `description`/`note`/`standing` strings, classified **by content** (MUST/refuses/equals vs illustration/provenance), plus incorporated prose contracts. Unbound mandatory clauses stay required with instance `UNBOUND`.
3. `enumerate_output_fields.walk_props` follows `$ref` with sibling keywords, `allOf`/`oneOf`/`anyOf`/`if`/`then`/`else`/`not`, and nested items. Presence/`suppliedJoin` is **not** `executed=true`. Output identity fields are `H` of the **derived** record, not copies of claimed pointers.
4. `evaluator.replay_from_retained` takes evaluator closure from Plan `semanticClosures` (kind=evaluator) and `executionPlanId` from admitted ExecutionInputsV1; evidence/seal/run identity fields are hashed from derived descriptors.

v5 required-count 1245 with 0 missing was after family-list filtering and description exclusion. That zero is **not** coverage of all selected owner laws. Preserved: `inventory/v6-before-methodology-correction.store.json` (the v5 positive).

## Specification inventory (executed as inventory, not as full admission)

| Quantity | Value |
|---|---|
| Selected schema documents | 19 |
| Clauses walked | 2877 |
| Bound occurrences (document identity in key) | 3257 |
| Mandatory-candidate occurrences | 1550 |
| Textual predicates interpreted with operands | 31 (0 refuse) |
| Unrecognized mandatory clauses still OPEN | **381** |

Account: `inventory/specification-inventory.json`, `inventory/textual-predicate-execution.json`.

Interpreted examples (operands compared, not labels): `semantic-evidence.importIds` Cset-equals `plan.importIds`; `scope.enumeratorClosure` kind=provider; EI `planId` equals selected Run plan; inventory `deficiency` null iff `state=complete`; TargetAttributionV2 `exported`/`evaluationNativeId`/`producerClosure` joins; enumeration-plan `snapshotId`/`scopeDigest` equals Plan.

The remaining 381 mandatory-candidate description/prose clauses were **not** dumped as PASS. They stay OPEN-uninterpreted.

## Field enumeration

283 walked fields including applicator variants. 225 executed comparisons. Nested ExecutionInputsV1 item joins (selectedRefs members, stage receipts, nativeCoverageAccounts rows, candidate refs, most cellOutcome columns) remain **unexecuted** in this enumerator even where `law_admit` families exist. Applicator-prefixed finding/witness/subject rows still lack a composition selector string (unaccounted labels) even when a branch check ran.

Proof C still equals the retained claim; `outputMismatches` empty. That whole-record equality does **not** discharge the OPEN nested/input/description conditions.

## Structural / semantic (still pass on this graph)

Same functions as v5:

- Positive `run3:f7525dc7…` — `structural_admit` pass, `semantic_replay` pass, fresh `pilot_ts_fresh_replay.py` pass. Store SHA-256 `f71af38af2d90acaf6846b04e92463791cf81b82619185e6b5576717c767f5ae`.
- Negative `run3:cbac72bc…` — same `structural_admit` pass, same `semantic_replay` refuse (`findingIds`; claimed `bea89606…` vs derived `91b449ff…`). Store SHA-256 `ff65d146660a80a4217b1f3135f5f6164672c8822ffda2cf2edf0ab23181bb17`. Fresh subprocess confirmed.

No remint was required after identity-from-derived hashing: derived IDs matched claimed IDs because complete C already matched.

## Fully executed / narrowly checked / unexecuted

**Fully executed on this TS graph:** shared structural entrypoint; semantic replay; native RC-0/1/2/6/§4.1a/lib joins from v5; 31 interpreted description joins; derived-identity hashing; specification inventory production.

**Narrowly checked:** if/then/else finding correspondence and packageManifestPath branches; EI planId/executionPlanId/evaluatorClosure/cell deficiency pairing.

**Unexecuted / OPEN (fails this checkpoint):**

1. Interpret and compare the remaining **381** mandatory-candidate textual/prose clauses (composition, atom, enumeration, execution-inputs, native-evidence, and schema descriptions) with actual operands — not family labels.
2. Independent per-field owner joins for **ExecutionInputsV1 nested arrays** (selectedRefs totality already has a law_admit family; it is not attached as executed per-item field evidence here).
3. Full contiguous read of remaining `identity-and-evidence.md` beyond selected joins.
4. Rust / syntax complete Runs; query/workflow; original 123/8/3 as a whole-task set.

No new design gap is inferred from omitted helper coverage. These are existing kit laws not yet compared.

## Commands

See `pilot/commands-v6.json`.
