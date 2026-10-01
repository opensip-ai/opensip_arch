# Review: journal X3b r1

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/journal-x3b/PROPOSAL.md` is 14951 bytes, sha256 `3e85290e52025f4d2f2c46d489c3cde522b8c866af0ed773d9ba4fa283ab38cb`, matching hashes.txt. Product HEAD is `f7acb6d7f8acadcbc0bf81d141f39077d817f043`. The real OpenSIP support directory is absent. No product cargo. X2 r3 is REQUIRED-FINDINGS and its author is revising it; nothing below re-files those findings or treats that law as accepted.

At this HEAD `crates/lifecycle/src/journal_store.rs` is absent. The lifecycle crate is `leases`, `lineage`, `locations`, and `selection`. The grant-journal read side is `crates/security/src/journal_store.rs`: `CURRENT_CARRIER_DDL` checks `carrier_format = 3`, `CARRIER_CAP` is `9007199254740991`, the append trigger reserves that sequence for `TERMINAL`, and `Witness` / `CarrierFloor` decode the closed shapes. `open` still compares `project_key_digest` with SHA-256 of a `project_key` string (`journal_store.rs` around line 538). There is no `reconcile_witness` procedure yet; naming that procedure is this unit's job. EXIT-PLAN's pointer at the lifecycle path is stale. The proposal's conclusion that the lifecycle transition journal is a different owner holds.

## Item 1

X2e producing the five-field binding is sound, and X3b consuming `ProjectOperation` is sound. Owner §8 derives `{schemaVersion:1, namespaceId:N, storeInstanceId:S, storeGeneration:G, stateSchema:K}` from the selected registry's N and the admitted endpoint, and an ordinary operation acquires its lease under the fence and then releases the fence. Doing that derivation from the owners X2e's handoff has already moved, before the fence is released, matches §8. Producing it in X3b after the release would need N and the endpoint after the fence is gone. X3a r3 left the production site to this law. X3b deciding "X2e produces it" is that decision.

X2 r3's open registry-capture defect stays on X2. Once that revision lands, the Eligible row the handoff moves is R2 after first registration and R0 on reuse. This law does not restate that step.

## Item 2

The layout is acceptable, and migration stays out of M2. `grant-journal.sqlite` and `grant-journal.witness.json` under `I/host/projects/N/` are the host-foundation file names, on the installation tree X2 publishes. The host-foundation lifecycle root (`lifecycle.sqlite`, `trust.sqlite`, `lifecycle.lock`, and `projects/` under that root) is the layout owner §1b does not adopt. "Exactly the host-foundation locations" means those two file names, WAL beside the database, and the rule that neither a project key nor its digest is a path component. The floor at `I/trust/carrier-floors/N.v1` is outside the namespace, so a namespace rollback cannot roll it back (§5.4, §5.5). N as the path component matches the registry owner: stable N paths never move, and ProjectId and N stay distinct. `trust/carrier-floors/` created on first need under the fence, with 465 item 3's create-or-admit rules, is the right parent. WAL, `synchronous=FULL`, `fullfsync=ON`, and `checkpoint_fullfsync=ON` match §5.6. A fresh X2 namespace has no carrierFormat 1 or 2 carrier, so F46–F51 stay out of M2. The fresh `carrier_format` row (`first_generation` 1, no migration fields) matches `CURRENT_CARRIER_DDL`.

Two defects sit on this item. The fence-only sentence is then contradicted by items 3 and 4 (RF-1). `projectKeyDigest` is defined as a hash of a registry field the v2 owner removed (RF-2).

## Item 3

The crash table matches v8 for the states it names. An empty database with no witness is INIT again. A complete schema and row with no witness is `witnesslessRestore` only when the journal holds a record, and otherwise INIT continues at the witness. A witness with no carrier is `uncertainTailLoss`. Transactional DDL makes a partial object set unreachable on the fresh path; observing one is the format-3 footprint S12 already calls `MIGRATION.CORRUPT`.

One window is unnamed. A crash after the `COMMITTED 0` witness and before the floor rename is neither INIT nor a floor comparison (RF-4).

## Item 4

The end path's fence retake is consistent with owner §5 for a floor-only write. §5's durability reconfirmation is the entry gate of the writing operation: one gate per process, the admitted writer holding the installation fence and reconfirming I and I-parent before any semantic write. The end step is that same admitted operation. It releases the lease first, which is S7's end rule, then retakes the fence through 458c-b1's shared charged walk and no-follow fence open, reusing this invocation's write receipt. It takes no second gate. It is a floor write by the admitted writer. It is not an observation session, and it does not promote a read.

The same end path, and creation, and the start copy, write the floor while the lease is held. That contradicts S7 and item 2 (RF-1). v8 §5.4 did copy the high-water while the lease was held. S1 records that handoff as refined by S7.

## Item 5

The append order matches F06–F10 and §5.6. Level 3 is `BEGIN IMMEDIATE` with `busy_timeout` 0, and a busy transaction is never waited on. The evidence-ledger transaction comes after the journal transaction and before level 4, composed by X3d. Level 4 is the in-process mutex. The record is `seq = tail + 1`, validated by the existing parser. The witness goes `PENDING`, then `INSERT` and `COMMIT`, then `COMMITTED`, then level 4 is released. X3b exposes the journal half and the ordering rule. It does not take X3c's evidence transaction.

The file protocol matches §5.6: an exclusive temporary name `grant-journal.witness.json.<32 hex>`, write, `F_FULLFSYNC`, rename, namespace directory barrier, reopen by name and confirm bytes and identity. The floor uses the same protocol under `trust/carrier-floors/`. A leftover temporary file is ignored by name and never adopted. A fixed temporary name is rejected. A failure before visibility keeps the previous durable state. A failure after visibility (failed commit, rename, or barrier) stops every further effect, reconciles by reopening, and assumes neither state. No evidence commit proceeds on an uncertain journal barrier (F09).

`TERMINAL` matches the product. The law's append at tail `9007199254740990` is `seq = tail + 1`, which is the reserved slot `9007199254740991`. The trigger aborts that sequence unless `record_type` is `TERMINAL`. Cause `grantGenerationClosure`, and whole-generation `REV` closing the generation the same way, match v8 WA-13.

## Items 6 and 7

`JournalAppendLock` is X4's lock. One mutex per carrier per process, owned by `ProjectOperation`, acquired only after level 3 and never while waiting on the fence or a lease. It is the S6 linearization point. X4's checkpoint receives a borrow that proves level 4 is held, and X4's abstract lock is replaced by this one. Observers never take it. F19's journal half matches S6: after a failed post-SEAL checkpoint, abort any open journal transaction, release level 4 then level 3, and append `REV` through a fresh lawful level-3 then level-4 call while the stopped session still holds the operation lease. Never reacquire level 3 under level 4. X4c remains the unit that lands the end-path `REV`/`CLN`.

The witness claim is the honest S6 bound. S6 says no owner asserts cryptographic authentication of the interior prefix; `bodySha256` names the tail body digest; confirming a retained carrier establishes presence, contiguity, and non-rollback below the last observed operation boundary, class `confirmed-under-retained-custody`. An unmet anchor is reported unknown. The proposal claims torn restores, lost tails, hash substitution within the carrier, and a namespace rollback below that boundary, and it rejects interior-prefix authentication and extra witness members. v8's further sentence, that a rollback to a state above the last observed floor while no operation was running is seen when a later operation observes a lower tail, is the comparison item 4's start performs.

## Items 8 to 12

The busy row matches S12: `PROJECT.BUSY` is operational-failed, exit 4, `LEDGER.BUSY_TIMEOUT`, faultCause `ledger-busy`, detail `PROJECT.BUSY`. I/O, including durability-undetermined, matches `HOST.IO_FAILURE` / `host-io`. The budget row as 468's existing work-budget refusal is the right row. The binding-mismatch projection (`LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted, nothing appended or published) matches S12 and carrier-format.v3 §8.1. The public quarantine projection for `uncertainTailLoss`, `witnesslessRestore`, `witnessMalformed`, protocol violation, and floor regression matches S12's rule that a journal-carrier quarantine publishes no `domainDetail`. A new internal carrier-refusal family, with no new public code and exhaustive matches, is the same pattern X3a used.

Two item 8 sentences do not match those rows (RF-3). Recording a `carrier_quarantine` row is a marker the writer open is forbidden to store. Classifying any non-format-3 object as `MIGRATION.CORRUPT` borrows the detail S12 reserves for a format-3 migration footprint. A partial format-3 object set stays that detail. Continuation only on a new grant generation, owned by a later unit, is correctly unclaimed.

The budget is bounded. Start reads the tail, the witness, and the floor, charged before they run, inside the bracketed capture limits the law names. Each append reserves its post-effect confirmation before the first effect (467 item 6). A full-journal read at start is rejected.

Coverage matches the build plan's split. In scope: F06's journal half, F07, F08, F09, F10, and F19's journal half. Prepared elsewhere: F06's evidence half and F11 (X3c), F19's evidence abort (X3d), F38–F41 (X4 and X3d). F46–F51 stay out. EXIT-PLAN's row still says X3b covers F06–F11 and F19 and points at the lifecycle file. The proposal's narrower split is the one that matches the build-plan paragraphs.

The tests are acceptable while X2e is pending. A crate-private `cfg(test)` carrier-location fixture in `opensip-security`, built with `installation_read_fixture`, with no production seam and no cross-crate bridge, is the right stand-in. The real composition test lands with X2e. The fixture's "test projectKey" uses whatever preimage RF-2 names. That is not a separate finding.

The units are the right split. X3b-1 is creation, open, reconciliation, the floor, and the start and end steps, with the item 11 tests. X3b-2 is the append protocol, the witness file protocol, `JournalAppendLock`, and record building. X3b-3, with X2e, composes the carrier start into the handoff and the end step into the operation's end path.

## Cross-law

X3b already requires the ordering X2 r3 does not yet record. Item 1 runs the carrier start inside X2e's handoff, after the join and before the fence is released, and says X2 records that step when next revised. X2 r3 item 7a still ends by releasing the fence, with no carrier-start step. X3b should require the ordering, and it does. X2's next revision records it, because that law is already REQUIRED-FINDINGS. X3b-3 is the composition unit. A law may name a later unit's obligation while the other law is open. The header's "X2 (r2, in revision)" is a stale citation. The operative handoff, move then release the fence, is the same in r3.

## Required findings

### RF-1 — The floor write is held under the lease

S7 says trust state is written only under the fence and never under a lease. S1 records v8 §5.4's fence/lease handoff as refined by that sentence. Item 2 states the rule for `I/trust/carrier-floors/N.v1`. Item 3 then creates the floor while the fence and the operation's EXCLUSIVE or APPEND-WRITE lease are both held. Item 4's start copies the observed tail into the floor inside X2e's handoff, after that handoff has taken the lease. Item 4's end releases the lease, takes the fence, re-acquires the lease, and if acquired re-reads the tail and copies it into the floor before releasing both.

Failure scenario: the operation follows items 3 and 4. The high-water, which is trust state, is published while the lease is held. An implementer who follows item 2 and S7 cannot complete the stated end sequence, because the copy is specified only after the lease is re-acquired. Holding the fence at the same time does not satisfy "never under a lease".

The lease may be probed under the fence to learn whether another writer holds it. It is released before the floor write. The fence stays held across that write, so no other acquirer can enter. If another writer holds the lease, the copy is skipped and the fence is released, which is v8's skip rule. The no-second-gate retake itself stays as item 4 states it.

### RF-2 — The carrier digest has no registry preimage

Registry owner v2 selects no historical opaque projectKey. A v2 entry is `projectId`, `namespaceId`, `root`, `status`, and `allocationKind`. Item 2 says `projectKeyDigest` is SHA-256 of the registry row's projectKey as that owner defines it, taken from `ProjectOperation`'s row snapshot, and the `carrier_format` row stores that digest. The product open still compares `carrier_format.project_key_digest` with SHA-256 of a `project_key` string. Host-foundation's digest is SHA-256 of projectKey UTF-8 bytes, and that is the layout owner §1b does not adopt. N as the floor's path component is the part of item 2 that already matches the registry owner.

Failure scenario: the handoff moves a lawful v2 row. The row has a `projectId` and no `projectKey`. The instruction is unsatisfiable. An implementer invents a key the registry does not have, or hashes some other field and still calls it the registry owner's projectKey. The admitted binding can be joined while the carrier digest is taken from that invented key, or every fresh open refuses because no lawful preimage was named.

The law names the exact bytes that are hashed. It does not point at X2's registry owner for a field that owner removed. This review does not choose those bytes.

### RF-3 — The writer stores a quarantine marker and classifies a non-format-3 file as a migration footprint

S12 and carrier-format.v3 §8.1 say a writer or maintenance refusal appends nothing, publishes nothing, and writes no quarantine marker. `carrier_quarantine.reason` keeps its inherited enum. Every open re-detects from the bytes it reads. Item 8 records a quarantine by the existing `carrier_quarantine` row and `failClosedNoAppend`. X3b is the writer open. Read-only recovery, which is the phase that reports a quarantine from stable observations, is X6 and is unclaimed.

The same item says any non-format-3 object, or a partial object set, is `MIGRATION.CORRUPT` on `LEDGER.CORRUPT`. S12 and carrier-format.v3 row 369 limit that detail, at a writer open, to a carrierFormat 3 migration footprint that is not a lawful durable prefix (partial object set, invalid definitions, `grant_journal_v3` rows before format publication) or a violated generation boundary (F51). S12 says `MIGRATION.CORRUPT` is not borrowed for ordinary journal corruption. Read-only format 1 or 2 is F46: operational-failed, exit 4, `HOST.IO_FAILURE`, faultCause `host-io`, `domainDetail` omitted.

Failure scenario: the writer inserts a `carrier_quarantine` row. The next open trusts that row instead of re-reading the bytes. Separately, a complete format-1 database planted under the namespace is reported as the migration-footprint detail, the code S12 reserves for a resumable-prefix failure, and the F46 class is skipped.

A partial format-3 object set stays `MIGRATION.CORRUPT`. The public projection item 8 already states for `uncertainTailLoss`, `witnesslessRestore`, `witnessMalformed`, protocol violation, floor regression, and the binding mismatch stays: `LEDGER.CORRUPT`, `ledger-corrupt`, `domainDetail` omitted.

### RF-4 — A witness without a floor is neither INIT nor a comparison

Item 3 writes the `COMMITTED 0` witness and then the floor. The creation predicate requires the carrier absent, the witness absent, and the floor positively absent. Item 4's start compares the tail with the floor and quarantines a lower tail or an equal sequence with a different body hash.

Failure scenario: the process crashes after the witness rename is durable and before the floor rename. The next start sees a complete carrier, a valid `COMMITTED 0` witness, and no floor. Creation does not resume, because the carrier is present. The comparison assumes a floor. Treating absence as "no high-water, copy the current tail" hides a floor that was published and later deleted: a namespace rollback would then be adopted as the new high-water. Quarantining the window makes this legitimate crash unrecoverable. The law distinguishes finish-INIT, where the carrier and the witness agree and the floor is positively absent with no prior floor identity, from a floor that was published and is now gone.
