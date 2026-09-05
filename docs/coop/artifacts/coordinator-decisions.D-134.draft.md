# D-134 — Scoped D-002 successor: add DR-131 and DR-133 to the condition-2 affected-row set

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Scoped D-002 successor
> required by D-018 §2. Amends only D-002's condition-2
> affected-row set. PREFERENCE-LADEN only in that D-132
> already selected those two future rows; this entry does not
> re-select the slice.
> **Does not** mark any row SATISFIED.
> **Does not** rewrite D-001's five checklist bullets.
> **Does not** edit file 08 in this entry (MF-6 is a later own
> cycle).
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** change D-002 commands, platforms, deferrals, or
> identity rides.
> This is coordinator decision **D-134**, not a register row.

D-132 is ADOPTED at `d3efe3c53539f4aadd7e3f3adbf6dec2de15cecd`.
D-133 is ADOPTED at `5b6f7232c66d72ae8385f709cf95b9e493c2af59`.
D-002 remains ADOPTED. D-018 remains ADOPTED.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORDINATOR-DECISIONS.md | `b4a5c2192450e1be9bb02610ac9ac3e2c88d578e7fe42b16f78854ee9aa13e7a` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |
| docs/v2/architecture/12-architecture-completion-goal.md | `a2de0b4c4a104837b0f7a5731073d039778b30ef182e1faac815a14cd2c55e92` |
| D-132 commit | `d3efe3c53539f4aadd7e3f3adbf6dec2de15cecd` |
| D-133 commit | `5b6f7232c66d72ae8385f709cf95b9e493c2af59` |

If a cited file moves in a way that is not append-only COORD
growth with file 08, file 12, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.
"File 12" means only
`docs/v2/architecture/12-architecture-completion-goal.md`.

## Why this entry exists

D-018 §2: changing D-002's command set, language-role set,
platform set, deferral set, identity-dependency rides,
condition-2 affected-row set, or condition-4 required-gate
set is a scoped D-002 successor with its own D-000 review.

D-132 / file 12 select two future file-08 rows, DR-131
(preview analyze contract) and DR-133 (provider-only output).
D-001 SF-3: condition 2's quantifier is evaluated over the
register as it stands; adding a row is a reviewed decision.
D-037 clause 3: the file-08 edit is not its own route.

This entry performs only the D-002-set half. It does not
create the rows. Creating them is a later MF-6 cycle.

## What is superseded, and what stands

1. **Superseded.** D-002's adopted condition-2 affected-row
   set, only as the list of rows that set names. The
   historical D-002 recital remains history.
2. **Stands, unchanged.**
   - D-002 commands (`analyze`, `doctor`, help/version).
   - D-002 language role (TypeScript only).
   - D-002 platforms (macOS arm64/x86_64, Linux
     x86_64/arm64; Windows deferred).
   - D-002 deferrals (DR-106, 108, 109, 110, 113, 116, 128,
     129, 130, Windows, baseline/ratchet as written).
   - D-002 identity-dependency rides.
   - D-002 condition-4 required-gate set.
   - D-010's range-free condition-2 wording and DR-128 / 129 /
     130 membership.
   - D-018 naming (architecture preview).
   - D-133 (eligibility property).
   - File 08 as of `1cdcf9d4…` (no rows added here).
3. **Not performed here.** No file-08 row. No SATISFIED. No
   D-056 Class A opening. No implementation authorization.

## Decision

1. **Add only DR-131 and DR-133** to D-002's condition-2
   affected-row set. After this entry that set is the adopted
   D-002/D-010 set plus DR-131 and DR-133.
2. **Do not add any other row**, including DR-132, DR-134, or
   DR-135. File 12 rejected those as register rows.
3. **Do not create the file-08 rows here.** A later MF-6 act
   adds DR-131 and DR-133 as `OPEN`. Until that act, they are
   named future rows, not live file-08 cells. Condition 2's
   live count stays 4 of 30. The snapshot is not rewritten
   here.
4. **This entry marks no row SATISFIED.** DR-131 and DR-133
   are not eligible in kind today (D-133).
5. **No implementation authorization.** Condition 5 last.
6. **Does not mint a D-096 (A) grant.**

### Alternatives

- Edit file 08 in this same entry. Rejected: D-037 clause 3;
  file 12 §6.4; MF-6 is a later own cycle.
- Add DR-132 / DR-134 / DR-135. Rejected: three-agent repair
  recorded in D-132 / file 12.
- Change platforms or drop independent-release. Rejected:
  user kept D-002 as adopted.
- Mark DR-131/133 SATISFIED. Rejected: no contract; D-133.

### Readiness effect

Zero. Condition 2 stays 4 of 30. Condition 5 last.

### Reversibility

Total before the later MF-6 row-adding act. Overturn restores
D-002's pre-D-134 affected-row set. Overturn: C-D134. After
the MF-6 act lands, overturn also requires that act's
supersession.
