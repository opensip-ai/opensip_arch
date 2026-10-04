GROK2 review: the M3 unit plan, **r7**, a record revision. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**, on **factual accuracy and consistency**.

Write only under `/tmp/opensip-implementation/reviews/grok2-m3-plan-r7`. The rules are as before:

(Lead note: the overnight log is a living file. r7 cites it as committed at arch `249d74ab4`; read it with `git show 249d74ab4:docs/implementation/OVERNIGHT-2026-10-03.md`. After r7 was drafted, the lead corrected five log lines that r7's drafter flagged: B1's AL2023 kernel 6.1.147 and its five F-3 amendments; B1 and B3 now block "M3-L taking effect"; B2's section and accepted floor (HD §5.6, 0.99 with k_min 299); I1-a not waiting for P0; and ruling R2's "item 24 row 3". r7 already states these facts correctly. Where the live log and r7 differ, that is why.)

- read-only: no repository edits, commits, pushes or delegation;
- no product builds, runs or tests. Reading product git objects is fine;
- never touch `~/Library/Application Support/OpenSIP`, and never read the private 413 UUID fixture.

**Subject:** `docs/implementation/m3/M3-PLAN.md`, r7, 148,956 bytes, sha256 `4ff335ec09b3f15a044912a15224f5552ba30d57bfa8f2a456d4f9b749bad11d`.

**Diff base:** `docs/implementation/m3/M3-PLAN-r6.md` (77,955 bytes, `a6956e88…`), the r6 bytes you accepted (`reviews/grok2-m3-plan-r6`). The live file's 2-line acceptance note is gone in r7. The r6, r5, r4 and r3 change tables are carried over verbatim.

**Product:** `/Users/sb/code/opensip-ai/opensip`, main `cd5958b`. The binding commits since r6's `3e64266` are `e093e90` (F8b), `0ceb9ad` (I1-L), `9c11c53` (B-S1), `240a795` (B-S2), `8adfe0c` (B-S9) and `cd5958b` (I1-P), with X4-F1's code at `15c0779`.

**Record cut-off.** r7 records the overnight log at sha256 `4a792685…` (315 lines, as committed at arch `249d74ab4`; last entry "M3-H r3 written"). The log is live and will grow. Judge r7 against those bytes (pinned in `hashes.txt`; `git show 249d74ab4:docs/implementation/OVERNIGHT-2026-10-03.md`), and treat anything the log records later as out of scope.

**Other assignment.** You also hold `reviews/grok2-crc-1-r1` (CRC-1). This record cites CRC-1 only as "in review"; the lead orders the two.

**Pins.** Every pin is in `hashes.txt`. Laws are pinned at their snapshots. Live drafts with no snapshot are pinned by sha256 and, where one exists, the arch commit that holds their bytes: M3-L r3 (`e35272519`) and M3-H r3 (`249d74ab4`). Some cited files were still untracked at drafting, and their sha256 is the reference: `resume-repair-jrw/PROPOSAL-r2.md` (the same bytes are at `9bccaa8fa`), FA-2's design record (`native-successors-fa/fa-2/README.md`), and CRC-1's and CR-1's records (`snapshot-plan-c/{crc-1,cr-1}/README.md`).

## What r7 changes

r7 is a record revision. Its "r7 changes" table maps each of its 18 changes to a source. In brief:
- **Status cells.** Tonight's accepted laws (S-OP-2 r6, M3-E1 r3, M3-J1 r3 and r4, M3-D r3, X3c r8, the M2 completion record r3), M3-C r6 and r7 accepted in review, six bound design units, X4-F1 integrated, the E0 report accepted, and what is still in review (M3-L r3, FA-2, M3-H, J-RW, CRC-1, CR-1).
- **M3-L.** The early-review rule as a lead decision; the refreshed gate (G2, G3 and G7 met; G4 and G5 under B3; G9 is O7, with CF-P's evidence; G1 not started); **day 0 means L in effect** (P7-1); r6's `:445` and `:426` rules superseded (L r2's X9); and **FA-2 as gate item G10** (P7-2).
- **Unit breakdowns from accepted laws:** D's eight sub-units, E's new E2s, and J1's J2a, J2b, J2c, J3a, J3b and J3d. H's H1 to H5 and J-RW's J4a to J4e are recorded as proposals and do not re-time the DAG (P7-5).
- **New units and successors:** FA-1, FA-2, the X-H3 widening (M3-C r8 and CRC-2), B-S9, SD-5 with S20, S19, X3d r9, X3c r9, the X9 r17 record, M3-B's record revision, E1's, I1's and D's record items, H3, the Rust3 limit successor, SYN-1F, SD-2 and SD-3, each with owner, dependencies and size where the source states one.
- **P5-1's owner list** gains X3b and the registry owner (J-RW, in review).
- **Critical path:** still 33 days. D3 moves to day 10, D5 to 13, D1b's primitive to 5, G2-v to 6 and O3 to 16; E2s is added; J2c finishes on day 27 and joins M3-X (P7-3); J3a's and J3b's lead sets fall on days 5 and 9.
- **Cross-law items** from L r2 and r3, H, J-RW, X3c r8, E1, J1, D, E0 and I1-L, in one routing table.
- **Owner blockers** B1 to B4 as they stand, and the night's reversible lead decisions by source.
- **Smaller:** the product-state generator rows (F8b), the O7 section's network denial (seccomp, per D's F8) and risk line (CF-P), E0's T-native outcome, P0's phase 1, and the Rust3 256-subject cap.

## Decide

1. **Facts.** Check each row of "r7 changes" against its cited source. Check also:
   - every status cell in the units table, the carry-in table and "New units and successors (r7)" against the overnight log (at the pinned bytes) and the review status files;
   - **that nothing still in review is recorded as accepted:** M3-L r3, FA-2, M3-H, J-RW, CRC-1, CR-1, and the in-review rows that cite them;
   - the owners, dependencies and sizes in "New units and successors (r7)", and that "not stated" is used only where the source states no size;
   - each route in "Cross-law items (r7)" against its source item (L r2 X9 to X12, L r3 X13 to X16, H X-H1 to X-H6, J-RW X-RW-1 to X-RW-12, X3c r8 CL-1 to CL-5, E1's M3P-E, J1's S17, S19 and S20, D's F7, F8, F9 and F13);
   - B1 to B4 against the log's "Blockers for the owner", and the reversible-decision table against the log entries it cites;
   - the re-pins: MB lines −2 against `PROPOSAL-r2.md` (for example MB:336, MB:803, MB:841, MB:845), r6's ML lines against ML1, and the snapshot shas in "Short names";
   - the product-state claim that no cited product file changed between `3e64266` and `cd5958b` (`git diff --stat`).
2. **The DAG.** Recompute every finish day in "r7 timing" from the stated durations and integration edges. Confirm or refute:
   - the D rows against MD's own timing (D's "Units after the law"), and D3's 2 days of slack against F1 and G1a;
   - G2-v on day 6, O3 on 16, E2s by day 12 at the latest, E3 still on 14;
   - J2b and J3d on 25 and 28, J2c on 27, and the lead sets on days 3, 4, 5 and 9;
   - the host chain B1-a → B1-b → B2-b → B2-c → C1a → C3a → C3b → C4a → H → J2b → J3d → M3-M → M3-X = 33, and M3-X = max(M3-M, R, 27, O2_selected) + 2;
   - the conditions (K2 by 28, O2_selected by 31, X12d's lead set by 22, J3d's waits, H r1's FA-2 and X-H3 timing) and the branch slack list.

   State any edge you think is wrong, or missing from an accepted law.
3. **Lead decisions.** Are P7-1 to P7-5 sound, and does each name its rejected alternative? In particular: does G10 (P7-2) stay a lead gate item on M3-L's own row, changing no owner-set gate or threshold? Is P7-3 (J2c into M3-X) a faithful reading of r6's J2 row? Are the r7 annotations to P5-1, P5-3, P5-4 and P5-8 accurate?
4. **Rules kept.** Is "the whole-M3 total is left uncomputed" still applied correctly? Are "Unsized" and the effort counts (about 72 law, successor or record units; about 92 code, harness or probe sub-units) consistent with the rows they count?
5. **Anything else wrong.**

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256".
