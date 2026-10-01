# The ordinary platform owner for writers that are not creators — proposal X1 r1

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X1 of EXIT-PLAN.md, under owner.md §5 ("Durable/write binding") and §6, and laws 462, 463, 468 r5, 458c r6 and 461 r3. Items 1, 2 and 5 contain lead decisions, made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation and record it. Not code. Library only: no command is wired (464 item 7; X10 and X11 own CLI enablement).

## Problem

Law 468 r5 item 2 lends the durable write gate its barrier policy, its H-filesystem check and its omission premise from "this same invocation's `InitialPlatform`, through a sealed private capability that only `InitialPlatform` implements". It closes: "Writers that are not creators get no gate until the ordinary platform owner exists (M2 exit)."

At d1b5eda the only way to obtain an `InitialPlatform` is inside `run_initial_creator`, which also mints the single-use creation intent. 458c-a showed the producers themselves need no intent: `produce_read_platform` runs the attempt, the actor, `produce_initial_core` and `produce_initial_platform`, and returns a private `ReadPremiseReceipt` lending only `ReadPremiseQualification`.

Every later writer needs to reach the gate without the creator's intent: store admission (X3a), commit (X3b to X3d) and the `NotInitializedWhenAbsent` commands. That includes the commit path the M2 exit matrix exercises.

## Decisions

1. **The receipt is the same receipt, typed by purpose (lead decision).** There is still exactly one producer composition: 458c-a's `produce_on` over the process's one `InitialInstallationAttempt`, `observe_actor`, `produce_initial_core` and `produce_initial_platform`.
   - **The type.** X1 generalizes the 458c-a receipt into one private, non-Clone, non-serializable `PlatformReceipt<P>`. `P` is a sealed purpose marker, `Read` or `Write`, fixed by the entry that produced it:
     - `produce_read_platform()` returns `PlatformReceipt<Read>`, which is 458c-a's `ReadPremiseReceipt` unchanged in behavior. Its only lending is `ReadPremiseQualification`.
     - `produce_write_platform()` returns `PlatformReceipt<Write>`. Its only lending is `DurableBarrierQualification`.
     - Neither receipt can be converted into the other. A process produces at most one, because the attempt is the process's one attempt.
   - **No widening.** `DurableBarrierQualification` stays implemented only by `InitialPlatform`, and lends exactly 468 item 2's three things. The write receipt lends its `&InitialPlatform` as `&impl DurableBarrierQualification` and nothing else. No new type implements either sealed trait, and no intent can be minted through either receipt: the attempt stays private to the receipt.
   - **Rejected alternative.** A separate `OrdinaryPlatform` producer would duplicate profile authentication, process, boot and loader checks and Evidence B minting. 458c item 1 forbids "a second platform or core producer", and the receipts would drift.
2. **The ordinary writer's admission (lead decision).** A library composition `admit_ordinary_writer()` runs, in order:
   1. `produce_write_platform()`. A development build ends at InitialCore F0 (`CORE.NO_EMBEDDED_RELEASE`) before any path is opened.
   2. The receipt's actor, core and platform rechecks (458c-a `recheck`).
   3. `DurableWriteGate::begin()`, then `admit(receipt.qualification())`: 468 item 3 steps 0 to 5 unchanged.
   4. The receipt's rechecks again, while the gate's fence is still held.

   Any failure at step 2 or 4 latches the attempt and ends on its item 6 row. A step 4 failure releases the admitted installation's fence before returning: the writer never receives it. On success the writer receives an `OrdinaryWriteAdmission`, which holds the `DurableInstallation` and the write receipt for later rechecks by the writer's own owner.

   Steps 2 and 4 bracket the gate because owner §5 requires "original account, custody, I-parent/name/I/fence and required file owners" to be rechecked around the barriers. The gate covers those, and the platform and core standing that lent the qualification must still hold at both edges. The creator path keeps 468c's route unchanged, since its creator act already rechecked them (467 item 1).
3. **Which writers, in M2.** In `host::installation_entry`, the ordinary writers are the `NotInitializedWhenAbsent` class (`import`, `baseline upgrade`, `repair apply`, `repair verify`, `test run`, `native prepare`), plus any `CommandOwnerDecides` command whose own owner later decides it writes. X1 enables none of them as a command. It provides the library entry that their units, and store admission and commit (X3a to X3d), call.
   - **Absent I.** When I is absent, an ordinary writer ends on `REQUEST.PRECONDITION_FAILED` / `INSTALLATION.NOT_INITIALIZED` (owner §6), through the gate's `Absent`. Since 458c-b1, the gate's `Absent` comes from the shared `walk_chain`. That is the positive absence of the first missing fixed-suffix component under its retained parent; a file, symlink, custody or I/O failure at that name takes its own row. An ordinary writer never creates I, an ancestor, or a stage.
4. **Standing.** `OrdinaryWriteAdmission` grants exactly what 468's `DurableInstallation` grants: the held installation fence and the confirmed durability of I's and the I-parent's names, for this invocation. It grants none of the following, each of which is its own unit:
   - store admission or a selected store (X3a);
   - trust admission;
   - project admission or leases (X2);
   - operational id reservation;
   - grants or live guards (X4);
   - a commit capability (X3d).

   It has no serialized form and no conversion into a read session, and it is dropped with the invocation.
5. **Budget (lead decision).** As for the creator path:
   - the receipt's work is charged to the attempt's ledger;
   - the gate's work to the gate's own ledger at the owner's caps (468 item 4);
   - the step 2 and step 4 rechecks to the attempt's ledger, each before it runs.

   **Rejected alternative.** One shared ledger would need the gate to accept a caller's ledger, which 468b deliberately does not.
6. **Refusal rows.** Every refusal uses 468 item 6, through 468c's existing per-family maps: `attempt_error`, `actor_refusal`, `core_refusal`, `platform_refusal`, `gate_refusal` and `work`. There is no new public code, row or subject. A receipt produced for one purpose and offered for the other cannot compile, so it has no row.
7. **One entry per process.** A process enters through exactly one of:
   - 468c's `run_initial_creator`, for the `Creator` class;
   - X1's `admit_ordinary_writer`;
   - 458c's read entries (`InstallationReadFence::acquire`, `observe_installation_for_doctor`).

   The process's one attempt (`InitialInstallationAttempt::begin`) and the one gate per process (`DurableWriteGate::begin`) already enforce this: a second entry ends as `Invariant`. A creator that published, lost the race or found I not pristine has already been routed through the gate by 468c. It does not call `admit_ordinary_writer`.
8. **Units after the law.**
   - **X1a.** The code, with an inventory successor:
     - `PlatformReceipt<P>`;
     - `produce_write_platform`;
     - `admit_ordinary_writer` and `OrdinaryWriteAdmission`;
     - tests on scratch homes with synthetic V2 profiles: success; dev-build F0; absent I with positive absence versus a non-directory; a step 2 and a step 4 recheck refusal, the latter with the fence released; busy; budget; the one-entry-per-process rule; and a compile-fail or type-level pin that a read receipt cannot reach the gate and a write receipt cannot reach the observation session.
   - **X1b.** A description-only contract successor, if `read_premise.rs`'s description becomes stale.

## Forbidden substitutes

A second platform or core producer; a cached, serialized or cross-process receipt; a receipt convertible between purposes; any new implementor of `DurableBarrierQualification` or `ReadPremiseQualification`; minting a creation intent, creating I, an ancestor or a stage on the ordinary path; reusing a creator handle, lock, receipt or observation; a caller-built premise, filesystem check or barrier policy; skipping either receipt recheck; returning an admission after a failed step 4 recheck; a new public code; wiring a command.

## Not claimed

CLI enablement of any writer; store, trust, project or id admission; grants and live guards; reading I's files under the held write fence (the writer's own owner, starting with X3a); commit; any qualified boot identity. This macOS 27 host stays BASELINE-ATTESTED, so a real ordinary writer here refuses at `/` without a synthetic test profile.
