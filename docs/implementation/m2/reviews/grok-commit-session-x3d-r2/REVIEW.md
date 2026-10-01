# X3d r2 CommitSession facade

REQUIRED-FINDINGS. r1 RF-1 through RF-5 are closed. Two new findings.

Subject `docs/implementation/m2/commit-session-x3d/PROPOSAL.md` is 21998 bytes, sha256 `5aed58d0be2b6ae6c06f9fbd33427f950facf1783cb98973cae851e77e733247`, matching hashes.txt. Preserved `PROPOSAL-r1.md` is 17916 bytes, sha256 `78ede338085d59e50b6bd2a3c519b1b8d8f882320e001ed8061431f4b8d1099a`, the reviewed r1. Live product HEAD is `5b5f04cf3132d4aa91ced618d4b40544f2aaf2f5`. Real `~/Library/Application Support/OpenSIP` is absent. No product cargo.

The diff is the r2 header and the five answer sites: the capacity predicate, the attempt-admission outcomes, the publish stop order, the end-path reserve, and the item 9 rows.

## r1 findings

**RF-1 is closed.** Step 3 returns `CarrierCapacityExhausted { grantGeneration, provenTailSeq }` when the proven tail is greater than or equal to `9007199254740990`, before the attempt transaction and before any object. The terminal slot stays `9007199254740991`. Storage does not call lifecycle. X7 completes cleanup, releases the lease, and routes rollover under the fence.

**RF-2 is closed.** Steps 0 to 3 take no level-3 lock. Step 4 is the attempt transaction, and it stops before any object. The no-replace trigger returns `ExistingAttempt`. A `COMMIT` that errors or loses the connection returns `CommitUndetermined` on the durability row, ExecutionId retained, no RunId, no retry. Busy, or I/O before that `COMMIT`, takes the busy or host I/O row.

**RF-3 is closed for the append.** Inside `publish`, a certain refusal after level 4 and before the evidence `COMMIT` rolls back the open ledger transaction, releases level 4, then each open level-3 transaction, and appends nothing. `finish` is the only `REV` and `CLN` owner: one fresh level-3-then-level-4 acquisition while the lease is held, when a durable SEAL has no evidence commit, the gate is latched (observer or a checkpoint that fetch-ORed 2), or a revocation was observed, and `CLN` when residue must be recorded, including F38's pair. An uncertain journal commit or barrier returns `CommitUndetermined` and appends nothing, in `publish` and in `finish`. A returned evidence `COMMIT`, `Committed` or `CommitUndetermined`, releases level 4 once. The floor copy after that uncertain outcome is RF-2 below.

**RF-4 is closed for a reserve that succeeds.** Step 0 reserves one `REV` and one `CLN` before any later check, as their own reserve, kept when the publication reserve fails. `finish` spends that reserve. A failed step-0 reserve is RF-1 below.

**RF-5 is closed.** The rows match the public detail registry and `diagnostic-routes.json`. Host I/O is operational-failed, exit 4, `HOST.IO_FAILURE`, `host-io`. `MIGRATION.CORRUPT` is the domain detail only for a carrierFormat 3 footprint that is not a lawful durable prefix. Ledger schema mismatch, a partial creation footprint, and an unequal object stay `LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted. Other journal quarantines stay on X3b r6 item 8, including F46 as host I/O. The invariant row, including `ExistingAttempt` before X6, is operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `HOST.INVARIANT_VIOLATED`. Budget is operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `WORK.BUDGET_EXHAUSTED`. Busy stays `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, `PROJECT.BUSY`. `CommitUndetermined` stays `DURABILITY.COMMIT_FAILED`, `durability-commit`.

## RF-1

Step 0 says a reserve that cannot be taken refuses on the budget row and that no `StoppedSession` then owes an append. The closing sentence of item 3 says a refusal at any step returns a `StoppedSession` which still holds the end-path reserve. Item 6 says every outcome is finished. Item 7 appends one `REV` when the gate is latched, and the observer may already have latched at the lease-free point, which is why the reserve is first. The only append exception in item 7 is an uncertain journal commit or barrier. A failed reserve with a latched gate therefore still owes the `REV`, and the session does not hold the reserve that would fund it.

Required: a failed step-0 reserve is the budget row, and `finish` appends neither `REV` nor `CLN`. The reserve-holding sentence applies to a refusal after the reserve was taken. A latched gate with no reserve releases and runs the end step, and appends nothing.

## RF-2

Item 4's uncertain bullet and item 7 both leave reconciliation to the next opener, and item 7 still runs X3b item 4's end step on every finish. That end step reads a committed tail and copies the floor forward when the tail is higher. X3b r6 item 5's uncertain-outcome rule is that this writer refuses every further effect, reconciles by reopening the carrier and running item 4's `reconcile_witness`, and assumes neither state. A `QUARANTINE` outcome leaves the floor untouched. A floor copy from an unreconciled read can record a tail the witness does not confirm. Lock release on the uncertain path stays: roll back the open ledger transaction, which writes nothing, and release level 4 once.

Required: after an uncertain journal commit or barrier, `finish` appends nothing. While the lease is still held, this writer reopens the carrier and runs `reconcile_witness`. The floor copy runs only after that reconciliation returns OK, REVERT, or ADVANCE. A QUARANTINE outcome leaves the floor untouched.
