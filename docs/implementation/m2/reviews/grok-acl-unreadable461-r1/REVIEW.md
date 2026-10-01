# Review: ACL omission unreadable 461 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of omitted ACL becoming unreadable at the descriptor-observation choke point. No repository edits and no product cargo.

Subject `docs/implementation/m2/acl-omission-unreadable-461/PROPOSAL.md`, 11325 bytes, sha256 `8f0c2d0afa9d661221277a5fb2effb21125310700c6b6836ce2929cc461d47e7`. Product HEAD is `d4239a540e37cbc2f1415e0e5edd040fb7a3fbfc`. The real OpenSIP directory is absent.

## Verdict

**REQUIRED-FINDINGS.**

The typed `DescriptorAcl` split, the consumer table, the project-root decision, and the budget match the product at `d4239a5`. Item 2 states a check order the pure predicate does not have. Item 3 names two different subjects. Item 6's source pin covers the ancestor placeholder that keeps that order.

## What holds

`macos::descriptor_acl` is the production reader behind `observe_descriptor`. `present == 0` returns the empty writer vector. A null ACL pointer and the NOACL sentinel (`acl as usize == 1`) stay `DescriptorObservationError::Acl`. A present ACL that ends at `EINVAL` returns the writers collected so far, and that vector is empty when no allow-write entry was kept. Linux stays `UnsupportedPlatform`. Replacing the vector with `DescriptorAcl::{Omitted, Present(Vec<AclWriter>)}` makes omission unrepresentable as an empty writer list. Equality sites (`macos_loader`, and the trust rechecks that compare the field) compare the observation and do not treat empty as no writers. Under the typed state those comparisons become `acl == acl`, so an `Omitted` / `Present` flip is a change.

Once `check` reaches the ACL arm, `AclWrite::Unreadable` is `Refusal::AclUnreadable` in every `Scope`, and `waive_owner` does not change that arm. The arm sits after kind, owner, others-write, and group-write. `uid == 0` is admitted as owner. The 18851-case fixture asserts `Refusal::code` of the first failing check, and `unknown_acl_is_not_empty_and_owner_waiver_preserves_other_guards` reaches `AclUnreadable` on mode `0o600` with `waive_owner`, then `HardLinked`, then `OthersWrite` when the mode bit is set. Item 6's security pin can require `Omitted` to refuse in every scope and with `waive_owner` on an observation that already passes kind, owner, and mode.

`check_descriptor_observation` is the production mapping of `possible_acl_writers` into `AclWrite::Known`. The item 4 table matches the callers at `d4239a5`. Trust files under I go through `inspect_operational_file`. Directory edges under I go through `directory_policy::inspect` and `check_operational_chain_observations`. `FileLock::observe_descriptor` in the gate and stage `fence_matches` reads metadata. `path_binding::observe_directories` and `directory_binding::observe_directory` carry the observation. `inspect_directory_path`, `NativeInstallationRoot`, and `SuppliedInstallationFence` have no production caller. `observe_bound_operational_file_with_policy` is called from `store_root::observe_marker`, and that function is reached from `store_root` tests. `judge_captured_ancestor` judges a bounded capture through `check_external_ancestor`. An omitted capture (`CapturedAclState::NotReturned`) is the premise path or `ParentRefusal::AncestorAclOmitted`. That path stays outside the writer-list change. 468c publishes it as subject `ancestor-acl-omitted`.

Items 5 and 9 match law 458 §5 and 458c item 3. The premise stays on root-to-H, `Library`, and `Application Support`. Project roots and operational paths stay outside it. No production path judges a project root. CREATOR-PLAN already records a separate project-root custody law as a prerequisite of project admission.

`descriptor_observation_cost` is two status reads plus `descriptor_acl_cost`. That cost is a static estimate at `MAX_ACL_ENTRIES` (128). The same `fstatx_np`, `filesec_query_property`, and ACL walk run. A choke-point refusal is custody. `descriptor_acl_cost` does not scale with the returned writer count.

461a is the code and the inventory successor. 461b is the contract successor for the stale descriptions. Retiring the test-only walkers waits on the project-root law.

## Required findings

### RF-1 — The ACL arm runs after owner, mode, and group

`check` returns kind first (`Symlink`, `NotDirectory`, `NotRegular`), then `ForeignOwner` unless `waive_owner` and the scope is not `OperationalFile`, then `OthersWrite`, then `GroupWrite`, then the ACL arm. `check_external_ancestor` documents that order: it feeds `AclWrite::Known(Vec::new())` so mode and owner still run, and the comment says the ACL judgment stays after mode. Item 2 says the pure `check` already returns `Refusal::AclUnreadable` for `AclWrite::Unreadable` before owner, mode, or group checks, and that no predicate changes. The ACL arm itself ignores scope and `waive_owner`. The earlier arms do not.

Item 4's omitted edge refuses `AclUnreadable` when kind, owner, others-write, and group-write already pass. An omitted directory that fails one of those earlier arms keeps that earlier refusal.

Failure scenario: an omitted-ACL directory is mode `0777`, or owned by another account, or the wrong kind. `check` returns `OthersWrite`, `ForeignOwner`, or `NotDirectory` before the ACL arm. An implementer who moves the ACL arm ahead of owner, mode, and group, to match item 2, publishes `acl-unreadable` for that directory and changes the code the 18851-case fixture asserts.

### RF-2 — The named subject and the lowercased code differ

Item 3 names the choke-point subject `acl-unreadable` and also says the subject is `Refusal::code` in lower case, following 468c. `Refusal::code` for `AclUnreadable` is `ACL_UNREADABLE`. Lower case of that string is `acl_unreadable`. 468c custody subjects are an explicit match with hyphens: `acl-not-returned`, `ancestor-acl-omitted`, `foreign-owner`. Nothing in the security crate lowercases `Refusal::code` or turns its underscores into hyphens. `lib.rs` exports `Refusal` as a workspace diagnostic, not a public report code, and `installation_routing` does not match `custody::Refusal`. The custody class already exists: request-rejected, exit 2, `CONFIG.INVALID`, `CONFIG.CUSTODY_REFUSED`. The new text is the subject string. A consumer that already reaches 468c through its own family keeps that family's row.

Failure scenario: one reading of item 3 publishes subject `acl_unreadable`. The other publishes subject `acl-unreadable`. Both sit on `CONFIG.CUSTODY_REFUSED`. They are different subjects. The law has to name one of them.

### RF-3 — The Known pin covers the ancestor placeholder

Item 6 requires a source check in the security crate that forbids constructing `AclWrite::Known` from anything but `DescriptorAcl::Present`. `check_external_ancestor` constructs `AclWrite::Known(Vec::new())` with no `DescriptorAcl`, so the mode and owner arms still run and `external_ancestor_acl` judges the capture afterward. The pure-predicate tests construct `AclWrite::Known` from the fixture, including the 18851-case corpus. `AclWrite` is private to `custody.rs`.

Failure scenario: the pin is applied to every `Known` in the crate. Satisfying it by changing the ancestor placeholder to `AclWrite::Unreadable` makes `check` return `AclUnreadable` for every ancestor that passes kind, owner, and mode, and `external_ancestor_acl` never runs. A present ancestor ACL that today returns `Ok` becomes `Refusal::AclUnreadable`. A present foreign write allow that `installation_parent_tests` asserts as `ParentRefusal::Ancestor { refusal: AclWrite }` becomes `AclUnreadable`. The observation adapter is the construction the pin can forbid: `check_descriptor_observation` builds `Known` only from `DescriptorAcl::Present`.

## Not reopened

The `DescriptorAcl` split, the NOACL and malformed-ACL errors, the consumer census, the capture-based ancestor judgment, the project-root prerequisite, the static observation cost, and the 461a / 461b split stand. The findings are the check order, the subject spelling, and the scope of the `Known` pin.
