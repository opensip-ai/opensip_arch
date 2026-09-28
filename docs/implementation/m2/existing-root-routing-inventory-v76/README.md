# Existing-root routing inventory76

Adds exactly four sources to selected75:
- crates/host/src/installation_termination.rs
- crates/security/src/custody/installation_routing.rs
- crates/security/src/custody/installation_routing_tests.rs
- crates/security/src/installation_termination.rs

It retains all 733 existing rows by value, the packages and dependencies, the pending decisions, and the carried unresolved obligations, for 737 planned files. No new crate or dependency: the host already depends on security and contracts. The rows are unit 468c under law 468 r5 items 1, 3 and 6.

- security installation_termination.rs (model) is the closed vocabulary of item 6 rows, re-exported for the host.
- installation_routing.rs (composition) ends the creator act on Published, LostRace or NotPristine, drops the attempt, and enters a fresh durable write gate with only this invocation's InitialPlatform. It maps every refusal of units 459 to 468 to its row by exhaustive matches with no wildcard arm.
- installation_routing_tests.rs (test) runs on scratch chains only, plus the live composition, which refuses at InitialCore F0 in a development build.
- host installation_termination.rs (adapter) projects each row onto its D9 class, exit, error code, fault cause, domain detail and subject.

The unit's other changes edit existing rows whose descriptions still hold:
- security lib.rs re-exports the row vocabulary;
- custody.rs gains the module wiring;
- trust.rs and trust/root_payload.rs re-export the two existing producers to custody;
- host lib.rs exposes the projection.

Library only: no command is wired, and the creator stays disabled.

The eight effective description overrides stay bound by stable file path, all inherited from the selected rows with parent inventory75. The projection helper is the inventory75 helper unchanged. Run it with python3 -I -B. evidence/build_v76.py rebuilds inventory76 and successor.json deterministically. The selected product verifier is unchanged.
