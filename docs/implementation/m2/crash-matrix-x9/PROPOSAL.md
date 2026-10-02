# The crash, lock and revocation matrix — proposal X9 r8

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X9 of `EXIT-PLAN.md`, the unit that gates M2 completion. It is written under:
- the build plan's M2 row (`docs/v2/architecture/implementation-boundaries-and-build-plan.md` line 886: "actual crash/lock/revocation matrix pass; synthetic fixtures remain labelled"), its ordered failure matrix F00–F53 (lines 524–587), its required API and fault-injection checks (lines 591–613; the test owner `crates/storage/tests/commit_tests.rs`, line 594), and the tooling row for storage and process faults (line 1072: "deterministic synchronization and crash barriers against actual storage/processes … Record platform/filesystem/profile, actual state bytes and exact outcomes; inject before/after each durability step, without sleep-and-hope synchronization");
- `EXIT-PLAN.md`'s X9 row and its "Choices left open" recommendation for crash injection;
- the accepted laws X2 r8, X3a r5, X3b r10, X3c r7, X3d r6, X4 r7, X4T r9, X6 r2 and X7 r3, for every failure case each one assigns to X9 or says "X9 records".

r1 was ACCEPTED by Grok on 2026-10-02; r1 bytes, without that note, are preserved in PROPOSAL-r1.md. r2 ACCEPTED by Grok on 2026-10-04.

r2 (2026-10-01) is an amendment made as lead decisions under the owner's standing direction. It changes two things and nothing else:
- **F34 (follows X6 r3 item 6).** A writer's invocation can never recover, because X1 r1 items 1 and 7 give a process one attempt and one entry. F34's row is rewritten: the injected run ends on the invariant row with the requested binding disclosed, and a separate recovery run gives `BindingUnusable` or the attempt's standing.
- **The clock (EXIT-PLAN, "X9 clock dependence", found by X9-1).** Since X4a, a fenced first read publishes a trust floor only when the wall clock, in whole seconds, has passed the stored evaluation floor F (X4T r9 item 7's write-ahead). So whether `x4t.floor-publication` is reached, and the trust store's bytes, depend on when a process runs (34 against 39 creates were observed between lawful runs). That breaks item 5's fixed kill set and item 7's repetition agreement. Item 3 gains a scripted wall clock in every matrix process, and items 5, 6, 7 and 12 follow.

**r3 (2026-10-04) is record-only.** r2 bytes are preserved in PROPOSAL-r2.md. r3 ACCEPTED by Grok on 2026-10-04. It records decisions already accepted elsewhere, and the current status of this law's cross-law gaps. It changes no injection mechanism, point kind, scope, label, evidence member, row, limit or forbidden substitute of r2, and no accepted outcome of any other law. The r2 sentences it touches stay in place, each followed by a short "r3 (record)" note that points here.
- **G5 is resolved by X6c (`reviews/grok-settlement-sweep-x6c-r1`, judgment call 1, accepted with no new law sentence).** A revoked closure subject does not refuse the sweep, and that includes the running core's own release closure.
  - **Why.** The sweep's admission is X1's `admit_ordinary_writer` and nothing else. X1 item 4 grants that admission no trust admission, and X6 r3 item 7 adds none: the sweep takes no X4 guard and reads no trust record. X6c's test `a_view_revoking_the_running_closure_does_not_refuse_the_sweep` pins this.
  - **The ladders.** C5 therefore no longer stops the F18, F19 and F38 ladders at R2. Their ladders run:
    - **R3:** the sweep is admitted under the revoked view, and settles the crashed attempt `refused`. A crashed attempt here is phase `admitted`, with neither receipt nor association, and its lease free.
    - **R4:** `terminal-not-committed`, the owner's composed case in §2.1.
  - **Recording the outcome.** These runs record that R3 and R4 outcome, not `"ladderEnd": "G5"`. X9-4 transcribes it.
  - **C5's rejection still stands.** C5 rejected X9 choosing the expected R3 itself. That is unchanged: X9 transcribes X6c's accepted reading and decides nothing.
  - **The alternative X6c rejected.** A fenced X4T trust admission on the sweep. It would be a new X1 or X6 sentence, and it would leave every revoked attempt `admitted` for as long as the revocation stood.
- **The joint predicate (X8 r3 item 4b, recorded as a wording change to X9 r1 and accepted with X8 r3).** X8's `scenario` surface and this law's `crash_matrix_support` share their fixture gates. A Rust item has one cfg predicate, so the two laws use one site list: X9-1's pin, extended by name by X8b. Two sentences change wording. No barrier point, `crash_matrix_support` item, row or outcome changes.
  - **Item 6.** The sentence "that `cfg(test)` becomes `cfg(any(test, feature = "crash-matrix"))` … no other site may use the feature" reads, for the shared sites, `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`.
    - **What the shared sites are.** At X8 r3: `Image::Injected`, `HomeSource::Fixture` and its `admit_with` arm, X4T-0's declaration, and the fenced `state.v1` publisher that item 6's helper and X8's `scenario::publish_revocation_fenced` both call.
    - **Crash-matrix-only sites.** A site that only `crash_matrix_support` calls keeps `cfg(any(test, feature = "crash-matrix"))`.
    - **Barrier and fault sites.** `AppendStep`, `ObjectStep` and the ledger commit hook stay `cfg(test)`, with this law's points beside them.
  - **The forbidden substitute.** "a `cfg(any(test, feature = "crash-matrix"))` site … in a build reached without an explicit `--features crash-matrix`" now excepts the shared sites reached through `scenario-fixtures`. Only `[dev-dependencies]` enable that feature. Those sites are still absent from every release build (X8 r3 item 4f).
  - **What stays forbidden** (X8 r3): folding the two features into one, enabling `crash-matrix` from any manifest, and a second site list or pin.
- **G1 to G4: current status.**
  - **G1 is open.** Its fix is item 6's support surface, together with X8b's `scenario-fixtures`.
    - **X9-1** builds that surface: the support modules, the shared site list under the joint predicate, and the fenced publisher. It is under review (`reviews/grok-crash-matrix-x91-r1`) and is not integrated.
    - **X8b** is not built.
    - **The units G1 names integrated before X9-1.** Each split its tests and deferred the cross-crate composition:
      - X3d-2 (review call 1): to X8c's B0–B4 and X9-2;
      - X6b (call 13): admission and `recover` in one fresh process, to X9-2 and X9-3;
      - X7a (call 16) and X7b (call 10): the session-level finalization rows, to X8c, X9-5 or an X7a-2 after X9-1.
    - **The one-line test-item amendments.** X3d r7 and X7 r6 record these in this batch. X6 item 11's waits for X6's next revision.
  - **G2 is open.** No law has restated its literal "`cfg(test)` only" sentence yet: X3c r7 item 11, X3b r10 item 11, and X4T item 12 (r9 when this law was drafted, r11 now). Item 2's guards meet the invariant those sentences protect. X9-1, still under review, also widens X4T-0's declaration and the fixture home source under the joint predicate. Each restatement waits for its law's next revision.
  - **G3 is closed by X6a and X6b.**
    - X6a placed the `x6.recover` bracket points `after-w1`, `after-h1`, `after-j`, `after-w2` and `after-h2`, and `after-fresh-capture` (`reviews/grok-recovery-capture-x6a-r2`).
    - X6b placed `after-lease` and `after-ledger-snapshot` (`reviews/grok-recovery-admission-x6b-r1`).
    - X6c placed item 5's `x6.sweep` points, which F53 uses.
  - **G4 is closed by X4a (`reviews/grok-live-guards-x4a-r1`).** It placed:
    - `x4.observer.tick` (kind `gate`) and `x4.observer.after-observation`;
    - `x4.checkpoint.before-observation`, `.after-observation` and `.before-admit`;
    - `x4.gate.admit.after` and `x4.gate.latch.after`.
- **A disclosed gap from X9-1, for X9-2 and X9-6 (from X9-1's review request; the review is still pending).** X9-1's census runs unarmed, so X4a's observer waits on its real 5 s period. X9-1 discloses it; it decides nothing.
  - **Why it holds today.** Each censused operation finishes well inside 5 s, and two census runs agree.
  - **What would expose it.** An operation slower than 5 s would add an observer reading and point. Under item 5 (r2), two census runs that disagree are a `HARNESS-ERROR`, never a smaller kill set.
  - **What it does not touch.** Matrix rows that arm `x4.observer.tick` (item 11) do not depend on the period.
  - **Who owes it.** X9-2's and X9-6's census runs, and this law's next revision if those runs need a rule for it.
- **Unchanged from r2:** everything else.

**r4 (2026-10-02) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r3 bytes are preserved in PROPOSAL-r3.md. r4 ACCEPTED by Grok on 2026-10-02. It was found while starting X9-2. It changes two things and nothing else.

- **The three driver entries (item 6 and the forbidden substitutes).**
  - **What X9-2 found** at product `a36da7c`. X9-2's drivers run in storage's matrix target. That target links security as an ordinary library, and it can obtain none of the three admissions its drivers start from over item 6's synthetic installation:
    - **The operation** (the `commit` driver, and R2's next writer). `admit_ordinary_writer`, `ordinary_writer::admit_with` and `OrdinaryWriteAdmission::begin_operation` are crate-private (`security/src/custody/ordinary_writer.rs`, lines 220 and 493–506), and no writer command is enabled in M2. So no production path outside security yields a `ProjectOperation`. Item 6 and this law's forbidden substitutes bar a support function that returns one. X8 r3 item 4's `scenario::operation` is the only lawful route. It is X8b's, it is not integrated, and it is not among X9-2's dependencies.
    - **The recovery admission** (R1 and R4). `RecoveryAdmission::admit` is the only public constructor (X6 r3 item 2). It always takes `HomeSource::Native`, the account database's home (`recovery_admission.rs`, lines 484–509): the real account's home, which no matrix process may touch, and which this BASELINE-ATTESTED host refuses. The fixture form (`admit_on` over `HomeSource::Fixture`) is crate-private. No law exposes it, and X8's `scenario` has no recovery entry.
    - **The sweep admission** (R3). `SettlementSweep::admit` is `admit_on(admit_ordinary_writer()?)`. It is native-only in the same way, and its fixture form is crate-private.

    X9-1's census reaches all three only because it is in-crate (`crash_matrix_census.rs`: `InstallationAt::writer` and `begin_operation`). X9-1's request (call 7) left X9-2 needing "X8b's or this surface's operation path", and its review accepted that without a ruling.
  - **Decision.** Item 6 gains exactly three driver entries in security's `crash_matrix_support`, forwarded unchanged by storage's and host's modules (item 6, r4). Each returns only what an existing crate-private production composition returns over the fixture home. This is the same exception X8 r3 item 4 gives `scenario::operation`. The forbidden substitutes are amended to match.
  - **Rejected:**
    - **A callback-style support function** that passes the `ProjectOperation`, `RecoveryAdmission` or `SettlementSweep` to a caller's closure and returns the closure's value. It would hand out the same authority type while technically not returning one. It meets the letter of the forbidden substitute and defeats its purpose, and it hides the exception instead of naming it.
    - **A home override on the production entries.** For example, a feature-only branch in `admit_ordinary_writer`, `RecoveryAdmission::admit` or `SettlementSweep::admit` that takes H from the environment. It would add a site outside X9-1's pinned list, which item 6 forbids. It would also put a test-only input inside a production entry. And it would still not produce the synthetic read and write receipts, which come from 462's signed test trees rather than the native platform.
    - **Waiting for X8b's `scenario::operation`.** It covers only the operation, so recovery and the sweep would still have no route. It would also tie the matrix target to `scenario-fixtures`, and X9-2 to X8b.
- **The per-unit check (items 7 and 12).**
  - **What X9-2 found.** `tools/check_crash_matrix.py check` requires `product.commit` to be the reviewed commit on a clean worktree, and every kill-set point of the full census to be killed by a process-death run. A unit's run set before X9-6 can meet neither: the unit is uncommitted while it is reviewed, and most of the census belongs to other units' rows.
  - **Decision.** X9-2 to X9-5 each apply the checker's per-run check and its repetition agreement to their own subset of `required-runs.v1.json`. The full `check`, with a clean committed tree and full kill-set coverage, belongs to X9-6 only. X9-2 adds the subset mode (item 7, r4).
  - **Rejected:** relaxing `check` itself, which would weaken the exit gate; and skipping the checker until X9-6, which would leave each unit's run records unchecked against their reviewed rows.
- **X8 cross-reference.** X8 r3 items 4b and 4e say that `crash_matrix_support` "still returns no authority type". From r4 on, that sentence reads with this law's three-entry exception. X8 is not edited here, and its next revision may restate the sentence. The two exceptions stay separate:
  - `scenario::operation` stays under `scenario-fixtures`;
  - the three entries stay under `crash-matrix` only;
  - neither surface calls the other;
  - there is still one shared site list (item 6, r3).
- **G1.** With r4, the matrix half of G1 has a lawful route. X9-2 closes G1 for its own rows.
- **Unchanged from r3:** every injection mechanism, point, kind, scope, label, evidence member, row, expected value, limit and other forbidden substitute. No accepted outcome of any other law changes. No new public code, row or detail.

**r5 (2026-10-02) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r4 bytes are preserved in PROPOSAL-r4.md. **r6 (2026-10-02)** answers Grok's X9 r5 RF-1 and changes nothing else. r5 bytes are preserved in PROPOSAL-r5.md. r6 ACCEPTED by Grok on 2026-10-02. The fix: a kill at `x3c.ledger-create.ddl.commit.after` comes after a schema `COMMIT` that returned success (`write_schema`, `project_ledger.rs` lines 500–502). So that point belongs to F00's UAU window, not its UC window. r6 corrects the two F00 sentences below and the F00 cell's r5 clause in place, because r5 was not accepted. X9-2 found these issues while transcribing its rows into `required-runs.v1.json`, before any run. The product is unchanged at `a36da7c`. r5 changes three things and nothing else.

- **F07 to F10: R1 is plain UAO (item 9).**
  - **What X9-2 found.** For F07 (and F08, "as F07"), F09 and F10, R1 was expected to be UAO with a witness diagnosis (would-REVERT, would-ADVANCE, or OK). The integrated `recover` cannot report one:
    - `RecoveredCommit::UnknownAttemptOpen` carries no fields (X6 r4 item 2's closed list; `storage/src/recover.rs` lines 101–104).
    - `recover` returns UAO at step 2 from the ledger standing alone (lines 380–381). An admitted attempt with neither receipt nor association is UAO (`recovery.rs` line 290).
    - The carrier capture, the only source of `witnessWould*` (`CarrierObservation::diagnosis`), runs only after the ledger joins a receipt and an association (lines 395–419).

    In these rows the evidence `COMMIT` never happened, so no such join exists.
  - **Decision.** In these rows R1 is plain UAO. The would-REVERT, would-ADVANCE or OK expectation moves to R2's witness action only (item 8's "start's witness action"), which each row already states. No X6 or X3b outcome changes.
  - **Rejected:** a carrier diagnosis on UAO, which would change X6's closed standings and its step order; and a separate carrier capture in R1's process, which X6 has no public route for and which item 8 does not ask of R1.
- **F00: split by kill point (item 9).**
  - **What X9-2 found.** F00 is a first commit, since it reaches registration and INIT. The ExecutionId is drawn in `CommitSession::open` (`x3d.session.execution-draw`), and `prepare_commit` creates the store directories and the ledger afterwards, inside `x3c.ledger-create`. A kill in between leaves one of two states:
    - no ledger: `read_recovery_ledger` gives `Missing` (`ledger_store/recovery_read.rs` lines 136–146), and `recover` gives UnknownCustody `ledger-missing` (`recover.rs` lines 314–325);
    - a ledger whose schema has not committed: UnknownCustody `ledger-unreadable`.

    Either is X6 r4 item 4's F24 sentence: "A missing, empty or fallback ledger or carrier is never absence". The row's "R1 and R4 UAU" therefore holds only once the ledger exists.
  - **Decision.** F00's runs are expected by kill point:
    - **before the draw** (no ExecutionId): R1 and R4 are not applicable (`"notApplicable": "no-execution-id"`, item 8);
    - **from the draw through `x3c.ledger-create.ddl.commit.before`**, that point included (r6): R1 is UC with reason `ledger-missing` or `ledger-unreadable`, whichever the kill left, and R4 is UAU, because R2 has created the ledger by then;
    - **from `x3c.ledger-create.ddl.commit.after`**, that point included (r6), until `x3c.attempt.commit.after`: R1 and R4 are both UAU.

    In every split, R3 writes nothing, and the rest of the row (no attempt row, the ledger's logical state unchanged, R2's crash-state handling and Committed) is unchanged. Which split a kill point falls in is fixed by its position in the census trace relative to those two points, never by a run's outcome. X9-2 transcribes the split into `required-runs.v1.json` before any run.
  - **Rejected:** keeping UAU for the whole window, which contradicts X6's F24 rule; and starting F00 from a namespace whose ledger already exists, which would drop registration and INIT from F00's kill set.
- **The synthetic run candidate moves to X9-2 (items 6 and 12).**
  - **What X9-2 found.** `prepare_commit` refuses unless two things hold (X3d item 3 step 1; `storage/src/commit.rs`, `plan`). No corpus Run meets either:
    - the Run's `projectId` must equal the session's ProjectId, and a first registration draws that id at random (`first_registration.rs` line 427);
    - the Run's evaluator closure must equal the session's selected core closure, and the injected test inventory's closure differs from every corpus closure.

    Item 6 already lists "a synthetic run candidate for the evaluator's public `replay_run`". X9-1 left it to X9-5, and X5 r3 left X8c's B0 Run to X8c. X9-2's `commit` driver cannot commit without it.
  - **Decision.** X9-2 adds the candidate to the support surface. Because it needs the evaluator, it lives in storage's `crash_matrix_support`, which host forwards.
    - **Inputs only.** It produces the retained inputs (objects and blobs) and the claimed RunId, never a `ReplayedRun` (item 6's forbidden list stands).
    - **How it is built.** It starts from a pinned corpus Run. It rewrites the snapshot's `projectId` and the evaluator closure to the caller's values (read from `CommitSession::project_id` and `core_closure`). **r7 (record):** the evaluator closure comes from `core_evaluator_closure`, and its descriptor is retained (see the r7 header). It recomputes every content id and blob digest that depends on them. It re-derives the outputs with the evaluator's public `derive_evaluation`, then builds the evidence, seal and Run descriptors as `replay_run` checks them.
    - **The production mint.** `replay_run` in the matrix child stays the only constructor of the `ReplayedRun` that `prepare_commit` takes.
    - **Labels.** Every run that uses it stays labelled `synthetic`.
  - **The matrix-only order.** A first registration draws the ProjectId inside the operation, so the matrix child calls `replay_run` after `CommitSession::open` and before `prepare_commit`. Replay is pure and takes no custody, so no X3d step changes. This order is stated for matrix children only. The host's order, replay before any custody (X5 r3 item 3, F01), is unchanged and stays X9-5's.
  - **Rejected:**
    - **A corpus Run with the ProjectId fixed to it.** That needs either a scripted ProjectId draw, which is a new cfg site, or rewriting the registry row and project marker after registration, which is a custody mutation outside item 6's inputs and would label every run `mutation`.
    - **Registering the root in the fixture child.** It removes registration and INIT from F00's kill set.
    - **A support function returning a `ReplayedRun`.** That is a forbidden authority type.
    - **Rewriting the outputs textually without re-derivation.** The derived proof carries digests of normalized evaluation records that no reference substitution reaches.
    - **Waiting for X8c's B0 Run.** It would couple the matrix to X8c's unit and order.
- **Not legislated.** A possible F00 state after `x3c.ledger-create.wal` and before `ddl.commit`, a non-empty ledger with a WAL that `create_or_open_ledger` may not resume, is not decided here. If a run shows it, X9-2 stops and reports it.
- **Unchanged from r4:** every injection mechanism, point, kind, scope, label, evidence member, limit and forbidden substitute, and every row and expected value not named above. No accepted outcome of any other law changes. No new public code, row or detail.

**r7 (2026-10-02) is record-only.** r6 bytes are preserved in PROPOSAL-r6.md. r7 ACCEPTED by Grok on 2026-10-02. It records X3d r8 and the identity contract successor EC1, reviewed together with it (`reviews/grok-evaluator-closure-x3d-r8`). It changes no injection mechanism, point, kind, scope, label, evidence member, row, expected value, limit or forbidden substitute of r6, and no accepted outcome of any other law. The r6 sentences it touches stay in place, each followed by a short "r7 (record)" note that points here.
- **The closure binding (X3d r8 item 3 step 1; EC1).** The r5 header's reason, "the Run's evaluator closure must equal the session's selected core closure", described X3d r7. No Run could meet it. A core closure is `kind: "core"`, and replay requires `kind: "evaluator"`. That is the blocker X9-2 found. X3d r8 compares the Run's evaluator closure with the session's core evaluator closure, `CommitSession::core_evaluator_closure()`. EC1 defines that value as the authenticated core descriptor with `kind` set to `"evaluator"`.
- **The synthetic run candidate.**
  - **What it rewrites.** It rewrites the evaluator closure to the session's core evaluator closure (`CommitSession::core_evaluator_closure`), not to `core_closure`.
  - **What it keeps.** It keeps that closure's descriptor as a retained closure object, with its manifest blob (the injected inventory body) and its tree blobs, through security's shared test-support accessor (X3d r8 item 13).
  - **What stays the same.** Everything else in the r5 header's "How it is built": the `projectId` rewrite from `CommitSession::project_id`, the recomputed content ids and blob digests, the re-derivation with `derive_evaluation`, inputs only, never a `ReplayedRun`, and the `synthetic` label.
- **Who lands it (X3d r8 item 13).** X3d-3 lands the candidate in storage's `crash_matrix_support`, under the same gate, because X3d-3's own storage tests need a Run that binds to a real session. X9-2 uses it and no longer adds it. X9-2 now also depends on X3d-3. Its `commit` driver order (replay after `CommitSession::open`, matrix children only) is unchanged.
- **Unchanged from r6:** everything else.

**r8 (2026-10-02) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r7 bytes are preserved in PROPOSAL-r7.md. X9-2 ran every one of its 232 transcribed rows once, in a development run on product `a2c5e8b`: 167 passed, 65 failed, and none was a harness error. Each failure was the owning law's lawful outcome for the crash state the kill left, where this law's row had expected another. r8 changes F00's and F07's R2, adds limit L11, and makes four of X9-2's choices law. Nothing else changes.

- **F00: R2 is the owning law's outcome for the crash state (item 9).**
  - **What X9-2 found.** F00's row expected R2 to reach Committed after every kill before `x3c.attempt.commit.after`. For 57 kill points, the next writer instead refuses permanently on the owning law's row:
    - **Registration.** Kills from `x2.fence.register.reserved/rename.after` through `x2.fence.register.active/rename.before` leave a RESERVED row, or partial namespace or marker owners. The next writer refuses with `PROJECT.ROOT_CUSTODY_REFUSED`, subject `identity-recovery-required` (X2 r8 item 3, "RecoveryNeeded: a matching RESERVED row", and item 8). Two points differ:
      - after `x2.fence.register.marker/create.after`, the marker exists before its private sample, and the subject is `marker-custody`;
      - at `x2.fence.register.marker/write.before`, the marker is private but empty, and the subject is `identity-contradiction`.
    - **A created owner not yet sampled private.** A kill at a creation's `create.after`, before the private sample that follows it with no point between, leaves an object that is not private:
      - `x3c.ledger-create.projects`, `x3c.ledger-create.namespace`, `x3c.object.objects`, `x3c.object.sha256` and `x3c.ledger-create` (the ledger file): `create.after` refuses on X3c's custody row (`Custody`, subject `private`). R2 never creates the ledger, so R4 stays UC.
      - `x3b.floor.directory/create.after`: the floor directory refuses on X3b's host I/O row.
      - `x4t.floor-publication.dependency`, `create.after` and `write.before` of a dependency file: the file is present and empty. Whether the next fenced read names that dependency, so that X4T's read refuses `INSTALLATION.INCOMPLETE`, or does not, so that the commit proceeds, is X4T r9's reading of that dependency. X9 does not restate it. Each such point admits either outcome.
    - **The WAL gap r5 left undecided.** `x3c.ledger-create.wal` and `x3c.ledger-create.ddl.commit.before` leave a non-empty ledger with a WAL. That is "a partial creation footprint other than item 2's resumable empty file", and it refuses `LEDGER.CORRUPT` (X3c r7 item 10). R4 stays UC.
  - **Decision.** F00's R2 expectation is the owning law's outcome for the crash state at the kill point, transcribed by census window as above, and Committed everywhere else. Where R2 does not create the ledger, R4 stays UC (`ledger-missing` or `ledger-unreadable`, whichever the state left). R1's split (r6), "R3 writes nothing", "no attempt row" and the R2 witness action are unchanged.
  - **Rejected:**
    - **A resume or repair path in the owning laws, added to make R2 commit.** M2 has no recovery or repair writer for any of these states. Writing one is M3's work (L11). An expectation that a missing writer would meet is not one this matrix can assert.
    - **Dropping these kill points from F00.** The census and the kill set are fixed by item 5, and each point's refusal is the evidence that the owning law fails closed there.
- **F07: R2's witness action is split at the pending witness's rename (item 9).**
  - **What X9-2 found.** F07's row expected R2 REVERT after every kill at `x3b.append.seal.witness-pending/*` and at `insert.before`. Before `witness-pending/rename.after`, the PENDING witness is not yet visible: only its temporary file exists. So the start reconciles as consistent, and the witness action is OK. Seven points gave OK.
  - **Decision.** R2's witness action is OK before `x3b.append.seal.witness-pending/rename.after`, and REVERT from that point on, `insert.before` included. Committed and the rest of the row are unchanged. F08 ("As F07") is after the rename, so it stays REVERT.
  - **Rejected:** keeping REVERT for the whole scope, which the start's reconciliation (X3b items 4 and 4a) cannot produce before the rename.
- **L11, recorded and not tested (item 10).** The states F00's split names leave the project refused permanently until a repair or resume writer exists:
  - an interrupted first registration;
  - a created owner not yet sampled private;
  - a partial ledger WAL.

  X9 records these as an M2 known limit. No product code is added. The later owner is M3, a repair or resume writer. `matrix.json`'s `limits` carries L1 to L11. The checker's limit list follows, in both `check` and `check-unit`.
- **Four choices made law (items 5, 7, 8 and 9).**
  - **Census scope (item 5).** A unit's census is the census of its own drivers. X9-2's census is its `commit` driver's lawful first commit on a fresh root: two runs, equal point for point. The `recover` and `sweep` censuses are X9-3's. X9-6's census is the union.
  - **The trace digest (item 7).** A child's `trace.sha256` hashes its records grouped by thread, in each thread's own order and threads by index. The pid and the process-wide sequence number are left out, because they interleave between threads. Every drawn value in a payload is numbered by first appearance with item 7's normalizer. Without this, an unarmed observer tick interleaving with the main thread, or a drawn ExecutionId in a payload, would make two lawful repetitions disagree.
  - **R3's value (item 8).** R3 is scored against the left attempt's ExecutionId. That is the outcome the sweep wrote for it, or "nothing". R2 is a lawful commit whose attempt the sweep also settles, `committed`; that settle is recorded beside R3 (`nextWriter`) and is not part of the row's R3. "R3 writes nothing" means nothing for the left attempt.
  - **F46's second variant (item 9).** "An association below `first_generation`" is not executed in M2. A fresh carrier's first generation is 1, and the ledger's `CHECK (grant_generation >= 1)` admits no association below it. Only a migrated carrier has a higher first generation, and no migration writer exists (L5). F46 runs the format-1 and format-2 variants.
- **Unchanged from r7:** every injection mechanism, point, kind, scope, label, evidence member and forbidden substitute, and every row and expected value not named above. No accepted outcome of any other law changes. No new public code, row or detail.

Product baseline: main `f1b8321` (X3d-0 integrated). Every item contains a lead decision made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Not product code. No new public code, row or detail.

## Problem

The build plan says "No crash case has been executed" (line 530), and M2 completes only when the actual matrix passes. The accepted laws each prove their own steps in-process and leave process-level execution to X9:
- X3d item 10: "X9 runs F00–F53 in fresh processes with crash barriers. X3d supplies named, test-only crash points before and after each durability step";
- X6 r2 items 10 and 11: F49's real concurrent processes, and "real crash and concurrency runs in fresh processes belong to X9";
- X4T r9 item 7: a whole-file `state.v1` restore is "a stated limit … X9's matrix records it as a stated limit and does not test it as a refusal".

At `f1b8321` the product has the following, and nothing more:
- **In-process crash and fault hooks, all `cfg(test)`.** These are:
  - X3b-2's `AppendStep` and `Fault { Crash, Fail }` hook on `JournalAppendLock` (`security/src/journal_store/carrier_append.rs` lines 273–366);
  - X3c-2's `ObjectStep` crash points with `simulate_crash`, and `PreparedLedgerCommit::with_commit_hook` (`storage/src/ledger_store/project_commit.rs` lines 130–316 and 548–580);
  - the gate and session step scripts in `custody/installation_admission.rs` and `installation_session.rs`.

  They write the state a death would leave and then return. They cannot model a real death: no destructor skipped, no flock released by the kernel, no SQLite rollback on reopen, no fresh process reading the bytes.
- **The platform's durable primitives.** `PublicationOps` in `platform/src/filesystem.rs` lines 945–1033 (`write`, `sync_file` by `F_FULLFSYNC`, `renameat`, `sync_directory` with the `F_FULLFSYNC`-then-`fsync` fallback), `replace_with`'s stages (`PublicationStage`: `Prepare`, `WriteTemporary`, `SyncTemporary`, `Rename`, `SyncDirectory`), and `publish_new_regular`. There are also the accounted forms that the witness and floor file protocol uses (`security/src/journal_store/carrier_floor.rs` `publish_private_file`, line 280: `create_private_regular_file`, `write_new_regular_accounted`, `rename_replace_accounted`, `confirm_directory_barrier_accounted`, reopen), and the non-blocking `FileLock` (`platform/src/locks.rs`).
- **A fresh-process precedent.** `journal_store.rs` line 1289 re-executes the test binary (`current_exe()`, `--exact`, an environment marker) so that a process-global mutation stays out of the workspace test process.
- **No integration test in storage or host.** `crates/storage/tests/` does not exist, and `crates/host/tests/` holds only fixtures. No crate declares a Cargo feature.

**A structural fact decides most of this law.** `cfg(test)` is set only for the crate under test. An integration target such as `crates/storage/tests/commit_tests.rs` links the libraries as non-test builds, so none of the `cfg(test)` hooks or fixtures above exist for it. These include X4T-0's signed store, the injected InitialCore image and the synthetic V2 profiles, without which this BASELINE-ATTESTED host refuses at F0 and at `/`. The same is true of storage's or host's unit tests reaching security's fixtures. "`cfg(test)` hooks only" therefore cannot cross a process, and it cannot cross a crate either.

## Decisions

1. **The injection mechanism: named barrier points compiled only into a test feature, in a re-executed child process that the parent kills while it is held at the point (lead decision).**
   - **The feature.** Each of `opensip-platform`, `opensip-security`, `opensip-storage` and `opensip-host` declares one Cargo feature, `crash-matrix`, that forwards to its internal dependencies' features of the same name. It is never default.
   - **The barrier module.** `opensip_platform::crash_barrier` exists only under the feature. It holds the point registry, the arming parser, the rendezvous protocol (item 2) and the parent-side driver (item 3).
   - **The macro.** Every point is written `crash_barrier!(scope, step, kind)`. Without the feature the macro expands to nothing: no call, no string, no branch.
   - **Platform points.** Inside the platform primitives the point is the primitive's own step: `create`, `write`, `file-barrier`, `rename`, `link`, `directory-barrier`, `reopen-confirm`, `lock`, `unlock`.
   - **Protocol scopes and protocol points.** The protocol that calls a primitive names a scope around the call with `crash_scope!`, which is thread-local and also compiled only under the feature, so a platform point reports its full name, for example `x3b.append.seal.witness-pending/rename.after`. SQLite steps (`begin`, `insert`, each `stage-<table>`, `commit`) and the protocol's own decision points are written at the protocol site, because the platform does not own SQLite.
   - **Grammar.** The full name is `<scope>[/<primitive-step>].<before|after>`. A point's occurrence `#k` (1-based) counts per full name within one process.
   - **Rejected:**
     - **`cfg(test)` hooks only.** They cannot reach an integration target or another crate, and they cannot produce a real death (see Problem). They remain the in-process unit-test seam. X9 does not remove or rename them.
     - **A separate child harness binary** (`[[bin]]` or `src/bin`). It would be a new binary target linking the feature, with its own inventory row and a shipping risk, and it duplicates libtest's selection. The re-executed test binary already has a precedent (journal_store.rs line 1289).
     - **`fork` without `exec` from the test process.** The libtest process is multi-threaded, so a forked child may inherit held locks and allocator state. It is also not a fresh process.
     - **An external debugger or `dtrace` breakpoint.** It is outside the pinned closure, its symbol names are not stable, and it is not deterministic.
     - **A custom SQLite VFS** that rendezvouses inside `xSync`. It is new `unsafe` code under the carrier, and it would change the very durability path under test (limit L2).

2. **Barrier points never exist in a release build (lead decision).** Four independent guards:
   1. **Compile guard.** Each crate that declares the feature carries `#[cfg(all(feature = "crash-matrix", not(debug_assertions)))] compile_error!(…)`. A release-profile build with the feature fails to compile.
   2. **No manifest enables it.** No `[dependencies]`, `[dev-dependencies]` or `[build-dependencies]` entry in any manifest names `crash-matrix`. The two matrix targets declare it as `[[test]] … required-features = ["crash-matrix"]`, so a plain `cargo test --workspace` skips them and builds no feature. The feature is reached only by an explicit `--features crash-matrix` on the matrix lane's command line. A source pin in X9-0 reads every `Cargo.toml` and confirms this.
   3. **The edge checker stays unchanged.** No self or reversed dev edge is added, so `check_package_edges.py`, which reads dev edges against the inventory policy, needs no exception.
   4. **Release-absence evidence (item 7).** Each matrix record builds `opensip-cli` in release with no features, and confirms that the binary contains neither the string `OPENSIP_X9_` nor any registered scope name. It also confirms that `cargo build --release -p opensip-storage --features crash-matrix` fails at the compile guard.

   **Unarmed behaviour.** With the feature built but no `OPENSIP_X9_ARMS` in the environment, every point is a read of a process-wide `OnceLock` followed by a return. No protocol's behaviour or order changes.

   **Rejected:** points compiled into every build and armed by an environment variable at run time. That is a release-build fault-injection surface, which every accepted law's forbidden substitutes exclude ("no production seam").

3. **The process protocol and how the parent verifies the death point, without sleeps (lead decision).**
   - **The child.** The child is the same test binary, run as `current_exe() --exact <child entry> --nocapture --test-threads=1`.
     - **Environment.** The environment is cleared and then given only: `OPENSIP_X9_CHILD` (the driver name: `commit`, `recover`, `sweep`, `competitor-writer`, `reader`, and (r2) `fixture`), `OPENSIP_X9_CLOCK` (r2; the scripted clock below), `OPENSIP_X9_INPUT` (the path of a driver input file under the run's scratch root), `OPENSIP_X9_ARMS`, and `TMPDIR` set to the run's scratch parent.
     - **The entry.** The child entry is an ordinary `#[test]` that returns at once unless `OPENSIP_X9_CHILD` is set. So it passes trivially in the parent's own run.
   - **The scripted wall clock (r2; lead decision).**
     - **What it replaces.** Under the feature only, and only when `OPENSIP_X9_CLOCK` is set, `opensip_platform::observe_clock` takes its wall reading from the script instead of the OS. The monotonic readings and the boot identity stay native, so every product bound measured on the monotonic clock (the 468 fence wait, S7's backoff, X4's freshness and observer bounds, item 11's timing guard) is unchanged. Without the variable, or without the feature, the wall reading is the OS's, as in production.
     - **The script.** `OPENSIP_X9_CLOCK=<E>:<k>`. E is the run set's epoch, a whole second fixed in `required-runs.v1.json` (`clockEpoch`) and inside every synthetic validity window of item 6's fixture. k is the process's ordinal in the run: the parent numbers its children 0, 1, 2, … in spawn order, and the fixture child (below) is 0. The n-th wall reading in the process (n from 0) is `E + 3600·k + n` seconds with zero nanoseconds. Readings are strictly increasing within a process and from one ordinal to the next. A process that would take a 3600th reading is a `HARNESS-ERROR`.
     - **Why it settles the dependence.** A fenced first read in a later process of the run always sees a wall second strictly later than any floor an earlier process wrote, so it publishes whenever X4T's rule allows, and identically in every repetition. Whether a read publishes no longer depends on when the process happened to run. Two concurrent children (contention, revocation) have distinct ordinals, so their readings never coincide, and the script fixes which one is later.
     - **The fixture child.** Item 6's synthetic installation, signed store and helpers are built by a child with driver `fixture` and ordinal 0, under the script, so that no stored floor or trust time comes from the OS clock. The parent's own process takes no wall reading during a run.
     - **Labels.** Every run carries `scripted-clock` beside `synthetic`. The record's `children` entries carry their ordinal.
     - **Rejected: comparing the trust store per publisher run.** It would leave the census and the kill set dependent on wall-clock timing: a run in which a fenced read happened within F's second would reach no `x4t.floor-publication` point, so the X4T floor kills of F00 could be reached only by waiting for the next second, which item 3 forbids. It would also take the trust store out of item 7's repetition agreement and so hide any real nondeterminism in trust publication.
     - **Rejected: freezing the wall clock** at one value. Every fenced read after the first would publish nothing, which is not a state production reaches, and an expiry could never pass.
   - **Channels.** The channels are the child's standard streams, created by `Command` as pipes. No descriptor passing and no `unsafe` is needed.
     - **stderr (report).** It carries tagged records `X9|<pid>|<thread>|<n>|<full name>#<k>|<event>|<payload>`, each one `write(2)` of at most 512 bytes (`PIPE_BUF` on macOS), so it is atomic. Untagged stderr is kept as diagnostics.
     - **stdin (control).** The parent writes `resume\n` on it.
   - **Arming.** `OPENSIP_X9_ARMS` is a comma-separated list of `<full name>#<k|*>=<action>`.
   - **The actions** (item 4 says which kinds of point admit which action):
     - **`hold`.** The thread writes a `held` record and then blocks in `read(2)` on stdin. It executes no product code between the write and the read. The parent then either kills the child (a crash) or writes `resume` (a pause: contention, revocation, a stalled step).
     - **`fail-before` and `fail-after`.** The primitive returns its own native error class without performing the effect, or after performing it (item 4).
     - **`torn`.** A `write` step writes the first half of the bytes, then holds.
     - **`inject-id:<exec1_…>`.** At `x3d.session.execution-draw` only, the draw returns the given ExecutionId (F34).
   - **Unarmed points.** Every reached point writes a `pass` record, so the parent holds the complete ordered trace.
   - **The kill.** On reading the armed point's `held` record, the parent sends `SIGKILL` (`Child::kill`), then `wait`s and reads stderr to EOF. The run counts as a death at that point only if all of the following hold:
     - `ExitStatusExt::signal()` is `Some(SIGKILL)`;
     - the last record from the holding thread is that `held` record;
     - no record from any thread names a durability point after it. Another thread may only report read-only points, and the observer is gated (item 5).

     A child that reaches EOF without reporting the armed point is a `HARNESS-ERROR` ("armed point not reached"), never a pass.
   - **No sleeps.** Every synchronization is a blocking read of a record the other side has written.
     - The one timed wait in the harness is a per-run watchdog of 300 s. Its only effect is to kill every child and record `HARNESS-ERROR`. It never decides an outcome.
     - A source pin over `crash_barrier`, the support module and both matrix targets admits no `sleep`, no polling loop and no other timed wait.
   - **Product waits.** The product's own bounded waits (the 468 fence's wait, S7's backoff) run as in production. Their outcome against a held peer is fixed, because the peer never releases.
   - **Rejected:**
     - **The child killing itself at the point.** It would need a second mechanism for pauses. With one parent-decided mechanism, a crash, a contention and a revocation are the same `hold`.
     - **A parent that kills after a delay.** That is the sleep-and-hope that line 1072 forbids.

4. **Point kinds and the faults that stand in for what cannot be triggered natively (lead decision).** Every point declares one kind in its macro. An armed action that the point's kind does not admit is a `HARNESS-ERROR` in the child.
   - **`step`.** Admits only `hold`. This is the default for every point.
   - **`fallible`.** Admits `hold`, `fail-before` and `fail-after`. Each `fail` returns the same failure the matching `cfg(test)` `Fault::Fail` documents (carrier_append.rs lines 294–300):
     - at an SQLite `commit`: `fail-before` is a `COMMIT` that does not land and reports failure; `fail-after` is a `COMMIT` that landed and reports failure. This is F09, F12 and F40;
     - at `file-barrier`, `rename` and `directory-barrier`: the native I/O error class of that step.
   - **`write`.** Admits `hold` and `torn`.
   - **`gate`.** A point that guards a product timed wait. In M2 the only one is X4a's observer period. Armed, its rendezvous replaces the timed wait, so a tick happens exactly when the parent resumes it. Unarmed, the product's 5 s period is unchanged.
   - **`draw`.** Admits `hold` and `inject-id`. Only `x3d.session.execution-draw` has this kind.

   **Labels.** A run whose death is a real `SIGKILL` is labelled `process-death`. A run that uses `fail-*`, `torn` or `inject-id` is labelled `injected`. A parent-side change to stored bytes between processes is labelled `mutation`. Every run also carries `synthetic` (item 6). A label is never dropped from a run's record.

   **Rejected:** injecting faults by `LD_PRELOAD`-style interposition, which is outside the pinned closure and is refused by hardened runtime.

5. **The points the matrix needs, and who places them.**
   - **The census.** The required points are not a hand list. X9-0 runs a lawful commit, recovery and sweep with nothing armed, and records every point reached: the census trace. The kill matrix is then every durability point in the census, at `#1` and, for repeated protocols (objects, appends), at the first, a middle and the last occurrence.
     - A durability primitive reached outside any scope is a `HARNESS-ERROR`, so no unnamed step can hide.
     - A census point that a later product change removes, or a new unarmed durability point, fails the coverage check (item 7).
     - (r2) The census runs under item 3's scripted clock, so its points, including each `x4t.floor-publication` occurrence, are a function of the script and the product only. Two census runs on one commit must be equal point for point; a difference is a `HARNESS-ERROR`, never a smaller kill set.
   - **The scopes, by owner:**

     | Scope | Owner law | Steps |
     |---|---|---|
     | `x4t.floor-publication` | X4T r9 item 7 (X4T-b) | the file protocol |
     | `x3b.floor`, `x3b.end.floor` | X3b items 3, 4 and 4a | the file protocol |
     | `x3b.init` | X3b item 3a | `create`, `ddl.commit`, barriers, then `x3b.init.witness` |
     | `x3b.start.witness` | X3b item 4 | REVERT, ADVANCE, INIT and OPEN witness writes |
     | `x3b.append.<seal\|rev\|cln\|terminal>` | X3b item 5 | `begin`, `level-four`, `witness-pending/…`, `insert`, `commit` (`fallible`), `witness-committed/…`, `release-level-four`, `release-level-three` |
     | `x3b.rollover` | X3b item 13 | `exclusive`, the `terminal` append, `open.witness` |
     | `x3c.ledger-create` | X3c item 2 | `create`, `wal`, `ddl.commit`, barriers |
     | `x3c.attempt` | X3c item 3 | `begin`, `insert`, `commit` (`fallible`) |
     | `x3c.object` | X3c item 4 | `create`, `write` (`write`), `file-barrier`, `link`, `directory-barrier` |
     | `x3c.evidence` | X3c items 5 and 6 | `begin`, `stage-<table>`, `commit` (`fallible`) |
     | `x3d.session` | X3d items 2 and 3 | `execution-draw` (`draw`; its `pass` record carries the ExecutionId), `settlement-reserved` |
     | `x3d.publish` | X3d item 4 | `after-staging`, `before-final-checkpoint`, `commit-returned`, `published` |
     | `x3d.finish` | X3d item 7 | `settle`, `lease-release`, `end-step` |
     | `x4.checkpoint` | X4 item 3 | `before-observation`, `after-observation`, `before-admit` |
     | `x4.gate` | X4 item 7 | `admit.after`, `latch.after` |
     | `x4.observer` | X4 item 5 | `tick` (`gate`), `after-observation` |
     | `x2.fence`, `x2.lease` | X2 item 7 | `lock` and `unlock` of the fence, `writer.lease` and `readers.lease` |
     | `x6.recover` | X6 r2 items 3 and 4 | `after-lease`, `after-ledger-snapshot`, after each of `W1 H1 J W2 H2`, `after-fresh-capture` |
     | `x6.sweep` | X6 r2 item 7 | `after-exclusive`, `after-snapshot`, `settle.commit` (`fallible`) |
     | `x7.delivery` | X7 r3 items 3 and 4 | `required` and `optional` (`fallible`: a renderer or optional-effect failure) |

     The scope names are fixed by this law. The step lists are fixed by the census.
   - **Who places them.**
     - **Units integrated before X9-0** (X3b-1/2/4, X3c-1/2, X2d, and X4T-b if it lands first): their points are placed by X9-1.
     - **Units built after X9-0** (X3d-1, X3d-2, X4a, X2e, X6a/b/c, X7a/b): each places its own points as part of its unit. X3d item 10 already requires this of X3d. For X4a, X6 and X7 it is a new requirement, recorded under "Cross-law corrections".
     - **Existing `cfg(test)` hooks stay.** Where one already exists (`AppendStep`, `ObjectStep`, the commit hook), the point sits at the same place, and its name matches the hook's variant.

6. **The synthetic test-support surface (lead decision).** Under the feature only, each of security, storage and host exposes one `#[doc(hidden)] pub mod crash_matrix_support`.
   - **What it exposes.** Producers of *inputs on disk* under a scratch root, never an authority type (r4: except the three driver entries below):
     - a synthetic installation through the real creator path, with InitialCore's injected loaded image and the synthetic V2 profile set;
     - X4T-0's signed accepted store, built from the public test-only quorum seeds;
     - a revocation or policy publication helper that replaces `state.v1` atomically under the installation fence, as the trust owner does;
     - the inherited format-1 and format-2 carrier fixture;
     - X3b-2's reserved-slot technique: lift `gj3_append_laws`, write, reinstall the trigger SQL byte-identically;
     - a synthetic run candidate for the evaluator's public `replay_run`. **r5:** X9-2 adds it, in storage's module, as inputs only (see the r5 header). **r7 (record):** X3d-3 adds it instead, binding the session's core evaluator closure (see the r7 header).
   - **What comes from production code.** `PlatformReceipt`, `ProjectOperation`, `CommitSession`, `ReplayedRun`, `PreparedCommit`, `PublishedCommit` and `RecoveredCommit` all come from the production paths over those inputs.
   - **Substitutions inside production types.** Where a production type needs its existing test-only variant to accept the synthetic input (for example `trust/initial_core.rs`'s `Image::Injected`), that `cfg(test)` becomes `cfg(any(test, feature = "crash-matrix"))`. X9-1 pins the exact list of such sites with a source pin, and no other site may use the feature.
     **r3 (record):** sites shared with X8's `scenario` are written `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`. There is one list and one pin, extended by name by X8b (X8 r3 item 4b; see the r3 header).
   - **Every record says so.** Each run records `"fixture": "synthetic-signed-v2"` and `"profileStanding": "BASELINE-ATTESTED"`, and (r2) `"clock": {"epoch": E, "script": "x9-ordinal-3600"}`. This is line 886's "synthetic fixtures remain labelled, not compiler qualification".
   - **Rejected:**
     - **Running against a real installation.** On this host the real path refuses at InitialCore F0 and at `/` without owner signing keys (EXIT-PLAN, "Owner actions").
     - **Running X9 inside security's unit-test binary.** Storage's `commit.rs` and host's finalization are unreachable from it, because security depends on neither.
     - **A support module that mints authority types directly.** That is a production-shaped seam even under a feature, and it would test the fixture instead of the composition.
   - **The three driver entries (r4; lead decision).** Security's `crash_matrix_support` exposes exactly three driver entries. Storage's and host's modules forward them unchanged, as they forward the rest of the surface:
     - `operation(at, root) -> Result<ProjectOperation, InstallationTermination>`. Over the synthetic installation `at` and the project root `root`, it runs the crate-private composition that X9-1's census already drives:
       - X1's ordinary writer admission, through `ordinary_writer::admit_with` with the write receipt over a signed test tree and the gate over `HomeSource::Fixture`;
       - X2's root admission and tracking, and the first registration when the root is unregistered;
       - `begin_operation` with APPEND-WRITE, which covers X2d's lease, X3a's endpoint, X4's monitor and first read, X3b's floor step and carrier start, and X2e's handoff.

       It returns the `ProjectOperation` that `begin_operation` returns, and nothing else.
     - `recovery_admission(at, request) -> Result<RecoveryAdmission, RecoveryRefusal>`. It produces a read receipt over a signed test tree for `at`'s H, allocates recovery's ledger as `admit` does, and runs `recovery_admission::admit_on` with `HomeSource::Fixture`. It returns that function's admission, and nothing else.
     - `settlement_sweep(at) -> Result<SettlementSweep, InstallationTermination>`. It runs X1's ordinary writer admission as `operation` does, then `settlement_sweep::admit_on`. It returns that function's sweep, and nothing else.

     **What every entry must satisfy:**
     - **Placement.** It sits inside the pinned support module, so it adds no cfg site. It calls only existing items. The fixture gates it reaches are the existing joint-predicate sites of X9-1's list: `HomeSource::Fixture`, `DurableWriteGate::for_tests`, `InitialInstallationAttempt::for_tests`, the synthetic V2 profile set and `Image::Injected`. It adds no site and no home override on any production entry. A crate-private item it calls may be widened within security, at most to `pub(crate)`, and never to `pub`.
     - **Release absence.** It is compiled only under `crash-matrix`, inside `cfg(all(feature = "crash-matrix", target_os = "macos"))`. It is never compiled under `scenario-fixtures` alone, and it is absent from every release build (item 2).
     - **Inputs.** Its inputs are item 6's on-disk inputs (`SyntheticInstallation`, a root path) and the public inert `RecoveryRequest`. It accepts no receipt, gate, guard, monitor, clock, session, permit or `ReplayedRun` from the caller. It constructs no authority type itself. It returns the production composition's own result, or that composition's refusal.
     - **One entry per process.** In line with X1 items 1 and 7, a process makes at most one call to any of the three. A second call refuses with the invariant row, without effect. The flag that enforces this is the support module's own. `publish_revocation` refuses, without writing, in a process that has made such a call: under item 11 the parent publishes, never a child that holds an operation.
     - **No other entry.** The three are the whole exception. Every other item of the surface still returns no authority type.

     **The production constructors stay the only ones** (X6 r4, record only): `RecoveryAdmission::admit` and `SettlementSweep::admit`. The three entries are test-only.
     **Rejected:** see the r4 header (a callback-style function, a home override on production entries, and waiting for X8b).

7. **The evidence shape (lead decision).**
   - **One record per run.** Each run writes `runs/<case>-<variant>.json`: canonical JSON through `opensip_identity::canonical_bytes`, sorted keys, no floats.

     ```
     { "schema": "opensip.x9.run.v1",
       "case": "F07", "variant": "kill-witness-pending-rename-after", "units": ["X3b"],
       "labels": ["process-death", "synthetic"],
       "product": { "commit": "<40 hex>", "worktreeClean": true, "toolchain": "<rustc -vV>",
                    "profile": "dev", "features": ["crash-matrix"] },
       "host": { "os": "<sw_vers>", "arch": "arm64", "filesystem": "apfs",
                 "profileStanding": "BASELINE-ATTESTED", "fixture": "synthetic-signed-v2" },
       "script": [ { "await": "x3b.append.seal.witness-pending/rename.after#1", "then": "kill" } ],
       "children": [ { "role": "commit", "exit": { "signal": 9 } | { "code": 0 },
                       "lastHeld": "<full name>#<k>" | null,
                       "trace": { "records": 41, "sha256": "<hex64>" },
                       "outcome": <the child's returned outcome or termination row> | null } ],
       "postState": { "raw": [ { "path": "<relative>", "bytes": n, "sha256": "<hex64>" } ],
                      "logical": { "ledger": {…}, "carrier": {…}, "witness": {…}, "floor": {…},
                                   "objects": [...], "trustState": "<sha256>" },
                      "normalizedSha256": "<hex64>" },
       "ladder": [ { "step": "R1-recover", "standing": "unknown-attempt-open", "stateUnchanged": true },
                   { "step": "R2-next-writer", "witnessAction": "REVERT", "outcome": "Committed" },
                   { "step": "R3-sweep", "wrote": "refused" },
                   { "step": "R4-recover", "standing": "terminal-not-committed" } ],
       "expected": { …this law's row, transcribed in required-runs… },
       "verdict": "PASS" | "FAIL" | "HARNESS-ERROR" }
     ```
   - **The post-state.**
     - **Capture.** It is captured after the last child of the scripted phase has exited and before the ladder starts. It is captured again after each ladder step, so that R1's `stateUnchanged` (recovery is read-only) is a comparison, not a claim.
     - **`raw`** is every file under the scratch installation by digest. That is line 1072's "actual state bytes".
     - **`logical`** dumps the SQLite tables row by row through a read-only connection, and decodes the witness, floor and object sets.
     - **`normalizedSha256`** hashes `logical` after replacing every drawn value (ExecutionId, `op-` token, staging nonce, wall-clock datum) by a placeholder numbered in order of first appearance. (r2) Under the scripted clock a wall-clock datum is already identical between repetitions; it is still replaced, so the comparison does not depend on the script's values. Raw digests differ between repetitions; the normalized digest must not.
   - **Where it lives.**
     - **In the product.** Runs write under `target/opensip-x9/<runSetId>/`, which git ignores. That directory holds `runs/`, `matrix.json` and, for a failed run only, a tarball of the raw scratch tree.
     - **`matrix.json`** lists the run files with their sha256, the census, the release-absence result (item 2), and the repetition comparison.
     - **In arch.** X9-6 commits the final run set to `docs/implementation/m2/crash-matrix-x9/evidence/<product commit>/` (`matrix.json` and `runs/`, without the tarballs).
   - **The checker.** It is `tools/check_crash_matrix.py` in the product: read-only, standard library only, under the pinned Python. It refuses unless all of these hold:
     - every `(case, variant)` in the reviewed `required-runs.v1.json` (item 9) has exactly one run, and no extra run exists;
     - every verdict is `PASS`;
     - the labels equal the required labels;
     - `product.commit` is the reviewed commit, and the worktree is clean;
     - the census and the kill set agree (item 5);
     - the release absence passes;
     - the two lead repetitions agree run by run on `normalizedSha256` and on the trace digest, the trust store (`logical.trustState`) included (r2);
     - (r2) every run's labels include `scripted-clock`, and every child's ordinal follows spawn order.
   - **The per-unit check (r4; lead decision).** Before X9-6, each of X9-2 to X9-5 checks its own run sets with a subset mode of the checker.
     - **Who adds it.** X9-2 adds it to `tools/check_crash_matrix.py` as the `check-unit` command, with its tests.
     - **The unit's rows.** `check-unit` names the unit (X9-2, X9-3, X9-4 or X9-5). It takes that unit's subset of the reviewed `required-runs.v1.json`: the rows whose case is in the unit's list in item 12.
     - **What it checks** on two lead run sets. It refuses unless all of these hold:
       - every subset row has exactly one run in each set, and no other run exists;
       - `check`'s per-run check passes on each run (canonical JSON, schema, verdict PASS, labels, units, script and expected equal to the row, the clock and ordinals, and kill verification by signal 9 and `lastHeld`). The one difference: `product.commit` must equal the stated base commit, and `worktreeClean` may be `false`, because a unit is reviewed uncommitted;
       - the census names only registered scopes, with their durability;
       - the kill set equals the one derived from the census;
       - every killed point of the unit's runs is in the kill set;
       - the release absence passes;
       - the limits are exactly L1 to L10;
       - the two sets agree run by run on `normalizedSha256`, the trust store included, and on every child's trace digest, and they agree on the census.

       It does not require the full kill-set coverage.
     - **What binds the reviewed bytes.** The unit's review subject manifest binds them. The run records do not.
     - **It is not a matrix pass.** The forbidden substitute "a matrix pass on a dirty worktree" still governs X9-6's `check`, which stays unchanged.
     - **Rejected:** see the r4 header.
   - **How the review checks it.** The reviewer owns the native lane for X9-6, and:
     1. reruns the whole matrix on the reviewed commit;
     2. runs the checker over both run sets;
     3. compares its normalized digests and traces with the lead's.

     Agreement across the three executions is the determinism evidence.
   - **Rejected:**
     - **Committing raw state bytes to arch.** A run set would be hundreds of megabytes of SQLite and trust files whose bytes carry random nonces. Digests plus logical dumps carry the same evidence, and failures keep their tarball.
     - **A pass/fail log without state.** Line 1072 requires the actual state and the exact outcomes.

8. **The recovery ladder.** Every run that leaves an attempt behind is followed by four steps, each in a fresh process:
   - **R1:** `recover(executionId)` (X6, `SHARED-READ`, no fence). It must leave `normalizedSha256` unchanged. (r2) It is its own process and read entry, with a plain `RecoveryRequest` naming the run's namespace (X6 r3 item 2).
   - **R2:** a next writer that runs a full lawful commit on the same namespace. It records the floor step's decision and the start's witness action (OK, REVERT, ADVANCE, INIT or OPEN), then its outcome.
   - **R3:** the settlement sweep (X6c, `EXCLUSIVE` under the fence). It records what it wrote, or that it wrote nothing.
   - **R4:** `recover(executionId)` again.

   **Exceptions.**
   - **Mutation rows** run R1 and R2 only, because the injected condition persists.
   - **Runs without an ExecutionId** skip R1 and R4 and record `"notApplicable": "no-execution-id"`. The ExecutionId comes from the `x3d.session.execution-draw` pass record.
   - **Every lawful run** also asserts the release order line 608 requires, from its trace: level 4, then each level-3 transaction, then the lease, then the fence.

   Abbreviations in item 9: CH committed-historically, CAD committed-availability-degraded, TNC terminal-not-committed, UAO unknown-attempt-open, UAU unknown-attempt-unobserved, UC unknown-custody, UQ unknown-quarantine-condition, UB unavailable-busy, BU binding-unusable, UCI unknown-carrier-incompatible.

9. **The matrix.** Every row runs on this macOS 27 host under item 6's synthetic fixture.
   - **Status values.** "exec" means executed here. "exec (inj)" means executed with an injected stand-in (item 4). "exec (mut)" means executed over a parent mutation. "elsewhere" means it is covered by an accepted law's in-process test and is not a process-level case. "LIMIT" means recorded and not executed (item 10).
   - **Expected values.** They come from the build plan's row and the owning law. X9-a units transcribe each row into `required-runs.v1.json` before any run. An expected value is never read back from a run.

   | Case | Owner | Injection | Status | Expected |
   |---|---|---|---|---|
   | F00 | X2, X3a, X3b, X4T-b | `hold`→kill at every census point before `x3c.attempt.commit.after` (X4T floor, X3b floor, INIT, start witness, leases) | exec | No attempt row; ledger logical state unchanged. R2: the floor step and start handle X3b item 3a's or item 4's crash state (INIT resumes or finishes, REVERT, ADVANCE), then Committed. With an ExecutionId drawn: R1 and R4 UAU, R3 writes nothing. **r5:** expected by kill point: before the draw, R1 and R4 not applicable; from the draw through `x3c.ledger-create.ddl.commit.before`, R1 UC (`ledger-missing` or `ledger-unreadable`, X6 F24) and R4 UAU; from `x3c.ledger-create.ddl.commit.after` (included, r6) until `x3c.attempt.commit.after`, R1 and R4 UAU. R3 writes nothing (see the r5 header). **r8:** R2 is the owning law's outcome for the crash state at the kill point: the registration window (X2 item 8 identity rows), the created-not-yet-private windows (custody, host I/O, or Committed or `INSTALLATION.INCOMPLETE` for an empty trust dependency), the WAL gap (`LEDGER.CORRUPT`), and Committed everywhere else. R4 stays UC where R2 does not create the ledger (see the r8 header; L11). |
   | F01 | X5 | replay-invalid candidate; substituted target or inventory | exec (host) | Refused before `prepare_commit`; no attempt row; no SEAL; ledger and carrier logical state unchanged. |
   | F02 | X3c | `torn` at `x3c.object.write` (first, middle and last object) | exec (inj) | Staging residue is never adopted. R1 UAO; R2 Committed; R3 refused; R4 TNC. The orphan stays (L6). |
   | F03 | X3c | kill at `file-barrier.before` and `.after` | exec (death branch; L1) | As F02. |
   | F04 | X3c | kill at `link.before` and `.after`; R2 republishes the same digest | exec | As F02. R2 confirms the existing object by exact bytes. An unequal-collision mutation variant refuses on X3c item 10's row. |
   | F05 | X3c | kill at `directory-barrier.before` and `.after` | exec (death branch; L1) | As F02. |
   | F06 | X3b, X3c, X3d | the parent holds a raw SQLite `BEGIN IMMEDIATE` on the carrier, or on the ledger, while the child runs `publish` (labelled `mutation`: a foreign holder) | exec (mut) | Busy row (`LEDGER.BUSY_TIMEOUT`/`PROJECT.BUSY`); an earlier level-3 transaction is released; no SEAL; orphans preserved. R1 UAO; R2 Committed after the holder ends; R3 refused; R4 TNC. |
   | F07 | X3b | kill at each `x3b.append.seal.witness-pending/*` point and at `insert.before` | exec | R1 UAO, diagnosis would-REVERT; R2 REVERT, Committed; R3 refused; R4 TNC. **r5:** R1 is plain UAO; would-REVERT is R2's witness action only (see the r5 header). **r8:** R2's witness action is OK before `witness-pending/rename.after` and REVERT from it on (see the r8 header). |
   | F08 | X3b | kill at `insert.after` and `commit.before` | exec | SQLite rolls back on reopen. As F07. |
   | F09 | X3b | kill at `commit.after`; `fail-after` and `fail-before` at the SEAL `commit` | exec; exec (inj) | Injected: `CommitUndetermined` (`DURABILITY.COMMIT_FAILED`); nothing appended; no evidence `COMMIT`; the settlement reserve is forfeited. R1 UAO with would-ADVANCE (landed) or would-REVERT (not landed); R2 ADVANCE or REVERT, Committed; R3 refused; R4 TNC. **r5:** R1 is plain UAO; landed or not landed shows only as R2's ADVANCE or REVERT (see the r5 header). |
   | F10 | X3b | kill at each `witness-committed/*` point | exec | R1 UAO, would-ADVANCE before the rename survives, OK after; R2 ADVANCE or OK; R3 refused; R4 TNC. **r5:** R1 is plain UAO; would-ADVANCE or OK is R2's witness action only (see the r5 header). |
   | F11 | X3c, X3d | kill after each `x3c.evidence.stage-<table>` | exec | The ledger transaction rolls back; the SEAL is durable with no `REV` (the process died before `finish`). R1 UAO; R2 Committed; R3 refused; R4 TNC. |
   | F12 | X3c, X3d, X7 | `fail-after` and `fail-before` at `x3c.evidence.commit` | exec (inj) | `CommitUndetermined` with ExecutionId and no RunId; no retry; nothing appended. R1 CH with pendingSettlement (landed) or UAO; R3 committed or refused; R4 CH or TNC. |
   | F13 | X3c, X3d | kill at `x3d.publish.commit-returned` | exec | R1 CH with pendingSettlement; R2 Committed; R3 committed; R4 CH. |
   | F14 | X3d, X6 | kill at `x3d.publish.published` and at `x3d.finish.settle.before` | exec | As F13. |
   | F15 | X6 | kill after `x3d.finish.end-step.after` | exec | R1 CH; R2 creates no second receipt for this ExecutionId. |
   | F16 | X7 | `fail-before` at `x7.delivery.required` | exec (host, inj) | `DELIVERY.REQUIRED_FAILED`, exit 4, runId kept; R1 CH. |
   | F17 | X7 | `fail-before` at `x7.delivery.optional` | exec (host, inj; L9) | Committed; optional failure disclosed; result unchanged. |
   | F18 | X4, X3d | `hold` at `x4.checkpoint.before-observation#1`; the parent publishes a revoking update, or makes the view unreadable or mixed; resume | exec | Refused `TRUST.COMPONENT_REVOKED_DURING_OPERATION`, or `OBSERVER.FAIL_STOP`; no SEAL; `finish` appends `REV` from the settlement reserve. R1 UAO; R2 refused at admission (revoked), or Committed after the view is restored (fail-stop variant); R3 and R4 per C5. |
   | F19 | X3b, X3d, X4 | as F18 at the repeated checkpoint after the SEAL (`#2`); also kill at each point of the end-path `REV` append | exec (stall variant: L3) | Refused; evidence transaction rolled back; the trace shows level 4, then level 3, then a fresh `x3b.append.rev`, then `CLN` if owed. A killed `REV` leaves X3b's append crash state. R1 UAO; R3 and R4 per C5 (or refused and TNC in the fail-stop variant). |
   | F20 | X6, X3b | the parent rewrites the witness as malformed or with a mismatched digest | exec (mut) | R1 UQ after the five stable observations; R2 quarantine row (`LEDGER.CORRUPT`). |
   | F21 | X6, X3b | the parent deletes the witness of a nonempty journal | exec (mut) | R1 UQ (`witnesslessRestore`); R2 quarantine row. |
   | F22 | X6, X3b | the parent restores a carrier copy taken at an earlier `hold`, under a newer floor; or equal seq with a different hash | exec (mut) | R1 UQ; R2 quarantine (floor regression or `uncertainTailLoss`). |
   | F23 | X6 | the parent deletes the receipt row, or the association row | exec (mut) | R1 UC; R3 writes nothing (one-sided). |
   | F24 | X6, X3a | ledger mode `000` or a truncated header; a wrong store generation selected | exec (mut) | R1 UC; R2 refused on its X3c or X3a row; R3 reports host I/O for that namespace and writes nothing. |
   | F25 | X6 | the parent deletes, or flips one byte of, a committed object | exec (mut) | R1 CAD with `evidence.missing` or `evidence.corrupt`. |
   | F26 | X4, X6 | commit, then the parent publishes a revocation | exec | R1 CH; R2 refused at admission; no grant reused. |
   | F27 | X6 | the parent swaps the association's namespace, generation, operation or execution; or a request with a different binding | exec (mut) | R1 BU. |
   | F28 | X6 | X6a's pruned-record fixture, read in a fresh process | exec (mut) | R1 UC. |
   | F29 | X6 | a reader process while the writer holds at `x3c.attempt.commit.after`, after the SEAL, at `x3d.publish.after-staging` and at `commit-returned` | exec | UAO, UAO, UAO, CH with pendingSettlement; never mixed; the reader takes `readers.lease` alongside APPEND-WRITE without waiting. |
   | F30 | X2, X6c | writer A holds (a) under its lease after the fence is released and (b) while it holds the fence; process B is a competing writer; process C is the sweep | exec | B: the busy row after S7's bounded fence or lease attempt, no upgrade, no state change. C: skips and retains the namespace. After A resumes, A is Committed, and a second B then succeeds. |
   | F31 | X3b | the parent installs the format-1 or format-2 fixture as the namespace's carrier | exec (mut) | R2 refused before commit work (X3b item 3a's F46 row); no SEAL is inserted. |
   | F32 | X3b-4, X7b | reserved-slot setup to tails `…987` and `…988`; kill at each X3b item 13 crash-table point | exec (host; mut + death) | `CarrierCapacityExhausted`; `finish`; the rollover in the end step; X7 r3 item 6a's busy row. Each crash row as X3b item 13 states; the next writer proceeds in G+1. |
   | F33 | X6 | the parent alters receipt bytes, the inventory, a signature, or the SEAL body digest | exec (mut) | R1 UC. |
   | F34 | X3d, X6 | (r2) run A: `inject-id` with a previous run's ExecutionId; then run B, a separate `recover` process, once with A's disclosed requested binding and once with the earlier attempt's own binding | exec (inj) | A: `ExistingAttempt`, projected on the invariant row (`SYSTEM.OUTCOME.ILLEGAL_STATE`, `HOST.INVARIANT_VIOLATED`) with the ExecutionId as subject and the requested binding disclosed (X6 r3 item 6, X7 r4 item 3); no new row, no SEAL, no recover in A; the earlier attempt's rows unchanged. B: with A's binding (a different `operationRef`), BU (`RECOVERY.REFUSED`, subject `operation`); with the earlier attempt's binding, that attempt's standing. B leaves `normalizedSha256` unchanged. |
   | F35 | — | — | LIMIT (L5) | — |
   | F36 | X3b, X3c, X6 | the orphan SEALs of F09, F11, F19 and F38, followed by R2 committing the same semantic RunId | exec | The earlier ExecutionId: R1 UAO, R3 refused, R4 TNC. The later ExecutionId: CH. The RunId is not blacklisted. |
   | F37 | X6 | — | elsewhere (X6 item 10: the pure ordering accessor) | — |
   | F38 | X3d, X4 | `hold` at `x3d.publish.after-staging`; the parent revokes; resumes `x4.observer.tick#1` and awaits `x4.gate.latch.after`; resumes the main thread | exec | The gate goes 0→2; no permit; staged transaction rolled back; `REV` and `CLN` from the reserve. R1 UAO; R2 refused at admission; R3 and R4 per C5. |
   | F39 | X3d, X4, X7 | `hold` at `x4.gate.admit.after`; revoke; observer tick; latch 1→3; resume | exec (storage half; host half in X9-5) | Committed with `latchedAfterAdmission`; host projects `DELIVERY.REQUIRED_FAILED`; R1 CH. |
   | F40 | X3d, X7 | as F12, with and without F39's latch | exec (inj) | `DURABILITY.COMMIT_FAILED`, ExecutionId, no RunId; the latch does not convert it. The ladder as F12. |
   | F41 | X4, X3d | the two process-level orders: latch before admission, and admission before latch | exec (two orders); every interleaving is covered elsewhere (X4's gate-trace test) | At most one `x3c.evidence.commit` in the trace; the gate stays in 0..3. |
   | F42 | X3d | abort is every kill above; the child driver `mem::forget`s its `StoppedSession` and exits; a held point with a reader running | exec (kernel stall: L3) | Forget: the kernel releases the lease, the attempt stays admitted, R1 UAO. The reader during a hold: UB or UAO. Never a claimed cleanup. |
   | F43 | X6 | tail-lost variant: after a commit, the parent truncates the journal tail below the association's `journalSeq` (reserved-slot technique) | exec (mut); the reconciling-retry variant is elsewhere (X6 item 11's hazard test) | R1 per the F43 rule: UB attributed to the carrier owner, or the F22 condition when the floor is at or above the requested sequence and two tail observations agree; never uncommitted. |
   | F44 | X6 | attempt A runs F39's script (Committed, gate latched after admission), so its `finish` owes a `REV`; A holds at `x3b.append.rev.witness-pending/directory-barrier.after`; a reader process recovers A's ExecutionId. A's SEAL is above the floor its own floor step wrote | exec | UC, not invalidated; diagnosis witnessWouldRevert; no REVERT, ADVANCE, witness write or floor raise; no wait on A. |
   | F45 | X6 | as F44, with A holding at `x3b.append.rev.commit.after` | exec | CH under witness-pending-at-tail, with `interior-bodies-not-authenticated`; diagnosis witnessWouldAdvance; no write. |
   | F46 | X6 | the format-1 or format-2 fixture, or an association below `first_generation` | exec (mut) | R1 UCI. **r8:** the association-below-`first_generation` variant is not executed in M2 (a fresh carrier's first generation is 1; L5; see the r8 header). |
   | F47, F48, F50, F51 | — | — | LIMIT (L5) | — |
   | F49 | X6 | (a) a reader holds between bracket reads while a lawful writer appends, then resumes; (b) writer A holds at `x3c.attempt.commit.after`, a reader of A's ExecutionId holds at `x6.recover.after-ledger-snapshot`, A is resumed to Committed, then the reader resumes | exec | (a) UB, never UQ, never a corruption diagnosis; (b) UAO or UB from the one stale snapshot, never TNC. |
   | F52 | X6 | the four lawful cells from earlier runs (admitted/none, admitted/both, settled-committed/both, settled-refused/none); the other seven by mutation | exec, exec (mut) | X6's §2 matrix; exactly one cell gives TNC. |
   | F53 | X6c | live (a held writer), crashed (killed runs), one-sided (mutation), inaccessible (mode `000`), already settled (a second sweep); also kill the sweep at `x6.sweep.settle.commit.before` and `.after` | exec | X6 r2 item 7: skip, settle, or write nothing. After a killed sweep, the next sweep settles each row exactly once (the monotone trigger). |

   **C5 (revocation ladders).** After a revocation of a subject in the closure, R2 is refused at X4T's admission. Whether R3, the sweep under X1's `admit_ordinary_writer`, is admitted under that revoked view is not fixed by an accepted law (gap G5). X9-4 transcribes R3 and R4 from the law that fixes it before running. Until then, the F18, F19 and F38 ladders end at R2 and record `"ladderEnd": "G5"`. **Rejected:** choosing the expected R3 in this law, which would decide an admission question for X1 and X6.

   **r3 (record):** X6c fixed it. A revoked closure subject does not refuse the sweep. So for F18, F19 and F38, R3 settles the crashed attempt `refused`, and R4 is `terminal-not-committed`. The `"ladderEnd": "G5"` stop no longer applies (see the r3 header).

   **Why F43's lawful race is not a process case.** X6 step 1 reads the ledger before step 3 captures the carrier. The writer makes the SEAL durable before the ledger `COMMIT` (X3d item 4). So no lawful interleaving of processes gives a reader a journal capture older than its ledger snapshot. Only lost tail bytes can, and that is the mutation variant. The retry that reconciles is X6's in-process hazard test.

10. **Limits: recorded, not tested.** Each is written into `matrix.json`'s `limits`, with its reason and its later owner.
    - **L1. Power loss, kernel panic and drive-cache loss.** Process death keeps unbarriered page-cache data, so F03 and F05 exercise only the "survived" branch. The "did not survive" branch of an unbarriered step equals the durable state at the preceding point, because every protocol barriers a file before linking or renaming it. The matrix kills there too, and torn content is covered by `torn`. Media and power faults are M6 qualification (line 1072: "M2/M6").
    - **L2. SQLite's interior commit.** SQLite's commit is atomic under process death by its own contract. The matrix kills at `commit.before` and `.after` and injects `fail-*`. It does not interrupt SQLite's WAL write and sync, and it adds no VFS shim (item 1).
    - **L3. Native stalls and S6 scheduling bounds.** A kernel-level stalled syscall, the observer's 10 s freshness stall (F19's stall variant) and the residual admission window (X4 item 3) need real elapsed time or kernel control. A `hold` emulates a stalled step, not a stalled syscall. X4's scripted-clock tests cover the logic. The bound is a qualification obligation (S6, M6).
    - **L4. Whole-file `state.v1` restore (X4T r9 item 7).** A self-consistent older `state.v1` with its whole closure is admitted. No run asserts that it is refused, and no run asserts that it is admitted: a passing test of the admission would pin the limit as required behaviour, and S9.3's restore lineage, or a future anchor outside I, would then have to break it. Its later owner is S9.3 or that anchor.
    - **L5. Store and carrier migration and restore (F35, F47, F48, F50, F51).** No migration or restore writer exists in M2 (X6 r2 item 9; X3b r10 item 10). F46's read side is executed.
    - **L6. Orphan collection.** No reachability GC exists (X6 r2, "Not claimed"), so F02 to F06's "later authorized reconciliation may remove orphans" is not executed. Orphans are recorded in `postState`.
    - **L7. Measured platform profile.** This host is BASELINE-ATTESTED under 469. Every run is synthetic (item 6). A measured row needs the owner's signing keys, and it is not required for M2.
    - **L8. Host coverage.** macOS 27 on APFS on this host only. Linux, other filesystems and external volumes are not executed.
    - **L9. Native optional delivery.** M2 has no browser launch or export, so F17 runs only as an injected failure.
    - **L10. Journal pruning.** No pruning writer exists, so F28 runs only over X6a's fixture.
    - **L11 (r8). Permanently refused crash states.** An interrupted first registration (X2 item 8's identity rows), a created owner not yet sampled private (custody, host I/O or `INSTALLATION.INCOMPLETE`), and a partial ledger WAL (`LEDGER.CORRUPT`, X3c item 10) leave the project refused until a repair or resume writer exists. F00 records each outcome. The later owner is M3, a repair or resume writer.

11. **Lock contention (F30) and live revocation, deterministically.**
    - **Contention.** Writer A holds at a named point, so its lease, and optionally the fence, is held for as long as the parent wants. The parent then spawns B, C or a reader as fresh processes and reads each one's outcome. Each peer meets a holder that cannot release, so its non-blocking `LOCK_NB` attempt, or the product's bounded fence wait, has exactly one outcome. The parent then resumes A and reads A's outcome. No step depends on timing, and none sleeps.
    - **Revocation.** Every child arms `x4.observer.tick#*=hold`, so the observer ticks only when the parent resumes it.
      - **Order of the parent's steps.** The parent holds the main thread at the named checkpoint or gate point, publishes the trust change (item 6's helper, under the fence, which the held child does not hold after its handoff), and resumes either the main thread (the checkpoint's own monitored read observes it) or one observer tick, awaiting `x4.gate.latch.after` before resuming the main thread.
      - **Why it is deterministic.** Which party latches, and in which gate state, is fixed by the script.
    - **Timing guard.** A held child's awake time counts against X4's 10 s bound. Each run records the monotonic time from the operation's first monitored read to its last checkpoint. A run above 2 s is a `HARNESS-ERROR`, never an `OBSERVER.FAIL_STOP` that the run then accepts.
    - **Rejected:** letting the observer tick on its own 5 s timer during matrix runs, which makes the latching party a race.

12. **Units after the law.** Each comes with its inventory successor and is reviewed alone.
    - **X9-0 (platform; the mechanism).** It contains:
      - the `crash-matrix` feature in platform;
      - the `crash_barrier` module: registry, kinds, the arming parser, the child rendezvous and the parent driver;
      - the `crash_barrier!` and `crash_scope!` macros, the compile guard and the manifest pin;
      - points in the platform primitives (`PublicationOps`, the `replace_with` stages, `publish_new_regular`, the accounted file effects, `FileLock`);
      - `tools/check_crash_matrix.py` with the run schema.

      **Tests.** A self-test child killed at a platform point, with the kill verified; `hold` then `resume`; each `fail-*` and `torn`; an unarmed run identical to a featureless run; an armed but unreached point as `HARNESS-ERROR`; an action at a point of the wrong kind as `HARNESS-ERROR`; the watchdog; and a no-sleep source pin.

      **Dependencies.** None. It should land before X3d-1, so that later units place their own points.
    - **X9-1 (security, storage and host; the support surface and existing points).** It contains:
      - the feature in the other three crates;
      - the `crash_matrix_support` modules (item 6), and the pinned list of `cfg(any(test, feature))` sites;
      - scopes and points at the integrated sites: X3b-1, X3b-2, X3b-4 (if integrated), X3c-1, X3c-2, X2d's leases, X4T-b's floor publication;
      - the post-state capture and normalizer, and the run writer;
      - the census of the then-integrated path;
      - (r2) item 3's scripted wall clock in `observe_clock` (a feature-only platform site, under item 2's guards, listed with the crash_barrier module), the `fixture` driver, the `scripted-clock` label and the census equality check.

      **Dependencies.** X9-0. It precedes X3d-2's, X6b's and X7a's composition tests, which need the same surface (gap G1).
    - **X9-2 (storage; carrier and objects).** `crates/storage/tests/commit_tests.rs` with `required-features`, the shared drivers (`commit`, `recover`, `sweep`, `competitor-writer`, `reader`), the ladder, and rows F00, F02–F05, F07–F10, F20–F22, F31 and F46, with their `required-runs.v1.json` rows. **Dependencies:** X9-1, X2e, X4a, X3d-1, X3d-2, X6a, X6b, X6c.
      **r4:** X9-2 also adds item 6's three driver entries, which its drivers use, and item 7's `check-unit`. It does not depend on X8b.
      **r5:** X9-2 also adds item 6's synthetic run candidate, and its `commit` driver replays after `CommitSession::open` (see the r5 header). It transcribes r5's F00 split and F07 to F10's R1.
      **r7 (record):** the candidate is X3d-3's, and X9-2 depends on X3d-3 (see the r7 header).
      **r8:** X9-2 transcribes r8's F00 and F07 splits, runs F46's format variants only, and carries L11 in the checker's limit list (see the r8 header).
    - **X9-3 (storage; commit and recovery).** Rows F11–F15, F23–F25, F27–F29, F33, F36, F42, F43–F45, F49, F52 and F53. **Dependencies:** X9-2.
    - **X9-4 (storage; locks and live revocation).** Rows F06, F18, F19, F26, F30, F34, F38, F39's storage half, F40 and F41, and C5 once G5 is decided (**r3 (record):** decided by X6c; C5's R3 is `refused` and its R4 is `terminal-not-committed`). **Dependencies:** X9-2 and X4a. It uses X4a's observer `gate` point.
    - **X9-5 (host).** `crates/host/tests/commit_matrix_tests.rs` with rows F01, F16, F17, F12's and F40's caller route, F32 with its rollover crash table, F39's delivery half, and F53's `store-gc` step. **Dependencies:** X9-2, X5a, X7a, X7b, X3b-4 and X6c.
    - **X9-6 (record; the M2 exit).** Two full lead runs on one integrated commit, the checker, release absence, the reviewer's rerun, and the arch evidence record. **Dependencies:** all of the above, and VD1 (EXIT-PLAN, "lands before the X9 exit").

## Cross-law corrections found while drafting

These are recorded for the owning laws' next revisions. None changes an accepted outcome or row.
- **G1. Cross-crate `cfg(test)` fixtures do not exist.**
  - **Which laws.** X3d r6 item 12 (storage tests build a `ProjectOperation` through security's `cfg(test)` fixtures and X4T-0), X6 r2 item 11 (X3b's and X3c's fixtures and X4T-0 in storage and host tests) and X7 r3 item 10 (host integration tests with X4T-0's trust) each rely on another crate's `cfg(test)` code.
  - **Why it fails.** Rust sets `cfg(test)` only for the crate under test, so those fixtures do not exist for storage's or host's tests.
  - **The fix.** Item 6's support surface supplies them. X3d-2, X6b and X7a's integration tests depend on X9-1, and each of those laws' test items needs a one-line amendment naming it.
- **G2. The literal "`cfg(test)` only" sentences.** X3c r7 item 11 ("A fault-injection hook exists only under `cfg(test)`"), X3b r10 item 11, and X4T r9 items 12 and 13 ("the fixture is `cfg(test)`") protect one invariant: the code is absent from every non-test build. Item 2 meets that invariant by other means. Those sentences should be restated as "absent from every non-test build (`cfg(test)` or X9's `crash-matrix` feature)".
- **G3. Read-path points (X6).** F49 needs named holds between `recover`'s bracket reads (`W1 H1 J W2 H2`), and F29, F44 and F45 need `recover` to report its admission and snapshot points. X6 r2 names none. X6a and X6b place item 5's `x6.*` points.
- **G4. Observer and checkpoint points (X4).** Deterministic F18, F19, F38 and F39 need the `x4.*` points, including the observer's `gate`. X4 r7 names none. X4a places them.
- **G5. The sweep's admission under a revoked view.** X6 r2 item 7 says the sweep "takes no X4 guard", but it does not say whether X1's `admit_ordinary_writer`, which the sweep runs first, refuses when a closure subject is revoked. The expected R3 for the F18, F19 and F38 ladders depends on it (C5). It needs an X1 or X6 decision before X9-4. **r3 (record):** X6c resolved it with no new law sentence (see the r3 header).
- **G6. EXIT-PLAN.** The X9 row's "Depends on" omits X2e and X5. The order "X9 (M2 exit)" last hides that X9-0 and X9-1 must precede X3d-2's, X6b's and X7a's composition tests (G1).
- **Not a gap.** X3d item 10's promise of "named, test-only crash points before and after each durability step" is met by item 5. Its "test-only" is item 2's feature.

## Forbidden substitutes

- Any barrier point, `crash_matrix_support` item or `cfg(any(test, feature = "crash-matrix"))` site in a release build, or in a build reached without an explicit `--features crash-matrix`. **r3 (record):** this excepts the shared sites of X8 r3 item 4b reached through `scenario-fixtures`. Those are still absent from every release build (see the r3 header).
- A manifest dependency of any kind that enables `crash-matrix`.
- A sleep, a polling loop or a timeout that decides an outcome. The watchdog only ever records `HARNESS-ERROR`.
- An in-process "crash" (`catch_unwind`, an early return, a simulated state) counted as a process death in the matrix.
- A kill not verified by `SIGKILL` status and by the trace's last held record.
- An expected value read back from a run, or written after it.
- Dropping `injected`, `mutation` or `synthetic` from a run's labels, or reporting a limit row as executed.
- A support function that returns an authority type (`PlatformReceipt`, `ProjectOperation`, `CommitSession`, `ReplayedRun`, `PreparedCommit`, `PublishedCommit`, `RecoveredCommit`, `AdmissionPermit`). **r4:** this excepts item 6's three driver entries, each returning only its crate-private production composition's own result (`ProjectOperation`, `RecoveryAdmission` or `SettlementSweep`) over the fixture home.
- (r4) A fourth driver entry, or one that constructs its result itself, accepts a receipt, gate, guard, monitor, clock, session, permit or `ReplayedRun`, or is compiled under `scenario-fixtures` or in any release build.
- (r4) A support function that hands an authority type to a caller's closure.
- (r4) A home override, or any test-only input, on a production entry (`admit_ordinary_writer`, `RecoveryAdmission::admit`, `SettlementSweep::admit`).
- (r4) A second entry in one process through the three entries, or `publish_revocation` in a process that made one.
- A `cfg(any(test, feature))` site outside X9-1's pinned list.
- Asserting either refusal or admission of a whole-file `state.v1` restore (L4).
- A durability primitive reached outside a named scope during a matrix run.
- An observer that ticks on its own timer in a matrix child.
- (r2) A wall reading from the OS in any process of a matrix run, a scripted wall reading in a build or process without the feature and `OPENSIP_X9_CLOCK`, or a scripted monotonic clock.
- (r2) A `recover` call inside F34's injected writer run.
- Raw state bytes committed to arch in place of the run records.
- A matrix pass on a dirty worktree, or on a commit other than the reviewed one. **r4:** a unit's `check-unit` (item 7) is not a matrix pass.

## Not claimed

Power-loss and media qualification, native S6 scheduling bounds and the residual admission window (M6); store and carrier migration and restore; orphan object collection; a measured platform profile row; Linux and non-APFS hosts; X8's compile-fail suite; CLI enablement (X10, X11); any new public code, row or detail; closing X4T r9's whole-file restore limit.
