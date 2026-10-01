Grok review r1: X3d-1, the security side of the `CommitSession` facade (law X3d r6 items 1 to 4, 7, 8 and 9, and item 13's X3d-1 list, with X4c's end path), with X9 r1's `x3d.*` crash points, X8 r3 item 3's owner rows for this unit, and inventory v119 (parent v113). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-commit-session-x3d1-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read or print the private 413 UUID fixture.

## The unit

X3d r6 item 13 defines X3d-1 (security) as:
- `CommitSession::open`;
- `begin_journal_txn` and its consuming abort;
- `JournalSealBinding`;
- `seal_under_append_lock` with the adapter trait;
- `StoppedSession::finish`, including X4c's `REV` and `CLN` and the real-lock swap.

r6 adds:
- the session's private end-path step, which takes the settlement reserve at item 3 step 0, and the end-path wrapper type;
- the end-path body bounds and the exact reserve cost, built from X3b-2's cost functions with no literal;
- the forfeit at each uncertain classification;
- `finish`'s single `settle`, for the `REV` and then the `CLN`;
- the end step skipped on a closed attempt ledger;
- the source pin on `reserve_settlement` and `settle`.

Its tests are listed in item 13.

Its dependencies are integrated:
- X3b-1b, X3b-2 and X3b-4 (`journal_store/carrier_*`);
- X3d-0 (`work_ledger.rs`: `reserve_settlement`, `settle`);
- X2e (`custody/operation_handoff.rs`: `ProjectOperation`, `journal`, `end`, `JournalOutcome`);
- X4a (the guard, the checkpoint over a `JournalAppendHeld` borrow, `FinalGate`, `AdmissionPermit`);
- X9-0 (the crash macros);
- X8a (the compile-fail driver);
- X4B-a.

The unit was written at a34dc6b and rebased onto 0fc8ea2 (X4B-a) before any review.

X3d-2 (storage `commit.rs`: `prepare_commit`, `publish`, the private adapter implementation, `PublishedCommit`) is the next unit and is not built here. This unit exposes what X3d-2 needs.

Library only: no command commits, and nothing here enables real-machine use.

## Law

All under arch `docs/implementation/m2/`, accepted:
- `commit-session-x3d/PROPOSAL.md` r6, the law of this unit, including "Units after the law";
- `journal-x3b/PROPOSAL.md` r10 (items 4, 5, 5a, 6, 8 and 9: the append, the stop order, the uncertain-outcome rule, the end step, the reserve);
- `reviews/grok-journal-x3b-r9-commit-session-x3d-r5/REVIEW.md` and `reviews/grok-journal-x3b-r10-commit-session-x3d-r6/REVIEW.md`, the combined reviews that accepted X3d r5 and r6;
- `live-guards-x4/PROPOSAL.md` r7 (items 3, 4, 6, 7 and 8);
- `refusal-suite-x8/PROPOSAL.md` r3, item 3: groups D, E, F and G for this unit's types, the `open` arity case, item 3a's census and item 3d's `execution_id()`;
- `crash-matrix-x9/PROPOSAL.md` r1, item 5: the `x3d.session`, `x3d.publish` and `x3d.finish` scopes, placed by the unit that builds them.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x3d1`, detached at `0fc8ea2` (main). The lock selects v113. Save `git -C <worktree> diff` as product.diff and report its sha256. The fifty-two new files are intent-to-add. Lead's value: `1a2fe9dcf5f5d8e0b9d483ef1856ac841772588591530417092a7e99f9b6e363`, 177914 bytes; 69 files, 3603 insertions(+), 113 deletions(-).
- **Arch:** these files, all untracked:
  - `repository-file-inventory.v119.json` (parent v113);
  - `commit-session-x3d1-inventory-v119-subject.json`;
  - `commit-session-x3d1-inventory-v119/`.

## What was built

All of the session is in `crates/security/src/custody/commit_session.rs`, a new custody module beside X2e's `operation_handoff` and X4a's `operation_guard`. It is exported from `opensip-security`'s root, macOS only.

**Types (item 1).** These are exported:
- `CommitSession`, `JournalWriteTxn`, `JournalSealBinding` and `StoppedSession`;
- the adapter traits `CommitAdapter` (stage) and `StagedCommit` (commit), and `EvidenceCommit<C>`;
- `SealOutcome<C, R>` and `SealRefusal<R>`;
- `SessionRefusal`, `CarrierCapacityExhausted` and `SessionEnd`;
- `begin_journal_txn` and `seal_under_append_lock`.

`ProjectOperation` becomes `pub`, because the public `open` takes it. Every type has private fields and is not Clone, Default or serializable. The only constructors are the facade's own. Every inherent function of the four session types is public, so item 3a's census has nothing to add for them.

**`CommitSession::open(operation)` (item 2).** It consumes the operation. On the attempt ledger it draws the ExecutionId (`exec1_` and 32 hex) and the operationRef (`op-` and 32 hex), each from 16 host-CSPRNG bytes. The ExecutionId draw is the `x3d.session.execution-draw` draw point. An injected id is held to the `exec1_` grammar.

It binds N, (S, G, K), the carrier digest `SHA-256(N)` and the receipt's selected core closure. Read-only getters expose them, with `execution_id()` (X8 3d) and `operation_ref()`.

On refusal it latches the gate and returns a `StoppedSession` holding no reserve. A failed draw is the host I/O row; an N that does not join is the invariant row.

**`reserve_end_path` (item 3 step 0; item 8).** It takes the attempt ledger's one `SettlementReserve` through a chain of wrappers: the attempt, then the write receipt, then the operation, then the session. Each wrapper has one production caller, and both directions are source-pinned. The reserve sits in a private, non-Clone `EndPath` that only the session and then its `StoppedSession` hold.

Its size is exact: for each of `REV` and `CLN`, X3b-2's own cost functions at the kind's bounded maximum, with no literal. Those functions are:
- `carrier_creation_cost`, for begin's writer open and `BEGIN IMMEDIATE`;
- `operational_read_cost`, for the witness read;
- `append_cost`, at the body length and the longer (`COMMITTED`) witness.

Both the body and the witness are measured at the widest decimal widths: grant generation `i64::MAX` and sequence `9007199254740990`. `acquire` charges nothing.

A refusal is the budget row, it latches the ledger, and the session stops holding no reserve. A second call is the invariant row. On success it reaches `x3d.session.settlement-reserved`.

**`capacity` (item 3 step 3).** It applies `seal_fits` to the tail the lock proves (`JournalAppendLock::proven_tail`, falling back to the start tail), with no literal threshold. An exhausted generation returns `CarrierCapacityExhausted { grantGeneration, provenTailSeq }` with a `StoppedSession` carrying `JournalOutcome::Exhausted`. The gate is not latched and the ledger stays open.

**X3d-2's hooks.**
- `charge`, on the session and on the transaction: one charged step on the attempt ledger. It lends only a `WorkScope`, never the ledger or the reserve.
- `refused()`, for a certain refusal: it latches the gate and keeps the reserve.
- `undetermined()`, for item 3 step 4's undetermined attempt admission: it forfeits the reserve.

**`begin_journal_txn` (item 4 step 1).** It takes the journal's non-waiting `BEGIN IMMEDIATE` on the attempt ledger. Busy, I/O or quarantine is the carrier row. A session without the reserve is the invariant row, so no SEAL path starts unfunded.

`JournalWriteTxn` holds the session and a `DetachedJournal`: the open level-3 connection and its tail, kept apart from the borrow of the lock and location (judgment call 2). `JournalWriteTxn::charge` is for storage's evidence-ledger `BEGIN IMMEDIATE`. `abort` is the consuming abort (F06): the journal's level 3 rolls back, the gate latches and the reserve is kept.

**`seal_under_append_lock(txn, &replayed, adapter)` (item 4 step 3).** All of it runs in one `ProjectOperation::journal` charge, with X4a's `Checkpoint` lent:
1. `attach` the detached level 3 to the operation's own lock (another carrier is refused), then `acquire` level 4;
2. `Checkpoint::effect`, admitting nothing yet;
3. `JournalAppendHeld::seal_record` builds and validates the `SEAL` with no effect, and `PreparedJournalSeal::bind` binds it to `&replayed`. `PreparedJournalSeal` is now crate-visible and borrows the replay;
4. to 6. `append_seal`: the `PENDING` witness, the insert and commit, and the `COMMITTED` witness. The appended body digest and RunId must equal the bound ones; otherwise the invariant row;
7. `Checkpoint::effect` again (F19);
8. `adapter.stage(&binding, work)`, in storage's open evidence transaction, then `x3d.publish.after-staging` and `before-final-checkpoint`;
9. `Checkpoint::admit(&held, staged, work)`, ending in `FinalGate::admit` and the one `AdmissionPermit`;
10. `permit.consume(StagedCommit::commit)`, then `x3d.publish.commit-returned`;
11. level 4 is released.

Stops:
- **A certain stop after step 1** drops the adapter, or the staged commit (the ledger rollback), then the held lock: level 4, then the journal's level 3 if still open. It happens exactly once, appends nothing and latches the gate. The `StoppedSession` records whether the `SEAL` was durable.
- **An uncertain `SEAL` commit or barrier** (`AppendError::Undetermined`, which latches X3b's lock), and **an undetermined evidence `COMMIT`**, return `CommitUndetermined { executionId }`. They forfeit the reserve there, where they are classified. The `StoppedSession` is `Uncertain`.
- **On success:** `Committed { committed, binding, latched_after_admission }`, where the flag is the gate state `1 → 3`.

**`StoppedSession::finish` (item 7, X4c).**
1. A `REV` is owed if any of these holds:
   - a durable `SEAL` has no evidence commit;
   - the gate is latched (state 2 or 3);
   - a revocation is the recorded stop.

   A `CLN` is owed for the `SEAL`-without-commit case.

   Owed records are appended in one `settle` of the reserve, the `REV` first, between `x3d.finish.settle.before` and `.after`. `ProjectOperation::settle_end_path` lends the location and carrier with no checkpoint (X4 item 3). Each record is a fresh `begin`, `acquire` and `append`. Each draft is first held to its kind's body bound, and a draft over the bound is the invariant row before any effect. The first failure ends the settlement: there is no `CLN` after a failed `REV`, and no retry. Its row is disclosed as `settlement_failure`; an undetermined end-path append is `DURABILITY.COMMIT_FAILED` and marks the outcome uncertain.

   Nothing owed: the reserve is dropped unspent (`forfeit`). No reserve: nothing is appended.
2. The lease is released (`x3d.finish.lease-release`, placed in `end_with`).
3. X2e's end step runs (`end-step.before` and `.after`), except after an uncertain outcome or on a closed attempt ledger, where `ProjectOperation::end` already returns `NotEntered`. After `Exhausted` it runs X3b-4's rollover.

`SessionEnd` reports `revocation_appended`, `cleanup_appended`, `settlement_failure` and `end_step_entered`.

**The real-lock swap.** X4a already built the checkpoint over the real `JournalAppendHeld`. No abstract test lock exists anywhere in the workspace (grepped), so no production or test path names one.

**Rows (item 9).** `SessionRefusal::termination()` maps every composition row exhaustively: X4's rows, X2's project rows, X3b's carrier rows and the budget row. `InstallationTermination` gains six variants on existing details, each with its S12 class, and the host projects them:
- `LedgerCorrupt` (`LEDGER.CORRUPT`, `ledger-corrupt`, no detail);
- `MigrationCorrupt` (the same with `MIGRATION.CORRUPT`);
- `CommitUndetermined` (`DURABILITY.COMMIT_FAILED`, `durability-commit`);
- `ProjectRootCustody { subject }` and `ProjectExplicitPath` (request-rejected, `CONFIG.INVALID`);
- `ProjectScopeLimit { subject }` (`REQUEST.UNSATISFIABLE`).

See judgment call 9.

**X8 r3 item 3 (crates/host/tests).** There are fifty cases under `refusal/cases/`, with fifty census rows (unit X3d-1).
- **Per exported type** (`CommitSession`, `JournalWriteTxn`, `JournalSealBinding`, `StoppedSession` and `ProjectOperation`):
  - group D: a literal (no code, "cannot construct `T` with struct literal syntax due to private fields"), `Default` (E0277) and `Deserialize` (E0277);
  - group E: `Clone` (E0277);
  - group G: `Serialize` (E0277).
- **Group E reuse** (E0382): `open` twice on one operation, `begin_journal_txn` twice, `abort` twice, `finish` twice.
- **Group F:**
  - `CommitSession::open(op, execution_id)` (E0061);
  - item 3a's census of `ProjectOperation`: sixteen crate-private inherent functions (E0624 "method `…` is private") and three `cfg(test)` ones (E0599 "no method named `…` found");
  - the `cfg(test)` producer `begin_operation_with`, pinned by `OrdinaryWriteAdmission` being unnameable (E0603).

The driver passes with 76 cases and 8 self-tests.

## Judgment calls: please rule

1. **Placement.** The session types live in `custody/commit_session.rs`, not in `commit_authority.rs` as the inventory's planned description of that file says. They need `ProjectOperation`'s crate-private owners and the custody-internal row types, as X4a's `operation_guard` did. `commit_authority.rs` keeps the gate primitive and `PreparedJournalSeal`. **Rejected:** widening custody's internals to the crate root.
2. **The detached level 3.** `ProjectOperation` lends the lock and location only inside a charged closure (`journal`), so a `JournalWriteTxn` that owned both the session and a borrowing `JournalTransaction` would be self-referential.
   - `JournalTransaction::detach` keeps the open `BEGIN IMMEDIATE` connection and its tail.
   - `DetachedJournal::attach(lock, location)` rebuilds the transaction under the same lock (another carrier is refused) at step 3.1.
   - Nothing is released between them, and `acquire` rechecks the tail as before.

   **Rejected:** `unsafe` self-reference; a closure-shaped `begin_journal_txn`, which would not match item 1's and item 4's signatures.
3. **Every certain refusal before admission latches the gate (`0 → 2`).** The source is X4 item 7: "a latch takes the gate from 0 to 2 … the operation ends refused". `OperationGuard::stop` is the fetch-OR 2. This makes item 7's "the gate is latched" owe the `REV` after the refusals item 13 tests. Two of them, busy at the evidence `BEGIN` and the publication-reserve overrun, come before any `SEAL`, so only the latch can owe their `REV`. `CarrierCapacityExhausted` is not a refusal and does not latch. **Rejected:** a separate "refused" flag, which would be a fourth `REV` condition beyond item 7.
4. **The closed `REV` reasons.**
   - S6's own words, `trust-revoked`, `policy` and `observer-fail-stop`, map from the recorded stop cause.
   - Two more cover the other latches: `stale-guard`, and `operation-stopped` for any other certain refusal or a `SEAL` without its commit.
   - No `trustEpochObserved` is recorded ("if X3d-1 records one").

   **Rejected:** a free-text reason, and an epoch object.
5. **The `CLN`.** F38's fixed pair is `["seal-without-evidence-commit", "evidence-transaction-rolled-back"]`. It is owed exactly when a durable `SEAL` has no evidence commit, which is M2's only residue: X4 item 7 leaves brokered residuals unclaimed.
6. **The exact cost.** Each kind is costed at its longest closed draft. The bound sits at the widest grant generation (`i64::MAX`) and the last ordinary sequence, because the body and the witness grow only with those decimal widths.
   - A real `REV` and `CLN` at sequences …989 and …990 of generation 1 charge exactly `end_path_append_cost(gen, seq)`, measured on the attempt ledger. Objects and edges equal the bound; bytes are below it.
   - Each draft is also held to its kind's body bound before its append. Only the closed drafts exist, so in production this is a guard on future code. The test feeds it a reason one byte longer, a longer residual and an epoch, and each is refused.
7. **The operationRef.** `open` also draws the operation's `op-` token from the CSPRNG. Item 2 names only the ExecutionId draw. But every journal record of the operation needs an operationRef. The build plan's identity table says "Exact security-owned op- plus 32 lowercase hex token from the live session", X3b item 13 says the host mints it per operation, and the attempt row maps ExecutionId to operationRef. **Rejected:** deriving it from the ExecutionId, which the identity table forbids.
8. **`ProjectOperation` exported, with its rows.** The public `open(ProjectOperation)` needs it public, or clippy's `private_interfaces` fails. Under X8's export rule an exported type gets the full capability set, so X3d-1 adds its D, E and G cases and item 3a's census: nineteen methods and the unnameable `OrdinaryWriteAdmission`. X8's table lists `ProjectOperation`'s rows under X2e, which integrated before X8a, so no unit had added them. X2e's internal `end_with` body was split into the free function `end_entered`, behaviour unchanged, to place the `x3d.finish` points without adding an inherent function.
9. **Six `InstallationTermination` variants.** X3d item 9 says every row maps through 468c's vocabulary. 468c lacks `LEDGER.CORRUPT`, `DURABILITY.COMMIT_FAILED` and X2's project rows, and no unit has owned their public projection. A stale guard keeps X2's own row (X4 item 8), so `termination()` cannot be total without them.
   - Each uses an existing detail with S12's class: lines 1302, 1309, 1310 and 1323 of `security-and-lifecycle.md`, and X3d item 9's durability row.
   - The host table gains six rows, and the class/fault pairing test admits `LEDGER.CORRUPT`/`ledger-corrupt` and `DURABILITY.COMMIT_FAILED`/`durability-commit`.

   **Rejected:** returning the internal row to storage, which cannot name it; and a fallback row.
10. **The adapter's shape.**
    - `CommitAdapter::stage(self, &JournalSealBinding, &mut WorkScope) -> Result<Staged, WorkFailure<Refusal>>` runs inside the SEAL path's charge.
    - `StagedCommit::commit(self) -> EvidenceCommit<Committed>` runs only inside `permit.consume`.
    - Storage's staging refusal is returned verbatim (`SealRefusal::Staging(R)`), so storage names its own row.
    - The traits are public. X8 3b leaves the single-implementer rule to X3d-2's source pin.
11. **One charge for the whole SEAL path, and failures as `Err`.** Every stop, the undetermined evidence `COMMIT` included, returns `Err` from the closure, so the attempt ledger closes as the platform latch requires. It is never reported as a value. The outcome is classified after the charge returns.
12. **`capacity`'s tail.** It is the lock's proven tail, through a new non-waiting `proven_tail`. That adds a third `try_lock`, so X3b-2's never-waits pin now counts three. It falls back to the start tail, which in M2 is the same.
13. **What X3d-2 receives.**
    - `charge` lends a `WorkScope` on the attempt ledger, never the ledger or the reserve.
    - `refused()` and `undetermined()` take no row: storage names its own.
    - The read-only getters are N, S, G, K, the carrier digest, the core closure and the operationRef.
14. **Crash points.** All are `step` points; `.before` and `.after` are part of the step name, as X4a's `admit.after` is. No injected failure path is added.
    - `x3d.session.execution-draw` (draw) and `settlement-reserved`.
    - `x3d.publish.after-staging`, `before-final-checkpoint` and `commit-returned`. `published` is X3d-2's.
    - `x3d.finish.settle.before` and `.after`, `lease-release`, and `end-step.before` and `.after`.
15. **The settlement source pin.**
    - The security test holds each link of the chain to one production call site, in the next file along. It also checks that the session's calls sit inside `reserve_end_path` and `finish`.
    - X3d-0's platform pin ("no production caller yet"), which named X3d-1 to replace it, now admits exactly the chain's six files, with one `.reserve_settlement(` call.
    - The ordinary writer's own private `settle` helper, an unrelated method, is the one other `.settle(` in production.
16. **`StoppedSession` boxes the operation and the ids.** Clippy's `result_large_err` flags the refusal tuples otherwise.
17. **Tests use a test adapter.** Storage's real half is X3d-2. The four certain refusals of item 13 are produced as follows:
    - the publication-reserve overrun: a charge beyond the limits;
    - busy at the evidence `BEGIN`: a `WorkFailure` inside `JournalWriteTxn::charge`, then `abort`;
    - the staging I/O error: an adapter `Err`;
    - the failed repeated checkpoint: the final checkpoint, with the scripted clock advanced 11 s during staging.

## Not done, for the lead

- **F39 end to end.** `latched_after_admission` is not exercised by an X3d-1 test. A latch between the permit and the `COMMIT` needs an observer tick inside `consume`, which X9's matrix (F39) drives with `x4.gate.admit.after`. X4a's tests cover the gate half.
- **Out-of-date descriptions.** `commit_authority.rs` ("Mint opaque live CommitSession …") and the platform test's "until X3d-1" are out of date. They are listed with the others in the inventory README for D1.
- **X3d r7.** X8 r3's record-only changes to X3d (item 12's fixture source, item 11's adapter case, "the X8 doctests") are untouched here.

## Tests

New: 21 in security, 50 compile-fail cases, 6 projection-table rows. One platform pin is rewritten.
- **`commit_session_tests.rs`: 18, through the real handoff:**
  - **`open`:** its ids and binding;
  - **a lawful commit:** one `SEAL`, no `REV` or `CLN`, and the floor copied;
  - **certain refusals that close the attempt ledger, each followed by the `REV`** (and the `CLN` after a `SEAL`) **with the end step taking no fence:**
    - the publication-reserve overrun;
    - busy at the evidence ledger, then `abort`;
    - a staging I/O error;
    - a failed final checkpoint (`observer-fail-stop`);
  - **a failed `REV`** (busy carrier): no `CLN`, and busy disclosed;
  - **a refused step 0:** no reserve, nothing appended;
  - **the invariant row:** an unfunded journal transaction, and a second reserve;
  - **uncertain outcomes,** each with nothing appended and no end step: an uncertain `SEAL` commit, an undetermined evidence `COMMIT`, an undetermined attempt admission;
  - **an exhausted generation:** returned with the ledger open, then rolled over;
  - **the reserve:** it equals the two bounds; the closed reasons; a draft one byte over is refused;
  - **the exact charge** of a real `REV` and `CLN` at …989 and …990;
  - **the settlement chain pin;**
  - **the crash point names.**
- **`commit_session.rs` unit tests: 3.** Every carrier row's and every project row's termination, and the id grammars.
- **Renamed:** the commit_authority SEAL binding test now borrows the replay.

## Checks

Product checks are at 0fc8ea2 plus this diff. Arch verifiers run against the real lock at 0fc8ea2, which selects v113.
- **Workspace runs:** two full runs on the final bytes (each with 1546 passed, 0 failed and 3 ignored, across 17 test binaries).
- **Lints:** `cargo clippy --offline --workspace --all-targets -- -D warnings` is clean. It is also clean with `-p opensip-platform --features crash-matrix`, and with `-p opensip-security --features opensip-platform/crash-matrix`.
- **Formatting:** `cargo fmt --all -- --check` is clean, and so is `rustfmt --edition 2024 --check` on the `include!`d files this unit touches or adds.
- **`check_package_edges --lane host` against v119:** passes, with 19 declared and 19 resolved edges and no new edge.
- **verify_scratch:** passes, with 81 inventory successors, 72 contract successors and 16 inheritance rows; v119 is selected.
- **verify_projection against the real lock:** 16 rows; 83 corruptions refused.
- **`build_v119.py`:** reruns produce the same bytes. 897 files; the 845 v113 rows are equal by value.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does X3d-1 meet X3d r6 items 1 to 4, 7, 8 and 9, and item 13's X3d-1 list? In particular:
  - one session per operation, and its draws;
  - the reserve: taken first, exact, held only by the session and the stopped session, spent only by `finish` (the `REV`, then the `CLN`), forfeited at every uncertain classification, never refunded;
  - the order of item 4 step 3 and the stop order, exactly once;
  - nothing appended or entered after any uncertain outcome;
  - the end step skipped on a closed attempt ledger;
  - the single production caller of each settlement method.
- Are the `x3d.*` points the right names and places?
- Rule on calls 1 to 17.
- Do the fifty cases pin what X8 r3 assigns to X3d-1?
- Is v119 right on v113?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `commit-session-x3d1-inventory-v119-subject.json` (lead's value `15a80a28d61ce2b03afd87626196f21d23cb1cfe692fc41e711c7c96b5fd06da`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v119, parent (the v113 pin), successorRecord (the pin of `commit-session-x3d1-inventory-v119/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
