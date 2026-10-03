Grok review: unit X9-3 r1, the crash matrix's commit and recovery rows in storage (law X9 r14 item 12). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT**.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x93-r1.
- You own the native lane for this review:
  - Use a CARGO_TARGET_DIR under that directory.
  - Use a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
  - Run nothing in parallel with the matrix sets, because F44 and F45's timing guard measures elapsed time.
- Run git read-only, and only against the worktrees named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Inputs

All inputs are pinned in `hashes.txt`.

### Laws

- **X9 r14:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL-r14.md`, accepted, sha256 `f2800ff9…`, Grok's r14 subject.
  - `PROPOSAL.md` now holds the r15 draft (arch `a35d82e89`, assigned to Codex for X9-4). This unit was built and run under r14, and r14 is its law.
  - r15's header states that X9-3's timing-guard measurement is unchanged. Its optional `unit` row member is X9-4's to add.

  The relevant parts of r14:
  - item 12's X9-3 line, with its r12 and r14 notes;
  - item 6, with r12's distinct candidate variant;
  - item 7, with r8's trace rule, r12's `timingGuard` and r14's object-publication group order;
  - item 8, with R5 (r12) and F25 run as R1 only (r14);
  - item 9's rows F11–F15, F23–F25, F27–F29, F33, F36, F42–F45, F49, F52 and F53, with their r12 and r14 notes;
  - item 10 (L1 to L11);
  - item 11, with r12's admission hold and the timing guard, and r13's 5,000 ms limit;
  - the r12, r13 and r14 headers;
  - the forbidden substitutes.
- **The owning laws the rows transcribe:**
  - X6 r4;
  - X3d r8;
  - X3c (`ledger-blob-x3c`), item 10's rows;
  - X3b (`journal-x3b`);
  - X2 (`project-root-x2`);
  - the owner's `commit-recovery-readonly.v3.md` (§1, §2 step 2, step 3's anchor table and the §4 sweep).

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-x9-3`, detached at main `b999ae34ed567a010bd789488512884fa38df05b` (X9-2 integrated). Nothing is committed and no file is added, so there is no inventory successor.
- **Diff:** `git diff b999ae3` is 334747 bytes, sha256 `f0d7c4c1bba5cf70625940dcec08c1584255ed74e84b6c51a0192fa62347b2af`. It covers 10 files, +1556 −122.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`.
- **Baseline worktree:** `/Users/sb/code/opensip-ai/opensip-x9-3-base`, a clean detached `b999ae3`. It is used only for the X9-2 trace comparison below. Its run set is `target/opensip-x9/x93-base`.

### Inventory

None. No file is added. The planned rows (`commit_tests.rs`, the required-runs fixture, the checker and its tests, and the support modules) keep their rows. The lock at `b999ae3` selects inventory131. Assess ACCEPT on the diff.

### Lead evidence, in this directory

- **`lead-check-unit.json`:** `check-unit --unit X9-3` over the two lead run sets, with every run's `normalizedSha256`.
- **`lead-release-absence.json`:** the release-absence record both sets used. It is byte-identical to X9-2's.
- **`transcribe_required_runs.py`:** X9-2's script, extended for X9-3 and run before any kill.
- **`lead-x92-regression-check-unit.json`:** `check-unit --unit X9-2` over two X9-2 sets run on this diff.
- **`lead-x92-trace-comparison.json`:** for X9-2's F02–F05 and F07–F10, every child's trace digest and `normalizedSha256`, baseline against this diff.

## What X9-3 builds

### Storage `tests/commit_tests.rs`

**The X9-3 runner.**
- `x9_3_matrix` sits beside `x9_2_matrix`, sharing one `run_matrix(unit, cases, census, census_only)`.
- `x9_2_matrix`'s behaviour is X9-2's, except for r14's group order in the trace digest.

**X9-3's census (r8 item 5: "the recover and sweep censuses are X9-3's").**
- In one run, after the fixture, X9-3's census traces three unarmed drivers:
  - the commit driver's first commit;
  - `recover` of that attempt, which must give CH;
  - the sweep, which must settle it `committed`.
- Each driver's census must be equal across two such runs, or the census is a `HARNESS-ERROR`.
- The unit census is the union by point name, at the largest occurrence count, as r11 states for host's union. That gives 227 points and a kill set of 289.
- The census digest hashes the three drivers' normalized lines in that order. `census-trace.txt` prefixes each line with its driver.

**The step form.** It is used where children overlap: a writer held while a reader, a publisher or a sweep runs.
- **Steps:**
  - `spawn`, with `for` passing the target's drawn ExecutionId and namespace to a reader or sweep;
  - `await … then hold|pass|kill`, where `kill` is item 3's verified death;
  - `resume`;
  - `finish`;
  - `mutate … of`;
  - `ladder … of`.
- Children are recorded in spawn order.
- X9-2's script form is unchanged. It gains four optional directives: `commit: forget` (F42), `ladder` (a row's named steps), `request: binding-operation` (F27) and `r2: distinct` (r12).

**The ladder.**
- `ladder_steps` runs R1 to R4 as X9-2 did, plus r12's **R5** (`recover` of R2's own ExecutionId, and whether the two SEALs name one RunId).
- It also records R2's receipt count for the crashed ExecutionId (F15), and R3's per-attempt left reason and report kind (F23, F24, F53).
- The defaults are unchanged: all four steps, or R1 and R2 for a mutation row.

**Children.**
- **`revoke`** (r12): the fenced publication helper in its own process. It revokes the `release` subject of the session's own core closure, which the commit child writes to a scratch file.
- **`commit`:**
  - `forget=1` makes it `mem::forget` its `StoppedSession` (F42);
  - `distinct=1` makes it commit r12's distinct variant;
  - `closure-out` names the scratch file for its closure.
- **`recover`:** takes an optional `requested` binding (F27).

**Mutations.** All are made in the parent, with triggers lifted and reinstalled from their own SQL where a table is guarded:
- a receipt, association or attempt row deleted;
- a settle to `refused` or `committed`;
- the ledger set to mode 000, its header truncated, or a wrong store generation;
- an object deleted or flipped;
- the association's store generation, namespace, operation or execution swapped;
- the receipt's assurance or signer, the Run material's inventory digest, or the association's SEAL digest changed;
- the journal tail lost below `journalSeq`;
- X6a's pruned-generation shape planted on the real carrier;
- an availability successor marked `purged`.

**Recovery text.** CH and CAD now print, in order: the settlement (`pendingSettlement`, `legacyCustodyUnknown` or `settled`), the anchor, any diagnosis and the §3 limitation. CAD also prints its `evidence.*` details. UC adds its diagnosis. X9-2's recovery texts (UAO, UAU, UC without a diagnosis, UQ and UCI) are unchanged.

**The timing guard (r12; r13: 5,000 ms).**
- The parent measures, on its monotonic clock, from reading the writer's first `x4.observer.tick` hold to reading its admission hold (`x3c.evidence.commit.before#1`).
- A run above the limit, or a run missing either hold, is a `HARNESS-ERROR`.
- The clock is named once, in the single line `type GuardClock = std::time::Instant;` (judgment call 1).

**The object-publication group order (r14).** It is implemented in `normalized_lines` exactly as r14's steps 1–4 state.

### Storage support

- `run_candidate.rs` adds `synthetic_run_candidate_distinct` (r12): the snapshot's source file `extensionless` gets same-length salted bytes (`salted!\n`) before the fixpoint rewrite.
- `crash_matrix_support.rs` forwards it.

### Security support

- **`run_record.rs`:** an optional `timingGuard` member, `{monotonicMs, limitMs: 5000}`, and `TIMING_GUARD_LIMIT_MS = 5000`.
- **`crash_matrix_census.rs`:** the field added to its one `RunRecord` literal.
- **`post_state.rs`:**
  - an unreadable file is recorded by its path, size and mode, never read;
  - an undumpable SQLite file is recorded as `undumpable`;
  - the F49 tie-break orders rows in tables without a rowid (judgment call 2).
  - None of these changes an earlier capture's `logical`. X9-2's 231 `normalizedSha256` values are unchanged (below).
- **`crash_matrix_sites.rs`:** the no-sleep pin admits exactly the one `GuardClock` line in the matrix target.

### Fixtures and tooling

- **`required-runs.v1.json`:** X9-2's 231 rows are byte-identical. X9-3 appends 57 rows, for 288 in all: 130804 bytes, sha256 `9a34fc5630d4c8f63738c559ad8383c90e8abf4057dab6807899eb4c5e9b8cff`.
- **`tools/check_crash_matrix.py`:** `timingGuard` is an admitted run member. It is required, and must be within its limit, on every run whose script arms `x4.observer.tick`, and it is refused on any other run. It is not compared between repetitions.
- **The checker's tests:** one new test, 17 tests in all.

## The rows (57)

| Case | Runs | What runs | Expected (law X9 r14 item 9 and the owning law) |
|---|---|---|---|
| F11 | 4 | Kill after each `x3c.evidence.stage-*` | R1 UAO; R2 Committed; R3 refused; R4 TNC |
| F12 | 2 | `fail-after` and `fail-before` at `x3c.evidence.commit` | CommitUndetermined, nothing appended, reserve forfeited; landed: R1 CH pending, R3 committed, R4 CH settled; not landed: UAO, refused, TNC |
| F13 | 1 | Kill at `x3d.publish.commit-returned`; R2 distinct | R1 CH pending; R2 Committed; R3 committed; R4 CH settled |
| F14 | 1 | Kill at `x3d.publish.published`; R2 distinct (settle.before is X9-4's, r12) | As F13 |
| F15 | 1 | Kill at `x3d.finish.end-step.after`; R2 distinct | R1 CH; R2 Committed with one receipt for the ExecutionId |
| F23 | 2 | Kill at commit-returned, then delete the receipt or the association; ladder R1–R3 | R1 UC; R3 nothing, left `one-sided` |
| F24 | 3 | Kill at `x3c.attempt.commit.after`, then ledger mode 000, truncated header, or wrong generation; ladder R1–R3 | 000 and truncated: R1 UC, R2 refused on its X3c or X3a row, R3 nothing (Unreadable). Wrong generation (r12): R1 UAU, R2 Committed, R3 nothing (swept) |
| F25 | 2 | Committed, then an object deleted or flipped; R1 only (r14) | R1 CAD `evidence.missing` or `evidence.corrupt` |
| F27 | 5 | The association's store generation, namespace, operation or execution swapped; a request with a different operation | Store generation and namespace: BU. Operation and execution (r12): UC `ledger-join`. Request: BU `operation` |
| F28 | 1 | X6a's pruned-generation shape | R1 UC |
| F29 | 4 | Reader while the writer holds at `x3c.attempt.commit.after`, after the SEAL (`witness-committed/directory-barrier.after`), `after-staging` and `commit-returned` | UAO, UAO, UAO, CH pending; writer Committed |
| F33 | 4 | Receipt assurance, signer, inventory digest, association SEAL digest | R1 UC |
| F36 | 2 | F09's and F11's orphan SEALs; ladder R1–R5 | UAO, Committed, refused, TNC; R5 CH, same RunId |
| F42 | 2 | Forgotten stopped session after a non-landed evidence `COMMIT`; reader during a hold | UAO, Committed, refused, TNC; reader UB or UAO |
| F43 | 1 | Journal tail lost | R1 UB or UQ |
| F44 | 1 | F39's script with r12's hold; A holds at `x3b.append.rev.witness-pending/directory-barrier.after`; reader | Writer Committed(latched=true); reader UC `pending-above-floor:witnessWouldRevert` |
| F45 | 1 | As F44, at `x3b.append.rev.commit.after` | Reader CH pending under `witness-pending-at-tail`, `witnessWouldAdvance`, `interior-bodies-not-authenticated` |
| F49 | 2 | (a) Reader held at `after-j` while a writer appends (r12); (b) reader's stale snapshot | (a) CH pending; (b) UAO or UB |
| F52 | 11 | The eleven cells: four lawful, seven by mutation | Exactly one TNC (settled-refused/none) |
| F53 | 7 | Live, crashed, one-sided, inaccessible, already settled; kill at `x6.sweep.settle.commit.before` and `.after` | Busy/nothing, refused, nothing (one-sided), nothing (Unreadable), refused then nothing; next sweep refused or nothing |

**How the rows were transcribed.** They were transcribed before any kill, from the law, the census and nothing read back from a run:

```
transcribe_required_runs.py <x92 census.json> <x92 census-trace.txt> <x92 reference.json> <x93 census.json> <out>
```

- **The inputs:** X9-2's census and reference run (unchanged inputs; its rows are reproduced byte-for-byte), plus X9-3's census.
- **Where the kill points come from:** X9-3's census.

## Lead results

All checks ran on `b999ae3` with this diff, and a private TMPDIR.

| Check | Result |
|---|---|
| Full workspace without the feature, run 1 | 1744 passed, 0 failed, 3 ignored |
| Full workspace without the feature, run 2 | 1744 passed, 0 failed, 3 ignored |
| Feature lane: `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets` | 1616 passed, 0 failed, 3 ignored, with the matrix target's 5 tests (run after 03:00 UTC; see the finding below) |
| Clippy `-D warnings`: workspace (no feature); the four crates with `crash-matrix`; security, storage and host with `scenario-fixtures` | Clean |
| `cargo fmt --all --check` | Clean |
| `check_package_edges.py --lane host` against v131 | Passed |
| Checker unit tests | 17 OK |

### The X9-3 lead sets

`OPENSIP_X9_RUN_SET=x93-lead-1` and `x93-lead-2`, each with `OPENSIP_X9_RELEASE_ABSENCE=<lead-release-absence.json>`.

- **Runs:** 57 of 57 PASS in each set, with 0 FAIL and 0 HARNESS-ERROR. Each set took about 333 s.
- **Timing guard:** F44 and F45 measured 2,766, 2,767, 2,790 and 2,786 ms, all under 5,000.
- **check-unit:**

  ```
  check_crash_matrix.py check-unit --repository . --unit X9-3 \
    --run-set target/opensip-x9/x93-lead-1 --repeat target/opensip-x9/x93-lead-2 \
    --required crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json \
    --commit b999ae34ed567a010bd789488512884fa38df05b
  ```

  It passed: 57 runs, census 227 points, kill set 289, 11 killed points, limits L1 to L11, repetitions agree, `matrixPass: false`.
- **Normalized digests:** the 57 `normalizedSha256` values (30 distinct) are in `lead-check-unit.json`. The SHA-256 of their canonical map is `b0f0a5a8a7ab954345b391176dbea49a756c4ce3a13ce0d7b6320853dffd3b28`.
- **matrix.json:** set 1 is `fc0f98ba…`, set 2 is `d236e9cc…`, 41378 bytes each.

### The X9-2 regression

Two X9-2 sets ran on this diff (`x93-x92reg-1` and `x93-x92reg-2`).
- **Runs:** 231 of 231 PASS in each set.
- **check-unit `--unit X9-2`:** passed, 231 runs, census 212, kill set 281, 219 killed points, repetitions agree.
- **The normalized map:** it is `4e5cba342b438abb749f73861161e6cd4cf38e6bdbd992a00068507d5df3ddaa`, equal key for key to X9-2's accepted `lead-check-unit.json`. 0 of 231 differ.

### The trace comparison (r14)

X9-2's F02–F05 and F07–F10 (48 rows) also ran on the clean baseline worktree (`x93-base`).
- **Unchanged:** every `normalizedSha256` is unchanged. F07–F10's child traces are all unchanged.
- **Changed:** in F02–F05, exactly 14 of 22 runs change one child's trace digest, the killed child (`commit`, ordinal 1). Those are the kills at an object's middle or last occurrence, whose partial last group now sorts first. Kills at `#1` are unchanged, because their partial group is already first.
- **The next writer's trace does not change in any F02–F05 run.** Its confirmed objects are a prefix in digest order, and a confirmed group already sorts before a new one (`file-barrier.before` < `link.after`). r14's header lists the next writer among the children whose digests the rule changes. That overstates it, but no expected value depends on it.
- **The two new sets agree** on every trace.

### Release absence

- `opensip-cli` was built in release with no features: 6315264 bytes, `b32604fe8c83343a93e7e38f023abc330afda2fa0f7cb255c842ab2b52aa5e49`, the same bytes as X9-2's.
- The scan found no `OPENSIP_X9_` string and no registered scope name.
- `cargo build --release -p opensip-storage --features crash-matrix` exited 101 at the compile guard.

### Real home

`~/Library/Application Support/OpenSIP` was absent throughout.

### A finding outside this unit

X9-1's platform self-test `a_scripted_clock_gives_each_ordinal_its_own_increasing_wall_seconds` fails whenever the real wall clock is between 2026-10-03 00:00 and 03:00 UTC.
- **The cause:** its fixed epoch E is 1,790,985,600, and it asserts that the OS reading lies outside E to E+3 h.
- **The effect:** the feature lane failed once at 01:45 UTC and was rerun after 03:00 UTC.
- **Scope:** it is not X9-3's code. A follow-up should derive E from a fixed past or future date, never one near the run.

## Judgment calls

1. **The `GuardClock` line (coordinator-accepted).**
   - **The problem:** both no-sleep pins ban `Instant`. `observe_clock` would also take a wall reading, which the parent may not take (item 3).
   - **The fix:** the matrix target names the monotonic clock once, as `type GuardClock = std::time::Instant;`. The security pin admits exactly that line, at most once, and pins every other line as before.
2. **The F49 tie-break in `post_state.rs` (r14: the unit's call, not law).**
   - **The problem:** tables without a rowid dump in primary-key order, so two `admitted` attempts of equal shape sit in their drawn ExecutionIds' order.
   - **The fix:** rows of such tables are ordered by shape. Rows whose shapes tie are ordered by how each normalizes against a numbering primed on the rest of the dump, with every tied row left out.
   - **What it does not change:** no value is dropped, and a dump without ties is untouched. X9-2's 231 normalized digests are unchanged.
3. **Post-state tolerance.**
   - **The problem:** a mode-000 ledger cannot be read (F24, F53), and a truncated one cannot be dumped (F24).
   - **The fix:** an unreadable file is recorded by its path, size and mode in `logical.unreadable`, present only when non-empty. An undumpable SQLite file is recorded as `{"undumpable": true}`. Their bytes stay out of `raw` and in `raw`, respectively.
4. **The recovery text.** CH and CAD carry, in order:
   - the settlement;
   - the anchor;
   - the diagnosis;
   - the limitation (CAD first lists its `evidence.*` details);
   - for UC, the diagnosis.

   This lets rows require or exclude each member. Rows that leave a member unstated use the `:*` suffix (X9-2 call 5).
5. **X9-3's census.** It is the union of its three drivers, each equal across two runs, at the largest occurrence count, with the digest over their lines in order. That is the rule r11 states for host.
6. **F23 and F24 run R3,** although they are mutation rows, because their rows name R3. They run R1 to R3, with no R4.
7. **F42's forget variant follows a non-landed evidence `COMMIT`** (`fail-before`), so the forgotten attempt is `admitted` with neither row: R1 UAO, as the row states.
8. **F52's cells.**
   - The four lawful cells come from real runs: a kill at `x3c.attempt.commit.after`, a lawful commit, that commit swept, and that kill swept.
   - The other seven are mutations with the triggers lifted:
     - settled-refused/both;
     - settled-committed/none;
     - no-row/none;
     - no-row/both (CH `legacyCustodyUnknown`);
     - receipt-only;
     - association-only;
     - purged: an availability generation 1 `purged`, with the largest object removed, giving CAD `evidence.purged`.
9. **Expected values from the owning law where a row is silent:**
   - the settlement member in a confirmation;
   - F12's end disclosure, from X3d item 7 and X3c item 10: nothing owed or appended, the reserve forfeited, no end step;
   - F44's reason `pending-above-floor` (C′);
   - R5's `settled`.
10. **Mutation choices:**
    - F25 mutates the unique largest object; a tie is a `HARNESS-ERROR`.
    - F24's wrong generation changes the first digit of every row's store-generation digest.
    - F27's swaps rewrite one member of the association body.
    - F33's four variants change the receipt's assurance and signer, the Run material's first inventory digest, and the association's `journalBodySha256`.
    - F43 deletes the rows at and above `journalSeq` in its generation.
    - F28 plants X6a's pruned-generation shape (generations 1 and 2 pruned, 3 closed, 4 open), with the witness and the floor at (4, 1).
11. **The distinct variant's salt.** It changes the 8-byte source file `extensionless` to `salted!\n`, the same length, so only digests change and the derivation succeeds.

## Decide

- **Scope:** does X9-3 implement X9 r14's X9-3 scope faithfully, and nothing of X9-4 to X9-6? That scope covers:
  - the census;
  - the 57 rows as transcribed;
  - the distinct variant;
  - R5;
  - the timing guard;
  - r12's admission hold for F44 and F45;
  - r14's group order and F25.
- **Constraints:** are item 6's constraints kept?
  - the distinct variant is inputs only;
  - no new cfg site;
  - no authority type;
  - one entry per process.
- **Transcription:** is it lawful? It must use the census and the law only, fixed before any kill.
- **Rerun and compare:**
  1. Run X9-3's census (`OPENSIP_X9_CENSUS_ONLY=1` with `x9_3_matrix`) and X9-2's, then rerun the transcription. It must reproduce `required-runs.v1.json`.
  2. Make your own release-absence record (build, scan, refused feature build).
  3. Run `x9_3_matrix` twice yourself, under `OPENSIP_X9_RUN_SET` names of your choice, one after the other:

     ```
     cargo test --locked --offline -p opensip-storage --features crash-matrix --test commit_tests x9_3_matrix -- --exact --test-threads=1
     ```

  4. Run `check-unit --unit X9-3` on your pair.
  5. Compare your `normalizedSha256` per run, and every child's trace digest, with `lead-check-unit.json` and the lead's run records under `/Users/sb/code/opensip-ai/opensip-x9-3/target/opensip-x9/x93-lead-{1,2}`. Agreement across the three executions is the determinism evidence. The `timingGuard` values are not compared.
  6. Optionally, run one X9-2 set (`x9_2_matrix`) and compare its `normalizedSha256` map with `4e5cba34…`.
- **Judgment calls:** are calls 1 to 11 acceptable?
- **Inventory:** ACCEPT on the diff, with no successor.

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `f0d7c4c1bba5cf70625940dcec08c1584255ed74e84b6c51a0192fa62347b2af`, the diff's sha256, as a single string;
- "inventoryCandidateAssessment": `{"verdict": "ACCEPT", "candidate": null, "note": "no file added; ACCEPT on the diff"}`.

Do not commit.
