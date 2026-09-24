# Ancestor ACL probe 457

2026-09-23, Claude Opus 5.5 as implementation lead. Read-only. The probe is a scratch crate that links the product's `opensip-platform` at 1b3a3c6 by path and calls `capture_descriptor_acl_accounted` once per directory, opened with `O_DIRECTORY | O_NOFOLLOW`. It prints kind, an owner class, permission bits, the capture state, and per entry the kind, flags, rights and a principal class. No uid, gid, UUID, inode, or home path is printed; the account home is written as H. The source is `probe-main.rs` beside this file. No product file changed. This host only; not profile qualification.

| Directory | Owner | Mode | ACL state | Entries |
|---|---|---|---|---|
| `/` | root | 0755 | NotReturned | — |
| `/Users` | root | 0755 | NotReturned | — |
| `/private`, `/private/var` | root | 0755 | NotReturned | — |
| H | invoking | 0750 | Entries(1) | deny, rights 0x10 (delete), a group |
| H/Library | invoking | 0700 | Entries(1) | deny, rights 0x10, a group |
| H/Library/Application Support | invoking | 0700 | Entries(1) | deny, rights 0x10, a group |
| H/Library/Application Support/OpenSIP | invoking | 0755 | NotReturned | — |

The ledger charged exactly one capture cost per directory.

## What follows

1. H and the two external fixed ancestors carry the stock "everyone deny delete" ACL. A check that refuses omission can still admit them.
2. `/` and `/Users` omit the ACL. Owner §1a step 5 admits the whole root-to-H chain, and §1b requires readable ACLs on external ancestors. Omission is not absence (root source findings 445; route 446). So the root-to-H chain cannot be admitted until a qualified platform premise says what omission means on the install filesystem. The current profile payload names `installRootFilesystems` only; it carries no ACL-omission statement. That premise is owned by `InitialPlatform` (owner step 4) and needs a profile-law successor. It is not supplied here.
3. An `OpenSIP` directory already exists on this host at 0755 with the ACL omitted. It holds a directory left by earlier review tooling. Under §1b `OpenSIP` is installation-owned and private. The creator must refuse it and never chmod, repair, adopt or delete it. The user decides what to do with it.
4. The legacy `observe_descriptor` reader returns an empty writer list when the ACL is omitted (`macos.rs` `descriptor_acl`, `present == 0`). The existing operational custody chain therefore passes `/` and `/Users` as having no ACL writers. That is the empty-writer-list substitution the retrospective names. It is recorded here. The new ancestor check does not use that reader.
