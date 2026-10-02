Grok review: law X9 r6, which answers your X9 r5 RF-1. Claude Opus 5.5 leads. You are the single reviewer.

**Rules.**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r6.
- This is a law review with no product cargo. Run git only read-only, against product `a36da7c`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## What changed

The pins are in hashes.txt. `crash-matrix-x9/PROPOSAL-r5.md` holds the r5 bytes you reviewed (82189 bytes, `729aa05e…`). Diff PROPOSAL.md against it. r5 was not accepted, so r6 corrects its F00 text in place. The changes are only these:

- **Title:** r5 becomes r6.
- **r5 header:** an r6 note is inserted after "r4 bytes are preserved in PROPOSAL-r4.md." It names RF-1 and the fix, and cites `write_schema` (`project_ledger.rs` lines 500–502: the barrier follows a successful `COMMIT`).
- **The F00 split in the r5 header, now:**
  - **UC window:** from the draw through `x3c.ledger-create.ddl.commit.before`, that point included. R1 is UC with reason `ledger-missing` or `ledger-unreadable`, whichever the kill left. R4 is UAU.
  - **UAU window:** from `x3c.ledger-create.ddl.commit.after`, that point included, until `x3c.attempt.commit.after`. R1 and R4 are both UAU.
- **The F00 cell's r5 clause:** the same split.

Unchanged:
- R3 still writes nothing.
- The rest of the F00 row stays as it was.
- The pre-draw bucket (n/a) stays.
- The undecided gap after `x3c.ledger-create.wal` and before `ddl.commit` stays undecided.
- Decisions 1 (F07 to F10) and 3 (the synthetic run candidate) are byte-identical to r5.
- The two wide line citations you noted for decisions 1 and 2 are not touched, since the request was for this fix only. They don't affect the expectation.

## Decide

- Does r6 resolve RF-1 exactly as required?
- Does it change nothing else in r5?
- Is anything else wrong?

Write REVIEW.md and review.json under the output directory. review.json contains:
- "verdict";
- "requiredFindings";
- "noAcceptedOutcomeChanged" (true: nothing beyond r5's three decisions, as corrected);
- "subjectSha256";
- "subject" (path, bytes, sha256);
- "preservedSnapshot": the accepted r4, `PROPOSAL-r4.md`, 74438 bytes, `4b387bbd…`.

Do not commit.
