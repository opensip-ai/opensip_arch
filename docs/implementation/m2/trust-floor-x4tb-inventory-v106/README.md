# Trust floor publication inventory106

Adds exactly two files to inventory112 (unit X3d-0, selected at product f1b8321):
- crates/security/src/trust/floor_publication.rs
- crates/security/src/trust/floor_publication_tests.rs

It keeps all 789 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 791 planned files. No crate or dependency edge is added: security's trust module already reaches custody, journal_store and private_access. The rows are units X4T-a2 and X4T-b together, law X4T r9 items 1, 2, 7, 8, 11 and 12.

- **floor_publication.rs (service).** current_trust_admission.rs's macOS child module: the retained trust current owner, the fenced first read with its S4 write-ahead floor publication, rollback check 3, and the publication protocol shared with X4B-a.
- **floor_publication_tests.rs (test).** That module's `cfg(test)` child, on ACL-scratch installations with X4T-0's signed store.

**Changes to existing rows.**
- `trust/current_trust_admission.rs` (X4T-a2 and X4T-b): `check_accepted_by` opens each out-of-chain `accepted.by` event by reference (at most six); the view carries the capsule's floors and, on a fenced non-report read, the S4 proposal; rollback checks 1 and 2; the `trust-rollback` and `required-files-changed` rows; the child module. Its description ("checks each accepted role's accepted.by against the loaded events of that role … It writes nothing; the write-ahead floor is X4T-b's") now understates the file.
- `trust/current_trust_admission_tests.rs`: the new `check_accepted_by` signature. Its description stays true.
- `trust/accepted_store_fixture_tests.rs`: the source pin admits floor_publication_tests.rs under the same `cfg(test)` check as X4T-a's tests. Its description was already stale and is listed in EXIT-PLAN D1.
- `trust/proposed_time_input.rs`: the S4EvaluationInputV2 assembly moves into `assemble`, which `prepare` now calls (same bytes). Its description stays true.
- `custody/installation_admission.rs`: `CurrentStore` keeps the bytes of the gate's one `state.v1` read; `current_trust`, `advance_current` (which, like X2c's `advance_registry`, advances only from the predecessor sample the publication reconfirmed) and `observe_private_file`; `RequiredFile::metadata` is crate-visible. Its description now understates the file.
- `custody/installation_admission_tests.rs`: the owner-advance test through the gate. Its description now understates the file.
- `custody/installation_session.rs`: `decode_current` takes the read's bytes by value. Its description stays true.
- `journal_store.rs`: re-exports `carrier_floor::publish_private_file` crate-wide. Its description stays true.
- `trust.rs`, `trust/root_payload.rs`, `trust/ordinary_targets.rs`: re-export `ConfirmedCurrent` (and, under `cfg(test)`, the owner and `publish` for the gate's test). Their descriptions stay true.

The understated descriptions (current_trust_admission.rs, installation_admission.rs and its tests) go to the description-only successor D1, as with X3c-2's rows. An additive successor carries every inherited row by value.

**Order.** Its parent is the inventory the real product lock selects: inventory112 (unit X3d-0) at product f1b8321. It was first built on inventory104 at b642c45 and rebuilt on inventory105 (X2c, 0206ce8) for review r1; X12b (inventory109), X2d (inventory110) and X3d-0 (inventory112) then integrated, so evidence/build_v106.py rebuilt it on inventory112 with the same two rows (one PRIOR entry each). The number 106 sits below its parent's 112; succession is by the lock's parent pin, not by number. The builder reads the parent from the lock, refuses to write over any path git already tracks, and refuses while a lock selects inventory106. Reruns reproduce the same bytes.

**Projection.** The sixteen effective description overrides bound to inventory112 (carried unchanged from inventory97 back to inventory81) stay bound by stable file path, with parent inventory112. verify_projection.py is inventory104's helper with only its comment corrected. It runs against the real lock at f1b8321, which selects inventory112. evidence/verify_scratch.py appends inventory106 in memory over the worktree's lock, with a synthetic review and assent.
