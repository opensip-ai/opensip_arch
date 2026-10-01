Grok review r2: X6a, the security side of read-only carrier recovery, `journal_store::recovery_capture` (law X6 r2 items 1, 4, 10, 11 and item 12's X6a list), with X9 r1's `x6.recover` bracket points (item 5, gap G3), and inventory v124 (parent v123). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-recovery-capture-x6a-r2. If you build or test, use a CARGO_TARGET_DIR under that directory, and run every test with a private TMPDIR: create a 0700 directory under `$(getconf DARWIN_USER_TEMP_DIR)` (for example `…/grok-x6a-tmp`), never the shared `/private/tmp/claude-501` tree, which other runs churn. Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read or print the private 413 UUID fixture. Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH`; Python is `python3.14`.


## r2: what changed since r1

Your r1 review (`reviews/grok-recovery-capture-x6a-r1/REVIEW.md`, copied in from `/tmp/opensip-implementation/reviews/grok-recovery-capture-x6a-r1/`) was REQUIRED-FINDINGS. It ruled on call 1 and calls 2 to 11, 13 and 14, accepted them, and accepted inventory v124 (subject `68fe96ea…`). r2 fixes RF-1 and RF-2 exactly as you asked. Product main has since moved to 54e6166 (X5a, evaluator, host and doctor ingress only), whose lock selects v123; the unit and v124 moved with it (below).

- **RF-1 (the F43 arm).** `covers()` is unchanged and is used only by the anchor's case C. In the `k > t` arm, `covers` is now `f1.generation == query.generation && f1.seq >= query.seq` (owner step 3's `H.lastSeq >= k`). `Verdict::Hazard` carries `offending(h1)`, and `decide` copies it into `UnknownQuarantineCondition.offending`. New test `a_query_above_a_closed_generation_with_the_open_successor_floor_is_busy`: a closed generation 1, a stable case-1 `COMMITTED (2, 0)`, the floor at (2, 0, null) and a query one above generation 1's `TERMINAL` give `UnavailableBusy` after two captures; the SEAL below the tail still confirms on the same state.
  - **Reachability, disclosed.** After this fix, a floor in g at or above k > t is already refused earlier: at step 14 by `floor_against` when g is the newest generation, or by `floorOk` (no row at that position) when g is closed. So the hazard's quarantine arm now carries the digest but is reached by no test. It stays as owner step 3 writes it. `the_f43_hazard_retries_once_and_never_concludes_uncommitted` is unchanged: its F22 expectation, with the floor's digest, comes from step 14.
- **RF-2 (the closure chain).** The row sum is replaced by one count of the generations in `[g, newest)` whose highest-`seq` row is a `TERMINAL` (a correlated `MAX(seq)`), which must equal `newest − g`. A missing generation and a generation whose last row is not `TERMINAL` both fail; a second `TERMINAL` in one generation closes no other. The distinct-generation count is no longer needed and is gone. New test `an_intermediate_generation_whose_last_row_is_not_terminal_breaks_the_chain`: generation 1 closed, generation 2 holding a `TERMINAL` and then an `RA` (planted with the append trigger lifted), generation 3 closed and generation 4 open with a matching witness and floor give `ProtocolViolation` after two stable captures; with generation 2 ending in its `TERMINAL`, the same SEAL confirms. The missing-generation case in `a_broken_succession_or_gap_…` is kept.
- **Rebase and inventory parent.** The worktree is now detached at 54e6166 (X5a integrated); X5a touched no file of this diff, which applies unchanged. The lock selects inventory123 (X5a), whose 55 inheritance rows already carry D2's four `after` texts: X5a folded D2, so the lock binds those four as plain inheritance rows on v123, and no supersession is bound on v123. v124 is rebuilt on v123. `build_v124.py`'s PRIOR table adds `replay-join-x5a-inventory-v123/successor.json`, and its fold is now generic: it folds any supersession the lock binds on the parent, requires exactly four on v122 and none on v123, and checks that each of D2's four `after` texts is its row's effective description. `verify_projection.py` folds the same way. The two added rows' text also changes for RF-1 and RF-2: the validator row says the chain counts generations ending in a `TERMINAL` and states the hazard's same-generation rule, and the test row names the two new tests. Every inherited row is equal by value to v123's. v124 is now 497254 bytes (`94d37479…`), on 924 files, and the successor record is 145222 bytes (`2e58b830…`). r1's acceptance was on v122, so the inventory needs your assessment again.

## The unit

X6 r2 item 12 defines X6a (security) as `journal_store::recovery_capture`:
- the bracket;
- shape validation;
- the anchor table;
- the step 4 rule;
- the carrier precedence observations.

All of it is read-only. It depends on X3b-1b. X6b (storage and host: admission, `recover`, `RecoveredCommit`, the `ExistingAttempt` routing) and X6c (the sweep) are later units.

X9 r1's gap G3 gives X6a and X6b the `x6.recover` points: `after-lease`, `after-ledger-snapshot`, after each of `W1 H1 J W2 H2`, and `after-fresh-capture`. X6a places the bracket points and `after-fresh-capture`. `after-lease` and `after-ledger-snapshot` belong to X6b's admission and ledger snapshot. X9-0's macros are on main.

X8 r3 assigns X6 no owner rows. Its only X6 mention is B4's "then the invariant row until X6 routes it", which is X6b's routing. So X6a has no X8 cases.

Library only. Nothing calls it outside its tests until X6b, and nothing enables real-machine use.

## Law

All under arch `docs/implementation/m2/` unless named otherwise, accepted:
- `carrier-recovery-x6/PROPOSAL.md` r2, the law of this unit;
- `docs/v2/architecture/commit-recovery-readonly.v3.md`, the algorithm owner: §1 (vocabulary, carrier rows and precedence), §2 steps 0 to 4, §3 (anchor bound);
- `docs/coop/design-corrections/security/carrier-format.v3.md` §8 and §8.1 (open dispatch, phase routes);
- `journal-x3b/PROPOSAL.md` r10: items 2, 3, 4, 4a, 5, 5a, 8 and 13, and the forbidden substitutes. X6 was written against X3b r6, so judgment call 1 says how r7 to r10 are applied;
- `crash-matrix-x9/PROPOSAL.md` r1: items 4 and 5, L10 and gap G3;
- `refusal-suite-x8/PROPOSAL.md` r3 (no X6a rows);
- `verify-design-vd1/PROPOSAL.md` item 3 and `description-batch-d2/README.md` ("After selection"), for folding D2's supersessions into v124's projection;
- `docs/v2/architecture/commit-recovery-plan.v1.json`: F20 to F22, F28, F43 to F46 and F49.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x6a`, detached at `54e6166` (main). The lock selects v123 (X5a), with 74 contract successors and 55 inheritance rows bound to v123 (D2's four supersessions are on v122 and already folded into those rows). The unit was written on adc9081, reviewed in r1 at 933e78b, and moved to 54e6166 for r2; none of the intervening commits touches a file of this diff. Save `git -C <worktree> diff` as product.diff and report its sha256. The two new files are intent-to-add. Lead's value: `eb5e1c8868ee29d2322bbf79bef3e565019279f078848999870cfffb3e0b8db8`, 85509 bytes; 4 files, 2137 insertions(+), 1 deletion(-).
- **Arch:** these files, all untracked:
  - `repository-file-inventory.v124.json` (parent v123);
  - `recovery-capture-x6a-inventory-v124-subject.json`;
  - `recovery-capture-x6a-inventory-v124/`.

## What was built

**`crates/security/src/journal_store/recovery_capture.rs`** (macOS) is `carrier_floor.rs`'s child module, as `start`, `append` and `rollover` are. It is `pub(super)` and not re-exported (judgment call 9).

**`RecoveryQuery::checked`** takes the association's carrier half, which X6b joins in its one ledger snapshot:
- `journalCarrierDigest`;
- `grantGeneration` (at least 1);
- `journalSeq` (1 to `9007199254740990`);
- `journalBodySha256`;
- `operationRef` (physical `op-` grammar);
- `runId` (`run3:`).

**`recover_carrier(&CarrierLocation, &RecoveryQuery, &mut WorkScope) -> Result<CarrierRecovery, WorkBudgetError>`**:
1. **§1 row 1.** If `journalCarrierDigest` ≠ SHA-256(N), the result is `BindingUnusable`, with zero captures and nothing read or charged.
2. **One capture,** exactly `W1 H1 J W2 H2`:
   - **W** is the witness under the retained namespace, read by X3b's capped operational read.
   - **H** is the floor under `trust/carrier-floors/`. The floors directory is opened if present and must pass the private-directory check. An absent directory or file is positively absent; a failing check is unreadable.
   - **J** opens one read-only transaction through X3b's `read_only_carrier_connection` and the names-first dispatch. For a current carrier it reads:
     - the format row and binding;
     - the newest tail L, with the writers' predecessor check (`committed_tail`);
     - the requested generation's `COUNT(*)` and last row;
     - below the newest generation, the closure chain: the generations in `[g, newest)` whose highest-`seq` row is a `TERMINAL` must number `newest − g` (r2, RF-2);
     - the SEAL row at (g, k).

     The transaction is retained across `W2 H2`. Then the row digest at each decoded floor's position is read in it.
   - **Charges.** Every read is charged before it runs: each witness and floor read at X3b's `operational_read_cost`, plus the directory open and check, and J at a fixed cost (16 objects, 64 edges, 8 MiB).
   - **Points.** `crash_barrier!("x6.recover", "after-w1" | "after-h1" | "after-j" | "after-w2" | "after-h2", step)` follow each read. A `cfg(test)` hook observes the same points.
3. **The verdict of one capture,** in this order. The first match decides.

   | Order | Condition | Verdict |
   |---|---|---|
   | 1 | Carrier missing, zero bytes, or neither format's objects (§1 row 4) | `UnknownCustody{CarrierAbsent}` |
   | 2 | Format 1 or 2 (row 3) | `UnknownCarrierIncompatible` |
   | 3 | Unpublished complete set over an inherited `grant_journal` (the `{A, B}` prefix) | busy |
   | 4 | SQLITE_BUSY or LOCKED | busy |
   | 5 | Other unreadable carrier (not a database, not WAL, I/O) | `UnknownCustody{CarrierUnreadable}` |
   | 6 | Partial set, invalid definition, rows before publication, unpublished fresh set, or a violated boundary | candidate `Footprint` |
   | 7 | Foreign format row | candidate `CarrierBinding` |
   | 8 | Any unreadable file observation | unavailable |
   | 9 | Witness or floor naming another project | candidate `CarrierBinding` |
   | 10 | Broken succession | candidate `ProtocolViolation` |
   | 11 | g < `first_generation` (F46) | `UnknownCarrierIncompatible` |
   | 12 | Malformed witness or floor | candidate `WitnessMalformed` or `FloorMalformed` |
   | 13 | Floor absent | candidate `FloorLost` |
   | 14 | Each floor above X3b's copy tail (`floor_against`, with the open-successor exception), or failing `floorOk` at its own position | candidate `FloorRegression` |
   | 15 | g holds no row below the newest generation (F28) | `UnknownCustody{RecordPruned}` |
   | 16 | `COUNT` ≠ last seq | candidate `JournalContiguity` |
   | 17 | g below the newest generation, not closed, or a broken chain | candidate `ProtocolViolation` |
   | 18 | k > t (F43) | hazard, with `covers` = the floor in g at or above k (r2, RF-1), carrying the floor's digest |
   | 19 | SEAL join fails | `UnknownCustody{SealJoin}` |
   | 20 | Otherwise | the anchor |

   **The SEAL join** checks every member: schema 3, type `SEAL`, `operation_ref`, `run_id`, and the stored digest equal to the association's. The body must be canonical, its recomputed domain-framed digest equal, `seal_run_id` equal, and the body's `grantGeneration`, `seq` and `operationRef` equal.

   **The anchor** follows item 4a's `succession` over L and W1:

   | Reconciliation | Result | Needs |
   |---|---|---|
   | OK | A, `witness-committed-tail` | stable W |
   | ADVANCE | B, `witness-pending-at-tail` + `witnessWouldAdvance` | stable W |
   | OPEN{ok} | A + `witnessWouldOpen` | stable W |
   | OPEN{advance} | B + `witnessWouldOpen` | stable W |
   | REVERT, floor covers (g, k) | C, `sc-trust-floor` + `witnessWouldRevert` | stable H |
   | REVERT, floor does not cover | C′, `UnknownCustody{PendingAboveFloor}` + `witnessWouldRevert` | — |
   | QUARANTINE(kind) | candidate `Carrier(kind)` | — |
   | NoSuccessor | `UnknownCustody{NoSuccessor}` | — |

   An unstable bracket on a usable anchor is a retry.
4. **Decide** (owner step 3's determinism and step 4).
   - Confirmed, unknown or incompatible settles at once.
   - Otherwise exactly one fresh capture follows (`after-fresh-capture`). It decides unless it is itself adverse. Then a candidate, or a hazard with `covers` (the F22 condition, `FloorRegression`), is `UnknownQuarantineCondition{reason, offending digest}` only if three things hold: the fresh capture's witness and floor brackets are byte-stable, and both journal snapshots agree on L and on g's tail. Anything else is `UnavailableBusy`.
   - Every `Confirmed` has `limitation() = interior-bodies-not-authenticated`.

**`carrier_dispatch.rs`** gains `CapturedDispatch::inherited_present` and a non-current `inherited` flag. These keep the `IncompletePublication` dispatch's inherited-format observation, which was discarded before (judgment call 5). **`carrier_floor.rs`** declares the child module.

Nothing in the module writes. It has no `INSERT`, `UPDATE`, `DELETE`, `IMMEDIATE`, witness or floor publication, lock, rename or sleep, and a source pin checks this.

**Inventory v124** adds 2 rows to v123 (924 files): `recovery_capture.rs` (validator) and `recovery_capture_tests.rs` (test). Every inherited row is equal by value to v123's bytes. The 55 projection rows the lock binds to v123 are carried by stable path; their candidate selectors move by the two inserted rows. D2's four (`store_lineage.rs`, `installation_session.rs`, `read_premise.rs`, `initial_installation.rs`) arrive already folded by X5a, each with its raw `before` and D2's `after` as its effective description, and the builder checks that they stay so. The count stays 55. Its README lists the existing rows this unit touches: `carrier_dispatch.rs` (description stays true) and `carrier_floor.rs` (out of date by omission, left to the next description-only successor).

## Judgment calls: please rule

1. **X3b r10 against X6's r6 basis: the anchor through item 4a.** Owner step 3's table assumes one generation: the witness names `A.grantGeneration`, H is that generation's floor, and t is its tail. Under X3b r7 to r10, a closure (the `TERMINAL`) moves the witness to G+1 (OPEN, case 1). The floor follows to (G+1, 0, null) only after `COMMITTED 0`, and it may lag in G while G+1 fills.
   - **Checked against r10.** The rules X6a relies on are these, and r10 changed none of them after r7:
     - closed generations (item 4a);
     - OPEN and who performs it ("X6 also reports `would-OPEN`", item 4 r7);
     - the open-successor floor exception (r9);
     - the predecessor check;
     - no reconciliation after an uncertain outcome (r9; X6a reconciles nothing);
     - the `TERMINAL` window (item 5a).
   - **What X6a does.** It applies X3b's own `succession`, `floor_against` and copy tail to the newest tail L.
     - On an open newest generation whose witness names g, this is exactly the owner's A, B, C and C′.
     - On a closed g, the witness anchors the newest effective tail. A floor in a later generation covers every record of g, because it is written only after g's `TERMINAL` and the successor's `COMMITTED 0`.
     - A `PENDING` after a `TERMINAL` is a quarantine candidate (item 4a: "never lawful"), not case C.
     - A floor at (G+1, 0) with a witness naming G is regression, as X3b says.
   - **Not a contradiction.** X3b r7 item 4 itself assigns `would-OPEN` to X6.
   - **Rejected:**
     - the literal "W.grantGeneration == A.grantGeneration". Every SEAL in a closed generation would then be busy forever.
     - the pre-M2 `generation_anchor` kernel. It requires `floor.grantGeneration == query.generation`, so it reads the lawful post-rollover floor (G+1, 0, null) as `floorMalformed`. A test pins the adapted behaviour.
2. **Targeted reads, not the full population.** The existing `bracketed_capture` and `generation_population` read and chain-verify every record of every generation, bounded by `max_records`. Owner step 3 needs only contiguity, `floorOk` and the SEAL join; §3 says the interior prefix is not authenticated; and X3b item 9 has the writer's start "read only the tail record". So J runs about eight bounded queries in one snapshot, and contiguity is `COUNT(*) = MAX(seq)` under the `(grantGeneration, seq)` primary key.
   - **Not changed:** `generation_anchor.rs` and `bracketed_capture.rs`, the pre-M2 read side.
   - **Rejected:** reusing the population. Its charge grows with the journal, so recovery of a long-lived namespace would end on the budget row.
3. **Step 4's "matching carrier naming"** is the association naming the admitted carrier (§1 row 1, decided before any read). §1 row 2 makes a witness naming another project a quarantine "with the Step 4 stable observations", which the literal reading would forbid.
4. **A present carrier with no floor is X3b's `floorLost`,** a quarantine candidate under step 4. The owner's table assumes a floor. X3b's floor-first INIT makes "floor absent beside a carrier" mean lost (X3b item 3). The pre-M2 kernel's "floor-absent" unknown is not kept.
5. **The unpublished complete object set** is the lawful `{A, B}` prefix (busy) only over an inherited `grant_journal`. On the fresh path, DDL and the format row commit in one transaction (X3b item 3a), so it is a footprint candidate. That is why `carrier_dispatch` now keeps the inherited flag it already observed.
6. **Carrier read failures.**
   - SQLITE_BUSY or LOCKED is busy after the fresh capture.
   - A carrier that is not a database, not WAL, unopenable or failing I/O is `unknown-custody`. That is the `HOST.IO_FAILURE` projection, matching X3b's `Unreadable` row and "a missing, empty or fallback carrier … is unknown-custody".
   - An unreadable witness or floor (including a floors directory failing its private check) is busy after the fresh capture.
7. **F28.** X9 r1 L10 says F28 runs over "X6a's pruned-record fixture". X6a's fixture is generations 1 and 2 removed, generation 3 closed and generation 4 open. It passes the writers' predecessor check, and a SEAL association in generation 1 is `UnknownCustody{RecordPruned}`.
   - A gap inside the requested generation is not pruning. It fails the owner's contiguity check, which is a candidate (`JournalContiguity`).
   - A missing generation between g and the newest is a broken chain (`ProtocolViolation`).
   - The fixture is `cfg(test)`. Exposing it to X9's process runs is X9-2's `crash_matrix_support` work.
8. **SQLite's sidecars.** A read-only WAL open can create an empty `-wal` and a `-shm` where the writer's last close removed them. X3b's own reader does the same. These are not carrier state: the empty WAL holds no frame, and `-shm` is the shared-memory index. The tests' byte comparison covers the database, any non-empty WAL, the witness, the floors listing and the floor, and leaves those two out.
9. **Placement and visibility.** The file is `journal_store/recovery_capture.rs`, declared `pub(super)` under `carrier_floor`, so that it reuses X3b's private `CarrierLocation`, `committed_tail`, `succession` and `floor_against`. There is no crate re-export and no production `CarrierLocation` yet. X6b adds both from its admission, as X3b-3 did for the writer.
   - **Rejected:** a re-export now, which is an unused import under `-D warnings`.
10. **Point names.** The registry grammar is lowercase, so W1 to H2 are spelled `after-w1` to `after-h2`. `after-fresh-capture` is reached once, after the second capture's `H2` and before the decision. Each point sits where the `cfg(test)` hook observes, as X9 item 5 asks of existing hooks.
11. **Step 4 governs the F43 hazard's F22 report too.** The owner's hazard sentence names `stableH` and agreeing tails. X6a also requires `stableW`, since step 4 says all five observations precede any quarantine report.
12. **Closure.** A generation is closed by a `TERMINAL` row of either cause, as the writers' predecessor check reads it. No purge writer exists in M2. `carrier_quarantine` rows are never consulted, because X3b item 8 says no open trusts a stored marker.
13. **Unknowns settle at the first capture.** `SealJoin`, `PendingAboveFloor`, `CarrierAbsent`, `CarrierUnreadable`, `RecordPruned` and `NoSuccessor` are each decided from one snapshot and are not quarantine reports, so no fresh capture is taken for them. The pre-M2 kernel did the same.
14. **Budget.** The capture charges the caller's `WorkScope`, which is X6b's recovery ledger, and returns `WorkBudgetError` for X6b to map to the budget row. J's fixed cost covers its open, dispatch, queries and two values bounded at 4 MiB each.

## Tests

New: 25 tests in `recovery_capture_tests.rs` (security lib).
- **Bracket on every recovery.** Each one asserts the bytes are unchanged, and that the points come in order: one capture `W1 H1 J W2 H2`, two plus `FreshCapture`, or none for row 1.
- **The query.** Its closed representation.
- **Row 1.** No read and no charge.
- **Anchors.**
  - A at four tails;
  - B (F45);
  - C;
  - C′ with the floor below k and at INIT (F44).
- **The SEAL join.** Run, operationRef, digest, an RA at k, and a body that no longer hashes to its stored digest.
- **Adverse witness rows.** Each is a quarantine after 2 stable captures, with the offending digest:
  - beyond the tail;
  - equal sequence, other hash;
  - non-adjacent `PENDING`;
  - malformed (F20);
  - lower generation;
  - missing (F21).
- **Adverse floor rows.**
  - above the tail;
  - equal sequence, other hash (F22);
  - `floorOk`;
  - malformed;
  - lost;
  - no floors directory.
- **Foreign witness or floor.**
- **Step 4.** An unstable witness bracket, an unstable floor bracket, and disagreeing journal tails are each busy.
- **F49.**
  - A lawful append at W1, H1, J and W2 confirms, after a fresh capture except at W2.
  - An in-flight `PENDING` gives C or C′, never a quarantine, with nothing reverted.
- **F43.**
  - busy below the floor;
  - the F22 quarantine at the floor;
  - the reconciling retry confirming.
- **§1 precedence.**
  - missing, emptied and fresh-install carriers are unknown custody, and format 1 and 2 are incompatible, whatever the witness;
  - the `{A, B}` prefix is busy;
  - a partial or unpublished fresh set, and a foreign row, are stable quarantines, busy when unstable;
  - for a migrated carrier, an association below `first_generation` is incompatible ahead of a malformed witness and behind a foreign one.
- **X3b r10 succession.**
  - case 1 OK, with the floor at (G+1, 0, null) or in G;
  - case 1 REVERT as C, and C′;
  - `COMMITTED (G+1, 2)` is `uncertainTailLoss`;
  - OPEN from OK and from ADVANCE;
  - `PENDING` after a `TERMINAL`;
  - a floor at (G+1, 0) against a witness naming G;
  - a later open generation anchoring an earlier SEAL, A and B;
  - a witness naming a superseded generation.
- **Structure.** A broken succession, a generation gap, and a sequence gap.
- **F28's fixture.**
- **Unreadable.** An unreadable floor is busy; a non-database carrier is unknown custody.
- **Budget.** A short ledger returns `Edges`.
- **Source pins.** No write statement, open, lock, rename or sleep; the capture called exactly twice; each `x6.recover` point once.

All 25 also pass with `--features opensip-platform/crash-matrix`, with the points live.

## Checks

Product checks are at 54e6166 plus this diff. Arch verifiers run against the real lock at 54e6166, which selects v123.
- **Workspace runs:** two full runs of `cargo test --locked --offline --workspace --all-targets` at 54e6166 plus the r2 diff, each with its own private 0700 TMPDIR: each with 1616 passed, 0 failed and 3 ignored, across 17 test binaries.
- **Lints:** `cargo clippy --workspace --all-targets -- -D warnings` is clean. So are `cargo clippy -p opensip-platform --features crash-matrix --all-targets -- -D warnings` and `cargo clippy -p opensip-security --all-targets --features opensip-platform/crash-matrix -- -D warnings`.
- **Formatting:** `cargo fmt --all -- --check` is clean.
- **`check_package_edges --lane host`:** passes against v123 and v124, with 20 declared and 20 resolved edges.
- **verify_scratch** (v124 appended in memory to the worktree's lock at 54e6166, with the inheritance replaced by the record's 55 rows): passes, with 84 inventory successors, 74 contract successors, 55 inheritance rows and 4 inventoryPassageSupersessions; v124 is selected.
- **verify_projection against the real lock at 54e6166:** 55 rows, no supersession bound on v123 to fold, D2's four already folded; 278 corruptions refused.
- **`build_v124.py`:** reruns produce the same bytes. 924 files; the 922 v123 rows are equal by value; 55 projection rows, each checked against the lock's inheritance row before it is carried, with D2's four `after` texts checked as their rows' effective descriptions.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does X6a meet X6 r2 items 1 and 4 and item 12's X6a list, with owner steps 3 and 4 and the §1 carrier rows and precedence? In particular:
  - the five observations in order, with at most one fresh capture;
  - shape before comparison;
  - the full SEAL join;
  - A, B, C and C′ with their stability needs;
  - the hazard rule;
  - quarantine only under the five stable observations;
  - rows 1 to 4 of the precedence;
  - no write, wait or lock.
- Are the `x6.recover` points right in name and place for G3, given that X6b owns `after-lease` and `after-ledger-snapshot`?
- Do RF-1 and RF-2's fixes and their tests meet your findings? Is anything in r1's accepted calls changed by them?
- Is v124 right on v123, with the two added rows' r2 text, the carried 55-row projection and D2's four supersessions kept folded?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `recovery-capture-x6a-inventory-v124-subject.json` (lead's value `4445a794bea86c827679d211419521410ff4751b9d30eec68ea57613e46094ae`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v124, parent (the v123 pin), successorRecord (the pin of `recovery-capture-x6a-inventory-v124/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
