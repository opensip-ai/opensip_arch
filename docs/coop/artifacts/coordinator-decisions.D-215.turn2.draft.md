# D-215 — Record harness.DR-G16.ci-isolation-integration.v5 as G16 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Frozen
> turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G16.ci-isolation-integration.v5.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-214. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-215**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-121.
> **Does not** SATISFY DR-117.
> **Does not** apply monorepo-ci-contract.v16.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** invent reserved CI encodings.
> **Does not** steal leftover-design of OBL-CI-ENCODING-RESERVED.
> **Does not** close leftover-design of OBL-G16-FX-AUTHORING.
> **Does not** record frozen v1, v2, v3, or v4 as a current
> occupancy remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G10, G14, G15, G16, G31, or
> G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

Turn-1 subject `coordinator-decisions.D-215.draft.md`
`dc40a3fa2a9711be996d142febb1743a2e51f66aa2e7ea31027b76644f8128f0`
held frozen. Claude 2 OBJECT, 0 MUST-FIX, 1 SHOULD-FIX
CLAUDE-D215-SF1. Codex CONSENT, 0 MUST-FIX, 0 SHOULD-FIX.

| ID | Sev | Disposition |
|---|---|---|
| CLAUDE-D215-SF1 | SHOULD-FIX | ACCEPTED. Decision item 4 now states that G16V5-OBS-2 is one shared class with the Claude Stage A notRaised naming-v6 path standing, which carries no identifier; the Codex identifier is preserved. |

D-214 is ADOPTED at
`28b4b0510af35c24b0fcb991824fc4f606bf7fae`.
HEAD is `28b4b0510af35c24b0fcb991824fc4f606bf7fae`.
Last live heading is D-214. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G16.ci-isolation-integration.v5.review-independent.claude2.json` | `246993a8c653d129348b4a470e82cc5e68f7724d24406223391e1e9086f44602` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G16.ci-isolation-integration.v5.review-independent.codex.json` | `629e5bca9b3df142bf1134f4eb3a7ac7404d48050acc2bdde2c6038e9a43e286` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G16.ci-isolation-integration.v5.json | `3e3107499ffb576c11b3d4c290470921062066f518cbd80b6a563b446ebc918e` |
| harness.DR-G16.ci-isolation-integration.v5.review-independent.claude2.json | `246993a8c653d129348b4a470e82cc5e68f7724d24406223391e1e9086f44602` |
| harness.DR-G16.ci-isolation-integration.v5.review-independent.codex.json | `629e5bca9b3df142bf1134f4eb3a7ac7404d48050acc2bdde2c6038e9a43e286` |
| COORDINATOR-DECISIONS.md | `2547f85075a51602d920dbe3271a9e8613ec6ab3f58404bcf1cf2f8742c95086` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `28b4b0510af35c24b0fcb991824fc4f606bf7fae` |
| Frozen turn-1 draft (not this subject) | `dc40a3fa2a9711be996d142febb1743a2e51f66aa2e7ea31027b76644f8128f0` |
| Turn-1 Claude OBJECT CLAUDE-D215-SF1 | `9366bbdd264bf9bce8e781813dc092012e815000bc0da763b16040849f32583e` |
| Turn-1 Codex CONSENT 0/0 | `a9bb6157a8492284d3dfb9c51784b9166dc16e0e12f6bba49b32468f06118a5a` |
| Frozen v1 (Claude REJECT CLAUDE-G16-V1-SF1, not this subject) | `6719ca75c19b2a2d303069becd09786c2ea7b6f85aeeca0f336baedb349791a7` |
| Frozen v2 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `8662bfa0868c5276e27423a8c2f353f87c214d3117ce6241ea647699317d89d7` |
| Frozen v3 (Claude REJECT CLAUDE-G16-V3-MF1 / CLAUDE-G16-V3-SF1, not this subject) | `30e08b3b01f082664f7d2471508742f67e41a0b3cc937de6b1beb3a278c472ee` |
| Frozen v4 (Claude REJECT CLAUDE-G16-V4-MF1 / CLAUDE-G16-V4-SF1, not this subject) | `5f591eda728648552cad8eda9982ea3292792bc53843f7972284a304faf04363` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v5, both
Stage A verdicts, frozen v1/v2/v3/v4, frozen turn-1 draft, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G16 lead
token remains `OPEN`; DR-121 remains `OPEN`. v5's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G16 (D-086). Frozen v2 remains a historical occupancy
as of HEAD `5d5d778` / required-now 26. Frozen v1, v3, and
v4 remain Claude-REJECT occupancies.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v2 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, and leftoverNameNote that no leftover-join
existed. After file 08 cardinality 28, g16 leftover-join.v3
(D-192) is the current G16 leftover-join and monorepo
leftover-join.v3 (D-181) is the current DR-121 leftover-join.
v3 remasured occupancy then Claude REJECTED CLAUDE-G16-V3-MF1
(executesVerbatim rewrote naming-v6 executes) and
CLAUDE-G16-V3-SF1 (bare leftover-join.v3 leftoverDesign of
DR-121). v4 landed the executesVerbatim half and the
leftover-join token, then Claude REJECTED CLAUDE-G16-V4-MF1
(basedOn.namingV6.role still truncated naming-v6 executes)
and CLAUDE-G16-V4-SF1 (registerRowNote roster omitted v3).
v5 lands those findings. Dual independent ACCEPT 0/0 now
exists. This entry records v5. It is not SATISFIED-GRADE.
v1, v2, v3, and v4 stay frozen; do not record them as
current.

## Decision

1. Record
   `harness.DR-G16.ci-isolation-integration.v5.json`
   as G16 occupancy remasurement after D-214. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1, v2, v3, and v4 are
   not recorded as a current occupancy remasurement.
2. DR-G16 stays `OPEN`. leftover-design of OBL-G16-HARNESS-SPEC
   remains measured closed at leftover-join.v3 (D-192).
   leftover-design of OBL-G16-FX-AUTHORING remains. Remainder
   is G16 execution once fixture implementations exist. Does
   not pin QUALIFIED. Does not invent fixture bytes. Does
   not invent reserved CI encodings. Does not apply v16.
   Does not steal OBL-CI-ENCODING-RESERVED.
3. Does not SATISFY DR-121. Does not SATISFY DR-117. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
4. Claude Stage A returned zero advisories. Codex Stage A
   returned zero advisories and three honesty observations,
   not findings: G16V5-OBS-1 (dr121Split still uses the
   v2-era "authors" verb), G16V5-OBS-2 (frozen naming v6
   still carries its at-authoring v1 path and artifactExists
   false), and G16V5-OBS-3 (monorepo-ci-contract.v16 retains
   an older whole-file file-08 pin). G16V5-OBS-2 is one
   shared class with the Claude Stage A notRaised naming-v6
   path standing, which carries no identifier; the Codex
   identifier is preserved. CLAUDE-D215-SF1 was landed. CLAUDE-G16-V3-MF1,
   CLAUDE-G16-V3-SF1, CLAUDE-G16-V4-MF1, and CLAUDE-G16-V4-SF1
   were landed in the occupancy bytes. CLAUDE-G16-V1-SF1
   remains retained. Does not execute fixtures. Does not
   rewrite G07, G08, G10, G14, G15, G16, G31, or G32. Does
   not edit file 08. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D215. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, or D-214.
