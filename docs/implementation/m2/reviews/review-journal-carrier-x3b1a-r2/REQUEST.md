REVIEWER re-review: X3b-1a r2 (journal carrier) after Grok's r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. If you build, use a CARGO_TARGET_DIR under it.

Subject: the worktree `/Users/sb/code/opensip-ai/opensip-x3b1`, rebased onto 5b5f04c (X4T-0 integrated, inventory v87 selected). Pins are in hashes.txt. Save `git -C <worktree> diff` (new files are intent-to-add) as product.diff and report its sha256. The r1 review is `reviews/grok-journal-carrier-x3b1a-r1/`.

**Inventory.** The candidate is now **inventory91, parent inventory87**: `repository-file-inventory.v91.json`, `journal-carrier-inventory-v91-subject.json` and `journal-carrier-inventory-v91/`. It replaces v85, whose parent v84 is no longer current. v85 stays committed and is never selected. v91's three added rows are byte-equal to v85's (the ones r1 accepted), and every other row is v87's by value, with the 16 inherited rows projected onto v91. Its `evidence/verify_scratch.py` appends only v91 over the real lock.

## Changes

- **RF-1.** `floor_step` classifies the carrier right after the lease probe, before it opens, judges or reads the floor. A format-1 or format-2 carrier, or a format-3 footprint, refuses on its own row whatever the floor holds. Floor refusals apply only with no carrier or a current carrier.
- **RF-2.**
  - `SQLITE_NOTADB` goes to host I/O.
  - `MigrationRequiresValidation` goes to `MIGRATION.CORRUPT`.
  - A consistent migrated format 3, and formats 1 and 2, stay on F46.
- **Tests.** Three new tests: not-a-database, the migration-validation cases, and classification winning over a malformed, directory or custody-refused floor.

## Checks

- Workspace, two runs on 5b5f04c: 1236 passed / 3 failed, and 1235 / 4. Every failure is in the untouched `trust::root_payload::native_census` tests: `Fence(Root(Descriptor(ChangedDuringRead)))` from the shared temp directory, plus a visit count of 0. The same tests fail on clean main 5b5f04c (12/4 and 14/2) while other worktrees' test binaries run concurrently. No other test failed. The unit's own tests pass: carrier_floor 20/20, file_replace 3/3, locations 3/3.
- verify_scratch passes (v91 over the real lock, 61 inventory successors, 16 inheritance rows). The v91 projection gives 16 rows and refuses 83 corruptions. Live verify_design passes with v87.
- Clippy and fmt are clean.
- `check_package_edges` passes.

## Decide

Are RF-1 and RF-2 closed? Is anything new wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of journal-carrier-inventory-v91-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v91, parent (the v87 pin), successorRecord (the pin of journal-carrier-inventory-v91/successor.json)}.

Write REVIEW.md and review.json. Do not commit.
