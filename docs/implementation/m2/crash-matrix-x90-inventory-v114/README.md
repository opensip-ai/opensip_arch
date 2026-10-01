# Crash-matrix mechanism inventory114

Adds exactly seven files to inventory111 (units X2e and X3b-3, selected at product abf2a48):
- crates/platform/src/crash_macros.rs
- crates/platform/src/crash_barrier.rs
- crates/platform/src/crash_barrier/driver.rs
- crates/platform/src/crash_barrier/self_tests.rs
- crates/platform/src/crash_matrix_tests.rs
- tools/check_crash_matrix.py
- tools/tests/test_check_crash_matrix.py

It keeps all 797 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 804 planned files. No crate, dependency or package edge is added: the barrier uses only `std` and `libc`, which platform already depends on, and the checker uses only the Python standard library. The rows are unit X9-0: law X9 r1 items 1 to 5, 7 and 12.

- **crash_macros.rs (public-api).** `crash_barrier!` and `crash_scope!`, defined in every build. Without the feature they expand to their effect or to nothing.
- **crash_barrier.rs (service).** The feature-only module: the scope registry, the point grammar, kinds, the arming parser and the child rendezvous.
- **crash_barrier/driver.rs (service).** The parent driver (re-exec, records, resume, `SIGKILL`, the watchdog, death verification) and the census with its kill set.
- **crash_barrier/self_tests.rs (test).** Item 12's X9-0 self-tests, compiled only with the feature.
- **crash_matrix_tests.rs (test).** The manifest pin (item 2, guard 2), the no-sleep source pin (item 3), the featureless expansion check and the shared self-test workload. These run in every platform test build.
- **tools/check_crash_matrix.py (validator) and its test.** Item 7's checker and the release-absence scan (item 2, guard 4).

**The Cargo feature.** `crates/platform/Cargo.toml` gains `[features] crash-matrix = []`. The inventory has no feature field: a package row records the package's purpose and internal dependencies only, and `check_package_edges.py` reads only dependency tables, so the feature changes neither. The manifest pin in crash_matrix_tests.rs is the check item 2 asks for. No manifest dependency names the feature, and no `[[test]]` target requires it yet; the two matrix targets arrive with X9-2 and X9-5.

**Changes to existing rows.**
- `crates/platform/Cargo.toml`: the `[features]` table. Its description ("Declare this package, explicit dependencies and build targets.") stays true.
- `crates/platform/src/lib.rs`: the compile guard (item 2, guard 1), `mod crash_macros`, the feature-only `pub mod crash_barrier` (`#[doc(hidden)]`) and the test-only pins module. Its description stays true.
- `filesystem.rs`, `filesystem/file_effects.rs`, `filesystem/file_replace.rs`, `filesystem/directory_effects.rs`, `locks.rs`: each native durability effect is wrapped in `crash_barrier!(primitive, …)`. The points are `create` (the staging file, `create_exclusive_regular` and `create_exclusive_directory` with their charged forms), `write`, `file-barrier`, `rename`, `link` (the exclusive `RENAME_EXCL` publication), `directory-barrier`, `reopen-confirm` (`confirm_existing_regular`'s reopen), `lock` and `unlock`. Without the feature the wrapped effect is the same expression as before. `write_new_regular_charged`'s write loop moves into `write_at_zero` unchanged, and the macOS file barrier into `native_file_sync` unchanged. Their descriptions stay true.
- `tools/README.md`: a "Crash matrix (X9)" section. Its description stays true.

**Order.** Its parent is the inventory the real product lock selects: inventory111 (units X2e and X3b-3) at product abf2a48.
- It was first built on inventory108 (unit X3b-4) at 97f630a and accepted at r1. X2e and X3b-3 then integrated, so it is rebuilt on inventory111 with the same seven rows; the product files are byte-identical to r1.
- evidence/build_v114.py reads the parent from the lock. It maps inventory106, inventory108 and inventory111 to the successor records that bound their sixteen rows.
- It refuses to write over any path git already tracks, and while a lock selects inventory114. Reruns reproduce the same bytes.
- Succession is by the lock's parent pin, not by number.

**Projection.** The sixteen effective description overrides bound to inventory111 (carried unchanged from inventory108 back to inventory81) stay bound by stable file path, with parent inventory111.
- verify_projection.py is inventory108's helper with only its comment corrected to name its parent. It runs against the real lock at abf2a48, which selects inventory111.
- evidence/verify_scratch.py appends inventory114 in memory over the real lock, with a synthetic review and assent.
