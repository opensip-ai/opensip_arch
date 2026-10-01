# The durable grant-journal append, its witness and the carrier high-water — proposal X3b r1

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X3b of `EXIT-PLAN.md` (DR-G19, COV-03), under owner.md §8, security-and-lifecycle S6 (linearization, commit-admission gate), S7 (lock order and modes) and S12, `security-completion.v8.md` §5.4 to §5.6 (the grant-journal carrier, lock handoff, witness, durability primitives), the selected physical carrier `design-corrections/security/grant-journal.carrier.v3.sql` (carrierFormat 3, S1 row 84), `host-foundation-completion.v2.md` (project namespace layout), the build plan's failure cases F06 to F11 and F19, and laws X1 r1, X3a r3, X4 r1 and X2 (r2, in revision). Items 1, 2, 4, 5, 7 and 9 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Not code. Library only: no command is wired.

## Problem

M2's commit path appends a `SEAL` to the project's grant journal under the level-4 append lock, between the object barriers and the evidence-ledger commit. The journal's write side does not exist at f7acb6d:
- `security/src/journal_store.rs` and `journal_store/` hold the read side only: the closed schema-3 `JournalRecord` parser, the carrierFormat 3 DDL (`CURRENT_CARRIER_DDL`), carrier dispatch, historical rows, generation population, the bracketed capture and the generation-anchor judgment, with `Witness` and `CarrierFloor` decoders. Nothing creates a carrier, appends a record, writes a witness or copies a high-water.
- No level-4 append lock exists, though X4 r1 item 3 runs the authority checkpoint under it.
- `lifecycle/src/journal_store.rs` (lifecycle transition records) is a different owner (COV-03, DR-G18, M5) and is not this unit.

## Decisions

1. **Where the N-bound binding is produced (lead decision): X2e.** X2 r2 item 7a's handoff already joins the Eligible row's N and X3a's `SelectedStoreEndpoint` under the held fence, by moving owners. The owner §8 five-field binding `{schemaVersion:1, namespaceId:N, storeInstanceId:S, storeGeneration:G, stateSchema:K}` is derived there, from those moved owners only, and becomes a field of `ProjectOperation`. X3b consumes `ProjectOperation`; it never derives N or (S, G, K).
   - **Required composition with X2e.** The carrier start of item 4 runs inside X2e's handoff, after the join and before the fence is released (§5.4: the tail, witness and high-water are compared and copied under the fence). X2's item 7a step 3 is therefore preceded by X3b's carrier start; X2e composes it, and X2 records this when it is next revised.
   - **Rejected:** producing the binding in X3b, which would need N and the endpoint after the fence is released, reversing the lock order owner §8 forbids.

2. **Location and format (lead decision).** The carrier is exactly the selected physical carrier, at exactly the host-foundation locations, under the namespace directory X2 publishes (`I/host/projects/N/`, X2 r2 item 6):
   - `grant-journal.sqlite`: carrierFormat 3, the bytes of `grant-journal.carrier.v3.sql` as embedded in `CURRENT_CARRIER_DDL`, WAL, with `synchronous=FULL`, `fullfsync=ON`, `checkpoint_fullfsync=ON` and foreign keys on (§5.6). Its WAL and shm sidecars are in the same directory.
   - `grant-journal.witness.json`: the closed v8 witness `{witnessSchema:1, projectKeyDigest, grantGeneration, seq, state, bodySha256}`, encoded by the existing `Witness` encoder.
   - **The carrier floor (SC-TRUST high-water):** `I/trust/carrier-floors/N.v1`, the existing `CarrierFloor` shape `{highWaterSchema:1, projectKeyDigest, grantGeneration, lastSeq, tailSha256}`. It is outside the namespace so that a namespace rollback cannot roll it back (§5.4), it is written only under the fence (S7: trust state is never written under a lease), and N is the path component (host-foundation: neither projectKey bytes nor its digest is a path component). `trust/carrier-floors/` is created on first need under the fence with 465 item 3's create-or-admit rules and barriers.
   - **Only the fresh path.** X3b creates and opens carrierFormat 3 carriers only. A namespace's carrier is created by its first operation (item 3), so no carrierFormat 1 or 2 carrier can exist under an X2 namespace. Any non-format-3 object found is refused (item 8); migration (F46 to F51) stays out of M2, per EXIT-PLAN.
   - `projectKeyDigest` is SHA-256 of the registry row's projectKey as X2's registry owner defines it, taken from `ProjectOperation`'s row snapshot.
   - **Rejected:** a carrier under the store (it would follow store reselection, which the journal must not) or a floor inside the namespace (§5.4's rollback detection would be void).

3. **Carrier creation (INIT).** Only when, under the held fence and the operation's EXCLUSIVE or APPEND-WRITE lease, the namespace holds positively observed no carrier and no witness, and the floor for N is positively absent:
   1. Create `grant-journal.sqlite` exclusively (no replace), set the pragmas, then in one `BEGIN IMMEDIATE` transaction apply the DDL and publish the `carrier_format` row (fresh path: `first_generation` 1, no migration fields). `COMMIT`; then the file's and the namespace directory's barriers. SQLite DDL is transactional, so the database holds either no schema objects or the complete set and its row.
   2. Write the witness `COMMITTED 0` (`bodySha256` null) by the item 5 file protocol.
   3. Write the floor `{lastSeq 0, tailSha256 null}` by the same protocol under `trust/carrier-floors/`.

   **Crash states:** an empty database (no schema objects) with no witness is INIT again; a complete schema with its row and no witness is `witnesslessRestore` only when the journal holds a record, otherwise INIT continues at step 2; a partial object set is impossible by step 1 and, if observed, is `MIGRATION.CORRUPT` (S12). A witness with no carrier is a quarantine (`uncertainTailLoss`).

4. **Operation start and end (the §5.4 handoff).**
   - **Start, under the fence, inside X2e:** open the carrier through the retained namespace handle; validate the format row's `project_key_digest` against the admitted one (a mismatch is the carrier project-binding row); read the tail and the witness; run `reconcile_witness` (§5.4 table: INIT, OK, REVERT, ADVANCE, QUARANTINE); compare the tail with the floor (a lower tail, or an equal sequence with a different body hash, quarantines); write the observed tail into the floor; capture the start tail for X4's epoch binding. Only an authorized writer (APPEND-WRITE or EXCLUSIVE, under the fence) performs REVERT, ADVANCE, INIT or the floor copy; read-only diagnosis (X6) only reports `would-REVERT` or `would-ADVANCE` (F07, F10).
   - **End:** release the lease; take the fence by the shared charged walk and no-follow fence open (458c-b1's helpers, with S7's bounded 5 s wait); re-acquire the lease non-blocking; if acquired, re-read the tail, copy it into the floor, and release both; if another writer holds it, skip the copy and release the fence. The end step reuses this invocation's write receipt and gate admission; it takes no second gate (one per process) and performs only the floor write, with its own barriers. A failure at end is disclosed and never rewrites the operation's outcome.

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

6. **The append lock X4 needs.** One `JournalAppendLock` per carrier per process: an in-process mutex owned by the operation's `ProjectOperation`, acquired only after the journal transaction (level 3) and never while waiting on the fence or a lease. It is the S6 linearization point: after a `REV` is appended under it, no `RA`, intent, commit or `SEAL` is appended. X4's checkpoint receives a borrow that proves level 4 is held; X4's abstract lock is replaced by this one (X4 item 10's X4c). Observers never take it (X4 item 5).

7. **The witness and what it proves (lead decision on standing).** The witness proves, within one carrier and grant generation, that the tail is either the last committed record or exactly one pending record whose body hash it names. With the floor it detects torn restores, lost tails and hash substitution within the carrier, and a namespace rollback below the last observed operation boundary. It does not authenticate the interior prefix (S6 carrier anchor bound: `confirmed-under-retained-custody`). **Rejected:** claiming interior-prefix authentication or adding chain members to the closed witness.

8. **Refusal rows.** Existing S12 rows only, through a new carrier family in 468c's closed vocabulary; every match stays exhaustive.
   - Busy journal transaction (F06): `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, detail `PROJECT.BUSY`, operational-failed, exit 4.
   - Quarantine (`uncertainTailLoss`, `witnesslessRestore`, `witnessMalformed`, protocol violation, floor regression): `LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted. A quarantine is recorded by the existing `carrier_quarantine` row and `failClosedNoAppend`; continuation only on a new grant generation (a later unit).
   - Carrier project-binding mismatch: `LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted; nothing is appended or published.
   - A non-format-3 or partial carrier object set: `MIGRATION.CORRUPT` on `LEDGER.CORRUPT`.
   - I/O, including durability-undetermined: `HOST.IO_FAILURE`, `host-io`.
   - Budget: 468's budget row.

9. **Budget (lead decision).** Every carrier read is bounded by the bracketed capture's existing limits (`max_file_bytes`, `max_generations`, `max_records`, `max_body_bytes`) and charged to the operation ledger before it runs. Start reads only the tail record, the witness and the floor, never the whole journal. Each append reserves its post-effect confirmation (witness reopen, directory barrier) before its first effect, as 467 item 6 does. **Rejected:** reading the full journal at start, which the protocol does not need.

10. **Failure cases.**
    - **Covered by X3b:** F06 (journal half), F07, F08, F09, F10, and the journal half of F19 (after a failed post-SEAL checkpoint: abort the open journal transaction if any, release level 4 then level 3, and append `REV` through a fresh lawful level-3 then level-4 call; never reacquire level 3 under level 4).
    - **Prepared, finished elsewhere:** F06's evidence half and F11 (X3c), F19's evidence abort (X3d), F38 to F41 (X4 and X3d).
    - **Not in scope:** F46 to F51 (no carrierFormat 1 or 2 carrier can exist under an X2 namespace).

11. **Tests while X2e is pending.** Until X2e lands, no production path produces a `ProjectOperation`. Tests in `opensip-security` use a crate-private, `cfg(test)` carrier location fixture: a scratch installation's retained namespace directory with the zero-rights owner allow, a test projectKey and N, built with `installation_read_fixture`. They cover INIT and each crash state, the full reconciliation table (twenty-four cases), the start and end handoff, each append step's crash (injected at crate-private step hooks, recorded like 458c-b1's step recorder), busy at level 3, TERMINAL rollover, quarantine rows and durability-undetermined reconciliation. No production seam or cross-crate bridge exists; the real composition test lands with X2e.

12. **Units after the law.**
    - **X3b-1:** carrier creation, open, `reconcile_witness`, the floor and the start and end steps, with the item 11 tests. Inventory successor.
    - **X3b-2:** the append protocol, the witness file protocol, `JournalAppendLock`, record building for `SEAL`, `REV`, `CLN`, `RA`, `TERMINAL`, and the uncertain-outcome reconciliation. Inventory successor.
    - **X3b-3, with X2e:** composing the carrier start inside X2e's handoff and the end step into the operation's end path.

## Forbidden substitutes

Deriving N or (S, G, K) outside X2e; a carrier format other than 3, or any migration; a floor inside the namespace or keyed by projectKey bytes or digest; writing the floor under a lease; appending under level 4 without the journal transaction, or acquiring level 3 under level 4; waiting on a busy journal transaction; a fixed or adopted temporary witness name; proceeding to evidence commit on an uncertain journal barrier; assuming either state after a failure after visibility; reconciliation (REVERT, ADVANCE, INIT) by a read-only path; claiming interior-prefix authentication; a production seam to construct a carrier location.

## Not claimed

CLI enablement; the evidence ledger, blob store and commit facade (X3c, X3d); carrier migration (F46 to F51); quarantine continuation on a new grant generation; lifecycle transition journals (M5); leftover temporary-file cleanup; read-only recovery (X6); any qualified boot identity on this BASELINE-ATTESTED host.
