# X9 r11 — ACCEPT

r11 closes RF-1. X9-5's census is the union of two unarmed `finalize` runs and one unarmed `store_gc` run. Each arm runs twice and the pair must match. A point reached in more than one arm takes the largest occurrence count. F53's kills at `x6.sweep.settle.commit` sit in that kill set.

Subject `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md` is 111180 bytes, sha256 `51f4fa16d6ae866eb0bfed4f1be2727157613c2647bc810a0e506413b434c8d1`. r10 was not accepted, so the preserved snapshot remains the accepted r9: `PROPOSAL-r9.md`, 95579 bytes, sha256 `e6ff60c12d45a5eb571169c0df832e2ebbb374d93d88abcd5bef379ae1a36cbe`. `PROPOSAL-r10.md` holds the RF-1 bytes, 109725 bytes, sha256 `27dd6f48668f541b17b5e3b027c68708748662d16d6a16f9e7c8e51472325ea3`, the r10 review's subject. The diff against that file is 60 lines in four hunks: the title, the item 5 census-scope bullet together with the r11 sentence on the r10 header, the census decision (including the rejected alternative), and the item 12 note. Product main `b999ae34ed567a010bd789488512884fa38df05b` is clean. No product cargo. The real home was absent.

## The fix

RF-1 required an unarmed `store_gc` run, twice and equal, unioned with the two `finalize` runs under the same larger-count rule. r11 states that rule for three runs as the largest occurrence count.

(a) is the lawful `finalize` commit on a fresh root. (b) is the exhausted-carrier `finalize`, so `finish` runs the rollover. (c) is `store_gc` in a fresh process after an unarmed (a) on that root. The sweep settles that attempt `committed`. Item 8 records this settle beside R3: a lawful commit's attempt is settled `committed`, and that settle is `nextWriter`, outside the row's R3. The product agrees. A lawful commit leaves the attempt `admitted`. The sweep lists `phase='admitted'` rows. Both the receipt and the association decide `Committed`. `settle_attempt` then commits at `x6.sweep` `settle.commit` (`crates/storage/src/ledger_store/sweep_settle.rs`). `x6.sweep` is `Access::Durable` (`crates/platform/src/crash_barrier.rs:108`), so one occurrence puts `settle.commit#1` in the kill set. F53 kills that point before and after. The F53 row stays on X9-5.

A (c) trace with no `x6.sweep.settle.commit` point is a `HARNESS-ERROR`. The kill set is the one derived from a trace that contains the point. Only the `store_gc` child's trace is (c). The unarmed (a) that prepares the root is that execution's setup, and the law says that (a) is not counted again. (a)'s own pair remains the lawful-commit arm. The decision's fixture and `candidate` children are that setup. (c)'s counted child is `store_gc`. The exclusion bullet keeps fixture and `candidate` traces out of the census.

Each of (a), (b) and (c) runs twice, and that arm's two executions match point for point (item 5, r2). A difference is a `HARNESS-ERROR`, never a smaller kill set. The trace digest is the normalized lines of (a), then (b), then (c).

The new rejected bullet is the alternative RF-1 allowed: moving F53's process-death kills into X9-3's file. Item 12 still gives F53's `store-gc` step to X9-5.

## What stands

The item 5 note and the item 12 note name the third run, so X9-6's union of the two targets' censuses includes it. X9-6's check sentence is unchanged: every point of that union's kill set is killed by a process-death run of either target. The runners, the host order, and the separate required-runs file are the r10 text. The one-entry sentence already requires the runner to refuse a second call when the first returned at replay before `operation`. X9-5 sets that flag in the runner. F53's row, and every other row, expected value, point, kind, scope, label, evidence member, and limit, are unchanged. No accepted outcome changes.

## Product

`maintenance::run` is the sweep loop (`maintenance.rs:89`). `SettlementSweep::sweep_one` leases, and the lease places `x6.sweep` `after-exclusive`. `sweep_namespace` places `after-snapshot`, then `settle_attempt` places `settle.commit`. `store_gc` calls `maintenance::run` over `settlement_sweep(at)`. A trace that reaches `settle.commit` has passed the earlier sweep points, and those points join the same union. Coverage of every kill-set point stays X9-6's `check`, which takes a kill from either target.
