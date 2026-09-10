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

Known **attribution conflict** for the same `(universe,kind,nativeSubjectId)` or the same fingerprint identity with disagreeing fingerprint **preimages** is **input refusal**, never silently incomplete.

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
- `emissionBindings` keyed by ruleId (contributionId, ruleStableId, semanticsMajor, detectorClosure, stabilityClass, emissionProfile)
- `waivedFindingIds` exact list from proof
- `ruleResults` exact admitted per-rule results (enumeration + outcome + findingIds + deficiencies)

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

Unmatched occurrences are excluded from `entries` and retained in `unmatchedOccurrences` with findingId, ruleId, subjectId, subjectPath, severity, waived.

`adopt_baseline` remains a pure projection over caller-admitted policy/scope/waivers. Scope selection join reuses `workflows_model.v1.verify_scope_parameter_binding` when `analysis_spec` is supplied. Descriptor `schemaMajor` is 2; `runId` is run3; fingerprint recipe major stays 2.

## 4. Comparison

Reuse `workflows_model.v1.classify` / audit profiles / detector union **unchanged**. Pivot presence is over **matched fingerprints only**.

Then add typed unmatched/population deficiencies:

- unmatched records are not UNCHANGED / CODE-NET-NEW / CODE-FIXED / resolved
- gating `correspondence-incomplete` when unmatchedCount>0 or `populationUnknown` (including zero findings)
- advisory/optional-only does not gate
- **CODE-NET-NEW fail dominates** correspondence indeterminate (fail > indeterminate)
- default `code-regression`: new waiver does **not** suppress CODE-NET-NEW
- `full-current` / `report-only` (`current-only`): `newWaiverSuppressesCodeNetNew` as in source

Current-Run vs audit:

- live unwaived unmatched finding on a gating rule → current **fail**
- path waiver of that unmatched finding can make current **pass**; comparison stays correspondence-incomplete
- fingerprint waiver cannot cover unmatched
- incomplete population without a live unwaived finding → current indeterminate; comparison correspondence-incomplete for gating rules

## 5. Repair, review, query, SARIF

- Repair targets remain finding-key2. Unmatched → `REQUEST.PRECONDITION_FAILED` / `REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE`.
- Several configurations, one fingerprint: compatible metadata (ruleId, subjectPath, kind, qualifiedName, ruleClosure) or `REPAIR.TARGET_METADATA_AMBIGUOUS`. Do not collapse `parameterDigest`.
- Candidates: matched key=fingerprint; unmatched key=findingId. No fake fingerprint. Fingerprint suppression does not hide unmatched.
- Query `findingId` locates any occurrence; `fingerprint` locates matched configurations only.
- SARIF/envelope: one result per findingId; `partialFingerprints` only when matched.
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
| (no new detail) | `OUTPUT.SERIALIZATION_FAILED` | operational-failed | `output-serialization` | array/C-byte bound |

Do not add a D9 family. `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` **is** an existing D9ErrorCode member.
