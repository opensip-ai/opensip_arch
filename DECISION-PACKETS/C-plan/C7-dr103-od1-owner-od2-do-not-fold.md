# C7 — DR-103 / OD-1 owner and caps, OD-2 do-not-fold: what remains after D-293

Measured at HEAD `f3456575071928022a1f0e3a77e531a87157b365` (last COORD heading `## D-294`).
file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; COORD
`31746810f9be78f697d66eb94d9cd50a95a51218998f97a154596363039fb9b6`;
`DECISION-PACKETS/C5-9-reserved-encodings-owners-units.md` `735720d9f4df7bba5717f78bb558f378edb9f825971cb60b20ed8cdf07a58e2b`.

---

## 1. What D-293 already decided, and what remains

**COORD `## D-293`, Decision item 7, C7 sentence (verbatim, COORD lines 16253–16257):**

> `C7: OD-1 is`
> `assigned to DR-115's `Product + release engineering` authority`
> `as a scoped D-006 threshold-family successor with measured caps`
> `before oversized-input fixtures; OD-2 is a final do-not-fold`
> `disposition.`

The adopted C7 detail (`DECISIONS-RECOMMENDED.md` `42f27394…` §C5–C9, Claude round 2, verbatim):

> `- **C7 OD-1:** assign to DR-115's `Product + release engineering` authority as a scoped D-006 threshold-family successor; do not import DR-G05's first-component-acceptance deferral automatically; record measured manifest-byte / tree-entry / path-length / alias-count caps before authoring oversized-input fixtures; if values are not available, leave the numeric limb open and say so. **C7 OD-2:** a final **do-not-fold** disposition (the candidate schema itself says the class-specific DR-111 statements are unambiguous); remeasure `OBL-OD-2` closed by that design choice; name OD-2 with OD-1 at the next MF-6. My round-1 "fold, delegated" withdrawn.`

| Limb | Does an artifact carry a token that must change? | Remaining record act |
|---|---|---|
| **(a) OD-1 owner = DR-115's `Product + release engineering`** | **Yes.** File 08's DR-103 status cell says `remains OPEN with its owner UNASSIGNED between DR-115 and DR-120`; `component-manifest-leftover-join.v9` `$.obligations[9].reason` says `Owner UNASSIGNED between DR-115 and DR-120`; `component-manifest-schemas.v11` `$.namedOpenDecisions[0].candidateOwners` names two candidates | **One act** (COORD entry + join successor); the file-08 cell waits for an MF-6 |
| **(b) the four caps** | No value in the record; D-293 supplies none. The adopted fallback: `if values are not available, leave the numeric limb open and say so` | **No act now**; the numeric limb stays an explicit named open decision (§6, Q8) |
| **(c) "do not import DR-G05's first-component-acceptance deferral automatically"** | A prohibition on the act | — |
| **(d) OD-2 = final do-not-fold** | **Yes.** `component-manifest-leftover-join.v9` `$.obligations[11]` has `leftoverDesign: true`; `component-manifest-schemas.v11` `$.namedOpenDecisions[1].standing` = `"OPEN. Still not folded at v11. …"` | **One act** — and it is the only **unblocked** leftoverDesign flip in the C set, and the first of its class on record (§3.2) |
| **(e) "name OD-2 with OD-1 at the next MF-6"** | The file-08 DR-103 cell names OD-1 and not OD-2 | **No act now** — it rides the next DR-103 MF-6, which `component-manifest-leftover-join.v9` `$.proposedLaterWork[0]` already anticipates |

Limbs (a) and (d) can be one entry or two. They share a subject artifact (`component-manifest-leftover-join.v10`)
and neither depends on the other.

---

## 2. Current artifacts

### 2.1 File 08 — DR-103 row (line 285), the OD-1 sentence verbatim

> `named open decision **OD-1** (manifest byte size / tree entry count / path length / alias count caps — an unbounded-input surface at metadata-only admission; oversized-input refusal UNSPECIFIED, not implied) remains OPEN with its owner UNASSIGNED between DR-115 and DR-120, and choosing that owner is a separate decision — DR-115's `DECIDED-V1-NOT-INTEGRATED` annotation does not cover these numbers, because D-006 decided DR-G01..G05 only.`

DR-103 owner cell: `Delivery + security`.
DR-115 row (line 297) owner cell: `Product + release engineering`; lead label
`**SATISFIED 2026-08-14 (D-089 / D-056 Class B).**`
DR-120 row (line 302) owner cell: `Component architecture + release/developer-experience + language owners`.
**OD-2 is not named in the DR-103 cell**; file 08 names it once, in the DR-G31 row (line 367).

### 2.2 The schema artifact that states both open decisions

`docs/coop/artifacts/component-manifest-schemas.v11.json` — sha256
`1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005`; `$.status` = `"CANDIDATE-NOT-APPLIED"`,
`$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`, `$.binds` = `"NOTHING"`; recorded at **`## D-104`**.

`$.namedOpenDecisions` is an array of objects; verbatim:

```
$.namedOpenDecisions[0].id            = "OD-1"
$.namedOpenDecisions[0].decision      = "Size caps: manifest byte size, tree entry count, path length, alias count"
$.namedOpenDecisions[0].standing      = "NO caps are stated in these schemas, and that absence is a NAMED OPEN DECISION, not a default. Unbounded manifests are a denial-of-service surface at metadata-only admission - the treeCommitmentShape alternatives note's own self-flag, answered here with an owner rather than left rhetorical."
$.namedOpenDecisions[0].candidateOwners = "DR-115's numeric-threshold machinery (which already owns the core's size/startup/memory numbers, DECIDED at D-006, with the measurement half at qualification) or DR-120's packaging contract (which owns what an adapter may emit). This artifact declines to mint the numbers: a cap is a product threshold, and thresholds in this corpus are product-owned, measured, and waiver-formed (the D-006 pattern)."
$.namedOpenDecisions[0].consequence  = "Until an owner states caps, admission enforces structural rules only, and oversized-input refusal is UNSPECIFIED, not implied - a fixture author must not assume it."

$.namedOpenDecisions[1].id            = "OD-2"
$.namedOpenDecisions[1].decision      = "Whether to normalize TC-ACCEPT/TC-SIG/TC-BYTE-EXACT lock deferral onto a single conditionalRequires array-of-{member,gate} shape (carried Claude v6 advisories V6-A2 and V6-A3)."
$.namedOpenDecisions[1].standing      = "OPEN. Still not folded at v11. Previously recorded at v8 /openDecisions[OD-V8-1]; moved to namedOpenDecisions at v9."
$.namedOpenDecisions[1].candidateOwners = ["this schema surface (DR-103)"]
$.namedOpenDecisions[1].consequence  = "Each class already states the DR-111 gate unambiguously. Normalization is findability/shape, not a change to the no-lock-until-DR-111 rule. Activation is a later successor of this artifact, not a SATISFIED-GRADE corpus review by itself."
$.namedOpenDecisions[1].priorId      = "OD-V8-1"
$.namedOpenDecisions[1].registerEchoAtApplication = "On any later application/MF-6 of this surface, the live DR-103 row must name OD-2 alongside OD-1. This artifact binds NOTHING and does not edit file 08."
$.namedOpenDecisions[1].corpusAdvance = "Corpus v2 is process-frozen against schemas.v9 so the v10/v11 digest citation stays resolvable. Advancing that draft to pin a later schema requires a corpus v3 or an explicit unfreeze-and-recite, not a silent retarget."
```

### 2.3 The current DR-103 leftover-join and the two obligations

`docs/coop/artifacts/component-manifest-leftover-join.v9.json` — sha256
`e71dca64c78a8feea9e72df5ae846eb2843be50fb10d01d54d5b65714ed1d2c4`; `$.version` = `9`; `$.date` = `"2026-08-26"`;
`$.status` = `"CANDIDATE-NOT-APPLIED"`; `$.registerRow` = `"DR-103"`; `$.file08StatusToken` = `"OPEN"`;
`$.head` = `"e4b20dd9b282c519cc85ecc4711da513d1efca10"`; `$.file08Pin.sha256` = `e503b75b…` (**live**).
Recording heading: **`## D-282 — Record component-manifest leftover-join.v9 as DR-103 leftover remasurement`**
(`ADOPTED 2026-08-26`, turn 2 of 3, dual CONSENT 0/0; Stage A Claude ACCEPT `db852c4d…` 0/0, Codex ACCEPT
`46b67eb6…` 0/0; turn-1 **dual OBJECT** — Claude `CLAUDE-D282-SF1`/`SF2`, Codex `CODEX-D282-SF1`/`SF2`/`SF3`).

`$.summary` (verbatim, in part):
`"leftoverDesign": ["OBL-WINDOWS-PATH", "OBL-ENVELOPE-MISMATCH", "OBL-UNICODE-NORM", "OBL-OD-1", "OBL-OD-2"]`,
`"specifiedNotLeftover": ["OBL-SCHEMA", "OBL-FIXTURE-51", "OBL-V2-A1", "OBL-G15-HARNESS-SPEC", "OBL-WINDOWS-PATH-NAMED"]`,
`"dischargedOrDeferred": ["OBL-SIG-CEREMONY", "OBL-LOCK"]`, `"requiredNowUnchanged": 28`,
`"file08CellStaleOnFixtureAbsence": true`.

The two obligation objects, verbatim:

```
$.obligations[9] = {
 "id": "OBL-OD-1", "leftoverDesign": true, "existingGate": "none",
 "executionObligationOwnerToday": "none", "rideStanding": "not-capable-of-riding",
 "reason": "File 08 named open decision OD-1: manifest byte size / tree entry count / path length / alias count caps. Owner UNASSIGNED between DR-115 and DR-120. UNDECIDED numbers are leftover-design (D-056). This join does not assign the owner and does not invent the numbers."
}

$.obligations[11] = {
 "id": "OBL-OD-2", "leftoverDesign": true, "existingGate": "none",
 "executionObligationOwnerToday": "none", "rideStanding": "not-capable-of-riding",
 "reason": "schemas.v11 namedOpenDecisions OD-2 is OPEN, still not folded at v11: whether to normalize TC-ACCEPT/TC-SIG/TC-BYTE-EXACT lock deferral onto a single conditionalRequires array-of-{member,gate} shape (Claude advisories CLAUDE-V6-A2/A3 on component-manifest-schemas.v6, carried as OD-2 into schemas.v11 namedOpenDecisions). Candidate owner is this schema surface (DR-103). Activation is a later successor of that artifact. registerEchoAtApplication: any later application/MF-6 of this surface must name OD-2 alongside OD-1 on the live DR-103 row. This join does not fold OD-2 and does not edit file 08."
}
```

`$.proposedLaterWork[4]` = `A later D-000 cycle may assign OD-1's owner and decide the numbers. This join does
neither.`; `$.proposedLaterWork[6]` = `A later schemas successor may fold OD-2 (conditionalRequires shape). This
join does not fold it.`; `$.proposedLaterWork[0]` anticipates the MF-6:
`A later D-000 MF-6 may rewrite the DR-103 status-cell clause that still recites D-013 'no fixtures exist to
run' and historical V2-A1-as-unlanded prose, recording the D-106 candidate and naming OD-1 alongside OD-2,
without SATISFIED. This join does not apply that MF-6.`

---

## 3. Precedent

### 3.1 "Scoped D-006 successor" — the form D-293 names for OD-1

**`## D-102 — D-006 fleet-class successor plus G03/G04 named identifiers`**, `Decision type` verbatim:
`PREFERENCE-LADEN scoped D-006 successor plus RULE-GOVERNED naming of the v3 reserved identifiers.`
Status: `**ADOPTED 2026-08-14.** Turn 2 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX.
… Turn-1 Claude 2 SHOULD-FIX D102-T1-SF-1 accepted (`CPU_SUBTYPE_ANY` + `ocount == 1`). … New cycle after D-101
CONTESTED.` — the C5–C9 packet notes that `D-094/D-098/D-099/D-101 were CONTESTED attempts at that same
successor before D-102 landed`. **A scoped D-006 successor is the most CONTESTED-prone act shape in this
corpus.**

D-102 did edit file 08 (`Write G03/G04 reserved identifiers into file 08 as named`) — but that was a
register-content act with condition-4 effect. **The C7 OD-1 act has no such warrant**: D-293 says
`It does not edit file 08.`, and the DR-103 cell edit is expressly routed to a later MF-6 by
`$.proposedLaterWork[0]` and by schemas.v11 `registerEchoAtApplication`.

### 3.2 A leftover-join obligation leaving the `leftoverDesign` partition

**The only recorded shape** is an authoring/execution obligation closed by authored bytes or a recorded
specification:

- `component-manifest-leftover-join.v2` (**`## D-161`**) → `component-manifest-leftover-join.v6.json`
  `9953f9692379f3f30254df12735d284559da6b6e979fd684296ace02d0e6e212` (**`## D-174`**):
  `OBL-G15-HARNESS-SPEC` moved from `$.summary.leftoverDesign` to `$.summary.specifiedNotLeftover`, its object
  becoming `{"id": "OBL-G15-HARNESS-SPEC", "leftoverDesign": false, "existingGate": "DR-G15",
  "namedIdentifiersNotAuthored": [], "executionObligationOwnerToday": "Component architecture + language
  publisher + release/DevEx", "rideStanding": "qualification-at-named-gate", "reason": "G15 is named (D-086) and
  the specification now exists at harness.DR-G15.packaging-adapter-conformance.v7 … Leftover-design of authoring
  that specification is therefore stale as an authoring claim. Remainder is G15 execution, which remains
  qualification (D-056). …"}` — **the exact same lineage as OD-2**, which makes it the closest template.
- `g23-leftover-join.v8.json` `498324e5e456562317c7681b44cdac9138ca1e947aa363dad5a331caa3eef812` (**`## D-240`**):
  `leftoverDesign is `[]`` after the D-237 / D-239 fixture recordings.

**Measured gap.** A sweep of every `*leftover-join*.json` in `docs/coop/artifacts/`, comparing
`summary.leftoverDesign` across consecutive versions, finds **no case in which a RESERVED/UNDECIDED-value
obligation left the partition.** The OD-2 flip will be the **first of its class**: an obligation closed by a
*design choice* rather than by authored bytes. The successor and its COORD entry should say so plainly; a
reviewer who cannot find the precedent will otherwise raise it.

### 3.3 What this lineage's reviewers attacked

- `component-manifest-leftover-join.v8.review-independent.codex.json` — **REJECT**, 0 MUST-FIX / 2 SHOULD-FIX.
  `CMLJ-V8-SF1` at `basedOn.predecessorV6.role`: `"The v8 successor retains v7's deictic speaker label … 'This
  v7 remasures occupancy v7 stale after occupancy v9 (D-214).' … deictic 'This v7' names the wrong speaker and
  triggers the prompt's explicit leftover-this-v7 attack."`; `CMLJ-V8-SF2` at `purpose`:
  `"The purpose calls the cumulative lands record unchanged while v8 extends it"`.
- `component-manifest-leftover-join.v8.review-independent.claude2.json` — **REJECT**, `CLAUDE-CMLJ-V8-SF1`,
  same site: `"The repair is a one-token wording change; a v9 carrying it with pins remeasured is the expected
  shape."`
- `component-manifest-leftover-join.v7` was **Dual REJECT** (D-282: `leftover-join.v7 is CANDIDATE-NOT-APPLIED
  (Dual REJECT: Codex CMLJ-V7-SF1; Claude CLAUDE-CMLJ-V7-SF1 / CLAUDE-CMLJ-V7-SF2)`).
- D-282 itself needed two turns and landed five Stage-B identifiers.

**This lineage has burned two candidate versions on custody wording alone.** Budget for it.

---

## 4. The successor's minimal diff

### 4.1 `component-manifest-leftover-join.v10.json` (Stage A subject)

**`$.obligations[9]` (`OBL-OD-1`):**
- `leftoverDesign` **stays `true`** — the four caps are still undecided. D-293 assigns an owner; it states no number.
- `existingGate` — **not stated by D-293.** DR-115 is `SATISFIED` and has no gate of its own for these caps;
  the D-006 threshold family measures at `DR-G01..G05`, which `whatThisDoesNotDo[3]` of
  `platform-tcb-contract.v45` and the file-08 cell both say do **not** cover these numbers
  (`D-006 decided DR-G01..G05 only`). The safe successor keeps `"none"` and records the owner in `reason`.
  **Do not** invent a gate to make the obligation ride: D-293's cross-cutting clause forbids an eligibility
  effect `without a separate reviewed act and a successor join`.
- `reason` — must replace `Owner UNASSIGNED between DR-115 and DR-120` with the D-293 assignment
  (`DR-115's `Product + release engineering` authority`), keep `UNDECIDED numbers are leftover-design (D-056)`,
  and state that the numeric limb is left open per the adopted fallback.

**`$.obligations[11]` (`OBL-OD-2`):**
- `leftoverDesign` **`true` → `false`**; the id moves out of `$.summary.leftoverDesign`.
- **Which bucket it moves to is not stated by D-293.** The lineage's two precedents are
  `specifiedNotLeftover` (`OBL-G15-HARNESS-SPEC`, D-174) and `dischargedOrDeferred`
  (`OBL-SIG-CEREMONY`, `OBL-LOCK`). A disposition-closed design decision reads closer to
  `dischargedOrDeferred`; **the successor should name its choice and its reason, not assume one** (§6, Q10).
- `existingGate`, `executionObligationOwnerToday`, `rideStanding` — must be restated consistently with
  `leftoverDesign: false`. The D-174 template set `rideStanding: "qualification-at-named-gate"` because a gate
  remained; OD-2 has **no** remainder at all once do-not-fold is final, so the honest values are not the D-174
  values. **Not stated in the record → the successor must reason from bytes and expect a reviewer challenge.**
- `reason` — must record: the disposition is final do-not-fold; its warrant is D-293 plus the schema's own
  `consequence` (`Each class already states the DR-111 gate unambiguously. Normalization is findability/shape,
  not a change to the no-lock-until-DR-111 rule.`); the register echo (`the live DR-103 row must name OD-2
  alongside OD-1`) remains owed at a later MF-6; and no schema successor is authored by this act.

**Byte-identical:** `$.obligations` for `OBL-WINDOWS-PATH`, `OBL-ENVELOPE-MISMATCH`, `OBL-UNICODE-NORM`
(all stay `leftoverDesign: true`); `$.summary.specifiedNotLeftover`; `$.summary.requiredNowUnchanged` = 28;
`$.file08Pin`; `$.file08StatusToken` = `"OPEN"`; `$.authoredFixtureAudit`
(`v6AuthoredCount: 51`, `filesPresent: 51`, `sha256Mismatches: 0`).

**Cross-lineage citations (D-294 Decision 3):** `component-manifest-leftover-join.v9` is one of the eight citing
joins D-294 measured — it cites `g15 leftover-join.v5`, and the current G15 GATE leftover-join is
`g15-leftover-join.v6` (recorded **`## D-290`**). Under D-294 Decision 1 that citation is **custody at
recording** and is not itself a defect; under Decision 3, this successor — issued for the OD-1/OD-2 reason —
**must** refresh it to v6 and label v5 not current.

### 4.2 Optionally `component-manifest-schemas.v12.json`

Only if reviewers require the disposition in schema bytes: `$.namedOpenDecisions[1].standing` records the
do-not-fold. **Beware `$.namedOpenDecisions[1].corpusAdvance`**: `Advancing that draft to pin a later schema
requires a corpus v3 or an explicit unfreeze-and-recite, not a silent retarget.` A schemas v12 therefore drags
a corpus act with it. **The cheaper act is COORD + join only**; D-293 does not require a schemas successor
(it says `OD-2 is a final do-not-fold disposition`, not "fold it at v12" — the round-1 "fold, delegated" position
was **withdrawn**).

---

## 5. Prohibitions

From **D-293**: `This entry marks nothing `SATISFIED`. It does not edit file 08. It does not open D-056 Class A.
It does not amend D-000 or D-056.` and `It does not record any artifact successor, fixture byte, or successor
join; every such act follows under D-000 as the adopted recommendation states.`

From the adopted recommendation itself: `do not import DR-G05's first-component-acceptance deferral
automatically`; `if values are not available, leave the numeric limb open and say so`.

From **D-282** (verbatim): `Does not pin QUALIFIED. Does not invent fixture bytes. Does not invent a
reserved-device-name list. Does not invent a schema successor. Does not decide OD-1 or assign its owner. Does not
fold OD-2. Does not invent a D9 code. Does not invent a section 7.1 recipe. Does not steal OBL-AT-FX-AUTHORING or
OBL-ADAPTER-IMPL. Does not occupy the identifier. Does not SATISFY DR-103. Does not SATISFY DR-120. Does not
SATISFY DR-117. Does not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`. Does not flatten DR-107
`PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`. … Gate 1 Class A is not opened. Not SATISFIED. Required-now stays 28.
Condition-4 effect is zero. … D-013's SATISFIED-refusal stands. … Does not execute G15. Does not rewrite
occupancy v9. Does not edit file 08. Does not authorize `docs/v2/implementation/`.`
(The successor inverts exactly two of these — `Does not decide OD-1 or assign its owner` and `Does not fold
OD-2` — and only in the direction D-293 states: it **assigns** OD-1's owner and records a **do-not-fold**
disposition. It still does not decide the numbers and still does not fold.)

From **D-106**: `Locks remain deferred to DR-111. … No lock producible.` — and `schemas.v11`
`$.lockSchema.purpose`: `NO lock is producible until DR-111 closes`. The do-not-fold disposition must say it
`is findability/shape, not a change to the no-lock-until-DR-111 rule`.

From **D-006** turn-2 NOTE-03, quoted at **`## D-013`** Alternatives (b): `the closed status vocabulary stays
closed; coining an analog would itself be a register-content decision` — no new file-08 token.

From HANDOFF: `Do not steal … OBL-OD-1 / OBL-OD-2`; `Do not invent … UNDECIDED numbers …`;
`No file-08 cell edit for leftover/occupancy remasurements.`;
`Do not SATISFY DR-117 / DR-131 / DR-133 (Class A unopened).`

---

## 6. Dependencies and ordering

- **Q8 — are the caps measurable from bytes? No.** Measured:
  - `component-manifest-schemas.v11` `$.namedOpenDecisions[0].standing`: `NO caps are stated in these schemas,
    and that absence is a NAMED OPEN DECISION, not a default.`
  - Same object, `candidateOwners`: `This artifact declines to mint the numbers: a cap is a product threshold,
    and thresholds in this corpus are product-owned, measured, and waiver-formed (the D-006 pattern).`
  - `## D-006`, Decision type: `PREFERENCE-LADEN (route C). Numbers are not derivable from any rule; the
    register says so ("numeric open").`
  - `component-manifest-leftover-join.v9` `$.obligations[9]`: `existingGate: "none"` — **no gate measures these
    four quantities**, so there is no harness whose measurement could produce them.
  D-293's phrase is `with measured caps before oversized-input fixtures`; it does **not** say what is measured,
  by whom, at which gate, or against which corpus. **Not stated → named open decision.** Until the owner
  supplies values, the numeric limb stays open and no oversized-input fixture may be authored
  (`a fixture author must not assume it`).
- **Q9 — MF-6 or successor-only for DR-115?** The C5–C9 packet's open question 2, verbatim: `For OD-1 assigned
  to DR-115: whether the caps require an MF-6 note on the (already `SATISFIED`) DR-115 row or only a D-006
  successor cited from the schemas/occupancies. The record shows both mechanisms in use (D-089 MF-6 for the
  label; D-102 successor without label change) and does not say which applies to added thresholds.` D-293 does
  not resolve it.
- **Q10 — which summary bucket `OBL-OD-2` moves to** (see §4.1). Not stated.
- **Ordering.** (a) and (d) are independent of each other and of every other C item. (d) is the cheaper and
  is fully determined by D-293. (b) is blocked on the owner. (e) rides a later DR-103 MF-6.
- **Consequence of (d) for DR-103's leftover set:** four obligations remain leftover-design
  (`OBL-WINDOWS-PATH`, `OBL-ENVELOPE-MISMATCH`, `OBL-UNICODE-NORM`, `OBL-OD-1`), three of which D-293
  Decision 8 reserves to the owner (`Reserved to the owner: … `OBL-WINDOWS-PATH`, `OBL-ENVELOPE-MISMATCH`,
  `OBL-UNICODE-NORM``). So (d) does **not** move DR-103 toward D-056 eligibility.
- **A stale cell the act should not fix.** The DR-103 cell still refers to `DR-115's
  `DECIDED-V1-NOT-INTEGRATED` annotation` while DR-115's lead label is now `**SATISFIED 2026-08-14 (D-089 /
  D-056 Class B).**`. That reconciliation belongs to the DR-103 MF-6, not here (C5–C9 packet, open question 6).

---

## 7. Act shape

**Act C7-a — "DR-103: OD-1 owner assigned to DR-115 `Product + release engineering`; OD-2 final do-not-fold"**
(unblocked).

- **Stage A**: `docs/coop/artifacts/component-manifest-leftover-join.v10.json` — dual adversarial review,
  ACCEPT only at 0/0.
- **Stage B**: `coordinator-decisions.D-NNN.draft.md` — dual CONSENT 0/0, up to three turns.
  Decision type: `PREFERENCE-LADEN scoped D-006 threshold-family successor` for the OD-1 limb (the D-102 form,
  with the owner's preference already exercised at D-293) **plus** `RULE-GOVERNED` for the OD-2 disposition.
- **Then**: COORD-only append; commit `C-DNNN`.

**Split option:** because the OD-1 limb inherits D-102's CONTESTED history and the OD-2 limb is the first
leftoverDesign flip of its class, running them as **two entries** (OD-2 first, as the cleaner act) reduces the
chance that one limb's objection parks both.

**Estimated acts: 1 (or 2 if split).** A later DR-103 MF-6 — naming OD-2 alongside OD-1 and reconciling the
stale DR-115 reference — is a third, separate, file-08-editing act that this plan does not schedule.
