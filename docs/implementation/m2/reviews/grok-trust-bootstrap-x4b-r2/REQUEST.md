Grok review: law X4B r2, first trust acceptance. It answers your X4B r1 RF-1 (where acceptance runs) and RF-2 (the role_machine::decide event sequence). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-trust-bootstrap-x4b-r2. Law review; no product cargo. Product HEAD is fc7dce7.

Subject: docs/implementation/m2/trust-bootstrap-x4b/PROPOSAL.md r2 (pin in hashes.txt). r1 bytes are preserved in PROPOSAL-r1.md (pinned too). Your r1 review is under /tmp/opensip-implementation/reviews/grok-trust-bootstrap-x4b-r1.

What changed:
- **Item 1 (RF-1).** Acceptance runs at X4T item 9's fenced first read:
  - X1's fence is already returned;
  - X3a's `trust/stores/S` and `state.v1` are retained;
  - R is fixed;
  - no lease is held.

  It runs only when that read returns F absent. The fenced admission then runs once more on the confirmed retained `state.v1`, before any lease, and the `FreshnessMonitor` is created just before that run. A second F absent is the host invariant row. X2e only receives the view.
- **Item 11.** X4B-b depends on X4B-a, X1's fence, X3a's retained store and X4T-b's fenced read, not on X2e.
- **Item 4 (RF-2).** The sequence from `Unbootstrapped` is:
  1. `PresentOrdinary` (admissible only, which stores `Trusted`);
  2. `Clock { expired, stale_revocation }` when either is true, which stores `Expired` or `StaleRevocation`;
  3. `Revoke { newer_and_byte_valid: true }` when the payload's revocation revokes the role, which stores `Revoked`.

  Every accepted event is recorded with its role change and publication event, and no no-op events are dispatched. `accepted.by` names the `EV-PRESENT-PAYLOAD` event, and `conditionEvidence.revokedBy` names the `EV-REVOKE`, as X4T-0's fixture does. A fresh, unrevoked document stays a single `PresentOrdinary`.
- **Items 9 and 10.** X4T-0 keeps only `QuorumLost` and `Recovery` as test-only states, and the tests expect the stored states of item 4's sequences.

Context: the accepted laws X1 r1, X2 r6, X3a r5, X4 r7 and X4T r7; `crates/security/src/trust/role_machine.rs` and `accepted_store_fixture.rs` at fc7dce7; S4 step 2, S5, S6 and S7; laws 463 and 467.

## Decide

Do RF-1 and RF-2 close? Does item 4's sequence match `decide` at fc7dce7, and is the record chain one that X4T-a's loaders accept? Is the single re-admission correctly placed before any lease? Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
