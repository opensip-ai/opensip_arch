GROK2 review: unit X4-F1 r1, observer rereads evaluate expiry. It is OpenSIP's fix for the known defect "X4 F-1" (M2-COMPLETE.md §5 row 16; EXIT-PLAN, "X4 F-1"). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** on the diff. This is a product code unit, an X4T-a successor. It adds no file, so it has no inventory successor and no design selection.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok2-observer-expiry-x4f1-r1`. If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- **Lead note (machine window).** This request was written for Codex. GROK2 reviews it, because GROK2 was free. Probe E0's timed runs are using this machine for about the next 90 minutes. **Do not run cargo, tests or crash-matrix sets.** Review the diff, the code and the lead's recorded lanes and X9 evidence in `evidence/`. If you need a run, say so in your review and the lead will run it after E0. Where the text asks Codex a question (call 5), answer it yourself.
- Run git read-only, and only against the worktree named below.
- Don't run any cargo lane while a crash-matrix lead set is running on this machine: its 5 s timing guard fails under load. Ask the lead first.
- Run every command at `nice -n 19`, with a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Law

All under arch `docs/implementation/m2/`, accepted:
- `trust-admission-x4t/PROPOSAL.md` r11, item 6 (unchanged since r9): "Only the fenced first read admits time (item 9). Observer rereads do not re-admit time. They evaluate expiry and staleness at the handoff's tEval advanced by the elapsed sleep-inclusive monotonic time on the same boot, and a boot change is a stop (X4 r2 item 5)." Also item 1 (role standing through `role_machine::continuation`), item 9 (a reread's errors are X4's callback errors, latched as `OBSERVER.FAIL_STOP`) and item 10 ("an `Expired` core: the continuation row (`core:expired`)").
- `live-guards-x4/PROPOSAL.md` r7: item 5 (the observation and its two attempts), item 3 (the checkpoint's final observation) and item 8 (the fail-stop row, "subject the stop reason").
- `trust-bootstrap-x4b/PROPOSAL.md` r5 item 4: `EV-CLOCK` through `role_machine::decide`, and which document's expiry applies to which role.
- Security contract S4 ("Expiry, staleness and future checks still fail closed at tEval") and S5 (the final root unexpired at tEval).

The finding is Grok's X4a r1 review (`reviews/grok-live-guards-x4a-r1/REVIEW.md`, "F-1, expiry on rereads"). It says: "The advanced instant is the handoff's tEval plus the monitor's elapsed monotonic time. The clock is this unit's [X4a]. The comparison … is X4T's time admission, and the accepted reread has no parameter for that instant."

**Lead decision (2026-10-04, M2-COMPLETE.md row 16):** this is a defect, fixed by an X4T-a successor that implements the existing law. **Rejected:** an X4 amendment that weakens the requirement.

## Subject

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-x4f1`, detached at product main `e093e908dd7fe735356a896f3cf4b97e1d93198e` (F8b). Nothing is committed or staged, and no file is added.
  - The unit was written on `3e64266` (F8a) and moved onto `e093e90` with no conflict, because F8b touches no `crates/` file.
  - The diff is byte-identical on either base.
- **Diff:** `git -C /Users/sb/code/opensip-ai/opensip-x4f1 diff e093e90` is 38214 bytes, sha256 `63eef2ab7e9db2c24d2ee51a1d4d988b4359e54ab51b416125cf855f3c4415fd`, with 10 files, +524 −33. A copy is at `evidence/x4f1.diff`.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`, Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`.
- **Evidence:** `evidence/` in this directory. Every file is pinned in `hashes.txt`.
  - **Scripts:** `lanes.sh`, `rows.py`, `set.sh`, `release.sh`, `x9.sh` and `compare.py`, as run. They name the lead's scratch paths.
  - **Lane summaries:** final and preliminary.
  - **`results.json`:** test counts and the X9 summary.
  - **`release-absence.json`.**
  - **`x9/`:** the row lists, the source-pin record, the run summary, `compare.json`, and the four run-set `matrix.json` files.

## The defect, at `3e64266` (the same lines at `e093e90`)

- **The reread evaluates no time.** In `current_trust_admission.rs:950`, `ReadMode::Reread => None`: the reread's time step does nothing. `ReadMode::Reread` (`:157`) carries no instant, and `ViewInputs.observation` (`:313`) is for the fenced read only. The view's standing (`:916`) is the role machine's join over the capsule's stored role states only.
- **The observation discards the only clock it has.** In `operation_guard.rs:238`, `Shared::observe` calls `monitor.read_sampled_with(clock, |_| …)`, dropping the monitored read's opening sample. `LiveObservation::observe()` (`live_observation.rs:470`) takes no clock, and it calls the reread with `ReadMode::Reread, observation: None` (`:545`).
- **What the law requires.** At every reread (each observer tick and each checkpoint's final observation), S4's expiry and staleness are evaluated at T = tEval_handoff + (M_now − M_handoff), on the same boot. They are evaluated against the reread view's authenticated documents: the signing root's `expiresAt` (`clock.record.rootExpiresAt`, S5's final root), the catalog's `expiresAt`, and the revocation list's `issuedAt` plus 90 days. These are the three fields S4's `finish` (`trust_time.rs:153-167`) evaluates at tEval on the fenced read, which today become `TimeAdmission.expired` (`:502`, `:525`).
- **Consequence.** An operation that starts before a list goes stale, or before a root or catalog expires, keeps observing, checkpointing and committing after that instant for as long as it runs.

## What X4-F1 changes

**X4T side: the comparison.**
- `ReadMode::Reread { at: i64 }`. A reread can't be made without its instant, in UTC seconds.
- A fenced read that admits time keeps a `HandoffClock` in the view: its tEval and its S4 observation's monotonic seconds and boot. It is set for report-only reads too. A reread view has none.
- `HandoffClock::advanced(observation)` admits the reread's S4 observation by the fenced read's own grammar (`RecordedObservation::admit`), then returns tEval + (M − M_handoff). Its errors are:
  - `boot`, when the boot differs;
  - `monotonic`, when M is below the handoff's or the sum overflows;
  - `observation`, when the observation isn't admissible.

  It never uses the wall clock.
- At the time step of `admit_bound`, a reread now runs `trust_time::evaluate_reread_expiry(&input, at)`. That function applies S4's own rule, `expiry_states`, which this unit extracts unchanged from `Assessment::finish`. It runs over the reread's authenticated times, the same payload times that `evaluate_retained_ordinary` presents on the fenced read. No observation, floor, anchor, continuity or plausibility step runs, and nothing is proposed for writing.
- `clock_roles` then applies `EV-CLOCK` to the stored roles through `role_machine::clock`, a three-line wrapper that dispatches `decide(state, Event::Clock { … })`. It uses X4B r5 item 4's mapping:
  - the root's expiry goes to TR-BUNDLE, TR-COMPONENT and TR-CORE;
  - the root's or the catalog's expiry goes to TR-INDEX;
  - staleness goes to all four.

  `standing_of` joins the result again. A refusal is `TrustRow::Continuation("core:expired" | "core:stale-revocation" | "component:…" | …)`. The reread view carries the clocked states and standing, and `time` stays `None`.

**X4a side: the clock.**
- `Shared::observe` passes the monitored read's opening sample to `LiveObservation::observe(opening)`. No other sample is taken.
- `LiveObservation::instant` projects that sample with `project_monitor_sample`, exactly as `operation_handoff.rs:1016` projects the first read's sample into its S4 observation. It then asks the start view's `HandoffClock` for the instant. Both attempts of one observation use that one instant.
- No instant is the new `ObservationFailure::Clock`. That happens when there is no handoff clock, when the projection fails, or when `advanced` fails. Its subject is `clock`, the subject the monitor's own `MalformedClock` already publishes.
- A clocked continuation refusal goes through X4a's accepted `classify` to `ObservationFailure::Standing`. That is `OBSERVER.FAIL_STOP`, operational-failed, exit 4, `HOST.IO_FAILURE`, subject `standing`. It latches the gate and records the first cause, and the next checkpoint names it.

**Unchanged:** the fenced read and its write-ahead, the floors and the S6 predicate, every row and code, the ledgers and their charges, every crash point and scope, and every read and clock sample.

| File | Change |
|---|---|
| `crates/security/src/trust_time.rs` | `expiry_states` extracted from `finish`; `evaluate_reread_expiry`; `RecordedObservation::mono()` and `boot()` |
| `crates/security/src/trust/role_machine.rs` | `clock` (EV-CLOCK through `decide`) |
| `crates/security/src/trust/current_trust_admission.rs` | `ReadMode::Reread { at }`, `HandoffClock`, `handoff_clock()`, `clock_roles`, and the reread's time step |
| `crates/security/src/trust/live_observation.rs` | `observe(opening)`, `instant`, `ObservationFailure::Clock` |
| `crates/security/src/custody/operation_guard.rs` | the opening sample passed to the observation (2 lines plus the comment) |
| five test files | below |

## Tests

New tests:
- **`current_trust_admission_tests.rs`:**
  - `a_reread_fails_closed_once_its_instant_passes_an_expiry`, in memory on the default X4T-0/X4B store. The store's list was issued 2026-10-01 and its root expires 2027-10-01. The reread is admitted at the handoff instant and at exactly 2026-12-30T00:00:00Z (S4's strict `>`). It refuses `core:stale-revocation` one second later and at root expiry − 1. It refuses `core:expired` at 2027-10-01T00:00:00Z: S4's `>=`, and expiry wins over staleness as `decide` orders them.
  - `the_handoff_clock_advances_by_monotonic_time_only`: the instant is tEval + 10 for a wall clock in 2020, at the handoff, or in 2029. A monotonic reading below the handoff's, another boot, or a non-observation has no instant. A report-only view keeps the same clock, and a reread view has none.
  - `a_rereads_clock_follows_x4b_item_4_and_the_role_machine`: the mapping and the join. A catalog alone gives index `Expired` and `ExistingOnly`. The root gives four `Expired` roles and `core:expired`. Staleness gives four `StaleRevocation` roles and `core:stale-revocation`. Expiry wins from either state. Recovery, Revoked, QuorumLost, Unbootstrapped and Expired never move, and TR-PROFILE and TR-REPAIR keep their states.
- **`live_observation_tests.rs`:** `an_observation_fails_closed_once_its_monotonic_instant_passes_an_expiry`, on native files through the retained handles with no fence held:
  - continue at 0, 5 and 7,686,000 s elapsed (the boundary);
  - `standing` with cause `core:stale-revocation` one second later;
  - the same with the wall clock set back to 2020;
  - continue with the wall clock a year ahead and 1 s elapsed;
  - `clock` for a monotonic reading before the handoff's, and for another boot.
- **`operation_live_tests.rs`:** `a_list_going_stale_during_the_operation_fail_stops_before_any_further_effect`, through the real handoff and guard. The scripted monitor clock's wall is shifted so that the first read's tEval is 2026-12-29T23:59:58Z: two seconds before staleness, and within S4's plausibility bound, because L is 2026-10-01. Its monotonic readings and boot are the script's own. The steps are:
  1. +1 s: a tick continues, and an effect checkpoint appends its `RA`;
  2. +2 s more: the tick fail-stops `standing`, and the gate is `LatchedBeforeAdmission`;
  3. the commit checkpoint refuses with that first cause, and no further record is appended.

Changed tests:
- The existing `observe()` calls in `live_observation_tests.rs` pass an opening sample.
- That file's first-read observation boot becomes a platform-grammar UUID, so that the projection of a same-boot sample matches it.
- Six `ReadMode::Reread` sites in `current_trust_admission_tests.rs`, `floor_publication_tests.rs` and `trust_bootstrap_tests.rs` gain an instant inside the store's window. Each is the instant the surrounding fenced read used, or a refusal that happens before time is considered.

Existing tests whose behaviour must not move: `a_boot_change_fail_stops_the_next_read` still gives `clock`, now from the observation's own `Clock` failure as well as from the monitor's. The stall, boundary and shared-history tests advance by seconds only, so no expiry is reached. The S4 reference fixtures (1894 clock cases and 44 admitted cases) still exercise `finish`, which now calls `expiry_states`.

## Crash barriers, traces and the X9 rows

**No crash point, scope, read, write or clock sample is added, removed or moved.** `git diff e093e90` touches no `crash_barrier!`, `crash_scope!`, `observe_clock`, `native_clock`, `cfg` or file I/O line outside tests. `instant` projects a sample the monitor already took, and the reread's expiry uses documents it has already authenticated. So every trace and kill set is unchanged.

Outcomes change only when an expiry or staleness instant falls inside a run's [tEval, tEval + elapsed]. The matrix's scripted wall starts at `clockEpoch` 2026-10-04T00:00:00Z (+3600 s per child ordinal). The nearest boundary in its stores is the list's staleness, 2026-12-30T00:00:00Z. So no required run's expected outcome changes.

### The rows that exercise the changed code

- **Storage, `x4.observer.tick` armed (43 runs):**
  - X9-4: F18 ×2, F19 ×31, F38, F39, F40 (latched), F41 ×2, and the moved F14 row;
  - X9-6 (r16 W5): F19 ×2;
  - X9-3: F44 and F45.
- **Storage, X9-4's other 8 rows** (F06 ×2, F26, F30 ×2, F34, F40 ×2), which complete X9-4's 47-row subset.
- **Storage, the r16 checkpoint kills around the observation (X9-6, 13 runs):** F07 ×4 and F11 ×9, at `x4.checkpoint/lock.before`, `.before-observation`, `.after-observation`, `.before-admit` and `x4.gate.admit.after`.
- **Host (4 runs):** F39 `latched-after-admission-delivery` and F40 ×3. F39 and F40's latched variant arm the tick.
- **Both censuses.**

Every other committing row also runs the reread at its checkpoint's final observation, with no trace change.

### The regression, run (2026-10-04, on `e093e90` plus the diff)

**Source pins first** (`evidence/x9/source-pins.txt`):
- Every X9 harness source is byte-identical at `e093e90` and at X9-6's C, `3d2d5b5`, and the diff touches none of them. Those sources are:
  - the checker and its test;
  - `crates/platform`;
  - storage's and host's tests and both `required-runs.v1.json` files;
  - security's `crash_matrix_sites.rs`, `crash_matrix_census.rs` and `crash_matrix_support`.
- The checker's suite passes: 26 tests, OK.
- X9-0's `no_manifest_enables_the_crash_matrix_feature` and X9-1's `every_test_feature_site_is_on_the_pinned_list` pass in both workspace runs. F8b's `tools/contracts/Cargo.toml` edit is among the manifests the first reads.

**The runs:**
- **Selection.** `evidence/rows.py` computes the 64 storage and 4 host rows from the required-runs files. It checks that the harness's own `OPENSIP_X9_ROWS` prefix rule selects exactly those rows and no other.
- **Two sets.** `evidence/set.sh` runs X9-6's run-set entry, `x9_6_matrix` (census, then the selected rows), for storage and then host. It ran as two sets, `x4f1-1` and `x4f1-2`, one after the other, with nothing else running and a private 0700 TMPDIR.
  - Storage: 384 s and 386 s.
  - Host: 69 s and 70 s.
  - Every run is PASS, and the real home stayed absent.

**The comparison** (`evidence/compare.py`, output `evidence/x9/compare.json`) is against the accepted X9-6 evidence, arch `crash-matrix-x9/evidence/3d2d5b5…/` (its lead-1 run files and both targets' `matrix.json`).
- **What it compares**, for every run in both sets:
  - verdict;
  - `postState.normalizedSha256`;
  - ladder and `notApplicable`;
  - every child's role, ordinal, exit, `lastHeld`, outcome and trace `{records, sha256}`;
  - whether `timingGuard` is present.
- **Per target and set:** the census points and census trace, and the kill set.
- **The result: identical, with 0 differences.**
  - Storage: 64/64 runs equal in both sets. Census: 259 points, trace 1379 records, `e9add21e…`. Kill set: 321 points.
  - Host: 4/4 runs equal in both sets. Census: 218 points, trace 1195 records, `93d0922a…`. Kill set: 271 points.
- **Timing guards** (not compared, all within 5,000 ms):
  - storage 2,603–2,943 ms (43 runs per set);
  - host 1,052–1,181 ms (2 runs per set).
- **Expected differences:** each record's `product` is `{commit: e093e90, worktreeClean: false}`, because the subject is uncommitted, and `releaseAbsence` carries the new binary below. Neither is in the comparison.

A full two-target `check` with `matrixPass` needs a clean commit, so it can only run at integration; the lead decides whether to run it then. These rows are the ones the change can reach.

## Judgment calls

1. **The split.** The comparison is X4T's: the reread takes the instant as a parameter and evaluates S4's rule. The clock is X4a's: the observation supplies the instant from the monitor's opening sample. This is the split Grok's X4a r1 review drew.
2. **The instant's arithmetic.** It uses S4's own M: the integer-second midpoint projection that already makes the first read's S4 observation, at both ends of the interval. That is the arithmetic of S4's continuity rule, `expected = anchorWall + (M − anchorMono)`. Expiry instants and tEval are whole seconds too.
   - **Rejected:** nanosecond `Duration` arithmetic on raw samples. The handoff keeps only its S4 observation, so that would be a second arithmetic for one M.
   - **Consequence:** the projection's span (≤ 1 s) and boot-grammar checks now also apply to rereads. They already apply to the first read, and a failure fails closed as `clock`.
3. **What evaluation does with the result.** The result goes through `EV-CLOCK` on the stored roles (X4B r5 item 4's mapping), then the role machine's join. So a root expiry or a stale list stops the operation (`core:…`). A catalog expiry alone gives `ExistingOnly`, which admits continuing work, and every M2 writer effect is continuing work (X4 r7, r5 note).
   - **Rejected:** refusing on any expiry flag, which would stop work the role machine admits, and would bypass X4T-a r1 call 6 ("clock expiry is never an S5 row").
   - **Rejected:** carrying the triple without applying it, which would not fail closed.
4. **TR-PROFILE and TR-REPAIR are not clocked.** No law maps their documents' expiry, and the standing's join doesn't read them.
5. **The instant is the law's, not max(T, F′).** A newer pointer from another process may carry F′ > T, F′ being that process's wall-derived tEval. Item 6 names the advanced handoff instant. Taking the larger would import another process's wall reading into an evaluation the law ties to this operation's monotonic clock. Is that reading right, or should S4's "freshness is evaluated at tEval ≥ F" govern the reread too?
6. **The fenced read is unchanged.** As accepted (X4T-a r1 call 6), it carries S4's triple on `TimeAdmission` and doesn't apply it to the roles. A store already expired or stale at the handoff's tEval is therefore admitted at the lease-free point. Its first reread, at T ≥ tEval, applies the expiry, so the first tick or checkpoint fail-stops before any effect after the handoff. With X4T-0's default (X4B-produced) stores this can't arise: L, and so A, is the list's issue time, so S4's plausibility bound stops W at the staleness boundary. It can arise in general, whenever a document newer than the list raises A. Whether the fenced read should apply `EV-CLOCK` too is a separate lead decision. It would publish item 10's continuation row at the lease-free point, and it is out of this unit.
7. **No new vocabulary.** There is no new code or detail, and no new fail-stop subject: `standing` and `clock` both exist.
8. **The extraction is behavior-preserving.** `finish` computes the same `rev_end` first, so its arithmetic errors keep their order.

## Not claimed

- The fenced read's own application of expiry (call 6).
- Detecting a stopped process's expiry before its next read. S6's 10 s bound already fail-stops a stall.
- Native scheduling of the 5 s and 10 s bounds (L3).
- Linux.

**Pre-existing, not this unit:** X4T-0's fixed dates (in produced stores, list issued and L both 2026-10-01) make native-clock lanes refuse `beyond-horizon` from 2026-12-30T00:00:01Z. This unit's staleness falls at the same second, so for those stores the date doesn't move. For the fixture's self-constructed stores (L 2026-10-02) it moves one day earlier, from 2026-12-31 to 2026-12-30. A fixture date refresh is owed before then. The crash matrix's scripted clock is unaffected.

## No inventory

The diff adds, removes and renames no file, so v134 stands. Inventory rows carry no bytes, and the touched files' descriptions remain true. As with F3–F8a, there is no inventory successor and no `inventoryCandidateAssessment`.

## Lead results

**How they ran:** every lane ran on `e093e90` plus the diff (`evidence/lanes.sh`), serially, with a private 0700 TMPDIR, `--locked --offline`, and nothing else running. The summary is `evidence/lanes-e093e90-summary.txt`, and the counts are in `evidence/results.json`. The real home stayed absent throughout.

| Lane | Result |
|---|---|
| `cargo fmt --all --check` | pass |
| `cargo build --workspace --all-targets` | pass |
| `cargo build` of platform, security, storage and host, `--features crash-matrix --all-targets` | pass |
| `cargo build` of security, storage and host, `--features scenario-fixtures --all-targets` | pass |
| `cargo build -p opensip-security --features opensip-platform/crash-matrix` | pass |
| `cargo clippy --workspace --all-targets -- -D warnings` | pass, no warnings |
| `cargo clippy`, the crash-matrix lane (four packages, `--all-targets`, `-D warnings`) | pass |
| `cargo clippy`, the scenario-fixtures lane (three packages, `--all-targets`, `-D warnings`) | pass |
| The six new and changed tests (security lib, `--test-threads=1`) | 6 passed, 0 failed |
| `cargo test --workspace`, run 1 | 1749 passed, 0 failed, 3 ignored (515 s) |
| `cargo test --workspace`, run 2 | 1749 passed, 0 failed, 3 ignored (520 s) |
| `cargo test`, platform, security, storage and host, `--features crash-matrix --all-targets` | 1629 passed, 0 failed, 3 ignored (506 s) |
| `verify_design.py --architecture ../opensip_arch --implementation .` | pass |
| `check_package_edges.py --lane host` against inventory v134 | pass |
| `python3.14 -m unittest tools/tests/test_check_crash_matrix.py` | 26 tests OK |
| X9 regression (above): two sets, 64 storage and 4 host runs, plus both censuses | identical to the X9-6 evidence, 0 differences |

**Notes on the results:**
- **Workspace count.** X9-6's lanes counted 1744 workspace tests at `3d2d5b5`; the 5 new tests make 1749.
- **Preliminary runs on `3e64266`.** The same lanes ran on `3e64266` before F8b landed, with the same diff and the same counts (`evidence/lanes-3e64266-preliminary-summary.txt`): workspace 1749/0/3 twice and the feature lane 1629/0/3. They are preliminary only.
- **Cached builds on `e093e90`.** The build and clippy steps there were fresh no-ops: F8b changes no Rust input, so cargo reused the artifacts the `3e64266` lanes had just built and linted from the same sources.

**Release absence** (`evidence/release.sh`, record `evidence/release-absence.json`):
- `cargo build --release -p opensip-cli` (no features) gives `target/release/opensip`, 6314800 bytes, sha256 `4055dd66d5fef89f758e0687e60368037223a5aa52e40952b8a6b2d63afbd0db`.
- Neither `OPENSIP_X9_` nor any of the 25 registered scope names appears in it (`found: []`, `passed: true`).
- The release builds of storage and of host with `--features crash-matrix` are each refused at the compile guard (exit 101).
- X9-2 to X9-6 recorded 6315264 bytes, `b32604fe…`. The binary differs because the security code it links changed.

## Decide

- **Defect:** is the analysis above right, and is this the whole of item 6's reread obligation?
- **Law:** does the change implement item 6 exactly: the instant, the fields, the rule, the boot stop and monotonic-only time? Does it change nothing else?
- **Outcome:** is `OBSERVER.FAIL_STOP` `standing` (or `clock`) the law's outcome for a reread past an expiry (X4T items 9 and 10, X4 item 8)?
- **Traces:** confirm that no crash point, read or clock sample moves, and that the X9 list is complete.
- **Tests:** do they pin before, at and after each boundary, the wall-independence, and the end-to-end fail-stop?
- **Judgment calls:** are calls 1 to 8 acceptable? Call 5 asks you a direct question.

Write REVIEW.md and review.json under the output directory. review.json needs:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectSha256"`: `63eef2ab7e9db2c24d2ee51a1d4d988b4359e54ab51b416125cf855f3c4415fd`, the diff's sha256, as a single string.

No `subjectManifestSha256` or `inventoryCandidateAssessment` is needed. Do not commit.
