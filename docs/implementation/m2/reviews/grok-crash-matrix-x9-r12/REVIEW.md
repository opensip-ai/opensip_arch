# X9 r12 — ACCEPT

r12 is the nine decisions the development run forced, and the diff is those decisions. Each expected value follows the owning law and the product at `b999ae34ed567a010bd789488512884fa38df05b`. No other row, point placement, or host rule changes.

Subject `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md` is 123524 bytes, sha256 `341075762e8cf515267e24c8a38ea4e2ba58368487893e83a7c1f9c0917b3337`. The preserved snapshot is the accepted r11: `PROPOSAL-r11.md`, 111180 bytes, sha256 `51f4fa16d6ae866eb0bfed4f1be2727157613c2647bc810a0e506413b434c8d1`. The diff against that file is 167 lines in ten hunks: the title, the r11 acceptance stamp, the r12 header, the item 7 limit note, the item 8 ladder note, the item 9 cells named in the request, the item 11 timing note, and the item 12 notes on X9-3 and X9-4. Product main is clean. No product cargo. The real home was absent. The development run is the lead's report; this review judges the decisions against the law and that commit.

## Distinct Run for F13, F14 and F15

After a landed evidence `COMMIT`, the receipt and the Run's availability row are retained. The ordinary candidate is one RunId for a project and a core evaluator closure, because the corpus is fixed and `synthetic_run_candidate` rewrites only those two bindings (`run_candidate.rs`). R2 therefore stages the same Run. `classify_staging` maps the SQLite abort `retained key cannot be replaced` to `StagingMismatch`, and that variant is `ProjectLedgerRow::Invariant` (`project_ledger.rs`). That is X3c item 10, and it is the limit X3d-2 disclosed: M2 does not commit one Run twice, because availability is staged unconditionally.

The distinct variant is test support in storage's `crash_matrix_support`, inputs only, under `crash-matrix`. It is built as the candidate is. Before `rewrite`, one source file's bytes in the snapshot inventory are replaced by same-length bytes. The fixpoint then rehashes that blob and substitutes every dependent content id, and `derive_evaluation` re-derives the outputs, so the RunId differs. Same length leaves the inventory's length fields intact. `replay_run` stays the only constructor. The run stays labelled `synthetic`. A script directive `{"r2": "distinct"}` names it.

R2 of F13, F14 and F15 uses it. F13 and F14 stay R2 Committed. F15 is Committed and still creates no second receipt for the killed ExecutionId: the distinct commit draws its own. Every other ladder, including X9-2 and F36, keeps the ordinary candidate. F36 must commit the same semantic RunId, and its orphan SEAL has no retained receipt. Expecting the invariant row would leave "the next writer proceeds" untested on the rows where the attempt committed. Re-committing the same Run stays X3d-2's limit.

## F14's settle point

`StoppedSession::finish` reaches `x3d.finish.settle.before` only inside the arm where a REV or a CLN is owed (`commit_session.rs`: `without_evidence || latched || revoked`, and the barrier sits in that arm). A lawful commit owes neither, so no X9-3 census run reaches the point, and an armed kill there is "armed point not reached".

The kill moves to X9-4: F39's script, then death at `x3d.finish.settle.before`, with F13's expectations. F39 latches after admission, so finish owes the REV and the barrier is reached. The evidence commit has already landed, so R1 is still committed-historically with `pendingSettlement`, and the sweep still settles that attempt. X9-3's F14 keeps the `x3d.publish.published` kill. X9-4's census must include an unarmed owed-end-record run, so the point is in that unit's kill set.

## F24 wrong store generation

The variant rewrites every row's store-generation digest and leaves the ledger file and schema readable. Recovery's snapshot is taken under the admitted digest (`read_recovery_ledger`). No receipt, association, or attempt row is visible. Owner step 2's row "both absent, no row" is `unknown-attempt-unobserved`. `join_ledger` returns `UnknownAttemptUnobserved` for that input. R2 commits under the admitted digest: the mutated rows are keyed by the other digest, so they do not collide. R3 is the left attempt. Item 8 scores that attempt as nothing written, and records R2's settle beside it as `nextWriter`. The namespace outcome is `swept`.

Owner step 1's "a wrong generation is never absence" is the other case: an unreadable ledger, an empty fallback, or a file that is another generation's database, which is `unknown-custody`. r12 rejects that file. It needs a second store generation, and no M2 writer creates one (L5). The mode-`000` and truncated-header variants keep R1 `unknown-custody`, R2 refused, and R3 host I/O.

## F27 operation and execution

Owner step 2 and `join_ledger` give `BindingUnusable` only when the association's store digest, namespace, or carrier differs from the admitted binding. X6 r4 item 6 gives the same standing to a request whose binding differs, including `operationRef` compared with the attempt row. An association whose `operationRef` differs from the attempt row, or whose `executionId` differs from the request, fails the join and returns `UnknownCustody`. `recover` records that standing as reason `ledger-join`. Those two variants are R1 `unknown-custody:ledger-join`. The store-generation and namespace swaps, and a request with a different binding, stay `binding-unusable`.

## F49(a)

The reader is held at `x6.recover.after-j`. The writer appends and exits. The first bracket is then unstable, and owner step 3 takes its one fresh capture. `decide` confirms on that second capture when the anchor is usable (`recovery_capture.rs`). The ledger snapshot already holds the receipt with the attempt still `admitted`, which step 2 continues as committed-historically with `pendingSettlement`. The row's "never UQ, never a corruption diagnosis" stays: step 4 reports a quarantine only when the fresh capture also fails its stable observations. The appending writer's own outcome is unscored. A second commit of the ordinary candidate is the F13 limit, and the reader's conclusion is the earlier attempt.

## F36

C5, as r3 recorded it, refuses R2 at admission under the revoked view. F19 and F38 therefore have no later commit of the same semantic RunId. F36 runs the orphan SEALs of F09 and F11 only. The later ExecutionId is ladder step R5: `recover` of R2's ExecutionId, and whether the orphan SEAL and R2's SEAL name one RunId. The earlier ExecutionId stays UAO, R3 refused, R4 terminal-not-committed, and the RunId stays unblacklisted.

## F39's admission hold

`OperationGate::admit` places `x4.gate.admit.after` and returns while `steps` still holds the shared monitor (`operation_guard.rs`: `finish()` runs, then `drop(cell)`). The observer's tick takes that same monitor (`observe`). A writer held at `admit.after` while the parent resumes `x4.observer.tick#1` never reaches `latch.after`. That is the watchdog X9-3 reproduced. Moving the placement would change X4 r7 item 3, which holds the monitor from the final observation through admission.

The next barrier after `drop(cell)` is `x3c.evidence.commit` `.before`. Staging's `begin` and `stage-*` points run before the final checkpoint. `permit.consume` calls `PreparedLedgerCommit::commit` with no barrier between the permit and that fallible point. So `x3c.evidence.commit.before#1` is the first point after admission at which the monitor is released, and the gate is already in state 1. The script arms the tick and that point, awaits the tick's first hold and then the point, publishes the revocation, resumes one tick, awaits `latch.after` at 1→3, and resumes the main thread. A latch after admission does not cancel the permit, so the row stays Committed with `latchedAfterAdmission`. This is the script for F39, F44 and F45. X9-4 inherits it for F39 and F40's latch variant. X9-5's delivery half runs the same F39 row. The r10 and r11 host machinery is unchanged.

The revoked subject is `CommitSession::core_closure`, the receipt's selected core, which is what the observer compares (`OperationGuard`'s `core_closure`). X8c's B6 publishes that value. The accepted store fixture's `CORE_CLOSURE` is the constant its P0 names (`accepted_store_fixture.rs`), and `install_accepted_trust` returns that constant. The commit child writes the session's closure under the scratch root, outside the installation and outside the trace, and the publisher child reads it.

## Timing guard

Item 11 already makes a run above 2 s a `HARNESS-ERROR` rather than an accepted `OBSERVER.FAIL_STOP`. r12 assigns that guard to every run that arms `x4.observer.tick`, and X9-3 implements the record for F44 and F45. X9-4 uses the same implementation.

The tick barrier is a gate that replaces the wait, so an armed observer holds at `x4.observer.tick` until the parent resumes it, and that hold is before the monitor lock (`observe_loop`). `OperationGuard::start` runs after `LeaseFree::first_read` (`operation_handoff.rs`). The parent's monotonic clock, from the first tick-hold record to the admission-hold record, therefore covers the writer's awake interval from just after that first read through the last checkpoint. The wall clock stays the scripted clock. The run records `timingGuard: {"monotonicMs": n, "limitMs": 2000}`. Above 2000 ms the run is a `HARNESS-ERROR`. The checker admits the member, requires it where the script arms the tick, and leaves it out of the repetition comparison.

## The limit list

Item 7's r4 bullet said the check-unit limits are L1 to L10. r8 set L1 to L11, and the checker implements that list. The r12 note records the bullet as L1 to L11. The limit list itself is unchanged.

## What stands

The standings r12 names are the owner's existing ones: `unknown-attempt-unobserved`, `unknown-custody` with `ledger-join`, `binding-unusable`, and committed-historically with `pendingSettlement`. No new public detail is introduced. X9-2's rows and X9-5's host rules are outside these notes. No accepted outcome changes beyond the nine decisions.
