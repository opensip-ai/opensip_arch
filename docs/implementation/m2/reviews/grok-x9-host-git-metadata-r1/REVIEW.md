# X9 harness host-Git metadata follow-up r1

Verdict: ACCEPT-UNIT.

On macOS the two X9 metadata helpers select `/usr/bin/git`. Other platforms still resolve `git` from `PATH`. `rustc` stays on `PATH`. Each Git child removes `GIT_CONFIG_COUNT`, `GIT_DIR`, and `GIT_WORK_TREE`, and sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`. `command` returns stdout only after the process reports success, so a failed `git status` cannot turn empty stdout into a clean worktree. The helpers do not set `PATH` or `HOME`, do not write a Git config, and do not change a product library, public outcome, matrix row, barrier, census, trace, expected value, clock, or limit.

The worktree is detached at `6bbd158f460ac31f22101206b86c511924ed6ec2`. The only product changes are `crates/host/tests/commit_matrix_tests.rs` and `crates/storage/tests/commit_tests.rs`. The evidence diff is 5296 bytes, sha256 `3392b6c13d7e34b93947e315a9cd962433d6e7c30459bf6b82acc10f2455b6bb`, and it matches `git diff`. The mandated PATH `/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin` does not contain `git`. `/usr/bin/git` is present, and `refs/opensip-x9-metadata-missing-control` is not a revision. Pinned authorities, both required-runs fixtures, `tools/check_crash_matrix.py`, and `crates/platform/src/crash_barrier.rs` match. The author logs record two passing metadata tests in each target (four total) and warning-denied Clippy for both targets, exit 0, under `nice -n 10`, a mode `0700` scratch, and absolute `cc`, `ar`, `ranlib`, and SDK paths. `rustfmt` used `skip_children=true` on the two integration files. The supplied script does not assign `HOME`. The OpenSIP support directory is absent. This review did not rerun Cargo, rustfmt, or the tests.

These four tests do not run a matrix row or qualify the product. X3c-3 remains the accepted code base. Its post-integration release, census, two whole clean-commit lead sets, and real check stay outstanding until this unit integrates. J4a, RW, and the O1-a, S-OP, and owner gates stay held.

## Inventory

Subject manifest sha256 `4b41abb889b62ed0d50e4cc43a477bf07a65e36189ce3b7a560267dd5d9e62c1` (1618 bytes). Its eight files match.

Inventory v163 is 611219 bytes, sha256 `36cab69d912dec5f6f56ef0c19a0504e3361975a01394d56f4ff092299c32da9`, with 1061 sorted unique paths. Both edited paths are already present: `crates/host/tests/commit_matrix_tests.rs` at index 148 (package `opensip-host`, role test) and `crates/storage/tests/commit_tests.rs` at index 773 (package `opensip-storage`, role test). No path is added. `inventorySuccessorRequired` is false. No inventory successor and no design-lock selection are proposed.
