Grok re-review: law X4 r4 after your r3 finding. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-live-guards-x4-r4. Law review; no product cargo.

Subject: docs/implementation/m2/live-guards-x4/PROPOSAL.md r4 (pin in hashes.txt). `diff` it against PROPOSAL-r3.md.

## Change (RF-1)

X4T's fenced admission is the monitor's first `read`, including its write-ahead floor. It runs at X2 r5 item 7's lease-free point, under the fence and before any lease.
- Item 2: 7a only moves the already-run monitor, view and gate, and publishes no trust state.
- Item 6: the guard is built in 7a from those, with no admission and no trust write.
- Items 8 and 9: the refusal and the charge happen at the lease-free point, with no charge inside 7a.
- The tests and the X4a unit text are aligned to match.

## Decide

Is RF-1 closed? Does no remaining sentence place the X4T admission or a trust write inside 7a? Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
