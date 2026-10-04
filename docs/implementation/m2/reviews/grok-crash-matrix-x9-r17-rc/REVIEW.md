# X9 r17 round 1 — ACCEPT

Scope is the r17 header, the section frame, and §RC. Verdict ACCEPT. No required findings. `noAcceptedOutcomeChanged` is true.

Subject `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`, 235499 bytes, sha256 `89fc47ff2ac17c0628cfdd68fce26fcc6eb6416b54e0cca78f61c5c474ff375c`. Diff base `PROPOSAL-r16.md`, 185750 bytes, sha256 `f08efe95deba681f2940a043c80c91b4faae4e4c804ca5865c024e0e083c0a85`. Product lines read with `git show d2c00a9:<path>`. Those blobs match `hashes.txt`. No census, lead set, or product build was run.

## Scope of the diff

Against r16 the only edits are the title, the r16 acceptance stamp on the preserved line (a stamp only), the r12 re-commit sentence at line 268, the r17 header, six in-place notes (items 5, 7, 8, 9, and 12, plus that r12 sentence), one forbidden substitute, and the appended "X9 r17 sections" (frame, §RC, reserved §S12 and §RW). §S12 and §RW are headings with no rows.

## Frame and LD-17-1

Section-by-section acceptance of one revision matches M3-PLAN r9's X9 r17 row (M3P:319) and the three citations that name "X9 r17": X3c r8 CL-2 (X3C:354), J1 successor S12 (J1:858), and J-RW X-RW-10 / RW-S6 (JRW:669, :625). Rules 1–6 keep the sections independent. Rule 2 allows a re-transcription only where the owning law requires it, listed by case and variant with old and new values; §RC has none. Rule 3 is r16's `"X9-6"` reading applied to `"X3c-3"`. Rule 6's snapshots are the right diff bases for later rounds of this same revision.

The reserved headings match their pins. §S12 names J1 item 12 and S12 (J1:832-841, :858), J3b for S12-B/-C/-U/-D and J3d for S12-O (J1:882-883), S12-C/-U only once S21 is accepted (J1:833), and S12-O after S18, which J1 r5 records as accepted and bound at `5214350` (J1:865). §RW names item 10, X-RW-10, and RW-S6 (JRW:519-596, :625, :669), J4e (JRW:607), and L11's retirement only on the evidence item 10 names (JRW:588). The second-integrator sentence is JRW:668, which is the sentence RC.6 cites.

## Spellings

LD-RC-1 through LD-RC-5 fit the checker and the harness at `d2c00a9`.

- Case grammar is `F[0-5][0-9]` and variant grammar is `[a-z0-9][a-z0-9-]*` (`check_crash_matrix.py:257`). Every RC case and `recommit-` variant matches. No existing variant starts with `recommit-`.
- RC-1 as F15, RC-2 as F04, RC-7 as F23, RC-4 as F12, and RC-5 as F13/F14/F15 by kill point follow X3c's windows and the owning rows. F15's existing R1 is `committed-historically:*`; F13 and F14 use `pendingSettlement`. RC-5 keeps that split. RC-4's `end(...)` string is F12's `scripted.end`.
- `"unit": "X3c-3"` belongs in `UNIT_VALUES` beside `"X9-6"` (`:105`), not in `UNIT_CASES`. `check-unit`'s choices are `UNIT_CASES` only (`:536`), and `in_unit` keeps a row with a `unit` member out of every other unit's subset (`:268-274`).
- The step form is `interpret` (`commit_tests.rs:1818-2160`). Every template key (`spawn`, `finish`, `unchanged`, `arm`, `await`, `then`, `ladder`, `of`, `r2`, `for`, `mutate`, `distinct`, `resume`, `on`) is read there. X9-2's form has no `spawn` (`:1659-1664`).
- `r2` selects the distinct variant only when the value is `distinct` (`:1753`, `:2122`). The 26 existing `r2` directives are all `distinct`. `"same"` is the candidate, and RC.7's guard rejects any other value. `meets` (`:1112-1123`) is the `:*` rule the expected spellings use. The verdict compares a key only when `expected` names it (`:2973-2986`).

## Census and LD-RC-6

At C the storage census is 259 points and its kill set 321; host is 218 and 271; the union is 321 points and 383 kill-set points. `check.json` has `killedOutsideKillSet` empty. All 82 `x3c.object/{create,write,file-barrier,link,directory-barrier}` occurrences sit in the commit part. `reopen-confirm` is absent. Host's counts for those names are also 82, so the union is 82.

`publish_new_regular` is create, write, file-barrier, link, directory-barrier (`filesystem.rs:1163-1206`, link at `:575-607`). A name that already exists fails at link, so `link.after` does not pass, and `confirm_existing_regular` then does one more file-barrier, one directory-barrier, and `reopen-confirm` (`:688-736`, called from `blob_store.rs:94-97` inside `crash_scope!("x3c.object")`). That is X9:446. E2 therefore reaches file-barrier 164 times and `reopen-confirm` 82 times, and reaches create, write, `link.before`, and directory-barrier 82 times. `link.after` stays 0 in E2. Selection `(n+1)/2` (`driver.rs:571-582`; `check_crash_matrix.py:172-179`) moves file-barrier from `#1,#41,#82` to `#1,#82,#164` and selects `#1,#41,#82` for each new name.

An existing ledger returns before any `x3c.ledger-create` file point or schema barrier (`project_ledger.rs:537-563`). Admitting an existing store directory still takes the two directory barriers and no create (`store_custody.rs:146-174`), which does not exceed the union. Staging on the re-commit branch reaches `stage-recovery_pair` and `stage-run_material` only (X3C:185; `project_commit.rs:469-530`). Those names are already at 1. Root, carrier, and trust steps of a process that follows an earlier one on the same root are the case r16 recorded at X9:736-741, where storage's count is already the union's. No other name in that path rises above the union.

The part adds 8 kill-set points and drops the two file-barrier `#41` selections. Net +6: storage kill set 321 to 327, union 383 to 389; census points +2.

F03's `kill-x3c-object-file-barrier-before-41` and `-after-41` kill those two points and nothing else in the file does. `check` records `killedOutsideKillSet` and does not refuse (`check_crash_matrix.py:481-489`). `check-unit` refuses (`:375-377`), and X9-2's census is the commit part only (`commit_tests.rs:3139`), which still has 82 and `#41`. F03 still kills `#1` and `#82`. RC-2's eight rows are the eight added points. RC-3's and RC-5's six `#1` points are already in the kill set (`stage-recovery_pair`, `stage-run_material`, `commit.after`, `commit-returned`, `published`, `end-step.after`). r16's count-shift sentence (X9:741) re-transcribes when a shift leaves a selected point unreached. Here every selected point stays covered, so leaving the two `#41` rows byte for byte is the right reading of frame rule 2.

## Rows

The 22 expected blocks spell X3C:277-307. Post-state keys are read at the ladder capture, after the scripted children and before R1 (`:2103-2111`); RC-8 has no ladder, so its capture is the end (`:2137-2147`). New keys are compared only where a row names them.

RC-1's stage list is the first-commit order at `project_commit.rs:472-530`, and E2's list drops availability and pins. RC-3's two SEALs and `sameRunId` depend on RC.7's generalization (at least two SEALs, every SEAL one RunId). F36's two rows hold exactly two SEALs and score `R5.sameRunId` true (`seal_runs` at `:1425-1436`; current test is `len()==2` at `:1619`). The generalization leaves that true. RC-4's fail-after association exists and fail-before's does not, so the sequence lists are `1,2` and `1`. RC-5's E3 takes sequence 3 because both earlier COMMITs landed. RC-9 links one object because `availability-purged` deletes one file (`:2624-2647`). The normalizer orders rowid-less tables by shape and then normalized content (`post_state.rs:196-205`, `:225-282`), which is what makes RC-9's mixed confirm/create child repeatable under r14.

## The 19 runs

Standing reads R's current availability and whether any Run-material row names R (X3C:114-120). It does not read attempt phase, receipts, or associations. `apply_x93` (`:2488-2657`) matches the table: only `run-material-inventory` changes material; nothing in the 19 deletes R's availability or material row. `availability-purged` inserts generation 1 and leaves generation 0, which 6a.4 still treats as a re-commit. `next_commit_sequence` (`ledger_store.rs:732-753`) returns 1 when the association table has no row, so rows 3 and 18 take sequence 1; body rewrites leave the key column, so those E3s take sequence 2. Neither sequence is scored.

The sweep decides per ExecutionId from that attempt's receipt, association, and attempt row (`sweep_settle.rs:211-259`). F23's scored `R3` / `R3.left` (`nothing` / `one-sided`) are the crashed attempt's decision. R2's settlement is `R3.others` (`commit_tests.rs:1574-1583`), and no expected value in either file contains `next-writer`, `R2`, `second`, or `Refused(Invariant)`. Host F01's two substituted rows use `HOST.INVARIANT_VIOLATED` at `finalize1`, with `attemptRows` 0. Of the 19, 18 are X9-2 form and capture before the ladder (`:1730`); F49 is the step-form run and captures after `second` (`:2137-2147`). The 17 X9-2-form runs whose outcomes change therefore keep `normalizedSha256`. F49's does not. Trace digests of the next writer and later ladder children are unscored. Nothing is re-transcribed. LD-RC-7 matches X3C:310 and frame rule 2.

Rows that stay first commits are the ones 6a.2 names: F24's admitted digest holds no per-Run row, F36 leaves none, F04 `kill-link-after-1-unequal-collision` refuses at the object, and every `r2: distinct` R2 commits another RunId (X9:262-264).

## Lead set and RC.7

RC.6 is X3C:260-261: census-only and `coverage`, then transcription, then development runs, then two serialized repetitions of 403 storage rows and 98 host rows. `check` requires full union coverage and reports `killedOutsideKillSet` without failing on it. The 5,000 ms guard is X9:391. Kept-state on a kill is new; F30 and F34 finish their `unchanged` children and no existing row kills one, so no scored value moves. The release-order check (`:620-624`, X9:753-769) already applies to every commit child; a re-commit uses the same journal and level-3/4/lease/fence steps (X3C:262). `"X3c-3"` in `UNIT_VALUES` does not change an existing row. No new crash point, scope, kind, label, run-record member, or limit.

## Accepted outcomes

Existing expected values of both required-runs files stay. The 18 outcome changes are the unscored record X3c r8 already decided. The line 268 note records that decision and leaves the distinct variant where r12 and r13 put it. No accepted outcome of another law changes.
