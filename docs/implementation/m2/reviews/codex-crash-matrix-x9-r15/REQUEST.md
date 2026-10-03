Codex review: law X9 r15, an amendment found while preparing unit X9-4 (locks and live revocation). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT**.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/codex-crash-matrix-x9-r15.
- This is a law review with no product cargo. Run git read-only, against product main `b999ae3`.
- These uncommitted worktrees may be read:
  - X9-4: `/Users/sb/code/opensip-ai/opensip-x9-4`. X9-3's diff is staged as the base, and X9-4's harness changes sit unstaged on top.
  - X9-3: `/Users/sb/code/opensip-ai/opensip-x9-3`.
- **Do not run the crash matrix, lead sets or full test lanes.** Another unit's timing-sensitive lead sets are running on this machine. Reading code is enough.
- If you must run something small, use a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Background

The law is `crash-matrix-x9/PROPOSAL.md`, the crash, lock and revocation matrix that gates M2. Grok reviewed r1 to r14 and accepted each. `crash-matrix-x9/PROPOSAL-r14.md` is the accepted r14: 145042 bytes, `f2800ff9…`, equal to `reviews/grok-crash-matrix-x9-r14/review.json`'s subjectSha256. Diff PROPOSAL.md against it. The current file also carries r14's "r14 ACCEPTED" stamp. Every earlier header records how the law got here.

## What r15 changes

r15 makes lead decisions under the owner's standing direction. They come from reading code, not from runs; the header says so. Each item in the r15 header gives its file:line evidence and the alternatives it rejects:
1. X9-4's census gains an unarmed refused-end commit run, so X9-4's REV-append kill points are reachable.
2. A required run may carry an optional `unit` member. `check-unit` honours it and `check` admits it. Only F14's moved `x3d.finish.settle.before` row carries it (`"X9-4"`).
3. The moved F14 row's R2 is refused at admission (C5) and not scored, as r13 has for F39.
4. The timing guard's window ends at the writer's first hold other than the observer tick. F18 and F19 resume the held tick after `x3d.finish.settle.before#1`.
5. F30:
   - the second B commits the distinct variant;
   - in (a), "no state change" compares the project's own state, and B's lawful trust-floor publication is recorded;
   - in (b), the sweep is refused busy at its own admission (X6 r4 item 7 step 1).
6. F18's mixed view is covered elsewhere, by a named X4a test. The unreadable view is `state.v1` at mode 000.
7. F26's "no grant reused" is R2 refused at admission, with the project's own state unchanged.
8. F34's run A: the ledger is unchanged and no SEAL is added. The carrier's one latched REV (r13) is unscored.
9. A list of X9-4 judgment calls, recorded and not law.

There are 11 in-place r15 notes, and the title is now r15.

## Decide

- Is each item the owning law's outcome, and does the cited code support it?
- Is each lead decision sound against its rejected alternatives?
- Does the `unit` member reintroduce the unit tag r10 rejected, or is it narrow enough?
- Does r15 change nothing else? Is anything else wrong?

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict": ACCEPT or REQUIRED-FINDINGS;
- "requiredFindings";
- "noAcceptedOutcomeChanged";
- "subjectSha256";
- "subject" (path, bytes, sha256);
- "preservedSnapshot": the accepted r14, `PROPOSAL-r14.md`, 145042 bytes, `f2800ff9…`.

Do not commit.
