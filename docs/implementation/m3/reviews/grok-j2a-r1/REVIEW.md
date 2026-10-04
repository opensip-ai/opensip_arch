# J2a r1

Verdict: **ACCEPT-UNIT** on the code and inventory v137 (`review.json`). No contract successor.

Product worktree `/Users/sb/code/opensip-ai/opensip-j2a`, detached at `d2c00a96c3136fe45b901bc067b6d0ca51f0c9c1`. `git diff d2c00a9` is 483391 bytes, sha256 `29cc56716f847d881007c845bfc65294ce9f35cfb102b2e485e7c2107b846b76`, six files. Every pin in the request's `hashes.txt` matches, including the law snapshots J1 r5 (`4ccb2320…`, item 14 at :878) and M3-D r5 (`224b9228…`).

Inventory subject `docs/implementation/m2/host-invocation-j2a-inventory-v137-subject.json` is 2357 bytes, sha256 `8288fd26bc040d588a5f94ddd50dd6f1811806dd3bcdc972e202e6eed18d5f62`. Candidate `repository-file-inventory.v137.json` is 558538 bytes, sha256 `92226626700a9d44c2a22eea92526aea615cb9b15279169f8ec7e2e88665ce56`. Parent v136 is 555473 bytes, sha256 `ba124e21d23c8cd100eb2031203fd5c04fd8aeaab056872af54d1fa8c92bacea`. Successor record `host-invocation-j2a-inventory-v137/successor.json` is 308078 bytes, sha256 `b328eff63c1b186c7d3d8f30c0e6a628a7a4e5a4ce877fb514bb0d23f4c68004`.

The staged lock is 515668 bytes, sha256 `fe776b81ed12de2cbd29b2e1310777b59f145f7bcd2fc71aed5244f1818fc3ff`. Its review and assent pins are the `SCRATCH-J2A` placeholders. Plain `verify_design` refuses that lock with `missing or escaping regular file: SCRATCH-J2A/review.json`. After the drift check the same staged bytes were restored.

## What the diff does

The diff names `crates/host/src/invocation.rs`, `invocation_tests.rs`, `outcomes.rs`, `outcomes_tests.rs`, `lib.rs`, and `design-lock.json`. `lib.rs` inserts the two private modules under `#[allow(dead_code)]` and leaves the existing public exports unchanged. `outcomes.rs` inserts a header and the imports the matrix needs, then appends 986 lines after the 188-line metadata ingress. Every hunk is an insertion. The metadata functions stay as they were.

`invocation.rs` is the pure request, step list, join chain, cancellation source, and settlement model. The three requests are `Default`, `Analyze`, and `AnalyzeEphemeral`. The step list is analysis then render, retry `none`, no import. A host-built list that fails `check_step_list` is item 10 row 2, with the workflow key in the operational record. Joins are zero-sized tokens moved by value: durable α through ι, ephemeral without γ and without ι. `refused` and `cancelled` end step 0 at any join. Re-entry and skip do not compile.

`OperationPoint::phase` is exhaustive: A, B, C, D, O, E, and LD-r5-1's publish return is C when the close sample shows admission and B otherwise. `CancellationSource` classifies each signal, returns the `SignalRecord` to the caller, and stores the first pre-decision signal. A later A/B/C/D signal is `Force` and does not replace that signal. O is `Defer`. E is `Record`. The ordinal is one saturating counter.

`Decision::decide` matches commit evidence with no wildcard. With a signal, rules 1 and 2 project the observation, rule 3 is interrupted with the runId when the phase is D and the attempt is committed and unlatched, and rule 4 is interrupted with no runId. Step 1 is then a cancelled terminal step. With no signal, step 1 renders the aggregate of step 0 and a completed success. `renderer_failed` replaces the envelope once, keeps an uncertain step 0's ExecutionId and namespace on `uncertain`, and a second failure or a failed write is `Undelivered` exit 4. `output_returned` is the settlement point. Step 0 keeps its own termination beside the envelope, which is the line J3d's empty-errors interrupted envelope has to keep.

`outcomes.rs` projects one variant per row family in one exhaustive `project` match. Remedies are set on the excluded-manifest row and the `NOT-SELECTED` cell. `REMEDY_EXCLUDED_MANIFEST` is SD-5's sentence with SD-7's phrase, 381 characters, and it is the sentence in SD-7's passages and successor. `REMEDY_PROVIDER_NOT_SELECTED` is the widened 254-character string from both model copies. Rows 56 and 57 select the least digest then the first class, and the first request class, respectively. Row 57 is the M3-D r5 X-D4-J1-1 row. The deficiency bridge, the 16 terminating registry keys, and `bounded_subject` follow NES and D9. `native.release-capability-undeclared` stays out: the registry marks it `notATermination`.

Production text of `outcomes.rs`, `lib.rs`, and `invocation.rs` names none of X11a's forbidden symbols. The only `Command::` uses are the request enum. There is no filesystem, process, environment, clock, crash-barrier, or unsafe use in the new modules. `apps/cli` is untouched.

## Lead rulings

Items 1 to 4 are left undecided, and J2a decides none of them. I found no further unsettled item.

1. **SD-5b.** Accepted. `Observation` has no variant for `MemoryBudgetBelowCeiling`, `ToolOutputBound`, `ToolScratchBound`, or `confinement-refused`. No placeholder row.
2. **SYN-1.** Accepted. No syntax row is added. `NativeContextRefused` and `HostInvariant` already express the routes J1 r6 will record.
3. **E-3.** Accepted. `EphemeralVerdict` carries no detail and no runId. J2a does not emit the conflicting form, and this unit does not change §7.4.
4. **Derivation.** Accepted. J2a projects an `AnalysisOutcome` it is given. It does not derive deficiencies from a Run or compose the analysis termination. That stays with J3d and J2c.

## Judgment calls

1. **Yes. Reserving the path meets "the name is J2a's."** Both modules stay crate-private, as `configuration` and `fact_admission` do. The entry does I/O, so `opensip_host::invocation::run` and `pub` land with J3d and J2c. A public stub `run` would be an entry with no pipeline and would put an analysis word in reach of the binary.

2. **Accepted.** `invocation.rs` is the planned row, and its description still says it executes the bounded step DAG and applies dependency, retry, and cancellation rules. `outcomes.rs` keeps the metadata ingress and takes the matrix and the aggregate; its planned text still says it maps typed host boundary observations and aggregates step outcomes under their existing owners. The opening derivation clause remains the file's planned job for the later units that will edit this same file. The three production rows are byte-identical between v136 and v137. The tests are sibling `_tests.rs` modules, which is why there is an inventory successor and no description successor.

3. **Accepted.** The join chain is consumed tokens. There is no runtime join-order fault, so there is no route for one.

4. **Yes. That is the right line.** Item 10 has no remedy column. The two remedies a bound successor assigns to this projection are the ones J2a selects: SD-5's excluded-form remedy as SD-7 conforms it, and `PROVIDER.NOT_SELECTED` as SD-7 widens it, on row 57 and on the mode-not-selected cell. Every other remedy, and the `errors` composition, belong to the envelope in J3d and J2c. `envelope_detail` is available for that composition and is not applied here except where the termination itself carries the detail.

5. **Accepted.** Rows 53 and 54 carry `NativePrepareBoundExceeded` and `NativeAmbientCargoConfig` and also keep the operational key. Row 30 carries no detail. That matches the carrier column and M3-D item 22.

6. **Yes. A typed origin is acceptable in place of the runtime refusal.** The three malformed-request keys and the mode-not-selected key take any `SpecOrigin`. The five release-declaration keys and the seven coverage-cause keys take none, because each has exactly one possible origin. An origin the registry makes impossible cannot be constructed, so NEM's `native.public-route-origin-not-possible` has no host counterpart. Mode-not-selected is origin-independent and is the `REQUEST.UNSATISFIABLE` / `PROVIDER.NOT_SELECTED` route, distinct from a release declaration's `REQUEST.PRECONDITION_FAILED`.

7. **Accepted.** `InvocationModeV1` and `RequestFlags` carry `default` and `analyze`'s five M3-B item 23 flags plus `--ephemeral` as the request itself. `--yes-policy` is absent from both commands and from the M3 request type.

8. **Accepted**, including the smaller readings as written. Row 34 carries no runId. Rows 38 and 39 put the ExecutionId in `subject` and in `executionId`; row 38 has no detail; row 39 also discloses the namespace beside the subject. Row 40 puts the namespace in the busy-row subject and in the beside field. D item 22's host-bug, session-spec, I/O, and abandoned cases are representable on rows 2, 23, and 49. Rule 4 is applied as written; the source's own labelling cannot emit a committed unlatched run at a phase other than D. The two D9 goldens that list an executionId are compared on class and codes. `ManifestDigest` is 64 lowercase hex, so the 84-character subject bound holds, and duplicate refusals are recorded once.

## Inventory v137

v136 plus two proposed, non-generated test rows in `opensip-host`: `invocation_tests.rs` and `outcomes_tests.rs`. 973 files. The 971 inherited rows are equal by value. Packages, edges, and pending decisions match v136. The standing text is the additive host invocation-model sentence. The two new descriptions match the 22 and 15 tests.

The successor projects 103 rows. Fifteen selectors stay put, one moves by one, and eighty-seven move by two. `inheritedRowsEqualByValue` and `packageDependencyGraphUnchanged` are true. `plannedRowsChanged` is the three production files. No supersession is folded. A scratch rerun of `build_v137.py` against the product lock at `d2c00a9` reproduced the candidate and the successor byte for byte.

Assessment: **ACCEPT**.

## Evidence this review ran

Private `CARGO_TARGET_DIR` under this review directory, private 0700 `TMPDIR`, `CARGO_HOME=/Users/sb/.cargo`, `--locked --offline`, `nice -n 10`. Each cargo command took the shared lane lock and released it. `~/Library/Application Support/OpenSIP` was absent before and after. The staged lock was copied aside before the drift swap and restored to `fe776b81…`.

| Check | Result |
|---|---|
| `cargo fmt --all --check` and `rustfmt --edition 2024 --check` on the two `_tests.rs` | exit 0 |
| `cargo build --workspace --all-targets` | exit 0 |
| Clippy `-D warnings`, workspace, crash-matrix, scenario-fixtures | exit 0, 0, 0 |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1775 passed, 0 failed, 3 ignored, 20 binaries |
| The same, run 2 | 1775 passed, 0 failed, 3 ignored, 20 binaries |
| `cargo test --workspace --doc` | 20 passed, 0 failed |
| Crash-matrix feature lane, platform, security, storage, host | 1673 passed, 0 failed, 3 ignored, 10 binaries |
| `cargo test -p opensip-host --lib -- outcomes:: invocation::` | 37 passed, 0 failed, 148 filtered out |
| `generate_contracts.py` on the staged lock | exit 1, `missing or escaping regular file: SCRATCH-J2A/review.json` |
| `generate_contracts.py` on HEAD's lock | passed, 40 sources, 8 outputs, `changed: []`; staged lock restored |
| `verify_scratch.py` staged | passed. Inventory successors 96 → 97, v137 selected; contract successors 97; inheritance 100 → 103; 21 inventory supersessions and 1 contract passage supersession; 40 generation sources; 48 admission sources, 15 aliases |
| Plain `verify_design` on the staged lock | refuses at `SCRATCH-J2A/review.json` |
| Plain `verify_design` on HEAD's lock | exit 0 |
| `verify_projection.py` against the lock at `d2c00a9` | PASS, 103 rows, 518 corruptions refused |
| `build_v137.py` rerun | same bytes for the candidate and the successor |
| `check_package_edges.py` host lane, v137 and v136 | both passed: 12 workspace packages, 22 declared, 20 resolved |
| `check_package_edges.py` rust-provider lane, v137 | passed: `opensip-rust-provider` only |
| `test_package_edges.py` | 14 tests, OK |
| `check_dependencies.py` `security-crypto-workspace` | passed: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | passed: 8 dependencies, 305 sources |
| `test_dependency_policy.py` | 9 tests, OK |
| `test_identity_dependencies.py` | 5 tests, OK |
