# GROK2 review: M3 unit plan r5

**Verdict: REQUIRED-FINDINGS.**

Subject: `docs/implementation/m3/M3-PLAN.md`, 77,296 bytes, sha256 `f4833c6033ee5237129273bf6efabf560e619038fa8bb70ccc8333350c935870`. That matches `hashes.txt`. This is a planning record. No product build, run, or test was used. `~/Library/Application Support/OpenSIP` was absent. The private 413 fixture was not read.

Two citations fail. The recomputed schedule, the owner assignments P5-1 through P5-8, and the kept scheduling rules match the sources named below.

## Required findings

### RF-1. B2 points the gating bar at the wrong section, and 59 is not the accepted floor

`M3-PLAN.md:527` (owner decision B2; r5-changes row 11 lands this text).

B2 calls the decision "the quality plan's D4 revisit; HD §8" and recommends "a 95% cluster-aware lower bound ≥ 0.95, which needs about 59 independent families with zero errors."

HD §8 is "Refactor and determinism suites (Q5)" (`harness/DESIGN.md:708`). It does not state the gating precision bar. The accepted rule is in §5:

- §5.6, QD-14 (`DESIGN.md:578-580`): at zero errors, *k*_min for a gating and repair-eligible target of 0.99 is **299**. *k* = 299 gives 990030 ppm; *k* = 298 gives 989997.
- §5.8 (`DESIGN.md:633`): a gating 0.99 PASS needs at least 299 held-out families.
- OI-3 (`DESIGN.md:1247`, and the scale paragraph at `DESIGN.md:637`): grow T2 toward that *k*_min, or revisit D4.

The same floor is the accepted quality plan. AQP:148 sets gating and repair-eligible precision at ≥ 0.99 as a one-sided 95% lower bound. AQP:156 says that takes about 299 error-free gating findings where the samples are independent, and that the D4 revisit is the later point to confirm or change it. AQP:544 records D4 as decided on 2026-10-03, with that revisit still ahead. T2R:296 states the same 299 / 29 floors and cites HD §5.8.

Fifty-nine is the zero-error count for a **0.95** bound under the same formula, *k*_min(*t*) = ⌈ln 0.05 / ln *t*⌉. ⌈ln 0.05 / ln 0.95⌉ = 59. That arithmetic fits the proposed 0.95 bound. It is not the accepted 0.99 floor, and B2 does not say it is proposing to replace 299.

The parenthetical "quality plan's D4 revisit" is the right decision (AQP:156, AQP:544, OI-3). The section pointer is not. ON line 12 of the pinned overnight blob has the same "harness design §8" and "about 59" wording. Copying that entry does not make §8 the precision bar.

**Correction.** Point B2 at HD §5.6, HD §5.8, and OI-3. State that the accepted gating floor is a 0.99 lower bound, *k*_min 299, and that 59 is the count for the proposed 0.95 lower bound.

### RF-2. G7 cites S-OP-2 r3 as ASSIGNED; status.json says REQUIRED-FINDINGS

`M3-PLAN.md:435` (gate row G7; r5-changes row 9).

G7 says S-OP-2 is met, and that "r3 is with Codex (ASSIGNED)", citing `reviews/codex-s-op-2-r3/status.json`.

That file is `{"reviewer":"codex","pane":"w3:p1","status":"REQUIRED-FINDINGS"}`. It has no assignment field. r1 and r2 are also `REQUIRED-FINDINGS`, so the sentence "r1 and r2 had required findings" matches those two files.

ML's own gate, written 2026-10-03, still says G7 is NOT STARTED (`provider-protocol-l/PROPOSAL.md:24`). The plan is right that this table is stale and that an S-OP-2 draft now exists (SOP2 is pinned). "Drafted" can remain the gate criterion. The status word ASSIGNED is not what the cited file says, and a review that returned required findings is not an open assignment.

**Correction.** Cite `status` `REQUIRED-FINDINGS` for r3. If the gate item stays "drafted", say the r3 draft exists and Codex returned required findings.

## Schedule

Day 0 is M3-L acceptance. Durations are S = 1, M = 2, L = 3, and C2b = 5. Edges are integration edges. Every finish day in "r5 timing" recomputes to the figure in that table:

| Sub-unit | Finish |
|---|---|
| B1-a, B1-b | 2, 4 |
| B3-a, B2-a | 1, 2 |
| B2-b, B2-c, B2-d | 7, **10**, 12 |
| B3-b, B3-c | 13, 15 |
| C2a, C2b, C2c | 2, 7, 4 |
| C1a, C1b, C1c | 12, 13, 13 |
| C3a, C3b, C3c | 15, 16, 17 |
| C4a, C4c | 19, 20 |
| X12d, then its lead set | 21, then **22** |
| CF-1, CF-2 | ≤ 5, ≤ 7 |
| D1, D2, D3, D4, D5 | 2, 4, 7, 9, 10 |
| E0, E2a | ≤ 0 |
| E2b, E2c, E3 | 5, 8, 14 |
| F1, F2, F3, F4 | 15, 19, 22, 17 |
| G2-v | 3 |
| G1a, G1b | 15, 19 |
| G3, G4 | 20, 23 |
| H, I2 | 22, 24 |
| J2, J3 | 25, 28 |
| X3c-3, then its rows | 2, then 3 |
| J4, then its rows | 3, then 4 |
| K1a, K1b, K1c | 2, 3, 5 (started at day 0) |
| K2 | **6** |
| O1, O3 | 4, 13 |
| R | 22 |
| M3-M | 31 |
| M3-X | **33** |

O2 parts stay successor-gated. O2_selected is compared at arrival at M3-X, whose start is max(M3-M, R, F4 = 17, O2_selected).

**b = 10.** MB:847 makes B2-b wait for B2-a, B1-b, and B3-a. B1-b finishes on day 4, so B2-b finishes on day 7 and B2-c on day 10. MB:805's "about day 8" is B2-a → B2-b → B2-c (2 + 3 + 3) and omits the B1-b edge. The nine code and harness rows plus B-S1 and B-S2 match MB:841-851.

**Host chain = 33.** 2+2+3+3+2+3+1+3+3+3+3+3+2. X12d's lead set reaches J2 on day 22, the same day H finishes, so that branch has zero slack. Variant A adds C3c to C4a's predecessors, finishes C4a on day 20, and gives 34.

**Conditions.** K2's scheduled finish is day 6, inside the day-28 bound. O2_selected must finish by day 31. X12d's lead set must finish by day 22.

**K2a slip.** A freeze slip of *s* days past day 6 leaves F1's start (day 12) with 6 days of margin and H's start (day 19) with 4 more. M3-X = 33 + max(0, *s* − 10). For *s* ≥ 10, F2 finishes at 13+*s* and J2 at 15+*s*, so F2 adds no further day. K2 → M3-M alone would move the chain only for *s* > 22.

**Slack, against the next consumer's start.** C4c 2 (day 20 vs J2 at 22). F1 4 (15 vs H at 19). I2 4 (24 vs M3-M at 28). G3 5 and G4 5. F2 6 and F3 6. C2b 5 (7 vs C1c at 12). B2-a 2 and B3-a 3 (against B2-b at 4). R 9. E3 14. B3-c, O3, F4, J4's rows, and X3c-3's rows are larger than those.

**Full C1/C2 edges.** F1 and G1a finish on day 16, F2 on 20, G3 on 21, G4 on 24. The host chain stays 33.

**J3 → J4.** J3 at 28, J4 at 31, rows at 32, M3-X at 34.

**I1 and F8b.** With X4T-c first, I1-c is at *f*+6 and I1-b2 at *f*+8, so F8b finishes by day 10. With I1-a first, those offsets are *f*+4 and *f*+6, so F8b finishes by day 12. Both meet I1-c by 16 and I1-b2 by 19. MIU:28-33 and MIU:40 support the product sizes and the downstream edges. F8b → I1-a is M2C §5 row 2, not an MIU "Depends on" cell, and the plan says so.

**C-law tolerance.** C2a starting on day 5 finishes C2b on day 12, which is C1c's start, so C4a does not move. SX-1 by day 2 is B2-a's slack before B2-b starts on day 4. VCS-1 and NIJ-1 by day 12, and R3 by day 15, match C1b, C3a, and C3c.

No integration edge used for a finish day above is contradicted by MB, MC "Units", ME item 20, or MIU:28-40. Edges that are named in a source and omitted from a timing cell, without moving a day, are observations below.

## Owner assignments

Each of P5-1 through P5-8 names a rejected alternative (`M3-PLAN.md:566-589`).

- **P5-1.** J-RW amends the three L11 families, and J4 waits for J-RW rather than J3. X9 L11 (`crash-matrix-x9/PROPOSAL.md:163-168` and `:1162`) names those families and leaves the later owner as an M3 repair or resume writer. X2 r9 still has item 8's identity rows, including `identity-recovery-required` (`project-root-x2/PROPOSAL.md:366`). X3c r7 item 10 has the partial-footprint `LEDGER.CORRUPT` row (`ledger-blob-x3c/PROPOSAL.md:70`). X4T r11 item 10 has the `installation-incomplete` row (`trust-admission-x4t/PROPOSAL.md:141`). EXIT:186-191 is the same limit; its parenthetical names X2 item 8 and X3c item 10, and M2C:331 adds the X4T dependency wording. Decoupling J4 from J3 is what keeps the rejected alternative at 34 days.
- **P5-2.** EXIT:171 is the re-commit refusal and says it needs an X3c successor. EXIT:70's accepted X3c is r7, so r8 is the next revision. X3c-3 before J3 matches M3-M's dependence on repeated commits through J3. The day-25 bound is J3's start; the scheduled finish is day 3.
- **P5-3.** Matches M2C rows 2 and 15 and both F8b bounds. The rejected alternative is a fixed order that waits out the other review.
- **P5-4.** Reads M2C row 16's "before any M3 analysis ships" as before J2. The rejected alternative is waiting until M3-X.
- **P5-5.** F9 by 2026-12-01, fixtures expire 2026-12-30. That date is in the pinned overnight log.
- **P5-6.** Variant B, b = 10, 33 days. Rejects the day-8 estimate and variant A at 34.
- **P5-7.** S-R is not an M3-X prerequisite. That matches the plan's statement of MC O-3: large repositories that refuse are reported as refused.
- **P5-8.** One machine queue. Product `eb0d503` is the crash-matrix commit whose message records the 5000 ms timing guard.

## Rules kept

`M3-PLAN.md:353` still leaves the whole-M3 total uncomputed. The unbounded list is the O7 date, the named pre-day-0 law and successor rounds, the P5-8 machine queue, the O2 parts, and S-R. K2 is removed at line 360, and Q0 does bound it (16 days, finish day 6 on this schedule). The Unsized section (lines 591-598) covers the O2 parts, S-R, provisional X4-F2 and F9, the INC-1 successor, and M3-L's acceptance date.

## Citations that match

Checked against the pinned bytes, or against product `3e64266` for product paths. History tables at lines 73-85 keep r4-era AQP lines on purpose (line 86). Those were not failed.

- **AQP r6** (`1611014d…`, 65,533 bytes). AQP:113 is the 66-cell count, 57 / 6 / 3. AQP:148 and AQP:156 are D4's 0.99 lower bound and the later revisit. AQP:370-379 is §5.2; the numeric rows are 376-378. AQP:542 D2, 543 D3, 544 D4, 546 D5a, 547 D6 (T3 gated on D14), 553 D12, 554 D13, 555 D14 Apache-2.0, 556 D15, 557 D16. AQP:500 is catalog evaluation at M3; AQP:502 is CLI dogfood at M4. The body's moved lines that were read (INC span 389-409, phase timings 359-366, adjudication 249-255) match r6. Shifts from r4 are not one constant.
- **EXIT.** Line 61 is the S/M/L/XL size sentence, copied at plan lines 187-191. EXIT:171 is the re-commit bullet. EXIT:186-191 is the permanently refused crash states. The +2 after line 61 (r4's 169 and 184-189) lands on these bullets.
- **X12 r3 snapshot** (`PROPOSAL-r3.md`). Item 8 is before everything (line 125). Line 134 takes policy only from AdmittedPack. Line 136 does not depend on X1. Lines 191-192 are X12c and X12d, and X12d lands before any analysis producer reaches X5. Lines 196-202 open the forbidden substitutes. The plan cites the snapshot, not the live r4 draft.
- **Product `3e64266`.** `package.json:8` is Node 24.16.0 and `:13` is TypeScript 6.0.3; the licence line is line 5. `providers/rust/Cargo.toml:8` is `rust-version = "1.95"`. `rust-toolchain.toml:2-4` is channel 1.95.0, profile minimal, components rustfmt and clippy. `git rev-list --count d4239a5..3e64266` is 62, and `d4239a5..3d2d5b5` is 60. Among the paths the product table cites, `git diff eb0d503 3e64266` changes only `providers/typescript/package.json` and `providers/rust/Cargo.toml`, one line each. The numbered configuration, fact-admission, request, lib, workspace Cargo.toml, component-manifest, macos-process, evaluator lib, pack-registry, policy, descriptors, protocol, native-carriers, protocol.ts, rust main, bootstrap, and arguments lines match the sentences that cite them. The absent modules named in that table are absent. `Cargo.lock` has no `tracing`. `arguments.rs` has no `--timings`.
- **M3-L gate.** G2's T2b status file is `ACCEPTED`. G3 cites HD:3. G4 and G5 cite AQP:543 and AQP:554. RPP:119 is `"cancellationGraceMilliseconds": 5000`. ML:180-188 is the cache2 / plan2 / INC-1 finding. ML:553's r4 AQP:370-390 span is live AQP:389-409.
- **M2 carry-ins.** M2C:5 is PENDING-RERUN. §3.3 leaves X3a-2, X4b, and X4T-c unbuilt and defers X12c/X12d. §4.1 L11 and §5 rows 2, 10, 11, and 13-16 say what the plan says they say, including row 16's rejected X4 amendment. §6 says the generator drift check and `check_typescript.py` still refuse until F8b. The pinned overnight blob contains "X4-F1 written".
- **Units.** MB:841-851 is two design units and nine code and harness units, with B2-b depending on B2-a, B1-b, and B3-a. MC's unit split, the narrowed F1/G1a edges, and the X12 r4 and SX-1 gates are the ones the plan uses. ME items 2, 3, and 20 are the Wasm / `wasmi` backend, the native fallback, and E0, E2a–c, E3. E3 finishes on day 14 with 14 days of slack against M3-M.
- **Folded observations.** GROK2 r3 NBO-2 was the stale "operability r3 in review" risk. The r5 header cites accepted OPP by section. NBO-3 asked that G2-v not be treated as D1's enforcement claim. Plan line 209 says that, and names CF-1 as the claim. CODEX2 r4 N01 asked that late branches be compared at arrival at the exit gate. Plan line 323 does that: max(28, K2)+3 against O2_selected.
- **T2.** T2R:24 is 49 repositories, 5 workspaces, and 33 families. T2R:296 is 10 held-out families.

## Observations (not required)

1. **Row 8's "nor a code unit" is stronger than r4.** `M3-PLAN-r4.md:168` names J4 as the resume/repair writer and puts "X3c successor" in that row's law column. It does not name a separate law, an author, an X3c revision, or an X3c code unit. M2C:327 and §5 rows 10-11, which say no row names the writer or the successor, do overstate the gap. P5-1 and P5-2 are the assignment that closes it.
2. **The overnight pin and the live file differ.** `hashes.txt` pins ON at 12,319 bytes, `856560a8…`, which is arch `8ada22ed6`. Every ON phrase cited above is in that blob. The live file is a later additive dispatch note. That drift is in the review pin, not in `M3-PLAN.md`.
3. **`crates/evaluator/Cargo.toml` also gained one line** between `eb0d503` and `3e64266`. The product table does not cite that file. The claim that the cited files changed only in `package.json` and `providers/rust/Cargo.toml` matches those cited paths.
4. **AQP:376-378** is the small, medium, and large budget rows. §5.2 starts at line 370, and the very-large row is line 379. The numeric budgets are the three cited rows.
5. **Timing cells omit some source edges, and no finish day moves.** X12d's timing cell names C4a and I1-b2. MC also names X12-A, and names I1-c in prose; I1-c is already on C4a, whose start is day 16. A successor bounded at five days from day 0 finishes before C4a. C1a's timing cell omits S-B, which MC places on J1's public projection. I1-c depends on I1-P (MIU:33); the plan's edge list follows MIU:35-38, which does not repeat that edge. I1-P is a design unit ahead of the product chain. The M3-H units row says "C4a; E3 or F1" (line 210) and the timing row says "C4a, F1". E3 finishes on day 14 and F1 on day 15, both before C4a on day 19, so H still finishes on day 22.
