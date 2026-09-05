# D-365 — Re-measure condition 2 over its qualifying set: three deferred rows sit on the deferral limb

> **Status:** DRAFT — under review.
> **Date:** 2026-09-02
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Re-measurement of the condition-2 snapshot
> against the rows it summarises, plus a D-001 MF-6 file-08 edit. This is
> coordinator decision **D-365**, not a register row.
> **Does not** mark any row `SATISFIED`, and does not change any row's lead label.
> **Does not** edit the status cell, acceptance-evidence cell or Blueprint-impact
> cell of DR-128, DR-129, DR-130, or any other row.
> **Does not** make condition 2 MET.
> **Does not** change condition 4's `32 of 32 owners named` measurement, which
> counts owners across every row of the table and is unaffected by which rows the
> condition-2 SATISFIED limb quantifies over.
> **Does not** change live required-now 28, and edits no gate-harness cell.
> **Does not** decide product scope: it measures the scope dispositions the rows
> already carry.
> **Does not** defer, re-defer, or un-defer anything.
> **Does not** perform D-056 Eligibility gate 4 or gate 5 for any row.
> **Does not** amend D-000, D-001, D-002, D-010, D-056, D-133, D-135 or D-363.
> **Does not** authorize `docs/v2/implementation/`.

HEAD is `7c8a1c965152b094744e41bf86361a772315df97` (D-363 ADOPTED).
Last live heading is D-363. Required-now is 28.
Live file 08 is
`476cfe5650f98fa30a3620a0a206e9db8fdddbda124b3c1ac8da355eb0149510`.

## Why this entry exists

Condition 2's authoritative text is D-001 checklist clause 2, quoted from live
file 08:

> Every row of the V2 architecture and product decisions table **that affects
> the first blueprint slice** is `SATISFIED` (wording made range-free by
> `COORDINATOR-DECISIONS.md` D-010 per D-001's new-row rule — the delta:
> DR-128/129 enter this condition's literal text for the first time, benign
> because both carry D-002 dispositions; and DR-130 joins the table);
> **deferred items have explicit product/architecture scope dispositions.**

The clause has two limbs. The first quantifies over rows that affect the first
blueprint slice. The second asks of deferred items only that they carry explicit
product/architecture scope dispositions.

The measured snapshot has been counting one limb over all thirty-two rows. The
snapshot block says of itself, in live file 08:

> This is a **dated snapshot of the rows above, and asserts nothing they do not**.
> Rows are authoritative; if this block and a row disagree, the row wins and this
> block is stale.

Three rows disagree with it. Each carries an explicit scope disposition in its
own status cell, and each states in its own bytes that it does not reach the
first blueprint slice:

| Row | Status cell, verbatim lead | Blueprint impact cell, verbatim |
|---|---|---|
| DR-128 | `OPEN — deferred post-MVP by recorded scope (DR-128/file 10; normalized 2026-08-13, C4)` | `Not an MVP blueprint blocker.` |
| DR-129 | `OPEN — deferred; applies only to a slice that elects a TUI, which slice 1 does not (normalized 2026-08-13, C4)` | `Blocks only a slice that elects to include a TUI; never blocks or replaces the mandatory CLI baseline` |
| DR-130 | `OPEN — slice 1 claims no upgrade continuity and its deferral disposition is RECORDED HERE (D-010, C-D010): DR-130 does not affect the first blueprint slice` | `Blocks any slice claiming upgrade continuity` |

DR-130's cell uses clause 2's own qualifying language verbatim: it "does not
affect the first blueprint slice". D-010's own change record, in COORD, states
that DR-128 and DR-129 entering condition 2's literal text is "benign because
both carry D-002 dispositions".

The same measured table already reports a two-limb condition in two components.
Condition 1 reads **`1 of 11 SATISFIED; 10 of 11 explicitly disposed for
architecture preview`**. Condition 2 is reported in one component only. This
entry brings the condition-2 report into the form its own clause and its
sibling condition already use.

## What this entry measures, and what it does not decide

This entry decides no product scope. The three dispositions are owner recordings
already in the register: D-002's deferrals for DR-128 and DR-129, and D-010 /
C-D010 for DR-130. This entry reads them and counts accordingly.

The qualifying set is a property of the slice, not of this entry. If a later
slice elects a TUI, DR-129 re-enters the SATISFIED limb by its own cell. If a
later slice claims upgrade continuity, DR-130 does. If MVP scope changes,
DR-128 does. Those cells are not edited here and continue to govern.

## Decision

1. Record that condition 2's SATISFIED limb quantifies over the **29** rows of
   the table that affect the first blueprint slice, and that DR-128, DR-129 and
   DR-130 sit on the clause's deferral limb, each carrying the explicit
   product/architecture scope disposition that limb requires.
2. Condition 2 remains **NOT MET**: of the 29 rows on the SATISFIED limb, 6 are
   `SATISFIED` and 23 are not (20 `OPEN`, 1 `DECIDED-V1-NOT-INTEGRATED`, 2
   `PROPOSED-CLOSED-FOR-REVIEW`).
3. Arithmetic. The table carries 32 rows. Before this entry: 6 `SATISFIED`, 23
   `OPEN`, 1 `DECIDED-V1-NOT-INTEGRATED`, 2 `PROPOSED-CLOSED-FOR-REVIEW`;
   6 + 23 + 1 + 2 = 32. DR-128, DR-129 and DR-130 each carry the lead label
   `OPEN`, so moving the three to the deferral limb leaves 29 on the SATISFIED
   limb: 6 + 20 + 1 + 2 = 29, and 29 + 3 = 32.
4. **Exact file-08 edits, and no others:**
   - Replace this unique live text (occurs once):

```
**6 of 32 `SATISFIED`** — 23 `OPEN`, 1 `DECIDED-V1-NOT-INTEGRATED`, 2 `PROPOSED-CLOSED-FOR-REVIEW`.
```

     with

```
**6 of 29 slice-affecting rows `SATISFIED`; 3 of 32 on the deferral limb with explicit product/architecture scope dispositions** — among the 29: 20 `OPEN`, 1 `DECIDED-V1-NOT-INTEGRATED`, 2 `PROPOSED-CLOSED-FOR-REVIEW`. Deferral limb (D-365): DR-128 deferred post-MVP by recorded scope (D-002; file 10); DR-129 applies only to a slice that elects a TUI, which slice 1 does not (D-002); DR-130's deferral disposition is recorded at D-010 / C-D010 and its cell states it does not affect the first blueprint slice. Their lead labels stay `OPEN` and their cells are unedited; each re-enters the SATISFIED limb by its own cell if a later slice reaches it.
```

   - In "What that means in one sentence", replace only this unique clause
     (occurs once):

```
condition 2 remains 6 of 32 SATISFIED
```

     with

```
condition 2 remains 6 of 29 slice-affecting rows SATISFIED, with 3 rows on the deferral limb
```

5. The condition-2 "Required" cell already reads "Every slice-affecting V2 row
   `SATISFIED`" and is not edited. Condition 4's `32 of 32 owners named` is not
   edited: owners are named for every row of the table, including the three on
   the deferral limb.

## Alternatives

- **Leave the snapshot counting 32.** Rejected: the snapshot's own words make
  the rows authoritative when they disagree with it, and three rows disagree.
- **Edit the three rows' cells to a new status token.** Rejected: the
  dispositions are already recorded there; a new token would be a scope decision
  this entry does not hold, and D-001 clause 2 asks for dispositions, not a
  token.
- **Treat the three as `SATISFIED`.** Rejected: they are not, and the deferral
  limb does not ask them to be.
- **Read the deferral limb as reaching any `OPEN` row with any deferral
  language.** Rejected: the limb is read here only for rows whose own cells
  state they do not reach the first blueprint slice. DR-107 and DR-122 carry
  `PROPOSED-CLOSED-FOR-REVIEW` and DR-118 carries
  `DECIDED-V1-NOT-INTEGRATED`; none of the three is moved by this entry, and
  each stays on the SATISFIED limb.
- **Amend D-001 clause 2.** Rejected: the clause already carries the deferral
  limb; nothing needs amending.

## Readiness effect

Condition 2 becomes **6 of 29 slice-affecting rows `SATISFIED`, with 3 of 32 on
the deferral limb**, and stays **NOT MET**. Zero rows become `SATISFIED`.
Condition 1 stays MET for architecture-preview scope. Condition 3 stays MET.
Condition 4 stays MET; `32 of 32 owners named` and `28 of 28 required gates` are
unchanged; required-now stays 28. Condition 5 remains NOT MET and last.

## Reversibility

C-D365 plus restore of the prior condition-2 "Measured now" text and the prior
one-sentence clause. Total: no row cell moves, so nothing depends on this edit.
Does not overturn D-001, D-002, D-010, D-056, D-133, D-135, D-363 or D-364.
Overturn: C-D365.

## Commit

C-D365.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORDINATOR-DECISIONS.md | `bbf72b3da812c10b6dd98073e6ce3539d5fb7c01c14d93a0ac322c38bf73ce62` |
| file 08 | `476cfe5650f98fa30a3620a0a206e9db8fdddbda124b3c1ac8da355eb0149510` |
| file 10 (MVP and future scope) | `5378cdbab2d7063fb485bea4b9f7133a92698566e3ec3bdae1e03da415298d18` |
| file 05 (V1→V2 relationship) | `1a57c9ca0f546358f5c241599be5dda4e425838ef432d63900c5ca0afec50852` |
| HEAD | `7c8a1c965152b094744e41bf86361a772315df97` |
| D-135 commit | `52ea851ea166439e48a5c0b81fcb9b9fc9daaffc` |
| D-363 commit | `7c8a1c965152b094744e41bf86361a772315df97` |
| D-364 commit | `d4e93724092d425ef00c24570fe50c451144f934` |

D-002 and D-010 predate the `D-NNN: …` commit-subject convention and carry no
such commit; both are pinned by their COORD headings, and COORD is pinned above.

If a cited file moves in a way that is not append-only COORD growth or COORD
heading hygiene, with file 08, file 10, file 05 and this draft unmoved,
re-measure before adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
