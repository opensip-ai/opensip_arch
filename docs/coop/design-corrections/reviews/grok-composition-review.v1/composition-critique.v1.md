# Grok independent composition critique — evaluator-composition-contract.v3

Standing: source-level design review of an isolated proposal. Not integrated, not implementation-ready, not source assent. No tests were run. Enumeration and atom appendices are treated as foreign inputs; this review owns composition joins and alternatives only. Identity-schemas.v3 draft mismatch with frozen source21 is treated as known pending integration except where it reveals a composition logic hole or a join the composition contract itself fails to name.

Proposal read in full:
- `evaluator-successor.v1/docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md`
- `evaluator-emission-plan.schema.v1.json`

Parent source21 read as needed:
- `docs/v2/contracts/product-v1/identity-and-evidence.md`
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md`
- `docs/coop/design-corrections/foundation/identity-schemas.v2.json`
- `docs/coop/design-corrections/workflows/schemas/{policy-document,baseline-artifact,comparison-result,command-envelope,review,repair,common,invocation-record,graph-query}.schema.json`
- `docs/coop/design-corrections/public-detail-registry.v1.json`

Joins consulted (not enumeration/atom authorship): successor `enumeration-plan.schema.v1.json`, `subject-inventory.schema.v1.json`, `evaluator-projection-registry.v1.json`, draft `identity-schemas.v3.json` finding/proof/witness/parameter-registry slices.

Verdict: **request changes**. Unmatched-as-finding is the right alternative. Several composition laws are underspecified against closed source vocabularies and will vacuous-pass, collide fingerprints, or silently skip existing Plan parameters.

---

## Settled alternatives (requested questions)

### 1. Nullable fingerprint + unmatched occurrences vs drop vs refuse-whole-run

**Settled: unmatched findings with nullable fingerprint, closed correspondence, and a new baseline unmatched array is coherent and superior.**

| Alternative | Effect on known `emitWhen=true` | Effect on comparison | Effect on fingerprint waiver/repair |
|---|---|---|---|
| Drop unmatched findings | Known violations vanish → current Run can pass | Baseline looks complete | N/A |
| Refuse whole Run | Punishes complete inventories for one incomplete collision class | No comparable subset | No repair of matched targets |
| Unmatched-as-finding (proposal) | Live unwaived finding still fails a gating rule | Matched subset still classifies; unmatched excluded from entries; correspondence deficiency on affected gating rules | Fingerprint targets refuse; path waiver and findingId inspection remain |

This is superior **only if** the MUST joins below land. Source conflicts that make the current draft incomplete:

- `identity-schemas.v2.json#/$defs/finding.properties.fingerprint` is required `finding-key2:` (non-null). Output major 3 is already the right move.
- `baseline-artifact.schema.json#/$defs/BaselineDescriptor.properties.entries` is unique by `fingerprint` with `schemaMajor` const 1 and no unmatched array. Missing array on major 1 must **not** be read as `[]` (proposal already says this; it is not yet a schema major).
- `comparison-result.schema.json#/$defs/RuleDeficiency.cause` is closed `{required-coverage-unsatisfied, required-coverage-unknown, required-evidence-unavailable}`. Correspondence cannot be carried without a new cause.
- `review.schema.json#/$defs/Candidate` requires `fingerprint` when `kind=finding`. Unmatched findings currently cannot be candidates.
- `repair.schema.json#/$defs/RepairPlanDescriptor.properties.targets` items are `Fingerprint` (`finding-key2:` only). Fingerprint-targeted repair must refuse unmatched; that refusal has no public code today.
- `common.schema.json#/$defs/Fingerprint` and `graph-query.schema.json` `params.fingerprint` have no `findingId` locator.

Dropping findings is rejected: it contradicts workflows §5 (“a true predicate emits a finding”) and identity §4 replay of complete findings. Whole-run refuse is rejected: identity already distinguishes incomplete native inputs → indeterminate Run from operational faults; a single anonymous symbol must not void matched file findings.

### 2. Path waiver vs fingerprint waiver

**Settled: the split preserves intended source semantics, with one required clarification.**

Source (`policy-document.schema.json#/$defs/Waiver.target`, workflows §5): a waiver matches fingerprint **or** exact `(ruleId, subjectPath)`. Proposal: occurrence waived iff any effective target equals its **nonnull** fingerprint or equals `(ruleId, subjectPath)`; unmatched cannot satisfy a fingerprint-target waiver.

That is the intended split. Path waiver is file-granularity by construction (same as repair’s imported projection widening). It will waive every unmatched and matched occurrence of that rule on that path; that is existing path-waiver meaning, not a new hole.

Required clarification (MUST-7): fingerprint-only waivers that match nothing because every hit was unmatched do **not** suppress those live unmatched findings, and a path waiver of unmatched findings does **not** cure comparison correspondence uncertainty (proposal sentence already says waiver does not cure correspondence uncertainty; it must also say the current-Run gate **can** pass via path waiver while audit stays indeterminate).

### 3. Collision-class incompleteness vs false match

**Settled: over-conservatism is acceptable and required.** False match would merge distinct native IDs into one `finding-key2`, poisoning waiver, baseline, repair, and review.

Must be per collision class `(universe, subjectLanguage, kind, path, qualifiedName, detectorClosure)`, **not** whole-run and **not** cross-kind:

- Partial **symbol** inventory → every symbol class that inventory could have omitted a duplicate for is unmatched (`population-incomplete`). In practice every symbol from that inventory.
- Complete **file** / **package** inventory still matches file/package findings. `SHA256(C([]))` file discriminator is not “empty/missing projection”; it is the specified constant discriminator. Do not unmatch files because symbols are partial.
- Unknown **export membership** is not unmatched and not a virtual `export` kind (agrees with projection-registry `exportIsNotAKind` and policy `subjectKind=export` as symbol∧exported).

### 4. Emission parameter + generic 7 params vs existing custom-param / related-subject contract

**Settled: explicit pre-Plan emission binding is the right shape.** Policy `ruleProgramRef` has contribution/stable/major/programDigest and **no** detector closure. Tokens come from inventory projections of a Plan-selected `kind=detector` closure. Do not infer a contribution↔closure oracle.

Generic 7 parameters for `declarative-subject-v1` do **not** unfulfill a policy custom-parameter contract: `PolicyDocumentV1.Rule` has no parameter template. `relatedSubjectKeys: []` is correct for this unary profile; clone/candidate producers stay outside. The profile must still **close** the 7 keys at emission admission (`finding-parameters` remains an open map in source).

Unfulfilled existing contract: **ScopeDocumentV1** (see MUST-1).

### 5. Required imports, optional unknown, disabled rules, budget, empty universe

See MUST-2, MUST-3, MUST-4, MUST-5. Short version:

- Required `evidenceUse` independent of Kleene short-circuit: accept.
- Optional-only root unknown → pass with disclosure: accept as consistent with `IMPORT.ABSENT_FOR_PREDICATE`; do not flatten unknown causes.
- Disabled rules empty + independent required execution cells: accept; join those cells to `EnumerationPlanV1.cells[].required` / `analysis-spec.requestedCapabilities[].required`.
- No covering program for a rule’s (portable domain, stored kind): **incomplete**, never complete-empty, never Plan-wide refuse, never vacuous pass.
- Valid complete-empty: covering available program **and** expected inventory present **and** complete **and** include/exclude selects zero subjects.

---

## Findings

### MUST-1 — ScopeDocumentV1 is an existing Plan parameter the composition never consumes

**Source:** identity-and-evidence §3 payload-registry parameter row `workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1`; comparison `EvaluationContext.scopeDigest`; `BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER` / `BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH`.

**Proposal:** subject selection is enumeration extents ∪ rule `include`/`exclude` only.

**Conflict:** E2→E3 is a re-evaluation under a different ScopeDocumentV1. If current evaluation ignores the Plan-selected scope document, E3 cannot equal “current facts under current scope”, and two hosts can attribute the scope axis differently for one PlanId.

**Revision:** when the ScopeDocumentV1 parameter is selected, evaluator selection is the intersection of (enumeration extents, rule globs, ScopeDocumentV1 globs), exclusion wins. Absent ScopeDocumentV1 remains legal for non-comparison analysis; comparison/baseline still use the existing missing-selection refusal. Do not substitute `plan.scopeDigest` (foundation `scope-descriptor`).

### MUST-2 — Missing covering program must not be complete-empty

**Source:** workflows §3 “zero emitted findings never establish complete analysis”; identity §4 completeness vs false pass; successor `rule-enumeration.state` is `disabled|complete|incomplete` with “Complete-empty is explicit”; `SubjectInventoryV1.state` is `complete|partial|unavailable`; `EnumerationPlanV1.cells` are requestedCapabilities tuples, kinds `file|symbol|package` (no export).

**Proposal:** “select every admitted program of the rule’s portable universe domain and required primary subject kind”. If none exist, selected arrays are empty. That is observationally identical to complete-empty unless a covering expected locator exists.

**Conflict:** Policy `subjectEnumeration.universe` is an open `CanonicalIdentifier` (fixtures: `typescript-v2`, `rust-v3`), not a native universe H digest. Enumeration cells may omit syntax while policy still has symbol/export rules. Treating “no program” as zero subjects vacuous-passes gating `none`/`all-covered` encodings and contradicts “missing expected outcome is an incomplete retained graph”.

**Logical definition (required):**

| Situation | rule-enumeration.state | Gating rule outcome | Notes |
|---|---|---|---|
| Disabled rule | `disabled` | `disabled` | Empty arrays; execution cells still assessed |
| No EnumerationPlanV1 cell whose `kinds` (export→symbol) and portable domain cover the rule | `incomplete` | `indeterminate` if gating | **Not** a whole-Plan refuse (file rules may still run) |
| Covering binding is `UnavailableProgramBindingV1` or expected inventory locator missing | `incomplete` | same | Missing locator ≠ empty population |
| Covering inventory `partial`/`unavailable` / unresolved export membership nonempty | `incomplete` | same; known rows still evaluate | Unknown export is unresolved, never unmatched |
| Covering available binding + complete inventory + include/exclude selects zero | `complete` | `pass` if no other deficiency | The only valid complete-empty |
| Unknown policy universe token (not in the closed portable-domain map) | Plan admission refuse | n/a | `CONFIG.INVALID`, new detail |

Publish the closed map from policy universe tokens to portable domains (`native.semantic-universe.typescript.v2|rust.v2|syntax.v2`). Unknown token is not empty selection.

### MUST-3 — Emission schema does not enforce the joins the prose claims

**Source:** identity analysis-spec parameter law (at most one per registry row; keyed by **document** digest); policy `rules[].ruleId` unique; `plan.policyDigest`; `plan.semanticClosures` + closure `kind`; finding-fingerprint identity excludes `ruleId`.

**Proposal prose:** one binding for every policy rule including disabled; duplicate rule IDs refuse; `ruleId`/contribution/stable/major equal policy; `detectorClosure` is Plan-selected `kind=detector`; policy independently resolved.

**Proposal schema (`evaluator-emission-plan.schema.v1.json`):**

- `rules` has `uniqueItems: true` (whole-object equality), **not** uniqueness by `ruleId`. Two bindings with the same `ruleId` and different `detectorClosure` admit.
- No minItems; policy `rules.minItems=1`.
- No join that the ruleId set equals `PolicyDocumentV1.rules`.
- No join `policyDigest == plan.policyDigest`.
- `stabilityClass`/`emissionProfile` consts are fine; detector kind is not in the schema.

**Also:** two enabled rules may share `ruleStableId`+`semanticsMajor` and different `ruleId`. Fingerprint is `finding-key2(ruleStableId, major, subjectKey)` so they mint one fingerprint and two findings. `BaselineEntry` unique by fingerprint **and** “all fields must agree” then refuses the entire baseline (`ruleId` disagrees). Source already cannot store two entries with one fingerprint. Composition makes the failure a whole-artifact refuse without a Plan-time check.

**Revision:**

1. `x-opensip-uniqueness` on `rules[].ruleId` (same shape as analysis-spec ownership tuples).
2. Plan admission: emission ruleId set **equals** policy ruleId set (including disabled).
3. `emission.policyDigest == plan.policyDigest == C(PolicyDocumentV1)`.
4. Each `detectorClosure` ∈ `plan.semanticClosures` and retained closure.kind=`detector`.
5. For this profile, `(ruleStableId, semanticsMajor)` unique across **all** emission rows (not only enabled). Do not mint `finding-key3`; uniqueness preserves retained `finding-key2`.

Payload-registry: identity3 draft already adds document-keyed rows for enumeration-plan and emission-plan (correct: separate documents, not a second `$def` of `policy-document.schema.json`). Class-wide `zeroIsLegal` still contradicts “exactly one required for this evaluator”. Per-row requiredness is required (MUST-8).

### MUST-4 — Budget preflight unknown/overflow/output-cardinality

**Source:** `plan.budget` equals `semantic-configuration.analysis.budget`, limit ≤ 2^53−1; D9 `budget-exhausted` is already a **native** whole-Run and per-requirement spelling; identity descriptor cap 4 MiB; proof `findingIds`/`predicateProofs` maxItems 100000; “a schema/identity/interpreter fault is an operational failure, not a fourth truth value”.

**Proposal:** charge `E + Σ_{r,s} [N(r) + A(r)*(F+I+K)]` with checked integer arithmetic; exceed Plan budget → semantic `budget-exhausted` output with empty predicates/findings and indeterminate gating rules; array/C-byte overflow refuses with “registered bounded-output fault”.

**Holes:**

1. If expected inventories are missing, `S` is not a complete selected set. Charging `|selected|` only is correct **iff** unresolved/missing locators are not later evaluated. State that explicitly. Do not treat unknown `S` as 0 (that would admit an unbounded later eval). Do not skip preflight when unresolved nonempty.
2. Charge overflow (including intermediate `A(r)*(F+I+K)`) is budget-exceeded, never wrap.
3. Whole-Run D9 member `budget-exhausted` may be reused (no new D9 family — workflows §9). Public **DomainDetailCode** must be new: native cell `budget-exhausted` remedy is provider/coverage; evaluator work-budget remedy is raise `analysis.budget`. Do not emit public `budget-exhausted` as if it were native §4.6.
4. Name the bounded-output public route. There is no `bounded-output` DomainDetailCode. Operational class, `faultCause=output-serialization` or a new `IDENTITY.DESCRIPTOR_BOUND_EXCEEDED` / `EVALUATION.OUTPUT_BOUND_EXCEEDED`. Never a successful empty Run.

### MUST-5 — Witness record major and cause vocabulary are composition-owned and unnamed

Composition adds witness `kind`, import observation addresses, uncertain matches, deficiencies. Source `predicate-witness` is schemaVersion 2 with only facts/coverage/countLimit/children. That is a record-shape change. It is not an H-prefix domain, so it is correctly absent from `finding3/proof3/...`, but it **must** be listed as `predicate-witness` schemaVersion 3 (draft identity3 already does this). Omitting it from the composition’s changed-record list will let a v2 witness parse as a v3 proof.

`evaluation-deficiency.cause` in the draft is `Text` with a promise of a closed per-source registry. Composition never names that registry. Two hosts can emit different cause strings and still seal. Close causes by `source`:

| source | closed causes (minimum) |
|---|---|
| enumeration | `missing-expected-inventory`, `incomplete-inventory`, `unknown-export-membership`, `no-covering-program` |
| native | existing `DeficiencyV2` / `NativeCause` (do not copy-widen) |
| import | existing import predicate/requirement outcomes (`IMPORT.ABSENT_FOR_PREDICATE`, required unavailable/unmapped/stale) |
| execution | `work-budget-exhausted`, `required-cell-unsatisfied` |
| correspondence | `projection-unavailable`, `signature-ambiguous`, `anonymous-subject`, `population-incomplete` (same as finding.correspondence.reason) |

### MUST-6 — Workflow majors and public routes are not listed

Proposal says “a new baseline artifact major” and “target-correspondence-unavailable” without schema majors, fields, or DomainDetailCode members. Source registries are closed. Exact list is in “Necessary schema changes” below.

### MUST-7 — Analyze fail vs audit indeterminate must be stated

A gating rule whose only live findings are unmatched: current Run **fail** (live unwaived finding); comparison emits **no** CODE-NET-NEW (unmatched not classified); `ruleDeficiencies` correspondence cause; comparison verdict **indeterminate** unless another matched entry fails. Path-waiving those unmatched can make the current Run **pass** while comparison stays indeterminate. If this split is not written, implementers will classify unmatched as CODE-NET-NEW or drop them from the current gate.

### MUST-8 — Required emission/enumeration parameters vs class-wide zeroIsLegal

Source parameter law: zero entries for a row is legal; missing ScopeDocumentV1 is refused only when a consumer needs it. Composition: exactly one EnumerationPlanV1 and one EvaluatorEmissionPlanV1 **required for this evaluator**. That is a per-row requiredness change. Public refusals cannot reuse `BASELINE.SCOPE_*`.

### SHOULD-1 — Close declarative-subject-v1 parameter keys

`finding-parameters.parameters` is an open map (`^[a-z][a-zA-Z0-9]*$` → string\|int\|bool). Profile admission: exactly `{ruleId, subjectPath, qualifiedName, subjectKind, subjectLanguage, matchingFactCount, matchingImportCount}`; counts ≥ 0; `subjectKind` ∈ `{file,symbol,package}` never `export`; `subjectLanguage` is native **row/body** language, not engine domain (identity clones `languageId` law). `messageCode` equals finding.messageCode.

### SHOULD-2 — Query and candidate locators for unmatched

Add optional `findingId` to `graph-query` params. Candidate `kind=finding`: require fingerprint **or** findingId; `controlBearing` still only gating+matched-or-live; unmatched candidates are inspectable, not fingerprint-suppressible. Review suppression by fingerprint does not hide unmatched (fingerprint unchanged is the suppression key; unmatched have none).

### SHOULD-3 — Collision-class completeness per producing inventory

State that completeness is the completeness of the inventory that would list every native ID in that class. File discriminator `SHA256(C([]))` is specified, not `projection-unavailable`.

### SHOULD-4 — Preflight also checks output cardinality

Work-units passing then 100001 findings refusing at serialization is lawful (operational refuse) but hostile. Charge an output-cardinality bound against schema maxItems before node evaluation.

### SHOULD-5 — Conflicting attribution of the same subject3

“Union duplicates only after exact attribution/projection agreement”: disagreement is incomplete/conflicting population, not last-writer.

### ADVISORY-1 — Optional `none`/`not` encodings

Optional-only unknown → pass is consistent with workflows §5 optional-absent. A rule whose `emitWhen` is a universal negative over optional imported evidence will pass when that evidence is unknown. Do not “fix” this by giving optional unknown gating authority.

### ADVISORY-2 — Emission `$id` style vs enumeration `$id`

Cosmetic (`urn:opensip:...` vs `opensip.product.enumeration-plan.1`). Registry keys by **file bytes**, not `$id`.

### ADVISORY-3 — Identity3 Domain enum vs Ref.domain

Draft `Domain` enum omits `subject-inventory` / `evaluation-subject` / `enumeration-plan` / `evaluator-emission-plan` while `Ref.properties.domain` includes them. Known pending identity3 integration; composition must require one registered set (identity §3: both enums equal `byDomain` keys).

---

## Necessary exact joins / schema changes

### Foundation / identity (output major 3, input 2 retained)

| Record | Change |
|---|---|
| `finding` | schemaVersion 3, prefix `finding3:`; nullable fingerprint; required `ruleId`, `subject`, `correspondence`; `subjectId` = `subject3:` |
| `evaluation-subject` | **new** H domain `subject3:`; `{schemaVersion:3,universe,kind,nativeSubjectId}`; kind `file\|symbol\|package` |
| `proof-bundle` | schemaVersion 3, prefix `proof3:`; add `evaluationState`, `ruleResults`, `waivedFindingIds`, `executionDeficiencies`; `findingIds` pattern `finding3:` |
| `predicate-witness` | schemaVersion 3 (canonical-record, not H prefix); add kind/import/uncertain/deficiencies |
| `semantic-evidence`, `evaluation-seal`, `run`, `policy-derivation` | prefix 3 because finding/proof identity and record shape changed |
| `finding-fingerprint` | **unchanged** major 2 |
| `plan`, `analysis-spec` | unchanged shape; values change when new parameters selected |
| `x-opensip-payload-registry.classes.parameter.rows` | add `foundation/enumeration-plan.schema.v1.json` and `foundation/evaluator-emission-plan.schema.v1.json` (own documents); **per-row** `minItems=1` for those two under evaluator3; do **not** add a second `$def` from `policy-document.schema.json` |
| `Domain` / `Ref.domain` / `ProofInputRef.domain` / `byDomain` | one set; add `evaluation-subject`, `subject-inventory`, `enumeration-plan`, `evaluator-emission-plan` (and `target-attribution` if retained as input) |
| `ProofInputRef` | may cite `subject-inventory`, `analysis-spec` (parameters live there). FindingEvidenceRef stays `{fact,coverage,import,predicate-witness,blob}` |
| `finding-parameters` | keep schemaVersion 2; profile-closed 7 keys at emission law, not a second H domain |

### Emission schema (input, major 1)

- uniqueness by `ruleId`
- admission joins listed in MUST-3
- `x-opensip-parameter-registry-extension` like EnumerationPlanV1 (`keyIsTheDocumentNotThePair`, at most one per spec, required for evaluator3)

### Workflows (new majors; historical must not acquire empty-array assertions)

| Document | Major | Fields / law |
|---|---|---|
| `baseline-artifact.schema.json` | **2** | required `unmatchedOccurrences[]` `{findingId, ruleId, subjectId, subjectPath, severity, waived}`; `schemaMajor` const 2; entries still unique by fingerprint of **matched** only; major 1 refused (`BASELINE.SCHEMA_MAJOR_UNSUPPORTED`), never default unmatched to `[]` |
| `comparison-result.schema.json` | **2** | `unmatchedOccurrences` (or equivalent current-side list); `RuleDeficiency.cause` add `correspondence-incomplete` (name closed); do not add unmatched into `entries`; `IndeterminateReason` add `correspondence-population-incomplete` if whole-comparison needs it — prefer per-rule deficiency so matched CODE-NET-NEW still fails |
| `common.schema.json` | **2** or additive | `RunId`/`EvidenceId` patterns for `run3:`/`evidence3:` **or** explicit version dispatch; keep `Fingerprint` = `finding-key2:`; add `FindingId` = `finding3:` |
| `review.schema.json` | **2** | `kind=finding` requires fingerprint **or** findingId; unmatched not fingerprint-suppressible |
| `repair.schema.json` | field law, possibly same major if only admission | targets remain fingerprints; unmatched target → `REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE` |
| `graph-query.schema.json` | **2** | optional `findingId` on params |
| `command-inventory` / SARIF projection | parity law | one result per finding3 including unmatched and per-configuration; `partialFingerprints` only when matched; never dedupe by fingerprint |
| `command-envelope` / `invocation-record` | via common RunId | no silent findings drop; AnalysisResult still has no inline findings array — renderer projection is the carrier |
| `policy-document.schema.json` | **no major required** for this profile if uniqueness is emission-admission | do not add virtual export kind; keep `subjectKind=export` as selection token |

### Public DomainDetailCode (new members; no new D9 family)

| Code | Class / existing error | When |
|---|---|---|
| `EVALUATION.ENUMERATION_PLAN_NOT_A_SELECTED_PARAMETER` | request-rejected / `REQUEST.PRECONDITION_FAILED` | evaluator3 Plan missing EnumerationPlanV1 |
| `EVALUATION.EMISSION_PLAN_NOT_A_SELECTED_PARAMETER` | same | missing EvaluatorEmissionPlanV1 |
| `EVALUATION.EMISSION_PLAN_POLICY_DIGEST_MISMATCH` | request-rejected / `CONFIG.INVALID` | emission.policyDigest ≠ plan.policyDigest |
| `EVALUATION.EMISSION_RULE_SET_MISMATCH` | same | emission ruleIds ≠ policy ruleIds, or duplicate ruleId, or duplicate `(ruleStableId,semanticsMajor)` |
| `EVALUATION.DETECTOR_CLOSURE_NOT_SELECTED` | same | detectorClosure not Plan-selected kind=detector |
| `EVALUATION.POLICY_UNIVERSE_UNREGISTERED` | same | policy universe token not in portable-domain map |
| `EVALUATION.WORK_BUDGET_EXHAUSTED` | indeterminate / existing `VERDICT.INDETERMINATE` or D9 `budget-exhausted` **with this detail** | preflight charge > Plan budget or charge overflow |
| `EVALUATION.OUTPUT_BOUND_EXCEEDED` | operational-failed / `HOST.IO_FAILURE` + `faultCause=output-serialization` | array/C-byte/maxItems overflow; no Run rewrite if already committed, else no successful empty Run |
| `COMPARISON.CORRESPONDENCE_INCOMPLETE` | comparison indeterminate detail | unmatchedOccurrences or enumeration uncertainty on a gating rule |
| `REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE` | request-rejected / `REQUEST.PRECONDITION_FAILED` | fingerprint-targeted repair/review on unmatched finding |
| `EVALUATION.MIXED_OUTPUT_MAJOR` | request-rejected / `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` | mixed finding2/finding3 graph |

Do **not** reuse `BASELINE.SCOPE_*` or native public `budget-exhausted` as the evaluator work-budget remedy. Do not add a D9 family.

Internal (may stay non-public if only Run closure sees them, but then they still need a public projection when they terminate): enumeration appendix codes already listed as NEW/internal remain enumeration-owned.

---

## Recommended exact revision (composition contract v4)

1. Keep unmatched-as-finding, nullable fingerprint, closed correspondence, baseline major 2 unmatched array, comparison correspondence deficiency, path-vs-fingerprint waiver split.
2. Add §2.1 **Rule population lattice** with the table in MUST-2 and the policy-universe→portable-domain map.
3. Add §2.2 **ScopeDocumentV1 intersection** (MUST-1).
4. Add §2.3 **Collision-class completeness** per producing inventory and stored kind; export is symbol∧exported; unknown export → unresolved, not unmatched.
5. Tighten §1 emission joins to the schema+admission list in MUST-3; unique `(ruleStableId,semanticsMajor)`.
6. Replace “registered bounded-output fault” and “budget-exhausted” with the named public codes in MUST-4/MUST-8.
7. List changed records including `predicate-witness` v3 and the workflow majors table.
8. Add the analyze-fail / audit-indeterminate split (MUST-7).
9. Close `declarative-subject-v1` parameter keys (SHOULD-1) and `evaluation-deficiency.cause` by source (MUST-5).
10. Do not invent virtual export kind, flatten unknown import causes, or put unmatched into comparison `entries`.

No source assent. Enumeration/atom contracts remain separately owned; composition must not re-specify atom completeness laws beyond the joins above.
