# X9 r5

Claude Opus 5.5 leads. Grok is the single reviewer. Law review only. No product cargo. Git was read-only, against `/Users/sb/code/opensip-ai/opensip` at `a36da7c` (`a36da7ce495b49c2d82ad31a9ecef707e6de9909`). `~/Library/Application Support/OpenSIP` is absent. The private 413 fixture was not read.

Verdict: **REQUIRED-FINDINGS**. One finding, RF-1. `noAcceptedOutcomeChanged` is true: the only accepted-outcome edits are the three lead decisions, and RF-1 is inside the second. No other row, and no other law, changes.

| | |
|---|---|
| Subject | `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`, 82189 bytes, `729aa05e1e955f95194c3187678eb55f9983ba89a9182662016c65e5c97e7131` |
| Preserved snapshot | `docs/implementation/m2/crash-matrix-x9/PROPOSAL-r4.md`, 74438 bytes, `4b387bbd7a08d901007ec50b811474b1f776f02b92f58c77812dc46e4091cd80` |

The snapshot equals the `subjectSha256` of `reviews/grok-crash-matrix-x9-r4-x6-r4/x9/review.json`. All sixteen `hashes.txt` rows match, including every product blob at `a36da7c`.

## Preservation

The r4 file is 485 lines and the r5 file is 531. Every predecessor line survives in order. Seven lines are not byte-identical, and each is an allowed exception:

- The title changes from r4 to r5.
- The r4 header gains `r4 ACCEPTED by Grok on 2026-10-02.` after `PROPOSAL-r3.md. `.
- Item 6's candidate bullet keeps its accepted sentence and appends the r5 clause.
- The F00, F07, F09, and F10 cells keep their accepted sentences and append the r5 clause before the closing pipe.

The r5 header (the three decisions, the rejected alternatives, the undecided WAL gap, and the unchanged-from-r4 sentence) is new. Item 12's X9-2 bullet keeps the r4 sentence and gains one r5 sentence after it. F08 stays `As F07.` The header applies F07's correction to F08 by that sentence, so F08 has no separate cell insertion.

## Decision 1 — F07 to F10, R1 is plain UAO

Sound, and consistent with X6 r4 items 2 and 4 and with X9 r4 item 8.

`RecoveredCommit::UnknownAttemptOpen` is a unit variant (`recover.rs` line 103). X6 r4 item 2's closed list names `UnknownAttemptOpen` and `UnknownAttemptUnobserved` with no fields. Step 2 of `recover_from` returns `UnknownAttemptOpen` from `LedgerStanding::UnknownAttemptOpen` (`recover.rs` lines 381 and 388). That standing is `join_ledger` on an admitted attempt with neither receipt nor association (`recovery.rs` line 290). The carrier capture, `source.carrier`, runs at line 416, after the association is present (line 404) and the evidence is present (line 409). X6 r4 item 4 puts the carrier at step 3, after the ledger snapshot and `join_ledger`.

F07, F09, and F10 say the evidence `COMMIT` never happened, so that join does not exist. Their r5 clauses keep the accepted R2, R3, and R4 sentences and move would-REVERT, would-ADVANCE, and OK to R2's witness action. Item 8 already defines that action as OK, REVERT, ADVANCE, INIT, or OPEN. F08 inherits the same R1 through `As F07.` Rows that do have the join (F02 and the others the header does not name) keep their R1 diagnoses. The rejected alternatives, a diagnosis field on UAO and a second carrier capture inside R1, would change X6's closed standings or its step order.

Two citation ranges are wide. Lines 101–104 also contain `TerminalNotCommitted`; the unit variant is line 103. The header's "lines 380–381" are the end of the binding check and the step-2 comment; the UAO return is line 388. The behavior those sentences use is the behavior at line 388.

## Decision 2 — F00 split by kill point

The three buckets are fixed by census position, and the UC reason inside the middle bucket is the disjunction the header states. The inclusive end of that bucket is wrong. That is RF-1.

What holds:

- Before `x3d.session.execution-draw`, there is no ExecutionId. Item 8 already skips R1 and R4 with `"notApplicable": "no-execution-id"`. `CommitSession::open` draws the id at `crash_barrier!("x3d.session", "execution-draw", …)` (`commit_session.rs` lines 330–332).
- From the draw until the schema commit returns, `read_recovery_ledger` returns `Missing` when `projects`, the namespace, or the ledger child is absent (`recovery_read.rs` lines 136–146) and `Unreadable` when the file is present and the open or the selected schema fails (lines 161–178). `recover_from` maps those to UnknownCustody `ledger-missing` and `ledger-unreadable` (`recover.rs` lines 355–365), before step 2. That is X6 r4 item 4's sentence: "A missing, empty or fallback ledger or carrier is never absence (F24)."
- After a selected schema exists and before `x3c.attempt.commit.after`, there is still no attempt row for the drawn ExecutionId. `read_pair` and `load_attempt` return none, and `join_ledger` on `(None, None)` with no attempt is `UnknownAttemptUnobserved` (`recovery.rs` line 291; `recovery_snapshot.rs` lines 89–96). R1 and R4 are both UAU. R3 writes nothing in every bucket, which the cell already said.
- R4 stays UAU once R2 has created the ledger, in both of the later buckets. F00's kill window still ends before `x3c.attempt.commit.after`, so the original ExecutionId has no attempt row.

The header's `recover.rs` lines 314–325 are `requested_mismatch` and the start of `recover_from`. The `ledger-missing` return is lines 355–359. `recovery_read.rs` lines 136–146 are exact.

The undecided gap is accurately left open. After `x3c.ledger-create.wal` and before `ddl.commit`, `create_or_open_ledger` resumes only an empty file whose `-wal` is absent (`project_ledger.rs` lines 540–550). Any other existing file goes to `open_verified`. The header says X9-2 stops and reports that state if a run shows it. That is R2's resume, and this revision does not classify it.

### RF-1

F00's middle split includes `x3c.ledger-create.ddl.commit.after`.

`create_or_open_ledger` runs under `crash_scope!("x3c.ledger-create", …)` (`project_ledger.rs` lines 521–524). Inside `write_schema`, `COMMIT` must return `Ok` before the barrier:

```
c.execute_batch("COMMIT")
    .map_err(|_| WorkFailure::Operation(ProjectLedgerRefusal::CreationUndetermined))?;
opensip_platform::crash_barrier!(_, "ddl.commit.after", step);
```

(`project_ledger.rs` lines 500–502). A kill at `x3c.ledger-create.ddl.commit.after` is after that `Ok`. The schema commit has landed. `ReadSnapshot::open` is the read-only WAL opener (`ledger_store.rs` lines 221–222), `verify_selected_schema` compares the stored schema with `selected_ddl()` (`project_ledger.rs` lines 388–393), and the empty receipt, association, and attempt join to `UnknownAttemptUnobserved`. `recover_from` returns that standing (`recover.rs` lines 389–390).

The header and the F00 cell put that point, included, in the UC bucket (`ledger-missing` or `ledger-unreadable`). X9-2 transcribes the cell into `required-runs.v1.json` before any run, so that census point would be recorded with an expectation `recover` does not meet. The header's own criterion is the one the code implements: UC while the schema has not committed, and UAU once the ledger exists with no attempt row. `ddl.commit.after` is the second of those.

Required: the UAU window starts at `x3c.ledger-create.ddl.commit.after`, that point included, and runs until `x3c.attempt.commit.after`. The UC window is from the draw through `x3c.ledger-create.ddl.commit.before`, with reason `ledger-missing` or `ledger-unreadable`, whichever the kill left. R4 stays UAU in both windows. R3 still writes nothing. The rest of the F00 row stays. The undecided WAL-before-ddl gap stays undecided.

## Decision 3 — the synthetic run candidate moves to X9-2

Sound, and it keeps item 6's limits. The matrix order is confined to matrix children.

`prepare_commit` takes a `ReplayedRun` and a `CommitSession` (`commit.rs` lines 462–464). Step 1 calls `plan`. `plan` refuses `PlanRefusal::Project` when the Run's `projectId` differs from the bound project, and `PlanRefusal::Closure` when `evaluator_closure` differs from `bound.core_closure` (lines 248–256). `Bound::of` copies `CommitSession::project_id` and `core_closure`. Those accessors exist (`commit_session.rs` lines 407 and 413). X3d r7 item 3 step 1 requires the evaluator closure to equal the session's selected core closure. X5 r3 item 3 puts target identity in that same comparison, and `project_id`'s comment cites both. A first registration's production draw is `opensip_platform::project_id_draw()` (`first_registration.rs` line 427). The scripted draw above it is `#[cfg(test)]` (lines 422–425), so a `crash-matrix` library build uses the random draw. No pinned corpus Run binds.

Item 6 already lists the candidate. The r5 clause puts the builder in storage's `crash_matrix_support`, which is the crate that already depends on the evaluator, and says the host module forwards it. The product is inputs only: a pinned corpus Run, `projectId` and closure rewritten from the session, dependent content ids and blob digests recomputed, outputs re-derived with public `derive_evaluation` (`composition.rs` line 1081), then evidence, seal, and Run built as `replay_run` checks them. `replay_run` is `pub fn replay_run` (`replay.rs` line 163) and its comment says only that function mints `ReplayedRun`. It calls `derive_evaluation` (line 202) and compares objects and blobs. Item 6's forbidden list still bars a support function that returns `ReplayedRun` (the authority-type bullet, with the r4 exception limited to the three driver entries). The r5 header rejects that return again. Runs stay labelled `synthetic` under item 6's existing record sentence.

The matrix child calls `replay_run` after `CommitSession::open` and before `prepare_commit`. The header says this order is for matrix children only, and that the host order, replay before any custody, stays X5 r3 item 3 and F01, which stay X9-5's. F01's cell is unchanged. Replay takes no custody, so no X3d step changes.

The rejected alternatives stay rejected. A ProjectId pinned to a corpus Run needs a scripted draw or a registry mutation. Registering in the fixture child would drop registration and INIT from F00. A textual output rewrite would not satisfy `replay_run`'s re-derived proof. Waiting for X8c would take X5 r3 item 7's B0 Run, which X5 leaves to X8c and which this revision does not take.

## Anything else

The unchanged-from-r4 sentence holds for every injection mechanism, point, kind, scope, label, evidence member, limit, and forbidden substitute, and for every row and expected value the three decisions do not name. No other law's accepted outcome changes. No new public code, row, or detail is added. The worktree was not committed.
