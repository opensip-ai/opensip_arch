# Review: existing-root admission 468 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of existing-root admission, diagnostics and routing. No repository edits and no product cargo.

Subject `docs/implementation/m2/existing-root-admission-468/PROPOSAL.md`, 5732 bytes, sha256 `dfcf90b61eba5a0b70627be7cf3b7cb034d95ada899ce8df3d83ea42fff49155`. Items 2, 6, 7 and 9 are owner decisions of 2026-09-27. This review judges how they are written. It does not reopen the choices.

## Verdict

**REQUIRED-FINDINGS.**

## What holds

Item 1 matches 467 items 9 and 11 and owner §6. `Published`, `LostRace` and `NotPristine` end the creator act, the attempt is dropped, and a writing command continues on a fresh installation fence. No creator handle, lock, receipt or observation is reused. `Outcome` in `installation_publication.rs` is those three results.

Item 3's order is the durable-write sequence in owner §5: nonblocking fence (`PROJECT.BUSY`, as 467 item 9 and S12 already route it), a recheck, I's own barrier (the one 467 item 4 left to this gate), the I-parent barrier on the retained parent handle, a recheck again, including after an error. Receipts are checked against their handles. A failure ends the durable path with no retry. The recheck set itself is RF-1.

Item 2 is tightly scoped. The capability is sealed, implemented only by this invocation's `InitialPlatform`, and not constructible by a caller. It lends the apfs barrier policy (`F_FULLFSYNC`, or the named `Fsync` fallback) and the check that a filesystem is H's, which is the existing qualification: local, not a union, and the same filesystem identity as H. It lends nothing about I and grants no standing. `PrimitivePolicy` also names the exclusive rename; this capability does not lend that. Writers that are not this creator wait for the ordinary platform owner.

Item 4 gives each admission one failure-latching ledger at the owner's caps, charges the gate's barriers and rechecks before the step, and charges the observation path's member reads up front.

Item 5's positive members are the installation fence, `project-registry.v2`, `selection.pair`, the endpoint marker, the lineage node chain, and the trust current record, observed under one fence. "Only when" states what is necessary. A missing required trust dependency stays unavailable under the existing read owner's refusal, which is owner §6. The doctor rule matches `doctor-cases.json` and `check_doctor.py`: the note is only for a complete I and only on `doctor`; it is not a defect and is not truncated; it occupies one of the 256 slots; 255 actual defects plus the note are produced with `defectsFound` equal to the actual count; 256 actual defects plus the note refuse and produce no report. A partial root keeps the 256-entry bound and does not receive the note.

Item 6's names follow the dotted form used for `INSTALLATION.NOT_INITIALIZED`, not the older lowercase `storage.backup-choice-required` spelling. `INSTALLATION.ACCOUNT_REFUSED` sits in that family. `CORE.NO_EMBEDDED_RELEASE` names InitialCore F0, a build with no embedded signed release, and its remedy is a release build. `WORK.BUDGET_EXHAUSTED` is a new code for the fixed creation and admission ledger. Reusing `EVALUATION.WORK_BUDGET_EXHAUSTED` would put it in the indeterminate class whose remedy is to raise an analysis budget; the owner caps cannot be raised, and the invocation does not retry. Operational-failed, exit 4, and fault cause `host-invariant` are representable as error code `SYSTEM.OUTCOME.ILLEGAL_STATE` with domain detail `WORK.BUDGET_EXHAUSTED`. The routes that do not yet name one termination are RF-2.

These existing rows are right: `storage.backup-choice-required` stays request-rejected, exit 2, `REQUEST.PRECONDITION_FAILED`. Custody, including an omitted ACL at `/`, stays `CONFIG.CUSTODY_REFUSED` with the sub-detail as subject, which S12 projects as request-rejected, exit 2, `CONFIG.INVALID`. An `NT-TCB-*` detail stays `EXTENSION.ADMISSION_REJECTED`, exit 2. Indeterminate rename, failure after the rename, barrier failure, filesystem I/O, and a failed disclosure write are operational-failed, exit 4, `HOST.IO_FAILURE`, fault cause `host-io`.

Item 7 defers the backup-status field on `RetentionDisclosure` to CLI enablement. No envelope is emitted before that unit. The stderr notice continues to carry the status, as 464 decision 3 requires until the field exists.

Item 8 matches the selected `command-inventory.v3.json` golden and 464 decision 6. `analyze-backup-choice-required-in-ci` drops "or an admitted storage-policy record" from the situation and "or select another admitted root" from the remedy. `default-first-use-durable` gains the account-derived root and "backup status unknown" beside the retention phrase it already records. Both are text overrides in a contract successor.

Item 9 records the 458c direction without enacting it: a fence-free, per-invocation platform receipt, authenticated through the embedded release, limited to the root-to-H prefix, and granting no other standing. The fenced read of a complete I does not depend on that receipt.

## Required findings

### RF-1 — The gate recheck drops custody and file owners

Owner §5 requires both paths to recheck the original account, custody, I-parent name, I, the fence, and the required file owners, under one failure-latching budget. The durable-write paragraph reconfirms I and its parent under those custody, name and identity observations, before the barriers and again after them, including when a barrier fails, while the fence is held.

Item 3 step 2 rechecks the account, the I-parent name, I and the fence. Step 5 rechecks that same set again. Custody and the required file owners are not in the set. The sentence that runs the recheck after any earlier error also applies it to a busy fence, where the invocation does not hold the lock.

Failure scenario: the fresh fence is acquired and the named rechecks pass. I's mode or ACL, or the owner of the fence file, has changed since publication. The gate still takes I's barrier and the I-parent barrier and continues the command's write. A busy fence likewise continues into an unlocked recheck instead of stopping at `PROJECT.BUSY`.

### RF-2 — Two new refusals have no single D9 error code, and several creator refusals have no row

Item 6 says each creator failure maps to exactly one public termination, and that no public code is added beyond the three new domain details. A request-rejected termination still needs a `D9ErrorCode`. Exit 2 alone is shared by `CONFIG.INVALID`, `REQUEST.PRECONDITION_FAILED`, `REQUEST.UNSATISFIABLE`, `EXTENSION.ADMISSION_REJECTED` and `REQUEST.SCHEMA_MAJOR_UNSUPPORTED`. `CORE.NO_EMBEDDED_RELEASE` and `INSTALLATION.ACCOUNT_REFUSED` name the class and the exit, and do not name the error code.

The same item does not assign a row to a `NotPerformed` rename, a pre-rename validation or name recheck, a core refusal other than a missing embedded release, or a platform refusal that is not an `NT-TCB-*` detail. `InitialPlatformRefusal::HomeFilesystem` is one of those. The forbidden-substitutes clause forbids a fourth domain detail, so these refusals are either unpublished or placed on a row whose remedy is a different fault.

Failure scenario: a development build and an account-home spelling failure can both be emitted as request-rejected exit 2 with different error codes, and a golden cannot pin either route. A stage whose bytes changed, or an H that is not a qualified install filesystem, is then reported as `HOST.IO_FAILURE` or `NT-TCB-PROFILE-UNQUALIFIED`. The caller is told to treat a content or filesystem refusal as a host I/O or TCB-profile failure.

## Not reopened

The choice of three new codes, the deferral of the envelope field, the `InitialPlatform` capability, and the 458c direction stand. The findings are the missing recheck members and the routes that are not yet one termination.
