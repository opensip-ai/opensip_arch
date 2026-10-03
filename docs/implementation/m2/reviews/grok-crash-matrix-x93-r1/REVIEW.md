# X9-3 r1 — ACCEPT-UNIT

X9-3 implements law X9 r14's storage commit and recovery rows on product main `b999ae34ed567a010bd789488512884fa38df05b`. The worktree is detached there, uncommitted, with ten modified files and no added file. `git diff b999ae3` is 334747 bytes, sha256 `f0d7c4c1bba5cf70625940dcec08c1584255ed74e84b6c51a0192fa62347b2af`, +1556 −122. The lock at that commit selects inventory v131. There is no successor. Inventory assessment is ACCEPT on the diff.

The rerun used a private `0700` TMPDIR and `CARGO_TARGET_DIR` under this review directory, `cargo --locked --offline`, and the two matrix sets one after the other. The real home stayed absent. The worktree HEAD and the ten-file diff were unchanged at the end. No product commit.

## What this review ran

| Check | Result |
| --- | --- |
| Pins in `hashes.txt` | All matched, including the diff, PROPOSAL-r14.md (`f2800ff9…`, 145042 bytes), the required-runs fixture, and both lead `matrix.json` files |
| X9-2 census, then X9-3 census (`OPENSIP_X9_CENSUS_ONLY=1`) | Both tests passed (13.62 s and 7.79 s) |
| `transcribe_required_runs.py` on those censuses | Byte-identical to `required-runs.v1.json`: 130804 bytes, sha256 `9a34fc5630d4c8f63738c559ad8383c90e8abf4057dab6807899eb4c5e9b8cff` |
| Release `opensip-cli`, no features | 6315264 bytes, sha256 `b32604fe8c83343a93e7e38f023abc330afda2fa0f7cb255c842ab2b52aa5e49`, the lead's binary |
| Release-absence scan | `passed`, `found` empty |
| `cargo build --release -p opensip-storage --features crash-matrix` | Exit 101 at platform's compile guard |
| Checker unit tests | 17 passed |
| `x9_3_matrix` as `x93-grok-1`, then `x93-grok-2` | 57 PASS each, 338.09 s and 340.25 s, 0 FAIL, 0 HARNESS-ERROR |
| `check-unit --unit X9-3` on that pair | Passed, and the JSON is byte-identical to `lead-check-unit.json` (6063 bytes) |

The normalized map of the 57 runs is sha256 `b0f0a5a8a7ab954345b391176dbea49a756c4ce3a13ce0d7b6320853dffd3b28`, 30 distinct values. `x93-grok-1`, `x93-grok-2`, `x93-lead-1` and `x93-lead-2` agree run by run on `normalizedSha256` and on every child's trace digest. That is the three-execution agreement the law asks for: the two lead sets and this rerun. `timingGuard` was recorded and left out of the comparison. This review's four measurements are 2,818, 2,813, 2,820 and 2,858 ms, all inside 5,000. The lead sets measured 2,766, 2,767, 2,786 and 2,790 ms.

The full workspace lane, clippy, rustfmt, `check_package_edges`, and the optional `x9_2_matrix` rerun are the lead's report. This review did not repeat them. The lead's X9-2 regression file carries map sha256 `4e5cba342b438abb749f73861161e6cd4cf38e6bdbd992a00068507d5df3ddaa`, 231 runs, census 212, kill set 281, 219 killed points.

## Scope

`X93_CASES` is F11–F15, F23–F25, F27–F29, F33, F36, F42–F45, F49, F52 and F53. The fixture holds 288 rows: the 231 rows at `b999ae3` are the prefix, equal object for object, and the 57 appended rows are those cases in the counts the law's table names (F11 has 4, F52 has 11, F53 has 7, and the rest match). `x9_2_matrix` still runs X9-2's rows through the same `run_matrix`. The trace digest both matrices share is r14's group order, applied in `normalized_lines` before drawn values are numbered.

The matrix target has five tests: `matrix_child`, `x9_2_matrix`, `x9_3_matrix`, the one-entry test, and the commit-driver census equality test. The diff adds no `cfg`, no `compile_error`, and no authority type. `synthetic_run_candidate_distinct` is a second inputs-only binding of the same session: the snapshot source `extensionless` is replaced with `salted!\n` only after an assertion that the corpus bytes have that length, and the fixpoint rewrite follows. `replay_run` remains the only `ReplayedRun` constructor. `revoke` is its own child process and publishes the closure the commit child wrote under the run scratch. The one-entry test still refuses a second operation, a sweep, a recovery admission, and `publish_revocation` after the first entry.

## Census and transcription

X9-3's census, in one scratch, traces an unarmed commit, `recover` of that attempt (the test requires a `committed-historically` outcome), and the sweep (the test requires `committed`). A second pass must match each driver's census or the run is a harness error. The unit census is the union by point name at the largest occurrence count. The digest hashes the three drivers' normalized lines in that order, and `census-trace.txt` prefixes each line with the driver. This review's census has 227 points and a kill set of 289. The trace is 1,144 lines: 1,111 commit, 12 recover, 21 sweep.

The transcription was rerun from this review's X9-2 census, its trace, its reference run, and this review's X9-3 census, before any of this review's kill runs. The output equals the fixture. Kill points come from those censuses. Expected values are the script's transcription of r14 and the owning laws, which is what the fixture already contained.

## The rows the rerun agreed on

Because the transcribed fixture matches and every run's post-state and child traces match both lead sets, the executed rows are the lead's rows. The shapes this review checked in the transcriber and the runner:

- F11 kills each `x3c.evidence.stage-*` point. F12 is `fail-after` and `fail-before` at `x3c.evidence.commit`, with the undetermined end (nothing owed or appended, reserve forfeited, end step absent).
- F13, F14 and F15 carry `r2: distinct`. F14's kill is `x3d.publish.published`. `x3d.finish.settle.before` is absent from these rows.
- F15 records `R2.receipts` as the receipt rows for the crashed ExecutionId.
- F23 and F24 name `ladder` `R1,R2,R3`. F25 names `R1` only, CAD `evidence.missing` or `evidence.corrupt`.
- F27's operation and execution swaps expect UC `ledger-join`; the request variant expects BU `operation`.
- F36 names R1–R5 and expects R5 CH settled with one RunId across the two SEALs.
- F42's forget variant arms `fail-before` at the evidence commit and expects the forgotten end, then UAO.
- F44 and F45 hold at `x4.observer.tick#1`, then `x3c.evidence.commit.before#1`, then the REV point, with the publisher child between the tick and the admission resume. The guard reads `GuardClock::now` at those two holds.
- F49(a) expects CH pending. F52 has eleven cells and one TNC (`settled-refused-none`). F53 includes both `x6.sweep.settle.commit` kills.

## Judgment calls

1. **GuardClock.** The matrix target names the monotonic clock once, `type GuardClock = std::time::Instant;`. The security no-sleep pin skips that one line in `commit_tests.rs` and asserts it appears at most once. `TIMING_GUARD_LIMIT_MS` is 5000 in `run_record.rs` and in the checker. A run that arms `x4.observer.tick` must carry `timingGuard` inside the limit; any other run that carries one is refused. The checker test covers a passing pair, a missing guard, 5,001 ms, and a stray guard. The member is omitted from the repetition comparison.

2. **F49 tie-break.** Tables whose SQL contains `WITHOUT ROWID` are ordered by row shape. When any shape is shared, those rows are ordered again by how each row normalizes against a numbering primed on the dump with every tied row removed. The four sets agree on F49 `reader-skewed-by-append`, including its `normalizedSha256`. The lead regression file's 231 X9-2 digests are the accepted map.

3. **Unreadable and undumpable files.** A permission failure is recorded as path, size and mode under `logical.unreadable`, and those bytes stay out of `raw`. A SQLite header that will not dump is `{"undumpable": true}`, and those bytes stay in `raw`. `unreadable` is inserted only when the list is non-empty.

4. **Recovery text.** `standing_text` prints a confirmation as its evidence details (CAD), then settlement, anchor, diagnosis and limitation, and UC with its diagnosis. Rows that leave a member open use the `:*` suffix already in the fixture.

5. **Census union.** Implemented as r11's host rule: per-driver equality, union at the largest occurrence, digest over the drivers in order. The rerun's census is 227 points and the kill set is 289, which `check-unit` accepted, with 11 killed points inside that set.

6. **F23 and F24.** Their scripts name `R1,R2,R3`. The default mutation ladder stays R1 and R2 where a row does not name steps. F25 names R1.

7. **F42 forget.** `end_of` `mem::forget`s the `StoppedSession` when `forget=1`, after `fail-before` at the evidence commit. The expected end is `forgotten` and R1 is UAO.

8. **F52.** Four cells are real runs (kill at attempt commit, a lawful commit, that commit swept, that kill swept). The other seven are parent mutations with triggers lifted: settle-refused, settle-committed, delete-attempt (with and without the pair), delete-association, delete-receipt, and availability generation 1 `purged` with the largest object removed.

9. **Owning-law members.** The fixture's expected objects include the settlement member on confirmations, F12's end disclosure, F44's `pending-above-floor`, and R5's `settled`. They were reproduced by the transcription.

10. **Mutation choices.** The largest object is unique by size or the run is a harness error. Wrong generation rewrites the first hex digit of every store-generation column. F27 rewrites one association-body member. F33 rewrites assurance, signer, the first inventory digest, or `journalBodySha256`. F43 deletes journal rows at and above `journalSeq`. F28 plants generations 1 and 2 pruned, 3 closed, 4 open, and sets the witness and the floor to generation 4 sequence 1.

11. **Salt.** `SALT` is `b"salted!\n"`. The distinct binder asserts the corpus file has that length and differs from the salt, then rewrites.

## X9-2 traces under the group order

`lead-x92-trace-comparison.json` covers the 48 F02–F05 and F07–F10 rows. Every `normalizedSha256` is equal to the baseline, and the two new sets agree on every trace. F07–F10 contribute no changed child. Of the 22 F02–F05 rows, 14 change exactly the killed child `commit` at ordinal 1, and each of those 14 is a middle or last occurrence (`#41` or `#82`). The `#1` kills are unchanged. No F02–F05 row changes the next writer's trace. r14's header also names that next writer among the children whose digest the rule changes. The comparison shows the killed child's partial group moving, which is the effect the rule has on these rows, and no expected value in the fixture depends on the next writer's trace digest.

## Outside this unit

The lead reports that X9-1's `a_scripted_clock_gives_each_ordinal_its_own_increasing_wall_seconds` fails when the wall clock sits between 2026-10-03 00:00 and 03:00 UTC, because its fixed epoch is 1,790,985,600. This review did not run that test. It is platform self-test code outside the ten-file diff.

## Inventory

No file is added. The ten paths keep their inventory rows: `commit_tests.rs`, the required-runs fixture, the checker and its test, and the support modules. v131 stays the selected inventory. `inventoryCandidateAssessment` is ACCEPT with no candidate.
