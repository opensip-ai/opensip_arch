Grok review: law X9 r8, an amendment. Claude Opus 5.5 leads. You are the single reviewer.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r8.
- This is a law review with no product cargo. Run git only read-only.
- Product facts are pinned at product `a2c5e8b` (`/Users/sb/code/opensip-ai/opensip`; use `git show a2c5e8b:<path>`).
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Why

X9-2 built its matrix target and ran every one of its 232 transcribed rows once, as a development run on `a2c5e8b`. That build is uncommitted and is not under review here.
- **Result:** 167 PASS, 65 FAIL, 0 HARNESS-ERROR.
- **The failures:** each one was the owning law's lawful outcome for the crash state at the kill point, where X9 r7's row expected a different outcome.
- **Decision:** the coordinator took the fixes as lead decisions and wants them in the law.

The per-run observations are summarized in the r8 header. The lead's development log is not pinned, because its run set is not a review subject.

## Pins

Pins are in hashes.txt.
- **Snapshot:** `crash-matrix-x9/PROPOSAL-r7.md` is X9 r7 byte for byte, without its "r7 ACCEPTED" note (85255 bytes, `913523…`). That equals `reviews/grok-evaluator-closure-x3d-r8/x9/review.json` subjectSha256. The snapshot already existed and was checked, not rewritten.
- **Diff:** diff PROPOSAL.md against it. Every predecessor line survives verbatim. The only exceptions are:
  - the title;
  - the r7 ACCEPTED note, which is already in the working law;
  - r8 text appended to the F00, F07 and F46 cells.

  New text:
  - the r8 header, after the r7 header;
  - L11 in item 10;
  - one r8 sentence on X9-2's unit line.

## What r8 decides

1. **F00's R2 follows the owning law's outcome for the crash state at the kill point.** The expected R2 is transcribed by census window:

   | Window | Expected R2 |
   |---|---|
   | `x2.fence.register.reserved/rename.after` through `x2.fence.register.active/rename.before` (a RESERVED row) | `PROJECT.ROOT_CUSTODY_REFUSED`, subject `identity-recovery-required` (X2 r8 items 3 and 8) |
   | `marker/create.after` (marker not yet private) | subject `marker-custody` |
   | `marker/write.before` (marker private but empty) | subject `identity-contradiction` |
   | `create.after` of the X3c `projects`, `namespace`, `objects` and `sha256` directories, and of the ledger file | X3c's custody row, subject `private` |
   | `x3b.floor.directory/create.after` | X3b's host I/O row |
   | An empty X4T dependency file (`create.after` and `write.before` of `x4t.floor-publication.dependency`) | Committed or `INSTALLATION.INCOMPLETE` |
   | `x3c.ledger-create.wal` and `ddl.commit.before` (the WAL gap) | `LEDGER.CORRUPT` (X3c r7 item 10) |
   | Everywhere else | Committed |

   - **R4:** stays UC wherever R2 doesn't create the ledger.
   - **Unchanged:** R1's r6 split, R3, "no attempt row", and the R2 witness-action set.
   - **Why the X4T dependency points admit either outcome:** whether the next fenced read names that dependency file is X4T r9's reading. X9 doesn't restate it. In the development run, `create.after#1`, `write.before#1` and `write.before#3` gave Incomplete, and `create.after#4`, `create.after#7` and `write.before#6` gave Committed.
2. **F07's R2 witness action** is OK before `x3b.append.seal.witness-pending/rename.after`, and REVERT from that point on. Before the rename, only the temporary file exists, so the start reconciles as consistent. F08 is after the rename, so it is unchanged.
3. **L11 (new).** The states in point 1 that refuse permanently are an M2 known limit, recorded and not tested:
   - an interrupted first registration;
   - a created owner not yet sampled private;
   - a partial ledger WAL.

   No product code is added for them; the later owner is M3, a repair or resume writer. `limits` and the checker carry L1 to L11. EXIT-PLAN already records the limit (arch `a100d85a7`).
4. **Four of X9-2's choices become law:**
   - **Census scope (item 5):** each unit's census is its own drivers' census. X9-2's is the commit driver's lawful first commit, two equal runs. X9-3 owns recovery and sweep, and X9-6 holds the union.
   - **Normalized trace digest (item 7):** records are grouped by thread in each thread's own order, without the pid or the process-wide sequence number, and with drawn payload values numbered by item 7's normalizer.
   - **R3 scoring (item 8):** R3 is scored against the left attempt's ExecutionId. R2's own settle is recorded as `nextWriter`.
   - **F46 (item 9):** the "association below `first_generation`" variant is not executed in M2. A fresh carrier's first generation is 1, and the ledger has `CHECK (grant_generation >= 1)` (`ledger_store.rs`). Only a migrated carrier, which is L5, would have such an association.

Not in r8: X6c's sweep took its `try_lock` locks outside any `x2.lease.*` scope. X9-2 carries that point placement as a unit-level judgment call (EXIT-PLAN `a100d85a7`). It compiles to nothing without the feature, so it changes no law text.

## Decide

- Is each decision sound and narrow?
- Is each consistent with the following?
  - X2 r8 items 3 and 8;
  - X3c r7 items 2 and 10;
  - X3b items 4 and 4a;
  - X4T r9;
  - X9 r7's items 5, 7, 8, 9 and 10.
- Are the windows defined from census positions and point names alone, before any run?
- Do L11 and the four promoted choices change any other accepted outcome?
- Is the r7 snapshot exact, and is every accepted sentence preserved?
- Is anything else wrong?

Write REVIEW.md and review.json under the output directory. review.json must contain:
- "verdict": ACCEPT or REQUIRED-FINDINGS;
- "requiredFindings";
- "noAcceptedOutcomeChanged": true means nothing changed beyond the stated decisions;
- "subjectSha256";
- "subject": path, bytes and sha256;
- "preservedSnapshot": path, bytes and sha256.

Do not commit.
