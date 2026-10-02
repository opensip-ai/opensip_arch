# F6 r1 — wrap the remaining ancestor-walking security tests

**Verdict: ACCEPT**

The scope is the test thread that reaches `judge_ancestor`, because that is the only thread `churned` can see. Wrapping those 230 bodies, with no assertion changes, is acceptable. The two production-file edits stay inside the test modules that were already there. `settled(|| { churned(|| …); })` is the right nesting for the three `store_endpoint` tests. The partial coverage of `two_concurrent_creators_publish_once_and_the_other_loses_the_race` is acceptable as disclosed, and the wrap should stay. `requiredFindings` is empty.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-f6`, detached at `f880145e4b5f0cc4b6307db045b008f770fbc97b`. Twenty-one files under `crates/security/src/`, 6818 insertions, 6348 deletions. No new paths and no role change, so there is no inventory successor.

`subject.diff` is the live `git diff` of that worktree: 639064 bytes, sha256 `387873b6ab5ab5470213755a0c777c9851788f231ca791a231eea7298dc4ce05`. All 21 `hashes.txt` pins match the worktree. `~/Library/Application Support/OpenSIP` is absent.

The committed bytes of these 21 paths are identical from `81214cb` to `f880145`, and from `f880145` to current main `d64ef7b`. The churn table measured at `81214cb` is a measurement of this same subject text. The walkers added after `f880145` are outside the diff: `recovery_admission_tests.rs` already contains seven `churned` wraps at `f880145`, and `settlement_sweep_tests.rs` on `d64ef7b` arrives already wrapped by its author.

`installation_read_fixture.rs` and `lib.rs` have empty diffs. `CHANGED_CAPTURES` and `churned` are unchanged.

## Scope

`CHANGED_CAPTURES` is a `#[cfg(test)]` thread-local in `installation_root.rs`. The only push is in `judge_ancestor`, and only when the capture error is `DescriptorAclCaptureError::Changed`. `churned` is the only reader: it `take`s the vec before the attempt and again after a panic, and it retries only when the vec is non-empty and every component is strictly above the private scratch parent. An empty witness, or any recorded component at the private parent or deeper, re-raises on that attempt. Eight attempts, then the last panic is reported. The backoff is 25 ms times the attempt number.

A wrap can therefore help only a test whose own thread reaches `judge_ancestor`. That is the right set. Tests that never walk record nothing, so a wrap would not retry them. Tests in other crates cannot name this `cfg(test)` `pub(crate)` witness, and `churned` is `pub(crate)` as well.

The census method matches that rule. A temporary patch, reverted before the measured tree, logged `std::thread::current().name()` from `judge_ancestor`. libtest names the test thread after the test, so the log is a list of tests whose test thread walked. A backtrace separated walks on unnamed threads. A second patch logged every `Changed` push; the lead reports a clean security lib with zero such pushes, which is what the retry rule needs: a deliberate mutation at H or below must not become a retry. If one did push, the component would sit at or below the private parent and the every-component rule would re-raise. This review did not re-apply those patches. The tree matches the set the lead reports from them.

Per file, the new wraps are 11, 11, 18, 11, 13, 12, 3, 4, 7, 17, 9, 16, 18, 16, 10, 8, 16, 3, 12, 2, and 13, in the module order given in the request. That is 230. The three F5 bodies are byte-identical to HEAD and still carry their one `churned`: `a_lost_race_enters_the_gate_and_admits_the_winner`, `the_target_holds_no_project_lock_for_the_floor_step`, and `a_revoking_update_is_seen_by_the_checkpoints_own_final_observation`. The worktree holds 233 `churned(||` tokens across the 21 files, against 3 at HEAD. They were not double-wrapped. With those three, the lead's table totals 233, and the routing, namespace-lease, and live rows are the F5 wrap plus the new ones (8, 10, and 19).

`session::a_staging_io_error_rolls_back_then_appends_rev_and_cln` is one of the 16 new session wraps. That is the F5 residual.

## The mechanical wrap

Every `#[test]` in the 21 files was paired with HEAD by name. String and block-comment text was blanked before brace matching, including raw strings and character literals, so a `{` inside a literal did not end a body. Of 296 tests, 66 are byte-identical to HEAD, 227 gained one top-level `churned(|| { … });`, and 3 gained that wrap inside an existing `settled` closure. Zero bodies failed that comparison.

Undoing the wrap is exact. The added lines are `churned(|| {` and `});` at the old body's indent, and every non-empty interior line gained four spaces. Blank lines stayed blank. Restoring those interiors leaves a file that differs from HEAD only in the import edits below. The opening-brace line and the function's closing line are unchanged for every test.

No reindented line begins inside a string literal or a block comment. A leading four spaces on such a line would have changed the literal. The multi-line raw string in `the_crash_points_are_the_laws_names_in_registered_scopes` is in a body that stayed byte-identical, as did `the_carrier_location_has_no_production_constructor_but_the_admitted_place`, whose assertions quote source text that contains braces.

Ignoring whitespace, `git diff -w` is 478 additions and 8 deletions: 230 openers, 230 closers, 18 import additions, and the 8 old import lines those extensions replace.

The import edits are only the name `churned`:

- Ten new `use` lines: `commit_session_tests.rs`, `git_tracking_tests.rs`, `installation_admission_tests.rs`, `installation_parent_tests.rs`, `installation_publication_tests.rs`, `installation_session_tests.rs`, `project_chain_tests.rs`, `initial_platform_tests.rs`, plus an indented `use` inside `creator_parent_tests` and inside `native_read_session::tests`.
- Eight existing `installation_read_fixture` imports gained `churned` in the brace group: `first_registration_tests.rs`, `installation_doctor_tests.rs`, `installation_read_tests.rs`, `operation_handoff_tests.rs`, `ordinary_writer_tests.rs`, `project_admission_tests.rs`, `store_endpoint_tests.rs`, and `installation_observation_tests.rs`.
- `installation_routing_tests.rs`, `namespace_lease_tests.rs`, and `operation_live_tests.rs` already imported `churned` for the F5 wrap. `operation_live_tests.rs` keeps `use super::super::super::installation_read_fixture::churned`, which is the path from `tests::live`. `commit_session_tests.rs` uses the crate path, which resolves from `tests::session`.

The included `*_tests.rs` files are pulled in from a `#[cfg(test)] mod tests` (`initial_platform`'s module is `#[cfg(test)]` as well). `operation_handoff.rs` includes the handoff tests from `#[cfg(test)] mod tests`, and that file's `mod live` and `mod session` include the other two.

## The two production files

`installation_root.rs` is included from `custody.rs` in every build. Its `creator_parent_tests` module is `#[cfg(all(test, target_os = "macos"))]`, and that module starts at the same line in HEAD and in the worktree (line 909). Every hunk is inside the module. The first added line is the `churned` import. `CHANGED_CAPTURES` and `judge_ancestor` are above that line and are unchanged. Net change for the file is +9 lines, which is four wraps and one import.

`native_read_session.rs` is included from `root_payload.rs` under `#[cfg(target_os = "macos")]`, so the file itself is part of a macOS build. Its `#[cfg(test)] mod tests` starts at the same line in HEAD and in the worktree (line 296). Every hunk is inside that module, and the first added line is the `churned` import. Net change is +27 lines, which is thirteen wraps and one import.

Both edits are acceptable. A non-test build compiles the same functions as HEAD.

## Nesting in store_endpoint

Three tests were already `crate::test_scratch::settled(|| { … })`: `a_read_session_admits_the_endpoint_of_its_one_read`, `each_join_refuses_on_its_own_row`, and `an_in_place_rewrite_after_the_read_fails_the_sessions_recheck`. Each now has `churned` as the statement inside that closure. The `settled(|| {` line and the closing `})` line are the HEAD lines, including the absence of a semicolon on `settled`, which is the function's value. `churned` is the statement `churned(|| { … });`.

That order is the F5 rule inside the F3 rule. Each `churned` attempt clears the witness and then runs the body once. `settled` retries only when the panic that `churned` re-raises contains `ChangedDuringRead`. A shared-ancestor `Changed` is retried by `churned` even when the panic text is a different row. A `ChangedDuringRead` panic whose witness is empty, or whose component is too deep, is re-raised at once, and `settled` still applies. A panic that qualifies for neither is re-raised at once.

The other direction would run every `settled` retry inside one `churned` attempt, so the witness would accumulate across those retries. The tree does not do that.

The other three tests in the file stay on `settled` alone: `the_admission_reads_no_file`, `the_creator_path_produces_no_endpoint`, and `the_session_limit_marks_every_bound_of_sixty_four`. Their text is HEAD.

## The race test

`installation_publication::tests::two_concurrent_creators_publish_once_and_the_other_loses_the_race` is one of the twelve publication wraps. Its test-thread walks are witnessed. Its two spawned creators walk on unnamed threads. `CHANGED_CAPTURES` on the test thread does not receive those pushes. If a creator thread is the only one that saw `Changed`, the test thread's witness is empty and `churned` re-raises. The failure is kept. Covering the creator threads would need a witness that crosses threads, which is a recorder change. This unit is the wrap. Leaving the test unwrapped would drop the walks the test thread does make. The disclosed partial coverage is the right close for this unit.

## What this review ran

The check above is the diff, read back against HEAD with a string-aware brace match. This review did not re-run the churn loops, and it did not replay the workspace suite, clippy, or `cargo fmt`. The lead's figures stand as the lead's measurements: at about 270 changes per second, 2 of 233 base failures and 0 of 233 on the fix; flat out, 106 and 55, with each sampled fix failure using all eight attempts. The flat-out remainder is the eight-attempt bound already stated for `churned`. The lead's disclosure of the first Poisson window, about 37 seconds while other security suites were running, is noted here and is not a defect in the wrap. `pgrep` shows no churn process at the end of this review.
