# C9 — D-006 MB unit (1e6 bytes) and G02 tree-accounting: what remains after D-293

Measured at HEAD `f3456575071928022a1f0e3a77e531a87157b365` (last COORD heading `## D-294`).
file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; COORD
`31746810f9be78f697d66eb94d9cd50a95a51218998f97a154596363039fb9b6`;
`DECISION-PACKETS/C5-9-reserved-encodings-owners-units.md` `735720d9f4df7bba5717f78bb558f378edb9f825971cb60b20ed8cdf07a58e2b`.

---

## 1. What D-293 already decided, and what remains

**COORD `## D-293`, Decision item 7, C9 sentence (verbatim, COORD lines 16261–16263):**

> `C9: MB means 1e6 bytes for the D-006`
> `G01/G02/G04 quantities; G02 installed-tree accounting stays open`
> `until the named authorities record a complete rule.`

The adopted C9 detail (`DECISIONS-RECOMMENDED.md` `42f27394…` §C5–C9, Claude round 2, verbatim):

> `- **C9 DR-115/D-006:** record now that MB means 1e6 bytes for the D-006 G01/G02/G04 quantities (the record-named decimal reading); leave G02 installed-tree accounting open until `Product + release engineering` and `Architecture + release` record a complete rule covering logical lengths, allocated blocks, metadata/xattrs, links, and deduplicated inventory nodes; do not invent it.`

**The unit decision is itself recorded — D-293 is the D-006 unit successor.** What remains is that **four live
artifacts still carry `UNDECIDED` tokens D-293 has now falsified in part**:

| Artifact | JSON path | Current value | After D-293 |
|---|---|---|---|
| `distribution-core-leftover-join.v9` | `$.summary.d006UnitUndecided` | `true` | must become `false` |
| `distribution-core-leftover-join.v9` | `$.obligations[1].reason` (`OBL-2`) | `"Remainder is (a) D-006 unit and G02 tree-accounting UNDECIDED, so size comparison cannot be scored, and (b) G01-G05 execution…"` | the unit half is decided; the accounting half and (b) remain |
| `harness.DR-G01.core-download.v9` | `$.basedOn.d006.role` | `"…Unit standing remains UNDECIDED. This occupancy does not invent 26214400 as an authorized bound…"` | unit standing decided |
| `harness.DR-G02.core-installed.v4` | `$.basedOn.d006.role` | `"…Unit standing remains UNDECIDED. G02 tree-accounting remains UNDECIDED…"` | unit decided; accounting still UNDECIDED |
| `harness.DR-G04.core-memory.v4` | `$.basedOn.d006.role` | `"…Unit standing remains UNDECIDED. This occupancy does not invent a binary-MB byte constant as an authorized bound…"` | unit standing decided |

So: **three occupancy successors and one join successor.** `OBL-2` does **not** leave the leftoverDesign
partition — its remainder (b), `G01-G05 execution, which remains qualification (D-056)`, and the G02 accounting
limb both survive.

---

## 2. Current artifacts

### 2.1 Where the leftover lives (not on DR-115)

DR-115 (file 08 line 297) is `**SATISFIED 2026-08-14 (D-089 / D-056 Class B).**` and has no leftover-join. The
unit/accounting limb is measured on DR-101's join.

`docs/coop/artifacts/distribution-core-leftover-join.v9.json` — sha256
`e6b235d3330a03e62acede6770919a413791c958a3e791eca5f677e822100bc7`; `$.version` = `9`; `$.date` = `"2026-08-27"`;
`$.status` = `"CANDIDATE-NOT-APPLIED"`; `$.registerRow` = `"DR-101"`; `$.file08StatusToken` = `"OPEN"`;
`$.file08Pin.sha256` = `e503b75b…` (**live**), whose `note` reads
`Post D-286. required-now 28. File 08 bytes are the live tree last moved by D-236 …`.
Recording heading: **`## D-287`**.

The obligation, verbatim (`$.obligations[1]`):

```
{
 "id": "OBL-2",
 "leftoverDesign": true,
 "existingGate": "DR-G01, DR-G02, DR-G03, DR-G04, DR-G05",
 "gateOwners": {"DR-G01": "Release engineering", "DR-G02": "Architecture + release", "DR-G03": "Release engineering", "DR-G04": "Release engineering", "DR-G05": "Component publisher + release"},
 "registerRowOwner": "Architecture + release engineering",
 "rideStanding": "not-capable-of-riding",
 "reason": "Independently reviewed G01-G05 occupancy remasurements now exist: G01 occupancy v9 (D-231), G02 occupancy v4 (D-232), G03 occupancy v5 (D-233), G04 occupancy v4 (D-234), G05 occupancy v4 (D-235), each dual ACCEPT 0/0, CANDIDATE-NOT-APPLIED, not QUALIFIED, live assurance stage SPECIFIED. Their frozen predecessors (G01 occupancy v1, G02 occupancy v1, G03 occupancy v4, G04 occupancy v1, G05 occupancy v1; CGHS v4 promised-path occupancies; Claude ACCEPT 0/0; Codex not reviewed) are not current. The authoring-of-specifications limb of OBL-2 is stale as an authoring claim. Remainder is (a) D-006 unit and G02 tree-accounting UNDECIDED, so size comparison cannot be scored, and (b) G01-G05 execution, which remains qualification (D-056). This join does not invent a D-006 unit and does not execute G01-G05."
}
```

`$.summary.d006UnitUndecided` = `true`; `$.summary.leftoverDesign` = `["OBL-2", "OBL-D1", "OBL-D2"]`.

### 2.2 The three occupancies

| Path | sha256 | Recorded at | `$.basedOn.d006.role` (verbatim) |
|---|---|---|---|
| `docs/coop/artifacts/harness.DR-G01.core-download.v9.json` | `f28b0d97723550c8690eec2a6ac7803efba93fd797f266600b038b14e269277b` | `## D-231` | `Threshold DECIDED: signed compressed distribution-core ≤ 25 MB per platform. Unit standing remains UNDECIDED. This occupancy does not invent 26214400 as an authorized bound and does not close leftover-join.v7 remainder (a) of OBL-2.` |
| `docs/coop/artifacts/harness.DR-G02.core-installed.v4.json` | `1bc247f779fa980ecde7d7a244effa6116f02a79be4a0ee74e0cedb168ccf360` | `## D-232` | `Threshold DECIDED: immutable installed tree ≤ 80 MB; mandatory-closure inventory enumerated. Unit standing remains UNDECIDED. G02 tree-accounting remains UNDECIDED. This occupancy does not invent 83886080 as an authorized bound and does not close leftover-join.v7 remainder (a) of OBL-2.` |
| `docs/coop/artifacts/harness.DR-G04.core-memory.v4.json` | `f664f7fd7a428dc9fd05a3142f5a50a242704659d72f66fb509c66106e4e7845` | `## D-234` | `Threshold DECIDED: --help/--version steady baseline ≤ 40 MB; peak ≤ 50 MB; doctor read-only steady baseline ≤ 60 MB; peak ≤ 100 MB. analyze RSS and doctor-with-consented-probes RSS remain outside D-006. Unit standing remains UNDECIDED. This occupancy does not invent a binary-MB byte constant as an authorized bound and does not close leftover-join.v7 remainder (a) of OBL-2.` |

Each is `$.status` `"CANDIDATE-NOT-APPLIED"`. Their `doesNot` lists carry the matching refusals, verbatim:
G01 `"Does not invent a D-006 unit or authorize 26214400 as the bound."`;
G02 `"Does not invent a D-006 unit or authorize 83886080 as the bound."` and `"Does not invent G02 tree-accounting."`;
G04 `"Does not invent a D-006 unit or authorize a binary-MB byte constant."` and `"Does not invent G02 tree-accounting."`
The scoring sentences: G01 EV-2 `passProperty`: `… Size comparison to 25 MB is scored only after a D-006 unit
successor. Exclusion membership is scored now.`; G02 EV-3 `passProperty`: `Raw installed-tree measurement is
recorded. Size comparison to 80 MB is scored only after a D-006 unit-and-accounting successor. …`

### 2.3 The unrecorded candidate that framed the question

`docs/coop/artifacts/core-gate-harness-specifications.v4.json` — sha256
`59f47a612f5f7b9ee073caec063a0dd336ca427a40a4aef2f08a174a44284b1b`; `$.status` = `"CANDIDATE-NOT-APPLIED"`,
`$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`, `$.binds` = `"NOTHING"`. **No COORD heading names it**
(the C5–C9 packet: `grep over `COORDINATOR-DECISIONS.md`: zero hits`); it reaches the record only as a digest
pin in `distribution-core-leftover-join.v9` `$.recordedInputs`, and that join calls the
`CGHS v4 promised-path occupancies` `not current`.
`$.d006UnitStanding.numerals` = `"25 / 80 / 40 / 50 / 60 / 100 MB as written in D-006. Not restated as a byte constant here."`;
`$.d006UnitStanding.g02InstalledTreeAccounting` = `"UNDECIDED. Logical file lengths vs allocated blocks vs metadata/xattrs vs links vs deduplicated inventory nodes is not decided here."`;
`$.d006UnitStanding.comparisonRule` = `"A later D-006 unit/accounting successor decides the conversion and G02 domain. Until then a job records raw bytes and the D-006 numeral but cannot claim pass/fail against a byte constant invented here."`
**Anything quoted from this file must be labelled as an unrecorded candidate**, exactly as the C5–C9 packet does.

---

## 3. Precedent

### 3.1 The scoped D-006 successor form

**`## D-102 — D-006 fleet-class successor plus G03/G04 named identifiers`**, Decision type verbatim:
`PREFERENCE-LADEN scoped D-006 successor plus RULE-GOVERNED naming of the v3 reserved identifiers.`
Status: turn 2 of 3, dual CONSENT 0/0, `New cycle after D-101 CONTESTED`, with `Turn-1 Claude 2 SHOULD-FIX
D102-T1-SF-1 accepted`. **D-293 has already played the D-102 role for the unit**; the acts below are the
downstream artifact remasurements, of the D-231…D-235 occupancy-remasurement class.

### 3.2 The occupancy-remasurement recording form

`## D-231` (G01 v9), `## D-232` (G02 v4), `## D-234` (G04 v4) — the C5–C9 packet quotes their Decision
sentences verbatim: D-231 `… Does not invent a D-006 unit or authorize 26214400 as the bound. …`;
D-232 `… Does not invent a D-006 unit or authorize 83886080 as the bound. Does not invent G02 tree-accounting. …`
Each is one COORD entry per occupancy: **five separate entries for five occupancies**. If that granularity is
kept, C9 is **three** occupancy entries plus one join entry.

### 3.3 What reviewers attacked

- `harness.DR-G02.core-installed.v3.review-independent.claude2.json`, line 132 (quoted in the C5–C9 packet):
  `"The constant is 80 MiB in bytes, which is exactly the conversion D-006 has not authorized …"` — the
  reviewer's own reason for refusing the binary constant, and the reason the decimal reading now needs an
  express warrant.
- `core-gate-harness-specifications.v2.review-independent.codex.json`: `"Those constants are 25×2^20 and 80×2^20."`
- `distribution-core-leftover-join.v8.review-independent.claude2.json` — **REJECT** 0/2, and
  **CLAUDE-DCLJ-V8-SF1 lands precisely on `obligations[OBL-2].reason`**: `"obligations[OBL-2].reason introduces a
  lineage-custody claim … that the frozen leftover-join.v3 bytes contradict"`. `OBL-2.reason` is the single most
  attacked field in this lineage; the C9 join successor edits exactly that field.

---

## 4. The successors' minimal diffs

### 4.1 `distribution-core-leftover-join.v10.json`

- `$.summary.d006UnitUndecided` — `true` → `false`.
- `$.obligations[1].reason` — remainder (a) narrows: the D-006 **unit** is decided at D-293
  (`MB means 1e6 bytes for the D-006 G01/G02/G04 quantities`); **G02 tree-accounting stays UNDECIDED**;
  remainder (b) `G01-G05 execution, which remains qualification (D-056)` is byte-identical.
  The sentence `This join does not invent a D-006 unit and does not execute G01-G05.` must change its first
  half: the join does not invent one — D-293 recorded one — and must cite D-293 rather than claim the decision.
- `$.obligations[1].leftoverDesign` — **stays `true`**; `$.summary.leftoverDesign` stays
  `["OBL-2", "OBL-D1", "OBL-D2"]`. **This act closes no obligation.**
- `$.obligations[4]` (`OBL-D1`) and `$.obligations[5]` (`OBL-D2`) — byte-identical; `languageNotDecided` and
  `ceremonyNotDecided` stay `true` (C8).
- `$.file08Pin`, `$.file08StatusToken` (`"OPEN"`) — byte-identical.
- The lands ledger and `findingDisposition` must carry v9's entries forward under the discipline D-287 spells
  out, re-landing nothing.

### 4.2 `harness.DR-G01.core-download.v10.json`, `harness.DR-G02.core-installed.v5.json`, `harness.DR-G04.core-memory.v5.json`

- `$.basedOn.d006.role` — `Unit standing remains UNDECIDED` → the D-293 unit, cited to D-293.
- The `doesNot` entries that refuse a byte constant must be reworded, **and this is the delicate part**:
  D-293 states the **rule** (`MB means 1e6 bytes`), not the **constants**. `25000000`, `80000000`,
  `40000000`, `50000000`, `60000000`, `100000000` appear **nowhere in the record**. A successor that writes a
  constant is deriving it arithmetically from D-293's rule; a successor that writes only the rule is safest.
  **Recommended form:** state the rule and the numeral (`≤ 25 MB, MB = 1e6 bytes per D-293`) and let the
  arithmetic be the reader's — mirroring `$.d006UnitStanding.numerals`'s own posture
  (`Not restated as a byte constant here.`). Flag the choice to reviewers rather than making it silently.
- **G01 and G04 become scorable; G02 does not.** G02's `passProperty` says
  `Size comparison to 80 MB is scored only after a D-006 unit-**and-accounting** successor` — and D-293 leaves
  accounting open. G02 v5 must keep `G02 tree-accounting remains UNDECIDED` and keep
  `"Does not invent G02 tree-accounting."`
- Everything else byte-identical: `$.status` `CANDIDATE-NOT-APPLIED`, `not QUALIFIED`, the naming parent
  (`naming v6 (D-145)`), `Does not change live required-now 28`, `Does not edit file 08`.

### 4.3 What must remain an explicit named open decision

**G02 installed-tree accounting.** D-293: `G02 installed-tree accounting stays open until the named authorities
record a complete rule.` The five dimensions the adopted recommendation requires that rule to cover —
`logical lengths, allocated blocks, metadata/xattrs, links, and deduplicated inventory nodes` — come from an
**unrecorded candidate** (`core-gate-harness-specifications.v4` `$.d006UnitStanding.g02InstalledTreeAccounting`),
and the recorded G02 occupancy says only `accounting method named but not invented here` (EV-3
`exactByteIntent`). The successors must not treat the five-dimension list as a recorded enumeration.

---

## 5. Prohibitions

From **D-293**: `This entry marks nothing `SATISFIED`. It does not edit file 08. It does not open D-056 Class A.`
and `G02 installed-tree accounting stays open until the named authorities record a complete rule.`

From **D-287** (verbatim): `Does not invent a D-006 unit.` — the successor inverts this **only** to the extent
D-293 decided, and must say it cites D-293 rather than deciding. Also from D-287: `Does not pin QUALIFIED. …
Does not execute G01-G05. Does not rewrite G01 occupancy v9, G02 occupancy v4, G03 occupancy v5, G04 occupancy
v4, or G05 occupancy v4. Does not edit file 08.`

From **D-232** (verbatim): `Does not invent a D-006 unit or authorize 83886080 as the bound. Does not invent G02
tree-accounting.` — the second half still holds in full.

From **`## D-006`** itself: `Falsifiability note: If early implementation shows a number infeasible, the lawful
path is a successor decision with the measurement attached — never a silent waiver.` The unit act
**re-decides no D-006 numeral**; DR-115 stays `SATISFIED` (D-089).

From **`## D-102`**'s pinned subject (`coordinator-decisions.D-102.turn2.draft.md`, item 5, line 178):
`GiB = bytes/1024³` for fleet-class RAM matching — **a different domain**, unchanged by D-293 (C5–C9 packet,
open question 3: `no recorded entry requires or forbids a common base`).

From HANDOFF: `Do not invent … UNDECIDED numbers …`; `No file-08 cell edit for leftover/occupancy
remasurements.`; `Do not occupy CGHS promised paths except frozen occupancies.`

---

## 6. Dependencies and ordering

- **Unblocked.** D-293 supplies the unit; the four successors need nothing from the owner.
- **Q14 — byte constants.** D-293 states `1e6` as a rule; the six derived constants are not in the record.
  Whether the successors may write them is a reviewer question the act must raise, not resolve silently.
- **Q15 — G02 accounting authorities.** D-293 says `until the named authorities record a complete rule` and
  names none in that sentence; the adopted recommendation names two —
  `Product + release engineering` and `Architecture + release` (the DR-115 and DR-G02 owner cells,
  file 08 lines 297 and 338). Whether D-293's `the named authorities` refers to those two is a reading the
  entry does not state. **Owner question.**
- **No readiness effect.** DR-115 stays `SATISFIED`; DR-101 keeps three leftover obligations; Condition 2
  stays 5 of 32; required-now stays 28.
- **Feeds C8.** Any core-language candidate comparison (C8-a) is measured against the D-006 envelope, which is
  only now unambiguous for G01/G04. Run C9 before C8-a.
- **Ordering with C8.** Both edit `distribution-core-leftover-join`. Running C9 first means C8's successor
  starts from v10; running them together risks one limb's objection parking both. **C9 first.**

---

## 7. Act shape

**Act C9-a — "G01 occupancy v10: D-006 unit decided at D-293"**
**Act C9-b — "G02 occupancy v5: D-006 unit decided; tree-accounting stays UNDECIDED"**
**Act C9-c — "G04 occupancy v5: D-006 unit decided at D-293"**
**Act C9-d — "distribution-core leftover-join.v10: OBL-2 unit limb remasured"** (after C9-a/b/c)

Each: **Stage A** the artifact, dual adversarial review at 0/0 → **Stage B** `coordinator-decisions.D-NNN.draft.md`,
dual CONSENT 0/0 → COORD-only append. Decision type `RULE-GOVERNED`, same no-cell-edit branch as
D-170 through D-235 and D-237 through D-294 (D-272 excluded — CONTESTED).

**Estimated acts: 4** at the D-231…D-235 granularity; **2** if the three occupancies are recorded in one entry
and the join in another (a bundling the record has not used for occupancies and which reviewers may refuse).
