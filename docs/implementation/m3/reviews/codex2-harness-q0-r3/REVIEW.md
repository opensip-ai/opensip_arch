# CODEX2 review — M3-Q0 r3

**Verdict: REQUIRED-FINDINGS.** Two required findings remain in the new missing-record coverage and consistency rules. The Linux completeness design and K2 slip correction resolve their r2 findings. Batch joins themselves are fixed, but their incomplete-evidence path needs the two corrections below.

Reviewed subjects:

- `docs/implementation/m3/harness/DESIGN.md`: 101,902 bytes; SHA-256 `b69c918f5fa5976285970dcda015cd98e3f04da706bf4c62d89a3c5900d73a04`.
- `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json`: 52,882 bytes; SHA-256 `f38b3f2046172b4365179694fe625a7936e107b95c937f341606c404de7fd96b`.

Both match REQUEST.md. Retained r2 DESIGN and schema hashes match `4225ca34728ba1494a087110c5b92664f7d3f1560dc5ce3dd70fa24cf91e63c4` and `df67c65128065c33867ad3317a1cf25f870a0b4670c06a8af4336ab00de9548f`, respectively. ENV below means the reviewed r3 schema.

## R2 finding resolution

| Finding | Resolution | Assessment |
|---|---|---|
| C2-Q0-R2-01 — complete lifetime RSS | **RESOLVED at design level** | DESIGN:704–741 now requires acknowledged subscriptions, per-CPU sentinels, connector continuity, loss/CPU-change rejection, terminal `AGROUP` selection through `ac_tgid`, and every known lifetime/thread's exit coverage. Unprovable components remain incomplete. Kernel admission still requires future calibration; no calibration result is claimed. N01/N02 below clarify the explanation. |
| C2-Q0-R2-02 — batch evidence join | **PARTIALLY RESOLVED** | Required `batchId` plus typed slots and batch-keyed observations fix the original ambiguity (ENV:215–269,620–646,1764–1821; DESIGN:791–820). Identity, coverage, uniqueness and orphan checks are assigned. The newly specified missing-record exception has no warmup absence carrier and conflicts with retained measured values: R3-01/R3-02. |
| C2-Q0-R2-03 — K2 slip arithmetic | **RESOLVED** | DESIGN:916–942 propagates F1 delay through H and J2, includes the day-six freeze margin, states the held branch assumptions and lists the corrected OI-12 integration rule. |

R2-N01, N02 and N03 are resolved at DESIGN:462/512,514 and391: CP/product error wording is distinguished, the unsupported OI-17 cost reduction is withdrawn, and “guaranteed when” replaces “exactly when.” R2-N04 assigns consistency to the semantic validator, but its new equivalence introduces R3-02.

## Required findings

### C2-Q0-R3-01 — Missing warmup records have no reason carrier (P2)

**Locations:** DESIGN:792–799; ENV:215–269,1420–1447,1558–1570.

DESIGN:796 requires exactly one operational record for **every warmup and measured slot**, or an incomplete row that lists `record-missing` on that slot. The incomplete Q6 row still has only seven untyped `runReasons` lists aligned with the seven measured sample positions. There is no warmup reason carrier. The new typed `runSlot` exists only on operational records that are present.

Consider batch B with all seven measured records and samples, warmup records 1 and 2, and a missing warmup-0 operational record. The intended failure is `(B, warmup, 0, record-missing)`. No field can represent it:

- `runReasons[0]` attributes the absence to measured run 0;
- adding a typed warmup-failure member violates the closed schema;
- inserting an operational record for the absent slot fabricates evidence.

The validator therefore cannot retain this intended incomplete batch alongside its retry while satisfying coverage.

**Required change:** add absence/reason rows keyed by `batchId` and `runSlot`, or an explicit separate warmup-reason carrier. Make coverage checks consult that carrier for every required warmup and measured slot. Preserve the seven measured-series positions and define how a warmup-only evidence failure keeps the batch incomplete and retained.

This is the unfinished missing-evidence portion of R2-02; the normal/retry batch-ID joins are already resolved.

### C2-Q0-R3-02 — A failure reason must not force deletion of known samples (P2)

**Locations:** DESIGN:770,776–799; ENV:5,1540–1570.

The new invariant at DESIGN:799 and ENV:5 says a slot has a null sample **if and only if** it has a nonempty reason list. But reasons can concern required operational evidence independently of elapsed/RSS collection. DESIGN:770 says an absent record produces null phase fields and a typed reason; DESIGN:778 requires retaining measured values where they exist.

For example, measured run 0 has:

```text
elapsedNanos[0]                = 1000000
concurrentSumPeakRssBytes[0]   = 1024
ownHighWaterSumBytes[0]        = 2048
peakRssBytes[0]               = 2048
runReasons[0]                 = ["record-missing"]
```

Its operational record is absent, so coverage requires incomplete status and the reason. `phaseTimingsPresent: false` and `phaseAbsenceReason: "record-missing"` describe the missing phase evidence, but all four numeric samples are known. The new equivalence rejects this faithful row unless a known measurement is erased or the required reason dropped. The batch-level null phase field is not a null member of a per-run numeric sample series.

**Required change:** require appropriate reasons for unavailable values without requiring every reason to make a numeric value unavailable. Missing/invalid record evidence and other failures may coexist with known numeric samples. Explicitly allow incomplete rows caused solely by missing required operational evidence, preserve available samples and aggregates when their inputs exist, and align DESIGN with ENV's semantic-validator description.

This is a new error introduced while addressing R2-N04. It needs a separate correction from the warmup carrier.

## Non-blocking observations

1. **C2-Q0-R3-N01 — Clarify correlation and sentinel fences (DESIGN:700,720–723,729–734,752).** Kernel terminal-record emission before reaping does not guarantee userspace reception before a reused TGID's new fork arrives on the other channel. Specify buffered per-TGID reconciliation or conservative rejection of reuse ambiguity, reconcile start-time versus fork-timestamp keys, and retain lifetime history for delayed host joins. Also narrow “read past the workload” to the birth-history fence: connector exit emission follows cgroup exit, so a known exit notification can arrive after a sentinel. The separate all-thread exit requirement and rejection of unevaluable proof components prevent premature completion; no categorical false-complete counterexample was established. [Linux taskstats source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/taskstats.c), [Linux exit source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/exit.c).

2. **C2-Q0-R3-N02 — Separate calibration success and rejection cases (DESIGN:736–741).** The introduction says the following cases are all detected as incomplete, but the short-lived-child, early-leader and PID-reuse cases describe successful peak capture/correct joins. State their expected statuses separately from induced-loss/discarded-message cases, which must be incomplete.

## Requested checks

**Linux positive completeness proof:** acceptable as a design with its explicit conservative admission rule. Connector sequence assignment and sends are serialized; fork notification precedes child wakeup, supporting the complete birth-history check. Terminal per-task `AGROUP` selection addresses early-leader undercounting, and accounting reads the address-space high-water mark before address-space release. Required terminal/exit coverage catches missing known records. These source facts were checked against Linux v6.18; admission on the eventual D12 kernel remains conditional on K1c calibration. [Connector source](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/connector/cn_proc.c), [fork source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/fork.c), [accounting source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/tsacct.c), [taskstats source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/taskstats.c).

**Batch carriers:** normal/retry joins are explicit and observations are per batch; per-runner calibration is appropriately separate. Typed slot bounds are correct: priming index 0, warmup indexes 0–2, measured indexes 0–6. The failures identified above concern the new absence rules, not a continued lack of batch IDs.

**Slip rule:** with `d = max(0, s − 1)`, for `d ≤ 2`, J3 = 21, M3-M = 24 and M3-X = 26. For `d > 2`, H = 13+d, J2 = 16+d, J3 = 19+d, M3-M = 22+d and M3-X = 24+d. R, F4 and J4 remain earlier under the stated assumptions. Thus `M3-X = 26 + max(0, s − 3)` is correct for nonnegative oracle slip. The alternative split authoring/run schedule is named but not adopted.

**Schema:** static inspection only. All 39 object schemas are closed; no number-typed fields were introduced. Required batch carriers, typed slot bounds and new RSS reason enums agree with the declared changes. Cross-row checks are assigned to the semantic validator. No validator was run.

**Changes beyond the table:** none of substance found. All 12 DESIGN diff hunks map to revision metadata/table, statistics wording/cost, RSS proof/identity/reasons, batch carriers/validation, K2 slip/OI-12 updates or the decisions index. The complete schema diff changes only its description, required batch observations, six RSS reasons, typed slots, runner calibration, operational-record joins and batch observations. The required findings are errors within these declared changes, not unlisted scope expansion.

Review was read-only static inspection of r3, retained r2 subjects/review, accepted M3-PLAN dependencies and primary Linux source, with analytic schedule checks. No product code, tests, builds, corpus fetches, benchmarks or runtime-home access; no commits. Only the requested two r3 review artifacts were written.
