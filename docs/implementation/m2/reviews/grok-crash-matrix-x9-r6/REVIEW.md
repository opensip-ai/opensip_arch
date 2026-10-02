# X9 r6

Claude Opus 5.5 leads. Grok is the single reviewer. Law review only. No product cargo. Git was read-only, against `/Users/sb/code/opensip-ai/opensip` at `a36da7c` (`a36da7ce495b49c2d82ad31a9ecef707e6de9909`). `~/Library/Application Support/OpenSIP` is absent. The private 413 fixture was not read.

Verdict: **ACCEPT**. `noAcceptedOutcomeChanged` is true. r6 corrects F00's boundary inside r5's second decision and leaves the other two decisions as r5 stated them.

| | |
|---|---|
| Subject | `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`, 82745 bytes, `34bff15dfdedd12adb29182c06678dbaf4872055fda2320260408dd9348a491a` |
| r5 bytes | `PROPOSAL-r5.md`, 82189 bytes, `729aa05e1e955f95194c3187678eb55f9983ba89a9182662016c65e5c97e7131`, the r5 review's `subjectSha256` |
| Preserved snapshot | `PROPOSAL-r4.md`, 74438 bytes, `4b387bbd7a08d901007ec50b811474b1f776f02b92f58c77812dc46e4091cd80`, the accepted r4 |

All seven `hashes.txt` rows match. Both files are 531 lines. Five lines differ.

## RF-1 is resolved

r5 put `x3c.ledger-create.ddl.commit.after` inside the UnknownCustody window, that point included. The required correction was: the UC window runs from the draw through `x3c.ledger-create.ddl.commit.before`, that point included, with reason `ledger-missing` or `ledger-unreadable`, whichever the kill left, and R4 UAU; the UAU window starts at `x3c.ledger-create.ddl.commit.after`, that point included, and runs until `x3c.attempt.commit.after`, with R1 and R4 both UAU.

r6 states that split in both places.

The header's decision bullets:

- from the draw through `x3c.ledger-create.ddl.commit.before`, that point included: R1 is UC with reason `ledger-missing` or `ledger-unreadable`, whichever the kill left, and R4 is UAU;
- from `x3c.ledger-create.ddl.commit.after`, that point included, until `x3c.attempt.commit.after`: R1 and R4 are both UAU.

The F00 cell's r5 clause states the same boundary: through `ddl.commit.before` for the UC reason and R4 UAU, and from `ddl.commit.after` (included) until `x3c.attempt.commit.after` for R1 and R4 UAU. The kill set is still every census point before `x3c.attempt.commit.after`, so that point stays outside F00.

At `a36da7c`, `write_schema` reaches the after-barrier only after `COMMIT` returns `Ok`:

```
c.execute_batch("COMMIT")
    .map_err(|_| WorkFailure::Operation(ProjectLedgerRefusal::CreationUndetermined))?;
opensip_platform::crash_barrier!(_, "ddl.commit.after", step);
```

(`project_ledger.rs` lines 500–502), inside `crash_scope!("x3c.ledger-create", …)` (lines 521–524). The `ddl.commit.before` barrier is the statement above that `COMMIT` (line 499). A kill at the before-point is while the schema commit has not returned. A kill at the after-point is after it has. The r6 note cites lines 500–502 for that order.

The pre-draw bucket stays `"notApplicable": "no-execution-id"`. R3 still writes nothing in every split. The rest of the F00 row (no attempt row, the ledger's logical state unchanged, R2's crash-state handling and Committed) stays. The sentence that the split is fixed by census position stays. The undecided gap after `x3c.ledger-create.wal` and before `ddl.commit` stays undecided, in the same words.

## Nothing else in r5 changed

The other four differing lines are the title (`r5` to `r6`) and one insertion in the r5 header, placed after `r4 bytes are preserved in PROPOSAL-r4.md.`. The note names RF-1, cites the `write_schema` order, and says the two F00 sentences and the F00 cell are corrected in place because r5 was not accepted. The r5 prose that follows the insertion is the same sentence: X9-2 found the issues while transcribing rows, the product is unchanged at `a36da7c`, and r5 changes three things.

Decisions 1 and 3 are byte-identical to r5, including F07, F08 (`As F07.`), F09, F10, item 6's candidate line, and item 12's r5 sentence. The wide citations left from r5 stay where they were: `recover.rs` lines 314–325 for `ledger-missing`, and lines 380–381 for the step-2 UAO return. This revision was the boundary fix only, and those ranges do not change the expectation.

No injection mechanism, point, kind, scope, label, evidence member, limit, or forbidden substitute changes. No other row changes. No other law's accepted outcome changes. The worktree was not committed.
