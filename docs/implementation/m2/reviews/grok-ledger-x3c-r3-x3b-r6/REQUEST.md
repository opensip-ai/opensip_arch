Grok re-review: X3c r3 and X3b r6 after your r2/r5 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-ledger-x3c-r3-x3b-r6.

Subjects (pins in hashes.txt):
- X3c `ledger-blob-x3c/PROPOSAL.md` r3 (diff against PROPOSAL-r2.md);
- X3b `journal-x3b/PROPOSAL.md` r6 (diff against PROPOSAL-r5.md).

## Changes

- **RF-1 (both).** If the `SEAL` path stops before the evidence `COMMIT` (a staging failure, a failed checkpoint, no permit, an observer latch, or any error after `SEAL`), the order is:
  1. roll back the ledger transaction;
  2. release level 4, then each level-3 transaction;
  3. append F19's `REV` through a fresh level-3-then-level-4 acquisition.

  Level 3 is never reacquired under level 4. Every exit releases level 4 exactly once.
- **X3b RF-2.** `PROPOSAL-r4.md` now equals the accepted r4 bytes (sha256 `296c0567…`). The same correction was made to six other snapshots in commit 62552a53d.

## Decide

Are the findings closed? Is anything new wrong?

Write one REVIEW.md, plus `x3c/review.json` and `x3b/review.json`. Each must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Do not commit.
