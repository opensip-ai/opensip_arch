# Existing-root admission after creation, diagnostics and routing — proposal 468 r1

2026-09-27. Claude Opus 5.5, implementation lead. Law for unit 468, under owner.md §5 to §7 and laws 464 and 467. Four decisions are the owner's own, made on 2026-09-27 (items 2, 6, 7 and the 458c direction recorded in item 9). Not code. Library only: CLI enablement is a separate unit (464 item 7).

## Decisions

1. **Continuing after the creator.** `Published`, `LostRace` and `NotPristine` all end the creator act, and the attempt is dropped. Because all four creator commands write, the invocation continues through the owner §5 durable write gate with a fresh installation fence. No creator observation, handle, lock or receipt is reused (467 item 9).
2. **The gate's barrier qualification (owner decision).** The durable write gate needs the qualified barrier method and filesystem check. It borrows both from this same invocation's `InitialPlatform`, through a sealed private capability that only `InitialPlatform` implements. The capability lends exactly two things: the barrier policy (apfs `F_FULLFSYNC`, or the named fallback) and the check that a filesystem matches H's. It lends nothing about I, grants no standing, and cannot be built from a caller. Writers that are not creators get no gate until the ordinary platform owner exists (M2 exit).
3. **The gate's order.**
   1. Nonblocking fence attempt. Busy gives `PROJECT.BUSY`.
   2. Recheck the account, the I-parent name, I and the fence.
   3. I's own directory barrier. This is the barrier 467 item 4 left to this gate.
   4. The I-parent barrier through the retained parent handle.
   5. Recheck everything again. The recheck also runs after any earlier error.

   Every receipt is checked against its handle. Any failure ends the invocation's durable path for good: no retry and no later effect.
4. **Budget.** Each existing-root admission uses one failure-latching ledger with the owner's limits. The gate charges its barriers and rechecks before each step. The observation-only read path charges its fixed member reads up front.
5. **Complete I.** I is complete only when the fence, `project-registry.v2`, `selection.pair`, the endpoint marker, its lineage node chain and the trust current record are all observed under one fence (owner §7). Anything else is unavailable under the existing read owner's refusal. The doctor informational note is produced only for a complete I, and only by `doctor`. It never counts as a defect, never truncates, and takes one of the 256 slots. 256 real defects plus the note refuses, and the report is not produced.
6. **Public outcomes for creator failures (owner decision: three new codes).** Each failure maps to exactly one public termination.
   - **Existing rows:**
     - backup choice required: `storage.backup-choice-required`, request-rejected, exit 2, as already routed;
     - custody refusal, including the omitted ACL at `/`: `CONFIG.CUSTODY_REFUSED`, with the sub-detail as subject;
     - platform refusal: the existing `NT-TCB-*` details, with `EXTENSION.ADMISSION_REJECTED`, exit 2;
     - indeterminate rename, failure after the rename, barrier failure, filesystem I/O failure, and a failed disclosure write: operational-failed, exit 4, `HOST.IO_FAILURE`, fault cause host-io.
   - **New domain detail codes**, appended to common4 `DomainDetailCode` with public detail registry rows and D9 routes:
     - `CORE.NO_EMBEDDED_RELEASE`: a build that embeds no signed release (InitialCore F0). Request-rejected, exit 2. The remedy is to use a release build.
     - `INSTALLATION.ACCOUNT_REFUSED`: an actor refusal (unequal real and effective UID, home out of bounds, account changed). Request-rejected, exit 2. The remedy is to run as the account owner from a normal session.
     - `WORK.BUDGET_EXHAUSTED`: the attempt or admission ledger refused a charge. Operational-failed, exit 4, fault cause host-invariant. No retry within the invocation.

   The codes are appended in the same way as the 2026-09-21 owner-selection unit appended `INSTALLATION.NOT_INITIALIZED`: a contract successor, generation and a drift check. No existing code, class or exit changes.
7. **Backup status in the envelope (owner decision: deferred).** The `RetentionDisclosure` carrier for backup status, which 464 decision 3 owed to 468, is deferred to the CLI-enablement unit, because no envelope is emitted before then. Until then the stderr notice carries it.
8. **Golden wording.** The command inventory golden for `analyze-backup-choice-required-in-ci` drops "or select another admitted root" and "an admitted storage-policy record" (464 decision 6). The first-use golden records that the root and "backup status unknown" were disclosed. Both changes are text overrides in a contract successor.
9. **Recorded direction for 458c (owner decision).** The read side's use of the omission premise will be a fence-free, per-invocation platform receipt, authenticated through the embedded release and limited to the root-to-H prefix, granting no other standing. That is law 458c's, not this proposal's. It is recorded here so 468's read path is not built to conflict with it.

## Forbidden substitutes

Reusing a creator handle, lock, receipt or observation as write authority; a gate with no fence or without I's barrier; a barrier qualification built by a caller; counting the doctor note as a defect, or truncating; a new public code other than the three in item 6; changing an existing code, class or exit.

## Not claimed

CLI enablement; project leases and first registration; operational id reservation; ordinary platform, core or trust admission for writers that are not creators; stage cleanup; a positive backup detector; 458c and 461.
