REVIEWER review: law X4 r1, the live security guards (operation grant, live revocation, stale guards, observer latch). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. Law review; no product cargo. Product HEAD is f7acb6d; you may read it.

Subject: docs/implementation/m2/live-guards-x4/PROPOSAL.md r1 (pin in hashes.txt). Context:
- EXIT-PLAN.md row X4;
- the build plan's DR-G09 and failure cases F18, F19, F26, F38, F39, F41 and F53;
- the security model's S6 and S7 (observer tick and lock order);
- laws 463 (revocation), 468, 458c, X1 and X3a;
- product `commit_authority.rs`, `revocation.rs` and `root_payload.rs`.

## Decide

- **Item 1 (lead decision).** Is splitting the grant kinds sound: an internal operation grant now, and only the admission check for the repo-execution grant, with `execution.rs` left to M5?
- **Item 2 (lead decision).** Is it sound to capture the start trust state from the session's fenced read, with no second read?
- **Item 3.** Is the authority checkpoint sound: under the journal append lock, clock-bounded revocation, observer latch, every guard rechecked, single-use permit?
- **Item 4 (lead decision).** Is "no stale refresh; any difference latches" right?
- **Item 5 (lead decision).** The observer:
  - Are the 5 s tick and 10 s stall, reading through retained handles without the fence (S7 lock order) and the per-check ledger right?
  - Is the per-check ledger a forbidden branch-local reset?
  - Can the trust current pointer be re-read through retained handles, or will the observer fail-stop on every pointer change?
- **Items 6 to 8.** The revocation outcomes, the rows (check each detail and class against the registry and S12), and the budget.
- **Items 9 and 10.** The failure-case coverage and the unit split.
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
