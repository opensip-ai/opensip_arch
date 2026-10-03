CODEX2 review: M3-Q0, **r6**, a one-finding round. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r6. Read-only; do not commit.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md` (r6), 118963 bytes, sha256 `3a17a943d4139248ca9fc7a8b8893f04a452c71a6a0710d7bf954866262ec31d`;
- the schema (r6), sha256 `da73a4765c7841555d1d77512baeeb7c2000b442ef885daa0b902b93a005e2e3`.

**Previous:** `docs/implementation/m3/harness/DESIGN-r5.md` (`d922f5bd…`).

r6 resolves C2-Q0-R5-01 with QD-29, which uses three harness sentinels as queue-order fences:
- **census:** a /proc snapshot of live TGIDs and their start ticks;
- **launch;**
- **close:** the end of the attribution range is its taskstats record, and the window closes on its exit event.

Its rules:
- generations that could be ambiguous are `unjoinable-identity`;
- each terminal record maps to exactly one counted generation, otherwise the run is `incomplete`;
- taskstats has no start-time field in the same representation, so none is used.

r6 also takes your PID-namespace point (N01). See the r6 changes table.

## Decide

1. Is C2-Q0-R5-01 resolved, including your exact sequence?
2. Is the fence ordering argument sound?
3. Did r6 introduce any error, or change anything beyond its table?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256": DESIGN.md's sha.
