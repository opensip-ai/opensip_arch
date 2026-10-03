GROK2 review: the M3 unit plan, r1, **fact validation**: every design and code claim, citation and module-state statement. Claude Opus 5.5 leads. Another reviewer covers the other half in parallel. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-m3-plan-r1.

**Rules:**
- Read-only. No commits, no product builds or test runs; crash-matrix runs are active.
- Never touch the real home.
- Never read the 413 fixture.

**Subject:** `docs/implementation/m3/M3-PLAN.md`, 28398 bytes, sha256 `65bf6ac57a663707a2eea47fba7e293c595daa3ac9e703b1e4ed511d38496830`. It is a planning record, the M3 counterpart of `docs/implementation/m2/EXIT-PLAN.md`. It builds on:
- the accepted M3 analysis-quality plan (`docs/implementation/m3/analysis-quality/PLAN.md` r4);
- the operability plan (`docs/implementation/m3/operability/PLAN.md` r2, in review);
- the build plan's M3 row (`docs/v2/architecture/implementation-boundaries-and-build-plan.md:887`) and qualification routing;
- `implementation-coverage.v1.json`;
- the product contracts in `docs/v2/contracts/product-v1/`.

Product: `/Users/sb/code/opensip-ai/opensip`, main `eb0d503`.

**Context:** the owner uses Rust, TypeScript and Python on AL2023, and wants excellence over speed. Up to four reviewers (Grok, Codex, GROK2, CODEX2) can run in parallel. Lead run sets are serialized.

## Decide

1. **For your focus:** is the plan correct and complete? Does it cover everything M3 must deliver: the build-plan completion criteria, the gates routed to M3, the quality plan's M3 obligations, and the operability M3 items?
2. **The surprises the drafter found.** Check each one:
   - missing owner modules;
   - stub providers and the missing `rustc-dev` component;
   - an empty pack registry;
   - real Rust dependencies needing an M5 import command;
   - D15 clashing with M2's Git layout rule;
   - the stale DR-G10 row;
   - DR-G14's owner module landing at M5.
3. **M2 carry-ins and choices left open:** are the lead recommendations sound?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings": each with id, location, problem or claim, evidence and fix;
- "nonBlockingObservations";
- "subjectSha256".

Do not commit.
