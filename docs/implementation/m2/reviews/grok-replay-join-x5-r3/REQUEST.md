Grok review r3: law X5 r3, the replay-to-commit join (`replay-join-x5/PROPOSAL.md`). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-replay-join-x5-r3. This is a law review: no product cargo is needed. If you choose to replay the probe below, use a CARGO_TARGET_DIR under that directory and a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, never `/private/tmp/claude-501`. Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH`; Python is `python3.14`. Run git only read-only. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read or print the private 413 UUID fixture.

## Subject

Pins are in hashes.txt.
- `docs/implementation/m2/replay-join-x5/PROPOSAL.md`, r3.
- `docs/implementation/m2/replay-join-x5/PROPOSAL-r2.md`, the preserved r2 bytes. Their sha256 must equal the subject you accepted in `reviews/grok-x5r2-x6r2-x2r6/x5/review.json` (`d2a1f585517b19a6c07b5a6267875dd2d728c05ffa1a7c49bd62cf4a33454365`, 9800 bytes).

Product: main `adc9081` (`/Users/sb/code/opensip-ai/opensip`, or the clean worktree `/Users/sb/code/opensip-ai/opensip-x5a` at the same commit).

## Why r3

While building X5a, the lead found that r2 item 5 contradicts r2 item 8 and RF-1. r2 routes `Input(MissingObject)` and `Input(MissingBlob)` to `evidence.missing`, and all of `Structure` to `EVALUATION.INPUT_REFUSED`. `replay_run` (`crates/evaluator/src/replay.rs`) runs `inspect_retained_walk` over the whole closure before any top-level read, so a missing object or blob is reported nested under `Structure`.

The lead's probe was a temporary test, since removed, run against `crates/host/tests/fixtures/replay-fixtures.json` at adc9081:
- The corpus case `missing-blob-03cc96…` (expected `EVIDENCE_UNAVAILABLE`) returns `Structure(Graph(Input(MissingBlob(..))))`.
- For cases `packet-0-original`, `forged-verdict` and `forged-empty-rule-results`, it removed each object and each blob in turn, one at a time:
  - every removal the walk reached gave `Structure(Graph(Input(Missing…)))` (63 objects, 99 blobs) or `Structure(Retention(Owner(Frame(Input(Missing…)))))` (3 objects, 36 blobs);
  - the rest were ambient: 11 objects and 2 blobs gave the forged cases' `Mismatch`, and 1 blob replayed;
  - no removal produced a top-level `Input(Missing…)`.
- The existing host test `independent_run_replay_matches_selected_reference_and_owns_its_closure` (`crates/host/src/native_owner_tests.rs`) already detects these cases only by searching the `Debug` text.

## What r3 changes

The owner's standing direction applies; the lead took each choice as a lead decision.
- **Item 5:** two steps. First, `ReplayError::unavailable_evidence()` returning `Some` is `evidence.missing`. Then an exhaustive variant table.
- **Item 5a:** the evaluator-owned accessor and `UnavailableEvidence`, in a new `crates/evaluator/src/unavailable_evidence.rs`. Its matches are exhaustive with no wildcard over the nested evaluator and identity error tree, and it does not inspect text. Three rejected alternatives: host-side descent, `Debug` text search, and hoisting inside `replay_run`.
- **Item 5b:** `EVALUATION.INPUT_REFUSED` takes the `provider-return` route: operational-failed, exit 4, `PROVIDER.PROTOCOL_VIOLATION`, `provider-protocol`.
- **Item 5, the `Evaluation(e)` row:** every `EvaluationError` takes the structural row. r2's `EVALUATION.WORK_BUDGET_EXHAUSTED` example is withdrawn: that detail is an indeterminate-class deficiency of a sealed Run (workflow-projection-contract v3, appendix), and the fault contract excludes exhausted logical budgets.
- **Item 5c:** the mismatch subject is the claimed RunId.
- **Item 5d:** remedy constants, as X12b does, from the fault schema's routes. `limits` stays a parameter, with a source pin that production callers pass `REPLAY_LIMITS`.
- **Item 5e:** the `REPLAY_LIMITS` values (those the corpus and X3d-2's tests use), and the bounds test by measured exact need, plus capture entries at the constant.
- **Item 5f:** a group E fixture (`ReplayedRun` reuse, E0382) and a group C fixture (`RunCandidateInputs` unnameable, E0603, for X3d item 11's `RunCandidate` case, which X8 r3's table omits).
- **Item 7:** X8c owns B0's synthetic Run. This answers the X3d-2 review's call 3, which named "X5a's producer"; X5 has none.
- **Items 8 and 9:** the new tests, and one combined X5a unit (evaluator and host) with one inventory successor. The split into X5a-0 and X5a is rejected because the chain is linear.

Unchanged: items 1, 3, 4 (except its reference to 5e), 6, the F01 coverage, and the forbidden substitutes (r3 adds four).

## Sources

- `docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md` and `evaluator-fault-observation.schema.v3.json` (`x-opensip-routes`).
- `docs/coop/design-corrections/foundation/identity-model.py`: `EvidenceUnavailable` and `RegenerationMismatch`, near line 607.
- `docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md`, the appendix table near line 140.
- `docs/coop/design-corrections/public-detail-registry.v1.json`.
- The accepted laws X3d r6 (items 9 to 11), X8 r3 (item 3, groups C, E and K, and the export rule), X7 r3 (items 1 and 11), X12 r3 (item 9), and the review `reviews/grok-commit-facade-x3d2-r1/REVIEW.md` (call 3).
- Product: `crates/evaluator/src/replay.rs`, `crates/evaluator/src/full_walk.rs`, `crates/identity/src/closure.rs`, `crates/host/src/configuration.rs` and `crates/host/src/installation_termination.rs`.

## Decide

- Is the contradiction real, and does r3's two-step mapping resolve it without changing `replay_run`?
- Is the accessor sound: exhaustive, no wildcard, no text, owned by the evaluator? Are the rejected alternatives rightly rejected?
- Are items 5b to 5f right against the fault contract, the identity carriers, S12 and X8 r3?
- Is withdrawing the `WORK_BUDGET_EXHAUSTED` example right?
- Is one combined unit acceptable?
- Is the B0 note right?
- Is PROPOSAL-r2.md byte-equal to the accepted r2?
- Is anything else wrong?

review.json must contain top-level "verdict" (`ACCEPT` or `REQUIRED-FINDINGS`), "requiredFindings" and "subjectSha256" (the sha256 of r3's PROPOSAL.md; lead's value in hashes.txt). Write REVIEW.md and review.json. Do not commit.
