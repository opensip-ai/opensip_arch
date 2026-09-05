# D-317 — Record g30-fixture-corpus.v2 as DR-G30 leftover-design fixture implementations

> **Status:** DRAFT — under review.
> **Date:** 2026-08-30
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g30-fixture-corpus.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 through D-316. D-272 is CONTESTED and is not on that
> no-cell-edit adoption branch. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE. This is
> coordinator decision **D-317**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-101.
> **Does not** SATISFY DR-G30.
> **Does not** pin QUALIFIED.
> **Does not** close leftover-design of OBL-G30-FX-AUTHORING.
> **Does not** remasure g30 leftover-join.v4.
> **Does not** remasure occupancy v2.
> **Does not** remasure g30-input-corpus.v1.
> **Does not** invent a PlanIntent schema.
> **Does not** invent the DR-131 pack.
> **Does not** mint Rust-as-core.
> **Does not** name G13 into required-now.
> **Does not** invent a D9 code, exit number, or HostTermination.
> **Does not** invent a section 7.1 recipe.
> **Does not** author G29 fixture bytes.
> **Does not** flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`.
> **Does not** flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption of this entry after CONSENT.

D-316 is ADOPTED at
`76cc272426e13a874b65d62bc2f2ed9771fe7f8f`.
HEAD is `76cc272426e13a874b65d62bc2f2ed9771fe7f8f`.
Last live heading is D-316. Required-now is 28. Last-heading custody only. D-317 does not unwrite D-316.

Stage A dual independent ACCEPT 0/0 of the frozen
successor (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g30-fixture-corpus.v2.review-independent.claude2.json` | `29bf3f84568b9c1de5901a3ba9e0c5a5d1d5349a53a008ba1d91cac7db582364` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g30-fixture-corpus.v2.review-independent.codex.json` | `4294e494d122099f216e05f39fb2e97e155dd04b5b637c837e31537713d4a8b7` | ACCEPT 0/0 |

Frozen predecessor `g30-fixture-corpus.v1.json` `0e86bd1690d92a6f33ca263f78aa0d3d582f9b1b5da1d0e0c682e397af1f6f0f` Stage A Claude REJECT CLAUDE-G30FX-V1-S1 (`557bcb724ddb1b8e6d7a9148650786f45fadd3bd3fe3f17ad831f0115c90380e`); Codex REJECT 0 MUST-FIX, 1 unlabeled SHOULD-FIX (`45d740fc830ec52e8c78ce910a80523b8cedb73986ae608c91786a1e04a0a394`). Findings land at g30-fixture-corpus.v2. Frozen g30-fixture-corpus.v1 stays frozen; do not record it as current.

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifiers | Standing |
|---|---|---|
| Claude | CLAUDE-G30FX-V2-O1, CLAUDE-G30FX-V2-O2, CLAUDE-G30FX-V2-O3 | Claude Stage A g30-fixture-corpus.v2 returned 3 named observationsNotFindings objects CLAUDE-G30FX-V2-O1, CLAUDE-G30FX-V2-O2, CLAUDE-G30FX-V2-O3 (members id, observation, severity, whyItDoesNotStandAsAFinding); an empty mustFix list; an empty shouldFix list; an empty advisories list; an empty blockers list; no observations field |
| Codex | none | Codex Stage A g30-fixture-corpus.v2 returned an empty observations list; an empty mustFix list; an empty shouldFix list; an empty advisories list; an empty blockers list; no observationsNotFindings field |

This entry names the Claude identifiers CLAUDE-G30FX-V2-O1, CLAUDE-G30FX-V2-O2, CLAUDE-G30FX-V2-O3; no identifier is invented. It recites no Codex observations. Codex Stage A g30-fixture-corpus.v2 returned no observation identifiers. Claude Stage A g30-fixture-corpus.v1 identifiers CLAUDE-G30FX-V1-S1, CLAUDE-G30FX-V1-O1 through CLAUDE-G30FX-V1-O7 travel as honesty work of the frozen predecessor. Codex Stage A g30-fixture-corpus.v1 returned no observation identifier.

## Subject

Frozen `docs/coop/artifacts/g30-fixture-corpus.v2.json` `c8ab0b08913c3889c72ab9fb62ac5158f980856d7a15bea5096d47595dcdc714`. Status CANDIDATE-NOT-APPLIED. binds NOTHING. Seven fixture files remain at `docs/coop/artifacts/fixtures/g30.v1/`. Frozen `docs/coop/artifacts/g30-leftover-join.v4.json` `3f3d84e0e24a2aea0ba95c282f809c8343d1827d0577ca8396d4560c5e012c75` remains the current recorded DR-G30 leftover-join (D-255). leftoverDesign remains `[OBL-G30-FX-AUTHORING]`. Frozen occupancy v2 remains unmoved. Frozen g30-input-corpus.v1 remains unmoved. This act does not remasure g30 leftover-join.v4.

## Decision

Record g30-fixture-corpus.v2 as DR-G30 leftover-design fixture implementations after D-316. The candidate binds NOTHING. DR-G30 stays `OPEN`. leftover-design of OBL-G30-FX-AUTHORING remains true on g30 leftover-join.v4 (D-255) because leftover-join remasurement is not this entry, leftoverDesignClosedIfAcceptedAndRecorded is empty, and per-platform copies remain a later successor. Does not remasure g30 leftover-join.v4. Does not remasure occupancy v2. Does not remasure g30-input-corpus.v1. Does not SATISFY DR-117. Does not SATISFY DR-G30. D-316 already opened D-056 Gate 1 Class A for DR-117; this entry does not open Class A and does not perform gates 4 or 5. Not SATISFIED. Not QUALIFIED. Required-now stays 28. Condition-4 effect is zero. Frozen g30-fixture-corpus.v1 stays frozen; do not record it as current. Claude Stage A observations CLAUDE-G30FX-V2-O1, CLAUDE-G30FX-V2-O2, CLAUDE-G30FX-V2-O3 travel as honesty work. Does not invent a PlanIntent schema, the DR-131 pack, Rust-as-core, a D9 code, or a section 7.1 recipe. Does not author G29 fixture bytes. Does not edit file 08. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last. This entry does not edit file 08.

## Reversibility

Total only before a later dependent leftover rewrite, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D317. Does not unwrite D-158, D-230, D-255, D-293, D-314, D-315, or D-316.
