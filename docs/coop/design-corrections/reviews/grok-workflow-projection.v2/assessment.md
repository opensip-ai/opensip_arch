I’ll resume the same owned workflow-projection work, read the prior prompt and root decisions, then finish the files and run the checks.Partial files exist. I’ll read the current owned artifacts, root’s composition v4 and finding3 shape, then finish the checker so it actually runs.I’ll fix the remaining schema/model gaps (run3 pins, output-bound detail, opaque package paths), then create a 3.12 env and run the checker.Policy v2 still points at original common; I’ll add that foreign schema to the checker registry and catch unresolved refs.Bounded workflow projection for evaluator3 is in place and the checker ran: **82/82 passed**. This is not full Run3 replay and not application readiness.

Owned files:

- `docs/coop/design-corrections/workflows/schemas/evaluator3/` (isolated `$id` namespace)
- `workflow_projection_model.v3.py`
- `check-workflow-projection.v3.py`
- `workflow-projection-contract.v3.md`

Receipt: `grok-workflow-projection.v1/workflow-projection-report.v3.json` (`passed: true`, `count: 82`).

**v1 majors vs this profile** (consts in the real v1 schemas, not description-only):

| Artifact | v1 `schemaMajor` | evaluator3 |
|---|---|---|
| baseline descriptor | 1 | **2** (`unmatchedOccurrences` in H preimage) |
| comparison descriptor | 1 | **2** |
| graph-query request | 1 | **2** (`findingId`) |
| repair-plan descriptor | 1 | **2** (`evidenceRunId` is run3) |
| envelope | 2 | **3** |
| invocation | 1 | **3** |
| command-inventory | 1 | **3** |

Prefixes are exact `run3` / `finding3` / `evidence3` / `subject3`. Fingerprint stays `finding-key2`. Retention pins are `run3|closure2`, not a `run[23]` mix. Historical schemaMajor 1 is `REQUEST.SCHEMA_MAJOR_UNSUPPORTED`; missing unmatched is not `[]`.

**Projection laws exercised:** two configs, one fingerprint, different params group; `legacyFingerprint` presence/value disagreement refuses; unmatched current fail / audit correspondence-incomplete; path waiver can pass current while audit stays unknown; matched CODE-NET-NEW fail dominates unmatched unknown; optional unknown does not gate; zero findings with incomplete population stay unknown; `source-syntax-invalid` is enumeration-local, not native vocab; same packageName at two manifest paths yields two fingerprints via `finding.subject.logicalPath`; `subjectId` is opaque; SARIF one row per findingId, `partialFingerprints` only when matched; repair unmatched refuses; multi-config path mismatch refuses without collapsing params.

Output bound uses **`OUTPUT.SERIALIZATION_FAILED`** / `faultCause=output-serialization` with detail `EVALUATION.OUTPUT_BOUND_EXCEEDED`, not `HOST.IO_FAILURE`.

New DomainDetailCode members are in isolated `common:3` only; root still owns `public-detail-registry.v1.json`.
