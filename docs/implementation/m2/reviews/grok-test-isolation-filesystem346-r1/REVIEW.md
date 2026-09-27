# Review: filesystem test isolation 346 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Review of one test-only change. No repository edits.

Product HEAD `ccf5f18026f4c733e9d4a48d80f8745537070266`. `crates/platform/src/filesystem/descriptor_filesystem.rs` matches `hashes.txt`: 14405 bytes, sha256 `b8366f529958eab65f4125bba5bb75212038d899d320536fb4107f60eab79460`. The diff is the sampling loop in `native_filesystem_original_file_lock_and_all_path_components_stay_owned`. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Answer

The retry is test-only and narrow. `observe_directories` is unchanged. The test still opens its fixture under `std::env::temp_dir()`, whose ancestors include the shared per-user temporary directory. `observe_descriptor` returns `ChangedDuringRead` when a directory's sample changes across its ACL read. Parallel tests create and remove entries there, so that error is the product seeing a real change, and the test was failing on it.

The loop calls `observe_directories` at most 8 times and continues only on `ChangedDuringRead`. Any other error fails the test at once. Eight changed samples in a row fail it at `expect`. A stable sample is still compared to the filesystem samples, including the leaf equal to the locked file's observation.

Moving the fixture does not remove the race. Every absolute path has shared ancestors, and `/tmp` is shared with the directory-effects fixtures. The per-user temporary directory is the ancestor this suite mutates. Retrying only the error that names that mutation keeps a persistent failure visible.

## Replay

- `cargo test --locked --offline -p opensip-platform --lib -- native_filesystem_original_file_lock_and_all_path_components_stay_owned`, five times: exit 0 each time. 1 passed.
- `cargo test --locked --offline -p opensip-platform --lib`, three times: exit 0 each time. 189 passed, 0 failed, 1 ignored.
- `cargo clippy --locked --offline -p opensip-platform --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
