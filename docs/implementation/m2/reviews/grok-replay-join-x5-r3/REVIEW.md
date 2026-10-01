# X5 r3 — replay-to-commit join

**Verdict: ACCEPT.** Required findings: none.

r3 closes the contradiction in accepted r2. `replay_run` reports a lost retained object or blob nested under `Structure`, and r2's table sent every `Structure` to `EVALUATION.INPUT_REFUSED`. The new evaluator accessor classifies that tree first, the host applies `evidence.missing` before the variant table, and `replay_run` stays as it is. Items 5b to 5f, the withdrawn budget example, the single X5a unit, and the B0 note agree with the fault contract, the identity carriers, S12, and X8 r3. `PROPOSAL-r2.md` is byte-equal to the accepted r2 subject.

## Subject

`docs/implementation/m2/replay-join-x5/PROPOSAL.md` (r3): 22501 bytes, sha256 `d9a101b83f083bed6e6b97f3b3d64344f07bb206e8ab14af75dac4aebc4d9b82`. Both rows in the review `hashes.txt` match.

`PROPOSAL-r2.md`: 9800 bytes, sha256 `d2a1f585517b19a6c07b5a6267875dd2d728c05ffa1a7c49bd62cf4a33454365`. That is the subject accepted in `reviews/grok-x5r2-x6r2-x2r6/x5/review.json`.

Product evidence is the clean worktree `/Users/sb/code/opensip-ai/opensip-x5a`, detached at `adc9081a0408f9cdac50b87c791f36d30f29e965`. Live `/Users/sb/code/opensip-ai/opensip` is `96dd1145b3da207e83479dc0f50d9d62cb1b7e04`. The law names `adc9081`, so the worktree is the product. No product cargo. The lead probe was not replayed; the walk-before-read order is in `replay.rs`.

`~/Library/Application Support/OpenSIP` is absent.

The r2-to-r3 diff leaves items 1, 3, and 6 unchanged. Item 4 keeps the budget decision and points the values and the bounds test at item 5e. Item 2 adds `ReplayRefusal`. Items 5, 5a to 5f, 7, 8, and 9, four forbidden substitutes, and the B0 sentence in Not claimed are the amendment.

## The contradiction, and the two-step map

The contradiction is real. At `adc9081`, `replay_run` (`crates/evaluator/src/replay.rs`) calls `with_read_capture` and then `inspect_retained_walk`, mapped with `ReplayError::Structure`, before any later `retained.object` that would become a top-level `ReplayError::Input`. `inspect_retained_walk` reads the Run through `inputs.object`, and `From<GraphError>` wraps that as `RetainedWalkError::Graph`. A missing Run is `Structure(Graph(Input(MissingObject)))`. Identity's `blob` returns `MissingBlob` when the map lacks the digest. Native retention wraps the same input error as `Retention(Owner(Frame(Input(Missing…))))` (`NativeRetentionError::Owner`, `NativeUniverseError::Frame`, `GraphError::Input`).

r2 item 5 sends only a top-level `Input(MissingObject)` or `Input(MissingBlob)` to `evidence.missing`, and all of `Structure` to `EVALUATION.INPUT_REFUSED`. r2 item 8 and RF-1 require a missing retained object or blob to be `HOST.IO_FAILURE` / `host-io` / `evidence.missing`. Read literally, r2 routes the corpus's missing-blob case, and every walk-reached removal, to `EVALUATION.INPUT_REFUSED`. The existing host test detects those cases by searching `Debug` text for `MissingBlob(` and `MissingObject(` (`native_owner_tests.rs`).

r3 resolves it without changing `replay_run`. Step 1 applies `unavailable_evidence()` wherever the missing leaf sits, including under `Structure` and `Evaluation`. Step 2 is an exhaustive match on the variants that remain. Returned values, order, and the evaluator's existing replay test stay.

## The accessor

The accessor is sound, and the three rejected alternatives are rightly rejected.

`UnavailableEvidence` is an inert exported enum, `Object(String)` and `Blob([u8; 32])`, with `reference()` producing the step 1 subject (the object key, or the blob digest as 64 lowercase hex). It lives in a new pure evaluator module. `Some` is exactly `RetainedInputError::MissingObject` and `MissingBlob`. Those two variants are the only missing-byte leaves in identity's `Error`. Every other leaf is `None`.

The named nesting is present and closed. Evaluator and identity error enums in this tree carry no `#[non_exhaustive]`. `EvaluationError::Reconstruction` can hold `ReconstructionError::Structure(RetainedWalkError)` or `Record(GraphError)`, so the required `Evaluation(Reconstruction(..))` case is a real path. Text-only payloads (`RetainedWalkError::Refused(&'static str)`, `ExecutionRefused(V)`, `ReconstructionError::Refused(String)`, `NativeRetentionError::Refused(Vec<String>)`) are `None` without inspection. The fault contract says the adapter does not parse exception text to establish origin. A source pin that refuses a `_ =>` arm keeps a new variant from compiling unclassified.

Host-side descent would make the host own the evaluator and identity error tree. `Debug` search is what the existing test does, and the contract forbids it for the adapter; the test stays a test. Hoisting inside `replay_run` needs the same descent and changes values and order the current replay test pins.

Two `Ok(None)` arms in `native_universe.rs` (`nested_record`, `nested_frame`) turn a `MissingBlob` into absence for an optional nested lookup. Those arms never produce a `ReplayError`, so the accessor does not see them. r3 leaves `replay_run` unchanged. The lead's walk-reached removals still surfaced as typed `Missing`. Item 8 is the check that a removed member of the claimed closure is `evidence.missing`.

## Items 5b to 5f

**5b.** `EVALUATION.INPUT_REFUSED` has three routes in `x-opensip-routes`. `external-specification` and `release-declaration` are request-rejected, `REQUEST.PRECONDITION_FAILED`. `provider-return` is operational-failed, `PROVIDER.PROTOCOL_VIOLATION`, `provider-protocol`, with the remedy "Correct the provider output and rerun the stage; retain its admission diagnostic." The identity and join twins use that same remedy. The candidate is retained producer data. The contract says re-admitting retained producer data preserves the producer-contract meaning of a structural violation, including re-derivation over retained producer inputs. `provider-return` is the route that sentence names. The rejected `external-specification` remedy asks for a caller-supplied specification. `host-internal` is a different detail, `HOST.INVARIANT_VIOLATED`, and r3 does not use it for this row.

The generated host enums already contain `ProviderProtocolViolation`, `HostIoFailure`, `EvaluationInputRefused`, `EvidenceMissing`, and `EvidenceRegenerationMismatch`. No new public code.

**5c.** `RegenerationMismatch` carries `run_id`, and its carrier subject is that id. The contract says both replay-mismatch origins require the affected Run reference. The public subject is the claimed RunId. The evaluator's `Mismatch` key is a static label such as `EVALUATOR_COMPLETE_PROOF_REPLAY`, and `target` is often `None`; both stay in the retained diagnostic. The route is `complete-replay-mismatch:retained-regeneration` (operational-failed, exit 4, `HOST.IO_FAILURE`, `host-io`, `evidence.regeneration-mismatch`). The schema's `host-internal` twin is the live first-party defect, which this retained candidate is not.

**5d.** `InstallationTerminationV1` has `class`, `exit`, `error_code`, `fault_cause`, `detail`, and `subject`, and no remedy field. `configuration.rs` holds `REMEDY_CONFIG_INVALID` beside `policy_selection_termination`, which constructs the struct directly and matches exhaustively. `replay_termination` and `replay_remedy` follow that shape. The three remedy strings are the schema strings, and the first two are the identity carriers' verbatim text. The signature keeps `limits`. The production-caller pin is vacuous until X7a adds the one caller (X7 r3 item 1 calls `replay_candidate`; item 11 depends on X5a). Dropping the parameter would add a second entry point the law does not name.

**5e.** The constants are the values already used by `native_owner_tests.rs` `independent_run_replay_matches_selected_reference_and_owns_its_closure` and by `commit_tests.rs`: walk and owner budgets 20_000_000 steps, depth 96, 20_000_000 descriptor work; 100_000 owner invocations; 100_000 capture entries; `32 * 1024 * 1024` retained bytes. No design source fixes different numbers. A corpus of 20_000_000 steps is not buildable, so the bounds test measures exact need per dimension, requires the need to be at most the constant, and refuses one below that need on the structural row. Capture is also pinned at the constant: 100_000 entries replay, and one more is `Capture(Limit)`, which step 2 already sends to the structural row.

**5f.** X8 r3's units list assigns X5a the `ReplayedRun` reuse case in group E. The table's unit cell cites X5 r2 item 3 for "a `ReplayedRun` passed to a second `prepare_commit`", E0382. That fixture is the one r3 names. Group C in the same table is `prepare_commit(&retained_inputs, session)`, E0308, owned by X3d-2. It does not list a `RunCandidate`. X3d r6 item 11 requires `prepare_commit` to reject a `RunCandidate`. r3 item 2 keeps `RunCandidateInputs` crate-private inside the host (item 6). X8's export rule gives a crate-private type one unnameable case, E0603, and calls that the stronger refusal. Filing that case under group C, with census rows for X5a, completes the omitted X3d row under the export rule. Inside the host the type remains constructible and inert, which is item 2's "anyone may construct it" within the crate that owns the join.

## The withdrawn budget example

Withdrawing `EVALUATION.WORK_BUDGET_EXHAUSTED` is right. The workflow-projection appendix lists it as class indeterminate: the sealed Run's termination carries D9 deficiency `budget-exhausted`, and the remedy is to raise `analysis.budget`. The fault contract excludes exhausted logical analysis budgets from the fault-condition enum. The registry still contains the code, owned by workflows, as a sealed-Run deficiency. No evaluator mapping sends `EvaluationError` to it. `EvaluationError::Limit` during replay is the local `REPLAY_LIMITS` bound, which item 4 keeps separate from operational work budgets. It takes the same structural row as `Structure(Limit)` and `Capture(Limit)`. A separate row per `EvaluationError` would borrow a detail whose owner did not fix that use.

## One unit, and the B0 note

One combined X5a is acceptable. The accessor has no caller other than this mapping. `verify_design` admits one successor at a time, so an X5a-0 split would insert a successor whose only purpose is the module reviewed here. X7a depends on X5a. The inventory successor lists the new evaluator and host files together.

The B0 note is right in its decision. The X3d-2 review, call 3, accepts the binding rule and records the corpus constraint for X8c: `crates/evaluator/tests/fixtures` holds no Run, a scenario `ProjectId` is a fresh draw, and a pre-built corpus Run cannot bind. Call 1 states that X8c needs a Run whose `projectId` is its scenario project's. The review does not name an X5 producer. The quoted phrase "through X5a's producer" is the lead's gloss of that constraint. The decision matches the review and X5's Not claimed list: analysis producers are M3, X5 has no producer, and X8c builds the synthetic labelled Run bound to the scenario project. X5a supplies the join that replays it. Item 8 moves the end-to-end receipt from "X3d-2's tests once X2e exists" to X8c's B0 and X9's matrix, which is the same boundary the X3d-2 review drew.

X12 r3 item 9 leaves `check_plan_pack` unwired in `replay_run` and in `replay_candidate`. Item 8's source pin requires `fact_admission.rs` to call `replay_run` once and no other evaluator function. That keeps the synthetic corpus replaying until the M3 Plan builder.

## Registry, S12, and diagnostic routes

`public-detail-registry.v1.json` already registers `evidence.missing` and `evidence.regeneration-mismatch` (identity), `EVALUATION.INPUT_REFUSED` (identity, fault contract), `EVALUATION.WORK_BUDGET_EXHAUSTED` (workflows), `HOST.IO_FAILURE` (security), and the fault-contract selectors. `PROVIDER.PROTOCOL_VIOLATION` is a generated D9 error code and the fault schema's provider-return code. It is not an installation row in `diagnostic-routes.json`.

S12 (`security-and-lifecycle.md`) maps I/O failure to operational-failed, exit 4, `HOST.IO_FAILURE`. The 468a and owner-selection `diagnostic-routes.json` rows for filesystem, doctor, and recovery I/O use that same class, code, `host-io`, and exit 4, with domain detail omitted on those installation boundaries. Identity's `EvidenceUnavailable` and `RegenerationMismatch`, and the two fault-schema routes, fix the domain details `evidence.missing` and `evidence.regeneration-mismatch` on that same class, code, fault, and exit. Item 5's precedence sentence takes that class and exit. The installation rows stay detail-omitted for their own boundaries. Security's `InstallationTermination` gains no row; the projection is the host `InstallationTerminationV1`, as X12b already does for an evaluator refusal.

## Item 8 wording

"Claimed closure" is the set the walk reads. `ReplayedRun::retained_evidence` documents that ambient unread inputs are excluded. The proposal's opening paragraph separates those ambient removals, which replay or fail as the forged cases' mismatch. The fixture case arrays also hold members the walk does not read, and the existing host test inserts an extra invalid ambient object and a zero digest. Item 8's removal test is the walk-reached set of one corpus case, each removed reference named by `reference()`. The corpus has 101 cases. Object map keys are the pool record's `id`. Blob subjects are 64 lowercase hex of the raw digest.

## Calls

1. The contradiction is real, and the two-step map resolves it with `replay_run` unchanged. **Accept.**
2. The accessor is exhaustive, has no wildcard and no text inspection, and is owned by the evaluator. The three rejected alternatives are rightly rejected. **Accept.**
3. Items 5b to 5f match the fault contract, the identity carriers, S12, and X8 r3. **Accept.**
4. Withdrawing `EVALUATION.WORK_BUDGET_EXHAUSTED` as a replay termination is right. **Accept.**
5. One combined X5a with one inventory successor is acceptable. **Accept.**
6. The B0 note assigns the synthetic Run to X8c and leaves X5 with no producer. **Accept.**
7. `PROPOSAL-r2.md` is byte-equal to the accepted r2. **Accept.**
8. Nothing else in the amendment is wrong. **Accept.**
