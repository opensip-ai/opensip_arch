# Current-trust admission inventory96

Adds exactly two sources to inventory94 (unit X3c-1, committed and next to be selected after inventory93 at product 8452ab9):
- crates/security/src/trust/current_trust_admission.rs
- crates/security/src/trust/current_trust_admission_tests.rs

It keeps all 768 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 770 planned files. No crate or dependency is added. The rows are unit X4T-a, law X4T r5.

**Order.** This successor replaces the reviewed inventory90 (parent inventory87) with the same two rows, byte for byte, rebuilt on the current predecessor; evidence/build_v96.py asserts that they equal inventory90's. inventory90 is left unchanged. The product source is rebased onto 8452ab9 with its hunks unchanged.

- current_trust_admission.rs (service) is a child module of `ordinary_targets` (in trust/root_payload.rs), so it reuses that module's retained-head authentication composition rather than copying it. It admits the installation's current trust read-only and writes nothing.
- current_trust_admission_tests.rs (test) runs the admission over X4T-0's signed store, both in memory and natively through a supplied fence on a scratch installation.

**Changes to existing rows.** Their descriptions stay true, with one exception noted below.
- trust/ordinary_targets.rs: the child module declaration only.
- trust/role_machine.rs: a `Standing` projection of the existing private continuation join.
- trust_time.rs: a read-only `TimeAdmission` view of an `OrdinaryClockProposal`.
- trust/native_current.rs: a `parts_mut` accessor on the existing capture (alongside F3's test-scratch change already on main).
- trust/accepted_store_fixture.rs (test fixture): the payload closure now lists its three envelope member rows, which the retained inventory requires (X4T-0 judgment call 3 left them empty). Its `Spec` gains `revocations`, the signed list's entries (empty by default), and the delivering core is named once as `CORE_CLOSURE`.
- trust_ordinary_metadata.rs: its private `catalog` module is visible to the root_payload tree, so X4T-a matches the catalog owner's typed causes instead of their text.
- trust/accepted_store_fixture_tests.rs: the source pin now admits X4T-a's test file, after checking it is included only under `cfg(test)`. Its other `Spec` literals take the new field's default.

**The one stale row.** The inherited description of trust/accepted_store_fixture_tests.rs says its source pin shows the constructor is named by no other source file. X4T-a's test file names it, so that sentence is now false. verify_design refuses an inventory successor that changes a row carried from its parent, so inventory96 carries the row by value and does not correct it. The correction is the D1 description batch of EXIT-PLAN.md (a description-only contract successor), which already lists this row as "named by X4T-a's tests"; inherited rows there wait for VD1.

The change to the pin was not avoided. Its alternatives each weaken the pin: reaching the generator through a re-exported alias in root_payload.rs, or naming X4T-a's test file with the `accepted_store_fixture` prefix the pin skips, would hide the use from the text the pin checks. The admitted exception is narrower: one named file, and only while its `include!` sits under `#[cfg(test)] mod tests`.

**Projection.** The sixteen effective description overrides bound to inventory94 (carried unchanged from inventory93, 91, 87, 84, 83, 82 and 81) stay bound by stable file path, with parent inventory94. verify_projection.py is inventory94's helper with only its comment corrected. While the real lock at 8452ab9 still selects inventory93, it runs against a scratch lock that evidence/projection_lock.py writes outside both repositories, with inventory94's successor row and re-projected inheritance appended; once inventory94 is selected, projection_lock.py copies the real lock unchanged. evidence/verify_scratch.py appends inventory94 and then inventory96 in memory over the real lock with synthetic reviews and assents, or only inventory96 once inventory94 is selected. evidence/build_v96.py refuses to write over any path git already tracks, and while a lock selects inventory96.
