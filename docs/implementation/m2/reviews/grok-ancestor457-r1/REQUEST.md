Grok source review of external-ancestor custody from the bounded ACL capture, unit 457 r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-ancestor457-r1. You own the serial native lane until your report is written. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline in /Users/sb/code/opensip-ai/opensip. Do not read or print the private 413 UUID fixture.

Product HEAD is 1b3a3c6. The uncommitted difference is:
- crates/security/src/custody.rs SHA256 ee7c51db8d176505fd8e7fff5c52f0974e48783e366bb6e9fc3a4a478d512c75, 56138 bytes
- crates/security/src/private_access.rs SHA256 a83b9d174e66a69934dc6b5b3ac0100d38c7299bf5713e575dde63856a170278, 39176 bytes

## The unit

Owner text: docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md §1b in /Users/sb/code/opensip-ai/opensip_arch. For H and external ancestors it requires a directory, owner invoking UID or root, no group or other write, readable ACLs, and no ACL write grant to any other principal. Project trust groups never waive this.

- `check_external_ancestor(metadata, state, entry, invoking_uid)` runs the existing pure `check` with `Scope::Directory`, no authorized groups and no owner waiver, with an empty known-writer list, so mode and owner refusals keep their order. It then judges the ACL from the capture.
- Omission and the NOACL sentinel return `AclUnreadable`. The captured state fixes the entry count; a missing entry, an unknown flag bit, or a kind other than allow or deny also returns `AclUnreadable`.
- An allow entry whose rights include any bit outside list, search, read attributes, read extended attributes, read security and synchronize is a possible write. Unknown and generic bits count as writes. Inheritance flags do not exempt it. Only the invoking user or root may hold such an entry; a group, another user, or an unresolved principal returns `AclWrite`. Deny entries are ignored.
- `observe_external_ancestor` captures once with `capture_descriptor_acl_accounted`, charged to the caller's scope, then judges. It creates and changes nothing.
- private_access.rs only makes four ACE constants `pub(crate)` so both modules share them.

Nothing calls the new functions yet. The legacy `observe_descriptor` reader and every existing custody caller are unchanged.

Probe 457 (docs/implementation/m2/ancestor-acl-probe-457/RESULT.md) is part of the subject. On this host H, Library and Application Support carry the stock group deny-delete ACL, while `/` and `/Users` omit the ACL. So this check admits the stock fixed ancestors, but the root-to-H chain cannot pass until a qualified omission premise exists. That premise is not part of this unit.

Lead saw these pass: `cargo test -p opensip-security --lib external_ancestor` (9), `--lib custody` (55), `--lib private_access` (10), `cargo check --workspace --all-targets`. Clippy on opensip-security reports two warnings, both in files this unit does not touch.

## What to decide

1. Is the read-only rights set right? Name any bit that can change a directory, its entries or its ACL and is missing from the write side.
2. Can any path admit an ancestor whose ACL was omitted, sentinel, truncated, or uninterpretable?
3. Is ignoring deny entries correct for a writer-exclusion predicate? Is treating inherit-only allows as writers the right conservative choice?
4. Does anything here read as parent admission or creator authority?

Read the diff against 1b3a3c6. Replay rustfmt --edition 2024 --check on both paths and the three test filters above. Mutation probes are welcome on a copy. If you accept, review.json must contain top-level "verdict": "ACCEPT-UNIT" and "requiredFindings": []. Otherwise list each required finding with a failure scenario. Write REVIEW.md and review.json. Do not commit.
