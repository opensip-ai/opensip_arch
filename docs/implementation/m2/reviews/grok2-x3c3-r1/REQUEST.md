GROK2 review: unit **X3c-3 r1**, the storage re-commit. It implements law **X3c r8** (accepted by you, GROK2, on 2026-10-04, `reviews/grok2-ledger-blob-x3c-r8/`, no findings) items 6, 6a, 9 to 12b and 13, and transcribes and runs **X9 r17 §RC** (accepted by Grok on 2026-10-04, `reviews/grok-crash-matrix-x9-r17-rc/`, no findings), the re-commit section of the crash matrix. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT** on the diff. This is a product code unit. It adds no file, so it has no inventory successor and no design selection (judgment call 1).

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok2-x3c3-r1`. If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git read-only, and only against the worktree named below.
- **Lanes are serialized** through the lock directory `"$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"`: take it with `mkdir` before any build, test, clippy or matrix run and `rmdir` it straight after; if it is held, wait. **A crash-matrix run set needs the machine quiet** (the 5,000 ms timing guard): hold the lock for the whole set, run it unniced, and check `ps` for any other `cargo`, `rustc` or test binary first.
- Run ordinary commands at `nice -n 10`, with a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Law

All under arch `docs/implementation/m2/`, accepted. Pins are in `hashes.txt`. Review against the snapshots; each live `PROPOSAL.md` adds only its acceptance note (X3c's live file has since moved to the r9 draft, J-RW's text, which is **not** this unit's scope).
- **`ledger-blob-x3c/PROPOSAL-r8.md`** (X3c r8, 66778 bytes, sha256 `ba638efb…`, equal to your `subjectSha256` in `reviews/grok2-ledger-blob-x3c-r8/review.json`). The parts this unit implements:
  - **Item 6 (r8 bullets) and item 6a**: re-commit of a Run already committed in (S, N). 6a.1 identity (R8-1); 6a.2 standing from R's committed per-Run rows only, inside the level-3 transaction, before any insert, with a one-sided Run `LEDGER.CORRUPT` (R8-2); 6a.3 byte-identical material against the least-ExecutionId row, lengths first (R8-3); 6a.4 and 6a.5 availability and pins written once, by the first commit, and a declared pin on a re-commit refused (R8-4, R8-5); 6a.6 to 6a.8 what each commit writes; 6a.9 no DDL, crash point, type or outcome change (R8-6).
  - **Item 9 (r8)**: the standing read charged as fixed statement costs, the comparison reading at most the attempt's own lengths, both inside staging's reservation before the first insert, and a re-commit not charged for the availability and pin statements it does not run.
  - **Item 10 (r8)**: the three refusal conditions on existing rows. **Item 11 (r8)**: the standing read is not a read-back. **Item 12 (r8)** and **item 12b**: coverage and X3c-3's tests.
  - **Item 13**: the X3c-3 unit (its files, tests, matrix work, lead set and integration order with J4). **Item 14**: the crash windows W-R0 to W-R5, rows RC-1 to RC-9, the census child, and the record of the 19 runs.
  - **Forbidden substitutes (r8)** and **Not claimed (r8)**.
- **`crash-matrix-x9/PROPOSAL-r17-RC.md`** (X9 r17 round 1, 235499 bytes, sha256 `89fc47ff…`, equal to Grok's `subjectSha256` in `reviews/grok-crash-matrix-x9-r17-rc/review.json`). The section frame (LD-17-1: frame rules 1 to 6) and **§RC**: RC.1 to RC.7, with LD-RC-1 to LD-RC-7.
- **`commit-session-x3d/PROPOSAL-r9.md`** (X3d r9, 97231 bytes, sha256 `c727001a…`, accepted by Grok, `reviews/grok2-x3d-r9/`): CL-1's restatement of item 4 step 3.8, availability and pins staged on a Run's first commit in (S, N) only. No X3d rule changes, and no X3d file changes.

## Subject

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-x3c3`, detached at product main `d2c00a96c3136fe45b901bc067b6d0ca51f0c9c1` (SD-7; 97 contract successors, 96 inventory successors, v136 selected). Nothing is committed or staged. No file is added, removed or renamed.
- **Diff:** `git -C /Users/sb/code/opensip-ai/opensip-x3c3 diff d2c00a9` is 491754 bytes, sha256 `bb86dd404622ecd4433356e0b1c0c706740ed630ca371430966c917042fd1802`, 11 files, +1522 −94. A copy is `evidence/x3c3.diff`. Most of its bytes are the one-line `required-runs.v1.json` (the line is replaced whole).
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH`; Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`.
- **Evidence:** `evidence/` in this directory, every file pinned in `hashes.txt`. The scripts are as run and name the lead's scratch paths.

| File | Change |
|---|---|
| `crates/storage/src/ledger_store/project_commit.rs` | `PreparedLedger::stage`: the standing read, the re-commit branch (declared pins, comparison), availability and pins on a first commit only; item 9's split reservation; `classify_staging` maps a one-sided Run to `LEDGER.CORRUPT`; module and method docs |
| `crates/storage/src/ledger_store/recovery_material.rs` | `RunStanding`, `WriteTransaction::run_standing` and `committed_material_identical`, beside `stage_run_material`; the material DDL check factored into `verify_material_definition` (now shared by `stage_run_material`, same check) |
| `crates/storage/src/ledger_store.rs` | `LedgerError::OneSidedRun` |
| `crates/storage/src/commit.rs` | doc comments only (`:13-17`, `:711-715`); the values handed to staging are unchanged |
| `crates/storage/src/ledger_store/project_commit_tests.rs`, `crates/storage/src/commit_tests.rs`, `crates/storage/src/recover_tests.rs` | item 12b's tests (below) |
| `crates/storage/tests/commit_tests.rs` | §RC.7: the `recommit` census part, the new observed values, `"r2": "same"` and its guard, R5's one-RunId rule, the two mutations, the commit child's `run-out` |
| `crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json` | the 22 RC rows appended after the 381 (403 rows) |
| `tools/check_crash_matrix.py`, `tools/tests/test_check_crash_matrix.py` | `UNIT_VALUES` admits `"X3c-3"`, with a test |

## What X3c-3 changes

### Storage (X3c r8 items 6, 6a, 9, 10)

**`PreparedLedger::stage`** (`project_commit.rs:482`). In the open level-3 transaction, after r7's operation and RunId join checks and **before any insert**:
1. **Standing** (6a.2): `run_standing` (`recovery_material.rs:355`) checks the material DDL, reads R's current availability record through r7's own indexed read (`load_current_availability`, which checks its DDL and parses the record), and `EXISTS` a `commit_run_material` row naming R, both under the attempt's store generation digest and N. Neither is `First`; both is `Committed`; exactly one is `LedgerError::OneSidedRun`, which `classify_staging` maps to `ProjectLedgerRefusal::Corrupt` (`LEDGER.CORRUPT`, `:668`). R is the receipt's RunId, which r7 already requires to equal the association's. Nothing else is read: no attempt row, phase, SEAL, object or staging residue.
2. **`First`**: the availability and pin charge (below), then exactly r7's staging.
3. **`Committed`** (a re-commit): a non-empty declared pin set refuses on the invariant row (6a.5); the comparison charge; then `committed_material_identical` (`:384`) selects R's row with the least `execution` (`ORDER BY execution`, BINARY collation, so byte order), compares `length(manifest)` and `length(inventory)` with the attempt's own first, and only on equal lengths reads the two bodies and compares them byte for byte. A difference refuses on the invariant row (6a.3). Then the receipt pair and the Run material are staged as r7 stages them, the published-object check runs, and **availability and pins are not staged** (`:604`, `if standing == RunStanding::First`).
4. The `stage-availability` and `stage-pins` crash barriers stay inside that branch, so a first commit's trace is unchanged and a re-commit's reaches `stage-recovery_pair` and `stage-run_material` only (6a.9). No crash point, scope, DDL, type, outcome, row or code is added.

**Item 9's charges.** r7's single `STAGE_COST` (16 objects, 128 edges, 64 KiB) is split in two halves that sum to it: `STAGE_COST` (8, 64, 32 KiB) for the pair and material statements, and `FIRST_COMMIT_COST` (8, 64, 32 KiB) for the availability and pin statements. The reservation taken before the standing read is `STAGE_COST + STANDING_COST + COMMIT_COST` plus the receipt, association, manifest and inventory bytes. Once the standing is known, still before the first insert, a first commit is charged `FIRST_COMMIT_COST` plus the availability record's and the pins' bytes, and a re-commit `COMPARE_COST` plus its own manifest and inventory lengths (the most the comparison can read). `STANDING_COST` (2, 8, 4 KiB) is "fixed statement costs, as `next_commit_sequence`'s scan" (two indexed reads, the availability body bounded by 4 KiB), and `COMPARE_COST` (2, 8, 64) covers the comparison's two statements. A first commit's total is r7's plus `STANDING_COST` (judgment call 3).

**`commit.rs`** changes only its module and `stage` doc comments. It still builds the initial availability record and the empty pin set; staging uses them on a first commit only (6a.9).

### Tests (X3c r8 item 12b), in the ordinary lanes

Through the facade's own functions with a real session's binding values (X3d-3's `session_values`, over `scenario-fixtures`), on a scratch `I/stores/S` (`commit_tests.rs`):
- **`the_same_candidate_committed_twice_is_committed_both_times`** (`:1087`), end to end through `prepare_commit` and `publish`: two real sessions on one registered root, each with its own candidate. Both `Committed`; the second confirms every object (`ConfirmedExisting`), takes `commitSequence` 2, has its own ExecutionId and the same RunId, and adds exactly one row to `attempt_custody`, `commit_receipts`, `commit_associations` and `commit_run_material` and none to `evidence_availability` (1 row), `active_run_pins` or `pin_change_facts`. The two material rows are byte-identical; the receipt parses with the second ExecutionId and sequence 2. A raw dump of every earlier row (every column through SQL `quote()`) is a subset of the dump after. The carrier holds two SEALs and no `REV` or `CLN`.
- **`standing_is_read_from_committed_per_run_rows_only`** (`:1193`): (a) an attempt staged after its SEAL and dropped before `COMMIT` leaves an `admitted` row and no per-Run row, and the next commit writes availability generation 0 and sequence 1; (b) with the fail-after hook (`land_commit`: the transaction's own `COMMIT` lands inside `with_commit_hook`, so the adapter's `COMMIT` reports `Undetermined` over a landed commit), the next commit is a re-commit: sequence 2, still one availability row, two material rows, earlier rows kept.
- **`a_regeneration_mismatch_is_refused_on_the_invariant_row`** (`:1238`): R's stored inventory changed through the crate's lifted-trigger hook (`lifted`, which drops the table's triggers, writes, reinstalls them from their own stored SQL and asserts they are byte-identical), once at the same length (a digest's last digit) and once longer by one byte. Each re-commit refuses `StagingMismatch` (the invariant row), the only added row is the refused attempt's own `admitted` row, and level 3 is free.
- **`a_one_sided_run_is_ledger_corrupt`** (`:1292`): R's material deleted (availability without material) and R's availability deleted (material without availability), each through `lifted`. Each re-commit is `ProjectLedgerRow::LedgerCorrupt`, `T::LedgerCorrupt`; nothing inserted; level 3 free.
- **`a_non_retained_record_stays_current_through_a_re_commit`** (`:1318`): a generation-1 `purged` successor written (parsed by `AvailabilityRecord::parse` first); the re-commit commits at sequence 2, the availability table is byte-identical, and the current record is still the `purged` one.
- **`a_commit_of_the_run_in_another_namespace_is_a_first_commit_there`** (`:1372`): the same Run committed in N, then in N2 of the same store: sequence 1 and availability generation 0 in N2, and N's ledger dump unchanged.
- **`every_execution_of_a_run_committed_three_times_recovers_committed`** (`recover_tests.rs:576`): three commits of one Run; `recover_from` of each ExecutionId is `CommittedHistorically` with R, pending settlement, and the carrier is asked exactly that attempt's own journal sequence.

At staging level (`project_commit_tests.rs`, X3c-2's fixture, whose first commits declare one pin):
- **`a_re_commit_stages_its_own_rows_and_no_availability_or_pins`** (`:936`): every object confirmed; staged rows invisible before `COMMIT`; afterwards 2 attempt rows, receipts, associations and material rows, still 1 availability row and the first commit's 1 active pin and 1 pin fact; earlier rows byte-identical; material identical; sequences `1,2`; the re-commit's own pair joins `ContinueCarrier { pending_settlement: true }`; E1's row stays `admitted`.
- **`a_re_commit_that_declares_a_pin_is_refused_before_any_insert`** (`:1032`): the declared pin refuses on the invariant row (through this crate-private construction of the staged rows; the facade declares none); only the attempt row is new; level 3 is free; the same attempt with no declared pin then commits.
- **`staging_one_unit_short_of_its_reservation_refuses_before_any_insert`** (`:1160`): on a first commit and on a re-commit, what staging uses equals `staging_cost` computed from the constants and bodies (and the two differ); one unit short in objects, in edges or in bytes refuses on the budget row with nothing inserted; the exact reservation commits.

**The first commit is unchanged:** r7's and X3d-2's staging tests stand unmodified in the lanes, and the census below shows the first commit's trace unchanged.

### The matrix (X9 r17 §RC.7), `crates/storage/tests/commit_tests.rs`

1. **Rows:** the 22 rows of RC.4 appended after the 381 (below).
2. **The `recommit` census part** (`recommit_part`, appended to `x96_parts`): its own fresh root and fixture child, an unarmed E1 commit (not part of the census), then an unarmed E2 commit of the same candidate in a fresh process, whose trace is the part. It is a harness error unless both are `Committed(latched=false)`, E2 reaches `x3c.object/reopen-confirm.after` and no `x3c.object/link.after`, and E2 reaches `stage-recovery_pair` and `stage-run_material` and neither `stage-availability` nor `stage-pins`. The part runs twice inside `union_census` (equal point for point), its lines are prefixed `recommit|`, and the trace digest hashes the five parts in order. Host's census is unchanged.
3. **Observed values,** each scored only where a row's `expected` names it (`verdict` is unchanged), none a run-record member:
   - `post_values`: `availabilityRows`, `materialRows`, `materialIdentical`, `commitSequences`, `pinRows`, and `revs` (`carrier_records`, counted as `seal_runs` finds SEALs: a `grant_journal_v3` row with a column equal to `REV`);
   - `trace_values`, for every commit child finished or killed: `<n>.objectsLinked` and `<n>.stages`;
   - kept-state values (`kept_values`) for a child spawned `unchanged`, now also when it is killed: `<n>.ledgerRowsKept` (every ledger row before is in the after dump, as a multiset per table) and `<n>.objectsKept` (every `objects/sha256/<64 hex>` raw entry keeps its path and SHA-256; staging names never match);
   - `ladder_steps`: `R2.objectsLinked` (from R2's exit, counted by `trace_values`), and from the capture R2 already takes for `R2.receipts`, `R2.commitSequence` (R2's own association) and `R2.availabilityRows`.
4. **R5's one-RunId check:** `runs.len() >= 2 && every SEAL names runs[0]`. F36's runs hold exactly two, so their value is unchanged.
5. **`"r2": "same"`:** `r2_distinct` reads `same` (or no directive) as the candidate and `distinct` as before; any other value is a `HARNESS-ERROR`, in both script forms.
6. **Two mutations** in `apply_x93`: `delete-availability` (exactly one `evidence_availability` row is required, else a harness error; then deleted through `lifted`); `plant-availability` (with the triggers in place, one generation-0 row for R: a copy of the `of` child's own generation-0 `retained` row, found through the `of` child's material row, with its RunId replaced by R in the column and the body). **R** is written by the `of` child to `run-<name>` under the run's scratch root (`run-out`, passed to every step-form commit child beside `closure-out`): the RunId of the candidate built from the child's own session, the distinct variant's child building the candidate for it. It is outside the installation and the trace, and never scored. `apply` and `apply_x93` take the `of` child's name.
7. **The checker:** `UNIT_VALUES = (*UNIT_CASES, 'X9-6', 'X3c-3')`, read as r16 reads X9-6; `check-unit --unit X3c-3` is refused by argparse. New test `test_an_x3c_3_row_is_in_no_units_subset_and_check_needs_it`.

Nothing else: no crash point, scope, kind, label, run-record member or limit.

## The X9 work (§RC.6), in order

### 1. The census-only step, before transcription

Both targets' `x9_6_matrix` with `OPENSIP_X9_CENSUS_ONLY=1` (run sets `x3c3-census-storage` and `x3c3-census-host`), compared with C's accepted censuses by `evidence/scripts/census_compare.py` (`evidence/census/census-compare.json`), then the checker's `coverage` (`coverage-before.json`).

| Figure | §RC.3 predicts | Observed |
|---|---|---|
| Storage census points | 259 → 261 | 259 → **261** |
| Storage kill set | 321 → 327 | 321 → **327** |
| Union census points | 321 → 323 | 321 → **323** |
| Union kill set | 383 → 389 | 383 → **389** |
| Points added | `x3c.object/reopen-confirm.before`, `.after` (82 each) | exactly those two, 82 each |
| Occurrence changes | `x3c.object/file-barrier.before`, `.after`: 82 → 164; `link.after` stays 82 | exactly those two, 82 → 164; `link.after` 82 |
| Kill-set points added | 8: the six `reopen-confirm` points and `file-barrier.{before,after}#164` | exactly those 8 |
| Kill-set points removed | 2: `file-barrier.{before,after}#41` | exactly those 2 |
| Host census | unchanged | equal to C's, 218 points |

- The storage parts are, in order, `commit`, `recover`, `sweep`, `refused-end`, `recommit`. The first four parts' traces equal C's `census-trace.txt` point for point and event for event, so **a first commit's trace is unchanged** (6a.9; item 12b's last test). The storage census trace is 2617 records, `4de56491…` (C's 1379, `e9add21e…`, plus the part).
- **Coverage before transcription:** union kill set 389, 383 killed; `uncovered` is exactly RC-2's eight points; `killedOutsideKillSet` is exactly F03's two `#41` points (LD-RC-6).
- **Nothing contradicted RC.3, so transcription went ahead.**

### 2. Transcription (RC.4)

`evidence/scripts/transcribe_x3c3.py` builds the 22 rows from §RC's templates and tables only (the values are typed into the script from RC.2 and RC.4; nothing is read from a run or from the census beyond the stop check above), appends them to `git show d2c00a9:` of storage's file, and asserts that the 381 landed rows' bytes are unchanged inside the new file and that no identity repeats. The file is canonical JSON, 403 rows, 209604 bytes, sha256 `292f8105…`. Host's file is unchanged.
- **Coverage after transcription** (`coverage-after.json`): 389 of 389 kill-set points killed, `uncovered: []`, and `killedOutsideKillSet` exactly `x3c.object/file-barrier.after#41` and `.before#41`.
- `check_required` admits the file (403 rows, 22 with `"unit": "X3c-3"`).

### 3. Development runs

`x3c3-dev1-storage` (`OPENSIP_X9_ROWS`: the 22 RC rows and the 19 runs of RC.5; F40's `-latched` variant matched a prefix too): **42 of 42 PASS**.
- Every RC row's observed values meet its expected values (`evidence/dev1/rc-rows-dev1.json`, one entry per row with every expected key's observed value).
- **The 19 runs of RC.5** (`dev1-compare.json`, against C's lead-1 records): 18 of them now end `Committed(latched=false)` at the changed child (R2, or F49's `second`), with `end(rev=false, cln=false, …, step=true)`; F33 `run-material-inventory` stays `Refused(Invariant)`, `end(rev=true, cln=true, …)`. All 19 PASS with no expected value re-transcribed. R3's `nextWriter` became `next-writer=committed` in exactly rows 1, 2, 3 and 13 (F12 and F40 `fail-after-evidence-commit`, F23 `delete-receipt` and `delete-association`). R2's association took sequence 1 after F23 `delete-association` and F52 `receipt-only`, and 2 elsewhere, as RC.5 says (unscored). r16's release-order verdict ran on the 18 committed children and found no miss.

### 4. Release absence

`evidence/scripts/release.sh` (`evidence/release/`): `opensip-cli` in release with no features, 6316560 bytes, sha256 `cf5deb6e…`; the scan found no `OPENSIP_X9_` string and none of the scope names; `cargo build --release` of storage and of host with `crash-matrix` each exited 101 at the compile guard. (The binary differs from X9-6's `b32604fe…` because main moved since C; this one record is what both X3c-3 lead sets carry.)

### 5. The lead sets (§RC.6)

Two repetitions of both targets on `d2c00a9` + this diff, each under one hold of the lanes lock, unniced, after `ps` showed no other `cargo`, `rustc` or test binary, with `OPENSIP_X9_RELEASE_ABSENCE` set:

```
OPENSIP_X9_RUN_SET=x3c3-lead-<n>-storage cargo test --locked --offline -p opensip-storage --features crash-matrix --test commit_tests x9_6_matrix -- --exact --test-threads=1
OPENSIP_X9_RUN_SET=x3c3-lead-<n>-host    cargo test --locked --offline -p opensip-host    --features crash-matrix --test commit_matrix_tests x9_6_matrix -- --exact --test-threads=1
```

| Set | Target | Runs | Time | Timing guard (tick-armed runs) | `matrix.json` |
|---|---|---|---|---|---|
| `x3c3-lead-1` | storage | 403 of 403 PASS | 2131 s | 43 runs, 2583–2828 ms | `6cb80e0b…` |
| `x3c3-lead-1` | host | 98 of 98 PASS | 747 s | 2 runs, 1078–1091 ms | `9658e431…` |
| `x3c3-lead-2` | storage | 403 of 403 PASS | 2135 s | 43 runs, 2573–2869 ms | `860c0b38…` |
| `x3c3-lead-2` | host | 98 of 98 PASS | 738 s | 2 runs, 1068–1075 ms | `8c59b392…` |

That is 501 runs per repetition. The run records are under `/Users/sb/code/opensip-ai/opensip-x3c3/target/opensip-x9/x3c3-lead-{1,2}-{storage,host}/`; the four `matrix.json` files are in `evidence/x9/`.

**Lead set 1's host half ran separately** (process record; `evidence/x9/waits.txt`). Its first attempt held the lock but never started: its load check matched the command-line text of another reviewer's script that was itself waiting for the lock, and the two waited on each other. By the lead's decision it was stopped (no run in progress; the lock it had taken at 23:19:54Z was released at 00:17:58Z), its load check was changed to match process names only (`ps -Ao comm=`, as X4-F3's `leadset.sh` does), and the host half alone was rerun under its own lock hold at 01:28:44Z (after a 30 s load wait). The storage half's result stands. `lead.v1-aborted.sh` is the script as first run; `lead.sh` is the fixed one, which lead set 2 also used.

**The pre-integration check** (`evidence/scripts/precheck_x3c3.py` → `evidence/x9/lead-precheck.json`; judgment call 15). Over the pair (lead-1, lead-2): passed; 501 runs; storage census 261 points, kill set 327, 313 points killed; host census 218, kill set 271, 81 killed; **union 323 points, kill set 389, all 389 killed in each repetition**; `killedOutsideKillSet` exactly the two F03 `#41` points (LD-RC-6), and nothing else; L1 to L11; the repetitions agree on both censuses, every `normalizedSha256` and every child trace digest. Normalized maps (sha256 of the canonical map): storage `90ba2116…` (95 distinct values), host `ede9384c…` (18), the latter equal to X9-6's.

**The real `check`** over the same pair refuses with `storage: matrix product is not the reviewed clean commit` (`lead-check-refusal.txt`), as it must for an uncommitted unit (X9 item 7; forbidden substitute "a matrix pass on a dirty worktree"). See "The gate and the clean commit".

**Against C** (`evidence/scripts/compare_c.py` → `lead1-compare.json`, `lead2-compare.json`; C's lead-1 records under `crash-matrix-x9/evidence/3d2d5b5…/`). In each repetition:
- **host:** 98 of 98 runs equal to C's: `normalizedSha256`, every child's trace digest and the ladder;
- **storage:** 362 of the 381 landed runs equal to C's in the same way. The other 19 are exactly RC.5's 19 runs, and they differ only as RC.5 records: the changed child's trace (`commit#3`) in all 19, the R3 sweep's trace and its `nextWriter` in rows 1, 2, 3 and 13, the R2 ladder entry's outcome in the 17 X9-2-form rows, and `normalizedSha256` in F49 `reader-skewed-by-append` only. No expected value changes (none names those children). Observation O-1 below covers F33 `run-material-inventory`.

### 6. The RC rows: transcription and results

Every row has `"units": ["X3c"]` and `"unit": "X3c-3"`; its expected values are RC.4's for its row, key for key (counted here). "Repetitions agree" is `normalizedSha256` and every child trace digest equal between lead-1 and lead-2. Every killed point is in the r17 kill set (RC-2's eight are the points the `recommit` part adds; RC-3's and RC-5's are the `#1` points F11, F13, F14 and F15 already kill).

| §RC row | File row | Case and variant | Transcription (RC.4) | Labels | Expected keys | Dev run | Lead 1 | Lead 2 | Repetitions agree |
|---|---|---|---|---|---|---|---|---|---|
| RC-1 | 382 | `F15-recommit-lawful` | T-L | plain | 19 | PASS | PASS | PASS | yes |
| RC-2 | 383 | `F04-recommit-kill-x3c-object-reopen-confirm-before-1` | T-K, P `x3c.object/reopen-confirm.before#1`, L `R1,R2,R3,R4`, + recover(E1) | death | 11 | PASS | PASS | PASS | yes |
| RC-2 | 384 | `F04-recommit-kill-x3c-object-reopen-confirm-before-41` | T-K, P `x3c.object/reopen-confirm.before#41`, L `R1,R2,R3,R4`, + recover(E1) | death | 11 | PASS | PASS | PASS | yes |
| RC-2 | 385 | `F04-recommit-kill-x3c-object-reopen-confirm-before-82` | T-K, P `x3c.object/reopen-confirm.before#82`, L `R1,R2,R3,R4`, + recover(E1) | death | 11 | PASS | PASS | PASS | yes |
| RC-2 | 386 | `F04-recommit-kill-x3c-object-reopen-confirm-after-1` | T-K, P `x3c.object/reopen-confirm.after#1`, L `R1,R2,R3,R4`, + recover(E1) | death | 11 | PASS | PASS | PASS | yes |
| RC-2 | 387 | `F04-recommit-kill-x3c-object-reopen-confirm-after-41` | T-K, P `x3c.object/reopen-confirm.after#41`, L `R1,R2,R3,R4`, + recover(E1) | death | 11 | PASS | PASS | PASS | yes |
| RC-2 | 388 | `F04-recommit-kill-x3c-object-reopen-confirm-after-82` | T-K, P `x3c.object/reopen-confirm.after#82`, L `R1,R2,R3,R4`, + recover(E1) | death | 11 | PASS | PASS | PASS | yes |
| RC-2 | 389 | `F04-recommit-kill-x3c-object-file-barrier-before-164` | T-K, P `x3c.object/file-barrier.before#164`, L `R1,R2,R3,R4`, + recover(E1) | death | 11 | PASS | PASS | PASS | yes |
| RC-2 | 390 | `F04-recommit-kill-x3c-object-file-barrier-after-164` | T-K, P `x3c.object/file-barrier.after#164`, L `R1,R2,R3,R4`, + recover(E1) | death | 11 | PASS | PASS | PASS | yes |
| RC-3 | 391 | `F11-recommit-kill-x3c-evidence-stage-recovery-pair-1` | T-K, P `x3c.evidence.stage-recovery_pair#1`, L `R1,R2,R3,R4,R5`, + recover(E1) | death | 16 | PASS | PASS | PASS | yes |
| RC-3 | 392 | `F11-recommit-kill-x3c-evidence-stage-run-material-1` | T-K, P `x3c.evidence.stage-run_material#1`, L `R1,R2,R3,R4,R5`, + recover(E1) | death | 16 | PASS | PASS | PASS | yes |
| RC-4 | 393 | `F12-recommit-fail-before-evidence-commit` | T-I, P `x3c.evidence.commit.before#1`, A `fail-before` | injected | 13 | PASS | PASS | PASS | yes |
| RC-4 | 394 | `F12-recommit-fail-after-evidence-commit` | T-I, P `x3c.evidence.commit.after#1`, A `fail-after` | injected | 13 | PASS | PASS | PASS | yes |
| RC-5 | 395 | `F13-recommit-kill-x3c-evidence-commit-after-1` | T-K, P `x3c.evidence.commit.after#1`, L `R1,R2,R3,R4` | death | 11 | PASS | PASS | PASS | yes |
| RC-5 | 396 | `F13-recommit-kill-x3d-publish-commit-returned-1` | T-K, P `x3d.publish.commit-returned#1`, L `R1,R2,R3,R4` | death | 11 | PASS | PASS | PASS | yes |
| RC-5 | 397 | `F14-recommit-kill-x3d-publish-published-1` | T-K, P `x3d.publish.published#1`, L `R1,R2,R3,R4` | death | 11 | PASS | PASS | PASS | yes |
| RC-5 | 398 | `F15-recommit-kill-x3d-finish-end-step-after-1` | T-K, P `x3d.finish.end-step.after#1`, L `R1,R2,R3,R4` | death | 11 | PASS | PASS | PASS | yes |
| RC-6 | 399 | `F33-recommit-run-material-inventory` | T-M, M `run-material-inventory`, L `R1,R3,R4` | mutation | 13 | PASS | PASS | PASS | yes |
| RC-7 | 400 | `F23-recommit-one-sided-material-only` | T-M, M `delete-availability`, L `R1,R3,R4` | mutation | 12 | PASS | PASS | PASS | yes |
| RC-7 | 401 | `F23-recommit-one-sided-availability-only` | T-P | mutation | 12 | PASS | PASS | PASS | yes |
| RC-8 | 402 | `F29-recommit-readers-across-publish` | T-R | plain | 6 | PASS | PASS | PASS | yes |
| RC-9 | 403 | `F52-recommit-purged` | T-M, M `availability-purged`, L `R1`, + recover(E1) | mutation | 8 | PASS | PASS | PASS | yes |

### 7. The lanes

Every lane ran on `d2c00a9` + the final diff (`evidence/scripts/lanes.sh`; `evidence/lanes-summary.txt`; counts in `evidence/results.json`), serially, each step under the lanes lock at `nice -n 10`, with a private 0700 TMPDIR and `--locked --offline`. The diff sha256 was the same at the start and end of the lanes and of each lead set. The real home was absent before and after.

| Lane | Result |
|---|---|
| `cargo fmt --all --check` | clean |
| `cargo build --workspace --all-targets` | pass |
| `cargo build` of platform, security, storage and host, `--features crash-matrix --all-targets` | pass |
| `cargo build` of security, storage and host, `--features scenario-fixtures --all-targets` | pass |
| `cargo clippy --workspace --all-targets -- -D warnings` | clean |
| `cargo clippy`, the crash-matrix lane (four packages, `--all-targets`, `-D warnings`) | clean |
| `cargo clippy`, the scenario-fixtures lane (three packages, `--all-targets`, `-D warnings`) | clean |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1748 passed, 0 failed, 3 ignored (20 binaries, 529 s) |
| The same, run 2 | 1748 passed, 0 failed, 3 ignored (519 s) |
| `cargo test --workspace --doc` | 20 passed |
| `cargo test`, platform, security, storage and host, `--features crash-matrix --all-targets --no-fail-fast` | 1646 passed, 0 failed, 3 ignored (527 s) |
| `tools/generate_contracts.py` drift check (rebuild-02 generator, node 24.16.0) | passed, `changed: []`, `generatorClosureSelected: true`, 40 sources, 8 outputs |
| `verify_design.py --architecture ../opensip_arch --implementation .` | pass: v136 selected, 97 contract and 96 inventory successors, 1 contract passage supersession, 40 generation and 48 admission sources |
| `check_package_edges.py --lane host` / `--lane rust-provider` against v136 | pass (12 packages, 22 declared and 20 resolved internal edges) / pass |
| `tools/tests/test_package_edges.py` | 14 run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` / `check_identity_dependencies.py` | pass (11 dependencies) / pass (8) |
| `tools/tests/test_dependency_policy.py` / `test_identity_dependencies.py` | 9 OK / 5 OK |
| `python3.14 -m unittest tools/tests/test_check_crash_matrix.py` | 27 tests OK (26 + the new one) |

Notes:
- The workspace and feature counts include the 10 new Rust tests (3 in `project_commit_tests.rs`, 6 in `commit_tests.rs`, 1 in `recover_tests.rs`). No existing test's assertions changed. Two shared helpers changed shape only: `commit_tests.rs`'s `prepare` takes its location from the binding's namespace (always N for the existing tests) and `Store` gained `*_in` variants for another namespace; `project_commit_tests.rs`'s `material` delegates to `material_of` with the seed it always used.
- **The first drift attempt** (`contracts-drift exit=1`) refused before generating anything: `missing regular input: tools/contracts/node_modules/typescript/LICENSE.txt`. A fresh worktree has none of the generator's ignored, pinned inputs; `tools/contracts/node_modules` and `python-packages` were copied from the main checkout (the generator checks every input against its pinned sha256), and the rerun (`contracts-drift-2`) passed. Both directories are ignored, so the worktree status is unchanged.
- Earlier lines of `lanes-summary.txt` (`check1`, `quick1`, the census runs and `dev1`) are the development record before the lanes.

## Observations

- **O-1. F33 `run-material-inventory`'s R2 takes a shorter path to the same outcome.** It stays `Refused(Invariant)` (RC.5 row 12, RC-6's rule), but the refusal now comes from the comparison before `stage-recovery_pair`, where at C it came from `stage_availability` after `stage-recovery_pair` and `stage-run_material`. So that child's trace digest changes, as it does for the 18 changed children. RC.5 lists trace changes only for the runs whose outcome changes; this one is unscored, both repetitions agree on it, and no expected value names it.
- **O-2. The comparison reads before identity admission.** A re-commit compares the attempt's manifest and inventory bytes before `stage_run_material` parses them. A byte-identical pair is then admitted exactly as on a first commit, and any difference refuses on the invariant row without parsing, which is item 6a.3's order ("before any insert").
- **O-3. Integration order (X3c r8 item 13; §RC.6; frame rule 5).** These sets ran storage's 381 + 22 rows and host's 98. If J4 (J-RW) integrates first, X3c-3's integration set must also run §RW's rows; if X3c-3 integrates first, J4e's set covers §RC's rows. Any lead set after integration runs §RC's rows (frame rule 5), including X4-F3's if it integrates later.

## Judgment calls

1. **No inventory successor.** X3c r8 item 13 lists "An inventory successor" among X3c-3's deliverables, written when the unit's file set was not yet known. The lead directed X3c-3 into existing files, and the laws allow it: §RC.7 names `commit_tests.rs` and storage's `required-runs.v1.json`, and item 13 names `project_commit.rs`, `ledger_store.rs`, `recovery_material.rs` and `commit.rs`; the tests went into the existing test modules (`project_commit_tests.rs`, `commit_tests.rs`, `recover_tests.rs`). The diff adds, removes and renames no file, so v136 (selected at `d2c00a9`) lists every file it touches, and inventory rows carry no bytes. As for X4-F1 and X4-F2, there is no candidate and no `inventoryCandidateAssessment`. Inventory numbers v137 (J2a) and v138 (E2a) are untouched.
2. **R is the receipt's RunId** for the standing read. Staging reads standing before any insert, so before `stage_recovery_pair` joins the pair to the attempt and before `stage_run_material` admits the manifest as R's identity preimage. r7's first check in `stage` already requires the receipt's and the association's RunId to be equal, and the facade builds both from the replay's RunId. A receipt naming another Run is refused later by `parse_material` (`RunIdentity`, the invariant row), whatever its standing.
3. **Item 9's split.** The law asks for three things at once: the standing read charged as fixed statement costs, both reads "inside staging's existing reservation, taken before the first insert", and "a re-commit is not charged for the availability or pin statements it does not run". The branch is known only after the standing read, inside the open transaction. So r7's single reservation became two charges, both before the first insert: the common part (with `STANDING_COST`) up front, and the branch's part (`FIRST_COMMIT_COST` and its bodies, or `COMPARE_COST` and the bodies the comparison may read) once the standing is known. r7's 16/128/64 KiB is split into two equal halves, so a first commit's total is r7's plus `STANDING_COST`. **Rejected:** one up-front reservation for both branches (charges a re-commit for the availability and pin statements); reserving the larger of the two branches and leaving the rest unused (no refund exists in `WorkLedger`, so the same overcharge). The test pins each branch's exact total.
4. **The comparison's row is fetched in two statements.** The lengths query picks R's least-ExecutionId row (`ORDER BY execution LIMIT 1`; `execution` has BINARY collation, so byte order), and only on equal lengths a second statement reads that row's bodies by its key. This is item 9's "lengths are compared first, so a longer stored body is never read". A missing row between the two statements cannot happen inside one `BEGIN IMMEDIATE` transaction; if it did, it would refuse on the invariant row (`run_material_missing`).
5. **`OneSidedRun` is its own `LedgerError` variant,** mapped to `Corrupt` by `classify_staging` (item 13: "`classify_staging` gains the one-sided `LEDGER.CORRUPT` mapping"). Every other match on `LedgerError` has a catch-all, so no other mapping changes.
6. **The declared-pin refusal comes before the comparison** on the re-commit branch. Both are the invariant row and both precede any insert; the cheaper check first.
7. **The fail-after hook in the unit tests** is the existing crate-private `with_commit_hook` running the transaction's own `COMMIT` (`land_commit`), so the adapter's `COMMIT` errors after a landed commit and reports `Undetermined`: X9's `fail-after`, without the `crash-matrix` feature in the ordinary lanes.
8. **`lifted` in the unit tests** is item 12b's "crate-private hook, with its trigger lifted and reinstalled byte-identically": it drops all of the table's triggers, as X9's `lifted` mutation does, and asserts the reinstalled `sqlite_schema` rows are byte-identical.
9. **The end-to-end re-commit test** checks dispositions through `PublishedObject::disposition`'s `Debug` spelling, because `ObjectDisposition` is not re-exported to `commit.rs` and item 13 allows only doc changes there. The staging-level test compares the typed value.
10. **Kept-state values when a child is killed** (§RC.7 item 3) are the two new values only. The existing `<n>.stateUnchanged`, `projectUnchanged`, `ledgerUnchanged`, `sealsAdded` and the `<n>-compared` ladder entry stay on the finish path, so no existing run record gains a ladder entry.
11. **`run-out` goes to every step-form commit child,** as `closure-out` does (§RC.7 item 6: "as r12's commit child writes its core closure"). The file lies under the run's scratch root, outside `capture`'s root (the scratch H) and outside the trace. A non-distinct child writes the candidate it already built; only the distinct variant's child builds the candidate a second time, and no existing step-form row spawns a distinct child. The regression comparison below confirms that every other landed run's records are unchanged.
12. **`plant-availability` finds the `of` child's row through that child's material row** (`commit_run_material.execution` = its drawn ExecutionId, then its `run_id`), so the copied row is exactly "the `of` child's generation-0 `retained` row", and the RunId is replaced in the column and in the body (it occurs once). R is checked for the `run3:` shape and must differ from the child's own RunId.
13. **`R2.objectsLinked` is counted by `trace_values`** on R2's exit, so it is the same count `<n>.objectsLinked` gives a scripted child.
14. **`R2.commitSequence` is inserted only when R2 has an association.** A row naming it for a refused R2 would observe `absent`; no RC row does.
15. **The precheck tolerates exactly one refusal (LD-RC-6).** `precheck_x3c3.py` is X9-6's `precheck_x96.py` (which runs each target's sets through `check_set(unit=True)` to admit the dirty worktree) with one change: `check_set(unit=True)` also refuses a killed point outside the target's kill set, which the real `check` does not (it lists such points). Exactly the storage refusal naming `x3c.object/file-barrier.after#41, x3c.object/file-barrier.before#41` is tolerated and counted; any other refusal stands. It reports the union `killedOutsideKillSet`, which must be those two points.
16. **Rows of the same Run in the step form** use one candidate per run; `"r2": "same"` is spelled in every RC ladder that runs R2 (T-L, T-K, T-I), and left out where the ladder has no R2 (T-M, T-P), exactly as RC.4's templates spell them.

## The gate and the clean commit

- **Why no matrix pass yet.** X9 item 7 and the forbidden substitutes refuse "a matrix pass on a dirty worktree, or on a commit other than the reviewed one", and §RC.6 asks for "two repetitions of both targets on X3c-3's integration commit". This unit is reviewed uncommitted, so its sets record `worktreeClean: false`, and the real `check` refuses them (correctly). `precheck_x3c3.py` applies every other condition of `check` through the checker's own functions and reports `matrixPass: false`. This is X9-6's arrangement (`reviews/grok-crash-matrix-x96-r1/`).
- **What remains after your acceptance:** the lead integrates this diff as main commit C′; on C′, with a clean checkout, the lead runs release absence, two full sets of both targets (serialized, as above) and the real `check`, where `matrixPass: true` is expected because the same bytes produced the agreement above; the lead records the evidence; and the X3c r8 "records owed after acceptance" (EXIT-PLAN's X3c row and follow-up (b), M2-COMPLETE §5 rows 6 and 11, M3-PLAN's carry-in row) are written then.
- **Your choice of when to rerun.** You may run your own two sets now on this worktree, or on C′ after integration, as you chose for X9-6. Say which in your review.

## Not claimed

X3c r8's "Not claimed" stands: availability regeneration or restoration by a re-commit; how a commit that declares pins joins a re-commit's set (no commit declares pins at M3); re-commit across store generations; the resume and repair writer and every L11 crash prefix (J-RW, J4; X3c r9 is in review and is not this unit); deduplicating per-attempt Run material. Also not claimed: X9 r17's §S12 and §RW (reserved), and the post-integration matrix pass (above).

## Lead notes (Claude Opus 5.5, before sending)

- **No inventory successor:** confirmed, following X4-F2's precedent. Every file is already in v136, so item 13's "an inventory successor" isn't needed when no file is added.
- **Product main has moved** to `083ad5c`. Since `d2c00a9` it has gained the binding commits, X4-F3, J2a, E2a and I1-b1. None touches X3c-3's 11 files, so integration rebases.
  - **Integration lead sets:** on the integrated commit, the lead runs release absence, two full sets of both targets and the real `check`, all serialized under the lock. Those runs include X4-F3's code, whose own lead sets matched X9-6.
  - **Your choice:** rerun now on the worktree, or accept on this evidence and leave the integration run to the lead, as with X9-6.
- **J4a is accepted and held.** It integrates after X3c-3, with §RW's six re-transcribed rows. X3c-3's rows don't include §RW's.
- **Shared machine:** take the lane lock (`mkdir "$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"`) for any cargo run, and release it only if your `mkdir` succeeded. Hold it unniced for a whole lead set, and keep cargo out of any waiting process's command line.

## Decide

- **Scope:** does the diff implement X3c r8 items 6, 6a, 9, 10, 11 (r8 note) and 13 faithfully: the standing read from committed per-Run rows only, inside the open transaction and before any insert; the byte-identical comparison against the least-ExecutionId row, lengths first; availability and pins on a first commit only; the one-sided `LEDGER.CORRUPT` mapping and the two invariant-row refusals; the charges; and no DDL, crash point, type, outcome, row or code? Does `commit.rs` change only in doc comments?
- **Tests:** do the ten new tests cover item 12b's list (the re-commit, a third commit with recovery, standing from committed rows only both ways, the three refusals, the non-retained record, another namespace, the unchanged first commit, the budget on both branches)?
- **The matrix (§RC.7):** are the census part and its checks, the observed values, `"r2": "same"` and its guard, R5's rule, the two mutations, `run-out` and the checker's `UNIT_VALUES` what §RC.7 asks, and nothing more?
- **Transcription (§RC.4, frame rule 1):** were the 22 rows transcribed from §RC and the census only, before any row ran, with the 381 landed rows byte for byte? Rerun `transcribe_x3c3.py` on `git show d2c00a9:crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json`; it must reproduce the worktree's file (`292f8105…`).
- **The census and the stops (§RC.3, §RC.6):** do the census-only results match RC.3's predictions exactly (above), with the first commit's trace unchanged?
- **The 19 runs (§RC.5):** 18 end `Committed`, all unscored, no expected value re-transcribed, and the record differences limited to what RC.5 records (plus O-1)?
- **Rerun and compare:** run both censuses, `coverage`, your own release-absence record, and two full sets of both targets one at a time with nothing else running (now or on C′); run `precheck_x3c3.py` on your pair and on (lead-1, yours); compare every `normalizedSha256` and child trace digest with `lead-precheck.json` and the lead's records (not `timingGuard`); confirm that the real `check` refuses only on the clean-commit condition.
- **Judgment calls 1 to 16** and **observations O-1 to O-3**: acceptable?
- **Inventory:** confirm that no successor is needed (judgment call 1).

Write REVIEW.md and review.json under the output directory. review.json needs:
- `"verdict"`: `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectSha256"`: `bb86dd404622ecd4433356e0b1c0c706740ed630ca371430966c917042fd1802`, the diff's sha256, as a single string;
- `"inventoryCandidateAssessment"`: `{"verdict": "NOT-APPLICABLE", "reason": "no file added; v136 lists all eleven"}` or your finding;
- `"rerun"`: `"now"` or `"after-integration"`.

Do not commit.
