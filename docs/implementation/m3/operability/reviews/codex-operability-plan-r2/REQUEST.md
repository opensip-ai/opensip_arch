Codex review: the M3 operability plan, **r2**. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-operability-plan-r2. The rules are as in r1: read-only, no product runs, never touch the real home, never read the 413 fixture, do not commit.

**Subject:** `docs/implementation/m3/operability/PLAN.md`, 54138 bytes, sha256 `a65ea9c7ff8da4315d9649d0fd79cfb81bfc773fe36dd2244e40d9e3d5ac814b`. **Previous:** `docs/implementation/m3/operability/PLAN-r1.md` (`f2005ed0…`), your r1 subject. Your r1 review is in `docs/implementation/m3/operability/reviews/codex-operability-plan-r1/`. r2's response table maps OP-R1-01 to OP-R1-10, and the non-blocking items, to their fixes.

**Two lead judgment calls to examine:**
- **O9:** whether to allow a restricted, consented capture of raw provider stderr. The recommendation is not at M3.
- **Cancellation:** a second signal inside the commit critical section waits for the commit's outcome, bounded by the commit's own budget, rather than force-exiting.

## Decide

1. Is each r1 finding resolved? Answer per ID.
2. Did r2 introduce any new error? Check the new citations (REG, APP, DRC §8, DC4, QG, CC, PCS, CINV, the command envelope, `bootstrap.rs`, `commit.rs:465`) and the outcome matrix in §5.2.
3. Is anything still missing?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "r1FindingResolution";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256".
