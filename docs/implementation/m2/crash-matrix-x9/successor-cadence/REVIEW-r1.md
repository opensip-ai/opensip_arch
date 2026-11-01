# X9-CADENCE independent review r1

X9-CADENCE: REJECT

The proposed census-only cadence is a viable narrow successor. The submitted record is not adoptable as written: C1's timing classifier does not establish its claimed precondition, and S4's case table overstates what the unchanged monitor detects. These are RF-1 and RF-2 below. No wider cadence rule is recommended.

## Subject, authority and checks

- Request: `REQUEST-r1.md`, SHA-256 `fbab2e8037c09d22effc9b6a496363b317a0728f7a0443d8f7223c85a6546f6a`.
- Subject: `inputs/X9-SUCCESSOR-CADENCE-r2.md`, SHA-256 `69b3027bf297a8afc55f26d5d6c4bfd3e1cffeb5f9e0669fc9c1a63f6b4e8a83`.
- All 17 members of `inputs/SHA256SUMS` verified, resolving names relative to `inputs/`. Request, manifest and members have mode 0444. The initial checksum invocation from the review root could not resolve the manifest-relative names; the corrected invocation from `inputs/` verified every member. No input was changed.
- A = `/Users/sb/code/opensip-ai/opensip_arch`, HEAD `5f328f32dc5fe026d0b044c487b1d2070ec4b863`; P = `/Users/sb/code/opensip-ai/opensip`, HEAD `fe379d218358d3193073db3f037b062713a258f2`. Both match the request. Tracked status is clean in both.
- Read the bootstrap orientation/status/routing documents and current control state. CURRENT-STATE's live queue LD-Q-233 selects this R3 review; LD-Q-235 selects r2 and records the coordinator's acceptance of the proposed C1 classification. That acceptance does not establish the classifier's technical soundness. Older execution checkpoints are historical under OD-PROC-1.
- Preflight: `python3 -I -B A/tools/agent_model_route.py check --provider codex --route R3-FRONTIER` returned `ROUTE-OK R3-FRONTIER codex gpt-6-astra/high` before substantive review. Claude-authored subject, Codex independent review.
- Law digests verified: X9 `7a37a16f664dfd110e4ce0cac5f5ce8e27b15eee72a9881a7a8f6080862e8a15`; X4r7 `fc8490f4e751e486bc4cf6dc15e04eb541672112bda2eab8c15759c31eaf0224`; X4r8 `bb2fd6a4b97ceaee33629b7103cdf515dc19073ad1da7734891f2d13d84af16b`.

References below are to these exact working-tree bytes. X9 means A `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`; X4r7 and X4 mean A `docs/implementation/m2/live-guards-x4/PROPOSAL-r7.md` and `PROPOSAL.md`. Product references are relative to P. This is source/law review with read-only JSON/trace analysis, not a product test, timing experiment, adoption, implementation, integration, lane or qualification result.

## Required findings

### RF-1 — C1 does not prove the stop was in the gap, nor make a scored baseline run deterministic

Subject lines 191–198 adopt the method at `inputs/REPLY-TO-W2A-r1.md:22–38`. Its decisive implication is false: taking at least six seconds to return from `await_event` does not prove the checkpoint record was emitted after SIGCONT.

`crates/platform/src/crash_barrier/driver.rs:226–227` merely starts a stderr reader. The reader blocks/reads/parses/sends at :422–440; the parent consumes the queue and searches records at :263–315. There is no scheduling bound, drain acknowledgement, emission timestamp or ordering proof relative to SIGSTOP/SIGCONT. A checkpoint record can already be in the pipe when the child stops, while the reader is descheduled for six seconds. Alternatively the parent can be descheduled during the measured call even with a queued record. Either execution satisfies the proposed hit test although the stop missed the specified gap. Counting misses and requiring three hits does not repair false-positive hits.

There is a second independent race even for a real hit. The observer reports `tick#1` before invoking its wait: `crates/platform/src/crash_barrier.rs:544–549,806–811` and `crates/security/src/custody/operation_guard.rs:590–600`. SIGSTOP can stop the entire child after that record but before `recv_timeout` begins (:569–575). After SIGCONT, its five-second wait can begin afresh and the guard can finish normally first. A stop while already waiting also gives no source-level guarantee that the observer executes its observation before the main thread finishes and sends Stop (:551–555). Thus a verified six-second suspension in the gap does not entail the promised second tick/after-observation on main. These are source-order counterexamples, not claimed observed runs.

**Required correction:** replace the latency-based proof with a reviewed method establishing the child's position independently of reader/parent scheduling, and distinguish that position proof from proof that a baseline timed observation actually occurred. Alternatively revise C1's claim and obtain the coordinator's disposition of a weaker empirical control. Do not discard a correctly positioned baseline that stays clean as a mere missed trigger, or select hits by the desired failure. Keep failures and all classifications in the record. Three repeats, a longer sleep, or the armed C4 form cannot establish the missing implication. This review does not authorize instrumentation, new points or wider R1 scope.

### RF-2 — State the bound's actual sampling interval and remove unconditional outcomes from S4

Subject :120–129 is not a correct exhaustive case table. The monitor is sampled, not an independently expiring ten-second deadline. `crates/security/src/revocation.rs:170–202` evaluates the bound only when a read completes; :73–79 compares the current read's latest closing instant against the previous successful read's earliest opening instant (or the current opening for the first read). The admission boundary also samples and checks against that earliest instant (:204–244). Equality at ten seconds is allowed; greater than ten seconds refuses. Read duration, mutex delay and the boundary interval matter, not just idle time between callbacks or record-arrival times.

Two concrete counterexamples to the table:

1. A successful initial read can consume eight seconds before the guard starts; a later checkpoint can finish four seconds after that opening read completed. The guard's lifetime can still be below five seconds, with no observer timeout, while the next bracket spans twelve seconds and refuses in BOTH versions. The initial read precedes guard construction (`custody/operation_handoff.rs:1038–1084`; `operation_guard.rs:643–675`). Consequently “every guard ends within 5 s → clean” is not valid. The useful narrower claim is preservation of observer behavior when the baseline makes no timed observation, not unconditional success.
2. Starving the observer beyond ten seconds does not necessarily fail-stop after R2. Security's fourth census operation starts, reads its carrier data and ends without a checkpoint (`crash_matrix_census.rs:211–214`). Its end drops the guard (`operation_handoff.rs:605–618`), whose observer is stopped and joined. Once its initial read succeeded, a long pause before that end supplies no later monitored read to detect the elapsed time under R2. Storage's refused-end path has the same absence of a later observation, which S4 itself acknowledges. Conversely, starvation of the observer alone need not cause a stale history today if checkpoints keep refreshing the shared monitor. The table's last row cannot promise fail-stop in either version without additional premises.

**Required correction:** describe the exact native read/boundary intervals, preserve R6 as “an actual bound-induced refusal is a harness error,” and qualify the case table by the existence of a later bound check, successful other prerequisites, and actual baseline timed observations. C2 must select a workload that necessarily reaches a later monitored check. Do not describe the ten-second rule as a lifetime watchdog or claim every slow census becomes red. Carry this precision into S8's load assessment. `inputs/REQUEST-W2A-EVIDENCE-r1.md:24–30` asks for parent first-record-to-before-checkpoint times and explicitly admits both overstatement and understatement: those are useful proxies, not the native interval checked by `bounded_read`, and must not become an exact ten-second clearance threshold. No bound increase or monotonic-clock scripting is needed to correct this record.

## Answers to the seven review questions

### 1. R1–R6 and the census gap

The intended change is a LAW-CHANGE, as LD-Q-232 corrected, rather than an implementation of already-selected scripted cadence. X9 :54–58 expressly leaves the timer running, :988 preserves it for unarmed gates, and :815 records the earlier decision that no rule was needed. A prospectively adopted, feature-only exception can supersede those census passages while preserving X4's production cadence. X9 already distinguishes an armed test gate from production, so this does not require changing the production five-second constant.

R1 matches `Census::from_exit`'s present/traced and empty-arming predicate (`driver.rs:563–569`). R2 removes the loop's only timed wake; its Stop return precedes observation (`operation_guard.rs:596–606`). It therefore closes the named elapsed-time observer-count gap for normally completed census workloads. It does not prove every source of census nondeterminism absent or every loaded run successful. R4 keeps nonempty other-arm children on the old timer. R5 keeps `GuardSeam::live` and featureless production unchanged. R6's refusal policy is sound with RF-2's precision.

For **R3's once-per-guard obligation**, a successfully started observer enters the gate before examining Stop; normal guard destruction sends Stop and joins, even if the observer had not yet been scheduled (:551–555,584–600,668–684). With R2 there is no second iteration. Current selected census paths do not leave a started guard alive at process exit: security consumes all four operations through `end` (:177–214); storage commit consumes its stopped session through `finish` (`tests/commit_tests.rs:175–181,187–219,260–291`); host's candidate explicitly finishes (:225–229), and finalize uses the same production session lifecycle. Recover/sweep do not start an X4 operation guard. Failed starts are not successfully started guards. This argument depends on normal completion/join, not thread fairness before main-thread completion. It is not a theorem about killed, leaked or harness-aborted children. The deliberate F42 `mem::forget` child is armed with `x3c.evidence.commit.before#1=fail-before` and therefore outside R1.

### 2. Item 3 and the exact narrowing

R2 scripts no clock reading. Native monotonic/boot observations remain at `crates/platform/src/clock.rs:68–87`; only the wall component is selected by `scripted_wall`. X9 :1329 remains satisfied. The five-second observer cadence clause in :951 must acquire the R1-only exception; the native numerical ten-second check and admission-boundary check remain unchanged, but their observation opportunities and history refreshes change. S3 identifies the main distinction correctly; RF-2 supplies the missing operational precision. Removing timed reads also removes their increments of the scripted wall-reading ordinal. That supports the intended deterministic census, rather than proving a general “only script and product” property under arbitrary failure/scheduling conditions.

### 3. Load limit, preservation and consumers' refusal behavior

The important adverse case is real: a slow baseline can refresh through timed observations and pass, whereas a later checkpoint after R2 can refuse because the previous successful read is now too old. Rejecting that census rather than retrying or shrinking its kill set is the right policy. LD-Q-233's separate LT-4 load/deferral decision is appropriate; no timing numbers or installation clearance exist in this package.

For a completed baseline with **no actual timed observation**, R2 removes no successful monitor refresh or wall reading, so the ordinary observer contribution remains one tick per joined guard and no after-observation. I found no semantic counterexample to that bounded preservation claim. It is not a cross-run scheduling guarantee and does not imply “clean”: other native bounds can already fail, as RF-2 shows.

Current relevant outcome checks reject bound-caused failure on paths that can newly encounter it: storage's commit expectations at `tests/commit_tests.rs:869–874,909–912`, recommit exact unlatched successes at :3518–3527; host lawful/store-GC preparation at `tests/commit_matrix_tests.rs:941–956`; security's expected integrated outcome at `crash_matrix_census.rs:883–887`. Host exhausted requires its specific rollover at :948–950. Initial trust-read failures propagate before an operation is returned (`operation_handoff.rs:1080–1084`). The generic `Census::from_exit` itself does not inspect semantic outcomes, so these caller checks must not be replaced by a claim that it universally enforces R6.

The **refused-end caveat is confirmed for R2**: storage :214–219 takes `reserve_end_path`/`refused`/`finish`; `custody/commit_session.rs:541–555` reserves, :606–607 refuses, and :1198–1207 explicitly specifies settlement without a checkpoint. The only subsequent shared-observation sites are the observer and checkpoint (`operation_guard.rs:603,904`). With the former disabled and the latter absent, no later freshness check occurs. Its accepted trace has no checkpoint, corroborating the source. The literal claim that it makes no later read is false on an arbitrarily slow baseline while the timer remains enabled. Under R2 this is a vacuous absence of a new bound refusal, not proof of a ten-second watchdog. Security's integrated census similarly passes `_checkpoint` unused in its append callback (:130–150).

### 4. CP-X9-ARMED-TIMER

Leaving this existing residual open is acceptable for this bounded successor. X9 :636 explicitly records F30's repetition risk, :988 specifies the unarmed gate timer, and :1328 retains the broad forbidden-substitute sentence. R4 neither creates nor expands the affected armed-other population. LD-Q-233 expressly retains the carry. The record must preserve the specific residual and its report-if-observed duty; it must not claim literal universal compliance with :1328 or general matrix determinism. An absence of observed failures is not a proof that the risk cannot occur. Closing it would be additional law and is not required to narrow the census defect.

### 5. Re-derived R1 reach

I reran the pinned heuristic and independently parsed the required JSON with the interpreters' lifecycle/arming rules in view.

- Storage: 403 rows; 216 explicit spawns = 121 empty + 52 other-arm + 43 tick-arm. Empty roles are reader 11, revoke 42, commit 32, sweep 18, competitor-writer 2, recover 16. Tracking children until actual `finish` (rather than assuming any await finishes them) finds no intervening `mutate`, and no such child left live at script end. Publication children are themselves included in the roles above. The scan's three revocation rows plus two omitted `ObserverFailStop` rows all tick-arm the affected writer (NB-1).
- The scan omits storage's implicit children: simple-script mutation bases use `finished("commit", "", "")` at :1960–1964, mutations follow that exit, and ladder/next-writer children also run without arming. I found no selected expected revocation/observer outcome requiring one of their autonomous ticks. They remain subject to RF-2's changed native-failure opportunities; this is not an all-load outcome-equivalence claim.
- Host: 102 rows. Arms accumulate in separate steps and are consumed/reset at each `run` (`tests/commit_matrix_tests.rs:1584–1620`). Re-derivation gives finalize 8 empty / 92 other / 2 tick, and store-GC 11 empty / 2 other. Every row also makes a completed empty-armed candidate child (:1558–1560,668–693). Only F39 `latched-after-admission-delivery` and F40 `latched-fail-after-evidence-commit` use the observer; both arm `tick#*=hold`, publish and explicitly resume the observer. Ordinary `run` children finish before later mutation steps; the two special concurrent publication sequences retain tick arming. No required value found depends intentionally on a nothing-armed child's periodic observation.

These checks support the predicate choice without broadening it to every child whose arms omit the tick.

### 6. Consumers and accepted values

There are three **observer-affected census families**, not exactly three `Census` consumers in the repository (NB-2). Security's pin remains `(x4.observer.tick, 4, false)` at :825 and its kill set remains 437 at :870. The point is read-only (`crates/platform/src/crash_barrier.rs:169`); kill selection filters durability (`driver.rs:598–606`). No kill-set relaxation, expected-value rewrite or row removal is warranted.

I read all four cited accepted trace files under A `docs/implementation/m2/crash-matrix-x9/evidence/3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f/`: storage commit and refused-end each have one tick; recover/sweep none; host a/b one each and c none; none has after-observation. These observer counts are compatible with R2. That establishes compatibility of this aspect of those historical bytes, not fresh execution, new emitter-closure identity or qualification at P. Current storage additionally includes recommit (:3491–3545); the cited historical storage trace has no recommit part. Implementation evidence must cover the current workload.

The `spawn(None)` normalization test at security :1121–1130 remains outside R1 and on the production timer, as S5 says.

### 7. Binding and controls

S9 correctly calls for prospective successor/receipt binding rather than rewriting accepted bytes. Its :988 and :951 exceptions, :1001 census counts/refusal policy, and :58/:815/:636 status notes identify the relevant passages. Bind the exact reviewed successor and preserve the :1328 carry explicitly. Interpret “all of X4 unchanged” as production law and numerical/native checks, subject to the explicitly selected test-cadence exception; it cannot mean unchanged census observation behavior. Resolve RF-2 before copying the load assertions into any receipt.

C1 requires RF-1 correction. C2 is useful only with a guaranteed subsequent native check and retained refusal evidence. C3 correctly preserves the constant/live-seam pin (`operation_guard_tests.rs:253–254`) but also needs the named release-absence/feature-boundary evidence. C4 is the right precision control and must remain separate from the census PASS reproduction. C5's proposed common `Census::from_exit` rejection of after-observation is sensible; it does not alone prove one tick per started guard or semantic R6 checks. C6 needs all three affected families with failures retained and no retries. None of these controls has run for this record.

The observer-only implementation constraint is important: platform's generic gate control expects `gate=waited` for an empty arming (`crash_barrier/self_tests.rs:623–630`). The named feature-site/source pins must be updated deliberately; production must continue to use `Cadence::Period(OBSERVER_PERIOD)`.

## Non-blocking notes

- **NB-1 — Correct the evidence counts.** S2 :72–75 says three expected revocation/observer rows; the scan's case-sensitive `OBSERVER` / `observer-fail-stop` search misses CamelCase `ObserverFailStop`. There are five: F18 revoked/unreadable, F19 revoked/unreadable, F38 revoked; all five arm the tick. Also the quoted 173-point stretch is not reproduced from the cited trace: its commit tick is line 177 and first before-observation checkpoint line 1039, with 861 intervening records and 43 distinct point names. There is no direct first-monitored-read timestamp/marker in that trace. Supply the counting rule and exact endpoints or withdraw 173; it is not a timing or hit-rate argument.
- **NB-2 — Qualify “three consumers.”** `crates/storage/src/ledger_store/project_commit_census.rs:207–229` also consumes `Census::from_exit`; its ledger-only stand-in path (:27–50) starts no operation observer. Platform self-tests consume it at :451 and :469 without an X4 guard. These are unaffected consumers, not missing fourth/fifth observer cadence fixes. Include them as excluded-by-source inventory entries, especially if C5 changes the common parser.

## Disposition

Revise the control proof and the bound case table in a new subject, retaining this review and the frozen inputs. The narrow cadence direction, unchanged production clock/cadence, unchanged selected expected values and named armed-timer residual can be retained. No adoption receipt, product change, native run, LT-4 installation or qualification is authorized by this review.

## Supplemental assessment of ADDENDUM-r1 (2026-11-01)

This section is appended to the completed review; its preceding text is preserved. The original review's SHA-256 before this append was `654759fc32c0818f2546ad4d2a04a836438d496f3fbd8bfe9b332d1d7551145d`. The score above remains unchanged. The replacement method resolves RF-1's reliance on stderr-reader latency in principle, but does not resolve RF-1's separate baseline-observer scheduling counterexample. RF-2 is not addressed by the addendum.

**Additional pinned inputs verified:**

- `ADDENDUM-r1.md`: `64dd3306a2df3ccd0505c6e4bfd8fae277bc3210332c3d249172e67dfd78afda`.
- `../REPLY-TO-W2A-r2.md`: `af5f37e0a2158d760fd3b233f744cf562a53ee73265ffa93e41c45226fb92e99`.
- `../../coordinator/msg-ldq235.txt`: `58e99276b4b4f344118c35a8643ceca7b10e026dee064caa86b810469cdd6260`.

All three have mode 0444. Both repository HEADs still match A and P above. The repeated R3 preflight returned the same ROUTE-OK result. The current queue confirms LD-Q-235. This assessment scores the supplied replacement method, not the withdrawn latency classifier. No stall, child, product test or object-store experiment was executed.

### The object count can establish position, with an exact counting contract

The layout is readable in principle. The directory to count is the fixture's **`I/stores/S/projects/N/objects/sha256`**, from the same installation/store/namespace for both samples. It is not the trust store, every object directory beneath the scratch root, or the namespace under `I/host/projects`. The path construction is `crates/storage/tests/commit_tests.rs:532–538`; object-directory creation is `crates/storage/src/ledger_store/project_ledger.rs:327–343`.

Count final regular-file names matching exactly 64 lowercase hexadecimal characters, excluding `.opensip-stage-*`. The existing name filter is illustrated at `tests/commit_tests.rs:1601–1617`. `blob_store.rs:78–82` publishes under `digest_hex`; `project_commit.rs:247–255` rejects duplicate declarations and :265–285 publishes the objects serially. Platform's `link` point wraps an exclusive rename of the staging name to the final name (`crates/platform/src/filesystem.rs:577–590,650–660`). Thus a final name is visible before its `link.after` record; a final name is not contingent on the later directory barrier or on the reader draining stderr.

For this fresh, sole-writer census, the corrected proof is:

1. Reading this child's `tick#1` before requesting SIGSTOP establishes that the tick record was emitted before the suspension, regardless of pipe latency.
2. A complete count while the child remains stopped, followed by a greater complete count in the same directory at its end, establishes that at least one final publication remained outstanding at the stopped snapshot. This requires excluding other writers, deletion, directory substitution and cleanup; the ordinary fresh census supplies that isolated workload, not arbitrary runs at arbitrary future heads.
3. In a valid complete trace, if the first checkpoint exists and every corresponding object publication's `link.after` precedes it, that outstanding publication places the stopped snapshot before the first checkpoint. The main thread could not already have passed that checkpoint. The child does not advance through the checkpoint during its suspension, so the controlled wait remains before it too.

I independently counted the cited historical **commit** trace: 82 link-after records, all between tick line 177 and checkpoint line 1039; first and last link-after are lines 222 and 1032. That verifies the historical ordering claim, not a required count at P. The new run must supply its own complete trace, checkpoint and counts as r2 proposes.

The implementer's counting contract must distinguish a positively identified, not-yet-created object directory from an unreadable or wrongly resolved one. Permission errors, failed directory entries, ambiguous namespace selection, malformed records and failed child completion are evidence failures, not zero objects or ordinary misses. Checkpoint presence must be explicit rather than relying on a vacuous “every link precedes it.” A stopping snapshot with `N_stop == N_final` can conservatively be a miss even when the main thread has not yet reached the checkpoint. No contents need be read or modified for this position proof. These details close the author's disclosed layout uncertainty at source level; they are still to be implemented and verified in the reproduction.

### RF-1 remains open: position is not proof of a baseline timed observation

The same concrete counterexample survives the stronger classifier. The observer emits `tick#1`, then is descheduled before entering `recv_timeout`. The parent reads that record and stops the child before its objects are all published. The stopped count is smaller than the final count, and all subsequent links precede checkpoint #1: **this is a true hit under the new ordering proof**. After SIGCONT the observer starts its five-second wait; the main thread can complete the remaining publication/checkpoints and destroy the guard before that wait expires. The baseline then has one tick and no after-observation, despite a correctly located 6.5-second suspension. Source ordering is `operation_guard.rs:569–600`, with Stop/join at :551–555.

Consequently r2 :41–43 still cannot promise its baseline signature on every correctly classified hit. Retain such a clean baseline as a hit whose expected reproduction did not occur; do not reclassify it as a miss or discard it in pursuit of three failures. Either establish the additional wait/observation precondition by a separately reviewed method within the existing constraints, or obtain a coordinator disposition that accurately limits C1 to empirical reproduction rather than the asserted implication. C4 remains useful independent evidence but does not prove the nothing-armed case. LD-Q-235's approval of self-checked hits does not supply this missing scheduling fact.

### Remaining text corrections

- RF-1's original latency-classifier objection is superseded for this supplemental method, conditional on the exact count/trace contract above. Its baseline-race objection remains. RF-2, the numerical evidence notes and the other original dispositions remain as recorded.
- r2 :44 incorrectly attributes **any** unlawful after-fix outcome to a gap exceeding ten seconds. An I/O, custody, malformed-trace or other failure need not be a freshness stall. Preserve the actual outcome and diagnostics; classify R6 only from the actual bound-caused refusal. Recording it as neither pass nor discard is correct.
- The recorded stop-confirmed-to-SIGCONT duration includes counting/FIFO delay before the driver's 6.5-second wait. The counter protocol must keep the child stopped until counting completes, and retain the measured interval; a nominal sleep duration alone is insufficient. That interval still does not establish the whole monitored-read bracket addressed by RF-2.
- The next subject must replace S7's stale method pointer and hash with the exact method ultimately reviewed, or an adoption receipt must expressly bind that exact replacement and the superseded passage. The supplied addendum identifies the replacement for this review; unchanged r2 bytes alone still refer implementers to the withdrawn method. Do not edit the frozen r2 input in place.

The object-count approach is therefore a sound direction for position evidence on the pinned isolated workload, not a completed C1 control or a resolution of the review's rejection.
