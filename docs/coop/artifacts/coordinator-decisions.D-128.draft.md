# D-128 draft — Record permission-truth-tables.v9 as DR-105 leftover T2-02 successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-093 / D-103 /
> D-104 / D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 /
> D-112 / D-113 / D-114 / D-115 / D-116 / D-117 / D-119 / D-118 /
> D-120 / D-121 / D-122 / D-123 / D-124 / D-125 / D-126 / D-127.
> **Subject:** `docs/coop/artifacts/permission-truth-tables.v9.json`
> only.

This is coordinator decision **D-128**. It is not register row
**DR-128** (third-party sandbox; deferred post-MVP by recorded
scope). D-127 remains the last adopted recording
(doctor-actor-join-integration-contract.v6). This cycle does not
retarget any D-110 through D-127 draft. It does not retarget
D-042 or permission-truth-tables.v2. It does not retarget D-109
or permission-truth-tables.v6. It does not retarget D-093,
D-126, or D-127.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| permission-truth-tables.v9.json | `05d559647d103a47c18ed5177b71900a1d9dfcdea6b9a1255aefcec5f09eaccb` |
| Claude 2 verdict | `ed192b68a08bcafbdc3a3f716e2cf1db77b8b2c60fb7bfa7769fe24c4e7c049f` ACCEPT-WITH-ADVISORIES, 0/0, advisories CLAUDE-V9-ADV-1 / CLAUDE-V9-ADV-2 |
| Codex verdict | `cec59dc540adeb6f87068f949970f813ad0abb30f27214522ed3001b79d3c854` ACCEPT, 0/0 |
| permission-truth-tables.v6 (D-109; unmoved) | `ad1bb75d7f029f64979d3c4e6fe5dd3446cd30465b36d4a7b3f9471f06a6dd34` |
| permission-truth-tables.v2 (D-042; unmoved) | `cce3afcaee90bbca388825a474751d6ebb17b30722b35dadcf6c631b34a8731a` |
| COORDINATOR-DECISIONS.md | `60417343c1fcc407b703bb005de0e5e7b216a160769cf1b89ff7578c6fb56ad5` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves in a way that is not append-only COORD growth
with file 08, the v9 subject, both v9 verdicts, recorded v6,
recorded v2, and this draft unmoved, re-measure before adoption.
Append-only COORD after this remasurement, with those files
unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX. The
apply writer re-measures COORD at adoption.

Both verdict files are mode 0444 at the measured digests. HEAD is
`12a2c2b` (D-127 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `permission-truth-tables.v9.json` as DR-105's leftover
   T2-02 **successor candidate**. Both independent reviewers
   returned 0 blockers and 0 SHOULD-FIX.
2. DR-105 stays `OPEN`. leftover-design/OPEN is not a finding
   against a recording of this row. No `SATISFIED`. No
   `QUALIFIED`. G09 is not QUALIFIED. The candidate binds
   NOTHING. D-056 Class A is not opened. Recording this
   candidate is not a D-096 (A) grant.
3. Permission-truth-tables.v6 `ad1bb75d…` remains the D-109
   subject. Permission-truth-tables.v2 `cce3afca…` remains the
   D-042 subject. This recording does not apply v2 or v6 and
   does not retarget D-042 or D-109.
4. Claude advisories CLAUDE-V9-ADV-1 and CLAUDE-V9-ADV-2 travel
   as honesty work. They are not SHOULD-FIX and do not block
   this recording.
5. Does not record FC-C1, apply host-effect, admit CA-1
   IN_PROCESS, or mint the later D-000 CA-2 gate.
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
   D-126, or D-127.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains FC-C1, G09
  execution, and BLK-1..BLK-4; D-096 (A) is unsatisfied.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.
- Retarget D-042 / v2 or D-109 / v6. Rejected: those subjects remain.
- Mint the later D-000 CA-2 gate or a D-096 (A) grant. Rejected:
  naming is not minting.
- Admit CA-1 IN_PROCESS. Rejected: recorded host-effect classifies
  it UNEXERCISABLE in the architecture preview.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D128.
