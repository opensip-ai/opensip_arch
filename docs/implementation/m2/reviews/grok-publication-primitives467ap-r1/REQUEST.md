Grok review 467a-p (charged stage, publish and file primitives) and inventory73, r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-publication-primitives467ap-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/initial-publication-467/PROPOSAL.md items 1, 4, 6 and 7 (accepted). Product HEAD f52e5eb. Platform crate only; the files are pinned in hashes.txt: new file_effects.rs, plus directory_publication.rs, work_ledger.rs, filesystem.rs and lib.rs.

## Summary

- **Stage creation.** `private_directory_stage_cost()` and `parent.create_private_directory_stage_reserved/_accounted(post)`: up to 8 nonce draws, mkdirat, open, kind checks and a binding recheck, all charged first. The fixed prefix is kept, mode 0700, and no ACL is added (security adds the zero-rights allow). The nonce and name builder is now one exact-capacity helper; the spelling is unchanged and pinned by a test.
- **Publication.** `exclusive_publication_cost()` and `stage.publish_exclusive_reserved/_accounted(name, post)`, with `DirectoryRenameFailure::class()` and a pure `classify_directory_rename(err, visibility)` returning `DirectoryRenameClass::{LostRace, NotPerformed, Indeterminate}`. LostRace is an OS EEXIST (not the synthetic kind) with visibility Unchanged. The loser is returned as an `Err`, which closes the scope: law item 7 ends the act; releasing the fence lock is uncharged. `publish_with` and its tests are unchanged.
- **File effects (file_effects.rs).**
  - `create_exclusive_regular_cost/_reserved`: O_EXCL, O_CLOEXEC, 0600, no-follow. A raw EEXIST gives `EntryExists` with the scope open.
  - `write_new_regular_cost(len)/_reserved`: pwrite and pread in 64 KiB chunks, where a short write or read is an error; the length is verified via fstat and the bytes are read back and compared; then the private `sync_file`, which is F_FULLFSYNC with no fallback on macOS (item 4). It returns a `FileBarrierReceipt` with `is_for`.
- **`ReservedPostchecks::prepaid(cost, |work| ..)`** runs charged work from a carved allowance. An overrun, including a swallowed error or an unwind, fails closed with ReservedPostcheck (item 6).
- **Tests:** listed in the implementer report. They include the loser route with a raw EEXIST, a moved stage giving NotPerformed, an injected EIO after rename giving Indeterminate, and an injected F_FULLFSYNC failure with no fallback.

Not priced: kernel and libc internals, error allocations, fd close. The publish name is charged at its 1024-byte maximum.

## Inventory73

v72 plus crates/platform/src/filesystem/file_effects.rs (adapter); 728 rows; the helper is byte-identical and gives PASS; scratch verify_design passed.

## Lead's replay

Platform lib 212/0. The workspace is green (`--no-fail-fast`). Clippy and fmt pass.

## Decide

Is every call and allocation charged first? Is the rename classification exactly item 7, with no path that treats an indeterminate rename as a loser or as success? Is the file barrier F_FULLFSYNC with no fallback? Is `prepaid` fail-closed in every case? Are the existing unaccounted functions unchanged in behaviour? Is v73 exactly v72 plus one row?

**Output format:** review.json must contain:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectManifestSha256": a single string, from subjects.txt;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of repository-file-inventory.v73.json, parent (v72 pin), successorRecord (the pin of the v73 unit's successor.json)}.

Write REVIEW.md and review.json. Do not commit.
