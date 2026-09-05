# D-093 — Record host-effect-authorization.v8 as the D-032 host-effect candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a SATISFIED
> re-record. Frozen D-092 subjects are not edited. Not a
> fifth D-056 Class A/B SATISFIED.
> **Decision type:** RULE-GOVERNED. Records independent ACCEPT
> (0 blockers) of a design-contract candidate. Same recording
> class as D-013 / D-015 / D-035.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mark DR-105 or DR-114 `SATISFIED`.
> **Does not** apply, seal, or bind the contract.
> **Does not** record the joint-owner FC-C1 act.
> **Does not** overturn D-032, D-035, D-056, or D-092.

The recorded subject is the committed HEAD blob, not the
uncommitted working-tree mutation of the same path.

## Subject

`docs/coop/artifacts/host-effect-authorization.v8.json`
at committed digest
`2cbad5612e546d3bf915074a8ad3fc4cae444122c997e2ddb3fe067d3cd022dc`
(`git show HEAD:docs/coop/artifacts/host-effect-authorization.v8.json`).

Independent reviews of those exact bytes, 0 blockers:

- Claude 2 ACCEPT
  `host-effect-authorization.v8.review-independent.claude2.json`
  `36a961e82a375778e71a08e7a66067843abb29a26170c84c38a12f15e121dec9`
- Codex ACCEPT
  `host-effect-authorization.v8.review-independent.codex.json`
  `3be46716fd7156e1b1ea23d4e2c5b55e16fafc8b834d824cedc3a8a66d15de93`

A later uncommitted working-tree rewrite of the same path
hashes `2d95f22c99fa20eac2789e19e7b4723029d03d594a91fe24e996d03518918794`
and is not this subject. This entry does not record, reject,
or adopt that mutation.

D-032 is ADOPTED. D-035 is ADOPTED. D-092 is ADOPTED at
`48cef7a779ba29bef1902a16afe8a4e4675acfab`. This entry does
not overturn those.

## Decision

1. Record the committed v8 bytes as the host-effect
   design-contract candidate D-032 requires before any CA-1
   host head, CA-2, CA-3, or host CA-4 act is exercisable.
2. The artifact stays `CANDIDATE-NOT-APPLIED`, binds NOTHING,
   and remains `DO-NOT-SEAL`. Existence plus ACCEPT is not
   the joint-owner recording FC-C1 names.
3. DR-105 stays `OPEN`. `permission-truth-tables.v1` remains
   independently REJECT (3 blockers). A permission v2
   successor remains owed.
4. DR-114 stays `OPEN`. Doctor-contract.v4 (D-035) stands.
   Actor-join and fixture-corpus execution remain unmet.
5. **Exact file-08 edits, and no others:**
   - In the DR-105 status cell, replace this unique phrase
     (occurs once):

```
host-effect contract still required before host doctor acts
```

     with

```
host-effect design-contract candidate recorded 2026-08-14 (D-093, committed v8 `2cbad561…`); permission-truth-tables.v1 remains REJECT; the joint-owner FC-C1 recording and a permission v2 successor remain; row stays OPEN
```

   - In the DR-114 status cell, replace this unique phrase
     (occurs once):

```
the host-effect contract and fixture-corpus execution remain
```

     with

```
host-effect design-contract candidate recorded 2026-08-14 (D-093, committed v8 `2cbad561…`); actor-join and fixture-corpus execution remain
```

   - Do not change condition-2 SATISFIED counts. Do not
     rewrite D-088 gate-harness cells. Do not remove either
     row's Blueprint hard-blocker.
6. Does not mark DR-105/114 SATISFIED. Does not waive
   BLK-1..BLK-4. Does not authorize
   `docs/v2/implementation/`.

## Alternatives

- Record the uncommitted working-tree mutation
  `2d95f22c…`. Rejected: those bytes have no ACCEPT on
  themselves; the dual ACCEPT is of `2cbad561…`.
- Mark DR-105 or DR-114 SATISFIED. Rejected: leftover is
  not only execution (D-056 ineligible class). D-056's
  eligible-in-kind set is exhausted (D092-N-1).
- Treat ACCEPT as the joint-owner FC-C1 recording.
  Rejected: D-032 / the artifact's own layers.
- Leave the accepted candidate unrecorded. Rejected:
  D-013/D-035 class — an independently accepted contract
  is recorded; the row stays OPEN on remaining halves.
- Authorize implementation. Rejected: condition 5 last.

## Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 30 and NOT MET.
Condition 4 unchanged. Condition 5 remains NOT MET and last.

## Reversibility

C-D093 plus restore of the two unique DR-105/DR-114 phrases.
Does not overturn D-032, D-035, or D-092.

## Measured inputs at dispatch

| Path | sha256 |
|---|---|
| COORD | `19eeb34d30d5d7652d36cfa3fca8cdea1f4f7a0975ee9e555226e263d3bcfd87` |
| file 08 | `947454dd4695217b3658b794b59b081a309b4f93d01fa0bb868c9b9edaf46e75` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-092 commit | `48cef7a779ba29bef1902a16afe8a4e4675acfab` |
| committed v8 | `2cbad5612e546d3bf915074a8ad3fc4cae444122c997e2ddb3fe067d3cd022dc` |
| Claude 2 v8 | `36a961e82a375778e71a08e7a66067843abb29a26170c84c38a12f15e121dec9` |
| Codex v8 | `3be46716fd7156e1b1ea23d4e2c5b55e16fafc8b834d824cedc3a8a66d15de93` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
