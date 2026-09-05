# D-129 draft — Record doctor-actor-join-integration-contract.v8 as DR-114 leftover-integration T2-02 successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-093 / D-103 /
> D-104 / D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 /
> D-112 / D-113 / D-114 / D-115 / D-116 / D-117 / D-119 / D-118 /
> D-120 / D-121 / D-122 / D-123 / D-124 / D-125 / D-126 / D-127 /
> D-128.
> **Subject:** `docs/coop/artifacts/doctor-actor-join-integration-contract.v8.json`
> only.

This is coordinator decision **D-129**. It is not register row
**DR-129** (optional TUI; deferred). D-128 remains the last adopted
recording (permission-truth-tables.v9). This cycle does not
retarget any D-110 through D-128 draft. It does not retarget
D-127 or recorded actor-join v6. It does not retarget D-128 or
permission-truth-tables.v9. It does not retarget D-035, D-093,
or D-126.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| doctor-actor-join-integration-contract.v8.json | `c830f954605a4a1d47c5643230439340994a0c42c4a487359541c578d00bc662` |
| Claude 2 verdict | `8f596a0b89e73f426295d8053f0e4a5b8a4fc37beff5047479ae67a4856cbbbf` ACCEPT, 0/0, advisory CLAUDE-DAJ7-A1 |
| Codex verdict | `20e9a013dce668f47f18fdf765ba6d1abeba0cc2d66719ab6b6687e079c1c724` ACCEPT, 0/0 |
| actor-join v6 (D-127; unmoved) | `f63554d534d249dfdb674be3c78b61bbd1a4a4bdeb56cb06247b24c647ab38d1` |
| permission-truth-tables.v9 (D-128; unmoved) | `05d559647d103a47c18ed5177b71900a1d9dfcdea6b9a1255aefcec5f09eaccb` |
| COORDINATOR-DECISIONS.md | `0ef537f04d396944aa298bb3bb33f8e1b52d662fef97275935a5aff477b9310e` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves in a way that is not append-only COORD growth
with file 08, the v8 subject, both v8 verdicts, recorded v6,
recorded perm v9, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remasurement, with those
files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.
The apply writer re-measures COORD at adoption.

Both verdict files are mode 0444 at the measured digests. HEAD is
`e0232a6` (D-128 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `doctor-actor-join-integration-contract.v8.json` as
   DR-114's leftover-integration T2-02 **successor candidate**.
   Both independent reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-114 stays `OPEN`. leftover-design/OPEN is not a finding
   against a recording of this row. No `SATISFIED`. No
   `QUALIFIED`. G09 is not QUALIFIED. The candidate binds
   NOTHING. D-056 Class A is not opened. Recording this
   candidate is not a D-096 (A) grant.
3. Actor-join v6 `f63554d5…` remains the D-127 subject. This
   recording does not retarget D-127. Permission-truth-tables.v9
   `05d55964…` remains the D-128 subject and is not applied.
4. Claude advisory CLAUDE-DAJ7-A1 travels as honesty work. It is
   not SHOULD-FIX and does not block this recording.
5. Does not record FC-C1, admit CA-1 IN_PROCESS, or mint the later
   D-000 CA-2 gate.
6. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
7. Does not mint a D-096 (A) grant. Does not SATISFY DR-101, DR-103,
   DR-104, DR-105, DR-106, DR-108, DR-109, DR-110, DR-111, DR-112,
   DR-113, DR-114, DR-115, DR-116, DR-117, DR-118, DR-120, DR-121,
   DR-122, DR-124, DR-125, DR-126, or DR-127. Does not overturn
   D-032, D-035, D-042, D-093, D-106 (corpus recording), D-107,
   D-108, D-109, D-110, D-111, D-112, D-113, D-114, D-115, D-116,
   D-117, D-118, D-119, D-120, D-121, D-122, D-123, D-124, D-125,
   D-126, D-127, or D-128.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains fixture-execution
  and FC-C1; D-096 (A) is unsatisfied; doctor v4 ID-DEP-12 remains
  NAMED, NOT RESOLVED.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.
- Retarget D-127 / v6 or D-128 / v9. Rejected: those subjects remain.
- Apply permission-truth-tables.v9. Rejected: leftover-integration
  names environment only.
- Mint the later D-000 CA-2 gate or a D-096 (A) grant. Rejected:
  naming is not minting.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D129.
