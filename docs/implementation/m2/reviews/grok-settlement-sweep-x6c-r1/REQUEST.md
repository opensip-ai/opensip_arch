Grok review r1: X6c, the authorized settlement sweep. This covers the sweep's settle write in `ledger_store` and the `store-gc` per-namespace step (law X6 r3 item 7 and item 12's X6c list, under `commit-recovery-readonly.v3.md` §4 and F53). It also covers X9 r2 item 5's `x6.sweep` points, X9 r2 gap G5, and inventory v127 (parent v126).

Claude Opus 5.5 leads. You are the single reviewer.

## Rules

- **What you may change.** Make no repository edits, commits, pushes or delegation. Write only under `/tmp/opensip-implementation/reviews/grok-settlement-sweep-x6c-r1`.
- **Builds and tests.** If you build or test, use a `CARGO_TARGET_DIR` under that directory. Run every test with a private TMPDIR: create a 0700 directory under `$(getconf DARWIN_USER_TEMP_DIR)` (for example `…/grok-x6c-tmp`). Never use the shared `/private/tmp/claude-501` tree, which other runs churn.
- **Git.** Run git read-only, and only against the worktree below.
- **Real home.** Never touch it: `~/Library/Application Support/OpenSIP` must stay absent.
- **Private fixture.** Never read or print the private 413 UUID fixture.
- **Toolchain.** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH`. Python is `python3.14`.

## The unit

X6 r3 item 12: "**X6c (storage and host).** The sweep's settle write in `ledger_store` and the `store-gc` per-namespace step. It depends on X6b, X1 and X2d's EXCLUSIVE lease primitive." Item 7 fixes what the sweep does:
1. **Admission.** It runs X1 `admit_ordinary_writer`, which holds the installation fence through the 468 gate.
2. **Lease.** For each registered N, it takes X2's EXCLUSIVE lease (`writer.lease` then `readers.lease`, each `LOCK_EX|LOCK_NB`) under that fence. A busy namespace is skipped and retained, never refused.
3. **Snapshot.** It reads one `ReadSnapshot` covering the receipt, the association and the custody row.
4. **Decision.** It decides per §4.2 through `join_ledger`.

Its only write is one `UPDATE attempt_custody SET phase='settled', settled_outcome=? WHERE … AND phase='admitted'` per transaction. The transaction is `BEGIN IMMEDIATE` with the ledger's own durability. The outcome is `committed` or `refused` only.

Leases are released in reverse order before the next namespace, and the fence is released last.

The sweep writes nothing in these cases:
- a busy lease;
- an unreadable ledger;
- a one-sided ledger (F23);
- an already settled row.

It never does any of the following:
- reuses a dead attempt's authority;
- takes a grant or an X4 guard;
- retries a commit;
- writes anything else.

Orphan objects are left in place ("Not claimed").

The rows come from item 8: "an unreadable ledger reports host I/O for that namespace and continues to the next." No CLI is wired; `store-gc`'s command surface belongs to X11 and M5.

## Law

All paths are under arch `docs/implementation/m2/` unless named otherwise. All are accepted.
- `carrier-recovery-x6/PROPOSAL.md` r3: items 1, 7, 8, 11, 12, "Forbidden substitutes" and "Not claimed". This is the law of this unit.
- `docs/v2/architecture/commit-recovery-readonly.v3.md`:
  - §4.1 to §4.3, the sweep;
  - §2 step 2 and §2.1, the matrix and the lawful interval;
  - §5, who may write `AttemptCustodyV1`.
- `docs/v2/architecture/commit-recovery-plan.v1.json`: F53, and F23, F24 and F36.
- `ordinary-platform-x1/PROPOSAL.md`: items 2, 4, 5 and 7.
- `project-root-x2/PROPOSAL.md` r8: item 7 (S7's modes, EXCLUSIVE, the busy row) and item 8 (rows).
- `crash-matrix-x9/PROPOSAL.md` r2:
  - item 5's `x6.sweep` row (`after-exclusive`, `after-snapshot`, `settle.commit` (`fallible`));
  - "Who places them", which requires X6c to place its own points;
  - C5 and gap G5;
  - F53's row.
- `refusal-suite-x8/PROPOSAL.md` r3. X8 assigns X6 no owner row (line 365: "Not owned here: … X6's recovery routing of B4"). Group I (`ledger_store` unnameable) is untouched, because the settle write stays crate-private.
- Your X6b review, `reviews/grok-recovery-admission-x6b-r1/REVIEW.md`. Its call 7 (a refused directory or ledger file closes the charged ledger) and call 13 (tests split by crate) carry over.

## Subject

Pins are in hashes.txt.

- **Product.**
  - **Worktree.** `/Users/sb/code/opensip-ai/opensip-x6c`, detached at `f880145` (main, with X6b integrated; the lock selects v126).
  - **The diff.** Save `git -C <worktree> diff` as product.diff and report its sha256. The seven new files are intent-to-add.
  - **Lead's value.** `880f980d25e3b92371c4c5d5b239463694563191cb2abb0ed2dd82e7dc671a6e`, 95576 bytes. 16 files changed, 2212 insertions(+), 5 deletions(-).
- **Arch.** These files are all untracked:
  - `repository-file-inventory.v127.json` (parent v126);
  - `settlement-sweep-x6c-inventory-v127-subject.json`;
  - `settlement-sweep-x6c-inventory-v127/`.

## What was built

### Security: `custody/settlement_sweep.rs`

This is new: a macOS module of `custody.rs`, exported from `lib.rs` as `SettlementSweep`, `SweepLease` and `SweepLeaseRefusal`. It is the custody half the sweep consumes (call 2).

**`SettlementSweep::admit()`.** This is `admit_ordinary_writer()` (X1), then the crate-private `admit_on(writer)`. Under the held fence, on the gate's ledger:
1. `join_store_endpoint` (X3a r5: S, G and K from the gate's one read, with the gate's and the receipt's rechecks).
2. One `gate_step` (followed by the gate's and the receipt's rechecks) that does two things:
   - `store_root_in` confirms `I/stores/S` against the endpoint's admitted marker. This is X6b's shared step.
   - `capture_registry` (X2b) lists every N held by exactly one row, that row ACTIVE, sorted (call 3).

A refusal is its 468c, X2 or X3a row. The writer is then dropped, which releases the fence.

`SettlementSweep` takes none of these:
- a trust admission;
- an X4 guard;
- an operation;
- a session;
- a grant;
- an ExecutionId.

**`lease(n)`.** This is X2's EXCLUSIVE for a listed N, taken as one `FenceHolder::fenced` step on the writer: X2d's discipline, with the gate's and the receipt's rechecks afterwards.
- **`exclusive_lease`.** It confirms `I/host`, `projects` and N with `required_directory`, then opens and judges both carriers with `open_carrier`. Then, as one effect reserved first (`effect_lease`), it locks `writer.lease` and then `readers.lease`, both `LockMode::Exclusive` and nonblocking. Last, it rechecks each locked carrier's name binding and the directories (`recheck_binding`, `recheck_namespace_at`).
- **Busy.** A held lock is `Ok(None)` through the new `namespace_lease::try_lock`, with `writer.lease` released again if `readers.lease` is held. This returns `SweepLeaseRefusal::Busy`. Nothing latches, and the gate is not spent (call 4).
- **The point.** Then `crash_barrier!("x6.sweep", "after-exclusive", step)`.
- **Refusals.** An unlisted N is `Row(Invariant)`. Any other refusal is its X2 item 8 row, which spends the gate, as every fenced refusal does (call 4).

**`SweepLease<'_>`.** It borrows the sweep mutably, so only one namespace is leased at a time.
- **What it lends:**
  - N, S, G, K and SHA-256(N) (`project_key_digest`);
  - `charge_store`, which charges its own fresh `WorkLedger::new()` at the owner's caps (call 5);
  - `I/stores/S`, its spelling and the uid, lent beside that charge.
- **Release.** Dropping it releases `readers.lease` and then `writer.lease`.

**`release(self)`.** It unlocks the fence last.

### Security: `custody/namespace_lease.rs` (X2d)

There are two additions, and X2d's own paths are unchanged:
- `HeldLease::exclusive(writer, readers)`, the subject-free EXCLUSIVE constructor;
- `try_lock`.

The module's "No lease is taken without the fence" stays true.

### Storage: `ledger_store.rs`

`WriteTransaction::settle_admitted_attempt(key, outcome)` is the only production settlement and the one `UPDATE attempt_custody` in the crate:

`UPDATE attempt_custody SET phase='settled', settled_outcome=?1 WHERE store_generation_digest=?2 AND namespace_id=?3 AND execution_id=?4 AND phase='admitted'`

- `?1` is `committed` or `refused`. `Admitted` is refused before any SQL.
- It runs after `verify_attempt_definition`.
- It returns the changed row count.
- `ac_monotone` still refuses a second settle.

### Storage: `ledger_store/sweep_settle.rs`

This is new, a child of `project_ledger`, beside X6b's `recovery_read`.

**`read_sweep_ledger`** is §4.3 step 2.
1. **Directories.** It admits `projects` and N only if present (`existing`, now `pub(super)` in `recovery_read`).
2. **Ledger file.** It observes the ledger's name, then opens it as a judged private file (`open_store_file`).
3. **Snapshot.** It charges the snapshot, then opens exactly one `ReadSnapshot`. The snapshot must name the same file and hold exactly the selected schema.
4. **Listing.** Inside it, it lists the admitted binding's `admitted` rows (store digest of (N, S, G, K) and N) in ExecutionId order, at most 4096 plus one (`more`) (call 7).
5. **Per row.** For each row, still inside the snapshot, it reads `read_pair` and `load_attempt` and charges their bodies as read. Then `join_ledger` decides (call 8):
   - `UnknownAttemptOpen` (both rows absent) gives `Refused`;
   - `ContinueCarrier { pending_settlement: true }` gives `Committed`;
   - `UnknownCustody` gives `Leave("one-sided")` when exactly one row is present, otherwise `Leave("contradiction")`;
   - `BindingUnusable` gives `Leave("binding-unusable")`;
   - anything else gives `Leave("invariant")`.

The read's outcomes, none of them settled:
- **Missing:** `projects`, N or the ledger is positively absent.
- **Busy:** SQLite reports busy.
- **Unreadable:**
  - a non-database;
  - a drifted schema;
  - another file at the path;
  - malformed rows.
- **ReadRefused:** a custody refusal of a directory or of the file.

**`settle_attempt`** is §4.3 step 4, for one decided attempt, as one charged step:
1. It rechecks the judged file's identity (`same_file`).
2. It opens `ExistingWriter` (`synchronous=FULL`, `fullfsync`, WAL required) and verifies the selected schema.
3. It runs `BEGIN IMMEDIATE`.
4. It runs exactly one statement, `settle_admitted_attempt`.
5. It commits at `crash_barrier!("x6.sweep", "settle.commit", fallible, transaction.commit()…, |_| ())`.

The results:

| Result | When |
|---|---|
| `Settled` | the transition committed |
| `Unchanged` | 0 rows changed; the transaction rolled back |
| `Busy` | the writer or its transaction found the ledger busy |
| `Unreadable` | the file changed, or could not be opened or written as the selected ledger |
| `Undetermined` | a `COMMIT` error, or either injected fault; never retried |

### Storage: `sweep.rs`

This is new, a macOS module that exports `sweep_namespace`, `NamespaceSweep`, `SettledOutcome`, `LeftAttempt` and `SweepStop`. `sweep_namespace(&mut SweepLease)` calls `sweep_from` over the `SweepSource` trait, which tests implement over a scratch store.

- **Step 2.** `read_sweep_ledger` on the lease's ledger, then `crash_barrier!("x6.sweep", "after-snapshot", step)` for every outcome, before any write. The outcomes before any write:
  - `NoLedger`, `Unreadable` and `Busy`;
  - `Budget`, when the lease's ledger refuses a charge.
- **Steps 3 and 4.** It settles each decided attempt in ExecutionId order, one transaction each (call 6).
  - `Leave` and `Unchanged` attempts go to `left`, with their reason (`not-admitted-at-write` for `Unchanged`).
  - The first `Busy`, `Unreadable`, `Undetermined` or ledger `Budget` stops the namespace's writes and is reported in `stopped` with its ExecutionId. Every later decided attempt is reported `after-stop` (call 10).
- **Result.** `NamespaceSweep::Swept { settled, left, more, stopped }`. It is an inert public report and grants nothing (call 13).

### Host: `maintenance.rs`

This is new. It is the inventory's already planned row, which the build plan names as `store-gc`'s owner (call 11).

- **`sweep_store()`.** `SettlementSweep::admit()` once; an admission refusal is `ended`. Otherwise it calls `run(sweep)`.
- **`run`.** It works over a `Sweep` trait, which `SettlementSweep` implements.
  - `sweep_one` leases N, calls `sweep_namespace`, and drops the lease before returning.
  - Each namespace is reported in order: `Skipped` (busy), or `Swept(NamespaceSweep)`.
  - A lease row ends the loop.
  - `release()` comes after the loop. A failed release is the host I/O row, unless a row already ended the sweep.
- **Item 8's rows (`namespace_row`):**

| Outcome | Row |
|---|---|
| unreadable | `HOST.IO_FAILURE` / `host-io` |
| the lease's ledger refuses a charge (budget) | `WORK.BUDGET_EXHAUSTED` |
| a stopped `Undetermined` | `DURABILITY.COMMIT_FAILED` (existing `CommitUndetermined`) |
| skipped, no ledger, SQLite-busy, a clean sweep, a busy stop | none |

  One-sided attempts are reported by ExecutionId and reason, with no row. `MIGRATION.CORRUPT` is on no row.

### Small changes

- `recovery_read.rs`: `existing` and `refused` become `pub(super)`.
- `project_ledger.rs`: declares `sweep_settle` and re-exports it.
- `commit_tests.rs`: declares `sweep_tests.rs` as its child module.
- `custody.rs` and the three `lib.rs` files: module declarations and re-exports.

## Judgment calls: please rule

1. **G5: the sweep's admission is not refused under a revoked view (narrowest reading; no law change).**
   - **The decision.** X1 item 4: `OrdinaryWriteAdmission` "grants none of … trust admission"; X1's composition performs none. X6 r3 item 7 lists exactly X1, X2's EXCLUSIVE, one snapshot and the decision, and "takes no X4 guard". The narrowest choice adds nothing: the sweep reads no trust record, so a revocation of a closure subject, including the running core's own release closure, does not refuse it.
   - **What the proof rests on.** §4.2's proof is custody (fence plus EXCLUSIVE), not trust.
   - **The ladders.** For the F18, F19 and F38 ladders this fixes R3 as `refused` (no receipt, lease free) and R4 as `terminal-not-committed`. X9-4 can transcribe them; recording that in X9's record is the lead's next step.
   - **The test.** `a_view_revoking_the_running_closure_does_not_refuse_the_sweep` publishes an accepted view revoking the writer's selected closure before the gate reads I. The sweep admits and leases.
   - **Rejected:** adding X4T's fenced trust admission to the sweep. Neither X1 nor X6 names it, and it would leave every revoked attempt `admitted` for as long as the revocation stands, with nothing else permitted to settle it.
2. **The custody half is a new security module.** Item 12 says "storage and host", but item 1 r3's rule ("custody owners are security-private, so their types are security's", for X1's writer, X2d's lease primitives, X2b's registry capture and X3a's endpoint) applies unchanged to the sweep.
   - **Rejected:** exporting X2d's primitives or the ordinary writer admission to storage or host.
3. **"Each registered N" means each N held by exactly one registry row, that row ACTIVE.** This is item 3 step 3's selection rule applied to every N. Two reasons:
   - X2d's presence rule (directories and lease files required) is the ACTIVE row's.
   - No M2 writer makes RESERVED, RETIRED or ABANDONED rows.

   Those rows, and duplicated N, are not swept.
4. **Busy versus refusal at the lease.**
   - **Busy.** X2d's `lock` turns a held lock into a refusal that fails the charged step, which closes the gate's ledger and spends the gate. That is right for its callers and wrong for "skipped and retained, never refused". `try_lock` returns `Ok(None)` instead; `lock` is unchanged.
   - **Every other lease-phase refusal** (a missing namespace directory or lease file, custody, I/O) keeps X2's FenceHolder rule: it is X2's item 8 row, it spends the gate and it ends the sweep. No later namespace is written, and the fence is still released last.
   - **Rejected:** continuing past a spent gate.
5. **One failure-latching ledger per leased namespace, at the owner's caps.** Fenced steps stay on the gate's ledger. Storage's snapshot and settles charge the lease's own ledger.
   - **Why.** The platform's latch closes a ledger on any failed charged step, including a custody refusal of the ledger file. One shared ledger would end the whole sweep at the first unreadable namespace, contrary to item 8's "continues to the next".
   - **Rejected:** charging storage to the gate's or the receipt's ledger.
6. **One transaction per settled attempt.** I read item 7's "exactly one statement, in one `BEGIN IMMEDIATE` transaction" and §4.3 step 4's "the single admitted → settled transition … in one transaction" per attempt. This also matches F53's "at most one transition per attempt" and X9's per-occurrence `settle.commit`.
   - **Crash behaviour.** A crash between transactions leaves each row in its pre-state or settled.
   - **Rejected:** many statements in one transaction.
7. **What the snapshot lists.** Only the admitted binding's rows: store digest of (N, S, G, K) and N, phase `admitted`, in ExecutionId order. Rows of another binding in the same file are neither listed nor touched (tested).
   - **The bound.** At most 4096 per namespace per sweep, with `more` observed from the 4097th, never guessed. The next sweep continues.
8. **The decision is `join_ledger`'s, nothing more.**
   - **Settle `committed`** needs "receipt and association both present and joined" (§4.2). X6b's call 9 (a missing Run material row is `UnknownCustody` to a reader) is not a sweep condition. Settling changes no commitment, and the reader still reports `run-material` afterwards.
   - **`UnknownCustody`** is split by fact: `one-sided` when exactly one of the two rows is present, `contradiction` otherwise. `BindingUnusable` and the standings an `admitted` row cannot have write nothing.
9. **Ledger observations, none settled.**
   - **Missing.** A positively absent `projects`, N or ledger has no attempt row to settle: `NoLedger`, no write, no row. F24's "never absence" governs a conclusion about an attempt, and the sweep draws none here.
   - **Unreadable** (host I/O, no write):
     - a non-database;
     - a drifted schema;
     - a non-private ledger file (a custody refusal, which closes only that namespace's ledger);
     - malformed rows.
   - **Busy.** A SQLite-busy snapshot is skipped and retained, like a busy lease, with no row: a foreign holder means proof is unavailable now.
10. **Write-time outcomes.**
    - **`Unchanged`** (0 rows: settled by something that ignored the leases) is left `not-admitted-at-write` and the sweep continues.
    - **`Busy`, `Unreadable`, `Undetermined` or `Budget`** stop that namespace's writes. Later decided attempts are reported `after-stop`.
    - **`Undetermined`** projects the existing `DURABILITY.COMMIT_FAILED` row and is never retried. The next sweep's single snapshot shows settled or admitted.
    - **No re-read.** Nothing re-reads a row to decide. The UPDATE's `phase='admitted'` guard and the trigger are the only write-time checks, besides the file identity and schema checks that custody of the file needs.
11. **The host report and its file.** The report is per namespace, with item 8's row only where an existing row fits: host I/O, budget, durability. One-sided attempts are reported by ExecutionId and reason (§4.2 "report the contradiction") with no D9 row. `store-gc`'s own D9 outcome and CLI belong to X11 and M5.
    - **The file.** The host file is the inventory's planned `crates/host/src/maintenance.rs` row, kept by value. Its description is broader than the file, not contradicted. Only `maintenance_tests.rs` is a new row.
12. **Rechecks.**
    - Each fenced step (admission, each lease) runs the gate's and the receipt's rechecks under the fence.
    - Storage's steps under the lease run none after them; the next lease's fenced step does.
    - `after-exclusive` sits after the fenced lease step returns, so it is reached only when both locks are held.
13. **Test split and the report type.** As X6b's call 13:
    - **Security** tests admission and leases on real scratch installations.
    - **Storage** tests `sweep_from`, the function `sweep_namespace` calls, over stores X3d-2's own steps committed, reading the result back with `recover_from`.
    - **Host** tests the loop over a scripted sweep.

    `NamespaceSweep` is a plain public report (the host tests construct it). Unlike `RecoveredCommit`, it is never an input to anything that grants.
    - **Not unit-tested here:**
      - an injected `COMMIT` failure (needs an armed `settle.commit`);
      - the 4096 bound (4097 fullfsync commits).

      Both are X9-3's F53 row: "kill the sweep at `x6.sweep.settle.commit.before` and `.after`".
14. **Out-of-date inherited descriptions** are left for the next description successor (inventory README):
    - `namespace_lease.rs` gains `HeldLease::exclusive` and `try_lock`, so its description is out of date by omission. Its "No fence-free lease" stays true.
    - `commit_tests.rs` is out of date by omission.
    - `project_ledger.rs`'s "Nothing here settles an attempt" stays true of it. The child `sweep_settle` settles, and it is its own row, as X6b's `recovery_read` reads.

## Tests

There are 18 new tests. All 18 also pass with `--features opensip-platform/crash-matrix`, with the points live and unarmed.

**Security, `settlement_sweep_tests.rs` (7).** Each runs on a scratch P0 with projects registered by released writers.
1. The sweep:
   - holds the fence throughout and lists the ACTIVE N sorted, with the endpoint's S;
   - leases each N EXCLUSIVE (both carriers refused to shared takers) with an empty fresh ledger;
   - releases each lease before the next, and the fence last;
   - writes nothing under I (every file's bytes and mtime unchanged).
2. Busy namespaces:
   - an APPEND-WRITE holder, and a SHARED-READ holder (where `writer.lease` is released again), each make N busy with no lock left;
   - the next N still leases, and the first does once free.
3. Rows that end the sweep:
   - an unlisted N is the invariant row;
   - a missing `readers.lease` is X2's incomplete row;
   - after that, the spent gate refuses the other N, and the fence is still released last.
4. An installation without projects lists nothing.
5. A held fence refuses on the gate's busy row.
6. G5: a view revoking the running closure does not refuse the sweep.
7. Source pins:
   - no trust, guard, operation, session, grant, ExecutionId, fence open, wait, shared lock or write;
   - `admit_ordinary_writer()` once;
   - `writer.lease` locked before `readers.lease`, both exclusive;
   - `after-exclusive` once, after `.fenced(`.

**Storage, `sweep_tests.rs` (7).**
1. Committed-but-unsettled and crashed attempts:
   - before: the reader gives `CommittedHistorically { pending_settlement: true }` and `UnknownAttemptOpen`;
   - the sweep settles `committed` and `refused` respectively, and writes no receipt, association or object;
   - after: the reader gives `pending_settlement: false` and `TerminalNotCommitted` (the owner's composed case, §2.1 and C14);
   - a second sweep lists nothing and leaves the ledger bytes unchanged.
2. One-sided (F23). The receipt, or the association, is deleted behind its reinstalled trigger. The attempt is reported `one-sided` and left `admitted` (the reader gives `UnknownCustody`), while the crashed attempt beside it settles.
3. Missing and unreadable ledgers:
   - no `projects` gives `NoLedger`;
   - a deleted ledger file gives `NoLedger`;
   - a non-database, a drifted schema and a 0644 ledger give `Unreadable`, with nothing written.
4. A foreign `BEGIN IMMEDIATE` holder:
   - it stops the writes `Busy` at the first ExecutionId, the other is reported `after-stop`, and both rows stay `admitted`;
   - the next sweep settles both, once.
5. An `admitted` row under another store digest is never listed or touched.
6. A short ledger gives `Budget`, and the row stays `admitted`.
7. Pins:
   - ledger_store's one `UPDATE attempt_custody` is exactly the guarded statement, with no `'undetermined'`;
   - it is called once, from `sweep_settle.rs` only, and is absent from recover, commit, recovery_read, project_ledger and project_commit;
   - `sweep.rs` and `sweep_settle.rs` hold no INSERT, DELETE, REPLACE, CREATE, UPDATE, staging, publish, create, barrier, SEAL, witness, sleep or retry;
   - `after-snapshot` is once, between the snapshot and the first settle;
   - `settle.commit` is once, fallible, after the statement.

**Host, `maintenance_tests.rs` (4).**
1. The order: namespaces in order, busy skipped, unreadable gives host I/O and continues, release last.
2. Ending the sweep:
   - a lease row ends the sweep, and the fence is still released;
   - a failed release is host I/O unless a row already ended the sweep.
3. Item 8's rows, exhaustively.
4. A source pin:
   - one admission;
   - the lease confined to `sweep_one` and dropped before it returns;
   - release after the loop;
   - no recover, RecoveryAdmission, commit facade, direct writer admission, MIGRATION, sleep or retry.

## Checks

These ran at f880145 plus this diff, with a private 0700 TMPDIR (`…/x6c-tmp`).
- **Workspace runs.** `cargo test --locked --offline --workspace --all-targets` twice: each 1678 passed, 0 failed and 3 ignored, across 17 test binaries. That is X6b's 1660 plus these 18.
- **Lints.** All clean, each with `--all-targets -- -D warnings`:
  - `cargo clippy --workspace --all-targets -- -D warnings`;
  - `-p opensip-platform --features crash-matrix`;
  - `-p opensip-security`, `-p opensip-storage` and `-p opensip-host`, each with `--features opensip-platform/crash-matrix`.
- **Formatting.** `cargo fmt --all -- --check` is clean. The `include!`d files (`settlement_sweep.rs`, `settlement_sweep_tests.rs`, `maintenance_tests.rs`) and `namespace_lease.rs` are clean under `rustfmt --check --edition 2024`.
- **`check_package_edges --lane host`** (worktree `cargo metadata`): passes against v126 and v127, with 20 declared and 20 resolved edges.
- **`verify_projection.py`** against the real lock at f880145: 55 rows, 278 corruptions refused.
- **`evidence/verify_scratch.py`** (v127 appended in memory to the worktree's lock, with the record's 55 rows): passes, with 87 inventory successors, 74 contract successors and 55 inheritance rows. v127 is selected.
- **`build_v127.py`** reruns produce the same bytes:
  - 948 files;
  - the 942 v126 rows equal by value, with six added;
  - 55 projection rows, each checked against the lock's inheritance before it is carried;
  - D2's four `after` texts checked.
- **Home.** `~/Library/Application Support/OpenSIP` is absent before and after.

## Decide

- Does X6c meet X6 r3 item 7, item 8's sweep row, and item 12's X6c list, under §4 and F53? In particular, check each of these:
  - **Admission:**
    - X1's admission and nothing else (no trust, guard, grant or ExecutionId);
    - the fence held throughout and released last.
  - **The lease:**
    - X2's EXCLUSIVE per namespace (`writer.lease` then `readers.lease`, `LOCK_EX|LOCK_NB`), with no wait and no upgrade;
    - a busy namespace skipped and retained, never refused;
    - each lease released before the next namespace.
  - **The snapshot and the decision:**
    - exactly one ledger snapshot per namespace, deciding through `join_ledger` with no re-read;
    - the one settle statement, `committed` or `refused` only, one transaction per attempt, with the ledger's durability;
    - nothing written for a busy, unreadable, one-sided or settled row;
    - an unreadable ledger reported as host I/O, with the sweep continuing.
- Is call 1 a lawful resolution of G5, or does it need law?
- Are `after-exclusive`, `after-snapshot` and `settle.commit` (fallible) right in name, kind and place?
- Is v127 right on v126, with the six added rows' text and the carried 55-row projection?
- Is anything else wrong?

## Output

Write REVIEW.md and review.json to `/tmp/opensip-implementation/reviews/grok-settlement-sweep-x6c-r1`. Do not commit.

review.json must contain:
- `"verdict"`: `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectManifestSha256"`: the sha256 of `settlement-sweep-x6c-inventory-v127-subject.json`. The lead's value is `d523b6311e63e1c4b7185d85418d370605b38712b4ed2ea0e8bcedc982a5d354` (2146 bytes).
- `"inventoryCandidateAssessment"`, with:
  - `verdict` and `requiredFindings`;
  - `path`, `bytes` and `sha256` of `repository-file-inventory.v127.json` (lead: 529197 bytes, `ba6133904aa9c92a44aafb4ff73cdc9774c8fe853670bce6a4e417403d8a3fb4`);
  - `parent`: the v126 pin (519279 bytes, `3858f185c78ab74641afeddf92b9063fd5876a84fa0ca4974656f5e45d87c289`);
  - `successorRecord`: the pin of `settlement-sweep-x6c-inventory-v127/successor.json` (lead: 145385 bytes, `bb66ade1b178abf71550db1c1d69a4d28fedbe7b43c849e8dae95a169950ac1c`).
