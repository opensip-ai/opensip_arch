# Existing-root admission after creation, diagnostics and routing — proposal 468 r2

2026-09-27. Claude Opus 5.5, implementation lead. Law for unit 468, under owner.md §5 to §7 and laws 464 and 467. Four decisions are the owner's own, made on 2026-09-27 (items 2, 6, 7 and the 458c direction recorded in item 9). Not code. Library only: CLI enablement is a separate unit (464 item 7). r2 answers Grok 468 r1 RF-1 (the gate recheck omitted custody and file owners; a busy fence must stop) and RF-2 (the D9 codes for the new request-rejected details, and refusals with no route). r1 bytes are preserved in PROPOSAL-r1.md.

## Decisions

1. **Continuing after the creator.** `Published`, `LostRace` and `NotPristine` all end the creator act, and the attempt is dropped. Because all four creator commands write, the invocation continues through the owner §5 durable write gate with a fresh installation fence. No creator observation, handle, lock or receipt is reused (467 item 9).
2. **The gate's barrier qualification (owner decision).** The durable write gate needs the qualified barrier method and filesystem check. It borrows both from this same invocation's `InitialPlatform`, through a sealed private capability that only `InitialPlatform` implements. The capability lends exactly two things: the barrier policy (apfs `F_FULLFSYNC`, or the named fallback) and the check that a filesystem matches H's. It lends nothing about I, grants no standing, and cannot be built from a caller. Writers that are not creators get no gate until the ordinary platform owner exists (M2 exit).
3. **The gate's order.**
   1. **Fence attempt.** A nonblocking attempt. If the fence is busy the invocation stops with `PROJECT.BUSY`. No recheck, barrier or later effect follows, because the lock is not held.
   2. **Recheck under the held fence.** The recheck set is:
      - the original account;
      - the I-parent name;
      - I's identity and the fence file's identity;
      - custody of I and of the I-parent: owner, mode and ACL under the existing private and ancestor custody predicates;
      - the required file owners: the fence, `project-registry.v2`, `selection.pair`, the endpoint marker, its lineage node chain and the trust current record, each owned by the invoking user, private mode, one link, private ACL.
   3. I's own directory barrier. This is the barrier 467 item 4 left to this gate.
   4. The I-parent barrier through the retained parent handle.
   5. The same recheck set again, still under the held fence. This recheck also runs after a failed barrier at step 3 or 4.

   Every receipt is checked against its handle. Any failure at steps 2 to 5 latches the invocation's durable path for good: no retry and no later effect.
4. **Budget.** Each existing-root admission uses one failure-latching ledger with the owner's limits. The gate charges its barriers and rechecks before each step. The observation-only read path charges its fixed member reads up front.
5. **Complete I.** I is complete only when the fence, `project-registry.v2`, `selection.pair`, the endpoint marker, its lineage node chain and the trust current record are all observed under one fence (owner §7). Anything else is unavailable under the existing read owner's refusal. The doctor informational note is produced only for a complete I, and only by `doctor`. It never counts as a defect, never truncates, and takes one of the 256 slots. 256 real defects plus the note refuses, and the report is not produced.
6. **Public outcomes (owner decision: three new codes).** Every refusal family from units 459 to 468 maps to exactly one public termination, as the table below. The mapping is total: code must match exhaustively, so a new refusal variant cannot compile without a row.

   | Refusal family | Class, exit | D9 error code | Domain detail |
   |---|---|---|---|
   | Embedded release absent (InitialCore F0) | request-rejected, 2 | `REQUEST.PRECONDITION_FAILED` | NEW `CORE.NO_EMBEDDED_RELEASE` |
   | Actor refusal: unequal UIDs, home spelling or bounds, account changed | request-rejected, 2 | `REQUEST.PRECONDITION_FAILED` | NEW `INSTALLATION.ACCOUNT_REFUSED` |
   | Backup choice required | request-rejected, 2 | `REQUEST.PRECONDITION_FAILED` | existing `storage.backup-choice-required` |
   | Command needs the installation and I is absent | request-rejected, 2 | `REQUEST.PRECONDITION_FAILED` | existing `INSTALLATION.NOT_INITIALIZED` |
   | Other core refusal: release authentication, quorum, revocation, entrypoint, code-signing flags, K, core-tree custody | request-rejected, 2 | `EXTENSION.ADMISSION_REJECTED` | existing `NT-TCB-IDENTITY`, with the refusal as subject |
   | Platform decision refusal: profile, major, build floor, identity, lane | request-rejected, 2 | `EXTENSION.ADMISSION_REJECTED` | the decision's own `NT-TCB-*` detail |
   | Platform mismatch, translated process, loader filesystem | request-rejected, 2 | `EXTENSION.ADMISSION_REJECTED` | existing `NT-TCB-PROFILE-UNQUALIFIED`, subject `platform` |
   | H not a qualified install filesystem | request-rejected, 2 | `EXTENSION.ADMISSION_REJECTED` | existing `NT-TCB-BOOT:INSTALL_ROOT_FS` |
   | Custody refusal on the chain, the ancestors or I (including the omitted ACL at `/`), a gate recheck custody or owner failure, and a stage validation or name-recheck failure before the rename (foreign interference) | request-rejected, 2 | `CONFIG.INVALID` | existing `CONFIG.CUSTODY_REFUSED`, with the sub-detail as subject |
   | Installation fence busy | refused, per the existing row | `PROJECT.BUSY` | per the existing row |
   | Rename not performed; indeterminate rename; any failure after the rename; barrier failure; filesystem or read I/O failure; disclosure write failure | operational-failed, 4 | `HOST.IO_FAILURE` | fault cause host-io |
   | Attempt or admission ledger refused a charge | operational-failed, 4 | `HOST.IO_FAILURE` | NEW `WORK.BUDGET_EXHAUSTED`, fault cause host-invariant |
   | `LostRace`, `NotPristine`, `Published` | not a failure: continue through the item 3 gate | — | — |

   The three new details are appended to common4 `DomainDetailCode` with public detail registry rows and D9 routes, the same way the 2026-09-21 owner-selection unit appended `INSTALLATION.NOT_INITIALIZED`: a contract successor, generation and a drift check. No existing code, class or exit changes. The table follows the existing registry's class and code for every existing detail; where the registry already fixes a class for a detail, the registry prevails and this table is corrected by review.
7. **Backup status in the envelope (owner decision: deferred).** The `RetentionDisclosure` carrier for backup status, which 464 decision 3 owed to 468, is deferred to the CLI-enablement unit, because no envelope is emitted before then. Until then the stderr notice carries it.
8. **Golden wording.** The command inventory golden for `analyze-backup-choice-required-in-ci` drops "or select another admitted root" and "an admitted storage-policy record" (464 decision 6). The first-use golden records that the root and "backup status unknown" were disclosed. Both changes are text overrides in a contract successor.
9. **Recorded direction for 458c (owner decision).** The read side's use of the omission premise will be a fence-free, per-invocation platform receipt, authenticated through the embedded release and limited to the root-to-H prefix, granting no other standing. That is law 458c's, not this proposal's. It is recorded here so 468's read path is not built to conflict with it.

## Forbidden substitutes

Reusing a creator handle, lock, receipt or observation as write authority; a gate with no fence or without I's barrier; a barrier qualification built by a caller; counting the doctor note as a defect, or truncating; a new public code other than the three in item 6; changing an existing code, class or exit.

## Not claimed

CLI enablement; project leases and first registration; operational id reservation; ordinary platform, core or trust admission for writers that are not creators; stage cleanup; a positive backup detector; 458c and 461.
