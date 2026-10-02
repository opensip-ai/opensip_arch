Grok review: unit X8c r1, the behavioural refusal cases B0 to B8 of law X8 r4 (item 5, item 5a, "Units after the law"). Claude Opus 5.5 leads, and you are the single reviewer. Make no repository edits, commits, pushes or delegations. Write only under `/tmp/opensip-implementation/reviews/grok-refusal-cases-x8c-r1`.

If you build or test:
- use a `CARGO_TARGET_DIR` under that directory;
- use a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees (X9-2 is in flight) churn the shared temp folder.

Rules:
- Run git only read-only, and only against the worktree below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent (it is).
- Never read the private 413 UUID fixture.

Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`, Python `python3.14`.

## Subject

The worktree is `/Users/sb/code/opensip-ai/opensip-x8c`, detached at product main `a2c5e8b` (X3d-3 integrated, with X8b, X9-1, X3d-1/2, X4a, X4T-b, X5a and X7a below it). Nothing is committed.

The one changed file is `crates/host/tests/admission_tests.rs`: +1025 −1. The −1 is the file's header comment, which gains one sentence naming X8c.
- **No file is added,** so there is no inventory successor. The role of `admission_tests.rs` is unchanged.
- **Untouched:** no product source, manifest, lock, feature or edge.

Save `git -C /Users/sb/code/opensip-ai/opensip-x8c diff a2c5e8b` as `subject.diff`. It is 45278 bytes, sha256 `8b394a1b8a9c7f2079a9c49b43394c0cf48c60676da356322f3f4e3e9d6b712f`. Every input is pinned in `hashes.txt`.

## Laws

- **X8 r4** (`refusal-suite-x8/PROPOSAL.md`, accepted): items 4c to 4e, 5 and 5a, the B table, "Units after the law" (X8c), and the forbidden substitutes under "Behavioural cases".
- **EXIT-PLAN.md corrections since r4:**
  - **B2's wording** compares against `CommitSession::core_evaluator_closure()` (X3d r8, EC1). The owner is "X3d-2, binding X3d-3". B6 still names the core closure.
  - **B0's Run** is storage's synthetic run candidate (X3d-3), by the narrowest lawful route.
  - **B4 / `ExistingAttempt`** stays on the invariant row, with the binding disclosed (X6 r3, X7 r6).
  - **B8** is a replay `Mismatch` refusal before any fence (X5).
- **Supporting laws:** X3d r8 (item 3 step 1, item 7's end path, item 13's candidate), X9 r7 (the candidate, item 3's helper shape, r5's matrix order), X4 r7 items 4, 5 and 8, X5 r3 item 3, and X6 r3 item 6.

## What X8c adds (all at the end of `admission_tests.rs`, `cfg(target_os = "macos")`)

**Support.**
- **`mod schema_sources`.** A test-crate shim, `registry()`, over host's public `embedded_schema_registry()`. The candidate source names `crate::schema_sources::registry()`.
- **`mod run_candidate`.** It is `#[path = "../../storage/src/crash_matrix_support/run_candidate.rs"]` with `#[allow(dead_code)]`: X3d-3's file, unchanged, included as storage's own `commit_tests.rs` includes it.
- **`mod x8c`.** It holds:
  - the case scratch layout;
  - `open`, which runs `ScenarioHome::create`, then `project`, then `operation` (X8b's production chain), then `CommitSession::open`, and asserts a fresh namespace;
  - the census;
  - `refused_end`;
  - the public projection via `opensip_host::installation_termination`;
  - `candidate_replay`, which is `replay_run` over `synthetic_run_candidate(&session)`;
  - `Corpus`, which reads host's pinned `tests/fixtures/replay-fixtures.json` and holds B8's alteration;
  - item 5a's helper (`helper_publish` and `publish_through_helper`);
  - `replace` and `another_generation`.

**Tests (12 new).**
- `x8_helper_publish_revocation`: item 5a's entry.
- `the_candidate_registry_is_storages_selected_registry`: host's and storage's `SOURCES` name the same 48 files in order, which pins the shim.
- Ten `synthetic_*` cases:

| Case | Test | Alteration (point) | Asserted outcome and row | Census after `finish` |
|---|---|---|---|---|
| B0 | `synthetic_b0_the_lawful_control_commits` | none | `Committed`, `latched_after_admission() == false`, RunId and ExecutionId, sequence 1, `authoritative_run(&published).run_id()` | SEAL 1, REV 0, CLN 0; 1 receipt; one attempt row for the ExecutionId; `finish`: no REV/CLN, end step entered, no failure |
| B1 | `synthetic_b1_another_runs_replay_does_not_bind` | `ReplayedRun` of another corpus Run (`replay-fixtures.json` `packet-1-original`; its `projectId` is not the session's) | `NotPrepared::Refused(Invariant)` → `SYSTEM.OUTCOME.ILLEGAL_STATE` / `HOST.INVARIANT_VIOLATED` | SEAL 0, REV 1, CLN 0; ledger absent (no attempt row, no receipt) |
| B2 | `synthetic_b2_another_evaluator_closure_does_not_bind` | X3d-3's `project_rebound_corpus(session.project_id())`: the project binds; the evaluator closure is neither `core_evaluator_closure()` nor `core_closure()` | the same invariant row | as B1 |
| B3 | `synthetic_b3_a_replaced_marker_is_refused_at_the_checkpoint` | `.opensip/project-id.v1` replaced (same bytes, new inode, `cp -p` then rename), after the handoff and `open` | `prepare_commit` admits the attempt; `publish` → `Refused(Custody{required-files-changed})` → `CONFIG.INVALID` / `CONFIG.CUSTODY_REFUSED` / `required-files-changed` | SEAL 0, REV 1, CLN 0; attempt `admitted`; 0 receipts |
| B3 | `synthetic_b3_a_replaced_lease_file_is_refused_at_the_checkpoint` | N's `writer.lease` replaced the same way, separately | the same custody row | as above |
| B4 | `synthetic_b4_an_existing_attempt_is_not_overwritten` | `storage::scenario::plant_attempt(session.execution_id())` before `prepare_commit` | `NotPrepared::ExistingAttempt` with that ExecutionId and `requested`: namespace, carrier digest and operationRef equal to the session's; 64-hex generation digest. Invariant row (X7a projects it with the ExecutionId as subject) | REV 1, SEAL 0; the ledger census equals the census right after planting (the planted row, unchanged and alone); 0 receipts |
| B5 | `synthetic_b5_a_lineage_node_naming_another_generation_is_refused` | the selected lineage node replaced by the same canonical node with `storeGeneration + 1` | the custody row, as B3 | as B3 |
| B6 | `synthetic_b6_a_live_revocation_of_the_core_closure_is_refused` | after the handoff and `open`, the item 5a helper process publishes `[("release", session.core_closure())]`; the test thread waits for it to exit | `Refused(RevokedDuringOperation{trust-revoked})` → `EXTENSION.ADMISSION_REJECTED` / `TRUST.COMPONENT_REVOKED_DURING_OPERATION` / `trust-revoked` | as B3 |
| B7 | `synthetic_b7_an_unrelated_revocation_still_commits` | the helper publishes `[]` (names nothing) | `Committed`, not latched | as B0 |
| B8 | `synthetic_b8_an_altered_claimed_output_never_replays` | one byte of a claimed output (see judgment call 6) | `replay_run` → `Mismatch{EVALUATOR_COMPLETE_PROOF_REPLAY, target: None}`, after the unaltered Run is shown to replay | no `operation` call: no `.opensip` in the root, no entry in `I/host/projects`, no `I/stores/S/projects` |

**Item 5a's helper, as built:**
- **The entry.** An ordinary `#[test] fn x8_helper_publish_revocation`, not ignored and at the crate root, so `--exact` names it. It returns at once unless `OPENSIP_X8_HELPER` is set.
- **The command.** `current_exe() --exact x8_helper_publish_revocation --nocapture --test-threads=1`.
- **The environment.** `env_clear()`, then only `OPENSIP_X8_HELPER=publish-revocation`, `OPENSIP_X8_INPUT` (a canonical-JSON input file: home, installation, store, subjects) and `TMPDIR`.
- **The publication.** It goes through `scenario::publish_revocation_fenced` and writes one `X8|published|<before>|<after>` record to stderr.
- **What the test thread checks** before calling `prepare_commit`:
  - the exit status;
  - `running 1 test`, `test x8_helper_publish_revocation ... ok`, and `test result: ok. 1 passed; 0 failed; 0 ignored;`;
  - exactly one record;
  - `after > before`;
  - `before == revocation_version(home)` read before the spawn;
  - `revocation_version(home) == after` after the exit.
- **No sleep anywhere.** The wait is `Command::output()`.

## Judgment calls (narrowest choice consistent with the laws)

1. **B0's Run route.** The candidate lives in storage's `crash_matrix_support`, gated `all(feature = "crash-matrix", target_os = "macos")`. No manifest may enable `crash-matrix` (X9 item 2), so host tests under `scenario-fixtures` cannot name it.
   - **Narrowest route: X3d-3's own `#[path]` include.**
     - The candidate's only crate-private reference is `crate::schema_sources::registry()`. A test-crate shim satisfies it over host's public `embedded_schema_registry()`, which compiles the same 48 pinned source files in the same order. A new test pins that.
     - The preimage accessor it calls (`CommitSession::core_evaluator_closure_preimages`) is on X8 item 4b's shared site list, which `scenario-fixtures` reaches.
     - The included copy is a test-crate module, not a `crash_matrix_support` item. X9's "never compiled under `scenario-fixtures` alone" governs X9's three driver entries, and storage's unit tests already include the same file.
   - **No product file, cfg site, feature, export or law changes.**
   - **Rejected:**
     - widening storage's support gate or the site list (a law change);
     - enabling `crash-matrix` from host (forbidden);
     - a second copy of the candidate.
2. **Replay order.** B0 to B7 replay after `CommitSession::open`, in the order X8 item 5 lists, because a first registration draws the ProjectId inside the operation (EXIT-PLAN limit (a); X9 r5's order). Replay is pure and takes no custody. B8 replays before any fence (X5 r3 item 3). The host's own order inside `finalize` (`pub(crate)`) is untouched.
3. **The corpus.** Item 5 names "a corpus Run from `crates/evaluator/tests/fixtures`", but that directory holds no Run (only policy-pack fixtures). The cases use host's pinned replay reference `crates/host/tests/fixtures/replay-fixtures.json`, the corpus `independent_run_replay_matches_selected_reference_and_owns_its_closure` pins. B1 uses `packet-1-original`, which is "another corpus Run" than the candidate's `packet-0-original`. B8 uses `selected-complete-file-positive`, a Run with findings. A record note is owed.
4. **REV for B1, B2 and B4.** The B table's census for these rows lists no REV, but X3d r6 item 7, as integrated, owes one: every certain refusal before admission latches the gate (`refused()`), and `finish` appends a REV (`operation-stopped`). The cases assert REV 1 and CLN 0 exactly. This adds to the table and does not contradict it.
5. **End step after a refusal.** Every refusal case asserts `end_step_entered() == false`, with no settlement or end-step failure. The refusal closes the attempt ledger, and X3d item 7 / `SessionEnd` defines not entering the end step as not a failure. B0 and B7 assert that the end step was entered.
6. **B8's "one byte of a claimed output".** One-byte edits elsewhere stop replay earlier, as I/O-shape refusals rather than `Mismatch`. The probes:
   - in place, they fail identity or schema checks;
   - in run, seal or proof fields, they fail joins (`REFERENCE_SOURCE_JOIN`, `CAPABILITY_JOIN`, `PROOF_JOIN`) or `MissingBlob`.

   The case therefore follows the corpus's own forged-output shape (`selected-same-count-message`). It changes the last byte of one finding's `messageCode`, which the finding carries twice (its member and its parameter blob). The same byte changes in both: the helper asserts exactly one changed byte in the blob.
   - The blob is retained under its new raw digest.
   - The finding and every object naming it (proof, evidence, seal, Run) are re-keyed to a fixpoint, with ascending id sets kept ascending.
   - The originals stay retained as unread ambient inputs.

   Replay then reconstructs the true proof and refuses `Mismatch{EVALUATOR_COMPLETE_PROOF_REPLAY}`.
7. **B7's "`revocation-unrelated` drift recorded" is not assertable at the public boundary.** Drift lives only in security's `pub(crate)` `OperationGuard::drift()`. Neither `PublishedCommit`, `SessionEnd` nor either `scenario` module discloses it, and adding a reader is a product change. B7 asserts what is observable:
   - the helper's self-checks (the revocation version advanced);
   - `Committed`, not latched;
   - B0's census.

   X4a's private test `operation_live_tests.rs:480` pins the drift itself. B6's "gate 0 → 2" is shown the same way: `Refused` (not a latched `PublishedCommit`), and the REV that `finish` owes only for a latched gate. A record note is owed.
8. **Where the alteration happens.** B3, B5, B6 and B7 alter after the handoff and after `open`, then build the candidate, then call `prepare_commit` and `publish`. `open` is needed for B6 to read `core_closure()`, because `ProjectOperation` exposes no public getter. The refusal therefore comes at `publish`'s first checkpoint, with the attempt row admitted, which is the table's census. `charge` ignores the latch, so if the 5 s observer ticks first in B6, it latches on the same revocation with the same row.
9. **"Replaced".** B3 replaces each file with its own bytes, using `cp -p` (mode, owner, flags and ACL kept) and then a rename, so only its identity changes. The refusal is identity-based, not content-based. B5 changes the content too ("naming another generation"). All three resolve to the same custody row.
10. **Scratch layout (churn, no sleeps).** Each process makes `<TMPDIR>/opensip-test/x8c-<pid>-<draw>/<case>/{homes,helper}` once, every case's directories before any case walks. The scenario home is created under `homes`.
    - Security's fixture lock (`test_scratch`, held per thread from `ScenarioHome::create`) serializes the cases in-process.
    - The helper's `TMPDIR` and input file are `helper`, the case's helper scratch parent. It sits beside the home, never above it, so nothing the helper creates changes an ancestor of H.
    - Neither `churned` nor any retry is used: it is crate-private and sleeps.
11. **No inventory.** No file is added and no file's role changes. `admission_tests.rs`'s inventory description ("…replay-invalid Runs, revoked authority and stale fences cannot produce acknowledged authoritative commits") already describes B0 to B8. So there is no v132; the review uses `ACCEPT` on the diff.

**Record notes owed** (for X8's next record-only revision; none changes an outcome):
- (a) B2's wording and owner (EXIT-PLAN);
- (b) the corpus path, call 3;
- (c) the REV on B1, B2 and B4, call 4;
- (d) B7's drift and B6's gate as shown at the public boundary, call 7;
- (e) B0's candidate route, call 1.

## Checks at a2c5e8b with this diff (private TMPDIR)

- **Full workspace, twice:** `cargo test --locked --offline --workspace --all-targets` gave 1726 passed, 0 failed, 3 ignored both times. X3d-3's baseline is 1714; the 12 new tests make up the difference.
- **Crash-matrix lane:** `cargo test --locked --offline -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets` gave 1611 passed, 0 failed, 3 ignored, against X3d-3's 1599 plus 12.
- **Scenario lane:** `cargo test --locked --offline -p opensip-security -p opensip-storage --features scenario-fixtures --all-targets` gave 1139 passed, 0 failed, 2 ignored. That is unchanged, since host is not in this lane.
- **Clippy `-D warnings`:** clean on the workspace `--all-targets`, on the four crates with `crash-matrix`, and on security and storage with `scenario-fixtures`.
- **Format:** `cargo fmt --all --check` is clean.
- **Package edges:** `check_package_edges --lane host` against the selected `repository-file-inventory.v130.json` passes, with 22 declared and 20 resolved internal edges.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does each case implement its X8 r4 B row (with the EXIT-PLAN corrections) and assert the exact row and the durable census after `finish`? Is B0 a real, non-vacuous control on the same harness?
- Is item 5a met exactly?
  - a non-ignored env-gated entry;
  - a cleared environment;
  - the fenced publisher in a process that holds no lease;
  - the published record, one test run, and the advanced version checked before and after;
  - no sleep.
- Does any case alter state inside `publish`, use timing, or publish trust from the lease-holding process?
- Is the `#[path]` include with the registry shim lawful under X8 item 4 and X9 item 6? Is it the narrowest route for B0's Run?
- Are judgment calls 1 to 11 acceptable? Are the record notes the right ones?
- Is anything else wrong?

review.json must contain top-level:
- "verdict": `ACCEPT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectSha256": the sha256 of `subject.diff`, `8b394a1b8a9c7f2079a9c49b43394c0cf48c60676da356322f3f4e3e9d6b712f`.

Write REVIEW.md and review.json. Do not commit.
