CODEX2 review: M3-Q0, **r12**, a one-finding round. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r12. Read-only; do not commit.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md` (r12), 148609 bytes, sha256 `72e70548b78843699bde2176231b909af6b549e7b30921b687bb1d6b463f2c36`;
- the schema (r12), sha256 `d05472ec700d8e8282b220f3d0d0b9530d00eafbe8f981eeeebf4c801a75d961`.

**Previous:** `docs/implementation/m3/harness/DESIGN-r11.md` (`c003a06a…`).

r12 resolves C2-Q0-R11-01 with QD-35:
- macOS settlement is not claimed; every macOS slot carries `settlement-unverified-platform`, so the row is `incomplete`;
- `elapsedNanos` is nulled, and the root-reaped time goes in a separate informational `rootReapedElapsedNanos`, never a budget input;
- Q6 qualification is declared Linux-only, on D12;
- OI-20 is new.

Your N01 calibration headings are fixed too.

## Decide

1. Is R11-01 resolved?
2. Did r12 introduce any error, or change anything beyond its table?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256": DESIGN.md's sha.
