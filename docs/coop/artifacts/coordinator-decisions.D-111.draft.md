# D-111 draft — Record anti-lockstep-contract.v7 as DR-127's accepted design-contract successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109 / D-110.
> **Subject:** `docs/coop/artifacts/anti-lockstep-contract.v7.json`
> only.

This is coordinator decision **D-111**. It is not register row
**DR-111**. D-110 remains the adopted SDK-v4 recording. This cycle
does not retarget any D-110 draft.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| anti-lockstep-contract.v7.json | `8c41bddd7c351abc3a0b4b721f9302df29ba7d053352cb950ec8b23e4afdd671` |
| Claude 2 verdict | `73fb7bde942b1b393faa928c4db3538fb7dfa58faee6bb8f4ad66368d2a67235` ACCEPT, 0/0, advisory CLAUDE-V7-A-1 |
| Codex verdict | `9f1adab71c6231a0e72a37f301f5e253453f2a76f1545739e27f40eba30d9663` ACCEPT, 0/0 |
| COORDINATOR-DECISIONS.md | `913eb753e6d24643c2cf028f545a93becd0dc4b98498f4917f2ef5e535ae6349` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files are mode 0444
at the measured digests. HEAD is `8daa2e6` (D-110 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `anti-lockstep-contract.v7.json` as DR-127's accepted
   design-contract **successor candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-127 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. Hostile
   dual-channel goldens remain named, not authored here. CC-1..CC-11
   remain specifications (D-015), not this row's executed SATISFIED
   evidence. The candidate binds NOTHING. D-056 Class A is not opened.
3. Claude advisory CLAUDE-V7-A-1 (nine booked advisories ride
   unfolded across three rounds) travels as honesty work. It is not
   a SHOULD-FIX and does not block this recording.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not dispose DR-117.
   Does not SATISFY DR-103, DR-107, DR-108, DR-110 (register row),
   DR-111, DR-112, DR-120, DR-121, DR-122, DR-124, DR-125, or
   DR-126. Does not overturn D-106, D-107, D-108, D-109, or D-110.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains design; goldens are
  not authored; G16/G18/G21 are not QUALIFIED by this recording.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D111.
