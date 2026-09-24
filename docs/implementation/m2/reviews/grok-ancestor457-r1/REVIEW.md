# Review: external-ancestor custody from the bounded ACL capture, 457 r1

Grok is the single reviewer. Claude Opus 5.5 leads. No repository edits, commits, or pushes. The report is only this directory. The native lane is released with this report.

## Verdict

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/security/src/custody.rs` (`ee7c51db…`, 56138 bytes) and `crates/security/src/private_access.rs` (`a83b9d17…`, 39176 bytes) on product `1b3a3c6` | **ACCEPT-UNIT, this source boundary only** | none |

`review.json` carries top-level `"verdict": "ACCEPT-UNIT"` and `"requiredFindings": []`.

This is a read of one directory descriptor. It does not admit a path, a parent chain, or a creator. Probe 457 remains true: H, Library, and Application Support can pass because their stock ACL is a group deny of delete, while `/` and `/Users` omit the ACL and this check refuses that omission.

## Answers

1. **Read-only rights.** The mask is list/read-data (bit 1), search/execute (bit 3), read attributes (bit 7), read extended attributes (bit 9), read security (bit 11), and synchronize (bit 20). Every bit in `KAUTH_VNODE_WRITE_RIGHTS` sits outside that mask, including add-file, add-subdirectory, delete, delete-child, write data, append, write attributes, write extended attributes, write security, take-ownership, link-target, and check-immutable. Synchronize is the Windows interoperability bit and does not change the directory. Search is the traversal the owner text allows on a reused external ancestor. Search-by-anyone, no-immutable, the generic access bit, and every undefined bit are treated as writes. No directory-changing bit is classified as read-only.

2. **Unreadable ACLs.** `NotReturned` and `NoAclSentinel` return `AclUnreadable` before any entry is consulted, including when the entry callback supplies a foreign allow. `Entries(n)` with a missing entry, an unknown flag bit, or a kind other than allow or deny is also `AclUnreadable`. None of those states return success. A present empty ACL (`Entries(0)`) can succeed, because that is a readable ACL with no grants.

3. **Deny and inherit-only.** A deny does not create a write grant, and the mode check still refuses group and other write bits. An allow is not cancelled by a deny. An inherit-only allow of a write right is refused. That ACE does not grant on the directory itself, and it can pass the write to a new child. Refusing it is the conservative reading of “no ACL write grant to any other principal” on an ancestor that will contain new children.

4. **Authority.** Nothing calls the new functions. `check` is invoked with an empty trust-group set and no owner waiver, then the capture is judged separately so an empty writer list is not the ACL result. `observe_external_ancestor` captures once, on the caller’s scope, and changes nothing. Success is a predicate result. The comment leaves the name binding and rechecks to the caller.

## Subject

Product HEAD is `1b3a3c6`. `git status` shows only the two paths. Both byte pins match the request. `private_access.rs` only publishes the four ACE flag constants. `custody.rs` adds `check_external_ancestor` and `observe_external_ancestor`. The legacy `observe_descriptor` path is untouched. Probe 457, in `docs/implementation/m2/ancestor-acl-probe-457/RESULT.md`, is the host observation the request includes. It is not a profile qualification.

Mode and owner refusals run first. A group-writable directory whose ACL was omitted is `GroupWrite`, not `AclUnreadable`. It is still refused. Root may own the directory and may hold a write ACE. Any other principal’s write ACE is `AclWrite`. Project trust groups are not consulted.

## Replay

Rust is `/opt/homebrew/Cellar/rust/1.95.0/bin`. Commands ran in the product checkout.

| Command | Exit |
|---|---|
| `rustfmt --edition 2024 --check` on both paths | 0 |
| `cargo test --locked --offline -p opensip-security --lib external_ancestor` | 0, 9 passed |
| `cargo test --locked --offline -p opensip-security --lib custody` | 0, 55 passed |
| `cargo test --locked --offline -p opensip-security --lib private_access` | 0, 10 passed |

The native ancestor test admits the stock deny-delete ACL and a read-only allow, and it refuses omission, add-file, add-subdirectory, delete-child, write-security, and an inherit-only add-file. An unpaid capture returns `Budget` and latches the ledger. I did not run a separate mutant copy. Those tests already kill omission-as-success and inherit-only exemption.

## Observations

- The root-to-H chain still cannot pass. `/` and `/Users` omit the ACL, and this unit correctly refuses that. The qualified omission premise remains outside this unit.
- The legacy descriptor reader still turns omission into an empty writer list. This unit does not use that reader, and it does not repair it.
- A successful result does not say the directory is the account home, `Library`, or `Application Support`. The caller still has to bind the name.
