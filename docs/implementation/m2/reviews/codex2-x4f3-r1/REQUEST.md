CODEX2 review: unit X4-F3 r1, the first-cause rule in code. It implements law X4 r8's S11.6 for sources 1 to 8 (accepted by you at review round 3, `reviews/codex2-x4-r8-round3/`, verdict ACCEPT, no required findings). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT** on the diff. This is a product code unit under X4 r8 (S11.9, LD8-9), gated before J3b. It adds no file, so it has no inventory successor and no design selection, as for X4-F1 and X4-F2.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/codex2-x4f3-r1`. If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git read-only, and only against the worktree named below.
- Don't run a crash-matrix run set while any other `cargo`, `rustc` or test binary is running on this machine, and don't run cargo while someone else's run set is running: the 5000 ms timing guard fails under load. The implementation agents serialize through the lock directory `$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock`; check it and `ps` first, and ask the lead if in doubt.
- Run every command at `nice -n 19` (a run set at normal priority, with nothing else running), with a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Law

All under arch `docs/implementation/`, accepted. Pins are in `hashes.txt`.
- **`m2/live-guards-x4/PROPOSAL-r8.md`** (X4 r8, 98566 bytes, sha256 `dc239187…`, equal to your round-3 `subjectSha256`; accepted at arch `19a267ec3`). The live `PROPOSAL.md` carries only the acceptance note; review against the r8 snapshot. The parts this unit implements:
  - **S11.6** (:383-502): rule FC; the stop transition's six steps (LD8-6); invariant I1; the entry rule in `OperationGuard::start` (LD8-10); the readers; the placeholder's withdrawal (LD8-8); sources 1 to 8 of the table at :443-453 with their product lines at `cca4fe4` (equal at `d2c00a9` for all five files, as your round-3 `productEvidence` records); the trailing latches; the boundary check's `AlreadyStopped`; the lock order and "no wait"; what each cause maps to, `CertainRefusal` included (LD8-7).
  - **S11.7** (:504-516): `x4.gate.latch.after` follows each stop transition's release, on the same calls and in the same thread order.
  - **S11.8** (:518-580): the controls this unit owns, W-6 (pairs among 1 to 8), W-8 (a), (b) and (d), W-9, W-10's certain-refusal half, W-11 and W-12.
  - **S11.9** (:582-606): X4-F3's scope, file by file, and its lead sets.
  - **S11.12** (:755-770): the X3d, X2 and X9 r17 record items.
  - **Forbidden substitutes** (:803-815): the first stop, and the guard's entry.
- **Your three reviews** of r8: `reviews/codex2-x4-r8/`, `-round2/` and `-round3/` (review.json pinned). Round 3's `entryProof.implementationObligations` are answered in "What X4-F3 changes" below.
- **For the lead sets:** J1 r5 item 12 (`m3/host-pipeline-j/PROPOSAL-r5.md` :824, `4ccb2320…`): "Both lead sets (storage 381, host 98 required runs at C = `3d2d5b5`) are rerun ... serialized"; and X9 r16 (`m2/crash-matrix-x9/PROPOSAL-r16.md`, `f08efe95…`), with X9-6's accepted evidence at C.
- **X3d r9** (`m2/commit-session-x3d/PROPOSAL-r9.md`, `c727001a…`), for the `REV` reasons that must not move.

## Subject

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-x4f3`, detached at product main `d2c00a96c3136fe45b901bc067b6d0ca51f0c9c1` (97 contract successors, 96 inventory successors, v136 selected). Nothing is committed or staged, and no file is added, removed or renamed. The five product files S11.6 cites are byte-identical at `cca4fe4` and `d2c00a9` (your round-3 `productEvidence`).
- **Diff:** `git -C /Users/sb/code/opensip-ai/opensip-x4f3 diff d2c00a9` is 80760 bytes, sha256 `33da62bcef187f8373d6d676710404fc82f3014128f1af12f57ba0f8b64227bb`, with 8 files, +1298 −129. A copy is at `evidence/x4f3.diff`.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH`, Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`.
- **Evidence:** `evidence/` in this directory. Every file is pinned in `hashes.txt`.
  - **Scripts, as run:** `locked.sh` (the lane lock), `lanes.sh`, `mutations.sh` and `mutate.py`, `pins.sh`, `release.sh`, `leadset.sh`, `x9.sh` and `x9b.sh`, `compare.py` and `results.py`. They name the lead's scratch paths.
  - **`lanes-summary.txt`**, **`results.json`** (test counts, mutations and the X9 summary), **`mutations-summary.txt`** and **`lock-log.txt`** (every lock taken and released).
  - **`release-absence.json`** and **`release-summary.txt`.**
  - **`x9/`:** `source-pins-first.txt` and `source-pins.txt` (before and after the sets), `waits.txt` (the load checks), `overlap.txt` (the 10 s sampler), `x9.summary`, `compare.json`, and both sets' `matrix.json`.

## The gap, at `d2c00a9`

X4a's sources latch and record in separate steps, and a reader records a placeholder:
- **The placeholder.** `Shared::latched()` (og:218-220) records `FailStop { latched }` when it finds the gate latched with no cause. Checkpoint step 3, `admit`'s refusal and an observer tick that meets `AlreadyStopped` all call it.
- **D8-1's two schedules** (S11.11). X3d's certain refusals latch with no cause (`OperationGuard::stop`, og:419-421, from cs:562, :577 and :986). An observer tick after one of them records the placeholder, and `finish` then writes `REV(observer-fail-stop)` instead of `REV(operation-stopped)`. The stale-guard path latches (og:548), then records `Stale(row)` (og:549); a reader in between turns the stale guard's row into `OBSERVER.FAIL_STOP`.
- **The monitor-side gaps.** The monitor latches inside its read (rv:149-151, :189-191) and its caller records afterwards (og:255-262, :570-574); `StopOnUnwind` (rv:84-91) latches with no cause at all; a poisoned monitor mutex latches, then records (og:221-226); the lock mismatch latches with no cause (og:538-543).
- **The entry gap** (RF-X4R8-R2-1). A first read that succeeds during unrelated unwinding returns `Ok` on a gate `StopOnUnwind` latched bare, and `start` (og:372-406) installs a guard with no cause.

## What X4-F3 changes

Line numbers are the worktree's. "og" is `crates/security/src/custody/operation_guard.rs`, "rv" `crates/security/src/revocation.rs`, "ca" `crates/security/src/commit_authority.rs`, "cs" `crates/security/src/custody/commit_session.rs` and "oh" `crates/security/src/custody/operation_handoff.rs`.

**The stop transition and I1 (og).**
- **`StopHandle`** (og:152-260): the operation's stop handle, `LeaseFree`'s `StopObserver` bound to the one stop-cause record (`StopRecord`, og:160-169). `Shared.cause` and `Shared::record` are gone; the record lives in the handle, and `Shared.stop` is the handle (og:453-464; `Shared::lock`, og:466-468).
- **`StopHandle::stop`** (og:208-234) is S11.6's stop transition: (1) the record's lock, (2) the one fetch-OR, (3) the record if, and only if, that fetch-OR set `LATCHED` (`Latched.first`; `get_or_insert`, so a recorded cause is never replaced), (4) the read, (5) the release at the end of the section closure, then (6) `x4.gate.latch.after` in `ca`'s `latch_within` after the section returns. It returns `Transition { state, first, cause }` (og:170-186). The section is exactly og:214-225: the record's lock, the one fetch-OR, the insert and the read, and nothing else; no I/O, wait, callback, crash point or monitor mutex.
- **Readers only read.** `StopHandle::latched` (og:239-242) returns the recorded cause, or `GuardRefusal::Invariant` if none is recorded (LD8-8); it records nothing. `cause()` (og:244-246) is `OperationGuard::cause`'s source (og:664-666).
- **The entry rule** (og:410-438, `Entered` and `enter`; og:605-648, `start`): (1) `StopHandle::new` (og:424), (2) the monitor's `rebind` to that handle, which consumes the bare `StopObserver` clone (og:428-432), (3) `entry_latched` reads the word under the record's lock (og:434, og:253-259), (4) a latched gate returns `Err(Entered)` with its parts untouched, (5) only `start` spawns the observer, after `enter` returned `Ok` (og:621, then the spawn at og:630-638). `GuardStart` (og:439-448) is `start`'s refusal: `Latched`, or `Observer(io::Error)` as before.
- **`OperationGate::latch`** is now `#[cfg(test)]` (ca:151-157), a W-12 seam: in production nothing latches an operation's gate except through `StopObserver`, which the guard holds only inside the handle.

**Sources 1 to 8, each in its stop transition.**

| # | Source | Changed lines | Cause recorded |
|---|---|---|---|
| 1 | The observer's revoking observation | og:282-298 (`observed`, :294), used by the tick and checkpoint step 2 through `Shared::observe` (og:475-500, :493) | `Revoked { subject }` |
| 2 | A monitor read's failure | rv:170-203 (`read_sampled_with`, its new `subject` argument; :199-201 `self.stop.fail(subject(reason))`); og:267-281 (`MonitorStop for StopHandle`, `fail` at :275-277); og:483-492 (the caller's subject: the observation's own failure's, else the stop reason's, exactly r7's og:260-262 rule) | `FailStop { subject }`, today's subject |
| 3 | The boundary check's own failure | rv:204-245 (`boundary_with`, its `subject` argument; :241-243); og:882-894 (`"admission-boundary"`, then the trailing transition) | `FailStop { admission-boundary }` |
| 4 | `StopOnUnwind` | rv:113-124 (`StopOnUnwind` calls `unwound()` on the monitor's stop); og:278-280 | `FailStop { latched }` after the entry; bare before it, and the entry refuses |
| 5 | The monitor's mutex poisoned | og:299-309 (`lock_monitor`), og:466-468 | `FailStop { latched }` |
| 6 | A stale guard at step 1 | og:310-314 (`stale`), og:850-852 | `Stale(row)` |
| 7 | The lock mismatch | og:315-327 (`refuse`'s `Invariant` arm), og:844-847 | `CertainRefusal`; the refusal stays `GuardRefusal::Invariant` |
| 8 | X3d's certain refusals | og:653-662 (`OperationGuard::stop(cause)`); cs:564, :579, :988 pass `StopCause::CertainRefusal` | `CertainRefusal` |

- **The trailing latch** on every checkpoint refusal (og:843, `refuse`, og:315-327) is a stop transition with the refusal's own cause and reports the first stop's cause (S11.6, "Trailing latches").
- **`CertainRefusal`** (og:113-117; its `row()` arm, og:139, the invariant row), and **`RevReason::of`**'s arm (cs:100-102): `Some(CertainRefusal) | None → OperationStopped`, so X3d's reason set, reserve and every `REV` reason stay as they were.
- **The monitor (rv).** `MonitorStop` (rv:83-99) is what a monitor latches through: the bare `StopObserver` at the lease-free point (rv:100-112, which ignores the subject), the stop handle from the entry (og:267-281). `FreshnessMonitor` is generic over it (rv:131-152, default `StopObserver`, so the monitor's own tests are unchanged), and `rebind` (rv:139-147) is the entry's step 2.
- **The crash point (ca).** `FinalGate::latch_within` (ca:39-49) runs a latch's section, then `x4.gate.latch.after`; the bare latch (ca:50-53) is the section with the fetch-OR alone. `Latching::fetch_latch` (ca:58-70) is the only `fetch_or` on the word, and `Latched` (ca:71-78) carries its result. One barrier site, as before.
- **The handoff (oh).** One mapping arm (oh:1234-1242): `GuardStart::Latched` → `OperationRefusal::Live(StopCause::FailStop { subject: StopReason::AlreadyStopped.subject() })`, which is `"latched"`, the value a first read returning `AlreadyStopped` takes (oh:1086-1089, `cca4fe4`'s :1085-1088); `GuardStart::Observer(e)` → `OperationRefusal::Observer(e)` as before. The import gains `GuardStart`.

**Round 3's implementation obligations:**
- *No raw stop-handle escape or clone surviving outside the transition.* The handle's clones are the guard's (`Shared.stop`) and its monitor's; the raw `StopObserver` inside is used only by `stop` (the transition), `observe` and `entry_latched` (loads). The test-only `Watch` and `hold_cause` read or lock; neither latches.
- *Rebind before the checked load; spawn after the cause lock is released.* `enter`'s order, pinned by W-9.
- *No clock or counter callback or monitor read while the cause lock is held.* The monitor calls `fail`/`unwound` after its callbacks return; the caller's `subject` closure runs before `fail` takes the lock.
- *Map the entry refusal to `Live`, keeping `Observer(io::Error)` for a failed spawn.* oh:1234-1242.
- *Keep the word monotonic and the monitor's history; no clear, reset, cause seeding or new row.* The entry returns the parts untouched; W-11 checks the latch and the history.

**Unchanged:** every row, code, class, exit, detail and `REV` reason; the checkpoint's steps and their order; the observer's cadence; the gate's state law, `admit` and `observe`; every crash point and scope (one barrier site moves inside `ca`, below); every read, write and clock sample; X3d's outcomes and reserve; the handoff's order and its other refusals. No file is added, removed or renamed. The cancellation latch, the window bits, the masked `admit` loop and `StopCause::Operator` are J3b's and are not here.

| File | Change |
|---|---|
| `crates/security/src/custody/operation_guard.rs` | the stop handle and transition, the sources' transitions, the entry rule, `CertainRefusal`; test seams `Watch`, `hold_cause`, `latch_bare`, `scripted::unwinding` |
| `crates/security/src/revocation.rs` | `MonitorStop`, the generic monitor, `rebind`, the caller's subject |
| `crates/security/src/commit_authority.rs` | `latch_within`, `Latching`, `Latched`; `OperationGate::latch` test-only |
| `crates/security/src/custody/commit_session.rs` | three call sites, `RevReason::of`'s arm; test helper `end_path_for_tests::reason` |
| `crates/security/src/custody/operation_handoff.rs` | the mapping arm |
| `operation_guard_tests.rs`, `operation_live_tests.rs`, `commit_session_tests.rs` | the new tests; four existing call sites gain the new `subject` argument (no expected value changes) |

## Tests: every control this unit owns

| Control (S11.8) | Test | Where | What it asserts |
|---|---|---|---|
| W-6 (pairs among 1 to 8) | `every_ordered_pair_of_sources_keeps_the_first_stops_cause` | og-tests :620 | All 56 ordered pairs, each on a fresh rig. A's path reports its own cause (`GuardRefusal::Invariant` for 7; for 8 a `Transition` with `first: true`); the record is A's cause and the gate is state 2 (I1). After B the record is still A's; B's path reports A's cause, its row is A's cause's row (the invariant row when B is 7), and for B = 8 the `Transition` has `first: false` and A's cause; `finish`'s `REV` reason (`RevReason::of`, through `end_path_for_tests::reason`) is A's |
| W-8 (a) | `a_certain_refusal_then_an_observer_tick_keeps_operation_stopped` | cs-tests :1049 | A real session with its settlement reserve: `refused()` records `CertainRefusal` (state 2); an observer tick returns false and records nothing; `finish` appends one `REV`, reason `operation-stopped`, and no `CLN` |
| W-8 (b) | `a_stale_guard_held_after_its_section_keeps_its_row_and_stale_guard` | cs-tests :1074 | A real session; the store marker replaced, so the publish path's first checkpoint is stale at step 1. A one-shot hook after the stale guard's transition is released runs an observer tick before the checkpoint returns: the tick returns false and reads `Stale(Installation(Custody { required-files-changed }))`. The outcome's termination is `T::Custody { required-files-changed }`, the record stays the stale guard's, and `finish` appends one `REV`, `stale-guard` |
| W-8 (d) | `an_observer_revocation_then_a_certain_refusal_keeps_trust_revoked` | cs-tests :1124 | Twice: an observer revocation (tick false, `Revoked { trust-revoked }`), then a certain refusal through `refused()`, and through `publish`, whose checkpoint reports `T::RevokedDuringOperation { trust-revoked }` before its refusal arm (source 8) records nothing. The record stays `Revoked`; `finish` appends one `REV`, `trust-revoked` |
| W-9 | `the_stop_transition_is_the_only_latch_after_the_guards_entry` | og-tests :678 | Over production text (comment lines dropped; X8 r3's convention) of og, ca, rv, cs and oh: one `fetch_or` on the word and no `fetch_and`, `store`, `swap` or lock in ca; the barrier once, right after the section's return; `latch_within` called once in og, inside `StopHandle::stop`; bare `.latch()` only in the test seam `latch_bare` and in rv's `MonitorStop for StopObserver`, and `OperationGate::latch` behind `#[cfg(test)]`; none in cs or oh; no `fn record`, one `get_or_insert`, inside the transition; `latched()` inserts and latches nothing; the section's exact text; the cause lock taken only by the transition, the reader, the entry check and `hold_cause`; `admit`'s success path takes no cause lock; `enter`'s order (record, rebind, check, refusal) and `start`'s (`enter` before the spawn); `Shared` holds no `StopObserver` and its monitor is `MonitorCell<StopHandle>` |
| W-10 (a), certain-refusal half | `a_certain_refusal_completes_while_an_observation_holds_the_monitor` | live-tests :1057 | While a test thread holds the monitor's mutex (`hold_monitor`), `guard.stop(CertainRefusal)` on another thread completes: state 2, cause `CertainRefusal`. It would deadlock if a stop transition took the monitor's mutex |
| W-10 (b) | W-9's pin | og-tests :678 | the section's exact text |
| W-10 (c) | `a_successful_admission_takes_no_stop_cause_lock` | live-tests :1077 | While a test thread holds the stop-cause lock (`hold_cause`, outside any transition), the final admission succeeds: a permit, state 1, no cause |
| W-11, at the handoff | `a_first_read_succeeding_during_unrelated_unwinding_is_refused_at_the_guards_entry` | live-tests :1010 | The real handoff, run in a destructor during an unrelated unwind (`resume_unwind`): the first read succeeds and latches bare; the handoff refuses with `OperationRefusal::Live(FailStop { latched })`, row `ObserverFailStop { latched }`; no operation exists; the fence and N are free |
| W-11, at the guard | `a_successful_lease_free_read_during_unrelated_unwinding_gets_no_guard` | og-tests :331 | The lease-free first read in a destructor during unwinding: `Ok`, gate state 2. `enter` refuses: the gate is still state 2, nothing is recorded, and the monitor's history is that read's (its earliest instant). No guard, so no observer |
| W-11, after the entry (source 4) | `the_same_read_after_the_guards_entry_records_its_fail_stop` | og-tests :348 | After a clear entry, the same read in a destructor through the rebound monitor: `Ok`, cause `FailStop { latched }`, state 2; the next read returns `AlreadyStopped`, and `observed` (the tick's and step 2's reader) returns that cause |
| W-12 and its control | `a_bare_latch_on_any_lease_free_handle_before_the_entry_gets_no_guard` | og-tests :379 | After a successful first read, a bare latch through the gate, `LeaseFree`'s `StopObserver`, and the monitor's clone, each in turn (test seam `latch_bare`): each is W-11's refusal. The control: with no latch, the parts are state 0 with no cause and the read's history, and their first stop transition records its cause (`first: true`) |
| LD8-7 | `a_certain_refusal_is_the_invariant_row` | og-tests :297 | `CertainRefusal.row()` is the invariant row; `REV` `operation-stopped` for it and for none |
| F41's existing tests, kept | `every_bounded_gate_trace_obeys_the_selected_two_bit_law`, `concurrent_stop_and_admission_…`, `one_gate_mints_one_permit_…`, `the_final_admission_mints_one_permit_and_a_late_latch_keeps_its_outcome` | ca's tests, og-tests, live-tests :307 | unchanged and passing |

**Mutation checks** (`evidence/mutations.sh` and `mutate.py`, run once on the final diff, `operation_guard.rs` restored byte-identical afterwards; `evidence/mutations-summary.txt`). Each mutation was applied alone and the twelve new tests run:
- **`r7-records`** (X3d's stop latches with no cause, and the reader records the placeholder, as r7): W-8 (a), W-10 (a) and W-9 fail.
- **`no-entry-check`** (the entry never refuses): both W-11 entry tests and W-12 fail.
- **`bare-unwind`** (the unwind latch through the handle records nothing): W-11's after-entry test, W-6 and W-9 fail.

W-6 does not catch `r7-records`, because its source 8 calls the handle's transition, which that mutation leaves alone; W-8 (a) catches it through the real `refused()`.

## Judgment calls

1. **Checkpoint step 3 on an admitted gate (a direct question).** S11.6's source table has no row for step 3 finding state 1 (`Admitted`, `LATCHED` clear): a checkpoint after this operation's own admission. No production path reaches it (`publish` admits once and consumes the session), but F41's existing test does: `the_final_admission_mints_one_permit_and_a_late_latch_keeps_its_outcome` (live-tests :336-350) runs a second admission and expects `Stopped(FailStop { latched })` and state 3. r7 produced that through the placeholder: `latched()` recorded `FailStop { latched }`, then the trailing latch took 1 to 3. With the placeholder withdrawn, step 3's `Admitted` arm (og:871-875) gives its refusal the cause `FailStop { latched }` itself, and its trailing latch, the first stop (1 to 3), records it in its own transition. I1 and FC hold, and the test's expected value is unchanged. I read S11.6's "Trailing latches ... Its cause is that refusal's own" as covering this, the refusal's own cause being today's; LD8-8 says the placeholder subject "survives only as the true cause of sources 4 and 5", which does not list it. **Rejected:** the invariant row or `CertainRefusal` for it, either of which changes F41's tested value. **Question:** do you accept this reading, or should the lead add a record note to X4 r8?
2. **W-5 is J3b's.** The lead's dispatch listed W-5 for this unit; S11.9 lists W-1 to W-5 under J3b, because W-5 races the cancellation latch, and this unit follows the law. The existing sources' readers are still exercised: the tick's and step 2's reader (`observed` after a failed read: W-6 with B = 2 or 4), step 3's (source 4's successful read), and the boundary check's own failure and its `AlreadyStopped` (source 3 as A and as B). `admit`'s refusal reader is not: with sources 1 to 8 nothing can latch between step 3 and `admit` while the checkpoint holds the monitor's mutex.
3. **W-8's signal steps are J3b's.** (a), (b) and (d) each include a signal (`OutsideWindow` or `AlreadyStopped`), which is the cancellation latch, source 9. This unit runs every other step as written, through real sessions; J3b adds the signals.
4. **W-8 (b)'s hold.** A one-shot test hook that runs after the next stop transition's release (`Watch::after_stop`; the `#[cfg(test)]` block after `latch_within` returns in `StopHandle::stop`, og:226-232), outside the critical section as S11.8 requires. It runs the observer tick on the session thread while the checkpoint is held between the stale guard's transition and its trailing latch. The tick cannot block there: step 1 holds neither the monitor's mutex nor the cause lock.
5. **W-10 (c) is included** although S11.9 lists only W-10's certain-refusal half: (c) pins that `admit`'s success path takes no cause lock, which this unit's transition design must keep. (b) is W-9's pin.
6. **W-6's rig.** S11.8: "The pairs run at the guard level". The rig is a real lease-free point after a real first read and a real entry (`enter`), with one monitor per monitor source on the operation's stop handle, each after one successful read made before any source runs (so no helper read happens while another source's destructor unwinds). Each source runs through the production function that makes its transition: `observed`, `read_sampled_with` and `boundary_with` with the scripted clock and counter seams, `lock_monitor` on a poisoned mutex, `stale`, `refuse`, and `StopHandle::stop(CertainRefusal)` for source 8, which is all `OperationGuard::stop` does (og:660-662; W-8 runs the real call). The checkpoint's trailing latch (`refuse`) follows sources 1 to 7. B's `first` callback runs A at B's last point before its own transition: inside B's counter (2, 4) or clock (3), so the monitor sources' own transitions run and find `LATCHED` set; otherwise just before B.
7. **The monitor's interface.** `MonitorStop` is a trait in `revocation.rs`, so the monitor does not depend on the guard's types; `FreshnessMonitor` is generic over it, and `rebind` consumes the bare stop, so after the entry the monitor holds no bare `StopObserver` (a type-level form of W-9's "nothing bare survives"). Source 2's subject comes from the caller's closure, evaluated before `fail` takes the lock: the observation's own failure, recorded in a `Cell` by the counter, else the reason's (r7's rule). Source 3's is the caller's argument. Source 4's `latched` is in og beside source 5's.
8. **One barrier site.** `x4.gate.latch.after` stays a single `crash_barrier!` in `commit_authority.rs`, now in `FinalGate::latch_within`, which runs every latch's section, bare or a transition, and then the point. The bare latch at the lease-free point fires it as before. On every path the number of calls is r7's: two on a refusal at step 1, at step 2 after a revocation or a failed read, at step 4 after the boundary's own failure, and for a poisoned mutex; one at step 3, on `admit`'s refusal, on step 2's or step 4's `AlreadyStopped` at entry, for the lock mismatch, for X3d's stop, and for an observer tick's revocation or failed read; none for a tick's `AlreadyStopped` at entry; and one more for `StopOnUnwind` whenever a read or check ends while its thread is panicking, as before.
9. **A destructor-time observation that revokes.** If an observation runs during unrelated unwinding and its read returns `Revoke`, `StopOnUnwind`'s latch at the read's end is the first stop (`FailStop { latched }`, source 4), and the revocation's transition then records nothing. r7's code latched bare there and recorded `Revoked` afterwards. This is FC with source 4 as round 3 defines it ("a read or check that succeeds while the thread is already unwinding") and S11.11's "other monitor-side gaps", not an exception; no test or production path reaches it.
10. **The lock mismatch now records `CertainRefusal`.** After source 7, `guard.cause()` is `Some(CertainRefusal)` where r7 left `None`. The refusal stays `GuardRefusal::Invariant`, and the `REV` reason stays `operation-stopped` (`of(None)` and `of(Some(CertainRefusal))` are equal). The existing test (`a_checkpoint_needs_this_operations_own_level_four`) asserts the refusal and the state, which are unchanged.
11. **`enter` is split from `start`.** The entry rule is its own function, so that W-11 and W-12 can check the refusal's parts (state, record, history) without a trust view; `start` calls it first and spawns only on `Ok`, and drops the parts on `Err`. W-9 pins both orders.
12. **Test seams.** All `#[cfg(test)]` and outside any critical section: `Watch` (tick, cause, state, `after_stop`), `hold_cause`, `LeaseFree::latch_bare` and `BareHandle`, `FreshnessMonitor::stop`, `OperationGate::latch`, `scripted::unwinding`, and `end_path_for_tests::reason` in `commit_session.rs`. `scripted::unwinding` uses `resume_unwind`, so `thread::panicking()` is true in the destructor without a panic message; the W-11 tests assert it was.
13. **The no-wait tests hang rather than time out on failure.** W-10 (a) and (c) join a thread with no timeout, as the existing `a_read_waiting_on_the_shared_monitor_counts_its_wait` does; the law asserts no timing bound.
14. **Four existing call sites gain an argument.** `operation_guard_tests.rs`'s two `read_sampled_with` and two `boundary_with` calls pass the new `subject` (`StopReason::subject`, `"admission-boundary"`); no expected value changes, and the diff removes no `#[test]` and no assertion line.

## Not claimed

- **J3b's half** (S11.9): the window bits, the masked `admit` loop, the cancellation latch (source 9) and its stop transition, `StopCause::Operator`, W-1 to W-5, W-6's pairs with source 9, W-7, W-8 (c) and W-10's cancellation half; J-C15 and J-C15b. No seam for source 9 is added: the law asks for none.
- Native scheduling of the cause lock or of the 5 s and 10 s bounds (S11.6 "no wait"; "Not claimed").
- The X9 r17 record note (S11.12): "`x4.gate.latch.after` follows the stop transition's release". That is law work for the lead; X4-F3 only makes the code match it.
- The lead-set rerun on the integration commit (S11.9 says "on its integration commit"); this request's sets ran on `d2c00a9` plus the uncommitted diff, before review, as S11.12's "before X4-F3's review" requires. The lead reruns them at integration.
- Linux.

## No inventory

The diff adds, removes and renames no file, so the selected inventory (v136 at `d2c00a9`) stands. Inventory rows carry no bytes, and the touched files' descriptions remain true. There is no inventory successor and no `inventoryCandidateAssessment`. (J2a's v137 and E2a's v138 candidates are independent of this unit.)

## Lead results

**How they ran:** every lane ran on `d2c00a9` plus the final diff (`evidence/lanes.sh`), serially, each taking the shared lane lock and releasing it straight after (`evidence/locked.sh`, `lock-log.txt`), at `nice -n 10`, with a private 0700 TMPDIR and `--locked --offline`. The real home was absent before and after. The lanes ran from 18:58 to 19:29Z; the drift rerun ran at 19:56Z.

| Lane | Result |
|---|---|
| `cargo fmt --all --check` | clean |
| `cargo build --workspace --all-targets` | pass |
| `cargo build` of platform, security, storage and host, `--features crash-matrix --all-targets` | pass |
| `cargo build` of security, storage and host, `--features scenario-fixtures --all-targets` | pass |
| `cargo build -p opensip-security --features opensip-platform/crash-matrix` | pass |
| `cargo clippy --workspace --all-targets -- -D warnings` | clean |
| `cargo clippy`, the crash-matrix lane (four packages, `--all-targets`, `-D warnings`) | clean |
| `cargo clippy`, the scenario-fixtures lane (three packages, `--all-targets`, `-D warnings`) | clean |
| The 12 new tests (security lib, `--test-threads=1`) | 12 passed, 0 failed |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1750 passed, 0 failed, 3 ignored (20 binaries, 528 s) |
| The same, run 2 | 1750 passed, 0 failed, 3 ignored (520 s) |
| `cargo test --workspace --doc` | 20 passed |
| `cargo test`, platform, security, storage and host, `--features crash-matrix --all-targets --no-fail-fast` | 1648 passed, 0 failed, 3 ignored (517 s) |
| `tools/generate_contracts.py` drift check (pinned node, generator `contracts-generator-rebuild-02`, the selected child Python) | pass: 40 sources verified, 8 outputs, `changed: []` |
| `verify_design.py --architecture ../opensip_arch --implementation .` | pass: v136 selected, 96 inventory and 97 contract successors, 100 inheritance rows, 21 inventory and 1 contract passage supersessions, 40 generation and 48 admission sources |
| `check_package_edges.py --lane host` against v136 | pass: 12 workspace packages, 22 declared and 20 resolved internal edges |
| `check_package_edges.py --lane rust-provider` against v136 | pass |
| `tools/tests/test_package_edges.py` | 14 run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` | pass: 8 local sources verified |
| `check_identity_dependencies.py` | pass: 305 sources |
| `tools/tests/test_dependency_policy.py` | 9 run, OK |
| `tools/tests/test_identity_dependencies.py` | 5 run, OK |
| `python3.14 -m unittest tools/tests/test_check_crash_matrix.py` | 26 tests OK |
| X9 lead sets (below): storage 381 and host 98 runs, in full | every run PASS; identical to the X9-6 evidence, 0 differences |

**Notes on the results:**
- **Counts.** The diff adds 12 `#[test]` functions and removes none, and removes no assertion line. So `d2c00a9` has 1738 workspace tests and 1636 in the crash-matrix lane, and the 12 make 1750 and 1648. `no_manifest_enables_the_crash_matrix_feature` and `every_test_feature_site_is_on_the_pinned_list` pass in both workspace runs.
- **The drift check's first attempt** exited 1 with "missing regular input: tools/contracts/node_modules/typescript/LICENSE.txt": a fresh worktree lacks the two git-ignored dependency trees. Main's ignored `tools/contracts/node_modules` and `python-packages` were copied in (the diff is unchanged; the generator checks every input's sha256), and the same command passed (`contracts-drift-rerun` in `lanes-summary.txt`). No generator input is a crate file.
- **Development runs before the lanes** (security lib only): the guard, gate and monitor tests (29 passed), then `operation_handoff::tests` (71 passed), and the mutation checks above.

## Crash barriers, traces and the X9 rows

**One barrier site moves inside `commit_authority.rs`; no point, scope, read, write or clock sample is added or removed.** `crash_barrier!("x4.gate", "latch.after", step)` keeps its text and its one site; it now sits in `FinalGate::latch_within`, after the latch's section returns (LD8-4). Judgment call 8 lists the calls per path, which equal r7's. Every `cfg` attribute the diff adds is `#[cfg(test)]` (the rest are W-9's pinned strings).

### The lead sets (S11.9; J1 r5 item 12), run 2026-10-04 on `d2c00a9` plus the final diff

**Source pins** (`evidence/x9/source-pins-first.txt` before the sets, `source-pins.txt` after, identical): the X9 harness sources (the checker and its test, `crates/platform`, storage's and host's `tests` trees with both `required-runs.v1.json`, storage's, host's and security's `crash_matrix_support`, and security's `crash_matrix_sites.rs` and `crash_matrix_census.rs`) are byte-identical at X9-6's C (`3d2d5b5`) and at `d2c00a9`, and the diff touches none of them. Both required-runs files have X9-6's hashes (`14a275ad…`, `80e4a02e…`). So no harness source or required-runs file changed.

**Which sets.** S11.9 and J1 r5 item 12 name both lead sets, storage (381 required runs) and host (98), rerun serialized. So both ran in full (no `OPENSIP_X9_ROWS`), once each, storage then host, through X9-6's run-set entry `x9_6_matrix` (census, then every required run), with `OPENSIP_X9_RELEASE_ABSENCE` set to the record below.

**How.** `evidence/x9b.sh` ran each set through `locked.sh`, holding the lane lock for the whole set, at `nice -n 0`. Before each set, `leadset.sh` required that no `cargo`, `rustc`, clippy or test binary be running (`waits.txt`): both were clear at once.
- **A stopped first attempt.** At 19:57Z the first attempt's load check matched other agents' lane scripts that were waiting for the lock by the word `cargo` in their command text, so it would never have cleared. It was stopped after 36 s, before any run started (the lock released normally), and the check now matches running executables only. `waits.txt` records it.
- **Overlap.** A 10 s sampler (`overlap.txt`) recorded every build or test process outside the worktree's binaries from the storage set's start to the comparison: it saw only the two sets' own `cargo` processes (pids 68952 and 81466).
- **Times:** storage 1914 s (20:24:42Z to 20:56:36Z, after 1560 s waiting for the lock), host 746 s (to 21:09:02Z). Every run PASS: 381 of 381 and 98 of 98. The real home stayed absent.
- **Timing guards:** 43 storage runs carry one, 2581 to 2846 ms, and 2 host runs, 1071 to 1084 ms, all under 5000 ms (X9-6's lead-1: 2667 to 2932 and 1010 to 1112). Their values are not compared.

**The comparison** (`evidence/compare.py`, X4-F2's method with every run selected; output `x9/compare.json`) is against the accepted X9-6 evidence, arch `crash-matrix-x9/evidence/3d2d5b5…/` (lead-1's run files and both targets' `matrix.json`).
- **What it compares**, for every run: verdict, `postState.normalizedSha256`, the ladder, `notApplicable`, every child's role, ordinal, exit, `lastHeld`, outcome and trace `{records, sha256}`, and whether `timingGuard` is present. Per target: the run list against the evidence's, the census and the kill set.
- **The result: identical, with 0 differences.**
  - Storage: 381 of 381 runs equal. Census: 259 points, trace 1379 records, `e9add21e…`. Kill set: 321 points.
  - Host: 98 of 98 runs equal. Census: 218 points, trace 1195 records, `93d0922a…`. Kill set: 271 points.
- **Expected differences, not compared:** each `matrix.json`'s `product` is `{commit: d2c00a9, worktreeClean: false}`, because the subject is uncommitted, and `releaseAbsence` carries the binary below.
- **So no transcribed value moves**, and X9 r17 has nothing to re-transcribe for X4-F3 (S11.12); its record note about the point's placement remains the lead's.

The equal censuses and child traces mean `x4.gate.latch.after` is reached on the same calls and in the same order in every census and every run, as LD8-4 requires. A full two-target `check` with `matrixPass` needs a clean commit, so it can run only at integration, with the integration-commit rerun.

## Release absence

`evidence/release.sh`, record `evidence/release-absence.json`:
- `cargo build --release -p opensip-cli` (no features) gives `target/release/opensip`, 6316960 bytes, sha256 `161c4f624b8f09fbb97ce63baff6b44049839a6edc4d17ca0eb3c30ea92acb57`.
- Neither `OPENSIP_X9_` nor any of the 25 registered scope names appears in it (26 strings searched, `found: []`, `passed: true`).
- The release builds of storage and of host with `--features crash-matrix` are each refused at the compile guard (exit 101).
- X9-6 recorded 6315264 bytes, `b32604fe…`, at `3d2d5b5`. The binary differs because main has moved since and the security code it links changed.

## Lead rulings (Claude Opus 5.5, before sending)

| Item | Ruling | Rejected |
|---|---|---|
| Judgment call 1: checkpoint step 3 on an admitted gate | **Accepted as a lead reading of S11.6.** A checkpoint that runs after this operation's own admission refuses with an explicit `FailStop { latched }`, and its trailing latch is then the first stop and records that cause. FC holds, and F41's existing expectation is unchanged. It goes to X4's next record revision as a record note. | Leaving no cause, which would yield the invariant row and change F41's accepted outcome; or a new cause value. |
| W-5, and W-8's signal steps (a), (b), (d) | **Confirmed as J3b's,** as S11.9 assigns them: each races or uses the cancellation latch, which is source 9. The existing sources' reader paths are exercised by W-6 here. | Building source 9's seams in X4-F3, ahead of J3b. |
| The two behaviour changes on unreached paths | **Confirmed as the law's own effect:** the source 4 ordering under unwinding, and `CertainRefusal` after a lock mismatch with the REV reason unchanged. | None. |
| X9 r17's record note for `latch.after` | **Already in review** as part of X9 r17 round 2 (`m2/reviews/grok-x5-r4-x9-r17-s12/`). This unit's lead sets show 0 differences from X9-6, which is the check that note names. | None. |

**Product main has moved** from `d2c00a9` to `0765f8c`. That is five binding commits (REG v3, CRC-2, ENUM-1, SD-8), and each changes only `design-lock.json`. The subject diff is against `d2c00a9`, and integration rebases it. The lead re-runs `verify_design` on the integrated tree.

**Shared machine.** Before any cargo build, test or clippy run, take the lane lock with `mkdir "$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"`, and remove it with `rmdir` straight after. If you rerun a lead set, hold the lock for the whole set, unniced. Other units' sets share this machine under the 5000 ms guard.

## Decide

- **Law:** does the diff implement S11.6 exactly for sources 1 to 8: the stop transition's steps and section, I1, the readers, the placeholder's withdrawal, `CertainRefusal` and its two mappings, the trailing latches, the boundary check's `AlreadyStopped`, the lock order, and the entry rule with its order and its `Live(FailStop { latched })` refusal?
- **Scope:** are the X3d call sites, `RevReason::of`'s arm and the handoff's arm exactly S11.9's and S11.12's, with no outcome change?
- **I1 everywhere:** can any production path after the entry set `LATCHED` outside `StopHandle::stop`, record outside it, or record from a transition that did not set `LATCHED`? Can a bare latch reach a guard?
- **The crash point:** is `x4.gate.latch.after` reached on the same calls, in the same thread order, after the release (LD8-4, S11.7), and does the lead-set comparison show nothing moved?
- **Tests:** do the controls cover W-6, W-8 (a), (b) and (d), W-9, W-10's certain-refusal half, W-11 and W-12 as S11.8 states them, with seams only outside the critical section?
- **Judgment calls:** are calls 1 to 14 acceptable? Call 1 asks you a direct question.

Write REVIEW.md and review.json under the output directory. review.json needs:
- `"verdict"`: `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectSha256"`: `33da62bcef187f8373d6d676710404fc82f3014128f1af12f57ba0f8b64227bb`, the diff's sha256, as a single string.

No `subjectManifestSha256` or `inventoryCandidateAssessment` is needed: the unit has no inventory or design selection. Do not commit.
