# Scenario-fixtures inventory129

Adds exactly six files to inventory118 (unit X9-1, selected at product a36da7c, with D1's thirty-nine overrides and D2's four supersessions already folded into its fifty-five inheritance rows):
- crates/security/src/scenario.rs
- crates/security/src/scenario_tests.rs
- crates/storage/src/scenario.rs
- crates/storage/src/scenario_tests.rs
- crates/host/tests/refusal/cases/security_scenario_unnameable.rs
- crates/host/tests/refusal/cases/storage_scenario_unnameable.rs

It keeps all 957 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 963 planned files.

**No new edge.** Storage's `scenario-fixtures` forwards to security's along the storage-to-security edge the parent declares. Storage's `[dev-dependencies]` name security, and host's name storage, each an edge the parent already declares for the same pair. A feature is not a package row, and `check_package_edges.py` admits a dev edge exactly where the policy admits the pair. The builder asserts each such edge is declared in the parent.

The rows are unit X8b, law X8 r3 item 4 (with r4's record-only note on its ordering): the `scenario-fixtures` feature in security and storage, enabled only from storage's and host's `[dev-dependencies]`; both `scenario` modules; X9-1's site pin extended by name; group J; and the dev-dependency entries.

- **security scenario.rs (service).** Security's feature-only, `doc(hidden)` seam: `ScenarioHome` (`create` under the caller's scratch parent, `open` by paths), `project`, `operation` (the production chain to a `ProjectOperation`, the one authority type it returns), `publish_revocation_fenced` (the shared fenced publisher, refused in a process that `operation` handed a lease to), and the read-only `revocation_version`, `paths` and `carrier_census`.
- **storage scenario.rs (service).** Storage's feature-only, `doc(hidden)` seam: the read-only `ledger_census` and `plant_attempt` through X3c-1's ordinary attempt admission.
- **scenario_tests.rs, security and storage (test).** Each module's own tests, compiled only with the feature in that crate's test build.
- **security_scenario_unnameable.rs and storage_scenario_unnameable.rs (fixture).** Group J: E0432 on each `scenario` from the plain host surface.

**Changes to existing rows.** Every row stays by value. Where a lock inheritance row overrides a row, the text judged here is the effective description. Out-of-date descriptions are left for the next description-only successor, as earlier units left theirs.
- `crates/{security,storage,host}/Cargo.toml`: storage declares `scenario-fixtures` (forwarding to security's, which X9-1 declared) and a `[dev-dependencies]` entry naming security with the feature; host gains a `[dev-dependencies]` entry naming storage with the feature; security's comment only. Their descriptions stay true.
- `crates/{security,storage}/src/lib.rs`: the feature-only `pub mod scenario` (`doc(hidden)`). Their descriptions stay true.
- `crates/security/src/custody/installation_read_fixture.rs`: `ReadFixture::new_in` (a caller's scratch parent); typed cores behind the unchanged `writer` and `publish_accepted_trust_fenced`, with their refusal text unchanged; and `InstallationAt::operation`, the one production-chain composition both support surfaces' operation entries are to call. Its effective description is out of date by omission, as it already was of X9-1's shared producers; it still says test support, which it remains.
- `crates/security/src/crash_matrix_sites.rs`: the pin extended by name with the two `scenario` declarations. Its description ("each crate's guard and support module") is out of date by omission of them.
- `crates/storage/src/commit.rs`: `ledger_failure` widened from private to `pub(crate)` for `plant_attempt`'s rows. Its description stays true.
- `crates/host/tests/admission_tests.rs`: group J's two rows and the `TestSeam` category, and the manifest pin's comment. Its effective description lists only some units' groups and is out of date by omission, as it already was of X3d-2's, X5a's and X7a's.

**Order.** Its parent is the inventory the real product lock selects: inventory118 (unit X9-1) at product a36da7c. The number 129 was assigned by the lead; succession is by the lock's parent pin, not by number. X9-2 builds inventory130 in parallel on the same parent, so whichever integrates second needs a parent-only rebuild. `evidence/build_v129.py` reads the parent from the lock (the product checkout's `design-lock.json`, or a lock path as its one argument), checks each inheritance row against the lock before carrying it, writes only its two paths, refuses tracked paths and refuses while a lock selects inventory129. Reruns reproduce the same bytes.

**Projection.** The fifty-five effective description overrides the lock binds to inventory118 stay bound by stable file path: the sixteen carried from inventory81 onward and D1's thirty-nine, with D2's four supersessions already folded. Only their candidate selectors move, by the six inserted rows. No contract successor bound at a36da7c names inventory118 as a supersession parent, so nothing new is folded (`supersessionsFolded: 0`).

`verify_projection.py` is inventory118's helper with its comment updated for this parent; it runs against the real lock at a36da7c. `evidence/verify_scratch.py` appends inventory129 in memory over the worktree's lock and replaces the inheritance rows with the record's fifty-five, with a synthetic review and assent.
