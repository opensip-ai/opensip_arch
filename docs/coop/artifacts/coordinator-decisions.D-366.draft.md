# D-366 — Record the six silent deferral-limb dispositions in file 08

> **Status:** DRAFT — under review.
> **Date:** 2026-09-03
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Recording-hygiene MF-6 discharging D-002's
> "never silence" requirement for six rows. This is coordinator decision
> **D-366**, not a register row.
> **Does not** mark any row `SATISFIED`, and does not change any lead label.
> **Does not** move any row between the SATISFIED-requiring set and the deferral
> limb, and changes no count: condition 2 stays 6 of 23 SATISFIED-requiring rows
> `SATISFIED` with 9 of 32 on the deferral limb (D-365).
> **Does not** defer, re-defer or un-defer anything: every disposition recorded
> here is D-002's, restated from D-002's own bytes.
> **Does not** edit any acceptance-evidence cell, Blueprint-impact cell,
> gate-harness cell, or any row outside the six.
> **Does not** reach condition 1, whose qualifying set is DR-001–011.
> **Does not** amend D-000, D-001, D-002, D-010, D-056, D-134, D-363, D-364 or
> D-365. **Does not** change live required-now 28.
> **Does not** authorize `docs/v2/implementation/`.

HEAD is `82714f3e8143f91b0bb1765dfcf121d5f8bac420`.
Last live heading is D-365. Required-now is 28.
Live file 08 is
`1bcc5739a8089004aca513108c3e87d7762e489d7ba484f99e91990ff4835375`.

## Why this entry exists

D-002 records its deferrals under a heading that states the requirement in its
own words: **"Explicit deferrals (each gets its recorded disposition, never
silence)"**. Nine rows sit on D-001 clause 2's deferral limb (D-365). Three of
them carry their disposition in their own file-08 status cell: DR-128, DR-129
and DR-130. **Six do not.** DR-106, DR-109 and DR-113 read `OPEN / inherits hard
blockers`; DR-108, DR-110 and DR-116 read bare `OPEN`. Their dispositions exist
only in D-002.

D-365 named this gap and expressly declined to close it, because D-002 gives
each disposition "its own artifact and commit". This entry is that act. It adds
nothing D-002 does not already decide.

## What each disposition is, from D-002's bytes

- **DR-106, DR-109, DR-113** — D-002: "**DR-106, DR-109 and DR-113 are deferred
  WHOLLY**" (turn-1 MF-03), because "Authoritative sealed closure, replay, and
  evidence custody are OUT of slice 1", "their acceptance-evidence cells all
  begin with applied DR-002..008 successors", and DR-113's "purge half" would
  have designed "the typed purge result DR-007 expressly forbids inventing"; the
  slice's local purge/doctor needs "route through DR-124/DR-114/DR-G12/DR-107
  instead". D-002 also records they close "via the condition-1 chain; their
  design enters a later slice".
- **DR-108** — D-002: "no credential-requiring features in slice 1".
- **DR-110** — D-002: "self-update/repair — install is fresh signed download in
  slice 1", with the repair-media/rollback surfaces deferring with it under
  D-002's G08 scoping. D-002 further records that "The DR-110 disposition, when
  authored, must draw the DR-107/G18 generation-rollback versus
  self-update-rollback boundary and address file 02's unexercised 'updates'
  inventory entry."
- **DR-116** — D-002: "no third-party support policy needed yet".

## Decision

1. Record each of the six rows' D-002 deferral disposition in its own file-08
   status cell, appended after the existing lead label and text, in one scoped
   form that names D-366 as the recording act and D-002 as the source.
2. Every lead label is unchanged. No row moves between the SATISFIED-requiring
   set and the deferral limb. No count changes.
3. The DR-110 note carries D-002's own forward requirement — the DR-107/DR-G18
   boundary and file 02's unexercised "updates" entry — so that requirement is
   visible on the row rather than only in D-002.
4. **Exact file-08 edits, and no others:**

   - **DR-106** — replace this unique live string (occurs once):

```
| OPEN / inherits hard blockers | Hard blocker for authoritative analysis profile |
```

     with

```
| OPEN / inherits hard blockers **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row WHOLLY (MF-03): authoritative sealed closure, replay and evidence custody are OUT of slice 1, its acceptance-evidence cell begins with applied DR-002..008 successors, it closes via the condition-1 chain, and its design enters a later slice. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker for authoritative analysis profile |
```

   - **DR-108** — replace this unique live string (occurs once):

```
| OPEN | Hard blocker only for features requiring stored credentials; not a V1 secret law |
```

     with

```
| OPEN **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row: no credential-requiring features in slice 1. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker only for features requiring stored credentials; not a V1 secret law |
```

   - **DR-109** — replace this unique live string (occurs once):

```
| OPEN / inherits hard blockers | Hard blocker for authoritative closure |
```

     with

```
| OPEN / inherits hard blockers **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row WHOLLY (MF-03): authoritative sealed closure, replay and evidence custody are OUT of slice 1, its acceptance-evidence cell begins with applied DR-002..008 successors, it closes via the condition-1 chain, and its design enters a later slice. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker for authoritative closure |
```

   - **DR-113** — replace this unique live string (occurs once):

```
| OPEN / inherits hard blockers | Hard blocker |
```

     with

```
| OPEN / inherits hard blockers **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row WHOLLY (MF-03): a "purge half" would have designed the typed purge result DR-007 expressly forbids inventing, and the slice's local purge and doctor needs route through DR-124, DR-114, DR-G12 and DR-107 instead. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker |
```

   - **DR-116** — replace this unique live string (occurs once):

```
| OPEN | Hard blocker for third-party ecosystem |
```

     with

```
| OPEN **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row: no third-party support policy is needed yet. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker for third-party ecosystem |
```

   - **DR-110** — replace this unique live string (occurs once):

```
 rollback, removable-media/expiry tests | OPEN | Hard blocker |
```

     with

```
 rollback, removable-media/expiry tests | OPEN **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row: self-update/repair is out of slice 1 because install is a fresh signed download, and the repair-media/rollback trust surfaces defer with it (D-002's G08 scoping). D-002 records that this disposition, when authored, must draw the DR-107/DR-G18 generation-rollback versus self-update-rollback boundary and address file 02's unexercised "updates" inventory entry. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker |
```

5. No other cell of these six rows is edited, and no other row is touched.

## Alternatives

- **Leave the six silent.** Rejected: D-002 requires each deferral to get "its
  recorded disposition, never silence", and six have had none since 2026-08-13.
- **Change the lead labels to a deferred token.** Rejected: D-365 records that
  the nine deferral-limb rows keep their lead labels, and minting a token is a
  scope act this entry does not hold.
- **Record the dispositions in COORD only.** Rejected: they are already in
  D-002; the gap is on the rows, which is where a reader looks.
- **Restate D-002's reasoning in the coordinator's own words.** Rejected: each
  note restates D-002's bytes and cites D-002, so nothing new is decided.
- **Include the non-row deferrals** (Windows platform support; baseline/ratchet).
  Rejected: they are not register rows and have no cell.

## Readiness effect

Zero. No row becomes `SATISFIED`, no lead label changes, and no count moves:
condition 2 stays **6 of 23 SATISFIED-requiring rows `SATISFIED`, with 9 of 32
on the deferral limb**, and stays NOT MET. Conditions 1, 3 and 4 are unchanged;
required-now stays 28. Condition 5 remains NOT MET and last.

## Reversibility

C-D366 plus restore of the six prior status cells. Total: nothing depends on
these notes. Does not overturn D-001, D-002, D-010, D-056, D-134, D-363, D-364
or D-365. Overturn: C-D366.

## Commit

C-D366.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORDINATOR-DECISIONS.md | `79a168425204ea1ed1c0b94439a4e4b530d027283902476d048f39e699e9ec8f` |
| file 08 | `1bcc5739a8089004aca513108c3e87d7762e489d7ba484f99e91990ff4835375` |
| HEAD | `82714f3e8143f91b0bb1765dfcf121d5f8bac420` |
| D-363 commit | `7c8a1c965152b094744e41bf86361a772315df97` |
| D-364 commit | `d4e93724092d425ef00c24570fe50c451144f934` |
| D-365 commit | `3b4aab267f487e00525eb0043dec7c566840ad63` |

D-002 predates the `D-NNN: …` commit-subject convention and carries no such
commit; it is pinned by its COORD heading, and COORD is pinned above.

If a cited file moves in a way that is not append-only COORD growth or COORD
heading hygiene, with file 08 and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with those files unmoved,
is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
