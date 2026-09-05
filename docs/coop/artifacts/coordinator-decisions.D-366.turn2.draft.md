# D-366 — Record the six silent deferral-limb dispositions in file 08

> **Status:** DRAFT — under review.
> **Date:** 2026-09-03
> **Protocol:** D-000, turn 2 of 3. Turn 1 drew OBJECT from both independent
> reviewers, at one MUST-FIX each and different ones. This turn lands every
> turn-1 identifier: **CODEX-D366-MF1**, **CLAUDE-D366-MF1**,
> **CLAUDE-D366-SF1**, **CLAUDE-D366-SF2**, **CLAUDE-D366-ADV-1**,
> **CLAUDE-D366-ADV-2**, **CLAUDE-D366-ADV-3**, **CLAUDE-D366-ADV-4**. Codex
> turn 1 returned `currentFindingIdentifiers` `["CODEX-D366-MF1"]` with empty
> shouldFix, advisories, observations and observationsNotFindings lists. Claude 2
> turn 1 returned `currentFindingIdentifiers` `["CLAUDE-D366-MF1",
> "CLAUDE-D366-SF1", "CLAUDE-D366-SF2"]`, four advisories and four unlabelled
> entries in its observationsNotFindings list; this entry invents no identifier
> for those four. The turn-1 subject `coordinator-decisions.D-366.draft.md`
> `ef07c22b95e8a5860758806e56c8f5e2e76c78d67e890614334172735f78646e` remains
> frozen and unrecorded.
> **Decision type:** RULE-GOVERNED. Recording-hygiene MF-6 discharging D-002's
> "never silence" requirement for six rows, and repairing the one condition-2
> prose clause this act makes false. This is coordinator decision **D-366**, not
> a register row.
> **Does not** mark any row `SATISFIED`, and does not change any lead label.
> **Does not** move any row between the SATISFIED-requiring set and the deferral
> limb, and changes no count: condition 2 stays 6 of 23 SATISFIED-requiring rows
> `SATISFIED` with 9 of 32 on the deferral limb (D-365).
> **Does not** defer, re-defer or un-defer anything: every disposition recorded
> here is D-002's, restated from D-002's own bytes.
> **Does not** author the DR-110 design D-002 requires "when authored"; it
> records only that row's deferral.
> **Does not** edit any acceptance-evidence cell, Blueprint-impact cell,
> gate-harness cell, or any row outside the six; the seventh edit is one prose
> clause of the condition-2 "Measured now" cell and touches no figure in it.
> **Does not** reach condition 1, whose qualifying set is DR-001–011, or any
> other condition's measurement.
> **Does not** amend D-000, D-001, D-002, D-010, D-056, D-134, D-363, D-364 or
> D-365. **Does not** change live required-now 28.
> **Does not** authorize `docs/v2/implementation/`.

HEAD is `82714f3e8143f91b0bb1765dfcf121d5f8bac420`.
Last live heading is D-365. Required-now is 28.
Live file 08 is
`1bcc5739a8089004aca513108c3e87d7762e489d7ba484f99e91990ff4835375`.

## Why this entry exists

D-002 records its deferrals under a heading stating its own requirement:
**"Explicit deferrals (each gets its recorded disposition, never silence)"**.
Nine rows sit on D-001 clause 2's deferral limb (D-365). Three carry their
disposition in their own file-08 status cell — DR-128, DR-129 and DR-130. **Six
do not.** DR-106, DR-109 and DR-113 read `OPEN / inherits hard blockers`;
DR-108, DR-110 and DR-116 read bare `OPEN`. Their dispositions exist only in
D-002. D-365 named the gap and left it to a separate act; this is that act.

## What turn 1 got wrong

Two independent MUST-FIXes.

**CLAUDE-D366-MF1.** D-365 wrote into the condition-2 "Measured now" cell that
the nine deferral-limb rows' "cells are unedited" and that "Six of the nine
carry no in-cell disposition … their in-cell recording is a later MF-6". Turn 1
performed exactly that later MF-6 while scoping itself to the six row cells, so
the adopted register would have said in one place that the six cells are
unedited and in six others that they were edited on 2026-09-03. D-001 turn-2
NOTE-1 requires a register-content act to amend file 08's condition-2 wording
"through the register's own process, so the checklist text and the register
never disagree". Turn 2 adds a seventh replacement repairing that clause. It
changes no figure: the counts stay 6 of 23 and 9 of 32.

**CODEX-D366-MF1**, with **CLAUDE-D366-SF2**. DR-113's note carried only the
purge-half prohibition and the local routing, dropping the whole-row rationale
D-002 records jointly for DR-106, DR-109 and DR-113. Turn 2 gives all three the
shared rationale and keeps DR-113's additional limbs.

**CLAUDE-D366-SF1.** D-002 binds "The DR-110 disposition, when authored" to draw
the DR-107/DR-G18 boundary and address file 02's unexercised "updates" entry.
Turn 1 left it undecidable whether D-366 was that authoring. Turn 2 says in bytes
that it is not: D-366 records the deferral only, and the authored design remains
a later act.

**CLAUDE-D366-ADV-2**, landed. Turn 1 attributed "its own artifact and commit" to
D-002 as a rule for each deferral disposition. In D-002 that phrase governs
"Each scoped inclusion elsewhere in this entry (DR-105, DR-124/G19, G09, and
G08)". Turn 2 does not repeat the attribution and rests the act on the "never
silence" requirement alone.

**CLAUDE-D366-ADV-4**, landed. Turn 1 asserted per row that DR-109's
acceptance-evidence cell "begins with applied DR-002..008 successors". Live
DR-109 begins "Applied evidence successor"; only DR-106 begins "Applied
DR-002–008". The claim is D-002's own, about the three rows jointly, and turn 2
attributes it to D-002 in quotation rather than asserting it of each row.

**CLAUDE-D366-ADV-3**, landed. Each note now follows its lead label with " — ",
matching DR-128, DR-129, DR-130 and DR-114.

**CLAUDE-D366-ADV-1**, recorded. D-002's Overturn bullet closes its one-revert
path once dependent commits land; C-D366 is such a commit, and this entry's own
Reversibility is C-D366 plus restoration of the seven spans, not a D-002 revert.

## What each disposition is, from D-002's bytes

- **DR-106, DR-109, DR-113** — "**DR-106, DR-109 and DR-113 are deferred
  WHOLLY**" (turn-1 MF-03), because "Authoritative sealed closure, replay, and
  evidence custody are OUT of slice 1"; D-002 records that their
  acceptance-evidence cells "all begin with applied DR-002..008 successors",
  that they close "via the condition-1 chain", and that "their design enters a
  later slice". For DR-113, D-002 adds that a "purge half" would have designed
  "the typed purge result DR-007 expressly forbids inventing", and that the
  slice's local purge/doctor needs "route through DR-124/DR-114/DR-G12/DR-107
  instead".
- **DR-108** — "no credential-requiring features in slice 1".
- **DR-110** — "self-update/repair — install is fresh signed download in slice
  1", with the repair-media/rollback surfaces deferring with it under D-002's
  G08 scoping, and D-002's forward requirement for the authored disposition.
- **DR-116** — "no third-party support policy needed yet".

## Decision

1. Record each of the six rows' D-002 deferral disposition in its own file-08
   status cell, appended after the existing lead label and text with " — ", in
   one scoped form naming D-366 as the recording act and D-002 as the source.
2. Repair the one condition-2 "Measured now" prose clause this act makes false,
   so the checklist text and the register agree (D-001 turn-2 NOTE-1). No figure
   in that cell changes.
3. Every lead label is unchanged. No row moves between the SATISFIED-requiring
   set and the deferral limb. No count changes.
4. D-366 is not the authored DR-110 disposition D-002 binds; that remains a
   later act.
5. **Exact file-08 edits, and no others:**

   - **DR-106** — replace this unique live string (occurs once):

```
| OPEN / inherits hard blockers | Hard blocker for authoritative analysis profile |
```

     with

```
| OPEN / inherits hard blockers — **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row WHOLLY (turn-1 MF-03), on the ground that authoritative sealed closure, replay and evidence custody are OUT of slice 1. D-002 records that DR-106, DR-109 and DR-113 "all begin with applied DR-002..008 successors" in their acceptance-evidence cells, that they close via the condition-1 chain, and that their design enters a later slice. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker for authoritative analysis profile |
```

   - **DR-108** — replace this unique live string (occurs once):

```
| OPEN | Hard blocker only for features requiring stored credentials; not a V1 secret law |
```

     with

```
| OPEN — **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row: no credential-requiring features in slice 1. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker only for features requiring stored credentials; not a V1 secret law |
```

   - **DR-109** — replace this unique live string (occurs once):

```
| OPEN / inherits hard blockers | Hard blocker for authoritative closure |
```

     with

```
| OPEN / inherits hard blockers — **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row WHOLLY (turn-1 MF-03), on the ground that authoritative sealed closure, replay and evidence custody are OUT of slice 1. D-002 records that DR-106, DR-109 and DR-113 "all begin with applied DR-002..008 successors" in their acceptance-evidence cells, that they close via the condition-1 chain, and that their design enters a later slice. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker for authoritative closure |
```

   - **DR-110** — replace this unique live string (occurs once):

```
 rollback, removable-media/expiry tests | OPEN | Hard blocker |
```

     with

```
 rollback, removable-media/expiry tests | OPEN — **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row: self-update/repair is out of slice 1 because install is a fresh signed download, and the repair-media/rollback trust surfaces defer with it under D-002's G08 scoping. D-002 further records that "The DR-110 disposition, when authored, must draw the DR-107/G18 generation-rollback versus self-update-rollback boundary and address file 02's unexercised 'updates' inventory entry"; that authoring is a later design act and is not performed by D-366, which records only the deferral. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker |
```

   - **DR-113** — replace this unique live string (occurs once):

```
| OPEN / inherits hard blockers | Hard blocker |
```

     with

```
| OPEN / inherits hard blockers — **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row WHOLLY (turn-1 MF-03), on the ground that authoritative sealed closure, replay and evidence custody are OUT of slice 1. D-002 records that DR-106, DR-109 and DR-113 "all begin with applied DR-002..008 successors" in their acceptance-evidence cells, that they close via the condition-1 chain, and that their design enters a later slice. D-002 adds, for this row, that a "purge half" would have designed the typed purge result DR-007 expressly forbids inventing, and that the slice's local purge and doctor needs route through DR-124, DR-114, DR-G12 and DR-107 instead. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker |
```

   - **DR-116** — replace this unique live string (occurs once):

```
| OPEN | Hard blocker for third-party ecosystem |
```

     with

```
| OPEN — **Deferral-limb disposition recorded 2026-09-03 (D-366; D-002 deferral, architecture-preview scope; not SATISFIED):** D-002 defers this row: no third-party support policy is needed yet. Lead label unchanged. This row is on D-001 clause 2's deferral limb (D-365) and is not a member of the SATISFIED-requiring set (D-002 as amended by D-134). | Hard blocker for third-party ecosystem |
```

   - **condition-2 Measured-now clause** — replace this unique live string (occurs once):

```
all nine keep the lead label `OPEN`, their cells are unedited, and 14 + 9 = 23 `OPEN` across the table. Six of the nine carry no in-cell disposition; theirs live in D-002 and their in-cell recording is a later MF-6.
```

     with

```
all nine keep the lead label `OPEN`, and 14 + 9 = 23 `OPEN` across the table. All nine carry an in-cell deferral disposition: DR-128, DR-129 and DR-130 from C4 / C-D010, and DR-106, DR-108, DR-109, DR-110, DR-113 and DR-116 recorded from D-002's bytes by D-366 (C-D366).
```

6. No other cell of these six rows is edited, no other row is touched, and no
   other span of the condition-2 cell is touched.

## Alternatives

- **Leave the six silent.** Rejected: D-002 requires each deferral to get "its
  recorded disposition, never silence", and six have had none since 2026-08-13.
- **Edit the six cells and leave the condition-2 clause stale.** Rejected: it
  would leave a known-false statement in the adopted register, against D-001
  turn-2 NOTE-1.
- **Change the lead labels to a deferred token.** Rejected: D-365 records that
  the nine keep their lead labels; minting a token is a scope act this entry
  does not hold.
- **Author the DR-110 disposition here.** Rejected: D-002 binds that authoring
  to content this entry does not hold, and it is a design act, not hygiene.
- **Record the dispositions in COORD only.** Rejected: they are already in
  D-002; the gap is on the rows.
- **Include the non-row deferrals** (Windows platform support; baseline/ratchet).
  Rejected: they are not register rows and have no cell.

## Readiness effect

Zero. No row becomes `SATISFIED`, no lead label changes, and no count moves:
condition 2 stays **6 of 23 SATISFIED-requiring rows `SATISFIED`, with 9 of 32
on the deferral limb**, and stays NOT MET. Conditions 1, 3 and 4 are unchanged;
required-now stays 28. Condition 5 remains NOT MET and last. The snapshot
heading date is not edited, keeping the D-135 / D-236 / D-363 / D-365 practice.

## Reversibility

C-D366 plus restore of the six prior status cells and the prior condition-2
prose clause. Total: nothing depends on these notes. Does not overturn D-001,
D-002, D-010, D-056, D-134, D-363, D-364 or D-365. Overturn: C-D366.

## Commit

C-D366.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORDINATOR-DECISIONS.md | `79a168425204ea1ed1c0b94439a4e4b530d027283902476d048f39e699e9ec8f` |
| file 08 | `1bcc5739a8089004aca513108c3e87d7762e489d7ba484f99e91990ff4835375` |
| HEAD | `82714f3e8143f91b0bb1765dfcf121d5f8bac420` |
| coordinator-decisions.D-366.draft.md (turn 1, frozen, unrecorded) | `ef07c22b95e8a5860758806e56c8f5e2e76c78d67e890614334172735f78646e` |
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
