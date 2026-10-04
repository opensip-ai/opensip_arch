# The durable grant-journal append, its witness, the carrier high-water and grant-generation rollover — proposal X3b r11
 r4 was ACCEPTED by Grok on 2026-09-30. r5 is an amendment found by Grok's X3c r1 review: on the SEAL path, level 4 is held through the evidence COMMIT, so no REV can slip between SEAL and commit. r4 bytes are preserved in PROPOSAL-r4.md. r6 answers Grok r5 RF-1 (the SEAL-path hold had no release when COMMIT is never called) and RF-2 (the r4 snapshot now equals the accepted bytes). r5 bytes are preserved in PROPOSAL-r5.md. r6 ACCEPTED by Grok on 2026-09-30; r6 bytes are preserved in PROPOSAL-r6.md.

**r7 (2026-10-01) is an amendment required by the accepted X7 r3** (item 6 and its dependency note). It defines grant-generation rollover inside item 4's end step, under the fence that step already holds. It covers the `EXCLUSIVE` closure, the `TERMINAL` append and its `op-` token, the opening of generation g+1 with its crash states, the floor write for g+1, skip-if-busy, and the charge to the attempt ledger. It also reconciles X3d r3 item 3's capacity threshold with what the carrier admits.
- **New:** item 4a (generation succession: the closed generation, the opened successor, the effective tail, the predecessor check), item 5a (the capacity window and the exact rollover trigger) and item 13 (the rollover operation).
- **Amended:** items 3 (step 4's last table row), 4 (start and end), 5 (the `TERMINAL` bullet), 6, 8, 9, 10, 11 and 12, the forbidden substitutes and the not-claimed list.
- **Unchanged from r6:** everything else.

**r8 (2026-10-01) answers Grok X3b r7 RF-1 to RF-3.** r7 bytes are preserved in PROPOSAL-r7.md. r8 ACCEPTED by Grok on 2026-10-01.
- **RF-1 (item 5a, item 11).** `RA`, `REV` and `CLN` are admitted only when t ≤ `9007199254740989`, so the appended `seq` is at most `9007199254740990`. This matches carrier-format.v3 §5 and X3b-2's `LAST_ORDINARY_SEQ` check. `GenerationFull` at t = `9007199254740990` stays on the busy row. The `SEAL` ceiling, the `TERMINAL` window and the trigger are unchanged. Item 11's boundary test now covers both sides.
- **RF-2 (item 13, item 11).** An observed open tail below the exhaustion's `provenTailSeq` refuses before any write, even inside the window. It refuses as floor regression when the floor is ahead of that tail, and as `uncertainTailLoss` otherwise. The `TERMINAL` row runs only when the observed tail is in the window and at least `provenTailSeq`. A test covers a restore that leaves the tail at `…988` or `…989` with `provenTailSeq` `…990`.
- **RF-3 (item 13, item 11).** When the open generation is `9223372036854775807`, item 13's observation refuses on item 8's invariant row before any write, and no `TERMINAL` is appended. Item 13's table gains that row, and item 11 gains its test.
- **Unchanged from r7:** everything else.

**r9 (2026-10-01) answers two law problems found while implementing X3b-4** (its r1 review request, judgment calls 3 and 13). r8 bytes are preserved in PROPOSAL-r8.md. r9 ACCEPTED by Grok on 2026-10-01. It is reviewed together with X3d r5, which makes the matching change on the commit path.
- **A floor at the open successor (item 4a's floor-regression bullet; items 3 and 13 cite it).** When the witness names the open successor (case 1, OK or REVERT), a floor exactly at (G+1, 0, null) is unchanged, not regression. Read literally, item 3 compared it with the copy tail L, which on case 1's REVERT is the closing `TERMINAL` in G, and quarantined a lawful state for good. Every other floor is compared as before.
- **No reconciliation in the same operation after an uncertain outcome (items 4, 4a, 5, 9, 11, 12 and 13, and the forbidden substitutes).** The attempt ledger is the platform's failure-latching `WorkLedger`. The failure after visibility closes it, so r8's in-operation reconciliation ("reconcile once" in item 13, X3b-2's reconciliation in item 5) was refused before it read anything and could never run. r9 withdraws it. The operation reports durability-undetermined, copies no floor, and the next writer's floor step and start reconcile, as they already do after a crash at the same point. Item 5 records the decision and the rejected alternatives. No platform change is made.
- **Unchanged from r8:** everything else, including item 9's reserved cost (r9 only clarifies what its reconciliation line covers), every crash table and every refusal row.

**r10 (2026-10-01) is an amendment required by X3d r6**, which is reviewed together with this revision. r9 bytes are preserved in PROPOSAL-r9.md. r10 ACCEPTED by Grok on 2026-10-02.
- **What X3d r6 decides.** The end path's `REV` and `CLN` after a certain refusal that closed the attempt ledger are funded by a settlement reserve in `WorkLedger`, from platform unit X3d-0.
  - It is taken once, before the first attempt effect, in the same attempt ledger, at the exact cost of those two appends.
  - It is spendable after the latch, but only by X3d's `finish`, for those two appends.
  - It is never refilled, and it is forfeited at any uncertain outcome (X3d r6 item 8).
- **Item 5.** r9's rejection of a post-failure allowance for the reconciliation stands. Its reasons are restated so that they do not contradict X3d r6. The reconciliation buys nothing the next writer does not already do, while F19 requires this invocation to record the `REV`, and no later writer can. The settlement reserve cannot fund a reconciliation. Step 7's F19 sentence names the funding.
- **Item 4.** The end step also ends at step 1 when the attempt ledger is closed when the operation ends. Its first step is charged, so it would be refused `Closed` before any effect.
- **Items 9, 10, 11 and 12, and the forbidden substitutes,** record the same: the funding, the tests, X3b-3's share, and the bars on spending the reserve for anything else.
- **Unchanged from r9:** everything else, every crash table and every refusal row.

**r11 (2026-10-04) is J-RW r4's successor RW-S4, made as a lead decision under the owner's standing direction of 2026-09-30.** r10 bytes, as accepted (sha256 `25a60824…`, without the acceptance sentence), are preserved in PROPOSAL-r10.md. **Draft r11, not accepted.** Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the autonomous run. Not code.
- **Its source.** J-RW r4, the accepted resume/repair writer law, cited as JRW (`docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md`, sha256 `9c53bce7…`; accepted by Codex, `m3/reviews/codex-resume-repair-jrw-r4`). Its successor row RW-S4 reads "Item 2: C-ACL for `trust/carrier-floors/` under the fence (X3B:52). Item 12: unit J4a." (JRW:682). The rule is JRW item 3.1, C-ACL (JRW:219-240), for JRW's state RW-P3 (JRW:432). X3B:NNN in JRW is r10's line, preserved in PROPOSAL-r10.md.
- **Item 2.** A `trust/carrier-floors/` that a crash left empty and without its owner allow is completed with that allow at the floor step, under the fence. Today it refuses on the host I/O row for every project of the installation.
- **Item 12.** J-RW's unit J4a carries the code and its tests.
- **Lead decision LD11-1: where the completion runs.** At the floor step's judgment of the existing `trust/carrier-floors/`: under the held fence, with no project lock, after the busy probe and the carrier classification, and before the floor is read (`carrier_floor.rs:837-844` at product `d2c00a9`). A busy probe skips the floor step, and the completion with it, so the skip still writes nothing.
  - **Rejected:** completing before the busy probe, which would write trust state on a step that v8's skip rule says writes nothing; and completing only at a floor write, which would leave the floor step's earlier judgment refusing first.
- **Unchanged from r10:** everything else. That includes the floor step's order, its busy probe and its table, every crash table, every refusal row, the forbidden substitutes and the not-claimed list. No new public code, row, detail or subject.

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X3b of `EXIT-PLAN.md` (DR-G19, COV-03), under owner.md §8, security-and-lifecycle S6 (linearization, commit-admission gate), S7 (lock order and modes) and S12, `security-completion.v8.md` §5.4 to §5.6 (the grant-journal carrier, lock handoff, witness, durability primitives), the selected physical carrier `design-corrections/security/grant-journal.carrier.v3.sql` (carrierFormat 3, S1 row 84), `host-foundation-completion.v2.md` (project namespace layout), the build plan's failure cases F06 to F11 and F19, and laws X1 r1, X3a r3, X2 r4 (items 5 to 7a: R0, R1, R2, X2d's lease, X2e's handoff), X4 r2 (`OperationGuard` inside X2e; the checkpoint under `JournalAppendLock`) and X4T r1; r7 is also written under X3d r3 (items 3, 7 and 8), X7 r3 (items 6, 6a and 7), X1 r1 item 5, `carrier-format.v3.md` §5, §7 and §8, and v8 §5.4's WA-13. r2 answers Grok X3b r1 RF-1 (no floor write under a lease), RF-2 (the digest's preimage), RF-3 (no writer quarantine marker; the F46 row) and RF-4 (floor before witness). r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok X3b r2 RF-1 (format dispatch before the floor table) and RF-2 (the floor table implements the crash list and reconciliation; a whole INIT floor). r2 bytes are preserved in PROPOSAL-r2.md. r4 answers Grok X3b r3 RF-1 (a present non-INIT floor with no carrier is `uncertainTailLoss`). r3 bytes are preserved in PROPOSAL-r3.md. r4 ACCEPTED by Grok on 2026-09-30. It keeps X2 r5 item 7's ordering (the floor step runs under the fence before any lease) and X4T r2's fenced admission at the same point. Items 1, 2, 3, 4, 4a, 5, 5a, 7, 9 and 13 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Not code. Library only: no command is wired.

## Problem

M2's commit path appends a `SEAL` to the project's grant journal under the level-4 append lock, between the object barriers and the evidence-ledger commit. The journal's write side does not exist at f7acb6d:
- `security/src/journal_store.rs` and `journal_store/` hold the read side only: the closed schema-3 `JournalRecord` parser, the carrierFormat 3 DDL (`CURRENT_CARRIER_DDL`), carrier dispatch, historical rows, generation population, the bracketed capture and the generation-anchor judgment, with `Witness` and `CarrierFloor` decoders. Nothing creates a carrier, appends a record, writes a witness or copies a high-water.
- No level-4 append lock exists, though X4 r2 item 3 runs the authority checkpoint under it.
- `lifecycle/src/journal_store.rs` (lifecycle transition records) is a different owner (COV-03, DR-G18, M5) and is not this unit.

## Decisions

1. **Where the N-bound binding is produced (lead decision): X2e.** X2 r4 item 7a's handoff already joins the Eligible row's N and X3a's `SelectedStoreEndpoint` under the held fence, by moving owners. The owner §8 five-field binding `{schemaVersion:1, namespaceId:N, storeInstanceId:S, storeGeneration:G, stateSchema:K}` is derived there, from those moved owners only, and becomes a field of `ProjectOperation`. X3b consumes `ProjectOperation`; it never derives N or (S, G, K).
   - **Required composition with X2.** Two X3b steps run inside X2's one fence hold:
     - item 3's **floor step**, under the fence with no project lock held, after the Eligible row (R0) or the first registration's ACTIVE row (R2) and before X2 r4 item 7 (X2d) takes the lease;
     - item 4's **carrier start**, inside X2e's handoff after the join and before the fence is released (X2 r4 item 7a step 3).

     X2e composes both (X3b-3), and X2 records the ordering when it is next revised.
   - **Rejected:** producing the binding in X3b, which would need N and the endpoint after the fence is released, reversing the lock order owner §8 forbids.

2. **Location and format (lead decision).** The carrier is exactly the selected physical carrier, at exactly the host-foundation locations, under the namespace directory X2 publishes (`I/host/projects/N/`, X2 r4 item 6):
   - `grant-journal.sqlite`: carrierFormat 3, the bytes of `grant-journal.carrier.v3.sql` as embedded in `CURRENT_CARRIER_DDL`, WAL, with `synchronous=FULL`, `fullfsync=ON`, `checkpoint_fullfsync=ON` and foreign keys on (§5.6). Its WAL and shm sidecars are in the same directory.
   - `grant-journal.witness.json`: the closed v8 witness `{witnessSchema:1, projectKeyDigest, grantGeneration, seq, state, bodySha256}`, encoded by the existing `Witness` encoder.
   - **The carrier floor (SC-TRUST high-water):** `I/trust/carrier-floors/N.v1`, the existing `CarrierFloor` shape `{highWaterSchema:1, projectKeyDigest, grantGeneration, lastSeq, tailSha256}`. It is outside the namespace so that a namespace rollback cannot roll it back (§5.4), it is written only under the fence (S7: trust state is never written under a lease), and N is the path component (host-foundation: neither projectKey bytes nor its digest is a path component). `trust/carrier-floors/` is created on first need under the fence with 465 item 3's create-or-admit rules and barriers.
     - **(r11, JRW RW-S4) Completing an interrupted creation (C-ACL; JRW item 3.1, state RW-P3).** A crash between the directory's exclusive creation and its zero-rights owner allow leaves `trust/carrier-floors/` empty, `0700`, with its ACL omitted. Today every later floor step refuses it on the host I/O row (`carrier_floor.rs:237`, `:841-844` at `d2c00a9`), and that blocks every project of the installation.
       - **Where.** Item 3's floor step, where it judges the existing directory (LD11-1): under the held fence, with no project lock held, after the busy probe and the carrier classification, and before the floor is read. It is a trust-state write under the fence, never in the namespace and never under a lease (S7). No read path completes it.
       - **The predicate, P-ACL.** On the retained directory, all of these hold: it is at its fixed name, on its parent's filesystem; it is owned by the invoking user, with mode exactly `0700`; its ACL is omitted (`CapturedAclState::NotReturned`; a NOACL sentinel, an inconsistent capture or a present ACL is not omission); and it holds no entry but `.` and `..`, by one bounded scan.
       - **Action.** Append exactly one zero-rights owner allow and sample again, through the fresh path's own step (`prepare_fresh_private_sample`). The new sample must judge private, or the step refuses on today's row; the allow stays. Then the owner's remaining steps run unchanged: exact name, filesystem, the directory's own barrier and its parent's. The floor step then continues.
       - **Never.** No deletion, rename, mode change or other ACE. Every other shape keeps the host I/O row (JRW N-P1): a directory that holds a floor file or any other entry, the wrong owner or mode, another filesystem, a symlink, or a present non-private ACL.
       - **No new row.** X3b's host I/O row no longer arises from this state (JRW:508).
       - **Budget.** Charged to the gate's ledger before it runs, with its post-effect confirmations reserved (JRW:514).
       - **Owner.** J-RW's unit J4a (item 12, r11).
   - **Only the fresh path.** X3b creates and opens carrierFormat 3 carriers only. A namespace's carrier is created by its first operation (item 3), so no carrierFormat 1 or 2 carrier can exist under an X2 namespace. Any non-format-3 object found is refused (item 8); migration (F46 to F51) stays out of M2, per EXIT-PLAN.
   - **The carrier digest's preimage (RF-2; lead decision).** Registry owner v2 has no projectKey. The carrier's `projectKeyDigest`, in the `carrier_format` row, the witness and the floor, is exactly `SHA-256(N)`, where N is the ACTIVE row's `namespaceId` as its canonical lowercase UUID text, UTF-8 encoded with no prefix, separator or terminator. N is taken from `ProjectOperation`'s row snapshot (X2 r4: R0 for an Eligible root, R2 after first registration). The product open's `project_key` string argument is that N text; the member names `projectKeyDigest` and `project_key_digest` are kept as the selected carrier and witness schemas spell them, and no historical projectKey is selected or invented.
     - **Why N:** the carrier lives in `I/host/projects/N/` and is bound to that namespace for its lifetime; N is immutable, never reused, and survives a same-N move (registry owner v2), so the digest names the carrier and nothing else.
     - **Rejected:** `projectId` (distinct from N, and a carrier must not follow a project to a different namespace), and any domain-separated preimage (it would break the selected carrier's existing open comparison and fixtures for no gain).
   - **Rejected:** a carrier under the store (it would follow store reselection, which the journal must not) or a floor inside the namespace (§5.4's rollback detection would be void).

3. **The floor step: the only floor write at operation start (RF-1, RF-4; lead decision).** The floor is trust state, so it is written only under the fence and never while this process holds a project lease (S7; S1 records v8 §5.4's handoff as refined by that sentence). The floor step runs under the held fence, before X2d takes the lease:
   1. **Probe.** Take `writer.lease` LOCK_EX|LOCK_NB and release it at once. If it is busy, another writer is admitted: skip the floor step entirely (v8's skip rule), write nothing, and continue; X2d will then report the busy row. If the probe succeeds, no writer can append until this fence hold ends, because a lease needs the fence (S7). No project lock is held for the rest of the step.
   2. **Observe, read-only.** Read the floor for N (positively present, or positively absent under the retained `trust/carrier-floors/`), and in the namespace the carrier, its committed tail from one read snapshot, and the witness bytes. Nothing in the namespace is written here.
   3. **Format dispatch first (RF-1).** The carrier is classified by the existing carrier dispatch before any floor decision, whether or not a floor is present:
      - **absent**, or an **empty database** holding no schema objects: no carrier;
      - a **complete carrierFormat 1 or 2** carrier: the F46 row (item 8), whatever the floor;
      - a **carrierFormat 3 footprint that is not a lawful durable prefix** (partial object set, definitions not byte-equal, rows before the format row, a violated generation boundary): the migration-footprint row (item 8);
      - a **complete carrierFormat 3** carrier: its `project_key_digest` must equal the lowercase hex of `SHA-256(N)`, or the carrier project-binding row.

      A present floor is decoded as the whole closed `CarrierFloor` and its `projectKeyDigest` must equal the same digest, or the binding row. Each refusal writes nothing.
   4. **Floor decision, in this table order (RF-2).** "Witness" means the witness file is present; it is decoded by the closed shape where a row says so.

      | Floor | Carrier (after step 3) | Witness | Action |
      |---|---|---|---|
      | absent | none | absent | **floor-first INIT:** write the whole INIT floor `{highWaterSchema:1, projectKeyDigest: hex SHA-256(N), grantGeneration:1, lastSeq:0, tailSha256:null}` |
      | absent | complete format 3 | any | `floorLost` |
      | absent | none | present | `floorLost` |
      | present | none | absent, and the floor is `grantGeneration 1, lastSeq 0` | INIT resumes under the lease (item 3a); nothing is written |
      | present | none | any witness state other than the INIT row above: a witness is present, or the floor is anything but `grantGeneration 1, lastSeq 0` (for example generation 2 at `lastSeq 0`) | `uncertainTailLoss` |
      | present | complete format 3 | any | run `reconcile_witness`, with item 4a's successor rule (r7), **as a decision only** (item 4's table, read-only; the witness is not written here). A QUARANTINE outcome (`witnesslessRestore`, `witnessMalformed`, `uncertainTailLoss`, protocol violation, carrier mismatch) refuses and leaves the floor untouched. An INIT outcome (empty journal, no witness) requires the floor to be `grantGeneration 1, lastSeq 0`, else `uncertainTailLoss`; nothing is written and item 3a finishes INIT. An OK, REVERT, ADVANCE or OPEN (r7, item 4a) outcome then compares item 4a's copy tail with the floor, subject to item 4a's open-successor exception (r9): a lower generation or a lower sequence in the floor's generation, or an equal sequence with a different body hash, is floor regression. Otherwise the floor is copied forward to the committed tail only if the tail is higher; it never moves down |

      The committed tail is the last committed row; REVERT and ADVANCE concern only the witness, so the copied tail is the same either way. On a closed generation (r7) the copied tail is item 4a's copy tail, which on an OPEN outcome is the closing `TERMINAL` row. The witness write that REVERT, ADVANCE or INIT needs is performed later by the carrier start under the lease (item 4).
      Writes use item 5's file protocol under `trust/carrier-floors/`, with the fence held and no project lock held.

   **Rejected:** r1's floor writes at creation, start and end while the lease was held (S7), and r1's witness-before-floor creation order, which made a crash between them indistinguishable from a deleted floor (RF-4). Floor first makes "floor absent" always mean "never published" when the namespace holds no carrier and no witness, and "lost" otherwise.

3a. **Carrier creation (INIT), under the lease.** Only when the floor step found the floor present at `lastSeq 0` (just written or found) and the namespace holds no carrier (absent or an empty database) and no witness. It runs in X2e under the held fence and the operation's EXCLUSIVE or APPEND-WRITE lease; it writes only namespace files, never trust state:
   1. Create `grant-journal.sqlite` exclusively (no replace; an empty database left by a crash is reused only if it holds no schema objects), set the pragmas, then in one `BEGIN IMMEDIATE` transaction apply the DDL and publish the `carrier_format` row (fresh path: `first_generation` 1, no migration fields, `project_key_digest` per item 2). `COMMIT`; then the file's and the namespace directory's barriers. SQLite DDL is transactional, so the database holds either no schema objects or the complete set and its row.
   2. Write the witness `COMMITTED 0` (`bodySha256` null) by item 5's file protocol.

   **Crash states**, each found by the next floor step and carrier start:
   - floor 0, no carrier, no witness: INIT resumes;
   - floor 0, empty database, no witness: INIT resumes at step 1;
   - a complete format-1 or format-2 carrier, with or without a floor: the F46 row;
   - floor 0, complete carrier with its row and an empty journal, no witness: INIT finishes at step 2;
   - floor 0, complete carrier, witness `COMMITTED 0`: created;
   - a complete carrier whose journal holds a record, with no witness: `witnesslessRestore`;
   - a complete format-3 carrier or a witness present with the floor absent: `floorLost` (floor step);
   - a partial format-3 object set: impossible by step 1; if observed, item 8's migration-footprint row.

4. **Carrier start and the end step (the §5.4 handoff, refined by S7).**
   - **Start, inside X2e, under the fence and the lease:** open the carrier through the retained namespace handle; validate the format row's `project_key_digest` against `SHA-256(N)` (a mismatch is the carrier project-binding row); read the tail and the witness; run `reconcile_witness` (§5.4 table: INIT, OK, REVERT, ADVANCE, QUARANTINE), whose REVERT, ADVANCE and INIT write only the witness in the namespace; confirm the tail still equals the floor step's observation (nobody could append in between, since the probe succeeded and the fence has been held throughout); capture the start tail for X4's epoch binding. The carrier start writes no floor. Only an authorized writer (APPEND-WRITE or EXCLUSIVE) reconciles; read-only diagnosis (X6) only reports `would-REVERT` or `would-ADVANCE` (F07, F10).
     **r7.** The start applies item 4a. On a closed generation it performs OPEN, which writes only the witness, as INIT does. The tail it confirms against the floor step's observation is the committed tail, which OPEN does not change. The start tail it returns, which X4 binds and `JournalAppendLock` follows, is item 4a's effective tail. X6 also reports `would-OPEN`.
   - **End (the only other floor write):**
     1. Release the operation lease (S7 end rule).
     2. Take the fence by the shared charged walk and no-follow fence open (458c-b1's helpers, with S7's bounded 5 s wait).
     3. **Rollover (r7).** Only when the operation's outcome was X3d's `CarrierCapacityExhausted` and every journal outcome of the operation was certain, run item 13's rollover under this fence. It takes and releases its own `EXCLUSIVE` lease and returns with no project lock held. A skip or a failure is disclosed and never stops the steps below.
     4. Probe `writer.lease` LOCK_EX|LOCK_NB. If it is busy, another writer was admitted after us and its start observed a tail at or above ours: skip the copy, release the fence, end.
     5. If the probe succeeds, read the committed tail and the witness from one observation, release the probe lock, then write the floor to item 4a's copy tail if it is higher, under the fence with no project lock held. The end step reads the witness and never writes it.
     6. Release the fence.

     The end step reuses this invocation's write receipt and gate admission; it takes no second gate (one per process). Its only effects are item 13's namespace effects under item 13's own lease, and this floor write with its own barriers. A failure at end is disclosed and never rewrites the operation's outcome.

     **r9: after an uncertain outcome the end step copies nothing** (item 5).
     - After an uncertain journal outcome of the operation itself, the end step ends at step 1. X3d's `finish` releases the lease and takes no fence (X3d r5 item 7).
     - After an uncertain rollover (item 13, run at step 3), steps 4 and 5 do not run, and step 6 releases the fence.

     In both cases nothing is read and the floor is untouched. The next writer's floor step copies it.

     **r10: the end step on a closed attempt ledger.** If the attempt ledger is closed when the operation ends, the end step ends at step 1 as well. A certain refusal may have closed it, or X3d's end-path settlement may have failed (X3d r6 items 7 and 8).
     - **Why.** Step 2's fence walk is the end step's first charge. It would be refused `Closed` before any effect, so the step is not attempted. X3d's `finish` makes that decision.
     - **What it leaves.** The floor stays where the floor step put it, the state that process death after step 1 leaves. The next writer's floor step copies it forward.
     - **No disclosure.** A step not attempted is not an end failure, and nothing is disclosed for it.
     - **Not funded by the settlement.** X3d's settlement reserve never funds the end step, the rollover or a floor copy.

4a. **Generation succession: the closed generation and the opened successor (r7; lead decision).**
   - **What a generation is.** Physically, a grant generation is exactly the `grant_journal_v3` rows carrying its `grantGeneration`. The `carrier_format` row is immutable, and `first_generation` stays 1 on the fresh path. Generation g+1 has no row until its first record. That record is at `seq` 1, and its `prev_sha256` is the genesis value for (N, g+1): `genesis_prev` with N as the key text, per item 2. So **opening g+1 writes no carrier row.** Opening is two things:
     - the witness `COMMITTED {grantGeneration: g+1, seq: 0, bodySha256: null}`, written in the namespace under a writer lease;
     - later, under the fence with no project lock held, the floor `{grantGeneration: g+1, lastSeq: 0, tailSha256: null}`.

     Both closed shapes already admit these values.
     - **Rejected:** a marker row opening g+1. `TERMINAL` is the only record type without grant-bearing members, and it closes a generation. Any other type would fabricate an operation.
     - **Rejected:** a new carrier file per generation. Item 2 fixes one carrier per namespace, and §8's dispatch reads one carrier.
     - **Rejected:** a `carrier_capacity_pause` row. It is an inherited side table, and item 8 already forbids writer-stored markers. Every open re-derives exhaustion from the tail.
   - **The effective tail.** Let L be the committed tail as r6 defines it: the last row of the newest generation G, or the empty tail of `first_generation`.
     - **L is not a `TERMINAL`:** reconcile against L, exactly as r6 does.
     - **L is a `TERMINAL` at (G, s, h):**
       1. **The witness is present, has the closed shape and names G+1.** Reconcile against the successor's empty tail (G+1, 0, none) by the unchanged §5.4 table:
          - `COMMITTED 0` is OK: the successor is open;
          - `PENDING 1` is REVERT: the witness becomes `COMMITTED (G+1, 0)`;
          - every other state is QUARANTINE by that table. For example, `COMMITTED n` with n > 0 is `uncertainTailLoss`.
       2. **Any other witness** (absent, malformed, naming G, or naming any other generation). Reconcile against L:
          - **OK** (`COMMITTED s h`) **or ADVANCE** (`PENDING s h`) is **OPEN**. The `TERMINAL` is durable, so the one action is to write the witness `COMMITTED (G+1, 0, null)` directly by item 5's file protocol.
          - **REVERT** (`PENDING s+1`) is QUARANTINE, protocol violation. Nothing can follow a `TERMINAL` (the DDL refuses it, and item 5a's lock refuses to build it), so a pending record after one was never lawful.
          - **Absent** is `witnesslessRestore`, and **malformed** is `witnessMalformed`. A witness naming any other generation is QUARANTINE. INIT cannot arise, because L is not empty.
       3. **G = 9223372036854775807.** No successor exists. OPEN refuses on the invariant row (item 8) and writes nothing. This is unreachable on the fresh path, because it needs 2^63 − 1 closures.

     The **effective tail** is (G+1, 0, none) after case 1 succeeds or after OPEN; otherwise it is L.
   - **Who performs OPEN (lead decision).** Exactly the writers that already write the witness on REVERT, ADVANCE or INIT:
     - the carrier start, under APPEND-WRITE or EXCLUSIVE;
     - item 13's rollover.

     The floor step only decides, read-only. X6 reports `would-OPEN`. **r9:** r8 also listed the reconciliation after an uncertain outcome. That reconciliation is withdrawn (item 5), so a `TERMINAL` left by an uncertain rollover is opened by the next writer's start.
     **Rejected:** OPEN only under `EXCLUSIVE`. §7 step 1 puts the closure, the `TERMINAL` append, under `EXCLUSIVE`. Once that row is durable, the successor is fully determined, and OPEN is a witness write with the same standing as INIT, which the start already makes under APPEND-WRITE. Requiring `EXCLUSIVE` would turn a crash between `TERMINAL` and OPEN into a refusal for every writer until a rollover holder appears.
   - **Which tail each step uses.**
     - **The start tail** (X4's epoch binding and `JournalAppendLock`'s tail) is the effective tail after the start's reconciliation. A lock made after OPEN therefore appends `seq` 1 of G+1 with the genesis chain value.
     - **The start's confirmation** against the floor step's observation compares the committed tail L, which OPEN does not change.
     - **The copy tail.** The floor step and the end step copy the effective tail only when the witness reconciles OK against it (case 1, `COMMITTED 0`). Otherwise they copy L, so on OPEN the floor step copies the closing `TERMINAL` row. A floor at (G+1, 0, null) is therefore written only after the successor's `COMMITTED 0` witness.
     - **Floor regression (r9 amends; lead decision).** The floor step, the end step and item 13's observation compare the floor with the copy tail, as item 3 does, with one exception.
       - **The open-successor exception.** When the witness names the open successor (case 1, OK or REVERT), a floor exactly at the successor's empty tail, `{grantGeneration: G+1, lastSeq: 0, tailSha256: null}`, is unchanged. It is not regression, and nothing is copied.
       - **Why the state is lawful.** A floor at (G+1, 0, null) is written only after the successor's `COMMITTED 0` witness (the copy-tail rule above). A later writer whose start tail is (G+1, 0) then writes `PENDING (G+1, 1)` for G+1's first record. If that record fails certainly (a refused `INSERT`) or the process dies before its commit, the next writer sees L = the closing `TERMINAL` in G, the witness `PENDING (G+1, 1)` (case 1, REVERT), and the floor at (G+1, 0, null). On REVERT the copy tail is L, so item 3's literal comparison would call this floor regression. Because a writer stores nothing on quarantine and every open re-detects (item 8), that lawful state would be refused for good.
       - **On case 1's OK**, the copy tail is (G+1, 0, null) itself, so the floor is unchanged without the exception.
       - **Every other floor is compared as item 3 says.** Two examples:
         - a floor at (G+1, n) with n > 0, against copy tail L, is regression;
         - a floor at (G+1, 0) against a witness that does not name G+1 (case 2, for example one still naming G) is regression. The successor witness preceded that floor, and a witness never returns to G.
       - **What the exception does not do.** It moves no floor. The copy never moves the floor down, and (G+1, 0, null) is still written only after `COMMITTED 0`.
       - **Rejected:** making the copy tail the successor on case 1's REVERT too. The floor step decides read-only, before the start writes REVERT's `COMMITTED (G+1, 0)`. Copying (G+1, 0, null) from a `PENDING` witness would raise the floor on a witness that, in this observation, never said `COMMITTED 0`. That breaks the copy-tail rule.
       - **Rejected:** the literal reading, which permanently quarantines a lawful crash or refusal state.
   - **The predecessor check (r7).** Every writer open checks this in the same read snapshot: the floor step, creation, the start, the level-3 open, the end step and the rollover. If the newest generation G is above `first_generation`, the last row below G must be a `TERMINAL` in generation G − 1. Otherwise the open refuses with QUARANTINE, protocol violation (item 8), and writes nothing. It is one bounded indexed query, charged like the tail query. The DDL refuses appends to a superseded generation, but it does not refuse a gap or an unclosed predecessor; this law's writer never produces either. **Rejected:** trusting the DDL alone.

5. **The append protocol (lead decision on the file protocol).** One append, in this order, under the operation lease:
   1. **Level 3:** `BEGIN IMMEDIATE` on the carrier, `busy_timeout` 0. Busy is never waited on (F06: S7 non-waiting, earlier resources released, orphan status preserved). The evidence-ledger transaction (X3c) is acquired after the journal transaction and before level 4, by X3d's composition; X3b exposes the journal half and the ordering rule.
   2. **Level 4:** the in-process append mutex (item 6). X4's authority checkpoint runs here.
   3. Build the record (closed schema-3 body, `seq = tail + 1`, `prev_sha256` chain, `body_sha256` per §5.4) and validate it with the existing parser.
   4. Witness `PENDING seq bodySha256`, durably.
   5. `INSERT` and `COMMIT` (durable by `synchronous=FULL` and `fullfsync`).
   6. Witness `COMMITTED seq bodySha256`, durably.
   7. Release level 4; the journal transaction is already closed. **Exception (r5):** on a `SEAL` append, step 7's release waits. Level 4 stays held while staging, X4's repeated checkpoint and `AdmissionPermit`, and the evidence-ledger `COMMIT` (X3c) all run, until that `COMMIT` returns `Committed` or `CommitUndetermined`. Then level 4 is released. Level 3 is never acquired or reacquired under level 4. **If the path stops before the evidence `COMMIT`** (a staging failure, a failed repeated checkpoint, no `AdmissionPermit`, an observer latch, or any error after `SEAL`), the order is fixed. Roll back the open ledger transaction, which writes nothing. Release level 4, then each level-3 transaction. Then follow F19: append `REV` through a fresh, lawful level-3-then-level-4 acquisition (item 6). (r10: X3d's `finish` does this, funded by its settlement reserve, which survives the attempt ledger's latch; X3d r6 item 8.) Level 3 is never reacquired under level 4. Every exit from the `SEAL` path releases level 4 exactly once: `Committed`, `CommitUndetermined`, or this failure path. The X3c ledger transaction is acquired before level 4 (item 5, step 1).

   **Witness file protocol:** write a fresh temporary file `grant-journal.witness.json.<32 hex>` created exclusively in the namespace directory, write the bytes, `F_FULLFSYNC`, rename over the witness name, then the namespace directory's barrier, then reopen by name and confirm the bytes and identity. The same protocol writes the floor in `trust/carrier-floors/`. A leftover temporary file is never adopted or read; it is ignored by name grammar and removed only by a later cleanup owner. **Rejected:** a fixed temporary name (a stale one from a crashed writer would be overwritten or adopted).
   - **Uncertain outcomes (§5.6):** a failure before visibility leaves the previous durable state; a failure after visibility (a failed commit, rename or barrier) is durability-undetermined: the writer refuses every further effect and never assumes either state (F09). No evidence commit proceeds on an uncertain journal barrier.
     **r9 (lead decision): no reconciliation in the same operation.** r6 to r8 said the writer then "reconciles by reopening the carrier and running item 4's reconciliation". That is withdrawn.
     - **What the writer does.** After an uncertain outcome, the writer refuses every further effect of the operation, reconciliation included. It reads nothing more from the carrier, writes no witness and copies no floor. Releasing locks and abandoning an open transaction are not effects, and still run (step 7; X3d item 4). The operation's outcome is durability-undetermined (`DURABILITY.COMMIT_FAILED`, X3d item 9; item 13 for the rollover).
     - **Where the state is reconciled.** Before its next use, by the next writer's open:
       - the floor step (item 3), deciding read-only and copying the floor forward;
       - the carrier start (item 4), which reopens the carrier, runs item 4's reconciliation with item 4a, and writes the witness on REVERT, ADVANCE, INIT or OPEN.

       This meets §5.6's rule: the carrier is reopened and its exact state reconciled before anything uses it, and neither state is assumed. r9 reads §5.6's "the writer" as the carrier's writer role, not this operation. Only a writer open uses the carrier's write side, and every writer open reconciles first.
     - **Why.** This operation's carrier work is charged to X1's attempt ledger (item 9), which is the platform's failure-latching `WorkLedger`. A failure in any nested scope closes that ledger for good, so that a failed native operation is never retried. A failure after visibility is such a failure. So a reconciliation in the same operation is refused `Closed` before it reads anything. r8's reconciliation could never run.
     - **Every state this leaves is already handled.** A failure after visibility leaves exactly the durable state that process death at the same point leaves:
       - item 3a's creation crash states;
       - the crash states of each append step;
       - item 13's crash table.

       The next writer's floor step and start already reconcile each of these, and read-only recovery (X6) already reports each as `would-REVERT`, `would-ADVANCE` or `would-OPEN` without writing. Until then the floor lags this operation. That stays inside §5.4's detection bound, because the floor covers the last *observed* operation boundary, and an undetermined boundary is not observed. r8 already accepted the same lag after a failed reconciliation.
     - **Precedent.** X7 r3 item 5 already declines to recover an undetermined commit in the same invocation: recovery must judge the carrier fresh rather than confirm the caller's hope, and it would spend more work on an already-failed path. The same reasoning applies here.
     - **Rejected:**
       - **A post-failure allowance** reserved up front in the same ledger, spendable after the latch only by the reconciliation path through a typed capability. Any such allowance is an exception to the platform latch: the no-retry property reviewed since 416 and relied on by 468's gate. In return it would buy only a witness write and a floor copy that the next writer performs anyway. A reconciliation straight after a failed sync on the same volume is also the one most likely to fail again. That is an exception for no safety gain.
         **r10.** X3d r6 makes the one exception that has a safety gain. A settlement reserve (platform unit X3d-0) funds only the end path's `REV` and `CLN` after a *certain* refusal.
         - **Why it is justified there.** F19 requires this invocation to record that `REV`, and no later writer can.
         - **Why it cannot fund a reconciliation.** It is forfeited at any uncertain outcome, and its only spender is X3d's `finish`, for those two appends.
         - **What stands.** This rejection, and r9's forbidden substitute against an allowance for a reconciliation, are unchanged.
       - **A second ledger, or the gate ledger,** for the reconciliation (item 9, X1 item 5, X7 r3 item 7).
       - **Reporting a failure after visibility as a value,** so that the ledger stays open. That routes a native failure around the latch that exists to stop it.
       - **Keeping the reconciliation as a step that is always refused.** Law that names a step which cannot run misleads every later unit.
   - **TERMINAL and rollover (r7).** `TERMINAL` with cause `grantGenerationClosure` is appended only by item 13's rollover. It goes through this same protocol, inside item 5a's window, and is the frozen recordSchema-1 body (carrier-format.v3 §4). The generation advances by item 4a's OPEN (v8 WA-13).
     - **Narrowed from r6.** r6 said that whole-generation `REV` closes the generation the same way. Under r7, WA-13's whole-generation `REV` closure would reuse item 13's operation under its own later law. It is not claimed in M2.
     - **After the `TERMINAL`.** Once it commits, its lock admits no further record (item 5a).

5a. **The capacity window and the rollover trigger (r7; lead decision; F32).** This item reconciles X3d r3 item 3, X7 r3 item 6 and the carrier.
   - **What the carrier admits.**
     - `gj3_append_laws` refuses an ordinary record at `9007199254740991` and every append after a `TERMINAL` in its generation. It admits `TERMINAL` at any `seq`, which carrier-format.v3 §7 step 1 relies on.
     - The read side (`journal_store.rs` prefix verification) also admits `TERMINAL` at any `seq`, and ordinary records below the cap.
     - X3b-2 at product 9dbefb9 is narrower: it builds `TERMINAL` only at tail `9007199254740990` (`TerminalSlot` elsewhere), and maps every capacity refusal to the invariant row.
   - **The defect if r6 is kept.** X3d r3 item 3 admits a `SEAL` at every proven tail up to `9007199254740989`, so a `SEAL` can take `9007199254740990`. That `SEAL`'s end path needs ordinary slots: X3d item 7's one `REV`, and the `CLN` of F38's SEAL-without-commit pair. None remains, because `9007199254740991` takes only `TERMINAL`. Both records would be refused, on the invariant row at 9dbefb9.
   - **The rule.** t is the committed tail of an open generation, one whose last row is not a `TERMINAL`:

     | Record | Admitted when |
     |---|---|
     | `SEAL` | t ≤ `9007199254740987`. The `SEAL` takes at most `9007199254740988`, which leaves `…989` and `…990` for its `REV` and `CLN`. |
     | `RA`, `REV`, `CLN` | t ≤ `9007199254740989`, so the record takes at most `9007199254740990` (r8, RF-1; carrier-format.v3 §5 and X3b-2's `LAST_ORDINARY_SEQ` check, unchanged in effect) |
     | `TERMINAL`, cause `grantGenerationClosure` | `9007199254740988` ≤ t ≤ `9007199254740990`, so the `TERMINAL` takes `…989` to `…991`. Only item 13 builds it. |
     | anything | never after a `TERMINAL` in that generation |

   - **The trigger (exact).** A generation is **exhausted** when its effective tail (item 4a) is open and t ≥ `9007199254740988`: no `SEAL` fits. That is exactly when X3d's `prepare_commit` returns `CarrierCapacityExhausted { grantGeneration, provenTailSeq }`. It is also the only condition on which item 13 appends `TERMINAL`.
     - **X7's "namespace full"** is this condition. The generation is full; neither the namespace nor the generation counter is.
     - **No other `TERMINAL` point exists.** A closed generation with an unopened successor is OPEN (item 4a), not a rollover. A generation at the counter's maximum is item 4a's invariant.
     - **Against v2 §5.4, which v8 §5.4 keeps.** That section says that when the tail reaches `9007199254740990` the writer appends `TERMINAL` and rolls, so that no unrepresentable sequence can exist. r7 closes no later than that point. It closes earlier only inside the window, where no `SEAL` fits. The cause is the same (`grantGenerationClosure`, the uint53 rollover of WA-13), no schema or enum changes, and the DDL already admits a `TERMINAL` at any `seq`.
   - **X3d.** Item 3's threshold, "proven tail ≥ `9007199254740990`", is superseded by "proven tail ≥ `9007199254740988`" (no `SEAL` fits).
     - X3d-1 calls X3b's exported predicate (`seal_fits(tail)`) and never a literal. X3d's next revision cites this item.
     - Because the start performs OPEN (item 4a), X3d never observes a `TERMINAL` tail.
   - **Refusals, each certain and before any effect.**
     - **`SealCeiling`:** a `SEAL` above the ceiling. Invariant: the caller skipped X3d's check.
     - **`TerminalSlot`:** a `TERMINAL` below the window. Invariant.
     - **`Capacity`:** any record after a `TERMINAL`. Invariant: a lock whose tail is a `TERMINAL`.
     - **`GenerationFull`:** an `RA`, `REV` or `CLN` at t = `9007199254740990`. This is a lawful full generation, and it takes the busy row (X7 r3 item 6a; item 8). X3d's `finish` treats a `GenerationFull` `REV` or `CLN` as not appended. It can arise only for an operation that appended no `SEAL` in this generation, since the ceiling keeps two slots behind every `SEAL`.
     - **S6 still holds.** No `SEAL` fits at that tail. Item 13's `TERMINAL` then refuses every later append in G. G+1's first operation captures its own trust epoch at its start (X4).
   - **Rejected:**
     - `TERMINAL` only at `9007199254740991`, with X3d's `9007199254740990` threshold. A `SEAL` at `…990` strands its `REV` and `CLN`.
     - `TERMINAL` at any tail on request. WA-13 limits the causes of closure, and a writer could burn generations.
     - A wider window. After a `SEAL`, the end path appends at most one `REV` and one `CLN` (X3d item 7).

6. **The append lock X4 needs.** One `JournalAppendLock` per carrier per process: an in-process mutex owned by the operation's `ProjectOperation`, acquired only after the journal transaction (level 3) and never while waiting on the fence or a lease. It is the S6 linearization point: after a `REV` is appended under it, no `RA`, intent, commit or `SEAL` is appended. X4 r2's checkpoint (item 3) receives a borrow that proves level 4 is held; `OperationGuard` (X4 r2 item 6) lives in `ProjectOperation` beside this lock and never owns it. X4c (inside X3d) appends the end path's `REV`/`CLN` through this lock. Observers never take it (X4 r2 item 5). **Rollover (r7).** Item 13 makes its own lock from its own carrier start under its `EXCLUSIVE` lease. That happens after `finish` has consumed the operation's session and dropped the operation's lock, so the process still holds at most one lock per carrier at a time. The rollover's lock is dropped before its `EXCLUSIVE` lease is released.

7. **The witness, the floor and what they prove (lead decision on standing).** The floor is exactly the closed `CarrierFloor` shape `{highWaterSchema:1, projectKeyDigest, grantGeneration, lastSeq, tailSha256}`: a journal high-water, not a trust epoch. It records no F, L, root, revocation or index snapshot version; those are SC-TRUST's own state (X4T). X4T r1 item 7's sentence that this floor "records the trust epoch at the last operation boundary" is corrected by X4T's next revision to compare its capsule against SC-TRUST's own retained floors. **Rejected:** widening the closed floor shape with trust-epoch members.

   **The witness.** The witness proves, within one carrier and grant generation, that the tail is either the last committed record or exactly one pending record whose body hash it names. With the floor it detects torn restores, lost tails and hash substitution within the carrier, and a namespace rollback below the last observed operation boundary. It does not authenticate the interior prefix (S6 carrier anchor bound: `confirmed-under-retained-custody`). **Rejected:** claiming interior-prefix authentication or adding chain members to the closed witness.

8. **Refusal rows.** Existing S12 rows only, through a new carrier family in 468c's closed vocabulary; every match stays exhaustive.
   - Busy journal transaction (F06): `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, detail `PROJECT.BUSY`, operational-failed, exit 4.
   - Quarantine (`uncertainTailLoss`, `witnesslessRestore`, `witnessMalformed`, `floorLost`, protocol violation, floor regression): `LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted. **The writer stores nothing (RF-3).** A writer refusal appends no record, publishes nothing, writes no `carrier_quarantine` row and no other marker, and leaves the witness and floor untouched (S12, carrier-format.v3 §8.1). Every open re-detects the condition from the bytes it reads; no open trusts a stored marker. `carrier_quarantine.reason` keeps its inherited enum. Continuation on a new grant generation is a later unit.
   - Carrier project-binding mismatch: `LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted; nothing is appended or published.
   - **A carrierFormat 3 footprint that is not a lawful durable prefix** (a partial format-3 object set, definitions not byte-equal to `CURRENT_CARRIER_DDL`, `grant_journal_v3` rows before the `carrier_format` row, or a violated published generation boundary): `MIGRATION.CORRUPT` on `LEDGER.CORRUPT`, `ledger-corrupt` (S12, carrier-format.v3 row 369). It is never borrowed for ordinary journal corruption.
   - **A complete carrierFormat 1 or 2 carrier** under the namespace (impossible on the fresh path, so a planted or foreign file): the F46 class, operational-failed, exit 4, `HOST.IO_FAILURE`, `host-io`, `domainDetail` omitted. Nothing is appended, migrated or published.
   - I/O, including durability-undetermined: `HOST.IO_FAILURE`, `host-io`.
   - Budget: 468's budget row.
   - **r7 rows** (items 4a, 5a and 13; no new code, subject or remedy):
     - **Generation full** (`GenerationFull`): the busy row, `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, detail `PROJECT.BUSY`, unchanged from X7 r3 item 6a.
     - **Broken succession:** an unclosed predecessor, a generation gap, or a pending record after a `TERMINAL`. This is the quarantine row, protocol violation, and nothing is written.
     - **No successor generation** (G = `9223372036854775807`): operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `HOST.INVARIANT_VIOLATED`. Nothing is written and no `TERMINAL` is appended. This state is unreachable lawfully, so the invariant row is honest here, unlike for a merely full generation (X7 r3 item 6a). **Rejected:** appending the `TERMINAL` anyway, which would leave a carrier with no open generation.
     - **`SealCeiling`, `TerminalSlot`, and `Capacity` after a `TERMINAL`:** the invariant row, as at 9dbefb9. So is a minted rollover token equal to the released operation's (item 13).
     - **An entropy or clock failure at the rollover:** `HOST.IO_FAILURE`, `host-io`, before any effect.

9. **Budget (lead decision).** Every carrier read is bounded by the bracketed capture's existing limits (`max_file_bytes`, `max_generations`, `max_records`, `max_body_bytes`) and charged to the operation ledger before it runs. Start reads only the tail record, the witness and the floor, never the whole journal. Each append reserves its post-effect confirmation (witness reopen, directory barrier) before its first effect, as 467 item 6 does. **Rejected:** reading the full journal at start, which the protocol does not need.
   - **The rollover (r7).** Item 13 charges only the attempt ledger: the ledger this item calls the operation ledger, which is X1 item 5's attempt ledger (X3d item 8, X7 r3 item 7). It never charges the gate ledger and opens no ledger.
     - **One reservation, made before the `EXCLUSIVE` lease is taken.** It is a fixed rollover cost, and it covers:
       - the two lease locks and their release;
       - the classification, predecessor query, tail, witness and floor reads;
       - the entropy draw and the clock sample;
       - at most one reconciliation witness publication (step 3's REVERT or ADVANCE before the `TERMINAL`; r9: nothing is reserved for reconciliation after an uncertain outcome, because none runs);
       - one `TERMINAL` append at item 5's append cost: two witness publications with their confirmations, and the commit;
       - one OPEN witness publication with its confirmation.
     - **Spending.** Only those steps spend the reservation.
     - **Failure.** If the reservation fails, the rollover is not attempted. The budget row is disclosed as a rollover failure, and the end step continues to its own charged floor copy.
     - **Rejected:** charging step by step, which could exhaust the ledger after the `TERMINAL` and before OPEN. Item 4a would recover that state, but it is avoidable. **Rejected:** the gate ledger (X1 item 5).
   - **The end path's `REV` and `CLN` (r10).** X3d r6 item 8's settlement reserve funds them, on this same attempt ledger. It is not a second ledger.
     - **The appends.** Each is an item 5 append, unchanged, and reserves its confirmations before its first effect inside the settlement, as any append does.
     - **Nothing else draws on it.** The floor step, the start, other appends, the end step and the rollover do not.
     - **Forfeit.** After an uncertain outcome it is forfeited, and nothing is charged (item 5, r9).

10. **Failure cases.**
    - **Covered by X3b:** F06 (journal half), F07, F08, F09, F10, and the journal half of F19 (after a failed post-SEAL checkpoint: abort the open journal transaction if any, release level 4 then level 3, and append `REV` through a fresh lawful level-3 then level-4 call; never reacquire level 3 under level 4). r10: that `REV` is funded by X3d's settlement reserve even when the failure closed the attempt ledger (X3d r6 item 8).
    - **Covered by X3b r7:** F32's journal half: the capacity window, the closure, OPEN and the g+1 floor (items 4a, 5a and 13).
    - **Prepared, finished elsewhere:** F06's evidence half and F11 (X3c), F19's evidence abort (X3d), F38 to F41 (X4 and X3d), and F32's route and projection (X7).
    - **Not in scope:** F46 to F51 (no carrierFormat 1 or 2 carrier can exist under an X2 namespace).

11. **Tests while X2e is pending.** Until X2e lands, no production path produces a `ProjectOperation`. Tests in `opensip-security` use a crate-private, `cfg(test)` carrier location fixture: a scratch installation's retained namespace directory with the zero-rights owner allow, a test N whose `SHA-256(N)` is the carrier digest, built with `installation_read_fixture`. They cover the floor step's table (including `floorLost`, the busy probe skip and the never-lower rule), INIT and each crash state, the full reconciliation table (twenty-four cases), the start and end steps (including the end probe's skip, and a test that no floor write happens while a project lock is held), each append step's crash (injected at crate-private step hooks, recorded like 458c-b1's step recorder), busy at level 3, TERMINAL rollover, quarantine rows and durability-undetermined outcomes (r9: no reconciliation in the operation; the next writer's floor step and start reconcile). No production seam or cross-crate bridge exists; the real composition test lands with X2e.
    **r7 tests (X3b-4).** Generations and tails near the cap are reached by X3b-2's reserved-slot technique: lift `gj3_append_laws`, insert, then reinstall the trigger's stored SQL byte-identically. The tests cover:
    - **item 5a's table at every boundary:**
      - `SEAL` at tail `…987` is admitted, and at `…988` it is `SealCeiling`;
      - `RA`, `REV` and `CLN` at tail `…989` are admitted at `seq` `…990`, and at tail `…990` they are `GenerationFull` on the busy row (r8, RF-1);
      - `TERMINAL` at `…987` is `TerminalSlot`, and at `…988`, `…989` and `…990` it is admitted;
      - nothing is admitted after a `TERMINAL`;
    - **every case of item 4a:**
      - OK and REVERT on the successor, and `COMMITTED (G+1, n>0)`;
      - OPEN from OK and from ADVANCE;
      - a `PENDING` after a `TERMINAL`, and an absent or malformed witness on a closed generation;
      - G at `9223372036854775807`;
      - the predecessor check (a gap, and an unclosed predecessor);
      - the copy tail, and floor regression against a floor at (G+1, 0);
      - a start after OPEN appending `seq` 1 of G+1 with the genesis chain value;
    - **item 13:**
      - a busy `writer.lease`; a busy `readers.lease` (with the writer lock released);
      - `AlreadyRolled`; floor regression refused before any write;
      - (r8, RF-2) a restore that leaves the tail at `…988` or `…989` with `provenTailSeq` `…990`: once with the floor ahead of the tail (floor regression) and once with the floor behind it (`uncertainTailLoss`). Each refuses before any write, with no witness change and no `TERMINAL`;
      - (r8, RF-3) an open generation `9223372036854775807` with an in-window tail: the invariant row before any write, and no `TERMINAL`;
      - a crash at every row of the crash table, and an uncertain outcome at each effect (r9: no reconciliation follows in the operation, and the next writer's floor step and start reconcile);
      - a token that is fresh per attempt and differs from the released operation's ref; the `wallClockData` shape;
      - a failed reservation, after which no lease is taken;
      - charges to the attempt ledger before each effect, with a stand-in gate ledger left unchanged;
      - no floor write while `EXCLUSIVE` is held;
      - the end step writing (G+1, 0, null) only after `COMMITTED 0`.
    **r9 tests (X3b-4).**
    - **The open-successor exception.** The state: L is the closing `TERMINAL` in G, the witness is `PENDING (G+1, 1)`, and the floor is at (G+1, 0, null).
      - The floor step and the end step leave that floor unchanged.
      - Item 13's observation returns `AlreadyRolled`.
      - The next start REVERTs to `COMMITTED (G+1, 0)`.
      - A floor at (G+1, 1) in the same state is regression.
      - A floor at (G+1, 0) against a witness naming G is regression.
    - **Uncertain outcomes, append.** At each of the append's four post-visibility steps, the lock latches. No read, witness write or floor copy follows in the operation, and the end step copies nothing. The next writer's floor step and start then reconcile to the stated outcome.
    - **Uncertain outcomes, rollover.** The same holds at each of the rollover's post-visibility effects.
    - **A source pin.** No reconciliation is reachable from an uncertain outcome.
    **r10 tests (X3b-3, with X3d-1).**
    - On a closed attempt ledger the end step takes no fence, reads nothing and copies no floor, and the next writer's floor step copies it forward.
    - An end-path `REV` appended inside X3d's settlement after the attempt ledger closed is an ordinary item 5 append. Its witness, chain and S6 latch are as any `REV`'s.

12. **Units after the law.**
    - **X3b-1:** the floor step, carrier creation, open, `reconcile_witness`, and the carrier start and end steps, with the item 11 tests. Inventory successor.
    - **X3b-2:** the append protocol, the witness file protocol, `JournalAppendLock`, record building for `SEAL`, `REV`, `CLN`, `RA`, `TERMINAL`, and the uncertain-outcome reconciliation (withdrawn by r9; X3b-4 removes it). Inventory successor.
    - **X3b-3, with X2e:** composing the floor step before X2d's lease and the carrier start inside X2e's handoff, and the end step into the operation's end path. **r7:** X3b-3 also threads the exhaustion from X3d's `finish` into the end step's step 3. **r10:** the end step is not entered on a closed attempt ledger (item 4), and X3d-1's `finish` decides that.
    - **X3b-4 (r7): grant-generation rollover.** In `opensip-security`'s `journal_store`, X3b-4 adds:
      - item 4a: the successor rule in the floor step's decision, the start, the uncertain reconciliation (withdrawn by r9) and the end step; OPEN; and the predecessor check in every writer open;
      - item 5a: `SealCeiling`, the `TERMINAL` window replacing X3b-2's single-slot rule, `GenerationFull`, and the exported `seal_fits` predicate;
      - item 13's `rollover`: its reservation, `EXCLUSIVE` order, token and clock draw, crash points and outcomes;
      - the end step's exhaustion input;
      - item 11's r7 tests;
      - **r9:**
        - item 4a's open-successor exception at every floor comparison;
        - removal of the in-operation reconciliation after an uncertain outcome (X3b-1b's and X3b-2's) and of the end step's reconciled-tail input;
        - item 11's r9 tests.

      It comes with an inventory successor. It depends only on X3b-1 and X3b-2, both integrated at 9dbefb9. It does not depend on X2e: its tests use the `cfg(test)` location fixture.
      - **Relation to X7b.** X3b-4 is the library operation that X7 r3 item 6 step 3 calls. It adds no admission, gate, fence or ledger. The order is:
        1. X3b-4;
        2. X3b-3, which feeds the exhaustion into the end step;
        3. X7b, which routes `CarrierCapacityExhausted` through `finish` to that end step and projects X7 r3 item 6a's row.

        X7a ships before X7b, with no rollover, as X7 r3 item 11 says. X7b's crash-point integration tests reuse item 13's crash table.
      - **Relation to X3d-1.** X3d-1 consumes `seal_fits`. Whichever of X3d-1 and X3b-4 lands second makes that join, and no literal threshold is written.
    - **J4a (r11; J-RW r4's unit, JRW:662).** Item 2's C-ACL for `trust/carrier-floors/` at the floor step, over J4a's shared C-ACL primitive in `security::private_access`, with JRW's controls RW-C1, RW-C2, RW-C3, RW-C6, RW-C10 and RW-C12 for state RW-P3. Its X9 row, RW-K7, is in J-RW's section of X9 r17 (JRW:609).

13. **The rollover operation (r7; lead decision; F32).** `rollover(location, exhaustion, work)` is called only from item 4's end step, step 3, under the fence that step holds. No project lock is held, and the call runs on this invocation's one write receipt and gate admission (X7 r3 item 6). The `exhaustion` is X3d's `{grantGeneration: G, provenTailSeq}`, and `work` is the attempt ledger (item 9).
   - **Precondition.** Every journal outcome of the operation was certain. After an uncertain outcome the rollover does not run (§5.6: no further effect, X3d item 7). The next writer reconciles and reaches the same route.
   1. **Reserve** the fixed rollover cost (item 9). On failure, take the budget row and stop; no lease was taken.
   2. **Take `EXCLUSIVE`**, as X2 item 7 does: `writer.lease` LOCK_EX|LOCK_NB, then `readers.lease` LOCK_EX|LOCK_NB, never waiting. **Skip if busy:** if either lock is busy, release any lock already taken, in reverse order, and return `Skipped` with nothing written. A busy `writer.lease` means another operation was admitted after this one. A busy `readers.lease` means a reader or the fence-free recovery selector holds it. The generation stays exhausted, and the next writer that reaches the exhaustion takes the route (X7 r3 item 6). The end step continues at its step 4.
   3. **Observe and decide.** Under the lease, run the carrier start's observation: classification, binding, the predecessor check, the committed tail L and the witness (items 4 and 4a). Also read the floor and compare it with the copy tail as item 3 does, with item 4a's open-successor exception (r9). S7 forbids only writing trust state under a lease, and nothing here writes it. There is no floor-step observation to confirm, because the end step has held the fence throughout and wrote nothing before this point.

      | Observed (item 4a) | Action |
      |---|---|
      | Any QUARANTINE, or floor regression | refuse on item 8's row; nothing is written |
      | The newest generation is above G, or G+1 is open (case 1) | `AlreadyRolled`: nothing is written |
      | L is a `TERMINAL` in G, and the witness reconciles OK or ADVANCE against it | OPEN only (step 6) |
      | G is open and G = `9223372036854775807` (r8, RF-3) | refuse on item 8's no-successor invariant row; nothing is written and no `TERMINAL` is appended |
      | G is open and t < `provenTailSeq`, whether or not t is inside the window (r8, RF-2) | the tail is below what the attempt proved. Refuse as floor regression when the floor is ahead of t, otherwise as `uncertainTailLoss`. Nothing is written. |
      | G is open, G < `9223372036854775807`, t is in item 5a's window, t ≥ `provenTailSeq`, and the witness is OK, REVERT or ADVANCE | write the witness for REVERT or ADVANCE as the start does, then steps 4 to 6 |

      The rows apply in order, and the first match decides. Because `provenTailSeq` ≥ `9007199254740988` (item 5a's trigger), a tail below the window is always below `provenTailSeq` and takes the RF-2 row. **Rejected (RF-2):** closing any in-window tail. A restore can leave the tail at `…988` or `…989` behind a floor that is still lower, and appending `TERMINAL` there would seal the generation over records the attempt proved.

   4. **Mint the token and the wall-clock data (lead decision).**
      - **Token.** The `TERMINAL`'s `operationRef` is `op-` followed by the lowercase hex of 16 bytes from the host CSPRNG (`opensip_platform::request_entropy`, the source X3d item 2 draws the ExecutionId from). It is drawn once per rollover attempt, after the lease is held. It must differ from the released operation's `operationRef`; if it is equal, the invariant row applies and there is no redraw.
      - **Where the token lives.** It is persisted nowhere but in the `TERMINAL` body. A crashed attempt's token is either in a durable `TERMINAL` (lawful history, never redone, F50's rule) or nowhere (its `PENDING` was reverted).
      - **`wallClockData`.** One clock sample, rendered in UTC to the second as `YYYY-MM-DDTHH:MM:SSZ`, the frozen body's lexical shape. It is data, never a trusted time input.
      - **Rejected:** the released analysis operation's ref (§7 step 1; F47).
      - **Rejected:** a token derived from (N, G). Two closure attempts would be indistinguishable in history and audit, and `operationRef` is a correlation id minted by the host per operation (security-completion v2 §5.4, kept by v8 §5.4).
   5. **Append the `TERMINAL`** at t + 1, through item 5 unchanged, on a lock made from this start (item 6):
      1. level 3, `BEGIN IMMEDIATE` with `busy_timeout` 0;
      2. level 4;
      3. build the frozen recordSchema-1 body, inside item 5a's window;
      4. `PENDING`;
      5. `INSERT` and `COMMIT`;
      6. `COMMITTED`;
      7. release level 4.

      Busy at level 3 takes the busy row, with nothing written.
   6. **OPEN.** Write the witness `COMMITTED (G+1, 0, null)` by item 5's file protocol (item 4a). It writes no carrier row, changes no format row and writes no `carrier_capacity_pause` row.
   7. **Release.** Drop the lock, then release `readers.lease` and then `writer.lease`. Return `Rolled { closed: (G, t+1), opened: G+1 }`.

   - **The floor for g+1.** The end step then continues at step 4. It probes, reads the tail and the witness, and copies the floor to (G+1, 0, null) by item 4a's copy rule. That write is under the fence with no project lock held, after the `EXCLUSIVE` lease is released, and is charged like any end-step copy. **Rejected:** writing the floor inside the rollover under `EXCLUSIVE` (S7).
   - **Uncertain outcomes inside the rollover (r9).**
     - **The latch.** A failure after visibility in step 5 or 6 latches the rollover's lock. No further effect follows, and that includes reconciliation (item 5, r9). r8's "reconcile once" is withdrawn.
     - **Release.** The rollover drops its lock, then releases `readers.lease` and then `writer.lease`, as in step 7.
     - **What the end step copies.** Nothing. Steps 4 and 5 do not run (item 4, r9), and the floor is left for the next writer's floor step.
     - **What the next writer finds.** The durable state is a row of the crash table below. The next writer's floor step and start handle it as that row says, opening G+1 where the `TERMINAL` is durable.
     - **Disclosure.** The rollover failure is disclosed as `DURABILITY.COMMIT_FAILED`. The attempt's outcome is never rewritten (X7 r3 item 6, whose rollover-failure list already says "reconciled by the next writer's start").
   - **Crash states.** These cover process death at any point; the kernel releases the flocks. Each state is found by the next writer's floor step and start (item 4a):

     | Durable state at the crash | What the next writer does |
     |---|---|
     | nothing written (before `PENDING`) | It finds G exhausted again. X3d returns the exhaustion, and that writer's end step runs the rollover with a fresh token. |
     | witness `PENDING (G, t+1)`, no new row | The start REVERTs, then as above. |
     | `TERMINAL` row, witness `PENDING (G, t+1)` matching it | The start ADVANCEs on the closing tail, which is OPEN; the operation proceeds in G+1. |
     | `TERMINAL` row, witness `COMMITTED (G, t+1)` | The start OPENs; the operation proceeds in G+1. |
     | `TERMINAL` row, witness `COMMITTED (G+1, 0)`, floor still in G | The floor step copies forward to (G+1, 0, null); the operation proceeds. |
     | after the end step's floor write | done |

     On the third and fourth rows, the floor step copies the closing `TERMINAL` row, and that writer's end step copies (G+1, …).
   - **Outcome.** The rollover returns `Skipped`, `AlreadyRolled`, `Rolled` or `Refused(row)`. In every case X7 projects the attempt on its item 6a row, and a rollover refusal is disclosed on its own row (X7 r3 item 6).

## Forbidden substitutes

Deriving N or (S, G, K) outside X2e; any floor write while this process holds a project lock; a creation order that writes the witness before the floor; a carrier digest over any preimage but N; a writer-stored quarantine marker or `carrier_quarantine` row; `MIGRATION.CORRUPT` for anything but a format-3 footprint or generation boundary; a carrier format other than 3, or any migration; a floor inside the namespace or keyed by projectKey bytes or digest; writing the floor under a lease; appending under level 4 without the journal transaction, or acquiring level 3 under level 4; waiting on a busy journal transaction; a fixed or adopted temporary witness name; proceeding to evidence commit on an uncertain journal barrier; assuming either state after a failure after visibility; reconciliation (REVERT, ADVANCE, INIT) by a read-only path; claiming interior-prefix authentication; a production seam to construct a carrier location. **r7:**
- a `TERMINAL` outside item 5a's window, or from anything but item 13;
- a `SEAL` above the ceiling, or a literal capacity threshold outside `seal_fits`;
- a carrier row, a format-row change or a `carrier_capacity_pause` row to open a generation;
- a successor other than G+1;
- OPEN before the `TERMINAL` is durable;
- a floor write under the rollover's `EXCLUSIVE` lease;
- the analysis operation's `operationRef`, or a derived token, on a `TERMINAL`;
- charging the rollover to the gate ledger, or opening a ledger for it;
- a rollover after an uncertain journal outcome;
- waiting for a lease at the rollover.

**r9:**
- any carrier read, witness write, floor copy or other reconciliation in the same operation after an uncertain outcome;
- a ledger allowance that survives the attempt ledger's latch, a second ledger, or a failure reported as a value, used to make such a reconciliation run;
- quarantining a floor at (G+1, 0, null) as regression while the witness names the open successor G+1.

**r10:**
- drawing on X3d's settlement reserve for anything but the end path's `REV` and `CLN` appends: no reconciliation, no witness write outside those appends, no floor copy, no end step and no rollover;
- an end step entered on a closed attempt ledger.

## Not claimed

CLI enablement; the evidence ledger, blob store and commit facade (X3c, X3d); carrier migration (F46 to F51); quarantine continuation on a new grant generation; whole-generation `REV` closure (WA-13), which would reuse item 13 under its own law; lifecycle transition journals (M5); leftover temporary-file cleanup; read-only recovery (X6); any qualified boot identity on this BASELINE-ATTESTED host.
