# D-127 draft — Record doctor-actor-join-integration-contract.v6 as DR-114 leftover-integration T2-02 candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-093 / D-103 /
> D-104 / D-105 / D-106 / D-107 / D-108 / D-109 / D-110 / D-111 /
> D-112 / D-113 / D-114 / D-115 / D-116 / D-117 / D-119 / D-118 /
> D-120 / D-121 / D-122 / D-123 / D-124 / D-125 / D-126.
> **Subject:** `docs/coop/artifacts/doctor-actor-join-integration-contract.v6.json`
> only.

This is coordinator decision **D-127**. It is not register row
**DR-127** (anti-lockstep; recorded as a candidate at D-111).
D-126 remains the last adopted recording
(host-effect-authorization.v25). This cycle does not retarget any
D-110 through D-126 draft. It does not retarget D-035 or
doctor-contract.v4. It does not retarget D-093 or recorded
host-effect v8. It does not retarget D-126 or recorded
host-effect v25.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| doctor-actor-join-integration-contract.v6.json | `f63554d534d249dfdb674be3c78b61bbd1a4a4bdeb56cb06247b24c647ab38d1` |
| Claude 2 verdict | `1139228d9955827440ffeaaa5db1335bcf30556a2b446d373282b44794c694bc` ACCEPT, 0/0 |
| Codex verdict | `987da6b6b00537b2b581a5adb52ce25048a978fda20f1f71aaf11d08808d4bc4` ACCEPT, 0/0 |
| doctor-contract.v4 (D-035; unmoved) | `df2e717555616db096e61548458f23b442f7f0e37b2d2461eabc2c33201e94b3` |
| host-effect v8 (D-093; unmoved) | `2cbad5612e546d3bf915074a8ad3fc4cae444122c997e2ddb3fe067d3cd022dc` |
| host-effect v25 (D-126; unmoved) | `b91b9f739b10b1bd30eb56b9d68feac81c483ad86f50e11ed33b95e98ae2d9b9` |
| COORDINATOR-DECISIONS.md | `643bd738fb9fc98953fd50289accd2abbf90208fadc1c4ecbb36b662087c4423` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves in a way that is not append-only COORD growth
with file 08, the v6 subject, both v6 verdicts, recorded doctor v4,
recorded v8, recorded v25, and this draft unmoved, re-measure
before adoption. Append-only COORD after this remasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a
MUST-FIX. The apply writer re-measures COORD at adoption.

Both verdict files are mode 0444 at the measured digests. HEAD is
`5827371` (D-126 ADOPTED).
Ignore stale C1 / D-100 / D-103 / D-104-era HEAD values
(`499c057`, `2327cf8`, `5bb125d`).
D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records
corpus v6 without SATISFYING DR-103.

## Decision

1. Record `doctor-actor-join-integration-contract.v6.json` as
   DR-114's leftover-integration T2-02 **candidate**. Both
   independent reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-114 stays `OPEN`. leftover-design/OPEN is not a finding
   against a recording of this row. No `SATISFIED`. No
   `QUALIFIED`. G09 is not QUALIFIED. The candidate binds
   NOTHING. D-056 Class A is not opened. Recording this
   candidate is not a D-096 (A) grant.
3. Doctor-contract.v4 `df2e7175…` remains the D-035 subject.
   ID-DEP-12 remains NAMED, NOT RESOLVED in doctor v4's own
   frozen bytes. This recording names D-032 successor standing
   as environment and does not rewrite doctor v4.
4. Recorded host-effect v8 `2cbad561…` remains the D-093
   subject. Recorded host-effect v25 `b91b9f73…` remains the
   D-126 subject. This recording does not retarget D-093 or
   D-126. D-093 and D-126 leftover recordings are not FC-C1.
5. CA-1 IN_PROCESS remains UNEXERCISABLE in the architecture
   preview. This recording does not admit it and does not
   relabel it as SPAWN. The later D-000 CA-2 product/authorization
   decision is named from recorded host-effect and is not minted.
6. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
7. Does not mint a D-096 (A) grant. Does not SATISFY DR-101, DR-103,
   DR-104, DR-105, DR-106, DR-108, DR-109, DR-110, DR-111, DR-112,
   DR-113, DR-114, DR-115, DR-116, DR-117, DR-118, DR-120, DR-121,
   DR-122, DR-124, DR-125, DR-126, or DR-127. Does not overturn
   D-032, D-035, D-093, D-106 (corpus recording), D-107, D-108,
   D-109, D-110, D-111, D-112, D-113, D-114, D-115, D-116, D-117,
   D-118, D-119, D-120, D-121, D-122, D-123, D-124, D-125, or
   D-126.

## Alternatives

- Wait for another generation. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: leftover remains fixture-execution
  and FC-C1 joint-owner recording; D-096 (A) is unsatisfied;
  doctor v4 ID-DEP-12 remains NAMED, NOT RESOLVED.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.
- Relabel the file 08 token leftover-design/OPEN. Rejected:
  the row is OPEN; leftover-design/OPEN on a non-OPEN row is
  D115-MF-1.
- Mint the later D-000 CA-2 gate or a D-096 (A) grant. Rejected:
  naming is not minting.
- Admit CA-1 IN_PROCESS. Rejected: recorded host-effect v8/v25
  classify it UNEXERCISABLE in the architecture preview.
- Retarget D-035 / doctor v4, D-093 / recorded v8, or D-126 /
  recorded v25. Rejected: those subjects remain.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D127.
