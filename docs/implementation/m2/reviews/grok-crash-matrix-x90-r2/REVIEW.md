# X9-0 r2 — rebase onto abf2a48

**Verdict: ACCEPT-UNIT.** Inventory v114 is ACCEPT on v111.

This round moves the accepted r1 unit onto product `abf2a489047fc6c5145266e9aa171de9191de5f9` and rebuilds v114 on the lock’s selected parent, inventory v111. The law is still X9 r1 (`325ccd75…`, 50022 bytes). Judgment calls 1–20 stay accepted. The fifteen product files are byte-identical to r1.

## Rebase

Worktree `/Users/sb/code/opensip-ai/opensip-x9-0` is detached at `abf2a48`. `git diff --stat 97f630a abf2a48 -- crates/platform tools Cargo.toml Cargo.lock` is empty, so those trees and the workspace manifests are the same blobs r1 sat on. `git diff abf2a48` is 153961 bytes, sha256 `351f1b3b1842228287f494346a0476ee635813f7beeba0026b346bc101d7005a`, the same bytes as r1’s `git diff 97f630a`, index lines included. The diff contains no conflict markers.

Status is eight unstaged modifications and seven intent-to-add paths. Each new path is the empty index blob `e69de29` and is absent from `abf2a48`: `crash_barrier.rs`, `crash_barrier/driver.rs`, `crash_barrier/self_tests.rs`, `crash_macros.rs`, `crash_matrix_tests.rs`, `tools/check_crash_matrix.py`, and `tools/tests/test_check_crash_matrix.py`. Every hashes.txt pin matches, and the fifteen product pins are the r1 pins.

The r1 request’s “17 self-tests” figure counted the `crash` filter. That filter matches the 13 `#[test]` functions in `crash_barrier/self_tests.rs` and the pins in `crash_matrix_tests.rs`. Five pins are compiled in a featureless build; `without_the_feature_points_leave_only_their_effect` is `#[cfg(not(feature = "crash-matrix"))]`, so the feature lane keeps four. The barrier module is compiled only with the feature, so the thirteen self-tests are absent from the featureless lane. The sources are the r1 bytes.

## Inventory v114

v114 is 393913 bytes, sha256 `5a6f2b74f549e2e7b8bce26e6df9f3e9b00c01039728f47e68521fc5002fceb4`. Parent v111 is 384661 bytes, sha256 `88c7178c7b248db1bc305e0951650797eab5074a4720593cf7cdef20df9d1d6d`. The successor record is 20395 bytes, sha256 `808220d37f1e6a8044a050e03d8798d624090f8737289062b77a76d5968d2452`. The subject manifest is 2109 bytes, sha256 `d02c5b450f17f2de07cfb2d17d27c007a3a08b7a35acbc610c4465a4b2574270`.

The lock’s last inventory successor is that v111 pin (76 inventory successors, 72 contract successors, 16 inheritance rows). `design-lock.json` and `tools/verify_design.py` match `verifier-anchor.json` at head `abf2a48`. The worktree lock and `/Users/sb/code/opensip-ai/opensip/design-lock.json` are the same bytes.

v111 has 797 file rows and v114 has 804. Both lists are sorted and have no duplicate paths. The seven added paths are the seven intent-to-add files. Every inherited row is equal by value to v111. `packages`, `pendingDecisions`, and `schemaVersion` match v111. The two carried unresolved obligations match v111’s successor record. The inventory standing is the X9-0 test-only standing.

The added roles and standing are the r1 set, each `standing: proposed`: `crash_macros.rs` public-api, `crash_barrier.rs` and `driver.rs` service, `self_tests.rs` and `crash_matrix_tests.rs` test, `check_crash_matrix.py` tooling validator, and its test a tooling test.

The successor’s sixteen projection rows are sorted, unique, and bound to v111. Each parent pointer names the v111 row whose description is `before`. Each candidate pointer names the v114 row at the same path, and that stored description is `before`. The inherited row at each of those paths equals the v111 row.

`~/Library/Application Support/OpenSIP` is absent.

## Replay

Replayed here with python3.14, read-only:

- `verify_projection.py` against the worktree lock: PASS, 16 rows, 83 corruptions refused.
- `verify_scratch.py` on the worktree, appending v114 in memory: passed, 77 inventory successors, 72 contract successors, 16 inheritance rows, v114 selected.
- `tools/tests/test_check_crash_matrix.py`: 11 OK.

The workspace suite, the crash-matrix feature lane, clippy, `cargo fmt --check`, `check_package_edges`, and the release guards were not replayed. The fifteen unit files match accepted r1, and `crates/platform`, `tools`, `Cargo.toml`, and `Cargo.lock` are the same blobs from `97f630a` to `abf2a48`. `build_v114.py` was not run; it writes the architecture tree.

## Verdict

ACCEPT-UNIT. Inventory v114 is ACCEPT on v111. `requiredFindings` is empty on both.
