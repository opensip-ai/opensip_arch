Grok review: law X7 r3, finalization. It answers your X7 r2 RF-1 (the rollover's ledger). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-finalization-x7-r3. Law review; no product cargo.

Subject: docs/implementation/m2/finalization-x7/PROPOSAL.md r3 (pin in hashes.txt). r2 bytes are preserved in PROPOSAL-r2.md (pinned too). Your r2 review is under /tmp/opensip-implementation/reviews/grok-finalization-x7-r2.

What changed:
- **Item 7.** The rollover's work is attempt work and is charged before it runs to the attempt ledger this invocation already opened (X1 item 5, X3d item 8, X3b item 9). That covers its carrier reads, the `TERMINAL` append, the g+1 publication and the end step's floor write. Every post-effect confirmation is reserved there first.
  - The gate ledger stays the gate's own work.
  - No second ledger and no fresh admission are created.
  - An exhausted attempt ledger at the rollover is a rollover failure on the budget row and never rewrites the attempt's outcome.
- **Item 10.** The rollover integration test expects these attempt-ledger charges and a gate ledger left unchanged by the rollover.

Nothing else changed.

## Decide

Does RF-1 close? Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
