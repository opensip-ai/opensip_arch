Grok review: 461a, an omitted ACL is unreadable at the custody choke point. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-acl-unreadable461a-r1.

Law: `docs/implementation/m2/acl-omission-unreadable-461/PROPOSAL.md` r3 (accepted).

## Subject

The worktree `/Users/sb/code/opensip-ai/opensip-461a`, based on d4239a5. Its diff is saved as subject.diff in your output directory, and the pins are in hashes.txt. It changes 19 existing files and adds none. No inventory successor is proposed, because every changed file's description stays accurate; please confirm that.

## What it does

- **Platform.**
  - `DescriptorAcl { Omitted, Present(Vec<AclWriter>) }` replaces `possible_acl_writers` (field `acl`).
  - `macos::descriptor_acl` returns `Omitted` when the ACL is absent. NOACL and malformed ACLs stay errors.
  - Every two-sample comparison now compares `acl`: macos_loader in both places, `directory_name_scan`, `native_current`, `directory_record_capture` and `native_record_capture`.
- **Choke point.** `check_descriptor_observation` maps `Omitted` to `Unreadable` and `Present` to `Known`. The arm order and the `check_external_ancestor` placeholder are unchanged.
- **No 468c arm,** per r3 item 3.
- **Pins:**
  - every scope and `waive_owner`;
  - the refusal order (NotDirectory, ForeignOwner, OthersWrite and GroupWrite win);
  - a source pin: one `Known(` in the choke point from `Present`, one named placeholder, `possible_acl_writers` gone;
  - the platform facts per r3 item 6.

## Test changes: please scrutinize

1. **A test-only ACL scratch horizon.** `test_scratch::acl_scratch()` creates a per-process base with an inheritable owner entry (`readattr`, naming no writer). Under `cfg(test)`, the chain check skips only the real system ancestors of that base, by device and inode, on the opted-in thread, because `/`, `/private` and `/var/folders/...` cannot be given an ACL. Everything at and below the base is judged normally. Is this strictly test-only, with no path into production? Is it keyed tightly enough (identity, thread, opt-in), and does it hide anything the tests should be asserting?
2. **Rewritten tests.**
   - root-only observation now refuses `/`;
   - policy capture of `/` and `/etc/hosts` now refuses at `/`, with retention and exact bytes moved to a scratch file;
   - storage's `observe_marker` tests refuse at `/` before any read.
3. **Fixture fixes.** Marker files and the census `empty_bucket` directory get the zero-rights owner allow, and one ForeignOwner index test skips the real ancestors above the base.

## Checks

- Workspace: 1142/0, on two runs. Clippy and fmt are clean.
- `check_package_edges --lane host` passes.
- Live verify_design passes, with v80 selected.

## Decide

- Does it implement law 461 r3 exactly, with no remaining path that reads omission as "no writers"?
- Is the test horizon sound?
- Is it right to skip inventory v81?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256" (the sha256 of subject.diff). Write REVIEW.md and review.json. Do not commit.
