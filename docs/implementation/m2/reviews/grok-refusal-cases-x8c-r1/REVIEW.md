# X8c r1 — behavioural cases B0–B8

**Verdict: ACCEPT.**

The subject is the uncommitted diff of `/Users/sb/code/opensip-ai/opensip-x8c` against `a2c5e8b4a72100c2bb22895690cc5487f9f79a6f`. It is one file, `crates/host/tests/admission_tests.rs`, 1025 insertions and 1 deletion. `subject.diff` is 45278 bytes, sha256 `8b394a1b8a9c7f2079a9c49b43394c0cf48c60676da356322f3f4e3e9d6b712f`. The deletion is the header comment, which gains one sentence naming X8c. No product source, manifest, lock, feature, or edge changes. No file is added. The inventory row for `admission_tests.rs` in `repository-file-inventory.v130.json` already describes replay-invalid Runs, revoked authority, and stale fences, and its role stays `test`. There is no inventory successor. The verdict on the diff is ACCEPT.

Laws were read at the bytes pinned in `hashes.txt`. X8 r4 is `d8166e48e` (`refusal-suite-x8/PROPOSAL.md`, 46674 bytes, `187c162e…`). EXIT-PLAN is `f5b54e861^` (26052 bytes, `38bfa9a6…`). The crash-matrix pin `e6ff60c1…` (95579 bytes) is `crash-matrix-x9/PROPOSAL-r9.md`; its item 6 candidate rule, item 3 helper shape, and matrix order are the text this unit relies on. Product inputs (the test file, `run_candidate.rs`, both `schema_sources.rs`, and host `replay-fixtures.json`) match their pins. The live arch copies of X8, EXIT-PLAN, and the X9 proposal have moved since the pin (an X8 r5 draft, the review-queue note, and an acceptance stamp). This review judges the pinned bytes.

## Cases

Each case is an ordinary `#[test]` under `cfg(target_os = "macos")`, on its own `ScenarioHome`, driving `scenario::operation`, `CommitSession::open`, `replay_run`, `prepare_commit`, `publish`, and `finish`. B0 is a real control on that harness: the synthetic candidate replays, its evaluator closure equals `CommitSession::core_evaluator_closure()` and differs from `core_closure()`, `prepare_commit` and `publish` return `Committed` with `latched_after_admission() == false`, the RunId, ExecutionId, and sequence 1 match, and `authoritative_run` names that RunId. After `finish` the census is SEAL 1, REV 0, CLN 0, one receipt, and one attempt row for the ExecutionId. The end step was entered, with no REV, CLN, or settlement failure.

B1 replays host `replay-fixtures.json` case `packet-1-original` and shows its `projectId` differs from the session. `prepare_commit` returns `NotPrepared::Refused(Invariant)`. The public projection is `SYSTEM.OUTCOME.ILLEGAL_STATE` / `HOST.INVARIANT_VIOLATED` / no subject. The ledger is absent. B2 uses X3d-3's `project_rebound_corpus(session.project_id())`: the project binds, and the evaluator closure equals neither `core_evaluator_closure()` nor `core_closure()`. The same invariant row and the same census follow. That is the EXIT-PLAN correction (compare against the core evaluator closure; owner “X3d-2, binding X3d-3”). B6 still publishes the core closure.

B3 replaces `.opensip/project-id.v1`, and separately N's `writer.lease`, after the handoff and `open`, with `cp -p` and a rename of the same bytes, so the identity changes and the mode is unchanged. `prepare_commit` admits the attempt. `publish` returns `Refused(Custody { subject: "required-files-changed" })`, projected as `CONFIG.INVALID` / `CONFIG.CUSTODY_REFUSED` / `required-files-changed`. Census: SEAL 0, REV 1, CLN 0, the attempt row `admitted`, zero receipts. B5 replaces the selected lineage node with the same canonical node at `storeGeneration + 1` and takes that same custody row and census. X3d item 7 owes a CLN for a durable SEAL left without its evidence commit. These refusals leave no SEAL, so the owed CLN count is zero. The gate latch is what owes the REV.

B4 plants an `admitted` attempt for `session.execution_id()` through `plant_attempt` before `prepare_commit`. The outcome is `NotPrepared::ExistingAttempt` for that ExecutionId. `requested` matches the session's namespace, carrier digest, and operationRef, and the store-generation digest is 64 hex digits. X6 r3 item 6 and X7 r4 item 3 keep this outcome on the invariant row in the writer's invocation. At this facade the outcome carries no `InstallationTermination`; the case spells the 468c projection of `Invariant` (`SYSTEM.OUTCOME.ILLEGAL_STATE` / `HOST.INVARIANT_VIOLATED`, subject absent). X7a's projector, already pinned in `finalization_tests.rs`, places the ExecutionId in the subject and discloses the binding beside that row. The binding members are asserted on `requested` here. After `finish` the ledger census equals the census taken immediately after planting, receipts stay 0, and the carrier is SEAL 0, REV 1, CLN 0.

B6, after the handoff and `open`, has the helper publish `[("release", session.core_closure())]` and waits for that process to exit before `prepare_commit`. `publish` returns `Refused(RevokedDuringOperation { subject: "trust-revoked" })`, projected as `EXTENSION.ADMISSION_REJECTED` / `TRUST.COMPONENT_REVOKED_DURING_OPERATION` / `trust-revoked`. The census matches B3. X4a's `a_revoking_update_latches_through_the_observer_and_refuses_the_checkpoint` publishes the same `("release", selected_core().0)` pair and records `StopCause::Revoked { subject: "trust-revoked" }`. The checkpoint names that first cause when the observer has already latched, and the checkpoint's own observation records the same cause when it runs first (`a_revoking_update_is_seen_by_the_checkpoints_own_final_observation`). The observer charges a separate per-observation ledger and appends nothing (`operation_guard.rs`; X4 r7 item 5). `record` keeps the first `StopCause`, so a later `AlreadyStopped` returns the revocation already recorded. The attempt ledger stays open until `publish`'s checkpoint returns the refusal. Both orders produce this row and this census. The case sleeps nowhere; the wait is `Command::output()`.

B7 has the helper publish `[]`. The outcome is `Committed`, not latched, with B0's census, and the helper's version checks show the revocation version advanced. B8 alters one byte of a claimed output on `selected-complete-file-positive` after the unaltered Run replays, and `replay_run` returns `Mismatch { key: "EVALUATOR_COMPLETE_PROOF_REPLAY", target: None }`. The case calls no `operation`. The project root has no `.opensip`, `I/host/projects` has no entry, and `I/stores/S/projects` is absent.

Every refusal calls `refused_end`: one REV, no CLN, no settlement failure, and the end step not entered. X3d item 7 step 3 treats an end step skipped because the attempt ledger is closed as outside the failure disclosure. B0 and B7 assert the end step was entered.

## Item 5a

`x8_helper_publish_revocation` is an ordinary `#[test]` at the crate root, with no `#[ignore]`. It returns at once unless `OPENSIP_X8_HELPER` is set, so the lane's own run passes it without publishing. The parent runs `current_exe() --exact x8_helper_publish_revocation --nocapture --test-threads=1` after `env_clear()`, with only `OPENSIP_X8_HELPER=publish-revocation`, `OPENSIP_X8_INPUT`, and `TMPDIR`. The helper opens the home by path and calls `scenario::publish_revocation_fenced`. That function refuses, writing nothing, when `LEASE_HANDED_OUT` is set. The flag is process-local and is set only by `scenario::operation`. The helper never calls `operation`. It writes one `X8|published|<before>|<after>` line to stderr. The parent requires success, the harness lines for one test run (`running 1 test`, the named test `ok`, and `1 passed; 0 failed; 0 ignored`), exactly one record, `after > before`, `before` equal to `revocation_version` read before the spawn, and the version after exit equal to `after`. Then it calls `prepare_commit`.

## Judgment calls

1. **B0's Run route is the narrowest lawful one.** The candidate lives in storage `crash_matrix_support`, gated `all(feature = "crash-matrix", target_os = "macos")`. X9 item 2 forbids any manifest from enabling `crash-matrix`. The file's only `crate::` reference is `crate::schema_sources::registry()`. The host test crate supplies that function over public `embedded_schema_registry()`, and `the_candidate_registry_is_storages_selected_registry` pins that host and storage `SOURCES` name the same 48 files in order. `CommitSession::core_evaluator_closure_preimages` is `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`, which is X8 item 4b's shared site list. X9 item 6's sentence that an entry is never compiled under `scenario-fixtures` alone governs the three driver entries, which return a `ProjectOperation`, a `RecoveryAdmission`, or a `SettlementSweep`. The included copy is a module of the host test crate, brought in by the same `#[path]` storage's `commit_tests.rs` uses, and it returns inputs for `replay_run`. Widening the support gate or the site list, enabling `crash-matrix` from host, or copying the candidate would each be a larger change. This route changes no product file, cfg site, feature, export, or law.

2. **Replay order.** B0–B7 replay after `CommitSession::open`, in the order item 5 lists. A first registration draws the ProjectId inside the operation (EXIT-PLAN limit (a)). Replay takes no custody. B8 replays with no `operation` call, which is X5 r3 item 3: a replay refusal ends before a project fence, lease, attempt, or journal effect. Host `finalize` is untouched.

3. **Corpus.** `crates/evaluator/tests/fixtures` holds policy-pack fixtures and no Run. The cases read host's pinned `crates/host/tests/fixtures/replay-fixtures.json`. B1 uses `packet-1-original`. The candidate is built from `packet-0-original` inside `run_candidate.rs`. B8 uses `selected-complete-file-positive`, a Run that has a finding. Record note (b).

4. **REV on B1, B2, and B4.** The B table's census for those rows lists no REV. X3d r6 item 7, as integrated, has `finish` append a REV when the gate is latched, and every certain refusal before admission latches the gate. The cases assert REV 1 and CLN 0. That is the end path's count added to the table. Record note (c).

5. **End step.** Refusals assert the end step was skipped and that the skip is undisclosed. B0 and B7 assert it was entered. This matches item 7 step 3.

6. **B8's one byte.** The alteration changes the last byte of one finding's `messageCode` in the finding and in its parameter blob, and the helper asserts the blob differs by exactly one byte. The blob is retained under the new raw digest. The finding and every object that names it are re-keyed to a fixpoint, with sorted id arrays kept sorted. The original objects and blob stay in the pools. `replay_run` then returns the proof-replay mismatch. That is the corpus's forged-output shape, and it is what reaches `Mismatch` rather than an earlier identity, schema, or join refusal.

7. **Drift and the gate at the public boundary.** `OperationGuard::drift` is `pub(crate)`. `PublishedCommit`, `SessionEnd`, and both `scenario` modules expose no drift reader. B7 asserts the version advance, `Committed`, the latch clear, and B0's census. X4a `operation_live_tests.rs` line 480 asserts `drift() == ["revocation-unrelated"]` for an unrelated publication. B6 shows `Refused` on the revocation row, and `finish` appends the REV a latched gate owes. The numeric `0 → 2` transition stays inside the guard. Record note (d).

8. **Where the alteration happens.** B3, B5, B6, and B7 alter after the handoff and `open`, then build the candidate, then call `prepare_commit` and `publish`. `open` is what exposes `core_closure()`; `ProjectOperation` has no public getter. The refusal is `publish`'s first checkpoint, with the attempt row already admitted, which is the table's census. Call 8's observer race is the pair of orders in judgment above. The case does not sleep, poll, or read a clock.

9. **Replaced.** B3's `cp -p` plus rename changes the inode and keeps the mode and the bytes. B5 also changes the generation. All three land on the custody row in item 8 of X4 r7.

10. **Scratch.** Each process creates `<TMPDIR>/opensip-test/x8c-<pid>-<draw>/<case>/{homes,helper}` once, for every case, before any case walks. The scenario home is created under `homes`. Security's `test_scratch` lock is an in-process mutex held by the test thread from `ScenarioHome::create` until that thread ends, so the cases run one at a time. The helper's `TMPDIR` and input file are `helper`, beside `homes`. A file created there is outside every ancestor of H. The helper's `ScenarioHome::open` takes no fixture lock, so it cannot wait on the parent's mutex. The cases do not call `churned`. `ReadFixture::new_in` still has its existing parent-churn `settle`, which sleeps only after a parent-preparation refusal; that is the creator path `ScenarioHome::create` already uses, and the private parent is what keeps that path from firing.

11. **Inventory.** No file is added and no role changes. The v130 description already covers these cases. `check_package_edges --lane host` against `repository-file-inventory.v130.json` passes, with 22 declared and 20 resolved internal edges.

## Record notes for X8's next record-only revision

None of these changes an outcome:

- (a) B2 compares against `CommitSession::core_evaluator_closure()` (X3d r8, EC1). The owner is “X3d-2, binding X3d-3”. B6 still names the core closure.
- (b) Item 5 names `crates/evaluator/tests/fixtures`. That directory holds no Run. The cases use host `crates/host/tests/fixtures/replay-fixtures.json`.
- (c) B1, B2, and B4 assert the REV that `finish` appends for a gate latched by a certain refusal before admission. The B table's census for those rows does not yet list it.
- (d) B7's `revocation-unrelated` drift and B6's gate transition `0 → 2` are visible on `OperationGuard`, which is crate-private. At the public boundary B7 is a commit with an advanced revocation version, and B6 is `Refused` on the revocation row with the REV `finish` owes a latched gate.
- (e) B0's Run is storage's synthetic candidate, included by `#[path]` with a test-crate registry shim over host's public embedded registry. The 48-source pin is `the_candidate_registry_is_storages_selected_registry`.

## Checks

Private `TMPDIR` mode 0700 under `DARWIN_USER_TEMP_DIR`. `CARGO_TARGET_DIR` under this review directory, removed after the runs. `cargo --locked --offline`.

- Workspace `--all-targets`, twice: 1726 passed, 0 failed, 3 ignored. All twelve new tests passed in the first run, including `x8_helper_publish_revocation` with the helper variable unset.
- Crash-matrix lane (platform, security, storage, host, `--all-targets`): 1611 passed, 0 failed, 3 ignored. The same twelve passed there.
- Scenario lane (security and storage, `--all-targets`): 1139 passed, 0 failed, 2 ignored.
- `cargo clippy -D warnings` clean for the workspace `--all-targets`, the four crates with `crash-matrix`, and security plus storage with `scenario-fixtures`.
- `cargo fmt --all --check` clean.
- Package edges as above.
- `~/Library/Application Support/OpenSIP` was absent before the runs and after them.

Nothing else in the diff is wrong.
