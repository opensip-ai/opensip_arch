Grok review: two law prerequisites of code unit J3b. They are **X5 r4**, J1's successor S8, and **X9 r17 round 2**: §S12, J1's successor S12, together with X4 r8's record note for X9 r17. Claude Opus 5.5 leads. Verdicts wanted: one for X5 r4 and one for X9 r17 round 2, each **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok-x5-r4-x9-r17-s12.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- **No run of any kind.** No product build, test, census-only step or lead set. This is a law review, and J3b's code does not exist yet. A timing-sensitive crash-matrix set may be using this machine.
- Run git read-only. Read the product at `1799d3d` with `git show 1799d3d:<path>`. Main has since moved to `0765f8c` by two binding commits, ENUM-1 and SD-8. Both change only `design-lock.json`, so every product file cited here is unchanged.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read the private 413 UUID fixture.
- You may write read-only scratch scripts under your review directory, for example to tabulate the host required runs at `1799d3d`.

## Subjects and pins

The pins are in `hashes.txt`. Both subjects are uncommitted in arch until they are accepted. If a subject's sha256 differs from `hashes.txt` when you read it, stop and report. Do not review other bytes.

- **Subject 1, X5 r4:** `docs/implementation/m2/replay-join-x5/PROPOSAL.md`. Diff it against `replay-join-x5/PROPOSAL-r3.md`, the r3 bytes Grok accepted (`d9a101b8…`, 22,501 bytes; `reviews/grok-replay-join-x5-r3`). The live r3 file carried the acceptance stamp "r3 ACCEPTED by Grok on 2026-10-03." at the end of its r3 paragraph. r4 keeps it.
- **Subject 2, X9 r17 round 2:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`. Diff it against `crash-matrix-x9/PROPOSAL-r17-RC.md`, round 1's accepted bytes (`89fc47ff…`, 235,499 bytes; `reviews/grok-crash-matrix-x9-r17-rc`). Round 1's acceptance note after line 1 is round 1's own and stays.
- **The owning law:** J1 r6, accepted by Codex (`m3/host-pipeline-j/PROPOSAL-r6.md`, `086e804a…`; `m3/reviews/codex-host-pipeline-j-r6`):
  - item 7, X5 r4's text (J1r6:505-539, with :517-519);
  - item 8, the phases and precedence (J1r6:543-669);
  - item 12, the rows and the host drivers (J1r6:849-871);
  - item 13's S8 and S12 rows (J1r6:885, :889), and item 14's J3b and J3d rows (J1r6:913-914).
- **The laws that fix the outcomes, all accepted:** X3d r9 (`commit-session-x3d/PROPOSAL-r9.md`, S10.2 to S10.9), X4 r8 (`live-guards-x4/PROPOSAL-r8.md`, S11.2 to S11.12), X7 r7 (`finalization-x7/PROPOSAL-r7.md`, S9.1 to S9.9), X3b r11 (`journal-x3b/PROPOSAL-r11.md`, items 3 and 4), and S18 and S21 (`m3/host-pipeline-j/s18/README.md`, `s21/README.md`).
- **X9's own citations:** X9:n is `PROPOSAL-r16.md`, as round 1 fixed. Round 2's new short names are listed in its header paragraph.
- **The evidence at C = `3d2d5b5`:** `crash-matrix-x9/evidence/3d2d5b5…/host/matrix.json` and `storage/matrix.json`.
- **The product:** main `1799d3d`. The key files are host's runner (`crates/host/src/crash_matrix_support.rs`), host's matrix harness (`crates/host/tests/commit_matrix_tests.rs`), both `required-runs.v1.json` files, `crates/host/src/finalization.rs`, `crates/security/src/custody/commit_session.rs` (`refused`, `refuse`, `finish`), `crates/platform/src/crash_barrier.rs` and `crash_barrier/driver.rs`, and `tools/check_crash_matrix.py`.

## What X5 r4 changes

Against r3, and only what S8 assigns, "item 3's order (item 7)" (J1r6:885):
- **The title, a header paragraph and an "r4 changes" table.**
- **Item 3.** "Replay before any custody" becomes replay after evaluation and before `prepare_commit`, inside host finalization. A replay refusal ends the attempt before any attempt row, object or journal effect. The session ends through `refused()` and `finish`, exactly once, with nothing appended, and `finish` releases the lease. This is J1r6:517 word for word, with its basis (J1r6:508-516; IE:1657-1658; X3D9:550-554; X7r7:312-326).
- **Item 3's rejected alternative,** "replaying under the project lease", is withdrawn (J1r6:518). r3's own order is rejected in its place.
- **Item 4.** Its decision stands (J1r6:519). Its reason "it runs before that ledger's operation begins" is withdrawn, because it is no longer true. The other reason stays, and X7's "finalization charges nothing" is cited (X7r7:331).
- **Item 7.** F01's sentence, "because the invocation ends before any effect", is restated for the new order.
- **Item 9.** One note: r4 adds no unit and changes no X5a file. J3b moves the one call site (J1r6:913).
- **Forbidden substitutes.** "replay under a held fence or lease" loses "or lease". One substitute is added: a replay refusal that ends the session other than through `refused()` and then `finish`, exactly once.

## What X9 r17 round 2 changes

Against round 1:
- **A round-2 paragraph** in the r17 header. It lists the changes, the new citations and the snapshot name, `PROPOSAL-r17-S12.md`. It carries **X4 r8's record note** (X4r8:762-765).
- **The frame table's §S12 status cell.**
- **Six in-place notes:** one "r17 round 2" note on G4's `x4.gate.latch.after`, and five "r17 (§S12)" notes on the old host order (r5's matrix-only order; r10's runner; r10's `finalize` child and its rejected alternative; r13's F01 decision).
- **One forbidden substitute,** on the signal step.
- **§S12, filled in place.** It has S12.1 to S12.7 and lead decisions LD-S12-1 to LD-S12-8.

§RC and §RW are unchanged, and so is every row of both required-runs files.

## What §S12 decides

- **The re-transcribed host driver (S12.3).** The runner `finalize_commit` reads the candidate file, makes its one entry, opens the session through finalization's opening entry, then calls `finalize` with the open session. `finalize` replays after `open`. The port is host's own cancellation source, and the SOP2 hook does nothing.
- **The existing host rows (S12.4; LD-S12-8).** None of host's 98 rows changes an expected value. The table checks each group. For F01's replay-refused variants, §S12 answers J-C13 (J1r6:539):
  - no reserve, so nothing is appended;
  - no attempt row or ledger;
  - the floor step and the end step write only when the copy tail is higher;
  - so the whole post state is unchanged.

  F53, which J1's list omits, uses the same runner and is unchanged too. The unscored changes are F01's two traces and their `notApplicable`.
- **The rows (S12.5):**

  | Row | Case | Variant | Unit | Outcome |
  |---|---|---|---|---|
  | S12-B | F38 | `signal-after-staging` | J3b | `interrupted:130`, no runId; `SEAL,REV,CLN` added; `REV` reason `operator`; R1 UAO, R2 `authoritative:0`, R3 refused, R4 TNC |
  | S12-C | F39 | `signal-after-admission-delivery` | J3b | F39's row with the runId; `SEAL,REV` added; `REV` reason `operator`; R1 `committed-historically:*`, R2 `authoritative:0` (distinct), R3 committed, R4 CH |
  | S12-U | F40 | `signal-fail-after-evidence-commit` | J3b | the durability row, no runId, never `interrupted`; `SEAL` only; the landed ladder |
  | S12-D | F15 | `signal-x3d-finish-end-step-after-1` | J3b | `interrupted:130` with the runId; no latch; `x7.delivery.required` reached with zero bytes; `SEAL` only; the committed ladder |
  | S12-O | F16 | `signal-before-required-delivery` | J3d | `authoritative:0`, 19 bytes delivered, the signal labelled O; `SEAL` only; the committed ladder |

- **The lead decisions:**
  - **LD-S12-1:** all five rows are host rows.
  - **LD-S12-2:** each row's case is its hold point's F-case.
  - **LD-S12-3:** variants are `signal-` and then the existing row's spelling without its action word.
  - **LD-S12-4:** the signal step. `then: "signal-resume"`, a `signal SIGINT` control line, delivery on the signal input's own thread, and a `signalled` acknowledgement record that names no point. Rejected: `kill(2)`, delivery on the held thread, and a crash point.
  - **LD-S12-5:** the fixed delivery phase renders only the success envelope's bytes.
  - **LD-S12-6:** the port is host's own source, and the hook does nothing, so S12-O tests deferral and the O label, not SOP2's freeze.
  - **LD-S12-7:** new observed values. These are `interrupted:<exit>`, `signal`, an interrupted `runId`, `arrivalPhases` and `revReasons`.
  - **LD-S12-8:** no existing row is re-transcribed.
- **The duties (S12.6, S12.7).** There is no census part and no new crash point. The prediction is that both censuses stay unchanged: host 218 points, kill set 271. J3b's census-only step, transcription, development runs and lead set (host 102 rows). J3d integrates S12-O (host 103 rows). What each unit adds to the harness, the crash barrier and the checker.

## Decide

**X5 r4:**
1. Is item 3's new text J1r6:517 exactly, and is each other edit one that the new order requires? Does r4 change anything S8 does not assign?
2. Do items 1, 2, 5 to 5f, 6 and 8 stand unchanged, with every row, detail, remedy and X5a file?
3. Is the new order consistent with X7r7:312-331, X3D9:550-554 and IE:1657-1658? Check in particular "no reserve, so nothing is appended" and "the end step only on an open attempt ledger" against `commit_session.rs` (`refused`, `refuse`, `finish`).
4. Is item 4's withdrawn reason rightly withdrawn, and does the decision still hold?
5. Is the added forbidden substitute within S8?

**X9 r17 round 2:**
1. **Scope.** Does round 2 change only the places its header lists? Are §RC and §RW byte-identical to round 1? Does any expected value of either file change?
2. **The driver (S12.3).** Is the runner the composition that X5 r4, X7 r7 S9.1 and S9.2, and LD7-1 require? Is its entry-refusal report a copy of today's value? Does it keep X9 r10's runner rules (X9:194-203)?
3. **The existing rows (S12.4).** Does each of host's 98 rows keep its expected value? Check closely:
   - F01's replay-refused variants (J-C13): X3D9 S10.6, `finish`'s owed records against the reserve, X3B11 items 3 and 4, and the `candidate` child's `REV` (X9:325-330);
   - F16 `fail-before-required-delivery` under LD-S12-5;
   - F32's rollover rows;
   - F53, which J1 omits.
4. **The lead decisions.** Are LD-S12-1 to LD-S12-8 sound and consistent with X9's conventions and RC.2? Look hardest at:
   - LD-S12-4: the mechanism, its determinism without a sleep, and its fit with item 3's hold rule (X9:887);
   - LD-S12-5: zero bytes for every non-success envelope;
   - LD-S12-6: the hook, and what S12-O does and does not test.
5. **The rows (S12.5).** Does each expected value follow from the clause cited beside it, with nothing read back from a run? Check against J1 8.2 and 8.3, X7r7:348-361 and :468-478, X3d r9's `REV(operator)` and `finish`'s CLN rule. Are the spellings host's (`outcome_head`, `fields`, `meets`)? Are the scripts executable with S12.7's additions? Do the cases and variants pass the checker's grammar?
6. **Census and lead sets (S12.6).** Is the census prediction right? Check that replay reaches no point, that host's only points are `x7.delivery`'s, and that the census skips a record whose point is `-`. Is J3d the right integrator for S12-O?
7. **X4 r8's record note.** Is the new placement stated as X4r8:395-397, :515 and :764 fix it? Is it right that no census or expected value changes? Is the list of rows that await or kill `x4.gate.latch.after`, or score `gateLatched`, complete? Is the check (X4-F3's lead set and W-7) adequate?
8. **Outcomes.** Does round 2 change any accepted outcome of another law?

**Not in scope.** J1, X3d r9, X4 r8, X7 r7, X3b r11, S18 and S21, which are accepted. §RC, which is accepted. §RW, which stays reserved. Any product code.

## Output

Write `REVIEW.md`, and two verdict files: `x5/review.json` and `x9/review.json`. Each review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"noAcceptedOutcomeChanged"`;
- `"subjectSha256"`: the subject's sha256;
- `"subject"`: path, bytes and sha256;
- `"preservedSnapshot"`: `PROPOSAL-r3.md` for X5, `PROPOSAL-r17-RC.md` for X9;
- `"scope"`: `"X5 r4 (J1 S8)"` or `"X9 r17 round 2: §S12 and X4 r8's record note"`.

These are law reviews, not unit reviews. J3b, with its transcription of §S12, gets its own review. Do not commit.
