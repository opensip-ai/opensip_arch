# Packet B2 — DR-133 Class A opening (candidate `provider-only-output-contract.v3`, recorded D-136)

Prepared 2026-08-27 by the Claude orchestrator for the human owner (sole decision authority). This packet decides nothing. Every factual claim below carries a citation; every quoted token is verbatim from bytes measured at the pins in §0. Where the record contains no value, the packet says "not in the record".

## 0. Pins at measurement

| What | Value | Source |
|---|---|---|
| HEAD | `4abb961aad98525ca8b992a24609a6286964a451` — `D-292: record g21 leftover-join.v13` | `git rev-parse HEAD`; `git log --oneline -1` |
| file 08 | `docs/v2/architecture/08-decision-and-readiness-register.md` sha256 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` | `sha256sum` |
| COORD | `docs/coop/COORDINATOR-DECISIONS.md` sha256 `47f7b2011ec719dfadcbccb553a142eb0808e3099f20bf544b4564ab18e28466`; 277 lines matching `^## D-` | `sha256sum`; `grep -c` |
| Candidate | `docs/coop/artifacts/provider-only-output-contract.v3.json` sha256 `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` (git-tracked) | `sha256sum`; `git ls-files --error-unmatch` |
| Claude verdict | `docs/coop/artifacts/provider-only-output-contract.v3.review-independent.claude2.json` sha256 `9670abc02373f3971572b78f439ec570c358f41ad4b0a0cf256091d6e57d5f82` | `sha256sum` |
| Codex verdict | `docs/coop/artifacts/provider-only-output-contract.v3.review-independent.codex.json` sha256 `0bb9f9c8ffecfa2dd039eb029c96388bc27160a7e7a0238618368e8d78eac603` | `sha256sum` |
| Review prompt | `docs/coop/artifacts/provider-only-output-contract.v3.review-prompt.md` sha256 `7036f62eb13546642f2d6ffe3905e38edd8199912b587d2e4e4c6d2f1cffd77b` | `sha256sum` |
| D-056 pinned turn-2 subject (the definition of the five gates per D-133) | `docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md` sha256 `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82` | `sha256sum`; COORD `## D-133` "Decision type" |
| Recording commits | D-136 `d204ba0`; D-140 `cb6d10e`; D-085 `0963beb`; D-236 `fc688b1` | `git log --oneline --all` |

The question the owner is asked (DECISIONS-NEEDED.md §B, item B2, verbatim): "**DR-133** provider-only TypeScript output — candidate `provider-only-output-contract.v3` (D-136). Same question." where B1's question is "Open Class A (application-grade acceptance, no express reservation) → then a SATISFIED-GRADE cycle? Or what must change first?" The same section records: "(Grok's standing instruction was "do not SATISFY DR-117/131/133"; I will not open Class A without your word.)" The standing instruction itself is at `HANDOFF.D-000-orchestrator-live.txt` line 83: "Do not SATISFY DR-117 / DR-131 / DR-133 (Class A unopened)."

---

## 1. The file-08 row, every cell verbatim

Source: file 08 line 314 (table header at line 280: `| ID | Decision | Owner / decision authority | Source pin / affected sections | Required acceptance evidence | Status | Blueprint impact |`).

| Cell | Verbatim bytes |
|---|---|
| ID | `DR-133` |
| Decision | `Provider-only TypeScript component output` |
| Owner / decision authority | `Semantic / component architecture` |
| Source pin / affected sections | `[`COORDINATOR-DECISIONS.md`](../../coop/COORDINATOR-DECISIONS.md) D-132 (user-made ADOPTED, commit `d3efe3c…`); D-134 (CONSENT Claude `0b672021…` / Codex `ec305159…`); recorded goal [file 12 §4](12-architecture-completion-goal.md) (file 12 has no authority)` |
| Required acceptance evidence | `Independently reviewed contract stating: the TypeScript component returns semantic facts and Coverage only; the host owns rules, policy, findings, and admission; component-emitted findings are refused, with retained negative tests.` |
| Status | `**OPEN** — accepted design-contract candidate recorded (D-136): [`provider-only-output-contract.v3.json`](../../coop/artifacts/provider-only-output-contract.v3.json) `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` — `CANDIDATE-NOT-APPLIED`, binds NOTHING. Not eligible in kind today (D-133). Not SATISFIED.` |
| Blueprint impact | `Hard blocker for preview `analyze`; condition 2 SATISFIED-requiring per D-134` |

Related file-08 bytes that name DR-133:

- Condition-2 snapshot row, line 415 (excerpt): `DR-131 and DR-133 added OPEN by D-135; neither is eligible in kind today (D-133).` The same row opens `**5 of 32 `SATISFIED`** — 24 `OPEN`, 1 `DECIDED-V1-NOT-INTEGRATED`, 2 `PROPOSED-CLOSED-FOR-REVIEW`.` and ends `| **NOT MET** |`.
- One-sentence summary, line 424 (tail): `condition 2 remains 5 of 32 SATISFIED.`
- DR-G23 row, line 359 (harness cell): `named: harness.DR-G23.provider-well-formed-admission.preview (D-147; not authored; not QUALIFIED). hostile-but-well-formed admission corpus (DR-133 NT-3, NT-5)`; status cell `OPEN`; owner `Protocol + semantic owners`.
- DR-G20 row, line 356, and DR-G21 row, line 357: neither cell contains the string `DR-133` or any `NT-` token (measured: `grep -n 'NT-1\|NT-3\|NT-5\|NT-6'` on file 08 hits only lines 359–363). Naming of DR-133 NT classes at G20/G21 lives in `gate-harness-naming.v6.json` (D-145), not in those cells — see §5 Gate 3.

---

## 2. D-136 — the recording entry and its reservation

COORD `## D-136 — Record provider-only-output-contract.v3 as DR-133 candidate` (line 5748), verbatim in full:

> - **Date:** 2026-08-15
> - **Status:** **ADOPTED 2026-08-15.** Turn 3 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX. Claude 2 (`artifacts/coordinator-decisions.D-136.review-adversarial.claude2.turn3.json`, `313565b135d13ba205f1c26983935d719d9d969f035ff993bd6fe5483bd7f80d`). Codex (`artifacts/coordinator-decisions.D-136.review-adversarial.codex.turn3.json`, `af91a1b1b7444df847160da91bfa990919a7ddd3147dd79e59bf94402b124265`). Subject `coordinator-decisions.D-136.turn3.draft.md` `0656ac390b3691f83cff0fd31a16160bfa344558bcc86eeb45c7477588c85185`.
> - **Decision type:** RULE-GOVERNED. Records independent dual ACCEPT of `provider-only-output-contract.v3.json` `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309`. Same no-cell-edit branch as D-116 / D-131.
> - **Decision:** Record v3 as DR-133's accepted design-contract candidate. DR-133 stays OPEN. No SATISFIED. Candidate binds NOTHING. D-056 Class A is not opened. Advisories CLAUDE-POOC-V3-ADV-1, CLAUDE-POOC-V3-ADV-2, and POOCV3-ADV1 travel as honesty work (ADV-2 and POOCV3-ADV1 are one class). **Owed later MF-6:** update DR-133's "no contract exists" clause. Not performed here.
> - **Readiness effect:** Zero. Condition 2 stays 4 of 32. Condition 5 last.
> - **Reversibility:** Total only before the owed MF-6 or another dependent act. Overturn: C-D136.
> - **Commit:** C-D136.

**The reservation, as recorded.** D-136's Decision paragraph contains the sentence `D-056 Class A is not opened.` That is the only Class-A language in the entry. D-136 does not contain the phrase "express reservation", does not measure the D-001 T2-02 property, and does not use the words "application-grade". (Contrast D-015 for DR-102, which recorded `**Route-A acceptance property:** MET.` — §7 below.) COORD's later text describes DR-117's D-137 as carrying an "express reservation" (D-168 line 7093: `Gate 1 Class A remains false under D-137's express reservation.`; D-207 line 9097: `under D-137's express reservation.`). COORD contains no sentence attributing an express reservation to D-136 by name (measured: `grep -n "D-136's\|under D-136"` returns no line). Whether D-136's `D-056 Class A is not opened.` is itself an "express reservation" in the T2-02 sense is not stated in the record; §6 Gate 1 sets out the bytes on both sides.

**The owed MF-6 was performed.** COORD `## D-140 — File 08 MF-6: record accepted candidate on DR-133` (line 5934), Decision: `Replace DR-133's Status-cell clause `no contract exists` with the recorded D-136 candidate in the established form (link, full digest, `CANDIDATE-NOT-APPLIED`, binds NOTHING). DR-133 stays `OPEN`. Not SATISFIED. Class A not opened. H2 / DR-131 is not performed. Does not change condition-2 arithmetic. Does not authorize `docs/v2/implementation/`.` (line-wrap joined) Reversibility: `Total only before a later dependent DR-133 cell rewrite or SATISFIED-grade application.`

---

## 3. The candidate's own authority fields

Source: `provider-only-output-contract.v3.json` (`ef2a7416…`), top-level keys.

| Field | Verbatim |
|---|---|
| `artifact` | `provider-only-output-contract.v3` |
| `version` | `3` |
| `date` | `2026-08-15` |
| `documentClass` | `DESIGN-CONTRACT-CANDIDATE` |
| `registerRow` | `DR-133` |
| `status` | `CANDIDATE-NOT-APPLIED` |
| `reviewStatus` | `AWAITING-INDEPENDENT-REVIEW` |
| `sealRecommendation` | `DO-NOT-SEAL` |
| `binds` | `NOTHING` |
| `authorityClaim` | `This artifact PROPOSES the DR-133 preview TypeScript provider-only output law. It applies nothing, edits no register row, seals nothing, marks nothing SATISFIED, and does not authorize docs/v2/implementation/. D-056 Class A is not opened.` |
| `purpose` | **not in the record** — the candidate has no `purpose` key. (Its `basedOn.relation` reads: `Predecessor ACCEPT by Codex, REJECT by Claude at 0 blockers / 3 SHOULD-FIX. This successor repairs CLAUDE-POOC-V2-SF1, SF2, SF3.`) |
| `doesNot` (all nine members) | `Does not SATISFY DR-133.` / `Does not open D-056 Class A.` / `Does not invent §7.1 identity recipes.` / `Does not advertise SARIF.` / `Does not choose default packs (DR-131).` / `Does not succeed P-1/P-2/G3 (DR-117).` / `Does not rewrite file 01's general closed boundary.` / `Does not change the TypeScript provider wire.` / `Does not authorize docs/v2/implementation/.` |

What the candidate answers (for the owner's read of substance):

- `registerRowQuoted.acceptanceEvidenceCellVerbatim` equals the live Required-acceptance-evidence cell byte-for-byte (both verdicts measured this; Claude `measurements.registerRowAudit.acceptanceEvidenceCellVerbatimMatches: true`; Codex `measurements`: "The quoted DR-133 acceptance-evidence cell compares equal byte-for-byte"). The candidate pins file 08 at `7585325d…` (the 2026-08-15 snapshot; live file 08 is `e503b75b…` — the row's Required-acceptance-evidence cell text is unchanged, see §1).
- Obligation decomposition `OBL-1` / `OBL-2` / `OBL-3` maps the three cell fragments to `outputLaw.admittedSemanticOutputs` = `["semanticFact","coverage"]`, `outputLaw.hostOwned` (eight members: `rules`, `policy`, `findings`, `admissionOfFacts`, `admissionOfCoverage`, `finding production from admitted facts`, `planAdmission`, `runFinalization`), and `outputLaw.refusal` (two-limb rule; eleven `namedInstances`).
- `negativeTests.status` = `specified-classes-not-executed`; seven classes `NT-1`..`NT-7`; `wirePin` = `docs/coop/artifacts/delivery.v2.json` `47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3`.
- `governingBoundary` pins file 01 `40ab9a3e5713c9294a2c90a4b0e7c46065277b1e7013ed5023027a90c10193e1`, section `Closed structural responsibility boundary`, with `designDelta`: `For the D-002 preview TypeScript *provider* role only, this contract narrows file 01's 'Component may return' column. File 01 remains the general closed boundary. This is a recorded preview-role delta, not a silent rewrite of file 01.`

---

## 4. The two independent verdicts

### 4a. Claude 2 — `provider-only-output-contract.v3.review-independent.claude2.json` (`9670abc0…`)

| Field | Verbatim |
|---|---|
| `verdict` | `ACCEPT` |
| `verdictRule` | `ACCEPT only at 0 blockers and 0 SHOULD-FIX. Measured: 0 blockers, 0 SHOULD-FIX, 2 advisories. Advisories do not block.` |
| `acceptanceGrade` | `ACCEPT as an independently reviewed DR-133 design-contract candidate. This verdict does not apply the artifact, does not mark DR-133 SATISFIED, and does not open D-056 Class A. The artifact's own status fields govern: CANDIDATE-NOT-APPLIED, DO-NOT-SEAL, binds NOTHING.` |
| `blockers` / `shouldFix` | `[]` / `[]` |
| `counts` | `{"blockers": 0, "shouldFix": 0, "advisories": 2, "attacksRun": 15, "attacksLanded": 2, ...}` |
| `advisories[0].id` | `CLAUDE-POOC-V3-ADV-1` — the `wirePin` note names only one of DR-011-R04's two halves; `whyNotBlocking`: "I tested the omitted half and it does not move the pin either." |
| `advisories[1].id` | `CLAUDE-POOC-V3-ADV-2` — v1's `identityDependencies` block (routing to DR-006 / D-077 / D-078) "still has no successor"; `whyNotBlocking`: "Nothing false is asserted in its place." |
| `whatThisAcceptanceDoesNotDo[2]` | `Does not open D-056 Class A. Whether this recording constitutes application-grade T2-02 acceptance is a coordinator determination, not this reviewer's.` |
| `whatThisAcceptanceDoesNotDo[4]` | `Does not adopt the file-01 preview-role delta. The artifact proposes it; recording it is a separate reviewed act.` |
| `coordinatorSummary` (last sentence) | `This acceptance is of the artifact as an independently reviewed design-contract candidate only; it applies nothing, marks no row SATISFIED, opens no D-056 class, and executes no test.` |
| `independence.priorParticipationDisclosed` (opening) | `I authored the v1 review (2 blockers, 3 SHOULD-FIX) and the v2 review (0 blockers, 3 SHOULD-FIX). v3 repairs my own three v2 findings, so accepting it means accepting my own positions back.` |

### 4b. Codex — `provider-only-output-contract.v3.review-independent.codex.json` (`0bb9f9c8…`)

| Field | Verbatim |
|---|---|
| `verdict` | `ACCEPT` |
| `blockerCount` / `shouldFixCount` / `advisoryCount` | `0` / `0` / `1` |
| `reviewScope` | `DR-133 provider-only-output-contract v3 only. This review does not mark DR-133 SATISFIED, open D-056 Class A, mint D-096 (A), authorize docs/v2/implementation/, apply or seal the candidate, or edit file 08 or COORD.` |
| `advisories[0].id` | `POOCV3-ADV1` — title `Parked identity dependencies remain implicit rather than routed`; `whyNotShouldFix`: "No operative v3 rule invents, computes, binds, or relies on a parked identity recipe." |
| `obligationAudit` | `OBL-1` `PASS`, `OBL-2` `PASS`, `OBL-3` `PASS` |
| `namedInstanceCoverage.uncoveredCount` | `0` |
| `authorityOfThisVerdict` | `{"marksDR133Satisfied": false, "opensD056ClassA": false, "mintsD096AGrant": false, "authorizesImplementation": false, "appliesOrSealsCandidate": false, ...}`; `note`: `This ACCEPT verdict is review evidence on the candidate bytes only. It leaves DR-133 OPEN and supplies no owner grant, row disposition, implementation authority, application, or seal.` |
| `summary` (last sentence) | `DR-133 remains OPEN and this verdict authorizes nothing.` |

### 4c. Reservation-language sweep (the D-015 / D-003 method applied to these bytes)

D-001's T2-02 property (COORD line 181, under `## D-001`): "a candidate is applicable when its independent review returns **0 blockers AND grants application-grade acceptance with no express reservation** — no candidate-only limitation, no EXPRESSLY-NOT-FOR-APPLICATION language, no named apply-condition left undischarged on the record". Measured over the three files:

- `provider-only-output-contract.v3.json`: zero matches for `reserv`.
- Claude verdict: one match for `reserv` — the substring of `preserved` inside ADV-2's `whyNotBlocking` ("structural law preserved from V1 and file 01"); not an acceptance reservation. One match for `candidate only` — the `coordinatorSummary` sentence quoted in 4a ("as an independently reviewed design-contract candidate only"). Zero matches for `DO-NOT-APPLY`, `NOT-FOR-APPLICATION`, `CANDIDATE-ONLY`.
- Codex verdict: one match for `reserv` — the substring of `preserves` inside `obligationAudit[0].detail` ("previewNarrowing preserves the non-semantic protocol surfaces"); not an acceptance reservation. Zero matches for `candidate only` / `candidate-only`; the `authorityOfThisVerdict.note` reads "review evidence on the candidate bytes only".
- Named apply-conditions: neither verdict names one (Claude `blockers: []`, `shouldFix: []`; Codex `blockerCount: 0`, `shouldFixCount: 0`). Both carry advisories that D-136 routes as "honesty work".

What that sweep does and does not show: it shows 0 blockers on both sides and no DO-NOT-APPLY / NOT-FOR-APPLICATION token. It also shows that both verdicts describe their own grade as candidate-level ("design-contract candidate only"; "review evidence on the candidate bytes only") and that Claude's verdict expressly hands the application-grade determination to the coordinator. Whether those sentences are a "candidate-only limitation" under T2-02 is the question the owner is being asked; the packet does not decide it.

---

## 5. The D-056 five gates — definition and per-gate evidence for DR-133

D-133 (COORD line 5621) makes the pinned D-056 turn-2 subject the definition: `D-056's pinned turn-2 subject `dfb0c2af…` already states eligibility as a property; its five gates govern.` and `A later SATISFIED re-record may use D-056 only when all five gates in the pinned turn-2 subject hold for that row at that later cycle.`

Gate text, verbatim from `coordinator-decisions.D-056.turn2.draft.md` (`dfb0c2af…`), section `## Eligibility (narrow)`:

> 1. One of:
>    - **Class A.** An independently accepted design contract exists at 0 blockers with application-grade acceptance and no express reservation (D-001 T2-02), recorded by a D-000 entry; the row's lead label is `OPEN`.
>    - **Class B.** The lead label is `DECIDED-V1-NOT-INTEGRATED` because a D-000 entry already recorded the product/architecture decision (D-006, D-008, D-009, or a later sibling of that form).
> 2. Every remaining acceptance-evidence member is **only** harness *execution*, fixture *execution*, or qualification *measurement*. Authoring of fixtures, schemas, successors, actor-joins, missing design, or still-UNDECIDED numbers is **not** a remainder this amendment may split.
> 3. Each such remainder is already named as a condition-4 / DR-G* obligation with an owner. Naming a harness identifier is not itself SATISFIED.
> 4. A dedicated later D-000 cycle plus independent SATISFIED-GRADE review of *that row* accepts the split and records SATISFIED under this amendment.
> 5. An MF-6 file-08 cell edit records SATISFIED and removes the cell's conflicting "until executed" / "until measured" SATISFIED-bar. This entry is not that edit.

The same subject's Decision clause 5: `**Authoring fixtures and harness *specifications* remains lawful design work now.** Execution remains qualification.`

### Gate 1 (Class A) — evidence

| Limb | Bytes for | Bytes against / unresolved |
|---|---|---|
| "independently accepted design contract exists at 0 blockers" | Claude `blockers: []`; Codex `blockerCount: 0` (§4). | — |
| "recorded by a D-000 entry" | D-136 ADOPTED 2026-08-15, dual CONSENT 0/0 (§2). | — |
| "the row's lead label is `OPEN`" | file 08 line 314 Status cell begins `**OPEN**` (§1). | — |
| "application-grade acceptance" | D-147 Decision: `CANDIDATE-NOT-APPLIED is not a Class A bar (D-085).` D-085's Eligibility recitation for DR-102 (draft `f0c6e54e…` §"Eligibility recitation") found Gate 1 on `D-015: Route-A acceptance property MET; zero acceptance reservations.` | Claude `acceptanceGrade`: `ACCEPT as an independently reviewed DR-133 design-contract candidate.`; Claude `whatThisAcceptanceDoesNotDo[2]`: `Whether this recording constitutes application-grade T2-02 acceptance is a coordinator determination, not this reviewer's.`; Codex `note`: `review evidence on the candidate bytes only`. D-136 records no T2-02 measurement. D-147 (2026-08-15): `Gate 1's application-grade / no-express-reservation limb is not established here.` No later COORD entry establishes it (every later DR-133 mention is a `Does not SATISFY DR-133` / `Gate 1 Class A is not opened` denial — e.g. D-240, D-279, D-292). |
| "no express reservation" | Sweep §4c: no DO-NOT-APPLY / NOT-FOR-APPLICATION token; no named apply-condition. | Candidate `authorityClaim` ends `D-056 Class A is not opened.`; `doesNot[1]` `Does not open D-056 Class A.`; D-136 `D-056 Class A is not opened.`; Claude `coordinatorSummary` "design-contract candidate only". |
| Venue for a lift | D-168 (DR-117 sibling, line 7093–7095): `Venue for any later lift is a reviewed coordinator act, not an artifact.` STATUS.2026-08-26.md §2 item 1 (line 22): `COORD says the only venue for a lift is "a reviewed coordinator act, not an artifact" — a D-000 cycle recording *application-grade, no-express-reservation* (T2-02) acceptance.` The same line characterises every candidate recording as carrying `an express reservation ("CANDIDATE-NOT-APPLIED; Class A not opened")` — that is the orchestrator's 2026-08-27 summary, not COORD text; COORD's own attribution of "express reservation" is to D-137 only (§2 above). | The record does not state whether a coordinator act may find application grade over verdicts that describe themselves as candidate-grade, or whether a fresh application-grade review is required (open question §9). |

**Gate 1 today:** not established on the record. Three of its five limbs hold on bytes (0 blockers; D-000 recording; `OPEN`); the "application-grade" and "no express reservation" limbs are exactly what B2 asks the owner to rule on.

### Gate 2 (remainder is only execution / measurement) — evidence

- D-147 Decision (2026-08-15): `NT-3 and NT-5 leftover-design closes: remainder is G23 execution. After this act, D-056 Eligibility gates 2 and 3 hold for all seven DR-133 NT classes.`
- D-144 Decision: `NT-1/2/4/6/7 are capable-of-riding G20/G21 after a later D-086 successor names them. NT-3 and NT-5 remain leftover-design.` (superseded for NT-3/NT-5 by D-147).
- The candidate's own `negativeTests.status` = `specified-classes-not-executed`.
- **Later measurement that bears on clause-5 fixture authoring (post-dates D-147):**
  - **G23 (NT-3, NT-5):** `g23-leftover-join.v8.json` (`498324e5…`, recorded D-240, line 11391) `summary.leftoverDesign` = `[]`; `OBL-G23-FX-AUTHORING` `leftoverDesign: false`, `rideStanding: qualification-at-named-gate`; `OBL-NT35-UNNAMED-REMAINDER-CLOSED` reason: `D-147 closed leftover-design of NT-3 and NT-5 as unnamed remainders; remainder is G23 execution.` Fixture implementations exist: `g23-fixture-corpus.v4.json` (`b3fce9f5…`, D-239) carries four NT-class members (one `"class": "NT-3"`, three `"class": "NT-5"`) with `id` values `G23.nt3.factcandidate-findingLikeResult`, `G23.nt5.coverage-narrows`, `G23.nt5.coverage-widens`, and `G23.nt5.unknown-to-covered`, each with four per-platform `path` entries under `docs/coop/artifacts/fixtures/g23.v4/` (`macos-arm64`, `macos-x86_64`, `linux-x86_64`, `linux-arm64`).
  - **G21 (NT-1, NT-2, NT-6):** `g21-leftover-join.v13.json` (`058717f5…`, recorded D-292, line 16035 — current at HEAD) `summary.leftoverDesign` = `["OBL-G21-FX-AUTHORING"]`. Its `OBL-G21-FX-AUTHORING` reason: `g21-fixture-corpus.v1 (D-241; dual ACCEPT 0/0) authors implementations of NT-1 and NT-2.` and `Remaining namedCorpusWhenFixturesExist classes are unauthored: live-cell crash/panic/timeout/resource/malformed/truncated/duplicate/EOF/process-tree/recovery, CC-1 through CC-4, remaining CC-5 injections, CC-6 through CC-11, DR-133 NT-6, and FC-NC-CA1-PROCESS-TREE. D-056 Decision clause 5: authoring those remaining fixtures remains design work.` and `Does not author NT-6.` The join's `namedCorpusWhenFixturesExist.dr133` = `["NT-1","NT-2","NT-6"]`.
  - **G20 (NT-4, NT-7):** `g20-leftover-join.v6.json` (`d666a449…`, recorded D-269, line 13708) `summary.leftoverDesign` = `["OBL-G20-FX-AUTHORING"]`; reason: `Occupancy v2 namedCorpusNotAuthored carries one live harness-cell corpus class. Fixtures are unauthored.` The join's bytes contain neither `DR-133` nor `NT-4` nor `NT-7` (measured). The G20 occupancy `harness.DR-G20.component-operability.v2.json` (`2c4823b7…`, D-217) does contain `DR-133 NT-4, NT-7 execute here (provider-only-output-contract.` and `It does not execute NT-4 or NT-7 by existing.` No `g20-fixture-corpus.*` artifact exists in `docs/coop/artifacts/` (measured: `ls | grep g20-fixture` returns nothing; only `g20-input-corpus.v1` and `g20-named-corpus-catalog.v1/v2`).

**Gate 2 today:** COORD's last explicit finding is D-147's "gates 2 and 3 hold for all seven DR-133 NT classes" (2026-08-15). The current G21 join (D-292, 2026-08-27) measures `DR-133 NT-6` as an unauthored fixture under `D-056 Decision clause 5: authoring those remaining fixtures remains design work.` The record does not reconcile these two statements for DR-133. NT-4/NT-7 fixture authoring status at G20 is not in the record (the G20 join does not name them). This is the material risk to a SATISFIED-GRADE cycle — see §8.

### Gate 3 (each remainder named at a condition-4 / DR-G* obligation with an owner) — evidence

- D-145 Decision: `DR-G21 names DR-133 NT-1, NT-2, NT-6. DR-G20 names DR-133 NT-4, NT-7.` Artifact `gate-harness-naming.v6.json` (`b74e3009…`) contains `DR-133 NT-4, NT-7 execute here (provider-only-output-contract.` and `DR-133 NT-1, NT-2, NT-6 execute here (provider-only-output-contract.`.
- D-147 Decision: `Assign `DR-G23 PROVIDER-WELL-FORMED-ADMISSION`. It owns DR-133 NT-3 and NT-5 only.` File 08 line 359 carries the row with owner `Protocol + semantic owners`.
- Owners in file 08: DR-G20 `Component architecture + CLI/operability` (line 356); DR-G21 `Supervisor + protocol + operability` (line 357); DR-G23 `Protocol + semantic owners` (line 359).
- Note: `gate-harness-naming.v7.json` (`d4e373f3…`) and `gate-harness-naming.v8.json` (`c79538c4…`) exist in the artifacts directory and v8 also carries the DR-133 naming sentences, but COORD contains zero occurrences of either filename (measured `grep -c`). The last gate-harness-naming version named by a COORD heading is v6 (D-145, line 6066). Their standing is not in the record.

**Gate 3 today:** holds on the record for all seven classes (D-145 + D-147), with the file-08 caveat in §1 that the G20/G21 cells themselves do not carry the DR-133 NT names.

### Gate 4 (dedicated SATISFIED-GRADE cycle for this row) — evidence

Not performed. No COORD heading records DR-133 SATISFIED (the only SATISFIED re-records are D-085 DR-102, D-089 DR-115, D-091 DR-119, D-092 DR-123, D-236 DR-104 — file 08 line 415). D-147: `Gate 4 reserves eligibility to a later dedicated SATISFIED-GRADE cycle.`

### Gate 5 (MF-6 cell edit recording SATISFIED) — evidence

Not performed. Status cell reads `**OPEN** …` (§1). D-140's reversibility clause anticipates it: `Total only before a later dependent DR-133 cell rewrite or SATISFIED-grade application.`

---

## 6. The current DR-133 leftover-join

**There is no artifact whose filename matches `<lineage>-leftover-join.vN.json` with `registerRow` = `DR-133`.** Measured: `grep -l DR-133 *-leftover-join.v*.json` (excluding reviews) returns only the `g21-`, `g23-`, `g25-`, and `provider-` families. Of those:

- `provider-leftover-join.v4.json` (`0e31f5b5…`, recorded D-279 line 14592) has `registerRow: "DR-G10"`; its `registerRowNote` begins `registerRow is DR-G10 because this join remasures leftover-design of G10 after occupancy v2 (D-212).` It names DR-133 only in `OBL-DR133-NOT-STOLEN` (`leftoverDesign: false`, `rideStanding: rides-DR-133`, reason `G10 catalog does not SATISFY DR-133. Provider-only leftover remains on DR-133. This join does not steal that leftover and does not SATISFY DR-133.`). Despite the filename, it is the G10 join, not the DR-133 join.
- `g25-leftover-join.*` is a DR-131 (G25) family.

The DR-133 leftover-design measurements recorded in COORD are two `registerRow: "DR-133"` artifacts (both status `CANDIDATE-NOT-APPLIED`, `binds: NOTHING`):

### 6a. `provider-only-nt-gate-join.v6.json` (`93bc62d43751d8037aa2a696209eccbdee0ae3b3f11292d9a05be2bc245082a3`, recorded D-144, line 6029)

`authorityClaim`: `This artifact PROPOSES an execution-remainder join for some DR-133 NT classes and records which classes remain leftover-design. It does not close leftover-design. It does not make gates 2 and 3 hold. It applies nothing, marks nothing SATISFIED, and does not authorize docs/v2/implementation/.`
`purpose`: `Split product law (stays on v3) from test execution. Name which NT classes can ride existing G20/G21 corpus fragments, which cannot, and the owed later D-086 successor that must name the riding classes at those gates the way DR-102 CC-1..CC-11 are named at G21.`

`classes[]` (this artifact uses `classes`, not `obligations`; there is no `summary` key):

| id | name | existingGate | executionRemainder.rideStanding | leftoverDesign |
|---|---|---|---|---|
| `NT-1` | `unknown-Finding-frame` | `DR-G21` | `capable-of-riding` | `false` |
| `NT-2` | `extra-finding-member-on-closed-payload` | `DR-G21` | `capable-of-riding` | `false` |
| `NT-3` | `fact-candidate-masquerade` | `none` | `not-capable-of-riding` | `true` (`leftoverReason`: `Remains leftover-design pending an obligation whose corpus exercises this admission refusal.`) |
| `NT-4` | `policy-verdict-threshold-waiver` | `DR-G20` | `capable-of-riding` | `false` |
| `NT-5` | `coverage-domain-mutation` | `none` | `not-capable-of-riding` | `true` (same `leftoverReason`) |
| `NT-6` | `d9-exit-hosttermination-refused` | `DR-G21` | `capable-of-riding` | `false` |
| `NT-7` | `planAdmission-refused` | `DR-G20` | `capable-of-riding` | `false` |

The NT-3/NT-5 `true` flags were measured 2026-08-15 and were closed as unnamed remainders by D-147 (`NT-3 and NT-5 leftover-design closes: remainder is G23 execution.`). No successor of this artifact exists (measured: no `provider-only-nt-gate-join.v7*` file; no COORD mention after D-146).

### 6b. `provider-only-admission-leftover.v1.json` (`eae27692b4d799df2bd6b2d16497b0cbe3378166b6b541bc77df1989b3181865`, recorded D-146, line 6103)

`authorityClaim`: `This artifact PROPOSES leftover-design work for DR-133 NT-3 and NT-5 only. It does not add a DR-G* row, does not change required-now 18, does not close leftover-design, does not open D-056 Class A, does not SATISFY DR-133, does not edit file 08, and does not authorize docs/v2/implementation/.`
`classes[]`: `NT-3` (`existingGate: none`, `residual: leftover-design: hostile-but-well-formed FactCandidate admission`), `NT-5` (`existingGate: none`, `residual: leftover-design: hostile-but-well-formed Coverage-domain admission`). `proposedObligation.status`: `candidate-not-adopted`, `proposedId`: `DR-G23 PROVIDER-WELL-FORMED-ADMISSION` — adopted by D-147 as the file-08 row at line 359.

### 6c. Where DR-133's execution remainders now sit (current gate joins at HEAD)

| Gate | Current join (recording) | `summary.leftoverDesign` | DR-133 classes carried | Fixture authoring status per join bytes |
|---|---|---|---|---|
| G23 | `g23-leftover-join.v8.json` `498324e5…` (D-240) | `[]` | NT-3, NT-5 | authored (D-237 implementations; D-239 per-platform copies); `OBL-G23-FX-AUTHORING` `leftoverDesign: false` |
| G21 | `g21-leftover-join.v13.json` `058717f5…` (D-292) | `["OBL-G21-FX-AUTHORING"]` | NT-1, NT-2, NT-6 | NT-1, NT-2 authored (D-241/D-243); **`DR-133 NT-6` listed among "unauthored"**; `Does not author NT-6.` |
| G20 | `g20-leftover-join.v6.json` `d666a449…` (D-269) | `["OBL-G20-FX-AUTHORING"]` | NT-4, NT-7 (named at the G20 occupancy v2 and naming v6, not in this join's bytes) | not in the record for NT-4/NT-7 (join names neither); join says `Fixtures are unauthored.` for its `one live harness-cell corpus class` |

---

## 7. Precedent: how Class A was found for DR-102 (the only Class A SATISFIED to date)

- D-015 (line 1201), DR-102's contract recording, measured the property at recording time: `**Route-A acceptance property:** MET. Reservation-language sweep of the VERDICT clean — three `reserv` hits, all forms of "preserve" … zero acceptance reservations. The subject carries 9, likewise none an acceptance reservation. No apply-conditions.` Note that D-015 recorded the row as staying `OPEN` "because the classes are specifications and no harness executes them."
- D-085 (line 3508), the SATISFIED-GRADE cycle, then recited Gate 1 as already met: `D-015: Route-A acceptance property MET; zero acceptance reservations. Lead label is `OPEN`.` (draft `f0c6e54e…` §"Eligibility recitation"). Advisories A-CPC2-01/02 were held to be "honesty work on a later successor; they are not acceptance-evidence members and were not reservations at D-015."
- D-003 (line 514) shows the same three-limb measurement for an applied artifact: `(1) independent review verdict `ACCEPT` at 0 blockers …; (2) application-grade with NO express reservation — a reservation-language sweep over the verdict file returns zero hits (no DO-NOT-APPLY, no candidate-only limitation, no application-warrant carve-out), in deliberate contrast to this lineage's v6 precedent whose verdict said "ACCEPT AS A CANDIDATE"; (3) no named apply-condition exists to discharge.`

Difference for DR-133: D-136 made no T2-02 measurement, and both v3 verdicts describe themselves as candidate-grade (§4). D-147 then stated `CANDIDATE-NOT-APPLIED is not a Class A bar (D-085)` — i.e., the artifact's own `status` field is not disqualifying — while also stating the application-grade limb "is not established here."

---

## 8. Pre-drafted T2-02 acceptance entry — DRAFT, not adopted, not dispatched

This is the shape of the COORD entry a "yes, open Class A" answer would send into a D-000 cycle. Bracketed items are placeholders the cycle would fill; nothing here is recorded. The number is not assigned (the last heading is D-292; the next number is assigned at recording).

```
## D-NNN — DR-133: T2-02 application-grade acceptance of provider-only-output-contract.v3 (Class A opened)

- **Date:** [date of adoption]
- **Status:** [DRAFT — awaiting dual adversarial review]
- **Decision type:** RULE-GOVERNED. Reviewed coordinator act (the venue D-168 names:
  "a reviewed coordinator act, not an artifact"). Not a SATISFIED re-record. Not an MF-6.
  Not a three-limb act. Performs the D-056 Gate 1 determination only.
- **Authority:** Owner ruling of [date], recorded verbatim: "[owner's words]". Row owner per
  file 08 line 314: `Semantic / component architecture`.
- **Subject:** `docs/coop/artifacts/provider-only-output-contract.v3.json`
  `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` (recorded D-136;
  cell recorded D-140). Verdicts: Claude 2
  `provider-only-output-contract.v3.review-independent.claude2.json`
  `9670abc02373f3971572b78f439ec570c358f41ad4b0a0cf256091d6e57d5f82` ACCEPT 0/0, advisories
  CLAUDE-POOC-V3-ADV-1, CLAUDE-POOC-V3-ADV-2; Codex
  `provider-only-output-contract.v3.review-independent.codex.json`
  `0bb9f9c8ffecfa2dd039eb029c96388bc27160a7e7a0238618368e8d78eac603` ACCEPT 0/0, advisory
  POOCV3-ADV1.
- **Route-A acceptance property (D-001 T2-02), measured:** (1) both independent verdicts
  ACCEPT at 0 blockers and 0 SHOULD-FIX; (2) reservation-language sweep: subject 0 `reserv`
  hits; Claude verdict 1 hit (`preserved`), Codex verdict 1 hit (`preserves`) — neither an
  acceptance reservation; no DO-NOT-APPLY, no NOT-FOR-APPLICATION token; (3) no named
  apply-condition on either verdict. Both verdicts describe their grade as candidate-level
  ("design-contract candidate only"; "review evidence on the candidate bytes only") and the
  Claude verdict states that application grade "is a coordinator determination, not this
  reviewer's". [ONE OF: (a) This act makes that determination: the candidate-level wording
  restates the artifact's status fields and is not a candidate-only limitation on acceptance;
  the property is MET. / (b) This act records fresh application-grade verdicts
  `[paths + sha256]` obtained under a review prompt that asks for application grade; the
  property is MET on those verdicts.]
- **Decision:** D-056 Eligibility Gate 1 (Class A) holds for DR-133: an independently
  accepted design contract exists at 0 blockers with application-grade acceptance and no
  express reservation, recorded by D-136; the lead label is `OPEN`. The D-136 sentence
  "D-056 Class A is not opened." is superseded for DR-133 by this entry. The candidate's
  `status` `CANDIDATE-NOT-APPLIED` is not a Class A bar (D-147, citing D-085). Advisories
  CLAUDE-POOC-V3-ADV-1, CLAUDE-POOC-V3-ADV-2, and POOCV3-ADV1 remain honesty work on a later
  successor; they are not acceptance-evidence members and are not reservations. This entry
  does not find Gates 2–5. [State Gate 2 standing explicitly: G23 leftoverDesign `[]`
  (D-240); G21 join v13 lists `DR-133 NT-6` unauthored (D-292); G20 join v6 does not name
  NT-4/NT-7 (D-269) — resolution: ONE OF (i) NT-6 (and NT-4/NT-7) fixture authoring is
  sequenced before the SATISFIED-GRADE cycle; (ii) owner rules those fixtures are execution
  remainder for DR-133 because the product law names the classes and the gates own them.]
  Marks nothing SATISFIED. Does not apply v3 (binds NOTHING stands). Does not adopt the
  file-01 preview-role delta (separate reviewed act per the Claude verdict). Does not edit
  file 08 [or: performs the cell edit in §9 as an MF-6 in the same act — owner's choice].
  Does not SATISFY DR-131 or DR-117. Does not authorize `docs/v2/implementation/`.
- **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32. Condition 5 last.
- **Reversibility:** Total before the dependent DR-133 SATISFIED-GRADE cycle. Overturn
  restores D-136's "D-056 Class A is not opened." as governing. Overturn: C-DNNN.
- **Commit:** C-DNNN.
```

Successor-audit note (memory: reviewers REJECT on deictic "This vK", bare version tokens, and claims contradicted by bytes): the draft above names every artifact by full filename and digest and does not claim Gate 2 holds.

---

## 9. The exact file-08 bytes that would change

**A Class A opening alone does not necessarily edit file 08.** D-136 and D-140 split recording (COORD-only, "no-cell-edit branch") from the cell edit (MF-6). If the owner wants the register to reflect the lift, the only DR-133 bytes that become stale are:

1. Line 314, Status cell, the clause `Not eligible in kind today (D-133).` — after Gate 1 is found, this clause is true only if Gates 2/3 fail; its replacement text is a DRAFT choice, e.g. `Class A opened (D-NNN); Gates 2–3 per [join citations]; SATISFIED-GRADE cycle not performed.` (wording not in the record).
2. Line 415, condition-2 row, the sentence `DR-131 and DR-133 added OPEN by D-135; neither is eligible in kind today (D-133).` — would need a DR-133-specific rewrite; DR-131's half is unaffected by B2.
3. Nothing else: the `**OPEN**` lead, the digest, `CANDIDATE-NOT-APPLIED`, `binds NOTHING`, `Not SATISFIED.`, and the Blueprint-impact cell stay true after a Gate-1-only act. The SATISFIED-GRADE cycle (Gate 4) and its MF-6 (Gate 5) would later replace the lead per the D-085 / D-236 form (`**SATISFIED <date> (D-NNN / D-056 Class A).**`) and rewrite line 415 to `6 of 32` and line 424's `condition 2 remains 5 of 32 SATISFIED.` — those are that later act's edits, not this one's.

---

## 10. Options and consequences

**Option 1 — Open Class A now by coordinator determination (draft §8 path (a)), then run the SATISFIED-GRADE cycle immediately.**
- Unblocks: Gate 1 for DR-133; the handoff's completion bar item (2) "DR-133 SATISFIED" (`HANDOFF.D-000-orchestrator-live.txt` line 3) becomes reachable.
- Consequence: the SATISFIED-GRADE reviewers must find Gates 2–3 from current bytes. The current G21 join (D-292) lists `DR-133 NT-6` as an unauthored fixture under clause 5, and the G20 join (D-269) does not name NT-4/NT-7. On the successor-audit precedent ("claims contradicted by bytes" → REJECT), a draft asserting "remainder is only execution" for all seven classes is exposed to a Gate-2 REJECT unless the cycle carries an explicit ruling on fixture authoring. Two reviewers' capacity is not the constraint (DECISIONS-NEEDED E3).
- Also carries: the Claude verdict's sentence that application grade "is a coordinator determination" — this option relies on that sentence; the Codex verdict has no equivalent sentence.

**Option 2 — Open Class A now, but sequence fixture authoring for NT-6 (and confirm NT-4/NT-7 at G20) before the SATISFIED-GRADE cycle.**
- Unblocks: same as Option 1, with Gate 2 measured clean before the row is put to SATISFIED-GRADE review.
- Consequence: fixture authoring is delegation item D1 (DECISIONS-NEEDED §D): NT-6's shape (a constructible extra member or out-of-vocabulary frame carrying a D9 class, exit number, or HostTermination — candidate `negativeTests.NT-6.input`) must be authored by someone; Grok's handoff line 81 says uniquely determined fixture bytes are exhausted. The owner would be answering D1 for at least this class at the same time. G21 corpus precedent exists (D-241/D-243 authored NT-1/NT-2 at dual ACCEPT 0/0).

**Option 3 — Re-review v3 (or a v4 successor) expressly for application grade first (draft §8 path (b)), then open Class A, then SATISFIED-GRADE.**
- Unblocks: removes the interpretive step over candidate-grade verdict wording; matches the D-015 / D-003 form ("verdict … zero hits").
- Consequence: one extra review cycle (two fresh verdicts on `ef2a7416…` or on a successor). A v4 successor would also be the natural place to land the three advisories (ADV-1 wirePin note; ADV-2 / POOCV3-ADV1 restore `identityDependencies` routing to DR-006 / D-077 / D-078). The Codex verdict's POOCV3-ADV1 `suggestion` reads `A later successor may restore explicit dependency routing for audit convenience without changing this contract's meaning or standing.`; the Claude verdict's ADV-2 `suggestion` reads `Restore the block in any successor.`; the Claude verdict's ADV-1 `suggestion` asks only to widen the wirePin note (`Widen the note to name both halves of R04 and say why neither moves the pin …`) — it contains no restore language. The phrase "may restore" appears in the Codex verdict only (measured: `grep -c 'may restore'` → claude2.json 0, codex.json 1). Neither verdict makes any of the three a bar (Claude `whyNotBlocking`; Codex `whyNotShouldFix`).

**Option 4 — Do not open Class A; state what must change first.**
- Candidates for "what must change", each from the record: (i) the advisories above; (ii) the file-01 preview-role delta recording (Claude verdict: "recording it is a separate reviewed act"); (iii) NT-6 / NT-4 / NT-7 fixtures; (iv) any substantive change to the output law the owner wants (the owner's D-132 words were `"Provider only — recommended"`).
- Consequence: DR-133 stays `OPEN`; Condition 2 stays 5 of 32; the handoff completion bar stays unmet on item (2).

**Option 5 — Defer DR-133 by explicit disposition.**
- STATUS §5 item 4 notes "a deferral disposition also satisfies Condition 2's wording for deferred items"; but D-134 placed DR-133 in the SATISFIED-requiring set (cardinality 23) and D-132's grant and the handoff bar both require DR-133 SATISFIED. A deferral would need a D-134 successor and would contradict the recorded goal; the record does not contain a deferral route for DR-133.

**Orchestrator recommendation:** Option 2 — open Class A by a reviewed coordinator act that cites both verdicts and D-147's "CANDIDATE-NOT-APPLIED is not a Class A bar", and sequence NT-6 fixture authoring (plus a byte check of NT-4/NT-7 at G20) before dispatching the SATISFIED-GRADE cycle, so that Gate 2 is measured from current joins rather than from D-147's 2026-08-15 sentence. This is a recommendation only; the determination is the owner's.

---

## 11. Open questions the bytes do not resolve

1. Whether a coordinator act may find "application-grade acceptance" over verdicts whose own text is candidate-grade (Claude: "design-contract candidate only"; Codex: "review evidence on the candidate bytes only"), or whether T2-02's "no candidate-only limitation" requires fresh verdicts. D-168 fixes the venue ("a reviewed coordinator act"), not the test.
2. Whether D-136's sentence `D-056 Class A is not opened.` is an "express reservation" in the T2-02 sense. COORD attributes an express reservation to D-137 (DR-117) but never to D-136 by name.
3. Gate 2 reconciliation: D-147 (2026-08-15) says gates 2 and 3 hold for all seven NT classes; `g21-leftover-join.v13` (D-292, 2026-08-27) lists `DR-133 NT-6` unauthored under clause 5. Which statement governs DR-133's Gate 2 today is not stated.
4. NT-4 / NT-7 fixture authoring at G20: `g20-leftover-join.v6` (D-269) names neither class; no `g20-fixture-corpus` artifact exists. Status not in the record.
5. `gate-harness-naming.v7.json` and `v8.json` exist in the artifacts directory with the DR-133 naming sentences but are named nowhere in COORD; whether they are drafts, withdrawn, or pending is not in the record.
6. Whether the Class A opening act should also perform the §9 cell edit (MF-6 in the same act) or stay COORD-only (D-136/D-140 pattern). Not determined by the record.
7. Whether the file-01 preview-role delta (`governingBoundary.designDelta`) needs its own recorded act before or as part of the SATISFIED-GRADE cycle (the Claude verdict calls it "a separate reviewed act"; no COORD entry has recorded it).
8. Disposition of advisories CLAUDE-POOC-V3-ADV-1, CLAUDE-POOC-V3-ADV-2, POOCV3-ADV1 at the lift: D-136 routes them as "honesty work"; the D-085 precedent treated A-CPC2-01/02 the same way and did not make them SATISFIED-bars. Whether the owner wants a v4 successor to land them first is a choice, not a record fact.
