# D-105 draft — Record signed-index-trust-contract.v8 as DR-112's accepted design-contract candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual ACCEPT
> (0 blockers, 0 SHOULD-FIX from both reviewers). Same form as the
> adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104.
> **Subject:** `docs/coop/artifacts/signed-index-trust-contract.v8.json`
> only.

This is coordinator decision **D-105**. It is not register row
**DR-105** (permission truth tables).

Measured inputs:

| Path | sha256 |
|---|---|
| signed-index-trust-contract.v8.json | `fc171321e969c74464dbc9ff67edd9b874aac1d1c7375c7dc8e431469442efe0` |
| Claude 2 verdict | `559cfad1f29443326734fe4cc480aca802bfac118668080956af59534029dead` ACCEPT-WITH-ADVISORIES, 0 blockers, 0 SHOULD-FIX, 1 advisory ADV-V8-01 |
| Codex verdict | `10784a6de2c2767cec5ce55549cc75d4402cd93f4fe5342e8ff95c5236fead13` ACCEPT, 0 blockers, 0 SHOULD-FIX, 1 advisory SITCV8-A1 |
| COORDINATOR-DECISIONS.md | `d210f103fc32a36e2220acd4c9bab8c7db1102370ba299c9989e9f54f9642166` |
| file 08 | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files are mode 0444
at the measured digests.

Finding-id collision discipline: Claude used `ADV-V8-01`; Codex used
`SITCV8-A1`. They are **different** findings. This draft names them
`CLAUDE-V8-A1` (memberApplicability parenthetical omits recovery
PRESENT member 18) and `CODEX-V8-A1` (finalized Codex v7 REJECT
`ffe079b9…` still described as unpinned provisional). They travel
separately.

## Decision

1. Record `signed-index-trust-contract.v8.json` as DR-112's accepted
   design-contract **candidate**, on the same terms as D-013 / D-015
   / D-035 / D-042 / D-103 / D-104. Both independent reviewers
   returned 0 blockers and 0 SHOULD-FIX.
2. Advisories CLAUDE-V8-A1 and CODEX-V8-A1 are not blockers. They do
   not prevent this recording. They remain owed as honesty work on a
   successor or in this disposition's carry, not as a reason to
   withhold the recording. CODEX-V8-A1 is discharged as **record**
   by this draft's measured pin of Codex v7
   `ffe079b9c634fe97a2a735fbda99efac386505870e11b31b2b23753c6f38a1e5`
   COMPLETE REJECT, 0/1/0, SITCV7-S1 only; v8 was authored before
   that freeze and that fact stays named.
3. DR-112 stays `OPEN`. No `SATISFIED`. Quorum, clock/freshness,
   emergency, and waiver **numbers** remain RESERVED. Repair-media
   remains DR-110. Newly-revoked replay remains DR-113. G06/G08 stay
   named-not-authored / not QUALIFIED. This recording does not make
   any lock producible. D-056 Class A is not opened: leftover is
   still design (reserved numbers, sibling rows, harness execution).
4. Does not edit file 08 (MF-6). No freeze motion. No blueprint.
   Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not dispose DR-117. Does
   not SATISFY DR-103 or DR-105.

## Alternatives

- Wait for a v9 that folds both advisories. Rejected for this
  recording: 0 blockers and 0 SHOULD-FIX is the gate; advisories travel.
- Mark SATISFIED. Rejected: reserved policy numbers, DR-110, DR-113,
  and G06/G08 execution remain; D-056 remainder is not
  measurement-only.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 stays last.

## Reversibility

Total. Overturn: C-D105.
