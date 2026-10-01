REVIEWER re-review: X3b-1a r2 (journal carrier) after Grok's r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. If you build, use a CARGO_TARGET_DIR under it.

Subject: the worktree `/Users/sb/code/opensip-ai/opensip-x3b1`, now rebased onto 8bfc78a (X2a integrated, v84 selected). Pins are in hashes.txt. Save the diff as product.diff and report its sha256. The r1 review is `reviews/grok-journal-carrier-x3b1a-r1/`. v85 and its arch pins are byte-identical to r1.

## Changes

- **RF-1.** `floor_step` classifies the carrier right after the lease probe, before it opens, judges or reads the floor. A format-1 or format-2 carrier, or a format-3 footprint, refuses on its own row whatever the floor holds. Floor refusals apply only with no carrier or a current carrier.
- **RF-2.**
  - `SQLITE_NOTADB` goes to host I/O.
  - `MigrationRequiresValidation` goes to `MIGRATION.CORRUPT`.
  - A consistent migrated format 3, and formats 1 and 2, stay on F46.
- **Tests.** Three new tests: not-a-database, the migration-validation cases, and classification winning over a malformed, directory or custody-refused floor.

Note: the tracked `evidence/verify_scratch.py` still appends v84, which is now selected, so it would trip its own assertion. A copy that appends only v85 passed. The tracked file will be refreshed at integration.

## Checks

- Workspace: 1232/0 on two runs. One earlier run had a single failure in the untouched `native_profile_census_later_file_fence_and_missing_bucket_changes_refuse`, which is known to be intermittent.
- Clippy and fmt are clean.
- `check_package_edges` passes.

## Decide

Are RF-1 and RF-2 closed? Is anything new wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of journal-carrier-inventory-v85-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v85, parent (the v84 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
