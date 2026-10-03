CODEX2 review: the M3 unit plan, **r2**, with the same focus as your r1 review. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-m3-plan-r2. The rules are as before: read-only, no product builds or runs, never touch the real home, never read the 413 fixture, do not commit.

**Subject:** `docs/implementation/m3/M3-PLAN.md`, 35300 bytes, sha256 `add49e2508816defdcc033a3720359fa8a639d8fcb94191950b91e8f5df8c841`. **Previous:** `docs/implementation/m3/M3-PLAN-r1.md` (`65bf6ac5…`), your r1 subject; your r1 review is in `docs/implementation/m3/reviews/codex2-m3-plan-r1/`. r2's "r2 changes and review responses" table maps all 11 required findings from both reviewers.

**Context.** O7 (hostile-input confinement) is an owner decision still pending. r2 records the lead's recommendation, makes O7 a hard prerequisite of M3-L and of provider launch, and adds M3-CF for the confinement successor. That successor is needed because accepted text says no confinement or sandbox is claimed (SL:1113, SL:497, AQ:344, NE:2554, REG:366; DR-128). The operability plan is now r3, in review.

## Decide

1. Is each of your r1 findings resolved? Answer per ID.
2. Did r2 introduce any new error? Check:
   - the new citations;
   - the recomputed critical path and the sub-unit table;
   - M3-CF's correctness against the cited law;
   - the M3-L acceptance gate.
3. Is anything still missing?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "r1FindingResolution";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256".
