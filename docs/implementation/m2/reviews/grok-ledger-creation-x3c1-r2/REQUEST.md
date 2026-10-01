Grok re-review: X3c-1 r2 (ledger creation) after Grok's r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-ledger-creation-x3c1-r2. If you build, use a CARGO_TARGET_DIR under it.

Subject: the worktree `/Users/sb/code/opensip-ai/opensip-x3c1` (base 5b5f04c). Pins are in hashes.txt. Save the diff as product.diff and report its sha256. The r1 review is `reviews/grok-ledger-creation-x3c1-r1/`.

## Changes

- **RF-1.** On creation, every engine error before `COMMIT` goes through `busy_or_sql`: `SQLITE_BUSY` and `SQLITE_LOCKED` are Busy, and the rest are host I/O. `configure_engine`'s non-SQL refusals on the new file are host I/O. A non-WAL mode, or a non-selected schema, stays `LEDGER.CORRUPT`.
- **RF-2.** A new `Custody(subject)` row (468c's custody arm). The kind refusals are split. Subjects:
  - `private`, `not-fresh`, `symlink`, `not-a-directory`;
  - `mode` (non-regular), `volume-unsupported`, `name-changed`;
  - `required-files-changed` (identity changed).

  Custody I/O stays host I/O.
- **v89 changed in one row.** The `project_ledger_tests.rs` description said a foreign mode refuses as `LEDGER.CORRUPT`, which became false. That row is corrected and v89 is rebuilt (parent still v87). You accepted v89 in r1, so please confirm this.

## Checks

- Workspace: 1234/0, on two runs. project_ledger: 18/18. Clippy and fmt are clean.
- `check_package_edges` passes, and so does verify_scratch.

## Decide

Are RF-1 and RF-2 closed, and is v89's changed row right? Is anything new wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of ledger-creation-inventory-v89-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v89, parent (the v87 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.

Note: the product has since moved to 7e676a9 (X3b-1a, v91). Review the code as pinned. The v89 inventory will be rebuilt on the current parent before integration and re-confirmed separately.
