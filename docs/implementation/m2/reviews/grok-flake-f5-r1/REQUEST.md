Grok review: F5, three flakes from the F4 root cause whose refusal reaches the test without a component. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-flake-f5-r1.

**Subject:** the worktree `/Users/sb/code/opensip-ai/opensip-f5`, detached at product main 0fc8ea2. Five existing files change. Four are compiled only under `cfg(test)`: `installation_read_fixture.rs` (`#[cfg(all(test, target_os = "macos"))]`), `installation_routing_tests.rs`, `namespace_lease_tests.rs`, and `operation_live_tests.rs` (each included only from a `#[cfg(test)] mod tests`), all under `crates/security/src/custody/`. One is a production file, `crates/security/src/custody/installation_root.rs`. Its change is a `#[cfg(test)]` thread-local and a `#[cfg(test)]` statement, so a non-test build compiles the same code as before (see "The production file" below). The file set and every role are unchanged, and the inventory records paths and roles, not bytes. So there is no inventory successor, as with F3 and F4. Save `git -C <worktree> diff` as subject.diff and report its sha256. Pins are in hashes.txt. Precedents: F3 at 8452ab9 (`test_scratch::settled`, review grok-scratch-isolation-f3-r1) and F4 at 8bd0283 (`shared_churn`, review grok-flake-f4-r1).

Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`. Use your own `CARGO_TARGET_DIR`. Never touch the real `~/Library/Application Support/OpenSIP`. **Churn caution:** a `$TMPDIR` churn loop affects every test run on this machine, including other units' runs. If you reproduce, start and stop the churn inside one command (`python3 churn.py & C=$!; trap "kill $C" EXIT; …`), keep it short, and make sure nothing outlives it.

## Root cause (one cause, three surfaces)

It is the F4 cause. Every ancestor walk (`judge_ancestor` in `installation_root.rs`) captures each directory from `/` through H. The capture compares `fstat` before and after `fgetattrlist`, and refuses `DescriptorAclCaptureError::Changed` when they differ. That includes the shared temp directory `T` (component 6 on this machine) and `opensip-test` (7), both above this process's private scratch parent (8). Any process that creates or removes an entry in `T` changes T's mtime. These three tests run many walks (fixture creation, writer admission, project admission, registration, namespace admission, the gate's and the guard's rechecks), and any one of them can refuse. F4 classifies the refusal structurally where it arrives as `ParentRefusal::Capture { component, .. }` (`ReadFixture::new` and `fence`). Here it also arrives at test code in shapes F4's classifier can't see:

- **`installation_routing::tests::a_lost_race_enters_the_gate_and_admits_the_winner`:** `route` (production) maps the creator's and the gate's refusal through `chain_refusal` to `T::Custody { subject: "ancestor-acl" }`, which drops the component (`installation_routing_tests.rs:161`). The winner's own `create_at` in the hook can also refuse (line 156).
- **`namespace_lease::tests::the_target_holds_no_project_lock_for_the_floor_step`:** `writer()`'s `admit_with` maps the gate refusal to `ancestor-acl` (line 64). `admitted`, `register`, `admit_namespace` and `lease_writer` return it nested, for example `Gate(Io(Chain(Capture { component: 6, error: Changed })))` and `Registration(Operation(Admission(Chain(Chain(Capture { … })))))`, at lines 77, 80, 97 and 519 (line numbers at 0fc8ea2).
- **X4a `operation_handoff::tests::live::a_revoking_update_is_seen_by_the_checkpoints_own_final_observation`:** in setup it appears as `ancestor-acl` (handoff `writer_with`, line 110), `Endpoint(Custody { subject: "ancestor-acl" })` (`join_store_endpoint`'s gate recheck, `operation_live_tests.rs:49`) and the nested shapes (lines 126, 129, 146). In the assertion under test, the checkpoint's own final observation can refuse for churn before it sees the revocation. The test then fails with `left: Stale(Project(Project(Admission(RootCustody("acl-unreadable")))))`, `right: Revoked { subject: "trust-revoked" }`. `project_chain::capture_row` maps `Changed` to `acl-unreadable`, again without the component.

Every failure observed, in every shape, was a `Changed` capture at component 6.

## Fix

**Witness at the source (production file, test builds only).** `installation_root.rs` gains `#[cfg(test)] thread_local! CHANGED_CAPTURES: RefCell<Vec<usize>>`. When `judge_ancestor`'s capture fails with `Changed`, a `#[cfg(test)]` statement in its `map_err` closure pushes the walk component. The returned `ParentRefusal::Capture { component, error }` is unchanged. `judge_ancestor` is the only place that constructs `ParentRefusal::Capture` (the other mention, `installation_parent.rs:491`, is a pattern). Nothing in production reads the thread-local. A test-only change could not do this: the component is dropped inside production mappers (`route`, `admit_with`, `join_store_endpoint`, `capture_row`, the guard's stop causes) before any test closure sees the refusal. The alternative was to change those mappers' error types to carry the component, which would be a production change. I chose the smaller one.

**`installation_read_fixture::churned(test)`** is F3's `settled` shape: a whole-test retry on fresh fixtures, at most 8 attempts, with backoff of 25 ms × attempt. The last attempt's panic is re-raised. The witness is cleared before each attempt. After a panic, the attempt is retried only if `CHANGED_CAPTURES` is non-empty and **every** recorded component is `< private_component()`. That bound is F4's: the canonical `test_scratch::temp_dir()` component count less one, which covers `/` through `opensip-test`. It does not read the panic text. A `Changed` at the private parent or below (H, I, the project, anything a test mutates) blocks the retry. `private_component()` is F4's existing computation, factored out of `shared_churn` (whose behavior is unchanged).

**Applied** to exactly the three tests: each body is wrapped in `churned(|| { … })`, re-indented with no other change. Every assertion is unchanged.

## Why this cannot hide a defect

- A retry needs a recorded churn capture above the private parent during that attempt. No test fixture, mutation or path under test touches `/` through `opensip-test` (F4's argument, which holds here too: every fixture is below the private parent).
- A deterministic failure recurs on each attempt. It is reported either from the first attempt that has no churn record or from attempt 8. The retry can lose only a failure that happens solely in attempts that also had shared-ancestor churn.
- The witness is thread-local. A refusal on another thread is not recorded, so it is never retried (fail-safe).
- F4's own retries (`ReadFixture::new`/`fence`) also record. So an attempt in which the fixture absorbed churn and the test later failed for another reason is retried, at most to attempt 8, where that failure is reported.

## Results

Reproduction: each of the three tests alone, under a Python loop that creates and removes one file in `$TMPDIR`. Every experiment started and stopped its churn inside one script (`trap` kill). Times are 2026-10-01 local.

| Experiment | Churn | Base 0fc8ea2 failures | Fix failures |
|---|---|---|---|
| E5/E6, 13:53:23–13:54:08 (≈45 s) | flat out, about 9,300/s | 11/15 (routing 1/5, lease 5/5, X4a 5/5) | 2/15 (X4a only, 8 attempts exhausted) |
| E3/E4, 13:52:54–13:53:18 (≈25 s) | Poisson, about 270/s | 1/15 (lease, `ancestor-acl` at line 64) | 0/15 |
| E1/E2, 13:52:27–13:52:47 (≈20 s) | Poisson, about 20/s | 0/15 | 0/15 |

Base failures name every surface listed above. Under flat-out churn, X4a's long setup (hundreds of walks) fails most attempts (E7, 13:54:16–13:54:42: 4 of 6 runs used all 8 attempts). That is the stated limit, and it is the same limit F3 and F4 have. At realistic rates the fix holds.

- Four concurrent full `opensip-security` lib suites, 2 rounds (8 suite runs), on the fix, 13:55–14:09, with no churn loop: 0 failures (879 passed, 2 ignored each).
- Full workspace, twice: 1543 passed, 0 failed, 3 ignored each.
- Clippy (`--workspace --all-targets -D warnings`) is clean, and `cargo fmt --all --check` is clean.

Disclosure: earlier exploratory loops in this unit left two churn processes running for about 17 and 22 minutes, at roughly 9,000/s and 450/s, until about 13:51. That inflated failures in other units' runs on this machine and in my own early measurements. All numbers above were taken after those processes were killed.

## Known residual, out of scope

The other tests in `namespace_lease_tests.rs` (11), `operation_handoff_tests.rs` (17), `operation_live_tests.rs` (19) and `installation_routing_tests.rs` (10) share these helpers and are exposed in the same way. `churned` applies to any of them unchanged. They are not wrapped here because the request is the three reported flakes.

## Decide

- Is the production change acceptable: test-builds-only, minimal, with production behavior unchanged? Or should the component be carried another way?
- Is the classifier narrow enough? Can a test's own mutation or a real defect produce a recorded `Changed` capture below `private_component()` and so be retried? Is "every recorded component above the private parent" the right rule, against "any"?
- Is the root cause right for all three tests?
- Should the residual tests be wrapped now, or left for a follow-up?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256" (the sha256 of subject.diff: c22fbc6e5065eae9ed6b95e36c85f006498e8f9817c07015de1e7bfb6a55c203). Write REVIEW.md and review.json. Do not commit.
