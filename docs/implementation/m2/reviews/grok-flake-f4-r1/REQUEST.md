Grok review: F4, the flake in `installation_observation::tests::every_capture_phase_refuses_actual_mutations`. Test-support code only. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-flake-f4-r1.

**Subject:** the worktree `/Users/sb/code/opensip-ai/opensip-f4`, detached at product main 0206ce8. Two existing files change, both compiled only under `cfg(test)`: `crates/security/src/custody/installation_read_fixture.rs` (the `#[cfg(all(test, target_os = "macos"))]` read fixture) and `crates/security/src/installation_observation_tests.rs`. No inventory successor, as with F3. Save `git -C <worktree> diff` as subject.diff and report its sha256. Pins are in hashes.txt. Precedent: F3 at 8452ab9 (review grok-scratch-isolation-f3-r1).

Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`. Use your own `CARGO_TARGET_DIR`. Never touch the real `~/Library/Application Support/OpenSIP`.

## Root cause

The read session's step 0 walk (`observe_parent`, law 460) starts at `/` and takes a descriptor ACL capture of every component through H. The capture compares the descriptor's metadata before and after, and refuses `DescriptorAclCaptureError::Changed` when it differs. F3 moved every fixture below `<temp>/opensip-test/<pid>-<nanos>`, but the walk still captures `/` through the shared system temp directory (`/private/var/folders/.../T`, component 6) and `opensip-test` (component 7). Any process that creates or removes an entry in T changes T's mtime, so a capture of T can refuse. The refusal surfaces as:

- `ReadFixture::fence()` unwrap: `Gate(Io(Chain(Capture { component: 6, error: Changed })))` (the reported failure, fixture line 104);
- `ReadFixture::new()` creation: `Err(Operation(Parent(Parent(Capture { component: 6, error: Changed }))))` (fixture line 81);
- the full recheck inside `capture_with`, which re-judges every retained directory from `/`. There the churn refusal can stand in for the mutation's refusal, which the test's `AfterOpen`/`in-place` assertion rejects. In the other cases it counts silently as the mutation's refusal.

F3's `settled` doesn't help: it matches only `ChangedDuringRead`, and this test isn't wrapped in it. This test is the most exposed because it builds 27 fixtures and sessions, each walking from `/` several times.

## Fix

- `installation_read_fixture::shared_churn(&ParentRefusal)` holds structurally only for `ParentRefusal::Capture { component, error: Changed }` with `component` above this process's private scratch parent. The bound is the component count of the canonical `test_scratch::temp_dir()`, so it covers `/` through `opensip-test`. No fixture step or mutation under test touches those directories. Every mutation acts on H or below (component 10 and up).
- `settle` allows at most 8 attempts, with F3's backoff of 25 ms × attempt. If the churn never settles, it fails the test.
- `ReadFixture::new` repeats a creation that refused only with `shared_churn`, each time in a fresh scratch root (the body moves into `create`). Any other outcome panics as before.
- `ReadFixture::fence` reopens a session that refused only with `shared_churn` (via `session_churn`). Any other refusal still panics at the unwrap.
- The test reruns a case on a fresh fixture when `capture_with`'s refusal is `session_churn`. Such a refusal never counts as the mutation's refusal. Every assertion is unchanged and runs on the first non-churn result, so the test is no weaker. A mutation that the session failed to refuse still fails.

## Results

- Reproduction under temp-directory churn (a Python loop creating and removing a file in `$TMPDIR`, about 9,000 per second), running the test alone, 10 runs each: 0206ce8 failed 10/10 (6 at `fence()` and 4 at `ReadFixture::new`, all component 6 `Changed`). The fix passed 10/10, in 15–19 s per run against 9 s unchurned.
- Four concurrent full `opensip-security` lib suites, 3 rounds (12 suite runs) each: 0206ce8 had 2 failures, both from the same cause. One was `consumption_rechecks_the_original_file_and_the_held_fence` at `ReadFixture::new` (component 6 `Changed`). The other was `installation_routing::tests::a_lost_race_enters_the_gate_and_admits_the_winner` (`Custody { subject: "ancestor-acl" }`). The fix had 0 failures in 12 runs (754 passed and 2 ignored each).
- Full workspace, twice: 1379 passed, 0 failed, 3 ignored each.
- Clippy (`--workspace --all-targets -D warnings`) and fmt are clean.

Known residual, out of scope: `a_lost_race_enters_the_gate_and_admits_the_winner` uses its own scratch and `route_at`, not `ReadFixture`. Its row (`ancestor-acl`) drops the component, so `shared_churn` can't classify it. It is a candidate F5 with the same root cause.

## Decide

- Does it change test code only?
- Is `shared_churn` narrow enough? Could it mask a real defect, or a refusal under test? In particular, is the component bound right, and can any mutation in the test produce a `Capture … Changed` at or above the private parent?
- Is the root cause right?
- Should the fixture-level retry (which also hardens other `ReadFixture` users) be kept, or confined to this test?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256" (the sha256 of subject.diff). Write REVIEW.md and review.json. Do not commit.
