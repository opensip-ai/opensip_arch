# Law X7 r7 — ACCEPT

GROK2 reviewed X7 r7, J1 r5's successor S9: the host half of the commit-phase cancellation join. The directory name stays `codex2-x7-r7`. Verdict: **ACCEPT**. No required findings. One non-blocking observation.

Subject `docs/implementation/m2/finalization-x7/PROPOSAL.md` is 59578 bytes, sha256 `7757935cdafa3a09a59723597cd23bd185ea45e6a47b5e47e9e5b70b91bc22dc`. Preserved snapshot `PROPOSAL-r6.md` is 28729 bytes, sha256 `9e17faf2811c53dd3db917f3924c2a5b84a2313d3e3d66a6ffe0e722e3deac03`. All 14 pins in `hashes.txt` match. Product main is `d2c00a96c3136fe45b901bc067b6d0ca51f0c9c1`; `git diff cca4fe4 HEAD` is empty for every cited file. `~/Library/Application Support/OpenSIP` is absent. No cargo.

`noAcceptedOutcomeChanged` is true. The order change, the interrupted envelope, the step-1 split, the coded `Interrupted` arm, and the movement of the D projection out of `x7.delivery.required` are S9's declared changes. Apart from those, every accepted r6 outcome and every other law's outcome stays.

## Faithfulness

S9 carries J1 8.6's X7 list and the S9 row (J1:660-665, J1:855): items 1, 3, 4 and 8, each cited, plus the four forbidden substitutes. The r7 changes table (PROPOSAL.md:103-115) and S9.1 to S9.6 follow that list.

It is read with the bound successors. S18 is bound at product `5214350`, so phase O's deferral, the failure envelope before any byte, the exit-4 write failure, and the one coded standard-error line are in force (J1:558-560, J1:632-640; `bootstrap.rs:42-47` and `:55-60`). S21 is bound at product `3f6f9a5`. Its WS:226 after-text keeps `interrupted` (130) except for two commit outcomes: an undetermined commit (`DURABILITY.COMMIT_FAILED`, ExecutionId, no runId) and a commit latched after admission (`DELIVERY.REQUIRED_FAILED`, with its runId). S9.3 therefore runs rules 1 and 2 for a signal now (J1:606-616).

Nothing in S9 decides X3d r9's token, window, sample, or the operator-stop row. S9.1 takes `take_cancellation_latch` and S10.2's single use as given. S9.2 reads `admitted_at_close()` (S10.3). S9.5 projects `InstallationTermination::Interrupted { signal }` (S10.5). S9.9 states that X3d r9 needs no change. Nothing decides X4 r8's gate word. The port reaches the gate only through X3d r9's token (S9.9; forbidden-substitute group at PROPOSAL.md:514-520). Grok's X3d r9 review assigns J1:914's projection clauses to this law, and r7 carries those clauses.

## Projection (S9.3)

The table is J1 8.3's. The returned outcome is matched first. The gate's state is never the selector (J1:588-598; forbidden substitute at J1:914).

| Returned outcome | Signal before the decision point | J1 row |
|---|---|---|
| `CommitUndetermined` | durability row, ExecutionId, namespace, no runId (rule 1) | 38 |
| latched `Committed` | F39, runId, no delivery phase (rule 2) | 42 |
| unlatched `Committed` | `interrupted` 130, kind run, `run.authority` authoritative, runId (rule 3) | 47 |
| `Refused(Interrupted { signal })` and every other pre-D end | `interrupted` 130, kind failure, `errors: []`, no runId (rule 4) | 46 |

The operator stop is the A/B envelope: class `interrupted`, exit 130, no error code, no runId (J1:555, row 46; X3D9 S10.5). The no-signal cell on that row is empty because only a signal produces the row (S9.2). Rows 43, 44 and 48 stay with S9.4: a renderer failure in O, and a signal in O or E.

S9.3's last bullet is J1's and S21's reading. Rule 4's empty-errors branch admits no other member (J1:598; ENV7:704-723, :790). An `ExistingAttempt`'s ExecutionId and binding, and the busy row's namespace, therefore stay in the operational record (SOP2:872) when a signal was observed. S21's two exceptions are only the undetermined commit and the latched-after-admission commit. M3-L r5 items 16e, 16f and 18 require the A/B signal to be `interrupted` 130 with no runId, and they leave the join to this successor. They do not require those disclosures inside the interrupted envelope.

## Step 1 and phase O (S9.4)

`DeliveryPhase::render` (`finalization.rs:256-262`) is the split J1:663 names. Today that method both projects and renders the committed Run, and `required` (`finalization.rs:310-318`) runs it inside `x7.delivery.required`. r7 splits it into a cancellable D projection, built in memory from `&PublishedCommit` and the evaluation result, and O's rendering of the envelope the decision point has already chosen.

Item 4's sentence "a failed or latched attempt never opens a delivery phase" stays, and S9.4 keeps it for the Run's own delivery: the D projection runs only for an unlatched `Committed`, after `finish`. Every decided envelope, a termination included, is still rendered and written in O. That is J1 5.2's required output of a terminal step 1, and J1 5.3's rule that a cancelled step 1 still renders its termination in the final output section.

O's failure routes are J1 8.2 row O's and S18's. A renderer failure before any byte takes item 3's F16 row, keeping the runId, when a `PublishedCommit` exists (row 43), and WS:1377's row 44 (`DELIVERY.REQUIRED_PROJECTION_FAILED`, no runId) otherwise. An uncertain step 0 keeps its ExecutionId and namespace (J-C14b). A write failure after the first byte is exit 4 with no replacement (`bootstrap.rs:55-60`; `deliver_required` at `delivery.rs:17-21` settles only after write and flush). An unrenderable failure envelope is exit 4 and the one coded standard-error line (`bootstrap.rs:42-47`). Settlement is the return of that required output. Optional effects follow only a success envelope.

## LD7-1

Keeping every facade call in `finalization.rs`, through two entries the pipeline calls, is the reading that satisfies both sides. J1 item 7 has the pipeline open the session at R12 (J1:492) and end every pre-commit path through `refused()` then `finish` (J1:486-487). X7 item 1 and X5 item 6 give the commit facade one host caller. The opening entry calls `CommitSession::open` and takes the token. The ending entry calls `refused()` and `finish` once, then runs step 1. `finalize` takes the open session and the candidate and no `admit` closure (J1:484-486).

The product already shows that `open`'s refusal can be finished. `CommitSession::open` returns `Err((SessionRefusal, StoppedSession))` (`commit_session.rs:322-324`, and `refused` at `:572-587` always builds the stopped session). Current `finalize` already calls `stopped.finish()` on that arm (`finalization.rs:422-427`). The opening entry does the same and then runs step 1. Moving `open` into `finalize` would put the ExecutionId after provider spawn (J1:479-480). Letting the pipeline call `open`, `refused()` and `finish` itself would give "exactly once" two owners. The host production tree names `CommitSession::open`, `prepare_commit`, `.publish()` and `.finish()` only in `finalization.rs`; T7-1 extends that pin to `take_cancellation_latch`, `refused` and `undetermined`.

## LD7-2

Handing the token over only at `Ok(PreparedCommit)` loses no signal J1 requires to latch at once.

Phase A does not use the latch (J1:555). A signal after replay and before `prepare_commit` is P2: `refused()` then `finish`, and the token is dropped unused. A signal during `prepare_commit` that then returns the admitted attempt is handled as B (J1:555). P3 hands the token over before `publish`, and the port latches at once, so `publish`'s first checkpoint sees it (J-C15b, J1:691). The checkpoints that refuse in B are publish steps 3.2, 3.7 and 3.9 (J1:556; X3D9 S10.2), which all run after that handoff. `prepare_commit`'s error returns keep row A's reading (J1:567, Scope), so those paths drop the token and never owe a P3.

The window opens inside `prepare_commit`, after step 4's attempt-row `COMMIT` and before step 6 (X3D9 LD9-1), and `Ok(PreparedCommit)` does not close it. A call outside the window returns `OutsideWindow` and consumes the single use (X3D9 S10.2). Handing the token out at R12 would spend it on a phase-A latch. Handing it out from inside `prepare_commit` would put a callback in the storage facade. Latching only at the main thread's points during `publish` would miss C's 1→3 sample, because `publish` has no such point. Reading the gate after `publish` in place of `admitted_at_close()` would let an observer latch after the close (X3D9 LD9-3) and would select from the gate's state (J1:914).

P1 through P6 are the reports finalization must own: take the token, ask before `prepare_commit`, hand it over at the `Ok` return, pass the close sample and whether the return enters D, ask once at the decision point, and mark E when the required output returns. The watcher, the phase labels, the SOP2 `host.signal.received` records, and the second stage stay with J3b and J3d (S9.2's last bullet; Not claimed). `refused()` and `undetermined()` are the session methods at `commit_session.rs:529-545`.

## LD7-3

An explicit invariant arm is the right form for a row only finalization can meet. `InstallationTerminationV1` requires `error_code` (`installation_termination.rs:21-28`), and the interrupted form has none (J1:542; X3D9 S10.5). Finalization's envelope therefore gains `Interrupted { signal, run: Option<AuthoritativeRun> }` beside `Authoritative` and `Terminated`. `run` is `Some` only in phase D, and only `authoritative_run(&PublishedCommit)` builds it (item 2, DR-G27).

`installation_termination` (`:60`) gains an explicit `Interrupted` arm that returns the existing invariant row (`SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, `HOST.INVARIANT_VIOLATED`). The match stays exhaustive, with no wildcard and no panic. Finalization matches `Refused(Interrupted { signal })` first. Only a `CommitSession` operation mints a token, and only finalization calls the session, so only finalization can meet the row. The five production callers of `installation_termination` are `maintenance.rs`, `crash_matrix_support.rs`, `doctor_report.rs`, `recovery_route.rs` and `finalization.rs`. Their existing rows are unchanged. An error code on `interrupted`, an optional `error_code`, or a new return type for all five callers would change rows this law does not own.

## LD7-4 and LD7-5

The `x7` points keep the census reach X9 kills, and `x7.delivery.required` moves to the place S12-O names.

Today `deliver` (`finalization.rs:283-308`) enters `x7.delivery.required` only for an unlatched `Committed`, and `x7.delivery.optional` only after that required step returns an exit of 0, 1 or 3. A latched commit returns `NotStarted` and enters neither point. J1 places S12-O's hold at `x7.delivery.required.before`, inside O, after the decision point and SOP2's finalization (J1:839), and adds no crash point (J1:840).

LD7-4 puts `x7.delivery.required` around O's rendering and output of the decided envelope on two runs: an unlatched `Committed` whose envelope is the success envelope, and phase D's interrupted envelope. Those are the unlatched-commit executions that enter the point today, the second one now carrying the signal-in-D envelope. `x7.delivery.optional` still follows only a success envelope's output. The D projection moves out of the point, before the decision point, so the S12-O hold is inside O. Every other envelope renders under no `x7` point, so refusal runs gain no census hit.

An in-process `RendererFailed` currently enters the barrier only because `render` sits inside it (`finalization.rs:313-314`). After the split, that failure is the D projection, outside the point. LD7-4 names this as the F16 and F17 host-driver move and assigns the re-transcription to X9 r17 before J3b's review (J1 item 12; S9.9). T7-7 checks the set LD7-4 names, with `x7.delivery.required` after P5 and SOP2's hook. That is S9's declared census change, carried by X9 r17, and it is why `noAcceptedOutcomeChanged` stays true.

LD7-5 fills the gap J1:558 leaves. J1 says a signal in D discards the projection. It does not say what a failed projection does when no signal was observed. With no signal, the failure is step 1's required failure before any byte, and the decision point decides item 3's F16 row, which keeps the runId (row 43, detail `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`). With a signal in D, the failed projection is discarded as a successful one would be, and the envelope is rule 3's `interrupted` with the runId (row 47). F16 does not dominate that signal: S21's exceptions are the undetermined commit and the latched commit, and a projection failure is neither. The failure is not settlement; the decision point remains the single check (J1:631).

## Controls and units

J1's controls and T7-1 to T7-8 cover S9 and the five lead decisions.

- J-C12 and T7-1 cover the single facade caller and the one `refused()`/`finish` end (LD7-1).
- T7-2 covers the token's custody, including a signal during `prepare_commit` that returns `Ok` (LD7-2). T7-3 covers P4. T7-4 covers the single P5 check. Phase E is J-C14's, and E begins only when P6 reports that the required output returned.
- J-C14, with S21 bound, runs the rule-1 and rule-2 signal cases, plus a signal in D, O and E. J-C14b covers O's renderer, the uncertain step 0's disclosure, the write failure, and the unrenderable envelope. J-C15b's projections cover B and C. J-C16 covers a stalled call.
- T7-5 and T7-6 cover item 2 and the invariant arm (LD7-3). T7-7 covers the census set (LD7-4). T7-8 covers a failed D projection with and without a signal (LD7-5).
- S12-D and S12-O are X9 r17's rows, with this law's expectations (J1:838-839).

The unit split is J1's. J3b (J1:882) carries `finalize`'s new signature, the two entries, the port and the token, the projection split, step 1's terminality, the decision point, S9.3's table, the interrupted branch, and the host arm. J3d (J1:883) carries O: SOP2's hook, rendering of every decided envelope, the failure envelope through J2a, and the durable signal wiring. S18 and S21 are bound, so neither unit waits. The r6 header's deferred session-level tests stay.

## Preservation

Of r6's 247 lines, the ordered alignment into r7 misses exactly two: the title, which becomes r7, and the r6 header's first line (r6 line 23), which gains the sentence "r6 ACCEPTED by Grok on 2026-10-04." Every other r6 sentence survives verbatim. The insertions are the r7 header, the short "r7 (S9)" notes, the S9 section, one forbidden-substitute group, and one Not claimed line.

Item 4's delivery-phase sentences stay in place and are scoped by S9.4 to the Run's own projection. Item 3's existing rows stay, and the r7 note adds the operator stop under S9.3's precedence. Law 468's host projection gains the `Interrupted` arm under this law, the same way X4 r7 item 8 and X3d r6 item 9 added their rows; every existing arm's row is unchanged. X3d r9, X4 r8, X5 item 6's single `replay_candidate` caller, and M3-L's items 16e, 16f and 18 are left as they stand. X5 r4 (S8) is assumed in J1's order and is named as owed.

## NBO-1

The r7 header's source list (PROPOSAL.md:71-75) cites J1 8.2 to 8.4 and does not name 8.1. S9.5 cites J1:542, the termination sentence inside 8.1, and the REV reason remains X3d r9's. The list should name 8.1 (J1:537-542) the next time that header is edited. The decision is already in S9.5.
