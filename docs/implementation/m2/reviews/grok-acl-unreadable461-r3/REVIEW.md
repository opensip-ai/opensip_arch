# Review: ACL omission unreadable 461 r3

Grok is the single reviewer. Claude Opus 5.5 leads. Law re-review of the implementation correction to the descriptor-observation pin and the subject-arm timing. No repository edits and no product cargo.

Subject `docs/implementation/m2/acl-omission-unreadable-461/PROPOSAL.md`, 13169 bytes, sha256 `19e150fa5898169c49614ea72646cea270416aa4e69351c81a154441b63bc15e`. `PROPOSAL-r2.md` is 12423 bytes, sha256 `00409486fa4adae5895fdaa9ac448e724b9ade4052dd1f664516b1338a14b714`. The accepted r2 subject was 12388 bytes, sha256 `fad51694be8825b5339f1f652895ac3ecc0521e55bd4b0506edd2e58cb597c8f`; the preserved file adds the acceptance stamp. The substantive diff is item 3 and item 6. Product HEAD is `d4239a540e37cbc2f1415e0e5edd040fb7a3fbfc`.

## Verdict

**ACCEPT.**

Both corrections are sound and fail closed. At `d4239a5` no choke-point `Refusal` reaches 468c.

## What holds

On this macOS 27.0 host a scratch file follows the item 6 split. After `chmod -N`, `filesec_query_property(FILESEC_ACL)` returns `present == 0` and the bounded capture is `NotReturned`. One added write allow makes `present` nonzero and the capture `Entries(1)`, with a mutation right, so the descriptor reader keeps that writer. Removing that only entry makes `present == 0` again, while the capture stays `Entries(0)`. A read-only allow (read, readattr, readextattr, readsecurity) makes `present` nonzero, the capture `Entries(1)`, and the mutation mask empty, so `descriptor_acl` keeps no writer. `Present(vec![])` is that readable ACL. The removed-last-entry file is `Omitted` at the filesec observer. `check_descriptor_observation` maps `Omitted` to `AclWrite::Unreadable`. Item 2 still returns `AclUnreadable` only after kind, owner, mode, and group pass, so an earlier refusal still wins, and the observation is never `Known` of an empty writer list. The capture path is unchanged: `external_ancestor_acl` judges `Entries(0)` as a present empty ACL, and 458 item 6 still qualifies last-entry-removed as present-empty on that capture.

No choke-point `Refusal` is an input of `gate_refusal` or `session_refusal`. Installation reads judge ancestors and private members from captures and publish through those two functions. `installation_routing` does not match `custody::Refusal`, `NativeRefusal`, or `DirectoryPathRefusal`. Trust policy capture returns `Error::File` and `Error::Directory` and has no 468c row. `SuppliedInstallationFence::recheck_held` does call `check_descriptor_observation`, and that fence has no production caller; its `Error` is not a 468c input. `InstallationReadFence` does not call the choke point. 461a therefore adds no subject arm. The subject stays `acl-unreadable`, hyphenated, not derived from `Refusal::code` (`ACL_UNREADABLE`). The first unit that routes a choke-point `Refusal` publicly adds that arm in its exhaustive match. The row remains request-rejected, exit 2, `CONFIG.INVALID`, `CONFIG.CUSTODY_REFUSED`. `CONFIG.CUSTODY_REFUSED` is the registered detail; the subject is its sub-detail. `ancestor-acl-omitted`, `acl-not-returned`, and the other existing subjects stay. A consumer that already reaches 468c through its own family keeps that family's row.

The r2 order, the `Known` pin and its ancestor placeholder, the consumer table, the project-root decision, and the static observation cost stand.

## Required findings

None.
