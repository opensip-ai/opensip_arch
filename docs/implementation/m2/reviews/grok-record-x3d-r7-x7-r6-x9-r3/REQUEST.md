Grok review: three record-only law revisions together, X3d r7, X7 r6 and X9 r3. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-record-x3d-r7-x7-r6-x9-r3. This is a law review with no product cargo. Run git only read-only. Never touch the real home (`~/Library/Application Support/OpenSIP` must stay absent), and never read the private 413 UUID fixture.

## What is asked

Each revision records decisions that were already accepted in another law or in a unit review. None of them makes a new decision. The main question, for each law separately: **does any accepted outcome change?** That covers any decision, outcome, row, code, type, lock order, budget, limit or forbidden substitute of the accepted predecessor, and any accepted outcome of another law. A record that goes beyond its source, or misstates it, is a finding.

## Pins

Pins are in hashes.txt. Each accepted predecessor is preserved byte for byte, without its "ACCEPTED" note. Each snapshot's sha256 equals the subjectSha256 of the review that accepted it:
- `commit-session-x3d/PROPOSAL-r6.md` is X3d r6, `4a5011d2…` (`reviews/grok-journal-x3b-r10-commit-session-x3d-r6/x3d/review.json`);
- `finalization-x7/PROPOSAL-r5.md` is X7 r5, `1b49b921…` (`reviews/grok-finalization-x7-r5/review.json`);
- `crash-matrix-x9/PROPOSAL-r2.md` is X9 r2, `b9b254c3…` (`reviews/grok-recovery-x6-r3-x7-r4-x9-r2/x9/review.json`).

All three snapshots already existed. They were checked, not rewritten.

Diff each PROPOSAL.md against its snapshot. Every changed line of the predecessor survives verbatim, with three kinds of exception: the title, an ACCEPTED note that is already in the working law, and a few "rN (record)" insertions. Accepted text is never deleted. Each revision has a header paragraph that says it is record-only. The sentences it touches carry a short "rN (record)" note that points to that header.

## X3d r7 (diff against PROPOSAL-r6.md)

Sources: X8 r3 items 1, 2, 3b, 4b and 4g, and its "Units after the law" line ("X3d r7 (record only)"); X6 r3 items 2 and 6; the X3d-2 review, calls 1, 8 and 12; EXIT-PLAN, "X3d-2 ordering and follow-ups (2026-10-03)".
- **Doctests superseded.** Item 11's "pinned by `compile_fail` doctests" and item 13's "the X8 doctests" are superseded by X8's fixture lane (X8a's driver in `admission_tests.rs`, inside `--workspace --all-targets`).
- **The adapter source pin (X8 r3 item 3b).** Group H covers the facade's arity. A source pin confines `CommitAdapter`, `StagedCommit`, `begin_journal_txn` and `seal_under_append_lock` to security's `custody/commit_session.rs` and `lib.rs` and to storage's `commit.rs`. These are the names and files X3d-2 call 12 accepted. Item 1's adapter bullet carries a pointer.
- **The fixture source.** Item 12's cross-crate fixtures come through `scenario-fixtures` (ordinary lane) or `crash-matrix` (matrix). Both reach X8 r3 item 4b's one shared site list under the joint predicate. The forbidden production seam stands.
- **The ordering.** X3d-2 integrated before X8b and X9-1. End-to-end composition with a real `CommitSession` is first tested by X8c B0–B4 (X3d-2 call 1; EXIT-PLAN lead decision).
  - X8 r3's unit-list sentence that X8b "lands before X3d-2" is noted as overtaken. **X8 is not amended here.** Please say whether X8 needs its own record.
- **`ExistingAttempt`.** X6 r3 item 6 superseded "before X6 exists" in item 3 step 5 and item 9. The invariant row is permanent in the writer's invocation, and the variant carries `requested` (X6 r3 item 2).
- **Known limit, follow-up for an X3c successor.** Re-committing the same Run in the same (S, N) is refused at staging, because X3c-2 stages availability unconditionally (X3d-2 call 8).

## X7 r6 (diff against PROPOSAL-r5.md)

Sources: the X7a review, calls 4, 5 and 16; the X7b review, calls 1 to 3, 7, 10 and 14. Call 14 asks for exactly this record. EXIT-PLAN, "X7 follow-ups (2026-10-04)".
- **The rollover runs inside `finish`.** `finish` carries `Exhausted` into X2e's `ProjectOperation::end`, where X3b-4's rollover runs. Item 11's "with no rollover" means X7a adds none of the route of its own. Item 11's X7b sentence is marked as history.
- **The `SessionEnd` accessors and `RolloverDisclosure`.** `end_step_failure()` and `rollover()`, with their `None` cases. The five variants, including `AlreadyRolled` (call 2). The type is not an authority type and owes no X8 row. `Undetermined` gets no `recover` remedy, because the rollover's `op-` token is not an ExecutionId (call 7). The exhausted attempt stays on item 6a's busy row.
- **Session-level tests deferred.** They need a `ProjectOperation` in a host test (X9 gap G1), so they land with X8c or X9-5, or as an X7a-2 after X9-1. The record lists what X7a and X7b test now.

## X9 r3 (diff against PROPOSAL-r2.md)

Sources: the X6c review, call 1; X8 r3 item 4b ("Wording change to X9 r1 (record only)"); the X6a r2, X6b and X4a reviews; the X3d-2, X6b, X7a and X7b reviews on G1; the X9-1 review request (pending), "Disclosed gap for X9-2 and X9-6"; EXIT-PLAN, "G5 decided in X6c (2026-10-04)".
- **G5, from X6c.** A revoked closure subject does not refuse the sweep. So the F18, F19 and F38 ladders run R3 to `refused` and R4 to `terminal-not-committed`, and no longer stop at `"ladderEnd": "G5"`. C5 is annotated, and so are X9-4's unit line and the G5 entry. C5's rejection of X9 choosing R3 itself still stands, because X9 transcribes X6c's accepted reading.
- **The joint predicate (X8 r3 item 4b).** Item 6's site sentence reads `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))` for the shared sites. The first forbidden substitute excepts those sites when reached through `scenario-fixtures`, which is still absent from every release build. Crash-matrix-only sites, and `AppendStep`, `ObjectStep` and the ledger commit hook, are unchanged.
- **G1 to G4 status.**
  - **G1 is open.** X9-1 is under review and X8b is not built. X3d-2, X6b, X7a and X7b each deferred their composition tests. X3d r7 and X7 r6 record their test-item lines. X6's waits.
  - **G2 is open.** No law has restated its sentence yet.
  - **G3 is closed** by X6a and X6b.
  - **G4 is closed** by X4a.
- **X9-1's disclosed gap.** The unarmed census leaves X4a's observer on its real 5 s period. Recorded as disclosed, with nothing decided. Please check that this records only what X9-1's request disclosed, even though X9-1's own review is pending. Say if it should instead wait for that review.

## Dates

The revisions are dated 2026-10-04, the date of the latest acceptances they record (X7 r5, X6 r3, X9 r2 and the X6c reading).

## Decide

For each law separately:
- Does the revision change any accepted outcome? See "What is asked" for what that includes.
- Is each record faithful to its named source, and does it go no further?
- Is the predecessor snapshot exact, and is every accepted sentence preserved?
- Is anything else wrong?

Write one REVIEW.md and three verdict files: `x3d/review.json`, `x7/review.json` and `x9/review.json`. Each must contain:
- "verdict": ACCEPT or REQUIRED-FINDINGS;
- "requiredFindings";
- "noAcceptedOutcomeChanged": true or false;
- "subjectSha256": that law's PROPOSAL.md;
- the preserved snapshot's path, bytes and sha256.

Do not commit.
