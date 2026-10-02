Grok review: unit X9-2 r1, the crash matrix's carrier and object rows in storage (law X9 r9 item 12), with inventory v131 on v130. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT**.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x92-r1.
- You own the native lane for this review. Use a CARGO_TARGET_DIR under that directory, and a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
- Run git read-only, and only against the worktree below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Inputs

All inputs are pinned in `hashes.txt`.

### Laws

- **X9 r9:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`, accepted at `e6ff60c1…`. The relevant parts:
  - item 12's X9-2 line, with its r4, r5, r7 and r8 notes;
  - item 6 (the support surface and r4's three driver entries);
  - item 7 (the evidence, and r4's `check-unit`);
  - item 8 (the ladder);
  - item 9 (rows F00, F02–F05, F07–F10, F20–F22, F31 and F46, with r6's split, r8's R2 by crash state and r9's per-occurrence X4T rule);
  - item 10 (L1 to L11);
  - the forbidden substitutes.
- **X6 r4:** the constructors record.
- **X3d r8 and X9 r7:** the synthetic run candidate, landed by X3d-3.
- **EXIT-PLAN:** the M2 known limit, and X9-2 carrying the X6c point fix.

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-x9-2`, detached at main `cdd4589` (X8c, above X3d-3's a2c5e8b). Nothing is committed. The two new files are intent-to-add.
- **Diff:** `git diff cdd4589` is 203916 bytes, sha256 `03f63c41db32d605c78804b0dcd1ff1ae82947c15b8ff2bc6cce4b69729b6e05`. It covers 14 files, +1836 −38.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`.

### Inventory

- `repository-file-inventory.v131.json`
- `crash-matrix-x92-inventory-v131/`
- `crash-matrix-x92-inventory-v131-subject.json`, sha256 `829066b07362a8be36881dfcaa71395b2f725e9f739ad4ed5f035a3aae005402`

They are untracked in arch.

### Lead evidence, in this directory

- **`lead-check-unit.json`:** the checker's `check-unit` result over the two lead run sets, with every run's `normalizedSha256`.
- **`lead-release-absence.json`:** the release-absence record both sets used.
- **`transcribe_required_runs.py`:** the transcription script, run before any kill.

## What X9-2 builds

### Security

- **`crash_matrix_support.rs`: X9 r4 item 6's three driver entries.**
  - `operation(at, root)` calls `InstallationAt::operation(root, AppendWrite)`, the composition X8b's `scenario::operation` also calls.
  - `recovery_admission(at, request)` makes a read receipt over a signed test tree for `at`'s H, then `allocate(&RECOVERY_ALLOCATED)` as `admit` does, then `recovery_admission::admit_on` over `HomeSource::Fixture`.
  - `settlement_sweep(at)` calls `InstallationAt::admitted_writer` and then `settlement_sweep::admit_on`.
  - The process-wide `ENTERED` flag allows one entry per process. A second call refuses on the invariant row without effect.
  - `publish_revocation` refuses in a process that made an entry.
  - The signed test trees live in the `SyntheticInstallation` value.
- **No new cfg site.** Five crate-private items are widened to `pub(crate)` and no further: `recovery_admission::{admit_on, allocate, RECOVERY_ALLOCATED}`, `settlement_sweep::admit_on`, `read_premise::produce_for`, `installation_admission::HomeSource`, and `InstallationAt::admitted_writer`.
- **`custody/namespace_lease.rs`: the X6c point fix** (judgment call 1). `try_lock`, which the sweep's EXCLUSIVE lease uses, now acquires inside the `x2.lease.writer` / `x2.lease.readers` crash scope, as `lock` does, and inside the same `work.run` step. Without the feature `crash_scope!` is its block alone, and the carrier name is bound as `_name`.
- **`crash_matrix_support/post_state.rs`** (judgment call 7):
  - a UTF-8 BLOB is dumped as `blobText`;
  - the object set is recorded by each name's shape, sorted;
  - each object's bytes stay in `raw`.
- **`crash_matrix_sites.rs`:**
  - the matrix target's whole-file support guard is added to the pinned site list, by name;
  - the no-sleep pin names the matrix target and the run candidate.

### Storage

- **`Cargo.toml`.** `[[test]] commit_tests` declares `required-features = ["crash-matrix"]`, so a plain `cargo test` skips it.
- **`tests/commit_tests.rs` (new; whole file under `cfg(all(feature = "crash-matrix", target_os = "macos"))`).**
  - **Child entry.** `matrix_child` serves the drivers:
    - `fixture`, ordinal 0: the synthetic installation, X4T-0's store, and the root `H/code/project`;
    - `commit` and `competitor-writer`: `operation`, `CommitSession::open`, then X3d-3's `synthetic_run_candidate` and `replay_run` after `open` (matrix only), then `prepare_commit`, `publish` and `finish`;
    - `recover` and `reader`: `recovery_admission`, then `recover`;
    - `sweep`: `settlement_sweep`, then `lease` and `sweep_namespace` per namespace, then `release`;
    - `entries`: a check of the one-entry rule.
  - **Parent.** It reads the reviewed required runs and transcribes nothing. Per run it:
    - spawns children under X9-0's driver with the scripted clock, ordinals in spawn order;
    - arms, awaits and kills by blocking record reads, then verifies each death (signal 9, last held, nothing durable after);
    - captures the post state;
    - runs item 8's ladder: R1 recover (with `stateUnchanged` compared), R2 next writer (with its witness action and floor decision read from its trace), R3 sweep, and R4 recover. Mutation rows run R1 and R2 only;
    - scores the observation against the row;
    - writes `runs/<case>-<variant>.json` and `matrix.json` under `target/opensip-x9/<OPENSIP_X9_RUN_SET>/`.
  - **When it runs.** `x9_2_matrix` does nothing unless `OPENSIP_X9_RUN_SET` is set.
  - **Census.** The census is two unarmed runs of the commit driver, asserted equal. `OPENSIP_X9_CENSUS_ONLY` also writes the census trace and r9's reference run.
  - **Lane tests:**
    - `a_process_makes_at_most_one_driver_entry`;
    - `the_commit_driver_census_is_equal_across_two_runs`.
  - **No timed waits.** Nothing sleeps or polls. The no-sleep pin covers the file.
- **`tests/fixtures/crash-matrix/required-runs.v1.json` (new).** X9-2's 231 rows: F00 174, F02 3, F03 6, F04 7, F05 6, F07 11, F08 2, F09 3, F10 10, F20 2, F21 1, F22 2, F31 2 and F46 2.

### Tooling

- **`tools/check_crash_matrix.py`:**
  - `check-unit --unit X9-2|X9-3|X9-4|X9-5` (X9 r4 item 7). It takes the unit's subset by item 12's case lists. Per run, `product.commit` must be the base commit, and `worktreeClean` may be false, for both the runs and `matrix.json`. Every killed point must lie in the kill set, but full coverage is not required. It reports `matrixPass: false`.
  - Limits L1 to L11, in `check` and `check-unit` (r8).
  - `check` is otherwise unchanged.
- **`tools/tests/test_check_crash_matrix.py`:** four `check-unit` tests and L11, for 16 tests in all.

## How the rows were transcribed (before any kill, never read back)

`transcribe_required_runs.py <census.json> <census-trace.txt> <reference.json> <out>` works from three inputs:
- **The census.** Two equal unarmed runs give 212 points and a kill set of 281. They supply the kill points and their order.
- **X9 r9's reference run, on one installation.**
  - (A) An unarmed commit at ordinal 1. Its new `trust/` entries, in APFS birth order, number `dependency/create#k` and, for files, `write#j`.
  - A's publication is then undone: its entries are removed, and `state.v1` gets its earlier bytes back in place.
  - (B) An unarmed commit at ordinal 2 shows the names the next publication writes.
  - Occurrences `create#1`, `write#1` and `write#3` collide with B. Their R2 is `operation:Incomplete`, which is `CONFIG.CUSTODY_REFUSED` with subject `installation-incomplete`. Occurrences `create#4`, `create#7` and `write#6` don't collide, so they are Committed.
- **The law's rows:**
  - **F00 R1 and R4:** r6's split. Before the draw, both are not applicable (a hold at the draw precedes the draw). From the draw through `x3c.ledger-create.ddl.commit.before`, R1 is UC; R4 is UC where R2 doesn't create the ledger, and UAU otherwise. After that point, both are UAU.
  - **F00 R2:** r8's crash states:
    - 44 registration points: `identity-recovery-required`;
    - `marker/create.after`: `marker-custody`;
    - `marker/write.before`: `identity-contradiction`;
    - 5 X3c created-not-private points: `Custody{private}`;
    - the X3b floor directory: `HostIo`;
    - the two WAL-gap points: `LedgerCorrupt`;
    - the three colliding X4T occurrences: `Incomplete`;
    - Committed elsewhere (117 rows).
  - **F07:** OK before `witness-pending/rename.after`, REVERT from it on.
  - **F09:** ADVANCE when the SEAL commit landed, REVERT when it did not.
  - **F10:** ADVANCE before `witness-committed/rename.after`, OK from it on.
  - **F20, F21 and F22:** R1 UQ (F21 `witnesslessRestore`) and R2 `LedgerCorrupt`.
  - **F31:** R2 `HostIo`.
  - **F46:** R1 UCI. The format-1 and format-2 variants only, per r8.
  - **F04:** the unequal-collision variant gives R2 `Refused(LedgerCorrupt)`.

## Lead results

All checks were run on cdd4589 with this diff, with a private TMPDIR.

| Check | Result |
|---|---|
| Full workspace without the feature, run 1 | 1726 passed, 0 failed, 3 ignored |
| Full workspace without the feature, run 2 | 1726 passed, 0 failed, 3 ignored |
| Feature lane: `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets` | 1615 passed, 0 failed, 3 ignored, including the matrix target's 4 tests |
| Clippy `-D warnings` on the workspace (no feature), on those four crates with `crash-matrix`, and on security, storage and host with `scenario-fixtures` | clean |
| `cargo fmt --all --check` | clean |
| `check_package_edges.py --lane host` against v130 and v131 | passed |
| Checker unit tests | 16 OK |

**Lead run sets.** `OPENSIP_X9_RUN_SET=x92-lead-1` and `x92-lead-2`, each with `OPENSIP_X9_RELEASE_ABSENCE=lead-release-absence.json`.
- **Runs:** 231 of 231 PASS in each, with 0 FAIL and 0 HARNESS-ERROR. Each set took about 986 s.
- **check-unit:**

  ```
  check_crash_matrix.py check-unit --repository . --unit X9-2 \
    --run-set target/opensip-x9/x92-lead-1 --repeat target/opensip-x9/x92-lead-2 \
    --required crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json \
    --commit cdd4589d30f378114e15d9f74e98d1693e3e0193
  ```

  Result: passed, 231 runs, census 212 points, kill set 281, 219 killed points, limits L1 to L11, repetitions agree, `matrixPass: false`.
- **Normalized digests:** the 231 `normalizedSha256` values (47 distinct) are in `lead-check-unit.json`. SHA-256 of their canonical map is `4e5cba342b438abb749f73861161e6cd4cf38e6bdbd992a00068507d5df3ddaa`.
- **Release absence:**
  - `opensip-cli` was built in release with no features: `target/release/opensip`, 6315264 bytes, `b32604fe…`.
  - The scan found no `OPENSIP_X9_` string and no registered scope name.
  - `cargo build --release -p opensip-storage --features crash-matrix` exited 101 at the compile guard.
- **Real home:** `~/Library/Application Support/OpenSIP` was absent before and after.

**Inventory v131.**
- **Contents:** v130 plus one row, `required-runs.v1.json` (fixture), giving 965 files with 964 rows equal by value. There is no new edge. Projection is 55 rows with `supersessionsFolded: 0`.
- **Checks:**
  - `verify_projection.py` against the lock at cdd4589: PASS, 55 rows, 278 corruptions refused.
  - `evidence/verify_scratch.py` over this worktree: passed, with 92 inventory successors, 75 contract successors and 55 inheritance rows, and v131 selected.
- **Lock:** the lock at cdd4589 is byte-identical to a2c5e8b's, so it still selects v130.

## Judgment calls

1. **The X6c point fix, carried here (coordinator's decision; EXIT-PLAN).**
   - **The defect:** `try_lock` took the sweep's EXCLUSIVE lease locks outside any scope, so every traced R3 child was a `HARNESS-ERROR` under item 5.
   - **The fix:** the scope is `lock`'s own, inside the same charged step.
   - **Without the feature:** it is the block alone, so behaviour is unchanged.
2. **Three driver entries and five `pub(crate)` widenings.**
   - **What they reuse:** `operation` reuses X8b's `InstallationAt::operation`.
   - **Recovery's ledger:** allocated by recovery's own `allocate(&RECOVERY_ALLOCATED)`, not the `cfg(test)` `allocate_for_tests`, so a second entry in the same process also meets recovery's own one-ledger rule.
   - **Signed test trees:** owned by the `SyntheticInstallation` value, because the entry returns only the production result.
3. **Matrix-only replay order (X9 r5).** The commit driver replays after `open`, because a first registration draws the ProjectId inside the operation.
4. **Where the required runs live:** `crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json`. Later units append to it, and host's X9-5 target can read it by path.
5. **Expected-value encoding.** A row's `expected` maps step keys to a string or a list of admitted strings, where a list is "whichever the state left", as r6 and r8 phrase it.
   - **Step keys:** `scripted`, `attemptRows`, `R1`, `R2.witnessAction`, `R2.outcome`, `R3`, `R4`.
   - **`:*` suffix:** a trailing `:*` admits any typed member after the standing. Only F20 and F22's UQ use it, because X6 gives no reason for them.
   - **Always checked:** R1's `stateUnchanged`.
   - **Observed strings:** the children's own outcome text, normalized. For example, `operation:ProjectRootCustody { subject: "…" }` is the `InstallationTermination` the operation entry returned.
6. **Run-set layout.**
   - **Records:** one record per run, with every child in spawn order: fixture, scripted child, then R1 to R4.
   - **Scripts:** `arm` / `await…then kill` / `mutate` / `then copy-carrier-and-resume`. F22's earlier carrier is copied at a resumed hold at `x3c.attempt.begin#1`.
   - **Release absence:** `matrix.json` carries the lane's release-absence record, passed by path.
   - **Census:** the census is the commit driver's (r8). Its trace digest is normalized like every child's.
7. **Normalization, beyond r8's trace rule.**
   - **The issue:** a first lead pair passed every run but disagreed on 43 runs.
   - **The cause:** two places where drawn values escaped item 7's normalizer:
     - JSON bodies stored as SQLite BLOBs (association and Run material) were dumped as hex;
     - the object set's listing order is a permutation of content digests derived from the drawn ProjectId.
   - **The fix:** BLOB text is now dumped as text, the object set is recorded by name shape, sorted, and the bytes stay in `raw`. The sweep driver's report is also ordered by outcome.
   - **Effect:** nothing compared is dropped, and every run's raw digests stay in its record.
   - **Result:** the final pair agrees on every run.
8. **Rebased onto cdd4589 before the final runs.** X8c landed there, adding only `crates/host/tests/admission_tests.rs`. The lock and `verify_design` are byte-identical to a2c5e8b's, so the parent stays v130. The release binary is byte-identical.

## Decide

- Does X9-2 implement X9 r9's X9-2 scope faithfully, and nothing of X9-3 to X9-6? That scope covers:
  - the entries;
  - `check-unit`;
  - the drivers and the ladder;
  - the rows as transcribed;
  - L11.
- Do the entries stay within r4's constraints?
  - test-only, crash-matrix only;
  - no cfg site;
  - production compositions only;
  - one entry per process.
- Is the transcription lawful? It must use only the census, r9's reference run and the law, fixed before any kill.
- **Rerun and compare:**
  1. Rerun the transcription inputs (`OPENSIP_X9_CENSUS_ONLY=1`).
  2. Run the matrix twice yourself, under `OPENSIP_X9_RUN_SET` names of your choice, with your own release-absence record (build, scan, refused feature build).
  3. Run `check-unit` on your pair.
  4. Compare your `normalizedSha256` per run, and the child trace digests, with `lead-check-unit.json` and the lead's run records. Agreement across the three executions is the determinism evidence.
- Are judgment calls 1 to 8 acceptable?
- **Inventory v131:** pin it, and assess it as an inventory candidate.

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectManifestSha256": `829066b07362a8be36881dfcaa71395b2f725e9f739ad4ed5f035a3aae005402`, as a single string;
- "inventoryCandidateAssessment": verdict, requiredFindings, the candidate's path, bytes and sha256, parent (v130's pin), and successorRecord (the pin of `crash-matrix-x92-inventory-v131/successor.json`).

Do not commit.
