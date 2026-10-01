# The durable grant-journal append, its witness and the carrier high-water — proposal X3b r4

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X3b of `EXIT-PLAN.md` (DR-G19, COV-03), under owner.md §8, security-and-lifecycle S6 (linearization, commit-admission gate), S7 (lock order and modes) and S12, `security-completion.v8.md` §5.4 to §5.6 (the grant-journal carrier, lock handoff, witness, durability primitives), the selected physical carrier `design-corrections/security/grant-journal.carrier.v3.sql` (carrierFormat 3, S1 row 84), `host-foundation-completion.v2.md` (project namespace layout), the build plan's failure cases F06 to F11 and F19, and laws X1 r1, X3a r3, X2 r4 (items 5 to 7a: R0, R1, R2, X2d's lease, X2e's handoff), X4 r2 (`OperationGuard` inside X2e; the checkpoint under `JournalAppendLock`) and X4T r1. r2 answers Grok X3b r1 RF-1 (no floor write under a lease), RF-2 (the digest's preimage), RF-3 (no writer quarantine marker; the F46 row) and RF-4 (floor before witness). r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok X3b r2 RF-1 (format dispatch before the floor table) and RF-2 (the floor table implements the crash list and reconciliation; a whole INIT floor). r2 bytes are preserved in PROPOSAL-r2.md. r4 answers Grok X3b r3 RF-1 (a present non-INIT floor with no carrier is `uncertainTailLoss`). r3 bytes are preserved in PROPOSAL-r3.md. It keeps X2 r5 item 7's ordering (the floor step runs under the fence before any lease) and X4T r2's fenced admission at the same point. Items 1, 2, 3, 4, 5, 7 and 9 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Not code. Library only: no command is wired.

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
      | present | complete format 3 | any | run `reconcile_witness` **as a decision only** (item 4's table, read-only; the witness is not written here). A QUARANTINE outcome (`witnesslessRestore`, `witnessMalformed`, `uncertainTailLoss`, protocol violation, carrier mismatch) refuses and leaves the floor untouched. An INIT outcome (empty journal, no witness) requires the floor to be `grantGeneration 1, lastSeq 0`, else `uncertainTailLoss`; nothing is written and item 3a finishes INIT. An OK, REVERT or ADVANCE outcome then compares the committed tail with the floor: a lower generation or a lower sequence in the floor's generation, or an equal sequence with a different body hash, is floor regression. Otherwise the floor is copied forward to the committed tail only if the tail is higher; it never moves down |

      The committed tail is the last committed row; REVERT and ADVANCE concern only the witness, so the copied tail is the same either way. The witness write that REVERT, ADVANCE or INIT needs is performed later by the carrier start under the lease (item 4).
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
   - **End (the only other floor write):**
     1. Release the operation lease (S7 end rule).
     2. Take the fence by the shared charged walk and no-follow fence open (458c-b1's helpers, with S7's bounded 5 s wait).
     3. Probe `writer.lease` LOCK_EX|LOCK_NB. If it is busy, another writer was admitted after us and its start observed a tail at or above ours: skip the copy, release the fence, end.
     4. If the probe succeeds, read the committed tail from one read snapshot, release the probe lock, then write the floor to that tail if it is higher, under the fence with no project lock held.
     5. Release the fence.

     The end step reuses this invocation's write receipt and gate admission; it takes no second gate (one per process), and performs only this floor write, with its own barriers. A failure at end is disclosed and never rewrites the operation's outcome.

5. **The append protocol (lead decision on the file protocol).** One append, in this order, under the operation lease:
   1. **Level 3:** `BEGIN IMMEDIATE` on the carrier, `busy_timeout` 0. Busy is never waited on (F06: S7 non-waiting, earlier resources released, orphan status preserved). The evidence-ledger transaction (X3c) is acquired after the journal transaction and before level 4, by X3d's composition; X3b exposes the journal half and the ordering rule.
   2. **Level 4:** the in-process append mutex (item 6). X4's authority checkpoint runs here.
   3. Build the record (closed schema-3 body, `seq = tail + 1`, `prev_sha256` chain, `body_sha256` per §5.4) and validate it with the existing parser.
   4. Witness `PENDING seq bodySha256`, durably.
   5. `INSERT` and `COMMIT` (durable by `synchronous=FULL` and `fullfsync`).
   6. Witness `COMMITTED seq bodySha256`, durably.
   7. Release level 4; the journal transaction is already closed.

   **Witness file protocol:** write a fresh temporary file `grant-journal.witness.json.<32 hex>` created exclusively in the namespace directory, write the bytes, `F_FULLFSYNC`, rename over the witness name, then the namespace directory's barrier, then reopen by name and confirm the bytes and identity. The same protocol writes the floor in `trust/carrier-floors/`. A leftover temporary file is never adopted or read; it is ignored by name grammar and removed only by a later cleanup owner. **Rejected:** a fixed temporary name (a stale one from a crashed writer would be overwritten or adopted).
   - **Uncertain outcomes (§5.6):** a failure before visibility leaves the previous durable state; a failure after visibility (a failed commit, rename or barrier) is durability-undetermined: the writer refuses every further effect, reconciles by reopening the carrier and running item 4's reconciliation, and never assumes either state (F09). No evidence commit proceeds on an uncertain journal barrier.
   - **TERMINAL and rollover:** at tail `9007199254740990` the append is `TERMINAL` with cause `grantGenerationClosure` and the generation advances (§5.4 v2, v8 WA-13); whole-generation `REV` closes the generation the same way. Both follow the same protocol.

6. **The append lock X4 needs.** One `JournalAppendLock` per carrier per process: an in-process mutex owned by the operation's `ProjectOperation`, acquired only after the journal transaction (level 3) and never while waiting on the fence or a lease. It is the S6 linearization point: after a `REV` is appended under it, no `RA`, intent, commit or `SEAL` is appended. X4 r2's checkpoint (item 3) receives a borrow that proves level 4 is held; `OperationGuard` (X4 r2 item 6) lives in `ProjectOperation` beside this lock and never owns it. X4c (inside X3d) appends the end path's `REV`/`CLN` through this lock. Observers never take it (X4 r2 item 5).

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

9. **Budget (lead decision).** Every carrier read is bounded by the bracketed capture's existing limits (`max_file_bytes`, `max_generations`, `max_records`, `max_body_bytes`) and charged to the operation ledger before it runs. Start reads only the tail record, the witness and the floor, never the whole journal. Each append reserves its post-effect confirmation (witness reopen, directory barrier) before its first effect, as 467 item 6 does. **Rejected:** reading the full journal at start, which the protocol does not need.

10. **Failure cases.**
    - **Covered by X3b:** F06 (journal half), F07, F08, F09, F10, and the journal half of F19 (after a failed post-SEAL checkpoint: abort the open journal transaction if any, release level 4 then level 3, and append `REV` through a fresh lawful level-3 then level-4 call; never reacquire level 3 under level 4).
    - **Prepared, finished elsewhere:** F06's evidence half and F11 (X3c), F19's evidence abort (X3d), F38 to F41 (X4 and X3d).
    - **Not in scope:** F46 to F51 (no carrierFormat 1 or 2 carrier can exist under an X2 namespace).

11. **Tests while X2e is pending.** Until X2e lands, no production path produces a `ProjectOperation`. Tests in `opensip-security` use a crate-private, `cfg(test)` carrier location fixture: a scratch installation's retained namespace directory with the zero-rights owner allow, a test N whose `SHA-256(N)` is the carrier digest, built with `installation_read_fixture`. They cover the floor step's table (including `floorLost`, the busy probe skip and the never-lower rule), INIT and each crash state, the full reconciliation table (twenty-four cases), the start and end steps (including the end probe's skip, and a test that no floor write happens while a project lock is held), each append step's crash (injected at crate-private step hooks, recorded like 458c-b1's step recorder), busy at level 3, TERMINAL rollover, quarantine rows and durability-undetermined reconciliation. No production seam or cross-crate bridge exists; the real composition test lands with X2e.

12. **Units after the law.**
    - **X3b-1:** the floor step, carrier creation, open, `reconcile_witness`, and the carrier start and end steps, with the item 11 tests. Inventory successor.
    - **X3b-2:** the append protocol, the witness file protocol, `JournalAppendLock`, record building for `SEAL`, `REV`, `CLN`, `RA`, `TERMINAL`, and the uncertain-outcome reconciliation. Inventory successor.
    - **X3b-3, with X2e:** composing the floor step before X2d's lease and the carrier start inside X2e's handoff, and the end step into the operation's end path.

## Forbidden substitutes

Deriving N or (S, G, K) outside X2e; any floor write while this process holds a project lock; a creation order that writes the witness before the floor; a carrier digest over any preimage but N; a writer-stored quarantine marker or `carrier_quarantine` row; `MIGRATION.CORRUPT` for anything but a format-3 footprint or generation boundary; a carrier format other than 3, or any migration; a floor inside the namespace or keyed by projectKey bytes or digest; writing the floor under a lease; appending under level 4 without the journal transaction, or acquiring level 3 under level 4; waiting on a busy journal transaction; a fixed or adopted temporary witness name; proceeding to evidence commit on an uncertain journal barrier; assuming either state after a failure after visibility; reconciliation (REVERT, ADVANCE, INIT) by a read-only path; claiming interior-prefix authentication; a production seam to construct a carrier location.

## Not claimed

CLI enablement; the evidence ledger, blob store and commit facade (X3c, X3d); carrier migration (F46 to F51); quarantine continuation on a new grant generation; lifecycle transition journals (M5); leftover temporary-file cleanup; read-only recovery (X6); any qualified boot identity on this BASELINE-ATTESTED host.
