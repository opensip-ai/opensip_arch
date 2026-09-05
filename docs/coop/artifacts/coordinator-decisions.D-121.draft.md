# D-121 draft — Record self-update-repair-contract.v3 as DR-110's accepted design-contract successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 / D-112 /
> D-113 / D-114 / D-115 / D-116 / D-117 / D-119.
> **Subject:** `docs/coop/artifacts/self-update-repair-contract.v3.json`
> only.

This is coordinator decision **D-121**. It is not register row
**DR-121** (monorepo CI; leftover T2-02 still in review at v12).
D-119 remains the last adopted recording (replay-purge v2).
D-118 and D-120 are in review and are not retargeted.
This cycle does not retarget any D-110 through D-120 draft.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| self-update-repair-contract.v3.json | `73a44c2b07a2b8e8db48497a04557d99d65f91497a717eaf2fdf07fc8008690a` |
| Claude 2 verdict | `c4f3cb59c2aacce310f34cf602560850cd2916b52d6142c9e0a00ea91e11df38` ACCEPT, 0/0 |
| Codex verdict | `e21b1e33bf2b235367f80bec53cb2ec950b77d27be4988d87c9e441d8cecc8b3` ACCEPT, 0/0 |
| COORDINATOR-DECISIONS.md | `f7d22fa5eb2a3c1e5a4d28077164c5534bf0a72dcf275f0423e79cb2483b4f72` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves in a way that is not append-only COORD growth
with file 08, the v3 subject, both v3 verdicts, and this draft
unmoved, re-measure before adoption. Append-only COORD after this
remasurement, with those files unmoved, is **PASS-NO-SCOPE-EFFECT**
and is not a MUST-FIX. The apply writer re-measures COORD at
adoption.

Both verdict files are mode 0444 at the measured digests. HEAD is
`f5a0082` (D-119 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `self-update-repair-contract.v3.json` as DR-110's accepted
   design-contract **successor candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-110 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. D-002
   defers self-update/repair from slice 1 (fresh signed download).
   The owner disposition remains unrecorded and is blocked on the
   lawful owner/grant path. The candidate binds NOTHING. D-056
   Class A is not opened. Recording this candidate is not a
   D-096 (A) grant.
3. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
4. Does not mint a D-096 (A) grant. Does not SATISFY DR-101, DR-103,
   DR-106, DR-108, DR-109, DR-111, DR-112, DR-113, DR-114, DR-115,
   DR-116 (register row), DR-117, DR-118, DR-120, DR-121, DR-122,
   DR-124, DR-125, DR-126, or DR-127. Does not overturn D-106
   (corpus recording), D-107, D-108 (packaging recording), D-109,
   D-110 (SDK recording), D-111, D-112, D-113, D-114, D-115,
   D-116, D-117, or D-119.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains design; D-002 defers
  the row from slice 1; owner disposition unrecorded; D-096 (A)
  is unsatisfied.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D121.
