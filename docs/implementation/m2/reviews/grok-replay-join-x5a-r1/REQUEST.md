Grok review r1: X5a, the replay join as one combined evaluator and host unit (law X5 r3 item 9), with X8 r3 item 3's owner rows for this unit and inventory v123 (parent v122). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-replay-join-x5a-r1.

**Rules for any run.**
- Use a CARGO_TARGET_DIR under that directory.
- Run every test with a private TMPDIR: create a 0700 directory under `$(getconf DARWIN_USER_TEMP_DIR)` (for example `…/grok-x5a-tmp`). Never use the shared `/private/tmp/claude-501` tree, which other runs churn.
- Run git only read-only, and only against the worktree below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read or print the private 413 UUID fixture.
- Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH`; Python is `python3.14`.

## The unit

X5 r3 item 9 defines X5a as one combined unit:
- **Evaluator:** `crates/evaluator/src/unavailable_evidence.rs`, with `UnavailableEvidence` and `ReplayError::unavailable_evidence` (item 5a), and their tests.
- **Host:** `crates/host/src/fact_admission.rs`, with:
  - `replay_candidate`, `RunCandidateInputs`, `ReplayRefusal` and `REPLAY_LIMITS`;
  - `replay_termination` and `replay_remedy`, and the remedy constants (items 2, 4 and 5 to 5e);
  - the tests;
  - the two X8 fixtures and their census rows (item 5f).
- **One inventory successor.**

It depends on nothing beyond the current product. X7a depends on it. Library only: nothing calls `replay_candidate` before X7a, and no command commits.

## Law

All under arch `docs/implementation/m2/`, accepted:
- `replay-join-x5/PROPOSAL.md` r3 (sha256 `d9a101b83f083bed6e6b97f3b3d64344f07bb206e8ab14af75dac4aebc4d9b82`; your review `reviews/grok-replay-join-x5-r3/`), the law of this unit;
- `refusal-suite-x8/PROPOSAL.md` r3: item 1 (the driver), item 3 (groups C and E, and the export rule) and the "Owner rows" list;
- `commit-session-x3d/PROPOSAL.md` r6, items 3, 10 and 11;
- `finalization-x7/PROPOSAL.md` r3, items 1 and 11 (the one caller);
- `policy-admission-x12/PROPOSAL.md` r3, item 9 (`check_plan_pack` not wired into replay);
- `reviews/grok-commit-facade-x3d2-r1/REVIEW.md`, call 3 (the X8c B0 Run);
- `description-batch-d2/README.md`, "After selection" (D2 is bound at 933e78b; this successor folds its four supersessions).

Design sources for the rows:
- `docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md`;
- `docs/coop/design-corrections/foundation/evaluator-fault-observation.schema.v3.json` (`x-opensip-routes`);
- `docs/coop/design-corrections/foundation/identity-model.py` (`EvidenceUnavailable`, `RegenerationMismatch`).

## Subject

Pins are in hashes.txt.

**Product.** The worktree `/Users/sb/code/opensip-ai/opensip-x5a`, detached at `933e78b` (main). Since X3d-2's integration at adc9081, two commits have landed, neither changing product source:
- VD1's tooling at 96dd114 (`tools/verify_design.py`, `tools/tests/test_design_binding.py`);
- D2's binding at 933e78b (`design-lock.json` only).

The lock selects v122. Its 55 inheritance rows carry D1's 39 overrides, and D2's four `passageSupersessions` are bound on v122. The unit was written on 96dd114 and moved to 933e78b before review. Its diff applies unchanged; only v123's projection changed, by D2's fold.
- Save `git -C <worktree> diff` as product.diff and report its sha256. The five new files are intent-to-add.
- Lead's value: `5a36fbb1c41466ec34c1f41f7df421ea618cf0ba318f822b66a951c99082cd98`, 63492 bytes; 9 files, 1598 insertions(+), 2 deletions(-).

**Arch.** These files, all untracked:
- `repository-file-inventory.v123.json` (parent v122);
- `replay-join-x5a-inventory-v123-subject.json`;
- `replay-join-x5a-inventory-v123/`.

## What was built

**`crates/evaluator/src/unavailable_evidence.rs`** (item 5a). It is a new private module, and `UnavailableEvidence` is re-exported from the evaluator root.
- **`UnavailableEvidence`** is `Object(String)` or `Blob([u8; 32])`. It is inert, and `reference()` gives the key, or the digest as 64 lowercase hex characters.
- **`impl ReplayError { pub fn unavailable_evidence(&self) -> Option<UnavailableEvidence> }`** works through a private trait `Find`, implemented once for each of twenty-four types:
  - `ReplayError`;
  - identity's `RetainedInputError`, `GraphError` and `CaptureError`;
  - the evaluator's walk, evaluation, reconstruction, execution-input, native-universe, native-context, native-retention, native-support, body, plan-native, run-link, plan-capability, policy, stage, predicate, view, coverage-producer, import-join, import-payload and enumeration-join errors.

  Every match lists every variant with no wildcard arm. `Some` is returned exactly for `MissingObject` and `MissingBlob`.
- **Leaves.** Payloads of leaf types that cannot hold a `RetainedInputError` are leaves, matched as `Variant(..)`: `CanonicalError`, `CandidateError`, schema errors, `DigestError` and `CapabilityRefusal`. Text payloads are never read.
- **`replay_run`** is unchanged.

**`crates/host/src/fact_admission.rs`** (items 2 to 5e), a private module declared `#[allow(dead_code)]` until X7a, as `configuration` is.
- **`REPLAY_LIMITS`** (`pub(crate) const`) holds item 5e's values:
  - walk and owner each 20 000 000 steps, depth 96 and 20 000 000 descriptor work;
  - 100 000 owner invocations;
  - 100 000 capture entries;
  - 33 554 432 retained bytes.
- **`RunCandidateInputs<'a>`** borrows the registry, the object map, the blob map and the claimed `run_id`, all as `pub(crate)` fields.
- **`ReplayRefusal`** holds the claimed RunId and the evaluator's `ReplayError` unchanged, behind getters. It has `Debug` and `PartialEq` only.
- **`replay_candidate(&RunCandidateInputs, ReplayLimits) -> Result<ReplayedRun, ReplayRefusal>`** builds `RetainedInputs`, calls `replay_run` once, and returns its result. A refusal is wrapped with the claim.
- **`route`** (private) applies item 5's two steps:
  1. `unavailable_evidence()` returning `Some` is `EvidenceMissing { reference }`.
  2. Otherwise, an exhaustive match on `ReplayError`:
     - `Structure`, `Capture`, `Law`, `Input` and `Evaluation` are `InputRefused`;
     - `Mismatch` is `RegenerationMismatch` with the claimed RunId.
- **`replay_termination`** returns an `InstallationTerminationV1`:
  - `evidence.missing`: operational-failed, 4, `HOST.IO_FAILURE`, `host-io`, with subject the reference;
  - `EVALUATION.INPUT_REFUSED`: operational-failed, 4, `PROVIDER.PROTOCOL_VIOLATION`, `provider-protocol`, with no subject;
  - `evidence.regeneration-mismatch`: operational-failed, 4, `HOST.IO_FAILURE`, `host-io`, with subject the RunId.
- **`replay_remedy`** returns the matching constant, byte for byte from the fault schema's routes.

**`crates/host/src/doctor_ingress.rs`**: `row_remedy` gains those three details, each taking `fact_admission`'s remedy, so the shared failure envelope can render the rows (judgment call 4).

**X8 (`crates/host/tests`).** Two cases with census rows for unit X5a. The driver passes with 97 cases and 8 self-tests.
- `host_run_candidate_unnameable.rs`: group C, `StructuralOnly`, E0603, "module `fact_admission` is private".
- `evaluator_replayed_second_prepare_commit.rs`: group E, `ClonedOrReused`, E0382, "use of moved value: `replayed`".

**Inventory v123** adds 4 rows to v122, for 922 files:
- `unavailable_evidence.rs`;
- `fact_admission_tests.rs`;
- the two cases.

`fact_admission.rs` is already a planned row of v122, so it is kept by value. Every inherited row is equal by value to v122's bytes, and the 55-row projection is carried with only its selectors moved.

The README lists the existing rows this unit makes out of date, judged against their effective text: `fact_admission.rs`, `doctor_ingress.rs` and `admission_tests.rs`.

**D2.** Both `build_v123.py` and `verify_projection.py` fold each bound supersession into its row's inheritance entry, as D2's README and VD1 item 3 require. The `before` stays the raw row text, the effective description becomes D2's `after`, and the count stays 55. The four folded rows are `store_lineage.rs`, `installation_session.rs`, `read_premise.rs` and `initial_installation.rs`.

As a negative check, the same builder run on 96dd114's lock (no D2) gives an unfolded record. Under 933e78b's lock, the real verify_design refuses it with "inventory passage inheritance differs from reviewed ancestor meaning". The folded candidate under review was then rebuilt, byte-identical.

## Judgment calls: please rule

1. **Where the rows live.** Item 5 names the host projection. The rows are `InstallationTerminationV1` values built in `fact_admission.rs`, exactly as `configuration.rs` builds X12's.
   - Security's `InstallationTermination` gains no row.
   - The route enum is private to the module.
   - **Rejected:** new security rows, which would put evaluator routes into 468c's installation vocabulary.
2. **`ReplayRefusal` is not `Clone`, and has no public members.** It carries the evaluator's diagnostic, which is not `Clone`, unchanged. Its `Debug` is the derived one. It grants nothing, and it never reaches a public surface except through `replay_termination`.
3. **The `limits` pin.**
   - **How it reads.** It reads every production `.rs` under `crates/host/src` (excluding `*_tests.rs`, `tests.rs`, comment lines, and a module's `#[cfg(test)]\nmod tests` tail). It finds each `replay_candidate(` that is not the definition, and requires the last top-level argument to be exactly `REPLAY_LIMITS`, `fact_admission::REPLAY_LIMITS` or `crate::fact_admission::REPLAY_LIMITS`.
   - **Today** it finds 0 calls, and it asserts at most 1 (X7a's).
   - **The self-check** refuses `limits`, a struct update from `REPLAY_LIMITS`, `REPLAY_LIMITS_FOR_TESTS`, `my_REPLAY_LIMITS`, a wrapping call and a missing argument.
4. **The remedies in `doctor_ingress.rs`.** The shared failure envelope (`refused_envelope`) looks up a remedy by detail and refuses a detail without one, so without new arms the rows could not render. X12b added its two details the same way. The three details are new to host, and each is keyed by its one route here.
   - **If another route later uses `EVALUATION.INPUT_REFUSED`,** for example `external-specification` with another remedy, the lookup will need the row, not only the detail. That is the later owner's change.
   - **Rejected:** carrying the remedy in `InstallationTerminationV1`, which every 468 row shares.
5. **The bounds test.**
   - **How it measures.** It runs one lawful corpus case (`packet-0-original`, 23 objects and 46 blobs) under `REPLAY_LIMITS`, with one dimension changed at a time. For each of the nine dimensions, bisection over `[0, constant]` finds the least passing value. The case replays there, and at one less it is refused on the structural row, with `unavailable_evidence()` `None`.
   - **Measured needs:** walk 1736 steps, depth 36 and 27 861 descriptor work; owner 2241 steps, depth 3 and 27 861; 45 owner invocations; 69 capture entries; 392 373 retained bytes.
   - **The two capture needs** are also checked as exact counts: the supplied entries, and the replay's `retained_evidence().byte_length()`.
   - **Bisection** assumes each bound refuses only when exceeded, which the evaluator's counters do (checked decrement, depth comparison and cumulative byte sum). The pass at the found value and the refusal one below are asserted directly.
6. **The removal test uses the read set as "the claimed closure".**
   - **Which members.** A member is in the claimed closure if the full replay's `retained_evidence()` holds it (Grok's r3 review, "Item 8 wording"). Of `packet-0-original`'s 69 members, 68 are in that read set, and each removal is `evidence.missing` naming exactly the removed reference. One blob is ambient, and removing it still replays.
   - **Grok's r3 note** about `native_universe.rs`'s two `Ok(None)` arms holds: no read-set member was turned into absence.
7. **The corpus test** runs all 101 cases with `REPLAY_LIMITS`:
   - the lawful cases return the claimed RunId, equal to the fixture's expected `runId`;
   - every `mismatch` case is `Mismatch`, on the regeneration row with the claimed RunId;
   - the one `unavailable` case is `evidence.missing` with its digest.

   These are the corpus's own forged outputs. Each is re-identified, so only complete replay sees it, as item 8's "the corpus's forged cases" says. A raw one-byte edit of a blob would fail its digest instead (`Input(BlobDigest)`, the structural row), and the input test covers that.
8. **Parallel test execution.** Replay is pure, so the corpus, removal and bounds tests spread their replays over `available_parallelism` threads with `std::thread::scope`. They take no lock and create no file. The host lib's X5a tests take about 26 s in a debug build.
9. **The evaluator pin.** In the production part of `unavailable_evidence.rs` (before `#[cfg(test)]`, comment lines removed), it refuses `_ =>`, `_ |`, `| _`, `format!`, `{:?}`, `contains(`, `starts_with(` and `Debug)`. It also requires exactly one `#[derive(` and twenty-four `impl Find for`.

## Tests

New: 4 in the evaluator, 12 in the host lib, and 2 compile-fail cases.

**`unavailable_evidence.rs`, 4 tests:**
- `Some` at 18 nestings for each of an object and a blob: top level; the walk's `Graph`, native `Retention`, `Owner(Context)`, `Execution(View(Producer))`, `Run(Capability)`, `Syntax`, `Body`, `Plan`, `Policy`, `Stage`, `Predicate`, `Import` and `Payload`; the evaluation's `Reconstruction`, through `Structure`, `Record`, `Enumeration(Plan(Retention))` and `Parameters`;
- the reference spelling;
- `None` for 23 other refusals, including text that names a missing input;
- the no-wildcard, no-text pin.

**`fact_admission_tests.rs`, 12 tests:**
- every row and remedy, rendered through `failure_envelope`, valid against command-envelope v7, with no `run` member;
- the remedies byte for byte;
- the 101-case corpus;
- the corpus missing-blob case, reported under `Structure`, as `evidence.missing`;
- the removal test;
- schema and identity failures as `INPUT_REFUSED`: an altered Run descriptor, a read blob's bytes, and the Run's domain;
- the `REPLAY_LIMITS` values;
- the bounds test;
- capture entries at the constant itself (100 000 replays, and 100 001 is `Capture(Limit)`);
- the join pin: `replay_run` exactly once, the evaluator `use` line exact, one `.unavailable_evidence()`, no `ReplayedRun` construction, `run3:`, verdict, `check_plan_pack`, `admit_pack`, `derive_evaluation`, `inspect_`, `Clone`, `Default`, serde, custody, storage, platform, lifecycle, ledger, I/O, environment, process or `_ =>`;
- the `limits` pin and its self-check.

**Host driver:** 97 cases (2 new) and 8 self-tests.

## Checks

Product checks are at 933e78b plus this diff. Arch verifiers run against the real lock at 933e78b, which selects v122 with D2 bound.
- **Workspace runs:** two full runs of `cargo test --locked --offline --workspace --all-targets` on the final bytes, each with its own private 0700 TMPDIR: each with 1591 passed, 0 failed and 3 ignored, across 17 test binaries (1575 at adc9081, plus the 16 new unit tests). Two earlier runs at 96dd114 gave the same counts.
- **Lints:** `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` is clean.
- **Formatting:** `cargo fmt --all -- --check` is clean, and so is `rustfmt --edition 2024 --check crates/host/src/fact_admission_tests.rs` (an `include!`d file).
- **`check_package_edges --lane host`:** passes against v122 and against v123, with 20 declared and 20 resolved edges. No edge is new.
- **verify_scratch** (v123 appended in memory to the worktree's lock at 933e78b, with the inheritance replaced by the record's 55 folded rows): passes, with 83 inventory successors, 74 contract successors and 55 inheritance rows; v123 is selected.
- **verify_projection against the real lock:** 55 rows; 278 corruptions refused.
- **`build_v123.py`:** reruns produce the same bytes. 922 files; the 918 v122 rows are equal by value; 55 projection rows; 4 supersessions folded.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does X5a meet X5 r3 items 2, 4, 5, 5a to 5f, 8 and 9? In particular:
  - the accessor: exhaustive, no wildcard, no text;
  - step 1 before step 2;
  - the three routes and their members;
  - the RunId subject;
  - the remedies;
  - the `limits` pin;
  - `REPLAY_LIMITS` and the bounds test;
  - one `replay_run` call, and nothing minted;
  - no `check_plan_pack`;
  - `pub(crate)` throughout.
- Rule on calls 1 to 9.
- Do the two cases and their census rows meet X8 r3 for X5a?
- Is v123 right on v122, including the 55-row projection with D2's four supersessions folded?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `replay-join-x5a-inventory-v123-subject.json` (lead's value `0f45c8ce7cdac3e92ab55b065f4fc908e9f99478eb5dfa1325a76883192285c7`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v123, parent (the v122 pin), successorRecord (the pin of `replay-join-x5a-inventory-v123/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
