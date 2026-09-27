# Review: charged directory effects 465a r1

Grok is the single reviewer. Claude Opus 5.5 leads. Code review of the charged barrier and exclusive-create primitives. No repository edits.

Product HEAD `000c5ce472ab38ef67ff3f20f5d708fddf7386b6`. The five files match `hashes.txt`. `directory_effects.rs` is new (32647 bytes, sha256 `0fcf6e7691f50a2420f3bba2425eeda630f9e1537a3dbbce1552a03524247881`) and has no inventory row yet. Law is 465 items 2, 3 and 6. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Answers

Every call in the new paths is charged or spent before it runs. `directory_barrier_cost` is 0 objects, two status buffers, and 4 edges on macOS: the status before the flush, `F_FULLFSYNC`, the reserved fallback `fsync`, and the status after the flush. Linux reserves its one `fsync` and is not compiled on this host. Both accounted and reserved forms call `confirm_directory_with`, so the named-unsupported fallback (`EINVAL`, `ENOTSUP`, `ENOTTY`) and the post-status error precedence are the unaccounted primitive. The receipt stays a borrow of the handle. A short ledger returns `Budget` and does not call the flush.

`create_exclusive_directory_cost` is 4 objects, 12 edges, and `name + 1` plus two status buffers plus one `dirent`. It is computed from the name length and charged before `single_component` copies the name. The steps are `mkdirat` at `0700`, a no-follow `openat`, `fstat` and `geteuid`, `fchmod` to `0700`, a bounded scan, and the kind check on the returned handle. The scan is at most three `readdir` calls: `.`, `..`, and the read that ends the stream or finds another entry. libc's stream buffer is not counted.

`EntryExists` is only a raw `EEXIST` from `mkdirat`. It returns `Ok` and leaves the scope open. It opens nothing and changes nothing, including an existing directory, file, or dangling symlink. `NotFresh` is the synthetic case: `mkdirat` succeeded and the opened entry is not a fresh, empty, effective-user-owned directory, or the bounded scan sees another name. It fails the scope. `AfterCreate` is a native error after `mkdirat`, and that directory may remain. Neither is admission. The unaccounted `create_exclusive_directory` still returns the synthetic `AlreadyExists` through `is_fresh_owned_directory` and `empty_directory`, which wrap the split helpers. `private_access.rs` still calls that function.

The reserved create and barrier spend their cost inside an existing reservation. A ledger that cannot hold the postchecks does not enter the effect. `open_child_directory_reserved` and `observe_filesystem_reserved` spend the same costs as their accounted forms. The `after_mkdir` hook is private. Production passes a no-op.

The fixtures live under `/tmp`. The per-user temporary directory is an ancestor of the live path test that has failed on `ChangedDuringRead` when fixtures appeared and disappeared there. `/tmp` is not that ancestor.

## Replay

- `cargo test --locked --offline -p opensip-platform --lib`: exit 0. 189 passed, 0 failed, 1 ignored.
- `cargo test --locked --offline --workspace --all-targets`: exit 0. 1008 passed, 0 failed.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
