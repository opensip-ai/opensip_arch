Grok re-review: law X4 r7 after your r6 finding. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-live-guards-x4-r7. Law review; no product cargo.

Subject: docs/implementation/m2/live-guards-x4/PROPOSAL.md r7 (pin in hashes.txt). `diff` it against PROPOSAL-r6.md.

## Change (RF-1)

The two admitted standings now have separate new-process rules:
- **`ExistingOnly`:** the repository-execution grant never admits a new process, on an existing `GRANT.*` detail.
- **`InstallGateRequiredForNewProcess`:** a new process is withheld on `GRANT.*` until `EV-INSTALL` is admitted, and granted after; the standing value itself does not change.

M2 writer effects stay allowed under both. Neither publishes the continuation row. The new-process grant is M5's.

## Decide

Is RF-1 closed? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
