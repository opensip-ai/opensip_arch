# C1 — DR-112 / OD-112-1..4: what remains after D-293

Measured at HEAD `f3456575071928022a1f0e3a77e531a87157b365` (last COORD heading `## D-294`).
Live digests measured at this HEAD: file 08 `docs/v2/architecture/08-decision-and-readiness-register.md`
`e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; COORD
`docs/coop/COORDINATOR-DECISIONS.md` `31746810f9be78f697d66eb94d9cd50a95a51218998f97a154596363039fb9b6`
(the C1–C4 packet measured COORD at `47f7b201…` / HEAD `4abb961`, before D-293 and D-294 were appended);
`DECISIONS-RECOMMENDED.md` `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370` (the digest
D-293 **Subject** cites); `DECISION-PACKETS/C1-4-reserved-numbers-security-quality.md`
`59497fe6835c3fb3b84dfe757b63daa22b1b4cbdd103fd2d74026a0e192c376c` (matches `DECISION-PACKETS/MANIFEST.sha256`
`ecdbb41dc07e4833abe787387fa39aacc5d0c4a9d98a01a25f645d32520809e0`).

This file plans record acts. It decides nothing, edits nothing under `docs/`, and invents no value.

---

## 1. What D-293 already decided, and what therefore remains

**COORD `## D-293`, Decision item 6, first sentence (verbatim, COORD lines 16238–16243):**

> `6. **C1–C4.** OD-112-3 is the final fail-closed policy; OD-112-1`
> `   and OD-112-2 stay under DR-112's `Security + operations``
> `   authority and OD-112-4 under product/release; any later parking`
> `   disposition names a real trigger and has no Condition-2 or`
> `   D-056 eligibility effect without a separate reviewed act and a`
> `   successor join.`

**D-293's own scope limit (verbatim, closing paragraph of its Decision):**

> `It does not record any artifact successor, fixture byte, or`
> `successor join; every such act follows under D-000 as the adopted`
> `recommendation states.`

Limb-by-limb:

| Limb | D-293's disposition | Does an artifact carry a token that must change? | Remaining record act |
|---|---|---|---|
| **OD-112-3** | "is the final fail-closed policy" | **Yes.** Three live artifacts still say `RESERVED` / `Preview refuse` / `Not minted`, and one says the refusal holds only "unless OD-112-3 is later numbered" (§2) | **One act** (see §7) |
| **OD-112-1** | "stay under DR-112's `Security + operations` authority" | No. File 08 line 294 already carries `Security + operations`; the contract says `RESERVED. Named. Not minted.`; the join says `existingGate: "none"`. D-293 restates the live state | **No further act** |
| **OD-112-2** | same | No, same measurement | **No further act** |
| **OD-112-4** | "and OD-112-4 under product/release" | No. `signed-index-trust-contract.v8` `$.namedOpenDecisions[3].standing` already reads `RESERVED to product/release…`; `$.auditAndWaiver.waiverExpiry` already reads `Gate-waiver duration is product/release authority per the file 08 gate preamble.` D-293 restates the live state | **No further act** |
| **"any later parking disposition names a real trigger and has no Condition-2 or D-056 eligibility effect…"** | A condition on a *future* act | No token today | **No act now**; it is a constraint the C5/C6/C7 acts must honour |

**No value for OD-112-1, OD-112-2 or OD-112-4 is in D-293 or anywhere in the record.** The C1–C4 packet §1.4
measured this: "**None in the record.** Evidence: `grep -n "OD-112" COORD` returns one line (9341, inside a
'does not mint OD-112-1..4' sentence)". Those three stay named open decisions in every successor authored under
this plan.

---

## 2. Current artifacts to succeed

### 2.1 The contract that originates the reservation

`docs/coop/artifacts/signed-index-trust-contract.v8.json` — sha256
`fc171321e969c74464dbc9ff67edd9b874aac1d1c7375c7dc8e431469442efe0`.
`$.status` = `"CANDIDATE-NOT-APPLIED"`, `$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`, `$.binds` = `"NOTHING"`.
Recording heading: **`## D-105 — Record signed-index-trust-contract.v8 as DR-112's accepted design-contract candidate`**.

`$.namedOpenDecisions` is an array of `{id, decision, standing}` objects; verbatim:

```
$.namedOpenDecisions[0] = {"id": "OD-112-1", "decision": "Quorum / threshold cardinality", "standing": "RESERVED. Named. Not minted."}
$.namedOpenDecisions[1] = {"id": "OD-112-2", "decision": "Clock skew and last-known-revocation freshness floors", "standing": "RESERVED. Named. Not minted."}
$.namedOpenDecisions[2] = {"id": "OD-112-3", "decision": "Emergency running-component / break-glass permission to continue a REVOKED component", "standing": "RESERVED. Preview refuse. Not minted."}
$.namedOpenDecisions[3] = {"id": "OD-112-4", "decision": "G08 waiver duration", "standing": "RESERVED to product/release. Named as an expiry-bearing waiver, not a number."}
```

The second OD-112-3 site, verbatim:

```
$.offlineRunningPolicy.totalDecision[4] = {
  "when": "TR-COMPONENT is ST-REVOKED",
  "alreadyRunning": "refuse unless OD-112-3 is later numbered; preview refuse",
  "newProcess": "refuse",
  "refusalReason": "CONTINUE-COMPONENT-NOT-TRUSTED"
}
```

### 2.2 The current G08 occupancy

`docs/coop/artifacts/harness.DR-G08.trust-recovery.install-surfaces.v3.json` — sha256
`13076be20e4eef0dfe352786b705de09304a69f583529502388e5086f6f098c0`; `$.status` = `"CANDIDATE-NOT-APPLIED"`,
`$.binds` = `"NOTHING"`. Recorded at **`## D-211`** (per `signed-index-leftover-join.v4` `recordedInputs`).
It carries the same four strings at `$.reservedNumbersRemainReserved.OD-112-1..4`, plus
`$.proposedLaterWork[6]`: `A later product/release act may set OD-112-1..4. This v3 occupancy does not mint those numbers.`
and `$.failsIf[22]`: `a quorum, clock, waiver, or ceremony number is invented`.

### 2.3 The current DR-112 leftover-join and the obligation to remeasure

`docs/coop/artifacts/signed-index-leftover-join.v4.json` — sha256
`ae5176e2a420be75b8aade77e7f265bc411968a75a35647ae01bfc708835a174`; `$.version` = `4`; `$.date` = `"2026-08-24"`;
`$.status` = `"CANDIDATE-NOT-APPLIED"`; `$.registerRow` = `"DR-112"`; `$.file08StatusToken` = `"OPEN"`;
`$.head` = `"28b79e14cb8e69c2ea4b7b446bf71ca8f0088114"`;
`$.file08Pin` = `{"path": "docs/v2/architecture/08-decision-and-readiness-register.md", "sha256": "e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e"}` — **already the live file-08 digest**.
`$.summary.leftoverDesign` = `["OBL-G08-FX-AUTHORING", "OBL-RESERVED-NUMBERS"]`.
Recording heading: **`## D-280 — Record signed-index leftover-join.v4 as DR-112 leftover remasurement`**
(`ADOPTED 2026-08-24`; turn 1 of 3, CONSENT from both reviewers, 0 MUST-FIX, 0 SHOULD-FIX; Stage A Claude ACCEPT
`1ff13ff4…` 0/0, Stage A Codex ACCEPT `581cf063…` 0/0).

Obligation object to remeasure, verbatim (`$.obligations[5]`):

```
{
 "id": "OBL-RESERVED-NUMBERS",
 "leftoverDesign": true,
 "existingGate": "none",
 "executionObligationOwnerToday": "none",
 "rideStanding": "not-capable-of-riding",
 "reason": "D-105 records quorum, clock/freshness, emergency, and waiver numbers remain RESERVED. G08 occupancy reservedNumbersRemainReserved names OD-112-1..OD-112-4 verbatim. Undecided numbers are leftover-design (D-056). This join does not mint those numbers and does not invent a recovery ceremony implementation. g08 leftover-join.v4 leftoverDesign is [OBL-G08-FX-AUTHORING] and does not steal OBL-RESERVED-NUMBERS. This join does not close it."
}
```

Top-level `$.reservedNumbersVerbatim` (verbatim):

```
{
 "OD-112-1": "Quorum / threshold cardinality. RESERVED. Named. Not minted.",
 "OD-112-2": "Clock skew and last-known-revocation freshness floors. RESERVED. Named. Not minted.",
 "OD-112-3": "Emergency running-component / break-glass permission to continue a REVOKED component. RESERVED. Preview refuse. Not minted.",
 "OD-112-4": "G08 waiver duration. RESERVED to product/release. Named as an expiry-bearing waiver, not a number. Waiver rule remains pass all safety cases."
}
```

`$.proposedLaterWork[2]`: `A later product/release act may set quorum, clock, emergency, or waiver numbers. This join does not mint those numbers.`

### 2.4 File 08 row (line 294, verbatim, first cells)

> `| DR-112 | Signed-index refresh, expiry, last-known revocation, quorum loss, root recovery, emergency running-component policy | Security + operations | … | OPEN | Hard blocker |`

Owner / decision-authority cell: `Security + operations`. Status cell: `OPEN`. **No cell edit is planned here** (§5).

---

## 3. Precedent

### 3.1 Contract successor of this very lineage: v7 → v8 at D-105

**`## D-105`**, Status: `**ADOPTED 2026-08-14.** Turn 1 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX.`
Decision type: `RULE-GOVERNED. Records independent dual ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same form as D-013 / D-015 / D-035 / D-042 / D-103 / D-104.`
Subject: `docs/coop/artifacts/signed-index-trust-contract.v8.json` `fc171321…`.

**What its reviewers attacked** (verdict files named in D-105):
`signed-index-trust-contract.v8.review-independent.claude2.json` `559cfad1f29443326734fe4cc480aca802bfac118668080956af59534029dead`
— `ACCEPT-WITH-ADVISORIES, 0 blockers, 0 SHOULD-FIX`, advisory **CLAUDE-V8-A1** (`ADV-V8-01: memberApplicability
parenthetical omits recovery PRESENT member 18`).
`signed-index-trust-contract.v8.review-independent.codex.json` `10784a6de2c2767cec5ce55549cc75d4402cd93f4fe5342e8ff95c5236fead13`
— `ACCEPT, 0 blockers, 0 SHOULD-FIX`, advisory **CODEX-V8-A1** (`SITCV8-A1: Codex v7 pin`).
The predecessor is the cautionary case: Codex v7 `ffe079b9c634fe97a2a735fbda99efac386505870e11b31b2b23753c6f38a1e5`
**COMPLETE REJECT, 0/1/0, SITCV7-S1 only** — a single SHOULD-FIX is a REJECT under the 0/0 rule.

### 3.2 A leftover-join whose obligation flipped out of `leftoverDesign` after a later act

`component-manifest-leftover-join.v2` (recorded **`## D-161`**) had
`$.summary.leftoverDesign` = `["OBL-G15-HARNESS-SPEC", "OBL-WINDOWS-PATH", "OBL-ENVELOPE-MISMATCH", "OBL-UNICODE-NORM", "OBL-OD-1", "OBL-OD-2"]`.
`component-manifest-leftover-join.v6.json` `9953f9692379f3f30254df12735d284559da6b6e979fd684296ace02d0e6e212`
(recorded **`## D-174 — Record component-manifest-leftover-join.v6 as DR-103 leftover remasurement`**) moved
`OBL-G15-HARNESS-SPEC` to `$.summary.specifiedNotLeftover` with `leftoverDesign: false`,
`existingGate: "DR-G15"`, `executionObligationOwnerToday: "Component architecture + language publisher + release/DevEx"`,
`rideStanding: "qualification-at-named-gate"`, and the reason
`"G15 is named (D-086) and the specification now exists at harness.DR-G15.packaging-adapter-conformance.v7 … Leftover-design of authoring that specification is therefore stale as an authoring claim. Remainder is G15 execution, which remains qualification (D-056)."`

**Measured caution — no precedent of the exact class this act needs.** A sweep of every
`*leftover-join*.json` in `docs/coop/artifacts/` comparing `summary.leftoverDesign` across consecutive versions
finds **no case in which a RESERVED-value obligation (`OBL-RESERVED-NUMBERS`, `OBL-THRESHOLDS`,
`OBL-NUMERIC-WINDOWS`, `OBL-RESERVED-TABLES`, `OBL-CI-ENCODING-RESERVED`, `OBL-ENCODING-RESERVED`,
`OBL-SDK-API-RESERVED`, `OBL-ADAPTER-IMPL`, `OBL-OD-1`, `OBL-OD-2`, `OBL-D1`, `OBL-D2`) left the
`leftoverDesign` partition**. Every partition shrink on record is an authoring or execution obligation closed by
authored bytes or by a recorded specification (`OBL-G15-HARNESS-SPEC` at D-174; `OBL-G09-HARNESS-SPEC`
permission v2→v3; `OBL-JOIN-FX-EXECUTION` doctor-actor v8→v9; `OBL-G23-FX-AUTHORING` → `[]` in
`g23-leftover-join.v8` at **`## D-240`**, after the D-237/D-239 fixture recordings;
`OBL-NT-11-EXECUTION` in identity-namespace v4→v5). **This act does not need such a flip** — see §4 —
but C7's OD-2 act does, and it will be the first of its kind.

### 3.3 What reviewers attack in leftover-join successors of this era (verdict files read)

- `platform-tcb-leftover-join.v8.review-independent.claude2.json` — **REJECT**, 0 MUST-FIX / 1 SHOULD-FIX,
  **CLAUDE-PTLJ-V8-SF1** at `basedOn.predecessorV6.role`: `"The v8 artifact self-labels as v7 … 'This v7 remasures occupancy v1 stale after occupancy v2 (D-219).'"`
- `platform-tcb-leftover-join.v8.review-independent.codex.json` — **REJECT**, **CODEX-PTLJ-V8-SF1**, same site,
  `"Once republished as v8, the deictic 'This' names the wrong subject version."`
- `component-manifest-leftover-join.v8.review-independent.codex.json` — **REJECT**, **CMLJ-V8-SF1** (same deictic
  class) and **CMLJ-V8-SF2** at `purpose`: `"The purpose calls the cumulative lands record unchanged while v8 extends it"`.
- `distribution-core-leftover-join.v8.review-independent.claude2.json` — **REJECT**, 0/2,
  **CLAUDE-DCLJ-V8-SF1** (`obligations[OBL-2].reason` asserts a landing custody claim the frozen v3 bytes
  contradict) and **CLAUDE-DCLJ-V8-SF2** (`"replaces 'carries the former basedOn object unchanged' with a description of the actual diff"`).
- `language-quality-leftover-join.v4.review-independent.codex.json` — **REJECT**, **CODEX-LQLJ-V4-SF1**:
  `"Both historical repairs are attributed to the wrong landing artifact"`.

Every one of these is a custody/wording defect, not a substantive one, and every one cost a REJECT.

---

## 4. The successor's minimal diff

**Scope note:** D-293 changed the standing of **one** named open decision. Nothing else about DR-112 moved.

### 4.1 `signed-index-trust-contract.v9.json` (Stage A subject 1)

Changes, and only these:

- `$.namedOpenDecisions[2].standing` — currently `"RESERVED. Preview refuse. Not minted."` The successor
  records the D-293 disposition. **The exact replacement wording is not stated in the record.** D-293's own words
  are `OD-112-3 is the final fail-closed policy`; the successor must carry that sentence verbatim with its
  citation (`D-293`) and must not add any condition, duration or exception D-293 does not state.
- `$.offlineRunningPolicy.totalDecision[4].alreadyRunning` — currently
  `"refuse unless OD-112-3 is later numbered; preview refuse"`. The clause `unless OD-112-3 is later numbered`
  is the sentence D-293 supersedes. **Whether the successor writes plain `refuse`, or keeps the word
  `preview`, is not stated in D-293** — flag as an owner/reviewer question (§6, Q1). The safe form is the one
  the record supports: state the D-293 disposition and mark the `unless … later numbered` clause superseded,
  without re-deciding the refusal's phrasing.
- `$.namedOpenDecisions[0]`, `[1]`, `[3]` — **byte-identical.** OD-112-1, OD-112-2 and OD-112-4 remain
  explicit named open decisions with their existing `standing` strings. D-293 states no value for them.
- `$.auditAndWaiver.waiverExpiry`, `$.trustPolicyShape.*`, `$.recoveryAuthorityShape.*`,
  `$.recoveryCeremony.doesNotMint`, `$.machine.*`, `$.fixtureClasses.*` — **byte-identical.** The threshold and
  freshness sites still read `value still OD-112-1` / `skew reserved` / `inside the reserved freshness floor`.
- `$.status`, `$.reviewStatus`, `$.binds` — unchanged (`CANDIDATE-NOT-APPLIED` / `AWAITING-INDEPENDENT-REVIEW` /
  `NOTHING`), per D-105's form.

### 4.2 `harness.DR-G08.trust-recovery.install-surfaces.v4.json` (Stage A subject 2)

- `$.reservedNumbersRemainReserved.OD-112-3` — same change, same wording discipline.
- `$.reservedNumbersRemainReserved.OD-112-1/2/4`, `$.proposedLaterWork[6]`, `$.failsIf[22]` — byte-identical
  (`a quorum, clock, waiver, or ceremony number is invented` still holds: D-293 mints no number).
- `$.connectivityClasses[1].exactByteIntent` (`OD-112-3 remains RESERVED; preview refuse on a REVOKED component.`)
  must be reconciled with the successor's OD-112-3 sentence or the artifact contradicts itself — the defect class
  Codex charged as `CODEX-PTLJ-V8-SF1`.

### 4.3 `signed-index-leftover-join.v5.json` (Stage A subject 3)

- `$.obligations[5]` (`OBL-RESERVED-NUMBERS`) — **stays `leftoverDesign: true`**, `existingGate: "none"`,
  `executionObligationOwnerToday: "none"`, `rideStanding: "not-capable-of-riding"` unchanged, because
  OD-112-1, OD-112-2 and OD-112-4 are still undecided. Only `reason` changes: it must record that OD-112-3 is
  decided at D-293 and that the remainder is OD-112-1/2/4. **`$.summary.leftoverDesign` stays
  `["OBL-G08-FX-AUTHORING", "OBL-RESERVED-NUMBERS"]`** — no partition change, which is exactly what the
  HANDOFF standing rule requires (`leftoverDesign set must not change except when a named finding requires
  additive honesty`).
- `$.reservedNumbersVerbatim.OD-112-3` — updated to the successor contract's sentence; `OD-112-1/2/4` byte-identical.
- `$.file08Pin`, `$.file08StatusToken` (`"OPEN"`), `$.registerRow` — byte-identical; file 08 has not moved.
- `$.head`, `$.date`, `$.version`, `$.basedOn.*` — advanced to this act's HEAD and predecessor custody.
- `$.proposedLaterWork[2]` — must drop `emergency` from `A later product/release act may set quorum, clock, emergency, or waiver numbers.` or the successor contradicts D-293.

**Cross-lineage citations (D-294 Decision 3).** The successor join must cite `g08 leftover-join.v5` — the
current G08 GATE leftover-join recorded at **`## D-281`**, not `g08 leftover-join.v4` as
`signed-index-leftover-join.v4` `$.obligations[5].reason` does — and must label the superseded version as not
current. D-294 Decision 3 verbatim: `A successor issued for any reason refreshes its cross-lineage citations to
the versions current at its dispatch and labels the superseded ones as not current`. D-294 Decision 1's
custody reading means the v4 citation is **not** itself a defect requiring a successor; the successor is
warranted by the OD-112-3 change, and the refresh rides on it.

---

## 5. Prohibitions that bound the act

From **D-293** (verbatim): `This entry marks nothing `SATISFIED`. It does not edit file 08. It does not open
D-056 Class A. It does not amend D-000 or D-056.`

From **D-280** (the recording this act succeeds; verbatim): `Does not pin QUALIFIED. Does not invent fixture
bytes. Does not mint reserved numbers. Does not invent a recovery ceremony implementation. … Does not steal
OBL-G08-FX-AUTHORING as a GATE closure. Does not steal OBL-RESERVED-NUMBERS. Does not occupy the identifier.
Does not SATISFY DR-112. Does not SATISFY DR-117. Does not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to
`OPEN`. Does not flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`. Does not SATISFY DR-131. Does not
SATISFY DR-133. Does not SATISFY DR-114. Does not SATISFY DR-101. Gate 1 Class A is not opened. Not SATISFIED.
Required-now stays 28. Condition-4 effect is zero. … Does not execute G08. Does not rewrite occupancy v3.
Does not edit file 08. Does not authorize `docs/v2/implementation/`.`
(The successor must **not** carry `Does not mint reserved numbers` unqualified: it now mints none of
OD-112-1/2/4, but D-293 has decided OD-112-3 — which is a policy, not a number.)

From **D-105** (verbatim): `Repair-media remains DR-110. Newly-revoked replay remains DR-113.`

From `HANDOFF.D-000-orchestrator-live.txt`
(`b926489df28b183eccf4447e7f0b4c7f9bb56ef1c1f19747ae2f01b147804c3d`), `## Do not invent / do not SATISFY`:
`Do not invent … UNDECIDED numbers …`; `Do not steal OBL-THRESHOLDS / OBL-MATRIX-CORPUS / OBL-G13-RESERVED /
OBL-RESERVED-NUMBERS / …`; `Do not SATISFY DR-117 / DR-131 / DR-133 (Class A unopened).`
And its Protocol section: `Stage A leftover/occupancy dual ACCEPT, then Stage B COORD draft dual CONSENT, then
COORD-only append. No file-08 cell edit for leftover/occupancy remasurements.` /
`SATISFIED-GRADE COORD drafts *do* MF-6 file-08 cell edit, and only when D-056 five gates hold.`
**No file-08 cell edit in this act.** The DR-112 row cells are unaffected by D-293 in any case.

---

## 6. Dependencies, ordering, and what is not in the record

- **Unblocked.** The OD-112-3 act depends on nothing but D-293 itself. No value must be supplied by anyone.
- **Not a D-056 unblock.** `OBL-RESERVED-NUMBERS` stays `leftoverDesign: true` and
  `OBL-G08-FX-AUTHORING` is untouched (it is Packet D / D-293 Decision 8 scope, and D-293 reserves the G08
  gate obligations to the owner: `Reserved to the owner: the gate obligations at G07, G08, G09, G12, G14 and G22`).
  DR-112 stays `OPEN`; Condition 2 stays 5 of 32.
- **Q1 (owner / reviewer question).** D-293 says `OD-112-3 is the final fail-closed policy`. It does **not**
  state the replacement text for `$.offlineRunningPolicy.totalDecision[4].alreadyRunning`
  (`"refuse unless OD-112-3 is later numbered; preview refuse"`), nor whether "final" removes the word
  `preview`, nor whether OD-112-3 should be deleted from `namedOpenDecisions` or kept there with a DECIDED
  standing. **Not stated → the successor must carry D-293's sentence verbatim and name the residual wording
  question, rather than choose.**
- **Q2.** OD-112-1's cardinality (one threshold or two — `trustPolicyShape.requiredOnEveryTrustedEntry[3]` and
  `recoveryAuthorityShape.requiredOnRecoverCommit[3]` both say `value still OD-112-1`) and OD-112-2's
  cardinality (`Clock skew and last-known-revocation freshness floors`, plural) remain **not in the record**;
  D-293 states no value. They stay named open decisions.

---

## 7. Act shape

**Act C1-a — "DR-112: OD-112-3 final fail-closed"** (1 act, 3 Stage-A subjects).

- **Stage A** (independent dual adversarial review, ACCEPT only at 0 MUST-FIX / 0 SHOULD-FIX):
  1. `docs/coop/artifacts/signed-index-trust-contract.v9.json`
  2. `docs/coop/artifacts/harness.DR-G08.trust-recovery.install-surfaces.v4.json`
  3. `docs/coop/artifacts/signed-index-leftover-join.v5.json`
- **Stage B**: `coordinator-decisions.D-NNN.draft.md` — dual CONSENT 0/0, up to three turns
  (D-000 clause 2: `**Termination clause: 3 turns each side.**`). Decision type: `RULE-GOVERNED` recording of a
  PREFERENCE-LADEN owner decision already made at D-293 (the D-105 / D-280 form, not the D-006 form —
  the preference was exercised by the user, not on their behalf).
- **Then**: COORD-only append; commit `C-DNNN`.

**Estimated acts: 1** (three Stage-A subjects inside it). A reviewer may insist the three subjects be split into
three recordings, as the G01–G05 occupancy remasurements were split across D-231–D-235; if so, **3 acts**.
