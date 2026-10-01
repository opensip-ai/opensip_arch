# Settlement reserve inventory112

Adds exactly one source to inventory110 (unit X2d, selected at product 9d51f33):
- crates/platform/tests/settlement_reserve_tests.rs

It keeps all 788 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 789 planned files. No crate or dependency edge is added: the test uses only `opensip-platform` and std. The row is unit X3d-0: law X3d r6 item 8 (the settlement reserve in `WorkLedger`), with item 13's X3d-0 tests.

- **settlement_reserve_tests.rs (test).** It is an integration test of the platform's public API, beside `work_ledger_tests.rs`. It covers item 13's behavioural cases through the re-export: a settlement spendable after each way the ledger closes; charges inside it drawing only from the allowance; an overrun, an `Err` and an unwind inside it latching both; one reservation per instance; a foreign reserve refused before its action; and another ledger unchanged. It also holds the source pin that no production source names `reserve_settlement` or `SettlementReserve` until X3d-1. item 13's `compile_fail` doctests live on `SettlementReserve` in work_ledger.rs.

**Why there is a successor at all.** Law X3d r6 item 13 says X3d-0 "comes with an inventory successor for the platform crate". The precedent (460, 461a and 464) is that a unit that adds no file owes no inventory successor if every changed file's description stays true. X3d-0 adds this test file, so the successor is owed and carries its row. The alternative, putting the public-API tests in work_ledger.rs's private test module, would add no file and leave the law's successor with nothing to carry.

**Changes to existing rows: none.** The descriptions stay true, so no existing row changes.
- `crates/platform/src/work_ledger.rs` gains `reserve_settlement`, `SettlementReserve` and `settle`, its `compile_fail` doctests, and one private-state unit test. Its description stays true. The ledger is still non-authority bounded accounting. Its failure is still permanent: `failed` is never cleared, and outside `settle` every call still refuses. The settlement is one more precharged reservation, charged before any effect and never refunded. The description does not name 467's `prepaid` either. A refresh naming both, if wanted, belongs to the same later description-only contract successor that inventory97, 101, 102, 105 and 110 named.
- `crates/platform/src/lib.rs` re-exports `SettlementReserve`. Its description ("Expose the intentionally public API; keep internal modules private") stays true.

No other existing source changes.

**Order.** This successor's parent is the inventory the real product lock selects: inventory110 (unit X2d) at product 9d51f33. `evidence/build_v112.py` reads the parent from the lock and maps inventory110 to the successor record that bound its sixteen rows. It writes only its own two paths, refuses to write over any path git already tracks, and refuses while a lock selects inventory112. Rerunning it reproduces the same bytes. inventory106, 108 and 111 are other units' in-flight candidate numbers; none is read or written here. If another unit is integrated first, this candidate needs a parent-only rebuild: add the new parent to `PRIOR` and rerun.

**Projection.** The sixteen effective description overrides bound to inventory110 (carried unchanged back to inventory81) stay bound by stable file path, with parent inventory110. verify_projection.py is inventory110's helper, with only its comment corrected to name its parent. It runs against the real lock at 9d51f33, which selects inventory110. `evidence/verify_scratch.py` appends inventory112 in memory over the real lock, with a synthetic review and assent, and runs the X3d-0 worktree's real `verify_design`.
