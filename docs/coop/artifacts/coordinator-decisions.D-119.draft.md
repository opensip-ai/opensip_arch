# D-119 draft — Record replay-purge-contract.v2 as DR-113's accepted design-contract successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 / D-112 /
> D-113 / D-114 / D-115 / D-116 / D-117.
> **Subject:** `docs/coop/artifacts/replay-purge-contract.v2.json`
> only.

This is coordinator decision **D-119**. It is not register row
**DR-119** (runtime/tool closure; SATISFIED at D-091 / D-056 Class B).
D-117 remains the last adopted recording (state-class v11).
D-118 (DR-106 candidate recording) is in review and is not
retargeted. This cycle does not retarget any D-110 through D-118
draft.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| replay-purge-contract.v2.json | `48cb28a5ea3a5609b2b74474a7599a386daeb7c373ec662241d35cd92b6a82e2` |
| Claude 2 verdict | `20ad538feeeb3b0e695a9e2b5b9030eb451cd5e8f648346812115ff897da9e2e` ACCEPT, 0/0, advisories CLAUDE-RP2-ADV-1 / CLAUDE-RP2-ADV-2 |
| Codex verdict | `969c89fb43db9971cef85a37e729f9c92b38f1c512c472e05036c65e0c4b9e51` ACCEPT, 0/0 |
| COORDINATOR-DECISIONS.md | `673a7a4307a1cb00f9c998986edbe2f882e7e85f4d3bfc5985173a89ff6d68f2` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves in a way that is not append-only COORD growth
with file 08, the v2 subject, both v2 verdicts, and this draft
unmoved, re-measure before adoption. Append-only COORD after this
remasurement, with those files unmoved, is **PASS-NO-SCOPE-EFFECT**
and is not a MUST-FIX. The apply writer re-measures COORD at
adoption.

Both verdict files are mode 0444 at the measured digests. HEAD is
`d624057` (D-117 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `replay-purge-contract.v2.json` as DR-113's accepted
   design-contract **successor candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-113 stays `OPEN / inherits hard blockers`. No `SATISFIED`.
   No `QUALIFIED`. D-002 defers this row WHOLLY from slice 1; this
   candidate is for the later slice that includes authoritative
   sealed closure, replay, and evidence custody. The candidate
   binds NOTHING. D-056 Class A is not opened. Recording this
   candidate is not a D-096 (A) grant.
3. Claude advisories CLAUDE-RP2-ADV-1 / CLAUDE-RP2-ADV-2 travel as
   honesty work. They are not SHOULD-FIX and do not block this
   recording.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not SATISFY DR-101, DR-103,
   DR-106, DR-108, DR-109, DR-110 (register row), DR-111, DR-112,
   DR-114, DR-115, DR-116 (register row), DR-117, DR-118, DR-120,
   DR-121, DR-122, DR-124, DR-125, DR-126, or DR-127. DR-119 is
   already SATISFIED at D-091 and is not listed here as a row this
   recording could SATISFY. Does not overturn D-106 (corpus
   recording), D-107, D-108 (packaging recording), D-109, D-110,
   D-111, D-112, D-113, D-114, D-115, D-116, or D-117.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains design; D-002 WHOLLY
  defers the row from slice 1; D-096 (A) is unsatisfied.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D119.
