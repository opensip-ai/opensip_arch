# Read-only carrier recovery capture inventory124

Adds exactly two files to inventory123 (unit X5a, selected at product 54e6166, with its fifty-five inheritance rows bound in the lock: D1's overrides joined at inventory122 and D2's four supersessions folded by X5a):
- `crates/security/src/journal_store/recovery_capture.rs` (validator)
- `crates/security/src/journal_store/recovery_capture_tests.rs` (test)

It keeps all 922 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 924 planned files. No package edge changes: the unit is inside `opensip-security`, and `check_package_edges --lane host` passes against inventory123 and inventory124 alike.

The rows are unit X6a: law X6 r2 item 1's security owner and item 12's X6a list, `journal_store::recovery_capture`:
- the bracket (`W1 H1 J W2 H2`, at most one fresh capture);
- closed witness and floor shape validation before any comparison;
- the anchor table, through X3b r10 item 4a's reconciliation of the newest tail;
- the step 4 rule;
- the §1 carrier precedence observations.

All of it is read-only. They also carry law X9 r1 item 5's read-path points in the read-only scope `x6.recover` (`after-w1`, `after-h1`, `after-j`, `after-w2`, `after-h2`, `after-fresh-capture`; gap G3).

- **recovery_capture.rs (validator).** It is `carrier_floor.rs`'s macOS child module, as the start, the append and the rollover are. The file sits at `journal_store/recovery_capture.rs`, and it is not re-exported: X6b adds the crate path and the production `CarrierLocation` from its admission.
- **recovery_capture_tests.rs (test).** It is included as `recovery_capture.rs`'s `cfg(test)` module. It uses X3b's production creation, start and append paths on X3b-1a's scratch fixture. Later generations, gaps and prunes are planted with the lifted-and-reinstalled triggers. It also holds F28's pruned-record fixture, which X9 r1 L10 names.

**Changes to existing rows.** Every row stays by value. Where a lock inheritance row overrides a row, the text judged here is the effective description. Out-of-date descriptions are left for the next description-only successor, as earlier units left theirs.
- `crates/security/src/journal_store/carrier_dispatch.rs`: `CapturedDispatch::inherited_present` and the non-current snapshot's `inherited` flag. These let read-only recovery tell the `{A, B}` prefix from an unpublished fresh footprint. The description stays true.
- `crates/security/src/journal_store/carrier_floor.rs`: declares the child module `recovery_capture` (macOS). The effective description (inherited unchanged from inventory123's projection) lists its own floor-step and creation duties. It names no read-only child, so it is out of date by omission.

Nothing else changes. `journal_store.rs`, `generation_anchor.rs` and `bracketed_capture.rs` are untouched (judgment call 2 of the review request).

**Order.** This successor's parent is the inventory the real product lock selects: inventory123 (unit X5a) at product 54e6166. The unit was written on adc9081 and moved to 933e78b for its r1 review (F5's test fixtures, VD1's tooling, and the lock-only D1 and D2 entries), on parent inventory122. For r2 it moved to 54e6166, where X5a (evaluator, host and doctor ingress only) selects inventory123; its product diff applies unchanged, and this successor was rebuilt on the new parent. The lead assigned the number 124. Succession is by the lock's parent pin, not by number.

`evidence/build_v124.py` reads the parent from the lock. Its PRIOR table maps inventory122 and inventory123 to the successor records that bound their fifty-five rows, and it checks each row against the lock's inheritance before carrying it. It writes only its own two paths, refuses to write over any path git already tracks, and refuses while a lock selects inventory124. Reruns reproduce the same bytes.

**Projection.** The fifty-five effective description overrides the lock binds to inventory123 stay bound by stable file path:
- the sixteen carried from inventory81 onward;
- D1's thirty-nine, joined at inventory122, four of them carrying D2's after text (below).

Their candidate selectors move by the two inserted rows. Contract successor D2's four `passageSupersessions` (law VD1 item 3; D2's README, "After selection"), on `store_lineage.rs`, `installation_session.rs`, `read_premise.rs` and `initial_installation.rs`, are on inventory122. X5a's inventory123 folded them, so the lock binds them to inventory123 as plain inheritance rows whose `after` is D2's `after`, and none remains to fold on this parent. `build_v124.py` folds any supersession the lock binds on the parent after checking its `before` against the current effective text, requires exactly four on inventory122 and none on inventory123, and checks that each of D2's four `after` texts is its row's effective description. The count stays 55. `verify_projection.py` is inventory122's helper with the same fold and its comment updated. It runs against the real lock at 54e6166: 55 rows, 278 corruptions refused. `evidence/verify_scratch.py` appends inventory124 in memory over the worktree's lock (54e6166) and replaces the lock's fifty-five inheritance rows with the record's fifty-five, with a synthetic review and assent. It reads the architecture checkout at its fixed path and writes nothing.
