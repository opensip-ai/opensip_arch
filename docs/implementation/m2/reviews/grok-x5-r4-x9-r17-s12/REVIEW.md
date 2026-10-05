# GROK2 review: X5 r4 and X9 r17 round 2

Reviewer GROK2. Two law reviews, no product run. Product was read at `1799d3d` (`git show`). `~/Library/Application Support/OpenSIP` was absent. Both subject hashes match `hashes.txt`.

| Law | Verdict | Subject |
|---|---|---|
| X5 r4 (J1 S8) | ACCEPT | `docs/implementation/m2/replay-join-x5/PROPOSAL.md`, 28966 bytes, `2734f74b629a0fc27d80e90c38d07a901e21ac625e830b7715897c3151f88b71` |
| X9 r17 round 2 | ACCEPT | `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`, 278697 bytes, `6b208ccf7d1b0ce5c18ec0329724fbc103de8b18d9abae0b02a6ac0856f397f3` |

Diff bases: X5 `PROPOSAL-r3.md` (22501 bytes, `d9a101b8…`); X9 `PROPOSAL-r17-RC.md` (235499 bytes, `89fc47ff…`). Verdict files: `x5/review.json` and `x9/review.json`.

## X5 r4 — ACCEPT

The diff against the unstamped r3 bytes is the r4 header (the r3 acceptance stamp stays on the r3 paragraph), the changes table, item 3, the withdrawn half of item 4's reason, item 7's F01 sentence, item 9's one-line note, and the two forbidden-substitute edits. Items 1, 2, 5, 5a to 5f, 6 and 8 stand, with every refusal row, detail, remedy and X5a file. `fact_admission.rs` is untouched. r4 adds no public code.

Item 3's order sentence is J1r6:517: replay after evaluation and before `prepare_commit`, and a refusal ends before any attempt row, object or journal effect. The ending through `CommitSession::refused()` and `finish`, exactly once, is J1r6:515 and J-C12 (J1r6:538). `prepare_commit` never runs, so step 0 takes no reserve. `finish` owes a `REV` when the gate is latched and appends only when a reserve is held (`commit_session.rs:1114-1125`); with no reserve it forfeits (`:1174-1175`). The end step runs only on an open attempt ledger, as X3D9:550-554 states. The handoff's fence release and the lease through evaluation are J1's R11 and IE:1657-1658. X7r7:312-326 is the same order, and the refusal is projected on X5 item 5 (X7r7:323-324).

Item 4's decision stands (J1r6:519). The reason "it runs before that ledger's operation begins" is withdrawn because replay now runs inside the open session. The remaining reason is that replay performs no native observation. X7's item 7 stands: finalization charges nothing (X7r7:331).

The forbidden-substitute edit drops "or lease", because the new order holds the lease, and adds the substitute that a replay refusal end other than through `refused()` and then `finish`, exactly once. Both edits are what S8 assigns (J1r6:518, :538, :885). r4 names no new unit. J3b moves the one call site (J1r6:913).

No accepted outcome of another law changes.

## X9 r17 round 2 — ACCEPT

### Scope

The diff against round 1's accepted bytes is round 1's acceptance note, the G4 placement note, five "r17 (§S12)" notes on the host order, the round-2 header, one forbidden substitute on the signal step, the frame table's §S12 status cell, and §S12 filled in place. §RC and §RW are outside that diff. Both required-runs files are the pinned product files: host 98 rows (`80e4a02e…`), storage 381 rows (`14a275ad…`). Round 2 edits neither file, and §S12.4 changes none of their expected values.

### Driver (S12.3)

The re-transcribed `finalize_commit` reads the candidate, makes one entry, opens the session, then calls `finalize`, which replays after `open` and before `prepare_commit`. That is the composition X5 r4, X7r7 S9.1 and LD7-1 require (X7r7:312-322; J1r6:517). An unreadable candidate is the host I/O row with no `operation` entry (`crash_matrix_support.rs:304-318`; `run_once` is the process flag at `:47-49`). An entry refusal is reported as today's admit refusal: the row, no runId (`finalization.rs:418-421`). The runner rules at X9:194-203 stay: pinned support module, on-disk inputs, one entry per process, value reports, no second coordinator. The `candidate` child and its one `REV` stay (X9:325-330).

### Existing host rows (S12.4)

The 98 rows are 4 of F01, 5 of F12 and F40, 1 of F39, 6 of F16 and F17, 76 of F32 and 6 of F53. Each scored spelling in the table is the spelling in host's file.

F01's two replay-refused rows keep `stateUnchanged` true, an empty `carrierAdded`, `ledgerPresent` false and `attemptRows` 0. `open` draws an ExecutionId and sets no end-path reserve. `refused()` latches and leaves `Seal::Absent`. `finish` forfeits. The attempt charge is the in-memory work ledger, and capture hashes files (`post_state.rs` walk). The lease files are empty and only locked (X2 r10 :380, :416). The `candidate` child's `REV` is already in the capture taken before `finalize`, which is why that child's reserve (the explicit `reserve_end_path` before `refused().finish()`) advances the tail while this child's floor steps see a tail that is not higher (X3b r11 :95, :123). The new trace points and the loss of `notApplicable: "no-execution-id"` are the unscored changes §S12 names. F01 runs no ladder (`NO_LADDER` at `commit_matrix_tests.rs:64`).

The substituted F01 rows keep the invariant row and `carrierAdded` `REV`. Replay reaches no crash point, so moving it between `open` and `prepare_commit` leaves the point order of those calls as X9:331-336 records it. F12, F39, F40, F16, F17, F32 and F53 keep the values in their rows. F16 `fail-before-required-delivery` keeps `delivered` `0` because the failure envelope writes zero bytes (LD-S12-5) while `x7.delivery.required` still wraps the success envelope (X7r7:470). F17 keeps `delivered` `19`. F53's `finalize` children use the same runner; J1's list omits F53 and the row values are unchanged.

### Lead decisions

LD-S12-1 through LD-S12-3 put all five rows on the host file, under the F-case of the hold, with variants `signal-` plus the existing row's spelling minus its action word. The five `(case, variant)` pairs are new in host's file. The checker grammar `F[0-5][0-9]` (`check_crash_matrix.py:257`) admits F15, F16, F38, F39 and F40, and the variant pattern admits each new name. Labels stay inside the checker's set and include `synthetic` and `scripted-clock`.

LD-S12-4's step awaits `held`, writes `signal SIGINT` on item 3's control channel (X9:884), awaits `signalled`, then resumes. No step sleeps. The held thread reads the control line and runs no product code (X9:887); delivery is on the signal input's thread. The record `X9|<pid>|<thread>|<n>|-|signalled|SIGINT` is the driver's field order (`driver.rs:58-68`, trace at `:510-511`). `Census::from_exit` skips `point != "-"` (`:544`). S12.7 item 3 is the addition that admits event `signalled` with point `-`; today's `EVENTS` list and the `-` allowance (`outcome` and `harness-error` only) are what that item extends. Rejecting `kill(2)`, delivery on the held thread, and a crash-point acknowledgement matches J1, X4r8 LD8-4 and the hold rule.

LD-S12-5 renders 19 bytes `{"x9":"delivered"}\n` for the success envelope and zero bytes for every other envelope. The harness already spells optional success `ok` and failure `failed` (`commit_matrix_tests.rs:340-344`). COMMON4 `D9Signal` is `SIGINT`, `SIGTERM`, `SIGHUP`.

LD-S12-6 passes host's own cancellation source and a hook that does nothing. S12-O therefore tests the deferral and the label O. SOP2's cutoff, freeze and post-freeze tally stay on S18-T1 (S18:221-226).

LD-S12-7's `interrupted:<exit>` is what `outcome_head` will read from `kind=interrupted` (S12.7 item 4; today's head is at `:850-857`). `revReasons` is read beside `carrierAdded` (`:1586-1598`) and is the empty string when the scripted phase adds no `REV`. No existing host expected key is that field. `operator` is the `REV` reason X3D9:537-542 and J1r6:570 add for `StopCause::Operator`.

LD-S12-8 re-transcribes no existing row. J1r6:863 asks for a re-transcription when an expectation changes. S12.4 shows none does.

### Rows (S12.5)

Each expected value follows the cited clause, in host's spellings (`outcome_head`, `fields`, `meets` with `:*`).

| Row | Outcome shape | Host spelling it follows |
|---|---|---|
| S12-B F38 | Rule 4, phase B: `interrupted:130`, no runId, `SEAL,REV,CLN`, `REV` reason `operator`, R1 `unknown-attempt-open`, R4 `terminal-not-committed` | J1r6:585 and :621; X7r7:355; `finish` owes `REV` and `CLN` for a SEAL without evidence (`commit_session.rs:1114-1120`); storage F38's R1/R3/R4 and host F12's not-landed row. R2 is `authoritative:0` because no revocation stands, so the candidate is a first commit (X9:265, :1129) |
| S12-C F39 | Rule 2: F39's row, runId `yes`, remedy `renderer-failed-after-commit`, `SEAL,REV`, R1 `committed-historically:*` | Host F39's expected object; X7r7:353; J1r6:586 and :619. R2 `authoritative:0` is the no-revocation branch of X9:364-366; the script's `r2: distinct` is X9:356 |
| S12-U F40 | Rule 1: durability row, subject `executionId`, remedy `commit-undetermined`, runId `no`, `SEAL` only, empty `revReasons` | Host F40's latch row, including R1 `committed-historically:pendingSettlement`. The undetermined outcome forfeits the reserve (J1r6:586) |
| S12-D F15 | Rule 3, phase D: `interrupted:130`, runId `claimed`, `gateLatched` false, `deliveryPhase` `started`, `delivered` `0`, `SEAL` only | J1r6:587 includes `finish`, so a hold at `x3d.finish.end-step.after#1` is inside D. The window is closed (X4r8:662-668). LD7-4 renders that envelope inside `x7.delivery.required` and LD-S12-5 writes zero bytes. The ladder is X9:713's W7 host spelling |
| S12-O F16 | The success envelope stands: `authoritative:0`, `delivered` `19`, optional `ok`, arrival `O` | X7r7:377 and :471; J1r6:588 and :870. The same W7 ladder |

`gateLatched` is already the trace test `x4.gate.latch.after` (`commit_matrix_tests.rs:1402-1406`). S12.7 item 5 admits `unit` `J3b` and `J3d` in `required_all` for every case, which is what keeps F15 and F38, and item 6 admits those two units in `UNIT_VALUES` the way r16 admits `X9-6`. `check-unit` admits neither. With those additions the scripts are executable. The canonical key order of each script object matches the file's sorted keys.

### Census and lead sets (S12.6)

§S12 adds no crash point. The evaluator and identity crates hold none. Host's only points are `x7.delivery.required` and `x7.delivery.optional` (`finalization.rs:287`, `:297`). Moving replay after `open` therefore adds no census name, and the D projection leaves the delivery point with no point of its own (X7r7:472). Host stays at 218 points and a 271-point kill set. Storage is unchanged by J3b: 259/321 at C, or RC.3's 261/327 once X3c-3 has integrated. J3b's lead set is host's 102 rows. J3d integrates S12-O (J1r6:914; X7r7:428-434; M3P:319) and the file then holds 103.

### X4 r8's record note

The note places `x4.gate.latch.after` after the stop transition's release (X4r8:395-397), on the same calls and in the same thread order (X4r8:515), which is the record S11.12 asks X9 to carry (X4r8:762-765). The critical section holds no I/O, wait, callback or crash point (X4r8:401). Existing-source count and order stay (W-7, X4r8:548-550). The cancellation latch fires only after a successful exchange (X4r8:397; LD8-4), so S12-D, S12-O and the LD-r5-1 span gain no latch point.

Every required-runs row that awaits or kills `x4.gate.latch.after`, or scores `gateLatched`, is in the note's list:

- storage awaits `#1` then resumes (`then: pass`): F14 `kill-x3d-finish-settle-before-1-after-latch`, F38 `revoked-after-staging`, F39 `latch-after-admission`, F40 `fail-after-evidence-commit-latched`, F41 `latch-before-admission` and `admission-before-latch`, and the single F44 and F45 rows;
- storage kills there: F19 `kill-x4-gate-latch-after-1-after-revoke`;
- host awaits it inside `revoke-latch-resume` and scores `gateLatched`: F39 `latched-after-admission-delivery` and F40 `latched-fail-after-evidence-commit`.

No expected value in either file names a `REV` reason. X4 r8's `CertainRefusal` keeps `operation-stopped` (X4r8:473, :513 pointing at S11.6, :698). The check is X4-F3's serialized lead sets and W-7 (X4r8:606, :765). A moved transcribed value is re-transcribed in a new round before that review.

### Outcomes

Round 2 spells J1's, X3d r9's, X4 r8's, X5 r4's, X7 r7's, S18's and S21's expectations. It changes none of those laws' accepted outcomes. `noAcceptedOutcomeChanged` is true.

One non-blocking observation is in `x9/review.json`: S12.7's arrival-phase parenthetical attaches `O` to SOP2:871, whose CancelPhase note is A–E. The row letters themselves follow J1.
