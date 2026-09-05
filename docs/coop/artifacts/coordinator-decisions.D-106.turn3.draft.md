# D-106 turn 3 — Record component-manifest-fixture-corpus.v6 as DR-103's accepted fixture-corpus candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 3 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> SATISFIED-GRADE ACCEPT (0 blockers, 0 SHOULD-FIX from both
> reviewers). Same form as the adopted set D-013 / D-015 / D-035 /
> D-042 / D-103 / D-104 / D-105.
> **Subject:** `docs/coop/artifacts/component-manifest-fixture-corpus.v6.json`
> only.

This is coordinator decision **D-106**. It is not register row
**DR-106**.

Turn-2 Codex OBJECT
`docs/coop/artifacts/coordinator-decisions.D-106.review-adversarial.codex.turn2.json`
(in flight at authoring if not yet frozen; the MUST-FIX
`CODEX-D106T2-M1` is accepted regardless): turn 2 pinned the
turn-1 Claude OBJECT at `06f4c343…`; after that pin the named
file's frozen bytes measure
`1e3f4a6a372dd95a889339d232395ca5ac2e2282f8ac68f775fe16529a26161c`
(12162 bytes, mode 0444, OBJECT, one MUST-FIX `CLAUDE-D106-M1`).
Those are the authoritative turn-1 Claude bytes. This draft
cites that reproducing digest only.

Turn-1 Claude OBJECT `CLAUDE-D106-M1` remains accepted as in
turn 2: the register path is
`docs/v2/architecture/08-decision-and-readiness-register.md`
`1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3`.
Do not substitute
`docs/coop/architecture/08-surfaces-and-topology.md`.

Turn-1 Codex CONSENT
`a7c671e83e5be1489136e08233fe97cfa99fdb145e66c94930c96e4d82e5e168`.

The operative recording decision is unchanged from turn 1.

Measured inputs:

| Path | sha256 |
|---|---|
| component-manifest-fixture-corpus.v6.json | `8dfa9346ada4fefce0aabca96062208e4fea7371a6aab68eaee75cdc908a21a5` |
| Claude 2 verdict | `b99dda48366dee5e0c90aae2c9475ca82d8152fcf302ad4898f52faaf51d533a` ACCEPT-WITH-ADVISORIES, 0/0, ADV-V6-01 |
| Codex verdict | `4ff72e1088169f0f11132bdc64d8e664d4add7711ffee604681af088f79c2a71` ACCEPT, 0/0, ADV-CMCV6-1 |
| D-106 turn-1 Claude 2 review | `1e3f4a6a372dd95a889339d232395ca5ac2e2282f8ac68f775fe16529a26161c` OBJECT, CLAUDE-D106-M1 |
| D-106 turn-1 Codex review | `a7c671e83e5be1489136e08233fe97cfa99fdb145e66c94930c96e4d82e5e168` CONSENT, 0/0 |
| Schema contract (D-104) | `1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005` |
| COORDINATOR-DECISIONS.md | `b9819d6ef0e71ef66ecec7916a75dfd47b3838fa7e58ebc8b688ec357ec46391` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure. Do not invent a turn-1 CONSENT.

Finding-id collision: Claude `ADV-V6-01` and Codex `ADV-CMCV6-1`
are the same `/date` roster defect (`CLAUDE-V6-A1` / `CODEX-V6-A1`).

## Decision

1. Record `component-manifest-fixture-corpus.v6.json` as DR-103's
   accepted fixture-corpus **candidate**. Both SATISFIED-GRADE
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. Advisories CLAUDE-V6-A1 / CODEX-V6-A1 travel as honesty work.
   Do not retarget corpus v6.
3. DR-103 stays `OPEN`. No `SATISFIED`. D-013 SATISFIED-refusal
   stands. D-104 schemas.v11 recording stands. Unicode-norm
   duplicate remains BLOCKED. Locks remain deferred to DR-111.
   No fixture executed. No lock producible. D-056 Class A not
   opened.
4. Does not retarget corpus v2/v3/v4/v5. Does not mutate
   `fixtures/dr-103.v2/` or `fixtures/dr-103.v4/`.
5. Does not edit
   `docs/v2/architecture/08-decision-and-readiness-register.md`
   (MF-6). Does not authorize `docs/v2/implementation/`.
6. Does not mint a D-096 (A) grant. Does not dispose DR-117.
   Does not SATISFY DR-111, DR-112, or DR-105.

## Alternatives

- Wait for a v7 that folds `/date`. Rejected: 0/0 is the gate.
- Mark SATISFIED. Rejected: blocked arm, lock deferral, no execution.
- Treat dual ACCEPT as seal. Rejected: binds NOTHING.
- Keep the 06f4c343… pin. Rejected: those bytes are not retrievable.

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 last.

## Reversibility

Total. Overturn: C-D106.
