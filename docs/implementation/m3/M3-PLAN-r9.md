# M3 unit plan

Draft r9, not accepted. Claude Opus 5.5, implementation lead; drafted for the lead by a lead-dispatched drafting agent during the overnight autonomous run. **Planning record: not law, not code, not a contract successor.** It is the M3 counterpart of [m2/EXIT-PLAN.md](../m2/EXIT-PLAN.md). It orders M3's obligations into reviewable units and changes no accepted contract, gate, threshold or register row.

**r7 is a record revision.** It brings the plan up to date with the laws, lead decisions and cross-law items of the night of 2026-10-03 to 2026-10-04. It moves no gate or threshold the owner set. Durations and edges move only where an accepted law moved them. It adds one lead gate item to M3-L's own row (G10, FA-2; P7-2).

**Product baseline: main `cd5958b`.** Since r6's `3e64266`, six design units have been bound and one M2 fix integrated: F8b at `e093e90` (77 contract successors), I1-L at `0ceb9ad` (78), B-S1 at `9c11c53` (79), B-S2 at `240a795` (80), B-S9 at `8adfe0c` (81), X4-F1's code at `15c0779`, and I1-P at `cd5958b` (82) (ON, "F8b accepted and bound", "I1-L accepted by CODEX2", "B-S1 accepted by GROK2", "B-S2 accepted by Codex", "B-S9 accepted by Grok", "X4-F1 accepted by GROK2 and integrated", "I1-P accepted at r2"; product `git log`). **M2 is complete.** Grok's rerun on C (`3d2d5b5`) was accepted, and GROK2 accepted the completion record at r3 (M2C header; ON, "M2 COMPLETE", "The M2 completion record was accepted at r3").

**History.** r1 (`M3-PLAN-r1.md`, sha256 `65bf6ac5…`) and r2 (`M3-PLAN-r2.md`, `add49e25…`) were reviewed by GROK2 (facts) and CODEX2 (method). r3 (`M3-PLAN-r3.md`, `7ef4f0d1…`) was accepted by GROK2. r4 (`M3-PLAN-r4.md`, `e50f75d3…`) was accepted by CODEX2 on 2026-10-03. r5 (`M3-PLAN-r5.md`, 77,296 bytes, `f4833c60…`) drew two required findings from GROK2. **r6 was accepted by GROK2 on 2026-10-04** (`reviews/grok2-m3-plan-r6`, no findings or observations). Its bytes are `M3-PLAN-r6.md` (77,955 bytes, sha256 `a6956e88c94f1e47c5ccdfbc6e6a97bbf5a020f0df3fe68d80ae3d4f802dea55`); the live file carried them with a 2-line acceptance note, which r7 removes. Diff r7 against `M3-PLAN-r6.md`.

**Record cut-off.** r7 records the overnight log at sha256 `4a792685…` (315 lines; last entry "M3-H r3 written") and the review records in the arch tree at drafting. Where a verdict exists only in its own review file, r7 cites that file and says so.

**Short names.**
- **Contracts and architecture** (unchanged from r6):
  - **BP** `docs/v2/architecture/implementation-boundaries-and-build-plan.md`;
  - **COV** `docs/v2/architecture/implementation-coverage.v1.json`;
  - **CH14** `docs/v2/architecture/14-repository-and-module-layout.md`;
  - **F02** `docs/v2/architecture/02-distribution-and-components.md`;
  - **REG** `docs/v2/architecture/08-decision-and-readiness-register.md`;
  - **NE / IE / AQ / WS / SL** `docs/v2/contracts/product-v1/{native-evidence,identity-and-evidence,admission-and-qualification,workflows-and-surfaces,security-and-lifecycle}.md`;
  - **PTT** `docs/coop/artifacts/permission-truth-tables.v9.json`;
  - **TES** `docs/coop/design-corrections/workflows/schemas/test-execution.schema.json`;
  - **NEM** `docs/coop/design-corrections/native/native_evidence_model.v2.py`;
  - **RPP** `docs/coop/artifacts/rust-provider-protocol.v2.json`.
- **Accepted plans** (unchanged since r6's pins):
  - **AQP** `docs/implementation/m3/analysis-quality/PLAN.md`, the live file: r6, accepted, sha256 `1611014d…` (r6 bytes plus its 2-line acceptance note). Its bytes have not changed since r5 re-pinned every AQP line to it, so r7 keeps those lines.
  - **OPP** `docs/implementation/m3/operability/PLAN-r3.md` (r3, sha256 `b49035f2…`, accepted by Codex), cited by section.
- **M3 unit records.** **r7 cites every law by its accepted snapshot** (`PROPOSAL-rN.md`), never by a live file that may move (ON, "Pin drift handled"). A law in review that has no snapshot is cited by item and pinned by sha256 and the arch commit that holds its bytes.
  - **T2R** `docs/implementation/m3/corpus/README.md` (T2a and T2b accepted by GROK2; sha256 `3d355e72…`, unchanged).
  - **HD** `docs/implementation/m3/harness/DESIGN.md` (M3-Q0, r13 accepted by CODEX2; live sha256 `1f108399…`, unchanged).
  - **MI / MIU** `docs/implementation/m3/preview-pack-i1/PROPOSAL-r2.md` and `UNITS-r2.md` (M3-I1 r2, accepted by CODEX2; `1eb47d1e…` and `0c3c0f44…`; `UNITS-r2.md` is byte-identical to the live `UNITS.md`, so r6's MIU lines hold). **I1L** `preview-pack-i1/i1-l/README.md` (I1-L, accepted and bound).
  - **MB** `docs/implementation/m3/config-discovery-b/PROPOSAL-r2.md` (M3-B r2, accepted by GROK2; `92e65825…`). r6 cited the live file, which carries a 2-line note, so **r7 re-pins every MB line by −2** (for example MB:843-851 becomes MB:841-849). **BS9** `config-discovery-b/b-s9/README.md` (B-S9, accepted by Grok and bound).
  - **MC** `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md` (M3-C r7, accepted in review by CODEX2; `a1ee9386…`), cited by item and section. r7 is r6 (`PROPOSAL-r6.md`, `8274bca1…`, also accepted in review) plus row 8's narrowing; its "r7 changes" and "r6 changes" sections record both. **CRC1 / CR1** `snapshot-plan-c/crc-1/README.md` (`202fc5c2…`) and `snapshot-plan-c/cr-1/README.md` (`c7cf5194…`), C's successors CRC-1 and CR-1, in review with GROK2 and CODEX2 (unit files untracked).
  - **MD** `docs/implementation/m3/supervisor-d/PROPOSAL-r3.md` (M3-D r3, accepted by GROK2; `9679dbc4…`).
  - **ME** `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` (M3-E1 r3, accepted by Codex; `d71031ff…`), cited by item. **E0R** `syntax-e/E0-REPORT.md` (`c1011e83…`, arch `c87d311f4`), the E0 record, accepted by GROK2 in record review (`reviews/grok2-e0-report-r1`).
  - **MJ** `docs/implementation/m3/host-pipeline-j/PROPOSAL-r4.md` (M3-J1 r4; r3 accepted by CODEX2, r4 accepted by GROK2; `c18c0d3c…`).
  - **SOP2** `docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md` (S-OP-2 r6, accepted by Codex, ACCEPT-DESIGN-UNIT; `ce8d3a4b…`). Its accepted bytes still carry r5's title line; the live file's acceptance note says so.
  - **ML1** `docs/implementation/m3/provider-protocol-l/PROPOSAL-r1.md` (M3-L r1, `5e858c05…`; never sent). r6's ML lines (ML:180-188, ML:453-455) are r1 lines and resolve here. **ML2** `PROPOSAL-r2.md`, M3-L r2 (`5bd4025e…`, 91,126 bytes; the same bytes are at arch `3625ae294`); Grok returned one required finding. **ML3** the live `PROPOSAL.md`, M3-L r3 (`6df524a4…`, 121,776 bytes, arch `e35272519`), **in review with Grok** (`reviews/grok-provider-protocol-l-r3`). All are cited by item and section. **FA2** `native-successors-fa/fa-2/` (README `6a0aa426…`), FA-2, **in review with Codex** (`reviews/codex-fa-2-r1`).
  - **MH** `docs/implementation/m3/fact-admission-h/PROPOSAL-r1.md` (M3-H r1, `69f50bb1…`; also at arch `9c716bc16`). **MH2** `PROPOSAL-r2.md`, M3-H r2 (`4ae48f09…`; also at arch `6eb918468`). r2 keeps r1's units, successors and cross-law items; it answers RF-1 and rebuilds item 10. Grok raised one consistency finding on r2. **r3**, the live `PROPOSAL.md` (`7a562720…`, arch `249d74ab4`), is written and queued for Grok after L r3: item 14.4 is the one routing authority, and X-H3's successor is renamed "M3-C r8 / CRC-2" (ON, "M3-H r2 written and sent to Grok", "M3-H r2: Grok raised one consistency finding", "M3-H r3 written"). r7 cites MH by item.
  - **JRW** `docs/implementation/m3/resume-repair-jrw/PROPOSAL-r2.md`, J-RW r2 (`7bff3d55…`; also at arch `9bccaa8fa`), **in review with Codex**: two P2 findings, and r3 is being written. r1 is `PROPOSAL-r1.md` (`0002c005…`).
  - **CFP** `docs/implementation/m3/confinement-cf/CF-P-RECORD.md` (the CF-P record, `6323a1b4…`), cited by section.
- **M2 records:**
  - **EXIT** `docs/implementation/m2/EXIT-PLAN.md` (sha256 `fee07b44…`). r6's EXIT lines still hold there: EXIT:61, :112, :171, :182 and :186-191 read as r6 cites them.
  - **M2C** `docs/implementation/m2/M2-COMPLETE-r3.md` (accepted by GROK2; `79336e24…`).
  - **F8B** `docs/implementation/m2/generator-closure-f8b/PROPOSAL-r2.md` (accepted by CODEX2; executed and bound at `e093e90`).
  - **X11** `docs/implementation/m2/cli-enablement-x11/PROPOSAL.md` (r1, accepted).
  - **X12** `docs/implementation/m2/policy-admission-x12/PROPOSAL-r3.md` (r6's X12:NNN lines). **X12r4** `PROPOSAL-r4.md` (accepted by Grok; `adc9a88a…`).
  - **X2r9** `docs/implementation/m2/project-root-x2/PROPOSAL-r9.md` (accepted by Grok; `0d68e3a5…`).
  - **X3C** `docs/implementation/m2/ledger-blob-x3c/PROPOSAL-r8.md` (X3c r8, accepted by GROK2; `ba638efb…`).
- **The overnight log, ON:** `docs/implementation/OVERNIGHT-2026-10-03.md`, cited by entry.
- Product paths are under `opensip/`.

## r9 changes

r9 answers GROK2's r8 review (`reviews/grok2-m3-plan-r8/`) and changes nothing else. r8's bytes are preserved in `M3-PLAN-r8.md`.

| Finding | Change |
|---|---|
| RF-1 | **Record cut-off kept.** r7, r8 and r9 all record at r7's cut-off, when M3-H r3 was in review. r8's "MH r3 accepted" in the day-0 assumption broke that rule and is withdrawn. Since the cut-off, Grok accepted M3-H r3 (`reviews/grok-fact-admission-h-r3/`, `7a562720…`); the next record revision records it everywhere at once. |
| RF-2 | The NBO-1 row now points at the DR-G10 sentence by section, not line. The rename reads "L-G1 onwards", since this plan's M3-L gate runs G1 to G10. |

## r8 changes

r8 answers GROK2's r7 review (`reviews/grok2-m3-plan-r7/`) and changes nothing else. r7's bytes are preserved in `M3-PLAN-r7.md`.

| Finding | Change |
|---|---|
| RF-1 | The day-0 assumption ("Critical path") and the Unsized list now name the X-H3 widening as M3-C r8 with CRC-2, matching the widening row, the cross-law route and the reversible-decision row. CRC-1 stays the day-5 successor for C's existing law. |
| RF-2 | The Risks bullet now records X4-F1's confirmation lane as passed: 1749/0/3 on `15c0779`. |
| NBO-1 | Recorded, not changed. In the units table, "G10" means the DR-G10 gate (the seven-gates sentence under "What M3 exit means"); in the M3-L gate table, item G10 is "FA-2 accepted". Both are defined where they appear. M3-L's next revision is to rename its gate items with an `L-` prefix (L-G1 onwards), which removes the collision at the source. |

## r7 changes

r7 is a record revision. Every row cites its source; a source still in review is marked "(in review)" and nothing from it is recorded as accepted.

| # | Change | Source |
|---|---|---|
| 1 | **Header and baseline.** r6's ACCEPTED note is removed. The baseline is product main `cd5958b` (82 contract successors, X4-F1 integrated). M2 is complete. Laws are cited by snapshot (see "Short names"); MB lines move by −2. | ON ("F8b accepted and bound", "I1-L accepted", "B-S1 accepted", "B-S2 accepted", "B-S9 accepted", "X4-F1 accepted by GROK2 and integrated", "I1-P accepted at r2", "Pin drift handled"); M2C header; product `git log`; `diff MB-r2 MB` |
| 2 | **Status cells.** Every unit row is brought up to date. **Accepted tonight:** S-OP-2 r6 (Codex), M3-E1 r3 (Codex), M3-J1 r3 (CODEX2) and r4 (GROK2), M3-D r3 (GROK2), X3c r8 (GROK2), the M2 completion record r3 (GROK2). **Accepted in review:** M3-C r6 and r7 (CODEX2). **Design units accepted and bound:** F8b (`e093e90`), I1-L (`0ceb9ad`), B-S1 with SX-1 (`9c11c53`), B-S2 (`240a795`), B-S9 (`8adfe0c`), I1-P (`cd5958b`). **Integrated:** X4-F1 (`15c0779`). **Accepted as a record:** the E0 report (GROK2). **In review:** M3-L r3 (Grok; r2 had one finding), FA-2 (Codex), M3-H (r1 and r2 one finding each; r3 queued), J-RW (r2 two findings; r3 being written), CRC-1 (GROK2) and CR-1 (CODEX2). P0's phase 1 is ready, and its phase 2 is running. | ON; `reviews/*/status.json` and `review.json` named in each row |
| 3 | **M3-L.** The early-review rule is recorded as a lead decision. The gate table is refreshed: G2, G3 and G7 met; G4 and G5 owner items under B3; G9 the owner item O7 (B1), with CF-P's evidence; G1 (S-M) not started. **Day 0 means L in effect** (P7-1). L r2's X9 is applied: r6's "Before L can be sent" (`M3-PLAN-r6.md:445`) and its r2-after-S-M drafting line (`:426`) are superseded, and the O7 risk line (`:524`) is refreshed. **FA-2 becomes gate item G10** (P7-2), as L r3, now in review, also proposes. | ON ("Lead decision: M3-L gets an early review round", "M3-L r2 written", "M3-L r2: Grok raised one required finding", "Plan for X-H1", "FA-2 and M3-L r3 written"); ML2 "Review and effect", "Acceptance gate", X9; ML3 G10, X16; `reviews/grok-provider-protocol-l-r2` |
| 4 | **M3-D's units** are taken from the accepted law: D1a, D1b (O7), D2a, D2b, D3a, D3b, D4 and D5, with D's own timing. D3 finishes on day 10, D4 on 10, D5 on 13 and D1b on 5, so G2-v moves to day 6 and O3 to day 16. D's successors SD-1 to SD-6 are named. The O7 section follows MD F8 (seccomp, not a network namespace), and the D lane is GROK2's (MD F9). | MD "Units after the law", items 14, 29, 30 (F8, F9) |
| 5 | **M3-E.** The units gain **E2s** (M, 2 days) from the accepted E1 r3, with SYN-1F, ME's second-integrator rule and ME's planning record M3P-E. **E0 is complete, and the outcome is T-native:** P5 fails (median 0.818 MiB/s against a 1.0 floor) while P1–P4 and P6 pass. By E1's predeclared rule, syntax uses native tree-sitter linked in the host (`native-linked-v1`), under item 18's fallback posture. GROK2 accepted the report. The units do not change, and E2a can start once P0 lands. | ME items 3, 18, 19, 20, "Owner notes"; E0R "Outcome"; ON ("E0 complete: the outcome is T-native", "E0 report accepted by GROK2") |
| 6 | **M3-J's units** are J1's: J2a, J2b, J2c, J3a, J3b and J3d, with J4 owned by J-RW. J1's successors S2 to S20 are listed, S19 (M3-C r7) and S20 (SD-5's record) among them. The host chain runs H → J2b → J3d. J2c joins M3-X (P7-3). | MJ items 12, 13 (S17, S19, S20), 14, 15 |
| 7 | **New units and successors found tonight** get a table with owner, dependencies and size: FA-1, FA-2, the X-H3 widening (M3-C r8 and CRC-2), B-S9 (now bound), SD-5 with S20, S19 (M3-C r7, now accepted in review), X3d r9, X3c r9, the X9 r17 record, M3-B's record revision, E1's, I1's and D's record items, and H's H3 unit. | "New units and successors (r7)" below |
| 8 | **P5-1's owner list** gains X3b (`trust/carrier-floors/`) and the registry owner, and J4's proposed sub-units J4a to J4e are recorded (in review). | JRW LD-12, X-RW-7, RW-S7, item 11, item 14 (in review) |
| 9 | **M3-H's proposal** is recorded (r1, kept by r2; in review): units H1 to H5, of which only H5 is on the host chain; successors FA-1, FA-2 and the X-H3 widening; H3 takes the host-produced inventory records (X-H5). | MH items 18, 25, "H. Successors", "Cross-law items"; MH2 (in review) |
| 10 | **Critical path.** Recomputed only where an accepted law changed a duration or an edge (P7-5). **Still 33 days.** What moved: the D rows, G2-v, O3, E2s and the J split. What did not: the host chain, K2 by 28, O2_selected by 31, X12d's lead set by 22. New conditions: J3d's waits (MJ item 14), D3's two days of slack, and H r1's FA-2 and X-H3 timing (in review). | "Critical path" below; MD, ME, MJ, MH item 25 |
| 11 | **M2 carry-ins.** F8b is done and bound. **X4-F1 is accepted and integrated** at `15c0779`, so M2's known defect X4 F-1 is fixed; X4-F2 remains. X3c r8 is accepted. The X11 successor law (J1) is accepted. X4T-c is unblocked. P5-8's run sets ahead of S-M are done, X4-F1's confirmation workspace lane included, and E0 is complete. | ON ("F8b accepted and bound", "X4-F1 accepted by GROK2 and integrated", "Confirmation lane on product main `15c0779`", "X3c r8 accepted", "E0 complete"); M2C §5; `m2/reviews/grok2-observer-expiry-x4f1-r1` |
| 12 | **M3-B, M3-C and M3-I1 detail.** B-S9 is split from B-S1, is B1-a's dependency, and is bound; all three B design units are bound. GROK2's ruling R2 on B-S1 sends a row-3 correction to M3-B's next record revision, and B-S2's observation goes to C1b. C r6's X-C1 and X-C2 are applied, and C r7 narrows row 8. Both I1 design units are bound, so the I1 product chain waits only for the machine. I1's record items are listed. | ON ("B-S9 accepted by Grok", "M3-C r7 accepted in review", "I1-P accepted at r2"); BS9 "What it is"; `reviews/grok2-b-s1-r1/REVIEW.md` "Rulings"; MC "r6 changes", "r7 changes"; I1L "Deviations" |
| 13 | **Cross-law items** from ML2 (X9 to X12), ML3 (X13 to X16; in review), MH (X-H1 to X-H6), JRW (X-RW-1 to X-RW-12), X3C (CL-1 to CL-5), ME (M3P-E), MJ (S17), MD (F1 to F13), E0 and I1-L get one routing table. | "Cross-law items (r7)" below |
| 14 | **Owner blockers** B1 to B4 are restated as they stand, with CF-P's evidence in B1, and the night's reversible lead decisions are listed by source. | ON "Blockers for the owner" and work log; CFP |
| 15 | **Effort, lanes, "Next", "Unsized", "Risks" and "Not claimed"** are updated. P5-3's generator order now includes E2s (P7-4). | arithmetic over the rows above; ME item 20; reviews |
| 16 | **Product state.** F8b's re-pins change the generator and lane-registry rows. No other cited product file changed between `3e64266` and `cd5958b`. | product `git diff --stat 3e64266 cd5958b`; `m2/reviews/grok-generator-closure-f8b-unit-r1/REVIEW.md` |
| 17 | **P0's phase 1 is ready:** inventory v135, `crates/components` and `crates/syntax` as members, and `tools/host/dependency-policy.json` with C's inflater rows; its phase 2 started after X4-F1's confirmation lane passed on `15c0779`. | ON ("P0 phase 1 ready", "Confirmation lane on product main `15c0779`") |
| 18 | **Rust3's 256-subject request cap** (ML3 X13, in review): 9 of the 22 T2 Rust repositories exceed it. The lead recommends a Rust3 limit successor before G3 ships, measured by S-M. It is recorded in the G row, the new-units table, "Risks" and "Owner decisions". | ON ("New finding, important for the owner's Rust use"); ML3 X13, R12 |

## r6 changes

r6 answers GROK2's r5 review and changes nothing else. r5 is preserved as `M3-PLAN-r5.md`.
- **RF-1:** B2 now cites HD §5.6, §5.8 and OI-3. It states the accepted gating floor (a 0.99 lower bound, k_min 299) and that 59 is the zero-error count for the lead's proposed 0.95 bound.
- **RF-2:** G7 now records that S-OP-2 r3 received required findings and that r4 is in review.

## r5 changes

| # | Change | Source |
|---|---|---|
| 1 | **Header.** The r4 ACCEPTED note is removed. The baseline is main `3e64266`; M2 completion waits for Grok's rerun on C. | ON ("X9-6 accepted and integrated", "M2 crash matrix"); M2C:5, §6 |
| 2 | **M3-T2 is complete.** T2a and T2b are accepted: 49 repositories, 33 families, 5 workspaces. Its two open items are carried into K1a and the gating bar. | ON ("M3-T2b sent", "accepted by GROK2"); T2R:24, T2R:296; `reviews/grok2-corpus-t2b-r1` |
| 3 | **M3-Q0 is accepted.** K2 is sized at **16 days**, with per-lane oracle freezes. K2b and K2c are frozen before day 0, and K2a on days 0–6. Every bound in Q0's OI-12 list is applied: the K2 row, the R and M3-M rows, the K2 condition, the unbounded list, the pre-day-0 list, F1's first T1 run, and the slip rule, recomputed for r5. | HD §13 (HD:1177-1237); OI-12 (HD:1256) |
| 4 | **M3-I1's law is accepted, and I1 is resized from M to L.** It splits into I1-L, I1-P, I1-a, I1-b1, I1-b2 and I1-c. New edges: **I1-c → C4a**, **I1-b2 → X12d and J2**, and **F8b → I1-a**, because the contract generator refuses until F8b. | MI (r2 ACCEPTED); MIU:28-40; ON ("M3-I1 r1 sent", "F8 split"); M2C §5 row 2 |
| 5 | **M3-B's law is accepted.** It has nine code and harness sub-units and two design units, with successors S1 (X2 r9) to S9. The discovery ledger profile raises the platform caps for discovery only. **B2-c, which C1a waits for, finishes on day 10.** MB's own estimate of "about day 8" omits B2-b's edge on B1-b. | MB items 12 and 25, F14 (MB:805), unit table (MB:843-851) |
| 6 | **M3-C r3's units are taken in.** C1, C2 and C3 each have three sub-units; C2b is a hard XL part (5 days). C3b gets the D1 edge, with O7 and the D law as day-0 assumptions. C4 splits into C4a and C4c (variant B), with C4b = X12d. **X12 r4 and SX-1 become gates.** F1 and G1a wait only for the interfaces they consume. | MC "r3 changes", "Successors", "Units", "Acceptance gate"; `reviews/codex2-snapshot-plan-c-r2` (C2-N1) |
| 7 | **The critical path is recomputed: 33 days** under variant B (34 unsplit). That is MC r3's b + 23 with b = 10. Its conditions are K2 by day 28, O2_selected by day 31, and X12d's lead set by day 22. The slip rule is now M3-X = 33 + max(0, *s* − 10). r4's 26 days and MC r2's 28 no longer hold. | "Critical path" below; MC "Units"; MB:843-851 |
| 8 | **M2 carry-ins without an owner now have one** (lead decisions P5-1 to P5-5). The **resume/repair writer** goes to J-RW (law) and J4 (code), and J4 no longer waits for J3. The **X3c successor** goes to X3c r8 (law) and X3c-3 (code) before J3. Also scheduled: X3a-2, X4T-c, X4-F1, X4-F2 and F9, with X4b deferred. M2C's "no M3 unit row names it" overstates the gap. r4's M3-J row did name J4 and an X3c successor (M3-PLAN-r4.md:168), but gave neither a law, an author nor a code unit. | M2C §3.3, §4.1 (L11), §5 rows 2, 10, 11, 13–16; EXIT:171, EXIT:186-191; ON ("X4-F1 written") |
| 9 | **M3-L's gate is updated.** T2b and S-OP-2 are now met. S-M, the D3 and D13 sign-offs, and O7 remain open. | ML "Acceptance gate"; ON; `reviews/codex-s-op-2-r3/status.json` |
| 10 | **M3-L's findings are recorded.** Changed-scope reuse needs an identity-contract successor (INC-1). The Rust3 stage-1 cancel grace is 5,000 ms. | ML item 4 (ML:180-188), item 16c (ML:453-455), X3 |
| 11 | **Owner decisions still pending:** O7 (B1), the gating precision bar (B2), the D3 and D13 sign-offs (B3), and OQ-1 (B4). Tonight's lead decisions are listed. | ON "Blockers for the owner"; MB item 27; MC "Open questions"; M2C §5 |
| 12 | **Citation re-pins:**<br>- **"AQP:537" is now AQP:556**, and every other AQP line moves with it (for example, INC-1 to INC-8 are now AQP:389-409);<br>- X12 is cited at its r3 snapshot;<br>- EXIT lines after 61 move +2;<br>- `package.json:7`, `:12` become `:8`, `:13` after L1's licence line;<br>- the stale "Draft r3" header is fixed. | MB:38 (F8); ML:553 (X8); `git diff 6f85fe717 HEAD -- EXIT-PLAN.md`; product `git diff eb0d503 3e64266` |
| 13 | **Non-blocking observations folded in:**<br>- the stale "operability r3 in review" risk is removed (GROK2 r3 NBO-2);<br>- G2-v is said not to be D1's enforcement claim (NBO-3);<br>- late branches are compared by their arrival at M3-X (CODEX2 r4 N01). | `reviews/grok2-m3-plan-r3/review.json`; `reviews/codex2-m3-plan-r4/review.json` |
| 14 | **Smaller updates:**<br>- the licence unit is done (L1, product `2967905`);<br>- T3 now waits only on OQ-1 for its multi-repo instance;<br>- the calibration count is 62 commits;<br>- the effort count and lanes are updated. | M2C §3.2 (rows 59 and 62); AQP:547, AQP:555; MB "Not claimed" |
| 15 | **The C law can be accepted only after L** (MC's gate), so it is accepted at or after day 0. The DAG tolerates acceptance by day 5, with SX-1 by day 2. | MC "Acceptance gate", "Units"; "Critical path" below |
| 16 | **M3-E's units come from E1 r1** (drafted, in review with Codex): E0 (a probe), E2a, E2b, E2c and E3. The backend decision is tree-sitter grammars compiled to Wasm, run in-host by `wasmi`, with native tree-sitter as the fallback if E0 fails. E3 lands on day 14, with 14 days of slack, so the host chain does not move. | ME items 2, 3, 19, 20; ON ("M3-E1 r1 drafted") |
| 17 | **The overnight log's "about 31 days"** (its "M3-C r3 sent" entry) is the b = 8 figure. r5 records **33** (b = 10) and shows 31 only as MB F14's estimate. | ON; row 7 |

## r4 changes and review responses

r4 changes one thing. GROK2 accepted r3 (`7ef4f0d1…`), and r3 is preserved as `M3-PLAN-r3.md`.

| Finding | Change |
|---|---|
| CODEX2 C2-M3-R3-01 | `O2_selected` is now in M3-X's dependencies and in its maximum. The 26-day condition now also needs every O2 part kept in M3 to finish by day 24. The note on which branch becomes critical when it runs late is qualified to match. |

## r3 changes and review responses

| Finding | Change |
|---|---|
| GROK2 RF-1, CODEX2 C2-M3-R2-01 (the DAG and critical path) | **Missing edges added:**<br>- K1 → M3-M;<br>- CF-P → D-law acceptance;<br>- CF-1 → D5 and D's enforcement claim;<br>- D1's confinement primitive → every provider launch.<br>**Authoring and launch are separate.** G2 is authored before day 0. Its lawful launch, G2-v, runs after O7 and D1.<br>**Every M3-M and M3-X prerequisite has a duration or a finish bound,** with three exceptions: K2, R and O2. Those are unbounded until Q0 sizes K2 and their successors are accepted.<br>**26 days is now only the conditional host-chain duration.** The whole-M3 total is left uncomputed. |
| GROK2 RF-2 | M3-M cites AQP:236 only for too few findings. Closing an exploratory report with gating or repair-eligible adjudication still pending is **this plan's rule**. Any later Q2 use still needs AQP:228 and AQP:246. |
| GROK2 RF-3 | OPP §10 is cited for its ten areas. The three escape cases are new D5 and S-OP-11 controls. |
| GROK2 RF-4, CODEX2 C2-M3-R2-02 | A gated **M5 successor package, M5-EX**, must be accepted before M5's `execution.rs` claims any enforcement:<br>- the native §5.2 admission and disclosure join (NE:2440-2444, NE:2480-2487; NEM:2170-2182);<br>- the WS §7 test-execution schema join (WS:1071-1081; TES:7-14);<br>- a measured truth-table profile succeeding PTT.<br>Repository-code execution stays out of M3. The worker prohibition (NE:2534-2535) and the closed DR-128 untrusted-code scope (AQ:344; REG:317) are preserved. |
| GROK2 NBO-1..6 | Adopted:<br>- the citations are now `policy.rs:1087`, `policy.rs:1401`, X12:134, NE:2534-2535 and COV:4772 with 8976;<br>- the r2 response wording for S-OP-4 is clarified below: S-OP-4 is law content, not a gate item;<br>- CF's gates add G09 and G30 (AQ:344);<br>- launch rules have one owner, the D law, and M3-L cites it. |
| CODEX2 N01..N03 | Adopted:<br>- S-P and S-M state their launch boundary;<br>- the escape controls are labelled as an extension;<br>- the NE:2534-2535 span. |

(The AQP lines in the r3 and r2 tables are r4-era lines, kept as reviewed. r2's table is in `M3-PLAN-r4.md`.)

(The r5 table's MB lines are the live file's, +2 against `PROPOSAL-r2.md`; the history tables keep their reviewed citations.)

## What M3 exit means

The build plan's milestone row (BP:887) defines M3:

- **Deliverable:** "M2 and provider build lanes; discovery/configuration, sealed snapshot/Plan, supervised TS/JS and Rust analysis and the guarded durable host pipeline".
- **Owners:** "Host discovery/snapshot/plan/analysis; components protocols; both providers and evaluator".
- **Completion:** "Selected native matrix/corpora, missing-role disclosures, cancellation, semantic admission and host-boundary durability checks; neither language silently dropped. Complete CLI analysis delivery follows at M4 with every advertised renderer".

**Routed to M3 by the coverage groups** (COV), with the gates in the qualification routing table (BP:999-1036). BP:933-945 is only the population census.

- **All 66 capability cells** (COV:2077-4425): 57 SUPPORTED-DESIGN, 6 UNSUPPORTED-TYPED and 3 NOT-SELECTED (AQP:113). That is 33 TS/JS, 22 Rust and 11 syntax-only cells.
- **Seven gates, to be prepared, not qualified:** DR-G10 (BP:1014), G13 (BP:1017), G14 (BP:1018), G21 (BP:1025), G23 (BP:1027), G25 (BP:1029) and G29 (BP:1033). Execution stays at M6 (BP:895, BP:999-1000).
- **All seven shared flags** (COV:5266-5407).
- **Twelve contract sections:**
  - security-and-lifecycle:3 (COV:6702);
  - native-evidence:2, :3, :4, :5, :7, :9, :10, :11, :14 and :15 (COV:7066, 7093, 7118, 7144, 7193, 7245, 7270, 7294, 7366, 7390);
  - workflows-and-surfaces:2 (COV:7438).
- **Five Fallow constraints:** FW-01 (COV:7852), FW-03 (7894), FW-08 (7999), FW-13 (8104) and FW-14 (8125).
- **No command.** Every analysis command is M4 or later (BP:949-995). Complete CLI delivery is M4 (BP:887-888). J1 confirms it: no analysis word is wired in the binary at M3 (MJ item 1).

**The accepted quality plan's M3 obligations.**

*Before the provider protocol is fixed* (AQP:499):
- INC-1 to INC-8 in the M3 law, plus the INC-7 spike;
- pinned T2 manifests, including the multi-repo approximation and Python (**done**: M3-T2);
- the harness design and the rule-catalog draft (**done**: M3-Q0).

*At M3* (AQP:500):
- T1 for all 57 supported cells per mode, typed refusal for 6 and non-advertisement for 3;
- Q1 and Q4 on T1;
- draft catalog rules run non-authoritatively, for exploratory Q2–Q4 on T2;
- the determinism suite and exploratory Q6 workloads;
- the multi-repo workspace shapes in discovery;
- the third-language readiness review;
- an internal-harness dogfood checkpoint, "not CLI `analyze`".

**The operability plan's provisional M3 items** (OPP r3 §8).

*Before the protocol law:*
- O1 decided, with S-OP-4's record join under (a). ML item 11 decides it, as a lead decision (ML1 and ML2).
- O7 decided by the owner. **Still pending (B1).** CF-P's evidence is in (CFP).
- The S-OP-2 vocabulary drafted. **Done and exceeded:** S-OP-2 was accepted at r6 by Codex (SOP2; `reviews/codex-s-op-2-r6`).

*At M3:*
- `tracing` with nonpersistent sinks, the vocabulary and allowlists, the bounds and loss marker;
- phase spans and the operational record as harness instrumentation;
- the supervision primitive and liveness;
- the outcome matrix in tests;
- two-stage cancellation;
- the enforcement checks.

*Once their successors are accepted* (OPP §9): the file sink (S-OP-1), crash records (S-OP-7), capacity preflight (S-OP-8), public switches (S-OP-5 and S-OP-6), and the cancellation and commit join (S-OP-12, now J1 item 8; MJ S15). The G20/G21 controls are authored now (S-OP-11). DR-G20 itself is an M5 implementation row (BP:1024).

**M2 carry-ins.** Every one has an owning unit; the table under "Units" gives the gates.
- **X11 successor law** → J1, **accepted** (MJ; X11:64-81). It fixes the order, the creator's host entry, the one-RequestId rule, the creator terminations, the F0 binary restatement and the backup-status successor (J-BS, S13), and resolves X11 r1 item 1a's conflict with X12 r4's first-use clause (MJ items 1 to 4, 9; S1).
- **X12c and X12d.** X12c, the DR-131 preview pack, is **M3-I1**. X12d, the Run-closure `check_plan_pack` join, is **C4b**. It must land before any producer reaches X5 (X12:191-192).
- **The resume/repair writer** for the crash states M2 leaves refused (EXIT:186-191; M2C §4.1, L11) → **J-RW and J4** (P5-1). J-RW is in review: r2 drew two findings, and r3 is being written.
- **An X3c successor**, because re-commit is refused at staging (EXIT:171) → **X3c r8, accepted, and X3c-3** (P5-2).
- **From the M2 completion record** (r3, accepted): F8b (done), X3a-2, X4b, X4T-c, X4-F1 (done: integrated at `15c0779`), X4-F2 and F9 (M2C §3.3, §5 rows 2, 13–16, 23, 24).
- **The product licence unit is done:** L1 at product `2967905`, inventory v134 (AQP:555; M2C §3.2 row 59).

## Product state, by M3 owner module

The table was read at `eb0d503` for r4, and every cited file was rechecked against `3e64266` for r5. **For r7,** `git diff --stat 3e64266 cd5958b` touches only `design-lock.json` (the six bindings), `schemas/registry.json`, `apps/report/src/generated/report.ts` and files under `tools/` (F8b), plus X4-F1's custody and trust files under `crates/security/src/` (`custody/operation_guard.rs`, `trust/*`, `trust_time.rs` and their tests). None of those is cited below, so every cited line holds; only the generator rows move.

| Owner (BP:887; CH14) | State | What exists |
|---|---|---|
| `crates/host/src/discovery.rs` | **absent** | First milestone M3 (COV:8963). |
| `crates/host/src/configuration.rs` | partial | Only X12's pack admission. "Layer merge, discovery, profiles, capabilities, waiver IDs and `resolvedConfigDigest` arrive with M3" (`crates/host/src/configuration.rs:1-4`). The digest is defined at IE:518. |
| `crates/host/src/snapshot.rs`, `plan.rs`, `analysis.rs`, `invocation.rs`, `syntax.rs` | **absent** | Planned owners at CH14:495, 489, 475, 485 and 496. |
| `crates/host/src/fact_admission.rs` | partial | The replay join only. "The M3 syntax, context, occupancy and Coverage joins arrive in this module" (`fact_admission.rs:1-3`). MH item 2 proposes child modules under `fact_admission/` (in review). |
| `crates/host/src/request.rs`, `outcomes.rs` | partial | A process-custody `RequestAuthority` for the nonpersistent metadata host (`request.rs:15-19`). |
| `crates/host/src/finalization.rs`, `crates/storage/src/commit.rs` | present (M2) | The finalization and commit library. No command reaches it (`crates/host/src/lib.rs:53-62`). |
| `crates/components/*`, `crates/syntax/*` | **absent** | Not workspace members (`Cargo.toml:3`). CH14:37 and CH14:41 mark them "proposed". |
| `crates/security/src/component_manifest.rs` | present | The structural manifest owner, "no runtime or artifact authority" (`component_manifest.rs:1-2`). `components/manifest.rs` (the DR-G29 owner, BP:1033) is absent. |
| `crates/security/src/grants.rs` | **absent** | Yet it owns four M3 flags (COV:5277, 5317, 5337, 5377). MB's B3-a creates it. X4b's `admit_repo_execution_grant` is deferred to M5-EX (M2C §5 row 14). |
| `crates/platform/src/process.rs` | **absent** | The only process module is a read-only translation query (`crates/platform/src/macos_process.rs:1-2`). MD's D1a builds it. |
| `crates/evaluator` | largely present | Inspectors (`crates/evaluator/src/lib.rs:9-38`), pack admission (`lib.rs:111`), derivation (`lib.rs:122`) and replay (`lib.rs:127`). The pack registry has **zero rows** (`pack-registry.json:3`). Named admission returns `NotBundled` (`policy.rs:1087`), and `check_plan_pack` refuses an unbundled Plan policy (`policy.rs:1401`, with the refusal at `:1402`). |
| `crates/identity`, `crates/contracts` | present | The `IdentityDomain` enum and its prefixes, `fact2` through `subject3` (`crates/identity/src/descriptors.rs:483-555`). Generated TS2 and Rust3 frame carriers (`crates/contracts/src/generated/protocol.rs:5422`, `:6111`) from a carrier input that is "not a production wire decoder" (`schemas/wire/native-carriers-v1.json:4`). **r7:** F8b is bound at `e093e90`. The generator closure and the TypeScript lane registry now pin VD1's `verify_design.py` (40,714 bytes, `c13d231e…`; `tools/typescript-lanes.json`), so the generator no longer refuses on the old pin (M2C §5 row 2; F8b unit review). `design-lock.json` holds 82 contract successors at `cd5958b`. |
| `providers/typescript` | stub | Present: `package.json`, `tsconfig.json` and the inert generated types (`src/generated/protocol.ts:1`), pinning Node 24.16.0 and TypeScript 6.0.3 (`package.json:8`, `:13`). Absent: every implementation source in CH14:507-517 and CH14:519-524. |
| `providers/rust` | stub | `main.rs` exits failure before reading a request (`providers/rust/src/main.rs:1-14`). It has its own workspace (`Cargo.toml:1-2`) and `rust-version = "1.95"` (`Cargo.toml:8`). The 1.95.0 pin has only rustfmt and clippy, no `rustc-dev` (`rust-toolchain.toml:2-4`). |
| `crates/lifecycle/src/installation.rs` | **absent** | The DR-G14 owner (BP:1018; COV:4770-4772), whose first milestone is M5 (COV:8976). |
| Tests | partial | `crates/host/tests/admission_tests.rs` exists. These named owners are absent: `discovery_tests.rs` (COV:5280), `workflow_tests.rs` (COV:7865) and `tests/qualification/README.md` (COV:8138). |
| Operability | **absent** | No `tracing` in `Cargo.lock`. No `std::panic::set_hook`. No `--timings` in `apps/cli/src/arguments.rs`. Three coded stderr lines (`apps/cli/src/bootstrap.rs:19`, `:44`, `:65`). The default command refuses (`arguments.rs:104`). |

Also in place:
- the M1 provider lane checks (`tools/check_typescript.py`, `tools/typescript-lanes.json`). **r7:** F8b re-pinned them onto VD1. `check_typescript.py` now passes its tracked rows and stops at the absent `node_modules` tree, before any child (`m2/reviews/grok-generator-closure-f8b-unit-r1/REVIEW.md`, step 8).
- the Rust provider, excluded from the host workspace (`Cargo.toml:4`), as BP:621-622 requires.

**Stale text that the M3 laws must not copy.** F02:220 still says TypeScript major 1, and F02:259 says Rust major 2. The current protocols are TS2 and Rust3 (BP:716-717).

## Units, in dependency order

Sizes follow EXIT:61:
- **S:** about one review round of a single file.
- **M:** several files with one inventory successor.
- **L:** a law plus two or three code units.
- **XL:** a law plus four or more units and a harness.

Each sub-unit (B1-a, C2b, D3a, J2b …) is reviewed on its own; the row is the planning unit. The dependency column gives integration edges. A unit may be **authored** earlier, against its predecessors' accepted interfaces (MC "Units"). Sub-units proposed by a law still in review are marked "(proposed)".

| Unit | Scope | Depends on | Law / successor? | Size | Gates and quality items |
|---|---|---|---|---|---|
| M3-T2 | **Done.** T2 corpus manifests and a harness-only `corpus fetch` (AQP:215, AQP:219-227). T2a and T2b are accepted by GROK2: 49 repositories, 5 multi-repo workspaces, 33 independence families (T2R:24). It includes the FW-14 inputs (COV:8125-8145).<br>**Carried out of T2:**<br>- only 10 held-out families exist (T2R:296), which bears on the gating bar (B2);<br>- aws-cdk and aws-sdk-rust exceed the 4 MiB canonicalizer limit for the tree digest, so K1a may need a chunked digest (ON, "M3-T2b sent"). | — | none; **D3 sign-off pending** (AQP:543; B3) | M | O1, D3, D9, D15, FW-14 |
| M3-Q0 | **Accepted, r13** (HD:3): the case model (AQP:138-143), the label ledger (AQP:257-271), the confidence rule (AQP:241-245), the exploratory envelope (AQP:438-444), the D12 runner, and the rule-catalog draft specs (AQP:175-199). **K2 is sized at 16 days** (HD §13). | — | D13 and D2 sign-offs (AQP:542, AQP:554); D12 (AQP:553) | M | Q1–Q8 definitions |
| M3-S | **S-P, feasibility probe:** can the pinned toolchain host the `rustc_driver` sidecar? Can Node and TypeScript load from a closure path? It is labelled preliminary and makes no Q6 claim.<br>**S-M, the measured INC-7 spike:** one-shot startup, sealing and replay costs on medium T2 (AQP:408), from a throwaway harness outside the product. S-M is a lead run set, queued on the machine (P5-8). ML2 item 9 names the figures SM-1 to SM-10 it must deliver, with SM-10 in the platform's native unit, labelled, and SM-5 and SM-6 also reporting `snapshot2`'s bounds.<br>**Launch boundary:** S-P and S-M are lead-run throwaway tooling over public, pinned T2 bytes. They are not the product supervisor. They execute no repository code: no build script, proc-macro or package script. Their samples are labelled preliminary, and they make no production or confinement claim.<br>**Status (r7):** neither has started. Every run set P5-8 puts ahead of S-M is done, X4-F1's confirmation workspace lane on `15c0779` included (1749 passed, 0 failed), and E0 is complete. P0's phase 2 lanes hold the machine now (ON, "Confirmation lane on product main `15c0779`", "E0 complete"). | S-P: — . S-M: T2a (met), Q0 envelope (met), D13 sign-off. D12 for Q6-labelled samples (AQP:553-554). | none | M | INC-7, Q6 |
| M3-CF | **Confinement work for O7** (see "O7").<br>- **CF-P, the confinement-feasibility probe: done** (CFP; arch `70ab22c71`). A lead trial with a trivial test child, no provider and no repository bytes. On macOS 27, Seatbelt through `sandbox_init_with_parameters` is feasible, with five amendments to MD F-3, a `kern.procargs` sysctl denial among them. The AL2023 desk check is feasible on kernels 6.1.147, 6.12.40 or 6.18 and later; earlier builds lack Landlock and disclose (CFP "Verdict (macOS 27)", "Linux desk check"). It claims nothing as enforced, and it met the D law's gate (MD G1).<br>- **CF-1 and CF-2** (MD SD-1 and SD-4), the successors, start once O7 is decided. CFP "What CF-1 must still measure" lists CF-1's first measurements. | CF-P: done. CF-1/CF-2: O7. | SL S10 and S6 successor (CF-1); AQ §5 item 4 and DR-128 disposition; disclosure-carrier successor (CF-2) | L | G09, G21, G29, G30 (AQ:344); O7 |
| M3-L | **M3 provider-protocol and reuse law. r3 in review with Grok** (ML3; `reviews/grok-provider-protocol-l-r3`). r2 (ML2) drew one required finding, RF-1: item 13's "closed set" of provider-wire identities omits members that NE's OpenUniverse payloads and HelloAcks carry, and J1:192 cites that sentence (`reviews/grok-provider-protocol-l-r2`). **r3** lists every wire identity per protocol in item 13, joins FA-2 in a new item 22, makes FA-2 gate item **G10**, and gives item 5 an exception for E1's syntax stage and H's inventory derivation (X-H4). It adds cross-law items X13 to X16 (ON, "FA-2 and M3-L r3 written"). r1 (ML1) was never sent; its draft request is `SUPERSEDED-UNSENT`.<br>**Review and effect, the early-review rule (lead decision; ON, "Lead decision: M3-L gets an early review round"; ML2 "Review and effect"):** L is reviewed now. An ACCEPT is recorded as "accepted in review", and L takes effect only when every gate item is met. Filling every ⟨SM-n⟩ from S-M, and any change O7 forces, go through a delta round with the same reviewer. A dependent's "M3-L accepted" means **L in effect** (P7-1). **Rejected:** holding all review until the owner items close.<br>It carries:<br>- INC-1 to INC-8 (AQP:389-409), with TS2/Rust3 unchanged (INC-5; BP:716-717) and one child per universe with no reuse (F02:222, F02:269); syntax universes have no child (ML2 item 2);<br>- O1(a) and the S-OP-4 record join (OPP §3.6, §9);<br>- RequestId as correlator and phase-lawful identities (OPP §3.1);<br>- the provider-side two-stage cancel (OPP §5.5); the commit-phase join is J1's (ML2 items 16f, 18);<br>- a reference to the D law, which alone owns the launch rules under O7;<br>- a record correcting DR-G10's selector (REG:355 against COV:4671).<br>**Findings:** changed-scope reuse needs an identity-contract (D5a IE) successor, the **INC-1 successor**, before it can ship; nothing ships at M3 (ML1:180-188; ML2 X1). **The Rust3 stage-1 cancel grace is 5,000 ms** (RPP:119); TS2 uses D3's provisional 2 s (ML1:453-455; MD item 14).<br>**r2's lead decisions the owner may reverse:** the review rule; stderr is counted and never held (item 12.1); TypeScript's `host-shutdown` cancel reason is never sent at M3 (item 16b).<br>**Acceptance gate:** S-M, complete T2 (T2b), Q0, D3, D13 and the D2 draft, S-OP-2 drafted, O1, **O7 decided**, and **FA-2 accepted (G10, P7-2)**. The S-OP-4 join is the law's content, not a gate item. Status is in "M3-L gate status". | the gate (G1–G10) | **law** (r3 in review); D5a successors only if an INC needs one (AQP:546); S-OP-4; FA-2 (in review with Codex) | L | G10, G21; INC-1..8; O1, O7 |
| M3-P0 | **Package scaffolds:**<br>- `crates/components` and `crates/syntax` (CH14:284, CH14:288) as members;<br>- the provider source layout;<br>- dependency-policy rows, including MC item 12's inflater row.<br>One inventory successor, so that parallel lanes don't race the linear chain. **Unblocked:** X9-6 and the licence unit are integrated.<br>**Status (r7): phase 1 ready, phase 2 started** (ON, "P0 phase 1 ready", "Confirmation lane on product main `15c0779`"). It is inventory v135 (parent v134): `crates/components` and `crates/syntax` as members, each a doc-comment-only `lib.rs` with no dependencies or modules, and `tools/host/dependency-policy.json` with C's item-12 inflater rows (miniz_oxide 0.9.1 and adler2 2.0.1, selected but not linked). **Lead decisions, accepting the drafter's recommendations:** the provider source layout is unchanged, because the directories exist and CH14 says not to create empty files; no checker for the new policy until C3a links the crate; `forbid(unsafe_code)` on `crates/syntax`, which holds under T-native through the `tree-sitter` crate's safe API and which E2b may revisit. Like every unit that touches `crates/contracts` or `crates/identity`, it runs both dependency checkers in its Python lanes (M2C §5 row 20). Every D, E2a, H1 and J2a code unit waits for it (MD "Units after the law"; ME item 20; MH item 25; MJ item 14). | X9-6 (met); licence unit (met) | inventory successor | S | — |
| M3-B | **Configuration and discovery. Law r2 accepted by GROK2** (MB). Units (MB:839-849):<br>- **B-S1** (design, M): successor S3, the SL S3 and NE §1.4 passages, SLS V3 schemas and the reader registry, with MC's SX-1 (`.opensip/` is never source). **Accepted by GROK2 (ACCEPT-DESIGN-UNIT) and bound at product `9c11c53`** (ON, "B-S1 accepted by GROK2"; `reviews/grok2-b-s1-r1`).<br>- **B-S9** (design): S9's `CONFIG.INVALID` remedy text, **split out of B-S1 by lead decision** (ON, "B-S1 and B-S2 drafted"). It is a complete successor copy of the two native-model files, so no `verify_design` successor (VD2) is needed. **Accepted by Grok (ACCEPT-DESIGN-UNIT) and bound at `8adfe0c`** (ON, "B-S9 accepted by Grok"; `reviews/grok-b-s9-r1`). Residual hazard (BS9 LD-4): a later unit could override a superseded copy's other lines, and only review catches that.<br>- **B-S2** (design, S): successor S4, IE `vcs-observation` schema 3. **Accepted by Codex (ACCEPT-DESIGN-UNIT) and bound at `240a795`** (ON, "B-S2 accepted by Codex"). Its one observation goes to C1b.<br>- **B1-a** (M) and then **B1-b** (M): the resolver, `resolvedConfigDigest` (IE:518), FW-13, and the carriers with X2 r9 item 3a. **B1-a now depends on B-S9**, not "B-S1 (S9 text)" (MB:841; BS9 "What it is"; GROK2's B-S1 review). **All three B design units are bound,** so B1-a, B2-a and B3-b are unblocked on their successors and wait for P0 and L (ON, "B-S9 accepted by Grok").<br>- **B3-a** (S): `grants.rs` with the four authorization records. X4b's `admit_repo_execution_grant` is **not** built at M3: it goes to M5-EX (M2C §5 row 14).<br>- **B2-a** (M), **B2-b** (L), **B2-c** (L) and **B2-d** (M): the shared rule; the S3 downward instrument with the **discovery ledger profile**; the native unit instrument U-0..U-9; host-side recognition (NE:2750).<br>- **B3-b** (L): D15 members through X2 r9 item 6b. **B3-c** (M, harness): the FW-14 outputs.<br>**GROK2's ruling R2 on B-S1:** MB item 22 and item 24 row 1 govern a crossing into a repository; item 24 row 3 is not applied to an explicit or config member. Row 3 gets a record correction in M3-B's next revision (`reviews/grok2-b-s1-r1/REVIEW.md`, "Rulings").<br>**Discovery caps (MB item 12).** The platform caps of 65,536 objects and 131,072 edges cannot hold T2's large repositories. A discovery-only ledger profile raises them, provisionally to 2^20 objects, 2^21 edges and 2^30 bytes (MB:336). A T2 census margin test (≥ 2×) guards the caps, and a failure returns them to the law. Exhaustion is `WORK.BUDGET_EXHAUSTED`, never truncation.<br>**D15's value at M3 is bounded** (MB F2–F4). There is no cross-unit resolution, and links are honoured only after S5 and S6. | P0, L; X2 r9 (S1) and X12 r4 (S2) **accepted**; B-S9 (bound) before B1-a; B-S1 (bound) before B3-b; SX-1 (bound) before B2-a | **law** (accepted); successors S1 X2 r9 (accepted), S2 X12 r4 (accepted), S3 (B-S1, bound), S4 (B-S2, bound), S9 (B-S9, bound), S5 (C3), S6 (C2), S8 (T2 record); S7 is S-OP-5's; a record revision for row 3 | XL | FW-01, FW-13, FW-14, D15; 6 `inventory/*` cells; 7 flags; SL:3, NE:2 (§1.4), NE:9 |
| M3-C | **Sealed snapshot and Plan. Law r7 accepted in review by CODEX2** (MC, `a1ee9386…`; `reviews/codex2-snapshot-plan-c-r6`, `-r7`), with no findings. It takes effect once M3-L is in effect; X12 r4, the gate's other item, is accepted (MC "Acceptance gate"; ON, "M3-C r7 accepted in review"). **r6 applied E1's two cross-law items:** X-C1 (lead decision: the core provider closure also produces syntax-universe work, and is a `semanticClosures` member exactly when a syntax universe is selected) and X-C2 (C4a builds the syntax-only `clones-near` census). C4a's acceptance carries their Plan legs (MC "r6 changes"). **r7** narrows row 8 to a selection among the component manifests admitted at J1's R10a (SD-6; MJ S19; MC "r7 changes"). C1a and C1b are unblocked on their successors and wait for P0 and L (ON, "B-S9 accepted by Grok").<br>Units (MC "Units"):<br>- **C1a** (M): `snapshot.rs`, the capture session, walk, custody, sealing and bounds (IE:179). **C1b** (S): the VCS observation; it carries B-S2's observation (ON, "B-S2 accepted by Codex"). **C1c** (S): the `node_modules` read set.<br>- **C2a** (M): closure admission and the core role closures. **C2b** (hard XL part, 5 days): the TS context and universe resolver and the layout. **C2c** (M): the Rust context functions. C2 covers NE:1255-1645 and BP:699-713.<br>- **C3a** (L): `imports.rs`, DS-1..DS-6, CRATE-ARCHIVE-1 (NE:1646-1698). **C3b** (S): the unified-features adapter, a tool launch under the D law, after D1's primitive and O7. **C3c** (M): prepared import under PO-0..PO-4 (NE:1803-1870).<br>- **C4a** (L): `plan.rs`, with `plan2` (IE:182), the prospective-Plan bounds (NE:4276), and r6's syntax stages and census. **C4c** (S): prepared-import wiring (variant B). **C4b = X12d** (M, plus one serialized X9 lead set; X12:192).<br>- H-DEP, H-NM, H-PREP (S each): harness recipes on the K lane.<br>**Asked of C by M3-H (r1, kept by r2; in review):** X-H3, a third admitted use of the core provider closure as producer of host inventory records in every universe, which the lead routes to **M3-C r8 and CRC-2**, before C4a (ON, "CRC-1 and CR-1 written"); X-H6, a subject-scope field in S-B; and a record correction at MC:874 (MH "Cross-law items", "Record corrections").<br>**Large repositories (MC item 5; O-3).** `snapshot2`'s 4 MiB descriptor holds about 27,000 rows. **S-R**, inventory by reference, is likely needed after S-M. It is conditional and unsized (see "Unsized"). | B (C1a: B2-c; C4a: B1-a, B2-c, B2-d), L in effect, I1 (C4a: I1-c; X12d: I1-c and I1-b2), D1 (C3b), X3a-2 (C1a). **Successor gates:** CRC-1 and CR-1 before C2a (both written; in review with GROK2 and CODEX2); SX-1 (bound) before C1a; VCS-1 before C1b; NIJ-1 before C3a; R3 before C3c; X12 r4 (accepted) before C4a; the X-H3 widening, M3-C r8 and CRC-2, before C4a (MH, in review; ON). | **law** (r7 accepted in review); X12d; CRC-1, CR-1, NIJ-1, VCS-1, SX-1 (bound), S-B, T2-DEP, X12-A; S-R conditional | XL | NE:3, NE:4; L-RS1, L-RS4 |
| M3-D | **Supervisor and common control. Law r3 accepted by GROK2** (MD, `9679dbc4…`; `reviews/grok2-supervisor-d-r3`). **Section F, confinement, is an O7 placeholder,** binding only if O7 is decided as recommended; everything outside it is ordinary law (MD header). Units (MD "Units after the law"):<br>- **D1a** (M): `platform/process.rs`, the spawn primitive on both platform families (items 1–8). It is the M6 DR-G22 owner (BP:1026), built early.<br>- **D1b** (L, O7): `apps/launch/` (`opensip-launch`), the F-2 and F-3 profiles and the availability probe; the O7 confinement primitive. No claim before CF-1.<br>- **D2a** (M): `control_protocol.rs`, CC v5. **D2b** (L): `provider_protocol.rs`, the CBOR reader and handshake checks; NE:10's dispatch (NE:2781-3316) with no translation (F02:168-169).<br>- **D3a** (L): `supervisor.rs`, the state machine, settlement, constants, liveness, bounds, stderr (counted, never kept), discard and records. **D3b** (M): tree kill, the cancellation and fault ladders, revocation, harness coexistence.<br>- **D4** (M): `manifest.rs` at J1's **R10a**, `session_factory.rs` and the request predicates: DR-G29's refusals before any **analysis-attempt** ExecutionId is drawn (REG:374; MD item 24).<br>- **D5** (L, harness): the G21 controls of OPP §10, plus three **new** escape controls (a network attempt, a write outside scratch, an ambient environment read) that extend S-OP-11; F-7 after CF-1.<br>**Constants (MD item 14):** Rust3's stage-1 grace is the protocol's 5,000 ms; TS2's is 2 s, provisional; liveness 5 s, raised to at least 2 × SM-8; TERM to KILL 1 s; reap ceiling 10 s, or 5 s under revocation.<br>**Successors (MD item 29):** SD-1 = CF-1; SD-2, the control select-tuple record (with D2a); SD-3, the launcher's closure rows (before D1b); SD-4 = CF-2; SD-5, J1's projections of D's internal refusals (J1's S20; not yet written); SD-6, J1's row R10a (**accepted** in J1 r4).<br>**Lead decisions the owner may reverse** (ON, "Lead decisions in M3-D r2"): Linux provider scratch in `/var/tmp`; a macOS group `SIGSTOP` deferred to CF-1; SD-6 as a J1 amendment. | Code units: P0, L in effect. D1b: D1a, O7 as recommended, SD-3. D3a: D2a, D2b, O1 (S-OP-2's registry). D4: D3a, SD-2, SD-6 (accepted), S19 = C r7 (MJ S19; accepted in review). D5: D3b, D4; CF-1 for F-7. | **law** (accepted) | XL | G10 (control), G21, G29; NE:10 |
| M3-E | **Syntax crate and grammar registry. Law E1 r3 accepted by Codex** (ME; `reviews/codex-syntax-e-r3`).<br>- **E1, law:** the backend choice (CH14:614); the `SyntaxGrammarBundleV1` closure (BP:684-688); seven languages, eight grammar rows and fourteen suffixes (NE:260-263); NE:2's syntax-only part.<br>- **The backend (lead decision, ME items 1–3):** two predeclared branches, T-wasm (tree-sitter grammars compiled to Wasm and run in-host by `wasmi`, with fuel-metered, typed parse failures) and T-native (tree-sitter linked natively), chosen by E0. **E0 chose T-native** (below).<br>- **Units (ME item 20):** **E0** (S, 2 days, probe); **E2a** (M, SYN-LANE); **E2s** (M, 2 days, **new in r3**): applies SYN-1 and SYN-1F to the product's schema sources, evaluator registries and the closed eight-output generation registry, by exact selector; **E2b** (L): `grammar.rs`, `parser.rs`, SYN-REG and SYN-DEP; **E2c** (L): `normalization.rs`, `candidates.rs`, SYN-NS; **E3** (M): `host/syntax.rs` (CH14:496).<br>- **The second-integrator rule (ME item 20):** for each join E3 shares, the unit that integrates second owns the final wiring and its end-to-end controls: H (day 22) for syntax views, facts and Coverage; C4a (19) for X-C1 and X-C2's Plan legs; J2 (25, now J2b) for the host capture into `ExecutionInputsV1`. E3 builds against the **accepted H law's** syntax-join interface.<br>- **E0: complete; the outcome is T-native** (E0R "Outcome"; ON, "E0 complete"). It pinned wasi-sdk-34, tree-sitter v0.27.0, the rust v0.24.2, typescript v0.23.2 and javascript v0.25.0 grammars, and `wasmi` 2.0.0. P1–P4 and P6 pass; P3 found byte-identical trees on both legs for 8,351 of 8,351 files. **P5 fails:** the median per-file throughput is 0.818 MiB/s against the 1.0 floor. **Lead decision under E1's predeclared rule (ME item 3):** syntax uses native tree-sitter linked in the host, with `executionModel` `native-linked-v1`, and item 18's fallback posture applies: parser defects are a declared residual risk, and the lead re-decides placement at M4 before CLI `analyze` takes untrusted input. The result is inside the predeclared branches, so E1 is not reopened. Under T-native, E2a shrinks to the definition records over the crate archives and E2b uses the `tree-sitter` crates; **the units do not change** (ME item 20). **GROK2 accepted the report** in record review, with no required findings, and E2a can start once P0 lands (ON, "E0 report accepted by GROK2"; `reviews/grok2-e0-report-r1`).<br>The crate is pure (BP:676-680). | E0: — . E2a: E0, P0. **E2s: SYN-1 and SYN-1F accepted.** E2b: E2a, C2a (CR-1, SYN-1's keys). E2c: E2b (SYN-NS). E3: E2c, C1a, B2-c, **E2s**. | **law** (accepted); SYN-1, **SYN-1F**, SYN-NS (contract successors); SYN-REG, SYN-DEP and SYN-LANE inside E2a/E2b; CR-1 (C's); LP-1 (M4) | XL | G13 (syntax); 11 `*/syntax-only` cells; NE:2 (syntax), NE:7 |
| M3-I1 | **The X12c preview pack. Law r2 accepted by CODEX2** (MI). It covers the frozen rule IR of `module-import-cycle`; the policy-language successor with one atom, `cycle-representative`, one finding per cyclic component; the identity-contract passages that authorize that one additive op value under the existing majors (LD-3); and the pack contract. Units (MIU:28-33):<br>- **I1-L** (design, M): **accepted by CODEX2 (ACCEPT-DESIGN-UNIT) and bound at product `0ceb9ad`** (ON, "I1-L accepted by CODEX2"). Lead decision LD-L1: the four JSON schema changes are complete successor copies carrying their parents' bound overrides, as 468a did (ON; I1L "Lead decisions"). Its observation I1-L-NB-01 goes to I1-b2's fixtures (`reviews/codex2-i1-l-r1`).<br>- **I1-P** (design, S): **accepted at r2 by CODEX2 (ACCEPT-DESIGN-UNIT) and bound at `cd5958b`** (ON, "I1-P accepted at r2"; `reviews/codex2-i1-p-r2`). r1 drew one required finding (`reviews/codex2-i1-p-r1`). Both I1 design units are bound, so the product chain starts once the machine queue reaches it.<br>- **I1-a** (M), **I1-b1** (S), **I1-b2** (L), **I1-c** (S).<br>Edges: I1-L → I1-P; I1-L → I1-a → I1-b1 → I1-c; I1-b1 → I1-b2 (MIU:35-38); F8b → I1-a. Downstream: **I1-c → C4a; I1-c and I1-b2 → X12d; I1-b2 → J2b** (MIU:40; MC "Units"). Forbidden substitutes apply (X12:196-202).<br>**I1's record items** are in "New units and successors (r7)". | I1-a: I1-L (bound), X9-6 (met), F8b (bound); the generator order of P5-3 and P7-4. I1-c: I1-P (bound), I1-b1. | X12c contract successors (I1-L and I1-P bound) | L | G25 path; X12c |
| M3-F | **TS/JS provider (TS2).**<br>- **F1, transport:** NE:2944-3002 and NE:3151-3316.<br>- **F2, facts:** imports, references, calls, unresolved edges, types (NE:2347), symbols and Coverage, across three modes. **Symbol Coverage needs a carrier** for the provider's symbol census: FA-2 (MH X-H1, in review; P7-2). F2 owes FA-2's emission duty.<br>- **F3:** reachability and framework recognition (L-FW1), syntax facts, and NE:7's clone modes including cross-tsjs (NE:2562-2647).<br>- **F4, runtime closure:** signed Node and TypeScript with no ambient Node (F02:252), running under the O7 profile.<br>Code can be authored earlier; a provider is **launched** only after O7 and D1b's primitive. **F1's first run on TS T1 fixtures waits for K2a's oracle freeze** (HD §13, QD-26). | Authoring: C1, C2, D2. **F1 integration: C1a, C2b, D3** (MC, narrowed). Launch: D1b, D3, O7. F2's symbol Coverage: FA-2. | none expected (BP:717); FA-2 is a negotiated payload successor (MH) | XL | G10, G13, G14 preparation; 33 TS/JS cells; NE:7, NE:10 frames |
| M3-G | **Rust provider (Rust3).**<br>- **G1a:** snapshot transport and `context.rs`.<br>- **G1b:** dependency and prepared frames (NE:2872-2943).<br>- **G2:** `compiler_adapter.rs`, the `rustc_driver` sidecar (`12-architecture-completion-goal.md:145`) with the rust-dev-llvm closure (NE:1445). It is **authored** after S-P. **G2-v** is its lawful launch and validation under the O7 profile, after O7 and D1b. It is not D1's enforcement claim, which needs CF-1.<br>- **G3:** inventory, facts and Coverage for L-RS1..L-RS3 (NE:1793). Symbol Coverage needs FA-2 (MH X-H1, in review).<br>- **G4:** prepared-mode consumption (L-RS4, PO-1..PO-4) and NE:7's clones. Rust3's `maxPreparedOutputEntries` of 256 may bound prepared transport (ML2 X12; MC X-3).<br>**Rust3's 256-subject request cap (ML3 X13; in review).** RPP puts every non-empty `.rs` file of the sealed snapshot into each Rust stage's subject list and refuses before spawn above `maxSubjectsPerStage` 256, which Rust3 checks by exact equality in Hello. By the T2 manifest, 9 of the 22 Rust repositories exceed it, tokio (808) and axum (301) among them, so a product Rust provider could not analyze them. S-M's throwaway harness is not bound by it. **Lead recommendation:** raise or remove the cap in a Rust3 limit successor before G3 ships, measured by S-M (ON, "New finding, important for the owner's Rust use"). | **G1a: C1a, C2c, D3** (MC, narrowed). G1b: G1a, C3a–C3c. G2 authoring: S-P. **G2-v: O7, D1b.** G3: G1a, G2-v; FA-2 for symbol Coverage; the Rust3 limit successor before it ships (lead recommendation). G4: G3, G1b, C4c. | none expected (BP:717) | XL | G10, G13, G14 preparation; 22 Rust cells; NE:7, NE:10 frames |
| M3-H | **Fact admission. In review with Grok; r3 is written and queued after L r3** (ON, "M3-H r3 written"). r2 (MH2; `reviews/grok-fact-admission-h-r2`) drew one consistency finding: items 10, 14.4 and 22 routed the same keys differently. **Lead direction for r3, which r3 applies with new control H-C25:** item 14.4's table is the sole routing authority; anchors take row 30 only; Coverage keys take row 30 or 32 by NE cause, with a tie rule; a provider's terminal Coverage counts as provider-origin; keys match by prefix token (ON, "M3-H r2: Grok raised one consistency finding"). r1 (MH) drew one required finding, RF-1: the anchor byte checks were placed before any view exists, so a bad provider anchor had no check that both calls the owner and takes the producer-boundary row (`reviews/grok-fact-admission-h-r1`). **r2** keeps the anchor checks with their owner, run once over a provisional view in a staging overlay and routed by the key and the view's origin, adds control H-C24, and rebuilds item 10 so that the owner's view join decides Coverage (ON, "M3-H r2 written and sent to Grok").<br>Scope as r6: the syntax, context, occupancy and Coverage joins (`fact_admission.rs:1-3`); relation-registry and Coverage-domain refusals (REG:368); a missing rung is indeterminate (REG:370); framing grants no fact authority (CH14:482). H admits what I1-b2 reads (MI item 8), and hands the full `admit_enumeration` its inputs in J2b (MC item 16, C2-R1).<br>**Proposed units (MH item 25):** **H1** (M) candidates; **H4** (S) occupancy; **H2** (M) Coverage and views, with closed world wired after FA-1; **H3** (M) inventory: symbol-census owner admission and the host-derived inventories, which **H absorbs because no unit owned them** (X-H5; lead decision, MH item 18); **H5** (L) the stage wiring and the end-to-end and second-integrator controls. **Only H5 is on the host chain:** it is r6's H row (3 days, day 22). H1–H4 run off the chain, after D2b.<br>**Proposed successors (MH "H. Successors"):** FA-1, FA-2, the X-H3 widening (M3-C r8 and CRC-2), the S-B scope field (X-H6), and L r3's wording (X-H4). H answers MD F7 (clean non-Complete terminals discard candidates and admit the terminal Coverage; MH item 4). | r6: C4a; E3 or F1. **Proposed H5:** C4a, F1, E3, D3, H1–H4; FA-2 (symbol-scope legs), the X-H3 widening (inventory leg), S-B (large scopes), SYN-1 and E2s. | **law** (in review) | L | G23, G25; NE:5 |
| M3-J | **Guarded durable host pipeline.**<br>- **J1, law: accepted.** r3 by CODEX2 with no required findings (`reviews/codex2-host-pipeline-j-r3`); **r4** by GROK2 (`reviews/grok2-host-pipeline-j-r4`), which adds row **R10a** (SD-6) and corrects item 11's `repair recover` record (MJ "r4 changes"). It is the X11 successor, the invocation DAG, J-BS (S13) and the S-OP-12 join (item 8). **No analysis word is wired in the binary at M3** (item 1). J-BS and S18 still need their own ACCEPT-DESIGN-UNIT reviews.<br>- **Units (MJ item 14):** **J2a** (M): `invocation.rs` and `outcomes.rs`, pure. **J2b** (L): `analysis.rs`, the shared analysis core, mode-agnostic. **J2c** (M): the ephemeral entry end to end; its output wiring waits for S18. **J3a** (L): `RequestIdentity`, `ExecutionIdReservations`, the durable entry and the S2–S7 code. **J3b** (L): the X3d r9, X4 r8, X7 r7 and X5 r4 code and rows S12-B, -C, -U, -D. **J3d** (L): the durable pipeline end to end, J-BS and `workflow_tests.rs`; its output wiring and S12-O wait for S18. Each J unit that touches `crates/security`, `crates/storage` or `host/src/finalization.rs` reruns both lead sets on its integration commit, serialized (MJ item 12).<br>- **J1's successors (MJ item 13):** S2 L468 r6, S3 X1 r2, S4 L464 r3, S5 X3A r6, S6 X4B r6, S7 X2 r10, S7b (joins owed by B, C and trust), S8 X5 r4, S9 X7 r7, **S10 X3d r9**, S11 X4 r8, **S12 X9 r17**, S13 J-BS, S16 S-B, **S18** (the final-output-section passage successor), **S19 = M3-C r7**, **S20 = SD-5's record**. S17 is this record.<br>- **J-RW, law** (P5-1): **r2 in review with Codex** (JRW). r1 drew three required findings (`reviews/codex-resume-repair-jrw-r1`), and r2 two P2 findings: the schema cookie wraps at 2³² (R2-01), and N-T2 splits at the native open (R2-02). **r3 is being written.** Lead direction on R2-01: keep C-LEDGER, scoped to OpenSIP writers, with a product-SQL census control; rejected, withdrawing C-LEDGER (ON, "J-RW r2: Codex raised two P2 findings"). It completes each L11 crash state inside the next admitted durable write, at its owning law's own step and under that owner's lock; nothing is deleted; any state that is not exactly a known crash prefix keeps its refusal (ON, "J-RW r1 written", "J-RW r2 written").<br>- **J4** (L plus one serialized lead set): J-RW's code unit, outside J1. **Proposed sub-units (JRW item 11):** J4a (M) shared primitives; J4b (M) registration; J4c (S) the ledger; J4d (S) trust; J4e the rows and one serialized lead set. L11 is retired only when J4e's lead set passes every RW row.<br>- **X3c r8, law: accepted by GROK2** (X3C; `m2/reviews/grok2-ledger-blob-x3c-r8`), no findings. A re-commit is a new attempt of the same Run that adds its own attempt rows and stages no availability or pins. **X3c-3** (M, storage code, plus one serialized lead set) follows, by day 25 (X3C item 13). | J2a: P0, J1. J2b: J2a and the J2 set: H, C4a, C4c, X12d and its lead set, D3, CF-2, I1-b2, X4-F1 (integrated), X4-F2; provider stages need O7 and D1b; closure selection needs S19. J2c: J2b, S3, S7b; S18 for output wiring. J3a: J1, S2–S7, S10 (item 2). J3b: J3a, S8–S12. **J3d: J2b, F2, G3, J3a, J3b, X3c-3 and its rows, O1, S13, S16, S18.** J4: J-RW. X3c-3: X3c r8, X9 r17's RC section. | **law** (J1 accepted); J-BS; **X3c r8** (accepted); **J-RW** (in review); S-OP-12 (J1 item 8) | XL | G25; NE:11, NE:14, NE:15; FW-03, FW-08; WS:2 |
| M3-I2 | **Draft catalog, non-authoritative.** `PolicyDocumentV2` rules (AQP:173-199), evaluated only in the harness over admitted facts (AQP:500). The product pack stays at M5 (D2, AQP:542). I1-L's reference model is the harness oracle for `module-import-cycle` (MI item 8). | H, Q0 | none at M3 | M | Q2–Q4 exploratory |
| M3-K | **Quality harness and T1** (HD §13).<br>- **K1:** K1a (M) is the case and ledger libraries, digests, the freeze, `corpus fetch` and the store. It may need a chunked tree digest. K1b (S) is the confidence module. K1c (M) is the run driver and determinism driver (AQP:324-327).<br>- **K2:** T1 in three lanes, 57, 6 and 3 cells (AQP:500; AQ:233-234), **16 days**. K2b (Rust, 5) and K2c (syntax, 3), each with its one-day review and freeze, run **before day 0**: 10 days after Q0. K2a (TS/JS, 5) and its freeze run on **days 0–6**. Each lane's oracle is frozen before any producer runs on that lane's T1 fixtures (QD-26). | Q0 (met), T2b (met) | D13 | XL | Q1, Q4, G13 |
| M3-M | **Exploratory measurement and the dogfood checkpoint:** Q1/Q4 on T1; Q2–Q4 through I2; the determinism suite; Q6 core analysis kept separate from first use and from preparation-invalidating edits (AQP:359-366); T3, now that the licence has landed (AQP:555; D6 at AQP:547). T3's multi-repo instance waits on OQ-1 (MB item 27). **This plan's rule, not AQP's:** the exploratory report may close while adjudication of gating and repair-eligible findings is still pending. Those strata are reported as not yet adjudicated. Strata with too few findings are INSUFFICIENT-EVIDENCE (AQP:244). Any later Q2 use still requires every such finding adjudicated (AQP:236), with unclear labels resolved by the human expert (AQP:254). Large T2 repositories that refuse at `snapshot2`'s bound before S-R are reported as refused (MC O-3). | J3 (J3d), G4, F3, E3, I2, K1, K2, O1 | none | L | Q1–Q6 exploratory |
| M3-O | **Operability.**<br>- **O1:** `tracing`, the S-OP-2 vocabulary, nonpersistent sinks, the bounds, phase spans and the operational record with INC-8's reuse disclosure (OPP §3.1-§3.3, §4.1), plus the enforcement checks (OPP §7). **S-OP-2 is accepted at r6, so O1 now waits only on P0** (ON, "S-OP-2 accepted at r6 by Codex"). D3a consumes S-OP-2's registry through O1 (MD "Units after the law"), and J3d needs O1 (MJ item 14).<br>- **O2, each part gated:** S-OP-1, S-OP-7, S-OP-8, S-OP-5 and S-OP-6. **Lead rule:** M3-X requires each O2 part whose successor is accepted by then. A part whose successor is not yet accepted is recorded as carried to M4. M3-X is not held for it.<br>- **O3:** the G20/G21 controls (OPP §10, plus D5's escape extension). It follows D5, so it now finishes on day 16. | P0; S-OP-2 (accepted) | S-OP-1, -2 (accepted), -5, -6, -7, -8, -11 (OPP §9) | L | G21; G20 controls (M5 row, BP:1024) |
| M3-R | **Third-language readiness review** with Python, and the onboarding kit (AQP:467-489). ME's PY-REG row is the Python registry template (ME item 19). | L, F2, G3, K2 | record only | M | O8, D9 |
| M3-X | **Exit gate.** BP:887's completion checks on this host's profile: the seven gates prepared, both languages present, and the O7 implementation in place. | M3-M, B3-c, D4, D5, E3, F4, CF-2, **J2c** (P7-3), J4 (and its X9 rows), O1, O3, R; O2 parts per the O-row rule; X4-F1 (integrated) and X4-F2 (through J2b) | none | L | all M3 gates |

**M2 carry-ins: owners, sizes and gates (r7).**

| Item | Source | Owning unit | Size | Must land | Status (r7) |
|---|---|---|---|---|---|
| **F8b**, the generator-closure and TS lane-registry re-pin | M2C §5 row 2; F8B | M2 follow-up (lead; CODEX2 reviewed the law, Grok the unit) | M, plus its machine steps | before I1-a and X4T-c | **done:** bound at `e093e90` (77 contract successors) (ON, "F8b accepted and bound"; `m2/reviews/grok-generator-closure-f8b-unit-r1`) |
| **X4T-c**, two continuation codes | M2C §5 row 15 | contract successor plus regeneration | M | after F8b; one regeneration at a time with I1-a and E2s (P5-3, P7-4) | unblocked on F8b (ON, "F8b accepted and bound"); no review of its successor is recorded |
| **X3a-2**, read-side adoption of the selected endpoint | M2C §5 row 13; X3a r5 items 4, 8 | post-M2 unit | M (inventory successor) | before C1a, so by **day 10** | not started (no ON entry) |
| **X4b**, `admit_repo_execution_grant` | M2C §5 row 14 | B3-a (`grants.rs` records only) and M5-EX | — at M3 | not an M3 code item | deferred (lead decision) |
| **X4-F1**, observer reread expiry (a real defect) | M2C §5 row 16 | X4T-a successor | M, plus full lanes and one lead run set | before J2 (J2b), so by **day 22** | **done: accepted by GROK2 and integrated at `15c0779`** (`m2/reviews/grok2-observer-expiry-x4f1-r1`). Its lanes passed on `e093e90`, and its X9 regression (64 storage and 4 host rows, two sets each) is byte-identical to the X9-6 evidence. The integrated diff equals the reviewed subject. **Lead decision:** no full two-target matrix run at integration; the confirmation workspace lane on `15c0779` then passed, 1749 passed and 0 failed (ON, "Confirmation lane on product main `15c0779`"). GROK2's rulings: the evaluation instant is tEval plus elapsed time, and the fenced read's own `EV-CLOCK` is outside this unit (ON, "X4-F1 is ready for review", "X4-F1 accepted by GROK2 and integrated") |
| **X4-F2**, the same expiry gap in the fenced read | M2C §5 row 23 | X4T successor | provisional M plus one lead set | before J2 (J2b) | no draft recorded |
| **F9**, test fixture dates that expire on 2026-12-30 | M2C §5 row 24 | test-only unit | provisional S | by **2026-12-01** (calendar) | no draft recorded |
| **Resume/repair writer** (L11) | EXIT:186-191; M2C §4.1, §5 row 10 | **J-RW** (law) and **J4** (code), with the X2, X3c, X4T, **X3b and registry owners** (P5-1, r7) | law ≤ 5 days; J4 L plus one lead set | J-RW before day 0; J4 before M3-X | J-RW r2 in review with Codex: two findings; r3 being written |
| **X3c successor** (re-commit) | EXIT:171; M2C §5 row 11 | **X3c r8** (law) and **X3c-3** (storage code) | law done; X3c-3 M plus one lead set | before J3d, so by **day 25** | **X3c r8 accepted** by GROK2 (ON, "X3c r8 accepted by GROK2") |
| X11 successor | X11:64-81; M2C §5 row 7 | J1 | — | J law | **J1 accepted** (r3, r4) |
| X12c / X12d | X12:191-192 | I1 / C4b | L / M plus a lead set | — / before J2b | I1-L and I1-P bound; C r7 accepted in review |
| Licence unit | AQP:555 | **done**: L1, `2967905` (v134) | — | — | — |

**Why these splits.**

- **B and C:** discovery answers to SL S3 and D15's successor; the snapshot answers to identity.
- **C, split by its law (MC "Units"):** C1, C2 and C3 have three sub-units each, and C4 has C4a, C4c and C4b. C4a still binds every input of `plan2` (IE:182), and the host owns resolved inputs before the PlanId (NE:2497-2499). C4c only wires prepared imports, so non-prepared Plans need not wait for C3c.
- **C3 and G1b/G4:** the host admits dependency and prepared sets (NE:1704-1712); the provider consumes them.
- **G1a and G1b:** splitting the snapshot frames from the dependency frames lets the Rust transport start on C1a instead of waiting for C3.
- **D, split by its law (MD "Units after the law"):** the spawn primitive (D1a) is apart from the O7 confinement primitive (D1b), so that only D1b waits for O7. The codecs are apart, and supervision (D3a) is apart from tree kill and cancellation (D3b).
- **J, split by its law (MJ item 14):** the pure invocation code (J2a) and the security, storage and finalization code (J3a, J3b) run before or beside H, off the host chain, which leaves J2b → J3d on it. The ephemeral entry (J2c) is separate because its output wiring waits for S18.
- **I1's product units:** I1-c (the row) feeds C4a. I1-b2 (the semantics) feeds X12d and J2b. Under LD-11, I1-c may land before I1-b2, because the op stays a structural refusal until then (MI §9).
- **I1 and I2:** I1 is a mandatory input of every real Plan (X12:125, X12:134; `policy.rs:1401`). I2 is exploratory only.
- **CF:** O7's successors have different owners from supervision (REG:317).
- **J-RW and J4 apart from J3:** L11's crash states are made by M2 code (first registration, owner creation, the ledger's WAL), not by J3. The writer needs those owners' successors, not the durable pipeline.
- **H and J4, as proposed (in review):** MH item 25 puts only H5 on the chain. JRW item 11 runs J4a and J4c in parallel, then J4b and J4d, then J4e's lead set.

## New units and successors (r7)

Found tonight. Each row gives an owner, dependencies and a size where the source states one. "Not stated" means the source gives no size; the plan's successor-law bound (about 3 rounds, at most 5 days; "Critical path") then applies.

| Item | What | Source (standing) | Owner | Depends on / needed before | Size |
|---|---|---|---|---|---|
| **FA-1** | A native passage successor to NE §10's fault law (NE:3849-3850). On a clean non-Complete terminal, the candidates before the terminal are discarded and its exhaustive terminal Coverage is admitted (X-H2). It also adds `native.coverage-closed-world-mismatch` to NE:3529's producer-boundary row. ACCEPT-DESIGN-UNIT. | MH "H. Successors", X-H2 (in review) | native owner | needed before H2's closed-world wiring. H's item 4 needs nothing: it applies the retained selectors. | not stated |
| **FA-2** | **The provider symbol-census carrier** (X-H1), a native contract successor. **Written and in review with Codex** (FA2; `reviews/codex-fa-2-r1`). Its carrier is the optional capability token `symbol-census-v1`: under it, the existing Analyze and Complete payloads of TS2 and Rust3 each gain one member, `symbolCensus`, within the current majors, as `target-attribution-v2` did. The request key commits to the census rule, an empty-subject scope; the terminal entry commits to the census values; only NE:3279's "equals the requested key" gains an exception, for symbol keys. It also closes an inherited DLV/RPP request-key rule that conflicted with NE §4.1a for every key (ML3 X15). ACCEPT-DESIGN-UNIT. | MH "H. Successors", X-H1; ON, "M3-H r1 written" (lead decision: draft FA-2 with L r3 before day 0), "FA-2 and M3-L r3 written"; ML3 G10, item 22 (in review) | native owner; protocol owners (DR-G10); M3-L | **M3-L gate item G10 (P7-2; ML3).** Needed before D2b's payload codec (day 2), F2, G3, H3's provider leg, H5's symbol-scope legs, and J2b's TS and Rust path. Its follow-ups for H, C, D2b, F2, G3 and this plan are ML3 X16. | not stated |
| **The X-H3 widening: M3-C r8 and CRC-2** | A third admitted use of the core provider closure: producer and enumerator of the three inventory relations' records in **every** universe, and a `semanticClosures` member whenever an inventory cell is requested. C2-T13 and C2-T13a extend to match, and C4a's `exec-plan2` gains one host inventory stage per universe. MH r1 and r2 call it "C r7 / CRC-1"; C r7 is now the SD-6 amendment, and CRC-1 carries only C's existing law, so the lead routes X-H3 to **M3-C r8 and CRC-2** (lead decision; H r3 follows). | MH "H. Successors", X-H3 (in review); ON, "M3-H r1 written", "CRC-1 and CR-1 written", "M3-H r3 written" | C's owners; identity (CRC-2) | before day 0, or at the latest before C4a starts (day 16); H3's TS and Rust inventory leg; H5 | not stated |
| **B-S9** | S9's `CONFIG.INVALID` remedy text, as complete successor copies of the two native-model files (the 468a and I1-L form). It binds on today's `verify_design`, so no VD2 is needed. | ON ("B-S1 and B-S2 drafted", "B-S9 goes to Grok", "B-S9 accepted by Grok"); BS9; `reviews/grok-b-s9-r1` — **accepted and bound at `8adfe0c`** | lead (M3-B successor S9) | before B1-a, so by day 0: **met** | not stated (S9 sat inside r6's B-S1, M) |
| **SD-5, with S20** | J1's item 10 rows, existing codes only, for the internal refusals the D law assigns to J1's projection: R10a's and ER10a's `ExcludedForm`, `MemoryBudgetBelowCeiling`, `ToolOutputBound`, `ToolScratchBound` and `confinement-refused`. It is the public route for R10a's refusal. **Not yet written,** and it must stay distinct from matrix row 27 (ON). | MD item 29 (SD-5); MJ item 13 (S20); ON, "J1 r4 and M3-C r7 written" | lead (J1's author) | J2a's projection of those refusals; J3d's R10a wiring and J2c's ER10a wiring, each with D4. Lands with J2 (MD). | not stated (record) |
| **S19 = M3-C r7** | Item 16's row 8 narrowed to a selection among the component manifests admitted at R10a or ER10a. It adds no admission. The core role closures are not component manifests and are unchanged. | MJ item 13 (S19); MC "r7 changes" — **accepted in review by CODEX2**, effective with L | the M3-C author (lead) | D4's integration; J2b's closure selection: met once L is in effect | a narrow amendment |
| **S20** | see SD-5 | MJ item 13 | lead | — | — |
| **X3d r9** | J1's S10: 8.1 and 8.6, with the latch window closed only where a `StoppedSession` is produced; the `refused()` record; item 2's ExecutionId reservation at `open`. Plus X3c r8's CL-1, a record restatement of X3d item 4 step 3.8: availability and pins are staged only on a Run's first commit in (S, N). | MJ item 13 (S10); X3C item 16 (CL-1) | the X3d owners (security, storage); the lead writes it (MJ "The X3D and X7 owners' assent") | J3a (item 2), J3b | not stated |
| **X3c r9** | J-RW's X3c text (RW-S3) on r8's accepted bytes: C-ACL for the store directories; the length-0 ACL-omitted file and L-UNC with its schema-cookie clause as resumable creation states; `LEDGER.CORRUPT` narrowed; items 12a and 13 and the partial-ledger forbidden substitute. None of r8's re-commit clauses changes. | X3C item 16 (CL-4, CL-5); JRW RW-S3, LD-11 (in review) | storage | lands once J-RW is accepted; gates J4a and J4c | not stated |
| **X9 r17 record** | One record revision with three independent sections, each transcribed when its unit is ready, none changing another's rows:<br>- **S12-** (J1): rows S12-B, -C, -U, -D, and -O once S18 is accepted; and the re-transcribed host drivers F01, F12, F16, F17, F32, F39 and F40 (host halves);<br>- **RC-** (X3c r8): RC-1 to RC-9, the census child, and the record of the 19 runs;<br>- **RW-** (J-RW, in review): RW-F00, RW-D1, RW-K1 to K10, RW-N1 to N12 and RW-B.<br>Whichever of X3c-3 and J4 integrates second reruns both sections' rows. | MJ items 12, 13 (S12); X3C items 13, 16 (CL-2); JRW X-RW-10, RW-S6 (in review) | lead | RC before X3c-3; S12 before J3b's review, S12-O before J3d's O wiring; RW before J4e | not stated (record) |
| **M3-B record revision** | MB item 24 row 3 corrected under GROK2's ruling R2 on B-S1: item 22 and item 24 row 1 govern; row 3 is not applied to an explicit or config member. B1-a's dependency reads B-S9. | `reviews/grok2-b-s1-r1/REVIEW.md` "Rulings" R2; ON, "B-S1 accepted by GROK2"; BS9 "What it is" | lead (M3-B's author) | — | record |
| **E1's record items** | From E0, for E1's next revision or for E2a and E2b: ERROR's symbol 0xFFFF needs an explicit exception to item 10 and A11; item 4's closure layout omits the wasm headers (moot under T-native, E0R); the grammar and runtime commits are now pinned by E0. E0's own lead decisions are also owed downstream: E0's `SyntaxTreeV1` byte layout is probe-only, and E2a fixes the normative one; `wasmi` compiles everything up front, an E2b obligation if T-wasm returns. E0R adds observations for E2a: the supertype symbol type, and the host crate count. | ON, "E0 phase 1 is ready", "E0 complete"; E0R "E1 record items and observations" | lead (E1's author) | E2a, E2b | record |
| **I1's record items** | From I1-L, for I1's next revision: the anchor imprecisions; five more passages that enumerate the closed op set (IE:1266, IE:1334, IE §4's predicate table, COMP:109, and the PDS and PPDS descriptions); WS's selected effective copy (WSE); and the item 2.3 and 2.5 choices that fix proof bytes, which I1-L's precisions P0–P7 settle. **For I1-a** (`verify_design`): a 468a-form record carrying its new admission registry, re-pointed source maps, and the moved line references. **For I1-b2's fixtures:** I1-L-NB-01, cases that discriminate the new precision branches. | ON, "I1-L and I1-P written", "I1-L accepted by CODEX2"; I1L "Deviations" 2, 4, 5, 7, 9 and "For I1-a"; `reviews/codex2-i1-l-r1` | lead (I1's author); I1-a; I1-b2 | I1-a; I1-b2 | record |
| **D's record items** | For D's next revision: D4-T1 and D4-T2 sample at R10a's return; "first use" also covers `LostRace` and `NotPristine`; SD-6's "MC r5" citation; SD-5 is still unwritten. MH (in review) adds that D's next revision cites MH item 4 for MD F7. | ON, "J1 r4 and M3-C r7 written"; MH X-H2 | lead (D's author) | D4 | record |
| **H3** | `fact_admission/inventory.rs`, MH items 17 to 19: symbol-census owner admission; the host-derived file and package inventories and inventory facts; origin tags. **H takes the host-produced inventory records that no unit owned** (X-H5; lead decision, MH item 18). | MH item 25 (in review) | M3-H | H1; FA-2 for the provider leg; the X-H3 widening for the TS and Rust inventory leg | **M, 2 days**, off the host chain |
| **H1, H2, H4, H5** | The rest of H's proposed units (see the M3-H row). H5 is r6's H row. | MH item 25 (in review) | M3-H | as in the M3-H row | H1 M, H2 M, H4 S, H5 L |
| **J4a–J4e** | J-RW's proposed sub-units of J4 (see the M3-J row). | JRW item 11 (in review) | M3-J | J-RW and RW-S1 to RW-S6, each gating only its own sub-unit; J4e also RW-S6 | M + M + S + S, plus the lead set |
| **Rust3 limit successor** (ML3 X13) | A Rust protocol successor that raises or removes `maxSubjectsPerStage` 256, which 9 of the 22 T2 Rust repositories exceed. It changes the Hello-checked limits map, so it cannot be a host change (ML3 item 1). It sits beside SM-6's possible TS2 limit successor. | ON, "New finding, important for the owner's Rust use" (lead recommendation); ML3 X13, R12 (in review) | the Rust protocol owner | before G3 ships, measured by S-M (lead recommendation); not an M3-L gate item | not stated |
| **SYN-1F** | The foundation successor beside SYN-1: `source-parse-error` enters the five foundation `NativeCause` copies, by selector. | ME item 19 | identity and execution-input owner | reviewed beside SYN-1; both before E2s | design unit |
| **SD-2, SD-3** | SD-2, the control select-tuple record (`analyzer`, provider id, major). SD-3, the launcher's closure rows (DR-G14 and DR-G22 rows, a CH14 entry for `apps/launch/`). | MD item 29 | SD-2: the manifest owner, with D2. SD-3: release, platform and security owners. | SD-2: D2a, D4. SD-3: D1b. | design units |
| **J1's other successors** | S2 L468 r6, S3 X1 r2, S4 L464 r3, S5 X3A r6, S6 X4B r6, S7 X2 r10 (shared with J-RW's RW-S1), S7b, S8 X5 r4, S9 X7 r7, S11 X4 r8, S13 J-BS, S16 S-B, S18. | MJ item 13 | as MJ names them (security, storage, host, workflows and identity owners; the lead writes the M2 laws' amendments) | J3a (S2–S7), J3b (S8–S12), J2c (S3, S7b, S18), J3d (S13, S16, S18) | not stated |
| **J-RW's other successors** | RW-S2, registry owner selection v3 (a record); RW-S4, X3b r11; RW-S5, X4T r12 with an X4B r6 note; RW-S8, a J1 record revision. | JRW item 12 (in review) | the registry owner; security and journal; trust; lead | J4b (RW-S2), J4a (RW-S4), J4d (RW-S5) | not stated |

## Cross-law items (r7)

Each item from tonight's laws is routed once. "Here" means this record takes it up.

| Item | From | To | r7 records |
|---|---|---|---|
| X9: the sending order and day 0 | ML2 (in review) | here | "M3-L gate status" replaces `M3-PLAN-r6.md:445` and `:426`; P7-1 |
| X9, "also stale": the O7 risk line | ML2 | here | "O7", "Risk" now carries CF-P's outcome |
| X10: six laws cite L r1 by line | ML2 | MC, MJ, SOP2, ME, MB and MD, at their next revisions | ML1 preserves the lines; each re-pins by item; no content change |
| X11: OPP's "held in memory" stderr and its `supervision.no_progress` name | ML2 | OPP's next revision | none here |
| X12: Rust3's `maxPreparedOutputEntries` of 256 | ML2; MC X-3 | the Rust protocol owner (ML2 R10; MC R4) | the M3-G row notes it |
| RF-1: item 13's closed identity set | Grok's L r2 review | L r3 (in review); then J1's next revision re-cites item 13 at J1:192 (ML3 X14) | the M3-L row |
| X13: Rust3's 256-subject request cap | ML3 (in review); ON | the Rust protocol owner (R12) | the G row; new-units table; "Risks"; "Owner decisions" |
| X15: inherited request-key commitment rules against NE §4.1a | ML3 | the native owner, through FA-2 | the FA-2 row |
| X16: FA-2's follow-ups: H (item 17's provider leg, symbol D, item 11's pre-Analyze entries, H-C17), C (the TS and Rust enumerator is the universe's provider closure; a worker for every universe an expected symbol inventory binds; the Plan-time token need), D2b (four payload versions), F2 and G3 (emission duty, signed capability rows), and this plan (G10 and the pre-day-0 round) | ML3 (in review) | H, C, D, F, G; here | G10 (P7-2); "Critical path"; the rest goes to those laws' next revisions |
| X-H1: no symbol-census carrier | MH (in review) | FA-2, with L r3 | G10 (P7-2); the F, G and H rows |
| X-H2: clean non-Complete terminals | MH | FA-1; MD's next revision cites MH item 4 | the new-units table |
| X-H3: no lawful producer for host inventory records in TS and Rust universes | MH | M3-C r8 and CRC-2, before C4a (lead decision; ON, "CRC-1 and CR-1 written") | the C row; the new-units table |
| X-H4: L's "no fact without a producing frame" | MH | L r3 ("no admitted provider frame or Plan-selected in-core producer stage") | the M3-L row |
| X-H5: nobody produces the inventory capability's records | MH | here (M3P-H): H3 takes them. `vcs-change@vcs-reported` stays open for C and the native owner | the H row; "Risks" |
| X-H6: the subject-scope bound after execution | MH | C's S-B successor | the C row; "Risks" |
| M3P-H: H's units, the X-H items, FA-2 and the X-H3 widening as pre-day-0 rounds | MH | here | recorded as proposals (P7-5) |
| H's record corrections: MC:874's ":107-111" reads ":108-111"; MJ row 36's reach | MH | C's next revision; J2a | none here |
| X-RW-1, X-RW-2: explicit recovery and the marker in place | JRW (in review) | REG's record (RW-S2); X2 (RW-S1) | the new-units table |
| X-RW-3, X-RW-5: the schema-less ledger; leftovers | JRW | X3c (RW-S3, X3c r9); X2 (RW-S1) | X3c r9 row |
| X-RW-4: the dependency rule | JRW | X4T r12 with an X4B record (RW-S5) | the new-units table |
| X-RW-6: L465 item 5's reach | JRW | owner flag | "Owner decisions" |
| X-RW-7: P5-1's owner list omits X3b and REG | JRW | here (RW-S7) | P5-1 |
| X-RW-8: `repair recover` | JRW | J1 | done in J1 r4 |
| X-RW-9, X-RW-11, X-RW-12 | JRW | none: no conflict | — |
| X-RW-10: X9 r17 is shared | JRW | X9 (RW-S6) | X9 r17 row |
| CL-1: X3d item 4 step 3.8 | X3C | X3d r9 | X3d r9 row |
| CL-2: the RC section | X3C | X9 r17 | X9 r17 row |
| CL-3: never replace a ledger holding committed rows | X3C | J-RW, which already meets it; any later J-RW revision keeps it | — |
| CL-4, CL-5: J-RW's X3c text; X3c item 2 against X3b's empty-database rule | X3C | X3c r9, after J-RW is accepted | X3c r9 row |
| M3P-E: E's units, the second-integrator rule, X-C1 and X-C2, item 18's M4 entry condition | ME | here | the E row; "Choices left open" |
| X-C1, X-C2 | ME | C | done in C r6 |
| S17: J's units, "J1 fixes the order", M3-C's "J1 chooses" items | MJ | here | the J row; "Choices left open". MJ item 15 answers M3C:115 → 5.4a, M3C:188 → 5.4b, M3C:291, :557, :571 → 5.4c, and M3C:854 → J-η |
| S19, S20 | MJ | C r7; SD-5 | the new-units table |
| F8: M3P's "network namespace" | MD | here | "O7": seccomp, not a network namespace |
| F9: D's unit sizes and lane | MD | here | the D row; the timing table; "Lanes" |
| F7: facts before the terminal | MD | H | answered by MH item 4 (in review) |
| F13: AL2023's `/tmp` is a size-limited tmpfs | MD | any unit placing large temporary data on Linux | "Risks" |
| SD-6 | MD | J1 r4 (accepted) and C r7 (accepted in review) | done; S19 |
| Ruling R2: MB item 24 row 3 | GROK2's B-S1 review | M3-B's next revision | new-units table |
| B-S2's observation | Codex's B-S2 review | C1b | the C row |
| E1's record items | E0 (ON) | E1's next revision, E2a, E2b | new-units table |
| I1's record items | I1-L (ON; I1L) | I1's next revision, I1-a, I1-b2 | new-units table |
| SM-10's unit | SOP2 item 23 | L | answered in ML2 item 9 |

## Critical path and parallel lanes

**Day 0 is M3-L in effect** (P7-1): L accepted in review, every gate item G1 to G10 met, and every delta round accepted (ML2 "Review and effect"). Because O7, S-M and FA-2 are in L's gate, all three are done by then.

**Assumed done before day 0** (not sized here):
- **Laws and successors:**
  - the D law (**accepted**, r3; its gate, CF-P, met), the E law (**accepted**, r3), the J law (**accepted**, J1 r4), X3c r8 (**accepted**), the H law (in review; r3 queued) and J-RW (in review; r3 being written);
  - the B law (accepted) and its successors X2 r9 and X12 r4 (**accepted**), and B-S1 with SX-1, B-S2 and B-S9 (**all bound**; B1-a needed B-S9 on day 0);
  - **FA-2**, with L r3 (gate item G10); both are in review (Codex and Grok);
  - **the X-H3 widening of C (M3-C r8) and CRC-2** (MH item 25; in review at this record's cut-off): before day 0, or at the latest before C4a starts on day 16.
  - X12 r4 lands with B1-a (MB item 25), which starts on day 0; it is accepted, so this is met.
- **P0 landed.**
- **I1's product units,** or at least I1-c by day 16 and I1-b2 by day 19 (below). Both I1 design units are bound.
- **G2 authored.**
- **K2b and K2c,** with their freezes.
- **X3a-2 and X4-F2,** or by their bounds in the carry-in table. X4-F1 is integrated (`15c0779`).

**Bounded by their first consumer, not by day 0:** SYN-1 and SYN-1F (E2s, by day 12 at the latest); SD-2 (D2a) and SD-3 (D1b); J1's S2–S7 and S10 (J3a), S8–S12 (J3b), S3, S7b and S18 (J2c), S13, S16 and S18 (J3d); S19, M3-C r7 (D4 from day 8; J2b), now accepted in review; SD-5 with S20 (J2a's projection of D's refusals); X9 r17's sections (X3c-3, J3b, J4e); J-RW's RW-S1 to RW-S6, each gating only its own J4 sub-unit (JRW item 11). Each sits off the host chain with the slack shown below.

**The C law takes effect at day 0.** C r7 is accepted in review, and MC's gate makes it effective once L is in effect, X12 r4 being accepted. The DAG tolerates:
- CRC-1 and CR-1 by **day 5**, since C2a must start by day 5 for C2b to finish before C1c at day 12;
- SX-1 by day 2: **met**, bound with B-S1 at `9c11c53`;
- VCS-1 and NIJ-1 by day 12;
- R3 by day 15;
- C r7 (S19) before D4 starts on day 8: **met** at day 0;
- the X-H3 widening by day 16 (MH, in review).

**Durations are planning assumptions:**
- a code sub-unit takes 1 day for S, 2 for M, 3 for L and 4–5 for a hard XL part, including build, review and integration;
- a successor law takes about 3 rounds, bounded at 5 days;
- one lead run set at a time, 1 day each where a unit needs one;
- edges are **integration** edges (MC "Units").

**r7 timing (variant B; MC "Units").** Rows that differ from r6 are marked **r7**. Only accepted laws re-time rows (P7-5).

| Sub-unit | Days | Integration after | Finishes (day) |
|---|---|---|---|
| B1-a → B1-b | 2 + 2 | — (B-S9; X12 r4) / B1-a | 2 / 4 |
| B3-a; B2-a | 1; 2 | —; — (SX-1, bound) | 1; 2 |
| B2-b → **B2-c** → B2-d | 3 + 3 + 2 | B2-a, B1-b, B3-a / B2-b / B2-c | 7 / **10** / 12 |
| B3-b → B3-c | 3 + 2 | B2-c (B-S1, bound) / B3-b, K1a, S8 | 13 / 15 |
| C2a → C2b; C2c | 2 + 5; 2 | — (CRC-1, CR-1) / C2a; C2a | 2 / 7; 4 |
| C1a | 2 | B2-c (SX-1, X3a-2) | 12 |
| C1b; C1c | 1; 1 | C1a (VCS-1); C1a, C2b | 13; 13 |
| C3a | 3 | C1a (NIJ-1) | 15 |
| C3b | 1 | C3a, D1's primitive (**r7:** D1b, day 5; O7 by day 0) | 16 |
| C3c | 2 | C3a (R3) | 17 |
| C4a | 3 | C1b, C1c, C2b, C2c, C3a, C3b, B1-a, B2-c, B2-d, I1-c (X12 r4; the X-H3 widening, in review) | 19 |
| C4c | 1 | C4a, C3c | 20 |
| X12d (C4b), then its X9 lead set | 2, then 1 | C4a, I1-b2 | 21, then **22** |
| CF-1 → CF-2 | ≤ 5 + 2 | O7 (≤ day 0) / CF-1 | ≤ 5 / ≤ 7 |
| **r7:** D1a; D1b | 2; 3 | —; D1a (O7 as recommended, SD-3) | 2; 5 |
| **r7:** D2a ∥ D2b | 2 ∥ 3 | after D1a, as MD's timing runs them | 4; 5 |
| **r7:** D3a → D3b | 3 + 2 | D2a, D2b, O1 / D3a | 8 / **10** |
| **r7:** D4; D5 | 2; 3 | D3a (SD-2, SD-6, S19); D3b, D4, CF-1 | 10; 13 |
| E0 → E2a | 2 + 2 | — / E0, P0 (both may finish before day 0) | ≤ 0 |
| **r7:** E2s | 2 | SYN-1 and SYN-1F accepted | ≤ 0; at the latest 12 |
| E2b → E2c → E3 | 3 + 3 + 2 | E2a, C2a (CR-1, SYN-1) / E2b (SYN-NS) / E2c, C1a, B2-c, **E2s** | 5 / 8 / 14 |
| F1 → F2 → F3 | 3 + 4 + 3 | C1a, C2b, D3 (launch: D1b, O7; first T1 run: K2a's freeze) | 15 / 19 / 22 |
| F4 | 2 | F1, D1b | 17 |
| **r7:** G2-v (launch and validation under the profile) | 1 | D1b (O7 by day 0) | **6** |
| G1a → G1b | 3 + 2 | C1a, C2c, D3 / G1a, C3a–C3c | 15 / 19 |
| G3 → G4 | 5 + 3 | G1a, G2-v / G3, G1b, C4c | 20 / 23 |
| H (MH's H5) | 3 | C4a, F1 (and E3, D3, H1–H4, all earlier) | 22 |
| I2 | 2 | H, Q0 | 24 |
| **r7:** J2a | 2 | P0, J1 | 2 |
| **r7:** J3a, then its lead set | 3, then 1 | J1, S2–S7, S10 (item 2) / serialized after X3c-3's and J4's sets | 3, then 5 |
| **r7:** J3b, then its lead set | 3, then 1 | J3a and its set, S8–S12 | 8, then 9 |
| **r7:** J2b → J3d | 3 + 3 | J2a, H, X12d and its lead set, C4c, D3, CF-2, I1-b2, X4-F1, X4-F2, S19 / J2b, F2, G3, J3a, J3b, X3c-3 and its rows, O1, S13, S16, S18 | 25 / 28 |
| **r7:** J2c | 2 | J2b, S3, S7b (S18 for its output wiring) | 27 |
| X3c-3, then its X9 rows | 2, then 1 | X3c r8 (accepted), X9 r17's RC section | 2, then 3 |
| J4, then its X9 rows | 3, then 1 | J-RW (≤ day 0) | 3, then 4 |
| K1a → K1b → K1c | 2 + 1 + 2 | Q0, T2b (both met; it may run before day 0) | 2 / 3 / 5 |
| **K2 (T1, three lanes; HD §13)** | 16: 10 before day 0 (K2b, K2c and their freezes), 6 on days 0–6 (K2a and its freeze) | Q0 | **6** |
| O1; O3 | 4; 3 | P0 (S-OP-2 accepted); O1 and D5 | 4; **r7: 16** |
| O2 parts | successor-gated | each S-OP | carried to M4 if unaccepted (O-row rule). **O2_selected** is the latest finish of the O2 parts the O-row rule keeps in M3, or 0 when none is kept. |
| R | 2 | F2, G3, K2 | max(20, K2) + 2 = 22 |
| M3-M | 3 | J3d, G4, F3, E3, I2, K1, K2, O1 | max(28, K2) + 3 = 31 |
| M3-X | 2 | M3-M, B3-c, D4, D5, E3, F4, CF-2, **J2c**, J4 and its rows, O1, O3, R, O2_selected | max(M3-M, R, 27, O2_selected) + 2 = 33 |

In r6 the third term was 17 (F4). It is now 27, J2c's finish (P7-3); M3-M's 31 still dominates.

**Conditional host-chain duration: 33 days, unchanged.**

> B1-a → B1-b → B2-b → B2-c → C1a → C3a → C3b → C4a → H → J2b → J3d → M3-M → M3-X

That is 2 + 2 + 3 + 3 + 2 + 3 + 1 + 3 + 3 + 3 + 3 + 3 + 2 = 33. J2b and J3d are r6's J2 and J3 under J1's names (MJ item 14). A second branch has zero slack: C4a → X12d → its X9 lead set → J2b, reaching J2b on day 22, the same day as H.

It holds only if all of the following hold, in addition to the day-zero assumptions above:
- **K2** finishes by day 28. Q0 gives 6, so this holds by construction unless K2a's freeze slips (next item).
- **K2a's freeze** slips by at most 10 days: M3-X = 33 + max(0, *s* − 10), for a freeze slip *s* past day 6. F1 starts on day 12, so the freeze has 6 days of margin. H then waits for C4a until day 19, which gives F1 4 days of slack. Q0's r4-era rule, 26 + max(0, *s* − 3), is superseded.
- **O2_selected** finishes by day 31. The late branches are compared by their **arrival at M3-X**: max(28, K2) + 3 against O2_selected.
- **X12d's X9 lead set** is complete by day 22, with no other lead run set holding the machine on days 21–22.
- **r7, J3d's waits (MJ item 14):** F2, G3, J3a, J3b, X3c-3 and its rows, O1 and S18 all finish by day 25, J2b's last day. Each is planned well before it. If one is late, J3d waits for it day for day, and the path runs through it.
- **r7, D3 by day 12:** D3 now finishes on day 10, and F1 and G1a start on day 12.
- **r7, H r1's conditions (MH item 25; in review):** FA-2 and the X-H3 widening are accepted before day 0, or at the latest FA-2 before D2b starts (day 2) and the widening before C4a starts (day 16). P7-2 puts FA-2 in L's gate, so it holds at day 0 by construction.

**What moved in r7, and what did not.** Only accepted laws moved rows.
- **D (MD "Units after the law"):** D's five rows become eight sub-units. D3 finishes on day 10 (r6: 7), D4 on 10 (9), D5 on 13 (10), and D1's confinement primitive, D1b, on 5 (r6's D1: 2). So G2-v moves from day 3 to 6, and O3 from 13 to 16. D's own reading agrees: "The critical path (33 days) is unchanged."
- **E (ME item 20):** E2s is added, before day 0 or by day 12 at the latest. E3 stays on day 14. E0 chose T-native, which shrinks E2a but changes no unit (ME item 20; E0R).
- **J (MJ item 14):** J2 becomes J2a, J2b and J2c, and J3 becomes J3a, J3b and J3d. J2b and J3d keep r6's J2 and J3 days (25 and 28). J3a's and J3b's lead sets fall on days 5 and 9. J2c finishes on day 27.
- **Did not move:** the 33-day host chain; K2 by 28; O2_selected by 31; X12d's lead set by 22 with zero slack; E3 (14); H (22); F1 and G1a (15); F2 (19); F3 (22); G3 (20); G4 (23); R (22); M3-M (31); the K2a slip rule.
- **Not re-timed (P7-5):** H r1's H1–H5 and J-RW r2's J4a–J4e. Both fit r6's rows: H5 is r6's H row, and H1–H4 finish by day 9 against D2b's day 5. J4's rows land by day 5 at this plan's durations; if J-RW's breakdown is accepted, J3a's set moves to day 6, inside its slack.

**Branch slack:**
- C4c finishes on day 20 and J2b starts on day 22: 2 days.
- **r7:** D3 (10) has 2 days against F1 and G1a, which start on day 12.
- F1 (15) has 4 days against H, which starts on day 19.
- I2 (24) has 4 days against M3-M, which starts on day 28.
- **r7:** J2c (27) has 4 days against M3-X, which starts on day 31.
- The Rust branch has 5 days: G3 (20) against J3d, which starts on day 25, and G4 (23) against M3-M.
- F2 (19) and F3 (22) have 6 days.
- C2b (7) has 5 days against C1c.
- B2-a has 2 days and B3-a has 3 against B2-b.
- **r7:** G2-v (6) has 9 days against G3, which starts on day 15.
- R (22) has 9 days. E3 (14) has 14. B3-c (15), O3 (16), F4 (17), D4 (10), D5 (13), J3a's set (5), J3b's set (9), J4's rows (4) and X3c-3's rows (3) have more.

**Why 33, and not 26, 28 or 31.**
- **r4's 26** used one-row C units and B2 finishing on day 5.
- **MC r2's 28** split C, but kept r4's B rows. Its figure reproduces under those rows: CODEX2 confirmed the 29/28-day figures (`reviews/codex2-snapshot-plan-c-r2`, C-R4 disposition).
- **MC r3** expresses the chain as **b + 23 days**, where b is the day B2-c finishes (MC "Units").
- **b = 10** from MB's accepted unit table at this plan's durations: B1-a (2) → B1-b (2) → B2-b (3) → B2-c (3). B2-b waits for B2-a, **B1-b** and B3-a (MB:845).
- **MB's F14 says "about day 8"** (MB:803). That counts B2-a → B2-b → B2-c (2 + 3 + 3) and omits B2-b's integration edge on B1-b, which MB's own table states. At b = 8 the chain would be 31.

**Variants and rejected alternatives:**
- **Variant A, C4 unsplit:** C4a also waits for C3c, so it finishes on day 20, and the chain runs through C3c: **34 days**. Rejected (MC's recommendation, adopted as P5-6).
- **Rust context minting inside C2c,** waiting for C3b: **30 days in both variants at b = 5** (MC r3, C2-N1), so 35 here. Rejected in MC.
- **Full C1/C2 rows as F1 and G1a edges:** F1 and G1a finish on day 16, F2 on 20, G3 on 21 and G4 on 24, all inside slack. 33 is unchanged.
- **J4 after J3,** as in r4, at J4's r5 size: J3 (28) → J4 (31) → its rows (32) → M3-X **34**. Rejected (P5-1).

**I1 and F8b bounds.** F8b is bound (`e093e90`), before day 0, so its bound is met. The I1 product chain does not wait for P0 or L (MIU: I1-a depends on I1-L and X9-6; r6 adds F8b). If it is late, it moves nothing as long as I1-c lands by day 16 and I1-b2 by day 19, X12d's start. I1-a now waits only for its turn on the generator lane and the machine (P5-3, P7-4). I1-P is bound, so I1-c waits only for I1-b1.

**The whole-M3 total is left uncomputed.** These are still unbounded:
- the O7 decision date, which is outside the lead's control;
- the parallel pre-day-0 law and successor rounds, each bounded at 5 days but contending for reviewers: L r3 and FA-2 (in review), H r3, J-RW r3, the X-H3 widening (M3-C r8 and CRC-2), CRC-1 and CR-1 (in review), and the successors in "New units and successors (r7)";
- the pre-day-0 machine queue: P0's phase 2 lanes now, then S-M (P5-8) and the I1 product chain;
- the O2 parts;
- S-R, if S-M shows it is needed.

K2 is not on this list: Q0 bounds it.

**The bounded pre-day-0 work:**
- T2 and Q0: **done**;
- CF-P: **done**;
- F8b: **done** (bound at `e093e90`);
- K2b and K2c with their freezes (10, from Q0's acceptance);
- P0: phase 1 **ready**, phase 2 (lanes, then its review) running;
- S-M (2), a lead run set, next under P5-8;
- S-P (1), then G2 authoring (4);
- E0: **done** (T-native); then E2a (2, after P0) and E2s (2, after SYN-1 and SYN-1F);
- X4T-c (2) and the I1 chain (I1-a 2, I1-b1 1, I1-c 1, I1-b2 3), one regeneration at a time with E2s;
- X3a-2 (2);
- X4-F1: **done**, integrated at `15c0779`, and its confirmation workspace lane passed;
- L in effect (about 2, once its gate is met).

Recompute the total when O7 is decided, when L takes effect (if any unit changes), after S-M, when H and J-RW are accepted (if their breakdowns change a row), if S-P fails, and if S-R becomes needed.

**Calibration only:** M2's exit integrated 62 product commits from `d4239a5` to `3e64266`, 60 of them up to C (`git rev-list --count`; M2C §3.2). Those were mostly smaller mechanism units.

**Effort.**
- **About 72 law, successor or record units** (r6: 39):
  - **r6's 39:** the laws L, B, C, D, E, H, J, J-RW and I1; the amendments X2 r9, X12 r4 and X3c r8; the successors CF-1, CF-2, backup-status (J-BS), S-OP-1/2/7/8/12 and D13; and the contract successors and records B-S1, B-S2, S5, S6, CRC-1, CR-1, NIJ-1, VCS-1, S-B, T2-DEP, X12-A, I1-L, I1-P, S8, SYN-1, SYN-NS, F8b and X4T-c.
  - **21 named by accepted laws tonight:** J1 r4; J1's successors L468 r6, X1 r2, L464 r3, X3A r6, X4B r6, X2 r10, X5 r4, X7 r7, X3d r9, X4 r8, X9 r17, S18, C r7 (S19) and SD-5 with S20 (MJ item 13); SD-2 and SD-3 (MD item 29); SYN-1F (ME item 19); X3c r9 (X3C CL-4); B-S9; and M3-B's record revision.
  - **9 proposed by drafts in review or by tonight's lead decisions:** FA-1, FA-2, M3-C r8 and CRC-2 (MH; ON); registry owner selection v3, X3b r11, X4T r12 and a J1 record revision (JRW RW-S2, RW-S4, RW-S5, RW-S8); and the Rust3 limit successor (ML3 X13; ON).
  - **3 record revisions owed:** D's, E1's and I1's record items.
  - S-R is conditional. LP-1 is an M4 record (ME item 19).
- **About 92 code, harness or probe sub-units** (r6: 76):
  - r6's 76, with D at 8 sub-units (r6: 5), E at 6 (E2s added) and J at J2a, J2b, J2c, J3a, J3b and J3d (r6: J2 and J3), giving **84 from accepted laws**;
  - plus the proposals of drafts in review: H1–H5 for r6's one H row (+4) and J4a–J4e for r6's one J4 row (+4).

That is roughly 164 reviewed units, against r6's 115. Most of the growth is the D, J and E laws' own unit tables and J1's successor list. M5-EX is M5 work.

**Lanes:**

| Lane | Units | Reviewer (suggested; actual so far) |
|---|---|---|
| Host core (the critical path) | B → C → H → J | B: GROK2 (law; B-S1), Codex (B-S2), Grok (B-S9). C: CODEX2 (r6 and r7 accepted in review). H: Grok (r1 and r2 one finding each; r3 queued). C's successors: CRC-1 GROK2, CR-1 CODEX2 (in review). J1: CODEX2 (r1–r3), GROK2 (r4). |
| Protocol | L, with FA-2 | L: Grok (r2 one finding; r3 in review). FA-2: Codex (in review). |
| Components and confinement | D, CF, F1/G1 conformance | D law: GROK2 (r3 accepted; MD F9). CF-P: lead-run record. |
| Rust compiler | S-P → G2 → G3 → G4 | CODEX2 |
| Syntax and TS analysis | E → F2/F3/F4 | E1 law: Codex (r3 accepted). E0 report: GROK2 (accepted). Code: GROK2. |
| Preview pack and M2 carry-ins | F8b → X4T-c, I1-a and E2s on the generator lane → I1-b1 → I1-c, I1-b2; X3a-2; X4-F1, X4-F2; X3c r8 → X3c-3; J-RW → J4; F9 | I1: CODEX2 (I1-L and I1-P accepted). F8b: CODEX2 (law), Grok (unit). X3c r8: GROK2 (accepted). J-RW: Codex (r2 in review). X4-F1: GROK2 (accepted). |
| Quality and operability | K1, K2 lanes, I2, O, R, M3-M | S-OP-2: Codex (r6 accepted). The rest: the next free reviewer; K2b and K2c first, because they are pre-day-0. |

**Lead run sets stay serialized.** The crash matrix has a 5000 ms timing guard (the subject of product commit `eb0d503`), and measurement needs a quiet machine. The order before day 0 is P5-8. After day 0, the run sets fall on X3c-3's rows (day 3), J4's rows (day 4), J3a's set (day 5), J3b's set (day 9), X12d's lead set (day 22, zero slack) and M3-M's measurement (days 28–31).

**Next, in order.** Product crates are open; X9-6 is in.
1. **On the machine:** Grok's rerun on C, F8b's cargo steps, X4-F1's lanes, X9 regression and confirmation lane, and E0 are done. P0's phase 2 lanes run now. Under P5-8, S-M is the next run set, and the I1 product chain starts when the queue reaches it (ON, "Confirmation lane on product main `15c0779`", "I1-P accepted at r2").
2. **Unblocked now:** X3a-2; K1, with K2b and K2c's oracle work; S-P between run sets; X4T-c and I1-a on the generator lane, one at a time (P5-3). E2a once P0 lands.
3. **Drafting:** J-RW r3; SD-5 with S20; J1's successors; X3d r9; X9 r17's sections as their units become ready; M3-C r8 and CRC-2 for X-H3; SYN-1 and SYN-1F; FA-1; the Rust3 limit successor (recommended); X4-F2's successor; the record revisions of M3-B, D, E1 and I1.
4. **In review:** M3-L r3 (Grok), with M3-H r3 queued after it; FA-2 (Codex); CRC-1 (GROK2); CR-1 (CODEX2); and this record (GROK2).

## M3-L gate status (2026-10-04, r7)

The source is L's own gate table (ML2, refreshed on 2026-10-04; ML3 adds G10; both in review), with the r7 status of each item. **G10 is new in r7** (P7-2).

| # | Gate item (the M3-L row) | Status | Evidence |
|---|---|---|---|
| G1 | S-M measured | **open: not started.** P5-8's run sets ahead of it are done: Grok's rerun on C; F8b's cargo steps (bound at `e093e90`); X4-F1's lanes and X9 regression, with X4-F1 integrated at `15c0779` and its confirmation lane passed. E0 is complete. P0's phase 2 lanes hold the machine now. S-M's report also waits for the D13 sign-off (G5), and its Q6-labelled samples wait for D12. | ML2 G1; ON ("F8b accepted and bound", "X4-F1 accepted by GROK2 and integrated", "Confirmation lane on product main `15c0779`", "E0 complete") |
| G2 | T2 complete (T2b) | **met.** GROK2 accepted T2b: 49 repositories. | `reviews/grok2-corpus-t2b-r1/status.json`; T2R:24 |
| G3 | Q0 | **met** (r13) | HD:3 |
| G4 | D3 sign-off | **open: owner (B3)** | AQP:543 |
| G5 | D13 sign-off | **open: owner (B3).** Its mechanisms were accepted in Q0 r13. | AQP:554; HD OI-1 |
| G6 | D2 draft | **met on the lead's reading** (Q0 §2). The sign-off is separate. ML2 asks its reviewer to confirm the reading (R7). | ML2 G6; AQP:542 |
| G7 | S-OP-2 drafted | **met and exceeded.** Codex accepted S-OP-2 at r6 (ACCEPT-DESIGN-UNIT, no required findings). ML2 item 14 checks that it registers every event L needs: the 11 provider-boundary needs map to 11 registered events. | SOP2; `reviews/codex-s-op-2-r6/status.json`; ON ("M3-L r2 written") |
| G8 | O1 | **decided in ML item 11** (lead decision). It becomes final when L takes effect. | ML2 G8 |
| G9 | O7 decided | **open: owner (B1).** CF-P's evidence is in, and it decides nothing: on macOS 27, Seatbelt through `sandbox_init_with_parameters` is feasible with a `kern.procargs` sysctl denial among five profile amendments, at high deprecation risk; AL2023 is feasible by desk check on kernels 6.1.147, 6.12.40, 6.18 and later, and earlier builds disclose. | ON B1; CFP "Verdict (macOS 27)", "Deprecation risk", "Linux desk check"; ML2 G9 |
| **G10** | **FA-2 accepted** (the provider symbol-census carrier, X-H1), reviewed with L r3 | **open: FA-2 is in review with Codex** (`reviews/codex-fa-2-r1`). L r3 adds the same item to L's own gate table (ML3 G10; in review with Grok). | MH X-H1 and FA-2 row; ON ("M3-H r1 written", "Plan for X-H1", "FA-2 and M3-L r3 written"); ML3 G10; P7-2 |

**How L is reviewed and takes effect (r7).** This replaces r6's "Before L can be sent: S-M, the two sign-offs and O7" (`M3-PLAN-r6.md:445`) and r6's drafting line for "M3-L r2, which fills ⟨SM-n⟩ after S-M" (`:426`). Both are superseded by the early-review rule (ML2 X9):
- **Review now.** L r2 was sent to Grok before its gate was met. Grok's verdict was REQUIRED-FINDINGS, with one finding (RF-1, item 13). r3 answers it, joins FA-2 (item 22, G10) and takes X-H4's wording; it is in review with Grok.
- **ACCEPT means "accepted in review".** L takes effect only when G1 to G10 are met and every delta round is accepted.
- **Delta rounds,** on the diff only and with the same reviewer: one fills every ⟨SM-n⟩ from S-M's report and records item 9's outcome; another takes any change O7's decision forces. A gate item met without a forced change is recorded as recording text.
- **Day 0 is L in effect** (P7-1). An ACCEPT in review alone satisfies no dependent's gate, MC's included.

## Choices left open, with lead recommendations

**Already decided; cite, don't reopen:**

- **Owner decisions:** D4, D5, D6, D9 timing, D10, D11, D14, D15 and D16 (AQP:544-557).
- **Evaluation and dogfood:** catalog evaluation is non-authoritative at M3 (AQP:500), and CLI dogfood is at M4 (AQP:502; BP:887).
- **Protocols and crates:**
  - the protocols are TS2 and Rust3 (BP:717);
  - the Rust substrate is `rustc_driver` (`12-architecture-completion-goal.md:145`);
  - `crates/syntax` is pure (BP:676-678).
- **Carried in from M2:** no creator command in M2 (X11:18); X12c and X12d at M3 (X12:191-192).
- **Python:** the support decision comes after M3's review (AQP:465). ME's PY-REG row is the template (ME item 19).
- **Decided in accepted unit laws tonight:** I1's IR and LD-3 (MI); B's D15 shape and discovery ledger (MB); E1's backend and E0's selection rule (ME items 1–3); C's snapshot, closure, dependency-source and Plan law, effective with L (MC r6); D's spawn, codec, supervision, DR-G29 and control law, with section F an O7 placeholder (MD); J1's order, identities, outcome matrix and S-OP-12 join (MJ); the safe event vocabulary and sinks (SOP2); re-commit (X3C).

The lead decides each choice below in the named unit's law, and a reviewer checks it.

- **O1 (M3-L).** Decided in ML item 11: (a), existing admitted observations only (OPP §3.6). Rejected: a new frame, which needs S-OP-3 and both protocol joins. Final when L takes effect.
- **Syntax backend (E1; CH14:614).** **Decided: T-native.** ME items 1–3 (r3, accepted) predeclared two branches, T-wasm first and T-native as the fallback, and E0 chose between them by six criteria. P5 failed (0.818 MiB/s against 1.0), so syntax uses native tree-sitter linked in the host, with `executionModel` `native-linked-v1`, under BP:680-682's TCB statement (E0R "Outcome"; ON, "E0 complete"). Item 18's fallback posture applies: parser defects are a declared residual risk, and the lead re-decides placement before CLI `analyze` takes untrusted input at M4, with E0's data as an input (ME item 18). GROK2 accepted the E0 report in record review (ON, "E0 report accepted by GROK2").
- **Dependency sources at M3 (C3).** Decided in MC (r7, accepted in review): a library-level import of user-named sources (NE:1681-1691), driven by the harness, with `.crate` archives decoded only under CRATE-ARCHIVE-1. The `import` command stays at M5 (BP:957).
- **Prepared mode at M3 (C3, G4).** Decided in MC (O-1): `imported-descriptor` sets from the harness recipe (NE:1806; NE:2533-2537). T2 measurement of the five `rust-cargo-prepared` cells waits for M5's authorized preparation. `native-prepare` stays at M5 (BP:992). No repository code runs at M3.
- **DR-G14 placement (M3-L).** The gate is M3 (COV:4770), but its owner module is M5 (owner string COV:4772; first milestone COV:8976). Recommendation: M3 prepares closure manifests and no-ambient-runtime refusals (F4, G2); installation stays at M5. MD's SD-3 adds the launcher's closure rows.
- **Public CLI (J1).** **Decided** in MJ item 1 (accepted): no analysis word is wired in the binary at M3. The M4 CLI unit replaces the `opensip`, `analyze` and `fit` refusals; `audit`'s stays until its M5 comparison step exists. "J1 fixes the order and identity rules" is done by MJ items 2 to 4 (MJ item 15).
- **Changed-scope (M3-L).** Recommendation: none ships. ML item 4 found that cross-edit reuse needs an IE successor (the INC-1 successor), because `cache2` binds the Plan. It is owned by the identity owner (AQP:546) and decided at M4 with S-M's data (AQP:502).
- **Stage-1 cancel grace and supervision constants (ML item 16c; MD item 14).** Rust3 keeps its protocol's 5,000 ms (RPP:119). TS2 uses 2 s, provisional. MD item 14 also fixes the liveness window (5 s, raised to at least 2 × SM-8), TERM to KILL (1 s) and the reap ceiling (10 s, or 5 s under revocation). OPP's cancellation goal (p95 ≤ 2 s) may be missed by Rust3 without a second signal; it is a goal, not a threshold.
- **Logging (O1).** Recommendation: `tracing` with one host-owned subscriber and no environment input (OPP §3.1, §3.5).
- **Platform scope (M3-X).** Recommendation: run and claim only this host's macOS family (NE:157-160). The Linux confinement code is built but exercised only on Linux lanes.

## O7: hostile-input confinement (owner decision, pending)

**Status.** O7 is an owner decision (OPP §5.6, §9) and is **pending** (ON blocker B1). It is a **hard prerequisite of M3-L taking effect and of provider launch**: no provider (F, G, G2-v) launches, and C3b's adapter does not run, until O7 is decided and D1b's primitive exists. Authoring may start earlier. This keeps OPP §8's schedule. **The D law is accepted with section F as an O7 placeholder,** binding only if O7 is decided as recommended; D1b waits for that decision (MD header, "Units after the law").

**The lead's recommendation, as put to the owner:**

1. **Analysis never executes repository code by default.** Existing law already says this: "Repository execution is disabled by default" (SL:1059), and the Rust worker's `workerExecutesRepositoryCode` is the constant `false` (NE:2534-2535).
2. **Providers run under OS confinement:**
   - on Linux and AL2023: Landlock, seccomp and no network;
   - on macOS: a Seatbelt profile that denies network access and any write outside the provider's scratch space.
3. **Where confinement is unavailable,** the result discloses it, and the documentation requires containers for untrusted pull requests.
4. **Executing repository code** (Rust build scripts and proc-macros in prepared mode) requires the existing `RepoExecutionGrantV2` (SL:1071) and runs only inside confinement or a container.

**Why it needs successors.** Accepted law currently disclaims confinement:
- "confinement is never claimed" (SL:1113);
- "No confinement is claimed" for unconfined children (SL:497);
- "No process/WASM boundary is claimed as a sandbox" (AQ:344);
- "No sandbox is claimed" (NE:2554);
- G21 "does not claim security confinement" (REG:366);
- DR-128 holds the sandbox boundary (REG:317).

Items 2 to 4 add enforced hardening and a disclosure. They must stay distinct from a sandbox claim for untrusted code, which only DR-128 could open.

**Units and successors it needs (all in M3-CF unless noted):**

- **CF-P, the feasibility probe: done** (CFP). It met the D law's gate (MD G1).
- **CF-1, the confinement successor (MD SD-1)** (owners: product security and platform owners, the DR-128 row's owners, REG:317):
  - an SL S10 and S6 successor with the per-platform enforcement matrix and the honest wording;
  - an AQ §5 item 4 disposition;
  - a DR-128 record saying this opens no untrusted-code scope.
- **CF-2, the disclosure carrier (MD SD-4):** a WS output successor, or an S-OP-6 join, for "provider ran unconfined: <reason>". It sits beside Coverage and never inside it.
- **D1b, the confinement primitive** (MD F-1 to F-4): a trusted launcher, `opensip-launch`, that applies the profile before exec.
  - **macOS:** a Seatbelt profile applied through `sandbox_init_with_parameters`, resolved with `dlsym`; a missing symbol means unavailable and disclosed. Neither mode of `sandbox_init` is used.
  - **Linux:** `no_new_privs`, Landlock and seccomp. **r7 (MD F8):** network is denied by seccomp, not by a network namespace as r6 said, because Ubuntu 24.04 denies capabilities inside an unprivileged user namespace (MD F-2, LX-12). CF-P's desk check confirms the reading (CFP:293-297). It is built at M3 and exercised on Linux lanes.
- **The D law:** the single owner of the launch rules under O7. M3-L and MC cite it.
- **D5 and S-OP-11:** three new escape controls (a network attempt, a write outside scratch and an ambient environment read). They extend OPP §10, which does not contain them. F-7, their O7 part, waits for CF-1.
- **F4 and G2:** the provider closures run inside the profile (Node, the `rustc` temporary directories).
- **M4:** the container guidance in the runbook (OPP §6).
- **M5-EX, a gated M5 successor package for item 4.** All three successors must be accepted before M5's `execution.rs` (`native-prepare`, `test-run`; BP:974, BP:992) claims any confinement or container enforcement. X4b's `admit_repo_execution_grant` lands with it (M2C §5 row 14).
  1. **The native §5.2 admission and disclosure join.** Today, `AuthorizedExecutionV2` effects are copied from PTT, and a record claiming more is refused: network, subprocess and filesystem write are `DISCLOSURE-ONLY` (NE:2440-2444; the reference admission is NEM:2170-2172). The mandatory human and JSON sentence says OpenSIP "does not prevent network access or other effects on this platform" (NE:2480-2487; NEM:2181-2182). The successor moves only the measured platform and effect cells and the sentence that depends on them.
  2. **The WS §7 test-execution schema join.** `ENFORCED-PLATFORM` is not in `EnforcementValue`, and admitting it "requires a successor truth-table profile and test-execution schema" (WS:1071-1081; TES:7-14). The test pre-spawn sentence also changes.
  3. **A measured permission truth-table profile succeeding PTT,** owned by the security owner (S10). Only cells measured on a platform move (NE:2480-2481).

  No new native carrier major is assumed where the existing vocabulary suffices. Until M5-EX is accepted, M5 execution keeps today's disclosure-only behaviour.

**Boundaries kept:**
- **No repository-code execution in M3.** Prepared sets are imported (C3).
- **The worker prohibition stands:** `workerExecutesRepositoryCode` is constant `false` (NE:2534-2535).
- **DR-128's untrusted-code scope stays closed.** Untrusted native or WASM components are not admitted, and no process boundary is claimed as a sandbox (AQ:344; REG:317). Items 2 to 4 are hardening and disclosure for first-party providers and trusted repository code, not an admission path.

**Risk (r7, after CF-P).** r6's "unverified" is replaced by CF-P's evidence (CFP; ML2 X9):
- **macOS 27:** Seatbelt through `sandbox_init_with_parameters` works from a single-threaded launcher, persists across `execve` and is inherited. It denies TCP, UDP and DNS, and writes outside scratch, and the pinned Node starts a trivial script under it. The profile needs five amendments, among them a `kern.procargs` sysctl denial; MD F-3 adopts them. The function is undeclared but exported, and the declared named mode of `sandbox_init` gets its caller SIGKILLed on macOS 27. **Deprecation risk is high:** each macOS major needs its own check, and a missing symbol means disclose (CFP "Verdict (macOS 27)", "Deprecation risk"; MD F5).
- **AL2023, desk check only:** feasible on kernels 6.1.147, 6.12.40 or 6.18 and later, with Landlock ABI 2, 6 or 7 plus seccomp. Earlier kernel builds have no Landlock and disclose. Whether Landlock is in the active LSM list on 6.12 and 6.18 is CF-1's first AL2023 measurement (CFP "Linux desk check").
- **Nothing is enforced or measured yet.** CF-P is a trial on a trivial child; only CF-1 may claim enforcement, per measured cell (MD F-8).

## Owner decisions

**Pending: the overnight blockers, as they stand (ON, "Blockers for the owner").**

| # | Decision | What it blocks | Lead recommendation |
|---|---|---|---|
| B1 | **O7**, hostile-input confinement | M3-L taking effect (G9), so day 0; provider launch; C3b's adapter; D1b and the binding force of MD section F; CF-1 and CF-2; M5-EX. Drafting continues. | As in "O7" above: Landlock, seccomp and no network on AL2023, Seatbelt on macOS; disclose where confinement is unavailable, and require containers for untrusted pull requests; run repository code only with `RepoExecutionGrantV2`, inside confinement. **CF-P's evidence** (CFP; ON B1): Seatbelt works on macOS 27 through the undocumented `sandbox_init_with_parameters`, with the `kern.procargs` profile fix, at high deprecation risk, so each macOS major needs a check and a missing symbol means disclose. AL2023 is feasible by desk check on current kernels; builds from before August 2025 lack Landlock and disclose. |
| B2 | **The gating precision bar** (the quality plan's D4 revisit; HD §5.6, HD §5.8 and OI-3) | Q2 acceptance for **gating** rules only. Nothing in M3's DAG, and not M3-X. | The accepted gating floor is a 95% cluster-aware lower bound ≥ 0.99, which needs k_min = 299 independent zero-error families (HD §5.6, §5.8). The lead recommends observed precision ≥ 0.99 plus a lower bound ≥ 0.95; with zero errors, 59 families meet that 0.95 bound. Rules graduate from advisory to gating as evidence from T2 and T3 accumulates. **Note:** T2 has 10 held-out families (T2R:296), so no rule can meet either bar on T2 alone (HD OI-3). |
| B3 | **The D3 sign-off** (the T2 selection) and the **D13 sign-off** (the exploratory envelope) | M3-L gate items G4 and G5, so day 0. D13 also gates S-M's report. | Approve as reviewed: T2a and T2b are accepted by GROK2 (49 repositories, 33 families); ENV was accepted inside Q0 r13. |
| B4 | **OQ-1:** the owner's real workspace on disk (MB item 27): the package-list file, whether the root is ever a Git repository, submodules or worktrees, and how Rust and npm packages refer to each other | Nothing. It sharpens D15's admitted shape and T3's multi-repo instance. | MB r2 admits a non-repo root with 1–64 disjoint conventional Git member repositories. Members are declared by explicit roots or by the Cargo patch and npm `workspaces` readers. |

**Lead decisions the owner may reverse.** Each was made under the owner's standing direction to decide on the lead's recommendation. None blocks. The overnight log records these:

| Source | Decisions | ON entry |
|---|---|---|
| M3-C | **O-1:** prepared-mode measurement waits for M5. **O-2:** every core release is a new detector closure. **O-3:** large repositories may hit the 4 MiB descriptor cap until S-R. **X-C1 (r6):** the core provider closure also produces syntax-universe work, so every core release is also a new syntax producer (ME owner note 4). | "M3-C r1 drafted", "M3-C r6 written" |
| M3-B | No consent flag for D15; a launch inside a member selects that member; discovery after the fence, on its own ledger profile. | "M3-B r1 drafted" |
| M2 completion | X3a-2 before C1a; X4b deferred to B3-a and M5-EX; X4T-c right after F8b; X4-F1 a defect fixed before any M3 analysis ships. | "The M2 completion record is drafted" |
| X2 r9, X12 r4 | The first-use clause reads "before any project-scoped effect", and a refused pack there leaves an empty, valid, disclosed installation; X2 runs the placement check and chain walk before item 3a's config reads. | "X2 r9 and X12 r4 drafted" |
| X4-F1 | Follow-ups X4-F2 (the fenced read) and F9 (fixture dates). | "X4-F1 written" |
| M3-PLAN r5 | P5-1 to P5-8 (below). | "M3-PLAN r5 sent to GROK2" |
| M3-E1 | The backend: tree-sitter grammars in Wasm under `wasmi`, with native tree-sitter as the fallback. **FYI:** the Wasm route needs a pinned wasi-sdk toolchain. | "M3-E1 r1 drafted" |
| E0 | Made before any data: P5 is read strictly (the median of bytes ÷ the full per-file cost, over non-empty files; aggregate throughput reported, not gated); E0's `SyntaxTreeV1` layout is probe-only; `wasmi` compiles everything up front (an E2b obligation). **The outcome, under E1's predeclared rule: T-native,** native tree-sitter linked in the host; parser defects are a declared residual risk until the M4 placement re-decision. | "E0 phase 1 is ready", "E0 complete" |
| M3-J1 | No new CLI commands at M3 (CLI dogfooding starts at M4); the durable steady state through a charged presence probe; producers run twice on first use; the ephemeral path is read-only; a signal during the final required output is recorded and deferred (phase O, S18). | "M3-J1 r1 drafted", "M3-J1 r2 sent to CODEX2" |
| M3-L | The early-review rule; stderr is counted and never held; TypeScript's `host-shutdown` cancel reason is never sent at M3. | "Lead decision: M3-L gets an early review round", "M3-L r2 written" |
| M3-D | Linux provider scratch in `/var/tmp`, because AL2023's `/tmp` is a tmpfs capped at half of RAM; a macOS group `SIGSTOP` deferred to CF-1; SD-6 as a J1 amendment (J1 r4, accepted). | "Lead decisions in M3-D r2" |
| X4-F1 integration | No full two-target matrix run at integration: the rows the change can move were rerun and match X9-6 byte for byte, and no crate reads `design-lock.json`, the only other difference from the tested base. A confirmation workspace lane on `15c0779` follows. | "X4-F1 accepted by GROK2 and integrated" |
| J-RW (in review) | A crashed first registration completes automatically, with no announcement (LD-1, LD-2); the owner's 465 item 5 ACL decision extends to the L11 owners (LD-3; JRW X-RW-6); trust files and ledgers are completed in place, suffix only (LD-4, LD-5). **r3 direction:** C-LEDGER stays, scoped to OpenSIP writers, because the product runs no VACUUM, DROP or ALTER on ledgers; a foreign SQL writer that wraps the schema cookie sits with forgery, outside the custody model (rejected: withdrawing C-LEDGER). | "J-RW r1 written", "J-RW r2: Codex raised two P2 findings" |
| P0 | The provider source layout is unchanged (the directories exist, and CH14 says not to create empty files); no checker for the new dependency policy until C3a links the crate; `forbid(unsafe_code)` on `crates/syntax`, which E2b may revisit. | "P0 phase 1 ready" |
| Rust3's subject cap | Recommendation: raise or remove Rust3's 256-subject request cap in a Rust3 limit successor before G3 ships, measured by S-M. | "New finding, important for the owner's Rust use" |
| CRC-1 and CR-1 | X-H3 goes to M3-C r8 and CRC-2, before C4a; CRC-1 carries C's law and does not amend it. CR-1 LD-3: the four roles other than `analyzer` (`toolchain`, `stdlib`, `rust-dev-llvm`, `grammar`) are closure-only, with no capabilities or permissions, and their entrypoint is never executed. | "CRC-1 and CR-1 written" |
| M3-H (in review) | FA-2 and L r3 are drafted before day 0 (rejected: deferring symbol Coverage past M3). r3: the prerequisite and totality keys take row 32, because they refuse a false `complete` or a wrong cause. Owner flags in MH: without FA-2 the preview rule decides no real TypeScript repository; a provider that exhausts its budget after finding a cycle cannot fail the Run on it; H absorbs the host inventory records; the core provider closure would produce inventory records in every universe. | "M3-H r1 written", "M3-H r3 written"; MH "Open questions for the owner" |
| I1-L | LD-L1: the JSON schema changes ship as complete successor copies. | "I1-L and I1-P written" |
| B-S1 | S9 is split out as B-S9 (rejected: a `verify_design` successor, VD2, which would stale F8b's pins). | "B-S1 and B-S2 drafted" |
| This revision | P7-1 to P7-5 (below). | — |

**Other owner items:**
- **Sign-offs D2 and D12** (AQP:542, AQP:553). D12 is on S-M's Q6-labelled samples.
- **FYI, important for the owner's Rust use: Rust3 caps a request's subject list at 256 files** and refuses before spawn above it. By the T2 manifest, 9 of the 22 Rust repositories exceed it, tokio (808 files) and axum (301) among them, so a product Rust provider could not analyze them. It goes to the Rust protocol owner as a limit successor, beside SM-6's possible TS2 limit successor. The lead recommends raising or removing the cap before G3 ships, measured by S-M (ON, "New finding, important for the owner's Rust use"; ML3 X13, in review).
- **FYI: the wasi-sdk build toolchain** (ME owner note 1) belongs to the Wasm route. E0 chose T-native, so it matters again only if T-wasm returns at M4; E0's measured fuel and memory constants are kept for that case (ON, "E0 complete").
- **FYI: no third-party licence allowlist yet.** ME's LP-1 records an interim rule for E's rows (MIT, Apache-2.0 and BSD/ISC/Zlib-family licences, and Apache-2.0 WITH LLVM-exception for build-only tools; every notice ships) and recommends a product-wide allowlist before M4 distribution (ME owner note 2).
- **Housekeeping:** CF-P's deliberately killed runs left five crash reports in `~/Library/Logs/DiagnosticReports/` (`cfp-2026-10-04-*`, `t_named-*`). They are safe to delete (ON, "CF-P run").
- **O4, OTLP** (OPP §4.2, §9): an M5 matter.
- **O9, raw provider stderr capture** (OPP §9; owner sign-off). Recommendation: not at M3. L r2 now counts provider stderr and keeps no text (ML2 item 12.1), so there is nothing to capture at M3.
- **Owner actions:**
  - adjudication expert time (AQP:254). It does not hold M3-X.
  - T3: the licence has landed and D6 allows it (AQP:547). Its multi-repo instance waits on OQ-1.
  - signing keys for real-machine runs (EXIT:112). They are not needed for M3 exit, where tests use labelled synthetic closures.

## Lead decisions

**Recorded in other records** (cited, not re-decided here):

| Decision | Recorded in |
|---|---|
| **I1 LD-3:** the `cycle-representative` op value widens in place, under an identity-contract passage successor. Rejected: a major bump, with its cascade. | MI §9; ON ("M3-I1: CODEX2's r1") |
| **I1 LD-11:** I1-c may land before I1-b2. | MI §9 |
| **F8 split:** F8a, the policy rows, is integrated at `3e64266`. F8b is the generator and lane re-pin, bound at `e093e90`. | ON ("F8 split", "F8b accepted and bound"); M2C §5 row 2 |
| **D15's shape:** a non-repo root with 1–64 conventional Git members, with no consent flag. A launch inside a member selects that member. Discovery runs after the fence, on its own ledger profile. | MB items 12, 19, 23, 27 |
| **The first-use clause:** "before any project-scoped effect". X11 r1 item 1a's conflict went to J1, which resolves it. X2 orders the placement check and chain walk before item 3a's config reads. | ON ("X2 r9 and X12 r4 drafted"); X2r9; X12r4; MJ item 4 |
| **MC O-1 to O-4:** prepared-mode measurement waits for M5; every core release is a new detector closure; large repositories may refuse until S-R; the plan impact. **Also:** the C4 split, the source and operational read split, CRATE-ARCHIVE-1, and r6's X-C1 widening. | MC "Open questions", "r3 changes", "r6 changes" |
| **M3-L:** O1(a). The stage-1 grace is Rust3's 5,000 ms, and TS2 uses D3's 2 s. No D5a successor is needed to accept L. **r2:** the early-review rule; stderr counted, never held; no `host-shutdown` at M3. **r3 (in review):** FA-2 as gate item G10. | ML1 items 4, 11, 16c; ML2 "Review and effect", items 12.1, 16b; ML3 G10 |
| **M2 carry-ins:** X3a-2 comes before C1. X4b is deferred to B3-a and M5-EX. X4T-c comes right after F8b. X4-F1 is a defect, fixed before any M3 analysis ships. | M2C §5 rows 13–16 |
| **X4-F1 is integrated** at `15c0779`, without a full two-target matrix run; X4-F2 and F9 are recorded as follow-ups. | ON ("X4-F1 written", "X4-F1 accepted by GROK2 and integrated") |
| **S-OP-2:** r2 to r6 answer Codex's findings; r6 is accepted. | ON; SOP2 |
| **M3-E1:** the syntax backend is chosen by E0 between T-wasm and T-native; **E0 chose T-native** (`native-linked-v1`), under item 18's fallback posture. | ME items 1–3, 18; E0R "Outcome"; ON ("M3-E1 r1 drafted", "E0 complete") |
| **M3-D:** Linux scratch in `/var/tmp`; the macOS group `SIGSTOP` deferred to CF-1; SD-6 as a J1 amendment; the supervision constants. | MD "r2 changes", items 6, 14, 18, 29; ON ("Lead decisions in M3-D r2") |
| **M3-J1:** no CLI at M3; the presence probe; producers twice on first use; the read-only ephemeral path; phase O deferred (S18); r4's R10a. | MJ items 1, 3, 6, 8; ON |
| **X3c r8:** a re-commit is a new attempt of the same Run; J-RW is disjoint (R8-7, R8-8). | X3C items 6a, 14, 15 |
| **J-RW (in review):** LD-1 to LD-14. | JRW "Lead decisions" |
| **M3-H (in review):** FA-2 with L r3 before day 0; H absorbs the host inventory records; clean non-Complete terminals discard their candidates. | ON ("M3-H r1 written"); MH items 4, 18 |
| **I1-L LD-L1** and the **B-S9 split.** | ON ("I1-L and I1-P written", "B-S1 and B-S2 drafted") |
| **P0:** the provider layout unchanged; no checker for the new policy until C3a; `forbid(unsafe_code)` on `crates/syntax`. | ON ("P0 phase 1 ready") |

**Made in r5 (P5).** Each is dated 2026-10-04, made under the owner's standing direction to decide on the lead's recommendation. A reviewer checks each one, and the owner may reverse any of them. r7 annotates three.

- **P5-1. The resume/repair writer is owned by M3-J,** as a new successor law **J-RW** and code unit **J4**.
  - **J-RW** amends X2 item 8, X3c item 10 and the X4T dependency-publication rule for L11's three state families, and adds their X9 coverage rows.
  - **J4** is resized from M to L, plus one serialized lead set. It depends on J-RW, not on J3: the crash states come from M2 code, not from the durable pipeline.
  - **Rejected:** keeping J3 → J4, which puts J4 and its rows on the exit path at 34 days; folding the writer into J1's law, which already carries the X11 successor and whose owners differ (X2, X3c, X4T).
  - **r7 (JRW LD-12, X-RW-7, item 14; in review):** the owner list gains **X3b**, for `trust/carrier-floors/` (RW-P3, through X3b r11), and **the registry owner**, for REG's authorization record (registry owner selection v3). The amended items read: X2 items 4, 6 and 8, with REG's record; X3c items 1, 2 and 10; X3b item 2; and X4T item 7 (leaves and parent directories), with an X4B record. J4 is proposed as J4a to J4e.
- **P5-2. The X3c successor is X3c r8 (law) plus X3c-3** (M, storage code, with its X9 storage-row rerun), and it lands before J3.
  - **Reason:** the determinism suite and the dogfood checkpoint re-run identical analyses, and so re-commit identical Runs (EXIT:171).
  - **Rejected:** keeping it inside J3, which is a host-pipeline unit while X3c is the storage owner's law; carrying re-commit as a known M3 limit, which would make durable repetitions refuse.
  - **r7:** X3c r8 is accepted. J3 is J3d.
- **P5-3. Generator order.** X4T-c and I1-a both follow F8b, and both regenerate `crates/contracts/src/generated`, so they integrate one at a time and never concurrently.
  - X4T-c goes first if its successor is accepted when F8b integrates (M2C row 15's "immediately after F8b"). Otherwise I1-a goes first, and X4T-c follows.
  - Neither waits for the other's review.
  - **Rejected:** a fixed order that idles the generator while one successor is still in review.
  - **r7:** E2s joins this rule (P7-4).
- **P5-4. X4-F1 and X4-F2 must land before J2,** the first unit that runs an analysis through the host pipeline (now J2b).
  - This reads M2C row 16's "before any M3 analysis ships" for M3, where nothing is shipped to users.
  - **Rejected:** "before M3-X" only, which would let J2, J3 and the determinism suite run on a known-defective observer.
  - **r7:** X4-F1 is integrated (`15c0779`). X4-F2 remains.
- **P5-5. F9 integrates by 2026-12-01,** a month before the fixtures expire on 2026-12-30, whatever day 0 turns out to be.
  - **Rejected:** scheduling it by DAG day, which is not anchored to the calendar.
- **P5-6. The plan adopts MC's variant B** (the C4 split), MC r3's narrowed F1 and G1a edges, and b from MB's accepted unit table: b = 10, giving 33 days.
  - **Rejected:** MB F14's "about day 8", which omits a stated edge; variant A, at 34 days.
- **P5-7. S-R is not an M3-X prerequisite.**
  - Until it lands, large T2 repositories that refuse at `snapshot2`'s bound are reported as refused (MC O-3). It is sized and scheduled after S-M.
  - **Rejected:** holding M3-X for an unsized, conditional successor.
- **P5-8. The machine order before day 0:** Grok's rerun on C, then F8b's cargo steps, then X4-F1's lanes and reruns, then S-M. S-P, CF-P and E0 run between run sets, never during one.
  - **Reason:** while O7 is pending, S-M is not what holds day 0, so M2's known defect goes first. If O7 is decided while both are waiting, S-M moves ahead of X4-F1.
  - **Rejected:** interleaving lead sets, which the 5 s timing guard forbids.
  - **r7 status:** the first three are done, and X4-F1's confirmation workspace lane on `15c0779` passed (ON, "Grok's X9-6 rerun on C was accepted", "F8b accepted and bound", "X4-F1 accepted by GROK2 and integrated", "Confirmation lane on product main `15c0779`"). E0 is complete. P0's phase 2 lanes hold the machine now, and S-M is the next run set.

**Made in this revision (P7).** Each is dated 2026-10-04 and made under the same standing direction. A reviewer checks each one, and the owner may reverse any of them.

- **P7-1. Day 0 is M3-L in effect:** accepted in review, every gate item G1 to G10 met, and every delta round accepted (ML2 "Review and effect"). Every "M3-L's acceptance", "L acceptance" or "M3-L accepted" in this plan reads so, and so does MC's gate.
  - **Reason:** under the early-review rule (ON), an ACCEPT can come before S-M and O7. r6's day 0 assumed both done by then (`M3-PLAN-r6.md:255`).
  - **Rejected:** day 0 at an ACCEPT in review, which could start day 0 before O7 is decided, against "O7" above.
- **P7-2. FA-2 is M3-L gate item G10.** FA-2, the provider symbol-census carrier, is accepted with L r3 before L takes effect.
  - **Reason:** without it, no TypeScript or Rust symbol Coverage can be admitted, F2 and G3 cannot deliver symbols and Coverage lawfully, and the preview rule cannot decide on a real Run (MH X-H1, in review). The lead already decided to draft FA-2 with L r3 before day 0 (ON, "M3-H r1 written", "Plan for X-H1"), and FA-2 is a protocol successor reviewed with L's next revision (MH FA-2 row).
  - **Rejected:** a code-leg gate only, as MH reads it. Day 0 could then start while D2b's codec (day 2), F2, G3, H3, H5 and J2b's TypeScript and Rust path all wait on an unaccepted protocol successor.
  - This adds a lead gate item to M3-L's row. It changes no owner gate or threshold.
- **P7-3. J2c joins M3-X's dependencies.** r6's J2 included the ephemeral path end to end, and reached M3-X through J3 and M3-M. Under J1's split, J3d needs J2b but not J2c (MJ item 14), so J2c would otherwise have no downstream edge. It finishes on day 27, inside M3-X's window.
  - **Rejected:** leaving the ephemeral path out of M3's exit.
- **P7-4. E2s joins P5-3's generator order.** E2s regenerates the closed eight-output generation registry (ME item 20), as X4T-c and I1-a regenerate `crates/contracts/src/generated`. The three integrate one at a time, never concurrently, and none waits for another's review. Each runs both dependency checkers in its Python lanes (M2C §5 row 20).
  - **Rejected:** concurrent regeneration on the shared generator.
- **P7-5. Only accepted laws re-time the DAG.** D r3's, E1 r3's and J1 r4's unit tables are used. H r1's H1–H5 and J-RW r2's J4a–J4e are recorded as proposals, and r6's H and J4 rows keep their timing until those laws are accepted. Both proposals fit inside the rows' slack ("Critical path").
  - **Rejected:** re-timing from drafts in review, whose breakdowns a review may still change.

## Unsized

These units could not be sized from the records:
- **The O2 parts** (S-OP-1, -5, -6, -7, -8). Their successors are not drafted. The O-row rule applies.
- **S-R.** It is conditional on S-M's SM-5 and SM-6, and has no draft (MC item 5).
- **X4-F2 and F9.** No draft exists. They are sized provisionally, as M plus a lead set and as S, and neither is on the host chain.
- **The INC-1 successor.** It is an M4 decision (ML item 4).
- **M3-L's in-effect date.** It depends on O7, S-M, the two sign-offs and FA-2 (G10).
- **r7:** FA-1, FA-2, the X-H3 C revision (M3-C r8) with CRC-2, SD-5 with S20, X3d r9, X3c r9, X9 r17's sections, SYN-1F, SD-2, SD-3, and J1's and J-RW's other successors. No source states a size. Each is a successor or a record, so the successor-law bound (about 3 rounds, at most 5 days) applies, and each reaches the host chain only through the conditions in "Critical path".
- **The Rust3 limit successor** (ML3 X13, in review; ON). It is recommended before G3 ships, and it has no draft.
- **H's and J4's sub-units** are sized by their drafts, which are in review (P7-5).

## Risks

- **The schedule stayed at 33 days, with more conditions.** X12d's lead set has zero slack at day 22. D3 has two days against F1 and G1a. J3d waits for F2, G3, J3a, J3b, X3c-3, O1 and S18 by day 25. H r1 adds FA-2 and the X-H3 widening before day 0 (in review).
- **The symbol census (X-H1).** No TS2 or Rust3 frame carries a provider's symbol census. Without FA-2, no TypeScript or Rust symbol Coverage can be admitted, and the preview rule is indeterminate on every real TypeScript repository (MH X-H1 and owner flag 1; in review). FA-2 changes TS2 and Rust3 payloads through a negotiated capability token, so it is a protocol successor; ML item 1 forbids any protocol change without one. P7-2 puts it in L's gate.
- **Rust3's 256-subject request cap.** 9 of the 22 T2 Rust repositories exceed it, so a product Rust provider could not analyze them; only a Rust3 limit successor can change it, which the lead recommends before G3 ships (ML3 X13, in review; ON).
- **The Rust compiler integration.** It needs rustc-dev and rust-dev-llvm (NE:1445). The pin has neither (`providers/rust/rust-toolchain.toml:2-4`). Stable-toolchain hosting is unverified. S-P probes it first.
- **Imported dependency sources.** Real Rust repositories need them (NE:1688-1698), and the `import` command is M5 (BP:957). C3 covers this. CRATE-ARCHIVE-1 has been checked only against unpinned Cargo sources so far (MC R6).
- **Large repositories:**
  - discovery's provisional caps, with the census margin test (MB item 12);
  - `snapshot2`'s 4 MiB descriptor holds about 27,000 rows. Five T2 repositories, and TypeScript repositories with `node_modules`, are at risk (MC item 5; S-R);
  - symbol scopes over large T2 repositories meet IDS's 100,000-subject and 4 MiB bounds; S-B needs the scope field (MH X-H6, in review);
  - the 4 MiB tree-digest limit for aws-cdk and aws-sdk-rust (K1a).
- **D15 at M3.** X2 r9 is accepted, and B-S1's D15 passages are bound (`9c11c53`). There is no cross-unit resolution, and links are honoured only after S5 and S6 (MB F2–F4).
- **Missing owners.**
  - `security/grants.rs` owns four M3 flags (COV:5277, 5317, 5337, 5377). B3-a creates it; X4b's predicate is M5-EX's.
  - `lifecycle/installation.rs` owns DR-G14 (BP:1018), but its first milestone is M5.
  - `platform/process.rs` is the M6 DR-G22 owner (BP:1026); D1a builds it early.
  - **r7:** nobody produced the inventory capability's host records. H r1 gives them to H3 (X-H5, in review). What M3 says for `vcs-change@vcs-reported` is still open, with C and the native owner.
- **Known M2 defects.** X4-F1 (observer reread expiry) is fixed and integrated at `15c0779`, without a full two-target matrix run (lead decision; its confirmation workspace lane then passed, 1749/0/3 on `15c0779`). X4-F2 (the fenced read) has no draft, and it gates J2b (P5-4).
- **Calendar.** The test fixtures expire on 2026-12-30 (F9; P5-5).
- **Held-out scale.** There are 10 held-out families (T2R:296), so Q2 PASS on T2 is INSUFFICIENT-EVIDENCE by design (HD OI-3; B2).
- **Cancellation goal.** Rust3's 5,000 ms grace can miss OPP's p95 ≤ 2 s without a second signal (ML item 16c).
- **Linux temporary space.** AL2023's `/tmp` is a size-limited tmpfs; D uses `/var/tmp`, and any unit that puts large temporary data on Linux should do the same (MD F13).
- **Record drift.**
  - DR-G10's register row is stale (REG:355). NE §14 says "independent Claude review pending" (NE:4203). F02:220 and F02:259 still state the old majors. M3-L records all three (ML2 X7).
  - **This revision** re-pins MB, ML, MC, ME and SOP2 to their snapshots. ML2 and J-RW r2 have no snapshot and are pinned by sha256 and arch commit.
  - Six laws cite L r1 by line; each re-pins by item at its next revision (ML2 X10).
  - MH r1 and r2 name X-H3's successor "C r7 / CRC-1". C r7 became the SD-6 amendment, so the lead renamed it "M3-C r8 / CRC-2" (ON, "CRC-1 and CR-1 written"; H r3).
- **The syntax backend.** E0 chose T-native, so the native C parser joins the host TCB, as BP:680-682 allows. Parser defects are a declared residual risk, and placement is re-decided before M4 accepts untrusted input (ME item 18; E0R). Wasm's memory boundary is not available at M3.
- **O7 sits outside the lead's control,** and it gates L. A late decision moves the whole schedule. CF-P shows that Seatbelt confinement on macOS depends on an undocumented symbol at high deprecation risk (CFP; MD F5). The confinement successors also reverse existing "never claimed" wording, which needs careful review.
- **Contention.**
  - **Reviewers:** the pre-day-0 law and successor rounds now include L r3 and FA-2 (in review), H r3, J-RW r3, CRC-1, CR-1, M3-C r8 and CRC-2, SD-5 and J1's successors. They compete for four reviewers. GROK2 holds CRC-1 as well as this record.
  - **Machine:** a single quiet machine (P5-8). P0's phase 2 lanes hold it now; S-M and the I1 product chain queue for it.
  - **Inventory chain and generator lane:** one linear inventory chain, and X4T-c, I1-a and E2s regenerate contracts one at a time (P5-3, P7-4).
  - P0 and the lanes reduce this; they don't remove it.
- **Budgets.** The one-shot design may miss the §5.2 budgets (AQP:376-378). S-M exists to find that out before L takes effect.
- **Adjudication capacity** (AQP:249-255) limits exploratory Q2 depth, not exit.

## Not claimed

- **No M3 product unit has started.** X4-F1, an M2 defect fix, is integrated. E0 was a probe outside the product.
- **What is accepted.** The accepted M3 design records are T2, Q0, and the laws I1, B, D (r3), E1 (r3), J1 (r4) and S-OP-2 (r6), with C r7 accepted in review and effective with L. The design units I1-L, I1-P, B-S1, B-S2 and B-S9 are accepted and bound, and the E0 report is accepted as a record. M3-L r3, FA-2, M3-H (r3 queued), J-RW (r3 being written), CRC-1 and CR-1 are in review, and nothing in them is recorded here as accepted.
- **Nothing was run for this record:** no measurement, spike, cargo command or test. The DAG figures are arithmetic over the stated durations and edges.
- **No change to contracts or gates.** No gate is prepared or qualified. No contract, schema, register row or threshold is changed. G10 is a lead gate item on M3-L's own row, not an owner gate.
- **Durations and effort are assumptions.**
- M3 does not claim:
  - CLI analysis (M4);
  - changed-scope or resident analysis;
  - `import`, `native-prepare` or repository-code execution (M5), or any confinement or container enforcement of it before M5-EX;
  - Linux or AL2023 runs;
  - Q2–Q8 qualification (M6, via D13);
  - any O7 outcome before the owner decides.
- **Sources read.** For r7: the overnight log at `4a792685…`, the snapshots and records pinned in the review request's `hashes.txt`, and the review directories cited. Product facts were read with `git log`, `git show --stat` and `git diff --stat` at main `cd5958b`, read-only. `git diff --stat 3e64266 cd5958b` shows that no product file cited above changed, apart from the F8b re-pins.
