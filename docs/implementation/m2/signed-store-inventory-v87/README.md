# Signed accepted-store inventory87

Adds exactly two test-only sources to inventory84 (unit X2a, committed in arch, under review):
- crates/security/src/trust/accepted_store_fixture.rs
- crates/security/src/trust/accepted_store_fixture_tests.rs

It keeps all 758 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 760 planned files. No crate or dependency is added. The rows are unit X4T-0, law X4T r4 item 13.

- accepted_store_fixture.rs (fixture) is declared only under `cfg(test)` in trust/root_payload.rs. On a real P0 publication from the product `initial_publication` producer, it constructs one retained publication: signed root, revocation, catalog and payload manifest (public test-only quorum seeds), the payload metadata closure, a bootstrap operation, S4 time evidence with a signed time source, root and metadata admission records, a list revocation history, an S4 clock-write event, per-role acceptance and conditioning role events with their role-change and publication-event rows, and the retained capsule and descriptor. Each record passes its closed shape before it is written.
- accepted_store_fixture_tests.rs (test) shows that `current_record_bindings::bind`, `publication_events::bind_events`, `bind_retained_head` and `capture_p2` accept the generated store, that the documents carry real quorum signatures, and that no production source names the constructor.

**Numbering.** Inventory85 (unit X3b-1) and the reserved inventory86 (unit X4T-a) are siblings, not parents. This unit's number and parent are provisional; it is renumbered and rebuilt on the real predecessor at integration. evidence/build_v87.py refuses to write over any path git already tracks.

**Changes to existing rows.** trust/root_payload.rs gains only the `cfg(test)` `accepted_store_fixture` module declaration; its description stays true. No other existing source changes.

**Projection.** The sixteen effective description overrides bound to inventory84 stay bound by stable file path, with parent inventory84. verify_projection.py is inventory84's helper with only its comment corrected. It runs against a scratch lock (the real lock at 99f1c35 with inventory84 appended in memory, written by `evidence/verify_scratch.py --lock-out`), because the real lock selects inventory83. evidence/verify_scratch.py appends inventory84 and then inventory87 in memory over the real lock, with synthetic reviews and assents.
