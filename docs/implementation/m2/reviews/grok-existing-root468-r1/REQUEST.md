Grok review law proposal 468 r1 (existing-root admission after creation, diagnostics and routing). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-existing-root468-r1. Law review. You may read code; do not run product cargo. Do not read or print the private 413 UUID fixture.

Subject: docs/implementation/m2/existing-root-admission-468/PROPOSAL.md (pin in hashes.txt). **Items 2, 6, 7 and 9 are owner decisions made on 2026-09-27.** Item 2: borrow the barrier qualification from InitialPlatform. Item 6: three NEW public codes rather than reusing rows. Item 7: defer the backup-status envelope field. Item 9: the 458c direction. Review how they are written and scoped, and whether the new code names, classes and exits fit the existing vocabulary. Do not re-decide the choices.

Context:
- owner.md §5–§7 (docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md; the durable write gate around lines 103–105)
- laws 464 (decisions 3 and 6) and 467 (items 4, 9 and 11)
- security-and-lifecycle.md §S12 (about lines 1298–1313)
- schemas/sources/common-v4.schema.json (DomainDetailCode, about 634–635)
- public-detail-registry.json and diagnostic-routes.json in initial-root-binding-owner-selection-v1, and its doctor reference (check_doctor.py, doctor-cases.json)
- installation_publication.rs (Outcome)
- installation_observation.rs (InstallationReadFence)
- initial_platform.rs

## Decide

- Is the gate order in item 3 exactly owner §5?
- Is item 2's capability tightly scoped?
- Is "complete I" (item 5) right, and is the doctor note rule exactly the reference's?
- Item 6: do the three code names follow the existing naming (for example INSTALLATION.NOT_INITIALIZED and storage.backup-choice-required)? Are their classes, exits and fault causes right? Are the existing-row mappings right?
- Item 8: is the golden wording right?
- Is anything missing?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" (id, title, failureScenario) and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
