# Complete evaluator composition — contract v3

This appendix is incorporated by product identity-and-evidence §4. Acceptance and implementation readiness are recorded separately. The scope here is the closed declarative policy evaluator; native extraction and candidate-only clone producers retain their own contracts. Enumeration and atom appendices provide the input population and exact atom laws. Their retained inputs are inputs to this composition, never expected output supplied by a provider.

## 1. Explicit version dispatch and input binding

`identity-schemas.v3.json` owns the new evaluator output profile. Changed H domains are finding3, proof3, evidence3, seal3, run3 and policy-derivation3. New subject3 identifies `{schemaVersion:3, universe, kind, nativeSubjectId}`, with packageManifestPath REQUIRED additionally for kind=package and forbidden otherwise. Native package names can repeat across first-party manifests in one universe; this path distinguishes their evaluation coordinates without inventing a native ID. Package fact source binding compares both packageName and manifestPath. Incoming package attribution must distinguish the manifest or remain unknown; a name alone cannot select among duplicate packages. Native H identities, snapshot2, closure2, import2, plan2, scope2, fact2, coverage2, view2, exec-plan2 and finding-key2 retain their recipes and record shapes. A changed parameter/schema value changes ancestor identity normally; unchanged record shape does not require relabelling its domain. Explicit version dispatch must reject mixed output-major graphs. Never stamp historical outputs with new prefixes or accept them as new proofs.

Exactly one EnumerationPlanV1 and one EvaluatorEmissionPlanV1 parameter are required for this evaluator. `analysis-spec.parameters` names exact document bytes and C(payload) bytes. Neither parameter contains PlanId or analysisSpecDigest. The emission parameter names the independent resolved policy digest and one binding for EVERY policy rule. `ruleId`, contributionId, ruleStableId and semanticsMajor equal policy. Its detectorClosure is a selected closure of kind detector. A provider or evaluator closure cannot stand in for it. The evaluator does not infer an undocumented closure-to-contribution manifest lookup: the explicit binding is part of the committed Plan. Changing it changes Plan.

Emission profile declarative-subject-v1 uses path-stable logical correspondence. Other detector families may introduce their own reviewed emission profiles; they may not masquerade as this profile. PolicyDocumentV2 (schemaMajor2) and RuleProgramV2 (schemaVersion2) add the atom endpoint and typed test filters. WaiverSetV1 and ScopeDocumentV1 retain their original owner document and bytes. Predicate-witness is canonical-record schemaVersion3, without an H prefix. Program predicate addresses retain their existing closed grammar and exact policy digest joins. The fingerprint namespace `(ruleStableId,semanticsMajor)` must be unique across all emission rows, including disabled rules. Per-row requiredForEvaluatorMajors=[3] enforces the two required parameters; the generic class zeroIsLegal law remains for other consumers.

The proof requires `executionInputsDigest`, the raw SHA-256 of the exact retained
`ExecutionInputsV1` canonical record. `evaluationInputRefs` equals its selected
references plus that one manifest reference. Reconstruction re-admits stage
receipts, expected inventories, native work accounts, candidate returns and
selected imports before composing outputs. Required execution deficiencies
retain original typed causes and input references, including when policy rules
are disabled. Physical store inventories and operational retention receipts are
excluded from this semantic record and from Run identity.

## 2. Independent population and enumeration

Build the expected inventory locator set from the committed enumeration parameter, before inspecting any fact, Coverage, finding or witness. Require every listed outcome exactly once, including unavailable and complete-empty outcomes. Admit their producer/Plan/context/universe/membership/extent joins using the enumeration appendix. A missing expected outcome is an incomplete retained graph, not an empty population.

For an enabled rule, select every admitted program of the rule's portable universe domain and required primary subject kind (export means symbol plus exported status). The closed policy universe token map is typescript→native.semantic-universe.typescript.v2, rust→native.semantic-universe.rust.v2, syntax→native.semantic-universe.syntax.v2. Unknown tokens refuse admission; historical illustrative tokens such as typescript-v2 are not additional implicit aliases. With no covering program binding for a rule domain/kind, its enumeration is incomplete with no-covering-program, never inferred complete-empty. Default recommendation resolves applicability when constructing policy; it does not silently disable an already committed enabled rule. Apply include/exclude to logical path, never opaque native IDs. Include absent or [] means all paths; exclusion wins. If the existing ScopeDocumentV1 parameter is selected, intersect its include/exclude globs as well; this is distinct from foundation plan.scopeDigest. Missing ScopeDocumentV1 is legal for ordinary analysis; baseline/comparison preserve their explicit selection requirement. Complete-empty requires a covering available binding, a complete expected inventory, and selection of zero subjects. A missing expected inventory pointer is structural refusal, not a manufactured unavailable outcome. Union duplicates only for the SAME `(universe,kind,nativeSubjectId)` (plus package manifest path for packages) after exact attribution/projection agreement. Distinct universes never merge. Source language is row attribution and can differ from engine domain.

For export selection, exported rows are selected; not-exported rows are excluded; unknown rows enter unresolvedSubjectIds without being evaluated as definitely exported. Partial/unavailable inventory belongs to incompleteInventoryRefs even if it has zero rows. Known rows of a partial inventory are still evaluated. Each rule retains selected, unresolved, relevant inventories and incomplete inventories as `rule-enumeration`. A disabled rule retains state disabled and empty arrays, emits no predicates/findings, and has outcome disabled. This does not delete independent required execution obligations.

## 3. Exact traversal, bounds and proof

Evaluate the entire predicate tree postorder for every selected subject, retaining every node; do not omit branches after a short-circuit value. Address node p and children by the existing program-predicate address law. Boolean witnesses have kind boolean, children exactly the grammar's immediate child addresses, and empty fact/import/Coverage match arrays. Atomic witnesses have kind native-atom or imported-atom, no children, countLimit only for count-at-most, and exact matching/uncertain evidence and deficiency sets from the atom appendix. All input references are direct retained roots or members of an evaluated view as the identity closure permits; witnesses cannot add roots.

Truth is strong Kleene: not reverses true/false and preserves indeterminate; and is false if any child false, true iff all true, otherwise indeterminate; or is true if any child true, false iff all false, otherwise indeterminate. Atomic known matches are preserved despite unrelated incomplete coverage: exists with known match is true, none with known match is false, count-at-most with known distinct count greater than the bound is false. The remaining cases require the atom-specific completeness law. all-covered assesses the requested rung and applicable native/import coverage, not a generic resolved-only bit.

Retain all deficiency provenance in witnesses even when a known value dominates it. Root-indeterminate gating relevance is computed separately: for an indeterminate and/or node only its indeterminate children contribute blocking causes; a determinate root has no truth-blocking cause. Enumeration and required execution deficiencies remain independent of truth. Optional imported evidence can leave a root indeterminate with disclosure but does not acquire gating authority solely because none or not was used.

A deterministic full-scan budget preflight is a semantics-preserving bound. Let S be selected subjects over enabled rules, N(r) all tree nodes, A(r) atoms, F all distinct input facts, I all imported observation addresses (whole-test execution is one address), K all Coverage records, and E total inventory rows plus expected inventory locators. Charge E + sum over (r,s) of [N(r) + A(r)*(F+I+K)] work units. Use checked unsigned 64-bit arithmetic, no host timing; any intermediate overflow is budget-exceeded. Unresolved and unseen subjects are never evaluated later under this charge: known selected subjects are the entire actual evaluation set, and independent population uncertainty remains retained. No late population addition under the same proof is permitted. This upper bound is independent of findings, values and optimization. If greater than Plan budget, produce explicit budget-exhausted output before node evaluation: empty predicates/findings, actual enumeration records, per-enabled-rule indeterminate outcomes where gating, and an execution budget-exhausted deficiency. Known rule matches are not claimed when never evaluated. Disabled rule records remain disabled. Optimization may use fewer actual scans, but cannot change this reference admission/result. Array/C-byte output bounds are separately enforced; overflow refuses with EVALUATION.OUTPUT_BOUND_EXCEEDED / OUTPUT.SERIALIZATION_FAILED (operational-failed, faultCause=output-serialization), never truncation or a successful empty Run.

## 4. Finding emission and correspondence

For each subject with emitWhen=true emit exactly one full finding3 occurrence. Distinct selected universes keep distinct subject3 IDs and findings. messageCode is the rule's value if present, otherwise ruleId. The rule emission binding supplies detectorClosure; severity is the resolved rule severity. The finding's explicit ruleId disambiguates multiple policy rules sharing a detector contribution.

The declarative-subject-v1 parameter record is `{schemaVersion:2,messageCode,parameters:{ruleId,subjectPath,qualifiedName,subjectKind,subjectLanguage,matchingFactCount,matchingImportCount}}`. Counts are distinct union of all descendant atom known matches, including branches whose truth did not control the root; counts never include uncertain matches. EvidenceRefs are exactly the root predicate-witness digest; every descendant known and uncertain fact; every descendant witness Coverage id (consulted, and allowed to be narrower than evaluationInputRefs); every descendant matching/uncertain observation importId; and every evaluationInputRefs member with domain=import (under whole-selection this equals the Plan import set). Observation addresses themselves remain on the witness. Enumeration and execution inventory refs remain on the proof. See §9.7. Full replay recomputes every value and citation. This fixed emission profile does not claim to reconstruct arbitrary third-party detector parameter templates.

File/package discriminator is SHA256(C([])); their qualifiedName is admitted path/package name. Symbol uses this detectorClosure's nonempty ordered signatureTokens. Collision class is `(universe,subjectLanguage,kind,path,qualifiedName,detectorClosure)` across the independently enumerated population, not merely subjects which emitted. Identical projected signatures among distinct native IDs, empty/missing projection, anonymous unavailable name, or incomplete collision-class population cannot establish stable correspondence. Duplicate observations of the SAME subject3 are not a collision. Across distinct universes, independently equal logical descriptors may yield one stable fingerprint.

Stable fingerprint descriptor remains finding-key2 with ruleStableId, detectorSemanticsMajor, subjectKey and empty relatedSubjectKeys for this unary declarative emission profile. Its key excludes universe. Related subjects are not invented from arbitrary predicate matches. Clone grouping/candidate producers retain their separate relation/projection contracts; no semantic similarity claim is introduced here.

**Unmatched occurrences remain findings.** finding3 carries nullable fingerprint plus correspondence state matched|unmatched and a closed reason. Matched requires nonnull admitted finding-key2; unmatched requires null. Both retain subject3, ruleId, path/language/kind/name, parameters/severity/citations and can fail an ordinary current-Run gate. A missing stable key does not turn a known policy violation into pass. No encounter-order/body-hash surrogate is labelled stable. Unmatched correspondence is disclosed and cannot satisfy a fingerprint-target waiver; exact `(ruleId,subjectPath)` waiver may apply normally. Unknown export membership is not an unmatched occurrence because it was never definitely selected.

## 5. Waiver and verdict composition

Consume ONLY the effective WaiverSet bytes committed by Plan. Trust-clock expiry and duplicate target rejection were already resolved at Plan construction; replay does not read today's clock. An occurrence is waived iff any effective target equals its nonnull fingerprint or equals its exact `(ruleId,subjectPath)`. Preserve waived findings, list exact waivedFindingIds in proof, never remove their evidence. A waiver does not cure unknown subject population, unknown predicate truth, correspondence uncertainty needed by a comparison, or required execution failure.

A rule gates iff enabled AND gate=true AND severity >= policy.gateSeverityAtLeast, with note<warning<error. A live unwaived finding for a gating rule makes its outcome fail. Otherwise a gating rule is indeterminate if its population is incomplete/unresolved or its root truth is indeterminate with at least one blocking native or required imported cause. Optional-only root unknown remains disclosed with rule outcome pass. An advisory rule's outcome is pass even if it retains findings/deficiencies. Required import obligations are assessed according to declared evidenceUse independently of a boolean branch suppressing their use; no undeclared import acquires authority. Disabled remains disabled.

Required execution cells contribute independent executionDeficiencies even with all rules disabled or empty populations. Operational provider protocol violations remain invocation failure under the existing operational dominance law; they are not converted to semantic unknown. Among admitted semantic results, any gating rule fail wins; otherwise any gating rule indeterminate or required execution deficiency produces indeterminate; otherwise pass. Sealed verdict has only pass|fail|indeterminate. Surface advisory is a derived display for pass with live advisory findings. Each ruleResult includes all its emitted finding IDs and complete deficiencies, not just failing findings.

## 6. Baseline, comparison, repair and surfaces

For matched findings, group by fingerprint only AFTER byte-equal logical descriptor verification. Compute every BaselineEntry field from each occurrence's explicit rule/emission binding and waiver state. All fields, including optional legacyFingerprint presence/value, must agree. Legitimately different message/parameters/citations remain on the original findings and are not compared for baseline equality. Conflicting baseline projections refuse; no first/last writer wins. Comparison pivot presence is any admitted matched occurrence at that pivot, and waived presence is the unanimously projected baseline state. Existing default/current-only audit-profile gates still decide whether a new waiver suppresses code-net-new.

Unmatched findings are excluded from the stable-entry array but MUST be retained in an explicit unmatched-occurrences array with findingId, ruleId, subjectId, subjectPath, severity and waived. A baseline cannot silently claim a complete correspondence population when that array or enumeration uncertainty is nonempty. Comparison reports a correspondence deficiency for affected gating rules and does not classify unmatched records as resolved, unchanged or code-net-new by guesswork. Known comparable regressions still fail. An unwaived unmatched gating occurrence fails current analysis, while audit can only report correspondence-indeterminate for it; it must not guess CODE-NET-NEW. Path-waiving the occurrence can make current analysis pass while audit remains correspondence-indeterminate. Missing fingerprint-only waiver matches cannot suppress unmatched occurrences. Baseline artifact2 and comparison result2 carry this addition; historical artifacts do not silently acquire an empty-array assertion. Fingerprint-targeted repair/review requires a stable matched target; unmatched findings stay inspectable by findingId and receive an explicit target-correspondence-unavailable refusal for fingerprint-targeted actions. No automatic source edit is authorized by this design work.

Command envelopes and SARIF retain one result per finding3, including separate configurations and unmatched occurrences. SARIF can use findingId as run-local identity; only matched findings carry stable partialFingerprints. Baseline aggregation must never silently deduplicate visible finding occurrences. A renderer cannot turn indeterminate into pass.

## 7. Complete replay criterion

An independent evaluator receives admitted input closure and constructs every output from scratch: subject descriptors; per-rule enumeration; all program-predicate descriptors and witnesses; every predicate proof; matched fingerprint descriptors and full findings/parameter bytes; unmatched records; waiver membership; rule outcomes/deficiencies; execution deficiencies; full proof; evidence, seal, policy derivation and Run IDs. It may not read claimed findings/witnesses to select subjects, parameters, citations or output IDs. Input admission precedes replay; hashes alone do not establish owner admission.

Compare C of the COMPLETE recomputed proof and every referenced output preimage and H identity with retained claims. Check exact reachable output-set equality so extra unreferenced semantic outputs cannot masquerade as evaluated findings. Counts, selected predicate fields, final verdict, or existence of a recomputed digest alone are insufficient. Discriminating controls must mutate same-count parameter values, citations, severity, waiver membership, enumeration, imported address and findings, independently remint all enclosing identities, and show semantic replay refusal rather than merely a stale hash. Positive graphs must retain the normative schema and all native principal/input bytes, admit under the actual owner closure, then pass complete replay. Report separately bounded shape/unit checks, complete graph admission and complete semantic replay.

## 8. Source-specific deficiency and public fault accounts

The schema's evaluator-deficiency-registry is closed by source and exact cause. Every import deficiency carries evidenceKind (the atom/declaration's actual kind) even when no wrapper exists; a missing import pointer is not needed to identify which required declaration it failed. Other sources carry evidenceKind=null. NativeCause is a separately typed nullable owner carrier and cannot widen DeficiencyV2. Required-execution `inputRefs` are the canonical set of the ExecutionInputsV1 ref plus each originating Coverage, inventory, or candidate ref from the internal requiredCellDeficiencies row, as specified in §9.6. Atom, enumeration, correspondence and required-import deficiency `inputRefs` follow §9.5. All non-null subject/predicate addresses belong to this rule's independent evaluation; cell-level execution deficiencies have null addresses. Required/optional relevance is derived from policy; no gating flag is accepted in a deficiency. The origin is recomputed during replay, not inferred from text prefixes.

EVALUATION.WORK_BUDGET_EXHAUSTED is an indeterminate semantic disclosure with remedy to raise/narrow the admitted analysis work budget. It is separate from a native provider cell budget-exhausted carrier. EVALUATION.OUTPUT_BOUND_EXCEEDED is operational with OUTPUT.SERIALIZATION_FAILED, never HOST.IO_FAILURE. Owner-profile parameter selection errors and unknown policy tokens are caller CONFIG.INVALID / REQUEST.PRECONDITION_FAILED as individually registered. A absent expected retained pointer, lost bytes behind a valid pointer, and supplied invalid bytes have separate input-graph/retention/admission routes. They are not semantic unavailable inventory states. The concrete route registry must identify caller configuration, retained-input and producer/output phases, because the same schema defect in caller configuration and host-generated output has different operational meaning.

Workflow output namespace3 uses Run3/Evidence3/Finding3 and explicit baseline2/comparison2/review2/query2 schema dispatch. Historical profile2 is preserved and cannot be read as an empty unmatched-population assertion. Fingerprint2 and unchanged native/input identities retain their exact owners. The workflow projection appendix owns the full schema map and surface parity checks.


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
- **Boolean node** (`and` / `or` / `not`): `inputRefs = Cset(union of immediate children's `inputRefs`)`. With the atomic rule above this equals `EI`; the union algorithm is still the boolean law (this profile's atoms emit `EI`).
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
| relevant inventory `state≠complete` | `enumeration` | `incomplete-inventory` | null | null | `[{domain:subject-inventory, digest:SHA-256(C(inventory))}]` | null | inventory `nativeCause` | null |
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

1. Every atom `causes[]` member must have its `code` in the registry for `plane` and its `evidenceKind` equal to the atom evidence kind on the import plane, null otherwise; disagreement refuses admission (`EVALUATOR_ATOM_CAUSE_UNREGISTERED` or `EVALUATOR_ATOM_CAUSE_PLANE_JOIN`), never silently drops the cause. For each admitted member emit `{source:plane, cause:code, subjectId: this subject3, predicateId: this address, inputRefs: atomEI, evidenceKind: node.evidence if plane=import else null, nativeCause: cause.nativeCause, universe: cause.universe if present else null}`. Import `evidenceKind` must equal the atom's evidence kind.
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
| Required enumerator unselected or binding `universe=null` | binding `UnavailableProgramBindingV1.deficiency` | `[]` for this binding/enumerator item. Each non-complete same-cell inventory contributes a separate inventory item with its own deficiency, nativeCause and single inventory ref as above; never attach those inventory refs to the binding carrier. |
| Required candidate envelope `partial` or `unavailable` | candidate `deficiency` | `[{domain:candidate-producer-result, digest: envelope digest}]` |
| Required native account not complete, Coverage records exist | each Coverage `entry.deficiency`, or if null the account summary `deficiency` (empty returned partitions use `provider-unavailable`) | `[{domain:coverage, digest: that Coverage H suffix}]` **per Coverage record**. Keep every Coverage of that account. Missing expected subjects (`source-path` / `package-name` / `symbol`) still emit per returned Coverage record with that summary `deficiency`. |
| Required native account not complete, no Coverage records | account summary `deficiency` (`provider-unavailable` when empty) | `[{domain:coverage, digest: hx} for hx in the account's named coverageIds]` (empty if none named) |
| Required unsupported-typed matrix cell | matrix cell `deficiency` | `[]` (no fabricated Coverage) |
| Required unavailable-unselected / unavailable-null-universe account | binding `deficiency` | `[]` |
| Inapplicable-VCS | (not required-unsatisfied; no row) | — |

Sibling source records and `nativeCause` pairs stay with their originating refs. Two Coverage of the same relation with different carriers remain two internal rows and two proof items because their Coverage digests differ.

**Internal full-coordinate uniqueness vs proof-record uniqueness.** Internal `requiredCellDeficiencies` are unique by `C` of the whole internal row, which includes `cellOrdinal`, `programOrdinal`, `relation`, `resolution`, `capabilityId`. Proof items have no those coordinates. Proof `Cset` uniqueness is of the evaluation-deficiency record in §9.6 steps 1–7. When two internal rows bridge to **byte-identical** proof records they carry identical proof-level information (same cause, carrier, universe, and same `XI` plus originating refs). Distinct cell/relation coordinates remain on hashed `ExecutionInputsV1.nativeCoverageAccounts` and `cellOutcomes`. Example: two unsupported-typed relations on one required cell with the same matrix `DeficiencyV2`, same `nativeCause`, same universe, and empty originating refs bridge to one proof item; both accounts remain on ExecutionInputsV1.

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


## Retained input selection and complete replay

`evaluator_input_model.v3.py` reconstructs the composition inputs using the native/schema/identity owner's admitted closure. It reads no claimed finding, witness value or verdict. Every selected Plan import is an evaluation input, including a wrapper whose scope has no matching subject; omission is structural. A non-null ImportObservation member must agree with the same claim in its canonical payload: runtime window/population, test selection, history range endpoints. Observation kind must equal wrapper kind, and members inapplicable to that kind are null. Null is undisclosed information; it is not a contrary positive assertion and is never filled with a fictional observation. The canonical payload remains the owner of its own declared selection/range/window.

Each atom is evaluated against the complete admitted evaluation input selection, retaining availability and empty-population inputs as well as hits. `predicate-witness` has no `inputRefs` field. That complete selection is projected onto every atomic `predicateProofs[].inputRefs` as specified in §9; boolean nodes take the canonical union of immediate children. Atom-model consumed-ref subsets are not evaluator3 proof fields. Coverage deficiencies retain their original native cause and source universe. Inputs are immutable preimages; a retained native extraction assertion remains provider evidence, and replay does not rerun a compiler to establish extraction truth.

`evaluator_replay_model.v3.py` first admits the retained owner graph, reconstructs inputs, invokes the actual atom scanner and composes complete outputs. It compares every recomputed proof field and every output object/blob preimage, then independently reconstructs semantic evidence, seal and Run. It compares full finding identities, message/parameter bytes, severity, citations, waivers and enumeration outcomes, not counts. The authoritative evidence view set equals selected view inputs; its coverage set is the union of those views' coverage plus explicit admitted coverage inputs. Additional retained unreachable objects do not become authoritative findings.

The synthetic reference harness uses a temporary graph only to open the legacy owner closure, whose API is Run-based. Its provisional outputs are discarded as semantic answers: reconstruction uses only Plan, execution and retained inputs. The exported positive Run is newly composed and must pass complete replay. Real extraction and platform qualification remain separate required work.

The public `identity-model.v3.close_run` boundary invokes complete replay. Storage preparation/restoration and cache admission against an authoritative Run inherit that stronger check. `open_run_closure` is an internal owner-admission primitive; calling it alone is not a claim that evaluator3 output is correct. Intermediate cache-key construction remains possible before a Run and grants no authority.

Every explicit coverage input must also belong to a selected admitted view, so the owner's coverage producer-admission and unresolved-edge accounting have run for it. A coverage wrapper by itself is not a substitute for that native view admission. The normalized scanner receives exact import wrappers plus separately derived import-scope and current/consumable maps from owner admission; those are host projections, not caller-supplied result flags.
