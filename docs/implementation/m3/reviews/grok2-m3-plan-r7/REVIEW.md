# GROK2 review: M3 unit plan r7

**Verdict: REQUIRED-FINDINGS.**

Subject: `docs/implementation/m3/M3-PLAN.md`, r7, 148,956 bytes, sha256 `4ff335ec09b3f15a044912a15224f5552ba30d57bfa8f2a456d4f9b749bad11d`. That matches the request pin. Diff base: `M3-PLAN-r6.md`, 77,955 bytes, sha256 `a6956e88c94f1e47c5ccdfbc6e6a97bbf5a020f0df3fe68d80ae3d4f802dea55`. Record cut-off: the overnight log at arch `249d74ab4`, 42,242 bytes, sha256 `4a7926856b41880ffe6c002dad09ee7c23e37fb8e65d974bd6103f0ba3c84bb7`, 315 lines, last entry "M3-H r3 written". Product main is `cd5958b3608f44a0035566c9d4500e5005c62e91`. No product build, run, or test was used. `~/Library/Application Support/OpenSIP` was absent. The private 413 fixture was not read.

Two sentences are stale against the record's own routing and against the pinned log. The schedule, the lead decisions P7-1 through P7-5, the status vocabulary, and the kept scheduling rules hold.

## Required findings

### RF-1. Two sentences still give the X-H3 widening to CRC-1

`M3-PLAN.md:373` and `M3-PLAN.md:791`.

The day-0 assumption says "the X-H3 widening of C and CRC-1". The Unsized list says "the X-H3 C revision with CRC-1".

The rest of this revision routes that widening to M3-C r8 and CRC-2:

- the new-units row (line 293) titles it "The X-H3 widening: M3-C r8 and CRC-2" and says CRC-1 carries only C's existing law;
- the unbounded-round list (line 498) lists "the X-H3 widening (M3-C r8 and CRC-2)" separately from "CRC-1 and CR-1 (in review)";
- the reversible-decision row (line 691) says X-H3 goes to M3-C r8 and CRC-2, and CRC-1 carries C's law;
- the record-drift bullet (line 822) says MH r1 and r2 still name the successor "C r7 / CRC-1", and that the lead renamed it "M3-C r8 / CRC-2".

Line 384 keeps CRC-1 and CR-1 as the day-5 gate for C2a. That is the existing-law reading and stays. The pinned log's last entry already records the rename to "M3-C r8 / CRC-2". CRC-1 remains in review at this cut-off; this finding is the name of the widening, and it does not record a verdict on CRC-1.

**Correction.** In both sentences, name the widening M3-C r8 and CRC-2. Leave CRC-1 as C's existing-law successor.

### RF-2. The Risks bullet still says X4-F1's confirmation lane is pending

`M3-PLAN.md:813`.

The bullet says the lane "is pending". The pinned log line 286 records the lane on product main `15c0779`: workspace 1749 passed, 0 failed, 3 ignored, in 554 s, after which P0 phase 2 started. The same passed result is in r7-changes row 11 (line 69), the X4-F1 carry-in (line 262), the run-set list (line 516), and the P5-8 status (line 765).

The reversible-decision row at line 687 says a lane on `15c0779` "follows" and cites the integration entry. That entry's pinned text (log line 260) is "runs after E0 frees the machine." The row records the decision as made at integration. The result is the later log entry. The stale status is the Risks bullet.

**Correction.** In the Risks bullet, record the lane as passed: 1749 passed and 0 failed, on `15c0779`.

## Non-blocking observation

### NBO-1. Two locally defined uses of the token G10

The units-table gates column says "G10, G21" on M3-L, M3-F and M3-G (lines 236, 243, 244) and "G10 (control)" on M3-D (line 240). Line 140 names that token DR-G10, one of the seven gates to be prepared. Those cells match the accepted r6 plan. The new acceptance-gate item G10, at line 571, is "FA-2 accepted". P7-2 and line 838 say that item is a lead gate on M3-L's own row and changes no owner-set gate or threshold. Both uses are defined where they appear. A reader of the units-table cell can still take the new item for DR-G10.

## What held

**Facts.** Status cells keep the vocabulary this revision defines: accepted, accepted in review (M3-C r6 and r7), accepted and bound (the six design units), integrated (X4-F1), accepted as a record (the E0 report), and in review (M3-L r3, FA-2, M3-H with r3 written and queued, J-RW, CRC-1, CR-1). Nothing in that in-review list is recorded as accepted. Later returns after the pinned log are outside this record. M3-H stays "written and queued".

The five corrections the lead made in the live log after drafting are already the facts r7 states, judged here against the confinement record, the harness design, the B-S1 review, and the I1 unit table. B1's detailed rows state kernel 6.1.147 and the five F-3 amendments, and B1 blocks M3-L taking effect. B2 cites HD §5.6 and §5.8, with the accepted floor 0.99 and k_min 299. I1-a depends on I1-L and X9-6. B-S1 ruling R2 is item 24 row 3 read as the review states it: item 22 and item 24 row 1 govern an explicit or config member.

`git diff --stat 3e64266 cd5958b` is 20 files, +688/−62: `design-lock.json`, `schemas/registry.json`, `apps/report/src/generated/report.ts`, files under `tools/`, and X4-F1's custody and trust files under `crates/security/src/` with their tests. That is the set line 192 names, and none of those paths is a cited row in the product-state table. `design-lock.json` at `cd5958b` has 82 contract successors. `tools/verify_design.py` is unchanged between `3e64266` and `cd5958b` (40,714 bytes, sha256 `c13d231eb755a08a33fae674426861145758c5ec136ba2cd6dd4b0f1020f8f08`).

MB re-pins resolve in `config-discovery-b/PROPOSAL-r2.md`: the profile bullet at MB:336, F14 at MB:803, the B1-a row at MB:841, B2-b's edges at MB:845, and the unit rows at MB:839–849. The carried r3–r6 change sections match r6 except the one citation note this history already states: the r5 table's MB lines are the live file's, +2 against `PROPOSAL-r2.md`. ML1:180–188 and ML1:453–455 match the r6 citations. G7's "11 provider-boundary needs map to 11 registered events" matches ML2 item 14.

**The DAG.** Recomputed finish days match the r7 timing table. The host chain is 2+2+3+3+2+3+1+3+3+3+3+3+2 = 33: B1-a, B1-b, B2-b (b = 10 from MB:845), B2-c, C1a, C3a, C3b, C4a, H, J2b, J3d, M3-M, M3-X. M3-X = max(31, 22, 27, O2_selected) + 2, which is 33 while O2_selected is at most 31. D's eight sub-units match MD "Units after the law": D3 finishes day 10, so F1 and G1a (day 12) have two days of slack; D5 is day 13; D1b's primitive is day 5; G2-v is day 6; O3 is day 16. E2s finishes by day 12 and E3 stays on day 14 (ME item 20). J2b is day 25, J3d day 28, J2c day 27, and the lead sets fall on days 3, 4, 5 and 9 (MJ item 14). H1–H4 finish by day 9 against D2b's day 5, inside the proposal's own slack, and H5 stays the host-chain unit. No accepted-law edge moves a finish day.

**Lead decisions.** P7-1 through P7-5 each name a rejected alternative. P7-1 defines day 0 as M3-L in effect: accepted in review, G1 through G10 met, and every delta round accepted. P7-2 adds G10 (FA-2) to M3-L's own gate table and changes no owner-set gate or threshold; ML3 says G10 is this law's addition to the plan's row. P7-3 follows MJ item 14: J2c is the ephemeral path, finishes day 27, and joins M3-X, while J3d depends on J2b. P7-4 matches ME item 20 (E2s regenerates the eight-output registry). The annotations to P5-1 (X3b and the registry owner, from J-RW r2), P5-3 (E2s), P5-4 (X4-F1 integrated, X4-F2 remaining) and P5-8 (the first three run sets and the confirmation lane done, S-M next) match their sources. P7-5 keeps H1–H5 and J4a–J4e as proposals and does not re-time the DAG. J4a–J4e sizes are M+M+S+S plus the lead set, matching J-RW item 11.

**Rules kept.** "The whole-M3 total is left uncomputed" still applies (lines 496–503): O7's date, the pre-day-0 rounds, the machine queue, the O2 parts, and S-R. K2 stays off that list because Q0 bounds it. Line 498 lists the widening as M3-C r8 and CRC-2 and lists CRC-1 and CR-1 separately, in review. The effort sentences count as written: 39 + 21 + 9 + 3 = 72 on the law, successor and record side, and 76 + 3 + 1 + 4 + 4 = 92 on the code, harness and probe side. J1 r4 and C r7 are further review rounds of laws already inside the 39, which the list says. CRC-1 sits inside the 39 as the existing-law successor; CRC-2 sits inside the 9.
