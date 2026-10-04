# S18 — the final output section (contract successor of law M3-J1)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r2, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, class, exit code, route or public code. It needs GROK2's `ACCEPT-DESIGN-UNIT` and the lead's root assent before it can be bound in the product's `design-lock.json`.

**Review history.** r1 (subject `9d184011…`) was reviewed by GROK2 in `reviews/codex2-s18-r1/`; the directory keeps the name of its first CODEX2 assignment. The verdict was REQUIRED-FINDINGS, with one required finding (RF-1) and two non-blocking observations (NBO-1, NBO-2). GROK2's other rulings (2 to 6) upheld the rest of r1, LD-1 to LD-12 among it. r2 answers RF-1, records both observations and changes nothing else of substance. The r1 members r2 changes are kept, byte for byte, in `reviews/codex2-s18-r2/r1-members/`.

**What it is.** Accepted law **M3-J1 r4** names successor **S18** (J1:772): "a passage successor to WS §1's cancellation paragraph (WS:224-231) and to OPP §5.5's phase table (OPP:330-340)", owned by the WS owner (product workflows) and the OPP owner (CLI and operability). It reconciles J1's **phase O**, the final output section, with both. J1 r3's acceptance moved CODEX2's two non-blocking observations, J1-R3-NB-01 and J1-R3-NB-02, into S18's text, not into the law (J1:11). S18 carries both.

**What waits on it.** Every output path that uses phase O: J2c's ephemeral output wiring, J3d's durable output wiring, J-C14c's O and E cases, and crash-matrix row S12-O (J1:394-395, :555, :786, :789, :746).

**Product.** Main `392499e`, read only, with 83 contract successors (CRC-1 was bound there after r1, which was built on `cd5958b` with 82). S18 binds there, 83 to 84 (see "Evidence runs").

## r2 changes and review response

| Finding | Change |
|---|---|
| **RF-1** (after-settle is still defined by terminality alone) | **Four new line overrides** define *after-settle* by the **settlement point**. The parenthetical spans two lines on each parent: WS:227-228 and WSE:229-230. Each pair makes the same two insertions: <br>- "(every required step" becomes "(after the settlement point: every required step"; <br>- "already terminal):" becomes "already terminal and, where the final output section below applies, the required output returned):". <br>The whole parenthetical now reads: "*after-settle* (after the settlement point: every required step already terminal and, where the final output section below applies, the required output returned)". An interrupted invocation, whose render step is `cancelled` at the decision point, is therefore not after-settle while its termination output is written. **The paragraph's settlement sentence** names the term: "The invocation settles when the output returns and not earlier: that return is its settlement point, so *after-settle* begins only then." <br>**Three-way partition.** Where the final output section applies, the three phases now partition time: *before-settle* runs up to and including the output decision point (WS:225, unchanged since r1); *final-output* runs from the decision point to the settlement point; *after-settle* runs after the settlement point. Elsewhere, both definitions read as before. WSE's lines carry other words around the parenthetical (the optional-Run sentences), so its `before`s are its own lines, and its `after`s make the same insertion. |
| **NBO-1** (INV5's after-settle description) | Recorded as cross-law item 4 for the invocation-record owner. INV5 is not changed here; LD-5 keeps an O signal out of that record. |
| **NBO-2** (S-OP-2 r6:653's drain sentence) | Recorded as cross-law item 2, as GROK2 suggests: O1 carries row O's qualifier. The cancellation drain applies only when the decided envelope is `interrupted`, so an O signal during a success envelope does not shorten the drain. The plan copy's row O already says this (LD-9), and the copy is unchanged. |
| Base and records | The base is `392499e`, read with `git show`. No lock entry is on any of S18's ten selectors there. CRC-1 sits at WS:308 and WSE:312, with no clash. `build_s18.py` emits the review path `codex2-s18-r2`, and the unit draft is renewed. |

**What r2 changes, by member.** The diff base is the r1 subject, `9d184011…`:
- `successor.json`:
  - the four new overrides;
  - one changed `after`: WS:231 and WSE:235, the settlement sentence;
  - the `standing`, which now counts ten overrides and names the after-settle lines;
  - the candidate pins.

  The six r1 `before`s, the selectors and the other `after`s are unchanged.
- `PASSAGES.md` and `evidence/copies-report.json` are regenerated. The report now records `392499e` and CRC-1's bound entries.
- `evidence/build_s18.py`, `check_s18.py` and `verify_scratch.py` are updated for the ten overrides and the new base.
- This README is updated.
- `operability/PLAN.md` is unchanged (`69af0f1b…`).

## Short names

| Name | Document |
|---|---|
| **J1** | `docs/implementation/m3/host-pipeline-j/PROPOSAL-r4.md`, the M3-J1 r4 bytes GROK2 accepted (120,506 bytes, `c18c0d3c…`; `reviews/grok2-host-pipeline-j-r4`). r3 (`ad887c90…`) was accepted by CODEX2 (`reviews/codex2-host-pipeline-j-r3`), and r4 changed nothing S18 touches. |
| **NB-01, NB-02** | J1-R3-NB-01 and J1-R3-NB-02 in `reviews/codex2-host-pipeline-j-r3/review.json` |
| **RF-1, NBO-1, NBO-2** | GROK2's findings on S18 r1, in `reviews/codex2-s18-r1/review.json` |
| **WS** | `docs/v2/contracts/product-v1/workflows-and-surfaces.md` (133,335 bytes, `1ee203e3…`), an accepted lock input |
| **WSE** | `docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md` (139,497 bytes, `4478ce1a…`), WS's selected effective copy, accepted as a member of `source-selection-v3` |
| **OPP** | the operability plan. Its accepted r3 bytes are `docs/implementation/m3/operability/PLAN-r3.md` (70,544 bytes, `b49035f2…`). The live `PLAN.md` adds only the two-line acceptance note after line 1, so live line n is r3 line n-2 from line 4: J1's OPP:330-340 is r3:328-338. Cited here as "OPP r3:n". **Not a `verify_design` input.** |
| **SOP2** | `docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, S-OP-2 r6, accepted ACCEPT-DESIGN-UNIT by Codex (130,001 bytes, `ce8d3a4b…`; `reviews/codex-s-op-2-r6`). It binds with M3-O's O1 unit. J1 cites r4's lines; this unit cites r6's (the map is under "Cross-law items"). |
| **X7** | `docs/implementation/m2/finalization-x7/PROPOSAL-r6.md` (28,729 bytes, `9e17faf2…`). The live file differs only by its acceptance words, line for line. |
| **X3D** | `docs/implementation/m2/commit-session-x3d/PROPOSAL-r8.md` (62,445 bytes, `5e491b92…`), the same way |
| **RTC** | `docs/coop/design-corrections/foundation/run-termination-contract.v1.md` (`cfe793fc…`), the owner WS:1404-1414 incorporates, an accepted lock input |
| **INV5, ENV7** | `opensip/schemas/sources/{invocation-v5, command-envelope-v7}.schema.json` at `392499e` (unchanged since `cd5958b`) |
| **CINV** | `docs/coop/design-corrections/workflows/command-inventory.v3.json` |

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: every override's exact `before` and its `after`, and every edit of the plan copy |
| `successor.json` | the contract successor record: two parents (WS, WSE), ten passage overrides, no supersession, seven candidates |
| `operability/PLAN.md` | generated: the complete successor copy of OPP r3, selected by the record |
| `evidence/copies-report.json` | generated: the copy's parent, its relation to the live plan, each edit with its r3, live and copy line, and the bound entries on WS and WSE |
| `evidence/build_s18.py` | builds every generated file, the record, the subject manifest and the unit draft; `--check` compares instead of writing |
| `evidence/check_s18.py` | read-only, independent checks: pins, the lock and in-flight records, the copy's alignment, content and every citation |
| `evidence/verify_scratch.py` | runs the real `verify_design` with a synthetic review and assent, and a conflicting-override probe |
| `../s18-subject.json` | the subject manifest (generated) |
| `../s18-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`, with the review path `reviews/codex2-s18-r2/review.json`; not part of the subject |

## What changes

**Ten line overrides**, five on WS and the matching five on WSE. Three pairs (225, the paragraph's end, the golden row) have byte-identical `before` and `after`. The two after-settle pairs make the same insertion inside lines that otherwise differ. `PASSAGES.md` has the full texts.

| # | Parent and line | Change |
|---|---|---|
| 1, 6 | WS:225, WSE:225 | The *before-settle* definition gains "and, where the final output section below applies, the signal observed no later than its output decision point". |
| 2-3, 7-8 | WS:227-228, WSE:229-230 (r2) | The *after-settle* definition runs "after the settlement point: every required step already terminal and, where the final output section below applies, the required output returned". |
| 4, 9 | WS:231, WSE:235 (the last line of the cancellation paragraph) | The line is kept, and a new paragraph follows it: **Final output section**. |
| 5, 10 | WS:1393, WSE:1466 (§9's golden row "SIGINT before / after settle") | The detail cell gains "a signal in the final output section (§1) is deferred and the decided class stands". |

**The new WS paragraph says**, in order:
1. **Scope.** It applies to an invocation whose last required step is the `render` step that writes its one required envelope.
2. **The output decision point.** This is the one cancellation check after every other required step is terminal and the render step's projection is done.
   - A signal observed no later than the check is before-settle. The render step is `cancelled`, its projection discarded, and the termination output is what the rule above gives.
   - Otherwise the envelope is the aggregate's.
3. **The final output section.** It runs from the decision point until that one envelope's output returns.
   - A render step that was not cancelled is terminal only then: it completes on a written and flushed envelope, and fails on a projection, renderer, write or flush failure.
   - The invocation settles then. That return is its settlement point, and *after-settle* begins only then. The after-settle parenthetical (WS:227-228) says the same.
4. **A signal in the section is *final-output*.** It is deferred:
   - it changes nothing the decision fixed (kind, termination, class, exit code, `runId`, errors, results);
   - it selects no interrupted form and cancels no step;
   - it is recorded neither in the envelope nor in an invocation record the envelope carries;
   - it is classified in memory, and its only record is the operational one.

   Durable and ephemeral analyses follow the same rule.
5. **A renderer failure before any byte of the decided envelope.** The render step fails, even where it was `cancelled` for a termination output. §8's required-output law (WS:1128-1145) chooses the detail by committed evidence:
   - `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` with the `runId`, when an earlier step committed a Run (WS:1376; X7's F16 row, X7:99);
   - otherwise `DELIVERY.REQUIRED_PROJECTION_FAILED` with no `runId` (WS:1377).

   The aggregate (WS:233-240) then decides the termination, and the resulting failure envelope replaces the decided one.
6. **An uncertain analysis attempt (NB-01).** It keeps its termination, ExecutionId and namespace disclosure under its fault owners: X3d r8 items 6 and 9 (X3D:176, :283) and X7 r6 items 3 and 5 (X7:101, :120). It stays out of verdict and closed-Run composition (§9: WS:1412-1413; RTC §7.1). Its ExecutionId and namespace stay disclosed whichever termination is primary, and they are never the render attempt's or a Run's.
7. **A failed write or flush of the decided envelope.** The invocation ends with exit 4, one coded standard-error line and no replacement envelope, whether or not any byte was written. A failure envelope that cannot be rendered ends the same way.
8. **Nothing is added.** No class, code, exit, field or step outcome.

**The plan copy** `operability/PLAN.md` (74,185 bytes, `69af0f1b…`, unchanged in r2). It is OPP r3 with five lines replaced and one inserted, and no other byte changed:

| r3 line (live, copy) | What it is | Change |
|---|---|---|
| 293 (295, 293) | §5.2's "User interrupt, any phase" outcome row | `interrupted` 130 only for a signal observed no later than the output decision point (and there only before FinalGate admission or after an unlatched commit); the decided class in the final output section |
| 328 (330, 328) | §5.5's lead-in to the phase table | Phases A to D end at the output decision point. A signal after it takes row O. An ephemeral request, or one that admits no attempt, stays in A until the decision point, then takes O and E. |
| 335 (337, 335) | row D | It ends at the decision point, where the render step is `cancelled`. Its envelope is the termination output, written in its own final output section. r3's open question ("S-OP-12 decides … whether a signal during the same step's required delivery takes this row or X7's latched row") is answered as J1 8.4 decided it. |
| — (—, 336) | **row O**, inserted | Phase O, with NB-02 and `CancelPhase` O (below) |
| 336 (338, 337) | row E | "Every required step terminal and the required output returned", the same settlement point as WS's after-settle definition |
| 433 (435, 434) | §10's cancellation control row | Phases "A–E and O", with the three O cases by S-OP-2's cutoff and freeze |

**Row O** says the following.
- **Deferred.** The signal is classified O in memory. It changes nothing the decision point fixed, selects no interrupted form and cancels no step.
- **A second signal** is deferred the same way. It waits for an in-flight write with no elapsed bound (OPP r3:339).
- **The record.** `host.signal.received` is attempted with `arrival_phase` `O`. `O` is a `CancelPhase` member added by S-OP-2's ordinary registration (SOP2:226-230).
- **When the record is lost (NB-02).** Its fate follows S-OP-2's finalization, which runs inside O (SOP2:652-683):
  - before the producer cutoff (step 1), the record is admitted;
  - after the cutoff, the call commits `drain-abandoned`. The frozen summary counts it if the commit precedes the freeze's reads (step 4), and a call still uncommitted at the freeze is disclosed in `in_flight_at_freeze`;
  - after those reads, it goes only to the post-freeze tally, which no carrier reports (SOP2:682, :704).
- **How a loss can reach the envelope.** Only as S-OP-2's loss line in `diagnostics` (SOP2:766), never in termination or exit.
- **What never changes.** No sink is reopened, and the frozen summary never changes.
- **The deadline.** Finalization keeps the decided termination's deadline (OPP r3:195-196).
- **Failures.** The renderer and write failures are as in WS.

Nothing else changes: no code, class, exit, field, step outcome, public code, schema, inventory, registry or product file.

## J1's S18 row, item by item

| J1 (r4) | Where S18 carries it |
|---|---|
| "Step 1 is terminal when its required output returns" (J1:772; 5.3, J1:386-389) | WS ¶ points 3 and 5; WS:227-228's after-settle definition (r2); OPP row E |
| The output decision point (8.4, J1:552) | WS ¶ point 2; OPP lead-in and row D |
| "From the output decision point to that moment, a signal is classified as phase O and deferred: it never changes the decided envelope or its exit" | WS ¶ point 4; OPP row O |
| "The rule is the same for the durable and the ephemeral path" (r3) | WS ¶ point 4; OPP lead-in and row O |
| Renderer failure before any byte: F16 with the runId when a `PublishedCommit` exists, otherwise WS:1377's row, both under WS:233-240 | WS ¶ point 5; OPP row O |
| "A write failure after the first byte ends exit 4 with no replacement envelope" | WS ¶ point 7 (LD-8 reads it for every write failure) |
| "`CancelPhase` gains `O` by SOP2's ordinary registration (SOP2:205-208)" | OPP row O, at r6's lines 226-230 |
| "It adds no class, code or exit" | WS ¶ point 8; `check_s18.py` checks that every code in the new text is already in WS or OPP, and that every exit is in the fixed table |
| NB-01 (J1:11) | WS ¶ point 6; OPP row O's cell |
| NB-02 (J1:11) | OPP row O |

## Why this form

- **WS's and WSE's lines are free.** In the lock at `392499e`:
  - WS's only bound overrides are lines 308 (CRC-1), 598 and 603 (I1-L), and 1296 (initial-root-binding);
  - WSE's are lines 312 (CRC-1), 602 and 607 (I1-L), and 1300 (initial-root-binding).

  None is in the cancellation paragraph or §9's golden table. No unbound successor record in arch touches S18's selectors either. `build_s18.py` asserts this against the lock, and `check_s18.py` scans every unbound record. Line selectors are therefore the form.
- **OPP cannot be a parent.** `contract_successor` admits a parent only if it is in the lock's accepted set (`tools/verify_design.py:221-229`). Neither `PLAN.md` nor `PLAN-r3.md` is, so the copy is an ordinary candidate at a new path. This is CR-1's case, with B-S9's selection form.
- **The copy is of the accepted bytes.** It is copied from `PLAN-r3.md`, Codex's r3, never from the live file (the pin rule). `copies-report.json` records the live file's two-line difference and the line map.
- **A later unit cannot silently replace S18's WS meaning.** `verify_scratch.py`'s probe shows that a second override of WS:231 is refused ("conflicting contract passage overrides").

## Lead decisions

Each decision is dated 2026-10-04 and made under the owner's standing direction to proceed on the lead's recommendation. Each names the alternatives it rejects, and the owner may reverse any of them. GROK2 upheld LD-1 to LD-12 in r1 (its rulings 2 to 5). LD-4 is amended in r2 for RF-1, and LD-2 now covers five lines.

**LD-1. The form: line overrides on WS and WSE, and a complete copy of OPP r3 selected by the record.**
- **Rejected:**
  - **a fragment document holding only §5.5's new table** (I1-L's §4a form). It selects part of a file that `verify_design` does not track, which no accepted unit has done, and a reader would have to compose two texts;
  - **making OPP a lock input.** That needs a new application manifest and its approval chain, for one plan;
  - **editing the live `PLAN.md` (an OPP r4).** That is the OPP owner's revision, outside this unit, and it would skip the design-unit review. OPP's next revision starts from this copy instead (cross-law item 3);
  - **copying the live `PLAN.md`.** Its acceptance note is not accepted bytes (the pin rule);
  - **J1's `PROPOSAL-r4.md` as a candidate** (I1-L's LD-L7). Nothing materializes from it. The record's standing pins it by sha256.

**LD-2. WSE takes the same overrides.** This follows I1-L's LD-L5 and the X12-0 and initial-root-binding precedents. WSE's cancellation paragraph is four lines longer (the M1 interruption owner's optional-Run sentences), so its lines are 225, 229-230, 235 and 1466.
- Three pairs carry the same texts.
- The after-settle pair (r2) makes the same insertion inside WSE's own lines.
- **Rejected:** WS alone, which would leave the selected effective copy contradicting WS.

**LD-3. Scope: every invocation whose last required step is the `render` step that writes its one required envelope.** In CINV that is 44 of 45 commands. `agent-serve` (steps `query`) is outside. The reason J1 gives for O, one required envelope that carries its own exit code (J1:553), holds for every such command.
- **Rejected:** M3's three requests only. That would leave WS §1 contradicting itself across commands that share a renderer, and the M4 CLI unit would need another successor.

**LD-4. The interrupted termination output is written in a final output section, and the settlement point is its output's return.** J1 says both that a D signal's envelope "is rendered and written in its own final output section" (J1:534) and that the render step is `cancelled` at the decision point. Read literally, a cancelled step would settle the invocation before its own termination output is written. S18 therefore defines the section by the decided envelope, whichever it is, and settlement by its output's return. A renderer failure of a termination output fails the render step, as J1's row 44 ("an interrupt with no Run", J1:690) and 8.2's "aggregate … over both required steps" require.
- **r2 (RF-1).** The after-settle parenthetical (WS:227-228, WSE:229-230) is amended in place to the same settlement point, so §1 has one definition: every required step terminal and, where the final output section applies, the required output returned.
- **Rejected:** settling an interrupted invocation at the decision point. The termination output's own rendering would then be after-settle, and rows 43 and 44 would have no step to own the failure.
- **Rejected (r2):** overriding only the parenthetical's second line (WS:228, WSE:230), as RF-1's minimal fix allowed. The lead's direction is to define after-settle by the settlement point, and the opening line is where the definition starts.

**LD-5. A final-output signal enters neither the envelope nor an invocation record it carries.** INV5's `Cancellation.phase` is closed: `none`, `before-settle`, `after-settle`. Its descriptions fit neither for a phase-O signal: before-settle says the aggregate is `interrupted`, and after-settle says every required step is terminal. At M3 the record appears only as ENV7's `invocation` member, which no M3 envelope carries. The record inside an envelope is part of the decided bytes. So its `cancellation` stays as the decision point fixed it, and the O signal's record is operational only. INV5's after-settle description lacks RF-1's output-returned conjunct; that is NBO-1, cross-law item 4.
- **Rejected:**
  - a new `phase` member, which is an INV5 successor with no M3 carrier;
  - recording O as `after-settle` or `before-settle`, whose schema descriptions it would falsify;
  - the latter would also break WSE's `J-INTERRUPTION-LEDGER`, which requires before-settle to carry the interrupted form (WSE:1389-1395).

**LD-6. NB-01: cite the fault owners directly.** The uncertain attempt's identity and namespace are X3D's and X7's (X3D:176, :283; X7:101, :120). WS §9 already returns fault terminations to their owners (WS:1412-1413), as RTC §7.1 does (RTC:220-225). CODEX2's row-44 ruling stands: the tie rule decides the primary, and the disclosure stays either way. That ruling is: "Row 44 therefore does not unconditionally replace an earlier detailed operational fault".
- **Rejected:** J1 r4's "through WS:1409-1411's composition of a termination's `executionId`" (J1:535). That passage is verdict composition, which this fault never enters.

**LD-7. NB-02: a three-way rule in OPP row O.** Classification and deferral are common to all of O. The event's fate follows S-OP-2 r6's real cutoff, reads and freeze. WS says only that the record is operational, because the sink law is S-OP-2's.
- **Rejected:**
  - J1 r4's "because O follows SOP2's freeze, that event is post-freeze loss" (J1:535). O begins before finalization (J1:552), so that holds only for the last part of O, which is S12-O's;
  - CODEX2's alternative, delayed emission after settlement. It needs a sink after the freeze, so a reopened gate, which SOP2:682 and :704 rule out.

**LD-8. Every failed write or flush of the decided envelope is final**, whether or not any byte was written. J1 states it "after the first byte, including one whose call cannot prove that no byte escaped" (J1:535). `deliver_required` uses `write_all` (`crates/host/src/delivery.rs:17-21`), which never reports how many bytes it wrote. `bootstrap.rs:55-60` already ends every such failure with exit 4, the coded line and no replacement.
- **Rejected:** a replacement after a provably empty write. The API cannot prove it, and the replacement would go to the handle that just failed.

**LD-9. S-OP-2's finalization keeps the decided termination's deadline.** That is OPP r3:196's cancellation drain only when the decided envelope is `interrupted`, and r3:195's normal drain otherwise. S-OP-2 r6:653 does not yet carry this qualifier; that is NBO-2, cross-law item 2.
- **Rejected:** switching to the cancellation drain when an O signal arrives. It would let the signal change the decided envelope's frozen `diagnostics`, and it would move a deadline mid-wait.

**LD-10. The plan copy changes only what the final output section touches.** That is §5.5's lead-in and rows D, O and E, plus two consequential rows: §5.2's interrupt row and §10's control row.
- **Left for OPP's next revision under J1's S15 ("S-OP-12 closed"):**
  - rows A to C;
  - the note after the table (r3:338);
  - §9's S-OP-12 row (r3:415).
- **Rejected:**
  - carrying S15 now. J1 gives it to OPP's next revision, and it would put S-OP-12's text under a second review;
  - row O alone. That would leave row D's open question, and row E's and §5.2's "before settle", contradicting O.

**LD-11. WS:1393 is qualified, and no golden is added.**
- **Rejected:**
  - a CINV golden now. CINV is a lock input JSON, so a new array entry needs a complete copy, and the M4 CLI unit owns the signal goldens (cross-law item 5);
  - leaving the row. Its "before settle" would then read against §1.

**LD-12. J1 8.3's commit-phase precedence is not restated in WS.** Rules 1 and 2 (J1:539-540) give X7's exit-4 rows, not `interrupted`, for a signal the commit gate latched in phase C. WS:226's before-settle rule still says `interrupted`, and no J1 successor amends it. S18's paragraph refers to "the termination the rule above gives", so it neither restates nor contradicts that. The gap is flagged as cross-law item 1f.
- **Rejected:** carrying it here. It is S-OP-12's (J1's S9 to S11 and S15), not the final output section's.

**LD-13. Binding.** After acceptance, a binding-only product commit appends S18's four pins. No product file is materialized: S18 has no product bytes, and J2a, J3b, J2c and J3d implement it under their own reviews.

## Controls proposed for J2c and J3d

These refine J1's J-C14, J-C14b and J-C14c. J-C14c and S12-O otherwise stand as J1 wrote them.
- **S18-T1 (J-C14's O case, NB-02).** One signal at each of three points:
  - after the output decision point and before S-OP-2's producer cutoff: the event is admitted;
  - between the cutoff and the freeze: `drain-abandoned` in the frozen summary, and the envelope's `diagnostics` shows the loss;
  - after the freeze, which is S12-O's point: post-freeze tally only, and no persisted record.

  In all three, durable and ephemeral, the envelope's kind, termination, class, exit and `runId` are the decided ones. The signal is classified O in memory.
- **S18-T2 (J-C14b, NB-01).** A `CommitUndetermined` whose failure envelope's renderer fails before any byte. Assert the analysis attempt's ExecutionId and namespace disclosure separately from the primary code and detail that WS:233-240's tie rule selects. Assert that there is no `runId`, and that the disclosed ExecutionId is not the render attempt's.
- **S18-T3 (LD-4).** Two cases:
  - a phase-D signal, then a renderer failure of the `interrupted` termination output: F16 with the `runId`;
  - a phase-A interrupt whose termination output fails to render: `DELIVERY.REQUIRED_PROJECTION_FAILED` with no `runId`.

  A signal during the termination output's write is classified O, not after-settle (RF-1), and changes nothing.
- **S18-T4 (LD-8).** A sink that fails its first write with no byte written gives exit 4, the coded line and no replacement envelope.
- **S18-T5 (LD-9).** An O signal before finalization starts leaves the normal-exit drain in force. Use S-OP-2's C-7 stalled-writer hook: abandonment comes at the normal deadline, not the cancellation one.
- **S18-T6 (LD-5), J2a's pure model.** An O signal leaves the invocation model's `cancellation` as the decision point fixed it. A signal after the settlement point is after-settle.

## Cross-law items

1. **J1's next revision:**
   - **a. NB-02.** Replace 8.2's O cell "because O follows SOP2's freeze, that event is post-freeze loss (SOP2:663)" with S18's three-way rule. S12-O stays the post-freeze case. J1:824's forbidden substitute, a required persisted record "after SOP2's freeze", already agrees.
   - **b. NB-01.** Replace "through WS:1409-1411's composition" (J1:535) with the fault owners and WS:1412-1413. J-C14b takes S18-T2's separate assertion.
   - **c. SOP2 citations.** Renew them from r4 to the accepted r6:
     - 205-208 → 226-230;
     - 623 → 652;
     - 623-650 → 652-683;
     - 663 → 704;
     - 815-816 → 871-872.

     Renew the SOP2 short name the same way.
   - **d. Settlement (LD-4, RF-1).** 5.3's "the settlement point is the moment step 1 becomes terminal" should read as WS:227-228 now defines it: every required step terminal and, where the final output section applies, the required output returned. For a cancelled step 1, that is later than its terminality.
   - **e. The phase table's gap.** 8.2's table has no row for a signal observed after `publish` returned `Refused` or `CommitUndetermined` and before the decision point. 8.3's rules 4 and 1 project it, but its `arrival_phase` is not fixed.
     - **Recommendation:** label it by the last phase the operation reached: B for a refused attempt, C for an undetermined evidence `COMMIT`.
   - **f. Commit precedence in WS (LD-12).** WS:224-227 still says a before-settle signal gives `interrupted`, against 8.3's rules 1 and 2. Name a WS successor for it, for example a WS:226 override beside S15.
   - **g. Item 13's S18 row.** Add WSE, the after-settle lines and the copy form.
2. **S-OP-2 and its binding unit O1:**
   - `host.signal.received`'s "CancelPhase: A–E, OPP §5.5" (SOP2:871) should read "A–E and O" at its next record revision, or in O1's registration. `O` itself is an ordinary registration.
   - **(r2, NBO-2.)** SOP2:653's "200 ms after it starts on normal exit, 100 ms on cancellation" should carry row O's qualifier when O1 implements it: "on cancellation" means a decided `interrupted` envelope, so an O signal during a success envelope keeps the normal drain (LD-9).
3. **OPP's next revision (J1's S15).** Start from S18's copy, then:
   - make S-OP-12's rows A to C as J1 8.2 has them;
   - drop the r3:338 note ("Until S-OP-12 is accepted…");
   - close §9's S-OP-12 row (r3:415).
4. **The invocation record (M4 `invocation`-kind envelopes and M4's invocation successor; M5's retained record):**
   - The record keeps the decision point's `cancellation`. Recording an O signal durably needs an INV5 successor.
   - **(r2, NBO-1.)** INV5's `Cancellation.phase` description still defines after-settle as "every required step already reached a terminal outcome". When the invocation-record owner restates it, it takes RF-1's conjunct: "and, where the final output section applies, the required output returned". Until then LD-5 keeps an O signal out of that record, so the stored phase is the decision point's and the description is not exercised by phase O.
5. **CINV.** When the M4 CLI unit wires signals, add a golden for a signal in the final output section, in which the decided class stands.
6. **M3-PLAN (S17).** S18 is drafted, at r2. J2c's and J3d's output wiring and S12-O wait for S18's binding.

## Points for the reviewer (r2)

GROK2 ruled on r1's R1 to R8 (its rulings 1 to 6). For r2:
- **R1. Is RF-1 resolved?**
  - Do WS:227-228 and WSE:229-230 now define *after-settle* by the settlement point, with every required step terminal and, where the final output section applies, the required output returned?
  - Are the four `before`s exact, and does each `after` make only the stated insertion?
  - Does the paragraph's settlement sentence agree?
- **R2. The partition.** Where the section applies, are *before-settle* (WS:225), *final-output* (the paragraph) and *after-settle* (WS:227-228) now disjoint and exhaustive, including for an interrupted invocation? Elsewhere, is every reading unchanged?
- **R3. The observations.** Are NBO-1 and NBO-2 recorded where they belong (cross-law items 4 and 2)?
- **R4. Nothing else changed.** Are the six r1 overrides' `before`s and selectors, their `after`s other than WS:231 and WSE:235, and the plan copy byte-identical to r1? The r1 bytes are in `reviews/codex2-s18-r2/r1-members/`.
- **R5. Selection at the new base.** Is the record well-formed under `verify_design` at `392499e`, after CRC-1, with no selector clash?

## Binding

S18 binds on the `verify_design` at main `392499e`, on top of all 83 contract successors, with no prerequisite. It shares no selector with CRC-1 (bound) or with any unbound record. After `ACCEPT-DESIGN-UNIT`:
1. copy the review to `docs/implementation/m3/reviews/codex2-s18-r2/review.json`;
2. complete `s18-unit.json`;
3. append the four pins to the product lock in a binding-only commit;
4. run plain `verify_design`.

If main has moved by then, rerun `evidence/verify_scratch.py` on the new main first. J2c's and J3d's output wiring, and S12-O's transcription, may then proceed under their other gates.

## Evidence runs

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, read only. Nothing ran cargo, a test, a generator or a product tool other than `verify_design` in the scratch harness, design-only.
- **`evidence/build_s18.py`**, twice. The second run's `--check` reported identical bytes.
- **`evidence/check_s18.py --rev 392499e`**: 133 checks pass. These include the four after-settle insertions and the parenthetical read across its two lines, on both parents.
- **`evidence/verify_scratch.py --rev 392499e`**: 83 to 84, passes. It shows ten overrides, no supersession, the selected inventory (`v134`) and the inheritance (55) unchanged, and the conflicting-override probe refused.

## Not claimed

- No product code, test or build was run, and no product file is changed.
- `verify_design` ran only design-only, in the scratch harness, on synthetic review and assent bytes.
- No M4 renderer timing, and no elapsed bound on a blocked output in phase O (OPP r3:339).
- INV5, ENV7, CINV, S-OP-2 and the live `PLAN.md` are not edited.
- No crash-matrix row is transcribed here: S12-O is S12's, after S18's acceptance.
