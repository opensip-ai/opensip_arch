# X9-2 r1 — ACCEPT-UNIT

Unit X9-2 implements X9 r9 item 12's storage scope: the three driver entries, `check-unit`, the commit-matrix drivers and ladder, the 231 transcribed rows, and L11. It adds none of X9-3 through X9-6. Inventory v131 is ACCEPT on v130.

Worktree `/Users/sb/code/opensip-ai/opensip-x9-2` is detached at `cdd4589d30f378114e15d9f74e98d1693e3e0193`. `git diff cdd4589` is 14 files, +1836 −38, sha256 `03f63c41db32d605c78804b0dcd1ff1ae82947c15b8ff2bc6cce4b69729b6e05`. The two new files are intent-to-add. The review left that diff unchanged. The real home was absent before the census, after both matrix sets, and after the inventory verifiers.

Subject manifest `docs/implementation/m2/crash-matrix-x92-inventory-v131-subject.json` is 2109 bytes, sha256 `829066b07362a8be36881dfcaa71395b2f725e9f739ad4ed5f035a3aae005402`.

## Scope

The diff is the X9-2 surface named in item 12, with the r4, r5, r7 and r8 notes.

- Security `crash_matrix_support.rs` adds the three driver entries. `operation` calls `InstallationAt::operation` with `WriterLease::AppendWrite` and keeps the signed test trees on the `SyntheticInstallation`. `recovery_admission` builds the read receipt with `produce_for::<Read>`, allocates `&RECOVERY_ALLOCATED`, and calls `admit_on` over `HomeSource::Fixture`. `settlement_sweep` calls `InstallationAt::admitted_writer` and then `settlement_sweep::admit_on`. Each returns that production composition's value or its refusal.
- `ENTERED` is a process-wide `AtomicBool`, set by the first entry and never cleared. A second call returns the invariant row and does not run the composition. `publish_revocation` refuses once an entry has been made.
- The widened symbols, each to `pub(crate)` and no further, are `recovery_admission::{admit_on, allocate, RECOVERY_ALLOCATED}`, `settlement_sweep::admit_on`, `read_premise::produce_for`, `installation_admission::HomeSource`, and `InstallationAt::admitted_writer`.
- `try_lock` acquires inside `crash_scope!` for `x2.lease.readers` or `x2.lease.writer`, inside the same `work.run(LOCK, …)` step as `lock`.
- `post_state.rs` dumps a UTF-8 SQLite BLOB as `blobText`, records each object name by `shape_string`, and leaves the bytes in `raw`.
- `crash_matrix_sites.rs` adds `crates/storage/tests/commit_tests.rs` to the whole-file support pin and adds that file plus `run_candidate.rs` to the no-sleep pin. Both additions are names on the existing lists.
- Storage `Cargo.toml` gives `commit_tests` `required-features = ["crash-matrix"]`. The new target is under `cfg(all(feature = "crash-matrix", target_os = "macos"))`.
- `commit_tests.rs` is the parent and the child roles: fixture, commit, competitor-writer, recover, reader, sweep, and the one-entry check. The commit child calls `synthetic_run_candidate` and `replay_run` after `CommitSession::open`. The ladder is R1 recover (with `stateUnchanged`), R2 next writer, then R3 sweep and R4 recover, and mutation rows return after R2. `meets` treats a trailing `:*` as a standing prefix and a JSON list as any-of. The file's own comment states that nothing sleeps, polls, or waits, and the no-sleep pin names it.
- `required-runs.v1.json` holds exactly 231 rows: F00 174, F02 3, F03 6, F04 7, F05 6, F07 11, F08 2, F09 3, F10 10, F20 2, F21 1, F22 2, F31 2, F46 2. Schema `opensip.x9.required-runs.v1`, clock epoch 1791072000. No other case is present.
- `check_crash_matrix.py` adds `check-unit` for X9-2, X9-3, X9-4 and X9-5, which is the subset mode item 7's r4 note assigns to this unit. This unit's rows are the X9-2 case list. Limits in `check` and `check-unit` are L1 through L11, in that order. `matrixPass` stays false. The test file has four `check-unit` tests and the L11 refusal, 16 tests in all.

X9-3's recover and sweep censuses, X9-4's lock and revocation rows, X9-5's host target, and X9-6's full `check` are absent. Host `crash_matrix_support.rs` is unchanged.

The accepted proposal's item 7 still has one bullet that names the per-unit limits as L1 to L10. The r9 header, item 10, and item 12's r8 note put L11 on both `check` and `check-unit`. The checker follows those three sentences.

The security and storage module headers still say the surface returns no authority type. The three entries return `ProjectOperation`, `RecoveryAdmission`, and `SettlementSweep`, which is the production result item 6 requires, and the signed trees stay on the `SyntheticInstallation`. Host's unchanged glob still forwards storage's surface.

## r4 constraints

The entries are compiled only with `crash-matrix` and debug assertions. Each crate's `lib.rs` keeps `compile_error!` for `crash-matrix` without `debug_assertions`. A release build of `opensip-storage` with `--features crash-matrix` exited 101 at that guard: "refuses every build without debug assertions". The site list gains the matrix target by name. There is no new `cfg` site. The compositions are the production ones named above, and one entry is admitted per process.

## Transcription

`transcribe_required_runs.py` was rerun on this review's census. `OPENSIP_X9_RUN_SET=x92-grok-census` and `OPENSIP_X9_CENSUS_ONLY=1` wrote the census, the census trace, and r9's reference run, then returned. The script's output is byte-identical to `required-runs.v1.json`: 107235 bytes, sha256 `6a02921123e1d28658934c2cbf9f3b2f4b2636f075de2b624fd67736650c5a18`. The matrix parent reads that file and transcribes nothing.

The census is two unarmed commit-driver runs, asserted equal: 212 points and a kill set of 281. F00's R1 and R4 follow r6's split, with R4 staying UC on the points whose R2 does not create the ledger. F00's R2 follows r8's crash states and r9's one value per X4T dependency occurrence. The reference run supplies the collision set: `create#1`, `write#1` and `write#3` are `operation:Incomplete` (`CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`); `create#4`, `create#7` and `write#6` are Committed. F07, F09, F10, F20–F22, F31, F46 and F04's unequal-collision variant match the law cells the request quotes. The expectations were fixed from the census, the reference run, and the law, before either kill set ran.

## Rerun

Private `TMPDIR` `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T//opensip-x92.9jNTFb` (mode 0700). `CARGO_TARGET_DIR` was under this review directory. `PATH` was Homebrew Rust 1.95.0. Cargo was `--locked --offline`. The two matrix sets ran one after the other. Lead sets `x92-lead-1` and `x92-lead-2` were left in place. Run names were `x92-grok-1` and `x92-grok-2`.

Release absence, produced here and passed in by `OPENSIP_X9_RELEASE_ABSENCE`:

- `cargo build --locked --offline --release -p opensip-cli`, no features. Binary 6315264 bytes, sha256 `b32604fe8c83343a93e7e38f023abc330afda2fa0f7cb255c842ab2b52aa5e49`, the same bytes as the lead record.
- `check_crash_matrix.py release-absence` scanned 26 strings (`OPENSIP_X9_` and the registered scope names) and found none. `passed` is true, `features` is `[]`, `profile` is `release`, `featureBuildRefused` is true.

Each matrix invocation was `cargo test --locked --offline -p opensip-storage --features crash-matrix --test commit_tests x9_2_matrix -- --exact --test-threads=1`. `x92-grok-1` ran from 22:21:53Z to 22:38:17Z. `x92-grok-2` finished in 988.79s and ended at 22:54:46Z. Each set wrote 231 run records, every verdict `PASS`.

`check-unit --unit X9-2` on that pair, with the required-runs fixture and commit `cdd4589d30f378114e15d9f74e98d1693e3e0193`, returned `passed` true, 231 runs, 212 census points, kill set 281, 219 killed points, limits L1 through L11, `repetitionsAgree` true, `matrixPass` false, `productQualification` false.

The canonical map of the 231 `normalizedSha256` values is sha256 `4e5cba342b438abb749f73861161e6cd4cf38e6bdbd992a00068507d5df3ddaa`, equal to `lead-check-unit.json` key for key. Every child's trace object (`records` and `sha256`) is equal across `x92-grok-1`, `x92-grok-2`, `x92-lead-1` and `x92-lead-2`, 231 runs in each. That is the agreement of the lead execution and this review's two executions.

`python3.14 -m unittest tools/tests/test_check_crash_matrix.py` ran 16 tests, OK. The full workspace, clippy, and `cargo fmt` lanes were the lead's; this review's cargo was the release build, the refused feature build, the census, and the two matrix sets.

## Judgment calls

1. Acceptable. `try_lock` now takes the sweep's exclusive lease inside `lock`'s scopes and inside the same charged step. Without the feature the macro is the block alone. The release binary is byte-identical to the lead's and contains none of the scanned scope names, and every traced R3 in these sets passed.
2. Acceptable. The three entries reuse `InstallationAt::operation` and the production `allocate` / `admit_on` paths. Recovery's ledger is `RECOVERY_ALLOCATED`, so a second entry also meets recovery's one-ledger rule. The signed trees are retained on the `SyntheticInstallation`.
3. Acceptable. The commit child replays after `CommitSession::open`, so the first registration can draw the ProjectId inside the operation. The candidate is X3d-3's, already in storage's support module.
4. Acceptable. The 231 rows live at `crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json`, which a later unit can append to and which a host target can read by path.
5. Acceptable. `expected` maps the step keys to a string or a list. A trailing `:*` is used for F20 and F22's unknown-quarantine standings. R1's `stateUnchanged` is recorded and checked when R1 ran. Observed text is the children's own outcome text, including `operation:Incomplete` for the custody row.
6. Acceptable. Each run record lists children in spawn order. Scripts are the arm, kill, mutate, and copy-carrier forms, including F22's resume at `x3c.attempt.begin#1`. `matrix.json` carries this review's release-absence record. The census trace is the commit driver's and is digested like every other child trace. `check-unit` accepted that shape on both sets.
7. Acceptable. The first lead pair's 43 disagreements came from hex-dumped JSON BLOBs and from object-set order derived from the drawn ProjectId. `blobText`, sorted name shapes, and the sweep report ordered by outcome and row close those two escapes. Raw digests remain on each record. These two sets and the lead's final pair agree on every normalized digest and every child trace.
8. Acceptable. The unit sits on `cdd4589`, where X8c is the added host admission tests already in the commit. The lock still selects v130. The release binary matches the lead record byte for byte.

## Inventory v131

Candidate `docs/implementation/m2/repository-file-inventory.v131.json`, 548804 bytes, sha256 `caaada927cf6b10d03ba5743971cf50e393a1b4d52c36d520563f323b8c2626c`.

Parent v130 is the lock's selected inventory: 547706 bytes, sha256 `80e1e2e5028c8d979bfb7e3ccf710fd3a72f0018998ff013c3cb22f7ceb69855`. Successor `docs/implementation/m2/crash-matrix-x92-inventory-v131/successor.json` is 145125 bytes, sha256 `25f2c69725fa8503d3b5b7ab1c8e1ee8d2dc6e22a820527504120cbcbf1377a5`. Its parent pin is that v130 pin. `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`, `packageDependencyGraphUnchanged` and `pendingDecisionsInheritedUnchanged` are true. `addedFiles` is the one fixture row. The description-override projection has 55 rows. The projection rule resolves those fifty-five effective descriptions from inventory130, the sixteen carried from inventory81 onward plus D1's thirty-nine overrides, with D2's four passage supersessions already folded. Standing text is the proposed crash-matrix layout for this unit and asks for independent review and lead assent.

`verify_projection.py` against the worktree lock: `{"readOnly": true, "projectionRows": 55, "positive": "PASS", "corruptionsRefused": 278, "directParentOverrideIncluded": true}`.

`evidence/verify_scratch.py` over this worktree, in memory only: passed, 92 inventory successors, 75 contract successors, 55 inheritance rows, selected inventory v131.

v131 is the candidate. The lock at `cdd4589` still selects v130.
