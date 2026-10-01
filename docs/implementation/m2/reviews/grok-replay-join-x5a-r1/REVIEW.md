# X5a r1 — replay join

ACCEPT-UNIT. Calls 1 to 9 are accepted. Inventory v123 is accepted on v122 with D2 folded.

Product worktree `/Users/sb/code/opensip-ai/opensip-x5a`, detached at `933e78be8cd8ebbf1b622b39a84b0b3dd1396117`. `product.diff` is 63492 bytes, sha256 `5a36fbb1c41466ec34c1f41f7df421ea618cf0ba318f822b66a951c99082cd98`: 9 files, 1598 insertions, 2 deletions. The five new files are intent-to-add. `~/Library/Application Support/OpenSIP` is absent. `build_v123.py` was not run.

The live `replay-join-x5/PROPOSAL.md` is the accepted r3 plus the stamp ` r3 ACCEPTED by Grok on 2026-10-03.` Removing that stamp restores 22501 bytes, sha256 `d9a101b83f083bed6e6b97f3b3d64344f07bb206e8ab14af75dac4aebc4d9b82`.

## The join

`replay_candidate` builds `RetainedInputs` and calls `replay_run` once (`fact_admission.rs` 93–101). `replay.rs` is outside the diff. `RunCandidateInputs`, `ReplayRefusal`, `REPLAY_LIMITS`, `replay_termination` and `replay_remedy` are `pub(crate)`. `ReplayRefusal` derives `Debug`, `PartialEq` and `Eq`, keeps both fields private, and exposes them through getters. The module is private under `#[allow(dead_code)]` (`lib.rs` 22–23), the same shape as `configuration`. Security’s `InstallationTermination` is untouched.

`route` asks `unavailable_evidence()` first (117–122). A `Some` is `EvidenceMissing` with `reference()`. The exhaustive match then sends `Structure`, `Capture`, `Law`, `Input` and `Evaluation` to `InputRefused`, and `Mismatch` to `RegenerationMismatch` with the claimed RunId (123–131). `Evaluation(Limit)` takes that structural row.

`replay_termination` builds `InstallationTerminationV1` with class operational-failed and exit 4:

- `evidence.missing`: `HOST.IO_FAILURE`, `host-io`, subject the reference;
- `EVALUATION.INPUT_REFUSED`: `PROVIDER.PROTOCOL_VIOLATION`, `provider-protocol`, subject absent;
- `evidence.regeneration-mismatch`: `HOST.IO_FAILURE`, `host-io`, subject the claimed RunId.

The three remedy constants are the schema strings. `promised-bytes-lost:evidence-store`, `complete-replay-mismatch:retained-regeneration`, and `input-schema-invalid:provider-return` (with the identity and join twins) in `evaluator-fault-observation.schema.v3.json` carry those remedies, and identity’s `EvidenceUnavailable` and `RegenerationMismatch` carry the first two verbatim, with the same class, code and fault. `row_remedy` maps the three details to those constants (`doctor_ingress.rs` 222–224). No other host arm emits them.

`REPLAY_LIMITS` is walk and owner 20_000_000 steps, depth 96 and 20_000_000 descriptor work; 100_000 owner invocations; 100_000 capture entries; 33_554_432 retained bytes.

## The accessor

`unavailable_evidence` is a private module. `UnavailableEvidence` is re-exported. `reference()` returns the object key, or `digest_hex` of the blob. `Find` is implemented for the twenty-four types in the replay tree, and each match lists every variant. `Some` is returned only for `RetainedInputError::MissingObject` and `MissingBlob`.

The `..` leaves are text, schema, digest, canonical and candidate payloads: `Canonical`, `Candidate`, `ClosureRole`, `Schema`, `Interpretation`, `Frame(DigestError)` on both `GraphError` and `CaptureError`, `Refused`, `ExecutionRefused`, `AtomRefused`, `CompositionRefused`, `SnapshotPath`, `SnapshotSource`, and `Manifest(CapabilityRefusal)`. Those payloads do not hold a `RetainedInputError`. `import_payloads::input` keeps `MissingObject` and `MissingBlob` as `Record(GraphError::Input(_))` and turns only `ClosureRole` into text. `native_universe.rs` still answers `Ok(None)` for an optional nested `MissingBlob`; that arm does not become a `ReplayError`. The removal test uses the full replay’s `retained_evidence()` as the claimed closure, so a walk-reached member is the one that must be `evidence.missing`.

## Calls

1. Accepted. The rows are `InstallationTerminationV1` values in `fact_admission.rs`. The route enum is private to the module. Security gains no row.
2. Accepted. `ReplayRefusal` is not `Clone`. Its members are private. The derived `Debug` is the retained diagnostic. Termination is the public projection.
3. Accepted. The pin walks production `.rs` under `crates/host/src`, skips `*_tests.rs`, `tests.rs` and a `#[cfg(test)]\nmod tests` tail, ignores the definition, and requires the last top-level argument to be `REPLAY_LIMITS`, `fact_admission::REPLAY_LIMITS` or `crate::fact_admission::REPLAY_LIMITS`. It finds no production call and asserts at most one. The self-check refuses `limits`, a struct update, `REPLAY_LIMITS_FOR_TESTS`, `my_REPLAY_LIMITS`, a wrapping call and a missing argument.
4. Accepted. `failure_envelope` looks up a remedy by detail. The three details are new on this path, and each has one route here. A later route that reuses `EVALUATION.INPUT_REFUSED` with another remedy is that owner’s change. `InstallationTerminationV1` gains no remedy field.
5. Accepted. Nine dimensions of `packet-0-original` are bisected over `[0, constant]`. The case replays at the least passing value, and one less is the structural row with `unavailable_evidence()` `None`. Capture entries are asserted equal to the case’s object count plus blob count, and retained bytes equal `retained_evidence().byte_length()`. A separate test pads ambient entries to 100_000, which replays, and 100_001 is `Capture(Limit)` on the structural row.
6. Accepted. A member is in the claimed closure when the full replay’s `retained_evidence()` holds it. Each such removal is `evidence.missing` naming that reference. A member outside the read set still replays.
7. Accepted. All 101 corpus cases run under `REPLAY_LIMITS`. Lawful cases return the claimed RunId. Each `mismatch` case is `Mismatch` on the regeneration row with that RunId. The one `unavailable` case is `evidence.missing`. The altered-descriptor, altered-blob and wrong-domain probes are `EVALUATION.INPUT_REFUSED` with `unavailable_evidence()` `None`.
8. Accepted. Corpus, removal and bounds use `std::thread::scope` over `available_parallelism`. They take no lock and create no file.
9. Accepted. The production half of `unavailable_evidence.rs`, comments removed, contains one `#[derive(`, twenty-four `impl Find for`, and none of `_ =>`, `_ |`, `| _`, `format!`, `{:?}`, `contains(`, `starts_with(` or `Debug)`.

The join pin shows one `replay_run(`, one `use opensip_evaluator::…` line, one `.unavailable_evidence()`, and none of `ReplayedRun {`, `check_plan_pack`, `admit_pack`, `derive_evaluation`, `inspect_`, `Clone`, `Default`, serde, custody, storage, platform, lifecycle, ledger or I/O in the production module.

## X8

Accepted. X8 r3 assigns X5a the `ReplayedRun` reuse case in group E. X5 r3 item 5f adds the group C unnameable case under the export rule for a crate-private type. The census has both, unit `X5a`:

- `host_run_candidate_unnameable.rs`, group C, `StructuralOnly`, E0603, `module `fact_admission` is private`;
- `evaluator_replayed_second_prepare_commit.rs`, group E, `ClonedOrReused`, E0382, `use of moved value: `replayed``.

`RunCandidateInputs` has no inherent function, so no group F row is owed. The driver census is 97 cases and 8 self-tests.

## Inventory

ACCEPT. v123 is 490531 bytes, sha256 `e183e6dafe21b40985f83136b9b5b2fe48e39a9a1cfad207a2d6d616fb5e6171`, parent v122 485705 / `69cf90db0ade09fc0f9536b3ef293d7de6aff68c7d3ae9a2aabfab4f6c244c7a`. Successor record 145321 / `df4970380827347b745b35b941a0263d54beade1481e2edba5cdc2e9306691eb`. Subject 2101 / `0f45c8ce7cdac3e92ab55b065f4fc908e9f99478eb5dfa1325a76883192285c7`.

922 files against v122’s 918. Added `unavailable_evidence.rs` (validator), `fact_admission_tests.rs` (test), and the two refusal cases (fixture). Removed none. `fact_admission.rs` stays the parent’s planned validator row, equal by value. 918 inherited file records are equal by value. `packages`, `pendingDecisions` and `schemaVersion` match. The standing text differs.

Projection: 55 rows. D2’s four supersessions keep the raw v122 description as `before` and as the v123 file description, and the effective description is D2’s `after`. D2’s `before` is the lock inheritance `after`. The candidate selectors of those four paths each move by 4. `verify_projection.py`: `{"readOnly": true, "projectionRows": 55, "positive": "PASS", "corruptionsRefused": 278, "directParentOverrideIncluded": true}`. `verify_scratch.py`: passed, 83 inventory successors, 74 contract successors, 55 inheritance rows, selected inventory v123.

The README’s stale-by-omission descriptions of `fact_admission.rs`, `doctor_ingress.rs` and `admission_tests.rs` stay for the next description successor. Inherited rows are equal by value, so this successor does not edit them.

## Replay

Private `TMPDIR` `$(getconf DARWIN_USER_TEMP_DIR)/grok-x5a-tmp`, mode 0700. `CARGO_TARGET_DIR` under this review directory. Both were removed after the runs.

`cargo test --locked --offline -p opensip-evaluator --lib -- unavailable_evidence`: 4 passed, 0 failed.

`cargo test --locked --offline -p opensip-host --lib -- fact_admission`: 12 passed, 0 failed, 24.09s.

`cargo test --locked --offline -p opensip-host --test admission_tests`: 6 passed, 0 failed, 22.98s, including `opaque_api_misuse_fails_for_the_intended_reason` over the 97-case census and 8 self-tests.

Workspace `cargo test`, clippy, `cargo fmt` and `check_package_edges` were not replayed.
