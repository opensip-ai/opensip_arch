# F5 r1 — shared-ancestor churn, three surfaces

**Verdict: ACCEPT**

The production change is test-builds only and leaves the refusal value unchanged. `churned` retries a whole test only when every `Changed` capture recorded on that thread sits strictly above the private scratch parent. That is the right rule. The same `judge_ancestor` refusal explains all three reported failures. The other exposed tests, including X3d-1's `a_staging_io_error_rolls_back_then_appends_rev_and_cln`, stay for a follow-up. `requiredFindings` is empty.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-f5`, detached at `0fc8ea21a5d2881624d0cb296ff7cae5981c5a64`. Five existing files, 125 insertions, 67 deletions. No new paths and no role change, so there is no inventory successor.

`subject.diff` is 13374 bytes, sha256 `c22fbc6e5065eae9ed6b95e36c85f006498e8f9817c07015de1e7bfb6a55c203`. All five `hashes.txt` file pins match. `~/Library/Application Support/OpenSIP` is absent.

## Production change

`installation_root.rs` adds a `#[cfg(test)]` thread-local, `CHANGED_CAPTURES`. Inside `judge_ancestor`'s `map_err`, a `#[cfg(test)]` statement pushes the walk component when the capture error is `DescriptorAclCaptureError::Changed`. The value returned is still `ParentRefusal::Capture { component, error }`. A non-test build compiles that closure without the push and without the thread-local. `cargo check --locked --offline -p opensip-security --lib` passed. Nothing in production reads the thread-local. `churned` is the only reader, and `LocalKey<RefCell<Vec<usize>>>::take` (Rust 1.95) returns the inner `Vec`.

Carrying the component out through `route`, `admit_with`, `join_store_endpoint`, `capture_row`, and the guard's stop cause would change production error types. The thread-local is the smaller change, and it can see the component after those mappers have dropped it.

`installation_parent.rs:491` also constructs `ParentRefusal::Capture`. It is `admit`'s `map_err` around `capture_descriptor_acl_reserved` for a fixed ancestor (`R::Parent(ParentRefusal::Capture { component, error })`), with `component = admission.library + index`. That walk is Library and Application Support, not the from-`/` walk, and it does not record into `CHANGED_CAPTURES`. A `Changed` there is omitted from the witness, so `churned` does not retry it. The component-6 failures are the from-`/` walk, whose only constructor is `judge_ancestor` (`observe_parent`'s `visit_directories`, and `project_chain::judge` for every component short of the leaf).

`shared_churn` now calls `private_component()` and keeps the same comparison: `Capture { Changed }` with `component` strictly less than the canonical private parent's index.

## Classifier

`private_component()` is `canonicalize(test_scratch::temp_dir()).components().count() - 1`. Component 0 is `/`. On this machine that index is the per-process parent (`<temp>/opensip-test/<pid>-<nanos>`), so `component < private_component()` is `/` through `opensip-test`, including `T`. `ReadFixture::create` canonicalizes its scratch root before it builds `home`, and `RetainedDirectoryPath` numbers the handles it opens from that path, so the walk index and `private_component()` name the same directories.

`churned` clears the witness, runs the test under `catch_unwind`, and retries only when the recorded list is non-empty and every component is `< private_component()`. The bound is eight attempts, the backoff is 25 ms times the attempt number, and attempt 8 re-raises. An empty witness, or any recorded component at the private parent or deeper, re-raises immediately.

A fixture mutation lands at the private parent or below it: creating a child changes that parent's mtime, and the project, H, and I are deeper. Those components are recorded and block the retry. A real defect that itself captures `Changed` at or below the private parent is reported on that attempt. The "every component" rule is the one that does this. An "any component" rule would retry an attempt that also saw `T` change, and could spend the eight attempts on a deep `Changed` that is the test's own.

The witness is thread-local. A refusal on another thread is not recorded and is not retried. The three wrapped tests walk on the test thread (the routing hook runs inside `route`).

F4's `ReadFixture::new` and `fence` retries also pass through `judge_ancestor`, so they append to the same witness. An attempt whose fixture absorbed shared churn and then failed for another reason is retried, at most until attempt 8, where that failure is reported. A deterministic failure still surfaces. The retry can drop only a failure that occurs on attempts that also recorded shared-ancestor `Changed` and no deeper `Changed`. That is the same bound F3 and F4 already have.

No test fixture writes `/` through `opensip-test`. `private_dir` creates `opensip-test` and the per-process child once; later fixtures are children of that child.

## The three tests

Each body is wrapped in `churned(|| { … })` and re-indented. The assertions are the same.

- `installation_routing::tests::a_lost_race_enters_the_gate_and_admits_the_winner`. `route` maps the creator's and the gate's refusal through `chain_refusal`. `ParentRefusal::Capture` becomes `T::Custody { subject: "ancestor-acl" }` (`installation_routing.rs:366`), and `acl_capture` keeps that row for `Changed` (`:297`). The winner's `create_at` in the rename hook walks the same ancestors. Both are on the test thread, so a component-6 `Changed` is in the witness when the `unwrap` or the `Published` assertion panics.
- `namespace_lease::tests::the_target_holds_no_project_lock_for_the_floor_step`. `writer` unwraps `admit_with` (line 64 at `0fc8ea2`). `admitted`, `register`, `admit_namespace`, and `lease_writer` unwrap the nested forms (`Gate(Io(Chain(Capture { … })))`, `Registration(Operation(Admission(Chain(Chain(Capture { … })))))`). Those walks call `judge_ancestor`.
- `operation_handoff::tests::live::a_revoking_update_is_seen_by_the_checkpoints_own_final_observation`. Setup goes through `eligible_live` → `begin_live` → `begin`, and `join_store_endpoint`'s gate recheck is `OperationRefusal::Endpoint` (`operation_handoff.rs:916`) around `gate_refusal` → `chain_refusal`. The handoff `writer_with` unwrap is the `ancestor-acl` surface. In the assertion, `checkpoint` → `operation_guard` step 1 records `StopCause::Stale` when `guards` fails (`operation_guard.rs:536`). `project_chain::judge` calls `judge_ancestor` for every ancestor, and `capture_row` maps `Changed` to `RootCustody("acl-unreadable")` with the component dropped (`project_chain.rs:160`). A churn refusal before the revocation is seen fails `assert_eq` against `StopCause::Revoked { subject: "trust-revoked" }` with the witness holding component 6, and `churned` starts the test over on a fresh fixture.

`cargo test --locked --offline -p opensip-security --lib` for those three names: 3 passed, 0 failed, 878 filtered, 1.98s. `TMPDIR` was a 0700 sibling of the user temp. No churn loop was started.

## Residual wraps are a follow-up

`churned` is `pub(crate)` and applies to any of these tests unchanged. This unit wraps the three reported flakes.

The files that share the helpers, and the tests left unwrapped:

| File | Tests in the file | Wrapped here |
| --- | ---: | ---: |
| `installation_routing_tests.rs` | 10 | 1 |
| `namespace_lease_tests.rs` | 11 | 1 |
| `operation_live_tests.rs` | 19 | 1 |
| `operation_handoff_tests.rs` | 17 | 0 |

Those unwrapped tests reach the same from-`/` walk through `writer`, `eligible`, `register`, `route`, and `begin_live`. A follow-up should wrap the ones whose setup unwraps that walk.

`a_staging_io_error_rolls_back_then_appends_rev_and_cln` is one of them, and it is not in this worktree. It lives in `commit_session_tests.rs`, included from current product main as `operation_handoff::tests::session`. That file is absent at `0fc8ea2`. `started()` calls `eligible()` and then the handoff; `eligible()` is the X2c `register` path (`operation_handoff_tests.rs` on the parent module, brought in with `use super::*`). A `Changed` at component 6 during that setup panics at the same `unwrap`s as the lease and handoff flakes, before the staging assertion. One such failure under concurrency is this cause. Wrapping it belongs in the follow-up, on a tree that already has `churned` and the session module, together with the other session tests that enter through `started` / `eligible`.

## Replay

Non-test `cargo check --locked --offline -p opensip-security --lib` passed. The three wrapped tests passed, as above. The lead's flat-out and Poisson churn table was not replayed; a churn loop on this machine lands in every other test run. The cargo target and the private temp directory were removed.
