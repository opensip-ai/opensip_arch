# Review: read premise 458c r4

Grok is the single reviewer. Claude Opus 5.5 leads. Law re-review of the read side's omission premise and the observation path. No repository edits and no product cargo.

Subject `docs/implementation/m2/read-premise-458c/PROPOSAL.md`, 16488 bytes, sha256 `9eb8b6e81e88fc48af9568b9f56b0f1ef874cb901d286b1efbc99d45c2fdbcef`. `PROPOSAL-r3.md` preserves the r3 bytes, 15931 bytes, sha256 `efb97a4ddae88cfac90c14e369f54c064c5aa9ea4b71fac26fd3287d00f214e2`. The diff is the header, the item 5 home bullet, and the item 11 `Err` bullet. Product HEAD is `7237f931ae78330243edc4de1e7d64daf1b50fd2`.

## Verdict

**REQUIRED-FINDINGS.**

The fence-wait errors match `lock_fence` and 468c. A permission failure and an unqualified filesystem match the write gate's published rows. A missing H is still the custody row, and 468c publishes host I/O for that open.

## What holds

The r3 fence finding is closed. Every `FileLock::try_acquire` `Err` stops the wait and ends on `HOST.IO_FAILURE`, fault cause `host-io`, exit 4. That includes a carrier that is no longer a regular file and a descriptor that is not close-on-exec. `lock_fence` maps each of those to `IoFailure::Lock`, and 468c maps `IoFailure::Lock` to `HostIo`. Only a lock still busy at 5 s or at 201 attempts uses `LEDGER.BUSY_TIMEOUT`, `PROJECT.BUSY`, `ledger-busy`. After the lock is held, `fence_matches` treats a replaced carrier (device, inode, link count, file type, or name) as `CustodyRefusal::FenceChanged`, which 468c publishes as `CONFIG.CUSTODY_REFUSED`, subject `fence-changed`. That is the step 2 recheck.

The permission and filesystem cells of the r3 home finding are closed. An open `missing()` does not accept, including `EACCES`, is `GateRefusal::Io`, and 468c publishes `HOST.IO_FAILURE`, exit 4. An opened H that `is_home_filesystem` refuses is `GateRefusal::Filesystem(Entry::Home)`, and 468c publishes request-rejected exit 2, `EXTENSION.ADMISSION_REJECTED`, `NT-TCB-BOOT`, subject `INSTALL_ROOT_FS`. None of these is absence or `INSTALLATION.ACCOUNT_REFUSED`.

The r1 recheck, the partial doctor report, the 201-attempt reservation, and positive absence of the first missing fixed-suffix component stand.

## Required findings

### RF-1 — A missing H is still the custody row

`observe_parent` opens H with `RetainedDirectoryPath::open_accounted` and reports failure as `ParentRefusal::Open`. The gate's `chain_refusal` records that open as `GateRefusal::Custody(Chain(Open))` when `missing()` matches: `NotFound`, `InvalidInput`, `ENOTDIR`, or `ELOOP`. `gate_refusal` then sends `Custody(Chain(chain))` through the routing `chain_refusal`. That function maps every `ParentRefusal::Open` to `HostIo`: operational-failed exit 4, `HOST.IO_FAILURE`, fault cause `host-io`, and no custody subject.

Item 5 says every H failure takes the row 468b classifies and 468c maps, and then says a missing H takes the custody row. The custody row is request-rejected exit 2, `CONFIG.INVALID`, `CONFIG.CUSTODY_REFUSED`, with a subject. 468c has no subject for this open and publishes the host I/O row. A symlink or a non-directory at H is the same `missing()` arm and the same published row.

Failure scenario: the account record names `/Users/name`, `InitialActor` admitted that spelling, and the directory is absent. `observe_parent` returns `ParentRefusal::Open(NotFound)`. The gate records `GateRefusal::Custody`. Item 5 ends on `CONFIG.CUSTODY_REFUSED`. `gate_refusal` at `7237f93` ends on `HOST.IO_FAILURE`, exit 4.

## Not reopened

The receipt, the 465 item 4 scope, the full recheck set, the partial doctor report, the fence-wait I/O row, the permission row, and the install-filesystem row stand. The finding is the published row for a missing H.
