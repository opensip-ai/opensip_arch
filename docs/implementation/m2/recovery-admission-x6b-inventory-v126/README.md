# Read-only recovery admission, recover and route inventory126

Adds exactly eight files to inventory125 (unit X7a, selected at product f097c5b, with its fifty-five inheritance rows bound in the lock: D1's overrides joined at inventory122 and D2's four supersessions folded by X5a):
- `crates/security/src/custody/recovery_admission.rs` (composition)
- `crates/security/src/custody/recovery_admission_tests.rs` (test)
- `crates/security/src/journal_store/recovery_location.rs` (adapter)
- `crates/storage/src/recover.rs` (service)
- `crates/storage/src/recover_tests.rs` (test)
- `crates/storage/src/ledger_store/recovery_read.rs` (store)
- `crates/host/src/recovery_route.rs` (composition)
- `crates/host/src/recovery_route_tests.rs` (test)

It keeps all 934 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 942 planned files. No package edge changes: storage already depends on security, and host on security and storage; `check_package_edges --lane host` passes against inventory125 and inventory126 alike.

The rows are unit X6b, law X6 r3 item 12's X6b list:
- **security:** `RequestedBinding`, `RecoveryRequest` and `RecoveryAdmission` (items 1 to 3: the read entry, 458c's walk without the fence, the registry and endpoint reads, X2 r8 item 7's fence-free SHARED-READ, the recheck), and the recovery-side carrier location constructor with the public view of X6a's standing;
- **storage:** `recover` and `RecoveredCommit` (items 4, 5 and 8) with the read-only ledger snapshot and object reads, and `NotPrepared::ExistingAttempt`'s `requested` binding (item 6);
- **host:** the read-entry route that admits a request, calls `recover` and projects item 8's rows.

They also carry law X9 r1 item 5's `after-lease` and `after-ledger-snapshot` points in the read-only scope `x6.recover` (gap G3).

**Changes to existing rows.** Every row stays by value. Where a lock inheritance row overrides a row, the text judged here is the effective description. Out-of-date descriptions are left for the next description-only successor, as earlier units left theirs. Two of them now say something this unit makes untrue, and are named first:
- `crates/security/src/journal_store/carrier_floor.rs` (inherited override): declares the new child module `recovery_location`. Its effective description says `CarrierLocation::admitted` "is CarrierLocation's only production constructor (item 11)". X6 r3 item 12 adds the recovery-side constructor `CarrierLocation::recovered`, so that sentence is now out of date by contradiction.
- `crates/security/src/custody/installation_session.rs` (inherited override): `read_members` takes the fence as an `Option` and `read_recovery_members` reads the same members without it. The description's "Its consumers are the read session … and doctor's installation check" omits recovery's admission.
- `crates/security/src/custody/namespace_lease.rs` (inherited override): seven private helpers become `pub(super)` and `HeldLease::shared_reader` is added, so that recovery's admission builds its lease from X2d's own primitives. The module itself still takes no fence-free lease, so its "No fence-free lease (item 7's recovery exception is X6's)" stays true.
- `crates/security/src/custody/operation_handoff.rs` (inherited override): `open_store_root`'s steps move into `store_root_in` (unchanged, now shared with recovery), and `namespace_spelling`, `STORES` and `STORE_MARKER` become `pub(super)`. The description stays true.
- `crates/security/src/custody/commit_session.rs`: three row maps become `pub(super)`. The description stays true.
- `crates/security/src/store_custody.rs`: adds `admit_existing_store_directory`, a read-only admission of an existing store directory. Out of date by omission.
- `crates/security/src/journal_store.rs` (inherited override), `crates/security/src/custody.rs`, `crates/security/src/lib.rs`: module declarations and re-exports. The descriptions stay true.
- `crates/storage/src/commit.rs`: `NotPrepared::ExistingAttempt` gains `requested: Box<RequestedBinding>` (X6 r3 item 2), and `store_generation_digest` becomes `pub(crate)` for recovery. The description stays true.
- `crates/storage/src/commit_tests.rs`: declares `recover_tests.rs` as its child module. Out of date by omission.
- `crates/host/src/finalization.rs` (X7a): the `ExistingAttempt` arm now carries the requested binding and item 3's row discloses all four of its members beside the invariant row (X7 r5 item 10 and X7a's judgment call 7: the second unit to integrate discloses it; the namespace is now the binding's). `Termination` gains `requested`. The description stays true.
- `crates/host/src/finalization_tests.rs` (X7a): the `ExistingAttempt` row's test checks the three other members, the join test passes the binding, and the source pin's security `use` line names `RequestedBinding`. Its description ("the binding's namespace beside it") is out of date by omission.
- `crates/storage/src/availability.rs`: adds `state_text`. The description stays true.
- `crates/storage/src/recovery.rs`: `LedgerStanding` derives `Clone`. The description stays true.
- `crates/storage/src/ledger_store.rs`, `crates/storage/src/ledger_store/project_ledger.rs` (inherited override), `crates/storage/src/lib.rs`, `crates/host/src/lib.rs`: module declarations and re-exports. `project_ledger.rs`'s "Nothing here settles an attempt or reads an outcome back" stays true of it; its child `recovery_read` reads, and is its own row.

Nothing else changes.

**Order.** This successor's parent is the inventory the real product lock selects: inventory125 (unit X7a) at product f097c5b. The unit was written on 81214cb (inventory124) and moved to f097c5b when X7a integrated first; the diff applied unchanged, with X7a's `ExistingAttempt` disclosure added, and this successor was rebuilt on the new parent. Succession is by the lock's parent pin, not by number.

`evidence/build_v126.py` reads the parent from the lock. Its PRIOR table maps inventory125 to the successor record that bound its fifty-five rows, and it checks each row against the lock's inheritance before carrying it. It writes only its own two paths, refuses to write over any path git already tracks, and refuses while a lock selects inventory126. Reruns reproduce the same bytes.

**Projection.** The fifty-five effective description overrides the lock binds to inventory125 stay bound by stable file path:
- the sixteen carried from inventory81 onward;
- D1's thirty-nine, joined at inventory122, four of them carrying D2's after text (below).

Their candidate selectors move by the inserted rows. D2's four `passageSupersessions` (law VD1 item 3), on `store_lineage.rs`, `installation_session.rs`, `read_premise.rs` and `initial_installation.rs`, are on inventory122. X5a's inventory123 folded them, and the lock binds them to inventory125 as plain inheritance rows whose `after` is D2's `after`, so none remains to fold on this parent. `build_v126.py` folds any supersession the lock binds on the parent after checking its `before` against the current effective text, requires none on inventory125, and checks that each of D2's four `after` texts is its row's effective description. The count stays 55. `verify_projection.py` is inventory124's helper with its comment updated. It runs against the real lock at f097c5b: 55 rows, 278 corruptions refused. `evidence/verify_scratch.py` appends inventory126 in memory over the worktree's lock (f097c5b) and replaces the lock's fifty-five inheritance rows with the record's fifty-five, with a synthetic review and assent. It reads the architecture checkout at its fixed path and writes nothing.
