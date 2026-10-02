# X8b r1 — scenario-fixtures

**Verdict: ACCEPT-UNIT.** Inventory v129 is **ACCEPT** on inventory118. Required findings: none.

## Disclosure

X10 r4 item 5 protects the shipped `opensip` binary, the doctor ingress, and every default or release build. A debug binary produced inside `cargo test --workspace` is a test build, so it is outside that pin. Release-absence holds, and the default debug build is clean as well.

This replay:

- `cargo build --locked --offline --release -p opensip-cli` produced `opensip` at 6314176 bytes, sha256 `e1b545662b2b913a680ba42721a0edfa75989b5461e143dc336dcb83f89628a8`. The security library in that build has features `[]`. The binary contains none of `x8-synthetic`, `scenario scratch`, either census SQL statement, `ScenarioHome`, `publish_revocation_fenced`, `plant_attempt`, `opensip_security::scenario`, `opensip_storage::scenario`, `OPENSIP_X8_`, `accepted store:`, or `revocation version:`.
- `cargo build --locked --offline -p opensip-cli` builds security with features `[]`. Those seam strings are absent, and `Injected` is absent. The byte sequence `scenario-fixtures` occurs there only as this review's target-directory path inside debuginfo.
- `cargo tree --locked --offline -e features -p opensip-cli` names `opensip-host` feature `default` and does not name `scenario-fixtures`.
- `cargo test --locked --offline --workspace --all-targets` builds the `opensip-security` and `opensip-storage` libraries with features `["scenario-fixtures"]`. Host and `opensip-cli` stay at features `[]`. The test-profile `opensip` links that security library. In the same run, `doctor_tests` passed 4, including `a_development_build_doctor_ends_at_no_embedded_release_in_both_formats` and `no_home_profile_or_release_selector_reaches_the_binary_or_the_ingress`. The scenario module's strings live in those feature-enabled rlibs. The test-profile `opensip` retains `initial_core::tests::InjectedImage` from the joint predicate, and that symbol is absent from the default and release binaries. No binary path calls `scenario`.

Item 5 allows `scenario-fixtures` in host, security, and storage under X8's release guard. Item 4a enables it from host's and storage's `[dev-dependencies]` so the refusal cases run in the workspace test lane. That enablement is what unifies the feature for one `cargo test --workspace` invocation, and the binary that invocation produces is a test build. This diff leaves the doctor ingress untouched. Those doctor tests still end at `CORE.NO_EMBEDDED_RELEASE`, exit 2, with the real home absent.

A later law that placed that test-lane binary inside the pin would be a law question, for example moving B0–B8 onto an explicit feature lane. This unit's code would stay as it is.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x8b`, detached at `a36da7ce495b49c2d82ad31a9ecef707e6de9909` (X9-1). `git diff a36da7c` is 52513 bytes, sha256 `24c6cd9547484b7376a8b23cf95a4b01275fbc69212becc7ec3d13a7dbb747a9`: 15 files, +881 −27. The six new files are intent-to-add. `Cargo.lock` is unchanged. `~/Library/Application Support/OpenSIP` is absent.

Subject manifest `docs/implementation/m2/scenario-fixtures-x8b-inventory-v129-subject.json`: 2155 bytes, sha256 `03dfd8bad44fce9102b582401dddb94fe41bca3c808c5a69b6a7109f037c1951`.

## Item 4

**4a.** Security keeps an empty `scenario-fixtures = []`. Storage forwards `scenario-fixtures = ["opensip-security/scenario-fixtures"]` and names security in `[dev-dependencies]` with that feature. Host names storage in `[dev-dependencies]` with that feature and declares no scenario feature of its own. No `[dependencies]` table and no default enables it.

**4b.** `crash_matrix_sites.rs` gains the two module declarations, `cfg(all(feature = "scenario-fixtures", target_os = "macos"))` once in each of security's and storage's `lib.rs`. The joint-predicate rows are unchanged. The doc comment says the list is extended by name. No shared fixture gate is added. `custody.rs`'s module gate is outside this diff.

**4c–4d.** Both modules are `#[doc(hidden)]` under that predicate. `ScenarioHome::create` makes `parent/x8-synthetic-<draw>` at mode 0700, installs the signed accepted store at revocation version 1 through the shared fixture, and offers `open`, `project`, `operation` (APPEND-WRITE), `paths`, and `carrier_census`. `publish_revocation_fenced` refuses on the invariant row, before any write, when the process-wide flag is set or a subject kind is outside `release`, `keyId`, `namespace`, and `catalogSnapshot`. `revocation_version` keeps the law's `u64` signature and panics if `state.v1` is unreadable. `ledger_census` is read-only (`SQLITE_OPEN_READ_ONLY`, `NO_MUTEX`, `NOFOLLOW`); an absent ledger is an empty census. `plant_attempt` takes `StoreBinding` values and an execution id, draws `op-` plus the 16-byte entropy hex (35 characters), and admits N's directory and ledger through `ledger_failure`, widened to `pub(crate)`. It takes no session and no lease.

**4e.** The authority type `scenario` returns is the `ProjectOperation` from `operation`. `ReadProducers` stays inside the home so the signed tree outlives the writer. Storage returns `Result<(), InstallationTermination>`.

**4f.** Group J is two E0432 cases, security's and storage's, category `TestSeam`, each with a compiling control. `admission_tests` passed 6, including `scenario_fixtures_stays_out_of_release_manifests` and `opaque_api_misuse_fails_for_the_intended_reason`.

**4g.** The dev-dependency seam this item names is the one storage's scenario test uses. X3d-2's ordinary-lane tests remain as integrated. X8 r4 records that they obtain no `ProjectOperation` through this feature. This unit leaves them in place. X8c's B0–B8 are absent from the diff, and so is any X9 crash-matrix driver.

## Judgment calls

All thirteen are the narrowest choices the laws allow.

1. `InstallationAt::operation(root, lease)` is the one composition, in the shared fixture already on X9-1's list. `scenario::operation` is the thin APPEND-WRITE caller and returns the signed tree beside the operation. The two surfaces are independent. No cfg site is added.
2. `FirstUseCandidate` registers. Every other class goes to `begin_operation` as `Eligible`.
3. `req1_` and `exec1_` are drawn from `request_entropy`.
4. `writer()` and `publish_accepted_trust_fenced()` keep their `String` surface. The typed cores are `admitted_writer` and `publish_trust_fenced`, whose `FencedRefusal::text()` rebuilds the previous strings.
5. `LEASE_HANDED_OUT` is set only after `operation` returns `Ok`, and the seam never clears it. The scenario test resets it at the start of each `churned` attempt.
6. Subjects are `(&str, &str)` pairs of the four matcher kinds. Each publication uses current + 1 and returns `u64`.
7. An unreadable `state.v1` panics from `revocation_version`.
8. `open` and the path accessors serve item 5a's helper. `paths` reads `selection.pair` so `lineage` can be `Option`. The function comment still says nothing is opened; the read is this call. `carrier_census` returns `Result<_, String>` and an `other` count. `plant_attempt` takes values only.
9. The home is `parent/x8-synthetic-<draw>`. Signed trees stay under security's per-process scratch.
10. `plant_attempt` creates or admits N's directory and ledger first, with no object directory and no lease.
11. Storage's E0432 case sits beside the law row, which names security's module. Item 4a defines both modules.
12. The pin gains two declaration rows. No scenario source is added to the no-sleep pin.
13. Each `scenario_tests.rs` is `cfg(test)` inside the feature module. Both tests passed in the scenario lane and in the workspace suite.

## Inventory v129

ACCEPT on parent inventory118 (`docs/implementation/m2/repository-file-inventory.v118.json`, 539833 bytes, sha256 `ae94d003acdd4ee203a672c7164513705acc876a723faf4eb45a25fb99eaa925`).

Candidate `docs/implementation/m2/repository-file-inventory.v129.json`, 545917 bytes, sha256 `139f9331b43288fe55e4c7526c4243263d04186afd8e973a43f291784da259d0`. Successor record `docs/implementation/m2/scenario-fixtures-x8b-inventory-v129/successor.json`, 145363 bytes, sha256 `6eb1e2e02c17a54f141e4dd93cac290f19378695fdc17f052638284379205b5a`.

963 files. Six added rows: both `scenario.rs` (service), both `scenario_tests.rs` (test), and both group J cases (fixture, package `opensip-host`). 957 inherited rows are equal by value. Packages (20) and pending decisions (9) match the parent. The carried obligations stay. The description projection is 55 rows, with `supersessionsFolded` 0. `packageDependencyGraphUnchanged` is true. `check_package_edges --lane host` passes against v118 and v129: 22 declared internal entries and 20 resolved pairs. `opensip-host → opensip-storage` and `opensip-storage → opensip-security` are each declared twice, once normal and once dev, and each resolves with both kinds. `verify_projection` against the worktree lock: PASS, 55 rows, 278 corruptions refused. `verify_scratch`: passed, 90 inventory successors, 74 contract successors, 55 inheritance rows, v129 selected.

The README leaves the descriptions of `installation_read_fixture.rs`, `crash_matrix_sites.rs`, and `admission_tests.rs` for a later description-only successor. Those descriptions stay as the parent had them. X9-2 builds v130 on the same parent, so whichever integrator lands second rebuilds from that parent alone.

## Replay

Private `TMPDIR` `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-x8b-r1.IWBiz1` (mode 0700). Each `CARGO_TARGET_DIR` was under this review directory and was removed after the runs.

- Workspace `cargo test --locked --offline --workspace --all-targets`: 1709 passed, 0 failed, 3 ignored, once. The lead's second identical run was left unreplicated.
- Scenario lane `-p opensip-security -p opensip-storage --features scenario-fixtures --all-targets`: 976 + 158 = 1134 passed, 0 failed, 2 ignored. Both new tests passed.
- `admission_tests`: 6 passed. `doctor_tests`: 4 passed.
- `cargo fmt --all -- --check`: clean.
- Clippy `-D warnings`: clean for security and storage with `--features scenario-fixtures --all-targets`, and clean for host `--all-targets`. Workspace clippy and the crash-matrix feature lane were left unreplicated. The site-pin tests ran inside the security library tests.

The real home was absent before the runs and absent after them.
