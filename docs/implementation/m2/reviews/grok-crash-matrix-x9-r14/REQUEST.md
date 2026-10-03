Grok review: law X9 r14, an amendment found by X9-3's two lead run sets. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT**.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r14.
- This is a law review with no product cargo. Run git read-only, against product main `b999ae3`. The X9-3 worktree `/Users/sb/code/opensip-ai/opensip-x9-3` is uncommitted and may be read, including its lead sets `target/opensip-x9/x93-lead-1` and `x93-lead-2` (these predate the prototype fixes).
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- If you run anything, use a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`.

## What changed

Pins are in hashes.txt. `crash-matrix-x9/PROPOSAL-r13.md` is the accepted r13: 134335 bytes, `f373415e…`, equal to the r13 review's subject. Diff PROPOSAL.md against it. The current file also carries r13's "r13 ACCEPTED" stamp.

Both lead sets passed all 57 X9-3 rows, but `check-unit` refused: seven runs disagreed between the sets. There were three causes. r14 makes these lead decisions under the owner's standing direction:

1. **The object-publication group order (extends r8's trace rule).**
   - **The problem:** X3c publishes in content-digest order, and digests derive from drawn values. A next writer that confirms some objects and creates others therefore interleaves the two branches in a drawn permutation. This hit F13, F14, F15, F25 `object-deleted` and F52 `purged`; only the trace digest differed.
   - **The rule:**
     - each thread's consecutive `x3c.object/` records are split into groups at `create.before`;
     - the groups are stably sorted by their records without occurrence numbers;
     - each name's occurrences are reassigned in ascending order.
   - **Lawful first commits are unchanged.** Their groups are all alike, and the census files are byte-identical with and without the rule.
   - **Consequence:** X9-2's F02–F05 trace digests change, but their `normalizedSha256` does not, and X9-2's acceptance stands.
2. **F25 runs R1 only, in both variants.**
   - After `object-flipped`, R2 refuses at a drawn position (1,115 against 1,141 records), so no ordering can make it agree.
   - R2 is not part of F25's row, and it re-commits the same Run, which is X3d-2's limit.
   - **Rejected:**
     - leaving R2's child out of the comparison;
     - committing R2 with the distinct variant.
3. **Record:** F49(a) has two tied `admitted` rows in a table keyed without rowid. That is fixed in X9-3's post-state normalizer as the unit's judgment call, like X9-2's call 7. It is not law.

In-place r14 notes are added to:
- r8's trace-digest bullet;
- item 7's two repetition bullets;
- the F25 cell;
- item 8's mutation-row exception;
- item 12's X9-3 line.

The title is now r14.

## Decide

- Is the group rule exact and sound?
  - Does it make lawful repetitions agree without hiding a real difference, such as the number of objects published?
  - Is it correct that every run whose groups are all alike is unchanged?
- Is F25 R1-only right? Is the F49 tie-break properly left to the unit?
- Does r14 change nothing else? Is anything else wrong?

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict";
- "requiredFindings";
- "noAcceptedOutcomeChanged";
- "subjectSha256";
- "subject" (path, bytes, sha256);
- "preservedSnapshot": the accepted r13, `PROPOSAL-r13.md`, 134335 bytes, `f373415e…`.

Do not commit.
