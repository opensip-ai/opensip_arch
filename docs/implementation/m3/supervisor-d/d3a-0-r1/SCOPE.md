# D3a-0 r1: the supervisor's platform mechanisms (M3-D r5 items 4, 16, 18 and 20; D3a plan r4, sub-unit D3a-0)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.**

It implements sub-unit D3a-0 of the D3a plan r4 (`../d3a/PLAN-r4.md`, accepted by Codex `codex-d3a-plan-r4`, with the LD-D3A-17 amendment): the mechanisms D3 needs in D1a's own module, `crates/platform/src/process.rs`. **Each holds no policy** (process.rs:1-4): the ceilings, the timeouts, the limits and what each outcome means are D3a-1 to D3a-3's.
- **Library only:** no production caller.
- **No new path:** no inventory successor.
- **No census-closure file changed.**

**Base:** product main as the subject manifest names.

## What it changes

| File | Change |
| --- | --- |
| `crates/platform/src/process.rs` | **`Child::try_reap(&mut self) -> Result<Option<Reaped>, LaunchError>`** (LD-D3A-14): `wait4(pid, WNOHANG)`, retried only on `EINTR`. It never blocks. `None` leaves the child unreaped, with its pid and group id still reserved. `reap` and `try_reap` share one settlement (`settle_reap`).<br>**`Child::abandon(self) -> Unreaped`** (LD-D3A-14; item 18's reap ceiling): the host never signals or reaps the root again. `Unreaped` keeps the scratch-root hold (`root_guard`), any attached scratch and the pid for the record. **Its `Drop` neither signals nor blocks**: it keeps both holds for the process's life, as D1a keeps an unreapable child's (D1a r2 RF-1). `Drop for Child` does nothing for an abandoned child.<br>**The bounded scratch walks** (LD-D3A-12; items 16 and 20), replacing `ChildScratch::remove`'s recursive `remove_tree` over `list`'s whole `Vec`:<br>- `ChildScratch::measure(&self, byte_limit, &mut WorkScope) -> Result<u64, _>` sums every non-directory entry's own `st_size` (a link's own length, never its target's) and stops once the sum passes `byte_limit`;<br>- `ChildScratch::remove_bounded(self, &mut WorkScope) -> Result<(), _>` removes everything below the scratch, then the scratch.<br>Both walk iteratively under held descriptors: a stack of open directories, each read through a stream over its own duplicate; `fstatat(AT_SYMLINK_NOFOLLOW)`; `O_NOFOLLOW | O_DIRECTORY` opens; `unlinkat`. **No listing is collected whole**: a name is copied into a stack buffer, and only an entered directory's name is kept. **Every read, status read, descent and unlink is charged to the caller's `WorkScope` before it is made**, at published costs (`READ_COST`, `STATUS_COST`, `UNLINK_COST`, `descend_cost`, `leaf_cost`). Removal re-reads a directory after any pass that removed something, until a pass finds it empty, so it never depends on `readdir`'s behaviour under concurrent unlinks. **Exhaustion** is the ledger's `Budget` failure, with no errno. **An I/O failure** is `LaunchError::Io {call, error}`, with that call's actual errno. Either leaves the rest in place. D3 maps them to `retained {reason: work-exhausted}` and `retained {reason: io-failure, errno}` (LD-D3A-17).<br>**`resident_bytes(pid) -> Result<u64, LaunchError>`** (LD-D3A-8): `proc_pid_rusage(RUSAGE_INFO_V0)`'s `ri_resident_size`, for the root and the members that `group_members` lists.<br>**`LaunchClass::TestFixture` and `LaunchSpec::fixture`** are now `cfg(any(test, feature = "test-fixture"))`, and `fixture` is `pub` (LD-D3A-9). `ChildEnvironment::fixture` stays `cfg(test)`: the feature exposes only the launch.<br>**Test seams** (`cfg(test)`): `SYSCALLS` records each signal and reap call where it is made; `WALK_LOG` records each walk call where it is made, priced by `scratch_cost`. The other targets' stubs refuse with `PlatformUnsupported`. |
| `crates/platform/src/lib.rs` | Exports `Unreaped` and `resident_bytes`. A `compile_error!` refuses the `test-fixture` feature in any build without debug assertions, as `crash-matrix` and operability's `test-mints` are refused. |
| `crates/platform/Cargo.toml` | The `test-fixture` feature: never a default, enabled only from a dependent's dev-dependencies. |
| `crates/platform/src/process_tests.rs` | Six tests (below). D1a's taken-scratch test now removes through `remove_bounded`. |

## Lead decisions

- **LD-D3A0-1. The stale-root sweep keeps D1a's walk.** `ScratchRoot::sweep` (item 6) still removes a dead sibling root through `list` and `remove_tree`. The plan's replacement is scoped to `ChildScratch`'s removal (LD-D3A-12, the RF-4 row), which D3 owns at settlement. The sweep is item 6's, runs before any child, and has no supervision budget to charge. Bounding it is item 6's owner's question and is not claimed here.
- **LD-D3A0-2. What the measure counts.** Item 16 bounds a child's scratch "with an exact bounded walk" (:551), and RPP:118 gives the limit in bytes. The walk counts each non-directory entry's own `st_size`. That is a regular file's length, a link's own length (never its target's, since links are not followed), and 0 for special files. Directories count nothing. Allocated blocks are not counted: a sparse file counts its length.
- **LD-D3A0-3. The walk's descriptor depth.** Each entered directory holds one descriptor and one stream until it is finished, so nesting deeper than the process's descriptor limit refuses with `EMFILE`. That is an I/O failure with its errno, and D3 settles it as `retained {reason: io-failure}`. The work bound is the caller's ledger, the discovery profile under LD-D3A-12; the descriptor limit is not a second policy.
- **LD-D3A0-4. The ceiling control.** No fixture can survive `SIGKILL`. So the D3-T3 qualification for a root that survives the ceiling (R2-NBO-2) is exercised at the mechanism the ceiling takes: a **live** child is abandoned. Destroying the `Unreaped` then makes no signal or reap call (the `SYSCALLS` seam), the child still runs, and its root hold survives the root's own drop, so a sibling sweep keeps the root. D3a-1 adds the timed ceiling around it.

## The tests

- **The non-blocking reap:** before the exit, `try_reap` returns `None` within 2 s, as exactly one `wait4(WNOHANG)`, with the child alive and unreaped. A watchdog releases the child after 5 s, so a blocking reap would return late with `Some`. After the exit, `try_reap` gives the exit source's status. A second call is `AlreadyReaped`.
- **The abandoned root:** abandoning a live child and dropping the `Unreaped` make no signal or reap call. The child still runs, and the hold keeps the root through the root's drop and a sibling sweep.
- **The measuring walk**, over 300 empty files, a 1,000-byte file, a 40-deep chain with a 5-byte leaf, and links out of the scratch to a file and a directory:
  - the exact total (link lengths included, targets never entered);
  - the ledger's charge equal to the price of the recorded calls, with the calls' counts derived from the tree: one descent per directory and the root; one status per entry; one read per entry plus three per directory;
  - the limit: at the total, the exact total; one byte under, a stop past it; over 20 one-byte files at limit 0, exactly one status read;
  - exhaustion as `Budget`;
  - the link targets untouched.
- **The removal walk** over the same tree: everything removed, the targets untouched, and the charge equal to the recorded calls' price, with one unlink per entry and one for the scratch itself.
- **The removal failures:** exhaustion is `Budget`, leaving the scratch. A read-only directory's entry is `Io {call: "unlinkat(scratch)"}` with errno `EACCES`, leaving the entry.
- **The sampler:** resident bytes of the root and of a forked group member (both listed by `group_members`), and `Io {call: "proc_pid_rusage"}` for no such process.

## Checks

Lane r1, attempt 3, `evidence/d3a0-checks-r1/` (the lane of record), on main `23b3871` (the v218 lock), passed every check (`allPassed`):
- **Attempt 1** (`evidence/d3a0-checks-r1-attempt1/`, on `3e70bbf`) passed the suites (platform 0 = 0 failures, 6 new), every repository check and all six mutations, but failed warning-denied Clippy on one test line: `drop` of a `Copy` value (the watchdog's `recv_timeout` result). It is now `.unwrap_or_default()`.
- **Attempt 2** (`evidence/d3a0-checks-r1-attempt2/`) aborted the candidate platform suite in parallel with the pre-existing `IO Safety violation: owned file descriptor already closed`, which D1a's lane avoids by running this suite serially. The runner now runs it serially too (`SERIAL`).

The checks:
- **the platform suite**, serially, at base and candidate: 0 failures each side, 321 → 327 passing (6 new);
- **warning-denied all-targets Clippy** on platform, and a **workspace all-targets check** (no dependent broken by the `ChildScratch::remove` replacement);
- **rustfmt** on the edited base-clean files;
- **the focused process tests**, serially;
- **the `test-fixture` feature:** a debug `cargo check` with it passes, and a release build with it is refused by `lib.rs`'s `compile_error!`;
- **repository checks:** the environment exceptions, the operability source census, the census-closure check (no closure file changed) and verify_design;
- **six mutations,** each failing the process tests: `try_reap` blocking (`WNOHANG` removed); `Unreaped`'s `Drop` reaping; an abandoned `Child`'s `Drop` still killing; the walks following links; a status read uncharged; the measure ignoring its limit.

## Not delivered

- **D3's policy:** the reap ceiling and `exit: unreaped`, the scratch byte limit and cause `scratch-bound`, the `retained` settlement and its event, the memory ceiling and the 250 ms sampling. These are D3a-1 to D3a-3's.
- **The sweep's bounding** (LD-D3A0-1).
- **Linux** (LD-D3A-1, as D1a).

## Not claimed

- No caller, no supervision and no qualification.

## Inventory

No new path. The edited paths are inventoried already.
