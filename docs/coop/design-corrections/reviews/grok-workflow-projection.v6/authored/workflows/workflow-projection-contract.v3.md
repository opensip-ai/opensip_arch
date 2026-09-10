# Evaluator3 workflow projection — isolated contract v3

Standing: isolated successor for workflow surfaces over an **already admitted** evaluator3 finding/proof view. Not full Run replay, not native admission, not frozen/live/product. Root owns foundation composition, `identity-model.v3.py`, `workflows_model.v3.py`, and `policy-document.v2.schema.json`. Enumeration/atom remain other owners. This unit owns schemas under `schemas/evaluator3/` and the pure projection reference.

## 0. Corrected population lattice (MUST-2)

The independent critique merged pointer-absence with semantic incomplete. Root qualification, now normative here:

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
| graph-query | `...evaluator3:graph-query:2` | **2** | `params.findingId` |
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

Joins enforced here (cross-field joins are **code**, not JSON Schema):

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
- indeterminate iff gating and (incomplete enumeration or rule deficiencies), **or** `executionDeficiencies`, **or** `evaluationState=budget-exhausted`
- advisory live findings do not fail; `ruleResults.outcome` is not a gating switch
- optional `proof_verdict` must equal the derived verdict

This unit consumes **admitted proof results**. Root owns origin Run close/replay (`close_run` → full replay) and any input-execution-manifest proposal for view totality. Passing `check-workflow-projection.v3.py` does **not** establish complete admission.

Checker output: stdout, or `--output` under `grok-workflow-projection.v5/` only. It must not write historical v1/v2/v3/v4 receipts.

## 8. Admitted-run adapter (`project_admitted_run_v3`)

Public entry: `identity-model.v3.close_run` (full semantic replay). `open_run_closure` stays owner-internal.

Then read the admitted Plan policy blob, the selected `evaluator-emission-plan` parameter, proof `findingIds` / `ruleResults` / `waivedFindingIds` / `executionDeficiencies` / `evaluationState` / `verdict`, and construct occurrences with complete finding preimages, parameter records, and fingerprint descriptors. Drive existing baseline-entry, candidate, SARIF, and current-verdict projections. No producer `verified` flags, expected finding lists, or `ruleResults.gating` fallbacks.

Ordinary analysis may select **zero** ScopeDocumentV1 parameters. Baseline **entry** projection does not require one. Baseline **artifact adoption** does, via the existing `verify_scope_parameter_binding` law. This adapter does not change that join, does not invent `exportedAtUtc`, and does not treat missing ScopeDocument as successful adoption.

Root M3 `close_run` is the strong public check. Execution-input-manifest completion remains a separate blocker. Synthetic `check-replay.v3.py` graphs are not real extraction qualification.

## 9. v6 admitted-run / comparison / SARIF law

- Current verdict unknown uses the composer `blocks()` law: `nonBlockingDisclosures` (today `cross-family-edge-not-owed`) never make a gating rule unknown. Import deficiencies block only when `evidenceKind` is required. Correspondence causes are not blocking unknown; they are unmatched/live findings.
- ComparisonDescriptor schemaMajor 2 carries `currentEvaluationState` and `currentExecutionDeficiencies` (exact source/cause). Execution unknown is independent of policy gating. Matched fail still dominates.
- Public adoption is `adopt_admitted_baseline_v3` (close_run + Plan policy/waiver/ScopeDocument/snapshot join, trusted custody). `adopt_baseline_v3` is an internal helper. `retentionPins` must equal the unique sorted `{run3} ∪ pivotClosure.closureId` set. Ordinary `project_admitted_run_v3` reports `scopeDocumentParameter=absent|selected` and does not emit an adoption error.
- `compare_v3` does not require E0–E3 maps before unmapped/schema/recipe whole refusal. Unchanged policy/scope/waiver/detector axes copy E4. `compare_admitted_v3` is the retained-run adapter. Unit `pivotPresence` maps are not full comparison evidence.
- SARIF adapter: waived findings emit `suppressions` (`kind=external`,`status=accepted`); `message.id` is defined in `messageStrings`; URIs are percent-encoded. Adapter schema is not OASIS full-schema qualification. `serialization_overflow_termination` is evaluator3 `StepTermination`.
