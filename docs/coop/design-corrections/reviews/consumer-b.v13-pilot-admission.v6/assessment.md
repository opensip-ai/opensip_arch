I'll start from the full v6 prompt and the v5 inventory/enumeration code so the law-coverage gaps can be corrected against the kit, not from prior claims.I’ll fix identity derivation from derived records first, then rebuild the specification inventory so descriptions and unrecognized predicates are no longer dropped.I’ll execute the schema if/then/else branches on findings, subjects, and cell outcomes so those applicators aren’t left as a whole uncompared class.**PILOT-CHECKPOINT-INCOMPLETE.** `reconstructionAccepted` is false. Root admission is unobserved. No whole ACCEPT.

The v5 “1245 required / 0 missing” result was not coverage of all selected owner laws: descriptions were dropped by key name, unrecognized predicates fell out of a family list, and dedup omitted document identity.

**What changed in the method**

- Specification inventory now walks selected schemas **including** `description`/`note`/`standing`, classified by **content** (MUST/refuses/equals vs illustration), plus incorporated prose. Dedup is `(document, pointer, instance, field)`. Unrecognized clauses are kept.
- Field walk follows `$ref` with sibling keywords and `allOf`/`if`/`then`/`else`. Presence is not `executed=true`. Evidence/seal/run IDs are `H` of the **derived** record, not copies of the claim. Evaluator closure and `executionPlanId` come from Plan/EI, not the claimed proof.

**Inventory vs execution**

| | |
|---|---|
| Clauses walked | 2877 |
| Occurrences with document identity | 3257 |
| Mandatory-candidate | 1550 |
| Textual predicates actually compared | **31** (0 refuse) |
| Still OPEN uninterpreted | **381** |

Those 381 are not marked PASS. Nested ExecutionInputsV1 item joins also remain unexecuted in the field enumerator.

**What still works on this graph**

Positive `run3:f7525dc7…` structurally and semantically passes (fresh process). Negative `run3:cbac72bc…` uses the same functions: structural pass, semantic refuse on `findingIds`. Exports unchanged (`f71af38a…` / `ff65d146…`). Pre-correction copy: `inventory/v6-before-methodology-correction.store.json`.

**Owed before rust/syntax/query:** interpret the 381 mandatory clauses with real operands; attach per-item EI owner joins; finish remaining `identity-and-evidence.md` reading. Existing kit laws omitted from the helper are not design gaps.
