# D-122 draft — Record third-party-policy-contract.v1 as DR-116's accepted design-contract leftover T2-02 candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 / D-112 /
> D-113 / D-114 / D-115 / D-116 / D-117 / D-119 / D-118 / D-120.
> **Subject:** `docs/coop/artifacts/third-party-policy-contract.v1.json`
> only.

This is coordinator decision **D-122**. It is not register row
**DR-122** (SARIF projection; recorded as a candidate at D-115).
D-120 remains the last adopted recording (storage-mechanics v5).
D-121 is in review and is not retargeted. This cycle does not
retarget any D-110 through D-121 draft.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| third-party-policy-contract.v1.json | `78386c7a386376508d9f44d8a3fbe1388b7c1b78798bceb74ab83002ab3ef442` |
| Claude 2 verdict | `dd8f6f7ace90c598e7fff2282c6d31b595a9a0d00fdbca47613f4e24d26a61f0` ACCEPT, 0/0, advisories TPP-C2-A1..A4 |
| Codex verdict | `dfb773685e08d552eb166620649b3b2b0ab5901f0b6c882e00a6912ea9c930a9` ACCEPT, 0/0 |
| COORDINATOR-DECISIONS.md | `ac10b3f9c6832d4450632df5095ce42083277718f6d571f78c2b2a522c8a8c98` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves in a way that is not append-only COORD growth
with file 08, the v1 subject, both v1 verdicts, and this draft
unmoved, re-measure before adoption. Append-only COORD after this
remasurement, with those files unmoved, is **PASS-NO-SCOPE-EFFECT**
and is not a MUST-FIX. The apply writer re-measures COORD at
adoption.

Both verdict files are mode 0444 at the measured digests. HEAD is
`e4fd117` (D-120 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `third-party-policy-contract.v1.json` as DR-116's accepted
   design-contract leftover T2-02 **successor candidate**. Both
   independent reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-116 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. D-002
   records "no third-party support policy needed yet." The
   candidate binds NOTHING. D-056 Class A is not opened.
   Recording this candidate is not a D-096 (A) grant.
3. Claude advisories TPP-C2-A1, TPP-C2-A2, TPP-C2-A3, and
   TPP-C2-A4 travel as honesty work. They are not SHOULD-FIX and
   do not block this recording.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not SATISFY DR-101, DR-103,
   DR-106, DR-108, DR-109, DR-110, DR-111, DR-112, DR-113, DR-114,
   DR-115, DR-117, DR-118, DR-120, DR-121, DR-122, DR-124, DR-125,
   DR-126, or DR-127. Does not overturn D-106 (corpus recording),
   D-107, D-108 (packaging recording), D-109, D-110, D-111, D-112,
   D-113, D-114, D-115, D-116, D-117, D-118, D-119, or D-120.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains design; D-002 defers
  the policy from slice 1; D-096 (A) is unsatisfied.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D122.
