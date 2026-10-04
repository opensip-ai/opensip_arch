CODEX2 re-review: law X4 r8, round 2. It follows your round-1 review (`reviews/codex2-x4-r8`; REQUIRED-FINDINGS, RF-X4R8-1 and NB-X4R8-1). r8 is still J1's successor **S11**, the gate word.

This is a **law review**. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-x4-r8-round2.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- No product builds or test runs. Timing-sensitive lanes may be using this machine. Do not run any lead set.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## What is asked

**The lead's decision.** RF-X4R8-1 found that round 1 left X4a's existing first-cause races (D8-1) as an ungated follow-up. The lead's response:
- **One rule.** D8-1's fix is folded into this revision as round 2, and the first-cause rule is made total.
- **Same name.** The revision keeps the name "X4 r8", because J1, X3d r9, M3-L r5 and M3-PLAN r9 cite it for S11.
- **No separate law.** The separate X4-F3 law route is dropped. X4-F3 is now a code unit under this law, gated before J3b.

**The questions:**
1. Is RF-X4R8-1 closed? Is NB-X4R8-1 addressed?
2. Is round 2's first-cause rule total and sound? Is it still exactly what J1 r5 and X3d r9 assume?
3. Does round 2 change any accepted outcome of X4 r7 or of another law, apart from S11's declared changes? Any changed `REV` reason, row, outcome, permit or gate state is a finding, and so is a reason or row changed "as an exception". Round 2 claims none.
4. Is anything else wrong?

Round 1's word, masked loops, bounds, never-reset rule, one-permit argument, LD8-1, LD8-2, LD8-4 (for the cancellation latch) and LD8-5 passed. They are unchanged in substance, so recheck them only where round 2 touches them.

## Pins

The pins are in `hashes.txt`. Apart from the subject and this request, every pin is an accepted snapshot, the round-1 snapshot, or a review record.
- **The subject:** `docs/implementation/m2/live-guards-x4/PROPOSAL.md`, X4 r8 round 2. It is the subject of `subjectSha256`.
- **The diff base: `live-guards-x4/PROPOSAL-r8-round1.md`** (`ee758471…`, 59,840 bytes). These are the exact round-1 bytes you reviewed, your round-1 subject. Diff PROPOSAL-r8-round1.md against PROPOSAL.md.
- **The accepted predecessor,** for checking that r7 is preserved: `live-guards-x4/PROPOSAL-r7.md` (`fc8490f4…`, = `reviews/grok-live-guards-x4-r7/review.json`'s `subjectSha256`). Against it, round 2 still changes only the title and the history line's 35-byte acceptance note.
- **Your round-1 review:** `reviews/codex2-x4-r8/review.json`, the copy in arch.
- **Sources and consumers** (accepted snapshots):
  - **J1 r5:** `m3/host-pipeline-j/PROPOSAL-r5.md` (`4ccb2320…`). It is cited for 8.1, 8.3's last paragraph (J1:598), 8.6, the S11 row, J-C15 and J-C15b (J1:684-691) and J3b.
  - **X3d r9:** `m2/commit-session-x3d/PROPOSAL-r9.md` (`c727001a…`, = `reviews/grok2-x3d-r9/review.json`'s `subjectSha256`). It is cited for S10.2 to S10.5, S10.8 and S10.9, LD9-3 to LD9-5, and S10.11.
  - **X7 r7, now accepted:** `m2/finalization-x7/PROPOSAL-r7.md` (`7757935c…`, = `reviews/codex2-x7-r7/review.json`'s `subjectSha256`; GROK2, directory name kept). It is cited in S11.12 only.
  - **M3-L r5,** accepted in review: `m3/provider-protocol-l/PROPOSAL-r5.md` (`f654ee4e…`), items 16f and 18.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `cca4fe4`, read-only. Main is now `d2c00a9`, and none of the cited files changed. Neither X4-F3 nor J3b is integrated. The cited lines:
  - `crates/security/src/custody/operation_guard.rs` ("og"):
    - `:96-131`, `StopCause`, its `row()` and `GuardRefusal`;
    - `:199-226`, `Shared.cause`, `record`, `latched()` and `lock()`;
    - `:255-262`, the observer;
    - `:372-406`, the guard's creation;
    - `:419-421`, `OperationGuard::stop`;
    - `:457`, `hold_monitor`;
    - `:512-518`, `admit`'s refusal;
    - `:536-575`, the checkpoint: the trailing `stop` closure and source 7 at `:538-543`, the stale path at `:547-549`, step 3 at `:563-566`, and the boundary check at `:570-574`.
  - `crates/security/src/revocation.rs` ("rv"):
    - `:84-91`, `StopOnUnwind`;
    - `:121-153`, the read: `AlreadyStopped` at `:126-127`, and the failure latch at `:149-151`;
    - `:159-193`, the boundary check: `AlreadyStopped` at `:163-165` and `:184-186`, and the latch at `:189-191`.
  - `crates/security/src/custody/commit_session.rs` ("cs"):
    - `:94-101`, `RevReason::of`, where `None` gives `operation-stopped` at `:100`;
    - `:529-531`, `refused()`;
    - `:553-569`, `refuse()`, with the latch at `:562`;
    - `:572-587`, `open`'s refusal, with the latch at `:577`;
    - `:985-1014`, `publish`'s refusal arm, with the latch at `:986` and `SealStep::Guard` at `:996-998`.
  - `crates/security/src/commit_authority.rs:40-44`, the existing latch and its crash point.

## The shape of the diff (round 1 to round 2)

- **The r8 header.**
  - The "What it changes" bullets list the two stop causes, the stop transition and the X4-F3 unit.
  - Rows 8 to 11 of the "r8 changes" table are revised. Row 11 was D8-1 "disclosed, not decided", and is now the total rule.
  - A new "Round 2" paragraph and a "Round 2 changes" table, R2-1 to R2-9 (`:67-90`), come before "## Problem".
- **The notes** on items 7, 8, 10 and 11 each gain a round-2 sentence.
- **S11.2 and S11.5.** The existing latch runs inside its source's stop transition.
- **S11.6 is rewritten** (`:360-448`). It contains:
  - rule FC;
  - the stop transition, in six steps;
  - invariant I1;
  - the readers;
  - the placeholder's withdrawal;
  - a table of all nine sources, with today's product lines, each source's cause, and its unit;
  - trailing latches, the boundary check's `AlreadyStopped`, and lock order;
  - what each cause maps to;
  - the four cancellation results;
  - D8-1's two schedules, as they now run;
  - `StopCause`'s five variants.
- **S11.7.** The crash-point placement.
- **S11.8.** W-5 now names all four readers. W-6 becomes the matrix of every ordered pair of sources. New: W-8 (D8-1's schedules and two more), W-9 (the source pin) and W-10 (no new wait).
- **S11.9 is rewritten.** It names X4-F3 (sources 1 to 8, including X3d's call sites and `RevReason::of`'s arm) and X4's part of J3b (source 9), and states the gate (LD8-9).
- **S11.10.**
  - LD8-3 gains a round-2 sentence.
  - LD8-4 gains the existing sources' placement.
  - New: LD8-6 (one stop transition for every source), LD8-7 (`CertainRefusal`), LD8-8 (the placeholder's withdrawal) and LD8-9 (X4-F3, gated before J3b).
- **S11.11 and S11.12.**
  - S11.11 is now "D8-1, resolved in round 2".
  - S11.12 adds a third X3d record note (`CertainRefusal` through `OperationGuard::stop`, mapped to `operation-stopped`) and an X9 r17 record note (`x4.gate.latch.after` follows the release). X7 r7 is cited as accepted.
- **Forbidden substitutes and Not claimed.** A new group, "The first stop (r8 round 2, S11.6)". "Not claimed" drops round 1's "D8-1's fix (X4-F3)".

## The first-cause rule, as round 2 states it (S11.6)

- **FC.** An operation has exactly one first stop: the source whose transition first sets `LATCHED`. Its cause is recorded in the same critical section as that transition and is never replaced. Every later source records nothing. Every reader, and `finish`, gets that cause.
- **The stop transition.** After the guard's creation, every latch is a stop transition:
  1. take the stop-cause lock;
  2. make the source's transition: `fetch_or(LATCHED)`, or the cancellation loop;
  3. record the cause if, and only if, that transition set `LATCHED`;
  4. read the recorded cause;
  5. release the lock;
  6. fire `x4.gate.latch.after` outside the lock.

  The section holds no I/O, wait, callback or crash point, and never spans a monitor read.
- **I1.** Outside the lock, `LATCHED` is set if, and only if, the first stop's cause is recorded.
- **The cause-less sources record `StopCause::CertainRefusal`.** These are X3d's certain refusals, through `OperationGuard::stop`, and the checkpoint's lock mismatch. It maps to `REV(operation-stopped)`, today's reason. Its `row()` is the invariant row, which no checkpoint reaches.
- **The placeholder record is withdrawn.** `latched()` reads only. On a breach of I1 it returns `GuardRefusal::Invariant` and records nothing.

## Decide

1. **RF-X4R8-1.**
   - **Both counterexamples.** Under S11.6, do both now end with the earlier cause's row and `REV` reason?
     - a certain refusal, then an observer tick, then a signal after the close, then `finish`;
     - a stale guard, then a cancellation that gets `AlreadyStopped`, then an observer tick, then the checkpoint's return.
   - **Every result.** Does the first cause survive each cancellation result: `BeforeAdmission`, `AfterAdmission`, `AlreadyStopped`, and `OutsideWindow` both before the window opens and after it closes?
   - **The landing gate.** Is LD8-9's gate, with X4-F3 before J3b or in its commit, the required acceptance and integration dependency?
2. **Totality.**
   - **Completeness.** Is S11.6's table of nine sources complete for every latch of an operation's gate after the guard's creation? Check it against og, rv and cs, including the trailing `stop` closure, `lock()`'s poisoned path, `StopOnUnwind`, and the boundary check's own failure and its `AlreadyStopped`.
   - **The invariant.** Does I1 hold at the guard's creation and under every transition?
   - **The readers.** Does every reader find the first cause?
3. **`CertainRefusal` (LD8-7).**
   - Does it keep X3d's `REV(operation-stopped)` and every row?
   - Is its invariant `row()` unreachable, as S11.6 argues?
   - Does recording it change anything else that reads `cause()`? `finish`'s `latched || revoked` test is at cs:1106-1116.
   - Is a code change in X3d's `commit_session.rs` under X4 r8, which changes no outcome, acceptable as X4-F3 scope, with a record note for X3d's next revision? Or does it need X3d's own revision?
4. **The placeholder's withdrawal (LD8-8).** Is a pure read, with `GuardRefusal::Invariant` and no record on a breach, right? Is keeping `latched` as the subject of sources 4 and 5 right?
5. **Lock order and waits.**
   - Is monitor-then-cause still the only order?
   - Is the lock never held across a monitor read? This answers your round-1 fix note, "do not … expand the cancellation lock across monitor I/O".
   - Is it true that no successful admission takes the lock?
   - Does moving the monitor's failure, boundary and unwind latches through the operation's stop handle keep item 2's and item 5's monitor rules?
6. **The crash point (LD8-4, round 2).** For the existing sources, `x4.gate.latch.after` moves from straight after the `fetch_or` to after the release, on the same calls and in the same order. Is that acceptable as an X9 r17 record note, with X4-F3's lead-set rerun as the check (S11.12)?
7. **NB-X4R8-1 and the controls.**
   - Does W-5 now name all four readers, including both boundary paths?
   - Do W-6's ordered pairs, W-8's schedules, W-9's source pin and W-10 cover every pair of sources? Do they cover `AlreadyStopped` and a closed window preserving the first cause's row and reason? Do they cover each new lead decision?
   - Are the seams outside the critical section?
8. **Units (LD8-9).** Is X4-F3's scope (sources 1 to 8) and J3b's (source 9) the right split? Is X4-F3 as a code unit under this law, with no separate law, acceptable?
9. **Preservation.**
   - Against PROPOSAL-r7.md, does every r7 sentence still survive verbatim, apart from the title and the acceptance note?
   - Apart from S11's declared changes, does any accepted outcome of X4 r7, X3d r9, J1 r5 or X7 r7 change?
10. **Anything else wrong.**

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with an id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"priorFindings"`: RF-X4R8-1 and NB-X4R8-1, each closed or open, with a reason;
- `"noAcceptedOutcomeChanged"`: true or false, judged apart from S11's declared changes;
- `"subjectSha256"`: PROPOSAL.md's sha256;
- `"preservedSnapshot"`: PROPOSAL-r7.md's path, bytes and sha256;
- `"diffBase"`: PROPOSAL-r8-round1.md's path, bytes and sha256.

Do not commit.
