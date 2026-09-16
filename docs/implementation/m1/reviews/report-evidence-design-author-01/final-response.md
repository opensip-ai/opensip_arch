I've written a design candidate that closes RP-DO-03, 05, 09 and 10 with concrete owner records, report carriers and a reference model. Its strict pinned check passes (exit 0, `CHECK OK`), and a fresh copy of exactly the listed files gives a byte-identical result. It's in `m1-report-evidence-design-author-01/candidate/`, with `check-result.json` and `candidate-inputs.json` beside it. It's not approved: the owner changes it proposes (S1–S4 below) still need review and acceptance.

**Where I departed from the register's suggestions:**

- **RP-DO-03, coupling.** `UnitMembershipV1` can't give Rust package ownership: a file maps to the workspace unit, and `#[path]` or shared files defeat directory inference. Rust ownership comes from `SourceUnitOwnershipV1` rows whose path matches exactly and whose target is selected; the target's declaring manifest must then match a package inventory row. TS/JS uses the retained membership row. Importer paths come from the native symbol inventory rows; symbol spellings are never parsed. The report carrier has:
  - directional counts, with provenance duplicates kept distinct;
  - explicit unattributed, external and unknown buckets;
  - a blank cell that means only "no projected fact". Absence is claimed only when there are no blockers.

  No new public query operation is needed. S3 proposes a whole-view internal projection for host reporting.
- **RP-DO-05, entry points.** The summary field is only state and source, and nothing currently ties a recognition to a unit or Plan. I propose a per-unit `FrameworkRecognitionPlanV1` as a Plan parameter (S2).
  - **Identity effect:** PlanId and RunId change for every evaluator3 Plan. This is justified because FR-5 already requires recognizer changes to be Plan-visible, and reachability consumes entry points. Universe, fact, coverage and subject identities don't change.
  - **Historical Runs** show `not-plan-bound`; nothing is inferred for them.
  - **Custody:** parameter purged/expired/corrupt/missing gives `unavailable`.
  - **Explicit configuration** replaces recognized entry points.
  - **Traces** start only at a native reachability origin whose path is a retained entry point. A missing path is never reported as dead code.
- **RP-DO-09, metrics.** No new relation is registered. A closed catalog of five existing graph queries gives exact, lower-bound or unknown counts, labelled static projected counts. A zero supports absence only when exact with no limitations.
- **RP-DO-10, test reachability.** Imported `TestPayloadV1` isn't used as origin identity (free `testId`, file-level `subjectPath`, executed observation).
  - **Rust origins:** paths owned only by selected `test` targets. The set is always partial, because `#[test]` inside lib or bin targets isn't a target fact.
  - **TS/JS origins:** unit-relative paths matching the retained vitest-jest test globs.
  - **"No static path"** is only asserted when the reach is exact, unlimited and the origin set is complete.

**Finding in subject-05:** besides the `FeatureId` enum, the report schema pins `featureStates` per command in `/allOf/3..9/then/properties/featureStates/const`. Those arrays are shared with the other seven obligations. My patch uses row-removal ops with exact before/after values, and the check proves they commute with another obligation's removals on the same selectors.

**What the check covers:**
- Owner-schema validation of every mock record, and byte-identical regeneration of owner files and fixtures.
- The 22 glob-contract examples, cross-checked against the pinned `workflows_model.v1.glob_match`.
- Positive cases with exact expected values. Variants cover partial package inventory, recognition not-plan-bound/purged/partial, no reachability view, 101 origins, 100,001 call facts (lower-bound) and purged Run evidence.
- Refusal cases, each with its exact code: 44 document mutations and 14 recognition-record mutations.
- 6 host cases where a guessed attribution (directory prefix, symbol spelling, target-as-package, `main`/`page` entry names) passes the in-document checks. Only the host derivation refuses these, so they are marked host-asserted in the carrier.
- Subject-05 `audit-full` with the new panels validates under the patched schema.
- 47 external files pinned; no child processes.

**Limits:**
- The worlds and the mock graph owner are constructions following the cited laws. Target occupancy reconciliation is taken as given on facts.
- Agreement with the native and query owner models is by implementing their rules, not by running those models.
- No runtime, browser, generator, performance or Run replay evidence.
- My grep of the pinned docs found only D372 (in DR-122); I didn't locate the D369–D371, source45 or application46 records. As you instructed, I didn't treat DRAFT/CANDIDATE labels as rejection.

**Still needed:** acceptance of four proposed owner changes, and the integration duties listed in the register (budget priority, static parity, generator, coverage issues 2/4/8/9, identity sweep, retention, browser, measurement).
- **S1, native §8 prose:** paths in recognition are repository-relative; the owner model currently keys them unit-relative.
- **S2:** the identity registry row for the new Plan parameter.
- **S3:** query §8a, the internal whole-view projection.
- **S4:** the report schema patch.

I found no remaining blocker for these four features.
