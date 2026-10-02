# X9 r10 — REQUIRED-FINDINGS

r10 is a lawful route for host's coordinator and sweep, and the separate required-runs file is the right fix for the case overlap. The host census does not cover `store_gc`. That is RF-1.

Subject `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md` is 109725 bytes, sha256 `27dd6f48668f541b17b5e3b027c68708748662d16d6a16f9e7c8e51472325ea3`. Preserved r9 is `PROPOSAL-r9.md`, 95579 bytes, sha256 `e6ff60c12d45a5eb571169c0df832e2ebbb374d93d88abcd5bef379ae1a36cbe`, the r9 review's subject. The diff against that snapshot is the r9 acceptance stamp, the title, the r10 header, the four in-place notes, and the new forbidden-substitute bullets. No row, expected value, limit, point, kind, scope, label, or evidence member changes. No accepted outcome of another law changes.

Product main `b999ae34ed567a010bd789488512884fa38df05b` is clean. Facts below are that commit. No product cargo. The real home was absent.

## Runners

The gap is real. `finalize` is `pub(crate)` at `finalization.rs:395`, inside private `mod finalization`. The crate exports `AuthoritativeRun` and `authoritative_run` only. `maintenance::run` and `sweep_store` are `pub(crate)` inside private `mod maintenance`. `sweep_store` calls `SettlementSweep::admit`. Host `crash_matrix_support` is the storage forward and nothing else. The only in-crate call of `finalize` is the unit-test include.

`finalize_commit` and `store_gc` are routes into that coordinator and that sweep step.

- `finalize` already takes `admit: impl FnOnce() -> Result<ProjectOperation, Row>` and `&mut impl DeliveryPhase`, and it calls `replay_candidate` before `admit()` and `CommitSession::open`. Setting `admit` to `operation(at, root)` uses the r4 entry. `operation` runs only after replay succeeds, which is the function's own order.
- `DeliveryPhase` is the existing item 4 seam. A fixed phase in the pinned support module, rendering exit 0 into a buffer the runner owns, goes through `deliver`'s `x7.delivery` `required` and `optional` barriers. A `fail-before` there is the delivery fault F16 and F17 already name. The phase is not a second coordinator, and the caller does not supply it.
- `SettlementSweep` implements `maintenance::Sweep` at `maintenance.rs:61`. `store_gc` calling `maintenance::run(settlement_sweep(at))` is the one sweep step. `sweep_store` stays unused, so the matrix process does not call `SettlementSweep::admit`.
- Both functions can see the `pub(crate)` items from host's support module. Nothing is widened and no cfg site is added. The module's existing `cfg(all(feature = "crash-matrix", target_os = "macos"))` gate and the crate `compile_error!` keep them off `scenario-fixtures` and off release.
- The report is values: `InstallationTerminationV1`, a RunId string, the exit, and the end-path, rollover, and optional disclosures. `AuthoritativeRun` stays inside `finalize` and is dropped after `run_id()` is copied. `NamespaceSweep` is already a value enum. The report holds no lease once the runner returns.
- One process, one call among the three entries and the two runners. A second call refuses on the invariant row and has no effect. That includes a first call that returned at replay and never reached `operation`: the r4 flag is set inside the entry, and the runner owes the refusal itself when the entry was not reached. `publish_revocation` still refuses after an entry.

The rejected substitutes match the code: a unit-test child would leave item 12's integration target, a `#[path]` copy would compile `finalization_tests.rs` under `cfg(test)`, and a public `finalize` is what X5 r3 item 6 rejects.

## Host order

X5 r3 item 3 is the finalize child's order. `finalize` replays, then admits, then opens the session. A replay refusal returns before `admit()`, so that invocation takes no fence, lease, attempt, object, or journal effect.

The `candidate` child exists because `synthetic_run_candidate` takes `&CommitSession` (`run_candidate.rs`). It calls `operation`, then `CommitSession::open`, writes the candidate's objects, blobs, and claimed RunId, and stops with `refused().finish()` before `prepare_commit`. `refused` is the certain-refusal path: the in-process gate latches, and with no end-path reserve `finish` appends no REV. The project ledger and the attempt row are `prepare_commit`'s. The law's stop rule, a ledger or attempt row in that child's trace or post state, matches that boundary. The next process's `finalize` is the root's first attempt.

The file is item 6's synthetic run candidate, written under the scratch root as inputs. F01's parent edits that file. Item 9's `mutation` label is a parent change to stored custody bytes. The candidate file is an input, and F01's row stays `exec (host)` with no mutation label. Storage's replay-after-open order is untouched.

## Required-runs file

`UNIT_CASES` at `b999ae3` gives F12 and F53 to X9-3 and X9-5, and F39 and F40 to X9-4 and X9-5. `check-unit` keeps every row of a named case from the one file it is given. One file would make each unit demand the other's variants. A host file with the same schema and `clockEpoch`, holding only X9-5's rows, lets `check-unit` stay as it is: X9-5 passes that file. X9-6 taking both files, both pairs of run sets, a union census, and kill-set coverage across either target is the same `check`, applied per set, with the coverage r4 reserved for X9-6. A `(case, variant)` is unique inside its own file and its own run set.

## Census

RF-1. The two `finalize` runs are the right census for the finalize driver. They are not the census of both host drivers.

## What did not change

The r9 stamp is the existing acceptance note. The product-baseline sentence still names `f1b8321`. X7 r6's session-level list maps onto F17's delivered base, F16, F39's delivery half, F12 and F40's caller route, and F32. `ExistingAttempt` remains F34 on X9-4, and the gate ledger is in memory, so a run record cannot show its balance. Both stay for X7's next revision. That scheduling leaves X7's rows as they are.

## RF-1

X9-5's drivers are `finalize_commit` and `store_gc`. Item 12 gives X9-5 F53's `store-gc` step, and F53 kills at `x6.sweep.settle.commit` before and after. `x6.sweep` is `Access::Durable` in the scope registry, so a census that records the point puts `settle.commit#1`, the middle occurrence, and `#n` in the kill set. `check-unit` refuses a killed point that is not in that set.

r10's census is two unarmed `finalize` runs, a lawful commit and an exhausted-carrier commit, fixture and `candidate` excluded. That pair is why F32's rollover points, reached only from `finish` after `CarrierCapacityExhausted`, are in the set. `finalize` does not call `maintenance::run` or `settlement_sweep`. An unarmed finalize trace has no `x6.sweep` point. F12's and F40's caller-route kills sit inside `finalize`, on `x3c.evidence`, so those points are in this census. F53's kills do not.

r8's rule is that a unit's census is the census of its own drivers, which is why the exhausted run was added. X9-3's sweep census is a different target and a different `matrix.json`. It does not satisfy X9-5's `check-unit`.

Required: the host census includes an unarmed `store_gc` run, twice and equal, unioned with the two `finalize` runs by the same larger-count rule, so F53's `x6.sweep` kills lie in X9-5's kill set. The alternative that keeps this census is a sentence that places those process-death kills in X9-3's file and states that X9-5's F53 rows kill no point outside the finalize union.
