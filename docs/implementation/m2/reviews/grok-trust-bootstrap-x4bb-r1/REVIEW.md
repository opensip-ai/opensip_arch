# X4B-b r1 — ACCEPT

The diff implements X4B r5 item 1 step 2. The monitor's single first read runs the F-absent admission, the acceptance on that read's own clock sample, and one confirming admission. The fence is held, no lease is taken, and the charge stays on the gate ledger. X2e receives the view. A second F absent is the existing host invariant row. The gate advances after each confirmed publication, in order.

None of the forbidden substitutes is reachable from this wiring. The payload is the write receipt's `InitialCore`, copied only when the F-absent branch is entered. A read receipt lends no source. The sequence calls the confirming admission once. `unreached()` is `cfg(test)`. `TrustRow::Invariant` adds no public code.

Judgment calls 1 to 10 are the narrowest reading. Calls 1, 3, 5, and 8 are stated below. Nothing else in the code that was read is wrong.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x4bb`, detached at `d884ed084109d1e6be70a30b2f26e496db252023`. Nothing is committed. Sixteen modified files, no additions: 710 insertions, 61 deletions. `subject.diff` is 50723 bytes, sha256 `048afcc13007631e8afbb2d4a02d3861464489053580d0d36c69c6a7a77fbe00`. All 25 `hashes.txt` pins match, including the sixteen product files, X4B r5, X4T r11, X4 r7, X9 r1, the three prior review files, inventory v113, and that diff. The worktree lock's last inventory successor selects v113 (`c35788a82f5b2561e6fb0df9b920def2c978790555190a9dc0f5a9105e7f5874`, 429574 bytes).

Law is X4B r5, `trust-bootstrap-x4b/PROPOSAL.md`, 21587 bytes, sha256 `77b9ab1e27028a50af5d1b49cccdd835a365c8066d6955052f263d87823fc62c`. X4T r11 is 53378 bytes, sha256 `8116f487a852675627bd61f6ccac7d8e7dab360e49dce80d683b78795c2c1db5`.

`~/Library/Application Support/OpenSIP` is absent.

## The first read

`bootstrapping_first_read` is the body of the monitor's first read. `ReadMode::Fenced { report: false }` is the only mode that enters the branch. Every other mode returns `fenced_first_read` as it stands, so a report-only read returns F absent and a reread mode is refused by that function (`fenced-read-mode`).

`first_read_sequence` holds the order. The first `admit` returns any view, and any refusal other than `TrustRow::NoAdmittedTimeContext`, immediately. On F absent it runs `accept` once. An acceptance `Err` returns through `?`, so the confirming admission does not run. The second `admit` is the one confirming admission. A second `NoAdmittedTimeContext` becomes `TrustRow::Invariant` with cause `("second-f-absent", refusal.cause)`. Any other confirming result is returned. The admit closure in the stub test panics on a third pop.

The production accept closure takes `inputs.observation`, refuses `HostIo` / `observation` when that sample is absent, copies the payload, and calls `accept_bootstrap` on that observation. `fenced_operation_read` builds the inputs as `ReadMode::Fenced { report: false }` with `Some(observation)`, where `trust_start` projects the observation from the monitor's opening sample.

## Payload source

`BootstrapSource` holds `Option<&InitialCore>`. `running_core` stores the reference. `payload` calls `BootstrapPayload::from_initial_core` only when the branch is entered, and that copy is charged on the caller's ledger. `unreached()` is `cfg(test)` and, if the branch is reached with it, refuses `TrustRow::Invariant` cause `bootstrap-source`.

`PlatformReceipt<Write>::bootstrap_source` is the only lender, and it lends `running_core` over the receipt's own core. `gate_step` lends that source beside the qualification and runs the action inside `gate.scope`. `trust_start` creates the monitor first, passes the source into `fenced_operation_read`, and still only moves the monitor, the view, and the gate. The source-pin test requires one `bootstrap_source` inside `impl PlatformReceipt<Write>`, one `bootstrapping_first_read(` in `live_observation.rs`, one `fenced_operation_read(` in `operation_handoff.rs`, one `accept_bootstrap(work` in `trust_bootstrap.rs`, and neither `installation_session.rs` nor `read_premise.rs` naming those entry points. Re-exports through `current_trust_admission`, `ordinary_targets`, `root_payload`, and `trust.rs` are `pub(crate)`.

## Confirmations and the gate

`RetainedCurrentTrust` keeps `confirmed` as a `Vec`. `publish` pushes each `ConfirmedCurrent`. `confirmed()` is the last element. `confirmations()` returns the slice in order. `fenced_operation_read` returns `owner.confirmations().to_vec()`. `trust_start` calls `advance_current` on each element in that order.

`the_gate_follows_two_confirmed_publications_of_one_hold_in_order` publishes twice in one hold. The second confirmation's predecessor equals the first confirmation's metadata. Advancing in order leaves the gate's current metadata equal to the second, and the gate recheck passes. Advancing the second first is `GateRefusal::Custody(Changed)`.

The confirming admission is the same `fenced_first_read`, write-ahead included. Item 1 step 2.3's "finds nothing to write" follows from tEval = max(F, W, A) = F on the same sample. The code adds no refusal that a confirming write would be an invariant. A confirming write would be another `ConfirmedCurrent` on the same list, followed by `trust_start` in order. The P0 handoff test pins revision 2 and one confirmation, so on that path the confirming admission wrote nothing.

## The row

`TrustRow::Invariant` codes `HOST.INVARIANT_VIOLATED`. `subject()` falls through to `None`. `trust_termination` maps it to `InstallationTermination::Invariant`. The host row, unchanged by this diff, is `Class::OperationalFailed`, exit 4, `Code::SystemOutcomeIllegalState`, `Fault::HostInvariant`, detail `Detail::HostInvariantViolated`. The termination table gains `(TrustRow::Invariant, T::Invariant)`.

The reread classifier's unreadable arm includes `Invariant` with `Incomplete`, `NoAdmittedTimeContext`, `StateSchemaUnsupported`, `HostIo`, and `RequiredFilesChanged`. `bootstrapping_first_read` is called only from `fenced_operation_read`, which hardcodes `Fenced { report: false }`, so a reread never produces the row. The existing reread test leaves the `Invariant` arm unnamed. The arm is present and grouped with the unreadable fail-stops.

The internal cause `second-f-absent` stays on `TrustRefusal.cause`. The diff changes no public code, detail, row, schema, or generated file.

## Judgment calls

1. No inventory successor. No file is added, and v121 is unused. `verify_design`'s `inventory_successor` admits only a strictly additive successor, so a description-only edit cannot be selected. The verdict is `ACCEPT` on the diff sha256. Three v113 descriptions are now false and belong in the description-only batch: `trust_bootstrap.rs` still ends "Not wired to the fenced first read (X4B-b); grants nothing."; `live_observation.rs` still says `fenced_operation_read` returns "the view and any confirmed publication"; `operation_live_tests.rs` still lists "a P0 installation refusing TRUST.NO_ADMITTED_TIME_CONTEXT before any lease with nothing written." The lead's understated-but-true rows (`trust_bootstrap_tests.rs`, `installation_admission_tests.rs`, `operation_guard_tests.rs`, `read_premise.rs`, `ordinary_writer.rs`) stay disclosures. This review carries no required finding for them and no `inventoryCandidateAssessment`.

2. The payload source is a narrow lending of the write receipt. Only `BootstrapSource` is lent, and only `PlatformReceipt<Write>` lends one. The copy and its charge happen on F absent. The rejected alternatives — an eager copy in `trust_start`, a public trait, and `Option<&InitialCore>` as a production "no bootstrap" value — are absent.

3. A second F absent is a new internal `TrustRow::Invariant`, mapped to the existing `InstallationTermination::Invariant`. Item 1 step 2.3 names that row. Adding a variant to the internal closed enum is not a new public code. `code()`, `subject()`, `trust_termination`, the termination table, and the reread classifier are exhaustive.

4. Only `ReadMode::Fenced { report: false }` enters the branch. A report-only read returns F absent. A reread mode returns `fenced-read-mode`. The read receipt lends no source.

5. The confirming admission is X4T-b's `fenced_first_read`, unchanged, write-ahead included. "Finds nothing to write" is what follows from tEval = max(F, W, A) = F on the same sample. It is not a refusal rule, and no "confirming write is an invariant" check is added. The tests pin that the P0 acceptance writes nothing. A confirming write, if `fenced_first_read` ever made one, would be a second confirmed publication followed in order. It would be another publication on the same hold, and the sequence would still have called `admit` twice.

6. The gate follows each confirmed publication, in order. The owner keeps the list, `fenced_operation_read` returns all of them, and `trust_start` calls `advance_current` on each. `advance_current` accepts only from the reconfirmed predecessor. The new test pins the in-order pass and the `Changed` refusal when the second is applied first.

7. `first_read_sequence` is tested apart from any store. The stub pins a view at counts `(1, 0)`, another first refusal at `(1, 0)`, an acceptance refusal at `(1, 1)`, a confirming result at `(2, 1)`, and a second F absent as `TrustRow::Invariant` with cause containing `second-f-absent`, code `HOST.INVARIANT_VIOLATED`, subject `None`, and counts `(2, 1)`. `bootstrapping_first_read` is a thin call of it.

8. No X9 barrier point is placed. X9 r1 item 5's table has no X4B scope, and `crash-matrix-x9/PROPOSAL.md` contains no X4B text. `subject.diff` contains no `crash_barrier`. The acceptance publication's durability steps run inside `floor_publication::publish`, the file protocol of the `x4t.floor-publication` scope. X4T-b integrated before X9-0, so those points are X9-1's to place. Recommendation to X9-1, carried by the lead: open that scope inside `publish`, which covers the floor write and the bootstrap acceptance. Opening it only at the floor write's call site would leave the bootstrap's primitives outside any scope, which item 5 makes a `HARNESS-ERROR`. That recommendation is not a finding for X4B-b.

9. The budget is `gate_step`'s `gate.scope`, the gate ledger with the fence held. The first admission, the payload copy, X4B-a's records and reserved publication, and the confirming admission run there. No separate reservation is added. The P0 handoff test runs that path on the production gate ledger's default limits.

10. Effects already pinned elsewhere stay there. A development build's `CORE.NO_EMBEDDED_RELEASE` row, the crash before the pointer, and the uncertain pointer replacement are X4B-a's and X4T-b's tests. X4B-b adds no effect of its own.

## Replay

Targeted `cargo test --locked --offline -p opensip-security --lib`, one filter at a time, `--test-threads=1`, `CARGO_TARGET_DIR` under this review directory. The lead's workspace total (1557 passed, 0 failed, 3 ignored), clippy, fmt, `check_package_edges`, and `verify_design.py` were not replayed.

`TMPDIR` was first `/tmp/opensip-implementation/reviews/grok-trust-bootstrap-x4bb-r1/tmp` (mode 0700). `trust_bootstrap::tests` passed 23 in 17.15s, `every_fenced_admission_row_takes_its_x4t_item_10_termination` passed 1, and `live_observation::tests` passed 5 in 0.97s. The two installation-chain tests panicked in fixture setup, `Ancestor { component: 2, refusal: OthersWrite }`, because `/private/tmp` is mode 0777. Those panics are at `installation_read_fixture.rs:65` and `installation_admission_tests.rs:83`, before either test body.

Those two were rerun with `TMPDIR=/private/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/opensip-x4bb-r1-review-tmp` (mode 0700, a sibling of `T`, ancestors mode 0755). `a_p0_installation_is_accepted_inside_the_first_read_before_any_lease` passed in 2.16s. `the_gate_follows_two_confirmed_publications_of_one_hold_in_order` passed in 1.16s.

Targeted total: 31 passed, 0 failed. The cargo target and both private temp directories were removed after the runs.
