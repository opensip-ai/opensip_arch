# D-108 draft — Record component-packaging-contract.v14 as DR-120's accepted design-contract candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual ACCEPT
> (0 blockers, 0 SHOULD-FIX from both reviewers). Same form as the
> adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 / D-105 /
> D-106 / D-107.
> **Subject:** `docs/coop/artifacts/component-packaging-contract.v14.json`
> only.

This is coordinator decision **D-108**. It is not register row
**DR-108**.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| component-packaging-contract.v14.json | `8321d527843c63592d8e4fd49c3df0ace690da0bcbcd1e268464e578fe30424c` |
| Claude 2 verdict | `b47485eb9ba2221e223fcecd588e3d6d49e86918aee7e672276c652aabddaf79` ACCEPT, 0/0, ADV-1 |
| Codex verdict | `ee4fd95833d165a936bd2ba14dac2345dbb59b523985bc30f142f610053170e5` ACCEPT-WITH-ADVISORIES, 0/0, CPCV14-A1 / CPCV14-A2 |
| COORDINATOR-DECISIONS.md | `a28f7a23a9466c3484a9540c77794ffaf8e65139efb0db5d2d0d4cec636293cf` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files are mode 0444
at the measured digests.

Finding-id collision discipline: Claude `ADV-1` is
`CLAUDE-V14-A1`. Codex `CPCV14-A1` / `CPCV14-A2` are
`CODEX-V14-A1` / `CODEX-V14-A2`. They are distinct findings.

## Decision

1. Record `component-packaging-contract.v14.json` as DR-120's
   accepted design-contract **candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. Advisories CLAUDE-V14-A1, CODEX-V14-A1, and CODEX-V14-A2
   travel as honesty work. Do not retarget pack v14.
3. DR-120 stays `OPEN`. No `SATISFIED`. DR-G15 stays
   named-not-authored / not QUALIFIED. Adapter implementations
   remain reserved. D-056 Class A is not opened.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not dispose DR-117.
   Does not SATISFY DR-103, DR-107, DR-111, DR-112, or DR-105.
   Does not overturn D-106 or D-107.

## Alternatives

- Wait for a v15 that folds the three advisories. Rejected: 0/0
  is the gate; advisories travel.
- Mark SATISFIED. Rejected: G15 unexecuted; leftover is not
  measurement-only.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D108.
