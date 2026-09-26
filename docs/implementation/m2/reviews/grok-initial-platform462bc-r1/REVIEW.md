# Review: InitialPlatform 462b/462c and inventory 70

Grok is the single reviewer. Claude Opus 5.5 leads. Review of the InitialPlatform producer, its tests, and inventory v70. No repository edits.

Product HEAD `430e469dd417cbcddac8e81e0d5fd9acfa974e82`. The ten files match `hashes.txt`. The subject manifest matches `subjects.txt` (1671 bytes, sha256 `a921be34344d5d61a721e555b0c9e50bafebf49e05344ec4ffc19a36e3621fa3`), and every file it lists matches. Law is 462 items 1–9. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Law questions

Evidence B from a V2 set authenticated by the pin alone is what item 6 says. The mint condition is V2, `install_acl_omission()`, and a standing that is not `SYNTHETIC` outside tests. It does not require the TR-PROFILE envelope. Under a schema-1 root the body is authenticated by the TR-CORE-signed inventory pin, which is the §S9.1 path. A V2 body on that path can still carry the measured-row member.

The `platform/` directory is judged. `open_release_file` duplicates the tree root, judges it, then opens each path component and the file no-follow by exact name under `CoreMember::Platform` and the core-tree predicate. The profile path is `platform/profile-set.json`. The envelope path is `platform/profile-set.sig.json`, opened only when the role is active.

Writable H is the mount's not-read-only flag. P8 requires `is_local`, not a union, `!is_read_only()`, and a type in `installRootFilesystems`. There is no write probe.

Active TR-PROFILE is schema 2 and role standing `"active"`. A validated root admits that standing only with the active key, threshold, and namespace rules. Typed absence is `"typed-absence-DR-110"`, which takes the pin-only path. The envelope file's presence does not choose the path.

## Producer

`produce_initial_platform` checks both lineages, then one `attempt.run`. P1–P3 are the accounted process, boot, and loader observations. A translated process refuses. `machine` must equal `core.platform()`. P5 requires the loader filesystem to be local, not a union, read-only, and `apfs`. P6 opens the profile and joins its sha256 and length to the platform-row tree entry. P7 is the final root: an active role verifies the envelope with `verify_profile_set_with(V1OrV2, …, pin, core.revoked())`; otherwise `verify_initial_core_pinned` checks V1 or V2 shape and the domain digest against the pin, and does not open the envelope. The decision runs only after that. It must have no refusals, a tier, and `core.platform()`. The receipt is returned only after P8–P12, including the closing recheck and `recheck_actor`.

P10 mints `AclOmissionPremise` only in `initial_platform.rs`. It is private, not `Clone`, bound to the attempt, and holds owned filesystem names plus a private `RowCitation` (profile digest, platform, lane, build, kernel UUID, dyld cdhash). `admits` takes its own charged `fstatfs`: local, not a union, type in the owned list. Custody only imports the type and calls `admits`. The test constructor is `cfg(test)`.

P11 records `PrimitivePolicy::Apfs` when H is apfs: exclusive same-parent `renameatx_np(RENAME_EXCL)` and `F_FULLFSYNC`, with the §5.6 fallback named and not called. No other filesystem gets a policy. Recheck re-observes process and boot, rechecks the loader and its filesystem, rechecks H's names and filesystem, and rechecks each opened profile file's identity, name, and custody. A difference is `Changed` and latches. A foreign attempt is `WrongAttempt` and latches. `InitialPlatform` is private and not `Clone`.

The twelve security tests cover the baseline host with no premise and `AncestorAclOmitted { component: 0 }`, the exact-measured host whose premise admits `/` and refuses `/dev`, the signed path staying baseline on this host, V1 carrying no premise, a schema-1 root not opening a present envelope, and the helper's production refusal of `SYNTHETIC`. Not covered, and named as such: a scratch ancestor chain, a schema-2 typed-absent root, a non-apfs or union H, and Linux.

## Inventory v70

v70 is v69 plus `initial_platform.rs` and `initial_platform_tests.rs`, in sorted order: 721 rows become 723, and nothing is removed. Every inherited row matches aside from the five carried description overrides. Packages, dependencies, and pending decisions match. Both new files are on disk. `verify_projection.py` is byte-identical to the earlier helper (2917 bytes, sha256 `bb82ef057ab4bb897f72b9a1f463ac67e3a5c60947649507d4c4d4532f9dd110`). Its recorded run is 5 projection rows and 28 corruptions refused.

## Replay

- `cargo test --locked --offline -p opensip-security --lib`, twice: exit 0 both times. 491 passed, 0 failed, 2 ignored. No flake.
- `cargo test --locked --offline --workspace --all-targets`: exit 0. 996 passed, 0 failed.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
