Grok review: F6, wrapping the remaining ancestor-walking security tests in F5's `churned`. Claude Opus 5.5 leads, and you are the single reviewer. Make no repository edits, commits, pushes or delegations. Write only under `/tmp/opensip-implementation/reviews/grok-flake-f6-r1`.

**Subject.** The subject is the worktree `/Users/sb/code/opensip-ai/opensip-f6`, detached at product main `f880145`. The change was built and measured on `81214cb`, then moved to `f880145`. The two commits between them touch none of the 21 subject files, and every file pin in `hashes.txt` was rechecked after the move. Main has since reached `d64ef7b`. Its three newer commits also touch none of the subject files. The new security walkers they add (`custody/settlement_sweep_tests.rs`, X6c) arrive already wrapped in `churned` by their author. Save `git -C /Users/sb/code/opensip-ai/opensip-f6 diff` as `subject.diff`; it is 639064 bytes with sha256 `387873b6ab5ab5470213755a0c777c9851788f231ca791a231eea7298dc4ce05`. The 21 files are all in `crates/security/src/`:
- 19 are `*_tests.rs` files, each included only from a `#[cfg(test)] mod tests` (or `tests::live` / `tests::session`).
- 2 are production files whose change lies only inside an existing `#[cfg(test)]` module: `custody/installation_root.rs` (`mod creator_parent_tests`, which is `#[cfg(all(test, target_os = "macos"))]`) and `trust/native_read_session.rs` (`#[cfg(test)] mod tests`).

No non-test code changes. F5's recorder (`installation_root::CHANGED_CAPTURES`) and `installation_read_fixture::churned` are unchanged. The file set and roles are also unchanged, so there is no inventory successor (the F3/F4/F5 precedent).

Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`, with your own `CARGO_TARGET_DIR`. Never touch the real `~/Library/Application Support/OpenSIP`; it is absent. **Churn caution:** a churn loop in the shared temp directory affects every test run on this machine, including other worktrees (several are active). If you reproduce anything, start and stop the churn inside one command with a `trap`, keep it short, check first that no other `deps/opensip_*` test binary is running, and confirm with `pgrep -fl churn` afterwards.

Precedents: F3 at 8452ab9 (`test_scratch::settled`), F4 at 8bd0283 (`shared_churn`, review grok-flake-f4-r1), and F5 at 96ca141 (`CHANGED_CAPTURES` and `churned`, review grok-flake-f5-r1). F5's review left the follow-up open under "Residual wraps are a follow-up". That list names X3d-1's `a_staging_io_error_rolls_back_then_appends_rev_and_cln`, which failed once in X2c registration setup at `operation_handoff_tests.rs:146`. EXIT-PLAN records it as "F5 widened again (2026-10-03)".

## What changed

230 test bodies are wrapped in `churned(|| { … });`, each re-indented by four spaces. Eighteen files gain or extend one `use … installation_read_fixture::churned` import. Ignoring whitespace, the diff is exactly:

- 230 × `+ churned(|| {` and 230 × `+ });`;
- 18 import additions (10 new `use` lines, plus 8 existing `installation_read_fixture::{…}` imports extended with `churned`).

Nothing else changes: no assertion, no helper, no fixture. A script did the wrapping. It finds `#[test] fn NAME() {` and the body's closing brace at the same indent, and it refuses any body containing a line that starts inside a string literal or block comment, since re-indenting such a line would change the literal. It refused none. One multi-line raw string exists in a changed file (`commit_session_tests.rs`, `the_crash_points_are_the_laws_names_in_registered_scopes`), and that test does not walk, so it is untouched.

**Nesting with F3.** Three tests in `store_endpoint_tests.rs` were already `crate::test_scratch::settled(|| { … })`. For those, `churned` goes inside `settled`: `settled(|| { churned(|| { … }) })`. `churned` then clears and judges its witness once per body run, which is the F5 semantics. `settled` still retries only a `ChangedDuringRead` panic that `churned` re-raises.

## How the set was chosen (empirical, not by reading)

The criterion is: every security lib test whose **test thread** reaches `judge_ancestor`. That thread-local witness is the only thing `churned` can read.

1. **Walkers.** A temporary local patch, never part of the subject and reverted before measuring, made `judge_ancestor` append `std::thread::current().name()` to a log. libtest names each test thread after its test. The full workspace was run with a private TMPDIR.
   - 233 distinct test names walked, all in `opensip-security`. No test thread in host, storage, cli, evaluator, lifecycle or platform walked.
   - 3 of the 233 are F5's wraps, so 230 were left to wrap. The script wrapped all 230.
   - At `f880145` the same census gives 240. The 7 new names are `custody::recovery_admission::tests::*` (X6b), and the X6b author already wrapped each of them in `churned`.
2. **Off-thread walks.** For walks on unnamed threads, the patch logged a backtrace. Every one of them came from `installation_publication::tests::two_concurrent_creators_publish_once_and_the_other_loses_the_race` and its two spawned creators.
3. **Deliberate `Changed` captures.** A second temporary patch logged every `Changed` push into `CHANGED_CAPTURES`, with the thread name and component. The whole security lib then ran without churn: 940 passed, and **zero** `Changed` captures were recorded. So no test produces a recorded `Changed` capture through its own mutation. The tests that mutate on purpose all act outside a capture's sample window:
   - `every_capture_phase_refuses_actual_mutations`;
   - `an_earlier_ancestor_changed_during_capture_or_consumption_refuses`;
   - `native_session_original_file_and_every_ancestor_survive_repeated_capture`;
   - the admission tests that assert `CustodyRefusal::Changed`.

   Those mutations act at H or below, and they reach the test as other rows. Even if one of them did record a capture, it would sit at or below the private parent, and the "every component" rule would re-raise it immediately.

The wrapped modules and counts are: `first_registration` 11, `git_tracking` 11, `installation_admission` 18, `installation_doctor` 11, `installation_parent` 13, `installation_publication` 12, `installation_read` 3, `installation_root::creator_parent_tests` 4, `installation_routing` 7, `installation_session` 17, `namespace_lease` 9, `operation_handoff` 16, `operation_handoff::tests::live` 18, `operation_handoff::tests::session` (commit_session) 16, `ordinary_writer` 10, `project_admission` 8, `project_chain` 16, `store_endpoint` 3, `installation_observation` 12, `trust::…::initial_platform` 2 and `trust::…::native_read_session` 13. That totals 230; with F5's 3 already in place, all 233 walkers are covered. The set includes `session::a_staging_io_error_rolls_back_then_appends_rev_and_cln`.

## Left unwrapped, or only partly covered

- **No walking test was left unwrapped.** None asserts on a capture it deliberately mutates (point 3 above).
- **Partly covered:** `installation_publication::tests::two_concurrent_creators_publish_once_and_the_other_loses_the_race`. It is wrapped, and its test-thread walks are witnessed. Its two spawned creators walk on unnamed threads, which the thread-local witness cannot see. A churn refusal on a creator thread alone leaves the witness empty, so `churned` re-raises it. That is fail-safe, but the test is not covered there. Covering it would need a cross-thread witness, which means production-side or recorder changes that this unit does not make.
- **Not walkers, so not wrapped:** `trust_bootstrap`, `live_observation` and `floor_publication` tests, and the non-walking tests in the wrapped files. None of them reached `judge_ancestor` on any thread. Those that already use F3's `settled` keep it.
- **Out of reach:** tests in other crates. `CHANGED_CAPTURES` is `cfg(test)` in `opensip-security`, so another crate's tests cannot read it, and the census found none that walk on their test thread.

## Results

**Churn experiments.** These ran on the shared `$TMPDIR` (`getconf DARWIN_USER_TEMP_DIR`), measured at `81214cb`. The binaries were base `81214cb` and fix (this subject at `81214cb`); the subject files are byte-identical at `f880145`.
- The loop creates and removes one file in `T`. For each module, it starts churn, runs the base binary then the fix binary on that module's exact walker names, and stops churn, all inside one script with a `trap`.
- Before each module, the script waited until no other worktree's `deps/opensip_*` test binary was running.
- `pgrep -fl churn` was empty after every round.

Per-module failures (n counts F5's 3 too, which are wrapped on both sides):

| Module | n | Poisson ≈270/s base | fix | flat out base | fix |
| --- | ---: | ---: | ---: | ---: | ---: |
| `custody::first_registration::tests` | 11 | 0 | 0 | 10 | 3 |
| `custody::git_tracking::tests` | 11 | 0 | 0 | 3 | 0 |
| `custody::installation_admission::tests` | 18 | 0 | 0 | 10 | 1 |
| `custody::installation_doctor::tests` | 11 | 0 | 0 | 1 | 0 |
| `custody::installation_parent::tests` | 13 | 0 | 0 | 2 | 0 |
| `custody::installation_publication::tests` | 12 | 0 | 0 | 3 | 0 |
| `custody::installation_read::tests` | 3 | 0 | 0 | 1 | 0 |
| `custody::installation_root::creator_parent_tests` | 4 | 0 | 0 | 0 | 0 |
| `custody::installation_routing::tests` | 8 | 0 | 0 | 1 | 0 |
| `custody::installation_session::tests` | 17 | 0 | 0 | 2 | 0 |
| `custody::namespace_lease::tests` | 10 | 0 | 0 | 9 | 8 |
| `custody::operation_handoff::tests` | 16 | 1 | 0 | 16 | 13 |
| `custody::operation_handoff::tests::live` | 19 | 1 | 0 | 18 | 18 |
| `custody::operation_handoff::tests::session` | 16 | 0 | 0 | 13 | 12 |
| `custody::ordinary_writer::tests` | 10 | 0 | 0 | 3 | 0 |
| `custody::project_admission::tests` | 8 | 0 | 0 | 4 | 0 |
| `custody::project_chain::tests` | 16 | 0 | 0 | 2 | 0 |
| `custody::store_endpoint::tests` | 3 | 0 | 0 | 1 | 0 |
| `installation_observation::tests` | 12 | 0 | 0 | 3 | 0 |
| `trust::root_payload::initial_platform::tests` | 2 | 0 | 0 | 0 | 0 |
| `trust::root_payload::native_read_session::tests` | 13 | 0 | 0 | 4 | 0 |
| **Total** | **233** | **2** | **0** | **106** | **55** |

- **Poisson ≈270/s, 2026-10-01 18:32:43 to 18:39:33** (≈6.8 min of churn in 21 short windows). Base failed 2 of 233 and fix failed 0 of 233. The two base failures were in setup on the X2c/handoff walk:
  - `operation_handoff::tests::a_failed_rollover_reservation_is_returned_with_no_copy` at `operation_handoff_tests.rs:126` (`admit_project_root(…).unwrap()`);
  - `live::a_replacement_during_the_first_attempt_is_absorbed_and_a_second_is_mixed` at `operation_live_tests.rs:598` (`begin_live(…).unwrap()`).

  This is the same shape as the reported `operation_handoff_tests.rs:146` failure.
- **Flat out, 18:39:52 to 18:54:33**, including gate waits. Base failed 106 of 233 and fix failed 55 of 233. Every fix failure is in the long-setup modules (`namespace_lease`, `operation_handoff`, `live`, `session`, `first_registration`), plus 1 in `installation_admission`.
- **Diagnostic, flat out, 18:55:39 to 18:57:26.** The fix binary ran on all of `namespace_lease` and `first_registration` plus that `installation_admission` test, with the panic lines counted per test. It produced 13 failures, and **each one panicked exactly 8 times**: all eight attempts were used up, and none was re-raised early for a non-churn reason. This is F5's stated limit. Under continuous churn, a setup with hundreds of walks rarely gets a clean attempt. At the realistic rate the fix holds.

**Checks**, with a private 0700 TMPDIR under `getconf DARWIN_USER_TEMP_DIR`:
- At `81214cb`, the full workspace ran twice: 1634 passed, 0 failed, 3 ignored each time (18:07 to 18:26).
- At `f880145`, the full workspace ran twice: 1678 passed, 0 failed, 3 ignored each time (19:03 to 19:20). Clippy and fmt were rerun there too.
- Clippy (`--workspace --all-targets -D warnings`) is clean, and `cargo fmt --all --check` is clean. `rustfmt` does not follow `include!`, so the included test files are outside that check, as for F4 and F5.

**Disclosure.** My first Poisson attempt (18:26:40 to 18:27:17, about 37 s) started while three other worktrees' security suites were running. I stopped it and added the gate described above. That window may have affected those runs.

## Decide

- Is "every test whose test thread reaches `judge_ancestor`" the right scope, and is the census method sound?
- Is wrapping 230 tests mechanically, with no assertion changes, acceptable? Is the change to two production files, confined to their existing `cfg(test)` modules, acceptable?
- Is `settled(|| churned(|| …))` the right nesting for the three `store_endpoint` tests?
- Is the partial coverage of `two_concurrent_creators_publish_once_and_the_other_loses_the_race` acceptable as disclosed, or should it be left unwrapped?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256" (the sha256 of subject.diff: 387873b6ab5ab5470213755a0c777c9851788f231ca791a231eea7298dc4ce05). Write REVIEW.md and review.json. Do not commit.
