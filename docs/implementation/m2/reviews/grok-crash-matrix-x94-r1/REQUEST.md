Grok review: unit X9-4 r1, the crash matrix's lock and live-revocation rows (law X9 r15 item 12). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT**. The unit adds no file, so there is no inventory candidate: the selected inventory v133 already lists every file it touches.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x94-r1.
- You own the native lane for this review:
  - Use a CARGO_TARGET_DIR under that directory.
  - Use a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
  - Run nothing in parallel with the matrix sets: 39 of X9-4's 47 rows arm the observer tick, and their timing guard measures elapsed time.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Inputs

All inputs are pinned in `hashes.txt`.

### Laws

- **X9 r15:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL-r15.md`, accepted by Codex (`reviews/codex-crash-matrix-x9-r15`), sha256 `0d195ff1…`. `PROPOSAL.md` holds the same text plus the acceptance line.

  The relevant parts:
  - item 12's X9-4 line, with its r3, r12 and r15 notes;
  - **the r15 header, which was written for this unit:**
    - X9-4's census (lawful commit ∪ refused end);
    - the required run's `unit` member;
    - the moved F14 row's R2;
    - the timing guard's end point, and F18's and F19's tick release;
    - F30's second B, its (a) project-state comparison and its (b) refused sweep;
    - F26's "no grant reused";
    - F18's mixed view, which is covered elsewhere;
    - F34's run A;
    - the unit's judgment calls;
  - item 5, with r8's census scope and r15's note;
  - item 7, with r8's trace rule, r12's `timingGuard`, r14's group order and r15's `unit` member;
  - item 8 (the ladder) and C5, with r3's G5 resolution;
  - item 9's rows F06, F14 (r12's moved kill), F18, F19, F26, F30, F34, F38, F39, F40 and F41, with their r12, r13 and r15 notes;
  - item 11, with r12's admission hold, r13's 5,000 ms limit and r15's guard end point;
  - the r12, r13 and r14 headers;
  - the forbidden substitutes.
- **The owning laws the rows transcribe:**
  - X4 r7: the gate states, the observer and the checkpoint, and items 7 and 8's rows;
  - X4T r11: C5's refusal at admission;
  - X3d r8: items 3 to 7, including `publish`'s order, `ExistingAttempt` and `finish`'s REV and CLN;
  - X3b r10: item 5's append and its crash points;
  - X6 r4: item 6's requested binding, and item 7's sweep and its admission;
  - X2 r8: the fence and the leases;
  - X7 r6: F39's and F40's host halves, which are X9-5's.

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-x9-4`, detached at main `9c5f1455a671b87a5717e1a90cb9d0d59e39b247` (X9-5 and F7 integrated). Nothing is committed, and there are no new files.
- **Diff:** `git diff 9c5f145` is 341701 bytes, sha256 `73f8f98afa6d77f93154e653c9046ba6af422a229bbc6a363379a0e7fb9c117b`. It covers 4 files, +572 −21. Most of the bytes are the one-line required-runs fixture.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`.

### Inventory

- **No candidate.** X9-4 adds no file. All four files it changes are rows of `repository-file-inventory.v133.json`, which the lock at `9c5f145` selects:
  - `commit_tests.rs` (test);
  - storage's `required-runs.v1.json` (fixture);
  - `tools/check_crash_matrix.py`;
  - its test.
- **Recommendation:** ACCEPT on the diff, with no inventory successor.

### Lead evidence, in this directory

- **`lead-check-unit.json`:** `check-unit --unit X9-4` over the two lead run sets, with every run's `normalizedSha256`.
- **`lead-release-absence.json`:** the release-absence record every set used. It is byte-identical to X9-5's.
- **`transcribe_x94.py`:** X9-4's transcription script. It appends to the landed `required-runs.v1.json`.
- **`lead-x92-regression-check-unit.json`, `lead-x93-regression-check-unit.json` and `lead-x95-regression-check-unit.json`:** check-unit over two fresh sets each, run on this diff.

## What X9-4 builds

### Storage `tests/commit_tests.rs`

All of the following is test-target code under the existing whole-file support guard.

**The commit driver.**
- **`refused-end=1`:** `open`, then `reserve_end_path` and `refused().finish()`, with nothing staged. This is r15's census part (b). The refusal latches the gate, so `finish` owes and appends one `REV`.
- **`ExistingAttempt`:** it now reports `;execution=<id>;requested=<store>,<namespace>,<carrier>,<op>` after the scored head `not-prepared:ExistingAttempt`. The disclosed binding is run B's input (F34).

**The census (r15).**
- `x94_census` is the union of (a) the lawful first commit and (b) the refused end. Each runs on its own fresh root, and each runs twice and must be equal. The union and digest follow r10's rules.
- The result is 244 points, a kill set of 313, and census trace digest `8a5a5a31b004ba510fdca5f7baf222af7ddd1cd742589ff98f7afc1b7680d00f` (1346 records).
- (b) reaches `x3d.finish.settle.before` and all 29 `x3b.append.rev.*` durability points. Otherwise the census is a harness error.

**`x9_4_matrix`.**
- It runs X9-4's rows, selected by r15's rule (`owned()`): a row with a `unit` member is that unit's alone, and any other row goes by case.
- X9-2's, X9-3's and X9-5's selections are unchanged. Their regressions below show it.

**The step interpreter (X9-3's `interpret`), extended:**
- **Arm substitution.** `@m` in an `arm` is child m's drawn ExecutionId. F34 uses `inject-id:@first`. The script keeps `@m`, so the record's script equals the row.
- **New `spawn` options:**
  - `"distinct": true` (unused by the final rows; F30's second B is R2, see call 2);
  - `"binding": "disclosed:<a>" | "own"`, F34's run B;
  - `"unchanged": true`. The child is captured before and after, giving `<n>.stateUnchanged`, `.projectUnchanged`, `.ledgerUnchanged` and `.sealsAdded`. Both comparisons are recorded as a `<n>-compared` entry of the run's `ladder` list (r15, F30(a)).
- **The foreign holder.** `sqlite-hold` / `sqlite-release` (`carrier` | `ledger`) is the parent's own raw `BEGIN IMMEDIATE`, F06's foreign holder, labelled `mutation`.
- **The ladder step** takes `"r2": "distinct"` and `"observe": "R2.projectUnchanged"` (F26). It now appends to the run's ladder; X9-3's rows have one ladder step and no comparisons, so their records are unchanged.
- **`competitor-writer`** is scored as a commit child.
- **Values read from a commit child's own trace:**
  - `.gate`: the gate's state changes, from 0;
  - `.evidenceCommits`;
  - `.releaseOrder`: `seal.L4,seal.L3,rev,cln`;
  - `.rev`, `.cln` and `.settlement`, from its end disclosure.
- **Post-state values:** `seals`, `receipts` and `orphansPresent`.
- **The timing guard (r15):** from reading the tick-armed child's first `x4.observer.tick` hold to reading its first hold at any other point. X9-3's F44 and F45 measure as before (see the regression).
- **Mutations:** `trust-state-unreadable` (`state.v1` mode `000`, its mode kept under scratch) and `trust-state-restored`.

### `tools/check_crash_matrix.py` and its test (r15)

- **`check_required`** admits an optional `unit` member that names a unit of item 12, and refuses any other value.
- **`in_unit`.** A row with `unit` is in that unit's subset only. Any other row is in each unit whose case list names it. `check-unit` and `check` both select through it, and `check` still requires every row's run.
- **The new test,** `test_a_row_with_a_unit_member_is_in_that_units_subset_only`, shows:
  - the moved row is in X9-4's subset;
  - it is an extra run for X9-3;
  - `check` needs it;
  - invalid units refuse.

  The checker has 18 tests, all passing.

### Storage `tests/fixtures/crash-matrix/required-runs.v1.json`

- **Contents.** X9-2's 231 and X9-3's 57 rows are byte for byte unchanged. X9-4's 47 rows are appended. The file is 169678 bytes, sha256 `b12efe670c6c58c289ad7337cd83a35795a2dc64415fdb4dba1d6552e8220859`.
- **Subsets.** By `in_unit`: X9-2 231, X9-3 57, X9-4 47.

## The rows (47)

C5 (r3, G5): R2 is refused at admission (`operation:*`, the row not scored), R3 is `refused`, and R4 is TNC.

| Case | Runs | What runs | Expected (X9 r15 item 9 and the owning law) |
|---|---|---|---|
| F06 | 2 | Writer held at `x3c.attempt.commit.after#1`. The parent takes `BEGIN IMMEDIATE` on the carrier, or on the ledger. Resume, writer ends, holder released | `Refused(Busy)`, no SEAL, orphans present; R1 UAO, R2 Committed, R3 refused, R4 TNC |
| F14 | 1 | `"unit": "X9-4"` (r12 and r15): F39's script, then a kill at `x3d.finish.settle.before#1`; R2 commits the distinct variant | R1 CH pending, R2 refused at admission (r15), R3 committed, R4 CH settled |
| F18 | 2 | Tick armed; hold at `x4.checkpoint.before-observation#1`; revoke, or `state.v1` at mode `000`; resume main; after `x3d.finish.settle.before#1` resume the tick (r15). The unreadable variant restores the mode before the ladder | `RevokedDuringOperation{trust-revoked}` or `ObserverFailStop{unreadable}`; REV, no CLN, settlement None, no SEAL. R1 UAO; R2 refused at admission, or Committed after the restore; R3 refused; R4 TNC |
| F19 | 31 | As F18 at checkpoint `#2`, 2 rows; plus a kill at each of the 29 `x3b.append.rev.*` points after the revocation | Base: the row as F18, with one SEAL, no receipt, `cln true`, `releaseOrder seal.L4,seal.L3,rev,cln`; R2 refused at admission, or unscored (fail-stop). Kills: R1 UAO, R2 refused at admission, R3 refused, R4 TNC |
| F26 | 1 | Commit, then the `revoke` child; ladder with R2 observed | R1 CH; R2 refused at admission and `R2.projectUnchanged` (r15) |
| F30 | 2 | (a) A held at `x3c.attempt.commit.after#1`; (b) at `x2.lease.writer/lock.after#1`. B competes (`unchanged`); C sweeps; A resumes; ladder R2 (distinct) | B `operation:Busy` with (a) project state, (b) full state unchanged; C (a) writes nothing, `busy`; (b) `admission:Busy`, nothing (r15); A Committed; R2 Committed |
| F34 | 1 | `first` commits; A with `x3d.session.execution-draw#1=inject-id:@first`; B with A's disclosed binding, and with the attempt's own binding | A `not-prepared:ExistingAttempt`, subject `first`, ledger unchanged, no SEAL added (r15); B: `binding-unusable:operation` and CH pending, each with `normalizedSha256` unchanged |
| F38 | 1 | Tick script, hold at `x3d.publish.after-staging#1`; revoke; one tick, latch; resume | Revoked, gate `0,2`, REV and CLN, settlement None, no receipt; R1 UAO, R2 refused at admission, R3 refused, R4 TNC |
| F39 | 1 | r12's script (hold `x3c.evidence.commit.before#1`) | `Committed(latched=true)`, gate `0,1,3`; R1 CH; R2 refused at admission |
| F40 | 3 | F12's two scripts under case F40; the latch variant, landed only (r13) | `CommitUndetermined`, nothing appended (the undetermined end); latch: gate `0,1,3`; R1 CH pending or UAO, R3 committed or refused, R4 CH or TNC |
| F41 | 2 | Latch before admission (hold at `x4.checkpoint.before-observation#3`), and admission before latch (F39's script) | At most one evidence `COMMIT`; gate monotone within 0..3 |

**How the rows were transcribed.**
- **The command:**

  ```
  transcribe_x94.py <the landed required-runs.v1.json at 9c5f145> <X9-4's census.json> <out>
  ```

- **When.** It ran on the census-only run (`x94-census`) before any row ran, and again after development run 2, for call 2.
- **Kill and hold points** come only from the census. Expected values come from the law only.
- **Reproducibility.** Rerunning it on either lead set's census (`matrix.json`'s `census`) reproduces the fixture byte for byte. The census-only run's `census.json` equals both lead sets' censuses.

## Lead results

All checks ran on `9c5f145` with this diff, a private 0700 TMPDIR, and nothing else running.

| Check | Result |
|---|---|
| Full workspace without the feature, run 1 | 1744 passed, 0 failed, 3 ignored |
| Full workspace without the feature, run 2 | 1744 passed, 0 failed, 3 ignored |
| Feature lane: `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets` | 1621 passed, 0 failed, 3 ignored |
| Clippy `-D warnings`: workspace (no feature); the four crates with `crash-matrix`; security, storage and host with `scenario-fixtures` | Clean |
| `cargo fmt --all --check` | Clean |
| `check_package_edges.py --lane host` against v133 | Passed |
| Checker unit tests | 18 OK |

### Development runs

- **`x94-dev1`:** 45 of 47 PASS.
  - F38 and F41's latch-first order failed on `writer.gate`: `0,2,2,2` against `0,2`.
  - `x4.gate.latch.after` follows every fetch-OR. A refused attempt latches again, idempotently: the checkpoint's stop, the session's refusal and the observer. So the harness lists state changes only (call 1).
- **`x94-dev2`:** 47 of 47 PASS.
  - F30's two `normalizedSha256` values differed from dev1's. Every other run, and every trace, agreed.
  - **The cause.** F30's post state was captured after the second B. It then held two Runs, the candidate and the distinct variant, whose `blobDigests` share most digests and interleave 12 new ones at drawn positions. This is r14's cause 1, in the post state.
  - **The fix.** It was corrected in the transcription (call 2).
- **`x94-dev3`** (47 of 47 PASS) **and `x94-dev4-f30`** (F30 only): they agree run by run with dev2, and F30 with each other.

### The X9-4 lead sets

- **How they ran:** `OPENSIP_X9_RUN_SET=x94-lead-1`, then `x94-lead-2`, one after the other, each with `OPENSIP_X9_RELEASE_ABSENCE=<lead-release-absence.json>`:

  ```
  cargo test --locked --offline -p opensip-storage --features crash-matrix --test commit_tests x9_4_matrix -- --exact --test-threads=1
  ```

- **Runs:** 47 of 47 PASS in each set, with 0 FAIL and 0 HARNESS-ERROR. Each set took 261 s.
- **Timing guard:** 39 runs per set arm the tick. They measured 2,593 to 2,844 ms (set 1) and 2,583 to 2,847 ms (set 2), all under 5,000.
- **check-unit:**

  ```
  check_crash_matrix.py check-unit --repository . --unit X9-4 \
    --run-set target/opensip-x9/x94-lead-1 --repeat target/opensip-x9/x94-lead-2 \
    --required crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json \
    --commit 9c5f1455a671b87a5717e1a90cb9d0d59e39b247
  ```

  It passed: 47 runs, census 244 points, kill set 313, 30 killed points (29 `REV` points and `x3d.finish.settle.before#1`), limits L1 to L11, repetitions agree, `matrixPass: false`.
- **Normalized digests:** the 47 `normalizedSha256` values (18 distinct) are in `lead-check-unit.json`. The SHA-256 of their canonical map (sorted keys, no spaces) is `df056f01072db1daf9a164bbd01834efde0cdb6ff434078ac4bec6428862c286`.
- **matrix.json:** set 1 is `1f9d5bcc…`, set 2 is `d71cfa9d…`, 43868 bytes each. Both carry census trace digest `8a5a5a31…`.

### The X9-2, X9-3 and X9-5 regressions

This diff changes the matrix target's shared harness (row selection, ladder append) and the checker. Six sets ran fresh on it, one after the other.

| Unit | Sets | Runs | check-unit | Normalized map | Against the accepted map |
|---|---|---|---|---|---|
| X9-2 | `x94-x92reg-1/2` (998 s each) | 231 of 231 PASS each | passed: census 212, kill set 281, 219 killed, repetitions agree | `4e5cba34…` | equal key for key |
| X9-3 | `x94-x93reg-1/2` (338 s, 342 s) | 57 of 57 PASS each | passed: census 227, kill set 289, 11 killed, repetitions agree | `b0f0a5a8…` | equal key for key; F44/F45 guards 2,788 to 2,843 ms |
| X9-5 | `x94-x95reg-1/2` (704 s, 708 s), host target | 94 of 94 PASS each | passed: census 218, kill set 271, 77 killed, repetitions agree | `5446751d…` | equal key for key; F39/F40 guards 940 to 1,082 ms |

### Release absence

- `opensip-cli` was built in release with no features: 6315264 bytes, `b32604fe8c83343a93e7e38f023abc330afda2fa0f7cb255c842ab2b52aa5e49`, the same bytes as X9-2's, X9-3's and X9-5's.
- The scan found no `OPENSIP_X9_` string and no registered scope name.
- `cargo build --release -p opensip-storage --features crash-matrix` and `-p opensip-host --features crash-matrix` each exited 101 at the compile guard.
- The record is byte-identical to X9-5's (`538a10c4…`).

### Real home

`~/Library/Application Support/OpenSIP` was absent throughout.

## Judgment calls

**Made in development, after a run:**

1. **The gate value lists state changes only.**
   - **What dev1 showed.** It found `x4.gate.latch.after` three times in F38's writer: the observer's latch, then the checkpoint's stop and the session's refusal, each an idempotent fetch-OR.
   - **The change.** `.gate` now records only changes of state.
   - **What it doesn't change.** No expected value changes, F38's `0,2` and F39's `0,1,3` included. The trace digests are unaffected, because the value is read from the trace, not written into it.
2. **F30's second B is the ladder's R2.**
   - **What dev2 showed.** A capture after the second B held two Runs, the candidate and r12's distinct variant. Their shared and new blob digests interleave at drawn positions in `blobDigests`, so `normalizedSha256` disagreed between dev1 and dev2.
   - **The basis.** The second B is item 8's R2, "a next writer that runs a full lawful commit on the same namespace". As R2 (`{"ladder": "R2", "of": "writer", "r2": "distinct"}`), the post state is captured before it, at the ladder (item 7), as in every other row.
   - **Unchanged.** r15's expectation, that it commits the distinct variant and is Committed, is scored as `R2.outcome`.
   - **When.** Re-transcribed before any lead run. There is precedent: X9-5's F32 correction, X9-3's cause 3 and X9-2's call 7.
   - **Rejected:** a normalizer rule for digest lists. It would change shared security support code for one row.

**Recorded in r15 as the unit's calls:**

3. **Hold points where a row names none:**
   - F06 at `x3c.attempt.commit.after#1`, with the foreign holder released after the writer exits. In the carrier variant the writer's own `REV` append is then busy: settlement `Busy`, unscored, and lawful under X3d item 7's "a failure inside the settlement ends it";
   - F30 (a) at `x3c.attempt.commit.after#1` and (b) at `x2.lease.writer/lock.after#1`;
   - F41's latch-first order at `x4.checkpoint.before-observation#3`, outside the shared monitor.
4. **F40's no-latch variants** run under case F40, with F12's scripts and expectations.
5. **Unscored values.** F26's, F39's and F41's R3 and R4 run and are recorded, but are unscored. So are F19's fail-stop R2 and F41's writer outcome.
6. **F06's "an earlier level-3 transaction is released"** has no barrier point and is not scored.
7. **F30's held writer under the unarmed observer's 5 s period** (r3's disclosed gap). F30 agreed across dev2 to dev4 and both lead sets, so no observer tick appeared in the hold.

**Made in this unit's harness:**

8. **The `unit` member** is read by the harness's row selection (`owned()`) and by the checker (`in_unit`), as r15 requires.
9. **The ladder step now appends,** and an `unchanged` child's two comparisons are a `<n>-compared` ladder entry. That is r15's "recorded, not scored" for F30(a), inside the existing `ladder` member. It adds no evidence member.
10. **F18's and F19's tick release** waits on the writer's `x3d.finish.settle.before#1` `pass` (r15). F19's kill rows never resume the tick.

## Decide

- **Scope:** does X9-4 implement X9 r15's X9-4 scope faithfully, and nothing of X9-5 or X9-6? That scope covers:
  - the census;
  - the 47 rows as transcribed;
  - r15's `unit` member, in the checker and the harness;
  - the timing guard's end point.
- **Constraints:** are item 6's constraints kept?
  - test-only, crash-matrix only;
  - no new cfg site;
  - no product code;
  - no authority type;
  - one entry per process.
- **Transcription:** is it lawful? It must use the census and the law only, and call 2's re-transcription must precede any lead run.
- **Rerun and compare:**
  1. Run the census (`OPENSIP_X9_CENSUS_ONLY=1` with `x9_4_matrix`), then rerun `transcribe_x94.py` on `git show 9c5f145:crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json` and that `census.json`. It must reproduce the fixture.
  2. Make your own release-absence record (build, scan, and both refused feature builds).
  3. Run `x9_4_matrix` twice yourself, under `OPENSIP_X9_RUN_SET` names of your choice, one after the other, with nothing else running.
  4. Run `check-unit --unit X9-4` on your pair.
  5. Compare your `normalizedSha256` per run, and every child's trace digest, with `lead-check-unit.json` and the lead's run records under `/Users/sb/code/opensip-ai/opensip-x9-4/target/opensip-x9/x94-lead-{1,2}`. The `timingGuard` values are not compared.
  6. Optionally, run one X9-3 storage set and compare its map with `b0f0a5a8…`.
- **Judgment calls:** are calls 1 to 10 acceptable?
- **Inventory:** confirm that no successor is needed, because X9-4 adds no file and v133 lists all four.

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `73f8f98afa6d77f93154e653c9046ba6af422a229bbc6a363379a0e7fb9c117b`, the diff's sha256, as a single string;
- "inventoryCandidateAssessment": `{"verdict": "NOT-APPLICABLE", "reason": "no file added; v133 lists all four"}` or your finding.

Do not commit.
