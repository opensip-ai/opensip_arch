CODEX2 review: the M3 unit plan, **r3**, with the same focus as before. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-m3-plan-r3. The rules are as before: read-only, no product builds or runs, never touch the real home, do not commit.

**Subject:** `docs/implementation/m3/M3-PLAN.md`, 43170 bytes, sha256 `7ef4f0d1147ce8311c49e375c83caf9b5d80895cd77b5e152b9c21799a019c2b`. **Previous:** `docs/implementation/m3/M3-PLAN-r2.md` (`add49e25…`), your r2 subject; your r2 review is in `docs/implementation/m3/reviews/codex2-m3-plan-r2/`. r3's "r3 changes" table maps all six r2 findings: GROK2 RF-1 to RF-4 and CODEX2 C2-M3-R2-01 and -02. The operability plan is now accepted at r3.

## Decide

1. Is each of your r2 findings resolved?
2. Did r3 introduce any error? Check:
   - the DAG edges (K1→M, CF-P→D, CF-1→D5, D1→provider launch);
   - the finish bounds;
   - the conditional 26-day host chain;
   - the M5-EX package;
   - the new citations.
3. Is anything else wrong?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "r2FindingResolution";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256".
