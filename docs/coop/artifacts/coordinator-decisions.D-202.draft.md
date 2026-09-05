# D-202 — Record g27-leftover-join.v3 as G27 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g27-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-201. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-202**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-131.
> **Does not** invent a sealed-Run class.
> **Does not** take over G19.
> **Does not** reopen leftover-design of DR-131 NT-6.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G27-FX-AUTHORING.
> **Does not** invent fixture bytes.
> **Does not** record frozen v1 or v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G27, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-201 is ADOPTED at
`7b50de693acfff2a6d46dbc54601567ff47396ac`.
HEAD is `7b50de693acfff2a6d46dbc54601567ff47396ac`.
Last live heading is D-201. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g27-leftover-join.v3.review-independent.claude2.json` | `82d0369e17c95ec2de53c8d5501337b49434a65a46ae39ed01acb1889d4ebfa9` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g27-leftover-join.v3.review-independent.codex.json` | `290dd425e0b74a7df69e7cbddec4f75d0d14718bc1abd1ca750e35b1330022dd` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g27-leftover-join.v3.json | `38c48e49bb02db824d216115821fbb8ce08cfacfbfa5da902f08912081d8a88d` |
| g27-leftover-join.v3.review-independent.claude2.json | `82d0369e17c95ec2de53c8d5501337b49434a65a46ae39ed01acb1889d4ebfa9` |
| g27-leftover-join.v3.review-independent.codex.json | `290dd425e0b74a7df69e7cbddec4f75d0d14718bc1abd1ca750e35b1330022dd` |
| COORDINATOR-DECISIONS.md | `cadadbd49f75aaa01bf1b29e5d391211a36fad49a127834229dbbaab890624f0` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `7b50de693acfff2a6d46dbc54601567ff47396ac` |
| Frozen v2 (historical, not this subject) | `802268daf22538c7ad1790da1c366a7aa527fd92a212e6f325342fc530ea4017` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G27 lead
token remains `OPEN`. v3's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins and replaces
D-167 placeholder sentences with carry-safe phrasing.
leftover-design of OBL-G27-FX-AUTHORING remains. Dual
independent ACCEPT 0/0 now exists. This entry records v3.
It is not SATISFIED-GRADE. v1 and v2 stay frozen; do not
record them as current.

## Decision

1. Record `g27-leftover-join.v3.json` as G27 leftover
   remasurement after D-201. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v1 and v2 are not recorded as a
   current remasurement.
2. DR-G27 stays `OPEN`. leftover-design of
   OBL-G27-FX-AUTHORING remains. G27 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-131. Does not invent a sealed-Run
   class. Does not take over G19. Does not reopen
   leftover-design of DR-131 NT-6. Gate 1 Class A is not
   opened. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes. Does not rewrite G27,
   G31, or G32. Does not edit file 08. Does not invent a
   D9 code. Does not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D202. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, or D-201.
