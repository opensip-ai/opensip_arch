# The crash, lock and revocation matrix — proposal X9 r1

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X9 of `EXIT-PLAN.md`, the unit that gates M2 completion. It is written under:
- the build plan's M2 row (`docs/v2/architecture/implementation-boundaries-and-build-plan.md` line 886: "actual crash/lock/revocation matrix pass; synthetic fixtures remain labelled"), its ordered failure matrix F00–F53 (lines 524–587), its required API and fault-injection checks (lines 591–613; the test owner `crates/storage/tests/commit_tests.rs`, line 594), and the tooling row for storage and process faults (line 1072: "deterministic synchronization and crash barriers against actual storage/processes … Record platform/filesystem/profile, actual state bytes and exact outcomes; inject before/after each durability step, without sleep-and-hope synchronization");
- `EXIT-PLAN.md`'s X9 row and its "Choices left open" recommendation for crash injection;
- the accepted laws X2 r8, X3a r5, X3b r10, X3c r7, X3d r6, X4 r7, X4T r9, X6 r2 and X7 r3, for every failure case each one assigns to X9 or says "X9 records".

Product baseline: main `f1b8321` (X3d-0 integrated). Every item contains a lead decision made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Not product code. No new public code, row or detail.

## Problem

The build plan says "No crash case has been executed" (line 530), and M2 completes only when the actual matrix passes. The accepted laws each prove their own steps in-process and leave process-level execution to X9:
- X3d item 10: "X9 runs F00–F53 in fresh processes with crash barriers. X3d supplies named, test-only crash points before and after each durability step";
- X6 r2 items 10 and 11: F49's real concurrent processes, and "real crash and concurrency runs in fresh processes belong to X9";
- X4T r9 item 7: a whole-file `state.v1` restore is "a stated limit … X9's matrix records it as a stated limit and does not test it as a refusal".

At `f1b8321` the product has the following, and nothing more:
- **In-process crash and fault hooks, all `cfg(test)`.** These are:
  - X3b-2's `AppendStep` and `Fault { Crash, Fail }` hook on `JournalAppendLock` (`security/src/journal_store/carrier_append.rs` lines 273–366);
  - X3c-2's `ObjectStep` crash points with `simulate_crash`, and `PreparedLedgerCommit::with_commit_hook` (`storage/src/ledger_store/project_commit.rs` lines 130–316 and 548–580);
  - the gate and session step scripts in `custody/installation_admission.rs` and `installation_session.rs`.

  They write the state a death would leave and then return. They cannot model a real death: no destructor skipped, no flock released by the kernel, no SQLite rollback on reopen, no fresh process reading the bytes.
- **The platform's durable primitives.** `PublicationOps` in `platform/src/filesystem.rs` lines 945–1033 (`write`, `sync_file` by `F_FULLFSYNC`, `renameat`, `sync_directory` with the `F_FULLFSYNC`-then-`fsync` fallback), `replace_with`'s stages (`PublicationStage`: `Prepare`, `WriteTemporary`, `SyncTemporary`, `Rename`, `SyncDirectory`), and `publish_new_regular`. There are also the accounted forms that the witness and floor file protocol uses (`security/src/journal_store/carrier_floor.rs` `publish_private_file`, line 280: `create_private_regular_file`, `write_new_regular_accounted`, `rename_replace_accounted`, `confirm_directory_barrier_accounted`, reopen), and the non-blocking `FileLock` (`platform/src/locks.rs`).
- **A fresh-process precedent.** `journal_store.rs` line 1289 re-executes the test binary (`current_exe()`, `--exact`, an environment marker) so that a process-global mutation stays out of the workspace test process.
- **No integration test in storage or host.** `crates/storage/tests/` does not exist, and `crates/host/tests/` holds only fixtures. No crate declares a Cargo feature.

**A structural fact decides most of this law.** `cfg(test)` is set only for the crate under test. An integration target such as `crates/storage/tests/commit_tests.rs` links the libraries as non-test builds, so none of the `cfg(test)` hooks or fixtures above exist for it. These include X4T-0's signed store, the injected InitialCore image and the synthetic V2 profiles, without which this BASELINE-ATTESTED host refuses at F0 and at `/`. The same is true of storage's or host's unit tests reaching security's fixtures. "`cfg(test)` hooks only" therefore cannot cross a process, and it cannot cross a crate either.

## Decisions

1. **The injection mechanism: named barrier points compiled only into a test feature, in a re-executed child process that the parent kills while it is held at the point (lead decision).**
   - **The feature.** Each of `opensip-platform`, `opensip-security`, `opensip-storage` and `opensip-host` declares one Cargo feature, `crash-matrix`, that forwards to its internal dependencies' features of the same name. It is never default.
   - **The barrier module.** `opensip_platform::crash_barrier` exists only under the feature. It holds the point registry, the arming parser, the rendezvous protocol (item 2) and the parent-side driver (item 3).
   - **The macro.** Every point is written `crash_barrier!(scope, step, kind)`. Without the feature the macro expands to nothing: no call, no string, no branch.
   - **Platform points.** Inside the platform primitives the point is the primitive's own step: `create`, `write`, `file-barrier`, `rename`, `link`, `directory-barrier`, `reopen-confirm`, `lock`, `unlock`.
   - **Protocol scopes and protocol points.** The protocol that calls a primitive names a scope around the call with `crash_scope!`, which is thread-local and also compiled only under the feature, so a platform point reports its full name, for example `x3b.append.seal.witness-pending/rename.after`. SQLite steps (`begin`, `insert`, each `stage-<table>`, `commit`) and the protocol's own decision points are written at the protocol site, because the platform does not own SQLite.
   - **Grammar.** The full name is `<scope>[/<primitive-step>].<before|after>`. A point's occurrence `#k` (1-based) counts per full name within one process.
   - **Rejected:**
     - **`cfg(test)` hooks only.** They cannot reach an integration target or another crate, and they cannot produce a real death (see Problem). They remain the in-process unit-test seam. X9 does not remove or rename them.
     - **A separate child harness binary** (`[[bin]]` or `src/bin`). It would be a new binary target linking the feature, with its own inventory row and a shipping risk, and it duplicates libtest's selection. The re-executed test binary already has a precedent (journal_store.rs line 1289).
     - **`fork` without `exec` from the test process.** The libtest process is multi-threaded, so a forked child may inherit held locks and allocator state. It is also not a fresh process.
     - **An external debugger or `dtrace` breakpoint.** It is outside the pinned closure, its symbol names are not stable, and it is not deterministic.
     - **A custom SQLite VFS** that rendezvouses inside `xSync`. It is new `unsafe` code under the carrier, and it would change the very durability path under test (limit L2).

2. **Barrier points never exist in a release build (lead decision).** Four independent guards:
   1. **Compile guard.** Each crate that declares the feature carries `#[cfg(all(feature = "crash-matrix", not(debug_assertions)))] compile_error!(…)`. A release-profile build with the feature fails to compile.
   2. **No manifest enables it.** No `[dependencies]`, `[dev-dependencies]` or `[build-dependencies]` entry in any manifest names `crash-matrix`. The two matrix targets declare it as `[[test]] … required-features = ["crash-matrix"]`, so a plain `cargo test --workspace` skips them and builds no feature. The feature is reached only by an explicit `--features crash-matrix` on the matrix lane's command line. A source pin in X9-0 reads every `Cargo.toml` and confirms this.
   3. **The edge checker stays unchanged.** No self or reversed dev edge is added, so `check_package_edges.py`, which reads dev edges against the inventory policy, needs no exception.
   4. **Release-absence evidence (item 7).** Each matrix record builds `opensip-cli` in release with no features, and confirms that the binary contains neither the string `OPENSIP_X9_` nor any registered scope name. It also confirms that `cargo build --release -p opensip-storage --features crash-matrix` fails at the compile guard.

   **Unarmed behaviour.** With the feature built but no `OPENSIP_X9_ARMS` in the environment, every point is a read of a process-wide `OnceLock` followed by a return. No protocol's behaviour or order changes.

   **Rejected:** points compiled into every build and armed by an environment variable at run time. That is a release-build fault-injection surface, which every accepted law's forbidden substitutes exclude ("no production seam").

3. **The process protocol and how the parent verifies the death point, without sleeps (lead decision).**
   - **The child.** The child is the same test binary, run as `current_exe() --exact <child entry> --nocapture --test-threads=1`.
     - **Environment.** The environment is cleared and then given only: `OPENSIP_X9_CHILD` (the driver name: `commit`, `recover`, `sweep`, `competitor-writer`, `reader`), `OPENSIP_X9_INPUT` (the path of a driver input file under the run's scratch root), `OPENSIP_X9_ARMS`, and `TMPDIR` set to the run's scratch parent.
     - **The entry.** The child entry is an ordinary `#[test]` that returns at once unless `OPENSIP_X9_CHILD` is set. So it passes trivially in the parent's own run.
   - **Channels.** The channels are the child's standard streams, created by `Command` as pipes. No descriptor passing and no `unsafe` is needed.
     - **stderr (report).** It carries tagged records `X9|<pid>|<thread>|<n>|<full name>#<k>|<event>|<payload>`, each one `write(2)` of at most 512 bytes (`PIPE_BUF` on macOS), so it is atomic. Untagged stderr is kept as diagnostics.
     - **stdin (control).** The parent writes `resume\n` on it.
   - **Arming.** `OPENSIP_X9_ARMS` is a comma-separated list of `<full name>#<k|*>=<action>`.
   - **The actions** (item 4 says which kinds of point admit which action):
     - **`hold`.** The thread writes a `held` record and then blocks in `read(2)` on stdin. It executes no product code between the write and the read. The parent then either kills the child (a crash) or writes `resume` (a pause: contention, revocation, a stalled step).
     - **`fail-before` and `fail-after`.** The primitive returns its own native error class without performing the effect, or after performing it (item 4).
     - **`torn`.** A `write` step writes the first half of the bytes, then holds.
     - **`inject-id:<exec1_…>`.** At `x3d.session.execution-draw` only, the draw returns the given ExecutionId (F34).
   - **Unarmed points.** Every reached point writes a `pass` record, so the parent holds the complete ordered trace.
   - **The kill.** On reading the armed point's `held` record, the parent sends `SIGKILL` (`Child::kill`), then `wait`s and reads stderr to EOF. The run counts as a death at that point only if all of the following hold:
     - `ExitStatusExt::signal()` is `Some(SIGKILL)`;
     - the last record from the holding thread is that `held` record;
     - no record from any thread names a durability point after it. Another thread may only report read-only points, and the observer is gated (item 5).

     A child that reaches EOF without reporting the armed point is a `HARNESS-ERROR` ("armed point not reached"), never a pass.
   - **No sleeps.** Every synchronization is a blocking read of a record the other side has written.
     - The one timed wait in the harness is a per-run watchdog of 300 s. Its only effect is to kill every child and record `HARNESS-ERROR`. It never decides an outcome.
     - A source pin over `crash_barrier`, the support module and both matrix targets admits no `sleep`, no polling loop and no other timed wait.
   - **Product waits.** The product's own bounded waits (the 468 fence's wait, S7's backoff) run as in production. Their outcome against a held peer is fixed, because the peer never releases.
   - **Rejected:**
     - **The child killing itself at the point.** It would need a second mechanism for pauses. With one parent-decided mechanism, a crash, a contention and a revocation are the same `hold`.
     - **A parent that kills after a delay.** That is the sleep-and-hope that line 1072 forbids.

4. **Point kinds and the faults that stand in for what cannot be triggered natively (lead decision).** Every point declares one kind in its macro. An armed action that the point's kind does not admit is a `HARNESS-ERROR` in the child.
   - **`step`.** Admits only `hold`. This is the default for every point.
   - **`fallible`.** Admits `hold`, `fail-before` and `fail-after`. Each `fail` returns the same failure the matching `cfg(test)` `Fault::Fail` documents (carrier_append.rs lines 294–300):
     - at an SQLite `commit`: `fail-before` is a `COMMIT` that does not land and reports failure; `fail-after` is a `COMMIT` that landed and reports failure. This is F09, F12 and F40;
     - at `file-barrier`, `rename` and `directory-barrier`: the native I/O error class of that step.
   - **`write`.** Admits `hold` and `torn`.
   - **`gate`.** A point that guards a product timed wait. In M2 the only one is X4a's observer period. Armed, its rendezvous replaces the timed wait, so a tick happens exactly when the parent resumes it. Unarmed, the product's 5 s period is unchanged.
   - **`draw`.** Admits `hold` and `inject-id`. Only `x3d.session.execution-draw` has this kind.

   **Labels.** A run whose death is a real `SIGKILL` is labelled `process-death`. A run that uses `fail-*`, `torn` or `inject-id` is labelled `injected`. A parent-side change to stored bytes between processes is labelled `mutation`. Every run also carries `synthetic` (item 6). A label is never dropped from a run's record.

   **Rejected:** injecting faults by `LD_PRELOAD`-style interposition, which is outside the pinned closure and is refused by hardened runtime.

5. **The points the matrix needs, and who places them.**
   - **The census.** The required points are not a hand list. X9-0 runs a lawful commit, recovery and sweep with nothing armed, and records every point reached: the census trace. The kill matrix is then every durability point in the census, at `#1` and, for repeated protocols (objects, appends), at the first, a middle and the last occurrence.
     - A durability primitive reached outside any scope is a `HARNESS-ERROR`, so no unnamed step can hide.
     - A census point that a later product change removes, or a new unarmed durability point, fails the coverage check (item 7).
   - **The scopes, by owner:**

     | Scope | Owner law | Steps |
     |---|---|---|
     | `x4t.floor-publication` | X4T r9 item 7 (X4T-b) | the file protocol |
     | `x3b.floor`, `x3b.end.floor` | X3b items 3, 4 and 4a | the file protocol |
     | `x3b.init` | X3b item 3a | `create`, `ddl.commit`, barriers, then `x3b.init.witness` |
     | `x3b.start.witness` | X3b item 4 | REVERT, ADVANCE, INIT and OPEN witness writes |
     | `x3b.append.<seal\|rev\|cln\|terminal>` | X3b item 5 | `begin`, `level-four`, `witness-pending/…`, `insert`, `commit` (`fallible`), `witness-committed/…`, `release-level-four`, `release-level-three` |
     | `x3b.rollover` | X3b item 13 | `exclusive`, the `terminal` append, `open.witness` |
     | `x3c.ledger-create` | X3c item 2 | `create`, `wal`, `ddl.commit`, barriers |
     | `x3c.attempt` | X3c item 3 | `begin`, `insert`, `commit` (`fallible`) |
     | `x3c.object` | X3c item 4 | `create`, `write` (`write`), `file-barrier`, `link`, `directory-barrier` |
     | `x3c.evidence` | X3c items 5 and 6 | `begin`, `stage-<table>`, `commit` (`fallible`) |
     | `x3d.session` | X3d items 2 and 3 | `execution-draw` (`draw`; its `pass` record carries the ExecutionId), `settlement-reserved` |
     | `x3d.publish` | X3d item 4 | `after-staging`, `before-final-checkpoint`, `commit-returned`, `published` |
     | `x3d.finish` | X3d item 7 | `settle`, `lease-release`, `end-step` |
     | `x4.checkpoint` | X4 item 3 | `before-observation`, `after-observation`, `before-admit` |
     | `x4.gate` | X4 item 7 | `admit.after`, `latch.after` |
     | `x4.observer` | X4 item 5 | `tick` (`gate`), `after-observation` |
     | `x2.fence`, `x2.lease` | X2 item 7 | `lock` and `unlock` of the fence, `writer.lease` and `readers.lease` |
     | `x6.recover` | X6 r2 items 3 and 4 | `after-lease`, `after-ledger-snapshot`, after each of `W1 H1 J W2 H2`, `after-fresh-capture` |
     | `x6.sweep` | X6 r2 item 7 | `after-exclusive`, `after-snapshot`, `settle.commit` (`fallible`) |
     | `x7.delivery` | X7 r3 items 3 and 4 | `required` and `optional` (`fallible`: a renderer or optional-effect failure) |

     The scope names are fixed by this law. The step lists are fixed by the census.
   - **Who places them.**
     - **Units integrated before X9-0** (X3b-1/2/4, X3c-1/2, X2d, and X4T-b if it lands first): their points are placed by X9-1.
     - **Units built after X9-0** (X3d-1, X3d-2, X4a, X2e, X6a/b/c, X7a/b): each places its own points as part of its unit. X3d item 10 already requires this of X3d. For X4a, X6 and X7 it is a new requirement, recorded under "Cross-law corrections".
     - **Existing `cfg(test)` hooks stay.** Where one already exists (`AppendStep`, `ObjectStep`, the commit hook), the point sits at the same place, and its name matches the hook's variant.

6. **The synthetic test-support surface (lead decision).** Under the feature only, each of security, storage and host exposes one `#[doc(hidden)] pub mod crash_matrix_support`.
   - **What it exposes.** Producers of *inputs on disk* under a scratch root, never an authority type:
     - a synthetic installation through the real creator path, with InitialCore's injected loaded image and the synthetic V2 profile set;
     - X4T-0's signed accepted store, built from the public test-only quorum seeds;
     - a revocation or policy publication helper that replaces `state.v1` atomically under the installation fence, as the trust owner does;
     - the inherited format-1 and format-2 carrier fixture;
     - X3b-2's reserved-slot technique: lift `gj3_append_laws`, write, reinstall the trigger SQL byte-identically;
     - a synthetic run candidate for the evaluator's public `replay_run`.
   - **What comes from production code.** `PlatformReceipt`, `ProjectOperation`, `CommitSession`, `ReplayedRun`, `PreparedCommit`, `PublishedCommit` and `RecoveredCommit` all come from the production paths over those inputs.
   - **Substitutions inside production types.** Where a production type needs its existing test-only variant to accept the synthetic input (for example `trust/initial_core.rs`'s `Image::Injected`), that `cfg(test)` becomes `cfg(any(test, feature = "crash-matrix"))`. X9-1 pins the exact list of such sites with a source pin, and no other site may use the feature.
   - **Every record says so.** Each run records `"fixture": "synthetic-signed-v2"` and `"profileStanding": "BASELINE-ATTESTED"`. This is line 886's "synthetic fixtures remain labelled, not compiler qualification".
   - **Rejected:**
     - **Running against a real installation.** On this host the real path refuses at InitialCore F0 and at `/` without owner signing keys (EXIT-PLAN, "Owner actions").
     - **Running X9 inside security's unit-test binary.** Storage's `commit.rs` and host's finalization are unreachable from it, because security depends on neither.
     - **A support module that mints authority types directly.** That is a production-shaped seam even under a feature, and it would test the fixture instead of the composition.

7. **The evidence shape (lead decision).**
   - **One record per run.** Each run writes `runs/<case>-<variant>.json`: canonical JSON through `opensip_identity::canonical_bytes`, sorted keys, no floats.

     ```
     { "schema": "opensip.x9.run.v1",
       "case": "F07", "variant": "kill-witness-pending-rename-after", "units": ["X3b"],
       "labels": ["process-death", "synthetic"],
       "product": { "commit": "<40 hex>", "worktreeClean": true, "toolchain": "<rustc -vV>",
                    "profile": "dev", "features": ["crash-matrix"] },
       "host": { "os": "<sw_vers>", "arch": "arm64", "filesystem": "apfs",
                 "profileStanding": "BASELINE-ATTESTED", "fixture": "synthetic-signed-v2" },
       "script": [ { "await": "x3b.append.seal.witness-pending/rename.after#1", "then": "kill" } ],
       "children": [ { "role": "commit", "exit": { "signal": 9 } | { "code": 0 },
                       "lastHeld": "<full name>#<k>" | null,
                       "trace": { "records": 41, "sha256": "<hex64>" },
                       "outcome": <the child's returned outcome or termination row> | null } ],
       "postState": { "raw": [ { "path": "<relative>", "bytes": n, "sha256": "<hex64>" } ],
                      "logical": { "ledger": {…}, "carrier": {…}, "witness": {…}, "floor": {…},
                                   "objects": [...], "trustState": "<sha256>" },
                      "normalizedSha256": "<hex64>" },
       "ladder": [ { "step": "R1-recover", "standing": "unknown-attempt-open", "stateUnchanged": true },
                   { "step": "R2-next-writer", "witnessAction": "REVERT", "outcome": "Committed" },
                   { "step": "R3-sweep", "wrote": "refused" },
                   { "step": "R4-recover", "standing": "terminal-not-committed" } ],
       "expected": { …this law's row, transcribed in required-runs… },
       "verdict": "PASS" | "FAIL" | "HARNESS-ERROR" }
     ```
   - **The post-state.**
     - **Capture.** It is captured after the last child of the scripted phase has exited and before the ladder starts. It is captured again after each ladder step, so that R1's `stateUnchanged` (recovery is read-only) is a comparison, not a claim.
     - **`raw`** is every file under the scratch installation by digest. That is line 1072's "actual state bytes".
     - **`logical`** dumps the SQLite tables row by row through a read-only connection, and decodes the witness, floor and object sets.
     - **`normalizedSha256`** hashes `logical` after replacing every drawn value (ExecutionId, `op-` token, staging nonce, wall-clock datum) by a placeholder numbered in order of first appearance. Raw digests differ between repetitions; the normalized digest must not.
   - **Where it lives.**
     - **In the product.** Runs write under `target/opensip-x9/<runSetId>/`, which git ignores. That directory holds `runs/`, `matrix.json` and, for a failed run only, a tarball of the raw scratch tree.
     - **`matrix.json`** lists the run files with their sha256, the census, the release-absence result (item 2), and the repetition comparison.
     - **In arch.** X9-6 commits the final run set to `docs/implementation/m2/crash-matrix-x9/evidence/<product commit>/` (`matrix.json` and `runs/`, without the tarballs).
   - **The checker.** It is `tools/check_crash_matrix.py` in the product: read-only, standard library only, under the pinned Python. It refuses unless all of these hold:
     - every `(case, variant)` in the reviewed `required-runs.v1.json` (item 9) has exactly one run, and no extra run exists;
     - every verdict is `PASS`;
     - the labels equal the required labels;
     - `product.commit` is the reviewed commit, and the worktree is clean;
     - the census and the kill set agree (item 5);
     - the release absence passes;
     - the two lead repetitions agree run by run on `normalizedSha256` and on the trace digest.
   - **How the review checks it.** The reviewer owns the native lane for X9-6, and:
     1. reruns the whole matrix on the reviewed commit;
     2. runs the checker over both run sets;
     3. compares its normalized digests and traces with the lead's.

     Agreement across the three executions is the determinism evidence.
   - **Rejected:**
     - **Committing raw state bytes to arch.** A run set would be hundreds of megabytes of SQLite and trust files whose bytes carry random nonces. Digests plus logical dumps carry the same evidence, and failures keep their tarball.
     - **A pass/fail log without state.** Line 1072 requires the actual state and the exact outcomes.

8. **The recovery ladder.** Every run that leaves an attempt behind is followed by four steps, each in a fresh process:
   - **R1:** `recover(executionId)` (X6, `SHARED-READ`, no fence). It must leave `normalizedSha256` unchanged.
   - **R2:** a next writer that runs a full lawful commit on the same namespace. It records the floor step's decision and the start's witness action (OK, REVERT, ADVANCE, INIT or OPEN), then its outcome.
   - **R3:** the settlement sweep (X6c, `EXCLUSIVE` under the fence). It records what it wrote, or that it wrote nothing.
   - **R4:** `recover(executionId)` again.

   **Exceptions.**
   - **Mutation rows** run R1 and R2 only, because the injected condition persists.
   - **Runs without an ExecutionId** skip R1 and R4 and record `"notApplicable": "no-execution-id"`. The ExecutionId comes from the `x3d.session.execution-draw` pass record.
   - **Every lawful run** also asserts the release order line 608 requires, from its trace: level 4, then each level-3 transaction, then the lease, then the fence.

   Abbreviations in item 9: CH committed-historically, CAD committed-availability-degraded, TNC terminal-not-committed, UAO unknown-attempt-open, UAU unknown-attempt-unobserved, UC unknown-custody, UQ unknown-quarantine-condition, UB unavailable-busy, BU binding-unusable, UCI unknown-carrier-incompatible.

9. **The matrix.** Every row runs on this macOS 27 host under item 6's synthetic fixture.
   - **Status values.** "exec" means executed here. "exec (inj)" means executed with an injected stand-in (item 4). "exec (mut)" means executed over a parent mutation. "elsewhere" means it is covered by an accepted law's in-process test and is not a process-level case. "LIMIT" means recorded and not executed (item 10).
   - **Expected values.** They come from the build plan's row and the owning law. X9-a units transcribe each row into `required-runs.v1.json` before any run. An expected value is never read back from a run.

   | Case | Owner | Injection | Status | Expected |
   |---|---|---|---|---|
   | F00 | X2, X3a, X3b, X4T-b | `hold`→kill at every census point before `x3c.attempt.commit.after` (X4T floor, X3b floor, INIT, start witness, leases) | exec | No attempt row; ledger logical state unchanged. R2: the floor step and start handle X3b item 3a's or item 4's crash state (INIT resumes or finishes, REVERT, ADVANCE), then Committed. With an ExecutionId drawn: R1 and R4 UAU, R3 writes nothing. |
   | F01 | X5 | replay-invalid candidate; substituted target or inventory | exec (host) | Refused before `prepare_commit`; no attempt row; no SEAL; ledger and carrier logical state unchanged. |
   | F02 | X3c | `torn` at `x3c.object.write` (first, middle and last object) | exec (inj) | Staging residue is never adopted. R1 UAO; R2 Committed; R3 refused; R4 TNC. The orphan stays (L6). |
   | F03 | X3c | kill at `file-barrier.before` and `.after` | exec (death branch; L1) | As F02. |
   | F04 | X3c | kill at `link.before` and `.after`; R2 republishes the same digest | exec | As F02. R2 confirms the existing object by exact bytes. An unequal-collision mutation variant refuses on X3c item 10's row. |
   | F05 | X3c | kill at `directory-barrier.before` and `.after` | exec (death branch; L1) | As F02. |
   | F06 | X3b, X3c, X3d | the parent holds a raw SQLite `BEGIN IMMEDIATE` on the carrier, or on the ledger, while the child runs `publish` (labelled `mutation`: a foreign holder) | exec (mut) | Busy row (`LEDGER.BUSY_TIMEOUT`/`PROJECT.BUSY`); an earlier level-3 transaction is released; no SEAL; orphans preserved. R1 UAO; R2 Committed after the holder ends; R3 refused; R4 TNC. |
   | F07 | X3b | kill at each `x3b.append.seal.witness-pending/*` point and at `insert.before` | exec | R1 UAO, diagnosis would-REVERT; R2 REVERT, Committed; R3 refused; R4 TNC. |
   | F08 | X3b | kill at `insert.after` and `commit.before` | exec | SQLite rolls back on reopen. As F07. |
   | F09 | X3b | kill at `commit.after`; `fail-after` and `fail-before` at the SEAL `commit` | exec; exec (inj) | Injected: `CommitUndetermined` (`DURABILITY.COMMIT_FAILED`); nothing appended; no evidence `COMMIT`; the settlement reserve is forfeited. R1 UAO with would-ADVANCE (landed) or would-REVERT (not landed); R2 ADVANCE or REVERT, Committed; R3 refused; R4 TNC. |
   | F10 | X3b | kill at each `witness-committed/*` point | exec | R1 UAO, would-ADVANCE before the rename survives, OK after; R2 ADVANCE or OK; R3 refused; R4 TNC. |
   | F11 | X3c, X3d | kill after each `x3c.evidence.stage-<table>` | exec | The ledger transaction rolls back; the SEAL is durable with no `REV` (the process died before `finish`). R1 UAO; R2 Committed; R3 refused; R4 TNC. |
   | F12 | X3c, X3d, X7 | `fail-after` and `fail-before` at `x3c.evidence.commit` | exec (inj) | `CommitUndetermined` with ExecutionId and no RunId; no retry; nothing appended. R1 CH with pendingSettlement (landed) or UAO; R3 committed or refused; R4 CH or TNC. |
   | F13 | X3c, X3d | kill at `x3d.publish.commit-returned` | exec | R1 CH with pendingSettlement; R2 Committed; R3 committed; R4 CH. |
   | F14 | X3d, X6 | kill at `x3d.publish.published` and at `x3d.finish.settle.before` | exec | As F13. |
   | F15 | X6 | kill after `x3d.finish.end-step.after` | exec | R1 CH; R2 creates no second receipt for this ExecutionId. |
   | F16 | X7 | `fail-before` at `x7.delivery.required` | exec (host, inj) | `DELIVERY.REQUIRED_FAILED`, exit 4, runId kept; R1 CH. |
   | F17 | X7 | `fail-before` at `x7.delivery.optional` | exec (host, inj; L9) | Committed; optional failure disclosed; result unchanged. |
   | F18 | X4, X3d | `hold` at `x4.checkpoint.before-observation#1`; the parent publishes a revoking update, or makes the view unreadable or mixed; resume | exec | Refused `TRUST.COMPONENT_REVOKED_DURING_OPERATION`, or `OBSERVER.FAIL_STOP`; no SEAL; `finish` appends `REV` from the settlement reserve. R1 UAO; R2 refused at admission (revoked), or Committed after the view is restored (fail-stop variant); R3 and R4 per C5. |
   | F19 | X3b, X3d, X4 | as F18 at the repeated checkpoint after the SEAL (`#2`); also kill at each point of the end-path `REV` append | exec (stall variant: L3) | Refused; evidence transaction rolled back; the trace shows level 4, then level 3, then a fresh `x3b.append.rev`, then `CLN` if owed. A killed `REV` leaves X3b's append crash state. R1 UAO; R3 and R4 per C5 (or refused and TNC in the fail-stop variant). |
   | F20 | X6, X3b | the parent rewrites the witness as malformed or with a mismatched digest | exec (mut) | R1 UQ after the five stable observations; R2 quarantine row (`LEDGER.CORRUPT`). |
   | F21 | X6, X3b | the parent deletes the witness of a nonempty journal | exec (mut) | R1 UQ (`witnesslessRestore`); R2 quarantine row. |
   | F22 | X6, X3b | the parent restores a carrier copy taken at an earlier `hold`, under a newer floor; or equal seq with a different hash | exec (mut) | R1 UQ; R2 quarantine (floor regression or `uncertainTailLoss`). |
   | F23 | X6 | the parent deletes the receipt row, or the association row | exec (mut) | R1 UC; R3 writes nothing (one-sided). |
   | F24 | X6, X3a | ledger mode `000` or a truncated header; a wrong store generation selected | exec (mut) | R1 UC; R2 refused on its X3c or X3a row; R3 reports host I/O for that namespace and writes nothing. |
   | F25 | X6 | the parent deletes, or flips one byte of, a committed object | exec (mut) | R1 CAD with `evidence.missing` or `evidence.corrupt`. |
   | F26 | X4, X6 | commit, then the parent publishes a revocation | exec | R1 CH; R2 refused at admission; no grant reused. |
   | F27 | X6 | the parent swaps the association's namespace, generation, operation or execution; or a request with a different binding | exec (mut) | R1 BU. |
   | F28 | X6 | X6a's pruned-record fixture, read in a fresh process | exec (mut) | R1 UC. |
   | F29 | X6 | a reader process while the writer holds at `x3c.attempt.commit.after`, after the SEAL, at `x3d.publish.after-staging` and at `commit-returned` | exec | UAO, UAO, UAO, CH with pendingSettlement; never mixed; the reader takes `readers.lease` alongside APPEND-WRITE without waiting. |
   | F30 | X2, X6c | writer A holds (a) under its lease after the fence is released and (b) while it holds the fence; process B is a competing writer; process C is the sweep | exec | B: the busy row after S7's bounded fence or lease attempt, no upgrade, no state change. C: skips and retains the namespace. After A resumes, A is Committed, and a second B then succeeds. |
   | F31 | X3b | the parent installs the format-1 or format-2 fixture as the namespace's carrier | exec (mut) | R2 refused before commit work (X3b item 3a's F46 row); no SEAL is inserted. |
   | F32 | X3b-4, X7b | reserved-slot setup to tails `…987` and `…988`; kill at each X3b item 13 crash-table point | exec (host; mut + death) | `CarrierCapacityExhausted`; `finish`; the rollover in the end step; X7 r3 item 6a's busy row. Each crash row as X3b item 13 states; the next writer proceeds in G+1. |
   | F33 | X6 | the parent alters receipt bytes, the inventory, a signature, or the SEAL body digest | exec (mut) | R1 UC. |
   | F34 | X3d, X6 | `inject-id` with a previous run's ExecutionId | exec (inj) | `ExistingAttempt`; X6 routing: the same binding gives that attempt's standing, a different one gives BU (`RECOVERY.REFUSED`); no new row, no SEAL. |
   | F35 | — | — | LIMIT (L5) | — |
   | F36 | X3b, X3c, X6 | the orphan SEALs of F09, F11, F19 and F38, followed by R2 committing the same semantic RunId | exec | The earlier ExecutionId: R1 UAO, R3 refused, R4 TNC. The later ExecutionId: CH. The RunId is not blacklisted. |
   | F37 | X6 | — | elsewhere (X6 item 10: the pure ordering accessor) | — |
   | F38 | X3d, X4 | `hold` at `x3d.publish.after-staging`; the parent revokes; resumes `x4.observer.tick#1` and awaits `x4.gate.latch.after`; resumes the main thread | exec | The gate goes 0→2; no permit; staged transaction rolled back; `REV` and `CLN` from the reserve. R1 UAO; R2 refused at admission; R3 and R4 per C5. |
   | F39 | X3d, X4, X7 | `hold` at `x4.gate.admit.after`; revoke; observer tick; latch 1→3; resume | exec (storage half; host half in X9-5) | Committed with `latchedAfterAdmission`; host projects `DELIVERY.REQUIRED_FAILED`; R1 CH. |
   | F40 | X3d, X7 | as F12, with and without F39's latch | exec (inj) | `DURABILITY.COMMIT_FAILED`, ExecutionId, no RunId; the latch does not convert it. The ladder as F12. |
   | F41 | X4, X3d | the two process-level orders: latch before admission, and admission before latch | exec (two orders); every interleaving is covered elsewhere (X4's gate-trace test) | At most one `x3c.evidence.commit` in the trace; the gate stays in 0..3. |
   | F42 | X3d | abort is every kill above; the child driver `mem::forget`s its `StoppedSession` and exits; a held point with a reader running | exec (kernel stall: L3) | Forget: the kernel releases the lease, the attempt stays admitted, R1 UAO. The reader during a hold: UB or UAO. Never a claimed cleanup. |
   | F43 | X6 | tail-lost variant: after a commit, the parent truncates the journal tail below the association's `journalSeq` (reserved-slot technique) | exec (mut); the reconciling-retry variant is elsewhere (X6 item 11's hazard test) | R1 per the F43 rule: UB attributed to the carrier owner, or the F22 condition when the floor is at or above the requested sequence and two tail observations agree; never uncommitted. |
   | F44 | X6 | attempt A runs F39's script (Committed, gate latched after admission), so its `finish` owes a `REV`; A holds at `x3b.append.rev.witness-pending/directory-barrier.after`; a reader process recovers A's ExecutionId. A's SEAL is above the floor its own floor step wrote | exec | UC, not invalidated; diagnosis witnessWouldRevert; no REVERT, ADVANCE, witness write or floor raise; no wait on A. |
   | F45 | X6 | as F44, with A holding at `x3b.append.rev.commit.after` | exec | CH under witness-pending-at-tail, with `interior-bodies-not-authenticated`; diagnosis witnessWouldAdvance; no write. |
   | F46 | X6 | the format-1 or format-2 fixture, or an association below `first_generation` | exec (mut) | R1 UCI. |
   | F47, F48, F50, F51 | — | — | LIMIT (L5) | — |
   | F49 | X6 | (a) a reader holds between bracket reads while a lawful writer appends, then resumes; (b) writer A holds at `x3c.attempt.commit.after`, a reader of A's ExecutionId holds at `x6.recover.after-ledger-snapshot`, A is resumed to Committed, then the reader resumes | exec | (a) UB, never UQ, never a corruption diagnosis; (b) UAO or UB from the one stale snapshot, never TNC. |
   | F52 | X6 | the four lawful cells from earlier runs (admitted/none, admitted/both, settled-committed/both, settled-refused/none); the other seven by mutation | exec, exec (mut) | X6's §2 matrix; exactly one cell gives TNC. |
   | F53 | X6c | live (a held writer), crashed (killed runs), one-sided (mutation), inaccessible (mode `000`), already settled (a second sweep); also kill the sweep at `x6.sweep.settle.commit.before` and `.after` | exec | X6 r2 item 7: skip, settle, or write nothing. After a killed sweep, the next sweep settles each row exactly once (the monotone trigger). |

   **C5 (revocation ladders).** After a revocation of a subject in the closure, R2 is refused at X4T's admission. Whether R3, the sweep under X1's `admit_ordinary_writer`, is admitted under that revoked view is not fixed by an accepted law (gap G5). X9-4 transcribes R3 and R4 from the law that fixes it before running. Until then, the F18, F19 and F38 ladders end at R2 and record `"ladderEnd": "G5"`. **Rejected:** choosing the expected R3 in this law, which would decide an admission question for X1 and X6.

   **Why F43's lawful race is not a process case.** X6 step 1 reads the ledger before step 3 captures the carrier. The writer makes the SEAL durable before the ledger `COMMIT` (X3d item 4). So no lawful interleaving of processes gives a reader a journal capture older than its ledger snapshot. Only lost tail bytes can, and that is the mutation variant. The retry that reconciles is X6's in-process hazard test.

10. **Limits: recorded, not tested.** Each is written into `matrix.json`'s `limits`, with its reason and its later owner.
    - **L1. Power loss, kernel panic and drive-cache loss.** Process death keeps unbarriered page-cache data, so F03 and F05 exercise only the "survived" branch. The "did not survive" branch of an unbarriered step equals the durable state at the preceding point, because every protocol barriers a file before linking or renaming it. The matrix kills there too, and torn content is covered by `torn`. Media and power faults are M6 qualification (line 1072: "M2/M6").
    - **L2. SQLite's interior commit.** SQLite's commit is atomic under process death by its own contract. The matrix kills at `commit.before` and `.after` and injects `fail-*`. It does not interrupt SQLite's WAL write and sync, and it adds no VFS shim (item 1).
    - **L3. Native stalls and S6 scheduling bounds.** A kernel-level stalled syscall, the observer's 10 s freshness stall (F19's stall variant) and the residual admission window (X4 item 3) need real elapsed time or kernel control. A `hold` emulates a stalled step, not a stalled syscall. X4's scripted-clock tests cover the logic. The bound is a qualification obligation (S6, M6).
    - **L4. Whole-file `state.v1` restore (X4T r9 item 7).** A self-consistent older `state.v1` with its whole closure is admitted. No run asserts that it is refused, and no run asserts that it is admitted: a passing test of the admission would pin the limit as required behaviour, and S9.3's restore lineage, or a future anchor outside I, would then have to break it. Its later owner is S9.3 or that anchor.
    - **L5. Store and carrier migration and restore (F35, F47, F48, F50, F51).** No migration or restore writer exists in M2 (X6 r2 item 9; X3b r10 item 10). F46's read side is executed.
    - **L6. Orphan collection.** No reachability GC exists (X6 r2, "Not claimed"), so F02 to F06's "later authorized reconciliation may remove orphans" is not executed. Orphans are recorded in `postState`.
    - **L7. Measured platform profile.** This host is BASELINE-ATTESTED under 469. Every run is synthetic (item 6). A measured row needs the owner's signing keys, and it is not required for M2.
    - **L8. Host coverage.** macOS 27 on APFS on this host only. Linux, other filesystems and external volumes are not executed.
    - **L9. Native optional delivery.** M2 has no browser launch or export, so F17 runs only as an injected failure.
    - **L10. Journal pruning.** No pruning writer exists, so F28 runs only over X6a's fixture.

11. **Lock contention (F30) and live revocation, deterministically.**
    - **Contention.** Writer A holds at a named point, so its lease, and optionally the fence, is held for as long as the parent wants. The parent then spawns B, C or a reader as fresh processes and reads each one's outcome. Each peer meets a holder that cannot release, so its non-blocking `LOCK_NB` attempt, or the product's bounded fence wait, has exactly one outcome. The parent then resumes A and reads A's outcome. No step depends on timing, and none sleeps.
    - **Revocation.** Every child arms `x4.observer.tick#*=hold`, so the observer ticks only when the parent resumes it.
      - **Order of the parent's steps.** The parent holds the main thread at the named checkpoint or gate point, publishes the trust change (item 6's helper, under the fence, which the held child does not hold after its handoff), and resumes either the main thread (the checkpoint's own monitored read observes it) or one observer tick, awaiting `x4.gate.latch.after` before resuming the main thread.
      - **Why it is deterministic.** Which party latches, and in which gate state, is fixed by the script.
    - **Timing guard.** A held child's awake time counts against X4's 10 s bound. Each run records the monotonic time from the operation's first monitored read to its last checkpoint. A run above 2 s is a `HARNESS-ERROR`, never an `OBSERVER.FAIL_STOP` that the run then accepts.
    - **Rejected:** letting the observer tick on its own 5 s timer during matrix runs, which makes the latching party a race.

12. **Units after the law.** Each comes with its inventory successor and is reviewed alone.
    - **X9-0 (platform; the mechanism).** It contains:
      - the `crash-matrix` feature in platform;
      - the `crash_barrier` module: registry, kinds, the arming parser, the child rendezvous and the parent driver;
      - the `crash_barrier!` and `crash_scope!` macros, the compile guard and the manifest pin;
      - points in the platform primitives (`PublicationOps`, the `replace_with` stages, `publish_new_regular`, the accounted file effects, `FileLock`);
      - `tools/check_crash_matrix.py` with the run schema.

      **Tests.** A self-test child killed at a platform point, with the kill verified; `hold` then `resume`; each `fail-*` and `torn`; an unarmed run identical to a featureless run; an armed but unreached point as `HARNESS-ERROR`; an action at a point of the wrong kind as `HARNESS-ERROR`; the watchdog; and a no-sleep source pin.

      **Dependencies.** None. It should land before X3d-1, so that later units place their own points.
    - **X9-1 (security, storage and host; the support surface and existing points).** It contains:
      - the feature in the other three crates;
      - the `crash_matrix_support` modules (item 6), and the pinned list of `cfg(any(test, feature))` sites;
      - scopes and points at the integrated sites: X3b-1, X3b-2, X3b-4 (if integrated), X3c-1, X3c-2, X2d's leases, X4T-b's floor publication;
      - the post-state capture and normalizer, and the run writer;
      - the census of the then-integrated path.

      **Dependencies.** X9-0. It precedes X3d-2's, X6b's and X7a's composition tests, which need the same surface (gap G1).
    - **X9-2 (storage; carrier and objects).** `crates/storage/tests/commit_tests.rs` with `required-features`, the shared drivers (`commit`, `recover`, `sweep`, `competitor-writer`, `reader`), the ladder, and rows F00, F02–F05, F07–F10, F20–F22, F31 and F46, with their `required-runs.v1.json` rows. **Dependencies:** X9-1, X2e, X4a, X3d-1, X3d-2, X6a, X6b, X6c.
    - **X9-3 (storage; commit and recovery).** Rows F11–F15, F23–F25, F27–F29, F33, F36, F42, F43–F45, F49, F52 and F53. **Dependencies:** X9-2.
    - **X9-4 (storage; locks and live revocation).** Rows F06, F18, F19, F26, F30, F34, F38, F39's storage half, F40 and F41, and C5 once G5 is decided. **Dependencies:** X9-2 and X4a. It uses X4a's observer `gate` point.
    - **X9-5 (host).** `crates/host/tests/commit_matrix_tests.rs` with rows F01, F16, F17, F12's and F40's caller route, F32 with its rollover crash table, F39's delivery half, and F53's `store-gc` step. **Dependencies:** X9-2, X5a, X7a, X7b, X3b-4 and X6c.
    - **X9-6 (record; the M2 exit).** Two full lead runs on one integrated commit, the checker, release absence, the reviewer's rerun, and the arch evidence record. **Dependencies:** all of the above, and VD1 (EXIT-PLAN, "lands before the X9 exit").

## Cross-law corrections found while drafting

These are recorded for the owning laws' next revisions. None changes an accepted outcome or row.
- **G1. Cross-crate `cfg(test)` fixtures do not exist.**
  - **Which laws.** X3d r6 item 12 (storage tests build a `ProjectOperation` through security's `cfg(test)` fixtures and X4T-0), X6 r2 item 11 (X3b's and X3c's fixtures and X4T-0 in storage and host tests) and X7 r3 item 10 (host integration tests with X4T-0's trust) each rely on another crate's `cfg(test)` code.
  - **Why it fails.** Rust sets `cfg(test)` only for the crate under test, so those fixtures do not exist for storage's or host's tests.
  - **The fix.** Item 6's support surface supplies them. X3d-2, X6b and X7a's integration tests depend on X9-1, and each of those laws' test items needs a one-line amendment naming it.
- **G2. The literal "`cfg(test)` only" sentences.** X3c r7 item 11 ("A fault-injection hook exists only under `cfg(test)`"), X3b r10 item 11, and X4T r9 items 12 and 13 ("the fixture is `cfg(test)`") protect one invariant: the code is absent from every non-test build. Item 2 meets that invariant by other means. Those sentences should be restated as "absent from every non-test build (`cfg(test)` or X9's `crash-matrix` feature)".
- **G3. Read-path points (X6).** F49 needs named holds between `recover`'s bracket reads (`W1 H1 J W2 H2`), and F29, F44 and F45 need `recover` to report its admission and snapshot points. X6 r2 names none. X6a and X6b place item 5's `x6.*` points.
- **G4. Observer and checkpoint points (X4).** Deterministic F18, F19, F38 and F39 need the `x4.*` points, including the observer's `gate`. X4 r7 names none. X4a places them.
- **G5. The sweep's admission under a revoked view.** X6 r2 item 7 says the sweep "takes no X4 guard", but it does not say whether X1's `admit_ordinary_writer`, which the sweep runs first, refuses when a closure subject is revoked. The expected R3 for the F18, F19 and F38 ladders depends on it (C5). It needs an X1 or X6 decision before X9-4.
- **G6. EXIT-PLAN.** The X9 row's "Depends on" omits X2e and X5. The order "X9 (M2 exit)" last hides that X9-0 and X9-1 must precede X3d-2's, X6b's and X7a's composition tests (G1).
- **Not a gap.** X3d item 10's promise of "named, test-only crash points before and after each durability step" is met by item 5. Its "test-only" is item 2's feature.

## Forbidden substitutes

- Any barrier point, `crash_matrix_support` item or `cfg(any(test, feature = "crash-matrix"))` site in a release build, or in a build reached without an explicit `--features crash-matrix`.
- A manifest dependency of any kind that enables `crash-matrix`.
- A sleep, a polling loop or a timeout that decides an outcome. The watchdog only ever records `HARNESS-ERROR`.
- An in-process "crash" (`catch_unwind`, an early return, a simulated state) counted as a process death in the matrix.
- A kill not verified by `SIGKILL` status and by the trace's last held record.
- An expected value read back from a run, or written after it.
- Dropping `injected`, `mutation` or `synthetic` from a run's labels, or reporting a limit row as executed.
- A support function that returns an authority type (`PlatformReceipt`, `ProjectOperation`, `CommitSession`, `ReplayedRun`, `PreparedCommit`, `PublishedCommit`, `RecoveredCommit`, `AdmissionPermit`).
- A `cfg(any(test, feature))` site outside X9-1's pinned list.
- Asserting either refusal or admission of a whole-file `state.v1` restore (L4).
- A durability primitive reached outside a named scope during a matrix run.
- An observer that ticks on its own timer in a matrix child.
- Raw state bytes committed to arch in place of the run records.
- A matrix pass on a dirty worktree, or on a commit other than the reviewed one.

## Not claimed

Power-loss and media qualification, native S6 scheduling bounds and the residual admission window (M6); store and carrier migration and restore; orphan object collection; a measured platform profile row; Linux and non-APFS hosts; X8's compile-fail suite; CLI enablement (X10, X11); any new public code, row or detail; closing X4T r9's whole-file restore limit.
