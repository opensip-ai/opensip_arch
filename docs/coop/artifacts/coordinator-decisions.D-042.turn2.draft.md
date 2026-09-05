# D-042 turn 2 — Record permission-truth-tables.v2 as DR-105's accepted design-contract candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. Records independent
> ACCEPT-WITH-ADVISORIES (0 blockers from both reviewers). Same
> form as D-035 / D-038.
> **Subject:** `docs/coop/artifacts/permission-truth-tables.v2.json`
> only.

Turn-1 subject `coordinator-decisions.D-042.draft.md`
`f974b2f82bcb53b092c84c714601a17a4a06da709242b2154148c6a53cf1e749`.

Turn-1 findings:

| ID | Sev | Disposition |
|---|---|---|
| C2-D042-01 | SHOULD-FIX | ACCEPTED. Remaining unmet items named below. |
| NOTE-D042-01 | NOTE | Adoption-time recording. |

Measured inputs:

| Path | sha256 |
|---|---|
| permission v2 | `cce3afcaee90bbca388825a474751d6ebb17b30722b35dadcf6c631b34a8731a` |
| Claude 2 | `021bacaf071dfa682e3e85574f42306adc3f2b12607e0bbd94b01aa344389301` ACCEPT-WITH-ADVISORIES 0 blockers |
| Codex | `c32f98751b848e3d2ccbe6e9927e60ea8e640f0b655315ebd1fc295c5a1e856d` ACCEPT-WITH-ADVISORIES 0 blockers |
| Claude 2 D-042 t1 | `61caf9726d4d963c7caeedbf463cd81b006b8f22727d6cd63ebb6658dd5a61da` |
| Codex D-042 t1 | `e5435ccf3b7c2dd3341d19cbad3f87d6cdd242309978ab5f9ef8565c1fa36cd2` |
| COORD | `a4d497383ef26f7be1a0072ca260d1776ec5f4ba525444eaeb1ea16d4d527f6a` |
| file 08 | `877e36d3b597fb9b51c1c91fb6b6c6f27eabdcb8b2b1a941ade2b34850a0f58f` |

If a cited file moves, re-measure.

## Decision

1. Record `permission-truth-tables.v2.json` as DR-105's accepted
   design-contract **candidate**, on the same terms as D-013 / D-015
   / D-035 / D-038. Both independent reviewers returned 0 blockers.
2. The row stays `OPEN`. Remaining unmet, named: fixture execution
   (DR-G09); join blockers BLK-1/2/3/4 STILL-ROUTED; host-under-
   instruction outside this vocabulary (D-032); host-effect live
   instance (FC-C1) unmet. This recording discharges none of those.
3. Advisories P2-01, P2-02, P2-03, and PT2-CX-A1 are not blockers.
   They remain owed as honesty work on a successor.
4. No `SATISFIED`. This recording does not make any host or
   component act exercisable. Does not edit file 08. No freeze
   motion. No blueprint.

## Alternatives

- Wait for a v3 that folds the advisories. Rejected for this
  recording: 0 blockers is the D-035 gate.
- Mark SATISFIED. Rejected.
- Omit the unmet list. Rejected (C2-D042-01).

## Readiness effect

Zero.

## Reversibility

Total. Overturn: C-D042.
