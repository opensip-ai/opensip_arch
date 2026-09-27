# Review: initial publication 467a/467b and inventory 74

Grok is the single reviewer. Claude Opus 5.5 leads. Review of the stage, validation, publication, routes and handoff, and inventory v74. No repository edits.

Product HEAD `f0a29bccadcbada59742284d1f582c44f796d24d`. All twelve files match `hashes.txt`. New files: `installation_stage.rs` (43230 bytes, sha256 `e4df7d59fd1f9f6313533ee380041762f5f676d0125a6dda24c5c517f2da39fc`), `installation_publication.rs` (14725 bytes, sha256 `83a619ec1adfe3377fc3aca90db1faaf392a79d54cc45123a1cd0f12ea81dc87`), `installation_publication_tests.rs` (33615 bytes, sha256 `1bb0bfa3aa3e9c403d991b8f8a61bdc1550cebe4b5850abc0435e2385004be89`). The subject manifest matches `subjects.txt` (1692 bytes, sha256 `df80dc2945e08b203c8e886ae3e11cca95948f4f3c1e35f24f1d7c7b488690fc`), and every file it lists matches. Law is 467 items 1–11 and the P0 tree, with owner §1a step 6 and §2–§6. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Composition

`create_initial_installation` is `pub(crate)` and has no other caller. It prepares the parent, mints the permit, then stages and publishes. `NotPristine` from preparation or the permit becomes `Outcome::Existing(NotPristine)` before any stage exists. A lost race becomes `Outcome::Existing(LostRace)`. The attempt is borrowed; the caller drops it.

S0 rechecks and consumes the permit, then `recheck_handoff_storage`. S1 draws S as 32 lowercase hex from the OS CSPRNG, takes one clock sample, and projects it with `project_creation_observation`. That projection is recorded evidence. K is the core's state writer, 1 or 2. S1 is charged as `INPUTS_COST` before the draw. S2 creates the private stage under the retained OpenSIP inside one effect that reserves `stage_postchecks` first: fresh private sample, filesystem sample, the stage's own barrier and its parent's on `stage.parent_directory()`, then the exact name. S3 builds P0 in memory through `initial_manifest::build`. S4 creates the 14 directories in manifest order, parents first, each in an effect that reserves `directory_postchecks` before `mkdirat`. A raw `EEXIST` inside the stage is `Foreign`. Each directory gets its own barrier and its parent's before the next child. S5 writes the 11 files in manifest order. The fence is index 0 and `selection.pair` is index 10. Each file effect reserves creation, the private sample, the bounded write with `F_FULLFSYNC` and no fallback, the containing-directory barrier, and the name rebind before the syscall. The fence is locked in that same effect, then `fence_matches` checks the locked descriptor. The lock stays held on `WrittenStage`.

S6 runs before any restage barrier or rename. Every retained directory is scanned for exactly the manifest's children (`.` and `..` ignored; a foreign name or a missing child is `Entries`), judged private, and compared to the device and inode kept at creation. Every file is reopened no-follow by name, judged private, compared by identity, and read with `read_bounded_accounted` at the written length. `Manifest::reread` decodes again, `verify_files` re-verifies the trust records, and `cross_joins` checks the marker, the staging nonce, `deliveringCore`, the store/generation/schema triple, the platform, and the handoff invocation with StepId 0.

S7 barriers the stage and its parent again, on `stage.directory()` and `stage.parent_directory()`, rechecks the stage name and the locked fence, then runs the five owner rechecks and returns their measured ledger use as `Δ_owner`. There are 44 slots: stage 0/1, directory `i` own `2+2i` and parent `3+2i`, file `j` at `30+j`, restage 41/42, I-parent 43. Each accepted receipt is checked with `is_for` on the handle it was taken on. `FullFlush` is the live kind; `Fsync` is accepted only as the primitive's named-unsupported fallback.

S8 copies `Published`'s values before the rename, then enters one effect whose reservation is `exclusive_publication_cost` plus the S9 confirmation cost plus `2 × Δ_owner`. Production calls `publish_exclusive_reserved(preview-v1)`. Success continues. `LostRace` releases the fence, leaves the stage, takes no I-parent barrier, and returns `Existing(LostRace)`. `NotPerformed` and `Indeterminate` return `Err` with that class, take no barrier, and leave the stage. The publisher's `Err` closes the ledger, so a lost race also leaves the attempt latched. Item 7 ends the act and returns the typed route; the caller drops the attempt, and nothing admits the winner.

S9, after a successful rename, spends the published exact name, takes the I-parent barrier on `publication.parent_directory()`, checks the locked fence, reopens the fence by name, requires I's device and inode to be the stage's, samples I's filesystem, then runs the same five owner rechecks inside `prepaid(2 × Δ_owner)`. The name spend is the same `binding_name_cost` already inside the reservation, so it does not consume the barrier's allowance. The measured owner rechecks, which are the overrun item 6 sizes, run after the barrier. Owner §4 states this order: confirm I's new name, apply the I-parent barrier, recheck the bound identities, then release the lock. A failure after the rename is `AfterRename`, and a budget failure there is `AfterRename(Budget)`. S10 releases the fence and returns `Published`.

`PublishedInstallation` is private, not `Clone`, and its `Debug` is non-exhaustive. It holds the target, S, K, the closure, the request, step and execution ids, and the command. It holds no handle, fence, lock or authority.

## Deviations

1. The fence's name and identity rebind runs in the file effect before `flock`; `fence_matches` then checks the locked descriptor in that same effect. The lock is on the descriptor just written.
2. The chain-name recheck is one of the five owner rechecks. `Δ_owner` is their measured cost, and S9 prepays twice that cost.
3. Stage-parent barriers use `stage.parent_directory()`, the duplicate handle §4 requires. The I-parent barrier uses `publication.parent_directory()`.
4. `publish_exclusive_reserved` closes the ledger on every failure, so `LostRace` latches the attempt while still returning `Existing(LostRace)`. The stage stays, the fence is released, and no barrier or retry runs.
5. A budget failure after the rename is `AfterRename(Budget)`. It is neither success nor `LostRace`.
6. There is no end-attempt call. Returning ends the act, and the caller drops the attempt. A latched ledger refuses a later recheck unpaid.
7. `recheck_exact_name`, `flock`, and the locked-descriptor observation are uncharged platform calls. The security effect spends `binding_name_cost`, `LOCK_COST`, and `fence_observation_cost` before them. S1's entropy, clock, and copies share `INPUTS_COST`, charged before the draw.
8. The indeterminate test spends the rename cost through a `cfg(test)` seam and does not rename. `Seam::live` and the non-test `rename()` return none, so production calls `publish_exclusive_reserved`. The seam's `return` leaves `publish` directly; the ledger guards still fail the attempt and dropping the fence releases it. The test observes the refusal, the latch, a free fence, an intact stage, and no I-parent barrier.
9. In tests, `Published.target` is the actor's disclosed I. `prepare_installation_parent_at` is `cfg(test)` and performs the walk on the scratch H. The storage recheck rebuilds the disclosed target from the actor and does not open it.

## Tests and safety

The twelve tests run on a scratch root from `test_scratch::temp_dir()`. They cover the private P0 tree and its modes, ACLs and 44 `FullFlush` barriers, the fence held through the act and free after, readers of the pair, marker, node and `state.v1`, the loser route, a moved stage, a scripted indeterminate rename, barrier failures at slots 0, 9, 30, 40, 41 and 43, an `Fsync` fallback at 1, 30 and 43, ledgers one edge short of the stage, directory 0, the fence and the rename, validation refusals, an owner change before the rename, one published winner and one `LostRace` from two threads, and `NotPristine` with no stage created. The happy-path test keeps the attempt inside the 65536 / 131072 / 256 MiB caps.

`~/Library/Application Support/OpenSIP` was absent before the replay (`exists` false, not a symlink) and absent after it.

## Inventory v74

v74 is v73 plus three sorted rows and nothing removed: 728 rows become 731. `installation_stage.rs` and `installation_publication.rs` are `service`. `installation_publication_tests.rs` is `test`. Every inherited file row matches. Packages and pending decisions match. The document standing text is this unit's. The five carried description overrides are the same paths and the same before/effective text; `package.json` and `schemas/sources/imported-v1.schema.json` move by the three inserted rows, and both selectors still name those files. The helper is byte-identical (2917 bytes, sha256 `bb82ef057ab4bb897f72b9a1f463ac67e3a5c60947649507d4c4d4532f9dd110`). Its recorded run is 5 projection rows, PASS, and 28 corruptions refused.

## Replay

- `cargo test --locked --offline -p opensip-security --lib`: exit 0. 526 passed, 0 failed, 2 ignored.
- `cargo test --locked --offline -p opensip-platform --lib`: exit 0. 212 passed, 0 failed, 1 ignored.
- `cargo test --locked --offline --workspace --all-targets`: exit 0. 1066 passed, 0 failed, summed from the package results (security 526/0/2 and platform 212/0/1 inside that run).
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Linux `cfg` branches were not compiled on this macOS host. Do not commit.
