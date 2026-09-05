# Packet B3 — DR-117 Class A opening

**Prepared:** 2026-08-27 by the D-000 orchestrator (Claude), for the human owner.
**Measured at:** HEAD `4abb961aad98525ca8b992a24609a6286964a451` (D-292). File 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. COORD `47f7b2011ec719dfadcbccb553a142eb0808e3099f20bf544b4564ab18e28466` (277 `## D-NNN` headings).
**Nothing here is decided.** Every factual line carries a citation; bytes are quoted verbatim; values absent from the record are marked *not in the record*. §9 presents options; one line is labelled "Orchestrator recommendation". Nothing under `docs/` was edited.

---

## 0. The question

`DECISIONS-NEEDED.md` §B, lines 37–38 (re-measured against the file's current bytes; the file is untracked), verbatim:

> B3. **DR-117** product-boundary successor — candidate `preview-product-boundary-successor.v8` (D-207). Same question.
>     (Grok's standing instruction was "do not SATISFY DR-117/131/133"; I will not open Class A without your word.)

"Same question" refers to B1 (lines 34–35): *"Open Class A (application-grade acceptance, no express reservation) → then a SATISFIED-GRADE cycle? Or what must change first?"*

The standing instruction, `HANDOFF.D-000-orchestrator-live.txt` line 83, verbatim:

> Do not SATISFY DR-117 / DR-131 / DR-133 (Class A unopened).

Why only the owner can answer, `STATUS.2026-08-26.md` §2 item 1, verbatim:

> COORD says the only venue for a lift is "a reviewed coordinator act, not an artifact" — a D-000 cycle recording *application-grade, no-express-reservation* (T2-02) acceptance. The file-08 owners of those rows are **Product owner** (DR-117) […] D-001 classes DR-117 as a route-C PREFERENCE-LADEN product decision. **This is your decision, not a reviewer's.**

The venue sentence in COORD, D-207 Decision paragraph (verbatim): *"Venue for any later lift is a reviewed coordinator act, not an artifact."*

---

## 1. File 08 row DR-117 — every cell

Source: `docs/v2/architecture/08-decision-and-readiness-register.md` line 299 (sha256 `e503b75b…` above). Table header (line 280; line 281 is the `|---|` separator row): `| ID | Decision | Owner / decision authority | Source pin / affected sections | Required acceptance evidence | Status | Blueprint impact |`.

| Cell | Bytes (verbatim) |
|---|---|
| ID | `DR-117` |
| Decision | `Product-boundary successor covering the SEVEN binding product-boundary items enumerated at [file 02 §product boundary](02-distribution-and-components.md#product-boundary) (count pinned at seven by `COORDINATOR-DECISIONS.md` D-011, CONSENT `cd08c5f0…`; any change to that enumeration re-opens this row; file 02 re-verified byte-identical at `1811c682…` at this edit)` |
| Owner / decision authority | `Product owner` |
| Source pin / affected sections | `DR-010; [Product boundary](02-distribution-and-components.md)` |
| Required acceptance evidence | `Explicit successor to P-1/P-2/G3 with enforcement evidence` |
| Status | `OPEN` |
| Blueprint impact | `Hard blocker; V1 exclusions remain until closed` |

Row stability (measured): the `| DR-117 |` line at the candidate's file-08 pin (`f909ddff…` = commit `892236a`, "D-169: add DR-G32 required-now actor-join fixture execution") and at HEAD (`e503b75b…` = commit `fc688b1`, "D-236: record DR-104 SATISFIED under D-056 Class B") are byte-identical (`diff` empty). File 08 moved exactly once between the candidate's pin and HEAD (D-236). The `DR-G29` and `DR-G30` rows are likewise identical across that move. File 02 at HEAD reproduces the row's pin: `1811c682cf293e1e0b255be82c62f7ed3c439f0873eb7922bfb0ad965b43f7db`.

### 1a. The two named gates that carry DR-117's remainder (file 08 lines 365–366, verbatim)

| Row (line) | Gate | Named harness / corpus | Owner | Status |
|---|---|---|---|---|
| 365 | `DR-G29 PREVIEW-BOUNDARY-EXCLUDED-FORM-ADMISSION` | `named: harness.DR-G29.preview-boundary-excluded-form-admission.preview (D-157; not authored; not QUALIFIED). hostile-but-well-formed excluded-form admission corpus and post-admission/pre-stage substitution-mutation corpus (DR-117 EE-1, EE-2, EE-3b, EE-4, EE-5a, EE-5b, EE-6a)` | `Product owner` | `PROPOSED; not QUALIFIED` / `OPEN` |
| 366 | `DR-G30 PREVIEW-BOUNDARY-INSTALL-SHAPE` | `named: harness.DR-G30.preview-boundary-install-shape.preview (D-158; not authored; not QUALIFIED). useful-install advertisement, role-list, and product-statement corpus (DR-117 EE-7a, EE-7b, EE-7d)` | `Product owner` | `PROPOSED; not QUALIFIED` / `OPEN` |

DR-G30 Decision cell, line 366, verbatim (this is the **G30 useful-install selection**):

> `Preview useful-install selection is signed distribution core + semantic host + one TypeScript closure + future DR-131 pack; core-only is not the analysis product; a second preview language role is refused; the rustc_driver sidecar is deferred not abandoned. Corpus is useful-install advertisement, role-list, and product-statement cases. Not DR-101 signed-distribution-core inventory. Not G13 language-quality. Not DR-131 pack identity`

### 1b. Condition-2 snapshot that would also move (file 08 lines 415 and 424, verbatim excerpts)

Line 415 (Condition 2 "Measured now" cell) begins: `**5 of 32 `SATISFIED`** — 24 `OPEN`, 1 `DECIDED-V1-NOT-INTEGRATED`, 2 `PROPOSED-CLOSED-FOR-REVIEW`.` and lists `DR-102 `SATISFIED` under D-056 Class A (D-085)` as the only Class A row to date.
Line 424 ends: `condition 2 remains 5 of 32 SATISFIED.`

Related: DR-010 row (line 43) carries `DR-117 and DR-011-R16 remain independently required (condition 2 / residual)`.

---

## 2. The recording chain and the express reservation

### 2a. Two lineages, two artifacts named "v8" — do not conflate

| Artifact | sha256 | Recorded at | Role per the record |
|---|---|---|---|
| `product-boundary-successor-contract.v8.json` | `52c70f7715fb869bae70bc588043dc5b4d731b73408d2d451e868b8de963f362` | D-116 (2026-08-15) | D-116 title: "Record product-boundary-successor-contract.v8 as DR-117's accepted design-contract successor candidate". D-137 Decision: `v8 remains the D-116 leftover T2-02 candidate.` Candidate v8's `lineage.productBoundarySuccessorV8.role`: `Remains DR-117's leftover T2-02 candidate for general succession. This artifact does not replace, apply, or succeed v8.` |
| `preview-product-boundary-successor.v8.json` | `f2e788e51c347e1033073f0718e701d164affe51e7f667da9bcd49a08837144c` | D-207 (2026-08-22) | **The B3 candidate.** D-207 title: "Record preview-product-boundary-successor.v8 as DR-117 leftover remasurement". |

The preview lineage: v5 recorded at D-137 (`5face6a97b311117569044c0214452571e6d3f051e1ab9b38f46abf442ce1262`); v6 REJECTED by Claude `REJECT 1/1 CLAUDE-PPBS-V6-B1 / CLAUDE-PPBS-V6-SF1; advisory CLAUDE-PPBS-V6-ADV-1` (candidate `basedOn.claudeReview.verdict`, full value); v7 recorded at D-168 (`243c12a2389a0f81d059209f5b7050a700498840d036275c7b81eeadc31fe548`); v8 recorded at D-207.

### 2b. The reservation's origin — D-137 (COORD lines 5779–5835), Decision paragraph verbatim

> Record v5 as DR-117's preview-scoped successor candidate, authorized by D-132. This is coordinator decision D-137, not a register row. DR-117 stays `OPEN`. No `SATISFIED`. The candidate binds NOTHING. D-056 Class A is not opened. Recording v5 does not make DR-117 D-056-eligible in kind on v5 alone: most enforcement classes are candidate-owned with no exact DR-G obligation. v8 remains the D-116 leftover T2-02 candidate. D-068 remains the owner recording of preview.v2 for DR-010. Advisories CLAUDE-PPBS-V5-ADV-1, CLAUDE-PPBS-V5-ADV-2, PPBSV4-ADV-1, and standing CLAUDE-PPBS-V3-ADV-1 travel as honesty work. Does not edit file 08. Does not mint a D-096 (A) grant. Does not SATISFY DR-131, DR-133, or any other row. Does not overturn D-116, D-068, D-066, or D-136. Does not authorize `docs/v2/implementation/`.

D-137 Reversibility (verbatim): `Total only before a dependent DR-117 status re-record, SATISFIED-grade application, MF-6 edit, or other dependent act lands.`

The user grant that authorized the lineage — D-132 Decision item 5 (verbatim): `after those acts, authoring and D-000 review of DR-133, the DR-117 preview successor, DR-131, and a D-036 successor;` and its limit: `This grant is **not** a D-096 (A) owner grant. It marks nothing `SATISFIED`.`

### 2c. D-207 — the current recording (COORD lines 9062–9124)

Status (verbatim): `**ADOPTED 2026-08-22.** Turn 1 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX.` Stage B verdicts: Claude `artifacts/coordinator-decisions.D-207.review-adversarial.claude2.json` `0d439cc827d0b2156a7fac364d01f968eb902021e90a94e0026026e1e14fa9f7` CONSENT; Codex `artifacts/coordinator-decisions.D-207.review-adversarial.codex.json` `f16766e2c47540bf50a0ea7e5b083421eb9d3f196c75f27d06c25ebb456636a2` CONSENT; subject draft `82d08f98a5f678aedb5cfd2626ee013a1ee51908feb5a29e08520eb65fab7617`. All three digests reproduce on disk (measured).

Decision type (verbatim): `RULE-GOVERNED. Records independent dual ACCEPT of `preview-product-boundary-successor.v8.json` (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as D-170 through D-206. Not a three-limb act.`

Decision paragraph, verbatim:

> Record v8 as DR-117 leftover remasurement after D-206. The candidate binds NOTHING. DR-117 stays `OPEN`. leftover-design of unnamed EE classes remains closed at D-159. Remainder is named-gate execution. leftover-design of OBL-G29-FX-AUTHORING and OBL-G30-FX-AUTHORING remains on the current G29 and G30 leftover-joins. Does not steal those leftovers. Does not SATISFY DR-117. D-056 Eligibility gates 2 and 3 continue to hold for DR-117 (D-159). Gate 1 Class A remains false under D-137's express reservation. v8 does not withdraw that reservation. Venue for any later lift is a reviewed coordinator act, not an artifact. Gates 4 and 5 are not performed. Not eligible in kind. Not SATISFIED. Required-now stays 28. Condition-4 effect is zero. Frozen v7 remains a historical measurement as of HEAD `5d5d778` / required-now 26. v7 stays frozen; do not record it as current. Advisories CLAUDE-PPBS-V8-ADV-1 and CLAUDE-PPBS-V8-ADV-2 travel as honesty work. Standing CLAUDE-PPBS-V3-ADV-1 venue limb stands. Does not invent fixture bytes or the DR-131 pack. Does not rewrite G13, G14, G29, G30, G31, or G32. Does not name G13 into required-now. Does not edit file 08. Does not invent a D9 code. Does not authorize `docs/v2/implementation/`.

Readiness effect (verbatim): `Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last.` (Condition 2 was 4 of 32 on 2026-08-22; it became 5 of 32 at D-236.)

Reversibility (verbatim): `Total only before a later dependent leftover rewrite, Class A reservation lift, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D207.`

Measured: no line of COORD after D-207 (lines > 9200) mentions `preview-product-boundary-successor.v8`.

---

## 3. The candidate — `preview-product-boundary-successor.v8.json`

Path `docs/coop/artifacts/preview-product-boundary-successor.v8.json`, 55,298 bytes, sha256 `f2e788e51c347e1033073f0718e701d164affe51e7f667da9bcd49a08837144c` (matches D-207 Subject).

| Field | Bytes (verbatim) |
|---|---|
| `artifact` / `version` / `date` | `preview-product-boundary-successor.v8` / `8` / `2026-08-22` |
| `documentClass` | `DESIGN-CONTRACT-CANDIDATE` |
| `status` | `CANDIDATE-NOT-APPLIED` |
| `reviewStatus` | `AWAITING-INDEPENDENT-REVIEW` |
| `binds` | `NOTHING` |
| `sealRecommendation` | `DO-NOT-SEAL` |
| `registerRow` / `file08StatusToken` | `DR-117` / `OPEN` |
| `head` | `df1301a8b6eeb7c91cc3c616b3aa0eecfe53bc99` (= commit "D-206: record language-quality leftover-join.v3", 2026-08-22) |
| `file08Pin.sha256` | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| `requiredNowUnchanged` | `28` |
| `recordedInputs` | 51 entries (count) |

**`authorityClaim`** (verbatim):

> This artifact PROPOSES the preview-scoped DR-117 successor candidate authorized by D-132 / file 12 §5, remasured after D-167 / D-169 / D-206. leftover-design of unnamed EE classes remains closed (D-157 / D-158 / D-159). It cites g29 leftover-join.v3 (D-204) as the current G29 leftover-join and g30 leftover-join.v3 (D-205) as the current G30 leftover-join. It does not steal OBL-G29-FX-AUTHORING or OBL-G30-FX-AUTHORING. It is not a second register row. It does not SATISFY DR-117. It does not treat product-boundary-successor-contract.v8 or product-boundary-preview.v2 as SATISFIED. It does not add a DR-G* row. It does not change live required-now 28. It does not name G13 into required-now. It applies nothing and does not authorize docs/v2/implementation/. This file existing is not a SATISFIED-GRADE cycle. D-056 Class A is not opened. Gate 1 Class A remains false under D-137's express reservation. Frozen v7 stays unmoved.

**`purpose`** (verbatim):

> Remasure v7 against live HEAD after D-167 / D-169 / D-206. Cite current named-gate leftover-joins. Preserve leftover-design of unnamed EE classes as closed (D-159: gates 2 and 3 hold). Remainder is named-gate execution. Gate 1 Class A remains false under D-137's express reservation until a coordinator act supersedes it. Frozen v7 stays unmoved. Do not SATISFY DR-117. Do not invent a new product-boundary item, fixture bytes, a D9 code, a section 7.1 recipe, a D-006 unit, or the DR-131 pack. Do not name G13 into required-now. Do not steal gate leftover-design.

**`eligibilityNote`** (verbatim):

> D-159 recorded that D-056 Eligibility gates 2 and 3 hold for DR-117. leftover-design of unnamed EE classes is closed. CANDIDATE-NOT-APPLIED is not a Class A bar (D-085 / D-147). binds NOTHING is this artifact's status field, not a cited holding. Gate 1's application-grade / no-express-reservation limb is not established by this file. Gate 1 Class A remains false under D-137's express reservation until a coordinator act supersedes it. This file existing does not perform Gate 4 SATISFIED-GRADE and does not edit file 08. Preview is not MVP (D-018). Live required-now is 28. Frozen v7 is not this remasurement.

**`doesNot`** — 20 entries; the ones bearing on this decision (verbatim): `Does not SATISFY DR-117.` · `Does not open D-056 Class A.` · `This file existing is not a SATISFIED-GRADE cycle and does not mark SATISFIED.` · `Does not replace product-boundary-successor-contract.v8.` · `Does not convert product-boundary-preview.v2 into DR-117 SATISFIED.` · `Does not steal leftover-design of OBL-G29-FX-AUTHORING or OBL-G30-FX-AUTHORING.`

**What the candidate answers** — `registerRowQuoted.acceptanceEvidenceCellVerbatim` = `Explicit successor to P-1/P-2/G3 with enforcement evidence`, split as `CELL-1` `Explicit successor to P-1/P-2/G3` → `sevenItems`, `p1p2g3Mapping` (keys `G3`, `P-1`, `P-2`), `lineage`; and `CELL-2` `with enforcement evidence` → `enforcementEvidence` (keys `status, ownerOfUnownedPreviewClasses, cellAnswer, v1SlicePin, classes`), the limb's `registerRowQuoted.cellLimbs[CELL-2].standing` beginning `Answered as specified-classes-not-executed for admission/request exclusions and for honesty/disclosure of unprevented trusted-TCB ambient effects. The classes are named at live condition-4 / DR-G* obligations (D-157 / D-158 / D-159). Remainder is execution.`

`sevenItems.countPin` (verbatim): `D-011, seven items. Any change to that enumeration re-opens DR-117.` `sevenItems.sourceSha256` = `1811c682…` (file 02; reproduces at HEAD). The seven `dispositions` (`name` → `preview`, verbatim):

1. `marketplace/catalog and governance depth` → `NO. First-party / explicitly trusted components only. No marketplace.`
2. `external lifecycle parity and discovery` → `NO public lifecycle parity. Host-owned one lifecycle for first-party components.`
3. `contribution roles beyond narrow/data-only` → `NO. P-2 narrow producers / data-only remains. Findings stay host-owned (DR-133 / D-136 candidate). Persistence, rendering, termination, and host lifecycle remain host-owned; they are not DR-133's output-law surface.`
4. `untrusted native or WASM admission and required enforcement evidence` → `NO admission. DR-128 stays post-MVP. DR-G21 is not a sandbox. Demonstrated OS/WASM enforcement, matrix, escape tests, revocation, incident ownership attach to DR-128, not condition 4. Preview enforcement is EE-4.`
5. `imperative contributions, probes, project hooks, and root commands` → `NO as contribution roles. Imperative contributions as a class, contribution-owned probes, project hooks, and contributor-owned root commands remain excluded. Host-owned consented doctor probes remain host acts under D-002 / D-032. No contributor owns a root command. Analyze stays offline.`
6. `network-granted analysis and egress defaults` → `NO. Offline preview. No network-granted analysis default.`
7. `replacement of the full-default G3 physical substrate` → `PARTIAL, recorded: TypeScript is the only preview language role. Default useful install is signed distribution core + semantic host + one selected TypeScript closure + the future DR-131 pack (pack not invented here). Core-only is recovery/management, not the analysis product. rustc_driver sidecar remains the substrate and is deferred as a supported analysis role, not abandoned. D-002 independent-release surface is preserved, not narrowed.`

Item 7 is the product statement that DR-G30 (file 08 line 366) executes; it matches file 12 §5's bullet `default useful install = signed distribution core + semantic host + one selected TypeScript closure + the DR-131 pack` (`docs/v2/architecture/12-architecture-completion-goal.md` lines 101–121, sha256 `a2de0b4c4a104837b0f7a5731073d039778b30ef182e1faac815a14cd2c55e92`).

`enforcementEvidence.status` = `specified-classes-not-executed`; 14 classes (`EE-1, EE-2, EE-3a, EE-3b, EE-4, EE-5a, EE-5b, EE-6a, EE-6b, EE-7a, EE-7b, EE-7c, EE-7d, EE-7e`); each class object has at least the keys `existingGate, id, input, invariant, item, laterExecution, owner, pass` (EE-7a, EE-7b, EE-7c, EE-7d, EE-7e also carry `subLimb`) — **no per-class `leftoverDesign` field**. Routing by `existingGate` first clause: EE-1/2/3b/4/5a/5b/6a → `DR-G29 (D-157)`; EE-3a → `DR-G21 (D-145) and DR-G23 (D-147)`; EE-6b → `DR-G09 leftover of DR-105`; EE-7a/7b/7d → `DR-G30 (D-158)`; EE-7c → `DR-G14 only (D-159 names DR-117 EE-7c)`; EE-7e → `DR-G16 (D-159 names DR-117 EE-7e)`.

### 3a. Pin currency at HEAD (measured)

| Pinned input | Candidate cites | Now | Effect |
|---|---|---|---|
| HEAD | `df1301a` (D-206) | `4abb961` (D-292) | 86 COORD entries later |
| file 08 | `f909ddff…` | `e503b75b…` (moved once, D-236) | DR-117 / G29 / G30 rows byte-identical |
| file 02 | `1811c682…` | `1811c682…` | unchanged |
| g29 leftover-join | v3 (D-204) | v4 (D-254) | superseded |
| g30 leftover-join | v3 (D-205) | v4 (D-255) | superseded |
| g09 leftover-join | v10 (D-189) | v12 (D-288) | superseded |
| language-runtime (G14) | v4 (D-179) | v7 (D-274) | superseded |
| g16 leftover-join | v3 (D-192) | v5 (D-278) | superseded |
| g21 leftover-join | v4 (D-196) | v13 (D-292) | superseded |
| g23 leftover-join | v4 (D-198) | v8 (D-240) | superseded |
| permission (DR-105) | v9 (D-171) | v12 (D-283) | superseded |
| distribution-core (DR-101) | v7 (D-173) | v9 (D-287) | superseded |
| monorepo (DR-121) | v3 (D-181) | v4 (D-277) | superseded |
| language-quality (DR-118) | v3 (D-206) | v5 (D-273) | superseded |
| doctor-actor (DR-114) | v11 (D-170) | v12 (D-285) | superseded |

All twelve leftover-joins the candidate cites as "current" have been superseded since 2026-08-22. The candidate's own `remeasurementClause` (verbatim): `If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene, with file 08, v7, both v7 Stage A verdicts, current leftover-joins named in basedOn, file 02, v1-slice, and this draft unmoved, re-measure before recording.` D-207 was itself the re-measurement of v7 on exactly this ground (`purpose`: `Remasure v7 against live HEAD after D-167 / D-169 / D-206.`). Whether a v9 is required before a Class A act is not decided anywhere in the record; see §9 and DECISIONS-NEEDED A4.

---

## 4. Both Stage A reviews of the candidate

### 4a. Claude 2

Path `docs/coop/artifacts/preview-product-boundary-successor.v8.review-independent.claude2.json`, sha256 `4f71ccfc3a89fd0b5fc1a2f393a3864e8a2b5f1c792c0b696c63f831c05e2bca` (matches D-207 "Stage A Claude ACCEPT"). `date` `2026-08-22`. `verdict` `ACCEPT`. `blockers` `[]`. `shouldFix` `[]`. Two advisories: `CLAUDE-PPBS-V8-ADV-1` (location `basedOn.doctorActorJoinV11`, pinning asymmetry) and `CLAUDE-PPBS-V8-ADV-2` (location `remeasurementClause`, enumeration subset).

`acceptanceGrade` (verbatim):

> ACCEPT as an independently reviewed DR-117 preview-scoped successor candidate, remasured at live HEAD df1301a / required-now 28. This verdict applies nothing, records nothing, marks no row SATISFIED, opens no Class A, satisfies no DR-117 limb, steals no gate leftover-design, names no G13, invents no fixture bytes and no DR-131 pack, and authorizes no docs/v2/implementation/. The subject's own status fields govern: CANDIDATE-NOT-APPLIED, DO-NOT-SEAL, binds NOTHING, AWAITING-INDEPENDENT-REVIEW. Gate 1 Class A remains false under D-137's express reservation; nothing in this verdict lifts it.

`standingAdvisoryCarriedForward` (`CLAUDE-PPBS-V3-ADV-1`), verbatim limbs:
- `venueLimb`: `Stands. The subject states it against its own interest: the artifact refuses Class A in terms, and the venue for lifting D-137's reservation is a reviewed coordinator decision, not this artifact.`
- `openItemForTheCoordinator`: `The advisory's original remedy - that the recording entry make the eligibility gap visible on the register rather than leaving it inside the artifact - remains addressed to the coordinator and is not something this artifact or this verdict can discharge.`

`whatThisVerdictDoesNotDo` includes (verbatim): `Does not open D-056 Class A and does not lift D-137's express reservation.` and `Does not claim Gate 1 Class A holds.`

### 4b. Codex

Path `docs/coop/artifacts/preview-product-boundary-successor.v8.review-independent.codex.json`, sha256 `5176f1de3713915cd8b5fbc2bafbd596b6d6fa285d68a299fdfbfee9375c1078` (matches D-207 "Stage A Codex ACCEPT"). `date` `2026-08-22`. `verdict` `ACCEPT`. `blockerCount` `0`. `shouldFixCount` `0`. `advisories` `[]`. `subjectMovedDuringReview` `false`.

`finalStanding` (verbatim): `ACCEPT. This verdict is review evidence only. It is not the coordinator recording, does not apply the candidate, and changes no live row or required-now membership.`

`authorityBoundaryAudit.eligibility` (verbatim JSON):

```json
{
  "gate1ClassA": false,
  "gate1Authority": "D-137 express reservation remains controlling",
  "gate2": "HOLDS per D-159",
  "gate3": "HOLDS per D-159",
  "gate4": "NOT-PERFORMED",
  "gate5": "NOT-PERFORMED"
}
```

### 4c. T2-02 reservation-language sweep of both verdicts (the test D-015 applied to DR-102)

The D-001 property (COORD line 181–190, verbatim): `a candidate is applicable when its independent review returns **0 blockers AND grants application-grade acceptance with no express reservation** — no candidate-only limitation, no EXPRESSLY-NOT-FOR-APPLICATION language, no named apply-condition left undischarged on the record`. D-015 recorded DR-102's contract as meeting it by a sweep: `Reservation-language sweep of the VERDICT clean — three `reserv` hits, all forms of "preserve" […]; zero acceptance reservations.`

Measured on the v8 verdicts (case-insensitive substring counts):

| Verdict | `candidate` | `reserv` (any) | `reservation` (whole word) | `application-grade` |
|---|---|---|---|---|
| Claude 2 | 9 | 13 | 8 — e.g. `Gate 1 Class A remains false under D-137's express reservation; nothing in this verdict lifts it.` (`acceptanceGrade`); `the venue for lifting D-137's reservation is a reviewed coordinato…` | 1 — inside an `attackRun` cell (`attack` `Gate 1 Class A claimed to hold`, `result` `NOT FOUND`) that quotes the subject's `eligibilityNote` sentence `Gate 1's application-grade / no-express-reservation limb is not established by this file.`; not the reviewer's own words |
| Codex | 6 | 12 | 2 — e.g. `Gate 1's application/no-reservation limb is expressly unesta[blished]`; the other `reserv` hits are `preserves` / `reserved` (G13) | 0 |

Reading in bytes: both verdicts are `ACCEPT` at `0/0`. Codex states in its own words that `Gate 1's application/no-reservation limb is expressly unestablished`. Claude 2's own words are `Gate 1 Class A remains false under D-137's express reservation; nothing in this verdict lifts it.` (`acceptanceGrade`) and `Does not claim Gate 1 Class A holds.` (`whatThisVerdictDoesNotDo`); its single `application-grade` hit is the subject's `eligibilityNote` quoted inside an `attackRun` cell. Neither verdict contains a grant of application-grade acceptance, and neither lifts D-137. Whether a Class A opening may rest on these two verdicts plus the owner's word, or requires a fresh grade-clarification review, is not decided in the record; the only precedent for the latter is D-005's remedy wording (COORD lines 656–662): `a targeted grade-clarification review putting the NEUTRAL question — "is this acceptance application-grade once its named condition is discharged?" — to a fresh reviewer against the review's frozen bytes`.

---

## 5. D-056's five eligibility gates — per-gate byte evidence for DR-117

Definition: D-133 Decision (verbatim): `A later SATISFIED re-record may use D-056 only when all five gates in the pinned turn-2 subject hold for that row at that later cycle.` The pinned turn-2 subject is `docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md` `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82` (reproduces on disk). Its `## Eligibility (narrow)` section (heading line 95; gate text lines 97–123), verbatim gate text, followed by DR-117's evidence:

**Gate 1** — `One of: **Class A.** An independently accepted design contract exists at 0 blockers with application-grade acceptance and no express reservation (D-001 T2-02), recorded by a D-000 entry; the row's lead label is `OPEN`.` (Class B is inapplicable: lead label is not `DECIDED-V1-NOT-INTEGRATED`.)

| Limb | DR-117 evidence | Holds? |
|---|---|---|
| independently accepted design contract at 0 blockers | v8 Claude ACCEPT `0/0` (`4f71ccfc…`), Codex ACCEPT `0/0` (`5176f1de…`), recorded by D-207 | yes (bytes) |
| application-grade acceptance | Claude 2 (own words): `acceptanceGrade` `Gate 1 Class A remains false under D-137's express reservation; nothing in this verdict lifts it.`; `whatThisVerdictDoesNotDo` `Does not claim Gate 1 Class A holds.` (its only `application-grade` text quotes the subject's `eligibilityNote`, §4c); Codex (own words): `Gate 1's application/no-reservation limb is expressly unestablished` | **no** (bytes) |
| no express reservation | D-137: `D-056 Class A is not opened.`; D-207: `Gate 1 Class A remains false under D-137's express reservation. v8 does not withdraw that reservation.`; candidate `authorityClaim`: `D-056 Class A is not opened.` | **no** (bytes) |
| recorded by a D-000 entry | D-207 ADOPTED, dual CONSENT | yes |
| lead label `OPEN` | file 08 line 299 Status `OPEN` | yes |

Clarification already in the record (D-147 Decision, verbatim): `CANDIDATE-NOT-APPLIED is not a Class A bar (D-085).` — i.e. the artifact's status token is not what blocks Gate 1; the express reservation in the recordings is.

**Gate 2** — `Every remaining acceptance-evidence member is **only** harness *execution*, fixture *execution*, or qualification *measurement*. Authoring of fixtures, schemas, successors, actor-joins, missing design, or still-UNDECIDED numbers is **not** a remainder this amendment may split.`

- For: D-159 Decision: `After this recording, D-056 Eligibility gates 2 and 3 hold for DR-117.` D-168 and D-207: `D-056 Eligibility gates 2 and 3 continue to hold for DR-117 (D-159).` Codex v8 audit: `"gate2": "HOLDS per D-159"`. Candidate `enforcementEvidence.status`: `specified-classes-not-executed`; every EE class `existingGate` says `Remainder is G29 execution` (or G30/G09/G14/G16/G21/G23 execution).
- Against (bytes the owner should weigh): the two gate joins that hold DR-117's remainder both carry a fixture-**authoring** leftover flagged `"leftoverDesign": true` — g29 v4 `OBL-G29-FX-AUTHORING` with `"rideStanding": "not-capable-of-riding as execution-only remainder"` and reason `D-056 Decision clause 5: authoring fixtures remains design work.`; g30 v4 `OBL-G30-FX-AUTHORING`, same wording (§6b–6c). `STATUS.2026-08-26.md` §2 item 2 states the general rule: `D-056 clause 5: authoring fixtures is design work, so a row with unauthored fixtures is ineligible.`
- Precedent on the same tension: DR-102 was recorded `SATISFIED` under Class A (D-085, 2026-08-14) with its remainder `CC-1..CC-11 *execution*` at DR-G21 (asterisked form from file 08 line 284, `CC-1..CC-11 *execution* remains owed at DR-G21`; D-085 Decision: `CC-1..CC-11 execution remains condition 4 / DR-G21 / DR-012`), and today's current G21 join, `g21-leftover-join.v13` (D-292), still lists `["OBL-G21-FX-AUTHORING"]` as `leftoverDesign: true` (measured). DR-104 was recorded `SATISFIED` under Class B (D-236) with `Negative-test execution` remaining at DR-G31 (file 08 line 286: `Negative-test execution remains condition 4 / DR-G31 / DR-012 qualification`). The record has therefore treated gate-side fixture authoring as condition-4 work rather than as the row's acceptance-evidence remainder in two prior SATISFIED acts. Whether that reading applies to DR-117 is for the owner and the SATISFIED-GRADE reviewers; it is not settled by any entry naming DR-117.

**Gate 3** — `Each such remainder is already named as a condition-4 / DR-G* obligation with an owner. Naming a harness identifier is not itself SATISFIED.`

Evidence: DR-G29 (file 08 line 365, D-157) owner `Product owner`; DR-G30 (line 366, D-158) owner `Product owner`; D-159 Decision: `DR-G09 names DR-117 EE-6b. DR-G14 names DR-117 EE-7c. DR-G16 names DR-117 EE-7e.`; EE-3a → `DR-G21 (D-145) and DR-G23 (D-147)` (candidate class EE-3a). Candidate `enforcementEvidence.ownerOfUnownedPreviewClasses`: `No preview EE class remains unowned. D-157 / D-158 / D-159 named every class that v5 marked owner=this-candidate.` Codex: `"gate3": "HOLDS per D-159"`. Holds (bytes).

**Gate 4** — `A dedicated later D-000 cycle plus independent SATISFIED-GRADE review of *that row* accepts the split and records SATISFIED under this amendment.` — D-207: `Gates 4 and 5 are not performed.` Codex: `"gate4": "NOT-PERFORMED"`. Not performed.

**Gate 5** — `An MF-6 file-08 cell edit records SATISFIED and removes the cell's conflicting "until executed" / "until measured" SATISFIED-bar. This entry is not that edit.` — Not performed (same bytes). The DR-117 Status cell is the bare token `OPEN`; it carries no "until executed" bar text, so the edit would be a replacement of `OPEN` and of the Blueprint-impact cell (§8).

Summary in one line (all from bytes): gates 3 hold; gate 2 is recorded as holding (D-159/D-207) with an unresolved fixture-authoring tension the record has previously tolerated; gate 1 fails on the application-grade / no-express-reservation limb only; gates 4 and 5 are unperformed and would be the SATISFIED-GRADE cycle plus MF-6.

---

## 6. The current DR-117 leftover-join

**Measured:** none of the 38 `*-leftover-join.vN.json` lineages in `docs/coop/artifacts/` has `registerRow` = `DR-117` (checked every file). The record's DR-117 leftover lineage is instead:

| Step | Artifact | sha256 | Recorded | What it holds |
|---|---|---|---|---|
| leftover-design measurement | `preview-product-boundary-ee-gate-join.v1.json` | `ae20b25fcb908a19fcd38dbb8e7c5963eee983b566132936c4bd1e7af34b3de0` | D-155 (2026-08-15) | 14 `classes` with `leftoverDesign` flags at that date: `true` for EE-1, EE-2, EE-3b, EE-4, EE-5a, EE-5b, EE-6a, EE-7a, EE-7b, EE-7d (10); `false` for EE-3a (`existingGate` `none`), EE-6b (`DR-G09`), EE-7c (`DR-G14`), EE-7e (`DR-G16`) (4). D-155: `Gates 2 and 3 do not hold.` |
| leftover grouping | `preview-product-boundary-admission-leftover.v1.json` | `6280d64867433a963a4ce0bcc44521c57c485b0eea19404b4740c36c94ef4cce` | D-156 | two `proposedObligations`: `proposedKind` `PREVIEW-BOUNDARY-EXCLUDED-FORM-ADMISSION` and `PREVIEW-BOUNDARY-INSTALL-SHAPE`, each `status` `candidate-not-adopted`, `owner` `Product owner` — later minted as DR-G29 (D-157) and DR-G30 (D-158) |
| leftover remasurement | `preview-product-boundary-successor.v7.json` | `243c12a2…` | D-168 | historical (`Frozen v7 remains a historical measurement`, D-207) |
| **current** leftover remasurement | `preview-product-boundary-successor.v8.json` | `f2e788e5…` | **D-207** | the B3 candidate; 14 EE classes, no per-class `leftoverDesign` field (§3) |

The `leftoverDesign: true` flags for DR-117's remainder therefore live on the **gate** joins, which the candidate cites at v3 but which are now v4:

### 6a. `g29-leftover-join.v4.json` — sha256 `9e1af4ba3b21e483154825fa2c6d275f7ee805d1fb455f01c9d35e48411c3f64` (matches D-254), `date` `2026-08-23`, `registerRow` `DR-G29`, `status` `CANDIDATE-NOT-APPLIED`, `binds` `NOTHING`; no top-level `leftoverDesign` key (the flag is carried per obligation only)

| `id` | `leftoverDesign` | `existingGate` | `executionObligationOwnerToday` | `rideStanding` |
|---|---|---|---|---|
| `OBL-G29-HARNESS-SPEC` | `false` | `DR-G29` | `Product owner` | `qualification-at-named-gate` |
| `OBL-G29-NAMED-CORPUS` | `false` | `none. Live harness-cell naming only.` | `Product owner` | `specified-not-leftover` |
| `OBL-G29-INPUT-CORPUS` | `false` | `none. INPUT-state corpus only.` | `Product owner` | `specified-not-leftover` |
| `OBL-G29-FX-AUTHORING` | **`true`** | `none as authored implementations` | `none` | `not-capable-of-riding as execution-only remainder` |
| `OBL-G29-EXECUTION` | `false` | `DR-G29` | `Product owner` | `qualification-at-named-gate` |
| `OBL-EE-UNNAMED-REMAINDER-CLOSED` | `false` | `none. Closed at D-157 as unnamed remainders.` | `none as leftover-design` | `specified-not-leftover` |

`OBL-G29-FX-AUTHORING.namedCorpusNotAuthored` (verbatim): `hostile-but-well-formed excluded-form admission corpus and post-admission/pre-stage substitution-mutation corpus (DR-117 EE-1, EE-2, EE-3b, EE-4, EE-5a, EE-5b, EE-6a)`. D-254 Decision: `leftover-design of OBL-G29-FX-AUTHORING remains on leftover-join.v4. […] Occupancy v3 is the current G29 occupancy remasurement.`

### 6b. `g30-leftover-join.v4.json` — sha256 `3f3d84e0e24a2aea0ba95c282f809c8343d1827d0577ca8396d4560c5e012c75` (matches D-255), `date` `2026-08-24`, `registerRow` `DR-G30`, `status` `CANDIDATE-NOT-APPLIED`, `binds` `NOTHING`; no top-level `leftoverDesign` key (the flag is carried per obligation only)

| `id` | `leftoverDesign` | `existingGate` | `executionObligationOwnerToday` | `rideStanding` |
|---|---|---|---|---|
| `OBL-G30-HARNESS-SPEC` | `false` | `DR-G30` | `Product owner` | `qualification-at-named-gate` |
| `OBL-G30-NAMED-CORPUS` | `false` | `none. Live harness-cell naming only.` | `Product owner` | `specified-not-leftover` |
| `OBL-G30-INPUT-CORPUS` | `false` | `none. INPUT-state corpus only.` | `Product owner` | `specified-not-leftover` |
| `OBL-G30-FX-AUTHORING` | **`true`** | `none as authored implementations` | `none` | `not-capable-of-riding as execution-only remainder` |
| `OBL-G30-EXECUTION` | `false` | `DR-G30` | `Product owner` | `qualification-at-named-gate` |
| `OBL-EE7ABD-UNNAMED-REMAINDER-CLOSED` | `false` | `none. Closed at D-158 as unnamed remainders.` | `none as leftover-design` | `specified-not-leftover` |

### 6c. G30 useful-install selection (the product statement DR-117 item 7 delegates to G30)

- File 08 line 366 (quoted in §1a): `Preview useful-install selection is signed distribution core + semantic host + one TypeScript closure + future DR-131 pack; core-only is not the analysis product; a second preview language role is refused; the rustc_driver sidecar is deferred not abandoned.`
- g30 v4 `OBL-G30-EXECUTION.reason` (verbatim): `G30's live claim owns preview useful-install advertisement, TypeScript-only role-list, and sidecar deferred-not-abandoned product-statement. Execution remains qualification (D-056). This join does not execute fixtures and does not claim QUALIFIED.`
- g30 v4 `OBL-G30-FX-AUTHORING.namedCorpusNotAuthored`: `useful-install advertisement, role-list, and product-statement corpus (DR-117 EE-7a, EE-7b, EE-7d)`; its reason adds `does not invent the DR-131 pack, and does not mint Rust-as-core`.
- Candidate class EE-7a `owner` (verbatim): `DR-117 / DR-G30 (D-158) for the aggregate default-useful-install selection and the core-only-is-not-analysis-product rule. DR-101 / D-114 distribution-core-inventory owns only the signed-distribution-core inventory and excludes analyzer components from that core closure.`
- Note the selection names `future DR-131 pack` — DR-131 is itself Class-A-unopened (Packet B1). The G30 corpus is unauthored (`OBL-G30-FX-AUTHORING` true), so nothing about the useful-install selection has been executed; it is a specified product statement.

### 6d. Currency caveat

`STATUS.2026-08-26.md` line 36 states: `Not candidates: lifecycle/monorepo/signed-index/DR-117 joins only cite a superseded *GATE* join; COORD (D-276/D-278/D-281) explicitly keeps those current.` Measured: the D-276, D-278 and D-281 entries mention DR-117 only in the phrase `Does not SATISFY DR-117`; none names `preview-product-boundary-successor.v8` or states its currency. The claim that the DR-117 join is "kept current" by those entries is therefore a STATUS reading of precedent, *not in the record* as a DR-117-specific statement. (See open question 4.)

---

## 7. Pre-drafted T2-02 acceptance entry — **DRAFT, NOT RECORDED, NOT REVIEWED**

Takes effect only if the owner rules for opening (§9 options B/C/D). Modelled on D-085's turn-3 recitation (`coordinator-decisions.D-085.turn3.draft.md` "Eligibility recitation" lines 36–63) and D-137/D-207's entry form. Values in `⟨…⟩` are *not in the record* and must be supplied by the act itself. The owner's own words go in the "User words" block, recorded verbatim as D-132 did.

```
## D-⟨NNN⟩ — Open D-056 Class A for DR-117: T2-02 acceptance of preview-product-boundary-successor.v8

- **Date:** ⟨date⟩
- **Status:** ⟨to be filled by the D-000 cycle: reviewer paths, digests, turn, CONSENT/OBJECT⟩
- **Decision type:** PREFERENCE-LADEN product decision by the Product owner (file 08 line 299
  owner cell; D-001 route C), recorded by the orchestrator; RULE-GOVERNED as to form (D-056
  Gate 1; D-001 T2-02). Supersedes, for DR-117 only, the express reservation "D-056 Class A is
  not opened" recorded at D-137 and carried by D-155, D-156, D-159, D-168, and D-207. Not a
  SATISFIED re-record. Not an MF-6 edit. Does not edit file 08.
- **Subject:** `docs/coop/artifacts/preview-product-boundary-successor.v8.json`
  `f2e788e51c347e1033073f0718e701d164affe51e7f667da9bcd49a08837144c` (D-207).
  Stage A verdicts: Claude `4f71ccfc3a89fd0b5fc1a2f393a3864e8a2b5f1c792c0b696c63f831c05e2bca`
  ACCEPT 0/0; Codex `5176f1de3713915cd8b5fbc2bafbd596b6d6fa285d68a299fdfbfee9375c1078`
  ACCEPT 0/0.
- **User words, recorded verbatim (⟨date⟩):** ⟨the owner's instruction opening Class A for DR-117⟩
- **T2-02 recitation (D-001, COORD line 181):** 0 blockers — MET (both Stage A verdicts).
  Application-grade acceptance with no express reservation — ⟨ONE OF: (i) "granted by this act
  on the Product owner's word; the D-137 reservation is lifted for DR-117"; OR (ii) "granted by
  the fresh grade-clarification review at ⟨path⟩ ⟨sha256⟩ answering the NEUTRAL question
  'is this acceptance application-grade?' (D-005 remedy form) at 0 reservations"⟩.
  Candidate-only limitation — ⟨statement that the Stage A verdicts' candidate language is
  superseded by this act / by the fresh review⟩. Named apply-condition — none on the record.
- **Decision:** For DR-117 only, D-056 Gate 1 Class A holds from this entry: the accepted
  design contract is `preview-product-boundary-successor.v8` at 0 blockers with
  application-grade acceptance and no express reservation, recorded by D-207 and this entry;
  the lead label is `OPEN`. Gates 2 and 3 continue to hold per D-159 / D-207. Gates 4 and 5
  are NOT performed here; a later dedicated SATISFIED-GRADE cycle of DR-117 and its MF-6 edit
  remain owed. DR-117 stays `OPEN`. Not SATISFIED. Not QUALIFIED. The candidate's status
  fields `CANDIDATE-NOT-APPLIED` / `binds NOTHING` / `DO-NOT-SEAL` are artifact fields, not
  reservations (D-147). `product-boundary-successor-contract.v8` (D-116) ⟨remains the leftover
  T2-02 candidate for general succession / is superseded — owner to state⟩. Does not steal
  OBL-G29-FX-AUTHORING or OBL-G30-FX-AUTHORING. Does not name G13 into required-now.
  Does not invent fixture bytes or the DR-131 pack. Does not open Class A for DR-131 or
  DR-133. Does not authorize `docs/v2/implementation/`. Required-now stays 28.
- **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET
  (28 of 28). Condition 5 last.
- **Reversibility:** Total before the dependent SATISFIED-GRADE cycle lands; afterwards
  requires that cycle's supersession. Overturn: C-D⟨NNN⟩. Restores D-137's reservation as
  controlling. Does not unwrite D-137, D-159, or D-207.
- **Commit:** C-D⟨NNN⟩.
```

Follow-on (not drafted here): the SATISFIED-GRADE cycle (Gate 4) plus MF-6 (Gate 5), in the D-085 form, whose recitation would cite this entry for Gate 1 and list the named remainder: G29 (EE-1, EE-2, EE-3b, EE-4, EE-5a, EE-5b, EE-6a), G30 (EE-7a, EE-7b, EE-7d), G09 (EE-6b), G14 (EE-7c), G16 (EE-7e), G21/G23 (EE-3a) execution. Whether the Class A opening and the SATISFIED-GRADE cycle are one act or two is Option D versus B/C in §9.

---

## 8. The exact file-08 cells that would change

**Nothing in file 08 changes at the Class A opening itself** — D-137 and D-207 were "no-cell-edit" recordings and the DRAFT in §7 says `Does not edit file 08`. (Whether an interim MF-6 note like D-141 (COORD line 5967, heading verbatim: `File 08 MF-6: record accepted candidate on DR-131`) is wanted for DR-117 is *not in the record*; the DR-117 row never received one.)

At the later SATISFIED-GRADE + MF-6 act (Gate 5), the cells are (line 299):

| Cell | Now (verbatim) | DRAFT after (form copied from DR-102 line 284 / DR-104 line 286; every `⟨…⟩` is not in the record) |
|---|---|---|
| Status | `OPEN` | `**SATISFIED ⟨date⟩ (D-⟨NNN⟩ / D-056 Class A).** Design-contract candidate `preview-product-boundary-successor.v8` (`f2e788e5…`) recorded 2026-08-22 (D-207) at dual ACCEPT 0/0; Class A opened by D-⟨class-A entry⟩. EE-class *execution* remains condition 4 at DR-G29 (EE-1, EE-2, EE-3b, EE-4, EE-5a, EE-5b, EE-6a), DR-G30 (EE-7a, EE-7b, EE-7d), DR-G09 (EE-6b), DR-G14 (EE-7c), DR-G16 (EE-7e), DR-G21/DR-G23 (EE-3a); it is not architecture SATISFIED evidence. Fixture authoring OBL-G29-FX-AUTHORING / OBL-G30-FX-AUTHORING remains on the G29 / G30 leftover-joins. Not QUALIFIED. D-011's seven-item count pin stands.` |
| Blueprint impact | `Hard blocker; V1 exclusions remain until closed` | `Architecture-preview SATISFIED under D-056 Class A (D-⟨NNN⟩). EE-class execution remains condition 4 / DR-G29 / DR-G30 / DR-G09 / DR-G14 / DR-G16 / DR-G21 / DR-G23 / DR-012 qualification, not an architecture hard blocker.` |

Snapshot cells (per D-236 precedent, COORD line 11157: `Rewrite condition 2 to 5 of 32 SATISFIED, standing NOT MET`; D-085 used the same form with its own numbers: `Rewrite condition 2 to 1 of 30 SATISFIED, standing NOT MET`): line 415 `**5 of 32 `SATISFIED`** — 24 `OPEN`` → `6 of 32` / `23 OPEN`, adding a DR-117 remainder clause; line 424 `condition 2 remains 5 of 32 SATISFIED` → `6 of 32`. Standing stays `**NOT MET**`. Decision, Owner, Source-pin, and Required-acceptance-evidence cells are untouched (D-085 replaced only "the DR-102 lead, SATISFIED-bar, and Blueprint-impact hard-blocker").

---

## 9. Options with consequences

**A. Do not open Class A; keep D-137's reservation.**
Consequences: DR-117 stays `OPEN`; Condition 2 stays `5 of 32`; the handoff's completion bar item `(3) DR-117 SATISFIED` (HANDOFF line 3) stays unmet; no cycle spent; the G29/G30 fixture-authoring leftover (§6) is untouched either way. D-207 Reversibility names four dependent-act classes (`a later dependent leftover rewrite, Class A reservation lift, SATISFIED cycle, or file-08 cell rewrite`, §2c); measured, none has landed — no COORD line after D-207 names `preview-product-boundary-successor.v8` (§2c).

**B. Open Class A now by coordinator act on v8 as it stands (§7 DRAFT limb (i)), then a separate SATISFIED-GRADE + MF-6 cycle.**
Consequences: two D-000 cycles (dual Stage B each). Risks the owner should know, all from bytes: (1) Codex says Gate 1's application/no-reservation limb is `expressly unestablished`, Claude 2 says `Does not claim Gate 1 Class A holds.`, and both carry candidate-only language (§4c) — a strict T2-02 reviewer may OBJECT that no application-grade *review* exists and the owner's word is standing in for one; (2) all twelve leftover-joins v8 cites are superseded (§3a) — a reviewer may demand a v9 remasurement first (D-207 is the precedent for exactly that demand); (3) the Gate 2 fixture-authoring reading (§5) will be tested at the SATISFIED-GRADE cycle, where DR-102/DR-104 are the only precedents.

**C. First cure the record, then open: (C1) author `preview-product-boundary-successor.v9` re-citing the twelve current joins (or rely on A4's content-based reading if adopted — note v8 has no `leftoverDesign` partition, so whether A4 even reaches it is *not in the record*); and/or (C2) dispatch a grade-clarification review putting the NEUTRAL question (D-005 form) to fresh reviewers so that an application-grade verdict exists in bytes; then the §7 act with limb (ii).**
Consequences: +1 to +2 Stage A cycles (~30–45 min each when reviews pass first time, STATUS §3A) before the opening; cleanest T2-02 record; lowest objection risk at Stage B; the owner's product decision is still required (reviewers cannot lift D-137).

**D. Open Class A and record SATISFIED in one combined act (D-085 form: Gate 1 recitation + SATISFIED-GRADE + MF-6).**
Consequences: fastest path to `6 of 32`; a three-limb act carrying every risk in B at once; the record has no precedent for opening Class A and SATISFYING in the same entry (D-085's Gate 1 was already met at D-015).

**E. "What must change first" (owner may name any):** e.g. authorship of the G29 / G30 fixtures (DECISIONS-NEEDED D1 delegation) before SATISFIED; a decision on which artifact is *the* DR-117 contract (§2a — the preview v8 says it `does not replace` contract.v8); or a change to the seven dispositions (§3) — any change to the seven-item enumeration `re-opens this row` (line 299), but changing a *preview disposition* within the seven is a new candidate, not a row re-open.

**Orchestrator recommendation:** Option C with C2 only (skip the v9 remasurement if DECISIONS-NEEDED A4 is adopted, otherwise include C1), then the §7 act, then the SATISFIED-GRADE cycle as a separate entry — because the only Gate-1 failure in bytes is the absence of an application-grade verdict, and that is curable by a review the owner does not have to write, while the product decision itself (the seven dispositions in §3) is already the owner's under D-132 and needs only the owner's word to lift D-137.

---

## 10. Open questions not resolvable from bytes

1. **Which artifact is "the" DR-117 design contract for Class A?** The preview lineage's v8 (D-207) states it `does not replace, apply, or succeed` `product-boundary-successor-contract.v8` (D-116), which D-137 calls `the D-116 leftover T2-02 candidate`. No entry says which of the two a Class A opening names, or whether both must be accepted.
2. **Does the owner's word alone satisfy T2-02's "application-grade acceptance with no express reservation", given Codex says that limb is `expressly unestablished` and Claude 2 says `Does not claim Gate 1 Class A holds.` (§4c)?** No precedent opens Class A by owner instruction; DR-102's Gate 1 was met by a reviewer verdict with a clean reservation sweep (D-015).
3. **Gate 2 versus gate-side fixture authoring:** D-159/D-207 record gates 2 and 3 as holding for DR-117 while g29/g30 v4 flag `OBL-G29-FX-AUTHORING` / `OBL-G30-FX-AUTHORING` `leftoverDesign: true` and `not-capable-of-riding as execution-only remainder`. DR-102 (G21) and DR-104 (G31) were SATISFIED under the same shape; no entry states the rule for DR-117.
4. **Currency of v8:** every one of its twelve cited leftover-joins is superseded (§3a). STATUS line 36 attributes a "kept current" holding to D-276/D-278/D-281, but those entries do not name the DR-117 join. Whether a v9 is required before any Class A act, or A4's content-based reading covers a candidate with no `leftoverDesign` partition, is undecided.
5. **Interim file-08 note:** whether a D-141-style MF-6 note recording the accepted candidate / Class A opening in the DR-117 row is wanted before SATISFIED is not in the record.
6. **Standing advisory CLAUDE-PPBS-V3-ADV-1 venue limb** (`openItemForTheCoordinator`: make the eligibility gap `visible on the register rather than leaving it inside the artifact`) remains addressed to the coordinator; no entry discharges it.

---

## 11. Citations relied on

- `DECISIONS-NEEDED.md` §B lines 33–38 (heading line 33; B1 34–35; B2 36; B3 37–38); §A4 lines 23–31. Untracked file; line numbers re-measured at packet time.
- `STATUS.2026-08-26.md` §1 table row 2; §2 items 1–2; §3A line 36; §3A item 12 line 43; "Left current by precedent" paragraph line 44.
- `HANDOFF.D-000-orchestrator-live.txt` line 3 (completion bar), lines 79–83 ("Do not invent / do not SATISFY").
- `docs/v2/architecture/08-decision-and-readiness-register.md` (`e503b75b…`): line 280 (table header; 281 is the separator row), line 43 (DR-010), line 284 (DR-102 cell form), line 286 (DR-104 cell form), line 299 (DR-117 row), lines 365–366 (DR-G29, DR-G30), line 415 (Condition 2), line 424 (one-sentence summary); git history: commit `892236a` (`f909ddff…`) and `fc688b1` (`e503b75b…`).
- `docs/v2/architecture/02-distribution-and-components.md` sha256 `1811c682…` at HEAD.
- `docs/v2/architecture/12-architecture-completion-goal.md` (`a2de0b4c…`) line 23; §5 lines 101–121.
- `docs/coop/COORDINATOR-DECISIONS.md` (`47f7b201…`): D-001 line 181–190 (T2-02 property); D-003 lines 524–530 and D-005 lines 645–662 (application-grade readings, NEUTRAL-question remedy); D-015 (DR-102 contract, reservation sweep); D-056 lines 3343–3399 (Decision paragraph, five gates); D-085 (Class A SATISFIED precedent); D-116; D-132 (user grant, Decision item 5); D-133 (gates are a property); D-137 (reservation origin); D-138 (DR-131 parallel); D-147 (`CANDIDATE-NOT-APPLIED is not a Class A bar`); D-155, D-156, D-157, D-158, D-159 (EE naming; gates 2/3); D-168 (v7); D-204, D-205 (g29/g30 v3); D-207 (v8); D-236 (Class B precedent, snapshot rewrite form); D-240, D-254, D-255, D-273, D-274, D-277, D-278, D-283, D-285, D-287, D-288, D-292 (current versions of the twelve cited joins); D-276/D-278/D-281 (searched for DR-117 wording).
- `docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md` (`dfb0c2af…`) lines 95–123 `## Eligibility (narrow)` (heading 95; gate text 97–123).
- `docs/coop/artifacts/coordinator-decisions.D-085.turn3.draft.md` lines 36–63 "Eligibility recitation".
- `docs/coop/artifacts/coordinator-decisions.D-207.draft.md` (`82d08f98…`), `…D-207.review-adversarial.claude2.json` (`0d439cc8…`), `…D-207.review-adversarial.codex.json` (`f16766e2…`).
- `docs/coop/artifacts/preview-product-boundary-successor.v8.json` (`f2e788e5…`): fields `artifact, version, date, documentClass, status, reviewStatus, binds, sealRecommendation, registerRow, file08StatusToken, head, file08Pin, authorityClaim, purpose, eligibilityNote, doesNot, sevenItems.{countPin,sourceSha256,dispositions}, enforcementEvidence.{status,cellAnswer,ownerOfUnownedPreviewClasses,classes[*].{id,existingGate,owner}}, registerRowQuoted, remeasurementClause, leftoverDesignOpenStanding, basedOn.*, lineage.*, recordedInputs (count)`.
- `…preview-product-boundary-successor.v8.review-independent.claude2.json` (`4f71ccfc…`): `verdict, acceptanceGrade, verdictStatement, blockers, shouldFix, advisories, standingAdvisoryCarriedForward, whatThisVerdictDoesNotDo, subject`.
- `…preview-product-boundary-successor.v8.review-independent.codex.json` (`5176f1de…`): `verdict, finalStanding, blockerCount, shouldFixCount, advisories, summary, authorityBoundaryAudit.eligibility, subjectSha256Expected/AtEnd, subjectMovedDuringReview`.
- `…preview-product-boundary-ee-gate-join.v1.json` (`ae20b25f…`): `classes[*].{id,leftoverDesign,existingGate}`, `status, binds, registerRow`.
- `…preview-product-boundary-admission-leftover.v1.json` (`6280d648…`): `proposedObligations[*].{proposedKind,status,owner}`.
- `…g29-leftover-join.v4.json` (`9e1af4ba…`) and `…g30-leftover-join.v4.json` (`3f3d84e0…`): `date, registerRow, status, binds, obligations[*].{id,leftoverDesign,existingGate,executionObligationOwnerToday,rideStanding,namedCorpusNotAuthored,reason}, leftoverDesignOpenStanding`.
- `…g21-leftover-join.v13.json`: `obligations[*].leftoverDesign` (`["OBL-G21-FX-AUTHORING"]`).
- Directory listing of `docs/coop/artifacts/*leftover-join.v*.json` (38 lineages; `registerRow` of every file checked).
