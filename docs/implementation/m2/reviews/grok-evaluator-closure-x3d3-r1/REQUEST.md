Grok review: unit X3d-3 r1, the commit path's evaluator-closure binding (law X3d r8 item 13, contract successor EC1), with the synthetic run candidate moved here from X9-2 (law X9 r7), and inventory v130 on v129. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-evaluator-closure-x3d3-r1. If you build or test, use a CARGO_TARGET_DIR under that directory and a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder. Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read the private 413 UUID fixture.

## Inputs

- **Laws.** All are pinned in `hashes.txt`.
  - **X3d r8** (`docs/implementation/m2/commit-session-x3d/PROPOSAL.md`, accepted). Item 3 step 1 compares the Run's evaluator closure with the session's core evaluator closure. Item 2 has `open` bind that value. Items 1 and 12 (holds cell; binding values from a real session). Item 13 defines X3d-3. Also the r8 forbidden substitute.
  - **EC1** (`docs/implementation/m2/core-evaluator-closure-ec1/`, bound at product 9d3b84b). The rule: the evaluator closure is closure2: + H("closure", D′), where D′ is the authenticated core descriptor with `kind` set to `"evaluator"`, and manifestDigest = SHA-256 of the TR-CORE inventory body. The test vector is `evidence/vector.json`, case `baseline-macos`.
  - **X9 r7** (`docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`, accepted). The r5 header and the r7 record together define the candidate: inputs only; it rewrites the `projectId` and the evaluator closure to the session's; it retains the closure's descriptor, its manifest blob and its tree blobs; it recomputes ids; it re-derives the outputs with `derive_evaluation`; and `replay_run` stays the only mint.
  - **X8 r4** (`docs/implementation/m2/refusal-suite-x8/PROPOSAL.md`). Item 4b: one site list, one joint predicate, extended by name.
  - **The r8 review** (`reviews/grok-evaluator-closure-x3d-r8/REVIEW.md`). It describes how X3d-3 should be shaped.
- **Product.** Worktree `/Users/sb/code/opensip-ai/opensip-x3d3`, detached at main `9d3b84b` (EC1 bound; X8b at 4faf729 below it). Nothing is committed. The one new file is intent-to-add. `git diff 9d3b84b` is 68691 bytes, sha256 `2563bc6c80578af8a445f756af5662acf56740de8074bcd14cd4467fcd088807`: 13 files, +1135 −65. Every file is pinned in `hashes.txt`.
- **Toolchain.** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`.

## What X3d-3 builds

### Security

- **`trust/core_inventory.rs`.**
  - `Projection` gains `evaluator_closure`, with an accessor beside `closure()`.
  - `bind` computes it from the descriptor it already builds, through `evaluator_descriptor(core)` (a clone with `kind` set to `"evaluator"`) and the same `hash_canonical_value("closure", …)`. That hash is now factored as `closure_id`, so the core closure's value is unchanged.
- **`trust/initial_core.rs`.** `InitialCore::evaluator_closure()` reads `release.authentication().core().inventory()`, exactly as `closure()` does, so it behaves the same on the running arm and the injected arm.
- **`custody/read_premise.rs` and `custody/operation_handoff.rs`.** `PlatformReceipt::core_evaluator_closure()` and `ProjectOperation::core_evaluator_closure()` are read-only `&str` values beside `selected_core()`, which is unchanged.
- **`custody/commit_session.rs`.**
  - `pub fn core_evaluator_closure(&self) -> &str` reads through the operation, as `core_closure()` does.
  - `core_closure()`'s doc comment no longer says that a Run's evaluator closure must equal it. Its value and its other uses are unchanged.
  - The header comment says `open` binds the value.
- **The shared test-support accessor (one accessor, on X8's one site list).**
  - `CommitSession::core_evaluator_closure_preimages()` is `#[doc(hidden)]` and gated `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`. It returns `(JsonValue descriptor, Vec<u8> inventory body, BTreeMap<String, Vec<u8>> tree bytes by logical path)`.
  - It reaches the core through two crate-private hops under the same predicate, `ProjectOperation` and then the write receipt.
  - The read itself is `InitialCore::evaluator_closure_preimages()`, inside `initial_core.rs`'s existing joint-predicate `tests` module, so that module gets no new site. It opens each tree member of the platform row through `open_release_file`: no-follow opens by exact name below the retained tree root, judged by the core-tree predicate. It checks each member's SHA-256 and length against the inventory.
  - `crash_matrix_sites.rs` gains three rows, one joint-predicate site in each of `commit_session.rs`, `operation_handoff.rs` and `read_premise.rs`. Its doc names them as shared gate 5, added by name.
  - No production path calls the accessor.

### Storage

- **`commit.rs`.**
  - `Bound.evaluator_closure` comes from `CommitSession::core_evaluator_closure()`, and `plan` compares the Run with it.
  - `Bound.core_closure` is removed: step 1 was its only use (judgment call 3).
  - The `PlanRefusal::Closure`, `plan` and `prepare_commit` doc comments name the core evaluator closure. The row is unchanged: a mismatch is still the invariant row.
- **`crash_matrix_support/run_candidate.rs` (new; declared in `crash_matrix_support.rs`, which forwards its names).** The synthetic run candidate, `synthetic_run_candidate(&CommitSession) -> SyntheticRunCandidate`. It returns inputs only: retained objects, blobs, the claimed RunId, a `retained_inputs()` view over storage's schema registry, and the `synthetic` label. `synthetic_replay_limits()` gives the bounds. The steps:
  1. Start from the pinned corpus Run that security's SEAL tests replay (`journal-seal-cases.json`, `packet-0-original`, compiled in with `include_bytes!`).
  2. Find the outputs by deriving once over the corpus: `derive_evaluation`'s objects and blobs, plus the proof, evidence, seal and Run. Everything else is an input.
  3. Rewrite the inputs, to a fixpoint. The snapshot's `projectId` becomes `project_id()`, and the corpus evaluator closure's hex becomes `core_evaluator_closure()`'s. Every input whose identity or digest changes adds its own old and new hex to the map. Each pass starts from the original bytes and keeps the latest identity per original.
     - An array that was in canonical byte order is re-sorted, for example `semanticClosures` and refs ordered by `digest`.
     - A canonical JSON blob is rewritten as a value. Any other blob is rewritten byte for byte, with the same length asserted, because framed blobs carry length prefixes.
     - The corpus evaluator closure is dropped, with its own manifest blob.
  4. Retain the session's closure: its descriptor, the inventory body as its manifest blob, and its tree blobs, all from the accessor. Before using them, assert that the descriptor's id is `core_evaluator_closure()`, that it has `kind: "evaluator"`, and that it differs from `core_closure()`.
  5. Re-derive the outputs with `derive_evaluation` over the rewritten inputs. Its input references are the corpus proof's `evaluationInputRefs` under the same map: a selection of inputs, not an output.
  6. Build the semantic evidence, seal and Run exactly as `replay_run` checks them.
  - It never returns a `ReplayedRun`.
  - Two `#[cfg(test)]` helpers serve the tests below: `project_rebound_corpus` (step 3 with only the project mapped) and `renaming_the_evaluator_closure` (the whole candidate renamed to a given closure descriptor).
- **`commit_tests.rs`.**
  - It includes the same `run_candidate.rs` by `#[path]`, with `#[allow(clippy::duplicate_mod)]` (judgment call 4).
  - `bound(execution, operation)` takes `project` and `evaluator_closure` from `session_values()`. That function opens a real `CommitSession` once per process over X8b's `ScenarioHome::operation`, which is a first registration on a synthetic installation. It records the two values and `core_closure()`, builds the candidate for that session, ends the session (`reserve_end_path`, `refused`, `finish`), and drops the home. `bound()` never reads a Run.
  - `replay()` is now `replay_run` of that candidate. The positive tests in `commit_tests.rs`, `recover_tests.rs` and `sweep_tests.rs` replay it, and `bound()` lost its Run argument in all three files.
  - Tests:
    - **`a_run_of_another_project_or_closure_does_not_bind`.** The candidate binds: its Run names the session's project and closure, and `plan` succeeds. Another project is refused `Project`, and another closure is refused `Closure`.
    - **`a_corpus_run_does_not_bind_to_a_real_session`** (the rewritten mismatch test).
      - The raw corpus Run is refused `Project` first.
      - The corpus Run with only its project rebound replays, keeps the corpus evaluator closure, and is refused `PlanRefusal::Closure`.
      - The same Run, rebound to a fresh real session's project, goes through `prepare_commit` and is refused `NotPrepared::Refused(Invariant)`. Nothing is written under `I/stores/S/projects/N`. `finish` appends the `REV`, so the carrier holds one `REV` and no `SEAL`.
    - **`the_core_closure_is_not_the_evaluator_closure`.**
      - The session's `core_closure()` differs from `core_evaluator_closure()`.
      - The retained closure is `kind: "evaluator"`, and the same descriptor with `kind: "core"` hashes to `core_closure()`.
      - A Run renamed to name the core closure is refused by `replay_run` with `Structure(Graph(Input(Candidate(Schema(Mismatch)))))`.
      - The control: the same rename to another `kind: "evaluator"` closure replays.
    - **`the_first_real_commit_composes_prepare_commit_and_publish`** (the first real composition):
      - A fresh scenario home and session, the candidate for it, and `replay_run` after `open` (judgment call 7).
      - The closure's manifest and tree blobs are among the retained evidence.
      - `prepare_commit` then `publish` gives `CommitOutcome::Committed`, with the RunId and ExecutionId, sequence 1, and no latch after admission.
      - `finish` appends neither `REV` nor `CLN`, has no settlement failure, and enters the end step.
      - The carrier census is one `SEAL`, zero `REV`, zero `CLN`.
      - The ledger holds exactly the published receipt bytes, which parse to (RunId, ExecutionId, N), and an `admitted` attempt row.
      - The store's `objects/sha256` equals exactly the retained frames' and blobs' digests.
- **`core_inventory.rs` tests.**
  - **`ec1_vector_core_evaluator_closure`** reproduces EC1's vector byte for byte from the fixture case `baseline-macos`: a 5990-byte body, both ids (`closure2:54322a2c…118d`, `closure2:7da97b9a…89e2`), both descriptors' canonical SHA-256 (`b1158c4b…c972`, `2e777ad0…ffa8`), manifestDigest `1d012c7d…ac5d` equal to the body's SHA-256, and the two kinds.
  - **`every_accepted_case_has_a_distinct_core_evaluator_closure`** checks all 53 accepted `core-inventory318` cases: the descriptors are equal except `kind`, the evaluator id is its recipe, and the two ids differ.

**Not changed:**
- no trust record, signed release format, component manifest or 463h builder;
- no schema source, generated report, `identity/src/closure.rs` or `view-joins-registry.json`;
- no `Cargo.toml`, `Cargo.lock`, feature or edge;
- no host file.

## Judgment calls (narrowest choice consistent with the laws)

1. **The accessor's reach.** The fields on the way are private to `operation_handoff` and `read_premise`, so the one public accessor needs two crate-private hops. Each hop is gated by the joint predicate, which gives three new pin rows in total. The read sits in the existing gated `initial_core` `tests` module, which can reach `InitialCore`'s private tree root, so no fourth site is needed. Rejected: an ungated `&InitialCore` lending through the receipt and operation, because the law calls those hops "read-only values".
2. **The accessor's shape and ledger.**
   - It returns a plain tuple, so no new public type is added.
   - Tree bytes are read on a fresh unbounded `WorkLedger`, not on the session's attempt ledger, so test support never spends the operation's budget.
   - A member that cannot be read or differs from the inventory panics, as fixtures do.
3. **`Bound.core_closure` is replaced, not kept beside the new field.** Step 1 was its only use, so keeping it would leave a dead field. `CommitSession::core_closure()` keeps every other use.
4. **Where the candidate compiles.** It is storage's `crash_matrix_support/run_candidate.rs`, under that module's existing gate. Storage's plain test build has no support module, so `commit_tests.rs` includes the same file by `#[path]` rather than gating it anew. No cfg site is added and no copy of the source exists. With `crash-matrix` in a test build, both copies compile, so clippy's `duplicate_mod` is allowed on the include. The two test helpers are `#[cfg(test)] #[allow(dead_code)]`, because the feature's copy never calls them. Rejected:
   - widening storage's pinned support-module predicate to `test`;
   - a second copy of the source.
5. **The candidate's input.** It takes `&CommitSession` read-only and calls only `project_id`, `core_evaluator_closure`, `core_closure` (to assert inequality) and the accessor. X9 r5 says the candidate reads the session's getters. The "accepts no session" rule in item 6 is about the three driver entries.
6. **The rewrite method.** The law says "recomputes every content id and blob digest that depends on them" but gives no algorithm. The method is a reference rewrite over the inputs to a fixpoint, with canonical order preserved. The output set is found by deriving over the corpus first, so no output is ever rewritten textually: `derive_evaluation` re-derives all of them (the r5 rejection stands). The corpus's own evaluator closure and its manifest blob are dropped rather than left as unread inputs.
7. **Test order.** The first real commit replays after `CommitSession::open`, the order X9 r5 states for matrix children. The candidate needs the ProjectId that the first registration draws. Replay is pure and takes no custody, so no X3d step changes. The host's order (replay before custody, X5 r3) is X9-5's and is untouched.
8. **The mismatch test's Run.** Item 13 asks for "a pinned corpus Run … refused `PlanRefusal::Closure`". `plan` checks the project first, and the binding must come from the session. So the test uses the corpus Run with only its project rebound (its closure is the corpus's) and also asserts that the raw corpus Run is refused `Project`. Rejected: a binding with the Run's project, because r8 forbids binding values copied from the Run.
9. **Session values once per process.** A `OnceLock` holds one real session's values and candidate, and that session then ends and its home is removed. The binding values still come from a real session, and the suite pays for one installation rather than one per test. The end-to-end test opens its own session.
10. **The EC1 vector is pinned as constants in the test.** The case's body comes from the existing product fixture. Copying `vector.json` into the product would add a fixture file and an inventory row for the same values.
11. **The core-closure refusal is pinned exactly.** `replay_run` refuses it at the identity schema check of the retained closure: `Structure(Graph(Input(Candidate(Schema(Mismatch)))))`. A control rename to another evaluator-kind closure replays, so the refusal is the kind and not the rewrite.
12. **Exports.** `crash_matrix_support` exports `SyntheticRunCandidate`, `synthetic_run_candidate`, `synthetic_replay_limits` and `SYNTHETIC_LABEL`. Host forwards storage's surface unchanged. X9-2 replays with the same bounds.

## Checks on 9d3b84b with this diff (private TMPDIR)

- **Full workspace, twice:** `cargo test --locked --offline --workspace --all-targets` gave 1714 passed, 0 failed, 3 ignored both times. X8b's baseline is 1709. The difference is the five new tests:
  - `ec1_vector_core_evaluator_closure`;
  - `every_accepted_case_has_a_distinct_core_evaluator_closure`;
  - `a_corpus_run_does_not_bind_to_a_real_session`;
  - `the_core_closure_is_not_the_evaluator_closure`;
  - `the_first_real_commit_composes_prepare_commit_and_publish`, the first real end-to-end commit.

  Every existing commit, recover and sweep test now runs on the candidate bound to a real session. An earlier full run, before the final comment, type-alias, lint-allow and test-strengthening edits, also gave 1714/0/3.
- **Crash-matrix lane:** `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets` gave 1599 passed, 0 failed, 3 ignored. X8b's figure was 1594. The pinned censuses are unchanged.
- **Scenario lane:** `cargo test -p opensip-security -p opensip-storage --features scenario-fixtures --all-targets` gave 1139 passed, 0 failed, 2 ignored. X8b's figure was 1134.
- **Clippy `-D warnings`:** clean on the workspace, on the four crates with `crash-matrix`, and on security and storage with `scenario-fixtures`. The only allow added is `clippy::duplicate_mod` on the include (judgment call 4).
- **Format:** `cargo fmt --check` is clean.
- **Package edges:** `check_package_edges --lane host` passes against v129 and against v130, with 22 declared internal edges and 20 resolved.
- **Site pin:** `crash_matrix_sites` passes with the three new rows in every lane.
- **Release absence:** `cargo build --release -p opensip-cli` gives `target/release/opensip`, 6315264 bytes, sha256 `bc7181f935530e936d2a954f2eb5d95c2d7032001708a5a2d48ec817ba6bc8e3`.
  - It differs from X8b's binary, because `bind` now also computes the evaluator closure.
  - None of these ten candidate or accessor strings is present: `core tree member`, `a framed blob's reference keeps its length`, `the rebound inputs derive`, `the corpus derives`, `packet-0-original`, `storage's selected schema registry`, `SyntheticRunCandidate`, `core_evaluator_closure_preimages`, `evaluator_closure_preimages`, `journal-seal-cases`. The positive control `CORE.NO_EMBEDDED_RELEASE` is present.
  - `cargo tree -e features -p opensip-cli` names neither test feature.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Inventory v130

`evaluator-closure-x3d3-inventory-v130/evidence/build_v130.py` adds one row, `crates/storage/src/crash_matrix_support/run_candidate.rs` (service, `opensip-storage`), to the parent the lock selects. That parent is inventory129 (X8b), 545917 bytes, sha256 `139f9331b43288fe55e4c7526c4243263d04186afd8e973a43f291784da259d0`.
- 963 inherited rows are equal by value, for 964 files. Packages, edges, pending decisions and carried obligations are unchanged. The builder asserts the storage → security, evaluator and identity edges.
- The fifty-five inheritance rows are re-projected by stable path: sixteen carried, D1's thirty-nine, and D2's four supersessions already folded. `supersessionsFolded` is 0, since EC1 supersedes no inventory row.
- The README lists each changed existing row and which descriptions go out of date by omission: `commit_tests.rs`, storage's `crash_matrix_support.rs`, `crash_matrix_sites.rs`, `commit_session.rs`, and host's `crash_matrix_support.rs` ("joins it with X9-5").
- Reruns are byte-identical. The builder refuses tracked paths and refuses a lock that already selects v130.

Pins:
- v130: 547706 bytes, sha256 `80e1e2e5028c8d979bfb7e3ccf710fd3a72f0018998ff013c3cb22f7ceb69855`.
- successor.json: 145124 bytes, sha256 `10ce6d544356901913132513c05b3f3d917b6dabbd32b84fdac1d4c2c00cf624`.
- Subject manifest `evaluator-closure-x3d3-inventory-v130-subject.json`: 2164 bytes, sha256 `d694b12356fac632d75165c03782f19954f3990970d71579b6fceefac3b77880`.

Verification:
- `verify_projection` against the real lock at 9d3b84b: PASS, 55 rows, 278 corruptions refused.
- `evidence/verify_scratch.py` appends v130 in memory over the worktree's lock, with a synthetic review and assent. It passed: 91 inventory successors, 75 contract successors, 55 inheritance rows, v130 selected.
- `check_package_edges --lane host` passes against v129 and v130: 22 declared internal edges and 20 resolved.

## Decide

- Does X3d-3 implement X3d r8 item 13 faithfully?
  - EC1's value from `Projection` to `CommitSession::core_evaluator_closure()`;
  - `Bound` and `plan`;
  - the one shared accessor on the site list;
  - the candidate per X9 r5 and r7;
  - the four required tests.
- Does it add nothing of X8c's or X9-2's?
- Is the session side of step 1 taken only from security's authenticated inventory, never from a Run, a worker claim, a build-time string or a binding copied from the Run (the r8 forbidden substitute)?
- Is every new test-feature site on the pinned list, extended by name? Is the accessor absent from every release build, and called by no production path?
- Is the candidate inputs-only? Are its outputs truly re-derived, with `replay_run` the only mint?
- Is the first end-to-end commit a real composition (`CommitSession::open` over the production chain, `prepare_commit`, `publish`, `finish`)?
- Is each judgment call acceptable? Is v130 right on v129?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `docs/implementation/m2/evaluator-closure-x3d3-inventory-v130-subject.json` `d694b12356fac632d75165c03782f19954f3990970d71579b6fceefac3b77880`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path `docs/implementation/m2/repository-file-inventory.v130.json`, bytes 547706, sha256 `80e1e2e5028c8d979bfb7e3ccf710fd3a72f0018998ff013c3cb22f7ceb69855`, parent (the v129 pin above), successorRecord (path `docs/implementation/m2/evaluator-closure-x3d3-inventory-v130/successor.json`, bytes 145124, sha256 `10ce6d54…`)}.

Write REVIEW.md and review.json. Do not commit.
