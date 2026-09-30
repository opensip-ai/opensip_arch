# The read side's omission premise and the observation path — proposal 458c r4

2026-09-29. Claude Opus 5.5, implementation lead. Law for unit 458c, under owner.md §5 to §7 and laws 458, 458b, 462, 463, 465 and 468 r5. Four decisions are the owner's own: the fence-free, per-invocation receipt authenticated through the embedded release (2026-09-27, recorded in 468 item 9); its scope, which matches 465 item 4 (2026-09-29); the read path's bounded busy wait (item 11, 2026-09-29); and doctor's refusal when it cannot reach I (item 12, 2026-09-29). It also carries the observation path, the doctor note and the 255+1 slot rule that 468 r5 item 4 deferred here. Not code. Library only: CLI enablement is a separate unit (464 item 7). r2 answers Grok 458c r1 RF-1 to RF-4: the required file owners in the recheck, doctor's partial report, the busy wait's pace and reservation, and positive absence. r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok 458c r2 RF-1 (a missing H) and RF-2 (I/O during the fence wait). r2 bytes are preserved in PROPOSAL-r2.md. r4 answers Grok 458c r3 RF-1 and RF-2 by adopting the write gate's own classification for H and for the fence lock's errors. r3 bytes are preserved in PROPOSAL-r3.md.

## Problem

Every read-side consumer reaches I through `InstallationReadFence::try_acquire`. That calls `NativeInstallationFence::try_acquire`, which captures `NativeInstallationRoot` and re-walks the whole chain with `inspect_directory_path` on every acquire, recheck and capture.
- **Uncharged.** It is not charged to any ledger. On a `/Users/<name>` home one acquire costs about 126k of the 131,072-edge cap (468 r4).
- **Omission read as "no writers".** It judges through `check_descriptor_observation`, whose `possible_acl_writers` come from `opensip_platform::observe_descriptor`. The macOS reader returns an empty writer list when `filesec_query_property` reports no ACL. So an omitted ACL reads as "no writers".

461 retires that reading at the single custody choke point. Once it does, `/` and `/Users`, which omit the ACL on a stock Mac (probe 457), refuse, and every read refuses with them. 458 §5 withheld Evidence B from existing consumers, so today nothing can admit them. This law gives the read side an admissible premise and a charged path, so that 461 can land.

## Decisions

1. **The receipt is `InitialPlatform` (owner decision, 2026-09-27).**
   - **What runs.** A read command that must open I produces the same receipts the creator produces, and only those:
     - `InitialInstallationAttempt::begin`, the process's one attempt, ledger and latch;
     - `InitialActor`, the 464 account predicate;
     - `produce_initial_core`: F0, then the running image, release authentication and revocation (463);
     - `produce_initial_platform`: profile authentication, process, boot, loader and H's `fstatfs`, the platform decision and Evidence B minting (462).
   - **What does not run.** No intent is minted, there is no storage choice, disclosure, preparation, permit, stage or effect, and no fence is taken. The attempt is the invocation's one charged act whether it creates or reads. A process that reads never calls `mint_intent`.
   - **One producer.** No second producer, reader-only variant, cached receipt or receipt from another process exists. The receipt is private, not Clone, not serializable, bound to the attempt's lineage, and dropped with the invocation. It grants no standing beyond item 2's.
   - **Which commands.** Only commands that read I produce it: the observation-only surfaces of owner §5 and `doctor`. Metadata-only commands keep their stronger no-installation-read boundary and never produce it (owner §5).
2. **What the read side borrows.** A sealed private capability, `ReadPremiseQualification`, is implemented only by `InitialPlatform`, in the same way as 468's `DurableBarrierQualification`. It lends exactly two things:
   - `is_home_filesystem`: the check that a filesystem is H's (462 item 4);
   - `omission_premise`: the `AclOmissionPremise`, if the receipt holds one.

   It lends no barrier policy, and no read path takes a barrier (owner §5). It cannot be built by a caller.
3. **Scope of the premise (owner decision, 2026-09-29).** Exactly 465 item 4's scope:
   - **Where it applies.** Root to H, `Library` and `Application Support`, and only through the premise's own `fstatfs` on each retained descriptor (`AclOmissionPremise::admits`).
   - **Where it never applies.** `OpenSIP`, I, the required files, project roots, operational files and private descendants.
   - **Without a premise.** An omitted ACL on any of the covered components refuses (`ParentRefusal::AncestorAclOmitted`). This replaces the root-to-H scope recorded in 468 item 9.
4. **Refusals when minting.** They use law 468 item 6's rows, with no new code:
   - F0 in a development build ends in `CORE.NO_EMBEDDED_RELEASE`, before any path is opened.
   - Other core refusals end in `NT-TCB-IDENTITY`.
   - Platform refusals end in their `NT-TCB-*` rows.
   - Account refusals end in `INSTALLATION.ACCOUNT_REFUSED`.
   - Budget refusals end in `WORK.BUDGET_EXHAUSTED`.

   An admitted receipt with no premise is not a refusal. That covers a BASELINE-ATTESTED host (469), a V1 profile, a row without `installAclOmission`, and a SYNTHETIC profile outside tests. Step 0 of item 5 then refuses at the first omitted component, on the custody row with subject `ancestor-acl-omitted`. This macOS 27 development host is such a host. The consequence is accepted as in 462 item 8.
5. **The observation path.** The observation path is 468 r5 items 3 and 4 without barriers. `InstallationObservation`, the successor of `InstallationReadFence`'s acquisition, runs:
   0. **Charged chain walk.** Walk from root to I with retained no-follow handles, under the 460/465 predicates and item 3's premise. H, `OpenSIP` and I must be on H's filesystem (`is_home_filesystem`). This is the same code as 468b step 0, shared rather than copied, except for how the end of the walk is classified:
      - **Positive absence.** The walk may end before I when a component of the fixed suffix (`Library`, `Application Support`, `OpenSIP`, `preview-v1`) is missing. That is a positive absence of I only when the first missing component is observed absent by a no-follow lookup under its retained, admitted parent. The observation returns a typed `ObservedAbsent { component }`, which routes to `INSTALLATION.NOT_INITIALIZED`.
      - **Not absence.** A non-directory, a symlink, a custody refusal, an I/O error or a budget failure at that name is never absence. Each takes its own item 6 row.
      - **H.** H itself must exist (owner §3), and it is never absence. Every H failure takes exactly the row the write gate gives it (468b's step 0 classification, mapped by 468c):
        - a missing H: the custody row;
        - an open refused by permission, or another I/O error: the host I/O row;
        - an H on a filesystem `is_home_filesystem` refuses: `NT-TCB-BOOT`, subject `INSTALL_ROOT_FS`.

        None of these is absence or an account refusal: `InitialActor` admits the UIDs and the home spelling, not the directory.
      - **The write gate** keeps its own classification.
   1. **Fence attempt.** Open `lifecycle.fence` no-follow through the retained I and judge it private. Then make one nonblocking exclusive attempt on that descriptor. `NativeInstallationFence::try_acquire` and `inspect_directory_path` are never called. Busy follows item 11.
   2. **Recheck.** Run 468 item 3's recheck set in full under the held fence:
      - the account;
      - the retained chain;
      - the I-parent name;
      - I and the fence's identity;
      - custody of I and the I-parent;
      - the required file owners.

      The required file owners limb covers each required file (the fence, `project-registry.v2`, `selection.pair`, the endpoint marker, its lineage node chain and the trust current record). Each must be owned by the invoking user, in private mode, with one link and a private ACL. In this first pass, the limb covers the fence and every required file already retained.
   3. **Member reads.** Each capture is charged before it runs: `capture_leaf`, `capture_descendant`, pair, marker, node chain and trust records. The fixed members are charged up front. Each lineage node is charged before its own read, because the chain's length is learned while reading it.
   4. **Recheck again.** Run the same full recheck set after the reads, and after any read failure. Its required-file-owner limb now covers every required file captured in step 3, each by the identity retained at its capture. Any recheck failure latches the session. A step 3 member that is missing, undecodable or wrongly linked is a structural finding (item 7), not a recheck failure.

   The session holds no barrier and no receipt of durability, and it cannot become a write capability (owner §5). A write needs a separately admitted operation through the 468 gate.
6. **Budget.** Each observation session has one failure-latching `WorkLedger` at the owner's caps (65536 objects, 131072 edges, 256 MiB), as 468b's gate does. It uses the same `WorkScope` / `work.run` / `ReservedPostchecks` idioms. The receipt's own work is charged to the attempt's ledger. A process gets one session, allocated like `DurableWriteGate::begin`. Name enumeration, captures and original-owner rechecks all use the session's ledger, with no branch-local reset (owner §7). A limit failure is unavailability, never absence or "no ancestor".
7. **Complete I and the doctor note.** I is complete only when the fence, `project-registry.v2`, `selection.pair`, the endpoint marker, its lineage node chain and the trust current record are all observed under one session (468 item 5).
   - **Doctor on a complete I** carries the informational `INSTALLATION.DURABILITY_NOT_CHECKED` entry, with owner §5's text. Only `doctor` carries it; `trust doctor` and `store status` never do.
   - **Slots.** The note takes one of the 256 slots. 255 actual defects plus the note is a report. With 256 actual defects the report refuses and latches, and is never truncated. `defectsFound` counts actual defects only, excluding that one code, and `DOCTOR.DEFECTS_FOUND` depends on that count.
   - **Other read commands** end an incomplete or contradictory I on 468's incomplete row: `CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`. The session latches.
   - **An absent I** ends on `INSTALLATION.NOT_INITIALIZED` only through step 0's `ObservedAbsent`.
8. **Consumers that move now.** Every production user of `InstallationReadFence::try_acquire` moves to `InstallationObservation`, keeping its capture API:
   - `host/src/installation_records.rs`, `installation_selection.rs`, `installation_lineage.rs` and `installation_trust.rs`;
   - `storage/src/store_root/native_marker.rs`;
   - `security/src/trust/native_read_session.rs`, together with the captures under it in `native_current.rs`, `native_record_capture.rs`, `directory_record_capture.rs`, `directory_name_scan.rs` and `native_profile_census.rs`.

   After the move, no production code path calls `NativeInstallationFence::try_acquire`. `NativeInstallationRoot::capture` and `SuppliedInstallationFence` remain only for supplied-root tests, until 461 decides them.

   Files under I keep `inspect_operational_file`. They carry the zero-rights owner allow of a private creation, so their ACL is present. Consumers outside I, such as project roots and `observe_bound_operational_file_with_policy` in `storage/src/store_root.rs`, are not given the premise (item 3). They stay with 461.
9. **What this sets up for 461.** After 458c-b, the only remaining root-to-H readers of the legacy writer list are gone. 461 can then map an omitted ACL to unreadable at `check_descriptor_observation`, the one choke point, without breaking any installation read. 461 still owns the other legacy readers:
   - `observe_bound_operational_file_with_policy`;
   - `path_binding` and `directory_binding`;
   - `FileLock::observe_descriptor`;
   - the `macos_loader` observations.
10. **Units after the law.** Each unit is reviewed by Grok with an inventory successor.
    - **458c-a:** `ReadPremiseQualification`; a library composition `produce_read_platform` (attempt, actor, core, platform, no intent); its termination mapping through 468c's `InstallationTermination`; tests on scratch homes with synthetic V2 profiles.
    - **458c-b:** `InstallationObservation`, with 468b's step 0 and step 1 factored into shared code, and every item 8 consumer migrated.
    - **458c-c:** the doctor complete-I note and the 255+1 rule on the existing `DoctorResult` shape, with no new envelope member.

11. **Busy on the read path (owner decision, 2026-09-29).** The observation session follows S7's level-0 row for the lifecycle fence.
    - **Pace.** It repeats the nonblocking attempt on the same retained fence descriptor, sleeping `FENCE_POLL` (25 ms, as in `lifecycle::leases`) between attempts. It stops after at most 5 s on the monotonic clock, and after at most 201 attempts: one attempt, then 200 retries.
    - **No re-walk.** There is no re-walk and no reopen.
    - **Reservation.** Before the first attempt, one reservation covers all 201 attempts at the gate's per-attempt lock cost. A reservation that cannot be made refuses before any attempt, on the budget row. Once made, the wait never ends in `WORK.BUDGET_EXHAUSTED`.
    - **Outcome.** Each attempt has three results, as `FileLock::try_acquire` does:
      - the lock: the session continues with step 2;
      - busy (`None`): wait and retry;
      - any other failure (`Err`): the wait stops at once, and the error is classified exactly as the write gate's lock step does (468b `lock_fence`, mapped by 468c). Every `Err`, including a carrier that is no longer a regular file, ends on the host I/O row: `HOST.IO_FAILURE`, `host-io`, exit 4. A carrier replaced by another file is caught by the step 2 recheck on the custody row.

      Only a lock still busy when the 5 s or the 201 attempts run out ends on the busy row: `LEDGER.BUSY_TIMEOUT`, `PROJECT.BUSY`, `ledger-busy`.
    - **The write gate** keeps 468's single attempt, which is stricter than S7 and still allowed.
12. **Doctor when it cannot reach I (owner decision, 2026-09-29).** If minting the receipt, the step 0 walk, the fence wait or a recheck refuses, `doctor` ends on 468 item 6's row like any read command, and no report is produced. That covers:
    - no embedded release;
    - a platform or account refusal;
    - an omitted ACL with no premise;
    - a custody refusal;
    - busy;
    - budget.

    **A reachable I that is incomplete or contradictory is not a refusal for doctor.** Owner §5 and `doctor-cases.json` govern that report unchanged:
    - Each structural finding from step 3 is an actual defect entry under the existing doctor defect classifications. This law adds no defect code, and it does not collapse the findings into one.
    - The informational note is absent, because I is not complete. The report keeps the existing 256-entry bound for reports without the note: 256 actual defects is a report, and 257 cannot be produced. That ends on `HOST.IO_FAILURE` / `DOCTOR.REPORT_NOT_PRODUCIBLE`, exit 4, and latches.
    - A doctor session does not latch on a structural finding. It still runs the step 4 recheck, and a recheck failure there ends on the item 6 row with no report.
    - Every other read command ends on the incomplete row (item 7).

## Forbidden substitutes

A second platform or core producer for reads; a cached, serialized or cross-process receipt; a caller-built premise or filesystem sample; the premise on `OpenSIP`, I, project roots, operational files or private descendants; `NativeInstallationFence::try_acquire` or `inspect_directory_path` on the observation path; an uncharged capture or recheck; a read session promoted to a write capability or used to skip the 468 gate; a barrier on a read path; the doctor note outside `doctor` or counted as a defect; truncating a report; a new public code.

## Not claimed

CLI enablement; 461's choke point; the non-installation legacy readers; any qualified boot identity (no measured row is checked in, and this host stays BASELINE-ATTESTED, so reads here refuse at `/` without a synthetic test profile); semantic complete-I joins beyond owner §7's structural completeness; a positive backup detector; changes to the 468 write gate.
