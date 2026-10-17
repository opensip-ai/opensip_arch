# D1a r4 review

**Verdict: ACCEPT-UNIT.** D1A-R3-RF-1 and the carried D1A-R3-NBO-1 are resolved. No required findings or new non-blocking observations.

## Subject and verification

Manifest `docs/implementation/m3/supervisor-d/d1a-r4-subject.json`: 8,995 bytes, SHA-256 `f9baf21cebceb4add0396b5431f94f70c59f1da60cdee51d949d68b3319e954c`, 40 members. Every member was rehashed successfully. All product-map candidate/archive rows and the existing lib.rs parent match. Product main is clean at `808ad6476fb848f84e732ee233a47229370081f4`; candidate HEAD matches, with only the three declared Rust paths changed/new. lib.rs is unchanged from r3.

Reviewed the r3-to-r4 implementation/test changes, their surrounding cleanup and ownership paths, the runner, mutation definitions and pinned lane evidence against the accepted D1a plan r2, M3-D r5 items 1–8 and prior review dispositions.

Only the permitted operability source check was executed in the candidate: passed=true, zero findings, 114 rows. No Cargo, rustc, build, lane, network, delegation, other-pane access or restricted fixture/installation/key/held-tree/T2-store access was performed. Runtime results below are archived evidence, not reviewer reruns.

## Uncertain-reap custody

The setup-failure branch now forgets its local ChildScratch if kill_and_reap returns an error. ChildScratch owns an Arc<RootState>, so the root and parent descriptors, invocation lock and scratch descriptor remain held for the process's lifetime. SetupAbandoned still returns both errors. This supplies the same conservative custody guarantee as Child::drop forgetting its independent root_guard after unsuccessful cleanup; retaining an additional scratch descriptor on the setup path does not weaken it.

The ownership paths are consistent:

- Before a successful spawn, normal error cleanup may release scratch because there is no child.
- After successful spawn and during exit-source setup, local scratch retains root custody. Failed setup releases it only after successful cleanup, including the accepted ECHILD/no-child result; uncertain cleanup now retains it deliberately.
- A returned Child owns its independent guard, even after scratch is taken and dropped. A failed public reap retains it. Successful exact wait4 reaping releases that guard while any remaining ChildScratch retains its own hold.
- Drop releases ordinary ownership after successful cleanup and deliberately retains the independent guard after an uncertain result.

No additional ordinary safe ownership sequence was identified that releases this custody while the child remains live or its cleanup remains uncertain. The deliberate leak is an appropriate fail-closed choice for the modeled unreapable outcome; it is not a claim of successful reaping.

FAIL_REAP first performs the real exact reap, then changes its reported result to an error. It is test-only and enters the same production Err branch as a genuine cleanup error; a genuine earlier error is preserved by Result::and. Reaping first avoids leaving a child behind while testing the caller's response to an uncertain result. The new control drops ScratchRoot, churns descriptors, verifies that a sibling sweep removes nothing and independently verifies the lock remains unavailable. The abandoned-scratch-released mutant fails that exact control. Earlier successful-reap controls continue to establish eventual reclamation.

## Forced interleavings

SCRATCH_HOOK and its three points are test-only and thread-local. Channel synchronization now forces the previously outstanding cases:

- B opens the dead root's lock and pauses. A acquires it and deletes the root. B then locks the old, unlinked file; re-verification prevents a second removal.
- A acquires the lock and pauses before re-verification/removal. B cannot acquire it and leaves the root intact. A then removes it once.
- A creator pauses with its staged root already locked. A sweep ignores that unpublished name. After publication, the creator's retained lock prevents reclamation.

The sweep-not-reverified mutant fails the named contested-sweeper control. These controls resolve the carried observation; the earlier stress test remains supplementary coverage. The documented pre-publication staging leftovers remain a separately coordinated cleanup limitation, not a claim that such cleanup has landed.

## Regression and lane

The production delta is the uncertain-setup scratch retention; other additions are test-only seams/hooks. No new production unsafe block or FFI argument/ownership change was introduced. The prior closed classes, exact protocol constructors and tool gate, structural VerifiedLaunch boundary, spawn attributes, pipe mapping and flags, dlsym fallback, core limit, exit observation, exact waits, reap-last rule, group enumeration, staged publication, locked no-follow sweep and unsupported branch retain their earlier dispositions.

Pinned r4 evidence establishes:

- Seven serial platform suites per side: 295 base versus 319 candidate passes, no failures and 24 additional passing tests. The focused process suite has 24 passes; both lib suites retain one ignored test.
- All eighteen mutations produce actual failed test results without compilation errors. Both new mutations fail their intended named controls.
- Warning-denied all-targets Clippy, rustfmt for all three edited Rust files, FW-01, environment exceptions, operability source, verify_design and closure-unchanged checks pass. lib.rs is also rustfmt-clean at base. verify_design selects inventory v212 and 173 contract successors.
- Independently rehashed all 19 census-closure files and compared them with Git base; all match. The candidate has no closure intersection, so it does not stale the blind receipt through a pinned closure change.

The added Rust scan finds no prohibited from/into/pid/line/issue calls. No new environment read or Linux claim was introduced.

Acceptance covers this macOS spawn-primitive unit only. D1b confinement, D3 supervision/cancellation, production callers, the Linux half and overall D1 completion remain outside this acceptance. The two new paths, `crates/platform/src/process.rs` and `crates/platform/src/process_tests.rs`, still require the subsequent inventory successor; lib.rs is existing.
