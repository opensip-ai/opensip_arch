# B2-b3c r2: what the candidate delivers (M3-B unit B2-b3, sub-unit B2-b3c: the seam and the flag rows)

**Lead scope record, 2026-10-15. Unreviewed candidate.** It implements LD-B2B3-12 of the accepted B2-b3 plan r3 (`config-discovery-b/b2-b3/PLAN-r3.md`; Codex `codex-b2b3-plan-r3`, the lead amendment found while preparing this unit). Its base is product `aa037d0`: B2-b3b is bound, inventory is v194, and contract successors are 164.

## r2 changes (Codex `codex-b2b3c-r1`, REQUIRED-FINDINGS)

**B2B3C-R1-RF-1: the operation's end is disclosed, never dropped.**
- **The defect.** r1 dropped `operation.end(...)`, so an end-path failure could disappear behind a clean-looking record.
- **The fix.**
  - `OperationEnd` gains two read-only methods (`custody/operation_handoff.rs`): `entered()` (`NotEntered` is not a failure) and `failure()`, the end-path failure the caller must disclose (`Failed`, or a failed copy or unlock after `RolledOver`).
  - The seam records `end_entered`, `end_rolled_over` and `end_failure` (the failure's row) beside the discovery outcome, which the end does not change.
- **New controls.**
  - `an_end_failure_is_disclosed_and_never_mistaken_for_a_clean_end` (security): a constructed `Failed` end is entered and discloses its host I/O row; `NotEntered` is neither entered nor a failure.
  - The host test asserts a clean run's end: entered, no rollover, no failure.

  A host test cannot inject an end failure without a new fixture gate, so the failure path is held by the security unit test.
- **New mutations:** `end-failure-hidden` and `end-not-recorded`.

**NBO-1.** An accepted result's boundary inventory must now convert, or the seam returns `Err`. A refused result has none. There is a new mutation, `accepted-inventory-skipped`.

The evidence is lane r3, with 8 mutations.

## Paths

| Path | Change |
|---|---|
| `crates/security/src/scenario.rs` | `ScenarioHome::discover`, `DiscoveryRequest` and `DiscoveryRecords`, in the `scenario-fixtures` seam (no new feature site). |
| `crates/host/src/discovery_flag_tests.rs` | **New.** The COV:5288 and COV:5388 rows, as host unit tests. |
| `crates/security/src/custody/operation_handoff.rs` | (r2) `OperationEnd::entered` and `OperationEnd::failure`, read-only. A test in `operation_handoff_tests.rs`. |
| `crates/host/src/lib.rs` | Declares `#[cfg(all(test, target_os = "macos"))] mod discovery_flag_tests;`. It has no other change. |

## The seam (LD-B2B3-12, r3)

`ScenarioHome::discover(&request, resolve) -> Result<DiscoveryRecords, String>` runs on an ordinary writer (the shared fixture's `writer`, X8 gate 2), in this order:
1. **Analysis phase 1** (`admit_project_carriers`), with the explicit path and the typed owner waiver. The waiver is built by `ProjectOwnerWaiver::from_invocation`, so a waiver without `--project` cannot be built. It records an `UpwardRecord`. A selection refusal ends the discovery with `UpwardRecord::discovery_refusal`'s code and detail; the writer is dropped, so it is released.
2. **`resolve`** over the captured carrier bytes (the caller's resolution: the host's resolver with its flag layer, and pack admission). It returns the winning `discovery.workspaceRoots`, none, or a refusal. A refusal ends the discovery before item 5.
3. **Item 5** (`complete_project_admission`, with the waiver).
4. **The shared composition's steps,** exactly as `InstallationAt::operation` takes them:
   - tracking over an empty environment and no system sources;
   - first registration when the root is a first-use candidate;
   - `begin_operation`, whose handoff releases the fence.
5. **The walk and the core.** `ProjectOperation::discovery_root`, then `discover_downward` on a fresh `WorkLedger::discovery_profile()`. The unit source is chosen before traversal: the winning roots as `config-workspace-roots`, else automatic. The invoking uid is the scratch home's owner (the account's own uid, which the seam cannot read from the installation outside `custody`).
6. **`end`** on the operation.

**The records** are plain values: how far the discovery got (`resolved`, `phase_two`, `walked`), the upward mode and stop, `custodyWaiver`, the unit source, the units and excluded units, a discovery refusal's code and detail, the resolution's refusal, and the accepted result's boundary inventory as canonical JSON. A refusal that is not discovery's is `Err`.

## The flag rows (COV:5288, COV:5388)

`crates/host/src/discovery_flag_tests.rs`, its own test module. B1-a's source pin (`configuration_tests.rs`, `production_source`) holds the configuration module's test includes exactly, so the rows do not join that module; lane r1's three pin failures showed it, and `configuration.rs` is unchanged. The module builds its own non-interactive resolver input from B1-a's `base` compiled defaults. The resolution closure is the host's own resolver over the captured bytes, with `flags.workspace_roots` set from the `--workspace-root` values. It records the winning roots' provenance.
- **`project_selects_exactly_its_path_examined_once_and_never_walked_upward`** (`--project`).
  - From a launch elsewhere, the mode is `explicit` and the stop `EXPLICIT`. Every phase runs, and the root's subtree gives its unit automatically.
  - An absent path refuses `PROJECT.EXPLICIT_PATH_INVALID`/`ABSENT` at selection, before any resolution.
- **`trust_project_owner_reaches_only_the_owner_check_of_its_explicit_root`.**
  - The waiver is recorded (`custodyWaiver`), and the walk runs.
  - An other-writable explicit root still refuses `WRITABLE_BY_OTHERS` before resolution.
  - Without `--project`, the waiver cannot be built.
  - A foreign owner cannot be made on a scratch tree; B2-b3a's and B2-b3b's vectors hold it (plan r3).
- **`configuration_never_impersonates_explicit_consent`.** A project configuration naming `project` or `trustProjectOwner` (Config2 has neither key, and refuses additional properties) is refused at resolution, before item 5 and any walk. No waiver is recorded.
- **`a_workspace_root_flag_wins_over_the_project_configuration_and_never_falls_through`** (`--workspace-root`).
  - Over a project configuration naming `a`, the flag `b` wins. Its provenance is the flag layer (`Layer::Flags`, `ProvenanceSourceV1::Flags`). The source is `config-workspace-roots`, with the one unit `b`.
  - An absent flag root refuses `PROJECT.EXPLICIT_PATH_INVALID`/`ABSENT` after the walk. The refusal's record keeps `config-workspace-roots`, with no units: no fall-through to automatic.
- **`the_configuration_alone_gives_its_roots_and_neither_gives_automatic`.** The configuration's roots come with carrier provenance. Without either, the source is automatic with both units.
- **`a_resolution_refusal_never_reaches_item_5_or_the_walk`** (the control r2 added). A refused pack, and an empty flag value, each end at resolution.
- **`selection_and_discovery_lend_nothing`.** The records are plain cloneable values with a V3 inventory, and a second discovery of the same root opens a new writer.

COV's owner path, `crates/host/tests/discovery_tests.rs`, stays planned for J1's public composition (plan r3; plan r4 LD-B2B-7).

## Check lanes

The evidence is lane r3, over the r2 candidate. Lane r2 was the r1 candidate's. Lane r1 (kept in the work directory) failed two rows:
- **Host suite.** B1-a's configuration source pin failed three tests, because r1 included the rows from `configuration.rs`'s test module. The module moved to `lib.rs`.
- **rustfmt.** `scenario.rs` was not formatted. It now is.

See `evidence/checks.json`. The rows are:
- the security and host suites at base and candidate, with equal failure sets and at least seven new passing host tests;
- the B1-b legacy admission spend probe;
- warning-denied all-targets Clippy;
- rustfmt on base-clean and new edited files;
- the environment pin, all three vector checks, the FW-01 pin, the configuration tables, the operability census and verify_design;
- eight code mutations, each caught:
  - `resolution-refusal-continues`;
  - `flag-roots-ignored`;
  - `waiver-not-recorded`;
  - `selection-refusal-dropped`;
  - `flag-layer-not-resolved`;
  - (r2) `end-failure-hidden`;
  - (r2) `end-not-recorded`;
  - (r2) `accepted-inventory-skipped`.

## Not claimed

- No production caller and no public composition (J1).
- No host `discovery.rs` and no export (B2-c).
- No `explicit-joins` producer (M4).
- No T2 census (B2-b4).
- No qualification.

B2-b3 is complete with this unit. B2-b is not complete: B2-b4 and its all-entry margin gate remain.
