Grok re-review: law X4 r6 after your r5 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-live-guards-x4-r6. Law review; no product cargo.

Subject: docs/implementation/m2/live-guards-x4/PROPOSAL.md r6 (pin in hashes.txt). `diff` it against PROPOSAL-r5.md.

## Changes

- **RF-1.** Item 5 step 2 captures in X4T r5 item 2's order, through its loaders, each file through its collection's retained handle:
  - publications and events: `capture_p2`, `bind` and `bind_trace`; `clock.record` stays inline;
  - objects: `bind_retained_head`;
  - objects and records: X4T-a's `Budget::load`;
  - then X4T-a's `accepted.by` check.
- **RF-2.** `ExistingOnly` and `InstallGateRequiredForNewProcess` are admitted standings (Continue). Every M2 writer effect continues admitted work, so both allow it, and the continuation row is never published for them. Starting a new process (M5) is withheld through `GRANT.*`. `Continuation::Refuse` stays X4T's admission row.

## Decide

Are RF-1 and RF-2 closed? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
