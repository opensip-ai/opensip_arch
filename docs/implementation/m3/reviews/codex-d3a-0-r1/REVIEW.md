# D3A-0-r1 review

**Verdict: REQUIRED-FINDINGS.** One required finding; no non-blocking observations. The recorded lane passes, but both bounded walks perform directory acquisition before their work charge.

Subject manifest SHA-256: `5dc0f5cf0da5217797561fb634e506b199ce0314c4c15085d58e36fba15abc90` (17,409 bytes). Rehashed all 75 members successfully. All four worktree candidates, archived copies and parent pins match product-map.json at base `23b3871269c6553c96097084dd412b3aa95dec68`. The candidate remains detached at that base, with exactly the four declared edited paths and no new paths. Authority and product-lock pins verify.

## Required finding

### D3A0-R1-RF-1 — Charge descent before the directory open/duplicate

**Location:** `crates/platform/src/process.rs:1006`, `:1018`, `:1044`, `:1053`, and the charge at `:1218`.

Both walks call `enter` with an already acquired OwnedFd. At the root, Rust evaluates `dup(self.dir.as_raw_fd())?` before entering the function. At each child directory, `open_entry(dir, entry)?` runs first. Only then does enter charge descend_cost. That cost expressly includes the no-follow open, or the root's descriptor duplicate, and LD-D3A-12 requires every opened directory to be charged before the operation.

For a concrete initial case, WorkLedger::with_limits permits objects=1, but the root descent costs three objects. Both walks nevertheless attempt fcntl(F_DUPFD_CLOEXEC) before refusing Budget. The same problem occurs at a nested descent when earlier reads/status checks fit but the descent does not: openat executes before its guard. If that call returns EACCES or EMFILE, the walk returns an I/O failure without even reaching the required work charge. Descriptor exhaustion is an appropriate I/O result for a funded descent; it must not bypass the preceding budget decision.

The successful-run charge-equality tests do not establish ordering. WalkCall::Descend is logged inside enter after the charge, so it also misses the acquisition already attempted by the caller. The status-charge mutation tests a different charge site.

**Required correction:** charge the complete descent once, before the initial duplicate and every child open in both walks. Move descriptor acquisition inside the charged helper, or supply it as a deferred operation. Retain the existing I/O call and errno for funded operations. Add call-site observations for the acquisition syscalls and initial/nested insufficient-budget controls proving that Budget precedes any unfunded open or duplicate. A late-charge mutation or equivalent ordering control should fail.

## Mechanisms and lead decisions

- try_reap uses wait4 with WNOHANG, retries EINTR, returns None without settling when the child is still live, and shares settle_reap with the blocking reap. The reserved root is retained until actual reap. The watchdog control detects the blocking mutation.
- abandon transfers the root hold and attached scratch into Unreaped. Child's abandoned Drop path neither signals nor reaps; Unreaped's Drop deliberately retains the holds for the host process's life and performs no blocking reap or signal. The live-child control and syscall seam are adequate for this platform mechanism: the child remains live and the root survives its owner's drop and a sibling sweep. This does not prove a timed ceiling or an uninterruptible-kernel scenario; those remain D3's policy and later controls.
- The walks are iterative under held descriptors and stream directory entries without collecting an entire listing. Entry status is no-follow; directory opens require O_NOFOLLOW and O_DIRECTORY; links are removed as links. Removal re-passes changed directories until an empty pass, then removes the directory. Name copies and stack growth are included in the descent cost; the stack-slot term is conservative for amortized Vec growth. Read, status and unlink charges precede their operations. The descent acquisition exception is RF-1.
- LD-D3A0-2 explicitly selects the sum of non-directory entries' own logical st_size, including link text and excluding directory sizes. It does not claim allocated-block usage or follow link targets. This is a reasonable explicit measurement decision for the byte-bound mechanism. The returned over-limit value may be the full crossing entry's size; policy uses its comparison with the limit.
- LD-D3A0-3's descriptor-depth limit is a platform I/O limit, not an additional selected work policy. Funded EMFILE failures carry their errno; Budget carries none, subject to fixing the acquisition order.
- resident_bytes reads ri_resident_size through proc_pid_rusage(RUSAGE_INFO_V0). Root/member enumeration and sampling controls are recorded; aggregation, ceilings and sampling cadence remain D3's.
- The test-fixture feature exposes LaunchSpec::fixture and its class, leaves ChildEnvironment::fixture test-only, and is rejected without debug assertions. No manifest enables the feature. Its debug acceptance/release refusal are recorded. The feature changes no production launch profile.
- LD-D3A0-1 is within the accepted plan's explicit ChildScratch replacement scope. The stale-root sweep retains D1a's existing walk; bounding that pre-child sweep remains an expressly unclaimed item-6 owner question.

## Evidence and boundaries

Reviewed the package builder and lane runner as text. Attempt 3 runs the suite serially and records 321 base versus 327 candidate passes, zero failures, equal suite counts and six new tests. Thirty focused process tests pass. All three edited Rust files are base-clean and candidate-clean under rustfmt; warning-denied all-targets platform Clippy and the workspace all-targets check pass. Feature checks, ten environment-exception tests, operability, the unchanged-closure check and verify_design pass as recorded.

All six mutations produce focused test failures rather than compilation failures: blocking reap, reaping Unreaped Drop, killing abandoned Child Drop, following links, omitting the status charge and ignoring the measurement limit. These controls support their respective mechanisms but do not cover RF-1's late descent charge.

Attempt 1 is accurately disclosed as failing Clippy on dropping a Copy result; its suites and other checks pass. Attempt 2 records the parallel candidate suite's IO-safety abort, fewer completed suites and a failed comparison; it is not counted as the lane of record. Serial attempt 3 supersedes it. The suite's existing serial-run discipline is appropriate here.

The permitted live operability source check passes: 114 rows, no findings. No new mint-census call, ambient environment read or `let _ =` is introduced. No census-closure file changes. This remains macOS library mechanism work without a caller, supervision policy, Linux implementation or product qualification.

Only reading, hashing, JSON parsing, Git queries and the permitted operability command were performed. No Cargo, rustc, builds, generators or lanes ran. Neither repository, worktree nor control files was edited. Only the requested REVIEW.md and review.json were written.
