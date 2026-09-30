# Review: read premise 458c r1

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of the read side's omission premise and the observation path. No repository edits and no product cargo. Product HEAD `7237f931ae78330243edc4de1e7d64daf1b50fd2` was read.

Subject `docs/implementation/m2/read-premise-458c/PROPOSAL.md`, 12514 bytes, sha256 `4e9b94f52d817ff631b997140bf874e08c25466f82349ddf740e8e1868e9c7dc`. The fence-free per-invocation receipt, the 465 item 4 scope, the 5 s busy wait, and doctor's refusal when the walk cannot reach I are owner decisions. This review judges how they are written.

## Verdict

**REQUIRED-FINDINGS.**

## What holds

Item 1 reuses `InitialInstallationAttempt::begin`, `InitialActor`, `produce_initial_core` and `produce_initial_platform`, and it mints no intent. That is the creator's receipt sequence through Evidence B, without storage choice, disclosure, preparation, permit, stage or effect. There is no second core or platform producer, no cached or cross-process receipt, and no standing past item 2. Metadata-only commands stay outside it, as owner §5 requires. A development build still ends at F0 before a path is opened.

Item 2's `ReadPremiseQualification` is sealed, implemented only by `InitialPlatform`, and lends `is_home_filesystem` plus `omission_premise`. It lends no barrier policy. `AclOmissionPremise::admits` samples that descriptor's own filesystem and admits a local, non-union type the premise carries. Item 3 limits the calls to root through H, `Library` and `Application Support`, which is 465 item 4 and 462 item 6, and it replaces the root-to-H sentence in 468 item 9. `OpenSIP`, I, the required files, project roots, operational files and private descendants stay outside the premise. An admitted receipt with no premise is a successful mint; the first omitted component then refuses as `ParentRefusal::AncestorAclOmitted`. On this BASELINE-ATTESTED host that is the 462 item 8 consequence.

Item 4 sends minting refusals through 468 item 6's rows and adds no public code. The busy row in item 11 names `LEDGER.BUSY_TIMEOUT`, `PROJECT.BUSY` and `ledger-busy`. The budget row remains `WORK.BUDGET_EXHAUSTED`. Other read commands keep the incomplete row, subject `installation-incomplete`, and a positive absence of I is the `INSTALLATION.NOT_INITIALIZED` row.

Item 5's walk, no-follow fence open, and private judgment of `OpenSIP` and I match 468 r5 items 3 and 4 with the barriers removed. `NativeInstallationFence::try_acquire` and `inspect_directory_path` stay off this path. Fixed members are charged up front. Each lineage node is charged before its own read, and a charge that fails is unavailability under item 6. The session holds no barrier and cannot enter the 468 gate. Item 6 gives the observation one failure-latching ledger at the owner's caps, with enumeration, captures and rechecks on that ledger.

Item 7's complete-I note matches owner §5 and `doctor-cases.json` for a complete installation. The code is the existing `INSTALLATION.DURABILITY_NOT_CHECKED`. Only `doctor` carries it. `trust doctor` and `store status` do not. `defectsFound` excludes that code, and `DOCTOR.DEFECTS_FOUND` follows the count. 255 actual defects plus the note produce a report. 256 actual defects on a complete I refuse and latch, and the report is not truncated. The owner's remedy text is incorporated. Item 12's first branch matches the settled decision: when minting or the step 0 walk refuses, `doctor` uses the same 468 row as any other read and produces no report.

Item 8's production holders of `InstallationReadFence` are the four host readers, `native_marker.rs`, and `native_read_session.rs`, plus the captures that already run under that session. At this HEAD the only production call to `NativeInstallationFence::try_acquire` is `InstallationReadFence::try_acquire`. The other call is the read-only factory test in `installation_fence.rs`. `native_census.rs` and `native_platform.rs` take a `SuppliedInstallationFence` from the session and do not acquire the native fence. `SuppliedInstallationFence` and `NativeInstallationRoot::capture` remain the supplied-root test path item 8 leaves to 461.

Item 9 matches the remaining legacy writer-list readers: `observe_bound_operational_file_with_policy` (it calls `inspect_directory_path`), `path_binding`, `directory_binding`, `FileLock::observe_descriptor`, and the `macos_loader` observations. The lifecycle lease crate opens `lifecycle.fence` on a supplied install handle and is not one of those readers. After 458c-b, 461 can refuse an omitted ACL at `check_descriptor_observation` without taking the installation read with it.

The S7 level-0 cell is a bounded 5 s wait on `<installRoot>/lifecycle.fence`, then `PROJECT.BUSY`. Item 11 uses that bound on the monotonic clock, repeats a nonblocking attempt on the same retained descriptor, and does not re-walk or reopen. The write gate stays at 468's single attempt. The attempt count inside those 5 s is RF-3.

## Required findings

### RF-1 — The observation recheck omits the required file owners

Owner §5 requires the observation path to recheck the original account, custody, the I-parent name, I, the fence, and the required file owners while the fence is held. 468 item 3's recheck set includes those owners: the fence, `project-registry.v2`, `selection.pair`, the endpoint marker, its lineage node chain and the trust current record, each owned by the invoking user, in private mode, with one link and a private ACL.

Item 5 step 2 cites that set and then states the set as the account, the retained chain, the I-parent name, I and the fence identity, and custody of I and the I-parent. Step 4 runs that same set after the member reads and after a read failure. The required file owners are in neither pass.

Failure scenario: the fence is held and the spelled rechecks pass. After `selection.pair` or a lineage node is captured, its owner, mode, link count or ACL changes. Step 4 does not look at that file again. The session accepts the capture and the command continues on bytes whose owner no longer matches the invoking user.

### RF-2 — An incomplete I makes doctor emit one defect

Owner §5 and `doctor-cases.json` keep a partial root on the 256-entry bound, with the informational note absent. `inherited-two-defects-no-notice` produces a report whose count is 2 and whose entry count is 2. `partial-capacity-no-notice` produces a report whose count is 256 and whose entry count is 256, exit 0. `partial-overflow` (257 actual defects) produces no report and exits 4. A report that cannot be produced stays `HOST.IO_FAILURE` / `DOCTOR.REPORT_NOT_PRODUCIBLE`. The owner allows a producible partial root to carry its actual structural defects.

Item 12 states that a reachable incomplete or contradictory I produces a report with one defect, `CONFIG.CUSTODY_REFUSED` subject `installation-incomplete`, and `defectsFound` 1. That is the whole report. Item 5 step 4 also latches the session on any failure, so a missing required file is both a latched failure and, for doctor, a report.

Failure scenario: doctor reaches I, the installation is missing two required members, and those members are the two structural defects in `inherited-two-defects-no-notice`. The published report has `defectsFound` 2 and two entries. Item 12 publishes one custody entry and `defectsFound` 1. A partial root with 256 actual defects, which `partial-capacity-no-notice` produces at exit 0, is likewise replaced by that single entry. A partial root with 257 actual defects, which must refuse at exit 4, is published as a one-defect report.

### RF-3 — Charging every busy retry spends the ledger before the 5 s row

Item 11 repeats a charged nonblocking attempt for at most 5 s and, when the lock is still absent, ends on 468's busy row. Item 6 sends a refused charge to `WORK.BUDGET_EXHAUSTED`. The current gate prices one nonblocking flock at 3 edges and 512 bytes (`LOCK_COST` in `installation_admission.rs`). The session edge cap is 131072. Item 11 states no interval and no maximum number of attempts.

Failure scenario: a writer holds the fence for the whole 5 s. The observation retries as fast as the nonblocking call returns, and each retry spends those 3 edges. The ledger reaches 131072 edges well inside the 5 s. Item 6 ends the command on `SYSTEM.OUTCOME.ILLEGAL_STATE`, `WORK.BUDGET_EXHAUSTED`, fault cause `host-invariant`. S7's level-0 result for that wait is `PROJECT.BUSY` on the busy row. The lifecycle crate's existing fence wait sleeps 25 ms between attempts, which stays near 200 tries and inside the cap. Item 11 does not bind the observation to a pace or a try cap that keeps the busy row reachable.

### RF-4 — The shared step 0 treats a missing ancestor as I's absence

Item 7 admits `INSTALLATION.NOT_INITIALIZED` only for a positive absence of I observed under the retained `OpenSIP`. Owner §5 forbids inferring pristine absence from a missing child. Item 5 step 0 uses the same code as 468b step 0, shared rather than copied. That function returns `GateRefusal::Absent` when the parent walk is not `FinalNamePresent`, when `Library`, `Application Support` or `OpenSIP` is missing, and when I itself is missing. 468c maps `Absent` only to `INSTALLATION.NOT_INITIALIZED`.

Failure scenario: `Application Support` is present and `OpenSIP` is absent. The shared walk returns `Absent` without retaining `OpenSIP` and without observing I. The read, including doctor, ends on `INSTALLATION.NOT_INITIALIZED`. Item 7 requires that row only after I was observed absent under a retained `OpenSIP`. A missing `Library` takes the same row. The write gate can keep its broader `Absent`. The observation path needs its own classification for an ancestor that ends before I.

## Not reopened

The fence-free per-invocation receipt, the 465 item 4 scope, the 5 s bound itself, and doctor's use of the ordinary 468 row when minting or the step 0 walk refuses, stand. The findings are the file-owner recheck, the partial doctor report, the unbounded busy retries, and the shared absence result.
