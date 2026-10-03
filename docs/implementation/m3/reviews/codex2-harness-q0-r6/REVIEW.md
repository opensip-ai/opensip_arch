# CODEX2 — M3-Q0 r6 review

**Verdict: REQUIRED-FINDINGS. One required finding, C2-Q0-R6-01 (P1).**

The exact C2-Q0-R5-01 predecessor sequence is resolved. The replacement has a new loss-coverage gap: its global generation window remains open after an individual CPU's sequence fence has ended.

## Subjects and scope

| Subject | Bytes | SHA-256 |
|---|---:|---|
| `docs/implementation/m3/harness/DESIGN.md` | 118963 | `3a17a943d4139248ca9fc7a8b8893f04a452c71a6a0710d7bf954866262ec31d` |
| `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json` | 53696 | `da73a4765c7841555d1d77512baeeb7c2000b442ef885daa0b902b93a005e2e3` |

Both match REQUEST.md. Compared all seven DESIGN diff hunks and the one schema hunk against the retained r5 subjects. Changes stay within the r6 response table, associated revision metadata and decision index. The schema changes only its revision references.

## Answers to the request

1. **Exact prior sequence: resolved.** A is alive during the census; B's reuse of its TGID is rejected by rule 1, regardless of A's delayed delivery or B's absent report (DESIGN:749,758,762,794). Outside-range records cannot satisfy B's terminal requirement. C2-Q0-R5-N01 is also addressed explicitly by the initial-PID-namespace and proc-view requirements at :763 and the mismatch cases at :797/:905.
2. **Fence ordering: sound causal basis, incomplete coverage.** For a pre-K generation, a terminal enqueue after L means the process could not already have been reaped during the census. Its fork notification attempt precedes its own terminal enqueue, which precedes S's terminal enqueue and S's connector EXIT. These relationships can establish the boundaries without clocks. They establish known generations only if connector loss is positively covered through the entire global window; the current rules fail that condition.
3. **New error: C2-Q0-R6-01 below.** No substantive change beyond the declared table was found.

## C2-Q0-R6-01 — Extend every CPU's loss proof through the global generation window

**P1.** Locations: DESIGN:744,748–759,776–781,796,900–904.

Step 3 checks connector sequence gaps only between **each CPU's own** pre-launch and post-run sentinels (:744). QD-29 instead attributes records through the **last global** sentinel S (:751,:759). An earlier CPU has an uncovered interval during which an outside generation can contribute an accepted counter.

A permitted two-CPU sequence is:

1. TGID p is absent from the census. Subtree B is born and exits before CPU0's post-run sentinel P0. B's taskstats report is silently omitted; its connector birth and exit arrive, and it is reaped.
2. P0's fork, terminal and exit arrive, ending CPU0's stated sequence-gap coverage. CPU1's final sentinel S has not yet closed the ranges.
3. Outside single-thread process C reuses p. Its fork notification is attempted on CPU0 after P0, but connector packet allocation fails. The CPU0 sequence advances without a delivered event or receiver overrun.
4. C's successful `AGROUP` record is enqueued between L's and S's taskstats records. C's connector EXIT is delayed beyond S and completion. No intervening CPU0 event exposes the missing fork.
5. All remaining post-run sentinels arrive, including S. Only B's birth is known for p; C's record is the sole in-range terminal and is attributed to B under :759.
6. B's observed exit and all sentinels satisfy :777–778. The cross-join also passes because p already has a lifetime. No host entry for B is required (:822).

This counterexample is an inference from the stated rules and kernel ordering, not an executed experiment. Connector sequence assignment precedes sending and the send result is ignored; initial allocation failure returns before broadcast, so it need not cause receiver `ENOBUFS`. ([Linux v6.18 process connector](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/connector/cn_proc.c), [connector transport](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/connector/connector.c))

Taskstats reply allocation can fail before sequence allocation, and the exit path then returns without a report. Terminal sending occurs before `exit_notify` and connector EXIT, allowing C's terminal to precede its delayed EXIT. ([taskstats](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/taskstats.c), [exit path](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/exit.c))

**Impact:** B's missing counter can be replaced by C's lower counter while the run is declared complete. If concurrent sampling misses B's brief peak, the run can falsely pass its RSS budget.

**Required correction:** positively cover connector birth attempts on every online CPU through the fixed global S close position. One sufficient approach is to freeze S and the K–S/L–S bounds, then obtain a further sequence-bearing validation probe on every CPU **after receiving S's connector EXIT**, checking continuity through those probes. Keep S as the attribution cutoff. Checking only gaps received before S is insufficient without a received upper sequence bound on CPU0. Unprovable coverage must remain incomplete.

Add the sequence above to calibration/reference cases; it must produce `event-loss`/incomplete, never C-to-B attribution or complete status. This obligation follows from r6's system-wide generation proof; the older workload-birth fence alone does not cover outside births after a CPU's sentinel.

## Non-blocking observations

- **C2-Q0-R6-N01:** rewrite :753–754 using enqueue and pre-reap ordering. Socket FIFO does not order different processes' exit completion. The narrower causal argument in answer 2 suffices once C2-Q0-R6-01 is fixed. Fork notification precedes child execution. ([fork path](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/fork.c))
- **C2-Q0-R6-N02:** :795 promises `terminal-record-missing` for a pre-launch exit/reuse without excluding a census entry or window birth. Either would instead require `unjoinable-identity` under :758. Qualify the case or allow that conservative outcome; both remain incomplete.

## Carrier and verification

Existing typed reasons and `slotReasons` support the new failures. QD-27 (:852) nulls figure (b) and peak while retaining elapsed and concurrent samples; :857/:873 keep any reasoned result incomplete and outside Q6. The stated r6 reference cases agree on observed data but omit the lost late birth above.

This was a read-only design review with static primary-source checks. No product code, tests, builds, validators, reference implementations, corpus fetches or benchmarks were run. No runtime home was accessed and no commit was created. Writes are limited to REVIEW.md and review.json in the requested r6 temporary directory.
