# D-110 turn 2 — Record component-sdk-contract.v4 as DR-125's accepted design-contract successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form
> as the adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 /
> D-105 / D-106 / D-107 / D-108 / D-109.
> **Subject:** `docs/coop/artifacts/component-sdk-contract.v4.json`
> only.

This is coordinator decision **D-110**. It is not register row
**DR-110**.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Turn-1 Claude 2 OBJECT
`docs/coop/artifacts/coordinator-decisions.D-110.review-adversarial.claude2.json`
`5f0e618e8562fee65fbc893de8f7721c62293e04ab49a29fbb13ece73f54eacd`
(1 SHOULD-FIX `CLAUDE-D110-S1`). Accepted into these bytes: the
measured-inputs table and Decision item 2 now record the three live
advisory observations from the frozen Claude v4 ACCEPT
(`O-1`, `O-2`, `O-3`; qualify `CLAUDE-V4-O1` / `CLAUDE-V4-O2` /
`CLAUDE-V4-O3`). They travel as honesty work. They are not blockers.
`O-4` is RESOLVED-NOTED and is not a live advisory. Turn-1 Codex
CONSENT
`630e1382615ee24e94c9a2b2eb598d8dd0e970a9b59fe762edc1c280eabb6ebd`
had 0 MUST-FIX and 0 SHOULD-FIX. The decision is otherwise
unchanged. The turn-1 draft
`coordinator-decisions.D-110.draft.md`
`dfdc7cce2e20505e4f0f13752a48fec68ede4ae9ce8b985bbe6a4ae99316e5af`
is not retargeted.

Measured inputs:

| Path | sha256 |
|---|---|
| component-sdk-contract.v4.json | `c53d541f12258eb96e86f0f5dbd3924a5f2e189d19c8f8672bae9037532461c3` |
| Claude 2 verdict | `b4a4b672174ba1893b071984f6cdb0cb56c99fefe0310b821e87ac454a599bff` ACCEPT, 0/0, observations O-1/O-2/O-3 (advisory) and O-4 (resolved) |
| Codex verdict | `c0cfad60a052abefd8ee08ea0f01a60bf9b6b3e459a619d13ddc895b6b0ed559` ACCEPT, 0/0 |
| D-110 turn-1 Claude 2 review | `5f0e618e8562fee65fbc893de8f7721c62293e04ab49a29fbb13ece73f54eacd` OBJECT, 1 SHOULD-FIX CLAUDE-D110-S1 |
| D-110 turn-1 Codex review | `630e1382615ee24e94c9a2b2eb598d8dd0e970a9b59fe762edc1c280eabb6ebd` CONSENT, 0 MUST-FIX, 0 SHOULD-FIX |
| COORDINATOR-DECISIONS.md | `72e71f2e60639d038e2c520a2335eb0554f52f5883c7e1ed9fa9de727419cf50` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files and the
subject are mode 0444 at the measured digests. HEAD is `2d5f15b`
(D-109 ADOPTED). D-106 draft `a1337c9d` is historical turn-1;
adopted D-106 records corpus v6 without SATISFYING DR-103.

## Decision

1. Record `component-sdk-contract.v4.json` as DR-125's accepted
   design-contract **successor candidate**. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. Claude observations `CLAUDE-V4-O1` (G20 death-ordering traces
   unnamed), `CLAUDE-V4-O2` (duplicated SATISFIED refusal in
   reviewGuidance), and `CLAUDE-V4-O3` (SF-3 "namespaced" sourced
   from unpinned file 03) travel as honesty work. Do not retarget
   SDK v4. `O-4` is resolved and is not carried as open residue.
3. DR-125 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. G20 remains
   NAMED-NOT-AUTHORED. Exact SDK APIs/frameworks remain reserved.
   The candidate binds NOTHING. D-056 Class A is not opened.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not dispose DR-117.
   Does not SATISFY DR-103, DR-107, DR-108, DR-111, DR-112,
   DR-120, DR-121, DR-122, DR-124, DR-126, or DR-127.
   Does not overturn D-106, D-107, D-108, or D-109.

## Alternatives

- Wait for a v5 that folds the three observations. Rejected: 0/0
  is the gate; advisories/observations travel.
- Mark SATISFIED. Rejected: leftover remains design; G20 is not
  authored; APIs remain reserved.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.
- Leave the three observations unrecorded. Rejected: CLAUDE-D110-S1.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D110.
