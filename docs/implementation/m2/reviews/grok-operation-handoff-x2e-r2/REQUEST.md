Grok review r2: X2e with X3b-3, the checked operation handoff (law X2 r8 item 7a) composed with the grant journal's floor step, carrier start and end step (law X3b r10 items 1, 3, 3a, 4, 11 and, new in r2, item 4 step 3 with item 13 through X3b-4), with inventory v111 (parent v108). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-operation-handoff-x2e-r2. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read or print the private 413 UUID fixture.

## What r2 answers

Your r1 (REQUIRED-FINDINGS, RF-1, inventory only) is in `reviews/grok-operation-handoff-x2e-r1/REVIEW.md` and `review.json`. You accepted all 13 judgment calls and the code. Since r1, product main has advanced twice: X4T-a2 + X4T-b (704251e, v106), then X3b-4 (97f630a, v108). The coordinator directed this order: wait for X3b-4, rebase onto it, join its rollover seam if usable, fix RF-1, and rebuild v111 on the then-selected parent.

So r2 has four parts:
1. **RF-1 (fixed).**
   - Both standing sentences now say "law X3b r10, unit X3b-3": v111's and successor.json's.
   - The `operation_handoff.rs` description cites "law X3b r10 items 1, 3, 3a and 4", and its end-path sentence says: "the end step is then not entered when the owner reports an uncertain journal outcome or when the attempt ledger is closed (law X3b r10 item 4): ProjectOperation::end returns NotEntered, with no fence walk, read or copy and nothing disclosed; otherwise …".
   - The `carrier_operation.rs` description cites "law X3b r10 items 1, 3, 3a, 4 and 11".
   - The builder literals emit exactly these (`evidence/build_v111.py`), and neither v111 nor successor.json contains "X3b r9".
   - Inherited rows stay by value: 793 v108 rows, 0 differing.
   - Beyond the finding: `operation_handoff_tests.rs`'s description said "a closed attempt ledger refusing the end step before the walk", which described r9-literal behaviour. It now says "not entering the end step (no walk while the fence is held elsewhere, no copy, nothing disclosed), and the next writer's floor step copying forward".
2. **The rebase onto 97f630a.** Two conflicts, each resolved by keeping both sides:
   - **`journal_store.rs`:** X4T-b's `publish_private_file` re-export (with its comment) is kept unchanged, then a blank line, then X2e's re-export block. The blank line keeps rustfmt from pulling upstream's line away from its comment into X2e's group.
   - **`journal_store/carrier_floor.rs`:** X3b-4's `#[path = "carrier_rollover.rs"] mod rollover;` is kept, followed by X2e's `operation` module declaration.

   X3b-4 changed the carrier internals X3b-3 composes through: `EndInput::Uncertain` became a unit variant, the r9 reconciliation API was removed, and `seal_fits` and the rollover were added. Every X3b-3 call site was already compatible, because `operation_end_copy` passes only `EndInput::Certain` and nothing used the removed API. `carrier_start.rs`, `carrier_append.rs` and `carrier_rollover.rs` are not edited.
3. **The X3b-4 rollover seam is now joined.** This is new code, so please review it as such.
   - **`carrier_operation.rs`:**
     - adds `operation_end_after_exhaustion(location, exhaustion, released_operation_ref, work) -> ExhaustedEnd`, a pass-through to X3b-4's `end_step_after_exhaustion` (item 4 step 3, then steps 4 and 5);
     - re-exports `CapacityExhaustion`, `ExhaustedEnd` and `RolloverOutcome`;
     - adds a `cfg(test)` `plant_committed_tail_for_tests`, which plants a committed `RA` at (1, seq) by X3b-2's reserved-slot technique (the trigger lifted and reinstalled from its own stored SQL) and writes the witness `COMMITTED` there. It is test support for the composition owner and never in a release build.
   - **`operation_handoff.rs`:**
     - `JournalOutcome` gains `Exhausted { exhaustion: CapacityExhaustion, operation_ref: String }`. It is X3d's `CarrierCapacityExhausted` for an operation whose journal outcomes were all certain, together with the released operation's `operationRef`. `JournalOutcome` is no longer `Copy`.
     - The end path is unchanged through the retaken fence, the I identity check and the rebinds. Then, for `Exhausted`, it calls `operation_end_after_exhaustion` in place of `operation_end_copy`, and the fence is released afterwards as before.
     - `OperationEnd` gains `RolledOver { rollover: RolloverOutcome, end: Result<EndOutcome, EndFailure> }`. The rollover outcome is kept whatever the copy or the unlock returned, and is disclosed on its own row (X7 r3 item 6). The copy's failure is mapped through the same `EndRefusal::Carrier`, and an unlock failure becomes `EndRefusal::Release`.
     - `NotEntered` still comes first: an uncertain outcome or a closed attempt ledger never reaches the rollover (X3b r10 item 4).
     - The rollover charges the same attempt ledger, inside `receipt.charge`, as X3b r10 item 9 requires; no other ledger is opened.
   - Judgment call 8's rollover seam is therefore closed. `OperationGuard` and X4a's monitor at the lease-free point remain commented seams.
4. **The inventory rebuilt on v108.** v108 is 376570 bytes, sha256 `9c6953f28572f6882bbdc71ae945104e4a4e65e5d7b87cae9cf91318d9eb1f44`, with successor record `journal-rollover-x3b4-inventory-v108/successor.json` (20206 bytes, sha256 `173239c56f31870c59d617e25fbb5ea0e151f5924148b81e21b85ac3ee30ee29`).
   - The builder's parent map is v108. The two production descriptions and the handoff test description now describe the rollover join.
   - verify_projection's comment names v108. `verify_scratch.py` now finds the arch root from its own location.
   - The README states the r2 history and the parent chain v110, v112, v106, v108, then v111.

## Law

All in arch `docs/implementation/m2/`, accepted:
- `project-root-x2/PROPOSAL.md` r8 item 7a, item 7's ordering note, and items 8, 9 and 10;
- `journal-x3b/PROPOSAL.md` r10 items 1, 2, 3, 3a, 4 (with step 3), 9, 11, 12 and 13;
- `store-admission-x3a/PROPOSAL.md` r5 items 1 and 2;
- `live-guards-x4/PROPOSAL.md` r7 items 2 and 6;
- `trust-admission-x4t/PROPOSAL.md` r9 items 7 and 9;
- `commit-session-x3d/PROPOSAL.md` r6 items 1, 2, 3 (step 3's `CarrierCapacityExhausted`), 7 and 8;
- X7 r3 item 6 (rollover disclosure).

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x2e`, detached at 97f630a. That is main with X3b-4 integrated; the lock selects v108. Save `git -C <worktree> diff` (the four new files are intent-to-add) as product.diff and report its sha256. Lead's value: `0633ba9ee43d0d6d2b838c046da6d001c99c031fba310b47bbe98ad7489532fd`, 103468 bytes; 14 files, 2105 insertions, 26 deletions. Your r1 product.diff is in `/tmp/opensip-implementation/reviews/grok-operation-handoff-x2e-r1/product.diff` (sha256 `7992c1a0…2d2c6`).
  - **Against r1, the added and removed lines differ in four files only:**
    - `operation_handoff.rs`: the rollover join and the header comment;
    - `operation_handoff_tests.rs`: one new test;
    - `carrier_operation.rs`: the pass-through, re-exports and test helper;
    - `journal_store.rs`: the new re-exports and the resolution placement.
  - **Pin changes in the other files.** `installation_admission.rs`, `installation_session.rs` and `carrier_floor.rs` have new pins only because of upstream base changes (X4T-b, X3b-4) and the resolution. Every other file is byte-identical to r1.
- **Arch:** v111 (parent v108), `operation-handoff-x2e-inventory-v111-subject.json` and `operation-handoff-x2e-inventory-v111/`. All are untracked until acceptance, and v111's r1 bytes are superseded.

## Judgment calls for r2: please rule

14. **The rollover seam's input.** The exhaustion comes in through the owner's report (`JournalOutcome::Exhausted`), as X3b r10 item 12 says ("X3b-3 also threads the exhaustion from X3d's `finish` into the end step's step 3"). The handoff does not detect it.
    - The released `operationRef` comes with it, because item 13 forbids the `TERMINAL` token from equalling it, and only X3d's session knows it.
    - **Rejected:** reading the carrier tail at end to decide exhaustion. That is X3d's `prepare_commit` decision (`seal_fits`), and the end step must not re-derive it.
15. **One result type for both outcomes.** After `Exhausted`, the end path returns `RolledOver` with both the rollover's outcome and the copy's result, mirroring X3b-4's `ExhaustedEnd`. A rebind or fence failure before the rollover is still `Failed` and runs no rollover.
    - The fence is released after the rollover whatever it returned. The rollover returns with no project lock held (X3b-4).
    - An unlock failure after a rollover is reported in `end` and does not hide the rollover outcome.
16. **Resolution placement.** In journal_store.rs the upstream line is kept in place with its comment, and in carrier_floor.rs X3b-4's `rollover` declaration comes before X2e's `operation`. No upstream line is changed.
17. **Test-only planting helper in the journal half.** The composition test needs an exhausted tail in a real namespace carrier. Witness encoding and the trigger lift are journal_store-private, so the helper lives there under `cfg(test)`, re-exported only under `cfg(all(test, target_os = "macos"))`.

## Tests

There are 17 new tests: r1's 16, plus `an_exhausted_generation_rolls_over_under_the_retaken_fence_then_copies_the_floor`. That test runs three operations on one project:
- a first operation creates the carrier;
- an `RA` is planted at tail 9007199254740990 (no `SEAL` fits);
- the next operation's floor step copies the floor to that tail, and its start tail is that tail. Its `end(Exhausted{1, …990})` returns `RolledOver { Rolled { closed: (1, …991), opened: 2 }, end: Ok(CopiedForward) }`;
- the witness is `COMMITTED (2, 0)`, the floor is (2, 0, null), and the fence and leases are free;
- a third operation starts at (2, 0, None).

## Checks

- At 97f630a plus this diff, two full workspace runs: 1476 passed, 0 failed, 3 ignored, both times.
- `cargo clippy --workspace --all-targets --offline --locked -- -D warnings` is clean, and so is `cargo fmt --all -- --check`.
- `rustfmt --check --edition 2024` (for the `include!`d custody files):
  - clean on operation_handoff.rs, operation_handoff_tests.rs, first_registration.rs, first_registration_tests.rs and namespace_lease.rs;
  - ordinary_writer.rs, installation_admission.rs, installation_session.rs and read_premise.rs are at exactly their base deltas (2, 15, 9 and 1).
- `check_package_edges --lane host` against v111 passes: 19 declared and 19 resolved edges, and no new edge.
- verify_scratch (v111 appended over the real lock at 97f630a) passes: 76 inventory successors, 72 contract successors, 16 inheritance rows, v111 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v111.py` reruns produce the same bytes.
- `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Is RF-1 fixed: both standing sentences and both production descriptions name law X3b r10, the handoff description states the closed-ledger bar, and the builder literals match?
- Is the rebase resolution correct, with no upstream line changed?
- Does the rollover join compose X3b r10 item 4 step 3 and item 13 exactly? In particular:
  - only after certain outcomes on an open attempt ledger;
  - under the retaken fence with no project lock;
  - on the attempt ledger;
  - the copy after the rollover;
  - the rollover outcome kept for disclosure;
  - nothing after an uncertain outcome.
- Rule on judgment calls 14 to 17.
- Is v111 right on v108?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `operation-handoff-x2e-inventory-v111-subject.json` (lead's value `5f61aaa10129454dd6fd705eeef4cbfd443f2d7cca1e70fc5ced44384349c498`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v111, parent (the v108 pin), successorRecord (the pin of `operation-handoff-x2e-inventory-v111/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
