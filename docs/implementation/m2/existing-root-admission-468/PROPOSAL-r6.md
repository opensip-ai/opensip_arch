# Existing-root admission after creation, diagnostics and routing — proposal 468 r6

2026-09-27. Claude Opus 5.5, implementation lead. Law for unit 468, under owner.md §5 to §7 and laws 464 and 467. Five decisions are the owner's own: four made on 2026-09-27 (items 2, 6, 7 and the 458c direction recorded in item 9), and the item 2 premise amendment made on 2026-09-28. Not code. Library only: CLI enablement is a separate unit (464 item 7). r2 answers Grok 468 r1 RF-1 (the gate recheck omitted custody and file owners; a busy fence must stop) and RF-2 (the D9 codes for the new request-rejected details, and refusals with no route). r3 answers Grok 468 r2 RF-1 (the busy row's error code) and RF-2 (the budget row's error code and fault cause). Earlier bytes are preserved in PROPOSAL-r1.md and PROPOSAL-r2.md. r3 was ACCEPTED by Grok on 2026-09-27. r4 is an amendment made after implementing 468b showed that the ordinary installation fence cannot be charged within the owner's budget: its unbounded chain re-observation costs about 126k of the 131,072-edge cap for one attempt on a `/Users/<name>` home, and it reads an omitted ACL as "no writers", which 461 retires. r3 bytes are preserved in PROPOSAL-r3.md. r5 answers Grok 468 r4 RF-1 (the observation path still took the uncharged fence). r4 bytes are preserved in PROPOSAL-r4.md. r5 ACCEPTED by Grok on 2026-09-28.

**r6 (2026-10-04) is an amendment: J1's successor S2.** It changes items 1, 2, 6 and 7, and adds one forbidden substitute. r5 bytes, as accepted (sha256 `0959e308…`, 11,373 bytes, without the acceptance note), are preserved in PROPOSAL-r5.md. **Draft r6, not accepted.** Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the autonomous run. Not code.
- **Its source.** J1 r5, the accepted host-pipeline law, cited as J1 (`docs/implementation/m3/host-pipeline-j/PROPOSAL-r5.md`, sha256 `4ccb2320…`; accepted by Codex, `m3/reviews/codex-host-pipeline-j-r5`). Its successor row S2 gives this law "item 1's route, and the value-only `created` record on the act's result and its post-rename refusals (item 3); item 7 landed by S13" (J1:847). J1 item 3 states the amendment (J1:279) and the record (J1:263-267). S13 is J1 item 9, the backup-status successor J-BS (J1:695-716).
- **What it changes.**
  - Item 1: after the creator act ends, the invocation continues through X1's ordinary admission on a fresh attempt B, not through a gate lent by the creator's `InitialPlatform`. The act's result, and its refusals after the publication rename, carry a value-only `created` record.
  - Item 2: one note. On the creator route, attempt B's `InitialPlatform` lends the unchanged capability.
  - Item 6: the continue row names item 1's route.
  - Item 7: the backup-status carrier lands with J1's successor S13, J-BS. The owner's deferral stands.
  - Forbidden substitutes: one line, taken from J1:909.
- **What it does not change.** No row, code, class, exit, subject or remedy of item 6. Items 3, 4, 5, 8 and 9 are unchanged.
- **Code.** The route and the record are code changes. They are J1 unit J3a's, which carries "the S2 to S7 code" (J1:881).
- **Unchanged from r5:** everything else. No accepted outcome of r5 or of another law changes, except as S2 declares.

**r6 changes.**

| # | Change | Where | Source |
|---|---|---|---|
| 1 | **The route.** `Published`, `LostRace` and `NotPristine` end the creator act, and attempt A is dropped with its core and platform. The invocation continues through X1's ordinary admission on a fresh attempt B, not through a gate lent by the creator's `InitialPlatform`. The creator act enters no gate. | item 1 | J1:259-261, :279, :847 |
| 2 | **The `created` record.** It is `Some` exactly when this act performed the exclusive publication rename. It comes from the act's own result. Every later path of the invocation carries it. Rows are unchanged. | item 1 | J1:263-267, :279; LD6-1 |
| 3 | **Item 2's capability is unchanged.** On the creator route, attempt B's `InitialPlatform` lends it. | item 2 | J1:279 |
| 4 | **The continue row** names item 1's route. | item 6 | J1:279 |
| 5 | **The backup-status carrier** lands with S13, J-BS, whose first emitter is J3d's durable envelope. The stderr notice stays. | item 7 | J1:697-713, :847; LD6-2 |
| 6 | **One forbidden substitute** for the record | Forbidden substitutes | J1:263, :909 |
| 7 | **The code is J3a's.** | item 1 | J1:267, :881 |

**r6 lead decisions.** Each is made under the owner's standing direction of 2026-09-30, where J1's text leaves a point open. Each names the alternative it rejects.
- **LD6-1. Which refusals carry `Some`.** J1 makes `created` `Some` "exactly when this invocation's creator act performed the exclusive publication rename". It then names "a refusal after the rename, which L468's host-I/O row covers as 'any failure after the rename'" (J1:264). Two refusals sit at the edge of that sentence. At product `d2c00a9`, the act marks the rename done only after the rename call returns success (`crates/security/src/custody/installation_publication.rs:277-285`).
  - **A ledger refusal after the rename.** The act returns it inside its post-rename refusal (`:370-376`), and 468c routes it to the budget row, not the host-I/O row (`installation_routing.rs:458-461`). **Decision:** `Some`. The rename was performed, and J1's defining clause governs over the row it names in passing.
  - **An indeterminate rename.** Item 6 lists it apart from "any failure after the rename". The act returns it as a rename refusal, before it marks the rename done (`installation_publication.rs:377-382`). **Decision:** `None`, as for a rename not performed. The act's own result does not establish that the rename happened. The stderr notice, flushed before any effect (464 item 3), has already disclosed the intended creation.
  - **Rejected:**
    - `None` for the post-rename ledger refusal, because its row is not the host-I/O row. I is published, and J1's control J-C6b expects "a failure after the rename" to disclose it (J1:328).
    - `Some` for an indeterminate rename. It claims a creation the act cannot establish. Settling it would need a later existence scan, which J1 forbids as the record's source (J1:265, :702).
- **LD6-2. Item 7 names S13 and keeps the owner's deferral.** Item 7 is an owner decision: the carrier waits until an envelope is emitted. r5 named "the CLI-enablement unit" as the place. X11 r1 item 3 moved it to the M3 unit that first emits a `retentionDisclosure`. J1, X11's successor, wires no CLI command at M3 (J1 item 1). It lands the carrier as its contract successor S13, J-BS, and J-BS's first emitter is J3d's durable envelope (J1:705, :713).
  - **Decision.** Item 7 names S13 as the carrier and J3d as its first emitter, and keeps the deferral condition. Until S13 is accepted and J3d emits the envelope, the stderr notice is the only carrier.
  - **Rejected:** recording the carrier as landed. S13 still needs its own ACCEPT-DESIGN-UNIT review (M3-PLAN r9, M3P:265), and no emitter exists yet.

## Decisions

1. **Continuing after the creator.** `Published`, `LostRace` and `NotPristine` all end the creator act, and the attempt is dropped. Because all four creator commands write, the invocation continues through the owner §5 durable write gate with a fresh installation fence. No creator observation, handle, lock or receipt is reused (467 item 9).
   - **(r6, J1 S2) The route.** The creator act runs on the process's attempt A (J1 item 3, route 3b). When it ends, attempt A is dropped with its core and platform, and the creator act enters no gate (J1:260). The invocation then continues through X1's ordinary admission on a fresh attempt B: `admit_ordinary_writer`, with fresh producers, the receipt's rechecks and the process's one gate, whose steps are item 3's (X1 r2 item 7; J1:261). It does not continue through a gate lent by the creator's `InitialPlatform` (J1:279).
   - **(r6, J1 S2) The `created` record.** The creator act's result, and each of its refusals after the publication rename, carry a value-only record, `created: Option<Created { classification, target }>` (J1:263, :279). It holds the backup classification and the target that the intent disclosed. It holds values only and carries no authority from attempt A.
     - **When it is `Some`.** Exactly when this act performed the exclusive publication rename (J1:264): the `Published` result, and every refusal after the rename, on whichever row item 6 gives it (LD6-1).
     - **When it is `None`.** For `LostRace` and `NotPristine`, which published nothing, and for every refusal before the rename, a rename not performed and an indeterminate rename included (J1:266; LD6-1).
     - **Where it comes from.** The act's own typed result. Never a later existence scan, and never the fact that an intent was minted (J1:265).
     - **What carries it.** Every later path of the invocation: attempt B's producers, gate, barriers and rechecks, and every refusal after them (J1:267). J1 item 9 discloses it in the envelope.
     - **Rows.** The record changes no row, code, class, exit, subject or remedy of item 6 (J1:278-279).
   - **(r6) Code.** The route and the record are code in J1 unit J3a (J1:881). At product `d2c00a9`, 468c's `route` enters the gate with the creator's `InitialPlatform` and drops a post-rename refusal's creation (`crates/security/src/custody/installation_routing.rs:90-119`).
2. **What the gate borrows (owner decisions, 2026-09-27 and 2026-09-28).** The durable write gate borrows from this same invocation's `InitialPlatform`, through a sealed private capability that only `InitialPlatform` implements. The capability lends exactly three things:
   - the barrier policy: apfs `F_FULLFSYNC`, or the named fallback;
   - the check that a filesystem matches H's;
   - `InitialPlatform`'s omission premise (Evidence B), if it holds one, with exactly 465 item 4's scope: the root-to-H prefix, `Library` and `Application Support`, applied only through the premise's own `fstatfs` on each descriptor. Without a premise, an omitted ACL on any of those refuses, as in 465. `OpenSIP` and I never use it.

   The capability lends nothing about I, grants no standing, and cannot be built from a caller. Writers that are not creators get no gate until the ordinary platform owner exists (M2 exit).

   **(r6, J1 S2)** On the creator route, the `InitialPlatform` that lends this capability is attempt B's, produced by X1's ordinary admission (item 1). The creator's own `InitialPlatform` lends nothing to the gate. The capability itself is unchanged (J1:279).
3. **The gate's order.**
   0. **Charged chain walk.** Walk from root through H, `Library`, `Application Support`, `OpenSIP` and I with retained no-follow handles. Use the existing 460 and 465 custody predicates, with item 2's premise where it applies. Every step is charged to the item 4 ledger. The ordinary installation fence's own uncharged re-observation of the chain is not used.
   1. **Fence attempt.** A nonblocking attempt on I's fence file, opened no-follow through the retained I handle from step 0. If the fence is busy the invocation stops with the existing busy termination (item 6), detail `PROJECT.BUSY`. No recheck, barrier or later effect follows, because the lock is not held. The gate still latches, so the invocation cannot try again. This is the same stable installation fence file and the same lock that ordinary holders take (owner §5, 467 item 9), so it excludes them exactly as before. Only the uncharged way of reaching it changes.
   2. **Recheck under the held fence.** The recheck set is:
      - the original account;
      - the I-parent name;
      - I's identity and the fence file's identity;
      - the retained chain from step 0: each component's identity and name, and custody under the step 0 predicates and premise;
      - custody of I and of the I-parent: owner, mode and ACL under the existing private and ancestor custody predicates;
      - the required file owners: the fence, `project-registry.v2`, `selection.pair`, the endpoint marker, its lineage node chain and the trust current record, each owned by the invoking user, private mode, one link, private ACL.
   3. I's own directory barrier. This is the barrier 467 item 4 left to this gate.
   4. The I-parent barrier through the retained parent handle.
   5. The same recheck set again, still under the held fence. This recheck also runs after a failed barrier at step 3 or 4.

   Every receipt is checked against its handle. Any failure at steps 2 to 5 latches the invocation's durable path for good: no retry and no later effect.
4. **Budget.** Each existing-root admission uses one failure-latching ledger with the owner's limits. The gate charges its chain walk, fence attempt, barriers and rechecks before each step. The post-barrier recheck is reserved with the barriers, before they run, as in 467 item 6. The observation-only read path (owner §5) never calls the ordinary fence's uncharged acquire either. It reaches the same fence through item 3's steps 0 and 1: the same charged, retained walk and the same no-follow fence attempt, under its own ledger. It then charges its fixed member reads up front and rechecks under the held fence. No barrier runs on that path.

   A read command has no `InitialPlatform`, so its premise for step 0 can only come from the 458c receipt (item 9). Until law 458c is accepted, 468 builds no observation path. 468c ships the write path and the public routing only. The observation path, doctor's informational note and its 256-slot rule are implemented with 458c/461. Open for 458c: item 9 recorded the receipt's scope as root to H, while step 0 also reaches `Library` and `Application Support`. 458c must either cover those two with 465 item 4's scope, or have them refuse on an omitted ACL.
5. **Complete I.** I is complete only when the fence, `project-registry.v2`, `selection.pair`, the endpoint marker, its lineage node chain and the trust current record are all observed under one fence (owner §7). Anything else is unavailable under the existing read owner's refusal (owner §7), routed publicly by item 6's incomplete-installation row. The doctor informational note is produced only for a complete I, and only by `doctor`. It never counts as a defect, never truncates, and takes one of the 256 slots. 256 real defects plus the note refuses, and the report is not produced.
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
   | I present but incomplete or contradictory (item 5): a required file missing, undecodable or with the wrong owner-chain linkage | request-rejected, 2 | `CONFIG.INVALID` | existing `CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete` |
   | Installation fence busy | operational-failed, 4 | `LEDGER.BUSY_TIMEOUT` | existing `PROJECT.BUSY`, fault cause ledger-busy |
   | Rename not performed; indeterminate rename; any failure after the rename; barrier failure; filesystem or read I/O failure; disclosure write failure | operational-failed, 4 | `HOST.IO_FAILURE` | fault cause host-io |
   | Attempt or admission ledger refused a charge | operational-failed, 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` | NEW `WORK.BUDGET_EXHAUSTED`, fault cause host-invariant |
   | `LostRace`, `NotPristine`, `Published` | not a failure: **(r6)** continue through X1's ordinary admission on attempt B, whose gate is item 3's (item 1) | — | — |

   The three new details are appended to common4 `DomainDetailCode` with public detail registry rows and D9 routes, the same way the 2026-09-21 owner-selection unit appended `INSTALLATION.NOT_INITIALIZED`: a contract successor, generation and a drift check. No existing code, class or exit changes. The table follows the existing registry's class and code for every existing detail; where the registry already fixes a class for a detail, the registry prevails and this table is corrected by review.
7. **Backup status in the envelope (owner decision: deferred).** The `RetentionDisclosure` carrier for backup status, which 464 decision 3 owed to 468, is deferred to **(r6)** the first unit that emits an envelope, because no envelope is emitted before then. Until then the stderr notice carries it.

   **(r6, J1 S2; LD6-2)** The carrier lands with J1's contract successor S13, J-BS (J1 item 9). r5 named the CLI-enablement unit. J1 is that unit's successor and wires no CLI command at M3 (J1 item 1). J-BS adds an optional `backupStatus` member to invocation-v5's `RetentionDisclosure`. It is present exactly when `firstUse` is true, and `firstUse` is true exactly when item 1's `created` is `Some` (J1:697-699). Its first emitter is J3d's durable envelope (J1:713). The stderr notice stays (J1:704). Until S13 is accepted and J3d emits the envelope, the notice is the only carrier.
8. **Golden wording.** The command inventory golden for `analyze-backup-choice-required-in-ci` drops "or select another admitted root" and "an admitted storage-policy record" (464 decision 6). The first-use golden records that the root and "backup status unknown" were disclosed. Both changes are text overrides in a contract successor.
9. **Recorded direction for 458c (owner decision).** The read side's use of the omission premise will be a fence-free, per-invocation platform receipt, authenticated through the embedded release and limited to the root-to-H prefix, granting no other standing. That is law 458c's, not this proposal's. It is recorded here so 468's read path is not built to conflict with it.

## Forbidden substitutes

Reusing a creator handle, lock, receipt or observation as write authority; a gate with no fence or without I's barrier; a barrier qualification built by a caller; counting the doctor note as a defect, or truncating; a new public code other than the three in item 6; changing an existing code, class or exit. **(r6)** A `created` record dropped on a refusal after the rename, taken from anything but the creator act's own result, or carrying authority from attempt A (J1:263, :909).

## Not claimed

CLI enablement; project leases and first registration; operational id reservation; ordinary platform, core or trust admission for writers that are not creators; stage cleanup; a positive backup detector; 458c and 461.
