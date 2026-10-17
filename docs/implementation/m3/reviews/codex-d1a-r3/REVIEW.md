# D1a r3 review

**Verdict: REQUIRED-FINDINGS.** The live-child detachment sequence is fixed, but the newly explicit uncertain-reap custody rule is not applied to SetupAbandoned. One required finding; one carried non-blocking observation.

## Verified subject and boundaries

Manifest `docs/implementation/m3/supervisor-d/d1a-r3-subject.json`: 8,519 bytes, SHA-256 `72708f4617b4e6ce37592f735cf483152833a01be31027b98e1682f9e50943a5`, 38 members. Rehashed every member successfully. All product-map candidate/archive rows and the existing lib.rs parent match. Main is clean at `808ad6476fb848f84e732ee233a47229370081f4`; candidate HEAD matches, with only the three declared Rust paths changed/new. lib.rs is byte-identical to the r2 candidate.

Reviewed the r2-to-r3 source/test changes against the accepted plan r2, M3-D items 1–8 and prior review dispositions. Only the permitted operability source check was executed: passed=true, zero findings, 114 rows. No Cargo, rustc, build, lane, network, delegation, other-pane access, private fixture, installation, signing keys, held trees or T2 stores were accessed. Runtime results below are pinned lane evidence, not reviewer reruns.

## Required finding

### D1A-R3-RF-1 (P2): SetupAbandoned still releases root custody without a successful reap

`crates/platform/src/process.rs:1162-1179`

The new fail-closed lifetime rule is implemented only once a Child has been constructed. After successful posix_spawn, exit_source can fail and kill_and_reap can return an error; this is the explicitly represented SetupAbandoned branch. That return drops the local ChildScratch, and root_guard has not yet been cloned. If the caller then drops ScratchRoot, no owner retains the invocation lock even though the reap result is uncertain. A sibling sweep can reclaim that root. Drop deliberately leaks its guard for the equivalent uncertain-reap outcome, so the two cleanup paths now implement different custody guarantees. This is a source-analysis finding in the represented cleanup-error branch; no real syscall failure was induced during this constrained review.

**Required:** Establish root custody for every successfully spawned process before exit-source setup, and preserve or deliberately leak that hold when setup cleanup cannot establish a reap/no-child result. Keep both errors in SetupAbandoned. A small shared guard can serve both the setup-error and Child::drop paths. Add an injected non-EINTR/non-ECHILD reap-error control for the setup-failure branch: after the error and dropping ScratchRoot, the lock must remain held and the root must not be swept. Verify the successful cleanup path still releases its hold.

## Guard lifetime and control

For a successfully returned Child, the independent Arc<RootState> resolves D1A-R2-RF-1's concrete sequence. Taking and dropping ChildScratch cannot release that guard; dropping ScratchRoot cannot release it either. A failed public reap returns before clearing it. Successful exact wait4 reaping sets reaped and clears the independent hold; an attached or detached ChildScratch continues to hold its own Arc. If Child::drop cannot complete kill_and_reap, forgetting the taken guard conservatively retains the root descriptors and flock for this process's remaining life. Forgetting a Child itself likewise retains its fields. No new unsafe block is introduced by this revision.

The intentional leak is a reasonable fail-closed choice for an uncertain cleanup outcome: the destructor cannot return an owner for later recovery, and releasing the lock would falsely signal that reclamation is safe. The process will eventually close these descriptors on termination. It must be applied consistently to the earlier setup-error path as RF-1 requires. This does not claim that a leak constitutes successful reaping or qualifies D3 supervision.

The new control establishes the requested normal lifecycle: a holding child has its scratch taken and dropped, then the original root is dropped; descriptor churn follows; a sibling sweep removes nothing, both paths still exist, and an independently opened lock cannot be acquired. Only after closing stdin, observing exit and successful reap does the sweep reclaim the root, while the Child value still exists. The child-root-guard-dropped mutant produces an actual failure in this named control. The bounded retries occur only after successful reap, allowing transient fork-to-exec inheritance to delay reclamation without relaxing the live-child assertions. Neither this control nor the sixteen mutations covers the setup cleanup returning a non-EINTR/non-ECHILD reap error.

## Other scope and evidence

- **Earlier fixes and regression surface:** the diff preserves staged, locked exclusive publication; lock-open failure retention; lock ownership through deletion; same_entry re-verification; exact CString removal names; EINTR handling; shared group/root/exact-reap cleanup; SetupAbandoned error preservation; and the forbidden-call correction. The unchanged classes, exact protocol constructors/tool gate, structural VerifiedLaunch, spawn flags, pipe mapping and host flags, dlsym fallback, core limit, kqueue/WNOWAIT, wait4 usage, reap-last guard, enumeration byte accounting and unsupported branch have no new identified regression. RF-1 concerns custody on the error branch rather than loss of either reported error.
- **Staging observation:** the comment at STAGING_PREFIX now explicitly documents unpublished crash leftovers, their lack of child execution, and the need for separately coordinated cleanup. That is an adequate disposition of r2 NBO-1 for this unit; it does not claim staging reclamation exists.
- **Lane:** seven serial platform suites on each side, 295 base versus 316 candidate passes, no failures and 21 new passes; the lib suites each retain one ignored test. Focused process suite: 21 passes. All sixteen mutation logs contain actual failed test results without compilation failure, including the new guard mutant.
- **Checks:** warning-denied all-targets Clippy, all three edited Rust-file rustfmt classifications, FW-01, environment exceptions, operability, verify_design and closure-unchanged all record success. verify_design selects inventory v212 and 173 contract successors. Independently rehashed all 19 census-closure files and compared them with Git base: every file matches, so this change does not stale the blind receipt through a closure edit.
- **Rules and limits:** the added Rust scan finds no actual from/into/pid/line/issue calls with the prohibited spellings. No new environment read or Linux claim was introduced. This remains the macOS spawn primitive, without D1b confinement, D3 supervision/cancellation, production callers, Linux qualification or overall D1 completion.
- **Inventory:** the two new paths remain crates/platform/src/process.rs and crates/platform/src/process_tests.rs; lib.rs is existing. A later inventory successor remains required.

## Non-blocking observation

### D1A-R3-NBO-1: Deterministic contested-sweep coverage remains outstanding

Carries D1A-R2-NBO-2. The current two-sweeper/creator stress test may run without forcing both sweepers to retain the same dead root and lock before one wins. Its regression value and the source protocol argument remain valid; a barrier or narrow hook would strengthen interleaving coverage. SCOPE correctly states this was not completed in r3.
