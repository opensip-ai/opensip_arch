# Read migration inventory79

Adds exactly four sources to selected78:
- crates/security/src/custody/installation_read.rs
- crates/security/src/custody/installation_read_tests.rs
- crates/security/src/custody/installation_read_fixture.rs
- crates/security/src/installation_observation_tests.rs

It keeps all 741 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 745 planned files. No crate or dependency is added. The rows are unit 458c-b2, the consumer migration of law 458c r5 item 8.

- installation_read.rs (service) is the read session. It keeps the complete I the observation session admitted, with that session's one ledger. Every capture and recheck is charged before it runs. Captures open only through the retained I and its retained descendants. A capture's failures are values, so the full recheck (item 5 step 4) runs after every capture, over the fence, the observation's required files and every file captured since. Any refusal latches the session. It lends the trust readers a held-fence view and charges their retained budget to the same ledger.
- installation_read_tests.rs (test) pins the migration in the readers' own sources, and checks the ledger sink and the held-fence view.
- installation_read_fixture.rs (test) publishes a real P0 under a scratch H and holds read fences on it.
- installation_observation_tests.rs (test) ports the readers' capture tests to the read session.

The unit's other changes edit existing rows:
- installation_observation.rs: `InstallationReadFence` is rebuilt on the read session. `acquire()` replaces `try_acquire(supplied_groups)`. The public capture API and `ProvisionalHeldFile` are unchanged in shape. Its test module moves to installation_observation_tests.rs.
- custody.rs gains the module wiring.
- custody/installation_fence.rs gains the `HeldFence` view, implemented by the supplied fence (supplied-root tests) and the read session, and a `Session` refusal.
- custody/installation_session.rs keeps its observation's account and fence identity, and gains `retain`.
- trust/native_read_session.rs, native_current.rs, native_record_capture.rs, native_census.rs, native_profile_census.rs and native_platform.rs take the `HeldFence` view instead of the supplied fence. The trust read session's budget charges the read session's ledger through `Budget::charged` (retained_metadata_index.rs).
- custody/installation_publication_tests.rs reads the published I through the read session.

The host and storage readers (installation_records.rs, installation_selection.rs, installation_lineage.rs, installation_trust.rs, store_root/native_marker.rs) need no source change: they already take `&InstallationReadFence`.

Five inherited descriptions are now partly stale:
- installation_observation.rs says "under a native installation fence";
- installation_session.rs ends "no consumer uses it yet";
- read_premise.rs ends "no read path uses it yet";
- native_read_session.rs says "borrowed native fence";
- installation_fence.rs does not name the held-fence view.

Inventory successors keep inherited rows by value, so the fix is a description override in a later contract successor, as 468a did.

The eight effective description overrides stay bound by stable file path. All are inherited from the selected rows, with parent inventory78. The projection helper is the inventory78 helper, unchanged. Run it with python3 -I -B. evidence/build_v79.py rebuilds inventory79 and successor.json deterministically. The selected product verifier is unchanged.
