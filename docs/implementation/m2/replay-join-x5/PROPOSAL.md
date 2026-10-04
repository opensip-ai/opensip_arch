# The replay-to-commit join — proposal X5 r4

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X5 of `EXIT-PLAN.md`, under the build plan's opaque-prerequisite decision (lines 25–70: `RunCandidate`, `ReplayedRun`, `CommitSession`, `PreparedCommit`), its M2 row (line 886: "Evaluator replay; … host fact_admission/finalization") and failure case F01, and under the accepted laws X3d r3 (items 1, 3 step 1 and 10), X3c r7, X4 r7 and X2 r5. Items 1 to 6 contain lead decisions made under the owner's standing direction to proceed on the lead's recommendation; each names the alternative it rejects. r2 answers Grok X5 r1 RF-1: a missing retained object or blob is unavailable evidence, not an input refusal. r1 bytes are preserved in PROPOSAL-r1.md. Not code. Library only: no CLI command is wired.

**r3 (2026-10-01) corrects a contradiction found while X5a was being built.** r2 bytes are preserved in PROPOSAL-r2.md (sha256 `d2a1f585517b19a6c07b5a6267875dd2d728c05ffa1a7c49bd62cf4a33454365`, the subject Grok accepted). r3 ACCEPTED by Grok on 2026-10-03.
- **The contradiction.** r2 item 5 routes `Input(MissingObject)` and `Input(MissingBlob)` to `evidence.missing`, and all of `Structure` to `EVALUATION.INPUT_REFUSED`. But `replay_run` walks the whole retained closure (`inspect_retained_walk`) before any top-level read. So with the real evaluator, a missing object or blob is reported nested under `Structure`, never as a top-level `Input`:
  - the corpus's own `missing-blob-03cc96…` case (`crates/host/tests/fixtures/replay-fixtures.json`, expected `EVIDENCE_UNAVAILABLE`) returns `Structure(Graph(Input(MissingBlob(..))))`;
  - removing each object and blob of three corpus cases in turn, one at a time, gave `Structure(Graph(Input(Missing…)))` or `Structure(Retention(Owner(Frame(Input(Missing…)))))` for every removal the closure walk reached, and never a top-level `Input(Missing…)`. The other removals were ambient members, which replayed or failed only as the forged cases' proof mismatch.

  Read literally, r2's table therefore routes every lost retained byte to `EVALUATION.INPUT_REFUSED`, which r2's own item 8 test and RF-1 forbid.
- **The fix (item 5a, lead decision).** The evaluator classifies its own error tree, with an exhaustive accessor. The host applies `evidence.missing` first, then the variant table.
- **Gaps settled (items 5 and 5b to 5f).** These are the class of `EVALUATION.INPUT_REFUSED`, the `Evaluation(e)` row, the mismatch subject, remedies, the `limits` parameter, the limit values and their test, the compile-fail rows, and X8c's B0 Run.
- **Units (item 9).** X5a becomes one combined unit across evaluator and host.

**r4 (2026-10-04) is J1's successor S8: item 3's order.** r3 bytes are preserved in PROPOSAL-r3.md (sha256 `d9a101b8…`, 22,501 bytes, the subject Grok accepted; `reviews/grok-replay-join-x5-r3`). Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Not accepted.** Not code.
- **Why.** J1 opens the `CommitSession` at the handoff (R12), before the capture session. The attempt's ExecutionId then exists before any provider spawns, and the writer holds the lease through source admission, evaluation and commit (J1r6:508-510; IE:1657-1658). Replay needs the evaluation's candidate, so it now runs after evaluation and before `prepare_commit`. J1 item 7 states the new item 3, and J1 item 13 assigns it to X5 r4 as successor S8 (J1r6:517-519, :885).
- **What r4 changes.** Item 3's order, and each sentence of r3 that states the old order: item 3's rejected alternative, one reason in item 4, item 7's F01 sentence and one forbidden substitute. It adds one forbidden substitute that guards the new order, and a one-line note in item 9 on where the code lands. The table below lists each change.
- **What stays.** Items 1, 2, 5, 5a to 5f, 6 and 8: the API, the refusal rows, the accessor, the remedies, the `limits` parameter, the limit values, the compile-fail rows, the single caller and the tests. Item 4's decision stands (J1r6:519). No public code, row, detail or remedy changes. No product file of X5a changes: `fact_admission.rs` and the evaluator's accessor stay as they are.
- **Citations.** J1r6:n is `m3/host-pipeline-j/PROPOSAL-r6.md` (J1 r6, accepted by Codex, `086e804a…`). X7r7:n is `finalization-x7/PROPOSAL-r7.md` (X7 r7, accepted by GROK2, `7757935c…`). X3D9:n is `commit-session-x3d/PROPOSAL-r9.md` (X3d r9, accepted by Grok, `c727001a…`). IE:n is `docs/v2/contracts/product-v1/identity-and-evidence.md`. X5:n is this law's `PROPOSAL-r3.md`.

## r4 changes

| Where | r3 | r4 | Source |
|---|---|---|---|
| Item 3, the order | "Order: replay before any custody". Replay runs before X1 write admission, X2 project admission and `CommitSession::open`. A refusal "ends the invocation before any fence, lease, attempt row, object or journal effect exists", "with nothing to clean up" (X5:39) | Replay runs after evaluation and before `prepare_commit`, inside host finalization. A replay refusal ends the attempt before any attempt row, object or journal effect. The lease and the session end through `refused()` and then `finish`, exactly once, and nothing is appended | J1r6:513-517; J1r6:538 (J-C12); X3D9:550-554 (S10.6); X7r7:312-326 (S9.1) |
| Item 3, the rejected alternative | "replaying under the project lease" (X5:43) | Withdrawn. r3's own order is rejected instead, because the candidate exists only after evaluation, which runs under the lease | J1r6:518; IE:1657-1658 |
| Item 4, the reason | "because it runs before that ledger's operation begins and performs no native observation" | The first reason is withdrawn: replay now runs inside the operation. The decision, and its other reason, stand | J1r6:519; X7r7:331 |
| Item 7, F01 | "a replay refusal publishes nothing, because the invocation ends before any effect" | The attempt ends before any attempt row, object or journal effect, and the session's end appends nothing | item 3 (r4) |
| Item 9 | (none) | r4 adds no unit. J3b moves the one call site in `finalization.rs` | J1r6:913; X7r7:312-322 |
| Forbidden substitutes | "replay under a held fence or lease" | "replay under a held fence". One substitute is added: a replay refusal that ends the session other than through `refused()` and then `finish`, exactly once | J1r6:518, :538 |

## Problem

X3d accepts only the evaluator's opaque `ReplayedRun` (X3d item 10): `prepare_commit(ReplayedRun, CommitSession)`. At 7e676a9 the replay owner exists: `opensip_evaluator::replay_run(&RetainedInputs, run_id, ReplayLimits) -> Result<ReplayedRun, ReplayError>` is the only constructor of `ReplayedRun`, which has private fields, no `Default`, no deserialization and a `compile_fail` doctest against forging. `opensip_identity::RetainedInputs::new(registry, objects, blobs)` borrows immutable caller-supplied values and does no I/O. Nothing in the host turns a candidate Run into a `ReplayedRun` and hands it to the commit facade. `crates/host/src/fact_admission.rs` does not exist.

F01 requires that a replay refusal, or a substituted target or inventory, publish no authority: "neither structural-only validation nor a stale boolean/token can publish authority", and "an identity-valid but replay-invalid candidate never publishes authority" (build plan, required checks).

## Decisions

1. **Scope: the M2 slice of `fact_admission.rs` is the replay join only (lead decision).** The build plan gives `host/fact_admission.rs` two jobs: the replay join for commit (M2), and source, context, occupancy, relation-at-rung and Coverage joins before ordinary evaluation (line 680; DR-G23 and DR-G25, both M3). X5 creates the module with the replay join alone. The syntax and Coverage joins arrive with M3 in the same module. **Rejected:** creating a separate `replay_join.rs` module, which would leave `fact_admission.rs` with two owners for one boundary.

   **Correction to EXIT-PLAN.** The plan lists G24 against X5. DR-G24 is the policy-pack gate (`crates/evaluator/src/policy.rs`, `crates/host/src/configuration.rs`: registered declarative policy, no imperative pack, strict numeric overrides). It is not the replay join. X5 prepares F01 only; G24 stays with its own owners.

2. **The API (lead decision).** One host function:

   `fact_admission::replay_candidate(candidate: &RunCandidateInputs<'_>, limits: ReplayLimits) -> Result<ReplayedRun, ReplayRefusal>`

   - `RunCandidateInputs` borrows exactly what `RetainedInputs::new` needs (the registered schemas, the object map and the blob map) plus the claimed `run_id`. It is the build plan's inert `RunCandidate`: anyone may construct it, and it claims nothing.
   - The function builds `RetainedInputs`, calls `opensip_evaluator::replay_run` once, and returns its `ReplayedRun` unchanged.
   - It never inspects, edits or re-serializes the Run, never supplies a truth map or callback, and never accepts a boolean, a RunId string or a previously serialized result as proof.
   - `ReplayLimits` is a host constant set (`REPLAY_LIMITS`), never a caller argument at the boundary into commit. How that is held while the signature keeps `limits` is item 5d.
   - **r3: `ReplayRefusal`.** It holds the claimed RunId and the evaluator's `ReplayError` unchanged, as the exact diagnostic retained separately (evaluator-fault-contract v3). It has read-only getters. It is crate-private, as are `RunCandidateInputs` and `replay_candidate` (item 6).

   **Rejected:** a host wrapper type around `ReplayedRun`. X3d and storage must receive the evaluator's own opaque type, so a wrapper would add a second unforgeable-looking type with no extra guarantee.

3. **Order: replay after evaluation and before `prepare_commit` (lead decision; r4, J1's successor S8).** Replay is pure: it reads only the borrowed inputs and takes no lock.
   - **r4: where it runs.** Host finalization runs `replay_candidate` after evaluation and before `prepare_commit` (J1r6:514, :517; X7r7:315). By then the pipeline has made X1's write admission and X2's project admission and handoff, and the session is open. The session opens at the handoff, so the attempt's ExecutionId exists before any provider spawns, and the writer holds the lease through source admission, evaluation and commit (J1r6:508-510; IE:1657-1658). The handoff releases the fence, so replay runs under the lease and never under the fence.
   - **r4: what a replay refusal leaves.** It ends the attempt before any attempt row, object or journal effect. The session then ends through `CommitSession::refused()` and `finish`, exactly once (J1r6:515, :538). `prepare_commit` never runs, so no end-path reserve exists, and `finish` appends nothing. `finish` releases the lease and runs its end step only on an open attempt ledger (X3D9:550-554). The refusal is projected on its item 5 row (X7r7:323-324). That is F01's "no authoritative receipt".
   - **r3 read** (X5:39): "The host runs `replay_candidate` before X1 write admission, X2 project admission and `CommitSession::open`. A replay refusal therefore ends the invocation before any fence, lease, attempt row, object or journal effect exists. That is F01's "no authoritative receipt", with nothing to clean up."
   - The binding comparison between the `ReplayedRun` and the session (target identity, inventory, producer closure) stays X3d's (item 3 step 1, the invariant row on mismatch). X5 does not duplicate it, and nothing on the X5 side can satisfy it.
   - Changed Plan inputs require a new replay (build plan line 66). A `ReplayedRun` is consumed by one `prepare_commit` and is not cached across invocations.

   **r4: r3's rejected alternative is withdrawn.** r3 rejected "replaying under the project lease" because it lengthened the lease hold with pure work, and a replay failure would then cost a lease and an attempt row it never needed (X5:43). IE:1657-1658 now holds the lease through evaluation, so replay runs under it (J1r6:518). A replay failure still costs no attempt row: the attempt row is `prepare_commit`'s step 4, which a refusal never reaches.

   **Rejected (r4): r3's order, replay before any custody.** The candidate is the evaluation's output, and evaluation runs under the lease and the open session (J1r6:508-510). So no replay of it can come before custody. Keeping r3's order would need evaluation outside the lease, which IE:1657-1658 forbids, or the session opened only at the commit, which J1 rejects because providers would then run under no ExecutionId (J1r6:534).

4. **Budget (lead decision).** Replay is bounded by `ReplayLimits` (the evaluator's local resource bounds: retained-walk limits, capture entries, retained bytes), which the evaluator documents as separate from operational work budgets. X5 fixes `REPLAY_LIMITS` as named constants (values in item 5e). Replay is not charged to X1's attempt ledger, because it performs no native observation. **r4:** r3 also gave the reason "it runs before that ledger's operation begins". Under item 3's r4 order, replay runs inside the operation, after the session opens, so that reason is withdrawn. The decision stands (J1r6:519), and so does X7's item 7: finalization charges nothing (X7r7:331). **Rejected:** charging replay to the attempt ledger, which would let pure semantic work exhaust the owner caps meant for native custody work.

5. **Refusal rows (existing details only; r3).** Every `ReplayRefusal` maps to exactly one row, in two steps.

   **Step 1, unavailable evidence first.** If `ReplayError::unavailable_evidence()` (item 5a) returns `Some(reference)`, the row is the promised-bytes-lost retention route (evaluator-fault-contract v3, `promised-bytes-lost:evidence-store`; identity's `EvidenceUnavailable` carrier). That route is operational-failed, exit 4, `HOST.IO_FAILURE`, `host-io`, detail `evidence.missing`, with subject the missing reference: the object key, or the blob digest as 64 lowercase hex characters. This holds wherever the evaluator reports the missing object or blob: at top level, under `Structure`, or under `Evaluation`.

   **Step 2, otherwise the variant table.** It is an exhaustive match on `ReplayError` with no wildcard arm:

   | `ReplayError` | Route |
   |---|---|
   | `Structure`, `Capture`, `Law`, `Input` (every variant left after step 1: schema, identity, digest or decode failures), and `Evaluation(e)` for every `e` | The structural evaluator input failure (item 5b): operational-failed, exit 4, `PROVIDER.PROTOCOL_VIOLATION`, `provider-protocol`, detail `EVALUATION.INPUT_REFUSED`, with the exact diagnostic retained separately (evaluator-fault-contract v3) |
   | `Mismatch { key, target }` | The retained-regeneration route (`complete-replay-mismatch:retained-regeneration`; identity's `RegenerationMismatch`): operational-failed, exit 4, `HOST.IO_FAILURE`, `host-io`, `evidence.regeneration-mismatch`, with subject the affected Run reference (item 5c) |

   - **Precedence.** Where S12 or the evaluator-fault contract fixes a class and exit for a detail, that class prevails. No new code is added. No failure envelope may replace a missing complete Run with an empty success (evaluator-fault-contract v3).
   - **Where the rows live.** They live in the host projection where X12b already projects an evaluator refusal: `InstallationTerminationV1` (`crates/host/src/installation_termination.rs`), through a crate-private `replay_termination(&ReplayRefusal) -> InstallationTerminationV1` in `fact_admission.rs`, as `configuration.rs`'s `policy_selection_termination` does. Security's `InstallationTermination` gains no row.
   - **r3, `Evaluation(e)`.** r2 sent it to "the evaluator's own fault mapping for e … (for example `EVALUATION.WORK_BUDGET_EXHAUSTED`)". No such mapping exists in the evaluator, and that example is withdrawn:
     - `EVALUATION.WORK_BUDGET_EXHAUSTED` is an indeterminate-class deficiency that a sealed Run carries (workflow-projection-contract v3, appendix: "the sealed Run's termination MUST carry D9 deficiency `budget-exhausted`"). It is not a termination.
     - The fault contract excludes "exhausted logical analysis budgets" from its fault conditions.
     - During replay, an `EvaluationError` (including `Limit`, the owner traversal bound of `REPLAY_LIMITS`) is the evaluator refusing to re-derive the retained closure. That is the structural row, the same row `Structure(Limit)` and `Capture(Limit)` already take.

   **Rejected:** a separate row per `EvaluationError` variant. The contract fixes no other condition for them, and a borrowed detail would carry a remedy its owner did not fix.

5a. **The unavailable-evidence accessor (lead decision, r3).** The evaluator owns its error tree, so it classifies it:

   `impl ReplayError { pub fn unavailable_evidence(&self) -> Option<UnavailableEvidence> }`

   `UnavailableEvidence` is an evaluator-exported, inert enum, `Object(String)` (the key) and `Blob([u8; 32])` (the raw digest), with `reference(&self) -> String` giving the step 1 subject.
   - **Where it lives.** A new evaluator module, `crates/evaluator/src/unavailable_evidence.rs`. It is pure, does no I/O, and grants nothing.
   - **How it searches.** It descends every variant of `ReplayError` and of each nested error type reachable from it, in the evaluator and in identity:
     - the evaluator's types, among them `RetainedWalkError`, `EvaluationError`, `ReconstructionError`, the native, plan, policy, stage, predicate, view, import, payload, run-link, body, coverage and enumeration-join errors;
     - identity's `GraphError`, `RetainedInputError` and `CaptureError`.

     It returns `Some` exactly for `RetainedInputError::MissingObject` and `RetainedInputError::MissingBlob`, wherever they are nested, and `None` for every other leaf.
   - **No wildcard.** Every match in the module is exhaustive with no wildcard (`_`) arm, so a new variant anywhere in the tree fails to compile until it is classified. A source pin in the module's tests refuses a `_ =>` arm.
   - **No text.** A payload that is only text (`Refused(String)`, `ExecutionRefused(V)` and the like) is not inspected. It is `None`, because the fault contract forbids establishing origin from error text.
   - **`replay_run` is unchanged.** Its returned values, its order and the evaluator's existing replay test stay as they are.

   **Rejected:**
   - **The host matching the evaluator's error tree itself.** The host would own about twenty evaluator and identity error types, and every evaluator variant change would break a host module that does not own it.
   - **Searching the `Debug` text** for `MissingObject(` or `MissingBlob(`, as the existing host replay test does. The fault contract says the adapter "does not parse exception text to establish origin". The existing test stays a test.
   - **Hoisting missing evidence to a top-level `ReplayError::Input` inside `replay_run`.** It needs the same exhaustive descent, and it also changes the values the evaluator's replay test pins and the order of `replay_run`.

5b. **The class of `EVALUATION.INPUT_REFUSED` (r3).** The fault contract publishes `EVALUATION.INPUT_REFUSED` under three routes: `external-specification`, `release-declaration` (request-rejected, `REQUEST.PRECONDITION_FAILED`) and `provider-return` (operational-failed, `PROVIDER.PROTOCOL_VIOLATION`, `provider-protocol`). r2 named the detail and not the route.

   The candidate is retained producer data, and the contract says "Re-admitting retained producer data preserves the producer-contract meaning of a structural violation", "including re-derivation over retained producer inputs". So the route is `provider-return`, as item 5's table states, and the remedy is that route's (item 5d).

   **Rejected:** the request-rejected `external-specification` route. Its remedy ("Supply a specification admitted under the selected contract") names a caller-supplied specification that a retained candidate is not.

5c. **The mismatch subject (r3).** The affected Run reference is the claimed RunId of the candidate, as identity's `RegenerationMismatch(run_id)` carries it, and the contract requires it ("no anonymous regeneration mismatch is admitted"). The evaluator's `key` and `target` (often `None`) stay in the retained diagnostic.

5d. **Remedies and the `limits` parameter (r3).**
   - **Remedies.** `InstallationTerminationV1` has no remedy field. As X12b does (`REMEDY_CONFIG_INVALID`), `fact_admission.rs` holds the three route remedies as crate-private constants, byte for byte from the fault schema's `x-opensip-routes`, which equal the identity carriers' verbatim:
     - `promised-bytes-lost:evidence-store`: "Restore the exact retained closure bytes or report their unavailability.";
     - `complete-replay-mismatch:retained-regeneration`: "Retain the sealed Run and investigate the differing regeneration result.";
     - `input-schema-invalid:provider-return` (and its identity and join twins): "Correct the provider output and rerun the stage; retain its admission diagnostic."

     A crate-private `replay_remedy(&ReplayRefusal) -> &'static str` maps each refusal to its route's remedy by the same two steps.
   - **`limits`.** The signature of item 2 keeps `limits`, so the bounds test can vary it. A source pin in `fact_admission.rs`'s tests requires every production call of `replay_candidate(` under `crates/host/src` to pass `REPLAY_LIMITS` as written. It passes vacuously until X7a adds the one caller.

     **Rejected:** dropping the parameter and adding a second private entry point for tests. That adds a function the law does not name.

5e. **`REPLAY_LIMITS` and the bounds test (r3).** No design source fixes the values. `REPLAY_LIMITS` takes the values the host's replay corpus test (`crates/host/src/native_owner_tests.rs`) and X3d-2's storage tests already replay under:
   - walk and owner budgets: 20 000 000 steps, depth 96 and 20 000 000 descriptor work each;
   - 100 000 owner invocations;
   - 100 000 capture entries;
   - 33 554 432 retained bytes (32 MiB).

   **The test.** A corpus at 20 000 000 steps is not buildable, so item 4's test measures the corpus. For each dimension, it takes `REPLAY_LIMITS` with only that dimension changed:
   - at the corpus's measured exact need, the corpus replays;
   - at one less, it is refused, on the structural row;
   - the need is at most the constant.

   Capture entries are also tested at the constant itself: ambient entries pad the inputs to exactly 100 000 entries, which replays, and one more is `Capture(Limit)`.

5f. **Compile-fail rows (r3; X8 r3 item 3).** X5a adds two fixtures to X8a's driver, with census rows for unit X5a:
   - **Group E, `ClonedOrReused`:** a `ReplayedRun` passed to a second `prepare_commit`, E0382 "use of moved value". This is X8 r3's X5a row.
   - **Group C, `StructuralOnly`:** `RunCandidateInputs`, the build plan's `RunCandidate`, is unnameable outside the host, E0603. This pins X3d item 11's "a `RunCandidate` in place of `ReplayedRun`", which X8 r3's table does not list. Under X8's export rule, a type its owner keeps crate-private takes the unnameable case.

6. **Where the join is called.** Only host finalization (X7) calls `replay_candidate` and then passes the `ReplayedRun` to `prepare_commit`. X5 exposes the function `pub(crate)` inside the host crate. Storage and security never call it. **Rejected:** a public host export, which would invite a second commit coordinator.

7. **Failure cases.**
   - **Covered:** F01, both halves:
     - a replay refusal publishes nothing (items 3 and 5). **r4:** the attempt ends before any attempt row, object or journal effect, and the session's end through `refused()` and `finish` appends nothing (item 3). r3 read "because the invocation ends before any effect";
     - a substituted target or inventory is refused at X3d's binding check, because only a `ReplayedRun` for the replayed Run can reach it.
   - **Elsewhere:** the binding comparison itself (X3d item 3 step 1), and everything after `prepare_commit` (X3d, X3c, X3b, X4).
   - **X8c's B0 Run (r3).** The X3d-2 review (call 3) found that no corpus Run binds to a scenario project, whose `ProjectId` is a fresh draw, and suggested a Run "through X5a's producer". X5 has no producer: analysis producers are M3 (Not claimed). B0's Run, bound to the scenario project's `projectId`, is a synthetic, labelled fixture that X8c owns and builds. X5a supplies only the join that replays it.

8. **Tests.** The tests live in host, except the accessor's own tests in the evaluator, and need no scratch installation, since replay is pure:
   - the evaluator's existing replay corpus (`crates/host/tests/fixtures/replay-fixtures.json`) replays through `replay_candidate`, and the result's `run_id()` equals the claim;
   - each `ReplayError` variant maps to its item 5 row, and its remedy to item 5d's, and the public members agree with the fault schema's routes;
   - a tampered output (one byte of a claimed output, the corpus's forged cases) is `evidence.regeneration-mismatch`, with subject the claimed RunId;
   - **r3:**
     - the corpus's `missing-blob-…` case is `HOST.IO_FAILURE` / `host-io` / `evidence.missing` with that digest;
     - removing each object and each blob of the claimed closure of one corpus case, one at a time, is `evidence.missing`, naming exactly the removed reference;
   - a schema or identity failure inside `Input` is `EVALUATION.INPUT_REFUSED` on the provider-return route;
   - the limits test of items 4 and 5e;
   - a source pin shows that `fact_admission.rs` calls `replay_run` exactly once, calls no other evaluator function (in particular not `check_plan_pack`, which X12 r3 item 9 leaves unwired in M2), and constructs no `ReplayedRun`, `RunId` or verdict itself;
   - the `REPLAY_LIMITS` caller pin of item 5d;
   - **r3, the evaluator's accessor tests:**
     - `Some` for a missing object and a missing blob at top level, under `Structure(Graph(Input(..)))`, under `Structure(Retention(Owner(Frame(Input(..)))))`, and under `Evaluation(Reconstruction(..))`;
     - `None` for every other corpus refusal and for a text-only refusal;
     - the no-wildcard pin of item 5a;
   - the two fixtures of item 5f, with the X8a driver green.

   The end-to-end case, where a replayed Run passes through X3d into a committed receipt on a scratch installation, belongs to X8c's B0 and X9's matrix.

9. **Units (r3).** One combined unit, **X5a**:
   - **Evaluator:** `crates/evaluator/src/unavailable_evidence.rs` with `UnavailableEvidence` and `ReplayError::unavailable_evidence` (item 5a), and their tests.
   - **Host:**
     - `crates/host/src/fact_admission.rs` with `replay_candidate`, `RunCandidateInputs`, `ReplayRefusal`, `REPLAY_LIMITS`, `replay_termination`, `replay_remedy` and the remedy constants (items 2, 4 and 5 to 5e);
     - the tests;
     - the two X8 fixtures and their census rows (item 5f).
   - **One inventory successor** that lists the new files of both crates.
   - **Dependencies.** None beyond the current product. It can land before X7a, which depends on it.

   **Why one unit, not X5a-0 plus X5a.** The accessor has no caller but X5a's mapping, and is about one module. The inventory chain is linear (verify_design), so a split would burn one more successor and one more re-review for a module whose only reason to exist is reviewed in the same request.

   **r4: no new unit.** r4 changes no X5a file. J3b carries "X5 r4 code" (J1r6:913): it moves the one call of `replay_candidate`, inside `finalization.rs`, to item 3's order, with X7 r7's new `finalize` signature (X7r7:312-322). X9 r17's §S12 records the matrix runner that follows from it.

## Forbidden substitutes

A `ReplayedRun` built anywhere but `replay_run`; a boolean, token, RunId string or serialized prior result standing in for replay; structural-only validation as authority; replay under a held fence (**r4:** r3 also forbade replay under a held lease, which item 3 now requires); a host wrapper type around `ReplayedRun`; caching a `ReplayedRun` across invocations or reusing it for a second `prepare_commit`; a caller-chosen `ReplayLimits` at the commit boundary; charging replay to an operation ledger; a new public code. **r3:** classifying missing evidence from error text; a wildcard arm in the accessor or in the row mapping; a lost retained byte reported as `EVALUATION.INPUT_REFUSED`; `EVALUATION.WORK_BUDGET_EXHAUSTED` as a replay termination. **r4:** a replay refusal that ends the session other than through `refused()` and then `finish`, exactly once.

## Not claimed

The M3 syntax, context, occupancy and Coverage joins in `fact_admission.rs`; DR-G24 (policy packs); any analysis producer of candidate Runs (M3); X8c's B0 synthetic Run (item 7); CLI enablement; compiler or semantic truth beyond what replay establishes ("`ReplayedRun` establishes semantic validity, not compiler truth, present custody or current availability", build plan line 64).
