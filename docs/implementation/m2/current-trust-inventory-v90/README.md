# Current-trust admission inventory90

Adds exactly two sources to inventory87 (unit X4T-0, selected at product 5b5f04c):
- crates/security/src/trust/current_trust_admission.rs
- crates/security/src/trust/current_trust_admission_tests.rs

It keeps all 760 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 762 planned files. No crate or dependency is added. The rows are unit X4T-a, law X4T r5.

- current_trust_admission.rs (service) is a child module of `ordinary_targets` (in trust/root_payload.rs), so it reuses that module's retained-head authentication composition rather than copying it. It admits the installation's current trust read-only and writes nothing.
- current_trust_admission_tests.rs (test) runs the admission over X4T-0's signed store, both in memory and natively through a supplied fence on a scratch installation.

**Changes to existing rows.** Their descriptions stay true, with one exception noted below.
- trust/ordinary_targets.rs: the child module declaration only.
- trust/role_machine.rs: a `Standing` projection of the existing private continuation join.
- trust_time.rs: a read-only `TimeAdmission` view of an `OrdinaryClockProposal`.
- trust/native_current.rs: a `parts_mut` accessor on the existing capture.
- trust/accepted_store_fixture.rs (test fixture): the payload closure now lists its three envelope member rows, which the retained inventory requires (X4T-0 judgment call 3 left them empty).
- trust/accepted_store_fixture_tests.rs: the source pin now admits X4T-a's test file, after checking it is included only under `cfg(test)`. Its inventory87 description ("named by no other source file") is now stale; an inventory successor carries rows by value, so that needs a later description-only contract successor.

**Projection.** The sixteen effective description overrides bound to inventory87 stay bound by stable file path, with parent inventory87. verify_projection.py is inventory87's helper with only its comment corrected, and runs against the real lock at 5b5f04c. evidence/verify_scratch.py appends inventory90 in memory over the real lock with a synthetic review and assent. evidence/build_v90.py refuses to write over any path git already tracks.
