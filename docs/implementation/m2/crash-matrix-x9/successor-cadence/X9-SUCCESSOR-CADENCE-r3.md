# X9-SUCCESSOR-CADENCE r3: the unarmed observer's cadence in census runs

**Status:** a draft successor record. It has no effect until the coordinator signs its adoption receipt (brief; LD-Q-232).
**Score:** `X9-CADENCE: ADOPTABLE | REJECT | ALTERNATIVE`.
**Author:** claude-x9-cadence (w39:p1, R3-FRONTIER, claude-opus-5-5/high), 2026-11-01.

**r3 changes.** This revision answers the REJECT in `review/REVIEW-r1.md`, which scored r2 (`69b3027b…`). r1 and r2 are history.
- **RF-1:** S7's C1 is replaced. The proof of a stall's position is separated from the observation of a timed tick, and a
  correctly positioned run with no second tick is kept. The method is now in this record, so the stale pointer is gone.
- **RF-2:** S4 is rewritten around the bound's actual sampling. R6's wording changes to match: its policy is the same, but
  "keeps running" wrongly implied a watchdog. **R1 to R5 are unchanged.**
- **Supplemental corrections:** S7 gains the exact counting contract, the stall's measured interval, and R6 classified only from
  an actual bound refusal.
- **NB-1:** S2's row counts are corrected, and the "173 barrier points" figure is withdrawn.
- **NB-2:** S5 lists the unaffected `Census` consumers.
- **New inputs:** w2A's measurements (S4), LD-Q-235 and LD-Q-236 (S7, S8).

**Bases.** **A** = architecture `5f328f32dc5f`; **P** = product main `fe379d218358`.

| Short name | File | sha256 |
|---|---|---|
| X9 (r17, accepted) | A `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md` | `7a37a16f664dfd11…` |
| X4r7 | A `docs/implementation/m2/live-guards-x4/PROPOSAL-r7.md` | `fc8490f4e751e486…` |
| X4 (r8, accepted) | A `docs/implementation/m2/live-guards-x4/PROPOSAL.md` | `bb2fd6a4b97ceaee…` |
| Failure report | `main-rustfmt-1/ldq228/REPORT-LDQ229-230-r1.md` §2 | `24ef0f0b44f1afb2…` |
| Law note | `flake7-fix-1/NOTE-LAW-r1.md` | `434ee09d6e46669f…` |
| Measurements | `flake7-fix-1/EVIDENCE-ITEM2-r1.md` | `53cf576d03ca69b8…` |
| Review of r2 | `x9-cadence/review/REVIEW-r1.md` | `ebb2df7d59b0834f…` |
| Rulings | `coordinator/msg-ldq230.txt`, `231`, `232`, `233`, `235`, `236` | `3199db4c…`, `5427b0b7…`, `fe3c87b8…`, `37377f88…`, `58e99276…`, `17e439ce…` |

Bare `:n` citations are X9 lines. `operation_guard.rs` and `revocation.rs` are in P `crates/security/src/` (`custody/` for
the first).

## S1. Why a rule is owed

r3 of X9 disclosed that census runs leave the observer on its real 5 s period, and that "this law's next revision" owes a rule
"if those runs need" one (:54-58). r16 recorded that X9-6's census parts were each equal across two runs, "so no rule is
needed" (:815).

Those runs now need one. At P, storage's `the_commit_driver_census_is_equal_across_two_runs` failed 1 of 2 under load
and 0 of 20 alone. The two censuses differ only in occurrences of the observer's two read-only points: `tick` 2 and
`after-observation` 1 against `tick` 1 (failure report §2). The cause is the gap r3 named: a guarded operation that
outlasts the timer.

## S2. The rule

> **R1. What a census run is.** For this rule, a census run is a matrix child whose `OPENSIP_X9_ARMS` is present and
> arms nothing. That is the child-side form of the precondition `Census::from_exit` already enforces, "traced with
> nothing armed" (P `crates/platform/src/crash_barrier/driver.rs:563-569`).
>
> **R2. Its cadence.** In a census run, the unarmed `x4.observer.tick` gate runs no timed wait. After reaching the point,
> the observer waits only for `Stop` (or a closed channel). There is no timed wake, so the observer thread makes no
> observation and `x4.observer.after-observation` never occurs.
>
> **R3. Its counts.** `x4.observer.tick` occurs exactly once per operation guard the run starts, and
> `x4.observer.after-observation` occurs zero times. A census holding `x4.observer.after-observation` is a
> `HARNESS-ERROR`.
>
> **R4. Every other process is unchanged.**
> - `OPENSIP_X9_ARMS` absent: the product's 5 s period (item 2's sentence at :942 stands).
> - An arming that names `x4.observer.tick`: the rendezvous replaces the wait (:988, :1246).
> - An arming that names other points only: the product's 5 s period.
>
> **R5. Production.** X4r7 item 5's "Every 5 s" (X4r7:75, carried at X4:175) and `OBSERVER_PERIOD` (5 s) are unchanged.
> R2 exists only under `crash-matrix`, and no production build can reach it.
>
> **R6. The 10 s bound is unchanged, and a refusal by it is not a census.** Every monitored read and admission-boundary check
> a census run reaches applies the bound on the native monotonic clock, as in production. A census child refused by such a
> check is a `HARNESS-ERROR`, never an `OBSERVER.FAIL_STOP` that the run then accepts, and never a retry or a smaller kill
> set.

**R3's scope.** "Once per guard" holds for a census that completes normally: a started observer reaches the gate before it
examines `Stop`, and the guard's drop sends `Stop` and joins (`operation_guard.rs:551-555`, `:584-600`). The reviewer traced
every current census path and found none that leaves a started guard alive at exit (REVIEW-r1 §1). It is not a claim about
killed, leaked or harness-aborted children, and F42's `mem::forget` child is armed, so it is outside R1.

**Why the predicate is wider than "census" (R1).** A child cannot know whether its parent will census it. The driver's
environment is a closed list (:948), the driver names are shared (`commit` is both the census child and a row's next
writer), and a new variable would widen that list. So R2 also reaches a row's nothing-armed children, such as ladder
steps and peers.

This is lawful because no expected value depends on their timer. Re-derived by the reviewer (REVIEW-r1 §5, NB-1):
- **Storage:** 403 rows, with 216 explicit spawns (121 empty, 52 other-armed, 43 tick-armed). No `mutate` falls between an empty
  child's spawn and its finish. Five rows expect a revocation or observer outcome (F18 revoked and unreadable, F19 revoked and
  unreadable, F38 revoked), and all five arm the tick. My scan said three, because it missed the CamelCase `ObserverFailStop`.
- **Storage's implicit children** (`finished("commit", "", "")` bases, ladder and next-writer children) are not in the scan's
  spawn count. The reviewer found no expected value that needs one of their autonomous ticks.
- **Host:** 102 rows. Only F39 and F40 use the observer, and both arm `tick#*=hold`.

Nothing-armed row children also meet S4's changed refusal opportunities. This is not a claim that they behave identically under
every load.

## S3. Item 3's scripted clock, and what is superseded

**Item 3.** Item 3 scripts one thing, the wall reading (:951). This rule adds the observer's cadence to what is fixed in a
census run, so "under the scripted clock" (:1001) now also means "with no elapsed-time tick". Item 3 gains no second
script: R2 removes a timer and replaces no reading.
- **The monotonic readings and boot identity stay native,** and "a scripted monotonic clock" stays forbidden (:1329).
- **One clause of :951 narrows.** In "X4's freshness and observer bounds … unchanged", the 5 s period gains the R1 exception.
  The 10 s check and the admission-boundary check stay numerically and natively unchanged, but their observation
  opportunities and history refreshes change (S4).
- **:1001's claim holds on slow, normally completing runs.** A timed observation takes wall readings through `native_clock`
  (`revocation.rs:43-44`, P `crates/platform/src/clock.rs:68-77`), so it shifts `n` in `E + 3600·k + n` for the main
  thread. R2 removes that source. This is not a general proof about failure or scheduling.

**Item 4.** "Unarmed, the product's 5 s period is unchanged" (:988) gains the exception in R2.

**r16's "no rule is needed" (:815) is superseded.** Its fact stands: those runs were equal. Its conclusion does not.

**r3's gap (:54-58) closes for census runs.**
- "An operation slower than 5 s would add an observer reading and point" no longer holds in a census run.
- X9-1's disclosure is answered, and the "who owes it" line is discharged by this record.

**Not closed, and not this rule: carry CP-X9-ARMED-TIMER (disclosed residual; LD-Q-233 item 3).** r14 (:636) also files "the
repetition risk of F30's held writer under the unarmed 5 s observer period" under r3's gap, and :1328 forbids "an observer
that ticks on its own timer in a matrix child". Armed rows that do not arm the tick still run the timer (R4), so a slow one
can still disagree on a trace digest in `check`. The duty stays as :636 left it: report it if a run shows it. This record must
not be cited as closing it, or as literal universal compliance with :1328, or as general matrix determinism.

**Leaving it open is lawful; the reviewer confirmed this (REVIEW-r1 §4).** R4 neither creates nor expands the affected
population, and :988 specifies that timer. No run has shown the risk, though that is no proof it cannot occur.

Extending R2 to those rows is not a small step (S7, rejected alternative 4).

## S4. The 10 s bound (checklist item 10: no silent "unchanged")

**What the bound is.** It is sampled. It is not a deadline that expires on its own.
- **A monitored read** (`revocation.rs:170-202`) compares its closing instant with the opening instant of the previous successful
  read, or with its own opening if it is the first (`:73-79`). So read duration and mutex waits count. Over 10 s refuses; exactly
  10 s passes. A successful read replaces the history.
- **An admission-boundary check** (`:204-244`) takes one sample against the opening instant of the read before it. It does not
  refresh the history.
- **So elapsed time is noticed only if a later read or boundary check runs.** No later check means no refusal, however long
  the run took.

**What R2 changes.** Timed observations are monitored reads, so each successful one refreshes the shared history (X4r7 item 2).
R2 removes them. The check is numerically the same, but in a census run only the main thread's reads remain.

| What the same run does today | Under this rule |
|---|---|
| Makes no timed observation | The same observer contribution: one tick per joined guard, no `after-observation`, and no refresh or wall reading removed. This does not mean the run is clean. Other checks can refuse in both versions: an 8 s first read and a checkpoint 4 s after it give a 12 s bracket, with the guard alive under 5 s |
| Makes timed observations, and without them every later check would still be within 10 s | Clean. **This is the fix** |
| Makes timed observations that keep the history fresh, and without them a later check would pass 10 s | Refused, so `HARNESS-ERROR` (R6). **This is the case that gets worse** |
| Takes over 10 s, but reaches no later check | No refusal: R2 cannot notice. Security's fourth operation and storage's refused end are like this (below). Their points stay equal |

**So the rule moves the load limit; it does not remove it.** Today's limit is the 5 s timer against a guard's lifetime. Under
the rule it is 10 s on the bracket between the main thread's successive monitored reads.

**What was measured** (w2A at P, N=20 per condition, all `Committed(latched=false)`; parent-side arrival times):

| Interval | Quiet: min / median / max | Loaded: min / median / max |
|---|---|---|
| A: writer's first record → `x4.checkpoint.before-observation#1` | 3.854 / 4.651 / 5.717 s | 4.716 / 6.912 / **9.765** s |
| Cg: `x4.observer.tick#1` → the same checkpoint | 3.353 / 4.149 / 5.296 s | 4.352 / 6.398 / 8.759 s |

- "Loaded" is `yes` ×18 on 18 CPUs plus a concurrent `cargo test --no-run`.
- **These are proxies for the post-fix bracket, not the bracket.** The first read opens somewhere between A's and Cg's start. The
  bracket closes when the checkpoint's own read closes, after this record. Parent arrival adds lag at both ends. So neither
  figure is an exact 10 s clearance, and neither is a strict bound on it.
- This stretch has no monitored read other than timed ticks: in the accepted 3d2d5b5 trace, 82 object links fall between its
  ends. r2's "173 barrier points" is withdrawn; 82 `x3c.object/link.after` records is the count the reviewer reproduced.

**No existing rule allows anything better:**
- scripting the monotonic clock is forbidden (:1329);
- lifting the bound would weaken the property under test, and L3 keeps its native bound for M6 (:1234);
- item 11 already sets this precedent: "a `HARNESS-ERROR`, never an `OBSERVER.FAIL_STOP` that the run then accepts" (:1249).

**The caller checks are what enforce R6, not `Census::from_exit`,** which does not read semantic outcomes. On paths that can newly
meet a refusal:
- **Storage:** `commit_tests.rs:869-874`, `:909-912`, and recommit's exact unlatched success at `:3518-3527`.
- **Host:** `commit_matrix_tests.rs:941-956`, with the exhausted run's rollover at `:948-950`.
- **Security:** `crash_matrix_census.rs:883-887`.
- **The first read:** its failure propagates before an operation is returned (`operation_handoff.rs:1080-1084`).

**Paths with no later check under R2.** Storage's refused end settles without a checkpoint (`commit_session.rs:1198-1207`), and
security's fourth operation ends without one (`crash_matrix_census.rs:211-214`). The only shared-observation sites after the
first read are the tick and the checkpoint (`operation_guard.rs:603`, `:904`). So under R2 these paths meet no new refusal.

## S5. Effect on the census consumers

The brief and LD-Q-231 name two. **Three census families are affected by the observer,** and they share it, so the fix sits in one
place and no comparison loosens.

| Family | Effect |
|---|---|
| **security** `CENSUS` `("x4.observer.tick", 4, false)` (P `crash_matrix_census.rs:825`; test `:882`, also `:1281`, `:1296`) | **The value stays 4,** now a function of the workload's four operations and not of elapsed time. No `after-observation` row is added. `KILL_SET` is unchanged, because the point is not a durability point |
| **storage** `commit_tests` (`:3770`; also the census parts at `:867`, `:906`, `:3447` and `:3515`, which feed X9-2, -3, -4 and -6's censuses) | The equality test is byte-for-byte unchanged. Accepted evidence: `commit` 1, `refused-end` 1, `recover` and `sweep` 0. The accepted trace predates the `recommit` part, so implementation evidence must cover the current workload |
| **host** `commit_matrix_tests` (`:2238`; `census_run:930`). **Not in the brief; added by LD-Q-233 item 2** | The same latent failure, and the same fix with no host change expected. Accepted evidence: (a) 1, (b) 1, (c) 0. FLAKE7-FIX-1's evidence must include it |

**`Census` consumers the observer does not affect** (excluded by source, REVIEW-r1 NB-2):
- `crates/storage/src/ledger_store/project_commit_census.rs:207-229`: its ledger-only path starts no operation observer;
- platform's self-tests at `crates/platform/src/crash_barrier/self_tests.rs:451` and `:469`: no X4 guard.

If C5 changes `Census::from_exit`, these must still pass.

**Other readers, unchanged.**
- `tools/check_crash_matrix.py` keeps `x4.observer` non-durable, so no kill-set point, row or expected value changes.
- A's accepted census traces at `3d2d5b5…` hold no `x4.observer.after-observation` (counted in all four). So their observer counts
  are compatible with this rule. That is compatibility of this aspect of those bytes, not a fresh run or a qualification at P.
- `two_census_runs_differ_in_raw_bytes_and_agree_when_normalized` (`crash_matrix_census.rs:1121-1126`) spawns with `None`,
  so despite its name it is not a census under R1. It stays on the timer. Its assertions read the outcome and the normalized
  state. The observer writes nothing, and wall data are normalized (:1102).

## S6. Effect on the r3 `HARNESS-ERROR` rule

:56 and :1001 are unchanged and stay as strict as they are: two census runs that disagree are a `HARNESS-ERROR`, never a
smaller kill set. What changes is what a disagreement means. On `x4.observer.*` it can no longer be lawful timing, so it
is a real defect to report. R3 and R6 add two named cases of the same `HARNESS-ERROR`. A `HARNESS-ERROR` under this
rule is not retried and not excluded (LD-Q-230).

## S7. What FLAKE7-FIX-1 must keep (the implementation is w2A's)

**Constraints.**
1. No new environment variable, scope, point, kind, action, label, record member, row, limit or manifest edit.
2. Selection reads only R1's predicate, in the child. `GuardSeam::live()` stays `Cadence::Period(OBSERVER_PERIOD)`
   (`operation_guard.rs:87-90`).
3. R2 is the observer's alone. The generic `gate()` and its `$wait` stay as they are:
   `gate_fallible_and_draw_points_at_protocol_sites` (P `crates/platform/src/crash_barrier/self_tests.rs:623-630`) pins
   `gate=waited` for a nothing-armed child.
4. Any new `cfg` site is added by name to the one pin (P `crates/security/src/crash_matrix_sites.rs:105`; :1042, :1325),
   with a `crash-matrix`-only predicate, never `scenario-fixtures`. The featureless expansion stays exactly the product's
   timed wait.
5. The comment at `operation_guard.rs:586-588` and the census doc at `crash_matrix_census.rs:394` are updated to cite this
   record.
6. C1's stall adds no timed wait to the matrix harness (:974-976, :1311).

**C1, the reproduction (LD-Q-235, LD-Q-236).** One-off evidence, kept out of the lane. It is an empirical control: it shows the
timer's effect where observed at main, and shows its absence after the fix. It does not claim that every positioned stall causes a
second tick at main. A tick can be recorded, and the child stopped, before the observer enters its wait. Its 5 s wait then starts
after SIGCONT, and the guard can end first (`operation_guard.rs:569-600`, `:551-555`). After the fix, the absence of a timed tick
follows from R2's source, not from the stall.

*The run.* QUIET, with no concurrent heavy load. A storage commit census child spawned as `census_run` does (`Some("")`):
1. `await_event("x4.observer.tick#1", "pass")`. The `Record` carries the pid.
2. An external driver sends SIGSTOP, confirms the child is stopped (`ps -o stat=` shows `T`), and tells the test.
3. While the child is stopped, the test takes `N_stop` (the count below) and tells the driver.
4. The driver sends SIGCONT **3.0 s after the stop confirmation** and records that measured interval from its own monotonic clock.
   Counting falls inside the interval, and the child stays stopped until counting ends. If counting overruns 3.0 s, the run is an
   evidence failure.
5. The child finishes. Before any cleanup, the test takes `N_final` in the same directory.

*The stall's derivation.* Long enough that at main the 5 s period elapses inside the guard: over 5 − Cg min (3.353) ≈ 1.65 s. Short
enough that after the fix the bracket stays under 10 s: under 10 − A max (5.717) ≈ 4.28 s. Both are quiet, parent-side proxies
(S4). The window is about (1.7, 4.3) s, and LD-Q-236 sets 3.0 s, superseding LD-Q-233b item 2's "over 5 s". If quiet-condition
drift takes 3.0 s out of the window, report it and do not retune silently.

*The count.* Final regular-file names of exactly 64 lowercase hex characters in `I/stores/S/projects/N/objects/sha256` of this
run's installation, store and namespace, excluding `.opensip-stage-*` (`commit_tests.rs:532-538`, `:1601-1617`;
`project_ledger.rs:327-343`). A positively identified directory that does not exist yet counts 0. A permission error, a failed
entry, an ambiguous namespace, a malformed record or a failed child completion is an **evidence failure,** not zero objects and
not a miss.

*Positioned* requires all of these, from this run alone:
- `N_stop < N_final`;
- this run's trace holds `x4.checkpoint.before-observation#1` explicitly;
- every `x3c.object/link.after` record precedes that checkpoint.

The parent read `tick#1` before asking for the stop, so the stall began after it. An outstanding link at the stop means the main
thread had not passed the checkpoint. The order is proven by these observations alone, with no timing (LD-Q-235 condition 3; the
reviewer verified it for this fresh, sole-writer workload). If a link follows the checkpoint at some head, stop and come back: the
proof needs a different marker.

*Classification. Every run is recorded under exactly one class, at each head:*

| Class | Condition | Treatment |
|---|---|---|
| **Miss** | Not positioned (`N_stop == N_final` is a conservative miss) | Discarded and counted, never scored as a pass |
| **Evidence failure** | As under "The count" | Retained; neither a miss nor a pass |
| **Reproduced** (main only) | Positioned, and the run shows a second `x4.observer.tick` and an `after-observation` | The FAIL at main |
| **Positioned, not reproduced** (main only) | Positioned, and the run shows one tick | **Retained and reported. Not a miss, not discarded and not re-tried away** |
| **Passed** (after the fix only) | Positioned, one tick, no `after-observation`, and the census equal to an unstalled run's | The PASS |
| **Positioned, failed** (after the fix only) | Positioned, with any other result | Retained with its actual outcome and diagnostics. It counts as R6 only if the outcome is an actual bound refusal |

*Requirements.*
- At least 3 **Reproduced** runs at main (LD-Q-236: a hit at main is the order proof plus the observed second tick).
- At least 3 positioned runs after the fix, **all of them Passed.**
- All counts are reported at each head. The classes are not selected by the desired result.
- If more than about 50 attempts per head would be needed, stop and go to the coordinator. Do not weaken the proof.
- **An unstalled arm at each head,** under the same quiet condition, N at least equal to the stalled attempts, with its tick counts.
  Quiet Cg can reach about 5.3 s by itself, so a second tick at main is evidence about the stall only beside this arm.

**The other controls.**
- **C2, a real refusal.** After the fix, a storage commit census child, which necessarily reaches a later checkpoint, stalled so
  that a bracket passes 10 s, ends as a `HARNESS-ERROR`. The refusal evidence is retained. One-off evidence is enough. Refused-end
  and security's fourth operation cannot serve (S4).
- **C3, production.** The pin at `operation_guard_tests.rs:253-254` passes unchanged. Item 2's release-absence and feature-boundary
  evidence is produced and named (:937-940).
- **C4, precision.** The predicate is true only for a present, empty arming, shown across absent, empty, tick-armed and other-armed.
  Tick-armed rows behave as before. A child armed with one main-thread `hold` in that stretch, held over 5 s and clearly under 10 s,
  shows the second `tick` and an `after-observation` both at main and after the fix (R4). The over-5 s hold stands here: the
  observer keeps running during a hold and refreshes the history. C4 does not prove the nothing-armed case.
- **C5, R3.** A census holding `x4.observer.after-observation` is refused. `Census::from_exit` is the natural place, since all three
  families pass through it. This does not prove once-per-guard (security's pin does that for its workload) or R6 (the caller checks
  do).
- **C6, repetition.** LD-Q-231 step 4 over all three families on the current workload (including `recommit`), with every failure
  retained and no retries, and any R6 outcome reported separately.

None of these has run for this record.

**Rejected alternatives.**
1. **Excluding the observer's counts from equality** (remedy 2) loosens the law's comparison (LD-Q-231).
2. **Arming the gate in the census** (remedy 3) contradicts "nothing armed" (:514, :524; LD-Q-231).
3. **Silent timed observations with no points.** It keeps the freshness refresh and hides the timer. Those observations
   would still shift wall readings by elapsed time and could latch, and it is the "timed tick" the brief excludes. w2A's loaded data
   make the refresh worth more than r1 assumed. LD-Q-236 handles load at LT-4 and keeps this rule, so this stays rejected.
4. **R2 for every child that does not arm the tick** (it would also close :636 and :1328). Held rows rely on the timer's
   refresh: F30's or F06's writer held past 10 s would fail-stop on resume, where today the observer keeps it fresh. It
   would need item 11's timing guard extended to those rows, which is more law than this rule.
5. **A scripted monotonic clock,** forbidden by :1329.
6. **A census-only environment variable,** which widens the closed list at :948 for no gain over R1.

## S8. The coordinator's rulings (LD-Q-233, LD-Q-235, LD-Q-236)

1. **The residual load limit (S4), for the reviewer to score.** Under this rule a monitored-read bracket over 10 s stays red, where a
   later check exists to see it. So "N≥20 under concurrent load: all equal" (LD-Q-231 step 4) holds only for load that keeps those
   brackets within 10 s. Loaded parent-side A reached 9.765 s, and the proxies do not establish a margin at that load.
   **Ruling (LD-Q-236 item 2), the coordinator's call and not part of this rule:**
   - LT-4 includes the storage and host census targets, run under the lane lock with the load rule in force (OD-PROC-1).
   - LT-4 records the load average at the start and end of that step, and the largest measured gap if available.
   - A gap over 10 s stays red as a `HARNESS-ERROR`, is never retried automatically, and goes to the coordinator with the load figures.
   - It is not a named deferral for now, and it is revisited if red lanes occur under the load rule.
   - The ruling cites a quiet margin of about 4.3 s. By S4 that is a proxy margin, not an exact clearance.
2. **:636 and :1328 stay open (S3). Ruling:** agreed, as carry CP-X9-ARMED-TIMER, which the coordinator registers.
3. **Three consumers (S5). Ruling:** host's `commit_matrix_tests:2238` joins FLAKE7-FIX-1's evidence.
4. **The predicate's reach (S2). Ruling:** fine, with the reviewer re-deriving the scan, which it did.
5. **C1's form (S7). Rulings:** LD-Q-235 accepts a self-checked hit, on binding conditions. LD-Q-236 sets the 3.0 s stall, run quiet,
   with a hit at main being the order proof plus the observed second tick. **This record adds one thing for the coordinator to confirm
   by adopting it:** RF-1 requires that a positioned run at main with no second tick is kept. So S7 calls such a run "Positioned, not
   reproduced": not a hit under LD-Q-236, and not a miss under LD-Q-235 either.

## S9. Binding clause (not done by this record)

On adoption, X9's next revision carries, or the receipt binds, these exact texts. Accepted bytes are not edited.
- **After :988's "Unarmed, the product's 5 s period is unchanged.":** "In a census run (X9-SUCCESSOR-CADENCE R1) there is
  no timed wait: the observer waits only for `Stop`."
- **After :951's "… is unchanged.":** "X9-SUCCESSOR-CADENCE: a census run does not run the observer's 5 s period, so it makes no timed
  observation; the 10 s check stays native, and applies at the reads and boundary checks that remain."
- **After :1001:** "X9-SUCCESSOR-CADENCE: `x4.observer.tick` occurs once per guard and `x4.observer.after-observation`
  not at all; a census holding it, or a census child refused by the 10 s bound, is a `HARNESS-ERROR`."
- **Status notes:** at :58, "Closed for census runs by X9-SUCCESSOR-CADENCE"; at :815, "Superseded by
  X9-SUCCESSOR-CADENCE; the runs' equality stands"; at :636 and :1328, "Not closed by X9-SUCCESSOR-CADENCE; carry
  CP-X9-ARMED-TIMER".

The product change, its inventory successor and its evidence are FLAKE7-FIX-1's.

**Unchanged:** every other injection mechanism, point, kind, scope, label, evidence member, row, expected value, limit and
forbidden substitute of X9; X4's production law and its numerical and native checks, though census observation behaviour changes
under R2 as S4 states; and every accepted outcome of any other law.

## S10. Self-review (checklist v4)

**Applicable.**
- **5, immutable pins:** pins are to A and P commits and digests of locked or reviewed bytes. `REVIEW-r1.md` is pinned as its final
  bytes after the reviewer went idle (item 24), and a locked copy is in the review inputs.
- **6, provenance:** every time in S4 and S7 is w2A's and labelled parent-side. No native bracket is claimed, and the derivation
  names its inputs.
- **7, failure latching:** a bound refusal latches as it does today. This rule does not change that.
- **8, disclosure:** S2 (implicit children, R3's scope), S3 (the carry), S4 (proxies, the worsened case, paths with no later check),
  S5 (the third family, unaffected consumers), S7 C1 (empirical, a raced trigger, positioned runs that do not reproduce).
- **9, mutations:** the row-level controls are the implementer's. C1's classes are built so that a false hit cannot score as a pass.
- **10, no silent unchanged:** S4 gives the timing change case by case.
- **11, sound over tight:** R6 and the conservative miss are plainly conservative.
- **16, custody:** this record and the inputs are locked read-only before the request.
- **17, name every deferral:** all controls are named as not yet run, and S8 records LT-4's terms.
- **18, evidence location:** everything is under the cache.
- **19, pins in shared files:** no file is edited here. S7 names the pins the implementer meets: `crash_matrix_sites.rs`,
  `operation_guard_tests.rs:253`, `crash_matrix_census.rs:825`. `the_crash_points_are_the_laws_names_in_registered_scopes`
  also pins the macro text at `operation_guard_tests.rs:258-269`.
- **22, head identity:** A and P are named. The route is `R3-FRONTIER`, preflight `ROUTE-OK`.
- **24, hash when final:** the digest is taken after locking.
- **26, emitter-coupled artifacts:** none changes (S5); the census values stay the same.
- **28, pinned tool:** my row scan was a heuristic, and it undercounted (NB-1). S2 now rests on the reviewer's re-derivation.
- **29, look at the pane:** done before sending. Long pane messages truncate, so messages go as a file, then the path and sha256.

**N/A.**
- **1-4, 12-14:** no pricing, funding, system-call or schema-table work.
- **15:** no frozen state machine.
- **20, 21:** no product build or base move here.
- **23:** no lock or temp lookups.
- **25:** no refresh or re-pin script.
- **27:** no type-size bound.
