# Proposed small field-derivation edits (output only)

Standing: coauthor proposal for Codex to reconcile into the target-identity successor. Not applied to frozen v24. Does not change intended semantics. Does not add an alternate evaluator. Does not duplicate native extraction (accounts remain derived from owner Coverage / inventories already admitted by execution-inputs). Preserves absent / unknown / incomplete / operational distinctions and complete-proof replay.

---

## Edit A — composition retained-input paragraph

**File.** `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md`  
**Current (retained-input section):**

> Each atom's witness binds the complete admitted evaluation input selection, retaining availability and empty-population inputs as well as hits.

**Replace with:**

Each atom is evaluated against the complete admitted input closure, including availability and empty-population inputs. `predicate-witness` has no `inputRefs` field (schema `additionalProperties: false`). Atomic `predicateProofs[].inputRefs` is the canonical set of every `ProofInputRef` that atom law actually read for that node: owning views of matching and uncertain facts; consulted Coverage; owed/selected imports of that atom's evidence kind, including zero-owed and empty wrappers; expected inventories the completeness law reads; consumed incoming-search and target-attribution sidecars. Empty owed partitions and wrappers are retained; known hits are not a license to drop them. The set is a subset of `proof.evaluationInputRefs`. It is not automatically equal to `proof.evaluationInputRefs` (that field also names unrelated cells' inventories, the ExecutionInputsV1 manifest, and inputs of other atoms). Boolean `predicateProofs[].inputRefs` is the canonical union of the immediate children's sets. Witnesses cannot add roots outside the admitted closure.

---

## Edit B — composition §8: execution-deficiency derivation table

**File.** `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md` §8  
**Insert after:** “All inputRefs are exact supporting roots and all non-null subject/predicate addresses belong to this rule's independent evaluation.”

Required-cell failures are written to `proof.executionDeficiencies` even when every rule is disabled. They are not copied from claimed proof bytes. `ExecutionInputsV1` itself is `proof.executionInputsDigest` and exactly one member of `proof.evaluationInputRefs`. That manifest ref is not prepended onto deficiency `inputRefs` and does not replace original source records. `evaluation-deficiency` has no cell/program/relation members; distinct required cells survive `canonical-set` only by keeping those original refs (and differing `universe` / `nativeCause` / `cause` where they actually differ). Dedup on `(cell, program, cause, relation)` remains forbidden.

| Failure class | `source` | `cause` | `nativeCause` | `universe` | `subjectId` / `predicateId` | `inputRefs` |
|---|---|---|---|---|---|---|
| Required partial or unavailable inventory | `execution` | `required-cell-unsatisfied` | inventory carrier, or null | binding universe or null | null / null | each failing `subject-inventory` digest; keep sibling inventories of that cell |
| Required unavailable binding or enumerator | `execution` | the binding pair if it is already an execution-registry cause (`provider-unavailable`, `budget-exhausted`, `input-closure-incomplete`, …); otherwise `required-cell-unsatisfied` | binding carrier, or null | binding universe or null | null / null | any still-retained same-cell inventory refs; empty if none |
| Required candidate envelope incomplete | `execution` | `required-cell-unsatisfied` | candidate carrier, or null | envelope universe or null | null / null | that `candidate-producer-result` digest |
| Required native account incomplete, mixed complete+unknown, or missing expected subjects (`source-path` / `package-name` / `symbol`) | `native` | original native-registry cause (`uncovered-expected-source-subject`, `coverage-unknown`, `missing-relation-coverage`, `provider-unavailable`, …) | per-Coverage carrier; do not unzip deficiency from a later unrelated nativeCause | account `sourceUniverse` or null | null / null | every original Coverage `inputRef` from that account's `coverageRecords`; keep all original coverage and inventory source records |
| Required unsupported-typed matrix cell | `execution` | `required-cell-unsatisfied` | matrix carrier if it is a `NativeCause`, else null | binding universe or null | null / null | empty; do not fabricate Coverage |
| Deterministic work-budget-exhausted | `execution` | `work-budget-exhausted` | null | null | null / null | `proof.evaluationInputRefs` |

Do not emit `native-work-incomplete` or `unsupported-typed` as `evaluation-deficiency.cause` (they are not in the closed execution enum). Native `DeficiencyV2` stays on the ExecutionInputs outcome/account row. Proof `cause` is the registry member required by `source`. Import deficiencies continue to carry `evidenceKind` and null `nativeCause`; other sources carry `evidenceKind=null`.

---

## Edit C — execution-inputs §4 / §5 join sentence

**File.** `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md`  
**After §4 sentence:** “Required partial inventory with otherwise complete native accounts still emits `required-cell-unsatisfied` with the inventory digest as `inputRef`.”

**Insert:**

That inventory digest is the proof `executionDeficiencies[].inputRefs` member for this failure class. It is not the supporting ref for a required native-account failure: those keep the Coverage `inputRef`s from `coverageRecords` (§5). Admission `requiredCellDeficiencies` / `derivedOutcomes` / `coverageRecords` are reconstruct joins, not hashed members of ExecutionInputsV1. Mapping them into `proof.executionDeficiencies` follows composition §8's table. The ExecutionInputsV1 digest remains `proof.executionInputsDigest`.

**After §5 uniqueness sentence** (“Dedup on `(cell, program, cause, relation)` is forbidden…”):

Proof items have no cell/program/relation fields. Preserve uniqueness by retaining every original Coverage and inventory `inputRef` on the corresponding deficiency. Do not collapse two Coverage of the same relation with different carriers into one record.

---

## Edit D — schema annotations (descriptions only)

**File.** `docs/coop/design-corrections/foundation/identity-schemas.v3.json`

### D1. `proof-bundle.properties.predicateProofs.items.properties.inputRefs`

Add:

```json
"description": "Canonical set of ProofInputRefs the addressed node actually read under atom/composition law, including empty owed partitions and wrappers. Subset of proof.evaluationInputRefs. Boolean nodes: canonical union of immediate children. Not hits-only. Not automatically equal to proof.evaluationInputRefs. Witnesses do not carry this field."
```

### D2. `proof-bundle.properties.executionDeficiencies`

Add:

```json
"description": "Independently recomputed required-execution and budget deficiencies, including when all rules are disabled. Item source/cause follow the closed registry and composition §8 failure-class table. inputRefs are the original failing Coverage, inventory, or candidate roots, not a substitute ExecutionInputsV1 ref. subjectId and predicateId are null on cell-level items."
```

### D3. `semantic-evidence.properties.importIds.description`

**Current last two sentences:**

> The evaluated SUBSET is named separately by proof-bundle.evaluationInputRefs; a selected import that nothing evaluated is still resolved and retained by the Run closure, and being selected alone grants it no evidence authority.

**Replace those two sentences with:**

This array equals `plan.importIds` as a canonical set (IMPORT_JOIN). A selected import that nothing evaluated is still resolved and retained. Being selected alone grants it no evidence authority. `proof.evaluationInputRefs` is the complete selectedRefs plus the ExecutionInputsV1 ref, not an evaluated subset. Per-node evaluated/consulted import roots, when present, appear on `predicateProofs[].inputRefs` and on finding `evidenceRefs` as specified by composition.

### D4. `evaluation-deficiency.properties.inputRefs`

Add:

```json
"description": "Exact supporting roots for this deficiency: original Coverage, subject-inventory, candidate-producer-result, or import refs. Canonical-set unique. Do not replace original source records with the ExecutionInputsV1 ref. Cell-level items have null subjectId and predicateId."
```

---

## Edit E — identity-and-evidence §4 one sentence

**File.** `docs/v2/contracts/product-v1/identity-and-evidence.md` §4  
**Current:**

> They bind the exact compiled-program node, admitted input references, matching and uncertain facts or imported observation addresses, Coverage and scope references, typed deficiencies and any quantifier limit.

**Replace “admitted input references” clause with:**

They bind the exact compiled-program node. Admitted input references for that node are `predicateProofs[].inputRefs` (witnesses have no `inputRefs` field). Witnesses also bind matching and uncertain facts or imported observation addresses, Coverage and scope references, typed deficiencies and any quantifier limit.

---

## Non-edits (intentional)

- No new evaluator profile, H domain, or native extraction rule.
- No `cellOrdinal` added to `evaluation-deficiency`.
- No change to Kleene, budget formula, operational/semantic split, or complete-`C` replay criterion.
- Symbol expected-subject census remains execution-inputs §5 existing law; not restated as new design.
- `proof.evaluationInputRefs` totality law is unchanged.
