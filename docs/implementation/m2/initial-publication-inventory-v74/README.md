# Initial publication inventory74

Adds exactly three sources to selected73:
- crates/security/src/custody/installation_publication.rs
- crates/security/src/custody/installation_publication_tests.rs
- crates/security/src/custody/installation_stage.rs

It retains all 728 existing rows by value, the packages and dependencies, the pending decisions, and the carried unresolved obligations. That makes 731 planned files. No new crate or dependency. The rows are units 467a and 467b under law 467 (items 1 to 11 and "The P0 tree"), owner.md §1a step 6 and §2 to §6, and law 465 items 9 to 11. installation_stage.rs (service) is S0 to S7: it rechecks and consumes the permit, rechecks the handed-off storage, draws S and one clock sample, creates the private stage and P0's 14 directories and 11 files as effects with reserved postchecks, locks the fence, validates the whole stage, barriers the stage and its parent again, and rechecks every owner. installation_publication.rs (service) is S8 to S10, the outcomes, the handoff and the one top-level composition: the exclusive rename with its prepaid owner rechecks, the LostRace, NotPerformed and Indeterminate routes, the I-parent barrier and post-publication rechecks, and a Published value with no handle, lock or authority. installation_publication_tests.rs (test) is the single combined test file for both, on scratch chains only. The unit's other changes (the handoff storage and in-scope actor rechecks, the in-scope core, platform and name rechecks, the creation clock projection, and the manifest's reread) edit existing rows whose descriptions still hold. Library only: no command is wired, and the creator stays disabled.

The five effective description overrides stay bound by stable file path. Rows after the new ones move down. The projection helper is byte-identical to the inventory64 to 73 helper. Run it with python3 -I -B. The selected product verifier is unchanged.
