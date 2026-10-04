Grok review: unit X9-6 r1, the crash matrix's M2 exit (law X9 r16 item 12). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT**. The unit adds no file, so there is no inventory candidate: the selected inventory v134 already lists every file it touches.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x96-r1.
- You own the native lane for this review:
  - Use a CARGO_TARGET_DIR under that directory.
  - Use a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
  - Run nothing in parallel with the matrix sets. 45 runs arm the observer tick, and their timing guard measures elapsed time. No other reviewer or worktree may run matrix sets at the same time.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Inputs

All inputs are pinned in `hashes.txt`.

### Laws

- **X9 r16:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL-r16.md`, accepted by you, sha256 `f08efe95…`. `PROPOSAL.md` holds the same text plus the acceptance line.

  The relevant parts:
  - **the r16 header, which was written for this unit:**
    - the 50 coverage rows and their window table;
    - the `"X9-6"` unit value;
    - the union occurrence counts;
    - X9-6's storage census;
    - item 8's release-order verdict condition;
    - the evidence layout;
  - item 12's X9-6 line, with its r10 and r16 notes;
  - item 5, with its census, r8's census scope, and r10, r11, r15 and r16's notes;
  - item 7: `check`, r10's two files, r15's `unit` member, the evidence and how the review checks it;
  - item 8, with r16's note;
  - item 9's cells F02, F07, F11, F13, F14, F16, F17, F19 and F53, with their r16 notes;
  - item 10 (L1 to L11);
  - item 11 (the timing guard);
  - the forbidden substitutes, especially "A matrix pass on a dirty worktree, or on a commit other than the reviewed one".
- **The owning laws the new rows transcribe:** X3b, X3c, X3d r8, X4 r7, X6 r4 with X6c, X7, and the owner's `commit-recovery-readonly.v3.md`. Each r16 window takes the expected values of that window's existing row.

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-x9-6`, detached at main `2967905d8152a5f2e431cd8006e1b82f898c3fe2` (L1 integrated, inventory v134). Nothing is committed, and there are no new files.
- **Diff:** `git diff 2967905` is 522499 bytes, sha256 `d68bcdf9e0e0203e5b563f298c57834632899d11c3f8332c7af345b94032430e`. It covers 6 files, +748 −91. Most of the bytes are the two one-line required-runs fixtures.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`.

### Inventory

- **No candidate.** X9-6 adds no file. All six files it changes are rows of `repository-file-inventory.v134.json`, which the lock at `2967905` selects:
  - `crates/storage/tests/commit_tests.rs`;
  - `crates/host/tests/commit_matrix_tests.rs`;
  - both `tests/fixtures/crash-matrix/required-runs.v1.json`;
  - `tools/check_crash_matrix.py` and its test.
- **Recommendation:** ACCEPT on the diff, with no inventory successor.

### Lead evidence, in this directory

- **`lead-precheck.json`:** the pre-integration two-target check over the two lead sets, with each target's census, kill set and every run's `normalizedSha256`. It is produced by `precheck_x96.py` and is **not a matrix pass** (see "The gate and the clean commit" below).
- **`lead-check-refusal.txt`:** the real `check` over the same sets. It refuses with "storage: matrix product is not the reviewed clean commit", as the law requires for an uncommitted unit.
- **`lead-release-absence.json`:** the release-absence record every set used. It is byte-identical to X9-2's to X9-5's (`538a10c4…`).
- **`transcribe_x96.py`:** the transcription of r16's 50 rows. It appends to the landed required-runs files at `2967905`.
- **`coverage.json`:** step 0's coverage report, made before transcription. It lists the 50 uncovered points by scope, with their census counts and windows.

## What X9-6 builds

### `tools/check_crash_matrix.py` and its test (r10, r15, r16)

- **`check` is the two-target gate.** It takes `--target NAME REQUIRED RUN_SET REPEAT` for `storage` and `host`, exactly once each, and implements it as `check_targets`.
  - Each target's sets are checked as before. The commit must be the reviewed one with a clean worktree, and per-set coverage is deferred.
  - The two files must have one `clockEpoch`.
  - The two repetitions must agree per target.
  - **The union census** (r10, r11): points are joined by name, each at its largest count, and durability must be equal across targets. Its kill set must be wholly killed by process-death runs of either target, in each repetition.
  - **It reports** `matrixPass: true` only for the two targets, `productQualification: false`, per-target `normalizedSha256` maps, and `killedOutsideKillSet`.
  - The one-pair `check()` function stays for the regression controls and `check-unit`, which is unchanged.
- **`coverage`.** It takes each target's census and its required runs, runs nothing, and reports the union kill set and every point no row kills.
- **The `"X9-6"` unit value** (r16). `UNIT_VALUES` is the four unit names plus X9-6. An X9-6 row is in no unit's subset, and `check` requires it. `check-unit` does not offer `--unit X9-6`.
- **Tests.** There are 26 tests, all OK. The new ones cover:
  - union coverage across targets;
  - an uncovered union point;
  - a larger occurrence count in the other target;
  - one clock epoch and one name per target;
  - per-target per-run checks and repetitions;
  - the CLI needing both targets;
  - `coverage`;
  - the X9-6 unit value.

### Storage `tests/commit_tests.rs`

- **`x9_6_matrix`.** It runs every storage row (381) with X9-6's storage census (r16): X9-3's commit, recover and sweep, then X9-4's refused end. Each runs twice and must be equal.
- **The union routines.** `union_census` is now the one union routine of `x93_census`, `x94_census` and `x96_census`, moved verbatim. `commit_part` is factored out of `x94_parts`.
- **Selection.** `run_matrix` delegates to `run_matrix_where`. X9-2, X9-3 and X9-4's selection (`owned`) is unchanged, and it already excludes `"X9-6"` rows.
- **The release-order condition (r16, item 8).** `release_order_misses` runs on every recorded child whose outcome starts `Committed`. Its misses turn a PASS into FAIL, as R1's `stateUnchanged` does. It checks:
  - **acquisition:** `x3b.append.seal.begin` < `x3c.evidence.begin` < `x3b.append.seal.level-four`;
  - **release:** `x3c.evidence.commit.after` < `seal.release-level-four` < `seal.release-level-three` < the first `x2.lease.writer/unlock.after` after it < the first `x2.fence.end/unlock.after` after that;
  - **owed records:** any `REV` or `CLN` append releases level 4, then level 3, before that lease release.
- **Tests:**
  - `the_release_order_condition_reads_a_commit_childs_trace`: the lawful order, three reversals, a missing fence and a missing evidence `COMMIT`.
  - `the_commit_driver_census_is_equal_across_two_runs` now also asserts the condition on the real census commit.

### Host `tests/commit_matrix_tests.rs`

- **`x9_6_matrix`.** It runs every host row (98) with X9-5's host census.
- **`x9_5_matrix`.** It now runs only rows without a `unit` member, that is X9-5's 94. Both share `run_host_matrix`.
- **The release-order condition** is the same function, applied to every child whose outcome starts `kind=authoritative`.

### The two required-runs files (r16)

- **Contents:**
  - **Storage:** 381 rows, with the 335 landed rows byte for byte. 191655 bytes, sha256 `14a275ad…`.
  - **Host:** 98 rows, with the 94 landed rows byte for byte. 53953 bytes, sha256 `80e4a02e…`.
- **The new rows.** Each of the 50 carries `"unit": "X9-6"`.
- **How they were transcribed.** `transcribe_x96.py` ran on step 0's census before any run. It places each point by its census-trace position, with r16's windows and the expected values of each window's existing row.
  - The F19 and F53 rows substitute the kill point into the landed rows' scripts: `kill-x3b-append-rev-begin-1-after-revoke`, `kill-x6-sweep-settle-commit-before-1` and `-after-1`.
  - The script asserts that the old `runs` array's bytes are unchanged inside the new file.
  - The windows: W1a 9, W1b 8, W2 12, W3 3, W4 6, W5 2, W6a 4, W6b 2, W7 4, as r16's table gives.
  - After transcription, `coverage` reports 383 of 383 kill-set points killed and nothing outside.

## Lead results

Everything ran on `2967905` with this diff, a private 0700 TMPDIR, and nothing else running. The real home stayed absent.

### Step 0, the census (before transcription)

| Census | Result |
|---|---|
| Storage | 259 points; trace 1379 records, `e9add21e…`; `census.json` `6fa3cc02…` |
| Host | 218 points; `census.json` `2492cbd0…`, byte-identical to X9-5's accepted census |
| Union | 321 points; kill set 383, of which the landed rows killed 333 |

### Development runs

- **`x96-dev1`.** The 50 new rows alone, selected through `OPENSIP_X9_ROWS`:
  - storage: 46 of 46 PASS, in 313 s;
  - host: 4 of 4 PASS, in 72 s.

  Every r16 prediction held, F11's and F07's witness action OK included.
- **`x96-dev2`.** A full pass of both targets with the release-order condition active:
  - storage: 381 of 381 PASS, in 1872 s;
  - host: 98 of 98 PASS, in 789 s.

  No commit child broke the guard order.

### The lead sets

- **How they ran:** `x96-lead-1`, then `x96-lead-2`, one at a time, each covering both targets, each with `OPENSIP_X9_RELEASE_ABSENCE=<lead-release-absence.json>`:

  ```
  OPENSIP_X9_RUN_SET=x96-lead-<n>-storage cargo test --locked --offline -p opensip-storage --features crash-matrix --test commit_tests x9_6_matrix -- --exact --test-threads=1
  OPENSIP_X9_RUN_SET=x96-lead-<n>-host    cargo test --locked --offline -p opensip-host --features crash-matrix --test commit_matrix_tests x9_6_matrix -- --exact --test-threads=1
  ```

- **Results:**

  | Set | Target | Runs | Time | `matrix.json` |
  |---|---|---|---|---|
  | `x96-lead-1` | storage | 381 of 381 PASS | 1890 s | `fac161ae…` |
  | `x96-lead-1` | host | 98 of 98 PASS | 792 s | `30e237a8…` |
  | `x96-lead-2` | storage | 381 of 381 PASS | 1892 s | `d6e3f569…` |
  | `x96-lead-2` | host | 98 of 98 PASS | 787 s | `7dc5461d…` |

- **Timing guard.**
  - Storage: 43 tick-armed runs measured 2,572 to 2,834 ms.
  - Host: 2 tick-armed runs measured 1,103 to 1,113 ms.
  - All are under 5,000 ms.
- **The pre-integration check** (`precheck_x96.py`, `lead-precheck.json`):
  - 479 runs;
  - storage: census 259 points, kill set 321, 305 points killed;
  - host: census 218 points, kill set 271, 81 points killed;
  - **union: 321 points, kill set 383, all 383 killed in each repetition**;
  - limits L1 to L11;
  - repetitions agree on the census, every `normalizedSha256` and every child trace digest.
- **Normalized maps** (the SHA-256 of the canonical map):
  - storage `1e094ddb…` (88 distinct values);
  - host `ede9384c…` (18 distinct values).
- **Against the accepted units.** The 429 landed rows' `normalizedSha256` values equal the accepted lead maps key for key: X9-2's 231, X9-3's 57, X9-4's 47 and X9-5's 94, with 0 differences. This is the regression evidence for the refactor and the new condition.
- **The real `check`** refuses on the dirty worktree, as it must (`lead-check-refusal.txt`).

### Run-record sizes (r16's evidence rule)

- **One full set** is storage 18,315,677 bytes (381 records) plus host 3,839,602 bytes (98). Records run from 40 to 86 KB.
- **Under r16's 64 MB per target,** so `runs/` goes as plain files.
- **The scratch evidence tree.** The lead built it per r16, under the scratchpad and not in arch: 490 files, 23 MB, with `hashes.txt`.

### Lanes

| Check | Result |
|---|---|
| `cargo fmt --all --check` | Clean |
| Workspace without the feature, run 1 | 1744 passed, 0 failed, 3 ignored |
| Workspace without the feature, run 2 | 1744 passed, 0 failed, 3 ignored |
| Feature lane: `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets` | 1624 passed, 0 failed, 3 ignored |
| Clippy `-D warnings`: workspace; the four crates with `crash-matrix`; security, storage and host with `scenario-fixtures` | Clean |
| `check_package_edges.py --lane host` against v134 | Passed |
| Checker unit tests | 26 OK |

### Release absence

- `opensip-cli` was built in release with no features: 6315264 bytes, `b32604fe…`, the same bytes as X9-2 to X9-5. The scan found no `OPENSIP_X9_` string and none of the 25 scope names.
- `cargo build --release -p opensip-storage --features crash-matrix` and `-p opensip-host --features crash-matrix` each exited 101 at the compile guard.

## The gate and the clean commit

- **Why no matrix pass yet.** Item 7 and the forbidden substitutes refuse "a matrix pass on a dirty worktree, or on a commit other than the reviewed one". Item 12 asks for "two full lead runs on one integrated commit". This unit is reviewed uncommitted, so its lead sets record `worktreeClean: false`. The real `check` refuses them, and that refusal is correct. `precheck_x96.py` applies every other condition of `check` through the checker's own functions, and it reports `matrixPass: false`.
- **What remains after your acceptance:**
  1. The lead integrates this diff as main commit C.
  2. On C, with a clean checkout, the lead runs release absence, two full sets and the real `check`. `matrixPass: true` is expected, because the same bytes produced the agreement above.
  3. The lead writes r16's evidence record to `crash-matrix-x9/evidence/<C>/`.
  4. Your rerun on C is the third execution (item 7). It will be a short recheck request after integration.
- **Your choice of when to rerun.** If you prefer a single rerun, run your two sets on C after integration instead of now, and say so in your review. In that case, this review covers the diff and the lead's pre-integration evidence.

## Judgment calls

1. **The storage census composition** (r16, record): X9-3's commit, recover and sweep parts, then X9-4's refused end. The lines go in that order, each part ×2 and equal.
2. **The release-order condition's reading:**
   - each step is its point's first record in the process-wide sequence;
   - the lease and fence releases are the first after the SEAL's level-3 release;
   - it applies to every child whose outcome is a commit (`Committed…`, including a latched F39, or `kind=authoritative`), and to no killed or refused child;
   - a miss is a verdict FAIL, not a row value.
3. **Host's `x9_5_matrix` excludes rows with a `unit` member,** so X9-5's accepted run set and `check-unit --unit X9-5` are unchanged. `x9_6_matrix` runs all rows.
4. **`union_census` and `commit_part` are refactors,** with the logic moved verbatim. The evidence is the equal normalized maps against X9-3's and X9-4's accepted sets above.
5. **The CLI `check` now requires both targets.** The single-pair Python `check()` stays for the regression controls and `check-unit`.
6. **`coverage`** is a read-only transcription aid and never a matrix pass.
7. **Transcription by census position.** The W5 and W6 rows reuse the landed F19 and F53 scripts with only the kill point substituted, so their scripts are the law's existing ones.
8. **`precheck_x96.py`** lives in this directory, not in the product. It is a diagnostic over the checker's functions, and it does not bypass `check`.
9. **F11's witness action OK** (r16's added scored value) held in dev1, dev2 and both lead sets.

## Decide

- **Scope:** does X9-6 implement X9 r16's X9-6 scope faithfully? That scope covers:
  - the two-target `check` and `coverage`;
  - the `"X9-6"` unit;
  - the storage driver and census;
  - the host driver;
  - the release-order verdict condition;
  - the 50 rows as r16's window table gives them.
- **Constraints:** test-only, crash-matrix only, no product source, no new cfg site, no authority type, and one entry per process.
- **Transcription:** is it lawful? It must work from step 0's census and r16 only, before any run, with the prior rows byte for byte.
- **Rerun and compare:**
  1. Run both censuses (`OPENSIP_X9_CENSUS_ONLY=1` with storage's `x9_6_matrix` and host's `x9_5_matrix`).
  2. Rerun `transcribe_x96.py` on `git show 2967905:` of both required-runs files and those censuses. It must reproduce both fixtures.
  3. Run `coverage`. It must show 0 uncovered.
  4. Make your own release-absence record.
  5. Run two full sets yourself, one at a time, each covering both targets, with nothing else running. Or run them on C after integration (see above).
  6. Run `precheck_x96.py` on your pair, and on (lead-1, yours).
  7. Compare every `normalizedSha256` and child trace digest with `lead-precheck.json` and the lead's records under `/Users/sb/code/opensip-ai/opensip-x9-6/target/opensip-x9/x96-lead-{1,2}-{storage,host}`. The `timingGuard` values are not compared.
  8. Confirm that the real `check` refuses only on the clean-commit condition.
- **Judgment calls:** are calls 1 to 9 acceptable?
- **Inventory:** confirm that no successor is needed, because X9-6 adds no file and v134 lists all six.

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `d68bcdf9e0e0203e5b563f298c57834632899d11c3f8332c7af345b94032430e`, the diff's sha256, as a single string;
- "inventoryCandidateAssessment": `{"verdict": "NOT-APPLICABLE", "reason": "no file added; v134 lists all six"}` or your finding.

Do not commit.
