# D-347 — Record leftover-join.v14 of sarif as DR-122 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-31
> **Protocol:** D-000 new cycle, turn 2 of 3. Lands SF-1. Turn-1 Claude 2 OBJECT 0 MUST-FIX, 1 SHOULD-FIX SF-1 (`artifacts/coordinator-decisions.D-347.review-adversarial.claude2.json` `0ff810615057f9e0863031fd73f0c5997ceeca1811261ca4e0f9eb92b6d9073a`); turn-1 Codex CONSENT 0/0 (`artifacts/coordinator-decisions.D-347.review-adversarial.codex.json` `0acd1a8be1332547bfe9a8b2677b5c57c0867758a7f65fc029c2fd7fe667d0c1`). Claude Stage B turn-1 returned 6 observations objects OBS-1, OBS-2, OBS-3, OBS-4, OBS-5, OBS-6. OBS-1, OBS-2, OBS-3, OBS-4, OBS-5 and OBS-6 members id, observation, raisedAndRefuted, whyNotAFinding; an empty mustFix list; a 1-member shouldFix list SF-1; an empty advisories list; an empty blockers list; a 1-member findings list SF-1; no observationsNotFindings field; decision is a string OBJECT; top-level verdict is OBJECT; mustFixCount is the number 0; shouldFixCount is the number 1; blockerCount is the number 0. Codex Stage B turn-1 returned an empty mustFix list; an empty shouldFix list; an empty advisories list; an empty observations list; an empty observationsNotFindings list; an empty blockers list; no findings field; no decision field; top-level verdict is CONSENT; mustFixCount is the number 0; shouldFixCount is the number 0; blockerCount is the number 0. All identifiers are named. No identifier is invented. The turn-1 subject remains frozen.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `sarif-leftover-join.v14.json` (0 blockers, 0 SHOULD-FIX). Same no-cell-edit
> branch as D-170 through D-235 and D-237 through D-346. D-272 is
> CONTESTED and is not on that no-cell-edit adoption branch. Not a
> three-limb act. Not a required-now successor. Not
> SATISFIED-GRADE. This is coordinator decision **D-347**, not a
> register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-122.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** pin QUALIFIED.
> **Does not** remasure sarif-fc-outfail-golden.v5.
> **Does not** remasure leftover-join.v11 of sarif as a golden.
> **Does not** remasure occupancy v2 of G26.
> **Does not** occupy G26.
> **Does not** remasure leftover-join.v7 of G29.
> **Does not** remasure leftover-join.v10 of G30.
> **Does not** remasure leftover-join.v20 of G21.
> **Does not** remasure leftover-join.v10 of G19.
> **Does not** remasure leftover-join.v16 of G20.
> **Does not** remasure leftover-join.v6 of anti-lockstep.
> **Does not** remasure leftover-join.v9 of platform-tcb.
> **Does not** remasure sarif-fc-nonauth-term-golden.v4.
> **Does not** author FC-OUTFAIL copies.
> **Does not** author FC-OUTFAIL.committed-run-preserved.
> **Does not** invent a D-002 platform list.
> **Does not** copy onto Windows.
> **Does not** invent a D9 code, a RunId recipe, or a section 7.1
> recipe.
> **Does not** advertise SARIF.
> **Does not** resurrect G17.
> **Does not** record leftover-join.v11 of sarif as current after this successor is
> recorded.
> **Does not** record leftover-join.v13 of sarif as current.
> **Does not** record leftover-join.v12 of sarif as current.
> **Does not** record leftover-join.v10 of sarif as current.
> **Does not** record leftover-join.v9 of sarif as current.
> **Does not** record leftover-join.v8 of sarif as current.
> **Does not** record leftover-join.v7 of sarif as current.
> **Does not** record leftover-join.v6 of sarif as current.
> **Does not** record leftover-join.v5 of sarif as current.
> **Does not** record leftover-join.v4 of sarif as current.
> **Does not** rewrite Frozen leftover-join.v12 of sarif Findings land off leftover-join.v13 of sarif.
> **Does not** rewrite Frozen leftover-join.v8 of sarif Findings land off leftover-join.v11 of sarif.
> **Does not** rewrite Frozen leftover-join.v9 of sarif Findings land off leftover-join.v11 of sarif.
> **Does not** rewrite Frozen leftover-join.v10 of sarif Findings land off leftover-join.v11 of sarif.
> **Does not** rewrite Frozen leftover-join.v5 of sarif Findings land off leftover-join.v7 of sarif.
> **Does not** rewrite Frozen leftover-join.v6 of sarif Findings land off leftover-join.v7 of sarif.
> **Does not** flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`.
> **Does not** flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption of this
> entry after CONSENT.

D-346 is ADOPTED at `7dd4cc37239109c51a62b8c2dbd59a8c13d08537`.
HEAD is `7dd4cc37239109c51a62b8c2dbd59a8c13d08537`.
Last live heading is D-346. Required-now is 28. Last-heading
custody only. D-347 does not unwrite D-346.

Stage A dual independent ACCEPT 0/0 of the frozen successor (not
this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/sarif-leftover-join.v14.review-independent.claude2.json` | `f87dca8bf26a1e8ae1e297e491cbdda6e3114a2239c4ba61b5abeb82363e5a58` | ACCEPT 0/0 (top-level verdict; no decision field) |
| Codex | `docs/coop/artifacts/sarif-leftover-join.v14.review-independent.codex.json` | `63027af4da07d8134dc787a85bdab3c9ed00ae1557134275f860ac777dc7f130` | ACCEPT 0/0 (top-level verdict; decision is an object with members verdict, mustFixCount, shouldFixCount, blockerCount, reason) |

Frozen predecessor `sarif-leftover-join.v13.json`
`6c1f5c5abfe37dde6f4f1731df54fe6955c56caf31df963611ee8fb0f46484a4`
Stage A Claude REJECT 0 MUST-FIX, 2 SHOULD-FIX SF-1 SF-2
(`1228401df962fcf6ad64076abd80b1973e6f9e4a0f79ccaecd4c384a813b2c02`);
Codex ACCEPT 0/0
(`2e520a259527f6b41bd214bef61a58e7fbd6410980080149969f811af96e0124`).
Findings land at leftover-join.v14 of sarif. Frozen
leftover-join.v13 of sarif stays frozen; do not record it as
current.

Frozen predecessor `sarif-leftover-join.v12.json`
`8390764ce33f23c58df6b74869443bc508a270be06a483e22ebfe9707e119342`
Stage A Claude REJECT 3 MUST-FIX MF-1 MF-2 MF-3, 2 SHOULD-FIX SF-1
SF-2
(`fdb2142f4433f74dbf84a1fe40c8ba3d38df2be881856b6a978efe81a56ca3e2`);
Codex REJECT 4 unlabeled MUST-FIX
(`a5ec12d39b544e64595d3448e25d713586c183ed1b9120503a8f3affb7c0b992`).
Findings land at leftover-join.v13 of sarif. Frozen
leftover-join.v12 of sarif stays frozen; do not record it as
current.

Frozen leftover-join.v11 of sarif
`c204456451df988d24526a6d0851fe1874fa3492030773ac32456508fb86b7e0`
remains the D-345 current recorded remasurement until this
successor is recorded. Frozen leftover-join.v8 of sarif Findings
land at leftover-join.v11 of sarif. Frozen leftover-join.v9 of
sarif Findings land at leftover-join.v11 of sarif. Frozen
leftover-join.v10 of sarif Findings land at leftover-join.v11 of
sarif. Frozen leftover-join.v7 of sarif is historical after D-345.
Frozen leftover-join.v5 of sarif Findings land at leftover-join.v7
of sarif. Frozen leftover-join.v6 of sarif Findings land at
leftover-join.v7 of sarif. Do not rewrite those landings. Frozen
leftover-join.v4 of sarif is historical after D-325.

Stage A observation disposition (no change requested; no
identifiers invented):


| Source | Identifiers | Standing |
|---|---|---|
| Claude | OBS-1, OBS-2, OBS-3, OBS-4, OBS-5, OBS-6 | Claude Stage A leftover-join.v14 of sarif returned top-level verdict ACCEPT; no decision field; an empty mustFix list; an empty shouldFix list; an empty blockers list; an empty findings list; mustFixCount is the number 0; shouldFixCount is the number 0; blockerCount is the number 0; no advisories field; no observations field; 6 observationsNotFindings objects OBS-1, OBS-2, OBS-3, OBS-4, OBS-5, OBS-6. OBS-1, OBS-2, OBS-3, OBS-4, OBS-5 and OBS-6 members id, observation, raisedAndRefuted, whyNotAFinding. They travel as honesty work. |
| Codex | none | Codex Stage A leftover-join.v14 of sarif returned top-level verdict ACCEPT; decision is an object with members verdict, mustFixCount, shouldFixCount, blockerCount, reason; an empty mustFix list; an empty shouldFix list; an empty blockers list; an empty observationsNotFindings list; no observations field; no findings field; no advisories field; mustFixCount is the number 0; shouldFixCount is the number 0; blockerCount is the number 0 |

This entry names Claude Stage A leftover-join.v14 of sarif
identifiers OBS-1, OBS-2, OBS-3, OBS-4, OBS-5, OBS-6; they travel
as honesty work. It recites no Codex observations as named
identifiers. Codex Stage A leftover-join.v14 of sarif returned no
observation identifiers. This entry names leftover-join.v13 of
sarif Stage A Claude identifiers SF-1 and SF-2 as landed at
leftover-join.v14 of sarif. This entry names leftover-join.v12 of
sarif Stage A Claude identifiers MF-1, MF-2, MF-3, SF-1, SF-2 and
Codex unlabeled MUST-FIX as landed at leftover-join.v13 of sarif.
This entry names leftover-join.v10 of sarif Stage A Claude
identifier SF-1 as landed at leftover-join.v11 of sarif. This
entry names leftover-join.v9 of sarif Stage A Claude identifier
SF-1 and Codex unlabeled SHOULD-FIX as landed at leftover-join.v11
of sarif. This entry names leftover-join.v8 of sarif Stage A
Claude identifiers MF-1, MF-2, MF-3 and Codex unlabeled MUST-FIX
and unlabeled SHOULD-FIX as landed at leftover-join.v11 of sarif.
Frozen leftover-join.v5 of sarif Findings land at leftover-join.v7
of sarif. Frozen leftover-join.v6 of sarif Findings land at
leftover-join.v7 of sarif. No identifier is invented.

## Subject

Frozen `docs/coop/artifacts/sarif-leftover-join.v14.json`
`8ecea58e0b6823968ebffbbe75640ba3473446985047fd709e308a4a7e40bf97`.
Status CANDIDATE-NOT-APPLIED. binds NOTHING. leftoverDesign is
[OBL-FC-OUTFAIL-FX]. leftover-design of the four D-346 copies is
stale as an authoring claim. leftover-design of
OBL-FC-NONAUTH-TERM-FX is stale as an authoring claim.
leftover-design of the eight D-344 copies is stale as an authoring
claim. leftover-design of the two D-296 implementations is stale
as an authoring claim. leftover-design of the D-297
FC-OUTFAIL.no-committed-run implementation is stale as an
authoring claim. leftover-design of
FC-OUTFAIL.committed-run-preserved remains. leftover-design of
OBL-FC-OUTFAIL-FX remains. Frozen leftover-join.v11 of sarif
remains the D-345 current recorded remasurement until this
successor is recorded. Frozen leftover-join.v13 of sarif stays
unrecorded. Frozen leftover-join.v12 of sarif stays unrecorded.
Frozen leftover-join.v10 of sarif stays unrecorded. Frozen
leftover-join.v9 of sarif stays unrecorded. Frozen
leftover-join.v8 of sarif stays unrecorded. Frozen
leftover-join.v12 of sarif Findings land at leftover-join.v13 of
sarif. Frozen leftover-join.v8 of sarif Findings land at
leftover-join.v11 of sarif. Frozen leftover-join.v9 of sarif
Findings land at leftover-join.v11 of sarif. Frozen
leftover-join.v10 of sarif Findings land at leftover-join.v11 of
sarif. Frozen leftover-join.v5 of sarif Findings land at
leftover-join.v7 of sarif. Frozen leftover-join.v6 of sarif
Findings land at leftover-join.v7 of sarif. Frozen
leftover-join.v4 of sarif is historical after D-325. Frozen
leftover-join.v7 of sarif is historical after D-345.

## Decision

Record leftover-join.v14 of sarif as DR-122 leftover remasurement
after D-346. The candidate binds NOTHING. DR-122 stays
`PROPOSED-CLOSED-FOR-REVIEW`. leftover-design of the four D-346
copies is stale as an authoring claim. leftover-design of
OBL-FC-OUTFAIL-FX remains. Does not remasure
sarif-fc-outfail-golden.v5. Does not remasure leftover-join.v11 of
sarif as a golden. Does not remasure occupancy v2 of G26. Does not
occupy G26. Does not SATISFY DR-117. Does not SATISFY DR-122. Does
not SATISFY DR-131. Does not SATISFY DR-133. D-316 already opened
D-056 Gate 1 Class A for DR-117; this entry does not open Class A
for DR-117 or DR-122 and does not perform gates 4 or 5. Not
SATISFIED. Not QUALIFIED. Required-now stays 28. Condition-4
effect is zero. Frozen leftover-join.v13 of sarif stays frozen; do
not record it as current. Frozen leftover-join.v12 of sarif stays
frozen; do not record it as current. Frozen leftover-join.v10 of
sarif stays frozen; do not record it as current. Frozen
leftover-join.v9 of sarif stays frozen; do not record it as
current. Frozen leftover-join.v8 of sarif stays frozen; do not
record it as current. Frozen leftover-join.v11 of sarif stays
frozen; do not record it as current after this successor is
recorded. Frozen leftover-join.v7 of sarif stays frozen; do not
record it as current. Frozen leftover-join.v5 of sarif stays
frozen; do not record it as current. Frozen leftover-join.v6 of
sarif stays frozen; do not record it as current. Frozen
leftover-join.v4 of sarif stays frozen; do not record it as
current. Claude Stage A leftover-join.v14 of sarif returned 6
observationsNotFindings objects OBS-1, OBS-2, OBS-3, OBS-4, OBS-5,
OBS-6; they travel as honesty work and this entry invents no
identifier. Does not invent a D-002 platform list, a PlanIntent
schema, a D9 code, a RunId recipe, or a section 7.1 recipe. Does
not remasure leftover-join.v7 of G29. Does not remasure
leftover-join.v10 of G30. Does not remasure leftover-join.v20 of
G21. Does not remasure leftover-join.v10 of G19. Does not remasure
leftover-join.v16 of G20. Does not remasure leftover-join.v6 of
anti-lockstep. Does not remasure leftover-join.v9 of platform-tcb.
Does not remasure sarif-fc-nonauth-term-golden.v4. Does not author
FC-OUTFAIL copies. Does not author
FC-OUTFAIL.committed-run-preserved. Does not copy onto Windows.
Does not advertise SARIF. Does not resurrect G17. Does not flatten
DR-107. Does not edit file 08. Does not authorize
`docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET
on the naming half (28 of 28). Condition 5 last. This entry does
not edit file 08.

## Reversibility

Total only before a later dependent leftover rewrite, SATISFIED
cycle, or file-08 cell rewrite. Overturn: C-D347. Does not unwrite
D-115, D-182, D-293, D-296, D-297, D-325, D-344, D-345, or D-346.

