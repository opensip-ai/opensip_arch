Grok review: X2d r2, a rebase-only recheck of namespace admission and leases (law X2 r8 item 7) with inventory v110 rebuilt on v109. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-namespace-lease-x2d-r2. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

## Background

You accepted X2d r1 as ACCEPT-UNIT, with no required findings. That acceptance is `reviews/grok-namespace-lease-x2d-r1/review.json`, pinned in hashes.txt. It covered:
- product 0206ce8 plus the diff (sha256 `90009b2e2fef312064a496bb7402b195146eebf03132876dd066544ce465bbb6`);
- v110 on v105 (subject sha256 `4ba60b8b47529cfe8fed82b809570918e9a48ae5be38e1f2a7ca4dd4ecc869f8`).

r1's REQUEST.md and REVIEW.md hold the full description and the twelve judgment calls. None of them changes here.

Since then X12b was integrated. Product main is now 6dd7363 (X12b: `crates/host/Cargo.toml`, `crates/host/src/{configuration.rs, configuration_tests.rs, doctor_ingress.rs, lib.rs}` and `design-lock.json` only). The lock now selects inventory109 (`policy-pack-x12b-inventory-v109`).

## What changed: only the base and the parent

- **Product.** The worktree `/Users/sb/code/opensip-ai/opensip-x2d` is now detached at 6dd7363, with the same uncommitted change; the two new files are intent-to-add.
  - X12b touched nothing under `crates/security`.
  - All six product files are byte-identical to r1. Compare the first six lines of hashes.txt with r1's.
  - `git -C <worktree> diff` is byte-identical too: sha256 `90009b2e2fef312064a496bb7402b195146eebf03132876dd066544ce465bbb6`, 75110 bytes, 6 files, 1620 insertions, 20 deletions.
- **Inventory.**
  - **Builder.** `evidence/build_v110.py` gains the v109 parent in its parent map (v109 → `policy-pack-x12b-inventory-v109/successor.json`, which bound the sixteen rows). Its docstring names both parents. The two added rows are unchanged.
  - **Rebuilt v110.** v110 was rebuilt on v109: 786 v109 rows by value plus the same two X2d rows, for 788 files. `packages`, dependencies, `pendingDecisions` and the carried obligations are unchanged, and the sixteen projection rows are re-bound to v109.
  - **Other edits.** These are rebase edits only, with no change to what the files check:
    - README's counts, parent and order;
    - verifier-anchor (head 6dd7363, the current lock);
    - verify_scratch's and verify_projection's comments.
- **Pins.**
  - **v109 parent:** `repository-file-inventory.v109.json`, 360591 bytes, sha256 `96df355ac8333940a08402feb21e0065a485cd7fd9f128fd470a83677c639e7c`.
  - **New v110:** 364396 bytes, sha256 `4d11a9d9578efa4dc0f6f963ff1d7a6cdc60c571087fadde8faed3438ecad6bc`.
  - **Successor record:** 20199 bytes, sha256 `1903fc699caa6907325387bace6588b4a6e1767b07e9e4b0123d6bd0132e9a4d`.
  - **Subject manifest:** `namespace-lease-x2d-inventory-v110-subject.json`, 2135 bytes, sha256 `26f7e3f327e4694f480e2f6a50ab4abaad708da5b9f5891e12cb3ee5977f391d`.
  
  All of these are untracked in arch until acceptance.

## Checks at 6dd7363 plus the diff

- Full workspace, one run: 1400 passed, 0 failed, 3 ignored. That is r1's 1390 plus X12b's host tests.
- `cargo clippy --workspace --all-targets --offline --locked -- -D warnings` and `cargo fmt --all --check` are clean. `rustfmt --check --edition 2024` is clean on both new files and on first_registration.rs.
- `check_package_edges --lane host` against v110 passes.
- verify_scratch (v110 appended over the real lock at 6dd7363) passes: 72 inventory successors, 72 contract successors, 16 inheritance rows, v110 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v110.py` reruns produce the same bytes.
- Every v109 row is equal by value in v110, and the only added paths are `namespace_lease.rs` and `namespace_lease_tests.rs`.
- `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Are the product files byte-identical to r1, with only the base moved to 6dd7363?
- Is v110 right on v109?
- Does anything in X12b's integration bear on X2d?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `namespace-lease-x2d-inventory-v110-subject.json` (lead's value `26f7e3f327e4694f480e2f6a50ab4abaad708da5b9f5891e12cb3ee5977f391d`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v110, parent (the v109 pin), successorRecord (the pin of `namespace-lease-x2d-inventory-v110/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
