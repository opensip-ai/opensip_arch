# GROK2 review: M3 unit plan r8

**Verdict: REQUIRED-FINDINGS.**

Subject: `docs/implementation/m3/M3-PLAN.md`, r8, 149,857 bytes, sha256 `30af01c798e3bd661c87b9ab3ddcc20e5b01a7719c990c704638ba4d9ce62a3c`. That matches `hashes.txt`. Base: `M3-PLAN-r7.md`, 148,956 bytes, sha256 `4ff335ec09b3f15a044912a15224f5552ba30d57bfa8f2a456d4f9b749bad11d`. The diff is the draft banner, the new "r8 changes" section, and three sentences. No product build, run, or test was used. `~/Library/Application Support/OpenSIP` was absent. The private 413 fixture was not read.

r7 RF-1's renaming and r7 RF-2 are resolved. The RF-1 sentence also records an acceptance this revision still denies, and the NBO-1 row cites the wrong line and an eleventh gate item.

## Required findings

### RF-1. The widening sentence now says MH r3 is accepted

`M3-PLAN.md:383`.

The day-0 assumption now names "the X-H3 widening of C (M3-C r8) and CRC-2". The Unsized list (line 801) names "the X-H3 C revision (M3-C r8) with CRC-2". CRC-1 stays the day-5 successor for C's existing law (line 394). Those are the r7 finding.

The same edit changes the citation from "in review" to "MH r3 accepted". Three lines above, the same list still says "the H law (in review; r3 queued)" (line 380). The closing claim (line 846) says M3-H, with r3 queued, is in review and that nothing in it is recorded here as accepted. The short-name pin (line 39), r7-changes row 2 (line 70), the M3-H row (line 255), the reviewer table (line 550) and the in-review list (line 564) say the same. The r8 changes row describes the renaming only. The pinned r3 bytes (`fact-admission-h/PROPOSAL-r3.md`) open "Draft r3, not accepted."

**Correction.** Keep the widening name M3-C r8 and CRC-2. Cite MH item 25 without recording MH r3 as accepted.

### RF-2. The NBO-1 row cites line 140 and an eleventh gate item

`M3-PLAN.md:61`.

Leaving the units-table cells unchanged, and routing a rename of M3-L's own gate items to M3-L's next revision, is the right disposition of r7 NBO-1. The row's two details do not match this file.

It says the units-table token G10 means the DR-G10 gate at line 140. Line 140 is the heading "What M3 exit means". The sentence that names DR-G10 is line 150. That sentence is line 140 of `M3-PLAN-r7.md`; the r8 section inserted above it moved it by ten lines.

It says the rename is L-G1 through L-G11. This plan's gate table is G1 through G10 (lines 572–581), and day 0 is "every gate item G1 to G10" (line 376). This record has no eleventh M3-L gate item.

**Correction.** Cite line 150. State the rename as L-G1 through L-G10.

## What held

**r7 RF-2.** The Risks bullet (line 823) records the confirmation lane as passed, 1749/0/3 on `15c0779`. The carry-in (line 272), the run-set list (line 526) and the gate row G1 (line 572) already said that lane passed. No sentence still calls it pending.

**The rest of the diff.** The banner is r8. The r8 changes section is the only added block. The widening row (line 303), the X-H3 route (line 341), the unbounded-round list (line 508) and the reversible-decision row (line 701) already named M3-C r8 and CRC-2, and they are unchanged. The units-table gates column is unchanged: "G10, G21" on M3-L, M3-F and M3-G, and "G10 (control)" on M3-D.
