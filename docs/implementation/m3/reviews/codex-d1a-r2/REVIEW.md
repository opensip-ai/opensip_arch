# D1a r2 review

**Verdict: REQUIRED-FINDINGS.** One remaining required finding, completing the live-child part of round-1 RF-1. Two non-blocking observations.

## Subject and verification

Rehashed the manifest: 15,127 bytes, SHA-256 `83551ba384edb7f6339f8d36ff31055b93b671ed92909b97ddf8189a92cc80bf`, and all 66 members: every size/hash matches. All product-map candidate and archived bytes match; the existing lib.rs parent matches too. Product main is clean at `808ad6476fb848f84e732ee233a47229370081f4`; candidate HEAD is the same base and its only changes are the three declared Rust paths.

Reviewed the r2 changes against the r1 archived implementation/tests, prior findings, accepted plan r2 and M3-D items 1–8. The SDK 27 declaration confirms renameatx_np's five arguments and unsigned flags; RENAME_EXCL is 0x00000004, available since macOS 10.12. No new unsupported symbol-version requirement was introduced by this call.

The permitted operability source check was executed in the candidate: passed=true, zero findings, 114 rows. No Cargo, rustc, build, lane, network, delegation, other-pane access or restricted fixture/installation/key/held-tree/T2-store access was performed. Runtime test results below are pinned lead evidence, not fresh executions by this reviewer.

## Required finding

### D1A-R2-RF-1 (P2): Taking scratch before reap can still release a live child's invocation lock

`crates/platform/src/process.rs:1044-1052,1274-1275; process_tests.rs:a_child_keeps_its_scratch_root_and_lock_after_the_root_is_dropped`

The Child retains RootState only through scratch: Option<ChildScratch>. take_scratch unconditionally takes that option, including while the child is running. The safe sequence spawn a holding child; take_scratch; drop the taken scratch; drop ScratchRoot leaves the live Child with no Arc<RootState>. The root descriptors and invocation lock are released, and a sibling sweep can delete the running child's scratch/cwd. Arc fixes the dangling descriptor in a retained ChildScratch, but it does not enforce the promised live-child lifetime after detachment. The new test takes scratch only after reap, so misses this sequence.

**Required:** Have Child retain its own root-state guard independently of the detachable scratch until the child is reaped/dropped, or refuse scratch detachment until the required child lifetime has ended. Add a control that takes and drops scratch while a holding child is still live, drops the original root, and verifies that the sibling sweep cannot reclaim that live invocation. Then complete cleanup and establish eventual reclamation. This completes the remaining part of D1A-R1-RF-1.

## Round-1 disposition

- **RF-1: partially resolved.** Shared RootState owns the parent/root descriptors and invocation lock; a retained ChildScratch safely keeps them alive, and remove uses that owned root. Dropping the original ScratchRoot with scratch still attached is safe. Unconditional detachment leaves the live-child hole above.
- **RF-2: resolved for published roots.** Staging names do not match the sweep prefix. Lock creation/acquisition precedes exclusive publication. A failed lock open or acquisition keeps the root. A successful sweeper retains the lock through recursive removal and root unlink. A second sweeper either fails acquisition, cannot open the removed lock, or acquires an old descriptor after the winner releases it and fails same_entry because the lock/root entry is gone. Creators publish while holding their lock, so cannot be mistaken for dead owners. same_entry uses no-follow fstatat and fstat on live owned descriptors; its valid buffers and device/inode comparison introduce no identified FFI ownership defect. Concurrent arbitrary replacement by an external same-user actor is not established as a solved threat model by these tests.
- **RF-3: resolved.** reap_exact uses one common result/error match for both injected and real waitpid results. EINTR continues that loop; exact-pid success returns the status; ECHILD returns nothing remaining to reap; other errors propagate. wait4 retries EINTR as well. Drop marks reaped only when the helper succeeds. The injected three-interruption test consumes all three injections and independently verifies ECHILD afterward; the no-retry mutant fails it.
- **RF-4: resolved.** Both setup failure and Drop call kill_and_reap: group SIGKILL while the root is reserved, direct-root fallback, then exact reap. SetupAbandoned retains setup and reap errors if both fail. The injected setup failure waits for a descendant to be created; the test requires its published pid and eventual disappearance. The root-only mutant fails. This is evidence of primitive group cleanup, not qualification of D3 tree supervision.
- **RF-5: resolved.** The helper transfers unique descriptor ownership with into_raw_fd/from_raw_fd. The forbidden six call spellings introduce no remaining actual calls in the added Rust; the pid wording in a comment is not a call.
- **NBO-1/NBO-2: resolved.** Package/runner metadata now describe plan r2, fifteen mutations, formatted lib.rs and public API additions consistently. list returns CString names and removal uses the exact bytes. The remaining lossy conversion is only the returned diagnostic name after deletion, not a filesystem operand.

## Tests, regression surface and lane

The five added tests cover root/scratch retention in the tested lifecycle, unopened/unreadable locks, concurrent sweep/create stress, interrupted Drop reaping and post-spawn group cleanup. The root-retention test's bounded probe/sweep retries occur only after the last intended owner has dropped. Allowing fork-to-exec descriptor inheritance to delay final reclamation is sound: persistent retention still fails within the bound, while the live-child and taken-scratch checks remain immediate. These retries do not cover or repair premature scratch detachment (RF-1).

The unchanged normal-spawn surface retains the closed classes and protocol-specific constructors/tool gate, structural VerifiedLaunch, absolute-path posix_spawn, SETSID/CLOEXEC_DEFAULT/SETSIGDEF/SETSIGMASK, high child pipe sources, host descriptor flags/F_SETNOSIGPIPE, typed dlsym addchdir fallback, checked zero soft core limit, kqueue/ WNOWAIT observation, exact wait4 usage, post-reap group-signalling refusal, proc_listpids byte accounting and explicit unsupported branch. The changed FFI paths retain owned descriptor lifetimes, initialized buffers and syscall argument types; no additional soundness defect was identified. No new production environment read or Linux qualification claim was found.

Attempt 2 is the correct r2 lane of record. All checks were rerun after attempt 1's sole operability failure on a discarded cleanup result. Archived attempt-2 evidence establishes:

- Seven platform suites on each side, serially: 295 base passes versus 315 candidate passes, zero failures, twenty added passes; one ignored lib test per side. Focused process suite: 20 passes.
- Warning-denied all-targets Clippy passes. All three edited Rust paths are rustfmt-clean; lib.rs is also clean at base.
- FW-01, environment exceptions, operability source, verify_design and closure-unchanged checks pass. verify_design selects inventory v212 and 173 contract successors.
- All fifteen mutation logs contain actual failed test results, with no compilation failure. The three new mutations specifically fail the interrupted-reap, root-only setup cleanup and missing-lock controls.
- Independently rehashed all 19 census-closure files and compared them with the candidate Git base; all match. The candidate change set has no closure intersection, so it does not stale the blind receipt through a pinned closure change.

The two new paths remain crates/platform/src/process.rs and crates/platform/src/process_tests.rs, for a subsequent inventory successor. lib.rs is existing. Acceptance here would be limited to this macOS primitive; no caller, D1b confinement, D3 supervision, Linux half or overall D1 completion is established.

## Non-blocking observations

### D1A-R2-NBO-1: Staging directories have no crash-reclamation path

Creation now correctly locks before publishing, but a crash or failure before rename leaves .opensip-scratch-staging-* outside the sweep's opensip-scratch-* prefix forever. These unpublished directories cannot yet contain a launched child's source scratch, so this does not block the current ownership/concurrency correction. Document their disposition or add a separately coordinated staging cleanup; simply sweeping staging names would reintroduce a creator race.

### D1A-R2-NBO-2: Concurrency test does not force both sweepers to the contested interleaving

The two-sweeper/creator stress test is useful and the source protocol handles competing acquisitions, but scheduling may serialize all sweeps and creations. A barrier or narrow test hook could make both sweepers retain the same dead root/lock before the winner removes it, and exercise publication while a creator holds its staged lock. This would strengthen regression coverage without changing the production protocol.
