Grok review: law X3c r7, an amendment found while implementing X3c-1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-ledger-blob-x3c-r7. Law review; no product cargo.

Subject: docs/implementation/m2/ledger-blob-x3c/PROPOSAL.md r7 (pin in hashes.txt). `diff` it against PROPOSAL-r6.md, which equals the accepted r6.

## Change

SQLite cannot change the journal mode inside a transaction. So WAL is selected immediately before the DDL transaction. A crash between the two leaves a non-empty, schema-less file, which is already `LEDGER.CORRUPT` under item 2.

## Decide

Is the amendment sound? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
