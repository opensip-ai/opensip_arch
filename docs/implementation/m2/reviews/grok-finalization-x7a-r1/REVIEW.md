# X7a r1

Claude Opus 5.5 leads. Grok is the single reviewer. Worktree `/Users/sb/code/opensip-ai/opensip-x7a` is detached at `81214cb234e75b33e5437b30036c4c157267868b`. Law is X7 r5, items 1 to 5 and 8, with item 10's injected-outcome tests. No repository edits. `~/Library/Application Support/OpenSIP` is absent. The private 413 fixture was not read.

Verdict: **ACCEPT-UNIT**. Inventory v125 is **ACCEPT** on v124. None of judgment calls 1 to 18 needs a law change. Calls 4, 5, and 16 are readings to record in X7's next record-only revision, as the lead recommends.

## Product

`product.diff` is 61780 bytes, sha256 `919e18cc8bd583248c3b4c1d4995ce26137f8867b8981c7a9f42be1b0a522063`, 14 files, matching hashes.txt. The eleven new files are intent-to-add. The diff hash was the same after the replay.

`finalize` is the one coordinator, macOS-only, `#[allow(dead_code)]`, and uncalled from any CLI. Its order is replay with `REPLAY_LIMITS`, then the caller's `admit`, then `CommitSession::open`, `prepare_commit`, `publish`, then `StoppedSession::finish` on every path that holds a stopped session, then delivery only for `Committed` that is not latched. A replay refusal returns before admission. An admission refusal is that row alone, with no session and no delivery. Open's refusal finishes the stopped session and projects the refusal. The matches on `CommitOutcome`, `NotPrepared`, `Concluded`, and `Delivery` have no wildcard arm.

The delivery phase is the caller-supplied `DeliveryPhase`. `finalize` lends it `&PublishedCommit` only. It builds no lease, receipt, or read session. `render` runs only after `finish` has consumed the stopped session. A rendered exit outside {0, 1, 3} fails before any byte. A required failure does not retry and does not run the optional effect. An optional failure is `optional_failure` beside an unchanged exit. `x7.delivery.required` and `x7.delivery.optional` are the two fallible crash-barrier points.

`authoritative_run(&PublishedCommit) -> AuthoritativeRun` is the one exported constructor. The type derives `Debug, PartialEq, Eq`, keeps its field private, and is re-exported from the host root. `ephemeral_run` stays `pub(crate)` and returns `ephemeral` with no RunId. The after-commit remedy is the reference projection's text, verbatim: `the Run is committed; rerun the renderer with this runId`.

Rows:

| Outcome | Projection |
|---|---|
| Delivered commit | `Authoritative`, exit 0, 1, or 3; optional failure beside it |
| Required failure or latch | operational-failed, exit 4, `DELIVERY.REQUIRED_FAILED`, `delivery-required`, `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`; RunId retained; no namespace |
| `CommitUndetermined` | durability row; ExecutionId subject; namespace beside it; no RunId; later read-only recovery, no retry |
| `ExistingAttempt` | invariant row; ExecutionId subject; namespace beside it; later recovery with the requested binding; no `recover` in this invocation |
| `Refused` | `installation_termination` of that row, unchanged |
| `CarrierCapacityExhausted` | busy row, `PROJECT.BUSY`, subject N; no extra remedy string |

`REPLAY_LIMITS` has exactly one production caller, `finalization.rs`.

## Judgment calls

1. No pack parameter, and `finalize` does not call `admit_policy_selection`. Pack admission stays on the analysis request, before evaluation (X12 items 8 and 9). The zero-row release registry would make a required `&AdmittedPack` uncallable. Accepted.
2. `admit: FnOnce() -> Result<ProjectOperation, InstallationTermination>` runs only after a successful replay. Taking a `ProjectOperation` by value would admit first. Only security can build one. Accepted.
3. On `CommitUndetermined`, finalization calls `finish` and reports the durability row. It does not reconcile, append, or copy a floor itself. At this base, `finish` after an uncertain outcome appends nothing and does not enter the end step (X3d r6 item 7, X3b r10). Accepted.
4. `finish` already passes `JournalOutcome::Exhausted` into `ProjectOperation::end`, and that end step runs the rollover that X3b already integrated. X7a must finish every end path, so it does not grow a second route, admission, gate, or fence. It projects item 6a's busy row. Item 11's "with no rollover" is this unit adding none of the item 6 route. X7b keeps that route's disclosure and the rollover tests. Accepted. No law change.
5. `end_failure` is `SessionEnd::settlement_failure()`, which is the failed `REV`/`CLN` settlement X3d item 9 names, and it never rewrites the outcome. `OperationEnd` (the end step, including a rollover failure) is `pub(crate)` in security, and the accessor that returns it is `cfg(test)`. Disclosing that row needs a `SessionEnd` accessor. That belongs with X7b, which owns the rollover rows. Accepted as a reading. No law change.
6. F16 and F39 share `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` with the RunId. The termination schema requires that detail when a `runId` is present and forbids `DELIVERY.REQUIRED_PROJECTION_FAILED` beside one. The remedy matches `delivery_required_termination`. Accepted.
7. No registered remedy string exists for `DURABILITY.COMMIT_FAILED` or the F34 invariant row. The two constants say later read-only recovery, no retry, and F34 names the requested binding. That is the content X7 r5 items 3 and 5 fix. Accepted.
8. The exhausted row's subject is N. Finalization observes no holders, so it names none. S7's retry is the busy row's own rule, and finalization attaches no extra remedy string, as it attaches none to the other X3d rows. Accepted.
9. The phase reads nothing from the store. The source pin requires the two commit-facade `use` lines and refuses a lease, read entry, read receipt, read session, `SharedRead`, `installation_read`, `doctor_report`, `join_ledger`, `RecoveredCommit`, store root, `std::fs`, or `File::`. Accepted.
10. Optional failure is a slot after required success. The implementations are M3's. Accepted.
11. The two `x7.delivery` points match the scope item 5 of the pinned crash-matrix law still states (`required` and `optional`, both fallible). An injected fault becomes that step's own failure. Accepted.
12. `Committed` and `CarrierCapacityExhausted` are not constructible in host tests. `project` covers every row, `Joined::from` covers every outcome a caller can build, and `deliver` is tested over `()`. There is no `cfg(test)` constructor. The child module writes the `AuthoritativeRun` literal. Accepted.
13. X8 r3 assigns X7a rows A and B and the export of the authoritative projection. Exporting `AuthoritativeRun` adds D, E, and G. There is no non-public inherent function and nothing `cfg(test)` returns one, so no F case is owed. `EphemeralRun` is not an X8 owner row and stays `pub(crate)`. Accepted.
14. Today `NotPrepared::ExistingAttempt` is `{ execution_id: String }`. The arm binds `{ execution_id, .. }`, so it compiles when X6b adds `requested`. What is disclosed now is the ExecutionId as subject and the session's N beside the row. N is the namespace storage will put in `requested.namespaceId`. The store-generation digest, carrier digest, and operation reference are disclosed by whichever of X6b and X7a integrates second. Recomputing the digest in the host is rejected. This is X7 r5 item 10's in-flight rule. Accepted. No law change.
15. The X5a pin now requires exactly one `REPLAY_LIMITS` caller, and `finalization.rs` is that caller. Accepted.
16. A host test cannot build a `ProjectOperation`. X9 r1 gap G1 still stands: `crash_matrix_support` and `scenario-fixtures` are not integrated. What this unit runs for real is the replay inside `finalize`: a missing-blob refusal ends before admission, and each of four admission rows runs once after a lawful replay. The session rows (committed and delivered, renderer failure, latch, undetermined with N, `ExistingAttempt` with its binding, exhaustion through `finish`) wait for X8c, X9-5, or an X7a-2 after X9-1. Accepted. No law change.
17. `Finalization` returns the row, the retained RunId, the remedy this unit owns, N where a later recovery needs it, and the disclosures. Envelope rendering is X11 and M3. Accepted.
18. The ExecutionId is the subject on the durability row and the F34 invariant row. Only those two rows carry `namespace`. The busy row puts N in the subject. Accepted.

## X8

Nine cases, census rows owned by X7a in `admission_tests.rs`. A is `JsonValue` into `authoritative_run` (E0308, mismatched types). B is `true`, a RunId `&str`, and `&ReplayedRun` (E0308 each). D is the private-field literal (no code, the private-fields fragment), `Default`, and `Deserialize` (E0277). E is `Clone` (E0277). G is `Serialize` (E0277). The driver directory holds 106 cases and 8 self-tests, and `opaque_api_misuse_fails_for_the_intended_reason` passed, which runs the census and every case.

## Inventory v125

Parent v124 is 497254 bytes, sha256 `94d374791cda35d373d846c2c843439ee7df188f01f1c6dc929e79c4ddc1360c`, the inventory the worktree lock selects. v125 is 506284 bytes, sha256 `1d157eea04974577502cc584b611c1ad77953214ca153eb1e14e514289df2d10`. `successor.json` is 145787 bytes, sha256 `b51be162fadc1b52b655ded2ac58736db1d025562e86a49adfeefed6c02fbc36`. The subject manifest is 2110 bytes, sha256 `41aadbe025b049a52b14fb3ece671b614f6dd263e32bc59d908d45521b25444b`.

934 files. The 924 v124 rows are equal by value, including the planned `finalization.rs` row. Ten files are added: `finalization_tests.rs` and the nine cases. Packages, dependencies, and pending decisions are unchanged. The 55-row projection keeps the same paths, the same `before` text, and the same effective descriptions. Parent selectors are v124's candidate selectors. Fifty candidate selectors move with the ten insertions; five files that sort before the insertions keep their index (`bootstrap.rs`, `package.json`, and the three `doctor_*` rows). No supersession names v124. A rerun of `build_v125.py` against the worktree lock, with its two writes redirected out of the architecture tree, reproduced both files byte for byte and reported `supersessionsFolded: 0`.

The README names the descriptions this unit leaves stale: `finalization.rs` (the planned row still speaks of routing exhaustion through lifecycle rollover and of `outcomes.rs` for the analysis projection), `fact_admission_tests.rs` (still says the caller pin is vacuous until X7a), and `admission_tests.rs` (the effective census list stops before X3d-2, X5a, and X7a). Those stay for a later description-only successor.

## Replay

Private `TMPDIR` was `$(getconf DARWIN_USER_TEMP_DIR)/grok-x7a-tmp`, mode 0700. `CARGO_TARGET_DIR` was under this review directory. Both were removed after the runs.

- `opensip-host` lib: 21 finalization tests and the two `REPLAY_LIMITS` pin tests passed (23 passed, 119 filtered).
- `opensip-host` clippy `--all-targets -D warnings` is clean.
- `rustfmt --edition 2024 --check` is clean on `finalization.rs`, `finalization_tests.rs`, `fact_admission_tests.rs`, and `lib.rs`.
- `admission_tests`: 6 passed, including the misuse driver over the 106 cases and 8 self-tests.
- `verify_projection` against the worktree lock: 55 rows, PASS, 278 corruptions refused.
- `verify_scratch`: passed, 85 inventory successors, 74 contract successors, 55 inheritance rows, v125 selected.
- `check_package_edges --lane host` passed against v124 and against v125, 20 declared and 20 resolved edges.

The full workspace suite, workspace clippy, and `cargo fmt --all` were not replayed.
