# GROK2 review: X4-F1 r1, observer rereads evaluate expiry

**Verdict: ACCEPT.**

This unit has no inventory successor. The verdict is ACCEPT.

Subject: uncommitted diff on `/Users/sb/code/opensip-ai/opensip-x4f1`, detached at `e093e908dd7fe735356a896f3cf4b97e1d93198e`. `git diff e093e90` is 38214 bytes, sha256 `63eef2ab7e9db2c24d2ee51a1d4d988b4359e54ab51b416125cf855f3c4415fd`, 10 files, +524 −33. The evidence copy `x4f1.diff` is the same bytes. Nothing is staged and no file is added. All 43 filesystem pins in `hashes.txt` match; the git pin is that diff. `~/Library/Application Support/OpenSIP` was absent.

No cargo, test, or crash-matrix command was run. Probe E0 is using this machine. The lanes, release scan, and X9 sets below are the lead's recorded evidence, re-read here.

## Defect

The analysis is right, and this diff is the whole of X4T r11 item 6's reread obligation.

At `e093e90` a reread is `ReadMode::Reread` with no instant, the time step returns no admission, and `Shared::observe` drops the monitored read's opening sample. Item 6 says a reread does not re-admit time and does evaluate expiry and staleness at the handoff's tEval advanced by elapsed sleep-inclusive monotonic time on the same boot, with a boot change as a stop. S4's rule for that evaluation is the triple `finish` already computes: the signing root's `expiresAt` (`>=`), the catalog's `expiresAt` (`>=`), and the revocation list's `issuedAt` plus 90 days (`>`). S5's final root is that root expiry. Those are the times `evaluate_retained_ordinary` presents from the authenticated documents.

The diff does that and leaves the fenced admission's own role states alone. Applying `EV-CLOCK` at the lease-free point is the separate decision call 6 leaves open.

## Law

`ReadMode::Reread { at: i64 }` cannot be built without an instant. `HandoffClock` stores the fenced read's tEval and the monotonic seconds and boot of the S4 observation that admission used. `advanced` admits the reread sample with `RecordedObservation::admit`, then returns tEval + (M − M_handoff). Another boot is `boot`. A monotonic reading below the handoff, or a sum that overflows, is `monotonic`. An observation `admit` rejects is `observation`. The wall field is not an input to that sum.

`evaluate_reread_expiry` calls `expiry_states` on the reread's `root_expires`, `catalog_expires`, and `revocation_issued`. It does not run the observation, floor, anchor, continuity, or plausibility steps, and it proposes no write. `finish` still computes `rev_end` before `expiry_states`, so an arithmetic error keeps its previous position. The triple expression is the one `finish` had inline.

`clock_roles` dispatches `role_machine::clock`, which is `decide(state, Event::Clock { … })`. Root expiry goes to TR-BUNDLE, TR-COMPONENT, and TR-CORE. Root or catalog expiry goes to TR-INDEX. Staleness goes to those four. TR-PROFILE and TR-REPAIR stay as stored. `standing_of` joins the clocked states. The reread view keeps `time: None` and `handoff: None`.

On the X4a side, `read_sampled_with` already samples the bracket's opening and, after the callback, its end. The callback now receives that opening sample. `LiveObservation::instant` projects it with `project_monitor_sample`, the same projection `operation_handoff` uses for the first read, and asks the start view's `HandoffClock` for the instant. Both attempts of the observation use that one instant. The observation takes no second sample.

A successful fenced admission has gone through `finish`, which sets `evaluation`, so the handoff clock is present, including a report-only read. A refused admission returns before the view exists.

## Outcome

A clocked continuation refusal is `TrustRow::Continuation`, the callback error item 9 assigns to X4. `classify` maps `core:…`, `index:…`, and `component:…` to `ObservationFailure::Standing`. The revoke-shaped continuation subjects stay `Observed::Revoke`. `Shared::observe` records `failure.subject()`, so the latch is `OBSERVER.FAIL_STOP` with subject `standing` (X4 r7 item 8). A missing handoff clock, a projection failure, or an `advanced` failure is `ObservationFailure::Clock`, subject `clock`, the subject the monitor's `MalformedClock` already publishes. Item 10's public continuation row stays the fenced admission's row. The reread publishes item 9's fail-stop, and the continuation subject is the cause text (`core:expired`, `core:stale-revocation`).

Root expiry reaches TR-CORE, so the join refuses `core:expired` before the index. Catalog expiry alone leaves the index `Expired` and the standing `ExistingOnly`. X4 r7 records that standing as continuing for existing verified work. List staleness reaches TR-CORE, so the join refuses `core:stale-revocation`. `decide` orders expiry ahead of staleness, and `Clock` does not move Recovery, Revoked, QuorumLost, Unbootstrapped, or Expired.

## Traces

Added production lines contain no `crash_barrier!`, `crash_scope!`, `observe_clock`, `native_clock`, or `cfg`. The ten paths are the five production files and five test files. The monitor's opening and closing samples are the samples it already took.

The row list recomputed from the worktree required-runs files is the pinned `rows-storage.txt` (64) and `rows-host.txt` (4), and the harness prefix rule selects exactly those names. Storage is 43 tick-armed, 13 checkpoint kills (F07 ×4, F11 ×9), and 8 other X9-4 rows. Tick-armed storage is F19 ×31 with no unit field, F19 ×2 marked X9-6, F18 ×2, F41 ×2, F14 marked X9-4, and one each of F38, F39, F40, F44, and F45. Host is F39 `latched-after-admission-delivery` and F40 `latched-fail-after-evidence-commit` (tick-armed) plus the other two F40 rows.

`clockEpoch` is 1791072000 (2026-10-04T00:00:00Z). The list's staleness is 2026-12-30T00:00:00Z. A required run's scripted elapsed time does not reach that boundary, so expected outcomes stay put. The copied matrix files match the accepted X9-6 evidence on census and kill set: storage 259 points, trace 1379 records `e9add21e…`, kill set 321; host 218 points, trace 1195 records `93d0922a…`, kill set 271. Both sets carry the same census and kill set. `compare.json` records `identical: true` and `differences: []`. Product on those matrices is `{commit: e093e90, worktreeClean: false}`.

## Tests

The three new tests pin the boundaries the rule uses. The in-memory reread is admitted at the handoff instant and at 2026-12-30T00:00:00Z, refuses `core:stale-revocation` one second later and at root expiry minus one second, and refuses `core:expired` at 2027-10-01T00:00:00Z. The handoff clock returns tEval + 10 for a wall in 2020, at the handoff, and in 2029, and returns `monotonic`, `boot`, or `observation` for the three failures. The role-machine test pins the mapping, `ExistingOnly`, the two continuation subjects, expiry winning, and the states `Clock` does not move. The native observation test continues at 0, 5, and 7,686,000 seconds, then `standing` / `core:stale-revocation`; a wall set to 2020 does not hide that instant, and a wall a year ahead with 1 second elapsed still continues. The live test starts at 2026-12-29T23:59:58Z, admits an effect one monotonic second later, fail-stops `standing` two seconds after that, and appends no further witness.

The six updated `ReadMode::Reread` sites pass an instant inside the store window. `a_boot_change_fail_stops_the_next_read` is unchanged and still expects `clock`.

The lead's `e093e90` lanes, in `results.json`: fmt, builds, and clippy exit 0; the six tests passed; workspace 1749/0/3 twice; crash-matrix feature lane 1629/0/3; `verify_design.py` and `check_package_edges.py --lane host` passed; the checker unittest is 26 tests. Release `opensip` is 6314800 bytes, sha256 `4055dd66d5fef89f758e0687e60368037223a5aa52e40952b8a6b2d63afbd0db`, `found: []`, and both crash-matrix release builds exit 101. These lanes were not replayed.

## Judgment calls

1. The split matches the X4a r1 finding: X4T compares at an instant it is given, and X4a supplies that instant from the monitor's opening sample.
2. M is S4's integer-second midpoint, the same projection as the first read, at both ends of the sample. The projection's span, boot-grammar, and wall-calendar checks fail closed as `clock`. That is the first read's projection, applied to a sample the monitor already took.
3. The triple goes through `EV-CLOCK` and the join. A root expiry or a stale list stops on `core:…`. A catalog expiry alone is `ExistingOnly`, which X4 r7 admits for existing verified work. Refusing on the bare flag would stop work the role machine admits.
4. TR-PROFILE and TR-REPAIR are outside X4B r5 item 4's carried roles, and `standing_of` does not read them.
5. The instant is the handoff tEval plus this operation's monotonic elapsed time. Item 6 names that instant. Item 9 says the reread does not re-admit time, so S4 step 5's `tEval = max(F, W, A)` and the sentence "freshness is evaluated at tEval ≥ F" stay on the fenced admission. F′ on a newer pointer is another writer's wall-derived floor. Using max(T, F′) would evaluate this operation at that wall. The law does not ask for that.
6. The fenced branch still returns the stored roles and the standing taken before the clock. `TimeAdmission` still carries S4's triple. A store already expired at the handoff's tEval is admitted there; the first reread, at T ≥ tEval, applies the clock. Whether the fenced read should publish item 10's continuation row is outside this unit.
7. The fail-stop subjects are the existing `standing` and `clock`. No new public code is added.
8. `expiry_states` is the extracted triple, and `finish` still resolves the revocation horizon before it.

## Not in this unit

The fenced read's own `EV-CLOCK`, expiry detected before the next read, native scheduling of the 5 s and 10 s bounds, and Linux stay out. A full two-target `check` with `matrixPass` needs a clean commit; the lead decides that at integration. The rows above are the ones whose traces this change can move, and those traces match the accepted X9-6 evidence.
