# D-113 draft — Record language-quality-matrix-contract.v13 as DR-118's accepted design-contract successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 / D-112.
> **Subject:** `docs/coop/artifacts/language-quality-matrix-contract.v13.json`
> only.

This is coordinator decision **D-113**. It is not register row
**DR-113** (replay/purge). D-112 remains the adopted
secret-storage-v3 recording. This cycle does not retarget any
D-110, D-111, or D-112 draft.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| language-quality-matrix-contract.v13.json | `9efffdb3f7ec806bc967db5eff5868aea0a7d11524b1e026993a46505d35c2ae` |
| Claude 2 verdict | `c98f6332292720d67b2109920fee6aec0df56c726f6729635bc4fa5f14b146a3` ACCEPT, 0/0, advisories CLAUDE-V13-ADV-1 / CLAUDE-V13-ADV-2 |
| Codex verdict | `ac5cf60ac2a57557168a776cbe1282ce51e5047e6342381d3a6a1313af98e130` ACCEPT, 0/0, advisory LQMCV13-A1 |
| COORDINATOR-DECISIONS.md | `0833973f33895e5e9cc70387b1d821b1cc5ae343e00884e58b1f05f9fc08ba71` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files are mode 0444
at the measured digests. HEAD is `272cbac` (D-112 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `language-quality-matrix-contract.v13.json` as DR-118's
   accepted design-contract **successor candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-118 stays `DECIDED-V1-NOT-INTEGRATED` / leftover-design. No
   `SATISFIED`. No `QUALIFIED`. Numeric thresholds remain UNDECIDED
   (D-007). The matrix/corpus is not authored. The candidate binds
   NOTHING. D-056 Class A is not opened. D-056 Class B remains
   ineligible while thresholds are UNDECIDED.
3. Claude advisories CLAUDE-V13-ADV-1 / CLAUDE-V13-ADV-2 and Codex
   advisory LQMCV13-A1 travel as honesty work. They are not
   SHOULD-FIX and do not block this recording.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not dispose DR-117.
   Does not SATISFY DR-101, DR-103, DR-108, DR-110 (register row),
   DR-111, DR-112, DR-113, DR-120, DR-121, DR-122, DR-124, DR-125,
   DR-126, or DR-127. Does not overturn D-106, D-107, D-108
   (the packaging recording), D-109, D-110, D-111, or D-112.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains design; thresholds
  UNDECIDED; no matrix/corpus authored.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D113.
