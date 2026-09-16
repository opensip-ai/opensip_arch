# Independent Grok review: workflow-timing02 original unit

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-workflow-timing-subject-02`
**Manifest SHA-256:** `00fe80539abd202184e736cd490449d3f39bb75f8d3abd3eb6f75f686ee03391`
**Members:** 9
**Verdict:** **ACCEPT WITHIN STATED REFERENCE SCOPE**

Root correction02 for TIM-F1–F4 (RP-DO-11). Pure owner/reference helpers. Not actual clocks, journal/crash recovery, report-ledger custody, or product selection. Later joint13 invocation:5 composition is **not** this freeze and is **not** a waiver.

## Custody

Verified before and after. Work used only `review/copy` and `review/probes`. Frozen subject not executed against and not written. No modes or symlinks listed.

| Check | Result |
| --- | --- |
| Manifest | `00fe8053…3391` matches declared |
| Files | 9 listed = 9 walk |
| Pins | **5/5** |
| After | frozen hash unchanged |

## TIM-F1–F4 (presentation review01 → this freeze)

Independently reproduced (**17/17**).

| Id | This freeze |
| --- | --- |
| **F1** | v4 `Attempt.allOf` if `outcome=abandoned` then `observedDuration` is const `{unavailable, supervisor-lost}`; else that reason is forbidden. Independently: abandoned+measured, completed+supervisor-lost, and abandoned+clock-unavailable are schema-invalid; abandoned+supervisor-lost and completed+measured are valid. Semantic `admit_duration` matches. |
| **F2** | Non-`int` samples refuse before the `None` missing-sample test. `(None, 4.0)`, `('0', None)`, `(True, None)` are `TimingRefusal`. True missing samples remain `clock-unavailable`. Historical **subject01** still maps `(None, 4.0)` to `clock-unavailable`. |
| **F3** | `summarize_attempts` admits each projection, unique `exec1_` IDs, at most three, no partial sum. `{state:bogus}` is `TimingRefusal` not `KeyError`. Duplicates and negative milliseconds refuse. Unique pair 3+8 sums to 11. Overflow is unavailable without truncation. Empty list is `no-attempts`, not measured zero. |
| **F4** | `source_support` maps every unsupported positive major including **1** to `incompatible/retained-schema-major-unsupported` (pinned `PanelNotPresentV1`) before any attempt decoder. `project_attempt(1, …)` does not decode. Historical subject01 had no `source_support` and left major 1 as an unowned refusal. |

**Also confirmed.** Zero/sub-ms floor is a measured 0, never a fallback. Abandoned always `supervisor-lost` even with a numeric pair. v3 projection is `not-retained` and does not rewrite the source record. `not-retained` is forbidden as a v4 persisted duration. Pinned report07 ledger already contains `render-in-progress`; the contract names it for the current render step (no terminal duration for that in-progress attempt).

Schema delta: invocation:4 is invocation:3 plus required `observedDuration`, `AttemptDurationV1`, the abandoned/supervisor-lost `allOf`, and major/id/title/description.

## Reproduction

Private copy, reference Python `-I -B`: `check.py` **11/11**, 5 pins, `selected: false`.

## Joint13

`composed-sources/invocation-record.proposed.schema.json` is invocation:5 (`28aa0c42…f4fb`), **not** this freeze’s invocation:4 (`814b61bd…1c89`). Later composition does not rewrite this 9-file unit.

## Must-fix / should-fix

None in the stated reference scope.

## Remaining duties

Host monotonic clock and durable Attempt custody, including crash recovery. Rebind invocation:3 consumers; the report ledger still references v3 and has no duration carrier. Coordinated ledger fields, bounds, labels, browser, and source-map selection. RP-DO-11 is not delivered by this isolated owner. Actual capture and report-ledger custody remain absent.
