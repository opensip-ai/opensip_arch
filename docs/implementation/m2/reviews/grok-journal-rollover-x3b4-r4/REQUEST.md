Grok review: X3b-4 r4, a rebase-only recheck of the accepted r3 onto product 704251e, with inventory v108 rebuilt on v106. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-journal-rollover-x3b4-r4. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

## Background

You accepted X3b-4 at r3 (`reviews/grok-journal-rollover-x3b4-r3/review.json`, sha256 `e873de1a819a49e05087ef6e7180d7eadc1682cb8a1a31fa9ca45078170031ff`): ACCEPT-UNIT, with the inventory at ACCEPT, v108 on v112 at product f1b8321.

Since then, X4T-a2 and X4T-b have integrated. Product main is now 704251e, and the lock selects inventory106. This round rebases r3 unchanged onto that base and rebuilds v108 on v106. The law is still X3b r10 (`PROPOSAL-r10.md`, `25a60824…`). No judgment call, test or behaviour changes.

## The rebase

- **How.** The worktree `/Users/sb/code/opensip-ai/opensip-x3b4` was moved from f1b8321 to 704251e by stash, detached checkout and stash pop. The two new files are intent-to-add again.
- **Conflict: none.** 704251e adds four lines at the end of `journal_store.rs` (the `publish_private_file` re-export for X4T r9 item 7). X3b-4's only `journal_store.rs` hunk is near the top: `SEAL_CEILING` and `seal_fits` beside `CARRIER_CAP`. Git merged them automatically, upstream's block is intact, and `cargo fmt --check` is clean. No hand resolution was needed.
- **Product files against the r3 diff.**
  - **The diff.** It is 163034 bytes, as in r3 (`a53c78f9…`), and now has sha256 `e4049b58580f84673ae1b833b617f34e8aaabb2c0e96a755bf2e2a438a2eeb33`. Compared line by line with the r3 diff, the only difference is the `journal_store.rs` header line, `index 7a77d4f..8e5eb77` becoming `index 2549367..4bd4f12`. That is the new base blob plus upstream's block. Every hunk is identical.
  - **Eight files byte-identical to r3:** carrier_floor.rs, carrier_floor_tests.rs, carrier_start.rs, carrier_start_tests.rs, carrier_append.rs, carrier_append_tests.rs, carrier_rollover.rs and carrier_rollover_tests.rs.
  - **`journal_store.rs`** is 724545 → 724763 bytes (`44626fb6…` → `319ceb07…`). That is exactly upstream's four-line block on top of X3b-4's unchanged hunk.
- **The new carrier module and upstream's re-export.** `publish_private_file` is X3b-1a's existing `pub(crate)` function in `carrier_floor`. X3b-4 does not change it, and the rollover calls it unchanged.

## Inventory

v108 was rebuilt by `build_v108.py`, whose parent map already listed `trust-floor-x4tb-inventory-v106`. The parent follows the lock: inventory106, 369829 bytes, sha256 `4b42c13f0ca1110588905bc2cd82a68ca874ea5e135ff22fb94d42a356630b32`.
- **Rows.** The same two added rows, with descriptions and standing (`law X3b r10, unit X3b-4`) unchanged from r3. 791 inherited rows equal by value, for 793 files, and 16 projection rows.
- **New bytes.**
  - v108: 376570 bytes, `9c6953f28572f6882bbdc71ae945104e4a4e65e5d7b87cae9cf91318d9eb1f44`;
  - successor.json: 20206 bytes, `173239c56f31870c59d617e25fbb5ea0e151f5924148b81e21b85ac3ee30ee29`;
  - subject manifest: `2f06f18728ffff1c95f538c8e9f1163de13b39b75253012a07115c8fe1331080`.
- **Text-only edits for the new parent:**
  - the builder's docstring;
  - the README's parent, row counts, order and projection lines;
  - verify_projection.py's parent comment;
  - verify_scratch.py's docstring;
  - verifier-anchor.json (head 704251e, with the lock and verify_design.py pins at 704251e).

## Checks on 704251e

- Full workspace, one run on the default `TMPDIR`: 1459 passed, 0 failed, 3 ignored. That includes the 68 carrier tests.
- Clippy `--workspace --all-targets -D warnings` and `cargo fmt --check` are clean.
- `check_package_edges --lane host` against v108 passes (19 declared and 19 resolved internal edges).
- verify_projection against the real lock: PASS, 16 rows, 83 corruptions refused.
- verify_scratch (v108 appended over the real lock at 704251e) passes: 75 inventory successors, 72 contract successors, 16 inheritance rows, v108 selected.
- `build_v108.py` reruns produce the same bytes.
- `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Is the product change against r3 exactly the rebase described: no conflict, upstream's block intact, X3b-4's hunks unchanged?
- Is v108 right on v106, with the same two rows and the inherited rows by value?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `journal-rollover-x3b4-inventory-v108-subject.json` (`2f06f187…`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v108, parent (the v106 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
