REVIEWER re-review: X2a r2 (project chain) after Grok's r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. If you build, use a CARGO_TARGET_DIR under that directory.

Subject: the worktree `/Users/sb/code/opensip-ai/opensip-x2a`, now rebased onto 99f1c35 (X3a-1 integrated, v83 selected). Pins are in hashes.txt. Save `git -C <worktree> diff` (new files are intent-to-add) as product.diff and report its sha256. The r1 review is `reviews/grok-project-chain-x2a-r1/`. v84 is byte-identical to r1, and its evidence now runs against the real lock.

## Changes

- **RF-1.** `same_birth` compares only device, inode and native birth (seconds and nanoseconds). Custody (mode, owner, ACL) is still judged by the custody recheck. Tests: a file created in the root, and `.opensip` created, both pass; a replaced root, or a different directory, fails.
- **RF-2.** Placement allocates nothing, because it compares borrowed path components. The spelling copy is charged first (`spelling_cost`). A test pins that placement takes zero objects and that a ledger one object short refuses before the copy.
- **Rebase.** The only conflict was the `custody.rs` module declarations; both modules are kept.

## Checks

- Workspace: 1209/0, on two runs. Clippy and fmt are clean.
- `check_package_edges` passes.
- verify_scratch passes with v84 over the real lock.

## Decide

Are RF-1 and RF-2 closed? Is anything new wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of project-chain-inventory-v84-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v84, parent (the v83 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
