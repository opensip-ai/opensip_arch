Grok review: law X3a r1, store admission under the write gate. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-store-admission-x3a-r1. Law review; no product cargo. Product HEAD is fdbedf4; you may read it.

Subject: docs/implementation/m2/store-admission-x3a/PROPOSAL.md r1 (pin in hashes.txt). Context: EXIT-PLAN.md rows X3a and X2, X1 r1 (accepted), 468b and 458c r6 items 5 and 7, owner.md §7 to §9, and the build plan's failure cases F00, F24 and F27.

## Decide

- **Item 1 (lead decision).** Is it sound to admit the store endpoint without a namespace, and leave the full store binding until a project is registered (X2, owner §8)? Does `SelectedStoreEndpoint` grant nothing beyond what it holds?
- **Item 2 (lead decision).** Each store file is read once per session, with a full metadata sample and its decoded value, and every recheck compares the full sample. Does that catch an in-place rewrite, and is it sound against owner §7?
- **Item 3 (lead decision).** Is the 64-node chain bound right, with the budget row beyond it and a pinned measured cost?
- **Item 4.** Is the read-side switch right, and is the extended source pin sufficient?
- **Item 5 (lead decision).** Are the rows right: `installation-incomplete:*` subjects, `NT-TCB-IDENTITY` with subject `selected-core-mismatch` for F24, and `STATE.SCHEMA_UNSUPPORTED` for an unsupported K? Check each against the registry and the 468 item 6 pairing.
- **Items 6 and 7.** The failure-case coverage and the unit split.
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
