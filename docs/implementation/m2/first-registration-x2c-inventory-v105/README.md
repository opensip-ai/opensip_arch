# First project registration inventory105

Adds exactly two sources to inventory104 (unit X12a, selected at product b642c45):
- crates/security/src/custody/first_registration.rs
- crates/security/src/custody/first_registration_tests.rs

It keeps all 783 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 785 planned files. No crate or dependency edge is added: the module uses only `opensip-identity` and `opensip-platform`, which security already depends on. The rows are unit X2c: law X2 r8 item 6 (first registration, the registry replacement primitive, and the create-or-admit of `I/host`, `I/host/projects` and `.opensip`), with item 8's rows and item 9's budget for those steps, and the write-gate entries for items 2 to 5 and 6a that X2b-1 left to this unit.

- **first_registration.rs (composition).** custody.rs's macOS module `first_registration`, beside X2b's `project_admission` and `git_tracking`, so the gate's, the admission's and the chain's private types stay crate-private. It holds the preconditions, the replacement primitive, the namespace publication, `.opensip` and the marker, the step 6 recheck, `RegisteredProject`, the refusal rows, and the write-gate entries.
- **first_registration_tests.rs (test).** Its `cfg(test)` child module: X2c's cases on scratch homes.

**Changes to existing rows.**
- `custody/ordinary_writer.rs`: `OrdinaryWriteAdmission` gains `admit_project_root`, `observe_project_tracking(_with)`, `register_first_use(_with)` and `recheck_registered`. Each runs on the gate's ledger under the held fence, then rechecks the write receipt; any refusal spends the gate. Its description ("grants exactly what DurableInstallation grants … no store, trust, project, id, grant or commit standing") was already incomplete after X3a-1's `admit_store_endpoint`; it is now more so, since the writer can register a project. An inventory successor carries rows by value, so the same later description-only contract successor that inventory97, inventory102 and inventory101 named must refresh it.
- `custody/installation_admission.rs`: `DurableInstallation` gains crate-internal accessors (`installation_directory`, `home_spelling`, `uid`) and `advance_registry(from, to)`, which moves the gate's retained `project-registry.v2` sample only when it still equals the reconfirmed predecessor (item 6: R changes only through a confirmed publication). `DurableWriteGate` gains `scope`, `is_spent` and `spend` on its own ledger. The description stays true; it does not name the new methods.
- `custody/project_admission.rs`: item 5's `RegistryCapture` now retains the descriptor it read (R0), as item 5 says, and the admission can be moved into its parts. Some helpers and constants become `pub(super)`. The description stays true.
- `custody.rs`: declares the `first_registration` module. The description stays true.
- `platform/src/lib.rs`: adds `project_id_draw()`, one complete 32-byte OS CSPRNG draw per ProjectId candidate. The description stays true.

No other existing source changes.

**Order.** This successor's parent is the inventory the real product lock selects: inventory104 (unit X12a) at product b642c45. evidence/build_v105.py reads the parent from the lock and maps inventory104 to the successor record that bound its sixteen rows. It refuses to write over any path git already tracks, and while a lock selects inventory105.

**Projection.** The sixteen effective description overrides bound to inventory104 (carried unchanged from inventory101 back to inventory81) stay bound by stable file path, with parent inventory104. verify_projection.py is inventory104's helper with only its comment corrected to name its parent. It runs against the real lock at b642c45, which selects inventory104. evidence/verify_scratch.py appends inventory105 in memory over the real lock, with a synthetic review and assent.
