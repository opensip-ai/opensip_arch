# Doctor report inventory80

Adds exactly four sources to selected79:
- crates/host/src/doctor_report.rs
- crates/host/src/doctor_report_tests.rs
- crates/security/src/custody/installation_doctor.rs
- crates/security/src/custody/installation_doctor_tests.rs

It keeps all 745 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 749 planned files. No crate or dependency is added. The rows are unit 458c-c: law 458c r6 items 7, 10 and 12, with owner section 5's Diagnostics paragraph.

- doctor_report.rs (adapter) is the first doctor report assembler, after the reference `doctor_projection.py` `DoctorSession.assemble` and `workflows_model.v1.py` `doctor()` and `terminate()`. It projects doctor's installation check: an unreachable installation on its law 468 item 6 row with no report, and each structural finding as one `CONFIG.CUSTODY_REFUSED` entry with its `installation-incomplete:` subject and fixed remedy.
- doctor_report_tests.rs (test) runs every `doctor-cases.json` vector against it, restated with the two inherited stand-in codes.
- installation_doctor.rs (service) is doctor's installation check on the observation session, returning the structural findings of a reachable incomplete installation instead of refusing.
- installation_doctor_tests.rs (test) checks it on scratch homes with a creator-published P0.

The unit's other changes edit existing rows:
- custody.rs gains the module wiring.
- security lib.rs re-exports `DoctorInstallation`, `InstallationFinding` and `observe_installation_for_doctor`.
- host lib.rs exposes the assembler.

`trust doctor` and `store status` have no report producer in the product, so neither can carry the note. The human label is a constant for the CLI renderer, which does not exist yet.

The five stale inherited descriptions named by inventory79 (installation_observation.rs, installation_session.rs, read_premise.rs, native_read_session.rs, installation_fence.rs) are unchanged here; the fix is a description override in a later contract successor, as 468a did.

The eight effective description overrides stay bound by stable file path, all inherited from the selected rows, with parent inventory79. The projection helper is the inventory79 helper, unchanged. Run it with python3 -I -B. evidence/build_v80.py rebuilds inventory80 and successor.json deterministically. The selected product verifier is unchanged.
