CODEX2 review: M3-Q0, **r5**, a one-finding round. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r5. Read-only; do not commit.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md` (r5), 111807 bytes, sha256 `d922f5bdea4a640b1f2723900da8bdadd6e4aa5c1c67acda3667bf467732637f`;
- the schema (r5), sha256 `3f79b9797be80fb06f7981344c6d2bc524a61d615dd451f99d6067316b701800`.

**Previous:** `docs/implementation/m3/harness/DESIGN-r4.md` (`f7afe275…`) and the r4 schema snapshot (`b6c7d8ae…`).

r5 resolves C2-Q0-R4-01 with QD-28: an exact (tgid, `/proc` field-22 start ticks) key, with no interval test and no clock conversion, and a new `host-join-unresolved` reason. It also withdraws r4's fork-timestamp attribution: a tgid reused within a run is now `unjoinable-identity`. See the r5 changes table.

## Decide

1. Is C2-Q0-R4-01 resolved?
2. Is the withdrawal of fork-timestamp attribution sound?
3. Did r5 introduce any error, or change anything beyond its table?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256": DESIGN.md's sha.
