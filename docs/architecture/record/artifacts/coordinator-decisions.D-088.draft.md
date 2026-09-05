# D-088 — File 08 MF-6: write presently recordable harness identifiers

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a fourth turn
> of D-086. Frozen D-086 subjects are not edited.
> **Decision type:** RULE-GOVERNED. File-08 content change
> (D-001 MF-6) bound by D-086 rider RB-GHN-V3-A1.
> **Does not** mark any row SATISFIED.
> **Does not** make condition 4 MET.
> **Does not** claim QUALIFIED or DEMONSTRATED.
> **Does not** execute any harness.
> **Does not** pin G03/G04 machines.
> **Does not** write G03/G04 as named.
> **Does not** write G17 as required-now.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** coin a new file-08 status token.

D-086 is ADOPTED at `14865abc42c13b9759f5761c2873db03b708ea32`.
This entry does not overturn D-086. It is the MF-6 write D-086
scheduled.

## Decision

1. **Write identifiers only for the 16 presently recordable
   required names.** Prefix each file-08 "Platform matrix /
   harness" cell with the exact string in the table below,
   then a space, then the current cell text unchanged.
2. **Do not write G03/G04 as named.** Prefix those two cells
   with the reservation strings below. They remain required
   and unnamed.
3. **Do not write G17 as required-now.** Prefix that cell
   with the dropped string below.
4. **Do not change G06, G11, or G13 cells** except G13
   receives the reservation prefix below (zero C4 progress;
   still not in the 18-gate required-now set).
5. **Rewrite only the condition-4 snapshot "Measured now"
   cell** as specified below. Do not change the snapshot
   heading date. Do not change the "What that means"
   paragraph except to replace `no gate names a concrete
   harness artifact` if that phrase still appears; it does
   not appear in the current paragraph, so leave the
   paragraph unchanged.
6. Does not mark SATISFIED. Does not claim QUALIFIED. Does
   not execute a harness. Does not authorize
   `docs/v2/implementation/`. Does not edit D-070/D-081/D-084
   notes.

## Exact prefixes (16 recordable)

Each prefix is followed by the live cell text, unchanged.

| Gate | Prefix inserted at start of harness cell |
|---|---|
| DR-G01 | `named: harness.DR-G01.core-download (D-086; not authored; not QUALIFIED).` |
| DR-G02 | `named: harness.DR-G02.core-installed (D-086; not authored; not QUALIFIED).` |
| DR-G05 | `named: harness.DR-G05.component-delta (D-086; not authored; not QUALIFIED).` |
| DR-G07 | `named: harness.DR-G07.exact-bytes (D-086; not authored; not QUALIFIED).` |
| DR-G08 | `named: harness.DR-G08.trust-recovery.install-surfaces (D-086; not authored; not QUALIFIED).` |
| DR-G09 | `named: harness.DR-G09.permissions.preview-scoped (D-086; not authored; not QUALIFIED).` |
| DR-G10 | `named: harness.DR-G10.provider-conformance.ts-major-1 (D-086; not authored; not QUALIFIED).` |
| DR-G12 | `named: harness.DR-G12.doctor-purge.preview (D-086; not authored; not QUALIFIED).` |
| DR-G14 | `named: harness.DR-G14.language-runtime-ux.typescript (D-086; not authored; not QUALIFIED).` |
| DR-G15 | `named: harness.DR-G15.packaging-adapter-conformance (D-086; not authored; not QUALIFIED).` |
| DR-G16 | `named: harness.DR-G16.ci-isolation-integration (D-086; not authored; not QUALIFIED).` |
| DR-G18 | `named: harness.DR-G18.lifecycle-generation-recovery (D-086; not authored; not QUALIFIED).` |
| DR-G19 | `named: harness.DR-G19.state-class-authority.preview-classes (D-086; not authored; not QUALIFIED).` |
| DR-G20 | `named: harness.DR-G20.component-operability (D-086; not authored; not QUALIFIED).` |
| DR-G21 | `named: harness.DR-G21.component-failure-containment (D-086; not authored; not QUALIFIED).` |
| DR-G22 | `named: harness.DR-G22.platform-abi-loader (D-086; not authored; not QUALIFIED).` |

## Exact prefixes (not named / not required-now)

| Gate | Prefix |
|---|---|
| DR-G03 | `reserved, not named (D-006 machine pins owed; D-086).` |
| DR-G04 | `reserved, not named (D-006 machine pins owed; D-086).` |
| DR-G13 | `reserved, not named (blocked on DR-118; D-086; zero C4 progress).` |
| DR-G17 | `dropped / inapplicable (D-077 SARIF drop; D-086). not required-now.` |

G06 and G11 are unchanged.

## Exact condition-4 "Measured now" replacement

Current:

**22 of 22 owners named** at role level; **no gate names a concrete harness artifact**; every assurance stage is below `QUALIFIED`; 19 `OPEN`, 3 `HARD-BLOCKED`

New:

**22 of 22 owners named** at role level; **16 of 18 required gates name a recorded identifier** (D-086 / D-088; not authored; not QUALIFIED); G03/G04 remain required and unnamed pending a D-006-conforming successor; G17 is inapplicable (D-077); every assurance stage is below `QUALIFIED`; 19 `OPEN`, 3 `HARD-BLOCKED`

Standing stays **PARTLY MET**.

## Alternatives

- Leave file 08 silent after D-086. Rejected: D-086 scheduled
  this MF-6; condition 4 still reads 0 named.
- Write G03/G04 as named. Rejected: RB-GHN-V3-A1 / GHN-V1-B2.
- Present 16 of 16. Rejected: GHN-V2-B1 / RB-GHN-V3-A1.
- Write G17 as required-now. Rejected: D-077 / RB-GHN-V3-A1.
- Mark condition 4 MET. Rejected: 16 of 18 is not all required
  gates named; MET is not QUALIFIED.
- Authorize implementation. Rejected: condition 5 remains last.

## Readiness effect

Condition 4 stays PARTLY MET. Named-harness half becomes 16
of 18 required in file 08. Owners remain 22 of 22. No
QUALIFIED. No SATISFIED. Condition 5 remains NOT MET and last.

## Reversibility

C-D088 plus restore of the prior 20 harness-cell prefixes
(16 named + G03/G04/G13/G17) and the prior condition-4
"Measured now" cell. Does not overturn D-086. Overturn:
C-D088.

## Measured inputs at dispatch

| Path | sha256 |
|---|---|
| COORD | `6dd904094be239a44ccff8f7b654815a1a2815d0951ce29fbe3e97b7cac848ec` |
| file 08 | `ff2ebaddc782443a5c5a88590bd77d340ac6caf30ed788977221225f4838a811` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| v3 | `b5236612394a3d24259f3b11b99e9928b530a4be3d147d2007d00c3ee96c3ccd` |
| D-086 commit | `14865abc42c13b9759f5761c2873db03b708ea32` |
| D-087 commit | `953b23116e337ca289a2a02613753697119cfbf9` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
