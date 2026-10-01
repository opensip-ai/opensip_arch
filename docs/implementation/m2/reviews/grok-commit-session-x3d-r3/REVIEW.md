# X3d r3 CommitSession facade

ACCEPT. r2 RF-1 and RF-2 are closed.

Subject `docs/implementation/m2/commit-session-x3d/PROPOSAL.md` is 23334 bytes, sha256 `2524b77adc123c1804b7794a84de58a2290afe719646f36d90f2068c2b4a8d5b`, matching hashes.txt. Preserved `PROPOSAL-r2.md` is 21998 bytes, sha256 `5aed58d0be2b6ae6c06f9fbd33427f950facf1783cb98973cae851e77e733247`, the reviewed r2. Preserved `PROPOSAL-r1.md` is 17916 bytes, sha256 `78ede338085d59e50b6bd2a3c519b1b8d8f882320e001ed8061431f4b8d1099a`, the reviewed r1. Live product HEAD is `7e676a93567bfb5030e01cc11b56de6831f8d19c`. That commit adds the journal floor and carrier on `5b5f04cf3132d4aa91ced618d4b40544f2aaf2f5`, which the proposal's product paragraph still names. `CommitSession` and the facade types are still absent. Real `~/Library/Application Support/OpenSIP` is absent. No product cargo.

The diff is the r3 header, the failed-reserve finish rule, the item 3 reserve sentence, and the uncertain-outcome reconciliation.

## r2 findings

**RF-1 is closed.** A step-0 reserve that cannot be taken refuses on the budget row and returns a `StoppedSession` that holds no end-path reserve. Its `finish` appends neither `REV` nor `CLN`, including when the gate is already latched, releases the lease, and runs the end step. An unfunded append is never attempted. Item 3's closing sentence now keeps the reserve only for a refusal after step 0 succeeded. Item 7 still funds a `REV` or `CLN` from that reserve, so a session that holds none has nothing to spend.

**RF-2 is closed.** After an uncertain journal commit or barrier, `publish` appends nothing, rolls back the open ledger transaction, releases level 4 once, and returns `CommitUndetermined`. `finish` appends nothing. While the lease is still held, this writer reopens the carrier and runs `reconcile_witness`. The floor copy runs only after that reconciliation returns `OK`, `REVERT`, or `ADVANCE`, and it copies only the reconciled tail. A `QUARANTINE` outcome, and a reconciliation that itself fails, leave the floor untouched. A failed reconciliation leaves the next opener to reconcile.

## Reconciliation and X3b r6 item 5

Reconciling inside this writer is what X3b r6 item 5 requires. After a failure past visibility, that item says this writer refuses every further effect, reconciles by reopening the carrier and running item 4's reconciliation, and assumes neither state. Item 4 runs that reconciliation under the fence and the lease, and only an `APPEND-WRITE` or `EXCLUSIVE` holder reconciles. `REVERT`, `ADVANCE`, and `INIT` write only the witness. The carrier start writes no floor. The end step releases the lease before the floor copy, and a floor write while a project lock is held is forbidden.

r3 does that split. Step 1 reconciles before the release, which is the lead decision, so this writer is still the authorized holder. Step 2 releases the lease. Step 3 runs the end step under the fence with no project lock, and the copy is gated on `OK`, `REVERT`, or `ADVANCE` of the reconciled tail. `QUARANTINE` leaves the witness and the floor as item 8 leaves them: untouched, with nothing stored. The witness write is the one item 4 already attaches to `reconcile_witness`. `publish` and `finish` still append no journal record on this path, and the end step's other publication effects stay off.

Item 9 is unchanged, so the r2 row check stands.
