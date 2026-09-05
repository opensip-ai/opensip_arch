# D-093 — Record host-effect-authorization.v8 as the D-032 host-effect candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Frozen
> turn-1 subject is not edited. Not a SATISFIED re-record.
> Not a fifth D-056 Class A/B SATISFIED.
> **Decision type:** RULE-GOVERNED. Records independent ACCEPT
> (0 blockers) of a design-contract candidate. Same recording
> class as D-013 / D-015 / D-035 / D-042.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mark DR-105 or DR-114 `SATISFIED`.
> **Does not** apply, seal, or bind the contract.
> **Does not** record the joint-owner FC-C1 act.
> **Does not** overturn D-032, D-035, D-042, D-056, or D-092.

Turn-1 subject `coordinator-decisions.D-093.draft.md`
`fd45e7d177dbab44d7edd6dcf994eb8b5c5f650f6bc4e1003ca3c5dbc27f3713`
held frozen. Claude 2 OBJECT, 1 MUST-FIX D093-MF-1. Codex
CONSENT, 0 MUST-FIX, 0 SHOULD-FIX.

| ID | Sev | Disposition |
|---|---|---|
| D093-MF-1 | MUST-FIX | ACCEPTED. D-042 already recorded permission-truth-tables.v2. This entry no longer says a permission v2 successor is owed. The DR-105 write now records D-042/v2 alongside the host-effect candidate. Advisory honesty work is named as P2-01/P2-02/P2-03/PT2-CX-A1, not as a missing v2. |
| D093-N-1 | NOTE | ACCEPTED into the retrieval qualifier. The file-08 write names `git show HEAD:` so the committed digest is not verified by hashing the mutated working-tree path. |

The recorded host-effect subject is the committed HEAD blob, not
the uncommitted working-tree mutation of the same path.

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
and is not this subject.

D-032 is ADOPTED. D-035 is ADOPTED. D-042 is ADOPTED.
D-092 is ADOPTED at `48cef7a779ba29bef1902a16afe8a4e4675acfab`.
This entry does not overturn those.

## Decision

1. Record the committed v8 bytes as the host-effect
   design-contract candidate D-032 requires before any CA-1
   host head, CA-2, CA-3, or host CA-4 act is exercisable.
2. The artifact stays `CANDIDATE-NOT-APPLIED`, binds NOTHING,
   and remains `DO-NOT-SEAL`. Existence plus ACCEPT is not
   the joint-owner recording FC-C1 names.
3. DR-105 stays `OPEN`. `permission-truth-tables.v2`
   `cce3afcaee90bbca388825a474751d6ebb17b30722b35dadcf6c631b34a8731a`
   remains that row's accepted design-contract candidate
   (D-042). `permission-truth-tables.v1` remains the rejected
   predecessor. Remaining unmet, named: joint-owner FC-C1
   recording; fixture execution at DR-G09; BLK-1..BLK-4
   STILL-ROUTED; D-042 advisory honesty work P2-01, P2-02,
   P2-03, and PT2-CX-A1. A full permission v2 successor is
   not owed.
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
host-effect design-contract candidate recorded 2026-08-14 (D-093; retrieve with `git show HEAD:docs/coop/artifacts/host-effect-authorization.v8.json`, digest `2cbad561…`); permission-truth-tables.v2 remains the accepted DR-105 design-contract candidate (D-042, `cce3afca…`); the joint-owner FC-C1 recording, DR-G09 fixture execution, and BLK-1..BLK-4 remain; D-042 advisories P2-01/P2-02/P2-03/PT2-CX-A1 remain owed as honesty work; row stays OPEN
```

   - In the DR-114 status cell, replace this unique phrase
     (occurs once):

```
the host-effect contract and fixture-corpus execution remain
```

     with

```
host-effect design-contract candidate recorded 2026-08-14 (D-093; retrieve with `git show HEAD:docs/coop/artifacts/host-effect-authorization.v8.json`, digest `2cbad561…`); actor-join and fixture-corpus execution remain
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
- Say a permission v2 successor remains owed. Rejected:
  D093-MF-1; D-042 already recorded v2.
- Mark DR-105 or DR-114 SATISFIED. Rejected: leftover is
  not only execution (D-056 ineligible class). D-056's
  eligible-in-kind set is exhausted (D092-N-1).
- Treat ACCEPT as the joint-owner FC-C1 recording.
  Rejected: D-032 / the artifact's own layers.
- Leave the accepted host-effect candidate unrecorded.
  Rejected: D-013/D-035/D-042 class.
- Authorize implementation. Rejected: condition 5 last.

## Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 30 and NOT MET.
Condition 4 unchanged. Condition 5 remains NOT MET and last.

## Reversibility

C-D093 plus restore of the two unique DR-105/DR-114 phrases.
Does not overturn D-032, D-035, D-042, or D-092.

## Measured inputs at turn-2 dispatch

| Path | sha256 |
|---|---|
| COORD | `19eeb34d30d5d7652d36cfa3fca8cdea1f4f7a0975ee9e555226e263d3bcfd87` |
| file 08 | `947454dd4695217b3658b794b59b081a309b4f93d01fa0bb868c9b9edaf46e75` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-092 commit | `48cef7a779ba29bef1902a16afe8a4e4675acfab` |
| committed v8 | `2cbad5612e546d3bf915074a8ad3fc4cae444122c997e2ddb3fe067d3cd022dc` |
| permission v2 | `cce3afcaee90bbca388825a474751d6ebb17b30722b35dadcf6c631b34a8731a` |
| Claude 2 v8 | `36a961e82a375778e71a08e7a66067843abb29a26170c84c38a12f15e121dec9` |
| Codex v8 | `3be46716fd7156e1b1ea23d4e2c5b55e16fafc8b834d824cedc3a8a66d15de93` |
| turn-1 subject | `fd45e7d177dbab44d7edd6dcf994eb8b5c5f650f6bc4e1003ca3c5dbc27f3713` |
| Claude 2 turn 1 | `0a13d5a63c652761e28f1e3faccb198661becc6334417376e20e981b179031ba` |
| Codex turn 1 | `f732ab598ca286c48133864c406cfed997757e0f0ff67120dcf8c02ef7bd8cc5` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
