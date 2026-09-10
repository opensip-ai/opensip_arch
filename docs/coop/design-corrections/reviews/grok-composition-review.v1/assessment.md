I'll critique the composition proposal against the specified source contracts only, with no edits outside this output directory. First I'll load the review guidance and the two proposal documents in full.I'll read the composition contract and emission schema in full, plus the workspace process files so the critique stays on those composition choices.Next I’ll read the parent source contracts and schemas the proposal claims to join, without scanning histories or private logs.The identity contract is longer than one read; I’ll continue it and locate the workflow schemas next.The workflow schemas aren’t at the path given; I’ll locate them under the candidate tree and keep reading the identity records that matter for composition.Workflow schemas live under the design-corrections tree. I’ll read those six files plus the successor finding/projection records needed for join analysis.I’ll pull the remaining join surfaces: payload registry, public routes, successor finding3, enumeration parameter, envelope findings, and Fingerprint.I have enough to settle the composition choices against source. I’ll write the bounded critique in this output directory and give the full findings in the final response.**Request changes.** Unmatched-as-finding with a nullable fingerprint is the right alternative to dropping findings or refusing the whole Run. The draft does not yet close the joins that stop vacuous empty populations, fingerprint collisions, or silent skipping of the existing ScopeDocumentV1 parameter. No tests were run. This is source-level design review only, not source assent.

Read in full: `evaluator-composition-contract.v3.md`, `evaluator-emission-plan.schema.v1.json`. Parent source21: identity-and-evidence, workflows-and-surfaces, identity-schemas.v2, and the listed workflow schemas. Enumeration/atom contracts were treated as foreign inputs, not authored here. Draft identity3 mismatch with frozen source21 is treated as known pending integration except where it exposes a composition hole.

---

## Settled alternatives

### Unmatched findings vs drop vs refuse-whole-run

**Keep unmatched findings**, nullable `finding-key2`, closed correspondence, and a **new baseline unmatched array**. That is coherent and superior to the two rejected alternatives:

| Alternative | Known `emitWhen=true` | Comparison | Fingerprint waiver/repair |
|---|---|---|---|
| Drop unmatched | Violations vanish; current Run can pass | Baseline looks complete | N/A |
| Refuse whole Run | One incomplete collision class voids matched file findings | No comparable subset | Matched targets cannot repair |
| Unmatched-as-finding | Live unwaived finding still fails a gating rule | Matched subset still classifies; unmatched stay out of entries; correspondence deficiency on affected gating rules | Fingerprint targets refuse; path waiver and `findingId` inspection remain |

This is superior **only if** the MUST joins land. Source already forbids the other two readings: workflows §5 emits a finding on a true predicate; identity §4 replays complete findings, not counts; incomplete native input is an indeterminate Run, not an operational voiding of unrelated matched work.

Nullable fingerprint is the correct record-shape reason for **finding/proof/evidence/seal/run/policy-derivation major 3**. Historical baseline/comparison artifacts must not acquire an implicit empty unmatched array (`schemaMajor` const 1 today).

### Path waiver vs fingerprint waiver

**The split preserves intended semantics.** Source waiver targets are fingerprint **or** exact `(ruleId, subjectPath)`. Unmatched (`fingerprint=null`) cannot satisfy a fingerprint-target waiver; path waiver still applies to the retained path.

That is existing path-waiver granularity (file-level), not a new hole. Required clarification: a fingerprint-only waiver that matches nothing because every hit was unmatched does **not** suppress those live findings; a path waiver **can** pass the current-Run gate and still leave comparison indeterminate (waiver does not cure correspondence uncertainty).

### Collision-class incompleteness vs false match

**Over-conservatism is required.** A false match would merge distinct native IDs into one `finding-key2` and poison waiver, baseline, repair, and review.

Completeness is **per collision class** `(universe, subjectLanguage, kind, path, qualifiedName, detectorClosure)`, not whole-run and not cross-kind:

- Partial **symbol** inventory → unmatched (`population-incomplete`) for every symbol class that inventory could have omitted a duplicate for.
- Complete **file**/**package** inventory still matches. `SHA256(C([]))` is the specified file discriminator, not “empty/missing projection”.
- Unknown **export membership** is unresolved, never unmatched, never a virtual `export` kind. That agrees with policy `subjectKind=export` as symbol ∧ exported, and with the projection registry’s `exportIsNotAKind`.

### Emission binding + 7 params vs custom-param / related-subject

**Explicit pre-Plan emission binding is the right shape.** Policy `ruleProgramRef` has contribution/stable/major/programDigest and **no** detector closure. Tokens come from inventory projections of a Plan-selected `kind=detector` closure. Do not infer a contribution↔closure oracle.

The 7 `declarative-subject-v1` parameters do **not** unfulfill a policy custom-parameter contract: `Rule` has no parameter template. `relatedSubjectKeys: []` is correct for this unary profile. Clone/candidate producers stay outside.

**Unfulfilled existing contract:** ScopeDocumentV1 (MUST-1). `finding-parameters` remains an open map in source; the profile must close the 7 keys at admission.

### Imports, disabled rules, budget, empty universe

- Required `evidenceUse` assessed independently of Kleene short-circuit: **accept**.
- Optional-only root unknown → pass with disclosure: **accept** as consistent with `IMPORT.ABSENT_FOR_PREDICATE`. Do not flatten unknown causes; do not give optional unknown gating authority solely because `none`/`not` was used.
- Disabled rules empty, required execution cells independent: **accept**, joined to `requestedCapabilities[].required` / enumeration `cells[].required`.
- **No covering program is not complete-empty** (MUST-2). Valid complete-empty is only: covering available program ∧ expected inventory present ∧ complete ∧ include/exclude selects zero.

---

## Findings

### MUST-1 — ScopeDocumentV1 is never consumed

Identity §3 registers ScopeDocumentV1 as an analysis-spec parameter; comparison `EvaluationContext.scopeDigest` is that document; missing selection is `BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER`. Composition selects from enumeration extents and rule globs only.

If current evaluation ignores the Plan-selected scope document, E2→E3 is not “current facts under current scope”, and two hosts can attribute the scope axis differently for one PlanId. `plan.scopeDigest` (foundation `scope-descriptor`) must not substitute.

**Revision:** when ScopeDocumentV1 is selected, selection is the intersection of enumeration extents, rule globs, and ScopeDocumentV1 globs (exclusion wins). Absent remains legal for non-comparison analysis; comparison/baseline keep the existing missing-selection refusal.

### MUST-2 — Missing covering program must not pass vacuously

Policy `subjectEnumeration.universe` is an open `CanonicalIdentifier` (fixtures: `typescript-v2`, `rust-v3`), not a native universe H digest. Enumeration cells are requestedCapabilities tuples with kinds `file|symbol|package`. A policy can have symbol/export rules while the Plan requested only inventory.

“Select every admitted program of the rule’s portable universe domain” with none present is observationally identical to complete-empty unless a covering expected locator is required. That contradicts workflows §3 (zero findings never establish complete analysis) and the proposal’s own “missing expected outcome is an incomplete retained graph”.

**Required lattice:**

| Situation | `rule-enumeration.state` | Gating outcome |
|---|---|---|
| Disabled | `disabled` | `disabled` (execution cells still assessed) |
| No cell whose kinds (export→symbol) and portable domain cover the rule | `incomplete` | `indeterminate` if gating; **not** whole-Plan refuse |
| Covering binding unavailable, or expected inventory locator missing | `incomplete` | same; missing locator ≠ empty population |
| Covering inventory partial/unavailable, or unresolved export nonempty | `incomplete` | known rows still evaluate; unknown export is unresolved, never unmatched |
| Covering available binding + complete inventory + include/exclude selects zero | `complete` | `pass` if no other deficiency — **only** valid complete-empty |
| Policy universe token not in the closed portable-domain map | Plan admission refuse | `CONFIG.INVALID` |

Publish the map from policy universe tokens to `native.semantic-universe.{typescript.v2,rust.v2,syntax.v2}`. Unknown token is not empty selection.

### MUST-3 — Emission schema does not enforce the prose joins

`evaluator-emission-plan.schema.v1.json` uses array `uniqueItems` (whole-object equality), not uniqueness by `ruleId`. Two bindings with the same `ruleId` and different `detectorClosure` admit. There is no minItems, no ruleId-set equality with policy, no `policyDigest == plan.policyDigest`, no `kind=detector` membership in `plan.semanticClosures`.

Worse: two enabled rules may share `ruleStableId`+`semanticsMajor` and differ in `ruleId`. Fingerprint stays `finding-key2` (no `ruleId`). Two findings, one fingerprint. Baseline entries are unique by fingerprint **and** “all fields must agree”, so disagreeing `ruleId` refuses the **entire** baseline. Source already cannot store two entries with one fingerprint. Catch this at Plan admission: for this profile, `(ruleStableId, semanticsMajor)` unique across **all** emission rows. Do not mint `finding-key3`.

Also required: emission ruleId set equals policy ruleId set including disabled; each `detectorClosure` is Plan-selected `kind=detector`. Payload-registry rows must be **separate documents** (identity3 draft already does this). Do not add a second `$def` from `policy-document.schema.json` (`PAYLOAD_PARAMETER_AMBIGUOUS_ROW`).

### MUST-4 — Budget preflight: unknown S, overflow, public route

Charge `E + Σ_{r,s} [N(r)+A(r)*(F+I+K)]` with checked integer arithmetic is the right shape. Holes:

1. Unknown/missing population must not be charged as `S=0` (that admits unbounded later work) and must not skip preflight. Charge `|selected|` only if unresolved/missing locators are never node-evaluated. `E` still includes expected locators plus actual rows.
2. Intermediate overflow is budget-exceeded, never wrap.
3. Whole-Run D9 member `budget-exhausted` may be reused (workflows §9: no new D9 family). Public **DomainDetailCode** must be new: native cell `budget-exhausted` means restore provider/coverage; evaluator work-budget means raise `analysis.budget`.
4. “Registered bounded-output fault” does not exist in the public registry. Operational-failed, no successful empty Run. Name `EVALUATION.OUTPUT_BOUND_EXCEEDED` (or equivalent) beside existing `faultCause=output-serialization`.

### MUST-5 — Witness major 3 and closed deficiency causes

Composition adds witness `kind`, import addresses, uncertain matches, deficiencies. Source `predicate-witness` is schemaVersion 2. That is a record-shape change. It is not an H-prefix domain, so it is correctly absent from `finding3/proof3`, but it **must** be listed as witness schemaVersion 3. A v2 witness must not parse into a v3 proof.

Draft `evaluation-deficiency.cause` is `Text` with a promise of a closed registry. Composition never names it. Close by `source`:

- enumeration: `missing-expected-inventory`, `incomplete-inventory`, `unknown-export-membership`, `no-covering-program`
- native: existing `DeficiencyV2` / `NativeCause` (do not copy-widen)
- import: existing `IMPORT.ABSENT_FOR_PREDICATE` / required unavailable/unmapped/stale
- execution: `work-budget-exhausted`, `required-cell-unsatisfied`
- correspondence: `projection-unavailable`, `signature-ambiguous`, `anonymous-subject`, `population-incomplete`

### MUST-6 — Workflow majors and public routes are unnamed

“New baseline artifact major” and “target-correspondence-unavailable” are not schema majors, fields, or `DomainDetailCode` members. Closed registries do not grow by prose. Exact list below.

### MUST-7 — Analyze fail vs audit indeterminate

A gating rule whose only live findings are unmatched: current Run **fail**; comparison emits **no** CODE-NET-NEW; `ruleDeficiencies` gets correspondence; comparison **indeterminate** unless another matched entry fails. Path-waiving those unmatched can pass `analyze` while `audit --baseline` stays indeterminate. If this split is not written, implementers will classify unmatched as CODE-NET-NEW or drop them from the current gate.

### MUST-8 — Required parameters vs class-wide `zeroIsLegal`

Source parameter law: zero entries for a row is legal; ScopeDocumentV1 is refused only when a consumer needs it. Composition: exactly one EnumerationPlanV1 and one EvaluatorEmissionPlanV1 **required for this evaluator**. That is per-row requiredness. Missing must not reuse `BASELINE.SCOPE_*`.

### SHOULD

1. Close the 7 parameter keys at profile admission; `subjectKind` ∈ `{file,symbol,package}` never `export`; `subjectLanguage` is native row/body language, not engine domain; counts ≥ 0.
2. Add `findingId` to graph-query params; candidate `kind=finding` accepts fingerprint **or** findingId; unmatched are not fingerprint-suppressible.
3. State collision-class completeness as completeness of the producing inventory for that class.
4. Preflight output cardinality against schema maxItems (100000 findings/proofs), not only work-units.
5. Conflicting attribution of the same `(universe,kind,nativeSubjectId)` is incomplete, not last-writer union.

### ADVISORY

- Optional `none`/`not` encodings will pass when optional evidence is unknown. Do not “fix” that by granting optional unknown gating authority.
- Emission `$id` URN vs enumeration `$id` style is cosmetic; registry keys by file bytes.
- Draft identity3 `Domain` enum vs `Ref.domain` split is pending identity3 integration; composition still requires one registered set.

---

## Necessary exact joins / schema changes

**Foundation (output 3, input 2 retained)**

- `finding` → `finding3:` nullable fingerprint, `ruleId`, `subject`, `correspondence`
- new H domain `evaluation-subject` / `subject3:` `{schemaVersion:3,universe,kind,nativeSubjectId}`
- `proof-bundle` → `proof3:` `evaluationState`, `ruleResults`, `waivedFindingIds`, `executionDeficiencies`
- `predicate-witness` schemaVersion **3** (canonical-record)
- `evidence3`, `seal3`, `run3`, `policy-derivation3` because finding/proof identity changed
- `finding-key2` **unchanged**
- payload-registry parameter rows: `foundation/enumeration-plan.schema.v1.json` and `foundation/evaluator-emission-plan.schema.v1.json` as own documents; **min 1** each for evaluator3
- `Domain` / `Ref.domain` / `ProofInputRef.domain` / `byDomain` one set, adding `evaluation-subject`, `subject-inventory`, `enumeration-plan`, `evaluator-emission-plan`
- FindingEvidenceRef stays `{fact,coverage,import,predicate-witness,blob}`; enumeration refs stay in the proof

**Emission schema v1:** uniqueness by `ruleId`; joins in MUST-3; registry extension like EnumerationPlanV1.

**Workflows (historical must not acquire empty unmatched arrays)**

| Document | Major | Change |
|---|---|---|
| `baseline-artifact.schema.json` | **2** | required `unmatchedOccurrences[]` `{findingId,ruleId,subjectId,subjectPath,severity,waived}`; entries unique by matched fingerprint only; major 1 → `BASELINE.SCHEMA_MAJOR_UNSUPPORTED`, never default `[]` |
| `comparison-result.schema.json` | **2** | unmatched list; `RuleDeficiency.cause` add `correspondence-incomplete`; unmatched **not** in `entries`; matched CODE-NET-NEW still fails |
| `common.schema.json` | additive / **2** | `RunId`/`EvidenceId` for `run3:`/`evidence3:` or explicit dispatch; `Fingerprint` stays `finding-key2:`; add `FindingId` `finding3:` |
| `review.schema.json` | **2** | finding candidates: fingerprint **or** findingId |
| `repair.schema.json` | admission law | targets remain fingerprints; unmatched → `REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE` |
| `graph-query.schema.json` | **2** | optional `findingId` |
| command-inventory / SARIF | parity law | one result per finding3 including unmatched and per-configuration; `partialFingerprints` only when matched; never dedupe by fingerprint |
| `policy-document.schema.json` | no major if uniqueness is emission-admission | do not add virtual export kind |

**New public DomainDetailCode (no new D9 family)**

| Code | Carrier |
|---|---|
| `EVALUATION.ENUMERATION_PLAN_NOT_A_SELECTED_PARAMETER` | request-rejected / `REQUEST.PRECONDITION_FAILED` |
| `EVALUATION.EMISSION_PLAN_NOT_A_SELECTED_PARAMETER` | same |
| `EVALUATION.EMISSION_PLAN_POLICY_DIGEST_MISMATCH` | request-rejected / `CONFIG.INVALID` |
| `EVALUATION.EMISSION_RULE_SET_MISMATCH` | same (ruleId set, duplicate ruleId, duplicate stable+major) |
| `EVALUATION.DETECTOR_CLOSURE_NOT_SELECTED` | same |
| `EVALUATION.POLICY_UNIVERSE_UNREGISTERED` | same |
| `EVALUATION.WORK_BUDGET_EXHAUSTED` | indeterminate; D9 `budget-exhausted` **with this detail**, not native cell remedy |
| `EVALUATION.OUTPUT_BOUND_EXCEEDED` | operational-failed |
| `COMPARISON.CORRESPONDENCE_INCOMPLETE` | comparison indeterminate detail |
| `REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE` | request-rejected / `REQUEST.PRECONDITION_FAILED` |
| `EVALUATION.MIXED_OUTPUT_MAJOR` | `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` |

Do not reuse `BASELINE.SCOPE_*` or native public `budget-exhausted` as the evaluator work-budget remedy.

---

## Recommended composition contract v4

1. Keep unmatched-as-finding, nullable fingerprint, closed correspondence, baseline major 2 unmatched array, comparison correspondence deficiency, path-vs-fingerprint waiver split.
2. Add the population lattice (MUST-2) and policy-universe→portable-domain map.
3. Consume ScopeDocumentV1 by intersection (MUST-1).
4. Collision-class completeness per producing inventory and stored kind; export is symbol∧exported.
5. Put emission uniqueness and Plan joins in schema+admission (MUST-3).
6. Replace unnamed budget/output faults with the public codes above.
7. List `predicate-witness` v3 and the workflow majors table.
8. Write the analyze-fail / audit-indeterminate split.
9. Close the 7 parameter keys and deficiency causes.
10. Do not invent a virtual export kind, flatten unknown import causes, or put unmatched into comparison `entries`.

Helper copy: `composition-critique.v1.md` in this output directory. Enumeration and atom contracts remain separately owned.
