# Description batch D3

Verdict: **ACCEPT-DESIGN-UNIT**.

D3 is one description-only contract successor of inventory v134. It changes 62 descriptions: 45 `passageOverrides` on plain rows and 17 `passageSupersessions` on inherited rows. No schema, registry, generated code, product file, or inventory successor is in the subject. Product main is `3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f`. The OpenSIP support directory stayed absent. No cargo, test, or crash-matrix command was run. The opensip-x9-6 worktree was left untouched.

Subject manifest `docs/implementation/m2/description-batch-d3-subject.json` is 1037 bytes, sha256 `b31ca109e8a42cd090780d0171e4cc77d91a8c338b3a9aa77bcbe6fccc6403e6`. `description-batch-d3/successor.json` is 240605 bytes, sha256 `b7b4ee2fdc454460c132fee7853b32558fd88cbb389fd6061954144349d99c50`. Every hashes.txt pin matches.

## What this review ran

Private 0700 `TMPDIR`. `PATH` as the lead named. Each evidence command at `nice -n 19`.

| Check | Result |
|---|---|
| `verify_scratch.py` on main, binding appended in memory | Passed. Mode appended. 94 inventory successors, 76 contract successors, v134 still selected, 55 inheritance rows, supersessions 4 to 21, D3 45 overrides and 17 supersessions. 40 generation sources, 48 admission sources, 15 aliases. |
| `verify_scratch.py` on `/Users/sb/code/opensip-ai/opensip-d3` | Passed. Mode bound. The same counts. The worktree's last contract entry is D3, with the real record and subject pins and the two `SCRATCH-D3` placeholders. |
| Plain `verify_design.py` on main | Passed. 75 contract successors, 94 inventory successors, 55 inheritance rows, 4 supersessions. v134 sha256 `626cd71996d79de5c0efd914438dd65b3123e701e774ccdad1f8f9681466c58a`. |
| `build_d3.py`, two runs, writes captured in memory | Both runs produced the pinned successor and subject bytes. The architecture tree was not written. |

The lead worktree differs from main only by the staged D3 binding in `design-lock.json`. The record and subject pins are the subject bytes. The review and assent pins are the `SCRATCH-D3` placeholders. Plain verify_design on that worktree refuses those placeholders, which is the state before this review is copied in.

`descriptions.json` and `successor.json` carry the same 62 before/after pairs. Every parent is v134. The 15 inherited rows other than `read_premise.rs` and `installation_session.rs` supersede D1's override on v119. Those two supersede D2's supersession on v122.

## Descriptions

Every sentence that remains in the new text is the old sentence word for word. Sentences that were replaced were false of the file at `3d2d5b5`, and the replacement names what the file now does.

Checked against the committed tree:

- `doctor_tests.rs` refuses a `[features]` table on `apps/cli` and `reporting`, and on host, security, and storage admits only `crash-matrix` and `scenario-fixtures` (`doctor_tests.rs:167-193`).
- Host `crash_matrix_support.rs` forwards storage's surface and adds `finalize_commit` and `store_gc` (`crash_matrix_support.rs:296` and `:357`). The authority sentence now excepts the forwarded driver entries.
- `fact_admission.rs` is the replay join. `finalization.rs:400` is the production `replay_candidate` call, before custody.
- `finalization.rs` does not route exhaustion through lifecycle and does not use `outcomes.rs`. `finalize` is the coordinator. A `CarrierCapacityExhausted` is finished through X3d's end step.
- `maintenance.rs` is `sweep_store`, `run`, and `namespace_row` (`maintenance.rs:78`, `:89`, `:117`). The planned sentence stays. The crash-matrix caller is `store_gc`.
- `clock.rs:68-85` takes `observe_clock`'s wall reading from `scripted_wall()` under the crash-matrix feature, and from `os::wall()` otherwise. `driver.rs:204-207` puts `OPENSIP_X9_CLOCK` in the cleared child environment when the spec carries a clock.
- `carrier_append.rs` still keeps cfg(test) hooks, and it also emits `crash_barrier!` points (`begin`, `level-four`, `release-level-four`, `built`) outside that predicate. `carrier_rollover.rs` and `project_commit.rs` are the same shape: the file's own hooks stay under cfg(test), and the X9 points have a body under the crash-matrix feature.
- `ProjectStoreLocation::selected` (`project_ledger.rs:141`) is the production location. The struct comment at line 128 still says only tests construct one; that comment is outside this successor.
- `post_state.rs` opens files for reading (`File::open` at line 107). The module note at lines 9-12 says the capture never opens, locks, checkpoints, or creates anything under the root. Unreadable files, undumpable databases, and tables without rowid are the X9-3 behavior the new text names. `run_record.rs` records `timingGuard`.
- `read_premise.rs` keeps all nine D2 sentences. The inserted sentence is `core_evaluator_closure` (`read_premise.rs:123`) and, under `any(test, crash-matrix, scenario-fixtures)`, `core_evaluator_closure_preimages` (`:129-130`). `opensip doctor` remains the one wired CLI path.
- `initial_core_tests.rs` and `initial_platform_tests.rs` are included under `#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]`. `accepted_store_fixture` is the same predicate (`root_payload.rs:917-919`). The module comment at `accepted_store_fixture.rs:11-12` still says cfg(test) only; that comment is left for the code follow-up.
- `floor_publication.rs` has `confirmations` (`:237`) and `publish_store_fenced` (`:546`).
- `first_registration.rs` has the Lease step (`:131`), Exact and Started footprints (`:1541`, `:1547`), and `recheck_registered_owners` (`:2413`).
- `CarrierLocation::recovered` is the recovery constructor (`recovery_location.rs:19`), used by recovery admission.
- Storage `tests/commit_tests.rs` is `#![cfg(all(feature = "crash-matrix", target_os = "macos"))]` with `required-features = ["crash-matrix"]`. It defines `x9_6_matrix` and `release_order_misses`. The removed harness sentence names nothing in the file.
- Host required runs: 98 rows, 4 with `"unit": "X9-6"`. Storage required runs: 381 rows, 46 with `"unit": "X9-6"`. Both epochs are 1791072000.
- `check_crash_matrix.py` requires L1 through L11, takes host and storage once each, and `check-unit` offers X9-2 through X9-5. `coverage` runs nothing.
- `commit_session.rs` and its tests cite X7 r6 for the SessionEnd accessors. `finalization.rs` cites X7 r5 for the coordinator the X7a and X7b units implemented.

`operation_handoff.rs` is 5073 characters and `commit_session.rs` is 4838. Ten further texts are over 3000. The length is the kept true sentences plus the clauses for what the file now does.

## Rows left as they are

122 rows were judged: 62 changed, 60 kept. The five lead decisions hold.

- `recovery_route.rs` keeps "no CLI command calls it before X11". Law X11 r1 item 4, in `cli-enablement-x11/PROPOSAL.md`, says that wording stays true. The same sentence covers `maintenance.rs`'s CLI, finalization, and the commit facade.
- `commit.rs`, `ledger_store.rs`, and `recovery.rs` keep their planned summaries. Those sentences still name the facades: bind and publish through `PublishedCommit`; private ledger transactions for the guarded commit and authorized maintenance paths; read-only reconciliation that does not repeat repository mutations.
- `installation_parent.rs` keeps its text. `recheck_names_in` is the preparation's own recheck.

The other kept rows are generic manifest and lib rows, F5 and F6 churn retries, files whose texts neither list X9 points nor claim "only cfg(test)", and the small census and verify_design edits. `scenario` in security and storage is still `cfg(all(feature = "scenario-fixtures", target_os = "macos"))`, so those descriptions stay true.

173 inventory paths differ between `8240856` and `3d2d5b5`. 122 of them are the judged set. The other 51 last changed in the commit that introduced them, and their descriptions describe that unit: the compile-fail cases, the X6 recovery and sweep modules, the X8b scenario seam, the X9-1 census child, and the license. They are contemporaneous with their text.

## Judgment calls

1. **One record, both forms.** Accepted. A row with an inheritance entry is superseded; a plain row is overridden. `build_d3.py` refuses an override of an inherited or already superseded row, and verify_design accepts the combined record. Inheritance stays 55. Supersessions grow by the 17 new links.
2. **Pre-D1 omissions.** Accepted. The seven named files were already missing later units' content, and `floor_publication.rs` also gains X4B-b's confirmations beside the X9-1 publisher. Leaving them would repeat this batch.
3. **Planned rows.** Accepted. `maintenance.rs` named none of `sweep_store`, `run`, or `namespace_row`, so the planned sentence alone was incomplete. `fact_admission.rs`, `finalization.rs`, and storage `tests/commit_tests.rs` keep the planned sentence where it is still the file's purpose. `finalization.rs` drops the lifecycle-rollover and `outcomes.rs` clauses. The commit-test file drops the harness sentence. `commit.rs`, `ledger_store.rs`, and `recovery.rs` stay, because the planned text already covers them.
4. **cfg(test) and X9 points.** Accepted. The three named files now keep their own hooks under cfg(test) and name the X9 points under the crash-matrix feature. Files that neither list points nor claim cfg(test) only stay as written. `commit_session.rs` and `operation_handoff.rs` gain the scopes they already list in code.
5. **Joint predicate.** Accepted. The four named files are compiled under `any(test, crash-matrix, scenario-fixtures)`.
6. **`clock.rs`.** Accepted as material. Under the crash-matrix feature the file's one wall observation comes from the scripted clock, and the sites pin names that feature site.
7. **`recovery_route.rs` kept.** Accepted, on X11 r1 item 4.
8. **X1b closed.** Accepted. D2's nine sentences are still true, including the Write receipt and `opensip doctor`. D3 adds `core_evaluator_closure` and the joint-predicate preimage read.
9. **Narrowed sentences.** Accepted. The capture sentence matches the module's own claim: nothing under the root is opened for writing, locked, checkpointed, or created, and the walk opens files to read them. Both support surfaces now except the forwarded driver entries from the authority sentence.
10. **Length.** Accepted. Rewording true sentences to shorten them would change text this batch is required to keep.
11. **Product doc comments.** Accepted as outside D3. The README's list matches comments still in the tree, including `accepted_store_fixture.rs:11-12`, `project_ledger.rs:128`, `driver.rs` on the child environment, and the `commit_session.rs` cites of X7 r5 item 6. The inventory text for `commit_session.rs` already says X7 r6.
12. **After selection.** Accepted. The next inventory successor carries every row by value, projects these 45 overrides so inheritance grows from 55 to 100, folds these 17 supersessions into the existing entries, and reads both forms. A parent-only rebuild after another inventory is selected changes the pins and needs a new review. `build_d3.py` finds rows by path.

## Binding

At acceptance the lead copies this review, completes `description-batch-d3-unit.json`, replaces the two placeholder pins, runs plain verify_design, and commits. That unit file is the lead's draft and is outside the subject.
