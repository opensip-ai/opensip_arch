# Evidence ledger transaction and blob publication — proposal X3c r8
 r2 answers Grok X3c r1 RF-1: the lock order now cites X3b r5's SEAL-path hold. r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok r2 RF-1: release on a SEAL path that stops before COMMIT. r2 bytes are preserved in PROPOSAL-r2.md. r4 answers Grok r3 RF-1: the old rejection now applies only to a path that continues to COMMIT. r3 bytes are preserved in PROPOSAL-r3.md. r5 answers Grok r4 RF-1: the forbidden-substitutes line now matches item 8. r4 bytes are preserved in PROPOSAL-r4.md. r6 answers Grok r5 RF-1: the fresh REV acquisition cites X3b r6 item 6, not this law's item 6. r5 bytes are preserved in PROPOSAL-r5.md. r6 was ACCEPTED by Grok on 2026-10-01. r7 is an amendment from implementing X3c-1: SQLite cannot switch to WAL inside a transaction, so WAL is selected just before the DDL transaction. r6 bytes are preserved in PROPOSAL-r6.md. r7 ACCEPTED by Grok on 2026-10-01. r8 (2026-10-04) is the successor that M3-PLAN r6 assigns by lead decision P5-2: re-commit of a Run already committed in the same store and namespace. r7 bytes, as accepted (sha256 `b9585372…`, without the acceptance note), are preserved in PROPOSAL-r7.md. **Draft r8, not accepted.**
2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X3c of `EXIT-PLAN.md` (DR-G19), under owner.md §7 and §8, security-and-lifecycle S6 (the commit-admission gate) and S7 (lock order and modes), the build plan's "Security/storage ownership and the final commit gate", "Publication sequence and lock discipline" (steps 3, 4 and 6), "Failure and recovery account" and failure cases F02 to F06 and F11 to F15, `commit-recovery-readonly.v3.md` (its D9 standings table, §4 the authorized settlement sweep, §5 the ledger-owned attempt phase), `attempt-custody.schema.v1.json`, the selected physical-layout owner (owner201, product `lifecycle/src/locations.rs`), and laws X1 r1, X2 r5 (`ProjectOperation`, X2e), X3a r5 (`SelectedStoreEndpoint`; no store work in a creator invocation), X3b r4 (the journal, witness, `CarrierFloor`, `JournalAppendLock`) and X4 r4 (`OperationGuard`, the checkpoint under `JournalAppendLock`, `FinalGate` and the single-use `AdmissionPermit`) and X4T r3. Items 1, 2, 3, 5, 6, 8 and 9 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Not code. Library only: no command is wired.

**r8 basis.** 2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Not code. r8 is written under:
- **identity-and-evidence (IE, `docs/v2/contracts/product-v1/identity-and-evidence.md`):**
  - "Retry always receives a new ExecutionId … Identical semantic inputs can produce the same Run on two attempts; attempts remain separately auditable" (IE:104-107);
  - the commit order and "Duplicate retry can share a Run but has a separate attempt receipt" (IE:1665-1683);
  - a landed receipt "establishes historical commitment on its own", even while its attempt row is `admitted` (IE:1689-1692);
  - availability is "a separate monotonic-generation record" that "may improve through verified restoration or regeneration" (IE:1721-1725), and "a regeneration mismatch refuses" (IE:1825-1827).
- **security-and-lifecycle (SL, `docs/v2/contracts/product-v1/security-and-lifecycle.md`):** GC "follows the admitted retention policy, pins and availability generations" (SL:1456).
- **The plan and the gap's records:**
  - M3-PLAN r6 (M3P, `m3/M3-PLAN-r6.md`, `a6956e88…`): the carry-in (M3P:157, :237), the M3-J row (M3P:217), the schedule (M3P:310), P5-1 (M3P:572-575) and P5-2 (M3P:576-578);
  - EXIT-PLAN (EXIT, `m2/EXIT-PLAN.md`): its X3c row (EXIT:70) and "X3d-2 ordering and follow-ups" (b) (EXIT:171);
  - M2-COMPLETE (M2C, `m2/M2-COMPLETE.md`) §5 rows 6 and 11.
- **Accepted laws:**
  - X3d r8 (X3D, `m2/commit-session-x3d/PROPOSAL.md`): its r7 known limit (X3D:51-54) and item 4 step 3.8 (X3D:152);
  - X6 r4, X7 r6, and X9 r16 (X9, `m2/crash-matrix-x9/PROPOSAL.md`);
  - M3-J1 r3 (J1, `m3/host-pipeline-j/PROPOSAL.md`): item 8's phases, item 11, and its successors S12 and S14.
- **The sibling successor, read but not edited:** J-RW r1, the resume/repair writer (J-RW, `m3/resume-repair-jrw/PROPOSAL.md`, draft with Codex, arch `80a5d822b`, sha256 `0002c005…`): its scope and out-of-scope list (J-RW:69-89), C-LEDGER (J-RW:151-163), its X9 r17 section (J-RW:304-360), its successor RW-S3 (J-RW:385), its cross-law items X-RW-3, X-RW-9 and X-RW-10 (J-RW:407-429), and LD-11 (J-RW:467).
- **The product** at main `e093e90` (F8b). F8b changed no file under `crates/`, so every product line cited here is the same at `3e64266`.

Items 6a.1 to 6a.5, 6a.9, 14 and 15 contain r8's lead decisions R8-1 to R8-8, made under the same standing direction; each names the alternatives it rejects. r8 adds no public code, row, detail, DDL, crash point, type or facade method.

## r8 changes

| # | Change | Items | Basis |
|---|---|---|---|
| 1 | **Re-commit is lawful.** A Run already committed in (S, N) is committed again by a new attempt, with its own attempt row, SEAL, receipt, association and Run-material row. It ends `Committed`, never on the invariant row. | 6, 6a.1 | IE:104-107, :1683; P5-2; J1 item 11 |
| 2 | **Standing.** Inside the open level-3 transaction, before any insert, staging reads whether the Run is already committed in (S, N), from the Run's committed per-Run rows only. A one-sided Run refuses. | 6a.2 | R8-2 |
| 3 | **Byte-identical material.** A re-commit's manifest and inventory must equal the Run's committed material byte for byte. Otherwise staging refuses: IE's regeneration mismatch. | 6a.3 | IE:1825-1827; R8-3 |
| 4 | **Per-Run rows are written once, by the first commit.** A re-commit stages no availability record and no pin change, and never writes an availability successor. | 6, 6a.4, 6a.5 | EXIT:171; X3D:51-54; R8-4, R8-5 |
| 5 | **What a re-commit writes, its idempotence, and different content** in the same namespace. | 6a.6 to 6a.8 | — |
| 6 | **No DDL change, no new crash point, no new type or outcome.** | 6a.9 | R8-6 |
| 7 | **Budget** of the standing read and the comparison. | 9 | — |
| 8 | **Three refusal conditions on existing rows:** the regeneration mismatch and a non-empty declared pin set on a re-commit (the invariant row); a one-sided Run (`LEDGER.CORRUPT`). | 10 | — |
| 9 | **G2 restatement (record).** Item 11's hook sentence now reads "absent from every non-test build". | 11 | X9:1219 (G2); M2C §5 row 6 |
| 10 | Failure-case coverage and X3c-3's tests. | 12, 12b | — |
| 11 | **Unit X3c-3** and its serialized lead set. | 13 | M3P:237, :310 |
| 12 | **The crash windows and the rows X9 r17 carries** (RC-1 to RC-9), the census child, and the 19 accepted runs with an unscored same-Run commit, 18 of which change outcome. | 14 | R8-7 |
| 13 | **Interactions:** J1's phases and cancellation; J-RW's boundary and text sequencing; X3d, X6 and X7. | 15 | J1 items 8 and 11; J-RW item 1, LD-11; R8-8 |
| 14 | **Cross-law items** CL-1 to CL-5, and the records owed after acceptance. | 16 | J-RW X-RW-3, X-RW-9, X-RW-10 |
| 15 | Forbidden substitutes and "Not claimed" are extended. | — | — |

Items 1 to 5, 7 and 8 are unchanged; in particular r8 does not touch item 2 (CL-5). Item 6 changes only where it is marked **r8**. r8's additions to item 10 and to the forbidden substitutes concern re-commit only. They do not carry J-RW's X3c text, which follows separately (CL-4).

## Problem

M2's commit path publishes immutable evidence objects, then commits one evidence-ledger transaction that carries the Run's receipt and its private recovery association, after the journal `SEAL` (X3b) and the commit gate (X4). At 99f1c35 the parts are present but inert:
- `storage/src/blob_store.rs` publishes and reads one digest-named object in a supplied, retained directory: exclusive new-file publication with its directory barrier, or byte-for-byte confirmation of an existing name. It has no caller, no layout and no budget.
- `storage/src/ledger_store.rs` opens only an **existing** ledger (`SQLITE_OPEN_NOFOLLOW`, `synchronous=FULL`, `fullfsync`, `checkpoint_fullfsync`, `trusted_schema=OFF`), begins `BEGIN IMMEDIATE`, and classifies a failed `COMMIT` as `CommitUndetermined`. It carries the selected DDL for `attempt_custody`, `commit_receipts`/`commit_associations`, `evidence_availability`, `commit_run_material`, `active_run_pins` and `pin_change_facts`, each verified against the stored schema, and the private staging of the receipt/association pair. It never creates a ledger.
- Nothing places the ledger or the objects, admits the attempt row, orders the level-3 acquisitions, or maps failures to public rows.

X3c owns the ledger and object side of steps 3, 4 and 6 up to the prepared commit and its durability classification. X3d's `CommitSession` facade composes it with X3b and X4; X6 owns read-only recovery and the settlement sweep.

**r8: the re-commit gap.** At main `e093e90`, as at `3e64266`, a second commit of a Run already committed in the same (S, N) is refused after its durable `SEAL`:
- **What staging is handed.** `stage` (`crates/storage/src/commit.rs:701-752`) always builds the Run's initial availability record, generation 0 `retained` (`:729`, `:792-804`), and the empty pin set (`:732`).
- **What staging does with them.** `PreparedLedger::stage` (`crates/storage/src/ledger_store/project_commit.rs:422-541`) stages the receipt pair and the Run material. It then calls `stage_availability` with expected generation `None` (`:503-511`), and `stage_pin_change` as a first publication (`:513-529`).
- **Why that refuses.** `evidence_availability` is keyed by (store generation digest, N, RunId, generation) (`ledger_store.rs:762-773`). The Run's generation-0 row from its first commit is therefore the current record. It is not the expected `None`, so `stage_availability` returns `availability_stale_generation` (`ledger_store.rs:856-860`).
- **The row.** `classify_staging` maps that to `StagingMismatch` (`project_commit.rs:559-576`), which is the invariant row (`ledger_store/project_ledger.rs:248-258`). It returns through `SealRefusal::Staging` (`crates/security/src/custody/commit_session.rs:916-925`, `:997`; `commit.rs:626-628`). The transaction rolls back, and `finish` revokes the durable `SEAL` with `REV` and `CLN`.

Every other row a re-commit writes is keyed by its own ExecutionId: the attempt row, the receipt, the association and the Run material (`ledger_store.rs:441-502`; `ledger_store/recovery_material.rs:13-26`). The pin stage passes at M3, because the declared set and the current set are both empty (`pin_inventory.rs:146-182`). So availability alone refuses.

Three records already point here:
- **X3d r7** recorded the limit and named the fix: "An X3c successor that stages availability only when none exists" (X3D:51-54).
- **X9 r12 and r13** worked around it. Every next writer after a committed Run commits a distinct candidate variant (X9:255-268, :353-365), and "Re-committing the same Run … stays X3d-2's known limit, and no M2 law decides it" (X9:268).
- **J1** needs the opposite: "The second commit of a byte-identical Run returns `Committed` with its own attempt row and receipt … It must not end on the invariant row" (J1 item 11).

M3P's reason is daily use: the determinism suite and the dogfood checkpoint re-run identical analyses, and so re-commit identical Runs (M3P:577).

## Decisions

1. **Location (lead decision).** For the operation's store S (X3a's endpoint) and namespace N (X2's ACTIVE row):
   - the evidence ledger is `I/stores/S/projects/N/ledger.sqlite`, with its `-wal` and `-shm` beside it, exactly as owner201's `LedgerNames::ledger_relative` already spells it;
   - the content-addressed objects are `I/stores/S/projects/N/objects/sha256/<64 lowercase hex>`, one physical CAS per (S, N). There is no cross-namespace or cross-store deduplication (host-foundation and the blueprint's per-project CAS rule).
   - **Directories.** `projects/`, `projects/N/`, `objects/` and `objects/sha256/` are created or admitted on first need with 465 item 3's create-or-admit rules (exclusive `mkdirat` 0700, raw `EEXIST` alone leads to admission, the zero-rights owner allow, the directory's own barrier and its parent's), under the namespace's writer lease. They are store data, not trust state, so S7's "never under a lease" rule for trust does not apply; the writer lease is what excludes another writer of N.
   - **Rejected:** creating them inside X2e's fence hold. That would add store writes to the trust-ordered handoff for no exclusion it does not already have, and would require an X2 amendment.
2. **Ledger creation (lead decision).** A namespace with no ledger gets one, created under the writer lease, as:
   1. exclusive no-follow create of `ledger.sqlite` (no adoption of an existing name);
   2. one SQLite transaction that runs the selected DDL fragments, in the order the product already pins them (`attempt_custody`, the receipt/association pair, `evidence_availability`, `commit_run_material`, `active_run_pins`, `pin_change_facts`). WAL is selected immediately before that transaction, because SQLite cannot change the journal mode inside one. A crash between the two leaves a non-empty file with no schema, which item 2's partial-ledger rule already classifies as `LEDGER.CORRUPT`;
   3. `COMMIT` under `synchronous=FULL` and `fullfsync`, which materializes `-wal`;
   4. the directory barrier of `projects/N/`, so the new names survive;
   5. reopen through the existing `open_existing` path, verifying every table against its DDL.

   **Crash states.** A crash before step 3 leaves a file with no selected schema; a crash after step 3 and before step 4 leaves a schema whose name may not survive. Any open that finds a `ledger.sqlite` whose stored schema is not exactly the selected DDL refuses (`LEDGER.CORRUPT`, item 10); an empty file of length 0 with no `-wal` is the only state treated as "creation not begun" and is completed by the same writer under the same lease. **Rejected:** adopting a schema-less or partial file as empty, and any migration (no other ledger format exists for this product).
3. **Attempt admission before evidence work (lead decision).** Before the first object is written, the writer inserts its `attempt_custody` row (`phase = admitted`, its store generation digest, N, ExecutionId and operationRef) in its own ledger transaction and commits it durably (blueprint: "Admit the `AttemptRecord` transactionally before snapshot work"; readonly-recovery §5). This is the pre-use uniqueness record for a durable-authoritative commit-capable attempt; the `ac_no_replace` trigger refuses a reused ExecutionId. A failed commit here is `durability-undetermined` for the attempt (item 10) and stops it before any object. **Rejected:** inserting the attempt row in the final commit transaction, which would leave a crashed attempt with no `admitted` row for the sweep to settle.
4. **Object publication (step 3).** Each object is a `VerifiedBlob` whose length and SHA-256 are checked against the Run's declared digest before any write. Publication reuses `blob_store`:
   - **New name.** `publish_new_regular` writes a private temporary file under `objects/sha256/`, takes its file barrier (`F_FULLFSYNC`), links it exclusively to the digest name (never replacing), and takes the directory barrier; the receipt's directory barrier is checked against the handle.
   - **Existing name.** Only an exclusive-publication collision whose visibility is unchanged leads to `confirm_existing_regular`, which reads and compares every expected byte and completes its own file and directory barriers. Unequal bytes, a non-regular file or a length mismatch are never overwritten (F04); they refuse as `LEDGER.CORRUPT` (item 10).
   - **Order and atomicity.** All objects of one commit are published, each with both barriers, before any level-3 acquisition (step 4). A failure at any object stops publication; already-published objects stay, unreferenced (F02 to F05).
   - **Orphans.** The attempt never deletes, renames or reuses its own objects after a failure. Unreferenced objects are removed only by the existing reachability GC under `store-gc`'s exclusive lease (readonly-recovery §4.3 step 5). Presence of an object grants nothing (F05).
5. **The two level-3 transactions (step 4, lead decision on ownership).** After the objects, X3c acquires the evidence ledger's `BEGIN IMMEDIATE` with `busy_timeout = 0` only after X3d holds X3b's open journal transaction, never the reverse:
   - grant journal first (X3b), evidence ledger second (X3c), both non-waiting;
   - if the ledger acquisition is busy or fails, X3c returns the failure without holding any ledger transaction, and X3d releases the journal transaction through X3b's consuming abort (F06);
   - neither is acquired while level 4 (`JournalAppendLock`) is held, and level 3 is never reacquired under level 4.

   X3c's handle is a private, owned, single-use `PreparedLedger` wrapping `WriteTransaction`; it has no SQL surface, is not Clone, and its `Drop` attempts only a local rollback. **Rejected:** a waiting ledger acquisition, and a ledger transaction opened before the objects are durable.
6. **Staging and the prepared commit (step 6, lead decision on the adapter boundary).** After X3b's `SEAL` and its `COMMITTED` witness are durable, X3d's staging callback receives X3b's opaque `JournalSealBinding` and hands X3c exactly the joined values. X3c then, in the open `PreparedLedger`, with nothing committed:
   - **r8:** first reads the Run's standing in (S, N), and on a re-commit compares the Run material, before any insert (item 6a.2 and 6a.3);
   - inserts the exact receipt and the thirteen-field private association through the existing `stage_recovery_pair` (savepoint, poisoned on partial insert, join checked by `join_ledger`);
   - inserts the Run's manifest material (`commit_run_material`) and its object references through their existing private mechanisms, each schema-verified. **r8:** On the Run's first commit in (S, N) only, it also inserts the availability record and the authorized pins the same way. A re-commit stages neither (items 6a.4 and 6a.5);
   - returns the owned prepared-commit adapter, whose one consuming method performs only `COMMIT`.

   All payload admission, association construction and SQL staging precede X4's `FinalGate::admit`; the adapter's commit runs only with the single-use `AdmissionPermit`. A staging failure aborts the ledger transaction without commit (F11: all required rows or none; a lone `SEAL` is never a commit). **Rejected:** committing inside the staging callback, and storage minting any security type.
6a. **Re-commit of a Run already committed in the same store and namespace (r8).** R is the Run's RunId. E1 is an attempt whose commit of R landed in (S, N), and E2 is a later attempt that commits R in the same (S, N).
   1. **Identity: the same Run, committed again by a new attempt (lead decision R8-1).**
      - **The same Run.** The RunId is the Run's content identity. Staging admits the manifest as R's identity candidate and refuses one whose identifier is not R (`parse_material`, `ledger_store/recovery_material.rs:90-104`). ExecutionIds, receipts and operation references are excluded from Run identity (IE:104-107). So "a new Run with the same content" cannot exist: it would need an operational value inside Run identity.
      - **A new attempt.** E2 has a fresh ExecutionId (X3d item 2), its own `attempt_custody` row (item 3) and its own `SEAL`. It also has its own receipt, association and Run-material row, each keyed by E2. E2's receipt names R and R's inventory digest, and takes the next `commitSequence` of (S, N) (`ledger_store.rs:724-753`).
      - **The outcome.** E2 ends `Committed(PublishedCommit)` exactly as a first commit does (X3d item 6). This is IE's "Duplicate retry can share a Run but has a separate attempt receipt" (IE:1683), and what J1 item 11 requires.
      - **Rejected:**
        - **Returning E1's receipt as E2's result.** Storage builds `PublishedCommit` only after the attempt's own `COMMIT` returned success (X3d item 1), and reading an outcome back on the write path is forbidden (item 11). It would also leave E2's row with no receipt, so the sweep would settle `refused` an attempt the caller was told had succeeded.
        - **Refusing, as M2 does.** P5-2 rejects it, because durable repetitions would refuse (M3P:578).
        - **Reusing E1's ExecutionId, `SEAL` or rows.** "Retry always receives a new ExecutionId" (IE:104), `ac_no_replace` refuses it, and F34 tests it.
   2. **Standing: decided only from R's committed per-Run rows, inside the transaction (lead decision R8-2).** Staging's first step, inside the open level-3 transaction and before any insert, reads two things under the attempt's store generation digest and N:
      - R's current availability record, through the existing indexed read (`load_current_availability`, `ledger_store.rs:805-823`);
      - whether any Run-material row names R (`commit_run_material.run_id`).

      Three outcomes:
      - **Neither exists: first commit.** It is staged exactly as r7 item 6 stages it: availability generation 0 `retained`, and the pins as a first publication.
      - **Both exist: re-commit.** It is staged by items 6a.3 to 6a.5.
      - **Exactly one exists: refuse, `LEDGER.CORRUPT`** (item 10). The commit transaction writes both or neither (item 6; F11), and neither table admits a delete (`availability_no_delete`, `run_material_no_delete`). So a one-sided Run is a state no writer of this product leaves.

      What standing never reads: attempt rows or their phase, `SEAL`s, objects, staging residue, or another transaction's uncommitted state. That has these consequences:
      - **An attempt that stopped before its `COMMIT` landed** (an orphan `SEAL`: F09, F11, F19, F38) leaves no per-Run row. The next commit of R is a first commit, as X9's F36 already expects: "The RunId is not blacklisted" (X9:1129).
      - **An attempt whose `COMMIT` landed** is committed, whatever its attempt phase. A receipt with an `admitted` row is the lawful interval before the settle write (IE:1689-1692). So the next commit of R is a re-commit, including after a `CommitUndetermined` whose `COMMIT` in fact landed (F12, F40).
      - **The earlier attempt stays X6's.** A re-commit does not act on an `admitted` attempt or on an undetermined commit. It neither reads nor changes the earlier attempt's row, phase, `SEAL` or outcome. It reads only the per-Run rows that the earlier attempt's landed `COMMIT` wrote. Settling the earlier attempt and recovering its outcome stay with X6 and X3c item 7, exactly where J-RW's out-of-scope list leaves them (J-RW:79-81). So no state is claimed by both laws: X6 owns the earlier attempt, J-RW owns L11's crash prefixes, and this item owns only E2's own attempt.
      - **No race.** The writer lease and `BEGIN IMMEDIATE` exclude every other writer of N across the read and the inserts (S7; item 8). Two attempts cannot both stage a first commit of R. If one ever did, the second generation-0 insert would still hit `availability_no_replace`.
      - **"The same store and namespace"** means the store generation digest and N, the key of every per-Run row. A commit under another generation of (S, N) is not a re-commit. No M3 writer changes a generation (X9 L5).
      - **Rejected:**
        - **Deciding standing in `prepare_commit`, before the attempt row.** That read is outside the transaction that inserts, so staging would have to repeat it. It could only move earlier a refusal that only a mutation reaches.
        - **Standing from receipts.** `commit_receipts` has no RunId column, so every receipt body in N would be parsed.
        - **Standing from the attempt row's phase.** Settlement is X6's (item 11), and a landed commit stays `admitted` until the sweep.
        - **Treating a one-sided Run as a first commit.** With R's availability record present, the generation-0 insert hits `availability_no_replace`, which is M2's invariant refusal. With R's material present and its availability record missing, a new generation 0 would restart a monotonic history whose earlier generations were lost, and so hide the loss.
   3. **Byte-identical material (lead decision R8-3).** On a re-commit, before any insert, staging compares E2's manifest and inventory with R's committed Run material: the material row of R in (S, N) with the least ExecutionId in byte order. Both bodies must be byte-identical. Otherwise staging refuses on the invariant row (item 10), inserts nothing, and the transaction rolls back.
      - **Why one row suffices.** Every committed material row of R entered either as R's first commit or after passing this comparison. By induction they are all byte-identical. The least ExecutionId makes the choice deterministic, so a changed row is found the same way in every repetition.
      - **Why this is the right test.** The manifest is R's identity preimage, so equal RunIds already mean equal manifests (6a.1). The comparison adds the inventory: the exact typed objects and raw blobs the commit publishes, which the receipt's `inventoryDigest` authenticates. Identical semantic inputs replay to identical retained evidence (IE:104-107). The retained evidence keeps its objects and blobs in ordered maps (`crates/identity/src/closure.rs:1543-1558`), and `plan` lists them in that order (`commit.rs:261-298`). So a lawful re-commit's inventory is byte-identical. A different one is IE's regeneration mismatch, which "refuses" (IE:1825-1827).
      - **Why the invariant row.** The cause is either a producer that did not replay deterministically, or a stored row changed outside this law. The writer cannot tell which, and it repairs neither. Recovery of E1 still reports E1's own join (X6 r4 item 4).
      - **Rejected:**
        - **No comparison.** One RunId in one namespace could then carry two inventories, each authenticated by its own receipt.
        - **Comparing every earlier row.** The work would grow with R's commit count, and induction already covers it.
        - **Comparing the receipts' `inventoryDigest`.** It parses a receipt body. The material row is what recovery reads and joins.
        - **`LEDGER.CORRUPT`.** It would label a replay defect as storage damage.
   4. **Availability: written once, by R's first commit (lead decision R8-4).** A re-commit stages no availability record. R's current record stays current and unchanged, whatever its generation and state.
      - **Why.** Availability belongs to the Run, keyed by RunId, not to a receipt: "a separate monotonic-generation record" (IE:1721-1724). The first commit writes generation 0 `retained`. A successor is an availability owner's transition (`availability.rs:1-3`, `:104-128`), and "an availability transition increments generation" (IE:1814-1815).
      - **How this reads IE's commit order.** Step 3 lists what one transaction inserts for a Run, including the "retained availability generation" and the pins (IE:1670-1673). For a duplicate retry, which "can share a Run but has a separate attempt receipt" (IE:1683), the shared Run's availability and pins already exist. The re-commit's transaction inserts the separate receipt, its private association and its per-attempt material. The shared per-Run rows stay as they are.
      - **At M3 the record is always generation 0 `retained`.** X3c-2's staging is the only production caller of `stage_availability` (`project_commit.rs:503-511`). No purge, expiry or restoration writer exists (X9 L5, L6). Another state is reachable only by mutation, as X9's F52 `availability-purged` does. There the re-commit is `Committed`, and the record stays as it is (RC-9). Recovery judges availability from the objects themselves, and uses the record's state only to label an object that is missing (`crates/storage/src/recover.rs:432-458`). So it reports what is actually present.
      - **Regeneration is not claimed.** IE lets availability "improve through verified restoration or regeneration" (IE:1724), and a byte-identical re-commit has replayed and confirmed every object. Whether that suffices to write a `retained` successor belongs to the retention and restoration owner (M5). That owner must also order it against purge and GC, which "follows the admitted retention policy, pins and availability generations" (SL:1456). Until then the record can lag the objects: a re-commit can make every object present again while the record still reads `purged`. Reconciling the record is that owner's work, not a re-commit's.
      - **Rejected:**
        - **A generation-0 record on every commit.** That is the M2 defect (`availability_no_replace`).
        - **A `retained` successor on every re-commit.** It would make the generation count attempts rather than availability changes, and add an availability writer whose positive claim this law cannot order against GC and pins.
        - **Refusing a re-commit whose record is not `retained`.** No existing row fits, and the refusal would follow a durable `SEAL`. Once a purge writer exists, every durable repetition of that project would refuse, which P5-2 rejects.
   5. **Pins: written once, by R's first commit (lead decision R8-5).** A re-commit stages no pin change. R's active pins are a per-Run set, keyed by RunId (`active_run_pins`, `ledger_store/recovery_pins.rs:15-22`). R's first commit publishes the declared set, and later changes belong to the pin owners' own operations.
      - **At M3 the declared set is empty** (`STAGING_LIMITS`, `commit.rs:56-60`; `:732`), so a re-commit leaves out nothing it declared.
      - **A declared pin is never silently dropped.** X3c-3 keeps this explicit: on the re-commit branch, a non-empty declared set refuses on the invariant row before any insert.
      - **Rejected:**
        - **Staging the declared set as a first publication again, as M2 does.** With an empty current set it is a no-op (`pin_inventory.rs:146-182`). But once a pin has been added since R's first commit, it refuses `StaleInventory` (`ledger_store/pin_transactions.rs:94-97`), so every re-commit of a pinned Run would refuse.
        - **Replacing the current set with the declared one.** A re-commit would clear another owner's pins.
        - **A merge rule now.** No commit declares pins at M3. The successor that lets a commit declare them decides how a re-commit's set joins the current one ("Not claimed").
   6. **What each commit writes.**

      | Row or object | R's first commit (E1) | A re-commit of R (E2) |
      |---|---|---|
      | `attempt_custody` | E1's row, `admitted` (item 3); X6's sweep settles it | E2's own row, the same way |
      | objects | each published new, or confirmed (item 4) | each confirmed byte for byte, or published new if it is missing. A corrupt object refuses (`LEDGER.CORRUPT`, F04) and is never overwritten |
      | `commit_receipts` | E1's receipt | E2's receipt: the same RunId, `namespaceId`, `inventoryDigest`, `sealedAssurance` and `signerKeyId` (the facade's constants, `commit.rs:48`, `:53`); its own ExecutionId and the next `commitSequence` |
      | `commit_associations` | E1's association | E2's association: its own `SEAL`'s carrier, grant generation and sequence |
      | `commit_run_material` | E1's row | E2's row, byte-identical to E1's (6a.3) |
      | `evidence_availability` | generation 0 `retained` | nothing (6a.4) |
      | `active_run_pins`, `pin_change_facts` | the declared set, as a first publication | nothing (6a.5) |
      | rows of earlier attempts | — | byte-unchanged. Receipts, associations, material, availability and pin facts refuse replacement, update and delete by trigger. An `attempt_custody` row changes only by the sweep's one settle (X6 r4 item 7) |
   7. **Idempotence.** A byte-identical re-commit is idempotent on the Run and additive on attempts.
      - **Unchanged.** After it, R's identity, material bytes, inventory, objects, availability and pins are exactly as before, and every earlier ExecutionId recovers as it did.
      - **Added.** One attempt row, one `SEAL`, one receipt, one association, one Run-material row and one `commitSequence`. Repeating it adds one more of each.
      - **Not a no-op** (6a.1).
      - **Its storage cost** is one Run-material row per commit, a copy of the manifest and inventory. That is what recovery reads per ExecutionId (X6 r4 item 4). Folding it into one per-Run row would need a DDL change (6a.9).
   8. **Different content in the same namespace.**
      - **A different RunId is not a re-commit.** It is the first commit of another Run. No row of R is read for its decisions or written: per-Run rows are keyed by RunId, and per-attempt rows by ExecutionId.
      - **The same RunId with a different manifest cannot be staged.** The manifest must be R's identity preimage (6a.1), so staging refuses (`StagingMismatch`, the invariant row) and rolls back.
      - **The same RunId with a different inventory** is the regeneration mismatch (6a.3). It is refused, nothing of R changes, and `finish` revokes E2's durable `SEAL` (X3d item 7).

      In every case nothing an earlier commit wrote is overwritten, and no two Runs share one RunId.
   9. **No DDL change, no new crash point, no new type or outcome (lead decision R8-6).** X3c-3 changes staging only.
      - **No DDL change.** Item 2 verifies every stored table against the selected DDL, and a mismatch is `LEDGER.CORRUPT`. A new index or per-Run table would make every existing ledger fail that check, or need a migration, which item 2 forbids. The standing read scans N's material rows for R. `next_commit_sequence` already scans N's associations the same way (`ledger_store.rs:724-753`).
      - **No new crash point.** The standing read and the comparison are reads inside the open transaction, before `stage-recovery_pair`, and have no durable effect. A death there leaves the state that a death at `x3c.evidence.begin` leaves.
      - **The trace.** A re-commit reaches `x3c.evidence.stage-recovery_pair` and `stage-run_material`. It does not reach `stage-availability` or `stage-pins`. A first commit's trace is unchanged.
      - **No API or type change.** `prepare_commit`, `publish`, `CommitOutcome` and `PublishedCommit` are unchanged (X3d items 1 and 6). `commit.rs` still builds the initial availability record and the empty pin set, and staging uses them only on a first commit.
      - **No new public code, row or detail** (item 10).
      - **Rejected:**
        - **A `stage-standing` crash point.** It would add a kill row for a read with no durable effect.
        - **A unique index on `run_id`.** That is a DDL change.
        - **A `ReCommitted` outcome.** It would tell callers something that X7 and J1 must not treat differently from `Committed`.
7. **Durability of the commit (F12 to F14).** The ledger is WAL with `synchronous=FULL`, `fullfsync=ON` and `checkpoint_fullfsync=ON`, so a `COMMIT` that returns success has passed its WAL barrier; no further barrier is owed for a ledger whose names were barriered at creation (item 2). Outcomes:
   - `COMMIT` returns success: the commit is durable. Only then may X3d produce `PublishedCommit` (F13, F14).
   - `COMMIT` returns an error or the connection is lost: `CommitUndetermined`. The attempt's D9 response is `durability-undetermined` with its ExecutionId (item 10); the attempt never retries, never infers absence and never writes again with its stopped session (F12). The `attempt_custody` row stays `admitted`; read-only recovery (X6) and the authorized sweep decide it.
   - Acknowledgement lost after a durable commit: the receipt is the authority; a fresh read-only lookup (X6) confirms it (F14). Recovery never re-runs the mutation or writes a second receipt (F15).
8. **Locks (lead decision on scope).** Objects and ledger creation run under the namespace writer lease (S7 level 1), never under the fence alone and never with level 3 or 4 held. The ledger write transaction is level 3; the commit happens while X3b's level 4 is still held, as X3b r5 item 5 step 7 requires on the `SEAL` path. The full order is:
   1. the journal transaction (level 3);
   2. the ledger transaction (level 3);
   3. level 4;
   4. `SEAL` and the durable `COMMITTED` witness;
   5. staging;
   6. X4's repeated checkpoint and `AdmissionPermit`;
   7. the ledger `COMMIT`;
   8. release level 4 once the `COMMIT` returns `Committed` or `CommitUndetermined`.

   Level 3 is never acquired or reacquired under level 4. **If the path stops before the evidence `COMMIT`** (a staging failure, a failed repeated checkpoint, no `AdmissionPermit`, an observer latch, or any error after `SEAL`), the order is fixed. Roll back the open ledger transaction, which writes nothing. Release level 4, then each level-3 transaction. Then follow F19: append `REV` through a fresh, lawful level-3-then-level-4 acquisition (X3b r6 item 6). Level 3 is never reacquired under level 4. Every exit from the `SEAL` path releases level 4 exactly once: `Committed`, `CommitUndetermined`, or this failure path. (X3b r6 item 5 step 7). Read-only paths open only `ReadSnapshot` and never take level 3 or 4. **Rejected:** releasing level 4 before the evidence commit on a path that continues to `COMMIT`, which would let a `REV` slip between `SEAL` and commit. A path that stops before `COMMIT` releases level 4 by the stop order above and never commits, so no `REV` can slip in before a commit.
9. **Budget (lead decision).** Every step charges the operation's ledger (X1's attempt ledger, which X4 r4 already uses for checkpoint work), reserving post-effect confirmations before each effect:
   - per object: one object and its edges for the temp file, link, both barriers and any confirmation read, plus its byte length;
   - the attempt-row transaction, the level-3 acquisition and the staged rows: fixed object and edge costs per statement, plus the staged body bytes;
   - ledger and directory creation (items 1 and 2): their create-or-admit costs from 465.
   - **r8: the standing read and the comparison.** The standing read (6a.2) is charged as fixed statement costs, as `next_commit_sequence`'s scan of N's associations already is (`project_commit.rs:66-72`). The comparison (6a.3) reads at most E2's own manifest and inventory lengths from R's stored row: lengths are compared first, so a longer stored body is never read. Both are inside staging's existing reservation, taken before the first insert (`project_commit.rs:436-456`). A re-commit is not charged for the availability or pin statements it does not run.

   A commit whose declared objects and staged bytes cannot be reserved refuses on the budget row before the first object is written; it is never truncated. The owner's 256 MiB cap therefore also bounds one commit's new object bytes. **Rejected:** an uncharged blob path, and charging per tick.
10. **Refusal rows (existing details only).** Each failure maps through 468c's `InstallationTermination` (or the D9 standings of readonly-recovery for durability), with no new code:
    - a busy ledger at level 3, or a busy writer lease: `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, `PROJECT.BUSY` (F06);
    - a ledger whose stored schema is not the selected DDL, a partial creation footprint other than item 2's resumable empty file, or an object collision with unequal bytes, length or type: `LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted (readonly-recovery's quarantine row; never `MIGRATION.CORRUPT`);
    - an object, directory or ledger I/O failure before any `COMMIT` was attempted: `HOST.IO_FAILURE`, `host-io`;
    - a failed or uncertain `COMMIT` (items 3 and 7): `DURABILITY.COMMIT_FAILED`, `durability-commit`, ExecutionId retained, `runId` omitted, no retry;
    - a reused ExecutionId refused by `ac_no_replace`: the invariant row (`SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, `HOST.INVARIANT_VIOLATED`), since ExecutionId uniqueness is the host's own pre-use rule;
    - budget: `WORK.BUDGET_EXHAUSTED`.
    - **r8: a lawful re-commit is not refused** (6a.1). Three conditions are added, each on an existing row:
      - a re-commit whose manifest or inventory is not byte-identical to R's committed material (the regeneration mismatch, 6a.3), or whose declared pin set is not empty (6a.5): the invariant row;
      - a one-sided Run, meaning R's availability record without any Run material of R, or the reverse (6a.2): `LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted.

      Each is a staging refusal after the durable `SEAL`. X3d's stop order and `finish`'s `REV` and `CLN` follow (X3d items 4 and 7).

    Where S12 or the public detail registry fixes a class for a code, it prevails.
11. **The recovery boundary with X6.** X3c writes only: the attempt row, objects, and the one commit. It never reads its own outcome back to decide commitment, never settles `attempt_custody`, never deletes objects and never writes after a failure. Read-only recovery (readonly-recovery steps 0 to 4) and the settlement sweep (§4) are X6's and use only `ReadSnapshot`. A fault-injection hook is absent from every non-test build (`cfg(test)` or X9's `crash-matrix` feature). **r8 (record):** that sentence restates r7's "exists only under `cfg(test)`", as X9's G2 asks (X9:1219; M2C §5 row 6). It changes no rule. **r8:** a re-commit's standing read and comparison (6a.2, 6a.3) read only R's committed rows. They are not a read-back of the attempt's own outcome.
12. **Failure-case coverage.**
    - **Covered by X3c:** F02, F03, F04, F05 (object publication), F06's evidence half (non-waiting level-3 acquisition and orphan preservation), F11 (all rows or none), F12 (undetermined commit, no retry), F13 (no `PublishedCommit` before a confirmed commit), and the write side of F14 and F15 (one commit, no second receipt).
    - **Prepared for others:** F14 and F15's read-side confirmation (X6), F38 to F41 (X4 and X3d's gate), F32 and F34 (X3d).
    - **r8:** IE's duplicate retry (IE:1683) and regeneration mismatch (IE:1825-1827) are covered by item 6a. F36's "the RunId is not blacklisted" is kept: an attempt that stopped before its `COMMIT` leaves no per-Run row (6a.2).
12a. **Tests while X2e is pending.** Tests in `opensip-storage` use a crate-private, `cfg(test)` location fixture: a scratch installation whose `stores/S` comes from `installation_read_fixture`, with a test N and a held test writer lease. They cover: ledger creation and each creation crash state; attempt admission and a reused ExecutionId; object publication new, confirmed existing, and unequal collision; a crash at each object step (temp write, before file barrier, after link, before directory barrier) via crate-private step hooks; non-waiting level-3 busy; staging all-or-none; commit success; a `COMMIT` error classified as undetermined; budget refusal before the first object; and that no path deletes an object. No production seam or cross-crate bridge exists; the real composition test lands with X3d.
12b. **X3c-3's tests (r8).** They run in `opensip-storage`'s ordinary lanes. The composition goes through X3d's facade with a real session, obtained through `scenario-fixtures` as X3d-3's tests obtain it (X3d r8 item 13).
    - **The re-commit.** Committing the same candidate twice ends `Committed` both times. The second adds exactly 6a.6's rows: `commitSequence` is one higher, there is one availability row, the pin tables are unchanged, and every object is `ConfirmedExisting`. A raw dump of every earlier row is byte-identical before and after.
    - **A third commit.** `recover` of each ExecutionId reports committed (X6).
    - **Standing from committed rows only:**
      - an earlier attempt killed after its `SEAL` and before its `COMMIT` leaves no per-Run row, so the next commit is a first commit (availability generation 0);
      - an earlier `COMMIT` that landed and was reported undetermined (the `fail-after` hook) makes the next commit a re-commit.
    - **The refusals,** each with nothing inserted and the transaction rolled back:
      - **regeneration mismatch:** R's stored inventory changed through a crate-private hook, with its trigger lifted and reinstalled byte-identically: the invariant row;
      - **one-sided:** availability without material, and material without availability: `LEDGER.CORRUPT`;
      - **declared pins:** a re-commit with a non-empty declared pin set, through a crate-private hook: the invariant row.
    - **A non-retained record.** A test writes a generation-1 `purged` successor. The re-commit commits, and the record is unchanged.
    - **Another namespace.** A commit of R in another namespace of the same store is a first commit there.
    - **The first commit is unchanged.** r7's staging tests stand, and its trace reaches the same `x3c.evidence` points.
    - **Budget.** Staging's reservation one unit short refuses before the first insert, on a first commit and on a re-commit.
13. **Units after the law.**
    - **X3c-1:** locations for the ledger and objects, directory create-or-admit, ledger creation and its open, and attempt admission. Inventory successor.
    - **X3c-2:** object publication over `blob_store`, the non-waiting level-3 `PreparedLedger`, staging, the prepared-commit adapter and the durability classification. Inventory successor.
    - X3d composes X3b, X3c and X4 into `CommitSession`.
    - **X3c-3 (r8; storage code, M, plus one serialized X9 lead set).**
      - **`ledger_store/project_commit.rs`.** `PreparedLedger::stage` gains the standing read, the comparison and the two branches (6a). `classify_staging` gains the one-sided `LEDGER.CORRUPT` mapping. The module and method docs are updated.
      - **`ledger_store.rs` and `ledger_store/recovery_material.rs`.** The private standing read and comparison go on `WriteTransaction`, beside `stage_run_material`, with the same schema verification every staging accessor runs.
      - **`commit.rs`.** Only doc comments change (`:10-15`, `:701-710`). The values handed to staging are unchanged.
      - **Tests:** item 12b.
      - **Matrix:** item 14's RC rows and census child, in `crates/storage/tests/commit_tests.rs` and storage's `required-runs.v1.json`, transcribed by X9 r17 (CL-2).
      - An inventory successor.
      - **Depends on:** this law's acceptance and X9 r17's rows. It lands before J3d (M3P:237; J1 S14), by M3 day 25.
      - **The lead set.** Two repetitions of both targets on X3c-3's integration commit: storage's 381 rows plus the RC rows, and host's 98. They are checked by `check`, with the union census and kill-set coverage (X9 item 7 and r16). The host target is rerun because every host commit passes the changed staging. The set is serialized with every other lead set, because of the 5000 ms timing guard (M3P:421).
      - **Integration order with J4 (J-RW:359).** X3c-3's lead set and J4's are independent, and neither unit depends on the other. Whichever of X3c-3 and J4 integrates second reruns both units' X9 rows: this law's RC rows and J-RW's RW rows. If J4 integrates first, X3c-3's set therefore covers storage's rows, the RC rows, the RW rows and host's rows.
14. **The crash windows and the rows X9 r17 carries (r8; lead decision R8-7).** A re-commit runs the same composition as a first commit: the same `prepare_commit`, journal, level-3, level-4, gate and `finish` steps (X3d items 3, 4 and 7). It differs in three windows: its objects are confirmed rather than created; staging takes the re-commit branch; and its landed `COMMIT` adds attempt rows only.
    - **Row ids** are this law's. X9 r17 (record and rows; the lead) fixes their `case` and `variant` spellings, for example as `recommit-` variants of the F-case each row names. It transcribes them into storage's `required-runs.v1.json` before any run, and never reads an expected value back from a run (X9:1089).
    - **Notation,** as X9 item 8: E1 is the candidate's first commit; E2 is the re-commit under test; E3 is a next writer (R2) that commits the same candidate (`{"r2": "same"}`, beside X9 r12's `{"r2": "distinct"}`). "recover(E1)" is an extra read-only step, as r12's R5 recovers a second ExecutionId. Labels follow X9 item 4.

    | Window | Steps | Rows |
    |---|---|---|
    | W-R0. Before E2's attempt row | preflight, layout, `x3c.attempt` | none new. As F00; standing is not yet read |
    | W-R1. Objects, confirm branch | per already-present object: `create`, `write`, `file-barrier`, `link.before` (the collision), `file-barrier`, `directory-barrier`, `reopen-confirm` | RC-2 |
    | W-R2. The `SEAL` path | X3b's append and X4's checkpoints | none new. The journal does not know the Run is committed, so these steps are a first commit's (F07 to F10, F19) |
    | W-R3. Staging, re-commit branch | the standing read and comparison (no point), `stage-recovery_pair`, `stage-run_material` | RC-3; refusals RC-6, RC-7 |
    | W-R4. The evidence `COMMIT` | `x3c.evidence.commit` | RC-4 |
    | W-R5. After a landed `COMMIT` | `commit.after` to `x3d.finish.end-step.after` | RC-5 |
    | Readers across W-R1 to W-R5 | — | RC-8 |

    The rows:
    - **RC-1. A lawful re-commit, and the census child.** E1 and E2 both commit the candidate, with nothing armed.
      - **Expected:** both `Committed(latched=false)`. E2's `commitSequence` is 2. The ledger holds 2 attempt rows, 2 receipts, 2 associations, and 2 Run-material rows with equal manifest and inventory. It holds 1 availability row (generation 0 `retained`), and the pin tables are empty. E2's trace has no `x3c.object/link.after`, because every object is confirmed. E1's rows are byte-equal before and after E2.
      - **Ladder:** R1(E2) CH `pendingSettlement`; R2 (E3) `Committed`; R3 settles every attempt `committed`; R4(E2) CH `settled`; recover(E1) CH.
      - **The census.** Storage's census gains E2 as a second commit child. It adds the confirm branch's points to the kill set: at least `x3c.object/reopen-confirm.before` and `.after` (`crates/platform/src/filesystem.rs:725`), which are absent from the union census at C (`crash-matrix-x9/evidence/3d2d5b5…/storage/census-trace.txt`), and the branch's later occurrences of the shared points.
    - **RC-2. Kills in the confirm branch** (F02 to F05's re-commit variant). E2 is killed at every kill-set point that RC-1's census child adds in `x3c.object`, at the first, a middle and the last object (X9 item 5).
      - **Expected:** E1's rows are unchanged. No object name or bytes changed; E2's staging file is never adopted.
      - **Ladder:** R1(E2) UAO; R2 (E3) `Committed`, with every object confirmed; R3 settles E2 `refused` and E3 `committed`; R4(E2) TNC; recover(E1) CH.
    - **RC-3. Staging kills** (F11's re-commit variant). E2 is killed at `x3c.evidence.stage-recovery_pair#1` and at `x3c.evidence.stage-run_material#1`.
      - **Expected:** the evidence transaction rolls back. E2's `SEAL` is durable with no `REV`, because the process died before `finish`. E2 has no receipt or material, and there is still 1 availability row.
      - **Ladder:** R1(E2) UAO; R2 (E3) `Committed`, witness action OK; R3 settles E2 `refused`; R4(E2) TNC; R5 recover(E3) CH, and E2's orphan `SEAL` and E3's `SEAL` name one RunId (F36's check); recover(E1) CH.
    - **RC-4. The undetermined `COMMIT`** (F12's and F40's re-commit variant): `fail-before` and `fail-after` at `x3c.evidence.commit` on E2.
      - **Expected:** `CommitUndetermined`, with E2's ExecutionId and no RunId, `end(rev=false, cln=false, …)`, and the reserve forfeited. With `fail-after`, E2's receipt, association and material exist; with `fail-before`, none of them do. Either way there is 1 availability row.
      - **Ladder:** R1(E2) CH `pendingSettlement` (landed) or UAO (not landed); R2 (E3) `Committed`; R3 `committed` or `refused`; R4 CH or TNC; recover(E1) CH.
    - **RC-5. The lost acknowledgement, with a same-Run next writer** (F13's to F15's re-commit variant). E2 is killed at `x3c.evidence.commit.after#1`, `x3d.publish.commit-returned#1`, `x3d.publish.published#1` and `x3d.finish.end-step.after#1`.
      - **Ladder:** R1(E2) CH, with `pendingSettlement` as F13 to F15 give it; R2 (E3) `Committed` with `commitSequence` 3, and no second receipt for E2; R3 `committed`; R4(E2) CH `settled`.
      - **Expected:** 1 availability row throughout.
    - **RC-6. A regeneration mismatch** (mutation; the same mutation as F33's `run-material-inventory`). After E1 commits, the parent replaces E1's stored inventory with a different canonical inventory that names R. It uses X9 item 6's reserved-slot technique: lift `run_material_no_update`, write, reinstall it byte-identically. E2 then commits the candidate.
      - **Expected:** E2 `Refused(Invariant)` at staging, `end(rev=true, cln=true, …)`. E2 has no receipt, association or material, and there is still 1 availability row. E2 does not change E1's rows.
      - **Ladder:** R1(E2) UAO; R3 settles E2 `refused`; R4(E2) TNC.
    - **RC-7. A one-sided Run** (mutation). Two variants:
      - **(a)** after E1 commits, the parent deletes R's availability row (lift `availability_no_delete`, delete, reinstall it);
      - **(b)** after a commit of the distinct variant creates the ledger, the parent inserts a generation-0 `retained` record for R, with no commit of R.

      Then a commit of the candidate.
      - **Expected:** `Refused(LedgerCorrupt)`, `end(rev=true, cln=true, …)`, and nothing inserted.
      - **Ladder:** R1 UAO; R3 `refused`; R4 TNC.
    - **RC-8. Reader isolation** (F29's re-commit variant). E2 holds at `x3d.publish.after-staging#1`, then at `x3d.publish.commit-returned#1`. At each hold, one reader recovers E1 and another recovers E2.
      - **Expected:** E1 is CH both times: the snapshot never contains E2's staged rows, and R's availability is unchanged. E2 is UAO, then CH `pendingSettlement`, as in F29. Readers take `readers.lease` beside APPEND-WRITE without waiting.
    - **RC-9. A non-retained record** (mutation; F52's `availability-purged`: an availability successor, generation 1 `purged`, and the largest object deleted). After E1 commits, the parent applies it. E2 then commits the candidate.
      - **Expected:** E2 `Committed(latched=false)`. E2 publishes the deleted object new and confirms the rest. No availability row is added, so generation 1 `purged` stays current.
      - **Ladder:** R1(E2) CH `pendingSettlement`, because every object is present again (`recover.rs:432-458`); recover(E1) CH.

    **Existing rows (record for X9 r17).**
    - **No transcribed expected value changes,** and every first commit's trace is unchanged (6a.9).
    - **19 runs have an unscored same-Run commit.** In these runs of the accepted storage set at C (`crash-matrix-x9/evidence/3d2d5b5…/storage/runs/`), an unscored next writer, or F49's scripted second writer, commits the candidate after the candidate was committed. Each ends `Refused(Invariant)` today:
      - F12 `fail-after-evidence-commit`;
      - F23 `delete-receipt` and `delete-association`;
      - F27's four association variants;
      - F28 `pruned-generations`;
      - F33's four variants;
      - F40 `fail-after-evidence-commit`;
      - F49 `reader-skewed-by-append`;
      - F52 `association-only`, `no-row-both`, `purged`, `receipt-only` and `settled-refused-both`.
    - **What they should give under r8.** Each is expected to end `Committed`, except where its mutation makes R one-sided (6a.2) or changes R's Run material (6a.3). By this law's reading of the matrix mutations (`crates/storage/tests/commit_tests.rs:2502-2657`), only F33 `run-material-inventory` changes R's material, so it stays on the invariant row by RC-6's rule. None makes R one-sided. F52 `purged` ends `Committed`, as RC-9 does. So 18 of the 19 change outcome.
    - **What follows.** R3's unscored `nextWriter` member follows that outcome, and the post-state digests change. The two new lead repetitions must still agree with each other. X9 r17 derives each run's new outcome from this law before the lead set. It confirms that no expected value names those outcomes, and re-transcribes any that does.
    - **The distinct variant stays** where X9 r12 and r13 put it. Those rows still test that the next writer proceeds after a committed Run. RC-5 adds the same-Run next writer beside them.
    - **Rejected:**
      - **Re-killing every first-commit point on a re-commit child.** The kill set is by point name and occurrence (X9 r16), and the shared points stay covered by the first-commit rows. This law adds rows for the windows where a re-commit's state differs.
      - **Switching F13 to F15's R2 to the same Run.** That changes accepted rows for no coverage RC-5 lacks.
15. **Interactions (r8).**
    1. **J1's commit phases and cancellation (J1 item 8).** A re-commit has the same phases:
       - **A** until its attempt row commits;
       - **B** through object confirmation, the `SEAL` and staging;
       - **C** from `FinalGate` admission;
       - **D** after an unlatched `Committed`;
       - **O** and **E** as J1 states them.

       The re-commit branch adds no window bit, latch source, checkpoint, crash point or `REV` reason.
       - **In B,** J1's cancellation latch (X3d r9) takes the gate 0→2, and the staged re-commit rolls back. Nothing of R changes. `finish` appends `REV(operator)`, plus `CLN` for the durable `SEAL` (F38).
       - **In C,** F39 or F40 applies by the returned outcome. Only a `Committed` carries R's RunId.
       - **In D,** the projection is `interrupted` with R's RunId. That RunId equals the earlier commits'; the ExecutionId stays the attempt's identity in the operational record.
       - **J1's 8.3 precedence** is unchanged.
       - **A refused re-commit** (RC-6, RC-7) is a certain staging refusal after the `SEAL`. It takes B's stop path and `REV` reason and projects as any staging refusal does (X7 r6 item 3).
       - **J1's S12 rows** are first-commit rows. This law asks for no re-commit variant of them, because the gate and its window do not depend on staging's branch (J1 8.1). **Rejected:** duplicating S12-B to S12-O for a re-commit.
       - **J1's requirement** (item 11) is met: E2 is `Committed` with its own attempt row and receipt. J-C21's storage half is item 12b's first two tests, and J3d keeps J-C21.
    2. **J-RW, the resume and repair writer (J-RW r1, draft; P5-1) (lead decision R8-8).**
       - **Disjoint by construction, as J-RW X-RW-9 also finds (J-RW:419-428).** J-RW completes only L11's crash prefixes: an interrupted first registration, not-yet-private store directories and ledger file, a bare-WAL ledger, and torn trust dependency files (J-RW item 1). It writes and reads no attempt row, receipt, association, availability record, Run material or pin. A ledger it completes holds the schema only (J-RW:151-163). Standing reads only committed per-Run rows (6a.2). So nothing J-RW writes can make a Run "already committed", and no L11 state holds one: a ledger holds rows only after its schema `COMMIT` (item 2).
       - **Re-commit is not repair.** E2 never completes another attempt's state: an orphan `SEAL`, an `admitted` row, staging residue, an undetermined `COMMIT` or a partial ledger. A Run left uncommitted by a crash is committed by a new attempt as a first commit (F36). A Run whose commit landed is committed again by item 6a. Neither needs J-RW. If a later writer ever produces a receipt, it does so only through X3d's facade and item 6a.
       - **The boundary J-RW asks r8 to cite (J-RW:427).** A re-commit proceeds over an earlier landed commit whose attempt is still `admitted`, or was reported `CommitUndetermined`. It does not act on that attempt (6a.2): the attempt stays with X6 and X3c item 7, as J-RW's out-of-scope list leaves it (J-RW:79-81).
       - **A ledger holding committed rows is never replaced (CL-3).** J-RW r1 already forbids migrating, truncating, renaming or deleting a ledger, and treating one with any committed schema object as resumable (J-RW:444).
       - **Text and matrix.** J-RW's X3c text follows as X3c r9, or is folded into r8's next round (CL-4). The X9 r17 sections are shared (CL-2), and the later of X3c-3 and J4 reruns both units' rows (item 13).
    3. **X3d, X6 and X7: no rule change.**
       - **X3d.** The facade and its outcomes are unchanged. Step 3.8's list (X3D:152) becomes conditional (CL-1).
       - **X6.** Recovery is per ExecutionId. It reads that attempt's receipt, association, material and attempt row, with R's availability (X6 r4 item 4). Two receipts of R recover independently, and the sweep settles each attempt (X6 r4 item 7).
       - **X7.** E2's `Committed(PublishedCommit)` projects as any `Committed` does (X7 r6 item 3).
16. **Cross-law items (r8).** Among the accepted laws, only X3d's step 3.8 wording conflicts with item 6a (CL-1). The identity contract, X6 r4, X7 r6 and J1 r3 are consistent with it. J-RW r1, the draft beside this one, is disjoint from it in meaning. It overlaps only in text and the shared matrix record (CL-2 to CL-5). Each item below names the law that must change.
    - **CL-1. X3d, record only.** The r7 known limit (X3D:51-54) is lifted by this law and X3c-3. Item 4 step 3.8 (X3D:152) lists "availability and pins" as always staged. It should read: X3c item 6's staging, with availability and pins on a Run's first commit in (S, N) only (X3c r8). The owner is X3d's next revision, X3d r9, which J1's S10 already requires. No X3d rule changes.
    - **CL-2. X9, record and rows.** This law decides what X9 r12 left undecided (X9:268). X9 r17 carries item 14 as its own section, with the prefix `RC-`: the RC rows, the census child, and the record of the 19 runs. It sits beside J1's `S12-` section (J1 S12) and J-RW's `RW-` section (J-RW X-RW-10, J-RW:429). Each section is transcribed when its unit is ready, and no section changes another's rows.
    - **CL-3. J-RW, a constraint it already meets.** A resume or repair writer must never recreate, replace or empty a ledger that holds any committed row. Doing so would turn R's next commit into a second first commit with a fresh generation-0 record: two availability histories for one Run in one (S, N). It would also lose the earlier receipts that recovery reads. J-RW r1 forbids it (J-RW:444) and completes only a ledger with no schema object (L-UNC, J-RW:151-163). There is no conflict. Any later J-RW revision must keep that substitute.
    - **CL-4. J-RW and this law both amend X3c: item 10 and the forbidden substitutes.** P5-1 has J-RW amend "X3c item 10" (M3P:573). J-RW's X3c text is its successor RW-S3: items 1, 2, 10, 12a and 13, and the forbidden substitute on partial ledgers (J-RW:385). r8 changes item 10 and the forbidden substitutes only for re-commit, and absorbs none of RW-S3. **The order (J-RW LD-11, J-RW:467):** once J-RW is accepted, its X3c text lands as X3c r9 on r8's accepted bytes. If r8 is still in review at that point, the text is folded into r8's next round as its own marked section. Neither waits for the other, and neither changes the other's clauses. **Rejected:** writing RW-S3's text into r8 now, which would put J-RW's undecided law under this review.
    - **CL-5. X3c item 2 and X3b's empty-database rule (J-RW X-RW-3, J-RW:407-409).** X3c item 2 treats only a length-0 file as "creation not begun". X3b item 3a already reuses an empty database. J-RW's RW-S3 aligns X3c with X3b under its stricter L-UNC. r8 leaves item 2 exactly as r7 has it, so it neither widens nor settles that difference. The law that must change is X3c, through RW-S3 (CL-4).
    - **Records owed after acceptance** (the lead; record only, not conflicts): EXIT-PLAN's X3c row (EXIT:70) and follow-up (b) (EXIT:171); M2-COMPLETE §5 row 11, and row 6 for item 11's G2 restatement; M3-PLAN's carry-in row (M3P:237), at X3c-3's integration.

## Forbidden substitutes

Overwriting, renaming or deleting an object after any failure; trusting an existing object name without a full byte comparison; publishing an object before its file barrier, or acquiring level 3 before every object's directory barrier; deduplicating across namespaces or stores; a waiting ledger acquisition; acquiring the ledger before the journal, or either under level 4; committing in the staging callback or without the `AdmissionPermit`; releasing level 4 before the evidence commit on a path that continues to `COMMIT` (the stop order of item 8 is not a substitute); inferring commitment or absence from a failed `COMMIT`, or retrying it; settling `attempt_custody` or reading back the outcome on the write path; adopting a partial or schema-less ledger, or migrating one; a new public code, including for an object collision; an uncharged object or staging step; a production seam that supplies a ledger or object location.

**r8:**
- staging an availability record or a pin change on a re-commit, or writing an availability successor in any commit;
- deciding a Run's standing from attempt rows, their phase, `SEAL`s, objects or uncommitted state, or outside the open level-3 transaction;
- committing a re-commit whose Run material is not byte-identical to the Run's committed material, or treating a one-sided Run as a first commit;
- returning an earlier attempt's receipt, or a `PublishedCommit` built from a read, as a re-commit's outcome;
- a re-commit that reuses, completes or settles another attempt's ExecutionId, `SEAL`, rows or staging residue;
- silently dropping a declared pin;
- a DDL change, new index, migration or new crash point for re-commit;
- an outcome that distinguishes a re-commit from a first commit.

## Not claimed

The `CommitSession` facade, `PublishedCommit` construction and the composition with X3b and X4 (X3d); read-only recovery, settlement and orphan GC (X6); pins' retention policy beyond inserting the rows the Run declares; index stores (M4); carrier or ledger migration; any CLI command; a qualified boot identity on this BASELINE-ATTESTED host.

**r8:**
- availability regeneration or restoration by a re-commit (IE:1724, :1825-1827): the retention and restoration owner (M5);
- how a commit that declares pins joins a re-commit's declared set to the current set: the successor that first lets a commit declare pins;
- re-commit across store generations (X9 L5); a commit of R in another namespace is a first commit there;
- the resume and repair writer and every L11 crash prefix (J-RW, J4), including X3c's own resumable-creation text (RW-S3);
- deduplicating per-attempt Run material.
