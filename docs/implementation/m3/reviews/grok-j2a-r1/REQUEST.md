Grok review: unit **J2a** r1 of the accepted host-pipeline law M3-J1 r5 — the pure invocation model (`invocation.rs`) and the M3 outcome matrix (`outcomes.rs`) — with inventory v137 on v136. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT** on the code and inventory v137, with an `inventoryCandidateAssessment` (`review.json`). J2a binds no contract successor.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok-j2a-r1`.
- You own the native lane for this review:
  - Use a `CARGO_TARGET_DIR` under that directory.
  - Use a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
  - Lanes are serialized with other agents through the lock directory `$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock`: take it with `mkdir` before each build, test or clippy run and `rmdir` it straight after; if it is held, wait with a background poll.
- **The generator is shared.** Before the drift check, check that no other `opensip-contract-generator` or `generate_contracts.py` process is running.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- No crash-matrix lead run set is needed or wanted (see "Pins checked", X9).

## Inputs

All inputs are pinned in `hashes.txt`. Laws and plans are pinned by their accepted snapshots, never by a live `PROPOSAL.md`.

### Law, successors and plan

- **The law: M3-J1 r5** (`m3/host-pipeline-j/PROPOSAL-r5.md`, 146331 bytes, `4ccb2320…7599`, Codex's r5 ACCEPT, `reviews/codex-host-pipeline-j-r5`). The live file is these bytes plus the acceptance note.
  - **Item 14, J2a's row** (:878): "`host/src/invocation.rs`: the typed request, the step lists, the join state machine, settlement, the cancellation source and phase recording. `outcomes.rs`: NE §10's deficiency-to-D9 bridge, the route and origin tables (NE:3364-3374, :3523-3575), and item 10's total projection. Pure, with no I/O. Tests: the WFC cases and D9 goldens." Depends on P0 and J1, both met.
  - The items J2a's code implements: 1 (the M3 request type), 4 (R1, R2), 5.1 to 5.3 and 5.5, 6's cancellation clause, 8.2 to 8.5 (the model, not the wiring), 10 (the matrix and its totality rule), and the S20 row.
- **SD-5** (`m3/supervisor-d/sd-5/`, Grok ACCEPT-DESIGN-UNIT, bound at product `052d3cb`): NE §10's row after NE:3540 for R10a's and ER10a's manifest-class `ExcludedForm`; LD-S4 (the one detail) and LD-S5 ("J2a selects this remedy by the `excluded-form:` subject prefix").
- **SD-7** (`m3/supervisor-d/sd-7/`, GROK2 ACCEPT-DESIGN-UNIT r2, bound at product `d2c00a9`, the first contract passage supersession): the conformed SD-5 row and remedy, item 25's request-class row on NE:3539, and `PROVIDER.NOT_SELECTED`'s widened remedy.
- **M3-D r5** (`m3/supervisor-d/PROPOSAL-r5.md`, `224b9228…`, Grok ACCEPT): item 22 (settlement causes to existing routes), item 24 (R10a's refusals), item 25 (request-class refusals, LD-R4-2), item 29 (SD-5b, SD-7) and X-D4-J1-1's row 57, given word for word (:1219-1223).
- **S18 and S21** (bound at product `5214350` and `3f6f9a5`): WS:225-231's final output section and settlement point; WS:226's commit-outcome exception. J1 r5 gated rules 1 and 2 for a signal on S21 outside J2a's pure model; S21 is now bound.
- **M3-PLAN r9** (`m3/M3-PLAN-r9.md`, `72bc7a13…`, GROK2): the M3-J row (:265) and J2a's timing row (:448), "J2a: P0, J1".
- **M3-B r2** (`m3/config-discovery-b/PROPOSAL-r2.md`, `92e65825…`, the snapshot J1 cites as M3B): item 3's `InvocationModeV1` (:108-122) and item 23's flag table (:720-730).

### Contract references the tests restate

| Short name | Document | What J2a takes from it |
|---|---|---|
| WS | `docs/v2/contracts/product-v1/workflows-and-surfaces.md`, with S18's and S21's bound lines | §1's step-list rules (:95-111), cancellation (:224-231), aggregate (:233-240); §9's exit table and goldens (:1353-1393) |
| NE | `docs/v2/contracts/product-v1/native-evidence.md`, with SD-5/SD-7, FA-1 and SYN-1 bound | §10's bridge (:3364-3394), route table (:3523-3541, with SYN-1's row after it) and origin table (:3569-3579) |
| NES | `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `x-opensip-public-route-registry`: 16 keys, origins, envelope details, `subjectBoundLaw` |
| NEM | `m3/config-discovery-b/b-s9/reference/native_evidence_model.py` (B-S9's selected copy; SD-7 overrides line 1159) | `public_termination_for`, `bounded_subject`, `DEFICIENCY_TO_D9_DEFICIENCY` |
| RTC | `docs/coop/design-corrections/foundation/run-termination-contract.v1.md` | §4's ordered deficiencies; §7.4 authority; §7.5's detail allowlist |
| D9 | `docs/coop/artifacts/d9-exit-contract.v1.14.json` | `classToExitCode`, `codeMaps`, the goldens |
| WFC, CINV | `docs/coop/design-corrections/workflows/{workflow-cases.v1.json, command-inventory.v3.json}` | the invocation cases; the commands' flags |
| WFM | `docs/coop/design-corrections/workflows/workflows_model.v1.py` | `validate_dag` and the aggregate in `run_invocation` |
| OPP, SOP2 | `m3/operability/PLAN.md`; `m3/operability/s-op-2/PROPOSAL-r6.md` (`ce8d3a4b…`) | §5.2's rows (:283-298); `host.signal.received` (:871) |

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-j2a`, detached at main `d2c00a9` (SD-7; 97 contract successors, 96 inventory successors, v136 selected). Nothing is committed. The three new files are intent-to-add, so `git diff d2c00a9` includes them.
- **Diff:** `git diff d2c00a9` is 483391 bytes, sha256 `29cc56716f847d881007c845bfc65294ce9f35cfb102b2e485e7c2107b846b76`. It covers 6 files, +5268 −386: the five host sources +4819, and the staged `design-lock.json` +449 −386.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`; Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`; generator `~/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator`; Node `~/.nvm/versions/node/v24.16.0/bin/node`. The worktree also holds the ignored `tools/contracts/node_modules` and `tools/contracts/python-packages`, copied from the main checkout for the drift check.

### Inventory (arch, untracked)

All under `docs/implementation/m2/`:
- `repository-file-inventory.v137.json` (candidate; parent v136, which the lock at `d2c00a9` selects);
- `host-invocation-j2a-inventory-v137/` (README, builder, lock stager, scratch verifier, projection verifier and its outputs, verifier anchor, successor record);
- `host-invocation-j2a-inventory-v137-subject.json`, sha256 `8288fd26bc040d588a5f94ddd50dd6f1811806dd3bcdc972e202e6eed18d5f62`;
- `host-invocation-j2a-inventory-v137-unit.json`, a DRAFT-PENDING-REVIEW record the lead completes at integration; not in the subject.

**Parallel unit.** E2a's inventory successor is to be rebuilt on this candidate as v138. J2a's file set is final.

## What J2a changes

| File | Change |
|---|---|
| `crates/host/src/invocation.rs` (new; a row planned since the original inventory) | The pure invocation model (below). |
| `crates/host/src/invocation_tests.rs` (new) | Its cfg(test) module: 22 tests. |
| `crates/host/src/outcomes.rs` | The metadata ingress is unchanged. Appended: item 10's total projection, the deficiency bridge, the route and origin tables, and WS:233-240's aggregate. |
| `crates/host/src/outcomes_tests.rs` (new) | Its cfg(test) module: 15 tests. |
| `crates/host/src/lib.rs` | `mod outcomes` gains `#[allow(dead_code)]`; `mod invocation` is declared the same way. Nothing new is public. |
| `design-lock.json` | The staged inventory137 binding (see "The staged lock"). |

Nothing else changes: no other crate, manifest, `Cargo.lock`, feature, schema, generated file, `apps/cli` byte, crash point, census point or X9 source. J2a has no I/O, no process, filesystem, clock or signal effect, and wires no analysis word into the binary (J1 item 1). Production code in `outcomes.rs` and `lib.rs` names none of X11a's forbidden symbols (J-C1; `creator_commands_tests.rs` passes unchanged).

### `invocation.rs`

| Part | J1 | What it is |
|---|---|---|
| `AnalysisRequest` | 1 | Exactly `Default`, `Analyze`, `AnalyzeEphemeral`. `fit`, `audit` and `default --ephemeral` are not representable. |
| `InvocationModeV1`, `OutputFormat::Json`, `RequestFlags` | 1, 4 (R1) | M3-B r2 item 3's observation; the one M3 format; the parsed values of the five item 23 flags CINV gives `default` and `analyze` (`--project`, `--workspace-root`, `--trust-group`, `--trust-project-owner`, `--allow-backup-custody`), carried typed to their owners, never admitted here. |
| `AdmittedRequest::admit` | 4 (R1) | Builds the step list and checks it; a failing host-built list is row 2 with its workflow key in the operational record. |
| `AdmittedRequest::installation_entry` | 4 (R2) | `request.rs`'s exhaustive table: `Creator`, `Creator`, `Outside`. |
| `StepList::for_request` | 5.1 | `[analysis (required, [], completed, none, durability, live-worktree), render (required, [0], terminal, none, json, required)]`; no `import` step. |
| `check_step_list` | 5.1; WS §1 | 1 to 64 steps; at most 8 unique lower dependencies; `terminal` only on `render`/`export-delivery`; no required step on an optional one; `idempotent-retry` only on retryable kinds. Keys spelled as WFM's `validate_dag`. |
| `Join<Path, J>` | 5.2 | Consumed tokens: durable α→β→γ→δ→ε→ζ→η→θ→ι, ephemeral α→β→δ→…→θ. A join can be neither re-entered nor skipped (the previous token is moved); `refused` and `cancelled` end step 0 at any join. |
| `OperationPoint::phase`, `CancelPhase` | 8.2; LD-r5-1 | A to E and O. A `publish` return that does not enter D is C when the close's sample shows admission (state 1 or 3), else B. |
| `CancellationSource` | 8.2, 8.5 | Classifies each signal in memory: `SignalRecord {signal, ordinal, phase}` (SOP2:871's fields) and an effect: `Cooperate` (A), `Latch` (B, C), `CancelAtDecisionPoint` (D), `Force` (a later signal before the decision point), `Defer` (O), `Record` (E). The first signal before the decision point decides. It keeps two counters, not a list. |
| `Decision::decide` | 5.3, 8.3, 8.4; S21 | The output decision point. Rules 1 to 4, matched on step 0's commit evidence (an exhaustive classifier with no wildcard arm), never on the gate's state. With a signal, step 1 is cancelled for a termination output; with none, step 1 renders the aggregate. |
| `Decision::renderer_failed`, `output_failed`, `output_returned` | 5.3, 8.4; S18 | Phase O: a renderer failure before any byte fails step 1, even a cancelled one, on row 43 (a `PublishedCommit` exists) or row 44, and the aggregate replaces the envelope; an uncertain step 0's ExecutionId and namespace stay disclosed beside it (`Uncertain`). A failure envelope that cannot be rendered, and a failed write or flush, end undelivered (exit 4, no replacement). The output's return is the settlement point. |

### `outcomes.rs`

| Part | J1 | What it is |
|---|---|---|
| `Termination` | 10 | Item 10's columns: class, error code, fault cause, reason codes, detail and subject, signal, runId, executionId, authority, coverageId, the namespace disclosed beside, and the internal keys for the operational record. The exit derives from the class by WS's fixed table only. `remedy` is set only where a bound successor makes J2a select it. |
| `Observation`, `project` | 10 | One variant per row family; one exhaustive match, no wildcard arm. Owners that already project their rows are lifted unchanged: `installation_termination` (468, X2, X3a, X4T, X4, X3d), `policy_selection_termination` (X12), `replay_termination`'s value (X5). Rows 1 and 49 after admission have no termination (`request_identity_unallocated`, `host_panic`). |
| `native_deficiency_d9`, `reason_code`, `Deficiencies` | 10 rows 27, 31, 33, 35; NE:3380-3394; RTC §4 | The bridge (five self-maps, four to `verdict-indeterminate`), D9's reason map, and ordered distinct deficiencies (never `none`). |
| `AnalysisOutcome`, `Verdict`, `EphemeralVerdict`, `AnalysisDetail` | 10 rows 27, 31, 33, 35; RTC §7.4-7.5 | A committed Run carries its runId and no authority; an ephemeral result carries `authority: ephemeral`, no runId and no detail; a committed indeterminate carries the §7.5 detail its composition selected. |
| `NativeRefusal` and its key families, `SpecOrigin`, `bounded_subject` | 10 rows 26, 32, 55; NE:3523-3579; NES | The 16 registry keys, typed by origin family so an impossible origin is unrepresentable; a detail only where the registry names one (subject: the bounded raw guard string), else the raw string to the operational record; each key's `envelopeDetail`. |
| `ExcludedManifest`, `ManifestDigest`, rows 56 and 57 | 10, S20; SD-5, SD-7; M3-D r5 items 24, 25 | Row 56: request-rejected 2, `EXTENSION.ADMISSION_REJECTED`, `PAYLOAD-NOT-ADMISSIBLE`, subject `excluded-form:<class>:<manifestDigest>` of the least digest then the first class, SD-7's conformed remedy, every refusal in the operational record, no ids. Row 57: request-rejected 2, `REQUEST.UNSATISFIABLE`, `PROVIDER.NOT_SELECTED`, subject `excluded-form:<class>` of the first class, the widened remedy. |
| `StepResult`, `aggregate` | 5.3; WS:233-240 | Over required, non-skipped steps: operational-failed > request-rejected > policy-failed > indeterminate > success; ties keep the first termination with a detail, else the first. |

## What J2a implements of J1, and what it leaves

**Implemented here:**
- **Item 1:** the M3 request type, JSON, `InvocationModeV1`; no selector of home, profile or release; nothing in `apps/cli`.
- **Item 4:** R1 (J2a's) and R2.
- **Item 5:** 5.1's step lists with retry `none`; 5.2's join chain; 5.3's step outcomes, aggregate, step terminality, settlement point and decision point; 5.5's forbidden substitutes in J2a's reach (another step list, a retry, a re-entered join, a refusal with no route).
- **Item 6:** the cancellation clause only. An ephemeral request is A up to its decision point, then O and E.
- **Item 8:** 8.2's phases with O and LD-r5-1, 8.3's rules 1 to 4 (lawful outside J2a's pure model too since S21 bound), 8.4's decision point and phase O, and 8.5's `Force`.
- **Item 10:** rows 1 to 57, except 41 (S-OP-8 is not accepted; J-C20 skips it), 45 (a disclosure beside the outcome, which X7's finalization already carries), 48 (the settlement model) and 50 (never a termination). Rows 51 and 53 are not reachable at M3 but fully specified, so they are projected and tested. The totality rule, S20's row 56, and row 57.
- **Controls:** J-C1 (X11a's pins stay green); J-C20's projection half, one test row per item 10 row; the pure halves of J-C14, J-C14b and J-C14c; the WFC cases and D9 goldens of item 14.

**Left to the other units** (J1 item 14):
- **J2b:** J-δ to J-θ, the shared analysis core, S19's closure selection and H's admission. The run-termination contract's derivation of a Run's ordered deficiencies (§4) and its §7 composition, which feed `AnalysisOutcome`, have no named unit (not-settled item 4).
- **J2c:** the ephemeral entry end to end (E-1 to E-4 through S7b; ER10a's wiring with D4), its output wiring, and J-C14c's O and E cases wired.
- **J3a:** `RequestIdentity`, `ExecutionIdReservations`, the durable entry, its probe, the two-slot attempt, `EntryRefusal` and `created` (item 3), S2 to S7 and S10's item 2; J-C2, J-C4, J-C4b, J-C5 to J-C9 and J-C6b.
- **J3b:** the latch and window bits, `StopCause::Operator`, the REV reason, `InstallationTermination::Interrupted`, `finalize`'s new signature, step 1's terminality and the decision point inside X7's finalization, the close sample's admission bit carried to the host (J2a takes it as `PublishReturned { admitted }`), and S12-B, -C, -U and -D. Whether `finalization.rs`'s item 3 table delegates to `outcomes::project` is J3b's call; J2a does not touch `finalization.rs`.
- **J3d:** the durable pipeline R0 to settlement over this model; `opensip_host::invocation::run` and the module's `pub`; J-BS and item 9's `retentionDisclosure`; `workflow_tests.rs` with J-C10 to J-C21 and J-C20b end to end; the envelope (WS:1340-1344's `errors` composition, using `NativeRefusal::envelope_detail`, and every other remedy); SOP2's records of each `SignalRecord`; the coded standard-error lines; S12-O. The signal handlers are the M4 CLI unit's (item 1).

## Tests

All pure: no installation, home, lock, process, signal or file.
- **`outcomes_tests.rs` (15):** every item 10 row field by field, each termination validated against the selected common-v4 `StepTermination` (a shape-only placeholder stands in for remedies J2a does not select), with a check that the covered rows are exactly 2 to 57 less 41, 45, 48 and 50; D9's exit and fault pairing; the operational keys of detail-less rows; rows 1 and 49; row 56's selection under every discovery order, its classes, its 84-character subject and SD-7's remedy; row 57's selection and the 254-character widened remedy; rows 56 and 27 distinct; `ManifestDigest`; the bridge and D9's reason map restated; `Deficiencies`; the 16 registry keys across their origins, with envelope details; the subject bound (4096 non-ASCII code points → exactly 1024, key kept, SHA-256 of the UTF-8 bytes); 18 D9 goldens of the analysis path; authority on committed and ephemeral results; the exit table.
- **`invocation_tests.rs` (22):** the three requests, their step lists, flags and entries; the WFC step-list refusals (`forward-dependency-refused`, `duplicate-depends-on-refused`, `sixty-five-steps-refused`, `terminal-gate-on-analysis-refused`, `required-depends-on-optional-refused`, `mutation-never-retried-schema`, and four more) as row 2, and lawful lists passing; both join chains; every operation point's phase; the cancellation source; the WFC cases in M3's terms (`default-analyze-render-success`, `policy-failed-with-run`, `ephemeral-result-has-no-run-and-no-authority`, `indeterminate-provider-unavailable`, `operational-fault-dominates-committed-policy-failure`, `cancel-before-settle-is-interrupted`, `cancel-after-settle-not-reclassified`, `cancel-mid-invocation-with-committed-run` as phase D, `host-io-not-retried`); rules 1 to 4 (rule 1 at every point before the decision point, including a latch 1→3 then an undetermined evidence `COMMIT`); phase O's deferral; the renderer-failure routes by committed evidence and the uncertain disclosure; a termination output's renderer failure; the undelivered ends; J-C14c; and the aggregate on `policy-fail-dominates-indeterminate-across-steps`, `optional-export-failure-keeps-success` and `optional-import-rejected-then-analysis-skipped-but-render-runs`, with the tie rule.

## The staged lock

The lock change is staged in the worktree, as P0 staged inventory135 and X3a-2 staged inventory136 (`m3/reviews/grok-x3a2-r1/REQUEST.md`, "The staged lock"). `host-invocation-j2a-inventory-v137/evidence/stage_lock_j2a.py` writes HEAD's `design-lock.json` plus:
- one `inventorySuccessors` entry: parent v136, candidate v137, record `host-invocation-j2a-inventory-v137/successor.json`, all real pins. Its review `SCRATCH-J2A/review.json` (764 bytes, `34bf2fc8…0408`) and assent `SCRATCH-J2A/assent.json` (620 bytes, `7abfc1f1…6fb4`) are placeholders;
- `inventoryPassageInheritance` replaced by the one hundred and three rows re-parented to v137, exactly as the record projects them.

No contract successor is added. The staged lock is 515668 bytes, sha256 `fe776b81ed12de2cbd29b2e1310777b59f145f7bcd2fc71aed5244f1818fc3ff`, in the lock's canonical formatting. The placeholder bytes are those of `evidence/verify_scratch.py`'s synthetic overlay. At integration, the lead:
1. copies your review in, to `m3/reviews/grok-j2a-r1/review.json`;
2. completes the unit record;
3. replaces exactly the two placeholder pins;
4. runs plain `verify_design`;
5. commits.

**Plain `verify_design` on the staged lock refuses,** at `SCRATCH-J2A/review.json`, which is correct until review; `verify_scratch.py` asserts this refusal. So does the public `generate_contracts.py` on the staged lock. `design-lock.json` stays outside the unit's `sourceBoundary`, as in every earlier inventory unit; its staged bytes are pinned here, and the diff sha covers them.

## Pins checked

- **X9: no row moves, so no run set.**
  - The X9 harness sources (the checker and its test, `crates/platform`, storage's and host's `tests/` with both `required-runs.v1.json`, `commit_tests.rs` and `commit_matrix_tests.rs`, security's `crash_matrix_sites.rs`, `crash_matrix_census.rs` and `crash_matrix_support`, and storage's and host's `crash_matrix_support`) are untouched: the diff names only the five host files and the lock.
  - The diff adds no `crash_barrier!`, `crash_scope!`, clock sample, file write or `cfg(feature …)` site. X9-1's `every_test_feature_site_is_on_the_pinned_list` and X9-0's `no_manifest_enables_the_crash_matrix_feature` pass in both workspace runs.
  - **Exercised paths.** J2a's code is reached by no production path: both modules are crate-private and only their own tests call them. No crash-matrix row can reach it.
- **X11a (J-C1).** `creator_commands_tests.rs` passes unchanged in both workspace runs, its source pin over `outcomes.rs` and `lib.rs` included.
- **Dependency policies.** No manifest, lock or feature changes. Both checkers and their suites pass (Lead results).
- **Package edges.** Both new rows are in `opensip-host`. No crate declares a new edge.
- **Generators and lanes.** No generator input, schema or TypeScript lane source changes. The drift check on HEAD's lock reports `changed: []`.

## Lead results

All lanes ran serially on `d2c00a9` plus this diff, each under the lane lock, with a private 0700 TMPDIR, `nice -n 10` and `--locked --offline`. `~/Library/Application Support/OpenSIP` was absent before and after. E2a's agent and other agents ran their own lanes between these, under the same lock.

| Check | Result |
|---|---|
| `cargo fmt --all --check` | Clean. The two `_tests.rs` files are included modules, so `rustfmt --edition 2024 --check` was run on them as well: clean. |
| `cargo build --workspace --all-targets` | Pass |
| Clippy `-D warnings`, workspace `--all-targets` | Clean |
| Clippy `-D warnings`, platform, security, storage and host with `crash-matrix` | Clean |
| Clippy `-D warnings`, security, storage and host with `scenario-fixtures` | Clean |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1775 passed, 0 failed, 3 ignored (20 test binaries, 522 s). Main `d2c00a9` has 1738: the confirmation lane's 1758 on `988f6ed` less its 20 doc tests, and no later commit adds a Rust test. J2a adds 37: 15 in `outcomes_tests.rs` and 22 in `invocation_tests.rs`. |
| The same, run 2 | 1775 passed, 0 failed, 3 ignored (513 s) |
| `cargo test --workspace --doc` | 20 passed, as main |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast` | 1673 passed, 0 failed, 3 ignored (10 binaries, 534 s): main's 1636 (X4-F2's 1637 on `3f6f9a5`, less X3a-2's net two, plus I1-a's one host test) plus J2a's 37. Includes storage's `commit_tests` (8), host's `commit_matrix_tests` (5) and the census pins, without a run set. |
| X11a's source pin (`no_creator_gate_writer_pack_or_commit_symbol_reaches_the_binary_or_the_ingress`) | Passes in both workspace runs |
| `generate_contracts.py` drift check, HEAD's lock | Passes: 40 sources verified, 8 outputs, `changed: []`. The staged lock was restored afterwards, byte for byte. |
| `generate_contracts.py`, staged lock | Refuses: "missing or escaping regular file: SCRATCH-J2A/review.json" (exit 1). Correct until integration. |
| `evidence/verify_scratch.py` (staged mode) | Passes. Inventory successors 96 → 97 with v137 selected; contract successors 97, unchanged; inheritance 100 → 103, equal to verify_design's own projection; 21 inventory supersessions and 1 contract passage supersession, unchanged; 40 generation and 48 admission sources (15 aliases). Plain verify_design refuses the staged lock at `SCRATCH-J2A/review.json`, as asserted. |
| Plain `verify_design.py --architecture ../opensip_arch --implementation .` on the staged lock | Refuses: "missing or escaping regular file: SCRATCH-J2A/review.json" (exit 1) |
| Plain `verify_design.py` on HEAD's lock, same sources | Passes |
| `verify_projection.py` against the real lock at `d2c00a9` | PASS: 103 rows, 518 corruptions refused |
| `evidence/build_v137.py` rerun | Same bytes |
| `check_package_edges.py --lane host`, against v137 and against v136 | Both pass: 12 workspace packages, 22 declared and 20 resolved internal edges, none new |
| `check_package_edges.py --lane rust-provider` against v137 | Passes: `opensip-rust-provider` only |
| `tools/tests/test_package_edges.py` | 14 run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` | Passes: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | Passes: 8 dependencies, 305 sources |
| `tools/tests/test_dependency_policy.py` | 9 run, OK |
| `tools/tests/test_identity_dependencies.py` | 5 run, OK |

Commands, from the worktree, with `PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`, `PYAPP=/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python` (the generator's pinned interpreter), `CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo`, `AR=~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`, `U=../opensip_arch/docs/implementation/m2/host-invocation-j2a-inventory-v137` and `V=../opensip_arch/docs/implementation/m2/repository-file-inventory.v137.json`:

```sh
cargo fmt --all --check
rustfmt --edition 2024 --check crates/host/src/outcomes_tests.rs crates/host/src/invocation_tests.rs
cargo build --workspace --all-targets --locked --offline
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
cargo test --workspace --all-targets --no-fail-fast --locked --offline   # twice
cargo test --workspace --doc --locked --offline
cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast --locked --offline
cargo test -p opensip-host --lib --locked --offline -- outcomes:: invocation::   # J2a's 37
# drift: on HEAD's lock (git show HEAD:design-lock.json > design-lock.json), then restage with $U/evidence/stage_lock_j2a.py .
$PY -I -B tools/generate_contracts.py --architecture ../opensip_arch --output <fresh dir> --node ~/.nvm/versions/node/v24.16.0/bin/node --generator ~/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator --python $PYAPP
$PY -I -B $U/evidence/verify_scratch.py .
$PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .   # refuses at SCRATCH-J2A
git show HEAD:design-lock.json > head-lock.json
$PY -I -B tools/verify_design.py --architecture ../opensip_arch --lock head-lock.json --implementation .
$PY -I -B $U/verify_projection.py --architecture ../opensip_arch --lock ../opensip/design-lock.json
cargo metadata --locked --offline --format-version 1 > host.json
(cd providers/rust && cargo metadata --locked --offline --format-version 1) > provider.json
$PY -I -B tools/check_package_edges.py --repository . --metadata host.json --inventory $V --lane host
$PY -I -B tools/check_package_edges.py --repository . --metadata provider.json --inventory $V --lane rust-provider
$PY -I -B tools/tests/test_package_edges.py -v
$PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
$PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
$PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
$PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
```

## Inventory v137

- **Contents:** v136 plus two rows, both in package `opensip-host`, role `test`, not generated, standing `proposed`:
  - `crates/host/src/invocation_tests.rs`;
  - `crates/host/src/outcomes_tests.rs`.

  That gives 973 files, with the 971 v136 rows equal by value. The packages, their edges and the pending decisions are unchanged. Check the two descriptions against the tests.
- **Planned rows changed, by value unchanged:** `crates/host/src/invocation.rs` (new bytes for a planned row), `crates/host/src/outcomes.rs` and `crates/host/src/lib.rs`. No description successor: the two rows' planned texts ("Execute the bounded step/attempt DAG and apply dependency, retry and cancellation rules."; "… map typed host boundary observations and aggregate step outcomes under their existing owners …") still describe the files.
- **Projection: one hundred and three rows,** re-parented by stable file path: the lock's one hundred inheritance rows on v136 (sixteen carried from inventory81 onward, D1's thirty-nine with D2's four supersessions folded, D3's forty-five with its seventeen folded) and the three direct overrides of the bound `read-endpoint-x3a2-descriptions` on v136 (rows 122, 123 and 747 there). No supersession is folded. One projected row moves by one and eighty-seven by two.
- **Pins:**
  - candidate: 558538 bytes, sha256 `92226626700a9d44c2a22eea92526aea615cb9b15279169f8ec7e2e88665ce56`;
  - successor record (`host-invocation-j2a-inventory-v137/successor.json`): 308078 bytes, sha256 `b328eff63c1b186c7d3d8f30c0e6a628a7a4e5a4ce877fb514bb0d23f4c68004`;
  - parent v136: 555473 bytes, sha256 `ba124e21d23c8cd100eb2031203fd5c04fd8aeaab056872af54d1fa8c92bacea`.
- **Order:** the lock at `d2c00a9` selects v136. Since X3a-2's `cca4fe4`, three commits have landed (X4-F2, VD2-a with F8c, SD-7), none with an inventory successor. The lead reserved v137 for J2a; E2a's will be v138 on it.

## Not settled by J1, SD-5 or SD-7: left out, not decided here

The lead was told to stop and report anything the law and the two successors do not settle. J2a leaves each of these out and decides none of them. Each needs the owner named, not J2a. Please confirm that J2a decides none of them, and say if you find another.

1. **SD-5b's four refusals.** `MemoryBudgetBelowCeiling`, `ToolOutputBound`, `ToolScratchBound` and `confinement-refused` have no item 10 row: J1's S20 records them as "still owed", and M3-D r5 item 29 names SD-5b "not written". `Observation` has no variant for them. **Recommendation:** write SD-5b row by row with each first consumer, as M3-D r5 item 29 schedules (`MemoryBudgetBelowCeiling` before J2b's first provider stage, with D3a; the tool bounds with C3b; `confinement-refused` with D1b, and only if O7 is decided as recommended). Each row is then one `Observation` variant and one matrix row, in the consuming unit. None blocks J2a.
2. **SYN-1's routes.** J1 r5 records SYN-1's X-J1 and O-1 as pending and adds no row; SYN-1 has since bound (product `682991f`): NE:3530's row gains the `native.syntax-*` keys, and NE gains the "syntax backend fault" row (operational-failed 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, `HOST.INVARIANT_VIOLATED`, subject `native.syntax-backend-fault:<grammarId>`). J2a adds no syntax row or test. **Recommendation:** J1's next record revision records both, plus O-1's two native-context keys. J2a's vocabulary already expresses them without a code change: `NativeContextRefused { key }` is row 52's route, and `HostInvariant { subject: Some("native.syntax-backend-fault:<id>") }` gives exactly the backend-fault route. A one-line matrix test can pin the new row once J1 records it.
3. **E-3's ephemeral detail.** J1 row 27 ("including ephemeral with no trust, E-3") and item 6's E-3 recommendation give an ephemeral request with no trust view `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` as its detail. The run-termination contract's §7.4, which WS:1399-1414 makes the owner of a step termination's detail and authority, admits no §7.5 detail on an ephemeral attempt (`RUN_TERMINATION_DETAIL_NOT_ADMITTED`). `EphemeralVerdict::Indeterminate` carries no detail, so J2a cannot emit the conflicting form. E-3 is S7b's join (M3-C and X4T), and it gates J2c only. **Recommendation:** S7b's E-3 owner settles it with the run-termination owner. The lead leans to keeping §7.4 (an ephemeral indeterminate carries `COVERAGE.PROVIDER_UNAVAILABLE` and no detail, with the install remedy carried by the envelope's capability-availability disclosure), and J1's next revision narrowing row 27's ephemeral case to match. The alternative is a §7.4 successor admitting row 2 for an ephemeral attempt.
4. **Who derives the analysis projection.** J2a projects an `AnalysisOutcome` it is given: ordered distinct D9 deficiencies, a coverageId and a §7.5 detail. Deriving them from the admitted Run (run-termination contract §4 and §5) and composing the whole analysis termination (§7, `admit_analysis_step_termination`, which needs the commit receipt) is named in no J1 unit row, although `outcomes.rs`'s planned row describes it. **Recommendation:** J3d for a committed Run, since §7.2's inputs include the commit receipt and the finalizer composes the termination; J2c for an ephemeral result's reasons through the bridge J2a already provides. Record it in J1's next revision's item 14.

**Record items, settled elsewhere and implemented:**
- **Row 57 is not in J1 r5.** J1 r5 item 10 left item 25's route to M3-D r4. M3-D r4 decided it (LD-R4-2) and r5 gives the row word for word (X-D4-J1-1); SD-7 binds NE's row. J2a implements it from those. J1's next revision owes the row, R1's sentence ("A well-formed request that is a request-class excluded form is not malformed; it takes row 57"), and S20's update (X-D4-J1-2).
- **J1 r5's S21 gate** (rules 1 and 2 for a signal) is met: S21 bound at `3f6f9a5`.

## Lead rulings on the unsettled items (Claude Opus 5.5, before sending)

These are lead decisions under the owner's standing direction. None changes J2a's code. Each is routed to the law named.

| Item | Ruling | Routed to | Rejected |
|---|---|---|---|
| 1, SD-5b | **Accepted as recommended.** SD-5b is written row by row with each refusal's first consumer, as M3-D r5 item 29 schedules. Each refusal then adds one row to `outcomes.rs` and one matrix test. J2a carries no placeholder. | M3-D's SD-5b, per first consumer | Adding provisional rows now, which would need a law J2a doesn't have. |
| 2, SYN-1's routes | **Accepted.** J1's next revision records the `native.syntax-*` keys on row 52, the "syntax backend fault" row, and O-1's two keys. J2a's existing observations already express both routes. | J1 r6 (record) | None needed. |
| 3, E-3's ephemeral detail | **The run-termination contract's §7.4 governs.** An ephemeral attempt carries no detail, so J1 row 27 and E-3's `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` detail are corrected to fit §7.4. J2a correctly can't emit the conflicting form. | J1 r6, and M3-C r8 for E-3's C half (being drafted) | Changing §7.4 through a contract successor. A law cannot override the contract, and nothing needs the detail. |
| 4, deriving the analysis projection | **Accepted as recommended:** J3d derives it for committed Runs, because it needs the commit receipt, and J2c for ephemeral results. | J1 r6's item 14 (record) | Putting it in J2a, which would break J2a's purity. |

Judge J2a with these rulings applied. A disagreement with a ruling is a finding.

**Shared machine.** Other units' X9 lead sets run on this machine under a 5000 ms timing guard. Before any cargo build, test or clippy run, take the shared lane lock with `mkdir "$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"`, and remove it with `rmdir` straight after. If the lock is held, wait until it is free. Python-only lanes need no lock.

## Judgment calls

The lead accepts each as a lead decision (2026-10-04). Calls 1, 4 and 6 are where a reviewer could most reasonably differ.

1. **Nothing public yet.** Both modules stay crate-private under `#[allow(dead_code)]`, like `configuration.rs` and `fact_admission.rs` ("library only"). J1 item 1 makes the entry's name, `opensip_host::invocation::run`, J2a's; the entry itself does I/O, so it lands with J3d and J2c, and the module becomes `pub` then. **Rejected:** a public stub `run`, which would be an entry with no pipeline behind it. **Question:** do you agree that "the name is J2a's" is met by reserving the path?
2. **Placement.** `invocation.rs` is a row planned since the original inventory. `outcomes.rs` keeps the metadata ingress and takes the matrix and the aggregate, because its planned row reads "map typed host boundary observations and aggregate step outcomes under their existing owners"; the settlement model, which calls the aggregate, is `invocation.rs`'s ("settlement", item 14). The tests are two sibling `_tests.rs` files, the crate's convention, which is why there is an inventory successor. Neither planned row's description becomes false, so there is no description successor.
3. **The join chain as consumed tokens.** No runtime join-order fault exists, so none needs a route ("a refusal with no route" is forbidden).
4. **Remedies.** J2a selects only the two remedies a bound successor assigns it: SD-5 LD-S5's excluded-form remedy (as SD-7 conforms it) and `PROVIDER.NOT_SELECTED`'s code-keyed remedy as SD-7 widens it (rows 57 and the NOT-SELECTED cell). Item 10 has no remedy column; every other remedy, and the `errors` composition, are the envelope's (J3d, J2c). **Question:** is that the right line?
5. **Rows 53 and 54 carry their registered details; row 30 does not.** NE:3531-3532's carrier column names `native.prepare-bound-exceeded` and `native.ambient-cargo-config`, both registered, and NE:3546-3555 carries a registered member that names the condition; the key is also kept for the operational record, as J1's rows say. NE:3529's carrier column for a worker fault is "operational record", and J1 row 30 and M3-D item 22 say the detail is absent, so row 30 carries none although `native.worker-fault` is registered.
6. **The registry typed by origin family.** The three malformed-request keys and the NOT-SELECTED key take any `SpecOrigin`; the five release-declaration keys and the seven Coverage-cause keys take none, because each has exactly one possible origin (NES `possibleOriginsLaw`). An impossible origin is unrepresentable, so NEM's runtime `native.public-route-origin-not-possible` refusal has no host counterpart. **Question:** acceptable in place of a runtime refusal?
7. **Request flags.** CINV gives `default` and `analyze` five of M3-B item 23's seven flags, plus `--ephemeral`, which is the request itself. `--yes-policy` is carried by neither command and has no M3 consumer, so the M3 request type does not carry it. `InvocationModeV1` is defined in `invocation.rs`, where B1-a's resolver can take it.
8. **Smaller readings.**
   - Row 34 carries no runId: evaluation (J-θ) precedes the commit (J-ι), so no Run exists.
   - Rows 38 and 39 put the ExecutionId in `subject` as well as `executionId`, as X7's item 3 projection does; row 38 has no detail.
   - D item 22's `host-fault` for a host bug takes row 2's route (NE:3573), its I/O case row 23, its `session-spec-inconsistent` row 2, and its `abandoned` `host_panic`.
   - 8.3's rule 4 is applied as written to a committed, unlatched Run whose signal was labelled other than D. That pairing cannot arise when the source labels by `OperationPoint`.
   - Two D9 goldens list an executionId that item 10 does not carry (`user-interrupt-finite`, `analysis-provider-protocol-prevents-seal`): ENV7's interrupted branch and J1 rows 30 and 46 carry none, so only their class and codes are compared.
   - `ManifestDigest` is typed (64 lowercase hex), so SD-5's 84-character subject bound holds by construction. Duplicate refusals are recorded once.

## Decide

- **Faithfulness:** does J2a do exactly what J1 r5 item 14 gives it, within items 1, 4, 5, 6 (cancellation), 8 and 10, with SD-5's and SD-7's rows and M3-D r5 items 22, 24 and 25 projected as stated? Is it pure? Check the forbidden substitutes in J2a's reach: another step list, a retry, a re-entered join, a refusal with no route, a wildcard termination arm, a new public code, an analysis word in the binary.
- **Rerun:** run the lanes above yourself, each under the lane lock:
  - fmt, the workspace build and the three clippy lanes;
  - the workspace tests (twice if time allows), the doc tests and the crash-matrix feature lane;
  - the generator drift check on HEAD's lock (it refuses on the staged lock, as asserted);
  - `verify_scratch.py` in staged mode, and plain `verify_design`, which must refuse at `SCRATCH-J2A/review.json`;
  - both package-edge lanes against v137, `verify_projection.py`, and both dependency checkers with their suites.

  Also rerun `evidence/build_v137.py ../opensip/design-lock.json` (it writes only its own untracked paths; a scratch copy of arch is fine) and confirm the same bytes.
- **Not settled:** confirm items 1 to 4 above are left undecided, and name any other.
- **Judgment calls:** are calls 1 to 8 acceptable? Answer the questions in 1, 4 and 6 directly.
- **Inventory v137:** pin it, and assess it as an inventory candidate.

Write REVIEW.md and review.json under the output directory.

review.json needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `29cc56716f847d881007c845bfc65294ce9f35cfb102b2e485e7c2107b846b76`, the diff's sha256, as a single string;
- "subjectManifestSha256": `8288fd26bc040d588a5f94ddd50dd6f1811806dd3bcdc972e202e6eed18d5f62`, as a single string;
- "inventoryCandidateAssessment": verdict, requiredFindings, the candidate's path, bytes and sha256, parent (v136's pin), and successorRecord (the pin of `host-invocation-j2a-inventory-v137/successor.json`).

Do not commit.
