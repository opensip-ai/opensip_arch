Grok review: law X9 r13, an amendment found by X9-5's development runs, plus the timing guard's limit from X9-3's measurements. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT**.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r13.
- This is a law review with no product cargo. Run git read-only, against product main `b999ae3`. The X9-5 worktree `/Users/sb/code/opensip-ai/opensip-x9-5` is uncommitted and may be read.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## What changed

Pins are in hashes.txt. `crash-matrix-x9/PROPOSAL-r12.md` is the accepted r12: 123524 bytes, `34107576…`, equal to the r12 review's subject. Diff PROPOSAL.md against it. The current file also carries r12's existing "r12 ACCEPTED" stamp.

r13 makes lead decisions under the owner's standing direction. These are the changes:

1. **Record: the `candidate` child's refused end appends the latched gate's one REV** (X3d item 7 step 1; X8 r5's B1, B2 and B4).
   - Every host row starts from INIT and that REV.
   - r10's "no attempt row, SEAL or object" holds unchanged.
2. **F01's two kinds of variant are told apart.**
   - **Replay-refused variants:** the whole post-state is unchanged.
   - **Substituted variants (B1 and B2):** no ledger, no attempt row, no SEAL, and the carrier gains exactly the latched gate's one REV.
   - **Dev evidence:** the carrier was `[REV, REV]`, and everything else matched.
3. **F40's latch variant runs landed only.**
   - It uses r12's F39 hold at `x3c.evidence.commit.before#1`, with `fail-after` at `.after`.
   - The not-landed latch variant is covered by F40 without the latch and by X4's gate-trace test.
4. **R2 commits r12's distinct variant after a committed Run.** That covers F12 landed, F16, F17, F39, F40's landed variants and F32 `…987`.
   - R2 is expected to be Committed where no revocation stands.
   - R2 is refused at admission (C5, unscored) for F39 and F40's latch variant.
   - **Dev evidence:** with the same candidate, R2 was `Refused(Invariant)`, which is r12's F13 finding.
5. **Record:** the host's publisher revokes the `candidate` session's `core_closure`, which is r12's subject.
6. **F32 `…987`: R1 and R4 are `unknown-quarantine-condition:journalContiguity`.**
   - **Basis:**
     - The owner's §2 requires "sequence contiguity `1..t`", and X6's capture enforces it as count == tail (`recovery_capture.rs`).
     - The reserved-slot technique plants one RA at `…987` above only the seq-1 REV.
     - The writer's start reads only the tail, witness and floor (X3b item 9), so it commits.
   - **Scope:** this is a fixture property, and it is a quarantine, never a negative. The `…988` rows never capture the carrier.
7. **The timing guard's `limitMs` is 5,000** (r12 header and item 11, in place).
   - **Measurements:** X9-3 measured F44 at 2,845 ms and F45 at 2,893 ms, from lawful writer work only.
   - **Why 5,000:** it is half of X4's 10 s freshness bound, and about 1.7× the measured values.
   - **Rejected:**
     - narrowing the window to the main thread's held time;
     - keeping 2,000 ms;
     - a limit near 10 s.
   - **Code changes owned by X9-3:** the checker's limit, its test, and the run record's constant.

In-place r13 notes are added to:
- the r12 timing-guard sentence and item 11;
- the F01, F32 and F40 cells;
- item 12's X9-5 line.

The title is now r13.

**X9-5's own calls,** which are not law:
- the F32 transcription read X3b item 4a case 2 (OPEN, not ADVANCE) literally;
- the substituted-target candidate retains the closure's blobs;
- F01 and F53 run no ladder;
- the publication is made by a publisher child under the scripted clock;
- R1 for F16, F17 and F39 is `committed-historically:*`.

These go to the X9-5 unit review.

## Decide

- Is each change the owning law's outcome, recorded or decided correctly?
- Is 5,000 ms a sound limit that still keeps every run well inside X4's freshness bound?
- Does r13 change nothing else? Is anything else wrong?

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict";
- "requiredFindings";
- "noAcceptedOutcomeChanged";
- "subjectSha256";
- "subject" (path, bytes, sha256);
- "preservedSnapshot": the accepted r12, `PROPOSAL-r12.md`, 123524 bytes, `34107576…`.

Do not commit.
