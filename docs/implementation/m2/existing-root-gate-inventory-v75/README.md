# Existing-root gate inventory75

Adds exactly two sources to selected74:
- crates/security/src/custody/installation_admission.rs
- crates/security/src/custody/installation_admission_tests.rs

It retains all 731 existing rows by value, the packages and dependencies, the pending decisions, and the carried unresolved obligations, for 733 planned files. No new crate or dependency. The rows are unit 468b under law 468 r5 items 1 to 5 and owner.md §5.

- installation_admission.rs (service) is the durable write gate. On one failure-latching ledger it runs the charged, retained chain walk (step 0), with InitialPlatform's premise only on the root-to-H prefix, Library and Application Support. It takes the no-follow nonblocking fence lock through the retained I handle (step 1). It runs the recheck set under the held fence, I's barrier and I's parent's barrier, and the same recheck reserved with the barriers (steps 2 to 5).
- installation_admission_tests.rs (test) runs on scratch chains only.

The unit's other changes edit existing rows whose descriptions still hold:
- custody.rs gains the module wiring;
- initial_installation.rs shares its account admission predicate;
- installation_publication.rs makes its test-only composition visible to the sibling tests.

Library only: no command is wired, and the creator stays disabled.

Eight effective description overrides stay bound by stable file path. Five are inherited, and three are 468a's direct overrides on inventory74. Rows after the new ones move down by two. The projection helper is the inventory74 helper with the row count changed from five to eight. Run it with python3 -I -B. The selected product verifier is unchanged.
