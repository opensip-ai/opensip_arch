# D-109 draft — Record permission-truth-tables.v6 as DR-105's accepted design-contract successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT-WITH-ADVISORIES (0 blockers, 0 SHOULD-FIX from both
> reviewers). Same form as the adopted set D-013 / D-015 / D-035 /
> D-042 / D-103 / D-104 / D-105 / D-106 / D-107 / D-108.
> **Subject:** `docs/coop/artifacts/permission-truth-tables.v6.json`
> only.

This is coordinator decision **D-109**. It is not register row
**DR-109**.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| permission-truth-tables.v6.json | `ad1bb75d7f029f64979d3c4e6fe5dd3446cd30465b36d4a7b3f9471f06a6dd34` |
| Claude 2 verdict | `9ec9f0563030e5bb06880fff1f8b483fde28e05465e5cc19d9d1087b08b1e20b` ACCEPT-WITH-ADVISORIES, 0/0, ADV-V6-01 |
| Codex verdict | `431f9b8629d947825dcaa2ed9289c84c3f376460dcffba80afe700803bbe3a21` ACCEPT-WITH-ADVISORIES, 0/0, CODEX-V6-A1 |
| COORDINATOR-DECISIONS.md | `c8933f7432e01c5a3584d83cd9e14080590ecdd9a093ffdd42748bf28228eb19` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files are mode 0444
at the measured digests.

Finding-id collision discipline: Claude `ADV-V6-01` is
`CLAUDE-V6-A1` (v4-roster durability). Codex `CODEX-V6-A1` is a
different finding (D-104 COORD snapshot no longer live after later
C-cycles). They travel separately.

## Decision

1. Record `permission-truth-tables.v6.json` as DR-105's accepted
   design-contract **successor candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX. D-042 remains
   the historical recording of permission-truth-tables.v2 and is
   not overturned.
2. Advisories CLAUDE-V6-A1 and CODEX-V6-A1 travel as honesty
   work. Do not retarget perm v6.
3. DR-105 stays `OPEN`. No `SATISFIED`. Host-effect candidate
   remains D-093 / v8. Joint-owner FC-C1, DR-G09 execution, and
   BLK-1..BLK-4 remain. D-056 Class A is not opened.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not dispose DR-117.
   Does not SATISFY DR-103, DR-107, DR-111, DR-112, or DR-120.
   Does not overturn D-106, D-107, or D-108.

## Alternatives

- Wait for a v7 that folds both advisories. Rejected: 0/0 is the
  gate; advisories travel.
- Mark SATISFIED. Rejected: FC-C1, G09, BLK-1..4 remain; leftover
  is not measurement-only.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D109.
