# Native security validation conditions

The private native security candidates test real retained descriptors, directory names, owner/mode/ACL observations and installation fences. Their fixture homes are synthetic. Passing them is not release qualification or proof that an actual user installation is admitted.

Run the security suite serially, on a host without a concurrent native fixture suite:

```sh
RUST_TEST_THREADS=1 cargo test --offline --locked -p opensip-security
```

On macOS, preserve the account's normal OS-provided `TMPDIR`, or explicitly obtain it from `getconf DARWIN_USER_TEMP_DIR`. Do not move these fixture homes beneath world-writable `/tmp`: ancestor custody checks correctly reject that location. A distinct Cargo target isolates build outputs, but it does not isolate filesystem ancestors observed by runtime fixtures. Do not run generator temporary-directory probes alongside the native suite either.

These conditions must be carried into the eventual product developer/CI entrypoint before materialization. They currently describe private candidate validation; they do not silently change the selected product, waive a source-policy gate, or create an implicit production retry.

The completed author366 run passed388 tests with two pre-existing ignored tests and four lifetime doctests, using one test thread. Actual365 review separately found default-parallel native observation failures, then encountered custody refusals when its temporary directory was relocated beneath `/tmp`. Preserve each failed run and its environment; later passing runs do not erase them. Concurrent activity alone does not identify the precise mutator or ancestor responsible for `ChangedDuringRead`.

A failed fixture setup or incidental custody error is not a successful fault control. Verify that each deliberate code fault compiled and reached its intended assertion. Use isolated build targets and verify restored source before a baseline replay; historical stale-build evidence must remain distinguishable from a product result.

Record the source manifest, exact command, Rust toolchain, relevant test-thread/temp-directory settings, result and cleanup. Coordinate independent author/reviewer native runs explicitly. Only manage processes positively identified as belonging to the current validation job; never stop another reviewer or root task to manufacture isolation.
