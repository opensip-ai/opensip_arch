# D-056 — Condition-2 SATISFIED versus qualification remainder

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Not a new
> cycle. Frozen turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. Scoped successor amendment
> to SATISFIED *evidence* for a named eligible class, and to
> D-015's SATISFIED-rejection for that class. Not a rider on
> any application. Not D-013 alternative (b): that alternative
> was coining `DESIGN-ACCEPTED`. This entry does not coin a
> token.
> **Does not** mark any row SATISFIED.
> **Does not** rewrite D-001's five checklist bullets.
> **Does not** edit file 08 in this entry (MF-6 later, per row).
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** coin `DESIGN-ACCEPTED` or any other file-08
> status token.

Turn-1 subject `coordinator-decisions.D-056.draft.md`
`d4b628f6c8b860c65e2d1ca3f063caeae090b2358e0f468fa1b29ced72bdae49`
held frozen. Claude 2 CONSENT, 0 MUST-FIX, 0 SHOULD-FIX. Codex
OBJECTIONS, 1 MUST-FIX ADV-D056-01, 0 SHOULD-FIX.

| ID | Sev | Disposition |
|---|---|---|
| ADV-D056-01 | MUST-FIX | ACCEPTED. Turn 1 claimed an evaluation rule that left D-001 and live row criteria unamended while authorizing later SATISFIED that excludes the execution D-015 and the DR-102 cell require. That is a successor amendment and must be recorded as one. This turn names the amendment, supersedes D-015's SATISFIED-rejection for the eligible class only, keeps D-015's design-contract recording, and extends reversibility to restore that rejection. |

D-084 is ADOPTED at `242dbe347cfeef9860a3c7fe1c85d749769c1715`.
Condition 1 is MET for architecture-preview scope only. This
entry does not overturn D-084 and does not move condition 1.

## Why this entry exists

File 08's SATISFIED legend: "exact acceptance evidence is linked
and independently reviewed." Condition 2 requires every
slice-affecting V2 row to be `SATISFIED`, or an explicit
deferral. Condition 4 requires named harnesses and forbids
unevidenced `QUALIFIED` / `DEMONSTRATED`. Condition 5 forbids
`docs/v2/implementation/` until 1, 2, and 4 hold.

D-013 recorded DR-103's design contract and refused `SATISFIED`
because the exact-byte corpus was unmet. D-015 did the same for
DR-102: the row stays OPEN until CC-1..CC-11 are *executed* by
a harness at DR-G21.

That last sentence, read as architecture SATISFIED evidence, is
a deadlock: execution is qualification (condition 4 / DR-012),
and condition 5 forbids product implementation until conditions
1–5 hold. Condition 2 cannot lawfully require execution that
condition 5 forbids.

The same deadlock exists for `DECIDED-V1-NOT-INTEGRATED` rows
whose leftover is only qualification measurement of
already-decided numbers or rules (DR-115 / D-006; DR-119 /
D-008; DR-123 / D-009).

Turn 1 tried to resolve that deadlock while saying D-001 and
the live cells were unamended. ADV-D056-01 is right: the
resolution *is* a successor amendment to SATISFIED evidence
and to D-015's SATISFIED-rejection. This turn records that
amendment.

D-013 alternative (b) was coining `DESIGN-ACCEPTED`. This
entry is not that decision. SATISFIED remains the only
architecture-satisfaction token.

D-070's two-axis snapshot is a condition-1 rule only. This
entry does not extend that algorithm to condition 2.

## What is superseded, and what stands

1. **Superseded, eligible class only.** D-015's clause that
   DR-102 "stays OPEN because the classes are specifications
   and no harness executes them" is superseded as a *bar to
   later SATISFIED* for a row that meets Eligibility below.
   The same supersession applies to any later sibling sentence
   of that form, including the live DR-102 cell's "not
   SATISFIED until the hostile-conformance classes are
   executed." Those sentences remain history and remain true
   as a description of qualification. They are no longer the
   governing SATISFIED rule for an eligible row.
2. **Stands.** D-015's recording of
   `control-protocol-contract.v2` as DR-102's accepted design
   contract. D-013's recording of
   `component-manifest-schemas.v2` as DR-103's accepted design
   contract. D-006 / D-008 / D-009 as the Class B decisions.
   D-001's five checklist bullets. File 08's SATISFIED legend
   for every row that is not in the eligible class.
3. **Not performed here.** No SATISFIED re-record. No file-08
   cell rewrite. The first SATISFIED re-record of an eligible
   row is a later own cycle and is the MF-6 act that removes
   the conflicting "until executed" sentence from that cell.

## Eligibility (narrow)

A later SATISFIED re-record of a slice-affecting architecture
row may use this amendment only when **all** of the following
are true of that row at the moment of that later cycle:

1. One of:
   - **Class A.** An independently accepted design contract
     exists at 0 blockers with application-grade acceptance and
     no express reservation (D-001 T2-02), recorded by a D-000
     entry; the row's lead label is `OPEN`.
   - **Class B.** The lead label is
     `DECIDED-V1-NOT-INTEGRATED` because a D-000 entry already
     recorded the product/architecture decision (D-006, D-008,
     D-009, or a later sibling of that form).
2. Every remaining acceptance-evidence member is **only**
   harness *execution*, fixture *execution*, or qualification
   *measurement*. Authoring of fixtures, schemas, successors,
   actor-joins, missing design, or still-UNDECIDED numbers is
   **not** a remainder this amendment may split.
3. Each such remainder is already named as a condition-4 /
   DR-G* obligation with an owner. Naming a harness identifier
   is not itself SATISFIED.
4. A dedicated later D-000 cycle plus independent
   SATISFIED-GRADE review of *that row* accepts the split and
   records SATISFIED under this amendment.
5. An MF-6 file-08 cell edit records SATISFIED and removes the
   cell's conflicting "until executed" / "until measured"
   SATISFIED-bar. This entry is not that edit.

## Motivating later candidates (not performed here)

| Row | Class | Why eligible *in kind* |
|---|---|---|
| DR-102 | A | D-015 accepted T2-02 contract; leftover is CC-1..CC-11 *execution* at DR-G21. |
| DR-115 | B | D-006 decided the numbers; leftover is MEASUREMENT at qualification. |
| DR-119 | B | D-008 accepted the rule; leftover is per-role closure *evidence* at DR-G14. |
| DR-123 | B | D-009 accepted the CLI baseline; leftover is evidence at DR-G01..G05/G12/G17. |

This entry still marks nothing SATISFIED. Each later own cycle
is required.

## Ineligible today (named, not exhaustive)

These rows are **not** made SATISFIED by this entry, and they
are **not** eligible for a later split under this amendment
until the named design leftover is closed:

| Row | Why ineligible today |
|---|---|
| DR-103 | Fixture *authoring* plus independent review remain. Authoring is design work (clause 6 below), not a C4 remainder. D-013's SATISFIED-refusal stands until that authoring exists. |
| DR-104 | Negative-test corpus authoring remains. This amendment is not that authoring. |
| DR-105 | v1 independently REJECTED. D-042 recorded v2 as a candidate, not as an accepted T2-02 contract. Actor-join / host-effect still design. |
| DR-114 | Design contract ACCEPTED (D-035). Actor-join remains design. Fixture-corpus execution is not the only leftover. |
| DR-118 | Per-row thresholds remain UNDECIDED. Undecided numbers are design. |
| DR-101 / 107 / 111 / 112 / 117 / 120 / 121 / 122 / 124 / 125 / 126 / 127 | No accepted T2-02 contract or DECIDED measurement-only leftover. |
| DR-106 / 108 / 109 / 110 / 113 / 116 / 128 / 129 / 130 | Deferral limb of condition 2 (D-002 / D-010), not this amendment. |

## Decision

1. **Scoped successor amendment, architecture-preview scope.**
   For a row that meets Eligibility above:
   - architecture SATISFIED may be recorded later only when
     Eligibility (1)–(5) all hold;
   - Execution, QUALIFIED, and DEMONSTRATED remain condition 4
     / DR-012. They are not architecture SATISFIED evidence.
   - File 08's SATISFIED legend is read, for those eligible
     rows only, as: the independently reviewed design contract
     or the already-recorded D-000 decision, plus the named
     C4/DR-G* remainder list. The execution of that remainder
     is not part of the architecture evidence set.
   - D-015's SATISFIED-rejection, and any live cell sentence
     that makes SATISFIED wait on that execution, is
     superseded for that row as stated under "What is
     superseded."
2. **This entry marks no row SATISFIED.** Each later SATISFIED
   re-record is its own D-000 cycle. Coordinator fiat remains
   unlawful (DR-204). Two authorities will not remain in
   conflict at the moment of that re-record: the re-record's
   MF-6 edit is what removes the cell-level bar.
3. **Does not rewrite D-001's five checklist bullets.**
   Condition 2 still requires SATISFIED or explicit deferral.
   This entry changes how SATISFIED is evidenced for the
   eligible class so condition 2 and condition 5 are not a
   deadlock. After this entry, condition 2 remains NOT MET.
   Zero SATISFIED is added.
4. **Does not rewrite live cells.** Those rewrites are later
   MF-6 acts, one row at a time, after Eligibility (4)–(5).
   Today's cells stay authoritative until that later edit.
   They are not a second live SATISFIED rule for an eligible
   row once that later edit lands.
5. **Authoring fixtures and harness *specifications* remains
   lawful design work now.** Execution remains qualification.
   DR-103's own schema already places fixture generation under
   DR-120 / DR-G15. That authoring must exist and be
   independently reviewed before DR-103 can become eligible.
6. **Deferred D-002 / D-010 items stay on the deferral limb.**
   This amendment is not a deferral and does not replace those
   dispositions. Later owner-recordings of those deferrals are
   separate cycles.
7. **No implementation authorization.** Condition 5 remains
   last.
8. **Does not extend D-070's two-axis algorithm to condition
   2.** Condition 2 continues to be counted from leading
   SATISFIED labels plus explicit deferral dispositions, not
   from this amendment existing.
9. **Does not coin `DESIGN-ACCEPTED`.** D-013 alternative (b)
   remains available as a later dedicated vocabulary decision
   and is not performed here.

### Alternatives

- Keep the DR-102 "until executed" SATISFIED sentence and wait
  for condition 5. Rejected: deadlock.
- Claim this is only an evaluation rule and leave D-015's
  SATISFIED-rejection live. Rejected: ADV-D056-01.
- Coin DESIGN-ACCEPTED. Rejected in this entry: D-006 NOTE-03 /
  D-013 (b); a later dedicated vocabulary decision may still
  do it.
- Mark DR-102/103/115 SATISFIED here. Rejected: DR-204; clause
  2; DR-103 is ineligible until fixtures are authored.
- Treat D-070's preview-note union as a condition-2 count.
  Rejected: D-070 is condition 1 only.
- Apply the split to any OPEN row with a design-contract note.
  Rejected: leftover authoring and actor-join are still
  design.
- Leave DECIDED-V1-NOT-INTEGRATED rows with no integration
  path. Rejected: same deadlock as DR-102, for the
  measurement-only leftovers.
- Include DR-118. Rejected: thresholds UNDECIDED.
- Use a condition-2 deferral of the execution remainder
  instead of amending SATISFIED evidence. Rejected for
  slice-affecting rows whose design contract is already the
  architecture outcome (DR-102 / D-015). Deferral would
  pretend the protocol surface is out of the preview. The
  honest successor is this SATISFIED-evidence amendment.

### Readiness effect

Zero at adoption. No SATISFIED. No blueprint. Condition 2
stays NOT MET. D-015's design-contract recording stands.
D-015's SATISFIED-rejection is superseded for the eligible
class only and has no SATISFIED effect until a later MF-6
re-record.

### Reversibility

Total before any dependent SATISFIED re-record. Overturn
restores D-015's SATISFIED-rejection as the governing
SATISFIED rule for DR-102, restores the live-cell
"until executed" / "until measured" bars as governing, and
restores the pre-amendment reading of the SATISFIED legend.
After a dependent SATISFIED re-record lands, overturn also
requires that re-record's supersession. Overturn: C-D056.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORD | `eec2f96601cc182783ae07cb53ac3bcdc2fb29e917938699ec5de50c3faa97b0` |
| file 08 | `ff2ebaddc782443a5c5a88590bd77d340ac6caf30ed788977221225f4838a811` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| claim-register.v1.json | `767dc210d4fa8b6d2588a6746df124192ff19af9da4e7be663164e9fde32d59c` |
| D-084 commit | `242dbe347cfeef9860a3c7fe1c85d749769c1715` |
| D-070 commit | `e40b3f190e68264a24ac5098b1cef300434d6709` |
| turn-1 subject | `d4b628f6c8b860c65e2d1ca3f063caeae090b2358e0f468fa1b29ced72bdae49` |
| Claude 2 turn 1 | `59b3f0fa8b40f584a729760d78e3900da934478214b96ef062129fd20b390c52` |
| Codex turn 1 | `c1609c5436e2649593b7ef9d78238ef2ca4c209fa5247fa0d51baf4d7febbfba` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.
