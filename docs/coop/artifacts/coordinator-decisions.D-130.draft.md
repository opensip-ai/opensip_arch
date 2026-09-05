# D-130 draft — Record identity-namespace-negative-test-corpus.v1 as DR-104 leftover T2-02 successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-093 / D-103 /
> D-104 / D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 /
> D-112 / D-113 / D-114 / D-115 / D-116 / D-117 / D-119 / D-118 /
> D-120 / D-121 / D-122 / D-123 / D-124 / D-125 / D-126 / D-127 /
> D-128 / D-129.
> **Subject:** `docs/coop/artifacts/identity-namespace-negative-test-corpus.v1.json`
> only.

This is coordinator decision **D-130**. It is not register row
**DR-130** (V1→V2 transition; slice 1 claims no upgrade
continuity). D-129 remains the last adopted recording
(doctor-actor-join-integration-contract.v8). This cycle does
not retarget any D-110 through D-129 draft. It does not
retarget D-123 or recorded identity v3. It does not retarget
D-106 or recorded corpus v6. It does not retarget D-104
(schemas v11), D-012, D-129, D-128, D-127, D-035, D-093, or
D-126.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| identity-namespace-negative-test-corpus.v1.json | `2c0795cd58e95e56afad46899b3c5d546d4fb520e38e1a8c3f7c132aa69583dd` |
| Claude 2 verdict | `7c84969cb06d26c01cd8c5de3f0c99908cc2abe274f5b5f33a2d33258e86fbda` ACCEPT, 0/0, advisories CLAUDE-NTC-V1-ADV-1 / CLAUDE-NTC-V1-ADV-2 |
| Codex verdict | `8676bac78cbde7415fb9ba3218f5bb1d0efcb0daf716cf37a1f6bfd805e7ed81` ACCEPT, 0/0 |
| identity v3 (D-123; unmoved) | `57bf89826c5c4ff6658bbea5f68b0b049abb134cb19001cd670f15cc0ef97091` |
| corpus v6 (D-106; unmoved) | `8dfa9346ada4fefce0aabca96062208e4fea7371a6aab68eaee75cdc908a21a5` |
| COORDINATOR-DECISIONS.md | `780a79410ade916e94a92a8e5e4fa6f519e89b335f896bef9bc46d39e4847c5c` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves in a way that is not append-only COORD growth
with file 08, the v1 subject, both v1 verdicts, recorded identity
v3, recorded corpus v6, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remasurement, with those
files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.
The apply writer re-measures COORD at adoption.

Both verdict files are mode 0444 at the measured digests. HEAD is
`351748d` (D-129 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `identity-namespace-negative-test-corpus.v1.json` as
   DR-104's leftover T2-02 **successor candidate**. Both
   independent reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-104 stays `DECIDED-V1-NOT-INTEGRATED`. leftover-design/OPEN
   is a finding against a recording of this row. No `SATISFIED`.
   No `QUALIFIED`. The candidate binds NOTHING. D-056 Class A
   is not opened. This recording is not a Class B SATISFIED
   re-record. Recording this candidate is not a D-096 (A) grant.
3. Identity v3 `57bf8982…` remains the D-123 subject. This
   recording does not retarget D-123 and does not rewrite
   identity v3's NAMED-NOT-AUTHORED standing string. Corpus v6
   `8dfa9346…` remains the D-106 subject and is not applied.
   This recording does not mutate `fixtures/dr-103.v2/` or
   `fixtures/dr-103.v4/` and does not execute any fixture.
4. Claude advisories CLAUDE-NTC-V1-ADV-1 / CLAUDE-NTC-V1-ADV-2
   travel as honesty work. They are not SHOULD-FIX and do not
   block this recording.
5. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
6. Does not mint a D-096 (A) grant. Does not SATISFY DR-101, DR-103,
   DR-104, DR-105, DR-106, DR-108, DR-109, DR-110, DR-111, DR-112,
   DR-113, DR-114, DR-115, DR-116, DR-117, DR-118, DR-120, DR-121,
   DR-122, DR-124, DR-125, DR-126, or DR-127. Does not overturn
   D-012, D-032, D-035, D-042, D-093, D-104 (schemas recording),
   D-106 (corpus recording), D-107, D-108, D-109, D-110, D-111,
   D-112, D-113, D-114, D-115, D-116, D-117, D-118, D-119, D-120,
   D-121, D-122, D-123, D-124, D-125, D-126, D-127, D-128, or
   D-129.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: execution remains at qualification;
  D-056 Class B SATISFIED is a later dedicated cycle; D-096 (A)
  is unsatisfied; leftover-design/OPEN would be a finding.
- Treat dual ACCEPT as application, seal, or fixture execution.
  Rejected: binds NOTHING.
- Retarget D-123 / v3 or D-106 / v6. Rejected: those subjects remain.
- Mutate the DR-103 fixture tree. Rejected: catalog only.
- Treat adopted D-106 as SATISFYING DR-103. Rejected: D-013
  SATISFIED-refusal stands; D-106 records without SATISFYING.
- Mint a D-096 (A) grant. Rejected: naming is not minting.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D130.
