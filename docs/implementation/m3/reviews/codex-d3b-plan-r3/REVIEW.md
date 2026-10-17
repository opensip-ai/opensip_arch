# D3B-PLAN-r3 review

**Verdict: ACCEPT.** The round-2 required finding is resolved at plan level. No required findings; one non-blocking clock-pair implementation clarification.

## Subject verification and scope

Independently rehashed the 752-byte subject manifest, SHA-256 `857527305a3e6eab16748fb6e360e8b8df123e7f6c857ba6648a4b87b67b8522`, and all three members:

- `d3b/PLAN-r3.md`: 55,134 bytes, SHA-256 `d67c5af0233602936d1e7d8b5d243ba1937d49e34c4a73d99c88c153226aa709`.
- Historical `d3b/PLAN-r2.md`: 47,535 bytes, SHA-256 `0e11a70a2c9d669838874c8e9b0826c1370a31d11de06eb661bb2e714fd58144`, unchanged from round 2.
- Historical `d3b/PLAN-r1.md`: 32,980 bytes, SHA-256 `4f0d8cb0b0e57abead364a615d40d8df43e2d6fc81d4b75ed21f43b3f7fdd6c9`, unchanged.

Read the round-2 review/JSON and the r2-to-r3 diff, with the revised sections in context. Checked SL S6's named clock and mark bounds; platform ClockObservation/observe_clock and macOS monotonic source through Git at the specified product base `d704ed4551d65da8be18faf69f4aeed26be369c2`; S-OP-2 r6's ordinary registration, existing kinds, elapsed semantics and descriptor rules; and the typed scratch-retained builder precedent at that same product base. Architecture authority remains the specified `9415426c053c8e2b287022f5db4dd380024d120a`.

## R2-RF-1 disposition

**Resolved.** The revised measurement rule separates the information available after a successful arming read from failure of the arming read itself.

- **Successful arming:** a valid observation supplies the lag from the fixed observer reference. Pending-mark timers are converted once into the loop's Instant domain. Determination reads either supply a measured bracket-relative elapsed value or fail closed with a labelled lower bound. Already elapsed bounds miss immediately; there is no negative deadline subtraction.
- **Failed arming:** no lag is asserted or inferred. Applicable pending marks become missed once, with `elapsed_status: unavailable` and no elapsed field. No mark timer is armed and no later mark read can reset the reference or revise those misses. Already satisfied marks stay satisfied and tool protocol-cancel stays inapplicable: the controlling rule is explicitly about pending marks, including where a provider cancel was already fully written before the observation.
- **Valid-read rule:** Ok alone is insufficient. Boot identity must match the original observation and monotonic_after must not precede its monotonic_before reference. Platform observe_clock itself also refuses regression within its bracket and a boot change during the read. These are clock observations, not admitted trust time or wall-clock measurements.
- **Later failures and recovery:** after successful arming, the fallback uses the measured lag plus the awake Instant delta. Its status is carried on the individual event as lower-bound. A later valid read may determine still-pending marks, but cannot revise/re-emit a prior miss or re-arm a timer. Each mark reaches a terminal state by settlement.
- **Ladder independence:** failure of mark measurement does not delay or cancel T-1 through T-5, the revocation reap ceiling or bounded scratch removal. Mark failure discloses inability to establish satisfaction; it is not proof that the action physically exceeded its deadline. The new explicit event definition preserves that distinction.

The fixed reference is the observer's earlier monotonic bracket and successful determinations use their later bracket. Accordingly, measured elapsed is a conservative bracket-to-bracket measurement, not an invented exact timestamp of the counter read. The fallback's lower-bound claim must refer to that fixed-reference interval and use correctly ordered paired samples (NBO-1).

## Schema and ordinary registration

The proposed schema is lawful as an ordinary code-unit registration under S-OP-2 item 3:

- ElapsedStatus is a registry-literal K1 table with exactly `measured`, `lower-bound` and `unavailable`. These are release-owned literals with valid bounded token spelling, not runtime/provider text or a new provenance class.
- Elapsed and bound retain existing K2 Elapsed, with monotonic nanosecond values and distinct documented roles. The status identifies measurement quality; bound is configured. No new SafeField kind or privacy class is introduced.
- The optional elapsed field is present exactly for measured/lower-bound. Three typed builders, with the unrestricted constructor hidden as in the scratch-retained precedent, can enforce that shape on the producer side. The complete descriptor and generated documentation must retain the optionality and status-dependent meaning for readers; missing elapsed is absence, not a fabricated zero or null duration.
- Provider revocation events require Project/Plan/Execution plus their role/universe fields. Tool counterparts remain Project-only without invented provider identities.
- The code unit now counts three event names and two literal tables, and must update registry documentation, static encoding bounds, budget slots and drift/source checks accordingly.

Changing optionality here does not retype an existing registered revocation event: these events were only proposed in r2 and have not been implemented/registered by this plan review. The implemented event descriptors still require their own code-unit review. S-OP-2's immutable existing-field rule remains unchanged.

## Controls, mutations and narrowness

The controls cover all four requested information states: initial arming failure; a later failed determination after valid arming; repeated failures through settlement; and recovery after a disclosed miss. They also exercise invalid boot identity/regression, assert status/field shape, preserve tool inapplicability and requests-refused satisfaction, check the unchanged ladder, forbid timer restart, and require exactly-once disclosure with no pending mark after settlement. These are adequate plan-level requirements, subject to the ordinary implementation controls below.

The four added mutations directly target assumed lag after failed arming, a reset reference, a lower bound mislabeled measured, and elapsed emitted with unavailable. Each must fail a behavioral assertion in its implementation lane. The existing late-completion/duplicate and ladder controls remain necessary. Add the delayed arming-read/sample-order case described in NBO-1 when implementing the clock-pair seam, rather than testing only instant-returning synthetic observations. Registry controls should exercise both duration-present builders and the duration-absent builder on both provider and tool event shapes.

The diff is narrow as requested: header; the new r3 disposition table and history heading; LD-D3B-9's status/optional-duration schema and table count; LD-D3B-10's measurement block; LD-D3B-13's table count; the clock-failure controls; and four mutations. No other operative section changes. R2's Q10/Q11/Q12 rulings and earlier tree, cancellation, trigger-order, protected-root and harness dispositions are not reopened. Their bounded deduplication, cause-following cancellation, normal-shutdown evidence, stamp-exhaustion and candidate-file/exclusion obligations remain carried to their code units.

## Non-blocking observation

**D3BPLAN-R3-NBO-1 (P3) — Pin the Instant sampling order in the clock-pair implementation.** Location: `docs/implementation/m3/supervisor-d/d3b/PLAN-r3.md:258`.

The lower-bound formula is sound for elapsed time from the fixed monotonic_before reference when its arming Instant is sampled after the successful observe_clock read, including that read's monotonic_after sample. The phrase "the Instant of the read" does not explicitly state the order. Sampling Instant before a slow clock observation would count part of that read both in lag and in the subsequent Instant delta, so exclusion of sleep alone would not prove the claimed lower bound.

Carry an explicit code-unit rule that observe_clock completes before the arming Instant is sampled, and sample the determination Instant at the decision point after any failed read. Describe the lower bound relative to the fixed reference bracket, as LD-D3B-10 defines it. Add a deterministic delayed-arming-read control proving the read interval is not counted twice. No clock reset, new field or new successor is needed.

This is a precise implementation requirement for the specified clock pair, not a new failure policy. Taking the arming Instant after the successful clock observation makes the awake delta omit any sampling gap rather than double-count the observation interval. Preserve that conservative direction if the clock/read seam changes.

## Review limits

Acceptance applies to this narrow plan revision. It establishes no executed clock, suspend, reboot, scheduling, real-codec, Linux, harness or product qualification result. The code units still owe implementation, ordinary registrations, controls/mutations, required checks and inventory treatment.

Only REVIEW.md and review.json were written in the requested directory. Neither repository, worktree nor control file was edited. No Cargo, rustc, build, lane, network, private fixture/key/installation material, held tree, held-out material, T2 store/overlay/cache, other pane or delegation was used.
