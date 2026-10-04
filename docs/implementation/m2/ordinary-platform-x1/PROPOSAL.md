# The ordinary platform owner for writers that are not creators — proposal X1 r2

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X1 of EXIT-PLAN.md, under owner.md §5 ("Durable/write binding") and §6, and laws 462, 463, 468 r5, 458c r6 and 461 r3. Items 1, 2 and 5 contain lead decisions, made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation and record it. Not code. Library only: no command is wired (464 item 7; X10 and X11 own CLI enablement). ACCEPTED by Grok X1 r1 on 2026-09-30.

**r2 (2026-10-04) is an amendment: J1's successor S3.** It changes items 1 and 7, the last sentence of item 2, and item 8's units. r1 bytes are preserved in PROPOSAL-r1.md (sha256 `d747adf0…`, 8,796 bytes). That copy keeps r1's acceptance sentence. Without that sentence, its bytes are the subject Grok accepted (sha256 `e47aff45…`, 8,758 bytes; `reviews/grok-ordinary-platform-x1-r1/review.json`). **Draft r2, not accepted.** Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the autonomous run. Not code.
- **Its source.** J1 r5, the accepted host-pipeline law, cited as J1 (`docs/implementation/m3/host-pipeline-j/PROPOSAL-r5.md`, sha256 `4ccb2320…`; accepted by Codex, `m3/reviews/codex-host-pipeline-j-r5`). Its successor row S3 gives this law "items 1 and 7 (item 3); the read receipt with or without a session (item 6)" (J1:848). J1 item 3 states the amendments (J1:280-284).
- **What it changes.**
  - Item 1: J1's durable creator-class entry is a third producing entry. It fixes the Write purpose after J1's presence probe and before any receipt exists, so no receipt converts.
  - Item 7: one exception to one entry per process, the creator-class sequence, with a two-slot attempt allocation and a `CreatorActEnded` token. The 458c read receipt is a lawful use of the process's one attempt, with or without a session. The `Creator` class enters through J1's durable entry.
  - Item 2: its last sentence, on the creator path, follows item 7 (LD2-3).
  - Item 8: the code is J1 unit J3a's.
- **What it does not change.** The two receipt types and their lendings, item 2's steps, standing, budget, refusal rows, the forbidden substitutes and "Not claimed". No public code, row or subject is added.
- **Unchanged from r1:** everything else. No accepted outcome of r1 or of another law changes, except as S3 declares.

**r2 changes.**

| # | Change | Where | Source |
|---|---|---|---|
| 1 | **A third producing entry.** J1 item 3's durable entry runs the producers on attempt A, then the presence probe. On `Present` it seals them as `PlatformReceipt<Write>` and runs item 2's steps 2 to 4. On `PositivelyAbsent` they serve the creator act and are dropped with it. | item 1 | J1:247-262, :280 |
| 2 | **At most one receipt per process,** with the reason restated. On the creator-class sequence the composition runs on attempt A and on attempt B. | item 1 | J1:247, :256-261; LD2-1 |
| 3 | **The creator-class sequence.** One creator act on attempt A, then exactly one `admit_ordinary_writer` on attempt B, allowed only after `Published`, `LostRace` or `NotPristine`. A two-slot attempt allocation and a `CreatorActEnded` token. Any other second allocation stays `Invariant`. One gate per process. | item 7 | J1:281-283, :309, :320 |
| 4 | **The `Creator` class's entry** is J1's durable entry. 468c's M2 composition is no longer an entry. | item 7 | J1:185, :278-281, :301; LD2-2 |
| 5 | **The read receipt, with or without a session** | item 7 | J1:284, :442, :453 |
| 6 | **Item 2's creator sentence** follows item 7 | item 2 | J1:279-281; LD2-3 |
| 7 | **Units:** J3a | item 8 | J1:881 |

**r2 lead decisions.** Each is made under the owner's standing direction of 2026-09-30, where J1's text leaves a point open. Each names the alternative it rejects.
- **LD2-1. A process still produces at most one receipt.** r1 says so "because the attempt is the process's one attempt", which is no longer true on the creator-class sequence. On J1's route 3b, the intent is minted on attempt A (J1:258), and item 1 lets no intent be minted through a receipt ("No widening"). So attempt A's producers serve the creator act unsealed, and attempt B's `produce_write_platform` makes the process's one receipt.
  - **Decision.** Keep the rule and restate its reason.
  - **Rejected:** dropping the sentence. It is what keeps a read receipt and a write receipt from coexisting in one process.
- **LD2-2. The `Creator` class enters through J1's durable entry.** r1's item 7 names 468c's `run_initial_creator` as the `Creator` class's entry. J1 makes its durable entry that class's entry (J1 item 4, rows R2 and R3). It rejects the M2 composition, which mints an intent and runs the creator act on every call (J1:301), and 468 r6 item 1 withdraws its route, which enters the gate with the creator's own `InitialPlatform`.
  - **Decision.** Item 7's first entry is J1's durable entry. `run_initial_creator` stays `pub(crate)` and defined once (J1's control J-C1, J1:185). How J3a reuses its creator act inside the durable entry is J3a's.
  - **Rejected:** listing both. A process could then enter through the M2 composition, which J1 item 3 rejects.
- **LD2-3. Item 2's last sentence follows item 7.** S3 names items 1 and 7. Item 2's last sentence says "The creator path keeps 468c's route unchanged". After S2 and S3 the creator path has no route of its own to the gate.
  - **Decision.** Amend that one sentence to point to item 7. Item 2's steps are unchanged.
  - **Rejected:** leaving it. It would contradict item 7 (r2) and 468 r6 item 1.

## Problem

Law 468 r5 item 2 lends the durable write gate its barrier policy, its H-filesystem check and its omission premise from "this same invocation's `InitialPlatform`, through a sealed private capability that only `InitialPlatform` implements". It closes: "Writers that are not creators get no gate until the ordinary platform owner exists (M2 exit)."

At d1b5eda the only way to obtain an `InitialPlatform` is inside `run_initial_creator`, which also mints the single-use creation intent. 458c-a showed the producers themselves need no intent: `produce_read_platform` runs the attempt, the actor, `produce_initial_core` and `produce_initial_platform`, and returns a private `ReadPremiseReceipt` lending only `ReadPremiseQualification`.

Every later writer needs to reach the gate without the creator's intent: store admission (X3a), commit (X3b to X3d) and the `NotInitializedWhenAbsent` commands. That includes the commit path the M2 exit matrix exercises.

## Decisions

1. **The receipt is the same receipt, typed by purpose (lead decision).** There is still exactly one producer composition: 458c-a's `produce_on` over the process's one `InitialInstallationAttempt`, `observe_actor`, `produce_initial_core` and `produce_initial_platform`. **(r2)** On item 7's creator-class sequence the process has two attempts, A and B, and the same composition runs on each (J1:247, :261).
   - **The type.** X1 generalizes the 458c-a receipt into one private, non-Clone, non-serializable `PlatformReceipt<P>`. `P` is a sealed purpose marker, `Read` or `Write`, fixed by the entry that produced it:
     - `produce_read_platform()` returns `PlatformReceipt<Read>`, which is 458c-a's `ReadPremiseReceipt` unchanged in behavior. Its only lending is `ReadPremiseQualification`.
     - `produce_write_platform()` returns `PlatformReceipt<Write>`. Its only lending is `DurableBarrierQualification`.
     - Neither receipt can be converted into the other. A process produces at most one. **(r2; LD2-1)** On item 7's creator-class sequence, attempt A's producers serve the creator act unsealed and are dropped with it, so only attempt B produces a receipt.
   - **(r2, J1 S3) A third producing entry: the durable creator-class entry.** J1 item 3's durable entry (`enter_durable_analysis`; the name is J3a's) uses the same producer composition: `produce_on` over the process's attempt A (J1:247). It then runs J1's presence probe (J1:249). It fixes the Write purpose after the probe and before any receipt exists, so no receipt converts (J1:280).
     - On `Present`, it seals attempt A's producers as `PlatformReceipt<Write>`, with no intent and no disclosure, and runs item 2's steps 2 to 4 on that receipt. The result is an `OrdinaryWriteAdmission`, from one attempt and one gate (J1:256).
     - On `PositivelyAbsent`, attempt A's producers serve the creator act and are never sealed as a receipt. The invocation reaches the gate only through item 7's creator-class sequence (J1:257-262).

     It never produces a `PlatformReceipt<Read>`.
   - **No widening.** `DurableBarrierQualification` stays implemented only by `InitialPlatform`, and lends exactly 468 item 2's three things. The write receipt lends its `&InitialPlatform` as `&impl DurableBarrierQualification` and nothing else. No new type implements either sealed trait, and no intent can be minted through either receipt: the attempt stays private to the receipt.
   - **Rejected alternative.** A separate `OrdinaryPlatform` producer would duplicate profile authentication, process, boot and loader checks and Evidence B minting. 458c item 1 forbids "a second platform or core producer", and the receipts would drift.
2. **The ordinary writer's admission (lead decision).** A library composition `admit_ordinary_writer()` runs, in order:
   1. `produce_write_platform()`. A development build ends at InitialCore F0 (`CORE.NO_EMBEDDED_RELEASE`) before any path is opened.
   2. The receipt's actor, core and platform rechecks (458c-a `recheck`).
   3. `DurableWriteGate::begin()`, then `admit(receipt.qualification())`: 468 item 3 steps 0 to 5 unchanged.
   4. The receipt's rechecks again, while the gate's fence is still held.

   Any failure at step 2 or 4 latches the attempt and ends on its item 6 row. A step 4 failure releases the admitted installation's fence before returning: the writer never receives it. On success the writer receives an `OrdinaryWriteAdmission`, which holds the `DurableInstallation` and the write receipt for later rechecks by the writer's own owner.

   Steps 2 and 4 bracket the gate because owner §5 requires "original account, custody, I-parent/name/I/fence and required file owners" to be rechecked around the barriers. The gate covers those, and the platform and core standing that lent the qualification must still hold at both edges. **(r2; LD2-3)** The creator path has no route of its own to the gate. After the creator act, the invocation reaches the gate through `admit_ordinary_writer` on attempt B, so steps 2 and 4 run there too (item 7; 468 r6 item 1).
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
   - **(r2; LD2-2)** J1 item 3's durable creator-class entry (item 1), for the `Creator` class. 468c's `run_initial_creator` composition is no longer an entry;
   - X1's `admit_ordinary_writer`;
   - 458c's read entries (`InstallationReadFence::acquire`, `observe_installation_for_doctor`). **(r2, J1 S3)** The 458c read receipt, `PlatformReceipt<Read>`, is a lawful use of the process's one attempt with or without a session (J1:284). J1's ephemeral request uses it with no session when I is positively absent (J1:442, :453).

   The process's one attempt (`InitialInstallationAttempt::begin`) and the one gate per process (`DurableWriteGate::begin`) already enforce this: a second entry ends as `Invariant`. **(r2)** The one exception is the creator-class sequence below.

   **(r2, J1 S3) The creator-class sequence** (J1:281-283). Inside the durable creator-class entry, one creator act runs on attempt A. Then exactly one `admit_ordinary_writer` runs on attempt B. The sequence is allowed only after the creator act ended `Published`, `LostRace` or `NotPristine`.
   - **The attempt.** The attempt allocation (`crates/security/src/initial_installation.rs:28`, `:96-99`) becomes a two-slot sequence. A non-Clone `CreatorActEnded` token is returned only by the creator act, and consumed only by attempt B's allocation. Any other second allocation stays `Invariant`, and so does a third (J1's control J-C6, J1:320). Attempt B without `CreatorActEnded` is forbidden (J1:309).
   - **The gate.** There is still one gate per process (`crates/security/src/custody/installation_admission.rs:801`). The creator act enters no gate (468 r6 item 1), so attempt B's admission takes the process's one gate.
   - **What crosses.** No creator observation, handle, lock or receipt reaches attempt B (J1:307). Only 468 r6 item 1's value-only `created` record does.
   - **A refused creator act** returns no token. No attempt B follows, and the invocation ends on the refusal's 468 item 6 row (J1:273).
8. **Units after the law.**
   - **X1a.** The code, with an inventory successor:
     - `PlatformReceipt<P>`;
     - `produce_write_platform`;
     - `admit_ordinary_writer` and `OrdinaryWriteAdmission`;
     - tests on scratch homes with synthetic V2 profiles: success; dev-build F0; absent I with positive absence versus a non-directory; a step 2 and a step 4 recheck refusal, the latter with the fence released; busy; budget; the one-entry-per-process rule; and a compile-fail or type-level pin that a read receipt cannot reach the gate and a write receipt cannot reach the observation session.
   - **X1b.** A description-only contract successor, if `read_premise.rs`'s description becomes stale.
   - **(r2) J3a.** J1 unit J3a carries r2's code: the third producing entry, the two-slot attempt allocation and `CreatorActEnded`, with J1's tests J-C5 to J-C9 (J1:881).

## Forbidden substitutes

A second platform or core producer; a cached, serialized or cross-process receipt; a receipt convertible between purposes; any new implementor of `DurableBarrierQualification` or `ReadPremiseQualification`; minting a creation intent, creating I, an ancestor or a stage on the ordinary path; reusing a creator handle, lock, receipt or observation; a caller-built premise, filesystem check or barrier policy; skipping either receipt recheck; returning an admission after a failed step 4 recheck; a new public code; wiring a command.

## Not claimed

CLI enablement of any writer; store, trust, project or id admission; grants and live guards; reading I's files under the held write fence (the writer's own owner, starting with X3a); commit; any qualified boot identity. This macOS 27 host stays BASELINE-ATTESTED, so a real ordinary writer here refuses at `/` without a synthetic test profile.
