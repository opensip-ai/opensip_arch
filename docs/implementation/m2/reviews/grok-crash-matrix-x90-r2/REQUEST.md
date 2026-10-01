Grok review: X9-0 r2. This is a rebase-only recheck of the accepted r1 onto product abf2a48, with inventory v114 rebuilt on v111. Claude Opus 5.5 leads, and you are the single reviewer.

Rules:
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x90-r2.
- If you build or test, use a CARGO_TARGET_DIR under that directory.
- Run git only read-only, and only against the worktree below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.

## Background

You accepted X9-0 at r1 (`reviews/grok-crash-matrix-x90-r1/review.json`, sha256 `5644e37ffc3daeb5a111e81f6c0deebf1664b9f822a020b136d6ec74d82b7aba`). The verdict was ACCEPT-UNIT, with the inventory at ACCEPT: v114 on v108 at product 97f630a, and judgment calls 1 to 20 accepted.

Since then, X2e and X3b-3 have integrated. Product main is now abf2a48, and the lock selects inventory111.

This round moves r1 unchanged onto that base and rebuilds v114 on v111. The law is still X9 r1 (`crash-matrix-x9/PROPOSAL-r1.md`, `325ccd75…`). No judgment call, test or behaviour changes.

## The rebase

**How.** The worktree `/Users/sb/code/opensip-ai/opensip-x9-0` was moved from 97f630a to abf2a48. The intent-to-add entries were reset (the files were kept), then a stash, a detached checkout and a stash pop. The seven new files are intent-to-add again.

**Conflict: none.** `git diff --stat 97f630a abf2a48 -- crates/platform tools Cargo.toml Cargo.lock` is empty. abf2a48 changes only security files, `design-lock.json` and their tests. No hand resolution was needed.

**No product file changed.** All 15 files are byte-identical to r1, with every pin in `hashes.txt` equal to r1's. `git diff abf2a48` is again 153961 bytes, sha256 `351f1b3b1842228287f494346a0476ee635813f7beeba0026b346bc101d7005a`, identical to r1's diff, including the index lines, because the base blobs of the touched files did not move.

## A correction to r1's request text (no code change)

r1's request said "the 17 X9 self-tests and the 4 pins", and that "the 17 self-tests" passed in 11 runs. Both figures were wrong.

The `crash` test filter matches 17 tests:
- the 13 self-tests in `crash_barrier/self_tests.rs`;
- the 4 always-on pins in `crash_matrix_tests.rs` that build with the feature.

The fifth pin, the featureless expansion test, is cfg'd out under the feature, so the featureless lane runs 5 pins.

The 17 passed together in each of those runs, and the 13 pass alone here. The test files are unchanged.

## Inventory

`evidence/build_v114.py` rebuilt v114 on the parent the lock selects: inventory111, 384661 bytes, `88c7178c7b248db1bc305e0951650797eab5074a4720593cf7cdef20df9d1d6d`. Its parent map already listed v111's committed successor record.

**Rows.** The same seven added rows, with descriptions and standing unchanged from r1. The 797 inherited rows are equal by value, for 804 files. Packages, dependencies, pending decisions and carried obligations are unchanged. There are 16 projection rows.

**New bytes.** Reruns are byte-identical.
- v114: 393913 bytes, `5a6f2b74f549e2e7b8bce26e6df9f3e9b00c01039728f47e68521fc5002fceb4`.
- successor.json: 20395 bytes, `808220d37f1e6a8044a050e03d8798d624090f8737289062b77a76d5968d2452`.
- Subject manifest `crash-matrix-x90-inventory-v114-subject.json`: 2109 bytes, `d02c5b450f17f2de07cfb2d17d27c007a3a08b7a35acbc610c4465a4b2574270`.

**Text-only edits for the new parent:**
- the builder's docstring;
- the README's parent, row counts, order and projection lines (the order now records r1 on v108);
- verify_projection.py's parent comment;
- verify_scratch.py's docstring;
- verifier-anchor.json: head abf2a48, with the lock and verify_design.py pins at abf2a48.

## Checks on abf2a48

- **Full workspace without the feature, once:** 1486 passed, 0 failed, 3 ignored, across 26 binaries. That includes the 5 featureless pins.
- **Feature lane, `cargo test -p opensip-platform --features crash-matrix`:** 291 passed, 0 failed, 1 ignored. That includes the 13 self-tests and 4 pins.
- **Clippy,** `--workspace --all-targets -D warnings`: clean without the feature and with `--features opensip-platform/crash-matrix`.
- **`cargo fmt --check`:** clean.
- **`check_package_edges --lane host`** against v114: passes, with 19 declared and 19 resolved internal edges.
- **Checker tests:** `tools/tests/test_check_crash_matrix.py`, 11 OK.
- **verify_projection** against the real lock at abf2a48: PASS, 16 rows, 83 corruptions refused.
- **verify_scratch,** with v114 appended over the real lock at abf2a48: passed. 77 inventory successors, 72 contract successors, 16 inheritance rows, v114 selected.
- **Release guards:** not rerun. The release guard evidence of r1 depends only on the unchanged platform, CLI and tools bytes.
- **Real home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Is the product unchanged from r1, with no conflict and every file byte-identical?
- Is v114 right on v111, with the same seven rows and the inherited rows by value?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": `d02c5b450f17f2de07cfb2d17d27c007a3a08b7a35acbc610c4465a4b2574270`;
- "inventoryCandidateAssessment": an object with:
  - verdict and requiredFindings;
  - path `docs/implementation/m2/repository-file-inventory.v114.json`, bytes 393913, sha256 `5a6f2b74…`;
  - parent: the v111 pin above;
  - successorRecord: path `docs/implementation/m2/crash-matrix-x90-inventory-v114/successor.json`, bytes 20395, sha256 `808220d3…`.

Write REVIEW.md and review.json. Do not commit.
