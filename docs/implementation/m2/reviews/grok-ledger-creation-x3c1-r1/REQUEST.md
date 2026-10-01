Grok review: the X3c-1 ledger creation code with inventory v89. The law X3c r7 is accepted. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-ledger-creation-x3c1-r1. If you build, use a CARGO_TARGET_DIR under it.

## Subject: X3c-1 code

Product: the worktree `/Users/sb/code/opensip-ai/opensip-x3c1`, based on 5b5f04c. Save its diff as product.diff and report its sha256.

Arch: v89 (parent v87, the selected inventory), `ledger-creation-inventory-v89-subject.json` and `ledger-creation-inventory-v89/`.

**What it adds.**
- **Security `store_custody.rs`:**
  - `create_or_admit_store_directory`, per 465 item 3: exclusive 0700 create with the zero-rights allow; admit only on a raw `EEXIST`; then the name, filesystem and both barriers;
  - `create_store_file` and `open_store_file`.
- **Storage `ledger_store/project_ledger.rs`:**
  - `ProjectStoreNames` (owner201 spellings) and a test-only `ProjectStoreLocation`;
  - namespace and object directory admission;
  - `create_or_open_ledger`, with outcomes Created, Resumed or Existing:
    1. exclusive create;
    2. WAL;
    3. the six pinned DDL fragments in one `BEGIN IMMEDIATE`;
    4. commit;
    5. namespace barrier;
    6. a reopen that requires the stored schema to equal the selected DDL.

    Only an empty file with no WAL resumes, and file identity is checked before and after.
  - `admit_attempt`: a durable `attempt_custody` row, `admitted`, for this namespace;
  - `ProjectLedgerRefusal::row()`.
- **`ledger_store.rs`:** `configure` is split, with no change for existing ledgers.

**Judgment calls: please rule on each.**
1. The WAL ordering, per the accepted X3c r7.
2. Item 12a's fixture is in the security crate's `cfg(test)`, which storage cannot reach, so storage uses its own scratch `I/stores/S` with a real `writer.lease` flock.
3. A new narrow public security API (`store_custody`) instead of a cross-crate test bridge.
4. Rows:
   - a failed creation `COMMIT` takes host I/O, because `DURABILITY.COMMIT_FAILED` is stated for the attempt row;
   - a store directory or file custody refusal, or a changed identity, takes `LEDGER.CORRUPT`, because item 10 names no custody row;
   - a malformed name takes Invariant.
5. Fixed SQLite charge ceilings.
6. The `-wal` and `-shm` files are 0600 without the zero-rights allow; this is the same open point as X3b-1a.
7. `crates/security/src/lib.rs` may need a merge later.

**Checks.**
- Workspace: 1231/0 on the clean run. One run failed only the known census flake (F3), which also fails on clean main. 15 new tests. Clippy and fmt are clean.
- `check_package_edges` passes.
- verify_scratch (v89) passes.

## Verdict files

Write REVIEW.md and one verdict file:
- `review.json`: "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS), "requiredFindings", "subjectManifestSha256" (the sha256 of ledger-creation-inventory-v89-subject.json) and "inventoryCandidateAssessment" {verdict, requiredFindings, path, bytes, sha256 of v89, parent (the v87 pin), successorRecord}.

Do not commit.
