# D-117 draft — Record state-class-contract.v11 as DR-124's accepted design-contract successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 / D-112 /
> D-113 / D-114 / D-115 / D-116.
> **Subject:** `docs/coop/artifacts/state-class-contract.v11.json`
> only.

This is coordinator decision **D-117**. It is not register row
**DR-117** (product-boundary; recorded as a candidate at D-116).
D-116 remains the adopted product-boundary-v8 recording. This
cycle does not retarget any D-110 through D-116 draft.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| state-class-contract.v11.json | `b5456c63e865b53738b1f11f46a898438afca7890a6069a8653aad6ea78d86bb` |
| Claude 2 verdict | `c20dc0cc4fd786ef4c5080dee23fe11bd8bfbfa5f963e831efcf39c39dfa3422` ACCEPT, 0/0 |
| Codex verdict | `6c40f95aaa0c2e34345942a19662f035368a81a6008a54709a2fe815f2837c75` ACCEPT, 0/0 |
| COORDINATOR-DECISIONS.md | `5fbd89eb162e112e44bab84b1b463fc8800660fc74abf3df3dead09a1e8079ee` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files are mode 0444
at the measured digests. HEAD is `0a2f605` (D-116 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `state-class-contract.v11.json` as DR-124's accepted
   design-contract **successor candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-124 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`.
   Grant-journal assignment remains a proposed supersession. The
   candidate binds NOTHING. D-056 Class A is not opened.
3. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
4. Does not mint a D-096 (A) grant. Does not dispose DR-117.
   Does not SATISFY DR-101, DR-103, DR-108, DR-110 (register
   row), DR-111, DR-112, DR-113, DR-114, DR-115, DR-116
   (register row), DR-117, DR-118, DR-120, DR-121, DR-122,
   DR-125, DR-126, or DR-127. Does not overturn D-106, D-107,
   D-108 (packaging recording), D-109, D-110, D-111, D-112,
   D-113, D-114, D-115, or D-116.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains design; owner
  concurrence on SUP-124-GRANT-JOURNAL is still required.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D117.
