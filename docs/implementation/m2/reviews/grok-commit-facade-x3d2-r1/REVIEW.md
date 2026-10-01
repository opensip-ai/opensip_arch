# X3d-2 r1 — storage commit facade

**Verdict: ACCEPT-UNIT.** Inventory v122 is **ACCEPT** on v119. Required findings: none.

Call 1 is accepted. Integrating X3d-2 before X8b and X9-1 leaves every X3d r6 requirement of this unit met. End-to-end composition of `prepare_commit` and `publish` with a real `CommitSession` is first exercised by X8c B0–B4. A record-only X3d r7 note follows and changes no X3d decision.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x3d2`, detached at `7be09a7040db59af530736418d7d1786030040c5`. The lock selects v119 with D1 bound. `product.diff` is 117719 bytes, sha256 `3afc55c34cca13b1b296325e07aa898ebb6b8f4955b548961746a859f7035002` (35 files, 2573 insertions, 16 deletions; the twenty-two new files are intent-to-add).

Subject manifest `commit-facade-x3d2-inventory-v122-subject.json`: 2128 bytes, sha256 `207ece22b1ac09b34dacfdc6e84c7dce3173ea5f461f38dbf0338bdd8245af7c`.

`~/Library/Application Support/OpenSIP` is absent.

## Call 1 — built before X8b and X9-1

Accepted. The ordering leaves no law requirement of this unit unmet.

X8 r3's owner rows for X3d-2 are the compile-fail rows A–D and G for `PreparedCommit` and `PublishedCommit`, group H (the facade takes no adapter and no `SealOutcome`), and item 3b's adapter source pin. Those rows are in this diff. The host driver passed with the census directory at 95 cases and 8 self-tests, of which 19 cases are this unit. They do not need X8b.

X8 r3 item 4g, and the unit table's sentence that X8b lands before X3d-2, describe storage tests that obtain a `ProjectOperation` through scenario-fixtures. This unit's storage tests do not take a `ProjectOperation`. They run the storage functions `prepare_commit` and `publish` compose, on a scratch private `I/stores/S`, with a real replay and no session. The unit adds no production seam that supplies a `ProjectOperation`. X3d r6 item 12 already allows tests to build a `ReplayedRun` through crate-private `cfg(test)` fixtures while X2e and X5 are pending.

X8c owns B0–B8 and depends on X8b and on X3d-2. B0–B4 are the first process that calls both halves together. Where the behavioral table names X3d-2 as the owner of a refusal, that names who produces the row. The test unit that composes the session with this facade is X8c.

X9 r1 item 5 gives this unit the point `x3d.publish.published`. Units built after X9-0 place their own points. X9-1 precedes this unit's composition tests (gap G1). Those tests are X8c and X9-2 (`crates/storage/tests/commit_tests.rs`). Placing the one point in `publish`'s `Committed` arm does not require X9-1's support surface.

What remains owed, and is outside this unit: X8c B0–B8 with a real `CommitSession`, and X9-2's matrix. Call 3's note on B0 stands for X8c. `crates/evaluator/tests/fixtures` holds no Run, and a scenario project's `ProjectId` is a fresh draw, so a pre-built corpus Run cannot bind. X8c needs a Run whose `projectId` is its scenario project's. `plan` here already requires `descriptor.projectId` to equal the session project and `evaluator_closure()` to equal the selected core closure.

## Law of the unit

X3d r6 items 1, 3, 4, 6, 8 and 9, and item 13's X3d-2 list, are met.

`prepare_commit` (`commit.rs`) takes `(ReplayedRun, CommitSession)` and returns `Result<PreparedCommit, (NotPrepared, StoppedSession)>`.

0. `session.reserve_end_path()` is first. A refusal is `NotPrepared::Refused` with a `StoppedSession` that holds no reserve.
1. One charge runs `plan`. The Run's `projectId` must equal the session project (`CommitSession::project_id`, the ACTIVE row). The evaluator closure must equal `core_closure()`. Every retained frame's `h_digest(identity)` must equal `raw_sha256(frame)`. The commit inventory is canonical `{schemaVersion: 2, runId, objects, blobDigests}`. Frames are declared under their H digest and blobs under their raw digest, each digest once (`BTreeSet`). A plan failure is the invariant row through `session.refused()`. The embedded registry is resolved inside this charge (`schema_sources::registry()`); a missing registry is `PlanRefusal::Material` and the same invariant row, before any store lock.
3. `session.capacity()` follows the completed plan scope. It calls `seal_fits` and does not latch. An exhausted generation is `NotPrepared::CarrierCapacityExhausted` with the attempt ledger still open and the end-path reserve still held (`commit_session.rs` `capacity`).
4. `session.store_root()` then `ProjectStoreLocation::selected`. One charge admits `projects/N`, `objects/sha256` and the ledger. A name that `ProjectStoreNames::new` refuses is the invariant row through `refused()`.
5. One charge takes `effect(0, reserve)` and `prepaid(reserve)` for exactly `attempt_and_objects_cost` (`OPEN_COST + ATTEMPT_COST + publication_cost`). Inside it, `admit_attempt` then `publish_objects`. `ReusedExecution` is `NotPrepared::ExistingAttempt` through `refused()`, so the gate latches. `AttemptUndetermined` is `NotPrepared::CommitUndetermined` through `undetermined()`, which forfeits the reserve. Any other failure is its X3c item 10 row through `refused()`.

`PreparedCommit::publish` consumes the value:

1. `begin_journal_txn`. A refusal is `CommitOutcome::Refused(termination())`.
2. `txn.charge(begin_prepared_ledger)`. On failure, `txn.abort()` and the ledger row.
3. `seal_under_append_lock` with the private `Stager`. Staging runs after the durable `SEAL`. A binding whose RunId, carrier digest or operationRef differs from the commit's is `StagingMismatch` before `next_commit_sequence`, so a non-joining binding allocates no counter. The counter, the receipt, the thirteen-field association, the initial availability and the empty pin set are staged through X3c-2, all or none. `StagedCommit::commit` calls only `PreparedLedgerCommit::commit` and maps `Committed` / `Undetermined` to `EvidenceCommit`.
4. `SealOutcome::Committed` builds `PublishedCommit`, then `crash_barrier!("x3d.publish", "published", step)`, then `CommitOutcome::Committed`. `CommitUndetermined` passes through. `Refused(Session)` is `termination()`. `Refused(Staging)` is the ledger row.

`PublishedCommit` is constructed in that one arm. Getters only. `Debug` is non-exhaustive and omits the receipt bytes. Neither `PreparedCommit` nor `PublishedCommit` is `Clone`, `Default` or serializable, and neither has a private inherent function, so no group F case is owed. Storage holds no settlement reserve and accepts no external adapter or `SealOutcome`.

The point name and place match X9 r1 item 5. The barrier is the `($scope, $step, step)` arm. With `crash-matrix` it calls `crash_barrier::point`; without the feature that arm is a no-op. `the_published_point_follows_the_published_commit_once` pins the single placement after the single construction. `seal_under_append_lock` returns before the barrier, so level 4 is already released.

## Calls 2–13

2. **Accepted.** `store_root` is one charge through the free function `operation_handoff::open_store_root`. `ProjectOperation` gains no inherent function. The open is no-follow from the retained I: `stores`, then S, each present, private, exactly named, on I's device. `S/store-instance.v1` must have the device and inode of the endpoint's retained marker sample, and the absolute spelling from H as walked must name the same directory. Missing or changed is custody `required-files-changed`. Other directory refusals keep X2's registration rows. I/O is host-io. A missing marker sample among required files is `InstallationTermination::Invariant`. `StoreRoot` is exported, lends the directory, the spelling and the uid, and grants nothing. It is not a row-D type and has no X8 rows. The security test replaces S with a copied marker and observes `Custody { subject: "required-files-changed" }` with the attempt ledger closed.

3. **Accepted.** Target identity is the ACTIVE row's `ProjectId`. The closure must equal the selected core closure. Binding only the closure is rejected by `plan`: another project is `PlanRefusal::Project`. The B0 corpus constraint is a finding for X8c, recorded under call 1.

4. **Accepted.** The publication reserve is taken after `capacity` and after layout, inside the same charge as attempt admission and object publication. Layout is charged by X3c-1 as those `admit_*` calls run. `effect` and `prepaid` do not outlive the charge, and `capacity` consumes the session, so no single charge can span steps 2 through 6. The only reservation that outlives a call is the settlement reserve from step 0. The reserve equals `attempt_and_objects_cost`. Admission and the objects draw only from it. A shortfall is the budget row before the attempt row and any object (`the_publication_reserve_is_exactly_what_admission_and_the_objects_charge`). When both capacity and budget would fail, capacity is reported, and that path writes no attempt and no object. `publish`'s `BEGIN` and staging reserves stay inside X3c-2's own charges. The SEAL path stays X3d-1's charge.

5. **Accepted.** identity-and-evidence's retention table keeps one CAS keyed by raw SHA-256. The object under an h-identity digest is the exact H preimage frame. The commit inventory is `{schemaVersion: 2, runId, objects, blobDigests}`, the exact set of typed object identities and retained raw blob digests. The staging join compares the published set with `blobDigests` plus the H digests of `objects`. `stage_run_material` returns both. A blob whose raw digest equals a frame is one object. `sealedAssurance` is `replayable`, which is the default authoritative profile and retains the closure.

6. **Accepted.** `signerKeyId` is `local-custody-unsigned`. The receipt schema allows any string of length 1..=4096. identity-and-evidence excludes receipt signing from semantic IDs and leaves authenticated receipt signing as an implementation-qualification obligation (the reference-lifecycle paragraph). A real signer is a successor's. `commitSequence` is per `(storeGenerationDigest, N)`, allocated inside the open evidence `BEGIN IMMEDIATE` by `WriteTransaction::next_commit_sequence`: `ORDER BY length(commit_sequence) DESC, commit_sequence DESC LIMIT 1`, `DecimalCounter::parse_text`, then `checked_add(1)`. None yields 1. A full u64 is `LedgerError::Configuration("commit_sequence_exhausted")`, which classifies as `StagingMismatch` and the invariant row. The association copies `sequence.to_string()`. The test pins 1, then 2/9/10/100 yielding 101, and the exhausted counter.

7. **Accepted.** `storeGenerationDigest` is raw SHA-256 over the canonical five-member `{schemaVersion: 1, namespaceId, storeInstanceId, storeGeneration, stateSchema}`, with sorted keys and no domain framing (store-instance-lineage v1 `canonicalDigestRecipe`). `the_store_generation_digest_is_the_lineage_recipe` pins that canonical string.

8. **Accepted, with the disclosed limit.** Initial availability is generation 0, `retained`, `missingRefs: []`, `reason: "observed"`. The pin set is empty. `StagingLimits` is `per_record_work: 4 << 20`, `pin_rows: 0`, `pin_text_bytes: 0`. No law names a pin a fresh commit must hold. X3c-2 stages that initial availability unconditionally, so a second commit of the same Run in the same `(S, N)` is refused at staging on the invariant row. identity-and-evidence allows a duplicate retry to share a Run with a separate attempt receipt. The fix belongs to an X3c successor that stages availability only when none exists. M2 never commits one Run twice. This is a disclosed limit, not a finding.

9. **Accepted.** `prepare_commit` takes no registry. Group H pins arity 2. Storage embeds the registry's pinned sources in `source_requirements` order and resolves them once per process. `the_embedded_sources_are_the_pinned_registry` compares each source to its pin and requires `registry()` to be `Some`. `from_sources` refuses any other bytes by those pins.

10. **Accepted.** `CommitOutcome` is `Committed`, `CommitUndetermined`, `Refused`. `NotPrepared` is `CarrierCapacityExhausted`, `ExistingAttempt`, `CommitUndetermined`, `Refused`. `ExistingAttempt` stays its own variant and uses `refused()`, so `finish` appends the `REV`. The facade does not map it to `T::Invariant`. X7 maps that variant to the invariant row until X6 exists.

11. **Accepted.** A SEAL binding that does not join, a receipt or association its own parser refuses, and a missing registry all terminate as `InstallationTermination::Invariant`. The first two are `StagingMismatch` on the staging path. The missing registry is `PlanRefusal::Material` inside `plan`, before staging. `ledger_row` maps `ProjectLedgerRow::Invariant` to `T::Invariant`.

12. **Accepted.** The pin confines `CommitAdapter`, `StagedCommit`, `begin_journal_txn` and `seal_under_append_lock` to `custody/commit_session.rs`, security `lib.rs`, and storage `commit.rs`. Production `.rs` under `crates/*/src` excludes `*_tests.rs` and `tests.rs`. Comments are stripped before the token scan. The self-check refuses a use outside those files. Both host tests passed. Group H uses the existing category `ForgedReceipt`, so the census enum is unchanged. The two H fixtures fail E0061 with the annotated arity text.

13. **Accepted.** See the point placement under the law section. The barrier follows the construction of `PublishedCommit` and follows the return of `seal_under_append_lock`.

## Inventory v122

Parent v119: 469771 bytes, sha256 `34443e615d5c30f64e7f93c56d3b6e60b6afa06712d3489c127ecc858e4e21c6`. Candidate v122: 485705 bytes, sha256 `69cf90db0ade09fc0f9536b3ef293d7de6aff68c7d3ae9a2aabfab4f6c244c7a`. Successor record: 143194 bytes, sha256 `25c054b45d6d8aa966df6b90451f585f8587adf83a75b146b32c3268de75a15a`. The parent pin inside the successor record is that v119 pin.

918 files = 897 inherited rows equal by value, plus 21 additions (`commit_tests.rs`, `schema_sources.rs`, and the 19 `storage_*.rs` cases). `commit.rs` stays the planned v119 row, kept by value. Packages and `pendingDecisions` are unchanged. The storage → evaluator edge was already declared; this unit adds it to `Cargo.toml` and `Cargo.lock`.

`descriptionOverrideProjection` has 55 rows: the 16 bound to v119, plus D1's 39 overrides, with D1's after text as the effective description. `verify_scratch.py` against the worktree lock passed: 82 inventory successors, 73 contract successors, 55 inheritance rows, v122 selected, nothing written. `verify_projection.py` against `design-lock.json` at this head passed: 55 rows, 278 corruptions refused, read-only. `build_v122.py` was not run.

Descriptions the README marks out of date (admission_tests, project_ledger, project_commit, recovery_material, and the session, handoff and session-test rows that omit the new hooks) stay equal by value. They belong to a later description batch. They are not v122 findings.

## Replay

Private `TMPDIR` `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/grok-x3d2-tmp`, mode 0700. `CARGO_TARGET_DIR` under this review directory. Toolchain cargo 1.95, `--locked --offline`.

- `opensip-storage` lib, filter `commit::tests` and `the_embedded_sources`: 27 passed, 0 failed, 114 filtered, 6.38s. That is the 11 `commit::tests` plus the schema-source test, and 15 `project_ledger::commit::tests` that the substring filter also selected. All 11 named commit tests passed, including the digest recipe, the counter, the one-byte-short reserve, the non-joining binding, and the published-point pin.
- `opensip-security` lib, `the_store_root_is_the_endpoints_store`: 1 passed, 0 failed, 0.82s.
- `opensip-host` `admission_tests`, the adapter pin, its self-check, and `opaque_api_misuse_fails_for_the_intended_reason`: 3 passed, 0 failed, 19.88s. The case directory is 95 files and the self-test directory is 8; the driver checks that census against the listings and requires each case to fail for its annotated reason.

The lead's two workspace runs (1575 passed, 0 failed, 3 ignored), clippy, fmt, and `check_package_edges` were not replayed here.

The cargo target and the private temp directory are removed. The output directory holds `product.diff`, `REVIEW.md` and `review.json`.
