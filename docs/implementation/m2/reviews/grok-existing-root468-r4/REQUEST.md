Grok review: law 468 r4, an owner-directed amendment after r3 acceptance. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-existing-root468-r4. Law review; no product cargo.

Subject: docs/implementation/m2/existing-root-admission-468/PROPOSAL.md r4 (pin in hashes.txt). `diff` it against PROPOSAL-r3.md.

## Why

Implementing 468b found that the ordinary installation fence re-observes the whole chain from `/` on every attempt, uncharged. At its own published per-observation cost, one attempt on a `/Users/<name>` home needs about 126k of the owner's 131,072-edge cap, before the two rechecks. It also reads an omitted ACL as "no writers", which 461 retires. Item 4 cannot charge it honestly. On 2026-09-28 the owner chose to have the gate also borrow `InitialPlatform`'s omission premise.

## Changes

- **Item 2.** The sealed capability lends a third thing: the premise, with exactly 465 item 4's scope (root to H, `Library`, `Application Support`, through the premise's own `fstatfs`). It is never used for `OpenSIP` or I. With no premise, those components refuse on an omitted ACL.
- **Item 3.**
  - A new step 0: a charged, retained, no-follow walk from root to I, using the 460 and 465 predicates.
  - Step 1: the fence file is opened through the retained I handle. It is the same fence file and lock that ordinary holders take. A busy fence also latches the gate.
  - The recheck set now includes the retained chain.
- **Item 4.** The chain walk and fence attempt are charged. The post-barrier recheck is reserved with the barriers, as in 467 item 6.
- **Items 5 and 6.** An incomplete or contradictory I now has a public row: request-rejected, exit 2, `CONFIG.INVALID`, existing `CONFIG.CUSTODY_REFUSED` with subject `installation-incomplete`. There is no new code; the owner allows only the three.

## Decide

- Is the premise's scope exactly 465 item 4's, and is it safe to lend it to the gate?
- Does reaching the same fence file through a charged retained walk preserve owner §5 and 467 item 9's exclusion?
- Is the incomplete-I row a faithful existing-vocabulary route, given owner.md §5 and §7 ("unavailable under the relevant owner")? If not, name the correct existing route.
- Does the observation-only read path in item 4 have the same budget problem? If so, say whether it belongs here or in 458c.
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
