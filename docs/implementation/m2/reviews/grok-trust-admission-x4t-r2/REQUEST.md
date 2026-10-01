Grok re-review: law X4T r2 after Grok's r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-trust-admission-x4t-r2. Law review; no product cargo. Product HEAD is f7acb6d.

Subject: docs/implementation/m2/trust-admission-x4t/PROPOSAL.md r2 (pin in hashes.txt). `diff` it against PROPOSAL-r1.md. The r1 findings are in `reviews/grok-trust-admission-x4t-r1/`.

## Changes

- **RF-1.** The fenced admission, its write-ahead and the monitor's creation run at X2 r5 item 7's lease-free point, under the fence and before any lease. 7a only moves them.
- **RF-2.** While fenced, only the confirmed publication advances the retained `state.v1`. After release the capture is provenance, and a newer pointer is admitted, with S6 deciding what it means. A rollback is `trust-rollback` at the handoff and `OBSERVER.FAIL_STOP` on a reread.
- **RF-3.** X4T's unfenced reread is one attempt. X4 r3's single callback owns the only retry, and every reread error goes to X4 as `OBSERVER.FAIL_STOP`.
- **RF-4.** "F absent" alone is `TRUST.NO_ADMITTED_TIME_CONTEXT`. The view runs `role_machine::continuation`, and a refusal publishes the continuation row with a role-and-state subject. `ExistingOnly` and `InstallGateRequiredForNewProcess` are admitted and carried for X4. Clock-expired roles never produce `ROOT.*` rows.
- **RF-5.** The closure is 11 files plus a chain with `ChainBudget{16 links, 16 MiB}`. `TRUST_VIEW_COST` is at most 64 objects, 1024 edges and 120 MiB, and X4T-a pins a measurement of a view with every file at its cap.
- **RF-6.** `permissionPolicyDigest` = `Effective::digest()` (domain `opensip.metadata.policy-effective.1`).
- **Lead decision (new section).** Add `CONTINUE-INDEX-NOT-TRUSTED` and `CONTINUE-COMPONENT-NOT-TRUSTED` in a contract successor, X4T-c, like 468a. Until then they are published under `CONTINUE-CORE-NOT-TRUSTED` with a role subject.

## Decide

Are RF-1 to RF-6 closed? Is the new-codes lead decision sound, including the row class? Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
