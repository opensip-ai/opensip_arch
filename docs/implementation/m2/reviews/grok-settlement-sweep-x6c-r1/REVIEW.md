# X6c r1 — authorized settlement sweep and the store-gc step

**Verdict: ACCEPT-UNIT.** Inventory v127 is ACCEPT on v126. Required findings: none.

**Judgment call 1 (G5): lawful resolution. No new law sentence.** The sweep's admission is X1's `admit_ordinary_writer` and nothing else. A revocation of a closure subject, including the running core's own release closure, does not refuse the sweep. X9-4 can transcribe R3 as admitted, with a crashed attempt settled `refused`, and R4 as `terminal-not-committed`.

Product worktree `/Users/sb/code/opensip-ai/opensip-x6c`, detached at `f880145e4b5f0cc4b6307db045b008f770fbc97b`. The lock's last inventory successor selects v126 (`3858f185c78ab74641afeddf92b9063fd5876a84fa0ca4974656f5e45d87c289`, 519279 bytes): 86 inventory successors, 55 inheritance rows. Product main has since moved to `3237afc273cedf6031b76adbd30bd6d6174cb866` (X4B-c, a test fixture, no inventory). This worktree is still at `f880145`. The subject is this diff, and it contains no X4B-c files. `git diff` is `product.diff`: 95576 bytes, sha256 `880f980d25e3b92371c4c5d5b239463694563191cb2abb0ed2dd82e7dc671a6e`, 16 files, 2212 insertions and 5 deletions. The seven new files are intent-to-add. `~/Library/Application Support/OpenSIP` is absent.

Law read at the pins: X6 r3 items 1, 7, 8, 11, 12, Forbidden substitutes, and Not claimed; owner `commit-recovery-readonly.v3.md` §4.1–§4.3, §2 step 2 and §2.1, and §5; F53, F23, F24, and F36; X1 items 2, 4, 5, and 7; X2 r8 items 7 and 8; X9 r2 item 5's `x6.sweep` row, who-places, C5, G5, and F53; X8 r3 line 365 (X6 has no owner row). X6b calls 7 and 13 carry over. Nothing wires a CLI command.

## Call 1, stated

G5 asks whether `admit_ordinary_writer`, which item 7 runs first, refuses when a closure subject is revoked. X9 r2 recorded that question as open and refused to choose R3 inside X9. The accepted sentences already answer it.

X1 item 2's admission is, in order: `produce_write_platform` (InitialCore and InitialPlatform; a development build ends at F0), the receipt's actor, core, and platform rechecks, the 468 gate, and those rechecks again under the held fence. X1 item 4 grants that admission the installation fence and the confirmed durability of I's and the I-parent's names. The same item's grants-none list includes trust admission, grants, live guards, and a commit capability. X1 item 7 is one entry per process, enforced by the one attempt and the one gate. X6 r3 item 7 lists the sweep as that admission, then X2's EXCLUSIVE lease, one snapshot, and `join_ledger`, and says the sweep takes no X4 guard. §4.2's proof that no writer for the namespace is live is the fence plus EXCLUSIVE.

`produce_write_platform` does not read the trust revocation list. `WritePlatformReceipt::recheck` rechecks the receipt's actor, core, and platform. `SettlementSweep::admit` is `admit_ordinary_writer` then `admit_on`, and `admit_on` joins the endpoint, confirms `I/stores/S`, and captures the registry. The sweep module passes empty trust groups into its fenced steps. Its source pin rejects `trust_start`, `TrustInvocation`, `current_trust`, `OperationGuard`, a session, a grant, and an ExecutionId. The custody half therefore performs no trust admission.

`a_view_revoking_the_running_closure_does_not_refuse_the_sweep` publishes an accepted view that revokes the writer's selected release closure, then runs the real receipt recheck and the gate before `admit_on`. The sweep admits, lists the ACTIVE namespace, leases it, and releases the fence. That is the gate's fresh read of I under the revoked view.

For the F18, F19, and F38 ladders the resulting behavior is:

- R3. The sweep is admitted under that revoked view. A crashed attempt (phase `admitted`, neither receipt nor association, lease free) is settled `refused`.
- R4. A later read of that settled row is `terminal-not-committed` (§2.1, the owner's composed case).

Recording that transcription in X9's record is outside this unit. X6 r3 and X9 r2 stay accepted. An X4T fenced trust admission on the sweep would be a new sentence in X1 or X6. While the revocation stood, §4's reconciliation would not run, and every revoked attempt would remain `admitted`.

## What the sweep does

`SettlementSweep` is a new security module (`custody.rs`, exported as `SettlementSweep`, `SweepLease`, and `SweepLeaseRefusal`). Item 12 names storage and host. Item 1's rule that custody owners are security's covers this composition the same way it covers X1's writer, X2d's lease, X2b's registry capture, and X3a's endpoint (call 2). Storage and host consume the type.

**Admission.** One `admit_ordinary_writer` per process. Under the held fence, on the gate's ledger, with the gate's and the receipt's rechecks: `join_store_endpoint` (S, G, K from the gate's one read), `store_root_in` against the endpoint's admitted marker, and `capture_registry`. The list is every N held by exactly one registry row, that row ACTIVE, sorted by `BTreeMap` (call 3). Any other status, a duplicated N, or an installation with no projects contributes nothing. A refusal is its existing row, and dropping the writer releases the fence.

**Lease.** `lease(n)` is one `FenceHolder::fenced` step. An unlisted N is `SweepLeaseRefusal::Row(Invariant)` before that step. `exclusive_lease` confirms `I/host`, `projects`, and N with `required_directory`, opens both carriers, and, inside one `effect_lease` reserve, locks `writer.lease` then `readers.lease`, each `LockMode::Exclusive` through the new `try_lock` (`FileLock::try_acquire`, nonblocking). The bindings and the directories are rechecked before the step returns. `HeldLease::exclusive` stores both locks. Drop releases `readers.lease` and then `writer.lease`.

A held lock is `Ok(None)`. If `readers.lease` is busy, the writer lock is dropped before the return. `lock` is unchanged and still turns a held lock into a refusal for its existing callers (call 4). Busy spends nothing: the gate's ledger is not failed, and the next N still leases. Any other lease-phase refusal is X2 item 8's row through the fenced step, which spends the gate. The host then stops the loop. Later namespaces are not written. `release` still runs, so the fence is last.

`SweepLease` borrows the sweep mutably, so one namespace is leased at a time. `charge_store` scopes a fresh `WorkLedger::new()` at the owner's caps (call 5). Fenced steps stay on the gate's ledger. Storage's snapshot and settles charge the lease's ledger, so a custody refusal of one namespace's ledger file closes that ledger only. X6b call 7 (a refused directory or ledger file closes the charged ledger) holds, and item 8's "continues to the next" holds with it.

**Snapshot and decision.** `sweep_namespace` calls `sweep_from`. `read_sweep_ledger` admits `projects` and N only if present (`existing`, now `pub(super)`), observes the ledger name, and opens it as a judged private file. One charged `ReadSnapshot` must name the same file and hold the selected schema. Inside it, the admitted binding's `admitted` rows (store digest of (N, S, G, K), and N) are listed in ExecutionId order, at most 4096, with `more` taken from a 4097th row when one exists (call 7). Each row's receipt, association, and attempt are read in that snapshot and decided by `join_ledger` (call 8):

| Standing | Decision |
|---|---|
| `UnknownAttemptOpen` | settle `refused` |
| `ContinueCarrier { pending_settlement: true }` | settle `committed` |
| `UnknownCustody`, exactly one of the two rows present | leave `one-sided` |
| `UnknownCustody` otherwise | leave `contradiction` |
| `BindingUnusable` | leave `binding-unusable` |
| any other standing an `admitted` row cannot have | leave `invariant` |

Rows of another binding in the same file are neither listed nor touched. A missing Run material row is not a sweep condition. Settling writes no receipt, association, or object. Nothing re-reads a row to decide (call 10).

**The one write.** `WriteTransaction::settle_admitted_attempt` is the only production `UPDATE attempt_custody`:

`UPDATE attempt_custody SET phase='settled', settled_outcome=?1 WHERE store_generation_digest=?2 AND namespace_id=?3 AND execution_id=?4 AND phase='admitted'`

`?1` is `committed` or `refused`. `Admitted` returns before any SQL. `verify_attempt_definition` runs first. The changed-row count comes back. `ac_monotone` still refuses a second settle. The only caller is `settle_attempt`, once. `recover`, `commit`, `recovery_read`, `project_ledger`, and `project_commit` do not call it. `ledger_store` stays a private module (X8 group I).

`settle_attempt` rechecks the judged file, opens `ExistingWriter` (WAL required, `synchronous=FULL`, `fullfsync`, `checkpoint_fullfsync`), verifies the selected schema, and runs one `BEGIN IMMEDIATE`. One statement, then `COMMIT`. A 0-row result drops the transaction, which rolls it back (`Unchanged`, reason `not-admitted-at-write`), and the sweep continues. One transaction per attempt (call 6): a crash between transactions leaves each row in its pre-state or settled. The sweep writes nothing else, takes no grant, reuses no dead attempt's authority, and does not retry a commit. Orphan objects stay where they are.

**Outcomes with no settle** (call 9). A positively absent `projects`, N, or ledger is `NoLedger`: no attempt conclusion, no write, no row. F24's "never absence" governs a conclusion about an attempt, and this path draws none. A non-database, a drifted schema, a file that is not the judged ledger, malformed rows, or a custody refusal of the directory or the file is `Unreadable`. SQLite busy or locked is `Busy`, skipped and retained, with no row. A short namespace ledger is `Budget`, and the row stays `admitted`.

**Write-time stop** (call 10). The first `Busy`, `Unreadable`, `Undetermined`, or settle-time `Budget` stops that namespace's writes and is reported with its ExecutionId. Later decided attempts are `after-stop`. `Undetermined` is a `COMMIT` error or either injected fault at `settle.commit`. It is never retried. The next sweep's single snapshot shows settled or admitted. The host projects it on the existing `DURABILITY.COMMIT_FAILED` row (`CommitUndetermined`) and continues to the next namespace, which has its own ledger.

## Crash points

X9 r2 item 5's `x6.sweep` row is `after-exclusive`, `after-snapshot`, and `settle.commit` (`fallible`). Who-places assigns these to X6c. All three are present, once, under those names.

- `after-exclusive` is kind `step`. It sits after `FenceHolder::fenced` returns both locks, and before `SweepLease` is handed out. Busy returns before it, with both locks already released (call 12). A kill here holds EXCLUSIVE and has written nothing.
- `after-snapshot` is kind `step`. It sits after `charge_store(read_sweep_ledger)` returns `Ok`, and before `settle_attempt`. `Missing`, `Unreadable` (a custody `ReadRefused` is mapped to `Unreadable` first), `Busy`, and `Snapshot` all pass the point and then return, having written nothing. A `WorkFailure::Budget` from that charge returns `NamespaceSweep::Budget` before the point, because the charge produced no snapshot outcome. That is the same placement as X6b's `after-ledger-snapshot`. A budget refusal inside a later `settle_attempt` is after the point and stops the namespace.
- `settle.commit` is kind `fallible`, wrapped around `transaction.commit()` after the one statement has changed one row. `Unchanged`, `Busy`, and `Unreadable` return before it. `Ok` is `Settled`. `Err` is `Undetermined`, and the function returns. There is no second commit.

The 4096 bound and an injected `COMMIT` failure are not unit-tested here (call 13). Both are X9-3's F53 row, which kills at `x6.sweep.settle.commit.before` and `.after`. The points are placed for that run.

## Host

`maintenance.rs` is the inventory's existing planned row, kept by value (call 11). The build plan names it as `store-gc`'s owner. The file is the settlement step only. The inherited description is broader than the file (store status, purge, backup, recovery, pin impact) and is not contradicted by what the file does. Only `maintenance_tests.rs` is a new row.

`sweep_store` admits once. An admission refusal is `ended`, with an empty namespace list. `run` walks the listed namespaces in order. `sweep_one` leases, calls `sweep_namespace`, and drops the lease before returning. Busy is `Skipped`. A lease row sets `ended` and breaks, so that namespace is the ending row and later namespaces are not entered. `release` runs after the loop. A failed release is host I/O when nothing has already ended the sweep.

Item 8's per-namespace rows, from an exhaustive match:

| Outcome | Row |
|---|---|
| unreadable ledger, or a stopped unreadable settle | `HOST.IO_FAILURE` / `host-io` |
| namespace-ledger budget, before or during a settle | `WORK.BUDGET_EXHAUSTED` |
| stopped `Undetermined` | `DURABILITY.COMMIT_FAILED` |
| skipped, no ledger, SQLite-busy, a clean sweep, a busy stop | none |

An unreadable ledger reports host I/O and the loop continues. One-sided and other left attempts are carried by ExecutionId and reason on `NamespaceSweep`. They add no D9 row. `MIGRATION.CORRUPT` is on no row. `sweep_store` is `pub(crate)`. No command calls it. The command's own D9 outcome and CLI stay with X11 and M5.

`NamespaceSweep` is a public report the host tests construct (call 13, X6b's split). It is not an input to anything that grants. Security tests admission and leases on scratch installations. Storage tests `sweep_from` over stores X3d-2's own steps committed, and reads the result back with `recover_from`. Host tests the loop over a scripted sweep.

## Judgment calls 2–14

2. **Accepted.** The custody half is a security module. Storage and host do not build the fence or the lease.
3. **Accepted.** "Each registered N" is each N held by exactly one row, that row ACTIVE. RESERVED, RETIRED, ABANDONED, and a duplicated N are not swept.
4. **Accepted.** Busy is `try_lock`'s `Ok(None)`, with the writer lock released again when readers are busy. Every other lease-phase refusal spends the gate and ends the sweep. The fence is still released last.
5. **Accepted.** One fresh failure-latching ledger per leased namespace, at the owner's caps. Storage does not charge the gate's ledger or the receipt's ledger.
6. **Accepted.** One `BEGIN IMMEDIATE` transaction per settled attempt. The monotone trigger refuses a second settle.
7. **Accepted.** The snapshot lists only the admitted binding's `admitted` rows, in ExecutionId order, at most 4096, with `more` observed from the next row.
8. **Accepted.** The decision is `join_ledger`'s, split for `UnknownCustody` by whether exactly one of the two rows is present. `BindingUnusable` and an impossible standing write nothing.
9. **Accepted.** Missing, unreadable, and busy are observations. None of them settles. A custody refusal closes only that namespace's ledger.
10. **Accepted.** `Unchanged` continues as `not-admitted-at-write`. `Busy`, `Unreadable`, `Undetermined`, and settle-time `Budget` stop that namespace. `Undetermined` is the existing durability row and is not retried.
11. **Accepted.** The host report is per namespace, with item 8's row only where an existing row fits. `maintenance.rs` stays the planned row by value.
12. **Accepted.** Each fenced step runs the gate's and the receipt's rechecks. `after-exclusive` is reached only when both locks are held. Storage's steps under the lease do not repeat those rechecks; the next lease's fenced step does.
13. **Accepted.** Tests are split by crate. `NamespaceSweep` grants nothing. The two gaps named above belong to X9-3.
14. **Disclosure, for the next description successor.** `namespace_lease.rs` gains `HeldLease::exclusive` and `try_lock`; its "no fence-free lease" sentence stays true, and the description is out of date by omission. `commit_tests.rs` is out of date by omission, as it already was for `recover_tests.rs`. `project_ledger.rs`'s "nothing here settles an attempt" stays true of that file; `sweep_settle` is its own row. `ledger_store.rs`, `recovery_read.rs`, and the four module-declaration files keep descriptions that stay true. These are not findings.

## Inventory v127

Parent v126, 942 files, sha256 `3858f185c78ab74641afeddf92b9063fd5876a84fa0ca4974656f5e45d87c289`, 519279 bytes. Candidate v127, 948 files, sha256 `ba6133904aa9c92a44aafb4ff73cdc9774c8fe853670bce6a4e417403d8a3fb4`, 529197 bytes. Subject manifest sha256 `d523b6311e63e1c4b7185d85418d370605b38712b4ed2ea0e8bcedc982a5d354`, 2146 bytes. Successor record sha256 `bb66ade1b178abf71550db1c1d69a4d28fedbe7b43c849e8dae95a169950ac1c`, 145385 bytes.

The 942 shared rows are equal by value. Nothing was removed. Packages, dependencies, schema version, and pending decisions are equal. The standing sentence is the X6c proposal. The six added rows are `settlement_sweep.rs` (composition), `settlement_sweep_tests.rs` (test), `sweep.rs` (service), `sweep_tests.rs` (test), `ledger_store/sweep_settle.rs` (store), and `host/src/maintenance_tests.rs` (test). Their descriptions match the code above, including G5's narrow reading, the three crash points, the 4096 bound, and the host rows. `maintenance.rs` is unchanged.

The successor's 55-row projection has the same paths, `before` texts, and effective descriptions as v126's projection. Seven rows are identical. Forty-eight differ only in selector, which moves with the inserted rows. No supersession is folded on this parent. `verify_projection.py` against the lock at `f880145`: 55 rows, positive PASS, 278 corruptions refused. `evidence/verify_scratch.py` appends v127 in memory over that lock and passes: 87 inventory successors, 74 contract successors, 55 inheritance rows, v127 selected. The builder was not re-run. It writes its own paths in the architecture tree, and the pinned bytes were compared directly.

## Replay

Private 0700 TMPDIR directories under `$(getconf DARWIN_USER_TEMP_DIR)`, `CARGO_TARGET_DIR` under this review directory, `cargo --locked --offline`, rustc 1.95.0.

- `opensip-security` lib filter `settlement_sweep`: 7 passed. Again with `--features opensip-platform/crash-matrix`: 7 passed. The G5 test is one of the seven.
- `opensip-storage` lib filter `settlement_sweep`: 7 passed, and 7 passed with the same feature. These are `commit::tests::settlement_sweep`, the seven storage tests.
- `opensip-host` lib filter `maintenance::`: 4 passed, and 4 passed with the same feature.
- `cargo fmt --all -- --check` is clean.
- `cargo clippy --locked --offline -p opensip-security -p opensip-storage -p opensip-host --all-targets -- -D warnings` is clean, and the same three crates are clean with `--features opensip-platform/crash-matrix`.

The lead's workspace runs (1678 passed, 0 failed, 3 ignored) and `check_package_edges --lane host` were not re-executed. The package and dependency objects of v127 equal v126, and the scratch verifier accepted the appended successor. The target directory and the private TMPDIRs were removed after the runs.
