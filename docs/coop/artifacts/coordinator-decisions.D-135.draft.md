# D-135 — File 08 MF-6: add DR-131 and DR-133 as OPEN

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. File-08 content change
> (D-001 MF-6) authorized by D-132 clause 4 and sequenced
> after adopted D-134. Does not mark SATISFIED.
> **Does not** mark any row SATISFIED.
> **Does not** rewrite D-001's five checklist bullets.
> **Does not** name DR-131 or DR-133 eligible in kind today
> (D-133: no contract yet).
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** add DR-132, DR-134, or DR-135 as register rows.
> **Does not** edit the COORD D-056 Decision paragraph (that
> annotation is D-133's owed later hygiene act, a separate
> cycle).
> This is coordinator decision **D-135**, not a register row.

D-132 is ADOPTED at `d3efe3c53539f4aadd7e3f3adbf6dec2de15cecd`.
D-133 is ADOPTED at `5b6f7232c66d72ae8385f709cf95b9e493c2af59`.
D-134 is ADOPTED at `d3a3b744a7b90619d381aea1efec864e430def72`.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORDINATOR-DECISIONS.md | `de5a4b3806dff919bcc5cf9637a8c254eda3b123b04f9e9f14347b82493c5d57` |
| docs/v2/architecture/08-decision-and-readiness-register.md | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |
| docs/v2/architecture/12-architecture-completion-goal.md | `a2de0b4c4a104837b0f7a5731073d039778b30ef182e1faac815a14cd2c55e92` |
| D-134 commit | `d3a3b744a7b90619d381aea1efec864e430def72` |

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

D-134 named DR-131 and DR-133 as members of D-002's
SATISFIED-requiring set (cardinality 23). They do not yet
exist as file-08 cells. D-001 SF-3 evaluates condition 2 over
the register as it stands. D-132 clause 4 authorizes an MF-6
edit that adds those two rows as `OPEN` and re-measures the
snapshot (4 of 30 → 4 of 32). This entry is that edit. It
does not SATISFY either row.

## Decision

1. **Insert exactly two new rows** into the V2 architecture
   and product decisions table, immediately after the DR-130
   row and immediately before the heading
   `## Five-review findings and dispositions`. The two rows
   are the exact markdown lines in §Exact new rows below.
   Do not insert any other row.
2. **Lead status of both new rows is `OPEN`.** Neither is
   SATISFIED, DECIDED-V1-NOT-INTEGRATED, or
   PROPOSED-CLOSED-FOR-REVIEW. D-133 remains: they are not
   eligible in kind today.
3. **Rewrite only these snapshot sentences**, leaving the
   snapshot heading date `2026-08-14` unchanged:
   - Condition 2 "Measured now" cell: replace
     `**4 of 30 \`SATISFIED\`** — 22 \`OPEN\`` with
     `**4 of 32 \`SATISFIED\`** — 24 \`OPEN\`` and append
     one clause: `DR-131 and DR-133 added OPEN by D-135;
     neither is eligible in kind today (D-133).`
   - The one-sentence "What that means" paragraph: replace
     `condition 2 remains 4 of 30 SATISFIED` with
     `condition 2 remains 4 of 32 SATISFIED`.
   Do not change conditions 1, 3, 4, or 5 measured cells.
   Do not change condition 2 standing (`NOT MET`).
4. **Do not rewrite D-001's five checklist bullets.**
   Condition 2 remains range-free (D-010). Adding two table
   rows grows the quantifier by SF-3.
5. **This entry marks no row SATISFIED.** No D-056 Class A
   opening. No implementation authorization.
6. **Does not mint a D-096 (A) grant.**
7. **Does not annotate the live COORD D-056 Decision
   paragraph.** That remains D-133 owed later work.

## Exact new rows

Insert these two lines, in this order, as table rows. Each is
one markdown table row.

DR-131:

`| DR-131 | Preview non-authoritative \`analyze\` product contract | Product + CLI / output | D-132; D-134; recorded goal [file 12 §3](12-architecture-completion-goal.md) (file 12 has no authority) | Independently reviewed contract that freezes: single first-party bundled declarative pack name/version; sealed facts+Coverage inputs; PlanId membership of the pack; core-evaluated \`policyOutcome\`; typed-indeterminate on a missing required rung; which preview identities are unstable; upgrade path to a sealed Run; citation of D-077 / D-078. The cell excludes human/machine JSON schema and exit generics already SATISFIED at DR-123 (D-092). | **OPEN** — no contract exists. Not eligible in kind today (D-133). Not SATISFIED. | Hard blocker for preview \`analyze\`; condition 2 SATISFIED-requiring per D-134 |`

DR-133:

`| DR-133 | Provider-only TypeScript component output | Semantic / component architecture | D-132; D-134; recorded goal [file 12 §4](12-architecture-completion-goal.md) (file 12 has no authority) | Independently reviewed contract stating: the TypeScript component returns semantic facts and Coverage only; the host owns rules, policy, findings, and admission; component-emitted findings are refused, with retained negative tests. | **OPEN** — no contract exists. Not eligible in kind today (D-133). Not SATISFIED. | Hard blocker for preview \`analyze\`; condition 2 SATISFIED-requiring per D-134 |`

## Arithmetic (measured, not a definition)

Before this edit the V2 decisions table has 30 rows
(DR-101–DR-130): 4 SATISFIED, 22 OPEN, 2
DECIDED-V1-NOT-INTEGRATED, 2 PROPOSED-CLOSED-FOR-REVIEW.
After this edit it has 32 rows: 4 SATISFIED, 24 OPEN, 2
DECIDED-V1-NOT-INTEGRATED, 2 PROPOSED-CLOSED-FOR-REVIEW.
D-134's SATISFIED-requiring set remains 23 (the 21 D-002
named rows plus DR-131 and DR-133). The snapshot denominator
is the whole table (32), matching the pre-edit convention
(30 = DR-101–DR-130).

### Alternatives

- SATISFY either row here. Rejected: no contract; D-133; DR-204.
- Add DR-132 / 134 / 135. Rejected: D-132 / file 12 / D-134.
- Edit file 08 without a D-000 cycle. Rejected: D-001 MF-6;
  D-037 clause 3.
- Annotate COORD D-056 in this same entry. Rejected: D-133
  named that as a separate hygiene cycle; mixing it here
  would hide a COORD edit inside an MF-6 file-08 act.
- Authorize `docs/v2/implementation/`. Rejected: condition 5.

### Readiness effect

Condition 2 stays NOT MET. Snapshot becomes 4 of 32
SATISFIED. Zero SATISFIED added. Condition 5 last.

### Reversibility

Total. Overturn: C-D135, plus restore of the two inserted
rows and of the two snapshot sentences. Does not overturn
D-132, D-133, or D-134.
