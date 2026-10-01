# Review: ACL omission unreadable 461a r1

Grok is the single reviewer. Claude Opus 5.5 leads. Code review of the descriptor-observation choke point. No repository edits and no product cargo.

Worktree `/Users/sb/code/opensip-ai/opensip-461a` at `d4239a540e37cbc2f1415e0e5edd040fb7a3fbfc`, nineteen modified files and no additions. `subject.diff` is 60719 bytes, sha256 `6c4d74bca31f08798aa7ad69e2ab9c5452cba5464555e543d97d2514e717f65b`, and it matches `git diff HEAD`. Every pin in `hashes.txt` matches the worktree. Law 461 r3 is the accepted text plus the acceptance stamp. The real OpenSIP directory is absent.

## Verdict

**REQUIRED-FINDINGS.**

The choke point, the platform split, the test horizon, and the decision to skip an inventory successor are sound. `DescriptorAcl::Present`'s own comment still describes a removed last entry as a present empty writer list.

## What holds

`macos::descriptor_acl` returns `DescriptorAcl::Omitted` when `filesec_query_property(FILESEC_ACL)` reports `present == 0`. A null ACL and the NOACL sentinel stay `DescriptorObservationError::Acl`. A present ACL that ends at `EINVAL` returns `Present(writers)`, and the writer loop still skips an allow with no mutation right, so that ACL is `Present` of an empty vector. `possible_acl_writers` is gone. `macos_loader`, `directory_name_scan`, `native_current`, `directory_record_capture`, and `native_record_capture` compare `acl`. `Omitted` and `Present(vec![])` compare unequal. `descriptor_observation_cost` is unchanged.

`check_descriptor_observation` maps `Omitted` to `AclWrite::Unreadable` and `Present(writers)` to `AclWrite::Known(writers)`. `check` still returns kind, then owner, then others-write, then group-write, then the ACL arm. `check_external_ancestor` still passes `AclWrite::Known(Vec::new())` and judges the capture afterwards. The source pin counts one `Known(` in the choke point, one in that placeholder, and no `possible_acl_writers` in the production text of `custody.rs`. The security tests refuse `Omitted` in every scope and with `waive_owner` when kind, owner, and mode already pass, and they keep `NotDirectory`, `ForeignOwner`, `OthersWrite`, and `GroupWrite` ahead of `AclUnreadable`. The platform test pins a fresh file and `chmod -N` as `Omitted`, one write allow as `Present` with that writer, a read-only allow as `Present(vec![])`, and `chmod -a# 0` as capture `Entries(0)` with observer `Omitted`. No `acl-unreadable` arm was added. `installation_routing` still does not match this `Refusal`.

`acl_scratch` and `above_acl_scratch` live in `test_scratch`, which is `#[cfg(test)]`. The chain skip is also `#[cfg(test)]`, so a production build and every other crate's tests link security without it. A thread opts in only by calling `acl_scratch`. The skip matches device and inode of the canonical parents of that base, recorded in a thread-local list. The base and everything below it are judged. The skip drops the whole component, so those real ancestors contribute neither an ACL refusal nor an owner or mode refusal. The scratch base carries an inheritable `readattr` allow, which names no writer. `root_only_observation_refuses_the_omitted_acl_of_root` judges `/` before any opt-in. The policy-capture tests assert that same `/` refusal before they call `acl_scratch`, then observe absence and retention under the base. `a_private_leaf_cannot_hide_a_writable_ancestor` still requires `OthersWrite` on a component above the leaf. Storage's `observe_marker` tests refuse at component 0 with `AclUnreadable` and do not opt in; the unchecked marker tests keep the read and the descriptor. Marker files and `empty_bucket` receive `append_owner_zero_allow`, a present ACL with no mutation right. The libtest runner starts a new thread per test, so the opt-in ends with that thread.

The v80 descriptions of all nineteen files stay true. None of them names the old writer list. No inventory successor is owed for this unit.

## Required findings

### RF-1 — Present's comment includes a removed last entry

`DescriptorAcl::Present` is documented as a readable ACL whose writers may be empty, including "one whose last entry was removed." On this platform `chmod -a# 0` makes the bounded capture `Entries(0)` and makes `filesec` report the ACL absent. `descriptor_acl` returns `Omitted` for that report, and `omission_and_a_present_acl_without_writers_are_distinct_states` asserts `Omitted`. Law 461 r3 item 6 fails that observation closed. `Present(vec![])` is the no-mutation allow, which the same test already pins.

Failure scenario: a reader of `DescriptorAcl` treats a removed last entry as `Present` of an empty writer list. `check_descriptor_observation` would then build `AclWrite::Known` of no writers and admit the object, which is the omission reading this unit closes.

## Not reopened

The mapping, the refusal order, the ancestor placeholder, the absence of a 468c arm, the test horizon, and the unchanged v80 descriptions stand. The finding is the `Present` comment.
