CODEX2 review: M3-Q0, the quality-harness design record, **r3**. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r3. The rules are as before: read-only, no product runs, do not commit.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md` (r3), 101902 bytes, sha256 `b69c918f5fa5976285970dcda015cd98e3f04da706bf4c62d89a3c5900d73a04`;
- the schema (r3), sha256 `f38b3f2046172b4365179694fe625a7936e107b95c937f341606c404de7fd96b`.

**Previous:** `docs/implementation/m3/harness/DESIGN-r2.md` (`4225ca34…`) and the r2 schema snapshot (`df67c651…`). Your r2 review is in `docs/implementation/m3/reviews/codex2-harness-q0-r2/`. r3's changes table maps C2-Q0-R2-01 to 03 and your four non-blocking items.

## Decide

1. Is each of the three r2 findings resolved?
2. Did r3 introduce any new error? Check:
   - the positive completeness proof for Linux RSS;
   - the `batchId` join and `batchObservations[]`;
   - the slip rule M3-X = 26 + max(0, s − 3).
3. Does r3 change anything beyond its table?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "r2FindingResolution";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256": DESIGN.md's sha.
