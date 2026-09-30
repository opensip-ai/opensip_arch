# Review: read premise 458c r5

Grok is the single reviewer. Claude Opus 5.5 leads. Law re-review of the read side's omission premise and the observation path. No repository edits and no product cargo.

Subject `docs/implementation/m2/read-premise-458c/PROPOSAL.md`, 16734 bytes, sha256 `06838b0d131cbe9179daec36a9e27d4b9a8e3f106a6108caaf962b1cc6512849`. `PROPOSAL-r4.md` preserves the r4 bytes, 16488 bytes, sha256 `9eb8b6e81e88fc48af9568b9f56b0f1ef874cb901d286b1efbc99d45c2fdbcef`. The diff is the header and the item 5 home bullet. Product HEAD is `7237f931ae78330243edc4de1e7d64daf1b50fd2`.

## Verdict

**ACCEPT.**

RF-1 is closed. The other public rows this law states match 468c's mapping at that commit.

## What holds

A missing H is no longer the custody row. Item 5 sends every H failure to the row `gate_refusal` gives the same step 0 refusal. At `7237f93` the two reference lines match that function. `observe_parent` reports a failed open of H as `ParentRefusal::Open`, including `NotFound`, `InvalidInput`, `ENOTDIR`, and `ELOOP`. The gate may record `missing()` as `GateRefusal::Custody(Chain(Open))` first. `gate_refusal` then maps every `ParentRefusal::Open` to `HostIo`: operational-failed exit 4, `HOST.IO_FAILURE`, fault cause `host-io`, with no custody subject. `ChildOpen`, `Absence`, `NameObservation`, and `ParentRefusal::Filesystem` (a failed `fstatfs` inside `AclOmissionPremise::admits`) take that same host I/O row. An opened directory that `is_home_filesystem` refuses is `GateRefusal::Filesystem`, published as request-rejected exit 2, `EXTENSION.ADMISSION_REJECTED`, `NT-TCB-BOOT`, subject `INSTALL_ROOT_FS`. The same function publishes that row for `OpenSIP` and I. None of these is absence or `INSTALLATION.ACCOUNT_REFUSED`.

The rest of the law's stated rows match the same mapper:

- Embedded root, entrypoint, or bootstrap absent is `CORE.NO_EMBEDDED_RELEASE`. The other core refusals in 468 item 6 are `NT-TCB-IDENTITY`. Native image and loader I/O stay `HOST.IO_FAILURE`. `PlatformUnavailable` is `NT-TCB-PROFILE-UNQUALIFIED`.
- A platform decision uses its own `NT-TCB-*` detail. Mismatch, translation, and loader filesystem are `NT-TCB-PROFILE-UNQUALIFIED`, subject `platform`. `InitialPlatformRefusal::HomeFilesystem` is `NT-TCB-BOOT`, subject `INSTALL_ROOT_FS`. Native process, boot, loader, and home-path I/O stay `HOST.IO_FAILURE`.
- Unequal UIDs, home spelling or bounds, and a changed account are `INSTALLATION.ACCOUNT_REFUSED`. `AccountObservationError::Lookup` is `HOST.IO_FAILURE`.
- A refused charge is `WORK.BUDGET_EXHAUSTED` on `SYSTEM.OUTCOME.ILLEGAL_STATE`, fault cause `host-invariant`.
- `AncestorAclOmitted` is `CONFIG.CUSTODY_REFUSED`, subject `ancestor-acl-omitted`.
- `ObservedAbsent` uses the same public row as `GateRefusal::Absent`: `INSTALLATION.NOT_INITIALIZED`. The write gate keeps its own internal classification. A symlink or a non-directory is an open error, so it stays off that row and on host I/O.
- An incomplete I for a command other than the doctor report is `CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`.
- Every `FileLock::try_acquire` `Err` is `HOST.IO_FAILURE`, exit 4. A carrier replaced after the lock is `FenceChanged`: `CONFIG.CUSTODY_REFUSED`, subject `fence-changed`. A lock still busy at 5 s or 201 attempts is `LEDGER.BUSY_TIMEOUT`, `PROJECT.BUSY`, fault cause `ledger-busy`.
- The doctor overflow stays the report channel: `HOST.IO_FAILURE` / `DOCTOR.REPORT_NOT_PRODUCIBLE`, exit 4.

## Required findings

None.
