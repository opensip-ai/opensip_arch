# The opaque API refusal suite — proposal X8 r4

2026-10-02. Claude Opus 5.5, implementation lead. Law for unit X8 of `EXIT-PLAN.md`. It is written under:
- the build plan's M2 row (`implementation-boundaries-and-build-plan.md` line 886: "Opaque API refusal tests … pass; synthetic fixtures remain labelled, not compiler qualification");
- its required checks (lines 591–613): `crates/host/tests/admission_tests.rs` "owns public-boundary scenarios", and "private evaluator/security unit tests own prerequisite construction" (lines 593–595); the compile-fail and behavioural checks of lines 597–604; and F01's line 609;
- its tooling matrix row (line 1071), which leaves "trybuild versus isolated Cargo compile-fail fixtures" to a trial, requires that misuse "fail for the intended reason", and asks that each trial retain "the exact input set, candidate/tool version, configuration, observed failures and accepted limitations" (line 1077);
- the offline build rule: every lane builds with `--locked --offline` from provisioned archives (product `README.md`, `tools/README.md`);
- the accepted laws X3d r6 (items 1, 3, 4, 10, 11, 12 and 13), X4 r7 (items 2, 4, 6, 8 and 10), X5 r2, X2 r8 (item 7a), X7 r3 (items 2 and 10) and X9 r1 (`crash-matrix-x9/PROPOSAL.md`: items 2, 3, 6, 11 and 12, and gap G1), and X4T r4's `cfg(test)` store generator (X4T-0).

**r2 (2026-10-02) answers Grok X8 r1 RF-1 and RF-2.** r1 bytes are preserved in PROPOSAL-r1.md.
- **RF-1: one shared gate predicate (item 4b).** Accepted X9 r1 item 6 already widens the same fixture gates to `cfg(any(test, feature = "crash-matrix"))`, and X9-1 pins them. A Rust item has one cfg predicate. So both laws now use one site list, X9-1's pin, extended by name. Each shared site is written `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`. The two features stay separate, and so do their support modules. X8 records the joint predicate as the wording change to X9 item 6 and to X9's matching forbidden substitute. X9's accepted outcome stands. Items 4b, 4c, 4f and 4g, the units and the forbidden substitutes change to match.
- **RF-2: B6 and B7 publish through X9 item 6's fenced helper, in a process that does not hold the operation lease (item 5a).** X4 item 2 forbids trust writes under a lease. r1's `publish_revocation` on the lease-holding test thread is withdrawn. The test thread waits for the helper process to exit, then calls `prepare_commit` and `publish`, with no sleep. B3 and B5 stay on the test thread.
- **Unchanged from r1:** everything else, including items 1 to 3, B0 to B5 and B8, and item 6.

**r3 (2026-10-02) answers Grok X8 r2 RF-1: the helper process exited 0 without publishing.** r2 bytes are preserved in PROPOSAL-r2.md. r3 ACCEPTED by Grok on 2026-10-02.
- **The defect.** r2 item 5a re-executed the test binary with `--exact` on an `#[ignore]`d test and no `--ignored` or `--include-ignored`. On rustc 1.95.0 the harness then prints "ignored" and exits 0, so the waited success was a process that published nothing. Separately, the entry could not reach the publisher: X9 item 6 places its helper in `crash_matrix_support`, which exists only under `crash-matrix`, and r2 named no `scenario` function to replace the withdrawn `publish_revocation`.
- **The change (items 4b, 4c and 5a, and the forbidden substitutes).**
  - The entry is an ordinary `#[test]` in X9 item 3's shape. It returns at once unless its helper environment variable is set, and it publishes only when it is.
  - It calls `scenario::publish_revocation_fenced`, which runs the shared fenced publisher. X9-1 places that publisher on item 4b's joint-predicate site list, so it compiles under `scenario-fixtures` alone, with `crash-matrix` off.
  - Two self-checks make a no-op exit fail the case: the helper's tagged `published` record, and a strictly advanced revocation version read before and after.
- **Unchanged from r2:** everything else.

**r4 (2026-10-04) is record-only.** r3 bytes are preserved in PROPOSAL-r3.md. It records one ordering that was already accepted elsewhere. It changes no item, trial result, case, group, code, fragment rule, feature, module, behavioural case, unit scope or dependency, or forbidden substitute of r3, and no accepted outcome of another law. The one r3 sentence it touches stays in place, followed by a short "r4 (record)" note that points here.
- **The source.** The record was asked for by Grok's review of X3d r7 (`reviews/grok-record-x3d-r7-x7-r6-x9-r3/REVIEW.md`, "X8's own record"), and noted in `EXIT-PLAN.md` as "X8 record note owed (2026-10-04)". The ordering itself is a lead decision accepted in the X3d-2 review (`reviews/grok-commit-facade-x3d2-r1`, call 1), recorded in `EXIT-PLAN.md` ("X3d-2 ordering and follow-ups (2026-10-03)") and in X3d r7 ("Ordering: X3d-2 before X8b and X9-1").
- **The overtaken sentence.** "Units after the law" says X8b "Lands before X3d-2, whose storage tests use it (item 4g)." X3d-2 integrated first, at product `adc9081`, before X9-1 (`a36da7c`) and before X8b was built.
  - **X3d-2's storage tests take no `ProjectOperation`.** They run the storage functions that `prepare_commit` and `publish` compose, on a scratch `I/stores/S`, with a real replay and no session (X3d r7). So no X3d-2 test needed this feature, and no requirement of X3d-2 is left unmet.
  - **The first end-to-end test.** `prepare_commit` and `publish` with a real `CommitSession` are first tested together by X8c's B0 to B4, then by X9-2's matrix (X3d r7; X3d-2 review, call 1).
- **What stands.**
  - **Item 4g.** It stands as the arrangement for any storage test that needs a `ProjectOperation` in the ordinary lane: it obtains one through `scenario-fixtures` as a dev-dependency, never through crate-private `cfg(test)` fixtures or a production seam.
  - **X8b's dependencies.** X9-1, X2e, X3a-1, X3b-3, X4a, X4T-0 and X3c-2 stand. X3d-2 was never one of them.
  - **X8c's dependencies.** X8b, X3d-2 (and so X3d-1, X4a and X3c-2) and X5a stand, with B6 and B7's further needs.
- **Unchanged from r3:** everything else.

Every decision here is a lead decision, made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Product baseline: `f1b8321` (X3d-0 integrated). Not code. X8 adds no public code, row or detail.

## Problem

M2 completes only when "opaque API refusal tests" pass. Four things are missing.

1. **No harness.** The product has 17 rustdoc `compile_fail` doctests: 10 in `platform/src/work_ledger.rs` (8 of them X3d-0's), one each in `evaluator/src/replay.rs`, `policy.rs` (X12a) and `capabilities.rs`, and two each in `security/src/installation_observation.rs` and `security/src/trust/native_read_session.rs`. A `compile_fail` doctest passes on any compile error, so none of them pins why it fails. X3d-0's reviewer checked each reason by compiling the snippets by hand (`grok-settlement-reserve-x3d0-r1/REVIEW.md`). That check is not repeatable.
2. **The trial.** The tooling matrix asks for one, and X3d item 11 and X7 item 10 assume an answer: X3d says "pinned by `compile_fail` doctests", and X3d-2 delivers "the X8 doctests".
3. **No behavioural home.** Lines 600–602 require altering an admitted input, inventory, namespace, execution or generation at the handoff, with no acknowledged authority resulting. No current crate can run that end to end:
   - the X1–X2e write chain is `pub(crate)` in security;
   - its test seams (`DurableWriteGate::for_tests`, `HomeSource::Fixture`, X4T-0's signed store) are `cfg(test)` in security;
   - so neither storage's tests nor host's integration tests can build a `ProjectOperation`.

   X3d item 12 says storage's tests build one "only through crate-private, `cfg(test)` fixtures". Across a crate boundary that cannot be done.
4. **One case Rust cannot refuse at compile time.** X3d item 11 lists "passing a caller-implemented adapter … to storage's facade". The adapter trait is security's, and storage implements it. A public trait can be implemented, and a public function called, by every crate that depends on security, host included. Rust visibility cannot confine a trait's implementations, or a function's callers, to one sibling crate.

## The trial (tooling matrix line 1071)

**Inputs.**
- Toolchain: rustc 1.95.0 (59807616e 2026-04-14) and cargo 1.95.0 (f2d3ce0bd 2026-03-21), from the pinned Homebrew cellar.
- Product: `f1b8321`, exported read-only with `git archive` to `/tmp/opensip-x8-trial/product`.
- Configuration: all builds `--locked --offline`.

The trial driver is `/tmp/opensip-x8-trial/product/crates/host/tests/admission_tests.rs`. It has 12 cases in `tests/refusal/` and 5 must-reject cases in `tests/refusal-selftest/`. The logs are `run1.log`, `run2.log`, `doctest-trial.log`, `trybuild-offline.log` and `shapes.log` in `/tmp/opensip-x8-trial`; the doctest probe crate is `/tmp/opensip-x8-trial/a`. No repository was edited.

**Observed.**
1. **Stable rustdoc does not check error codes.** A doctest marked `compile_fail,E0599` whose snippet fails with E0451 passes. So does a `compile_fail` snippet that fails only on a typo in a path (`doctest-trial.log`). The `,E0505` and `,E0515` annotations in `native_read_session.rs` and `installation_observation.rs` are therefore documentation, not checks. Codes are enforced only behind the nightly gate (`RUSTC_BOOTSTRAP=1`), and even then a snippet without a code passes on any error.
2. **The documented lane never runs doctests.** The README lane is `cargo test --locked --offline --workspace --all-targets`. `--all-targets` means `--lib --bins --tests --benches --examples`, and doctests are not among them. The trial confirmed this. Today the 17 doctests run only when someone runs `cargo test --doc` or `cargo test` without `--all-targets`.
3. **trybuild cannot be resolved.** It is not in `Cargo.lock` (61 packages) or in the provisioned registry cache. `cargo generate-lockfile --offline` for a manifest naming `trybuild = "1"` fails with exit 101 (`trybuild-offline.log`). Adopting it would add a dependency selection: trybuild plus `glob`, `target-triple` and `termcolor`, with their archives, licences and policy rows.
4. **An isolated-fixture driver works inside the existing lane.** The driver runs inside `cargo test -p opensip-host --test admission_tests`. It starts a nested `cargo check --locked --offline -p opensip-host --message-format=json` into `CARGO_TARGET_TMPDIR`, takes the `.rmeta` path of every `opensip_*` library and `serde_json` from cargo's `compiler-artifact` messages, and compiles each fixture twice with the pinned `rustc --error-format=json`.
   - **Timing:** a cold surface check takes 17.5 s; warm, 0.05 s. All 17 cases take 0.86 s.
   - **No deadlock** with the outer cargo, because the target directory is separate. trybuild uses the same nested-cargo pattern.
5. **The driver separates intended from unintended failures.** All 12 cases passed. All 5 must-reject cases were rejected:
   - a typo (E0422 instead of the intended reason);
   - an extra, unrelated error;
   - the right error on the wrong line;
   - a vacuous case: `.clone()` on `&ReplayedRun` compiles, because references are `Clone`;
   - a control that does not compile.
6. **Diagnostic shapes on 1.95.0.** Some were measured on product types, and the sealed-trait, private-function, arity and `verified` shapes on the stand-in crate `/tmp/opensip-x8-trial/standin` (`shapes.log`).
   - A struct literal naming every private field: E0451.
   - A partial or empty literal: no code, with the message "cannot construct `T` with struct literal syntax due to private fields".
   - A trait-bound probe for `Clone`, `Copy`, `Default` or `Deserialize`: E0277, "the trait bound `T: Clone` is not satisfied".
   - A sealed-trait impl outside the crate: E0277 on the private supertrait.
   - A private associated function: E0624.
   - A private module: E0603.
   - An unresolved import: E0432.
   - Use after move: E0382.
   - A wrong argument type: E0308.
   - A literal naming a field the type does not have, such as `verified`: E0560, as the only error.
   - A wrong arity: E0061.

   The existing `AdmittedPack` and `CapabilityManifest` literals fail with E0451, the intended reason.

**Accepted limitations.** Message fragments are rustc's English text. They are stable under the pinned toolchain, but a re-pin can change them (item 1d). The driver checks the public surface of a plain `cargo check`. It does not check other targets or platforms.

## Decisions

1. **The harness: isolated compile-fail fixtures, driven from `admission_tests.rs` by the pinned toolchain (lead decision; settles line 1071).**
   a. **Where it lives.** Each case is one Rust file under `crates/host/tests/refusal/cases/`, and each driver self-test under `crates/host/tests/refusal/selftest/`. No fixture is named `main.rs`, so Cargo never discovers one as a target. One `#[test]` in `crates/host/tests/admission_tests.rs` drives all of them. A single test means no two nested builds race on one target directory.
   b. **The surface.** The driver runs `$CARGO check --locked --offline -p opensip-host --message-format=json`, with `--manifest-path` set to the workspace root and `--target-dir` set to `CARGO_TARGET_TMPDIR/x8-surface`. It takes the `.rmeta` of each `opensip_*` library and of `serde_json` from the `compiler-artifact` messages; a duplicate name fails.
      - This is the release public surface: no `cfg(test)`, no dev-dependencies and no features. A `cfg(test)` constructor is absent there exactly as it is in a release build.
      - Fixtures may name only those crates. Transitive crates resolve through `-L dependency=`.
   c. **One case, two compilations.** Each case is compiled with the same rustc, `--edition 2024 --crate-type lib --emit=metadata --error-format=json --cap-lints allow`:
      - once as the **control**, without `--cfg x8_misuse`, which must produce no error diagnostic;
      - once as the **misuse**, with `--cfg x8_misuse`.

      The misuse line and its lawful twin differ only under that `cfg`. The case passes only if all of these hold:
      - the misuse produces exactly one error diagnostic, not counting rustc's "aborting due to" summary;
      - its `code` equals the annotation's code, or is absent where the annotation says `none`;
      - its message contains the annotation's fragment;
      - one of its primary spans starts on the annotated line.

      The annotation is `//~ ERROR <code|none> "<fragment>"`. There is exactly one per case. `none` is allowed only where rustc 1.95.0 emits no code for the intended error; today that is the partial or empty private-field literal.

      This pins the reason in four independent ways, and the compiling control proves that nothing else in the file is broken. A doctest pins none of them.
   d. **Toolchain identity.** The driver reads `RUSTC`, or else `rustc`, and requires `rustc -vV` to report `release: 1.95.0`, the `rust-toolchain.toml` pin. It requires `CARGO` to be set.
      - A missing or different toolchain fails the test; it never skips.
      - A re-pin must update the pinned release in the same reviewed unit that re-checks every fragment and code.
      - An `.rmeta` from another compiler fails as E0514, which is never an intended reason.
   e. **Self-test.** The selftest directory holds at least the trial's five must-reject shapes: a wrong reason, an extra error, a wrong line, a vacuous misuse and a broken control. The driver fails if any of them passes. This shows that the driver can tell intended from unintended failures, not only that the cases fail.
   f. **Census.** `admission_tests.rs` holds the case table of item 3, as `(file, owning crate, type, unit, category)`.
      - The driver fails if the `cases/` listing differs from the table.
      - It fails if any category of lines 597–598 and line 1071 has no case. The categories are raw DTO, boolean `verified`, structural-only input, serialized previous session, forged receipt, cloned or reused session, and private constructor.
   g. **The lane.** It is an integration test, so it runs in the documented `cargo test --locked --offline --workspace --all-targets`. No new tool, dependency, lock file, Cargo root or lane is added. The test writes only under `CARGO_TARGET_TMPDIR`.

   **Rejected:**
   - **`compile_fail` doctests as the evidence** (EXIT-PLAN's "extending the rustdoc doctests"). Trial items 1 and 2: stable rustdoc accepts any error, ignores the code annotation, and the documented lane never runs doctests.
   - **`RUSTC_BOOTSTRAP=1`** to enable code checks. It is a nightly gate on a pinned stable toolchain, and code-less cases would still pass on any error.
   - **trybuild.** It cannot be resolved offline (trial item 3), and it needs a new dependency selection. It compares normalized rendered stderr, so every rustc message change rewrites every expectation. It asserts text, not code, line and a single error, and it has no lawful control. It also drives a nested cargo, as this driver does, so it adds no precision.
   - **Fixture crates with their own Cargo root.** These need a second lock kept equal to the workspace lock, an `exclude` entry, and a manifest per case. They add no precision over rustc on the surface `.rmeta`.
   - **Fixtures as workspace targets** (examples or bins). `--all-targets` and `clippy --all-targets` would build, and fail on, every misuse.
   - **Locating `.rmeta` files by globbing `target/debug/deps`.** Stale hashes make that ambiguous. Cargo's own artifact messages are exact.

2. **What becomes of `compile_fail` doctests (lead decision; succeeds X3d r6 item 11's "pinned by `compile_fail` doctests" and X3d-2's "the X8 doctests").**
   - X8's fixtures are the pinned evidence for every must-not-compile case in X3d item 11, X7 item 10 and item 3 below.
   - X3d-1, X3d-2, X5a and X7a add their cases as X8 fixtures, not doctests. A doctest may still illustrate a type, but it is never cited as evidence.
   - The 17 existing doctests stay unchanged as documentation; removing reviewed lines buys nothing. Their cases are ported to fixtures in X8a (item 3, group L), so their reasons are pinned for the first time.
   - **Rejected:** deleting the doctests, which is churn on accepted bytes; and leaving their reasons hand-checked.

3. **The case list.** Each row is one fixture, or one fixture per listed type. "Unit" is the unit that adds the fixture, together with the type it pins.

   **The export rule.** The owner unit declares whether each type is exported, and the table records it.
   - **An exported type** gets the full capability set: literal, `Default`, `Clone`, `Deserialize`, `Serialize` and reuse.
   - **A type the owner keeps crate-private** gets one unnameable case instead: E0603 (private item or module) or E0432 (unresolved), on its path. Being unnameable is the stronger refusal.

   **Codes.** Codes are fixed here. Fragments name the type and trait, and the unit fixes their exact text.

   | Group | Case (misuse line) | Owning type and crate | Expected | Unit |
   |---|---|---|---|---|
   | A raw DTO | `storage::prepare_commit(raw, session)` with `opensip_identity::JsonValue` holding a Run | `ReplayedRun` (evaluator) at `prepare_commit` (storage) | E0308 | X3d-2 |
   | A | the same, with the generated contracts Run record | same | E0308 | X3d-2 |
   | A | the authoritative projection given a `JsonValue` | X7's projection (host) | E0308 | X7a |
   | B boolean `verified` | `prepare_commit(true, session)` | `ReplayedRun` at `prepare_commit` | E0308 | X3d-2 |
   | B | the authoritative projection given `true`, a RunId `&str` or `&ReplayedRun` | X7's projection | E0308 each | X7a |
   | B | `PublishedCommit { verified: true }` | `PublishedCommit` (storage) | E0560 "has no field named `verified`" | X3d-2 |
   | C structural-only | `prepare_commit(&retained_inputs, session)`, an inert `RetainedInputs` | `ReplayedRun` at `prepare_commit` | E0308 | X3d-2 |
   | D forged receipt | a partial literal; a `Default` probe; `serde_json::from_str::<T>` | `CommitSession`, `JournalWriteTxn`, `JournalSealBinding`, `StoppedSession` (security); `PreparedCommit`, `PublishedCommit` (storage); `ProjectOperation` (security) | none "struct literal syntax due to private fields"; E0277 "`T: Default`"; E0277 "`T: serde::Deserialize`" | X3d-1, X3d-2, X2e |
   | D | unnameable | `AdmissionPermit`, `FinalGate`, `OperationGuard` (security, crate-private per X3d item 4 step 3.9 and X4 item 6) | E0603 | X4a |
   | E cloned or reused | a `Clone` probe on every type in row D | same | E0277 "`T: Clone`" | X3d-1, X3d-2, X2e |
   | E | `CommitSession::open(op)` twice; `prepare_commit` with a consumed session; `publish` twice; `finish` twice; a `ReplayedRun` passed to a second `prepare_commit` | `ProjectOperation`, `CommitSession`, `PreparedCommit`, `StoppedSession`, `ReplayedRun` | E0382 each | X2e/X3d-1, X3d-2, X5 r2 item 3 |
   | F private constructor | each non-public or `cfg(test)` constructor of a row D type, found by item 3a's census | as listed | E0624 if private; E0599 "no function or associated item named" if absent outside `cfg(test)`; E0603 if the type is unnameable | the type's unit |
   | F | `CommitSession::open(op, execution_id)`: no caller-chosen ExecutionId | `CommitSession` | E0061 | X3d-1 |
   | G serialized previous session | `serde_json::to_string(&x)` | every row D type that is exported | E0277 "`T: Serialize`" | X3d-1, X3d-2, X2e |
   | H external adapter | `prepared.publish(adapter)`; `prepare_commit(run, session, outcome)` | storage's facade (X3d item 1) | E0061 each | X3d-2 |
   | I storage internals | `use opensip_storage::ledger_store` (where `stage_recovery_pair` and the SQL connection live) | storage | E0603 | X8a |
   | J test seam | `use opensip_security::scenario` | item 4's module | E0432 | X8b |
   | K replay | an empty literal; a `Deserialize` probe; `JsonValue` and `true` in place of `ReplayedRun` | `ReplayedRun` (evaluator) | none "…private fields"; E0277; E0308; E0308 | X8a |
   | L ported doctests | every existing doctest's misuse, with a lawful control. `SettlementReserve`: clone, re-`settle`, `Default`, literal, both methods on `WorkScope` and on `ReservedPostchecks`. `WorkScope`: replacement and swap. `ReplayedRun`, `AdmittedPack` and `CapabilityManifest` literals. `NativeTrustReadSession` and the installation-observation fence: the use-after-drop and escape cases | platform, evaluator, security | E0599, E0382, E0277, E0451, E0505, E0515 and the rest, as each misuse yields on 1.95.0 | X8a |

   a. **Constructor census (row F).** The unit that adds a row D type lists, in the case table, every inherent function or associated constant of that type, and every `cfg(test)` item that returns it, that is not public in a release build. Each one gets a case.
      - Today's known members, all on crate-private types: `DurableWriteGate::for_tests`, `HomeSource::Fixture`, `InitialInstallationAttempt::for_tests`, `ObservationSession::for_tests`, `CarrierLocation::for_tests`, `AclOmissionPremise::for_tests`, X4T-0's `accepted_store_fixture`, and X4's abstract test lock.
      - Each of these is pinned either by its type's unnameable case or by its own case.
   b. **The adapter (X3d item 11, correction).** Group H pins storage's facade: it takes no adapter and no `SealOutcome`.
      - **What compile-fail cannot pin.** It cannot pin that security's adapter trait, `begin_journal_txn` and `seal_under_append_lock` are used only by storage (Problem 4). The rest of X3d item 11's list stands as compile-fail cases.
      - **A source pin instead.** It lives in `admission_tests.rs` and is added by X3d-2. In production code under `crates/*/src`, those three names may appear only in security's defining module and in `crates/storage/src/commit.rs`. A use anywhere else fails.
      - **What a bypass could reach.** A caller that went around the pin could reach at most a durable SEAL without an evidence commit (F36 and F38's recoverable state). It still could not reach authority: only storage can construct `PublishedCommit` (row D), and only a `PublishedCommit` sets an authoritative label (X7 item 2).
      - **Rejected:** claiming it as compile-fail, which would be a fixture that cannot pass.
   c. **X7's projection.** X7a exports the authoritative projection, so that its signature can be pinned from outside. It is inert: it consumes only `&PublishedCommit`, which no caller can forge. X7 r3 does not fix its visibility, so no amendment is needed.
   d. **ExecutionId reader.** X3d-1 gives `CommitSession` a read-only `execution_id()`. Item 5's B4 needs it. It returns the drawn identifier and admits nothing.

4. **The test seam for behavioural cases: one test-only Cargo feature (lead decision).**
   a. **The feature.** `opensip-security` declares `scenario-fixtures = []`. `opensip-storage` declares `scenario-fixtures = ["opensip-security/scenario-fixtures"]`. Storage's and host's `[dev-dependencies]` enable it, and nothing else does. Under it, security compiles one `#[doc(hidden)] pub mod scenario`, and storage one `#[doc(hidden)] pub mod scenario`.
   b. **One shared site list and one joint predicate (r2, RF-1).** `scenario` uses the fixture gates that X9 r1 item 6 already widens for `crash_matrix_support`. A Rust item has only one cfg predicate, so the two laws share one list.
      - **The list is X9-1's pin, extended by name.** There is no second list. At X9 r1 the shared sites are:
        - `Image::Injected` in `security/src/trust/initial_core.rs`;
        - `HomeSource::Fixture` and its match arm in `admit_with` (`security/src/custody/installation_admission.rs`);
        - X4T-0 (`security/src/trust/accepted_store_fixture.rs` and its module declaration);
        - the fenced `state.v1` publisher of X9 item 6 (item 5a). X9-1 places it on this list under the joint predicate (r3). It is a function beside the trust owner's publication code, not an item of `crash_matrix_support`. `crash_matrix_support`'s helper and `scenario::publish_revocation_fenced` (item 4c) are both thin callers of it.
      - **The predicate.** Each shared site is written `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`, and nothing else.
      - **What goes on the list.** A site goes on the list only if both support surfaces call it.
        - X9's barrier and fault sites stay `cfg(test)` with X9's points beside them: `AppendStep`, `ObjectStep` and the ledger commit hook. `scenario` never names them.
        - `scenario` adds no gate of its own inside a production item.
        - If X8b finds that `operation` needs a fixture gate outside the list, that is a revision of this law, never a unit-level choice.
      - **The source pin.** X9-1's source pin enforces the list. X8b extends that pin by name for the sites above, and adds no second pin.
      - **The two features stay separate.**
        - `scenario-fixtures` is enabled from storage's and host's `[dev-dependencies]`, so B0 to B8 run in `cargo test --workspace --all-targets`.
        - `crash-matrix` keeps X9 item 2 unchanged: no manifest names it, only the matrix targets' `required-features` reach it, and a release build with it fails at `compile_error!`.
        - Folding them into one feature would either compile X9's barrier points into every host test or drop B0 to B8 out of the documented lane.
      - **The two modules stay separate.** `crash_matrix_support` still returns no authority type (X9 item 6). `scenario` is compiled only under `scenario-fixtures`. Its `operation` returns the `ProjectOperation` that the production chain returns, and nothing else.
      - **Production behaviour does not change.** With either feature on, a shared site is reachable from outside security only through its feature's support module. Without both, the build is byte-for-byte today's.
      - **Wording change to X9 r1 (record only).** Two sentences change wording:
        - X9 item 6's "that `cfg(test)` becomes `cfg(any(test, feature = "crash-matrix"))` … no other site may use the feature" reads, for the shared sites, `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`.
        - X9's forbidden substitute "a `cfg(any(test, feature = "crash-matrix"))` site … in a build reached without an explicit `--features crash-matrix`" excepts the shared sites reached through `scenario-fixtures`, which are still absent from every release build (item 4f).

        No barrier point, `crash_matrix_support` item, row or outcome of X9 changes.
   c. **What security's `scenario` offers.**
      - **`ScenarioHome::create(parent)`:** a 0700 scratch home under the caller's scratch parent. It holds a P0 installation on 462's signed test trees and synthetic signed profile rows, and X4T-0's signed accepted store with its roles Trusted. Every path in it carries the label `synthetic`.
      - **`project(name)`:** a scratch project root.
      - **`operation(&self, root) -> Result<ProjectOperation, InstallationTermination>`.** It runs the production chain:
        - X1's write admission;
        - X2's root admission, registration and namespace lease;
        - X3a's endpoint;
        - X4's lease-free monitor and first read;
        - X3b's floor step and carrier start;
        - X2e's handoff.

        It uses only the shared sites of item 4b: the injected image and the synthetic V2 profile set through the real creator path, as X9 item 6's installation does; the fixture home source; and X4T-0's store.
      - **No in-process trust publication (r2, RF-2).** r1's `publish_revocation` is withdrawn. A trust update after the handoff runs only in a separate helper process (item 5a).
      - **`publish_revocation_fenced(home, subjects) -> Result<RevocationVersions, InstallationTermination>` (r3).** It calls the shared fenced publisher of item 4b:
        - it takes the installation fence by its production walk;
        - it writes an X4T-0-signed revocation record naming `subjects`, an empty list meaning a revocation that names nothing in any closure;
        - it replaces `state.v1` atomically;
        - it releases the fence.

        It returns the revocation version before and after. It is compiled under `scenario-fixtures` alone, with `crash-matrix` off. It refuses, without writing, if the calling process holds any operation lease that `scenario::operation` handed out (a process-wide flag that `operation` sets). Only item 5a's helper entry calls it.
      - **`revocation_version(home) -> u64` (r3).** It reads `state.v1` by name and returns its revocation version. It is read-only: it takes no fence, writes nothing, admits nothing and returns no authority type. It exists for item 5a's self-check.
      - **`paths(namespace)`:** the read-only paths of the root, `.opensip`, marker, lease, endpoint and lineage files.
      - **`carrier_census(namespace)`:** a read-only count of SEAL, REV, CLN and TERMINAL records.
   d. **What storage's `scenario` offers.**
      - **`ledger_census`:** a read-only list of each `attempt_custody` row (ExecutionId and phase) and the receipt count.
      - **`plant_attempt(execution_id)`:** writes one `admitted` `attempt_custody` row through the ledger's ordinary insert, as an earlier process would have left it.
   e. **What `scenario` never does.**
      - It never constructs an authority type itself. The one exception is the `ProjectOperation` that the production chain returns from `operation`.
      - It accepts no receipt, guard, gate, monitor, session, permit, `ReplayedRun` or clock from the caller.
      - It exposes no `FinalGate`, monitor clock or barrier point.
   f. **Release guard.**
      - **Source pin.** A source pin in `admission_tests.rs` checks every `Cargo.toml` in the workspace. `scenario-fixtures` may appear only in security's and storage's `[features]` and in `[dev-dependencies]`. It may never be a default feature or appear in `[dependencies]`.
      - **Compile-fail.** Group J's E0432 proves the plain `cargo check -p opensip-host` surface has no `scenario`. That is the surface `opensip-cli` builds against.
      - **The shared sites.** With neither feature, every shared site of item 4b is `cfg(test)` only. X9 item 2's release-absence evidence covers them unchanged.
   g. **Correction to X3d r6 item 12.** X3d-2's storage tests in the ordinary lane obtain their `ProjectOperation` through this feature (as a dev-dependency), not through crate-private `cfg(test)` fixtures, which storage cannot reach. Its matrix rows use X9's `crash-matrix` (X9 G1). Both reach the same shared site list of item 4b. X3d's next revision records this, naming that list. X3d's forbidden "production seam that supplies a `ProjectOperation`" stands, because this seam is absent from every release build (item 4f).

   **Rejected:**
   - **Behavioural cases only in the owners' private tests.** Storage cannot reach security's `cfg(test)` fixtures, so `prepare_commit` with a real session would have no test at all. `admission_tests.rs` would lose the public-boundary scenarios line 593 assigns it.
   - **A test-support crate.** X4T-0 and the write seams use security-private modules, so a separate crate would have to duplicate them, and the duplicate would diverge.
   - **A `--cfg` set through `RUSTFLAGS`.** It rebuilds the whole closure, applies to every crate, and leaks into any build run in that environment.
   - **Public seams without a feature.** That is a production seam.

5. **The behavioural cases and how they run.**

   Each is an ordinary `#[test]` in `admission_tests.rs`, named `synthetic_…` (line 886's label), on its own `ScenarioHome`. Each drives the public facade:
   - `scenario::operation`;
   - `CommitSession::open`;
   - `evaluator::replay_run` on a corpus Run from `crates/evaluator/tests/fixtures`;
   - `storage::prepare_commit`;
   - `publish`;
   - `finish`.

   **What every refusal case asserts:**
   - the outcome variant;
   - its exact `InstallationTermination` row, from X3d item 9 or X4 item 8;
   - that no `PublishedCommit` exists, which the outcome type shows;
   - the durable census after `finish`.

   **Synchronization.** Every alteration happens between two public calls on the test thread: after `operation` (the X2 item 7a handoff) or before `publish`. It is deterministic, with no sleep and no timing.
   - **On the test thread:** B3 and B5 replace project files, and B4 plants a ledger row. None of them takes the installation fence or writes trust state.
   - **In a helper process:** B6 and B7's trust publication (item 5a).

   a. **The revocation helper (r2, RF-2).** X4 item 2 forbids writing trust state under a lease, and after the handoff the test's session holds the operation lease (X2 r8 item 7a).
      - **Who publishes.** The publication is the fenced trust-owner update: X9 item 6's helper, the shared publisher on item 4b's site list. It takes the installation fence by its production walk, writes the signed revocation record, and replaces `state.v1` atomically.
      - **Where it runs (r3).** In a separate process that never ran `operation` and holds no operation lease. The fence is free, because the handoff released it.
        - **The entry.** It is an ordinary `#[test] fn x8_helper_publish_revocation()` in `admission_tests.rs`, in X9 item 3's shape. It returns at once unless `OPENSIP_X8_HELPER` is set, so it passes trivially in the lane's own run and never publishes there. It is not `#[ignore]`d, so no harness flag decides whether its body runs.
        - **The command.** The test re-executes its own binary as `current_exe() --exact x8_helper_publish_revocation --nocapture --test-threads=1`.
        - **The environment.** The environment is cleared and then given only `OPENSIP_X8_HELPER=publish-revocation`, `OPENSIP_X8_INPUT` (a file under the case's scratch root naming the scenario home and the subjects), and `TMPDIR`, set to the case's scratch parent.
        - **What the helper does.** With the variable set, it reads the input file and calls `scenario::publish_revocation_fenced`. On success it writes one tagged stderr record, `X8|published|<before>|<after>`, and returns, so the process exits 0. Any error panics, so the process exits non-zero.
      - **How the test thread waits (r3).** It reads `scenario::revocation_version(home)` before it spawns the helper. It then waits for the helper to exit, with no sleep. The case fails unless all of these hold:
        - the exit status is success;
        - stderr holds exactly one `X8|published|` record, and the harness reports one test run, not zero filtered;
        - the record's `after` is greater than its `before`;
        - `revocation_version(home)` read after the exit equals the record's `after`.

        Only then does it call `prepare_commit` and `publish`. A helper that exits 0 without publishing therefore fails the case: an ignored entry, a filter that matches nothing, or an unset variable.
      - **What the publication reaches.** The first checkpoint's monitored observation reads the published view, so the outcome does not depend on the observer's 5 s tick. If the observer ticks first, it latches on the same revocation, with the same row.
      - **Rejected:** r1's in-process `publish_revocation` on the lease-holding thread, which either takes the fence under a lease or replaces `state.v1` with no fence; and a helper thread in the test process, which shares the process that holds the lease.
      - **Rejected (r3):**
        - an `#[ignore]`d entry spawned with `--ignored`, which works, but a dropped flag turns it back into a silent no-op, and the lane's `--include-ignored` runs would execute it without the helper environment;
        - calling `crash_matrix_support`'s helper, which does not exist with `crash-matrix` off;
        - trusting the exit status alone.

   | Case | Alteration | Expected outcome | Census after `finish` | Owner of the refusal |
   |---|---|---|---|---|
   | B0 lawful control | none | `Committed(PublishedCommit)`, not latched | 1 SEAL, 1 receipt, no REV | X3d |
   | B1 admitted input | a `ReplayedRun` of another corpus Run, whose RunId, plan or proof does not bind to the session | `Refused`, invariant row `HOST.INVARIANT_VIOLATED` (X3d item 3 step 1) | no attempt row, no SEAL, no receipt | X3d-2 |
   | B2 inventory | a `ReplayedRun` whose evaluator closure differs from the session's selected core closure | the same invariant row | the same | X3d-2 |
   | B3 namespace | the marker, then (separately) the lease file, replaced after the handoff | `Refused`, custody row `CONFIG.CUSTODY_REFUSED` / `required-files-changed` (X4 item 8); gate latched | attempt row `admitted`, no SEAL, 1 REV and a CLN exactly where X3d item 7 requires one, no receipt | X4a with X3d |
   | B4 execution | `plant_attempt(session.execution_id())` before `prepare_commit` | `ExistingAttempt`, then the invariant row until X6 routes it | the planted row unchanged and alone, no SEAL | X3d-2 / X3c |
   | B5 generation | the endpoint's lineage file replaced with one naming another generation, after the handoff | the custody row; gate latched | as B3 | X4a / X3a |
   | B6 live revocation | after the handoff, the item 5a helper process publishes a revocation naming the session's core closure, and the test thread waits for it to exit | `Refused`, `TRUST.COMPONENT_REVOKED_DURING_OPERATION` (X4 item 8); gate `0 → 2` | as B3 | X4a |
   | B7 unrelated revocation | the same helper publishes a revocation naming nothing in the closure | `Committed`, with `revocation-unrelated` drift recorded | as B0 | X4a |
   | B8 replay-invalid (F01, line 609) | one byte of a claimed output altered | `replay_run` returns `Mismatch`, so no `ReplayedRun` exists to pass on (row K pins that nothing else can stand in) | the scratch home has no attempt, carrier or lease | X5a |

   - **B0 is required.** It is the positive control that makes B1 to B8 non-vacuous: the same harness, home and corpus do reach a commit.
   - **Alterations inside `publish`** (between the SEAL and the repeated checkpoint, F19) need X3d's named barrier points, which X9's law fixes. They are X3d-1's private tests and X9's matrix, not X8's.
   - **Timing cases** (the 10 s bound, a stall, a boot change, a lost lock on an unchanged descriptor) need scripted clocks. They stay in X4a's private tests (X4 item 10).
   - **X4 item 10's last bullet** ("the build plan's altered input, inventory, execution and generation handoff tests") is met at the public boundary by B1 to B5. X4a's private guard-level tests remain X4's.
   - **Rejected:**
     - altering state from a second thread with sleeps;
     - inferring "no authority" from the returned value alone, without the durable census;
     - refusal cases without B0.

6. **Failure cases and gates.** X8 tests these; their owners cover them:
   - F01 (B8; X5);
   - F18 (B6; X4);
   - F34's routing (B4; X3d);
   - the stale-guard half of the handoff checks (B3, B5; X4);
   - lines 597–604 and line 1071.

   It covers no F-case alone and qualifies no gate. M2 completion still needs X9.

## Units after the law

Each unit is reviewed with an inventory successor that lists its new files.

- **X8a (host tests; no dependency, can land now on `f1b8321`).**
  - The driver, annotation parser, toolchain check, census table and self-test (item 1).
  - Groups I, K and L.
  - The `scenario-fixtures` source pin, which passes vacuously until X8b adds the feature.

  It lands first, so each later owner unit adds its rows to a working suite.
- **Owner rows, added by their units:**
  - **X2e:** `ProjectOperation` rows D, E, F and G.
  - **X4a:** the unnameable rows for `AdmissionPermit`, `FinalGate` and `OperationGuard`.
  - **X3d-1:** rows D, E, F and G for `CommitSession`, `JournalWriteTxn`, `JournalSealBinding` and `StoppedSession`; the `open` arity case; and `execution_id()` (item 3d). It depends on X3d-0, X4a and X2e, as X3d r6 states.
  - **X3d-2:** rows A to D and G for `PreparedCommit` and `PublishedCommit`; group H; and the adapter source pin (item 3b). This replaces "the X8 doctests". It depends on X3d-1.
  - **X5a:** the `ReplayedRun` reuse case in row E.
  - **X7a:** the projection rows A and B, and the projection's export (item 3c).

  Each owner's review runs the X8a driver green with its rows added.
- **X8b (security, storage and host manifests).** The `scenario-fixtures` feature and both `scenario` modules (item 4); the joint predicate on item 4b's shared sites, extending X9-1's pin by name; group J; and the dev-dependency entries.
  - **Depends on:** X9-1 (the site list, its pin and the fenced publisher), X2e (the handoff), X3a-1, X3b-3 (the carrier start), X4a (the monitor's first read in the chain), X4T-0, and X3c-2 (the ledger census).
  - **Lands before X3d-2,** whose storage tests use it (item 4g).
    **r4 (record):** overtaken. X3d-2 integrated first, and its storage tests take no `ProjectOperation`. Item 4g stands for any storage test that needs one (see the r4 header).
- **X8c (host tests).** B0 to B8 (item 5).
  - **Depends on:** X8b, X3d-2 (and so X3d-1, X4a and X3c-2), and X5a.
  - **B6 and B7** also need X4T-b's admitted reading of a newly published revocation, which X4a's observation path depends on, and X9-1's fenced publisher (item 5a).
- **X3d r7 (record only):** item 12's storage-test fixture source, naming item 4b's shared site list (item 4g); item 11's adapter case (item 3b); and "the X8 doctests" in item 13 (item 2). No decision of X3d changes.
- **X9 (record only):** the joint-predicate wording of item 6 and of its matching forbidden substitute (item 4b). X9's accepted outcome stands.
- **EXIT-PLAN:** the X8 row gains "law X8 r2; units X8a–X8c". The "Choices" recommendation, which extends doctests, is superseded by item 1.

## Forbidden substitutes

- **As evidence:** a `compile_fail` doctest, a doctest error-code annotation, or a reason checked by hand.
- **Weak cases:**
  - a fixture without a compiling control;
  - a misuse that produces more than one error;
  - an annotation with no line, no fragment, or `none` where rustc emits a code.
- **Text matching:** comparing whole rendered or normalized stderr.
- **Toolchain:** skipping instead of failing when `CARGO`, the pinned rustc or a surface artifact is missing or different; `RUSTC_BOOTSTRAP`, or any nightly feature.
- **Dependencies:** trybuild or any new dependency; a second Cargo root or lock for fixtures; fixtures as workspace targets.
- **The wrong surface:** compiling fixtures against a surface built with dev-dependencies, features or `cfg(test)`.
- **Claiming too much:** an unpinnable case claimed as compile-fail.
- **The feature:**
  - `scenario-fixtures` as a default feature, in any `[dependencies]` table, as a new gate inside a production item's body (item 4b), or reachable from the plain host surface;
  - a `scenario` item that constructs, accepts or returns an authority type, except `operation`'s production-chain `ProjectOperation`;
  - (r2) a shared fixture site gated on one feature alone, a second site list or pin, a site on the list that only one surface calls, or X9's barrier and fault sites (`AppendStep`, `ObjectStep`, the ledger commit hook) widened to `scenario-fixtures`;
  - (r2) folding `scenario-fixtures` and `crash-matrix` into one feature, or enabling `crash-matrix` from any manifest.
- **Behavioural cases:**
  - one that sleeps, uses wall-clock timing, or alters state inside `publish` without X9's barrier points;
  - (r2) a trust publication from the process or thread that holds the operation lease, or one not made under the installation fence by the shared publisher;
  - (r3) a helper entry whose body a harness flag can skip, or a helper success accepted on its exit status alone, without the `published` record and the advanced revocation version;
  - a refusal asserted without B0, or without the durable census.
- **New vocabulary:** a new public code, row or detail.

## Not claimed

- **Not X9's matrix:** the crash, lock and revocation matrix, fresh-process recovery, and barrier points.
- **Not qualification:**
  - native scheduling and the 5 s and 10 s bounds;
  - process isolation;
  - compiler qualification ("synthetic fixtures remain labelled").
- **Not general Rust guarantees:**
  - that Rust visibility confines security's adapter trait or functions to storage (item 3b pins this by source instead);
  - any toolchain other than rustc 1.95.0;
  - other targets.
- **Not owned here:** the owner units' private tests; X6's recovery routing of B4; CLI enablement.
