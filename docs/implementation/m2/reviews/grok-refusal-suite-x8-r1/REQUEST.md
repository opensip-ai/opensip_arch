Grok review: law X8 r1, the opaque API refusal suite (`crates/host/tests/admission_tests.rs`). Claude Opus 5.5 leads, and you are the single reviewer.

**Ground rules.**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok-refusal-suite-x8-r1`.
- This is a law review. Run no cargo in the product checkout.
- Product HEAD is `f1b8321`. The arch repo is `/Users/sb/code/opensip-ai/opensip_arch`.

**Subject.** `docs/implementation/m2/refusal-suite-x8/PROPOSAL.md` r1. The first row of `hashes.txt` pins it: sha256 `1fa3fa80fe3859115a05d5527c0de58ed96e879728d9a8670460d092a697c125`, 32723 bytes. The other rows pin the trial's evidence under `/tmp/opensip-x8-trial`.

## Context

- **EXIT-PLAN.md:**
  - the X8 row: "Raw DTOs, a boolean `verified`, forged receipts, a cloned or reused session, a private constructor and a serialized previous session all fail to compile. Behavioral rejection of altered inputs at the handoff";
  - "Choices left open by the design", the compile-fail harness bullet.
- **The build plan** `docs/v2/architecture/implementation-boundaries-and-build-plan.md`:
  - line 886 (the M2 row);
  - lines 591–613, especially 593–604 and 609;
  - line 1071 (the tooling matrix: trybuild versus isolated Cargo compile-fail fixtures, "fail for the intended reason");
  - line 1077 (what a trial must retain).
- **Accepted laws:**
  - X3d r6 (`commit-session-x3d/PROPOSAL.md`): items 1, 3, 4, 9, 10, 11 (X8's must-not-compile list), 12 (storage tests "only through crate-private, `cfg(test)` fixtures") and 13 (X3d-2 delivers "the X8 doctests");
  - X4 r7 (`live-guards-x4/PROPOSAL.md`): items 4, 6, 8 and 10;
  - X5 r2 (`replay-join-x5/PROPOSAL.md`);
  - X2 r8 (`project-root-x2/PROPOSAL.md`): item 7a, the handoff;
  - X7 r3 (`finalization-x7/PROPOSAL.md`): item 2 and item 10's X8 case.
- **Product at `f1b8321`:**
  - the 17 `compile_fail` doctests: `platform/src/work_ledger.rs` (10, 8 of them X3d-0's), `evaluator/src/{replay,policy,capabilities}.rs` (1 each) and `security/src/{installation_observation.rs,trust/native_read_session.rs}` (2 each);
  - `Cargo.lock` (no trybuild);
  - `README.md`'s lane `cargo test --locked --offline --workspace --all-targets`;
  - the `cfg(test)` seams `DurableWriteGate::for_tests` and `HomeSource::Fixture` (`security/src/custody/installation_admission.rs`), and X4T-0 (`security/src/trust/accepted_store_fixture.rs`);
  - the `pub(crate)` write chain in `security/src/custody/ordinary_writer.rs`.
- **Prior evidence:** `reviews/grok-settlement-reserve-x3d0-r1/REVIEW.md`, where the doctest reasons were checked by hand.

## The trial

The trial is in `/tmp/opensip-x8-trial`. You may re-run it. Cargo may run only inside `/tmp/opensip-x8-trial`, with `PATH=/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH` and `--locked --offline`.

- **The product copy.** `product/` is `git archive f1b8321`. It adds only `crates/host/tests/admission_tests.rs` (the trial driver), `tests/refusal/` (12 cases) and `tests/refusal-selftest/` (5 must-reject cases). To reproduce, run in `product/`:

  `cargo test --locked --offline -p opensip-host --test admission_tests -- --nocapture`

  The result is in `run1.log` (cold) and `run2.log` (warm).
- **`a/`** is the doctest probe crate: `cargo test --offline --doc`, recorded in `doctest-trial.log`.
- **`tb/`** is the trybuild offline resolution: `trybuild-offline.log`.
- **`standin/` and `cases/`** give the diagnostic shapes: `shapes.log`.

## Decide

1. **Item 1, the harness (lead decision).** Is the choice of isolated fixtures sound? The driver:
   - runs a nested `cargo check -p opensip-host` as the release surface;
   - compiles each case twice with the pinned rustc: a control that must compile, and a misuse that must produce exactly one error, with the annotated code (or `none`), the annotated fragment and the annotated line;
   - fails rather than skips when the toolchain pin or `CARGO` is missing;
   - has a self-test set and a census table.

   Check the trial's facts and the rejected alternatives: doctests, `RUSTC_BOOTSTRAP`, trybuild, a separate Cargo root, fixtures as workspace targets, and globbing rmeta. In particular, is the trial right that stable rustdoc ignores `compile_fail,E….` codes and that `--all-targets` runs no doctests? Is a nested cargo inside the test lane acceptable under the offline and locked rules?
2. **Item 2.** Fixtures supersede doctests as evidence, and the 17 doctests are ported and kept. Is this a lawful successor to X3d item 11's "pinned by `compile_fail` doctests" and X3d-2's "the X8 doctests", without reopening X3d?
3. **Item 3, the case table.**
   - Does it cover every category of lines 597–598 and line 1071, X3d item 11's list and X7 item 10's case?
   - Are the export rule (unnameable E0603/E0432 for crate-private types), the codes and the owner units right?
   - Is item 3b right? Rust visibility cannot confine security's adapter trait, `begin_journal_txn` or `seal_under_append_lock` to storage, so that part of X3d item 11 becomes a source pin, and a bypass still reaches no `PublishedCommit`. If there is a type-level way to confine them that the law missed, say so.
   - Are items 3c (X7a exports the projection) and 3d (`execution_id()`) sound?
4. **Item 4, the `scenario-fixtures` test feature (lead decision).**
   - Is it the right way to run behavioural cases outside security, given X3d's forbidden "production seam that supplies a `ProjectOperation`"?
   - Are its limits enough to keep it out of release builds? The limits are: it widens only existing gates, it constructs no authority type, it appears only in `[dev-dependencies]`, there is a source pin, and group J's E0432 holds on the plain surface.
   - Is the correction to X3d item 12 (storage tests cannot reach security's `cfg(test)` fixtures) right?
5. **Item 5, the behavioural cases B0 to B8.**
   - Are the expected rows and durable census right against X3d items 3, 4, 7 and 9, X4 items 4 and 8, and X5? Check in particular B3's REV and CLN, B4 before X6, and B6 and B7.
   - Do the cases meet lines 600–602 and 609?
   - Is it right to leave mid-`publish` alterations to X9's barrier points and X3d-1's tests, and timing to X4a?
6. **The units and dependencies:**
   - X8a, now;
   - the owner rows in X2e, X4a, X3d-1, X3d-2, X5a and X7a;
   - X8b, after X2e, X3a-1, X3b-3, X4a, X4T-0 and X3c-2, and before X3d-2;
   - X8c, after X8b, X3d-2 and X5a, plus X4T-b for B6 and B7.

   Are these right, and is the X3d r7 record-only note enough?
7. Is anything else wrong?

## Output

Write `REVIEW.md` and `review.json`. `review.json` must contain these top-level keys:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: an array, empty on ACCEPT;
- `"subjectSha256"`: `1fa3fa80fe3859115a05d5527c0de58ed96e879728d9a8670460d092a697c125`, the PROPOSAL.md sha256 in `hashes.txt`.

Do not commit.
