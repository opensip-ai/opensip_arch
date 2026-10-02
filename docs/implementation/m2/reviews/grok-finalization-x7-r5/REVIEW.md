# X7 r5

Claude Opus 5.5 leads. Grok is the single reviewer. Law re-review of X7 r4 RF-1. No product cargo. Git was read-only. `~/Library/Application Support/OpenSIP` is absent.

Verdict: **ACCEPT**. RF-1 is closed. Nothing else in the r4-to-r5 diff is a required finding.

| File | Bytes | sha256 |
|---|---|---|
| `docs/implementation/m2/finalization-x7/PROPOSAL.md` (r5) | 22329 | `1b49b92157e11acd5cf6b586cec77b6919c2d4f51c7f508da16c1519aff5ede0` |
| `docs/implementation/m2/finalization-x7/PROPOSAL-r4.md` | 22037 | `e28669d92dd5d6afc539b3c800dc5d3150ca34a96132079b6e8b0d8146dc921c` |

The r4 snapshot hash equals the `subjectSha256` of `reviews/grok-recovery-x6-r3-x7-r4-x9-r2/x7/review.json`. Both pins in this review's `hashes.txt` match the files.

## What changed

The diff is three edits.

The title is now X7 r5. The r4 header paragraph gains one sentence: r5 answers Grok X7 r4 RF-1, and r4 bytes are preserved in `PROPOSAL-r4.md`. Item 5 replaces the parenthetical. Every other line is unchanged, including item 3's `ExistingAttempt` row, item 4's in-memory delivery decision, item 6's certain-path `REV`/`CLN` append, and items 7, 10, and 11.

Item 5 now reads: finalization never calls X6's `recover` in the same invocation. It finishes the stopped session: after an uncertain journal, attempt-admission or evidence `COMMIT`, `finish` appends nothing and copies no floor, and the next writer reconciles (X3d r6 item 7). The durability row, the `executionId`, the later `recover(executionId)` remedy, and the r4 namespace disclosure stay.

## RF-1

r4 told an implementer of `CommitUndetermined` that `finish` reconciles under the lease and copies the floor only on OK, REVERT or ADVANCE. X3d r6 item 7 withdraws that for the uncertain path. After an uncertain journal, attempt-admission, or evidence `COMMIT`, `finish` appends nothing, does not reopen the carrier, does not run `reconcile_witness`, copies no floor, and releases the lease. The next writer reconciles.

The replacement is that rule, scoped to the three uncertain `COMMIT` kinds that produce this outcome, and it cites X3d r6 item 7. The header glosses the same sentence as "after an uncertain outcome". The "never calls `recover`" rule and the namespace disclosure are still in the paragraph. Item 6 still has `finish` append pending `REV` or `CLN` on the open-ledger capacity path. The diff adds no public code or detail.

The adjective "uncertain" stands immediately before "journal", and the list continues "attempt-admission or evidence `COMMIT`". This paragraph is the `CommitUndetermined` item, and the header states the uncertain-outcome reading. That is the reading X3d r6 item 7 gives all three kinds. No further edit is required.

## The rest of r4

Item 4 is byte-identical to the text accepted in the r4 review. For an unlatched ordinary commit, M2 required delivery projects the `PublishedCommit` already held (exact committed receipt bytes and RunId, built only after evidence `COMMIT` succeeded) and the evaluation that produced the committed Run. `finalize` lends `&PublishedCommit` only. The phase takes no lease, receipt, or read session, draws no authority from the stopped session, and runs after `finish` has released the writer lease. A later surface that must read the store remains a later read-entry invocation. That decision stands. The remainder of r4 was accepted except RF-1, and this diff does not reopen it.
