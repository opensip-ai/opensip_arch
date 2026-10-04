# Unit X9-6 r1

Verdict: **ACCEPT-UNIT**. Inventory: **NOT-APPLICABLE**. No file was added, and inventory v134 already lists all six paths this diff touches.

Law X9 r16 item 12, the M2 exit of the crash matrix. Worktree `/Users/sb/code/opensip-ai/opensip-x9-6` is detached at `2967905d8152a5f2e431cd8006e1b82f898c3fe2`. Nothing was committed. `git diff 2967905` is 522499 bytes, sha256 `d68bcdf9e0e0203e5b563f298c57834632899d11c3f8332c7af345b94032430e`, six files, +748 −91. Porcelain stayed those six modifications. `~/Library/Application Support/OpenSIP` stayed absent.

## Rerun timing

This review did the census, the transcription reproduction, coverage, the release-absence record, and the code review now. The two full sets are deferred to one rerun on the integrated commit C, in a short follow-up request. This review covers the diff and the lead's pre-integration evidence. After C, that rerun is the third execution of the matrix (item 7).

## What this review ran

Private 0700 `TMPDIR` under `DARWIN_USER_TEMP_DIR`. `CARGO_TARGET_DIR` under this review directory. `cargo --locked --offline`. The two censuses ran one after the other. No kill-matrix set ran beside them.

| Check | Result |
|---|---|
| Storage census `OPENSIP_X9_CENSUS_ONLY=1`, `x9_6_matrix`, run set `x96-grok-census-storage` | Passed. `census.json` is byte-identical to the lead census: 21368 bytes, sha256 `6fa3cc023a9540eb30f79c129c3b5be665f724a0b59dc49b122d52570c223ffa`, 259 points, trace digest `e9add21ea35fcd31da809930ed05c619cd36da3b77e818cfd8e651b6d4e8b61f`, 1379 records. |
| Host census `OPENSIP_X9_CENSUS_ONLY=1`, `x9_5_matrix`, run set `x96-grok-census-host` | Passed. `census.json` is byte-identical to the lead census: 18020 bytes, sha256 `2492cbd0e796712de3011ecbfc9253fdfabc821c45614c9eb4ed32d0802498ee`, 218 points, trace digest `93d0922ab69945043d769e0361fd0121662052ffadf44970c5425d78511cf8d6`, 1195 records. |
| `transcribe_x96.py` on `git show 2967905:` of both required-runs files and those censuses | Storage 381 rows and host 98 rows. Both outputs are byte-identical to the worktree fixtures (191655 / `14a275ad73ab1036b109e35b923f59f77c36dcab50a4145e9333696910626aa9`, 53953 / `80e4a02eb2862e1e5d5d2e3f395707d1b775a0cafd7bdf06b0e188e0e65090d5`). Windows: W1a 9, W1b 8, W2 12, W3 3, W4 6, W5 2, W6a 4, W6b 2, W7 4. Uncovered before transcription: 50. |
| `coverage` on the transcribed fixtures | Kill set 383, killed points 383, nothing outside the kill set, union census 321, `passed` true, `matrixPass` false. |
| `coverage` on the landed `2967905` fixtures | Killed points 333, `passed` false, 50 uncovered, the same union of 321 and kill set of 383. |
| Checker unit tests | 26 OK. |
| `the_release_order_condition_reads_a_commit_childs_trace` | Passed. Lawful order, three reversals, a missing fence, and a missing evidence COMMIT. |
| `the_commit_driver_census_is_equal_across_two_runs` | Passed. The two censuses are equal, and `release_order_misses` on the lawful commit is empty. |
| `opensip-cli` release, no features | 6315264 bytes, sha256 `b32604fe8c83343a93e7e38f023abc330afda2fa0f7cb255c842ab2b52aa5e49`. The scan found no `OPENSIP_X9_` string and none of the 25 scope names. |
| `cargo build --release -p opensip-storage --features crash-matrix` and `-p opensip-host --features crash-matrix` | Each exited 101 at `crates/platform/src/lib.rs:6`. |
| `precheck_x96.py` on the lead pair | Byte-identical to `lead-precheck.json`: 56877 bytes, sha256 `6c99a0cfa1b3cbbf536c0bc82c2e82bc025c11b8696e610757c6d3fea532cd11`. 479 runs, repetitions agree, union 321 points, kill set 383, all 383 killed in each repetition, `passed` true, `matrixPass` false, `worktreeClean` false on both targets. |
| Real `check` on the two lead sets | Refused with the clean-commit sentence, byte-identical to `lead-check-refusal.txt`. |

The raw census traces differ from the lead traces in the execution-id hex of a few payload lines. The normalizer strips those ids, which is why `census.json` and the point sequence match.

Normalized maps from that reproduced precheck: storage `1e094ddba47c9e247ec3976c84aa1822ae1ea5f8567f11688ebdb087046ae143` (381 entries, 88 distinct) and host `ede9384ce31d38cef459d16abe0332747b19507eb561614cdfad939dd556cb84` (98 entries, 18 distinct). Against this reviewer's earlier `check-unit.json` files, X9-3's 57 storage keys, X9-4's 47 storage keys, and X9-5's 94 host keys match with 0 differences. The reproduced precheck covers the remaining landed storage keys, including X9-2's 231, and the two lead repetitions agree on every `normalizedSha256`. Comparing a reviewer set with the lead sets waits for the rerun on C.

## What stayed with the lead's record

The lead's development runs, the two full lead sets, `cargo fmt`, the two workspace runs, the feature-lane test run, clippy, and `check_package_edges.py` stayed as the lead recorded them. This review reproduced the precheck and the clean-commit refusal from those lead sets. It did not rebuild the scratch evidence tree.

## Scope

The diff is tests, the two required-runs fixtures, and the checker. No `crates/*/src` file is in it. The Rust and Python diff adds no `cfg`, no authority type, and no `compile_error`. The platform guard at `crates/platform/src/lib.rs:6` is the existing release refusal, and both feature builds hit it.

`check` is the two-target gate. It takes storage and host once each. Each target is checked as before, the commit must be the reviewed one with a clean worktree, both files share one `clockEpoch` (1791072000), and the repetitions of a target must agree. The union takes points by name, the larger occurrence count, and equal durability. The kill set must be wholly killed by either target, in each repetition. `matrixPass` is true only for that gate. `killedOutsideKillSet` is reported. The one-pair `check()` remains for `check-unit` and the regression controls. `check-unit --unit` still offers only X9-2 through X9-5, so `--unit X9-6` is refused. A row with `unit` belongs to that unit alone, so an X9-6 row is outside every unit subset, and `check` still requires every row.

`coverage` reads a census and the required runs, runs nothing, and reports `matrixPass` false. It passes when the union kill set has no uncovered point.

Storage's `x9_6_matrix` runs every storage row. Its census is X9-3's commit, recover, and sweep parts, then the refused end, each part twice and equal, lines in that order. Host's `x9_5_matrix` drops every row that carries `unit`, so X9-5's 94 rows stay its set. Host's `x9_6_matrix` runs all 98 host rows on X9-5's census. `owned()` still gives a row with `unit` to that unit alone, so X9-2, X9-3, and X9-4 exclude the X9-6 rows.

`union_census` is the landed census body plus an equal-length guard on the two runs of each part. `commit_part` is the landed X9-4 loop body. `x93_parts` is unchanged. The release-order function is the same text in both targets. Storage applies it when the outcome starts with `Committed`, which includes a latched F39. Host applies it when the outcome starts with `kind=authoritative`. A miss turns that run's PASS into FAIL, in the same class as R1 `stateUnchanged`. Killed and refused children fall outside those outcome prefixes. Acquisition is the first record of seal begin, then evidence begin, then seal level-four. Release is the first record of evidence commit after, then release level-four, then release level-three, then the writer unlock after the seal's level-three release, then the fence-end unlock after that lease. An owed REV or CLN that appears after the seal's level-three release must release level-four then level-three before that writer unlock.

The fifty transcribed rows all carry `"unit": "X9-6"`. Storage gains 46 (334 prior rows with no unit, plus the one X9-4 row, plus 46). Host gains 4 (94 plus 4). Cases: F02 9, F07 8, F11 12, F13 3, F14 6, F16 2, F17 2, F19 2, F53 6. `R2.witnessAction` is `OK` on the eight F07 rows and the twelve F11 rows. Distinct is set on the three F13 rows, the six F14 rows, and all four host rows. F02 matches an existing F02 kill. F13 and F14 use the committed-historically ladder with distinct. The two F19 rows reuse the landed REV template with the kill point substituted, and their expected values stay that template's ladder. The six F53 rows reuse the sweep templates: the four points before `settle.commit.before` keep the second-sweep refusal, and the two unlock points after `settle.commit.after` keep the second sweep that writes nothing. The string substitution rewrites both the arm and the await. Host F16 and F17 use the host committed-historically ladder, with `{"r2":"distinct"}` first. Storage puts that directive last on its nine distinct rows. Both executors find `r2` anywhere in the script.

`a_process_makes_at_most_one_driver_entry` remains. The census-equality test now also requires an empty release-order miss list on a lawful commit.

## Judgment calls

1. **Storage census composition.** Accepted. Commit, recover, sweep, then the refused end, each part twice and equal. The reviewer census matches the lead `census.json`.
2. **Release-order reading.** Accepted. First record of each named point, lease and fence taken after the seal's level-three release, commit outcomes only, a miss is a verdict FAIL. The synthetic test and the lawful census assertion both passed.
3. **Host `x9_5_matrix` drops rows with `unit`.** Accepted. `x9_6_matrix` runs every host row. X9-5's subset stays the 94 rows with no unit member.
4. **`union_census` and `commit_part` are refactors.** Accepted. The moved logic matches the landed functions, with the equal-length guard added. X9-3's 57 and X9-4's 47 normalized keys match the reproduced lead maps with 0 differences.
5. **CLI `check` requires both targets.** Accepted. The one-pair Python `check()` remains for `check-unit`.
6. **`coverage` is a transcription aid.** Accepted. It reports `matrixPass` false, and the transcribed rows leave 0 uncovered.
7. **Transcription by census position.** Accepted. Replaying the script on the landed required-runs files and this review's censuses reproduced both fixtures byte for byte. The W5 and W6 rows reuse the landed F19 and F53 scripts with the kill point substituted.
8. **`precheck_x96.py` is a diagnostic.** Accepted. It lives in the review directory, calls the checker's own functions, and reports `matrixPass` false. The real `check` still refuses the dirty worktree.
9. **F11 witness action OK.** Accepted as a reported result of the lead's dev1, dev2, and both lead sets, and as the encoding in the reproduced fixtures: W1b and W2 add `R2.witnessAction` `OK`. This reviewer's own run of that score is the rerun on C.

## The gate

Item 7 refuses a matrix pass on a dirty worktree or on a commit other than the reviewed one. These lead sets record `worktreeClean` false, and the real `check` refuses them with the clean-commit sentence. That refusal is the gate. `precheck_x96.py` applies the other conditions and keeps `matrixPass` false.

After acceptance the lead integrates this diff as main commit C, runs release absence, two full sets, and the real `check` on a clean checkout, and writes the r16 evidence record under `crash-matrix-x9/evidence/<C>/`. The reviewer's rerun on C is the third execution.
