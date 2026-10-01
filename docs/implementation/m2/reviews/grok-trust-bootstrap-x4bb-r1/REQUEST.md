Grok review: unit X4B-b r1, the wiring of first trust acceptance into X4T's fenced first read. Claude Opus 5.5 leads, and you are the single reviewer.

## Rules
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok-trust-bootstrap-x4bb-r1`.
- If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git only read-only, and only against the worktree below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent (it is absent at the time of writing). Never read or print the private 413 UUID fixture.
- Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`, and python3.14 at `/opt/homebrew/bin/python3.14`.
- **Scratch temp.** The user's `$TMPDIR` (`/private/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T`) has over a thousand entries and churns while other agents run. The scratch homes' chain capture then refuses at component 6 (`T`) with `Changed`, consistently, on main d884ed0 too (the F5 residual). The lead's runs used `TMPDIR=/private/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/opensip-x4bb-tmp/` (0700, outside `T`). If you replay, use a quiet directory of your own outside `T` and say which.

## The law
Arch paths are under `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/`.

- **X4B r5** (`trust-bootstrap-x4b/PROPOSAL.md`, 21587 bytes, sha256 `77b9ab1e…c62c`), accepted. X4B-b is item 11's second unit: item 1, the F-absent branch inside the `FreshnessMonitor`'s single first `read`, with items 3 (the read's own clock sample), 7 (rows), 8 (budget) and item 10's X4B-b cases (ordering, the monitor, no lease, read-only commands, a second F absent). Its forbidden substitutes apply in full.
- **X4T r11** (`trust-admission-x4t/PROPOSAL.md`, 53378 bytes, sha256 `8116f487…c1db5`), accepted: items 7 and 8 (the retained owner and its advance; one publication protocol), 9 (the fenced first read before any lease) and 10 (rows). Its r10 note makes X4B-b depend on X4T-a3, which is on main.
- **X4 r7** (`live-guards-x4/PROPOSAL.md`) item 2: the monitor and `FinalGate` are created first; the fenced admission is the monitor's first `read`; X2e's handoff only moves the monitor, view and gate.
- **X4T-b judgment call 9** (`reviews/grok-trust-floor-x4tb-r1/REQUEST.md`, accepted): a fence hold with two confirmed publications (X4B's acceptance and then a floor write) advances the gate after each one, in order.
- **X9 r1** (`crash-matrix-x9/PROPOSAL.md`) item 5: the scope table.
- Your X4B-a reviews: `reviews/grok-trust-bootstrap-x4ba-r1/` and `-r2/` (ACCEPT-UNIT; call 13 left ordering, the monitor, the lease, read-only commands and a second F absent to X4B-b).

## Subject
The worktree `/Users/sb/code/opensip-ai/opensip-x4bb`, detached at product main `d884ed0` (X4T-a3; the lock selects inventory v113). Nothing is committed and no file is added.

Save `git -C /Users/sb/code/opensip-ai/opensip-x4bb diff` as `subject.diff` in your output directory: 50723 bytes, sha256 `048afcc13007631e8afbb2d4a02d3861464489053580d0d36c69c6a7a77fbe00`. Sixteen existing files change: 710 insertions, 61 deletions. `hashes.txt` pins each file.

## What it does

**The read (`trust/trust_bootstrap.rs`, new X4B-b section).**
- `bootstrapping_first_read(work, fence, owner, inputs, invocation, source)` is the body of the monitor's first `read`:
  1. X4T-b's `fenced_first_read` on the retained owner (with its write-ahead);
  2. only on `TRUST.NO_ADMITTED_TIME_CONTEXT`, and only for `ReadMode::Fenced { report: false }`: the payload from `source`, then X4B-a's `accept_bootstrap` on `inputs.observation`, which is the read's own S4 observation. Its confirmed `state.v1` replaces the retained owner;
  3. `fenced_first_read` once more, the one confirming admission, on that owner with the same inputs. Its result is returned.
- A view, or any first refusal other than F absent, is returned as is, and nothing else runs. An acceptance refusal is returned, and no confirming admission runs. A second F absent is `TrustRow::Invariant`. No third admission runs.
- The order lives in a private generic `first_read_sequence(state, admit, accept)`, so it is tested on its own (call 7).
- A report-only fenced read returns F absent as is. A reread mode is refused by `fenced_first_read` itself (`fenced-read-mode`).
- `BootstrapSource<'a>` is the F-absent branch's only payload source (call 2). `running_core(&InitialCore)` copies the payload through X4B-a's `BootstrapPayload::from_initial_core`, charged, and only when the branch is entered. `unreached()` is `cfg(test)` and refuses as the invariant row if reached.

**The owner (`trust/floor_publication.rs`).** `RetainedCurrentTrust` keeps every confirmed publication of the hold in order (`confirmations()`); `confirmed()` is the last one, as before. `publish` pushes instead of replacing. Nothing else in the protocol changes.

**The lease-free point.**
- `trust/live_observation.rs`: `fenced_operation_read` takes the `BootstrapSource`, calls `bootstrapping_first_read`, and returns the view with every confirmed publication, in order (`Vec<ConfirmedCurrent>`).
- `custody/read_premise.rs`: `PlatformReceipt<Write>::bootstrap_source()` lends the source over the receipt's own `InitialCore`. The read receipt has no such method.
- `custody/ordinary_writer.rs`: `gate_step` lends the receipt's source beside the qualification, on the gate's ledger as before.
- `custody/operation_handoff.rs`: `trust_start` passes the source into the monitor's first read and advances the gate's `state.v1` owner after each confirmed publication, in order. The X4B-b seam comment is replaced; X2e still only moves the monitor, gate and view.

**The row.**
- `TrustRow::Invariant` (code `HOST.INVARIANT_VIOLATED`, no subject) maps to the existing `InstallationTermination::Invariant`. That is operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `HOST.INVARIANT_VIOLATED`, the pairing X3d item 9's carrier row already uses (host `installation_termination.rs`).
- X4's reread classifier puts it with the unreadable fail-stops. A reread never produces it.
- No public code, detail, row, schema or generated file changes.

**Re-exports.** `BootstrapSource` is re-exported through `current_trust_admission`, `ordinary_targets`, `root_payload` and `trust.rs`, beside `fenced_operation_read`.

## Judgment calls (lead decisions, narrowest reading)
1. **No inventory successor; v121 unused.** No file is added. `verify_design`'s `inventory_successor` admits only a strictly additive successor, so a v121 could not be selected (X4T-a3 call 1; 463h, 461a). The review is `ACCEPT` on the diff's sha256.
   - **Rows this unit makes false**, for the description-only batch (D1):
     - `trust_bootstrap.rs` ends "Not wired to the fenced first read (X4B-b)";
     - `live_observation.rs` says `fenced_operation_read` returns "the view and any confirmed publication". It now runs the bootstrap on F absent and returns every confirmed publication in order;
     - `operation_live_tests.rs` lists "a P0 installation refusing TRUST.NO_ADMITTED_TIME_CONTEXT before any lease with nothing written". That test is now the P0 acceptance case.
   - **Rows that become understated but stay true:** `trust_bootstrap_tests.rs` (already false since X4T-a3), `installation_admission_tests.rs`, `operation_guard_tests.rs`, `read_premise.rs` (its text is the read receipt's) and `ordinary_writer.rs` (`gate_step` is crate-internal).
2. **The payload source is a narrow lending of the write receipt.** Item 2 says the payload is read "through the InitialCore that X1's write receipt retains".
   - **What is lent:** only a `BootstrapSource`, which can do nothing but produce that payload. It is not `&InitialCore`, whose recheck and other surface the read has no use for.
   - **Read-only commands never bootstrap,** structurally: only `PlatformReceipt<Write>` lends one.
   - **Item 8:** the payload is copied, and charged, only on F absent, so an operation on an accepted store pays nothing for it.
   - **Rejected:**
     - an eager payload copy in `trust_start`, which charges every operation;
     - a public trait, which would let another source be supplied (a forbidden substitute);
     - `Option<&InitialCore>`, which would make "no bootstrap" a production value.
3. **A second F absent is a new internal `TrustRow::Invariant`, mapped to the existing termination.** Item 1 step 2.3 names the row. `TrustRow` had no variant for it, and 468c's `InstallationTermination::Invariant` is exactly that row. Adding a variant to the internal closed enum is not a new public code (item 7; forbidden substitutes). Every match stays exhaustive.
4. **Only `ReadMode::Fenced { report: false }` enters the branch.** A report-only fenced read reports F absent (458c, S4's report-only mode). No current read path calls this function: the read receipt lends no source, and doctor runs no trust admission. The guard keeps a future report-only caller from writing.
5. **The confirming admission is X4T-b's `fenced_first_read`, unchanged, write-ahead included.**
   - Item 1 step 2.3 says its write-ahead "finds nothing to write". That states what follows from tEval = max(F, W, A) = F on the same sample. It is not a refusal rule, so no "confirming write is an invariant" check is added. The tests pin that it writes nothing.
   - If it ever did write, that would be a second confirmed publication, followed in order (call 6). It would not be a second admission.
   - **Rejected:** a separate confirming reader. It would be a second implementation of X4T items 2 to 7.
6. **The gate follows each confirmed publication, in order (X4T-b call 9).**
   - The owner keeps an ordered list rather than the last publication, `fenced_operation_read` returns all of them, and `trust_start` calls `advance_current` on each in turn.
   - `advance_current` already accepts only from the reconfirmed predecessor, so order is enforced at the gate. The new test publishes twice in one hold: the in-order advance passes the gate's recheck, and the second applied first is `Changed`.
   - **Rejected:** advancing only to the last publication. The gate's predecessor check would refuse it after two publications.
7. **The order is factored and tested apart from any store.**
   - A real second F absent needs a confirmed pointer that is P0 again. `publish`'s reopen and confirm, and the owner's recheck, exist to prevent exactly that, so no lawful store produces it.
   - `first_read_sequence` carries the whole branch logic. Its stub test pins:
     - at most one acceptance;
     - at most two admissions;
     - nothing after a view or another refusal;
     - no confirming admission after an acceptance refusal;
     - the invariant row on a second F absent, its cause naming `second-f-absent`.
   - The production function is a thin call of it.
8. **No X9 barrier point is placed.**
   - X9 r1 item 5's table has no X4B scope. The acceptance publication's durability steps all run inside `floor_publication::publish`, the file protocol of the `x4t.floor-publication` scope. X4T-b integrated before X9-0, so its points are X9-1's to place.
   - **Recommendation to X9-1** (in flight, on an older base): open the scope inside `publish`, which covers both of its callers, not at the floor write's call site. Otherwise the bootstrap's primitives run outside any scope, which item 5 makes a `HARNESS-ERROR`. The lead will carry this to X9-1's rebase.
9. **Budget (item 8).** Everything runs inside `gate_step`'s `gate.scope`, the gate ledger with the fence held. That covers the first admission, the payload copy, X4B-a's records and reserved publication, and the confirming admission. No separate reservation is added, and X4B-a's and X4T-b's reservations are unchanged. The real handoff test runs the whole bootstrap on the production gate ledger's default limits.
10. **Not duplicated here:**
    - A dev build has no `InitialCore`, so no write receipt and no source; `ordinary_writer_tests::a_development_build_ends_in_the_no_embedded_release_row` already pins `CORE.NO_EMBEDDED_RELEASE`.
    - The crash before the pointer, with its rerun, is X4B-a's test on the same `accept_bootstrap`.
    - The uncertain pointer replacement is X4T-b's test of `publish`.
    - X4B-b adds no effect of its own.

## Tests
**`trust_bootstrap_tests.rs`, six new tests:**
- **The F-absent branch.** On P0 with the rotated default release, the read returns the confirming view: `InstallGateRequiredForNewProcess`, epoch `rootVersion` 2, and the four carried roles trusted. There is exactly one confirmed publication, the acceptance, with P0's sample as its predecessor. F, L and the anchor come from the read's observation, and the view's tEval equals F. A later first read with an `unreached()` source is admitted, enters no branch and writes nothing.
- **Never bootstrapping.** A report-only read returns F absent and a reread mode returns `fenced-read-mode`, with nothing written.
- **Acceptance refusals end the read.**
  - With no catalog, `PAYLOAD-NOT-ADMISSIBLE` (`catalog`) is returned, nothing is written, and no confirming admission runs.
  - With W beyond A + 90 d on the read's own sample, `CLOCK-EXCURSION-FORWARD` (`beyond-horizon`) is returned, and nothing is written.
  - With no component manifest, one publication is confirmed and the confirming admission refuses `component:unbootstrapped`.
- **A first refusal other than F absent.** A changed `state.v1` gives `required-files-changed`, with no acceptance and nothing written.
- **The sequence's stub test** (call 7), plus the code and subject of `TrustRow::Invariant`.
- **Source pins.**
  - `bootstrap_source` appears once in `read_premise.rs`, inside `impl PlatformReceipt<Write>`.
  - `bootstrapping_first_read(` appears once in `live_observation.rs`, and `fenced_operation_read(` once in `operation_handoff.rs`.
  - `unreached()` is `cfg(test)`.
  - Neither `installation_session.rs` nor `read_premise.rs` names the bootstrap entry points.

**`operation_live_tests.rs`, through X2e's real handoff.** `a_p0_installation_is_accepted_inside_the_first_read_before_any_lease` replaces X4a's P0-refusal test. The fixture is a creator-published P0 with the write receipt's own `InitialCore`, from 462's signed trees. A probing scripted clock records each monitor sample:
- **The bracket.** The first read's opening sample sees P0, with the fence held and both lease carriers free. Its closing sample sees the accepted `state.v1`, still with no lease.
- **The record.** The anchor equals the projection of the opening sample, and `evalHighWater` is that sample's wall time. The revision is 2, so the confirming admission wrote nothing. The four carried roles are `ST-TRUSTED`, and the start view's standing is `InstallGateRequiredForNewProcess`.
- **Afterwards.** The handoff completes, so the gate followed the confirmation, and a tick reads the same store. A second operation on the same sample changes nothing.

**`installation_admission_tests.rs`.** `the_gate_follows_two_confirmed_publications_of_one_hold_in_order` (call 6).

**`operation_guard_tests.rs`.** The termination table gains `(TrustRow::Invariant, T::Invariant)`.

**`live_observation_tests.rs`.** The first-read helper passes `BootstrapSource::unreached()` and expects one confirmed publication, the floor write.

**The lead's runs**, all with the quiet `TMPDIR` above:
- `cargo test --locked --offline --workspace`, twice on these bytes: 1557 passed, 0 failed, 3 ignored, both times. X4T-a3's recorded total was 1550; this unit adds 7 tests and replaces one. The security lib has 893 passed and 2 ignored.
- Targeted: `cargo test -p opensip-security --lib -- trust_bootstrap a_p0_installation the_gate_follows every_fenced_admission_row live_observation` gives 31 passed.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: clean.
- `cargo fmt --all --check`: clean. The include files have no rustfmt differences in this diff's hunks. Two of them, `operation_live_tests.rs` and `trust_bootstrap_tests.rs`, were clean at base and are clean now. The other include files already differ from standalone rustfmt at base, and those differences are untouched.
- `check_package_edges --lane host` against v113: passed, with 19 declared and 19 resolved.
- `verify_design.py --architecture … --lock design-lock.json --implementation .`: passed, with v113 selected.
- On main d884ed0 without this diff, with the default `TMPDIR`, `operation_handoff::tests::live::the_first_read_admits_the_start_view_before_any_lease_and_the_guard_carries_it` fails in setup (`Chain(Capture { component: 6, error: Changed })`). With the quiet `TMPDIR` it passes, which is why that `TMPDIR` was used.

## Decide
1. Does the diff implement X4B r5 item 1 step 2 exactly? In particular:
   - one monitor first read, with the F-absent admission, the acceptance and the one confirming admission all inside it;
   - acceptance only on F absent, on the read's own clock sample;
   - everything on the held fence, before any lease, on the gate ledger;
   - X2e receiving only the view;
   - a second F absent on the existing host invariant row;
   - the gate advancing after each confirmed publication, in order.
2. Is any forbidden substitute reachable? Check for:
   - a payload other than the running core's;
   - acceptance from a read-only command;
   - more than one confirming admission;
   - a clock sample of the acceptance's own;
   - a new public code;
   - `unreached()` in a non-test build.
3. Are judgment calls 1 to 10 the narrowest reading? Look especially at:
   - call 1, no inventory and the three now-false rows for D1;
   - call 3, the internal `TrustRow::Invariant`;
   - call 5, no invariant check on a confirming write;
   - call 8, no barrier point here, with the recommendation to X9-1.
4. Is anything else wrong?

## review.json
There is no inventory candidate, so the verdict is `ACCEPT`, not `ACCEPT-UNIT`, and there is no `inventoryCandidateAssessment`. review.json must contain top-level:
- "verdict": `ACCEPT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectSha256": the sha256 of `subject.diff`, `048afcc13007631e8afbb2d4a02d3861464489053580d0d36c69c6a7a77fbe00`.

Write REVIEW.md and review.json. Do not commit.
