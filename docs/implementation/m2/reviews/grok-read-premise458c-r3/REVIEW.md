# Review: read premise 458c r3

Grok is the single reviewer. Claude Opus 5.5 leads. Law re-review of the read side's omission premise and the observation path. No repository edits and no product cargo.

Subject `docs/implementation/m2/read-premise-458c/PROPOSAL.md`, 15931 bytes, sha256 `efb97a4ddae88cfac90c14e369f54c064c5aa9ea4b71fac26fd3287d00f214e2`. `PROPOSAL-r2.md` preserves the r2 bytes, 15247 bytes, sha256 `5660fc33e811ebbed59ebf47cbba5d79cfed44663aa573cb0106f486dfd71ebc`. The diff is the header, the item 5 home bullet, and the item 11 reservation and outcome bullets.

## Verdict

**REQUIRED-FINDINGS.**

The actor-row cell and the busy-row collapse are closed. The replacement home sentence puts three write-gate outcomes on one custody row. The fence-wait sentence puts a non-regular carrier on the custody row.

## What holds

The r2 actor-row cell is closed. Item 5 cites owner §3. H is never absence and never `INSTALLATION.ACCOUNT_REFUSED`. `InitialActor` admits the UIDs and the home spelling, not the directory.

The r2 busy collapse is closed for an I/O error and for a lock that stays busy. Each attempt has the three `FileLock::try_acquire` results. The lock continues. Busy `None` waits and retries. `Err` stops at once. An I/O error ends on `HOST.IO_FAILURE`, fault cause `host-io`. Only a lock still busy at 5 s or at 201 attempts ends on `LEDGER.BUSY_TIMEOUT`, `PROJECT.BUSY`, `ledger-busy`. The reservation says the wait never ends in `WORK.BUDGET_EXHAUSTED`. The write gate stays one attempt.

The r1 recheck, the partial doctor report, the 201-attempt reservation, and positive absence of the first missing fixed-suffix component stand as accepted in r2.

## Required findings

### RF-1 — Missing, inaccessible, and unsupported H share one custody row

Owner §3 refuses a missing, inaccessible, or unsupported H before any mkdir. 468 item 6 and the write gate publish different rows for those three outcomes.

`observe_parent` opens H with `RetainedDirectoryPath::open_accounted`. The gate's `chain_refusal` records `ParentRefusal::Open` as `GateRefusal::Custody` only when `missing()` matches: `NotFound`, `InvalidInput`, `ENOTDIR`, or `ELOOP`. Every other open error becomes `GateRefusal::Io`. `gate_refusal` then sends `Custody(Chain(chain))` and `Io(Chain(chain))` through the routing `chain_refusal`, and that function maps every `ParentRefusal::Open` to `HostIo`. The published row is operational-failed exit 4, `HOST.IO_FAILURE`, fault cause `host-io`. That mapper emits no custody subject for an open.

After H is open, `filesystem()` samples it. A sample `is_home_filesystem` refuses becomes `GateRefusal::Filesystem(Entry::Home)`. 468c maps that to `InstallRootFilesystem`. Item 6's row is request-rejected exit 2, `EXTENSION.ADMISSION_REJECTED`, `NT-TCB-BOOT`, subject `INSTALL_ROOT_FS`. A failed sample is `Io(Filesystem)`, which publishes the host I/O row.

Item 5 sends a missing, inaccessible, or unsupported H to the custody row, `CONFIG.CUSTODY_REFUSED`, with the walk's sub-detail as subject, and says the write gate does that. The public mapper has no open subject. An unsupported home is the install-filesystem row. An inaccessible open is the host I/O row.

Failure scenario: H exists, the open succeeds, and `is_home_filesystem` refuses the sample. Item 5 ends on `CONFIG.CUSTODY_REFUSED` with a walk sub-detail. The write gate and 468 item 6 end on `NT-TCB-BOOT`, subject `INSTALL_ROOT_FS`. The same sentence sends an open that returns `EACCES` to that custody row. `missing()` does not treat `EACCES` as a missing open, and the write gate publishes `HOST.IO_FAILURE`, exit 4.

### RF-2 — A fence carrier that is no longer a regular file takes the custody row

`FileLock::try_acquire` returns `Err` when the carrier is not a regular file, when the descriptor is not close-on-exec, and when `flock` fails for a reason other than busy. The write gate's `lock_fence` maps every one of those errors to `GateRefusal::Io(IoFailure::Lock)`. 468c maps `IoFailure::Lock` to `HostIo`: operational-failed exit 4, `HOST.IO_FAILURE`, fault cause `host-io`.

Item 11 sends the non-regular carrier to the custody row. That row is request-rejected exit 2, `CONFIG.CUSTODY_REFUSED`. The close-on-exec `Err` is the same `lock_fence` path, and item 11 names no row for it. Both are `try_acquire` errors, and the write gate publishes the host I/O row for every such error. The identity recheck that can end on custody runs only after the lock is held.

Failure scenario: during the wait, metadata on the retained fence descriptor reports that it is no longer a regular file. `try_acquire` returns `Err`. Item 11 ends on the custody row, exit 2. `lock_fence` ends on `HOST.IO_FAILURE`, exit 4.

## Not reopened

The receipt, the 465 item 4 scope, the full recheck set, the partial doctor report, the 25 ms pace, the 201-attempt reservation, and positive absence of the first missing suffix component stand. The findings are the home row and the non-regular fence carrier.
