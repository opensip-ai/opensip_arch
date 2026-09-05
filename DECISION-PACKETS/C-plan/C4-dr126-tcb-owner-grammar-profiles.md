# C4 — DR-126 / platform TCB: what remains after D-293

Measured at HEAD `f3456575071928022a1f0e3a77e531a87157b365` (last COORD heading `## D-294`).
file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; COORD
`31746810f9be78f697d66eb94d9cd50a95a51218998f97a154596363039fb9b6`.

---

## 1. What D-293 already decided, and what remains

**COORD `## D-293`, Decision item 6, C4 sentence (verbatim, COORD lines 16245–16248):**

> `C4: the "G22`
> `qualification evidence" wording is candidate standing only;`
> `owner assignment, then an application-grade TCB successor that`
> `makes the grammar governing, then complete profile population.`

Four limbs:

| Limb | Does an artifact carry a token that must change? | Remaining record act |
|---|---|---|
| **(a) "G22 qualification evidence" wording = candidate standing only** | **No.** The wording lives in `platform-tcb-contract.v45` (`$.status` = `"CANDIDATE-NOT-APPLIED"`, `$.binds` = `"NOTHING"`) and in the G22 occupancy's `namedTcbEvidenceClassesCitedNotApplied`; the current join already measures it as unresolved design (§2.3) | **No further act.** D-293's reading is what the live join already records |
| **(b) owner assignment** | The assignee is **not stated in D-293** (§6, Q4) | **One act**, blocked on the owner |
| **(c) application-grade TCB successor that makes the grammar governing** | Yes — `$.status`/`$.binds` and every `RESERVED` selector standing | **One act**, ordered after (b) by D-293's own word "then" |
| **(d) complete profile population** | Yes — four stems × two RESERVED selectors, plus the per-OS member tables | **One act**, ordered after (c); values not in the record (§6, Q5) |

Limb (a) is the one the reviewers argued over. Codex round 2
(`C1-4-…codex-recommendation.r2.json` `14ed02f426e7c05e7427dbafd186c583433b9566040d9510eab4d8ca16bfcf1e`)
amendment 3, verbatim:

> `Qualify C4's G22-evidence phrase as non-operative candidate standing: ikconfigParserVectors and NT-TCB-KEXEC remain unresolved design unless governing evidence is authored, and reservation alone assigns no gate, execution owner, or riding standing.`

and its refutation, verbatim: `platform-tcb-leftover-join.v9 OBL-RESERVED-TABLES includes both names and records
leftoverDesign true, existingGate 'none', executionObligationOwnerToday 'none', and rideStanding
'not-capable-of-riding'. platform-tcb-contract.v45 contains the G22-evidence wording but is
CANDIDATE-NOT-APPLIED and binds NOTHING.` — i.e. the live join **already** encodes limb (a); nothing to change.

---

## 2. Current artifacts

### 2.1 File 08

Row **DR-126** (line 308, verbatim): `| DR-126 | Platform base/host-ABI TCB and loader closure | Security + release + platform owners | [Exact-byte delivery](04-lifecycle-delivery-and-operations.md#exact-byte-delivery) | Closed OS ABI/loader/libc/framework/cert/font/ICU-class allowlist and identity rules; retained loader traces; undeclared-system-resolution negative tests | OPEN | Hard blocker for platform qualification |`
Owner cell: `Security + release + platform owners`.

Gate row **DR-G22** (line 358): owner `Security + release + platform`; status `PROPOSED; not QUALIFIED`;
waiver cell `pass all declared platforms or remove platform support`; blueprint status `OPEN`.

### 2.2 The contract that reserves the tables and selectors

`docs/coop/artifacts/platform-tcb-contract.v45.json` — sha256
`da87bdb4d100c90e9450fb82744b7d327ae6b7332db550ea808bdbdb0444a7e5`; `$.status` = `"CANDIDATE-NOT-APPLIED"`,
`$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`, `$.binds` = `"NOTHING"`; recorded at **`## D-125`**
(`DR-126 stays OPEN. No SATISFIED. G22 is not QUALIFIED. The candidate binds NOTHING.`).

Verbatim, the reserving JSON paths:

```
$.identityRuleShape.populatedTables = "Per-OS concrete members are RESERVED as G22 qualification evidence."
$.platformProfile.populationPacket  = "A later packet that supplies these selectors is a different artifact. Standing remains RESERVED. requiredBeforeAllowlistFreeze remains true. This contract authors the grammar, including version/build and filesystem selectors, and does not populate them. This row does not name, designate, or claim independent review of that later packet. Choosing its owner is a separate decision. Windows remains D-002 absent."
$.platformProfile.selectorGrammar.requiredMembers = ["osFamily", "architecture", "supportedVersionOrBuildSelector", "filesystemWhereItAffectsResolution"]
$.platformProfile.selectorGrammar.beforeAllowlistFreeze = "Every required member MUST be populated. Partial preview identity is osFamily+architecture only and cannot freeze an allowlist."
$.platformProfile.slice1ProfileStems[0] = {"osFamily": "macos", "architecture": "arm64",
   "supportedVersionOrBuildSelector": {"standing": "RESERVED", "requiredBeforeAllowlistFreeze": true},
   "filesystemWhereItAffectsResolution": {"standing": "RESERVED", "requiredBeforeAllowlistFreeze": true, "mustNot": "apfs-or-hfs-plus as a single value"}}
   (four stems: macos/arm64, macos/x86_64, linux/x86_64, linux/arm64)
$.g22.ikconfigParserVectors = "RESERVED as G22 evidence. vectorRosterRule is GOVERNING: …"
$.taxonomy = ["OS ABI", "loader", "libc", "framework", "certificate store", "font", "ICU", "comparable system-class dependency"]
$.whatThisDoesNotDo[1] = "Does not populate per-OS allowlist rows."
```

### 2.3 The current DR-126 leftover-join and the obligation to remeasure

`docs/coop/artifacts/platform-tcb-leftover-join.v9.json` — sha256
`1774427e9500940d24f75fbaee622142a8be72547d68a026e18d6e957369e26a`; `$.version` = `9`; `$.date` = `"2026-08-24"`;
`$.status` = `"CANDIDATE-NOT-APPLIED"`; `$.registerRow` = `"DR-126"`; `$.file08StatusToken` = `"OPEN"`;
`$.head` = `"1e3e6644edf88fd9a0f11affb1addb70c71393f6"`; `$.file08Pin.sha256` = `e503b75b…` (**live**).
`$.summary.leftoverDesign` = `["OBL-G22-FX-AUTHORING", "OBL-RESERVED-TABLES"]`.
Recording heading: **`## D-268 — Record platform-tcb leftover-join.v9 as DR-126 leftover remasurement`**
(`ADOPTED 2026-08-24`, turn 2; Stage A Claude ACCEPT `408c6fde…` 0/0, Codex ACCEPT `1383c328…` 0/0).

The obligation, verbatim (`$.obligations[5]`):

```
{
 "id": "OBL-RESERVED-TABLES",
 "leftoverDesign": true,
 "existingGate": "none",
 "executionObligationOwnerToday": "none",
 "rideStanding": "not-capable-of-riding",
 "reason": "G22 leftoverNameNote and G22 v1 fields keep per-OS tables, filesystem selectors, version/build selectors, ikconfigParserVectors, and NT-TCB-KEXEC RESERVED. filesystems.standing is RESERVED; matrixStanding is INCOMPLETE on the filesystem selector axis. versionOrBuildSelector.standing is RESERVED; requiredBeforeAllowlistFreeze remains true. v45 whatThisDoesNotDo includes 'Does not populate per-OS allowlist rows.' Undecided tables and selectors are leftover-design (D-056). This join does not populate them and does not freeze an allowlist."
}
```

`$.proposedLaterWork[2]` (verbatim): `A later TCB population packet may supply filesystem and version/build
selector values. This join does not populate those selectors and does not choose that packet's owner.`

### 2.4 The current G22 occupancy

`docs/coop/artifacts/harness.DR-G22.platform-abi-loader.v2.json` — sha256
`2973cda2adac1b612c084b64606e4fc5b5ed5b78317fc64780a7311172ff1307`; `$.status` = `"CANDIDATE-NOT-APPLIED"`,
`$.binds` = `"NOTHING"`; recorded at **`## D-219`** (per the join's `recordedInputs`).
`$.filesystems.standing` = `"RESERVED"`;
`$.filesystems.matrixStanding` = `"INCOMPLETE on the filesystem selector axis until that later packet supplies values."`;
`$.filesystems.laterAct` contains `That packet is a different artifact. This specification does not name, designate, or claim independent review of that packet. Choosing its owner is a separate decision.`;
`$.versionOrBuildSelector.standing` = `"RESERVED on TCB v45. requiredBeforeAllowlistFreeze remains true."`

---

## 3. Precedent

### 3.1 The recording form for this lineage

**`## D-268`**, Decision (verbatim, in part): `Record v9 as DR-126 leftover remasurement after D-267. The
candidate binds NOTHING. DR-126 stays `OPEN`. leftover-design of OBL-G22-FX-AUTHORING and OBL-RESERVED-TABLES
remains on leftover-join.v9. … Does not pin QUALIFIED. Does not invent fixture bytes. Does not populate reserved
TCB tables. Does not invent Rosetta. Does not apply TCB v45. … Does not steal OBL-RESERVED-TABLES. Does not
occupy the identifier. Does not SATISFY DR-126. … Gate 1 Class A is not opened. Not SATISFIED. Required-now
stays 28. Condition-4 effect is zero.`

### 3.2 The application-grade acceptance property (what limb (c) must satisfy)

**COORD `## D-001`, "Standing route-A acceptance property (T2-02)" (verbatim, COORD lines 181–190):**

> `a candidate is applicable when its independent review returns **0 blockers AND grants application-grade acceptance with no express reservation** — no candidate-only limitation, no EXPRESSLY-NOT-FOR-APPLICATION language, no named apply-condition left undischarged on the record — and the coordinator then applies per route A.`

The worked measurement of that property is **`## D-013 — DR-103: the accepted manifest/index/lock design contract`**:
`- **Route-A acceptance property (D-001 T2-02):** MET. 0 blockers; application-grade language;
reservation-language sweep of the VERDICT clean — 5 `reserv` hits, all schema-local …; zero acceptance
reservations. The subject itself carries 60 such hits, all schema-local by construction. Zero named
apply-conditions.` — note the sweep is over the **verdict**, not the subject, and that D-013 still left the row
`OPEN` because a fourth acceptance-evidence element was unmet.

**This is the same programme D-293 authorized for DR-117 at Decision item 5** (`a fresh application-grade dual
review bound to v9's final digest; then the owner-controlled opening entry`), so C4(c) can be modelled on the
DR-117 sequence — but **D-056 Class A stays unopened**: D-293, `It does not open D-056 Class A.`

### 3.3 What this lineage's reviewers attacked

`platform-tcb-leftover-join.v8.review-independent.claude2.json` — **REJECT**, 0 MUST-FIX / 1 SHOULD-FIX,
**CLAUDE-PTLJ-V8-SF1** at `basedOn.predecessorV6.role`: `"The v8 artifact self-labels as v7 …
'This v7 remasures occupancy v1 stale after occupancy v2 (D-219).' … carried unchanged into an artifact whose
artifact field is 'platform-tcb-leftover-join.v8' and whose version is 8, it makes the document attribute its own
remasuring act to a different, frozen artifact."`
`platform-tcb-leftover-join.v8.review-independent.codex.json` — **REJECT**, **CODEX-PTLJ-V8-SF1**, same site:
`"Once republished as v8, the deictic 'This' names the wrong subject version. The same v8 document correctly says
'This v8' in predecessorV7.role and findingDisposition, so it now has conflicting self-labels."`
D-268 records that leftover-join.v9 **landed** both (`leftover-join.v9 lands CLAUDE-PTLJ-V8-SF1 and
CODEX-PTLJ-V8-SF1 (same class: predecessorV6.role leftover this-v7 speaker)`), and that
`CLAUDE-PTLJ-V3-SF1 already landed in this lineage at leftover-join.v5. This entry does not re-land it.`

---

## 4. Successor diffs

### 4.1 Act C4-b — owner assignment (COORD-only)

**Subject**: the COORD draft itself (the D-294 / D-006 / D-010 shape: a decision entry with no artifact
successor). **Decision content**: exactly the assignee the owner names — nothing else. D-293 states none.
If the owner declines to name one, the entry cannot be written: the record says three times that
`Choosing its owner is a separate decision.` (contract `$.platformProfile.populationPacket`; occupancy
`$.filesystems.laterAct`; join `$.proposedLaterWork[2]` in its own words).

Optional companion: `platform-tcb-leftover-join.v10` whose `OBL-RESERVED-TABLES.reason` records the assignment.
`leftoverDesign` **stays `true`** and `$.summary.leftoverDesign` stays
`["OBL-G22-FX-AUTHORING", "OBL-RESERVED-TABLES"]` — the tables and selectors are still unpopulated.

### 4.2 Act C4-c — application-grade TCB successor (`platform-tcb-contract.v46`)

**Changes:** whatever the reviewers require for the grammar to be *governing* rather than proposed —
at minimum `$.status`, `$.reviewStatus`, `$.binds` and the `sealRecommendation`, plus removal of any
express reservation the acceptance property forbids. **D-293 does not state the target values of those fields**,
and `binds` is the field whose value the whole eligibility question turns on; the successor must not choose a
`binds` value the reviewers have not granted.

**Byte-identical:** `$.platformProfile.slice1ProfileStems` (all four stems still `"standing": "RESERVED"`,
`"requiredBeforeAllowlistFreeze": true`), `$.identityRuleShape.populatedTables`, `$.taxonomy`,
`$.g22.ikconfigParserVectors`, `$.whatThisDoesNotDo[1]` — **the grammar becomes governing; the values stay
reserved.** That separation is exactly what D-293's ordering ("then complete profile population") requires.

**Successor join** (`platform-tcb-leftover-join.v11`): `OBL-RESERVED-TABLES` **stays `leftoverDesign: true`**.
Making the grammar governing does not populate a table.

### 4.3 Act C4-d — complete profile population

**Changes:** all four stems' `supportedVersionOrBuildSelector` and `filesystemWhereItAffectsResolution`
populated inside the closed grammar, plus the per-OS member tables over the eight `$.taxonomy` classes.
**No value is in the record** (C1–C4 packet §4.4: `**None in the record** for any per-OS table row, filesystem
selector value, or version/build selector value.`). The grammar bounds any value:
`filesystemWhereItAffectsResolution` is a `closed tagged identifier owned by this contract` with
`identifierEnum` `["apfs", "hfs-plus", "ext4", "xfs", "btrfs", "tmpfs"]` plus `OTHER-FSTYPE`, `wildcardRejected`,
`emptyRejected`, `noOrJoin`; `supportedVersionOrBuildSelector` admits only tag `EXACT-BUILD`
(`CLOSED-RANGE` is `PROHIBITED as a required-member value until this contract versions a total order per
identifierScheme`), with schemes `macos-product-build` (macOS only) and `linux-distro-userspace` (Linux only).

**Only at this act** does `OBL-RESERVED-TABLES` become a candidate for `leftoverDesign: false` — and only if the
per-OS member tables are populated too, since the obligation covers `per-OS tables, filesystem selectors,
version/build selectors, ikconfigParserVectors, and NT-TCB-KEXEC`. Under D-293, `ikconfigParserVectors` and
`NT-TCB-KEXEC` `remain unresolved unless their governing evidence is authored` (Codex round 3), so a partial
population leaves the obligation open.

**Precedent gap to state in the entry:** a sweep of every `*leftover-join*.json` in `docs/coop/artifacts/`
comparing `summary.leftoverDesign` across consecutive versions finds **no case in which a RESERVED-value
obligation has left the partition**. The only recorded partition shrinks are authoring/execution obligations
(`OBL-G15-HARNESS-SPEC` at `## D-174`; `OBL-G23-FX-AUTHORING` → `[]` in `g23-leftover-join.v8` at `## D-240`).
Whatever act closes `OBL-RESERVED-TABLES` will be the first of its class and should say so.

---

## 5. Prohibitions

From **D-293**: `This entry marks nothing `SATISFIED`. It does not edit file 08. It does not open D-056 Class A.
It does not amend D-000 or D-056.` and `It does not record any artifact successor, fixture byte, or successor
join; every such act follows under D-000 as the adopted recommendation states.`

From **D-268** (verbatim): `Does not pin QUALIFIED. Does not invent fixture bytes. Does not populate reserved TCB
tables. Does not invent Rosetta. Does not apply TCB v45. Does not invent a D9 code. Does not invent a section 7.1
recipe. Does not steal OBL-RESERVED-TABLES. Does not occupy the identifier. Does not SATISFY DR-126. Does not
SATISFY DR-117. Does not SATISFY DR-131. Does not SATISFY DR-133. Does not SATISFY DR-114. Does not SATISFY
DR-101. Gate 1 Class A is not opened. … Does not execute G22. Does not rewrite occupancy v2. Does not edit file
08. Does not authorize `docs/v2/implementation/`.`

From **D-125**: `DR-126 stays OPEN. No SATISFIED. G22 is not QUALIFIED. The candidate binds NOTHING.`

From the contract itself: `$.whatThisDoesNotDo[8]`: `Does not remove linux/x86_64 or linux/arm64 from D-002
slice-1 platforms. A machine that cannot produce measuredBootBind fails qualification; the platform class
remains.`; `$.platformProfile.populationPacket`: `Windows remains D-002 absent.`;
`$.tcbCarrier.dependencyIfCarrierAbsent`: `G22 cannot QUALIFY until that one signed carrier exists and is bound.
A population packet is not a substitute carrier.` (that carrier is DR-101's — **C8**).

From the occupancy: `$.filesystems.notG07CoverageDomain` — G07's supported-filesystem coverage domain is a
different question (it is `DECISIONS-NEEDED.md` item C10, which D-293 does **not** decide).

From HANDOFF: `Do not invent … reserved lists … or Rosetta.`; `Do not steal … OBL-RESERVED-TABLES`;
`Do not SATISFY DR-117 / DR-131 / DR-133 (Class A unopened).`;
`D-002 platforms, when quoting occupancy: `macos/arm64`, `macos/x86_64`, `linux/x86_64`, `linux/arm64`. Windows
deferred. Do not invent the platform list.`

---

## 6. Dependencies and ordering

- **D-293 fixes the order literally**: `owner assignment, **then** an application-grade TCB successor that makes
  the grammar governing, **then** complete profile population.` (b) → (c) → (d).
- **Q4 — the assignee is not stated in D-293.** The sentence that shows it: D-293 Decision item 6 says only
  `owner assignment, then an application-grade TCB successor …`; it names no authority.
  The round-2 recommendation the round-3 text adopts "on top of" **does** name one —
  `C1-4-…claude-recommendation.r2.md` `44f51a5d…`, C4 bullet: `assign the population packet to the row's
  authority (`Security + release + platform owners`)` — but that string appears in **neither** D-293's own text
  **nor** the round-3 text carried in `DECISIONS-RECOMMENDED.md` §C1–C4. Whether D-293's adoption reaches the
  round-2 file is an owner call; **not stated in the entry → named open decision.**
- **Q5 — no selector or table value is in the record.** C1–C4 packet §4.4, verbatim: `**None in the record** for
  any per-OS table row, filesystem selector value, or version/build selector value.` D-293 supplies none.
- **Cross-item dependency to C8.** `$.tcbCarrier.dependencyIfCarrierAbsent` routes G22's qualification to a
  signed carrier that is DR-101's — i.e. C8 (OD-101-1 / OD-101-2). C4 can proceed to (c) without it; G22 cannot
  QUALIFY without it.
- **Not a Condition-2 unblock.** `OBL-G22-FX-AUTHORING` stays leftover-design regardless, and D-293 Decision 8
  reserves the G22 gate obligation to the owner (`Reserved to the owner: the gate obligations at G07, G08, G09,
  G12, G14 and G22 … G22 stays reserved until C4 resolves.`).

---

## 7. Act shape

**Act C4-b — "DR-126: TCB population-packet owner"** (blocked on Q4).
Stage A: none (COORD-only decision), or `platform-tcb-leftover-join.v10` if reviewers want the assignment carried
in join bytes. Stage B: COORD draft, dual CONSENT 0/0, up to three turns. `PREFERENCE-LADEN` (route C).

**Act C4-c — "DR-126: application-grade TCB successor (grammar governing)"** (ordered after C4-b).
Stage A: `docs/coop/artifacts/platform-tcb-contract.v46.json` — an **application-grade** dual review against the
D-001 T2-02 property, plus `platform-tcb-leftover-join.v11`. Stage B: COORD draft. `RULE-GOVERNED`.

**Act C4-d — "DR-126: complete profile population"** (blocked on Q5 and on C4-c).
Stage A: the population-packet artifact (a new lineage — the contract says it `is a different artifact`), plus
`harness.DR-G22.platform-abi-loader.v3` (removing `matrixStanding: INCOMPLETE`) and a further
`platform-tcb-leftover-join`. Stage B: COORD draft. `PREFERENCE-LADEN` for the values.

**Estimated acts: 3** (all blocked; the first on an owner sentence, the next two on the first).
