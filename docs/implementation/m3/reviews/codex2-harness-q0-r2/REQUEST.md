CODEX2 review: M3-Q0, the quality-harness design record, **r2**. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r2. The rules are as before: read-only, no product runs, do not commit.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md` (r2), 91319 bytes, sha256 `4225ca34728ba1494a087110c5b92664f7d3f1560dc5ce3dd70fa24cf91e63c4`;
- `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json` (r2), sha256 `df67c65128065c33867ad3317a1cf25f870a0b4670c06a8af4336ab00de9548f`.

**Previous:** `docs/implementation/m3/harness/DESIGN-r1.md` (`22df1afb…`) and the r1 schema snapshot (`4cdfbb60…`). Your r1 review is in `docs/implementation/m3/reviews/codex2-harness-q0-r1/`. r2's "r2 changes" table maps C2-Q0-R1-01 to 08 and the five non-blocking items.

**New open items r2 raises:**
- **OI-17:** a sharper sample-based census guard.
- **OI-18:** macOS descendant RSS recorded as `incomplete`.
- **OI-12:** the M3-PLAN K2 updates.

## Decide

1. Is each r1 finding resolved?
2. Did r2 introduce any new error? Check:
   - the water-filling allocation;
   - the two-sided census guard;
   - the Linux taskstats/cgroup mechanism;
   - the schema's rejection cases;
   - the K2 freeze schedule.
3. Is anything still wrong?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "r1FindingResolution";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256": DESIGN.md's sha.
