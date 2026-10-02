Grok review: unit X8b r1, the `scenario-fixtures` feature and both `scenario` modules (law X8 r3 item 4), with inventory v129 on v118. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-scenario-fixtures-x8b-r1. If you build or test, use a CARGO_TARGET_DIR under that directory, and a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)` (other worktrees churn the shared temp folder; X9-2 is building in parallel). Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read the private 413 UUID fixture.

## Inputs

- **Laws** (all pinned in `hashes.txt`):
  - X8 r3, `docs/implementation/m2/refusal-suite-x8/PROPOSAL-r3.md`, 44288 bytes, sha256 `1dc6b71fa4e5ec064fc409abf1164a968ddaa6ca1d635f363080128d2bbbf385` (accepted). Items 4a to 4g and 5a, and "Units after the law", define X8b:
    - the feature in security and storage, enabled only from storage's and host's `[dev-dependencies]`;
    - security's `scenario` (`ScenarioHome::create`, `project`, `operation`, `publish_revocation_fenced`, `revocation_version`, `paths`, `carrier_census`) and storage's (`ledger_census`, `plant_attempt`);
    - X9-1's site pin extended by name, with no second list or pin;
    - group J's E0432, and the release guard of item 4f.
  - X8 r4 (record-only, in review as `reviews/grok-refusal-suite-x8-r4`): it records only that X3d-2 integrated before X8b. Nothing in X8b depends on it.
  - X9 r3, `docs/implementation/m2/crash-matrix-x9/PROPOSAL-r3.md`, 62835 bytes, sha256 `1f270548777b3234f0188ecb3496cedcef718a30bcb46d0b07832a4be6a0b04a` (accepted). Item 2 (release guards; no manifest names `crash-matrix`) and item 6 (the support surface; the shared sites under the joint predicate; "one list and one pin, extended by name by X8b").
  - X10 r4, `docs/implementation/m2/read-cli-x10/PROPOSAL-r4.md`, 17619 bytes, sha256 `33095e6c13c0e16a5e4fdc87832dbd2f048b01f126b432d49347cc2f116b386a` (accepted). Item 5's narrowed pin: `apps/cli` and reporting declare no features; host, security and storage only `crash-matrix` and `scenario-fixtures`; no bridge reaches the binary, the doctor ingress, or a default or release build.
  - X9 r4 (pending, `reviews/grok-crash-matrix-x9-r4-x6-r4`) is context only: it gives `crash_matrix_support` an `operation` driver entry under `crash-matrix` alone. See judgment call 1.
- **Product.** Worktree `/Users/sb/code/opensip-ai/opensip-x8b`, detached at main `a36da7c` (X9-1 integrated), uncommitted. The six new files are intent-to-add. `git diff a36da7c` is 52513 bytes, sha256 `24c6cd9547484b7376a8b23cf95a4b01275fbc69212becc7ec3d13a7dbb747a9`: 15 files, +881 −27. Every file is pinned in `hashes.txt`.
- **Toolchain.** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`.
- **X9-1** at `a36da7c` built the shared site list under the joint predicate, its pin (`crash_matrix_sites.rs`), the shared installation fixture (`custody/installation_read_fixture.rs`: `InstallationAt`, `writer`, `install_accepted_trust`, `publish_accepted_trust_fenced`) and the fenced publisher (`trust::publish_store_fenced`). It also declared an empty `scenario-fixtures` in security. X8a's driver and its `scenario-fixtures` manifest pin are in `crates/host/tests/admission_tests.rs`.

## What X8b builds

- **The feature (item 4a).**
  - Storage declares `scenario-fixtures = ["opensip-security/scenario-fixtures"]`. Security's empty declaration stays; only its comment changes.
  - Storage's `[dev-dependencies]` name `opensip-security` with the feature, so storage's tests reach security's seam (item 4g).
  - Host's `[dev-dependencies]` name `opensip-storage` with the feature, which forwards to security's.
  - Host declares no feature. No `[dependencies]` table, default or other manifest names it. `Cargo.lock` is unchanged.
- **Security's `scenario` (item 4c),** `#[cfg(all(feature = "scenario-fixtures", target_os = "macos"))] #[doc(hidden)] pub mod scenario`:
  - `ScenarioHome::create(parent)` creates `parent/x8-synthetic-<draw>` (0700). Under it, it builds the shared fixture's P0 through the real creator path (injected loaded image, synthetic V2 profile set) and installs X4T-0's signed accepted store at revocation version 1, with no entries. `ScenarioHome::open(home, installation, store)` names a home created by another process, for item 5a's helper. There are path accessors `home`, `installation` and `store`.
  - `project(name)` creates the root `H/code/<name>`, 0755 with no ACL, as X9-1's fixture does.
  - `operation(&self, root) -> Result<ProjectOperation, InstallationTermination>` is a thin caller of the shared fixture's new `InstallationAt::operation(root, WriterLease::AppendWrite)`, which runs the production chain:
    - X1's writer through `ordinary_writer::admit_with`, with the write receipt over a signed test tree and the gate over `HomeSource::Fixture`;
    - X2b's root admission and tracking;
    - X2c's first registration when the root classifies as `FirstUseCandidate`; otherwise the admitted root goes to `begin_operation` as `Eligible`;
    - `begin_operation`, covering X2d, X3a's endpoint, X4's first read and monitor, X3b's floor step and carrier start, and X2e's handoff.

    Each refusal maps to its row through X3d r6 item 9's existing maps (`project_termination`, `operation_termination`). The signed tree is kept for the home's lifetime. On success, `operation` sets a process-wide flag.
  - `publish_revocation_fenced(home, &[(kind, subject)]) -> Result<RevocationVersions, InstallationTermination>` is a thin caller of the shared fenced publisher, at revocation version current + 1. It returns versions before and after as `u64`. It refuses on the invariant row, with no write, in two cases: when the flag is set, and when a subject kind is not one the revocation matcher knows (`release`, `keyId`, `namespace` or `catalogSnapshot`). The publisher's other refusals map through `gate_refusal` and `trust_termination`.
  - `revocation_version(home) -> u64` reads `state.v1` by name, read-only.
  - `paths(root, namespace) -> ScenarioPaths` names the root, `.opensip`, the marker, N's directory, the two lease files, `selection.pair`, S's marker and the selected lineage node. Nothing is opened except a read of `selection.pair` to find G and K.
  - `carrier_census(namespace)` gives a read-only count of `SEAL`, `REV`, `CLN`, `TERMINAL` and other records from `grant_journal_v3`.
- **Storage's `scenario` (item 4d),** under the same predicate:
  - `ledger_census(home, store, namespace)` reads the ledger read-only (`SQLITE_OPEN_READ_ONLY`, no follow): each `attempt_custody` row's ExecutionId and phase, and the `commit_receipts` count. An absent ledger gives an empty census.
  - `plant_attempt(home, StoreBinding { namespace, store, generation, schema }, execution_id)` writes one `admitted` row. Its key uses the facade's own `store_generation_digest`, and it draws a fresh operationRef. It goes through X3c-1's `admit_namespace_directory`, `create_or_open_ledger` and `admit_attempt` (the ordinary insert), on a location built by the production `ProjectStoreLocation::selected` over `I/stores/S`. Refusals map through the facade's `ledger_failure`, widened to `pub(crate)`. It takes values, never a session or lease.
- **The shared fixture (`installation_read_fixture.rs`, already on the list under the joint predicate through `custody.rs`'s module gate).** No new cfg site:
  - `ReadFixture::new_in(tag, parent)`, which `new` now calls with `None`;
  - typed cores behind the unchanged `writer()` and `publish_accepted_trust_fenced()`. These are `admitted_writer` (stage plus row) and `publish_trust_fenced` with `FencedRefusal`, whose `text()` reproduces the old strings and whose `termination()` gives the row;
  - `InstallationAt::operation`, the one production-chain composition.
- **The pin (item 4b).** `crash_matrix_sites.rs` gains two rows, `cfg(all(feature = "scenario-fixtures", target_os = "macos"))` once in each of security's and storage's `lib.rs`, under "the feature's own declarations", and its doc comment says so. No shared fixture gate is added, and the joint-predicate rows are unchanged.
- **Group J (item 4f).** `security_scenario_unnameable.rs` and `storage_scenario_unnameable.rs`, each E0432 "unresolved import `opensip_…::scenario`", with a compiling control. The rows are in `admission_tests.rs`'s table (unit X8b, group J, new category `TestSeam`), and the header and manifest-pin comment are updated.
- **Tests.**
  - Security's `scenario_tests.rs` is one ordered test, wrapped in F5's `churned`:
    - the label, and version 1;
    - two publications (1→2, 2→3), and an unknown kind refused with `state.v1` unchanged;
    - `open` by paths;
    - a first-use `operation`, with its paths present;
    - publication then refused with `state.v1` unchanged;
    - `end`, a second operation on the registered root, an absent root refused, and the refusal still in force.
  - Storage's `scenario_tests.rs`:
    - `operation` and then `CommitSession::open`, with no ledger yet;
    - `plant_attempt` with the session's own ExecutionId, read back as one admitted row with no receipt;
    - the same key refused on the invariant row, and `../x` refused, with the census unchanged;
    - `reserve_end_path().refused().finish()`, then a carrier census of one `REV` and no `SEAL`.

## Judgment calls (narrowest choice consistent with the laws)

1. **One composition, in the shared fixture (lead's direction).** `InstallationAt::operation(root, lease)` sits in the shared installation fixture, which is already on X9-1's list. So `scenario::operation` is a thin caller, and X9 r4's proposed `crash_matrix_support::operation` can call the same function under `crash-matrix`.
   - Neither surface calls the other, and no cfg site is added.
   - It returns the signed tree beside the operation, because the receipt's tree must outlive the writer. X9-1's census drops it early.
   - It takes the lease mode because X9's census also uses EXCLUSIVE. `scenario` passes APPEND-WRITE, since every B case is a commit.
2. **First use by the production classification.** `FirstUseCandidate` registers. Every other classification goes to `begin_operation` as `Eligible`, whose namespace admission refuses it on its own row. The scenario keeps no registry of its own.
3. **Invocation identity.** The `req1_` and `exec1_` of `TrustInvocation` are drawn from the host CSPRNG, where X9-1's census uses fixed literals. The law fixes neither.
4. **Typed cores, unchanged wrappers.** To return `InstallationTermination` as item 4c's signatures require, the shared `writer()` and `publish_accepted_trust_fenced()` keep their `String` API and exact text, over typed cores.
   - Fixture-precondition failures map to the invariant row: an unreadable `state.v1`, or a non-addressed store file that differs.
   - A failed fence release maps to the host I/O row, which is what `gate_refusal` gives `IoFailure::Lock`.
5. **The lease flag is sticky.** It is a process-wide `AtomicBool`, set when `operation` returns `Ok` and never cleared, because the seam cannot observe the release of a production `ProjectOperation`. That is narrower than tracking drops, and it matches item 5a's helper, "a separate process that never ran `operation`". The refusal is the invariant row, with no write. The test resets the flag at the start of each `churned` attempt; that is test-only.
6. **Subjects and version.** Subjects are `&[(&str, &str)]` pairs of `(subjectKind, subject)`, limited to the four kinds the matcher reads. The law gives no version argument, so each publication uses current + 1. Versions are returned as `u64`, the type the law gives `revocation_version`.
7. **`revocation_version(home) -> u64`** keeps the law's signature exactly, so an unreadable `state.v1` panics as a broken home, as fixtures do.
8. **Signatures beyond the law's sketch.**
   - `open(home, installation, store)` and the path accessors exist for item 5a's input file.
   - `paths` takes the root as well as N, because the law's paths include the root's own. `lineage` is `Option`, since `selection.pair` may not decode.
   - `carrier_census` returns `Result<_, String>` and an `other` count.
   - Storage's functions take the home and values. `plant_attempt` takes `StoreBinding` (N, S, G, K, from the session's public accessors) and never a session (item 4e).
9. **`create(parent)`.** The home is under `parent/x8-synthetic-<draw>`, so every path carries `synthetic`. The signed test trees still live under security's per-process test scratch parent, which also takes `test_scratch`'s per-thread lock, as every fixture does.
10. **`plant_attempt` creates or admits N's directory and ledger first.** B4 plants before `prepare_commit`, when no ledger exists yet. The object directory is not created. It takes no lease: the case's session holds N's.
11. **Group J has two cases.** Law row J names security's module. Item 4a defines both modules, and item 4f's guard covers both, so storage's gets the same E0432 case. The category is a new `TestSeam`, as group I has `StorageInternals`.
12. **The pin extension.** There are two rows for the two module declarations, macOS-only like `crash_matrix_support`, because the chain is macOS-only. No `scenario` source is added to X9-1's no-sleep pin, which the law does not ask for: `ReadFixture::new`'s F4 backoff is already shared.
13. **Where the tests run.** Each `scenario_tests.rs` is `cfg(test)` inside its feature-only module, so it runs when that crate's test build has the feature.
    - In the documented lane, Cargo's feature unification gives both crates the feature through host's dev-dependency. Both tests ran there: 1709 against X9-1's 1707.
    - It also gives both crates the feature in the crash-matrix lane (1594 against 1592), and in the explicit `-p opensip-security -p opensip-storage --features scenario-fixtures` lane.
    - `cargo test -p opensip-storage` alone compiles security's seam but not storage's own module.

## Disclosure for your ruling: feature unification in the test lane

`cargo test --workspace --all-targets --no-run --message-format=json` shows `opensip_security` and `opensip_storage` built once, each with `["scenario-fixtures"]`. The debug `opensip` binary built in that invocation, for `apps/cli`'s tests, links them. Its shared sites under the joint predicate are therefore compiled in:
- `Image::Injected`;
- `HomeSource::Fixture`;
- the SYNTHETIC-standing `cfg!` in `initial_platform.rs`.

No code path of the binary calls the seam. The doctor binary tests still pass (`CORE.NO_EMBEDDED_RELEASE`, exit 2, the home untouched). Default and release builds are unaffected: the release `opensip` is byte-identical to X9-1's (below), and `cargo tree -e features -p opensip-cli` names no `scenario-fixtures`.

This follows from item 4b's own choice: the feature is enabled from host's dev-dependencies, so that B0 to B8 run in `cargo test --workspace --all-targets`. X10 r4 item 5 speaks of "the binary, the doctor ingress, or any default or release build". Please rule whether a test-lane debug binary linking the joint-predicate sites is within that. If it is not, the remedy is a law question, not an X8b one: for example, moving B0 to B8 to an explicit feature lane.

## Checks on a36da7c with this diff (private TMPDIR)

- **Full workspace twice,** `cargo test --locked --offline --workspace --all-targets`: 1709 passed, 0 failed, 3 ignored, both times. X9-1's baseline is 1707; the two new tests make the difference.
- **Crash-matrix lane,** `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets`: 1594 passed, 0 failed, 3 ignored. Both pinned censuses (277 and 46 points) are unchanged. The scenario tests are included through unification.
- **Scenario lane,** `cargo test -p opensip-security -p opensip-storage --features scenario-fixtures --all-targets`: 1134 passed, 0 failed, 2 ignored.
- **X8a driver,** `cargo test -p opensip-host --test admission_tests`: 6 passed, group J included. `scenario_fixtures_stays_out_of_release_manifests` is no longer vacuous.
- **Clippy `-D warnings`:** clean on the workspace, on the four crates with `crash-matrix`, and on security and storage with `scenario-fixtures`.
- **`cargo fmt --check`:** clean.
- **`check_package_edges --lane host`:** passes against v118 and v129. 22 declared internal edges (the two new dev edges are host→storage and storage→security) and 20 resolved.
- **Release absence:**
  - `cargo build --release -p opensip-cli` → `target/release/opensip`, 6314176 bytes, sha256 `e1b545662b2b913a680ba42721a0edfa75989b5461e143dc336dcb83f89628a8`. That is byte-identical to X9-1's release binary.
  - None of 12 scenario strings is present: `x8-synthetic`, `scenario scratch`, both census SQL statements, `ScenarioHome`, `publish_revocation_fenced`, `plant_attempt`, `opensip_security::scenario`, `opensip_storage::scenario`, `OPENSIP_X8_`, and two panic texts.
  - `cargo tree -e features -p opensip-cli` names no `scenario-fixtures`.
  - Group J's E0432 holds on the plain `cargo check -p opensip-host` surface.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Inventory v129

`scenario-fixtures-x8b-inventory-v129/evidence/build_v129.py` adds six rows to the parent the lock selects: inventory118 (X9-1), 539833 bytes, sha256 `ae94d003acdd4ee203a672c7164513705acc876a723faf4eb45a25fb99eaa925`.
- The rows: `security/src/scenario.rs` and `storage/src/scenario.rs` (service); the two `scenario_tests.rs` (test); and the two group J cases (fixture, package `opensip-host`).
- 957 inherited rows are equal by value, for 963 files. Packages, pending decisions and carried obligations are unchanged.
- The fifty-five inheritance rows are re-projected by stable path (sixteen carried, D1's thirty-nine, D2's four supersessions folded), with `supersessionsFolded: 0`.
- The README lists the changed existing rows, and which descriptions go out of date by omission (`installation_read_fixture.rs`, `crash_matrix_sites.rs`, `admission_tests.rs`).
- Reruns are byte-identical. The builder refuses tracked paths and a lock that selects v129.
- X9-2 builds v130 on the same parent, so whichever integrates second needs a parent-only rebuild.

Pins:
- v129: 545917 bytes, sha256 `139f9331b43288fe55e4c7526c4243263d04186afd8e973a43f291784da259d0`;
- successor.json: 145363 bytes, sha256 `6eb1e2e02c17a54f141e4dd93cac290f19378695fdc17f052638284379205b5a`;
- subject manifest `scenario-fixtures-x8b-inventory-v129-subject.json`: 2155 bytes, sha256 `03dfd8bad44fce9102b582401dddb94fe41bca3c808c5a69b6a7109f037c1951`.

Verification:
- `verify_projection` against the real lock at a36da7c: PASS, 55 rows, 278 corruptions refused.
- `evidence/verify_scratch.py` (v129 appended in memory over the worktree's lock, with a synthetic review and assent): passed, with 90 inventory successors, 74 contract successors, 55 inheritance rows, and v129 selected.

## Decide

- Does X8b implement X8 r3 item 4 faithfully (4a to 4g, and 5a's helper-facing functions), with nothing of X8c's B0–B8 and nothing of X9?
- Is every new test-feature site on the pinned list? Is the extension by name only, with no shared gate added and no second list? Is anything reachable from a release or default build?
- Does `scenario` construct, accept or return anything beyond item 4e's one exception?
- Is the shared composition sound and the narrowest placement (judgment call 1)? Are the typed cores behaviour-preserving for X9-1's callers?
- Rule on the test-lane unification disclosure.
- Is each judgment call acceptable? Is v129 right on v118?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": `03dfd8bad44fce9102b582401dddb94fe41bca3c808c5a69b6a7109f037c1951`, the sha256 of `docs/implementation/m2/scenario-fixtures-x8b-inventory-v129-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path `docs/implementation/m2/repository-file-inventory.v129.json`, bytes 545917, sha256 `139f9331…`, parent (the v118 pin above), successorRecord (path `docs/implementation/m2/scenario-fixtures-x8b-inventory-v129/successor.json`, bytes 145363, sha256 `6eb1e2e0…`)}.

Write REVIEW.md and review.json. Do not commit.
