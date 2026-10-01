# F3 r1 — test scratch isolation

Grok. Test-support only. Worktree `/Users/sb/code/opensip-ai/opensip-f3` at `7e676a93567bfb5030e01cc11b56de6831f8d19c`. `hashes.txt` recomputed 4/4. The OpenSIP support directory is absent. `subject.diff` is `git diff HEAD`: 85051 bytes, sha256 `9a22aafca03b1ab7257e6e08dac859eec19b96ae72a9c6b810897fe759bb9d51`, 4 `diff --git` headers.

## Decisions

The change is test code. `lib.rs` edits sit inside `#[cfg(test)] mod test_scratch`. `native_census.rs` and `native_current.rs` edits sit inside `mod tests`. `store_endpoint_tests.rs` is a test file.

The root cause is right. The census fixture, the current fixture, and `ReadFixture` (which the endpoint tests use) were created through `temp_dir()`, which returned the shared system temp directory. Those walkers compare every ancestor. Another process creating or removing an entry there changes that ancestor and the walk refuses `Root(Descriptor(ChangedDuringRead))`. `temp_dir()` now returns `<temp>/opensip-test/<pid>-<nanos>`, created at mode 0700. A sibling process's files are not on this process's ancestor chain. `opensip-test` itself changes when a test process creates its private child, and `settled` absorbs that residual. `acl_scratch` still keys off `temp_dir()`, and `above_acl_scratch` still skips ancestors by device and inode, so 461a's horizon is unchanged.

`settled` is narrow enough. It re-runs the whole test at most 8 times, with backoff, only when the panic payload is a `String` or `&str` containing `ChangedDuringRead`. On this toolchain a formatted panic boxes a `String`, so `assert` failures and the census re-raise are visible to that check. Any other payload or message is resumed at once. The last attempt's panic is always resumed. Assertions are not weakened: the attempt that returns still had to pass them. A defect that reports `ChangedDuringRead` on every attempt still fails. The census visitor-stop loop re-raises only a refusal that reached no visitor and whose cause is `Root(Descriptor(ChangedDuringRead))`. Any other early refusal still fails the visit-count assertion. All 16 census tests, all 6 current tests, and all 6 endpoint tests are wrapped, and those are every `#[test]` in the three modules.

## Replay

Reviewer's own, Rust 1.95.0, `cargo test --locked --offline -p opensip-security --lib -- native_census:: native_current:: store_endpoint::`: 28 passed, 0 failed, 634 filtered out. Workspace suite, clippy, fmt, and the lead's repeated runs were not replayed. The cargo target was removed.

## Verdict

ACCEPT.
