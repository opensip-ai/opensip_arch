# D-123 draft — Record identity-namespace-integration-contract.v3 as DR-104's leftover-integration T2-02 candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 / D-112 /
> D-113 / D-114 / D-115 / D-116 / D-117 / D-119 / D-118 / D-120.
> **Subject:** `docs/coop/artifacts/identity-namespace-integration-contract.v3.json`
> only.

This is coordinator decision **D-123**. It is not register row
**DR-123** (CLI baseline; SATISFIED at D-092). D-120 remains the
last adopted recording. D-121 and D-122 are in review and are not
retargeted. This cycle does not retarget any D-110 through D-122
draft.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| identity-namespace-integration-contract.v3.json | `57bf89826c5c4ff6658bbea5f68b0b049abb134cb19001cd670f15cc0ef97091` |
| Claude 2 verdict | `881c9df77635090239172fef7d66aae2105ba259b696c26cbc252e78fa4fbfd7` ACCEPT, 0/0, advisories INIC-V3-CL-ADV-1 / INIC-V3-CL-ADV-2 |
| Codex verdict | `30fb71405a7286dcfcc7fb73eedd8625d91636fbcd9980f902ba80930fbf1332` ACCEPT, 0/0 |
| COORDINATOR-DECISIONS.md | `ac10b3f9c6832d4450632df5095ce42083277718f6d571f78c2b2a522c8a8c98` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves in a way that is not append-only COORD growth
with file 08, the v3 subject, both v3 verdicts, and this draft
unmoved, re-measure before adoption. Append-only COORD after this
remasurement, with those files unmoved, is **PASS-NO-SCOPE-EFFECT**
and is not a MUST-FIX. The apply writer re-measures COORD at
adoption.

Both verdict files are mode 0444 at the measured digests. HEAD is
`e4fd117` (D-120 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `identity-namespace-integration-contract.v3.json` as
   DR-104's leftover-integration T2-02 **successor candidate**.
   Both independent reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-104 stays `DECIDED-V1-NOT-INTEGRATED`. leftover-design/OPEN
   is a finding against a recording of this row. No `SATISFIED`.
   No `QUALIFIED`. The candidate binds NOTHING. D-056 Class A is
   not opened. Recording this candidate is not a D-096 (A) grant.
3. Claude advisories INIC-V3-CL-ADV-1 and INIC-V3-CL-ADV-2 travel
   as honesty work. They are not SHOULD-FIX and do not block this
   recording.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not SATISFY DR-101, DR-103,
   DR-106, DR-108, DR-109, DR-110, DR-111, DR-112, DR-113, DR-114,
   DR-115, DR-116, DR-117, DR-118, DR-120, DR-121, DR-122, DR-124,
   DR-125, DR-126, or DR-127. Does not overturn D-012, D-106
   (corpus recording), D-107, D-108, D-109, D-110, D-111, D-112,
   D-113, D-114, D-115, D-116, D-117, D-118, D-119, or D-120.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains integration; D-096
  (A) is unsatisfied; negative tests remain unauthored.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.
- Relabel the file 08 token leftover-design/OPEN. Rejected:
  D115-MF-1.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D123.
