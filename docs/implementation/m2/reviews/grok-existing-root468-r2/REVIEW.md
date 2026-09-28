# Review: existing-root admission 468 r2

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review of law 468 after r1. No repository edits and no product cargo.

Subject `docs/implementation/m2/existing-root-admission-468/PROPOSAL.md`, 8138 bytes, sha256 `2e348f9ac590ddefc13289d14c37b54d486523240f8af43af78526c9268878c0`. `PROPOSAL-r1.md` preserves the r1 bytes (`dfcf90b61eba5a0b70627be7cf3b7cb034d95ada899ce8df3d83ea42fff49155`, 5732 bytes). The diff is item 3 and the item 6 table.

## Verdict

**REQUIRED-FINDINGS.**

r1 RF-1 is closed. r1 RF-2 is closed for the families that were unassigned, and two table cells still disagree with the existing termination vocabulary.

## Gate

A busy fence stops at `PROJECT.BUSY`. No recheck, barrier or later effect runs, because the lock is not held. Under the held fence the recheck set is the original account, the I-parent name, I's identity and the fence file's identity, custody of I and of the I-parent (owner, mode and ACL under the existing predicate for that directory), and the required files: the fence, `project-registry.v2`, `selection.pair`, the endpoint marker, the lineage node chain and the trust current record, each owned by the invoking user, in private mode, with one link and a private ACL. That set runs before the barriers and again after them, including after a failed barrier at step 3 or 4, still under the held fence. I's own barrier remains the one 467 item 4 left to this gate, and the I-parent barrier stays on the retained parent handle. A failure at steps 2 to 5 latches the durable path.

## Routes that match

Checked against `public-detail-registry.json`, `diagnostic-routes.json`, and S12, which is where those details receive a class. `diagnostic-routes.json` carries `INSTALLATION.NOT_INITIALIZED`, `storage.backup-choice-required` and the doctor rows. It has no `PROJECT.BUSY`, `NT-TCB-*`, `CONFIG.CUSTODY_REFUSED` or `HOST.IO_FAILURE` route.

| Family | Table | Existing class and code | |
|---|---|---|---|
| Embedded release absent | request-rejected, 2, `REQUEST.PRECONDITION_FAILED`, new `CORE.NO_EMBEDDED_RELEASE` | Same shape as `INSTALLATION.NOT_INITIALIZED` | matches |
| Actor refusal | request-rejected, 2, `REQUEST.PRECONDITION_FAILED`, new `INSTALLATION.ACCOUNT_REFUSED` | Same | matches |
| Backup choice | request-rejected, 2, `REQUEST.PRECONDITION_FAILED`, `storage.backup-choice-required` | diagnostic-routes and S12 | matches |
| I absent for a command that needs it | request-rejected, 2, `REQUEST.PRECONDITION_FAILED`, `INSTALLATION.NOT_INITIALIZED` | diagnostic-routes and owner §6 | matches |
| Other core refusal | request-rejected, 2, `EXTENSION.ADMISSION_REJECTED`, `NT-TCB-IDENTITY` plus subject | S12 `NT-TCB-*` row | matches |
| Platform decision, mismatch, translated process, loader filesystem, unqualified H | request-rejected, 2, `EXTENSION.ADMISSION_REJECTED`, the decision's `NT-TCB-*` detail, `NT-TCB-PROFILE-UNQUALIFIED` subject `platform`, or `NT-TCB-BOOT:INSTALL_ROOT_FS` | S12, and the profile decision's own `NT-TCB-BOOT:INSTALL_ROOT_FS` spelling | matches |
| Custody, gate owner failure, stage validation or name failure before the rename | request-rejected, 2, `CONFIG.INVALID`, `CONFIG.CUSTODY_REFUSED` plus subject | S12 and S12.1 | matches |
| NotPerformed, indeterminate, after the rename, barrier, read I/O, disclosure write | operational-failed, 4, `HOST.IO_FAILURE`, fault cause `host-io` | S12 I/O row; schema pairs `host-io` with `HOST.IO_FAILURE` | matches |
| `LostRace`, `NotPristine`, `Published` | continue through the gate | 467 item 11 | matches |

`NT-TCB-BOOT:INSTALL_ROOT_FS` is the registered code `NT-TCB-BOOT` with subject `INSTALL_ROOT_FS`, not a fourth domain detail. The three new details remain the only additions. Items 2, 5, 7, 8 and 9 are unchanged and stay as accepted in r1.

## Required findings

### RF-1 — The busy row puts `PROJECT.BUSY` in the error-code column

`PROJECT.BUSY` is a domain detail in `public-detail-registry.json` and in `DomainDetailCode`. It is not a `D9ErrorCode`. S12 maps that refusal to operational-failed, exit 4, error code `LEDGER.BUSY_TIMEOUT`. The schema pairs that error code with fault cause `ledger-busy`. The detail is `PROJECT.BUSY`.

The table's busy row says class "refused, per the existing row", puts `PROJECT.BUSY` in the D9 error-code column, and leaves the detail as "per the existing row". `diagnostic-routes.json` has no busy route that could supply another class.

Failure scenario: the fence is busy and the termination is built from the table. `PROJECT.BUSY` is emitted as the error code. The envelope is not a valid operational-failed termination, because that class requires `LEDGER.BUSY_TIMEOUT` with fault cause `ledger-busy` and the detail `PROJECT.BUSY`. A caller that treats "refused" as request-rejected also leaves exit 4.

### RF-2 — The budget row pairs `HOST.IO_FAILURE` with fault cause `host-invariant`

The ledger row is operational-failed, exit 4, error code `HOST.IO_FAILURE`, domain detail `WORK.BUDGET_EXHAUSTED`, fault cause `host-invariant`. The closed fault map pairs `host-io` with `HOST.IO_FAILURE` and `host-invariant` with `SYSTEM.OUTCOME.ILLEGAL_STATE`. A termination cannot carry `HOST.IO_FAILURE` and `host-invariant` together. `WORK.BUDGET_EXHAUSTED` is new, so no registry row fixes this cell, and the sentence that defers to an existing class does not apply.

Failure scenario: the admission ledger refuses a charge. Emitting the table as written fails schema validation. Emitting `HOST.IO_FAILURE` with fault cause `host-io` to make it validate tells the caller the ledger cap was an I/O failure. The representable pair for fault cause `host-invariant` is error code `SYSTEM.OUTCOME.ILLEGAL_STATE`, with domain detail `WORK.BUDGET_EXHAUSTED`.
