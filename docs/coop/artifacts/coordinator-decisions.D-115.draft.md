# D-115 draft — Record sarif-projection-contract.v15 as DR-122's accepted design-contract successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 / D-112 /
> D-113 / D-114.
> **Subject:** `docs/coop/artifacts/sarif-projection-contract.v15.json`
> only.

This is coordinator decision **D-115**. It is not register row
**DR-115** (numeric thresholds; SATISFIED at D-089). D-114 remains
the adopted inventory-v16 recording. This cycle does not retarget
any D-110, D-111, D-112, D-113, or D-114 draft.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| sarif-projection-contract.v15.json | `8996a92d00ddd47d212dbeecaf51f25b77b90d87aaa618cda9ad00749fd1d589` |
| Claude 2 verdict | `fe5f55181b305c5cafd3993b672d30296b7d62c7f10dd236585a81bd99aaaad0` ACCEPT, 0/0, advisory ADV-1 (qualify CLAUDE-V15-ADV-1) |
| Codex verdict | `9f402c72267ed7c92657a1aa38e4c0fc185a25eaf23bb7aad69042dd9dbfad76` ACCEPT, 0/0, advisory SARIFV15-A1 |
| COORDINATOR-DECISIONS.md | `7da759558e74222c533ec0d4a0ea26c7f5712699aaff930dad0af70d480af3d1` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files are mode 0444
at the measured digests. HEAD is `7acef4f` (D-114 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `sarif-projection-contract.v15.json` as DR-122's accepted
   design-contract **successor candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-122 stays leftover-design / OPEN. No `SATISFIED`. No
   `QUALIFIED`. Preview still does not advertise SARIF. G17 stays
   inapplicable. The candidate binds NOTHING. D-056 Class A is not
   opened.
3. Claude advisory CLAUDE-V15-ADV-1 (ADV-1) and Codex advisory
   SARIFV15-A1 travel as honesty work. They are not SHOULD-FIX and
   do not block this recording.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not dispose DR-117.
   Does not SATISFY DR-101, DR-103, DR-108, DR-110 (register row),
   DR-111, DR-112, DR-113, DR-114, DR-115, DR-118, DR-120, DR-121,
   DR-124, DR-125, DR-126, or DR-127. Does not overturn D-106,
   D-107, D-108 (packaging recording), D-109, D-110, D-111, D-112,
   D-113, or D-114.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains design; preview does
  not advertise SARIF; no qualification.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D115.
