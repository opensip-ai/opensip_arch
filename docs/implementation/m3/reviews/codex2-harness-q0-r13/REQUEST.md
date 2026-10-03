CODEX2 review: M3-Q0, **r13**, a one-finding round. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r13. Read-only; do not commit.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md` (r13), 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`;
- the schema (r13), sha256 `71f682d125c956eaec7a0f015fc8a0203f78b15f4538935f7beab45a398a2eb6`.

**Previous:** `docs/implementation/m3/harness/DESIGN-r12.md` (`72e70548…`).

r13 replaces the if-and-only-if rule for `rootReapedElapsedNanos` with three rules:
1. a non-null value requires `settlement-unverified-platform`;
2. the value is required only when a root was created and reaped;
3. it is null with `run-failed` otherwise.

It adds 3 test cases and a calibration case.

## Decide

1. Is R12-01 resolved?
2. Does r13 change anything else?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256": DESIGN.md's sha.
