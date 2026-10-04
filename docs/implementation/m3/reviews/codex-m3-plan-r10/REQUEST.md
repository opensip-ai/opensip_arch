Codex review: **M3-PLAN r10**, a record revision of the M3 unit plan. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**, on factual accuracy and consistency. Claude Opus 5.5 leads.

Write only under `/tmp/opensip-implementation/reviews/codex-m3-plan-r10`.

**Rules:**
- read-only: no repository edits, commits, pushes or delegation;
- no run: no product build, cargo command, test or measurement. Reading files and product git objects is fine;
- never touch `~/Library/Application Support/OpenSIP`, and never read the private 413 UUID fixture.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/M3-PLAN.md`, r10, 226,011 bytes, sha256 `ec8c38f8c6ac8d522989ea6226363817a1b77c5b37560e72e2520088601bb964`.
- **The diff base:** `docs/implementation/m3/M3-PLAN-r9.md` (150,586 bytes, `72bc7a13…`), the r9 bytes GROK2 accepted (`reviews/grok2-m3-plan-r9`). The live file's 2-line acceptance note is gone. The r9, r8, r7 and earlier change tables are carried over unchanged. r10 marks each changed cell **r10:** in place and lists its changes in "r10 changes".
- **Product:** `/Users/sb/code/opensip-ai/opensip`, main `d2c00a9`. Since r9's baseline `cd5958b` there are 17 commits: the bindings `392499e` (CRC-1), `f97c02b` (FA-1), `052d3cb` (SD-5), `8ca420f` (FA-2), `7347614` (RUST3-LIM), `5214350` (S18), `3fe7eb5` (CR-1), `682991f` (SYN-1), `218465f` (SYN-1F), `6190e66` (SYN-NS), `3f6f9a5` (S21) and `d2c00a9` (SD-7); and the code units `5e25d04` (P0), `4c761e8` (I1-a), `cca4fe4` (X3a-2), `988f6ed` (X4-F2) and `d761121` (VD2-a with F8c).

**The cut-off.** r10 records up to arch commit `17584e1f5`. That means the overnight log as committed there (sha256 `2fdf6752…`, 714 lines; last entry "J-RW's successors written and sent to CODEX2") and the review records committed there. r9 recorded at r7's cut-off: the log at `4a792685…` (315 lines, arch `249d74ab4`; last entry "M3-H r3 written"). So everything between the two is new in r10, not only the items the lead listed. Read both logs with `git show <commit>:docs/implementation/OVERNIGHT-2026-10-03.md`. Treat anything after `17584e1f5` as out of scope. The working tree holds untracked files from after the cut-off (J2a's and E2a's inventory candidates v137 and v138, and `reviews/grok2-e2a-r1`); r10 does not record them.

**Pins.** Laws are pinned at their accepted snapshots. Laws in review with no snapshot are pinned by sha256 and the arch commit that holds their bytes: J-RW's successors (X2 r10, X3c r9, X3b r11, X4T r13) at `17584e1f5`, and X9 r17's round 1 at `138a95b8d`. REG v3's subject manifest was untracked at the cut-off; its sha256 is the reference. Live `PROPOSAL.md` files are being amended in parallel. If a live file differs from its pin, read the pinned bytes with `git show <commit>:<path>`.

## What r10 changes

r10 is a record revision. It makes no new lead decision, and it re-times the DAG only where an accepted law moved a duration or an edge (P7-5). In brief:
- **Laws accepted since r9's cut-off:** M3-H r3; M3-L r5, accepted in review; M3-D r5; M3-J1 r5, M3-B r4, M3-E1 r4 and M3-I1 r3 (record revisions); VD2; X4T r12; X3d r9 (J1's S10), X7 r7 (S9) and X4 r8 (S11, with the new code unit X4-F3); J-RW r4; J1's S2 to S6.
- **Bound:** CRC-1, FA-1, SD-5, FA-2, RUST3-LIM, S18, CR-1, SYN-1, SYN-1F, SYN-NS, S21 and SD-7, the first contract passage supersession. **Integrated:** P0, I1-a, X3a-2, X4-F2, and VD2-a with F8c. **Started:** J2a and E2a, and X4-F3. **In review at the cut-off:** J-RW's successors with CODEX2, and X9 r17's round 1 with Grok.
- **M3-L's gate** is renamed L-G1 to L-G11, and L-G11 (RUST3-LIM) is recorded. L-G10 and L-G11 are met. **The critical path now waits on the owner:** what is left is O7 (B1), D3 and D13 (B3), and S-M, whose report waits for D13.
- **Timing:** H's and J4's sub-units now have rows. J4's rows move from day 4 to 5, J3a's lead set from 5 to 6, and J3b from 8 to 9 with its set from 9 to 10. New edges: X4-F3 → J3b, S21 → J3b and J3d (met), I1-a → E2s (met). The host chain stays 33 days.
- **New units and successors, cross-law routes, lead decisions** (each with its rejected alternative, or a note that the log records none), owner FYIs, product state, effort, "Unsized", "Risks" and "Not claimed".
- **One correction:** r9 cited MC:874, a C r6 line, under its C r7 pin. The line is MC:885.

## Decide

1. **Facts.** Check each row of "r10 changes" against its source. In particular:
   - every **r10:** cell in the units table, the carry-in table, "New units and successors" and "Cross-law items", against the log at `17584e1f5`, the review `status.json` and `review.json` files, and product `git log`;
   - **that nothing in review at the cut-off is recorded as accepted:** X2 r10, REG v3, X3c r9, X3b r11, X4T r13 and X9 r17's round 1, with its LD-RC-6;
   - that each accepted law's `review.json` `subjectSha256`, or each design unit's `subjectManifestSha256`, matches the bytes r10 pins;
   - the counts at `d2c00a9`: 97 contract successors, 96 inventory successors, v136 selected, and the order of the 15 new contract successors;
   - the product-state claim that, of the product files the table cites, only `Cargo.toml` and the generator pins changed between `cd5958b` and `d2c00a9`;
   - M3-L's gate: L-G10 and L-G11 met, and no delta round owed, because FA-2 was accepted at the subject L r5 joined (`dca02900…`) and RUST3-LIM is bound with the bytes L r5 pins (`70f494d9…`);
   - the lead-decision rows marked **r10:** against the log entries they cite;
   - the MC:874 → MC:885 correction.
2. **Scope.** Does r10 change any unit's scope beyond what an accepted law decided? Each scope change it records should cite its law: X4-F3 (X4 r8), S21 (J1 r5), E2s after I1-a (E1 r4), D4's own (a) check (D r5), L-G11 (L r5), H1 to H5 (H r3) and J4a to J4e (J-RW r4).
3. **The DAG.** Recompute the rows marked **r10:** in "r7 timing": H1 to H4 (7, 8, 9 and 9), J4a to J4e (J4e's set on day 5), J3a's set on 6, J3b on 9 with its set on 10, and X4-F3 before J3b starts on day 6. Confirm the 33-day host chain and the branch slack list. Name any edge from an accepted law that r10 misses.
4. **The owner gate.** Is "the critical path now waits on the owner" accurate? Check L's remaining items (L-G1, L-G4, L-G5, L-G9), S-M's dependence on D13, and that every host-chain unit from B1-a on needs L in effect.
5. **Rules kept.** The effort counts (about 79 law, successor or record units and about 94 code sub-units, about 173 in all), "Unsized", and the whole-M3 total left uncomputed.
6. **Points the drafter flags for your ruling:**
   - The log's P0 entry says P0 unblocks "D1–D4". D's own gate also needs L in effect, and r10 follows the law. Is that right?
   - The J-RW successors' `status.json` is ASSIGNED with a "not yet sent" note, while the log records the batch as sent. Several accepted reviews carry the same stale note. r10 records the batch as in review. Is that right?
   - P5-8 named S-M as the next run set. Since then the machine has run code-unit lanes, and S-M has not started; no log entry changes P5-8. r10 records this as status, not as a decision. Is that enough?
   - MB keeps r2 for its line citations, while MD, ME, MJ, MI, MH, ML and JRW move to their new snapshots. Is any cited MB line changed in r4?
7. **Anything else wrong,** including any r9 sentence that is now stale and that r10 should have marked.

## Output

Write `review.json` and `REVIEW.md`. `review.json` needs `verdict`, `subjectSha256`, `requiredFindings` and `nonBlockingObservations`. Don't commit.
