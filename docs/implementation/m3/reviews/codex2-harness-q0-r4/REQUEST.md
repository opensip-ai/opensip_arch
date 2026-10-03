CODEX2 review: M3-Q0, **r4**, a two-finding round. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r4. The rules are as before: read-only, do not commit.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md` (r4), 107617 bytes, sha256 `f7afe2755e21c0f11dfb2fb071d4d8a89d293a1932b1590c1ad385df0fa9adec`;
- the schema (r4), sha256 `b6c7d8ae34eb0ac4759a3b9ec330cc6b914c69aee2534932d95c08c9c3fb3006`.

**Previous:** `docs/implementation/m3/harness/DESIGN-r3.md` (`b69c918f…`) and the r3 schema snapshot (`f38b3f20…`). r4 changes:
- C2-Q0-R3-01: `slotReasons[]`, keyed by typed run slot, covering warmups;
- C2-Q0-R3-02: per-quantity nulling, QD-27;
- your two non-blocking items;
- the r4 changes table.

The test cases are listed in §9.5.

## Decide

1. Are both r3 findings resolved?
2. Did r4 introduce any error?
3. Does r4 change anything beyond its table?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256": DESIGN.md's sha.
