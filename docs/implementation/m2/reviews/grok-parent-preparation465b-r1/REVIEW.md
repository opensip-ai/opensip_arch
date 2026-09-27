# Review: parent preparation 465b and inventory 71

Grok is the single reviewer. Claude Opus 5.5 leads. Review of the parent preparation, the creation permit, and inventory v71. No repository edits.

Product HEAD `000c5ce472ab38ef67ff3f20f5d708fddf7386b6`. The fifteen files match `hashes.txt`. The 465a platform pins are the bytes accepted in that review. The subject manifest matches `subjects.txt` (1741 bytes, sha256 `8dac6e051428f7ceeeb9c33362027b6be98fe1cf394a1047655a136c44355add`), and every file it lists matches. Law is 465 items 1–11. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

`~/Library/Application Support/OpenSIP` did not exist before the replay and does not exist after it. The only live-home test refuses at `/` with the probe's barrier and create counts at zero. Every other preparation uses a scratch home.

## Verdict

**ACCEPT-UNIT.**

## Producer

No effect runs before the rechecks. A0 requires the attempt to be unlatched and every lineage to match, including the premise when one exists. A1 rechecks the actor, `InitialCore` and `InitialPlatform`. A2 is the 460 walk. A3 requires the walk's H to be the platform's H, on a filesystem `qualifies_installation_filesystem` accepts. A4 rechecks the intent target and storage, then the chain's exact names. Only then does E1 take H's barrier.

The seven slots are H at 0, then for ancestor `i` its own barrier at `1 + 2i` and its parent's at `2 + 2i`. Slot 2 is H again, as `Library`'s parent. Each of `Library`, `Application Support` and `OpenSIP` is one `work.effect` whose postchecks are reserved before `mkdirat`. A raw `EEXIST` opens no-follow and is admitted as a reused directory. `NotFresh` and any other error after `mkdirat` fail the effect. A reused ancestor and a new one take the same admission: exact name, custody, H's filesystem, its own barrier, and its parent's barrier.

Item 4 applies only to `Library` and `Application Support`, new or reused, through `admits_reserved` on that descriptor. With no premise, an omitted ACL refuses. Item 5 applies only to `OpenSIP`. A present ACL is judged as private. An omitted ACL is finished with the zero-rights owner allow only when this act just created the directory, or when the existing directory is owned by the invoking user, mode exactly 0700, and holds no entry except `.`, `..`, and `.opensip-stage-install-` plus 32 lowercase hex, at most 64 such names. Any other state is `Unfinishable` or `Private`.

The preparation stores the intent's `binding()` and a copy of the disclosed target. `mint_creation_permit` requires that same binding and target, a positive no-follow absence of `preview-v1` (a dangling symlink is `NotPristine`), the name, core, platform, actor, target and storage rechecks, and `consume`. The permit is not `Clone`. `hand_off` consumes it. Its recheck does not look at `preview-v1` again. Storage strength is `NotBackedUp` < `Unknown` < `BackedUp`; a stronger class without the flag is `StorageChanged`.

The disclosed deviations match the code. `OpenSipJudgment::Retain` keeps `OpenSIP` by name so item 5 can be judged before any effect; the 460 entry point still uses `Private`. `preview-v1` is observed in A2. A reused ancestor shares the reserved admission inside a zero-cost effect. Evidence B is still the premise's own `fstatfs`. The name recheck is the exact descriptor name plus a no-follow reopen of the same device and inode. The staging scan stops at 64 entries. FullFlush and the named `Fsync` fallback are both recorded. `prepare_fresh_private_sample_reserved` is `pub(crate)`. The `private_interfaces` allows are on the two modules whose types the new modules name.

## Inventory v71

v71 is v70 plus `directory_effects.rs`, `installation_parent.rs` and `installation_parent_tests.rs`, in sorted order: 723 rows become 726, and nothing is removed. Every inherited row matches aside from the five carried description overrides. Packages, dependencies and pending decisions match. The helper is byte-identical to the earlier one (2917 bytes, sha256 `bb82ef057ab4bb897f72b9a1f463ac67e3a5c60947649507d4c4d4532f9dd110`). Its recorded run is 5 projection rows and 28 corruptions refused. The stale descriptions of `initial_installation.rs` and `private_access.rs` stay as they were in v70. A new override is a contract-successor concern, and this unit records that follow-up rather than inventing one.

## Replay

- `cargo test --locked --offline -p opensip-security --lib`: exit 0. 505 passed, 0 failed, 2 ignored. All 13 `installation_parent` tests passed.
- `cargo test --locked --offline -p opensip-platform --lib`: exit 101. 188 passed, 1 failed, 1 ignored. The failure is `native_filesystem_original_file_lock_and_all_path_components_stay_owned`: `ChangedDuringRead`.
- `cargo test --locked --offline --workspace --all-targets`: exit 0. 1022 passed, 0 failed. The platform lib in this run is 189 passed, 0 failed, 1 ignored.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
