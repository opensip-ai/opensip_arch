# D-112 draft — Record secret-storage-contract.v3 as DR-108's accepted design-contract successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111.
> **Subject:** `docs/coop/artifacts/secret-storage-contract.v3.json`
> only.

This is coordinator decision **D-112**. It is not register row
**DR-112** (signed-index trust). D-111 remains the adopted
anti-lockstep-v7 recording. This cycle does not retarget any
D-110 or D-111 draft.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| secret-storage-contract.v3.json | `2919b5cd77782cdb3785650390de6b25725c850bd5b359bf7fccd62265651923` |
| Claude 2 verdict | `1d198228f0eca04ac0bc62ad845be24156ec6409a698a40b4a356c0ae2b99857` ACCEPT, 0/0, advisories ADV-1/ADV-2 |
| Codex verdict | `9561dee0c1584b00b885135a30b5e145095e4ea9d616005aee3005a7a4513261` ACCEPT, 0/0 |
| COORDINATOR-DECISIONS.md | `2cbf74b3cc244375ccc958a21363a202c1ce8fc1592f1ca1d3e3571253c891ee` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files are mode 0444
at the measured digests. HEAD is `63518e5` (D-111 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `secret-storage-contract.v3.json` as DR-108's accepted
   design-contract **successor candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-108 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. OS keychain
   and user-file fallback remain proposed and unexercised in the
   first slice. Exact APIs remain reserved. The candidate binds
   NOTHING. D-056 Class A is not opened.
3. Claude advisories ADV-1/ADV-2 travel as honesty work. They are
   not SHOULD-FIX and do not block this recording.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not dispose DR-117.
   Does not SATISFY DR-103, DR-107, DR-110 (register row),
   DR-111, DR-112, DR-120, DR-121, DR-122, DR-124, DR-125,
   DR-126, or DR-127. Does not overturn D-106, D-107, D-108
   (the packaging recording), D-109, D-110, or D-111.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains design; keychain is
  unexercised; no threat-model evidence is authored.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D112.
