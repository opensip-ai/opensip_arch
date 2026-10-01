Grok re-review: X4T-a r3, a rebase-only re-check before integration. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-current-trust-x4ta-r3.

You accepted the X4T-a r2 code and v90 (`reviews/grok-current-trust-x4ta-r2/x4ta/`). Since then, product main has moved to 8452ab9 (X2b-1 v93, F3), and X3c-1 integrates next as v94.
- The worktree `/Users/sb/code/opensip-ai/opensip-x4ta` is rebased onto 8452ab9. Save the diff as product.diff and report its sha256. X4T-a's own hunks are byte-identical. Only `trust/native_current.rs` moved, because F3 also edited it.
- The inventory is rebuilt as **v96, with parent v94**, adding the same two rows. verify_scratch passes both over the real lock (appending v94 then v96) and over a lock that already selects v94.
- The D1 deferral for the `accepted_store_fixture_tests.rs` description is unchanged.

Checks: 26 X4T-a and fixture tests, one full workspace run 1267/0, clippy, fmt and `check_package_edges`.

## Decide

Is the rebase faithful? Is v96 right on v94?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of current-trust-inventory-v96-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v96, parent (the v94 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
