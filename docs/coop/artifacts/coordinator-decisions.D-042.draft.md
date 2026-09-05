# D-042 draft — Record permission-truth-tables.v2 as DR-105's accepted design-contract candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent
> ACCEPT-WITH-ADVISORIES (0 blockers from both reviewers). Same
> form as D-035 / D-038.
> **Subject:** `docs/coop/artifacts/permission-truth-tables.v2.json`
> only.

Measured inputs:

| Path | sha256 |
|---|---|
| permission v2 | `cce3afcaee90bbca388825a474751d6ebb17b30722b35dadcf6c631b34a8731a` |
| Claude 2 | `021bacaf071dfa682e3e85574f42306adc3f2b12607e0bbd94b01aa344389301` ACCEPT-WITH-ADVISORIES 0 blockers, 3 SHOULD-FIX |
| Codex | `c32f98751b848e3d2ccbe6e9927e60ea8e640f0b655315ebd1fc295c5a1e856d` ACCEPT-WITH-ADVISORIES 0 blockers, 1 advisory |
| COORD | `a4d497383ef26f7be1a0072ca260d1776ec5f4ba525444eaeb1ea16d4d527f6a` |
| file 08 | `877e36d3b597fb9b51c1c91fb6b6c6f27eabdcb8b2b1a941ade2b34850a0f58f` |

If a cited file moves, re-measure.

## Decision

1. Record `permission-truth-tables.v2.json` as DR-105's accepted
   design-contract **candidate**, on the same terms as D-013 / D-015
   / D-035 / D-038. Both independent reviewers returned 0 blockers.
2. Advisories P2-01, P2-02, P2-03, and PT2-CX-A1 are not blockers.
   They do not prevent this recording. They remain owed as honesty
   work on a successor, not as a reason to withhold the recording.
3. DR-105 stays `OPEN`. No `SATISFIED`. Host-under-instruction
   remains outside this vocabulary (D-032). This recording does
   not make any host or component act exercisable.
4. Does not edit file 08 (MF-6). No freeze motion. No blueprint.

## Alternatives

- Wait for a v3 that folds the advisories. Rejected for this
  recording: 0 blockers is the D-035 gate; advisories travel.
- Mark SATISFIED. Rejected.

## Readiness effect

Zero.

## Reversibility

Total. Overturn: C-D042.
