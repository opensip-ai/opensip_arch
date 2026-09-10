## 9. Proof and evidence output field derivation

This section is the normative field mapping from admitted inputs to evaluator3 proof, witness, finding, evidence, seal, Run and policy-derivation bytes. It publishes the current intended bridge. It does not add an evaluator profile, change native extraction, Kleene, gates, the budget formula, or output identity recipes. Reference models remain reconstruction evidence; a normative-only consumer reproduces the fields below without reading those models.

**Notation.** `C(x)` is product canonical UTF-8 JSON (`canonical.py`: sorted keys, compact separators, exact typed JSON). `Cset(X)` is the unique members of X keyed by `C(member)`, ordered by those canonical bytes. That is schema `uniqueItems` plus `x-opensip-order: canonical-set`. `ProofInputRef` is `{domain, digest}` with `digest` a 64-hex and `domain` a member of `#/$defs/ProofInputRef/properties/domain/enum`. H prefixes are stripped from `digest` (the 64-hex is the suffix). Let `EI` be `proof.evaluationInputRefs`. Let `XI` be the unique `ProofInputRef` in `EI` with `domain=execution-inputs`.

### 9.1 Proof identity and selection

| Field | Exact bytes |
|---|---|
| `schemaVersion` | `3` |
| `planId` | admitted Plan H (`plan2:` + 64-hex) |
| `executionPlanId` | admitted execution-plan H (`exec-plan2:` + 64-hex) |
| `evaluatorClosure` | the Plan-selected closure of kind `evaluator` |
| `executionInputsDigest` | raw SHA-256 of `C(ExecutionInputsV1)` of the unique retained execution-inputs blob named by `XI` |
| `evaluationInputRefs` | `Cset(ExecutionInputsV1.selectedRefs ∪ {XI})`. Forbidden members: proof-bundle, finding, evaluation-seal, run, semantic-evidence. Every Plan `importIds` member appears as `{domain:import, digest:suffix}`. |
| `ruleProgramDigest` | raw SHA-256 of `C(RuleProgramV2)` where RuleProgramV2 is `{schemaVersion:2, policyDigest: SHA-256 of C(PolicyDocumentV2), rules:[{ruleId, ruleProgramRef, emitWhen} for each policy.rules member in policy order]}`. `ruleProgramRef` is the policy object's `ruleProgramRef` (includes `programDigest`). |

### 9.2 Atomic and boolean `predicateProofs[].inputRefs` (whole admitted selection)

`predicate-witness` has no `inputRefs` field (`additionalProperties: false`). The composition sentence “each atom's witness binds the complete admitted evaluation input selection, retaining availability and empty-population inputs as well as hits” **projects** onto `predicateProofs[].inputRefs` as follows.

- **Atomic node** (`exists` / `none` / `count-at-most` / `all-covered`): `inputRefs = EI` (the complete admitted evaluation input selection). This is the evaluator3 profile output field. It is not the atom-model internal consumed-ref subset (`evaluate_atom.evaluationInputRefs`, Coverage ids actually scanned). Those internal arrays are not proof fields and are not a second profile.
- **Boolean node** (`and` / `or` / `not`): `inputRefs = Cset(union of immediate children's `inputRefs`)`. With the atomic rule above this equals `EI`; the union algorithm is still the boolean law (so a future atomic subset would union, but this profile's atoms emit `EI`).
- Witnesses cannot add roots outside `EI`.
- **Not hits-only.** Empty owed imports, empty inventories, and unused Coverage remain members of `EI` and therefore of every atomic `inputRefs`.
- Optimization or physical scan order MUST NOT change `inputRefs`. Whole-selection is the stable semantic-ID discriminator.

### 9.3 Witness fields that may be narrower

These are consulted evidence, not a second input-selection law. They may be a proper subset of `EI` without contradiction.

| Witness field | Atomic | Boolean |
|---|---|---|
| `kind` | `native-atom` or `imported-atom` from the atom plane | `boolean` |
| `matchingFactIds` / `uncertainFactIds` | `Cset` of atom known / uncertain fact2 ids; imported-atom empty | empty |
| `matchingImportRows` / `uncertainImportRows` | `Cset` of atom known / uncertain `ObservationAddressV1`; native-atom empty | empty |
| `coverageIds` | `Cset` of Coverage H ids the atom completeness/matching law returned | empty |
| `scopeIds` on **predicateProof** (not on witness) | `Cset` of scope2 ids the atom completeness law returned | `Cset` of union of children's `scopeIds` |
| `countLimit` | node `n` if `count-at-most`, else null | null |
| `childPredicateIds` | empty | `Cset` of immediate child addresses from the program-predicate address law |
| `programPredicateDigest` | raw SHA-256 of `C({schemaVersion:2, ruleProgramDigest, ruleId, predicateId, operation, nodeDigest})` with `nodeDigest` = raw SHA-256 of `C(the Predicate node)` and `operation` = node `op` | same |
| `schemaVersion` | `3` | `3` |
| `deficiencies` | `Cset` of evaluation-deficiency records in §9.5 | `Cset` of union of children's `deficiencies` |

Uncertain matches and deficiencies are retained even when a known value dominates. Root-indeterminate blocking causes are computed from indeterminate children's deficiencies for gating; they are not a stored field.

### 9.4 Predicate-proof population, order, value

If the budget preflight of §3 exceeds Plan budget: `predicateProofs=[]`, `findingIds=[]`, `evaluationState=budget-exhausted`, and §9.6 emits the execution `work-budget-exhausted` item. Disabled rules emit no predicate proofs.

Otherwise, for every enabled policy rule and every `selectedSubjectIds` member, evaluate the entire `emitWhen` tree postorder. One `predicateProofs[]` item per node:

| Field | Bytes |
|---|---|
| `ruleId` | the policy rule id |
| `subjectId` | subject3 of that selected subject |
| `predicateId` | program-predicate address (`p`, `a.i`, `a.0`) |
| `operation` | node `op` |
| `inputRefs` | §9.2 |
| `scopeIds` | §9.3 |
| `value` | Kleene / atom determinate-evidence law of §3 and identity-and-evidence §4 |
| `witnessDigest` | raw SHA-256 of `C(predicate-witness)` |

Array order: `x-opensip-order: predicate` = strictly increasing UTF-8 tuples `(ruleId, subjectId, predicateId)`.

### 9.5 Witness and ruleResult deficiencies (non-execution)

Each evaluation-deficiency is `{source, cause, subjectId, predicateId, inputRefs, evidenceKind, nativeCause, universe}` with closed source×cause membership. `Cset` uniqueness is of that whole record.

**Enumeration** (per enabled rule; disabled rules have `deficiencies=[]`):

| Condition | `source` | `cause` | `subjectId` | `predicateId` | `inputRefs` | `evidenceKind` | `nativeCause` | `universe` |
|---|---|---|---|---|---|---|---|---|
| no inventory locator of the rule's portable domain and primary kind (`export` → symbol) | `enumeration` | `no-covering-program` | null | null | `[]` | null | null | null |
| relevant inventory `state≠complete` | `enumeration` | `incomplete-inventory` | null | null | `[{domain:subject-inventory, digest:C(inventory)}]` | null | inventory `nativeCause` | null |
| same inventory and `inventory.deficiency=source-syntax-invalid` | `enumeration` | `source-syntax-invalid` | null | null | same single inventory ref | null | null | null |
| export selection and row `exported=unknown` | `enumeration` | `unknown-export-membership` | that subject3 | null | that inventory ref | null | null | null |

Relevant inventories are every retained inventory whose `kind` equals the rule primary kind and whose cell `languageMode` maps to the rule's portable universe domain. `ruleResults[].enumeration.inventoryRefs = Cset` of those inventory refs (including unavailable). `incompleteInventoryRefs = Cset` of those whose `state≠complete`. `selectedSubjectIds` / `unresolvedSubjectIds` as composition §2. `state` is `incomplete` if any enumeration deficiency exists, else `complete`. Include/exclude globs apply to inventory `row.path`; include absent or `[]` means all paths; exclusion wins; optional ScopeDocumentV1 intersects.

**Required import (policy `evidenceUse`, enabled rules only):**

| Condition | `source` | `cause` | addresses | `inputRefs` | `evidenceKind` | `nativeCause` | `universe` |
|---|---|---|---|---|---|---|---|
| `requirement=required` and that `kind` is not among Plan-selected import wrapper kinds | `import` | `evidence-kind-unavailable` | null / null | `[]` | the declared `evidenceUse.kind` | null | null |

No import pointer is required. Optional `evidenceUse` entries emit nothing here.

**Atom-mapped (per atomic node, copied onto that node's witness and into the rule's `deficiencies`):**

Let `plane` be `import` if the atom is imported-atom, else `native`. Let `atomEI = EI` (whole selection; not the internal consumed subset).

1. For each atom `causes[]` member whose `code` is in the registry for `plane`: emit `{source:plane, cause:code, subjectId: this subject3, predicateId: this address, inputRefs: atomEI, evidenceKind: node.evidence if plane=import else null, nativeCause: cause.nativeCause, universe: cause.universe if present else null}`. Import `evidenceKind` must equal the atom's evidence kind.
2. For each atom `nativeDeficiencies[]` member (a `DeficiencyV2` from sufficiency_v2): emit `{source:native, cause:that DeficiencyV2, subjectId, predicateId, inputRefs: atomEI, evidenceKind:null, nativeCause:null, universe:null}`.
3. For each atom `coverageIds` member whose Coverage payload `entry.deficiency` is non-null: emit `{source:native, cause:entry.deficiency, subjectId, predicateId, inputRefs:[{domain:coverage, digest: coverage H suffix}], evidenceKind:null, nativeCause:entry.nativeCause, universe: Coverage key sourceUniverse}`. This overwrites only this item's `inputRefs` to that Coverage; it does not change §9.2.

Boolean nodes do not invent causes; they `Cset`-union children. Structural atom codes `omitted-selected-wrapper` / `missing-expected-inventory` refuse admission and are not semantic proof causes.

**Correspondence** (only when emitWhen is true and a finding is minted):

| Condition from composition §4 correspondence | `source` | `cause` | `subjectId` | `predicateId` | `inputRefs` | `evidenceKind` | `nativeCause` | `universe` |
|---|---|---|---|---|---|---|---|---|
| symbol missing detector projection or empty `signatureTokens` | `correspondence` | `projection-unavailable` | that subject3 | `p` | the rule's `enumeration.inventoryRefs` | null | null | null |
| collision-class population incomplete | `correspondence` | `population-incomplete` | that subject3 | `p` | same inventory refs | null | null | null |
| two distinct native ids share the projected signature | `correspondence` | `signature-ambiguous` | that subject3 | `p` | same inventory refs | null | null | null |

File/package use discriminator `SHA-256(C([]))` and do not emit correspondence deficiencies. Registry member `anonymous-subject` remains closed membership; the current correspondence algorithm classifies empty symbol tokens as `projection-unavailable`.

**Work-budget on a ruleResult** (when §3 preflight exceeds budget): one additional `{source:execution, cause:work-budget-exhausted, subjectId:null, predicateId:null, inputRefs:[], evidenceKind:null, nativeCause:null, universe:null}` on that enabled rule. Disabled rules stay disabled with empty deficiencies.

`ruleResults` has one item per policy rule, ordered by `ruleId` UTF-8. `findingIds` on the rule is `Cset` of minted finding3 ids. `outcome` follows §5.

### 9.6 `proof.executionDeficiencies` — required-execution bridge

`requiredCellDeficiencies` and `derivedAccounts` are **internal admission-result records**, not `evaluation-deficiency`. They may use internal `cause` tokens `native-work-incomplete` and `unsupported-typed`. Those tokens are **not** proof `cause` values.

**Bridge (applied to every internal `requiredCellDeficiencies` row before proof emission):**

1. `source` := `execution` (assessment layer for required execution cells; not a claim that the raw evidence provider is “execution”).
2. Let `d = row.deficiency` (the typed `DeficiencyV2` or `null` or enumeration-local `source-syntax-invalid`).
3. If `d` is a member of `x-opensip-evaluator-deficiency-registry.sources.execution`, proof `cause := d`. Else if `d` is `null` or `source-syntax-invalid`, proof `cause := required-cell-unsatisfied`. Else admission refuses `EVALUATOR_EXECUTION_CAUSE_UNREGISTERED` (not a semantic proof).
4. `nativeCause := row.nativeCause` (owner `NativeCause` or null; not unzipped from a later sibling).
5. `universe :=` that row's enumeration binding `universe` (64-hex suffix or null).
6. `subjectId` := null; `predicateId` := null; `evidenceKind` := null.
7. `inputRefs := Cset({XI} ∪ row.inputRefs)`. `XI` is committed execution-context. `row.inputRefs` are the originating Coverage, inventory, or candidate refs. `XI` does not replace them.

Every native `DeficiencyV2` member is a member of both the execution and native cause registries. Native-registry evaluator diagnostics (`uncovered-expected-source-subject`, `coverage-unknown`, …) are atom/witness causes (§9.5), not `DeficiencyV2` carriers, and are not this bridge's `cause`.

**Originating `row.inputRefs` by failure class** (internal row construction; proof refs are those plus `XI`):

| Failure class | Internal `row.deficiency` | Originating `row.inputRefs` |
|---|---|---|
| Required inventory not `complete` | inventory `deficiency` (`DeficiencyV2` or `source-syntax-invalid`) | `[{domain:subject-inventory, digest: that inventory C digest}]`. Keep every such sibling inventory of the cell. |
| Required enumerator unselected or binding `universe=null` | binding `UnavailableProgramBindingV1.deficiency` | inventories of that cell if still present as source items; otherwise `[]` |
| Required candidate envelope `partial` or `unavailable` | candidate `deficiency` | `[{domain:candidate-producer-result, digest: envelope digest}]` |
| Required native account not complete, Coverage records exist | each Coverage `entry.deficiency`, or if null the account summary `deficiency` (empty returned partitions use `provider-unavailable`) | `[{domain:coverage, digest: that Coverage H suffix}]` **per Coverage record**. Keep every Coverage of that account. Missing expected subjects (`source-path` / `package-name` / `symbol`) still emit per returned Coverage record with that summary `deficiency`. |
| Required native account not complete, no Coverage records | account summary `deficiency` (`provider-unavailable` when empty) | `[{domain:coverage, digest: hx} for hx in the account's named coverageIds]` (empty if none named) |
| Required unsupported-typed matrix cell | matrix cell `deficiency` | `[]` (no fabricated Coverage) |
| Required unavailable-unselected / unavailable-null-universe account | binding `deficiency` | `[]` |
| Inapplicable-VCS | (not required-unsatisfied; no row) | — |

Sibling source records and `nativeCause` pairs stay with their originating refs. Two Coverage of the same relation with different carriers remain two internal rows and two proof items because their Coverage digests differ.

**Internal full-coordinate uniqueness vs proof-record uniqueness.** Internal `requiredCellDeficiencies` are unique by `C` of the whole internal row, which includes `cellOrdinal`, `programOrdinal`, `relation`, `resolution`, `capabilityId`. Proof items have no those coordinates. Proof `Cset` uniqueness is of the evaluation-deficiency record in §9.6 steps 1–7. When two internal rows bridge to **byte-identical** proof records they carry identical proof-level information (same cause, carrier, universe, and same `XI` plus originating refs). Distinct cell/relation coordinates remain on hashed `ExecutionInputsV1.nativeCoverageAccounts` and `cellOutcomes`. Adding proof fields is not required unless a graph is shown where two bridged records are identical **and** existing law still requires two proof items; no such operand is admitted here. Example: two unsupported-typed relations on one required cell with the same matrix `DeficiencyV2`, same `nativeCause`, same universe, and empty originating refs bridge to one proof item; both accounts remain on ExecutionInputsV1.

**Work-budget-exhausted** (composition, not a requiredCellDeficiencies row): `{source:execution, cause:work-budget-exhausted, subjectId:null, predicateId:null, inputRefs:EI, evidenceKind:null, nativeCause:null, universe:null}` appended to `executionDeficiencies` when §3 preflight exceeds budget. (RuleResult copy of this cause uses empty `inputRefs` as in §9.5.)

`proof.executionDeficiencies = Cset` of the bridged required-cell items plus the optional budget item. Required cells still contribute when all rules are disabled.

### 9.7 Findings, evidence, seal, Run

**Finding** (one per selected subject with emitWhen value `true`; none when budget-exhausted):

| Field | Bytes |
|---|---|
| `schemaVersion` | `3` |
| `fingerprint` | finding-key2 H if correspondence succeeded, else null |
| `correspondence.state` | `matched` iff fingerprint non-null, else `unmatched` |
| `correspondence.reason` | null if matched; else the correspondence cause of §9.5 |
| `ruleClosure` | emission binding `detectorClosure` |
| `ruleId` | policy rule id |
| `subjectId` | subject3 |
| `subject` | `{language: row.subjectLanguage, kind, logicalPath: row.path, qualifiedName: row.qualifiedName}` |
| `messageCode` | rule `messageCode` if present, else `ruleId` |
| `parameterDigest` | raw SHA-256 of `C({schemaVersion:2, messageCode, parameters:{ruleId, subjectPath:row.path, qualifiedName, subjectKind, subjectLanguage, matchingFactCount, matchingImportCount}})` with counts = distinct union of descendant atom **known** matches (not uncertain) |
| `severity` | resolved rule severity |
| `evidenceRefs` | `Cset` of FindingEvidenceRef: `{domain:predicate-witness, digest: root witnessDigest}`; `{domain:fact, digest: fact2 suffix}` for every descendant known and uncertain fact id; `{domain:coverage, digest: coverage suffix}` for every descendant **witness** `coverageIds` member (consulted, may be narrower than `EI`); `{domain:import, digest: import2 suffix}` for every descendant matching/uncertain observation `importId` **and** every `EI` member with `domain=import`. Under whole-selection the import set equals Plan `importIds` suffixes. Observation addresses themselves remain on the witness, not on `evidenceRefs`. Enumeration/execution inventory refs stay on the proof, not on `evidenceRefs`. |

`proof.findingIds = Cset` of minted finding3 H ids. `proof.waivedFindingIds = Cset` of those whose fingerprint or exact `(ruleId, subjectPath)` matches an effective WaiverSet target.

**Semantic evidence3:** `{schemaVersion:3, planId, viewIds: Cset(view2:d for {domain:view,digest:d} in EI), coverageIds: Cset(coverage ids named by those views ∪ {coverage2:d for domain=coverage in EI}), importIds: Plan.importIds in Plan array order then admitted as the Plan-selected set (equal as a set to plan.importIds; schema canonical-set orders the stored array by C of each id string), findingIds: proof.findingIds, proofBundleId}`. `importIds` is the exact Plan import selection, **not** an evaluated subset and **not** `EI`. Matched/uncertain observation addresses live on witnesses. Atomic `predicateProofs[].inputRefs` may contain every selected import under §9.2 without those imports being “consulted” Coverage/observation evidence.

**Seal3 / Run3 / policy-derivation3:** existing identity recipes. Seal `verdict` equals `proof.verdict`. Evidence, seal and Run H ids are `identifier` of those descriptors. Policy-derivation3 copies `planId`, `proofBundleId`, `policyDigest`, `waiverDigest`, `verdict` from the fully replayed Run.

**Verdict / evaluationState:** §3 and §5 unchanged. Any nonempty `proof.executionDeficiencies` makes sealed verdict at least indeterminate (fail still dominates).
