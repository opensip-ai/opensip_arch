#!/bin/zsh
# J3a's X9 source pins: which harness sources the J3a diff touches. The
# harness sources are byte-identical at X9-6's C (3d2d5b5) and at 1d24900
# except as main's own units changed them; J3a touches crates/platform
# (lib.rs: the identity types; crash_barrier.rs: the inject-id reservation)
# and crates/host/tests (the X8 case table and sixteen new cases), and no
# crash_barrier!/crash_scope! site, required-runs file or checker.
set -u
cd /Users/sb/code/opensip-ai/opensip-j3a
H=(tools/check_crash_matrix.py tools/tests/test_check_crash_matrix.py crates/platform crates/storage/tests crates/host/tests crates/storage/src/crash_matrix_support crates/storage/src/crash_matrix_support.rs crates/host/src/crash_matrix_support crates/host/src/crash_matrix_support.rs crates/security/src/crash_matrix_sites.rs crates/security/src/crash_matrix_census.rs crates/security/src/crash_matrix_support crates/security/src/crash_matrix_support.rs)
echo "head $(git rev-parse HEAD)"
echo "== git diff --stat 3d2d5b5 1d24900 -- harness (main's own changes since C):"; git diff --stat 3d2d5b5 1d24900 -- $H | cat
echo "== git diff --stat 1d24900 -- harness (the J3a worktree):"; git diff --stat 1d24900 -- $H | cat
echo "== untracked harness files:"; git ls-files --others --exclude-standard -- $H | cat
echo "== required-runs sha256:"; shasum -a 256 crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json crates/host/tests/fixtures/crash-matrix/required-runs.v1.json
echo "== diff lines naming crash_barrier!/crash_scope!/observe_clock/native_clock:"; git diff 1d24900 -U0 | grep -E '^[-+][^-+]' | grep -E 'crash_barrier!|crash_scope!|observe_clock|native_clock' || echo "  (none)"
echo "== files the diff touches:"; git diff --stat 1d24900 | cat
