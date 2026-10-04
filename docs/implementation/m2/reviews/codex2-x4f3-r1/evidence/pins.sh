#!/bin/zsh
# X4-F3's X9 source pins: the harness sources are byte-identical at X9-6's C
# (3d2d5b5) and at d2c00a9, and the X4-F3 diff touches none of them; the only
# crash-barrier line the diff touches is LD8-4's move of `x4.gate.latch.after`.
set -u
cd /Users/sb/code/opensip-ai/opensip-x4f3
H=(tools/check_crash_matrix.py tools/tests/test_check_crash_matrix.py crates/platform crates/storage/tests crates/host/tests crates/storage/src/crash_matrix_support crates/storage/src/crash_matrix_support.rs crates/host/src/crash_matrix_support crates/host/src/crash_matrix_support.rs crates/security/src/crash_matrix_sites.rs crates/security/src/crash_matrix_census.rs crates/security/src/crash_matrix_support crates/security/src/crash_matrix_support.rs)
echo "head $(git rev-parse HEAD) diff-sha256 $(git diff d2c00a9 | shasum -a 256 | cut -d' ' -f1)"
echo "== harness paths present at HEAD:"; for p in $H; do test -e $p && echo "  $p"; done
echo "== git diff --stat 3d2d5b5 d2c00a9 -- harness (empty = identical):"; git diff --stat 3d2d5b5 d2c00a9 -- $H
echo "== git diff --stat d2c00a9 -- harness (worktree; empty = untouched):"; git diff --stat d2c00a9 -- $H
echo "== required-runs sha256:"; shasum -a 256 crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json crates/host/tests/fixtures/crash-matrix/required-runs.v1.json
echo "== diff lines naming crash_barrier!/crash_scope!/observe_clock/native_clock:"; git diff d2c00a9 -U0 | grep -E '^[-+][^-+]' | grep -E 'crash_barrier!|crash_scope!|observe_clock|native_clock' || echo "  (none)"
echo "== files the diff touches:"; git diff --stat d2c00a9 | cat
