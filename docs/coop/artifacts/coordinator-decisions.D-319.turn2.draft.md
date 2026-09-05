# D-319 — Record g30 leftover-join.v7 as G30 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-30
> **Protocol:** D-000 new cycle, turn 2 of 3. Lands CLAUDE-D319-S1 and CLAUDE-D319-S2. Turn-1 Claude 2 OBJECT 0 MUST-FIX, 2 SHOULD-FIX CLAUDE-D319-S1 CLAUDE-D319-S2 (`artifacts/coordinator-decisions.D-319.review-adversarial.claude2.json` `5a61d060ce42ffaf148f876e9f4d30e1ca004467fe6d3ffa7b8d5d84d8a9624f`); turn-1 Codex CONSENT 0/0 (`artifacts/coordinator-decisions.D-319.review-adversarial.codex.json` `a20da120f3c723064e190c7f08a444ded38bb375ec6c179afed3b36fa5ca28c0`). Claude Stage B turn-1 observations CLAUDE-D319-O1, CLAUDE-D319-O2, CLAUDE-D319-O3 have members id, severity, where, observation, whyItDoesNotStand; an empty mustFix list; a 2-member shouldFix list CLAUDE-D319-S1 CLAUDE-D319-S2; an empty advisories list; an empty blockers list; no observationsNotFindings field. Codex Stage B turn-1 returned an empty mustFix list; an empty shouldFix list; an empty advisories list; an empty blockers list; an empty observationsNotFindings list; no observations field. All identifiers are named. No identifier is invented. The turn-1 subject remains frozen.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g30-leftover-join.v7.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 through D-318. D-272 is CONTESTED and is not on that
> no-cell-edit adoption branch. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE. This is
> coordinator decision **D-319**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-101.
> **Does not** SATISFY DR-G30.
> **Does not** pin QUALIFIED.
> **Does not** close leftover-design of OBL-G30-FX-AUTHORING.
> **Does not** remasure occupancy v2.
> **Does not** remasure g30-fixture-corpus.v2.
> **Does not** invent per-D-002-platform copies.
> **Does not** invent a D-002 platform list.
> **Does not** invent a PlanIntent schema.
> **Does not** invent the DR-131 pack.
> **Does not** mint Rust-as-core.
> **Does not** name G13 into required-now.
> **Does not** invent a D9 code, exit number, or HostTermination.
> **Does not** invent a section 7.1 recipe.
> **Does not** record g30 leftover-join.v5 as current.
> **Does not** record g30 leftover-join.v6 as current.
> **Does not** flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`.
> **Does not** flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption of this entry after CONSENT.

D-318 is ADOPTED at
`3f1f11d6156d4f4f37a4b8c6114d80878c53af15`.
HEAD is `3f1f11d6156d4f4f37a4b8c6114d80878c53af15`.
Last live heading is D-318. Required-now is 28. Last-heading custody only. D-319 does not unwrite D-318.

Stage A dual independent ACCEPT 0/0 of the frozen
successor (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g30-leftover-join.v7.review-independent.claude2.json` | `4da23e7cf34ff95fa03210d4156a7e84d67bfa26fa1fae36428776b9840b08d5` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g30-leftover-join.v7.review-independent.codex.json` | `ea8df3f1df7e8e725b4e6745e08624934ecd7b7adfbad091845a4d6783fbb90a` | ACCEPT 0/0 |

Frozen predecessor `g30-leftover-join.v6.json` `174cd906d850218fe95aec56b6428d5c8843d9b163b046dc7e30ee3987a9433a` Stage A Claude REJECT SF-1 SF-2 (`1228028f0172daf00e8b503b91c82ee7088d3e3483bceb475396c57e0769c6fa`); Codex REJECT 1 unlabeled MUST-FIX, 1 unlabeled SHOULD-FIX (`9d3598cbbd37bf32ccfac6da4db80ece2384d1ad379a516495ee6992a8553b6f`). Findings land at g30 leftover-join.v7. Frozen `g30-leftover-join.v5.json` `f5ca1291645b9d5bf83a0161b6fe79c70440cbfd5aa93f667f2d8fdc2dbe89da` Stage A Claude ACCEPT 0/0 (`f9df86c1f66c2ba31105990adc2c15f2b87cd53e03c643dfaf394536fa876f8a`); Codex REJECT 0 MUST-FIX, 1 unlabeled SHOULD-FIX (`033e78d67fcaec1973197b1f0fba252a0c72e5e95ea012e3a4c75f40f4b2fd71`). That SHOULD-FIX landed at g30 leftover-join.v6 and is retained at g30 leftover-join.v7. Frozen g30 leftover-join.v5 and g30 leftover-join.v6 stay frozen; do not record them as current. Frozen `g30-leftover-join.v4.json` `3f3d84e0e24a2aea0ba95c282f809c8343d1827d0577ca8396d4560c5e012c75` remains the D-255 historical recording until this successor is recorded.

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifiers | Standing |
|---|---|---|
| Claude | OB-1, OB-2, OB-3 | Claude Stage A g30 leftover-join.v7 returned 3 named observations objects OB-1, OB-2, OB-3 (members id, note); an empty mustFix list; an empty shouldFix list; an empty advisories list; an empty blockers list; no observationsNotFindings field |
| Codex | none | Codex Stage A g30 leftover-join.v7 returned an empty observations list; an empty observationsNotFindings list; an empty mustFix list; an empty shouldFix list; an empty advisories list; an empty blockers list |

This entry names the Claude identifiers OB-1, OB-2, OB-3; no identifier is invented. It recites no Codex observations. Codex Stage A g30 leftover-join.v7 returned no observation identifiers. Claude g30 leftover-join.v6 SHOULD-FIX identifiers SF-1 and SF-2 landed at g30 leftover-join.v7. Claude g30 leftover-join.v6 observations OB-1 and OB-2 travel as honesty work of the frozen predecessor. g30 leftover-join.v6 Codex returned no observation identifier.

## Subject

Frozen `docs/coop/artifacts/g30-leftover-join.v7.json` `806c4dc88ef931a4130c403f59e619acc935d8521ef1c1e1edc5f5362990c67a`. Status CANDIDATE-NOT-APPLIED. binds NOTHING. leftoverDesign remains `[OBL-G30-FX-AUTHORING]`, scoped to per-D-002-platform copies. leftover-design of the seven D-317 implementations is stale as an authoring claim. Frozen occupancy v2 remains unmoved. Frozen g30-fixture-corpus.v2 remains unmoved. Frozen `g30-leftover-join.v4.json` `3f3d84e0e24a2aea0ba95c282f809c8343d1827d0577ca8396d4560c5e012c75` is the D-255 historical recording and is not current after this successor is recorded.

## Decision

Record g30 leftover-join.v7 as G30 leftover remasurement after D-318. The candidate binds NOTHING. DR-G30 stays `OPEN`. leftover-design of OBL-G30-FX-AUTHORING remains true, scoped to per-D-002-platform copies of the seven D-317 implementations. leftover-design of those seven implementations is stale as an authoring claim. Does not remasure occupancy v2. Does not remasure g30-fixture-corpus.v2. Does not SATISFY DR-117. Does not SATISFY DR-G30. D-316 already opened D-056 Gate 1 Class A for DR-117; this entry does not open Class A and does not perform gates 4 or 5. Not SATISFIED. Not QUALIFIED. Required-now stays 28. Condition-4 effect is zero. Frozen g30 leftover-join.v5 and g30 leftover-join.v6 stay frozen; do not record them as current. Claude Stage A observations OB-1, OB-2, OB-3 travel as honesty work. Does not invent a PlanIntent schema, the DR-131 pack, Rust-as-core, a D9 code, a section 7.1 recipe, or a D-002 platform list. Does not author per-D-002-platform copies. Does not remasure G29. Does not edit file 08. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last. This entry does not edit file 08.

## Reversibility

Total only before a later dependent leftover rewrite, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D319. Does not unwrite D-158, D-230, D-255, D-293, D-316, D-317, or D-318.
