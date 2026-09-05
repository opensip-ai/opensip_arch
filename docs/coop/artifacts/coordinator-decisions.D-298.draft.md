# D-298 — Record g20-fixture-corpus.v5 as DR-G20 leftover-design fixture implementations

> **Status:** DRAFT — under review.
> **Date:** 2026-08-28
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g20-fixture-corpus.v5.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 through D-271 and D-273 through D-297. D-272 is CONTESTED and is not on that
> no-cell-edit adoption branch. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE. This is
> coordinator decision **D-298**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-125.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-122.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-101.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G20-FX-AUTHORING.
> **Does not** steal leftover-design of OBL-SDK-API-RESERVED.
> **Does not** close OBL-DR125-ACTIVATION.
> **Does not** remasure leftover-join.v6.
> **Does not** remasure sdk leftover-join.v6.
> **Does not** author G19, OBL-HOSTILE-GOLDENS, or G21 fixture corpora.
> **Does not** invent an SDK language, framework, or API surface.
> **Does not** apply component-sdk-contract.v4.
> **Does not** mint a D9 code, exit number, or HostTermination.
> **Does not** invent a RunId or section 7.1 recipe.
> **Does not** invent a D-002 platform list.
> **Does not** advertise SARIF.
> **Does not** resurrect G17.
> **Does not** pin QUALIFIED.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption of this entry after CONSENT.

D-297 is ADOPTED at
`4d6478e8646b909b2fe9a8f5d4ade564357a23c0`.
HEAD is `4d6478e8646b909b2fe9a8f5d4ade564357a23c0`.
Last live heading is D-297. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
successor (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g20-fixture-corpus.v5.review-independent.claude2.json` | `2854f32bb642e8d6d7e08ebf0e0f5ba538015c19c74c866378f8bf634ddd4e33` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g20-fixture-corpus.v5.review-independent.codex.json` | `1a5361715ad36a1724f0525806f595a66a8e742cf4ebe25d2be42c019b3f88b5` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifiers | Standing |
|---|---|---|
| Claude | CLAUDE-G20FX-V5-A-1, CLAUDE-G20FX-V5-A-2, CLAUDE-G20FX-V5-A-3, CLAUDE-G20FX-V5-A-4 | Claude Stage A g20-fixture-corpus.v5 returned 4 named advisories objects. CLAUDE-G20FX-V5-A-1, CLAUDE-G20FX-V5-A-2, CLAUDE-G20FX-V5-A-3 have members carriesForward, id, observation, severity, suggestedShape, whyNotAFinding. CLAUDE-G20FX-V5-A-4 has members field, id, newAtV5, observation, severity, suggestedShape, whyItStillMatters, whyNotAFinding. No observations field; no observationsNotFindings field |
| Codex | none | Codex Stage A g20-fixture-corpus.v5 returned an empty observations list; an empty advisories list; no observationsNotFindings field |

This entry names the Claude identifiers CLAUDE-G20FX-V5-A-1, CLAUDE-G20FX-V5-A-2, CLAUDE-G20FX-V5-A-3, CLAUDE-G20FX-V5-A-4; no identifier is invented. It does not claim that both reviewers' identifiers are preserved. Codex Stage A g20-fixture-corpus.v5 returned no observation identifiers.

## Subject

`docs/coop/artifacts/g20-fixture-corpus.v5.json` `3d7d8dba4a7409b98720ae04a8f826f84271e9acfd7c804f2a21e12b78d612c8` — leftover-design fixture implementations for occupancy v2 namedCorpusClasses[0] (eight surfaces × the TypeScript provider) and for NT-4 and NT-7 as occupancy v2 namedCorpusWhenFixturesExist.dr133 records them, authored under D-293 Decision 8. Fixture files remain at `docs/coop/artifacts/fixtures/g20.v2/` with no platform subdirectory. The D-002 platform list is quoted from G20 occupancy v2 `#$.platforms` and ORDERED-EQUAL against G23 occupancy v2 and G10 occupancy v2; g20-fixture-corpus.v5 does not invent a D-002 platform list. Frozen g20-fixture-corpus.v1 was Claude REJECT (CLAUDE-G20FX-S-1) and Codex ACCEPT 0/0; its findings landed at g20-fixture-corpus.v2. Frozen g20-fixture-corpus.v2 was Claude ACCEPT 0/0 and Codex REJECT (unlabeled SHOULD-FIX on basedOn.g21FixtureCorpusV1.role speaker); its findings landed at g20-fixture-corpus.v3. Frozen g20-fixture-corpus.v3 was Claude REJECT (CLAUDE-G20FX-V3-S-1) and Codex ACCEPT 0/0; its findings landed at g20-fixture-corpus.v4. Frozen g20-fixture-corpus.v4 was dual REJECT (Claude CLAUDE-G20FX-V4-S-1; Codex unlabeled SHOULD-FIX, same class: component-sdk-contract.v4 bare version tokens); its findings landed at g20-fixture-corpus.v5. None of those predecessors is recorded as current.

## Decision

Record g20-fixture-corpus.v5 as DR-G20 leftover-design fixture implementations after D-297. The candidate binds NOTHING. DR-G20 stays `OPEN`. leftover-design of OBL-G20-FX-AUTHORING remains on leftover-join.v6 (D-269) and on sdk leftover-join.v6 (D-267) because leftover-join remasurement is not this entry, and closing that obligation needs a successor on both joins. leftover-design of OBL-SDK-API-RESERVED remains on sdk leftover-join.v6. Does not remasure leftover-join.v6. Does not remasure sdk leftover-join.v6. Does not SATISFY DR-125. Does not SATISFY DR-133. D-056 Eligibility gates 2 and 3 do not hold for DR-G20. Gate 1 Class A is not opened. Not eligible in kind. Not SATISFIED. Required-now stays 28. Condition-4 effect is zero. Frozen g20-fixture-corpus.v1, g20-fixture-corpus.v2, g20-fixture-corpus.v3, and g20-fixture-corpus.v4 stay frozen; do not record them as current. Claude Stage A advisories CLAUDE-G20FX-V5-A-1, CLAUDE-G20FX-V5-A-2, CLAUDE-G20FX-V5-A-3, CLAUDE-G20FX-V5-A-4 travel as honesty work. Does not invent an SDK API, a D9 code, a RunId recipe, a CommandEnvelope schema, or a D-002 platform list. Does not advertise SARIF. Does not resurrect G17. Does not edit file 08. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D298. Does not unwrite D-086, D-217, D-267, D-269, D-293, D-294, D-295, D-296, or D-297.
