# Review: InitialPlatform 462 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of `docs/implementation/m2/initial-platform-462/PROPOSAL.md`. No repository edits. No product cargo.

The proposal is 5914 bytes, sha256 `874deb43f988f9e44ea171fbb262fda6b51eb396b00c3bad70062bd777556e82`, matching `hashes.txt`. It settles owner.md §1a step 4 under §3, laws 458, 458b, 469, and 463. The creator stays disabled.

## Verdict

**ACCEPT.**

## Answers

Item 1 is the missing locator. `CoreProfileBindingV2` pins `platformProfileSetBodyDigest` and no path. 463 opens the inventory pair, the payload pair, the root chain, and the revocation, and no other name. The profile is two fixed files under the core tree root, `platform/profile-set.json` and, only when item 2 requires the envelope, `platform/profile-set.sig.json`. Both are file rows of the platform's inventory row. `InitialPlatform` opens them no-follow from `InitialCore`'s retained tree root, under the core-tree custody predicate, and requires each file's sha256 and length to equal its tree row. The body digest under `opensip.metadata.platform-profile-set.1` must equal the inventory pin. Those opens are not bootstrap members, so 463 item 9 is unchanged.

Item 2 is the right split, and the final root chooses it. `verify_profile_set_with` returns `NoProfileRole` unless the root schema is 2 and `TR-PROFILE` has a non-empty key list (`admitted_profiles.rs`). §S9.1 says a schema-1 root has no TR-PROFILE, so only the copy pinned by the signed core release is used, and a schema-2 root with an active TR-PROFILE admits a standalone envelope only as transport for that same pin. Owner step 4 says the same: schema-1 delivery is the pinned bytes, and a schema-2 TR-PROFILE envelope additionally obeys the role, quorum, and core-pin rules. An active role requires the envelope and the opt-in V1-or-V2 reader, with the inventory pin as the core pin and the revoked set from 463 item 5. A schema-1 root, or a schema-2 root whose TR-PROFILE is typed-absent, authenticates the body by that pin alone: V1 or V2 shape, and the domain digest equal to the pin. The envelope file is not opened. Whether the file exists does not choose the path. A root whose role is active and whose quorum then fails does not fall back to the pin-only path.

Item 3 matches the budget owner. `observe_macos_boot`, `observe_macos_process`, and `capture_system_loader` take no ledger. 462 charges process, boot, the 348a loader, the loader's filesystem, and H's `fstatfs` before each call. `machine` already refuses a translated process and returns `macos-aarch64` or `macos-x86_64` only when the process family and the loader CPU agree. That id must equal `InitialCore`'s compiled platform. The decision uses the full observed identity, must admit at either tier, and must have no refusals. Its `fsType` is H's sample, which is the volume where I will be created. The running image's volume is not that base.

Item 4 is the §3 home-base premise. H already exists, is opened no-follow, and must be local, not a union mount, writable, and a type in that platform's `installRootFilesystems`. Its filesystem identity is retained so 465 and 467 can require each fixed ancestor and the stage to share it. 469's predicates are the same at both tiers. No profile member is added.

Item 5 is consistent with step 4's "including" clause. The profile's install filesystem selects the primitive: for apfs, exclusive same-parent `renameatx_np(RENAME_EXCL)` and `F_FULLFSYNC`, with the §5.6 fallback only for its named unsupported errors. A probe would be an effect before the storage choice, and a successful call would qualify nothing. The typed receipts are taken when the operations happen: barriers in 465 and the rename in 467. An unsupported result there makes the creator unavailable. The `Fsync` fallback still satisfies an apfs chain, and its receipt kind stays.

Item 6 mints `AclOmissionPremise` only when the set is V2 and `install_acl_omission()` holds. That accessor already requires exact-measured, a lane, no refusals, and the matched last-duplicate row. The premise is private, not `Clone`, bound to the attempt, and holds the owned `installRootFilesystems` names plus an in-memory citation of the profile digest, platform, lane, build, kernUuid, and dyldCdhash. It samples each descriptor 460 judges with its own `fstatfs`: local, not a union, type in the owned list. The scope is 458 §5: root to H, `Library`, and `Application Support`. Moving the premise out of custody code removes the production constructor from the module that only judges.

Item 7 keeps Evidence B off a `SYNTHETIC` standing outside tests. A real embedded root's release is not a synthetic profile; the check is the defensive refusal if one is pinned anyway.

Item 8 is the accepted consequence of 458, 458b, and 469. A baseline host has no matched measured row, so there is no premise, and 460 refuses the omitted ACL at `/`. Creation waits until a release signs a measured row for that build, kernel UUID, and dyld hash with `installAclOmission`. This macOS 27 development host is in that set. There is no exception.

Item 9 matches the `InitialCore` receipt. `InitialPlatform` is private, not `Clone`, bound to the attempt, and holds the samples, the profile evidence, H, and the optional premise. Recheck re-samples process, boot, the loader and its filesystem, H's filesystem and exact names, and each profile file's identity, name, and custody. A difference refuses and latches.

Do not commit.
