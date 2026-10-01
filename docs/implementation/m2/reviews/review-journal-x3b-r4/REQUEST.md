REVIEWER re-review: law X3b r4 after Grok's r3 finding. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. Law review; no product cargo.

Subject: docs/implementation/m2/journal-x3b/PROPOSAL.md r4 (pin in hashes.txt). `diff` it against PROPOSAL-r3.md.

## Change (RF-1)

The floor table's no-carrier rows are now total. A present floor with no carrier resumes INIT only when there is no witness and the floor is exactly `grantGeneration 1, lastSeq 0`. Any other state, such as a present witness or a non-INIT floor (for example generation 2 at `lastSeq 0`), is `uncertainTailLoss`.

## Decide

Is RF-1 closed? Is the table now total? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
