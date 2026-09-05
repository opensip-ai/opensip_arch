# C8 — DR-101 / OD-101-1 core language, OD-101-2 signing & notarization: what remains after D-293

Measured at HEAD `f3456575071928022a1f0e3a77e531a87157b365` (last COORD heading `## D-294`).
file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; COORD
`31746810f9be78f697d66eb94d9cd50a95a51218998f97a154596363039fb9b6`;
`DECISION-PACKETS/C5-9-reserved-encodings-owners-units.md` `735720d9f4df7bba5717f78bb558f378edb9f825971cb60b20ed8cdf07a58e2b`.

---

## 1. What D-293 already decided, and what remains

**COORD `## D-293`, Decision item 7, C8 sentence (verbatim, COORD lines 16257–16261):**

> `C8: OD-101-1 is resolved before the`
> `core-implementation blueprint under `Architecture + release`
> `engineering` (a dedicated D-000 successor, or the owner's`
> `direct statement); OD-101-2 gets its own DR-101 successor owned`
> `separately from DR-112.`

The adopted C8 detail (`DECISIONS-RECOMMENDED.md` `42f27394…` §C5–C9, Claude round 2, verbatim):

> `- **C8 OD-101-1:** resolve the core implementation language before the core-implementation blueprint through a dedicated D-000 successor that compares candidates against DR-101's constraints, recorded under `Architecture + release engineering` (PREFERENCE-LADEN, cheap overturn); the owner may instead state the choice directly — both are lawful; "the owner's alone" and "gates G01–G05 fixtures" withdrawn. **C8 OD-101-2:** its own DR-101 successor covering core code-signing and platform notarization, owned separately from DR-112's trust-recovery mechanics (reviews may be coordinated with C1 but not merged); a deferral to C1 does not close `OBL-D2`.`

| Limb | What D-293 supplies | Remaining record act |
|---|---|---|
| **(a) OD-101-1 — the language** | **The route and the authority only.** No language is named anywhere in D-293 | **One act**, whose *content* is not in the record (§6, Q11–Q12) |
| **(b) OD-101-2 — the ceremony** | **The route only** — "its own DR-101 successor owned separately from DR-112" | **One act**, whose *content* is not in the record (§6, Q13) |
| **(c) "a deferral to C1 does not close `OBL-D2`"** | A prohibition | — |

**Neither limb is dispatchable today.** Both name an act; neither supplies the value the act would record.

---

## 2. Current artifacts

### 2.1 File 08 row (line 283, verbatim)

> `| DR-101 | Native signed distribution-core language, mandatory closure/TCB inventory, layering, signing/notarization, platforms | Architecture + release engineering | [Distribution](02-distribution-and-components.md) | Reviewed closure inventory and dependency graph; gate harnesses DR-G01–G05 | OPEN | Hard blocker for core implementation blueprint |`

Owner cell: `Architecture + release engineering` — the authority D-293 names.
Related: DR-118 blueprint-impact cell (line 300): `does not mandate implementation language`.

### 2.2 The contract carrying both reservations

`docs/coop/artifacts/distribution-core-inventory-contract.v16.json` — sha256
`429b8c7a9cd5c8f2b495337c055ccbd262e796ba1cc42efb173779c72018fb5b`; `$.status` = `"CANDIDATE-NOT-APPLIED"`,
`$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`, `$.binds` = `"NOTHING"`; `$.version` = `16`;
`$.date` = `"2026-08-15"`; recorded at **`## D-114`**.

```
$.namedOpenDecisions[0] = {
  "id": "OD-101-1",
  "decision": "Core implementation language (the decision-column word 'language')",
  "standing": "RESERVED. File 02 says 'small native executable' and later uses native/Rust as quality framing, not a recorded language selection. This artifact does not mint Rust-as-core.",
  "owner": "A later Route-C or rule-governed successor, not this extraction."
}
$.namedOpenDecisions[1] = {
  "id": "OD-101-2",
  "decision": "OS notarization ceremony and signing ceremony details",
  "standing": "RESERVED. Signing ROLES are listed (inventory/identity). Ceremony/thresholds/notarization remain a DR-101 decision. DR-112 recovery ceremony and DR-110 repair-media trust are adjacent input mechanics, not owners of core code-signing or OS notarization.",
  "owner": "A later DR-101 successor, not this extraction. Same form as OD-101-1."
}
```

### 2.3 The DR-101 constraints a candidate must be compared against (verbatim from v16)

The adopted recommendation requires `a dedicated D-000 successor that compares candidates against DR-101's
constraints`. Those constraints, quoted verbatim from bytes:

**From the file-08 row (line 283):** the Decision column
`Native signed distribution-core language, mandatory closure/TCB inventory, layering, signing/notarization,
platforms`; the required-acceptance-evidence column `Reviewed closure inventory and dependency graph; gate
harnesses DR-G01–G05`; the blueprint-impact column `Hard blocker for core implementation blueprint`.

**From `distribution-core-inventory-contract.v16`:**

```
$.threeCores.rule                    = "The three terms are not collapsed."
$.threeCores.signedDistributionCore  = "Proposed small native executable plus its mandatory runtime/data closure. Boundary: packaging, install, update, trust, management/recovery footprint."
$.threeCores.semanticHost            = "Host authority for admission, Snapshot/Plan, findings/facts, Coverage, policy, finalization, durable authority, D9, and output. Authority is non-delegable. MAY share a process with the distribution core."
$.threeCores.pureEvaluationCore      = "R-1 data-only deterministic evaluation function returning CoreCompletion. No effects, callbacks, ports, entropy, filesystem, network, process, store, or resident state."
$.threeCores.oneExecutableSharing    = "Distribution core and semantic host may initially be one executable. That does not permit semantic work to migrate into components or effects into the pure evaluation core."

$.defaultInstall.contains  = ["routing", "strict configuration", "authentication", "trust", "updates", "host semantic authority", "output", "component protocol/supervision", "lifecycle/recovery", "essential lock/journal/audit state"]
$.defaultInstall.excludes  = ["language runtimes", "analyzers", "graph engines", "report generators", "evidence databases", "telemetry backends"]
$.defaultInstall.managementOnly = "Core-only is management and recovery: help, version, completion, configuration, component inventory/lifecycle, status, doctor, and repair. It is not the current full analysis product and cannot claim absent capabilities."
$.defaultInstall.containsStanding = "PROPOSED inclusion list. File 02 L23: 'The default install is proposed to contain'."

$.platforms.slice1  = ["macos/arm64", "macos/x86_64", "linux/x86_64", "linux/arm64"]
$.platforms.windows = "DELIBERATELY absent. D-002 defers Windows."
$.platforms.warrant = "D-002. This artifact does not reopen the platform set."

$.gatesG01G05.standing     = "Named (D-086/D-088/D-102). Not authored. Not QUALIFIED."
$.gatesG01G05.numbers      = "DECIDED by D-006. Recorded SATISFIED Class B for DR-115 (D-089). Measurement leftover is condition 4."
$.gatesG01G05.staleFile02  = "File 02 L38-41's 'thresholds remain open at DR-115' is stale. Live law is D-006."
$.gatesG01G05.thisArtifact = "Binds the inventory members those gates measure. Does not re-decide numbers. Does not execute the harnesses."

$.whatThisDoesNotDo[0] = "Does not SATISFY DR-101 until independently reviewed at SATISFIED-GRADE and recorded by a later D-000 MF-6. A T2-02 contract alone does not make the row D-056-eligible while OD-101-1 and OD-101-2 remain design reservations."
$.whatThisDoesNotDo[1] = "Does not choose the core implementation language."
$.whatThisDoesNotDo[2] = "Does not design notarization or signing ceremony."
$.whatThisDoesNotDo[3] = "Does not claim a qualified small core."
$.whatThisDoesNotDo[4] = "Does not put language runtimes, analyzers, evidence databases, or storage backends in the default install."
$.whatThisDoesNotDo[5] = "Does not execute G01-G05."
$.whatThisDoesNotDo[6] = "Does not authorize docs/v2/implementation/."
```

And the eligibility sentence the C5–C9 packet pins at `$.recordedInputs.governingSources[1].role`:
`… DR-101 is ineligible under D-056 and remains so while OD-101-1 and OD-101-2 are open design reservations: the
remainder is not only execution/measurement (gate 2) and is not already named at a condition-4 / DR-G*
obligation (gate 3). A T2-02 contract alone does not unlock SATISFIED. …`

**Plus the D-006 numeric envelope any language choice must live inside** (file 08 DR-115 row, line 297):
`core ≤25 MB compressed / ≤80 MB installed; help/version cold p50/p95/p99 100/150/250 ms, warm p95/p99 50/100 ms;
RSS steady/peak 40/50 MB help-version, 60/100 MB doctor read-only` — now with `MB` = 1e6 bytes for
G01/G02/G04 by D-293 (see **C9**).

**No candidate language list exists anywhere in the record** (§6, Q11).

### 2.4 The current DR-101 leftover-join and the two obligations

`docs/coop/artifacts/distribution-core-leftover-join.v9.json` — sha256
`e6b235d3330a03e62acede6770919a413791c958a3e791eca5f677e822100bc7`; `$.version` = `9`; `$.date` = `"2026-08-27"`;
`$.status` = `"CANDIDATE-NOT-APPLIED"`; `$.registerRow` = `"DR-101"`; `$.file08StatusToken` = `"OPEN"`;
`$.head` = `"81c76572dde1d413aa48b214f6c7fc36008baf62"`; `$.file08Pin.sha256` = `e503b75b…` (**live**).
It has **no `proposedLaterWork` field**. Recording heading:
**`## D-287 — Record distribution-core leftover-join.v9 as DR-101 leftover remasurement`**
(`ADOPTED 2026-08-27`; Stage A dual ACCEPT 0/0; Stage B dual CONSENT 0/0).

`$.summary` (verbatim): `{"leftoverDesign": ["OBL-2", "OBL-D1", "OBL-D2"], "capableOfRidingNamedGates":
["OBL-1", "OBL-D-INV", "OBL-D-LAY", "OBL-D3"], "requiredNowUnchanged": 28, "newRowProposed": false,
"languageNotDecided": true, "ceremonyNotDecided": true, "harnessSpecificationsNotAuthored": false,
"d006UnitUndecided": true}`

```
$.obligations[4] = {
 "id": "OBL-D1", "alias": "OD-101-1", "leftoverDesign": true, "existingGate": "none", "gateOwners": {},
 "registerRowOwner": "Architecture + release engineering", "rideStanding": "not-capable-of-riding",
 "reason": "Core implementation language is RESERVED on distribution-core-inventory-contract.v16. G01-G05 measure size, startup, memory, and component delta. They do not own a language choice. G13 is language-quality for supported analyzer roles, not core-language selection. This join does not mint Rust-as-core."
}

$.obligations[5] = {
 "id": "OBL-D2", "alias": "OD-101-2", "leftoverDesign": true, "existingGate": "none", "gateOwners": {},
 "registerRowOwner": "Architecture + release engineering", "rideStanding": "not-capable-of-riding",
 "reason": "distribution-core-inventory-contract.v16 extracts signing ROLES and reserves ceremony/thresholds/notarization. G01-G05 do not own OS notarization or code-signing ceremony. DR-112 recovery ceremony and DR-110 repair-media trust remain adjacent, not owners."
}
```

(`$.obligations[1]` `OBL-2` is **C9**'s.)

---

## 3. Precedent

### 3.1 The recording form for this lineage

**`## D-287`**, Decision (verbatim, in part): `Record leftover-join.v9 as DR-101 leftover remasurement after
D-286. The candidate binds NOTHING. DR-101 stays `OPEN`. leftover-design of OBL-2, OBL-D1, OBL-D2 remains on
leftover-join.v9. … OBL-2 remains leftover-design on the D-006 unit/accounting limb; OD-101-1 and OD-101-2 remain
leftover-design; harness-spec authoring is measured closed against the current G01-G05 occupancy remasurements;
execution remains qualification (D-056). Does not pin QUALIFIED. Does not invent fixture bytes. Does not invent a
D-006 unit. Does not mint Rust-as-core. Does not decide OD-101-2. Does not invent G01-G05 harness
specifications. … Does not steal G30 useful-install selection from DR-117. Does not retarget G22 / DR-126. Does
not occupy the G01-G05 identifiers. Does not SATISFY DR-101. … Gate 1 Class A is not opened.`

### 3.2 What this lineage's reviewers attacked, one version earlier

`distribution-core-leftover-join.v8.review-independent.claude2.json` — **REJECT**, 0 blockers / 0 MUST-FIX /
2 SHOULD-FIX, 29 attacks run, 2 landing:

- **CLAUDE-DCLJ-V8-SF1**, at `obligations[1].reason` (id `OBL-2`), title verbatim:
  `"obligations[OBL-2].reason introduces a lineage-custody claim — the authoring limb 'was measured stale as an
  authoring claim at leftover-join.v3' — that the frozen leftover-join.v3 bytes contradict and that the
  subject's own predecessorJoin.v3.role contradicts"`.
- **CLAUDE-DCLJ-V8-SF2**: the verdict's `whatWouldAccept` verbatim: `"A leftover-join.v9 that (1) drops or
  corrects the 'at leftover-join.v3' custody token in OBL-2.reason to what v3/v4/v7 bytes support, and (2)
  replaces 'carries the former basedOn object unchanged' with a description of the actual diff. Partition, pins,
  digests, occupancy quotations, speaker labels, token qualification and the cumulative lands record are all
  correct at this fold and need no change."`

D-287 records that leftover-join.v9 landed both, and documents the lands ledger in unusual detail — the entry's
own words: `Its findingDisposition carries leftover-join.v7's three identifiers in the same order … each reading
`ACCEPTED` in leftover-join.v7 and, in leftover-join.v9, `ACCEPTED. Landed in this lineage at leftover-join.v3.
This v9 does not re-land it.` …`. **The v10 successor inherits that ledger discipline.**

### 3.3 The precedent gap for the flip

`OBL-D1` and `OBL-D2` are RESERVED-value obligations. A sweep of every `*leftover-join*.json` in
`docs/coop/artifacts/` comparing `summary.leftoverDesign` across consecutive versions finds **no case in which a
RESERVED-value obligation left the partition** — see the C7 file §3.2 for the two authoring/execution
precedents (`OBL-G15-HARNESS-SPEC` at `## D-174`; `g23-leftover-join.v8` `[]` at `## D-240`). Whichever of
C7-OD-2, C8-OD-101-1 or C8-OD-101-2 lands first will be the first of its class.

---

## 4. The successor's minimal diff

### 4.1 If the owner states a language (act C8-a)

**Subject options, both lawful per the adopted text:** a `distribution-core-inventory-contract.v17` recording
the selection, **or** the COORD entry alone with a `distribution-core-leftover-join.v10`.
**D-293 does not choose between them**; it says `a dedicated D-000 successor, or the owner's direct statement`.

`distribution-core-leftover-join.v10` diff:
- `$.obligations[4]` (`OBL-D1`) — `leftoverDesign` `true` → `false`; id leaves `$.summary.leftoverDesign`;
  `$.summary.languageNotDecided` `true` → `false`. Bucket not stated by D-293 (this lineage's summary has
  `capableOfRidingNamedGates` and `leftoverDesign` only — **there is no discharged bucket in this schema**, so
  the successor must either add one and say so, or keep `OBL-D1` in `obligations[]` with
  `leftoverDesign: false` and no summary membership. Not stated → name the choice in the entry).
- `$.obligations[5]` (`OBL-D2`) — **byte-identical**, `leftoverDesign: true`. `$.summary.ceremonyNotDecided`
  stays `true`.
- `$.obligations[1]` (`OBL-2`) — see **C9**; unaffected by the language choice.
- `$.file08Pin`, `$.file08StatusToken` (`"OPEN"`), `$.registerRow` — byte-identical.
- **Must retain** the guard wherever it is not made moot: the entry may not read as minting a language the owner
  did not name. If the owner names Rust, the successor must say so explicitly and cite the owner's words — the
  corpus carries `does not mint Rust-as-core` in `## D-231`, `## D-232`, `## D-287`,
  `distribution-core-leftover-join.v9` `$.obligations[4].reason`, `packaging-leftover-join.v4`
  `$.obligations[OBL-ADAPTER-IMPL].reason`, and HANDOFF. Superseding a guard that dense needs an express
  sentence, not silence.

### 4.2 If the owner states a ceremony (act C8-b)

`distribution-core-leftover-join.v11` (or v10 if run together) diff:
- `$.obligations[5]` (`OBL-D2`) — `leftoverDesign` `true` → `false`; `$.summary.ceremonyNotDecided` → `false`.
- Must preserve the boundary verbatim: `DR-112 recovery ceremony and DR-110 repair-media trust remain adjacent,
  not owners.` and the C1 split — `component-manifest-schemas.v11` `$.whatThisDoesNotDo[2]`:
  `Does NOT define the signing ceremony: key custody, thresholds, rotation, expiry, revocation, quorum loss,
  recovery, and envelope validity are DR-112's surface.` — that is the *index/component* ceremony; OD-101-2 is
  the **core binary code-signing and OS notarization** ceremony only.
- Platform-bound: any notarization statement quantifies over `$.platforms.slice1` =
  `["macos/arm64", "macos/x86_64", "linux/x86_64", "linux/arm64"]`; `Windows` stays `DELIBERATELY absent`.

### 4.3 Cross-lineage citations (D-294 Decision 3)

`distribution-core-leftover-join.v9` is **not** among the eight citing joins D-294 measured, so no existing
cross-lineage citation needs repair; any citation the successor adds must name the version current at its
dispatch and label superseded ones not current.

---

## 5. Prohibitions

From **D-293**: `This entry marks nothing `SATISFIED`. It does not edit file 08. It does not open D-056 Class A.
It does not amend D-000 or D-056.`; and the C8-specific `OD-101-2 gets its own DR-101 successor owned separately
from DR-112.` (reviews `may be coordinated with C1 but not merged`; `a deferral to C1 does not close OBL-D2`).

From **D-287** (verbatim): `Does not pin QUALIFIED. Does not invent fixture bytes. Does not invent a D-006 unit.
Does not mint Rust-as-core. Does not decide OD-101-2. Does not invent G01-G05 harness specifications. Does not
invent a D9 code. Does not invent a section 7.1 recipe. Does not steal G30 useful-install selection from DR-117.
Does not retarget G22 / DR-126. Does not occupy the G01-G05 identifiers. Does not SATISFY DR-101. Does not
SATISFY DR-117. Does not SATISFY DR-126. Does not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`. Does not
flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`. Does not SATISFY DR-131. Does not SATISFY DR-133. Does
not SATISFY DR-114. Gate 1 Class A is not opened. Not SATISFIED. Required-now stays 28. Condition-4 effect is
zero. … Does not execute G01-G05. Does not rewrite G01 occupancy v9, G02 occupancy v4, G03 occupancy v5, G04
occupancy v4, or G05 occupancy v4. Does not edit file 08. Does not authorize `docs/v2/implementation/`.`

From the contract: `$.whatThisDoesNotDo[0]` — `A T2-02 contract alone does not make the row D-056-eligible while
OD-101-1 and OD-101-2 remain design reservations.`; `$.platforms.warrant` — `D-002. This artifact does not
reopen the platform set.`

From HANDOFF, `## Do not invent / do not SATISFY`: `Do not invent … reserved lists, UNDECIDED numbers …`;
`Do not SATISFY DR-117 / DR-131 / DR-133 (Class A unopened).`;
`D-002 platforms, when quoting occupancy: `macos/arm64`, `macos/x86_64`, `linux/x86_64`, `linux/arm64`. Windows
deferred. Do not invent the platform list.`

---

## 6. Dependencies, ordering, and what is not in the record

- **Q11 — no candidate language, and no candidate list, is in the record.** The C5–C9 packet §C8 measured:
  `OD-101-1: **none in the record** as a decision. The only language-shaped bytes are file 02's "small native
  executable" and "native/Rust as quality framing" (as characterised by v16's own standing sentence).`
  A `dedicated D-000 successor that compares candidates against DR-101's constraints` therefore has to
  **enumerate the candidates first** — and HANDOFF says `Do not invent … reserved lists`. **D-293 names no
  candidate set.** The sentence that shows it: item 7 says only `OD-101-1 is resolved before the
  core-implementation blueprint under `Architecture + release engineering` (a dedicated D-000 successor, or the
  owner's direct statement)`.
- **Q12 — route C or rule-governed?** `## D-001` classes DR-101 as `Rule-governed architecture authoring with
  review`, while the contract's own `$.namedOpenDecisions[0].owner` says `A later Route-C or rule-governed
  successor, not this extraction.` The record does not resolve the disjunction (C5–C9 packet, open question 4);
  D-293 does not either. It matters because route C sets the overturn cost (D-000 clause 5).
- **Q13 — no ceremony content is in the record.** C5–C9 packet §C8: `OD-101-2: **none in the record.** Signing
  ROLES exist (v16 `inventorySchema.signingRolesNote`, inventory/identity only); no ceremony, threshold, or
  notarization procedure is named.`
- **Ordering.** OD-101-1 first: the contract's `$.namedOpenDecisions[1].owner` says OD-101-2 is
  `Same form as OD-101-1`, D-293 sequences the language `before the core-implementation blueprint`, and the
  C5–C9 packet notes the ceremony `is platform-mechanical once the language and toolchain exist`.
- **Both are required for DR-101 eligibility, and are still not sufficient.** `$.recordedInputs
  .governingSources[1].role` requires **both** closed; `OBL-2`'s execution limb (C9) and Gate-1 Class A remain.
- **Downstream of C8.** `platform-tcb-contract.v45` `$.tcbCarrier.dependencyIfCarrierAbsent`:
  `G22 cannot QUALIFY until that one signed carrier exists and is bound. A population packet is not a substitute
  carrier.` — so **C4**'s gate qualification waits on this row's signing decision.

---

## 7. Act shape

**Act C8-a — "DR-101: OD-101-1 core implementation language"** (blocked on Q11/Q12/the owner's word).

- **Stage A**: `distribution-core-inventory-contract.v17.json` (if the selection is carried in contract bytes)
  **and** `distribution-core-leftover-join.v10.json`; or the join alone.
- **Stage B**: `coordinator-decisions.D-NNN.draft.md` — dual CONSENT 0/0, up to three turns.
  Decision type: `PREFERENCE-LADEN` (D-000 clause 5: `their overturn procedure is written to cost less than the
  decision did`), unless the owner directs the rule-governed reading (Q12).

**Act C8-b — "DR-101: OD-101-2 core code-signing and OS notarization"** (blocked on Q13; ordered after C8-a).

- **Stage A**: a DR-101 successor artifact carrying the ceremony **and** a further
  `distribution-core-leftover-join`. Review may be coordinated with the C1 (DR-112) review but **not merged**.
- **Stage B**: COORD draft, dual CONSENT 0/0.

**Estimated acts: 2** (both blocked on owner content that D-293 does not supply).
