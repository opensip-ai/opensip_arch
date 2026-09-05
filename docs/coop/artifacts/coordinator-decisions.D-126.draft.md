# D-126 draft — Record host-effect-authorization.v25 as DR-105 leftover T2-02 successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-093 / D-103 /
> D-104 / D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 /
> D-112 / D-113 / D-114 / D-115 / D-116 / D-117 / D-119 / D-118 /
> D-120 / D-121 / D-122 / D-123 / D-124 / D-125.
> **Subject:** `docs/coop/artifacts/host-effect-authorization.v25.json`
> only.

This is coordinator decision **D-126**. It is not register row
**DR-126** (platform TCB; recorded as a candidate at D-125).
D-125 remains the last adopted recording (platform-tcb-contract v45).
This cycle does not retarget any D-110 through D-125 draft.
It does not retarget D-093 or the recorded v8 subject.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| host-effect-authorization.v25.json | `b91b9f739b10b1bd30eb56b9d68feac81c483ad86f50e11ed33b95e98ae2d9b9` |
| Claude 2 verdict | `e7845d03defac1d5eb409899392cde5bdc5a54d74b992a253ca7caaa0c0c1247` ACCEPT, 0/0, advisories CLAUDE-HEA25-A1 / CLAUDE-HEA25-A2 / CLAUDE-HEA25-A3 |
| Codex verdict | `09fe6ec87e0172bb57dfee696c5464e89de45863a20a637bc7ce1e557c676e99` ACCEPT, 0/0, advisories HAE25-ADV-01 / HAE25-ADV-02 / HAE25-ADV-03 |
| Recorded v8 (D-093; unmoved) | `2cbad5612e546d3bf915074a8ad3fc4cae444122c997e2ddb3fe067d3cd022dc` |
| COORDINATOR-DECISIONS.md | `7d396ca7540780cc40521b6a4265e82c90917de385d799e0bf46a6f05e533667` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves in a way that is not append-only COORD growth
with file 08, the v25 subject, both v25 verdicts, recorded v8, and
this draft unmoved, re-measure before adoption. Append-only COORD
after this remasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX. The apply writer
re-measures COORD at adoption.

Both verdict files are mode 0444 at the measured digests. HEAD is
`01d778c` (D-125 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `host-effect-authorization.v25.json` as DR-105's leftover
   T2-02 **successor candidate**. Both independent reviewers
   returned 0 blockers and 0 SHOULD-FIX.
2. DR-105 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. G09 is
   not QUALIFIED. The candidate binds NOTHING. D-056 Class A is
   not opened. Recording this candidate is not a D-096 (A) grant.
3. Recorded v8 `2cbad561…` remains the D-093 subject. This
   recording does not retarget D-093.
4. Claude advisories CLAUDE-HEA25-A1 / CLAUDE-HEA25-A2 /
   CLAUDE-HEA25-A3 and Codex advisories HAE25-ADV-01 /
   HAE25-ADV-02 / HAE25-ADV-03 travel as honesty work. They are
   not SHOULD-FIX and do not block this recording.
5. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
6. Does not mint a D-096 (A) grant. Does not SATISFY DR-101, DR-103,
   DR-104, DR-105, DR-106, DR-108, DR-109, DR-110, DR-111, DR-112,
   DR-113, DR-114, DR-115, DR-116, DR-117, DR-118, DR-120, DR-121,
   DR-122, DR-124, DR-125, DR-126, or DR-127. Does not overturn
   D-093, D-106 (corpus recording), D-107, D-108, D-109, D-110,
   D-111, D-112, D-113, D-114, D-115, D-116, D-117, D-118, D-119,
   D-120, D-121, D-122, D-123, D-124, or D-125.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains design; G09 evidence
  remains at qualification; D-096 (A) is unsatisfied; actor-join
  remains named-not-resolved.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.
- Retarget D-093 / recorded v8. Rejected: v8 remains the D-093
  subject.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D126.
