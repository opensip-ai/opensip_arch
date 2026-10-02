# Authorized settlement sweep inventory127

Adds exactly six files to inventory126 (unit X6b, selected at product f880145, with its fifty-five inheritance rows bound in the lock: D1's overrides joined at inventory122 and D2's four supersessions folded by X5a):
- `crates/security/src/custody/settlement_sweep.rs` (composition)
- `crates/security/src/custody/settlement_sweep_tests.rs` (test)
- `crates/storage/src/sweep.rs` (service)
- `crates/storage/src/sweep_tests.rs` (test)
- `crates/storage/src/ledger_store/sweep_settle.rs` (store)
- `crates/host/src/maintenance_tests.rs` (test)

It keeps all 942 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 948 planned files. No package edge changes: storage already depends on security, and host on security and storage. `check_package_edges --lane host` passes against inventory126 and inventory127 alike, with 20 declared and 20 resolved edges.

The rows are unit X6c, law X6 r3 item 12's X6c list ("the sweep's settle write in `ledger_store` and the `store-gc` per-namespace step"), under `commit-recovery-readonly.v3.md` §4 and F53:
- **security:** the custody half the sweep consumes (X6 r3 item 1's rule that custody owners are security's). It covers X1's admission with the endpoint, `I/stores/S` and the registry under the held fence, and X2's EXCLUSIVE lease per namespace, built from X2d's primitives.
- **storage:** the per-namespace step with its one ledger snapshot and its one settle write.
- **host:** the `store-gc` per-namespace step.

They also carry law X9 r2 item 5's `x6.sweep` points `after-exclusive`, `after-snapshot` and `settle.commit` (fallible).

**The host step is an existing row.** `crates/host/src/maintenance.rs` is already a planned row ("Coordinate store status, authorized purge/backup/recovery and pin-impact decisions through lifecycle/security/storage owners; never use cache deletion as evidence deletion."). The build plan also names it as `store-gc`'s owner. X6c creates the file with the sweep step only. The row stays by value; its description is broader than the file and is not contradicted. Only its test module is a new row.

**Changes to existing rows.** Every row stays by value. Where a lock inheritance row overrides a row, the text judged here is the effective description. Out-of-date descriptions are left for the next description-only successor, as earlier units left theirs.
- `crates/security/src/custody/namespace_lease.rs` (inherited override) gains two items:
  - `HeldLease::exclusive`, the EXCLUSIVE lease built outside `take_lease` for the sweep, which takes no project subject;
  - `try_lock`, `lock` for a caller that continues past a busy carrier (`Ok(None)`, so nothing latches).

  Its "No fence-free lease (item 7's recovery exception is X6's)" stays true: the sweep's lease is taken under the held fence. The description is out of date by omission.
- `crates/storage/src/ledger_store.rs`: adds `WriteTransaction::settle_admitted_attempt`, the one settle statement, and re-exports the sweep's child items. Its "used only by the guarded commit/authorized maintenance paths" is now exactly the case. The description stays true.
- `crates/storage/src/ledger_store/project_ledger.rs` (inherited override): declares the child module `sweep_settle`. Its "Nothing here settles an attempt or reads an outcome back" stays true of it. The child settles, and it is its own row, as `recovery_read` reads.
- `crates/storage/src/ledger_store/recovery_read.rs` (X6b): `existing` and `refused` become `pub(super)`, shared with `sweep_settle`. The description stays true.
- `crates/storage/src/commit_tests.rs`: declares `sweep_tests.rs` as its child module. The description is out of date by omission, as it already was for `recover_tests.rs`.
- Module declarations and re-exports only; the descriptions stay true:
  - `crates/security/src/custody.rs`
  - `crates/security/src/lib.rs`
  - `crates/storage/src/lib.rs`
  - `crates/host/src/lib.rs`

Nothing else changes.

**Order.** This successor's parent is the inventory the real product lock selects: inventory126 (unit X6b) at product f880145. Succession is by the lock's parent pin, not by number. X9-1's inventory118 is in flight on another parent, and whichever integrates second is rebuilt on the first.

`evidence/build_v127.py` reads the parent from the lock. Its PRIOR table maps inventory126 to the successor record that bound its fifty-five rows, and it checks each row against the lock's inheritance before carrying it. It writes only its own two paths, refuses to write over any path git already tracks, and refuses while a lock selects inventory127. Reruns reproduce the same bytes.

**Projection.** The fifty-five effective description overrides the lock binds to inventory126 stay bound by stable file path:
- the sixteen carried from inventory81 onward;
- D1's thirty-nine, joined at inventory122, four of them carrying D2's after text.

Their candidate selectors move by the inserted rows. No supersession is bound on inventory126, so none is folded, and the builder checks that each of D2's four `after` texts is still its row's effective description. The count stays 55.

`verify_projection.py` is inventory126's helper with its comment updated. It runs against the real lock at f880145: 55 rows, 278 corruptions refused.

`evidence/verify_scratch.py` appends inventory127 in memory over the worktree's lock (f880145) and replaces the lock's fifty-five inheritance rows with the record's fifty-five, with a synthetic review and assent. It reads the architecture checkout at its fixed path and writes nothing.
