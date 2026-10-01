REVIEWER re-review: law X4T r3 after Grok's r2 finding. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. Law review; no product cargo.

Subject: docs/implementation/m2/trust-admission-x4t/PROPOSAL.md r3 (pin in hashes.txt). `diff` it against PROPOSAL-r2.md.

## Change (RF-1)

A recorded root chain beyond `ChainBudget{16 links, 16 MiB}` now takes the existing budget row: `WORK.BUDGET_EXHAUSTED`, operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`. The chain is never truncated. Item 10's budget line names this case.

## Decide

Is RF-1 closed? Is the whole law sound? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
