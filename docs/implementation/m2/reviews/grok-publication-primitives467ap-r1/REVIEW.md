# Review: publication primitives 467a-p and inventory 73

Grok is the single reviewer. Claude Opus 5.5 leads. Review of the charged stage, publish, and file primitives, and inventory v73. No repository edits.

Product HEAD `f52e5eb55966d6133d5da64e3812b4b68a24e253`. The five files match `hashes.txt`. `file_effects.rs` is new (24895 bytes, sha256 `d8cc9f12d1ddcfd928228aace01ac094b17ffe2284e8a2cef1dcd7a15e39d2f8`). The subject manifest matches `subjects.txt` (1769 bytes, sha256 `807193ff9918dc4a9860fbe2b210e6f87bc763950c6c4006c6df73b0e11bdd9d`), and every file it lists matches. Law is 467 items 1, 4, 6 and 7. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Primitives

Every new call is charged or spent before it runs.

`private_directory_stage_cost` reserves eight nonce candidates before the first draw: two exact-capacity allocations and one `mkdirat` each, then the parent duplicate, the no-follow open, the two kind checks, and one binding recheck. The name is still `.opensip-stage-install-` plus 32 lowercase hex. The mode is `0700`. No ACL call is made. `EEXIST` skips that name unread. The existing unaccounted stage function is the same loop.

`exclusive_publication_cost` reserves the final name at 1023 bytes plus the NUL, the recheck before `renameatx_np(RENAME_EXCL)`, the rename, and the recheck after it. `classify_directory_rename` is the item 7 split. A raw `EEXIST` with visibility `Unchanged` is `LostRace`. A synthetic `AlreadyExists` with `Unchanged` is `NotPerformed`. Every `Indeterminate` visibility, including `EEXIST` whose postcheck failed, is `Indeterminate`. The accounted and reserved publishers return that error, so the scope closes. The loser is not a success. Releasing the fence lock stays outside this charge. `publish_with` is unchanged.

`create_exclusive_regular_cost` is the NUL-terminated name and the new descriptor, charged before the copy: no-follow `O_CREAT | O_EXCL | O_CLOEXEC` at `0600`, then `fchmod` to `0600`. A raw `EEXIST` is `EntryExists` and leaves the scope open. Every other outcome fails it. Nothing existing is changed, and no ACL is added.

`write_new_regular_cost` is `n` positioned writes and `n + 1` positioned reads, with `n = ceil(len / 64 KiB)`, one status read, and one file barrier. A short write or a short read is an error. `fstat` must show a regular file of that length. The bytes are compared, and one more read at the end must return zero. The barrier is `F_FULLFSYNC` on macOS with no fallback, and `fsync` on Linux. The receipt borrows the handle and `is_for` compares that object. The verify buffer is a stack array, so the cost is 0 objects and 64 KiB plus the status buffer.

`ReservedPostchecks::prepaid` spends the allowance first, then runs a `WorkScope` whose charges draw from that carved credit and do not move `used()` again. A charge past the allowance is `ReservedPostcheck` before the work it would cover, and it closes the ledger. A swallowed nested failure or an unwind also closes it. Unused allowance is not refunded.

## Inventory v73

v73 is v72 plus `crates/platform/src/filesystem/file_effects.rs`, in sorted order: 727 rows become 728, and nothing is removed. Every inherited row matches aside from the five carried description overrides. Packages, dependencies and pending decisions match. The row role is `adapter`. The helper is byte-identical to the earlier one (2917 bytes, sha256 `bb82ef057ab4bb897f72b9a1f463ac67e3a5c60947649507d4c4d4532f9dd110`). Its recorded run is 5 projection rows and 28 corruptions refused.

## Replay

- `cargo test --locked --offline -p opensip-platform --lib`: exit 0. 212 passed, 0 failed, 1 ignored.
- `cargo test --locked --offline --workspace --all-targets`: exit 0. 1054 passed, 0 failed.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
