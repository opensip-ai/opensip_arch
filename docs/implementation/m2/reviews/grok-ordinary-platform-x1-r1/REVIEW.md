# Review: ordinary platform owner X1 r1

Verdict: ACCEPT.

Subject `docs/implementation/m2/ordinary-platform-x1/PROPOSAL.md` is 8758 bytes, sha256 `e47aff459a26d99b30faaf5380739987091c764cb3b7700ae71631dab860839b`, matching hashes.txt. The request names product `d1b5eda`. Live HEAD is `fdbedf4acc7ef57fb71eed424c3b08fa2af7fe98`, and the only change since `d1b5eda` is `design-lock.json` selecting 461b. The code below is that tree. No product cargo.

## Item 1

One composition is sound under 458c item 1. `produce_on` is the single producer of the attempt, the actor, `produce_initial_core` and `produce_initial_platform`. `produce_read_platform` already calls it and mints no intent. `produce_write_platform` is a second entry on that same composition, with purpose `Write`. 458c's ban is a second platform or core producer, which is the rejected `OrdinaryPlatform`. 468 item 2 is what left writers without a gate until this owner.

The purpose marker keeps the lendings apart. `DurableWriteGate::admit` takes `&impl DurableBarrierQualification`. `ReadPremiseReceipt::qualification` yields `&impl ReadPremiseQualification`, and that trait has no barrier policy. `ObservationSession::retain` and `observe_with` take `ReadPremiseReceipt` by value. `InitialPlatform` implements both sealed traits, and both receipts keep the platform private: the read receipt lends only `ReadPremiseQualification`, the write receipt lends only `DurableBarrierQualification`, and neither converts. A purpose mismatch does not compile, so it has no row. X1a's compile-fail pin is the right check. Both entries call `InitialInstallationAttempt::begin`, and a second `begin` stays `AlreadyAllocated` even after the first attempt is dropped, so one process produces one receipt.

## Item 2

The order is sound and the grant stops at `DurableInstallation`.

1. `produce_write_platform` uses `produce_on`, so a development build still ends at InitialCore F0 (`CORE.NO_EMBEDDED_RELEASE`) before any path is opened.
2. The receipt recheck is 458c-a's actor, core and platform recheck, charged on the attempt.
3. `DurableWriteGate::begin` then `admit` is 468 item 3 steps 0 to 5, with the gate's own ledger. `admit` borrows the qualification only for the walk, the barriers and the recheck set, and the returned `DurableInstallation` holds the fence, the chain, the required files and the two barrier receipts.
4. The receipt recheck runs again while that fence is held. `FileLock::release` consumes the guard. On a step 4 failure the law returns the recheck's item 6 row and releases the installation first, so the writer does not receive it. Drop also unlocks, and the explicit release is what makes the failure observable.

The gate's own steps 2 and 5 recheck the account, the chain, the names, the identities, the custody and the required file owners around the barriers, including after a failed barrier. The receipt rechecks are the platform and core standing at both edges. The creator route stays `run_initial_creator`: it drops the attempt inside `route` and passes `&InitialPlatform` to `admit`. 467 rechecks the actor, core and platform inside the creator act. This law leaves that route as 468c shipped it.

`OrdinaryWriteAdmission` holds that installation and the write receipt so the writer's later owner can recheck. 468 item 2's three lendings grant no standing. The admission adds no store, trust, project, id, grant or commit capability, and it has no conversion into a read session.

## Item 3

`host::installation_entry` matches the list. `NotInitializedWhenAbsent` is `import`, `baseline upgrade`, `repair apply`, `repair verify`, `test run` and `native prepare`. `CommandOwnerDecides` stays with each command's own owner. X1 wires no command. Owner §6's absence row is `REQUEST.PRECONDITION_FAILED` / `INSTALLATION.NOT_INITIALIZED`, which is `InstallationTermination::NotInitialized` and the host projection of that variant. `gate_refusal(GateRefusal::Absent)` is that variant.

The gate's step 0 calls shared `walk_chain` and maps every `Walked::Absent` to `GateRefusal::Absent`. Absence is the first missing fixed-suffix component observed with `ENOENT` under its retained parent (`Library`, `Application Support`, `OpenSIP`, or `preview-v1`). A file, symlink, custody refusal or I/O error at that name stays the walk's own refusal and takes that refusal's item 6 row. The ordinary path calls no creator, mints no intent, and creates no ancestor, I or stage.

## Items 4 to 7

Standing is the held fence and the confirmed durability of I's name and the I-parent's name. The two ledgers match the code: `WorkLedger::new` is the owner caps (65536 objects, 131072 edges, 256 MiB) for both the attempt and `DurableWriteGate`, and `admit` does not take a caller's ledger. Receipt work and the step 2 and step 4 rechecks stay on the attempt. Gate walk, fence, barriers and gate rechecks stay on the gate ledger.

The named maps exist: `attempt_error`, `actor_refusal`, `core_refusal`, `platform_refusal`, `gate_refusal` and `work`. `CORE.NO_EMBEDDED_RELEASE` and `INSTALLATION.NOT_INITIALIZED` are registry details and diagnostic routes, both `REQUEST.PRECONDITION_FAILED`, exit 2. No new code is introduced. A second `begin` of the attempt or the gate is the existing `Invariant` (`AlreadyAllocated`, or `GateRefusal::Latched`). A creator that reached `Published`, `LostRace` or `NotPristine` has already entered through `route` and does not call `admit_ordinary_writer`. A read entry (`InstallationReadFence::acquire` or `observe_installation_for_doctor`) has already taken the one attempt.

## Item 8

X1a is the receipt, `produce_write_platform`, the admission, the tests named in the law, and an inventory successor. X1b is the right conditional follow-up: it runs only if `read_premise.rs`'s description becomes stale once the write entry exists.

## Anything else

The forbidden substitutes match 458c, 468 and owner §5: no second producer, no cached or convertible receipt, no new implementor of either sealed trait, no intent and no creation on this path, no skipped recheck, no admission after a failed step 4, and no new public code. On this BASELINE-ATTESTED host a real ordinary writer still refuses at `/` without a synthetic profile, as 458c item 4 already accepted.
