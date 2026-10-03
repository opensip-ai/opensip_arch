Grok review: unit X9-5 r1, the crash matrix's host rows (law X9 r15 item 12), with inventory v133 on v131. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT**.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x95-r1.
- You own the native lane for this review:
  - Use a CARGO_TARGET_DIR under that directory.
  - Use a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
  - Run nothing in parallel with the matrix sets, because F39's and F40's timing guard measures elapsed time.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Inputs

All inputs are pinned in `hashes.txt`.

### Laws

- **X9 r15:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL-r15.md`, accepted by Codex, sha256 `0d195ff1…`. `PROPOSAL.md` holds the same text plus the acceptance line.

  The relevant parts:
  - item 12's X9-5 line, with its r10 and r13 notes;
  - item 5, with r10's and r11's host census;
  - item 6, with r10's runners, `candidate` child and candidate file, and r12's distinct variant;
  - item 7, with r8's trace rule, r12's `timingGuard` and r14's object-publication group order;
  - item 8 (the ladder), with r13's distinct R2 in host rows;
  - item 9's rows F01, F12, F16, F17, F32, F39, F40 and F53, with their r10, r12 and r13 notes;
  - item 10 (L1 to L11);
  - item 11, with r12's admission hold, r13's 5,000 ms limit and r15's guard end point;
  - the r10, r11, r12, r13, r14 and r15 headers;
  - the forbidden substitutes.
- **What r14 and r15 change for X9-5:** nothing in its rows or expected values (both headers say so).
  - **r14's group order** is already in host's `normalized_lines` / `object_groups_ordered`, byte-identical to storage's copy at `eb0d503`.
  - **r15's guard end point** ("the writer's first hold at any other point" after its first `x4.observer.tick` hold): host's two tick-armed scripts (F39, F40 latch) arm only `x4.observer.tick#*=hold` and `x3c.evidence.commit.before#1=hold`. The tick thread stays held at `#1`, so the first other hold is the admission hold the parent awaits. The measurement is unchanged.
  - **r15's `unit` member** belongs to X9-4. Host's file needs none.
- **The owning laws the rows transcribe:**
  - X7 (`finalization-x7`): the caller route, the delivery phase, remedies;
  - X5 r3 item 3: host's order, replay before custody;
  - X3d r8 and X3d-3's synthetic run candidate;
  - X3b (`journal-x3b`): item 4a and item 13's rollover crash table;
  - X6 r4 and X6c: the `store-gc` step;
  - X4 r7 (the gate and the observer) and X4T (C5);
  - the owner's `commit-recovery-readonly.v3.md`.

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-x9-5`, detached at main `eb0d50398035fe3532dadc332f88cf1d8bc4cb69` (X9-3 integrated). Nothing is committed. The two new files are intent-to-add, so `git diff eb0d503` includes them.
- **Diff:** `git diff eb0d503` is 147921 bytes, sha256 `1276f8f5a248bace1e45e22e04fa34ecf609b755a7e8ffaec28dbb05ca87d276`. It covers 5 files, +2371 −6.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`.

### Inventory

- `repository-file-inventory.v133.json` (candidate; parent v131, which the lock at `eb0d503` selects);
- `crash-matrix-x95-inventory-v133/`;
- `crash-matrix-x95-inventory-v133-subject.json`, sha256 `3b9cc6f1e0d5afb9f8d765a476e113c5cb577af1388d80b7ccc98c1437388198`.

They are untracked in arch. The number 132 was assigned to X9-3, which landed with no successor, so 132 is unused. Succession is by the lock's parent pin, not by number.

### Lead evidence, in this directory

- **`lead-check-unit.json`:** `check-unit --unit X9-5` over the two lead run sets, with every run's `normalizedSha256`.
- **`lead-release-absence.json`:** the release-absence record both sets used. It is byte-identical to X9-2's and X9-3's.
- **`transcribe_required_runs.py`:** X9-5's transcription script, run before any lead run.
- **`lead-x92-regression-check-unit.json`** and **`lead-x93-regression-check-unit.json`:** `check-unit --unit X9-2` and `--unit X9-3` over two fresh storage sets each, run on this diff.

## What X9-5 builds

### Host `src/crash_matrix_support.rs` (r10)

- **Two runners**, each the process's one entry, each returning value reports only (no authority type):
  - `finalize_commit`: host's own `finalize` over the on-disk candidate, so replay runs before any custody (X5 r3 item 3), then admission, commit, finish and the fixed delivery phase. Its `FinalizeReport` carries the outcome, any end or end-step failure, the rollover, whether the optional phase failed, and the delivered bytes.
  - `store_gc`: X6c's step through `maintenance::run`, reported per namespace (`GcReport`).
- **The run candidate file**, `opensip.x9.run-candidate.v1`: `write_run_candidate` and `read_run_candidate` (the retained objects, blobs and claimed RunId). This is neither a fourth entry nor an authority type.
- **The fixed delivery phase:** a renderer that writes `FIXED_RESPONSE` (19 bytes) and an optional phase.

### Host `tests/commit_matrix_tests.rs` (new)

- **The gate.** It is a `[[test]]` with `required-features = ["crash-matrix"]` and whole-file under the support predicate. A plain test run skips it.
- **The children:** this binary re-executed by X9-0's driver under the scripted wall clock:
  - `fixture`;
  - `candidate`: r10's host order. Its one entry is `operation`. It opens a `CommitSession`, writes X3d-3's candidate, r12's distinct variant and the session's core closure to the scratch root, then ends refused before `prepare_commit`, which appends the latched gate's one `REV` (r13);
  - `finalize`;
  - `store-gc`;
  - `recover`;
  - `publisher`: the shared fenced revocation publisher, in a process that holds no operation. It revokes the `release` subject of the `candidate` child's core closure (r12 and r13).
- **The census (r10, r11).** It is the union of three unarmed runs, each run twice and required equal:
  - (a) a lawful `finalize` commit;
  - (b) an exhausted-carrier `finalize` (the reserved-slot plant at `…988`), whose `finish` runs the rollover;
  - (c) a `store_gc` run after an unarmed (a) on the same root, which must reach `x6.sweep.settle.commit`.

  That gives 218 points, a kill set of 271, and a census trace digest of `93d0922ab69945043d769e0361fd0121662052ffadf44970c5425d78511cf8d6` (1195 records).
- **The parent.** It runs each row's script step by step (`candidate`, `plant`, `arm`, `run`, `await … then kill | revoke-latch-resume | store-gc-resume`, `mutate`, `r2`) by blocking record reads. It captures the post state, runs item 8's ladder, and writes one run record per run and `matrix.json`.
- **The timing guard (r12, r13, r15).** The parent measures, on its monotonic clock, from reading the writer's first `x4.observer.tick` hold to reading its next hold, at `x3c.evidence.commit.before#1`. The clock is named once, as `type GuardClock = std::time::Instant;`, as in storage's target.
- **The trace digest:** r8's rule with r14's group order, the same code as storage's.

### Security `src/crash_matrix_sites.rs`

- The site pin names host's matrix target's whole-file support guard.
- The no-sleep pin covers the host target, and admits its one `GuardClock` line. "Named once" is now counted per file (judgment call 7).

### Host `Cargo.toml`

The `[[test]] commit_matrix_tests` target with `required-features = ["crash-matrix"]`.

### Host `tests/fixtures/crash-matrix/required-runs.v1.json` (new; r10)

This is host's file, separate from storage's. It has the same schema and the same `clockEpoch` (1791072000), and holds X9-5's rows only: 52135 bytes, sha256 `4fd160922f6772d48f77293754296e89e0c140ac5db2f8dd041d0acc431cd71c`.

The checker (`tools/check_crash_matrix.py`) and its tests are unchanged from `eb0d503`. `check-unit --unit X9-5` already exists.

## The rows (94)

| Case | Runs | What runs | Expected (law X9 r15 item 9 and the owning law) |
|---|---|---|---|
| F01 | 4 | Candidate variants: replay object missing, descriptor altered (replay refused); substituted target, substituted inventory | Replay-refused: X7's evidence-missing or input-refused row, nothing delivered, whole post state unchanged (r13). Substituted: invariant row, no ledger, no attempt row, no SEAL, the carrier gains exactly one `REV` (r13). No ladder |
| F12 | 2 | `fail-after` and `fail-before` at `x3c.evidence.commit` (host's caller route) | `DURABILITY.COMMIT_FAILED`, remedy `commit-undetermined`, subject ExecutionId, nothing delivered. Landed: R1 CH pending, R2 (distinct) Committed, R3 committed, R4 CH. Not landed: UAO, refused, TNC |
| F40 | 3 | F12's two scripts under case F40; the latch variant: F39's script with `x3c.evidence.commit.after#1=fail-after` (r13) | As F12; latch: gate latched, R1 CH pending, R3 committed, R4 CH; R2 refused at admission, unscored (r13, C5). Timing guard |
| F16 | 1 | `fail-before` at `x7.delivery.required.before#1` | `DELIVERY.REQUIRED_FAILED/DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, exit 4, 0 bytes delivered, RunId disclosed; R1 CH; R2 (distinct) Committed |
| F17 | 1 | `fail-before` at `x7.delivery.optional.before#1` | Authoritative, 19 bytes delivered, optional failed, RunId claimed; R1 CH; R2 (distinct) Committed |
| F39 | 1 | r12's script: tick and `x3c.evidence.commit.before#1` held; publisher revokes; one tick; latch; resume | Committed with the latch, projected `DELIVERY.REQUIRED_FAILED`, remedy `renderer-failed-after-commit`; R1 CH; R2 refused at admission, unscored (r13). Timing guard |
| F32 | 76 | `tail-987` and `tail-988` plants; 74 kills at the rollover points of X3b item 13's crash table (`tail-988` plant) | `…987`: commits, R1 and R4 UQ `journalContiguity` (r13), R2 busy with `rolled:2`. `…988`: busy with `rolled:2`, R1 UC `ledger-missing`, R2 Committed, R4 UAU. Kills: R1 UC `ledger-missing`, R3 nothing; R2 by window: busy and `rolled:2` (witness OK or REVERT), or Committed with no rollover (witness OPEN or OK), R4 to match |
| F53 | 6 | `store-gc` after a commit, after a crash, during a live writer, on a mode-000 ledger; kills at `x6.sweep.settle.commit.before` and `.after` | Settles `committed`, or `refused`, once; skips the live namespace; Unreadable with `HOST.IO_FAILURE`, then settles after the restore; after a killed sweep the next sweep settles each row exactly once. No ladder |

**How the rows were transcribed.** They were transcribed before any lead run, from the law, the host census, and nothing read back from a run:

```
transcribe_required_runs.py <host census.json> <census-trace-b.txt> <out>
```

- **Where F32's kill points and windows come from:** the census's exhausted-carrier run (b).
- **Rerunning it** on either census run (`target/opensip-x9/x95-census0` or `x95-census1`) reproduces `required-runs.v1.json` byte for byte.

## Lead results

All checks ran on `eb0d503` with this diff, a private 0700 TMPDIR, and nothing else running.

| Check | Result |
|---|---|
| Full workspace without the feature, run 1 | 1744 passed, 0 failed, 3 ignored |
| Full workspace without the feature, run 2 | 1744 passed, 0 failed, 3 ignored |
| Feature lane: `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets` | 1620 passed, 0 failed, 3 ignored, including host's matrix target's 4 tests (run after 03:00 UTC) |
| Clippy `-D warnings`: workspace (no feature); the four crates with `crash-matrix`; security, storage and host with `scenario-fixtures` | Clean |
| `cargo fmt --all --check` | Clean |
| `check_package_edges.py --lane host` against v133 | Passed |
| Checker unit tests | 17 OK |

### The X9-5 lead sets

- **How they ran:** `OPENSIP_X9_RUN_SET=x95-lead-1`, then `x95-lead-2`, one after the other, each with `OPENSIP_X9_RELEASE_ABSENCE=<lead-release-absence.json>`:

  ```
  cargo test --locked --offline -p opensip-host --features crash-matrix --test commit_matrix_tests x9_5_matrix -- --exact --test-threads=1
  ```

  An earlier, interrupted set is kept aside as `x95-lead-1.aborted`. It is not evidence.
- **Runs:** 94 of 94 PASS in each set, with 0 FAIL and 0 HARNESS-ERROR. The sets took 727 s and 709 s.
- **Timing guard:**
  - F39 measured 1,036 and 1,054 ms;
  - F40's latch variant measured 1,028 and 1,096 ms.

  All are under 5,000. They are shorter than storage's F44 and F45 (about 2,800 ms). The lead has not established why; no expected value depends on it.
- **check-unit:**

  ```
  check_crash_matrix.py check-unit --repository . --unit X9-5 \
    --run-set target/opensip-x9/x95-lead-1 --repeat target/opensip-x9/x95-lead-2 \
    --required crates/host/tests/fixtures/crash-matrix/required-runs.v1.json \
    --commit eb0d50398035fe3532dadc332f88cf1d8bc4cb69
  ```

  It passed: 94 runs, census 218 points, kill set 271, 77 killed points, limits L1 to L11, repetitions agree, `matrixPass: false`.
- **Normalized digests:** the 94 `normalizedSha256` values (18 distinct) are in `lead-check-unit.json`. The SHA-256 of their canonical map (sorted keys, no spaces) is `5446751d769edc875a924abd07b288f0c4ae9c47c54d23c757c6f98095ebb285`.
- **matrix.json:** set 1 is `318f3d71…`, set 2 is `130fd838…`, 46655 bytes each. Both carry census trace digest `93d0922a…`.

### The X9-2 and X9-3 storage regression

This diff touches `crash_matrix_sites.rs`, a security source both storage units' lanes compile. Four storage sets ran fresh on it, one after the other.
- **X9-2** (`x95-x92reg-1`, `x95-x92reg-2`):
  - 231 of 231 PASS in each set;
  - `check-unit --unit X9-2` passed: census 212, kill set 281, 219 killed points, repetitions agree;
  - its map is `4e5cba34…`, equal key for key to X9-2's accepted map.
- **X9-3** (`x95-x93reg-1`, `x95-x93reg-2`):
  - 57 of 57 PASS in each set;
  - `check-unit --unit X9-3` passed: census 227, kill set 289, 11 killed points, repetitions agree;
  - its map is `b0f0a5a8…`, equal key for key to X9-3's accepted map;
  - F44 and F45 measured 2,835 to 2,844 ms.

### Release absence

- `opensip-cli` was built in release with no features: 6315264 bytes, `b32604fe8c83343a93e7e38f023abc330afda2fa0f7cb255c842ab2b52aa5e49`, the same bytes as X9-2's and X9-3's.
- The scan found no `OPENSIP_X9_` string and no registered scope name.
- `cargo build --release -p opensip-storage --features crash-matrix` and `-p opensip-host --features crash-matrix` each exited 101 at the compile guard.

### Inventory v133

- **Contents:** v131 plus two rows, `commit_matrix_tests.rs` (test) and host's `required-runs.v1.json` (fixture). That gives 967 files, with 965 rows equal by value. There is no new edge. The projection is 55 rows with `supersessionsFolded: 0`.
- **Checks:**
  - `evidence/build_v133.py` reruns to the same bytes.
  - `verify_projection.py` against the lock at `eb0d503`: PASS, 55 rows, 278 corruptions refused.
  - `evidence/verify_scratch.py` over this worktree passed: 93 inventory successors, 75 contract successors and 55 inheritance rows, with v133 selected.
- **The lock:** the lock at `eb0d503` is byte-identical to `b999ae3`'s, so it still selects v131.

### Real home

`~/Library/Application Support/OpenSIP` was absent throughout.

## Judgment calls

**From development, recorded in the X9 r13 request ("X9-5's own calls"):**

1. **F32's literal reading of X3b item 4a case 2.**
   - **The text:** a TERMINAL tail whose witness reconciles OK or ADVANCE takes one action, OPEN: the witness `COMMITTED (G+1, 0)`. Item 13's crash table's "ADVANCEs on the closing tail, which is OPEN" is that one write.
   - **The rows:** a kill before the G+1 witness is durable expects R2's witness action OPEN; a kill after it expects OK.
   - **The evidence:** ten F32 kill rows passed only after this correction. The law is unchanged by it.
2. **The substituted-target candidate retains the closure's blobs.** Only the target is substituted, so the run is refused on X3d item 3 step 1's invariant row (r13), not for a missing blob.
3. **F01 and F53 run no ladder.**
   - F01 creates no attempt row, so the ladder has no attempt to recover.
   - F53's rows are the sweep's own sequence, scored as `gc1` to `gc3`.
4. **The publisher child runs under the scripted clock**, like every matrix child. It holds no operation, as item 11 requires.
5. **R1 for F16, F17 and F39 is `committed-historically:*`.** The rows state CH and leave the settlement member unstated, so the `:*` suffix admits any, as X9-2 call 5 did.

**Made in this unit:**

6. **The timing guard's end point under r15.** No code change was needed. Host's awaited point is the writer's first hold other than the tick, because only the tick and the admission hold are armed and the tick is held at `#1`.
7. **The `GuardClock` count is per file.** The sites pin now allows the one `GuardClock` line once in each matrix target (storage's and host's), not once in total. Every other line stays pinned.
8. **The new files are intent-to-add** (`git add -N`), so the subject diff includes them, as X9-2's did. Nothing is staged otherwise.
9. **Inventory number 133 with 132 unused** (see Inventory). The successor is by parent pin. `crash-matrix-x95-inventory-v133/` gains a README, `verification.json` and `verifier-anchor.json` in X9-2's shape.

## Decide

- **Scope:** does X9-5 implement X9 r15's X9-5 scope faithfully, and nothing of X9-4 or X9-6? That scope covers:
  - the two runners;
  - the candidate file;
  - the fixed delivery phase;
  - the `candidate` and `finalize` children in host order;
  - the host census;
  - the host required-runs file and its 94 rows as transcribed;
  - r13's host rulings.
- **Constraints:** are item 6's constraints kept?
  - test-only, crash-matrix only;
  - no new cfg site beyond the pinned guard;
  - no authority type;
  - one entry per process.
- **Transcription:** is it lawful? It must use the census and the law only, fixed before any lead run.
- **Rerun and compare:**
  1. Run the host census (`OPENSIP_X9_CENSUS_ONLY=1` with `x9_5_matrix`), then rerun the transcription on its `census.json` and `census-trace-b.txt`. It must reproduce host's `required-runs.v1.json`.
  2. Make your own release-absence record (build, scan, and both refused feature builds).
  3. Run `x9_5_matrix` twice yourself, under `OPENSIP_X9_RUN_SET` names of your choice, one after the other, with nothing else running:

     ```
     cargo test --locked --offline -p opensip-host --features crash-matrix --test commit_matrix_tests x9_5_matrix -- --exact --test-threads=1
     ```

  4. Run `check-unit --unit X9-5 --required crates/host/tests/fixtures/crash-matrix/required-runs.v1.json` on your pair.
  5. Compare your `normalizedSha256` per run, and every child's trace digest, with `lead-check-unit.json` and the lead's run records under `/Users/sb/code/opensip-ai/opensip-x9-5/target/opensip-x9/x95-lead-{1,2}`. Agreement across the three executions is the determinism evidence. The `timingGuard` values are not compared.
  6. Optionally, run one X9-2 or X9-3 storage set and compare its map with `4e5cba34…` or `b0f0a5a8…`.
- **Judgment calls:** are calls 1 to 9 acceptable?
- **Inventory v133:** pin it, and assess it as an inventory candidate.

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `1276f8f5a248bace1e45e22e04fa34ecf609b755a7e8ffaec28dbb05ca87d276`, the diff's sha256, as a single string;
- "subjectManifestSha256": `3b9cc6f1e0d5afb9f8d765a476e113c5cb577af1388d80b7ccc98c1437388198`, as a single string;
- "inventoryCandidateAssessment": verdict, requiredFindings, the candidate's path, bytes and sha256, parent (v131's pin), and successorRecord (the pin of `crash-matrix-x95-inventory-v133/successor.json`).

Do not commit.
