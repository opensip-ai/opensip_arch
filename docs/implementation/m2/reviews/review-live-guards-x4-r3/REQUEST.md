REVIEWER re-review: law X4 r3 after Grok's r2 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. Law review; no product cargo.

Subject: docs/implementation/m2/live-guards-x4/PROPOSAL.md r3 (pin in hashes.txt). `diff` it against PROPOSAL-r2.md. Earlier findings are in `reviews/codex-live-guards-x4-r1/` and `reviews/grok-live-guards-x4-r2/`.

## Changes

- **RF-1.** Both mixed-read attempts now run inside one `FreshnessMonitor::read` callback (lead decision):
  - It returns a coherent view if either attempt matches, and latches only when the view is still mixed or on a hard failure.
  - The clock bracket covers both attempts, and both charge one ledger.
  - Tests cover a lawful rename that is absorbed, and a mixed view that latches.
- **RF-2.** The stale-guard rows are split:
  - a receipt failure takes its 468c row;
  - a replaced file takes custody, `required-files-changed`;
  - a lost lock on an unchanged lease file takes S7's busy row (`LEDGER.BUSY_TIMEOUT`, `ledger-busy`, `PROJECT.BUSY`).
- **Alignment.** X3b r2's single fence hold and `JournalAppendLock`. The per-observation ledger is 2 × X4T's `TRUST_VIEW_COST`. References point to X2 r4 item 7a.

## Decide

Are RF-1 and RF-2 closed? Is the whole law sound? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.

Note: r3 also carries pre-review alignment with X4T r2: the monitor is created at X2 r5 item 7's lease-free point, not inside 7a, and the per-observation ledger is 2 × X4T r2's ceiling (128 objects, 2048 edges, 240 MiB).
