# D-107 draft — Record lifecycle-generation-contract.v2 as DR-107's accepted design-contract candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual ACCEPT
> (0 blockers, 0 SHOULD-FIX from both reviewers). Same form as the
> adopted set D-013 / D-015 / D-035 / D-042 / D-103 / D-104 / D-105 /
> D-106.
> **Subject:** `docs/coop/artifacts/lifecycle-generation-contract.v2.json`
> only.

This is coordinator decision **D-107**. It is not register row
**DR-107**.

"File 08" in this draft means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Measured inputs:

| Path | sha256 |
|---|---|
| lifecycle-generation-contract.v2.json | `a5f9d6a35f83d64687cdd2a00ec3106251ae407e54a5538727c086dd8f9ab77b` |
| Claude 2 verdict | `b4d47968e6f25a94907b8933887acba811165a9870640f178c35e98fdcfaa9d2` ACCEPT, 0 blockers, 0 SHOULD-FIX, 1 advisory ADV-1 |
| Codex verdict | `2643387c882d1de9508a6a413c2734ec1516ad43394a4493fba6c594b2ec69ee` ACCEPT, 0 blockers, 0 SHOULD-FIX |
| COORDINATOR-DECISIONS.md | `39f372e1e1031a67de132b311b463e18e0deca9224afdb085754e30c4540aac0` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Both verdict files are mode 0444
at the measured digests.

Finding-id collision discipline: Claude used `ADV-1`. This draft
names it `CLAUDE-V2-A1` (`/date` is not on the closed roster). Codex
recorded no advisory. They are not collapsed with any other `/date`
advisory class.

## Decision

1. Record `lifecycle-generation-contract.v2.json` as DR-107's accepted
   design-contract **candidate**, on the same terms as D-013 / D-015 /
   D-035 / D-042 / D-103 / D-104 / D-105 / D-106. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. Advisory CLAUDE-V2-A1 is not a blocker. It travels as honesty
   work. Do not retarget lifecycle v2.
3. DR-107 stays `PROPOSED-CLOSED-FOR-REVIEW` / OPEN. No `SATISFIED`.
   DR-G18 stays named-not-authored / not QUALIFIED. Concrete
   journal/lock/lease encoding remains reserved. Generation-rollback
   remains distinct from DR-110 self-update rollback. Lock
   production remains deferred to DR-111. D-056 Class A is not
   opened: leftover is still design plus condition-4 execution.
4. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not dispose DR-117. Does
   not SATISFY DR-103, DR-111, DR-112, or DR-105. Does not overturn
   D-106.

## Alternatives

- Wait for a v3 that folds `/date`. Rejected: 0/0 is the gate;
  the advisory travels.
- Mark SATISFIED. Rejected: G18 unexecuted, encoding reserved,
  DR-111 lock deferral, leftover is not measurement-only.
- Treat dual ACCEPT as application or seal. Rejected: binds NOTHING.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D107.
