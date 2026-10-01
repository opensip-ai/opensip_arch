Grok review: law X1 r1, the ordinary platform owner for writers that are not creators. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-ordinary-platform-x1-r1. Law review; no product cargo. Product HEAD is d1b5eda; you may read it.

Subject: docs/implementation/m2/ordinary-platform-x1/PROPOSAL.md r1 (pin in hashes.txt). Context: EXIT-PLAN.md row X1, 468 r5 items 2 and 6, 458c r6 item 1, owner.md §5 (durable/write binding), and `host::installation_entry`.

## Decide

- **Item 1 (lead decision).** Is a sealed-purpose `PlatformReceipt<Read|Write>` from the one `produce_on` sound under 458c item 1's one-producer rule? Can a Read receipt reach the gate, or a Write receipt reach the read session?
- **Item 2 (lead decision).** Is the admission order sound: receipt recheck, gate, receipt recheck while the fence is held, release on failure? Does it grant nothing beyond `DurableInstallation`?
- **Item 3.** Is the writer classification right, and is the absent-I behavior (`NotInitialized` through positive absence; never create) right?
- **Items 4 to 7.** Standing, the two-ledger budget (lead decision), the 468 item 6 rows only, and one entry per process.
- **Item 8.** The unit split.
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
