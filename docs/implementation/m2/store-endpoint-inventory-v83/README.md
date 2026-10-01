# Store endpoint inventory83

Adds exactly two sources to inventory82 (unit X10a, committed in arch and under review):
- crates/security/src/custody/store_endpoint.rs
- crates/security/src/custody/store_endpoint_tests.rs

It keeps all 754 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 756 planned files. No crate or dependency is added. The rows are unit X3a-1, law X3a items 1, 2, 3, 5 and 7.

- store_endpoint.rs (composition) admits `SelectedStoreEndpoint` from the values one session already read once. It reads no file, checks the endpoint in memory on the session's ledger, and grants only the base of a later owner §8 binding. Its producers are the ordinary writer's admission and the read session. The creator path produces none (law X3a r4).
- store_endpoint_tests.rs (test) checks it on scratch homes with a creator-published P0, and pins that 468c's route produces no endpoint.

**Order.** This successor depends on inventory82, so it integrates after X10a, the X10b contract successor and inventory82. evidence/build_v83.py refuses to write over any path git already tracks.

**Changes to existing rows.** The unit's other changes edit existing rows; no row is added for them:
- **Write gate (installation_admission.rs).**
  - Its required files keep their full metadata sample.
  - Step 2 reads the pair, marker, node chain and trust current record once (the last with its own 4 MiB bound) and keeps their decoded values.
  - Step 5 rechecks those samples instead of reading again.
  - At most 64 lineage nodes are read; past that, the budget row.
  - New incomplete kinds `Core` and `CurrentStore`, a `StateSchemaUnsupported` refusal, and the gate's own ledger kept for one more recheck.
- **Observation session (installation_session.rs).** The same rules on the read side. It also records the core and C.store findings and keeps the endpoint values of a complete I.
- **Read session (installation_read.rs).** Gains `store_endpoint`.
- **Ordinary writer (ordinary_writer.rs).** Keeps its gate and gains `admit_store_endpoint` / `StoreAdmittedWriter`.
- **Read premise (read_premise.rs).** Gains `selected_core`.
- **Doctor (installation_doctor.rs, host doctor_report.rs).** Two findings, with subjects `installation-incomplete:core` and `installation-incomplete:current-store` and their fixed remedies.
- **Termination rows (security and host installation_termination.rs).** The `STATE.SCHEMA_UNSUPPORTED` row: request-rejected, exit 2, `REQUEST.SCHEMA_MAJOR_UNSUPPORTED`.
- **Trust current record (trust/native_current.rs, root_payload.rs, trust.rs).** Exposes the record's own decoder and bound for `C.store`.
- **Identity (store_lineage.rs).** `SuppliedChain::into_nodes`.
- **Test fixtures.** `installation_read_fixture.rs` gains `select_generation`. One existing observation test now expects an in-place rewrite of a read required file to be refused.

**Descriptions that now understate their files.** These stay true, but do not mention X3a's additions:
- installation_admission.rs, installation_session.rs, installation_read.rs, ordinary_writer.rs, installation_doctor.rs and native_current.rs;
- the two installation_termination.rs rows (they name only 468's rows);
- doctor_report.rs.

They are carried unchanged here. The direct rows can be refreshed by a later description-only contract successor, as 461b did. installation_session.rs, read_premise.rs and store_lineage.rs are inherited overrides, and wait for tooling follow-up VD1.

**Projection.** The sixteen effective description overrides bound to inventory82 (carried unchanged from inventory81) stay bound by stable file path, with parent inventory82. verify_projection.py is inventory82's helper, with only its comment corrected. evidence/build_v83.py rebuilds inventory83 and successor.json deterministically.

**How the checks were run.** The live product lock still selects inventory81.
- **Projection check.** The helper requires the lock's last inventory successor to be inventory82. evidence/scratch_lock.py writes such a lock outside both repositories: the live lock with X10b and inventory82 appended exactly as integration would append them. verify_projection.py then runs against it; verification.json records the command.
- **Scratch verify.** evidence/verify_scratch.py appends X10b, inventory82 and inventory83 in memory, each with a synthetic review and assent. It then runs the real verify_design, which must select inventory83.
