# Decision Packet C (part 1) — reserved numbers and lists: DR-112, DR-118, DR-111, DR-126

Prepared for the human owner (sole decision authority) by the Claude orchestrator's packet subagent, 2026-08-27.
Measured at HEAD `4abb961` (last COORD heading D-292; 277 `## D-` headings counted by `grep -c "^## D-"`).

Pinned sources (sha256 measured at HEAD):

| Source | Path | sha256 |
|---|---|---|
| file 08 (the register) | `docs/v2/architecture/08-decision-and-readiness-register.md` | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| COORD | `docs/coop/COORDINATOR-DECISIONS.md` | `47f7b2011ec719dfadcbccb553a142eb0808e3099f20bf544b4564ab18e28466` |
| D-056 turn-2 subject | `docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md` | `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82` |

Packet rules honoured: every claim carries a citation; tokens, numbers and statuses are quoted verbatim; nothing is decided here; where the record holds no value the packet says **not in the record**; nothing under `docs/` was edited.

---

## 0. Ground common to all four items

### 0.1 What Condition 2 requires, and how a deferral counts

**File 08, `### Current position — measured snapshot, 2026-08-15`, Condition table, row 2** (line 415):

> `| 2 | Every slice-affecting V2 row `SATISFIED` | **5 of 32 `SATISFIED`** — 24 `OPEN`, 1 `DECIDED-V1-NOT-INTEGRATED`, 2 `PROPOSED-CLOSED-FOR-REVIEW`. … | **NOT MET** |`

**COORD `## D-001`, quoted adopted checklist, bullet 2** (COORD line 107-109):

> `2. DR-101 through DR-127 that affect the first blueprint slice are`
> `   `SATISFIED`; deferred items have explicit product/architecture scope`
> `   dispositions.`

(D-010 later made this quantifier range-free: "the condition quantifies over 'every row of the V2 architecture and product decisions table that affects the first blueprint slice.'" — COORD `## D-010`, **Decision** bullet.)

**COORD `## D-001`, "Condition 2 — all 29 rows classified (MF-5 closed the DR-108 gap)"** (COORD line 267-268):

> `Items D-002 excludes get explicit`
> `deferral dispositions, never silence.`

**COORD `## D-056`, Decision bullet:** `D-002/D-010 deferrals stay on the deferral limb.`

**D-056 turn-2 subject (`dfb0c2af…`), `## Decision` items 3, 6, 8** (draft lines 175-180, 191-194, 197-200):

> `3. **Does not rewrite D-001's five checklist bullets.**`
> `   Condition 2 still requires SATISFIED or explicit deferral.`
> …
> `6. **Deferred D-002 / D-010 items stay on the deferral limb.**`
> `   This amendment is not a deferral and does not replace those`
> `   dispositions. Later owner-recordings of those deferrals are`
> `   separate cycles.`
> …
> `8. **Does not extend D-070's two-axis algorithm to condition`
> `   2.** Condition 2 continues to be counted from leading`
> `   SATISFIED labels plus explicit deferral dispositions, not`
> `   from this amendment existing.`

**Same draft, disposition table row** (draft line 151): `| DR-106 / 108 / 109 / 110 / 113 / 116 / 128 / 129 / 130 | Deferral limb of condition 2 (D-002 / D-010), not this amendment. |`

So the record's own term is **"explicit deferral disposition"** / **"the deferral limb"**. The token "post-Condition-5" appears in `DECISIONS-NEEDED.md` items C5–C6 only (lines 46-47); items C1–C4 do not carry it (C1 reads `Decide now, or defer with an explicit disposition?`). `STATUS.2026-08-26.md` §3.C (line 60) uses the phrase `after Condition 5` — `DR-120 adapter implementations, DR-125 SDK APIs, DR-107/121 encodings are reserved to *after Condition 5* — implementation, not design` — for DR-120/DR-125/DR-107/121, not for the four items here. Neither phrase occurs in COORD or file 08 (`grep -n -i "post-condition-5\|after condition 5\|post-condition 5\|post-Condition"` returns nothing in either file). A disposition "to after Condition 5" would therefore be new wording for these four items; the record's existing deferral shapes are the two precedents below.

### 0.2 The two deferral precedents in the record

**Row-level (row leaves the slice):** file 08 row **DR-130**, Status cell (line 312): `OPEN — slice 1 claims no upgrade continuity and its deferral disposition is RECORDED HERE (D-010, C-D010): DR-130 does not affect the first blueprint slice`. Rows DR-128/DR-129 carry the same shape (lines 310-311: `OPEN — deferred post-MVP by recorded scope …`, `OPEN — deferred; applies only to a slice that elects a TUI …`).

**Number-level inside a slice-affecting row (the closer precedent for this packet):** file 08 row **DR-G05 COMPONENT-DELTA**, "Threshold / waiver" cell (line 341): `measurement mandatory, caps deferred by explicit disposition (D-006)`. The disposition itself, COORD `## D-006`, Decision clause 5 (COORD lines 765-774):

> `5. **DR-G05 (component delta):** slice 1 mandates MEASUREMENT AND`
> `   VISIBILITY (download/install/start/RSS delta published per component,`
> `   per platform) with NO numeric cap in this decision — caps become`
> `   product decisions at the first component-acceptance decision under`
> `   DR-G05's own evidence column. **Trigger defined (turn-1 SF-1):**`
> `   since slice 1's TypeScript provider IS a component, that trigger`
> `   fires within slice 1's own qualification cycle — the deferral is`
> `   short-lived by design, and that is recorded here, not discovered`
> `   later.`

DR-115 was afterwards recorded `SATISFIED` under D-056 Class B (COORD `## D-089`: `Record DR-115 SATISFIED for architecture-preview condition 2. Measurement remains condition 4 / DR-G01..G05 / DR-012.`). That is the only such precedent the packet found (search: `grep -n -i "deferred by explicit disposition\|caps deferred"` on file 08 returns only line 341; `grep -c "explicit disposition"` on COORD returns 1) — a number-deferral-by-disposition coexisting with a later SATISFIED.

Caution the record imposes on that precedent: D-056's gates require that the remainder is "only execution / measurement" and is "already named at a condition-4 / DR-G* obligation with an owner" (COORD `## D-056`, Decision bullet). DR-G05's cap sits at a named gate with an owner (`Component publisher + release`, line 341). Whether an OD-112 / DR-111 / DR-126 number can be parked the same way depends on whether it can be routed to a named, owned condition-4 obligation — that mapping is **not in the record** for any of the four items; see §6 open questions.

### 0.3 Why the four items cannot be settled by rule

**COORD `## D-006`, Decision type bullet:** `PREFERENCE-LADEN (route C). Numbers are not derivable from any rule; the register says so ("numeric open"). Decided on the user's behalf; overturn is one supersession line + one revert.`

**COORD `## D-000`, clause 5:** `Decisions that turn on the user's preferences rather than on judgment are additionally marked `PREFERENCE-LADEN`, and their overturn procedure is written to cost less than the decision did.`

**COORD `## D-001`, "Condition 2 — all 29 rows classified (MF-5 closed the DR-108 gap)":** `product decisions (route C, PREFERENCE-LADEN): DR-104, DR-115, DR-116, DR-117, DR-118, DR-119, DR-123, DR-128, DR-129. Rule-governed architecture authoring with review: DR-101, DR-102, DR-103, DR-105, DR-107 (+DR-G18), DR-110, DR-111, DR-112, DR-114, DR-120, DR-121, DR-122, DR-125, DR-126, DR-127.` — DR-118 is classed route C; DR-111/DR-112/DR-126 are classed rule-governed as rows, but every join below records their reserved numbers/tables as "not-capable-of-riding" leftover-design (quoted per item).

**D-056 five eligibility gates** (COORD `## D-056`, Decision bullet): `(Class A T2-02 contract or Class B DECIDED-V1-NOT-INTEGRATED; remainder is only execution / measurement; remainder already named at a condition-4 / DR-G* obligation with an owner; dedicated later SATISFIED-GRADE review; MF-6 that records SATISFIED and removes the cell-level execution/measurement bar)`.

**D-056 turn-2 subject, `## Decision` item 5** (draft lines 186-190): `Authoring fixtures and harness *specifications* remains lawful design work now. Execution remains qualification.` — the signed-index v4 and platform-tcb v9 joins cite this as `D-056 Decision clause 5`; the language-quality v5 join as `(D-056 Decision 5)`; the compatibility v2 join does not cite it.

### 0.4 Slice membership (all four rows are in the affected set)

**COORD `## D-002`, "Condition-2 affected-row set under this slice":** `DR-101, DR-102, DR-103, DR-104, DR-105 (…), DR-107, DR-111, DR-112, DR-114, DR-115, DR-117 (…), DR-118 (TypeScript role), DR-119, DR-120, DR-121, DR-122, DR-123, DR-124 (touched classes), DR-125, DR-126, DR-127.` — So none of the four can leave Condition 2 by silence; any deferral of a row or a number is a recorded disposition (D-001, quoted in §0.1).

### 0.5 Two recording shapes the record already uses for owner decisions

- **User-made, recorded verbatim:** COORD `## D-132`, Status bullet: `Made directly by the user in conversation. Same class as D-000 / D-054: the grant is the user's decision, recorded verbatim rather than made on their behalf. No subagent review of this entry is required. Later process acts this grant names still require their own D-000 cycles.` Decision type: `PREFERENCE-LADEN user amendment. Route C under D-037 clause 3.`
- **Decided on the user's behalf under D-000 review:** COORD `## D-006` (quoted in §0.3), three-turn adversarial consensus.

`DECISIONS-NEEDED.md` (preamble) says the orchestrator "will turn each answer into a D-000 cycle (dual adversarial review) and record it." Which shape applies is the owner's call; the skeletons in §1–§4 are written in the D-006/D-280 bullet form and can be relabelled to the D-132 form.

---

## 1. C1 — DR-112 signed-index: OD-112-1..4

### 1.1 File 08 row (line 294, verbatim)

> `| DR-112 | Signed-index refresh, expiry, last-known revocation, quorum loss, root recovery, emergency running-component policy | Security + operations | [Security](03-configuration-and-security.md) | Reviewed state machine, air-gap/removable-media fixtures, recovery ceremony, audit/waiver expiry | OPEN | Hard blocker |`

- **Owner / decision authority cell:** `Security + operations`
- **Status cell:** `OPEN`
- The cell fragment that reserves the values is `audit/waiver expiry` together with `quorum loss` and `last-known revocation` in the Decision cell; the row itself carries no numbers. The reservation is written in the accepted contract (§1.3), not in the row.
- Related gate row **DR-G08 TRUST-RECOVERY** (line 344): Owner `Security + release`; Threshold / waiver cell `pass all safety cases`; Status `OPEN`.
- Gate-table preamble (lines 332-333): `Waivers require product and release authority, an expiry, a measured residual, and cannot waive an inherited semantic/trust blocker.`

### 1.2 Current leftover-join holding the values RESERVED

`docs/coop/artifacts/signed-index-leftover-join.v4.json` — sha256 `ae5176e2a420be75b8aade77e7f265bc411968a75a35647ae01bfc708835a174`; `"version": 4`; `"date": "2026-08-24"`; `"status": "CANDIDATE-NOT-APPLIED"`; `"file08StatusToken": "OPEN"`; `"head": "28b79e14cb8e69c2ea4b7b446bf71ca8f0088114"`; `file08Pin.sha256` = `e503b75b…` (matches live file 08).

Recorded by **COORD `## D-280 — Record signed-index leftover-join.v4 as DR-112 leftover remasurement`** (`ADOPTED 2026-08-24`, Stage A `Claude ACCEPT` `1ff13ff4…` 0/0; `Codex ACCEPT` `581cf063…` 0/0; Status: `Turn 1 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX.`). D-280 Decision: `leftover-design of OBL-G08-FX-AUTHORING and OBL-RESERVED-NUMBERS remains on leftover-join.v4.` … `Does not mint reserved numbers.`

Obligation, verbatim (`obligations[5]`):

```
"id": "OBL-RESERVED-NUMBERS",
"leftoverDesign": true,
"existingGate": "none",
"executionObligationOwnerToday": "none",
"rideStanding": "not-capable-of-riding",
"reason": "D-105 records quorum, clock/freshness, emergency, and waiver numbers remain RESERVED. G08 occupancy reservedNumbersRemainReserved names OD-112-1..OD-112-4 verbatim. Undecided numbers are leftover-design (D-056). This join does not mint those numbers and does not invent a recovery ceremony implementation. g08 leftover-join.v4 leftoverDesign is [OBL-G08-FX-AUTHORING] and does not steal OBL-RESERVED-NUMBERS. This join does not close it."
```

`reservedNumbersVerbatim` (top-level field of the join):

```
"OD-112-1": "Quorum / threshold cardinality. RESERVED. Named. Not minted.",
"OD-112-2": "Clock skew and last-known-revocation freshness floors. RESERVED. Named. Not minted.",
"OD-112-3": "Emergency running-component / break-glass permission to continue a REVOKED component. RESERVED. Preview refuse. Not minted.",
"OD-112-4": "G08 waiver duration. RESERVED to product/release. Named as an expiry-bearing waiver, not a number. Waiver rule remains pass all safety cases."
```

`summary.leftoverDesign` = `["OBL-G08-FX-AUTHORING", "OBL-RESERVED-NUMBERS"]` (the first is fixture authoring — Packet D scope, not this packet). `proposedLaterWork[2]`: `A later product/release act may set quorum, clock, emergency, or waiver numbers. This join does not mint those numbers.`

The same four strings are carried by the current G08 occupancy `docs/coop/artifacts/harness.DR-G08.trust-recovery.install-surfaces.v3.json` (sha256 `13076be20e4eef0dfe352786b705de09304a69f583529502388e5086f6f098c0`, recorded D-211) at `reservedNumbersRemainReserved.OD-112-1..4`, with `proposedLaterWork[6]`: `A later product/release act may set OD-112-1..4. This v3 occupancy does not mint those numbers.` and `failsIf[22]`: `a quorum, clock, waiver, or ceremony number is invented`.

### 1.3 Where the reservation originates (accepted contract)

`docs/coop/artifacts/signed-index-trust-contract.v8.json` — sha256 `fc171321e969c74464dbc9ff67edd9b874aac1d1c7375c7dc8e431469442efe0`; recorded by **COORD `## D-105`** (`ADOPTED 2026-08-14`; `Claude … ACCEPT-WITH-ADVISORIES, 0 blockers, 0 SHOULD-FIX. Codex … ACCEPT, 0 blockers, 0 SHOULD-FIX.`). D-105 Decision: `Quorum, clock/freshness, emergency, and waiver numbers remain RESERVED. Repair-media remains DR-110. Newly-revoked replay remains DR-113.`

`namedOpenDecisions` (verbatim):

| id | decision | standing |
|---|---|---|
| `OD-112-1` | `Quorum / threshold cardinality` | `RESERVED. Named. Not minted.` |
| `OD-112-2` | `Clock skew and last-known-revocation freshness floors` | `RESERVED. Named. Not minted.` |
| `OD-112-3` | `Emergency running-component / break-glass permission to continue a REVOKED component` | `RESERVED. Preview refuse. Not minted.` |
| `OD-112-4` | `G08 waiver duration` | `RESERVED to product/release. Named as an expiry-bearing waiver, not a number.` |

### 1.4 Candidate values proposed anywhere in the record

**None in the record.** Evidence: `grep -n "OD-112" COORD` returns one line (9341, inside a "does not mint OD-112-1..4" sentence); searches of COORD for `quorum` with an `N-of-M` / `quorum size N` / `threshold of N` pattern, and for `clock skew` / `clock-skew` with a time quantity, return nothing. The contract's fixture class `FC-QUORUM` says of itself: `The fixture names the reserved knob; it does not invent the number as decided.`

### 1.5 Constraints the record imposes on the values (verbatim)

- **OD-112-1 (threshold) is used in two places** — trust entry and recovery commit — and the contract binds both to the same open decision:
  - `trustPolicyShape.requiredOnEveryTrustedEntry[3]`: `thresholdEvaluation: observed signers meet the reserved threshold parameter (value still OD-112-1)`
  - `recoveryAuthorityShape.requiredOnRecoverCommit[3]`: `recoveryAuthorityThreshold: observed recovery signers meet the reserved recovery threshold (value still OD-112-1)`
  - `recoveryAuthorityShape.standing`: `SHAPE ONLY. No quorum, participant list, or officer is minted (OD-112-1 remains RESERVED).`
  - `recoveryCeremony.doesNotMint`: `Quorum size, participant list, break-glass officer, or waiver duration.`
  - `machine.states[4]` `ST-QUORUM-LOST` `means`: `Observed signer set is below the reserved threshold. No new admission.`
  - `machine.transitions[13].guard`: `ACCEPT the observation. Still-below stays. Restored quorum also stays: leaving ST-QUORUM-LOST requires an ordinary payload refresh, not this event.`
  - Whether recovery threshold and ordinary threshold must be the same number is **not in the record** (both say "value still OD-112-1").
- **OD-112-2 (skew / freshness):**
  - `trustPolicyShape.requiredOnEveryTrustedEntry[4]`: `expiryAndFutureTime: not expired; not issued unreasonably in the future (skew reserved)`
  - `trustPolicyShape.requiredOnEveryTrustedEntry[5]`: `revocationFreshness: last-known revocation is inside the reserved freshness floor`
  - `trustPolicyShape.standing`: `SHAPE ONLY. No quorum, skew, or freshness NUMBER is minted (OD-112-1, OD-112-2 remain RESERVED).`
  - `machine.states[3].means`: `Last-known revocation is older than the reserved freshness floor.`
  - `machine.events[1]` `EV-CLOCK` `means`: `A host clock observation is recorded. Clock authority is this row's; untrustworthy clock cannot silently extend expiry.`
  - Whether "floors" means one number or two (skew vs freshness) — the id text says `Clock skew and last-known-revocation freshness floors` (plural); the record does not fix the cardinality of values behind OD-112-2.
- **OD-112-3 (emergency / break-glass):**
  - `offlineRunningPolicy.totalDecision[4].alreadyRunning`: `refuse unless OD-112-3 is later numbered; preview refuse`
  - G08 occupancy v3 `connectivityClasses[1].exactByteIntent`: `OD-112-3 remains RESERVED; preview refuse on a REVOKED component.`
  - Note the record's word is "numbered" although the decision is a permission; whether OD-112-3 is a duration, a policy token, or a refusal-forever is **not in the record**.
- **OD-112-4 (G08 waiver duration):**
  - `auditAndWaiver.waiverExpiry`: `Gate-waiver duration is product/release authority per the file 08 gate preamble. This artifact requires that any waiver of G08 carry an expiry and an audit record. It does not mint the duration.`
  - File 08 line 332-333 (quoted §1.1): waivers need `product and release authority, an expiry, a measured residual`, and `cannot waive an inherited semantic/trust blocker`.
  - DR-G08 row waiver cell: `pass all safety cases`; G08 occupancy v3 `passProperty`: `Waiver of a safety case is not a skipped cell; the waiver rule is pass all safety cases. Waiver duration remains OD-112-4 RESERV…`
  - So OD-112-4 is authority-split: the row owner is `Security + operations` but the contract and join both say `RESERVED to product/release`.
- **Not this row (do not set here):** `Repair-media remains DR-110. Newly-revoked replay remains DR-113.` (D-105).

### 1.6 Fill-in form — DR-112

| Field | Your entry |
|---|---|
| OD-112-1 quorum / threshold cardinality — ordinary TRUSTED entry | ☐ value: ______ (form: N-of-M? the record does not fix the form) ☐ defer by explicit disposition (trigger: ______) |
| OD-112-1 — recovery-commit threshold | ☐ same as above ☐ different value: ______ ☐ defer |
| OD-112-2 clock skew ("not issued unreasonably in the future") | ☐ value: ______ ☐ defer (trigger: ______) |
| OD-112-2 last-known-revocation freshness floor | ☐ value: ______ ☐ defer (trigger: ______) |
| OD-112-3 emergency / break-glass on a REVOKED component | ☐ keep `preview refuse` as the decided answer (permanent refuse) ☐ permit under conditions: ______ ☐ defer (trigger: ______) |
| OD-112-4 G08 waiver duration | ☐ value: ______ (must carry expiry + audit + measured residual) ☐ defer to product/release act (trigger: ______) |
| Recording shape | ☐ user-made verbatim (D-132 form) ☐ D-000 cycle on my behalf (D-006 form) |
| If deferring: where the number rides | name the condition-4 / DR-G* obligation and owner (D-056 gate 3): ______ |

**Orchestrator recommendation (non-binding):** the record already contains a lawful, reviewed shape for parking a number with a trigger (D-006 clause 5); if you do not have values in hand today, a disposition in that shape for each OD-112-n, naming the trigger and the owning gate, is the cheapest recordable answer. Setting OD-112-3 as "preview refuse stands" would convert a reservation into a decision without inventing a number.

### 1.7 COORD-entry skeleton (DRAFT — not recorded, values in ⟨⟩)

```
## D-⟨NNN⟩ — DR-112: set OD-112-1..4 ⟨or: record explicit deferral disposition for OD-112-1..4⟩

- **Date:** ⟨YYYY-MM-DD⟩
- **Status:** ⟨ADOPTED …; either "Made directly by the user in conversation … recorded verbatim" (D-132 form) or "Turn k of 3: CONSENT from both independent reviewers …" (D-006 form)⟩
- **Decision type:** PREFERENCE-LADEN (route C). Numbers are not derivable from any rule (D-006). Does not mark SATISFIED. Does not edit file 08. Does not coin a token.
- **Subject:** `docs/coop/artifacts/signed-index-trust-contract.v8.json` `fc171321…` namedOpenDecisions OD-112-1..4; current DR-112 leftover-join `signed-index-leftover-join.v4.json` `ae5176e2…` (D-280) obligation OBL-RESERVED-NUMBERS; G08 occupancy v3 `13076be2…` reservedNumbersRemainReserved.
- **Decision:**
  OD-112-1 = ⟨value | DEFERRED by explicit disposition: trigger ⟨…⟩, rides at ⟨DR-G08 / owner⟩⟩ — applies to both thresholdEvaluation and recoveryAuthorityThreshold ⟨or: recovery threshold = ⟨value⟩⟩.
  OD-112-2 = skew ⟨value⟩; last-known-revocation freshness floor ⟨value⟩ ⟨or DEFERRED …⟩.
  OD-112-3 = ⟨"preview refuse" confirmed as the decision | permitted under ⟨conditions⟩ | DEFERRED …⟩.
  OD-112-4 = ⟨duration⟩ ⟨set by product/release per the file 08 gate preamble; expiry + audit record + measured residual required⟩ ⟨or DEFERRED …⟩.
  Repair-media remains DR-110. Newly-revoked replay remains DR-113. Does not author G08 fixtures (OBL-G08-FX-AUTHORING stays leftover-design). Does not SATISFY DR-112. Does not open D-056 Class A. Does not authorize `docs/v2/implementation/`.
- **Successor work this entry names (separate cycles):** signed-index leftover-join.v5 remasuring OBL-RESERVED-NUMBERS to leftoverDesign ⟨false | deferred-or-rides-elsewhere⟩; G08 occupancy v4 carrying the values; contract successor v9 if the reviewers require the values in the contract bytes.
- **Readiness effect:** Zero SATISFIED at adoption. Condition 2 stays 5 of 32. Condition 5 last.
- **Reversibility:** Total before any dependent leftover-join or SATISFIED re-record. Overturn: one supersession line + revert of C-D⟨NNN⟩.
- **Commit:** C-D⟨NNN⟩.
```

---

## 2. C2 — DR-118 language-quality: per-row thresholds, matrix/corpus acceptance, G13 reserved

### 2.1 File 08 row (line 300, verbatim)

> `| DR-118 | Language-native analysis quality and supported language/tooling roles | Product + language architecture owners | [Language-native quality](02-distribution-and-components.md#language-native-product-quality); acceptance structure at `COORDINATOR-DECISIONS.md` D-007 (adversarial consensus, CONSENT `1fbbce62…`) | Product-selected role list; per-role capability/parity matrix; language-specific semantic/graph goldens; behavior/performance baseline; known limitations; explicit no-silent-fallback tests | **DECIDED-V1-NOT-INTEGRATED** — role list DECIDED (D-002: TypeScript, sole slice-1 role) and acceptance STRUCTURE decided (D-007: role × capability × platform matrix with manifest-boundary rows, known-limitations-as-claim, behavior AND performance baselines against the pinned prototype with the lawful replacement path, DR-006 identity/Coverage rides named with prose-never-settles, five-member no-silent-fallback negative-test class); **per-row thresholds remain UNDECIDED** (unlike DR-115) — product approvals at matrix acceptance; the matrix/corpus evidence half discharges at DR-G13/G14 qualification | Hard blocker for every slice-1 language role; does not mandate implementation language |`

- **Owner / decision authority cell:** `Product + language architecture owners`
- **Status cell lead label:** `**DECIDED-V1-NOT-INTEGRATED**`; the reserving fragment: `**per-row thresholds remain UNDECIDED** (unlike DR-115) — product approvals at matrix acceptance`.

**Gate row DR-G13 LANGUAGE-QUALITY** (line 349, verbatim):

> `| DR-G13 LANGUAGE-QUALITY | Each supported language/tooling role delivers language-native quality rather than a lowest-common-denominator abstraction | reserved, not named (blocked on DR-118; D-086; zero C4 progress). future product-selected role × platform × digest-pinned corpus matrix; no such accepted corpus/measurement manifest exists in this V2 snapshot | capability/parity matrix, exact corpus/golden digests, quality/performance measurements, limitations, and fallback-refusal cases | Product + language owners | OPEN FUTURE ACCEPTANCE EVIDENCE; not QUALIFIED | threshold/parity decision per role; semantic degradation has no silent waiver | OPEN |`

- G13 Owner cell: `Product + language owners`. COORD `## D-086`: `G13 is reserved behind DR-118.`
- Gate row DR-G14 (line 350) Owner cell: `Product + language + release + security`.

### 2.2 Current leftover-join holding the values RESERVED

`docs/coop/artifacts/language-quality-leftover-join.v5.json` — sha256 `e12101736f9a320a06a3311f405981801fad73c42ba9b7537f506e6c4859bd53`; `"version": 5`; `"date": "2026-08-24"`; `"status": "CANDIDATE-NOT-APPLIED"`; `"file08StatusToken": "DECIDED-V1-NOT-INTEGRATED"`; `"head": "438b2b820ff6c8c683c56c74006973de186f0e69"`; `file08Pin.sha256` = `e503b75b…`.

Recorded by **COORD `## D-273 — Record language-quality leftover-join.v5 as DR-118 leftover remasurement`** (`ADOPTED 2026-08-24`; Stage A `Claude ACCEPT` `f1dc8c40…` 0/0, `Codex ACCEPT` `eae8cdc3…` 0/0; `New cycle after CONTESTED D-272. Not a fourth turn.`). D-273 Decision: `leftover-design of OBL-THRESHOLDS, OBL-MATRIX-CORPUS, and OBL-G13-RESERVED remains on leftover-join.v5.` (D-272 on the same subject is CONTESTED — DECISIONS-NEEDED A1.)

Three obligations, verbatim:

```
"id": "OBL-THRESHOLDS", "leftoverDesign": true, "existingGate": "none",
"executionObligationOwnerToday": "none", "rideStanding": "not-capable-of-riding",
"reason": "D-007 item 7 / D-056 / D-113 / file 08: per-row thresholds remain UNDECIDED. Undecided numbers are leftover-design. Parity-or-improvement is a product approval at matrix acceptance. This join does not invent numbers."

"id": "OBL-MATRIX-CORPUS", "leftoverDesign": true, "existingGate": "none as authored implementations",
"executionObligationOwnerToday": "none", "rideStanding": "not-capable-of-riding as execution-only remainder",
"reason": "D-007: the matrix and corpus are acceptance evidence authored during qualification. D-113 / file 02: no digest-pinned quality corpus or accepted measurement manifest exists. Authoring remains design work (D-056 Decision 5). This join does not author that corpus. Matrix authoring waits on DR-125 closure or disposition (OBL-DR125-ACTIVATION)."

"id": "OBL-G13-RESERVED", "leftoverDesign": true, "existingGate": "DR-G13 reserved, not named",
"namedIdentifiersNotAuthored": [], "executionObligationOwnerToday": "none", "rideStanding": "not-capable-of-riding",
"reason": "File 08 / D-086: G13 is reserved, not named, blocked on DR-118. Zero C4 progress. Naming G13 into required-now is a later scoped D-002 successor and a D-086 successor in the same act. This join assigns no number and does not invent a harness specification. Live required-now remains 28 without G13."
```

`summary.leftoverDesign` = `["OBL-THRESHOLDS", "OBL-MATRIX-CORPUS", "OBL-G13-RESERVED"]`; `summary.classBTokenPresent` = `true`; `summary.classBSatisfiedNotOpened` = `true`. `proposedLaterWork`:

> `"A later D-000 cycle may product-approve per-row thresholds at matrix acceptance. This join invents no numbers."`
> `"A later D-000 cycle may author the digest-pinned matrix and corpus only after DR-125 closes or is disposed. This join does not author those bytes and does not apply D-110."`
> `"A later act that names G13 into required-now is a scoped D-002 successor and a D-086 successor in the same act. This join assigns no number."`

### 2.3 Where the reservation originates

**COORD `## D-007`, Decision item 7** (lines 882-884): `7. **Thresholds:** parity-or-improvement per row is a PRODUCT approval at matrix acceptance (the DR-115 pattern); no row ships with a silent regression against its stated baseline.` Item 9: `PER-ROW THRESHOLDS REMAIN UNDECIDED (unlike DR-115, whose numbers were decided); the matrix/corpus evidence half discharges at DR-G13/G14 qualification.` Alternatives: `THRESHOLDS-NOW was rejected — no measured denominator exists pre-blueprint, and inventing numbers would repeat the class D-006's reviewer struck (a threshold whose runner/workload is unnamed measures nothing). Either remains reachable by successor decision.`

**Accepted contract** `docs/coop/artifacts/language-quality-matrix-contract.v13.json` — sha256 `9efffdb3f7ec806bc967db5eff5868aea0a7d11524b1e026993a46505d35c2ae`; recorded **COORD `## D-113`** (`ADOPTED 2026-08-15`; dual `ACCEPT, 0 blockers, 0 SHOULD-FIX`). D-113 Decision: `Numeric thresholds remain UNDECIDED (D-007). The matrix/corpus is not authored. … D-056 Class B remains ineligible while thresholds are UNDECIDED.`

- `thresholds.standing`: `UNDECIDED / RESERVED`
- `thresholds.rule`: `Parity-or-improvement per row is a PRODUCT approval at matrix acceptance (the DR-115 pattern of product-owned numbers, not the D-006 numbers themselves). No row ships with a silent regression against its stated baseline (D-007 item 7).`
- `thresholds.whyNoNumbersHere`: `D-007 rejected THRESHOLDS-NOW: no measured denominator exists pre-blueprint, and inventing numbers would repeat the class D-006's reviewer struck (a threshold whose runner/workload is unnamed measures nothing).`
- `rowFields.required[7]`: `threshold cell (RESERVED; product-approved at matrix acceptance; no silent regression against the stated baseline)`
- `matrixShape.shape`: `role x capability x platform`; `matrixShape.illustrativeFloor`: `["parse fidelity", "semantic resolution", "graph construction", "finding classes", "output projections"]` — labelled `an ILLUSTRATIVE FLOOR, not a closed vocabulary`.
- `matrixShape.dr125ActivationGate`: `OPEN. Owner: DR-125. Divergence owner: the DR-125 successor, not this artifact. Matrix authoring waits on that closure or its disposition.`
- `corpusDiscipline.rule`: `Digest-pinned per file, product-approved before any measurement claim, versioned by supersession. EIR measured-or-cited-at-digest applies to every cell (D-007 item 4).`; `corpusDiscipline.standing`: `No digest-pinned quality corpus or accepted measurement manifest exists in this V2 snapshot (file 02). This artifact does not author one.`
- `g13g14.g13`: `harness.DR-G13 reserved, not named (blocked on DR-118; D-086). Naming here does not author the harness.`
- `g13g14.evidenceRemainder`: `Matrix/corpus evidence discharges at DR-G13/G14 qualification after product-approved thresholds exist.`

### 2.4 Candidate values proposed anywhere in the record

**None in the record.** No per-row threshold number, no matrix row list beyond the `illustrativeFloor` above, and no corpus file list appears in COORD or the artifacts cited here. The record's own reason for the absence is quoted above (`no measured denominator exists pre-blueprint`).

### 2.5 Constraints (verbatim, beyond §2.3)

- Row set is not closed: `capabilityBoundary`: `One row per capability the role's component manifest advertises, derived from the host-contract capability declaration (DR-125). DR-125 is OPEN. That closure is an activation gate for matrix authoring (D-007 OBS-D007-T2-02)`. So per-row thresholds cannot be enumerated row-by-row until DR-125 closes or is disposed — the join records this as `OBL-DR125-ACTIVATION` (`deferredOrRidesElsewhere`).
- Baseline referent: file 08 row: `behavior AND performance baselines against the pinned prototype with the lawful replacement path`.
- Threshold semantics are fixed as a floor form: `parity-or-improvement per row`; `no row ships with a silent regression against its stated baseline`.
- G13: `threshold/parity decision per role; semantic degradation has no silent waiver` (file 08 line 349, Threshold / waiver cell). Naming G13 requires `a scoped D-002 successor and a D-086 successor in the same act` (join reason; contract `g13g14`).
- Class B path: D-113 `D-056 Class B remains ineligible while thresholds are UNDECIDED.`

### 2.6 Fill-in form — DR-118

| Field | Your entry |
|---|---|
| Per-row threshold rule | ☐ set numbers now (list rows and values: ______) ☐ confirm "parity-or-improvement per row, product-approved at matrix acceptance" as the decided rule and record an explicit deferral of numeric values to matrix acceptance (trigger: DR-125 closure/disposition + first matrix submission) ☐ other: ______ |
| Matrix row vocabulary | ☐ adopt the five-area illustrative floor as the slice-1 row set now ☐ wait for DR-125 (record as deferral) ☐ other: ______ |
| Corpus acceptance | ☐ name the digest-pinned corpus source now: ______ ☐ defer to qualification with the D-007 item-4 discipline as the rule |
| G13 gate | ☐ leave `reserved, not named` (state explicitly) ☐ direct a scoped D-002 successor + D-086 successor naming `harness.DR-G13.…` into required-now (changes required-now from 28) |
| Recording shape | ☐ user-made verbatim (D-132 form) ☐ D-000 cycle (D-006 form) |

**Orchestrator recommendation (non-binding):** the record's own rejection of THRESHOLDS-NOW (D-007) still holds — no measured denominator exists — so an explicit deferral disposition that names the trigger (DR-125 closure/disposition, then matrix acceptance) and confirms the parity-or-improvement rule as decided is the option consistent with the bytes; setting numbers today would require a successor to D-007's alternatives text.

### 2.7 COORD-entry skeleton (DRAFT)

```
## D-⟨NNN⟩ — DR-118: per-row threshold disposition, matrix/corpus acceptance route, G13 standing

- **Date:** ⟨YYYY-MM-DD⟩
- **Status:** ⟨ADOPTED …; D-132 form or D-006 form⟩
- **Decision type:** PREFERENCE-LADEN (route C; D-001 classes DR-118 as a product decision). Does not mark SATISFIED. Does not edit file 08. Does not name G13 ⟨unless the G13 line below says otherwise⟩.
- **Subject:** `language-quality-matrix-contract.v13.json` `9efffdb3…` (D-113) thresholds / rowFields.required[7] / matrixShape / corpusDiscipline; current DR-118 leftover-join `language-quality-leftover-join.v5.json` `e1210173…` (D-273) obligations OBL-THRESHOLDS, OBL-MATRIX-CORPUS, OBL-G13-RESERVED.
- **Decision:**
  Thresholds: ⟨per-row values ⟨list⟩ | the rule "parity-or-improvement per row; no silent regression against the stated baseline" is DECIDED; numeric values are DEFERRED by explicit disposition to matrix acceptance, trigger ⟨DR-125 closure or disposition, then first matrix submission⟩, product approval by ⟨Product + language architecture owners⟩⟩.
  Matrix rows: ⟨adopt illustrative floor ⟨five areas⟩ as slice-1 rows | DEFERRED to DR-125 activation⟩.
  Corpus: ⟨source ⟨…⟩ digest-pinned per file | DEFERRED to qualification under D-007 item 4 discipline⟩.
  G13: ⟨remains reserved, not named; required-now stays 28 | to be named by a scoped D-002 successor and a D-086 successor in one later act⟩.
  Does not author the matrix or corpus. Does not SATISFY DR-118. Does not open D-056 Class A or record Class B. Does not authorize `docs/v2/implementation/`.
- **Successor work this entry names:** language-quality leftover-join.v6 remasuring OBL-THRESHOLDS ⟨and OBL-MATRIX-CORPUS⟩ standing; contract v14 if reviewers require the disposition in the artifact bytes.
- **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32. Required-now stays 28 ⟨unless G13 is named⟩. Condition 5 last.
- **Reversibility:** one supersession line + revert of C-D⟨NNN⟩. Does not overturn D-002, D-007, D-113.
- **Commit:** C-D⟨NNN⟩.
```

---

## 3. C3 — DR-111 compatibility: numeric reader-support windows

### 3.1 File 08 row (line 293, verbatim)

> `| DR-111 | Separate compatibility windows for core/index/control, each provider major, component API, state schema, and evidence formats | Versioning authority | [Operations](04-lifecycle-delivery-and-operations.md) | Per-surface matrices and cross-version conformance; no shared same-version assumption | OPEN | Hard blocker |`

- **Owner / decision authority cell:** `Versioning authority`
- **Status cell:** `OPEN`
- The row's Decision cell names the surfaces (`core/index/control, each provider major, component API, state schema, and evidence formats`) but no numbers; the reservation lives in the contract (§3.3).

### 3.2 Current leftover-join holding the values RESERVED

`docs/coop/artifacts/compatibility-leftover-join.v2.json` — sha256 `33e4299d7f65bf37c2f5d54193e004c69d542d3f5da99417e1360efc2f8b7259`; `"version": 2`; `"date": "2026-08-21"`; `"status": "CANDIDATE-NOT-APPLIED"`; `"file08StatusToken": "OPEN"`; `"head": "f76aa872d91e071c83bd7b03dd650402518eda64"`; **`file08Pin.sha256` = `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1`** — that was the live file 08 when D-177 was recorded (file 08 at commit `892236a`, `2026-08-20 D-169`; D-177 committed `afb115d`, 2026-08-21). File 08 has moved exactly once since — commit `fc688b1` (`2026-08-23 D-236: record DR-104 SATISFIED under D-056 Class B`), producing the live `e503b75b…`. COORD contains no later compatibility-leftover-join recording (the only post-D-177 mention of DR-111 is D-181's "not steal DR-111, DR-118, or DR-127 leftover"). So v2 is the current DR-111 join by recording, and it is the one of the four joins in this packet whose file-08 pin is one edit behind the live register. (Flagged in §6.)

Recorded by **COORD `## D-177 — Record compatibility-leftover-join.v2 as DR-111 leftover remasurement`** (`ADOPTED 2026-08-21`; Stage A `Claude ACCEPT` `a0cef800…` 0/0, `Codex ACCEPT` `ba6c178b…` 0/0). D-177 Decision: `leftover-design of OBL-NUMERIC-WINDOWS and OBL-LOCK-JOIN remains. D-056 Eligibility gates 2 and 3 do not hold for DR-111. … Does not invent numeric windows. Does not produce a lock.`

Obligations, verbatim:

```
"id": "OBL-NUMERIC-WINDOWS", "leftoverDesign": true, "existingGate": "none",
"executionObligationOwnerToday": "none", "rideStanding": "not-capable-of-riding",
"reason": "v5 numericWindows is RESERVED: 'This artifact does not mint how long a reader is supported. Product/versioning sets numbers later. Alias-window numbers are D-012's, not this row's.' Undecided numbers are leftover-design (D-056). This join does not invent those numbers."

"id": "OBL-LOCK-JOIN", "leftoverDesign": true, "existingGate": "none on DR-111. Consumed later on DR-103.",
"executionObligationOwnerToday": "none on this row alone", "rideStanding": "not-capable-of-riding",
"reason": "v5 lockJoin PROPOSES that no lock of any form is producible until this row closes with evaluable windows, and that a later DR-103 successor would consume those windows. Evaluable windows wait on OBL-NUMERIC-WINDOWS. This join does not invent window numbers, does not emit a lock, and does not retarget DR-103."
```

Top-level `numericWindowsVerbatim`: `RESERVED. This artifact does not mint how long a reader is supported. Product/versioning sets numbers later. Alias-window numbers are D-012's, not this row's.` `proposedLaterWork[0]`: `A later product/versioning act may set numeric reader-support windows. This join does not invent those numbers.`

### 3.3 Where the reservation originates

`docs/coop/artifacts/compatibility-matrices-contract.v5.json` — sha256 `d0386cee26d8aafd3d07b46f21352cc3d9d03cdc8f406de0adf571f8c81f7f41`; recorded **COORD `## D-103`** (`ADOPTED 2026-08-14`; dual `ACCEPT, 0 blockers, 0 SHOULD-FIX`). D-103 Decision: `Numeric windows remain RESERVED. S-EVIDENCE remains deferred with DR-113. No lock is producible.`

- `numericWindows`: `RESERVED. This artifact does not mint how long a reader is supported. Product/versioning sets numbers later. Alias-window numbers are D-012's, not this row's.`
- `sixCells`: `["current writer", "supported readers", "migrations/bridges", "future-major refusal", "downgrade/no-return", "test evidence"]`
- Surfaces and their window standing (`surfaces[i].id` / `thisClosure` / `skeleton`):

| id | name | thisClosure | skeleton |
|---|---|---|---|
| `S-CORE` | `distribution core and core state` | `ADMITTED` | `current writer = signed distribution core major as published; numeric windows RESERVED` |
| `S-SCHEMA` | `signed root/index/manifest/lock schemas` | `ADMITTED` | `current writer = DR-103 schema majors; windows RESERVED` |
| `S-CTRL` | `common control protocol` | `ADMITTED` | `consumes control-protocol-contract.v2 row skeleton; window SEMANTICS reserved here` |
| `S-TS1` | `TypeScript provider protocol major 1` | `ADMITTED` | `current writer = applied delivery major 1; windows RESERVED` |
| `S-RUST2` | `Rust merged provider protocol major 2` | `ADMITTED-UNSHIPPED` | `Matrix may exist. Slice 1 does not ship this role (D-002).` |
| `S-ROLE` | `each other component role API/subprotocol` | `RESERVED` | `Cannot invent roles beyond D-002 TypeScript. Additional roles enter by later slice.` |
| `S-STATE` | `component-owned state schema` | `ADMITTED-SCOPED` | (preview ships the rebuildable cache/index and operational-metadata classes …) |
| `S-EVIDENCE` | `evidence/custody/replay formats` | `DEFERRED` | `DR-202 F3: … Named and deferred with DR-113. Not deleted.` |

So the surfaces whose windows this decision would fill are **four** (`S-CORE`, `S-SCHEMA`, `S-TS1` with `windows RESERVED`; `S-CTRL` with `window SEMANTICS reserved`); `S-STATE` carries no window text in its skeleton; `S-RUST2`/`S-ROLE`/`S-EVIDENCE` are unshipped / reserved / deferred by the contract itself.

### 3.4 Candidate values proposed anywhere in the record

**None in the record.** `grep -c -i "numeric window" COORD` = 2, both reservation sentences (D-103 `Numeric windows remain RESERVED.`; D-177 `Does not invent numeric windows.`). No `reader-support` phrase with a duration or a major-count appears in COORD. The only decided window-like number nearby belongs to a different row: **COORD `## D-012`, Decision item 5**: `a rename keeps the old name as a deprecated alias for AT LEAST one minor release cycle AND no fewer than 90 days from the deprecating release, whichever is longer` — and the contract says `Alias-window numbers are D-012's, not this row's.`

### 3.5 Constraints (verbatim)

- `whatThisDoesNotDo[1]`: `Does not fill numeric windows.`; `whatThisDoesNotDo[3]`: `Does not ship Rust major 2 or extra roles in slice 1.`; `whatThisDoesNotDo[4]`: `Does not pull evidence/replay formats into slice 1.`; `whatThisDoesNotDo[5]`: `Does not authorize provider-frame translation as a bridge.`
- `bridgesMean`: `A bridge is a declared, versioned reader or writer adapter owned by the surface's matrix. It MUST NOT wrap, translate, normalize, reorder, reinterpret, merge, or assign new fates to semantic frames of an existing provider protocol (file 02 must-not; D-015 T-3).`
- Row: `no shared same-version assumption` (file 08 Required-acceptance-evidence cell).
- `lockJoin` (contract) / `OBL-LOCK-JOIN` (join): no lock is producible `until this row closes with evaluable windows`; `a later DR-103 successor would consume those windows` — so the values feed DR-103, and DR-103's owner (`Delivery + security`, file 08 line 285) is downstream.
- `S-TS1` current writer is pinned to the applied delivery: `Warrant for S-TS1 current writer = TypeScript provider protocol major 1. Window SEMANTICS still reserved here.` (`recordedInputs.governingSources[11].role`).
- Unit of a "window" (majors? releases? days?) is **not in the record**; the contract's own phrase is `how long a reader is supported`.

### 3.6 Fill-in form — DR-111

| Field | Your entry |
|---|---|
| Window unit | ☐ number of prior majors ☐ number of releases ☐ calendar duration ☐ other: ______ (not fixed by the record) |
| `S-CORE` supported-reader window | ☐ value: ______ ☐ defer (trigger: ______) |
| `S-SCHEMA` window | ☐ value: ______ ☐ defer |
| `S-CTRL` window semantics | ☐ value/rule: ______ ☐ defer |
| `S-TS1` window | ☐ value: ______ ☐ defer |
| `S-STATE` (scoped; no window text in skeleton) | ☐ set: ______ ☐ state explicitly that none is set for slice 1 |
| Deciding authority named in the entry | ☐ `Versioning authority` (file 08 owner cell) ☐ `Product/versioning` (contract wording) ☐ both |
| Precondition: remasure compatibility-leftover-join (v3) to the live file 08 before or with the value act? | ☐ yes ☐ no (see §6) |
| Recording shape | ☐ user-made verbatim ☐ D-000 cycle |

**Orchestrator recommendation (non-binding):** because the record fixes neither the unit nor the surfaces' coupling (whether all four share one window), stating the unit first is what makes any later number evaluable; a deferral without the unit would leave OBL-LOCK-JOIN unevaluable and DR-103's lock rule blocked.

### 3.7 COORD-entry skeleton (DRAFT)

```
## D-⟨NNN⟩ — DR-111: numeric reader-support windows ⟨set | explicit deferral disposition⟩

- **Date:** ⟨YYYY-MM-DD⟩
- **Status:** ⟨ADOPTED …; D-132 form or D-006 form⟩
- **Decision type:** PREFERENCE-LADEN (route C for the numbers; D-001 classes the row itself rule-governed). Does not mark SATISFIED. Does not edit file 08. Does not produce a lock.
- **Subject:** `compatibility-matrices-contract.v5.json` `d0386cee…` (D-103) numericWindows / surfaces S-CORE, S-SCHEMA, S-CTRL, S-TS1; current DR-111 leftover-join `compatibility-leftover-join.v2.json` `33e4299d…` (D-177) obligations OBL-NUMERIC-WINDOWS, OBL-LOCK-JOIN.
- **Decision:**
  Window unit = ⟨…⟩.
  S-CORE supported readers = ⟨value⟩; S-SCHEMA = ⟨value⟩; S-CTRL window semantics = ⟨rule⟩; S-TS1 = ⟨value⟩; S-STATE = ⟨value | none set for slice 1, stated⟩.
  ⟨or: values DEFERRED by explicit disposition; trigger ⟨…⟩; the D-103 lock rule stays "no lock is producible" until then.⟩
  Alias windows remain D-012's. S-EVIDENCE remains deferred with DR-113. S-RUST2 / S-ROLE remain as the contract states. Does not SATISFY DR-111. Does not open D-056 Class A. Does not authorize `docs/v2/implementation/`.
- **Successor work this entry names:** compatibility-leftover-join.v3 pinned to live file 08 `e503b75b…`, remasuring OBL-NUMERIC-WINDOWS ⟨false | deferred⟩ and OBL-LOCK-JOIN; a DR-103 successor consuming evaluable windows (owner Delivery + security).
- **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32. Condition 5 last.
- **Reversibility:** one supersession line + revert of C-D⟨NNN⟩. Does not overturn D-012, D-013, D-103.
- **Commit:** C-D⟨NNN⟩.
```

---

## 4. C4 — DR-126 platform TCB: per-OS allowlist tables, filesystem and version/build selectors

### 4.1 File 08 row (line 308, verbatim)

> `| DR-126 | Platform base/host-ABI TCB and loader closure | Security + release + platform owners | [Exact-byte delivery](04-lifecycle-delivery-and-operations.md#exact-byte-delivery) | Closed OS ABI/loader/libc/framework/cert/font/ICU-class allowlist and identity rules; retained loader traces; undeclared-system-resolution negative tests | OPEN | Hard blocker for platform qualification |`

- **Owner / decision authority cell:** `Security + release + platform owners`
- **Status cell:** `OPEN`
- The reserving fragment in the Required-acceptance-evidence cell: `Closed OS ABI/loader/libc/framework/cert/font/ICU-class allowlist and identity rules`.

**Gate row DR-G22 PLATFORM-ABI-LOADER** (line 358, verbatim):

> `| DR-G22 PLATFORM-ABI-LOADER | Executed closure uses only declared platform TCB dependencies | named: harness.DR-G22.platform-abi-loader (D-086; not authored; not QUALIFIED). supported OS/filesystem/architecture × hostile loader/system library/tool environment | full loader trace, identity/version allowlist, negative undeclared libc/framework/cert/font/ICU/tool resolution and alternate-loader search | Security + release + platform | PROPOSED; not QUALIFIED | pass all declared platforms or remove platform support | OPEN |`

- G22 Owner cell: `Security + release + platform`; waiver cell: `pass all declared platforms or remove platform support`.

### 4.2 Current leftover-join holding the tables RESERVED

`docs/coop/artifacts/platform-tcb-leftover-join.v9.json` — sha256 `1774427e9500940d24f75fbaee622142a8be72547d68a026e18d6e957369e26a`; `"version": 9`; `"date": "2026-08-24"`; `"status": "CANDIDATE-NOT-APPLIED"`; `"file08StatusToken": "OPEN"`; `"head": "1e3e6644edf88fd9a0f11affb1addb70c71393f6"`; `file08Pin.sha256` = `e503b75b…`.

Recorded by **COORD `## D-268 — Record platform-tcb leftover-join.v9 as DR-126 leftover remasurement`** (`ADOPTED 2026-08-24`, turn 2; Stage A `Claude ACCEPT` `408c6fde…` 0/0, `Codex ACCEPT` `1383c328…` 0/0). D-268 Decision: `leftover-design of OBL-G22-FX-AUTHORING and OBL-RESERVED-TABLES remains on leftover-join.v9.` … `Does not populate reserved TCB tables. Does not invent Rosetta. Does not apply TCB v45.`

Obligation, verbatim (`obligations[5]`):

```
"id": "OBL-RESERVED-TABLES", "leftoverDesign": true, "existingGate": "none",
"executionObligationOwnerToday": "none", "rideStanding": "not-capable-of-riding",
"reason": "G22 leftoverNameNote and G22 v1 fields keep per-OS tables, filesystem selectors, version/build selectors, ikconfigParserVectors, and NT-TCB-KEXEC RESERVED. filesystems.standing is RESERVED; matrixStanding is INCOMPLETE on the filesystem selector axis. versionOrBuildSelector.standing is RESERVED; requiredBeforeAllowlistFreeze remains true. v45 whatThisDoesNotDo includes 'Does not populate per-OS allowlist rows.' Undecided tables and selectors are leftover-design (D-056). This join does not populate them and does not freeze an allowlist."
```

`summary.leftoverDesign` = `["OBL-G22-FX-AUTHORING", "OBL-RESERVED-TABLES"]` (the first is fixture authoring — Packet D scope). `proposedLaterWork[2]`: `A later TCB population packet may supply filesystem and version/build selector values. This join does not populate those selectors and does not choose that packet's owner.` The `OBL-G22-FX-AUTHORING` reason also states the coupling: `The filesystem token of that class is the TCB filesystem selector; that axis is RESERVED and is OBL-RESERVED-TABLES, not a populated fixture set.`

### 4.3 Where the reservation originates

**Accepted contract** `docs/coop/artifacts/platform-tcb-contract.v45.json` — sha256 `da87bdb4d100c90e9450fb82744b7d327ae6b7332db550ea808bdbdb0444a7e5`; recorded **COORD `## D-125`** (`ADOPTED 2026-08-15`; dual `ACCEPT, 0 blockers, 0 SHOULD-FIX`). D-125 Decision: `DR-126 stays OPEN. No SATISFIED. G22 is not QUALIFIED. The candidate binds NOTHING.`

- `identityRuleShape.populatedTables`: `Per-OS concrete members are RESERVED as G22 qualification evidence.`
- `taxonomy`: `["OS ABI", "loader", "libc", "framework", "certificate store", "font", "ICU", "comparable system-class dependency"]` (eight classes).
- `whatThisDoesNotDo[1]`: `Does not populate per-OS allowlist rows.`; `[3]`: `Does not re-decide D-006 size numbers.`; `[4]`: `Does not put language-runtime/Node into the core TCB (those are DR-119 component closures).`; `[8]`: `Does not remove linux/x86_64 or linux/arm64 from D-002 slice-1 platforms. A machine that cannot produce measuredBootBind fails qualification; the platform class remains.`
- `platformProfile.selectorGrammar.requiredMembers`: `["osFamily", "architecture", "supportedVersionOrBuildSelector", "filesystemWhereItAffectsResolution"]`
- `platformProfile.selectorGrammar.beforeAllowlistFreeze`: `Every required member MUST be populated. Partial preview identity is osFamily+architecture only and cannot freeze an allowlist.`
- `platformProfile.slice1ProfileStems` — four stems, each with both selectors `"standing": "RESERVED", "requiredBeforeAllowlistFreeze": true`:
  - `{"osFamily": "macos", "architecture": "arm64", …, "filesystemWhereItAffectsResolution": {…, "mustNot": "apfs-or-hfs-plus as a single value"}}`
  - `{"osFamily": "macos", "architecture": "x86_64", …}`
  - `{"osFamily": "linux", "architecture": "x86_64", …}`
  - `{"osFamily": "linux", "architecture": "arm64", …}`
- `platformProfile.populationPacket`: `A later packet that supplies these selectors is a different artifact. Standing remains RESERVED. requiredBeforeAllowlistFreeze remains true. This contract authors the grammar, including version/build and filesystem selectors, and does not populate them. This row does not name, designate, or claim independent review of that later packet. Choosing its owner is a separate decision. Windows remains D-002 absent.`
- `g22.ikconfigParserVectors`: `RESERVED as G22 evidence. vectorRosterRule is GOVERNING: …`

**Current G22 occupancy** `docs/coop/artifacts/harness.DR-G22.platform-abi-loader.v2.json` — sha256 `2973cda2adac1b612c084b64606e4fc5b5ed5b78317fc64780a7311172ff1307` (recorded D-219 per the join):
- `filesystems.standing`: `RESERVED`; `filesystems.matrixStanding`: `INCOMPLETE on the filesystem selector axis until that later packet supplies values.`
- `filesystems.laterAct`: `A later population packet (TCB v45 populationPacket) supplies selector values. That packet is a different artifact. This specification does not name, designate, or claim independent review of that packet. Choosing its owner is a separate decision. That act is not leftover-design closed here and is not the G07 supported-filesystem coverage-domain act.`
- `filesystems.passPropertyUntilPopulated`: `Quantified over the four D-002 platforms (OS × architecture) alone. There is no filesystem waiver. An undefined filesystem is not a skipped cell. Waiver of a declared platform is platform removal.`
- `filesystems.notG07CoverageDomain`: `G07's 'supported filesystems' exact-bytes coverage domain is a different question. …` (G07's own list is DECISIONS-NEEDED C10, not this packet.)
- `versionOrBuildSelector.standing`: `RESERVED on TCB v45. requiredBeforeAllowlistFreeze remains true.`; `.note`: `… a stem-only profile cannot enter G22.`
- `namedTcbEvidenceClassesCitedNotApplied.populatedTables`: `Per-OS concrete members remain RESERVED as G22 qualification evidence (TCB v45 identityRuleShape.populatedTables / memberPopulation). This specification does not populate them.`

### 4.4 Candidate values proposed anywhere in the record

**None in the record** for any per-OS table row, filesystem selector value, or version/build selector value. What the record does fix is the **value language** the packet must use (grammar, not values):

- Filesystem selector (`selectorGrammar.filesystemWhereItAffectsResolution`): `"form": "closed tagged identifier owned by this contract"`, `"identifierEnum": ["apfs", "hfs-plus", "ext4", "xfs", "btrfs", "tmpfs"]`, plus `otherTag` `OTHER-FSTYPE` (`sha-256` over the normalized token; `lawfulOnlyWhen`: `the normalized token is absent from identifierEnum`); `wildcardRejected: true`, `emptyRejected: true`, `noOrJoin: true`. The macos/arm64 stem adds `"mustNot": "apfs-or-hfs-plus as a single value"`.
- Version/build selector (`selectorGrammar.supportedVersionOrBuildSelector`): `"form": "closed tagged union owned by this contract"`; lawful tag `EXACT-BUILD` (`wildcardRejected: true`, `emptyRejected: true`, `comparisonAlgorithm: opensip-platform-build-exact.1`); `CLOSED-RANGE.standing`: `PROHIBITED as a required-member value until this contract versions a total order per identifierScheme. A CLOSED-RANGE object cannot occupy supportedVersionOrBuildSelector.`; `serialization`: `exactly one lawful tag object. The later packet chooses values inside this language and MUST NOT mint range or scheme semantics.`; identifier schemes: `macos-product-build` (`osFamily = macos`; observation `macOS product-build string as Apple publishes it, after Unicode NFC and trim …`) and `linux-distro-userspace` (`schemeId = opensip-linux-distro-userspace.1`; fields `publisher` from `/etc/os-release ID` with `knownIds` `["amzn","alpine","arch","debian","fedora","rhel","sles","ubuntu","opensuse-leap","opensuse-tumbleweed"]` else `OTHER-PUBLISHER`; `userspaceRelease` from `/etc/os-release VERSION_ID`, `absent` ⇒ `the profile refuses`); `schemeBinding`: `macos-product-build is lawful only for osFamily=macos. linux-distro-userspace is lawful only for osFamily=linux.`
- The `identifierEnum` tokens are explicitly **not** a populated domain: occupancy v2 `filesystems.doesNotInvent`: `… does not treat TCB identifierEnum tokens as a populated G22 coverage domain.`

### 4.5 Constraints (verbatim, beyond §4.3–4.4)

- Ownership of the packet is itself undecided: `Choosing its owner is a separate decision.` (verbatim in contract v45 `platformProfile.populationPacket` and in G22 occupancy `harness.DR-G22.platform-abi-loader.v2` `filesystems.laterAct`); the current join `platform-tcb-leftover-join.v9` `proposedLaterWork[2]` says it in its own words: `This join does not populate those selectors and does not choose that packet's owner.` The row owner cell is `Security + release + platform owners`.
- Because `EXACT-BUILD` is the only lawful tag and `CLOSED-RANGE` is `PROHIBITED`, a version/build selection is one exact macOS product build per macOS stem and one exact `publisher:VERSION_ID` per Linux stem — per `serialization`: `exactly one lawful tag object` — unless a contract successor `versions a total order per identifierScheme`.
- Signed carrier dependency: `tcbCarrier.dependencyIfCarrierAbsent`: `G22 cannot QUALIFY until that one signed carrier exists and is bound. A population packet is not a substitute carrier.` (that carrier is DR-101's — occupancy `dr101Split`; DECISIONS-NEEDED C8).
- `Windows remains D-002 absent.`

### 4.6 Fill-in form — DR-126

| Field | Your entry |
|---|---|
| Population-packet owner | ☐ `Security + release + platform owners` (row owner) ☐ other named authority: ______ ☐ defer the owner choice (state trigger) |
| macos/arm64 — filesystem selector | ☐ `apfs` ☐ `hfs-plus` ☐ other enum / `OTHER-FSTYPE` ☐ defer — (`mustNot`: `apfs-or-hfs-plus as a single value`) |
| macos/arm64 — `EXACT-BUILD` macos-product-build | ☐ value: ______ ☐ defer |
| macos/x86_64 — filesystem / build | ☐ ______ / ______ ☐ defer |
| linux/x86_64 — filesystem (`ext4`/`xfs`/`btrfs`/`tmpfs`/other) / `publisher:VERSION_ID` | ☐ ______ / ______ ☐ defer |
| linux/arm64 — filesystem / `publisher:VERSION_ID` | ☐ ______ / ______ ☐ defer |
| Per-OS allowlist member tables (8 taxonomy classes × 4 stems) | ☐ author now via packet (owner above) ☐ defer to G22 qualification evidence by explicit disposition (this is the contract's current standing: `RESERVED as G22 qualification evidence`) |
| `ikconfigParserVectors`, `NT-TCB-KEXEC` | ☐ leave `RESERVED as G22 evidence` (state explicitly) ☐ other |
| Single-exact-build limitation acceptable? | ☐ yes ☐ no — direct a contract successor that `versions a total order per identifierScheme` first |
| Recording shape | ☐ user-made verbatim ☐ D-000 cycle |

**Orchestrator recommendation (non-binding):** the smallest decision that unblocks anything here is the packet's owner plus the four filesystem selectors — both are pure choices inside a closed grammar; the per-OS member tables already carry a recorded standing (`RESERVED as G22 qualification evidence`) that a disposition can simply confirm.

### 4.7 COORD-entry skeleton (DRAFT)

```
## D-⟨NNN⟩ — DR-126: TCB population-packet owner and slice-1 selector values ⟨or: explicit deferral disposition⟩

- **Date:** ⟨YYYY-MM-DD⟩
- **Status:** ⟨ADOPTED …; D-132 form or D-006 form⟩
- **Decision type:** PREFERENCE-LADEN (route C for the values; D-001 classes the row rule-governed). Does not mark SATISFIED. Does not edit file 08. Does not freeze an allowlist. Does not apply TCB v45.
- **Subject:** `platform-tcb-contract.v45.json` `da87bdb4…` (D-125) platformProfile.populationPacket / slice1ProfileStems / selectorGrammar; G22 occupancy v2 `2973cda2…` (D-219) filesystems / versionOrBuildSelector; current DR-126 leftover-join `platform-tcb-leftover-join.v9.json` `1774427e…` (D-268) obligation OBL-RESERVED-TABLES.
- **Decision:**
  Population-packet owner = ⟨authority⟩ ⟨or DEFERRED, trigger ⟨…⟩⟩.
  Filesystem selectors (filesystemWhereItAffectsResolution): macos/arm64 = ⟨enum token⟩; macos/x86_64 = ⟨…⟩; linux/x86_64 = ⟨…⟩; linux/arm64 = ⟨…⟩ ⟨or DEFERRED to the packet⟩.
  Version/build selectors (EXACT-BUILD only; CLOSED-RANGE prohibited): macos/arm64 = macos-product-build ⟨…⟩; macos/x86_64 = ⟨…⟩; linux/x86_64 = linux-distro-userspace ⟨publisher⟩:⟨VERSION_ID⟩; linux/arm64 = ⟨…⟩ ⟨or DEFERRED to the packet⟩.
  Per-OS allowlist member tables: ⟨authored by the packet under the owner above | remain "RESERVED as G22 qualification evidence" by explicit disposition, trigger: G22 qualification run⟩.
  ikconfigParserVectors and NT-TCB-KEXEC remain RESERVED as G22 evidence. Windows remains D-002 absent. G07's supported-filesystem coverage domain is a separate act (DR-G07). Does not SATISFY DR-126. Does not QUALIFY G22. Does not open D-056 Class A. Does not authorize `docs/v2/implementation/`.
- **Successor work this entry names:** the population packet artifact (independent dual review); platform-tcb leftover-join.v10 remasuring OBL-RESERVED-TABLES; G22 occupancy v3 with matrixStanding no longer INCOMPLETE on the filesystem axis.
- **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays 28 of 28 named. Condition 5 last.
- **Reversibility:** one supersession line + revert of C-D⟨NNN⟩. Does not overturn D-002, D-006, D-125, D-219, D-268.
- **Commit:** C-D⟨NNN⟩.
```

---

## 5. One-page summary of the four decisions

| Item | Row owner cell (file 08) | Current join (sha256 prefix, recorded at) | Reserved obligation(s) | Candidates in record | Cheapest lawful shapes |
|---|---|---|---|---|---|
| C1 DR-112 | `Security + operations` (OD-112-4 also `RESERVED to product/release`) | `signed-index-leftover-join.v4` `ae5176e2…` (D-280) | `OBL-RESERVED-NUMBERS` (OD-112-1..4) | none | set values; or explicit deferral with trigger (D-006 clause-5 shape); OD-112-3 may be confirmed as `preview refuse` |
| C2 DR-118 | `Product + language architecture owners`; G13 `Product + language owners` | `language-quality-leftover-join.v5` `e1210173…` (D-273) | `OBL-THRESHOLDS`, `OBL-MATRIX-CORPUS`, `OBL-G13-RESERVED` | none (five-area `illustrativeFloor` is not a value) | confirm rule + deferral to matrix acceptance; G13 stays reserved unless a D-002+D-086 successor is directed |
| C3 DR-111 | `Versioning authority` | `compatibility-leftover-join.v2` `33e4299d…` (D-177; file-08 pin `f909ddff…`, one edit behind live) | `OBL-NUMERIC-WINDOWS` (+ dependent `OBL-LOCK-JOIN`) | none (D-012's 90-day alias window is another row's) | state unit + values for S-CORE/S-SCHEMA/S-CTRL/S-TS1; or deferral with trigger; remasure join to live file 08 |
| C4 DR-126 | `Security + release + platform owners`; G22 `Security + release + platform` | `platform-tcb-leftover-join.v9` `1774427e…` (D-268) | `OBL-RESERVED-TABLES` | none (grammar only: 6-token filesystem enum + `OTHER-FSTYPE`; `EXACT-BUILD` only) | choose packet owner + four filesystem selectors; confirm tables `RESERVED as G22 qualification evidence` by disposition |

---

## 6. Open questions not resolvable from bytes

1. **Does a number-level deferral make a slice-affecting row D-056-eligible?** The only precedent (DR-115 / D-006 clause 5 / D-089) parked a cap at a named, owned gate (DR-G05). For OD-112-n, DR-111 windows and DR-126 tables the joins record `existingGate: "none"` and `rideStanding: "not-capable-of-riding"`; whether a deferral disposition can move them to `deferredOrRidesElsewhere` and satisfy D-056 gates 2–3 is not stated anywhere in the record.
2. **Token for the deferral.** "post-Condition-5" (DECISIONS-NEEDED items C5–C6 wording; not used in C1–C4) and "after Condition 5" (STATUS §3.C wording for DR-120/DR-125/DR-107/121) do not occur in COORD or file 08; the record's terms are "explicit deferral disposition" / "deferral limb". Which wording the owner wants recorded is open.
3. **OD-112-1 cardinality:** whether ordinary-trust threshold and recovery-commit threshold are one number or two (both cite `value still OD-112-1`).
4. **OD-112-2 cardinality:** one floor or two (skew vs. freshness); units unstated.
5. **OD-112-3 type:** the contract says `refuse unless OD-112-3 is later numbered` for a permission decision; what "numbered" means for a break-glass permission is not defined.
6. **DR-111 window unit** and whether the four reserved surfaces share one window.
7. **compatibility-leftover-join.v2 currency:** its `file08Pin.sha256` is `f909ddff…` (file 08 at commit `892236a`, D-169 — live when D-177 was recorded on 2026-08-21); file 08 moved once afterwards (commit `fc688b1`, D-236, 2026-08-23 → live `e503b75b…`); no COORD entry after D-177 addresses this. Whether a v3 remasurement must precede or accompany a value act is a process call (the other three joins in this packet pin the live `e503b75b…`).
8. **DR-118 row set:** per-row thresholds cannot be enumerated until DR-125 closes or is disposed (`matrixShape.dr125ActivationGate: OPEN`); DR-125's disposition is outside this packet.
9. **DR-126 population-packet owner** — expressly `a separate decision` in three artifacts; not named anywhere.
10. **Recording shape** for each item (D-132 user-made verbatim vs. D-006 decided-on-behalf under D-000 review) — both exist as precedent; DECISIONS-NEEDED says the orchestrator "will turn each answer into a D-000 cycle".

---

## 7. Citations relied on

File 08 (`docs/v2/architecture/08-decision-and-readiness-register.md`, `e503b75b…`): line 280 (V2 table header: `Owner / decision authority`); line 285 (DR-103 owner); line 293 (DR-111); line 294 (DR-112); line 300 (DR-118); line 302 (DR-120 blueprint impact); line 307 (DR-125 blueprint impact); line 308 (DR-126); lines 310–312 (DR-128/129/130 deferral dispositions); lines 329–333 (gate preamble incl. waiver sentence); line 335 (gate header); line 337 (DR-G01); line 341 (DR-G05 `caps deferred by explicit disposition (D-006)`); line 343 (DR-G07); line 344 (DR-G08); line 349 (DR-G13); line 350 (DR-G14); line 358 (DR-G22); lines 397–424 (`### Current position — measured snapshot, 2026-08-15`, Condition rows 1–5 and the one-sentence summary).

COORD (`docs/coop/COORDINATOR-DECISIONS.md`, `47f7b201…`): `## D-000` clauses 2 and 5; `## D-001` quoted checklist bullet 2, pin-note, three routes (A)/(B)/(C), "Condition 2 — all 29 rows classified"; `## D-002` platforms, explicit deferrals, condition-2 affected-row set; `## D-006` Status/Decision type, Decision clauses 5–6; `## D-007` Decision items 7–9 and Alternatives (THRESHOLDS-NOW); `## D-010` Decision; `## D-012` Decision item 5; `## D-056` Status/Decision/Readiness; `## D-086` (`G13 is reserved behind DR-118`); `## D-089` Decision; `## D-103`; `## D-105`; `## D-113`; `## D-125`; `## D-132` Status/Decision type; `## D-177`; `## D-181` (only post-D-177 DR-111 mention); `## D-268`; `## D-273`; `## D-280`; heading count 277.

Artifacts (`docs/coop/artifacts/`, sha256 in full above): `coordinator-decisions.D-056.turn2.draft.md` (`dfb0c2af…`, lines 151, 175–200); `signed-index-leftover-join.v4.json` (`ae5176e2…`); `signed-index-trust-contract.v8.json` (`fc171321…`); `harness.DR-G08.trust-recovery.install-surfaces.v3.json` (`13076be2…`); `language-quality-leftover-join.v5.json` (`e1210173…`); `language-quality-matrix-contract.v13.json` (`9efffdb3…`); `compatibility-leftover-join.v2.json` (`33e4299d…`); `compatibility-matrices-contract.v5.json` (`d0386cee…`); `platform-tcb-leftover-join.v9.json` (`1774427e…`); `platform-tcb-contract.v45.json` (`da87bdb4…`); `harness.DR-G22.platform-abi-loader.v2.json` (`2973cda2…`); `g22-named-corpus-catalog.v1.json` (`6380431c…`, cited by the join, not quoted).

Git: `git log -- docs/v2/architecture/08-decision-and-readiness-register.md` — commit `892236a` (2026-08-20, D-169) is the file-08 version whose sha256 is `f909ddff…`; the only later file-08 commit is `fc688b1` (2026-08-23, D-236, sha256 `e503b75b…`). D-177's recording commit is `afb115d` (2026-08-21).

Working documents (not sources of truth): `DECISIONS-NEEDED.md` §C items C1–C4; `STATUS.2026-08-26.md` §3.C.
