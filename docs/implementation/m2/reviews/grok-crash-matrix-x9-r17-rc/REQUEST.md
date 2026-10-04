Grok review: law X9 r17, round 1. This round is the r17 header, the section frame and §RC, the re-commit section that X3c r8 assigns to X9 r17. Claude Opus 5.5 leads. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**, on §RC and the r17 frame only.

Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r17-rc.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- **No run of any kind.** No product build, test, census-only step or lead set. This is a law review, and X3c-3's code does not exist yet. A timing-sensitive crash-matrix set may be using this machine.
- Run git read-only. Read the product at main `d2c00a9` with `git show d2c00a9:<path>`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read the private 413 UUID fixture.
- You may write read-only scratch scripts under your review directory, for example to tabulate the X9 evidence at C or the required-runs files.

## Subject and pins

The pins are in `hashes.txt`. The subject is uncommitted in arch until it is accepted. If the live file has moved on when you read it, use the arch commit that assigned this request.
- **The subject:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`, law X9 r17, round 1. Its sha256 is the `subjectSha256`.
- **The diff base:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL-r16.md` (`f08efe95…`, 185,750 bytes). These are the r16 bytes Grok accepted, without the note, and they equal `reviews/grok-crash-matrix-x9-r16/status.json`'s `subjectSha256`. Diff PROPOSAL-r16.md against PROPOSAL.md. The live file also carries r16's "ACCEPTED" stamp on line 641; r17 keeps it.
- **The owning law:** X3c r8, accepted by GROK2 (`m2/ledger-blob-x3c/PROPOSAL-r8.md`, `ba638efb…`; `reviews/grok2-ledger-blob-x3c-r8`):
  - item 13's X3c-3 and its matrix duty (X3C:252-261);
  - item 14's windows, RC-1 to RC-9, the census child and the 19-run record (X3C:262-325);
  - CL-2 (X3C:354).
- **The plan:** M3-PLAN r9's "X9 r17 record" row (`m3/M3-PLAN-r9.md:319`): RC before X3c-3, S12 before J3b's review, RW before J4e.
- **The sibling sections, pinned but not reviewed here:** J1 r5 (`m3/host-pipeline-j/PROPOSAL-r5.md`, accepted; item 12 and successor S12, J1:832-841, :858) and J-RW r3 (`m3/resume-repair-jrw/PROPOSAL-r3.md`, in review with Codex; item 10, X-RW-10 and RW-S6, JRW:519-596, :625, :669).
- **The evidence at C = `3d2d5b5`:** `m2/crash-matrix-x9/evidence/3d2d5b5…/` (`storage/census-trace.txt`, `storage/matrix.json`, `host/matrix.json`, `check.json`).
- **The product:** main `d2c00a9`. The key files are `crates/storage/tests/commit_tests.rs` (the harness), storage's and host's `required-runs.v1.json`, `tools/check_crash_matrix.py`, `crates/platform/src/crash_barrier/driver.rs` (`kill_set`), `crates/platform/src/filesystem.rs` (the confirm path, :681-738), `crates/security/src/crash_matrix_support/post_state.rs` (the normalizer) and `crates/storage/src/ledger_store.rs` (`next_commit_sequence`, the DDL). Since C, product main changed `crates/security` (X4-F1, X4-F2) and `crates/storage/src/store_root/native_marker.rs` (X3a-2). It did not change the harness, the checker, `crates/platform` or the ledger store.

## What round 1 changes

Against r16:
- **The title** reads r17.
- **The r17 header** after r16's header. It holds lead decision LD-17-1: r17 is accepted section by section.
  - This round writes the header, the frame and §RC.
  - §S12 and §RW are reserved headings that carry no rows.
  - Later rounds append them to the same r17, each reviewed on its own.
  - Rejected: r17, r18 and r19 as separate revisions, which would make four laws' "X9 r17" citations stale; and waiting for all three, which would block X3c-3 on J-RW and J3b.
- **Six in-place "r17" notes:** r12's re-commit rejection (line 268), and items 5, 7, 8, 9 and 12. Each points to §RC.
- **One forbidden substitute:** a section that changes another section's rows, or re-transcribes a row its owning law does not require.
- **"X9 r17 sections"** after "Not claimed":
  - the section frame (six rules);
  - §RC in full (RC.1 to RC.7);
  - §S12 and §RW as reserved headings.

## What §RC decides

- **Spellings (RC.2).**
  - Every RC row is a `recommit-` variant of the F-case it extends.
  - Rows carry `"units": ["X3c"]` and `"unit": "X3c-3"`, and use the step form.
  - R2 commits the same candidate (`{"r2": "same"}`). `e1-recover` is X3c r8's "recover(E1)".
  - **LD-RC-1:** the case for RC-1 is F15, for RC-2 F04, and for RC-7 F23. RC-4's rows are F12's, and RC-5's are F13, F14 or F15 by kill point.
  - **LD-RC-2:** every row uses the step form.
  - **LD-RC-3:** `"unit": "X3c-3"`, which the checker admits with r16's reading of `"X9-6"`.
  - **LD-RC-4:** `"r2": "same"` is explicit, and any other value than `same` or `distinct` is a `HARNESS-ERROR`.
  - **LD-RC-5:** new observed values, compared only where a row names them.
- **The census part and the kill set (RC.3).**
  - Storage's census gains a fifth part, `recommit`: E2, a lawful re-commit after E1 on its own fresh root, with its checks.
  - **The prediction,** from the code and C's census: two new names, `x3c.object/reopen-confirm.before` and `.after`. `x3c.object/file-barrier.before` and `.after` rise from 82 to 164 occurrences, because a confirmed object takes two file barriers (X9:446). So their selection under r10's union and item 5 moves from `#1, #41, #82` to `#1, #82, #164`.
  - **The totals:** union census 321 to 323 points; union kill set 383 to 389. The part adds 8 kill-set points and removes 2.
  - **LD-RC-6: F03's two `#41` rows stay byte for byte.** They kill census points outside the new selection. `check` lists them in `killedOutsideKillSet` and does not refuse. No `check-unit` subset is affected.
    - Rejected: deleting or moving them; a named exception list in the checker; leaving the part out of the union for shared names.
  - **A stop rule** applies if X3c-3's census-only run differs.
- **The 22 rows (RC.4),** each with its script template, labels and expected values, and the X3c r8 clause each value comes from:
  - RC-1: 1 row;
  - RC-2: 8 rows (the 8 added kill-set points);
  - RC-3: 2;
  - RC-4: 2;
  - RC-5: 4;
  - RC-6: 1;
  - RC-7: 2;
  - RC-8: 1;
  - RC-9: 1.
- **The 19-run record (RC.5).**
  - Each run's child outcome is derived from X3c r8's standing and material rules and from each mutation's code (`commit_tests.rs:2488-2657`). 18 become `Committed(latched=false)`. F33 `run-material-inventory` stays `Refused(Invariant)`.
  - No expected value in either file names those outcomes, so nothing is re-transcribed.
  - What changes is unscored: R3's `nextWriter` in four runs, trace digests, and F49's `normalizedSha256` only.
  - r16's release-order verdict now applies to the 18 children.
  - **LD-RC-7:** the 18 stay unscored.
- **The lead-set duty (RC.6).**
  - Census-only and `coverage` come first, then the transcription, then development runs.
  - Two serialized repetitions of both targets follow: 403 storage rows and 98 host rows, checked by `check`.
  - Whichever of X3c-3 and J4 integrates second reruns both sections' rows.
- **What X3c-3 adds (RC.7):**
  - the rows and the census part;
  - the observed values;
  - R5's generalized one-RunId check;
  - the `r2` guard;
  - two mutations, `delete-availability` and `plant-availability`;
  - `"X3c-3"` in the checker's `UNIT_VALUES`.

## Decide

1. **The frame and LD-17-1.**
   - Is section-by-section acceptance of one revision sound?
   - Do frame rules 1 to 6 keep the sections independent? This covers rule 2's allowance for re-transcription that an owning law requires, rule 3's `unit` rule and rule 6's snapshots.
   - Do §S12 and §RW carry no rows, and do they state their owners and conditions correctly against J1 r5, J-RW r3 and M3-PLAN r9?
2. **Spellings.** Are LD-RC-1 to LD-RC-5 consistent with X9's existing rows and the harness? Check the step form, `meets`, the `unit` reading and the variant grammar.
3. **The census part and the kill set.**
   - Is the `recommit` part's composition right under item 5, r8's census rule and r10's union?
   - Is the predicted effect in RC.3 right? Check the confirm path against `filesystem.rs:681-738` and X9:446, and check whether any other name could rise above the union's count at C.
   - Is LD-RC-6 sound against item 5, item 7, r16's union record (X9:734-741) and the checker's code? Or must F03's `#41` rows be re-transcribed?
4. **The rows.**
   - Does each RC row's expected value follow from X3c r8's text (X3C:277-307) and the owning X9 row, with nothing read back from a run?
   - Are the scripts executable by the step form as written, with RC.7's additions?
   - Does every killed point lie in the r17 kill set?
5. **The 19-run record.**
   - Is each derived outcome right? Check the mutations (`commit_tests.rs:2488-2657`), `next_commit_sequence` (`ledger_store.rs:732-753`), the association DDL and X3c r8 6a.2 and 6a.3.
   - Is it right that no expected value in either required-runs file names them?
   - Is the statement of which digests change right (`commit_tests.rs:1730`, `:2137-2147`)?
6. **The lead-set duty and RC.7.** Are they complete and bounded? Does any addition change an existing row's scored value?
7. **Scope.** Does round 1 change anything in r16 beyond the title, the r17 header, the six notes, the one forbidden substitute and the appended sections? Does it change any accepted outcome of another law?

**Not in scope.** The future contents of §S12 and §RW. X3c r8's own rules, which are accepted. Any product code.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"noAcceptedOutcomeChanged"`;
- `"subjectSha256"`: PROPOSAL.md's sha256;
- `"subject"`: path, bytes and sha256;
- `"preservedSnapshot"`: the accepted r16, `PROPOSAL-r16.md`;
- `"scope"`: `"X9 r17 round 1: header, section frame, §RC"`.

This is a law review, not a unit review. X3c-3, with its transcription of §RC, gets its own review. Do not commit.
