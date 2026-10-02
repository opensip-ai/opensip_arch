# Host finalization inventory125

Adds exactly ten files to inventory124 (unit X6a, selected at product 81214cb, with D1's thirty-nine overrides and D2's four supersessions already folded into its fifty-five inheritance rows):
- crates/host/src/finalization_tests.rs
- nine files under crates/host/tests/refusal/cases/:
  - host_authoritative_run_raw_json.rs
  - host_authoritative_run_bool.rs
  - host_authoritative_run_run_id.rs
  - host_authoritative_run_replayed.rs
  - host_authoritative_run_literal.rs
  - host_authoritative_run_default.rs
  - host_authoritative_run_deserialize.rs
  - host_authoritative_run_clone.rs
  - host_authoritative_run_serialize.rs

`crates/host/src/finalization.rs` is not added. It is already a planned row of the parent, so it is kept by value (see "Changes to existing rows").

It keeps all 924 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 934 planned files.

**No new edge.** The host already depends on the evaluator, security, storage, contracts and platform (declared and resolved since before inventory119). `check_package_edges --lane host` passes against both inventory124 and inventory125, with 20 declared and 20 resolved edges.

The rows are unit X7a, one host unit (law X7 r5 item 11). It covers items 1 to 5 and 8, with item 10's tests on injected outcomes, read under the laws X3b r10, X3d r6, X5 r3, X6 r3, X8 r3, X9 r1 and X12 r3:
- `finalize`: the replay join with `REPLAY_LIMITS`, the caller's admission, `CommitSession::open`, `prepare_commit`, `publish`, `finish` on every end path, then the delivery phase;
- the delivery phase reads nothing from the store and takes no lease, receipt or read session (X7 r5 item 4), with `ExistingAttempt` on the invariant row with its ExecutionId and `CommitUndetermined` with the namespace disclosed (items 3 and 5);
- the exported authoritative projection `authoritative_run(&PublishedCommit) -> AuthoritativeRun`, and the separate ephemeral projection;
- item 3's table, projected exhaustively into the host's `InstallationTerminationV1`, with the RunId retained after commit and the ExecutionId disclosed for an undetermined commit;
- X9's two `x7.delivery` points (`required` and `optional`, both fallible);
- law X8 r3 item 3's owner rows for this unit.

The files:
- **finalization_tests.rs (test).** It is included as `finalization.rs`'s `cfg(test)` module, as `fact_admission_tests.rs` is for `fact_admission.rs`. It opens no scratch installation, home or lock. Its order tests run on the synthetic replay corpus `crates/host/tests/fixtures/replay-fixtures.json`. A `ProjectOperation` cannot be built from the host's tests until X9-1's support surface or X8b's scenario seam exists (law X9 r1 gap G1), so the session-level integration rows of X7 r5 item 10 are not in this unit.
- **The nine `refusal/cases` files (fixture).** Only X8a's driver compiles them, against the plain `cargo check -p opensip-host` surface. In each, the control compiles and the misuse fails with exactly one error, carrying the annotated code, fragment and line:
  - **Group A** (E0308, "mismatched types"): the authoritative projection given a raw `JsonValue` holding a Run.
  - **Group B** (E0308 each): the projection given `true`, a RunId `&str`, or a replayed but uncommitted `&ReplayedRun`.
  - **Groups D, E and G**, for the exported `AuthoritativeRun` under X8's export rule: a struct literal (no code, "cannot construct `AuthoritativeRun` with struct literal syntax due to private fields"), a `Default` probe, a `Deserialize` probe, a `Clone` probe and a `Serialize` probe (E0277 each).

  Census rows are added for unit X7a. `AuthoritativeRun` has no non-public inherent function, and nothing `cfg(test)` returns one (the tests write the literal from the child module), so no group F case is owed.

**Changes to existing rows.** Every row stays by value. Where a lock inheritance row overrides a row, the text judged here is the effective description. Out-of-date descriptions are left for the next description-only successor, as earlier units left theirs.
- `crates/host/src/finalization.rs`: the planned row's description says the coordinator routes `CarrierCapacityExhausted` "through cleanup and operation-lease release to lifecycle rollover under its fence" and uses `outcomes.rs` for the retained analysis projection. X7a finishes the exhausted attempt (X3d's `finish` carries the exhaustion into X3b's end step, which owns the rollover) and projects item 6a's busy row. The analysis envelope's rendering is the caller's delivery phase (M3, X11). So the description is out of date by omission on the projection, not wrong on the route.
- `crates/host/src/lib.rs`: declares the private `finalization` module (`#[allow(dead_code)]`, macOS only, as the security and storage commit types are) and re-exports `AuthoritativeRun` and `authoritative_run`. The description ("Expose the intentionally public API; keep internal modules private.") stays true.
- `crates/host/src/fact_admission_tests.rs`: the `REPLAY_LIMITS` caller pin moves from "at most one" (vacuous until X7a) to exactly one caller, in `finalization.rs`. The description says "(vacuous until X7a)", so it is out of date by that phrase.
- `crates/host/tests/admission_tests.rs` (X8a's driver): the nine census rows for unit X7a and the header note. The effective description lists the census rows by unit up to X3d-1, so it is out of date (already by X3d-2's and X5a's rows).

**Order.** This successor's parent is the inventory the real product lock selects: inventory124 (unit X6a) at product 81214cb. The lead assigned the number 125. inventory118 (X9-1) is in flight elsewhere. Succession is by the lock's parent pin, not by number. The unit was first written on 54e6166 with inventory125 built on inventory123. When X6a integrated at 81214cb, before any review, the product diff was moved unchanged (its bytes are identical) and inventory125 was rebuilt on inventory124. No earlier candidate was reviewed.

`evidence/build_v125.py` reads the parent from the lock (by default the product checkout's `design-lock.json`, or a lock path given as its one argument). Its PRIOR table maps inventory124 to the successor record that bound its fifty-five rows. It checks each row against the lock's inheritance before carrying it. It writes only its own two paths, refuses to write over any path git already tracks, and refuses while a lock selects inventory125. Reruns reproduce the same bytes.

**Projection.** The fifty-five effective description overrides the lock binds to inventory124 stay bound by stable file path:
- the sixteen carried from inventory81 onward;
- D1's thirty-nine, joined at inventory122;
- D2's four supersessions, already folded into their rows' effective descriptions when inventory123 integrated, and carried through inventory124.

Only their candidate selectors move, by the ten inserted rows. No contract successor bound at 81214cb names inventory124 as a supersession parent, so the builder folds nothing new (`supersessionsFolded: 0`) and the count stays fifty-five.

`verify_projection.py` is inventory123's helper with its comment updated for this parent. It runs against the real lock at 81214cb: 55 rows, 278 corruptions refused. `evidence/verify_scratch.py` appends inventory125 in memory over the worktree's lock (81214cb) and replaces the lock's fifty-five inheritance rows with the record's fifty-five, with a synthetic review and assent. It reads the architecture checkout at its fixed path and writes nothing.
