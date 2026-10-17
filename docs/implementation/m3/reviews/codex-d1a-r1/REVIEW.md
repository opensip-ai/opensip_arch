# D1a r1 review

**Verdict: REQUIRED-FINDINGS.** Five required findings; two non-blocking observations.

## Subject and verification

Reviewed manifest `docs/implementation/m3/supervisor-d/d1a-r1-subject.json`: 19,489 bytes, SHA-256 `d50ef70a21ea42d838204b4c75e3c268abcabc68674f1e1646944b03cc0229ed`. Rehashed all 85 members successfully. Candidate and archived product bytes match every product-map row; the existing lib.rs parent also matches. Product main is clean at `808ad6476fb848f84e732ee233a47229370081f4`; candidate HEAD is the same base and its only changes are the three declared Rust paths.

Read the accepted plan r2, M3-D r5 items 1–8, pinned contracts, implementation, tests, lane runner and evidence. No Cargo, rustc, build, lane, network, delegation or restricted fixture access was performed. The permitted source check ran in the candidate and returned `passed: true`, zero findings, 114 rows.

## Required findings

### D1A-R1-RF-1 (P1): Child scratch does not retain its parent descriptor or invocation lock

`crates/platform/src/process.rs:769-778,829-850; Child::take_scratch`

ChildScratch stores only ScratchRoot.root.as_raw_fd(). Neither Child nor ChildScratch borrows or owns ScratchRoot, so safe callers can drop ScratchRoot while the child or a taken scratch is alive. This closes the parent descriptor and releases the invocation flock. A sibling sweeper can then delete a running child's cwd; remove() later uses a closed or reused descriptor for unlinkat. The safety comment at line 848 is not enforced by the API.

**Required:** Make children and detached scratch values retain the owning scratch-root state, including its held parent/root descriptors and invocation lock, or enforce equivalent lifetimes. A duplicate of the root descriptor alone does not preserve the lock. Add coverage for dropping the original root while a child/taken scratch remains alive, including descriptor reuse and a sibling sweep.

### D1A-R1-RF-2 (P1): The sweep can delete a root without acquiring its lock and releases acquired locks before removal

`crates/platform/src/process.rs:721-750,796-820`

When openat(lock) fails for any reason, sweep falls through to remove_tree. A concurrent creator publishes its opensip-scratch-* directory before creating/locking its lock file, so a sweeper can remove a live root during that window. Permission and other open failures also do not establish a dead owner. On success, lock_fd is dropped at the end of the if block, before remove_tree/unlinkat, allowing another sweeper to enter the same deletion concurrently.

**Required:** Define a creation/publication and sweep protocol that never treats absence or failure to open a lock as proof of death, handles the create-before-flock window, and keeps the acquired lock alive through deletion of the root. Cover concurrent creation versus sweep and two concurrent sweepers with controlled interleavings.

### D1A-R1-RF-3 (P2): Last-resort reaping ignores interrupted waits

`crates/platform/src/process.rs:1039-1046,1229-1242`

Both failure cleanup and Child::drop call blocking waitpid only once and ignore its result. A caught signal whose handler does not restart waits can produce EINTR before the SIGKILLed child becomes waitable. Drop then marks reaped=true and discards the child handle although no reap succeeded, leaving a zombie. The existing normal-exit tests do not exercise this path.

**Required:** Use a shared exact-pid reap helper that retries EINTR and distinguishes successful reap, ECHILD, and other failures; do not infer successful reaping merely because waitpid was called. Preserve the no-wildcard and reap-last rules. Provide an interruption control for cleanup.

### D1A-R1-RF-4 (P2): Exit-source setup failure kills only the root and can orphan its group

`crates/platform/src/process.rs:1037-1046`

After successful posix_spawn, exit_source may fail, for example when kqueue cannot allocate a descriptor. The child can already have forked a descendant. This branch kills only process_id and reaps it, unlike Drop, which first kills the unreaped root's group. Descendants in that group can survive after spawn returns Err, with no Child handle available to clean them up.

**Required:** On post-spawn setup failure, kill the reserved child group before reaping the root, retain the direct-root fallback, and use the robust exact-pid reap helper. Cover an injected exit-source failure with a child that has created a descendant. This is primitive error cleanup, independent of D3 supervision policy.

### D1A-R1-RF-5 (P2): The new test helper introduces a prohibited from( call

`crates/platform/src/process_tests.rs:139`

open_dir introduces OwnedFd::from(File::open(path).unwrap()). Request item 5 explicitly prohibits new from( calls and supplies no test-only exception. Passing FW-01 does not establish compliance with this separate rule.

**Required:** Replace this conversion using an allowed ownership-preserving spelling, and rescan all added/changed Rust code for the six prohibited call names. Preserve unique descriptor ownership.

## Assessment of the remaining requested checks

- The closed classes, test-only fixture class, crate-internal tool constructor, fixed TS/Rust argv and environments, absolute/NUL validation, and structural VerifiedLaunch boundary follow plan r2. VerifiedLaunch remains the accepted D4 handoff, not an independent digest verifier.
- The normal macOS spawn path uses posix_spawn by absolute path, the four required flags, all-default signal set, empty mask, and soft core limit zero. Child pipe ends are moved above the destination slots; host ends receive the required flags and write-end F_SETNOSIGPIPE. Attribute/action RAII, argv/env buffers, descriptor transfer, fdopendir ownership, and the typed dlsym signatures have no additional identified FFI defect. The scratch parent-lifetime claim is specifically defective as RF-1 explains.
- Exit observation uses kqueue and WNOWAIT; normal final reap uses exact-pid wait4 with rusage. The public group-signalling guard refuses calls after successful reap, and proc_listpids is interpreted as bytes. Error cleanup needs RF-3 and RF-4.
- The 15 tests cover the planned normal macOS controls, including exact profiles, session/group/cwd/fds, concurrent inheritable descriptors, environments, unrepaired Rust runtime signal exceptions, inherited SIGUSR1/SIGUSR2 controls, direct F_GETNOSIGPIPE probes, and the forced _np fallback. Their success does not cover the lifetime, concurrent-sweep or failure-cleanup cases above. All twelve mutation logs contain actual failing test results and no compilation failure.
- Attempt 3 is a reasonable lane of record: both sides use the same serial platform suite after the recorded base parallel-test interference. Its seven suites report 295 base versus 310 candidate passes, no failures, and one ignored lib test on each side. Attempts 1/2 preserve the differing path-binding failures/IO-safety abort history; the base-flakiness note records three serial passes. This supports a serial-lane claim, not a claim that parallel interference has been fixed.
- Recorded warning-denied all-targets Clippy, all three edited-file rustfmt classifications, FW-01, environment-exception checks, verify_design, and operability pass. verify_design selects inventory v212 and 173 contract successors. Census closure reports 19 files with no intersection with the changed paths; the source census remains 114 rows. The unchanged census is the accepted LD-D1A-5 result, not evidence of supervision qualification.
- No new production environment read was identified; test fixture reads are explicit test instrumentation. The forbidden-call scan finds RF-5 (the other lexical match is a comment). Linux is explicitly not built/run or qualified; the non-macOS implementation returns PlatformUnsupported. No Linux acceptance or overall D1 completion is inferred.
- The two new paths requiring a later inventory successor are crates/platform/src/process.rs and crates/platform/src/process_tests.rs. lib.rs is an existing path.

## Non-blocking observations

### D1A-R1-NBO-1: Package metadata retains obsolete descriptions

SCOPE.md says both that lib.rs is clean/formatted and that it is not clean/not reformatted; attempt-3 rustfmt-classification.json establishes baseClean=true and candidateClean=true. source.json and the runner docstring still name plan r1, the runner docstring says ten mutations, and source.json says publicApiAdded=false despite new public re-exports. The manifest and request identify the actual reviewed bytes and authority, so these are editorial observations; reconcile them in the successor package.

### D1A-R1-NBO-2: Directory traversal converts names lossily

process.rs:880 converts readdir bytes with String::from_utf8_lossy, then reconstructs syscall names from that string. A byte name outside UTF-8 would no longer identify the same entry and could prevent cleanup. No such filename was created or filesystem capability tested in this read-only review. Prefer retaining C/OsString bytes throughout traversal, or document and establish the supported scratch filesystem restriction before claiming byte-exact cleanup.
