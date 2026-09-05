# D-116 draft — Record product-boundary-successor-contract.v8 as DR-117's accepted design-contract successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 / D-112 /
> D-113 / D-114.
> **Subject:** `docs/coop/artifacts/product-boundary-successor-contract.v8.json`
> only.

This is coordinator decision **D-116**. It is not register row
**DR-116** (third-party publisher/support/vulnerability/revocation
policy). D-115, if later adopted, remains the SARIF-v15 recording.
This cycle does not retarget any D-110, D-111, D-112, D-113, D-114,
or D-115 draft.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| product-boundary-successor-contract.v8.json | `52c70f7715fb869bae70bc588043dc5b4d731b73408d2d451e868b8de963f362` |
| Claude 2 verdict | `7e48d2d4f0c5b5305f9427b04ddb60450dccfe51f708fb639078c28e065a0b48` ACCEPT-WITH-ADVISORIES, 0/0, advisories PBSCV8-A1 / PBSCV8-A2 (qualify CLAUDE-V8-A1 / CLAUDE-V8-A2) |
| Codex verdict | `938666820e114972bef8fd431dccfa16cb189d147f8b08b8580acd30bbd5acda` ACCEPT, 0/0 |
| COORDINATOR-DECISIONS.md | `7da759558e74222c533ec0d4a0ea26c7f5712699aaff930dad0af70d480af3d1` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files are mode 0444
at the measured digests. HEAD is `7acef4f` (D-114 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `product-boundary-successor-contract.v8.json` as DR-117's
   accepted design-contract **successor candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-117 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. Preview
   exclusion (D-066/D-068) is not this row SATISFIED. The seven
   binding items remain extracted, not implemented. The candidate
   binds NOTHING. D-056 Class A is not opened.
3. Claude advisories CLAUDE-V8-A1 (PBSCV8-A1) and CLAUDE-V8-A2
   (PBSCV8-A2) travel as honesty work. They are not SHOULD-FIX and
   do not block this recording.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not SATISFY DR-101, DR-103,
   DR-108, DR-110 (register row), DR-111, DR-112, DR-113, DR-114,
   DR-115, DR-116, DR-118, DR-120, DR-121, DR-122, DR-124, DR-125,
   DR-126, or DR-127. Does not overturn D-106, D-107, D-108 (the
   packaging recording), D-109, D-110, D-111, D-112, D-113, or
   D-114.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains design; preview is not
  this row; no enforcement evidence is authored.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D116.
