# Review: ACL omission unreadable 461 r2

Grok is the single reviewer. Claude Opus 5.5 leads. Law re-review of omitted ACL becoming unreadable at the descriptor-observation choke point. No repository edits and no product cargo.

Subject `docs/implementation/m2/acl-omission-unreadable-461/PROPOSAL.md`, 12388 bytes, sha256 `fad51694be8825b5339f1f652895ac3ecc0521e55bd4b0506edd2e58cb597c8f`. `PROPOSAL-r1.md` preserves the r1 bytes, 11325 bytes, sha256 `8f0c2d0afa9d661221277a5fb2effb21125310700c6b6836ce2929cc461d47e7`. The diff is the header, the item 2 order sentence, the item 3 subject sentence, and the item 6 pin. Product HEAD is `d4239a540e37cbc2f1415e0e5edd040fb7a3fbfc`.

## Verdict

**ACCEPT.**

RF-1, RF-2, and RF-3 are closed. The typed split, the consumer table, the project-root decision, and the budget still match the product.

## What holds

The ACL arm stays after kind, owner, others-write, and group-write. `check` returns `Symlink`, `NotDirectory`, or `NotRegular` first, then `ForeignOwner` unless `waive_owner` applies and the scope is not `OperationalFile`, then `OthersWrite` (`mode & 0o002`), then `GroupWrite` (`mode & 0o020`), then `AclWrite::Unreadable` as `Refusal::AclUnreadable`. That arm ignores scope and `waive_owner`, so once it is reached the refusal is `AclUnreadable` in every scope. An omitted directory that is the wrong kind, foreign-owned, other-writable, or group-writable keeps that earlier refusal. `AclUnreadable` is the result when those arms pass. Item 2 leaves the predicate and the order unchanged, so the 18851-case fixture keeps `Refusal::code` of the first failing check. Item 4's omitted edge refuses `AclUnreadable` where the same edge would have passed. Item 6's security pin can require `Omitted` to refuse in every scope and with `waive_owner` on an observation that already passes kind, owner, and mode.

The choke-point subject is `acl-unreadable`. Item 3 says 461a adds that one arm to 468c's custody-subject mapping and does not derive it from `Refusal::code` (`ACL_UNREADABLE`). The row is the existing custody row: request-rejected, exit 2, `CONFIG.INVALID`, `CONFIG.CUSTODY_REFUSED`. `CONFIG.CUSTODY_REFUSED` is the registered detail. Diagnostic routes publish its subject as the sub-detail, and those sub-details stay out of the public-code registry. `ancestor-acl-omitted` and `acl-not-returned` stay as they are. A consumer that already reaches 468c through its own family keeps that family's row. `ParentRefusal::Ancestor` stays subject `ancestor`, including an inner `Refusal::AclUnreadable` from an uninterpretable capture. `AncestorAclOmitted` stays `ancestor-acl-omitted`.

The `AclWrite::Known` pin covers a platform observation mapped in `check_descriptor_observation`, and only `DescriptorAcl::Present` may become `Known` there. The allowed exception is `check_external_ancestor`'s `AclWrite::Known(Vec::new())` placeholder. It stays. It carries no ACL judgment and keeps the ACL arm after mode. `external_ancestor_acl` judges the capture: `CapturedAclState::Entries` is the writer check, and `NotReturned` or the NOACL sentinel is `Refusal::AclUnreadable`. `judge_captured_ancestor` admits `NotReturned` only when the premise's own `fstatfs` accepts it, then re-judges that descriptor as `Entries(0)`. That is 458 §5 for root-to-H, `Library`, and `Application Support`, and 465 item 4 for a new ancestor of those two names. Making the placeholder `Unreadable` would return `AclUnreadable` before `external_ancestor_acl` and refuse a present ancestor ACL. The pure-predicate fixtures construct `Known` from the corpus, not from a platform observation, so they sit outside the pin.

`macos::descriptor_acl` remains the production reader. `present == 0` is the omission case. A null ACL and the NOACL sentinel stay `DescriptorObservationError::Acl`. A present ACL that ends at `EINVAL` can return an empty writer vector. Linux stays `UnsupportedPlatform`. Equality sites compare the observation. `descriptor_observation_cost` stays two status reads plus the static `descriptor_acl_cost` at `MAX_ACL_ENTRIES`. The item 4 callers match `d4239a5`. Trust files under I keep a present ACL. `FileLock` fence matches read metadata. `inspect_directory_path`, `NativeInstallationRoot`, `SuppliedInstallationFence`, and `observe_bound_operational_file_with_policy` have no production caller. The capture path for root-to-H, `Library`, and `Application Support` stays off the writer list. Project roots stay outside the premise, and a separate project-root custody law remains the prerequisite of project admission. 461a is the code and inventory successor. 461b is the stale-description contract successor.

## Required findings

None.
