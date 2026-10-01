# First trust acceptance producer inventory113

Adds exactly two files to inventory116 (unit X4a, selected at product a34dc6b):
- crates/security/src/trust/trust_bootstrap.rs
- crates/security/src/trust/trust_bootstrap_tests.rs

It keeps all 843 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 845 planned files. No crate or dependency edge is added: security's trust module already reaches custody and the platform crate. The rows are unit X4B-a, law X4B r5 items 2 to 6 and 10.

- **trust_bootstrap.rs (service).** current_trust_admission.rs's macOS child module, beside floor_publication.rs. It is the producer of first trust acceptance from the embedded bootstrap payload, publishing through floor_publication's shared protocol.
- **trust_bootstrap_tests.rs (test).** That module's `cfg(test)` child. It runs on ACL-scratch P0 installations, with test-signed releases produced into an InitialCore.

**Changes to existing rows.**
- `trust/initial_core.rs`: `BootstrapDocuments` also retains the revocation pair's stored bytes, which item 5 verified. `bootstrap_release` lends the anchor's root binding, the manifest and inventory pairs and the root chain's pairs. Its description ("law 463 r3–r8") was already incomplete after 463h and is listed for D1.
- `trust/core_authentication.rs`: the test builder signs component manifests before the catalog, and the catalog lists one release row per signed component. 463h judgment call 7 left the catalog's releases empty, and the retained reader's catalog join needs these rows. Three `Spec` knobs set the catalog's expiry, the list's issue time and the roots' expiry. Its description stays true.
- `trust/floor_publication.rs`: `may_create` also admits `trust/objects`, which P0's closed tree (law 467) omits, so the first acceptance creates it. `TrustWrite` gains crate-local accessors. Its description stays true.
- `trust/current_trust_admission.rs`: declares the child module. Its description ("It writes nothing") has understated the file since X4T-b's child module, and still does.
- `trust/role_machine.rs`: `bootstrap_sequence` dispatches item 4's PresentOrdinary, Clock and Revoke sequence through the private `decide`. Its description stays true.
- `trust_time.rs`: `evaluate_fresh_install` runs the unchanged S4 kernel on a record with no floor (S4 step 2). The `TimeAdmission` projection is shared. Its description stays true.

The understated descriptions (initial_core.rs and current_trust_admission.rs) go to the description-only successor D1, as with earlier rows. An additive successor carries every inherited row by value.

**Order.** Its parent is the inventory the real product lock selects: inventory116 (unit X4a) at product a34dc6b. It was first built on inventory114 (unit X9-0) at daa7b01, and Grok accepted that candidate at r1. X8a (inventory117, c2352ae) and then X4a (inventory116, a34dc6b) integrated, so evidence/build_v113.py rebuilt it on each in turn with the same two rows, whose descriptions follow r2's RF-1 fix. The PRIOR table has one entry for each parent. The number 113 sits below its parent's 117; succession is by the lock's parent pin, not by number. The builder reads the parent from the lock. It refuses to write over any path git already tracks, and refuses while a lock selects inventory113. Reruns reproduce the same bytes.

**Projection.** The sixteen effective description overrides bound to inventory116, which are carried unchanged from inventory117 back to inventory81, stay bound by stable file path, with parent inventory116. verify_projection.py is inventory116's helper with only its comment corrected, and it runs against the real lock at a34dc6b. evidence/verify_scratch.py appends inventory113 in memory over the worktree's lock, with a synthetic review and assent.
