Grok review: law X3d r1, the CommitSession storage facade. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-commit-session-x3d-r1. Law review; no product cargo. Product HEAD is 5b5f04c.

Subject: docs/implementation/m2/commit-session-x3d/PROPOSAL.md r1 (pin in hashes.txt). Context:
- EXIT-PLAN row X3d;
- the accepted laws X2 r5, X3b r6, X3c r7, X4 r7 and X4T r5;
- build plan lines 25–190 and failure cases F06, F11–F19, F32, F34 and F36–F41;
- product `storage/commit_authority.rs`, `recovery.rs` and `ledger_store`.

## Decide

- **Item 1.** Are the types and owners right: security owns `CommitSession`, `JournalWriteTxn`, `JournalSealBinding` and `StoppedSession`; storage owns `PreparedCommit` and `PublishedCommit`; the adapter trait is private? Is storage's new dependency on the evaluator allowed by `check_package_edges` and the build plan?
- **Item 2 (lead decision).** One operation, one attempt, with a 16-byte random execution ID.
- **Item 3.** The `prepare_commit` order, F32 capacity, and the F34 duplicate route. In particular: should a duplicate before X6 exists be the invariant row?
- **Item 4.** Is the `publish` order exactly consistent with X3c r7 item 8, X3b r6 item 5 step 7 (including the stop order) and X4 r7 items 2 and 3?
- **Items 5 and 6.** The latch for F38, F39 and F41, and the separate outcome types.
- **Item 7.** The end path (X4c merged here): `REV` and `CLN` through a fresh lock acquisition under the lease, then X3b's end step.
- **Items 8 and 9.** The budget and the rows; check them against S12.
- **Items 10 to 13.** The boundaries, X8's must-not-compile list, the failure-case coverage and the units.
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
