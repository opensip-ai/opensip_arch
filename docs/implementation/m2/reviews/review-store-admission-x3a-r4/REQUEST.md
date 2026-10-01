REVIEWER review: law X3a r4, an amendment after r3 acceptance found while implementing X3a-1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. Law review; no product cargo.

Subject: docs/implementation/m2/store-admission-x3a/PROPOSAL.md r4 (pin in hashes.txt). `diff` it against PROPOSAL-r3.md.

## Change

Item 2's producers drop 468c's `AdmittedInstallation`, as a lead decision. 468c's `route` drops the creator's attempt and `InitialCore` before the gate, per 468 r5 item 1, so there is no selected core to join the pair against. Carrying the creator's core values through `route` would reuse a creator observation. A creator invocation produces no endpoint, and X11 decides how creator commands reach a store, within 468 item 1 and X1 item 7. The rejected alternative is carrying the creator's core values through `route`.

## Decide

Is the amendment sound and consistent with 468 r5 item 1, X1 r1 item 7 and 467 item 9? Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
