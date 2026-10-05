# J3a inventory139 (the durable entry)

Adds exactly sixteen rows to inventory138 (unit E2a). They belong to unit **J3a** of law M3-J1 r6 (`docs/implementation/m3/host-pipeline-j/PROPOSAL-r6.md`, accepted; items 2, 3 and 14), the platform and security code of the durable entry: `RequestIdentity` and `ExecutionIdReservations` (item 2), the durable entry with its presence probe, two-slot attempt and `EntryRefusal` (item 3), the code of successors S2 to S7 (468 r6, X1 r2, 464 r3, X3a r6, X4B r6, X2 r10) and `CommitSession::open`'s reservation (X3d r9 S10.1).

**Parent: inventory138, integrated.** The lead's rule stages J3a's candidate last, on the highest existing candidate. That is E2a's inventory138 (`syntax-lane-e2a-inventory-v138/`), which the lock at product `b7b87b7` selects (J2a's inventory137 integrated at `174aa30`, then E2a's inventory138 at `b7b87b7`). **If another unit (E2s may) stages inventory139 first, this candidate must be rebuilt as the next version on that one**, with its record, subject, staged lock and review pins.

All sixteen rows are compile-fail cases of law X8 r3's refusal suite in the existing `opensip-host` package, under `crates/host/tests/refusal/cases/`, each with a row in `crates/host/tests/admission_tests.rs`'s case table:
- **`RequestIdentity`** (law M3-J1 r6 item 2, control J-C4) and **`ReservedExecutionId`** (item 2, J-C4b; X3d r9 S10.7), the two identity types J3a exports from `opensip-platform`: X8 r3 item 3's full capability set for an exported type, a literal from bytes, `Default`, `Deserialize`, conversions from bytes and from text (group D), `Clone` (E) and `Serialize` (G). Fourteen rows.
- **`platform_reserved_execution_id_injected_absent.rs`** (group F, item 3a's census): `ReservedExecutionId`'s one constructor from text, the crash matrix's `inject-id` reservation at `x3d.session.execution-draw`, lives in platform's `crash_barrier` module, which exists only under the test-only `crash-matrix` feature.
- **`security_commit_session_open_reserved.rs`** (group F, J-C4b): `CommitSession` accepts no other ExecutionId, not even a reserved one.

It keeps all 995 existing rows of inventory138 by value, along with the packages and their edges, the pending decisions and the carried unresolved obligations, for 1011 planned files.

**Planned rows changed.** Seventeen planned rows change bytes (`plannedRowsChanged` in `successor.json`): platform's `lib.rs` and `crash_barrier.rs`; host's `request.rs` and `tests/admission_tests.rs`; security's `initial_installation.rs`, `custody/installation_routing.rs`, `read_premise.rs`, `ordinary_writer.rs`, `commit_session.rs`, `installation_stage.rs` and `installation_read_fixture.rs`; and six security test files. No description becomes false, but several become incomplete (for example, `initial_installation.rs` still says "the one pre-installation attempt per process", which X1 r2 item 7 makes a two-slot sequence on the creator-class path). J3a's request routes them to the lead for a description-only contract successor, as X1b was planned. No inventory row's bytes change here: inherited rows are equal by value.

**No new edge, crate or dependency.** The rows are in `opensip-host`, whose tests already compile against `opensip-platform` and `opensip-security`. No manifest, `Cargo.lock` or dependency policy changes. The builder asserts that every added path is new and every changed path is planned.

**Order.** `evidence/build_v139.py`:
- takes the lock (by default the product checkout's), which must select inventory138 with E2a's successor record;
- checks every meaning the lock binds to the parent before carrying it;
- writes only its two paths;
- refuses tracked paths, and refuses while a lock selects inventory139.

Reruns reproduce the same bytes for a given lock. **At integration,** rerun the builder and verifiers against the real lock, and replace J3a's two placeholder pins in the staged lock with the accepted review and the completed unit record.

**Projection: one hundred and three rows.** Once inventory139 is selected, inventory138 becomes an ancestor, and every description meaning a lock selecting inventory138 binds to it is inherited by stable file path: its one hundred and three inheritance rows, as inventory138 projected them. No bound contract successor has a passage override or supersession on inventory138, and none is folded. Eighty-four projected rows, sorted after the inserted paths, move.

- `verify_projection.py` is inventory138's helper with its comment updated for this parent. Against the real lock at `b7b87b7`: PASS, 103 rows, 518 corruptions refused (`verification.*`, `verifier-anchor.json`).
- `evidence/stage_lock_j3a.py` stages the lock change in the J3a worktree, as E2a staged inventory138: HEAD's `design-lock.json` plus the inventory139 entry, with the one hundred and three inheritance rows re-parented to inventory139. The parent, candidate, record and subject pins are real. J3a's review and assent pins are `SCRATCH-J3A/` placeholders, which integration replaces with the accepted review and the completed unit record. J3a has no contract successor.
- `evidence/verify_scratch.py` checks the staged lock (or, on an unstaged worktree, applies the same change in memory). It requires the staged lock to equal HEAD's plus exactly that entry and that inheritance, serves a synthetic review and assent for J3a's placeholders, runs the worktree's real `verify_design` on HEAD's lock and on the lock with inventory139, and requires verify_design's own projected inheritance to equal the record's. It also checks that plain `verify_design` refuses the staged lock at the placeholder (`SCRATCH-J3A/review.json`), as it must until integration.
- `evidence/drift_scratch_j3a.py` runs the worktree's real public generator (`generate_contracts.generate`, the selected rebuild-02 generator, write false) with the same synthetic review and assent served in memory, as E2a's drift gate did. It must pass with `changed: []`: J3a changes no generation input.
