# Read observation inventory78

Adds exactly two sources to selected77:
- crates/security/src/custody/installation_session.rs
- crates/security/src/custody/installation_session_tests.rs

It keeps all 739 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 741 planned files. No crate or dependency is added. The rows are unit 458c-b1, under law 458c r5 items 5, 6, 7 and 11.

- installation_session.rs (service) is the observation path. It reuses the write gate's step 0, step 1 and recheck code; that code is shared, not copied. It takes no barrier. The fence wait is the bounded, fully reserved one of item 11. The member reads are charged before they run, and the full recheck runs over every captured file, including after a failed read. Structural findings are exposed for doctor (458c-c). Refusals take exactly the write gate's rows. Library only: no consumer uses it yet (458c-b2).
- installation_session_tests.rs (test) runs on scratch homes with a creator-published P0, signed test trees and an injected wait clock.

The unit's other changes edit existing rows whose descriptions still hold:
- custody.rs gains the module wiring;
- custody/installation_admission.rs gives its step 0 walk, fence opening, recheck set and private-file judgment to the session through shared helpers. The gate's behavior is unchanged, and its tests pass unchanged.
- custody/read_premise.rs lends its qualification and rechecks together through `split`.
- platform locks.rs gains `FileLock::try_acquire_retaining`, which hands the descriptor back when busy.
- platform work_reader.rs gains `read_bounded_observed`, whose ordinary read outcomes are values.
- platform filesystem/descriptor_acl_capture.rs gains `capture_descriptor_acl_observed`, whose native capture failures are values, so step 4 still runs after one (Grok 458c-b1 r1 RF-1).
- platform lib.rs and filesystem.rs export them.

One inherited description is now partly stale. read_premise.rs ends "Library only: no read path uses it yet", but the session now uses it. Inventory successors keep inherited rows by value, so the fix is a description override in a later contract successor, as 468a did.

The eight effective description overrides stay bound by stable file path. All are inherited from the selected rows, with parent inventory77. The projection helper is the inventory77 helper, unchanged. Run it with python3 -I -B. evidence/build_v78.py rebuilds inventory78 and successor.json deterministically. The selected product verifier is unchanged.
