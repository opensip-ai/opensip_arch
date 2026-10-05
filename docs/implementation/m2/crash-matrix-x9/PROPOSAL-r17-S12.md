# The crash, lock and revocation matrix — proposal X9 r17

**r17 round 1 (the section frame and §RC) ACCEPTED 2026-10-04 by Grok** (`89fc47ff…`; `reviews/grok-crash-matrix-x9-r17-rc/`), with no required findings. Under LD-17-1, r17 is accepted section by section. These bytes, without this note, are preserved in `PROPOSAL-r17-RC.md`. §S12 and §RW stay reserved until their own rounds.

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
    - `x4.gate.admit.after` and `x4.gate.latch.after`. **r17 round 2 (X4 r8 S11.12, record):** `x4.gate.latch.after` now follows the stop transition's release, after the stop-cause lock is released, not the `fetch_or`. It is reached on the same calls in the same order, and no expected value or census changes (the r17 header, "X4 r8's record note").
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
  - **The matrix-only order.** A first registration draws the ProjectId inside the operation, so the matrix child calls `replay_run` after `CommitSession::open` and before `prepare_commit`. Replay is pure and takes no custody, so no X3d step changes. This order is stated for matrix children only. The host's order, replay before any custody (X5 r3 item 3, F01), is unchanged and stays X9-5's. **r17 (§S12):** under X5 r4 item 3, host's own order also replays after `open` and before `prepare_commit`, so the two orders now coincide (§S12.3).
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

**r8 (2026-10-02) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r7 bytes are preserved in PROPOSAL-r7.md. r9 ACCEPTED by Grok on 2026-10-02. **r9 (2026-10-02)** answers Grok's X9 r8 RF-1 and changes nothing else. r8 bytes are preserved in PROPOSAL-r8.md. The fix: an X4T dependency kill point has one R2 per census occurrence, not a two-valued class, and the row is `CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete` (X4T r9 item 10). r8 was not accepted, so r9 corrects the dependency sentence below, the F00 cell's r8 clause and L11 in place. X9-2 ran every one of its 232 transcribed rows once, in a development run on product `a2c5e8b`: 167 passed, 65 failed, and none was a harness error. Each failure was the owning law's lawful outcome for the crash state the kill left, where this law's row had expected another. r8 changes F00's and F07's R2, adds limit L11, and makes four of X9-2's choices law. Nothing else changes.

- **F00: R2 is the owning law's outcome for the crash state (item 9).**
  - **What X9-2 found.** F00's row expected R2 to reach Committed after every kill before `x3c.attempt.commit.after`. For 57 kill points, the next writer instead refuses permanently on the owning law's row:
    - **Registration.** Kills from `x2.fence.register.reserved/rename.after` through `x2.fence.register.active/rename.before` leave a RESERVED row, or partial namespace or marker owners. The next writer refuses with `PROJECT.ROOT_CUSTODY_REFUSED`, subject `identity-recovery-required` (X2 r8 item 3, "RecoveryNeeded: a matching RESERVED row", and item 8). Two points differ:
      - after `x2.fence.register.marker/create.after`, the marker exists before its private sample, and the subject is `marker-custody`;
      - at `x2.fence.register.marker/write.before`, the marker is private but empty, and the subject is `identity-contradiction`.
    - **A created owner not yet sampled private.** A kill at a creation's `create.after`, before the private sample that follows it with no point between, leaves an object that is not private:
      - `x3c.ledger-create.projects`, `x3c.ledger-create.namespace`, `x3c.object.objects`, `x3c.object.sha256` and `x3c.ledger-create` (the ledger file): `create.after` refuses on X3c's custody row (`Custody`, subject `private`). R2 never creates the ledger, so R4 stays UC.
      - `x3b.floor.directory/create.after`: the floor directory refuses on X3b's host I/O row.
      - `x4t.floor-publication.dependency`, `create.after` and `write.before` (r9): a kill at `create.after` leaves the new leaf present and empty, and one at `write.before` leaves it torn (`primitive_write` writes the first half, then holds). Both are before the pointer replacement, so the next fenced read sees the unchanged capsule and does not name the leaf (X4T r9 item 2's closed, reference-directed read set). The next publication then writes a determined list of content-addressed names, and `write_dependency` creates a name only when it is absent, admits equal bytes and refuses unequal bytes. So each census occurrence has exactly one R2:
        - **The next publication writes that name** (the empty or torn leaf can never equal its complete bytes): `CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete` (X4T r9 item 10; `TrustRow::Incomplete`).
        - **The next publication does not write that name:** Committed.

        **How the per-occurrence value is obtained (r9), before any kill run and never from a run under test.** The occurrence index is part of the point identity (`name#k`), and both publications are functions of the script and the product (item 5). The transcription makes one deterministic, unarmed reference run, under the run set's clock epoch, with two fresh synthetic installations:
        - **(A)** an unarmed commit at ordinal 1, the killed child's ordinal;
        - **(B)** an unarmed commit at ordinal 2, R2's ordinal. A kill before the draw leaves no R1, so R2 is the second child after the fixture.

        In (A), the entries the publication created under `trust/` are numbered in creation order: APFS birth time, where each creation is separated by its own file or directory barrier. Every entry counts toward `dependency/create#k`, and files alone count toward `dependency/write#j`, the census's own numbering. An occurrence whose entry is a file at a relative path that (B) also writes takes the refusal. An occurrence whose path (B) does not write takes Committed. A directory occurrence is not in X9-2's kill set at this census (the kill set's `create` occurrences are files). A later census that puts one there transcribes it by the same reference, under X4T's parent-directory step.
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
    **r10:** X9-5's census is the union of two unarmed `finalize` runs, a lawful commit and an exhausted-carrier commit, and (r11) one unarmed `store_gc` run, and X9-6's union spans both targets (see the r10 header).
    **r15:** X9-4's census is the union of two unarmed commit-driver runs: the lawful first commit and the refused end (`open`, then the refused end path, which owes one `REV`), as X9-5's `candidate` child ends (see the r15 header).
    **r16:** X9-6's storage census is the union of X9-3's commit, recover and sweep parts and X9-4's refused end; the checker unions it with host's (see the r16 header).
  - **The trace digest (item 7).** A child's `trace.sha256` hashes its records grouped by thread, in each thread's own order and threads by index. The pid and the process-wide sequence number are left out, because they interleave between threads. Every drawn value in a payload is numbered by first appearance with item 7's normalizer. Without this, an unarmed observer tick interleaving with the main thread, or a drawn ExecutionId in a payload, would make two lawful repetitions disagree.
    **r14:** before the normalizer numbers drawn values, each thread's consecutive `x3c.object/` records are split into per-object groups at `x3c.object/create.before`, the groups are ordered by their records without occurrences (stable), and each name's occurrences are reassigned ascending in that order. Every lawful first commit is unchanged (see the r14 header).
  - **R3's value (item 8).** R3 is scored against the left attempt's ExecutionId. That is the outcome the sweep wrote for it, or "nothing". R2 is a lawful commit whose attempt the sweep also settles, `committed`; that settle is recorded beside R3 (`nextWriter`) and is not part of the row's R3. "R3 writes nothing" means nothing for the left attempt.
  - **F46's second variant (item 9).** "An association below `first_generation`" is not executed in M2. A fresh carrier's first generation is 1, and the ledger's `CHECK (grant_generation >= 1)` admits no association below it. Only a migrated carrier has a higher first generation, and no migration writer exists (L5). F46 runs the format-1 and format-2 variants.
- **Unchanged from r7:** every injection mechanism, point, kind, scope, label, evidence member and forbidden substitute, and every row and expected value not named above. No accepted outcome of any other law changes. No new public code, row or detail.

**r10 (2026-10-02) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r9 bytes are preserved in PROPOSAL-r9.md. r11 ACCEPTED by Grok on 2026-10-02. It was found while starting X9-5, before any X9-5 code or run, on product main `b999ae3` (X9-2 integrated). It changes four things and nothing else. The r9 sentences it touches stay in place, each followed by a short "r10" note that points here. **r11 (2026-10-02)** answers Grok's X9 r10 RF-1 and changes nothing else. r10 bytes are preserved in PROPOSAL-r10.md. The fix: X9-5's drivers are `finalize_commit` and `store_gc`, and F53 kills at `x6.sweep.settle.commit`, a point no `finalize` run reaches. So the host census also unions an unarmed `store_gc` run. r10 was not accepted, so r11 corrects the census point below, the item 5 note and the item 12 note in place.

- **Host's two matrix runners (item 6).**
  - **What X9-5 found.** Item 12 puts X9-5's rows in the integration target `crates/host/tests/commit_matrix_tests.rs`. Every one of them runs through host's commit coordinator or host's `store-gc` step, and no integration target can reach either:
    - `finalize` is `pub(crate)` (`crates/host/src/finalization.rs` line 395), in the private `mod finalization` (`crates/host/src/lib.rs`). The crate exports only `AuthoritativeRun` and `authoritative_run`.
    - `maintenance::run` and `sweep_store` are `pub(crate)`, in the private `mod maintenance`. `sweep_store` also admits natively (`SettlementSweep::admit`), which no matrix process may do (item 6, r4).
    - Nothing public calls either one. Host's `crash_matrix_support` only forwards storage's surface, and X8c's B0 to B8 drive storage's API directly, not `finalize`.

    This is the same kind of gap r4 found for the operation.
  - **Decision.** Host's `crash_matrix_support` gains exactly two runners:
    - `finalize_commit(at, root, candidate)`. It reads the on-disk run candidate at `candidate` (below), then calls host's own `finalize` with `admit` set to `operation(at, root)`, and with the support module's fixed delivery phase. `finalize` replays the candidate first, so the order "replay, then custody" is host's own code (X5 r3 item 3), and `operation` runs only if the replay succeeded. **r17 (§S12):** under X5 r4 and X7 r7, the runner makes its entry, opens the session through finalization's opening entry, then calls `finalize`, which replays after `open`. §S12.3 states the re-transcribed runner and its fixed delivery phase.
      - **The fixed delivery phase.** It renders one fixed response with exit 0 into an in-memory buffer the runner owns, and its optional effect succeeds. A delivery failure comes only from item 3's `fail-before` arm at `x7.delivery.required` or `x7.delivery.optional` (item 4; labelled `injected`). Like every delivery phase, it reads nothing from the store and takes no lease, receipt or read session (X7 r6 item 4).
    - `store_gc(at)`. It calls host's own `maintenance::run` over `settlement_sweep(at)`. `SettlementSweep` already implements `maintenance::Sweep` (`maintenance.rs` line 61). An admission refusal is reported as `sweep_store` reports one.

    **What both runners must satisfy:**
    - **Placement.** They sit in host's pinned support module, so they add no cfg site. They are compiled only under `crash-matrix`, inside `cfg(all(feature = "crash-matrix", target_os = "macos"))`, never under `scenario-fixtures`, and they are absent from every release build (item 2). They call only existing items. `finalize`, `DeliveryPhase` and `maintenance::run` are already `pub(crate)`, so nothing is widened.
    - **Value reports only.** Each returns a report of values and nothing else: the terminations as `InstallationTerminationV1` values, the retained RunId as a string, the exit, and the end-path, rollover and optional disclosures; or, for `store_gc`, each namespace's outcome and row and the ending row. A report never returns or lends an authority type (the forbidden list, with `AuthoritativeRun` and `RecoveredCommit`), and it holds no lease, lock, session or store handle once the runner returns.
    - **Inputs.** Their inputs are item 6's on-disk inputs (`SyntheticInstallation`, a root path, the candidate file). They accept no receipt, gate, guard, monitor, clock, session, permit, `ProjectOperation` or `ReplayedRun` from the caller, and no delivery phase or callback.
    - **One entry per process.** A runner makes its process's one driver entry, through `operation` or `settlement_sweep`, so r4's rule carries over unchanged. A process makes at most one call to any of the three entries and the two runners together. A second call refuses on the invariant row without effect. `publish_revocation` refuses in a process that made one: under item 11 the parent publishes, never a child.
    - **No second coordinator.** The runners are routes into host's one coordinator and host's one sweep step. They decide no outcome and project nothing of their own beyond copying values out of host's result.
  - **Rejected:**
    - **Running X9-5's children in host's unit-test binary,** where `finalize` is reachable. It contradicts item 12, which names the integration target, and item 2's `required-features` gate, which a library's unit tests cannot carry.
    - **Including a copy of `finalization.rs` in the test target with `#[path]`.** It is a second commit coordinator (X7's forbidden substitutes), and it would test the copy instead of the library. It would also compile `finalization_tests.rs`, which the file includes under `cfg(test)`, into the matrix target.
    - **Making `finalize` or `maintenance` public.** X5 r3 item 6 rejects a public host export because it invites a second commit coordinator, and no command is wired in M2 (X11).
- **The host-only order: the candidate is written before custody (items 6 and 12).**
  - **What X9-5 found.** X3d-3's `synthetic_run_candidate` is built from a `CommitSession` (`CommitSession::project_id`, `core_evaluator_closure` and its preimages; X9 r7). `finalize` replays before admission, so no session exists when it needs the candidate. A child cannot open a session for the candidate and then call `finalize`, because that would be a second entry.
  - **Decision.** A host run's scripted phase has two children before the ladder:
    - **The `candidate` child.** Its one entry is `operation(at, root)`. It then calls `CommitSession::open`, builds X3d-3's candidate from that session, and writes the candidate's retained objects (domain and descriptor), blobs and claimed RunId as canonical JSON to a file under the run's scratch root. It ends the session on its refused end path before `prepare_commit`. Host's support module supplies that file's writer and the runner's reader, as inputs only. The child registers the root and starts its carrier, as the first registration does. It creates no attempt row, SEAL or object. Its trace is recorded as every child's is. If its trace or the post state shows a ledger or attempt row, X9-5 stops and reports.
    - **The `finalize` child.** It calls `finalize_commit` over that file. Its replay runs before any custody of its own, as X5 r3 item 3 requires. **r17 (§S12):** under X5 r4 item 3, its replay runs after its entry and `open` (§S12.3). The `candidate` child is unchanged.

    The ladder's ExecutionId is the `finalize` child's draw, never the `candidate` child's. Every run that uses the file stays labelled `synthetic`. F01's replay-invalid and substituted variants are written by the parent from that file before the `finalize` child starts. They are inputs, not stored custody bytes, so they take no `mutation` label.

    This order is for host's matrix runs only. X9 r5's matrix-only order (replay after `open`) stays for storage's `commit` driver.
  - **Rejected:**
    - **Replaying after admission in host's children** (r5's matrix-only order). The children would no longer run host's order, which X5 r3 item 3 fixes, and which r5 left to X9-5. **r17 (§S12):** X5 r4 item 3 makes this host's own order, so this rejection lapses (§S12.3).
    - **A support function that builds the candidate from the installation without a session.** It would read the ProjectId and the core closure's preimages outside `CommitSession`'s getters, which X3d r8 item 13 binds the candidate to.
    - **A full commit in the `candidate` child.** The `finalize` child would then not be the root's first attempt. Its ledger would already exist, and every host row would start from a committed state the row does not name.
- **A separate host required-runs file (items 7 and 9).**
  - **What X9-5 found.** `check-unit` takes a unit's rows by case alone (`check_crash_matrix.py`, `UNIT_CASES`). Item 12 names F12, F39, F40 and F53 for both a storage unit (X9-3 or X9-4) and X9-5. With one file, X9-3's `check-unit` would demand X9-5's host F12 and F53 rows in X9-3's storage run sets, and refuse with "missing runs". The same refusal happens the other way round.
  - **Decision.** X9-5's rows live in `crates/host/tests/fixtures/crash-matrix/required-runs.v1.json`. That file uses the same schema (`opensip.x9.required-runs.v1`) and the same `clockEpoch` as storage's file, and it holds X9-5's rows and nothing else. Storage's file keeps the rows of X9-2, X9-3 and X9-4. A case in both lists has its storage rows in storage's file and its host rows in host's.
    - **Item 7's "the reviewed `required-runs.v1.json`".** It reads as the two reviewed files, each run by its own target into its own run set.
    - **`check-unit` is unchanged.** X9-5 runs `check-unit --unit X9-5 --required <host file>` over its two host run sets.
    - **X9-6's `check` takes both files and both pairs of run sets.** Every `(case, variant)` of each file has exactly one run in its own target's set, and no extra run exists. The census is the union of the two targets' censuses (item 5, r10), and every point of the union's kill set is killed by a process-death run of either target. Every other condition of `check` applies to each set. X9-6 adds this to the checker.
  - **Rejected:**
    - **X9-5's rows in storage's file.** The case-based subset refuses, as shown above.
    - **Changing `check-unit` to take rows by a unit tag.** r4 fixed the subset as item 12's case lists. A row's `units` field names owning laws, not X9 units.
- **The host census: two unarmed `finalize` runs and one unarmed `store_gc` run (item 5; r11).**
  - **What X9-5 found.** r8's census rule makes a unit's census the census of its own drivers. A lawful `finalize` commit never reaches the rollover, so F32's kills at X3b item 13's rollover points would lie outside the kill set, and `check-unit` refuses a killed point outside it. (r11) No `finalize` run calls `maintenance::run` or `settlement_sweep`, so F53's kills at `x6.sweep.settle.commit` would lie outside it too. `x6.sweep` is a durable scope.
  - **Decision.** X9-5's census is the union of three unarmed runs (r11: (c) added), each after its own fixture and `candidate` child:
    - **(a) A lawful commit** on the fresh root.
    - **(b) An exhausted-carrier commit.** The root is first set up by F32's reserved-slot setup, so the attempt reaches `CarrierCapacityExhausted`, and `finish`'s end step runs the rollover (X3b item 13; X7 r6 item 6).
    - **(c) (r11) A `store_gc` run.** It follows an unarmed (a) on the same root, in a fresh process. The sweep settles (a)'s attempt `committed`, as it settles any lawful commit's attempt (item 8, r8's R3 value), so it reaches `x6.sweep.settle.commit`. If its trace has no `x6.sweep.settle.commit` point, the run is a `HARNESS-ERROR`. Only the `store_gc` child's trace is (c)'s. The (a) before it is not counted again.

    Each of (a), (b) and (c) runs twice, and the two runs must be equal point for point. A difference is a `HARNESS-ERROR`, never a smaller kill set (item 5, r2).
    - **The union.** A point reached in more than one run takes the largest occurrence count, and the kill set is derived from the union as usual.
    - **The census trace digest.** It is the normalized lines of (a), then (b), then (c) (r8's trace rule).
    - **What the census excludes.** The fixture child and the `candidate` child are not in it. Their points are X9-2's `commit` driver prefix, not host's drivers.
  - **Rejected:**
    - **A census of the lawful commit alone.** F32's rollover kills would be refused.
    - **(r11) Moving F53's process-death kills to X9-3's file,** so that X9-5's F53 rows kill no point outside the `finalize` union. Item 12 gives F53's `store-gc` step to X9-5, and a host row of `store_gc` that cannot be killed at the sweep's own commit would not exercise the step under process death.
    - **Adding the `candidate` child's trace.** It would count X9-2's registration and INIT points again as host's.
- **Item 12.** X9-5 builds the two runners, the candidate file's writer and reader, the fixed delivery phase, the host target with its `candidate` and `finalize` children, the host required-runs file and the host census. X7 r6's session-level finalization tests (X7a call 16, X7b call 10) are met by X9-5's rows that run them:
  - a committed Run delivered (F17's base);
  - a renderer failure after commit (F16);
  - a latch after admission (F39's delivery half);
  - `CommitUndetermined` with the namespace (F12's and F40's caller route);
  - exhaustion through `finalize` (F32).

  `ExistingAttempt` with its binding is F34, X9-4's storage row. The gate-ledger balance assertion is not observable from a run record. Both stay with X7's next revision.

  X9-5 now also depends on X3d-3, the candidate's owner.
- **Unchanged from r9:** every injection mechanism, point, kind, scope, label, evidence member, row, expected value and limit; storage's `commit` driver and its r5 order; and every forbidden substitute not added below. No accepted outcome of any other law changes. No new public code, row or detail.

**r12 (2026-10-02) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r11 bytes are preserved in PROPOSAL-r11.md. r12 ACCEPTED by Grok on 2026-10-02. X9-3 found these issues in a development run of its 58 transcribed rows on product main `b999ae3`, before any lead run set. 46 rows passed, and none of the 46 changes here. Six rows failed and two were harness errors. Each was either the owning law's lawful outcome where this law's row had expected another, or a script this law fixed that cannot run. No product code changed. The r11 sentences it touches stay in place, each followed by a short "r12" note that points here. It changes the following and nothing else.

- **F13 and F14 (and F15): R2 commits a distinct Run (items 6, 8 and 9).**
  - **What X9-3 found.**
    - After a kill at `x3d.publish.commit-returned` or `x3d.publish.published`, the evidence `COMMIT` has landed. The ledger holds a receipt for the synthetic candidate's RunId.
    - The candidate gives one RunId per project (X9 r5 and r7: a function of `projectId` and the core evaluator closure). So R2 replays the same Run and stages a receipt and Run material for it.
    - The retained key already holds that Run, and staging refuses on X3c item 10's invariant row: "values that do not join, or that a retained key already holds" (`project_commit.rs`, `classify_staging`).
    - R2 was therefore `Refused(Invariant)` in F13 and F14. F12's landed variant and F15 met the same refusal, though their rows score no R2 outcome. Re-committing a Run a project already committed is the known limit X3d-2 left. This law does not test it.
  - **Decision.** Storage's `crash_matrix_support` gains a distinct variant of X3d-3's synthetic run candidate, as test support. Like the candidate, it is inputs only and compiled under `crash-matrix` only.
    - **How it is built.** It is built exactly as the candidate is, with the same session's `projectId` and core evaluator closure. The one difference: before the fixpoint rewrite, one source file's bytes in the snapshot's inventory are replaced by bytes of the same length (a salt). The rewrite then recomputes every dependent content id and digest, and the outputs are re-derived with `derive_evaluation`, so the RunId differs.
    - **What does not change.** `replay_run` stays the only constructor of its `ReplayedRun`, and every run that uses the variant stays labelled `synthetic`. No product code changes.
    - **Where R2 uses it.** R2 in F13, F14 and F15 commits the distinct variant. R2's expected outcome in F13 and F14 stays Committed. F15 gains R2 Committed beside its existing "no second receipt for this ExecutionId". A script directive (`{"r2": "distinct"}`) names it.
    - **Where R2 keeps the candidate.** Every other ladder's R2 commits the candidate as before. That includes X9-2's rows, which are unchanged, and F36's, whose R2 must commit the same semantic RunId.
  - **Rejected:**
    - **R2 expected on X3c item 10's invariant row.** "The next writer proceeds" would then be untestable in exactly the rows where the attempt committed.
    - **Re-committing the same Run.** It stays X3d-2's known limit, and no M2 law decides it. **r17 (record):** X3c r8 decides it (X3c r8 item 6a), and §RC carries its rows. The distinct variant stays where r12 and r13 put it.
- **F14's `x3d.finish.settle.before` moves to X9-4 (items 9 and 12).**
  - **What X9-3 found.** `finish` reaches that point only when a REV or a CLN is owed (`commit_session.rs`, `finish`). A lawful commit owes neither. So no X9-3 run reaches it, and it is in no census. The kill was "armed point not reached".
  - **Decision.** F14's second kill moves to an owed-end-record run under X9-4's latch context: F39's script, then a kill at `x3d.finish.settle.before`, with F13's expectations. It is an X9-4 row, and X9-4's census must reach the point. X9-3's F14 keeps its `x3d.publish.published` kill only.
- **F24's wrong-store-generation variant (item 9).**
  - **What X9-3 found.** Every row's store generation digest was changed in the parent, and the ledger file and schema stayed readable. Recovery's one snapshot then holds no attempt, receipt or association row under the admitted digest. That is the owner's §2 matrix row "both absent, no row" (`commit-recovery-readonly.v3.md` step 2): R1 is `unknown-attempt-unobserved`. R2 commits under the admitted digest. R3 finds no `admitted` row under it, so the sweep is `swept` and writes nothing.
  - **Decision.** That variant's R1 is `unknown-attempt-unobserved`, R2 is Committed, and R3 is "nothing" with the sweep `swept`. The mode-`000` and truncated-header variants keep the row as written (R1 UC, R2 refused on its X3c or X3a row, R3 host I/O and nothing written). The forbidden reading "a wrong generation is no commit" is not met: the standing is unobserved, not a negative.
  - **Rejected:** a ledger whose bytes belong to another generation's store, which needs a second store generation that no M2 writer creates (L5).
- **F27's operation and execution swaps (item 9).**
  - **What X9-3 found.** X6 r4 item 4 and the owner's step 2 make `binding-unusable` the association's store-generation, namespace or carrier mismatch only. An association whose `operationRef` differs from the attempt row, or whose `executionId` differs from the request, fails the same snapshot's join. That gives `unknown-custody` with reason `ledger-join` (`join_ledger`).
  - **Decision.** Those two variants expect R1 `unknown-custody:ledger-join`. The store-generation and namespace swaps, and a request carrying a different binding (X6 r4 item 6), keep `binding-unusable`.
- **F49(a) (item 9).**
  - **What X9-3 found.** A reader held at `x6.recover.after-j` while a lawful writer appends and exits sees the moved tail when it resumes. It takes the owner's one permitted fresh capture (step 3), which reconciles: the earlier attempt is confirmed.
  - **Decision.** F49(a)'s R1 is `committed-historically` with `pendingSettlement`. The row's law is unchanged: never UQ, never a corruption diagnosis. The second writer's own outcome is not scored, because it re-commits the same Run (the F13 limit above).
- **F36's variants (item 9).** F36 runs the orphan SEALs of F09 and F11 only. The F19 and F38 variants do not exist: under the revoked view R2 is refused at admission (C5, r3), so no later operation can commit the same semantic RunId after them. The row's later-ExecutionId check is a fifth ladder step, **R5**: `recover` of R2's own ExecutionId, together with whether the two SEALs name one RunId (item 8).
- **The F39 script's admission hold, for F39, F44 and F45 (item 11).**
  - **What X9-3 found.** `x4.gate.admit.after` is reached inside the checkpoint's shared-monitor critical section (`operation_guard.rs`, `steps`: the monitor is held from step 2 through `FinalGate::admit`). The observer's tick needs that monitor to observe and latch. So a writer held at `x4.gate.admit.after` while the parent resumes `x4.observer.tick#1` never reaches `x4.gate.latch.after`, and the run ends at the watchdog. X9-3 reproduced this with the session's own core closure revoked.
  - **Decision.** The admission-hold point of F39's script is `x3c.evidence.commit.before#1`. It is the first point after admission at which the shared monitor is released, and the gate is already admitted (state 1). The script is:
    1. arm `x4.observer.tick#*`, that point and any later hold;
    2. await the tick's first hold, then that point;
    3. the parent publishes the revocation;
    4. resume one tick and await `x4.gate.latch.after`, which is 1→3;
    5. resume the main thread.

    This is law for F39, F44 and F45. X9-4 inherits it for F39 and F40's latch variant. No point placement changes.
  - **The revoked subject.** The revocation names the `release` subject of the session's own core closure (`CommitSession::core_closure`), as X8c's B6 does. The commit child writes that closure to a file under the run's scratch root, outside the installation and outside its trace, and the publisher child reads it. The accepted store fixture's own `CORE_CLOSURE` is not the session's.
  - **Rejected:** moving the `x4.gate.admit.after` placement outside the monitor. That changes X4a's accepted placement for a script that has a lawful point to use.
- **Item 11's timing guard: assigned and specified (items 7, 11 and 12).**
  - **Where it applies.** It applies to every run that arms `x4.observer.tick`: F39, F40's latch variant, F44 and F45, and X9-4's revocation rows. X9-3 implements it for F44 and F45, and X9-4 uses the same implementation.
  - **The measurement.** The parent takes it with its own monotonic clock, not the wall clock (item 3's scripted wall clock is untouched). It runs from the moment the parent reads the writer's first `x4.observer.tick` hold record (the observer starts after the operation's first monitored read) to the moment it reads the writer's hold at the script's admission-hold point (after its last checkpoint). That bounds the awake time that X4's 10 s freshness bound charges between the first read and the last checkpoint.
  - **The record.** The run records it as an optional member `timingGuard: {"monotonicMs": n, "limitMs": 2000}` (**r13:** `limitMs` 5000; see the r13 header). Above 2000 ms (**r13:** 5000 ms) the run is a `HARNESS-ERROR`, never a pass and never an `OBSERVER.FAIL_STOP` that the run accepts. The checker admits the member, requires it for a run whose script arms `x4.observer.tick`, and refuses one above its limit. The member is not in the repetition comparison.
- **Item 7, record.** `check-unit`'s limit list is L1 to L11, as r8 set and as the checker implements. "L1 to L10" in item 7's r4 bullet was out of date.
- **Unchanged from r11:**
  - every injection mechanism, point placement, kind, scope, label, evidence member not named above, and limit;
  - every forbidden substitute;
  - every row and expected value not named above, including all of X9-2's rows;
  - X9-5's host rules.

  No accepted outcome of any other law changes. No new public code, row or detail.

**r13 (2026-10-02) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r12 bytes are preserved in PROPOSAL-r12.md. r13 ACCEPTED by Grok on 2026-10-02.
- **Where it comes from.** X9-5 found these issues in development runs of its 95 transcribed host rows, on product main `b999ae3`, before any lead run set.
- **What passed.**
  - Every F53 row and every F32 row.
    - Ten F32 kill rows passed only after a transcription correction.
    - That correction read X3b item 4a case 2 literally. The law is unchanged by it.
  - F12, F16 and F17.
  - F40 without the latch.
  - F01's two replay-refused variants.
- **What did not.**
  - Two F01 rows failed on the owning law's lawful outcome.
  - Three revocation rows were harness errors on the admission hold r12 has since moved.
- **No product code changed.**
- **How it edits r12.** The r12 sentences it touches stay in place, each followed by a short "r13" note that points here.

It changes the following and nothing else.

- **The `candidate` child's refused end appends one `REV` (record; items 6 and 9).**
  - **What X9-5 found.** The `candidate` child opens a `CommitSession` and ends it on its refused end path before `prepare_commit` (r10).
    - Every refusal after `open` latches the gate.
    - `finish` therefore appends the latched gate's one `REV` (X3d item 7 step 1, funded by the settlement reserve). X8 r5 records the same `REV` for B1, B2 and B4.
    - So every host row starts from the carrier's INIT and that one `REV` at seq 1. It has no ledger, no attempt row, no SEAL and no object.
  - **Decision.** This is the host rows' starting state. r10's "It creates no attempt row, SEAL or object" holds unchanged. The `REV` is not a ledger or attempt row, so r10's stop rule is not met.
- **F01: the substituted variants gain the latched gate's one `REV` (item 9).**
  - **What X9-5 found.**
    - **The substituted-target and substituted-inventory variants.**
      - Each replays.
      - Each is admitted, opens its session, and is refused at X3d item 3 step 1 on the invariant row. No attempt row, no ledger and no SEAL follow.
      - The refusal latches the gate, so `finish` appends one `REV`. The carrier's logical state therefore changes by exactly that record. These are X8c's B1 and B2, and X8 r5 records the same `REV`.
    - **The replay-refused variants** end inside `finalize` before `admit` (X5 r3 item 3). They leave the whole post-state unchanged. **r17 (§S12):** under X5 r4 they end after the entry and `open`, through `refused()` and `finish` with nothing appended, and still leave the whole post-state unchanged (§S12.4).
  - **Decision.**
    - **F01's replay-refused variants:** the whole post-state is unchanged (`normalizedSha256` before and after the `finalize` child). That is stronger than the cell's "ledger and carrier logical state unchanged".
    - **F01's substituted variants:** the ledger stays absent, there is no attempt row and no SEAL, and the carrier gains exactly one record, the latched gate's `REV`. Nothing else in the cell changes.
  - **Rejected:** "carrier logical state unchanged" for the substituted variants. X3d item 7 step 1 owes that `REV`, and no host order can avoid it once the session is open.
- **F40's latch variant runs landed only (items 9 and 11).**
  - **What X9-5 found.** r12 moves the admission hold to `x3c.evidence.commit.before#1`. A point takes one action, so the latch variant cannot both hold there and inject `fail-before` there.
  - **Decision.** F40's latch variant runs one script: r12's F39 script, holding at `x3c.evidence.commit.before#1`, with `x3c.evidence.commit.after#1=fail-after` armed.
    - Its expectations are F12's landed ladder, with the latch observed.
    - The not-landed latch variant is not run. Two things cover it:
      - F40 without the latch, both landed and not landed;
      - X4's in-process gate-trace test, which runs every interleaving of latch and admission (F41's "elsewhere").
    - The timing guard (r12) applies to the variant, as to F39.
  - **Rejected:**
    - **Holding at `x3c.evidence.commit.after`.** The not-landed injection is `fail-before` at `.before`, so that hold could never pair with it.
    - **Moving a placement.** r12 rejects that for the same script.
- **R2 commits r12's distinct variant after a committed Run, in host rows (items 8 and 9).**
  - **What X9-5 found.** F12's landed variant, F16 and F17 leave a committed Run, so each R2 re-committed the same Run and was refused on X3c item 10's invariant row. That is r12's F13 finding, in host rows.
  - **Decision.**
    - **Where R2 commits the distinct variant.** In every host row whose scripted phase leaves a committed Run, R2 commits r12's distinct variant (`{"r2": "distinct"}`):
      - F12's landed variant;
      - F16;
      - F17;
      - F39;
      - F40's landed variants, with and without the latch;
      - F32's `…987` variant.
    - **How the host builds it.** The host's `candidate` child writes the variant beside the candidate, from the same session. That keeps it "inputs only".
    - **What R2 is expected to give:**
      - Committed, where no revocation stands: F12, F16, F17 and F40 without the latch;
      - refused at admission, where one does: F39 and F40's latch variant (C5). The exact row is not scored.
      - In F32's `…987` variant, R2 reaches the exhausted generation before staging, as the row already states. The variant changes nothing there.
  - **Rejected:** R2 unscored in these rows. It would leave "the next writer proceeds" untested where the attempt committed.
- **The revoked subject in host rows (record of r12).** The `candidate` child writes `CommitSession::core_closure` to a file under the run's scratch root, and the host's publisher child reads it. That is r12's revoked subject, applied to the host's order, where the session is the `candidate` child's.
- **F32's `…987` variant: R1 and R4 are `unknown-quarantine-condition:journalContiguity` (item 9).**
  - **What X9-5 found.** After the reserved-slot setup at `…987`, the attempt commits (its SEAL takes `…988`). `recover` of its ExecutionId gives `unknown-quarantine-condition` with reason `journalContiguity`.
  - **Why this is the owning law's outcome.**
    - The owner's §2 ("The requested sequence against tail and floor") requires "sequence contiguity `1..t`" before any confirmation. X6's capture enforces it as the generation's row count equal to its tail (`recovery_capture.rs`).
    - X3b-2's reserved-slot technique (item 6) plants one committed `RA` at `(1, …987)`, with the trigger lifted. Below it the generation holds only the `candidate` child's `REV` at seq 1, so the count is far below the tail.
    - The writer's start reads only the tail, the witness and the floor (X3b item 9), and the floor step admits a floor below the tail. So the writer commits, and R2 reaches the exhaustion.
    - Recovery is the one reader that checks the whole sequence, and it quarantines. It is not a negative: the standing is a quarantine condition, never "not committed".
  - **Decision.** F32's `…987` R1 and R4 are `unknown-quarantine-condition:journalContiguity`.
    - R3 is not scored. The sweep reads the ledger, not the carrier.
    - The `…988` variant and its kills are unaffected. Their attempt writes no ledger, so recovery stops at the ledger (UC `ledger-missing`, then UAU) and never captures the carrier.
    - This is a property of the fixture, not of any production state. A lawful generation is contiguous. The same applies to F43's tail technique (X9-3).
  - **Rejected:** planting 986 contiguous predecessor rows to make the tail lawful. That writes a synthetic journal of about 9×10¹⁵ rows, which is impossible, and it is not the technique item 6 names.
- **The timing guard's limit is 5,000 ms (items 7, 11 and 12; r12's timing guard).**
  - **What X9-3 found.**
    - **The measurements.** On F44 the guard measured 2,845 ms, and on F45 2,893 ms.
    - **What the window covers.** It runs from the writer's first `x4.observer.tick` hold to its hold at the admission-hold point. In that time it covers only the writer's own lawful work:
      - the attempt row;
      - about 40 objects, each barriered by `F_FULLFSYNC`;
      - the SEAL and its witness writes;
      - the checkpoints.
    - **Why 2,000 ms cannot be met.** Neither the parent nor the publisher runs inside the window. In the matrix's debug profile on this host, 2,000 ms cannot be met by any lawful run.
  - **Decision.** `limitMs` is 5,000. Above 5,000 ms the run is a `HARNESS-ERROR`, as before.
    - **Why it still bounds what X4 charges.** 5,000 ms is half of X4's 10 s freshness bound, the awake time the guard exists to keep away from, and about 1.7× the measured value. So a run that passes still leaves X4's freshness stall unreached, and an `OBSERVER.FAIL_STOP` still never passes as a run.
    - **What else stays.** The measurement, its window, the record member and its exclusion from the repetition comparison are unchanged.
  - **The code changes that follow, owned by X9-3:**
    - the checker's limit;
    - its test;
    - the run record's `limitMs` constant.
  - **Rejected:**
    - **Narrowing the window to the main thread's held time.** It would stop measuring the awake time the guard bounds: the observer's freshness is charged across the writer's work, not only across its holds.
    - **Keeping 2,000 ms.** No lawful run on this host meets it, so every revocation row would be a `HARNESS-ERROR`.
    - **A limit at or near 10 s.** It would accept runs whose awake time approaches X4's own bound.
- **Unchanged from r12:**
  - every injection mechanism, point placement, kind, scope, label, evidence member and limit, except the timing guard's limit above;
  - every forbidden substitute;
  - every row and expected value not named above, including all of X9-2's and X9-3's rows;
  - X9-5's runners, host order, required-runs file and census.

  No accepted outcome of any other law changes. No new public code, row or detail.

**r14 (2026-10-03) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r13 bytes are preserved in PROPOSAL-r13.md. r14 ACCEPTED by Grok on 2026-10-03.

- **Where it was found.** In X9-3's two lead run sets, `x93-lead-1` and `x93-lead-2`, on product main `b999ae3`. They ran r13's 57 X9-3 rows uncommitted, with the 5,000 ms timing guard.
- **What passed.**
  - Each set passed all 57 rows, verdict `PASS`.
  - The two sets agreed on 50 runs, on both `normalizedSha256` and every child's trace digest.
  - F44's and F45's timing guards measured 2,683 to 2,791 ms.
- **What disagreed.** Seven runs disagreed between the two sets, so `check-unit` refused ("repetitions disagree on a trace digest"):
  - F13, F14 and F15;
  - F25's two variants;
  - F49(a);
  - F52 `purged`.

  There are three causes:
  1. **A next writer that confirms some objects and creates others.** This affects F13, F14, F15, F25 `object-deleted` and F52 `purged`, on the R2 child's trace digest. Their normalized post states agree.
     - **The mechanism.** X3c publishes a Run's objects in content-digest order (X3c item 4). The digests derive from drawn values: the synthetic candidate's ProjectId, and in F13 to F15 r12's distinct variant.
     - **Where it shows.** An R2 that finds some of its objects already present takes X3c item 4's confirm-existing branch for those and the new-object branch for the rest. Which object takes which branch, at which position, is a drawn permutation.
     - **The evidence.** In F13's R2, 54 confirmed and 28 new objects interleaved differently in two runs: the same records, permuted.
  2. **A next writer that refuses partway through its objects.** This affects F25 `object-flipped`, on the R2 child's trace digest, with 1,115 records in one set and 1,141 in the other.
     - R2 replays the same Run (r12's X3d-2 limit) and refuses at the flipped object.
     - That object's position in digest order is drawn, so the number of objects R2 publishes before it refuses differs between runs.
     - No ordering of the trace can make that agree.
  3. **Two `admitted` attempt rows in one table without rowid.** This affects F49(a)'s `normalizedSha256`.
     - Such a table dumps in primary-key order. With two rows of equal shape, that order follows their drawn ExecutionIds.
     - The unit fixes this in its post-state normalizer, as X9-2's call 7 fixed the object set. It is X9-3's judgment call, reviewed with the unit, and not law.
- **No product code changed.**
- **How it edits r13.** The r13 sentences it touches stay in place, each followed by a short "r14" note that points here.

It changes the following and nothing else.

- **The trace digest orders each object publication's groups (r8's trace rule; item 7).**
  - **The basis.** r8's trace rule makes two lawful repetitions comparable where a drawn value would otherwise move a record. X3c item 4's digest order is such a value, because it orders identical steps by drawn digests. So the rule extends to it, in the same place and with the same scope: a child's trace digest only.
  - **Decision: the object-publication group order.** Item 7's normalized lines are computed per thread, in that thread's order (r8). Before r8's normalizer numbers drawn values, each thread's records are rewritten as follows:
    1. **Runs.** A *run* is a maximal sequence of consecutive records of that thread whose full name begins `x3c.object/`. These are the per-object publication steps. The directory steps `x3c.object.objects/…` and `x3c.object.sha256/…` are not in a run, and they end one.
    2. **Groups.** A run is split into *groups*.
       - Each group begins at a record whose name is `x3c.object/create.before`, and runs up to the record before the next such record, or to the run's end.
       - Every object, new or already present, begins at `create.before`. X3c item 4 creates the object's staging file before it attempts the link. For an object already present, the link finds the name taken, and the group continues through `confirm_existing_regular`'s barriers and reopen. It never reaches `link.after`. In F13's R2, each of the 54 confirmed objects is `create, write, file-barrier, link.before, file-barrier, directory-barrier, reopen-confirm`, and each of the 28 new objects is `create, write, file-barrier, link, directory-barrier`.
       - A killed child's last group ends at its held record.
       - Records of a run before its first `create.before` form one leading group, ordered like any other. None occurs at this product.
    3. **The order key.** A group's key is the list of its records, each as `<full name without "#k">|<event>|<payload>`, compared element by element as strings, with a list that is a prefix of another ordering first. The groups of a run are sorted by key. The sort is stable, so groups with equal keys keep their trace order. Such groups hold identical records apart from their occurrences, so after step 4 their order cannot show.
       - The payload is the record's raw payload. At this product every `x3c.object/` point's payload is empty.
    4. **Renumbering.** Within a run, each full name keeps exactly the occurrence numbers it had. They are reassigned ascending in the sorted order, so the *n*th record of that name in the sorted run takes the *n*th smallest of them.
       - Records outside runs are unchanged, as are other threads.
       - The point names and occurrences in `lastHeld`, kill verification, the census points and the kill set are unchanged. They come from the raw records, not from the digest's lines.
  - **Why every lawful first commit is unchanged.**
    - **Why nothing moves.** In a lawful first commit on a fresh root, every object is new. So every group of the run has the same key: `create, write, file-barrier, link, directory-barrier`, each `pass` with an empty payload. A stable sort of equal keys moves nothing, and step 4 then assigns each name's occurrences in the order they already had. The lines, and so the digest, are byte-identical.
    - **The evidence.** X9-2's census (its commit driver) and X9-3's census (commit, recover and sweep) were regenerated with the rule in place. Both `census.json` files are byte-identical to those of the same product without it, including the census trace digest.
    - **The same holds in every run whose object groups are all alike:**
      - a writer whose every object is new;
      - a writer whose every object is confirmed, such as R2 after F07 to F12, F36 and F42, which re-publishes the same Run's complete object set.
  - **What the rule does change.**
    - **X9-3's rows.** In a run with unequal groups the digest changes, and it now agrees between repetitions. On X9-3's rows, three development run sets agreed after the change on F13, F14, F15, F25 `object-deleted`, F52 `purged` and F49(a) (F49(a) with the unit's post-state call).
    - **X9-2's rows.** The rule also changes the trace digests of X9-2's runs whose groups are unequal:
      - the child killed inside an object publication in F02 to F05, whose last group is partial;
      - the next writer in those rows, which confirms the killed attempt's objects and creates the rest.

      Their `normalizedSha256` is unaffected. Their repetition agreement is per run set and holds as before, because those orders were already deterministic: the confirmed objects are a prefix in digest order. X9-2's accepted run sets stay accepted. X9-3's X9-2 regression run uses the new rule, and X9-6 reruns everything under it.
  - **Rejected:**
    - **Sorting object groups by name, or by digest.** Names and digests are drawn values. The point is an order that does not depend on them.
    - **Leaving `x3c.object/` records out of the trace digest.** It would hide every object step from the repetition comparison, including a real difference in how many objects a writer published.
    - **Excluding the affected children from the comparison.** It drops the comparison for exactly the runs where the next writer's behaviour matters.
    - **Changing X3c's publication order.** That is product code. X3c item 4's order is lawful and is not this law's to change.
- **F25 runs R1 only, both variants (items 8 and 9).**
  - **The basis.** F25's row expects R1 alone: CAD with `evidence.missing` or `evidence.corrupt`. Its R2 is a mutation row's default (item 8), not part of the row, and it re-commits the same Run, X3d-2's known limit (r12).
    - After `object-flipped`, R2 refuses at the flipped object, at a drawn position. So its trace cannot repeat (cause 2).
    - After `object-deleted`, R2 re-creates the missing object among confirmed ones (cause 1).
  - **Decision.** F25's two variants run R1 only (`{"ladder": "R1"}`). The expected value is unchanged. R1's `stateUnchanged` is still compared.
  - **Rejected:**
    - **Leaving R2's child out of the repetition comparison.** It weakens item 7's agreement for one child kind, and it records a run whose next writer's outcome no row scores.
    - **R2 commits r12's distinct variant.** R2 would still publish around the flipped object at a drawn position, so the record count still varies.
- **The unit's post-state call (record).** Cause 3 is fixed in X9-3's post-state normalizer as a judgment call reviewed with the unit, as X9-2's call 7 was. Item 7's `normalizedSha256` definition does not change: every drawn value is still numbered by first appearance, and nothing compared is dropped.
- **Unchanged from r13:**
  - every injection mechanism, point placement, kind, scope, label, evidence member, limit and timing guard;
  - every forbidden substitute;
  - every row and expected value not named above, including all of X9-2's rows, X9-3's other rows and X9-5's;
  - X9-5's runners, host order, required-runs file and census.

  No accepted outcome of any other law changes. No new public code, row or detail.

**r15 (2026-10-03) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r14 bytes are preserved in PROPOSAL-r14.md. r15 ACCEPTED by Codex on 2026-10-03.

- **Where it was found.** It was found while preparing X9-4, on product main `b999ae3` with X9-3's uncommitted worktree as its base.
- **Nothing has been run.** X9-4 has made no census run, no development run and no lead run set. Every finding below comes from reading the code and X9-3's census trace (`x93-r14-census-x93`), and each states its file:line evidence.
  - Where a finding predicts a run's outcome, the prediction is the code's. It is not an observation.
  - If a development run contradicts one, X9-4 stops and reports, as X9-2 and X9-3 did.
- **No product code changed.**
- **How it edits r14.** The r14 sentences it touches stay in place, each followed by a short "r15" note that points here.

It changes the following and nothing else.

### X9-4's census adds the unarmed refused end (items 5 and 12)

- **What X9-4 found.**
  - **Kills outside any census.** X9-4 kills at two kinds of point that no lawful commit reaches:
    - each point of the end-path `REV` append (F19);
    - `x3d.finish.settle.before` (F14's moved kill, r12).
    - `check-unit` refuses "killed points outside the kill set" (item 7). So these points must be in X9-4's census.
  - **Why a lawful commit misses them.** `finish` owes a `REV` only if a durable SEAL has no evidence commit, the gate is latched, or a revocation was observed (`security/src/custody/commit_session.rs:1115`). It reaches `x3d.finish.settle.before` only when something is owed (`:1128`). A lawful commit owes nothing. That is r12's own finding for F14.
  - **Why the scripts that reach them cannot be a census.** Those scripts arm `x4.observer.tick` (item 11). X9-0's `Census::from_exit` refuses any armed run: "a census runs traced with nothing armed" (`platform/src/crash_barrier/driver.rs:536-541`).
- **Decision.** X9-4's census is the union of two unarmed runs of storage's commit driver. Each runs on its own fresh root after its own fixture child.
  - **(a) The lawful first commit.** This is X9-2's census run.
  - **(b) The refused end.** The child makes its one entry (`operation`) and calls `CommitSession::open`. It then reserves the end path and ends on the session's refused end path (`reserve_end_path`, then `refused().finish()`), with no candidate, no `prepare_commit` and nothing staged.
    - **Why it owes a `REV`.** The refusal latches the gate (`refuse` calls `operation.guard().stop()`, `commit_session.rs:562`). So `finish` owes one `REV` and appends it from the settlement reserve, through `x3d.finish.settle.before` and every `x3b.append.rev` point.
    - **The precedent.** This is the shape of X9-5's `candidate` child (r10), whose one `REV` r13 recorded.
    - **A check.** If (b)'s trace has no `x3d.finish.settle.before` point, the census is a `HARNESS-ERROR`.
  - **The usual rules.** Each of (a) and (b) runs twice, and the two runs must be equal point for point (item 5, r2). The union and the census trace digest follow r10's rules: the largest occurrence count wins, and the digest covers (a)'s normalized lines, then (b)'s.
  - **What is not in it.** The census does not include `recover` or `sweep` runs. X9-4 kills no point of theirs.
- **Rejected:**
  - **An armed census of F19's or F39's script.** It needs a new census constructor in X9-0's driver. It would also make a revocation, a pause and the timing guard part of the census.
  - **Dropping F19's `REV` kills, or F14's moved kill.** Item 9 and r12 name both. The census serves the kill set, not the reverse.

### A row may name its unit; F14's moved row is X9-4's (items 7, 9 and 12)

- **What X9-4 found.** r12 makes F14's `x3d.finish.settle.before` kill an X9-4 row. But `check-unit` takes a unit's rows by case alone, and F14 is in X9-3's list (`tools/check_crash_matrix.py:73`, X9-3's worktree; X9-4's list at `:75` has no F14).
  - So X9-3's `check-unit` would demand the moved row in X9-3's run sets, and X9-4's would never see it.
  - This is r10's finding again, within one file.
- **Decision.**
  - **The `unit` member.** A required run may carry an optional member `unit`, naming one unit of item 12: `"X9-2"` to `"X9-5"`. It is used only where a law moves a row to a unit other than the one its case is listed under.
  - **Only one row carries it.** It is F14's moved row, with `"unit": "X9-4"`.
  - **`check-unit` honours it.** Its subset for unit U is every row with `unit` equal to U, plus every row without `unit` whose case is in U's list. A row with `unit` is in no other unit's subset.
  - **`check` honours it.** It admits the member. Every `(case, variant)` still has exactly one run in its target's set, and nothing else in `check` changes.
  - **Who owns it.** X9-4 adds the member to the checker's required-run validation and to both selections, with tests. The harness's per-unit row selection reads the same member.
- **Why this is not r10's rejected alternative.** r10 rejected "changing `check-unit` to take rows by a unit tag", meaning re-keying every row. Here selection stays by case, and the override names only a row a law has moved. A row's `units` field still names owning laws, not X9 units.
- **Rejected:**
  - **A separate X9-4 required-runs file.** r10 used one for a second target. X9-4's rows run in storage's target with X9-2's and X9-3's.
  - **Giving the row to X9-3.** X9-3 would then run X9-4's revocation script and census part (above).

### The moved F14 row's R2 is refused at admission (items 8 and 9; C5)

- **What X9-4 found.** r12 gives the moved row "F13's expectations", and F13's R2 is Committed. But the row runs F39's script, which revokes the `release` subject of the session's own core closure (r12). Under C5, R2 is then refused at X4T's admission. The commit candidate and r12's distinct variant both bind that closure, so no R2 can commit.
  - X9-5 met the same thing in host's F39, and r13 set R2 there to "refused at admission … The exact row is not scored".
- **Decision.** The moved row's R2 is refused at admission, and the exact row is not scored.
  - R1 is CH with `pendingSettlement`, R3 `committed` and R4 CH `settled`, as F13 gives. The sweep is admitted under the revoked view (r3, G5).
  - R2 still commits r12's distinct variant if it is ever admitted. That keeps the script identical to r12's.
- **Rejected:** restoring the view before R2. No row names a restore after a revocation, and the restore would test a different state than r12 moved.

### The timing guard ends at the script's own main hold; F18 and F19 release the held tick (items 7 and 11)

- **What X9-4 found.**
  - **The guard's end point.** r12 ends the guard's window at "the script's admission-hold point (after its last checkpoint)". Only F39's script, which F40's latch variant and F14's moved row reuse, has such a point.
    - X9-4's other tick-armed scripts hold the main thread earlier: F18 at `x4.checkpoint.before-observation#1`, F19 at `#2`, F38 at `x3d.publish.after-staging#1`, and F41's latch-first order at `x4.checkpoint.before-observation#3`.
    - Each of those publishes or mutates while held there, and has no hold after its last checkpoint.
  - **The observer must be released.** In F18 and F19, item 11 resumes the main thread, never a tick, so the checkpoint's own monitored read observes the change. But the observer, held at `x4.observer.tick#1`, can only leave its loop after a stopping observation (`security/src/custody/operation_guard.rs:309-341`, `if stopped` at `:338`). The guard's drop joins the observer thread (`Observer::drop`, `:276-281`), and `finish` drops the guard (`operation_handoff.rs:592`). So a child whose tick is never resumed cannot exit. The run would end at the watchdog as a `HARNESS-ERROR`.
- **Decision.**
  - **The guard's window.** For every run whose script arms `x4.observer.tick`, the window runs from the parent's read of the writer's first `x4.observer.tick` hold to its read of the writer's first hold at any other point. That second hold is the script's main hold.
    - In F39's script, its F40 and F14 uses, and F44 and F45, that hold is r12's `x3c.evidence.commit.before#1`, so X9-3's measurement is unchanged.
    - In F18, F19, F38 and F41's latch-first order, the hold comes earlier, so the window is shorter. It still bounds the awake time X4 charges before the main hold, and nothing else changes: the 5,000 ms limit, the record member and its exclusion from the repetition comparison all stay.
  - **F18 and F19 release the tick.** After the parent resumes the main thread, it reads the writer's `x3d.finish.settle.before#1` `pass`, then resumes `x4.observer.tick#1`.
    - By then the gate is latched and the stop cause recorded (the first cause wins, `Shared::record`, `operation_guard.rs:213-216`). The tick cannot change which party latched or what the end path owes.
    - F19's kill rows, which kill inside the end path, never resume it.
- **Rejected:**
  - **No guard for scripts without an admission hold.** r12 applies the guard to every run that arms the tick.
  - **Resuming the tick before the main thread.** The observer would then latch first, which is F38's order, not F18's or F19's.
  - **Leaving the tick armed only for `#1`.** It still needs a resume to exit.

### F30: the second B commits the distinct variant; (a) compares the project's state; (b)'s sweep is refused at its admission (item 9)

- **The second B.** After A commits the candidate, a second B re-commits the same Run, because the candidate's RunId is a function of the project (r12). It is refused on X3c item 10's invariant row: r12's F13 finding, X3d-2's limit.
  - **Decision.** The second B commits r12's distinct variant, and is expected to be Committed.
- **(a) "No state change".** A holds its lease after the fence's release (X9-4 holds it at `x3c.attempt.commit.after#1`). B's admission then takes the free fence and runs X4T's fenced first read at the lease-free point. That read publishes a trust floor before B's lease attempt is refused busy.
  - **Evidence for the order.** In the commit driver's census trace, the `x4t.floor-publication` points come before `x2.lease.writer/lock.before` (`x93-r14-census-x93/census-trace.txt`, commit lines 71–134 against 155). See also `operation_guard.rs:2-4`.
  - **Why it publishes.** Under the scripted clock, B's wall second is past every stored floor (r2), so it does publish.
  - **What else B writes.** X3b's floor step writes nothing: it is skipped when the writer lease is busy (`journal_store/carrier_floor.rs:826-827`).
  - **Decision.** In (a), "no state change" compares the project's own state before and after B. That state is N's ledger and carrier, its witness and carrier floor, and its objects: the post state without `trustState` and the directory list. B's trust-floor publication is lawful (X4T r9 item 7) and is recorded, not scored: the run's `ladder` list carries one entry for B with both the full-state and the project-state comparison.
  - **(b) keeps the full comparison.** There A holds the fence, so B stops at the fence's non-blocking lock before any write.
- **(b) C, the sweep.** X6 r4 item 7, "How it gets the namespace", step 1, admits the sweep through "X1 `admit_ordinary_writer`, which holds the installation fence through the 468 gate". Its step 2, "A busy namespace is skipped and retained, never refused", applies only after that admission.
  - **What the code does.** The gate's fence lock never waits: `lock_fence`, `security/src/custody/installation_admission.rs:1129-1142`, returns `GateRefusal::Busy`. That is projected as `Busy` (`installation_routing.rs:469`). The matrix entry `settlement_sweep` runs the same writer admission before `admit_on` (`security/src/crash_matrix_support.rs:256-263`, r4).
  - **The result.** With A holding the fence in (b), C is refused at its own admission on the busy row and writes nothing. In (b) A has drawn no ExecutionId yet, so C names no attempt.
  - **Decision.** (b)'s C is expected to be refused at admission on the busy row, writing nothing. (a)'s C keeps "skips and retains the namespace".
- **Rejected:**
  - **The second B committing the same Run.** That is r12's rejected expectation.
  - **The full-state comparison for (a).** No lawful run meets it.
  - **Moving (b)'s hold to after A releases the fence.** That is (a).

### F26's "no grant reused" is observed on R2 (item 9)

- **What X9-4 found.** X4 r7 item 7 states it as "The guard is never reused, and current custody still gates reading (F26)". No barrier point or outcome names a grant.
- **Decision.** F26 scores the row's "no grant reused" as two things:
  - R2 is refused at admission (exact row not scored);
  - R2 leaves the project's own state unchanged (the F30 comparison above), captured just before and just after R2.
- R1 is CH.
- **Rejected:** an in-process assertion on the guard's identity, which no process-level run can make.

### F18's mixed view is covered elsewhere; its unreadable view is defined (item 9)

- **What X9-4 found.**
  - **What "mixed" needs.** A mixed view is X4 r7 item 5's "second view that is still mixed": `state.v1` replaced under both attempts of one observation (`ObservationFailure::Mixed`, `security/src/trust/live_observation.rs:365`, returned at `:479`).
  - **Why no process can produce it.** Between an attempt's open (step 1) and its reopen (step 4), the only seam is the `cfg(test)` `ObservationHook` (`:398-406`). The observation has no barrier point there, and adding one would be a new placement, which item 5 assigns to the owning unit.
- **Decision.**
  - **F18's mixed variant is "elsewhere".** It is covered by X4a's in-process test `a_replacement_during_the_first_attempt_is_absorbed_and_a_second_is_mixed` (`security/src/custody/operation_live_tests.rs:593`). The test drives two replacements through the hook and asserts `OBSERVER.FAIL_STOP`, subject `mixed` (`:625`).
  - **F18's unreadable variant is executed.** The parent sets `I/trust/stores/S/state.v1` to mode `000` while the writer holds at the checkpoint (labelled `mutation`), and restores its mode before the ladder.
    - Expected: `OBSERVER.FAIL_STOP`, subject `unreadable`; R2 is Committed after the restore, as the row states.
    - F19's fail-stop variant uses the same mutation at checkpoint #2.
- **Rejected:** a placement inside the live observation, which changes X4a's accepted placements for a case its own test covers.

### F34's run A: the ledger and SEALs are unchanged; the carrier gains the latched gate's one `REV` (item 9)

- **What X9-4 found.** A's `ExistingAttempt` comes from `prepare_commit` after `open`, on `session.refused()` (`storage/src/commit.rs:528-535`). That latches the gate (`commit_session.rs:529-530`, `:562`), so `finish` appends one `REV`. This is r13's finding for every refusal after `open`.
  - So "no new row, no SEAL … the earlier attempt's rows unchanged" holds for the ledger and the SEALs, not for the whole post state.
  - The invariant-row projection (`SYSTEM.OUTCOME.ILLEGAL_STATE`, `HOST.INVARIANT_VIOLATED`) is the host's (X7 r4 item 3). A storage run observes `NotPrepared::ExistingAttempt { execution_id, requested }`.
- **Decision.** F34's run A expects:
  - `ExistingAttempt`, whose `execution_id` is the earlier attempt's (the subject);
  - N's ledger unchanged across A;
  - no SEAL added;
  - the carrier's change, the one `REV`, is not scored.

  A's disclosed `requested` binding is run B's input. B's two expectations, and its `normalizedSha256` unchanged, stay as the row states. The host's projection stays with X7's next revision, as r10's item 12 note left it.
- **Rejected:** "the whole post state unchanged" across A, which X3d item 7 step 1 forbids once the gate has latched.

### The unit's judgment calls (record)

These change no expected value and are X9-4's, reviewed with the unit:
- the hold points X9-4 chose where a row names none:
  - F06 holds the writer at `x3c.attempt.commit.after#1` while the parent takes its `BEGIN IMMEDIATE`, and releases it after the writer exits;
  - F30(a) and (b) hold A at `x3c.attempt.commit.after#1` and `x2.lease.writer/lock.after#1`;
  - F41's latch-first order holds at `x4.checkpoint.before-observation#3`, outside the shared monitor (`operation_guard.rs:549` against `:552`);
- F40's two no-latch variants run under case F40 with F12's scripts;
- F26's, F39's and F41's R3 and R4 run and are recorded, unscored;
- F19's fail-stop R2 and F41's writer outcome are unscored, as their rows give none;
- F06's "an earlier level-3 transaction is released" has no barrier point and is not scored;
- the repetition risk of F30's held writer under the unarmed 5 s observer period. This is r3's disclosed gap; X9-4 reports it if a run shows it.

### Unchanged from r14

- every injection mechanism, point placement, kind, scope, label, evidence member, limit, and the timing guard's limit, measurement clock, record member and repetition exclusion;
- every forbidden substitute;
- every row and expected value not named above, including all of X9-2's, X9-3's and X9-5's rows;
- r14's trace rule, X9-5's runners, host order, required-runs file and census.

No accepted outcome of any other law changes. No new public code, row or detail.

**r16 (2026-10-03) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r15 bytes are preserved in PROPOSAL-r15.md. r16 ACCEPTED by Grok on 2026-10-03.

- **Where it was found.** It was found while preparing X9-6, the M2 exit, on product main `91cb45a`, which has X9-0 to X9-5 integrated.
  - X9-6's checker and storage driver are uncommitted in worktree `opensip-x9-6`, as the code unit X9-6a.
  - No `crates/*/src` file has changed since `b999ae3`.
- **What was run.** Census runs only: no development run and no lead run set.
  - Storage's `x9_6_matrix` and host's `x9_5_matrix` ran with `OPENSIP_X9_CENSUS_ONLY`, as run sets `x96-census-storage` and `x96-census-host`.
  - Then the new checker command `coverage` ran. It compares the union census's kill set with the kill scripts of both reviewed required-runs files, and runs nothing.
- **What the census and the coverage gave:**

  | Measure | Value |
  |---|---|
  | Storage census | 259 points; trace 1379 records, `e9add21e…`; `census.json` `6fa3cc02…` |
  | Host census | 218 points, the same as X9-5's accepted census; trace 1195 records, `93d0922a…`; `census.json` `2492cbd0…` |
  | Union census | **321 points**; kill set **383** |
  | Kill-set points killed by an existing row | 333 |
  | Killed points outside the kill set | none |
  | Kill-set points no row kills | **50** |

- **Predictions.** Where a finding below predicts a run's outcome, the prediction comes from the code, the census trace and the owning law. It is not an observation.
  - X9-6 transcribes the new rows before any run.
  - If a development run contradicts a prediction, X9-6 stops and reports, as X9-2 to X9-4 did.
- **No product code changes** beyond X9-6a's matrix-target and checker code. No product file is added.
- **How it edits r15.** The r15 sentences it touches stay in place, each followed by a short "r16" note that points here.

It changes the following and nothing else.

### Kill-set coverage: 50 new kill rows (items 5, 7, 9 and 12)

- **What X9-6 found.**
  - **The requirement.** Item 5 makes the kill matrix "every durability point in the census, at `#1` and … the first, a middle and the last occurrence". Item 7 and r10 require every point of the union's kill set to be killed by a process-death run of either target.
  - **Why it is not met.** Each of X9-2 to X9-5 transcribed only its own item-9 rows under `check-unit`, which requires only that the unit's killed points lie inside its kill set (r4). Item 12's X9-6 line adds no rows. So 50 union kill-set points have no row.
    - X9-2's F00 kills every kill-set point *before* `x3c.attempt.commit.after` (its transcription, `reviews/grok-crash-matrix-x92-r1/transcribe_required_runs.py:105`). After that point it kills only the F02 to F10 steps.
    - X9-3, X9-4 and X9-5 add only their rows' points.
  - **The 50 points, by scope.** `coverage.json` lists each one with its census counts.

    | Scope | Points |
    |---|---|
    | `x4.checkpoint` | 12 |
    | `x3c.object` | 9 |
    | `x2.lease` | 6 |
    | `x3b.append.seal` | 5 |
    | `x7.delivery` | 4 |
    | `x3c.evidence` | 3 |
    | `x3d.finish` | 3 |
    | `x2.fence` | 2 |
    | `x3d.publish` | 2 |
    | `x4.gate` | 2 |
    | `x6.sweep` | 2 |

- **Decision.** Every uncovered point gets a process-death row. None is dropped by a coverage rule.
  - **Why no coverage rule.** Each of the 50 is a real step at which a process can die. Several hold a lock or an open transaction: the level-3 `BEGIN`s and level 4, the checkpoint's monitor lock, the readers lease, the fence's end lock, and the sweep's exclusive hold. Item 5 names exactly these as the matrix.
  - **Equivalence is not a ground.** "Equivalent to an adjacent point" would be a reading of the product, not of the census. A kill costs about 5 s.
  - **Not a point that can be omitted.** `x4.checkpoint` and `x4.gate` are registered `Durable` (`crash_barrier.rs:102-103`), and the checkpoint takes a lock primitive (`x4.checkpoint/lock.before`). Changing their registration would be a product change, outside this law.
  - **Recover's readers lease** (`x2.lease.readers/*` in the `recover` part) has the same point identity as the sweep's. It is covered by the sweep rows below, because the census and the kill set are by point name and occurrence.
  - **Window and expected values.** Each row is placed by its crash window, a position in the census trace, never a run's outcome (as r5 placed F00's split). It takes the expected values the owning law already gives that window's existing row. Each is a kill script, `[{"arm": "<P>=hold"}, {"await": "<P>", "then": "kill"}]`, unless stated otherwise.
  - **Labels.** `process-death`, `scripted-clock`, `synthetic`.
  - **Variant names.** As X9-2's transcription names them: `kill-<point slug>-<k>`.
  - **Units.** Those of the case.

**The windows.** Commit-trace positions are those of the storage census's `commit` part, `census-trace.txt`. Abbreviations are item 8's.

| Window | Points (census trace) | Case | Expected (the owning law) |
|---|---|---|---|
| **W1a.** Attempt committed; objects being published; no SEAL | `x3c.object/create.before`, `create.after`, `write.after`, each at `#1`, `#41`, `#82` (9 points; 82 occurrences in both targets) | F02 | As F02: `scripted` killed, R1 UAO, R2 Committed, R3 refused, R4 TNC. Staging residue is never adopted (X3c item 4; F02's row). F02's existing rows do not score R2's witness action, and neither do these. |
| **W1b.** Both level-3 transactions and level 4 taken, the first checkpoint, nothing appended (trace 30–37: `x3b.append.seal.begin` < `x3c.evidence.begin` < `level-four` < `x4.checkpoint/lock.before#1` < `before-observation#1` < `after-observation#1` < `before-admit#1` < `built`) | the 8 points named, each `#1` | F07 | As F07 before `witness-pending/rename.after` (r8): R1 UAO; R2 witness action **OK**, Committed; R3 refused; R4 TNC. The open transactions die with the process (L2), and the start reconciles a consistent tail (X3b items 4 and 4a; r8's F07 finding). |
| **W2.** SEAL and its COMMITTED witness durable; evidence transaction open, not committed (trace 62–77) | `x4.checkpoint/lock.before`, `before-observation`, `after-observation`, `before-admit` at `#2` and `#3`; `x3d.publish.after-staging#1`; `x3d.publish.before-final-checkpoint#1`; `x4.gate.admit.after#1`; `x3c.evidence.commit.before#1` (12 points) | F11 | As F11: the ledger transaction rolls back, and the SEAL is durable with no `REV`. R1 UAO; R2 Committed; R3 refused; R4 TNC. **Also scored:** R2 witness action **OK**. The tail is the SEAL under a COMMITTED witness, F10's state after `witness-committed/rename.after` (F10 r5 and r8; X3b item 4). A kill at `x3c.evidence.commit.before` is F12's not-landed state, reached by death. |
| **W3.** Evidence `COMMIT` landed; before `published` (trace 78–81) | `x3c.evidence.commit.after#1`; `x3b.append.seal.release-level-four#1`; `x3b.append.seal.release-level-three#1` | F13 | As F13: R1 CH `pendingSettlement`; R2 commits r12's distinct variant (`{"r2": "distinct"}`), Committed; R3 committed; R4 CH `settled`. F12's landed state, reached by death. |
| **W4.** Published; lease release and end step, before the end floor (trace 83–88) | `x2.lease.writer/unlock.before#1`, `unlock.after#1`; `x3d.finish.lease-release#1`; `x3d.finish.end-step.before#1`; `x2.fence.end/lock.before#1`, `lock.after#1` | F14 | As F14's `published` row (as F13): R1 CH `pendingSettlement` (a lawful `finish` owes and settles nothing, X3d item 7); R2 distinct, Committed, its floor step handling any unwritten end floor (X3b item 4a); R3 committed; R4 CH `settled`. |
| **W5.** The refused end path after a revocation (refused-end census part: `x4.gate.latch.after#1` before `x3d.finish.settle.before#1`; `x3d.finish.settle.after#1` after the `REV` append) | `x4.gate.latch.after#1`; `x3d.finish.settle.after#1` | F19 | F19's kill script (r15), with the kill at the point: arm `x4.observer.tick#*`, `x4.checkpoint.before-observation#2` and the point; revoke while held at the checkpoint; resume the main thread; await the point, then kill. Expected as F19's `REV` kill rows: R1 UAO; R2 refused at admission (`operation:*`, row not scored, C5); R3 refused; R4 TNC. The timing guard applies (r12, r15). |
| **W6a.** The sweep before its settle `COMMIT` | `x2.lease.readers/lock.before#1`, `lock.after#1`; `x6.sweep.after-exclusive#1`; `x6.sweep.after-snapshot#1` | F53 | F53's sweep-kill script (writer killed at `x3c.attempt.commit.after#1`; the first sweep armed and killed at the point; a second sweep; ladder R1). Expected as F53's `settle.commit.before` kill: `first` killed, `second` refused, R1 TNC. Nothing was settled, and the next sweep settles the row once (X6 r4 item 7; the monotone trigger). |
| **W6b.** The sweep after its settle `COMMIT` | `x2.lease.readers/unlock.before#1`, `unlock.after#1` | F53 | As F53's `settle.commit.after` kill: `first` killed, `second` nothing, R1 TNC. |
| **W7.** Host delivery after `x3d.finish.end-step.after` (host census (a), trace 1005–1008) | `x7.delivery.required.before#1`, `.after#1` (F16); `x7.delivery.optional.before#1`, `.after#1` (F17) | F16, F17 | Host script `[{"r2": "distinct"}, {"arm": "<P>=hold"}, {"run": "finalize"}, {"await": "<P>", "then": "kill"}]`, the shape of F32's kill rows. Expected: `finalize1` killed; R1 `committed-historically:pendingSettlement`; R2 `authoritative:0`; R3 committed; R4 `committed-historically` (host's spellings, as in F12's landed host row). The Run is committed and kept; a death in delivery changes no evidence (line 610; X7 r6 item 4: delivery reads nothing from the store and takes no custody). |

**Totals.** Storage gains 46 rows (F02 9, F07 8, F11 12, F13 3, F14 6, F19 2, F53 6), for 381 in all. Host gains 4 (F16 2, F17 2), for 98.

- **Transcription.** X9-6 appends these rows to the two files before any run, from `x96-census-storage` and `x96-census-host` and this table only. X9-2's to X9-5's rows stay byte for byte.
- **Selection.** The new rows carry `"unit": "X9-6"` (see the `unit` member below), so no unit's `check-unit` subset changes.
- **F17's L9 is unchanged.** F17's kill rows kill the process inside the injected-path delivery phase. They are not native optional delivery, which stays a limit.
- **Rejected:**
  - **A coverage rule that exempts read-only-looking or "adjacent-equivalent" points** (the checkpoint, the gate, the delivery points). It weakens item 5 by a reading of the product. The rows are cheap.
  - **Re-registering `x4.checkpoint`, `x4.gate` or `x7.delivery` as `ReadOnly`.** That is a product change to X4a's and X7's accepted placements.
  - **Killing W1b and W2 under F18, F38 or F39's revocation scripts.** Those test revocation. These rows test death at the step.

### The `unit` member gains `"X9-6"` (items 7 and 12; r15)

- **What X9-6 found.** The 50 rows above belong to cases in other units' lists (F02, F07 and F11 to F53). Under r15's rule, X9-2's, X9-3's and X9-4's `check-unit` would demand them, and so would X9-5's, which lists F16, F17 and F53.
- **Decision.** r15's `unit` member may name `"X9-6"`. Each of the 50 rows carries it.
  - `check-unit` admits no `--unit X9-6`: X9-6 is checked only by `check`.
  - `check` needs every row, as before.
  - The checker's validation and the harness's `owned()` read the member as r15 states. This is an X9-6a code change, with a test.
- **Rejected:** giving the rows to the case's unit, which would reopen accepted units' run sets.

### The union occurrence counts (items 5 and 7; r10 and r11)

- **What the census showed.** Every name the two targets share has an equal count in both, except the eight `x4t.floor-publication.dependency/*` names.
  - Storage's commit reaches one more occurrence than host's `finalize`, whose installation already published once in the `candidate` child.
  - The union takes storage's count. So F00's kills at storage's `#1`, middle and last are exactly the union's kill-set points for those names.
  - Host's own middles (for example `create.after#3` of 6) are not union points.
  - `killedOutsideKillSet` is empty.
- **Decision.** None is needed. r10's rule stands. This is recorded so that a later census that inverts the counts is read by the same rule: such a shift re-transcribes the affected F00 rows before any run, never after one.

### X9-6's storage census (record; items 5 and 12)

- **The composition.** X9-6's storage census is the union of every storage driver's unarmed census part:
  - X9-3's commit, recover and sweep, on one fresh root;
  - then X9-4's refused end, on its own fresh root.

  Each part runs twice and must be equal, and the trace digest hashes the parts' normalized lines in that order. X9-2's census is the commit part, and X9-4's lawful commit is the same run.
- **Host.** Host's census stays X9-5's (a), (b) and (c).
- **Across targets.** The checker forms the cross-target union. Each target's census trace digest is compared between repetitions; no cross-target trace digest is defined.

### Item 8's release order is asserted on every lawful commit child (items 7 and 8)

- **What X9-6 found.**
  - **The law.** Item 8 says "every lawful run also asserts the release order line 608 requires, from its trace". The required order is level 4, then each level-3 transaction, then the lease, then the fence. Build plan lines 139–143 and 168–172 give it: both level-3 transactions are taken in a fixed order before level 4, and they are released after it, then the lease, then the S7 end handoff.
  - **What the harness checks today.** It derives `<n>.releaseOrder` as `seal.L4,seal.L3,rev,cln` only (`commit_tests.rs:1312-1349`). Only F19's base rows score it. The lease and the fence appear in no assertion, and host asserts nothing.
- **Decision.** It is a verdict condition, like R1's `stateUnchanged` (`verdict()`, `commit_tests.rs`): not a row value and not a new evidence member.
  - **Which children.** For every child of a run, storage or host, whose outcome is a commit (`Committed…` or `authoritative:…`), the harness checks, on that child's own trace:
    1. **acquisition:** `x3b.append.seal.begin` < `x3c.evidence.begin` < `x3b.append.seal.level-four`, the fixed order, never level 3 under level 4;
    2. **release:** `x3c.evidence.commit.after` < `x3b.append.seal.release-level-four` < `x3b.append.seal.release-level-three` < `x2.lease.writer/unlock.after` < `x2.fence.end/unlock.after`, each at the occurrence that follows the SEAL;
    3. **owed records:** where the child appends a `REV` or `CLN`, that append's `release-level-four` < `release-level-three` comes before the same `x2.lease.writer/unlock.after`.
  - **On violation.** The run's verdict is `FAIL`, with the miss "release order".
  - **Where it holds already.** The storage census `commit` part meets it (trace 30–32 and 78–104).
  - **What it does not touch.** Killed children are exempt, since they release nothing.
  - **Who owns it.** X9-6a adds it to both matrix targets.
- **Rejected:**
  - **Scoring it as a row value.** That re-transcribes about 300 accepted rows for a condition every lawful child shares.
  - **A checker condition.** The checker sees trace digests, not traces.

### The evidence record (item 7)

- **What X9-6 found.** Item 7 commits "the final run set" as one `matrix.json` and `runs/`. X9-6 has two targets, each with its own `matrix.json`, and two repetitions.
- **Decision.** The layout of `docs/implementation/m2/crash-matrix-x9/evidence/<C>/` is:

  ```
  check.json                    the checker's two-target `check` output (matrixPass)
  release-absence.json          the record every set used
  hashes.txt                    sha256, bytes, path of every file below, and of both
                                required-runs.v1.json files at C
  storage/matrix.json           lead-1
  storage/census-trace.txt      lead-1
  storage/runs/*.json           lead-1, 381 records
  host/matrix.json              lead-1
  host/census-trace-{a,b,c}.txt lead-1
  host/runs/*.json              lead-1, 98 records
  lead-2/storage/matrix.json    pins every lead-2 run's bytes and sha256
  lead-2/host/matrix.json
  ```

  - **Why lead-1 in full and lead-2 by its pins.** The checker has already compared lead-2 with lead-1 run by run.
  - **The reviewer's rerun** stays in its review directory, with its own `check.json` for the pairs (lead-1, reviewer) and (lead-2, reviewer).
  - **No tarballs.** Failure tarballs and raw state bytes are never committed (item 7).
- **Size.**
  - **Not measured yet.** The census-only runs write no run record: `census.json` is 21 KB for storage and 18 KB for host, and the traces are 76 KB and 55 KB.
  - **The estimate.** It comes from the post-state capture (`crash_matrix_support/post_state.rs` `capture`: one `raw` entry per installation file, plus the SQLite tables row by row): about 40–100 KB per record, so about 20–48 MB for 479 records.
  - **The rule.** X9-6 measures one set before committing.
    - If a target's `runs/` is at most 64 MB, the records are committed as plain files.
    - Otherwise that target's `runs/` is committed as one `runs.tar.xz`. Under `docs/implementation/**` LFS already tracks it. Its `matrix.json` stays plain, with every member's pin, and `hashes.txt` pins the archive.
    - This is not a failure tarball, and the evidence stays digests plus logical dumps.
- **Rejected:**
  - **Committing both repetitions in full.** It doubles the size for evidence the checker has already compared.
  - **A merged `matrix.json`.** That would be a new schema. The checker already unions the two targets' records.

### Records (no rule changes)

- **The r14 overstatement.** r14 says its object-group order changes X9-2's F02 to F05 next-writer trace digests too. X9-3's comparison showed that only the killed child's digest changed (14 of 22 runs): the next writer's confirmed objects already sort first. No expected value depended on it.
- **The X9-1 clock-window self-test flake** (EXIT-PLAN, "X9 follow-ups") is closed by F7 at product `9c5f145`.
- **r3's disclosed gap** (the unarmed 5 s observer in census runs). X9-6's census parts were each equal across their two runs, so no rule is needed.

### Unchanged from r15

- every injection mechanism, point placement, kind, scope, label, evidence member, limit, and the timing guard's limit, measurement clock, record member, repetition exclusion and end point;
- every forbidden substitute;
- every existing row and expected value, including all of X9-2's, X9-3's, X9-4's and X9-5's;
- r14's trace rule;
- X9-5's runners, host order, required-runs file and census;
- X9-4's census.

No accepted outcome of any other law changes. No new public code, row detail or product file.

**r17 (2026-10-04) is a record revision in three sections, accepted section by section (lead decision LD-17-1).** r16 bytes are preserved in PROPOSAL-r16.md (sha256 `f08efe95…`, 185,750 bytes). r16's acceptance note above is r16's own and stays. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Round 1 (this round) is this header, the section frame and §RC. Not accepted.**

- **Citations.** r17 cites pinned snapshots:
  - X9:n is `PROPOSAL-r16.md`;
  - X3C:n is `m2/ledger-blob-x3c/PROPOSAL-r8.md` (X3c r8, accepted by GROK2, `ba638efb…`);
  - J1:n is `m3/host-pipeline-j/PROPOSAL-r5.md` (J1 r5, accepted by Codex, `4ccb2320…`);
  - JRW:n is `m3/resume-repair-jrw/PROPOSAL-r3.md` (J-RW r3, in review, `9aa30410…`);
  - M3P:n is `m3/M3-PLAN-r9.md` (accepted by GROK2, `72bc7a13…`);
  - OVERNIGHT:n is `OVERNIGHT-2026-10-03.md`.

  Product lines are at main `d2c00a9`.
- **Why r17 exists.** Three laws name "X9 r17" as the record that carries their rows:
  - X3c r8's CL-2: "X9 r17 carries item 14 as its own section, with the prefix `RC-`" (X3C:354). X3c-3 needs it before its code (X3C:257, :259).
  - J1's successor S12, "X9 r17 (record and rows)" (J1:858), for J3b and J3d.
  - J-RW's X-RW-10 and RW-S6 (JRW:669, :625), for J4e.

  M3-PLAN r9's "X9 r17 record" row makes these one record revision with three sections. Each is transcribed when its unit is ready, and none changes another's rows (M3P:319).
- **Lead decision LD-17-1: r17 is accepted section by section.**
  - This round writes the r17 header, the section frame and §RC in full.
  - §S12 and §RW are reserved headings. Each states its owner and the condition that fills it. Neither carries a row.
  - Later rounds append §S12 and §RW to this same r17. Each is reviewed on its own, and none changes another's rows.
  - So every citation of "X9 r17" in J1, X3c r8, J-RW and M3-PLAN stays valid.
  - **Rejected: r17 as §RC only, with §S12 in r18 and §RW in r19.** Four laws cite "X9 r17" for their rows, and each of those citations would go stale.
  - **Rejected: waiting for all three sections.** §RW waits on J-RW, which is still in review, and §S12 waits on J3b. Waiting would block X3c-3 on both.
- **What round 1 changes outside its sections:**
  - the title;
  - six in-place "r17" notes, each pointing to §RC: r12's re-commit rejection, and items 5, 7, 8, 9 and 12;
  - one forbidden substitute.

  The sections themselves follow "Not claimed", under "X9 r17 sections".
- **Unchanged from r16:**
  - every injection mechanism, point placement, kind, scope, label, run-record member, limit, and the timing guard's limit, clock, member, exclusion and end point;
  - every forbidden substitute, apart from the one r17 adds;
  - every existing row and expected value of both required-runs files;
  - r14's trace rule;
  - X9-5's runners, host order, required-runs file and census;
  - X9-4's census.

  No accepted outcome of any other law changes. No new public code, row detail or product file. §RC.7 lists what §RC adds to the matrix target and the checker.

**r17 round 2 (2026-10-04) fills §S12 and records X4 r8's note. Not accepted.** Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Its diff base is round 1's accepted bytes, `PROPOSAL-r17-RC.md` (`89fc47ff…`, 235,499 bytes). The live file differed from those bytes only by round 1's acceptance note, which stays.
- **What round 2 changes:**
  - this paragraph;
  - the frame table's §S12 status cell;
  - §S12, filled in place, with lead decisions LD-S12-1 to LD-S12-8;
  - six in-place notes: one "r17 round 2" note on G4's `x4.gate.latch.after` (above), and five "r17 (§S12)" notes on the host order: r5's matrix-only order, r10's runner, r10's `finalize` child and its rejected alternative, and r13's F01 decision;
  - one forbidden substitute.
- **What it does not change.** §RC, and every other text of r16 and round 1. Every expected value of both required-runs files (§S12.4). Every census and kill set (§S12.6). Every accepted outcome of another law. There is no new public code, row detail or product file.
- **Citations in round 2.** Round 1's short names stand, so X9:n is still `PROPOSAL-r16.md`. Round 2 adds these snapshots:
  - J1r6:n is `m3/host-pipeline-j/PROPOSAL-r6.md` (J1 r6, accepted by Codex, `086e804a…`; `m3/reviews/codex-host-pipeline-j-r6`). J1 r6 keeps r5's item 12 rows and records S18 and S21 as bound (J1r6:864);
  - X3D9:n is `commit-session-x3d/PROPOSAL-r9.md` (X3d r9, accepted by Grok, `c727001a…`);
  - X4r8:n is `live-guards-x4/PROPOSAL-r8.md` (X4 r8, accepted by CODEX2 at round 3, `dc239187…`);
  - X7r7:n is `finalization-x7/PROPOSAL-r7.md` (X7 r7, accepted by GROK2, `7757935c…`);
  - X3B11:n is `journal-x3b/PROPOSAL-r11.md` (X3b r11, accepted by CODEX2, `27ed0aaf…`);
  - S18:n and S21:n are `m3/host-pipeline-j/s18/README.md` and `s21/README.md` (both accepted and bound);
  - SOP2:n is `m3/operability/s-op-2/PROPOSAL-r6.md` (accepted by Codex, `ce8d3a4b…`).

  X5 r4, J1's successor S8, is in review beside this round. §S12 cites its item 3 through J1r6:517, which states it word for word, and X7r7:315, which assumes it. Product lines are at main `1799d3d`.
- **Snapshot.** On acceptance, round 2's bytes, without its acceptance note, are preserved as `PROPOSAL-r17-S12.md`, as round 1's are `PROPOSAL-r17-RC.md` (frame rule 6).
- **X4 r8's record note (X4r8:762-765; LD8-4).** X9 names `x4.gate.latch.after` as X4a placed it, straight after the gate's `fetch_or` (G4, above; item 5's point table, X9:943). Under X4 r8, the point follows the stop transition's release, after the stop-cause lock is released, for every existing latch source, on every call (X4r8:395-397). Code unit X4-F3 makes this move (X4r8:593). J3b adds the cancellation latch's point, which fires only after a successful exchange (X4r8:397).
  - **What stays.** The point is reached on the same calls, in the same per-thread order (X4r8:515; W-7, X4r8:548). The stop transition's critical section holds only the word's atomic operations and one record. It never holds I/O, a wait, a callback or a crash point (X4r8:401). So nothing durable happens between the `fetch_or` and the point's new place.
  - **The census does not change.** Each target's census keeps every name and every occurrence count, so item 5's kill set and r10's union keep every point (X9:233).
  - **No expected value changes.** These rows observe the point:
    - storage's F14 `kill-x3d-finish-settle-before-1-after-latch`, F38 `revoked-after-staging`, F39 `latch-after-admission`, F40 `fail-after-evidence-commit-latched`, F41 `latch-before-admission` and `admission-before-latch`, F44 and F45. Each awaits `x4.gate.latch.after#1` before it resumes the writer;
    - storage's F19 `kill-x4-gate-latch-after-1-after-revoke`, which kills there;
    - host's F39 `latched-after-admission-delivery` and F40 `latched-fail-after-evidence-commit`, which await it inside `revoke-latch-resume` and score `gateLatched` from its presence in the trace.

    Each awaits or kills the same occurrence of the point. When the parent now sees it, the first stop's cause is already recorded, which is the state each expected value assumed. A kill there ends the process with the latch and the cause in memory only, so F19's killed row leaves the same durable state. X4 r8's `CertainRefusal` keeps every row and the `REV` reason `operation-stopped` (X4r8:513), and no expected value names a `REV` reason.
  - **How it is checked.** X4-F3's integration commit reruns both lead sets, serialized (X4r8:606). Its census-only step comes first. It must show both censuses unchanged: the same names, counts and kill sets as the lead set before it. Then `check` must pass every row of both files. X4-F3's in-process test W-7 pins the point's count and per-thread order. If a transcribed value moved, X4-F3 stops and reports, and the lead re-transcribes it in a new round of r17 before X4-F3's review, never from a run (X4r8:765; J1r6:863). If X4-F3 lands in J3b's commit, J3b's lead set is X4-F3's too (§S12.6).

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
     **r16:** X9-6's union census (storage 259 points, host 218, union 321, kill set 383) left 50 kill-set points without a row; each gets a process-death row by its crash window, and none is exempted (see the r16 header).
     **r17 (§RC):** storage's census gains the `recommit` part, a lawful re-commit. It adds `x3c.object/reopen-confirm.before` and `.after`, and raises `x3c.object/file-barrier.before` and `.after` to 164 occurrences, so their selection becomes `#1`, `#82` and `#164`. F03's two `#41` rows stay (see §RC.3).
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

     **r10:** host's support module adds two runners, `finalize_commit` and `store_gc`. Each makes its process's one entry and returns value reports only. Host's module also holds the on-disk run candidate's writer and reader. These are not a fourth entry, and they return no authority type (see the r10 header).

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
       **r16:** for two targets: lead-1's storage and host `matrix.json`, census traces and `runs/` in full, lead-2's two `matrix.json`, the `check` output, the release-absence record and `hashes.txt`; `runs/` over 64 MB per target goes as one LFS `runs.tar.xz` (see the r16 header).
   - **The checker.** It is `tools/check_crash_matrix.py` in the product: read-only, standard library only, under the pinned Python. It refuses unless all of these hold:
     - every `(case, variant)` in the reviewed `required-runs.v1.json` (item 9) has exactly one run, and no extra run exists (**r15:** a row's optional `unit` member is admitted);
     - every verdict is `PASS`;
     - the labels equal the required labels;
     - `product.commit` is the reviewed commit, and the worktree is clean;
     - the census and the kill set agree (item 5);
     - the release absence passes;
     - the two lead repetitions agree run by run on `normalizedSha256` and on the trace digest, the trust store (`logical.trustState`) included (r2) (**r14:** the trace digest with r14's object-publication group order);
     - (r2) every run's labels include `scripted-clock`, and every child's ordinal follows spawn order.
   - **r10:** the reviewed required runs are two files: storage's, and `crates/host/tests/fixtures/crash-matrix/required-runs.v1.json` for X9-5's rows. X9-6's `check` takes both files and both pairs of run sets, and checks the union census (see the r10 header).
     **r16:** a row's `unit` member may name `"X9-6"`; such a row is in no unit's `check-unit` subset and is required by `check` (see the r16 header).
     **r17 (§RC):** a row's `unit` member may also name `"X3c-3"`, with the same reading. X3c-3's `check` lists `x3c.object/file-barrier.before#41` and `.after#41` in `killedOutsideKillSet` (see §RC.3).
   - **The per-unit check (r4; lead decision).** Before X9-6, each of X9-2 to X9-5 checks its own run sets with a subset mode of the checker.
     - **Who adds it.** X9-2 adds it to `tools/check_crash_matrix.py` as the `check-unit` command, with its tests.
     - **The unit's rows.** `check-unit` names the unit (X9-2, X9-3, X9-4 or X9-5). It takes that unit's subset of the reviewed `required-runs.v1.json`: the rows whose case is in the unit's list in item 12.
       **r15:** a row with a `unit` member is in that unit's subset only, whatever its case; F14's moved row carries `"unit": "X9-4"` (see the r15 header).
     - **What it checks** on two lead run sets. It refuses unless all of these hold:
       - every subset row has exactly one run in each set, and no other run exists;
       - `check`'s per-run check passes on each run (canonical JSON, schema, verdict PASS, labels, units, script and expected equal to the row, the clock and ordinals, and kill verification by signal 9 and `lastHeld`). The one difference: `product.commit` must equal the stated base commit, and `worktreeClean` may be `false`, because a unit is reviewed uncommitted;
       - the census names only registered scopes, with their durability;
       - the kill set equals the one derived from the census;
       - every killed point of the unit's runs is in the kill set;
       - the release absence passes;
       - the limits are exactly L1 to L10 (**r12 (record):** L1 to L11, as r8 set);
       - the two sets agree run by run on `normalizedSha256`, the trust store included, and on every child's trace digest, and they agree on the census (**r14:** each trace digest with r14's object-publication group order).

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

   **r12:** F36 adds **R5**: `recover` of R2's own ExecutionId, and whether the orphan SEAL and R2's SEAL name one RunId. In F13, F14 and F15, R2 commits the distinct candidate variant (see the r12 header).
   **r17 (§RC):** in re-commit rows, R2 commits the same candidate (`{"r2": "same"}`), and a row may recover its first commit after the ladder (`e1-recover`). R5's one-RunId check holds when every SEAL of the carrier names one RunId (see §RC.2 and §RC.7).

   **Exceptions.**
   - **Mutation rows** run R1 and R2 only, because the injected condition persists.
      **r14:** F25 runs R1 only (see the r14 header).
   - **Runs without an ExecutionId** skip R1 and R4 and record `"notApplicable": "no-execution-id"`. The ExecutionId comes from the `x3d.session.execution-draw` pass record.
   - **Every lawful run** also asserts the release order line 608 requires, from its trace: level 4, then each level-3 transaction, then the lease, then the fence.
     **r16:** every commit child of every run, storage and host, is checked for the fixed acquisition order (journal level 3, ledger level 3, level 4) and the release order (evidence COMMIT, level 4, level 3, writer lease, end fence); a violation makes the run FAIL, like R1's `stateUnchanged` (see the r16 header).

   Abbreviations in item 9: CH committed-historically, CAD committed-availability-degraded, TNC terminal-not-committed, UAO unknown-attempt-open, UAU unknown-attempt-unobserved, UC unknown-custody, UQ unknown-quarantine-condition, UB unavailable-busy, BU binding-unusable, UCI unknown-carrier-incompatible.

9. **The matrix.** Every row runs on this macOS 27 host under item 6's synthetic fixture.
   - **Status values.** "exec" means executed here. "exec (inj)" means executed with an injected stand-in (item 4). "exec (mut)" means executed over a parent mutation. "elsewhere" means it is covered by an accepted law's in-process test and is not a process-level case. "LIMIT" means recorded and not executed (item 10).
   - **Expected values.** They come from the build plan's row and the owning law. X9-a units transcribe each row into `required-runs.v1.json` before any run. An expected value is never read back from a run.
   - **r17 (§RC):** X3c r8's re-commit rows are `recommit-` variants of F04, F11 to F15, F23, F29, F33 and F52, with `"unit": "X3c-3"`. They are §RC's rows. No row of this table changes (see §RC.4 and §RC.5).

   | Case | Owner | Injection | Status | Expected |
   |---|---|---|---|---|
   | F00 | X2, X3a, X3b, X4T-b | `hold`→kill at every census point before `x3c.attempt.commit.after` (X4T floor, X3b floor, INIT, start witness, leases) | exec | No attempt row; ledger logical state unchanged. R2: the floor step and start handle X3b item 3a's or item 4's crash state (INIT resumes or finishes, REVERT, ADVANCE), then Committed. With an ExecutionId drawn: R1 and R4 UAU, R3 writes nothing. **r5:** expected by kill point: before the draw, R1 and R4 not applicable; from the draw through `x3c.ledger-create.ddl.commit.before`, R1 UC (`ledger-missing` or `ledger-unreadable`, X6 F24) and R4 UAU; from `x3c.ledger-create.ddl.commit.after` (included, r6) until `x3c.attempt.commit.after`, R1 and R4 UAU. R3 writes nothing (see the r5 header). **r8:** R2 is the owning law's outcome for the crash state at the kill point: the registration window (X2 item 8 identity rows), the created-not-yet-private windows (custody, host I/O, and for an X4T dependency occurrence (r9) `CONFIG.CUSTODY_REFUSED` `installation-incomplete` when the next publication writes its name, Committed when it does not), the WAL gap (`LEDGER.CORRUPT`), and Committed everywhere else. R4 stays UC where R2 does not create the ledger (see the r8 header; L11). |
   | F01 | X5 | replay-invalid candidate; substituted target or inventory | exec (host) | Refused before `prepare_commit`; no attempt row; no SEAL; ledger and carrier logical state unchanged. **r13:** the replay-refused variants leave the whole post-state unchanged; the substituted variants add only the latched gate's one `REV` to the carrier (see the r13 header). |
   | F02 | X3c | `torn` at `x3c.object.write` (first, middle and last object) | exec (inj) | Staging residue is never adopted. R1 UAO; R2 Committed; R3 refused; R4 TNC. The orphan stays (L6). **r16:** also killed at `x3c.object/create.before`, `create.after` and `write.after` (first, middle, last), as F02 (see the r16 header). |
   | F03 | X3c | kill at `file-barrier.before` and `.after` | exec (death branch; L1) | As F02. |
   | F04 | X3c | kill at `link.before` and `.after`; R2 republishes the same digest | exec | As F02. R2 confirms the existing object by exact bytes. An unequal-collision mutation variant refuses on X3c item 10's row. |
   | F05 | X3c | kill at `directory-barrier.before` and `.after` | exec (death branch; L1) | As F02. |
   | F06 | X3b, X3c, X3d | the parent holds a raw SQLite `BEGIN IMMEDIATE` on the carrier, or on the ledger, while the child runs `publish` (labelled `mutation`: a foreign holder) | exec (mut) | Busy row (`LEDGER.BUSY_TIMEOUT`/`PROJECT.BUSY`); an earlier level-3 transaction is released; no SEAL; orphans preserved. R1 UAO; R2 Committed after the holder ends; R3 refused; R4 TNC. |
   | F07 | X3b | kill at each `x3b.append.seal.witness-pending/*` point and at `insert.before` | exec | R1 UAO, diagnosis would-REVERT; R2 REVERT, Committed; R3 refused; R4 TNC. **r5:** R1 is plain UAO; would-REVERT is R2's witness action only (see the r5 header). **r8:** R2's witness action is OK before `witness-pending/rename.after` and REVERT from it on (see the r8 header). **r16:** also killed at the SEAL append's prefix (`begin`, `x3c.evidence.begin`, `level-four`, the first checkpoint's four points, `built`), with R2 OK (see the r16 header). |
   | F08 | X3b | kill at `insert.after` and `commit.before` | exec | SQLite rolls back on reopen. As F07. |
   | F09 | X3b | kill at `commit.after`; `fail-after` and `fail-before` at the SEAL `commit` | exec; exec (inj) | Injected: `CommitUndetermined` (`DURABILITY.COMMIT_FAILED`); nothing appended; no evidence `COMMIT`; the settlement reserve is forfeited. R1 UAO with would-ADVANCE (landed) or would-REVERT (not landed); R2 ADVANCE or REVERT, Committed; R3 refused; R4 TNC. **r5:** R1 is plain UAO; landed or not landed shows only as R2's ADVANCE or REVERT (see the r5 header). |
   | F10 | X3b | kill at each `witness-committed/*` point | exec | R1 UAO, would-ADVANCE before the rename survives, OK after; R2 ADVANCE or OK; R3 refused; R4 TNC. **r5:** R1 is plain UAO; would-ADVANCE or OK is R2's witness action only (see the r5 header). |
   | F11 | X3c, X3d | kill after each `x3c.evidence.stage-<table>` | exec | The ledger transaction rolls back; the SEAL is durable with no `REV` (the process died before `finish`). R1 UAO; R2 Committed; R3 refused; R4 TNC. **r16:** also killed at every point from the second checkpoint to `x3c.evidence.commit.before` (12 points), with R2's witness action OK (see the r16 header). |
   | F12 | X3c, X3d, X7 | `fail-after` and `fail-before` at `x3c.evidence.commit` | exec (inj) | `CommitUndetermined` with ExecutionId and no RunId; no retry; nothing appended. R1 CH with pendingSettlement (landed) or UAO; R3 committed or refused; R4 CH or TNC. |
   | F13 | X3c, X3d | kill at `x3d.publish.commit-returned` | exec | R1 CH with pendingSettlement; R2 Committed; R3 committed; R4 CH. **r12:** R2 commits the distinct candidate variant, so it is Committed (see the r12 header). **r16:** also killed at `x3c.evidence.commit.after` and the SEAL's level-4 and level-3 releases (see the r16 header). |
   | F14 | X3d, X6 | kill at `x3d.publish.published` and at `x3d.finish.settle.before` | exec | As F13. **r12:** R2 as F13. The `x3d.finish.settle.before` kill moves to X9-4, after F39's script, where an end record is owed (see the r12 header). **r15:** that row is X9-4's (`"unit": "X9-4"`); its R2 is refused at admission (C5), not scored, as r13 has for F39 (see the r15 header). **r16:** also killed, as the `published` kill, at the writer lease's unlock, `x3d.finish.lease-release`, `end-step.before` and the end fence's lock (see the r16 header). |
   | F15 | X6 | kill after `x3d.finish.end-step.after` | exec | R1 CH; R2 creates no second receipt for this ExecutionId. **r12:** R2 commits the distinct variant: Committed, with no second receipt for this ExecutionId (see the r12 header). |
   | F16 | X7 | `fail-before` at `x7.delivery.required` | exec (host, inj) | `DELIVERY.REQUIRED_FAILED`, exit 4, runId kept; R1 CH. **r16:** also a host kill at `x7.delivery.required.before` and `.after`: the Run stays committed, R1 CH `pendingSettlement`, R3 committed, R4 CH (see the r16 header). |
   | F17 | X7 | `fail-before` at `x7.delivery.optional` | exec (host, inj; L9) | Committed; optional failure disclosed; result unchanged. **r16:** also a host kill at `x7.delivery.optional.before` and `.after`, as F16's kills; L9 is unchanged (see the r16 header). |
   | F18 | X4, X3d | `hold` at `x4.checkpoint.before-observation#1`; the parent publishes a revoking update, or makes the view unreadable or mixed; resume | exec | Refused `TRUST.COMPONENT_REVOKED_DURING_OPERATION`, or `OBSERVER.FAIL_STOP`; no SEAL; `finish` appends `REV` from the settlement reserve. R1 UAO; R2 refused at admission (revoked), or Committed after the view is restored (fail-stop variant); R3 and R4 per C5. **r15:** the mixed view is elsewhere (X4a's `a_replacement_during_the_first_attempt_is_absorbed_and_a_second_is_mixed`); the unreadable view is `state.v1` at mode `000`, restored before the ladder (see the r15 header). |
   | F19 | X3b, X3d, X4 | as F18 at the repeated checkpoint after the SEAL (`#2`); also kill at each point of the end-path `REV` append | exec (stall variant: L3) | Refused; evidence transaction rolled back; the trace shows level 4, then level 3, then a fresh `x3b.append.rev`, then `CLN` if owed. A killed `REV` leaves X3b's append crash state. R1 UAO; R3 and R4 per C5 (or refused and TNC in the fail-stop variant). **r16:** after the revocation, also killed at `x4.gate.latch.after#1` and `x3d.finish.settle.after#1`, as the `REV` kills (see the r16 header). |
   | F20 | X6, X3b | the parent rewrites the witness as malformed or with a mismatched digest | exec (mut) | R1 UQ after the five stable observations; R2 quarantine row (`LEDGER.CORRUPT`). |
   | F21 | X6, X3b | the parent deletes the witness of a nonempty journal | exec (mut) | R1 UQ (`witnesslessRestore`); R2 quarantine row. |
   | F22 | X6, X3b | the parent restores a carrier copy taken at an earlier `hold`, under a newer floor; or equal seq with a different hash | exec (mut) | R1 UQ; R2 quarantine (floor regression or `uncertainTailLoss`). |
   | F23 | X6 | the parent deletes the receipt row, or the association row | exec (mut) | R1 UC; R3 writes nothing (one-sided). |
   | F24 | X6, X3a | ledger mode `000` or a truncated header; a wrong store generation selected | exec (mut) | R1 UC; R2 refused on its X3c or X3a row; R3 reports host I/O for that namespace and writes nothing. **r12:** the wrong-store-generation variant (every row's digest changed, the ledger readable) gives R1 UAU, R2 Committed, and R3 `swept` with nothing written, per the owner's §2 matrix (see the r12 header). |
   | F25 | X6 | the parent deletes, or flips one byte of, a committed object | exec (mut) | R1 CAD with `evidence.missing` or `evidence.corrupt`. **r14:** both variants run R1 only; R2 would re-commit the same Run at a drawn position (see the r14 header). |
   | F26 | X4, X6 | commit, then the parent publishes a revocation | exec | R1 CH; R2 refused at admission; no grant reused. **r15:** "no grant reused" is R2 refused at admission and leaving the project's own state unchanged (see the r15 header). |
   | F27 | X6 | the parent swaps the association's namespace, generation, operation or execution; or a request with a different binding | exec (mut) | R1 BU. **r12:** the association's operation and execution swaps give R1 UC `ledger-join` (the snapshot's join); the store-generation and namespace swaps, and a request with a different binding, give BU (see the r12 header). |
   | F28 | X6 | X6a's pruned-record fixture, read in a fresh process | exec (mut) | R1 UC. |
   | F29 | X6 | a reader process while the writer holds at `x3c.attempt.commit.after`, after the SEAL, at `x3d.publish.after-staging` and at `commit-returned` | exec | UAO, UAO, UAO, CH with pendingSettlement; never mixed; the reader takes `readers.lease` alongside APPEND-WRITE without waiting. |
   | F30 | X2, X6c | writer A holds (a) under its lease after the fence is released and (b) while it holds the fence; process B is a competing writer; process C is the sweep | exec | B: the busy row after S7's bounded fence or lease attempt, no upgrade, no state change. C: skips and retains the namespace. After A resumes, A is Committed, and a second B then succeeds. **r15:** the second B commits r12's distinct variant; in (a), B's "no state change" compares the project's own state and its lawful trust-floor publication is recorded; in (b), C is refused at its own admission on the busy row and writes nothing (X6 r4 item 7 step 1) (see the r15 header). |
   | F31 | X3b | the parent installs the format-1 or format-2 fixture as the namespace's carrier | exec (mut) | R2 refused before commit work (X3b item 3a's F46 row); no SEAL is inserted. |
   | F32 | X3b-4, X7b | reserved-slot setup to tails `…987` and `…988`; kill at each X3b item 13 crash-table point | exec (host; mut + death) | `CarrierCapacityExhausted`; `finish`; the rollover in the end step; X7 r3 item 6a's busy row. Each crash row as X3b item 13 states; the next writer proceeds in G+1. **r13:** the `…987` variant's R1 and R4 are `unknown-quarantine-condition:journalContiguity` (the planted tail is not contiguous from 1), and its R2 commits the distinct variant (see the r13 header). |
   | F33 | X6 | the parent alters receipt bytes, the inventory, a signature, or the SEAL body digest | exec (mut) | R1 UC. |
   | F34 | X3d, X6 | (r2) run A: `inject-id` with a previous run's ExecutionId; then run B, a separate `recover` process, once with A's disclosed requested binding and once with the earlier attempt's own binding | exec (inj) | A: `ExistingAttempt`, projected on the invariant row (`SYSTEM.OUTCOME.ILLEGAL_STATE`, `HOST.INVARIANT_VIOLATED`) with the ExecutionId as subject and the requested binding disclosed (X6 r3 item 6, X7 r4 item 3); no new row, no SEAL, no recover in A; the earlier attempt's rows unchanged. B: with A's binding (a different `operationRef`), BU (`RECOVERY.REFUSED`, subject `operation`); with the earlier attempt's binding, that attempt's standing. B leaves `normalizedSha256` unchanged. **r15:** across A, N's ledger is unchanged and no SEAL is added; the carrier gains the latched gate's one `REV` (r13), unscored (see the r15 header). |
   | F35 | — | — | LIMIT (L5) | — |
   | F36 | X3b, X3c, X6 | the orphan SEALs of F09, F11, F19 and F38, followed by R2 committing the same semantic RunId | exec | The earlier ExecutionId: R1 UAO, R3 refused, R4 TNC. The later ExecutionId: CH. The RunId is not blacklisted. **r12:** F09 and F11 only; the F19 and F38 variants do not exist, because R2 is refused under the revoked view. The later ExecutionId is ladder step R5 (see the r12 header). |
   | F37 | X6 | — | elsewhere (X6 item 10: the pure ordering accessor) | — |
   | F38 | X3d, X4 | `hold` at `x3d.publish.after-staging`; the parent revokes; resumes `x4.observer.tick#1` and awaits `x4.gate.latch.after`; resumes the main thread | exec | The gate goes 0→2; no permit; staged transaction rolled back; `REV` and `CLN` from the reserve. R1 UAO; R2 refused at admission; R3 and R4 per C5. |
   | F39 | X3d, X4, X7 | `hold` at `x4.gate.admit.after`; revoke; observer tick; latch 1→3; resume | exec (storage half; host half in X9-5) | Committed with `latchedAfterAdmission`; host projects `DELIVERY.REQUIRED_FAILED`; R1 CH. **r12:** the admission hold is `x3c.evidence.commit.before#1`, the first point after the shared monitor is released (see the r12 header). |
   | F40 | X3d, X7 | as F12, with and without F39's latch | exec (inj) | `DURABILITY.COMMIT_FAILED`, ExecutionId, no RunId; the latch does not convert it. The ladder as F12. **r13:** the latch variant runs landed only, with r12's F39 hold; the not-landed latch variant is covered by F40 without the latch and by X4's gate-trace test (see the r13 header). |
   | F41 | X4, X3d | the two process-level orders: latch before admission, and admission before latch | exec (two orders); every interleaving is covered elsewhere (X4's gate-trace test) | At most one `x3c.evidence.commit` in the trace; the gate stays in 0..3. |
   | F42 | X3d | abort is every kill above; the child driver `mem::forget`s its `StoppedSession` and exits; a held point with a reader running | exec (kernel stall: L3) | Forget: the kernel releases the lease, the attempt stays admitted, R1 UAO. The reader during a hold: UB or UAO. Never a claimed cleanup. |
   | F43 | X6 | tail-lost variant: after a commit, the parent truncates the journal tail below the association's `journalSeq` (reserved-slot technique) | exec (mut); the reconciling-retry variant is elsewhere (X6 item 11's hazard test) | R1 per the F43 rule: UB attributed to the carrier owner, or the F22 condition when the floor is at or above the requested sequence and two tail observations agree; never uncommitted. |
   | F44 | X6 | attempt A runs F39's script (Committed, gate latched after admission), so its `finish` owes a `REV`; A holds at `x3b.append.rev.witness-pending/directory-barrier.after`; a reader process recovers A's ExecutionId. A's SEAL is above the floor its own floor step wrote | exec | UC, not invalidated; diagnosis witnessWouldRevert; no REVERT, ADVANCE, witness write or floor raise; no wait on A. **r12:** F39's script with the r12 admission hold; the revoked subject is the session's core closure (see the r12 header). |
   | F45 | X6 | as F44, with A holding at `x3b.append.rev.commit.after` | exec | CH under witness-pending-at-tail, with `interior-bodies-not-authenticated`; diagnosis witnessWouldAdvance; no write. **r12:** as F44. |
   | F46 | X6 | the format-1 or format-2 fixture, or an association below `first_generation` | exec (mut) | R1 UCI. **r8:** the association-below-`first_generation` variant is not executed in M2 (a fresh carrier's first generation is 1; L5; see the r8 header). |
   | F47, F48, F50, F51 | — | — | LIMIT (L5) | — |
   | F49 | X6 | (a) a reader holds between bracket reads while a lawful writer appends, then resumes; (b) writer A holds at `x3c.attempt.commit.after`, a reader of A's ExecutionId holds at `x6.recover.after-ledger-snapshot`, A is resumed to Committed, then the reader resumes | exec | (a) UB, never UQ, never a corruption diagnosis; (b) UAO or UB from the one stale snapshot, never TNC. **r12:** (a) is CH with `pendingSettlement`: the owner's one fresh capture reconciles the moved tail (see the r12 header). |
   | F52 | X6 | the four lawful cells from earlier runs (admitted/none, admitted/both, settled-committed/both, settled-refused/none); the other seven by mutation | exec, exec (mut) | X6's §2 matrix; exactly one cell gives TNC. |
   | F53 | X6c | live (a held writer), crashed (killed runs), one-sided (mutation), inaccessible (mode `000`), already settled (a second sweep); also kill the sweep at `x6.sweep.settle.commit.before` and `.after` | exec | X6 r2 item 7: skip, settle, or write nothing. After a killed sweep, the next sweep settles each row exactly once (the monotone trigger). **r16:** the sweep is also killed at its readers lease's lock and unlock, `after-exclusive` and `after-snapshot` (see the r16 header). |

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
    - **L11 (r8). Permanently refused crash states.** An interrupted first registration (X2 item 8's identity rows), a created owner not yet sampled private (custody, host I/O, or (r9) `CONFIG.CUSTODY_REFUSED` `installation-incomplete` for an X4T dependency that the next publication writes), and a partial ledger WAL (`LEDGER.CORRUPT`, X3c item 10) leave the project refused until a repair or resume writer exists. F00 records each outcome. The later owner is M3, a repair or resume writer.

11. **Lock contention (F30) and live revocation, deterministically.**
    - **Contention.** Writer A holds at a named point, so its lease, and optionally the fence, is held for as long as the parent wants. The parent then spawns B, C or a reader as fresh processes and reads each one's outcome. Each peer meets a holder that cannot release, so its non-blocking `LOCK_NB` attempt, or the product's bounded fence wait, has exactly one outcome. The parent then resumes A and reads A's outcome. No step depends on timing, and none sleeps.
    - **Revocation.** Every child arms `x4.observer.tick#*=hold`, so the observer ticks only when the parent resumes it.
      - **Order of the parent's steps.** The parent holds the main thread at the named checkpoint or gate point, publishes the trust change (item 6's helper, under the fence, which the held child does not hold after its handoff), and resumes either the main thread (the checkpoint's own monitored read observes it) or one observer tick, awaiting `x4.gate.latch.after` before resuming the main thread.
      - **Why it is deterministic.** Which party latches, and in which gate state, is fixed by the script.
    - **Timing guard.** A held child's awake time counts against X4's 10 s bound. Each run records the monotonic time from the operation's first monitored read to its last checkpoint. A run above 2 s (**r13:** 5 s, measured as r12 states; see the r13 header) is a `HARNESS-ERROR`, never an `OBSERVER.FAIL_STOP` that the run then accepts.
      **r12:** it applies to every run that arms `x4.observer.tick`. It is measured on the parent's monotonic clock, from the writer's first `x4.observer.tick` hold record to its hold at the script's admission-hold point, and recorded as `timingGuard`. X9-3 implements it for F44 and F45, and X9-4 uses it (see the r12 header).
      **r15:** the window ends at the writer's first hold at a point other than the observer tick, the script's own main hold; F18 and F19 resume the held tick after reading `x3d.finish.settle.before#1` (see the r15 header).
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
      **r12:** X9-3 also adds the distinct candidate variant, R5, the timing guard with its `timingGuard` member in the run writer and the checker, and the F39 script with the r12 admission hold for F44 and F45. Its F14 is the `published` kill only, and its F36 is F09 and F11 only (see the r12 header).
      **r14:** X9-3 also adds r14's object-publication group order to the matrix target's trace digest, and runs F25 with R1 only (see the r14 header).
    - **X9-4 (storage; locks and live revocation).** Rows F06, F18, F19, F26, F30, F34, F38, F39's storage half, F40 and F41, and C5 once G5 is decided (**r3 (record):** decided by X6c; C5's R3 is `refused` and its R4 is `terminal-not-committed`). **Dependencies:** X9-2 and X4a. It uses X4a's observer `gate` point.
      **r12:** X9-4 also takes F14's `x3d.finish.settle.before` kill, in an owed-end-record run after F39's script. It inherits the r12 admission hold and X9-3's timing guard (see the r12 header).
      **r15:** X9-4 also adds its census's refused-end run, the required run's `unit` member in the checker (`check-unit` and `check`) with its tests, and the timing guard's general end point (see the r15 header).
    - **X9-5 (host).** `crates/host/tests/commit_matrix_tests.rs` with rows F01, F16, F17, F12's and F40's caller route, F32 with its rollover crash table, F39's delivery half, and F53's `store-gc` step. **Dependencies:** X9-2, X5a, X7a, X7b, X3b-4 and X6c.
      **r10:** X9-5 adds host's two runners, the candidate file's writer and reader, and the fixed delivery phase. It also adds the `candidate` and `finalize` children (host order: the candidate is written before custody), the host required-runs file and the host census of two `finalize` runs and (r11) one `store_gc` run. It depends on X3d-3 too (see the r10 header).
      **r13:** X9-5's host rows start from the `candidate` child's INIT and one `REV`; R2 commits r12's distinct variant after a committed Run; F40's latch variant runs landed only; the timing guard's limit is 5,000 ms (see the r13 header).
    - **X9-6 (record; the M2 exit).** Two full lead runs on one integrated commit, the checker, release absence, the reviewer's rerun, and the arch evidence record. **Dependencies:** all of the above, and VD1 (EXIT-PLAN, "lands before the X9 exit").
      **r10:** X9-6's `check` covers both required-runs files and both targets' run sets, with the union census and kill-set coverage across both (see the r10 header).
      **r16:** X9-6 also adds the storage driver over every storage row with its union census, the checker's two-target `check` and `coverage`, the `"X9-6"` unit value, item 8's release-order verdict condition, and the 50 kill rows of the r16 header (storage 381 rows, host 98) (see the r16 header).
    - **X3c-3 (r17, §RC; X3c r8 item 13; not an X9 unit).** It transcribes §RC's 22 rows into storage's file, adds the `recommit` census part and the harness and checker members of §RC.7, and runs one serialized lead set on both targets (see §RC.6).

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
- (r10) A host runner that returns or lends an authority type; that accepts a receipt, gate, guard, monitor, clock, session, permit, `ProjectOperation`, `ReplayedRun`, delivery phase or callback from its caller; or that is compiled under `scenario-fixtures` or in any release build. A third runner. A runner call in a process that already made an entry, or a second runner call.
- (r10) A copy of host's `finalization.rs` or `maintenance.rs` compiled into a test target. `finalize` or `maintenance` made public. Host's matrix children run in host's unit-test binary.
- (r10) A host matrix child that replays its candidate after admission. A candidate built without a `CommitSession`.
- (r10) Native admission (`SettlementSweep::admit`, `sweep_store`, `RecoveryAdmission::admit`) in any matrix process.
- A `cfg(any(test, feature))` site outside X9-1's pinned list.
- Asserting either refusal or admission of a whole-file `state.v1` restore (L4).
- A durability primitive reached outside a named scope during a matrix run.
- An observer that ticks on its own timer in a matrix child.
- (r2) A wall reading from the OS in any process of a matrix run, a scripted wall reading in a build or process without the feature and `OPENSIP_X9_CLOCK`, or a scripted monotonic clock.
- (r2) A `recover` call inside F34's injected writer run.
- Raw state bytes committed to arch in place of the run records.
- A matrix pass on a dirty worktree, or on a commit other than the reviewed one. **r4:** a unit's `check-unit` (item 7) is not a matrix pass.
- (r17) A section of r17 that changes another section's rows, or that re-transcribes a row of r16 or earlier which its owning law does not require (the r17 section frame, rule 2).
- (r17, §S12) A matrix signal sent by `kill(2)`, after a timed wait, or on a held thread; a signal step acknowledged by a crash point, or resumed before its acknowledgement; a matrix runner whose cancellation source is not host's own.

## Not claimed

Power-loss and media qualification, native S6 scheduling bounds and the residual admission window (M6); store and carrier migration and restore; orphan object collection; a measured platform profile row; Linux and non-APFS hosts; X8's compile-fail suite; CLI enablement (X10, X11); any new public code, row or detail; closing X4T r9's whole-file restore limit.

## X9 r17 sections

### The section frame (r17 round 1; LD-17-1)

Each section of r17 is the X9 record of one owning law's rows. These rules apply to every section.

| Section | Owning law and items | Unit that transcribes and runs it | Needed before | Status |
|---|---|---|---|---|
| §RC | X3c r8, items 13 and 14, CL-2 (X3C:252-261, :262-325, :354) | X3c-3 | X3c-3's code (X3C:259; M3P:319) | Round 1, this round |
| §S12 | J1 r5, item 12 and successor S12 (J1:832-841, :858) | J3b (S12-B, -C, -U, -D) and J3d (S12-O) | J3b's review; S12-O before J3d's O wiring (M3P:319) | Round 2 (not accepted) |
| §RW | J-RW, item 10, X-RW-10 and RW-S6 (JRW:519-596, :625, :669) | J4e | J4e (JRW:607; M3P:319) | Reserved; J-RW in review |

1. **Transcription.** A section's code unit transcribes the section's rows into the reviewed required-runs files before any run of that unit. It works from the section and the census only (X9:717). An expected value is never read back from a run (X9:1089, :1233).
2. **No section changes another's rows.** A section adds its own rows and changes no row of another section (X3C:354; M3P:319).
   - A section re-transcribes a row of r16 or earlier only where its owning law requires it. It lists each such row by case and variant, with the old and the new value. J1's host drivers (J1:832) and J-RW's RW-F00 (JRW:519-596) are such re-transcriptions. §RC has none (§RC.5).
   - If two sections would re-transcribe one row, the later round stops and reports.
   - Where a section's census part moves an existing row's place in the kill set, the section records the move and leaves the row as it is (§RC.3).
3. **Selection.** Each row a section adds carries a `unit` member naming the section's code unit. Such a row is in no X9 unit's `check-unit` subset, and `check` requires it. That is r16's reading of `"X9-6"` (X9:725-732). Each section names its value, and the checker admits it. A re-transcribed row keeps its own selection.
4. **Census parts.** A section that adds a census part names it and states its composition and its checks. It records every kill-set point the part adds or removes. The union is r10's: each name at its largest occurrence count (X9:234).
5. **Lead sets.** `check` requires every row of both files (X9:1032), so a lead set on a commit runs every row of both files at that commit, whatever its section. Whichever of two section units integrates second reruns both sections' rows (X3C:261; JRW:668).
6. **Rounds and snapshots.**
   - Each round is reviewed on its own. Its acceptance is recorded beside its section's heading.
   - A round's accepted bytes are preserved, without the acceptance note, as `PROPOSAL-r17-<section>.md`: `-rc` first, then `-s12` and `-rw` in the order they are accepted. When the third section is accepted, its snapshot is also preserved as `PROPOSAL-r17.md`.
   - Each later round's diff base is the previous round's snapshot.
   - While r17 is open, a correction to an accepted section is a new round of that section. Once all three sections are accepted, a correction is r18.

### §RC. The re-commit section (X3c r8 item 14; unit X3c-3)

**Round 1, 2026-10-04. Not accepted.**

#### RC.1 What §RC carries and what it decides

- **Its law.** X3c r8 decides what r12 left undecided (X9:268). A Run already committed in (S, N) is committed again by a new attempt, which ends `Committed` (X3C:105-109). Item 14 names the windows where a re-commit differs from a first commit: its objects are confirmed, staging takes the re-commit branch, and its landed `COMMIT` adds attempt rows only. It also names the rows RC-1 to RC-9, the census child and the record of 19 runs (X3C:262-325). CL-2 puts them here (X3C:354).
- **What §RC fixes,** as item 14 asks (X3C:263):
  - the rows' `case` and `variant` spellings (RC.2, RC.4);
  - their scripts and expected values, each derived from X3c r8's row text and the owning X9 row, never from a run (RC.4);
  - the census part for RC-1's census child, and its effect on the kill set under item 5 and r10 (RC.3);
  - the record of the 19 runs, with each run's outcome under X3c r8 (RC.5);
  - X3c-3's lead-set duty (RC.6), and what X3c-3 adds to transcribe and run the rows (RC.7).
- **What §RC does not decide.** It changes no X3c, X3d, X6 or X7 outcome. Where X3c r8 states an expectation, §RC spells it. Where X3c r8 leaves a spelling open, §RC takes it from X9's existing rows and records a lead decision (LD-RC-1 to LD-RC-7).
- **Its basis.**
  - Product main `d2c00a9`, read only. X3c-3's code does not exist yet, so no census or run has re-committed a Run.
  - Every census figure below is C's: `3d2d5b5`, `evidence/3d2d5b5…/storage/census-trace.txt` (`c82cf452…`) and `matrix.json`.
  - X4-F1's and X4-F2's X9 regressions found both censuses unchanged since C: storage 259 points, host 218 (OVERNIGHT:312, :612). X3a-2 (`cca4fe4`), a read-side change, has had no census run.
  - Where §RC predicts a census or a run, the prediction is the code's and the law's. X3c-3's census-only run checks it before any row runs (RC.6).

#### RC.2 Spellings and conventions

| Member | RC rows | Basis |
|---|---|---|
| `case` | The F-case each row extends. X3c r8's parenthesis names one case for RC-3, RC-6, RC-8 and RC-9, and two or three for RC-2, RC-4 and RC-5. LD-RC-1 fixes RC-1, RC-2 and RC-7, and splits RC-4 and RC-5 | X3C:263; the checker's case grammar `F[0-5][0-9]` (`tools/check_crash_matrix.py:257`) |
| `variant` | `recommit-` followed by X9's existing spelling for the same kind of run: `kill-<point slug>-<k>` (X9:698), `fail-before-evidence-commit` and `fail-after-evidence-commit` (F12), or the mutation's name (F33, F52). A short name is used where no row of that kind exists | X3C:263 |
| `units` | `["X3c"]`: the law whose item 14 owns the row | `units` names owning laws (X9:532) |
| `unit` | `"X3c-3"` (LD-RC-3) | frame rule 3 |
| `labels` | Item 4's labels: `process-death` for a kill, `injected` for `fail-*`, `mutation` for a parent mutation. Every row also carries `scripted-clock` and `synthetic`. They are sorted, as the file sorts them | X9:915, :879 |
| `script` | X9-3's step form for every row (LD-RC-2) | `commit_tests.rs:1775-1817` |
| Expected spellings | Each outcome, standing and end as X9's existing rows spell it: `Committed(latched=false)`, `CommitUndetermined`, `Refused(Invariant)`, `Refused(LedgerCorrupt)`, `killed`, `unknown-attempt-open`, `terminal-not-committed`, `committed-historically:pendingSettlement:*`, `committed-historically:settled:*`, `committed-historically:*`. A `:*` suffix matches any further detail (`meets`, `commit_tests.rs:1112-1123`) | the F11 to F15, F29 and F36 rows |

**Notation** (X3C:264). These child names are used in every RC script:
- `e1` is E1, the candidate's first commit in (S, N).
- `e2` is E2, the re-commit under test, of the same candidate.
- The ladder's R2 is E3, a next writer that commits the same candidate. Its ladder step carries `"r2": "same"`, beside r12's `"r2": "distinct"` (X9:264).
- `e1-recover` is X3c r8's extra read-only step "recover(E1)": a `recover` child `for` `e1` after the ladder. Like r12's R5 (X9:1076), it is its own process with a plain request.
- `d` is RC-7(b)'s commit of r12's distinct variant.

**Lead decision LD-RC-1: the case of RC-1, RC-2 and RC-7.** X3c r8 names the F-case for the other rows. RC-4's two rows are F12's, because F40's no-latch rows run F12's scripts (X9:626), and RC-4 has no latch. RC-5's rows take F13, F14 or F15 by kill point, as r16 placed `x3c.evidence.commit.after#1` under F13 (X9:708).
- **RC-1 is F15.** F15 is the committed, acknowledged Run whose later process must not create "a second receipt for the same attempt" (X9:1108). RC-1's E2 is that later process. It has its own receipt, and E1 still has one.
  - **Rejected: F36.** F36 is an orphan SEAL's later commit, which RC-3's R5 already extends.
  - **Rejected: F34.** F34 is a request for the same ExecutionId, which a re-commit never reuses (X3C:113).
- **RC-2 is F04.** X3c r8 says "F02 to F05". Every RC-2 point lies in the confirm branch, which is F04's "verify existing collisions by exact digest/length" (X9:1097). **Rejected:** a case by step name, such as F03 for the barrier. The barrier killed is the confirm branch's own, not the staging file's.
- **RC-7 is F23.** F23 is the build plan's one-sided case, and RC-7 is its per-Run counterpart (X3C:121; X9:1116).
  - **Rejected: F33.** F33 is a changed join, which RC-6 extends.
  - **Rejected: F52.** F52 is the attempt-row matrix.

**Lead decision LD-RC-2: every RC row uses the step form.** Every RC row commits E1 before the child under test, and several add a child after the ladder. X9-2's form has one scripted child (`commit_tests.rs:1659-1768`). The step form names each child (`:1818-2160`). **Rejected:** a new X9-2-form directive for a leading commit, which would add a second way to write the same script.

**Lead decision LD-RC-3: `"unit": "X3c-3"`.**
- **Why a `unit` member.** Every RC row's case is in an X9 unit's case list. Without the member, X9-2's, X9-3's or X9-4's `check-unit` would demand the row. r10 and r15 avoid that (X9:218, :523).
- **Why this value.** It names the unit that transcribes and runs the rows. The checker adds it to `UNIT_VALUES` (`tools/check_crash_matrix.py:105`) with r16's reading of `"X9-6"` (frame rule 3).
- **Rejected: `"X9-6"`.** It would name the M2 exit unit as the owner of an M3 unit's rows.
- **Rejected: no `unit` member,** for the reason above.

**Lead decision LD-RC-4: `"r2": "same"`.**
- **What it does.** The harness's R2 already commits the candidate unless the directive says `distinct` (`commit_tests.rs:1753`, `:2122`). §RC spells the same-Run next writer explicitly, as X3c r8 does, so each row that tests it shows it.
- **The guard.** X3c-3 makes any `r2` value other than `same` or `distinct` a `HARNESS-ERROR`. No existing row carries another value.
- **Rejected:** leaving the directive out, which hides the property the RC rows test.

**Lead decision LD-RC-5: new observed values.** X3c r8's expectations name state the harness does not observe yet: availability rows, Run-material rows, commit sequences, linked objects, staged tables and kept rows. RC.7 defines each value X3c-3 adds.
- The verdict compares a value only where a row's `expected` names it (`verdict`, `commit_tests.rs:2973-3000`). No existing row names one.
- None is a run-record member.
- **Rejected:** leaving those expectations unscored, because they are item 14's content.

#### RC.3 RC-1's census child: the `recommit` census part

- **Composition (X3C:280).** Storage's census (X9:743-751) gains a fifth part, `recommit`, after X9-4's refused end. It runs:
  - on its own fresh root, after its own fixture child;
  - first an unarmed lawful commit E1 of the candidate, which is not part of the census, as r11's (c) does not count the (a) before it (X9:231);
  - then, in a fresh process, an unarmed lawful commit E2 of the same candidate. E2's trace is the part.
- **Checks.** The part is a `HARNESS-ERROR` unless all of these hold:
  - E1 and E2 are both `Committed(latched=false)`;
  - E2's trace reaches `x3c.object/reopen-confirm.after` and no `x3c.object/link.after`;
  - E2's trace reaches `x3c.evidence.stage-recovery_pair` and `stage-run_material`, and neither `stage-availability` nor `stage-pins` (X3C:185).
- **The usual rules.** The part runs twice, and the two runs must be equal point for point (X9:924).
  - The storage census trace digest hashes the five parts' normalized lines in order: commit, recover, sweep, refused end, recommit.
  - `census-trace.txt` prefixes the part's lines with `recommit|`.
  - Host's census is unchanged.

**The predicted effect.**
- **Why most counts stay.** A confirmed object takes the steps `create, write, file-barrier, link.before, file-barrier, directory-barrier, reopen-confirm` (X9:446; the confirm path, `crates/platform/src/filesystem.rs:681-738`). So E2 reaches each `x3c.object/` name as often as E1 does, 82 objects at C, except these:

  | Name | E1 (C's census) | E2 | Union | Selected at r16 | Selected at r17 |
  |---|---|---|---|---|---|
  | `x3c.object/reopen-confirm.before` | 0 | 82 | 82 | none | `#1`, `#41`, `#82` |
  | `x3c.object/reopen-confirm.after` | 0 | 82 | 82 | none | `#1`, `#41`, `#82` |
  | `x3c.object/file-barrier.before` | 82 | 164 | 164 | `#1`, `#41`, `#82` | `#1`, `#82`, `#164` |
  | `x3c.object/file-barrier.after` | 82 | 164 | 164 | `#1`, `#41`, `#82` | `#1`, `#82`, `#164` |
  | `x3c.object/link.after` | 82 | 0 | 82 | unchanged | unchanged |

- **Why nothing else moves.** Every other point E2 reaches is a name the union already holds, at a count no smaller than E2's:
  - E2 admits its store directories and opens its ledger through the same `create` and `directory-barrier` names, and reaches no `x3c.ledger-create/` file point (`crates/security/src/store_custody.rs:111-170`, `:229-247`; `crates/storage/src/ledger_store/project_ledger.rs:516-560`);
  - its root, carrier and trust steps are those of host's `finalize` child, which also follows an earlier process on its root (X9:205-209, :736-741);
  - its staging reaches two of the four `stage-` names (X3C:185).
- **The totals this predicts:**
  - storage census 259 to 261 points; storage kill set 321 to 327;
  - union census 321 to 323 points; union kill set 383 to 389;
  - kill-set points the part adds: 8 (the six `reopen-confirm` points, `file-barrier.before#164` and `file-barrier.after#164`);
  - points the part removes from item 5's selection: 2 (`file-barrier.before#41` and `file-barrier.after#41`).

**Lead decision LD-RC-6: F03's two `#41` rows stay, outside the selected kill set.**
- **The move.** Under r10's union rule the two `file-barrier` names reach 164 occurrences, so item 5's selection for them is `#1`, `#82` and `#164` (`(n + 1) / 2`; `crates/platform/src/crash_barrier/driver.rs:571-582`; `tools/check_crash_matrix.py:172-179`). F03's rows `kill-x3c-object-file-barrier-before-41` and `kill-x3c-object-file-barrier-after-41` now kill census points that the selection no longer names.
- **The decision.** Both rows stay byte for byte.
  - Each still kills a real durability point of the census (41 is at most 164), on a first commit.
  - `check` lists them in `killedOutsideKillSet` and does not refuse (`tools/check_crash_matrix.py:481-489`).
  - Only `check-unit` refuses a kill outside the kill set (`:375-377`). No unit's subset is affected: X9-2's own census has no re-commit part, so 82 occurrences and `#41` still stand there.
  - So X3c-3's lead `check` lists exactly these two points in `killedOutsideKillSet`. Any other point there is a stop.
- **Coverage.** F03's rows still cover `#1` and `#82`. Only a re-commit reaches `#164`, so RC-2 covers it.
- **r16's count-shift sentence** (X9:741) re-transcribes rows when a shift leaves a kill-set point unreachable by them. Here every selected point stays covered, and F03's `#41` stays reachable and killed. Re-transcribing would delete two accepted X9-2 rows, which frame rule 2 forbids.
- **Rejected:**
  - **Deleting or moving F03's `#41` rows.** No first commit reaches `#164`, and deleting changes X9-2's accepted rows.
  - **Keeping r16's selected points by a named list in the checker.** It adds a rule and code to keep two points that F03 kills anyway.
  - **Leaving the part out of the union for names other parts reach.** The census would then understate E2's trace. Item 5 makes the census what the unarmed runs reached (X9:920).
- **Stop rule.** X3c-3 stops and reports before transcription if its census-only run shows any other added or removed kill-set point, or other counts, as X9-2 to X9-6 did (X9:662). The correction is a new round of §RC (frame rule 6).

#### RC.4 The rows

There are 22 rows. X3c-3 appends them to storage's `required-runs.v1.json` after its 381 rows, so the file holds 403. Every expected value below comes from X3c r8's row text (X3C:277-307), and the clause is cited beside it. The spelling comes from the owning X9 row.

**Script templates.** Keys are sorted, as the file's canonical JSON sorts them. `P` is the armed point, `A` its action, `M` a mutation, `L` the ladder's steps.

```
T-L  [{"name":"e1","spawn":"commit"},{"finish":"e1"},
      {"name":"e2","spawn":"commit","unchanged":true},{"finish":"e2"},
      {"ladder":"R1,R2,R3,R4","of":"e2","r2":"same"},
      {"for":"e1","name":"e1-recover","spawn":"recover"},{"finish":"e1-recover"}]

T-K  [{"name":"e1","spawn":"commit"},{"finish":"e1"},
      {"arm":"P=hold","name":"e2","spawn":"commit","unchanged":true},
      {"await":"P","on":"e2","then":"kill"},
      {"ladder":"L","of":"e2","r2":"same"}]
     followed, where the row says "+ recover(E1)", by
      {"for":"e1","name":"e1-recover","spawn":"recover"},{"finish":"e1-recover"}

T-I  [{"name":"e1","spawn":"commit"},{"finish":"e1"},
      {"arm":"P=A","name":"e2","spawn":"commit","unchanged":true},{"finish":"e2"},
      {"ladder":"R1,R2,R3,R4","of":"e2","r2":"same"},
      {"for":"e1","name":"e1-recover","spawn":"recover"},{"finish":"e1-recover"}]

T-M  [{"name":"e1","spawn":"commit"},{"finish":"e1"},
      {"mutate":"M","of":"e1"},
      {"name":"e2","spawn":"commit","unchanged":true},{"finish":"e2"},
      {"ladder":"L","of":"e2"}]
     followed, where the row says "+ recover(E1)", by
      {"for":"e1","name":"e1-recover","spawn":"recover"},{"finish":"e1-recover"}

T-P  [{"distinct":true,"name":"d","spawn":"commit"},{"finish":"d"},
      {"mutate":"plant-availability","of":"d"},
      {"name":"e2","spawn":"commit","unchanged":true},{"finish":"e2"},
      {"ladder":"R1,R3,R4","of":"e2"}]

T-R  [{"name":"e1","spawn":"commit"},{"finish":"e1"},
      {"arm":"x3d.publish.after-staging#1=hold,x3d.publish.commit-returned#1=hold","name":"e2","spawn":"commit"},
      {"await":"x3d.publish.after-staging#1","on":"e2","then":"hold"},
      {"for":"e1","name":"e1-at-staging","spawn":"reader"},{"finish":"e1-at-staging"},
      {"for":"e2","name":"e2-at-staging","spawn":"reader"},{"finish":"e2-at-staging"},
      {"on":"e2","resume":"x3d.publish.after-staging#1"},
      {"await":"x3d.publish.commit-returned#1","on":"e2","then":"hold"},
      {"for":"e1","name":"e1-at-returned","spawn":"reader"},{"finish":"e1-at-returned"},
      {"for":"e2","name":"e2-at-returned","spawn":"reader"},{"finish":"e2-at-returned"},
      {"on":"e2","resume":"x3d.publish.commit-returned#1"},
      {"finish":"e2"}]
```

**The rows.** Every row has `"units": ["X3c"]` and `"unit": "X3c-3"`. In the labels column, "death" means `["process-death", "scripted-clock", "synthetic"]`, "injected" means `["injected", "scripted-clock", "synthetic"]`, "mutation" means `["mutation", "scripted-clock", "synthetic"]` and "plain" means `["scripted-clock", "synthetic"]`.

| Row | Case | Variant | Script | Labels |
|---|---|---|---|---|
| RC-1 | F15 | `recommit-lawful` | T-L | plain |
| RC-2 | F04 | `recommit-kill-x3c-object-reopen-confirm-before-1` | T-K, P `x3c.object/reopen-confirm.before#1`, L `R1,R2,R3,R4`, + recover(E1) | death |
| RC-2 | F04 | `recommit-kill-x3c-object-reopen-confirm-before-41` | as above, P `…reopen-confirm.before#41` | death |
| RC-2 | F04 | `recommit-kill-x3c-object-reopen-confirm-before-82` | as above, P `…reopen-confirm.before#82` | death |
| RC-2 | F04 | `recommit-kill-x3c-object-reopen-confirm-after-1` | as above, P `x3c.object/reopen-confirm.after#1` | death |
| RC-2 | F04 | `recommit-kill-x3c-object-reopen-confirm-after-41` | as above, P `…reopen-confirm.after#41` | death |
| RC-2 | F04 | `recommit-kill-x3c-object-reopen-confirm-after-82` | as above, P `…reopen-confirm.after#82` | death |
| RC-2 | F04 | `recommit-kill-x3c-object-file-barrier-before-164` | as above, P `x3c.object/file-barrier.before#164` | death |
| RC-2 | F04 | `recommit-kill-x3c-object-file-barrier-after-164` | as above, P `x3c.object/file-barrier.after#164` | death |
| RC-3 | F11 | `recommit-kill-x3c-evidence-stage-recovery-pair-1` | T-K, P `x3c.evidence.stage-recovery_pair#1`, L `R1,R2,R3,R4,R5`, + recover(E1) | death |
| RC-3 | F11 | `recommit-kill-x3c-evidence-stage-run-material-1` | as above, P `x3c.evidence.stage-run_material#1` | death |
| RC-4 | F12 | `recommit-fail-before-evidence-commit` | T-I, P `x3c.evidence.commit.before#1`, A `fail-before` | injected |
| RC-4 | F12 | `recommit-fail-after-evidence-commit` | T-I, P `x3c.evidence.commit.after#1`, A `fail-after` | injected |
| RC-5 | F13 | `recommit-kill-x3c-evidence-commit-after-1` | T-K, P `x3c.evidence.commit.after#1`, L `R1,R2,R3,R4` | death |
| RC-5 | F13 | `recommit-kill-x3d-publish-commit-returned-1` | T-K, P `x3d.publish.commit-returned#1`, L as above | death |
| RC-5 | F14 | `recommit-kill-x3d-publish-published-1` | T-K, P `x3d.publish.published#1`, L as above | death |
| RC-5 | F15 | `recommit-kill-x3d-finish-end-step-after-1` | T-K, P `x3d.finish.end-step.after#1`, L as above | death |
| RC-6 | F33 | `recommit-run-material-inventory` | T-M, M `run-material-inventory`, L `R1,R3,R4` | mutation |
| RC-7 | F23 | `recommit-one-sided-material-only` | T-M, M `delete-availability`, L `R1,R3,R4` | mutation |
| RC-7 | F23 | `recommit-one-sided-availability-only` | T-P | mutation |
| RC-8 | F29 | `recommit-readers-across-publish` | T-R | plain |
| RC-9 | F52 | `recommit-purged` | T-M, M `availability-purged`, L `R1`, + recover(E1) | mutation |

Each RC row's killed point is a kill-set point at r17: RC-2's eight are the points the `recommit` part adds (RC.3), and RC-3's and RC-5's six are the `#1` points F11, F13, F14 and F15 already kill. A point's occurrence counts within E2's own process (X9:852).

**Expected values.** The post-state values (`attemptRows`, `receipts`, `seals`, `revs`, `commitSequences`, `materialRows`, `materialIdentical`, `availabilityRows`, `pinRows`) are read at the ladder's capture, after the scripted children and before R1 (`commit_tests.rs:2103-2111`). RC-8 has no ladder, so its values come at the end. RC.7 defines each new value.

**RC-1. A lawful re-commit** (X3C:277-280). Case F15, `recommit-lawful`.

| Key | Expected | X3c r8 |
|---|---|---|
| `e1`, `e2` | `Committed(latched=false)` | "both `Committed(latched=false)`" |
| `e1.stages` | `recovery_pair,run_material,availability,pins` | E1 is a first commit, staged as r7 stages it (X3C:119); point order `project_commit.rs:472-530` |
| `e2.stages` | `recovery_pair,run_material` | X3C:185 |
| `e2.objectsLinked` | `0` | "E2's trace has no `x3c.object/link.after`" |
| `e2.ledgerRowsKept` | `true` | "E1's rows are byte-equal before and after E2" |
| `attemptRows`, `receipts`, `materialRows` | `2` each | "2 attempt rows, 2 receipts … 2 Run-material rows" |
| `commitSequences` | `1,2` | "E2's `commitSequence` is 2"; 2 associations |
| `materialIdentical` | `true` | "with equal manifest and inventory" |
| `availabilityRows` | `1` | "1 availability row" |
| `pinRows` | `0` | "the pin tables are empty" |
| `R1` | `committed-historically:pendingSettlement:*` | R1(E2) CH `pendingSettlement` |
| `R2.outcome` | `Committed(latched=false)` | R2 (E3) `Committed` |
| `R3`, `R3.others` | `committed`; `next-writer=committed` | "R3 settles every attempt `committed`" (E2; E3) |
| `R4` | `committed-historically:settled:*` | R4(E2) CH `settled` |
| `e1-recover` | `committed-historically:settled:*` | recover(E1) CH, after R3 settled E1 |

**RC-2. Kills in the confirm branch** (X3C:281-283). Case F04, the eight variants above, one expected set.

| Key | Expected | X3c r8 |
|---|---|---|
| `e1` | `Committed(latched=false)` | RC-2 follows E1's commit |
| `e2` | `killed` | the kill |
| `e2.ledgerRowsKept` | `true` | "E1's rows are unchanged" |
| `e2.objectsKept` | `true` | "No object name or bytes changed" |
| `R1` | `unknown-attempt-open` | R1(E2) UAO |
| `R2.outcome` | `Committed(latched=false)` | R2 (E3) `Committed` |
| `R2.objectsLinked` | `0` | "with every object confirmed"; E2's staging file is never adopted |
| `R3`, `R3.others` | `refused`; `next-writer=committed` | "R3 settles E2 `refused` and E3 `committed`" |
| `R4` | `terminal-not-committed` | R4(E2) TNC |
| `e1-recover` | `committed-historically:settled:*` | recover(E1) CH, after R3 |

**RC-3. Staging kills** (X3C:284-286). Case F11, two variants, one expected set.

| Key | Expected | X3c r8 |
|---|---|---|
| `e1` | `Committed(latched=false)` | |
| `e2` | `killed` | |
| `e2.ledgerRowsKept` | `true` | the transaction rolls back |
| `seals`, `revs` | `2`; `0` | "E2's `SEAL` is durable with no `REV`" (E1's SEAL and E2's) |
| `receipts`, `materialRows` | `1` each | "E2 has no receipt or material" |
| `availabilityRows` | `1` | "there is still 1 availability row" |
| `R1` | `unknown-attempt-open` | R1(E2) UAO |
| `R2.outcome`, `R2.witnessAction` | `Committed(latched=false)`; `OK` | "R2 (E3) `Committed`, witness action OK" |
| `R3` | `refused` | "R3 settles E2 `refused`" |
| `R4` | `terminal-not-committed` | R4(E2) TNC |
| `R5` | `committed-historically:settled:*` | "R5 recover(E3) CH", after R3, as F36's R5 |
| `R5.sameRunId` | `true` | "E2's orphan `SEAL` and E3's `SEAL` name one RunId" (with RC.7's R5 rule) |
| `e1-recover` | `committed-historically:settled:*` | recover(E1) CH, after R3 |

**RC-4. The undetermined `COMMIT`** (X3C:287-289). Case F12, two variants.

| Key | `recommit-fail-before-evidence-commit` | `recommit-fail-after-evidence-commit` | X3c r8 |
|---|---|---|---|
| `e1` | `Committed(latched=false)` | `Committed(latched=false)` | |
| `e2` | `CommitUndetermined` | `CommitUndetermined` | `CommitUndetermined`, with E2's ExecutionId and no RunId |
| `e2.end` | `end(rev=false,cln=false,settlement=None,step=false,stepFailure=None)` | the same | "`end(rev=false, cln=false, …)`, and the reserve forfeited", spelled as F12's `scripted.end` |
| `e2.ledgerRowsKept` | `true` | `true` | 6a.6's earlier rows (X3C:170) |
| `receipts`, `materialRows` | `1` each | `2` each | "with `fail-after` … receipt, association and material exist; with `fail-before`, none" |
| `commitSequences` | `1` | `1,2` | the association |
| `availabilityRows` | `1` | `1` | "Either way there is 1 availability row" |
| `R1` | `unknown-attempt-open` | `committed-historically:pendingSettlement:*` | UAO (not landed) or CH `pendingSettlement` (landed) |
| `R2.outcome` | `Committed(latched=false)` | `Committed(latched=false)` | R2 (E3) `Committed` |
| `R3` | `refused` | `committed` | |
| `R4` | `terminal-not-committed` | `committed-historically:settled:*` | R4 TNC or CH |
| `e1-recover` | `committed-historically:settled:*` | `committed-historically:settled:*` | recover(E1) CH, after R3 |

**RC-5. The lost acknowledgement, with a same-Run next writer** (X3C:290-292). Cases F13, F14 and F15, four variants.

| Key | Expected | X3c r8 |
|---|---|---|
| `e1` | `Committed(latched=false)` | |
| `e2` | `killed` | |
| `e2.ledgerRowsKept` | `true` | 6a.6's earlier rows (X3C:170) |
| `availabilityRows` | `1` | "1 availability row throughout" |
| `R1` | F13 and F14: `committed-historically:pendingSettlement:*`; F15: `committed-historically:*` | "R1(E2) CH, with `pendingSettlement` as F13 to F15 give it" (X9's F13, F14 and F15 spellings) |
| `R2.outcome` | `Committed(latched=false)` | R2 (E3) `Committed` |
| `R2.commitSequence` | `3` | "with `commitSequence` 3" |
| `R2.receipts` | `1` | "no second receipt for E2" (F15's `R2.receipts`) |
| `R2.availabilityRows` | `1` | "1 availability row throughout" |
| `R3` | `committed` | |
| `R4` | `committed-historically:settled:*` | R4(E2) CH `settled` |

**RC-6. A regeneration mismatch** (X3C:293-295). Case F33, `recommit-run-material-inventory`. The mutation is F33's own: one digest in E1's stored inventory changed, with `run_material_no_update` lifted and reinstalled (`commit_tests.rs:2581-2587`).

| Key | Expected | X3c r8 |
|---|---|---|
| `e1` | `Committed(latched=false)` | |
| `e2` | `Refused(Invariant)` | "E2 `Refused(Invariant)` at staging" |
| `e2.rev`, `e2.cln` | `true`; `true` | "`end(rev=true, cln=true, …)`" |
| `e2.stages` | the empty string | refused before any insert (X3C:134, :184) |
| `e2.ledgerRowsKept` | `true` | "E2 does not change E1's rows" |
| `receipts`, `materialRows` | `1` each | "no receipt, association or material" |
| `commitSequences` | `1` | no association |
| `availabilityRows` | `1` | "still 1 availability row" |
| `R1`, `R3`, `R4` | `unknown-attempt-open`; `refused`; `terminal-not-committed` | the ladder R1, R3, R4 |

**RC-7. A one-sided Run** (X3C:296-302). Case F23, two variants. Mutations `delete-availability` and `plant-availability` are RC.7's.

| Key | `recommit-one-sided-material-only` (a) | `recommit-one-sided-availability-only` (b) | X3c r8 |
|---|---|---|---|
| `e1` or `d` | `e1`: `Committed(latched=false)` | `d`: `Committed(latched=false)` | (a) after E1 commits; (b) after the distinct variant's commit |
| `e2` | `Refused(LedgerCorrupt)` | `Refused(LedgerCorrupt)` | "`Refused(LedgerCorrupt)`" |
| `e2.rev`, `e2.cln` | `true`; `true` | `true`; `true` | "`end(rev=true, cln=true, …)`" |
| `e2.stages` | the empty string | the empty string | "nothing inserted" (X3C:121, :184) |
| `e2.ledgerRowsKept` | `true` | `true` | "nothing inserted" |
| `receipts`, `materialRows` | `1` each | `1` each | E1's, or `d`'s |
| `availabilityRows` | `0` | `2` | (a) R's row deleted; (b) `d`'s row and R's planted row |
| `R1`, `R3`, `R4` | `unknown-attempt-open`; `refused`; `terminal-not-committed` | the same | "R1 UAO; R3 `refused`; R4 TNC" |

**RC-8. Reader isolation** (X3C:303-304). Case F29, `recommit-readers-across-publish`. No ladder, as F29 has none.

| Key | Expected | X3c r8 |
|---|---|---|
| `e1`, `e2` | `Committed(latched=false)` | E2 is resumed to its end |
| `e1-at-staging`, `e1-at-returned` | `committed-historically:pendingSettlement:*` | "E1 is CH both times"; E1 is not settled, because no sweep runs |
| `e2-at-staging` | `unknown-attempt-open` | "E2 is UAO", as F29 at `x3d.publish.after-staging#1` |
| `e2-at-returned` | `committed-historically:pendingSettlement:*` | "then CH `pendingSettlement`", as F29 at `x3d.publish.commit-returned#1` |

**RC-9. A non-retained record** (X3C:305-307). Case F52, `recommit-purged`. The mutation is F52's own `availability-purged`: a generation-1 `purged` record, and the largest object deleted (`commit_tests.rs:2624-2654`).

| Key | Expected | X3c r8 |
|---|---|---|
| `e1`, `e2` | `Committed(latched=false)` | "E2 `Committed(latched=false)`" |
| `e2.objectsLinked` | `1` | "E2 publishes the deleted object new and confirms the rest" |
| `e2.stages` | `recovery_pair,run_material` | "No availability row is added" |
| `e2.ledgerRowsKept` | `true` | the generation-1 record "stays current" |
| `availabilityRows` | `2` | generation 0 and generation 1; none added |
| `R1` | `committed-historically:pendingSettlement:*` | "R1(E2) CH `pendingSettlement`, because every object is present again" |
| `e1-recover` | `committed-historically:pendingSettlement:*` | recover(E1) CH; no sweep has run |

**Repetition.** Each RC row's two lead repetitions must agree on `normalizedSha256` and on every child's trace digest (item 7).
- X9-3's normalizer orders the rows of every table without rowid by shape, and ties by normalized content (`crates/security/src/crash_matrix_support/post_state.rs:196-205`, `:225-282`). So two receipts or two material rows of one Run compare between repetitions.
- r14's group order makes a child that confirms some objects and creates others repeatable (X9:440-466). RC-9's E2 is such a child.

#### RC.5 The record of the 19 runs

- **The record** (X3C:309-322). In 19 runs of the accepted storage set at C, an unscored next writer, or F49's scripted second writer, commits the candidate after the candidate was committed. Each ends `Refused(Invariant)` at C (X3C:311).
- **How each new outcome is derived.**
  - **Standing** (X3C:114-133): both of R's per-Run rows exist (a re-commit), neither exists (a first commit), or one exists (`LEDGER.CORRUPT`).
  - **Material** (X3C:134-142): a re-commit's manifest and inventory must equal R's committed material, or the invariant row applies.
  - **What each mutation touches:** read from its code (`commit_tests.rs:2488-2657`).

| # | Run | Child | What the run leaves before that child | Standing | Material | Under X3c r8 |
|---|---|---|---|---|---|---|
| 1 | F12 `fail-after-evidence-commit` | R2 | E1's `COMMIT` landed and was reported undetermined | re-commit | identical | `Committed(latched=false)` |
| 2 | F23 `delete-receipt` | R2 | E1 killed at `x3d.publish.commit-returned#1`, so its `COMMIT` landed; then E1's receipt deleted (`:2505`) | re-commit | identical | `Committed(latched=false)` |
| 3 | F23 `delete-association` | R2 | as row 2, with E1's association deleted (`:2506`) | re-commit | identical | `Committed(latched=false)` |
| 4 to 7 | F27 `association-store-generation`, `association-namespace`, `association-operation`, `association-execution` | R2 | one member of E1's association body rewritten; its key columns unchanged (`:2559-2573`) | re-commit | identical | `Committed(latched=false)` |
| 8 | F28 `pruned-generations` | R2 | carrier generations pruned and planted; ledger untouched (`:2655`) | re-commit | identical | `Committed(latched=false)` |
| 9, 10 | F33 `receipt-assurance`, `receipt-signer` | R2 | E1's receipt body rewritten (`:2575-2580`) | re-commit | identical | `Committed(latched=false)` |
| 11 | F33 `association-seal-digest` | R2 | E1's association body rewritten (`:2588`) | re-commit | identical | `Committed(latched=false)` |
| 12 | F33 `run-material-inventory` | R2 | one digest of E1's stored inventory changed (`:2581-2587`) | re-commit | **differs** | **`Refused(Invariant)`**, by RC-6's rule (X3C:134) |
| 13 | F40 `fail-after-evidence-commit` | R2 | as row 1 | re-commit | identical | `Committed(latched=false)` |
| 14 | F49 `reader-skewed-by-append` | `second` | `first` committed, nothing mutated | re-commit | identical | `Committed(latched=false)` |
| 15 | F52 `association-only` | R2 | E1's receipt deleted (`delete-receipt`) | re-commit | identical | `Committed(latched=false)` |
| 16 | F52 `no-row-both` | R2 | E1's attempt row deleted (`:2507`) | re-commit | identical | `Committed(latched=false)` |
| 17 | F52 `purged` | R2 | a generation-1 `purged` record added and the largest object deleted (`:2624-2654`) | re-commit | identical | `Committed(latched=false)`, publishing the deleted object new, as RC-9 |
| 18 | F52 `receipt-only` | R2 | E1's association deleted (`delete-association`) | re-commit | identical | `Committed(latched=false)` |
| 19 | F52 `settled-refused-both` | R2 | E1's attempt row settled `refused` (`:2510`) | re-commit | identical | `Committed(latched=false)` |

- **18 of the 19 change outcome; one does not.** No mutation deletes R's availability row or R's material row, so no run leaves R one-sided. Only `run-material-inventory` changes R's material. This is X3c r8's count (X3C:320).
- **Sequences after a deleted association** (rows 3 and 18). `next_commit_sequence` reads the association table's key columns (`crates/storage/src/ledger_store.rs:732-753`), so E3's association takes sequence 1. No association holds it any more, and no DDL or X3c rule compares it with E1's receipt body. The F27 and F33 mutations rewrite the body only, so E3 takes sequence 2 there. Neither is scored.
- **No existing expected value names those outcomes.**
  - None of the 19 rows' `expected` names the child whose outcome changes: R2's members, or F49's `second`. They score R1, the scripted child, and, where the row runs them, `R3`, F23's `R3.left` and `R4`, each for E1. F49 scores `first` and `reader`. Each of those values is E1's, or is taken before R2, and none changes.
  - F49's `reader` keeps `committed-historically:pendingSettlement:*`. r12's reading holds with the second writer now committed: "a lawful writer appends and exits", and the one fresh capture confirms the earlier attempt (X9:280-281).
  - No expected value in either file names `Refused(Invariant)`. Host's two invariant expectations, F01 `substituted-target` and `substituted-inventory` (`finalize1`), are refusals at X3d item 3 step 1, before any attempt row, so staging never runs.
  - **So nothing is re-transcribed.**
- **What changes in those runs' records,** all unscored:
  - the child's outcome;
  - `R3`'s `nextWriter` in rows 1, 2, 3 and 13: `next-writer=refused` becomes `next-writer=committed`;
  - trace digests of that child and of later ladder children;
  - `normalizedSha256` of F49 only. X9-2's form captures the post state before the ladder (`commit_tests.rs:1730`), so the 17 runs in that form keep it. F49's step form has no ladder and captures after its children (`:2137-2147`).
- **r16's release-order verdict now applies** to the 18 children, because each ends `Committed` (`commit_tests.rs:620-624`; X9:753-769). A re-commit runs the same journal, level-3, level-4, lease and fence steps as a first commit (X3C:262; X3C:182-187), so the order is expected to hold. A violation is a FAIL and a stop.
- **Rows that stay first commits under X3c r8:**
  - F24 `wrong-store-generation`'s scored R2 `Committed` commits under the admitted digest, which holds no per-Run row (X3C:128);
  - F36's R2 follows an orphan SEAL, which leaves no per-Run row (X3C:124);
  - F04 `kill-link-after-1-unequal-collision`'s R2 refuses at the object, before staging;
  - every R2 that r12 and r13 give the distinct variant commits another Run (X9:264, :356). Those rows stay as they are (X3C:322).

**Lead decision LD-RC-7: the 18 changed outcomes stay unscored.** RC-1 to RC-9 score the same-Run commit directly.
- **Rejected: scoring them in their rows.** It re-transcribes 18 accepted rows of X9-3 and X9-4 for coverage the RC rows already give. X3c r8 records "no transcribed expected value changes" (X3C:310), and frame rule 2 forbids it.

#### RC.6 The lead-set duty

- **Before the lead set.** On its integration candidate, X3c-3:
  1. runs the census-only step of both targets (`OPENSIP_X9_CENSUS_ONLY`) and the checker's `coverage` (X9:647-648);
  2. compares the result with RC.3;
  3. transcribes the 22 rows from §RC and that census only;
  4. makes development runs of the RC rows and the 19 runs of RC.5.

  If any step contradicts RC.3, RC.4 or RC.5, X3c-3 stops and reports, as X9-2 to X9-6 did (X9:662). The correction is a new round of §RC.
- **The lead set** (X3C:260). Two repetitions of both targets on X3c-3's integration commit:
  - storage's 381 rows and the 22 RC rows, 403 in all;
  - host's 98 rows.

  That is 501 runs per repetition. `check` must pass over both targets (item 7, X9:1031-1041; r10, X9:222). It requires every row of both files, the union census and full kill-set coverage. The record states the union totals and `killedOutsideKillSet` (RC.3).
- **Why host reruns.** Every host commit passes the changed staging (X3C:260). No host outcome is predicted to change, because no host child re-commits a committed Run (RC.5).
- **Serialized** with every other lead set. The 5,000 ms timing guard (X9:391) fails under a concurrent set (M3P:567).
- **Integration order with J4** (X3C:261; JRW:668). X3c-3 and J4 are independent. Whichever integrates second reruns both sections' rows:
  - if J4 integrates first, X3c-3's set covers storage's rows, §RC's, §RW's and host's;
  - if X3c-3 integrates first, J4e's set covers §RC's rows as well as its own.
- **J3b and later units.** By frame rule 5, any lead set after X3c-3 integrates runs §RC's rows too.

#### RC.7 What X3c-3 adds

These are X3c-3's additions to the matrix target and the checker, beside X3c r8 item 13's storage code (X3C:252-259). The harness is `crates/storage/tests/commit_tests.rs`. X3c-3 makes each change, with a test where the checker or harness has one for its neighbours. §RC edits no product file.

1. **Rows.** The 22 rows of RC.4, appended to `crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json` after its 381 rows. No existing row changes. The file holds 403 rows.
2. **The `recommit` census part** (RC.3), in `x96_parts` (`:3143-3147`), with its checks.
3. **Observed values.** The verdict compares each value only where a row's `expected` names it.
   - **Post-state values,** read beside `seals`, `receipts` and `orphansPresent` at the step form's capture (`post_values`, `:1412-1423`):
     - `availabilityRows`: rows of `evidence_availability`;
     - `materialRows`: rows of `commit_run_material`;
     - `materialIdentical`: `true` when every `commit_run_material` row has the same `manifest` bytes and the same `inventory` bytes;
     - `commitSequences`: every `commit_associations` row's `commit_sequence`, in numeric order, comma-joined;
     - `pinRows`: rows of `active_run_pins` plus rows of `pin_change_facts`;
     - `revs`: `REV` records in N's carrier, counted as `seals` counts SEALs (`seal_runs`, `:1425-1439`).
   - **Commit-child values,** for every commit child `n`, finished or killed (`trace_values`, `:1331-1370`):
     - `n.objectsLinked`: its `x3c.object/link.after` records;
     - `n.stages`: the `<table>` of each `x3c.evidence.stage-<table>` point it reached, in trace order, comma-joined. It is the empty string when there is none.
   - **Kept-state values,** for a child spawned `"unchanged": true` (`:1915-1917`, `:2028-2061`). They are computed when the child finishes, and now also when it is killed:
     - `n.ledgerRowsKept`: `true` when every ledger row present before the child is present after it, byte for byte;
     - `n.objectsKept`: `true` when every digest-named object present before the child is present after it with the same sha256. Staging names are not objects.

     No existing row kills a child spawned `unchanged` (F30 and F34 finish theirs), so no existing value changes.
   - **R2 values** (`ladder_steps`, `:1528-1568`), from R2's exit and the capture R2 already takes for `R2.receipts`:
     - `R2.objectsLinked`;
     - `R2.commitSequence`: the `commit_sequence` of R2's own association;
     - `R2.availabilityRows`.
4. **R5's one-RunId check** (`:1611-1628`). `R5.sameRunId` is `true` when the carrier holds at least two SEALs and every SEAL names one RunId. F36's runs hold exactly two, so their value is unchanged.
5. **`"r2": "same"`** (LD-RC-4). The harness reads it as the candidate, the default. Any `r2` value other than `same` or `distinct` is a `HARNESS-ERROR`.
6. **Two mutations** (`apply_x93`, `:2488-2657`). Each run that uses one is labelled `mutation`.
   - **`delete-availability`.** It deletes the one `evidence_availability` row of N, with `availability_no_delete` lifted and reinstalled from its own stored SQL (item 6's reserved-slot technique, as `lifted` does, `:2324-2343`). Any other row count is a `HARNESS-ERROR`.
   - **`plant-availability`.** It inserts one row, with the triggers in place, for the candidate's RunId R. The row is a copy of the `of` child's generation-0 `retained` row, with its RunId replaced by R.
     - **How the parent learns R.** R is the RunId of X3d-3's candidate (X9 r7), built from the `of` child's own session. That child writes R to a file under the run's scratch root, outside the installation and outside its trace, as r12's commit child writes its core closure (X9:293).
     - R is an input and is never scored.
7. **The checker** (`tools/check_crash_matrix.py:105`). `UNIT_VALUES` admits `"X3c-3"` with r16's reading of `"X9-6"`, with a test. `check-unit` admits no `--unit X3c-3`.
8. **Nothing else.** There is no new crash point, scope, kind, label, run-record member or limit (X3C:182-191).

### §S12. J1's section (J1 item 12 and successor S12; units J3b and J3d)

**Round 2, 2026-10-04. Not accepted.**

#### S12.1 What §S12 carries and what it decides

- **Its law.** J1 item 12 names the crash-matrix rows that J's units must keep, and the new rows S12-B, S12-C, S12-U, S12-D and S12-O (J1r6:849-871). J1's successor S12 is this section (J1r6:889). The frame's row cites J1 r5's lines (J1:832-841, :858). J1 r6, accepted, keeps r5's item 12 rows and records that S18 and S21 are bound, so all five rows may be transcribed now (J1r6:864).
- **The laws that fix each outcome:**
  - J1 r6 items 7 and 8: the session opened at the handoff, the latch window, the phases and precedence rules 1 to 4 (J1r6:505-539, :543-669);
  - X3d r9 S10: the cancellation latch, the operator stop row, `REV(operator)`, the `refused()` record and the rows S10 needs (X3D9:495-580);
  - X4 r8 S11: the gate word, rule FC and the stop transition (X4r8:271-516);
  - X7 r7 S9: `finalize`'s order and entries, the cancellation port, the projection table, step 1's split and LD7-4's crash points (X7r7:292-497);
  - X5 r4 item 3: replay after evaluation and before `prepare_commit` (J1r6:517);
  - S18 and S21, both bound: phase O's deferral, and the commit-outcome exception to the before-settle rule (J1r6:896, :899).
- **What §S12 fixes,** as J1 item 12 and X7 r7 S9.9 ask (J1r6:863-870; X7r7:492-495):
  - the re-transcribed host driver: the runner `finalize_commit` and its fixed delivery phase under X5 r4 and X7 r7 (S12.3);
  - each existing host row's expected value under that driver (S12.4). None changes, which answers J-C13 (J1r6:539);
  - the five rows' spellings, scripts and expected values, each derived from the laws above and X9's owning row, never from a run (S12.2, S12.5);
  - the census and lead-set duties of J3b and J3d, and which of them integrates S12-O (S12.6);
  - what J3b and J3d add to transcribe and run the rows (S12.7).
- **What §S12 does not decide.** It changes no outcome of J1, X3d, X4, X5, X7, S18 or S21. Where one of them states an expectation, §S12 spells it. Where a spelling or a harness member is open, §S12 takes it from X9's existing rows and records a lead decision, LD-S12-1 to LD-S12-8. SOP2's own finalization, cutoff and freeze stay outside the matrix: S18-T1 tests them in process (S18:221-226; LD-S12-6).
- **Its basis.**
  - Product main `1799d3d`, read only. J3b's code does not exist yet, so no run has signalled a matrix child.
  - Every census figure below is C's (`3d2d5b5`): host 218 points with a 271-point kill set, storage 259 points with a 321-point kill set, and the union 321 points with 383 (`evidence/3d2d5b5…/host/matrix.json`, `storage/matrix.json`; RC.3). X4-F1's and X4-F2's X9 regressions found both censuses unchanged (OVERNIGHT:312, :612).
  - Where §S12 predicts a census or a value, the prediction is the law's and the code's. J3b's census-only run and development runs check it before its lead set (S12.6).

#### S12.2 Spellings and conventions

| Member | S12 rows | Basis |
|---|---|---|
| Target | host's `required-runs.v1.json`, for all five rows (LD-S12-1) | J1r6:865-870; X7r7:333-346 |
| `case` | the F-case of the row's hold point: S12-B F38, S12-C F39, S12-U F40, S12-D F15, S12-O F16 (LD-S12-2) | X9:696, :1108-1109, :1131-1133; the checker's grammar `F[0-5][0-9]` (`tools/check_crash_matrix.py:257`) |
| `variant` | `signal-` followed by the spelling of the existing row whose hold the script uses, without that row's action word (LD-S12-3) | X9:698; RC.2 |
| `units` | `["J1"]`: the law whose item 12 owns the row | `units` names owning laws (X9:532) |
| `unit` | `"J3b"` for S12-B, -C, -U and -D; `"J3d"` for S12-O | frame rule 3; J1r6:913-914; X7r7:421-434 |
| `labels` | item 4's labels: `["scripted-clock", "synthetic"]` for a signal run, and `injected` added for S12-U's `fail-after`. A signal is neither a death, an injected stand-in nor a mutation | X9:915 |
| `script` | host's script form, with one new `then` value, `signal-resume` (LD-S12-4) | `crates/host/tests/commit_matrix_tests.rs:1415-1570` |
| Expected spellings | host's existing spellings (`authoritative:0`, `terminated:<code>/<detail>`, `unknown-attempt-open`, `terminal-not-committed`, `committed-historically:*`), and S12.7's new values. A `:*` suffix matches any further detail, as in host's `meets` (`commit_matrix_tests.rs:1048`) | the F12, F16, F39 and F40 host rows |

**Lead decision LD-S12-1: all five rows are host rows.**
- **Why.** Each row's outcome is a host projection, or it depends on host's cancellation source:
  - finalization takes the token at the session's opening and hands it to host's cancellation source at P3 (X7r7:337-339, LD7-2);
  - only finalization calls the session (X7r7 LD7-1, :439-447), so only a host child can latch through the token;
  - S12-B's expectation names the interrupted projection, S12-C's and S12-U's name X7's rows, and J1 puts S12-D and S12-O in a host run (J1r6:865-870).
- **Rejected: storage rows for S12-B, -C and -U.** Storage's `commit` child has no cancellation source and no projection. It would have to take the token itself, a second holder that LD7-2 rules out.

**Lead decision LD-S12-2: each row's case is the F-case of its hold point.** r16 placed its kill rows by window in the census trace (X9:696), and LD-RC-1 placed RC-5's rows by kill point.
- S12-B holds at `x3d.publish.after-staging#1`, F38's hold, and its expectation is F38's (J1r6:865; X9:1131).
- S12-C holds at `x3c.evidence.commit.before#1`, r12's F39 hold, and its expectation is F39's (J1r6:866; X9:1132).
- S12-U is S12-C with F40's `fail-after`, and its expectation is F40's (J1r6:867; X9:1133).
- S12-D holds at `x3d.finish.end-step.after#1`, which J1 names as F15's point (J1r6:869; X9:1108).
- S12-O holds at `x7.delivery.required.before#1`, F16's host point (J1r6:870; X9:1109, :713).
- **Rejected: a case of its own, such as `S12`.** No build-plan case is the cancellation join's, and the checker's grammar admits only `F` and two digits (`tools/check_crash_matrix.py:257`).
- **Rejected: F14 or F17 for S12-D and S12-O.** F14's points are `published` and the settle, not the end step. F17 is the optional effect, which S12-D never reaches.

**Lead decision LD-S12-3: variant spellings.** A variant is `signal-` and then the spelling of the existing row whose hold the script uses, without that row's action word (`revoked`, `latched`, `fail` or `kill`).

| Row | Existing row | Variant |
|---|---|---|
| S12-B | storage F38 `revoked-after-staging` | `signal-after-staging` |
| S12-C | host F39 `latched-after-admission-delivery` | `signal-after-admission-delivery` |
| S12-U | host F40 `latched-fail-after-evidence-commit` | `signal-fail-after-evidence-commit` |
| S12-D | storage F15 `kill-x3d-finish-end-step-after-1` | `signal-x3d-finish-end-step-after-1` |
| S12-O | host F16 `fail-before-required-delivery` | `signal-before-required-delivery` |

Each `(case, variant)` pair is new in host's file. **Rejected:** J1's row names (`s12-b` and so on). No other variant names a law's row, and they say nothing about the run.

**Lead decision LD-S12-4: the signal step.** J1 sends S12-B's signal "through the support surface" (J1r6:865). J1 item 1 gives the M4 CLI unit the wiring of SIGINT, SIGTERM and SIGHUP into the cancellation source (J1r6:192), so no OS handler exists at M3.
- **The step.** `{"await": P, "then": "signal-resume"}` follows the row's `{"run": "finalize"}`, as `kill` and `revoke-latch-resume` do. The parent:
  1. awaits the child's `held` record at P;
  2. writes one control line, `signal SIGINT`, on the child's stdin, item 3's control channel (X9:884);
  3. awaits the child's `signalled` record;
  4. resumes P.
- **The child.** The runner registers one signal input with the crash barrier, bound to host's own cancellation source. The held thread reads the line, as it reads every control line, and hands it to that input's own thread. The held thread runs no product code (X9:887). The input's thread delivers SIGINT to the source, as the M4 CLI's handler will. When the source returns, the thread writes one tagged record, `X9|<pid>|<thread>|<n>|-|signalled|SIGINT`. That record names no point, so the census ignores it (`Census::from_exit` skips records whose point is `-`, `crates/platform/src/crash_barrier/driver.rs:536-545`).
- **What the source does with it,** as J1 8.2 and X7 r7 S9.2 fix:
  - in B and C, it holds the token and the window is open, so it latches at once, on its own thread (J1r6:580; X7r7:339). The latch's `x4.gate.latch.after` is written before `signalled` (X4r8:395-397);
  - in D, it keeps the signal for the decision point and takes no latch (J1r6:587);
  - in O, after P5, it labels the signal O and defers it (X7r7:341, :377).
- **Why it is deterministic.** The parent resumes only after the source has observed the signal and taken any latch it takes. No step sleeps or polls (item 3).
- **Rejected:**
  - **A real `SIGINT` by `kill(2)`.** Delivery is asynchronous. In D and O no latch point follows it, so the parent could resume before the source saw the signal, and the phase would be a race. It also needs an OS handler in the library, which J1 gives to the M4 CLI unit.
  - **Delivering on the held thread.** A held thread runs no product code (X9:887).
  - **A crash point as the acknowledgement.** J1, X3d r9, X4 r8 and X7 r7 add no crash point (J1r6:871; X3D9:573; X4r8:515; X7r7:468).

**Lead decision LD-S12-5: the fixed delivery phase renders only the success envelope's bytes.** X7 r7 splits X7a's `render` into the D projection and O's rendering of the decided envelope (X7r7:366-368).
- **The decision.**
  - The projection is built in memory and never fails. It runs under no `x7` point (X7r7:472).
  - O's rendering gives the success envelope today's fixed response, `{"x9":"delivered"}\n` (19 bytes), with exit 0.
  - It gives every other decided envelope zero bytes, with that envelope's own exit. That covers phase D's interrupted envelope, every termination and the failure envelope.
  - The optional effect still succeeds, and it follows only a success envelope (X7r7:471).
  - A delivery failure still comes only from an armed `x7.delivery` point (X9:191).
- **Why.** The matrix scores outcomes from the runner's report, not from envelope bytes. A decided envelope's bytes are J2a's total projection (J1r6:816), which J3d tests end to end (X7r7:428-434). Zero bytes keep every scored `delivered` value: F16 `fail-before-required-delivery` keeps `0`, because its failure envelope writes nothing, and F17 keeps `19`.
- **Rejected: fixed bytes for each envelope kind.** F16's `delivered` would then change when J3d wires the failure envelope (X7r7:431). That re-transcribes a row J1 does not require (frame rule 2).

**Lead decision LD-S12-6: the runner's port is host's own cancellation source, and its SOP2 hook does nothing.**
- **The port.** `finalize` takes a caller-supplied port (X7r7:333). The runner passes host's own cancellation source, the one J3b and J3d build (X7r7:346), never a matrix copy. The support surface adds only the signal input (LD-S12-4). So the matrix tests host's labels and latch, as it tests host's own `finalize` (X9:199).
- **The hook.** O's SOP2 finalization runs through a caller-supplied hook (X7r7:375). The runner's hook does nothing, as its delivery phase is fixed. A matrix child has no operational sink, so no SOP2 record is written.
- **What S12-O then tests.** The deferral in O, and the source's label O, at a hold after P5 and after the hook (J1r6:870). SOP2's producer cutoff, freeze and post-freeze tally are S18-T1's in-process control (S18:221-226).
- **Rejected: O1's real finalization in the matrix child.** The matrix tests durable custody, not observability. O1's sink is S-OP-1's, which is not yet accepted (J1r6:226), and S18-T1 already tests SOP2's three cases.

**Lead decision LD-S12-7: new observed values.** S12.7 defines them: the head `interrupted:<exit>`, `finalize1.signal`, `finalize1.runId` on an interrupted outcome, `finalize1.arrivalPhases` and `revReasons`.
- The verdict compares a value only where a row's `expected` names it (host's `verdict`, `commit_matrix_tests.rs:1834`). No existing host row names one.
- None is a run-record member.
- **Rejected: leaving the arrival phase and the `REV` reason unscored.** They are what the rows test: J1 8.2's phases and X3d r9's `REV(operator)` (J1r6:580; X3D9:537-542).

**Lead decision LD-S12-8: no existing host row is re-transcribed.** S12.4 shows that every expected value of host's 98 rows holds under the new driver. Frame rule 2 allows a re-transcription only where the owning law requires one. J1 requires one for "a changed driver or expectation" (J1r6:863): the driver changes, and no expectation does.
- **Rejected: re-transcribing F01's post-state values to be safe.** That rewrites accepted values the law still gives (S12.4), which frame rule 2 forbids.

#### S12.3 The re-transcribed host driver

J1 item 12 re-transcribes the host drivers of F01, F12, F16, F17, F32, F39 and F40 "because of item 7's signature" (J1r6:863; X7r7:494). Those rows share one driver, the runner `finalize_commit` (X9:190-203). F53's `finalize` children use it too, though J1's list omits F53 (S12.4).

**The runner under J3b.** `finalize_commit(at, root, candidate)` keeps its signature, inputs and report type. It runs these steps:
1. **Read the candidate file,** as today. A file that cannot be read is the host I/O row, with no entry (`crates/host/src/crash_matrix_support.rs:304-318`).
2. **Make the process's one driver entry,** `operation(at, root)` (X9 r4 item 6). An entry refusal is reported as `finalize` reports its `admit` refusal today: the row through host's `installation_termination`, with no runId, remedy, namespace or binding (`crates/host/src/finalization.rs:418-421`).
3. **Open the session** through finalization's opening entry, which takes P1's token (X7r7:441-442). An `open` refusal runs `finish` and step 1, as finalization does.
4. **Call `finalize`** with the open session, the candidate's inputs, the fixed delivery phase (LD-S12-5), host's own cancellation source as the port, and a hook that does nothing (LD-S12-6). `finalize` then replays, prepares, publishes, finishes, and runs step 1, the output decision point and phase O, in X7 r7's order (X7r7:313-321; J1r6:517).
5. **Report values only.** The report gains the interrupted outcome and the source's arrival labels (S12.7). Nothing else in it changes.

**What stays** (X9:194-203): the runner's place in host's pinned support module, its on-disk inputs, one entry per process, value reports only, and no second coordinator. The `candidate` child and the host rows' starting state stay too: the carrier's INIT and the `candidate` child's one `REV` (X9:204-213, :325-330). The `candidate` child still builds the candidate from its own session, and R2 and F01's variants still read its file.

**What the new order means for the matrix.** X9 r5's matrix-only order, replay after `open` (X9:116), and host's own order now coincide (X5 r4 item 3). This runner replaces r10's "replay, then custody" (X9:190, :208). The in-place "r17 (§S12)" notes at those lines point here.

#### S12.4 The existing host rows under the new driver

| Host rows | Runs | What the new driver changes in the run | Scored values, each unchanged | Why each holds |
|---|---|---|---|---|
| F01 `replay-run-object-missing`, `replay-run-descriptor-altered` | 2 | The `finalize` child now makes its entry and opens its session, drawing an ExecutionId, before it replays. The refusal ends the session through `refused()` and `finish` | `finalize1` and its `deliveryPhase` (`not-started`), `remedy`, `runId` (`no`) and `subject`; `attemptRows` `0`; `sealRows` `0`; `carrierAdded` empty; `ledgerPresent` `false`; `ledgerCarrierUnchanged` `true`; `stateUnchanged` `true` | J-C13, below |
| F01 `substituted-target`, `substituted-inventory` | 2 | Replay moves after `open`, and it reaches no point | `finalize1` the invariant row, with its `deliveryPhase`, `remedy`, `runId` and `subject`; `attemptRows` `0`; `carrierAdded` `REV`; `ledgerPresent` `false`; `sealRows` `0` | The same calls in the same order: entry, `open`, step 0's reserve, step 1's refusal, `finish`'s one `REV` (X9:331-336). X7 r7 projects the refusal on its own row (X7r7:356) |
| F12 `fail-after-evidence-commit` and `fail-before-evidence-commit`; F40 the same two and `latched-fail-after-evidence-commit` | 5 | Replay moves after `open` | `finalize1` the durability row, with its `subject`, `namespace`, `remedy` and `runId`; `deliveryPhase` `not-started`; `gateLatched`; the ladder | Rule 1 (X7r7:352). The durability row's envelope renders under no `x7` point (X7r7:473). The latch variant's observer latch is unchanged (the r17 header, "X4 r8's record note") |
| F39 `latched-after-admission-delivery` | 1 | Replay moves after `open` | `finalize1` F39's row, with `runId` `yes`, `remedy`, `deliveryPhase` `not-started` and `gateLatched` `true`; `R1` | Rule 2 (X7r7:353). A latched `Committed` renders under no `x7` point (X7r7:470-473) |
| F16 `fail-before-required-delivery` | 1 | The D projection moves out of `x7.delivery.required` | `finalize1` F16's row, with `delivered` `0`, `exit` `4`, `remedy` and `runId` `yes`; `R1`; `R2.outcome` | `x7.delivery.required` still wraps the success envelope's rendering and output (X7r7:470). `fail-before` there is a renderer failure before any byte, so F16's row (X7r7:378-379). Its failure envelope writes zero bytes (LD-S12-5) |
| F16 `kill-x7-delivery-required-before-1` and `-after-1`; F17 `fail-before-optional-delivery`, `kill-x7-delivery-optional-before-1` and `-after-1` | 5 | As F16's | `finalize1` `killed`, or `authoritative:0` with `delivered` `19`, `optional` and `runId` `claimed`; the ladder | The same runs reach each `x7.delivery` point, at the same occurrence (X7r7:470-471; T7-7, X7r7:418). A death in delivery changes no evidence (X9:713) |
| F32, every row | 76 | Replay moves after `open` | `finalize1`, `rollover`, `endStep`, `subject`; `attemptRows`; the ladder | `CarrierCapacityExhausted` is `prepare_commit`'s step 3, and the rollover is `finish`'s end step (X3d item 3; X3B11:115-138). Neither moves, and replay adds no point |
| F53, every row | 6 | Replay moves after `open` | `finalize1`; `gc1` to `gc3` | J1's list omits F53, but its `finalize` children use the same runner. The attempt row's commit point and the sweep are unchanged |

The table covers all 98 host rows: 4 of F01, 5 of F12 and F40, 1 of F39, 6 of F16 and F17, 76 of F32 and 6 of F53.

**F01's replay-refused variants (J-C13).** J1 re-transcribes F01's host variant "if `finish`'s end step changes its post-state" (J1r6:539). It does not:
- **Nothing is appended.** `prepare_commit` never runs, so step 0's reserve is never taken. `refused()` latches the gate, and `finish` owes a `REV`, but with no reserve it appends nothing (X3D9:550-554; `crates/security/src/custody/commit_session.rs:1106-1125`). So `carrierAdded` stays empty.
- **No attempt row or ledger.** Both start at `prepare_commit`'s step 4, which is never reached. The substituted variants already show no ledger after an entry and `open` (X9:331-336).
- **No floor write.** The entry's floor step and `finish`'s end step write the floor only when the copy tail is higher than the floor (X3B11:75-95, :123). The `candidate` child's end step already copied the tail at its `REV` (X9:325-330), and this child appends nothing. So neither step writes.
- **Nothing else is written.** The `candidate` child already registered the root (X9:207). The lease files are empty and are only locked (`project-root-x2/PROPOSAL-r10.md:380`, :416). The session's draws and the ExecutionId reservation are in memory (J1r6:247).
- **So** `stateUnchanged`, `ledgerCarrierUnchanged`, `ledgerPresent`, `attemptRows`, `sealRows` and `carrierAdded` keep their values. `finalize1` is still X5 item 5's row (X7r7:356). Its envelope renders under no `x7` point, so `deliveryPhase` stays `not-started` (X7r7:473).

**Unscored changes.**
- **F01's two replay-refused runs.** The `finalize` child's trace now holds its entry, `x3d.session.execution-draw`, `refused()`'s `x4.gate.latch.after` and `finish`'s points, so its trace digest changes. The child now draws an ExecutionId, so the run record's `notApplicable: "no-execution-id"` is absent. F01 runs no ladder either way (`NO_LADDER`, `commit_matrix_tests.rs:64`).
- **Every other host row.** Its children reach the same points in the same order, because replay reaches no point: the evaluator and identity crates hold no crash point, and host's only points are `x7.delivery`'s (`finalization.rs:287`, :297). Their trace digests are therefore expected to stay. Item 7's repetition agreement checks them (X9:994).

**Stop rule.** If J3b's development runs show any of host's 98 values moved, J3b stops and reports before its lead set. The correction is a new round of §S12 (frame rule 6), never a value read back from a run.

#### S12.5 The rows

There are five rows. J3b appends S12-B, -C, -U and -D to host's `required-runs.v1.json` after its 98 rows, so the file holds 102. J3d appends S12-O, so it holds 103. Every expected value comes from the clause cited beside it. Its spelling comes from the host row named.

**Scripts.** Keys are sorted, as the file's canonical JSON sorts them.

```
S12-B  [{"arm":"x3d.publish.after-staging#1=hold"},{"run":"finalize"},
        {"await":"x3d.publish.after-staging#1","then":"signal-resume"}]

S12-C  [{"r2":"distinct"},{"arm":"x3c.evidence.commit.before#1=hold"},{"run":"finalize"},
        {"await":"x3c.evidence.commit.before#1","then":"signal-resume"}]

S12-U  [{"r2":"distinct"},{"arm":"x3c.evidence.commit.before#1=hold"},
        {"arm":"x3c.evidence.commit.after#1=fail-after"},{"run":"finalize"},
        {"await":"x3c.evidence.commit.before#1","then":"signal-resume"}]

S12-D  [{"r2":"distinct"},{"arm":"x3d.finish.end-step.after#1=hold"},{"run":"finalize"},
        {"await":"x3d.finish.end-step.after#1","then":"signal-resume"}]

S12-O  [{"r2":"distinct"},{"arm":"x7.delivery.required.before#1=hold"},{"run":"finalize"},
        {"await":"x7.delivery.required.before#1","then":"signal-resume"}]
```

- **R2's candidate.** `{"r2": "distinct"}` follows host's rule: after a committed Run, R2 commits the distinct variant (X9:356). S12-B commits no Run, so its R2 commits the candidate, a first commit (X9:265).
- **No observer arm.** No row arms `x4.observer.tick`. No revocation is published, so the observer finds the view unchanged and latches nothing, as in host's F12 and F16 rows.
- **The hold points.** Each is in host's census (a) at `#1`.

| Row | Case | Variant | Unit | Labels |
|---|---|---|---|---|
| S12-B | F38 | `signal-after-staging` | J3b | `scripted-clock`, `synthetic` |
| S12-C | F39 | `signal-after-admission-delivery` | J3b | `scripted-clock`, `synthetic` |
| S12-U | F40 | `signal-fail-after-evidence-commit` | J3b | `injected`, `scripted-clock`, `synthetic` |
| S12-D | F15 | `signal-x3d-finish-end-step-after-1` | J3b | `scripted-clock`, `synthetic` |
| S12-O | F16 | `signal-before-required-delivery` | J3d | `scripted-clock`, `synthetic` |

Every row has `"units": ["J1"]`. The harness reads each value where it reads it today: the `finalize1` values from the child's report; `attemptRows`, `sealRows`, `carrierAdded` and `revReasons` from the post state after the scripted phase; and `R1` to `R4` from the ladder (`commit_matrix_tests.rs:1299-1380`, :1586-1600).

**S12-B. A signal in phase B** (J1r6:585, :865; X3D9:575). Case F38, `signal-after-staging`. The latch takes the gate from 0 to 2 after the SEAL. The final checkpoint refuses on the operator stop row, and the staged transaction rolls back.

| Key | Expected | Basis |
|---|---|---|
| `finalize1` | `interrupted:130` | `Refused(Interrupted { signal })` takes rule 4: `interrupted` 130 with no runId (X7r7:355; J1r6:621; row 46) |
| `finalize1.signal` | `SIGINT` | the token's signal (X7r7:358) |
| `finalize1.runId` | `no` | rule 4 |
| `finalize1.arrivalPhases` | `B` | observed by the watcher at once, after the attempt row and before FinalGate admission (J1r6:580, :585) |
| `finalize1.gateLatched` | `true` | the latch, and then the checkpoint's trailing stop transition, reach `x4.gate.latch.after` (X4r8:395-397) |
| `finalize1.deliveryPhase` | `not-started` | this envelope renders under no `x7` point (X7r7:473) |
| `attemptRows`, `sealRows` | `1`; `1` | the attempt row stays `admitted`, and the SEAL stays as history (J1r6:585; F38, X9:1131) |
| `carrierAdded` | `SEAL,REV,CLN` | the SEAL, then `finish`'s `REV` and `CLN` from the reserve: a SEAL without its evidence owes both (J1r6:585; `commit_session.rs:1114-1120`) |
| `revReasons` | `operator` | the first stop is `Operator`, whose reason is `operator` (X3D9:537-542; J1r6:570) |
| `R1` | `unknown-attempt-open` | F38's R1 (X9:1131) |
| `R2.outcome` | `authoritative:0` | No revocation, so R2 is admitted. The refused attempt left no per-Run row, so R2's commit of the candidate is a first commit (X3C:114-133; F36, X9:1129) |
| `R3` | `refused` | the sweep settles the `admitted` attempt `refused` (J1r6:585) |
| `R4` | `terminal-not-committed` | F38's R4 without C5's revocation, as host's F12 not-landed row gives it |

**S12-C. A signal in phase C** (J1r6:586, :866; X3D9:576). Case F39, `signal-after-admission-delivery`. The latch takes the gate from 1 to 3 before the evidence `COMMIT`, which then lands.

| Key | Expected | Basis |
|---|---|---|
| `finalize1` | `terminated:DELIVERY.REQUIRED_FAILED/DELIVERY.RENDERER_FAILED_AFTER_COMMIT` | rule 2: a latched `Committed(PublishedCommit)` takes X7's F39 row, never `interrupted` (X7r7:353; J1r6:619; S21) |
| `finalize1.runId` | `yes` | the `PublishedCommit`'s runId |
| `finalize1.remedy` | `renderer-failed-after-commit` | host F39's spelling |
| `finalize1.deliveryPhase` | `not-started` | F39's row has no delivery phase (X7r7:353, :473) |
| `finalize1.gateLatched` | `true` | the latch from 1 to 3 |
| `finalize1.arrivalPhases` | `C` | J1r6:586 |
| `carrierAdded` | `SEAL,REV` | `finish` appends `REV(operator)` after `Committed`. A SEAL with its evidence owes no `CLN` (J1r6:586; `commit_session.rs:1114-1120`) |
| `revReasons` | `operator` | X3D9:537-542 |
| `R1` | `committed-historically:*` | host F39's R1 |
| `R2.outcome` | `authoritative:0` | No revocation: R2 commits the distinct variant (X9:356) |
| `R3` | `committed` | the sweep settles the committed attempt `committed` |
| `R4` | `committed-historically` | host F12's landed spelling |

**S12-U. A signal in phase C, then an undetermined `COMMIT`** (J1r6:867-868; X3D9:577). Case F40, `signal-fail-after-evidence-commit`. The latch takes the gate from 1 to 3. The evidence `COMMIT` lands and reports failure.

| Key | Expected | Basis |
|---|---|---|
| `finalize1` | `terminated:DURABILITY.COMMIT_FAILED/-` | rule 1, whatever the gate's state: never F39, never `interrupted` (J1r6:618, :868; X7r7:352) |
| `finalize1.subject` | `executionId` | host F40's spelling |
| `finalize1.namespace` | `yes` | the namespace is disclosed |
| `finalize1.remedy` | `commit-undetermined` | host F40's spelling |
| `finalize1.runId` | `no` | no runId (J1r6:868) |
| `finalize1.deliveryPhase` | `not-started` | X7r7:473 |
| `finalize1.gateLatched` | `true` | the latch from 1 to 3 |
| `finalize1.arrivalPhases` | `C` | J1r6:586 |
| `carrierAdded` | `SEAL` | the undetermined outcome forfeits the reserve, so `finish` appends nothing (J1r6:586) |
| `revReasons` | the empty string | no `REV` |
| `R1` | `committed-historically:pendingSettlement` | the `COMMIT` landed (host F40's latch variant) |
| `R2.outcome` | `authoritative:0` | R2 commits the distinct variant (X9:356) |
| `R3` | `committed` | host F40's |
| `R4` | `committed-historically` | host F40's |

**S12-D. A signal in phase D** (J1r6:587, :869; X7r7:354). Case F15, `signal-x3d-finish-end-step-after-1`. The Run commits unlatched, and the window closes. The signal comes after `finish`'s end step and before the output decision point.

| Key | Expected | Basis |
|---|---|---|
| `finalize1` | `interrupted:130` | rule 3: `interrupted` on `kind: run`, with the runId (X7r7:354; J1r6:620; row 47) |
| `finalize1.signal` | `SIGINT` | the first signal the source observed (X7r7:358) |
| `finalize1.runId` | `claimed` | the committed Run's runId, built only through `authoritative_run(&PublishedCommit)` (X7r7:397-400) |
| `finalize1.arrivalPhases` | `D` | J1r6:587 |
| `finalize1.gateLatched` | `false` | the window is closed, so no latch is taken (J1r6:587; X4r8:662-668) |
| `finalize1.deliveryPhase` | `started` | `x7.delivery.required` wraps O's rendering of phase D's interrupted envelope (X7r7:470) |
| `finalize1.delivered` | `0` | no byte of a success envelope (J1r6:869). The fixed phase writes this envelope as zero bytes (LD-S12-5) |
| `carrierAdded` | `SEAL` | no `REV` is owed for the signal (J1r6:587) |
| `revReasons` | the empty string | no `REV` |
| `R1` | `committed-historically:pendingSettlement` | the Run is committed (J1r6:869), as host's W7 rows give it (X9:713) |
| `R2.outcome` | `authoritative:0` | R2 commits the distinct variant (X9:356) |
| `R3` | `committed` | X9:713 |
| `R4` | `committed-historically` | X9:713 |

**S12-O. A signal in phase O** (J1r6:588, :870; X7r7:377; S18). Case F16, `signal-before-required-delivery`. The hold is inside the final output section, after the output decision point and the hook.

| Key | Expected | Basis |
|---|---|---|
| `finalize1` | `authoritative:0` | the decided envelope stands: a signal in O never changes it or its exit (X7r7:377; J1r6:588) |
| `finalize1.runId` | `claimed` | the committed Run's runId |
| `finalize1.delivered` | `19` | the decided envelope is written whole |
| `finalize1.optional` | `ok` | the optional effect follows a success envelope (X7r7:471) |
| `finalize1.arrivalPhases` | `O` | labelled O in memory (J1r6:870; X7r7:341) |
| `finalize1.gateLatched` | `false` | the window is closed |
| `finalize1.deliveryPhase` | `started` | X7r7:470 |
| `carrierAdded` | `SEAL` | nothing is owed |
| `revReasons` | the empty string | no `REV` |
| `R1` | `committed-historically:pendingSettlement` | X9:713 |
| `R2.outcome` | `authoritative:0` | X9:356 |
| `R3` | `committed` | X9:713 |
| `R4` | `committed-historically` | X9:713 |

No persisted log record is expected or scored. The runner's hook writes nothing (LD-S12-6), and J1 expects none (J1r6:870).

**Repetition.** Each S12 row's two lead repetitions must agree on `normalizedSha256` and on every child's trace digest (item 7). The `signalled` record is part of the child's trace, once per run.

#### S12.6 The census and lead-set duties

- **No census part.** §S12 adds no crash point (J1r6:871; X3D9:573; X4r8:515; X7r7:468). A signal run is not an unarmed lawful run, so it is no census part (item 5).
- **The prediction: J3b changes neither census.**
  - Host's census runs (a), (b) and (c) keep every name, count and order. Replay reaches no point, and it only moves after `open`. The window bits, the token, the sample, the stop-cause record and the ExecutionId reservation are in memory (X3D9:573; X4r8:516; J1r6:247). The D projection leaves `x7.delivery.required` and has no point of its own (X7r7:472).
  - Storage's census is unchanged by J3b, whose security and storage code adds no point (X3D9:573; X4r8:515).
  - So host stays at 218 points with a 271-point kill set, as at C. Storage stays at its last lead set's census: 259 points with 321 at C, or RC.3's 261 with 327 once X3c-3 has integrated. The union kill set stays at 383 points, or RC.3's 389.
- **J3b, before its lead set.** On its integration candidate, J3b:
  1. runs the census-only step of both targets and the checker's `coverage` (X9:647-648);
  2. compares the result with the prediction above;
  3. transcribes S12-B, -C, -U and -D from §S12 and that census only;
  4. makes development runs of the four rows and of all 98 host rows under the new runner.

  If any step contradicts S12.4, S12.5 or the prediction, J3b stops and reports. The correction is a new round of §S12 (frame rule 6).
- **J3b's lead set** (J1r6:855). Two serialized repetitions of both targets on J3b's integration commit:
  - storage: its 381 rows, plus §RC's 22 if X3c-3 has integrated (RC.6), plus §RW's if J4e has (frame rule 5);
  - host: 102 rows.

  `check` must pass over both targets (X9:1031-1041). The record states the union totals and `killedOutsideKillSet`: empty before X3c-3, and RC.3's two F03 `#41` points after it.
  - **With X4-F3.** If X4-F3 lands in J3b's commit, this lead set is X4-F3's too (X4r8:606, LD8-9). If it landed earlier, its own lead set ran first.
- **Which unit integrates S12-O: J3d.** J1 gives S12-O to J3d with the final output section's wiring, and X7 r7 lists it among J3d's tests (J1r6:914; X7r7:428-434). M3-PLAN places it "before J3d's O wiring" (M3P:319). J3b does not transcribe it, so J3b's lead set runs without it.
- **J3d, before its lead set.** J3d:
  1. runs the census-only step of both targets, with the same prediction. Its wiring keeps `x7.delivery.required` where LD7-4 places it (X7r7:470-473), and the runner's hook still does nothing;
  2. transcribes S12-O, so host's file holds 103 rows;
  3. makes development runs of S12-O and of the host rows;
  4. stops and reports on any contradiction.

  Its lead set is two serialized repetitions of both targets, with host's 103 rows (J1r6:855).
- **Order.** J3b integrates before J3d, which depends on it (J1r6:914). Every later lead set runs every S12 row (frame rule 5).

#### S12.7 What J3b and J3d add

These are J3b's additions to host's matrix target, its support surface, the crash barrier and the checker, beside J3b's own code (J1r6:913). The harness is `crates/host/tests/commit_matrix_tests.rs`. J3b makes each change, with a test where the harness or checker has one for its neighbours. §S12 edits no product file.

1. **Rows.** S12-B, -C, -U and -D, appended to host's `required-runs.v1.json` after its 98 rows. No existing row changes.
2. **The runner and its fixed phase** (S12.3; LD-S12-5, LD-S12-6), in `crates/host/src/crash_matrix_support.rs`. The runner's existing test stays: a missing candidate file ends on the host I/O row with no entry, and a second runner call refuses (`a_process_makes_at_most_one_runner_call`, `commit_matrix_tests.rs:2049-2076`).
3. **The signal step** (LD-S12-4):
   - **the parent:** `then: "signal-resume"` in host's script reader (`commit_matrix_tests.rs:1484-1570`);
   - **the control line** `signal <NAME>`, on item 3's control channel. `SIGINT` is the only name the rows use. An unknown name, or a line in a child that registered no input, is a `harness-error` (`crates/platform/src/crash_barrier.rs`; `crash_barrier/driver.rs`);
   - **the child:** the signal input, registered by the runner and served on its own thread, and the `signalled` record, written after the source returns.
4. **Observed values** (LD-S12-7). The verdict compares each only where a row's `expected` names it.
   - **The head `interrupted:<exit>`.** The report's new outcome, `Interrupted { signal, run_id }`, is written `kind=interrupted;exit=<exit>;signal=<signal>;runId=<value>`. `outcome_head` reads it as `interrupted:<exit>` (`commit_matrix_tests.rs:850-857`).
   - **`<slot>.signal`:** the interrupted envelope's signal, in COMMON4's spelling (`SIGINT`).
   - **`<slot>.runId` on an interrupted outcome:** `claimed` when its run carries the candidate's RunId, `other` when it carries another, and `no` when it carries none. The other outcomes keep today's spellings.
   - **`<slot>.arrivalPhases`:** the arrival-phase label host's cancellation source gave each signal it observed in the child, in order and comma-joined, in SOP2's `CancelPhase` spelling (`A` to `E`, and `O`; SOP2:871). It is `-` when the source observed none, and no existing row names it.
   - **`revReasons`:** the `reason` of each `REV` the scripted phase added to N's carrier, in carrier order and comma-joined. It is the empty string when there is none. It is read beside `carrierAdded` (`commit_matrix_tests.rs:1586-1598`).
5. **Selection.** Host's `required_all` admits every row whose `unit` is `"J3b"` or `"J3d"`, whatever its case (`commit_matrix_tests.rs:1074-1091`). X9-5's `required()` keeps excluding rows that carry a `unit` (`:1063-1072`). Without this, the F15 and F38 rows would be dropped, because X9-5's case list omits them (`:60`).
6. **The checker** (`tools/check_crash_matrix.py:105`). `UNIT_VALUES` admits `"J3b"` and `"J3d"` with r16's reading of `"X9-6"`, with a test. `check-unit` admits neither.
7. **Nothing else.** There is no new crash point, scope, point kind, point action, label, run-record member or limit. The control line and the `signalled` record are item 3's only additions.

**J3d adds** S12-O, appended after J3b's four rows, and any harness member S12-O needs beyond J3b's. None is expected: S12-O uses only J3b's signal step and values.

### §RW. J-RW's section (reserved)

**Reserved. It carries no rows.**
- **Owner.** J-RW, item 10, X-RW-10 and its successor RW-S6 (JRW:519-596, :625, :669). J4e transcribes and runs it (JRW:607).
- **What it will carry.**
  - RW-F00, which re-transcribes F00's L11 cells.
  - RW-D1, RW-K1 to RW-K10, RW-N1 to RW-N12 and RW-B.
  - J4's census.
  - L11's retirement, only on the evidence J-RW item 10 names (JRW:588).
- **What fills it.** A later round of r17, reviewed on its own, once J-RW is accepted and before J4e. J-RW r3 is in review with Codex, which recorded two required findings, JRW-R3-01 and JRW-R3-02 (`m3/reviews/codex-resume-repair-jrw-r3`).
- **Its tie to §RC.** Whichever of X3c-3 and J4 integrates second reruns both sections' rows (X3C:261; JRW:668; §RC.6).
