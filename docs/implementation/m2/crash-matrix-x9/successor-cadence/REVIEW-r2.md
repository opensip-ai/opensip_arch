# X9-CADENCE independent review r2

X9-CADENCE: ADOPTABLE

The r3 record resolves the two required findings as a prospective law/control specification. C1 no longer promises that every positioned suspension produces a baseline tick; all positioned non-reproductions remain evidence. R6 now preserves the sampled native bound without inventing an expiring deadline. There are no required findings in this round. The non-blocking notes below delimit the evidence claims; none establishes execution or installation readiness.

## Identity and scope

- Request SHA-256: `9deb1c198ebeb7429756858ba6ca7e3a7553a6e0f900b2cf38bba07e5f774d77`.
- Subject `inputs/X9-SUCCESSOR-CADENCE-r3.md`: `12e9b8d12ec06739b174d0f8e5eed01a8b3697d7f2f65beeb470248a400cb85a`.
- Manifest `inputs/SHA256SUMS`: `d96c9614c250a1b09b9acd14fc003afaebc592cfc60396c5b955bb5dd728dce4`; all 13 members verify, and every input file is non-writable. The request and manifest are mode 0444.
- A = `/Users/sb/code/opensip-ai/opensip_arch`, HEAD `5f328f32dc5fe026d0b044c487b1d2070ec4b863`; P = `/Users/sb/code/opensip-ai/opensip`, HEAD `fe379d218358d3193073db3f037b062713a258f2`. Both match the request and have clean tracked status. The three law-file digests remain those verified in round 1.
- The original `../REVIEW-r1.md` remains unchanged at `ebb2df7d59b0834fa161960e0bd418c841585a33508f61108f1406890e87a1d3`; its pinned copy includes the supplemental assessment. This verdict applies to r3, not retrospectively to the rejected r2.
- Current control decisions LD-Q-233, LD-Q-235 and LD-Q-236 agree with the request and pinned messages. Preflight again returned `ROUTE-OK R3-FRONTIER codex gpt-6-astra/high`. Claude-authored subject, Codex independent review.

This review verified hashes, compared rule text, inspected pinned source and checked arithmetic. It did not run product tests, stall a child, inspect an actual run's object store, rerun the measurement, or modify either checkout. Product references below are relative to P; subject references are line numbers in r3. The original review supplies the unchanged law/reachability audit at these same Git pins.

## 1. RF-1: position, classification and the empirical claim

**Resolved for this specification.** The counting contract at subject :247–261 incorporates the exact directory, final regular-file/64-lowercase-hex filter, exclusion of staging, explicit checkpoint presence, same-run ordering, and evidence-failure treatment for unreadable or ambiguous observations.

The source connection is sound for the named fresh, sole-writer workload: `crates/storage/tests/commit_tests.rs:532–538` selects `I/stores/S/projects/N`; `ledger_store/project_ledger.rs:327–343` creates its `objects/sha256`; `blob_store.rs:78–82` publishes digest names; `ledger_store/project_commit.rs:247–275` rejects duplicates and publishes serially. `crates/platform/src/filesystem.rs:577–590` brackets exclusive publication with the link point. Final-name visibility precedes `link.after`. With no competing mutation/cleanup, a smaller stopped count means a final publication remains outstanding; the complete trace places that publication before checkpoint #1. Reading tick #1 before requesting the stop supplies the other endpoint. This does not depend on how promptly the reader drains stderr.

The position proof alone still does not establish a timed observation. Subject :227–231 now states the precise counterexample: the observer can emit its first tick before beginning `recv_timeout`, so a stopped child can resume into a fresh five-second wait and finish first. This matches `operation_guard.rs:569–600` and its Stop/join path at :551–555. The new record no longer relies on the false implication.

The classes at :263–278 retain a positioned clean baseline as **Positioned, not reproduced**. Requiring at least three **Reproduced** baseline witnesses is acceptable for an empirical existence/reproduction control when every attempt and every class remains reported. It does not permit computing a success rate from the reproduced subset, calling non-reproductions misses, or presenting the selected three as the whole experiment. The after-fix rule is stronger: every positioned run must pass, not merely the first three successes. Evidence failures must remain outside passes and misses, with diagnostics retained.

S8 item 5 correctly identifies the reconciliation with LD-Q-235/236 as something the coordinator confirms through adoption. The distinct position and reproduction classifications satisfy the prior review's requirement; they do not contradict the coordinator's narrower use of “hit.” The record's explicit empirical limitation is accurate. See NB-2 for what the unstalled comparison can establish.

## 2. RF-2: sampling, R6 and the four timing cases

**Resolved as a bound-policy correction.** R1 through R5 compare byte-for-byte equal between the pinned r2 and r3 blocks. R6 alone changes in the normative block, at :67–70, to checks actually reached by the child.

The exact read interval is `end.after - previous.before`, or `end.after - start.before` on the first read (`crates/security/src/revocation.rs:53–81`). The stored history uses the successful read's opening `before` and closing `after` (:170–202). The boundary samples `now.after - last.before`, without refreshing history (:204–244). Greater than ten seconds fails the time comparison; equality does not. Clock validity, counter success and existing latch conditions remain independently required. The checkpoint can also fail its boundary after completing the monitored observation (`custody/operation_guard.rs:896–933`). Subject :127–137 and S3 :98–104 capture these distinctions.

The four rows at :139–144 cover the relevant timing effects; they are comparative timing cases rather than a disjoint enumeration of every product failure:

1. With no baseline timed observation, no observer refresh or wall read is removed. One tick per normally joined guard remains the observer contribution. The included eight-plus-four-second example correctly shows that this does not imply success.
2. Where timed reads are removed and the remaining native checks still satisfy their bounds, the elapsed-time observer nondeterminism is removed. “Clean” concerns this timing cause, with other operation prerequisites still required (NB-1).
3. If a successful timed read previously kept the history fresh but the remaining later check now exceeds its bound, the census must be refused as a harness error. This is the adverse load case, not a retry opportunity.
4. With a successful initial read and no later main-thread check, R2 supplies no new freshness refusal, regardless of the elapsed lifetime. Storage's refused end settles without a checkpoint (`custody/commit_session.rs:1198–1207`); security's fourth operation goes directly to its end (`crash_matrix_census.rs:211–214`). “Points stay equal” describes normally completed repetitions under R2, not equality with an old slow trace containing timed observer points (NB-1).

The former independent-watchdog/starvation claim is gone. The unchanged caller checks remain the enforcement sites for actual bound refusals; `Census::from_exit` is not silently promoted to a semantic-outcome validator. No native clock or numerical bound is weakened.

## 3. New measurements and LT-4

The twelve table values in S4 :153–154 match the pinned `analysis-r2.txt` and `EVIDENCE-ITEM2-r1.md`: quiet A 3.854/4.651/5.717 seconds and Cg 3.353/4.149/5.296; loaded A 4.716/6.912/9.765 and Cg 4.352/6.398/8.759. The supplied report says 20 runs per condition and all 40 outcome heads `Committed(latched=false)`. Those are reported measurements, not measurements independently rerun in this review.

R3 correctly improves on the measurement memo's stronger language: neither interval is a strict native-bracket bound. The initial read is before the observer gate in the child, the closing checkpoint sample is after its before-observation record, and parent-arrival lag can affect both endpoints. Native first-read work and the checkpoint read's own duration cannot be cleared by subtracting a parent-record interval from ten seconds.

Accordingly, 9.765 seconds is a warning about loaded behavior, not proof of 0.235 seconds of usable native margin. S4 :157–159 and S8 :314–322 say so. LD-Q-236's decision to include the targets under the load rule is an operational selection that retains red outcomes and escalation; it is not supported as a quantitative guarantee by these proxies. It does not eliminate FLAKE7-FIX-1's controls or the separate installation gates. NB-3 records the remaining provenance limits of the supplied summaries.

## 4. The 3.0-second stall and its derivation

The arithmetic is correct **as a pilot choice from the quiet proxies**:

```text
lower proxy threshold = 5.000 - 3.353 = 1.647 s
upper proxy threshold = 10.000 - 5.717 = 4.283 s
1.647 < 3.000 < 4.283
Cg_min + 3.000 = 6.353 s
A_max  + 3.000 = 8.717 s
```

R3 uses **Cg minimum**, which is the correct statistic for this proposed lower-threshold calculation. The measurement memo's prose saying “from Cg max 5.3” cannot derive 1.7; r3 :242 fixes that provenance error. The displayed `(1.7, 4.3)` is only an approximate description, not an outward-rounded safe interval from which arbitrary durations may be selected.

Neither empirical extrema from twenty runs nor these proxy endpoints prove a working native interval on future runs. The delayed-start observer counterexample remains possible even when the sums exceed five seconds, and actual post-fix read duration can consume apparent headroom. R3 explicitly makes reproduction empirical, labels both operands as proxies, records real refusals, and prohibits silent retuning, so its three-second choice is acceptable without treating it as a proven scheduling bound.

Counting is now **inside** the stop-confirmed-to-SIGCONT interval (:235–239). Counting for two seconds followed by a fresh three-second sleep would not implement this specification. The driver must retain actual monotonic times; counting overrun is an evidence failure. A delayed SIGCONT or other interval deviation must likewise be disclosed, not reported as a nominal exact three-second act. The selected delay is a target for the experiment; measured execution determines whether the intended control was actually performed.

## 5. C2, C3, C5 and C6

- **C2:** The storage commit path supplies a later checkpoint, unlike the expressly excluded no-later-check paths. A completed actual native bound refusal and its conversion to harness error are the evidence required. A failed child that never reaches that check proves neither C2 nor a measured bracket. The wording at :283–285 is a suitable control obligation, not a claim it has run.
- **C3:** :286–287 requires both the unchanged five-second/live-seam pin (`operation_guard_tests.rs:253–254`) and the release-absence/feature-boundary evidence. That closes the earlier concern that the constant pin alone would establish production exclusion.
- **C5:** :292–294 keeps the common parser rejection narrow and explicitly separates it from once-per-guard and R6. S5 also requires the unaffected parser consumers to keep passing. Normal completion and observer join remain part of R3's scope (:72–75).
- **C6:** :295–296 includes all three affected families, current recommit coverage, every failure, no retries and separate R6 classification. This is the correct current-workload obligation. Neither the old 3d2d5b5 traces nor the parent-arrival experiment discharges it.

C4 remains a distinct armed precision control, not an alternative proof of C1. The generic gate and its `gate=waited` self-test must remain unchanged. All controls remain pending as stated at :298.

## 6. S2, S5 and S9

The NB-1 corrections are accurate: S2 now has five storage revocation/observer expected rows, including the two CamelCase `ObserverFailStop` rows missed by the heuristic, and distinguishes implicit children from the 216 explicit spawns. All five affected writers arm the tick. The statement is limited by :90–91 rather than asserting all-load equivalence. The 173-point figure is withdrawn; the historical count of 82 link-after records agrees with the trace analysis in the prior supplement.

S5 now says **three observer-affected census families**, explicitly lists storage's ledger-only census and platform self-tests as unaffected consumers, includes current recommit coverage, and limits historical evidence to compatible observer counts. This resolves NB-2 without claiming only three callers exist. No expected value, kill-set point or row needs to change for the cadence rule. The `spawn(None)` normalization case remains outside R1.

S9 binds the precise exceptions prospectively, preserves accepted bytes, explicitly limits the unchanged X4 claim to production law and numerical/native checks, and carries both :636 and :1328 as CP-X9-ARMED-TIMER. The stale method pointer is removed because the reviewed method is now in S7. The adoption receipt must identify this exact r3 hash and confirm the S8 item 5 classification reconciliation. This review is adoptability evidence for that receipt, not the receipt itself.

## Non-blocking notes

- **NB-1 — Timing-table shorthand.** Prefer “no additional cadence-induced refusal, assuming the other checks succeed” to an unqualified “Clean,” and “normally completed post-rule repetitions retain these points” to “Their points stay equal.” The present record's R6, first row, no-later-check discussion and explicit limits on scheduling claims supply that scope. The table does not authorize accepting an I/O, malformed-clock, existing-latch or other unrelated failure, and does not promise point equality with an old trace containing timed observations. Similarly :146–147 summarizes the observer-related load issue; it is not an exhaustive native failure threshold.
- **NB-2 — The unstalled arm limits attribution.** A side-by-side report is sufficient context for the deliberately limited claim “timed observations occurred in these baseline runs and are absent after the change,” together with source evidence. It does not by itself prove the suspension caused a particular second tick or measure its causal effect. If unstalled baselines show the same ticks, report that; do not call those ticks stall-induced or imply that the original two-census equality test necessarily failed in each reproduced run. Preserve complete counts and denominators for all classes and both arms. A minimum of three reproduced witnesses supplies neither a failure-rate estimate nor a guarantee that all positioned baselines reproduce.
- **NB-3 — Preserve measurement caveats in the implementation evidence.** The supplied memo says the concurrent Cargo build finished before the loaded series ended. `analysis-r2.txt` reports two loaded runs with a missing record and labels tick counts as limited by warm-up order. The figures are accurately transcribed here, but this review has not audited the raw TSVs or measurement program, and those caveats preclude upgrading the summary into full per-run trace coverage or constant-load proof. Keep the raw artifacts and load chronology with any later execution review.

## Remaining gates

No required RF remains for adoption of this specification. The coordinator's exact adoption receipt, FLAKE7-FIX-1 implementation and independent review, C1–C6 execution evidence, current-workload validation, inventory/integration and LT-4 installation obligations remain separate. CP-X9-ARMED-TIMER remains open. No product qualification is established.
