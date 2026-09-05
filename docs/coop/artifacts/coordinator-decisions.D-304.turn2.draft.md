# D-304 — Record component-manifest leftover-join.v12 as DR-103 leftover remasurement (OD-2 final do-not-fold)

> **Status:** DRAFT — under review.
> **Date:** 2026-08-29
> **Protocol:** D-000 new cycle, turn 2 of 3. Lands the unlabeled Codex turn-1 SHOULD-FIX. Subject now reads: The C7-a(i) limb is not this artifact. Turn-1 Claude 2 CONSENT 0/0 (`artifacts/coordinator-decisions.D-304.review-adversarial.claude2.json` `accd6441cf1290b78897f5bd2cd0aba46c0d5db8e66dd1e067d9e3669b9bb126`); turn-1 Codex OBJECT 0 MUST-FIX, 1 SHOULD-FIX (`artifacts/coordinator-decisions.D-304.review-adversarial.codex.json` `985ed2cf6a1a4d29049a96ec7e51d7ca37f6a0fb4a323f036262e482b218ef43`). Claude Stage B turn-1 observations CLAUDE-D304-O1, CLAUDE-D304-O2, CLAUDE-D304-O3, CLAUDE-D304-O4, CLAUDE-D304-O5 have members id, measurement, title; an empty advisories list; no observationsNotFindings field. Codex Stage B turn-1 returned an empty mustFix list; a 1-member shouldFix list with no id member (members claimUnderReview, doesNotRequire, measurement, path, primaryEvidence, requiredRepair, severity, title, whyNotMustFix, whyShouldFix); an empty advisories list; an empty observations list; an empty observationsNotFindings list. All identifiers are named. No identifier is invented. The turn-1 subject remains frozen.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `component-manifest-leftover-join.v12.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 through D-271 and D-273 through D-303. D-272 is CONTESTED and is not on that
> no-cell-edit adoption branch. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE. This is
> coordinator decision **D-304**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-103.
> **Does not** SATISFY DR-120.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-101.
> **Does not** open D-056 Class A.
> **Does not** assign OD-1's owner.
> **Does not** invent OD-1 numbers.
> **Does not** fold OD-2 onto a conditionalRequires shape.
> **Does not** invent a schemas successor.
> **Does not** edit file 08.
> **Does not** pin QUALIFIED.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption of this entry after CONSENT.

D-303 is ADOPTED at
`2f9ffc66be9a9f6a36daeb4efbca1561becab858`.
HEAD is `2f9ffc66be9a9f6a36daeb4efbca1561becab858`.
Last live heading is D-303. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
successor (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/component-manifest-leftover-join.v12.review-independent.claude2.json` | `ca170adeb96f23e76982a36453b569eca6076c4a3eda19d33c6a29f2fe193f2b` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/component-manifest-leftover-join.v12.review-independent.codex.json` | `3a52996c2c87dfcfb0054a5487491e996f745936819e49ff9c6d975795afe8e8` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifiers | Standing |
|---|---|---|
| Claude | CLAUDE-CMLJ-V12-A1 | Claude Stage A component-manifest leftover-join.v12 returned 1 named advisoriesNotFindings object (CLAUDE-CMLJ-V12-A1 has members forcesReject, id, observation, path, severity). No observations field; no observationsNotFindings field |
| Codex | none | Codex Stage A component-manifest leftover-join.v12 returned an empty mustFix list; an empty shouldFix list; no advisories field; no observations field; no observationsNotFindings field |

This entry names the Claude identifier CLAUDE-CMLJ-V12-A1; no identifier is invented. It does not claim that both reviewers' identifiers are preserved. Codex Stage A component-manifest leftover-join.v12 returned no observation identifiers.

## Subject

`docs/coop/artifacts/component-manifest-leftover-join.v12.json` `948eff600d593a3eed5e04715cdc4cb90c92876c114c9fc788051d687874c0b8` — DR-103 leftover remasurement of component-manifest leftover-join.v9 (D-282) under D-293 Decision 7 C7 OD-2 as a final do-not-fold disposition. leftoverDesign of OBL-OD-2 is false. leftoverDesign remains `[OBL-WINDOWS-PATH, OBL-ENVELOPE-MISMATCH, OBL-UNICODE-NORM, OBL-OD-1]`. This is the first recorded leftoverDesign flip of a RESERVED/UNDECIDED-value obligation. Frozen leftover-join.v10 was Claude REJECT (CLAUDE-CMLJ-V10-SF1, CLAUDE-CMLJ-V10-SF2) and Codex ACCEPT 0/0. Frozen leftover-join.v11 was dual REJECT (CLAUDE-CMLJ-V11-B1, CLAUDE-CMLJ-V11-B2, CLAUDE-CMLJ-V11-SF1, CLAUDE-CMLJ-V11-SF2; Codex three unlabeled SHOULD-FIX). Neither predecessor is recorded as current. OD-1 owner stays UNASSIGNED. The C7-a(i) limb is not this artifact.

## Decision

Record component-manifest leftover-join.v12 as DR-103 leftover remasurement after D-303. The candidate binds NOTHING. DR-103 stays `OPEN`. leftover-design of OBL-OD-2 is measured closed as a final do-not-fold. leftover-design of OBL-WINDOWS-PATH, OBL-ENVELOPE-MISMATCH, OBL-UNICODE-NORM, and OBL-OD-1 remains. Does not assign OD-1's owner. Does not invent OD-1 numbers. Does not fold OD-2 onto a conditionalRequires shape. Does not invent a schemas successor. Does not steal OBL-AT-FX-AUTHORING or OBL-ADAPTER-IMPL. Does not SATISFY DR-103. D-056 Eligibility gates 2 and 3 do not hold for DR-103. Gate 1 Class A is not opened. Not eligible in kind. Not SATISFIED. Required-now stays 28. Condition-4 effect is zero. Frozen leftover-join.v10 and leftover-join.v11 stay frozen; do not record them as current. Claude Stage A advisory CLAUDE-CMLJ-V12-A1 travels as honesty work. The unlabeled Codex Stage B turn-1 SHOULD-FIX is landed. Claude Stage B turn-1 observations CLAUDE-D304-O1, CLAUDE-D304-O2, CLAUDE-D304-O3, CLAUDE-D304-O4, CLAUDE-D304-O5 travel as honesty work. Codex Stage B turn-1 returned no observation identifiers. Does not invent a D9 code or a D-006 unit. Does not edit file 08. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D304. Does not unwrite D-013, D-104, D-106, D-174, D-214, D-266, D-270, D-282, D-290, D-293, D-303.
