Grok review the 463d code, r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-core-tree463d-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Law: 463 r3's core-tree custody bullet, and r5 amendment item 7 (docs/implementation/m2/initial-core-launch-463/PROPOSAL.md). Product HEAD 9f0b932. Subject: two uncommitted files, pinned in hashes.txt: crates/security/src/custody.rs and crates/platform/src/macos_image.rs. **The working tree also has uncommitted 458b decoder changes in crates/security/src/trust/root_payload.rs and admitted_profiles.rs. They are out of scope and will come to you separately; treat them only as the environment your replay runs in.** No file is added.

## Changes

- custody.rs, `CoreTreeKind { Directory, Regular }` and `check_core_tree_member(metadata, expected, acl_state, entry)`:
  - Symlink refuses first, then the wrong kind (NotDirectory or NotRegular).
  - Other write, then group write.
  - A regular file needs links == 1: 0 is Unlinked, and more than 1 is HardLinked.
  - Then the ACL, through the existing `external_ancestor_acl` with the member's own uid standing where the invoking uid stood. The effect: owner or root may hold write grants; any other principal's possible write refuses, inherit-only included; unknown flags refuse; omission and NOACL refuse.
  - Any owner is accepted.
  - A new test module `core_tree_tests` has 4 tests.
- macos_image.rs: `RunningImageObservation::capture_file_acl(&self, work)` is a bounded ACL capture of the retained executable descriptor, charged to `work`. The descriptor does not escape. The live test asserts the charge and the same device and inode.
- Nothing yet composes these into `InitialCore`. That is 463f.

## Lead's replay

core_tree 4/0; macos_image 5/0; security lib 449/0; clippy `-D warnings` and fmt pass.

## Decide

Does the predicate implement the law exactly, in the right refusal order? Is reusing `external_ancestor_acl` with the owner uid correct for files as well as directories, given the read-only rights mask? Is there any case where an owner's group, `everyone` or an unresolved principal passes wrongly? Is the capture honestly charged, and does it keep the descriptor private? Anything else wrong? Replay the platform and security libs, workspace clippy and fmt.

review.json must contain top-level "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS) and "requiredFindings". Write REVIEW.md and review.json. Do not commit.
