Grok review: law X5 r1, the replay-to-commit join (host/src/fact_admission.rs). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-replay-join-x5-r1. Law review; no product cargo. Product HEAD is 7e676a9.

Subject: docs/implementation/m2/replay-join-x5/PROPOSAL.md r1 (pin in hashes.txt).

Context:
- the accepted laws X3d r3 (its X5, X6 and X7 boundaries), X3b r6, X3c r7, X4 r7, X4T r6 and X2 r5;
- the build plan's M2 items and F-cases;
- `architecture/commit-recovery-readonly.v3.md`;
- identity-and-evidence, "Read-only recovery selectors";
- owner.md §5;
- product `evaluator` (`ReplayedRun`), `storage/recovery.rs`, `ledger_store` and lifecycle `replay.rs`.

## Decide

Does every numbered decision match the design sources and the accepted laws? Are the lead decisions, each with its rejected alternative, sound? Are the rows right against S12? Is the failure-case coverage right? Are the units and dependencies right? Is anything wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.

Also check X5's claim that EXIT-PLAN's G24 mapping was wrong (DR-G24 is the policy-pack gate), and that X5 prepares only F01.
