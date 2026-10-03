CODEX2 review: M3-Q0, **r9**. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r9. Read-only; do not commit.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md` (r9), 120794 bytes, sha256 `4db107c03d9d65b4c62cc113baf15335810228d3d6328bae961d809ca3d5924b`;
- the schema (r9), sha256 `00f6d032c24c886341f27c4bb2befe6104f76daa0ca462c34c8175edb2c47d36`.

**Previous:** `docs/implementation/m3/harness/DESIGN-r8.md` (`c958fdab…`), whose review is in `docs/implementation/m3/reviews/codex2-harness-q0-r8/`.

r9 follows the lead decision in the quality plan r5 (§5.1, now under separate review by you and GROK2). Per-process RSS attribution is withdrawn, and Linux peak memory is the per-run cgroup v2 leaf's `memory.peak` (QD-32). The details:
- a fresh leaf for every run;
- `nsdelegate` plus a cgroup namespace to prevent escape;
- six typed incomplete reasons;
- `wait4` `ru_maxrss` kept as information only.

Your R8-01 to 04 are moot. R8-05 is moot because elapsed time and memory now come from the same runs.

## Decide

1. Is the cgroup method sound and complete? Check:
   - fresh leaf creation, and entry before exec;
   - drain and `populated`;
   - the escape prevention: does `nsdelegate` with a namespace actually stop a same-UID process migrating out?
   - the launcher's capability use and drop;
   - the page-cache disclosure.
2. Are your r8 findings correctly moot?
3. Did r9 introduce any error? Check the schema, nulling, validator, and the remapped citations.

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256": DESIGN.md's sha.
