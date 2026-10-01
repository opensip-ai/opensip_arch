REVIEWER re-review: X3a-1 r2 (selected store endpoint) after Grok's r1 finding. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. If you build, use a CARGO_TARGET_DIR under that directory.

Subject: the same worktree `/Users/sb/code/opensip-ai/opensip-x3a1` (base 84a8bfd). Pins are in hashes.txt. Save `git -C <worktree> diff` as product.diff and report its sha256. The r1 review is `reviews/grok-store-endpoint-x3a1-r1/`. v83 and every arch pin are unchanged.

## Change (RF-1)

`lineage_bound` marks the session limit whenever the bound is 64 (`>=`), including G+1 == 64. A chain that has not ended after 64 nodes is the budget row (`WorkBudgetError::Record`), with no chain finding, on both the gate and the session. The chain row is only for a stop at a generation bound strictly below 64.

Three new tests:
- the gate and the session at G=63 with a 65th predecessor;
- a bound unit test at G 62, 63, 64 and `i64::MAX`.

Both G=63 tests were confirmed to fail with the old comparison.

## Checks

- Workspace: 1192/0, on two runs. Clippy and fmt are clean.
- `check_package_edges` passes.
- verify_scratch (v83) passes.

## Decide

Is RF-1 closed? Is anything new wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of store-endpoint-inventory-v83-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v83, parent (the v82 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
