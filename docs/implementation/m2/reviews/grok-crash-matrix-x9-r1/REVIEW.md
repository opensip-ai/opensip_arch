# Law X9 r1 — the crash, lock and revocation matrix

Verdict: **ACCEPT**.

`docs/implementation/m2/crash-matrix-x9/PROPOSAL.md` is 50022 bytes, sha256 `325ccd7524c90d0611f6b4aabcd4549d5029dc7e901245cb552afcac5cd38d82`, matching `hashes.txt`. No product cargo was run. The cited product lines were read at `f1b832183c1c9fc0ef1da647945b45453061a06c`. The primary checkout's `main` is now `704251ee4e6643bb2673c3f50d191ce27059be21`. The law's baseline pin is the earlier commit, and the lines below were checked there.

## Structural premise

`cfg(test)` is set only for the crate under test. An integration target such as `crates/storage/tests/commit_tests.rs` links `opensip-security` as a normal library, so security's `cfg(test)` items are absent. At `f1b8321`, `Image::Injected` is `#[cfg(test)]` (`trust/initial_core.rs` lines 106–107), X4T-0 is `cfg(test)` in the security crate, and no `Cargo.toml` has a `[features]` table. `crates/storage/tests` does not exist. `crates/host/tests` holds fixture JSON only. That fact rules out a `cfg(test)`-only matrix and requires a feature that the matrix targets enable and release builds do not.

## Items 1 and 2

The mechanism matches EXIT-PLAN's crash-injection choice and build-plan line 1072: named points, a test feature, and a child the parent kills. The re-executed test binary already exists at `journal_store.rs` lines 1289–1291 (`current_exe()`, `--exact`, an environment marker). A separate harness binary, `fork` without `exec`, a debugger, and an SQLite VFS are the right rejections. The VFS would change the durability path L2 leaves alone.

The four guards keep the points out of a release build:

1. `compile_error` when the feature is on and `debug_assertions` is off, so `cargo build --release --features crash-matrix` fails.
2. No dependency entry names the feature. The two matrix targets opt in with `required-features`, so a plain `cargo test --workspace` skips them. A source pin in X9-0 reads the manifests.
3. The feature adds no package edge, so `check_package_edges.py` stays as it is.
4. Each run record checks that a featureless release `opensip-cli` contains neither `OPENSIP_X9_` nor a registered scope name, and that the release build with the feature fails at the compile guard.

Without the feature the macros expand to nothing. With the feature and no `OPENSIP_X9_ARMS`, a point is an unarmed `OnceLock` read and a return. That is not the rejected release-build injection surface.

## Item 3

A `held` record followed by a blocking `read(2)`, with no product code between them, and a parent `SIGKILL` only after that record, is a death at that point when `ExitStatusExt::signal()` is `SIGKILL`, the holding thread's last record is that `held`, and no later record names a durability point. A missing armed point is `HARNESS-ERROR`, never a pass. stderr records of at most 512 bytes are atomic on a macOS pipe. The 300 s watchdog kills children and records `HARNESS-ERROR` only. The source pin admits no sleep, poll, or other timed wait in the harness. The product's own fence and S7 waits still run, against a peer that does not release, so their outcome is fixed.

## Item 4

`Fault::Fail` at `f1b8321` (`carrier_append.rs` lines 294–299) is a `COMMIT` that fails without landing at `Inserted`, and a `COMMIT` that landed and reported failure at `Committed`. Item 4's `fail-before` and `fail-after` are those two outcomes, and the file-barrier, rename, and directory-barrier points use that step's native I/O error. `ObjectStep::TemporaryWrite` already writes the first half of the bytes (`project_commit.rs` line 302); `torn` is that stand-in plus a hold. `inject-id` is confined to `x3d.session.execution-draw`. `process-death`, `injected`, `mutation`, and `synthetic` stay on the record. The labels are honest: only a verified `SIGKILL` is a process death.

## Item 5

X9-0's unarmed census is the kill set: every durability point, and for a repeated protocol the first, a middle, and the last occurrence. A durability primitive outside a scope, a census point a later change removes, and a new unarmed durability point all fail the coverage check. X9-1 places points for units already integrated (X3b-1/2/4, X3c-1/2, X2d, and X4T-b if it has landed). Each later unit places its own. Existing `AppendStep`, `ObjectStep`, and commit-hook sites stay, and the new point sits at the same place. The scope names in the table are the law; the step lists are the census.

## Item 6

`crash_matrix_support` is `#[doc(hidden)]`, feature-only, and produces inputs on disk: a synthetic installation, X4T-0's signed store, a trust publication helper, the format-1 and format-2 fixture, the reserved-slot technique, and a replay candidate. `PlatformReceipt`, `ProjectOperation`, `CommitSession`, and the other authority types come from the production paths over those inputs. `cfg(any(test, feature = "crash-matrix"))` is allowed only at sites X9-1 pins. Every record says `synthetic-signed-v2` and `BASELINE-ATTESTED`, which is line 886. The module is not a production seam under items 1 and 2. The forbidden list bars a support function that returns an authority type.

## Items 7 and 8

One canonical JSON record per run, raw digests of the scratch installation, a logical dump, and `normalizedSha256` over logical state with drawn values replaced in order of first appearance. Raw digests may differ across repetitions; the normalized digest and the trace digest may not. Capture happens before the ladder and after each ladder step, so R1's `stateUnchanged` is a comparison. Runs live under gitignored `target/opensip-x9/`. X9-6 commits `matrix.json` and `runs/` to arch, without raw tarballs. `tools/check_crash_matrix.py` is read-only and refuses unless the reviewed `required-runs.v1.json` matches one PASS run each, the labels match, the commit is clean and reviewed, the census matches the kill set, release absence passes, and the two lead repetitions agree. The reviewer's rerun is X9-6's determinism check. There is no matrix to rerun in this law review.

R1 through R4 are fresh processes: read-only `recover`, a next lawful writer, the sweep, and `recover` again. Mutation rows stop after R2. Runs with no ExecutionId skip R1 and R4. Lawful runs assert the release order from line 608. The abbreviations are X6's standings, including `unknown-attempt-unobserved`.

## Item 9

The rows cover F00–F53. Expected values follow the build-plan row where a later accepted law has not restated it, and the owning law where it has. `required-runs.v1.json` is transcribed before any run.

- **F43.** X6 item 4 reads one ledger snapshot (step 1) before the carrier capture (step 3). X3d item 4 makes the SEAL durable before the evidence `COMMIT`. A lawful writer can add journal records after the reader's ledger snapshot; it cannot leave that snapshot naming a sequence the later capture no longer has. The process case is the tail-loss mutation. The reconciling retry stays in X6 item 11's in-process hazard test. The expected standing is the build plan's F43 rule: binding-unusable attributed to the carrier owner, or the F22 condition when the floor is at or above the requested sequence and two tail observations agree, and never uncommitted.
- **F44 and F45.** They use F39's end-path `REV`, held before the end step copies the floor forward. A's SEAL stays above the floor its own floor step wrote. A later writer's floor step would raise that floor and remove the condition. F44's hold is the pending witness before the `REV` commit: unknown-custody, not invalidated, diagnosis `witnessWouldRevert`, no REVERT, ADVANCE, witness write, or floor raise, and no wait. F45's hold is after that commit: committed-historically under `witness-pending-at-tail`, with `interior-bodies-not-authenticated` and `witnessWouldAdvance`, and no write. Both match the build-plan rows.
- **C5.** X6 item 7 starts the sweep at X1's `admit_ordinary_writer` and says the sweep takes no X4 guard. It does not say whether that admission refuses a revoked closure subject. F18, F19, and F38 therefore end the ladder at R2 with `ladderEnd: G5` until an X1 or X6 law fixes R3. Choosing R3 here would decide that admission.
- **F13.** X3d item 6 returns `PublishedCommit` only after the evidence `COMMIT` succeeds and names that case F13. The kill at `x3d.publish.commit-returned` is committed-historically with `pendingSettlement`, which is that law, and F14 is the same standing once the acknowledgement is lost.
- **F00.** A kill before the attempt commit leaves no attempt row. A drawn ExecutionId that was never written is X6's `unknown-attempt-unobserved` (no attempt row). The next writer then commits.
- **F32.** The busy row is X7 r3 item 6a. The rollover is the end step, which is X3b item 13, and it is not inside `publish`.
- **F37** is X6 item 10's private ordering accessor, so it is `elsewhere`. **F35, F47, F48, F50, and F51** are L5, matching X6 item 9. **F46** is the executed read side.

## Item 10

L1 through L10 are recorded in `matrix.json` and are not PASS rows. L1's lost page cache is not what `SIGKILL` does; F03 and F05 are marked as the survived branch, and torn content is the `torn` stand-in. L2 leaves SQLite's interior commit to SQLite. L3's real stalls and the 10 s freshness stall need elapsed time; a `hold` is not a stalled syscall. L4 records X4T r9 item 7's whole-file `state.v1` limit and asserts neither refusal nor admission. X4T item 12's own unit test already admits that restore; this matrix does not add a second pin. L5, L6, L9, and L10 match the absence of a migration writer, an orphan collector, a native optional delivery, and a pruning writer. No LIMIT row is also an executed PASS, and no executed row is filed as a limit.

## Item 11

Writer A held at a named point cannot release, so B, C, and a reader each have one outcome from `LOCK_NB` or the product's bounded fence wait. Revocation children arm `x4.observer.tick` as `hold`, so a tick happens only when the parent resumes it. The parent publishes the trust change under the fence after the child's handoff, then resumes either the main thread or one tick, and waits for `x4.gate.latch.after` before resuming the main thread. The 2 s guard is from the first monitored read to the last checkpoint. A run over 2 s is `HARNESS-ERROR`, so a slow script cannot be accepted as `OBSERVER.FAIL_STOP`. The observer's own 5 s period stays in force only when the point is unarmed.

## Item 12

X9-0 is the platform mechanism and lands before X3d-1. X9-1 is the support surface and the points for units already integrated, and it precedes the X3d-2, X6b, and X7a composition tests. X9-2 through X9-5 split the rows across storage and host, with the dependencies the proposal names, including X2e, X4a, X5a, X6a/b/c, X7a/b, X3d-1/2, X3b-4, and VD1 before the X9-6 exit. X9-6 is the two lead runs, the checker, release absence, the reviewer's rerun, and the arch record.

## Cross-law corrections

They are real, and none of them changes an accepted outcome or row.

- **G1.** X3d r6 item 12 tells `opensip-storage` tests to build a `ProjectOperation` through security's `cfg(test)` fixtures and X4T-0. X6 r2 item 11 builds scratch installations from X3b's and X3c's test fixtures and X4T-0 for storage and host tests. X7 r3 item 10's integration tests need X4T-0's signed trust from the host crate. Those fixtures are not visible across crates. Item 6 is the supply, and X3d-2, X6b, and X7a depend on X9-1.
- **G2.** X3c r7 item 11 says a fault-injection hook exists only under `cfg(test)`. X3b r10 item 11 and X4T r9 items 12 and 13 keep their fixtures `cfg(test)` and say there is no production seam. Item 2 keeps the code out of every non-test build by the feature and the four guards. The restatement belongs to those laws' next revisions.
- **G3 and G4.** X6 r2 names no hold between the bracket reads, and X4 r7 names no observer or checkpoint point. F49, F29, F44, F45, F18, F19, F38, and F39 need them. X6a/b and X4a place the item 5 points.
- **G5.** The sweep's admission under a revoked view is open, as C5 says.
- **G6.** EXIT-PLAN's X9 row omits X2e and X5, and its "X9 last" order hides that X9-0 and X9-1 precede the composition tests. The proposal's unit list is the order that implements G1.

X3d item 10's named test-only crash points are item 5, and its "test-only" is item 2.
