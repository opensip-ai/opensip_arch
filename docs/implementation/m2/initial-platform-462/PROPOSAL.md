# InitialPlatform for the initial creator — proposal 462 r1

2026-09-26. Claude Opus 5.5, implementation lead. Law for unit 462, under owner.md §1a step 4 and §3, laws 458 and 458b (Evidence B), 469 (macOS 27) and 463 (InitialCore). It closes the points the owner leaves to the implementation. Not code, not creator authority. The creator stays disabled. ACCEPTED by Grok 462 r1 on 2026-09-26.

## Decisions

1. **Where the profile lives.** A release tree carries the platform profile set as two fixed files under the core tree root: `platform/profile-set.json`, and when item 2 requires it, `platform/profile-set.sig.json`. Both are `file` rows of the platform's inventory row. `InitialPlatform` opens them by no-follow from `InitialCore`'s retained tree root, under the core-tree custody predicate (463 item 7). It requires each file's sha256 and length to equal its tree row, and the profile body's domain digest (`opensip.metadata.platform-profile-set.1`) to equal the signed inventory's `platformProfileBinding.platformProfileSetBodyDigest`. These opens belong to `InitialPlatform`. `InitialCore`'s own opens (463 items 1 and 2) are unchanged, and the files are not bootstrap payload members, so 463 item 9 is unaffected.
2. **Authentication under the release context only.** The root is `InitialCore`'s final authenticated root, and the revoked set is the set after 463 item 5. No caller set exists anywhere.
   - **The final root has an active TR-PROFILE role:** the envelope file is required, and the profile is verified by the opt-in V1-or-V2 reader (458b) with the inventory pin as core pin.
   - **Otherwise** (a schema-1 root, or a schema-2 root whose TR-PROFILE is typed-absent): the profile is authenticated by the TR-CORE-signed inventory pin alone, as contract §S9.1 and the owner step 4 schema-1 sentence say. The body must pass V1 or V2 shape, and its domain digest must equal the pin. The envelope file is not opened.

   The final root decides which path applies. Whether an envelope file exists never does.
3. **Observations.** Every native observation is charged to the attempt's one ledger before it runs: process, boot, the system loader (348a), the loader's filesystem, and H's own `fstatfs`. The machine id from process and loader must equal `InitialCore`'s compiled platform (463 item 3). A translated process refuses. The platform decision uses the full observed identity, and its `fsType` is H's. The decision must admit (at either tier) with no refusals.
4. **Home-base premise.** H, the account home that `InitialActor` names, opened as a retained no-follow path, must be local, not a union mount, writable and a type in the profile's `installRootFilesystems`. Its filesystem identity is retained. Later owners require each fixed ancestor and the stage to share H's filesystem identity (465, 467). This is an assumption of the selected population (469 item 3: predicates identical at both tiers). It adds no profile member.
5. **Rename and barriers.** 462 records the primitive policy the profile's install filesystem selects. For apfs that is exclusive same-parent `renameatx_np(RENAME_EXCL)` and `F_FULLFSYNC`, with the §5.6 fallback only for its named unsupported errors. 462 does not probe: a probe would be an effect before the storage choice, and a successful syscall qualifies nothing. The typed receipts are taken at effect time, barriers in 465 and the rename in 467. An unsupported result there means the creator is unavailable. The §5.6 `Fsync` fallback satisfies an apfs chain, with its receipt kind kept.
6. **Evidence B minting.** `InitialPlatform` mints an `AclOmissionPremise` only when the profile set is V2 and the decision's `install_acl_omission()` holds. That accessor already requires exact-measured, a lane, no refusals, and the matched last-duplicate row carrying the member (458b decision 5). The premise is private, not Clone, bound to the attempt, and carries:
   - owned filesystem type names from that platform's `installRootFilesystems`;
   - an in-memory `RowCitation`: profile digest, platform, lane, build, kernUuid and dyldCdhash.

   It runs its own `fstatfs` on each retained descriptor that 460 judges: local, not union, type in the owned list. Its scope is exactly 458 §5's: root to H, `Library` and `Application Support`. The premise moves out of custody code, so custody code cannot construct one.
7. **SYNTHETIC profiles.** A profile set whose `standing` is `SYNTHETIC` never mints Evidence B outside `#[cfg(test)]`. This is defensive: such a profile cannot authenticate under a real embedded root.
8. **BASELINE-ATTESTED hosts.** Such a host has no matched measured row, so there is no premise, and 460 refuses the omitted ACL at `/`. Creation is therefore impossible on such a host until a release signs a measured row for its build, kernel UUID and dyld hash with `installAclOmission`. That includes this macOS 27 development host under 469. This is an accepted consequence of 458, 458b and 469. There is no exception.
9. **Receipt and recheck.** `InitialPlatform` is private, not Clone, bound to the attempt, and holds the samples, the profile evidence, H and the optional premise. Its recheck re-samples process, boot, the loader and its filesystem, H's filesystem and exact names, and each profile file's identity, name and custody. Any difference refuses and latches.

## Forbidden substitutes

An unsigned profile fixture outside tests; a caller revoked set; an existing installation fence; a profile file chosen by listing or by name "latest"; an envelope's presence deciding which authentication path applies; a probe rename or barrier before the storage choice; Evidence B from a BASELINE-ATTESTED decision, a V1 body, an unmatched duplicate row, or a SYNTHETIC profile outside tests; a caller-built filesystem sample.

## Not claimed

No boot identity is qualified. No measured row is checked in for any host. No creator is enabled. 461 and 458c are unchanged.
