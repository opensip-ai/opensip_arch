# D-143 — File 08 MF-6: add DR-G23 as DR-131 NT leftover C4 owner

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. File-08 content change
> (D-001 MF-6). Performs the first D-139 L step for the
> already-recorded DR-131 leftover: name the missing
> condition-4 / DR-G* obligation that D-138 found absent.
> Scoped successor to D-086's required-now cardinality
> only (18 → 19) by adding this one gate. This is
> coordinator decision **D-143**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** make DR-131 eligible in kind.
> **Does not** close leftover-design (mapping NT-1..NT-8
> onto this gate is a later own L cycle).
> **Does not** edit DR-131, DR-133, or DR-117 Status cells.
> **Does not** add DR-G24 or any other gate.
> **Does not** change condition-2 arithmetic.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-142 is ADOPTED at `2d1254e29247cc54de7aaab611c20f953edd62fe`.

Measured inputs:

| Path | sha256 |
|---|---|
| file 08 | `7128f62ecea3d8121b670359fa0ca0bce4ec2df8a8f4680bb3edba09f42b865f` |
| COORDINATOR-DECISIONS.md | `64d76c32aa7f1c9c1ed1e0ebd9f0c328e0872c60ea9d68ce41369d6d5b8365c1` |
| preview-analyze-contract.v2.json | `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` |
| D-142 commit | `2d1254e29247cc54de7aaab611c20f953edd62fe` |

If a cited file moves in a way that is not append-only COORD
growth with file 08, the v2 candidate, and this draft
unmoved, re-measure before adoption. Append-only COORD after
this remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Why this entry exists

D-138 recorded that NT-1..NT-8 assign no owner and no
`existingGate`, and that no DR-G obligation names them.
D-056 Eligibility (3) requires each execution remainder to
be already named as a condition-4 / DR-G* obligation with
an owner. D-139 scheduled that leftover as L. This entry
names the missing obligation. It does not map the NT
classes, does not author the harness, and does not
SATISFY DR-131.

The gate restates admission and policyOutcome-mapping
classes already specified in independently ACCEPTed
`preview-analyze-contract.v2.json`. It does not invent
product law. NT-4 remains DR-133. NT-5 remains D-077 /
DR-G17 inapplicable.

## Exact edit

Two file-08 edits only. Locate by text, not a remembered
line number.

### Edit 1 — insert one gate row

Locate the unique line beginning `| DR-G22 `. Insert
immediately after that line, before the blank line and
`## Blueprint-readiness decision`, this row (verbatim):

    | DR-G23 PREVIEW-ANALYZE-ADMISSION | Preview analyze admits only the named first-party declarative pack; refuses user/third-party and imperative packs; a missing required TypeScript semantic rung is typed Coverage-indeterminate; the host does not mint fail/warn or a D9 class from policyOutcome; a preview result is not a sealed Run | named: harness.DR-G23.preview-analyze-admission (D-143; not authored; not QUALIFIED). preview analyze admission and policyOutcome-mapping corpus | retained class results for pack-admission, imperative-refusal, missing-rung, non-sealed-run, host-must-not-mint-verdict, host-must-not-mint-d9 | Product + CLI / output | SPECIFIED, not QUALIFIED | pass all named classes; no silent syntax fallback; no host-minted policy | OPEN |

No other gate-table byte changes. DR-G01..DR-G22 are
untouched.

### Edit 2 — condition-4 snapshot cell

Locate the unique snapshot row beginning `| 4 | Gates have`.
Replace only that row's Measured-now cell.

Before (verbatim):

    **22 of 22 owners named** at role level; **18 of 18 required gates name a recorded identifier** (D-086 / D-088 / D-102; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); every assurance stage is below `QUALIFIED`; 19 `OPEN`, 3 `HARD-BLOCKED`

After (verbatim):

    **23 of 23 owners named** at role level; **19 of 19 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-143; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G23 named under D-143; G17 is inapplicable (D-077); every assurance stage is below `QUALIFIED`; 20 `OPEN`, 3 `HARD-BLOCKED`

Standing stays **MET**. No other snapshot byte changes.
Condition 2 stays **4 of 32 SATISFIED** and **NOT MET**.
The 65-row preamble is unchanged (gates excluded).

## Decision

1. Apply the two file-08 edits above and no other file-08
   edit.
2. DR-G23 is a condition-4 execution-remainder owner for
   later mapping of DR-131 NT-1, NT-2, NT-3, NT-6, NT-7,
   and NT-8. This entry does not perform that mapping.
3. Marks nothing SATISFIED. Opens no Class A. Admits no
   leftover-design row. Does not close leftover-design.
4. Does not edit DR-131, DR-133, or DR-117. Does not add
   DR-G24. Does not succeed D-086 except the required-now
   cardinality 18 → 19.
5. Does not authorize `docs/v2/implementation/`. Does
   not mint a D-096 (A) grant.
6. Does not edit COORD except the append-only adoption
   of this entry after CONSENT.

### Readiness effect

Zero SATISFIED added. Condition 2 stays 4 of 32.
Condition 4 stays MET. Condition 5 last.

### Reversibility

Total before a later dependent mapping, SATISFIED-grade
application, or further gate-table rewrite of DR-G23.
Overturn deletes the DR-G23 row and restores the
condition-4 measured cell. Overturn: C-D143. Does not
unwrite D-086, D-088, D-102, D-138, D-139, or D-142.
