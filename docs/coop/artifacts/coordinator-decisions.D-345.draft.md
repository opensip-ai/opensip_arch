# D-345 — Record sarif leftover-join.v11 as DR-122 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-31
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `sarif-leftover-join.v11.json` (0 blockers, 0 SHOULD-FIX). Same no-cell-edit
> branch as D-170 through D-235 and D-237 through D-344. D-272 is
> CONTESTED and is not on that no-cell-edit adoption branch. Not a
> three-limb act. Not a required-now successor. Not
> SATISFIED-GRADE. This is coordinator decision **D-345**, not a
> register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-122.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** pin QUALIFIED.
> **Does not** remasure sarif-fc-nonauth-term-golden.v4.
> **Does not** remasure sarif-fc-outfail-golden.v3.
> **Does not** remasure occupancy v2 of G26.
> **Does not** occupy G26.
> **Does not** remasure leftover-join.v7 of G29.
> **Does not** remasure leftover-join.v10 of G30.
> **Does not** remasure leftover-join.v20 of G21.
> **Does not** remasure leftover-join.v10 of G19.
> **Does not** remasure leftover-join.v16 of G20.
> **Does not** remasure leftover-join.v6 of anti-lockstep.
> **Does not** remasure leftover-join.v9 of platform-tcb.
> **Does not** author FC-OUTFAIL copies.
> **Does not** author FC-OUTFAIL.committed-run-preserved.
> **Does not** invent a D-002 platform list.
> **Does not** copy onto Windows.
> **Does not** invent a D9 code, a RunId recipe, or a section 7.1
> recipe.
> **Does not** advertise SARIF.
> **Does not** resurrect G17.
> **Does not** record leftover-join.v7 of sarif as current after this successor is
> recorded.
> **Does not** record leftover-join.v10 of sarif as current.
> **Does not** record leftover-join.v9 of sarif as current.
> **Does not** record leftover-join.v8 of sarif as current.
> **Does not** record leftover-join.v6 of sarif as current.
> **Does not** record leftover-join.v5 of sarif as current.
> **Does not** record leftover-join.v4 of sarif as current.
> **Does not** rewrite Frozen leftover-join.v5 of sarif Findings land off leftover-join.v7 of sarif.
> **Does not** rewrite Frozen leftover-join.v6 of sarif Findings land off leftover-join.v7 of sarif.
> **Does not** flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`.
> **Does not** flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption of this
> entry after CONSENT.

D-344 is ADOPTED at `d6098a82e80fa237fe0626d025dc263b86c19363`.
HEAD is `d6098a82e80fa237fe0626d025dc263b86c19363`.
Last live heading is D-344. Required-now is 28. Last-heading
custody only. D-345 does not unwrite D-344.

Stage A dual independent ACCEPT 0/0 of the frozen successor (not
this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/sarif-leftover-join.v11.review-independent.claude2.json` | `cf60eb23d45391f056a448010f9de638b9ee8bca965bd0d408b3a859e39da47a` | ACCEPT 0/0 (top-level verdict; no decision field) |
| Codex | `docs/coop/artifacts/sarif-leftover-join.v11.review-independent.codex.json` | `61fba60e5a5261d6bf72600f0562bf35d862e2370fa9ee4877d3f64e34ad315c` | ACCEPT 0/0 (top-level verdict; decision is an object with members verdict, mustFixCount, shouldFixCount, blockerCount, reason) |

Frozen predecessor `sarif-leftover-join.v10.json` `f2abd67833dc396ce68f4627adf2862ca8f5486c058c566a240ad516eb8600b3` Stage A Claude REJECT 0 MUST-FIX, 1
SHOULD-FIX SF-1 (`0a9d484fedee14ae3c285d75f04bae2749d0f749bd668ea57ca67b6f1b6ea30a`); Codex ACCEPT 0/0 (`33cf4d82a8ed3a37cd89077d9213f29e3063241c060ca1c0829e17224bcfb0af`). Findings land at
sarif leftover-join.v11. Frozen sarif leftover-join.v10 stays frozen; do not record it as current.

Frozen predecessor `sarif-leftover-join.v9.json` `f025b62d4490b43088d01d9287bb866b3b4328679cd7c515d4d8892fb7718103` Stage A Claude REJECT 0 MUST-FIX, 1
SHOULD-FIX SF-1 (`292372791703e782267bb0a83f0e6e882737682d114ddda0ad56579a703e71bf`); Codex REJECT 0 MUST-FIX, 1 unlabeled
SHOULD-FIX (`e624e4513067c8cdb3388733e2d64b6577f6842c5fdcafb79ea642257a71cf48`). Findings land at sarif leftover-join.v11. Frozen sarif leftover-join.v9 stays frozen; do
not record it as current.

Frozen predecessor `sarif-leftover-join.v8.json` `b11b2ba0fc967446f9bdfc52dac40ab6cd137b7761b60859d455b82ea7a34aeb` Stage A Claude REJECT MF-1 MF-2 MF-3
(`3fb6af516d0ada1c924c04c94c7bd7bd5e784c793c96775a8f2203a2f0d13d14`); Codex REJECT 3 unlabeled MUST-FIX, 1 unlabeled SHOULD-FIX
(`67d54154a946e398d7c7b83ce569a76862d6048f66a79d6de734bba282f9e997`). Findings land at sarif leftover-join.v11. Frozen sarif leftover-join.v8 stays frozen; do not record
it as current.

Frozen `sarif-leftover-join.v7.json` `2df7dedf150dff97319e18de78b0c2d8267aa3a77eedeadd8b966e92c194c31b` Stage A Claude ACCEPT 0/0 (`e3333252466220ffa0c2b90ddef209d483ab1374fe3968e8e33e26b0b809b219`); Codex ACCEPT 0/0
(`ad4ea6068a589d2c86b9300e812fa061a320dc03d57cfbe9b515019183bb81b4`). Frozen sarif leftover-join.v7 remains the D-325 current recorded remasurement
until this successor is recorded.

Frozen leftover-join.v5 of sarif Findings land at leftover-join.v7 of sarif. Frozen leftover-join.v6 of sarif Findings land at leftover-join.v7 of sarif. Do
not rewrite those landings. Frozen leftover-join.v4 of sarif is historical after D-325.

Stage A observation disposition (no change requested; no
identifiers invented):

| Source | Identifiers | Standing |
|---|---|---|
| Claude | OBS-1, OBS-2, OBS-3 | Claude Stage A sarif leftover-join.v11 returned top-level verdict ACCEPT; no decision field; an empty mustFix list; an empty shouldFix list; an empty blockers list; mustFixCount is the number 0; shouldFixCount is the number 0; blockerCount is the number 0; no advisories field; no findings field; no observations field; 3 observationsNotFindings objects OBS-1, OBS-2, OBS-3. OBS-1 and OBS-2 members id, observation, whyNotAFinding, raisedAndRefuted. OBS-3 members id, observation, whyNotAFinding. They travel as honesty work. |
| Codex | none | Codex Stage A sarif leftover-join.v11 returned top-level verdict ACCEPT; decision is an object with members verdict, mustFixCount, shouldFixCount, blockerCount, reason; an empty mustFix list; an empty shouldFix list; an empty blockers list; an empty observationsNotFindings list; no observations field; no findings field; no advisories field; mustFixCount is the number 0; shouldFixCount is the number 0; blockerCount is the number 0 |

This entry names Claude Stage A sarif leftover-join.v11 identifiers OBS-1, OBS-2,
OBS-3; they travel as honesty work. It recites no Codex
observations as named identifiers. Codex Stage A sarif leftover-join.v11 returned no
observation identifiers. This entry names leftover-join.v10 of sarif Stage A Claude
identifier SF-1 as landed at leftover-join.v11 of sarif. This entry names leftover-join.v9 of sarif Stage A
Claude identifier SF-1 and Codex unlabeled SHOULD-FIX as landed at
leftover-join.v11 of sarif. This entry names leftover-join.v8 of sarif Stage A Claude identifiers MF-1, MF-2,
MF-3 and Codex unlabeled MUST-FIX and unlabeled SHOULD-FIX as
landed at leftover-join.v11 of sarif. No identifier is invented.

## Subject

Frozen `docs/coop/artifacts/sarif-leftover-join.v11.json` `c204456451df988d24526a6d0851fe1874fa3492030773ac32456508fb86b7e0`. Status CANDIDATE-NOT-APPLIED. binds NOTHING.
leftoverDesign is [OBL-FC-OUTFAIL-FX]. leftover-design of
OBL-FC-NONAUTH-TERM-FX is stale as an authoring claim.
leftover-design of the eight D-344 copies is stale as an authoring
claim. leftover-design of the two D-296 implementations is stale
as an authoring claim. leftover-design of the D-297
FC-OUTFAIL.no-committed-run implementation is stale as an
authoring claim. leftover-design of
FC-OUTFAIL.committed-run-preserved remains. leftover-design of
per-D-002-platform copies of the D-297 implementation remains.
obligations[5].rideStanding is specified-not-leftover. Frozen leftover-join.v7 of sarif
remains the D-325 current recorded remasurement until this
successor is recorded. Frozen leftover-join.v10 of sarif stays unrecorded. Frozen leftover-join.v9 of sarif
stays unrecorded. Frozen leftover-join.v8 of sarif stays unrecorded. Frozen leftover-join.v5 of sarif Findings
land at leftover-join.v7 of sarif. Frozen leftover-join.v6 of sarif Findings land at leftover-join.v7 of sarif. Frozen leftover-join.v4 of sarif is
historical after D-325.

## Decision

Record sarif leftover-join.v11 as DR-122 leftover remasurement after D-344. The
candidate binds NOTHING. DR-122 stays `PROPOSED-CLOSED-FOR-REVIEW`. leftover-design of
OBL-FC-NONAUTH-TERM-FX is stale as an authoring claim.
leftover-design of the eight D-344 copies is stale as an authoring
claim. leftover-design of OBL-FC-OUTFAIL-FX remains. Does not
remasure sarif-fc-nonauth-term-golden.v4. Does not remasure
sarif-fc-outfail-golden.v3. Does not remasure occupancy v2 of G26.
Does not occupy G26. Does not SATISFY DR-117. Does not SATISFY
DR-122. Does not SATISFY DR-131. Does not SATISFY DR-133. D-316
already opened D-056 Gate 1 Class A for DR-117; this entry does
not open Class A for DR-117 or DR-122 and does not perform gates 4
or 5. Not SATISFIED. Not QUALIFIED. Required-now stays 28.
Condition-4 effect is zero. Frozen leftover-join.v10 of sarif stays frozen; do not
record it as current. Frozen leftover-join.v9 of sarif stays frozen; do not record it
as current. Frozen leftover-join.v8 of sarif stays frozen; do not record it as current.
Frozen leftover-join.v7 of sarif stays frozen; do not record it as current after this
successor is recorded. Frozen leftover-join.v5 of sarif stays frozen; do not record it
as current. Frozen leftover-join.v6 of sarif stays frozen; do not record it as current.
Frozen leftover-join.v4 of sarif stays frozen; do not record it as current. Claude
Stage A sarif leftover-join.v11 returned 3 observationsNotFindings objects OBS-1,
OBS-2, OBS-3; they travel as honesty work and this entry invents
no identifier. Does not invent a D-002 platform list, a PlanIntent
schema, a D9 code, a RunId recipe, or a section 7.1 recipe. Does
not remasure leftover-join.v7 of G29. Does not remasure leftover-join.v10 of G30. Does not remasure leftover-join.v20 of G21. Does
not remasure leftover-join.v10 of G19. Does not remasure leftover-join.v16 of G20. Does not remasure leftover-join.v6 of anti-lockstep. Does
not remasure leftover-join.v9 of platform-tcb. Does not author FC-OUTFAIL copies. Does not
author FC-OUTFAIL.committed-run-preserved. Does not copy onto
Windows. Does not advertise SARIF. Does not resurrect G17. Does
not flatten DR-107. Does not edit file 08. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET
on the naming half (28 of 28). Condition 5 last. This entry does
not edit file 08.

## Reversibility

Total only before a later dependent leftover rewrite, SATISFIED
cycle, or file-08 cell rewrite. Overturn: C-D345. Does not unwrite
D-115, D-182, D-293, D-296, D-297, D-325, or D-344.
