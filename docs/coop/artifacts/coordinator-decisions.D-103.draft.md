# D-103 draft — Record compatibility-matrices-contract.v5 as DR-111's accepted design-contract candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual ACCEPT
> (0 blockers, 0 SHOULD-FIX from both reviewers). Same form as
> D-013 / D-015 / D-035 / D-042.
> **Subject:** `docs/coop/artifacts/compatibility-matrices-contract.v5.json`
> only.

Measured inputs:

| Path | sha256 |
|---|---|
| compatibility-matrices-contract.v5.json | `d0386cee26d8aafd3d07b46f21352cc3d9d03cdc8f406de0adf571f8c81f7f41` |
| Claude 2 verdict | `40a638d4c80601f77b3ff3c7c8de570b8c4c1669405003f0eb445bdd4df2f55b` ACCEPT, 0 blockers, 0 SHOULD-FIX, 2 advisories |
| Codex verdict | `453ec57d98b9caa503b969b49fb99846aa19da830e4b21b70a7395ca550d1731` ACCEPT, 0 blockers, 0 SHOULD-FIX, 1 advisory |
| COORDINATOR-DECISIONS.md | `12d192f758f48f692e69cb410a1d7a9bf776c765257c8e910272d3de457ec3e3` |
| file 08 | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure.

## Decision

1. Record `compatibility-matrices-contract.v5.json` as DR-111's
   accepted design-contract **candidate**, on the same terms as
   D-013 / D-015 / D-035 / D-042. Both independent reviewers
   returned 0 blockers and 0 SHOULD-FIX.
2. Advisories (Claude ADV-1/ADV-2; Codex CMCV5-A1) are not blockers.
   They do not prevent this recording. They remain owed as honesty
   work on a successor, not as a reason to withhold the recording.
3. DR-111 stays `OPEN`. No `SATISFIED`. Numeric windows remain
   RESERVED. S-EVIDENCE remains deferred with DR-113. This recording
   does not make any lock producible. D-056 Class A is not opened
   by this recording: leftover is not only execution/measurement.
4. Does not edit file 08 (MF-6). No freeze motion. No blueprint.
   Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not dispose DR-117.

## Alternatives

- Wait for a v6 that folds the advisories. Rejected for this
  recording: 0 blockers and 0 SHOULD-FIX is the gate; advisories travel.
- Mark SATISFIED. Rejected: numeric windows and S-EVIDENCE remain
  design leftovers; D-056 remainder is not measurement-only.
- Treat dual ACCEPT as application. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 stays last.

## Reversibility

Total. Overturn: C-D103.
