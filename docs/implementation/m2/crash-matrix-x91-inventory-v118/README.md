# Crash-matrix support inventory118

Adds exactly eight files to inventory128 (unit X11a, selected at product 099de03, with D1's thirty-nine overrides and D2's four supersessions already folded into its fifty-five inheritance rows):
- crates/security/src/crash_matrix_support.rs
- crates/security/src/crash_matrix_support/post_state.rs
- crates/security/src/crash_matrix_support/run_record.rs
- crates/security/src/crash_matrix_census.rs
- crates/security/src/crash_matrix_sites.rs
- crates/storage/src/crash_matrix_support.rs
- crates/storage/src/ledger_store/project_commit_census.rs
- crates/host/src/crash_matrix_support.rs

It keeps all 949 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 957 planned files.

**No new edge.** The `crash-matrix` feature forwards only along edges the parent already declares (security to platform; storage to security and platform; host to storage, security and platform). A feature is not a package row, and `check_package_edges.py` reads only dependency tables. The builder asserts each forwarded edge is declared in the parent.

The rows are unit X9-1, law X9 r2 item 12 (r1's unit, with r2's scripted wall clock): the feature in security, storage and host; the `crash_matrix_support` modules; the pinned shared fixture-gate site list (law X8 r3 item 4b); barrier points at the integrated sites; the post-state capture, normalizer and run writer; the scripted wall clock; and the census of the integrated path.

- **crash_matrix_support.rs and its two children (service).** Security's feature-only, `doc(hidden)` surface: the synthetic installation, X4T-0's accepted store, the revocation helper over the shared fenced publisher, the carrier fixtures, and the post-state and run-record writers. Nothing returns an authority type.
- **storage and host crash_matrix_support.rs (service).** Re-exports only: the shared gates live in security.
- **crash_matrix_census.rs and project_commit_census.rs (test).** Feature-gated census children and verified kills; pinned censuses of 277 points (kill set 437) and 46 points (kill set 70).
- **crash_matrix_sites.rs (test).** The source pin of every test-feature site, in every security test build.

**Changes to existing rows.** Every row stays by value. Where a lock inheritance row overrides a row, the text judged here is the effective description. Out-of-date descriptions are left for the next description-only successor, as earlier units left theirs.
- `crates/{security,storage,host}/Cargo.toml`: a `[features]` table (`crash-matrix`, forwarding; security also declares an empty `scenario-fixtures` so the joint predicate is a known cfg). Their descriptions stay true.
- `crates/{security,storage,host}/src/lib.rs`: the compile guard, the feature-only `pub mod crash_matrix_support` (`doc(hidden)`) and the test modules; `test_scratch`'s private parent is named by an entropy draw instead of a wall reading (law X9 r2 item 3: a matrix child takes no OS wall reading). Their descriptions stay true.
- Protocol sources with barrier points or scopes, each a no-op without the feature: `custody/{installation_admission,first_registration,namespace_lease,operation_handoff,commit_session}.rs`, `journal_store/{carrier_append,carrier_floor,carrier_start,carrier_operation,carrier_rollover}.rs`, `trust/floor_publication.rs`, `storage/src/ledger_store/{project_ledger,project_commit}.rs`. `installation_admission.rs` gains a private `FenceLock` so that the fence's unlock on every path, including a refusal's drop, is named `x2.fence.release`. Their descriptions stay true.
- Shared fixture gates widened from `cfg(test)` to the joint predicate: `trust/{initial_core,initial_platform,core_authentication,root_payload,current_trust_admission,ordinary_targets}.rs`, `trust.rs`, `initial_installation.rs`, `custody.rs`, `custody/{installation_admission,installation_session,installation_publication,installation_parent,recovery_admission}.rs` (X6b's recovery admission walks the same `HomeSource::Fixture`). `trust/floor_publication.rs` gains the shared fenced publisher, and `custody/installation_read_fixture.rs` the shared producers. Descriptions stay true; the fixture file's says test support, which it remains.
- `journal_store.rs`, `journal_store/carrier_operation.rs`: the reserved-slot and inherited-carrier fixtures under `any(test, feature = "crash-matrix")`.
- `trust/accepted_store_fixture.rs`: unchanged from the parent (X4a's Spec extension). `trust/accepted_store_fixture_tests.rs`: its source pin accepts the joint predicate and the site pin's file. Its description ("declared only under cfg(test)") is out of date by that.
- `crates/platform/src/{crash_barrier.rs,crash_barrier/driver.rs,crash_barrier/self_tests.rs,clock.rs}`: law X9 r2 item 3's scripted wall clock (`OPENSIP_X9_CLOCK`, `ScriptedClock` on `ChildSpec`) and its self-tests. The driver's and barrier's descriptions are out of date by omission of the clock.
- `tools/check_crash_matrix.py` and its test: r2's `scripted-clock` label, the required runs' `clockEpoch`, the run's `clock` and children's `ordinal`. Their descriptions are out of date by omission.
- `apps/cli/tests/doctor_tests.rs`: the test-bridge pin narrowed to law X10 r4 item 5. Its description stays true.

**Order.** Its parent is the inventory the real product lock selects: inventory128 (unit X11a) at product 099de03. The number 118 was assigned by the lead; succession is by the lock's parent pin, not by number. It was first built on inventory125 (X7a, f097c5b) before any review; X6b, X4B-c, X6c, X11a, F6 and X7b then integrated (only X6b, X6c and X11a with inventories), the diff was moved onto 099de03 (with one more `HomeSource::Fixture` arm widened, in X6b's `recovery_admission.rs`, and F6's `churned` import in the widened `initial_platform` test module kept `cfg(test)`), and it was rebuilt on inventory128. The PRIOR table maps inventory125 to inventory128. `evidence/build_v118.py` reads the parent from the lock (the product checkout's `design-lock.json`, or a lock path as its one argument), checks each inheritance row against the lock before carrying it, writes only its two paths, refuses tracked paths and refuses while a lock selects inventory118. Reruns reproduce the same bytes.

**Projection.** The fifty-five effective description overrides the lock binds to inventory128 stay bound by stable file path: the sixteen carried from inventory81 onward and D1's thirty-nine, with D2's four supersessions already folded. Only their candidate selectors move, by the eight inserted rows. No contract successor bound at 099de03 names inventory128 as a supersession parent, so nothing new is folded (`supersessionsFolded: 0`).

`verify_projection.py` is inventory125's helper with its comment updated for this parent; it runs against the real lock at 099de03. `evidence/verify_scratch.py` appends inventory118 in memory over the worktree's lock and replaces the inheritance rows with the record's fifty-five, with a synthetic review and assent.
