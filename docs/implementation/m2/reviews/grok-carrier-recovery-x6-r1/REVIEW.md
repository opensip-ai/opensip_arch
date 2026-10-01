# Law X6 r1 — read-only carrier recovery and the settlement sweep

Law review only. No product cargo. The OpenSIP support directory is absent. `PROPOSAL.md` is 15035 bytes, sha256 `2c26332929bffac38cd19cb2faa227f0ecb136351d6cc43b006053fbce6201bd`, matching `hashes.txt`. Live product HEAD is `8452ab962ad42a5a17e4b4755188943874725423`. The proposal names `7e676a9`. `recovery.rs` and `ledger_store.rs` are unchanged between those commits. `attempt_custody.phase` and `settled_outcome` are the ledger columns, and `settled_outcome` is `committed` or `refused`.

## Item 7

The sweep's single write is sound. §4.2 permits only `committed` or `refused`, and only for a free exclusive lease with a readable, two-sided snapshot. Busy, unreadable, one-sided and already-settled namespaces write nothing. The statement is one `admitted → settled` update, which is the transition the monotone trigger allows. `BEGIN IMMEDIATE` with WAL, FULL and `fullfsync` is the evidence ledger's existing writer transaction.

The lock scope matches X2 r5 item 7 and §4.1. `admit_ordinary_writer` holds the installation fence. Each namespace then takes `writer.lease` and `readers.lease`, both `LOCK_EX|LOCK_NB`, and a busy namespace is skipped. Leases release in reverse order and the fence is last. Orphan removal stays out: §4.3 step 5 permits the existing reachability GC, and that GC is not in the product.

## Item 3

Identity §5, owner §5 and `commit-recovery-readonly.v3.md` §2 require this selector to take `SHARED-READ` and prohibit the install fence. Item 3 follows that: 458c step 0, no step 1, then `readers.lease` `LOCK_SH|LOCK_NB`, with a change on recheck returning `UnavailableBusy`.

Accepted X2 r5 item 7 says there is no lease without the fence, and its forbidden list repeats that, with no recovery exception. Item 3 does not amend that sentence. The exception is the behavior the recovery owner requires, and it becomes lawful only when X2 records it. That is RF-1.

## Rows and coverage

F14, F15, F20–F25, F27–F29, F33, F34, F36, F37, F43–F46, F49, F52 and F53 are the read-side and sweep cases. F35 and F47, F48, F50 and F51 stay outside M2, and F46 remains the read-only `UnknownCarrierIncompatible` classification. `MIGRATION.CORRUPT` stays off every read-only path. Quarantine keeps `LEDGER.CORRUPT` / `ledger-corrupt` with no detail. Binding refusal is request-rejected / `EXTENSION.ADMISSION_REJECTED` / `RECOVERY.REFUSED`. The budget caps are 458c's. X3d's writer still never settles.

Item 8's degraded row drops half of the §1 projection. That is RF-2.

## Verdict

REQUIRED-FINDINGS. RF-1, RF-2.
