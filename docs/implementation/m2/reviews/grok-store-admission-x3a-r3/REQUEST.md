Grok re-review: law X3a r3 after your r2 finding. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-store-admission-x3a-r3. Law review; no product cargo.

Subject: docs/implementation/m2/store-admission-x3a/PROPOSAL.md r3 (pin in hashes.txt). `diff` it against PROPOSAL-r2.md.

## Change (RF-1)

Item 2 now reads `trust/stores/S/state.v1` once per session like the other endpoint files:
- through the retained I, charged first;
- with an exact-length cap at the existing trust state decoder's own bound;
- decoded by that decoder, with its `C.store` (S, G, K) retained for item 1's join.

A present `state.v1` that is over its cap, undecodable, or whose `C.store` mismatches is a structural finding of kind `CurrentStore`. That is the incomplete row in a termination and `installation-incomplete:current-store` as a doctor entry. It is never a pass.

## Decide

Is RF-1 closed, and is the cap named correctly (the existing decoder's bound)? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
