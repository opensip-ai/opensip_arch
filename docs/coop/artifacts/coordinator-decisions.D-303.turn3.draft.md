# D-303 — Record compatibility leftover-join.v3 as DR-111 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-29
> **Protocol:** D-000 new cycle, turn 3 of 3. Lands CLAUDE-D303-MF1. Lands CLAUDE-D303-T2-SF1. Turn-2 Claude 2 OBJECT 0 MUST-FIX, 1 SHOULD-FIX CLAUDE-D303-T2-SF1 (`artifacts/coordinator-decisions.D-303.review-adversarial.claude2.turn2.json` `0a357ceac9aa9393f8efa56d803df8532172e6119153cd0acef25ae41cb35ab6`); turn-2 Codex CONSENT 0/0 (`artifacts/coordinator-decisions.D-303.review-adversarial.codex.turn2.json` `a1bc288962e58c41db83f5be60827a2791693a72f0b3ce2179917dbe7bfe22da`). Claude Stage B turn-2 CLAUDE-D303-T2-SF1 has members claimUnderReview, doesNotRequire, id, primaryEvidence, repair, severity, title, where, whyShouldFix; observations CLAUDE-D303-T2-O-1, CLAUDE-D303-T2-O-2, CLAUDE-D303-T2-O-3, CLAUDE-D303-T2-O-4 have members id, measurement, title; an empty advisories list; no observationsNotFindings field. Codex Stage B turn-2 returned an empty mustFix list; an empty shouldFix list; an empty advisories list; an empty observations list; no observationsNotFindings field. All identifiers are named. The turn-1 subject remains frozen at `artifacts/coordinator-decisions.D-303.draft.md` `425fc5174110a348cbcc55cc8d307267856788dd7767706dd9a680e5438769e0`. The turn-2 subject remains frozen.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `compatibility-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 through D-271 and D-273 through D-302. D-272 is CONTESTED and is not on that
> no-cell-edit adoption branch. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE. This is
> coordinator decision **D-303**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-111.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-101.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-NUMERIC-WINDOWS.
> **Does not** close leftover-design of OBL-LOCK-JOIN.
> **Does not** invent numeric windows.
> **Does not** invent a window unit, surface coupling, or window value.
> **Does not** produce a lock.
> **Does not** treat D-294 as the warrant.
> **Does not** pin QUALIFIED.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption of this entry after CONSENT.

D-302 is ADOPTED at
`83de4c66d35cd017a9d9d685b9036e125020340c`.
HEAD is `83de4c66d35cd017a9d9d685b9036e125020340c`.
Last live heading is D-302. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
successor (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/compatibility-leftover-join.v3.review-independent.claude2.json` | `86756fe56f3f5c26897865d210eaf5067b03af512e3bac483257ea2ee4eb90e6` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/compatibility-leftover-join.v3.review-independent.codex.json` | `f1a0e1d6142d589bc3aea227377b9468a769466517137915a39158c712af9245` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifiers | Standing |
|---|---|---|
| Claude | none | Claude Stage A compatibility leftover-join.v3 returned an empty advisories list; no observations field; no observationsNotFindings field |
| Codex | none | Codex Stage A compatibility leftover-join.v3 returned an empty observations list; an empty advisories list; no observationsNotFindings field |

This entry invents no identifier. It does not claim that both reviewers' identifiers are preserved. Claude Stage A compatibility leftover-join.v3 returned no observation identifiers. Codex Stage A compatibility leftover-join.v3 returned no observation identifiers.

## Subject

`docs/coop/artifacts/compatibility-leftover-join.v3.json` `3feb83673b659e810e57918ffa4b8f575976c17bcc50565fc2fac2171546d4a1` — DR-111 leftover remasurement of compatibility leftover-join.v2 (D-177) against live file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` under D-293 Decision 6 limb (i) (adoption commit `c10319d207cb90e2bf9df4c5e5997cfd35a30193`). The warrant is that owner adoption, not D-294's three successor triggers. D-236 (`fc688b15d17edbce3e4464ac8dcd4f82dc70fa7e`) is the one intervening file-08 commit; it recorded DR-104 SATISFIED and did not rewrite the DR-111 row. leftoverDesign remains `[OBL-NUMERIC-WINDOWS, OBL-LOCK-JOIN]`. Frozen compatibility leftover-join.v2 stays unmoved. Frozen compatibility leftover-join.v1 stays unmoved. Window unit, whether the four reserved surfaces share one window, and each surface's value remain named open decisions.

## Decision

Record compatibility leftover-join.v3 as DR-111 leftover remasurement after D-302. The candidate binds NOTHING. DR-111 stays `OPEN`. leftover-design of OBL-NUMERIC-WINDOWS and OBL-LOCK-JOIN remains. Does not invent numeric windows. Does not invent a window unit, surface coupling, or window value. Does not produce a lock. Does not treat D-294 as the warrant. Does not SATISFY DR-111. D-056 Eligibility gates 2 and 3 do not hold for DR-111. Gate 1 Class A is not opened. Not eligible in kind. Not SATISFIED. Required-now stays 28. Condition-4 effect is zero. Frozen compatibility leftover-join.v2 stays frozen; do not record it as current after this successor is recorded. Claude Stage B turn-1 MUST-FIX CLAUDE-D303-MF1 is landed. Claude Stage B turn-2 SHOULD-FIX CLAUDE-D303-T2-SF1 is landed. Claude Stage B turn-2 observations CLAUDE-D303-T2-O-1, CLAUDE-D303-T2-O-2, CLAUDE-D303-T2-O-3, CLAUDE-D303-T2-O-4 travel as honesty work. Codex Stage B turn-2 returned no observation identifiers. Claude Stage B turn-1 observations CLAUDE-D303-O1, CLAUDE-D303-O2, CLAUDE-D303-O3, CLAUDE-D303-O4 travel as honesty work. Codex Stage B turn-1 returned no observation identifiers. Does not invent a D9 code or a D-006 unit. Does not edit file 08. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D303. Does not unwrite D-012, D-103, D-177, D-236, D-293, D-294, D-295, D-296, D-297, D-298, D-299, D-300, D-301, or D-302.
