# D3b-0 r1: the macOS descendant mechanisms (M3-D r5 items 4, 8, 16 and 18; D3b plan r3, sub-unit D3b-0)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1.**

This unit implements sub-unit D3b-0 of the D3b plan r3 (`../d3b/PLAN-r3.md`, accepted by Codex `codex-d3b-plan-r3`). It adds the mechanisms item 18's macOS descendant step needs, in D1a's own module, `crates/platform/src/process.rs`.
- **No policy.** Each mechanism holds no policy (process.rs:1-4). The walk, its bound (item 18's four times the class's process count), the eligibility of each target, the confirm and every outcome's meaning belong to D3b-1.
- **Library only:** no production caller. D3b-1 composes these.
- **No new path:** no inventory successor.
- **No census-closure file is changed.**

**Base:** the product main that the lane of record ran on, recorded as `productBase` in `evidence/d3b0-checks-r1/checks.json`. The candidate was written on `d704ed4` (D3a-3, inventory v227, S-OP-2c). Main moved meanwhile (C2a-3k, C1b-1: security files only), so the runner moves the worktree onto main inside the lane lock, only when every change since the worktree's base is disjoint from the candidate's paths. It records any such move in `rebased.json`.

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
- the platform suite at base and candidate, serial, with equal failure sets and six new passing tests;
- rustfmt on the edited base-clean files (all three are base-clean);
- warning-denied all-targets Clippy on platform;
- a workspace all-targets check;
- the focused D3b-0 tests;
- the environment exceptions;
- the operability source census;
- the census-closure check;
- verify_design;
- eight mutations, each of which must fail the focused tests and not fail to compile.

**The six tests:**
- `child_processes_counts_the_children_into_a_bounded_buffer`: the count semantics, with exactly two children. The listing is `Complete` at capacity 4 and at capacity 2, `Exceeded` at capacity 1 and 0, and `ListingCapacity` at `usize::MAX`.
- `group_members_bounded_lists_at_and_refuses_over_its_capacity`: three members are `Complete` at capacity 3 and 8, `Exceeded` at 2, and `ListingCapacity` at `usize::MAX`.
- `process_identity_reads_the_group_and_start_time`: the root's pgid is its pid; the escapee's pgid is its own; a killed escapee, which is a zombie, has no identity; nor does a reaped root.
- `kill_descendant_sends_only_on_an_equal_identity`: an identity whose start microseconds or seconds differ gives `IdentityChanged`, with no `kill` recorded and the escapee alive. The equal identity gives `Sent`, with exactly one `kill`. The zombie then gives `Exited`.
- `kill_descendant_refuses_the_root_init_the_host_and_after_the_reap`: `Root`; `InitOrGroup` for 1, 0, −1 and −pid; `Host`; no call is made for any of these. After the root's reap, the escapee gives `AfterReap`, and it stays alive.
- `a_start_time_before_the_roots_is_still_killed` (RF-4): a process spawned before the root has a lower start time and is still `Sent`. Once reaped, it gives `Exited`.

**The mutations:**
- the count read as bytes;
- `Exceeded` truncated to a full list;
- the group listing's capacity ignored;
- the identity equality skipped;
- a start-time order filter reintroduced (RF-4);
- the root not refused;
- the after-reap refusal dropped;
- a zombie's `ESRCH` read as an error.

**Lane attempts.** Attempt 4 is the lane of record (`evidence/d3b0-checks-r1`). The four before it:
- **Attempts 0 and 1** stopped at the runner's opening check that main and the worktree share a base. Main had moved, by C2a-3k and then C1b-1, while the lane queued for the lock. The runner now moves the worktree onto main inside the lock, only when the changes are disjoint (`rebased.json`).
- **Attempt 2** (`d3b0-checks-r1-attempt2`, kept outside the package) passed every row except the operability source census. `ProcessIdentity::pid()` added `pid(` calls, and `pid` is a mint-census member. The accessor is now `process_id()`, as `Child`'s is, and the census passes with no exception change. The other rows and all eight mutations passed in that attempt too.
- **Attempt 3** passed every row but rustfmt. The rename had lengthened one test line past rustfmt's width, and a stdin `--check` the lead ran beforehand had not shown it. That line is now formatted, with no other change.

## Not claimed

- No walk, confirm, tree report or record (D3b-1).
- No cancellation (D3b-2).
- No Linux: the stubs refuse, and D3b-L follows D1a-L.
- No production caller.
- No claim that `Sent` means death, or that equality proves ancestry.

## Questions for the reviewer

- **Q1.** Is LD-D3B0-1 acceptable? Under it, the unbounded `group_members` stays, with a removal note, until D3b-1 moves the supervisor's callers to `group_members_bounded`, given that `supervisor.rs` is held for D3a-4 and D2b-3b r2.
- **Q2.** Does LD-D3B0-2's `Err(LaunchError::Io)` for failed calls, in place of a `KillOutcome::Failed(errno)` variant, satisfy the plan's D3b-0 row?
