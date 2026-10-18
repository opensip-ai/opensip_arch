# D3b-0 r2: the macOS descendant mechanisms (M3-D r5 items 4, 8, 16 and 18; D3b plan r3, sub-unit D3b-0)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 2.**

## Round 2

Round 1 (`codex-d3b-0-r1`, subject `ae101c34…`) returned REQUIRED-FINDINGS: one finding and one non-blocking observation. Q1 and Q2 were both accepted. The r1 package (`../d3b-0-r1/`) is history and unchanged.

| Item | Round 1 | Disposition in r2 |
| --- | --- | --- |
| **D3B0-R1-RF-1** (libproc listing failures read as `Complete(empty)`) | `proc_listpids` and `proc_listchildpids` return 0, not -1, when the underlying `proc_info` call fails. Both listings tested only for a negative return, so a failure became `Ok(Listing::Complete(vec![]))`. | **Fixed.**<br>**The discipline.** Both listings now go through one `native_listing(call, …)`. It clears this thread's errno immediately before the call, so a stale errno is never read. Zero with errno set is `Io {call, error}`, which keeps the call's name and errno. Zero with errno clear is a real empty list. A negative return also fails.<br>**Unchanged:** the single capacity-plus-one buffer and the count-against-bytes distinction (`proc_listchildpids`' count is used directly; `proc_listpids`' bytes are divided by the pid size).<br>**Probed on this host:** a buffer smaller than one pid makes both calls return 0 with `ENOMEM`, and a successful empty listing returns 0 with errno untouched.<br>**Controls.** A `cfg(test)` seam, `LISTING_BYTES`, passes a one-byte size to the real call. Two tests are added:<br>• `a_listing_failure_is_never_an_empty_list`: each listing's real zero return with `ENOMEM` is `Io`, with its own call name and errno, and never an empty list;<br>• `an_empty_listing_is_complete_despite_a_stale_errno`: with errno preset to `EPERM`, a childless root's children and a reaped root's emptied group are each `Complete(vec![])`.<br>**Mutations added:** `listing-error-read-as-empty` (the zero-with-errno test removed) and `listing-errno-not-cleared` (the clear removed).<br>**Applied to every libproc and `kill` call** (the self-review's item 3, below):<br>• D1a's unbounded `group_members` now uses the same `native_listing`. It is kept until D3b-1 (LD-D3B0-1), and the failure test covers it too;<br>• `process_identity`'s `proc_pidinfo` also returns 0 on failure, so it clears errno before the call. `None` is given only for `ESRCH`. A zero or short return with no errno is `Io`, never a missing process. A third test, `an_identity_failure_is_never_a_missing_process`, presets a stale `ESRCH`, forces a real `ENOMEM` failure through the `IDENTITY_BYTES` seam (a ten-byte size), and requires `Io`. Mutation `identity-error-read-as-gone`;<br>• `proc_pid_rusage` (`resident_bytes`) and `kill` return -1 with a fresh errno on failure and 0 on success (probed). They are checked by `check` and by the `kill` match, so they need no change. |
| **D3B0-R1-NBO-1** (the rebase record's attempt) | r1's REQUEST and SCOPE pointed to a `rebased.json` in the packaged lane. The move was made by attempt 2, and the record was not packaged. | **Fixed.** Attempt 2's record (274dccc to 2ead5cf, security files only, disjoint from the candidate) is archived and hashed at `evidence/r1-lane-attempt2/rebased.json`. The r1 attempt history below names attempt 2 as the attempt that moved the worktree. The r2 lane of record has a `rebased.json` only if it moved the worktree itself. |
| Q1 (LD-D3B0-1) | Accepted | Kept. D3b-1 moves the sampler and confirm callers to the bounded API and removes `group_members`. |
| Q2 (LD-D3B0-2) | Accepted | Kept. D3b-1 carries the `Io` errors into the per-pid evidence. |

This unit implements sub-unit D3b-0 of the D3b plan r3 (`../d3b/PLAN-r3.md`, accepted by Codex `codex-d3b-plan-r3`). It adds the mechanisms item 18's macOS descendant step needs, in D1a's own module, `crates/platform/src/process.rs`.
- **No policy.** Each mechanism holds no policy (process.rs:1-4). The walk, its bound (item 18's four times the class's process count), the eligibility of each target, the confirm and every outcome's meaning belong to D3b-1.
- **Library only:** no production caller. D3b-1 composes these.
- **No new path:** no inventory successor.
- **No census-closure file is changed.**

**Base:** the product main that the lane of record ran on, recorded as `productBase` in `evidence/d3b0-checks-r2/checks.json`. Round 1 was written on `d704ed4` (D3a-3, inventory v227, S-OP-2c), and r1's attempt 2 moved the worktree onto `2ead5cf` (`evidence/r1-lane-attempt2/rebased.json`). The runner moves the worktree onto main inside the lane lock only when every change since its base is disjoint from the candidate's paths. A move made by the r2 lane of record is recorded in its own `rebased.json`.

## What it changes

| File | Change |
| --- | --- |
| `crates/platform/src/process.rs` | **Shared types**, at module level so the other targets' stubs use them too:<br>• `Listing {Complete(Vec<i32>), Exceeded}`: a bounded pid listing (LD-D3B-3);<br>• `ProcessIdentity {pid, pgid, start_seconds, start_micros}` (its pid accessor is `process_id()`, since `pid(` is a mint-census member), with private fields, made only by `process_identity`. Its `same_process` compares the pid and the start time for **equality only**; start times are never compared for order (RF-4). A `cfg(test)` constructor serves the changed-identity and protected-pid controls;<br>• `KillOutcome {Sent, IdentityChanged, Exited, Refused(Protected)}`. `Sent` means `kill` returned 0, not that the process died;<br>• `Protected {Root, InitOrGroup, Host, AfterReap}` (Q9);<br>• `LaunchError::ListingCapacity(usize)`, for a capacity whose buffer does not fit the call's `int`.<br>**`child_processes(pid, capacity) -> Result<Listing, LaunchError>`** calls `proc_listchildpids`, which returns a pid **count** (SDK27 `libproc.h`:95; CFP:224, confirmed on this host), into one buffer of `capacity + 1` slots. Filling the buffer gives `Exceeded`. Zombie children are listed too.<br>**`group_members_bounded(group, capacity) -> Result<Listing, LaunchError>`** calls `proc_listpids(PROC_PGRP_ONLY)`, which returns **bytes**, into the same kind of buffer.<br>**`process_identity(pid) -> Result<Option<ProcessIdentity>, LaunchError>`** calls `proc_pidinfo(PROC_PIDTBSDINFO)` for `pbi_pgid`, `pbi_start_tvsec` and `pbi_start_tvusec`. It gives `None` on `ESRCH`, which covers no such process and also a zombie, whose BSD info the kernel no longer reports (observed on this host). Any other failure is `Io {call: "proc_pidinfo"}`.<br>**`Child::kill_descendant(&self, &ProcessIdentity) -> Result<KillOutcome, LaunchError>`**, on the owned child (Q9).<br>• **Before any read,** it refuses: once the root is reaped (`AfterReap`); this child's own root (`Root`, since the root is signalled only through its group, item 4); pid ≤ 1, which is init or a pid `kill` reads as a group (`InitOrGroup`); and the host's own pid (`Host`).<br>• **Then** it rereads the identity. `None` gives `Exited`; an unequal pid or start time gives `IdentityChanged`, with no `kill` made. On equality it calls `kill(pid, SIGKILL)`: 0 gives `Sent`, `ESRCH` gives `Exited`, and any other errno is `Io {call: "kill"}`.<br>• **The race.** Between the reread and the send, the pid could in principle be reused within the same start time. That is item 18's stated best effort (:602), and the doc comment says so.<br>**Test seam:** `SYSCALLS` records `kill` where it is made.<br>**The other targets' stubs** refuse with `PlatformUnsupported`. |
| `crates/platform/src/lib.rs` | Exports `KillOutcome`, `Listing`, `ProcessIdentity`, `Protected`, `child_processes`, `group_members_bounded` and `process_identity`. |
| `crates/platform/src/process_tests.rs` | Two fixture modes, `two-children` and `escapee`. Each forked child makes only async-signal-safe calls. The escapee calls `setpgid` on both sides, so it has left the group before its pid is written. The modes back six tests (below). |

## Lead decisions

- **LD-D3B0-1. `group_members` stays until D3b-1.** The plan's D3b-0 row says the bounded listing replaces D1a's unbounded doubling. The existing `group_members(group)` is called by `supervisor.rs`, by its sampler and confirm. D3a-4 and D2b-3b r2 are in flight on that file, and the coordinator holds D3b-1 and D3b-2 until both integrate. So D3b-0 **adds** `group_members_bounded` and leaves `group_members` unchanged, with a doc note. **D3b-1** moves the supervisor's callers to the bounded form and removes `group_members`. The bound is the plan's: item 18's four times the class's process count, which is components' policy. The platform invents no cap (Q1).
- **LD-D3B0-2. Call failures are `Err`, not a `KillOutcome` variant.** The plan's D3b-0 row lists `Failed(errno)` among the outcomes. This unit expresses a failed `proc_pidinfo` or `kill` as `Err(LaunchError::Io {call, error})`, which carries the errno, in the module's established style. `KillOutcome` then holds only what was observed without a call failure. The information is the same (Q2).
- **LD-D3B0-3. Pid ≤ 1 is one refusal.** `kill` reads 0 and negative pids as groups, and pid 1 is init. All three are `InitOrGroup`, refused before any read. That is the plan's "pid 1", widened to the pids for which `kill` would not target a single process.
- **LD-D3B0-4. A zombie has no identity.** `proc_pidinfo(PROC_PIDTBSDINFO)` fails with `ESRCH` for a zombie on this host (probed; `kill(zombie, 0)` still succeeds). A zombie is therefore `None`, and `kill_descendant` reports `Exited` for it without signalling.

## Checks of record

The lane runner is `evidence/run_d3b0_checks.py`, adapted from D3a-0's. Its rows are:
- the platform suite at base and candidate, serial, with equal failure sets and nine new passing tests;
- rustfmt on the edited base-clean files (all three are base-clean);
- warning-denied all-targets Clippy on platform;
- a workspace all-targets check;
- the focused D3b-0 tests;
- the environment exceptions;
- the operability source census;
- the census-closure check;
- verify_design;
- eleven mutations, each of which must fail the focused tests and not fail to compile.

**The nine tests:**
- `child_processes_counts_the_children_into_a_bounded_buffer`: the count semantics, with exactly two children. The listing is `Complete` at capacity 4 and at capacity 2, `Exceeded` at capacity 1 and 0, and `ListingCapacity` at `usize::MAX`.
- `group_members_bounded_lists_at_and_refuses_over_its_capacity`: three members are `Complete` at capacity 3 and 8, `Exceeded` at 2, and `ListingCapacity` at `usize::MAX`.
- `process_identity_reads_the_group_and_start_time`: the root's pgid is its pid; the escapee's pgid is its own; a killed escapee, which is a zombie, has no identity; nor does a reaped root.
- `kill_descendant_sends_only_on_an_equal_identity`: an identity whose start microseconds or seconds differ gives `IdentityChanged`, with no `kill` recorded and the escapee alive. The equal identity gives `Sent`, with exactly one `kill`. The zombie then gives `Exited`.
- `kill_descendant_refuses_the_root_init_the_host_and_after_the_reap`: `Root`; `InitOrGroup` for 1, 0, −1 and −pid; `Host`; no call is made for any of these. After the root's reap, the escapee gives `AfterReap`, and it stays alive.
- `a_start_time_before_the_roots_is_still_killed` (RF-4): a process spawned before the root has a lower start time and is still `Sent`. Once reaped, it gives `Exited`.
- **(r2)** `a_listing_failure_is_never_an_empty_list` (all three listings), `an_empty_listing_is_complete_despite_a_stale_errno` and `an_identity_failure_is_never_a_missing_process` (D3B0-R1-RF-1 and the self-review's item 3, above).

**The mutations:**
- the count read as bytes;
- `Exceeded` truncated to a full list;
- the group listing's capacity ignored;
- the identity equality skipped;
- a start-time order filter reintroduced (RF-4);
- the root not refused;
- the after-reap refusal dropped;
- a zombie's `ESRCH` read as an error;
- **(r2)** a listing's zero return with errno set read as an empty list;
- **(r2)** errno not cleared before a listing;
- **(r2)** `proc_pidinfo`'s zero return with errno set read as a missing process.

**Lane of record (r2):** `evidence/d3b0-checks-r2`.

**Round 2's earlier attempt.** Attempt 0 (`d3b0-checks-r2-attempt0`, kept outside the package) ran the suites, Clippy, the workspace check, the focused tests, operability, the closure check and verify_design on an earlier r2 candidate. That candidate fixed only the two bounded listings. The attempt stopped at its third mutation's anchor check, because the errno-clearing line also matched a deeper-indented line elsewhere in `process.rs`. The anchor now includes its neighbouring lines. The self-review then extended the errno discipline to `group_members` and `proc_pidinfo` before the lane of record.
Attempt 1 (`d3b0-checks-r2-attempt1`, empty) waited for the lock and then refused inside it. Main had moved to `6fab8fc` (D4-1, CI-2 and CI-3, C1b-2, and inventories v229 and v230), and CI-2 had appended a `component_tree` module declaration to `crates/platform/src/lib.rs`, a candidate path. The runner's disjointness check refused the move, as it must. The candidate was then rebased by hand: its diff re-applied cleanly on `6fab8fc`, with `process.rs` and `process_tests.rs` byte-identical, and `lib.rs` keeping CI-2's appended lines and this unit's export block. The runner now polls the lock every second instead of every five. The lane of record then moved the worktree itself, inside the lock, from `6fab8fc` to `f16f50d`. That move's changes (`crates/components/src/provider_protocol/ts2.rs`, `crates/components/src/provider_protocol/ts2/participant.rs`, `crates/components/src/provider_protocol/ts2/send.rs`, `crates/components/src/provider_protocol/ts2_send_tests.rs`, `crates/components/src/provider_protocol/ts2_tests.rs`, `crates/components/src/supervisor.rs`) are disjoint from the candidate's paths, and it is recorded in `evidence/d3b0-checks-r2/rebased.json`. The lane ran on `f16f50d`.

**Round 1's lane attempts (history).** Attempt 4 was r1's lane of record (`../d3b-0-r1/evidence/d3b0-checks-r1`). The four before it:
- **Attempts 0 and 1** stopped at the runner's opening check that main and the worktree share a base. Main had moved, by C2a-3k and then C1b-1, while the lane queued for the lock. The runner was then changed to move the worktree onto main inside the lock, when the changes are disjoint.
- **Attempt 2** made that move, from 274dccc to 2ead5cf. Its record is archived here at `evidence/r1-lane-attempt2/rebased.json` (NBO-1). It passed every row except the operability source census: `ProcessIdentity::pid()` added `pid(` calls, and `pid` is a mint-census member. The accessor became `process_id()`.
- **Attempt 3** passed every row but rustfmt. One renamed test line was too long, and a stdin `--check` had not shown it. Attempt 4 started already aligned with main, so it made no move and has no `rebased.json`.

## Self-review (the lead's pre-submission checklist, `PRE-SUBMISSION-CHECKLIST.md`)

| Item | Result |
| --- | --- |
| 1. Charge before work | **Not applicable.** D3b-0 charges nothing. Its walks are bounded by a caller-sized buffer (LD-D3B-3), not by a ledger, and the plan's round-1 "Bounds" ruling accepted that. Each listing allocates its one buffer only after the checked capacity arithmetic succeeds. |
| 2. Exact charges against bounds | **Not applicable**: no ledger charge, and no feasibility claim. |
| 3. System-call error conventions | **Applied to every call.** Two wrappers return 0 on failure: `proc_listchildpids` and `proc_listpids`, the latter in the bounded listing and in D1a's `group_members`. Both go through `native_listing`, which clears errno per call; zero with errno is `Io`, zero without errno is empty. `proc_pidinfo` returns 0 on failure: errno is cleared first, `None` is only `ESRCH`, and a zero or short return with no errno is `Io`. `proc_pid_rusage` and `kill` return -1 with errno set, and are unchanged. Every failure keeps its call name and errno. Controls: three forced real failures (`ENOMEM`), and two stale-errno presets. |
| 4. Pinned-source equality | **Not applicable**: no table or enum is taken from a schema or generated source. `PROC_PGRP_ONLY` is D1a's existing constant. |
| 5. Immutable context pins | The subject pins only this round's own files, the published D3b plan r3 and its accepted reviews, and round 1's submitted subject and reviews. |
| 6. Time and measurement provenance | **Not applicable**: no duration is measured. Start times are only compared for equality. |
| 7. Failure latching | **Not applicable**: each mechanism is a single call with no later steps. A failed listing returns at once, and its buffer is dropped. |
| 8. Disclosure | The untested paths are listed in "Untested paths" below. |
| 9. Mutations | One per applicable class: listing error read as empty, errno not cleared, identity error read as gone, and the r1 eight. Each must fail a test, not compilation. |

**Untested paths** (item 8):
- **A negative return** from either listing wrapper. This host's wrappers map -1 to 0 (Codex's disassembly), so a negative return cannot be produced. It is still handled as `Io`.
- **A zero or short `proc_pidinfo` return with no errno.** It was not producible in the probes. It is handled as `Io` (`InvalidData`), not `None`. Because no real call reaches it, the errno clear before `proc_pidinfo` has no mutation that a test could catch. The clear is defensive, and is disclosed here.
- **`kill` failing with an errno other than `ESRCH`**, for example `EPERM` for another user's process. That is `Io {call: "kill"}`, but the test user's processes cannot produce it.
- **Linux and the other targets.** Their stubs refuse, and no lane runs them.

## Not claimed

- No walk, confirm, tree report or record (D3b-1).
- No cancellation (D3b-2).
- No Linux: the stubs refuse, and D3b-L follows D1a-L.
- No production caller.
- No claim that `Sent` means death, or that equality proves ancestry.

## Questions for the reviewer

- **Q1.** Is LD-D3B0-1 acceptable? Under it, the unbounded `group_members` stays, with a removal note, until D3b-1 moves the supervisor's callers to `group_members_bounded`, given that `supervisor.rs` is held for D3a-4 and D2b-3b r2.
- **Q2.** Does LD-D3B0-2's `Err(LaunchError::Io)` for failed calls, in place of a `KillOutcome::Failed(errno)` variant, satisfy the plan's D3b-0 row?
