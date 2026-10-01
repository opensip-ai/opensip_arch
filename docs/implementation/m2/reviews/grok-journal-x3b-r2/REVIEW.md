# Review: grant journal X3b r2

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/journal-x3b/PROPOSAL.md` is 21949 bytes, sha256 `cb14fe66734aa913fe207543cdf3ad890255ed130b7feb9b85d2557fd5e1e78c`, matching hashes.txt. `PROPOSAL-r1.md` is the r1 subject: 14951 bytes, sha256 `3e85290e52025f4d2f2c46d489c3cde522b8c866af0ed773d9ba4fa283ab38cb`. Product HEAD is `f7acb6d7f8acadcbc0bf81d141f39077d817f043`. The real OpenSIP support directory is absent. No product cargo.

## r1

RF-1 is closed. The floor step runs under the fence before X2d takes the lease. It probes `writer.lease` with `LOCK_EX|LOCK_NB` and releases that lock before any floor write. A busy probe writes nothing. A successful probe plus the held fence excludes another writer until the fence is released, which is S7's rule that a lease requires the fence. The end step releases the operation lease, retakes the fence with the bounded wait, and probes again. A busy end probe skips the copy and releases the fence. A successful end probe reads the tail, releases the probe, and only then writes, with no project lock held. The floor is written only when the observed tail is higher. The end path still reuses the write receipt and takes no second gate. That retake remains consistent with owner §5.

RF-2 is closed. Registry owner v2 has no projectKey. `namespaceId` is the canonical lowercase UUIDv4 text. The preimage is that text as UTF-8, with no prefix, separator, or terminator. The product open compares `carrier_format.project_key_digest` and the witness digest with the lowercase hex of `SHA-256` of the `project_key` argument's bytes (`journal_store.rs`). Passing that N text as `project_key` leaves the comparison unchanged. The stored member is that hex text: the carrier check requires 64 lowercase hex characters, and the witness and floor decoders accept the same hex. `grantGeneration` and the genesis preimage keep using the same N string.

RF-4's original case is closed. The floor is published at `{lastSeq 0}` before any carrier or witness. Floor absent with no carrier and no witness is INIT. Floor absent with a carrier or witness is `floorLost`. Creation no longer leaves a COMMITTED 0 witness in front of a missing floor.

RF-3 is not closed. Item 8 states the right rows, and the floor-step table reaches a different row first. See the finding below.

## What holds

The N-bound binding stays in X2e's handoff. The carrier, witness, and floor paths match the selected format-3 carrier and the `CarrierFloor` / `Witness` shapes. `tailSha256` and `bodySha256` are null only at sequence 0, which is what `observed_body` accepts. Reconciliation stays the §5.4 table, and a read-only path does not apply REVERT, ADVANCE, or INIT. The append order, the exclusive temporary witness, `JournalAppendLock` after the journal transaction, and the checkpoint borrow match X4 r2. Observers do not take the lock.

X3b's own order is the right cross-law correction: the floor step is before X2d's lease, and the carrier start is inside X2e's handoff before the fence release. X2's current item 7a still places both steps inside that handoff; this law leaves the recording to X2's revision. The closed floor records no trust epoch. That matches the comparison X4T already states against SC-TRUST's own floors.

## Required findings

### RF-1 — A non-format-3 file with no floor is floorLost

Item 8 matches S12 and carrier-format.v3 §8.1. The writer stores no quarantine marker and does not trust a stored one. `MIGRATION.CORRUPT` is only a format-3 footprint that is not a lawful prefix, or a violated generation boundary. A complete format-1 or format-2 carrier is F46: operational-failed, exit 4, `HOST.IO_FAILURE`, `host-io`, `domainDetail` omitted. A partial format-3 set is the migration row.

The floor step runs first, in table order. Floor absent and anything other than "no carrier and no witness" is `floorLost`: `LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted. A planted format-1 database, and a partial format-3 object set, are that "anything else." Item 8 is not reached.

Failure scenario: the namespace contains a complete format-1 `grant-journal.sqlite` and no floor. The table reports `floorLost`. The public row is journal corruption with no detail. F46's `HOST.IO_FAILURE` never runs. The same open reports a partial format-3 set as `floorLost` instead of `MIGRATION.CORRUPT`.

Format dispatch happens before the floor table. A complete format-1 or format-2 carrier is the F46 row whether or not a floor is present. A partial format-3 set is `MIGRATION.CORRUPT`. `floorLost` remains a format-3 carrier or a witness whose floor is positively gone.

### RF-2 — The floor table does not implement the crash list

The crash list says a complete carrier whose journal holds a record and whose witness is absent is `witnesslessRestore`, and that a quarantine leaves the floor untouched. §5.4 gives the same witnessless row, plus `witnessMalformed` and the other reconcile quarantines. `reconcile_witness` does not consult the floor, so the floor step has to refuse those states before it copies.

The fourth row is checked before the compare row. Its condition is written as "no carrier, witness present, or lastSeq > 0" against any present floor. The compare row then copies a present carrier's tail up whenever the tail is higher, and it does not read the witness. The INIT cell names `{lastSeq 0, tailSha256 null}` and not the rest of `CarrierFloor`. The decoder rejects a floor that omits `grantGeneration` or `projectKeyDigest`.

Failure scenario: the first operation commits a record and publishes a floor with `lastSeq` above 0. The next start matches the fourth row and quarantines `uncertainTailLoss` without comparing the healthy carrier and witness. If that row is implemented as the absent-carrier case only, a carrier with records and no witness takes the compare row instead. The floor moves up to that tail, reconcile then quarantines `witnesslessRestore`, and the high-water stays on the unwitnessed tail because it never moves down.

The absent-carrier quarantine is only a present floor, no carrier, and a present witness or `lastSeq` above 0. A present carrier is dispatched by format first and then by witness reconciliation. `witnesslessRestore`, `witnessMalformed`, and the other reconcile quarantines leave the floor where it was. The floor is copied forward only after reconciliation returns OK, REVERT, or ADVANCE, and only when the committed tail is higher. The INIT floor is a whole `CarrierFloor`: `highWaterSchema` 1, `projectKeyDigest` the lowercase hex of `SHA-256(N)`, `grantGeneration` 1, `lastSeq` 0, `tailSha256` null.
