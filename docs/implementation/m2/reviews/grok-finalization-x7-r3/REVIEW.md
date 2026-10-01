# Law X7 r3 — host finalization

Law review only. No product cargo. The OpenSIP support directory is absent. Subject `finalization-x7/PROPOSAL.md` is 17625 bytes, sha256 `aa390f820472807235b3414122e1df2c2d9e3b7ec9452d849bd3e17aa1aa1c3e`, matching `hashes.txt`. Preserved r2 is `PROPOSAL-r2.md`, 16470 bytes, sha256 `6757ad1391056531135081447a64336bdc653014cc2072bb607b72e327d8c1b1`, matching the r2 review. Live product HEAD is `46b1d60faef4ca004170ae3cbcff7c9b29ad3f7c`.

The diff against r2 is the title, the r3 provenance sentence, item 7, and one bullet of the capacity-exhaustion integration test. Item 6, item 6a, and the rest of the accepted r2 text are unchanged.

Judged against the r2 finding and accepted X1 r1 item 5, X3d r3 item 8, X3b r6 items 4 and 9, and the unchanged 468a budget and busy rows.

## What holds

r2 RF-1 is closed. Item 7 charges the rollover to the attempt ledger this invocation's one admission already opened, which X3d item 8 identifies with X1's attempt ledger and X3b item 9 calls the operation ledger. The charge covers the rollover's carrier reads, the `TERMINAL` append, the g+1 publication, and the end step's floor write. Each is charged before it runs. Every post-effect confirmation is reserved there first, including the witness reopen and directory barrier X3b item 9 names. The gate ledger stays the gate's own work. No second ledger is opened, and no fresh admission is created. Charging the rollover to the gate ledger is the rejected alternative.

An exhausted attempt ledger at the rollover is item 6's existing budget rollover failure, `WORK.BUDGET_EXHAUSTED`, and it does not rewrite the attempt's outcome. That is X3b item 4's end-step rule, already in item 6. The attempt itself stays on item 6a's row when the rollover completes or is skipped: operational-failed, exit 4, `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, detail `PROJECT.BUSY`, with S7's subject and remedy. The 468a route for `WORK.BUDGET_EXHAUSTED` is unchanged: operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`.

The integration test expects those attempt-ledger charges, each confirmation reserved first, and a gate ledger whose balance the rollover does not change.

The r2 holdings outside this charge stay in force. `finish` still appends any pending REV or CLN under the analysis operation lease, then releases it. The end step still takes the installation fence by X3b item 4's walk on this invocation's one write receipt and one gate admission. Finalization does not call `admit_ordinary_writer`, does not begin a second `DurableWriteGate`, and does not take a fence of its own. Under that fence, X3b r7's rollover still takes X2 item 7's EXCLUSIVE order. A busy lock still skips the rollover. The `TERMINAL` append still uses X3b item 5's order under that lease. Until X3b r7 is accepted, X7a reports item 6a's row and performs no rollover. Replay stays inside X5's limits. The commit and its end path stay on the attempt ledger. Delivery stays on the read session's ledger. DR-G27, the delivery phase, `CommitUndetermined`, and the exhaustive projection are unchanged.

X3d's rejection of charging the REV and CLN at end time stays on item 3 step 0's end-path reserve. The rollover is later attempt work on the same ledger, charged before each of its own effects, and a shortfall is a rollover failure rather than an unfunded REV.

## Verdict

ACCEPT. r2 RF-1 is closed.
