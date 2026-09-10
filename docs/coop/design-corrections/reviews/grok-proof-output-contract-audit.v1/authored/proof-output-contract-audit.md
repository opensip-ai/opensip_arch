# Evaluator3 proof-output contract audit

**Standing.** Bounded DESIGN COAUTHOR diagnostic on frozen `candidate-subject.v24`. Not a blind consumer review. Not independent final design acceptance. Not product implementation, commit/push, live source edit, or historical rewrite. Codex is finishing authorized architecture/design/reference corrections. Another coauthor is editing an isolated target-identity successor; this session did not read or modify its active bytes.

**Python.** `/tmp/opensip-architecture-review-env/bin/python -I -B` used only to inventory frozen files. No subagents. No web.

**Question.** Does the current published normative-only kit uniquely determine a complete evaluator3 proof and every referenced output field from admitted inputs, or does any field derivation live only in excluded reference code?

**Answer.** The kit does **not** uniquely determine complete proof bytes. Several proof fields that change `C(proof)` admit more than one reconstruction that all satisfy schema shape. The excluded reference implements one convention. P7’s successor complete-`C` path implemented another that matched claimed syntax-data bytes. Neither convention is kit-unique reconstructability. Root reference is not automatically law. P7 full-`C` equality is not sufficient when expected fields are derived from an arbitrary convention.

No acceptance, freeze, or readiness is granted.

---

## 1. Corpus and method

### 1.1 Admitted kit (normative-only reconstructability)

Incorporated by `docs/v2/contracts/product-v1/identity-and-evidence.md` §4:

| Path under `candidate-subject.v24` | Role |
|---|---|
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | Incorporating owner; complete replay criterion |
| `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md` | Proof/finding/verdict/deficiency composition |
| `docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md` | Atom truth, completeness, witness causes |
| `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` | ExecutionInputsV1, accounts, required cells |
| `docs/coop/design-corrections/foundation/enumeration-contract.v1.md` | Expected inventories, extents, membership |
| `docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md` | Operational vs semantic boundary |
| `docs/coop/design-corrections/foundation/identity-schemas.v3.json` | `proof-bundle`, `predicate-witness`, `evaluation-deficiency`, `rule-result`, `ProofInputRef`, `x-opensip-evaluator-deficiency-registry` |
| `docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json` | Hashed ExecutionInputsV1; **no** `requiredCellDeficiencies` field |
| `docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json` | EnumerationPlanV1 |
| `docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json` | SubjectInventoryV1 |
| `docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json` | Emission bindings |
| `docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json` | Atom input keys, relation/capability map |
| `docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json` | `RuleProgramV2` / `Predicate` |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` `#/$defs/NativeCause` | Owner carrier enum |

### 1.2 Authorized reference (comparison only; not kit reconstructability)

`evaluator_composition_model.v3.py`, `evaluator_input_model.v3.py`, `evaluator_replay_model.v3.py`, `execution_inputs_model.v1.py`, `atom_model.v1.py`, `enumeration_model.v1.py`.

“Reference function says so” is not normative-only reconstructability.

### 1.3 Inputs beside this prompt

- `p7-producing-selfaudit.md` / `.json` — COMPLETE49 four-Run self-audit
- `root-syntaxdata-field-diagnostic.json` — selected-field discrepancy on syntax-data `run3:ab1d6fc4…`
- `pilot-producing-diagnostic.json` / `pilot-root-assessment.md` — pilot symbol-census (existing-law omission)

### 1.4 Classification used below

| Class | Meaning |
|---|---|
| **Covered** | Kit prose + schema annotations uniquely determine the field from admitted inputs |
| **Explicit law missed by consumer** | Kit is unambiguous; a consumer/checker/export failed to execute it |
| **Underspecified mapping** | Coherent intended law exists, but two or more field reconstructions remain open |
| **True contradiction** | Kit texts cannot all be true |
| **Reference bug** | Excluded reference disagrees with closed kit membership or with itself |

Honest **schema-only** reconstructability is treated separately from **admitted whole-Run** reconstructability (identity-and-evidence §4 + the four incorporated contracts). Schema-only is never complete-proof uniqueness: `uniqueItems` + `x-opensip-order: canonical-set` constrain order and duplicate records, not which supporting roots belong in the set.

---

## 2. Substantive verdict

The published normative-only kit defines:

- the **shape** of a version-3 proof and every required member;
- **complete-proof replay** as `C` of the whole recomputed proof plus referenced output preimages (composition §7; identity-and-evidence §4);
- **proof.evaluationInputRefs** = ExecutionInputs `selectedRefs` ∪ `{domain:execution-inputs, digest}` (composition §1; execution-inputs §7);
- **proof.executionInputsDigest** = raw SHA-256 of `C(ExecutionInputsV1)`;
- Kleene truth, postorder retention of every node, witness kind/emptiness, finding emission, waiver/verdict aggregation, disabled-rule empty enumeration, required-cell independence from disabled rules.

It does **not** uniquely define:

1. `predicateProofs[].inputRefs` complete Run selection vs consulted subset vs hits-only;
2. `proof.executionDeficiencies[]` `source` / `cause` / `inputRefs` mapping from required native account vs inventory vs candidate/binding failure, including whether the ExecutionInputsV1 ref is prepended;
3. exact supporting `inputRefs` on `ruleResults[].deficiencies` and on witness `deficiencies` for atom/import/coverage carriers.

Those three families change proof bytes. A consumer can obtain complete `C` equality by copying a convention. That is not kit-unique reconstructability.

**Kit-unique complete evaluator3 proof: no.**

---

## 3. Focus (1) — atomic `predicateProof.inputRefs`, witness, boolean unions

### 3.1 What the kit actually says

**Schema (`identity-schemas.v3.json#/$defs/proof-bundle/properties/predicateProofs`).** Required `inputRefs` array of `ProofInputRef`, `uniqueItems`, `x-opensip-order: canonical-set`. No description. No `minItems`. No join to `proof.evaluationInputRefs`. No “complete vs subset” annotation.

**Witness schema (`#/$defs/predicate-witness`).** `additionalProperties: false`. Required fields do **not** include `inputRefs`. Boolean kind forces empty match/Coverage arrays and null `countLimit`. Native-atom forbids import rows and children. Imported-atom forbids facts, Coverage, and children.

**Composition §3.** “All input references are direct retained roots or members of an evaluated view as the identity closure permits; witnesses cannot add roots.” Boolean witnesses: kind `boolean`, children exactly the grammar’s immediate child addresses, empty fact/import/Coverage match arrays. Atomic witnesses: kind `native-atom` or `imported-atom`, no children.

**Composition retained-input paragraph.** “Each atom’s witness binds the complete admitted evaluation input selection, retaining availability and empty-population inputs as well as hits.”

**Identity-and-evidence §4.** Predicate-witness records “bind the exact compiled-program node, admitted input references, matching and uncertain facts or imported observation addresses, Coverage and scope references, typed deficiencies and any quantifier limit.”

**Atom contract §8.** `evaluate_atom` returns `evaluationInputRefs` among other fields. No statement that this array is copied onto `predicateProof.inputRefs`.

**Semantic-evidence `importIds` description (true contradiction).** “The evaluated SUBSET is named separately by proof-bundle.evaluationInputRefs.” Composition §1 and execution-inputs §7 require `evaluationInputRefs` to be the **complete** selected set plus the manifest ref, including selected imports that nothing evaluated.

### 3.2 What the excluded reference does

`evaluator_replay_model.v3.py` `scanner` (lines 23–45):

- Comment: every atom binds the complete admitted input selection.
- Sets `inputRefs = normalized['evaluationInputRefs']` (the **whole Run** selection).
- Ignores `atom_model.v1.py`’s own `evaluationInputRefs` (native path: consumed Coverage ids only, `atom_model.v1.py` ~1495–1527).
- Copies atom `scopeIds` and witness `coverageIds` from the atom result (**consulted**, not Run-wide).

`evaluator_composition_model.v3.py` `eval_node` (lines 131–150):

- Boolean `inputRefs` = canonical union of children.
- Atomic `inputRefs` = scanner result.
- Witness blob has **no** `inputRefs` field.

So the reference is internally inconsistent: `inputRefs` are Run-wide, `scopeIds`/`coverageIds` are consulted. The composition “complete selection” sentence is implemented only for `predicateProof.inputRefs`.

### 3.3 Root vs claimed vs P7

`root-syntaxdata-field-diagnostic.json` path `/predicateProofs/0/inputRefs`:

| | Count | Members |
|---|---|---|
| Claimed | 2 | `view:995522af…`, `coverage:d8eb8768…` |
| Root-derived | 8 | 3× `subject-inventory`, 3× `coverage`, `view:995522af…`, `execution-inputs:d8ec00cb…` |

P7 successor complete-`C` matched the claimed proof, so P7’s expected `predicateProof.inputRefs` were the 2-ref set (or whatever convention reproduced claimed bytes), not the 8-ref reference emission.

### 3.4 Competing constructions

**Schema-only.** Any unique `ProofInputRef` list is shape-valid, including empty, including refs absent from `evaluationInputRefs`. Not unique.

**Whole-Run construction B (reference).** Every atomic `predicateProof.inputRefs` equals `proof.evaluationInputRefs`. Boolean union is idempotent and also equals that set. Makes the per-node field redundant with the proof-level field. Matches the retained-input sentence if “binds” means “lists”.

**Consulted-set construction A.** Atomic `inputRefs` = every admitted root the atom law **read** for that node, including empty owed partitions/wrappers (not hits-only). Boolean = canonical union of children. Subset of `evaluationInputRefs`. Matches “exact supporting roots” (composition §8), matches why the field exists per node, matches reference treatment of `scopeIds`/`coverageIds`.

**Hits-only construction H.** Only views/Coverage/imports that produced known matches. Forbidden by “retaining availability and empty-population inputs as well as hits,” but schema-legal. Claimed 2-ref list is consistent with H or with a thin A (one evaluated view + one Coverage).

**Classification: underspecified mapping**, plus **true contradiction** on the semantic-evidence `importIds` annotation. Witness carrying no `inputRefs`: **covered** (schema `additionalProperties: false` + composition §3 emptiness laws). Boolean union algorithm: **covered** as union-of-children once atomic sets are defined; the atomic sets are not.

A small table (proposed patch) can remove B vs A vs H without a new evaluator and without duplicating native extraction: atom contract already says which Coverage, inventories, imports, and sidecars the atom reads.

---

## 4. Focus (2) — `proof.executionDeficiencies`

### 4.1 Kit law that is actually unique

| Topic | Owner | Status |
|---|---|---|
| Required cells still emit execution deficiencies when all rules are disabled | composition §5, §1 | Covered |
| Operational provider protocol stays operational, not semantic unknown | composition §5; fault contract | Covered |
| Closed `source` × `cause` membership | `identity-schemas.v3.json#/$defs/evaluation-deficiency` `allOf` + `x-opensip-evaluator-deficiency-registry` | Covered as **shape** |
| `evidenceKind` required for import, null otherwise | schema `allOf`; composition §8 | Covered |
| `nativeCause` is owner `NativeCause` or null; cannot widen `DeficiencyV2` | schema enum = native `NativeCause`; composition §8 | Covered as enum |
| `subjectId`/`predicateId` null unless they belong to that rule’s evaluation | composition §8 | Covered for cell-level (must be null) |
| `universe` nullable 64-hex native-universe suffix | schema | Covered as shape |
| Canonical uniqueness of every distinct cause and coordinate; no `(cell, program, cause, relation)` collapse | execution-inputs §5 | Covered as **intent**; see mapping gap |
| Required partial inventory with otherwise complete native accounts → `required-cell-unsatisfied` with **inventory digest** as `inputRef` | execution-inputs §4 | Covered for **that failure class** |
| Native account records keep `deficiency+nativeCause+inputRef` together; `inputRef` is the Coverage | execution-inputs §5 | Covered for **account records**, not automatically for proof items |
| `proof.evaluationInputRefs` includes the ExecutionInputsV1 ref; `proof.executionInputsDigest` is `C` of that record | composition §1; execution-inputs §7; schema `executionInputsDigest` | Covered |
| `requiredCellDeficiencies` / `derivedOutcomes` / `coverageRecords` | admission results in execution-inputs model | **Not hashed fields** of ExecutionInputsV1 (`execution-inputs.schema.v1.json` has no such members) |

`evaluation-deficiency` has **no** `cellOrdinal` / `programOrdinal` / `relation` / `resolution`. Distinct required cells survive `uniqueItems` / `canonical-set` only if `inputRefs`, `universe`, `cause`, or `nativeCause` differ. If mapping drops original Coverage/inventory refs and leaves only a shared ExecutionInputsV1 ref, two cells collapse. That would violate execution-inputs §5 uniqueness.

### 4.2 What the excluded reference does

`execution_inputs_model.v1.py`:

- `derive_outcome` keeps original source items: inventory → `{domain:subject-inventory,digest}`; coverage records → that Coverage `inputRef`; candidate → `{domain:candidate-producer-result,digest}`; binding/enumerator often empty `inputRefs`.
- Emits `requiredCellDeficiencies` with **`source: "execution"` always**.
- Causes include **`native-work-incomplete`** and **`unsupported-typed`**, which are **not** in the closed execution cause enum (`identity-schemas.v3.json` execution causes: `budget-exhausted`, `confidence-floor-unmet`, `derivation-policy-unmet`, `external-consumers-unknown`, `input-closure-incomplete`, `language-tier-unsupported`, `provider-unavailable`, `required-cell-unsatisfied`, `required-relation-missing`, `resolution-incomplete`, `work-budget-exhausted`).

**Reference bug.** Those two cause spellings cannot appear on a proof deficiency with `source=execution`.

`evaluator_input_model.v3.py` `execution_input_account` (lines 46–56):

```
cause = row.get('deficiency')   # native DeficiencyV2, NOT row['cause']
if cause not in execution-registry:
    if cause not in (None, 'source-syntax-invalid'): raise UNREGISTERED
    cause = 'required-cell-unsatisfied'
source = 'execution'
inputRefs = {execution-inputs ref} ∪ row['inputRefs']
universe = binding['universe']
subjectId = predicateId = None
```

Effects:

- Always `source=execution`, even when the original typed cause is a **native-registry** cause (`coverage-unknown`, `uncovered-expected-source-subject`, …). Schema `allOf` would then forbid keeping the original cause.
- Uses `row.deficiency` rather than `row.cause`, so `native-work-incomplete` is discarded and a native `DeficiencyV2` (or `required-cell-unsatisfied` if null) is stamped instead.
- **Prepends** the ExecutionInputsV1 ref onto every deficiency. Kit never says deficiency `inputRefs` include that manifest. The manifest is already `proof.executionInputsDigest` / `evaluationInputRefs`.
- `E.cset` uniqueness is of the mapped record. Distinct original sources survive only if their remaining `inputRefs` still differ after the prepend.

### 4.3 Root vs claimed vs P7 on syntax-data

`root-syntaxdata-field-diagnostic.json` `/executionDeficiencies/0`:

| Field | Claimed | Root-derived |
|---|---|---|
| `source` | `native` | `execution` |
| `inputRefs` | `[subject-inventory 3148550880…]` | `[coverage b87610f362…, execution-inputs d8ec00cbd4…]` |

P7: original selected-field compare would have accepted empty `inputRefs`. Successor “derives those refs from the required clones-fact cell `inventoryDigests` (execution-inputs §4), then complete `C(proof)` matches claimed.”

That P7 sentence assumes the failure class is **required partial inventory**. Execution-inputs §4 is exactly that class. It is **not** the law for a required **native account** failure; §5 keeps Coverage `inputRef`s. Root’s derived pair (Coverage + ExecutionInputs) is the input-model convention for a native-account row after prepending the manifest ref.

Three reconstructions, all schema-shaped if `cause` is chosen to match `source`:

| Construction | `source` | `inputRefs` | Motivating kit text |
|---|---|---|---|
| Claimed / P7 inventory | `native` | clones-fact inventory only | §4 inventory digest; claimed `source=native` |
| Root reference | `execution` | Coverage + ExecutionInputsV1 | input model always-execution + prepend |
| Kit-faithful account class | `native` if original cause is native-registry; else `execution`/`required-cell-unsatisfied` | original Coverage records only; **no** mandatory ExecutionInputs prepend | composition §1 “original typed causes and input references”; §8 “exact supporting roots”; §5 uniqueness |

**Classification: underspecified mapping** of requiredCellDeficiencies → `proof.executionDeficiencies`. **Reference bugs** as listed in 4.2. P7’s use of §4 for this graph is **not independently justified** from the kit without showing that the clones-fact inventory was actually non-complete. Hashed `cellOutcomes[].inventoryDigests` plus independently admitted inventory bytes would decide that; citing the claimed proof’s inventory ref does not.

`source=native` on an `executionDeficiencies` item is **schema-legal**. Composition §5 says required cells contribute to that **array**; it does not say every item’s `source` field equals `execution`. Forcing `source=execution` while “retaining original typed causes” is a **true contradiction** whenever the original cause is native-only (`uncovered-expected-source-subject`, `coverage-unknown`, `scope-without-coverage`, …).

### 4.4 Recommended join (does not change intended semantics)

Keep original source records. Do not invent cell coordinates on `evaluation-deficiency`. Do not duplicate native extraction: admission already derived accounts from Coverage.

Insert a derivation table (see `proposed-proof-field-derivation.patch.md`):

| Failure class | `source` | `cause` | `nativeCause` | `universe` | addresses | `inputRefs` |
|---|---|---|---|---|---|---|
| Required partial/unavailable inventory | `execution` | `required-cell-unsatisfied` | inventory carrier | binding U or null | null/null | each failing `subject-inventory` digest; keep siblings |
| Required unavailable binding/enumerator | `execution` | execution-registry cause if the binding pair is already in that enum (`provider-unavailable`, `budget-exhausted`, `input-closure-incomplete`, …), else `required-cell-unsatisfied` | binding carrier | binding U or null | null/null | any still-retained same-cell inventory refs; empty if none |
| Required candidate incomplete | `execution` | `required-cell-unsatisfied` | candidate carrier | envelope U | null/null | `candidate-producer-result` digest |
| Required native account incomplete / missing expected subjects | `native` | original native-registry cause (`uncovered-expected-source-subject`, `coverage-unknown`, `missing-relation-coverage`, `provider-unavailable`, …) | per-Coverage carrier; do not unzip | account `sourceUniverse` or null | null/null | **every** original Coverage `inputRef`; all coverage/inventory source records kept |
| Required unsupported-typed | `execution` | `required-cell-unsatisfied` (matrix `DeficiencyV2` is not an execution cause; keep it in `nativeCause` only if it is a `NativeCause`, else null) | matrix carrier if `NativeCause` else null | binding U or null | null/null | empty (no fabricated Coverage) |
| Work-budget-exhausted | `execution` | `work-budget-exhausted` | null | null | null/null | `proof.evaluationInputRefs` |

ExecutionInputsV1 remains `proof.executionInputsDigest` and one member of `proof.evaluationInputRefs`. It is **not** a substitute for the failing source records and is **not** prepended onto every deficiency.

---

## 5. Focus (3) — `ruleResult` / witness / required-import deficiencies and exact support refs

### 5.1 Covered

- One `ruleResult` per compiled policy rule, including disabled and zero-subject (schema description; composition §2, §5).
- Disabled: enumeration all arrays empty, outcome `disabled`, no predicates/findings (composition §2).
- Enumeration `inventoryRefs` = all relevant expected outcomes for the rule’s domain/kind, including unavailable; `incompleteInventoryRefs` includes partial/unavailable even with zero rows; known rows of partial inventories still evaluate (composition §2; enumeration §4).
- Outcome: live unwaived gating finding → fail; else gating incomplete/unresolved or root-indeterminate with blocking native/required-import cause → indeterminate; advisory findings do not fail; optional-only root unknown remains pass with disclosure (composition §5).
- Required import availability is independent of a boolean branch suppressing use (composition §5).
- Import deficiency carries `evidenceKind` even when no wrapper exists; missing import pointer is not required to identify the declaration (composition §8).
- Witness deficiencies retained even when a known value dominates (composition §3; atom §7).
- Root-indeterminate blocking causes are computed separately and are not a stored field (composition §3).

### 5.2 Underspecified / reference-only

**Exact `inputRefs` on atom-mapped deficiencies.** Replay `record()` stamps the **whole** `evaluationInputRefs` onto every atom cause, then overwrites Coverage-entry deficiencies to a single Coverage ref (`evaluator_replay_model.v3.py` 27–41). Kit: “exact supporting roots.” Whole-Run refs on a `scope-without-coverage` or `zero-owed-wrappers` item are a convention.

**`nativeDeficiencies` (sufficiency_v2 `DeficiencyV2`) → `evaluation-deficiency.cause`.** Replay does `record(deficiency)` with `source=native`. Some `DeficiencyV2` values are native-registry causes; some may not be. Kit does not give a field table. Untyped strings refuse (atom §7).

**Required `evidence-kind-unavailable`.** Input model uses empty `inputRefs` (`evaluator_input_model.v3.py` 188–189). Composition §8 allows no import pointer. **Covered as empty refs.**

**Correspondence deficiencies.** Composition model uses `enumeration['inventoryRefs']` as `inputRefs` (`evaluator_composition_model.v3.py` 190). Kit says unmatched correspondence is disclosed; it does not name those refs. **Underspecified**, small.

**Finding `evidenceRefs`.** Composition §4: root predicate-witness plus every descendant known/uncertain fact, used Coverage, and selected import ID; enumeration refs stay in the proof. Composition model also copies `inputRefs` with `domain==import` (line 178). “Selected import ID” vs matching/uncertain observation addresses is slightly loose. FindingEvidenceRef enum is `fact|coverage|import|predicate-witness|blob` — **no** `subject-inventory` / `execution-inputs`, which is consistent with leaving enumeration/execution refs on the proof.

### 5.3 Explicit law missed by a producer/consumer (not missing design)

Rust-partial claimed `ruleResults.enumeration` listing only the complete inventory-cell file inventory with outcome `pass`, omitting the clones-fact partial inventory: **explicit** composition §2 / enumeration totality. P7 correctly preserves this as diagnostic. First refusal remains earlier membership/extent cover. Do not treat as a kit hole.

Pilot symbol census: execution-inputs §5 already requires expected subjects of the relation’s subject-kind, **including `symbol`**. Enumeration §9 forbids recomputing extraction truth, not comparing admitted symbol rows to retained partitions. P5 `producing_law.py` 1430–1433 exemption is a **checker omission**. Not missing design. Not a proof-field derivation gap.

---

## 6. Every proof-bundle field (not only the examples)

| Field | Kit uniqueness | Notes |
|---|---|---|
| `schemaVersion` | Covered | const 3 |
| `planId` | Covered | Plan H |
| `executionPlanId` | Covered | exec-plan2 |
| `evaluatorClosure` | Covered | selected evaluator closure |
| `ruleProgramDigest` | Covered | `C(RuleProgramV2)`; schema + composition construction `{schemaVersion:2,policyDigest,rules[{ruleId,ruleProgramRef,emitWhen}]}` |
| `evaluationInputRefs` | Covered | `selectedRefs` ∪ execution-inputs ref; forbidden domains in execution-inputs §1 |
| `executionInputsDigest` | Covered | raw SHA-256 of ExecutionInputsV1 |
| `predicateProofs` population | Covered | every enabled rule × selected subject × postorder node; addresses identity-and-evidence §4 |
| `predicateProofs[].ruleId/subjectId/predicateId/operation/value` | Covered | operation = node `op`; value Kleene |
| `predicateProofs[].witnessDigest` | Covered | `C(predicate-witness)`; witness fields mostly covered |
| `predicateProofs[].inputRefs` | **Underspecified** | §3 |
| `predicateProofs[].scopeIds` | Mostly covered | atom completeness pairing; boolean union of children; not Run-wide |
| `findingIds` | Covered | emitWhen true → one finding3; unmatched still findings |
| `verdict` | Covered | fail ≻ indeterminate ≻ pass; required execution deficiencies induce indeterminate |
| `evaluationState` | Covered | `budget-exhausted` vs `evaluated` |
| `ruleResults` | Covered as rows | deficiencies’ refs: §5 |
| `ruleResults[].enumeration` | Covered | composition §2 |
| `ruleResults[].outcome` | Covered | composition §5 |
| `ruleResults[].findingIds` | Covered | all emitted, not only failing |
| `ruleResults[].deficiencies` | **Underspecified refs** | exact support roots |
| `waivedFindingIds` | Covered | effective WaiverSet only; findings preserved |
| `executionDeficiencies` | **Underspecified mapping** | §4 |
| Witness `kind` / empty match arrays / `childPredicateIds` / `countLimit` | Covered | schema `allOf` + composition §3 |
| Witness `matching*` / `uncertain*` / `coverageIds` | Covered | atom result; uncertain retained when known dominates |
| Witness `deficiencies` | **Underspecified refs** | same as atom mapping |
| Witness `inputRefs` | Covered **absent** | must not exist |
| Finding parameters / fingerprint / correspondence | Covered | composition §4; identity-and-evidence finding-parameters |
| Finding `evidenceRefs` | Slightly underspecified | §5.2 |
| Evidence3 `viewIds`/`coverageIds`/`importIds` | Covered with **contradiction** in importIds annotation | replay: views from evaluationInputRefs; coverage = union of those views plus explicit coverage inputs; importIds = `plan.importIds` |
| Seal3 / Run3 / policy-derivation3 | Covered | composition §7; replay remint |

Budget preflight formula, output-bound operational failure, and absent/unknown/incomplete/operational distinctions: **covered** (composition §3, §8; fault contract; enumeration §6). Do not collapse them.

---

## 7. Independent controls vs competing constructions

Discriminating controls that do **not** depend on reference goldens:

1. **Same-count, different-ref proof.** Two reconstructions with equal verdict, equal finding count, equal witnessDigest, and different `predicateProofs[].inputRefs` or `executionDeficiencies[].inputRefs` must disagree on `C(proof)` (composition §7). Selected-field compare is not replay. P7 correctly withdrew COMPLETE49’s projection. That withdrawal is preserved.

2. **Schema-only vs whole-Run.** Schema-only accepts claimed 2-ref `predicateProof.inputRefs` and root 8-ref equally. Whole-Run still does not pick one until the derivation table exists.

3. **Failure-class control for executionDeficiencies.** Independently admit inventories and Coverage accounts from ExecutionInputs + retained bytes. If clones-fact inventory `state=complete` and a syntax/literal account is incomplete, §4 inventory-digest law does **not** apply; §5 Coverage refs do. P7’s syntax-data inventory convention is this control. This session did not re-admit that export’s bytes (not in the granted corpus).

4. **Uniqueness control.** Two required Coverage records with different carriers must yield two proof deficiencies after `canonical-set`. Mapping that leaves only `{execution-inputs}` collapses them. Kit forbids that collapse.

5. **Source/cause allOf control.** `source=native` + `cause=required-cell-unsatisfied` is schema-invalid. `source=execution` + `cause=coverage-unknown` is schema-invalid. Claimed `source=native` is only lawful with a native-registry cause, which the diagnostic does not show.

6. **Redundancy control.** If every atomic `inputRefs` equals `evaluationInputRefs`, mutating an unused other-cell inventory already changes `evaluationInputRefs` and therefore `C(proof)`. Per-node `inputRefs` then add no discriminating power. That is an argument **against** treating construction B as necessary for complete-proof replay, and **for** stating A explicitly.

---

## 8. P7 self-audit, critically

Preserved and agreed as far as they go:

- Successor scoped verdict `FOUR_RUNS_REFUSED`.
- Rust `FOUR_RUN_FULL_ADMIT` **withdrawn**. Diagnostic later `C(proof)` equality and reminted `run3:9032d3b0…` matching **does not** restore FULL_ADMIT. Composition §7: input admission precedes replay; hashed inventories/extents do not self-certify. First refusal `ENUMERATION_MEMBERSHIP_SNAPSHOT_COVER` (`#/Cargo.toml`, `#/a/Cargo.toml`, `Cargo.lock`) remains.
- TypeScript first refusal `IMPORT_PRODUCER_KIND` preserved; producing `notReached`.
- Rust-partial original rule-outcome mismatch preserved as diagnostic; first refusal now earlier membership/extent. `notReached` on producing is preserved as the first refusal.
- Original COMPLETE49 `_proof_compare` was a projection (verdict, selected predicate fields, sorted cause pairs, copied claimed `evaluationInputRefs` / `executionPlanId` / …). Counts/selected fields/witnessDigest are not complete-bundle comparison. Original `proofCompare: []` exceeded coverage. That withdrawal stands.
- Original enumeration compared inventory rows to **claimed** `binding.extents`. Enumeration §5 / file-kind extent law requires independently remaining first-party snapshot paths. Original never joined `C(UnitMembershipV1)` or snapshot cover (§8). Withdrawal stands.
- Whole-134-consumer ACCEPT not claimed. No product qualification. `R-RUN-SYNTAX-CODE` still not in these four exports.

**Not agreed:**

- Syntax-data successor `FOUR_RUN_FULL_ADMIT` re-earned “on complete C-equality” is **not** kit-unique reconstructability. Root independently recomputed different `executionDeficiencies[0].source/inputRefs` and `predicateProofs[0].inputRefs`. P7 obtained claimed bytes by deriving expected `executionDeficiencies.inputRefs` from clones-fact `inventoryDigests` under §4. That is P7’s convention unless P7 also independently showed the clones-fact inventory was the unsatisfied required work. Full `C` of a self-derived expected proof is circular if the expected fields are not kit-unique.
- Root reference bytes are **not** an oracle. Root’s 8-ref `predicateProof.inputRefs` and Coverage+ExecutionInputs deficiency refs are the excluded replay/input-model convention, including the prepend and always-`source=execution` bugs.
- Therefore syntax-data remains **DIAGNOSTIC** for proof-field uniqueness even if P7’s producing joins on membership/extent/package parse are otherwise sound. This does not restore the withdrawn original FULL_ADMIT basis; it also does not accept the successor FULL_ADMIT as frozen.

---

## 9. Pilot symbol census (do not treat as missing design)

Pilot run `run3:4b58935ae046…`, refusal `EVALUATOR_EXECUTION_INPUTS_JOIN:EXECUTION_INPUTS_OUTCOME_DERIVE`. Claimed syntax cell `state=complete`. Independently, `literal@syntactic` account has `accountState=incomplete`, `censusMissing=["function:add"]`, while the Coverage entry itself is `coverage=complete`. Execution-inputs §5 already requires every expected source subject of the relation subject-kind (`source-path` / `package-name` / `symbol`) to be in some returned partition. Enumeration §9 does not forbid that compare. Checker exemption of symbol census is an existing-law omission. Not a missing proof-output field. Not a reason to invent a new evaluator.

---

## 10. Reference corrections (for Codex; not applied here)

1. Stop emitting `native-work-incomplete` / `unsupported-typed` as `evaluation-deficiency.cause`. Map through the closed registry (table in §4.4).
2. Stop using `row.deficiency` as proof `cause`. Keep native `DeficiencyV2` on the account/outcome; proof `cause` is the registry member.
3. Stop forcing `source=execution` for native-account failures. Native-registry causes require `source=native`.
4. Stop prepending the ExecutionInputsV1 ref onto deficiency `inputRefs`. Keep original Coverage/inventory/candidate refs so canonical uniqueness is real.
5. Stop stamping `normalized['evaluationInputRefs']` onto every atomic `predicateProof.inputRefs` and most atom deficiencies. Use the same consulted-set discipline already used for `scopeIds` / witness `coverageIds`, including empty owed inputs.
6. Do not ignore `atom_model` consumed refs; also do not treat consumed-hits as complete. Align atom return, scanner, and composition on one table.
7. Fix semantic-evidence `importIds` description: evaluated subset is **not** `proof.evaluationInputRefs`.

Do not duplicate native extraction in the evaluator. Do not add cellOrdinal onto `evaluation-deficiency`.

---

## 11. Implications for current consumer grades

| Export / grade | Implication |
|---|---|
| COMPLETE49 original rust FULL_ADMIT | Stay withdrawn |
| COMPLETE49 original syntax-data FULL_ADMIT basis | Stay withdrawn |
| P7 rust producing `ENUMERATION_MEMBERSHIP_SNAPSHOT_COVER` | First refusal stands |
| P7 TS `IMPORT_PRODUCER_KIND` | First refusal stands; producing `notReached` stands |
| P7 rust-partial | First refusal membership/extent stands; ruleResults C mismatch remains diagnostic |
| P7 syntax-data successor FULL_ADMIT | **Not accepted here** as kit-unique complete-proof reconstructability; producing joins may still be independently sound; proof-field C match used a convention |
| Pilot symbol census fail | Existing-law checker omission; not a design miss |
| Any consumer that copied claimed `evaluationInputRefs` into computed proof | Still invalid under composition §7 |
| Schema-only validators | Cannot certify unique complete proof |

No whole-kit ACCEPT. No implementation authorization. No automatic agreement with root or with P7.

---

## 12. Proposed kit edits

Exact small tables/paragraphs: `proposed-proof-field-derivation.patch.md`. They state field derivation that the contracts already intend (original typed causes, exact supporting roots, empty-population retention, canonical uniqueness, ExecutionInputsV1 at proof level). They do not add an alternate evaluator or native extraction rules.

Until those bytes are in the published kit, complete evaluator3 proof is **not** uniquely reconstructable from the normative-only kit.
