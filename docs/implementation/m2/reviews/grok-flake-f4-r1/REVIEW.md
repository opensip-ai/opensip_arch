# F4 r1 — shared-ancestor churn in the read fixture

ACCEPT. The diff is test support only. `shared_churn` retries one refusal shape, a descriptor-ACL `Changed` on a component strictly above this process's private scratch parent, and every mutation in `every_capture_phase_refuses_actual_mutations` acts at H or below that cut. The fixture-level retry stays. The `a_lost_race` residual stays out of scope.

Subject: worktree `/Users/sb/code/opensip-ai/opensip-f4`, detached at `0206ce8673ade3689331fe22801458a03646f502`. `git diff` is two files, 101 insertions, 29 deletions. Saved as `subject.diff`, 9866 bytes, sha256 `87e9165a6d56e9c533e4841b4f9c9c13f5205bd0a953e97007dbbbae10e6a68b`. Both product pins in `hashes.txt` match the worktree bytes. `~/Library/Application Support/OpenSIP` is absent. No inventory successor.

## Test code only

Yes. `installation_read_fixture` is included from `custody.rs` only under `#[cfg(all(test, target_os = "macos"))]`. `installation_observation_tests.rs` is included from `installation_observation.rs` only inside `#[cfg(test)] mod tests`. The diff names those two files and no other. `create`, `shared_churn`, `session_churn`, and `settle` live in the fixture. Production `observe_parent`, `chain_refusal`, and `recheck_chain` are unchanged.

## The bound

On this machine the canonical temp directory is `/private/var/folders/<id>/<id>/T`. Its components are 0 `/`, 1 `private`, 2 `var`, 3 `folders`, 4 and 5 the two ids, 6 `T`. `test_scratch::temp_dir()` is that path plus `opensip-test` (7) plus `<pid>-<nanos>` (8). `shared_churn` canonicalizes that path and sets `private` to `components().count() - 1`, which is 8, the private parent's own index. `component < private` is `/` through `opensip-test`. The fixture's nonce directory is 9 and H (`…/<nonce>/home`) is 10. The same count tracks any temp-directory depth; the literal 6 and 10 are this machine's layout, and the code does not hardcode them.

`visit_directories` uses the same numbering: index 0 is the filesystem root, then one index per retained edge (`path_binding.rs`). `judge_ancestor` stores that index on `ParentRefusal::Capture`. The fixture canonicalizes the scratch root before it builds H, and `shared_churn` canonicalizes `temp_dir()`, so a `/var` → `/private/var` symlink does not shift the cut. Without that canonicalize, `opensip-test` in the walk (component 7) would sit on the private index of the unresolved path and would be excluded.

`chain_refusal` (`installation_admission.rs`) sends `ParentRefusal::Capture` to `GateRefusal::Io(IoFailure::Chain(_))`. `Ancestor`, `AncestorAclOmitted`, and `NameChanged` go to `Custody(Chain(_))`. `session_churn` matches only `SessionRefusal::Gate(Io(Chain(_)))`, then `settle`. `ReadFixture::new` matches only `Failure::Operation(CreationRefusal::Parent(ParentPreparationRefusal::Parent(_)))`, which is the nesting `prepare_installation_parent_at` and `compose` produce for an `observe_parent` error, and then the same `settle`. Any other outcome still panics, including a non-`Published` creation and a session `Err` that is not this row (`fence` still `unwrap`s it).

`settle` allows eight attempts. Attempts 1 through 7 sleep `25 ms × attempt` and retry. Attempt 8 asserts. That is the same bound and backoff as F3's `settled` (`1..=8`, report the eighth failure). Creation retries in a fresh scratch root because `create` builds a new nonce directory and drops the failed `Scratch`. `fence` reopens a session on the same fixture: the installation is already published, and the churn is above it. Each `session_at` builds a new attempt and a new observation session, so a latched failed open does not poison the next one.

## It does not mask a mutation

`every_capture_phase_refuses_actual_mutations` mutates `selection.pair` under I, `lifecycle.fence` under I, or H's mode (`"root"` is `set_permissions` on `inner.home`). Those directories are component 10 and below (I is H plus `Library` / `Application Support` / `OpenSIP` / `preview-v1`). Creating, removing, or renaming an entry updates that entry's parent directory, not the ancestors above it. `chmod` updates the inode that was chmod'd. None of that is a `Capture { Changed }` at a component below 8.

The private parent itself (component 8) is also outside the retry. This process creates and drops nonce directories there, and the `TREE` guard is held by the thread that first called `temp_dir()` until that thread exits, so another thread in the same process cannot be creating under that parent during the walk. Another process writes its own `<pid>-<nanos>` under `opensip-test`, which changes `opensip-test` (component 7) and can change `T` (component 6). It does not write inside this process's `0700` parent. A `Changed` on the private parent fails the test.

The full recheck inside `capture_with` walks `/` through H before it rechecks the retained file (`recheck_chain`). A `Changed` at component 6 therefore returns before `Custody(Changed)`. For `AfterOpen` / `in-place` the capture itself can succeed, because the rewrite finishes before the first body sample, and the test requires `SessionRefusal::Gate(Custody(Changed))` from that recheck. The case loop continues only when `session_churn` holds, then runs the original assertions on the first other result and breaks. A churn refusal is discarded with the fixture. An `Ok` still fails `is_err`. A non-churn `Err` still has to match the `in-place` pattern. For `BeforeRead` and `AfterRead`, the capture's own before/after sample returns `Custody(Changed)` and `capture_with` keeps that refusal when the later recheck also fails, so ancestor churn does not replace it.

`shared_churn` additionally requires `DescriptorAclCaptureError::Changed`. `Io`, `Unsupported`, and `Malformed` on the same component are not retried.

## Root cause

The step 0 walk and the full recheck both call `judge_ancestor` → `capture_descriptor_acl_accounted` on every retained directory from `/`. That capture returns `Changed` when the descriptor's metadata differs across the sample. F3 placed fixtures under `<temp>/opensip-test/<pid>-<nanos>`, and `T` and `opensip-test` remain on the walk. Any create or remove in `T` changes `T`'s mtime, which is component 6 on this machine, the component in the reported `fence` and `ReadFixture::new` failures. F3's `settled` retries only a panic whose text contains `ChangedDuringRead`. `DescriptorAclCaptureError::Changed` is a different type, and this test is not wrapped in `settled`. Building 27 fixtures, each walking from `/` more than once, is the exposure the lead describes.

## Keep the retry on the fixture

`ReadFixture::new` and `fence` are the open path for every fixture user, including `consumption_rechecks_the_original_file_and_the_held_fence`, which the lead saw fail at `new` with component 6 `Changed`. The classifier is the same structural row those callers panic on today. Confining the retry to this one test would leave that open path on the flake. The case loop in this test is still required: `capture_with`'s recheck runs after `fence` has returned, so `fence`'s retry never sees it.

## Residual, not a finding

`installation_routing::tests::a_lost_race_enters_the_gate_and_admits_the_winner` uses its own scratch and `route_at`. `chain_refusal` in `installation_routing.rs` maps `ParentRefusal::Capture` to `ancestor-acl` and drops the component, so `shared_churn` cannot classify that row. Same churn class, different fixture. Out of scope for F4, as the request says. Candidate F5.

`rustfmt 1.9.0 --edition 2024 --check` fails on both files at `0206ce8` and on this diff. The base already has over-width lines in these files. F4 adds more of the same (the creation match, the `session_churn` arm, the `settle` assert, and the `installation_root` import placed after `installation_session`). That is the drift the accepted tree already carries here. It is not a required finding. Clippy and the lead's suite runs were not replayed; the judgment is the diff, the refusal types, and the component count.
