Grok review: law X9 r5, an amendment. Claude Opus 5.5 leads. You are the single reviewer.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r5.
- This is a law review with no product cargo. Run git only read-only.
- Product facts are pinned at product `a36da7c`. Read them with `git show a36da7c:<path>` in `/Users/sb/code/opensip-ai/opensip`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Why

Unit X9-2 transcribes its rows into `required-runs.v1.json` before any run. While doing so it found two rows whose expected values the integrated `recover` cannot meet, and one producer its `commit` driver needs. The coordinator took all three as lead decisions and asked for them in the law itself, so that you rule on them once rather than as unit-level judgment calls.

## Pins

Pins are in hashes.txt.
- **The snapshot.** `crash-matrix-x9/PROPOSAL-r4.md` is X9 r4 byte for byte, without its "r4 ACCEPTED" note: 74438 bytes, `4b387bbd…`. That equals `reviews/grok-crash-matrix-x9-r4-x6-r4/x9/review.json` subjectSha256.
- **The diff.** Diff PROPOSAL.md against that snapshot. Every predecessor line survives verbatim, with these exceptions:
  - the title;
  - the ACCEPTED note already in the working law;
  - "r5" insertions. In the table rows F00, F07, F09 and F10, and in item 6's candidate line, each insertion is appended after the accepted text.

## The three decisions (the r5 header; table cells; item 6; item 12)

1. **F07 to F10: R1 is plain UAO.**
   - **What the code does.** `RecoveredCommit::UnknownAttemptOpen` has no fields (`recover.rs`, lines 101–104), as in X6 r4 item 2. `recover` returns UAO at step 2 from the ledger alone (lines 380–381; `recovery.rs` line 290 for admitted with no receipt and no association). It captures the carrier, which is the only source of a `witnessWould*` diagnosis, only after a receipt and association join (lines 395–419).
   - **What the decision does.** These rows never reached the evidence `COMMIT`, so their R1 is plain UAO. The would-REVERT, would-ADVANCE or OK expectation is R2's witness action only, which each row already states.
2. **F00 split by kill point.**
   - **What the code does.** The ExecutionId is drawn in `CommitSession::open`. The ledger is created later, in `prepare_commit`, inside `x3c.ledger-create`. Between those two steps, `recover` gives UC `ledger-missing` (`recovery_read.rs`, lines 136–146; `recover.rs`, lines 314–325) or UC `ledger-unreadable`. That is X6's F24 sentence.
   - **The expectations by kill point:**

     | Kill point | R1 | R4 |
     |---|---|---|
     | Before the draw | n/a | n/a |
     | From the draw through `x3c.ledger-create.ddl.commit.after` | UC (`ledger-missing` or `ledger-unreadable`) | UAU |
     | After that point | UAU | UAU |

   - **What stays the same.** R3 writes nothing, and the rest of the row is unchanged. Which split applies is fixed by census position, never by outcome.
3. **The synthetic run candidate moves to X9-2.**
   - **Why X9-2 needs it.** `prepare_commit` refuses unless the Run's `projectId` is the session's ProjectId and its evaluator closure is the session's core closure. A first registration draws the ProjectId at random (`first_registration.rs`, line 427), and the injected test inventory's closure is not any corpus closure, so no corpus Run binds.
   - **Where it lives.** Item 6 already lists the producer. X9-2 builds it in storage's `crash_matrix_support`, because it needs the evaluator.
   - **What it produces.** Inputs only, never a `ReplayedRun`. It rewrites the project id and closure, recomputes the dependent content ids and blob digests, re-derives the outputs with the public `derive_evaluation`, and builds evidence, seal and Run as `replay_run` checks them.
   - **The order.** The matrix child calls `replay_run` after `CommitSession::open` and before `prepare_commit`. This is stated as a matrix-only order. The host's replay-before-custody order (X5 r3 item 3, F01) is unchanged and stays X9-5's.
   - **Rejected alternatives, recorded:**
     - a ProjectId pinned to a corpus Run, by a scripted draw or a registry mutation;
     - registering in the fixture child;
     - a support function returning `ReplayedRun`;
     - a textual output rewrite without re-derivation;
     - waiting for X8c.

Also recorded, and not decided: a possible F00 state between `x3c.ledger-create.wal` and `ddl.commit` that `create_or_open_ledger` may not resume. X9-2 stops and reports it if a run shows it.

## Decide

- Is each decision sound and narrow, and consistent with X6 r4 (items 2 and 4), X3d r7 item 3, X5 r3 items 3 and 7, X3c's ledger creation, and X9 r4's items 6 to 8?
- Does the candidate keep item 6's limits (inputs only, no authority type, `synthetic` label, `replay_run` the only mint)?
- Is the matrix-only replay order safely confined so that the host order is unaffected?
- Is the F00 split well defined from the census, before any run?
- Does any other accepted outcome change? Is the r4 snapshot exact, with every accepted sentence preserved?
- Is anything else wrong?

Write REVIEW.md and review.json under the output directory. review.json contains:
- "verdict": ACCEPT or REQUIRED-FINDINGS;
- "requiredFindings";
- "noAcceptedOutcomeChanged": true means nothing changed beyond the three stated decisions;
- "subjectSha256";
- "subject" (path, bytes, sha256);
- "preservedSnapshot" (path, bytes, sha256).

Do not commit.
