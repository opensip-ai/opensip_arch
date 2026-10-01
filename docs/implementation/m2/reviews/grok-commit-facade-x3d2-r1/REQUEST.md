Grok review r1: X3d-2, the storage side of the `CommitSession` facade (law X3d r6 items 1, 3, 4, 6, 8 and 9, and item 13's X3d-2 list), with X9 r1's `x3d.publish.published` point, X8 r3 item 3's owner rows for this unit and item 3b's adapter source pin, and inventory v122 (parent v119). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-commit-facade-x3d2-r1. If you build or test, use a CARGO_TARGET_DIR under that directory, and run every test with a private TMPDIR: create a 0700 directory under `$(getconf DARWIN_USER_TEMP_DIR)` (for example `…/grok-x3d2-tmp`), never the shared `/private/tmp/claude-501` tree, which other runs churn. Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read or print the private 413 UUID fixture. Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH`; Python is `python3.14`.

## The unit

X3d r6 item 13 defines X3d-2 (storage) as `crates/storage/src/commit.rs` with:
- `prepare_commit` (items 3 and 8);
- `PreparedCommit::publish`;
- the private adapter implementation;
- `PublishedCommit`;
- the `storage → evaluator` edge;
- the X8 rows (X8 r3 item 2 replaces "the X8 doctests" with fixtures).

r6 adds: step 0 calls the session's end-path step, `CarrierCapacityExhausted` is returned after a completed scope, and storage holds no settlement reserve.

X8 r3's owner rows for X3d-2 are rows A to D and G for `PreparedCommit` and `PublishedCommit`, group H (the facade takes no adapter or `SealOutcome`, E0061), and item 3b's adapter source pin. X9 r1 item 5 gives X3d-2 the `x3d.publish.published` point.

Its dependencies are integrated:
- X3c-2 (`ledger_store/project_commit.rs`: objects, `PreparedLedger`, staging, the prepared-commit adapter);
- X3d-1 (`custody/commit_session.rs`: `charge`, `refused()`, `undetermined()`, the binding getters, `CarrierCapacityExhausted`, `SealOutcome`, `SessionRefusal::termination()`; review call 13);
- X3d-0 (`work_ledger`);
- X8a's driver (`crates/host/tests/admission_tests.rs`).

Library only: no command commits, and nothing here enables real-machine use.

## Law

All under arch `docs/implementation/m2/`, accepted:
- `commit-session-x3d/PROPOSAL.md` r6, the law of this unit, including "Units after the law";
- `ledger-blob-x3c/PROPOSAL.md` r7 (items 1 to 10 and 12a);
- `refusal-suite-x8/PROPOSAL.md` r3, items 2, 3 (groups A to H for this unit), 3a, 3b and 4g;
- `crash-matrix-x9/PROPOSAL.md` r1, item 5 (`x3d.publish`);
- `reviews/grok-commit-session-x3d1-r1/REVIEW.md`, the X3d-1 acceptance and its call 13;
- `description-batch-d1/README.md`, contract successor D1 (39 description overrides on v119, bound at product 7be09a7), whose "After selection" section says how the next inventory successor projects them.

Design sources for values no M2 law fixes (judgment calls 5 to 8): `docs/v2/contracts/product-v1/identity-and-evidence.md` (the retention table near line 462, commit order near line 1666, sealed assurance near line 1718), `docs/v2/architecture/store-instance-lineage.v1.json` (`storeGenerationDigest`), `docs/v2/architecture/implementation-boundaries-and-build-plan.md` lines 25 to 190 and 386 to 405 (the counter accessor).

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x3d2`, detached at `7be09a7` (main). After X3d-1, X4B-b landed at 8240856 with no inventory change, and 7be09a7 binds D1 on v119 (a lock entry only). The lock selects v119, with D1 bound. Save `git -C <worktree> diff` as product.diff and report its sha256. The twenty-two new files are intent-to-add. Lead's value: `3afc55c34cca13b1b296325e07aa898ebb6b8f4955b548961746a859f7035002`, 117719 bytes; 35 files, 2573 insertions(+), 16 deletions(-).
- **Arch:** these files, all untracked:
  - `repository-file-inventory.v122.json` (parent v119);
  - `commit-facade-x3d2-inventory-v122-subject.json`;
  - `commit-facade-x3d2-inventory-v122/`.

## What was built

**`crates/storage/src/commit.rs`** (macOS), exported from `opensip-storage`'s root: `prepare_commit`, `PreparedCommit`, `PublishedCommit`, `CommitOutcome` and `NotPrepared`. `opensip-storage` now depends on `opensip-evaluator` (Cargo.toml and Cargo.lock).

**`prepare_commit(ReplayedRun, CommitSession) -> Result<PreparedCommit, (NotPrepared, StoppedSession)>`** (item 3). In this order:
0. `session.reserve_end_path()`, security's step. A refusal is `NotPrepared::Refused(row)` with its `StoppedSession`, which holds no reserve.
1. One charge on the attempt ledger (cost: the retained evidence's bytes) that binds and plans:
   - the replay's Run must name the session's ProjectId, its target identity (`CommitSession::project_id`, call 3);
   - its evaluator closure must equal `core_closure()`;
   - every retained frame must be its identity's H preimage;
   - it builds the canonical commit inventory `{schemaVersion 2, runId, objects, blobDigests}`, the manifest (the Run descriptor's canonical bytes), the `storeGenerationDigest`, and the declared objects (every frame under its H digest, every blob under its raw digest, each once).

   A mismatch is the invariant row through `session.refused()`.
3. `session.capacity()` (`seal_fits`, no literal): `NotPrepared::CarrierCapacityExhausted` with the session's `StoppedSession`. Nothing was latched; the step-1 scope had completed.
4. Then, as security's own charge, `session.store_root()` (call 2) opens `I/stores/S`, and X3c-1's production `ProjectStoreLocation::selected` is built from it. One charge then creates or admits `projects/N`, `objects/sha256` and the ledger (X3c-1's `admit_*` and `create_or_open_ledger`).
5. One charge does `effect(0, reserve)` and `prepaid(reserve)` (step 2, call 4). The reserve is exactly what attempt admission and the objects charge (`attempt_and_objects_cost`). Inside it:
   - `admit_attempt` with the session's `admitted` row: a no-replace refusal is `NotPrepared::ExistingAttempt { executionId }` through `refused()` (step 5); an undetermined `COMMIT` is `NotPrepared::CommitUndetermined` through `undetermined()`, which forfeits the reserve;
   - then `publish_objects`, all frames and blobs with their barriers (step 6).
6. Any other failure is its X3c item 10 row through `refused()`.

**`PreparedCommit::publish(self) -> (CommitOutcome, StoppedSession)`** (item 4):
1. `begin_journal_txn(session)`: a refusal is `Refused(termination())`.
2. `txn.charge(begin_prepared_ledger(...))`: the evidence ledger's non-waiting level 3. On failure, `txn.abort()` (F06), with the ledger's row.
3. `seal_under_append_lock(txn, &run, Stager { … })`. Storage's private adapter stages after the durable `SEAL` (call 6):
   - the SEAL binding's RunId, carrier digest and operationRef must equal the commit's (otherwise the invariant row);
   - the receipt counter is allocated in the open transaction (`PreparedLedger::next_commit_sequence`);
   - the exact receipt and the thirteen-field association are built and parsed by their own parsers;
   - X3c-2's `stage` writes the pair, the Run material, the initial availability and the empty pin set, all or none.

   `StagedCommit::commit` performs only X3c-2's `COMMIT` and maps it to `EvidenceCommit`.
4. `SealOutcome::Committed` builds `PublishedCommit`, then `x3d.publish.published`, then `CommitOutcome::Committed`. `CommitUndetermined` passes through. `Refused(Session(r))` is `r.termination()`, and `Refused(Staging(r))` is the ledger row.

**`PublishedCommit`** holds the exact receipt bytes, RunId, ExecutionId, commit sequence, the SEAL's (generation, seq) and `latchedAfterAdmission`, behind read-only getters. Its one construction is in `publish`'s `Committed` arm. Neither it nor `PreparedCommit` is Clone, Default or serializable, and neither has a non-public inherent function.

**Security (calls 2 and 3), two read-only hooks:**
- `CommitSession::project_id()` returns N's ACTIVE row's ProjectId.
- `CommitSession::store_root() -> Result<StoreRoot, WorkFailure<SessionRefusal>>` is one charge on the attempt ledger, through the free function `operation_handoff::open_store_root`, so `ProjectOperation` gains no inherent function and owes no census row. It:
  - opens `stores`, then S, no-follow from the retained I, each present, private, exactly named and on I's device;
  - requires `S/store-instance.v1` to have the device and inode of the endpoint's retained marker sample;
  - requires the absolute spelling from H as walked to name the same directory.

  Missing or changed is the custody row `required-files-changed`; other directory refusals keep X2's registration rows; I/O is host-io. `StoreRoot` (exported) lends the directory, its spelling and the uid.

**Existing storage modules:**
- `ledger_store.rs`: `WriteTransaction::next_commit_sequence`, the one counter accessor (call 6). It also re-exports the X3c owners to `crate::commit`.
- `recovery.rs`: `DecimalCounter::parse_text`.
- `project_ledger.rs`: `ProjectStoreLocation::selected`, and the re-exports.
- `project_commit.rs`: `attempt_and_objects_cost`, `PreparedLedger::next_commit_sequence`, `h_digest`, and the staging join widened to typed objects (call 5).
- `recovery_material.rs`: `stage_run_material` returns objects and blobs.

**Inventory v122** adds 21 rows to v119 (918 files): `commit_tests.rs`, `schema_sources.rs` and the 19 cases. `crates/storage/src/commit.rs` is already a planned row of v119, and its description stays true, so it is kept by value. Every inherited row is equal by value to v119's bytes. The projection grows from 16 rows to 55, as D1's README requires: the 16 bound to v119, plus D1's 39 overrides on v119. Its README lists the existing rows this unit makes out of date, judged against D1's effective text: admission_tests.rs, project_ledger.rs, project_commit.rs and recovery_material.rs.

**`crates/storage/src/schema_sources.rs`** (call 9): storage's embedded copy of the 48 pinned schema sources, compiled once per process and resolved at step 1, before any lock.

**X8 (`crates/host/tests`):** nineteen cases under `refusal/cases/storage_*.rs`, with nineteen census rows (unit X3d-2):
- **A** (E0308): `JsonValue`, and the generated `Identity3Run`, at `prepare_commit`;
- **B:** `prepare_commit(true, session)` (E0308), and `PublishedCommit { verified: true }` (E0560 "has no field named `verified`");
- **C** (E0308): `&RetainedInputs`;
- **D, E and G** for `PreparedCommit` and `PublishedCommit`: literal (no code), `Default`, `Deserialize`, `Clone` and `Serialize` (E0277);
- **E reuse** (E0382): `prepare_commit` with a consumed session, and `publish` twice;
- **H** (E0061): `prepared.publish(adapter)` ("this method takes 0 arguments but 1 argument was supplied"), and `prepare_commit(run, session, outcome)` ("this function takes 2 arguments but 3 arguments were supplied").

Item 3b's source pin, `the_commit_adapter_and_session_functions_are_confined_to_storage_commit`, has a self-check, `the_adapter_pin_refuses_a_use_outside_its_files` (call 12). The driver passes with 95 cases and 8 self-tests.

## Judgment calls: please rule

1. **Built before X8b and X9-1.** X8 r3 says X8b "lands before X3d-2, whose storage tests use it" (item 4g). X9 r1 says X9-1 "precedes X3d-2's … composition tests". Neither has landed (X9-1 is in flight, and X8b depends on it). The lead assigned X3d-2 now.
   - **What is tested now.** Storage's tests run every storage function that `prepare_commit` and `publish` compose, without a session, on a real scratch `I/stores/S` with a real replay. X3d-1's tests already cover the session half with a stand-in adapter.
   - **What is not tested yet.** The glue that calls both halves in one process (`prepare_commit` and `publish` with a real `CommitSession`) is first exercised by X8c's B0 to B4 and X9-2.
   - **Rejected:**
     - a storage-side seam that supplies a `ProjectOperation`, which is the forbidden production seam;
     - building X8b here, which would duplicate X9-1's shared site list;
     - stopping until X8b lands.
   - **Ruling asked.** Is X3d-2 acceptable now with the composition test owed to X8c, which already depends on X3d-2? The lead recommends yes, recorded in X3d r7, X8's scheduled record-only revision.
2. **`StoreRoot`, a security hook.** X3c-1 says "No production constructor of a location exists yet: X3d supplies it from X2e's ProjectOperation and X3a's endpoint". The operation retains I's chain, but no `I/stores/S` handle, and X3d-1's call 13 surface has none. So `store_root` opens it read-only and binds it to the endpoint's admitted marker by identity.
   - **Rejected:** storage walking I itself (storage holds no I, and that custody is security's); a bare path; a new inherent function on `ProjectOperation`.
   - `StoreRoot` is exported but is not a row D type: it grants nothing, and nothing accepts it in place of a session. So it gets no X8 rows.
3. **Target identity.** Item 3 step 1 ("RunId, plan and proof bind to the session") and X5 r2 ("target identity, inventory, producer closure") need a session value for the Run to bind to. That value is the ACTIVE row's ProjectId, which the Run descriptor's `projectId` must equal. The closure must also equal the selected core closure.
   - **Finding for X8c.** B0 commits "a corpus Run from `crates/evaluator/tests/fixtures`". That directory holds no Run today, and a scenario project's ProjectId is a fresh CSPRNG draw (X2 r8 item 6, allocation), so a pre-built corpus Run cannot bind to it. X8c needs a Run whose `projectId` is its scenario project's, for example through X5a's producer.
   - **Rejected:** binding only the closure. Another Run of the same closure would then pass B1.
4. **Step 2's reserve is taken after step 3, immediately before the attempt row.** The platform's only reservation that outlives a call is the settlement reserve (X3d r6's "second gap"); `effect` and `prepaid` live inside one charge. Step 3 consumes the session, so no charge can span steps 2 to 6.
   - **What is reserved.** The reserve is taken in the same charge as steps 4 to 6, after `capacity` and after the layout, which X3c-1 charges as it runs. It is exactly `OPEN_COST + ATTEMPT_COST + publication_cost(declared)`, and attempt admission and the objects draw only from it: nothing is charged twice, and a shortfall is refused before the attempt row.
   - **What is reserved elsewhere.** `publish`'s storage steps are reserved inside their own charges by X3c-2 before their first effect: `BEGIN`, and staging's `STAGE_COST + COMMIT_COST` plus the bodies. The SEAL path is X3d-1's charge.
   - **The only observable change.** When both capacity and budget fail, capacity is reported. No write precedes either.
   - **Rejected:** charging the total at step 2 and again as each step runs. That double-counts, and it still would not guarantee the later charges unless the remaining budget were at least twice the total.
5. **Typed objects are published as their H frames.** identity-and-evidence's retention table says one CAS keyed by raw SHA-256 holds "raw artifacts, canonical records and H identities", with the object under an h-identity digest being "the exact H preimage frame". The commit inventory is "the exact set of typed object identities and retained raw blob digests the commit published", and replayable assurance retains the closure.
   - X3c-2's staging join compared the published set with `blobDigests` alone. It now compares it with `blobDigests` plus the H digests of `objects`, and `stage_run_material` returns both. A blob equal to a frame is one object.
   - **Rejected:** publishing blobs only, which would leave a "replayable" Run's typed objects unretained.
6. **The receipt's values.**
   - `sealedAssurance` is `replayable` (the default authoritative profile).
   - `signerKeyId` is `local-custody-unsigned`. M2 has no receipt signing key, and "authenticated receipt signing" is left to implementation qualification. A real signer is a successor's.
   - `commitSequence` is per (storeGenerationDigest, N) and starts at 1, as in the reference model (`len(receipts)+1`). It is allocated inside the open evidence `BEGIN IMMEDIATE` by the one accessor: `ORDER BY length DESC, text DESC`, an exact u64 decode, plus one. A full u64 is refused on the invariant row. The association copies it as canonical decimal text.
   - **Rejected:** a lexical or `CAST` MAX, and allocation outside the evidence transaction.
7. **`storeGenerationDigest`** is raw SHA-256 over the canonical five-member `{schemaVersion 1, namespaceId, storeInstanceId, storeGeneration, stateSchema}`, with no domain framing (store-instance-lineage v1). A test pins the canonical string.
8. **Availability and pins.**
   - The initial availability is generation 0, `retained`, no missing refs, `observed`.
   - The pin set is empty, because no law names a pin a fresh commit must hold. The pin read bounds are 0. `per_record_work` is 4 MiB.
   - **Disclosed limit.** X3c-2 stages the initial availability unconditionally, so a second commit of a Run already committed in the same (S, N) is refused at staging on the invariant row. identity-and-evidence says "Duplicate retry can share a Run but has a separate attempt receipt". The fix is an X3c successor's (stage availability only when none exists). M2 never commits one Run twice.
9. **Storage's own schema sources.** `prepare_commit` takes no registry (group H fixes arity 2), and storage cannot reach host's `embedded_schema_registry`. So storage embeds the same 48 files in `source_requirements` order. A test compares them byte for byte, and `from_sources` refuses anything else by its pins.
10. **Outcomes.**
    - `CommitOutcome` is publish's: `Committed`, `CommitUndetermined` and `Refused`.
    - `NotPrepared` is prepare's: `CarrierCapacityExhausted`, `ExistingAttempt`, `CommitUndetermined` and `Refused`.
    - `ExistingAttempt` is its own variant. Its `StoppedSession` comes from `refused()`, so the gate latches and `finish` appends the `REV`. X7 maps it to the invariant row until X6 exists.
11. **Staging rows.** A SEAL binding that does not join, a receipt or association its own parser refuses, and a missing registry are all the invariant row (`StagingMismatch`).
12. **The adapter pin.**
    - **Names.** `CommitAdapter`, `StagedCommit`, `begin_journal_txn` and `seal_under_append_lock`: both traits of the pair, not one.
    - **Allowed files.** Security's `custody/commit_session.rs` and its root re-export `lib.rs`, plus storage's `commit.rs`.
    - **Production.** Every `.rs` under `crates/*/src` except files named `*_tests.rs` or `tests.rs`. Comments are not uses.
    - **Category.** Group H rows use the existing category `ForgedReceipt` (a caller-made `SealOutcome` or adapter forges the seal's result), so the census enum is unchanged.
13. **`x3d.publish.published`** is placed once, in the `Committed` arm, after `PublishedCommit` is built and after `seal_under_append_lock` has released level 4.

## Tests

New: 11 in storage (plus 1 schema-source test), 1 in security, 19 compile-fail cases and 2 host source-pin tests.
- **`crates/storage/src/commit_tests.rs`, 11 tests** (the corpus Run of `crates/security/tests/fixtures/journal-seal-cases.json`, replayed by `opensip_evaluator::replay_run`, on a scratch private `I/stores/S`):
  - the plan declares exactly the retained frames and blobs, and the inventory lists them;
  - another project or another closure does not bind;
  - the `storeGenerationDigest` recipe;
  - a prepared commit stages every row, visible to no other connection until its one `COMMIT`, after which the pair joins the admitted attempt with settlement pending;
  - the counter: 1 first, then 2/9/10/100 give 101, and a full u64 is the invariant row;
  - a non-joining SEAL binding (RunId, carrier digest, operationRef) stages nothing;
  - an evidence `COMMIT` error is `Undetermined` with the attempt still admitted;
  - the reserve equals the exact charge, and one byte short is the budget row before the attempt row and any object;
  - a reused ExecutionId is refused before any object;
  - every ledger row maps to its existing termination;
  - the `published` point is placed once, after the one construction.
- **`crates/storage/src/schema_sources.rs`, 1 test:** the embedded sources are the pinned registry.
- **`commit_session_tests.rs`, 1 test, through the real handoff:** `project_id` is the ACTIVE row's; `store_root` is the endpoint's `I/stores/S` by identity and spelling; a replaced S holding a copied marker is `required-files-changed` and closes the attempt ledger.
- **Host:** the driver with 95 cases (19 new); the adapter pin and its self-check.

## Checks

Product checks are at 7be09a7 plus this diff. Arch verifiers run against the real lock at 7be09a7, which selects v119 with D1 bound.
- **Workspace runs:** two full runs of `cargo test --locked --offline --workspace --all-targets` on the final bytes, each with a private 0700 TMPDIR: each with 1575 passed, 0 failed and 3 ignored, across 17 test binaries.
- **Lints:** `cargo clippy --offline --workspace --all-targets -- -D warnings` is clean. It is also clean with `-p opensip-storage -p opensip-security --all-targets --features opensip-platform/crash-matrix`.
- **Formatting:** `cargo fmt --all -- --check` is clean, and so is `rustfmt --edition 2024 --check` on the two `include!`d test files.
- **`check_package_edges --lane host`:** passes against v119 and against v122, with 20 declared and 20 resolved edges, including `opensip-storage` → `opensip-evaluator` (already declared since inventory89).
- **verify_scratch** (v122 appended in memory to the worktree's lock at 7be09a7, with the inheritance replaced by the record's 55 rows): passes, with 82 inventory successors, 73 contract successors and 55 inheritance rows; v122 is selected.
- **verify_projection against the real lock:** 55 rows; 278 corruptions refused.
- **`build_v122.py`:** reruns produce the same bytes. 918 files; the 897 v119 rows are equal by value; 55 projection rows. It refuses unless D1 is bound and each D1 before text equals its v119 row.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does X3d-2 meet X3d r6 items 1, 3, 4, 6, 8 and 9, and item 13's X3d-2 list? In particular:
  - step 0 first;
  - the binding;
  - `CarrierCapacityExhausted` after a completed scope, with the ledger open;
  - attempt admission's three outcomes;
  - level 3 then level 3 then security's SEAL path;
  - staging only after the durable SEAL;
  - the `COMMIT` only through the permit;
  - `PublishedCommit` only after a successful `COMMIT`;
  - no reserve held by storage;
  - no external adapter or `SealOutcome` accepted.
- Is `x3d.publish.published` right in name and place?
- Rule on calls 1 to 13. Call 1, the ordering against X8b and X9-1, needs an explicit ruling.
- Do the nineteen cases and the source pin meet X8 r3 for X3d-2?
- Is v122 right on v119, including the 55-row projection with D1?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `commit-facade-x3d2-inventory-v122-subject.json` (lead's value `207ece22b1ac09b34dacfdc6e84c7dce3173ea5f461f38dbf0338bdd8245af7c`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v122, parent (the v119 pin), successorRecord (the pin of `commit-facade-x3d2-inventory-v122/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
