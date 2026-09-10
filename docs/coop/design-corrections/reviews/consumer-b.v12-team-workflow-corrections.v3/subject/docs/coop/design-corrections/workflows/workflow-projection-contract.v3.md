# Evaluator3 workflow projection contract

Standing: incorporated by the product workflow contract into the intended
evaluator3 design. Acceptance and application are governed by external review
records. This projection consumes already admitted findings and proofs; its
public Run adapter first invokes the foundation's complete replay boundary.
The current output schemas are under `schemas/evaluator3/`.

## 0. Population and input custody

Input custody and semantic incompleteness have distinct routes:

| Condition | Route | Projection effect |
|---|---|---|
| Missing **expected inventory POINTER** (locator committed by EnumerationPlanV1, no retained record) | **Structural refusal** at input admission. Do **not** fabricate an `unavailable` inventory outcome. | Projection is not reached. |
| Expected locator present and an **unavailable inventory record** is retained | Semantic incomplete | `rule-enumeration.state=incomplete`; correspondence coverage `populationUnknown=true` |
| **No-covering-program** (no cell/kind cover, or unavailable program binding with a retained record) | Semantic incomplete | same |
| Lost retained bytes of a provided record | Distinct custody route (`evidence.missing` / operational HOST.IO) | Not correspondence-incomplete |
| Provided **invalid** bytes | Distinct admission/corrupt route | Not correspondence-incomplete |
| Covering available binding + complete inventory + include/exclude selects zero | Valid complete-empty | `populationUnknown=false`, zero findings is a real empty |

Known **attribution conflict** for the same `(universe,kind,nativeSubjectId)` (plus package manifest path for packages) or the same fingerprint identity with disagreeing fingerprint **preimages** is **input refusal**, never silently incomplete.

`source-syntax-invalid` is an enumeration-local cause. It is not a NativeCause/DeficiencyV2 member. If `rule-enumeration.state=incomplete` (including that cause, no-covering-program, or unknown export), zero findings must not become a vacuous pass: correspondence coverage keeps `populationUnknown=true`.

Package subject3 adds `packageManifestPath` at identity. Workflow projection treats `subjectId` as opaque and uses `finding.subject.logicalPath` as the path (the manifest path for packages). Same packageName at two manifests produces two fingerprints because the paths differ.

## 1. Version dispatch

| Artifact | Isolated `$id` | Identity-bearing `schemaMajor` | Why the major moved |
|---|---|---|---|
| common | `...evaluator3:common:3` | n/a (defs) | run3/evidence3/finding3/subject3 exact patterns |
| baseline | `...evaluator3:baseline:2` | **2** | required `unmatchedOccurrences` in H preimage |
| comparison | `...evaluator3:comparison:2` | **2** | unmatched + correspondenceCoverage in H preimage |
| review | `...evaluator3:review:2` | candidate shape | findingId; nullable fingerprint |
| graph-query | `...evaluator3:graph-query:3` | **3** | closed graph.* params, ResolvedView, traversal/count disclosure; `params.findingId` retained for finding ops |
| repair plan descriptor | `...evaluator3:repair:2` | **2** | `evidenceRunId` is run3 |
| envelope | `...evaluator3:command-envelope:3` | **3** | run3 + FindingSurface |
| invocation | `...evaluator3:invocation:3` | **3** | AnalysisResult.runId is run3 |
| command-inventory | `...evaluator3:command-inventory:3` | **3** | findings parity is FindingSurface |

Historical baseline/comparison `schemaMajor` 1 is `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` with detail `BASELINE.SCHEMA_MAJOR_UNSUPPORTED`. Missing unmatched arrays are **not** `[]`.

Output prefixes are exact (`^run3:`, `^finding3:`, `^evidence3:`). Mixed `run[23]` regex is forbidden. Native/input prefixes stay snapshot2/plan2/closure2/import2/fact2/finding-key2.

ScopeDocumentV1 and WaiverSetV1 remain on `urn:opensip:product-v1:workflows:policy-document`. Baseline embedded policy is `PolicyDocumentV2` on `urn:opensip:product-v1:policy-document:2`.

## 2. Projection preconditions

Pure functions consume an **admitted** evaluator3 view. They do not read producer expected baseline entries, expected comparison classifications, or any `verified=true` flag.

Required view fields:

- `runId` run3, `snapshotId` snapshot2, `planId` plan2, `projectId`
- `occurrences[]`: `{findingId, finding, fingerprintDescriptor?, parameterRecord, legacyFingerprint?}`
- `finding.subjectId` is an opaque `subject3:` value. Do not reconstruct subject3 from universe/kind/nativeId. `finding.subject.logicalPath` owns path (package: the manifest path; same packageName at two manifests are two fingerprints).
- `emissionBindings` keyed by ruleId (contributionId, ruleStableId, semanticsMajor, detectorClosure, stabilityClass, emissionProfile)
- `waivedFindingIds` exact list from proof
- `ruleResults` exact admitted per-rule results (enumeration + outcome + findingIds + deficiencies). There is **no** `gating` field. Missing `occurrences` / `ruleResults` is refusal (`EVALUATION.PROJECTION_INPUT_INCOMPLETE`); an omitted key is never `[]`.
- `executionDeficiencies` and `evaluationState` (including `budget-exhausted`) are required current fields and remain independent of rule findings.
- Independently admitted `pivotPresence` supplies E0–E3 only. Current `presence.E4`, `waivedC`, and `entryRules` are **derived** from matched occurrences. Caller-supplied `presence` / `entryRules` refuse.

Joins enforced here (cross-field joins are the reference model as cross-record laws beyond JSON Schema):

- findings map keyed by `findingId` only; duplicate ids refuse
- matched ⇔ nonnull `finding-key2` ⇔ `correspondence.state=matched` ⇔ `reason=null` ⇔ descriptor present and `H(finding-fingerprint, descriptor)=fingerprint`
- unmatched ⇔ `fingerprint=null` ⇔ `state=unmatched` ⇔ closed reason ⇔ no descriptor
- `parameterDigest = SHA256(C(parameterRecord))`
- declarative-subject-v1 parameter keys exactly the generic 7
- fingerprint **preimage** byte-equality for the same fingerprint id; disagreement is input refusal

`(ruleStableId, semanticsMajor)` uniqueness across **all** emission rows including disabled is a conservative profile admission owned by root composition. This projector assumes it already held, so BaselineEntry.ruleId cannot conflict under one fingerprint for this profile.

## 3. Baseline

Matched occurrences group only after **byte-equal fingerprint descriptors**. Then **all BaselineEntry fields** must agree, including optional `legacyFingerprint` **presence and value**. Per-occurrence message/parameters/citations may differ and are **not** compared.

Conflicting projections refuse (`CONFIG.INVALID` / `BASELINE.ENTRY_PROJECTION_CONFLICT`). No first/last writer.

Unmatched occurrences are excluded from `entries` and retained in `unmatchedOccurrences` with `side` (`baseline`|`current`), findingId, ruleId, subjectId, subjectPath, severity, waived.

`adopt_baseline` remains a pure projection over caller-admitted policy/scope/waivers. ScopeDocumentV1 parameter join is **mandatory** (`verify_scope_parameter_binding`); `analysis_spec=None` is not a bypass. `exportedAtUtc` / `exportedByHostRelease` are **trusted custody inputs**, not a hardcoded observed timestamp. `verify_baseline_artifact_v3` enforces schemaMajor 2, H(baselineId), context-document digest bindings, `side=baseline` unmatched, and `run3|closure2` retention pins. It does **not** call `evaluator_replay_model.v3.derive/replay`; origin Run admission is a prerequisite. Descriptor `schemaMajor` is 2; `runId` is run3; fingerprint recipe major stays 2. Historical schemaMajor 1 is `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` / `BASELINE.SCHEMA_MAJOR_UNSUPPORTED` before any unmatched-array coercion.

## 4. Comparison

Reuse `workflows_model.v1.classify` / audit profiles / detector union as an **explicit adapter**: emit ComparisonDescriptor `schemaMajor` 2; do not call `workflows_model.v1.compare` (schemaMajor 1). Pivot presence is over **matched fingerprints only**. E4/waivedC/entryRules come from admitted current occurrences, never from caller-expected maps.

Then add typed unmatched/population deficiencies for the **relevant** baseline and current population:

- comparison `unmatchedOccurrences` is the union of both sides, ordered by `(side, findingId)`
- unmatched records are not UNCHANGED / CODE-NET-NEW / CODE-FIXED / resolved
- `gateRuleUnder=baseline-or-current` (`code-regression` / `policy-change`): baseline unmatched gating obligations survive current empty findings or a removed current rule
- `gateRuleUnder=current-only` (`full-current` / `report-only`): use current policy coverage; a removed current rule does not inherit a baseline unmatched gate
- gating `correspondence-incomplete` when unmatchedCount>0 or `populationUnknown` (including zero findings) on a **gating** rule
- advisory/optional-only (`gate=false` or below severity floor) does not always-block
- **CODE-NET-NEW fail dominates** correspondence indeterminate (fail > indeterminate)
- default `code-regression`: new waiver does **not** suppress CODE-NET-NEW
- `full-current` / `report-only` (`current-only`): `newWaiverSuppressesCodeNetNew` as in source
- whole unmapped / recipe-unsupported / schema-major-unsupported still carry required `contextDelta`; `comparisonPerformed=false`; unmatched and coverage empty; typed `errorCode` is D9ErrorCode (`REQUEST.PRECONDITION_FAILED` or `REQUEST.SCHEMA_MAJOR_UNSUPPORTED`), never `CONFIG.INVALID` as a DomainDetail

Current-Run vs audit:

- live unwaived unmatched finding on a gating rule → current **fail**
- path waiver of that unmatched finding can make current **pass**; comparison stays correspondence-incomplete
- fingerprint waiver cannot cover unmatched
- incomplete population without a live unwaived finding → current indeterminate; comparison correspondence-incomplete for gating rules

## 5. Repair, review, query, SARIF

- Repair targets remain finding-key2. Unmatched → `REQUEST.PRECONDITION_FAILED` / `REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE`.
- Several configurations, one fingerprint: compatible metadata (ruleId, subjectPath, kind, qualifiedName, ruleClosure) or `REPAIR.TARGET_METADATA_AMBIGUOUS`. Do not collapse `parameterDigest`.
- Candidates: matched group-by-fingerprint **after** BaselineEntry-field agreement, one logical `candidateId` carrying **all** `findingIds` and per-occurrence parameters; unmatched stay one candidate per findingId. No representative findingId may drop other configuration evidence. Reviewed-clone suppression is keyed by that logical `candidateId`; fingerprint suppression does not hide unmatched findingId candidates.
- Query `findingId` locates any occurrence; `fingerprint` locates matched configurations only.
- Graph query (`graph-query:3`, `query-projection-contract.v3.md`): `graph.neighbors|path|reach` use native endpoints, closed per-op params, admitted-Run snapshot join, vertex-domain endpoint admission, single visited-endpoint budget, and mandatory retained Coverage/deficiency disclosure. Other 17 operations keep their existing owners. This unit does not implement a parallel absence evaluator.
- `project_finding_surfaces` is the intermediate host row (`FindingSurface`), **not** SARIF. `project_sarif` emits SARIF 2.1.0 (`sarif-adapter:2`): one result per finding3, citations from `evidenceRefs`, message properties from the generic-7 parameter record, `partialFingerprints` only when matched.
- Envelope AnalysisResult still uses FindingSurface. Do not claim SARIF conformance from a custom row.
- No automatic source edit.

## 6. Output bound

Overflow of array/C-byte materialization uses existing **`OUTPUT.SERIALIZATION_FAILED`** with `faultCause=output-serialization`. Not `HOST.IO_FAILURE`.

## 7. Per-row required parameters (root-owned registry note)

`requiredForEvaluatorMajors: [3]` on EnumerationPlanV1 and EvaluatorEmissionPlanV1 rows. Other consumers keep class-wide zero-legal. This projector does not mutate the payload registry.

## Appendix — NEW public keys/routes (root integrates)

This unit does **not** edit `public-detail-registry.v1.json`. Isolated `common:3` DomainDetailCode includes the members so StepTermination can carry them. Root must register:

| DomainDetailCode | D9ErrorCode | class | faultCause | When |
|---|---|---|---|---|
| `BASELINE.ENTRY_PROJECTION_CONFLICT` | `CONFIG.INVALID` | request-rejected | none | BaselineEntry field or legacyFingerprint presence disagreement |
| `BASELINE.SCHEMA_MAJOR_UNSUPPORTED` | `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` | request-rejected | none | baseline/comparison schemaMajor ≠ 2; never `[]` coercion |
| `COMPARISON.CORRESPONDENCE_INCOMPLETE` | (comparison indeterminate; existing `VERDICT.INDETERMINATE` reason when that is the sole signal) | indeterminate | none | unmatched or populationUnknown on a gating rule, no matched fail |
| `REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE` | `REQUEST.PRECONDITION_FAILED` | request-rejected | none | fingerprint-targeted action on unmatched / missing matched fp |
| `REPAIR.TARGET_METADATA_AMBIGUOUS` | `REQUEST.PRECONDITION_FAILED` | request-rejected | none | multi-config same fp, incompatible path/kind/rule metadata |
| `EVALUATION.WORK_BUDGET_EXHAUSTED` | (sealed Run may reuse D9 deficiency `budget-exhausted`) | indeterminate | none | evaluator work-unit preflight; remedy is raise analysis.budget — not native provider install |
| `EVALUATION.OUTPUT_BOUND_EXCEEDED` | `OUTPUT.SERIALIZATION_FAILED` | operational-failed | `output-serialization` | array/C-byte bound; never HOST.IO_FAILURE |
| `EVALUATION.FINDING_JOIN_REFUSED` | `CONFIG.INVALID` | request-rejected | none | duplicate findingId, parameter/preimage/subject join |
| `EVALUATION.MIXED_OUTPUT_MAJOR` | `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` | request-rejected | none | run2/finding2/subject2 or mixed output prefix |
| `EVALUATION.PROOF_VERDICT_INCONSISTENT` | `CONFIG.INVALID` | request-rejected | none | admitted proof verdict disagrees with policy-derived verdict |
| `EVALUATION.PROJECTION_INPUT_INCOMPLETE` | `REQUEST.PRECONDITION_FAILED` | request-rejected | none | missing required current/baseline/custody/pivot/ruleResults fields; supplied derived presence |

Do not add a D9 family. `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` **is** an existing D9ErrorCode member. `CONFIG.INVALID` is both an error code and a DomainDetailCode; it is **not** an arbitrary DomainDetail for evaluator3 projection refusals.

Current-run verdict (admitted policy, not `ruleResults.gating`):

- gating = `enabled AND gate AND severity >= gateSeverityAtLeast`
- fail iff gating and live unwaived findings
- indeterminate iff a gating rule has admitted `ruleResults.outcome=indeterminate`, **or** `executionDeficiencies`, **or** `evaluationState=budget-exhausted`
- advisory live findings do not fail; `ruleResults.outcome` is not a gating switch
- optional `proof_verdict` must equal the derived verdict

This unit consumes **admitted proof results**, including the required execution-inputs manifest and emitWhen root `p` values. Foundation owns origin Run close/replay (`close_run` → full replay). Passing `check-workflow-projection.v3.py` does **not** establish complete admission.

Checker output is stdout or a newly selected `--output` report path. Historical review receipts remain unchanged.

## 8. Admitted-run adapter (`project_admitted_run_v3`)

Public entry: `identity-model.v3.close_run` (full semantic replay). `open_run_closure` stays owner-internal.

Then read the admitted Plan policy blob, the selected `evaluator-emission-plan` parameter, proof `findingIds` / `ruleResults` / `waivedFindingIds` / `executionDeficiencies` / `evaluationState` / `verdict`, and construct occurrences with complete finding preimages, parameter records, and fingerprint descriptors. Drive existing baseline-entry, candidate, SARIF, and current-verdict projections. No producer `verified` flags, expected finding lists, or `ruleResults.gating` fallbacks.

Ordinary analysis may select **zero** ScopeDocumentV1 parameters. Baseline **entry** projection does not require one. Baseline **artifact adoption** does, via the existing `verify_scope_parameter_binding` law. This adapter does not change that join, does not invent `exportedAtUtc`, and does not treat missing ScopeDocument as successful adoption.

Foundation `close_run` is the strong public check. The execution-inputs manifest is a required admitted-Run field; a public projection that lacks it is incomplete, not omitted admission. Synthetic `check-replay.v3.py` graphs are not real extraction qualification.

## 9. admitted-run / comparison / SARIF law

- For an indeterminate predicate root, current verdict unknown uses the composer `blocks()` law: `nonBlockingDisclosures` (today `cross-family-edge-not-owed`) never make a gating rule unknown. Import deficiencies block only when `evidenceKind` is required. Correspondence causes are not blocking unknown; they are unmatched/live findings.
- ComparisonDescriptor schemaMajor 2 carries `currentEvaluationState` and `currentExecutionDeficiencies` (exact source/cause). Execution unknown is independent of policy gating. Matched fail still dominates.
- Public adoption is `adopt_admitted_baseline_v3` (close_run + Plan policy/waiver/ScopeDocument/snapshot join, trusted custody). `adopt_baseline_v3` is an internal helper. `retentionPins` must equal the unique sorted `{run3} ∪ pivotClosure.closureId` set. Ordinary `project_admitted_run_v3` reports `scopeDocumentParameter=absent|selected` and does not emit an adoption error.
- `compare_v3` does not require E0–E3 maps before unmapped/schema/recipe whole refusal. Unchanged policy/scope/waiver/detector axes copy E4. `compare_admitted_v3` is the retained-run adapter. Unit `pivotPresence` maps are not full comparison evidence.
- SARIF adapter: waived findings emit `suppressions` (`kind=external`,`status=accepted`); `message.id` is defined in `messageStrings`; URIs are percent-encoded with `safe='/'` (colon is not a scheme). Adapter schema is not OASIS full-schema qualification. `serialization_overflow_termination` is evaluator3 `StepTermination`.

## 10. admitted comparison / verdict / pivot-run law

- Admitted-run current verdict: fail from policy-gating live unwaived findings; indeterminacy from admitted `ruleResult.outcome==indeterminate` (one semantic owner) plus execution/budget. Retained non-blocking or determinate-branch causes do not override outcome.
- `requiredCoverage` is derived from admitted outcome and required-evidence causes, not from inventory completeness alone.
- Comparison execution deficiencies copy the full foundation3 evaluation-deficiency record (`inputRefs`, `predicateId`, `nativeCause`, …).
- `compare_admitted_v3(..., pivot_runs={E0..E3: admitted Run})` binds section-3 substitutions (current snapshot; policy/scope/waivers/detector per axis). Incomplete pivot population is not false absence. `current_detectors` may only repeat admitted emission identity; `compatibleWith` requires authenticated provenance and is refused as an arbitrary map.
- PivotClosure successor includes `provider`. Host adapter rewrites closure platform `any` on **host comparison metadata only**; it does not mutate admitted closure descriptors, manifestDigest, or object-map identity. Untrusted caller `compatibleWith` is refused. `declared-compatible` is workflows-and-surfaces §2: the listing at `.opensip/detector-compatibility.json` in the admitted same closure tree names a baseline `closure2` at the same major. The current-trust receipt requires an admitted origin. An absent path supplies no declaration; a malformed present listing refuses. `closure.manifestDigest` is the separate component manifest body.
- Baseline/comparison refuse when ScopeDocumentV1 is not selected. `plan.scopeDigest` is not a substitute.
- `evidenceAvailability.relations` is derived from admitted selected views / `evaluationInputRefs`, not from scanning the ambient object map.

## 11. pivot presence / detector map / envelope / Boolean coverage

- E0–E3 measured presence uses the same `derive_current_matched` law as E4 (matched occurrences, `waivedFindingIds`, `emissionBindings`). Waived matched findings remain present; waiver status is `waivedC`, not absence.
- E0 detector join is the exact baseline selected `{detectorId → (closureId, semanticsMajor)}` map, not a subset of common IDs. Extra, missing, or major-disagreeing detectors refuse.
- `compare_admitted_v3` derives `detectorChanged` from that map. It does not hardcode false and does not copy E1→E0 for a changed detector. Unbound changed axes stay `null`; `null` is not false-absence.
- CommandEnvelope `kind=failure` requires `errors` and **prohibits** `run`, including a schema-valid AnalysisResult.
- Isolated DomainDetailCode prose preserves shared registration of `EVALUATION.INPUT_REFUSED`, `EVALUATION.SELECTION_LIMIT`, and `EVALUATION.REQUIRED_OUTPUT_OMITTED`.
- Determinate Boolean rule outcomes (`pass`/`fail`) keep `requiredCoverage=satisfied` even when nonblocking required-partial diagnostics are retained. `AND(false, partial-required-history)→pass` and `OR(true, partial-required-history)→fail` are not indeterminate coverage regressions.
- `derive_policy_result` / `admit_policy_result` remain root foundation APIs. They are consumed through their foundation owner.

## 12. pivot absence knowledge / pivot-only fingerprints / declared-compatible standing

- E4 / E0–E3 presence is ANY matched occurrence, including waived (`waivedC` is separate). Waived presence is distinct from suppression at the waiver axis.
- Pivot absence is per-fingerprint/per-rule: `true` = known hit; `false` only when that rule can prove complete negative from admitted emitWhen root `p` values for every selected subject (enabled, evaluated, complete population, every root determinate `true` or `false`, and that fingerprint absent from the exact admitted emitted set); otherwise `null`. Advisory pass is not inherently unknown. Strong-Kleene AND(false, required unknown) is determinate false while witnesses may retain unknown child causes. Optional unknown stays indeterminate. Incomplete enumeration on one row does not drop known hits on another. Unrelated unknown must not erase a known CODE-NET-NEW fail.
- Comparison universe is baseline entries ∪ current matched occurrences ∪ bound pivot matched fingerprints. A fingerprint that exists only on E0–E3 (disabled current, empty baseline, enabled E1) remains, with admitted pivot `(ruleId, detectorId)` metadata. A bug introduced and hidden by disabling the rule is `CODE-NET-NEW` with `subsequentDeltas` including policy, per workflows-and-surfaces §3. Disabled/unknown current must not erase a baseline gating unmatched obligation (`gateRuleUnder=baseline-or-current`).
- `command-inventory.v1.json` stays the historical major-1 artifact. `command-inventory.v3.json` is the evaluator3 instance (JSON renderer 3 / envelope 3). This unit does not rewrite the v1 instance.

## 13. pivot source-input join / declared-compatible body / wider scope

- E1..E3 re-evaluate retained **current** facts. Bind snapshot, resolvedConfig, nativeContext, Plan-selected imports, foundation `plan.scopeDigest`, capability bytes, closures, fact/coverage evidence, and inventory rows (parent `planId` stripped). policy/waiver/emission/analysis-spec/rule-program are the axis substitutions and may remint Plan locators. A same-snapshot same-policy pivot with a different admitted import/coverage/config is refused (`EVALUATION.FINDING_JOIN_REFUSED`).
- E0 may use the prior detector: detector closures are excluded from the E0 source-input map. Current native/provider/toolchain equality is not required on E0.
- Absence False is not claimed for a fingerprint whose `subjectPath` is outside the attested inventory examined extent or the pivot ScopeDocument, unless foundation `plan.scopeDigest` covers the path and inventories are complete (deleted under a covering census). Snapshot `sourceInventory` membership is not extraction proof. A wider baseline ScopeDocument over the same snapshot is a real E2 counterfactual; a ScopeDocument wider than the admitted extraction is typed missing-extent, not false absence.
- `DetectorManifestV1` is **not** `closure.manifestDigest`. That digest is the DR-103 component-manifest body. The listing is the reserved tree file `.opensip/detector-compatibility.json` on the admitted same `closure2`.

## 14. sidecar locators / proof-root absence / required manifest / TCB body

- Sidecar and candidate records (`target-attribution`, `incoming-search`, `candidate-producer-result`) bind `planId` / `executionPlanId`. Legitimate policy/scope/waiver remints must join on stripped parent locators. Preserve sourceFactId, universes, member/group, source-body, coverage, and other native evidence. `incoming-search.expectedInventoryRefs` expand to stripped inventory bodies (those C hashes remint with planId). `candidateResultRefs` expand the same way. Groups remain semantically identical when they do not carry parent locators.
- Negative knowledge is the admitted proof emitWhen root `p` for every selected subject, not an advisory `pass`/gating flag or arbitrary retained child deficiencies. Complete determinate roots and the exact emitted set prove absence for a non-emitted fingerprint, even if another subject has a known finding. Advisory all-false roots also prove absence. Boolean AND(false, required unknown) is determinate false. Optional unknown remains true-indeterminate. A live known hit remains usable when other roots are unknown.
- Execution-inputs is required on a public admitted Run. Missing capture is `EVALUATION.PROJECTION_INPUT_INCOMPLETE`.
- Host-only compatibility projection after existing TCB admission of the same `closure2`: `{closureId, componentManifestDigest, listing:{path,sha256,bytes}, trustOrigin, compatibleClosures, tree, platform, protocolMajor}`. `trustOrigin` is retained-generation / installed-signed-release / signed-closure-bundle. Select the unique reserved tree path; compare exact retained blob SHA-256 and length. Path absent is no declaration. Empty `compatibleClosures` is a complete listing. Present malformed / unrecognized / missing / hash-or-length mismatch refuses (never silent no-declaration). Request maps never assert trust or admission. Signature verification remains security TCB.
- ScopeDocument matching reuses owner `W.in_scope` / `W.glob_match`. `**/*.ts` matches root `a.ts`.
- A now-absent path inside a complete covering foundation scope may be determinate absence (deleted-file CODE-FIXED). A path outside the foundation walk is unexamined even if a wider ScopeDocument names it.

## 15. listing tree-path / covering-scope deletion / candidate locators

- Security v6 finding: three-field DetectorManifestV1 cannot occupy `closure.manifestDigest`. W consumes the admitted same-`closure2` tree commitment; security TCB authenticates the component manifest and platform tree.
- Candidate-producer-result parent locators remint with Plan; stripped evidence joins E1..E3 the same way as other sidecars.
