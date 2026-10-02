Grok review r1: X7a, host finalization (law X7 r5 items 1 to 5 and 8, with item 10's tests on injected outcomes), read under X3b r10, X3d r6, X5 r3, X6 r3, X8 r3, X9 r1 and X12 r3, with X8 r3 item 3's owner rows for this unit and inventory v125 (parent v124). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-finalization-x7a-r1.

**Rules for any run.**
- Use a CARGO_TARGET_DIR under that directory.
- Run every test with a private TMPDIR: create a 0700 directory under `$(getconf DARWIN_USER_TEMP_DIR)` (for example `…/grok-x7a-tmp`). Never use the shared `/private/tmp/claude-501` tree, which other runs churn.
- Run git only read-only, and only against the worktree below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read or print the private 413 UUID fixture.
- Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH`; Python is `python3.14`.

## The unit

X7 r5 item 11 defines X7a as `crates/host/src/finalization.rs` with items 1 to 5 and 8, tested on injected outcomes. X7b (item 6, the capacity rollover route) is a separate unit. Until X7b lands, X7a projects the exhaustion on item 6a's busy row.

It depends on:
- X3d-1 and X3d-2 (product 5f4395d and adc9081);
- X5a (54e6166);
- X2e's `ProjectOperation::end` with `JournalOutcome::Exhausted`;
- X12b's `configuration.rs`;
- X8a's driver.

All of them are integrated at 81214cb (X6a), the base under review. Library only: no CLI command calls `finalize`.

## Law

All under arch `docs/implementation/m2/`, accepted. The pins are in hashes.txt.
- `finalization-x7/PROPOSAL-r5.md`, X7 r5, the law of this unit. r4 and r5 changed X7a in three places: item 3's `ExistingAttempt` row, item 4's delivery read, and item 5's namespace disclosure (item 10, "X7a in flight").
- It is read under:
  - `carrier-recovery-x6/PROPOSAL.md` r3: item 1's `RequestedBinding` and `NotPrepared::ExistingAttempt { execution_id, requested }` (X6b, not yet integrated), and item 6 (`ExistingAttempt` is never recovered in the writer's invocation);
  - `journal-x3b/PROPOSAL.md` r10: items 4 (the end step; not entered after an uncertain outcome or on a closed attempt ledger), 5 (no in-operation reconciliation after an uncertain outcome) and 13 (the rollover, called from the end step);
  - `commit-session-x3d/PROPOSAL.md` r6: items 3, 4, 6, 7, 8 (the settlement reserve, forfeited at any uncertain outcome) and 9 (rows, including end-path failures);
  - `replay-join-x5/PROPOSAL.md` r3: items 3 (replay before any custody), 5d (the `REPLAY_LIMITS` production-caller pin) and 6 (only X7 calls `replay_candidate`);
  - `refusal-suite-x8/PROPOSAL.md` r3: items 1, 2, 3 (groups A and B, and the export rule), 3c (X7a exports the projection) and the "Owner rows" list;
  - `crash-matrix-x9/PROPOSAL.md` r1: item 5 (the `x7.delivery` scope, `required` and `optional`, both fallible; units after X9-0 place their own points) and gap G1;
  - `policy-admission-x12/PROPOSAL.md` r3: items 8 (pack admission first) and 9 (no Plan join wired into replay).

Design sources for the rows:
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md` lines 1130–1146 and the golden table at 1376–1377 (`DELIVERY.REQUIRED_FAILED`; the after-commit detail requires a `runId`, the no-Run detail forbids one);
- `docs/coop/design-corrections/workflows/query_surface_projection.v3.py`, `delivery_required_termination` (the after-commit remedy text);
- `docs/v2/architecture/implementation-boundaries-and-build-plan.md` lines 820–835 (delivery) and F12, F16, F17, F34, F39, F40;
- `docs/v2/contracts/product-v1/security-and-lifecycle.md` S7, lines 594–602 and 636–643 (`PROJECT.BUSY` names the namespace; retry outside the fence).

## Subject

**Product.** The worktree `/Users/sb/code/opensip-ai/opensip-x7a`, detached at `81214cb` (main). The lock selects v124 (unit X6a), whose 55 inheritance rows carry D1's 39 overrides and D2's 4 supersessions, already folded.
- The unit was written on 54e6166. X6a integrated at 81214cb before review. It changes only security's journal store (`recovery_capture.rs`, private) and the lock, so no X7a file overlaps. The diff was carried over byte for byte, then amended for X7 r4/r5, and v125 was rebuilt on v124. Every check below ran on 81214cb with the final bytes.
- Save `git -C <worktree> diff` as product.diff and report its sha256. The eleven new files are intent-to-add.
- The lead's value is in hashes.txt (`product.diff`): 14 files.

**Arch.** These files, all untracked:
- `repository-file-inventory.v125.json` (parent v124);
- `finalization-x7a-inventory-v125-subject.json`;
- `finalization-x7a-inventory-v125/`.

Inventory118 (X9-1) is in flight elsewhere and is not a parent of v125.

## What was built

**`crates/host/src/finalization.rs`** is new. It is a private module, macOS only like the security and storage commit types, and `#[allow(dead_code)]` as `fact_admission` and `configuration` are.

**`finalize(candidate, admit, phase) -> Finalization`** (`pub(crate)`) is the one coordinator (item 1). In order:
1. `replay_candidate(candidate, REPLAY_LIMITS)`. A refusal returns at once on `replay_termination` with `replay_remedy`. Nothing else has run (X5 item 3, F01).
2. `admit()`, the caller's X1 write and X2 project admission and handoff: `FnOnce() -> Result<ProjectOperation, InstallationTermination>`. It runs only after a successful replay, and its refusal is its own row.
3. `CommitSession::open`. Its refusal finishes the returned `StoppedSession`, then projects the refusal. N is taken from the open session.
4. `prepare_commit`, then `publish`. Both outcome sets join one private enum through two exhaustive `From` impls. The `ExistingAttempt` arm binds `{ execution_id, .. }`, so it compiles both today and once X6b adds `requested`.
5. `StoppedSession::finish` on every end path, before any delivery.
6. For `Committed` only: `authoritative_run(&commit)`, then the delivery phase unless `latched_after_admission()`.
7. One projection (item 3), exhaustive, with no wildcard arm.

**The projections (item 2).**
- **`authoritative_run(&PublishedCommit) -> AuthoritativeRun`** is exported, with the type, from the host root. It is the one place that writes `authority() == "authoritative"` and `run_id()`. `AuthoritativeRun` has private fields and derives only `Debug, PartialEq, Eq`.
- **`ephemeral_run(&EvaluationCandidate) -> EphemeralRun`** is `pub(crate)`. It gives `authority() == "ephemeral"`, `run_id() == None`, and the derived proof's id to cite.

**The delivery phase (item 4, r4).** `DeliveryPhase<C = PublishedCommit>` is a `pub(crate)` trait, supplied by the caller: `render(&C) -> Result<RenderedResponse, RendererFailed>`, `output() -> &mut dyn Write` and `optional(&C) -> Result<(), OptionalFailed>`. It reads nothing from the store. `finalize` lends it `&PublishedCommit` only, and builds no lease, receipt or read session.

**`deliver`** is private and generic over `C`:
- **Latched:** `NotStarted`. Nothing is rendered or written.
- **Required:** `x7.delivery.required` (fallible) wraps the render, then `deliver_required` to the output. A rendered exit outside {0, 1, 3} is a renderer failure before any byte. Any failure is `Failed`, with no retry.
- **Optional:** on success, `x7.delivery.optional` (fallible) wraps `optional`. A failure is disclosed beside the exit.

**`Finalization`** is `{ outcome, end_failure, optional_failure }`.
- `outcome` is either `Authoritative { run, exit }` or `Terminated(Termination { row: InstallationTerminationV1, run_id, remedy, namespace })`.
- `end_failure` is `SessionEnd::settlement_failure()` through `installation_termination`, disclosed beside the outcome.

**The rows (item 3):**

| Concluded | Outcome |
|---|---|
| `Committed`, delivered | `Authoritative { run, exit }`, with the delivered exit (0, 1 or 3); an optional failure is disclosed beside it (F17) |
| `Committed`, required delivery failed (F16) or latched after admission (F39) | operational-failed, 4, `DELIVERY.REQUIRED_FAILED`, `delivery-required`, `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`; `run_id` retained; remedy "the Run is committed; rerun the renderer with this runId" |
| `CommitUndetermined` (F12, F40), from `publish` or `prepare_commit` | `installation_termination(CommitUndetermined)` (operational-failed, 4, `DURABILITY.COMMIT_FAILED`, `durability-commit`); subject the ExecutionId; `namespace` N beside it (item 5, r4); no RunId; remedy `REMEDY_COMMIT_UNDETERMINED` (later read-only recovery, no retry) |
| `ExistingAttempt` (F34, item 3, r4) | `installation_termination(Invariant)`; subject the ExecutionId; `namespace` N beside it; remedy `REMEDY_EXISTING_ATTEMPT` (a later invocation's read-only recovery with the requested binding, no retry); no recovery in this invocation (call 14) |
| `Refused(row)`, from any source | `installation_termination(row)`, unchanged |
| `CarrierCapacityExhausted` | `installation_termination(Busy)` (operational-failed, 4, `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, `PROJECT.BUSY`), subject N |

**Other product files.**
- **`crates/host/src/lib.rs`** declares `finalization` and re-exports `AuthoritativeRun` and `authoritative_run` (both macOS only).
- **`crates/host/src/fact_admission_tests.rs`:** X5's `REPLAY_LIMITS` caller pin moves from "at most 1" (vacuous until X7a) to exactly 1, and it requires `finalization.rs` among the sources.

**X8 (`crates/host/tests`).** Nine cases with census rows for unit X7a. The driver passes with 106 cases and 8 self-tests.
- **Group A:** `host_authoritative_run_raw_json.rs`, `RawDto`, E0308 "mismatched types".
- **Group B:** `host_authoritative_run_bool.rs`, `_run_id.rs` and `_replayed.rs`, `BooleanVerified`, E0308 each.
- **Groups D, E and G**, for the exported `AuthoritativeRun` under X8's export rule:
  - `_literal.rs`: D, no code, "cannot construct `AuthoritativeRun` with struct literal syntax due to private fields";
  - `_default.rs` and `_deserialize.rs`: D, E0277;
  - `_clone.rs`: E, E0277;
  - `_serialize.rs`: G, E0277.

No group F case is owed. There is no non-public inherent function, and nothing `cfg(test)` returns one: the tests write the literal from the child module.

**Inventory v125** adds 10 rows to v124, for 934 files: `finalization_tests.rs` and the nine cases.
- `finalization.rs` is already a planned row of v124, so it is kept by value.
- Every inherited row is equal by value to v124's bytes.
- The 55-row projection is carried with only its selectors moved.
- No supersession names v124, so the builder folds nothing new (`supersessionsFolded: 0`). D2's four were folded at v123 and carried through v124.
- The README lists the existing rows this unit makes out of date: `finalization.rs`, `fact_admission_tests.rs` and `admission_tests.rs`.

## Judgment calls: please rule

1. **X12's order: no pack parameter.** Pack admission belongs to the analysis request, which runs it before evaluation and so before finalization (X12 item 8). `finalize` admits no pack and wires no Plan join into replay (X12 item 9).
   - **Rejected: a `&AdmittedPack` witness parameter.** The M2 release registry has zero rows (`configuration_tests.rs`, nt1), so no production code and no host test could ever call `finalize`.
   - **Rejected: `finalize` calling `admit_policy_selection` itself.** That would admit after evaluation, which X12's forbidden substitutes refuse.
2. **The admission seam.** `finalize` takes `admit: FnOnce() -> Result<ProjectOperation, InstallationTermination>`, called only after a successful replay.
   - **Rejected: taking a `ProjectOperation`.** That would admit before the replay, against X5 item 3.
   - The closure is not a production seam that supplies a `ProjectOperation`: only security makes one.
3. **Item 5 after an uncertain outcome (X3b r10, X3d r6; X7 r5's parenthetical).** `finish` appends nothing, reconciles nothing, runs no end step and copies no floor, and the settlement reserve is forfeited. Finalization only calls `finish` and reports the durability row.
4. **The rollover already runs inside `finish`.** X3b-4 and X2e's `end` already carry `JournalOutcome::Exhausted` into the end step's rollover. X7a must finish every end path, so it cannot avoid that. Item 11's "with no rollover" is read as: X7a adds no route, admission, gate or fence of its own, and projects item 6a's row. X7b keeps the route's disclosure and item 10's rollover and crash tests.
5. **End-path disclosure is limited to what `SessionEnd` exposes.** X7a discloses `settlement_failure()` as `end_failure`.
   - The end step's own failure (`OperationEnd::Failed`) and the rollover outcome are `pub(crate)` in security, and not visible to the host.
   - **Finding for the lead:** X3d r6 item 9 and X3b item 4 say these are disclosed by the caller. That needs a `SessionEnd` accessor, which is a security change. It is recommended for X7b, which already owns the rollover rows.
6. **One after-commit detail for F16 and F39.** Every required-delivery failure after commit takes `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` with the RunId: a renderer failure, an unlawful exit, an output write or flush failure, or a latch that started no delivery.
   - The termination schema requires that detail whenever a `runId` is present, and forbids `DELIVERY.REQUIRED_PROJECTION_FAILED` with one (workflows-and-surfaces 1134–1137).
   - The remedy is the reference projection's text, verbatim.
7. **The two recovery remedies.** No registered remedy string exists for `DURABILITY.COMMIT_FAILED`, or for the F34 invariant row. X7 r5 items 3 and 5 fix the content: later read-only recovery of this ExecutionId, with the requested binding for F34, and no retry. The wording is the lead's.
8. **Item 6a's subject and remedy.** The subject is N, as S7 names "that namespace". Holders are not named, because finalization observes none. No remedy is attached: S7 fixes the retry, not a string, and the caller's renderer owns the busy row's remedy, as for every other X3d row.
9. **The delivery phase reads nothing from the store (X7 r5 item 4).**
   - `DeliveryPhase` is caller-supplied. It is lent `&PublishedCommit` only; the evaluation result is the phase's own in-memory value.
   - Finalization builds no lease, receipt or read session. A source pin requires the two exact security and storage `use` lines (the commit facade only). It refuses any lease, read entry, read receipt, read session, `SharedRead`, `installation_read`, `doctor_report`, `join_ledger`, `RecoveredCommit`, store-root, `std::fs` or `File::` name in `finalization.rs`.
   - `render` is called only after `finish` consumed the `StoppedSession`.
   - A rendered exit outside {0, 1, 3} is a renderer failure before any byte, so a success can never carry exit 2 or 4.
10. **Optional effects (F17).** There is a slot after required success. Its failure is `optional_failure`, beside an unchanged outcome. The implementations are M3's.
11. **X9 points.** `x7.delivery.required` wraps render and output together, and `x7.delivery.optional` wraps the optional effects. Both are fallible, and an injected fault maps to that step's own failure. The scope was already in X9-0's registry.
12. **How the tests inject outcomes.** `Committed` holds a `PublishedCommit`, and `CarrierCapacityExhausted` a security value; neither is buildable in host tests.
    - The pure stage `project(Concluded)` carries every row.
    - The tests write `AuthoritativeRun`'s literal from the child module.
    - `Joined::from` is tested for every outcome a caller can construct.
    - `deliver` is generic over the commit value, so the phase is tested over `()`.
    - There is no `cfg(test)` constructor.
13. **The extra X8 rows.** X8 r3 assigns X7a rows A and B. Exporting `AuthoritativeRun` brings it under the export rule, so its full capability set (D, E, G) is added. `EphemeralRun` stays `pub(crate)`, so it is not exported.
14. **`ExistingAttempt`'s requested binding is disclosed in part until X6b lands.** X7 r5 item 3 discloses the four members of `requested`. X6b has not integrated `NotPrepared::ExistingAttempt { execution_id, requested: RequestedBinding }`, so the variant today carries only the ExecutionId.
    - **What X7a discloses now:** the ExecutionId as subject, and the session's N beside the row. N is `requested.namespaceId` by X6 r3 item 1's construction, since storage builds it from the session's N.
    - **What the arm does:** it matches `{ execution_id, .. }`, so it compiles before and after X6b.
    - **What follows:** the other three members (store generation digest, carrier digest, operation reference) are disclosed by whichever of X6b and X7a integrates second, as item 10 says.
    - **Rejected:** recomputing the store generation digest in the host. Storage owns that recipe.
15. **The `REPLAY_LIMITS` pin** is tightened in X5a's test file to exactly one caller, as X5 r3 item 5d anticipated.
16. **Session-level integration tests are not in this unit.** A host test cannot build a `ProjectOperation`. Security's fixtures are `cfg(test)` in security only, and neither X9-1's `crash_matrix_support` nor X8b's `scenario-fixtures` is integrated (X9 r1 gap G1, which already amends X7 item 10).
    - **What X7a does test with real code:** the real replay through `finalize`. A replay refusal ends before admission. Admission runs once after a successful replay, and its refusal is its own row.
    - **Recommended:** the session rows (committed and delivered, renderer failure after commit, latch, undetermined with N, `ExistingAttempt` with its binding, exhaustion through `finish`) land with X8c or X9-5, or as an X7a-2 after X9-1.
17. **`Finalization` is typed, not rendered.** Rendering the v7 envelope is X11's and M3's. X7a returns the row, the retained RunId, the remedy it owns, N where a later recovery needs it, and the disclosures.
18. **Subjects on the invariant and durability rows.** The ExecutionId is the subject on the durability row and on the F34 invariant row, as X7 r5 item 3 states. The installation projection's invariant row otherwise carries no subject. Only these two rows of finalization add one, and only they carry `namespace`.

The lead's view is that none of these needs a law change. It recommends recording calls 4, 5 and 16 in X7's next record-only revision.

## Tests

**`finalization_tests.rs`: 21 tests.**
- **Item 3's table:**
  - delivered at exits 0, 1 and 3, with and without an optional failure;
  - failed and latched delivery, on the delivery row with the RunId and no namespace;
  - undetermined, with the ExecutionId subject, N beside it, and the remedy;
  - eleven refusal rows, unchanged, with no namespace;
  - existing attempt, as the invariant row with the ExecutionId subject, N and its remedy;
  - exhaustion, as the busy row naming N.
- **Joining outcomes:** every caller-constructible `CommitOutcome` and `NotPrepared` joins one outcome.
- **End failures:** five settlement failures are disclosed beside the outcome and never rewrite it.
- **The delivery phase:**
  - a latched commit starts nothing;
  - a delivered response settles its exit and flushes once;
  - a renderer failure, an exit of 2, 4 or 130, a write failure and a flush failure each fail once, with no retry and no optional effect;
  - an optional failure never changes the exit.
- **Order, over the replay corpus:**
  - a replay refusal ends before admission, with the replay join's row and remedy;
  - admission runs once after replay, and each of four admission rows stands as its own.
- **DR-G27:** the ephemeral label is never authoritative and has no RunId.
- **Source pins:**
  - no other host module calls `replay_candidate`, `CommitSession::open`, `prepare_commit`, `.publish()`, `.finish()` or `authoritative_run`;
  - `finalize`'s order is replay, admit, open, prepare, publish, finish, deliver; each step runs once, and `finish` appears twice;
  - no recovery, read receipt or session, admission, gate, ledger, scope, charge, settle, lifecycle, rollover, fence, loop, retry, wildcard, `unwrap` or `expect`;
  - item 4's pin: the exact security and storage `use` lines, and no lease, read entry or storage reader;
  - exactly one authoritative literal, inside `authoritative_run(commit: &PublishedCommit)`, and one `-> AuthoritativeRun`;
  - the derive line is exact, with no `From`, `bool` authority, `Clone` or `Default`;
  - exactly the two `x7.delivery` points.

**`fact_admission_tests.rs`:** the caller pin now requires exactly 1.

**Host driver:** 106 cases (9 new) and 8 self-tests.

## Checks

Product checks are at 81214cb plus this diff. Arch verifiers run against the real lock at 81214cb, which selects v124.
- **Workspace runs:** two full runs of `cargo test --locked --offline --workspace --all-targets` on the final bytes, each with its own private 0700 TMPDIR: each with 1637 passed, 0 failed and 3 ignored, across 17 test binaries. The diff's sha256 was the same before and after the runs.
- **Lints:** `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` is clean.
- **Formatting:** `cargo fmt --all -- --check` is clean, and so is `rustfmt --edition 2024 --check` on `finalization_tests.rs` and `fact_admission_tests.rs` (both `include!`d).
- **`check_package_edges --lane host`:** passes against v124 and against v125, with 20 declared and 20 resolved edges. No edge is new.
- **verify_scratch:** v125 is appended in memory to the worktree's lock at 81214cb, with the inheritance replaced by the record's 55 rows. It passes with 85 inventory successors, 74 contract successors and 55 inheritance rows, and v125 is selected.
- **verify_projection against the real lock:** 55 rows; 278 corruptions refused.
- **`build_v125.py`:** reruns produce the same bytes. 934 files; the 924 v124 rows are equal by value; 55 projection rows; 0 supersessions newly folded.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does X7a meet X7 r5 items 1 to 5 and 8, and item 10 as far as gap G1 allows? In particular:
  - the one coordinator, and its order;
  - finishing before delivery on every end path;
  - no delivery when latched;
  - a delivery phase that reads nothing from the store;
  - only `&PublishedCommit` labels authoritatively;
  - the ephemeral projection;
  - every row, with its RunId, ExecutionId and namespace;
  - no recovery, retry, admission, gate, fence or ledger of its own;
  - the exhaustive matches;
  - the `x7.delivery` points;
  - the `REPLAY_LIMITS` pin.
- Rule on calls 1 to 18, and say whether any of them needs a law change rather than a reading.
- Do the nine cases and their census rows meet X8 r3 for X7a?
- Is v125 right on v124, including the 55-row projection?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `finalization-x7a-inventory-v125-subject.json` (lead's value in hashes.txt);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v125, parent (the v124 pin), successorRecord (the pin of `finalization-x7a-inventory-v125/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
