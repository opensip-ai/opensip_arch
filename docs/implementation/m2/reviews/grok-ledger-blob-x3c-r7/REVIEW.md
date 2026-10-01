# X3c r7 ledger creation WAL

ACCEPT. Nothing new is wrong.

Subject `docs/implementation/m2/ledger-blob-x3c/PROPOSAL.md` is 18855 bytes, sha256 `b95853727f0e73c03231953645ff59bd231dc1edf73eecdefc4a7c7ff36b0622`, matching hashes.txt. Preserved r6 is `PROPOSAL-r6.md`, 18392 bytes, sha256 `15f8f9845595c274daae4e7447cb87435784ce7129f057300207b168422ccb8e`, the accepted r6 subject. The diff is the r7 header and item 2 step 2. Live product HEAD is `5b5f04cf3132d4aa91ced618d4b40544f2aaf2f5`. Real `~/Library/Application Support/OpenSIP` is absent. No product cargo.

Step 2 still runs the pinned DDL in one transaction. WAL is selected immediately before that transaction, because SQLite refuses a journal-mode change inside one. A crash in that gap leaves a non-empty file whose stored schema is not the selected DDL. Item 2 resumes creation only for a length-0 file with no `-wal`, and item 10 classifies every other partial creation footprint as `LEDGER.CORRUPT`, `ledger-corrupt`, with `domainDetail` omitted. The amendment names that existing row. It adds no code.

A host probe of SQLite 3.54.0 matches the footprint: `PRAGMA journal_mode=WAL` on a zero-length file, outside a transaction, returns `wal` and leaves a 4096-byte database, write version WAL, an empty `sqlite_master`, and no `-wal` yet. The following DDL commit is what creates `-wal`, so step 3's "COMMIT materializes `-wal`" still holds. The same pragma inside a transaction leaves the mode `delete`. The length-0 resume rule does not include this file, and the forbidden substitute that adopts a schema-less ledger stays rejected.

The durability claim in item 7, the creation charge in item 9, and the lock order in item 8 are unchanged. Creation remains under the writer lease. The WAL pragma is not a second level-3 transaction.
