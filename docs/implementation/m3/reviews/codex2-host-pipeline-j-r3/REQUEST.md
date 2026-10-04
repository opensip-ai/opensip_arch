CODEX2 review: M3-J1 r3, the guarded durable host pipeline. This is a **law and method-soundness** review, round 3. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-host-pipeline-j-r3.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs, and no lead set.
- Never touch the real home.
- Never read the 413 fixture.
- If you compute digests, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`. The subject file is untracked in arch until acceptance.
- `docs/implementation/m3/host-pipeline-j/PROPOSAL.md`, law M3-J1 r3. It is the subject of `subjectSha256`.
- `docs/implementation/m3/host-pipeline-j/PROPOSAL-r2.md` holds the r2 bytes you reviewed (`f7efb87a…`), for diffing.

**Your r2 review** is at `/tmp/opensip-implementation/reviews/codex2-host-pipeline-j-r2/` (REQUIRED-FINDINGS: J1-R2-01 to -03 required, J1-R2-NB-01 non-blocking). r3's "r3 changes and review responses" table maps each finding to its change. You closed every r1 finding in r2 except as those three state, and r3 changes nothing else of substance.

**The records** are as in r2: M3-PLAN r6, M3-C r5, X12 r4 and X2 r9 by their accepted bytes; S-OP-2 by its r4 bytes; M3-L r1 draft; M2 complete. The product is `/Users/sb/code/opensip-ai/opensip` at main `3e64266`, read-only.

## The r3 answers to check

1. **J1-R2-01 (8.1, 8.6, S10, S11, J-C15, J-C15b).**
   - `Ok(PreparedCommit)` leaves the window open.
   - `WINDOW_CLOSED` is set only in the step that produces the operation's `StoppedSession`. Those steps are `prepare_commit`'s four error returns, `publish`'s three returns (the successful `latchedAfterAdmission` sample included), and `refused()` and `undetermined()`.
   - The compare-exchange loops carry the window bits through and change only the state bits.
   - J-C15b cancels during `publish` after a successful preparation.
2. **J1-R2-02 (8.2's phase O, 8.4, 8.6, S18, matrix rows 43 and 44, J-C14b).** A renderer failure in O, before any byte, takes:
   - F16 with the runId, when a `PublishedCommit` exists;
   - otherwise WS:1377's no-Run row 44, under WS:233-240's aggregate.

   An uncertain step 0 keeps its ExecutionId disclosure. A write failure after the first byte ends exit 4 with no replacement. An unrenderable failure envelope ends exit 4 with the one coded line.
3. **J1-R2-03 (5.3, item 6, 8.2, 8.4, S18, J2c, J3d, J-C14c).** One common rule for both paths.
   - **Before S18:** no output path that uses phase O is wired, durable or ephemeral, and WS:224-228 stands. The ephemeral rule is phase A only.
   - **After S18:** A (with D only where a Run committed), the output decision point, O, then E, for both paths. J2c's output wiring is gated on S18 as J3d's is.
4. **J1-R2-NB-01 (8.2's phase O, S12-O, S18).** "Recorded with arrival phase O" now means:
   - an in-memory classification by the host cancellation source;
   - a SOP2 event, attempted with a `CancelPhase` member `O` by ordinary registration (SOP2:205-208);
   - post-freeze loss (SOP2:663).

   No sink is reopened, and no persisted record is required.

## Decide

1. Does each answer close its finding without opening a new defect?
2. **The close rule.** Is it total over every terminal outcome and empty over every continuing one? That includes A-phase sessions ended by `refused()` and a `PreparedCommit` dropped by a panic. Does it still give phases B and C their full span inside `publish` (X3D:141-172)?
3. **Row 44 under WS:233-240's aggregate.** Is it routed correctly when step 0 also failed? Is keeping an uncertain step 0's ExecutionId through WS:1409-1411's composition lawful?
4. **The S18 gate.** Is it now consistent across 5.3, item 6, 8.2, 8.4, S18 and item 14, with no wired path left under two dispositions?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256, as one string.

This is a law review, not a `verify_design` unit. J-BS, S18 and the inventory units J2a to J3d each need reviews of their own; a contract successor's verdict must be `ACCEPT-DESIGN-UNIT`. Do not commit.
