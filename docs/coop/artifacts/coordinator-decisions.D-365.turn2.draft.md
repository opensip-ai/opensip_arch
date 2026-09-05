# D-365 — Re-measure condition 2 over D-002's affected-row set as amended by D-134

> **Status:** DRAFT — under review.
> **Date:** 2026-09-02
> **Protocol:** D-000, turn 2 of 3. Turn 1 drew OBJECT from both independent
> reviewers on the same MUST-FIX. This turn lands every turn-1 identifier:
> **CODEX-D365-MF1**, **CLAUDE-D365-MF1**, **CLAUDE-D365-SF1**,
> **CLAUDE-D365-SF2**, **CLAUDE-D365-SF3**, **CLAUDE-D365-ADV-1**,
> **CLAUDE-D365-ADV-2**, **CLAUDE-D365-ADV-3**, **CLAUDE-D365-ADV-4**. Codex
> turn 1 returned `currentFindingIdentifiers` `["CODEX-D365-MF1"]`, an empty
> shouldFix list, an empty advisories list, an empty observations list and an
> empty observationsNotFindings list. Claude 2 turn 1 returned no
> `currentFindingIdentifiers` value. Each reviewer's file is described only as
> this cycle's own prompts and verdict files state it. The turn-1 subject
> `coordinator-decisions.D-365.draft.md`
> `93ae1670135e8a45f03f53da8cada144a257f5b894c7c5b0b8dab9d6ef845a7a` remains
> frozen and unrecorded.
> **Decision type:** RULE-GOVERNED. Re-measurement of the condition-2 snapshot
> against the adopted affected-row set, plus a D-001 MF-6 file-08 edit. This is
> coordinator decision **D-365**, not a register row.
> **Does not** mark any row `SATISFIED`, and does not change any row's lead label.
> **Does not** edit the status, acceptance-evidence or Blueprint-impact cell of
> any row.
> **Does not** amend D-002's affected-row set or D-134's cardinality, and does
> not move any row between the SATISFIED-requiring set and the deferral limb.
> **Does not** make condition 2 MET.
> **Does not** touch condition 4's `32 of 32 owners named`, which counts the 32
> release gates DR-G01..G32 and is unrelated to the decisions table.
> **Does not** change live required-now 28, and edits no gate-harness cell.
> **Does not** record an in-cell disposition for any deferral-limb row.
> **Does not** perform D-056 Eligibility gate 4 or gate 5 for any row.
> **Does not** amend D-000, D-001, D-002, D-010, D-056, D-133, D-134, D-135 or
> D-363. **Does not** authorize `docs/v2/implementation/`.

HEAD is `7c8a1c965152b094744e41bf86361a772315df97` (D-363 ADOPTED).
Last live heading is D-363. Required-now is 28.
Live file 08 is
`476cfe5650f98fa30a3620a0a206e9db8fdddbda124b3c1ac8da355eb0149510`.

## What turn 1 got wrong

Turn 1 proposed a qualifying set of 29 rows, reached by subtracting the three
rows whose own file-08 cells state they do not reach the first blueprint slice.
Both reviewers landed the same MUST-FIX: the qualifying set is not a cell-text
property the coordinator may derive. **It is an adopted object.** D-002 names
the condition-2 affected-row set; D-134 amends its cardinality to 23 and already
uses the term "deferral limb". Turn 1 cited neither, substituted a membership
rule found in no adopted text, and would have written a third number into file
08 matching neither the row total nor the adopted set — under a header
disclaiming any amendment of D-002.

Turn 2 measures the adopted set instead. The correction moves six further rows
onto the deferral limb, so the SATISFIED-requiring set is smaller than turn 1
claimed, not larger.

## The adopted set, from bytes

**D-002** (ADOPTED 2026-08-13) names the condition-2 affected-row set under this
slice: DR-101, DR-102, DR-103, DR-104, DR-105 (scoped), DR-107, DR-111, DR-112,
DR-114, DR-115, DR-117, DR-118 (TypeScript role), DR-119, DR-120, DR-121,
DR-122, DR-123, DR-124 (touched classes), DR-125, DR-126, DR-127 — **21 rows**.

The same entry records, under "Explicit deferrals (each gets its recorded
disposition, never silence)": DR-108, DR-110, DR-116, DR-128, DR-129, and
DR-106, DR-109, DR-113 "each deferred WHOLLY" — **eight rows**, alongside
non-row deferrals (Windows platform support; baseline/ratchet, conditional).

**D-134** (ADOPTED 2026-08-15), a scoped D-002 successor authorized by D-132
clause 3, decides: "D-002's SATISFIED-requiring affected-row set is the 21 rows
D-002 named plus **DR-131** and **DR-133** (cardinality 23). DR-128, DR-129, and
DR-130 remain on the deferral limb."

So the SATISFIED-requiring set is **23** and the deferral limb is **nine**:
DR-106, DR-108, DR-109, DR-110, DR-113, DR-116 (D-002), DR-128, DR-129 (D-002),
DR-130 (D-010 / C-D010). 23 + 9 = 32.

Measured from live file 08 lead labels, among the 23: **6** `SATISFIED`
(DR-102, DR-104, DR-115, DR-117, DR-119, DR-123), **14** `OPEN` (DR-101,
DR-103, DR-105, DR-111, DR-112, DR-114, DR-120, DR-121, DR-124, DR-125, DR-126,
DR-127, DR-131, DR-133), **1** `DECIDED-V1-NOT-INTEGRATED` (DR-118), **2**
`PROPOSED-CLOSED-FOR-REVIEW` (DR-107, DR-122); 6 + 14 + 1 + 2 = 23. All nine
deferral-limb rows carry the lead label `OPEN`; 14 + 9 = 23 `OPEN` across the
table, which is the count the live snapshot already reports.

Six of the nine — DR-106, DR-108, DR-109, DR-110, DR-113, DR-116 — carry no
in-cell disposition; their cells read bare `OPEN` or `OPEN / inherits hard
blockers`, and their dispositions live in D-002. D-002 requires each deferral to
get "its recorded disposition, never silence"; recording those six in-cell is a
separate MF-6 act with its own artifact and commit, and is **not performed
here**. This entry does not cure that silence by counting, and does not treat
the absence of an in-cell note as membership in the SATISFIED-requiring set.

## Decision

1. Record that condition 2's SATISFIED limb quantifies over **D-002's
   condition-2 affected-row set as amended by D-134 — 23 rows** — and that the
   remaining **nine** rows sit on D-001 clause 2's deferral limb with the
   dispositions D-002 and D-010 record.
2. Condition 2 remains **NOT MET**: of the 23, 6 are `SATISFIED` and 17 are not.
3. This entry moves no row between the two sets. Membership is D-002's as
   amended by D-134, and changing it requires a scoped D-002 successor of the
   D-132 clause 3 / D-134 form, which this entry is not.
4. **Exact file-08 edits, and no others:**
   - Replace this unique live text (occurs once):

```
**6 of 32 `SATISFIED`** — 23 `OPEN`, 1 `DECIDED-V1-NOT-INTEGRATED`, 2 `PROPOSED-CLOSED-FOR-REVIEW`.
```

     with

```
**6 of 23 SATISFIED-requiring rows `SATISFIED`; 9 of 32 on the deferral limb** — among the 23: 14 `OPEN`, 1 `DECIDED-V1-NOT-INTEGRATED`, 2 `PROPOSED-CLOSED-FOR-REVIEW`; 6 + 14 + 1 + 2 = 23. The SATISFIED-requiring set is D-002's condition-2 affected-row set as amended by D-134 (cardinality 23). The deferral limb is DR-106, DR-108, DR-109, DR-110, DR-113, DR-116, DR-128, DR-129 (D-002) and DR-130 (D-010 / C-D010); all nine keep the lead label `OPEN`, their cells are unedited, and 14 + 9 = 23 `OPEN` across the table. Six of the nine carry no in-cell disposition; theirs live in D-002 and their in-cell recording is a later MF-6.
```

   - In "What that means in one sentence", replace only this unique clause
     (occurs once):

```
condition 2 remains 6 of 32 SATISFIED
```

     with

```
condition 2 remains 6 of 23 SATISFIED-requiring rows SATISFIED, with 9 rows on the deferral limb
```

   - In the snapshot preamble, immediately after the condition-1 qualifying-set
     rule, insert this sentence so the condition-2 figures are regenerable
     (replace this unique live text, which occurs once):

```
disposed, with set-union deduplication if a future row has both.
```

     with

```
disposed, with set-union deduplication if a future row has both. Condition 2's
qualifying set is not a lead-label property: it is D-002's condition-2
affected-row set as amended by D-134 (23 rows). The remaining nine rows sit on
D-001 clause 2's deferral limb with the dispositions D-002 and D-010 record;
they keep their lead labels and are counted separately. Changing that membership
requires a scoped D-002 successor of the D-132 clause 3 / D-134 form.
```

5. Condition 2's "Required" cell already reads "Every slice-affecting V2 row
   `SATISFIED`" and is not edited. Condition 4's measured cell is not edited:
   its `32 of 32 owners named` counts the 32 release gates DR-G01..G32 (29
   `OPEN`, 3 `HARD-BLOCKED`), not the decisions table, and the shared number 32
   is a numeric coincidence.

## Alternatives

- **Leave the snapshot counting 32.** Rejected: the snapshot reports condition 2
  in one component while the clause has two limbs and the qualifying set is
  adopted at 23.
- **Turn 1's cell-self-declaration rule (29 and 3).** Rejected: it appears in no
  adopted text, contradicts D-002 and D-134, and would silently return six
  D-002 deferrals to the SATISFIED-requiring set. Adopting it would be a scope
  change requiring D-132-style authorization, which this entry does not hold.
- **Record the six missing in-cell dispositions in the same act.** Rejected:
  D-002 gives each its own artifact and commit; this entry is a snapshot
  re-measurement and performs no row-cell edit.
- **Treat the nine as `SATISFIED`.** Rejected: they are not, and the deferral
  limb does not ask them to be.
- **Amend D-001 clause 2.** Rejected: the clause already carries the deferral
  limb.

## Readiness effect

Condition 2 becomes **6 of 23 SATISFIED-requiring rows `SATISFIED`, with 9 of 32
on the deferral limb**, and stays **NOT MET**. Zero rows become `SATISFIED` and
no row changes set. Condition 1 stays MET for architecture-preview scope.
Condition 3 stays MET. Condition 4 stays MET; `32 of 32 owners named` and `28 of
28 required gates` are unchanged; required-now stays 28. Condition 5 remains NOT
MET and last.

## Reversibility

C-D365 plus restore of the prior condition-2 "Measured now" text, the prior
one-sentence clause, and the prior preamble paragraph. Total: no row cell moves.
Does not overturn D-001, D-002, D-010, D-056, D-133, D-134, D-135, D-363 or
D-364. Overturn: C-D365.

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
| coordinator-decisions.D-365.draft.md (turn 1, frozen, unrecorded) | `93ae1670135e8a45f03f53da8cada144a257f5b894c7c5b0b8dab9d6ef845a7a` |
| D-135 commit | `52ea851ea166439e48a5c0b81fcb9b9fc9daaffc` |
| D-363 commit | `7c8a1c965152b094744e41bf86361a772315df97` |
| D-364 commit | `d4e93724092d425ef00c24570fe50c451144f934` |

D-002, D-010 and D-134 predate or fall outside the `D-NNN: …` commit-subject
convention and carry no such commit; each is pinned by its COORD heading, and
COORD is pinned above. Quotations from D-002, D-134 and file 08 carry no
emphasis of this entry's own except where a quoted source itself carries it;
bold inside the D-134 quotation is D-134's.

If a cited file moves in a way that is not append-only COORD growth or COORD
heading hygiene, with file 08, file 10, file 05 and this draft unmoved,
re-measure before adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
