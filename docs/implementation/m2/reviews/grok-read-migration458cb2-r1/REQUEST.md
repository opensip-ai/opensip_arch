Grok review: 458c-b2, the migration of installation reads onto the observation session, and inventory v79. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-read-migration458cb2-r1.

Law: `docs/implementation/m2/read-premise-458c/PROPOSAL.md` r5, items 5, 6, 8 and 9.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-458cb2`, based on 0ce4c72. Its diff is product.diff in your output directory.
- **Arch:** v79, `read-migration-inventory-v79-subject.json`, and `read-migration-inventory-v79/`.

## What it does

- **`InstallationReadFence`.** It is rebuilt on a new `ReadSession` (`custody/installation_read.rs`), which holds the complete I admitted by `ObservationSession` (fence, retained chain, account, receipt) and that session's ledger.
  - `acquire()` replaces `try_acquire(supplied_groups)`: receipt, then session, then I must be complete. Refusals use item 6 rows.
  - `capture_leaf`, `capture_descendant`, `recheck` and `ProvisionalHeldFile` keep their shape.
- **Captures.**
  - They open only through the retained I and its retained descendants, charged before each step.
  - Directories are judged private with an exact name, a check added because APFS is case-insensitive.
  - Files are judged private, regular and capped, then named, checked for filesystem, read, judged again, and reopened by name to confirm identity.
  - A failed capture is a value, and the full recheck (fence, the observation's required files, every file captured so far) runs after it. Any refusal latches.
- **`HeldFence` view.** A new view, implemented by `SuppliedInstallationFence` for supplied-root tests and by `ReadSession`. The trust captures take `&dyn HeldFence`, and `Budget::charged(sink)` sends the trust readers' charges to the session's one ledger.
- **Unchanged consumers.** The host consumers and storage `native_marker` have no source change.
- **Pin.** A test scans the production text of every reader, across host, storage and security, and fails on `NativeInstallationFence`, `NativeInstallationRoot`, `SuppliedInstallationFence`, `inspect_directory_path`, `native_guard` or `fixture_at`. It fixes the one entry point as `InstallationReadFence::acquire`.
- **Tests.** They publish a real P0 through the new `installation_read_fixture.rs`. The old tests used hand-built I trees without ACLs, which the charged walk refuses.

## Judgment calls: please rule on each, against the law

1. **Light held-fence check.** Between full rechecks, the held-fence check only confirms that the lock descriptor's name and the one-link regular file under the retained I are unchanged, at about 10 edges. Mode and ACL are left to the full recheck, which runs after every capture. A fence mode change is therefore caught at the next full recheck. The reason is that capturing the ACL on every trust-reader recheck cost about 280 edges each, and one census test reached 105k of the 131,072 edges.
2. **No chain re-walk in capture rechecks.** `ProvisionalHeldFile::recheck` covers the fence, its edges and its file only. Chain changes are caught by the full recheck after each capture. Measured on a deep scratch home: admission 8,514 edges, one capture including its full recheck about 3,400, and one capture recheck 273.

   **Budget risk:** at about 3.4k edges per capture, roughly 35 captures fit in one session. Is that bound acceptable under law items 5 and 6 for the real trust and census readers? Or is a required finding needed now, for example scoping the full recheck per capture differently?
3. **Every capture failure latches**, including a missing file, after the full recheck.
4. **No supplied groups.** The read session has empty supplied groups, so every judgment is the owner's.
5. **Descendants under I** are judged by the private predicate. The trust captures' own file judgments stay on the legacy `inspect_operational_file` observers, now charged; retiring them belongs to 461.
6. **Stale descriptions.** Five descriptions are stale: `installation_observation.rs`, `installation_session.rs`, `read_premise.rs`, `native_read_session.rs` and `installation_fence.rs`. The plan is a later contract successor, as in 468a.

## Checks

- Workspace: 1123/0, on two runs. Migrated readers: 30/30.
- Clippy and fmt are clean.
- `check_package_edges --lane host` passes. The rust-provider lane refuses the same way on untouched main.
- `verify_scratch` passes with v79.

## Decide

- Does the migration satisfy law item 8, with no production path to the uncharged fence or re-walk?
- Are the captures correctly charged, rechecked and latched per items 5 and 6?
- Rule on the judgment calls, especially 1 and 2 and the budget bound.
- Are v79 and the inheritance right?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of read-migration-inventory-v79-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v79, parent (the v78 pin), successorRecord (the pin of read-migration-inventory-v79/successor.json)}.

Write REVIEW.md and review.json. Do not commit.
