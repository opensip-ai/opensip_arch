# Evaluator-closure inventory130

Adds exactly one file to inventory129 (unit X8b, selected at product 4faf729 and still at 9d3b84b, where EC1 is bound; D1's thirty-nine overrides and D2's four supersessions are already folded into its fifty-five inheritance rows):
- crates/storage/src/crash_matrix_support/run_candidate.rs

It keeps all 963 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 964 planned files.

**No new edge.** The candidate calls security (`CommitSession`'s public getters and the shared test-support accessor), the evaluator (`derive_evaluation`) and identity, along the storage-to-security, storage-to-evaluator and storage-to-identity edges the parent declares. The builder asserts each one.

The row is unit X3d-3, law X3d r8 item 13, with X9 r7's record that the candidate moved here from X9-2.

- **run_candidate.rs (service).** The synthetic run candidate, a child module of storage's `crash_matrix_support` (`doc(hidden)`, under the test-only `crash-matrix` feature). Storage's unit tests (`commit_tests.rs`) include the same source file with `#[path]`, because storage's support module is not compiled in its plain test build. Inputs only. Starting from the pinned corpus Run, it:
  - rewrites the snapshot's `projectId` and the evaluator closure to the session's (`project_id`, `core_evaluator_closure`);
  - retains that closure's descriptor, its manifest blob and its tree blobs;
  - recomputes the dependent identities and digests;
  - re-derives the outputs with `derive_evaluation`;
  - builds the evidence, seal and Run as `replay_run` checks them.

  It never returns a `ReplayedRun`.

**Changes to existing rows.** Every row stays by value. Where a lock inheritance row overrides a row, the text judged here is the effective description. Out-of-date descriptions are left for the next description-only successor, as earlier units left theirs.
- `crates/security/src/trust/core_inventory.rs`: `Projection` gains the core evaluator closure (EC1), computed in `bind`, and the EC1 vector tests. Its description ("validate … before anchor authentication") stays true.
- `crates/security/src/trust/initial_core.rs`: `InitialCore::evaluator_closure`. Its description stays true.
- `crates/security/src/trust/initial_core_tests.rs`: `InitialCore::evaluator_closure_preimages`, the read behind the shared accessor, inside the existing joint-predicate `tests` module. Its description ("compiled only for tests") was already out of date by omission, since X9-1 put this module on the joint predicate; it still says test support, which it remains.
- `crates/security/src/custody/read_premise.rs` and `custody/operation_handoff.rs`: the read-only `core_evaluator_closure` value beside `selected_core`, and one joint-predicate hop each for the accessor. Their descriptions stay true.
- `crates/security/src/custody/commit_session.rs`: `core_evaluator_closure()` and the `doc(hidden)` accessor `core_evaluator_closure_preimages()`. Its description ("binds … the receipt's selected core closure") is out of date by omission of the evaluator closure.
- `crates/security/src/crash_matrix_sites.rs`: the pin extended by name with the accessor's three sites (shared gate 5). Its description lists the four gates, so it is out of date by omission of the fifth.
- `crates/storage/src/commit.rs`: `Bound.evaluator_closure` replaces `Bound.core_closure` (its only use was step 1), and `plan` compares against it. Its description stays true.
- `crates/storage/src/crash_matrix_support.rs`: it declares the candidate module. Its description ("forwards security's surface unchanged … storage adds no second site") is out of date by omission of the candidate. No cfg site is added.
- `crates/storage/src/commit_tests.rs`: `bound()` comes from a real session, the positive tests replay the candidate, the mismatch tests are rewritten, and there is the first real `prepare_commit`/`publish` composition. Its description ("without a session") is now wrong in that clause.
- `crates/storage/src/recover_tests.rs` and `sweep_tests.rs`: `bound()` lost its Run argument. Their descriptions stay true.
- `crates/host/src/crash_matrix_support.rs`: unchanged. Its description says the candidate "joins it with X9-5", which X9 r5 and r7 superseded; it is now forwarded through storage's surface.

**Order.** Its parent is the inventory the real product lock selects: inventory129 (unit X8b) at product 9d3b84b. The number 130 was assigned by the lead; succession is by the lock's parent pin, not by number. `evidence/build_v130.py` reads the parent from the lock (the product checkout's `design-lock.json`, or a lock path as its one argument), checks each inheritance row against the lock before carrying it, writes only its two paths, refuses tracked paths and refuses while a lock selects inventory130. Reruns reproduce the same bytes.

**Projection.** The fifty-five effective description overrides the lock binds to inventory129 stay bound by stable file path: the sixteen carried from inventory81 onward and D1's thirty-nine, with D2's four supersessions already folded. Only the candidate selectors after the inserted row move, by one. No contract successor bound at 9d3b84b names inventory129 as a supersession parent, so nothing new is folded (`supersessionsFolded: 0`).

`verify_projection.py` is inventory129's helper with its comment updated for this parent. It runs against the real lock at 9d3b84b. `evidence/verify_scratch.py` appends inventory130 in memory over the worktree's lock, replaces the inheritance rows with the record's fifty-five, and supplies a synthetic review and assent.
