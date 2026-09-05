# D-325 — Record sarif leftover-join.v7 as DR-122 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-30
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `sarif-leftover-join.v7.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 through D-324. D-272 is CONTESTED and is not on that
> no-cell-edit adoption branch. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE. This is
> coordinator decision **D-325**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-122.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** pin QUALIFIED.
> **Does not** close leftover-design of OBL-FC-OUTFAIL-FX or OBL-FC-NONAUTH-TERM-FX.
> **Does not** steal G26 leftover from DR-131.
> **Does not** remasure occupancy v2 of G26.
> **Does not** remasure sarif-fc-nonauth-term-golden.v3.
> **Does not** remasure sarif-fc-outfail-golden.v3.
> **Does not** invent a D-002 platform list.
> **Does not** advertise SARIF.
> **Does not** resurrect G17.
> **Does not** mint a D9 code or a RunId recipe.
> **Does not** flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`.
> **Does not** flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
> **Does not** record sarif leftover-join.v4 as current after this successor is recorded.
> **Does not** record sarif leftover-join.v5 as current.
> **Does not** record sarif leftover-join.v6 as current.
> **Does not** remasure g21 leftover-join.v14.
> **Does not** remasure g20 leftover-join.v9.
> **Does not** remasure g19 leftover-join.v6.
> **Does not** remasure g30 leftover-join.v8.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption of this entry after CONSENT.

D-324 is ADOPTED at
`8bfcd02c36d28b079da2d29350beb6d3fac8168a`.
HEAD is `8bfcd02c36d28b079da2d29350beb6d3fac8168a`.
Last live heading is D-324. Required-now is 28. Last-heading custody only. D-325 does not unwrite D-324.

Stage A dual independent ACCEPT 0/0 of the frozen
successor (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/sarif-leftover-join.v7.review-independent.claude2.json` | `e3333252466220ffa0c2b90ddef209d483ab1374fe3968e8e33e26b0b809b219` | ACCEPT 0/0 (top-level verdict; no decision field) |
| Codex | `docs/coop/artifacts/sarif-leftover-join.v7.review-independent.codex.json` | `ad4ea6068a589d2c86b9300e812fa061a320dc03d57cfbe9b515019183bb81b4` | ACCEPT 0/0 (top-level verdict; decision is an object with members verdict, mustFixCount, shouldFixCount, blockerCount, reason) |

Frozen predecessor `sarif-leftover-join.v6.json` `dc5def46901093c05665fe3177f7103366dafa1f081a30a7f9c9b0b03fea693f` Stage A Claude REJECT MF-1 (`cd18921256ffdda406b8dd841938aef0335d3490704ca1080fd94554384cd038`); Codex REJECT 0 MUST-FIX 1 unlabeled SHOULD-FIX (`5ef80c124acc0441628f361720987b80e39a62090ef9134e991d22e998e5dc26`). Findings land at sarif leftover-join.v7 as one class. Frozen sarif leftover-join.v6 stays frozen; do not record it as current. Frozen predecessor `sarif-leftover-join.v5.json` `5d8ceccce1345c6093b4aba6a7c87b7a4cfd86ef77e6e600b7b5d1b7ce5fe510` Stage A Claude REJECT MF-1 SF-1 SF-2 (`e305c74d6308946c6573c8cb64cfcf16c65e3b6182e45d2aa4b47f0ecd02052b`); Codex ACCEPT 0/0 (`a96cd8be101f8d78c6bf940e032850c7e471b2b6b56ecf58368d0b000b4158e0`). Frozen sarif leftover-join.v5 stays frozen; do not record it as current. Frozen `sarif-leftover-join.v4.json` `a2ab59d79051337906ae610b4c34f8203dcac0d9038f2826b32f68630bd07640` remains the D-182 historical recording until this successor is recorded.

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifiers | Standing |
|---|---|---|
| Claude | none | Claude Stage A sarif leftover-join.v7 returned no observations field; no observationsNotFindings field; no findings field; no decision field; no advisories field; top-level verdict is ACCEPT; mustFix is an empty list; shouldFix is an empty list; blockers is an empty list |
| Codex | none | Codex Stage A sarif leftover-join.v7 returned no observations field; an empty observationsNotFindings list; no findings field; an empty mustFix list; an empty shouldFix list; an empty blockers list; no advisories field; decision is an object with members verdict, mustFixCount, shouldFixCount, blockerCount, reason; no findings member on decision; top-level verdict is ACCEPT |

This entry invents no identifier. It recites no Claude observations. Claude Stage A sarif leftover-join.v7 returned no observation identifiers. It recites no Codex observations. Codex Stage A sarif leftover-join.v7 returned no observation identifiers.

## Subject

Frozen `docs/coop/artifacts/sarif-leftover-join.v7.json` `2df7dedf150dff97319e18de78b0c2d8267aa3a77eedeadd8b966e92c194c31b`. Status CANDIDATE-NOT-APPLIED. binds NOTHING. leftoverDesign remains `[OBL-FC-OUTFAIL-FX, OBL-FC-NONAUTH-TERM-FX]`. leftover-design of the two D-296 FC-NONAUTH-TERM implementations is stale as an authoring claim. leftover-design of the D-297 FC-OUTFAIL.no-committed-run implementation is stale as an authoring claim. leftover-design of FC-OUTFAIL.committed-run-preserved remains NOT-AUTHORED under the section 7.1 RunId park. leftover-design of per-D-002-platform copies remains: G10 occupancy v2 platforms are quoted, ORDERED-EQUAL to G23 occupancy v2. Occupancy v2 remains the current G26 occupancy remasurement. Frozen G26 occupancy v2 remains unmoved. Frozen sarif-fc-nonauth-term-golden.v3 remains unmoved. Frozen sarif-fc-outfail-golden.v3 remains unmoved. Frozen `sarif-leftover-join.v4.json` `a2ab59d79051337906ae610b4c34f8203dcac0d9038f2826b32f68630bd07640` is the D-182 historical recording and is not current after this successor is recorded.

## Decision

Record sarif leftover-join.v7 as DR-122 leftover remasurement after D-324. The candidate binds NOTHING. DR-122 stays `PROPOSED-CLOSED-FOR-REVIEW`. leftover-design of OBL-FC-OUTFAIL-FX and OBL-FC-NONAUTH-TERM-FX remains true. leftover-design of the two D-296 implementations and of the D-297 no-committed-run implementation is stale as an authoring claim. leftover-design of FC-OUTFAIL.committed-run-preserved remains. Occupancy v2 remains the current G26 occupancy remasurement. Does not remasure G26 occupancy v2. Does not remasure sarif-fc-nonauth-term-golden.v3. Does not remasure sarif-fc-outfail-golden.v3. Does not SATISFY DR-117. Does not SATISFY DR-122. D-316 already opened D-056 Gate 1 Class A for DR-117; this entry does not open Class A for DR-117 or DR-122 and does not perform gates 4 or 5. Not SATISFIED. Not QUALIFIED. Required-now stays 28. Condition-4 effect is zero. Frozen sarif leftover-join.v5 and sarif leftover-join.v6 stay frozen; do not record them as current. Frozen sarif leftover-join.v4 stays frozen; do not record it as current after this successor is recorded. Claude Stage A sarif leftover-join.v7 returned no observation identifiers; this entry invents no identifier. Does not invent a D-002 platform list, a D9 code, a RunId recipe, a PlanIntent schema, the DR-131 pack, Rust-as-core, or a section 7.1 recipe. Does not advertise SARIF. Does not resurrect G17. Does not steal G26 leftover from DR-131. Does not flatten DR-107. Does not remasure G21. Does not remasure G20. Does not remasure G19. Does not remasure G30. Does not edit file 08. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last. This entry does not edit file 08.

## Reversibility

Total only before a later dependent leftover rewrite, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D325. Does not unwrite D-077, D-115, D-152, D-182, D-226, D-293, D-296, D-297, D-316, or D-324.
