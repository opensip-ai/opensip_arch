Grok review: law X4B r3, first trust acceptance. It answers your X4B r2 RF-1 (the monitor before F is chosen). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-trust-bootstrap-x4b-r3. Law review; no product cargo. Product HEAD is fc7dce7.

Subject: docs/implementation/m2/trust-bootstrap-x4b/PROPOSAL.md r3 (pin in hashes.txt). r2 bytes are preserved in PROPOSAL-r2.md (pinned too). Your r2 review is under /tmp/opensip-implementation/reviews/grok-trust-bootstrap-x4b-r2.

What changed:
- **Item 1.** The `FreshnessMonitor` and `FinalGate` are created first (X4 item 2). Their single first `read` runs the retained-capsule admission. On F absent, and only then, it runs the acceptance and the one confirming admission on the confirmed retained `state.v1`, then returns that view.
  - The acceptance and the confirming admission both use that read's clock sample. The confirming admission's tEval equals the F just written, so it writes nothing.
  - Everything stays on the fence already held, before any lease. X2e only moves the monitor, the gate and the view.
  - The r2 placement is recorded as rejected.
- **Item 3.** The anchor and tEval come from that read's sample.
- **Item 8.** The charge is the gate ledger, inside that read, as X4T item 11 charges the fenced first read.
- **Item 10.** The ordering test brackets the monitor around the F choice.
- **Item 11.** X4B-b also depends on X4a's monitor and `FinalGate` creation.
- **Forbidden substitutes** are updated to match.

## Decide

Does RF-1 close? Does the single first `read` now satisfy X4 item 2 and X4T item 9? Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
