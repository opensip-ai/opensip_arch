# D-175 — Record identity-namespace-leftover-join.v6 as DR-104 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1.
> Frozen turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `identity-namespace-leftover-join.v6.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 / D-171 / D-172 / D-173 / D-174. Not a three-limb
> act. Not a required-now successor.
> This is coordinator decision **D-175**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-104.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** change the file 08 token off
> DECIDED-V1-NOT-INTEGRATED.
> **Does not** execute the eleven classes.
> **Does not** record frozen v4 or v5 as a current
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G31 or G32.
> **Does not** force a ride onto G15.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

Turn-1 subject `coordinator-decisions.D-175.draft.md`
`1bbe85c00ecc8a5fed9838d24f8570b73dcdb21c60d8b2ef9ec2ee9d002d18a6`
held frozen. Claude 2 CONSENT, 0 MUST-FIX, 0 SHOULD-FIX.
Codex OBJECT, 1 SHOULD-FIX D175-SF1, 0 MUST-FIX.

| ID | Sev | Disposition |
|---|---|---|
| D175-SF1 | SHOULD-FIX | ACCEPTED. Turn 1 Reversibility omitted adopted D-168 from the D-167-through-D-174 non-unwrite span. Inserted D-168 after D-167. The clause now reads: Does not unwrite D-012, D-130, D-131, D-162, D-167, D-168, D-169, D-170, D-171, D-172, D-173, or D-174. |

Claude turn-1 CONSENT 0/0 is not a finding to land.

D-174 is ADOPTED at
`5945d46d8be631ffeb0cc8f49afb045910c535ba`.
HEAD is `5945d46d8be631ffeb0cc8f49afb045910c535ba`.
Last live heading is D-174. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/identity-namespace-leftover-join.v6.review-independent.claude2.json` | `eaa9e3b39eb896315e5f95e60294c0f3bae05ca3881404e732a76c7af91039b2` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/identity-namespace-leftover-join.v6.review-independent.codex.json` | `6ff7f24bc5025813254a569ef6a0d443c29c4e9bd0db20e0f8581175b20a679e` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| identity-namespace-leftover-join.v6.json | `ab31c6075723d34503958a838ad1a3c4da37b3644390b6df8117ae34758099cc` |
| identity-namespace-leftover-join.v6.review-independent.claude2.json | `eaa9e3b39eb896315e5f95e60294c0f3bae05ca3881404e732a76c7af91039b2` |
| identity-namespace-leftover-join.v6.review-independent.codex.json | `6ff7f24bc5025813254a569ef6a0d443c29c4e9bd0db20e0f8581175b20a679e` |
| COORDINATOR-DECISIONS.md | `37b9d5ce7498251d8204fe86b9344cc57a33ea42ca440e8ae622ac0ef3a0c390` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `5945d46d8be631ffeb0cc8f49afb045910c535ba` |
| Frozen v5 (not this subject) | `11779fcd170eb77098808223b7e6e164182ea4aaf0fa74f8d9a717300141a249` |
| Turn-1 subject (frozen) | `1bbe85c00ecc8a5fed9838d24f8570b73dcdb21c60d8b2ef9ec2ee9d002d18a6` |
| Claude 2 turn-1 verdict | `f7fd700eaa4fdec06515d7f50da2716c282ae0c1c51d13d33bcb64a5ac38b9a0` |
| Codex turn-1 verdict | `0c934f9b2557a0adcd3ae3ae7c56d0e35fe25d00a02d27155ad2425fde0b61c6` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v6, both
Stage A verdicts, the frozen turn-1 subject, both turn-1
verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-104 lead
token remains `DECIDED-V1-NOT-INTEGRATED`. DR-G31 is live.
v6's top-level head, recordedInputs.HEAD, file08Pin, and
both requiredNowUnchanged fields equal those live values.
Frozen v4 remains a historical measurement as of HEAD
`5d5d778` / required-now 26, before D-167. Frozen v5 stays
unmoved and is not recorded.

## Why this entry exists

Wave 2. Frozen v4 asserted required-now 26 at HEAD
`5d5d778` and treated G31 as not live. D-167 recorded
DR-G31. v5 remasured that G31 owns NT-11 execution and
received dual REJECT 0/1 (CLAUDE-INLJ-V5-SF1 / INLJ-V5-SF1).
v6 lands both findings. leftover-design of unnamed NT-11
execution remainder is measured closed. Remainder is G31
execution, which remains qualification. Dual independent
ACCEPT 0/0 now exists. This entry records v6. It is not
SATISFIED-GRADE. v4/v5 stay frozen; do not record them as
current.

## Decision

1. Record `identity-namespace-leftover-join.v6.json` as
   DR-104 leftover remasurement after D-174. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v4 and v5 are not
   recorded as a current remasurement.
2. DR-104 stays `DECIDED-V1-NOT-INTEGRATED`. leftover-design
   of unnamed NT-11 execution remainder is closed. Remainder
   is G31 execution. Naming is not execution. Not QUALIFIED.
3. Gate 1 Class A is not opened. Class B SATISFIED is not
   recorded. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not execute the eleven classes. Does not rewrite
   G31 or G32. Does not force a ride onto G15. Does not
   edit file 08. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D175. Does not unwrite D-012, D-130, D-131, D-162,
D-167, D-168, D-169, D-170, D-171, D-172, D-173, or D-174.
Does not unwrite the turn-1 OBJECT.
