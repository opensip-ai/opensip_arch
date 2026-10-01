# Evidence ledger transaction and blob publication — proposal X3c r6
 r2 answers Grok X3c r1 RF-1: the lock order now cites X3b r5's SEAL-path hold. r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok r2 RF-1: release on a SEAL path that stops before COMMIT. r2 bytes are preserved in PROPOSAL-r2.md. r4 answers Grok r3 RF-1: the old rejection now applies only to a path that continues to COMMIT. r3 bytes are preserved in PROPOSAL-r3.md. r5 answers Grok r4 RF-1: the forbidden-substitutes line now matches item 8. r4 bytes are preserved in PROPOSAL-r4.md. r6 answers Grok r5 RF-1: the fresh REV acquisition cites X3b r6 item 6, not this law's item 6. r5 bytes are preserved in PROPOSAL-r5.md. r6 ACCEPTED by Grok on 2026-10-01.
2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X3c of `EXIT-PLAN.md` (DR-G19), under owner.md §7 and §8, security-and-lifecycle S6 (the commit-admission gate) and S7 (lock order and modes), the build plan's "Security/storage ownership and the final commit gate", "Publication sequence and lock discipline" (steps 3, 4 and 6), "Failure and recovery account" and failure cases F02 to F06 and F11 to F15, `commit-recovery-readonly.v3.md` (its D9 standings table, §4 the authorized settlement sweep, §5 the ledger-owned attempt phase), `attempt-custody.schema.v1.json`, the selected physical-layout owner (owner201, product `lifecycle/src/locations.rs`), and laws X1 r1, X2 r5 (`ProjectOperation`, X2e), X3a r5 (`SelectedStoreEndpoint`; no store work in a creator invocation), X3b r4 (the journal, witness, `CarrierFloor`, `JournalAppendLock`) and X4 r4 (`OperationGuard`, the checkpoint under `JournalAppendLock`, `FinalGate` and the single-use `AdmissionPermit`) and X4T r3. Items 1, 2, 3, 5, 6, 8 and 9 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Not code. Library only: no command is wired.

## Problem

M2's commit path publishes immutable evidence objects, then commits one evidence-ledger transaction that carries the Run's receipt and its private recovery association, after the journal `SEAL` (X3b) and the commit gate (X4). At 99f1c35 the parts are present but inert:
- `storage/src/blob_store.rs` publishes and reads one digest-named object in a supplied, retained directory: exclusive new-file publication with its directory barrier, or byte-for-byte confirmation of an existing name. It has no caller, no layout and no budget.
- `storage/src/ledger_store.rs` opens only an **existing** ledger (`SQLITE_OPEN_NOFOLLOW`, `synchronous=FULL`, `fullfsync`, `checkpoint_fullfsync`, `trusted_schema=OFF`), begins `BEGIN IMMEDIATE`, and classifies a failed `COMMIT` as `CommitUndetermined`. It carries the selected DDL for `attempt_custody`, `commit_receipts`/`commit_associations`, `evidence_availability`, `commit_run_material`, `active_run_pins` and `pin_change_facts`, each verified against the stored schema, and the private staging of the receipt/association pair. It never creates a ledger.
- Nothing places the ledger or the objects, admits the attempt row, orders the level-3 acquisitions, or maps failures to public rows.

X3c owns the ledger and object side of steps 3, 4 and 6 up to the prepared commit and its durability classification. X3d's `CommitSession` facade composes it with X3b and X4; X6 owns read-only recovery and the settlement sweep.

## Decisions

1. **Location (lead decision).** For the operation's store S (X3a's endpoint) and namespace N (X2's ACTIVE row):
   - the evidence ledger is `I/stores/S/projects/N/ledger.sqlite`, with its `-wal` and `-shm` beside it, exactly as owner201's `LedgerNames::ledger_relative` already spells it;
   - the content-addressed objects are `I/stores/S/projects/N/objects/sha256/<64 lowercase hex>`, one physical CAS per (S, N). There is no cross-namespace or cross-store deduplication (host-foundation and the blueprint's per-project CAS rule).
   - **Directories.** `projects/`, `projects/N/`, `objects/` and `objects/sha256/` are created or admitted on first need with 465 item 3's create-or-admit rules (exclusive `mkdirat` 0700, raw `EEXIST` alone leads to admission, the zero-rights owner allow, the directory's own barrier and its parent's), under the namespace's writer lease. They are store data, not trust state, so S7's "never under a lease" rule for trust does not apply; the writer lease is what excludes another writer of N.
   - **Rejected:** creating them inside X2e's fence hold. That would add store writes to the trust-ordered handoff for no exclusion it does not already have, and would require an X2 amendment.
2. **Ledger creation (lead decision).** A namespace with no ledger gets one, created under the writer lease, as:
   1. exclusive no-follow create of `ledger.sqlite` (no adoption of an existing name);
   2. one SQLite transaction that runs the selected DDL fragments, in the order the product already pins them (`attempt_custody`, the receipt/association pair, `evidence_availability`, `commit_run_material`, `active_run_pins`, `pin_change_facts`), and sets WAL;
   3. `COMMIT` under `synchronous=FULL` and `fullfsync`, which materializes `-wal`;
   4. the directory barrier of `projects/N/`, so the new names survive;
   5. reopen through the existing `open_existing` path, verifying every table against its DDL.

   **Crash states.** A crash before step 3 leaves a file with no selected schema; a crash after step 3 and before step 4 leaves a schema whose name may not survive. Any open that finds a `ledger.sqlite` whose stored schema is not exactly the selected DDL refuses (`LEDGER.CORRUPT`, item 10); an empty file of length 0 with no `-wal` is the only state treated as "creation not begun" and is completed by the same writer under the same lease. **Rejected:** adopting a schema-less or partial file as empty, and any migration (no other ledger format exists for this product).
3. **Attempt admission before evidence work (lead decision).** Before the first object is written, the writer inserts its `attempt_custody` row (`phase = admitted`, its store generation digest, N, ExecutionId and operationRef) in its own ledger transaction and commits it durably (blueprint: "Admit the `AttemptRecord` transactionally before snapshot work"; readonly-recovery §5). This is the pre-use uniqueness record for a durable-authoritative commit-capable attempt; the `ac_no_replace` trigger refuses a reused ExecutionId. A failed commit here is `durability-undetermined` for the attempt (item 10) and stops it before any object. **Rejected:** inserting the attempt row in the final commit transaction, which would leave a crashed attempt with no `admitted` row for the sweep to settle.
4. **Object publication (step 3).** Each object is a `VerifiedBlob` whose length and SHA-256 are checked against the Run's declared digest before any write. Publication reuses `blob_store`:
   - **New name.** `publish_new_regular` writes a private temporary file under `objects/sha256/`, takes its file barrier (`F_FULLFSYNC`), links it exclusively to the digest name (never replacing), and takes the directory barrier; the receipt's directory barrier is checked against the handle.
   - **Existing name.** Only an exclusive-publication collision whose visibility is unchanged leads to `confirm_existing_regular`, which reads and compares every expected byte and completes its own file and directory barriers. Unequal bytes, a non-regular file or a length mismatch are never overwritten (F04); they refuse as `LEDGER.CORRUPT` (item 10).
   - **Order and atomicity.** All objects of one commit are published, each with both barriers, before any level-3 acquisition (step 4). A failure at any object stops publication; already-published objects stay, unreferenced (F02 to F05).
   - **Orphans.** The attempt never deletes, renames or reuses its own objects after a failure. Unreferenced objects are removed only by the existing reachability GC under `store-gc`'s exclusive lease (readonly-recovery §4.3 step 5). Presence of an object grants nothing (F05).
5. **The two level-3 transactions (step 4, lead decision on ownership).** After the objects, X3c acquires the evidence ledger's `BEGIN IMMEDIATE` with `busy_timeout = 0` only after X3d holds X3b's open journal transaction, never the reverse:
   - grant journal first (X3b), evidence ledger second (X3c), both non-waiting;
   - if the ledger acquisition is busy or fails, X3c returns the failure without holding any ledger transaction, and X3d releases the journal transaction through X3b's consuming abort (F06);
   - neither is acquired while level 4 (`JournalAppendLock`) is held, and level 3 is never reacquired under level 4.

   X3c's handle is a private, owned, single-use `PreparedLedger` wrapping `WriteTransaction`; it has no SQL surface, is not Clone, and its `Drop` attempts only a local rollback. **Rejected:** a waiting ledger acquisition, and a ledger transaction opened before the objects are durable.
6. **Staging and the prepared commit (step 6, lead decision on the adapter boundary).** After X3b's `SEAL` and its `COMMITTED` witness are durable, X3d's staging callback receives X3b's opaque `JournalSealBinding` and hands X3c exactly the joined values. X3c then, in the open `PreparedLedger`, with nothing committed:
   - inserts the exact receipt and the thirteen-field private association through the existing `stage_recovery_pair` (savepoint, poisoned on partial insert, join checked by `join_ledger`);
   - inserts the Run's manifest material (`commit_run_material`), its object references, availability record and authorized pins through their existing private mechanisms, each schema-verified;
   - returns the owned prepared-commit adapter, whose one consuming method performs only `COMMIT`.

   All payload admission, association construction and SQL staging precede X4's `FinalGate::admit`; the adapter's commit runs only with the single-use `AdmissionPermit`. A staging failure aborts the ledger transaction without commit (F11: all required rows or none; a lone `SEAL` is never a commit). **Rejected:** committing inside the staging callback, and storage minting any security type.
7. **Durability of the commit (F12 to F14).** The ledger is WAL with `synchronous=FULL`, `fullfsync=ON` and `checkpoint_fullfsync=ON`, so a `COMMIT` that returns success has passed its WAL barrier; no further barrier is owed for a ledger whose names were barriered at creation (item 2). Outcomes:
   - `COMMIT` returns success: the commit is durable. Only then may X3d produce `PublishedCommit` (F13, F14).
   - `COMMIT` returns an error or the connection is lost: `CommitUndetermined`. The attempt's D9 response is `durability-undetermined` with its ExecutionId (item 10); the attempt never retries, never infers absence and never writes again with its stopped session (F12). The `attempt_custody` row stays `admitted`; read-only recovery (X6) and the authorized sweep decide it.
   - Acknowledgement lost after a durable commit: the receipt is the authority; a fresh read-only lookup (X6) confirms it (F14). Recovery never re-runs the mutation or writes a second receipt (F15).
8. **Locks (lead decision on scope).** Objects and ledger creation run under the namespace writer lease (S7 level 1), never under the fence alone and never with level 3 or 4 held. The ledger write transaction is level 3; the commit happens while X3b's level 4 is still held, as X3b r5 item 5 step 7 requires on the `SEAL` path. The full order is:
   1. the journal transaction (level 3);
   2. the ledger transaction (level 3);
   3. level 4;
   4. `SEAL` and the durable `COMMITTED` witness;
   5. staging;
   6. X4's repeated checkpoint and `AdmissionPermit`;
   7. the ledger `COMMIT`;
   8. release level 4 once the `COMMIT` returns `Committed` or `CommitUndetermined`.

   Level 3 is never acquired or reacquired under level 4. **If the path stops before the evidence `COMMIT`** (a staging failure, a failed repeated checkpoint, no `AdmissionPermit`, an observer latch, or any error after `SEAL`), the order is fixed. Roll back the open ledger transaction, which writes nothing. Release level 4, then each level-3 transaction. Then follow F19: append `REV` through a fresh, lawful level-3-then-level-4 acquisition (X3b r6 item 6). Level 3 is never reacquired under level 4. Every exit from the `SEAL` path releases level 4 exactly once: `Committed`, `CommitUndetermined`, or this failure path. (X3b r6 item 5 step 7). Read-only paths open only `ReadSnapshot` and never take level 3 or 4. **Rejected:** releasing level 4 before the evidence commit on a path that continues to `COMMIT`, which would let a `REV` slip between `SEAL` and commit. A path that stops before `COMMIT` releases level 4 by the stop order above and never commits, so no `REV` can slip in before a commit.
9. **Budget (lead decision).** Every step charges the operation's ledger (X1's attempt ledger, which X4 r4 already uses for checkpoint work), reserving post-effect confirmations before each effect:
   - per object: one object and its edges for the temp file, link, both barriers and any confirmation read, plus its byte length;
   - the attempt-row transaction, the level-3 acquisition and the staged rows: fixed object and edge costs per statement, plus the staged body bytes;
   - ledger and directory creation (items 1 and 2): their create-or-admit costs from 465.

   A commit whose declared objects and staged bytes cannot be reserved refuses on the budget row before the first object is written; it is never truncated. The owner's 256 MiB cap therefore also bounds one commit's new object bytes. **Rejected:** an uncharged blob path, and charging per tick.
10. **Refusal rows (existing details only).** Each failure maps through 468c's `InstallationTermination` (or the D9 standings of readonly-recovery for durability), with no new code:
    - a busy ledger at level 3, or a busy writer lease: `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, `PROJECT.BUSY` (F06);
    - a ledger whose stored schema is not the selected DDL, a partial creation footprint other than item 2's resumable empty file, or an object collision with unequal bytes, length or type: `LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted (readonly-recovery's quarantine row; never `MIGRATION.CORRUPT`);
    - an object, directory or ledger I/O failure before any `COMMIT` was attempted: `HOST.IO_FAILURE`, `host-io`;
    - a failed or uncertain `COMMIT` (items 3 and 7): `DURABILITY.COMMIT_FAILED`, `durability-commit`, ExecutionId retained, `runId` omitted, no retry;
    - a reused ExecutionId refused by `ac_no_replace`: the invariant row (`SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, `HOST.INVARIANT_VIOLATED`), since ExecutionId uniqueness is the host's own pre-use rule;
    - budget: `WORK.BUDGET_EXHAUSTED`.

    Where S12 or the public detail registry fixes a class for a code, it prevails.
11. **The recovery boundary with X6.** X3c writes only: the attempt row, objects, and the one commit. It never reads its own outcome back to decide commitment, never settles `attempt_custody`, never deletes objects and never writes after a failure. Read-only recovery (readonly-recovery steps 0 to 4) and the settlement sweep (§4) are X6's and use only `ReadSnapshot`. A fault-injection hook exists only under `cfg(test)`.
12. **Failure-case coverage.**
    - **Covered by X3c:** F02, F03, F04, F05 (object publication), F06's evidence half (non-waiting level-3 acquisition and orphan preservation), F11 (all rows or none), F12 (undetermined commit, no retry), F13 (no `PublishedCommit` before a confirmed commit), and the write side of F14 and F15 (one commit, no second receipt).
    - **Prepared for others:** F14 and F15's read-side confirmation (X6), F38 to F41 (X4 and X3d's gate), F32 and F34 (X3d).
12a. **Tests while X2e is pending.** Tests in `opensip-storage` use a crate-private, `cfg(test)` location fixture: a scratch installation whose `stores/S` comes from `installation_read_fixture`, with a test N and a held test writer lease. They cover: ledger creation and each creation crash state; attempt admission and a reused ExecutionId; object publication new, confirmed existing, and unequal collision; a crash at each object step (temp write, before file barrier, after link, before directory barrier) via crate-private step hooks; non-waiting level-3 busy; staging all-or-none; commit success; a `COMMIT` error classified as undetermined; budget refusal before the first object; and that no path deletes an object. No production seam or cross-crate bridge exists; the real composition test lands with X3d.
13. **Units after the law.**
    - **X3c-1:** locations for the ledger and objects, directory create-or-admit, ledger creation and its open, and attempt admission. Inventory successor.
    - **X3c-2:** object publication over `blob_store`, the non-waiting level-3 `PreparedLedger`, staging, the prepared-commit adapter and the durability classification. Inventory successor.
    - X3d composes X3b, X3c and X4 into `CommitSession`.

## Forbidden substitutes

Overwriting, renaming or deleting an object after any failure; trusting an existing object name without a full byte comparison; publishing an object before its file barrier, or acquiring level 3 before every object's directory barrier; deduplicating across namespaces or stores; a waiting ledger acquisition; acquiring the ledger before the journal, or either under level 4; committing in the staging callback or without the `AdmissionPermit`; releasing level 4 before the evidence commit on a path that continues to `COMMIT` (the stop order of item 8 is not a substitute); inferring commitment or absence from a failed `COMMIT`, or retrying it; settling `attempt_custody` or reading back the outcome on the write path; adopting a partial or schema-less ledger, or migrating one; a new public code, including for an object collision; an uncharged object or staging step; a production seam that supplies a ledger or object location.

## Not claimed

The `CommitSession` facade, `PublishedCommit` construction and the composition with X3b and X4 (X3d); read-only recovery, settlement and orphan GC (X6); pins' retention policy beyond inserting the rows the Run declares; index stores (M4); carrier or ledger migration; any CLI command; a qualified boot identity on this BASELINE-ATTESTED host.
