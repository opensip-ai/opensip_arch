# Independent Grok review: fit-interruption01 original unit

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-fit-interruption-subject-01`
**Manifest SHA-256:** `bc90da6b5263cf88d37ea1f5d2196c19dae5c7722d602d0fe9f0514344bb2e0d`
**Members:** 24
**Verdict:** **ACCEPT WITHIN STATED REFERENCE SCOPE**

Narrow schema-fragment / binding-projection proposal for Q-FIT-1. Joint10 combined acceptance does **not** waive this unit and does **not** close Q-FIT-1. Later L02 root selection cannot excuse the deterministic missing `advisoryReport` member. This freeze is **not** a completed Q-FIT-1 correction.

## Custody

Verified before and after. Work used only `review/copy` and `review/probes`. Frozen subject not executed against and not written. Architecture, product, and historical bytes untouched. No modes or symlinks listed.

| Check | Result |
| --- | --- |
| Manifest | `bc90da6b…2e0d` matches declared and adjacent copy |
| Files | 24 listed = 24 walk |
| Pins | **9/9** |
| After | frozen hash unchanged |

## Original defect (preserved)

`fit/primary/signal-before-required-render`: completed query, committed Run, no `advisoryReport`. Planned request is placeholder `run3:bbbb…` / `prj1-aaaa…`, not the sealed Run/project. Unchanged `static_parity_text` raises `KeyError('advisoryReport')`. Independently reproduced. Report08 still treats Q-FIT-1 as an open omission permission.

## Proposed laws — adequate to integrate, not closed

| Law | This freeze |
| --- | --- |
| **Planning** | Closed host-only `FitQueryFromAnalysisParams`: `{kind:query, operation:candidate.list, sourceStep}`. Earlier analysis, explicit `dependsOn`, `dependencyGate=completed`. Golden already has that dependency; only the placeholder `request` is rewritten. Plan is not mutated into the resolved request. |
| **Dispatch** | Authoritative completed analysis → existing `GraphQueryRequestV1` with invocation `projectId`, source `runId`, `includeSuppressed=false`, best-effort, page size 100, no cursor. Ephemeral → no public request; unavailable-ephemeral-analysis; cannot fill an authoritative run envelope. Failed/skipped/cancelled analysis still blocked. |
| **Completed-response lifetime** | Dictionary handle `{requestId, stepId, executionId, report}` after admit/derive/summary join. Copied exactly into the interrupted run envelope. No re-query. Lost handle → `RequiredProjectionFailure`, query remains `completed`. |
| **Unavailable query** | `unavailable-query-result` with actual `cancelled`/`skipped`/`failed`/`rejected`, RunId, all parity fields null. Empty `[]`/`0` is not absence. Failed is not relabelled cancelled. Independent: leftover completed summary on a cancelled step still yields unavailable, not a sealed page. |
| **Failure carriers** | No `advisoryReport` (signal-before-first-step, first-step-rejected). Unchanged. |

**Adequacy.** These are sufficient *proposed* owner laws for parent succession. They are not product custody, not full invocation/page/native admission, and not renderer/browser qualification. Do **not** mark Q-FIT-1 closed.

**Required succession:** invocation `QueryParams` oneOf; envelope fit union + root allOf guard; inventory planning/parity prose; workflow dispatcher; report08 builders, admission, fixtures (replace placeholder request with a real bound page); compose timing/interruption successors; real private completion custody. Final majors chosen in joint source closure, not reused here.

Candidate-summary owner is AST-extracted (`command_surface_summary` and helpers only). Noncompleted tests are synthetic outcome edits, not re-admitted invocation records.

## Reproduction

Private copy, reference Python `-I -B`:

- `build_schema.py`: **three** fragments byte-identical (`f09e7b50…`, `478792be…`, `dcf06e82…`)
- `check.py`: **13/13**, 9 pins, actual `static_parity_text` for **36** interruption fixtures
- `mutants.py`: **11/11** targeted semantic witnesses

**Preserved first broad-control run** (`prior/mutants01`): 9/11. `resolved-project-is-placeholder` and `completed-report-dropped` produced `ERROR:` in unrelated tests, so the suite-wide `ERROR:`-absent predicate missed them even though the named witnesses also `FAIL`ed. Retargeted driver runs only the named witness and requires `FAIL:` without `ERROR:`. Classification accepted; not a remaining product defect.

## Independent probes (18/18)

Including original KeyError, placeholder mismatch, sourceStep identity, handle joins, lost-handle fault, leftover-summary cancellation, failed-not-cancelled, empty-list refusal, ephemeral, 36-golden fit-carrier split, prior-mutant classification, parent Q-FIT-1 still open, joint10 `reference-composed-review-pending`, L02 does not waive.

## Must-fix / should-fix

**Must-fix:** none in the stated reference scope.

**S1 (should-fix).** Standalone param schema uses JSON Schema `integer` without an exact-int type checker, so `sourceStep: 0.0` validates. `query_parts` requires `type(source_id) is int` and refuses. Tighten the fragment (or compose with the project integer checker) before product integration. Not a false-accept of a later source step.

## Remaining duties

Parent report builder/admission/fixture integration; full invocation/envelope majors with timing/interruption composition; private host completion custody (not dictionaries); full schema/native/run/page admission; every renderer format and browser. Joint10 remaining for Q-FIT-1 matches this. L02 selected policy is unrelated and does not close the missing-member defect.
