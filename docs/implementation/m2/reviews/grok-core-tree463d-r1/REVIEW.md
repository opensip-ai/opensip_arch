# Review: core-tree custody 463d code r1

Grok is the single reviewer. Claude Opus 5.5 leads. Code review of the uncommitted core-tree predicate. No repository edits.

Product HEAD `9f0b932f87e4f6aa344c919dd231efa311390162`. The two pinned files match `hashes.txt`. `custody.rs` is 63757 bytes, sha256 `2e1b1d3aa91a814ce1a623effd5881c3c18b99bd2126578a7c1e121c9a9f4ac1`. `macos_image.rs` is 16663 bytes, sha256 `eca4fe5d2b831df6b4b8f95225431c5d74c45e848fe8e2cc3e3ec66e4dc00c5f`. No file is added. The working tree also has uncommitted 458b edits in `root_payload.rs` and `admitted_profiles.rs`. Those are the replay environment, not this subject. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`. Law is 463 r3's core-tree custody bullet and r5 amendment item 7.

## Verdict

**ACCEPT-UNIT.**

## Answers

`check_core_tree_member` is the law's predicate, and it is not `check_external_ancestor`. The refusal order is symlink, then the wrong kind (`NotDirectory` or `NotRegular`), then other write, then group write, then a regular file's link count, then the ACL. The kind-and-mode test passes a `NotReturned` capture and still receives those earlier refusals, so the ACL does not hide them. A symlink is `Symlink` for both expected kinds. A regular file with `links == 0` is `Unlinked` and any larger count is `HardLinked`. A directory is not held to one link.

Any uid is an acceptable owner, including root. The mode test is only the group and other write bits. Owner write remains allowed.

The ACL call reuses `external_ancestor_acl` with the member's own uid in the invoking-uid position. That is the right substitution for a tree whose owner may be any account. Root stays uid 0, so root may hold a write grant on a file the root does not own. The read-only mask is the same six bits already used for ancestors (list/read-data, search/read-attributes, read extended attributes, read security, synchronize, and bit 20). Every other rights bit is a possible write. A permit of any such bit refuses unless the principal is `User(owner)` or `User(0)`.

That covers the principals that could pass wrongly. The owning group is `Group(gid)`, which is not the owner user, so a write grant to it refuses. `Group(0)` refuses. `Unresolved` refuses. `everyone` is not a fourth principal: `mbr_uuid_to_id` yields a user, a group, or `Unresolved`, and a write grant on the last two refuses. Inherit-only does not exempt an allow. A deny is not a grant. A present zero-entry ACL admits. `NotReturned` and `NoAclSentinel` are `AclUnreadable` for both directories and regular files. Unknown ACE flags and an unknown kind are `AclUnreadable`.

`capture_file_acl` calls `capture_descriptor_acl_accounted` on `&self.file`. That reserves `descriptor_acl_capture_cost` before the native read. The returned sample is a `DescriptorAclCapture`; the descriptor does not escape. The live test captures the running image's file, sees the ledger's edge count rise, and checks the sample's device and inode against the retained metadata. Nothing here composes the predicate into `InitialCore`.

## Replay

- `cargo test --locked --offline -p opensip-platform --lib macos_image`: exit 0. 5 passed, 0 failed.
- `cargo test --locked --offline -p opensip-platform --lib`: exit 0. 171 passed, 0 failed.
- `cargo test --locked --offline -p opensip-security --lib core_tree`: exit 0. 4 passed, 0 failed.
- `cargo test --locked --offline -p opensip-security --lib`: exit 0. 449 passed, 0 failed, 2 ignored. This run includes the out-of-scope 458b files.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
