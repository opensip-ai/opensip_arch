# D-296 — Record sarif-fc-nonauth-term-golden.v3 as DR-122 leftover-design FC-NONAUTH-TERM fixture implementations

> **Status:** DRAFT — under review.
> **Date:** 2026-08-28
> **Protocol:** D-000 new cycle, turn 2 of 3. Lands CLAUDE-D296-MF1 (Stage A observation disposition: OBS-1 has members detail, id, note, title, whyNotCharged; OBS-2 through OBS-5 have members detail, id, title, whyNotCharged and omit note), CLAUDE-D296-SF1 (Decision: Claude Stage A sarif-fc-nonauth-term-golden.v3 requested no change; OBS-1 through OBS-5 are reviewer-local labels and carry those identifiers), CLAUDE-D296-SF2 (the asymmetry guard: this entry does not claim that both reviewers' identifiers are preserved; Codex Stage A sarif-fc-nonauth-term-golden.v3 returned no observation identifiers), and the unlabeled Codex turn-1 SHOULD-FIX (same observation-member recital as CLAUDE-D296-MF1). All identifiers are named. The turn-1 subject remains frozen.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `sarif-fc-nonauth-term-golden.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 through D-271 and D-273 through D-295. D-272 is CONTESTED and is not on that
> no-cell-edit adoption branch. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE. This is
> coordinator decision **D-296**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-122.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-101.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-FC-NONAUTH-TERM-FX.
> **Does not** close leftover-design of OBL-FC-OUTFAIL-FX.
> **Does not** remasure leftover-join.v4.
> **Does not** author FC-OUTFAIL.
> **Does not** mint a D9 code.
> **Does not** invent a RunId or section 7.1 recipe.
> **Does not** invent a CommandEnvelope schema.
> **Does not** advertise SARIF.
> **Does not** resurrect G17.
> **Does not** invent a D-002 platform list.
> **Does not** pin QUALIFIED.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption of this entry after CONSENT.

D-295 is ADOPTED at
`b993902017d8f8fda5f9fc0590b402ec4c27a41f`.
HEAD is `b993902017d8f8fda5f9fc0590b402ec4c27a41f`.
Last live heading is D-295. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
successor (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/sarif-fc-nonauth-term-golden.v3.review-independent.claude2.json` | `73b9b58137ebbb710eaaac71048ffd3d0c8d1f7815e7f812c1b4c4d461ea7884` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/sarif-fc-nonauth-term-golden.v3.review-independent.codex.json` | `77601ced19170dd0d0a5c54d55337c183547ddb6f5c8a553bc552b19c777c4b9` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifiers | Standing |
|---|---|---|
| Claude | OBS-1, OBS-2, OBS-3, OBS-4, OBS-5 | Claude Stage A sarif-fc-nonauth-term-golden.v3 returned 5 named observations objects OBS-1, OBS-2, OBS-3, OBS-4, OBS-5 (each with members detail, id, title, whyNotCharged; OBS-1 additionally carries note); no observationsNotFindings field; no advisories field |
| Codex | none | Codex Stage A sarif-fc-nonauth-term-golden.v3 returned an empty observations list; an empty advisories list; no observationsNotFindings field |

This entry names the Claude Stage A sarif-fc-nonauth-term-golden.v3 reviewer-local labels OBS-1, OBS-2, OBS-3, OBS-4, OBS-5; no identifier is invented. It does not claim that both reviewers' identifiers are preserved. Codex Stage A sarif-fc-nonauth-term-golden.v3 returned no observation identifiers.

## Subject

`docs/coop/artifacts/sarif-fc-nonauth-term-golden.v3.json` `de3c859b4028ff8dcb8b71028809bf5339b7092d78bb0dc34dd7229a644cd5ed` — leftover-design fixture implementations for the two FC-NONAUTH-TERM namedCases on sarif-fc-nonauth-term-bind.v1, authored under D-293 Decision 8. Fixture files remain at `docs/coop/artifacts/fixtures/sarif-fc-nonauth-term.v1/` with no platform subdirectory. The D-002 platform list is quoted from G10 occupancy v2 and ORDERED-EQUAL against G23 occupancy v2; sarif-fc-nonauth-term-golden.v3 does not invent a D-002 platform list. Frozen sarif-fc-nonauth-term-golden.v1 was Claude ACCEPT 0/0 and Codex REJECT (one unlabeled SHOULD-FIX: D-293 Decision 8 pin); its findings landed at sarif-fc-nonauth-term-golden.v2. Frozen sarif-fc-nonauth-term-golden.v2 was Claude REJECT (reviewer-local label SF-1: incomplete speaker rename) and Codex ACCEPT 0/0; its findings landed at sarif-fc-nonauth-term-golden.v3. Neither predecessor is recorded as current.

## Decision

Record sarif-fc-nonauth-term-golden.v3 as DR-122 leftover-design FC-NONAUTH-TERM fixture implementations after D-295. The candidate binds NOTHING. DR-122 stays `PROPOSED-CLOSED-FOR-REVIEW`. leftover-design of OBL-FC-NONAUTH-TERM-FX remains on leftover-join.v4 (D-182) until a later leftover-join remasurement. leftover-design of OBL-FC-OUTFAIL-FX remains; this recording does not author FC-OUTFAIL. Does not remasure leftover-join.v4. Does not SATISFY DR-122. D-056 Eligibility gates 2 and 3 do not hold for DR-122. Gate 1 Class A is not opened. Not eligible in kind. Not SATISFIED. Required-now stays 28. Condition-4 effect is zero. Frozen sarif-fc-nonauth-term-golden.v1 and sarif-fc-nonauth-term-golden.v2 stay frozen; do not record them as current. Claude Stage A sarif-fc-nonauth-term-golden.v3 requested no change; OBS-1, OBS-2, OBS-3, OBS-4 and OBS-5 are reviewer-local labels and carry those identifiers. Does not invent a D9 code, a RunId recipe, a CommandEnvelope schema, or a D-002 platform list. Does not advertise SARIF. Does not resurrect G17. Does not edit file 08. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D296. Does not unwrite D-115, D-182, D-293, D-294, or D-295.
