# Adoption receipt: X10-SUCCESSOR-GA-r2, the X10 r4 feature-list successor for profile-allocations (2026-10-31)

**Decision LD-COORD-X10-GA (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1, after R3
different-vendor review.** Authority: LD-Q-165-B and LD-COORD-GUARD-AMEND-B.

`X10-SUCCESSOR-GA-r2.md` (sha256 `15b8f638…`) is adopted as a successor to X10 r4 `PROPOSAL-r4.md:94` (parent
`33095e6c…` at arch `9b0eb222816d03eb1db9ee75b6c4eecbfa53ea2d`). opensip-host's exact `[features]` list becomes
`crash-matrix`, `operability-dev-sinks`, `harness-instrumentation` and `profile-allocations`. The new feature:
- forwards nothing;
- is never default;
- has no outside activation;
- is refused by `compile_error!` without debug assertions.

The security and storage lists are unchanged. The successor pins product code head H6
`d2729979f0ff264711620f74b42fce84fb36e34c`.

| Artifact | sha256 |
|---|---|
| **R3 review r2, `review/REVIEW-x10-law-note.md`** (`X10-LAW-NOTE: ACCEPT`) | `bb2775981ee30521ccf5bb9ef1a434240533e263ea68f082a8ffbc13abcf5536` |
| **r1 history, `REVIEW-x10-law-note` r1** (3 BLOCKING, closed by r2) | `3baa4187…` |

- **The reviewer:** codex-guard-amend-r3, gpt-6-astra/high, R3. It is a different vendor from the Claude author (w2C).
- **Binding:** by value at `docs/implementation/m2/read-cli-x10/successor-ga/`, together with both GA receipts, the GA
  review, the r2 review and this receipt, in the C2b binding stage-joint-r3. The lock commit is H7, pending.
- **Owner notification:** flagged as an owner-delegated law successor.
