# Read-only carrier recovery and the settlement sweep — proposal X6 r3

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X6 of `EXIT-PLAN.md`. It is written under:
- `architecture/commit-recovery-readonly.v3.md`, the bounded algorithm owner: steps 0–4, §1 vocabulary, §3 anchor bound, §4 sweep;
- identity-and-evidence's "Read-only recovery selectors" (`recover(ExecutionId)`: `SHARED-READ`, one snapshot, no fence acquisition, no wait on a writer);
- owner.md §5's internal recovery selector paragraph;
- the build plan's `RecoveredCommit` row (line 54) and failure cases F14, F15, F20–F29, F33–F37, F43–F53;
- the accepted laws X3d r3 (items 3, 6, 9 and 10), X3b r6, X3c r7, X3a r5, X2 (r6, item 7's read-only recovery exception), X1 r1 and 458c r6.

Items 1 to 9 contain lead decisions made under the owner's standing direction to proceed on the lead's recommendation; each names the alternative it rejects. r2 answers Grok X6 r1 RF-1 (the fence-free lease is now X2 r6's exception) and RF-2 (both projections of the degraded standing). r1 bytes are preserved in PROPOSAL-r1.md. r2 ACCEPTED by Grok on 2026-10-01.

r3 (2026-10-01) is an amendment from starting X6b, made as a lead decision under the owner's standing direction. As r2 stood, item 6 had the host call `recover` on X3d's `ExistingAttempt` in the writer's own invocation, and items 2 and 3 admit recovery on the read receipt. X1 r1 items 1 and 7 and 458c r5 item 1 allow a process exactly one attempt, one receipt and one entry, and the writer's receipt is already spent, so no process can do both (`ATTEMPT_ALLOCATED` at product 81214cb). r3 changes item 6: `ExistingAttempt` stays on X3d item 9's invariant row, discloses the requested binding, and is recovered only by a later read-entry invocation. Items 1, 2 and 3 settle what that needs: the recovery request's shape and owner, the binding X3d supplies with `ExistingAttempt`, the one read entry, and how admission picks N. Item 8 gains the unregistered-namespace row, and item 12's X6b is restated. Items 4, 5, 7, 9, 10 (except F34's line) and 11 are unchanged. r2 bytes are preserved in PROPOSAL-r2.md. Not code. Library only: no CLI command is wired; the `repair recover` CLI surface is not this selector.

## Problem

The algorithm is fully specified by its owner document, and most of its pure parts exist at 7e676a9:
- `storage::recovery` holds `ReceiptCandidate`, `AssociationCandidate`, `DecimalCounter` and `join_ledger`, which implements the settlement matrix over supplied same-snapshot rows;
- `ledger_store` holds a private `ReadSnapshot` and the `AttemptCustodyV1` row reader;
- the journal read side holds `reconcile_observations`.

What is missing:
- an admission that obtains the binding without the fence;
- the bracketed carrier capture of step 3;
- the anchor and quarantine rules of steps 3 and 4 as code;
- a `RecoveredCommit` result;
- the routing of X3d's `ExistingAttempt` and `CommitUndetermined`;
- the writer of the §4 sweep.

X6 decides ownership, API, locks and units. It does not redesign the algorithm.

## Decisions

1. **Owners (lead decision).**
   - **Security** owns the read-only carrier capture: the five-observation bracket, closed witness-shape validation, the anchor table and the step 4 quarantine rule, in a new `journal_store::recovery_capture`.
   - **Storage** owns `recover` and `RecoveredCommit` in `recovery.rs`: admission, the one ledger snapshot, the §2 matrix through the existing `join_ledger`, the SEAL join and availability, and the composition with security's capture. It also owns the sweep's single settle write in `ledger_store`.
   - **Host** owns routing only: X3d's `ExistingAttempt` and, through X7, `CommitUndetermined`; and `store-gc`'s per-namespace sweep step.

   This matches the build plan (storage `recovery.rs`; `RecoveredCommit` is "storage recovery result validated against current ledger and objects") and keeps carrier rules in their security owner (S6, S9). **Rejected:** carrier rules in storage, which would duplicate X3b's owner.

   **r3: the custody half of admission is security's.** Item 3's steps (the read receipt, the walk, the registry and endpoint reads, the fence-free lease and the recheck) use security-private owners: the receipt, 458c's walk, X2b's registry capture, X3a's endpoint values and X2d's lease carriers. So `RecoveryAdmission`, `RecoveryRequest` and `RequestedBinding` are security types, as `CommitSession` is (X3d item 1). Storage's `recover` consumes the admission. Storage owns everything after it, as above. **Rejected:** moving security's walk, registry and lease owners into storage, which would give storage custody it cannot own.

2. **The API (lead decision).**
   - `RecoveryAdmission::admit(receipt: &mut ReadPremiseReceipt, request: RecoveryRequest) -> Result<RecoveryAdmission, RecoveryRefusal>`.
   - `recover(admission: RecoveryAdmission) -> RecoveredCommit`.

   `RecoveryRequest` carries the ExecutionId, and, for F34, the full requested binding that X3d supplies: store generation digest, namespace, journal carrier digest and operation reference.

   **r3: the request and its binding (lead decision).**
   - **`RequestedBinding`** is a public, inert security value: `storeGenerationDigest` (64 lowercase hex), `namespaceId`, `journalCarrierDigest` (64 lowercase hex) and `operationRef` (the physical `op-` grammar). Its one constructor checks those grammars and nothing else. It grants nothing and admits nothing.
   - **What X3d supplies.** `prepare_commit`'s outcome becomes `NotPrepared::ExistingAttempt { execution_id, requested: RequestedBinding }`. Storage builds `requested` from the plan it was about to write (the session's N, the digest of (N, S, G, K), the carrier digest and the operation reference), never from a read. No other `NotPrepared` or `CommitOutcome` variant changes.
   - **`RecoveryRequest`** has two checked constructors: one from an ExecutionId and a namespace id (a plain recovery, such as X7 item 5's later recovery of a `CommitUndetermined`), and one from an ExecutionId and a `RequestedBinding` (F34). The namespace id is a selector only (item 3 step 3).
   - **The read entry.** Recovery is one of X1 item 7's read entries. The public `RecoveryAdmission::admit(request)` produces the process's one read receipt (458c-a's `produce_read_platform`) and then runs item 3 on it. The crate-private form taking `&mut ReadPremiseReceipt` is the signature above, kept for tests over synthetic receipts. A process that has already entered (the creator, an ordinary writer or another read entry) refuses with the `Invariant` row at receipt production, as X1 item 7 already says.
   - **Rejected:** a public `ReadPremiseReceipt`, which would expose the attempt-holding receipt outside security; and a request whose namespace comes from the ExecutionId by scanning every namespace's ledger, which is unbounded and is not the selector.

   `RecoveredCommit` is a closed, private-constructor enum of exactly the §1 standings:
   - `CommittedHistorically { runId, pendingSettlement, legacyCustodyUnknown, confirmedUnderRetainedCustody, availability }`;
   - `CommittedAvailabilityDegraded`;
   - `TerminalNotCommitted`;
   - `UnknownAttemptOpen` and `UnknownAttemptUnobserved`;
   - `UnknownCustody`;
   - `UnknownQuarantineCondition { reason }`;
   - `UnavailableBusy`;
   - `BindingUnusable { subject }`;
   - `UnknownCarrierIncompatible`.

   Every confirming result carries `interior-bodies-not-authenticated` (§3).

   **Rejected:** a boolean "committed" result, or folding unknowns into an error type. Both let a caller read absence into an unknown.

3. **Admission without the fence (lead decision).** The read-only recovery selectors take `SHARED-READ` and "no fence acquisition and no wait on a writer" (identity §5; owner §5 excludes this selector from the fenced binding path). The steps:
   1. **Receipt.** Produce the read receipt (458c-a, X1 `<Read>`). On this BASELINE-ATTESTED host it refuses at `/` without a synthetic test profile, which is the same accepted consequence as 458c. (r3) This is the process's one entry (item 2); a writer's invocation can never reach it.
   2. **Walk.** Run 458c's charged retained walk from `/` to I (step 0). Its fence attempt, 458c step 1, is **not** taken.
   3. **Binding reads.** Through those retained handles, read the registry (X2b's single bounded capture) and X3a's endpoint files (pair, marker, the node chain, `state.v1`), with full metadata samples. Take N from the registry's ACTIVE row and (S, G, K) from the endpoint, never from request fields.
      - **(r3) Which row.** The request's namespace id only selects. The registry must hold exactly one row with that `namespaceId`, and its status must be ACTIVE. N is that row's own `namespaceId`. No row, a row in any other state, or more than one row is the unregistered-namespace refusal (item 8), before any lease. The digest of (N, S, G, K) and the carrier digest SHA-256(N) are computed from the admitted values only; a `RequestedBinding` is never an input to them, only compared with them (item 6).
      - **Rejected:** the project-root admission of X2 items 1 to 6, which runs under the fence through a `FenceHolder`, and which this selector may not take.
   4. **Lease.** Take `readers.lease` `LOCK_SH|LOCK_NB` for N, without the fence. This is X2 r6 item 7's one exception to "no lease without the fence"; it never takes `writer.lease` and is never upgraded. Busy, meaning an EXCLUSIVE holder such as the sweep, returns `UnavailableBusy`.
   5. **Recheck.** Recheck the registry and endpoint samples once after the lease. Any change is `UnavailableBusy`, never a conclusion.

   The binding is used only to compare against the association and the carrier; it allocates nothing. **Rejected:** admitting through 458c's `ReadSession`, which takes the fence and waits up to 5 s for it, both of which the selector forbids.

4. **Order: exactly the owner's algorithm.** After admission:
   - Step 1: one coherent ledger snapshot (`ReadSnapshot`) reading the receipt, the association, the Run manifest, object references, availability, pins and `AttemptCustodyV1` together.
   - Step 2: the settlement matrix through `join_ledger`. The association's binding against the admitted binding gives `BindingUnusable` (F27).
   - Step 3: security's bracketed capture `W1 H1 J W2 H2`, the §1 carrier precedence, the SEAL join at `k`, and the anchor table, with at most one fresh capture.
   - Step 4: the five stable observations before any quarantine.
   - Then availability (the `evidence.*` family) for a confirmed receipt.

   The bounds are those of the owner: one ledger snapshot, at most two journal snapshots, four witness reads and four floor reads. The whole path performs no write, no witness INIT/REVERT/ADVANCE, no floor raise, no quarantine marker, no repair and no wait. A missing, empty or fallback ledger or carrier is never absence (F24).

5. **Budget (lead decision).** Recovery owns one failure-latching `WorkLedger` at the owner's caps (65536 objects, 131072 edges, 256 MiB), one per process, allocated like 458c's session. The walk, binding reads, ledger snapshot, carrier captures and object availability checks are all charged before they run. The read receipt's own work stays on its attempt ledger. A limit failure maps to the budget row and is never absence. **Rejected:** sharing X3d's operation ledger, which belongs to a writer that may still be live.

6. **Routing from X3d (lead decision; r3).**
   - **F34, `ExistingAttempt { executionId, requested }`.** It is never recovered in the writer's invocation: that process has spent its one attempt and receipt on the write entry, and cannot make a read entry (X1 items 1 and 7). So:
     - **In the writer's invocation.** The outcome stays on X3d item 9's invariant row (`SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `HOST.INVARIANT_VIOLATED`), the row X3c item 10 gives a reused ExecutionId. A fresh CSPRNG ExecutionId cannot collide on a lawful first attempt, so the row is honest. Finalization (X7 r4 item 3) discloses the ExecutionId as the subject and the four members of `requested` beside the row, with a remedy naming a later read-only recovery with that binding. No `INSERT OR REPLACE`, no new SEAL, no read of the existing attempt.
     - **In a later read-entry invocation.** `recover` is admitted on a `RecoveryRequest` carrying that ExecutionId and that `RequestedBinding` (item 2). Admission picks N only from the single ACTIVE registry row the request's namespace selects (item 3 step 3). After the one ledger snapshot, the requested binding is compared exactly with the admitted one: its `storeGenerationDigest` with the admitted (N, S, G, K) digest, its `namespaceId` with N, its `journalCarrierDigest` with SHA-256(N), and its `operationRef` with the attempt row's `operation_ref` in that snapshot. Any difference, or no attempt row to compare the operation with, is `BindingUnusable` (`RECOVERY.REFUSED`) with the first differing member as the subject (`store-generation`, `namespace`, `carrier` or `operation`). The same binding gives whatever standing the attempt has.
     - **This supersedes r2's routing**, and with it X3d item 9's "before X6 exists": the invariant row is the writer's permanent projection of `ExistingAttempt`. X3d item 3 step 5's "for the host to route to read-only recovery" is met by the disclosure and the later invocation.
   - **F12/F40, `CommitUndetermined`.** X3d keeps the `attempt_custody` row `admitted`. X7 r3 item 5 already decided: finalization never calls `recover` in the same invocation, which this law's read-entry rule now also requires. A later invocation recovers it with a plain `RecoveryRequest` (the ExecutionId and the namespace id finalization discloses, X7 r4 item 5). A stopped session never calls `recover` itself and never settles.

   **Rejected:**
   - settling from the writer path, which the owner forbids (§5, "A stopped cleanup-only session may not write it");
   - (r3) handing the spent write receipt back from `StoppedSession::finish` so that recovery can admit on it in the writer's invocation. It would change X3d item 7's end path and X1 item 1's purpose rule (a write receipt lending the read qualification) for an outcome no lawful first attempt reaches;
   - (r3) recovering before `finish` under the operation's live session, which would read under a writer's authority and its lease.

7. **The sweep: exactly what it writes, and under which lock (lead decision).**
   - **Where.** It is a per-namespace step of the existing `store-gc` command (`owner: security`, `requestClass: lifecycle`, `authorizationClass: exclusive-lease`).
   - **How it gets the namespace.**
     1. X1 `admit_ordinary_writer`, which holds the installation fence through the 468 gate.
     2. For each registered N, X2's EXCLUSIVE lease primitive: `writer.lease` then `readers.lease`, each `LOCK_EX|LOCK_NB`, under that fence. A busy namespace is skipped and retained, never refused.
     3. One `ReadSnapshot` reading the receipt, association and custody row together.
     4. A decision per the §4.2 table, through the same `join_ledger`.
   - **What it writes.** Exactly one statement, in one `BEGIN IMMEDIATE` transaction with the ledger's own durability (WAL, FULL, `fullfsync`):
     `UPDATE attempt_custody SET phase='settled', settled_outcome=? WHERE … AND phase='admitted'`,
     with `?` being `committed` or `refused` only. The existing monotone trigger refuses a second settle.
   - **When it writes nothing.** A busy lease, an unreadable ledger, a one-sided ledger (F23), or a row already settled.
   - **What it never does.** It writes nothing else: no receipt, association, SEAL, witness, floor, trust record or grant. It reuses no dead attempt's authority, obtains no execution grant, takes no X4 guard and never retries a commit.
   - **Release.** Each namespace's leases are released in reverse order before the next namespace. The fence is released last.
   - **Orphan objects.** Their removal ("the existing reachability GC") does not exist in the product. It is **not** implemented by X6 (see Not claimed). The sweep leaves orphan objects in place, which the owner allows: orphans "may" be removed.

   **Rejected:** writing `undetermined` (the owner's C14 flaw), and settling without the EXCLUSIVE lease.

8. **Refusal rows.** These are the §1 projection exactly, with no new code:

   | Standing | Projection |
   |---|---|
   | `committed-historically` | success |
   | `committed-availability-degraded` | Two projections, exactly as §1: for history, success; when a selected operation requires an object that is unavailable, operational-failed / `HOST.IO_FAILURE` / `host-io` with detail `evidence.missing`, `evidence.corrupt`, `evidence.purged` or `evidence.expired` for that object. `recover` reports the standing with the per-object availability; the selected operation's owner applies the second projection. A required unavailable object is never reported as success. |
   | `terminal-not-committed` | success |
   | `unknown-attempt-open` and `unavailable-busy` | `LEDGER.BUSY_TIMEOUT` / `ledger-busy` / `PROJECT.BUSY` |
   | `unknown-attempt-unobserved`, `unknown-custody` and `unknown-carrier-incompatible` | `HOST.IO_FAILURE` / `host-io` |
   | `unknown-quarantine-condition` | `LEDGER.CORRUPT` / `ledger-corrupt`, no detail |
   | `binding-unusable` | request-rejected / `EXTENSION.ADMISSION_REJECTED` / `RECOVERY.REFUSED` with a typed subject |

   - **Admission refusals** (receipt, walk, registry or endpoint) take their 458c and 468c item 6 rows.
   - **(r3) An unregistered namespace** (item 3 step 3) is a refused recovery request: request-rejected, `EXTENSION.ADMISSION_REJECTED`, detail `RECOVERY.REFUSED`, subject `namespace-unregistered`. This is owner §1's "`RECOVERY.REFUSED` for a refused recovery request"; no code or detail is added.
   - **Budget** takes the `WORK.BUDGET_EXHAUSTED` row.
   - **Sweep:** an unreadable ledger reports host I/O for that namespace and continues to the next.

   `MIGRATION.CORRUPT` appears on no read-only path.

9. **Carrier formats 1 and 2 (lead decision).** M2 carriers are freshly created format 3 only (X3b r6). X6 still classifies a format-1 or format-2 carrier, or an association below `first_generation`, as `UnknownCarrierIncompatible` (F46), because the open dispatch exists and the classification is read-only. Migration and its interrupted states (F47, F48, F50 and F51's migrated case) stay outside M2, because no migration writer exists. A format-unaware core opening a migrated carrier (F51) cannot occur without a migration. **Rejected:** omitting F46, which would turn an inherited carrier into `unknown-custody` and lose the owner's distinction.

10. **Failure cases.**
    - **Covered:**
      - F14 and F15 (read side);
      - F20 to F25 and F27;
      - F28, read side: a pruned journal record is `unknown-custody`;
      - F29;
      - F33;
      - F34 (binding comparison, in a later invocation; r3);
      - F36, read side: an orphan SEAL is never confirmed;
      - F37: the private ordering accessor, `DecimalCounter`, tested at 0, 2, 9, 10, 100 and `u64::MAX`, rejecting leading zeroes, negatives and over-range values;
      - F43 to F46;
      - F49: deterministic interleaving tests here; real concurrent processes in X9;
      - F52 and F53.
    - **Not covered:** F35 (store migration and restore lineage: no migration writer in M2); F47, F48, F50 and F51 (carrier migration).

11. **Tests.**
    - **Fixtures.** Scratch installations built with X3b's and X3c's test-only fixtures and X4T-0's signed store, on synthetic V2 profiles.
    - **Matrix.** Each of the eleven F52 matrix cells.
    - **Anchors.** Each anchor case, A, B, C and C′, plus the adverse rows.
    - **Precedence.** Each §1 carrier precedence row.
    - **Hazard.** The F43 hazard, with and without the retry reconciling it.
    - **Stability.** The F49 stability rule, through a `cfg(test)` capture hook that mutates the witness, floor or tail between bracket reads. A lawful later append never yields a quarantine.
    - **Sweep.** Every §4.2 row, including a busy namespace skipped and an already-settled row unchanged.
    - **Pins.** A source pin shows:
      - `recover` reaches no write statement;
      - the sweep's only write is the settle `UPDATE`;
      - neither calls the fence or a writer lease from `recover`.
    - **Real crash and concurrency runs** in fresh processes belong to X9.

12. **Units.**
    - **X6a (security).** `journal_store::recovery_capture`: the bracket, shape validation, anchor table, step 4 rule and the carrier precedence observations, all read-only. It depends on X3b-1b.
    - **X6b (security, storage and host; r3).** Security: `RequestedBinding`, `RecoveryRequest` and `RecoveryAdmission` (items 1 to 3; the read entry, the walk without the fence, the registry and endpoint reads, X2 r6's fence-free SHARED-READ, the recheck), and the recovery-side carrier location constructor from that admission. Storage: `recover` and `RecoveredCommit` (items 4, 5 and 8), and `NotPrepared::ExistingAttempt`'s `requested` binding (item 6). Host: the read-entry route that admits a `RecoveryRequest`, calls `recover` and projects the `RecoveredCommit` on item 8's rows. X9 r1's `after-lease` and `after-ledger-snapshot` points. It depends on X6a, X3c-1, X2b, X2d and X3a-1, and on X3d-2 for the association writer's exact shape. Finalization's disclosure of `ExistingAttempt` is X7's (X7 r4 item 3).
    - **X6c (storage and host).** The sweep's settle write in `ledger_store` and the `store-gc` per-namespace step. It depends on X6b, X1 and X2d's EXCLUSIVE lease primitive.

## Forbidden substitutes

A negative conclusion from anything but `settled` + `refused` with both rows confirmed absent in one snapshot; a conclusion assembled from two ledger snapshots or from independently timed observations; a liveness probe or in-memory active set; a fence acquisition or writer-lease wait in `recover`; (r3) `recover` called in a writer's invocation, a receipt of any purpose but `<Read>` admitting recovery, N taken from a request field or from more than one registry row; any write on the recovery path (witness, floor, quarantine marker, attempt row); a binding taken from request fields; a quarantine report without the five stable observations; a stopped session settling its own row; a sweep that writes `undetermined`, writes without EXCLUSIVE, writes for a busy, unreadable or one-sided namespace, or writes anything besides the settle transition; reusing a dead attempt's authority or retrying its commit; `MIGRATION.CORRUPT` on a read-only path; a new public code.

## Not claimed

Orphan object garbage collection (the "existing reachability GC" does not exist in the product; F02 to F06's "later authorized reconciliation may remove orphans" stays open); carrier-format migration and its read paths (F35, F47, F48, F50, F51); real concurrent-process and crash execution (X9); CLI enablement, including `repair recover`; prefix authentication beyond retained custody (§3: a selected limit, not a gap).
