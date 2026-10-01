# The replay-to-commit join — proposal X5 r2

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X5 of `EXIT-PLAN.md`, under the build plan's opaque-prerequisite decision (lines 25–70: `RunCandidate`, `ReplayedRun`, `CommitSession`, `PreparedCommit`), its M2 row (line 886: "Evaluator replay; … host fact_admission/finalization") and failure case F01, and under the accepted laws X3d r3 (items 1, 3 step 1 and 10), X3c r7, X4 r7 and X2 r5. Items 1 to 6 contain lead decisions made under the owner's standing direction to proceed on the lead's recommendation; each names the alternative it rejects. r2 answers Grok X5 r1 RF-1: a missing retained object or blob is unavailable evidence, not an input refusal. r1 bytes are preserved in PROPOSAL-r1.md. r2 ACCEPTED by Grok on 2026-10-01. Not code. Library only: no CLI command is wired.

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
   - `ReplayLimits` is a host constant set (`REPLAY_LIMITS`), never a caller argument at the boundary into commit.

   **Rejected:** a host wrapper type around `ReplayedRun`. X3d and storage must receive the evaluator's own opaque type, so a wrapper would add a second unforgeable-looking type with no extra guarantee.

3. **Order: replay before any custody (lead decision).** Replay is pure: it reads only the borrowed inputs and takes no lock. The host runs `replay_candidate` before X1 write admission, X2 project admission and `CommitSession::open`. A replay refusal therefore ends the invocation before any fence, lease, attempt row, object or journal effect exists. That is F01's "no authoritative receipt", with nothing to clean up.
   - The binding comparison between the `ReplayedRun` and the session (target identity, inventory, producer closure) stays X3d's (item 3 step 1, the invariant row on mismatch). X5 does not duplicate it, and nothing on the X5 side can satisfy it.
   - Changed Plan inputs require a new replay (build plan line 66). A `ReplayedRun` is consumed by one `prepare_commit` and is not cached across invocations.

   **Rejected:** replaying under the project lease. That lengthens the lease hold with pure work, and a replay failure would then cost a lease and an attempt row it never needed.

4. **Budget (lead decision).** Replay is bounded by `ReplayLimits` (the evaluator's local resource bounds: retained-walk limits, capture entries, retained bytes), which the evaluator documents as separate from operational work budgets. X5 fixes `REPLAY_LIMITS` as named constants with a test that a corpus at each bound replays and one above refuses. Replay is not charged to X1's attempt ledger, because it runs before that ledger's operation begins and performs no native observation. **Rejected:** charging replay to the attempt ledger, which would let pure semantic work exhaust the owner caps meant for native custody work.

5. **Refusal rows (existing details only).** `ReplayError` maps one-to-one, by an exhaustive match with no wildcard arm, including over every `RetainedInputError` variant inside `Input`:

   | `ReplayError` | Termination |
   |---|---|
   | `Input(MissingObject(key))`, `Input(MissingBlob(digest))` | The promised-bytes-lost retention route (evaluator-fault-contract v3, `promised-bytes-lost:evidence-store`; identity's `EvidenceUnavailable` carrier): operational-failed, exit 4, `HOST.IO_FAILURE`, `host-io`, detail `evidence.missing`, carrying the missing object key or blob digest as the reference |
   | `Structure`, `Capture`, `Law`, and every other `Input` variant (schema, identity, digest or decode failures) | The structural evaluator input failure: `EVALUATION.INPUT_REFUSED`, with the exact diagnostic retained separately (evaluator-fault-contract v3) |
   | `Mismatch { key, target }` | The retained-regeneration route: `HOST.IO_FAILURE`, `host-io`, `evidence.regeneration-mismatch`, carrying the affected Run reference (identity's `RegenerationMismatch`; evaluator-fault-contract v3) |
   | `Evaluation(e)` | The evaluator's own fault mapping for `e`, which the evaluator-fault-contract already fixes (for example `EVALUATION.WORK_BUDGET_EXHAUSTED`) |

   Where S12 or the evaluator-fault contract fixes a class and exit for a detail, that class prevails. No new code is added. No failure envelope may replace a missing complete Run with an empty success (evaluator-fault-contract v3).

6. **Where the join is called.** Only host finalization (X7) calls `replay_candidate` and then passes the `ReplayedRun` to `prepare_commit`. X5 exposes the function `pub(crate)` inside the host crate. Storage and security never call it. **Rejected:** a public host export, which would invite a second commit coordinator.

7. **Failure cases.**
   - **Covered:** F01, both halves:
     - a replay refusal publishes nothing, because the invocation ends before any effect (items 3 and 5);
     - a substituted target or inventory is refused at X3d's binding check, because only a `ReplayedRun` for the replayed Run can reach it.
   - **Elsewhere:** the binding comparison itself (X3d item 3 step 1), and everything after `prepare_commit` (X3d, X3c, X3b, X4).

8. **Tests.** The tests live in host and need no scratch installation, since replay is pure:
   - the evaluator's existing replay corpus replays, and the result's `run_id()` equals the claim;
   - each `ReplayError` variant maps to its item 5 row;
   - a tampered output (one byte of a claimed output) is `evidence.regeneration-mismatch`;
   - a missing retained object, and a missing retained blob, are each `HOST.IO_FAILURE` / `host-io` / `evidence.missing` with the missing reference;
   - a schema or identity failure inside `Input` is `EVALUATION.INPUT_REFUSED`;
   - the limits test of item 4;
   - a source pin shows that `fact_admission.rs` calls `replay_run` exactly once and constructs no `ReplayedRun`, `RunId` or verdict itself.

   The end-to-end case, where a replayed Run passes through X3d into a committed receipt on a scratch installation, belongs to X3d-2's tests once X2e exists, and to X9's matrix.

9. **Units.** One unit, **X5a**: `crates/host/src/fact_admission.rs` with `replay_candidate`, `RunCandidateInputs` and `REPLAY_LIMITS`, the item 5 mapping into 468c's termination vocabulary (or the host projection where the evaluator rows already live), the tests, and an inventory successor. It depends on nothing beyond the current product; it can land before X3d.

## Forbidden substitutes

A `ReplayedRun` built anywhere but `replay_run`; a boolean, token, RunId string or serialized prior result standing in for replay; structural-only validation as authority; replay under a held fence or lease; a host wrapper type around `ReplayedRun`; caching a `ReplayedRun` across invocations or reusing it for a second `prepare_commit`; a caller-chosen `ReplayLimits` at the commit boundary; charging replay to an operation ledger; a new public code.

## Not claimed

The M3 syntax, context, occupancy and Coverage joins in `fact_admission.rs`; DR-G24 (policy packs); any analysis producer of candidate Runs (M3); CLI enablement; compiler or semantic truth beyond what replay establishes ("`ReplayedRun` establishes semantic validity, not compiler truth, present custody or current availability", build plan line 64).
