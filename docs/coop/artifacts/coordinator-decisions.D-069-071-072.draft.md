# D-069 / D-071 / D-072 — Select Route B for DR-006, DR-007, DR-009

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a fourth turn of
> CONTESTED D-051 / D-052 / D-053.
> **Decision type:** PREFERENCE-LADEN. Three severable entries.
> Same form as adopted D-028 / D-029 / D-030 / D-047 / D-048.
> **Does not** write dispositions. **Does not** mark SATISFIED.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit file 08.

D-051 / D-052 / D-053 are CONTESTED (commit
`11a4e6998b48b762d46e313a470431ff68236db8`). This is a new cycle
for the same three selections. Decision merits passed on Claude's
side. Process ledger ADV-D051-053-T3-01 did not pass on Codex's
side.

The unadopted `coordinator-decisions.D-059-063.draft.md` five-entry
owner-recording draft is not this cycle and is not adopted here.
D-070 is ADOPTED at commit `e40b3f190e68264a24ac5098b1cef300434d6709`
(file-08 MF-6 notes; two-axis snapshot). It is not this file. These
entries do not adopt or overturn D-070. D-070's condition-1 row
still names DR-006, DR-007, and DR-009 as remaining without
SATISFIED or scoped owner-recorded disposition. This cycle selects
Route B for those three rows; it does not owner-record them.

## Predecessor ledger (CONTESTED D-051 / D-052 / D-053)

| Turn | Kind | Path | sha256 | Counts |
|---|---|---|---|---|
| 1 | subject | `coordinator-decisions.D-051-053.draft.md` | `080a3c203134787195e76ed73e5c14515282ee9e3dd6afaae4fa4d80ff2a4aa5` | — |
| 1 | prompt | `coordinator-decisions.D-051-053.review-prompt.md` | `9484351c428e8515085ad274238f03decf707830fcd254f94dbd532783f03899` | — |
| 1 | Claude 2 | `coordinator-decisions.D-051-053.review-adversarial.claude2.json` | `62ff5a3fcf0b7a21449772eb92359721a0bae449bc37fe04c1e385a7daa7caaa` | OBJECT; 0 MUST-FIX; 1 SHOULD-FIX C2-D051-053-SF1; 3 notes |
| 1 | Codex | `coordinator-decisions.D-051-053.review-adversarial.codex.json` | `2e4f590dd88d139fcae6cd7cec81eb6e96be8506949b7cb5062a2eb419621e6d` | CONSENT; 0 MUST-FIX; 0 SHOULD-FIX; 1 note |
| 2 | subject | `coordinator-decisions.D-051-053.turn2.draft.md` | `5a03fe666630015917c79e1b76406c2b8e54989a19ad98933983659204d62496` | — |
| 2 | prompt | `coordinator-decisions.D-051-053.turn2.review-prompt.md` | `f1bbc834dd9baec74920ff3972c904ea95c8aefa447b77ee10afdd8a7508cdbc` | — |
| 2 | Claude 2 | `coordinator-decisions.D-051-053.review-adversarial.claude2.turn2.json` | `e7da77e496b63ae1ddf06b228c979df9ab6d363973a4dbbcccf686f51fbafdd5` | OBJECT; 0 MUST-FIX; 1 SHOULD-FIX C2-D051-053-T2-SF1; 3 notes |
| 2 | Codex | `coordinator-decisions.D-051-053.review-adversarial.codex.turn2.json` | `daeb12878962ab8d5b94113453e544fe8415abc231eed027acb3bbb189523140` | OBJECTIONS; 0 MUST-FIX; 1 SHOULD-FIX ADV-D051-053-T2-01 |
| 3 | subject | `coordinator-decisions.D-051-053.turn3.draft.md` | `231abf8ae41a3cde92861d1e270486d65e72c932be5491d6bf5bccb9cde40940` | — |
| 3 | prompt | `coordinator-decisions.D-051-053.turn3.review-prompt.md` | `a405d89a4c4331e4a9c0bba931a0e9fa0e6e88f8136dc367c3f6d07ca09690f3` | — |
| 3 | Claude 2 | `coordinator-decisions.D-051-053.review-adversarial.claude2.turn3.json` | `fb386ef598fb970c168d1270bcdd3029b177d7de5f131be40375dfb8b25a31ad` | CONSENT; 0 MUST-FIX; 0 SHOULD-FIX; 2 notes |
| 3 | Codex | `coordinator-decisions.D-051-053.review-adversarial.codex.turn3.json` | `9826b2a8b2be5567a5567669ce2a23972ed7ce18b8d803a8df154d8fabef0fb4` | OBJECTIONS; 0 MUST-FIX; 1 SHOULD-FIX ADV-D051-053-T3-01 |

CONTESTED register: COORD `D-051 / D-052 / D-053` at commit
`11a4e6998b48b762d46e313a470431ff68236db8`.

## Finding dispositions

| ID | Sev | Raised | Disposition |
|---|---|---|---|
| C2-D051-053-SF1 | SHOULD-FIX | Claude 2 turn 1 | ACCEPTED. Status is under review once dispatched. |
| C2-D051-053-T2-SF1 | SHOULD-FIX | Claude 2 turn 2 | ACCEPTED. Protocol identifies the actual turn of this file. |
| ADV-D051-053-T2-01 | SHOULD-FIX | Codex turn 2 | ACCEPTED in full. Two parts: (1) title/path/Protocol name the actual turn; (2) hash-pinned predecessor subjects plus both reviewers' verdict paths/digests/counts. This new-cycle subject is turn 1, not turn 4. The ledger above is part 2. |
| ADV-D051-053-T3-01 | SHOULD-FIX | Codex turn 3 | ACCEPTED. Same two-part repair, now present in this new subject. Do not edit the frozen D-051-053 turn-3 subject. |

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORD | `4220481f9de1920bcc02a5b7bfe050e28e87f161e9665c7d62dde6b9f0c141fe` |
| file 08 | `9495c70f96936c4d33fcaf8e8a395c59a44ad2b7203af38be7f0ac2b62dc2dfd` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| claim-register.v1.json | `767dc210d4fa8b6d2588a6746df124192ff19af9da4e7be663164e9fde32d59c` |
| D-070 commit | `e40b3f190e68264a24ac5098b1cef300434d6709` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

These three rows remain the inherited V1 prerequisites with no
adopted Route B selection. DR-002/003/004/005/008 already have
preview Route B selections and owner recordings (D-058, D-065,
D-064, D-060, D-061). DR-001 is SATISFIED. DR-010 is Route C with
DR-117 and is owner-recorded at preview scope by D-068. DR-011
residuals follow their owning surfaces; D-055 remains a separate
undispatched selection draft.

D-002 already named the consequence of scoped disposition on these
rows: if a named condition-1 closure lands by scoped disposition
rather than binding recipes, the dependent feature ships reduced,
re-scoped, or waits. This draft selects that path for preview
scope only. It does not hide the rides.

## D-069 — Select Route B for DR-006 (preview scope)

- **Subject:** DR-006 only.
- **Owning V1 authority (file 08):** Each identity-owning V1 surface +
  FACT-PLANE/evidence authorities + coordinator.

### Decision

1. Select Route B for DR-006, architecture preview only.
2. This selection is one row. It does not select DR-002, DR-003,
   DR-004, DR-005, DR-007, DR-008, DR-009, DR-010, or DR-011.
3. Preview-scoped. Binding per-surface identity recipes remain owed
   on the authoritative path. EIR v12 is the applied lineage head
   (D-003). Application of a head is not binding recipes and is not
   SATISFIED of this row.
4. **Named D-002 rides, if this selection is later owner-recorded.**
   These features do not survive on prose:
   - SARIF for `analyze` drops from the preview (RunId and Finding
     fingerprint stay conceptual).
   - Rebuildable cache/index keys stay conceptual. The class may
     still exist; its identity recipe may not be designed as settled.
   - Coverage on the TypeScript provider dispatch path stays
     conceptual (`subjectScopeCommitment`).
   - PlanId for the TypeScript role stays conceptual
     (`typescriptStdlibMerkleRoot` has no producing rule).
5. Coordinator selects. Named owners record. Coordinator may draft
   disposition bytes. D-000 does not make the coordinator those
   identity-owning surfaces. Independent review is required. A
   coordinator-composed SATISFIED is unlawful (DR-204).
6. Writes no disposition. Marks nothing SATISFIED. Authorizes no
   blueprint. A completed, reviewed, owner-recorded disposition may
   discharge condition 1 for DR-006 within the scope it names.
   Conditions 2–5 remain. Condition 5 remains the only
   implementation authorization.

### Alternatives

- Leave on full Route A (binding recipes before preview). Reachable;
  rejected for preview scope only. D-002 already chose honesty about
  the park over early CI leverage.
- Select Route B and keep SARIF / Coverage / PlanId / cache-key
  recipes as if settled. Rejected: D-002 T2-04 symmetry.

### Readiness effect

Zero at adoption.

### Reversibility

Total before any dependent disposition lands. After one lands,
overturn also requires that disposition's owning-authority
supersession. Overturn: C-D069.

## D-071 — Select Route B for DR-007 (preview scope)

- **Subject:** DR-007 only.
- **Owning V1 authority (file 08):** D9 authority + evidence/retention
  owner.

### Decision

1. Select Route B for DR-007, architecture preview only.
2. This selection is one row. It does not select DR-002, DR-003,
   DR-004, DR-005, DR-006, DR-008, DR-009, DR-010, or DR-011.
3. Preview-scoped. The D9 successor closing observation→faultCause,
   optional presence, success/policy/interrupted branch, and
   retention-loss integration remains owed on the authoritative
   path. `d9-exit-contract.v1.14` stays the live contract. This
   entry invents no D9 code.
4. **Named D-002 rides, if this selection is later owner-recorded.**
   Doctor's D9 mapping (DR-114) and containment goldens (DR-G21)
   that need the observation→faultCause successor ship reduced,
   re-scoped, or wait. Preview may still emit a D9 exit (D-018)
   using v1.14 without those closures.
5. Coordinator selects. Named owners record. Coordinator may draft.
   D-000 does not make the coordinator the D9 authority. Independent
   review is required. A coordinator-composed SATISFIED is unlawful
   (DR-204).
6. Writes no disposition. Marks nothing SATISFIED. Authorizes no
   blueprint. A completed, reviewed, owner-recorded disposition may
   discharge condition 1 for DR-007 within the scope it names.
   Conditions 2–5 remain. Condition 5 remains the only
   implementation authorization.

### Alternatives

- Leave on full Route A. Reachable; rejected for preview scope only.
- Invent preview D9 codes for retention loss or observation→faultCause.
  Rejected: file 08 and D-002 both forbid inventing those codes.

### Readiness effect

Zero at adoption.

### Reversibility

Total before any dependent disposition lands. After one lands,
overturn also requires that disposition's owning-authority
supersession. Overturn: C-D071.

## D-072 — Select Route B for DR-009 (preview scope)

- **Subject:** DR-009 only.
- **Owning V1 authority (file 08):** R-1/evidence authorities.

### Decision

1. Select Route B for DR-009, architecture preview only.
2. This selection is one row. It does not select DR-002, DR-003,
   DR-004, DR-005, DR-006, DR-007, DR-008, DR-010, or DR-011.
3. Preview-scoped. One-shot/no-reuse remains preserved. `LN-13`,
   `policyOutcome.derivationDigest`, and `R1-PARK-*` stay parked.
   Identity-dependent implementation waits. r1 v1.9 is the applied
   lineage head (D-005). Application of a head is not park closure
   and is not SATISFIED of this row. DR-204 already ruled the
   dialect-repair date anomaly CLEAN for reliance; this entry does
   not re-open that adjudication.
4. Coordinator selects. Named owners record. Coordinator may draft.
   D-000 does not make the coordinator the R-1 authority.
   Independent review is required. A coordinator-composed SATISFIED
   is unlawful (DR-204).
5. Writes no disposition. Marks nothing SATISFIED. Authorizes no
   blueprint. A completed, reviewed, owner-recorded disposition may
   discharge condition 1 for DR-009 within the scope it names.
   Conditions 2–5 remain. Condition 5 remains the only
   implementation authorization.

### Alternatives

- Leave on full Route A. Reachable; rejected for preview scope only.
- Treat applied r1 v1.9 as SATISFIED of LN-13 / derivationDigest /
  R1-PARK. Rejected: D-005 closed application of the head, not the
  parks.

### Readiness effect

Zero at adoption.

### Reversibility

Total before any dependent disposition lands. After one lands,
overturn also requires that disposition's owning-authority
supersession. Overturn: C-D072.
