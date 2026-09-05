# D-087 — Remove the duplicate D-056 heading

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a fourth
> turn of D-056. Frozen D-056 subjects are not edited.
> **Decision type:** RULE-GOVERNED. Recording hygiene. Same
> class as D-080 / D-073 (COORD recital correction). Does not
> reopen D-056.
> **Does not** mark any row SATISFIED.
> **Does not** amend D-056's adopted substance.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** coin a file-08 status token.
> **Does not** perform the D-085 SATISFIED re-record draft.

D-056 is ADOPTED at `75c981dd2b827c5ce11c37013b2e124870ee9c6e`.
Two CONSENT verdicts, 0 MUST-FIX, 0 SHOULD-FIX. This entry
does not overturn that adoption.

## Fact

C-D056 added **two** consecutive `## D-056` headings to
`COORDINATOR-DECISIONS.md`. Measured: the heading
`## D-056 — Condition-2 SATISFIED versus qualification remainder`
occurs **twice**. Cause: two apply writers appended in the
same commit window.

Both recitals cite the same frozen turn-2 subject
`dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82`
and the same two CONSENT verdicts
`8a95badbd92866d62f999a55c5226632880fb3498c75062aeab8f01f9bdf3d1c`
(Claude 2) and
`6e755bee06d991f9ac818899f7765690c9424a8e95199593bbce4ec3888fe434`
(Codex). Neither recital changes D-056's substance.

A decision register with two live ADOPTED entries for one id
is a recording defect. One heading must remain.

## Decision

1. **Keep the first D-056 recital** (the block that begins
   immediately after C-D084 and whose Readiness effect
   enumerates condition 2 NOT MET, condition 3 MET,
   condition 4 PARTLY MET, condition 5 NOT MET and last).
2. **Delete the second D-056 recital** in full, from the
   horizontal rule that precedes its heading through its
   `Commit: C-D056.` line, inclusive of that rule.
3. **Union one sentence into the kept Decision paragraph**,
   taken from the deleted recital and already true of the
   adopted D-056 draft, so row names are not lost:

   Eligible in kind, not performed: DR-102, DR-115, DR-119,
   DR-123. DR-103/104/105/114/118 and the twelve no-contract
   rows remain ineligible. D-002/D-010 deferrals stay on the
   deferral limb.

   Insert that sentence in the kept Decision immediately
   before "This entry marks no row SATISFIED".
4. Do not edit the frozen D-056 subjects or verdicts. Do not
   edit file 08. Do not mark SATISFIED. Do not reopen
   ADV-D056-01. Do not authorize `docs/v2/implementation/`.
   Do not adopt or freeze the in-flight D-085 SATISFIED draft.

## Alternatives

- Leave both headings. Rejected: one id, two ADOPTED recitals.
- Delete the first and keep the second. Rejected: the first
  already enumerates conditions 2–5 standings; the second
  does not.
- Re-open D-056. Rejected: dual CONSENT stands; this is
  recording hygiene.
- Silent working-tree edit without a D-000 entry. Rejected:
  D-000 clause 3 — COORD content is a recorded decision.
- Bundle this into D-085. Rejected: D-085 as currently
  drafted is a SATISFIED re-record, a different act.

## Readiness effect

Zero. D-056's readiness effect is unchanged. Condition 2
stays NOT MET. Condition 5 stays last.

## Reversibility

C-D087 plus restore of the deleted second recital and removal
of the union sentence. Does not overturn D-056. Overturn:
C-D087.

## Measured inputs at dispatch

| Path | sha256 |
|---|---|
| COORD | `e65753891eae66eaf7d870f9df2d59585b252336d35bb7dfef0a22380490a188` |
| file 08 | `ff2ebaddc782443a5c5a88590bd77d340ac6caf30ed788977221225f4838a811` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-056 commit | `75c981dd2b827c5ce11c37013b2e124870ee9c6e` |
| D-056 turn-2 subject | `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
