# Operation handoff and journal composition inventory111

Adds exactly four sources to inventory108 (unit X3b-4, selected at product 97f630a). Round 1 was reviewed on inventory112 (unit X3d-0, product f1b8321); the unit was first built on inventory110 (unit X2d, product 9d51f33):
- crates/security/src/custody/operation_handoff.rs
- crates/security/src/custody/operation_handoff_tests.rs
- crates/security/src/journal_store/carrier_operation.rs
- crates/security/src/journal_store/carrier_operation_tests.rs

It keeps all 793 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 797 planned files. No crate or dependency edge is added: both modules use only `opensip-identity` and `opensip-platform`, which security already depends on. The rows are units X2e and X3b-3 together, as X3b's unit plan says: law X2 r8 item 7a (the checked operation handoff), composed with law X3b r10 items 1, 3, 3a, 4 and 11 (the floor step at the lease-free point, the carrier start inside the handoff, the end step in the operation's end path, including step 3's rollover from X3b-4 after a capacity exhaustion). Round 2 answers Grok r1 RF-1: both standing sentences and both new production descriptions name law X3b r10, and the handoff description states that a closed attempt ledger does not enter the end step. Round 3 answers Grok r2 RF-1 (a code finding; the inventory was accepted): the rollover's outcome is kept outside the attempt-ledger charge; the handoff test description lists the new cases, and the journal half's description names its test-only re-exports.

- **operation_handoff.rs (composition).** custody.rs's macOS module `operation_handoff`, beside X2d's `namespace_lease`, so the gate's, the receipt's and the namespace's private owners stay crate-private. It holds the handoff (`begin`), `ProjectOperation`, owner §8's `OperationBinding`, `CarrierPlace` (the only input of the carrier location's production constructor), the end path (with X3b-4's rollover after `JournalOutcome::Exhausted`) and the refusal rows.
- **operation_handoff_tests.rs (test).** Its `cfg(test)` child module: the composition on scratch homes.
- **carrier_operation.rs (composition).** journal_store's carrier-floor child module `operation`: X3b-3's journal half (the production `CarrierLocation::admitted`, the floor step keeping its observation, creation and the start inside the handoff, the end copy, and the end step from step 3 through X3b-4's `end_step_after_exhaustion`), with a `cfg(test)` helper that plants a committed tail by X3b-2's reserved-slot technique.
- **carrier_operation_tests.rs (test).** Its `cfg(test)` child module, on X3b-1's scratch carrier fixture.

**Changes to existing rows.**
- `custody/namespace_lease.rs`: `NamespaceTarget::lease_free` (the holder and N at the lease-free point), `FencedNamespace::into_parts` and `NamespaceParts` (the move), `pub(super)` on the namespace, lease and recheck helpers, and a footprint argument to the subject's recheck. The description stays true; it already names X2e as the handoff.
- `custody/first_registration.rs`: `Footprint { Exact, Started }` and `recheck_registered_with`, so a registered subject's namespace can be rechecked after X3b's carrier start (X2d review judgment call 5); `Owner::Trust`; `Step::Handoff`. Exact stays the rule for registration and X2d. The description stays true: that file still takes no lease and builds no handoff.
- `custody/first_registration_tests.rs`: one test of the two footprints. The description is not refreshed (it lists cases; a description-only successor can add it).
- `custody/ordinary_writer.rs`: `begin_operation`, `join_store_endpoint`, `attempt_step` and `into_parts`. Its description was already out of date after X3a-1, X2c and X2d and stays so; the same later description-only successor named at inventory97, 101, 102, 105 and 110 must refresh it.
- `custody/read_premise.rs`: the write receipt's `charge` (one step on the attempt ledger, with the qualification lent beside it) and `is_closed`. Its description was already out of date after X1 (the write receipt) and stays so, for the same successor.
- `custody/installation_admission.rs`: `DurableInstallation::into_handoff` and `Chain::installation_id`. The description stays true.
- `custody/installation_session.rs`: the bounded fence wait becomes `pub(super)`, shared by the end step's fence retake. The description stays true.
- `journal_store.rs` and `journal_store/carrier_floor.rs`: the `operation` module declaration (after X3b-4's `rollover`) and its crate re-exports (after X4T-b's `publish_private_file`). The descriptions stay true; carrier_floor's "no production constructor until X3b-3" is now met by X3b-3's child module.
- `custody.rs`: declares the `operation_handoff` module. The description stays true.

- `journal_store/carrier_rollover.rs` (X3b-4's): one `cfg(test)` entry, `end_step_after_exhaustion_at`, the same rollover and end with the module's test points, so the composition owner's tests reach X3b-4's undetermined and step points through the real end path. No production line changes; the description stays true.

No other existing source changes.

**Order.** This successor's parent is the inventory the real product lock selects: inventory108 (unit X3b-4) at product 97f630a. evidence/build_v111.py reads the parent from the lock and maps inventory108 to the successor record that bound its sixteen rows. It writes only its own two paths, refuses to write over any path git already tracks, and refuses while a lock selects inventory111. The number 111 was assigned before X3d-0 took 112 and X4T-b and X3b-4 took 106 and 108; the chain stays linear by parent (v110, v112, v106, v108, then v111).

**Projection.** The sixteen effective description overrides bound to inventory108 (carried unchanged back to inventory81) stay bound by stable file path, with parent inventory108. verify_projection.py is inventory110's helper with only its comment corrected to name its parent. It runs against the real lock at 97f630a, which selects inventory108. evidence/verify_scratch.py appends inventory111 in memory over the real lock, with a synthetic review and assent; it finds the architecture root from its own location.
