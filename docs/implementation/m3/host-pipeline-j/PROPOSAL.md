# The guarded durable host pipeline — proposal M3-J1 r6

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Law for unit **M3-J1** of the accepted M3 unit plan (M3P:265).

**Draft r6, not accepted. Not code.** M2 is complete: its crash-matrix gate was met by Grok's accepted rerun on C = `3d2d5b5` (`m2/M2-COMPLETE.md`; M3P:7). P0 is integrated (product `5e25d04`). The B, D and H laws are accepted (M3B; M3D; MH), and M3-C r7 is accepted in review and takes effect with M3-L (M3C; M3L). J's code units still wait, as item 14 lists for each, for M3-C and M3-L to take effect, for the other units named there, and for I1's product units.

r1 (`PROPOSAL-r1.md`, sha256 `ff5cb156…`, 75,581 bytes) was reviewed by CODEX2 (`reviews/codex2-host-pipeline-j-r1`; REQUIRED-FINDINGS, 7 required, 2 non-blocking). r2 answered all nine.

r2 (`PROPOSAL-r2.md`, sha256 `f7efb87a…`, 100,981 bytes) was reviewed by CODEX2 (`reviews/codex2-host-pipeline-j-r2`; REQUIRED-FINDINGS, 3 required, 1 non-blocking). CODEX2 closed J1-R1 and J1-R3 to R7 and J1-N2. r3 answers all four r2 findings and changes nothing else of substance.

r3 (`PROPOSAL-r3.md`, sha256 `ad887c90…`, 111,561 bytes) was **accepted** by CODEX2 with no required findings (`reviews/codex2-host-pipeline-j-r3`). The acceptance covers the law and its method only: J-BS and S18 still need their own ACCEPT-DESIGN-UNIT reviews, and J2a–J3d need inventory-unit reviews. Its two non-blocking observations, J1-R3-NB-01 (narrow the WS:1409 composition citation to the X3D and X7 fault owners) and J1-R3-NB-02 (qualify post-freeze loss by the actual SOP2 freeze point), are carried into S18's successor text, not into this law.

r4 (`PROPOSAL-r4.md`, sha256 `c18c0d3c…`, 120,506 bytes) was **accepted** by GROK2 with no required findings (`reviews/grok2-host-pipeline-j-r4`). It was a narrow amendment: it applied successor **SD-6** of the accepted supervisor law M3-D r3 (**M3D**; SD-6's row is M3D:1181 in r5) and one record correction, and changed nothing else. M3D owns what the new row admits and refuses, and how each refusal is routed; J1 only places the row. GROK2's one observation, NBO-1, is recorded in r5's M3D short name.

r5 (`PROPOSAL-r5.md`, sha256 `4ccb2320…`, 146,331 bytes) was **accepted** by Codex with no required findings (`reviews/codex-host-pipeline-j-r5`). It was a record revision with two lead decisions, LD-r5-1 (8.2) and LD-r5-2 (8.3). Its table, "r5 changes", follows r6's. Codex's one observation, J1-R5-NB-01, is applied in r6's M3C short name: of the 36 M3C lines J1 cites, 35 keep their text, and item 16's row 8 is the exception (S19).

**r6 is a record revision.** It records what accepted laws, bound successors and the lead's rulings have settled since r5, and it pins every cited law and plan at an accepted snapshot. It decides nothing new. Two corrections come from the lead's rulings on J2a's open items (2026-10-04; `reviews/grok-j2a-r1/REQUEST.md`, "Lead rulings"): row 27's ephemeral form (E-3) and item 14's derivation owners. One sentence of a bound NE row is recorded and routed to the lead, not resolved (item 10). r6 changes nothing else. The table below maps each change to its source. Diff r6 against `PROPOSAL-r5.md`.

## r6 changes

| Source | Where | Change |
|---|---|---|
| **M3-D r5, accepted** (Grok, `224b9228…`; `reviews/grok-supervisor-d-r5`): item 25 and its cross-law item X-D4-J1-1. **SD-7, accepted and bound** (GROK2 ACCEPT-DESIGN-UNIT at r2, `reviews/grok-sd-7-r2`; product `d2c00a9`) | item 10: new row 57, and the bullet that replaces r5's "routed to M3-D r4"; item 4's R1 row; J-C20; item 13's S20 row; Not claimed | **Row 57** is M3-D item 25's request-class route. M3-D r4 decided it (LD-R4-2). M3-D r5 gives the row word for word (X-D4-J1-1, M3D:1222), and r6 copies it. SD-7 binds NE's row on NE:3539 and widens `PROVIDER.NOT_SELECTED`'s code-keyed remedy. R1's row gains M3-D r5's sentence: "A well-formed request that is a request-class excluded form is not malformed; it takes row 57 (M3-D item 25)." J-C20 tests row 57. S20 records R1's route as bound. |
| **SD-7's X-SD7-J1** (`supervisor-d/sd-7/README.md`, "Cross-law items") | item 10, a bullet after the table; J-C20 | Row 56's basis, "NE §10 (SD-5)", is NE:3540 as SD-7 supersedes it. Row 57's "NE §10 (SD-7)" is SD-7's override of NE:3539. J-C20 tests both. Row 56's columns are unchanged. |
| **S21, accepted and bound** (Grok ACCEPT-DESIGN-UNIT at r2, `reviews/codex2-s21-r2`; product `3f6f9a5`): its cross-law item 1 | 8.3's LD-r5-2 paragraph; J-C14; item 12's new rows; item 13's S12 and S21 rows; item 14 (J3b, J3d, the critical path); Open questions 7; Not claimed | J1 r5's rule-1 and rule-2 gate for a signal is met. 8.3's "WS's text does not say so" is now history. The S21 row takes S21's scope, a required analysis or verify step's commit (S21 LD-3), and its two per-kind lines, WS:229 and WSE:233 (S21 LD-6). r6 wires nothing: each item that waited for S21 proceeds under its own unit review. |
| **M3-D r5's re-citation** (D's acceptance note: "J1's next revision re-cites D at r5") | short name M3D; the r4 history paragraph; the r4 and r5 changes tables; items 4, 6 and 13 | M3D is now M3-D r5. Each r3 line is re-pinned and keeps its fact: 717-722 → 764-769; 717-734 → 764-797; 718 → 765; 719 → 766; 720 → 767; 722 → 769; 733 → 796; 743-746 → 812-815; 748-763 → 827-851; 1091 → 1179-1180; 1092 → 1181. Two re-pinned lines say more in r5. M3D:796 states SD-5's route as accepted and bound, where r3:733 recommended it. M3D:769's quotation cites J1 r4's line (J1:176), where r3:722 cited J1 r3's (J1:161). r3:758, a recommendation that M3-D r4 replaced with LD-R4-2, is cited only in the r5 changes table, as "M3D r3:758". X-D4-J1-2 lets J-C10b add D4-T4's positive case. r6 adds no control: D4-T4 runs that case on the three paths (M3D:818-819). |
| **M3-L r5's X14** | none | Nothing of X14 is open. r5 applied it in full: item 2's forbidden substitute cites M3L item 13, not r1:377. |
| **SYN-1, accepted and bound** (CODEX2 ACCEPT-DESIGN-UNIT at r2, `reviews/codex2-syn-1-r2`; product `682991f`): its X-J1, LD-5, LD-12 and O-1 (`syntax-e/syn-1/README.md`) | item 10: row 52, new row 58, and the bullet that replaces r5's "Pending SYN-1"; J-C20; Not claimed | **Row 52** gains SYN-1's syntax grammar context row, NE §10's new row after NE:3530. Its `native.syntax-grammar-*` and `native.syntax-normalizer-*` keys take row 52's route at J-ε, before the PlanId, each in the form NE §1.2's key table gives. **Row 52** also gains O-1's two native-context keys, `native.native-context-closure-malformed:<where>` and `native.native-context-field-mismatch:<subject>`. NE:3530 still lists neither: SYN-1 records that gap for the NE owner. **Row 58** is SYN-1's syntax backend fault: operational-failed 4, `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, `HOST.INVARIANT_VIOLATED` with subject `native.syntax-backend-fault:<grammarId>`, and no runId. J-C20 tests row 58. |
| **Lead ruling on E-3's ephemeral detail** (`reviews/grok-j2a-r1/REQUEST.md`, "Not settled" item 3 and "Lead rulings" item 3; work log, "Lead rulings on J2a's open items") | row 27; item 6's E-3 row; item 10, a bullet after the table; short name RTC; Open questions 3 and the new lead item | **The run-termination contract's §7.4 governs.** WS:1399-1414 makes RTC §7 the owner of a step termination's detail and authority, and §7.4 admits no §7.5 detail on an ephemeral attempt (`RUN_TERMINATION_DETAIL_NOT_ADMITTED`). So row 27's ephemeral case and item 6's E-3 recommendation drop `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`. That form is indeterminate 3, `COVERAGE.PROVIDER_UNAVAILABLE`, `authority: ephemeral`, no runId and no detail. The durable case keeps the detail. **Rejected:** a contract successor changing §7.4. A law cannot override the contract, and nothing needs the detail. **Recorded, not resolved:** NE's excluded-form row, as SD-7 supersedes it at NE:3540, still names that detail for "an ephemeral request with no trust view". r6 changes no NE text. **Lead ruling:** SD-8, an NE passage supersession of SD-7's NE:3540 override, drops that detail before J2c. |
| **Lead ruling on deriving the analysis projection** (J2a's request, "Not settled" item 4 and "Lead rulings" item 4) | item 14: the J2a, J2c and J3d rows | J2a projects an analysis outcome it is given, and stays pure. **J3d** derives a committed Run's outcome: its ordered D9 deficiencies (RTC §4), its coverageId (RTC §5) and the whole termination's §7 composition (`admit_analysis_step_termination`), which needs the commit receipt. **J2c** derives an ephemeral result's outcome: its reasons through J2a's NE §10 bridge, and its RTC §7.4 form. **Rejected:** J2a, which would break its purity. |
| **Item 13's successors, by state** (each law's accepted snapshot and review directory, cited in its row; work log) | item 13: S2 to S16 and S20; item 14 | **Accepted:** S2 (468 r6), S3 (X1 r2), S4 (464 r3), S5 (X3a r6), S6 (X4B r6), S9 (X7 r7), S10 (X3d r9) and S14 (X3c r8; X3c r9 is also accepted). S7 (X2 r10) is accepted with J-RW's RW-S1. S11 (X4 r8) is accepted at round 3 and adds code unit X4-F3. S12 (X9 r17) is accepted section by section: §RC is accepted and §S12 is reserved. **Not yet written:** S7b's E-1 and X4T parts (M3-C r8, accepted in review, carries E-2 and E-3's C half), S8 (X5 r4), S13 and S16. **S20** stays partly owed, as SD-5b. |
| **M3-C r8, accepted in review** (CODEX2, `578c186e…`; `reviews/codex2-snapshot-plan-c-r8`): its LD8-4, LD8-5 and cross-law item X-8 | item 6's E-3 row; item 10, a bullet after the table; item 13's S7b row; item 14's J2c row; short name M3C | M3-C r8 carries S7b's E-2 (LD8-4: one fresh ProjectId draw per ephemeral invocation, never persisted or compared) and E-3's C half (LD8-5: no manifest-admitted closure, every requested cell kept as an unavailable binding, and no detail under RTC §7.4). Both take effect with M3-L. Its X-8, "for the enumeration owner, with J1", finds that a required cell whose closure is not admitted has no binding the enumeration contract admits. That covers E-3's required cells other than `inventory` cells, and WS:1374's durable not-installed golden, which J1 routes to row 27. M3-C r8 recommends an enumeration-contract successor, and says C4a's and J2c's legs for that case wait for it. r6 records the dependency and decides nothing. M3C stays r7. |
| **X4 r8's LD8-9** (X4r8 S11.9) | item 14: J3b's row and the critical path | J3b depends on X4-F3, which lands before J3b or in its commit. M3-PLAN r10 records the same edge (M3P10:82). |
| **X3d r9's LD9-3** (X3D9) | 8.2's LD-r5-1 paragraph; 8.6's X3d list; item 13's S10 row; item 14's J3b row | The close's admission bit is the read-only accessor `StoppedSession::admitted_at_close()`. J1 8.6 had not said where the bit lives. |
| **The SD-5b rule** (M3-D r5 item 29, M3D:1180; J2a's request, "Lead rulings" item 1) | item 10, a bullet after the table; item 13's S20 row | SD-5b is written row by row with each refusal's first consumer: `MemoryBudgetBelowCeiling` before J2b's first provider stage, with D3a; `ToolOutputBound` and `ToolScratchBound` with C3b; `confinement-refused` with D1b, and only if O7 is decided as recommended. Each adds one item 10 row and one J-C20 test in its consuming unit. J2a carries no placeholder. r5's "land with D1 to D5 (SD-5 LD-S6)" is replaced. |
| **J-RW r4's RW-S8** (Codex, `9c53bce7…`; `reviews/codex-resume-repair-jrw-r4`; JRW item 12) | item 11; item 13's S14b row | Item 11's recommendation is replaced by J-RW's decisions (JRW items 2 and 5). J-C22 is JRW item 9's. The `repair recover` correction, RW-S8's other half, has stood since r4. |
| **Snapshot pins** (the lead's rule: pin snapshots only) | Short names; every M3B, I1, OPP and AQP line | r5 pinned seventeen laws and plans at their live files. Each now pins the snapshot J1's lines were read against. For thirteen (X1, X3A, X3D, X4, X4B, X4T, X5, X7, X9, X10, X11, L464 and L468), the live file at every J1 revision from r1 to r5 differed from that snapshot by at most one line, edited in place by its acceptance record, and no cited line is that line, so no cited line moves. For the other four (M3B, I1, OPP and AQP), the live file was the snapshot plus a two-line acceptance note after line 1, so each cited line number drops by 2. Twelve of the seventeen live files now hold a later revision. Nine are J1's own successors (S2 to S6 and S9 to S12), and X4T, M3B and I1 moved for other reasons. New short names: RTC, JRW, M3P10, X3D9, X4r8 and X7r7. EXIT has no snapshot, and the lines J1 cites from it are unchanged since J1 r1. |
| **Header and product** | header; Short names; Open questions (R9 to R11); Not claimed | r5's acceptance is recorded. Three reviewer questions are added, R9 to R11. Product main is now `1799d3d`, with 99 contract successors and 96 inventory successors (v136 selected). No product file J1 cites changed between `5214350` and `1799d3d`. M3P stays r9: r6 cites r10 only for the X4-F3 edge. |

## r5 changes

| Source | Where | Change |
|---|---|---|
| **SD-5, accepted and bound** (Grok ACCEPT-DESIGN-UNIT, `reviews/grok-sd-5-r1`; product `052d3cb`): its cross-law item X-SD5-J1, and this law's S20 | item 10: new row 56, row 27 and J-C20; item 4's R10a bullet; item 13's S20 row | **Row 56** is SD-5's row, word for word. A component manifest that is an excluded form at R10a or ER10a is request-rejected 2, `EXTENSION.ADMISSION_REJECTED`, with detail `PAYLOAD-NOT-ADMISSIBLE` and subject `excluded-form:<class>:<manifestDigest>`, and carries no runId or executionId. Row 27's "not admissible" now reads "not admitted by current trust", and never covers an excluded form. J-C20 gains row 56's test. S20 is recorded as bound for R10a's and ER10a's route, and SD-5's other refusals stay owed. |
| **M3-C r7, accepted in review** (CODEX2, `reviews/codex2-snapshot-plan-c-r7`): this law's S19 | item 13's S19 row | S19 is recorded as accepted in review. It takes effect with M3-L. |
| **SD-5's X-SD5-1** (M3D item 25) | item 10, a new bullet; item 13's S20 row | M3-D item 25's request-class `ExcludedForm` at R1 is recorded as **routed to M3-D r4**. M3-D r4 has not decided it: arch holds no M3-D r4 at r5's drafting. The row's shape is recorded as **pending**. SD-5 recommends request-rejected 2, `REQUEST.UNSATISFIABLE` (M3D r3:758). No row is added. |
| **S18, accepted and bound** (GROK2 ACCEPT-DESIGN-UNIT at r2, `reviews/codex2-s18-r2`; product `5214350`): its cross-law items 1a to 1d and 1g | 5.3; 8.2's row O; 8.4; J-C14; J-C14b; S12-O; item 13's S18 row; every SOP2 citation | **1a (J1-R3-NB-02; S18 LD-7).** Row O's "because O follows SOP2's freeze, that event is post-freeze loss" becomes S18's three-way rule. The event is admitted before the producer cutoff. After the cutoff it is committed `drain-abandoned`. After the freeze's reads it reaches only the post-freeze tally. S12-O stays the post-freeze case, and J-C14's O case takes S18-T1's three points. <br>**1b (J1-R3-NB-01; S18 LD-6).** "Through WS:1409-1411's composition" becomes the fault owners (X3D:176, :283; X7:101, :120) and WS:1412-1413. J-C14b takes S18-T2's separate assertion. <br>**1c.** Every SOP2 line moves from r4 to r6: 205-208 → 226-230; 623 → 652; 623-650 → 652-683; 663 → 704; 815 → 871; 816 → 872. 710 → 766 is added, because S18 does not cite that line. <br>**1d (S18 LD-4).** 5.3's settlement point becomes "every required step terminal and the required output returned". r4 said the output decision point "does not make step 1 terminal", which is false when the decision point cancels step 1. 5.3 and 8.4 now say instead that it does not settle the invocation. Phase O is recorded as WS's own rule, no longer an exception J1 holds open. <br>**1g.** Item 13's S18 row records WSE, the after-settle lines and the copy form. |
| **S18's cross-law item 1e** | 8.2, a new paragraph after the table; J-C14; J3b (item 14) | **Lead decision LD-r5-1.** Suppose `publish` returns without entering D, and a signal is then observed. That signal is labelled by the last phase the operation reached: C if FinalGate admission had succeeded, and B otherwise. The label is read from the window close's own sample. |
| **S18's cross-law item 1f** (its LD-12) | 8.3, a new paragraph; item 13, new successor S21; item 12 and item 13's S12 row (S12-C, S12-U); item 14 (J3b, J3d, the critical path); Forbidden substitutes; Open questions | **Lead decision LD-r5-2.** 8.3's rules 1 and 2 stand against WS:226, on the basis of IE:1680-1681 and SL:551-554. The WS amendment this needs is recorded as an owed successor, **S21**, on WS:226 and WSE:226. Both lines are free in the lock at `5214350`. r5 does not make the amendment. Until S21 is accepted, no unit delivers a rule-1 or rule-2 termination for a signal. |
| **FA-1's X-FA1-J1** (Grok ACCEPT-DESIGN-UNIT, `reviews/grok-fa-1-r1`; product `f97c02b`) | item 10, row 31's basis | Row 31's basis now reads NE:3849-3850 as FA-1 states them. The stage stays `partial` and the Run stays authoritative. The route is unchanged. |
| **M3-L r5's X14** (and M3P's routing row for L r2's RF-1), and **FA-2's X-FA2-J1** (Codex ACCEPT-DESIGN-UNIT r2; product `8ca420f`) | item 2's forbidden substitutes (r4:207; r3:192) | "Beyond M3L:377's" becomes "beyond those M3L item 13 lists". Item 13's list is derived from the schemas and re-derived by control L-C1, and it includes FA-2's members. |
| **M3-L r5's X10** (and M3P's routing row X10) | short name M3L; G2; items 2, 5.2, 7, 8.2 and 8.5 | M3L is now L r5, accepted in review. It is cited by item and finding, never by line. r1's lines map as follows: :120 → item 2; :375-382 and :377 → item 13; :442-462 → item 16; :450-457 → item 16c; :548 → X3. |
| **Moved snapshots** | Short names; every citation of each | <br>- **M3P** is M3-PLAN r9 (GROK2, `72bc7a13…`). Every fact r9 still holds is re-pinned to r9's line. <br>- **M3P6** is new. It keeps r6 (`a6956e88…`) for r6's own words: item 1's quotation, item 14's r6 sizing and item 15's corrections to r6. <br>- **M3C** is M3-C r7 (`a1ee9386…`). Every line J1 cites keeps its text, and moves by 22 to 49 lines **(r6: except item 16's row 8; J1-R5-NB-01)**. <br>- **M3D** stays r3. Its sentence about the live file is corrected, which answers GROK2's NBO-1 on r4. <br>- **MH** is new: M3-H r3 (Grok, `7a562720…`). <br>- **SOP2** is S-OP-2 r6 (Codex, `ce8d3a4b…`). <br>- **X3C** is new: X3c r8 (GROK2, `ba638efb…`). <br>- **M3L** is L r5, as the X10 row above says. |
| **M3-PLAN r9** (its routing row S17) | item 13's S17 row; item 15 | S17 is recorded as done: M3P r7 to r9 carry J's units and the M3P6 corrections (M3P:265, :619). |
| **X3c r8, accepted** (GROK2, `m2/reviews/grok2-ledger-blob-x3c-r8`) | item 11; item 13's S14 row | X3C items 6 and 6a give J exactly the re-commit it needs. X3c-3 follows. |
| **SYN-1, in review** (CODEX2, `reviews/codex2-syn-1-r2`; not accepted) | item 10, a new bullet | SYN-1's X-J1 asks row 52 to gain the `native.syntax-*` keys, and asks for a new "syntax backend fault" row. Its O-1 adds two native-context keys. Both are recorded as **pending SYN-1's acceptance**. No row changes. |
| **Header and product** | header; Short names; Not claimed | r4's acceptance and r5's purpose are recorded. Product main is now `5214350` (88 contract successors; inventory v135). Of the product files J1 cites, only `operation_guard.rs` has changed since `3e64266`. X4-F1 changed its lines 225-241, and the lines J1 cites there (:99-106) are unchanged. |

## r4 changes

| Source | Where | Change |
|---|---|---|
| **M3D SD-6: row R10a** (M3D item 24, M3D:764-769) | item 4: the order table, the R10a bullet; 5.2's J-β | **R10a, the pre-draw component admission,** sits between R10 and R11. After R10's fenced first read yields the authenticated trust view, and before R11's handoff and R12's ExecutionId draw, D4's `components/manifest.rs` admits every component manifest that the trust view admits and that the analysis step can select. It refuses the manifest-class excluded forms EE-1, EE-3b, EE-4's manifest part and EE-5a. A refusal there draws and reserves no analysis-attempt ExecutionId. Its route is M3D item 24's: the internal `ExcludedForm`, projected by J1 with existing codes under M3D's SD-5 (S20). J-β's range becomes R4-R10a. |
| **SD-6: the ephemeral counterpart** | item 6 | **ER10a** is the last step under the read session's fence, after X4T's report-only trust admission. The ephemeral attempt starts, and so draws and reserves its ExecutionId, only after ER10a returns. With no trust view (E-3, E-4), ER10a admits nothing and refuses nothing. |
| **SD-6: the first-use exception** | item 4's R10a bullet; J-C10b | Quoted as M3D r3 states it. The creation prelude's ExecutionId, drawn and reserved earlier in `mint_intent`, may already exist at R10a. It names the creation act only and is never bound to the analysis attempt. |
| **SD-6: controls and successors** | item 4 (J-C10b); item 13 (S19, S20); Forbidden substitutes; Short names | **J-C10b** is the placement half of M3D's D4-T1. It samples the reservation registry when R10a returns its refusal, before step 1's render draw. **S19** is M3-C r7, which narrows M3C item 16's row 8 to a selection among R10a-admitted manifests. **S20** records the SD-5 projections that R10a's route needs. One forbidden-substitute line is added, and one short name, **M3D**. |
| **Record correction** (found by the J-RW r1 drafter, X-RW-8; record only) | item 11 | r3's "A `repair recover` command is M5 (BP:973)" is withdrawn. `repair-recover` is the source-repair journal recovery command (CINV:988-989; WS:1024; SL:673), not a storage repair. |

## r3 changes and review responses

| Finding | Change |
|---|---|
| J1-R2-01 (the window and publication) | 8.1: `Ok(PreparedCommit)` is a continuing result and leaves the window **open**. The window closes only on `prepare_commit`'s error returns and on every return of `publish`, the successful sample included. Put simply, it closes in the step that produces the operation's `StoppedSession`, and only there. The CAS loops keep the word's window bits. 8.6, S10, S11 and J-C15 follow. New control J-C15b cancels during `publish` after a successful preparation. r2's J1-N1 sentence, "closed on every return of `prepare_commit` and `publish`", is withdrawn. |
| J1-R2-02 (the renderer-failure route in phase O) | 8.2's phase O, 8.4, S18 and matrix rows 43 and 44 make the route depend on committed evidence. When a `PublishedCommit` exists, F16 applies (X7:99; WS:1376). Otherwise (ephemeral results, pre-commit refusals, undetermined commits, an interrupt with no Run) the route is WS:1377, row 44's `DELIVERY.REQUIRED_PROJECTION_FAILED`, with no runId, under WS:233-240's aggregate. An uncertain step 0 keeps its ExecutionId disclosure. New control J-C14b. |
| J1-R2-03 (the ephemeral path and S18) | One common rule (5.3, item 6). **Before S18 is accepted:** no output path that uses phase O is wired, neither J2c's nor J3d's. Item 6's ephemeral rule stays as written: phase A only, under WS's before-settle rule. **Once S18 is accepted:** both paths use A (D only where a Run committed), then the output decision point, then O, then E. J2c is gated on S18 exactly as J3d is. New ephemeral controls go before the decision point, inside O and after settlement (J-C14c). |
| J1-R2-NB-01 (recording a signal in phase O) | Adopted. "Recorded with arrival phase O" means: the host cancellation source classifies the signal in memory, and the SOP2 event is attempted with the new `CancelPhase` member `O` (an ordinary registration, SOP2:226-230). After the freeze it counts as post-freeze loss (SOP2:704). No sink is reopened, and the frozen diagnostics do not change. S12-O and J-C14 check the in-memory classification, never a persisted record. |

## r2 changes and review responses

| Finding | Change |
|---|---|
| J1-R1 (precedence) | Item 8.3 now matches the X3d outcome first. Rule 1 is any `CommitUndetermined` (the durability row). Rule 2 is a `Committed(PublishedCommit)` whose `latchedAfterAdmission` is set (X7's F39 row). State 3 alone selects nothing. Phase C (8.2), matrix rows 38 and 42, J-C14 and S12-U follow. |
| J1-R2 (settlement) | The settlement point is now the moment the required output returns, when every required step is terminal (5.3). An **output decision point** (8.4) now ends phase D. From that point to settlement is the **final output section, phase O**: a cancellation-deferral exception that successor **S18** reconciles with the WS and OPP owners, and J3d's output code is gated on it. S12-D now holds at a cancellable D point (`x3d.finish.end-step.after`). The new S12-O holds inside O (`x7.delivery.required.before`). `bootstrap.rs:57-58` is kept. |
| J1-R3 (creation disclosure) | The durable entry's refusal now carries the value-only creation record (item 3, `EntryRefusal { termination, created }`). It is taken from this act's own result: `Published`, or a failure after the publication rename. Item 9's presence rule starts at publication and covers every envelope except the empty-errors `interrupted` branch. The new control is J-C6b. |
| J1-R4 (ExecutionId reservation) | Item 2: every ExecutionId is reserved, uniqueness-checked, in a process-custody `ExecutionIdReservations` before P0, a provider frame or a record uses it (IE:77-81). That reservation is distinct from the durable attempt row (IE:83-101; X3D:114). Only the reserved type reaches a writer. This touches successors S4 and S10 and unit J3a, and adds control J-C4b. |
| J1-R5 (J3d's dependencies) | J3d depends on F2 and G3 again (M3P:265, :451). The critical path is restated (item 14). |
| J1-R6 (refusal families) | Matrix rows 52 to 55 cover native contexts and universe binding (NE:3530), the preparation bound (NE:3531), ambient Cargo configuration (NE:3532; M3C:716) and the authenticated release declaration (NE:3540, :3574). The new control is J-C20b. |
| J1-R7 (audit at M4) | Item 1: the M4 CLI unit replaces the `opensip`, `analyze` and `fit` refusals. `audit`'s refusal stays until its M5 comparison prerequisite exists (BP:955). X11:28's "all four at once" is reconciled per command. |
| J1-N1 (latch minting and window) | Adopted: the latch is minted once per operation, and its window is two bits of the gate's own atomic word. The window is closed on every return of `prepare_commit` and `publish` (8.1). **r3:** that close is withdrawn for `Ok(PreparedCommit)` (J1-R2-01). |
| J1-N2 (SOP2's implementation) | Adopted: J3d depends on O1 (M3P:269, :457). |
| Context | M3-PLAN r6 is accepted (`a6956e88…`). M3-C r5 is accepted in review (`7f76052d…`) and takes effect once M3-L and X12 r4 are accepted. X12 r4 and X2 r9 are accepted by Grok. S-OP-2 is cited by its r4 bytes while r5 is in progress. M2 is complete. Every citation and pin is renewed. |

**Standing direction.** Every item below that says "lead decision" is made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation. Each names the alternative it rejects. The owner may reverse any of them. No item blocks on an owner decision (see "Open questions").

**What this law is.** The M3-J row asks J1 for four things (M3P:265):
1. the X11 successor (X11:64-81);
2. the invocation DAG (WS:76-256) as M3 implements it;
3. the backup-status successor;
4. the commit-phase cancellation join S-OP-12, with the X3D and X7 owners (OPP §5.5, §9).

It also fixes the M3 outcome matrix and breaks J2 to J4 into units.

**The X3D and X7 owners' assent.** OPP names S-OP-12's owning authority as "storage + security (X3D owner) + host finalization (X7 owner)" (OPP:415). Both laws, X3d r8 and X7 r6, are the lead's. Their amendments are written here as successors X3d r9 and X7 r7, as lead decisions under the standing direction. Neither changes before J1 is accepted, and each is reviewed with J1 or right after it.

## Short names

| Name | Document |
|---|---|
| **M3P** | `docs/implementation/m3/M3-PLAN-r9.md`, the M3-PLAN r9 bytes GROK2 accepted (sha256 `72bc7a13…`; `reviews/grok2-m3-plan-r9`). The live `M3-PLAN.md` carries the acceptance note. r9 records the state at its r7 cut-off. **(r5)** r4 and earlier cited r6. Every citation of a fact that r9 still holds is re-pinned to r9's line. |
| **M3P6** | `docs/implementation/m3/M3-PLAN-r6.md`, the r6 bytes GROK2 accepted (`a6956e88…`). J1 r2 to r4 cite it. **(r5)** It is cited only for r6's own words: item 1's quotation, item 14's r6 sizing, and item 15's corrections to r6. |
| **M3P10** | `docs/implementation/m3/M3-PLAN-r10.md`, the M3-PLAN r10 bytes Codex accepted (`ec8c38f8…`; `reviews/codex-m3-plan-r10`). **(r6)** It is cited only for item 14's X4-F3 edge. M3P stays r9. |
| **X11** | `docs/implementation/m2/cli-enablement-x11/PROPOSAL-r1.md`, the X11 r1 bytes (`b98debc9…`) (r6) |
| **X12r4** | `docs/implementation/m2/policy-admission-x12/PROPOSAL-r4.md`, the r4 bytes Grok accepted (`adc9a88a…`) |
| **X12** | `…/policy-admission-x12/PROPOSAL-r3.md` (r3 accepted). Its lines are cited the way other laws cite them. |
| **X3D** | `docs/implementation/m2/commit-session-x3d/PROPOSAL-r8.md`, the X3d r8 bytes (`5e491b92…`) (r6) |
| **X7** | `docs/implementation/m2/finalization-x7/PROPOSAL-r6.md`, the X7 r6 bytes (`9e17faf2…`) (r6) |
| **X3D9, X4r8, X7r7** | the accepted successors S10, S11 and S9 (r6): `docs/implementation/m2/commit-session-x3d/PROPOSAL-r9.md` (X3d r9, Grok, `c727001a…`; `m2/reviews/grok2-x3d-r9`), `live-guards-x4/PROPOSAL-r8.md` (X4 r8, CODEX2 at review round 3, `dc239187…`; `m2/reviews/codex2-x4-r8-round3`) and `finalization-x7/PROPOSAL-r7.md` (X7 r7, GROK2, `7757935c…`; `m2/reviews/codex2-x7-r7`) |
| **X3C** | `docs/implementation/m2/ledger-blob-x3c/PROPOSAL-r8.md`, the X3c r8 bytes GROK2 accepted (`ba638efb…`; `m2/reviews/grok2-ledger-blob-x3c-r8`) (r5). r8 leaves items 1 to 5, 7 and 8 unchanged, so "X3c item 3" and "X3c item 4" (items 2 and 5.4) read the same. |
| **L464, L468** | `docs/implementation/m2/creation-ingress-464/PROPOSAL-r2.md` (464 r2, `a940ba50…`) and `docs/implementation/m2/existing-root-admission-468/PROPOSAL-r5.md` (468 r5, `0959e308…`) (r6) |
| **X2** | `docs/implementation/m2/project-root-x2/PROPOSAL-r9.md`, the r9 bytes Grok accepted (`0d68e3a5…`) |
| **X1, X3A, X4, X4B, X4T, X5, X9, X10** | under `docs/implementation/m2/` (r6): `ordinary-platform-x1/PROPOSAL-r1.md` (X1 r1, `d747adf0…`), `store-admission-x3a/PROPOSAL-r5.md` (X3a r5, `310197d3…`), `live-guards-x4/PROPOSAL-r7.md` (X4 r7, `fc8490f4…`), `trust-bootstrap-x4b/PROPOSAL-r5.md` (X4B r5, `97c2eef3…`), `trust-admission-x4t/PROPOSAL-r11.md` (X4T r11, `7fe098fd…`), `replay-join-x5/PROPOSAL-r3.md` (X5 r3, `d9a101b8…`), `crash-matrix-x9/PROPOSAL-r16.md` (X9 r16, `f08efe95…`) and `read-cli-x10/PROPOSAL-r4.md` (X10 r4, `33095e6c…`) |
| **OWN** | `docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md` |
| **EXIT** | `docs/implementation/m2/EXIT-PLAN.md` |
| **M3B** | `docs/implementation/m3/config-discovery-b/PROPOSAL-r2.md`, the M3-B r2 bytes (`92e65825…`). **(r6)** r5 cited the live file's lines, and that file was r2 plus a two-line acceptance note after line 1, so each M3B line is now 2 lower. M3-B r4 has since been accepted (GROK2). J1 cites r2's bytes. |
| **M3C** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md`, the M3-C r7 bytes CODEX2 accepted in review (`a1ee9386…`, 1232 lines; `reviews/codex2-snapshot-plan-c-r7`). Under its own gate, it takes effect once M3-L is in effect. X12 r4, its other gate item, is accepted. **(r5)** r4 cited r5 (`PROPOSAL-r5.md`, `7f76052d…`). r7 is r5 plus r6's X-C1 and X-C2 and r7's row 8 narrowing (S19). Every line J1 cites keeps its text, and moves by 22 to 49 lines. **(r6; Codex's J1-R5-NB-01 on r5)** 35 of the 36 cited lines keep their text. The exception is item 16's row 8, r7:871 (r5:829), which r7 replaced with SD-6's narrowing (S19). M3-C r8 has since been accepted in review (CODEX2, `578c186e…`; `reviews/codex2-snapshot-plan-c-r8`). J1 cites r7's bytes, and cites r8 by item. |
| **M3D** | `docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`, the M3-D r5 bytes Grok accepted (`224b9228…`; `reviews/grok-supervisor-d-r5`). The live `PROPOSAL.md` differs from these bytes by D's acceptance note. **(r6)** r5 and earlier cited r3 (`PROPOSAL-r3.md`, `9679dbc4…`; `reviews/grok2-supervisor-d-r3`), and each line is re-pinned: 717-722 → 764-769; 717-734 → 764-797; 718 → 765; 719 → 766; 720 → 767; 722 → 769; 733 → 796; 743-746 → 812-815; 748-763 → 827-851; 1091 → 1179-1180; 1092 → 1181. "M3D r3:758" names r3's own line. M3-D r5 cites J1 r4's lines. Row 56 (from SD-5) cites "MD item 24" and row 57 (from M3-D r5) cites "M3-D item 25": items 24 and 25 keep their numbers from r3 to r5. |
| **MH** | `docs/implementation/m3/fact-admission-h/PROPOSAL-r3.md`, the M3-H r3 bytes Grok accepted (`7a562720…`; `reviews/grok-fact-admission-h-r3`) (r5) |
| **M3L** | `docs/implementation/m3/provider-protocol-l/PROPOSAL-r5.md`, the M3-L r5 bytes GROK2 accepted in review (`f654ee4e…`; `reviews/grok-provider-protocol-l-r5`). The law takes effect only when every gate item, L-G1 to L-G11, is met. **(r5; M3L X10)** J1 cites it by item and finding, never by line. r4 and earlier cited r1's lines (`PROPOSAL-r1.md`, `5e858c05…`), and each is re-pinned: :120 → item 2; :375-382 and :377 → item 13; :442-462 → item 16; :450-457 → item 16c; :548 → X3. |
| **JRW** | `docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md`, the J-RW r4 bytes Codex accepted (`9c53bce7…`; `reviews/codex-resume-repair-jrw-r4`) (r6) |
| **I1** | `docs/implementation/m3/preview-pack-i1/PROPOSAL-r2.md`, the I1 r2 bytes (`1eb47d1e…`). **(r6)** As for M3B, each I1 line is 2 lower. I1 r3 has since been accepted (CODEX2). |
| **OPP** | `docs/implementation/m3/operability/PLAN-r3.md`, the OPP r3 bytes Codex accepted (`b49035f2…`). It is cited by section and by line. **(r6)** r5 cited the live file's lines. That file is r3 plus a two-line acceptance note after line 1, so each OPP line is now 2 lower. |
| **SOP2** | `docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, the S-OP-2 r6 bytes Codex accepted with ACCEPT-DESIGN-UNIT (`ce8d3a4b…`; `reviews/codex-s-op-2-r6`). Its accepted bytes still carry r5's title line. It binds with M3-O's O1 unit. **(r5; S18 cross-law item 1c)** r4 cited r4's lines (`PROPOSAL-r4.md`, `db10e19c…`), and each is re-pinned: 205-208 → 226-230; 623 → 652; 623-650 → 652-683; 663 → 704; 710 → 766; 815 → 871; 816 → 872. |
| **AQP** | `docs/implementation/m3/analysis-quality/PLAN-r6.md`, the AQP r6 bytes (`8aed6eb8…`). **(r6)** As for OPP, each AQP line is 2 lower. |
| **WS, IE, SL, NE** | `docs/v2/contracts/product-v1/{workflows-and-surfaces, identity-and-evidence, security-and-lifecycle, native-evidence}.md` |
| **RTC** | `docs/coop/design-corrections/foundation/run-termination-contract.v1.md`, the run-termination contract (r6). WS:1399-1414 makes it the owner of a committed Run's analysis projection, and its §7 the composition law for a step termination's `executionId`, `domainDetail` and `authority`. |
| **BP** | `docs/v2/architecture/implementation-boundaries-and-build-plan.md` |
| **CINV, WFC** | `docs/coop/design-corrections/workflows/{command-inventory.v3.json, workflow-cases.v1.json}` |
| **ENV7, COMMON4, INV5** | `opensip/schemas/sources/{command-envelope-v7, common-v4, invocation-v5}.schema.json` |

**(r6) Every law and plan that has an accepted snapshot is pinned at it.** r5 pinned seventeen at their live files. For thirteen of them, the live file J1 r1 to r5 read differed from its snapshot by at most one line, edited in place by the acceptance record, and J1 cites no such line, so each pin above keeps every cited line. For M3B, I1, OPP and AQP, the live file was the snapshot plus a two-line acceptance note after line 1, so each of their line numbers drops by 2. Many of those live files now hold a later revision, nine of them J1's own successors (item 13). J1 cites the bytes it was read against. For its own successors, those are also the bytes its amendments are stated against, and the accepted successors are cited by their own short names (X3D9, X4r8, X7r7) or in item 13's rows. EXIT, the M2 exit plan, has no snapshot: the lines J1 cites from it (EXIT:169-171, :186-191) are unchanged since J1 r1.

Product paths are under `opensip/` at main `3e64266`. They were read, not run. **(r5)** Product main is now `5214350`, with 88 contract successors and inventory v135 (P0). Between the two commits, the only product file J1 cites that changed is `crates/security/src/custody/operation_guard.rs`. X4-F1 changed its lines 225-241, and the lines J1 cites there (:99-106) are byte-identical. Every product citation stands. **(r6)** Product main is now `1799d3d`, with 99 contract successors and 96 inventory successors, v136 selected. No product file J1 cites changed between `5214350` and `1799d3d`: the last commit, CRC-2's binding, changed only `design-lock.json`.

## Problem

**What exists at `3e64266`.**
- **The binary.** It wires metadata and `doctor` only (`apps/cli/src/arguments.rs:86-108`). `opensip`, `analyze`, `fit` and `audit` refuse, and X11a pins that byte for byte (`apps/cli/tests/creator_commands_tests.rs:484-554`).
- **The request identity.** RequestId is drawn under process custody before parsing (`apps/cli/src/bootstrap.rs:14-24`; `crates/host/src/request.rs:15-55`). That registry says that "durable host audit custody uses the separately implemented durable ingress" (`request.rs:16`), and no such ingress exists.
- **The creator.** `run_initial_creator` (`crates/security/src/custody/installation_routing.rs:66-86`) runs these steps on every call:
  - the attempt, actor, core and platform;
  - the creation intent, which draws its own RequestId and ExecutionId (`crates/security/src/initial_installation.rs:591`) and writes "first use creates the installation" to the disclosure writer (`:430-437`, `:602`);
  - only then the creator act, which may find I present (`NotPristine`);
  - and the gate (`installation_routing.rs:90-119`).
- **Finalization.** `finalize` replays the candidate first, then calls an `admit` closure for the X1 and X2 admissions, then opens the session (`crates/host/src/finalization.rs:395-422`). X3d draws the ExecutionId at `CommitSession::open` (`crates/security/src/custody/commit_session.rs:313-345`).
- **The commit gate.** It latches only from the observer or a failed checkpoint (`crates/security/src/commit_authority.rs:26-48`; `custody/operation_guard.rs:99-106`). Nothing reaches it from a signal.

**Five gaps.**
- **G1. No creator-class command can commit, even in steady state.** The creator's route drops `InitialCore` before the gate, so its `AdmittedInstallation` has no store (X3A:31-36) and no trust bootstrap (X4B:64, :181). X1 item 7 forbids a second entry in the process (X1:49-54). Every creator-class invocation would also mint an intent and print the first-use notice, whether or not I exists.
- **G2. The lease and the attempt identity are in the wrong place for analysis.**
  - IE:1657-1658 requires one writer to hold the lease "through source admission, evaluation and atomic commit". X5 item 3 and `finalize` replay before any admission (X5:39-43).
  - Providers carry the attempt's `executionId` on the wire before they spawn (M3L items 2 and 13). X3d draws it only at the session's open, which today follows evaluation.
- **G3. Two RequestIds.** The intent's and the envelope's are separate draws (X11:74).
- **G4. No signal reaches the commit gate.** That is S-OP-12 (OPP §5.5, OPP:328-338).
- **G5. Three things are missing:**
  - the backup-status carrier (X11:47-56; L468:53);
  - an ephemeral path;
  - the M3 outcome matrix.

## Decisions

### 1. Which commands go live at M3: none in the binary (lead decision)

- **Decision.**
  - **The binary.** No analysis word is wired in `opensip` at M3. `opensip`, `analyze`, `fit` and `audit` keep X11 r1 item 2's refusals byte for byte (X11:30-45). X11a's pins keep passing unchanged. `help` and `completion` keep the four-row catalogue. `doctor` and the metadata commands are unchanged.
  - **What goes live.** One host-library entry, `opensip_host::invocation::run` (the name is J2a's), for exactly three requests:
    - `default`, durable;
    - `analyze`, durable;
    - `analyze --ephemeral`.

    Each runs the step list `[analysis, render]` (item 5). Its callers are host tests (`workflow_tests.rs`, the COV:7865 owner) and the internal harness (AQP:498).
  - **Not at M3:** `fit` and `audit`. `fit`'s steps are `analysis, query, render` (CINV:188), and query is M4 (BP:956). `audit`'s steps are `analysis, analysis, comparison, render` (CINV:257), and comparison is M5 (BP:955). Neither is in the M3 request type. Their durable entry is item 3's, unchanged, when their commands land.
  - **Format.** The M3 request carries one format, JSON (ENV7). Human, SARIF, HTML and agent output are M4 (BP:888).
  - **What the entry takes.** It takes the disclosure writer, the output handle, `InvocationModeV1` and a cancellation source as typed arguments. It never takes a home, profile or release selector (X11:66; X10 r4 item 5).
  - **Which unit replaces which refusal (r2, J1-R7).** Each refusal is replaced by the unit that delivers its command, once every prerequisite of that command exists (BP:895, BP:951-955):
    - the **M4 CLI unit** replaces the `opensip` (default), `analyze` and `fit` refusals. `fit` also needs its M4 query step (BP:956);
    - **`audit` keeps X11 r1's refusal through M4.** Its comparison step is M5 (BP:955), and the M5 unit that delivers comparison replaces it.

    X11:28's "the M3 unit replaces all four refusals at once" was written before the milestones were split. It is reconciled per command here, and J1 does not call any collective enablement an M4 unit. The M4 CLI unit also wires:
    - standard error as the disclosure writer;
    - standard output as the output handle;
    - `isatty(0) && isatty(2)` into `InvocationModeV1` (M3B:112-116). No automation flag is added (M3B:116), so no CINV successor is needed at M3;
    - the SIGINT, SIGTERM and SIGHUP handlers into the cancellation source (item 8).
- **Basis:**
  - BP:887: "Complete CLI analysis delivery follows at M4 with every advertised renderer";
  - BP:895: "Every command delivery also waits for all of its advertised renderer milestones … not releases with silently reduced format contracts";
  - BP:951-955: `default`, `analyze` and `fit` are M4, `audit` is M5;
  - M3P6:110 and M3P6:468 ("nothing is wired. J1 fixes the order and identity rules"), which M3P now records as decided (M3P:166, :619);
  - AQP:498 (the dogfood checkpoint "is not CLI `analyze`") and AQP:500 (CLI dogfood is M4);
  - M3B:718, M3B:902.

  Every non-release build ends at InitialCore F0, and this host is BASELINE-ATTESTED (X11:42-45). A live command would therefore give the owner nothing observable at M3.
- **Rejected:**
  - **Wiring `analyze` and the default at M3 with JSON only.** That moves two command rows ahead of their renderer milestone (BP:895).
  - **A hidden or feature-gated CLI word for the harness.** X11:118 forbids an argument, feature or `cfg` seam in the binary. The harness calls the library.
  - **Shipping X11's "create, then refuse".** X11:20-21's reasons b and c still hold for the binary.
  - **Replacing all four refusals in one M4 unit (r2, J1-R7).** That would deliver `audit` before its M5 comparison prerequisite (BP:895, BP:955).
- **Forbidden substitutes:**
  - an analysis word wired in `apps/cli` at M3;
  - a binary seam;
  - a library entry that selects a home, profile or release;
  - `fit` or `audit` in the M3 request type;
  - an `audit` word wired before its M5 comparison step exists.
- **Controls:**
  - **J-C1.** X11a's tests stay green on every J unit's integration commit, its source pin included (`creator_commands_tests.rs:484-554`). J's units name no forbidden symbol in `apps/cli/src`, `host/src/{outcomes,doctor_ingress,request,lib}.rs`. The new security entry of item 3 is a different function, and `run_initial_creator` and `admit_ordinary_writer` stay `pub(crate)`, each defined once.

### 2. One request identity per invocation, and the attempt identities (lead decision)

- **Decision.**
  - **The RequestId.** One per invocation, minted at ingress before parsing and admission (WS:78; IE:61-62) by the host's process-custody `RequestAuthority` (`request.rs:15-55`). It serves as:
    - the envelope's `requestId`;
    - the correlator of every operational record (OPP §3.1; M3L item 13);
    - on the creation route, the RequestId that P0's `OperationInputV1.invocation` records.
  - **The handoff to security (successor S4, a 464 r3 amendment).** A sealed value `RequestIdentity` lives in `opensip-platform`. It is minted only by the CSPRNG draw (`request_entropy`). It has no constructor from bytes or text, and it is not `Default` or deserializable. The host's registry reserves it, and the host lends `&RequestIdentity` to item 3's entry. `mint_intent` records it and draws no RequestId of its own: it still draws its ExecutionId (`initial_installation.rs:591`). An ephemeral request involves no security draw.
  - **Uniqueness (stated limit).** IE:77-79 requires a reservation "in the corresponding operational ledger before use". For a host that serves one request per process (X10:30), that ledger is the process-custody registry (`request.rs:15-16`, `:28-41`), as for metadata and doctor.
    - M3 keeps no durable RequestId registry. The 128-bit CSPRNG draw is the cross-process argument.
    - The durable traces are P0, on first use, and S-OP-1's file sink once it is accepted.
    - A retained invocation record, which WS:119-123's mutation replay scope needs, is M5's, with mutation steps.
  - **ExecutionIds.**
    - **The creation prelude** keeps the intent's own draw (L464:34). It names the creation act in P0 only.
    - **The durable analysis attempt** is X3d's draw at `CommitSession::open` (X3D:113-117). Item 7 opens the session at the handoff, so the id exists before any provider spawns. It is the id the attempt row reserves (X3D:130) and the receipt carries.
    - **The ephemeral attempt** gets a host draw at the attempt's start. It never reaches attempt custody (IE:88).
    - **The render step's attempt** gets a host draw that appears only in operational records.
  - **The ExecutionId reservation (r2, J1-R4; lead decision under IE:77-81).** IE §2 is the governing rule. Both identities use "independent 16-byte host-CSPRNG draws, reserved with uniqueness checked in the corresponding operational ledger before use", and that reservation "applies to **every** RequestId and ExecutionId, in every request mode" (IE:77-81). J1 names that ledger for ExecutionIds.
    - **The owner.** A process-custody registry, `ExecutionIdReservations`, lives in `opensip-platform` beside `request_entropy`, because both security and the host draw ExecutionIds. It applies `RequestAuthority`'s discipline (`request.rs:28-41`) to ExecutionIds.
    - **How it reserves.** It holds one reservation set per process. Each draw reserves its 16 bytes only after checking them against every ExecutionId already reserved in the process. A collision redraws, at most eight draws in all, as `RequestAuthority` does (`request.rs:32-40`).
    - **When it refuses.** Exhaustion, or a failed draw, refuses on the drawing owner's existing host-I/O row: security's HostIo row (X3D:278; L468:48), or the host's `HOST.IO_FAILURE`. No code is added.
    - **No release.** A reservation is never released or reused in the process.
    - **The sealed result.** The registry returns `ReservedExecutionId`. It has no constructor from bytes or text, and it is not `Default` or deserializable. P0's writer, the provider frame builders, `CommitSession`, the attempt row and the operational record take only that type or its read-only projection, so a bare draw reaches none of them.
    - **Who reserves which id:**
      - the prelude's, in `mint_intent`, before P0 is staged (S4);
      - the durable attempt's, in `CommitSession::open` (S10). It keeps its security-owned draw (X3D:114) and reserves it in the same step, before the session exists, so before any provider frame;
      - the ephemeral and render attempts', in the host, at each attempt's start.
    - **Its relation to attempt custody.** The process reservation is IE:77-81's pre-use uniqueness reservation. It is not a durable record.
      - A durable, commit-capable attempt is reserved a second time, durably, by X3c item 3's attempt row at `prepare_commit` step 4 (X3D:130; IE:83-101). That row's no-replace trigger refuses a reused ExecutionId (F34; X3D:134).
      - The ephemeral and render ids never reach attempt custody (IE:88).
    - **Stated limit.** Until an id reaches attempt custody, cross-process uniqueness rests on the 128-bit draw. As for RequestIds, M3 keeps no permanent ExecutionId ledger.
    - **The crash-matrix census.** `x3d.session.execution-draw` keeps its name and place (X9:939). The reservation is in memory and adds no durability point. F34's `inject-id` still reaches the attempt row's trigger, because an earlier run's injected id is not in this process's registry.
  - **Phase-lawful identities.** OPP §3.1's table holds, with one reading fixed. For a durable request the ExecutionId is lawful from the session's open (OPP:154's "attempt admission"; item 7), which is the attempt's start. That open precedes the attempt row (X3D:130), and item 8 uses "attempt admitted" for the attempt row only, as OPP §5.5 does (OPP:333).
- **Basis:** WS:78-82; IE:61-63, IE:77-81, IE:83-101, IE:88; L464:13-21 and :34; X3D:114, :130-134; X11:74; OPP §3.1 (OPP:143-158); M3L item 13; `request.rs:28-41`.
- **Rejected:**
  - **Binding the envelope's id to the intent's.** The intent exists only on the creation route, after F0, the probe and the actor. A refusal before it (parse, F0, a probe custody row) still needs a RequestId, which is "retained for refusal as well as success" (WS:78-79).
  - **Binding the prelude's ExecutionId to the analysis attempt.** X3d item 2 would have to take an id carried across the creator/ordinary boundary, and the shared RequestId already gives the correlation.
  - **A durable RequestId ledger at M3.** It is a new state class with no carrier.
  - **(r2) Treating the CSPRNG draw, or the draw's ledger charge, as the ExecutionId reservation.** IE:77-81 asks for a uniqueness-checked reservation. A draw is not one, and a budget charge is not an identity reservation.
  - **(r2) A permanent ExecutionId ledger at M3.** It has no carrier, and attempt custody already reserves every id that can commit.
  - **(r2) One registry for RequestIds and ExecutionIds.** IE:77-79 reserves each "in the corresponding operational ledger".
- **Forbidden substitutes:**
  - two RequestIds in one invocation;
  - a RequestId from a caller, from text or from a draw other than the ingress's;
  - any identity on a provider's wire beyond those M3L item 13 lists (r5, M3L X14; FA-2's X-FA2-J1). Item 13's list is derived from the cited schemas and re-derived by its control L-C1;
  - a RunId before `Committed` (OPP:155);
  - (r2) an ExecutionId used by P0, a provider frame, a session or a record before its process reservation; a reservation released or reused.
- **Controls:**
  - **J-C2.** On the creation route, P0's `invocation.requestId` equals the envelope's `requestId` and every record's. No second RequestId appears anywhere in the invocation's output, records or P0.
  - **J-C3.** Provider frames carry the session's `execution_id()`, and the receipt carries the same ExecutionId.
  - **J-C4.** `RequestIdentity` has no constructor but the draw. This is a compile-fail fixture under X8's driver.
  - **J-C4b (r2).** The ExecutionId reservation, with forced draw sequences as `request.rs`'s `allocate` tests use:
    - a repeated draw is redrawn;
    - eight collisions refuse on the drawing owner's row;
    - `ReservedExecutionId` has no other constructor, and P0's writer, the frame builders and `CommitSession` accept nothing else (compile-fail fixtures);
    - a first-use durable invocation reserves three distinct ExecutionIds (prelude, session, render), and none of them is used before its reservation.

### 3. The durable entry: the creator's host entry, first use and steady state (lead decision)

- **Decision.** Each durable request makes exactly one security call: `enter_durable_analysis(command, backup_custody_flag, &RequestIdentity, disclosure) -> Result<DurableEntry, EntryRefusal>`. The name is J3a's. It is one call, with no producer injection and no home, profile or release selector (X11:66). It runs:
  1. **Producers, on the process's attempt A:** the attempt, the actor, InitialCore and InitialPlatform (`read_premise.rs:331`, `produce_on`).
     - A development build ends at F0 here, `CORE.NO_EMBEDDED_RELEASE`, before any path is opened and with no disclosure.
  2. **The presence probe.** One charged, fence-free, no-follow walk from `/` to I, under gate step 0's custody predicates and premise (L468:15; X1:32's positive absence). It has three outcomes:
     - `Present`;
     - `PositivelyAbsent`: the first missing fixed-suffix component, under its retained parent;
     - a custody, I/O or budget refusal on its L468 item 6 row.

     The probe selects a route and nothing else. It is never authority: the ordinary gate re-establishes presence under the fence, and owner §1a step 6 re-establishes absence for the permit (OWN:26).
  3. **Route.**
     - **3a. `Present` (steady state).** Attempt A's producers are sealed as `PlatformReceipt<Write>`, with no intent and no disclosure. Then X1 item 2's steps 2 to 4 run: recheck, gate, recheck (X1:22-30). The result is an `OrdinaryWriteAdmission`, from one attempt and one gate.
     - **3b. `PositivelyAbsent` (first use).**
       1. The intent is minted on attempt A with the lent RequestId (S4). Its notice is written and flushed before any effect, and a failed write is HostIo (L464:27-32).
       2. The creator act runs (465 to 467) and ends `Published`, `LostRace` or `NotPristine`.
       3. Attempt A is dropped with its core and platform (L468:7; 467 item 9). The creator act enters no gate.
       4. `admit_ordinary_writer()` runs on a second attempt B: X1 item 2's steps 1 to 4, with fresh producers and the process's one gate (X1:22-30; `custody/ordinary_writer.rs:493`).
       5. The result is an `OrdinaryWriteAdmission`.
  4. **What it returns (r2, J1-R3).** On success it returns `DurableEntry { admission, created }`. On refusal it returns `EntryRefusal { termination, created }`. In both, `created: Option<Created { classification, target }>` holds values only and carries no authority from attempt A.
     - **When `created` is `Some`.** Exactly when this invocation's creator act performed the exclusive publication rename. That covers the act's `Published` result, and a refusal after the rename, which L468's host-I/O row covers as "any failure after the rename" (L468:48).
     - **Where it comes from.** The act's own typed result, never a later existence scan or the fact that an intent was minted.
     - **When it is `None`.** For `LostRace` and `NotPristine`, which published nothing, and for every refusal before the rename.
     - **What carries it.** Every later path keeps it: attempt B's producers, gate, barriers and rechecks, and every refusal after R3. Today's `route` drops it (`installation_routing.rs:107-118`); S2 records the change.
- **The probe's race.** Suppose the probe says `Present`, but the gate's walk then finds I positively absent, because I was deleted outside OpenSIP. The request ends on L468's `INSTALLATION.NOT_INITIALIZED` row (L468:40), whose remedy, "run an admitted durable analysis", is the true next step.
  - **Rejected:** the custody row. I is absent, not foreign.
- **How the creator command ends (X11:67-73; X3A:36).** It does not end after creation. The first-use invocation continues as an ordinary writer through the whole durable DAG, and its termination is the analysis's (item 10). What it tells the user:
  - the standard-error notice (L464:27-32);
  - the envelope's `retentionDisclosure`, with `firstUse` and `backupStatus` (item 9).
- **The creator terminations (X11:74-75).** Every probe, creator, gate and recheck refusal ends on its L468 item 6 row (L468:35-50) through `installation_termination`. It is projected as X10 r4 item 3's refused branch: `kind: failure`, `errors` holding the row's detail (or `HOST.IO_FAILURE`), and exit 2 or 4. When `created` is `Some`, every such envelope, including a refusal at attempt B, carries `retentionDisclosure` with `firstUse: true` and `backupStatus` (X12r4:200; item 9). The empty-errors `interrupted` branch is the one exception (ENV7:790).
- **The F0 restatement (X11:78-80).**
  - A development build ends at F0 in step 1. That is before the probe, the intent, any disclosure, the fence and pack admission.
  - X11 r1 item 5.8's "after pack admission" followed X12 r3's order. Under X12 r4, pack admission follows the fence, so F0 now precedes it.
  - A release build on this BASELINE-ATTESTED host ends at the probe's custody refusal at `/` (L468:45; X10 r4 "Not claimed"), before any intent or notice. Today's composition mints the intent first.
- **The amendments.** All are lead decisions, recorded as successors S2 to S8. None changes a public code, class, exit, subject or remedy.
  - **L468 r6, item 1.** `Published`, `LostRace` and `NotPristine` end the creator act. The invocation continues through X1's ordinary admission on a fresh attempt, not through a gate lent by the creator's `InitialPlatform`. L468 item 2's sealed capability is unchanged, and attempt B's `InitialPlatform` lends it. **r2:** the act's result, and its post-rename refusals, carry the value-only `created` record above. Their rows are unchanged.
  - **X1 r2, item 1.** The durable creator-class entry is a third producing entry. It fixes the Write purpose after the probe and before any receipt exists, so no receipt converts.
  - **X1 r2, item 7.** One entry per process holds, with one exception, the creator-class sequence: one creator act on attempt A, then exactly one `admit_ordinary_writer` on attempt B. The sequence is allowed only after the creator act ended `Published`, `LostRace` or `NotPristine`.
    - The attempt allocation (`initial_installation.rs:28`, `:96-99`) becomes a two-slot sequence. A non-Clone `CreatorActEnded` token is returned only by the creator act and consumed only by attempt B's allocation. Any other second allocation stays `Invariant`.
    - There is still one gate per process (`installation_admission.rs:801`).
    - **Also (S3, the ephemeral clause of item 6):** the 458c read receipt is a lawful use of the process's one attempt with or without a session.
  - **X3A r6, item 2.** "A later, separately admitted invocation" becomes "a separately admitted ordinary write operation: a later invocation, or this invocation's attempt B (J1 item 3)". The creator act itself still produces no endpoint.
  - **X4B r6.** The forbidden substitute "acceptance in the creator invocation" (X4B:181) becomes "acceptance in the creator act". The rejected bullet at X4B:64 records that attempt B is an ordinary writer.
  - **X2 r10, item 6.** The branch "or under the creator's `AdmittedInstallation` from 468c" (X2:202) is withdrawn, so first registration runs under an `OrdinaryWriteAdmission` only.
  - **L464 r3, items 1 and 5.** The intent holds the invocation's lent RequestId and a fresh ExecutionId. Item 5's "if a later ordinary operation in the same process ever used these ids" now reads: the RequestId is the whole invocation's, and the prelude's ExecutionId is never reused.
  - **X11 r1, item 1a: reconciled.** Under X12 r4, the creator's installation effects precede pack admission on the creation route (X12r4:197-200). "Creating I first" is therefore the lawful order. X11's M2 decision stood on its other reasons (X12r4:44).
- **Basis:**
  - OWN:21: the four commands use "durable-authoritative mode and the same initialization effect before their named steps";
  - OWN:32: P0 "does not authorize the remaining requested analysis steps";
  - OWN:103: "the creator's first ordinary write admission … a separately admitted write operation";
  - OWN:114: the race loser ends its creator act, then is separately admitted;
  - WS:250-253 and CINV:1747 (`default-first-use-durable`: success 0, in one invocation); WS:1373;
  - IE:1633-1636.
- **Rejected:**
  - **End and rerun** (create, then end, telling the user to rerun). It breaks the first-use golden (CINV:1747; WS:1373) and WS:250-253.
  - **A second process.** It needs a self-exec path from the core tree and a continuation argument in the binary (forbidden by X11:118). It splits cancellation and output across two processes, and it carries the RequestId between them.
  - **Carrying the creator's `InitialCore` through `route`,** to give the creator's `AdmittedInstallation` a store. X3A:38-39 rejects it, and so does 467 item 9.
  - **Running the creator act on every creator-class invocation** (today's composition). Every steady-state `analyze` would print "first use creates the installation" and would still have no store.
  - **Ordinary admission first, then the creator on its `Absent`.** It spends the one gate on the absence, and needs a third attempt and a second gate.
  - **One attempt for both acts.** The creator act's shared budget (OWN:19) and the commit's attempt ledger (X3D:216) would share one ledger at the owner's caps, and attempt A's `InitialCore` would cross the creator/ordinary boundary.
- **Forbidden substitutes:**
  - an intent or notice on a `Present` probe;
  - authority drawn from the probe;
  - a creator observation, handle, lock or receipt reaching attempt B;
  - a second gate or a third attempt;
  - attempt B without `CreatorActEnded`;
  - a store, a trust acceptance or a registration inside the creator act;
  - (r2) a creation disclosure taken from an existence scan or from the minted intent, rather than from the act's own result.
- **Controls** (scratch homes and synthetic V2 profiles, as X1a's):
  - **J-C5.** Steady state:
    - one attempt and one gate;
    - no intent, no notice and no P0 change;
    - standard error is empty unless something else writes to it.
  - **J-C6.** First use:
    - the notice is flushed before the first creation effect;
    - attempt B is fresh: its core and platform identities are re-observed, and no handle of A is retained (a type-level pin);
    - a third allocation is refused `Invariant`.
  - **J-C7.** The probe's three outcomes, and the `Present`-then-`Absent` race ending on `NOT_INITIALIZED`.
  - **J-C6b (r2, J1-R3).** `Published`, then a failure of attempt B:
    - the producers;
    - the gate busy;
    - a barrier failure;
    - a recheck failure.

    Each envelope carries `retentionDisclosure` with `firstUse: true` and `backupStatus: unknown`. A failure after the rename carries the same. A refusal before the rename, `LostRace` and `NotPristine` each give `firstUse: false`, or no member before R3. An `interrupted` envelope never carries the member.
  - **J-C8.** `LostRace` and `NotPristine` each continue to attempt B and commit.
  - **J-C9.** A development build ends at F0 with no notice and no file access. X11a's binary test already pins the binary itself.

### 4. The request order before analysis, and the first-use clause (law)

The durable request runs this order. Each row ends with a typed value the next row consumes.

| Row | Step | Owner and basis |
|---|---|---|
| R0 | RequestId, before parsing | item 2; `bootstrap.rs:14-24` |
| R1 | Typed request admission: the command, the mode, the flags of M3B item 23's table (M3B:718-728), JSON and `InvocationModeV1`. The host builds the step list. A malformed library request is a host-generated layer: `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant` (NE:3573). **(r6; M3-D item 25)** A well-formed request that is a request-class excluded form is not malformed; it takes row 57 (M3-D item 25). | J2a |
| R2 | `installation_entry`: `Creator` for a durable request, `Outside` for an ephemeral one | `request.rs:85-135` |
| R3 | Durable entry → `OrdinaryWriteAdmission`, with the fence held | item 3 |
| R4 | S3's selection walk; X2 r9 item 3a's placement check and chain walk; the carrier captures | M3C:864; M3B:96 |
| R5 | B1 configuration resolution | M3C:865; M3B items 1-11 |
| R6 | X12 pack admission | X12r4:195-206; M3C:866 |
| R7 | The S3.1 storage choice (`grants.rs`), which is pure. Under 464's constant `UNKNOWN` it admits with the notice's disclosure. A positive `BACKED_UP` without the flag is `storage.backup-choice-required` (L468:39). | M3B:376, :727 |
| R8 | X3a's endpoint admission, from the gate's own retained captures, with no new read | X3A:28-29 |
| R9 | X2 item 5's registry capture; X2 item 6's first registration when the root is unregistered, with item 6a's tracking observation | M3C:867; X2:192, :202 |
| R10 | X3b's floor step; the operation's `FreshnessMonitor` and `FinalGate`; X4T's fenced first read, with X4B's acceptance when F is absent | X4:44; X4B:42-56 |
| R10a | **(r4, SD-6) Pre-draw component admission.** D4's `components/manifest.rs` admits every component manifest that R10's trust view admits and that the analysis step can select, and refuses each manifest-class excluded form (EE-1, EE-3b, EE-4's manifest part, EE-5a) as `ExcludedForm {class, subject}`, routed as M3D item 24 fixes. The fence is still held. No analysis-attempt ExecutionId is drawn or reserved. It ends with the admitted manifest set, which M3C item 16's row 8 selects from (S19). | M3D item 24, the owner of what it admits and refuses; CH14:433 |
| R11 | X2 item 7's `APPEND-WRITE` lease; X2e's handoff. The fence is released and the lease is held. | X2:328; `operation_handoff.rs:330` |
| R12 | `CommitSession::open`, which draws the ExecutionId | item 7 |

- **The S3.1 slot (lead decision).** M3B says J3 calls the S3.1 choice "at the first source-derived write" (M3B:376). J1 reads that as "before any project-scoped effect of the durable request" (R7). Like a pack refusal, a storage-choice refusal then leaves no project effect. On first use, the intent has already applied the same choice to the creation (L464:9), and R7 rechecks it against the same classification.
- **The first-use clause (X12r4:33-47, :197-200).** This law owns that clause's control.
  - **Control J-C10.** On the creation route (item 3b), a refused project-layer pack ID at R6 leaves:
    - a complete installation;
    - no registry row, namespace, `.opensip`, marker, lease or journal;
    - the refusal's disclosure of the creation, through the notice on standard error and `retentionDisclosure` with `firstUse: true` (item 9).

    This control is shared with M3C:955-959 (C4-T20) and B1-a.
- **R10a, the pre-draw component admission (r4; M3D item 24, successor SD-6).** J1 places the row. M3D owns what it admits, what it refuses and how each refusal is routed (M3D:764-797).
  - **Its place.** After R10, whose fenced first read yields the authenticated trust view, and before R11's handoff and R12's draw. It does not wait for the Plan's selection, because selection needs discovery, and discovery runs only after R12 (M3D:765).
  - **Its route.** The internal refusal is `ExcludedForm {class, subject}`. Its public projection is J1's, with existing codes, under M3D's successor SD-5 (S20). **(r6)** M3D r5 states it as SD-5's accepted and bound route: request-rejected 2 with `EXTENSION.ADMISSION_REJECTED` (SL:1306; M3D:796). No public code is added. **(r5)** SD-5 is accepted and bound, so the projection is row 56 (item 10): request-rejected 2, `EXTENSION.ADMISSION_REJECTED`, with detail `PAYLOAD-NOT-ADMISSIBLE` and subject `excluded-form:<class>:<manifestDigest>`.
  - **What a refusal leaves.** It comes before R11 and R12, so there is no handoff, lease or `CommitSession`, and neither `refused()` nor `finish` runs (item 7 governs every end after R12). Step 0 ends on the refusal, and step 1 projects it (5.2). When item 3's `created` is `Some`, the refusal discloses the creation, as every refusal after R3 does (item 9).
  - **The first-use exception, as M3D states it** (M3D:769; r6): "On the first-use route, the creation prelude's own ExecutionId was drawn earlier and names the creation act only (J1:176). It is not the analysis attempt's, and R10a creates none." M3D's J1:176 is a J1 r4 line. In this law's terms: on route 3b, whatever the creator act's result, the prelude's reservation, made in `mint_intent` before P0 is staged (item 2; S4), may already be in `ExecutionIdReservations` when R10a runs. It is never bound to the analysis attempt (item 2, "Rejected"). R10a's no-draw property concerns the analysis attempt's ExecutionId only.
  - **What follows it.** M3C item 16's row 8 selects only among the manifests R10a admitted, and adds no admission of its own (S19). The ephemeral counterpart is ER10a (item 6).
  - **Control J-C10b (r4, SD-6).** The placement half of M3D's D4-T1 (M3D:812-815), on its hostile but well-formed corpus for EE-1, EE-3b, EE-4's manifest part and EE-5a. It runs on the steady-state durable path (3a), on the first-use path (3b, once each for `Published`, `LostRace` and `NotPristine`) and on the ephemeral path (ER10a):
    - **Sampled when R10a or ER10a returns its refusal,** `ExecutionIdReservations` holds no analysis-attempt reservation. Its set equals its set at R10a's entry: empty on 3a and on the ephemeral path, and the creation prelude's alone on 3b.
    - On the durable path, R11 and R12 never run: there is no handoff, lease or session, and the census point `x3d.session.execution-draw` is never reached. On the ephemeral path, the ephemeral attempt never starts.
    - No capture session opens, nothing is spawned and no source byte moves.
    - The only reservation added after the refusal is step 1's render draw (item 2), and it is never bound to the analysis attempt.
    - On 3b, when `created` is `Some`, the envelope carries `retentionDisclosure` with `firstUse: true` (item 9).
    - With no trust view (E-3, E-4), ER10a admits nothing and refuses nothing.
- **Rejected:**
  - **Pack admission before the durable entry.** The project carrier is judged only by the fenced selection (X12r4:42; M3B:304).
  - **The S3.1 choice at the commit.** Its refusal would come after the whole analysis and after project-scoped effects.

### 5. The invocation DAG as M3 implements it (law)

**5.1 Step lists** (WS:76-104; CINV:7, CINV:114).

- **`default` and `analyze`, durable:**
  - step 0 is `analysis`: required, `dependsOn []`, gate `completed`, retry `none`, durability `authoritative`, `snapshotSource: live-worktree`;
  - step 1 is `render`: required, `dependsOn [0]`, gate `terminal`, retry `none`, `format: json`, the caller's output handle, `required: true`.

  This is WFC:3612's `default-analyze-render-success`, except for the retry policy.
- **`analyze --ephemeral`:** the same two steps, with step 0's durability `ephemeral` (WFC:3741).
- **`analyze`'s `import` step** (CINV:114) is instantiated only when an import is selected. M3 selects none: the `import` command is M5 (BP:957), and C3's library importer is not a step (M3C:517).
- **Retry is `none` (lead decision).** A second durable attempt would need a second write entry, which X1 item 7 forbids even after S3. WS:105-108 makes idempotent retry lawful, not mandatory. A ledger-busy attempt therefore ends on the busy row (X3D:277), with no `WORKFLOW.RETRY_BUDGET_EXHAUSTED`.

**5.2 The analysis step's joins.** Each join hands the next a typed value. No join is re-entered, and a refusal at any join ends step 0 (`rejected` or `failed`). Step 1's gate is `terminal`, so it then projects that refusal.

| Join | From → to | Owner |
|---|---|---|
| J-α | request → durable entry (R0-R3), or the ephemeral entry (item 6) | J2a; J3a |
| J-β | fence → project admission, configuration, pack, S3.1 and (r4) component admission (R4-R10a) | X2; M3B; X12r4; M3D item 24 |
| J-γ | handoff → the open session (R11-R12) | X2e; X3d; item 7 |
| J-δ | capture session → sealed `snapshot2`: M3C rows 5-9 (M3C:868-872), with downward discovery after the fence (M3B:334) | C1; B2 |
| J-ε | the Plan: M3C rows 10-16 (M3C:873-879). The PlanId is minted at row 14 (M3C:877). Row 15's pre-execution joins come before any provider (M3C:878). | C3; C4 |
| J-ζ | provider stages, one child per `(ExecutionId, SnapshotId, universe key)` (M3L item 2), launched only under the D law and O7 (M3P:627) | D; F; G |
| J-η | H's fact admission; then the **full `admit_enumeration`**, after every stage return is admitted and the host-derived inventories exist, and before `derive_evaluation`. This places it, as M3C:896 asks J1 to. MH item 19 implements that placement unchanged (r5). | H; J2b |
| J-θ | evaluation through `derive_evaluation` with I1-b2 (I1:404). The Plan's policy comes only from an `AdmittedPack` (X12r4:208). | I1; J2b |
| J-ι | finalization (item 7): replay (X5, with X12d's Run-closure join), `prepare_commit`, `publish`, `finish` | X5; X3d; X7 |
| J-κ | step 1, the render step: the projection of what step 0 holds, the **output decision point** (8.4), then the **final output section**: SOP2's finalization (SOP2:652-683), rendering of the decided envelope, and its output and flush (X7 item 4) | X7; SOP2; S18 |

**5.3 Settlement (r2, J1-R2).**
- Step outcomes are the closed set (WS:101-103).
- The aggregate is taken over required steps in D9 order (WS:233-240). The exit comes from the class by the fixed table only (WS:1355-1356; COMMON4 `StepTermination`).
- A required render failure dominates and keeps the runId (WS:236-238).
- **When each step is terminal:**
  - **Step 0** is terminal when its attempt ends. For a durable attempt, that is when `finish` has returned; for an ephemeral one, when the evaluation result is held.
  - **Step 1** is terminal only when its required work is done: projection, rendering and the output of the required envelope (X7:85; `finalization.rs:310-318`). It completes when `deliver_required` returns `Ok`. It fails when the renderer, the output or the flush fails. **(r5; S18 LD-4)** The exception is a step 1 that the output decision point cancels (row D). That step 1 is terminal at the decision point, but its termination output is still rendered and written in a final output section, and a renderer failure before any byte fails it.
- **The settlement point (r5; S18 LD-4)** is the moment when every required step is terminal and the required output has returned (WS:227-228, as S18 states them). For a step 1 that completes or fails, that is the moment it becomes terminal. For a step 1 cancelled at the output decision point, it is later: the return of its termination output. The invocation is settled there, and not earlier (WS:224-228; OPP:335-336).
- **The output decision point** (8.4) comes before settlement. It fixes which envelope is rendered: the decided class, or `interrupted` for a signal observed in D. It does not settle the invocation, even where it cancels step 1 (r5; S18 LD-4).
- **The final output section, phase O,** runs from the decision point to the settlement point. A signal observed there is deferred: it is recorded with arrival phase O (8.2) and never changes the envelope already decided. This was a cancellation-deferral exception to WS's before-settle rule (WS:224-226), forced by the single required envelope (`bootstrap.rs:57-58`; L464:32).
  - **(r5)** S18 is accepted and bound (product `5214350`), so the rule is now WS's own. WS:225's before-settle ends at the output decision point. The "Final output section" paragraph after WS:231 defers the signal. WS:227-228's after-settle begins at the settlement point. r4's "J1 does not claim the existing rule covers it" is withdrawn.
- **One common rule, and one gate (r3, J1-R2-03).** The durable and ephemeral step lists share the same required render step (5.1), so the rule is the same for both:
  - **Before S18 is accepted,** no unit wires an output path that uses phase O. That means neither J3d's durable output nor J2c's ephemeral output. Every rule stands as WS:224-228 writes it. Authoring and testing the pure state models, and every part of J2c and J3d short of output wiring, may go ahead.
  - **Once S18 is accepted,** both paths use the same phases: A (and D, only where a Run committed), the output decision point, O, then E (8.2). J2c and J3d are gated on S18 alike (item 14). **(r5)** S18 is now accepted: GROK2 accepted it at r2, and it is bound at product `5214350`.
- Interruption follows item 8 (WS:224-231).

**5.4 The choices M3-C hands J1.**
- **(a) Candidate blob custody (M3C:137), lead decision.** Both modes capture into the invocation's private temporary custody. The durable commit publishes from the replay's retained evidence, through X3c item 4, at `prepare_commit` step 6 (`crates/storage/src/commit.rs:243-266`). Nothing is written to the store before the attempt row.
  - **Rejected:** capturing into `I/stores/S`'s CAS during analysis. That would mean store effects before attempt admission and before the publication reserve (X3D:128), orphans on every refusal or cancellation, and a contradiction of S-OP-8's placement, which assumes none (OPP §5.4).
- **(b) The lease (M3C:210).** The writer lease is held from R11 through the commit (IE:1657-1658). The capture walk and discovery run under it, never under the fence (M3B:334).
- **(c) The public projection of `SnapshotBound`, `DependencySetBound` and `DependencyAcquisitionBound`** (M3C:313, :599, :613). J1 adopts S-B: request-rejected 2, `REQUEST.UNSATISFIABLE`, detail `PROJECT.SCOPE_LIMIT`, subject `field:count>limit`, with no Plan and no Run (NE:3534; M3C:964). J's units that can reach these refusals are gated on S-B (M3C:1057).
- **(d) Where the full `admit_enumeration` runs:** J-η.

**5.5 Forbidden substitutes:**
- a step list other than 5.1's;
- a retry;
- a re-entered join;
- an evaluation before J-η;
- a Plan policy not taken from an `AdmittedPack`;
- a store write before the attempt row;
- a downward walk under the fence;
- a refusal with no route.

### 6. The ephemeral path (lead decision; four joins owed by other laws)

- **Decision.** An ephemeral request observes what is lawful to read and writes nothing durable.
  - **The entry.** `Outside` (`request.rs:92`). It goes through the 458c read entry (X1:52): the read receipt on the process's one attempt. It never uses the creator, the ordinary writer or the write gate. It never creates, registers, bootstraps, takes a lease or writes (OWN:28; SL:1521; IE:88, IE:1639-1641).
  - **Core identity.** The read receipt's InitialCore gives the Plan's evaluator closure (EC1; X3D:65-68). A development build ends at F0.
  - **I complete.** Under the read session's fence (X2:169; X12r4:195), the request runs:
    - S3's selection and captures;
    - layer 2, through the session's private-access judgment (M3B:89, :95);
    - configuration resolution and pack admission;
    - X4T's report-only trust admission (X4T:123), with no X4B acceptance (X4B:58);
    - the registered ProjectId when the root is registered, and E-2's otherwise;
    - **(r4, SD-6) ER10a,** R10a's ephemeral counterpart (item 4; M3D:767): the same pre-draw component admission over the report-only trust view, with the same refusals and routes.

    It reads no store and takes no lease. Then the read session's equivalent release (M3B:334; X2:84) comes before the capture session.
  - **I positively absent.** There is no session. Layer 2 is absent: "absent is no layer" (M3B:89). Joins E-1 to E-3 then apply.
  - **I present but incomplete.** The request refuses on the read path's row (L468:46). It never degrades to the absent shape.
  - **The ephemeral attempt's draw (r4, SD-6).** The ephemeral attempt starts, and so draws and reserves its ExecutionId (item 2), only after ER10a returns. A refusal at ER10a therefore draws and reserves no analysis-attempt ExecutionId. With no trust view (I positively absent, E-3; or F absent, E-4), ER10a admits no manifest and has nothing to refuse (M3D:767).
  - **The projection.** X7 item 2's ephemeral projection: authority `ephemeral`, no runId (DR-G27; X7:87-93). A failing verdict is policy-failed 1 with `authority: ephemeral` (WS:247-248). Custody is temporary (5.4a).
  - **Cancellation (r3, J1-R2-03).** Before S18 is accepted, cancellation has phase A only, under WS's before-settle rule, and J2c wires no output (5.3). Once S18 is accepted, the common rule applies: A runs through step 1's projection to the output decision point, with cooperative cancellation and no commit gate; then O, the deferred final output; then E, after actual required-step terminality. Phases B, C and D never occur, because an ephemeral request has no commit.
- **Joins owed by other laws.** J2c, the ephemeral entry end to end, waits on all four. J2a and J2b do not.

| Join | Owner | Need | Lead recommendation |
|---|---|---|---|
| **E-1** | M3-B and X2 (successor S7b) | S3's selection and carrier captures with no installation fence, when I is positively absent. They produce no `ProjectRootAdmission` and grant no registry read, registration, marker or lease. | the same custody predicates on the ephemeral ledger. The fence protects I, and no I exists. |
| **E-2** | M3-C (`snapshot2` takes `projectId` from X2, M3C:342) | the ProjectId of an unregistered root, or of a request with no I | a fresh per-invocation draw that is never persisted or compared. Such PlanIds are not comparable across invocations, and that is stated. |
| **E-3** | M3-C item 7 (closure admission is TR-INDEX-verified by the trust owner, M3C:362-365) and X4T | what an ephemeral request admits with no admitted trust view (I absent, or F absent) | no manifest-admitted closure. Each capability it would serve is provider-unavailable: indeterminate 3, `COVERAGE.PROVIDER_UNAVAILABLE` (NE:3370), `authority: ephemeral`, no runId and no detail, never silently dropped (BP:887). **(r6, lead ruling)** RTC §7.4 admits no §7.5 detail on an ephemeral attempt, so r5's `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` (WS:1374) is dropped from this form. M3-C r8 (accepted in review) states the same form for E-3's C half (LD8-5). |
| **E-4** | X4T | F absent under an ephemeral read session | not a refusal: there is no trust view (E-3). Every other X4T refusal (authentication, floor, rollback, continuation) refuses on its own row (X4T:139-150). |

- **Rejected:**
  - **An ephemeral path that never opens I.** It ignores the user's layer 2 (M3B:89, "always") and can admit no closure at all (M3C:362-365). That makes it indeterminate on every machine.
  - **Writing temporary custody inside I.** Forbidden by SL:1521.
- **Forbidden substitutes:**
  - any write, lease, registration, bootstrap or creation by an ephemeral request;
  - a runId or authoritative label on an ephemeral result;
  - an X4T refusal other than F absent degraded to "no trust";
  - an absent-shape run over an incomplete I.

### 7. Finalization: the session opens at the handoff (lead decision; successors X5 r4 and X7 r7)

- **Decision.**
  - **When the session opens.** It opens at R12, right after the handoff and before the capture session. There are two reasons:
    - the attempt's ExecutionId must exist before any provider spawns (M3L items 2 and 13; WS:81), and X3d draws it at `open` (X3D:114; `commit_session.rs:322-345`);
    - IE:1657-1658 requires the writer to hold the lease through source admission, evaluation and commit.

    Opening early changes no security or storage code. X9's census already reaches `x3d.session.execution-draw` right after the handoff (X9:939).
  - **What `finalize` takes** (`finalization.rs:395-445`). It takes the open `CommitSession` and the evaluation candidate, and no longer takes an `admit` closure.
    - Replay (X5) still runs first, before `prepare_commit`.
    - A replay refusal ends the session with `CommitSession::refused()` (`commit_session.rs:529-531`) and `finish`, then projects the replay row (X5 item 5). No reserve exists, so nothing is appended (X3D:120).
  - **Every other end after R12.** A refusal or cancellation during analysis ends the session the same way, exactly once: `refused()`, then `finish`.
  - **X5 r4, item 3.** "Replay before any custody" (X5:39) becomes: "replay after evaluation and before `prepare_commit`. A replay refusal ends the attempt before any attempt row, object or journal effect, and the lease and session end through `finish`."
    - The rejected bullet "replaying under the project lease" (X5:43) is withdrawn, because IE:1657-1658 fixes the lease through evaluation.
    - X5 items 4 and 6 stand.
  - **X7 r7, item 1.** The order becomes:
    1. the session, opened by the pipeline at the handoff;
    2. replay;
    3. `prepare_commit` and `publish`;
    4. `finish`, after which step 0 is terminal;
    5. step 1's projection of the committed Run, which is still cancellable (phase D);
    6. the output decision point (8.4);
    7. the final output section (phase O): SOP2's finalization (SOP2:652-683), then rendering and output of the decided envelope (the delivery phase, X7 item 4);
    8. the settlement point, when the output returns (5.3).

    X7 item 7 stands: finalization charges nothing.
  - **X3d r9 (record).** `refused()` also ends a session whose attempt never started. It latches the gate. With no reserve, `finish` appends nothing, and it runs its end step only on an open attempt ledger (X3D:204-210).
- **Rejected:**
  - **Drawing the ExecutionId inside `ProjectOperation` at the handoff.** It changes X2e and X3d item 2 and moves X9's census point.
  - **Opening the session only at the commit.** Providers would run under no ExecutionId, or under one the receipt does not carry.
  - **Keeping `finalize`'s `admit` closure, with X1 and X2 admission after evaluation.** That breaks IE:1657-1658 and X12r4's fenced order, and X1 item 7 forbids the second entry an earlier selection would need.
- **Controls:**
  - **J-C11.** The session opens before the capture session. Providers carry its ExecutionId.
  - **J-C12.** A replay refusal, an analysis refusal and a phase-A cancellation each end through `refused()` and `finish`, once, with nothing appended.
  - **J-C13.** X9's F01 host variant is re-transcribed by S12 if `finish`'s end step changes its post-state.

### 8. S-OP-12: the commit-phase cancellation join (lead decision; successors X3d r9 and X7 r7)

**8.1 The latch: a third source for the existing commit gate.**

The operation's one `FinalGate` (X4:44, :115-116; `commit_authority.rs:26-48`) already latches from the observer and from a failed checkpoint. X3d r9 adds the cancellation latch as a third source, with the same two-bit law.

- **The type, minted once per operation (r2, J1-N1).** `CommitSession::take_cancellation_latch(&mut self) -> Option<CancellationLatch>` returns `Some` once per operation and `None` after that. The latch is security-owned and `Send`. It is not `Clone` or `Default`, not serializable and not constructible. Its one-use method is `latch(self, signal: D9Signal) -> LatchOutcome`. So single use holds per operation, not only per token.
- **Its window, in the gate's own atomic word (r2, J1-N1).** The `FinalGate`'s `AtomicU8` (`commit_authority.rs:26-48`) gains two window bits, beside the two state bits that X4's law already fixes. They are `WINDOW_OPEN` and `WINDOW_CLOSED`, and only the cancellation latch reads them.
  - **Opening.** `WINDOW_OPEN` is set, with one `fetch_or`, when `prepare_commit`'s attempt row commits (X3D:130-133).
  - **Closing (r3, J1-R2-01).** `WINDOW_CLOSED` is set, with one `fetch_or` whose returned prior value is the sample, **exactly in the step that produces the operation's `StoppedSession`**. That is every terminal return and no continuing one:
    - **`prepare_commit`'s error returns** (`Refused`, `CommitUndetermined`, `CarrierCapacityExhausted`, `ExistingAttempt`). Each comes with a `StoppedSession` (X3D:174-180; `crates/storage/src/commit.rs:465-557`). The window may never have opened: `ExistingAttempt` and an undetermined attempt-row `COMMIT` precede it. The close is still set, so a later latch is a no-op.
    - **Every return of `publish`** (`crates/storage/src/commit.rs:571`; X3D:141-156):
      - `Committed`, where the returned state bits are the `latchedAfterAdmission` sample (`commit_session.rs:953-954`);
      - `Refused`;
      - `CommitUndetermined`.
    - **`CommitSession::refused()` and `undetermined()`** (`commit_session.rs:529-545`). An A-phase session whose window never opened is closed too.
    - **`Ok(PreparedCommit)` is not a return that closes.** It is a continuing result, and the window stays open from the attempt row's commit through `publish`. That is the span phases B and C need (8.2), and the span S12-B, S12-C and S12-U hold in.
    - **A `PreparedCommit` dropped without `publish`** (a panic or abort) leaves the window open on an operation that admits no further effect. Its only consequence is recovery evidence (X3D:213), and no permit can follow, because `publish` consumes the only path to the permit.

    The close is ordered before any later effect of the return path.
  - **The synchronization order.** `latch` is one compare-exchange loop on the same word. It succeeds only while `WINDOW_OPEN` is set and `WINDOW_CLOSED` is clear, and then it sets the latch bit (`commit_authority.rs:40-44`) in the same exchange. The `x4.gate.latch.after` point fires after it.
    - All of `admit`'s compare-exchange, the latch, the opening and the close are on one atomic, in one total order (SeqCst).
    - Every compare-exchange loop (`admit`, the cancellation latch) matches and changes only the two state bits, and it carries the window bits through unchanged. The opening and the close are `fetch_or`s, so they cannot clear a state bit. No step resets either kind of bit.
    - A latch is therefore either before the close, and so seen by the sample, or after it, and so a no-op returning `OutsideWindow`.
    - Outside the window, `latch` changes nothing.
  - **Results inside the window.** `latch` records `StopCause::Operator { signal }` only if it is the operation's first stop (`operation_guard.rs:99-106`). It returns `BeforeAdmission` (0→2), `AfterAdmission` (1→3) or `AlreadyStopped`.
  - **What does not change.** The admit and latch state law, F41, and every other latch source. `admit`, `observe` and the existing `latch` mask the window bits: `admit` becomes a compare-exchange loop over the word that still moves the two state bits only 0→1, and `state` decodes the state bits alone (`commit_authority.rs:17-25`, `:31-38`). The observer's and checkpoints' latches ignore the window bits.
  - **The successor.** This adds to X4's gate word, so S11 becomes an X4 r8 amendment, not record-only.
- **It grants nothing else:** no observation, admission, permit, effect, ledger charge, retry or reset (F41).
- **The REV reason.** The closed REV reason set (`commit_session.rs:62-104`) gains `operator`, which is S6's own word for an operator stop (SL:491). `StopCause::Operator` maps to it. The reason is shorter than `observer-fail-stop`, so the settlement reserve's exact cost (X3D:243-252) and its pin are unchanged.
- **The termination.** 468c's closed vocabulary gains `InstallationTermination::Interrupted { signal }`, the row of `StopCause::Operator`. It projects to D9 class `interrupted`, exit 130 and `signal`, with no errorCode, faultCause or detail (WS:1363-1364; COMMON4 `StepTermination`, `common-v4.schema.json:750`). `InstallationTerminationV1` requires an errorCode (`crates/host/src/installation_termination.rs:21-28`), so X7 r7's termination type carries the interrupted form separately.

**How X3D's latch rules are kept:**
- **X3D:168-172.** F38 is unchanged: state 2 means no permit, a rolled-back transaction, and the SEAL as history. F39 is unchanged: in state 3 the outcome stands.
- **X3D:261.** The latch retries nothing. The signal latches the gate, and the next checkpoint's refusal latches the attempt ledger as any failed checkpoint does. The settlement reserve funds the REV.
- **X3D:383.** The cancellation is never reported as a value to keep the ledger open.

**8.2 The five phases, and the final output section.**

A phase is fixed by the operation's state when the host **observes** the signal: at once by the latch watcher in B and C, or at the main thread's next decision point in A and D. SOP2's `host.signal.received` record keeps the arrival phase (SOP2:871). Phase O (r2) lies between OPP's D and E. It is the deferral exception of 5.3, and it is not one of OPP's five. **(r3)** The table is the durable path's. An ephemeral request has A, which runs to the output decision point, then O and E, and never B, C or D (item 6). It uses O only once S18 is accepted (5.3).

| Phase | Interval (code anchor) | What the signal does | Projection | Durable effect |
|---|---|---|---|---|
| **A.** Before attempt admission | From R0 until `prepare_commit` returns with the attempt row committed (X3D:130). It includes the durable entry, project admission, the whole analysis and replay. | It is cooperative. No new join starts. Providers get `cancel` (M3L item 16). Native work already in flight completes, including the security entry's. With a session open, the host calls `refused()` and then `finish`. The cancellation latch is not used: `refused()` latches the gate as any refusal before admission does (X4:115), and with no reserve `finish` appends nothing (X3D:120). A signal seen during `prepare_commit`, when `prepare_commit` then returns the admitted attempt, is handled as B. | per 8.3: `interrupted` 130, `kind: failure`, `errors: []`, `termination {class, signal}` (ENV7:704-723), with no runId. A `CommitUndetermined` from the attempt row's own `COMMIT` takes rule 1. | Only what completed. An installation already created stays, and its notice is already on standard error. |
| **B.** Attempt admitted, before FinalGate admission | From the committed attempt row until the compare-exchange at `publish` step 3.9 (`commit_session.rs:930`) | The latch takes the gate 0→2 and records `Operator`. The next checkpoint (3.2, 3.7 or 3.9) refuses: no permit, the staged transaction rolls back, and a durable SEAL stays history (F36, F38). `finish` appends `REV(operator)`, plus `CLN` if a SEAL exists, from the settlement reserve. | per 8.3: `interrupted` 130, as A, unless an uncertain journal commit or barrier came first, which takes rule 1. | The attempt row stays `admitted` until X6's sweep settles it `refused` (X6 item 7). Orphan objects remain. |
| **C.** FinalGate admitted | From state 1 until `publish`'s sample (`commit_session.rs:953-954`) | The latch takes the gate 1→3. The evidence `COMMIT`'s own outcome stands (X3D:170; F39, F40). `finish` appends `REV(operator)` only after `Committed`, because an undetermined outcome forfeits the reserve (X3D:253-258). | per 8.3, matched on the outcome `publish` returned, never on the gate's state: **`CommitUndetermined`** is operational-failed 4, `DURABILITY.COMMIT_FAILED`, `durability-commit`, the ExecutionId as subject, the namespace disclosed, and no runId (X7:101, :120); **`Committed(PublishedCommit)` with `latchedAfterAdmission`** is X7's F39 row (X7:100): operational-failed 4, `DELIVERY.REQUIRED_FAILED`, `delivery-required`, detail `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, the runId, no delivery phase (SL:551-554). Neither is `interrupted`. | The Run is committed, or undetermined. |
| **D.** Committed, not latched; step 1 cancellable | From `publish` returning `Committed` unlatched (the window is closed) until the output decision point. It includes `finish` and step 1's projection. | There is no latch. `finish` runs to completion. At the decision point, step 1 is `cancelled` and its projection is discarded. | `interrupted` 130 on `kind: run`, with `run.authority: authoritative`, the runId, and `termination {class: interrupted, signal, runId}` (WS:224-227; WFC:4720). This envelope is the invocation's termination output. It is rendered and written in its own final output section. | The Run is committed. No REV is owed for the signal. |
| **O.** Final output section (r2; S18; durable and ephemeral alike, r3) | From the output decision point until the required output returns (5.3) | **Deferred.** It never changes the decided envelope. **"Recorded with arrival phase O" (r3, NB-01)** means three things: the host cancellation source classifies the signal as O in memory; SOP2's `host.signal.received` is attempted with the new `CancelPhase` member `O` (an ordinary registration, SOP2:226-230); and **(r5; J1-R3-NB-02; S18 LD-7)** that event's fate follows SOP2's finalization, which runs inside O (SOP2:652-683). Before the producer cutoff (step 1), the event is admitted. After the cutoff, its call commits `drain-abandoned`: the frozen summary counts it if the commit precedes the freeze's reads (step 4), and `in_flight_at_freeze` discloses it if it is still uncommitted at the freeze. After those reads, it reaches only the post-freeze tally, which no carrier reports (SOP2:682, :704). No sink is reopened and the frozen diagnostics are unchanged. A second signal waits for an in-flight write, as for any native effect (OPP:339). **A renderer failure inside O, before any byte (r3, J1-R2-02),** replaces the decided envelope with the failure envelope, built through J2a's total projection (item 10), chosen by the committed evidence: <br>- **a `PublishedCommit` exists:** X7's F16 row (X7:99; WS:1376), operational-failed 4, `DELIVERY.REQUIRED_FAILED`, `delivery-required`, `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, keeping its runId; <br>- **no committed Run** (an ephemeral result, a refusal before the commit, a `CommitUndetermined`, an interrupt with no Run): WS:1377's row 44, operational-failed 4, `DELIVERY.REQUIRED_FAILED`, `delivery-required`, `DELIVERY.REQUIRED_PROJECTION_FAILED`, with no runId. <br>Either way, WS:233-240's aggregate decides the termination over both required steps. **(r5; J1-R3-NB-01; S18 LD-6)** An uncertain step 0 keeps its termination, ExecutionId and namespace disclosure under its fault owners: X3d r8 items 6 and 9 (X3D:176, :283) and X7 r6 items 3 and 5 (X7:101, :120). It stays out of verdict and closed-Run composition (WS:1412-1413). Its ExecutionId and namespace stay disclosed whichever termination is primary, and they are never the render attempt's or a Run's. No Run is manufactured. **A write failure after the first byte**, including one whose call cannot prove that no byte escaped, ends exit 4 with no replacement envelope (`bootstrap.rs:55-60`). If the failure envelope itself cannot be rendered, the invocation ends exit 4 with the one coded standard-error line, as `bootstrap.rs:42-47` does. | the decided envelope, or the failure envelope above; the exit follows it | as decided |
| **E.** Settled | After the settlement point (5.3) | Nothing is reclassified. The signal is recorded only. | The settled class stands (WS:227-228, WS:1393; WFC:4650). | none |

**After a `publish` return that does not enter D (r5; lead decision LD-r5-1; S18 cross-law item 1e).** D begins only when `publish` returns `Committed` unlatched. The table gives no label to a signal observed after `publish` returns anything else and before the output decision point. Those returns are `Refused`, `CommitUndetermined`, and `Committed` with `latchedAfterAdmission`.
- **Decision.** Such a signal takes the last phase the operation reached:
  - **C** if FinalGate admission had succeeded;
  - **B** otherwise.

  The label comes from the state bits in the window close's own sample (8.1), which every `publish` return takes. State 1 or 3 gives C, and state 0 or 2 gives B. J3b carries that bit to the host cancellation source with the returned outcome. **(r6)** X3d r9 keeps it as the read-only accessor `StoppedSession::admitted_at_close()` (X3D9 LD9-3). The bit is held in memory and adds no durability point.
  - **`Refused`** is a stop before the permit is used (X3D items 4 and 6). After a successful admission the commit's own outcome stands instead (F39; X3D item 5). So a `Refused` return always takes B.
  - **An uncertain journal commit or barrier** (`publish` steps 3.4 to 3.6) takes B.
  - **An undetermined evidence `COMMIT`** takes C, and so does a **`Committed` that the latch sampled**.

  The SOP2 record is `host.signal.received`, with that label as its `arrival_phase` (SOP2:871). No `CancelPhase` member is added.
- **What the signal does.**
  - The window is already closed, so a latch attempt returns `OutsideWindow` and changes nothing (8.1).
  - `finish` runs to completion. Its REV follows 8.3's last paragraph: it takes the earlier cause's reason, and there is no REV where an undetermined outcome forfeited the reserve (X3D:253-258).
  - The projection is 8.3's, by the returned outcome:
    - rule 1 for any `CommitUndetermined` (row 38);
    - rule 2 for a latched `Committed` (row 42);
    - rule 4 for a `Refused` (row 46: `interrupted` 130, with no runId).
  - The durable effect is whatever the return left.
- **Scope.** This labels only the span after `publish` returns. `prepare_commit`'s error returns keep row A's reading, which r5 does not change.
- **Rejected:**
  - **D.** D is the phase of a committed, unlatched Run, which `interrupted` names by its runId (row 47). Labelling this span D would claim a Run that does not exist, or hide the latch.
  - **A.** By its own words, row A ends when `prepare_commit` returns the admitted attempt. Here it has returned it, and `publish` has run.
  - **A new `CancelPhase` member for the span.** It would be an ordinary registration (SOP2:226-230). But it would add a row to OPP §5.5's table, which is now S18's copy, for a span that B and C already handle. It would change no outcome.
  - **No label.** `host.signal.received` requires an `arrival_phase` (SOP2:871).

**8.3 Precedence (lead decision; r2, J1-R1).** For a signal observed before settlement, the rule matches the outcome X3d actually returned first. The gate's state 3 alone proves neither a commitment nor a RunId (X3D:170; X7:100-101; `commit_session.rs:939-958`, where an undetermined `COMMIT` builds no `PublishedCommit`). The first rule that applies decides:
1. **Any `CommitUndetermined`**: from the attempt row's `COMMIT`, a journal commit or barrier, or the evidence `COMMIT`, whatever the gate's state. It takes the durability row, with the ExecutionId (IE:1680-1681; X3D:283; X7:101). The uncertainty must be recovered, and the empty-errors `interrupted` branch can carry no ExecutionId (ENV7:704-723).
2. **A `Committed(PublishedCommit)` whose `latchedAfterAdmission` is set.** X7's F39 row, with the RunId the `PublishedCommit` carries (SL:551-554; X7:100).
3. **A `Committed(PublishedCommit)` not latched, with the signal observed in phase D.** `interrupted`, with that RunId.
4. **Otherwise:** `interrupted`, with no runId.

A signal observed in phase O or E is not "before settlement" for the envelope: O defers it (8.4), and E is settled.

End-path failures are disclosed beside the outcome and never rewrite it (X3D:289).

When another stop came first (`AlreadyStopped`), or a certain refusal ended the attempt before the signal was observed, the REV takes that cause's reason (S6), and the projection still follows rules 1 to 4. WS's before-settle rule makes the aggregate `interrupted` (WS:224-226). The refused attempt's own row is kept in the operational record (SOP2:872), not in the envelope: the empty-errors `interrupted` branch admits no other member (ENV7:704-723, :790).

**Rules 1 and 2 against WS:226 (r5; lead decision LD-r5-2; S18 cross-law item 1f, its LD-12).** WS §1's before-settle rule makes the aggregate `interrupted` (130) for every signal observed before settlement (WS:225-226, with WS:225 as S18 states it). Where X3d returned a `CommitUndetermined`, or a `Committed(PublishedCommit)` latched after admission, rules 1 and 2 give operational-failed 4 instead. Each of those two rows is a contract row in its own right:
- IE:1680-1681 makes an undetermined commit "`durability-undetermined` to the caller, exit 4, with an ExecutionId for read-only recovery";
- SL:551-554 says that for a state-3 attempt "the required delivery is reported failed through the existing `DELIVERY.REQUIRED_FAILED` path", and calls this "the **selected** law, not an open choice".

No contract text orders these rows against WS:226. WS:233-240's aggregate order omits `interrupted`, and WS:226 sets `interrupted` outright. So the contracts conflict exactly where a signal meets one of these two outcomes.
- **Decision.** Rules 1 and 2 stand. X3d's returned outcome is matched first, and for these two outcomes IE:1680-1681 and SL:551-554 govern over WS:226. J1 reads WS:226 as governing every other before-settle signal, under rules 3 and 4. WS's text does not say so, so a WS passage successor is owed: **S21** (item 13). S21 is to override WS:226 and WSE:226 to state the exception, adding no class, code or exit. Both lines are free in the lock at `5214350`. r5 records S21 and does not write it. **(r6)** S21 is accepted and bound (Grok ACCEPT-DESIGN-UNIT at r2, `reviews/codex2-s21-r2`; product `3f6f9a5`). WS:226 and WSE:226 now state the exception, so "WS's text does not say so" is history (S21 cross-law item 1). S21 also overrides WS:229 and WSE:233: an analysis attempt that the signal aborts leaves no Run (S21 LD-6).
- **Until S21 is accepted,** no wired path delivers, and no control or row asserts, a rule-1 or rule-2 termination for a signal. This mirrors phase O's wait for S18 (5.3). These wait for S21:
  - J3d's durable signal wiring;
  - J-C14's rule-1 and rule-2 signal cases;
  - J-C15b's phase-C projections;
  - X9 rows S12-C and S12-U.

  These may go ahead:
  - J2a's pure model;
  - J3b's latch code and its other tests, J-C15b's latch and durable-effect assertions among them;
  - rows S12-B and S12-D.

  Rules 1 and 2 also cover an observer's latch, and an undetermined commit with no signal. X7 already routes both (X7:100-101), and no signal is involved, so neither waits. **(r6)** S21 is accepted and bound, so this gate is met. Each item that waited for S21 now proceeds under its own unit review.
- **Rejected:**
  - **Following WS:226 as written, which gives `interrupted` 130 under rules 1 and 2.**
    - The empty-errors `interrupted` branch can carry no ExecutionId (ENV7:704-723). An undetermined commit would then lose the recovery disclosure that IE:1680-1681 requires.
    - A latched committed Run would be reported as interrupted, where SL:551-554 selects `DELIVERY.REQUIRED_FAILED`.
    - It would reopen J1-R1, which r2 closed.
  - **Reading WS:226 as already subordinate to WS:233-240's aggregate,** so that an operational fault dominates `interrupted`. That order lists five classes, and `interrupted` is not one of them. S18's accepted LD-12 found that no successor amends WS:226.
  - **Calling such a signal after-settle or final-output.** Step 0 is not terminal before `finish`, and the decision point has not been reached. That reading would falsify WS:225-228 as S18 states them.
  - **Amending WS in this revision.** WS changes only through a reviewed contract successor, in S18's form, and r5 is a record revision.
  - **No gate until S21.** Wired code would then deliver a termination that WS:226 forbids, on a reading not yet accepted. J1 gated phase O on S18 for the same reason (r3, J1-R2-03).
  - **Gating J2a, or all of J3b.** Neither delivers a termination for a signal, and S18's gate likewise let the pure models proceed.

**8.4 Phase D, the output decision point and phase O (OPP:335; lead decision, r2 J1-R2).**
- **D takes WS's before-settle row,** `interrupted` with the runId. X7's F39 row is reserved for a `Committed` that `publish` sampled as latched (8.3, rule 2).
- **The output decision point** is the single cancellation check after `finish` and step 1's projection. It comes before SOP2's finalization, because SOP2 finalizes once, "after the command's result is decided and before the required envelope is rendered or written" (SOP2:652). It decides which envelope the final output section renders. It does not settle the invocation (5.3; r5, S18 LD-4).
- **Phase O defers a signal.** The required envelope is one, and once its first byte is written no replacement may follow (`bootstrap.rs:57-58`; L464:32). The envelope also carries its own `exitCode` (ENV7 `exitCode`), so a signal that changed the class mid-section would contradict bytes already decided or written. O therefore records the signal and defers it.
  - **This was an exception to WS:224-226's before-settle rule,** because the invocation has not settled in O. **(r5)** S18 makes it WS's own rule (5.3).
  - **S18** reconciles the exception with the WS owner (WS §1's cancellation paragraph) and the OPP owner (OPP §5.5's phase table) as a passage successor. **Every** output path that uses O is gated on S18's acceptance, J2c's ephemeral output as well as J3d's durable output (r3, J1-R2-03). Until then, both units may land everything except their output wiring. **(r5)** S18 is accepted and bound at product `5214350`, so this gate is met.
  - **Its bound.** The section's length is SOP2's bounded finalization (SOP2:652-683) plus one rendering and one output. A blocked output has no elapsed bound (OPP:339), and that is stated, not hidden.
- **Rejected:**
  - **X7's latched row for D.** It would report a delivery failure that did not happen. X7's F39 row means the commit observed a latch after admission (X7:100).
  - **Treating the decision point as settlement (r1).** Step 1 is not terminal there unless the signal cancels it, and a render failure can still follow, even of a termination output (X7:85; `finalization.rs:310-318`; r5, S18 LD-4).
  - **Re-deciding after SOP2's finalization, or interrupting the envelope mid-write.** The first contradicts SOP2:652. The second tears the single required envelope or appends a replacement (`bootstrap.rs:57-58`).
  - **Leaving the output section under the before-settle rule.** A signal there would have to change an envelope whose class and `exitCode` are already decided, or be emitted as exit 130 beside a success envelope.

**8.5 The second stage.**
- A second signal, or the grace expiring, forces provider-tree kill (M3L item 16; OPP §5.5). The grace is the protocol member that M3L item 16c reconciles, not OPP's provisional 2 s. This answers M3L's cross-law finding X3 for S-OP-12.
- Inside a native effect already in flight, the forced stage waits for it to return, with no elapsed bound (OPP:339):
  - in A, the security entry's native work;
  - in B, a journal commit, barrier or object write;
  - in C, the evidence `COMMIT`.
- SIGKILL leaves M2's recovery evidence (X3D:213). No outcome is invented.

**8.6 What changes in X3D and X7.**
- **X3d r9 (S10):**
  - item 5: the third latch source; `take_cancellation_latch`, minted once per operation; and the window, opened at the attempt row's commit, kept open across `Ok(PreparedCommit)`, and closed only where a `StoppedSession` is produced (8.1; r3, J1-R2-01);
  - items 7 and 8: `StopCause::Operator` and the REV reason `operator`, with the reserve cost unchanged;
  - item 9: `InstallationTermination::Interrupted { signal }`, row "operator stop", projected by X7;
  - item 13: unit J3b;
  - the record of item 7 above, on `refused()`;
  - item 2 (r2, J1-R4): `open` reserves its drawn ExecutionId in `ExecutionIdReservations` before the session exists (item 2);
  - (r6) the close's admission bit, kept as the read-only accessor `StoppedSession::admitted_at_close()` (X3D9 LD9-3; 8.2);
  - new forbidden substitutes: a latch outside the window, a second latch for one operation, a latch used as authority, and the outcome selected from the gate's state rather than from the returned outcome.
- **X4 r8, an amendment (S11; r2).** X4 item 7's gate gains the cancellation latch as a source, and its atomic word gains the two window bits of 8.1. The two-bit state law is unchanged.
- **X7 r7 (S9):**
  - item 1: item 7's order;
  - item 3: a new row, `Refused(Interrupted { signal })`, projected as the A/B `interrupted` envelope. The F39 and `CommitUndetermined` rows are unchanged, and are named as applying whatever the latch source. They are selected by the returned outcome, `CommitUndetermined` first (8.3);
  - item 4: step 1's terminality and the settlement point (5.3), the output decision point, phase D's row and phase O's deferral (8.4, under S18). X7a's `DeliveryPhase::render` (`finalization.rs:256-262`) splits into a projection, which is cancellable in D, and the rendering of the decided envelope, which happens in O. In O, a renderer failure takes F16 only when a `PublishedCommit` exists, and WS:1377's no-Run row otherwise (r3, J1-R2-02);
  - item 8: the termination type's interrupted branch, still with no wildcard arm;
  - new forbidden substitutes: projecting D as F39; F39 for a `CommitUndetermined`; re-deciding the envelope after the output decision point; and a replacement envelope after output has begun.

**8.7 Controls** (OPP §10's cancellation row, OPP:433, made concrete):
- **J-C14.** In-process: a signal at each of phases A to E and O, through the host cancellation source, gives 8.2's projection and durable effect. That includes:
  - "`Committed(PublishedCommit)` with the latch → exit 4 with the runId";
  - "`CommitUndetermined` → exit 4 with the ExecutionId", including **a latch 1→3 followed by an undetermined evidence `COMMIT`**, which must never give F39 or a runId (8.3, rule 1; r2, J1-R1);
  - "a signal in D → exit 130 with the runId";
  - "a signal in O → the decided envelope and its exit, with the signal recorded as O", at S18-T1's three points: before the producer cutoff, between the cutoff and the freeze, and after the freeze (r5; J1-R3-NB-02);
  - "a renderer failure in O → the failure envelope chosen by committed evidence, with no byte of the decided envelope written" (J-C14b);
  - (r5, LD-r5-1) a signal after each `publish` return that does not enter D. A checkpoint refusal is B, rule 4. An uncertain journal commit is B, rule 1. An undetermined evidence `COMMIT` is C, rule 1. An observer-latched `Committed` is C, rule 2. Each is classified by the close's sample. The rule-1 and rule-2 cases wait for S21 (8.3). **(r6)** S21 is bound, so they no longer wait.
- **J-C14b (r3, J1-R2-02).**
  - A durable `Committed` Run whose renderer fails before any byte gives F16, with the runId kept and `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`.
  - An ephemeral result whose renderer fails before any byte gives `DELIVERY.REQUIRED_PROJECTION_FAILED`, with no runId, and so does the rendering of a pre-commit refusal.
  - A `CommitUndetermined` whose failure envelope's renderer fails keeps the ExecutionId disclosure and has no runId. **(r5; S18-T2; J1-R3-NB-01)** The test asserts the analysis attempt's ExecutionId and namespace disclosure separately from the primary code and detail that WS:233-240's tie rule selects. It also asserts that the disclosed ExecutionId is not the render attempt's.
  - A write failure after the first byte gives exit 4 with no replacement envelope.
  - An unrenderable failure envelope gives exit 4 and the one coded line.
- **J-C14c (r3, J1-R2-03).** The ephemeral path:
  - A signal before the output decision point (analysis, evaluation, or step 1's projection) gives `interrupted` 130 on the empty-errors branch, with no runId and no durable effect. This holds before and after S18.
  - **Once S18 is accepted, and gating J2c's output wiring:** a signal inside O gives the decided ephemeral envelope and its exit, with the signal classified as O in memory; a signal after settlement reclassifies nothing.
- **J-C15.** `CancellationLatch` changes nothing outside its window. `take_cancellation_latch` returns `None` the second time. A second `latch` on one token is refused at compile time. `AlreadyStopped` keeps the first cause's REV reason. **(r3)** A latch racing each closing return is either seen by that return's sample or is a no-op. The closing returns are the four `prepare_commit` errors, the three `publish` returns, and `refused()` and `undetermined()`. The window bits survive every `admit` and latch exchange.
- **J-C15b (r3, J1-R2-01).** First obtain `Ok(PreparedCommit)`, then assert the window is still open. Then cancel during `publish` at:
  - the journal transaction's start (3.1);
  - after the SEAL (3.6);
  - before the final checkpoint;
  - after admission and before the evidence `COMMIT`.

  The projections and durable effects are phase B's or C's (8.2): `REV(operator)`, F38's rollback, and F39 or F40 by the returned outcome. A latch after `Ok(PreparedCommit)` and before `publish` is called is seen by `publish`'s first checkpoint.
- **J-C16.** An injected stall in the evidence `COMMIT` and in a barrier, with a second signal: the process keeps waiting, invents no refusal, and projects per X7 once the call returns.
- **J-C17.** X9 rows S12-B, S12-C, S12-U, S12-D and S12-O (S12, item 12).

### 9. The backup-status successor, J-BS (lead decision; contract successor S13)

- **Shape (the direction recorded at X11:49-54).** `invocation-v5` `$defs/RetentionDisclosure` (INV5:1863-1892) gains an optional member `backupStatus`. Its values are exactly `BackupClassification::disclosed`'s three spellings: `backed-up`, `not-backed-up` and `unknown` (`initial_installation.rs:335-340`). It is never `not-backed-up` from a missing detector.
- **Presence.** It is present exactly when `firstUse` is true. A schema `if`/`then`/`else` enforces both directions.
  - **`firstUse` (lead decision; r2, J1-R3)** is true exactly when item 3's `created` is `Some`: this invocation's creator act performed the publication rename, whether it ended `Published` or refused after the rename. `LostRace` and `NotPristine` minted an intent but created nothing, so `firstUse` is false there and the member is absent.
  - **Rejected:**
    - "true whenever an intent was minted", which would claim a creation this invocation did not perform;
    - a later existence scan, which cannot tell this invocation's creation from another's.
- **Value.** The classification held by this invocation's `CreationIntent`. Under L464 item 2 that is always `unknown`.
- **The notice stays.** It is still written and flushed before effects (L464:27-32). The field adds a carrier and replaces nothing. 464 item 4's acknowledgement member is not added, because no positive detector lands.
- **Versioning (lead decision).** An in-place optional-member append to `invocation-v5`, as a contract successor with regeneration (contracts crate and TypeScript types) and a registry re-pin. Precedents: 468a's in-place `DomainDetailCode` append (L468:52), and NE:3410-3419's prerelease document revision. The successor runs after F8b's execution, because the generator refuses until F8b.
  - **Rejected:** `invocation-6` with `command-envelope-8`. That moves every emitter (metadata, doctor, the delivery failure) and every golden for one optional member, before any release exists.
- **Which envelopes carry `retentionDisclosure` (r2, J1-R3; the existing carrier, ENV7's `retentionDisclosure`):**
  - **Durable, from publication.** Once item 3's `created` is `Some`, **every** envelope of the invocation carries it, success or failure, the one exception being the empty-errors `interrupted` branch. That includes a refusal of attempt B's producers, gate, barriers or rechecks (`EntryRefusal.created`), and every later refusal. Its form is `{policy: durable-unbounded, provenance: DEFAULTED, firstUse: true, storageRoot: the intent's disclosed target, backupStatus}`.
  - **Durable, otherwise,** once R3 has succeeded: the same form with `firstUse: false`, `storageRoot` set to the admitted I's account-derived target, and no `backupStatus`. Before R3, it is absent: no retention posture applies yet.
  - M3 applies no bounded retention (purge and GC are M5).
  - **Ephemeral**, once the capture session has opened: `{policy: ephemeral, provenance: EXPLICIT-FLAG, firstUse: false, storageRoot: the temporary custody root}`.
  - **The empty-errors `interrupted` branch never** carries it (ENV7:790). On a first-use interrupt, the notice is the carrier.
- **The first emitter** is J3d's durable envelope, validated end to end by `workflow_tests.rs`. That answers X11:55: the field is tested through the envelope that carries it.
- **Controls:**
  - **J-C18.** Schema validity of every combination, and absence on the `interrupted` branch.
  - **J-C19.** `firstUse: true` only when `created` is `Some`, on success and on every refusal after the rename (J-C6b). `backupStatus` equals the intent's classification, and its spelling is never `not-backed-up` while the classifier is constant.

### 10. The M3 outcome matrix (law): existing codes only

Every row uses an existing D9 class, error code, fault cause and detail. **No public code is added.** The internal additions are:
- `InstallationTermination::Interrupted`, which maps to the existing class `interrupted`;
- `StopCause::Operator`;
- the REV reason `operator`, which is S6's word (SL:491).

| # | Class (phase) | Class / exit | errorCode / faultCause | Detail or reasonCodes | runId / executionId | Basis |
|---|---|---|---|---|---|---|
| 1 | RequestId allocation fails | — / 4 (one fixed line on standard error, no envelope) | — | `HOST.IO_FAILURE: request identity allocation failed.` | none | `bootstrap.rs:17-23`; OPP:158 |
| 2 | Malformed library request or step list (host-built) | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | absent; the key goes to the operational record | none | NE:3573 |
| 3 | Embedded release absent (F0), durable or ephemeral | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | `CORE.NO_EMBEDDED_RELEASE` | none | L468:37 |
| 4 | Actor; other core; platform decision; platform mismatch; H filesystem | request-rejected / 2 | as L468 | as L468:38, :41-44 | none | L468 item 6 |
| 5 | Custody at the probe, the chain, the creator, the gate or the rechecks (including `/` on this host) | request-rejected / 2 | `CONFIG.INVALID` | `CONFIG.CUSTODY_REFUSED`, with its sub-detail as subject | none | L468:45 |
| 6 | I present but incomplete (durable gate, or ephemeral read path) | request-rejected / 2 | `CONFIG.INVALID` | `CONFIG.CUSTODY_REFUSED`, `installation-incomplete` | none | L468:46 |
| 7 | Probe `Present`, gate `Absent` (race) | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | `INSTALLATION.NOT_INITIALIZED` | none | item 3; L468:40 |
| 8 | Backup choice required (intent or R7) | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | `storage.backup-choice-required` | none | L468:39; L464:9 |
| 9 | Fence busy (durable gate or read session) | operational-failed / 4 | `LEDGER.BUSY_TIMEOUT` / ledger-busy | `PROJECT.BUSY` | none | L468:47 |
| 10 | Notice write or flush failure; a creator or gate rename, barrier or I/O failure | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | — (the envelope's `errors` carries `HOST.IO_FAILURE`) | none | L468:48; X10 r4 item 3 |
| 11 | An attempt or admission ledger charge refused | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `WORK.BUDGET_EXHAUSTED` | none | L468:49 |
| 12 | Project carrier custody; invalid configuration | request-rejected / 2 | `CONFIG.INVALID` | `CONFIG.CUSTODY_REFUSED` / `CONFIG.INVALID` | none | M3B:97, :149-150 |
| 13 | Invalid compiled default or host-built flags layer | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `HOST.INVARIANT_VIOLATED` | none | M3B:151 |
| 14 | Pack rows 1, 2 and 3a; row 3; row 4 | request-rejected 2; 2; operational-failed 4 | `CONFIG.INVALID`; `CONFIG.INVALID`; `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `CONFIG.INVALID` (X12-0 remedy); `POLICY.IMPERATIVE_KEY_REFUSED`; `HOST.INVARIANT_VIOLATED` | none; first use also discloses the creation | X12:105-111 |
| 15 | Project admission: scope limits; registry or identity refusals | as X2 item 8's rows | as X2 | as X2 (for example `PROJECT.SCOPE_LIMIT`) | none | X2 item 8 |
| 16 | Store endpoint (X3a) | as X3a's rows | as X3a | as X3a (`STATE.SCHEMA_UNSUPPORTED` and so on) | none | X3A item 5 |
| 17 | Trust at the fenced first read: F absent (durable only; item 6 and E-4 for ephemeral); continuation; root chain; payload; clock; incomplete trust records | per X4T item 10: F absent is request-rejected 2; continuation, root, payload and clock are request-rejected 2; incomplete records take row 6 | `REQUEST.PRECONDITION_FAILED` for F absent; `EXTENSION.ADMISSION_REJECTED` for continuation; the others as X4T item 10 fixes | `TRUST.NO_ADMITTED_TIME_CONTEXT`; `CONTINUE-CORE-NOT-TRUSTED`; S5 `ROOT.*`; `PAYLOAD-NOT-ADMISSIBLE`; `CLOCK-EXCURSION-FORWARD` | none | X4T:139-150 |
| 18 | Revoked during the operation | request-rejected / 2 | `EXTENSION.ADMISSION_REJECTED` | `TRUST.COMPONENT_REVOKED_DURING_OPERATION` | none | X4:120 |
| 19 | Observer or monitor fail-stop, including a starved observer during a long analysis | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | `OBSERVER.FAIL_STOP`, subject the stop reason | none | X4:121 |
| 20 | Workspace-unit excess | request-rejected / 2 | `REQUEST.UNSATISFIABLE` | `PROJECT.WORKSPACE_UNIT_LIMIT` | none | NE:3533; M3B:368 |
| 21 | Discovery or snapshot ledger exhausted | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `WORK.BUDGET_EXHAUSTED` | none | M3B:338 |
| 22 | Snapshot, dependency-set or acquisition bound; prospective-Plan bounds; selection arrays | request-rejected / 2 | `REQUEST.UNSATISFIABLE` | `PROJECT.SCOPE_LIMIT`, `field:count>limit` | none | 5.4c; NE:3534; M3C:964 |
| 23 | Host I/O during capture or discovery | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | — | none | OPP:291 |
| 24 | Explicit root without a marker; root path invalid | request-rejected / 2 | `CONFIG.INVALID` | `native.explicit-root-without-marker` / `PROJECT.EXPLICIT_PATH_INVALID` | none | NE:3527 |
| 25 | Discovery inventory mismatch; stale or non-inert import or prepared row | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | `PROJECT.DISCOVERY_INVENTORY_MISMATCH` / `native.stale-*` | none | NE:3525, :3528 |
| 26 | Capability request: invalid; contradictory; not selected | request-rejected / 2 | `CONFIG.INVALID`; per origin; `REQUEST.UNSATISFIABLE` | per NE's route registry | none | NE:3536-3539, :3569-3575 |
| 27 | Required provider closure not installed, or not admitted by current trust (including ephemeral with no trust, E-3); never a trust-admitted excluded form, which is row 56 (r5, SD-5) | indeterminate / 3 | — | `COVERAGE.PROVIDER_UNAVAILABLE`; durable: `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`. **(r6, lead ruling)** Ephemeral (E-3): no detail (RTC §7.4). | runId if committed; **(r6)** `authority: ephemeral` and no runId if ephemeral | WS:1374; NE:3370; **(r6)** RTC §7.4 |
| 28 | Installed closure bytes corrupt, or unspawnable | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | `DELIVERY.CLOSURE_BYTES_CORRUPT` / `DELIVERY.CLOSURE_UNSPAWNABLE` | none | WS:1375 |
| 29 | Plan just built fails `check_plan_pack`, or the structural enumeration admission | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `HOST.INVARIANT_VIOLATED` | none | X12:144; M3C:878 |
| 30 | Worker fault: process fault, protocol violation, `ProviderFault`, crash, deadline, liveness, RSS breach | operational-failed / 4 | `PROVIDER.PROTOCOL_VIOLATION` / provider-protocol | absent; the key goes to the operational record | none: no facts, Coverage or Run | NE:3529, :3837-3843; NE:3224 |
| 31 | Clean `Unavailable` or `BudgetExhausted` stage terminal; admitted incomplete inputs | indeterminate / 3 | — | the primary deficiency's route (NE:3364-3374) | runId (authoritative) or `authority: ephemeral` | NE:3844-3855, with NE:3849-3850 as FA-1 states them (r5; MH item 4) |
| 32 | Producer Coverage cause or carrier refusal; contradictory completeness | operational-failed / 4 | `PROVIDER.PROTOCOL_VIOLATION` / provider-protocol | absent | none | NE:3538, :3541 |
| 33 | Evaluator work budget | indeterminate / 3 | — | `COVERAGE.BUDGET_EXHAUSTED`; detail `EVALUATION.WORK_BUDGET_EXHAUSTED` | runId (sealed) | OPP:282 |
| 34 | Evaluation output bound | operational-failed / 4 | `OUTPUT.SERIALIZATION_FAILED` / output-serialization | `EVALUATION.OUTPUT_BOUND_EXCEEDED` | per that route (WPC:141, via OPP) | OPP:283 |
| 35 | Verdict: pass; fail; insufficient Coverage | success 0; policy-failed 1; indeterminate 3 | — | reasonCodes on indeterminate | runId, or `authority: ephemeral` | WS:233-248; NE:3364-3374 |
| 36 | Replay refusal (X5) | X5 item 5's rows | as X5 (`EVALUATION.INPUT_REFUSED` and so on) | as X5 | none | X5 item 5 |
| 37 | Commit: busy; host I/O; quarantine; invariant; budget | operational-failed / 4 | per X3D item 9 | per X3D:277-287 | none | X3D:276-289 |
| 38 | `CommitUndetermined`, in any phase, whatever the gate's state (8.3, rule 1) | operational-failed / 4 | `DURABILITY.COMMIT_FAILED` / durability-commit | the ExecutionId as subject; the namespace disclosed | executionId, no runId | X3D:283; X7:101, :120; 8.3 |
| 39 | `ExistingAttempt` (lawfully impossible) | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `HOST.INVARIANT_VIOLATED`, with the requested binding | executionId | X7:103 |
| 40 | Carrier capacity exhausted | operational-failed / 4 | `LEDGER.BUSY_TIMEOUT` / ledger-busy | `PROJECT.BUSY`, with the rollover disclosed beside | none | X7:104, :165-177 |
| 41 | Capacity preflight (once S-OP-8 is accepted) | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | as S-OP-8 fixes | none | OPP:292 |
| 42 | `Committed(PublishedCommit)` with `latchedAfterAdmission` (observer or signal), selected by the returned outcome, never by state 3 alone (8.3, rule 2) | operational-failed / 4 | `DELIVERY.REQUIRED_FAILED` / delivery-required | `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` | the `PublishedCommit`'s runId | X7:100; SL:551-554 |
| 43 | Required renderer or output failure when a `PublishedCommit` exists, including inside phase O (r3) | operational-failed / 4 | `DELIVERY.REQUIRED_FAILED` / delivery-required | `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` | runId | WS:1376; X7:99 |
| 44 | Required projection or renderer failure with no committed Run, including inside phase O (r3): an ephemeral result, a pre-commit refusal, a `CommitUndetermined` (its ExecutionId disclosure kept), or an interrupt with no Run. Aggregated with step 0 under WS:233-240. | operational-failed / 4 | `DELIVERY.REQUIRED_FAILED` / delivery-required | `DELIVERY.REQUIRED_PROJECTION_FAILED` | none (an uncertain step 0's executionId kept) | WS:1377; WS:233-240; X7:101 |
| 45 | End-path settlement, end-step or rollover failure | disclosed beside the outcome; never rewrites it | its own row | its own row | — | X3D:289; X7:141-150 |
| 46 | Signal: phase A or B | interrupted / 130 | — | `signal` | none | 8.2; WS:224-227 |
| 47 | Signal: phase D (before the output decision point) | interrupted / 130 | — | `signal` | runId | 8.2; WFC:4720 |
| 48 | Signal: phase O (deferred, durable or ephemeral, only once S18 is accepted) or E; optional output failure | the decided or settled class | unchanged | unchanged | unchanged | 5.3; 8.4; WS:1393; X7:106 |
| 49 | Host panic before or after FinalGate admission | operational-failed 4, host-invariant, where the termination layer is reachable after unwinding / nothing manufactured | `SYSTEM.OUTCOME.ILLEGAL_STATE` | — | none / unchanged | OPP:294-295; X3D:213 |
| 50 | Observability loss (SOP2) | none, ever | — | counters only | — | OPP:296; SOP2:766 |
| 51 | `--ephemeral` with an authority prerequisite (not reachable at M3) | request-rejected / 2 | `REQUEST.UNSATISFIABLE` | `WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY` | none | WS:246; CINV `analyze-ephemeral-required-authority` |
| 52 | Native context or universe binding refused: a stdlib, rust-dev-llvm or tool closure that is unretained, recomputes to another identity or has the wrong kind; a suffix, component, `libSelection`, tool-member or compiler-version join that fails; a universe bound to a context this host did not mint, or to the other language's record. **(r6, SYN-1 O-1)** Also a native-context closure that is malformed, or a native-context field that does not match. **(r6, SYN-1 X-J1)** Also a syntax grammar context that cannot be minted: no admissible `kind=grammar` closure is installed, a §1.2 row check fails, or the execution admission chain refuses the installed closure. It is reached at J-ε (C2 contexts, M3C rows 10-13), before the PlanId, with no worker spawned. | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` / — | absent unless a registered `DomainDetailCode` names it. The `native.native-context-*`, `native.universe-context-binding-mismatch` or `native.native-context-language-mismatch` key goes to the operational record. **(r6)** So do O-1's `native.native-context-closure-malformed:<where>` and `native.native-context-field-mismatch:<subject>`, and SYN-1's `native.syntax-grammar-*` and `native.syntax-normalizer-*` keys, each in its NE §1.2 form. | none | NE:3530; NE:3546-3555; **(r6)** NE §10's syntax grammar context row (SYN-1); SYN-1 O-1 |
| 53 | Preparation bound exceeded. Reached only by native preparation (M5, BP:992), not at M3; recorded as not reachable. | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | per NE's route registry; the key `native.prepare-bound-exceeded` goes to the operational record | none | NE:3531; NE:3546-3555 |
| 54 | Ambient Cargo configuration in an ancestor, or an environment override, at the Rust context and adapter join (C3; M3C:716, C3-T9) | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | per NE's route registry; the key `native.ambient-cargo-config` goes to the operational record | none | NE:3532; NE:3546-3555 |
| 55 | Invalid authenticated release declaration: a capability the matrix does not register, a mode outside the registered set, a `NOT-SELECTED` mode, a duplicate `capabilityId`, or a `preview-*` spelling. The origin is the authenticated release declaration (NE:3574), reached at B1's layer 1 (M3B:88), before any Plan, with no worker spawned. | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` / — | absent. The `native.release-capability-*` key goes to the operational record. | none | NE:3540, :3574 |
| 56 | Component manifest that is a DR-117 excluded form at R10a or ER10a (EE-1, EE-3b, EE-4's manifest part, EE-5a), before any analysis-attempt ExecutionId | request-rejected / 2 | `EXTENSION.ADMISSION_REJECTED` | `PAYLOAD-NOT-ADMISSIBLE`, subject `excluded-form:<class>:<manifestDigest>`; every `ExcludedForm` in the operational record | none | NE §10 (SD-5); SL:1306; MD item 24 |
| 57 | Request that is a DR-117 request-class excluded form at R1 (EE-2, EE-4's request part, EE-6a): well formed, neither malformed nor a host fault | request-rejected / 2 | `REQUEST.UNSATISFIABLE` | `PROVIDER.NOT_SELECTED`, subject `excluded-form:<class>`; every `ExcludedForm` in the operational record | none | NE:3577-3579 (the NOT-SELECTED-cell precedent for this class and code); NE §10 (SD-7); M3-D item 25 |
| 58 | **(r6, SYN-1 X-J1)** Syntax backend fault while parsing a source file after admission (NE §1.2's per-file parse outcomes): a tree that fails validation, on either branch, or, under `wasm32-fuel-v1` only, a trap other than fuel or memory exhaustion or a protocol violation by the grammar module. Never retried with another backend; no Coverage, no candidate envelope and no Run | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `HOST.INVARIANT_VIOLATED`, subject `native.syntax-backend-fault:<grammarId>` | none | NE §10's syntax backend fault row, after NE:3541 (SYN-1 LD-12) |

- **Totality.** J2a's projection is an exhaustive match with no wildcard arm (X7 item 8). A detail with no row is a model error, never exit 0 (NE:3543).
- **(r5) Row 56 is S20 for R10a's and ER10a's route.** SD-5 adds it to NE §10 after NE:3540 (Grok ACCEPT-DESIGN-UNIT; bound at product `052d3cb`), and this row quotes it word for word. Every `ExcludedForm` that R10a or ER10a returns now has a row.
- **(r6) Row 57 is M3-D item 25's request-class route.** `ExcludedForm` also arises at R1, in request validation, for EE-2, EE-4's request part and EE-6a (M3D item 25, M3D:827-851). r5 routed it to M3-D r4 (SD-5's X-SD5-1). M3-D r4 decided it (LD-R4-2), and M3-D r5 gives the row word for word (X-D4-J1-1, M3D:1222). SD-7 binds NE's row on NE:3539 and widens `PROVIDER.NOT_SELECTED`'s code-keyed remedy (GROK2 ACCEPT-DESIGN-UNIT at r2, `reviews/grok-sd-7-r2`; product `d2c00a9`). R1's malformed-request sentence keeps its own scope (item 4). Every `ExcludedForm` that R1, R10a or ER10a returns now has a row.
- **(r6; SD-7's X-SD7-J1) The bases of rows 56 and 57.** Row 56's "NE §10 (SD-5)" is NE:3540 as SD-7 supersedes it. SD-7 conforms that row's EE-3b and EE-5a wording and its remedy to M3-D r5 item 24 (LD-R4-1), and changes none of row 56's columns. Row 57's "NE §10 (SD-7)" is SD-7's override of NE:3539. J-C20 tests both.
- **(r6) SD-5b's refusals have no row yet.** `MemoryBudgetBelowCeiling`, `ToolOutputBound`, `ToolScratchBound` and `confinement-refused` are SD-5b's (S20). SD-5b writes each one's row, with an existing code, together with its first consumer (M3D:1180). J2a carries no placeholder for them.
- **(r6, lead ruling) Row 27's ephemeral form.** RTC §7 owns a step termination's detail and authority (WS:1399-1414). §7.4 admits no §7.5 detail on an ephemeral attempt (`RUN_TERMINATION_DETAIL_NOT_ADMITTED`), so row 27's ephemeral case (E-3) carries `COVERAGE.PROVIDER_UNAVAILABLE`, `authority: ephemeral`, no runId and no detail. The durable case keeps `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`. **Rejected:** a contract successor changing §7.4. A law cannot override the contract, and nothing needs the detail.
  - **Recorded, not resolved.** NE's excluded-form row, as SD-7 supersedes it at NE:3540, says that a required closure current trust does not admit, "an ephemeral request with no trust view included", "keeps that golden: `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`". r6 amends no NE text. **Lead ruling:** the sentence is corrected by **SD-8**, an NE passage supersession of SD-7's NE:3540 override. SD-8 keeps the row's class and code for that ephemeral form and drops the detail, under §7.4. It is owed before J2c (Open questions).
- **(r6; M3-C r8's X-8) Row 27's required cells wait for an enumeration successor.** M3-C r8 (accepted in review) finds that a required cell whose closure is not admitted has no binding the enumeration contract admits: it refuses an unselected enumerator on a required cell, and no admitted closure can stand in for the missing one. That covers E-3's required cells other than `inventory` cells, and WS:1374's durable not-installed golden, which this law routes to row 27. M3-C r8 recommends an enumeration-contract successor and says C4a's and J2c's legs for that case wait for it. r6 records the dependency and changes no row.
- **Control J-C20.** One test per row that M3 code can reach. Rows 41, 51 and 53 are skipped until their owners land, and the skip is recorded. **(r5; SD-5)** Row 56's test is D4-T1's public-route assertion. On paths 3a, 3b and ER10a, the envelope is row 56's, `errors` equals its one detail, and there is no runId or executionId. **(r6)** J-C20 tests row 57 once M3 code can reach it (X-D4-J1-1), and rows 56 and 57 with SD-7's remedies (X-SD7-J1). It tests row 58 as it tests every reachable row.
- **Control J-C20b (r2, J1-R6).**
  - At the C2 context boundary: each row 52 key refuses before the PlanId, with no worker spawned and its key in the operational record.
  - At the Cargo adapter boundary: an ancestor `.cargo/config.toml`, and an environment override, refuse on row 54. This shares C3-T9's fixture (M3C:716).
  - At the release boundary: a malformed declaration under the labelled synthetic signed release refuses on row 55, before any Plan.
- **The internal keys.** Where no registered public detail names a condition, `domainDetail` is absent and the key goes to the operational record (NE:3546-3555). No public code is added.
- **(r6) SYN-1's routes.** SYN-1 is accepted by CODEX2 at r2 (ACCEPT-DESIGN-UNIT, `reviews/codex2-syn-1-r2`) and bound at product `682991f`. r5 recorded its X-J1 and O-1 as pending. r6 records them.
  - **X-J1, row 52.** SYN-1 adds NE §10's syntax grammar context row after NE:3530 (SYN-1 LD-5). It routes the `native.syntax-grammar-*` and `native.syntax-normalizer-*` keys as NE:3530 routes its own: request-rejected 2, `REQUEST.PRECONDITION_FAILED`, a request detail before the PlanId, with no Plan minted and no file parsed. Each key is emitted in the form NE §1.2's key table gives. Row 52 records them, at J-ε before the PlanId.
  - **X-J1, row 58.** SYN-1 adds NE §10's syntax backend fault row after NE:3541 (SYN-1 LD-12). Row 58 records it.
  - **O-1, row 52.** The native-context admission also emits `native.native-context-closure-malformed:<where>` and `native.native-context-field-mismatch:<subject>`. Row 52 records both. NE:3530 still lists neither: SYN-1 records that gap for the NE owner and changes no NE line.

### 11. Re-commit and the resume writer: owned elsewhere (record of J's interface)

M3P assigns both M2 carry-ins outside J1: re-commit to X3c r8 and X3c-3 (P5-2), and the resume writer to the separate law J-RW and its code unit J4 (P5-1) (M3P:204-205, :284-285, :756-763). J1 decides neither. It records what the pipeline needs from each.

- **Re-commit (X3c r8, X3c-3).** Two analyses of an unchanged project produce the same RunId (IE:104-107). Today the second commit is refused at staging (EXIT:169-171; X3D:51-54). Daily use needs it.
  - **What J needs.** The second commit of a byte-identical Run returns `Committed` with its own attempt row and receipt: "Duplicate retry can share a Run but has a separate attempt receipt" (IE:1683). It must not end on the invariant row. **(r5)** X3c r8 is accepted, and its items 6 and 6a give exactly this (X3C). A re-commit is a new attempt of the same Run, with its own attempt row, SEAL, receipt, association and Run-material row. It ends `Committed`, never on the invariant row, and stages no availability or pins.
  - **Order.** X3c-3 lands before J3d (M3P:265).
  - **Control J-C21 (J3d's).** Two durable analyses of an unchanged scratch project both end `Committed`, with two receipts for one RunId. Recovery of either ExecutionId reports committed. X3c-3's own tests own the storage half.
- **The resume writer (J-RW, J4).** The crash states M2 leaves permanently refused are listed at EXIT:186-191.
  - **J1's constraints on J-RW.** Any writer that resumes them is an X1 ordinary writer reached through item 3's durable entry, never the creator act. It adds no public code, class, exit or detail. It deletes no user data and adopts no foreign artifact (OWN:111-120).
  - **(r6; J-RW r4's RW-S8) J-RW's decisions replace r5's recommendation.** J-RW r4 is accepted (Codex; JRW). There is no separate repair operation. Each L11 family is completed inside the next admitted durable write request that reaches its owner's step, by that owner and under that owner's lock (JRW item 2). A state that is not exactly one of JRW item 4's keeps today's refusal (JRW item 5). No read path completes anything: the 458c read session, `doctor`, the read-only recovery selector, the sweep and the ephemeral entry keep today's refusals (JRW item 2). r5's recommendation, "complete forward at the next durable request's admission, by each owner's own predicates", is withdrawn.
  - **Record correction (r4).** r3's sentence "A `repair recover` command is M5 (BP:973)" is withdrawn. `repair-recover` is the source-repair journal recovery command, `opensip repair recover REQUEST-ID [--apply-recovery]` (CINV:988-989), a closed table over repair-journal states (WS:1024) under S10.2's authorization (SL:673), owned by `crates/host/src/repair.rs` (BP:973). It is not a storage-repair or crash-state resume command. The error was found by the J-RW r1 drafter (X-RW-8).
  - **Control J-C22** is J-RW's to define. J3d keeps one test: a durable request over a resumable fixture behaves exactly as J-RW fixes. **(r6)** JRW item 9 defines it: one host durable request over an RW-R5 fixture ends `Committed`, with one receipt and an ordinary envelope (`firstUse: false`); one over an N-R2 fixture ends on `identity-recovery-required`, with nothing written.

### 12. Controls, tests and the crash matrix

- **`workflow_tests.rs`** (COV:7865) carries J-C1 to J-C21 and J3d's half of J-C22, on scratch homes with labelled synthetic signed releases, profiles and closures under the existing `scenario-fixtures` surface (X3D:36-40). It adds no production seam. J's tests also cover:
  - every WFC invocation case M3's step lists can express: WFC:3612, :3741, :4592, :4650 and :4720, plus `operational-fault-dominates-committed-policy-failure`;
  - the CINV goldens `default-first-use-durable` (CINV:1747), `analyze-renderer-failed-after-commit` (:1793), `interrupted-before-settle` (:2047) and `interrupted-after-settle` (:2055).
- **The crash matrix rows J's code must keep passing.**
  - **Both lead sets** (storage 381, host 98 required runs at C = `3d2d5b5`) are rerun on each integration commit of a J unit that touches `crates/security`, `crates/storage` or `host/src/finalization.rs`. The runs are serialized with every other lead set. The 5000 ms timing guard means no concurrent matrix run (M3P:567).
  - **The rows J's units touch:**
    - F00 (census, `x3d.session.execution-draw`);
    - F01 (host replay refusal, with the new `finalize` signature);
    - F06, F11 to F17, F18 and F19;
    - F29 and F30 (lease contention; the lease is now held through analysis);
    - F32 (the capacity rollover, host);
    - F34, F38 to F42, and F44.
  - **Each must keep its transcribed expected value** (X9:1089). A changed driver or expectation (F01, F12, F16, F17, F32, F39 and F40 host halves, because of item 7's signature) is re-transcribed by **S12** (X9 r17, record) **before** that unit's review, never read back from a run.
- **New rows (S12).** Each is transcribed before any run. **(r5)** S12-C and S12-U, which pin rules 2 and 1 for a signal, are transcribed only once S21 is accepted (8.3), as S12-O waits for S18. **(r6)** S18 and S21 are both bound, so all five rows may be transcribed, in a later round of X9 r17 that fills its reserved §S12 (X9 r17 LD-17-1):
  - **S12-B:** a hold at `x3d.publish.after-staging`; a signal through the support surface; the expectation is F38's with `REV(operator)` and the interrupted projection;
  - **S12-C:** a hold at `x3c.evidence.commit.before#1`; a signal; the expectation is F39's, with REV reason `operator`;
  - **S12-U:** S12-C with `fail-after` at `x3c.evidence.commit`; the expectation is F40's, never `interrupted`;
  - **S12-U (r2, J1-R1):** this is the row that pins 8.3's rule 1: a latch 1→3 followed by an undetermined evidence `COMMIT` gives the durability row, never F39 or a runId;
  - **S12-D (r2, J1-R2):** in a host run, a hold at `x3d.finish.end-step.after` (F15's point), which is after `finish` and before the output decision point, so a genuinely cancellable phase D point. Then a signal, then a resume. The expectation is `interrupted` with the runId, the Run committed (R1 CH), and no byte of a success envelope;
  - **S12-O (r2, J1-R2; r3, NB-01):** a host hold at `x7.delivery.required.before`, which is inside the final output section, after the output decision point and SOP2's finalization. Then a signal, then a resume. The expectation is the decided envelope and its exit, the Run committed, and the signal **classified as O by the host cancellation source in memory**. No persisted log record is expected: the SOP2 event is post-freeze loss (SOP2:704), which is 8.2's post-freeze case (r5). This row exercises S18's deferral, and it is transcribed only once S18 is accepted.
- **Census.** Item 7 adds no durability point. S-OP-12 adds none: it reuses `x4.gate.latch.after`, and its window bits are in memory. The ExecutionId reservation is in memory too (item 2). The REV reason `operator` adds one end-path body inside the existing reserve.

### 13. Successors

| # | Successor | Owner (law) | Content | Gates |
|---|---|---|---|---|
| S1 | **This law** (the X11 successor) | lead | items 1 to 4; it supersedes X11 r1 items 1a, 3 and 5 for M3. X11 items 2 and 6 stand until the M4 CLI unit. | all J units |
| S2 | L468 r6. **(r6) Accepted** by Codex (`existing-root-admission-468/PROPOSAL-r6.md`, `93f4d014…`; `m2/reviews/codex-j1-successors-s2-s6-r1`, one batch for S2 to S6) | security | item 1's route, and the value-only `created` record on the act's result and its post-rename refusals (item 3); item 7 landed by S13 | J3a. **(r6)** Met. |
| S3 | X1 r2. **(r6) Accepted** by Codex (`ordinary-platform-x1/PROPOSAL-r2.md`, `1d03e1f7…`; the S2 batch) | security | items 1 and 7 (item 3); the read receipt with or without a session (item 6) | J3a, J2c. **(r6)** Met. |
| S4 | L464 r3. **(r6) Accepted** by Codex (`creation-ingress-464/PROPOSAL-r3.md`, `e0803ad9…`; the S2 batch) | security | items 1 and 5: the lent RequestId; the prelude's ExecutionId reserved before P0 (item 2) | J3a. **(r6)** Met. |
| S5 | X3A r6. **(r6) Accepted** by Codex (`store-admission-x3a/PROPOSAL-r6.md`, `cb213261…`; the S2 batch) | security | item 2's consequence | J3a. **(r6)** Met. |
| S6 | X4B r6. **(r6) Accepted** by Codex, with J-RW's RW-S5 record note (`trust-bootstrap-x4b/PROPOSAL-r6.md`, `c8c54154…`; the S2 batch) | security/trust | item 1's rejected bullet; forbidden-substitute wording | J3a. **(r6)** Met. |
| S7 | X2 r10. **(r6) Accepted** by CODEX2, with J-RW's RW-S1 (`project-root-x2/PROPOSAL-r10.md`, `a0d43d99…`; `m2/reviews/codex2-jrw-successors-r1`) | security | item 6's creator branch withdrawn | J3a. **(r6)** Met. |
| S7b | M3-B and X2 successor (E-1); M3-C (E-2); M3-C item 7 and X4T (E-3, E-4) | B, C, trust owners | item 6's joins. **(r6)** E-3's form carries no detail (item 6; lead ruling). **Not yet written:** E-1, and the X4T parts (E-3's trust half, E-4). M3-C r8, accepted in review by CODEX2 (`snapshot-plan-c/PROPOSAL-r8.md`, `578c186e…`; `reviews/codex2-snapshot-plan-c-r8`), effective with M3-L, carries E-2 (LD8-4) and E-3's C half (LD8-5). | J2c |
| S8 | X5 r4. **(r6) Not yet written.** | host | item 3's order (item 7) | J3b |
| S9 | X7 r7. **(r6) Accepted** by GROK2 (X7r7; `m2/reviews/codex2-x7-r7`, directory name kept) | host | items 1, 3, 4 and 8 (items 7 and 8) | J3b. **(r6)** Met. |
| S10 | X3d r9. **(r6) Accepted** by Grok (X3D9; `m2/reviews/grok2-x3d-r9`, directory name kept) | security, storage | 8.1 and 8.6, with the window closed only where a `StoppedSession` is produced (r3); the `refused()` record; item 2's reservation at `open`; **(r6)** the close's admission bit as `StoppedSession::admitted_at_close()` (X3D9 LD9-3) | J3a (item 2), J3b. **(r6)** Met. |
| S11 | X4 r8 (amendment; r2, r3). **(r6) Accepted** by CODEX2 at review round 3 (X4r8; `m2/reviews/codex2-x4-r8-round3`) | security | the cancellation latch as a gate source; the two window bits in the gate's word, preserved by every compare-exchange loop and never reset (8.1). **(r6)** X4 r8 also fixes rule FC: an operation has one first stop, whose cause is recorded with the transition that sets `LATCHED` and never replaced. It adds code unit **X4-F3**, which carries FC for latch sources 1 to 8 and lands before J3b or with it (X4r8 S11.9, LD8-9). | J3b. **(r6)** Met; J3b also waits for X4-F3 (item 14). |
| S12 | X9 r17 (record and rows). **(r6) Accepted section by section** (X9 r17 LD-17-1). Round 1, the frame and §RC, is accepted by Grok (`crash-matrix-x9/PROPOSAL-r17-RC.md`, `89fc47ff…`; `m2/reviews/grok-crash-matrix-x9-r17-rc`). §S12, J1's section, is reserved and carries no rows. | lead | re-transcribed host drivers; rows S12-B, -C, -U, -D and -O (-O after S18; r5: -C and -U after S21; r6: S18 and S21 are bound) | J3b, J3d. **(r6)** A later round of r17 fills §S12, before J3b's review. |
| S13 | J-BS (contract). **(r6) Not yet written.** | workflows/identity | item 9; after F8b's execution | J3d |
| S14 | X3c r8 and X3c-3 (M3P P5-2, M3P:761-763) | storage | re-commit (item 11). J1 needs only its outcome. **(r5)** X3c r8 is accepted (X3C), and X3c-3 follows. **(r6)** X3c r9 is also accepted (CODEX2, `ledger-blob-x3c/PROPOSAL-r9.md`, `46156e8e…`; `m2/reviews/codex2-jrw-successors-r1`). It carries J-RW's RW-S3 and X3c r8's CL-4. | J3d |
| S14b | J-RW and J4 (M3P P5-1, M3P:756-759) | M3-J, with the X2, X3c and X4T owners | the resume writer (item 11), under J1's constraints. **(r6)** J-RW r4 is accepted (JRW), and item 11 applies its RW-S8. | M3-X |
| S15 | S-OP-12 closed | OPP §9 | item 8 with S9 to S11. OPP's next revision cites it. **(r6)** S9 to S11 are accepted. | — |
| S16 | S-B (M3-C). **(r6) Not yet written.** | native | the bounded projections (5.4c) | J units that reach them |
| S17 | M3-PLAN's next revision (record) | lead | the J row and its units (item 14); "J1 fixes the order" done; M3-C's "J1 chooses" items answered. **(r5) Done:** M3P r7 to r9 record them (M3P:265, :619; M3P's "Cross-law items", row S17). | — |
| S18 | **The final-output-section successor (r2, J1-R2):** a passage successor to WS §1's cancellation paragraph (WS:224-231) and to OPP §5.5's phase table (OPP:328-338). **(r5) Accepted** by GROK2 at r2 (ACCEPT-DESIGN-UNIT; `reviews/codex2-s18-r2`), and bound at product `5214350` | the WS owner (product workflows) and the OPP owner (CLI and operability) | Step 1 is terminal when its required output returns. From the output decision point to that moment, a signal is classified as phase O and deferred: it never changes the decided envelope or its exit. The rule is the same for the durable and the ephemeral path (r3). A renderer failure there, before any byte, takes the failure envelope chosen by committed evidence: F16 with the runId when a `PublishedCommit` exists, otherwise WS:1377's no-Run row, both under WS:233-240 (r3). A write failure after the first byte ends exit 4 with no replacement envelope (5.3, 8.2, 8.4). `CancelPhase` gains `O` by SOP2's ordinary registration (SOP2:226-230). It adds no class, code or exit. **(r5; S18 cross-law item 1g)** As accepted, S18 is ten line overrides: five on WS and the matching five on WS's selected effective copy WSE (WS:225, :227-228, :231, :1393; WSE:225, :229-230, :235, :1466). They include the after-settle pair (WS:227-228, WSE:229-230), which defines after-settle by the settlement point (S18 LD-4). With them comes a complete successor copy of OPP r3 with §5.5's row O (`s18/operability/PLAN.md`), selected by S18's record. | **every** output path that uses O: J2c's and J3d's output wiring (r3); S12-O. **(r5)** Met: S18 is bound. |
| S19 | **M3-C r7 (r4, SD-6):** item 16's row 8 narrowed. **(r5) Accepted in review** by CODEX2 (M3C, `a1ee9386…`), and effective with M3-L | the M3-C author (lead) | Row 8's closure admission becomes a selection among the component manifests that R10a, or ER10a, admitted. It adds no admission of its own (M3D:766). The core role closures of M3C item 9 are not component manifests and are unchanged. | D4's integration (M3D's Units); J2b's closure selection. **(r5)** Met once M3-L is in effect. |
| S20 | **M3D's SD-5, for R10a's route (r4, record)** | lead (J1's author) | Item 10 rows, with existing codes only, for the internal refusals M3D assigns to J1's projection (M3D:1179-1180), R10a's and ER10a's `ExcludedForm` among them (M3D:796). Until S20 lands, item 10 has no row for them, and J2a's projection of them is incomplete. **(r5) R10a's and ER10a's route is bound.** SD-5 (Grok ACCEPT-DESIGN-UNIT, `reviews/grok-sd-5-r1`; product `052d3cb`) adds NE §10's row after NE:3540, and item 10 records it as row 56. **(r6) R1's route is bound too.** M3-D item 25's request-class `ExcludedForm` is row 57: M3-D r4 decided it (LD-R4-2), M3-D r5 gives it (X-D4-J1-1), and SD-7 binds NE's row (product `d2c00a9`). **Still owed, as SD-5b:** `MemoryBudgetBelowCeiling`, `ToolOutputBound`, `ToolScratchBound` and `confinement-refused`. SD-5b is written row by row with each refusal's first consumer (M3D:1180; lead ruling): `MemoryBudgetBelowCeiling` before J2b's first provider stage, with D3a; the two tool bounds with C3b; `confinement-refused` with D1b, and only if O7 is decided as recommended. Each adds one item 10 row and one J-C20 test in its consuming unit. r5's "land with D1 to D5 (SD-5 LD-S6)" is replaced. | J2a's projection of those refusals; J3d's R10a wiring and J2c's ER10a wiring, each with D4. **(r5)** Met for R10a's and ER10a's refusal. J2a's projection of the rest still waits. **(r6)** Met for R1's refusal too. Each SD-5b refusal waits for its own row. |
| S21 | **The commit-outcome exception to WS's before-settle rule (r5; LD-r5-2; S18 cross-law item 1f):** a passage successor to WS:226 and to WSE:226, the matching line of WS's selected effective copy. **(r6) Accepted** by Grok at r2 (ACCEPT-DESIGN-UNIT; `reviews/codex2-s21-r2`, directory name kept) **and bound** at product `3f6f9a5` | the WS owner (product workflows), with the X3D and X7 owners; the lead drafts it | A signal observed before settlement leaves the aggregate `interrupted` (130), except where the analysis attempt's commit outcome governs. An undetermined commit takes IE:1680-1681's durability termination with its ExecutionId. A commit latched after FinalGate admission takes SL:551-554's `DELIVERY.REQUIRED_FAILED` row. Each is operational-failed 4 (8.3, rules 1 and 2). It adds no class, code or exit, and leaves S18's lines (WS:225, :227-228, :231) as they are. **(r6; S21 cross-law item 1)** As accepted, the exception covers a required analysis or verify step's commit (S21 LD-3), and the commit's returned outcome decides, never the latch state alone (S21 LD-4). S21 is four line overrides: WS:226 and WSE:226, and the per-kind lines WS:229 and WSE:233, which now say that an analysis attempt that the signal aborts leaves no Run (S21 LD-6). | J3d's durable signal wiring; J-C14's rule-1 and rule-2 signal cases; J-C15b's phase-C projections; X9 rows S12-C and S12-U. **(r6)** Met. |

Not successors: X12r4, whose first-use clause J1 implements unchanged; and S-OP-2, whose finalization point J1 places (SOP2:652).

### 14. Units J2 to J4

Each unit is reviewed on its own. J4 is listed for its interface only; J-RW owns it (item 11). Inventory numbers are assigned at build time under the linear-chain rule.

| Unit | Content | Depends on | Size |
|---|---|---|---|
| **J2a** | `host/src/invocation.rs`: the typed request, the step lists, the join state machine, settlement, the cancellation source and phase recording. `outcomes.rs`: NE §10's deficiency-to-D9 bridge, the route and origin tables (NE:3364-3374, :3523-3575), and item 10's total projection. Pure, with no I/O. Tests: the WFC cases and D9 goldens. **(r6, lead ruling)** It projects an analysis outcome it is given, and derives none of it: J3d and J2c derive it. | P0, J1 | M |
| **J2b** | `host/src/analysis.rs`: the shared analysis core from the capture session through evaluation (J-δ to J-θ), on scratch projects with labelled synthetic closures. It is mode-agnostic and opens no installation. | J2a, and M3P's J2 set: H, C4a, C4c, X12d and its lead set, D3, CF-2, I1-b2, X4-F1 and X4-F2 (M3P:265, :451). Its provider stages also need O7 and D1's primitive (M3P:627). | L |
| **J2c** | The ephemeral entry end to end (item 6). Its output wiring, and J-C14c's O and E cases, wait for S18 (r3, J1-R2-03). Everything else may land before. **(r6, lead ruling)** J2c derives an ephemeral result's analysis outcome: its reasons through J2a's NE §10 bridge, and the RTC §7.4 form, `authority: ephemeral` with no runId and no detail. RTC derives no ephemeral reasons (§7.4). | J2b, S3, S7b; **S18** for output wiring. **(r6)** S3 and S18 are met. Row 27's required-cell leg also waits for the enumeration-contract successor M3-C r8's X-8 recommends. | M |
| **J3a** | Platform and security: `RequestIdentity` and `ExecutionIdReservations` (item 2); the durable entry, its probe, the two-slot attempt and `EntryRefusal` (item 3); the S2 to S7 code; `open`'s reservation (S10, item 2). Tests J-C2, J-C4, J-C4b and J-C5 to J-C9, with J-C6b. | J1, S2-S7, S10's item 2. **(r6)** S2 to S7 and S10 are met. | L |
| **J3b** | X3d r9, X4 r8, X7 r7 and X5 r4 code: `take_cancellation_latch`, the window bits, `Operator`, the `refused()` uses, `finalize`'s new signature, step 1's terminality, the output decision point. S12's rows S12-B, -C, -U and -D. **(r5)** S12-C and S12-U wait for S21 (8.3). J3b also carries the window close sample's admission bit to the host, for LD-r5-1's label (8.2). **(r6)** It reads the bit through `StoppedSession::admitted_at_close()` (X3D9 LD9-3). | J3a, S8-S12; **S21** for S12-C and S12-U (r5); **(r6) X4-F3**, which lands before J3b or in its commit (X4r8 S11.9, LD8-9). S9 to S11 and S21 are met; S8 and §S12 of S12 are not. | L |
| **J3d** | The durable pipeline end to end, R0 to the settlement point; J-BS (S13); `workflow_tests.rs`; J-C10 to J-C21 and J-C20b. Its final output section, its output wiring and row S12-O wait for S18, as J2c's do. **(r5)** Its durable signal wiring, and J-C14's rule-1 and rule-2 signal cases, wait for S21 (8.3). **(r6, lead ruling)** J3d derives a committed Run's analysis outcome from the admitted Run: its ordered D9 deficiencies (RTC §4), its coverageId (RTC §5) and the whole termination's §7 composition (`admit_analysis_step_termination`), which needs the commit receipt (RTC §7.3). | J2b, **F2 and G3** (M3P:265, :451; r2, J1-R5), J3a, J3b, X3c-3 and its rows, **O1** for SOP2's finalization (M3P:269, :457; r2, J1-N2), S13, S16, S18; **S21** for its durable signal wiring (r5). **(r6)** S18 and S21 are met. | L |
| **J4** | J-RW's code unit (M3P P5-1), outside J1. It reaches the pipeline only through item 3's entry. | J-RW | L |

**Critical path (r2, J1-R5).** M3P6 sizes J2 → J3 at 3 + 3, finishing on days 25 and 28. J3 needs J2, F2, G3, X3c-3 and its rows; J4 needs J-RW, not J3 (M3P6:309-311, :322, :572-578). Under this breakdown:
- J2a, J3a and J3b run before or beside H, off the host chain.
- The chain is H → J2b (3) → J3d (3) → M3-M, so the host-chain figure is unchanged **only if** all of these finish by J2b's last day, M3P's day 25:
  - F2 and G3, whose M3P finishes leave slack against J3;
  - J3a, J3b, X3c-3 and its rows, with their serialized lead sets;
  - O1, S18 and (r5) S21. **(r6)** S18 and S21 are bound. J3b's new dependency, X4-F3 (X4r8 LD8-9), sits inside J3b's term. M3-PLAN r10 records that edge and keeps the 33-day host chain (M3P10:81-82).

  If any of them is late, J3d waits for it, day for day, and the path runs through it. Their assumed early finish keeps the estimate, but it does not remove the dependency.
- J4 follows J-RW, as M3P has it.
- The whole-chain estimate stays M3P's conditional 33 days (M3P:465-467). Item 14 changes it only through the waits above, and S17 carries the unit names.

### 15. Record corrections (record only)

- **M3P6:217.** J's units are item 14's. M3P6:468's "J1 fixes the order and identity rules" is done by items 2 to 4. **(r5)** M3P has applied both (M3P:265, :619; S17).
- **X11:28's "The M3 unit replaces all four refusals at once"** reads per command (item 1; r2, J1-R7). `audit`'s refusal stays until M5.
- **X11:78-80 (F0 after pack admission)** reads per item 3 under X12 r4.
- **X7:11's "no CLI command is wired (X11 owns CLI enablement)"** now reads: J1 and the M4 CLI unit.
- **The M3C items J1 was asked to choose:** M3C:137 → 5.4a; M3C:210 → 5.4b; M3C:313, :599, :613 → 5.4c; M3C:896 → J-η.

## Forbidden substitutes

- An analysis word wired in the binary at M3; any binary or ingress seam (X11:118).
- Two RequestIds; a RequestId or ExecutionId from a caller or from text; an ExecutionId used before its process reservation (r2); a RunId before `Committed`.
- A creation intent or notice when I is present; authority from the probe; a creator observation reaching attempt B; a second gate; a third attempt; a creation disclosure dropped on a refusal after the rename, or taken from anything but the act's own result (r2).
- Pack admission after any project-scoped effect (X12r4:197-200); a storage-choice refusal after one.
- A store write before the attempt row; a downward walk under the fence; a lease released before the commit's `finish`.
- A retry of any attempt; a re-entered join.
- A signal latch outside its window, minted twice for one operation, or used as authority; a cancellation reported as a value to keep a ledger open (X3D:383).
- Selecting F39 from the gate's state rather than from a returned `Committed(PublishedCommit)`; F39 or a runId for any `CommitUndetermined` (r2); projecting a `Committed` with a latch, or any `CommitUndetermined`, as `interrupted`; projecting phase D as X7's F39 row.
- Calling the output decision point settlement; re-deciding the envelope after it; a replacement envelope after output has begun (r2); rewriting a settled class (WS:1393).
- (r3) Closing the window on `Ok(PreparedCommit)`, or anywhere a `StoppedSession` is not produced; a compare-exchange that drops the window bits.
- (r3) F16, or a runId, for a renderer failure with no `PublishedCommit`; an uncertain step 0's ExecutionId dropped from the failure envelope.
- (r3) Wiring any output path that uses phase O, durable or ephemeral, before S18 is accepted; requiring a persisted log record of an O signal after SOP2's freeze.
- (r4) A manifest-class refusal (M3D item 24) after R11, R12 or the ephemeral attempt's start; an analysis-attempt ExecutionId drawn or reserved before R10a or ER10a returns; the creation prelude's ExecutionId bound to the analysis attempt.
- (r5) Labelling a signal that follows a `publish` return that does not enter D as D, as A, or by a new `CancelPhase` member. A rule-1 or rule-2 termination delivered, or asserted by a control or row, for a signal before S21 is accepted, outside J2a's pure model. WS:226 amended outside a reviewed contract successor.
- `audit`'s refusal replaced before its M5 comparison step exists (r2).
- A `backupStatus` without `firstUse`, or `not-backed-up` from a missing detector.
- An ephemeral write, lease, registration, bootstrap, creation, runId or authoritative label.
- A new public code, class, exit, fault cause or detail; a wildcard termination arm.
- Any crash-matrix expectation read back from a run.

## Open questions

**No owner decision blocks J1.** O7 gates provider launch (J-ζ; J2c), not this law (M3P:627).

**Flagged for the owner (non-blocking lead decisions the owner may reverse):**
1. No CLI command at M3 (item 1). The owner's first daily use of `analyze` is M4, with signed releases.
2. First use creates I and then admits a fresh ordinary writer in the same process, running the core and platform producers twice on first use only (item 3).
3. `--ephemeral` reads the installation when one is complete. With no installation, it is indeterminate for every closure-backed capability (item 6). **(r6, lead ruling)** That result carries no detail, so it carries no detail remedy either (RTC §7.4). r5 named WS:1374's install remedy here.
4. M3 does not retry a busy durable attempt in-process (5.1).
5. (r2) A signal that arrives while the required envelope is being finalized, rendered or written is deferred: it never changes the envelope or the exit (phase O, S18). The alternative would be exit 130 beside a success envelope that has already been decided.
6. (r5, LD-r5-1) A signal can arrive after the commit has returned anything other than an unlatched `Committed`, and before the output decision point. It is labelled B or C, the last phase the operation reached. The label changes no outcome.
7. (r5, LD-r5-2) Where a signal meets an undetermined commit, or a committed Run latched after admission, IE's and SL's exit-4 rows govern over WS's `interrupted` 130. WS gains that exception through successor S21. The wired signal paths that can produce those terminations wait for S21. **(r6)** S21 is bound, so they no longer wait.

**Routed to the lead (r6; not a J1 decision), and ruled:**
- **NE's excluded-form row and E-3.** That row (SD-5, as SD-7 supersedes it at NE:3540) says that a required closure current trust does not admit, "an ephemeral request with no trust view included", keeps the not-installed golden: `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`. Under the lead's ruling, RTC §7.4 gives that ephemeral form no detail (item 6; row 27). r6 amends no NE text. **Lead ruling:** an NE passage supersession, **SD-8**, of SD-7's NE:3540 override. It keeps every word of that row except the ephemeral no-trust form's detail, which §7.4 drops. SD-8 is owed before J2c, the first unit that emits the ephemeral form. **Rejected:** reading the sentence as fixing only the class and code. That leaves a bound contract sentence contradicting §7.4.

**For the reviewer:**
- **R1.** Is the presence probe (item 3, step 2) lawful against OWN §1a, §5 and §6, and against X1 item 1's purpose-typed receipts?
- **R2.** Does the two-slot attempt (S3) keep the purposes of the one-attempt rule, which are no laundered budget and no reused receipt?
- **R3.** Is opening the session at the handoff (item 7) sound against X5 item 3 and IE:1657-1658, with X3d unchanged?
- **R4.** Is the latch window (8.1), now in the gate's own word and closed on every return, the right boundary for phases B and C? Does 8.3's outcome-first precedence close J1-R1 against X3D:170 and X7:100-101?
- **R5 (r3).** Do 8.1's open-across-`Ok(PreparedCommit)` window (J1-R2-01), 8.2's evidence-dependent renderer route (J1-R2-02) and 5.3's common S18 gate (J1-R2-03) close the r2 findings? The r2 question follows. Do 5.3, 8.2 and 8.4 close J1-R2? That is: step 1 terminal only when its output returns; the output decision point not called settlement; phase O routed as an exception through S18; S12-D at a cancellable D point and S12-O inside O.
- **R6.** Is J-BS's in-place append lawful under the versioning rules, and does item 9's presence rule from publication (with `EntryRefusal.created`) close J1-R3?
- **R7.** Does item 2's `ExecutionIdReservations` meet IE:77-81 for every ExecutionId, and is it kept distinct from the durable attempt row (IE:83-101; X3D:130-134)?
- **R8.** Are rows 52 to 55 routed exactly as NE:3530-3532, :3540 and :3574 fix them, and is any reachable M3 family still missing?
- **R9 (r6).** Is each r6 change faithful to its source, as the r6 changes table cites it? Does r6 change anything that no source or lead ruling calls for?
- **R10 (r6).** Does every re-pinned citation resolve to the same fact: the M3D r3 → r5 map, the seventeen live-file pins, and the drop of 2 for M3B, I1, OPP and AQP?
- **R11 (r6).** Can row 27's ephemeral form stand beside NE's excluded-form row as bound, or must that sentence change first?

## Not claimed

- No command enabled; no CLI wiring; no M4 renderer; no `fit` or `audit` pipeline.
- No code, test, build or matrix run for this law.
- No measurement. The critical-path figures are planning assumptions.
- No positive backup detector; no bounded retention; no durable RequestId or ExecutionId registry beyond attempt custody.
- No confinement claim (O7, CF-1); no provider launch rule (D law).
- No settlement of `admitted` attempt rows at M3. X6's sweep reaches them when `store-gc` lands (M5, BP:990), as in M2.
- No elapsed bound on a second-signal wait inside a native effect, or on a blocked output in phase O (OPP:339).
- **(r5)** S-OP-2 r6 is accepted (Codex). J1 places its finalization point (SOP2:652) and changes nothing in it.
- **(r5)** No WS successor is written here: S21 is owed (8.3). No route is given for M3-D item 25's request class (X-SD5-1), and no SYN-1 row is added (item 10). **(r6)** S21 is bound, row 57 is M3-D item 25's route, and rows 52 and 58 carry SYN-1's routes. r6 writes no contract text and amends no NE line (item 10).
- No change to the binary's bytes, to `doctor`, or to any accepted public code, class, exit or detail.
- J1 was written from reading the product at `3e64266` and the laws named above. r2 rereads none of the product beyond the r1 citations and `commit_session.rs:939-958`. **(r5)** r5 reads no product file. It only re-checks, at main `5214350`, that the files J1 cites are unchanged (see "Short names"). **(r6)** r6 reads no product file either. It re-checks at main `1799d3d` that no file J1 cites changed since `5214350`.
