# C5 — DR-121 / monorepo CI encodings: what remains after D-293

Measured at HEAD `f3456575071928022a1f0e3a77e531a87157b365` (last COORD heading `## D-294`).
file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; COORD
`31746810f9be78f697d66eb94d9cd50a95a51218998f97a154596363039fb9b6`;
`DECISION-PACKETS/C5-9-reserved-encodings-owners-units.md` `735720d9f4df7bba5717f78bb558f378edb9f825971cb60b20ed8cdf07a58e2b`.

---

## 1. What D-293 already decided, and what remains

**COORD `## D-293`, Decision item 7, C5/C6 sentence (verbatim, COORD lines 16249–16253):**

> `7. **C5–C9.** C5/C6: reviewed architecture-scope acts classify the`
> `   reserved encodings; no concrete encoding becomes post-Condition-5`
> `   work without an express scope/eligibility successor and a`
> `   successor-join remeasurement; live file 04's "same-filesystem`
> `   atomic rename or a reviewed equivalent" rule stands.`

The adopted C5 detail (`DECISIONS-RECOMMENDED.md` `42f27394…` §C5–C9, Claude round 2, verbatim):

> `- **C5 DR-121:** a reviewed DR-121 architecture-scope act classifies the six `reservedForBlueprint` members as implementation encodings (ownership record stays the impact authority); concrete encodings move after Condition 5 only if a scoped D-056/Condition-2 successor expressly accepts that classification and a successor join remeasures; until then `OBL-CI-ENCODING-RESERVED` stays leftoverDesign true.`

Codex round 2 (AGREE), verbatim: `For C5 and C6, classify the reserved encodings through reviewed
architecture-scope acts and require an express scope/eligibility successor plus successor-join remeasurement
before treating any concrete encoding as post-Condition-5 implementation work`.

| Limb | Remaining record act |
|---|---|
| **(a) a reviewed DR-121 architecture-scope act classifying the six members as implementation encodings** | **One act.** D-293 authorizes it and states its content; nothing further is needed from the owner |
| **(b) an express scope/eligibility successor + successor-join remeasurement** | **Conditional, not now.** D-293 makes it the *precondition* for a later move, not an act it authorizes; and it would touch D-056/Condition-2 eligibility, which D-293 expressly does not (`It does not amend D-000 or D-056.`) |
| **(c) `OBL-CI-ENCODING-RESERVED` stays leftoverDesign true** | **No act.** It already is |

---

## 2. Current artifacts

### 2.1 File 08 row (line 303, verbatim)

> `| DR-121 | Monorepo isolated component CI and independent release qualification | Release engineering + component owners + core/protocol/integration owners | [Monorepo CI model](02-distribution-and-components.md#monorepo-ci-and-independent-component-releases); DR-103/111/118/120 | Ownership/dependency selection model; per-component relevant-platform lane contract for build/test/package/sign/attest/SBOM/quality; shared-core lane; cross-component protocol/authority/lock/offline/bundle gates; change-impact and missed-dependency negative tests; independent release evidence | OPEN | Hard blocker for release architecture; does not require separate repositories or lockstep versions |`

Owner cell: `Release engineering + component owners + core/protocol/integration owners`.
Gate row **DR-G16** (line 352), owner cell: `Release engineering + component/core/protocol/integration owners
(owner cell made concrete 2026-08-13, C4)`; status `OPEN`.

### 2.2 The contract carrying the reservation

`docs/coop/artifacts/monorepo-ci-contract.v16.json` — sha256
`67ca501660a2ba515ce37adc799c5418e4ffd156308189662245e5a5e45a2ddb`; `$.status` = `"CANDIDATE-NOT-APPLIED"`,
`$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`, `$.binds` = `"NOTHING"`; recorded at **`## D-124`**
(the C5–C9 packet §C5 constraint 6 quotes D-124: `DR-121's leftover T2-02 successor candidate … The candidate
binds NOTHING. D-056 Class A is not opened.`).

```
$.reservedForBlueprint = ["CI provider", "YAML", "repository path filters", "caches", "commands", "implementation tooling"]
$.selector.authority = "The ownership record is the only impact authority. It includes: unit→owner maps, shared-surface→consumer-component edges, multiComponentSharedLaneSelection, roleApplicability (custodied DR-118 component→role map), validated platform sets, and the previous/current comparison basis. …"
$.selector.ownershipRecord.standing = "AUTHORITATIVE committed design record. Not CI YAML. Not a path-filter table as authority."
$.selector.ownershipRecord.unitIdentity = "… Concrete path encoding is reserved for the later blueprint; …"
```

### 2.3 The current DR-121 leftover-join and the obligation

`docs/coop/artifacts/monorepo-leftover-join.v4.json` — sha256
`03d4478c3ce6ea843f8a4ee3ea1dcc6d8c06bd661f71970fe836ce107b611481`; `$.version` = `4`; `$.date` = `"2026-08-24"`;
`$.status` = `"CANDIDATE-NOT-APPLIED"`; `$.registerRow` = `"DR-121"`; `$.file08StatusToken` = `"OPEN"`;
`$.head` = `"456a5285fd44a4fed720c39fe3dd82ce0e6ccadb"`; `$.file08Pin.sha256` = `e503b75b…` (**live**).
Recording heading: **`## D-277 — Record monorepo leftover-join.v4 as DR-121 leftover remasurement`**
(`ADOPTED 2026-08-24`; Stage A dual ACCEPT 0/0; Stage B dual CONSENT 0/0).

`$.summary` (verbatim, in part): `"leftoverDesign": ["OBL-G16-FX-AUTHORING", "OBL-CI-ENCODING-RESERVED"]`,
`"deferredOrRidesElsewhere": ["OBL-WINDOWS", "OBL-EE-7E", "OBL-HOSTILE-GOLDENS", "OBL-G13"]`,
`"requiredNowUnchanged": 28`, `"ciEncodingInvented": false`, `"classAOpened": false`.

The obligation to remeasure, verbatim (`$.obligations[5]`):

```
{
 "id": "OBL-CI-ENCODING-RESERVED",
 "leftoverDesign": true,
 "existingGate": "none",
 "executionObligationOwnerToday": "none",
 "rideStanding": "not-capable-of-riding",
 "reason": "v16 reservedForBlueprint is CI provider, YAML, repository path filters, caches, commands, implementation tooling. G16 occupancy does not choose those encodings. Undecided encodings are leftover-design (D-056). This join does not invent them. g16 leftover-join.v4 does not steal OBL-CI-ENCODING-RESERVED. This join does not close it."
}
```

`$.reservedForBlueprintVerbatim` = the same six members.
`$.proposedLaterWork[2]` = `A later implementation successor may choose a CI provider, YAML, path filter, cache,
command, or tooling. That successor must still prove the live file 02 properties. This join chooses none.`

---

## 3. Precedent

### 3.1 There is no recorded "architecture-scope act" of exactly this shape

A search of COORD for the record's own deferral-disposition language finds two shapes, both of which wrote into
file 08 (the C1–C4 packet §0.2 measured this):

- **Row-level:** file 08 row **DR-130** status cell: `OPEN — slice 1 claims no upgrade continuity and its
  deferral disposition is RECORDED HERE (D-010, C-D010): DR-130 does not affect the first blueprint slice`.
  The act was **`## D-010`** — a `RULE-GOVERNED register-content change` that added the row and its disposition
  in one cycle.
- **Number-level inside a slice-affecting row:** file 08 row **DR-G05**, Threshold/waiver cell:
  `measurement mandatory, caps deferred by explicit disposition (D-006)`; the disposition itself is
  **`## D-006`** Decision clause 5 (`caps become product decisions at the first component-acceptance decision
  under DR-G05's own evidence column. **Trigger defined (turn-1 SF-1):** …`).

**Neither is a sub-row scope classification recorded in COORD alone.** The nearest COORD-only decision shape is
**`## D-294`** itself: subject = `docs/coop/artifacts/coordinator-decisions.D-294.turn3.draft.md`
`9be8f7db1dc9b6c1137c899ccfffbbd9d769ff3c25869526721cb40022fd5f05`, no artifact successor, `RULE-GOVERNED`,
three turns to CONSENT. That is the template this act should follow.

### 3.2 What reviewers attacked at D-294 (the closest same-class cycle)

**`## D-294`** Status, verbatim: `turn-1 Claude 2 OBJECT (CLAUDE-D294-SF1, CLAUDE-D294-SF2, CLAUDE-D294-SF3;
`6066dc92448268d0ee75eca1390399aa9bfb0b8aa09a12cde14b2ead22fb9e92`); turn-1 Codex OBJECT (CODEX-D294-MF1,
CODEX-D294-MF2, CODEX-D294-SF1, CODEX-D294-SF2; `75298d52dd7596efbb8bfd22205dd2773577308d68c7dec0d518f417136fbd19`);
turn-2 Claude 2 OBJECT (CLAUDE-D294-T2-SF1, CLAUDE-D294-T2-SF2; …); turn-2 Codex OBJECT (CODEX-D294-T2-SF1,
CODEX-D294-T2-SF2; …).` — a COORD-only decision entry took **all three turns** and drew two MUST-FIXes.
Budget accordingly.

### 3.3 The leftover-join recording form, if a join successor is included

**`## D-277`**, Decision (verbatim, in part): `Record leftover-join.v4 as DR-121 leftover remasurement after
D-276. The candidate binds NOTHING. DR-121 stays `OPEN`. leftover-design of OBL-G16-FX-AUTHORING and
OBL-CI-ENCODING-RESERVED remains on leftover-join.v4. … Does not invent reserved CI encodings. Does not name G13
into required-now. … Does not steal OBL-G16-FX-AUTHORING as a GATE closure. … Does not SATISFY DR-121.`
Its Stage A Claude review returned named observations `MLJ4-O1`, `MLJ4-O2`, `MLJ4-O3`, no change requested;
Codex returned zero.

---

## 4. The successor's minimal diff

### 4.1 The COORD entry (the act's substance)

**Records, and only this:** that the six `reservedForBlueprint` members of `monorepo-ci-contract.v16`
(`67ca5016…`) — `CI provider`, `YAML`, `repository path filters`, `caches`, `commands`,
`implementation tooling` — are **implementation encodings**, that the ownership record stays the only impact
authority (`$.selector.authority`), and that the classification **has no Condition-2 or D-056 eligibility
effect** without a separate reviewed scope/eligibility successor and a successor-join remeasurement
(D-293 Decision item 6's cross-cutting clause, which the C5/C6 acts must honour verbatim:
`any later parking disposition names a real trigger and has no Condition-2 or D-056 eligibility effect without a
separate reviewed act and a successor join`).

**Must NOT record:** any concrete CI provider, YAML shape, path-filter table, cache key, command or tooling
choice. The C5–C9 packet §C5 measured: `**None in the record.** No artifact or COORD entry names a CI provider,
a YAML shape, a path-filter table, a cache key/strategy, or a command line for DR-121.` Those six values remain
**explicit named open decisions** in the successor.

**Must NOT record:** a "post-Condition-5" routing as a fact. The C5–C9 packet §0 measured that the phrase
`after condition 5` occurs in exactly two lineages — `packaging-leftover-join.v4`
(`03251cc80cc774c12335ad038eedbb38ce73431623306f11fa1e75e40db61d07`, DR-120) and `sdk-leftover-join.v6`
(`e91d6e926830833d563bb89f3693d65328173af6f0d42275ad5339ef73880341`, DR-125) — and **not** for DR-121:
`No `COORDINATOR-DECISIONS.md` entry contains "after condition 5" or "after Condition 5" (grep: zero hits).`
D-293 itself only says a concrete encoding does not *become* post-Condition-5 work without the further successor.

### 4.2 Optional `monorepo-leftover-join.v5.json`

- `$.obligations[5].reason` — extended to cite the classification act; `leftoverDesign` **stays `true`**,
  `existingGate: "none"`, `executionObligationOwnerToday: "none"`, `rideStanding: "not-capable-of-riding"` all
  byte-identical. `$.summary.leftoverDesign` stays `["OBL-G16-FX-AUTHORING", "OBL-CI-ENCODING-RESERVED"]`.
- `$.reservedForBlueprintVerbatim`, `$.file08Pin`, `$.file08StatusToken` (`"OPEN"`) — byte-identical.
- **Cross-lineage citation refresh (D-294 Decision 3):** the current G16 GATE leftover-join is
  `g16-leftover-join.v5` (recorded **`## D-278`**), not `g16 leftover-join.v4` as
  `$.obligations[5].reason` says. Under D-294 Decision 1 that citation is custody at recording and is **not**
  itself a defect; under Decision 3, a successor issued for another reason must refresh it and label v4 not
  current.

**Reviewer risk to price in:** a join successor whose only change is a `reason` sentence may be charged as an
unwarranted successor. The safer minimum is the COORD-only entry; add the join successor only if Stage B asks
for the classification to be carried in join bytes.

---

## 5. Prohibitions

From **D-293**: `This entry marks nothing `SATISFIED`. It does not edit file 08. It does not open D-056 Class A.
It does not amend D-000 or D-056.`

From **D-277** (verbatim): `Does not pin QUALIFIED. Does not invent fixture bytes. Does not invent reserved CI
encodings. Does not name G13 into required-now. Does not invent a D9 code. Does not invent a section 7.1 recipe.
Does not steal OBL-G16-FX-AUTHORING as a GATE closure. Does not occupy the identifier. Does not SATISFY DR-121.
Does not SATISFY DR-117. Does not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`. Does not flatten DR-107
`PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`. … Gate 1 Class A is not opened. Not SATISFIED. Required-now stays 28.
Condition-4 effect is zero. … Does not execute G16. Does not rewrite occupancy v5. Does not edit file 08. Does
not authorize `docs/v2/implementation/`.`

From **D-056**'s pinned subject (`coordinator-decisions.D-056.turn2.draft.md`
`dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82`), `## Eligibility (narrow)`, gate 2,
verbatim: `Every remaining acceptance-evidence member is **only** harness *execution*, fixture *execution*, or
qualification *measurement*. Authoring of fixtures, schemas, successors, actor-joins, missing design, or
still-UNDECIDED numbers is **not** a remainder this amendment may split.`

From HANDOFF: `Do not invent … reserved CI encodings …`; `Do not steal … OBL-CI-ENCODING-RESERVED …`;
`No file-08 cell edit for leftover/occupancy remasurements.`

---

## 6. Dependencies and ordering

- **Unblocked.** D-293 supplies the classification's content; no owner value is needed.
- **Open question the act must name, not answer (Q6).** Whether the classification is echoed in file 08 — as
  DR-G05's `caps deferred by explicit disposition (D-006)` and DR-130's in-row disposition were — or lives only
  in COORD. **D-293 does not say.** The sentence that shows it: D-293's Decision closes with
  `It does not edit file 08.` and item 7 says only `reviewed architecture-scope acts classify the reserved
  encodings`, naming no register site. A file-08 echo would be an MF-6 with its own cycle; HANDOFF permits a
  cell edit only for `SATISFIED-GRADE COORD drafts`.
- **Open question (Q7).** Whether an obligation classified as implementation-scope but still
  `leftoverDesign: true` can ever satisfy D-056 gate 2. The C5–C9 packet's open question 1, verbatim:
  `Whether an obligation deferred by explicit owner disposition … counts as "missing design, or still-UNDECIDED
  numbers" under D-056 gate 2, or as a lawful deferral that lets gate 2 hold. No COORD entry or artifact rules
  on a sub-row deferral`. D-293's cross-cutting clause answers half of it — no effect **without** a separate
  reviewed act — and leaves open whether such an act can succeed.
- **Runs in parallel with C6.** The two acts are structurally identical and share the same reviewer arguments;
  a reviewer may ask why they are not one entry. They address different rows with different live tokens
  (DR-121 `OPEN` vs DR-107 `PROPOSED-CLOSED-FOR-REVIEW`), which argues for two entries.

---

## 7. Act shape

**Act C5-a — "DR-121: architecture-scope classification of the six reserved CI encodings"** (unblocked).

- **Stage A**: none required (COORD-only decision, the `## D-294` shape); optionally
  `docs/coop/artifacts/monorepo-leftover-join.v5.json`.
- **Stage B**: `coordinator-decisions.D-NNN.draft.md` — dual CONSENT 0/0, up to three turns
  (D-294 needed all three for a comparable entry).
  Decision type: `RULE-GOVERNED` recording of the owner's D-293 disposition (route-C content already exercised
  by the user).
- **Then**: COORD-only append; commit `C-DNNN`.

**Estimated acts: 1** (2 if reviewers require the join successor as a separate recording).
