GROK2 review: the M3 unit plan, **r5**. Focus: **fact validation and DAG validation**. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok2-m3-plan-r5`. The rules are as before:
- read-only: no repository edits, commits, pushes or delegation;
- no product builds, runs or tests. Reading product git objects is fine;
- never touch the real home, and never read the 413 fixture.

**Subject:** `docs/implementation/m3/M3-PLAN.md`, r5. Its sha256 and bytes are pinned in `hashes.txt`.

**Previous:** `docs/implementation/m3/M3-PLAN-r4.md` (43,947 bytes, `e50f75d3…`), the accepted r4 bytes. You accepted r3 (`reviews/grok2-m3-plan-r3`), and CODEX2 accepted r4 (`reviews/codex2-m3-plan-r4`).

**Product:** `/Users/sb/code/opensip-ai/opensip`, main `3e64266`.

**Other assignment.** You also hold `reviews/grok2-m2-complete-r1`, which the lead will order. One r5 finding touches that record: M2C §4.1 (L11) and §5 rows 10–11 say no M3 row names the resume/repair writer or the X3c successor. r4's M3-J row (`M3-PLAN-r4.md:168`) did name both, but gave neither a law, an author nor a code unit. r5 row 8 says so.

## What r5 changes

r5 folds in the overnight records (`docs/implementation/OVERNIGHT-2026-10-03.md`). Its "r5 changes" table maps each of its 17 changes to a source. In brief:
- **Accepted records:** M3-T2, M3-Q0 r13 (K2 at 16 days, per-lane freezes), M3-I1 r2 (I1 resized to L and split) and M3-B r2 (nine code and harness units, two design units, discovery caps).
- **Drafts in review:** M3-C r3 (C1–C3 split in three, the C4 split, the narrowed F1/G1a edges, the X12 r4 and SX-1 gates) and M3-E1 r1 (E0, E2a–c, E3).
- **The M3-L draft's** gate status and findings.
- **The M2 completion draft's** carry-ins, with owners assigned as lead decisions P5-1 to P5-8.
- **A recomputed critical path:** 33 days under variant B, from M3-C r3's b + 23 with b = 10 taken from M3-B's unit table.
- **Citation re-pins:** every AQP line to the live r6 file; EXIT lines after 61 moved by +2; X12 cited at its r3 snapshot; `package.json` lines after L1.

## Decide

1. **Facts.** Check each row of the "r5 changes" table against its cited source. Check also:
   - every AQP and EXIT line citation in the r5 body. The r4, r3 and r2 history tables keep their reviewed r4-era lines, and say so;
   - the X12 r3 snapshot lines;
   - the product citations at `3e64266`, especially `providers/typescript/package.json:8`, `:13`;
   - the M3-L gate table against ML's gate and the review statuses;
   - the M2 carry-in table against M2C §3.3 and §5 rows 2, 10, 11 and 13–16, and against the overnight log's "X4-F1 written" entry;
   - the unit rows for B, C, E and I1 against MB:843-851, MC "Units", ME item 20 and MIU:28-40.
2. **The DAG.** Recompute every finish day in "r5 timing" from the stated durations and integration edges. Confirm or refute each of the following:
   - **b = 10.** B2-b waits for B2-a, B1-b and B3-a (MB:847). MB F14's "about day 8" (MB:805) omits the B1-b edge.
   - **The host chain:** B1-a → B1-b → B2-b → B2-c → C1a → C3a → C3b → C4a → H → J2 → J3 → M3-M → M3-X = 33, with the zero-slack X12d lead-set branch reaching J2 on day 22. Variant A gives 34.
   - **The conditions:** K2 by 28, O2_selected by 31 (compared at arrival at M3-X), and X12d's lead set by 22.
   - **The K2a slip rule:** M3-X = 33 + max(0, *s* − 10).
   - **The branch slack list.**
   - **The full-edge alternative:** F1/G1a at 16, G3 at 21 and G4 at 24, with no change to 33.
   - **The rejected J3 → J4 alternative** at 34.
   - **The I1 and F8b bounds:** I1-c by 16 and I1-b2 by 19, so F8b by 10 or 12.
   - **The C-law acceptance tolerance:** C2a starting by day 5, SX-1 by day 2.

   State any edge you think is wrong, or missing from a source law.
3. **Owner assignments.** Are P5-1 (J-RW and J4, with J4 decoupled from J3) and P5-2 (X3c r8 and X3c-3 before J3) coherent with EXIT:171, EXIT:186-191, X9 L11 and the owning M2 laws (X2 item 8, X3c item 10, X4T)? Are P5-3 to P5-8 sound? Each names its rejected alternative.
4. **Rules kept.** Is "the whole-M3 total is left uncomputed" still correctly applied? Is K2 correctly removed from the unbounded list, and is the "Unsized" list complete?
5. **Anything else wrong?**

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256";
- "dagCheck": your finish day for each sub-unit in "r5 timing", and the host-chain figure;
- "citationCheck": the citations you checked, with pass or fail.
