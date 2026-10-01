# Omitted ACL is unreadable at the single custody choke point — proposal 461 r1

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit 461, under owner.md §1b and §5 to §7 and laws 458 (§5), 458b, 462, 465 item 4, 468 r5 item 2 and 458c r6 items 3, 8 and 9. Item 9 is a lead decision made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation. Not code. Library only: CLI enablement is a separate unit (464 item 7).

## Problem

`opensip_platform::observe_descriptor` returns a `DescriptorObservation` whose `possible_acl_writers` is a `Vec<AclWriter>`. The macOS reader `macos::descriptor_acl` returns `vec![]` when `filesec_query_property(FILESEC_ACL)` reports the ACL absent (`present == 0`). The field's own comment says it is "Empty only after a successful read", but an omitted ACL and a present ACL that grants no write both arrive as the same empty vector. `check_descriptor_observation` in `crates/security/src/custody.rs` turns that vector into `AclWrite::Known(..)`, so omission is judged as "no ACL writers".

Law 458 §5 says omission is not evidence of absence (source findings 445, route 446). The bounded capture (`CapturedAclState`) already keeps omitted, NOACL and present apart, and `check_external_ancestor` and the private judgment already refuse omission. Only the legacy writer list still reads it as "no writers". 461 retires that reading.

458c made this safe to do now. Every installation read is on the charged session over retained handles (458c-b2), and a source pin keeps production readers off `NativeInstallationFence`, `NativeInstallationRoot`, `SuppliedInstallationFence` and `inspect_directory_path`. The root-to-H prefix, `Library` and `Application Support` are judged only by the capture-based predicates with the receipt-bound premise (458c item 3, 468 r5 item 2). No production read of the installation reaches the legacy writer list for a component that omits its ACL.

## Decisions

1. **The platform observation carries the ACL state, not a bare writer list.** `DescriptorObservation::possible_acl_writers: Vec<AclWriter>` is replaced by `acl: DescriptorAcl`:
   ```
   pub enum DescriptorAcl {
       Omitted,                 // FILESEC_ACL reported absent
       Present(Vec<AclWriter>), // a readable ACL; its possible writers, possibly none
   }
   ```
   - `macos::descriptor_acl` returns `DescriptorAcl::Omitted` where it returns `vec![]` today on `present == 0`. A present ACL returns `Present(writers)`, where an empty vector means a readable ACL with no write allow.
   - The NOACL sentinel and a malformed ACL stay errors (`DescriptorObservationError::Acl`), as today.
   - Keeping the field name `possible_acl_writers` with an added flag, or leaving omission as an empty vector, is forbidden. The type must make omission unrepresentable as "no writers".
2. **The choke point.** `check_descriptor_observation` maps:
   - `DescriptorAcl::Omitted` to `AclWrite::Unreadable`;
   - `DescriptorAcl::Present(writers)` to `AclWrite::Known(writers)`.

   The pure `check` already returns `Refusal::AclUnreadable` for `AclWrite::Unreadable` in every scope, before owner, mode or group checks, and whatever `waive_owner` is. No predicate changes. This is the only place in production that turns a platform observation into a custody judgment, and every consumer in item 4 goes through it: `check_retained_descriptor`, `inspect_operational_file`, `check_operational_chain_observations`, `directory_policy::inspect` and `inspect_directory_path`.
3. **The public row.** `Refusal::AclUnreadable` from the choke point is the 468 item 6 custody row: request-rejected, exit 2, `CONFIG.INVALID`, `CONFIG.CUSTODY_REFUSED`, subject `acl-unreadable`. The subject is `Refusal::code` in lower case, following 468c's sub-detail spellings. There is no new public code, and no change to 468c's existing subjects (`ancestor-acl-omitted`, `acl-not-returned`, and the others). Where a consumer's refusal already reaches 468c through its own family, it keeps that family's row; this item fixes only the subject of the choke-point refusal.
4. **The consumers.** All production consumers of the platform observation, at product d4239a5:

   | Consumer | What it judges | ACL on a stock Mac | Outcome under 461 |
   |---|---|---|---|
   | Trust captures under the read session: `inspect_operational_file` in `native_current`, `native_record_capture` and `directory_record_capture` | Trust files under I | Present: the zero-rights owner allow of a private creation | Unchanged; judged `Present` |
   | `directory_policy::inspect` (via `check_operational_chain_observations`) in `native_current`, `native_record_capture`, `directory_record_capture`, `directory_name_scan`, `native_census` and `directory_provers` | Retained parent/child edges under I (trust directories) | Present | Unchanged. An edge whose directory omits its ACL now refuses `AclUnreadable` instead of passing, which is correct: a directory under I with no ACL is foreign or tampered |
   | `FileLock::observe_descriptor` in the gate's and the stage's `fence_matches` (`installation_admission.rs`, `installation_stage.rs`) | The locked fence: identity, link count and type only | Not judged | Unchanged: these read `metadata` only |
   | `macos_loader` observations (before/after samples of loader files) | Equality of two samples of the same descriptor | Not judged | Unchanged: the comparison becomes `acl == acl`, so an `Omitted`/`Present` flip between samples is a change, which is stricter and correct |
   | `path_binding::observe_directories` and `directory_binding::observe_directory` | Only what their callers judge | — | Carry the typed state; the judgment is item 2 |
   | `inspect_directory_path` (a full-path walk from `/`) | Every component from `/` | `/` and `/Users` omit | Now refuses at `/` on a stock Mac. It has no production caller: the 458c-b2 pin, plus the one below |
   | `observe_bound_operational_file_with_policy` (public in `opensip_security`), used by `store_root::observe_marker` | A parent path from `/`, then an operational file | `/` omits | Now refuses at `/`. No production caller exists: `observe_marker` is reached only from `store_root` tests, and nothing else in the workspace calls the function |
   | `NativeInstallationRoot`, `SuppliedInstallationFence` (supplied-root tests) | Scratch chains | Test-controlled | Test-only (458c-b2); tests that relied on omission-as-no-writers are updated in 461a |

   So no production path changes outcome except toward refusal of a component that is foreign, tampered or outside the premise. The creator, the write gate and the read session already judge the root-to-H prefix, `Library` and `Application Support` through captures with the premise, and `OpenSIP`, I and private descendants through the private predicate.
5. **Project roots and operational files are not given the premise.** Law 458 §5 and 458c item 3 exclude them. Under 461, a project root, or any operational path judged through the choke point, whose directory omits its ACL refuses with `AclUnreadable`, and so does every ancestor walk that starts at `/` (`inspect_directory_path`). On this host, `/Users/sb/code` and the project directories below it omit the ACL, as ordinary user-created directories do. Today no production path judges a project root, so nothing breaks now. A future project-admission path would refuse every ordinary project. Item 9 decides how that is handled. 461 does not widen the premise.
6. **The legacy writer list is removed.** After item 1 no code can obtain omission as an empty writer list.
   - A platform test pins that `observe_descriptor` on a fresh file after `chmod -N` returns `Omitted`, a file with one added entry returns `Present` with that writer, and a file with its last entry removed returns `Present(vec![])` (458 item 6's fixture set, on the descriptor observer).
   - A security test pins that `check_descriptor_observation` refuses `Omitted` in every `Scope` and with `waive_owner`.
   - A source check in the security crate forbids constructing `AclWrite::Known` from anything but `DescriptorAcl::Present`.
7. **Budget.** No work changes: the same `fstatx_np`, `filesec_query_property` and ACL walk run. `descriptor_observation_cost` is unchanged, and charged consumers keep their charges. A refusal is a custody refusal, never a budget or I/O failure.
8. **Units after the law.**
   - **461a:** `DescriptorAcl` in platform; the macOS reader; every field user (item 4) moved to the typed state; the choke-point mapping; the pins of item 6; the supplied-root and `observe_bound_operational_file_with_policy` tests updated to scratch chains that carry ACLs, or to assert the new refusal; inventory successor.
   - **461b:** a contract successor for the stale inventory descriptions recorded by 458c-b1, b2 and c (`installation_observation.rs`, `installation_session.rs`, `read_premise.rs`, `native_read_session.rs`, `installation_fence.rs`), plus any description 461a makes stale (`filesystem.rs`, `custody.rs`), as 468a did.
   - Retiring the test-only legacy walkers (`inspect_directory_path`, `NativeInstallationRoot`, `SuppliedInstallationFence`, `observe_bound_operational_file_with_policy`) is not required by this law. It may follow the owner's answer to the open question, since a project-root law decides whether a charged successor of the `/`-rooted operational walk is needed.

9. **Project roots (lead decision, 2026-09-30).** 461 lands as written. Project roots and operational paths stay outside the premise, and refuse on an omitted ACL through the choke point.
   - **A required prerequisite.** Before any project-admission path is enabled (M2 exit or CLI enablement), a separate project-root custody law must be accepted. It decides whether project roots on H's filesystem get a receipt-bound omission premise of their own, scoped to the project root and its operational directories under the same qualified profile member (458 item 3), or another admissible evidence path. CREATOR-PLAN records it as a prerequisite of project admission.
   - **The alternative, rejected.** Exempting the project scope from 461 now would keep omission-as-no-writers there, the reading 458 §5 rejects. It would also be the one place the old reading survived.
   - **Owner override.** The owner may override this decision.

## Forbidden substitutes

Reading omission as an empty writer list anywhere; a flag beside a writer vector instead of a type that separates omission; the premise on project roots, operational files, `OpenSIP`, I or private descendants; a new public code or subject family; changing the pure `check` predicates or the NOACL treatment; a production caller of `inspect_directory_path`, `NativeInstallationRoot`, `SuppliedInstallationFence` or `observe_bound_operational_file_with_policy` added without a law that decides project roots; treating an `Omitted`/`Present` difference between two samples as equal.

## Not claimed

CLI enablement; project-root admission or discovery; any widening of Evidence B; Linux (the descriptor observer stays `UnsupportedPlatform`); a qualified measured row for this macOS 27 host, which stays BASELINE-ATTESTED, so real installation reads here still refuse at `/` without a synthetic test profile; retiring the test-only walkers.
