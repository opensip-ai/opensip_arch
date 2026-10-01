# Live security guards inventory116

Adds exactly eight files to inventory117 (unit X8a, selected at product c2352ae):
- crates/security/src/custody/operation_guard.rs
- crates/security/src/custody/operation_guard_tests.rs
- crates/security/src/custody/operation_live_tests.rs
- crates/security/src/trust/live_observation.rs
- crates/security/src/trust/live_observation_tests.rs
- crates/host/tests/refusal/cases/security_admission_permit_unnameable.rs
- crates/host/tests/refusal/cases/security_final_gate_unnameable.rs
- crates/host/tests/refusal/cases/security_operation_guard_unnameable.rs

It keeps all 835 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 843 planned files. No crate or dependency edge is added: both new modules use only `opensip-identity` and `opensip-platform`, which security already depends on; the host projection uses `opensip-security` and `opensip-contracts`, which host already depends on; and the cases name only `opensip_security`, compiled against the existing surface. The rows are unit X4a: law X4 r7 items 2 to 8 and 11 (the monitor and gate created first and the fenced first read as the monitor's first read at the lease-free point, `OperationGuard` built inside X2e's handoff, the shared monitor history, the observer thread and its per-observation ledger, the checkpoint over a `JournalAppendLock` borrow, `FinalGate` admission and the termination mapping), with law X9 r1 G4's `x4.*` crash points and law X8 r3 item 3's group D rows that X8 assigns to X4a.

- **operation_guard.rs (composition).** custody.rs's macOS module `operation_guard`, beside X2e's `operation_handoff`, so the receipt's, the lease's and the subject's private owners stay crate-private. It holds `LeaseFree`, `OperationGuard`, the observer thread, `Checkpoint`, the stop causes and rows, `trust_termination`, and a `cfg(test)` scripted clock.
- **operation_guard_tests.rs (test).** Its `cfg(test)` child module: the guard's pieces with scripted clocks.
- **operation_live_tests.rs (test).** Included under `operation_handoff_tests.rs`'s `cfg(test)` module (`mod live`), so it reuses X2e's scratch-home helpers: X4a through the real handoff.
- **live_observation.rs (service).** current_trust_admission.rs's macOS child module, beside X4T-b's `floor_publication`: the fenced operation read, the retained trust handles, the observation and the S6 predicate.
- **live_observation_tests.rs (test).** Its `cfg(test)` child module.
- **The three `refusal/cases` files (fixture).** X8 r3 group D's unnameable rows for `AdmissionPermit`, `FinalGate` and `OperationGuard`: each misuse fails with exactly one E0603 on the private module in its path (`commit_authority`, `commit_authority`, `custody`), and each control compiles. They are compiled only by X8a's driver.

**Changes to existing rows.** Every row stays by value. The descriptions marked "out of date" are left for the description-only successor already named at inventory97 to inventory111, as earlier units left theirs.
- `custody/operation_handoff.rs`: the seams filled (`trust_start` at the lease-free point; the guard built and moved into `ProjectOperation`; `journal` lends a `Checkpoint`; the end path drops the guard first; three refusal variants). Its description's "OperationGuard (X4a) is a seam not built here" is now out of date.
- `custody/operation_handoff_tests.rs`: X2e's tests run on accepted stores through a `begin_test` adapter (scripted clock, ticks on request), and include `operation_live_tests.rs`. The description's case list is out of date.
- `custody/ordinary_writer.rs`: `begin_operation` takes the floor publication's `TrustInvocation`; `begin_operation_with` (`cfg(test)`), `gate_step`, `selected_closure`. Already out of date (inventory111) and stays so.
- `custody/read_premise.rs`: `charge_guarded` and `ReceiptGuard` (the receipt's rechecks on a borrowed scope of its own attempt ledger). Already out of date and stays so.
- `custody/installation_admission.rs`: `WriterFence`, the write gate's held fence as the trust readers' `HeldFence`. The description stays true.
- `custody/namespace_lease.rs`: `recheck_namespace_at`, `HeldLease::recheck_held` (name binding and the fresh nonblocking probe), and a `cfg(test)` lost-lock seam. The description does not mention the post-release guard.
- `custody/project_admission.rs` and `custody/first_registration.rs`: owners-only rechecks after the release (`recheck_owners`, `recheck_registered_owners`). Descriptions stay true as far as they go.
- `custody/installation_read_fixture.rs`: `accept_trust`, `write_trust` and `swap_trust` (atomic replacement), with the zero-rights owner allow on every new trust file. The description does not mention them.
- `custody.rs`: declares `operation_guard`. The description stays true.
- `commit_authority.rs`: `OperationGate` (created before any prepared value; `admit` binds it and hands it back on a refusal) and the `x4.gate.admit.after` and `x4.gate.latch.after` points.
- `revocation.rs`: `FreshnessMonitor` crate-visible, `Sample` with the wall clock, `read_sampled_with` (the counter receives the opening sample), `boundary_with` (item 3 step 4), stop-reason subjects.
- `clock_observation.rs`: `project_monitor_sample`, the existing projection over the monitor's opening sample.
- `installation_termination.rs` (security) and `crates/host/src/installation_termination.rs`: `RootDetail` and seven variants on existing details, with their S12 classes. Both descriptions name only 468's rows and are out of date.
- `journal_store.rs`, `journal_store/carrier_operation.rs`, `journal_store/carrier_append.rs`: `JournalAppendHeld` re-exported, `JournalAppendHeld::holds`, `JournalAppendLock::namespace_id`.
- `trust/current_trust_admission.rs`: the admitted view keeps item 4's closure components and revocation evidence; `live_observation` declared. `trust/floor_publication.rs`: one comment. `trust/ordinary_targets.rs`, `trust/root_payload.rs`, `trust.rs`, `lib.rs`: re-exports, `RootDetail`, and the `cfg(test)` `write_accepted_trust`.
- `trust/accepted_store_fixture.rs` (X4T-0): `Spec.store` and `Spec.revocation_version`, defaults unchanged. The description does not mention them.
- `crates/host/tests/admission_tests.rs` (X8a's driver): an `owned` row constructor and the three group D rows in the census, unit X4a. Its description stays true.

**Order.** This successor's parent is the inventory the real product lock selects: inventory117 (unit X8a) at product c2352ae. The unit was first written on inventory111 at abf2a48, then rebased onto daa7b01 (inventory114) and onto c2352ae before any review, so no earlier candidate was reviewed. evidence/build_v116.py reads the parent from the lock and maps inventory114 and inventory117 to the successor records that bound their sixteen rows. It writes only its own two paths, refuses to write over any path git already tracks, and refuses while a lock selects inventory116. Reruns reproduce the same bytes. The number 116 sits below its parent's 117; succession is by the lock's parent pin, not by number.

**Projection.** The sixteen effective description overrides bound to inventory117 (carried unchanged from inventory114 back to inventory81) stay bound by stable file path, with parent inventory117. verify_projection.py is inventory117's helper with only its comment corrected to name its parent. It runs against the real lock at c2352ae, which selects inventory117. evidence/verify_scratch.py appends inventory116 in memory over the real lock, with a synthetic review and assent; it finds the architecture root from its own location.
