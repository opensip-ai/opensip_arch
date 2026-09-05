# D-124 draft — Record monorepo-ci-contract.v16 as DR-121's accepted design-contract leftover T2-02 candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 / D-112 /
> D-113 / D-114 / D-115 / D-116 / D-117 / D-119 / D-118 / D-120 /
> D-121.
> **Subject:** `docs/coop/artifacts/monorepo-ci-contract.v16.json`
> only.

This is coordinator decision **D-124**. It is not register row
**DR-124** (state-class; recorded as a candidate at D-117).
D-121 remains the last adopted recording (self-update v3).
D-122 and D-123 are in review and are not retargeted.
This cycle does not retarget any D-110 through D-123 draft.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| monorepo-ci-contract.v16.json | `67ca501660a2ba515ce37adc799c5418e4ffd156308189662245e5a5e45a2ddb` |
| Claude 2 verdict | `eb4d3942045710c10923c45f001618a9e006fd885ccbdbe0581f9ecf58e7b8d1` ACCEPT, 0/0, advisories CLAUDE-V16-A1 / CLAUDE-V16-A2 |
| Codex verdict | `b7ba80924a2c0d910edd9428afa93908e64f10c8d45e18ea274019bfb97fe975` ACCEPT, 0/0, advisory MCICV16-A1 |
| COORDINATOR-DECISIONS.md | `da321c467e895f9214c76633380b2173118ab2b4737d2c57f0043586095ee502` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves in a way that is not append-only COORD growth
with file 08, the v16 subject, both v16 verdicts, and this draft
unmoved, re-measure before adoption. Append-only COORD after this
remasurement, with those files unmoved, is **PASS-NO-SCOPE-EFFECT**
and is not a MUST-FIX. The apply writer re-measures COORD at
adoption.

Both verdict files are mode 0444 at the measured digests. HEAD is
`1d24e52` (D-121 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `monorepo-ci-contract.v16.json` as DR-121's accepted
   design-contract leftover T2-02 **successor candidate**. Both
   independent reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-121 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. G16 is
   not QUALIFIED. The candidate binds NOTHING. D-056 Class A is
   not opened. Recording this candidate is not a D-096 (A) grant.
3. Claude advisories CLAUDE-V16-A1 / CLAUDE-V16-A2 and Codex
   advisory MCICV16-A1 travel as honesty work. They are not
   SHOULD-FIX and do not block this recording.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not SATISFY DR-101, DR-103,
   DR-106, DR-108, DR-109, DR-110, DR-111, DR-112, DR-113, DR-114,
   DR-115, DR-116, DR-117, DR-118, DR-120, DR-122, DR-124, DR-125,
   DR-126, or DR-127. Does not overturn D-106 (corpus recording),
   D-107, D-108, D-109, D-110, D-111, D-112, D-113, D-114, D-115,
   D-116, D-117, D-118, D-119, D-120, or D-121.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains design; G16 evidence
  remains at qualification; D-096 (A) is unsatisfied.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D124.
