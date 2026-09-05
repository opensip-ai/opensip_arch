# D-164 — Record doctor-actor-leftover-join.v2 as DR-114 leftover-design measurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-16
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `doctor-actor-leftover-join.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-163 / D-162. This is coordinator decision **D-164**,
> not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold for DR-114.
> **Does not** add a DR-G* row or change requiredNow (26).
> **Does not** execute fixtures.
> **Does not** record FC-C1.
> **Does not** apply D-035, D-126, D-127, or D-129.
> **Does not** admit CA-1 IN_PROCESS or mint the later CA-2 gate.
> **Does not** invent a D9 code.
> **Does not** mint a D-096 (A) grant.
> **Does not** force a ride onto G09.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-163 is ADOPTED at `665415a8cf4831b979ab0b35540ec739f97ca355`.
HEAD is `665415a8cf4831b979ab0b35540ec739f97ca355`.

Join-verdict custody (recital before review):

| Path | sha256 | mode |
|---|---|---|
| doctor-actor-leftover-join.v2.review-independent.claude2.json | `f1e43240e675f27bd0c91a24d65f57f75f90f565a8f5325a66338187f9cd12a8` | 0444 |
| doctor-actor-leftover-join.v2.review-independent.codex.json | `0cfe8bb3045e0d88d5e11e6f877d3ec73a487d6c9a03be48f7692bb6b0c97e9f` | 0444 |

Measured inputs:

| Path | sha256 |
|---|---|
| doctor-actor-leftover-join.v2.json | `874af09ad24d21179fb6abb9f4f94332e56eb956b7991295e5c31631e84f80c6` |
| Claude 2 join verdict | `f1e43240e675f27bd0c91a24d65f57f75f90f565a8f5325a66338187f9cd12a8` ACCEPT, 0/0; mode 0444 |
| Codex join verdict | `0cfe8bb3045e0d88d5e11e6f877d3ec73a487d6c9a03be48f7692bb6b0c97e9f` ACCEPT, 0/0; mode 0444 |
| doctor-contract.v4.json | `df2e717555616db096e61548458f23b442f7f0e37b2d2461eabc2c33201e94b3` |
| doctor-actor-join-integration-contract.v8.json | `c830f954605a4a1d47c5643230439340994a0c42c4a487359541c578d00bc662` |
| COORDINATOR-DECISIONS.md | `9d8be34be203a95ee1f9536b804c3cb712e0d1a6398f62a85aaae5828f655f76` |
| file 08 | `3a9442d1761864de59f103374489a9fbffdd12cc4ba39ddd7c7f491f64357e44` |
| D-163 commit | `665415a8cf4831b979ab0b35540ec739f97ca355` |
| HEAD | `665415a8cf4831b979ab0b35540ec739f97ca355` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v2, both
join verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-139 L names DR-114 leftover: leftover-design / actor-join
(D-056 ineligible table; D-129). Join v2 received
independent dual ACCEPT at 0 blockers and 0 SHOULD-FIX
after Codex REJECT of v1 (DALJ-V1-SF1). This entry records
that measurement. It does not add a row and does not
SATISFY DR-114. The competing filename
`doctor-leftover-join.v1.json` is not this subject and is
not recorded.

## Decision

1. Record `doctor-actor-leftover-join.v2.json` as DR-114
   leftover-design measurement. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX.
2. DR-114 stays `OPEN`. leftover-design/OPEN is the token,
   not a finding. Leftover-design is not closed. Remaining
   leftover-design: OBL-G12-HARNESS-SPEC,
   OBL-G21-HARNESS-SPEC, OBL-DOCTOR-FX-AUTHORING,
   OBL-JOIN-FX-AUTHORING, OBL-JOIN-FX-EXECUTION, OBL-FC-C1,
   and OBL-BLK-1..4. D-032 actor scope, D-035 doctor v4,
   and the recorded actor-join / host-effect candidates
   are not leftover-authoring. Actor-join fixture execution
   is not forced onto G09.
3. D-056 Class A is not opened. Gates 2 and 3 do not hold
   for DR-114. No SATISFIED. Required-now stays 26. This
   entry does not execute fixtures, does not record FC-C1,
   does not apply D-035, D-126, D-127, or D-129, does not
   admit CA-1 IN_PROCESS, does not mint the later CA-2
   gate, does not invent a D9 code, and does not mint a
   D-096 (A) grant.
4. **Proposed later work, not performed here:** a later
   D-000 cycle may author the G12 and G21 harness
   specifications and independently pin the twelve doctor
   FC implementations and thirteen join-fixture
   implementations; a later joint-owner act may record
   FC-C1; a later cycle may name actor-join fixture
   execution at a gate whose live claim owns that
   property. Each later act that adds a required-now row
   is a scoped D-002 successor and a D-086 successor in
   the same act.
5. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (26 of 26). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
naming successor, FC-C1 recording, or SATISFIED cycle.
Overturn: C-D164. Does not unwrite D-032, D-035, D-126,
D-127, D-129, or D-163.
