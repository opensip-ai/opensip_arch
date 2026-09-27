Grok review a small test-only fix, r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-test-isolation-filesystem346-r1. You own the native lane until your report is written. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline.

Product HEAD ccf5f18. One uncommitted file is pinned in hashes.txt: crates/platform/src/filesystem/descriptor_filesystem.rs. Only the test `native_filesystem_original_file_lock_and_all_path_components_stay_owned` changed.

Problem: the test calls `path.observe_directories()` over the fixture's full ancestor path, which includes the shared per-user temp directory. `observe_descriptor` samples each directory before, during and after its ACL read, and returns `ChangedDuringRead` if a sample changes. Parallel tests create and remove entries in that temp directory, so the call occasionally fails. That is correct product behaviour, but it makes the test flaky: it failed once in a full workspace run during 465.

Fix: retry `observe_directories` up to 8 times, and only on `ChangedDuringRead`. Any other error, or 8 changed samples in a row, still fails the test. Nothing in production changed. The platform lib passed 5 of 5 runs; clippy and fmt pass.

Decide: is this retry test-only and narrow enough, or does it hide a real defect? Would isolating the fixture elsewhere be better (any path's ancestors include a shared temp directory)? Replay the platform lib a few times.

review.json must contain top-level "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS) and "requiredFindings". Write REVIEW.md and review.json. Do not commit.
