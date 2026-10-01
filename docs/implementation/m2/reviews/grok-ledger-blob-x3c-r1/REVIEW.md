# Review: evidence ledger and blob publication X3c r1

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/ledger-blob-x3c/PROPOSAL.md` is 16555 bytes, sha256 `b15f15d91fb293b9491808e093d71e9e6eb041a9ec255602f0f5781a6ba642e1`, matching hashes.txt. The live product HEAD is `99f1c35b50ddd7a3a2724d9acadf9c72f27ce7da`, the same commit the request names. The real OpenSIP support directory is absent. No product cargo.

## Required finding

### RF-1 — The evidence commit's lock hold contradicts X3b's release

Item 8 commits the evidence ledger while level 4 is still held, and forbids releasing that lock before the commit. It attributes the hold to X3b item 6, in the words "the append lock stays held through the witness and evidence commit". X3b r4 item 6 does not say that. X3b r4 item 5 step 7 releases level 4 once the `COMMITTED` witness is durable, and by then the journal transaction is already closed. That release is before X3c stages rows and before `COMMIT`.

X4 r4 item 3 repeats the checkpoint, which requires a level-4 borrow, after the `SEAL`, the witness, and association staging, and before evidence-commit admission. The build plan holds the journal lock through the ledger commit. Those two rules agree with item 8's own hold. They do not agree with X3b step 7. As the three laws stand, a `SEAL` either releases level 4 before the evidence commit, which lets a `REV` slip between them, or it keeps the lock and violates X3b step 7.

Required: on the `SEAL` path, X3b item 5 step 7's release waits until the evidence `COMMIT` has returned, whether the return is success or `CommitUndetermined`. The order is journal transaction, then ledger transaction, then level 4, then the `SEAL` and its `COMMITTED` witness, then staging, then X4's repeated checkpoint and `AdmissionPermit`, then the ledger `COMMIT`, then the release. Level 3 is not acquired or reacquired under level 4.

## Locations

`LedgerNames::ledger_relative` is `stores/S/projects/N/ledger.sqlite`, with `-wal` and `-shm` beside it. Item 1 uses that spelling. The object path `objects/sha256/<64 lowercase hex>` is not in `locations.rs`.

`locations.rs` spells the witness as `host/projects/N/grant-journal.witness` and the floor as `trust/journal-floors/N/<generation>.floor`. X3b r4 spells `host/projects/N/grant-journal.witness.json` and `trust/carrier-floors/N.v1`. X3c does not open either file. Item 6 takes X3b's opaque `JournalSealBinding` after X3b has made the `COMMITTED` witness durable. X3c-1's locations are the ledger names and the new object path.

## What matches

The ledger is store data under the writer lease, created on first need with 465's create-or-admit rules, not inside X2e's handoff. Creation is an exclusive file, one DDL transaction in the product's table order, a full-sync commit, the directory barrier, and a schema-verifying reopen. A length-0 file with no `-wal` is the only resumable footprint. Any other schema mismatch is `LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted, and is never `MIGRATION.CORRUPT`.

The `attempt_custody` row is committed before the first object. Objects reuse `blob_store`: temporary file, `F_FULLFSYNC`, exclusive link, directory barrier; an existing name is confirmed byte for byte and is never overwritten. Every object's directory barrier precedes the step-4 level-3 pair. Orphans stay. `store-gc` is the only remover. Journal then ledger, both `busy_timeout = 0`. A busy ledger or a busy writer lease is `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, `PROJECT.BUSY`. The prepared ledger is private and single-use. Staging is all rows or none, after the durable `SEAL` and witness, and `COMMIT` runs only with the single-use `AdmissionPermit`.

A `COMMIT` that returns success is durable, and only then may X3d produce `PublishedCommit`. An error or a lost connection is `CommitUndetermined`: `DURABILITY.COMMIT_FAILED`, `durability-commit`, operational-failed, exit 4, ExecutionId retained, `runId` omitted, no retry, and the custody row stays `admitted`. That is the readonly-recovery projection and F40. I/O before any `COMMIT` is `HOST.IO_FAILURE`, `host-io`. A reused ExecutionId at `ac_no_replace` is the invariant row; F34's route to read-only recovery stays with X3d. Budget is `WORK.BUDGET_EXHAUSTED` on X1's attempt ledger, reserved before the first object, and a commit is never truncated. The 256 MiB owner cap bounds that reservation. X3c writes the attempt row, the objects, and the one commit, and does not settle or read its outcome back.
